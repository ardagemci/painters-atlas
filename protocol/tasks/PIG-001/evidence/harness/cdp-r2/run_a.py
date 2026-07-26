import json, os, sys, time
import cdp

OUT = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"

PROBE = """(function(){
 var nav=document.querySelector('.main-nav'), app=document.getElementById('app');
 var cs=nav?getComputedStyle(nav):null, ca=getComputedStyle(app);
 var nr=nav?nav.getBoundingClientRect():null;
 return JSON.stringify({
  iw:window.innerWidth, cw:document.documentElement.clientWidth,
  sw:document.documentElement.scrollWidth,
  appPadL:ca.paddingLeft, appPadT:ca.paddingTop,
  navOrder:cs?cs.order:null, navOverflowX:cs?cs.overflowX:null,
  navWrap:cs?cs.flexWrap:null,
  navW:nr?Math.round(nr.width):null, navH:nr?Math.round(nr.height):null,
  navLinks:nav?nav.querySelectorAll('a').length:0,
  navVisible: nr? (nr.width>0 && nr.height>0 && nr.top < window.innerHeight) : false,
  theme:document.documentElement.dataset.theme,
  h1:(document.querySelector('#app h1')||{}).textContent||null,
  imgs:document.images.length,
  brokenImgs:[].filter.call(document.images,function(i){return i.complete&&i.naturalWidth===0}).length
 });})()"""

def main():
    b = cdp.Browser()
    log = []
    try:
        n = 0
        for theme in ["dark", "light"]:
            sid = b.cmd("Page.addScriptToEvaluateOnNewDocument",
                        {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})["identifier"]
            for (w, h, vp) in [(1440, 900, "desktop-1440x900"), (390, 844, "mobile-390x844")]:
                b.metrics(w, h)
                for (slug, route) in cdp.ROUTES16:
                    n += 1
                    url = "%s/index.html?vr=%d%s" % (cdp.BASE, n, route)
                    b.goto(url, settle=1.7)
                    p = json.loads(b.ev(PROBE))
                    fn = "%s/%s__%s__%s.png" % (OUT, slug, vp, theme)
                    size = b.shot(fn)
                    # capture-time assertions
                    exp_pad = "16px" if w == 390 else "28px"
                    exp_padT = "22px" if w == 390 else "34px"
                    ok = (p["iw"] == w and p["cw"] == w and p["appPadL"] == exp_pad
                          and p["appPadT"] == exp_padT and p["theme"] == theme
                          and p["navVisible"] is True and p["navLinks"] == 8)
                    if w == 390:
                        ok = ok and p["navOrder"] == "3" and p["navOverflowX"] == "auto"
                    else:
                        ok = ok and p["navOrder"] == "0" and p["navOverflowX"] == "visible"
                    p.update({"slug": slug, "vp": vp, "theme": theme, "png": os.path.basename(fn),
                              "bytes": size, "ASSERT": "PASS" if ok else "FAIL"})
                    log.append(p)
                    print(n, slug, vp, theme, p["ASSERT"], "iw=%s pad=%s nav=%sx%s sw=%s" %
                          (p["iw"], p["appPadL"], p["navW"], p["navH"], p["sw"]), flush=True)
            b.cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": sid})
    finally:
        b.close()
    with open("capture-assertions.json", "w") as f:
        json.dump(log, f, indent=1)
    bad = [x for x in log if x["ASSERT"] != "PASS"]
    print("\nTOTAL", len(log), "FAILED ASSERTIONS", len(bad))
    for x in bad:
        print("  FAIL", x["slug"], x["vp"], x["theme"], x)

main()
