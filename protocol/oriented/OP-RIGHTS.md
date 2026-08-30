# OP-RIGHTS

**Prefix:** `RIGHTS-` · **Lead:** Hogarth (`claude-rights-analyst`)

## The question it answers

> On what basis may Pigment show this, and what does the owner need to decide?

Not "is this allowed." The protocol is named **Rights**, not Legal, and the
distinction is load-bearing. OD-5 forbids this project from stating clearances,
and a protocol called "Legal" invites exactly the determinations it must never
make. "Rights" is also already the vocabulary of the schema, the census and the
credits registry.

## Standing constraints

OD-5 binds absolutely and is not waivable inside this OP by any finding, any
deadline, or any agent's confidence:

- Record **asserted basis and residual uncertainty, never clearance.**
- Name the jurisdiction every time. "Life plus 70" is not a global boolean.
- A hosting policy is not a determination. What Wikimedia Commons permits on
  its own servers is a statement about Commons.
- Distinguish **the work** from **the photograph of the work**, always. They
  have separate authors, separate terms, and can be in opposite states.
- Death-year arithmetic is a heuristic, not a finding.
- Where the answer is unknown, say "I don't know" in those words.

The banned-phrase guard (`tests/test_rights_tooling.py::TestProseLanguage`)
scans `docs/`, `tools/`, `tests/`, `js/app.js` and `protocol/oriented/`. Prose
produced by this OP is subject to it like any other. Exemption markers are
pinned; adding one is a reviewable act, never a quiet edit.

## Write scope

**May write**

| Path | Condition |
|---|---|
| `docs/*.md` | rights documents and schema sections |
| `protocol/tasks/RIGHTS-*/` | its own task artifacts |
| `protocol/oriented/OP-RIGHTS.md` | this file |
| `js/catalog-*.js` | **the `image:{}` block only** — `src`, `page`, `status` |
| `js/photo-credits.js` | via `tools/build_photo_credits.py` only, never by hand |
| `protocol/tasks/PIG-001/evidence/*rights*.json` | via `tools/audit_artwork_rights.py` only |
| `tests/test_rights_tooling.py` | guards, ledgers, ratchets |
| `p/**`, `sitemap.xml` | via `tools/build_seo.jxa.js` only, when an image URL changed |

**May not write**

- Any catalog field other than `image:{}` — not `description`, `notice`,
  `tags`, `tier`, `coords`, `related`. A rights decision that needs prose
  changed asks OP-CONTENT.
- `css/`, `index.html`, or rendering logic in `js/app.js`. A rights decision
  that needs a new UI state asks OP-INTERFACE and records the dependency.
- `js/taxonomy.js`, `js/influences.js`, `js/artists-*.js`, `js/lists-*.js`.
- The Lane III sealed set, in Lane III.

Two paths are marked *generated*: `js/photo-credits.js` and the rights census.
Hand-editing either produces a file its generator would not reproduce, which is
the precise class of drift this project's guards exist to catch.

## Agents

| Agent | Role in this OP |
|---|---|
| **Hogarth** | Lead. Frames questions, assembles evidence, drafts counsel briefs, states no conclusion and decides nothing |
| **Seurat** | Data integrity across records and census; verifies a claimed basis against the file it describes |
| **Dürer** | The only code-writing role: schema tokens, guards, tool runs |
| **Van Eyck** | Independent review; never certifies work it implemented |
| **Caravaggio** | Opposition, on request, where a proposed basis looks convenient |

Consultation outside this set is evidence, not authority.

## Acceptance criteria

A RIGHTS task may reach `human_review_ready` only when all hold:

1. Every claim names **what asserts it** and **where** — a file page, a licence
   template, a statute, a census entry — with the assertion distinguished from
   the assertor's authority to make it.
2. Every jurisdiction-dependent statement names its jurisdiction.
3. Residual uncertainty is stated in the artifact, not only in conversation.
4. Any new counted guard is proved non-vacuous by deliberately breaking it, and
   the break is recorded.
5. Any inventory or census drift is **declared in its ledger** before the suite
   is made to pass. A ceiling is never raised to accommodate a finding.
6. `tools/validate.jxa.js` exits 0 and the suite passes.
7. Where an image changed, the prerendered stubs were re-emitted in the same
   commit — `og:image`, `twitter:image` and the JSON-LD `image` must not lag the
   data.
8. The artifact ends in an **owner decision or a counsel brief**. Never a
   clearance, and never a recommendation dressed as a finding.

## Failure modes this OP exists to prevent

Each of these has already happened once in this repository, which is why they
are written down rather than assumed.

- **A proxy checked for the thing.** A census summary read instead of the file
  page; a regex matching `{{PD-old}}` inside a malformed `{{self}}` block and
  reporting a clean basis. Open the file.
- **A count that fell for the wrong reason.** Swapping a URL the census has
  never seen drops a record from a guard's tally without changing anything real.
  Regenerate the evidence, then read the count.
- **Metadata lagging data.** The record changed; the stub page kept serving the
  old file in `og:image`, where the public actually sees it.
- **Filename trust.** Titles and filenames misdescribe their images in both
  directions — a crop tagged as the whole, a whole tagged as a detail, a photo
  of a wall label passing as the work. Look at the pixels.
- **Ranking by the wrong axis.** The largest file in a Commons category may
  carry `{{superseded}}` and point at a better one.
