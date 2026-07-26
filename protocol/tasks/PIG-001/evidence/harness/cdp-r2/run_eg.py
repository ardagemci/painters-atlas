"""E — route announcement channels (AC15 / C-8), and
G — 25-route console/network regression sweep + photo credits.
Both run inside a single document so observers and the Resource Timing buffer
survive across hash navigations (which is how a real user moves through the SPA).
"""
import json, time
import cdp

INSTALL = r"""(function(){
 window.__v={live:[],focus:[],err:[],warn:[]};
 var LIVE='[aria-live],[role=status],[role=alert],[role=log]';
 var mo=new MutationObserver(function(ms){ms.forEach(function(m){
   var t=m.target.nodeType===1?m.target:m.target.parentElement;
   if(!t)return; var host=t.closest?t.closest(LIVE):null;
   if(host)window.__v.live.push({sel:host.tagName.toLowerCase()+(host.id?'#'+host.id:'')+
     '[role='+(host.getAttribute('role')||'')+',aria-live='+(host.getAttribute('aria-live')||'')+']',
     text:(host.textContent||'').trim().slice(0,60),type:m.type});});});
 mo.observe(document.documentElement,{subtree:true,childList:true,characterData:true,
   attributes:true,attributeFilter:['aria-live','role']});
 document.addEventListener('focusin',function(e){var t=e.target;
   window.__v.focus.push({sel:t.tagName.toLowerCase()+(t.id?'#'+t.id:'')+
     (t.classList&&t.classList.length?'.'+[].slice.call(t.classList).join('.'):''),
     tabindex:t.getAttribute?t.getAttribute('tabindex'):null,
     text:(t.textContent||'').trim().replace(/\s+/g,' ').slice(0,60),
     role:t.getAttribute?t.getAttribute('role'):null,
     label:t.getAttribute?(t.getAttribute('aria-label')||null):null});},true);
 var ce=console.error, cw=console.warn;
 console.error=function(){window.__v.err.push([].slice.call(arguments).join(' ').slice(0,160));
   return ce.apply(console,arguments);};
 console.warn=function(){window.__v.warn.push([].slice.call(arguments).join(' ').slice(0,160));
   return cw.apply(console,arguments);};
 window.addEventListener('error',function(e){window.__v.err.push('onerror: '+(e.message||''));});
 window.addEventListener('unhandledrejection',function(e){window.__v.err.push('rejection: '+e.reason);});
 return 1;})()"""

RESET = "window.__v.live=[];window.__v.focus=[];1"
READ = "JSON.stringify({live:window.__v.live,focus:window.__v.focus," \
       "active:(function(a){return a?a.tagName.toLowerCase()+(a.id?'#'+a.id:'')+" \
       "(a.classList&&a.classList.length?'.'+[].slice.call(a.classList).join('.'):'')" \
       "+'|tabindex='+(a.getAttribute?a.getAttribute('tabindex'):'')+'|'+" \
       "(a.textContent||'').trim().replace(/\\s+/g,' ').slice(0,50):null;})(document.activeElement),"\
       "liveEls:document.querySelectorAll('[aria-live],[role=status],[role=alert],[role=log]').length," \
       "h1:(function(h){return h?h.textContent.trim().slice(0,60):null;})(document.querySelector('#app h1')),"\
       "title:document.title})"

SAMPLE = ["#/museums", "#/timeline", "#/palette", "#/credits", "#/no-such-page"]


def nav(b, h, wait=0.85):
    b.ev("location.hash=%r" % h)
    b.ev("new Promise(function(r){setTimeout(r,%d)})" % int(wait * 1000), await_promise=True)


def main():
    b = cdp.Browser()
    out = {}
    try:
        b.metrics(1440, 900)
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','dark')}catch(e){}"})
        b.goto(cdp.BASE + "/index.html?eg=1#/", settle=2.0)
        b.ev(INSTALL)

        # ---------------- E: route announcement
        e_rows = []
        for h in SAMPLE:
            b.ev(RESET)
            nav(b, h, 1.0)
            r = json.loads(b.ev(READ))
            e_rows.append({"route": h, **r})
            print("E", h, "live=%d liveEls=%d active=%s" %
                  (len(r["live"]), r["liveEls"], r["active"]), flush=True)
        out["E"] = e_rows

        # ---------------- G: full route sweep in the same document
        routes = json.load(open("zoom200.json"))["routes"]
        for h in routes:
            nav(b, h, 0.7)
        b.ev("new Promise(function(r){setTimeout(r,2500)})", await_promise=True)

        g = json.loads(b.ev(r"""JSON.stringify((function(){
         var res=performance.getEntriesByType('resource');
         var hosts={},bad=[];
         res.forEach(function(e){var h;try{h=new URL(e.name).host}catch(x){h='?'}
          hosts[h]=(hosts[h]||0)+1;
          if(typeof e.responseStatus==='number'&&e.responseStatus>=400)
            bad.push(e.responseStatus+' '+e.name.slice(0,110));});
         return {hosts:hosts,total:res.length,bad:bad,
          statusSupported:res.length?('responseStatus' in res[0]):false,
          errors:window.__v.err,warnings:window.__v.warn};})())"""))
        out["G_resources"] = g
        print("\nG hosts", json.dumps(g["hosts"]), "total", g["total"],
              "bad", len(g["bad"]), "errors", len(g["errors"]), "warnings", len(g["warnings"]), flush=True)

        # broken images across routes
        broken = []
        for h in routes:
            nav(b, h, 0.9)
            r = json.loads(b.ev("JSON.stringify({n:document.images.length,"
                                "b:[].filter.call(document.images,function(i){"
                                "return i.complete&&i.naturalWidth===0}).length})"))
            broken.append({"route": h, **r})
        out["G_images"] = broken
        print("G images checked", sum(x["n"] for x in broken),
              "broken", sum(x["b"] for x in broken), flush=True)

        # CDP-level console/log entries
        cdp_console = [e for e in b.events if e.get("method") in
                       ("Runtime.consoleAPICalled", "Log.entryAdded", "Runtime.exceptionThrown")]
        sev = []
        for e in cdp_console:
            p = e["params"]
            if e["method"] == "Log.entryAdded":
                en = p["entry"]
                if en.get("level") in ("error", "warning"):
                    sev.append("%s %s %s" % (en["level"], en.get("source"), en.get("text", "")[:120]))
            elif e["method"] == "Runtime.consoleAPICalled":
                if p.get("type") in ("error", "warning", "assert"):
                    sev.append("console.%s %s" % (p["type"], json.dumps(p.get("args", []))[:120]))
            else:
                sev.append("exception " + json.dumps(p)[:140])
        out["G_cdp_console"] = sev
        print("G CDP error/warning entries:", len(sev), flush=True)
        for s in sev[:10]:
            print("   ", s)

        # ---------------- photo credits
        cred = {}
        for name, h in (("museum-louvre", "#/museum/louvre"), ("artwork-david", "#/artwork/david")):
            nav(b, h, 1.4)
            cred[name] = json.loads(b.ev(r"""JSON.stringify((function(){
             var c=[].slice.call(document.querySelectorAll('.img-credit'));
             return {count:c.length, texts:c.map(function(e){return e.textContent.trim().replace(/\s+/g,' ').slice(0,150)}),
              links:c.map(function(e){return [].map.call(e.querySelectorAll('a'),function(a){
                return a.getAttribute('rel')+' :: '+a.getAttribute('href').slice(0,80)})}),
              rawLeak:c.some(function(e){return /&lt;|&gt;|<[a-z]+>/i.test(e.textContent)})};})())"""))
            print("CRED", name, cred[name]["count"], cred[name]["texts"][:1], flush=True)
        out["credits"] = cred
    finally:
        b.close()
    json.dump(out, open("eg.json", "w"), indent=1)


main()
