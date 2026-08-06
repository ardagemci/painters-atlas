"""PIG-001 N-1 — the two passport-import mobile frames, recaptured at HEAD.

Split out of n1recap.py because the first attempt produced NO conflicts: the
harness's SEED_PASSPORT leaves quiz/palette/persona.adopted empty, and
ppFieldKey() treats an empty shell as "no decision", so passportConflicts()
returned [] and the arrival screen offered "Merge into my passport" instead of
"Choose what to keep". Step 2 therefore never rendered and the conflicts file
was a duplicate of the arrival file. Here the LOCAL passport is given a decision
in all four single-value fields and the incoming payload differs in all four, so
the conflicts step is real.

Same shutter discipline: setDeviceMetricsOverride, innerWidth asserted in-page.

usage: python3 n1pp.py <theme>
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

MINE = """(function(){
  var p = JSON.parse(localStorage.getItem('pigment.taste.v1'));
  p.quiz = {answers:{mood:'calm', era:'baroque'}, at:'2026-07-29'};
  p.palette = {tones:[TASTE_TONES[0].id, TASTE_TONES[1].id]};
  p.persona = {adopted:PERSONAS[0].id, candidates:[], adoptedAt:'2026-07-29', hidden:false};
  p.milestones = {onboarded:true, confidence:'sketch'};
  localStorage.setItem('pigment.taste.v1', JSON.stringify(p));
  return PERSONAS[0].id + ' / ' + PERSONAS[1].id;
})()"""

THEIRS = """(function(){
  var p = JSON.parse(localStorage.getItem('pigment.taste.v1'));
  p.quiz = {answers:{mood:'restless', era:'modern'}, at:'2026-08-01'};
  p.palette = {tones:[TASTE_TONES[2].id, TASTE_TONES[3].id]};
  p.persona = {adopted:PERSONAS[1].id, candidates:[], adoptedAt:'2026-08-01', hidden:false};
  p.milestones = {onboarded:true, confidence:'atlas'};
  p.admirations = (p.admirations||[]).concat([{id:'the-scream', at:'2026-08-01'}]);
  var j = JSON.stringify(p);
  return btoa(unescape(encodeURIComponent(j)))
    .replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');
})()"""


def shoot(b, name, theme, asserts, note=""):
    iw = b.ev("window.innerWidth")
    th = b.ev("document.documentElement.dataset.theme")
    h1 = b.ev("(document.querySelector('h1')||{}).textContent||''")
    kick = b.ev("(document.querySelector('.page-kicker')||{}).textContent||''")
    assert iw == W, "innerWidth %s != %s for %s" % (iw, W, name)
    assert th == theme, "theme %s != %s for %s" % (th, theme, name)
    out = os.path.join(EV, "%s__%s__%s.png" % (name, VP, theme))
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False})
    open(out, "wb").write(base64.b64decode(r["data"]))
    rec = {"file": os.path.basename(out), "theme": th, "innerWidth": iw,
           "innerHeight": b.ev("window.innerHeight"),
           "h1": (h1 or "").strip()[:60], "kicker": (kick or "").strip()[:80],
           "bytes": os.path.getsize(out), "note": note}
    asserts.append(rec)
    print("%-28s iw=%-4d th=%-5s %7d B  kicker=%-42s h1=%s"
          % (name, iw, th, rec["bytes"], rec["kicker"], rec["h1"]), flush=True)


def main():
    theme = sys.argv[1]
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9493")))
    asserts = []
    try:
        sc.boot(b, theme)
        b.metrics(W, H)
        b.goto("%s/index.html?n1pp=%d#/taste" % (cdp.BASE, os.getpid()), settle=2.0)
        print("personas:", b.ev(MINE), flush=True)
        payload = b.ev(THEIRS)
        b.goto("%s/index.html?n1pp=%d#/passport/%s" % (cdp.BASE, os.getpid(), payload),
               settle=2.4)
        sc.wait_settled(b)
        shoot(b, "passport-import-arrival", theme, asserts, "step 1")
        clicked = b.ev("(function(){var el=document.querySelector('[data-tsx=\\\"import-review\\\"]');"
                       "if(!el)return 'NO-BUTTON:'+document.body.innerHTML.length;"
                       "el.click();return 'clicked';})()")
        time.sleep(1.4)
        sc.wait_settled(b)
        b.ev("window.scrollTo(0,0)")
        shoot(b, "passport-import-conflicts", theme, asserts, "step 2 · " + str(clicked))
    finally:
        b.close()
    p = os.path.join(OUT, "n1-recap-pp-%s.json" % theme)
    json.dump(asserts, open(p, "w"), indent=1)
    print("wrote %d captures; assertions -> %s" % (len(asserts), p))


if __name__ == "__main__":
    main()
