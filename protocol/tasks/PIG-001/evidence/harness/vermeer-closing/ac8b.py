"""AC8 addendum — S1.4 redone with a real mouse click.

In ac8.py my own instrumentation (overriding HTMLAnchorElement.prototype.click to
intercept the export download) also disabled the notice's "Open the Taste
Passport" link, so that step measured my harness rather than the build. Redone
here with a genuine CDP mouse click and no override in place.
"""
import json, os, sys
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp

PORT = int(os.environ.get("CDP_PORT", "9333"))
KEY = "pigment.taste.v1"
OUT = os.path.dirname(os.path.abspath(__file__))
SEED = json.dumps({"version": 1, "createdAt": "2026-07-01T00:00:00.000Z",
                   "updatedAt": "2026-07-01T00:00:00.000Z",
                   "admirations": [{"id": "mona-lisa", "at": "2026-07-01T00:00:00.000Z"}],
                   "notForMe": [], "seen": [], "wantToSee": [], "saved": [], "probes": [],
                   "quiz": None, "palette": None,
                   "persona": {"adopted": None, "candidates": [], "adoptedAt": None, "hidden": False},
                   "tasteVector": None, "milestones": {"onboarded": False, "confidence": "sketch"}})
BREAK_WRITE = """(function(){var S=Storage.prototype,o=S.setItem;
 S.setItem=function(k,v){if(k===%r){var e=new Error('QuotaExceededError');
  e.name='QuotaExceededError';throw e;}return o.call(this,k,v);};return 1;})()""" % KEY


def click(b, x, y):
    for t in ("mousePressed", "mouseReleased"):
        b.cmd("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left",
                                           "clickCount": 1, "buttons": 1 if t == "mousePressed" else 0})
    b.ev("new Promise(function(r){setTimeout(r,900)})", await_promise=True)


b = cdp.Browser(port=PORT)
out = {}
try:
    b.metrics(1440, 900)
    b.goto(cdp.BASE + "/index.html#/", settle=1.2)
    b.ev("localStorage.setItem(%r,%r);1" % (KEY, SEED))
    b.goto(cdp.BASE + "/index.html?ac8b=1#/artwork/the-starry-night", settle=2.0)
    b.ev(BREAK_WRITE)
    p = json.loads(b.ev("""(function(){var b=document.querySelector('[data-pp="admirations"]');
        var r=b.getBoundingClientRect();return JSON.stringify(
        {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});})()"""))
    click(b, p["x"], p["y"])
    out["noticeUp"] = b.ev("!!document.getElementById('pp-notice')")
    q = json.loads(b.ev("""(function(){var a=document.querySelector('#pp-notice a[href="#/taste"]');
        var r=a.getBoundingClientRect();return JSON.stringify(
        {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),label:a.textContent});})()"""))
    out["chip"] = q
    click(b, q["x"], q["y"])
    out["afterClick"] = json.loads(b.ev("""(function(){var a=document.getElementById('app');
        return JSON.stringify({hash:location.hash,title:document.title,
         h1:(a.querySelector('h1')||{}).textContent||null,
         focus:document.activeElement.tagName+'.'+document.activeElement.className,
         admirationsShown:a.textContent.indexOf('Mona Lisa')>=0});})()"""))
    out["passportIntact"] = b.ev(
        "JSON.parse(localStorage.getItem(%r)).admirations.length" % KEY)
finally:
    b.close()
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(OUT, "ac8-notice-chip.json"), "w"), indent=1)
