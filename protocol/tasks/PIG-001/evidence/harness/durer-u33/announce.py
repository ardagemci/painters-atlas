"""AT-1 / AT-3 / AT-4 / AT-5 / AT-6 / AT-7 — what an assistive technology would
have to read, verified in the DOM at the moment it would be read.

This CANNOT confirm an announcement. Nothing driven by CDP can: a live region is
a promise to a screen reader, and only a screen reader can say whether the
promise was kept. What it CAN establish, and what is checked here, is that at
the instant the announcement is due:

  * the live region exists, is persistent across route changes, and holds the
    correct text;
  * the accessible name of the card and of each control names the artwork;
  * the search field exposes exactly one role and one popup declaration;
  * no decorative arrow is left exposed to the accessibility tree.

Everything below is a DOM fact. Ear-confirmation is outstanding and is recorded
as outstanding in the unit 33 build log.

usage: python3 announce.py <theme> <w> <h>
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402

OK, BAD = [], []


def check(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %-4s %-46s %s" % ("PASS" if cond else "FAIL", name, detail))


def settle(b, ms=420):
    b.ev("new Promise(function(r){setTimeout(r,%d)})" % ms, await_promise=True)


def live(b):
    return b.ev("(function(){var e=document.getElementById('live-status');"
                "return e?e.textContent:null;})()")


def click_tsx(b, act):
    return b.ev("(function(a){var e=document.querySelector('[data-tsx=\"'+a+'\"]');"
                "if(!e)return false;e.click();return true;})(%s)" % json.dumps(act))


def run(theme, vw, vh):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9481")))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s');"
                         "localStorage.removeItem('pigment.taste.v1');"
                         "sessionStorage.removeItem('pigment.onboarding.v1')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)

        # ---------------------------------------------------------- the channel
        print("\nthe live region (index.html, outside #app)")
        b.goto(cdp.BASE + "/index.html#/", settle=2.0)
        reg = json.loads(b.ev(
            "(function(){var e=document.getElementById('live-status');"
            "if(!e)return JSON.stringify({missing:true});"
            "return JSON.stringify({role:e.getAttribute('role'),"
            "live:e.getAttribute('aria-live'),atomic:e.getAttribute('aria-atomic'),"
            "inApp:!!document.getElementById('app').contains(e),"
            "text:e.textContent});})()"))
        check("live region present", not reg.get("missing"), str(reg))
        check("role=status, aria-live=polite, atomic",
              reg.get("role") == "status" and reg.get("live") == "polite"
              and reg.get("atomic") == "true")
        check("outside #app, so route() cannot destroy it", reg.get("inApp") is False)
        check("silent at rest — route() does not write here", reg.get("text") == "")
        b.ev("location.hash='#/artists'")
        settle(b, 900)
        check("still silent after a route change (C-8 not re-created)", live(b) == "")

        # ------------------------------------------------------------ AT-4 roles
        print("\nAT-4 — one coherent role on the search field")
        b.goto(cdp.BASE + "/index.html#/", settle=1.8)
        at = json.loads(b.ev(
            "(function(){var e=document.getElementById('search');"
            "return JSON.stringify({role:e.getAttribute('role'),"
            "haspopup:e.getAttribute('aria-haspopup'),"
            "autocomplete:e.getAttribute('aria-autocomplete'),"
            "expanded:e.getAttribute('aria-expanded'),"
            "controls:e.getAttribute('aria-controls')});})()"))
        check("aria-haspopup removed (the source of two of three roles)",
              at.get("haspopup") is None, str(at))
        check("role=combobox retained", at.get("role") == "combobox")
        check("aria-autocomplete/expanded/controls retained",
              at.get("autocomplete") == "list" and at.get("expanded") == "false"
              and at.get("controls") == "search-results")

        # ------------------------------------------------------------ AT-3 search
        print("\nAT-3 — dismissing search says so")
        b.ev("(function(){var i=document.getElementById('search');i.focus();"
             "i.value='van';i.dispatchEvent(new Event('input',{bubbles:true}));"
             "return true;})()")
        settle(b)
        check("panel open before Escape",
              b.ev("!document.getElementById('search-results').hidden"))
        b.ev("(function(){var i=document.getElementById('search');"
             "i.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));"
             "return true;})()")
        settle(b)
        txt = live(b)
        check("panel closed", b.ev("document.getElementById('search-results').hidden"))
        check("dismissal announced", bool(txt) and "closed" in (txt or ""), repr(txt))
        check("focus returned to the field",
              b.ev("document.activeElement&&document.activeElement.id") == "search")
        # and it must stay silent when there was nothing open
        b.ev("(function(){var e=document.getElementById('live-status');e.textContent='';"
             "var i=document.getElementById('search');i.value='';"
             "i.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));"
             "return true;})()")
        settle(b)
        check("Escape on a closed panel stays silent", live(b) == "", repr(live(b)))

        # -------------------------------------------------------------- AT-1 deck
        print("\nAT-1 — the deck names the artwork being judged")
        b.goto(cdp.BASE + "/index.html#/palette", settle=1.8)
        click_tsx(b, "start")
        settle(b)
        # each tap re-renders, so the NodeList is stale after the first click
        for k in range(4):
            b.ev("(function(k){var t=document.querySelectorAll('.tone')[k];"
                 "if(t)t.click();return true;})(%d)" % k)
            settle(b, 260)
        click_tsx(b, "tones-done")
        settle(b, 800)
        card = json.loads(b.ev(
            "(function(){var c=document.querySelector('.deck-card');"
            "if(!c)return JSON.stringify({missing:true});"
            "var t=document.querySelector('.deck-meta b').textContent;"
            "return JSON.stringify({role:c.getAttribute('role'),"
            "label:c.getAttribute('aria-label'),"
            "alt:c.querySelector('img').getAttribute('alt'),"
            "admire:document.querySelector('.deck-admire').getAttribute('aria-label'),"
            "pass:document.querySelector('.deck-pass').getAttribute('aria-label'),"
            "title:t});})()"))
        check("card is a labelled group", card.get("role") == "group")
        check("card name carries title, artist and position",
              card.get("label", "").startswith("Artwork 1 of 16")
              and card.get("title", "") in card.get("label", ""),
              card.get("label"))
        check("image alt names artist, not only title",
              card.get("title", "") in card.get("alt", "") and "—" in card.get("alt", ""),
              card.get("alt"))
        check("Admire names its object",
              bool(card.get("admire")) and card.get("title", "x") in card["admire"],
              card.get("admire"))
        check("Pass names its object",
              bool(card.get("pass")) and card.get("title", "x") in card["pass"],
              card.get("pass"))
        check("card 1 announced on entering the deck",
              "1 of 16" in (live(b) or ""), repr(live(b)))
        first = card.get("title")
        # advance one card — the button keeps focus, so only the live region can say
        # focus first: element.click() alone does not move focus, and the whole
        # point of AT-1 is that the REAL interaction leaves focus on the button
        b.ev("(function(){var e=document.querySelector('.deck-admire');"
             "e.focus();e.click();return true;})()")
        settle(b, 700)
        second = b.ev("document.querySelector('.deck-meta b').textContent")
        spoken = live(b)
        check("focus stayed on the pressed control (nothing else would speak)",
              b.ev("!!(document.activeElement&&document.activeElement.dataset&&"
                   "document.activeElement.dataset.tsx)"),
              b.ev("document.activeElement&&document.activeElement.className"))
        check("the NEW artwork is announced after a tap",
              bool(spoken) and second in (spoken or "") and "2 of 16" in (spoken or ""),
              repr(spoken))
        check("the announcement changed with the card", first != second)

        # ---------------------------------------------- AT-6 / AT-7 passport import
        # Two real passports differing on all four non-mergeable fields, exactly
        # the fixture the owner's second VoiceOver session used.
        print("\nAT-6 / AT-7 — cancelling, and the merge outcome")
        MINE = {"version": 1, "createdAt": "2026-07-01T00:00:00.000Z",
                "updatedAt": "2026-07-01T00:00:00.000Z",
                "admirations": [{"id": "david", "at": "2026-07-01T00:00:00.000Z"}],
                "notForMe": [], "seen": [], "wantToSee": [], "saved": [], "probes": [],
                "skipped": [], "deckSeen": [],
                "quiz": {"answers": {"q1": "a"}, "at": "2026-07-01"},
                "palette": {"tones": ["ochre", "indigo"]},
                "persona": {"adopted": "the-colourist", "adoptedAt": "2026-07-01",
                            "candidates": [], "hidden": False},
                "tasteVector": None,
                "milestones": {"onboarded": True, "confidence": "sketch"}}
        THEIRS = json.loads(json.dumps(MINE))
        THEIRS["admirations"] = [{"id": "the-kiss", "at": "2026-07-02T00:00:00.000Z"},
                                 {"id": "guernica", "at": "2026-07-02T00:00:00.000Z"}]
        THEIRS["quiz"] = {"answers": {"q1": "b", "q2": "c"}, "at": "2026-07-02"}
        THEIRS["palette"] = {"tones": ["vermilion", "bone"]}
        THEIRS["persona"] = {"adopted": "the-realist", "adoptedAt": "2026-07-02",
                             "candidates": [], "hidden": False}
        THEIRS["milestones"] = {"onboarded": True, "confidence": "map"}

        def seed_and_open():
            b.cmd("Page.addScriptToEvaluateOnNewDocument",
                  {"source": "try{localStorage.setItem('pigment-theme','%s');"
                             "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                             % (theme, json.dumps(json.dumps(MINE)))})
            # a query string, not a bare fragment: navigating between two hashes of
            # the same document is a same-document navigation and would not re-run
            # the seeding script
            b.goto(cdp.BASE + "/index.html?u33seed=%d#/" % int(time.time() * 1000),
                   settle=2.0)
            assert b.ev("!!localStorage.getItem('pigment.taste.v1')"), "seed did not land"
            payload = b.ev("(function(p){return btoa(unescape(encodeURIComponent(p)))"
                           ".replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');})(%s)"
                           % json.dumps(json.dumps(THEIRS)))
            b.ev("location.hash='#/passport/' + %s" % json.dumps(payload))
            settle(b, 900)
            return payload

        seed_and_open()
        check("import arrival screen reached",
              b.ev("!!document.querySelector('[data-tsx=\"import-review\"]')"))
        click_tsx(b, "import-review")
        settle(b, 700)
        check("per-field conflict screen reached, 4 choices",
              b.ev("document.querySelectorAll('.pp-conflicts .panel').length") == 4)
        before = b.ev("localStorage.getItem('pigment.taste.v1')")
        click_tsx(b, "import-cancel")
        settle(b, 1000)
        spoken = live(b)
        after = b.ev("localStorage.getItem('pigment.taste.v1')")
        check("cancel is still byte-identical (the fix changed nothing functional)",
              before == after)
        check("cancel relocates to the home page",
              b.ev("location.hash") in ("#/", ""), b.ev("location.hash"))
        check("cancel says nothing was changed",
              "Nothing on this device has been changed." in (spoken or ""), repr(spoken))

        # now the merge, with a mixed decision: keep mine on two, take theirs on two
        seed_and_open()
        click_tsx(b, "import-review")
        settle(b, 700)
        for fld, which in (("quiz", "theirs"), ("palette", "mine"),
                           ("persona", "theirs"), ("milestones", "mine")):
            b.ev("(function(id){var e=document.querySelector('[data-tsid=\"'+id+'\"]');"
                 "if(e)e.click();return true;})(%s)" % json.dumps(fld + ":" + which))
            settle(b, 260)
        click_tsx(b, "import")
        settle(b, 1200)
        spoken = live(b)
        onpage = b.ev("(function(){var e=document.getElementById('taste-msg');"
                      "return e?e.textContent:null;})()")
        stored = json.loads(b.ev("localStorage.getItem('pigment.taste.v1')"))
        check("merge lands on the taste page", b.ev("location.hash") == "#/taste")
        check("outcome announced", bool(spoken) and "merged" in (spoken or "").lower(),
              repr(spoken))
        check("outcome names every field that was decided",
              all(k in (spoken or "") for k in
                  ("Onboarding answers", "Chosen tones", "Adopted Persona",
                   "Progress markers")), repr(spoken))
        check("outcome reports theirs taken where theirs was chosen",
              "Adopted Persona: theirs taken" in (spoken or ""))
        check("outcome reports yours kept where yours was chosen",
              "Chosen tones: yours kept" in (spoken or ""))
        check("outcome is on the page as well, not only announced",
              onpage == spoken, repr(onpage))
        check("the announcement matches what was actually stored — persona",
              stored["persona"]["adopted"] == "the-realist",
              stored["persona"]["adopted"])
        check("the announcement matches what was actually stored — tones",
              stored["palette"]["tones"] == ["ochre", "indigo"],
              str(stored["palette"]["tones"]))

        # -------------------------------------------------------------- AT-5 arrows
        print("\nAT-5 — decorative arrows are not exposed")
        bare = b.ev(
            "(function(){var n=0;[].forEach.call(document.querySelectorAll('#app *'),"
            "function(e){[].forEach.call(e.childNodes,function(c){"
            "if(c.nodeType===3&&/[\\u2190\\u2192]/.test(c.nodeValue)&&"
            "e.getAttribute('aria-hidden')!=='true')n++;});});return n;})()")
        check("no arrow left in exposed text on #/palette", bare == 0, "bare arrows: %s" % bare)
        b.goto(cdp.BASE + "/index.html#/explore", settle=1.8)
        bare = b.ev(
            "(function(){var n=[];[].forEach.call(document.querySelectorAll('#app *'),"
            "function(e){[].forEach.call(e.childNodes,function(c){"
            "if(c.nodeType===3&&/[\\u2190\\u2192]/.test(c.nodeValue)&&"
            "e.getAttribute('aria-hidden')!=='true')n.push(c.nodeValue.trim().slice(0,30));});});"
            "return JSON.stringify(n);})()")
        check("no arrow left in exposed text on #/explore", bare == "[]", bare)
    finally:
        b.close()
    print("\n%d checks pass, %d fail" % (len(OK), len(BAD)))
    if BAD:
        print("FAILING: " + ", ".join(BAD))
    return not BAD


if __name__ == "__main__":
    ok = run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    sys.exit(0 if ok else 1)
