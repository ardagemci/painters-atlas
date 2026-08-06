#!/usr/bin/env python3
"""Wikimedia Commons rights capture for Pigment's artwork tooling.

Standard library only, no dependencies, same as every other tool here.

Two rules govern this whole module, and they are not stylistic:

1. **A transient failure is never a negative finding.** upload.wikimedia.org
   and the Commons API both rate-limit hard, and this project has been burned
   by treating a 429 as a verdict. A timeout, a 429, a 5xx or a connection
   reset produces status ``unverified`` — never "no licence", never "dead",
   never "unresolved because we checked and found nothing". Only an explicit
   ``missing`` page from the API is a definitive negative, and even that is
   reported as ``missing``, not as a rights conclusion. PIGMENT.md §14 says
   this for dead-URL classification; it matters more here, where a wrong
   negative is a false accusation and a wrong positive is a false clearance.

2. **Nothing here reaches a legal conclusion.** This module records what
   Commons *asserts* — licence short name, licence template, author, credit,
   attribution requirement, origination date — and the Commons file page it
   asserted it on. Per owner decision OD-5, a clearance claim needs qualified
   review; unresolved entries stay labelled unresolved. Every record carries
   ``legal_conclusion: "none"`` so no downstream consumer can mistake the
   register for a clearance.

Why the Commons file page matters: the catalog's own ``image.page`` field
points at an English Wikipedia *article* (e.g. ``en.wikipedia.org/wiki/
The_Calling_of_Saint_Matthew``), which carries no licence statement at all.
The rights register needs ``descriptionurl`` — the real
``commons.wikimedia.org/wiki/File:...`` page.
"""
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "PigmentAtlas/1.0 (personal static art atlas; gemciarda@gmail.com)"}

API = "https://commons.wikimedia.org/w/api.php"

#: Minimum seconds between two outbound requests, enforced process-wide.
MIN_INTERVAL = 0.25

#: Backoff schedule for retryable failures, in seconds.
BACKOFF = (1.0, 3.0, 9.0)

#: The extmetadata keys this project cares about, mapped to record field names.
EXTMETA_FIELDS = (
    ("LicenseShortName", "license_short_name"),
    ("License", "license"),
    ("LicenseUrl", "license_url"),
    ("UsageTerms", "usage_terms"),
    ("Artist", "artist"),
    ("Credit", "credit"),
    ("Attribution", "attribution"),
    ("AttributionRequired", "attribution_required"),
    ("DateTimeOriginal", "date_time_original"),
    ("Copyrighted", "copyrighted"),
    ("Restrictions", "restrictions"),
)

_last_request = [0.0]


class Unverified(Exception):
    """A request failed in a way that proves nothing about the asset."""


def _throttle():
    gap = time.time() - _last_request[0]
    if gap < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - gap)
    _last_request[0] = time.time()


def api_get_json(url, attempts=4):
    """GET JSON, politely, with backoff.

    Raises Unverified on anything that does not prove a fact about the asset.
    """
    last = None
    for i in range(attempts):
        _throttle()
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 404):
                # A malformed or absent API endpoint is a bug in the caller,
                # not a fact about the asset. Still unverified.
                raise Unverified(last)
            wait = BACKOFF[min(i, len(BACKOFF) - 1)]
            retry_after = e.headers.get("Retry-After") if e.headers else None
            if retry_after:
                try:
                    wait = max(wait, float(retry_after))
                except ValueError:
                    pass
            if i < attempts - 1:
                time.sleep(wait)
        except Exception as e:                       # timeout, DNS, reset, bad JSON
            last = f"{type(e).__name__}: {e}"
            if i < attempts - 1:
                time.sleep(BACKOFF[min(i, len(BACKOFF) - 1)])
    raise Unverified(last or "unknown failure")


def strip_html(s):
    """extmetadata values arrive as HTML fragments; render them as plain text."""
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def commons_file_title(url):
    """Derive the Commons ``File:`` title from an upload.wikimedia.org URL.

    Handles both the direct form
        /wikipedia/commons/0/05/Name.gif
    and the thumbnail form
        /wikipedia/commons/thumb/5/59/Name.jpg/500px-Name.jpg
    where the real filename is the segment before the rendered thumbnail.
    Returns None for anything not hosted on the Commons file tree.
    """
    if not url:
        return None
    path = urllib.parse.urlparse(url).path
    parts = [p for p in path.split("/") if p]
    if "commons" not in parts:
        return None                                   # e.g. /wikipedia/en/ = local fair use
    if "thumb" in parts:
        i = parts.index("thumb")
        if len(parts) <= i + 3:
            return None
        fname = parts[i + 3]
    else:
        fname = parts[-1]
    fname = urllib.parse.unquote(fname)
    return "File:" + fname if fname else None


def rights_from_imageinfo(ii):
    """Flatten one ``imageinfo`` entry into a rights record.

    ``ii`` is the dict the API returns for a single file revision. Missing
    extmetadata keys become empty strings, never guesses.
    """
    ext = ii.get("extmetadata") or {}
    rec = {
        "commons_file_page": ii.get("descriptionurl", ""),
        "file_url": ii.get("url", ""),
        "mime": ii.get("mime", ""),
        "legal_conclusion": "none",
    }
    for key, field in EXTMETA_FIELDS:
        raw = (ext.get(key) or {}).get("value", "")
        rec[field] = strip_html(raw if isinstance(raw, str) else str(raw))
    return rec


#: extmetadata keys that describe *what the file depicts*, as opposed to who
#: holds rights in it. Kept separate from EXTMETA_FIELDS on purpose: these feed
#: the exact-artwork check in tools/audit_artworks.py, never the rights record,
#: and adding them to a rights record would imply Commons' description is a
#: rights assertion. It is not.
DESCRIPTIVE_FIELDS = (
    ("ObjectName", "object_name"),
    ("ImageDescription", "description"),
    ("Artist", "artist"),
    ("Credit", "credit"),
)


def describe_from_imageinfo(ii):
    """Flatten one ``imageinfo`` entry into what Commons says the file *depicts*.

    Missing keys become empty strings. An empty field means Commons asserted
    nothing, which is not the same as Commons asserting a negative — callers
    must not read absence as evidence.
    """
    ext = (ii or {}).get("extmetadata") or {}
    out = {}
    for key, field in DESCRIPTIVE_FIELDS:
        raw = (ext.get(key) or {}).get("value", "")
        out[field] = strip_html(raw if isinstance(raw, str) else str(raw))
    return out


def _query_url(titles):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "titles": "|".join(titles),
    }
    return API + "?" + urllib.parse.urlencode(params)


def fetch_rights(titles, batch=50, on_batch=None):
    """Resolve rights for Commons file titles.

    Yields one record per requested title, in request order, each with a
    ``status`` of:
      ``ok``          — imageinfo with extmetadata came back
      ``no-metadata`` — the page exists but returned no imageinfo (rare)
      ``missing``     — the API explicitly says the file does not exist
      ``unverified``  — the request failed; this proves NOTHING about the file

    ``batch`` is capped at 50, the Commons API's limit for anonymous clients.
    """
    titles = list(titles)
    batch = max(1, min(int(batch), 50))
    for start in range(0, len(titles), batch):
        chunk = titles[start:start + batch]
        try:
            data = api_get_json(_query_url(chunk))
        except Unverified as e:
            for t in chunk:
                yield {"title": t, "status": "unverified", "reason": str(e),
                       "legal_conclusion": "none"}
            if on_batch:
                on_batch(start, len(chunk), "unverified")
            continue

        pages = ((data.get("query") or {}).get("pages")) or []
        # formatversion=2 gives a list; normalized/redirect maps let us match
        # the title we asked for back to the title we got.
        norm = {n["from"]: n["to"] for n in ((data.get("query") or {}).get("normalized") or [])}
        by_title = {p.get("title"): p for p in pages}

        for t in chunk:
            p = by_title.get(norm.get(t, t)) or by_title.get(t)
            if p is None:
                yield {"title": t, "status": "unverified",
                       "reason": "title absent from response", "legal_conclusion": "none"}
                continue
            if p.get("missing"):
                yield {"title": t, "status": "missing", "legal_conclusion": "none"}
                continue
            info = p.get("imageinfo") or []
            if not info:
                yield {"title": t, "status": "no-metadata", "legal_conclusion": "none"}
                continue
            rec = rights_from_imageinfo(info[0])
            # Key on the title the caller asked for, not the normalized one the
            # API echoes back — Commons turns underscores into spaces, and a
            # caller that keyed on the response would silently lose every hit.
            rec["title"] = t
            rec["resolved_title"] = p.get("title", t)
            rec["status"] = "ok"
            yield rec
        if on_batch:
            on_batch(start, len(chunk), "ok")


def sidecar_path():
    """Where opportunistic rights captures accumulate.

    fetch_artworks.py and audit_artworks.py already talk to the Commons API;
    asking for ``extmetadata`` in the query they were making anyway costs one
    extra parameter and zero extra requests, so they stash what comes back
    here. Deliberately a **sidecar**, not a field on ``js/artworks.js``:
    licence metadata is build-time provenance, and inflating the shipped
    bundle with ~530 authors and licence templates would make every visitor
    download rights paperwork to look at a painting.

    Override with the PIGMENT_RIGHTS_CACHE environment variable.
    """
    import os
    return os.environ.get(
        "PIGMENT_RIGHTS_CACHE",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "rights-cache.json"))


def load_sidecar(path=None):
    import os
    path = path or sidecar_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}                                     # a corrupt cache is not a finding


def save_sidecar(records, path=None, merge=True):
    """Write ``{commons_file_title: rights_record}``, merging by default.

    Merging matters: a run that failed to verify a file must not erase what an
    earlier run *did* verify. An ``unverified`` record never overwrites an
    ``ok`` one.
    """
    path = path or sidecar_path()
    out = load_sidecar(path) if merge else {}
    for title, rec in records.items():
        prev = out.get(title)
        if prev and prev.get("status") == "ok" and rec.get("status") != "ok":
            continue
        out[title] = rec
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    return len(out)


def capture_from_imageinfo(store, page):
    """Stash rights from an API page dict, if it carried extmetadata.

    Safe to call on any page shape; a page without extmetadata is skipped
    rather than recorded as having no licence.
    """
    info = (page or {}).get("imageinfo") or []
    if not info or "extmetadata" not in info[0]:
        return False
    rec = rights_from_imageinfo(info[0])
    rec["status"] = "ok"
    rec["captured_at"] = time.strftime("%Y-%m-%d")
    title = page.get("title") or rec.get("commons_file_page", "")
    if not title:
        return False
    store[title] = rec
    return True


def rights_for_urls(urls, batch=50, on_batch=None):
    """Resolve rights for upload.wikimedia.org URLs.

    Deduplicates by underlying Commons file, so N thumbnail widths of one file
    cost one lookup. Returns ``{url: record}``; a URL whose Commons title
    cannot be derived gets status ``not-commons`` (a fact about the URL shape,
    not a rights finding).
    """
    title_by_url, out = {}, {}
    for u in urls:
        t = commons_file_title(u)
        if t is None:
            out[u] = {"status": "not-commons", "legal_conclusion": "none"}
        else:
            title_by_url[u] = t

    wanted = sorted(set(title_by_url.values()))
    resolved = {}
    for rec in fetch_rights(wanted, batch=batch, on_batch=on_batch):
        resolved[rec["title"]] = rec

    for u, t in title_by_url.items():
        rec = dict(resolved.get(t, {"title": t, "status": "unverified",
                                    "reason": "not returned", "legal_conclusion": "none"}))
        rec["requested_title"] = t
        out[u] = rec
    return out
