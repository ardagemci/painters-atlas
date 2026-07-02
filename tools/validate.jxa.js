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
M.forEach(x => { if(!A.some(a => a.movements.includes(x.id)) && !M.some(c => c.parent === x.id)) warns.push("movement " + x.id + " has no artists"); });
T.forEach(x => { if(!A.some(a => a.techniques.includes(x.id)) && !T.some(c => c.parent === x.id)) warns.push("technique " + x.id + " has no artists"); });
N.forEach(x => { if(!A.some(a => a.nation === x.id)) warns.push("nation " + x.id + " has no artists"); });
E.forEach(x => { if(!A.some(a => a.eras.includes(x.id))) warns.push("era " + x.id + " has no artists"); });

out.push("artists: " + A.length + ", movements: " + M.length + ", techniques: " + T.length +
  ", eras: " + E.length + ", nations: " + N.length + ", painter styles: " + Object.keys(styleNames).length);
if(warns.length) out.push("WARNINGS:\n  " + warns.join("\n  "));
out.push(errs.length ? "ERRORS:\n  " + errs.join("\n  ") : "ALL REFERENCES VALID");
out.join("\n");
