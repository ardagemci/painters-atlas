/* data integrity check — run with: node tools/validate.js */
const fs = require("fs"), path = require("path"), vm = require("vm");
const root = path.join(__dirname, "..");
const window = {};
const ctx = vm.createContext({ window });
["taxonomy.js","artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js","artists-14.js"]
  .forEach(f => vm.runInContext(fs.readFileSync(path.join(root,"js",f),"utf8"), ctx, { filename:f }));

const { ARTISTS:A, MOVEMENTS:M, TECHNIQUES:T, ERAS:E, NATIONS:N } = window;
const errs = [];
const ids = list => new Set(list.map(x => x.id));
const mIds = ids(M), tIds = ids(T), eIds = ids(E), nIds = ids(N);

// painter styles implemented in app.js
const appSrc = fs.readFileSync(path.join(root,"js","app.js"),"utf8");
const styleNames = new Set([...appSrc.matchAll(/^(\w+)\(ctx,w,h,P,R\)/gm)].map(m => m[1]));

const dupCheck = (list, label) => {
  const seen = new Set();
  list.forEach(x => { if(seen.has(x.id)) errs.push(`${label}: duplicate id ${x.id}`); seen.add(x.id); });
};
dupCheck(A,"artist"); dupCheck(M,"movement"); dupCheck(T,"technique"); dupCheck(E,"era"); dupCheck(N,"nation");

M.forEach(m => { if(m.parent && !mIds.has(m.parent)) errs.push(`movement ${m.id}: bad parent ${m.parent}`);
  if(!styleNames.has(m.style)) errs.push(`movement ${m.id}: unknown style ${m.style}`);
  if(!m.palette || m.palette.length < 4) errs.push(`movement ${m.id}: bad palette`); });
T.forEach(t => { if(t.parent && !tIds.has(t.parent)) errs.push(`technique ${t.id}: bad parent ${t.parent}`);
  if(!styleNames.has(t.style)) errs.push(`technique ${t.id}: unknown style ${t.style}`); });
E.forEach(e => { if(!styleNames.has(e.style)) errs.push(`era ${e.id}: unknown style ${e.style}`); });

const req = ["id","name","years","born","nation","eras","movements","techniques","style","palette","tagline","works","life","career","outside","facts"];
A.forEach(a => {
  req.forEach(k => { if(a[k] === undefined || a[k] === "") errs.push(`artist ${a.id}: missing ${k}`); });
  if(!nIds.has(a.nation)) errs.push(`artist ${a.id}: bad nation ${a.nation}`);
  a.eras.forEach(e => !eIds.has(e) && errs.push(`artist ${a.id}: bad era ${e}`));
  a.movements.forEach(m => !mIds.has(m) && errs.push(`artist ${a.id}: bad movement ${m}`));
  a.techniques.forEach(t => !tIds.has(t) && errs.push(`artist ${a.id}: bad technique ${t}`));
  if(!styleNames.has(a.style)) errs.push(`artist ${a.id}: unknown style ${a.style}`);
  if(!a.palette || a.palette.length !== 5 || a.palette.some(c => !/^#[0-9a-f]{6}$/i.test(c)))
    errs.push(`artist ${a.id}: bad palette [${a.palette}]`);
  if(!a.works || a.works.length < 3) errs.push(`artist ${a.id}: <3 works`);
  if(!a.facts || a.facts.length < 3) errs.push(`artist ${a.id}: <3 facts`);
});

// orphan categories (no artists, no children) — warn only
const movArtists = id => A.filter(a => a.movements.includes(id)).length;
const tecArtists = id => A.filter(a => a.techniques.includes(id)).length;
const warns = [];
M.forEach(m => { if(!movArtists(m.id) && !M.some(x => x.parent === m.id)) warns.push(`movement ${m.id} has no artists`); });
T.forEach(t => { if(!tecArtists(t.id) && !T.some(x => x.parent === t.id)) warns.push(`technique ${t.id} has no artists`); });
N.forEach(n => { if(!A.some(a => a.nation === n.id)) warns.push(`nation ${n.id} has no artists`); });
E.forEach(e => { if(!A.some(a => a.eras.includes(e.id))) warns.push(`era ${e.id} has no artists`); });

console.log(`artists: ${A.length}, movements: ${M.length}, techniques: ${T.length}, eras: ${E.length}, nations: ${N.length}`);
console.log(`painter styles in app.js: ${styleNames.size}`);
if(warns.length) console.log("WARNINGS:\n  " + warns.join("\n  "));
if(errs.length){ console.error("ERRORS:\n  " + errs.join("\n  ")); process.exit(1); }
console.log("✓ all references valid");
