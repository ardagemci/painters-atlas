// Pigment SEO/share prerender (ADMIRE_SPEC §11 + PIGMENT.md)
// Emits static stub pages with real content, OG/Twitter tags, JSON-LD and a
// sitemap, because the hash-routed SPA is invisible to crawlers and scrapers.
//   osascript -l JavaScript tools/build_seo.jxa.js
// Rerun after any data change (catalog/artists/museums/lists). Output:
//   p/artist/{id}.html · p/artwork/{id}.html · p/museum/{id}.html · p/list/{id}.html
//   sitemap.xml · robots.txt
ObjC.import("Foundation");
function read(p){
  const s = $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null);
  if(s.isNil()) throw new Error("cannot read " + p);
  return ObjC.unwrap(s);
}
function write(p, content){
  $.NSFileManager.defaultManager.createDirectoryAtPathWithIntermediateDirectoriesAttributesError(
    $(p).stringByDeletingLastPathComponent, true, $(), $());
  $(content).writeToFileAtomicallyEncodingError(p, true, $.NSUTF8StringEncoding, $());
}
const argv = ObjC.unwrap($.NSProcessInfo.processInfo.arguments).map(a => ObjC.unwrap(a));
const me = argv.find(a => String(a).endsWith("build_seo.jxa.js")) || "tools/build_seo.jxa.js";
const base = String(me).replace(/tools\/+build_seo\.jxa\.js$/, "");
var window = {};
["taxonomy.js","artworks.js","venues.js","catalog-1.js","catalog-2.js","catalog-3.js","catalog-4.js","catalog-5.js",
 "tier1-artists.js","lists-1.js","museums-1.js","photo-credits.js",
 "artists-1.js","artists-2.js","artists-3.js","artists-4.js","artists-5.js","artists-6.js","artists-7.js",
 "artists-8.js","artists-9.js","artists-10.js","artists-11.js","artists-12.js","artists-13.js",
 "artists-14.js","artists-15.js","artists-16.js","artists-17.js","artists-18.js"]
  .forEach(f => eval(read(base + "js/" + f)));

const SITE = "https://ardagemci.github.io/painters-atlas/";
const A = window.ARTISTS, CAT = window.CATALOG, VEN = window.VENUES,
      MN = window.MUSEUM_NOTES || {}, LISTS = window.EDITORIAL_LISTS || [],
      T1 = window.TIER1 || {}, AW = window.ARTWORKS || {};
const Ax = {}; A.forEach(a => Ax[a.id] = a);
const Vx = {}; VEN.forEach(v => Vx[v.id] = v);

/* ---- photo credit (js/photo-credits.js) ----
   A prerendered stub shows the same photograph the app does, so it owes the
   same credit. Same registries, same TASL shape; no URL global in JXA, so the
   Commons title is parsed from the path by hand. */
const PC = window.PHOTO_CREDITS || {}, IC = window.IMAGE_CREDITS || {};
function commonsTitle(src){
  if(!src) return null;
  const m = String(src).match(/^[a-z]+:\/\/[^/]+(\/[^?#]*)/i);
  const path = m ? m[1] : String(src).split(/[?#]/)[0];
  const parts = path.split("/").filter(Boolean);
  if(parts.indexOf("commons") < 0) return null;
  const t = parts.indexOf("thumb");
  const name = t >= 0 ? parts[t + 3] : parts[parts.length - 1];
  if(!name) return null;
  try { return "File:" + decodeURIComponent(name); } catch(e){ return "File:" + name; }
}
/* venueId is given only when `src` is that venue's building photograph */
function creditHtml(src, label, venueId){
  let c = null;
  if(venueId && PC[venueId]) c = PC[venueId];
  else { const t = commonsTitle(src); c = t ? IC[t] : null; }
  if(!c) return "";
  const bits = [c.author ? esc(label) + ": " + esc(c.author) : esc(label)];
  bits.push(c.licenseUrl ? `<a href="${esc(c.licenseUrl)}" rel="license nofollow">${esc(c.license)}</a>` : esc(c.license));
  if(c.page) bits.push(`<a href="${esc(c.page)}" rel="nofollow">file on Commons</a>`);
  return `<p class="cred">${bits.join(" · ")}</p>`;
}
const catByArtist = {}, catByVenue = {};
CAT.forEach(w => {
  (catByArtist[w.artistId] = catByArtist[w.artistId] || []).push(w);
  if(w.museum && w.museum.id) (catByVenue[w.museum.id] = catByVenue[w.museum.id] || []).push(w);
});
const SENTINELS = { "private-collection":1, lost:1, unknown:1 };

const esc = s => String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const trim160 = s => { s = String(s || "").replace(/\s+/g," ").trim(); return s.length <= 158 ? s : s.slice(0, 155).replace(/\s+\S*$/, "") + "…"; };
const firstSentence = s => (String(s || "").match(/^.*?[.!?](\s|$)/) || [s || ""])[0].trim();

/* The artist's social preview.

   This used to prefer any catalogued work, which meant the share image moved
   the moment an artist got their first catalog record — and it had already
   moved for 49 artists. Leonardo's preview was not the Mona Lisa, Van Gogh's
   was not The Starry Night, Munch's was not The Scream.

   Owner decision, 2026-08-08: an artist keeps a designated hero. The artist
   record's `works:[]` array is already an ordered, hand-made statement of which
   pictures matter most, so the first listed work IS the designation; `hero:`
   exists to override it where the first listed work is not the right share
   image. Falling through to the catalog last keeps artists who have no gallery
   entry from losing their preview entirely. */
function artistImage(a){
  const aw = AW[a.id];
  if(a.hero && aw && aw[a.hero]) return aw[a.hero].img;
  if(aw && a.works) for(const w of a.works){ if(w && aw[w.t]) return aw[w.t].img; }
  if(aw) for(const k in aw) return aw[k].img;
  const pd = (catByArtist[a.id] || []).find(w => w.image && w.image.src && w.image.status === "pd");
  return pd ? pd.image.src : null;
}

function page(o){
  // o: { path, appRoute, title, desc, img, jsonld, bodyHtml }
  const url = SITE + o.path;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(o.title)} — Pigment</title>
<meta name="description" content="${esc(o.desc)}">
<link rel="canonical" href="${url}">
<meta property="og:site_name" content="Pigment — An Atlas of Painters">
<meta property="og:type" content="${o.ogType || "article"}">
<meta property="og:title" content="${esc(o.title)}">
<meta property="og:description" content="${esc(o.desc)}">
<meta property="og:url" content="${url}">
${o.img ? `<meta property="og:image" content="${esc(o.img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${esc(o.img)}">` : `<meta name="twitter:card" content="summary">`}
<meta name="twitter:title" content="${esc(o.title)}">
<meta name="twitter:description" content="${esc(o.desc)}">
${o.jsonld ? `<script type="application/ld+json">${JSON.stringify(o.jsonld)}</script>` : ""}
<style>
body{margin:0;background:#0d0c0a;color:#ece6d9;font:300 16px/1.65 "Inter","Segoe UI",system-ui,sans-serif;padding:40px 22px}
main{max-width:680px;margin:0 auto}
h1{font-family:"Playfair Display",Georgia,serif;font-size:2rem;line-height:1.15;margin:.2em 0 .4em}
img{max-width:100%;border-radius:14px;border:1px solid rgba(201,164,92,.3)}
a{color:#e8c98a;text-decoration:none}
.k{font-size:.68rem;letter-spacing:.34em;text-transform:uppercase;color:#c9a45c}
.meta{color:#9b937f;font-size:.92rem}
.cta{display:inline-block;margin-top:18px;padding:11px 22px;border:1px solid #c9a45c;border-radius:999px;color:#e8c98a;font-weight:500}
.rel{margin-top:28px;padding-top:14px;border-top:1px solid rgba(201,164,92,.25)}
.rel a{display:inline-block;margin:3px 10px 3px 0}
footer{margin-top:34px;color:#6e675a;font-size:.8rem}
.cred{color:#9b937f;font-size:.78rem;margin:8px 0 0}
.cred a{color:#c9b58a;text-decoration:underline}
</style>
</head>
<body>
<main>
<div class="k">Pigment · an atlas of painters</div>
${o.bodyHtml}
<a class="cta" href="${SITE}#/${o.appRoute}">Open in the atlas →</a>
<footer>Pigment — find your place in the history of art. <a href="${SITE}">Home</a></footer>
</main>
</body>
</html>`;
}

const urls = [];
let count = 0;
function emit(path, html){ write(base + path, html); urls.push(SITE + path); count++; }

/* ---- artworks ---- */
CAT.forEach(w => {
  const a = Ax[w.artistId]; if(!a) return;
  const img = w.image && w.image.status === "pd" && w.image.src || null;
  const venue = w.museum && w.museum.id && Vx[w.museum.id] && !SENTINELS[w.museum.id] ? Vx[w.museum.id] : null;
  const desc = trim160(w.description ||
    `${w.title} (${w.year.display}) by ${a.name}${venue ? ", in the " + venue.name + ", " + venue.city : ""}. ${a.tagline}.`);
  const jsonld = { "@context":"https://schema.org", "@type":"VisualArtwork",
    name: w.title, creator: { "@type":"Person", name: a.name },
    dateCreated: w.year.display, url: SITE + "p/artwork/" + w.id + ".html" };
  if(img) jsonld.image = img;
  if(venue) jsonld.contentLocation = { "@type":"Museum", name: venue.name, address: venue.city };
  const rel = (catByArtist[a.id] || []).filter(o => o.id !== w.id).slice(0, 5)
    .map(o => `<a href="${SITE}p/artwork/${o.id}.html">${esc(o.title)}</a>`).join("");
  emit("p/artwork/" + w.id + ".html", page({
    path: "p/artwork/" + w.id + ".html", appRoute: "artwork/" + w.id,
    title: `${w.title} by ${a.name}`, desc, img,
    jsonld,
    bodyHtml: `<h1>${esc(w.title)}</h1>
<p class="meta"><a href="${SITE}p/artist/${a.id}.html">${esc(a.name)}</a> · ${esc(w.year.display)}${venue ? " · " + esc(venue.name) + ", " + esc(venue.city) : ""}${w.dims ? " · " + esc(w.dims) : ""}</p>
${img ? `<img src="${esc(img)}" alt="${esc(w.title)} by ${esc(a.name)}">` + creditHtml(img, "Image credit") : ""}
<p>${esc(w.description || `One of the ${(catByArtist[a.id] || []).length} works by ${a.name} catalogued in Pigment, the interactive atlas of painters.`)}</p>
${w.notice ? `<ul>${w.notice.map(n => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}
${rel ? `<div class="rel"><span class="k">More by ${esc(a.name.split(" ").pop())}</span><br>${rel}</div>` : ""}` }));
});

/* ---- artists ---- */
A.forEach(a => {
  const img = artistImage(a);
  const t1 = T1[a.id];
  const desc = trim160((t1 ? t1.why : "") || (a.tagline + ". " + firstSentence(a.life)));
  const jsonld = { "@context":"https://schema.org", "@type":"Person",
    name: a.name, description: a.tagline,
    birthDate: String(a.born), url: SITE + "p/artist/" + a.id + ".html" };
  if(a.died) jsonld.deathDate = String(a.died);
  if(img) jsonld.image = img;
  const rel = (catByArtist[a.id] || []).slice(0, 8)
    .map(o => `<a href="${SITE}p/artwork/${o.id}.html">${esc(o.title)}</a>`).join("");
  emit("p/artist/" + a.id + ".html", page({
    path: "p/artist/" + a.id + ".html", appRoute: "artist/" + a.id,
    title: `${a.name} (${a.years})`, desc, img, ogType: "profile",
    jsonld,
    bodyHtml: `<h1>${esc(a.name)}</h1>
<p class="meta">${esc(a.years)} · ${esc(a.tagline)}</p>
${img ? `<img src="${esc(img)}" alt="Work by ${esc(a.name)}">` + creditHtml(img, "Image credit") : ""}
<p>${esc(t1 ? t1.why : firstSentence(a.life))}</p>
<p>${esc(firstSentence(a.career))}</p>
${rel ? `<div class="rel"><span class="k">Works in the atlas</span><br>${rel}</div>` : ""}` }));
});

/* ---- museums (holding venues) ---- */
VEN.forEach(v => {
  if(SENTINELS[v.id]) return;
  const works = catByVenue[v.id] || [];
  if(!works.length) return;
  const note = MN[v.id];
  const img = (note && note.photo && note.photo.src) || (works.find(w => w.image && w.image.src) || {}).image?.src || null;
  const desc = trim160((note && note.essay ? firstSentence(note.essay) : "") ||
    `${v.name}, ${v.city} — ${works.length} work${works.length === 1 ? "" : "s"} in the Pigment atlas${note ? ": " + note.hook : ""}.`);
  const rel = works.slice(0, 8).map(o => `<a href="${SITE}p/artwork/${o.id}.html">${esc(o.title)}</a>`).join("");
  emit("p/museum/" + v.id + ".html", page({
    path: "p/museum/" + v.id + ".html", appRoute: "museum/" + v.id,
    title: `${v.name}, ${v.city}`, desc, img,
    jsonld: { "@context":"https://schema.org", "@type":"Museum", name: v.name,
      address: { "@type":"PostalAddress", addressLocality: v.city, addressCountry: v.country || "" },
      url: SITE + "p/museum/" + v.id + ".html" },
    bodyHtml: `<h1>${esc(v.name)}</h1>
<p class="meta">${esc(v.city)}${v.country ? " · " + esc(v.country) : ""}${note ? " · " + esc(note.hook) : ""}</p>
${img ? `<img src="${esc(img)}" alt="${esc(v.name)}">` + creditHtml(img, "Photograph", note && note.photo && note.photo.src === img ? v.id : null) : ""}
<p>${esc(note && note.essay ? note.essay.split("\n\n")[0] : `${v.name} holds ${works.length} of the works catalogued in Pigment, the interactive atlas of painters.`)}</p>
${rel ? `<div class="rel"><span class="k">In the collection</span><br>${rel}</div>` : ""}` }));
});

/* ---- lists ---- */
LISTS.forEach(l => {
  const cover = CAT.find(w => w.id === l.cover);
  const img = cover && cover.image && cover.image.src || null;
  const rel = l.works.slice(0, 10).map(e => {
    const w = CAT.find(x => x.id === e.id);
    return w ? `<a href="${SITE}p/artwork/${w.id}.html">${esc(w.title)}</a>` : "";
  }).join("");
  emit("p/list/" + l.id + ".html", page({
    path: "p/list/" + l.id + ".html", appRoute: "list/" + l.id,
    title: l.title, desc: trim160(l.lede), img,
    jsonld: { "@context":"https://schema.org", "@type":"ItemList", name: l.title,
      description: l.lede, numberOfItems: l.works.length, url: SITE + "p/list/" + l.id + ".html" },
    bodyHtml: `<h1>${esc(l.title)}</h1>
<p class="meta">An editorial list · ${l.works.length} works</p>
${img ? `<img src="${esc(img)}" alt="${esc(l.title)}">` + creditHtml(img, "Image credit") : ""}
<p>${esc(l.lede)}</p>
${rel ? `<div class="rel"><span class="k">The works</span><br>${rel}</div>` : ""}` }));
});

/* ---- index.html's own description, generated ----
   It was hand-typed and said "247 artists, 317 masterpieces" long after the
   atlas held 266 and 350 — on the homepage, in every search result, and in
   every social card. A number a human retypes is a number that goes stale, so
   this rewrites it from the live registries on every build. The sentence around
   it stays fixed; only the counts move. */
(function(){
  const path = base + "index.html";
  const html = read(path);
  const venues = VEN.filter(v => !SENTINELS[v.id] && (catByVenue[v.id] || []).length).length;
  const desc = "Pigment is an interactive atlas of painters — " + A.length + " artists, " +
    CAT.length + " catalogued works, " + venues + " museums and churches, movements, " +
    "and an engine that maps your taste in art. An editorial selection, not a complete history.";
  const re = /<meta name="description" content="[^"]*">/;
  if(!re.test(html)) throw new Error("index.html has no meta description to regenerate");
  const next = html.replace(re, '<meta name="description" content="' + esc(desc) + '">');
  if(next !== html) write(path, next);
})();

/* ---- sitemap + robots ---- */
const today = new Date().toISOString().slice(0, 10);
write(base + "sitemap.xml",
`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>${SITE}</loc><lastmod>${today}</lastmod><priority>1.0</priority></url>
${urls.map(u => `<url><loc>${u}</loc><lastmod>${today}</lastmod></url>`).join("\n")}
</urlset>`);
write(base + "robots.txt", `User-agent: *\nAllow: /\nSitemap: ${SITE}sitemap.xml\n`);
"emitted " + count + " stub pages + sitemap (" + (urls.length + 1) + " urls) + robots.txt";
