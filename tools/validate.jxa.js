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
  if(w.worksKey || w.title){
    const key = w.worksKey || w.title;
    const artist = A.filter(function(x){ return x.id === w.artistId; })[0];
    if(artist && !artist.works.some(function(wk){ return wk.t === key; }))
      warns.push(tag + ": worksKey/title '" + key + "' not in artist works array (no back-link)");
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
  ", venues: " + VEN.length + ", catalog: " + CAT.length + " (tier1: " + CAT.filter(function(w){ return w.tier === 1; }).length + ")");
if(warns.length) out.push("WARNINGS:\n  " + warns.join("\n  "));
out.push(errs.length ? "ERRORS:\n  " + errs.join("\n  ") : "ALL REFERENCES VALID");
out.join("\n");
