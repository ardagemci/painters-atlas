"""PIG-001 N-1 — recapture the whole mobile-390x844 pack at HEAD. Vermeer.

Van Eyck's revision 5 left the 47 mobile frames stale: they predate unit 37
(fb8ba6e), which scrolls the nav row on focusin at <=820px. The owner chose
recapture over a stated limitation, so every mobile frame is retaken here and
overwritten in place.

Same shutter discipline as pack.py: Emulation.setDeviceMetricsOverride (headless
Chrome clamps windows to 500px minimum on this Mac, which once produced 500px
LAYOUTS cropped into 390px FILES), and window.innerWidth asserted IN THE PAGE at
shutter time. Filenames keep `mobile` and `dark`/`light` literal for the kernel's
quality gate.

usage: python3 n1recap.py <theme>
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-u32"
sys.path.insert(0, C)
sys.path.insert(0, V)
import cdp                                     # noqa: E402
import sitecensus as sc                        # noqa: E402

EV = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 390, 844
VP = "mobile-390x844"

# every name in the shipped mobile pack, mapped back to the state that made it
ROUTES = [
    ("home", "#/"),
    ("artists", "#/artists"),
    ("artist-leonardo", "#/artist/leonardo-da-vinci"),
    ("artwork-david", "#/artwork/david"),
    ("explore", "#/explore"),
    ("timeline", "#/timeline"),
    ("influences", "#/influences"),
    ("museums", "#/museums"),
    ("museum-louvre", "#/museum/louvre"),
    ("lists", "#/lists"),
    ("palette", "#/palette"),
    ("taste", "#/taste"),
    ("daily", "#/daily"),
    ("privacy", "#/privacy"),
    ("credits", "#/credits"),
    ("invalid-route", "#/no-such-page"),
    ("u27-museum-k20-dusseldorf", "#/museum/k20-dusseldorf"),
    ("u27-museum-louvre", "#/museum/louvre"),
    ("u27-museum-moderna-museet", "#/museum/moderna-museet"),
    ("u30-artist-caravaggio", "#/artist/caravaggio"),
    ("u30-era-16th-century", "#/era/16th-century"),
]
DARK_ONLY = [("v32-influences-svg-labels", "#/influences")]

# a payload that differs from the seeded passport in the single-value fields, so
# the arrival screen offers "Choose what to keep" and step 2 renders conflicts
MAKE_PAYLOAD = """(function(){
  var raw = localStorage.getItem('pigment.taste.v1');
  var p = JSON.parse(raw);
  p.persona = {adopted:'the-colourist', at:1};
  p.tones = ['gold','teal'];
  p.onboarding = {done:true, answers:{a:1}};
  p.markers = {seenIntro:true};
  var j = JSON.stringify(p);
  return btoa(unescape(encodeURIComponent(j)))
    .replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');
})()"""


def shoot(b, name, theme, asserts, note=""):
    iw = b.ev("window.innerWidth")
    th = b.ev("document.documentElement.dataset.theme")
    hsh = b.ev("location.hash")
    h1 = b.ev("(document.querySelector('h1')||{}).textContent||''")
    navn = b.ev("document.querySelectorAll('.site-nav a, header nav a').length")
    imgs = b.ev("(function(){var i=[].slice.call(document.images);"
                "return JSON.stringify({total:i.length,broken:i.filter(function(x){"
                "return x.complete&&x.naturalWidth===0;}).length});})()")
    assert iw == W, "innerWidth %s != %s for %s" % (iw, W, name)
    assert th == theme, "theme %s != %s for %s" % (th, theme, name)
    out = os.path.join(EV, "%s__%s__%s.png" % (name, VP, theme))
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False})
    open(out, "wb").write(base64.b64decode(r["data"]))
    rec = {"file": os.path.basename(out), "theme": th, "innerWidth": iw,
           "innerHeight": b.ev("window.innerHeight"), "hash": hsh,
           "h1": (h1 or "")[:60].strip(), "navLinks": navn,
           "images": json.loads(imgs), "bytes": os.path.getsize(out),
           "note": note}
    asserts.append(rec)
    print("%-30s iw=%-4d th=%-5s nav=%-2s imgs=%2d/%d %7d B  h1=%s"
          % (name, iw, th, navn, rec["images"]["total"],
             rec["images"]["broken"], rec["bytes"], rec["h1"]), flush=True)


def main():
    theme = sys.argv[1]
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9491")))
    asserts = []
    try:
        sc.boot(b, theme)
        b.metrics(W, H)
        for name, route in ROUTES:
            b.goto("%s/index.html?n1=%d%s" % (cdp.BASE, os.getpid(), route),
                   settle=2.4)
            sc.wait_settled(b)
            shoot(b, name, theme, asserts)
        if theme == "dark":
            for name, route in DARK_ONLY:
                b.goto("%s/index.html?n1=%d%s" % (cdp.BASE, os.getpid(), route),
                       settle=2.4)
                sc.wait_settled(b)
                shoot(b, name, theme, asserts)
        # passport import: arrival, then the conflicts step
        b.goto("%s/index.html?n1=%d#/taste" % (cdp.BASE, os.getpid()), settle=2.0)
        payload = b.ev(MAKE_PAYLOAD)
        b.goto("%s/index.html?n1=%d#/passport/%s" % (cdp.BASE, os.getpid(), payload),
               settle=2.4)
        sc.wait_settled(b)
        shoot(b, "passport-import-arrival", theme, asserts, "step 1")
        clicked = b.ev("(function(){var el=document.querySelector('[data-tsx=\\\"import-review\\\"]');"
                       "if(!el)return 'NO-BUTTON';el.click();return 'clicked';})()")
        time.sleep(1.4)
        sc.wait_settled(b)
        shoot(b, "passport-import-conflicts", theme, asserts, "step 2 · " + str(clicked))
    finally:
        b.close()
    p = os.path.join(OUT, "n1-recap-%s-%d.json" % (theme, W))
    json.dump(asserts, open(p, "w"), indent=1)
    print("wrote %d captures; assertions -> %s" % (len(asserts), p))


if __name__ == "__main__":
    main()
