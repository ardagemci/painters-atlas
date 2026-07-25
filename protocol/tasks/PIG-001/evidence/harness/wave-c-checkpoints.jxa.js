// PIG-001 U18 — prove the five frozen onboarding checkpoints round-trip through
// storage, using the REAL obWrite/obClear/obRestore source text from js/app.js.
//   osascript -l JavaScript protocol/tasks/PIG-001/evidence/harness/wave-c-checkpoints.jxa.js
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
 "tier1-artists.js","personas.js",
 "artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js","artists-14.js",
 "artists-15.js","artists-16.js","lists-1.js","museums-1.js"]
  .forEach(f => { try{ eval(read(base + "js/" + f)); }catch(e){ console.log("LOAD ERROR " + f + ": " + e.message); } });

const CAT = window.CATALOG || [];
const CatX = Object.fromEntries(CAT.map(x => [x.id, x]));
const TASTE_QUESTIONS = window.TASTE_QUESTIONS;
const TASTE_TONES = window.TASTE_TONES;

// a faithful stand-in for the two Storage objects
function mkStore(){
  const m = {};
  return { _m: m,
    getItem: k => (k in m ? m[k] : null),
    setItem: (k, v) => { m[k] = String(v); },
    removeItem: k => { delete m[k]; } };
}
var sessionStorage = mkStore();
var localStorage = mkStore();

// ---- extract the REAL persistence code from js/app.js ----
const src = read(base + "js/app.js");
const from = src.indexOf('const OB_KEY = "pigment.onboarding.v1";');
const to = src.indexOf("function obStart(){");
if(from < 0 || to < 0) throw new Error("could not locate the onboarding persistence block");
eval(src.slice(from, to) +
  "\nvar __OB = { get:function(){return ob;}, set:function(v){ob=v;}, write:obWrite, clear:obClear, restore:obRestore, KEY:OB_KEY };");

// the real deck pool, so the stored ids are real catalog ids
const pool = CAT.filter(w => w.tier === 1 && w.coords && w.image && w.image.status === "pd" && w.image.src);
const DECK = pool.slice(3, 19);          // 16 real works, a deterministic slice
if(DECK.length !== 16) throw new Error("deck pool too small: " + DECK.length);

let pass = 0, fail = 0;
function ok(label, cond, detail){
  if(cond) pass++; else fail++;
  console.log("  " + (cond ? "PASS" : "**FAIL**") + " — " + label + (detail ? "   (" + detail + ")" : ""));
}
function state(over){
  return Object.assign({ step:1, tones:[], deck:DECK.slice(), di:0, admired:[], skipped:[], answers:{}, adopted:false }, over);
}
// save → wipe every trace of memory → restore, exactly as a reload would
function roundTrip(s){
  __OB.set(s); __OB.write();
  __OB.set(null);
  const raw = sessionStorage.getItem(__OB.KEY);
  const back = __OB.restore();
  return { back: back, raw: raw };
}
const ids = d => d.map(w => w.id).join(",");

console.log("Storage key: " + __OB.KEY + "   (Passport key pigment.taste.v1 is a different store entirely)");
console.log("");

console.log("CHECKPOINT 1 — tone selection (step 1, 2 of 4 tones chosen):");
{
  const t = [TASTE_TONES[1].id, TASTE_TONES[4].id];
  const r = roundTrip(state({ step:1, tones:t.slice() }));
  ok("resumes at step 1", r.back && r.back.step === 1, "step=" + (r.back && r.back.step));
  ok("both chosen tones intact", r.back && r.back.tones.join(",") === t.join(","), r.back && r.back.tones.join(","));
  ok("the same 16 works are still the deck", r.back && ids(r.back.deck) === ids(DECK));
}

console.log("CHECKPOINT 2 — the deck, artwork 8 of 16 (step 2, di=7):");
{
  const adm = [DECK[0].id, DECK[2].id, DECK[5].id], skp = [DECK[1].id, DECK[3].id, DECK[4].id, DECK[6].id];
  const r = roundTrip(state({ step:2, tones:TASTE_TONES.slice(0,4).map(x=>x.id), di:7, admired:adm, skipped:skp }));
  ok("resumes at step 2", r.back && r.back.step === 2);
  ok("still on artwork 8 of 16", r.back && r.back.di === 7, "di=" + (r.back && r.back.di));
  ok("card 8 is the SAME artwork", r.back && r.back.deck[7].id === DECK[7].id, r.back && r.back.deck[7].title);
  ok("3 admirations preserved", r.back && r.back.admired.join(",") === adm.join(","));
  ok("4 passes preserved", r.back && r.back.skipped.join(",") === skp.join(","));
  ok("whole deck order preserved", r.back && ids(r.back.deck) === ids(DECK));
  ok("four tones preserved", r.back && r.back.tones.length === 4);
}

console.log("CHECKPOINT 3 — the questions, question 3 of 5 (step 3, 2 answered):");
{
  const a = {}; a[TASTE_QUESTIONS[0].id] = TASTE_QUESTIONS[0].options[1].id;
                a[TASTE_QUESTIONS[1].id] = TASTE_QUESTIONS[1].options[2].id;
  const r = roundTrip(state({ step:3, tones:TASTE_TONES.slice(0,4).map(x=>x.id), di:16,
                              admired:DECK.slice(0,9).map(w=>w.id), skipped:DECK.slice(9).map(w=>w.id), answers:a }));
  ok("resumes at step 3", r.back && r.back.step === 3);
  ok("both prior answers intact, same options", r.back && JSON.stringify(r.back.answers) === JSON.stringify(a),
     r.back && JSON.stringify(r.back.answers));
  ok("next question is question 3", r.back && Object.keys(r.back.answers).length === 2);
  ok("the 9 deck admirations survived into the question step", r.back && r.back.admired.length === 9);
}

console.log("CHECKPOINT 4 — the reveal (step 4):");
{
  const a = {}; TASTE_QUESTIONS.forEach((Q,i) => a[Q.id] = Q.options[i % Q.options.length].id);
  const r = roundTrip(state({ step:4, tones:TASTE_TONES.slice(0,4).map(x=>x.id), di:16,
                              admired:DECK.slice(0,9).map(w=>w.id), skipped:DECK.slice(9).map(w=>w.id), answers:a }));
  ok("resumes at the reveal, not the intro", r.back && r.back.step === 4);
  ok("all five answers intact", r.back && Object.keys(r.back.answers).length === 5);
  ok("tones intact for the reveal palette", r.back && r.back.tones.length === 4);
}

console.log("CHECKPOINT 5 — adopt / decide later (step 4, persona adopted):");
{
  const a = {}; TASTE_QUESTIONS.forEach((Q,i) => a[Q.id] = Q.options[i % Q.options.length].id);
  const r = roundTrip(state({ step:4, adopted:true, tones:TASTE_TONES.slice(0,4).map(x=>x.id), di:16, answers:a }));
  ok("resumes at the reveal with the adoption recorded", r.back && r.back.step === 4 && r.back.adopted === true);
  ok("answers still intact behind the adoption", r.back && Object.keys(r.back.answers).length === 5);
}

console.log("");
console.log("SAFETY / NON-REGRESSION:");
{
  // nothing stored at all
  sessionStorage.removeItem("pigment.onboarding.v1");
  ok("no stored run → no resume (clean intro)", __OB.restore() === null);

  // unreadable bytes
  sessionStorage.setItem("pigment.onboarding.v1", "{not json");
  ok("unreadable stored run → no resume, no throw", __OB.restore() === null);

  // wrong version
  sessionStorage.setItem("pigment.onboarding.v1", JSON.stringify({ v:2, deck:[DECK[0].id], step:2 }));
  ok("unknown schema version → no resume", __OB.restore() === null);

  // a deck id the catalog no longer has
  __OB.set(state({ step:2, di:4 })); __OB.write();
  const s = JSON.parse(sessionStorage.getItem("pigment.onboarding.v1"));
  s.deck[5] = "an-artwork-that-was-removed";
  sessionStorage.setItem("pigment.onboarding.v1", JSON.stringify(s));
  ok("a work missing from the catalog → refuse to half-resume", __OB.restore() === null);

  // out-of-range progress index
  __OB.set(state({ step:2, di:999 })); __OB.write();
  const b = __OB.restore();
  ok("impossible progress index is clamped, not crashed", b && b.di <= 16 && b.step === 3, "di=" + (b&&b.di) + " step=" + (b&&b.step));

  // step 3 with a full answer sheet must not render question six
  __OB.set(state({ step:3, answers:(function(){const a={};TASTE_QUESTIONS.forEach((Q,i)=>a[Q.id]=Q.options[0].id);return a;})() }));
  __OB.write();
  const c = __OB.restore();
  ok("a completed answer sheet resumes at the reveal, never at question 6", c && c.step === 4);

  // retake / reset clears the store
  __OB.set(state({ step:2, di:3 })); __OB.write();
  __OB.clear();
  ok("clear() removes the stored run", sessionStorage.getItem("pigment.onboarding.v1") === null);
  ok("clear() drops the in-memory run", __OB.get() === null);

  // the Passport store is never touched by any of this
  localStorage.setItem("pigment.taste.v1", '{"admirations":[{"id":"x","at":"t"}]}');
  const before = localStorage.getItem("pigment.taste.v1");
  __OB.set(state({ step:2, di:2 })); __OB.write(); __OB.restore(); __OB.clear();
  ok("pigment.taste.v1 is byte-identical after a full write/restore/clear cycle",
     localStorage.getItem("pigment.taste.v1") === before);
  ok("onboarding writes land only under pigment.onboarding.v1",
     Object.keys(localStorage._m).join(",") === "pigment.taste.v1");
}

console.log("");
console.log("CHECKPOINTS: " + pass + " assertions pass, " + fail + " fail");
