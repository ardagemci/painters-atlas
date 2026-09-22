# Owner-led loop study

## Goal and limits

Run five observed sessions before expanding the Persona set, following PIGMENT.md §16 priority 2. Examine whether a new visitor can complete Discover → Admire → Map → Become, recognise something of their taste in the result, discover another work, and return to their Passport. This kit adds no instrumentation; the owner moderates and keeps manual notes. Instrumentation remains a separate owner decision (§16 priority 8).

Five sessions can expose obstacles, confusing language, recovery failures and differences between intended and understood behavior. They cannot establish general enjoyment, population completion rates, recommendation accuracy, long-term retention or demand for sharing. Report “3 of these 5 participants,” not a population percentage. Expressed enthusiasm is a quote, not proof of product fit.

Basis: PIGMENT.md §§3, 8, 9, 16; docs/ADMIRE_SPEC.md; current js/app.js functions viewPalette, obHandoff, viewTaste and passportActions. The current onboarding uses four tones, sixteen Admire/Pass decisions and five questions, then a provisional map and three Persona candidates. The deck is selected up front, not response-adaptive. Results offer matched artists and a list; the taste page has Discovery rings with artwork cards. Do not promise a museum route or an immediate large change in the map after one admiration.

## Participants and recruiting

Recruit five adults who are curious about paintings and have not used this build or helped design it. Include people who do not know art terminology, a range of museum/art familiarity, and visitors interested in modern as well as older work. Avoid recruiting only the owner's fellow builders or art experts. Aim to include both phone and desktop use and, where feasible, someone's usual keyboard or assistive-technology workflow. Five people cannot cover every accessibility need; record the gaps.

Invitation: “Would you spend about 25–30 minutes trying a small art website while I watch how it works for you? No art knowledge is needed. You can stop at any time.” Do not promise a flattering or accurate personality result. Keep scheduling details outside the repository. Use anonymous session labels S1–S5, not names or identifying biographical descriptions. Record only broad prior familiarity if needed to interpret an obstacle.

## Owner setup

1. Choose one build for all five sessions. Note its commit, any uncommitted changes, date, browser/version, viewport, input method and theme in private session notes. If an urgent repair changes the build, label subsequent sessions as a new version; do not pool them silently.
2. From the repository root, serve with `python3 -m http.server 8421 -d .`. Open `http://localhost:8421/` in a dedicated study browser profile. Keep the hostname and port constant because storage is origin-specific. Images are requested from external sources; verify ordinary image loading before the participant starts.
3. Before **each** session, clear this study origin's localStorage and sessionStorage (onboarding progress can resume from sessionStorage), close other study tabs, and reload the homepage. In the study tab's developer console: `localStorage.clear(); sessionStorage.clear(); location.href = '/';`. Do this only in the dedicated profile, not a participant's personal Pigment session. Confirm no previous Passport appears.
4. Prepare a stopwatch and the results template below. No analytics installation, event hooks, account creation or code changes are required. Perform one owner rehearsal to confirm labels and links; a rehearsal is not a participant session.
5. Ask about needed display/input accommodations. Let participants use their normal interaction method. Note image delays or failures separately from navigation confusion.

## Moderator opening — read aloud

“Thank you. We're testing the website, not you. There are no correct art preferences. Please say what you're looking for, what you expect, and anything that surprises you. Use it as you normally would; you may pass on paintings and choose not to adopt a Persona. I may stay quiet so I can see what the page communicates. You can pause, skip a task or stop whenever you like. I'll take anonymous notes. I will not record your voice or screen unless you separately agree.”

Obtain consent for observation and notes. No recording without explicit consent; declining recording does not exclude participation. Explain any agreed recording's storage, access and deletion date before starting.

## Task script and timing

Read one task at a time. Keep the expected path column for the moderator; do not read it as navigation instructions. Start each task clock at the end of its spoken instruction. Mark first action, completion, stalls, wrong turns, help and abandonment. Preserve raw elapsed time and separately annotate moderator interruptions or technical loading pauses. Think-aloud timing is not natural-use timing.

| Step | Exact participant task | Moderator observation and endpoint |
| --- | --- | --- |
| 1. Entry | “Starting here, find how to discover what this site says about your taste in art.” | Start on homepage. Observe discovery of Find your palette / Taste. Stop when onboarding introduction is reached. If lost, record before rescue. |
| 2. Onboarding | “Go through this experience using your own preferences until you reach your first result.” | Expected: Begin → four tones → To the deck → sixteen Admire/Pass choices → five questions → Your first map. Time Begin to first map, plus tone, deck and question stages separately. Record hesitation, accidental choices and understanding of Pass. The under-four-minute target is a diagnostic comparison, not a participant deadline. |
| 3. Result and Passport | “Take a look at your result. Tell me what it says about you. Decide what you want to do about the Persona suggestions, then find your taste page.” | Record spontaneous interpretation before asking recognition questions below. Adoption and deciding later are both successful choices. Expected destination: #/taste, labelled The Taste Passport. Time reveal-to-decision and decision-to-taste-page separately; mark discussion time. |
| 4. Recommended artwork | “Find a painting this site suggests for you that you'd like to look at more closely, and open its page.” | On #/taste, Discovery rings leads to artwork cards. A participant may instead use the reveal's Start here artist or List for you path. Record actual path and artwork ID. Stop on the artwork detail page, not an artist page or enlarged image alone. If none appeals, record that outcome without requiring a positive preference. |
| 5. Admire | “If this painting appeals to you, show the site that you admire it. If it doesn't, choose another suggested work that does, if there is one.” | Observe finding Admire and recognising its changed state. Note confusion with Seen in person or Save for later. If already admired during onboarding, ask for another unadmired suggestion without toggling it off on their behalf. If nothing appeals, record task declined; optionally invite a clearly labelled practice toggle with consent, never count that as preference evidence. |
| 6. Return | “Go back to your Taste Passport and show me where you would check what you just did.” | Observe finding Taste / #/taste and locating the work under admirations. Stop when the participant identifies it, or abandons. Record whether they expect the map or adopted Persona to change. A single admiration may cause little visible map movement; adopted Personas must not silently switch. |

After step 6, optionally ask: “If you came back tomorrow, what would you expect to find?” With their agreement, reload and observe whether the saved admiration is still visible. Keep this separate from the main loop timing. Sharing is a discussion question only: “Would you want to show any part of this to someone? What, if anything?” Do not require sending, copying a Passport link or downloading personal state.

### Recognition questions

Ask after the participant's spontaneous first-result interpretation, before continuing to recommendations. Avoid approving or explaining their answer.

- “What, if anything, feels like you here? What doesn't?”
- “Which choice you made would you connect to that part of the result?”
- “What do you think ‘provisional’ means here?”
- “What would you do if none of these Personas fit?”
- After returning: “Does this result help you decide what to look at next? Tell me how, or why not.”

Record recognition as their own account: recognises / mixed / does not recognise / unclear, with the supporting quote. Keep visual appeal, label recognition and recommendation relevance separate; one does not demonstrate the others. Do not interpret the Persona as a diagnosis.

### Neutral prompts and rescue

Use “What are you thinking?”, “What did you expect to happen?”, “What are you looking for?” or “What does that mean to you?” Avoid “Did you notice the Taste button?” or “Doesn't this Persona fit?” Do not teach terminology mid-task.

After roughly 30 seconds without progress, offer a neutral prompt; if still stuck, ask whether they want a hint or to stop. Record the help and timestamp before giving the smallest hint. A direct route such as #/palette or #/taste is a rescue, not an unaided completion. Let the session continue after rescue so downstream obstacles can still surface. Stop for discomfort or on request.

## Privacy and close

Collect no names, email addresses, recordings, screenshots of personal information, raw Passport JSON or share payloads in the repository. Keep identifiable scheduling/consent records and any consented recordings in owner-controlled storage with restricted access and an agreed deletion date. Anonymous notes can still identify someone through a distinctive quote; paraphrase or omit such details before producing a repository summary.

Close: “What was the most confusing part? What would you change first? Is there anything in your comments you would like me not to retain?” Thank them without defending the design. Clear study storage after the session; delete any incidental exports or clipboard payloads. Do not erase a participant's own pre-existing data.

## RESULTS TEMPLATE — one per session

Keep raw session notes outside the repo. Only aggregate, anonymised findings belong in a later repository report.

Session: S__ · build: __ · device/browser/input/theme: __ · broad familiarity: __
Observation consent: __ · recording: none / separately consented __ · technical interruptions: __

| Step | Elapsed time | Outcome: unaided / prompted / rescued / declined / abandoned | Help or technical pause |
| --- | --- | --- | --- |
| Entry | | | |
| Tones | | | |
| Sixteen artworks | | | |
| Five questions | | | |
| Begin → first result (total) | | | |
| Result interpretation and decision | | | |
| Reach Passport | | | |
| Open suggested artwork | | | |
| Admire | | | |
| Return and locate admiration | | | |

Recognition: __ · participant's explanation: __ · expectation after another admiration: __

| observed obstacle | affected loop step | supporting observation (quote/timing) | severity | proposed next experiment |
| --- | --- | --- | --- | --- |
| [Describe an observed action or failure, not an inferred motive] | [Entry / onboarding / result / recommendation / Admire / return] | [S__, anonymised quote, elapsed time, intervention] | [Blocker / major / minor] | [One change or hypothesis; next task and success observation] |

Severity: **blocker** = cannot complete or loses state without recovery; **major** = needs help, takes a substantial detour or persistently misunderstands a core action; **minor** = recovers unaided with brief friction. Frequency and severity are separate; one state-loss incident can outrank several cosmetic complaints. Label suggestions without an observed obstacle as hypotheses.

## Five-session synthesis template

Build(s): __ · sessions completed: __ of 5 · device/input coverage and gaps: __

1. Cluster observations by obstacle, preserving contrary cases and session IDs. Do not count several incidents by one participant as several participants.
2. Rank by severity, how directly the obstacle breaks the loop, then number of participants affected. Keep uncertain explanations explicit. Separate technical failures from usability obstacles.
3. Choose a small next experiment for each leading obstacle. Specify one observable improvement and what new sessions must check. Name an owner; do not turn this sample into a feature mandate.

| Rank | Obstacle and loop step | Severity | Participants affected / observed | Evidence and contrary cases | Proposed next experiment | Success observation | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | __ / __ | | | | |
| 2 | | | __ / __ | | | | |
| 3 | | | __ / __ | | | | |

Summary: “Across these five sessions, __ blocked completion, __ obscured the result, and __ hindered returning to the Passport. Recognition was __, supported by __; contradictory observations were __. Next we will test __. We still cannot conclude __ about enjoyment, retention or broader audiences.”
