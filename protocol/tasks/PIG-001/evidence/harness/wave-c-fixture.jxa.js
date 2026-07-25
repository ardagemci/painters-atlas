// PIG-001 U17 — run the FROZEN 24-query search fixture against the REAL data,
// using the REAL ranking source text extracted from js/app.js.
//   osascript -l JavaScript protocol/tasks/PIG-001/evidence/harness/wave-c-fixture.jxa.js
ObjC.import("Foundation");
function read(p){
  const s = $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null);
  if(s.isNil()) throw new Error("cannot read " + p);
  return ObjC.unwrap(s);
}
const argv = ObjC.unwrap($.NSProcessInfo.processInfo.arguments).map(a => ObjC.unwrap(a));
const me = argv.find(a => /wave-c-[a-z]+\.jxa\.js$/.test(String(a))) || "";
const base = String(me).replace(/protocol\/tasks\/PIG-001\/evidence\/harness\/wave-c-[a-z]+\.jxa\.js$/, "") || "./";

var window = {};
["taxonomy.js","artworks.js","venues.js","catalog-1.js","catalog-2.js","catalog-3.js","catalog-4.js",
 "tier1-artists.js",
 "artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js","artists-14.js",
 "artists-15.js","artists-16.js","lists-1.js","museums-1.js"]
  .forEach(f => { try{ eval(read(base + "js/" + f)); }catch(e){ console.log("LOAD ERROR " + f + ": " + e.message); } });

// ---- the exact top-of-app.js lookups the INDEX builder depends on ----
const A = window.ARTISTS, M = window.MOVEMENTS, T = window.TECHNIQUES,
      E = window.ERAS, N = window.NATIONS;
const byId = list => Object.fromEntries(list.map(x => [x.id, x]));
const Ax = byId(A);
const CAT = window.CATALOG || [];
const LISTS = window.EDITORIAL_LISTS || [];
const VEN = window.VENUES || [];
const VENUE_SENTINELS = { "private-collection":1, "lost":1, "unknown":1 };
const catByVenue = {};
CAT.forEach(w => { if(w.museum && w.museum.id) (catByVenue[w.museum.id] = catByVenue[w.museum.id] || []).push(w); });
const esc = s => String(s);

// ---- extract the REAL ranking code from js/app.js ----
const src = read(base + "js/app.js");
const from = src.indexOf("const INDEX = [");
const to = src.indexOf("function runSearch(q){");
if(from < 0 || to < 0) throw new Error("could not locate the search block in js/app.js");
const block = src.slice(from, to);
eval(block + "\nvar __S = { INDEX:INDEX, srRank:srRank, srSelect:srSelect, srKeys:srKeys, srWordStart:srWordStart,\n  SR_NONE:SR_NONE, SR_MAX:SR_MAX, SR_EXACT:SR_EXACT, SR_PREFIX:SR_PREFIX, SR_WORD:SR_WORD, SR_META:SR_META, SR_SUB:SR_SUB, SR_METASUB:SR_METASUB };");
const IDX = __S.INDEX;
const R_NONE = __S.SR_NONE, R_MAX = __S.SR_MAX, R_PREFIX = __S.SR_PREFIX, R_SUB = __S.SR_SUB;

// ---- reproduce runSearch's selection + display grouping (DOM-free) ----
function search(q){
  q = String(q).trim().toLowerCase();
  const scored = [];
  IDX.forEach(it => { const r = srRank(it, q); if(r < R_NONE) scored.push({ it, r }); });
  const hits = srSelect(scored, R_MAX);
  const groups = [];
  hits.forEach(it => {
    let g = groups.find(x => x.type === it.type);
    if(!g) groups.push(g = { type: it.type, items: [] });
    g.items.push(it);
  });
  const display = [];
  groups.forEach(g => g.items.forEach(it => display.push(it)));
  return { q, scored, hits, groups, display, total: scored.length };
}
function rankOf(res, it){ const s = res.scored.find(x => x.it === it); return s ? s.r : 9; }

// ---- the FROZEN fixture (unrouted/ux-requirements.md §3) ----
const FIX = [
  ["F1","vermeer","Johannes Vermeer","Artists","artist/johannes-vermeer"],
  ["F2","rembrandt","Rembrandt van Rijn","Artists","artist/rembrandt"],
  ["F3","frida kahlo","Frida Kahlo","Artists","artist/frida-kahlo"],
  ["F4","basquiat","Jean-Michel Basquiat","Artists","artist/jean-michel-basquiat"],
  ["F5","starry night","The Starry Night","Artworks","artwork/the-starry-night"],
  ["F6","guernica","Guernica","Artworks","artwork/guernica"],
  ["F7","mona lisa","Mona Lisa","Artworks","artwork/mona-lisa"],
  ["F8","las meninas","Las Meninas","Artworks","artwork/las-meninas"],
  ["F9","louvre","Musée du Louvre","Museums","museum/louvre"],
  ["F10","rijksmuseum","Rijksmuseum","Museums","museum/rijksmuseum"],
  ["F11","impressionism","Impressionism","Movements","movement/impressionism"],
  ["F12","cubism","Cubism","Movements","movement/cubism"],
  ["F13","fresco","Fresco","Techniques","technique/fresco"],
  ["F14","woodcut","Woodcut","Techniques","technique/woodblock"],
  ["F15","17th century","17th Century","Eras","era/17th-century"],
  ["F16","19th","19th Century","Eras","era/19th-century"],
  ["F17","japan","Japan","Nations","nation/japan"],
  ["F18","türkiye","Türkiye","Nations","nation/turkey"],
  ["F19","tate","Tate Modern","Museums","museum/tate-modern"],
  ["F20","art","Artemisia Gentileschi","Artists","artist/artemisia-gentileschi"],
  ["F21","son","Sonia Delaunay","Artists","artist/sonia-delaunay"],
  ["F22","min","Minneapolis Institute of Art","Museums","museum/minneapolis-institute-of-art"],
  ["F23","zzzqx",null,null,null],
  ["F24","qwertyuiopasdf",null,null,null]
];

let pass = 0, fail = 0;
console.log("INDEX size = " + IDX.length);
console.log("");
console.log("| # | query | expected #1 | actual #1 | route | tier | shown/total | pass |");
console.log("|---|---|---|---|---|---|---|---|");
FIX.forEach(([id, q, expName, expType, expHref]) => {
  const res = search(q);
  const top = res.display[0];
  let ok, actual;
  if(expName === null){
    ok = res.display.length === 0;
    actual = ok ? "(no match → .sr-empty)" : (top.name + " [" + top.type + "]");
  } else {
    ok = !!top && top.href === expHref;
    actual = top ? top.name + " [" + top.type + "]" : "(no match)";
  }
  if(ok) pass++; else fail++;
  console.log("| " + id + " | `" + q + "` | " + (expName || "(no match)") + " | " + actual +
    " | " + (top ? "#/" + top.href : "—") + " | " + (top ? rankOf(res, top) : "—") +
    " | " + res.display.length + "/" + res.total + " | " + (ok ? "PASS" : "**FAIL**") + " |");
});
console.log("");
console.log("FIXTURE: " + pass + "/" + FIX.length + " pass, " + fail + " fail");

// ---- R11 at the RANKING level (selection order, pre-grouping) and at the
// ---- DISPLAY level (post-grouping), measured separately and honestly.
console.log("");
console.log("R11 — every exact/prefix hit (tier<=1) ordered above every non-prefix hit (tier>=2):");
const ALLQ = FIX.map(f => f[1]).concat(["the","a","van","de","o","paris","picasso","moma","new york",
  "night","portrait","self","museum","gogh","monet","water","de la","la","new","san","st","mo","ar","ma"]);
let rankOK = 0, rankBad = [], dispOK = 0, dispBad = [];
ALLQ.forEach(q => {
  const res = search(q);
  const seq = arr => { let lastStrong = -1, firstWeak = 99;
    arr.forEach((it, i) => { const r = rankOf(res, it);
      if(r <= 1) lastStrong = i; if(r >= 2 && i < firstWeak) firstWeak = i; });
    return lastStrong < firstWeak; };
  if(seq(res.hits)) rankOK++; else rankBad.push(q);
  if(seq(res.display)) dispOK++; else dispBad.push(q);
});
console.log("  ranking order (what the cap selects): " + rankOK + "/" + ALLQ.length + " clean" +
  (rankBad.length ? "  VIOLATIONS: " + rankBad.join(", ") : ""));
console.log("  display order (after type grouping):  " + dispOK + "/" + ALLQ.length + " clean" +
  (dispBad.length ? "  cross-group interleave on: " + dispBad.join(", ") : ""));
console.log("");
console.log("F19-F22 visible lists (name/type/tier, display order):");
["tate","art","son","min"].forEach(q => {
  const res = search(q);
  console.log("  " + q + " → " + res.display.map(it => it.name + " [" + it.type + " t" + rankOf(res, it) + "]").join(" · ") +
    "   [" + res.display.length + " of " + res.total + "]");
});

// ---- group-header uniqueness across every fixture query + probes ----
console.log("");
let dupHeaders = 0;
FIX.concat([["X","the",0,0,0],["X","a",0,0,0],["X","van",0,0,0],["X","de",0,0,0],["X","o",0,0,0],
            ["X","paris",0,0,0],["X","picasso",0,0,0],["X","moma",0,0,0],["X","new york",0,0,0]])
  .forEach(([id, q]) => {
    const res = search(q);
    const seen = {};
    res.groups.forEach(g => { if(seen[g.type]) dupHeaders++; seen[g.type] = 1; });
  });
console.log("duplicate group headers across all probed queries: " + dupHeaders);

// ---- starvation probe: types represented before vs after ----
console.log("");
console.log("Starvation probes (types represented in the visible 9):");
["art","the","van","o","paris","picasso","moma","new york","night","portrait"].forEach(q => {
  const res = search(q);
  const types = {}; res.display.forEach(it => types[it.type] = (types[it.type]||0)+1);
  const typesAll = {}; res.scored.forEach(s => typesAll[s.it.type] = (typesAll[s.it.type]||0)+1);
  console.log("  " + q + ": shown " + JSON.stringify(types) + "  of matching " + JSON.stringify(typesAll));
});

// ---- metadata reachability (defect e) ----
console.log("");
console.log("Metadata reachability (artwork found by its painter's name):");
["vermeer","basquiat","artemisia"].forEach(q => {
  const res = search(q);
  const aw = res.display.filter(it => it.type === "Artworks");
  console.log("  " + q + ": artworks shown = " + aw.length + " → " + aw.map(x => x.name).join(" | "));
});

// ---- frozen "known limitation" baselines (ux-requirements.md Section 3) ----
console.log("");
console.log("Documented no-match baselines (must stay no-match):");
["durer","velazquez","cezanne","rose","1600","seventeenth","moma","woodblock"].forEach(q => {
  const res = search(q);
  console.log("  " + q + ": " + (res.total === 0 ? "no match (unchanged)" :
    "NOW MATCHES " + res.total + " → " + res.display.slice(0,3).map(it => it.name + "[t" + rankOf(res, it) + "]").join(", ")));
});
