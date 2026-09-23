#!/usr/bin/env python3
"""Audit and repair js/artworks.js.

Flags entries whose image clearly isn't the artwork (museum-room photos,
building photos, unrelated pages), re-resolves them against what Commons
asserts about each candidate file, health-checks every URL, and rewrites
js/artworks.js. Needs /tmp/pigment-artists.json (tools/dump-artists.jxa.js).

The acceptance rule lives in match_verdict(); read its docstring before
changing anything here. It replaced a filename-only rule that accepted a file
whose name shared *either* an artist word *or* a title word, which is how 20
confirmed mismatches reached the shipped catalog (docs/IMAGE_RIGHTS_ROUTES.md
§1.6): Van Gogh's Irises under Ogata Korin, a Seurat under Berthe Morisot, a
photograph of Kurt Schwitters standing in for a sound poem.
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commons_rights as cr

# Rights metadata captured while auditing. extmetadata rides along on queries
# this tool already makes, so the capture costs no extra request and cannot
# make the rate-limiting worse. See tools/rights_register.py. No legal
# conclusion is reached here or anywhere in this file.
RIGHTS = {}

UA = {"User-Agent": "PigmentAtlas/1.0 (personal static art atlas; gemciarda@gmail.com)"}
ART_WORDS = ("painting", "painted", "canvas", "fresco", "triptych", "altarpiece",
             "series of", "mural", "woodblock", "print", "panel", "scroll", "icon")
NOT_ART = ("cathedral in", "church in", "museum in", "building in", "is a museum",
           "is a church", "is a cathedral", "statue", "sculpture in")

# --- vocabulary for the exact-artwork check -------------------------------
#
# Every list below answers one question: which words, standing alone, must
# NOT be allowed to establish that a file depicts a particular work? Each is
# checked against our own record title first, so a painting actually called
# "The Blue Room" is not rejected for containing "room", and Corot's
# "Souvenir de Mortefontaine" is not rejected for containing "souvenir".

# The work is not in the picture: a gallery wall, a vitrine, an install shot.
ROOM_WORDS = ("room", "salle", "interior", "interieur", "installation", "visitors",
              "exhibition", "exposition", "in situ", "hanging", "walls of", "zaal",
              "gallery of honour", "gallery of honor")

# The picture is of an object that reproduces the work, not of the work
# (PIGMENT.md §14: "not a museum room, building, souvenir, detail crop,
# reproduction object"). This is how Emily Carr's "Big Raven" became a 1971
# Canadian postage stamp.
REPRO_WORDS = ("stamp", "postage", "postcard", "banknote", "souvenir", "replica",
               "poster", "mug", "tapestry")
REPRO_PHRASES = ("book cover", "mosaic copy", "cigarette card")

# Only part of the work, or a rehearsal for it, or somebody else's copy of it
# (§14: "full compositions are preferred over detail crops"). Multilingual
# because Commons is: "Skizze", "étude", "Ausschnitt", "bozzetto".
PARTIAL_WORDS = ("detail", "cropped", "crop", "fragment", "ausschnitt", "etude",
                 "studie", "skizze", "bozzetto", "esquisse", "modello", "reproduction")
PARTIAL_PHRASES = ("study for", "sketch for", "copy of", "copy after", "engraving after")

# Generic art vocabulary. These words appear in thousands of unrelated files,
# so a shared "portrait" or "landscape" is not evidence that two records name
# the same painting — that shared word is precisely what let four self-portrait
# confusions and a Danish 1831 oil (as Sesshu Toyo) through the old rule.
STOP_WORDS = set("""
portrait portraits selfportrait autoportrait bildnis retrato ritratto
landscape landscapes seascape scene scenes view views vue vista veduta vedute
still life nature morte nude nudes akt study studies etude sketch skizze composition untitled
figure figures woman women girl girls child children lady young head face hand hands
flower flowers floral fruit tree trees forest wood woods river ocean lake mountain mountains
field fields house village town city street road bridge church cathedral castle ruins tower
harbour harbor port beach shore cloud clouds moon sunset sunrise
night morning evening dawn dusk winter summer spring autumn season seasons
rain snow storm mist light shadow horse horses bird birds
saint santa madonna virgin christ jesus holy angel angels
painting paintings picture image work works series panel canvas tempera fresco print prints
drawing drawings watercolour watercolor gouache pastel engraving etching woodcut plate detail
number left right upper lower front first second third great grand petit large small
family group interior exterior garden gardens park
""".split())

# Articles and prepositions, in the languages Commons file pages actually use.
FUNCTION_WORDS = set("""a an and the of in on at with by from for to or as is its his her their
le la les el il los las un une der die das den dem des von zu im am""".split())

# "This file is a self-portrait", in the languages Commons says it in. Needed
# in both directions: a self-portrait must not stand in for a subject picture
# (Poussin, Stubbs), and a named sitter must not stand in for a self-portrait
# (Mihri Musfik's "Leyla Turgut Portresi").
SELF_MARKERS = ("self portrait", "selfportrait", "self portr", "autoportrait",
                "autoritratto", "autorretrato", "autoportret", "autoretrat",
                "auto retrato", "selbstbildnis", "selbstportrat", "selbstportraet",
                "zelfportret", "autoportre")

# artist-id::work-title -> other titles the same work is legitimately known by.
#
# The check below cannot translate, and Commons files are titled in the
# language of whoever uploaded them. Where the English title we ship and the
# title Commons asserts are the same painting, that equivalence is a
# *curatorial fact*, recorded here by a human, exactly like PINNED above —
# never guessed. Only add an entry after reading the Commons file page.
#
# Note that most translated titles need no entry: a file page in French or
# Danish simply carries no English title to contradict ours, and the check
# reports "unconfirmed" rather than rejecting. Entries are needed only where
# Commons asserts a *different English* title for the same work.
# Every entry below was needed: without it the shipped image is rejected, with
# it the same image is confirmed. Word-spacing ("The Beaneater" / "The Bean
# Eater") and English plurals ("Cloud Studies" / "Cloud Study") are handled by
# the check itself and need no entry.
TITLE_ALIASES = {
    "jean-honore-fragonard::The Bolt": ["Le Verrou", "The Lock"],
    "theodore-gericault::Portraits of the Insane": ["Portrait of a Kleptomaniac",
                                                    "Monomanies"],
    "claude-monet::Haystacks series": ["Meules", "Stacks of Wheat", "Wheatstacks"],
}

# artist-id::work-title -> wikipedia titles to trust first
OVERRIDES = {
    "leonardo-da-vinci::Salvator Mundi": ["Salvator Mundi (Leonardo)"],
    "claude-monet::Rouen Cathedral series": ["Rouen Cathedral (Monet series)", "Rouen Cathedral Series (Monet)"],
}

# artist-id::work-title -> exact Commons file, hand-curated; never re-searched
PINNED = {
    # Hand-corrected 2026-09-23 (owner present). The pin named "Sistine Chapel
    # ceiling 02 (brightened).jpg" while the gallery served this file, so the
    # pin described no shipped image and a re-resolution run would have swapped
    # one in unasked. The brightened file is a 2014 in-situ photograph of the
    # chapel interior: the ceiling recedes in perspective, the side walls carry
    # other painters' frescoes, and its lower half is The Last Judgment — this
    # artist's sibling record below. This file is a rectified reproduction of
    # the vault alone. Chosen on subject, not on rights: the two Commons pages
    # assert different bases and this reaches no legal conclusion (OD-5, AC12).
    "michelangelo::Sistine Chapel Ceiling": "Sistine ceiling.jpg",
    "michelangelo::The Last Judgment": "Last Judgement (Michelangelo).jpg",
    "claude-monet::Water Lilies (Grandes Décorations)": "Claude Monet - The Water Lilies - Setting Sun - Google Art Project.jpg",
    "jan-van-eyck::Man in a Red Turban": "Jan van Eyck - Portrait of a Man (Self Portrait?) 1433.jpg",
    "jacek-malczewski::The Vicious Circle": "Bledne kolo.jpg",
    "hilma-af-klint::Paintings for the Temple": "Hilma af Klint - Altarpiece No. 1 Group X (13919).jpg",
    "caravaggio::Judith Beheading Holofernes": "Judith Beheading Holofernes-Caravaggio (c.1598-9).jpg",
    # Hand-corrected 2026-07-25 (PIG-001 AC11 register). The previous file was
    # "Aleppo ca1537 by Matrakci Nasuh …" — the same manuscript and artist, but
    # the Aleppo folio, not the Istanbul one, and a duplicate of this artist's
    # sibling "View of Aleppo" record. Before pinning: the exact-work check
    # passed against the Commons file page, and that page's metadata asserts a
    # public-domain basis. No independent legal determination (OD-5, AC12).
    "matrakci-nasuh::View of Istanbul (Mecmu-ı Menazil)": "Matrakçı Nasuh - İstanbul.jpg",
    # Batch 21 (docs/ROSTER_BATCH_21.md), 2026-09-19. Every file opened by eye;
    # each Commons page's metadata is recorded in docs/roster-batch-21/<id>.json.
    # No independent legal determination (OD-5).
    "cimabue::Santa Trinita Maestà": "Cimabue - Maestà di Santa Trinita - Google Art Project.jpg",
    "cimabue::Crucifix of Santa Croce": "Cimabue 025.jpg",
    "cimabue::The Mocking of Christ": "La Dérision du Christ - Cimabue - Musée du Louvre Peintures RFML.PE.2023.33.1 - après restauration.jpg",
    "cimabue::Maestà of the Louvre": "La Vierge et l'Enfant en majesté entourés de six anges - Cimabue - Musée du Louvre Peintures INV 254 ; MR 159.jpg",
    "simone-martini::Annunciation with Saints Margaret and Ansanus": "Simone Martini — Annunciation with St. Margaret and St. Ansanus.jpg",
    "simone-martini::Saint Louis of Toulouse Crowning Robert of Anjou": "Simone Martini 013.jpg",
    "simone-martini::Maestà": "Maestà di simone martini, siena palazzo pubblico 1315-1321.jpg",
    "simone-martini::Orsini Polyptych": "Orsini Polyptiek, Simone Martini, 14de eeuw, Koninklijk Museum voor Schone Kunsten Antwerpen, 257-260.jpg",
    "ambrogio-lorenzetti::Effects of Good Government in the City": "Ambrogio Lorenzetti - Effects of Good Government in the city - Google Art Project.jpg",
    "ambrogio-lorenzetti::Presentation in the Temple": "Ambrogio Lorenzetti - Presentazione di Gesù al tempio - Google Art Project.jpg",
    "ambrogio-lorenzetti::Annunciation": "Ambrogio Lorenzetti Annunciation.jpg",
    "ambrogio-lorenzetti::Maestà of Massa Marittima": "Ambrogio lorenzetti, maestà di massa marittima.jpg",
    "filippo-lippi::Madonna and Child with Two Angels": "Madonna and Child with two Angels (by Filippo Lippi) – Galleria degli Uffizi, Florence.jpg",
    "filippo-lippi::Adoration in the Forest": "Maria, das Kind verehrend, mit dem Johannesknaben und dem Heiligen Bernhard - Die Anbetung im Walde, Die Anbetung im Walde - Gemäldegalerie Berlin - 5223451.jpg",
    "filippo-lippi::Coronation of the Virgin": "Fra Filippo Lippi 007.jpg",
    "filippo-lippi::Barbadori Altarpiece": "Pala Barbadori - Fra Filippo Lippi - Musée du Louvre Peintures INV 339.jpg",
    "paolo-uccello::The Battle of San Romano": "Uccello — the Battle of San Romano.jpg",
    "paolo-uccello::Saint George and the Dragon": "Paolo Uccello Heiliger Georg und der Drachen 1 470.jpg",
    "paolo-uccello::The Hunt in the Forest": "Hunt in the forest by paolo uccello.jpg",
    "paolo-uccello::Monument to Sir John Hawkwood": "Paolo Uccello 044.jpg",
    "domenico-ghirlandaio::An Old Man and His Grandson": "Ghirlandaio, Domenico - An Old Man and His Grandson - Louvre - Google Art Project.jpg",
    "domenico-ghirlandaio::Portrait of Giovanna Tornabuoni": "Domenico Ghirlandaio, 1489-1490 - Portrait of Giovanna Tornabuoni - Google Art Project.jpg",
    "domenico-ghirlandaio::Calling of the First Apostles": "Ghirlandaio, Domenico - Calling of the Apostles - 1481.jpg",
    "domenico-ghirlandaio::Adoration of the Magi": "Adoration of the Magi Spedale degli Innocenti.jpg",
    "antonello-da-messina::Saint Jerome in His Study": "Antonello da Messina - St Jerome in his study - National Gallery London.jpg",
    "antonello-da-messina::Virgin Annunciate": "Antonello da Messina, Annunciata di Palermo, circa 1475-77 -FG2.jpg",
    "antonello-da-messina::Saint Sebastian": "Antonello da Messina - St. Sebastian - Google Art Project.jpg",
    "antonello-da-messina::Portrait of a Man": "Antonello da Messina - Portrait of a Man - National Gallery London.jpg",
    "robert-campin::Werl Triptych": "Werl-Triptychons.jpg",
    "robert-campin::Nativity": "La Nativité, par Robert Campin.jpg",
    "robert-campin::Portrait of a Woman": "Robert Campin 012.jpg",
    "robert-campin::Seilern Triptych": "Triptych-with-the-entombment-of-christ-1822.jpg",
    "pontormo::Deposition from the Cross": "Jacopo Pontormo - Kreuzabnahme Christi.jpg",
    "pontormo::Visitation": "Pontormo-visitation-after-restorationRGB.jpg",
    "pontormo::Portrait of a Halberdier": "Pontormo (Jacopo Carucci) (Italian, Florentine) - Portrait of a Halberdier (Francesco Guardi?) - Google Art Project.jpg",
    "pontormo::Joseph in Egypt": "Jacopo Pontormo - Joseph in Egypt - WGA18079.jpg",
    "elisabetta-sirani::Timoclea Kills the Captain of Alexander the Great": "Sirani, Elisabetta - Timoclea uccide il capitano di Alessandro Magno - 1659.jpg",
    "elisabetta-sirani::Portia Wounding Her Thigh": "Elisabetta Sirani - Portia wounding her thigh.jpg",
    "elisabetta-sirani::Virgin and Child": "Sirani Virgin and Child.jpg",
    "elisabetta-sirani::Portrait of Vincenzo Ferdinando Ranuzzi as Cupid": "Sirani Vincenzo Ferdinando Ranuzzi.jpg",
    "tawaraya-sotatsu::Wind God and Thunder God": "Wind God and Thunder God Screens by Tawaraya Sotatsu hi-res.png",
    "tawaraya-sotatsu::Waves at Matsushima": "俵屋宗達《松島図》17世紀、フリーア美術館.jpg",
    "tawaraya-sotatsu::Sekiya and Miotsukushi Screens": "Genji screen 1.jpg",
    "al-wasiti::Abu Zayd before the Governor of Rahba": "Yahyâ ibn Mahmûd al-Wâsitî 001.jpg",
    "al-wasiti::The Pilgrims' Caravan": "Yahyâ ibn Mahmûd al-Wâsitî 005.jpg",
    "al-wasiti::A Village": "Yahyâ ibn Mahmûd al-Wâsitî 007.jpg",
    "al-wasiti::The Eastern Island": "Yahyâ ibn Mahmûd al-Wâsitî 002.jpg",
    "melchor-perez-de-holguin::Entry of Viceroy Morcillo into Potosí": "Entrada Virrey Arzobispo Morcillo.jpg",
    "melchor-perez-de-holguin::Saint Christopher": "Melchor Pérez Holguin - Saint Christopher - 2018.652.2 - Metropolitan Museum of Art.jpg",
    "melchor-perez-de-holguin::Saint Peter of Alcántara and Saint Teresa": "Melchor Pérez Holguín - Saint Peter of Alcántara and Saint Teresa - A1837 - Hispanic Society of America.jpg",
    "melchor-perez-de-holguin::Virgin of the Rosary": "Melchor Pérez Holguín - Virgin of the Rosary - 1994.37.3 - Dallas Museum of Art.jpg",
    "shin-yun-bok::Portrait of a Beauty": "Shin Yun-bok - A Beautiful Woman - Google Art Project.jpg",
    "shin-yun-bok::Dano Day": "Hyewon-Dano.pungjeong.jpg",
    "shin-yun-bok::Lovers under the Moon": "Hyewon-Wolha.jeongin-3.jpg",
    "shin-yun-bok::Sword Dance": "Hyewon-Ssanggeomdaemu.jpg",
    "arnold-bocklin::Isle of the Dead": "Arnold Böcklin - Die Toteninsel III (Alte Nationalgalerie, Berlin).jpg",
    "arnold-bocklin::Self-Portrait with Death Playing the Fiddle": "Arnold Boecklin-fiedelnder Tod.jpg",
    "arnold-bocklin::The Plague": "Arnold Böcklin - Die Pest.jpg",
    "arnold-bocklin::War": "Arnold Böcklin - Der Krieg.jpg",
    "arturo-michelena::Miranda in La Carraca": "Miranda en la Carraca by Arturo Michelena.jpg",
    "arturo-michelena::The Young Mother": "La Joven Madre 1889 by Arturo Michelena.jpg",
    "arturo-michelena::Charlotte Corday": "Arturo Michelena 03.JPG",
    "arturo-michelena::Penthesilea": "Arturo Michelena, Penthesilea, 1891.jpg",
    "alphonse-mucha::Gismonda": "Alfons Mucha - 1894 - Gismonda.jpg",
    "alphonse-mucha::Job": "Alphonse Mucha - Advertisment for Job cigarettes, 1896.jpg",
    "alphonse-mucha::The Seasons": "Alfons Mucha - The Seasons, 1896.jpg",
    "alphonse-mucha::The Slav Epic": "Apotheosis of the Slavs history - Alfons Mucha.jpg",
    "helene-schjerfbeck::The Convalescent": "Helene Schjerfbeck (1862-1946)- The Convalescent - Toipilas - Konvalescenten (32721924996).jpg",
    "helene-schjerfbeck::Wounded Warrior in the Snow": "Helene Schjerfbeck - Wounded Warrior in the Snow.jpg",
    "helene-schjerfbeck::Self-Portrait with Black Background": "Helene Schjerfbeck, Self-Portrait, Black Background, 1915.jpg",
    "helene-schjerfbeck::Girl with Blonde Hair": "Girl with Blonde Hair (SM 2463).png",
    "gwen-john::Self-Portrait": "Gwen John - Self-portrait (1902).jpg",
    "gwen-john::A Corner of the Artist's Room in Paris": "Gwen John - A Corner of the Artist's Room in Paris, 1907–1909, VIS.2576, Museums Sheffield.jpg",
    "gwen-john::Nude Girl": "Gwen John - Nude Girl.jpg",
    "gwen-john::Girl Reading at the Window": "Gwen John - Girl Reading at a Window, 1911, 421.1971.jpg",
    "joaquin-torres-garcia::Inverted America": "Joaquín Torres García - América Invertida.jpg",
    "joaquin-torres-garcia::Constructive Clock": "'Constructive Clock' by Joaquín Torres García , 1936. oil on canvas.jpg",
    "joaquin-torres-garcia::Portrait of Josep Pijoan": "(Barcelona) Retrat de Josep Pijoan - Joaquim Torres-Garcia - Museu Nacional d'Art de Catalunya.jpg",
}

# Works that must never carry an image. Imported from the resolver so the two
# tools cannot drift; see tools/fetch_artworks.py SUPPRESS for the reasoning.
from fetch_artworks import SUPPRESS                              # noqa: E402

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

FOLD_MAP = (("ı", "i"), ("œ", "oe"), ("æ", "ae"), ("ø", "o"), ("ß", "ss"),
            ("ł", "l"), ("đ", "d"), ("þ", "th"), ("ð", "d"))

def fold(s):
    """Lowercase, strip accents, reduce punctuation to spaces.

    Commons writes "Cézanne", "Şeker", "Œdipe", "Krøyer"; we write the same
    names without the marks. The old rule stripped non-ASCII outright, which
    turned "Şeker Ahmed" into the tokens "eker" and "ahmed" and matched
    neither.
    """
    s = (s or "").lower()
    for a, b in FOLD_MAP:
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()

def stem(t):
    """Crude English plural fold, so "Cloud Studies" matches "Cloud Study"."""
    if len(t) > 4 and t.endswith("ies"):
        return t[:-3] + "y"
    if len(t) > 4 and t.endswith("es"):
        return t[:-2]
    if len(t) > 3 and t.endswith("s"):
        return t[:-1]
    return t

def tokens(s, minlen):
    return [t for t in fold(s).split() if len(t) >= minlen]

def fname_of(url):
    return fold(cr.commons_file_title(url) or url.rsplit("/", 1)[-1])

def has_word(hay, words):
    """Whole-word (plural-insensitive) membership — not substring.

    Substring matching is what made "coin" (French for *corner*) mark
    Pissarro's "Les toits rouges, coin de village" as a reproduction object.
    """
    present = {stem(t) for t in hay.split()}
    return any(stem(w) in present for w in words)

def mentions(hay, own, *marker_lists):
    """Does `hay` carry one of these markers that our own title does not?

    Multi-word markers are matched as substrings, single words as whole words.
    Markers our own title already contains are skipped, so Corot's "Souvenir
    de Mortefontaine" is not read as a souvenir and Anna Ancher's "Sunlight in
    the Blue Room" is not read as a photograph of a room.
    """
    for markers in marker_lists:
        phrases = [m for m in markers if " " in m]
        words = [m for m in markers if " " not in m and not has_word(own, [m])]
        if has_word(hay, words) or any(p in hay and p not in own for p in phrases):
            return True
    return False

QS_LABEL = re.compile(r'QS:(?:P1476,|L)([a-z]{2,3})[,:]?\s*"([^"]*)"')

def english_titles(object_name):
    """English titles Commons *structurally* asserts for a file.

    Commons stores multilingual titles as `label QS:Len,"..."` inside
    ObjectName. An English label that disagrees with our title is real
    evidence of a different work; a French or Japanese one is not, because we
    cannot tell disagreement from translation.
    """
    return [v for lang, v in QS_LABEL.findall(object_name or "") if lang == "en"]

def title_terms(titles):
    """(distinctive, content, loose) terms for a work title and its aliases."""
    dist, content, loose = [], [], []
    for t in titles:
        clean = re.sub(r"\(.*?\)", " ", t)
        content += [x for x in tokens(clean, 3) if x not in FUNCTION_WORDS]
        dist += [x for x in tokens(clean, 4) if x not in STOP_WORDS]
        loose += [x for x in tokens(clean, 3)
                  if x not in STOP_WORDS and x not in FUNCTION_WORDS]
    return dist, content, loose

def any_in(terms, hay):
    return bool(terms) and any(t in hay or t in hay.replace(" ", "") for t in terms)

def all_words_in(terms, hay):
    present = {stem(t) for t in hay.split()}
    return bool(terms) and all(stem(t) in present for t in terms)

def any_word_in(terms, hay):
    present = {stem(t) for t in hay.split()}
    return bool(terms) and any(stem(t) in present for t in terms)

def match_verdict(url, artist_name, titles, meta=None, article_title=""):
    """Does this file depict *this artist's* *this work*?

      "confirmed"   — Commons' own metadata, or the Wikipedia article the
                      candidate came from, ties the file to both the artist
                      and the work.
      "unconfirmed" — the artist checks out, but nothing available names the
                      work either way. Usually a file page written in another
                      language: "Le berceau" for The Cradle, "Der Turm der
                      blauen Pferde" for The Tower of Blue Horses. A caller
                      holding independent evidence of the work's identity may
                      accept these; a caller holding nothing but a fuzzy
                      search hit may not.
      "rejected"    — positive evidence against.

    The rule this replaced read the filename only, and accepted on artist
    evidence OR work evidence. Both halves are now required, and both may be
    satisfied from Commons' ObjectName/Artist/Credit as well as from the
    filename — because in every one of the 20 confirmed mismatches, the file
    page said plainly what the file actually was.

    `meta` is what commons_meta() / cr.describe_from_imageinfo() returned. Do
    not call this at all when that lookup failed: empty metadata reads as
    "unconfirmed", which a caller may accept, whereas a request that timed out
    proves nothing and must produce no verdict of any kind. Both callers skip
    the candidate and set their `unverified` flag instead.

    ImageDescription is deliberately *not* consulted. It is free prose, and
    prose about the right painting is not evidence that this file is it: the
    Emily Carr postage stamp's description reads "the stamp depicts Carr's
    painting Big Raven", which would confirm the very file §14 excludes.
    """
    meta = meta or {}
    own = fold(" ".join(titles))
    fname = fname_of(url)
    object_raw = meta.get("object_name", "")
    surface = fname + " | " + fold(object_raw)
    ident = " | ".join([surface, fold(meta.get("artist", "")), fold(meta.get("credit", ""))])

    if mentions(surface, own, ROOM_WORDS, REPRO_WORDS, REPRO_PHRASES,
                PARTIAL_WORDS, PARTIAL_PHRASES):
        return "rejected"

    name_toks = tokens(artist_name, 4) or tokens(artist_name, 3)
    if not any(t in ident for t in name_toks):
        return "rejected"                       # no tie to the artist at all

    ours_self = any(m in own for m in ("self portrait", "selfportrait"))
    if ours_self != any(m in surface for m in SELF_MARKERS):
        return "rejected"                       # self-portrait / subject confusion

    dist, content, loose = title_terms(titles)
    if any_in(dist, surface) or (not dist and all_words_in(content, surface)):
        return "confirmed"
    if article_title:                           # the work's own Wikipedia page
        at = fold(article_title)
        if any_in(dist, at) or (not dist and all_words_in(content, at)):
            return "confirmed"
    for en in english_titles(object_raw):
        if any_in(dist, fold(en)) or any_word_in(loose, fold(en)):
            return "confirmed"
        return "rejected"                       # Commons asserts a different work
    return "unconfirmed"

def commons_meta(url):
    """What Commons says the file at `url` depicts.

    Raises cr.Unverified on anything that proves nothing — a timeout, a 429, a
    reset. Callers must treat that as "not checked", never as "not a match"
    (PIGMENT.md §14; tools/commons_rights.py rule 1). Pacing and backoff are
    commons_rights' MIN_INTERVAL/BACKOFF; this adds none of its own.
    """
    title = cr.commons_file_title(url)
    if not title:
        raise cr.Unverified("not a Wikimedia Commons file URL")
    d = cr.api_get_json(cr.API + "?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "titles": title}))
    pages = ((d.get("query") or {}).get("pages")) or []
    if not pages or pages[0].get("missing"):
        raise cr.Unverified("no file page returned for " + title)
    cr.capture_from_imageinfo(RIGHTS, pages[0])
    return cr.describe_from_imageinfo((pages[0].get("imageinfo") or [{}])[0])

def wiki_summary(title):
    q = urllib.parse.quote(title.replace(" ", "_"))
    try:
        return get_json("https://en.wikipedia.org/api/rest_v1/page/summary/" + q)
    except Exception:
        return None

def try_wiki(cands, artist_name, titles):
    """Resolve via the work's own English Wikipedia article.

    Returns (art, unverified). This path carries evidence the Commons search
    path does not: we asked Wikipedia for a *named work* and got a standard
    article back, so the article establishes which work the lead image belongs
    to. What it cannot establish is whose work it is — that is exactly how
    "Irises (painting)" supplied Van Gogh's canvas for Ogata Korin. So the
    article stands in as work evidence and the artist evidence is checked
    against Commons.
    """
    name_toks = tokens(artist_name, 4) or tokens(artist_name, 3)
    unverified = False
    for cand in cands:
        s = wiki_summary(cand); time.sleep(0.06)
        if not s or s.get("type") != "standard":
            continue
        thumb = (s.get("thumbnail") or {}).get("source", "")
        if "/wikipedia/commons/" not in thumb:
            continue
        text = fold((s.get("description") or "") + " " + (s.get("extract") or ""))
        if any(w in text for w in NOT_ART) and not any(w in text for w in ART_WORDS):
            continue
        if not (any(w in text for w in ART_WORDS) or any(t in text for t in name_toks)):
            continue
        img = cr.strip_tracking(re.sub(r"/\d+px-", "/500px-", thumb))
        try:
            meta = commons_meta(img)
        except cr.Unverified as ex:
            unverified = True                          # a throttle is not a finding
            print(f"      unverified ({ex}); {cand} left unjudged", flush=True)
            continue
        if match_verdict(img, artist_name, titles, meta, s.get("title", "")) != "confirmed":
            continue
        page = ((s.get("content_urls") or {}).get("desktop") or {}).get("page", "")
        return {"img": img, "page": cr.strip_tracking(page)}, unverified
    return None, unverified

def try_commons(queries, artist_name, titles):
    """Resolve via Commons full-text search.

    Returns (art, unverified). Nothing here establishes which work a hit
    depicts — Commons ranks "Lucas Cranach ... Sibylle von Cleve" highly for
    the query "Adam and Eve Lucas Cranach" because the artist name matches
    hard. So a hit is accepted only on a "confirmed" verdict; "unconfirmed"
    gets no benefit of the doubt on this path.
    """
    unverified = False
    for q in queries:
        u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
             "&generator=search&gsrnamespace=6&gsrlimit=8"
             "&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=500"
             "&gsrsearch=" + urllib.parse.quote(q))
        try:
            d = get_json(u)
        except Exception as ex:
            unverified = True                          # the search never ran
            print(f"      unverified ({ex}); query {q!r} left unjudged", flush=True)
            continue
        time.sleep(0.06)
        pages = (d.get("query") or {}).get("pages") or {}
        for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            ii = (p.get("imageinfo") or [{}])[0]
            url = cr.strip_tracking(ii.get("thumburl", ""))
            if not ii.get("mime", "").startswith("image/") or not url:
                continue
            if ".djvu" in url.lower() or ".pdf" in url.lower():
                continue
            # extmetadata rode along on the search query; no extra request.
            meta = cr.describe_from_imageinfo(ii)
            if match_verdict(url, artist_name, titles, meta) == "confirmed":
                cr.capture_from_imageinfo(RIGHTS, p)
                return {"img": url,
                        "page": cr.strip_tracking(ii.get("descriptionurl", ""))}, unverified
    return None, unverified

def main():
    artists = {a["id"]: a for a in json.load(open("/tmp/pigment-artists.json"))}
    src = open("js/artworks.js").read()
    head, tail = src.split("window.ARTWORKS = ", 1)
    data = json.loads(tail.rstrip().rstrip(";"))

    flagged, fixed, kept, dropped, unverified = [], [], [], [], []
    for aid, works in data.items():
        a = artists[aid]
        name_toks = tokens(a["name"], 4) or tokens(a["name"], 3)
        for title in list(works):
            key = f"{aid}::{title}"
            if key in SUPPRESS:                            # must never carry an image
                del works[title]
                dropped.append(key + "  (suppressed: " + SUPPRESS[key] + ")")
                print(f"  {key} -> SUPPRESSED", flush=True)
                continue
            if key in PINNED:                              # hand-curated: resolve exact file, skip search
                u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
                     "&iiprop=url|mime|extmetadata&iiurlwidth=500&titles="
                     + urllib.parse.quote("File:" + PINNED[key]))
                try:
                    p = list(get_json(u)["query"]["pages"].values())[0]
                    ii = p["imageinfo"][0]
                    cr.capture_from_imageinfo(RIGHTS, p)
                    works[title] = {"img": cr.strip_tracking(ii["thumburl"]),
                                    "page": cr.strip_tracking(ii["descriptionurl"])}
                    print(f"  {key} -> PINNED", flush=True)
                except Exception as ex:
                    print(f"  {key} -> PIN FAILED ({ex}), kept", flush=True)
                time.sleep(0.2)
                continue
            entry = works[title]
            titles = [title] + TITLE_ALIASES.get(key, [])
            page_l = fold(urllib.parse.unquote(entry.get("page", "")))
            suspect = key in OVERRIDES \
                or any(b in fname_of(entry["img"]) for b in ROOM_WORDS) \
                or (not any(t in fname_of(entry["img"]) for t in name_toks)
                    and not any(t in page_l for t in name_toks))
            if not suspect:
                continue
            flagged.append(key)
            clean = re.sub(r"\s*\(.*?\)", "", title).strip()
            surname = a["name"].split()[-1]
            cands = OVERRIDES.get(key, []) + [
                f"{clean} ({surname} series)", f"{clean} ({surname})", f"{clean} (painting)"]
            art, unv = try_wiki(cands, a["name"], titles)
            if not art:
                art, unv2 = try_commons(
                    [f"{clean} {a['name']} painting", f"{clean} {a['name']}"], a["name"], titles)
                unv = unv or unv2
            if art and art["img"] != entry["img"]:
                works[title] = art; fixed.append(key)
            elif art:
                kept.append(key + "  (same image reconfirmed)")
            elif unv:
                # Something we could not reach declined to answer. Deleting the
                # record here would turn a 429 into a verdict (PIGMENT.md §14).
                unverified.append(key); kept.append(key + "  (unverified, kept)")
            else:
                del works[title]; dropped.append(key)
            print(f"  {key} -> {'FIXED' if key in fixed else 'DROPPED' if key in dropped else 'UNVERIFIED (kept)' if key in unverified else 'kept'}", flush=True)

    print("\nHealth-checking all URLs (politely)...", flush=True)
    dead, unknown = 0, 0                                   # unknown: throttled, kept
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
    if RIGHTS:
        cached = cr.save_sidecar(RIGHTS)
        print(f"rights captured this run: {len(RIGHTS)} (cache now {cached}) -> {cr.sidecar_path()}")
    total = sum(len(v) for v in data.values())
    print(f"\nDONE flagged:{len(flagged)} fixed:{len(fixed)} dropped:{len(dropped)} "
          f"unverified-kept:{len(unverified)} dead:{dead} unknown-kept:{unknown}")
    for key in unverified:
        print("  UNVERIFIED (kept, not a finding)", key)
    print(f"final: {len(data)} artists, {total} works")

if __name__ == "__main__":
    main()
