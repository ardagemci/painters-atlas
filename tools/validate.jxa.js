// data integrity check via macOS JavaScriptCore:
//   osascript -l JavaScript tools/validate.jxa.js
//
// Exits 1 on any error or load failure, 0 only on a clean run. Until 2026-08-17
// this script ended by *returning* its report, so osascript exited 0 on broken
// data and every automated green it reported was unconditional (backlog C7).
// The report therefore goes to stdout explicitly, before the exit.
ObjC.import("Foundation");
ObjC.import("stdlib");
function emit(s){
  const d = $.NSString.alloc.initWithUTF8String(s + "\n").dataUsingEncoding($.NSUTF8StringEncoding);
  $.NSFileHandle.fileHandleWithStandardOutput.writeData(d);
}
function read(p){
  const s = $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null);
  if(s.isNil()) throw new Error("cannot read " + p);
  return ObjC.unwrap(s);
}
// resolve the project root from this script's own path (works from any checkout location)
const argv = ObjC.unwrap($.NSProcessInfo.processInfo.arguments).map(a => ObjC.unwrap(a));
const me = argv.find(a => String(a).endsWith("validate.jxa.js")) || "tools/validate.jxa.js";
const base = String(me).replace(/tools\/+validate\.jxa\.js$/, "");
var window = {};
const out = [];
/* A file that will not parse is not a warning. Its records are simply absent,
   so every reference check below then runs on less data and can still come back
   clean — a parse failure used to make this script *more* likely to pass. Load
   failures are tracked separately from `errs` so the verdict can say the run was
   inconclusive rather than valid. */
/* C2. Numbered data families are DISCOVERED, never listed.

   `catalog-5.js` was named in five separate places and `artists-18.js` in three.
   A new `catalog-6.js` is then picked up by whichever lists someone remembers
   and silently skipped by the rest — and the quiet ones are the rights audit and
   the validator, where a miss is least visible. This session hit it directly:
   adding artists-18.js meant editing three files, and forgetting one would have
   left 4 painters invisible to a tool that still reported success.

   Sorted numerically, not lexically, so catalog-10 follows catalog-9. */
function familyFiles(prefix){
  const dir = base + "js";
  /* Each element comes back as an ObjC string; ObjC.unwrap on the ARRAY does not
     unwrap its members, and String() on one yields "[id __NSCFString]". Unwrap
     per element or the filter silently matches nothing — which is how the first
     version of this returned zero files and reported "artists: 0". */
  const all = (ObjC.unwrap($.NSFileManager.defaultManager
    .contentsOfDirectoryAtPathError(dir, $())) || []).map(f => ObjC.unwrap(f));
  return all
    .filter(f => new RegExp("^" + prefix + "-\\d+\\.js$").test(f))
    .sort((a, b) => (+a.match(/\d+/)[0]) - (+b.match(/\d+/)[0]));
}

const loadErrs = [];
function loadFail(msg){ loadErrs.push(msg); }

// parse-check app.js without executing it
try { new Function(read(base + "js/app.js")); out.push("app.js: syntax OK"); }
catch(e){ loadFail("app.js SYNTAX ERROR: " + e.message); }

// load data files (eval = syntax + execution check)
["taxonomy.js"].concat(familyFiles("artists"))
  .forEach(f => { try { eval(read(base + "js/" + f)); } catch(e){ loadFail(f + " ERROR: " + e.message); } });
/* The gallery pool. Loaded so an artist's optional `hero` can be checked against
   the works that actually have an image, rather than against a title list. */
try { eval(read(base + "js/artworks.js")); } catch(e){ loadFail("artworks.js ERROR: " + e.message); }

const A = window.ARTISTS || [], M = window.MOVEMENTS || [], T = window.TECHNIQUES || [],
      E = window.ERAS || [], N = window.NATIONS || [];
const errs = [];
const ids = list => { const s = {}; list.forEach(x => s[x.id] = 1); return s; };
const mIds = ids(M), tIds = ids(T), eIds = ids(E), nIds = ids(N);

const appSrc = read(base + "js/app.js");
const styleNames = {};
let m, re = /^(\w+)\(ctx,w,h,P,R\)/gm;
while((m = re.exec(appSrc))) styleNames[m[1]] = 1;

function dup(list, label){
  const seen = {};
  list.forEach(x => { if(seen[x.id]) errs.push(label + ": duplicate id " + x.id); seen[x.id] = 1; });
}
dup(A,"artist"); dup(M,"movement"); dup(T,"technique"); dup(E,"era"); dup(N,"nation");

M.forEach(x => { if(x.parent && !mIds[x.parent]) errs.push("movement " + x.id + ": bad parent " + x.parent);
  if(!styleNames[x.style]) errs.push("movement " + x.id + ": unknown style " + x.style);
  if(!x.palette || x.palette.length < 4) errs.push("movement " + x.id + ": bad palette"); });
T.forEach(x => { if(x.parent && !tIds[x.parent]) errs.push("technique " + x.id + ": bad parent " + x.parent);
  if(!styleNames[x.style]) errs.push("technique " + x.id + ": unknown style " + x.style); });
E.forEach(x => { if(!styleNames[x.style]) errs.push("era " + x.id + ": unknown style " + x.style); });

const req = ["id","name","years","born","nation","eras","movements","techniques","style","palette","tagline","works","life","career","outside","facts"];
A.forEach(a => {
  req.forEach(k => { if(a[k] === undefined || a[k] === "") errs.push("artist " + a.id + ": missing " + k); });
  if(!nIds[a.nation]) errs.push("artist " + a.id + ": bad nation " + a.nation);
  (a.eras||[]).forEach(e => { if(!eIds[e]) errs.push("artist " + a.id + ": bad era " + e); });
  (a.movements||[]).forEach(v => { if(!mIds[v]) errs.push("artist " + a.id + ": bad movement " + v); });
  (a.techniques||[]).forEach(v => { if(!tIds[v]) errs.push("artist " + a.id + ": bad technique " + v); });
  if(!styleNames[a.style]) errs.push("artist " + a.id + ": unknown style " + a.style);
  if(!a.palette || a.palette.length !== 5 || a.palette.some(c => !/^#[0-9a-f]{6}$/i.test(c)))
    errs.push("artist " + a.id + ": bad palette " + (a.palette||[]).join(","));
  if(!a.works || a.works.length < 3) errs.push("artist " + a.id + ": <3 works");
  /* An optional `hero` names the gallery work used as this artist's social
     preview (tools/build_seo.jxa.js, artistImage). A hero that does not resolve
     falls back silently to the works[] ordering, which looks like it worked — so
     a typo here must fail loudly rather than quietly serve a different picture. */
  if(a.hero && !(((window.ARTWORKS || {})[a.id] || {})[a.hero]))
    errs.push("artist " + a.id + ": hero \"" + a.hero + "\" is not one of this artist's gallery works");
  /* A4. Optional acknowledgment beside the single-valued flag. Kept short
     because it renders inline on the identity line, and required to be prose
     rather than a second nation id — it qualifies the filing, it does not
     duplicate it. */
  if(a.nationNote !== undefined){
    if(typeof a.nationNote !== "string" || !a.nationNote.trim())
      errs.push("artist " + a.id + ": nationNote must be a non-empty string");
    else if(a.nationNote.length > 90)
      errs.push("artist " + a.id + ": nationNote is " + a.nationNote.length + " chars (max 90)");
  }
  if(!a.facts || a.facts.length < 3) errs.push("artist " + a.id + ": <3 facts");
});

const warns = [];

// venue registry + artwork catalog integrity (ARTWORK_SCHEMA v1)
try { eval(read(base + "js/venues.js")); } catch(e){ loadFail("venues.js ERROR: " + e.message); }
familyFiles("catalog").forEach(function(f){
  try { eval(read(base + "js/" + f)); } catch(e){ loadFail(f + " ERROR: " + e.message); }
});
const VEN = window.VENUES || [], CAT = window.CATALOG || [];
const VENUE_TYPES = { museum:1, church:1, palace:1, site:1 };
dup(VEN, "venue"); dup(CAT, "artwork");
const vIds = ids(VEN), aIdsMap = ids(A), catIds = ids(CAT);
VEN.forEach(function(v){
  if(!VENUE_TYPES[v.type]) errs.push("venue " + v.id + ": bad type " + v.type);
  if(!/^[a-z0-9-]+$/.test(v.id)) errs.push("venue " + v.id + ": non-kebab id");
});
CAT.forEach(function(w){
  const tag = "artwork " + w.id;
  if(!/^[a-z0-9-]+$/.test(w.id)) errs.push(tag + ": non-kebab id");
  if(w.tier !== 1 && w.tier !== 2) errs.push(tag + ": bad tier");
  if(!aIdsMap[w.artistId]) errs.push(tag + ": unknown artist " + w.artistId);
  if(!w.year || !w.year.display || typeof w.year.sort !== "number") errs.push(tag + ": bad year");
  (w.movements || []).forEach(function(m){ if(!mIds[m]) errs.push(tag + ": bad movement " + m); });
  (w.techniques || []).forEach(function(t){ if(!tIds[t]) errs.push(tag + ": bad technique " + t); });
  if(w.nation && !nIds[w.nation]) errs.push(tag + ": bad nation " + w.nation);
  if(w.museum && w.museum.id && !vIds[w.museum.id]) errs.push(tag + ": unknown venue " + w.museum.id);
  (w.related || []).forEach(function(r){
    if(r === w.id) errs.push(tag + ": self-related");
    if(!catIds[r]) errs.push(tag + ": related id not in catalog: " + r);
  });
  if(w.image && w.image.status === "pd" && (w.image.src || "").indexOf("/wikipedia/commons/") === -1)
    errs.push(tag + ": pd image not Commons-hosted");
  if(w.image && ["pd","copyright","none"].indexOf(w.image.status) === -1)
    errs.push(tag + ": bad image status " + w.image.status);
  if(w.tier === 1){
    const c = w.coords || {};
    ["F","D","E","C","M"].forEach(function(k){
      if(typeof c[k] !== "number" || c[k] < -100 || c[k] > 100 || c[k] !== Math.round(c[k]))
        errs.push(tag + ": coords." + k + " missing or out of range");
    });
    const words = (w.description || "").split(/\s+/).filter(Boolean).length;
    if(words < 30 || words > 110) errs.push(tag + ": description " + words + " words (30–110)");
    if(!w.notice || w.notice.length !== 3) errs.push(tag + ": needs exactly 3 notice bullets");
    if(!w.tags || w.tags.length < 3) errs.push(tag + ": needs ≥3 tags");
    if(!w.image || w.image.status === "none") errs.push(tag + ": tier 1 needs an image");
  }
  if(w.tier === 1 && (w.worksKey || w.title)){
    const key = w.worksKey || w.title;
    const artist = A.filter(function(x){ return x.id === w.artistId; })[0];
    if(artist && !artist.works.some(function(wk){ return wk.t === key; }))
      warns.push(tag + ": worksKey/title '" + key + "' not in artist works array (no back-link)");
  }
});

// Painting of the Day must always have a deep, displayable pool.
const DAILY = CAT.filter(function(w){
  return w.tier === 1 && w.description && w.notice && w.notice.length &&
    w.image && w.image.status === "pd" && w.image.src && aIdsMap[w.artistId];
});
if(DAILY.length < 30) errs.push("daily pool too small: " + DAILY.length + " (needs at least 30)");
DAILY.forEach(function(w){
  const words = (w.description || "").split(/\s+/).filter(Boolean).length;
  if(words < 60 || words > 90)
    errs.push("daily " + w.id + ": description " + words + " words (60–90)");
});

// editorial lists integrity
try { eval(read(base + "js/lists-1.js")); } catch(e){ loadFail("lists-1.js ERROR: " + e.message); }
const LST = window.EDITORIAL_LISTS || [];
/* B2 Actuality. One story per month, dated to the month it was reported — the
   cadence IS the product, and two entries in one month with a gap beside them
   is the failure it is easiest to ship without noticing. */
try { eval(read(base + "js/actuality-1.js")); } catch(e){ loadFail("actuality-1.js ERROR: " + e.message); }
const ACTL = window.ACTUALITY || [];
(function(){
  const seen = {};
  ACTL.forEach(function(e){
    const tag = "actuality " + e.id;
    if(!/^[a-z0-9-]+$/.test(e.id || "")) errs.push(tag + ": non-kebab id");
    if(["list","article"].indexOf(e.kind) === -1) errs.push(tag + ": kind must be list or article");
    if(!/^\d{4}-\d{2}-\d{2}$/.test(e.published || "")) errs.push(tag + ": published must be YYYY-MM-DD");
    if(!e.source || !e.source.name || !e.source.url) errs.push(tag + ": needs a named, linked source");
    if(e.kind === "list" && !ids(LST)[e.listId]) errs.push(tag + ": listId not in EDITORIAL_LISTS: " + e.listId);
    if(e.kind === "article" && !catIds[e.workId]) errs.push(tag + ": workId not in catalog: " + e.workId);
    if(e.coverStyle && !aIdsMap[e.coverStyle]) errs.push(tag + ": coverStyle is not an artist id: " + e.coverStyle);
    const month = String(e.published || "").slice(0, 7);
    if(seen[month]) errs.push(tag + ": a second entry for " + month + " (already: " + seen[month] + ") — one story per month");
    else seen[month] = e.id;
  });
  /* and no missing months between the first and last */
  const months = ACTL.map(function(e){ return String(e.published || "").slice(0,7); }).filter(Boolean).sort();
  if(months.length > 1){
    let cur = months[0];
    while(cur < months[months.length - 1]){
      let y = +cur.slice(0,4), m = +cur.slice(5,7) + 1;
      if(m > 12){ m = 1; y++; }
      cur = y + "-" + (m < 10 ? "0" + m : m);
      if(cur <= months[months.length-1] && months.indexOf(cur) === -1)
        errs.push("actuality: no entry for " + cur + " — the cadence is monthly and has a hole");
    }
  }
})();

dup(LST, "list");
LST.forEach(function(l){
  const tag = "list " + l.id;
  if(!/^[a-z0-9-]+$/.test(l.id)) errs.push(tag + ": non-kebab id");
  if(!l.title || l.title.length > 64) errs.push(tag + ": missing or over-64-char title");
  const lw = (l.lede || "").split(/\s+/).filter(Boolean).length;
  if(lw < 15 || lw > 60) errs.push(tag + ": lede " + lw + " words (15–60)");
  if(!l.works || l.works.length < 5 || l.works.length > 14) errs.push(tag + ": needs 5–14 works");
  const seenW = {};
  (l.works || []).forEach(function(e){
    if(!catIds[e.id]) errs.push(tag + ": work not in catalog: " + e.id);
    if(seenW[e.id]) errs.push(tag + ": duplicate work " + e.id);
    seenW[e.id] = 1;
    if(!e.note || e.note.length > 120) errs.push(tag + ": note missing or over 120 chars for " + e.id);
    /* B2. Optional longer paragraph, used by Actuality lists. Bounded at both
       ends: under 200 chars it is not a paragraph and belongs in `note`, over
       900 it is an article and belongs on its own page. */
    if(e.essay !== undefined){
      if(typeof e.essay !== "string" || e.essay.trim().length < 200)
        errs.push(tag + ": essay for " + e.id + " must be a paragraph of 200+ chars (use note for one-liners)");
      else if(e.essay.length > 900)
        errs.push(tag + ": essay for " + e.id + " is " + e.essay.length + " chars (max 900)");
    }
  });
  if(!l.cover || !seenW[l.cover]) errs.push(tag + ": cover must be one of the list's own works");
});
if(LST.length && LST.filter(function(l){ return l.featured; }).length < 3)
  warns.push("fewer than 3 featured lists for the homepage");

/* E4. The onboarding deck opens by picking one anchor per F×D quadrant from the
   works it can actually show (Tier 1 + coordinates + a public-domain image). Two
   of those four quadrants are currently held up by ONE picture each — see
   docs/TASTE_AUDIT.md §7. Losing it degrades the deck's opening silently, with
   no error anywhere, so the count is reported on every run.

   A warning rather than an error: the thin state is pre-existing and largely
   structural (29 of 35 abstract works are in copyright and cannot be shown), so
   failing the build would block on a condition no data edit can clear. */
(function(){
  const deck = CAT.filter(function(w){
    return w.tier === 1 && w.coords && w.image && w.image.status === "pd" && w.image.src;
  });
  [["F+D+",1,1],["F+D-",1,-1],["F-D+",-1,1],["F-D-",-1,-1]].forEach(function(q){
    const name = q[0], sf = q[1], sd = q[2];
    const n = deck.filter(function(w){ return sf * w.coords.F >= 25 && sd * w.coords.D >= 25; }).length;
    if(n === 0) errs.push("deck quadrant " + name + " has NO qualifying work — buildDeck cannot anchor it");
    else if(n < 2) warns.push("deck quadrant " + name + " rests on a single work (" + n + "); losing it degrades the deck silently");
  });
  const abstract = deck.filter(function(w){ return w.coords.F >= 30; }).length;
  if(abstract < 3) warns.push("deck pool has only " + abstract + " works at F>=30; buildDeck's §6.2 quota asks for 3");
})();

// museum notes integrity
try { eval(read(base + "js/museums-1.js")); } catch(e){ loadFail("museums-1.js ERROR: " + e.message); }
const MN = window.MUSEUM_NOTES || {};
Object.keys(MN).forEach(function(vid){
  const tag = "museum-note " + vid, n = MN[vid];
  if(!vIds[vid]) errs.push(tag + ": unknown venue id");
  if(!n.hook || n.hook.length > 64) errs.push(tag + ": hook missing or over 64 chars");
  if(n.essay){                                 /* full note: essay implies founded */
    if(!n.founded) errs.push(tag + ": has essay but missing founded");
    const ew = n.essay.split(/\s+/).filter(Boolean).length;
    if(ew < 100 || ew > 180) errs.push(tag + ": essay " + ew + " words (100–180)");
  }
  if(n.photo && (!n.photo.src || n.photo.src.indexOf("https://upload.wikimedia.org/wikipedia/commons/") !== 0))
    errs.push(tag + ": photo src must be Commons-hosted");
  if(n.photo && !n.photo.page) errs.push(tag + ": photo missing source page");
  if(!n.photo) warns.push(tag + ": no building photo (generative cover fallback)");
});
// photo credits: the attribution registry must cover every photograph we show
// (js/photo-credits.js, generated by tools/build_photo_credits.py). An uncredited
// attribution-required photograph is a licence breach, so it is an error, not a warning.
try { eval(read(base + "js/photo-credits.js")); } catch(e){ loadFail("photo-credits.js ERROR: " + e.message); }
const PC = window.PHOTO_CREDITS || {}, IC = window.IMAGE_CREDITS || {};
Object.keys(MN).forEach(function(vid){
  if(!MN[vid].photo) return;
  const c = PC[vid];
  if(!c){ errs.push("photo-credit " + vid + ": museum photograph has no credit record"); return; }
  const tag = "photo-credit " + vid;
  if(!c.license) errs.push(tag + ": missing licence name");
  if(!c.page) errs.push(tag + ": missing Commons file page");
  if(c.required){
    if(!c.author) errs.push(tag + ": licence requires attribution but no author recorded");
    if(!c.licenseUrl) errs.push(tag + ": licence requires attribution but no licence URL");
  }
});
Object.keys(PC).forEach(function(vid){
  if(!vIds[vid]) errs.push("photo-credit " + vid + ": unknown venue id");
  else if(!MN[vid] || !MN[vid].photo) warns.push("photo-credit " + vid + ": credit for a photograph no longer shown");
});
Object.keys(IC).forEach(function(t){
  const c = IC[t], tag = "image-credit " + t;
  if(t.indexOf("File:") !== 0) errs.push(tag + ": key must be a Commons File: title");
  if(!c.author) errs.push(tag + ": missing author");
  if(!c.license) errs.push(tag + ": missing licence name");
  if(!c.licenseUrl) errs.push(tag + ": missing licence URL");
  if(!c.page) errs.push(tag + ": missing Commons file page");
});

// every venue holding catalog works must carry at least a hook
VEN.forEach(function(v){
  if(v.id === "private-collection" || v.id === "lost" || v.id === "unknown") return;
  if(CAT.some(function(w){ return w.museum && w.museum.id === v.id; }) && !MN[v.id])
    errs.push("venue " + v.id + " holds works but has no museum note (hook required)");
});

// Phase 1.5: personas, onboarding data, deck-pool gates (ADMIRE_SPEC §6.2)
try { eval(read(base + "js/personas.js")); } catch(e){ loadFail("personas.js ERROR: " + e.message); }
const PS = window.PERSONAS || [];
dup(PS, "persona");
if(PS.length < 12 || PS.length > 16) errs.push("personas: launch set must be 12-16, have " + PS.length);
PS.forEach(function(ps){
  const tag = "persona " + ps.id;
  if(!ps.name || !ps.blurb) errs.push(tag + ": missing name/blurb");
  if(!ps.palette || ps.palette.length !== 4) errs.push(tag + ": palette must be 4 tones");
  if(ps.kind === "specific"){
    ["F","D","E","C","M"].forEach(function(a){
      const c = (ps.coords || {})[a];
      if(typeof c !== "number" || c < -100 || c > 100) errs.push(tag + ": coords." + a + " missing/range");
    });
    if(ps.sig && ps.sig.movement && !mIds[ps.sig.movement]) errs.push(tag + ": bad sig movement");
  } else if(["contradiction","eclectic","time-traveler"].indexOf(ps.rule) < 0) errs.push(tag + ": bad general rule");
});
if((window.TASTE_QUESTIONS || []).length !== 5) errs.push("taste questions: need exactly 5");
(window.TASTE_QUESTIONS || []).forEach(function(Q){
  if(!Q.options || Q.options.length !== 4) errs.push("question " + Q.id + ": needs 4 options");
});
if((window.TASTE_TONES || []).length < 16) errs.push("taste tones: need at least 16");
(window.TASTE_TONES || []).forEach(function(t){
  if(!/^#[0-9a-f]{6}$/i.test(t.hex || "")) errs.push("tone " + t.id + ": bad hex");
});
const POOL = CAT.filter(function(w){ return w.tier === 1 && w.coords && w.image && w.image.status === "pd" && w.image.src; });
const NONEU = { japan:1, usa:1, mexico:1 };
if(POOL.filter(function(w){ return w.coords.F >= 30; }).length < 3) errs.push("deck pool: needs >=3 works with F>=+30");
if(POOL.filter(function(w){ return NONEU[w.nation]; }).length < 2) errs.push("deck pool: needs >=2 non-European works");
if(POOL.filter(function(w){ return w.year.sort < 1700; }).length < 3) errs.push("deck pool: needs >=3 pre-1700");
if(POOL.filter(function(w){ return w.year.sort >= 1800 && w.year.sort < 1880; }).length < 3) errs.push("deck pool: needs >=3 19th-century");
if(POOL.filter(function(w){ return w.year.sort >= 1880 && w.year.sort <= 1935; }).length < 3) errs.push("deck pool: needs >=3 early-modern");
["F","D","E","C","M"].forEach(function(a){
  if(POOL.filter(function(w){ return w.coords[a] >= 40; }).length < 2) warns.push("deck pool: <2 works with " + a + ">=+40");
  if(POOL.filter(function(w){ return w.coords[a] <= -40; }).length < 2) warns.push("deck pool: <2 works with " + a + "<=-40");
});
[[1,1],[1,-1],[-1,-1],[-1,1]].forEach(function(qd){
  if(!POOL.some(function(w){ return qd[0]*w.coords.F >= 25 && qd[1]*w.coords.D >= 25; }))
    warns.push("deck pool: empty F×D quadrant " + qd.join(","));
});

// Tier 1 artist overlay integrity
try { eval(read(base + "js/tier1-artists.js")); } catch(e){ loadFail("tier1-artists.js ERROR: " + e.message); }
const T1 = window.TIER1 || {};
const GN_TYPES = { artist:1, movement:1, technique:1, work:1 };
Object.keys(T1).forEach(function(aid){
  const tag = "tier1 " + aid, t = T1[aid];
  if(!aIdsMap[aid]) errs.push(tag + ": unknown artist");
  const words = (t.why || "").split(/\s+/).filter(Boolean).length;
  if(words < 25 || words > 75) errs.push(tag + ": why is " + words + " words (25–75)");
  if(!t.lookFor || t.lookFor.length < 3 || t.lookFor.length > 5) errs.push(tag + ": lookFor needs 3–5 traits");
  (t.lookFor || []).forEach(function(s){ if(s.length > 60) errs.push(tag + ": trait too long: " + s.slice(0, 30) + "…"); });
  if(!t.goNext || t.goNext.length < 2 || t.goNext.length > 5) errs.push(tag + ": goNext needs 2–5 entries");
  (t.goNext || []).forEach(function(g){
    if(!GN_TYPES[g.t]) errs.push(tag + ": goNext bad type " + g.t);
    const ok = (g.t === "artist" && aIdsMap[g.id]) || (g.t === "movement" && mIds[g.id]) ||
               (g.t === "technique" && tIds[g.id]) || (g.t === "work" && catIds[g.id]);
    if(!ok) errs.push(tag + ": goNext unresolved " + g.t + "/" + g.id);
    if(!g.why) errs.push(tag + ": goNext " + g.id + " missing why");
  });
  const c = t.coords || {};
  ["F","D","E","C","M"].forEach(function(k){
    if(typeof c[k] !== "number" || c[k] < -100 || c[k] > 100) errs.push(tag + ": coords." + k + " missing/out of range");
  });
  if(t.arc){
    if(t.arc.length < 5 || t.arc.length > 12) errs.push(tag + ": arc needs 5–12 acts, has " + t.arc.length);
    t.arc.forEach(function(act, i){
      const atag = tag + " act " + (i + 1);
      if(!act.y || !act.t) errs.push(atag + ": missing year or title");
      if((act.t || "").length > 48) errs.push(atag + ": title over 48 chars");
      const aw = (act.text || "").split(/\s+/).filter(Boolean).length;
      if(aw < 20 || aw > 80) errs.push(atag + ": text " + aw + " words (20–80)");
      if((act.works || []).length > 4) errs.push(atag + ": max 4 work chips");
      (act.works || []).forEach(function(wid){ if(!catIds[wid]) errs.push(atag + ": work not in catalog: " + wid); });
    });
  }
});

var infGrounding = { ungrounded: 0, sourced: 0 };
// influence graph integrity
try { eval(read(base + "js/influences.js")); } catch(e){ loadFail("influences.js ERROR: " + e.message); }
const aIds = ids(A), EDGE_TYPES = { taught:1, influenced:1, befriended:1, rivaled:1, partners:1 };
const seenEdges = {};
(window.INFLUENCES || []).forEach(function(e, i){
  if(!aIds[e[0]]) errs.push("influence " + i + ": unknown artist " + e[0]);
  if(!aIds[e[1]]) errs.push("influence " + i + ": unknown artist " + e[1]);
  if(!EDGE_TYPES[e[2]]) errs.push("influence " + i + ": unknown type " + e[2]);
  if(e[0] === e[1]) errs.push("influence " + i + ": self-loop " + e[0]);
  const key = [e[0], e[1]].sort().join("|");
  if(seenEdges[key]) errs.push("influence " + i + ": duplicate pair " + key);
  seenEdges[key] = 1;
});

/* E2 — every edge must be GROUNDED, and the ungrounded count may only fall.

   js/influences.js used to claim in its header that "every relationship is
   grounded in the artist bios elsewhere in the atlas". Measured on 2026-08-24
   that was false for 107 of 246 edges. The claim is now enforced instead of
   asserted: an edge is grounded if either endpoint's own prose names the other
   painter, or the edge carries a fourth element — a source string.

   This is a RATCHET, not a pass/fail. 107 edges are ungrounded today and
   failing the build on them would block every unrelated change until a research
   project finishes. What the ceiling stops is the thing that actually costs
   something: a NEW edge asserted with nothing behind it. The number can fall
   and the ceiling should be lowered when it does.

   The name matcher is deliberately strict — word-boundary, accent-folded, and
   with given names and ordinary words removed from the token set, because
   "David" matches three painters and "Still" is a word. A false negative here
   only asks for a source string, which is the safe direction to be wrong in. */
const INF_UNGROUNDED_CEILING = 107;
(function(){
  const STOP = {};
  ("della delle dalla van von der den del dei the and still young white black green " +
   "paul jean john hans carl karl anna maria pierre henri louis frans juan luis jose david thomas james " +
   "william george peter mary jacob joseph francis charles albert edward robert richard michael andrea " +
   "antonio giovanni pietro alfaro clemente auguste marie").split(" ").forEach(function(w){ STOP[w] = 1; });

  function fold(s){
    return String(s == null ? "" : s).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }
  const tokens = {}, prose = {};
  A.forEach(function(a){
    const ts = {};
    [a.name, a.id.replace(/-/g, " ")].forEach(function(src){
      fold(src).split(/[\s.\-]+/).forEach(function(t){
        if(t.length > 3 && !STOP[t]) ts[t] = 1;
      });
    });
    tokens[a.id] = Object.keys(ts);
    prose[a.id] = fold([a.tagline, a.life, a.career, a.outside].concat(a.facts || []).join(" "));
    if(!tokens[a.id].length)
      warns.push("influence grounding: artist " + a.id + " has no distinctive name token, so no edge of theirs can be attested by prose");
  });
  function names(text, aid){
    return (tokens[aid] || []).some(function(t){
      return new RegExp("\\b" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b").test(text);
    });
  }
  let ungrounded = 0, sourced = 0;
  (window.INFLUENCES || []).forEach(function(e, i){
    const tag = "influence " + i + " (" + e[0] + " -> " + e[1] + ")";
    const src = e[3];
    if(src !== undefined){
      if(typeof src !== "string") { errs.push(tag + ": source must be a string"); return; }
      if(src.length < 20) { errs.push(tag + ": source is " + src.length + " chars — a stub source is worse than none"); return; }
      sourced++;
      return;                                   // a real source grounds the edge
    }
    if(!prose[e[0]] || !prose[e[1]]) return;    // unknown artist: already an error above
    if(!names(prose[e[0]], e[1]) && !names(prose[e[1]], e[0])) ungrounded++;
  });
  infGrounding = { ungrounded: ungrounded, sourced: sourced };
  if(ungrounded > INF_UNGROUNDED_CEILING)
    errs.push("influence graph: " + ungrounded + " edges are neither attested in artist prose nor sourced, above the ceiling of " +
              INF_UNGROUNDED_CEILING + ". A new edge must name its ground — write the relationship into a bio, or give the edge a source string.");
  else if(ungrounded < INF_UNGROUNDED_CEILING)
    warns.push("influence graph: ungrounded edges down to " + ungrounded + " from a ceiling of " + INF_UNGROUNDED_CEILING +
               " — lower INF_UNGROUNDED_CEILING in tools/validate.jxa.js to keep the ratchet tight");
})();
M.forEach(x => { if(!A.some(a => a.movements.includes(x.id)) && !M.some(c => c.parent === x.id)) warns.push("movement " + x.id + " has no artists"); });
T.forEach(x => { if(!A.some(a => a.techniques.includes(x.id)) && !T.some(c => c.parent === x.id)) warns.push("technique " + x.id + " has no artists"); });
N.forEach(x => { if(!A.some(a => a.nation === x.id)) warns.push("nation " + x.id + " has no artists"); });
E.forEach(x => { if(!A.some(a => a.eras.includes(x.id))) warns.push("era " + x.id + " has no artists"); });

out.push("artists: " + A.length + ", movements: " + M.length + ", techniques: " + T.length +
  ", eras: " + E.length + ", nations: " + N.length + ", painter styles: " + Object.keys(styleNames).length +
  ", influence edges: " + (window.INFLUENCES || []).length +
  " (ungrounded: " + infGrounding.ungrounded + ", sourced: " + infGrounding.sourced + ")" +
  ", venues: " + VEN.length + ", catalog: " + CAT.length + " (tier1: " + CAT.filter(function(w){ return w.tier === 1; }).length + ")" +
  ", daily pool: " + DAILY.length +
  ", museum notes: " + Object.keys(window.MUSEUM_NOTES || {}).length +
  ", photo credits: " + Object.keys(window.PHOTO_CREDITS || {}).length +
  " (attribution required: " + Object.keys(window.PHOTO_CREDITS || {}).filter(function(k){ return window.PHOTO_CREDITS[k].required; }).length +
  "), artwork image credits: " + Object.keys(window.IMAGE_CREDITS || {}).length +
  ", personas: " + (window.PERSONAS || []).length +
  ", lists: " + (window.EDITORIAL_LISTS || []).length +
  " (featured: " + (window.EDITORIAL_LISTS || []).filter(function(l){ return l.featured; }).length + ")" +
  ", tier1 artists: " + Object.keys(window.TIER1 || {}).length +
  " (arcs: " + Object.keys(window.TIER1 || {}).filter(function(k){ return window.TIER1[k].arc; }).length + ")");
if(warns.length) out.push("WARNINGS:\n  " + warns.join("\n  "));
if(loadErrs.length) out.push("LOAD FAILURES — a data file did not parse, so every check above ran on incomplete data:\n  " + loadErrs.join("\n  "));
/* "ALL REFERENCES VALID" is the clean-run string other tools match on; it is
   emitted only when nothing failed and nothing was missing. A load failure is
   never valid, only inconclusive — the checks did pass, on the wrong corpus. */
out.push(errs.length     ? "ERRORS:\n  " + errs.join("\n  ")
       : loadErrs.length ? "INCONCLUSIVE — reference checks ran on incomplete data"
       :                   "ALL REFERENCES VALID");
emit(out.join("\n"));
$.exit((errs.length || loadErrs.length) ? 1 : 0);
