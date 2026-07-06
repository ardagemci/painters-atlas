#!/usr/bin/env python3
"""Audit and repair js/artworks.js.

Flags entries whose image clearly isn't the artwork (museum-room photos,
building photos, unrelated pages), re-resolves them with strict filename
validation, health-checks every URL, and rewrites js/artworks.js.
Needs /tmp/pigment-artists.json (tools/dump-artists.jxa.js).
"""
import json, re, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "PigmentAtlas/1.0 (personal static art atlas; gemciarda@gmail.com)"}
BLACKLIST = ("room", "salle", "interior", "interieur", "installation", "visitors",
             "exhibition", "exposition", "in_situ", "hanging", "walls_of", "zaal")
ART_WORDS = ("painting", "painted", "canvas", "fresco", "triptych", "altarpiece",
             "series of", "mural", "woodblock", "print", "panel", "scroll", "icon")
NOT_ART = ("cathedral in", "church in", "museum in", "building in", "is a museum",
           "is a church", "is a cathedral", "statue", "sculpture in")

# artist-id::work-title -> wikipedia titles to trust first
OVERRIDES = {
    "leonardo-da-vinci::Salvator Mundi": ["Salvator Mundi (Leonardo)"],
    "claude-monet::Rouen Cathedral series": ["Rouen Cathedral (Monet series)", "Rouen Cathedral Series (Monet)"],
    "claude-monet::Water Lilies (Grandes Décorations)": ["Water Lilies (Monet series)", "Nymphéas (Monet)"],
}

def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def head_check(url):
    """'ok' | 'bad' (definitive 4xx) | 'unknown' (throttle/network — do not delete)."""
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status == 200 and r.headers.get("Content-Type", "").startswith("image/"):
                return "ok"
            return "unknown"
    except urllib.error.HTTPError as e:
        if e.code in (400, 404, 410):
            return "bad"
        return "unknown"                                   # 429/5xx: throttled, not broken
    except Exception:
        return "unknown"

def tokens(s, minlen):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("_", " ")).split() if len(t) >= minlen]

def fname_of(url):
    return urllib.parse.unquote(url.split("/")[-1]).lower().replace("_", " ")

def fname_valid(url, name_toks, title_toks):
    f = fname_of(url)
    if any(b.replace("_", " ") in f for b in BLACKLIST):
        return False
    return any(t in f for t in name_toks) or any(t in f for t in title_toks)

def wiki_summary(title):
    q = urllib.parse.quote(title.replace(" ", "_"))
    try:
        return get_json("https://en.wikipedia.org/api/rest_v1/page/summary/" + q)
    except Exception:
        return None

def try_wiki(cands, name_toks, title_toks):
    for cand in cands:
        s = wiki_summary(cand); time.sleep(0.06)
        if not s or s.get("type") != "standard":
            continue
        thumb = (s.get("thumbnail") or {}).get("source", "")
        if "/wikipedia/commons/" not in thumb:
            continue
        text = ((s.get("description") or "") + " " + (s.get("extract") or "")).lower()
        if any(w in text for w in NOT_ART) and not any(w in text for w in ART_WORDS):
            continue
        if not (any(w in text for w in ART_WORDS) or any(t in text for t in name_toks)):
            continue
        img = re.sub(r"/\d+px-", "/500px-", thumb)
        if not fname_valid(img, name_toks, title_toks):
            continue
        page = ((s.get("content_urls") or {}).get("desktop") or {}).get("page", "")
        return {"img": img, "page": page}
    return None

def try_commons(queries, name_toks, title_toks):
    for q in queries:
        u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
             "&generator=search&gsrnamespace=6&gsrlimit=8"
             "&prop=imageinfo&iiprop=url|mime&iiurlwidth=500"
             "&gsrsearch=" + urllib.parse.quote(q))
        try:
            d = get_json(u)
        except Exception:
            continue
        time.sleep(0.06)
        pages = (d.get("query") or {}).get("pages") or {}
        for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            ii = (p.get("imageinfo") or [{}])[0]
            url = ii.get("thumburl", "")
            if not ii.get("mime", "").startswith("image/") or not url:
                continue
            if ".djvu" in url.lower() or ".pdf" in url.lower():
                continue
            if fname_valid(url, name_toks, title_toks):
                return {"img": url, "page": ii.get("descriptionurl", "")}
    return None

def main():
    artists = {a["id"]: a for a in json.load(open("/tmp/pigment-artists.json"))}
    src = open("js/artworks.js").read()
    head, tail = src.split("window.ARTWORKS = ", 1)
    data = json.loads(tail.rstrip().rstrip(";"))

    flagged, fixed, kept, dropped = [], [], [], []
    for aid, works in data.items():
        a = artists[aid]
        name_toks = tokens(a["name"], 4)
        for title in list(works):
            key = f"{aid}::{title}"
            entry = works[title]
            title_toks = tokens(re.sub(r"\(.*?\)", "", title), 5)
            page_l = urllib.parse.unquote(entry.get("page", "")).lower().replace("_", " ")
            suspect = key in OVERRIDES \
                or any(b.replace("_", " ") in fname_of(entry["img"]) for b in BLACKLIST) \
                or (not any(t in fname_of(entry["img"]) for t in name_toks)
                    and not any(t in page_l for t in name_toks))
            if not suspect:
                continue
            flagged.append(key)
            clean = re.sub(r"\s*\(.*?\)", "", title).strip()
            surname = a["name"].split()[-1]
            cands = OVERRIDES.get(key, []) + [
                f"{clean} ({surname} series)", f"{clean} ({surname})", f"{clean} (painting)"]
            art = try_wiki(cands, name_toks, title_toks) \
                or try_commons([f"{clean} {a['name']} painting", f"{clean} {a['name']}"], name_toks, title_toks)
            if art and art["img"] != entry["img"]:
                works[title] = art; fixed.append(key)
            elif art:
                kept.append(key + "  (same image reconfirmed)")
            else:
                del works[title]; dropped.append(key)
            print(f"  {key} -> {'FIXED' if key in fixed else 'DROPPED' if key in dropped else 'kept'}", flush=True)

    print("\nHealth-checking all URLs (politely)...", flush=True)
    dead, unknown = 0, 0
    for aid, works in list(data.items()):
        for title in list(works):
            url = works[title]["img"]
            st = head_check(url)
            time.sleep(0.25)
            if st == "unknown":                            # back off once, then trust it
                time.sleep(2.5)
                st = head_check(url)
                time.sleep(0.25)
                if st == "unknown":
                    unknown += 1
                    print(f"  UNKNOWN (kept) {aid}::{title}", flush=True)
                    continue
            if st == "ok":
                continue
            alt = re.sub(r"/\d+px-", "/330px-", url)       # definitive 4xx: try smaller bucket
            if alt != url and head_check(alt) == "ok":
                works[title]["img"] = alt
                print(f"  RESIZED {aid}::{title}", flush=True)
            else:
                del works[title]; dead += 1
                print(f"  DEAD (4xx) {aid}::{title}", flush=True)
            time.sleep(0.25)
        if not works:
            del data[aid]

    with open("js/artworks.js", "w") as f:
        f.write(head + "window.ARTWORKS = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    total = sum(len(v) for v in data.values())
    print(f"\nDONE flagged:{len(flagged)} fixed:{len(fixed)} dropped:{len(dropped)} dead:{dead} unknown-kept:{unknown}")
    print(f"final: {len(data)} artists, {total} works")

if __name__ == "__main__":
    main()
