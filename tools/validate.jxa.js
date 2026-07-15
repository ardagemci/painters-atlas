// data integrity check via macOS JavaScriptCore:
//   osascript -l JavaScript tools/validate.jxa.js
ObjC.import("Foundation");
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

// parse-check app.js without executing it
try { new Function(read(base + "js/app.js")); out.push("app.js: syntax OK"); }
catch(e){ out.push("app.js SYNTAX ERROR: " + e.message); }

// load data files (eval = syntax + execution check)
["taxonomy.js","artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js","artists-14.js","artists-15.js"]
  .forEach(f => { try { eval(read(base + "js/" + f)); } catch(e){ out.push(f + " ERROR: " + e.message); } });

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
  if(!a.facts || a.facts.length < 3) errs.push("artist " + a.id + ": <3 facts");
});

const warns = [];

// venue registry + artwork catalog integrity (ARTWORK_SCHEMA v1)
try { eval(read(base + "js/venues.js")); } catch(e){ out.push("venues.js ERROR: " + e.message); }
try { eval(read(base + "js/catalog-1.js")); } catch(e){ out.push("catalog-1.js ERROR: " + e.message); }
try { eval(read(base + "js/catalog-2.js")); } catch(e){ out.push("catalog-2.js ERROR: " + e.message); }
try { eval(read(base + "js/catalog-3.js")); } catch(e){ out.push("catalog-3.js ERROR: " + e.message); }
try { eval(read(base + "js/catalog-4.js")); } catch(e){ out.push("catalog-4.js ERROR: " + e.message); }
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
try { eval(read(base + "js/lists-1.js")); } catch(e){ out.push("lists-1.js ERROR: " + e.message); }
const LST = window.EDITORIAL_LISTS || [];
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
  });
  if(!l.cover || !seenW[l.cover]) errs.push(tag + ": cover must be one of the list's own works");
});
if(LST.length && LST.filter(function(l){ return l.featured; }).length < 3)
  warns.push("fewer than 3 featured lists for the homepage");

// museum notes integrity
try { eval(read(base + "js/museums-1.js")); } catch(e){ out.push("museums-1.js ERROR: " + e.message); }
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
// every venue holding catalog works must carry at least a hook
VEN.forEach(function(v){
  if(v.id === "private-collection" || v.id === "lost" || v.id === "unknown") return;
  if(CAT.some(function(w){ return w.museum && w.museum.id === v.id; }) && !MN[v.id])
    errs.push("venue " + v.id + " holds works but has no museum note (hook required)");
});

// Tier 1 artist overlay integrity
try { eval(read(base + "js/tier1-artists.js")); } catch(e){ out.push("tier1-artists.js ERROR: " + e.message); }
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

// influence graph integrity
try { eval(read(base + "js/influences.js")); } catch(e){ out.push("influences.js ERROR: " + e.message); }
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
M.forEach(x => { if(!A.some(a => a.movements.includes(x.id)) && !M.some(c => c.parent === x.id)) warns.push("movement " + x.id + " has no artists"); });
T.forEach(x => { if(!A.some(a => a.techniques.includes(x.id)) && !T.some(c => c.parent === x.id)) warns.push("technique " + x.id + " has no artists"); });
N.forEach(x => { if(!A.some(a => a.nation === x.id)) warns.push("nation " + x.id + " has no artists"); });
E.forEach(x => { if(!A.some(a => a.eras.includes(x.id))) warns.push("era " + x.id + " has no artists"); });

out.push("artists: " + A.length + ", movements: " + M.length + ", techniques: " + T.length +
  ", eras: " + E.length + ", nations: " + N.length + ", painter styles: " + Object.keys(styleNames).length +
  ", influence edges: " + (window.INFLUENCES || []).length +
  ", venues: " + VEN.length + ", catalog: " + CAT.length + " (tier1: " + CAT.filter(function(w){ return w.tier === 1; }).length + ")" +
  ", daily pool: " + DAILY.length +
  ", museum notes: " + Object.keys(window.MUSEUM_NOTES || {}).length +
  ", lists: " + (window.EDITORIAL_LISTS || []).length +
  " (featured: " + (window.EDITORIAL_LISTS || []).filter(function(l){ return l.featured; }).length + ")" +
  ", tier1 artists: " + Object.keys(window.TIER1 || {}).length +
  " (arcs: " + Object.keys(window.TIER1 || {}).filter(function(k){ return window.TIER1[k].arc; }).length + ")");
if(warns.length) out.push("WARNINGS:\n  " + warns.join("\n  "));
out.push(errs.length ? "ERRORS:\n  " + errs.join("\n  ") : "ALL REFERENCES VALID");
out.join("\n");
