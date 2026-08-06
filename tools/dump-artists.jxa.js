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
// Enumerate the shard files that actually exist rather than counting to a
// hard-coded ceiling. The literal 15 silently dropped artists-16 and -17 when
// they were added — sixteen artists vanished from the dump, and main() in
// tools/audit_artworks.py met them as a bare KeyError. A directory listing
// cannot go stale when an eighteenth shard lands.
const fm = $.NSFileManager.defaultManager;
const listing = fm.contentsOfDirectoryAtPathError(base + "js", $());
if(listing.isNil()) throw new Error("cannot list " + base + "js");
const shards = ObjC.unwrap(listing).map(f => ObjC.unwrap(f))
  .map(f => [f, /^artists-(\d+)\.js$/.exec(f)])
  .filter(p => p[1])
  .sort((a, b) => Number(a[1][1]) - Number(b[1][1]))   // numeric, so 10 follows 9
  .map(p => p[0]);
if(!shards.length) throw new Error("no js/artists-*.js files found under " + base);
["taxonomy.js"].concat(shards).forEach(f => eval(read(base + "js/" + f)));
JSON.stringify(window.ARTISTS.map(a => ({ id: a.id, name: a.name, died: a.died, works: a.works.map(w => w.t) })));
