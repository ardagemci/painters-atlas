#!/usr/bin/env python3
"""Offline census. Writes only the sibling Markdown evidence; no build or fetch."""
from pathlib import Path
import collections
import hashlib
import json
import re
import subprocess
import unicodedata
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name('cross-registry-identity.md')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def asset(url):
    u = urlsplit(url or '')
    path = unquote(u.path)
    name = None
    if u.hostname == 'upload.wikimedia.org':
        m = re.match(r'/wikipedia/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/]+)', path)
        if m:
            name = m[1]
    elif u.hostname == 'commons.wikimedia.org' and path.startswith('/wiki/File:'):
        name = path.split('/wiki/File:', 1)[1]
    return unicodedata.normalize('NFC', name.replace('_', ' ')) if name else None

class Meta(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.images = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('property') == 'og:image':
            self.images.append(a.get('content', ''))

def cell(x):
    return str(x).replace('|', '&#124;').replace('\n', ' ')

def main():
    files = sorted(ROOT.glob('js/catalog-*.js')) + sorted(ROOT.glob('js/artists-*.js')) + [ROOT/'js/artworks.js', ROOT/'js/tier1-artists.js']
    # JXA evaluates only data registries in memory, never the app or SEO builder.
    code = 'var window = {};\n' + '\n'.join(p.read_text() for p in files)
    code += '\nJSON.stringify(window);'
    data = json.loads(subprocess.check_output(['osascript', '-l', 'JavaScript', '-'], input=code, text=True))
    cats = data['CATALOG']
    artists = {a['id']: a for a in data['ARTISTS']}
    sources = {c['id']: next(str(p.relative_to(ROOT)) for p in files if p.name.startswith('catalog-') and re.search(r'\bid\s*:\s*"'+re.escape(c['id'])+'"', p.read_text())) for c in cats}
    rows = []
    for aid, works in data['ARTWORKS'].items():
        for title, g in works.items():
            ga = asset(g.get('img'))
            exact = [c for c in cats if ga and ga == asset(c.get('image', {}).get('src'))]
            named = [c for c in cats if c['artistId'] == aid and title in (c['title'], c.get('worksKey'))]
            # Same artist plus partial title is a candidate only, never confirmation.
            plausible = [c for c in cats if c['artistId'] == aid and any(title.casefold() in t.casefold() or t.casefold() in title.casefold() for t in (c['title'], c.get('worksKey', c['title'])))]
            matches = exact or named
            kind = 'EXACT ASSET' if exact else 'CONFIRMED SAME ARTWORK' if len(named) == 1 else 'AMBIGUOUS' if named or plausible else 'UNMATCHED'
            if not exact and named and 'series' in title.casefold():
                kind = 'AMBIGUOUS'
            if kind == 'AMBIGUOUS':
                matches = []
            arc = bool(data.get('TIER1', {}).get(aid, {}).get('arc'))
            key_present = any(w['t'] == title for w in artists.get(aid, {}).get('works', []))
            render = bool(g.get('img')) and key_present and not arc
            rows.append(dict(aid=aid, title=title, g=g, asset=ga, matches=matches, candidates=named or plausible, kind=kind, render=render, arc=arc, key=key_present))
    count = collections.Counter(r['kind'] for r in rows)
    def withheld(c):
        i = c.get('image', {})
        return i.get('status') not in ('pd', 'licensed') or not i.get('src')
    conflicts = [(r,c) for r in rows for c in r['matches'] if withheld(c) and r['g'].get('img')]
    lines = ['# IFACE-001 — Cross-registry identity evidence', '', f'Inspection baseline: `{git("rev-parse", "HEAD")}`. Offline census of local registries and checked-in artwork stubs. No remote source or image loading was tested.', '',
    '## Method and limits', '',
    'Plan: enumerate both registries; match assets before artwork keys; separate eligibility from gallery reachability; inspect route stubs; enumerate conflicts and unresolved identity cases.', '',
    '`EXACT ASSET` means the gallery img and catalog image.src identify the same Commons file after decoding percent escapes, replacing underscores with spaces, and removing thumbnail sizing/path wrappers (Unicode NFC). Commons file titles establish shared assets, not artwork identity. Source page URLs are preserved as evidence, not silently substituted for the delivered image.', '',
    '`CONFIRMED SAME ARTWORK` means a different file, identical artistId and exact gallery title equality with catalog title or worksKey. This is confirmation under the requested registry-key rule, not independent art-historical verification. A missing catalog src also permits this key comparison. A series-level key is insufficient to confirm a particular work and is classified AMBIGUOUS even when worksKey agrees. `AMBIGUOUS` retains same-artist partial-title candidates (or multiple title matches) without assigning identity. `UNMATCHED` means neither asset nor title evidence nor a same-artist partial-title candidate; shared artist alone is insufficient. No translation, fuzzy-title or Commons redirect inference is made.', '',
    'Catalog eligibility requires a nonempty src and status pd or licensed. Tokens are recorded metadata, not legal conclusions. Missing gallery status is an unresolved policy question; it is not itself classified as an error.', '',
    'Gallery behavior: viewArtist in js/app.js has an ungated ARTWORKS image path, as RIGHTS-001 E-007 established. However, that Major works panel runs only when the artist has no TIER1 arc and the title occurs in artist.works. Arc artists instead use catalog cards. “Active” below means static source reachability through that ungated path, not a browser/network success. “Latent” means the entry has an img but is currently hidden by the arc panel or absent artist key. Both are listed so registry conflicts are not mistaken for currently visible images.', '',
    '**Prerender: INSPECTION OF CHECKED-IN STUBS, not execution of tools/build_seo.jxa.js.** The builder could emit different metadata if the stubs are stale. Each matched route below gives the literal decoded og:image content from git HEAD; a missing route or tag is explicit. Runtime eligibility and stub content are separate measurements.', '',
    '## Summary', '', '| Measure | Count |', '| --- | ---: |', f'| Catalog records | {len(cats)} |', f'| ARTWORKS entries | {len(rows)} |']
    for k in ('EXACT ASSET','CONFIRMED SAME ARTWORK','AMBIGUOUS','UNMATCHED'):
        lines.append(f'| {k} | {count[k]} |')
    lines += [f'| Gallery entries reachable through ungated panel | {sum(r["render"] for r in rows)} |', f'| Matched withheld catalog / gallery-img conflicts (entry–record pairs) | {len(conflicts)} |', f'| Of those, active ungated gallery rendering | {sum(r["render"] for r,c in conflicts)} |', f'| Of those, latent gallery entries | {sum(not r["render"] for r,c in conflicts)} |', f'| Entries without a confirmed artwork route mapping | {sum(not r["matches"] for r in rows)} |', '', '## Full withheld-catalog / gallery-img conflict list', '']
    for r,c in conflicts:
        i=c['image']
        lines.append(f'- `{r["aid"]}` / **{r["title"]}** → `{c["id"]}` ({r["kind"]}); status `{i.get("status")}`, src {"present" if i.get("src") else "missing"}; gallery **{"ACTIVE ungated render path" if r["render"] else "LATENT (not currently rendered by this panel)"}**. Full URLs and stub inspection follow in its census row.')
    lines += ['', '## Complete entry census', '', 'Every heading identifies the exact ARTWORKS artistId/title key. Catalog references preserve record IDs and source files. No confirmed mapping means no identified canonical artwork route; candidate routes must not be treated as an identity link.', '']
    stub_cache={}
    for n,r in enumerate(rows,1):
        lines += [f'### {n}. {r["aid"]} / {r["title"]}', '', f'- Classification: **{r["kind"]}**.', f'- Gallery source: `js/artworks.js` → `{r["aid"]}` → `{r["title"]}`; img: `{r["g"].get("img", "")}`; page: `{r["g"].get("page", "")}`.', f'- Normalized gallery asset: `{r["asset"]}`.', f'- Gallery rendering: {"ACTIVE ungated image path" if r["render"] else "LATENT: arc replaces panel" if r["arc"] else "LATENT: artist works key or img absent"}; no gallery status field.']
        for c in r['matches']:
            i=c['image']; path=f'p/artwork/{c["id"]}.html'
            if path not in stub_cache:
                p=subprocess.run(['git','show',f'HEAD:{path}'],cwd=ROOT,text=True,capture_output=True)
                stub_cache[path]=Meta(p.stdout).images if p.returncode == 0 else None
            og=stub_cache[path]
            ev=f'same Commons asset `{asset(i.get("src"))}`' if r['kind']=='EXACT ASSET' else f'identical artistId `{c["artistId"]}` and gallery key equals catalog '+ ('title' if r['title']==c['title'] else 'worksKey')+f' `{r["title"]}`' + ('; catalog src absent' if not i.get('src') else '; different image files')
            lines += [f'- Catalog: `{sources[c["id"]]}` / `{c["id"]}`; title `{c["title"]}`; worksKey `{c.get("worksKey", "(absent)")}`; artistId `{c["artistId"]}`. Evidence: {ev}.', f'- Catalog image.status: `{i.get("status")}`; eligibility: **{"WITHHOLD" if withheld(c) else "eligible"}**; src: `{i.get("src", "")}`; page: `{i.get("page", "")}`.', f'- Checked-in route `{path}` — og:image: '+ ('**ROUTE MISSING**' if og is None else '**TAG ABSENT**' if not og else '; '.join(f'`{u}`' for u in og))+'.']
            if withheld(c) and og:
                lines.append('- Stub flag: withheld catalog record still has og:image metadata; the URL above may be a fallback image rather than this artwork. It must be assessed separately from gallery delivery.')
        if not r['matches']:
            lines.append('- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/'+r['aid']+'`. Do not invent a slug from the gallery title.')
            if r['candidates']:
                lines.append('- Unconfirmed same-artist title candidates: '+ '; '.join(f'`{c["id"]}` ({sources[c["id"]]}), title `{c["title"]}`, worksKey `{c.get("worksKey", "(absent)")}`' for c in r['candidates'])+'. A partial or series-level title does not establish individual artwork identity.')
            else:
                lines.append('- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.')
        if r['kind'] == 'AMBIGUOUS':
            for c in r['candidates']:
                ci = c.get('image', {})
                lines.append(f'- Candidate asset evidence for `{c["id"]}` (not a confirmed match): src `{ci.get("src", "")}`; page `{ci.get("page", "")}`; normalized asset `{asset(ci.get("src"))}`.')
        if r['title'] == 'The Swan series':
            lines.append('- Specific contradiction: gallery asset names No. 22; catalog swan-no-17 names No. 17. Shared series key does not resolve that difference.')
        if r['title'] == 'Rouen Cathedral series':
            lines.append('- Series ambiguity: gallery page identifies the series; its file name does not establish the catalog’s Full Sunlight (Harmony in Blue and Gold) version.')
        lines.append('')
    lines += ['## What this means for the pending theory brief', '', '- Cross-registry identity: should shared files and artwork identity remain separate links, and who resolves ambiguous titles, versions and unmatched gallery keys?', '- Rights precedence: when a catalog token withholds an image and a gallery entry supplies one, which registry governs? Should a different file of the same artwork inherit a decision, or require its own source evidence?', '- Consistent withholding: how should a decision propagate across the active gallery, latent entries, catalog cards, lightbox and prerender metadata? What fallback is appropriate when a checked-in stub contains another artwork?', '- Policy completeness: what evidence and owner decision should fill the missing gallery-status contract without treating absence as an automatic finding?', '', '## Reproduction and source fingerprints', '', 'From the repository root on macOS, run:', '', '```sh', 'python3 protocol/tasks/IFACE-001/evidence/cross_registry_identity.py', 'git show HEAD:js/app.js', 'git show HEAD:p/artwork/the-starry-night.html', '```', '', 'The Python script uses the standard library and osascript/JXA only to evaluate registry declarations in memory. It does not execute the app or SEO builder, fetch URLs, or change git state. It rewrites only this report. Registry files are read from the working tree; stubs are read from HEAD. SHA-256 fingerprints pin the inspected data:', '']
    for p in files:
        lines.append(f'- `{p.relative_to(ROOT)}`: `{hashlib.sha256(p.read_bytes()).hexdigest()}`')
    OUT.write_text('\n'.join(lines)+'\n')
    print(json.dumps({'entries':len(rows),'classes':count,'conflicts':[(r['aid'],r['title'],c['id'],r['render']) for r,c in conflicts],'ambiguous':[(r['aid'],r['title']) for r in rows if r['kind']=='AMBIGUOUS']},indent=2))

if __name__ == '__main__':
    main()
