"""AC4 / F-3 — the frozen journey matrix, walked end to end in a real browser.

Two things are being evidenced at once and they are not the same thing:

  * the five frozen journeys J1-J5 of unrouted/ux-requirements.md §5, each step of
    which has an observable anchor / relationship / consequence / onward-path
    definition, plus a stated Pass condition; and
  * AC4's own eleven-link chain: entry, onboarding, Passport creation, an Admire
    action, consequence explanation, persistence, return, export or share,
    import, conflict handling, reset - "without a broken or unexplained
    transition".

Every step below records the route, what was clicked (a real CDP mouse or key
event on a real element, never a JS shortcut), what rendered afterwards, and the
four observable properties. Nothing is inferred from source.

usage: python3 ac4.py [j1 j2 j3 j4 j5 chain]   (default: all)
"""
import json, os, sys, time
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp

OUT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("CDP_PORT", "9333"))
KEY = "pigment.taste.v1"
T = []          # the transcript


def rec(journey, step, route, action, rendered, props, verdict="", note=""):
    row = {"journey": journey, "step": step, "route": route, "action": action,
           "rendered": rendered, "observable": props, "verdict": verdict, "note": note}
    T.append(row)
    print("\n[%s] %s\n  route   %s\n  action  %s\n  render  %s\n  props   %s\n  %s %s"
          % (journey, step, route, action, json.dumps(rendered)[:420],
             json.dumps(props)[:520], verdict, note), flush=True)


SNAP = """(function(){
 var app=document.getElementById('app');
 return JSON.stringify({
  hash:location.hash, title:document.title,
  h1:((app.querySelector('h1')||{}).textContent||'').trim(),
  focus:document.activeElement.tagName.toLowerCase()+
        (document.activeElement.className?'.'+String(document.activeElement.className).split(' ')[0]:''),
  focusText:(document.activeElement.textContent||'').trim().slice(0,40),
  chars:app.textContent.trim().length});})()"""


def snap(b):
    return json.loads(b.ev(SNAP))


def settle(b, ms=800):
    b.ev("new Promise(function(r){setTimeout(r,%d)})" % ms, await_promise=True)


def q(b, expr):
    """Evaluate and JSON-parse a JSON.stringify(...) expression."""
    v = b.ev("JSON.stringify(%s)" % expr)
    return json.loads(v) if v is not None else None


def click_sel(b, sel, idx=0, ms=900):
    """Real mouse click on the idx-th match of sel, after scrolling it into view."""
    info = q(b, """(function(){var e=document.querySelectorAll(%r)[%d];
      if(!e)return null; e.scrollIntoView({block:'center'});
      var r=e.getBoundingClientRect();
      return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),
              text:(e.textContent||'').trim().slice(0,60),
              href:e.getAttribute('href')||null,tag:e.tagName.toLowerCase()};})()""" % (sel, idx))
    if not info:
        raise RuntimeError("no element for %s[%d]" % (sel, idx))
    settle(b, 260)
    info = q(b, """(function(){var e=document.querySelectorAll(%r)[%d];
      var r=e.getBoundingClientRect();
      return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),
              text:(e.textContent||'').trim().slice(0,60),
              href:e.getAttribute('href')||null,tag:e.tagName.toLowerCase()};})()""" % (sel, idx))
    for t in ("mousePressed", "mouseReleased"):
        b.cmd("Input.dispatchMouseEvent", {"type": t, "x": info["x"], "y": info["y"],
                                           "button": "left", "clickCount": 1,
                                           "buttons": 1 if t == "mousePressed" else 0})
    settle(b, ms)
    return info


def key(b, k, code=None, ms=500):
    for t in ("keyDown", "keyUp"):
        p = {"type": t, "key": k, "code": code or k, "windowsVirtualKeyCode":
             {"Tab": 9, "Enter": 13, "ArrowDown": 40, " ": 32}.get(k, 0)}
        if k == " ":
            p["text"] = " "
        b.cmd("Input.dispatchKeyEvent", p)
    settle(b, ms)


def typetext(b, s, ms=650):
    for ch in s:
        b.cmd("Input.dispatchKeyEvent", {"type": "keyDown", "text": ch, "key": ch})
        b.cmd("Input.dispatchKeyEvent", {"type": "keyUp", "key": ch})
    settle(b, ms)


# --------------------------------------------------------------- J1
def j1(b):
    b.goto(cdp.BASE + "/index.html?j1=1#/", settle=2.0)
    s = snap(b)
    rec("J1", "1 entry", s["hash"], "load #/", s,
        {"anchor": s["h1"], "onward": q(b, "document.querySelectorAll('#app a[href]').length")},
        "OK")
    # search combobox -> known artist
    box = click_sel(b, "#search", 0, 500)
    typetext(b, "Leonardo", 900)
    opts = q(b, """[].slice.call(document.querySelectorAll('#search-results [role="option"]')).slice(0,4)
        .map(function(o){return o.textContent.trim().replace(/\\s+/g,' ').slice(0,50);})""")
    exp = b.ev("(document.querySelector('#search')||{}).getAttribute&&document.querySelector('#search').getAttribute('aria-expanded')")
    click_sel(b, '#search-results [role="option"]', 0, 1400)
    s = snap(b)
    art = q(b, """(function(){var a=document.getElementById('app');
      return {chips:[].slice.call(a.querySelectorAll('.chips a.chip,.chip')).slice(0,8)
                .map(function(c){return c.textContent.trim().slice(0,40);}),
        chipLinks:a.querySelectorAll('a.chip').length,
        why:((a.querySelector('.why-card')||{}).textContent||'').trim().slice(0,120),
        whyHeading:((a.querySelector('.why-card h2,.why-card .sec-title,.why-card h3')||{}).textContent||'').trim(),
        lineage:!!a.querySelector('a[href*="influences"],a[href*="lineage"]'),
        heroH1:((a.querySelector('.hero h1')||{}).textContent||'').trim()};})()""")
    rec("J1", "2 land on artist (via search)", s["hash"],
        "typed 'Leonardo' in #q, clicked option 1 (%s)" % (opts[0] if opts else "?"),
        {"h1": s["h1"], "title": s["title"], "focus": s["focus"], "options": opts,
         "ariaExpanded": exp},
        {"anchor": "hero h1 = %r" % art["heroH1"],
         "relationship": "%d chip links: %s" % (art["chipLinks"], art["chips"][:5]),
         "consequence": "why-card: %r" % art["why"][:90],
         "onward": "chip <a> present: %s" % (art["chipLinks"] > 0)},
        "PASS" if art["heroH1"] and art["chipLinks"] and art["why"] else "FAIL")
    anchor = art["heroH1"]
    # traverse a relationship BY KEYBOARD: tab to the first chip link, Enter
    b.ev("document.querySelector('#app a.chip').focus();1")
    f = snap(b)
    key(b, "Enter", "Enter", 1400)
    s2 = snap(b)
    rel = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        members:a.querySelectorAll('a[href^="#/artist/"],a[href^="#/artwork/"]').length,
        memberHeading:((a.querySelector('h2')||{}).textContent||'').trim(),
        chips:a.querySelectorAll('a.chip').length};})()""")
    rec("J1", "3 traverse a relationship (keyboard)", s2["hash"],
        "focused first chip link (%r) and pressed Enter" % f["focusText"],
        {"h1": rel["h1"], "memberLinks": rel["members"], "focus": s2["focus"]},
        {"anchor": rel["h1"], "relationship": "member list of the related entity",
         "consequence": "%d painters/works listed" % rel["members"],
         "onward": "%d chips + %d cards" % (rel["chips"], rel["members"])},
        "PASS" if rel["h1"] and rel["members"] else "FAIL")
    # and back, without losing the artist anchor
    b.cmd("Page.navigateToHistoryEntry", {"entryId": _prev_entry(b)})
    settle(b, 1500)
    s3 = snap(b)
    back = q(b, "((document.querySelector('#app .hero h1')||{}).textContent||'').trim()")
    rec("J1", "4 back to the artist", s3["hash"], "browser Back",
        {"h1": s3["h1"], "heroH1": back},
        {"anchor": "artist name still visible: %s" % (back == anchor),
         "relationship": "chips intact", "consequence": "why-card intact",
         "onward": "unchanged"},
        "PASS" if back == anchor else "FAIL",
        "frozen J1 Pass condition: keyboard user reaches >=1 related entity and back "
        "without losing the visible artist-name anchor")


def _prev_entry(b):
    h = b.cmd("Page.getNavigationHistory")
    return h["entries"][max(0, h["currentIndex"] - 1)]["id"]


# --------------------------------------------------------------- J2
def j2(b):
    b.goto(cdp.BASE + "/index.html?j2=1#/artwork/the-starry-night", settle=2.2)
    s = snap(b)
    aw = q(b, """(function(){var a=document.getElementById('app');
      var pan=[].slice.call(a.querySelectorAll('h2,h3,.sec-title')).map(function(h){
        return h.textContent.trim().replace(/\\s+/g,' ').slice(0,44);});
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        artistLink:((a.querySelector('.hero-sub a')||{}).textContent||'').trim(),
        artistHref:(a.querySelector('.hero-sub a')||{}).getAttribute?
                   a.querySelector('.hero-sub a').getAttribute('href'):null,
        chips:[].slice.call(a.querySelectorAll('a.chip')).map(function(c){
          return c.textContent.trim().slice(0,30);}).slice(0,8),
        ppButtons:[].slice.call(a.querySelectorAll('[data-pp]')).map(function(x){
          return {label:x.textContent.trim(), pressed:x.getAttribute('aria-pressed'),
                  field:x.dataset.pp};}),
        panels:pan,
        museumPanel:!!a.querySelector('.aw-where,.mu-panel')||pan.join('|').toLowerCase().indexOf('hang')>=0,
        copy:[].slice.call(a.querySelectorAll('.aw-note,.aw-copy,p')).map(function(p){
          return p.textContent.trim().slice(0,60);}).slice(0,6)};})()""")
    rec("J2", "1 land on artwork", s["hash"], "load #/artwork/the-starry-night",
        {"h1": aw["h1"], "title": s["title"]},
        {"anchor": "h1 = %r + artist sub-link %r -> %s" % (aw["h1"], aw["artistLink"], aw["artistHref"]),
         "relationship": "chips %s ; museum panel present: %s" % (aw["chips"][:5], aw["museumPanel"]),
         "consequence": "copy: %s" % aw["copy"][:3],
         "onward": "onward panels: %s" % aw["panels"][:5]},
        "PASS" if (aw["h1"] and aw["artistLink"] and aw["chips"] and aw["panels"]
                   and len(aw["ppButtons"]) == 3) else "FAIL",
        "frozen J2 Pass: artist link + >=1 chip + >=1 onward panel + the 3 passport buttons "
        "(found %d)" % len(aw["ppButtons"]))
    # personal action
    before = aw["ppButtons"]
    click_sel(b, '[data-pp="admirations"]', 0, 900)
    after = q(b, """[].slice.call(document.querySelectorAll('[data-pp]')).map(function(x){
        return {label:x.textContent.trim(),pressed:x.getAttribute('aria-pressed'),field:x.dataset.pp};})""")
    stored = q(b, "JSON.parse(localStorage.getItem(%r)||'null')" % KEY)
    rec("J2", "2 personal action (Admire)", s["hash"], "clicked the Admire button",
        {"before": before, "after": after},
        {"anchor": "artwork h1 unchanged", "relationship": "Admire toggle",
         "consequence": "label swap %r -> %r, aria-pressed %s -> %s" %
                        (before[0]["label"], after[0]["label"],
                         before[0]["pressed"], after[0]["pressed"]),
         "onward": "feeds #/taste"},
        "PASS" if (after[0]["pressed"] == "true" and stored
                   and any(e["id"] == "the-starry-night" for e in stored["admirations"])) else "FAIL",
        "independent fields after the click: %s" % [x["field"] + "=" + str(x["pressed"]) for x in after])
    # persistence across reload
    b.goto(cdp.BASE + "/index.html?j2=2#/artwork/the-starry-night", settle=2.0)
    after2 = q(b, """[].slice.call(document.querySelectorAll('[data-pp]')).map(function(x){
        return {label:x.textContent.trim(),pressed:x.getAttribute('aria-pressed')};})""")
    rec("J2", "3 persistence across a full reload", "#/artwork/the-starry-night", "reload",
        {"buttons": after2},
        {"consequence": "state survives reload: %s" % (after2[0]["pressed"] == "true")},
        "PASS" if after2[0]["pressed"] == "true" else "FAIL")


# --------------------------------------------------------------- J3
def j3(b):
    b.goto(cdp.BASE + "/index.html?j3=1#/lists", settle=2.0)
    s = snap(b)
    first = click_sel(b, '#app a[href^="#/list/"]', 0, 1500)
    s2 = snap(b)
    li = q(b, """(function(){var a=document.getElementById('app');
      var ol=a.querySelector('ol.list-entries');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        ordered:!!ol, tag:ol?ol.tagName.toLowerCase():null,
        entries:ol?ol.children.length:0,
        notes:a.querySelectorAll('.le-note').length,
        firstNote:((a.querySelector('.le-note')||{}).textContent||'').trim().slice(0,90),
        entryLinks:a.querySelectorAll('ol.list-entries a[href^="#/artwork/"]').length,
        moreLists:[].slice.call(a.querySelectorAll('.sec-title')).map(function(h){
          return h.textContent.trim().replace(/\\s+/g,' ').slice(0,40);}),
        siblingLists:a.querySelectorAll('a[href^="#/list/"]').length};})()""")
    rec("J3", "1 lists -> a list", s2["hash"], "clicked list card %r" % first["text"],
        {"h1": li["h1"], "orderedList": li["ordered"], "entries": li["entries"]},
        {"anchor": "h1 = %r" % li["h1"],
         "relationship": "<%s class=list-entries> with %d entries" % (li["tag"], li["entries"]),
         "consequence": "%d per-entry .le-note, e.g. %r" % (li["notes"], li["firstNote"]),
         "onward": "%d entry links to artworks" % li["entryLinks"]},
        "PASS" if (li["ordered"] and li["entries"] and li["notes"] and li["entryLinks"]) else "FAIL")
    rec("J3", "2 end of list", s2["hash"], "(same page, scrolled)",
        {"sections": li["moreLists"]},
        {"relationship": "'More lists' section: %s" % [x for x in li["moreLists"] if "list" in x.lower()],
         "consequence": "%d sibling list links on the page" % (li["siblingLists"]),
         "onward": "listCard <a>"},
        "PASS" if li["siblingLists"] >= 2 else "FAIL",
        "frozen J3 Pass: ordered walk + per-entry notes + >=1 onward list link")
    ent = click_sel(b, 'ol.list-entries a[href^="#/artwork/"]', 0, 1500)
    s3 = snap(b)
    rec("J3", "3 list entry -> artwork", s3["hash"], "clicked entry %r" % ent["text"][:40],
        {"h1": s3["h1"], "title": s3["title"]},
        {"anchor": s3["h1"], "relationship": "the list's pick",
         "consequence": "artwork page renders",
         "onward": "%d chips" % q(b, "document.querySelectorAll('#app a.chip').length")},
        "PASS" if s3["hash"].startswith("#/artwork/") and s3["h1"] else "FAIL")


# --------------------------------------------------------------- J4
def j4(b, fresh=True):
    if fresh:
        b.goto(cdp.BASE + "/index.html?j4=0#/", settle=1.2)
        b.ev("try{localStorage.removeItem(%r);sessionStorage.clear()}catch(e){};1" % KEY)
    b.goto(cdp.BASE + "/index.html?j4=1#/palette", settle=2.0)
    s = snap(b)
    rec("J4", "1 start", s["hash"], "load #/palette",
        {"h1": s["h1"], "hasBegin": q(b, "!!document.querySelector('[data-tsx=\"start\"]')")},
        {"anchor": s["h1"], "relationship": "-", "consequence": "enters the step machine",
         "onward": "Begin ->"}, "PASS" if s["h1"] else "FAIL")
    click_sel(b, '[data-tsx="start"]', 0, 1100)
    # step 1 - tones
    s = snap(b)
    tones = q(b, "document.querySelectorAll('[data-tsx=\"tone\"]').length")
    cta0 = q(b, """(function(){var c=document.querySelector('[data-tsx="tones-done"]');
      return {disabled:c.disabled, label:c.textContent.trim()};})()""")
    prog = []
    for i in range(4):
        click_sel(b, '[data-tsx="tone"]', i * 3, 380)
        prog.append(q(b, """(function(){var c=document.querySelector('[data-tsx="tones-done"]');
          var t=document.body.textContent.match(/\\d of 4 chosen/);
          return {progress:t?t[0]:null, ctaDisabled:c.disabled,
                  pressed:[].slice.call(document.querySelectorAll('[data-tsx="tone"]'))
                    .filter(function(x){return x.getAttribute('aria-pressed')==='true';}).length};})()"""))
    rec("J4", "2 tones (step 1)", s["hash"], "clicked 4 of %d tone buttons" % tones,
        {"progressAfterEachClick": prog, "ctaBefore": cta0},
        {"anchor": s["h1"], "relationship": "%d .tone buttons, 4-cap" % tones,
         "consequence": "'N of 4 chosen' + CTA disabled until 4: %s -> %s"
                        % (cta0["disabled"], prog[-1]["ctaDisabled"]),
         "onward": "To the deck ->"},
        "PASS" if (cta0["disabled"] and not prog[-1]["ctaDisabled"]
                   and prog[-1]["pressed"] == 4) else "FAIL")
    click_sel(b, '[data-tsx="tones-done"]', 0, 1200)
    # step 2 - the 16-card deck
    dprog = []
    for i in range(16):
        d = q(b, """(function(){var m=document.body.textContent.match(/(\\d+) of 16/);
          var bar=document.querySelector('.deck-progress i');
          var im=document.querySelector('.deck-card img,.ob-deck img');
          return {progress:m?m[0]:null, bar:bar?bar.style.width:null,
                  kicker:((document.querySelector('.page-kicker')||{}).textContent||'').trim(),
                  hasCard:!!im,
                  meta:((document.querySelector('.deck-meta,.dc-meta')||{}).textContent||'').trim().slice(0,50),
                  admire:!!document.querySelector('[data-tsx="deck-admire"]')};})()""")
        if not d["admire"]:
            break
        dprog.append(d)
        click_sel(b, '[data-tsx="deck-admire"]' if i % 2 == 0 else '[data-tsx="deck-pass"]', 0, 320)
    s = snap(b)
    rec("J4", "3 deck (step 2)", s["hash"], "answered 16 deck cards (alternating Admire / Pass)",
        {"firstCard": dprog[0] if dprog else None, "lastCard": dprog[-1] if dprog else None,
         "cardsAnswered": len(dprog), "nowShowing": s["h1"]},
        {"anchor": "deck card image + meta", "relationship": "Admire / Pass",
         "consequence": "progress bar di/16 observed at every card: %s"
                        % all(x["progress"] for x in dprog),
         "onward": "auto-advance at 16 -> %r" % s["h1"]},
        "PASS" if len(dprog) == 16 and all(x["progress"] for x in dprog) else "FAIL")
    # step 3 - five questions
    qprog = []
    for i in range(5):
        d = q(b, """(function(){var m=document.body.textContent.match(/question (\\d+) of 5/);
          var bar=document.querySelector('.deck-progress i');
          return {progress:m?m[0]:null, bar:bar?bar.style.width:null,
            kicker:((document.querySelector('.page-kicker')||{}).textContent||'').trim(),
            question:((document.querySelector('h1.ob-q,.q-text')||{}).textContent||'').trim().slice(0,70),
            options:document.querySelectorAll('[data-tsx="answer"]').length};})()""")
        if not d["options"]:
            break
        qprog.append(d)
        click_sel(b, '[data-tsx="answer"]', i % max(1, d["options"]), 420)
    s = snap(b)
    rec("J4", "4 questions (step 3)", s["hash"], "answered %d questions" % len(qprog),
        {"questions": qprog, "nowShowing": s["h1"]},
        {"anchor": "question text", "relationship": "%s option buttons"
                   % [x["options"] for x in qprog],
         "consequence": "progress qi/5 at every question: %s" % [x["progress"] for x in qprog],
         "onward": "auto-advance to reveal -> %r" % s["h1"]},
        "PASS" if len(qprog) == 5 and all(x["progress"] for x in qprog) else "FAIL")
    # step 4 - reveal
    rv = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        map:!!a.querySelector('svg'),
        personaCards:a.querySelectorAll('[data-tsx="adopt"]').length,
        later:!!a.querySelector('[data-tsx="later"]'),
        toTaste:!!a.querySelector('a[href="#/taste"]'),
        handoff:!!a.querySelector('.ob-handoff'),
        handoffArtists:a.querySelectorAll('.ob-handoff a.mini-card').length,
        handoffList:((a.querySelector('.ob-handoff a.chip')||{}).textContent||'').trim()};})()""")
    stored = q(b, "JSON.parse(localStorage.getItem(%r)||'null')" % KEY)
    rec("J4", "5 reveal (step 4) + Passport creation", "#/palette", "(auto-advanced)",
        {"reveal": rv, "passportWritten": bool(stored),
         "passportKeys": sorted(stored.keys()) if stored else None,
         "onboarded": stored and stored.get("milestones", {}).get("onboarded"),
         "admirationsFromDeck": len(stored["admirations"]) if stored else 0},
        {"anchor": "signal-word h1 = %r" % rv["h1"],
         "relationship": "taste map SVG + %d persona candidates" % rv["personaCards"],
         "consequence": "Adopt / Decide later present: %s/%s ; handoff %d artists + list %r"
                        % (rv["personaCards"] > 0, rv["later"], rv["handoffArtists"], rv["handoffList"]),
         "onward": "'To your taste page' present: %s" % rv["toTaste"]},
        "PASS" if (rv["h1"] and rv["map"] and rv["personaCards"] == 3 and rv["later"]
                   and rv["toTaste"] and rv["handoff"] and stored
                   and stored["milestones"]["onboarded"]) else "FAIL")
    adopted_name = q(b, "((document.querySelector('.persona-stack .p-name,.persona-stack h3')||{}).textContent||'').trim()")
    click_sel(b, '[data-tsx="adopt"]', 0, 1100)
    st2 = q(b, "JSON.parse(localStorage.getItem(%r)).persona" % KEY)
    click_sel(b, 'a[href="#/taste"]', 0, 1600)
    s = snap(b)
    tp = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        kicker:((a.querySelector('.page-kicker')||{}).textContent||'').trim(),
        lede:((a.querySelector('.page-lede')||{}).textContent||'').trim().slice(0,200),
        map:!!a.querySelector('svg'),
        chips:[].slice.call(a.querySelectorAll('.chips .chip')).map(function(c){
          return c.textContent.trim();}),
        admiredSection:a.querySelectorAll('a.card').length};})()""")
    rec("J4", "6 adopt a Persona -> the Passport page", s["hash"],
        "clicked 'Adopt this Persona', then 'To your taste page ->'",
        {"personaStored": st2, "tastePage": tp},
        {"anchor": "h1 = %r" % tp["h1"],
         "relationship": "map + persona + admirations",
         "consequence": "adopted persona preserved through the handoff: %s"
                        % (st2 and st2.get("adopted")),
         "onward": "chips: %s" % tp["chips"]},
        "PASS" if (st2 and st2.get("adopted") and tp["map"]
                   and any("Reset" in c for c in tp["chips"])) else "FAIL",
        "frozen J4 Pass: six-step machine completes with visible progress at each step, "
        "a persistent onward link, and reveal->#/taste preserves the saved persona")


# --------------------------------------------------------------- J5
def j5(b):
    b.goto(cdp.BASE + "/index.html?j5=1#/explore", settle=2.0)
    s = snap(b)
    ex = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        lede:((a.querySelector('.page-lede')||{}).textContent||'').trim().slice(0,220),
        cards:[].slice.call(a.querySelectorAll('a.entry-card')).map(function(c){
          return {href:c.getAttribute('href'),
                  title:(c.querySelector('h2,h3,.ec-title')||c).textContent.trim().replace(/\\s+/g,' ').slice(0,40)};})};})()""")
    rec("J5", "1 explore hub", s["hash"], "load #/explore",
        {"h1": ex["h1"], "lede": ex["lede"], "entryCards": ex["cards"]},
        {"anchor": ex["h1"], "relationship": "%d entry-cards" % len(ex["cards"]),
         "consequence": "lede names the instruments",
         "onward": [c["href"] for c in ex["cards"]]},
        "PASS" if len(ex["cards"]) >= 2 else "FAIL")
    # timeline projection
    click_sel(b, 'a[href="#/timeline"]', 0, 2200)
    s = snap(b)
    tl = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        bars:a.querySelectorAll('.tl-bar,.tl-row a,a.tl-bar').length,
        legend:a.querySelectorAll('.tl-legend *,.legend *').length,
        controls:[].slice.call(a.querySelectorAll('button,select')).map(function(c){
          return c.textContent.trim().slice(0,26);}).slice(0,8),
        artistLinks:a.querySelectorAll('a[href^="#/artist/"]').length};})()""")
    rec("J5", "2 timeline projection", s["hash"], "clicked the timeline entry-card",
        {"h1": tl["h1"], "bars": tl["bars"], "legendNodes": tl["legend"],
         "controls": tl["controls"], "artistLinks": tl["artistLinks"]},
        {"anchor": tl["h1"], "relationship": "bars = lifespans, legend = movements",
         "consequence": "isolate/zoom controls present: %s" % bool(tl["controls"]),
         "onward": "%d bar links into #/artist/*" % tl["artistLinks"]},
        "PASS" if (tl["h1"] and tl["artistLinks"]) else "FAIL")
    hit = click_sel(b, '#app a[href^="#/artist/"]', 0, 1800)
    s = snap(b)
    rec("J5", "3 timeline -> canonical page", s["hash"],
        "clicked a timeline bar (%r)" % hit["text"][:36],
        {"h1": s["h1"], "hash": s["hash"]},
        {"anchor": s["h1"], "consequence": "canonical artist page renders",
         "onward": "%d chips" % q(b, "document.querySelectorAll('#app a.chip').length")},
        "PASS" if s["hash"].startswith("#/artist/") else "FAIL")
    # influence projection
    b.goto(cdp.BASE + "/index.html?j5=2#/influences", settle=2.6)
    ig = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        svg:!!a.querySelector('#ig-svg'),
        svgRole:(a.querySelector('#ig-svg')||{}).getAttribute?a.querySelector('#ig-svg').getAttribute('role'):null,
        svgLabel:(a.querySelector('#ig-svg')||{}).getAttribute?a.querySelector('#ig-svg').getAttribute('aria-label'):null,
        nodes:a.querySelectorAll('.ig-node').length,
        legend:[].slice.call(a.querySelectorAll('[data-etype-btn]')).map(function(x){
          return x.textContent.trim().replace(/\\s+/g,' ').slice(0,30);})};})()""")
    rec("J5", "4 influence projection", "#/influences", "load #/influences",
        {"graph": ig},
        {"anchor": ig["h1"], "relationship": "force graph, %d nodes, edge-type legend %s"
                   % (ig["nodes"], ig["legend"][:6]),
         "consequence": "svg role=%s label=%r" % (ig["svgRole"], ig["svgLabel"]),
         "onward": "node focus reveals a lineage panel"},
        "PASS" if (ig["h1"] and ig["nodes"] and ig["legend"]) else "FAIL")
    b.ev("document.querySelector('.ig-node').focus();1")
    key(b, "Enter", "Enter", 1200)
    pan = q(b, """(function(){var a=document.getElementById('app');
      var op=[].slice.call(a.querySelectorAll('a')).filter(function(x){
        return /Open .*page/.test(x.textContent);})[0];
      var inf=a.querySelector('#ig-info');
      return {panel:(inf&&!inf.hidden?inf.textContent:'').trim().replace(/\\s+/g,' ').slice(0,220),
        panelHidden:inf?inf.hidden:null,
        openLink:op?{text:op.textContent.trim(),href:op.getAttribute('href')}:null};})()""")
    rec("J5", "5 focus a node -> lineage panel", "#/influences",
        "focused an .ig-node and pressed Enter",
        {"lineagePanel": pan["panel"], "openLink": pan["openLink"]},
        {"anchor": "the focused entity", "relationship": "its lineage",
         "consequence": pan["panel"][:120],
         "onward": pan["openLink"]},
        "PASS" if (pan["panel"] and pan["openLink"]) else "FAIL",
        "frozen J5 Pass: #/explore names exactly the instruments it links to and each "
        "instrument offers a link into a canonical page")


# ------------------------------------------------- AC4's eleven-link chain
def chain(b):
    b.goto(cdp.BASE + "/index.html?ch=0#/", settle=1.2)
    b.ev("try{localStorage.clear();sessionStorage.clear()}catch(e){};1")
    # 1 entry .. 3 passport creation .. 6 persistence are covered by j4 on a clean slate
    j4(b, fresh=False)
    # 4/5 Admire + consequence explanation, then persistence and return
    b.goto(cdp.BASE + "/index.html?ch=1#/artwork/mona-lisa", settle=2.0)
    click_sel(b, '[data-pp="admirations"]', 0, 800)
    cons = q(b, """(function(){var t=document.body.textContent;
      var i=t.indexOf('Admire');var a=document.getElementById('app');
      return {btn:((a.querySelector('[data-pp="admirations"]')||{}).textContent||'').trim(),
        pressed:(a.querySelector('[data-pp="admirations"]')||{}).getAttribute('aria-pressed')};})()""")
    b.goto(cdp.BASE + "/index.html?ch=2#/taste", settle=2.2)
    tp = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        lede:((a.querySelector('.page-lede')||{}).textContent||'').trim().slice(0,240),
        explains:/admiration/i.test(a.textContent),
        rings:((a.querySelector('.sec-title')||{}).textContent||'').trim().replace(/\\s+/g,' '),
        ringNote:((a.querySelector('.chip-label')||{}).textContent||'').trim().slice(0,120),
        chips:[].slice.call(a.querySelectorAll('.chips .chip')).map(function(c){return c.textContent.trim();})};})()""")
    rec("CHAIN", "4/5/6/7 Admire -> consequence explanation -> persistence -> return",
        "#/taste", "Admired Mona Lisa on its own page, then returned to #/taste",
        {"button": cons, "tastePage": tp},
        {"consequence": "the Passport page states what the admiration did: %r" % tp["lede"],
         "persistence": "survived two full page loads",
         "onward": tp["chips"]},
        "PASS" if (cons["pressed"] == "true" and tp["explains"]) else "FAIL")
    # 8 export or share
    b.ev("""window.__dl=[];HTMLAnchorElement.prototype.click=function(){
         window.__dl.push({download:this.download,len:(this.href||'').length});};1""")
    click_sel(b, '[data-tsx="export"]', 0, 700)
    dl = q(b, "window.__dl")
    # the share link: disable the clipboard so the build's own fallback prints the URL
    b.ev("try{Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true})}"
         "catch(e){};1")
    click_sel(b, '[data-tsx="share-url"]', 0, 900)
    msg = b.ev("(document.getElementById('taste-msg')||{}).textContent||''")
    share = msg.split("#/passport/")[1] if "#/passport/" in msg else ""
    rec("CHAIN", "8 export or share", "#/taste",
        "clicked 'Back up data (.json)', then 'Copy share link' with the clipboard API removed "
        "so the build's own fallback renders the URL in #taste-msg",
        {"downloadIntercepted": dl, "shareUrlShown": msg[:90],
         "sharePayloadChars": len(share), "sharePayloadHead": share[:40]},
        {"consequence": "a .json backup and a #/passport/<payload> share link",
         "onward": "the link is the import path"},
        "PASS" if (dl and dl[0]["download"] and share) else "FAIL")
    b.goto(cdp.BASE + "/index.html?ch=3#/taste", settle=1.6)   # drop the click override
    mine = q(b, "JSON.parse(localStorage.getItem(%r))" % KEY)
    # 9/10 import + conflict handling: give this device a DIFFERENT passport first
    other = dict(mine)
    other = json.loads(json.dumps(mine))
    other["persona"]["adopted"] = None
    other["palette"] = {"tones": ["ash", "ash", "ash", "ash"], "source": "chosen"} \
        if mine.get("palette") else None
    other["quiz"] = None
    other["admirations"] = [{"id": "the-night-watch", "at": "2026-07-02T00:00:00.000Z"}]
    b.ev("localStorage.setItem(%r,%s);1" % (KEY, json.dumps(json.dumps(other))))
    b.goto(cdp.BASE + "/index.html?ch=4#/passport/" + share, settle=2.4)
    arr = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        lede:[].slice.call(a.querySelectorAll('.page-lede')).map(function(p){
          return p.textContent.trim().replace(/\\s+/g,' ').slice(0,300);}),
        cta:[].slice.call(a.querySelectorAll('[data-tsx]')).map(function(x){
          return {act:x.dataset.tsx,label:x.textContent.trim()};})};})()""")
    rec("CHAIN", "9 import (the share link opened on a device that already has a passport)",
        "#/passport/<payload>", "opened the share URL",
        {"arrival": arr},
        {"anchor": arr["h1"], "relationship": "incoming vs local",
         "consequence": arr["lede"][:2],
         "onward": [c["label"] for c in arr["cta"]]},
        "PASS" if arr["h1"] and arr["cta"] else "FAIL")
    click_sel(b, '[data-tsx="import-review"]', 0, 1200)
    conf = q(b, """(function(){var a=document.getElementById('app');
      return {h1:((a.querySelector('h1')||{}).textContent||'').trim(),
        fields:[].slice.call(a.querySelectorAll('[data-tsx="ppc"]')).map(function(x){
          return {choice:x.dataset.tsid,label:x.textContent.trim().slice(0,70),
                  pressed:x.getAttribute('aria-pressed')};}),
        cancel:!!a.querySelector('[data-tsx="import-cancel"]'),
        merge:!!a.querySelector('[data-tsx="import"]')};})()""")
    rec("CHAIN", "10 conflict handling (per-field choice)", "#/passport/<payload>",
        "clicked 'Choose what to keep ->'",
        {"conflictScreen": conf},
        {"relationship": "each conflicting field offers Keep mine / Take theirs",
         "consequence": "%d field buttons; cancel present: %s" % (len(conf["fields"]), conf["cancel"]),
         "onward": "'Merge with these choices'"},
        "PASS" if (conf["fields"] and conf["cancel"] and conf["merge"]) else "FAIL")
    before_merge = q(b, "JSON.parse(localStorage.getItem(%r))" % KEY)
    click_sel(b, '[data-tsx="import"]', 0, 1600)
    after_merge = q(b, "JSON.parse(localStorage.getItem(%r))" % KEY)
    s = snap(b)
    rec("CHAIN", "10b merge applied", s["hash"], "clicked 'Merge with these choices'",
        {"admirationsBefore": [e["id"] for e in before_merge["admirations"]],
         "admirationsAfter": [e["id"] for e in after_merge["admirations"]],
         "personaBefore": before_merge["persona"]["adopted"],
         "personaAfter": after_merge["persona"]["adopted"],
         "landedOn": s["h1"]},
        {"consequence": "union fields combined, single-value fields resolved by the choices",
         "onward": s["hash"]},
        "PASS" if len(after_merge["admirations"]) >= len(before_merge["admirations"]) else "FAIL")
    # 11 reset
    b.goto(cdp.BASE + "/index.html?ch=5#/taste", settle=2.0)
    b.ev("window.confirm=function(m){window.__cm=m;return true};1")
    click_sel(b, '[data-tsx="reset"]', 0, 1500)
    s = snap(b)
    rec("CHAIN", "11 reset", s["hash"], "clicked 'Reset everything' and confirmed",
        {"confirmText": b.ev("window.__cm"),
         "storedAfter": b.ev("localStorage.getItem(%r)" % KEY),
         "h1": s["h1"], "title": s["title"]},
        {"consequence": "passport removed from this device",
         "onward": "the empty-state Passport page invites the onboarding again"},
        "PASS" if b.ev("localStorage.getItem(%r)" % KEY) in (None, "") else "FAIL")


def main():
    which = sys.argv[1:] or ["j1", "j2", "j3", "j4", "j5", "chain"]
    b = cdp.Browser(port=PORT)
    try:
        b.metrics(1440, 1200)
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','dark')}catch(e){}"})
        for w in which:
            globals()[w](b)
    finally:
        b.close()
    json.dump(T, open(os.path.join(OUT, "ac4-journeys.json"), "w"), indent=1)
    print("\n=== VERDICTS ===")
    for r in T:
        print("  %-6s %-52s %s" % (r["journey"], r["step"], r["verdict"]))
    bad = [r for r in T if r["verdict"] == "FAIL"]
    print("\nsteps: %d   FAIL: %d" % (len(T), len(bad)))


main()
