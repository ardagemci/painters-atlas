#!/usr/bin/env python3
"""Fetch public-domain artwork images from Wikipedia/Wikimedia Commons.

Reads /tmp/pigment-artists.json (from tools/dump-artists.jxa.js), resolves each
listed work of every painter who died in or before 1955 to an image, and writes
js/artworks.js. Only images hosted on Wikimedia Commons are accepted, because
Commons' own upload policy requires a free-licence or public-domain basis to be
*asserted* for the US and the source country. That is a hosting policy and an
assertion by an uploader — not a determination by Commons, and not one by this
project. Nothing in this file reaches a legal conclusion (OD-5, AC12).
"""
import json, os, re, sys, time, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commons_rights as cr

# Rights metadata captured opportunistically while resolving images. Asking
# Commons for extmetadata costs one query parameter and zero extra requests,
# so there is no reason to keep throwing it away — see tools/rights_register.py
# for the register built on top of it. Nothing here reaches a legal conclusion.
RIGHTS = {}

CUTOFF = 1955
UA = {"User-Agent": "PigmentAtlas/1.0 (personal static art atlas; gemciarda@gmail.com)"}

# artist-id::work-title -> why no image may be resolved for this work.
#
# The CUTOFF above is a *heuristic for which artists to try*, not a rights
# determination (AC28/OD-5: no legal conclusion follows from a death year).
# Where an artist clears the cutoff but the individual works are still in
# copyright, Commons holds no image of the work — and the resolvers below,
# which accept the best *search hit*, will happily return something else that
# merely shares a word with the title. That is how Kahlo's "The Broken Column"
# became a photograph of a broken column in Syracuse (CC BY 2.0), and "The Two
# Fridas" a photograph of a park sculpture (CC BY-SA 4.0) — wrong artworks
# carrying attribution obligations Pigment honours nowhere.
#
# Suppressed works render as a plain title row in "Major works" (js/app.js),
# which is the honest outcome: no image, no generative cover posing as one.
# Remove an entry only for a file that passes the exact-work check AND whose
# Commons metadata asserts a public-domain basis. Neither test is a clearance.
#
# Language note (unit 35, 2026-08-05, D-019): the reasons below previously read
# "works still in copyright" and "No PD image exists on Commons" — a legal   # OD5-EXEMPT
# conclusion and an exhaustive-absence claim, both beyond this project's
# evidence. They are restated as what was actually observed. OD-5 / AC12.
SUPPRESS = {
    "frida-kahlo::The Two Fridas":
        "Kahlo d.1954; Mexico's term runs life+100, so no PD basis is assertable on the "
        "ordinary term arithmetic. This audit's Commons searches (2026-07-25, logged in "
        "evidence/rights-register.md) located no candidate passing the exact-work check.",
    "frida-kahlo::Self-Portrait with Thorn Necklace and Hummingbird":
        "Kahlo d.1954; same term arithmetic. Resolver previously returned a Ducreux "
        "self-portrait — a confirmed wrong-artwork match, not a rights finding.",
    "frida-kahlo::The Broken Column":
        "Kahlo d.1954; same term arithmetic. Resolver previously returned a CC BY 2.0 "
        "photograph of a column in Syracuse — a confirmed wrong-artwork match.",
}
ART_WORDS = ("painting", "painted", "fresco", "triptych", "altarpiece", "portrait",
             "mural", "woodblock", "print", "icon", "panel", "canvas", "miniature",
             "screens", "scroll", "watercolour", "watercolor", "drawing", "series")

def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def wiki_summary(title):
    q = urllib.parse.quote(title.replace(" ", "_"), safe="()_,%C3%A0-")
    try:
        return get_json("https://en.wikipedia.org/api/rest_v1/page/summary/" + q)
    except Exception:
        return None

def from_wikipedia(candidates, surname):
    for cand in candidates:
        s = wiki_summary(cand)
        time.sleep(0.06)
        if not s or s.get("type") != "standard":
            continue
        thumb = (s.get("thumbnail") or {}).get("source", "")
        if "/wikipedia/commons/" not in thumb:
            continue                                   # fair-use or missing -> reject
        text = ((s.get("description") or "") + " " + (s.get("extract") or "")).lower()
        if surname.lower() not in text and not any(w in text for w in ART_WORDS):
            continue                                   # probably not an artwork page
        img = re.sub(r"/\d+px-", "/500px-", thumb)     # 500 is an allowed thumb bucket
        page = ((s.get("content_urls") or {}).get("desktop") or {}).get("page", "")
        return {"img": img, "page": page}
    return None

def from_commons(query):
    u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
         "&generator=search&gsrnamespace=6&gsrlimit=6"
         "&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=500"
         "&gsrsearch=" + urllib.parse.quote(query))
    try:
        d = get_json(u)
    except Exception:
        return None                                    # transient: unresolved, not absent
    pages = (d.get("query") or {}).get("pages") or {}
    for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        u = ii.get("thumburl", "")
        if ii.get("mime", "").startswith("image/") and u and ".djvu" not in u.lower() and ".pdf" not in u.lower():
            cr.capture_from_imageinfo(RIGHTS, p)
            return {"img": u, "page": ii.get("descriptionurl", "")}
    return None

def candidates_for(title, surname):
    base = title.strip()
    noparen = re.sub(r"\s*\(.*?\)", "", base).strip()
    cands = [base]
    if noparen != base: cands.append(noparen)
    if noparen.endswith(" series"): cands.append(noparen[:-7])
    cands += [f"{noparen} ({surname})", f"{noparen} (painting)"]
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c); out.append(c)
    return out

def main():
    artists = json.load(open("/tmp/pigment-artists.json"))
    result, hits, misses = {}, 0, []
    todo = [a for a in artists if a["died"] and a["died"] <= CUTOFF]
    for i, a in enumerate(artists_iter := todo):
        surname = a["name"].split()[-1]
        found = {}
        for t in a["works"]:
            key = "%s::%s" % (a["id"], t)
            if key in SUPPRESS:
                print("  SUPPRESSED %s — %s" % (key, SUPPRESS[key]), flush=True)
                continue
            art = from_wikipedia(candidates_for(t, surname), surname)
            if not art:
                clean = re.sub(r"\s*\(.*?\)", "", t).strip()
                art = from_commons(f"{clean} {a['name']}")
                time.sleep(0.06)
            if art:
                found[t] = art; hits += 1
            else:
                misses.append(f"{a['id']} :: {t}")
        if found:
            result[a["id"]] = found
        print(f"[{i+1}/{len(todo)}] {a['id']}: {len(found)}/{len(a['works'])}", flush=True)
    with open("js/artworks.js", "w") as f:
        f.write("/* PIGMENT - public-domain artwork images, resolved at build time.\n")
        f.write("   All URLs are hosted on Wikimedia Commons (PD in US + source country per Commons policy).\n")
        f.write("   Regenerate: osascript -l JavaScript tools/dump-artists.jxa.js > /tmp/pigment-artists.json\n")
        f.write("               python3 tools/fetch_artworks.py */\n")
        f.write("window.ARTWORKS = ")
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    if RIGHTS:
        total = cr.save_sidecar(RIGHTS)
        print(f"rights captured this run: {len(RIGHTS)} (cache now {total}) -> {cr.sidecar_path()}")
    print(f"\nDONE artists:{len(result)} works:{hits} misses:{len(misses)}")
    for m in misses: print("  MISS", m)

if __name__ == "__main__":
    main()
