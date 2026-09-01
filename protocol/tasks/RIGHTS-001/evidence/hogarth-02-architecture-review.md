# Hogarth — review of `docs/ARTWORK_SOURCES_COPYRIGHT_ARCHITECTURE.md`

**Provenance.** Produced by `claude-rights-analyst` (Hogarth) on owner
instruction during Lane II session work on 2026-08-30, **before RIGHTS-001 was
opened**. Not routed through the Coordinator, no message envelope, no liaison
audit. Filed here unaltered because the round-two request to the Theory Team
enumerates five weaknesses drawn from it, and the task record should contain the
analysis it acts on.

**Two claims in it were checked afterwards and both held.** The GESAM reference
could not be located in a search of visual-arts collecting societies, and the
generative covers were confirmed present in `js/app.js` (`canvasTag`) — see
decision record E-001, which narrows the finding: the covers draw on Pigment's
own hand-authored palette assignment for the artist, and sample no artwork
pixels.

---

**The decision the owner faces:** whether to adopt this document's model as
Pigment's rights architecture, or take only its vocabulary and leave its
machinery. I do not rank those.

**1. Where it holds and where it is loose.** It holds where it refuses
inference. "API availability is an ingestion signal—not a rights grant" is the
same discipline this repo already applies to Commons — a hosting policy is not a
determination, and neither is an API response. §9's non-assumptions are sound,
particularly "Notice-and-takedown is a safety process, not a licensing
strategy." The strongest legal sentence in it is in Tier C.2: "Buying or
obtaining a photograph does not automatically clear the artwork reproduced in
it."

It is loose on jurisdiction, which its own header promises to defer. "In the
European Union, Article 14 of Directive (EU) 2019/790 limits new copyright or
related rights in non-original reproductions of public-domain visual art" fairly
describes the article's effect, but a directive binds through each member state's
transposition, not directly; it reaches neither the United States, where GitHub
Pages hosts this site, nor the post-Brexit United Kingdom. The document never
names whose exposure it is modelling — the owner's country, the host's (US), or
the reader's — and that is exactly the open question it would need to answer to
be usable here.

It is overstated at R1, which collapses "CC BY, CC BY-SA, or a clear
institutional licence" into one policy. Version is load-bearing: CC BY and BY-SA
2.0, 2.5 and 3.0 terminate automatically on breach with no cure period; 4.0 adds
a thirty-day cure. Pigment's twenty-four credit-required files span 2.0, 2.5,
3.0, 4.0, BY-SA 3.0 and BY-SA 4.0, so one tier with one rule is under-specified
for the set it would govern. "Enforce adaptation and ShareAlike constraints where
applicable" also asserts the obligation without stating what triggers it —
whether a resized thumbnail is an adaptation is the question ShareAlike turns on,
and it goes unasked.

**2. Does the framework fit the pd-token problem.** The three-layer cut is right
in principle, and Pigment partly makes it already: `docs/ARTWORK_SCHEMA.md` §3
documents `status` as a rendering token, and the evidence lives outside the
record in `protocol/tasks/PIG-001/evidence/artwork-image-rights.json` with
credits generated into `js/photo-credits.js`.

It does not decide the six. The model files a CC BY 2.5 photograph of
Michelangelo's *Pietà* and a CC BY-SA 4.0 file of af Klint's *The Ten Largest,
No. 9* in the same R1 bucket, and the entire difference between them is the
distinction the document never draws: whether the media asset carries any
copyright of its own. A photograph of a sculpture — *Pietà*, *David*, Degas's
*Little Dancer* — is a new work by a living author who chose viewpoint and light.
A flat reproduction of a Hokusai print or an af Klint canvas is the case Article
14 addresses in member states that transposed it, and separately what US
flat-copy reasoning addresses. Same tier, opposite reasoning. Adding a
`media_rights_status` field renames the question.

For `the-ten-largest-no-9` the model would actively conceal the problem. A bare
CC tag naming no licensor populates `licence_uri` and satisfies R1's schema while
leaving open whether the tagger had standing to license anything; the best-tagged
alternative carries "© Stiftelsen Hilma af Klints Verk" inside a file tagged
PD-Art. Two assertions by strangers, in conflict, on a painter who died in 1944.
R4 catches that only if a human already noticed the conflict — which is the work,
not the framework.

**3. Insight versus engineering in legal clothing.** Genuine: the ADAGP
two-rights point; "Display permission must not be repurposed as training
permission"; §4's refusal to promise deletion from backups and its split between
prospective withdrawal and already-valid third-party uses; §9 entire. Engineering
wearing legal clothes: most of §6 and §7 — evidence snapshots, versioned
adapters, immutable decision events, deny-by-default renderer, scheduled
revalidation, kill switch. Sound provenance practice, not law, and it presumes a
database, a server, and hosted bytes. Pigment has none: no build step, no
backend, and all 337 catalog image sources hotlink `upload.wikimedia.org`.
`storage_object_key`, `quarantined_at`, `offline_cache_allowed` and suppression
"from caches" describe a system this is not. The runtime policy engine here is a
two-value literal read by `js/app.js`; the kill switch is a commit.

**4. Asserted as fact, worth checking before reliance.** The Met's "more than
492,000 public-domain images" is undated. The per-source characterisations of
Met, Rijksmuseum, Smithsonian and Art Institute reflect policies that change.
"GESAM" I could not place among collecting societies — ADAGP, DACS and ARS
exist; GESAC is a Brussels umbrella that licenses nothing — and a fabricated
licensor in a licensing plan is worth catching early. Whether the Europeana Data
Exchange Agreement binds a reuser or only a contributing institution. And Article
14 as actually transposed in whichever state governs.

**5. What it omits that matters here.** Hotlinking versus hosting as legally
distinct acts — the whole document assumes Pigment stores files. The 61
`status:"copyright"` records and their generative covers: §9's list has no entry
for "we generated it ourselves," and the document is silent on style-imitation,
which is Pigment's most novel exposure and least settled ground. The artist's
moral and attribution rights as distinct from the photographer's credit. OD-5:
the document says "clearance rates" and "cleared its artwork rights," language
the repository's guard rejects, so its vocabulary cannot be imported unedited.
And scale — 127 Tier 1 records, ~750 audited images, one owner. A five-tier
review queue is a staffing model, unstated.

**6. What I do not know.** I don't know which jurisdiction governs the owner's
exposure, or whether the answer differs for owner, host and reader. I don't know
whether a resized thumbnail is an adaptation under CC BY-SA. I don't know who
applied the af Klint tag or whether they had standing. I don't know whether
Stiftelsen's © notice claims the work, the photograph, or is house boilerplate.
Those four are what I would put to counsel, with the census already assembled so
no one pays for reading time.
