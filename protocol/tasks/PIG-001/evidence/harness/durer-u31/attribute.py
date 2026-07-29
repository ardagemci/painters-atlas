"""Unit 31 — attribution runs. Measure one selector twice: as shipped, and with
one named layer suppressed. If the ratio moves, the suppressed layer IS the
backdrop the worst pixel sat on. Used for the two findings this unit reports but
does not fix, so that neither is attributed by argument:

  N-31-1  `.tl2-year` vs the 1 px `.tl2-grid` line directly behind it
  N-31-2  `.sr-group` vs the `.main-nav` row that overlaps the open search
          panel at 390 px

usage: python3 attribute.py <theme> <w> <h> <draws> <route> <selector> <suppress-css> [prep]
"""
import json, os, sys

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, H + "/cdp-r2")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp
import inkprobe as ip

theme, vw, vh, draws = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
route, sel, suppress = sys.argv[5], sys.argv[6], sys.argv[7]
prep = getattr(ip, sys.argv[8]) if len(sys.argv) > 8 else None

b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9448")))
try:
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s');"
                     "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                     % (theme, json.dumps(ip.SEED_PASSPORT))})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
    b.metrics(vw, vh)
    for label, extra in (("as shipped", None), ("suppressed", suppress)):
        worst = None
        for d in range(draws):
            b.goto("%s/index.html?u31attr=%d-%d%s" % (cdp.BASE, d, os.getpid(), route),
                   settle=2.0)
            assert b.ev("document.documentElement.dataset.theme") == theme
            if extra:
                b.ev("(function(){var s=document.createElement('style');s.textContent=%s;"
                     "document.head.appendChild(s);return true;})()" % json.dumps(extra))
            ip.wait_settled(b)
            if prep:
                assert b.ev(prep) is True
                b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
            found = json.loads(b.ev(ip.LOCATE % json.dumps(sel)))
            seen = set()
            for ai in sorted({0, len(found) // 2, len(found) - 1}):
                b.ev("(function(){var e=document.querySelectorAll(%s)[%d];"
                     "if(e)e.scrollIntoView({block:'center',inline:'center'});return true;})()"
                     % (json.dumps(sel.split("::")[0]), ai))
                b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                els = [e for e in json.loads(b.ev(ip.LOCATE % json.dumps(sel)))
                       if ip.visible_frac(e["rect"], vw, vh) >= 0.9 and e["idx"] not in seen]
                if not els:
                    continue
                seen |= {e["idx"] for e in els}
                pre = {e["idx"]: tuple(e["rect"]) for e in els}
                res = ip.probe(b, sel, els, vw, vh)
                post = {e["idx"]: tuple(e["rect"])
                        for e in json.loads(b.ev(ip.LOCATE % json.dumps(sel)))}
                if any(post.get(i) != r for i, r in pre.items()):
                    continue
                for r in res:
                    if worst is None or r["worst"] < worst["worst"]:
                        worst = r
        print("%-11s %-5s %4dx%-3d %-28s worst %5.2f  ink %s on %s  '%s'"
              % (label, theme, vw, vh, sel, worst["worst"], worst["ink"],
                 worst["backdrop"], worst["text"]), flush=True)
finally:
    b.close()
