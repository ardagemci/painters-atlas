"""D2 — targeted re-checks at 200% text zoom, plus the 26th route and zoom shots.

  * button.skip-inline measured FOCUSED (unfocused it is a deliberate 1x1
    visually-hidden control, so an unfocused clip reading is an artifact).
  * div.mu-hero on both museum routes, with enough detail to say whether any
    content is actually lost.
  * #/artwork/david, the router case missing from the discovery sweep.
  * .main-nav used width vs its declared width at 390.
"""
import json
import cdp

OUT = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"


def zoom(b):
    b.ev("document.documentElement.style.fontSize='200%'")
    b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
    b.ev("document.documentElement.style.fontSize='200%'")


def main():
    b = cdp.Browser()
    out = {}
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','dark')}catch(e){}"})
        b.metrics(1270, 800)

        # ---- 26th router case
        b.goto(cdp.BASE + "/index.html?d2=aw#/artwork/david", settle=1.6)
        zoom(b)
        out["artwork"] = json.loads(b.ev(
            "JSON.stringify({cw:document.documentElement.clientWidth,"
            "sw:document.documentElement.scrollWidth,"
            "over:document.documentElement.scrollWidth-document.documentElement.clientWidth})"))
        print("artwork/david @200%", out["artwork"], flush=True)

        # ---- skip-inline, focused
        b.goto(cdp.BASE + "/index.html?d2=inf#/influences", settle=2.2)
        zoom(b)
        out["skip_inline"] = {}
        for state in ("unfocused", "focused"):
            if state == "focused":
                b.ev("document.querySelector('button.skip-inline').focus()")
                b.ev("new Promise(function(r){setTimeout(r,350)})", await_promise=True)
            out["skip_inline"][state] = json.loads(b.ev(r"""(function(){
             var el=document.querySelector('button.skip-inline'),cs=getComputedStyle(el),
              r=el.getBoundingClientRect();
             return JSON.stringify({pos:cs.position,ovx:cs.overflowX,ovy:cs.overflowY,
              w:Math.round(r.width),h:Math.round(r.height),
              left:Math.round(r.left),right:Math.round(r.right),top:Math.round(r.top),
              lostW:el.scrollWidth-el.clientWidth, lostH:el.scrollHeight-el.clientHeight,
              inViewport:(r.left>=0&&r.right<=innerWidth),
              isActive:document.activeElement===el,
              text:el.textContent.trim().slice(0,60), color:cs.color, bg:cs.backgroundColor});})()"""))
            print("skip-inline", state, out["skip_inline"][state], flush=True)

        # ---- mu-hero on both museums
        out["mu_hero"] = {}
        for m in ("louvre", "met"):
            b.goto(cdp.BASE + "/index.html?d2=%s#/museum/%s" % (m, m), settle=2.2)
            zoom(b)
            out["mu_hero"][m] = json.loads(b.ev(r"""(function(){
             var h=document.querySelector('div.mu-hero'); if(!h) return JSON.stringify(null);
             var cs=getComputedStyle(h), hr=h.getBoundingClientRect();
             var body=h.querySelector('.mu-hero-body');
             var br=body?body.getBoundingClientRect():null;
             var kids=[].map.call(h.children,function(c){var r=c.getBoundingClientRect();
              return {sel:c.tagName.toLowerCase()+(c.classList.length?'.'+[].slice.call(c.classList).join('.'):''),
               pos:getComputedStyle(c).position, top:Math.round(r.top), h:Math.round(r.height)};});
             var texts=[].map.call(h.querySelectorAll('h1,p,span,div'),function(e){
              var t=(e.childNodes.length&&[].filter.call(e.childNodes,function(n){return n.nodeType===3&&n.nodeValue.trim()}).length)?e:null;
              if(!t)return null; var r=e.getBoundingClientRect();
              return {sel:e.tagName.toLowerCase()+(e.classList.length?'.'+[].slice.call(e.classList).join('.'):''),
               top:Math.round(r.top),bottom:Math.round(r.bottom),
               aboveHero:r.top<hr.top-0.5, belowHero:r.bottom>hr.bottom+0.5,
               txt:e.textContent.trim().replace(/\s+/g,' ').slice(0,40)};}).filter(Boolean);
             return JSON.stringify({height:cs.height,minHeight:cs.minHeight,overflow:cs.overflow,
              display:cs.display,alignItems:cs.alignItems,
              clientH:h.clientHeight,scrollH:h.scrollHeight,lostH:h.scrollHeight-h.clientHeight,
              clientW:h.clientWidth,scrollW:h.scrollWidth,lostW:h.scrollWidth-h.clientWidth,
              heroTop:Math.round(hr.top),heroBottom:Math.round(hr.bottom),
              bodyTop:br?Math.round(br.top):null,bodyH:br?Math.round(br.height):null,
              children:kids, textsOutside:texts.filter(function(t){return t.aboveHero||t.belowHero}),
              textCount:texts.length});})()"""))
            print("mu-hero", m, json.dumps(out["mu_hero"][m])[:400], flush=True)

        # ---- nav width at 390
        b.metrics(390, 844)
        b.goto(cdp.BASE + "/index.html?d2=nav#/", settle=1.6)
        out["nav390"] = json.loads(b.ev(r"""(function(){
         var n=document.querySelector('.main-nav'),cs=getComputedStyle(n),r=n.getBoundingClientRect();
         var hd=document.querySelector('.site-header');
         return JSON.stringify({declaredWidth:cs.width,flexBasis:cs.flexBasis,flexGrow:cs.flexGrow,
          flexWrap:cs.flexWrap,usedWidth:Math.round(r.width),usedHeight:Math.round(r.height),
          scrollWidth:n.scrollWidth,clientWidth:n.clientWidth,
          headerHeight:Math.round(hd.getBoundingClientRect().height),
          maskImage:cs.webkitMaskImage||cs.maskImage,
          linkOverflowing:[].filter.call(n.querySelectorAll('a'),function(a){
            return a.getBoundingClientRect().right>r.right+0.5;}).length,
          links:n.querySelectorAll('a').length});})()"""))
        print("NAV390", json.dumps(out["nav390"]), flush=True)

        # ---- zoom screenshots (evidence)
        for theme in ("dark", "light"):
            b.cmd("Page.addScriptToEvaluateOnNewDocument",
                  {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
            b.metrics(1280, 800)
            for slug, r in (("home", "#/"), ("artists", "#/artists"),
                            ("influences", "#/influences"), ("museum-louvre", "#/museum/louvre")):
                b.goto("%s/index.html?zs=%s_%s%s" % (cdp.BASE, theme, slug, r), settle=2.0)
                zoom(b)
                if slug == "influences":
                    b.ev("document.querySelector('button.skip-inline').focus()")
                    b.ev("new Promise(function(r){setTimeout(r,300)})", await_promise=True)
                b.shot("%s/zoom200-%s__desktop-1280x800__%s.png" % (OUT, slug, theme))
                print("shot zoom200", slug, theme, flush=True)
    finally:
        b.close()
    json.dump(out, open("d2.json", "w"), indent=1)


main()
