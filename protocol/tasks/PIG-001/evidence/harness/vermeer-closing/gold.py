"""Independent check of unit 26c: the six gold-as-small-text call sites now
compute --gold2, and what they actually measure against their real backdrop.

Sites (css/styles.css:984, 1016, 1031, 1178, 1189, 1277):
  .branch-chip::before   .tl2-leg-more   .tl2-year.now
  .list-card .lc-kicker  .le-num         .pc-kind

For each, on a route that renders it: computed colour (including ::before), font
size, large-text classification, and the contrast against the first opaque
painted ancestor background. Sites that paint over a photograph are measured by
glyph pixels in photos.py instead - noted here where that applies.
"""
import json, os, sys
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp, png

PORT = int(os.environ.get("CDP_PORT", "9333"))
OUT = os.path.dirname(os.path.abspath(__file__))

SITES = [
    ("#/movements", ".branch-chip", "::before"),
    ("#/movement/impressionism", ".branch-chip", "::before"),
    ("#/timeline", ".tl2-leg-more", ""),
    ("#/timeline", ".tl2-year.now", ""),
    ("#/lists", ".list-card .lc-kicker", ""),
    ("#/list/paintings-that-still-scare-us", ".le-num", ""),
    ("#/taste", ".pc-kind", ""),
    ("#/palette", ".pc-kind", ""),
]

PROBE = r"""(function(sel,pseudo){
 var el=document.querySelector(sel);
 if(!el) return JSON.stringify({found:false});
 var cs=pseudo?getComputedStyle(el,pseudo):getComputedStyle(el);
 var r=el.getBoundingClientRect();
 /* first ancestor with a non-transparent background-color */
 var n=el, bg=null, bgFrom=null;
 while(n){var c=getComputedStyle(n).backgroundColor;
  var m=c.match(/[\d.]+/g);
  if(m && (m.length<4 || parseFloat(m[3])>0.99)){bg=[+m[0],+m[1],+m[2]];
   bgFrom=n.tagName.toLowerCase()+(n.classList.length?'.'+[].slice.call(n.classList).join('.'):'');
   break;}
  n=n.parentElement;}
 var fp=parseFloat(cs.fontSize), wt=parseInt(cs.fontWeight,10)||400;
 var col=cs.color.match(/[\d.]+/g);
 return JSON.stringify({found:true, color:[+col[0],+col[1],+col[2]],
  content:pseudo?cs.content:null, fontPx:fp, weight:wt,
  large:(fp>=24||(fp>=18.66&&wt>=700)),
  bg:bg, bgFrom:bgFrom,
  rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
  overPhoto:(function(){var hit=false;
    [].forEach.call(document.images,function(i){
      if(!/upload\.wikimedia\.org/.test(i.currentSrc||i.src||''))return;
      var q=i.getBoundingClientRect();
      if(r.left<q.right&&r.right>q.left&&r.top<q.bottom&&r.bottom>q.top)hit=true;});
    return hit;})()});})"""

TOKENS = ("JSON.stringify({gold:getComputedStyle(document.documentElement)"
          ".getPropertyValue('--gold').trim(),"
          "gold2:getComputedStyle(document.documentElement)"
          ".getPropertyValue('--gold2').trim(),"
          "theme:document.documentElement.dataset.theme})")


SEEDED = json.dumps({
    "version": 1, "createdAt": "2026-07-01T00:00:00.000Z", "updatedAt": "2026-07-01T00:00:00.000Z",
    "admirations": [{"id": i, "at": "2026-07-01T00:00:00.000Z"} for i in
                    ["mona-lisa", "the-starry-night", "the-scream", "the-night-watch",
                     "guernica", "composition-vii", "black-square", "the-birth-of-venus"]],
    "notForMe": [], "seen": [], "wantToSee": [], "saved": [], "probes": [],
    "deckSeen": [], "skipped": [],
    "quiz": None, "palette": {"tones": ["caravaggio-black"], "source": "chosen"},
    "persona": {"adopted": None, "candidates": [], "adoptedAt": None, "hidden": False},
    "tasteVector": None, "milestones": {"onboarded": True, "confidence": "sketch"}})


def hex2rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


rows = []
b = cdp.Browser(port=PORT)
try:
    b.metrics(1440, 1000)
    for theme in ("dark", "light"):
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        tk = None
        for k, (route, sel, pseudo) in enumerate(SITES):
            if route == "#/taste":
                b.goto(cdp.BASE + "/index.html?seed=1#/", settle=1.2)
                b.ev("localStorage.setItem('pigment.taste.v1',%s);1" % json.dumps(SEEDED))
            b.goto("%s/index.html?g=%s%d%s" % (cdp.BASE, theme, k, route), settle=2.2)
            if tk is None:
                tk = json.loads(b.ev(TOKENS))
                print("\n== %s  --gold %s  --gold2 %s" % (tk["theme"], tk["gold"], tk["gold2"]))
            d = json.loads(b.ev("(%s)(%r,%r)" % (PROBE, sel, pseudo)))
            if not d["found"]:
                print("  %-26s %-22s NOT RENDERED on this route" % (sel + pseudo, route))
                rows.append({"theme": theme, "route": route, "sel": sel + pseudo,
                             "found": False})
                continue
            g, g2 = hex2rgb(tk["gold"]), hex2rgb(tk["gold2"])
            which = "--gold2" if d["color"] == g2 else ("--gold" if d["color"] == g else "other")
            ratio = png.ratio(tuple(d["color"]), tuple(d["bg"])) if d["bg"] else None
            need = 3.0 if d["large"] else 4.5
            rows.append({"theme": theme, "route": route, "sel": sel + pseudo,
                         "found": True, "color": d["color"], "token": which,
                         "fontPx": d["fontPx"], "large": d["large"], "need": need,
                         "bg": d["bg"], "bgFrom": d["bgFrom"],
                         "ratio": None if ratio is None else round(ratio, 2),
                         "verdict": None if ratio is None else
                                    ("PASS" if ratio >= need else "FAIL"),
                         "overPhoto": d["overPhoto"], "content": d["content"]})
            print("  %-26s %-30s %-8s %5.1fpx  ratio %s vs %s  %s%s"
                  % (sel + pseudo, route, which, d["fontPx"],
                     "%.2f" % ratio if ratio else "n/a", need,
                     "" if ratio is None else ("PASS" if ratio >= need else "FAIL"),
                     "  [over a wikimedia photo - see photos.py]" if d["overPhoto"] else ""))
finally:
    b.close()
json.dump(rows, open(os.path.join(OUT, "gold-sites.json"), "w"), indent=1)
bad = [r for r in rows if r.get("verdict") == "FAIL"]
notg2 = [r for r in rows if r.get("found") and r.get("token") != "--gold2"]
print("\nsites measured: %d   FAIL: %d   not computing --gold2: %d"
      % (len([r for r in rows if r.get('found')]), len(bad),
         len(notg2)))
for r in bad + notg2:
    print("  !", r["theme"], r["sel"], r["route"], r.get("token"), r.get("ratio"))
