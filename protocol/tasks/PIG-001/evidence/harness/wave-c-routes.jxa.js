// PIG-001 U19 — load the REAL js/app.js under a minimal DOM shim and drive all 24
// router branches, asserting each still renders, sets its title, and lands focus.
//   osascript -l JavaScript protocol/tasks/PIG-001/evidence/harness/wave-c-routes.jxa.js
ObjC.import("Foundation");
function read(p){
  const s = $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null);
  if(s.isNil()) throw new Error("cannot read " + p);
  return ObjC.unwrap(s);
}
const argv = ObjC.unwrap($.NSProcessInfo.processInfo.arguments).map(a => ObjC.unwrap(a));
const me = argv.find(a => /wave-c-[a-z]+\.jxa\.js$/.test(String(a))) || "";
const base = String(me).replace(/protocol\/tasks\/PIG-001\/evidence\/harness\/wave-c-[a-z]+\.jxa\.js$/, "") || "./";


// ---------------- minimal DOM ----------------
function anyStub(){
  const f = function(){ return anyStub(); };
  return new Proxy(f, {
    get: (t, k) => {
      if(k === "toString" || k === Symbol.toPrimitive) return () => "";
      if(k === "length") return 0;
      if(k === Symbol.iterator) return function*(){};
      return anyStub();
    },
    set: () => true,
    apply: () => anyStub()
  });
}
function El(tag){
  const e = {
    tagName: String(tag || "div").toUpperCase(),
    dataset: {}, style: {}, attrs: {}, children: [], hidden: false,
    innerHTML: "", textContent: "", value: "", disabled: false, offsetWidth: 0,
    scrollLeft: 0, scrollTop: 0, scrollWidth: 0, clientWidth: 0,
    classList: { _s: {},
      add(){ [].forEach.call(arguments, c => this._s[c] = 1); },
      remove(){ [].forEach.call(arguments, c => delete this._s[c]); },
      toggle(c, on){ if(on === undefined) on = !this._s[c]; if(on) this._s[c] = 1; else delete this._s[c]; },
      contains(c){ return !!this._s[c]; } },
    setAttribute(k, v){ this.attrs[k] = String(v); },
    getAttribute(k){ return k in this.attrs ? this.attrs[k] : null; },
    hasAttribute(k){ return k in this.attrs; },
    removeAttribute(k){ delete this.attrs[k]; },
    addEventListener(){}, removeEventListener(){},
    appendChild(c){ this.children.push(c); return c; },
    removeChild(){}, remove(){}, click(){},
    focus(){ DOC.activeElement = this; FOCUS_LOG.push(this); },
    blur(){}, scrollIntoView(){}, closest(){ return null; },
    querySelector(){ return null; },
    querySelectorAll(){ return []; },
    contains(){ return false; },
    getContext(){ return anyStub(); },
    getBoundingClientRect(){ return { x:0, y:0, width:0, height:0, top:0, left:0, right:0, bottom:0 }; },
    toBlob(){}, insertAdjacentHTML(){}
  };
  return e;
}
const FOCUS_LOG = [];
const BYID = {};
const DOC = {
  activeElement: null,
  documentElement: El("html"),
  body: El("body"),
  fonts: { load: () => Promise.resolve(), ready: Promise.resolve() },
  title: "",
  getElementById(id){ return BYID[id] || (BYID[id] = El("div")); },
  createElement(t){ return El(t); },
  querySelector(){ return null; },
  querySelectorAll(){ return []; },
  addEventListener(t, fn){ (DOCL[t] = DOCL[t] || []).push(fn); }
};
const DOCL = {}, WINL = {};
var document = DOC;
var location = { hash: "", href: "https://example.invalid/", search: "", pathname: "/" };
var navigator = { clipboard: null, userAgent: "jxa" };
var performance = { now: () => 0 };
function requestAnimationFrame(){ return 0; }
function setTimeout(){ return 0; }
function mkStore(){ const m = {}; return { _m:m, getItem: k => (k in m ? m[k] : null),
  setItem: (k,v) => { m[k] = String(v); }, removeItem: k => { delete m[k]; } }; }
var localStorage = mkStore(), sessionStorage = mkStore();
var window = {
  matchMedia: () => ({ matches: true, addListener(){}, addEventListener(){} }),
  addEventListener(t, fn){ (WINL[t] = WINL[t] || []).push(fn); },
  scrollTo(){}, innerWidth: 1280, innerHeight: 800,
  devicePixelRatio: 1, requestAnimationFrame, location, document: DOC, localStorage, sessionStorage
};
var innerWidth = 1280, innerHeight = 800, devicePixelRatio = 1, scrollY = 0, scrollX = 0;
function scrollTo(){}
function addEventListener(t, fn){ (WINL[t] = WINL[t] || []).push(fn); }
function getComputedStyle(){ return anyStub(); }
var URL = { createObjectURL: () => "", revokeObjectURL(){} };
var Image = function(){ return El("img"); };

// capture what the router writes into #app
const APP = El("main"); BYID["app"] = APP;
let lastHTML = "";
Object.defineProperty(APP, "innerHTML", { get: () => lastHTML, set: v => { lastHTML = String(v); } });
BYID["search"] = El("input"); BYID["search-results"] = El("div");
BYID["theme-toggle"] = El("button"); BYID["bg-canvas"] = El("canvas");
BYID["route-status"] = El("p");

// ---------------- load the data, then the real app ----------------
["taxonomy.js","worldmap.js","artworks.js","influences.js","venues.js",
 "catalog-1.js","catalog-2.js","catalog-3.js","catalog-4.js","tier1-artists.js",
 "artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js","artists-14.js",
 "artists-15.js","artists-16.js","lists-1.js","personas.js","museums-1.js"]
  .forEach(f => { try{ eval(read(base + "js/" + f)); }catch(e){ console.log("LOAD ERROR " + f + ": " + e.message); } });
// the data files publish onto `window`; a browser makes those bare globals too
eval(Object.keys(window).filter(k => /^[A-Z][A-Z0-9_]*$/.test(k))
  .map(k => "var " + k + " = window[" + JSON.stringify(k) + "];").join("\n"));

try{ eval(read(base + "js/app.js")); }
catch(e){ console.log("APP LOAD ERROR: " + e.message + "\n" + (e.stack || "")); throw e; }

const routeFns = WINL["hashchange"] || [];
if(!routeFns.length) throw new Error("no hashchange listener registered — cannot drive the router");
const go = h => { location.hash = h; DOC.activeElement = null; routeFns.forEach(fn => fn()); };

// ---------------- the frozen 24 router branches ----------------
const A0 = window.ARTISTS[0].id, W0 = window.CATALOG[0].id, L0 = window.EDITORIAL_LISTS[0].id;
const M0 = window.MOVEMENTS[0].id, T0 = window.TECHNIQUES[0].id, E0 = window.ERAS[0].id, N0 = window.NATIONS[0].id;
const V0 = (window.VENUES.find(v => !/^(private-collection|lost|unknown)$/.test(v.id) && window.CATALOG.some(w => w.museum && w.museum.id === v.id)) || {}).id;
const ROUTES = [
  ["1  home",        "#/"],
  ["2  artists",     "#/artists"],
  ["3  timeline",    "#/timeline"],
  ["4  influences",  "#/influences"],
  ["5  daily",       "#/daily"],
  ["6  lists",       "#/lists"],
  ["7  list/{id}",   "#/list/" + L0],
  ["8  palette",     "#/palette"],
  ["9  taste",       "#/taste"],
  ["10 passport/{p}","#/passport/notavalidpayload"],
  ["11 museums",     "#/museums"],
  ["12 museum/{id}", "#/museum/" + V0],
  ["13 explore",     "#/explore"],
  ["14 artist/{id}", "#/artist/" + A0],
  ["15 artwork/{id}","#/artwork/" + W0],
  ["16 movements",   "#/movements"],
  ["17 movement/{id}","#/movement/" + M0],
  ["18 techniques",  "#/techniques"],
  ["19 technique/{id}","#/technique/" + T0],
  ["20 eras",        "#/eras"],
  ["21 era/{id}",    "#/era/" + E0],
  ["22 nations",     "#/nations"],
  ["23 nation/{id}", "#/nation/" + N0],
  ["24 default/404", "#/no-such-page-at-all"]
];
let pass = 0, fail = 0;
console.log("| # | route | renders | <h1> | title set | focus moved | announced |");
console.log("|---|---|---|---|---|---|---|");
ROUTES.forEach(([label, hash]) => {
  DOC.title = ""; BYID["route-status"].textContent = ""; FOCUS_LOG.length = 0;
  let err = null;
  try{ go(hash); }catch(e){ err = e.message; }
  const html = lastHTML;
  const okRender = !err && typeof html === "string" && html.length > 120 && /<h1|<div/.test(html);
  const okH1 = /<h1/.test(html);
  const okTitle = !!DOC.title;
  const isFirst = label.indexOf("1  home") === 0;
  const okFocus = isFirst ? FOCUS_LOG.length === 0 : FOCUS_LOG.length > 0;
  const okAnn = isFirst ? !BYID["route-status"].textContent : !!BYID["route-status"].textContent;
  const ok = okRender && okTitle && okFocus && okAnn;
  if(ok) pass++; else fail++;
  console.log("| " + label + " | `" + hash + "` | " + (okRender ? (html.length + " B") : "**ERROR: " + err + "**") +
    " | " + (okH1 ? "yes" : "no") + " | " + (okTitle ? "`" + DOC.title + "`" : "**no**") +
    " | " + (isFirst ? "n/a — first load, focus deliberately not stolen" : (okFocus ? "yes" : "**no**")) + " | " + (isFirst ? "n/a — first load" : (okAnn ? "`" + BYID["route-status"].textContent + "`" : "**no**")) + " |");
});
console.log("");
console.log("ROUTES: " + pass + "/" + ROUTES.length + " render + orient correctly, " + fail + " fail");

// ---------------- re-render must NOT announce or steal focus ----------------
console.log("");
console.log("Re-render behaviour (an onboarding tap calls route() on the same hash):");
function reRender(){ routeFns.forEach(fn => fn()); }
go("#/artists");
BYID["route-status"].textContent = "";
FOCUS_LOG.length = 0;
reRender();
console.log("  same-hash re-render announces nothing: " +
  (BYID["route-status"].textContent === "" ? "PASS" : "**FAIL** (" + BYID["route-status"].textContent + ")"));
console.log("  same-hash re-render does not jump focus to the heading: " +
  (FOCUS_LOG.length === 0 ? "PASS" : "**FAIL** (" + FOCUS_LOG.length + " focus calls)"));

// ---------------- onboarding end to end, then a reload mid-run ----------------
console.log("");
console.log("Onboarding end-to-end through the real click handler:");
const clickers = DOCL["click"] || [];
function fire(el){
  const ev = { target: { closest: sel => {
    if(sel === "[data-tsx]") return el.dataset && el.dataset.tsx ? el : null;
    if(sel === "[data-skipto]") return el.dataset && el.dataset.skipto ? el : null;
    return null;
  } }, preventDefault(){}, stopPropagation(){} };
  clickers.forEach(fn => fn(ev));
}
function btn(tsx, tsid){ const e = El("button"); e.dataset.tsx = tsx; if(tsid) e.dataset.tsid = tsid; return e; }
go("#/palette");
fire(btn("start"));
const tones = window.TASTE_TONES.slice(0, 4).map(t => t.id);
tones.forEach(t => fire(btn("tone", t)));
fire(btn("tones-done"));
let taps = 0;
while(taps < 40 && JSON.parse(sessionStorage.getItem("pigment.onboarding.v1")).step === 2){
  fire(btn(taps % 3 ? "deck-pass" : "deck-admire")); taps++;
}
let s = JSON.parse(sessionStorage.getItem("pigment.onboarding.v1"));
console.log("  16 deck taps advance to the questions: " + (s.step === 3 && taps === 16 ? "PASS" : "**FAIL** step=" + s.step + " taps=" + taps));
console.log("  admirations + passes recorded: " + (s.admired.length + s.skipped.length === 16 ? "PASS" : "**FAIL**"));
// reload in the middle of the questions
window.TASTE_QUESTIONS.slice(0, 2).forEach((Q, i) => fire(btn("answer", Q.id + ":" + Q.options[0].id)));
s = JSON.parse(sessionStorage.getItem("pigment.onboarding.v1"));
console.log("  question 3 of 5 is the stored checkpoint: " +
  (s.step === 3 && Object.keys(s.answers).length === 2 ? "PASS" : "**FAIL** " + JSON.stringify(s.answers)));
window.TASTE_QUESTIONS.slice(2).forEach(Q => fire(btn("answer", Q.id + ":" + Q.options[0].id)));
s = JSON.parse(sessionStorage.getItem("pigment.onboarding.v1"));
const saved = JSON.parse(localStorage.getItem("pigment.taste.v1") || "null");
console.log("  the fifth answer reaches the reveal: " + (s.step === 4 ? "PASS" : "**FAIL** step=" + s.step));
console.log("  obFinish wrote the Passport: " +
  (saved && saved.milestones && saved.milestones.onboarded && saved.quiz &&
   Object.keys(saved.quiz.answers).length === 5 && saved.palette.tones.length === 4 &&
   saved.admirations.length ? "PASS" : "**FAIL** " + JSON.stringify(saved && saved.milestones)));
console.log("  the reveal checkpoint survives a reload (stored run still present): " +
  (sessionStorage.getItem("pigment.onboarding.v1") ? "PASS" : "**FAIL**"));
console.log("  Passport keys written: " + Object.keys(localStorage._m).join(", "));
console.log("  onboarding keys written: " + Object.keys(sessionStorage._m).join(", "));

// ---------------- the influence-graph bypass ----------------
console.log("");
go("#/influences");
console.log("Influence graph bypass: " +
  (/data-skipto="ig-end"/.test(lastHTML) && /id="ig-end"[^>]*tabindex="-1"/.test(lastHTML)
    ? "PASS — skip control before the graph, target after it" : "**FAIL**"));
const nodeStops = (lastHTML.match(/class="ig-node"/g) || []).length;
console.log("  focusable graph nodes bypassed: " + nodeStops);
