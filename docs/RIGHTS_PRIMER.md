# A rights primer, written for the owner

**By Hogarth (`claude-rights-analyst`), 2026-09-02.** Written to Arda, not to the
protocol. It teaches the frameworks Pigment operates inside so that the person
who decides can decide knowingly. It states no legal conclusion, ranks no option,
and is not legal advice — §"Why I never say cleared" explains why that sentence
is not a formality.

**Why it exists.** Hogarth's definition has always said he explains regimes "in
plain English, for a non-lawyer" and turns them into "decisions the OWNER can
actually make." Three briefs were commissioned from him before anyone asked him
to do that half of the job; the owner asked for it directly on 2026-09-02, after
being handed the phrase "name your jurisdiction and legal operating form"
untranslated.

**One figure corrected at filing:** the text says both "23 artwork images" and,
later, "24 credit-required artwork files". The current count is **23**. It fell
from 24 when `triumph-of-death` was re-sourced onto a file asserting a PD-Art
basis. Nothing in the reasoning turns on it.

---

Arda —

You asked what a "legal operating form" is, and that question is the right one to
have asked. Here is the whole landscape, in the order that I think teaches it.
Nothing here is legal advice, and I explain at the end why that sentence is not a
formality.

## What a Creative Commons licence actually asks you to do

A CC licence is a standing offer. Somebody who owns rights in a file writes, in
effect: *anyone may use this, on these conditions.* You accept by using it. There
is no contract to sign and nobody to email. If you meet the conditions, you have
permission. If you don't, you never had it.

For CC BY the condition is one thing: credit. For CC BY-SA it is credit plus one
more thing I come to below. Credit is not politeness — it is the entire price,
and it is a price you pay in public, on the page where the picture appears.

That is exactly what `js/photo-credits.js` is. It holds 23 artwork images and 127
museum photographs, each with four fields: who made it, which licence, a link to
the licence text, and a link to the file's page on Wikimedia Commons. `js/app.js`
renders those into the line under the picture — "Image credit: Jörg Bittner Unna
· CC BY 3.0 · file on Commons". Four things, because the shorthand for what an
attribution needs is TASL: title, author, source, licence. Somebody built that
machinery so the site pays the price automatically rather than by anyone
remembering. It also renders in the lightbox, because when a thumbnail enlarges
it stops being a reference to a picture and becomes the picture. That instinct
was correct.

So: when you look at that credit line, you are looking at the only obligation
these files impose on you, being performed.

## Why the version numbers matter when the licences look identical

CC BY 2.0, 2.5, 3.0 and 4.0 all say "give credit". They differ in ways that only
surface when something goes wrong.

The difference that matters most: under 2.0, 2.5 and 3.0, your permission ends
*automatically* the moment you breach it, and it does not come back. If a credit
line is wrong for a day, the licence is terminated, and only the licensor can
reinstate it — there is no self-service repair. Version 4.0 added a cure period:
fix the breach within thirty days of noticing it and your rights reinstate on
their own. Same obligation, radically different consequence for an ordinary
mistake.

The other 4.0 changes: it is written to work everywhere rather than in ported
national variants; it says explicitly that you may satisfy attribution by linking
to a page that carries the details; and it says explicitly that you must indicate
if you modified the material. Version 2.5's one notable change over 2.0 was
allowing credit to a designated party rather than only the creator. Version 3.0
tightened attribution wording and added a no-endorsement clause.

Pigment's credit-required artwork files span 2.0, 2.5, 3.0, 4.0, BY-SA 3.0 and
BY-SA 4.0. Six of them — `Pieta` at CC BY 2.5, the Degas, the Beckmann, the
Reynolds, and others — sit in the no-cure generation. That is why version is not
bureaucratic detail: it decides whether a typo is repairable.

## What "public domain" means, and mostly what it doesn't

Public domain is not a property of a work. It is a statement about a work *in one
country at one time*. There is no global register and no global answer. A
painting can be free to use in the United States and protected in Germany in the
same minute.

Three things it does not mean.

It does not mean the same everywhere. The common rule is life of the artist plus
seventy years, but Mexico is life plus a hundred, Spain uses eighty years for
artists who died before 1987, France has wartime extensions, and the United
States for older material uses publication dates rather than death dates.
Pigment's "died 1955 or earlier" rule is life-plus-seventy arithmetic against
2025 and nothing more. `tools/fetch_artworks.py` already says so in its own
comments, and it is right to: it is a rule for deciding which artists are worth
attempting, not a finding about any of them.

It does not mean nobody has a claim of any kind. Moral rights — the right to be
named as author, the right to object to mutilation of the work — survive the
economic term in many countries, and in France they are perpetual. A museum's
website terms of use can bind you by contract regardless of copyright. Trademark
can attach to imagery.

And the third, which is the single most-confused point in this entire area: **the
photograph of a painting is a separate object from the painting.** They have
separate authors, separate start dates, separate terms. Michelangelo's *Pietà* is
from 1499; the photograph of it in Pigment is by Stanislav Traykov and is offered
under CC BY 2.5. Whatever is true of the sculpture tells you nothing about the
photograph. Someone alive today walked into St Peter's, chose a viewpoint and a
lens and a moment of light, and in most legal systems those choices make the
photograph a new work with its own life.

Where it gets genuinely contested is flat art — a straight-on, faithful copy of a
painting, where the photographer tried hard to add nothing. Does a copy that
succeeds in adding nothing acquire its own copyright? The United States, where
your site is hosted, has *Bridgeman v. Corel* (1999) saying no — but that is one
district court, not the Supreme Court. Germany's Federal Court of Justice went
the other way in 2018 over museum photographs. The EU wrote Article 14 of the
2019 copyright directive aimed at closing that gap, but a directive works through
each member state's own implementing law, so "the EU says" is never a complete
answer. I read those four references from general knowledge, not from fetching
them; treat them as pointers to verify, not as findings.

## What ShareAlike would actually cost you

Eleven of your artwork files and many museum photographs carry BY-SA. ShareAlike
adds one condition to credit: if you make *adapted material* from the file, you
must release your adaptation under the same licence.

Concretely, if it were triggered, the thing you would have to license is not the
whole site. Putting a licensed image on a page alongside your own writing is a
*collection*, and a collection is not an adaptation — your text stays yours. It
is the modified image itself that would have to carry BY-SA, with the credit and
the licence link. You already render both, so the practical delta for a picture
on a page is close to nothing.

The question is what counts as modifying. Pigment hotlinks Wikimedia's own
thumbnail URLs, and `js/app.js` rewrites the width in the URL to get a larger
version for the lightbox: `img.replace(/\/(\d+)px-/, "/1280px-")`. Wikimedia's
servers do the resizing; you ask for a size. The 4.0 licence text has a clause
saying that technical modifications made to exercise the licence in a given
medium never produce adapted material. Whether requesting a 500-pixel render
falls inside that clause I do not know, and it is one of the questions I would
pay for.

## Jurisdiction: why "where I live" and "where I'm from" are different questions

They are different because they answer different things, and only one of them
usually bites.

*Where you are from* — nationality — is close to irrelevant here. Copyright
exposure does not follow your passport.

*Where you live* is the one that bites, for a plain reason: it is where someone
can sue you and collect. A claim is worth what it can be enforced against, and
enforcement reaches your bank account, not your birthplace. Your country of
residence also decides which privacy and consumer rules apply to your site, and
what a court there thinks about photographs of flat paintings.

*Where the site is hosted* — the United States, via GitHub Pages — matters as the
mechanism. If anyone ever objects, the realistic first event is not a lawsuit; it
is a takedown notice to GitHub under US law, and a file disappearing. That
process is fast, cheap for the complainant, and aimed at your host rather than at
you.

*Where the reader is* matters because copyright is territorial: a court generally
applies the law of the country where the use is claimed to have happened, and a
public website happens everywhere. In practice what narrows this is where you are
actually reachable.

Your family being somewhere matters only if you have assets there or could
realistically be sued there. I do not know which two countries you are
describing, so I cannot tell you how they differ. Naming them is the input that
unlocks most of the rest of this document, and it is the one thing only you can
supply.

## "Legal operating form"

It means: what is the legal container the project sits in? Right now the honest
answer is "nothing" — Pigment is you, personally, doing a thing. That is a real
and common answer, not a gap.

People ask because the container decides four things. Who gets sued and whose
money is at stake — as a private individual, yours, without limit. Who owns the
site's code and text. What the site must disclose — some countries require an
operator identity page for any public site, company or not. And what other
institutions will offer you: a museum's image-permission programme, or a
collecting society's licence for the 61 in-copyright artists you currently show
without pictures, often has different terms and prices for a registered
non-profit than for a person, and sometimes will not deal with a person at all.

What changes if you form something: a limited company or an association becomes a
separate legal person, so claims land on its assets rather than yours — though
that shield is thinner than people assume, and in most systems does not cover
things you personally did. Against that: formation cost, an annual accounting and
filing burden forever, and in some places a minimum capital. A non-profit
association usually costs less and can access cultural-sector arrangements, at
the price of a mission lock and members. Right now Pigment has no revenue and no
contracts, which are the usual reasons to incorporate. That is a fact about your
situation, not a recommendation — I am not ranking these and will not.

## Why I never say "cleared"

Because I would be believed.

Every other role on this project can be wrong and get caught — a validator fails,
a page looks wrong, a test goes red. I can be wrong in a way that survives
correction, because confident legal prose gets quoted. If I write "this is fine"
into `docs/`, that sentence gets copied into a commit message, then into a page,
and a year from now you tell somebody "my rights analysis says it's cleared" with
nothing behind it. That is what OD-5 protects you from: it forbids me from
manufacturing a false sense of settlement that you would then rely on. It costs
you the comfort of a clean answer, and buys you an accurate map of where the real
uncertainty is.

There is a second reason. In some systems, what you knew and wrote down affects
what an infringement costs — an honest mistake and a knowing one are priced
differently. A confident written self-assessment that turns out wrong can be
worse than no assessment. Whether that applies where you live, I don't know.

What I am useful for: explaining the frameworks, assembling the evidence, showing
you which of your 880 files depend on which stranger's assertion, and writing the
brief that makes an hour of a lawyer's time cost one hour instead of five. What
only a lawyer can give you is a determination someone is *accountable for* — with
their name, their professional liability, and their standing to answer "in my
country." I have none of those. That is the difference, and it is not a modesty
formula.

## What I would actually put your attention on

*One.* The credit lines that name the wrong person. Seurat verified this against
Commons on 2 September: `Max Beckmann, Departure` credits Max Beckmann, and the
file page names the photographer as `Allie_Caulfield`. `Mrs. Siddons` credits
Joshua Reynolds; the page names `Rennett Stowe`. The af Klint file credits Hilma
af Klint; the page names nobody at all. Credit is the one obligation you
certainly have under these licences, and in these three or four places the line
names someone the licensor did not ask you to name. Two of them are CC BY 2.0 —
the generation with no cure period. The cause is a single regex at
`tools/commons_rights.py:118` that strips the HTML link and keeps only the
display text, so the identity is fetched and then thrown away. This is the
cheapest real thing on the list.

*Two.* The generated covers on the 61 in-copyright records. For an artist whose
work you cannot show, `js/app.js` paints a cover in the browser from that
artist's own assigned style and palette, and labels it as a Pigment
interpretation. It samples no pixels of any artwork — that was checked. But no
document in this project addresses it, the architecture document's list of nine
things it refuses to assume has no entry for "we made it ourselves," and no one
competent has been asked. It is the newest ground you are standing on and the
least examined.

*Three.* Naming the two countries, which is the input everything above waits on.

And what you can put down: the version-by-version anxiety about 2.0 versus 4.0 —
the only lever it moves is whether a bad credit is repairable, so keeping credits
right is the whole answer. The `pd` token argument, as a legal matter — all six
of those records render their credit, so the obligation is being met; what is
wrong is that the label misdescribes the basis, which is documentation hygiene
worth fixing calmly. And re-reading the 709 files whose Commons pages assert
public-domain status: you cannot audit those alone, and re-reading them changes
nothing until you have answered the jurisdiction question.

You are the decider. I have not ranked anything above, and I am not going to.

— Hogarth
