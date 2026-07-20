# Pigment Coordinator

The Coordinator is neutral workflow software, not a third product-thinking
agent. It calls the ChatGPT theory pole and Claude synthesis/build pole,
validates their messages, persists the audit trail, enforces budgets and gates,
and stops for the product owner at `human_review_ready`.

It never chooses a product direction, edits the website, merges, or deploys.

## What is implemented

- A resumable task state machine stored in `protocol/tasks/<task_id>/state.json`.
- Strict validation against `protocol/message-schema.json`, including protection
  for Coordinator-owned routing fields.
- One liaison analyst per pole, validated by
  `protocol/analyst-packet-schema.json`, with JSON packets routed to the Kernel
  and owner reports disclosed according to explicit visibility rules.
- OpenAI Responses and Claude Messages adapters using structured JSON outputs.
- Optional command adapters for real ChatGPT/Codex and Claude Code teams.
- A deterministic fake provider for no-cost rehearsals and tests.
- A maximum deliberation round and provider-call budget per task.
- Deterministic convergence, build authorization, quality, and human gates.
- Atomic state writes, immutable numbered provider messages, generated protocol
  artifacts, and a cumulative Decision Record.
- Explicit refusal to treat a text-only Claude API response as a website build.

## State cycle

```text
intake
  -> challenge                 ChatGPT Theory Brief + Theory Liaison audit
  -> theory_revision           Claude Challenge + Synthesis Liaison audit
  -> final_synthesis           ChatGPT Revision/Defense + Theory Liaison audit
  -> awaiting_build_approval   Claude Final Synthesis + Synthesis Liaison audit
  -> approved_for_build        Coordinator convergence check + spec freeze
  -> building                  workspace-capable Claude command
  -> internal_review           Claude build/evidence + Synthesis Liaison audit
  -> revision                  ChatGPT review + Theory Liaison audit
  -> internal_review           Claude response/revisions + liaison audit
  -> human_review_ready        Coordinator quality gate + review package
  -> approved | rejected       product owner only
```

The transition to `approved_for_build` is automatic when the convergence
contract passes. This avoids interrupting the product owner during ordinary
deliberation. It authorizes isolated development only, never merging or
production deployment.

## First rehearsal

Run the state machine without network calls or API cost:

```sh
python3 tools/pigment_coordinator.py --fake create PIG-900 \
  "Rehearse the dipolar workflow without changing the website"
python3 tools/pigment_coordinator.py --fake run PIG-900
```

The rehearsal stops at the quality gate unless real or fixture review evidence
exists. It creates no production-code changes.

Inspect the task:

```sh
python3 tools/pigment_coordinator.py status PIG-900
find protocol/tasks/PIG-900 -maxdepth 2 -type f
```

Delete rehearsal task directories only when you intentionally no longer need
their audit records. Do not hand-edit `state.json` to bypass a gate.

## Live provider setup

Set secrets in the environment or your secret manager. Never put keys in the
repository. `.env.pigment.example` documents the supported variables.

The default live routing is:

- Theory: OpenAI Responses API using `OPENAI_API_KEY` and `OPENAI_MODEL`.
- Claude deliberation: Claude Messages API using `ANTHROPIC_API_KEY` and
  `ANTHROPIC_MODEL`.
- Claude build: pauses at `approved_for_build` until a workspace-capable command
  is configured.

Direct model APIs can return structured deliberation but cannot operate this
local repository by themselves. To run the actual Claude agent team, configure
`PIGMENT_CLAUDE_TEAM_COMMAND`. The command must read the complete prompt from
stdin, operate inside this repository, and print either the required message
JSON or a JSON object whose `result` field contains that JSON.

Example shape when Claude Code is installed and supports the project agent:

```sh
export PIGMENT_CLAUDE_TEAM_COMMAND='claude -p --output-format json'
```

The Coordinator prompt assigns the main session the Synthesis Lead role; that
session can then spawn the project agents. Avoid launching the main process with
a narrowly tool-restricted specialist definition that cannot coordinate peers.

Configure a separate workspace-capable command through
`PIGMENT_CLAUDE_BUILD_COMMAND`. It is intentionally not inherited from the
deliberation command: granting repository write access must be explicit.

`PIGMENT_CHATGPT_TEAM_COMMAND` can similarly replace the direct OpenAI adapter
with a local command that invokes the reconstructed ChatGPT team. It must remain
read-only on the repository.

Start a live objective:

```sh
python3 tools/pigment_coordinator.py create PIG-001 \
  "Describe the user outcome, not a predetermined implementation"
python3 tools/pigment_coordinator.py run PIG-001
```

`run` is resumable. A provider failure, budget limit, missing build command, or
failed gate leaves the last valid state on disk. Resolve the condition and run
the same command again.

## Deterministic gates

### Convergence

Claude's Final Synthesis must contain:

- accepted points prefixed `user_outcome:`, `information_architecture:`, and
  `principal_flow:`;
- at least one acceptance criterion;
- evidence prefixed `feasibility-confirmed:`;
- no `[critical]` disputed point or risk.

The Coordinator then copies the synthesis into `specification.md`, adds a SHA-256
freeze marker, and sets `build_authorized: true`.

### Quality

Before `human_review_ready`, the task must contain:

- `specification.md`, `decision-record.md`, and `build-evidence-report.md`;
- `quality-review.md` containing `GATE 2: CERTIFIED`, `OPEN CRITICAL: 0`, and
  `OPEN MAJOR: 0`;
- non-empty PNG evidence covering desktop/mobile and dark/light;
- a passing repository validator when one is configured.

The default validator is Node when available, otherwise the macOS JXA validator.
Override it with `PIGMENT_VALIDATOR_COMMAND`. Setting that variable to an empty
string disables only the repository validator; the other quality checks remain.

### Human authority

Only these commands close a review-ready task:

```sh
python3 tools/pigment_coordinator.py approve PIG-001 --note "Approved for merge"
python3 tools/pigment_coordinator.py reject PIG-001 --note "Revise the principal flow"
```

Approval records the decision; it does not merge or deploy.

## Security and operational boundaries

- Commands are tokenized without a shell, so pipes, substitutions, and redirects
  in command variables are not interpreted.
- Provider responses cannot alter task IDs, routing, rounds, timestamps, or
  workflow transitions.
- API calls retry bounded transient failures and never log API keys.
- Provider prompts and outputs are stored because they are the task audit trail.
  Do not place secrets or private user data in product objectives.
- Run one Coordinator process per task. Atomic writes prevent partial files but
  this first version does not provide distributed locking for simultaneous
  processes acting on the same task.

## Verification

```sh
PYTHONPYCACHEPREFIX=/tmp/pigment-pycache \
  python3 -m unittest discover -s tests -v
osascript -l JavaScript tools/validate.jxa.js
```
