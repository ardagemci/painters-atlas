// dump artist basics as JSON for the artwork fetcher:
//   osascript -l JavaScript tools/dump-artists.jxa.js > /tmp/pigment-artists.json
ObjC.import("Foundation");
function read(p){
  const s = $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null);
  if(s.isNil()) throw new Error("cannot read " + p);
  return ObjC.unwrap(s);
}
const argv = ObjC.unwrap($.NSProcessInfo.processInfo.arguments).map(a => ObjC.unwrap(a));
const me = argv.find(a => String(a).endsWith("dump-artists.jxa.js")) || "tools/dump-artists.jxa.js";
const base = String(me).replace(/tools\/+dump-artists\.jxa\.js$/, "");
var window = {};
const files = ["taxonomy.js"];
for(let i = 1; i <= 15; i++) files.push("artists-" + i + ".js");
files.forEach(f => eval(read(base + "js/" + f)));
JSON.stringify(window.ARTISTS.map(a => ({ id: a.id, name: a.name, died: a.died, works: a.works.map(w => w.t) })));
