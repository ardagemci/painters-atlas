# VoiceOver session script — PIG-001, acceptance criterion 15

**Operator:** Arda (human) · **Purpose:** the frozen specification requires
accessibility to be confirmed on a *tested assistive-technology setup*. No agent
can run a screen reader and honestly report what it said, so this session is the
only way this criterion can be met truthfully.

**What you do:** run through the six tasks below with VoiceOver on, and tell me
**what you heard** — roughly, in your own words. You do not need to transcribe
word-for-word. If VoiceOver said nothing at a step, that is a finding, and one of
the most valuable ones you can give me. "It said nothing" and "I couldn't tell
where I was" are both real results.

**What I do:** turn your report into the evidence record, mark anything that
failed, and route it. I will not embellish what you tell me.

---

## Setup (2 minutes)

1. Open **Safari** at **http://localhost:8422** (the server is already running
   and serving the built branch `pig-001-stabilization`).
2. Turn VoiceOver on: **⌘ + F5**. To turn it off later, ⌘ + F5 again.
3. If a "Welcome to VoiceOver" dialog appears, press **V** to skip the tutorial.

**Keys you need — that is all of them:**

| Key | What it does |
| --- | --- |
| **Control** (tap) | Shut VoiceOver up mid-sentence. Use this constantly. |
| **Tab** | Move to the next control, exactly as a keyboard user would |
| **Control + Option + A** | Read continuously from where you are |
| **Control + Option + →** | Step forward one item |
| **Space** or **Return** | Activate the thing you are on |

"VO" below means **Control + Option** held together.

Work in **light mode** if you have a choice — several of the known defects are
light-theme only.

---

## Task 1 — Does the page tell you where you are? (3 min)

The build changed how route changes are announced; it should now announce the
new page **once**, not re-read the whole page.

1. On the homepage, press **VO + A** and listen for a few seconds, then tap
   **Control** to stop.
2. Press **Tab** a few times until you reach a navigation link, e.g. *Artists*,
   and press **Return**.
3. **Listen carefully at the moment the page changes.**

**Tell me:** Did it announce the new page? Roughly what did it say? Did it say it
**once**, or repeat / start re-reading everything? Did you have any sense of
where you had landed?

---

## Task 2 — The skip link (2 min)

1. Go back to the homepage (⌘ + [ or the Back button).
2. Press **Tab exactly once** from the top of the page.

**Tell me:** What was the very first thing focused, and what did VoiceOver call
it? Could you *see* it appear on screen? Press **Return** on it — where did you
end up, and what was announced?

---

## Task 3 — Search (4 min)

1. **Tab** to the search box near the top.
2. **Tell me what VoiceOver called it** — the exact label it read for the box
   itself, as best you caught it.
3. Type **leonardo**.
4. **Listen** as results appear. Press **↓** two or three times.
5. Press **Escape**.

**Tell me:** Did it announce that results had appeared, and how many? As you
pressed ↓, did it read each result — and did you know *what kind* of thing each
was (a painter? an artwork? a museum?)? After Escape, where did your focus go —
back in the search box, or somewhere you couldn't identify?

---

## Task 4 — The influence graph and its bypass (4 min)

This page has about two hundred painters, each individually focusable. A "skip"
control was added so keyboard users are not trapped stepping through all of them.

1. Go to **http://localhost:8422/#/influences**.
2. **Tab** through the page and listen for a control that offers to skip past the
   graph. Activate it when you find it.
3. **Tell me** whether the next Tab after that landed you *past* the graph, or
   back inside it.
4. Now **Tab into the graph itself** and stop on a painter.

**Tell me:** What did VoiceOver say for that painter — just a name, or something
about their connections? Press **Return** on one. What was announced then?

> Known issue you may well hit: painters' names sitting on top of the connecting
> lines are very hard to *see*. If VoiceOver reads them fine, that is worth
> knowing — it would mean the problem is purely visual.

---

## Task 5 — Interrupting the onboarding (4 min)

The build added the ability to resume the taste onboarding if it is interrupted.

1. Go to **http://localhost:8422/#/palette**, and begin.
2. Work through with the keyboard — choose four tones, then answer a handful of
   the artwork cards. **Stop around the eighth card.**
3. **Reload the page** (⌘ + R).

**Tell me:** Did it put you back where you were, with your earlier answers
intact? Did VoiceOver make it clear what had happened and where you were? Did
you ever lose track of your progress — e.g. did it tell you which card of
sixteen you were on?

---

## Task 6 — Importing a taste passport over your own (3 min)

The most important fix in the entire build: importing someone else's passport
used to silently overwrite your own adopted persona. It now has to ask you.

1. Finish or restart the onboarding so you have a passport of your own, and
   **adopt a persona**.
2. Go to **http://localhost:8422/#/taste**, use **Copy share link**, and paste
   that link into the address bar — then **change a few characters in the long
   code** so it reads as a *different* passport, and load it.
3. Work through whatever appears, **using only the keyboard**.

**Tell me:** Were you asked, per item, whether to keep yours or take theirs — and
was that clear from listening alone? If you **cancel**, does it tell you nothing
was changed? Was anything about it confusing or alarming?

*(If step 2 turns out to be fiddly, skip it and say so — I can put the two
passports in place for you and you can redo just this task.)*

---

## When you are done

Turn VoiceOver off (**⌘ + F5**) and tell me, per task:

- **what you heard** (roughly is fine),
- **anything that said nothing at all**,
- **anything where you could not tell where you were or what had happened**,
- **anything that surprised or annoyed you.**

Blunt is better than polite. A screen-reader session that finds nothing is
suspicious; one that finds three irritating things is doing its job. Anything you
report as broken, I will record as a finding and fix — not argue with.
