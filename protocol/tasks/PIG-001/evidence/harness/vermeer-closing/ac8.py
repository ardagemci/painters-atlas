"""AC8 — local persistence cannot be read or written.

"When local persistence cannot be read or written, the interface does not claim
success and preserves context while offering a meaningful retry, recovery, or
export path."

Van Eyck verified only the no-false-success half under a throwing setItem, with
no passport present. This exercises the rest:

  S1 write denied, passport present   - notice? truthful? retry/recovery/export?
  S2 corrupt pigment.taste.v1         - trouble view? bytes preserved or wiped?
  S3 read denied (getItem throws)     - which trouble view, and is it truthful?
  S4 app usable throughout            - routes still render under each failure

Every assertion is read back out of the live DOM.
"""
import json, os, sys, time
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp

OUT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("CDP_PORT", "9333"))
KEY = "pigment.taste.v1"
LOG = []


def step(name, detail):
    LOG.append({"step": name, "observed": detail})
    print("\n### %s" % name)
    print(json.dumps(detail, indent=1)[:2600], flush=True)


# a real-looking passport with one admiration already in it
SEED = json.dumps({
    "version": 1, "createdAt": "2026-07-01T00:00:00.000Z", "updatedAt": "2026-07-01T00:00:00.000Z",
    "admirations": [{"id": "mona-lisa", "at": "2026-07-01T00:00:00.000Z"}],
    "notForMe": [], "seen": [], "wantToSee": [], "saved": [], "probes": [],
    "quiz": None, "palette": None,
    "persona": {"adopted": None, "candidates": [], "adoptedAt": None, "hidden": False},
    "tasteVector": None, "milestones": {"onboarded": False, "confidence": "sketch"}})

# throwing setItem for our key only; reads still work
BREAK_WRITE = """(function(){
 var S=Storage.prototype, orig=S.setItem;
 window.__origSet=orig;
 S.setItem=function(k,v){ if(k===%r){ var e=new Error('QuotaExceededError');
   e.name='QuotaExceededError'; throw e; } return orig.call(this,k,v); };
 return 'setItem now throws for '+%r;})()""" % (KEY, KEY)

BREAK_READ = """(function(){
 var S=Storage.prototype, orig=S.getItem;
 S.getItem=function(k){ if(k===%r){ throw new Error('SecurityError: access denied'); }
   return orig.call(this,k); };
 return 'getItem now throws for '+%r;})()""" % (KEY, KEY)

NOTICE = """(function(){
 var n=document.getElementById('pp-notice');
 if(!n) return JSON.stringify({present:false});
 var cs=getComputedStyle(n), r=n.getBoundingClientRect();
 return JSON.stringify({present:true, hidden:n.hidden, role:n.getAttribute('role'),
  display:cs.display, visible:(r.width>0&&r.height>0&&cs.display!=='none'&&cs.visibility!=='hidden'),
  rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
  text:n.textContent.trim().replace(/\\s+/g,' '),
  actions:[].map.call(n.querySelectorAll('button,a'),function(b){
    return {tag:b.tagName.toLowerCase(), label:b.textContent.trim(),
            act:b.getAttribute('data-tsx')||b.getAttribute('href')};})});})()"""

PPBTN = """(function(){
 var b=document.querySelector('[data-pp="admirations"]');
 if(!b) return JSON.stringify({found:false});
 var r=b.getBoundingClientRect();
 return JSON.stringify({found:true, label:b.textContent.trim(),
  pressed:b.getAttribute('aria-pressed'), onClass:b.classList.contains('on'),
  id:b.dataset.ppid, x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2)});})()"""

PAGE = """(function(){
 var app=document.getElementById('app');
 return JSON.stringify({title:document.title,
  h1:(app.querySelector('h1')||{}).textContent||null,
  lede:((app.querySelector('.page-lede')||{}).textContent||'').trim().replace(/\\s+/g,' ').slice(0,320),
  chips:[].map.call(app.querySelectorAll('.chips .chip'),function(c){
    return {label:c.textContent.trim(), act:c.getAttribute('data-tsx')||c.getAttribute('href')};}),
  cards:app.querySelectorAll('a.card,a.mini-card,a.entry-card').length,
  bodyLen:app.textContent.trim().length});})()"""


def click_at(b, x, y):
    for t in ("mousePressed", "mouseReleased"):
        b.cmd("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left",
                                           "clickCount": 1, "buttons": 1 if t == "mousePressed" else 0})
    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)


def main():
    b = cdp.Browser(port=PORT)
    try:
        b.metrics(1440, 900)

        # ---------- S1: write denied, passport present ----------
        b.goto(cdp.BASE + "/index.html#/", settle=1.2)
        b.ev("localStorage.setItem(%r,%r);localStorage.setItem('pigment-theme','dark');1" % (KEY, SEED))
        b.goto(cdp.BASE + "/index.html?ac8=s1#/artwork/the-starry-night", settle=2.0)
        raw_before = b.ev("localStorage.getItem(%r)" % KEY)
        print("BREAK:", b.ev(BREAK_WRITE))
        before = json.loads(b.ev(PPBTN))
        step("S1.0 seeded passport + Admire control before the click",
             {"passportBytes": len(raw_before or ""), "button": before})
        click_at(b, before["x"], before["y"])
        after = json.loads(b.ev(PPBTN))
        notice = json.loads(b.ev(NOTICE))
        raw_after = b.ev("localStorage.getItem(%r)" % KEY)
        step("S1.1 Admire clicked while setItem throws", {
            "button": after,
            "falseSuccess": after["pressed"] == "true" or after["label"].endswith("✓"),
            "notice": notice,
            "storedBytesUnchanged": raw_after == raw_before,
            "storedBytes": len(raw_after or "")})

        # is the app still usable, and does the notice survive navigation?
        b.ev("location.hash='#/museums'")
        b.ev("new Promise(function(r){setTimeout(r,700)})", await_promise=True)
        step("S1.2 navigate away with the notice up", {
            "page": json.loads(b.ev(PAGE)), "notice": json.loads(b.ev(NOTICE))})

        # exercise the notice's own affordances
        b.goto(cdp.BASE + "/index.html?ac8=s1b#/artwork/the-starry-night", settle=2.0)
        b.ev(BREAK_WRITE)
        bt = json.loads(b.ev(PPBTN)); click_at(b, bt["x"], bt["y"])
        # intercept the export download instead of writing a file
        b.ev("""window.__dl=[];HTMLAnchorElement.prototype.click=function(){
             window.__dl.push({href:(this.href||'').slice(0,120),
             len:(this.href||'').length, download:this.download});};1""")
        exp = b.ev("""(function(){var n=document.getElementById('pp-notice');
              var t=n&&n.querySelector('[data-tsx="export"]'); if(!t)return 'no export chip';
              t.click(); return JSON.stringify(window.__dl);})()""")
        b.ev("new Promise(function(r){setTimeout(r,250)})", await_promise=True)
        dl = b.ev("JSON.stringify(window.__dl)")
        dismiss = b.ev("""(function(){var n=document.getElementById('pp-notice');
              var t=n&&n.querySelector('[data-tsx="notice-close"]'); if(!t)return 'no dismiss chip';
              t.click(); var m=document.getElementById('pp-notice');
              return JSON.stringify({hidden:m.hidden,
               display:getComputedStyle(m).display});})()""")
        step("S1.3 the notice's export and dismiss affordances, actually clicked", {
            "exportClickReturn": exp, "downloadIntercepted": json.loads(dl) if dl else None,
            "afterDismiss": json.loads(dismiss) if dismiss.startswith("{") else dismiss})

        # the "Open the Taste Passport" chip under a failed write
        b.ev("""(function(){var n=document.getElementById('pp-notice');n.hidden=false;
             var a=n.querySelector('a[href="#/taste"]'); a.click();})()""")
        b.ev("new Promise(function(r){setTimeout(r,900)})", await_promise=True)
        step("S1.4 following the notice's 'Open the Taste Passport' chip", {
            "page": json.loads(b.ev(PAGE)),
            "passportStillReadable": bool(b.ev("!!JSON.parse(localStorage.getItem(%r))" % KEY))})

        # ---------- S2: corrupt passport ----------
        CORRUPT = '{"version":1,"admirations":[{"id":"mona-lisa","at":"2026'
        b.goto(cdp.BASE + "/index.html?ac8=s2#/", settle=1.2)
        b.ev("localStorage.setItem(%r,%r);1" % (KEY, CORRUPT))
        b.goto(cdp.BASE + "/index.html?ac8=s2b#/taste", settle=2.0)
        page = json.loads(b.ev(PAGE))
        raw = b.ev("localStorage.getItem(%r)" % KEY)
        step("S2.1 #/taste with corrupt %s" % KEY, {
            "page": page,
            "storedBytesPreserved": raw == CORRUPT,
            "storedBytes": raw,
            "ppState": json.loads(b.ev("JSON.stringify({read:1})"))})

        # does an Admire elsewhere refuse to write over the unreadable bytes?
        b.ev("location.hash='#/artwork/the-starry-night'")
        b.ev("new Promise(function(r){setTimeout(r,1100)})", await_promise=True)
        bt = json.loads(b.ev(PPBTN))
        click_at(b, bt["x"], bt["y"])
        step("S2.2 Admire with a corrupt passport present (no storage break at all)", {
            "button": json.loads(b.ev(PPBTN)),
            "notice": json.loads(b.ev(NOTICE)),
            "storedBytesPreserved": b.ev("localStorage.getItem(%r)" % KEY) == CORRUPT})

        # the trouble view's own affordances: export the raw bytes, then retry, then replace
        b.goto(cdp.BASE + "/index.html?ac8=s2c#/taste", settle=1.8)
        b.ev("""window.__dl=[];HTMLAnchorElement.prototype.click=function(){
             window.__dl.push({href:decodeURIComponent((this.href||'').replace(/^data:[^,]*,/,'')),
             download:this.download});};1""")
        b.ev("""document.querySelector('[data-tsx="export"]').click();1""")
        b.ev("new Promise(function(r){setTimeout(r,300)})", await_promise=True)
        dl2 = json.loads(b.ev("JSON.stringify(window.__dl)"))
        step("S2.3 'Download the stored data' on the trouble view", {
            "downloadIntercepted": dl2,
            "rawBytesRecovered": bool(dl2) and dl2[0]["href"] == CORRUPT,
            "filename": dl2[0]["download"] if dl2 else None})

        b.ev("""document.querySelector('[data-tsx="storage-retry"]').click();1""")
        b.ev("new Promise(function(r){setTimeout(r,700)})", await_promise=True)
        step("S2.4 'Try reading it again' with the data still corrupt", {
            "page": json.loads(b.ev(PAGE)),
            "storedBytesPreserved": b.ev("localStorage.getItem(%r)" % KEY) == CORRUPT})

        b.ev("window.confirm=function(m){window.__confirmMsg=m;return true};1")
        b.ev("""document.querySelector('[data-tsx="storage-reset"]').click();1""")
        b.ev("new Promise(function(r){setTimeout(r,900)})", await_promise=True)
        step("S2.5 'Replace it with a new Passport' (confirm accepted)", {
            "confirmText": b.ev("window.__confirmMsg"),
            "storedAfter": b.ev("localStorage.getItem(%r)" % KEY),
            "page": json.loads(b.ev(PAGE))})

        # ---------- S3: read denied ----------
        b.goto(cdp.BASE + "/index.html?ac8=s3#/", settle=1.2)
        b.ev("localStorage.setItem(%r,%r);1" % (KEY, SEED))
        b.cmd("Page.addScriptToEvaluateOnNewDocument", {"source": BREAK_READ})
        b.goto(cdp.BASE + "/index.html?ac8=s3b#/taste", settle=2.0)
        step("S3.1 #/taste while getItem throws", {
            "page": json.loads(b.ev(PAGE))})
        b.ev("location.hash='#/artwork/the-starry-night'")
        b.ev("new Promise(function(r){setTimeout(r,1100)})", await_promise=True)
        bt = json.loads(b.ev(PPBTN))
        click_at(b, bt["x"], bt["y"])
        step("S3.2 Admire while reads are denied", {
            "button": json.loads(b.ev(PPBTN)),
            "notice": json.loads(b.ev(NOTICE))})

        # ---------- S4: app usable under each failure ----------
        routes = ["#/", "#/artists", "#/museums", "#/museum/louvre", "#/explore",
                  "#/timeline", "#/daily", "#/lists", "#/credits"]
        usable = []
        for r in routes:
            b.ev("location.hash=%r" % r)
            b.ev("new Promise(function(x){setTimeout(x,750)})", await_promise=True)
            p = json.loads(b.ev(PAGE))
            usable.append({"route": r, "h1": p["h1"], "chars": p["bodyLen"], "cards": p["cards"]})
        step("S4 routes rendered while reads are denied", {"routes": usable})
    finally:
        b.close()
    json.dump(LOG, open(os.path.join(OUT, "ac8-storage.json"), "w"), indent=1)
    print("\nwrote ac8-storage.json")


main()
