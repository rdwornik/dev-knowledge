# Research note — Dynamic Workflows (Claude Code)

**BACKLOG #80 deliverable** · 2026-06-03 · Author: architect (browser chat) ·
Status: research + synthesis, no code

> Repo landing location intentionally unset — placed per existing convention by
> Rob/CC, not invented here (no new folders without approval).

---

## 1 · Grounding (the #80 mandate, executed)

All claims below verified against Anthropic's own published sources on
2026-06-03 [witnessed — fetched directly this session]:

- **S1** — Official docs: <https://code.claude.com/docs/en/workflows>
  ("Orchestrate subagents at scale with dynamic workflows") — the authoritative
  mechanics reference. Freshest source (updated within hours of fetch).
- **S2** — Launch blog: <https://claude.com/blog/introducing-dynamic-workflows-in-claude-code>
  (2026-05-28) — use cases, Bun case study, positioning.
- **S3** — Opus 4.8 announcement: <https://www.anthropic.com/news/claude-opus-4-8>
  — launch context (workflows shipped alongside Opus 4.8 + effort controls).
- **S4** — Anthropic research: <https://www.anthropic.com/research/long-running-Claude>
  — the only official source using the term "agentic laziness"; documents the
  Ralph loop and the native `/loop` command.

**Where S1 and S2 conflict, S1 wins** (it is newer and more specific). One
material conflict found — availability, §4.

## 2 · What the feature is (one paragraph)

A dynamic workflow is a **JavaScript orchestration script that Claude writes
for your task and a runtime executes in the background**, coordinating tens to
hundreds of subagents in parallel while the session stays responsive. The
architectural inversion vs. everything we use today: with subagents, skills,
and agent teams, *Claude* is the orchestrator and every intermediate result
lands in a context window; with a workflow, *the script* holds the loop, the
branching, and the intermediate state, and Claude's context holds only the
final verified answer. The script is a file (under `~/.claude/projects/`),
so the orchestration is **readable, diffable, editable, rerunnable, and
saveable as a slash command** — orchestration becomes a versioned artifact,
not an ephemeral conversation. [witnessed — S1]

## 3 · Taxonomy reconciliation — the key #80 finding

**The bundle's "six patterns / three failure modes" taxonomy is seed-article
vocabulary, not Anthropic's official taxonomy.** The official docs (S1/S2)
describe the *mechanisms* but never enumerate a named six-pattern list. The
named list traces to secondary coverage of Anthropic team commentary (e.g.
The Neuron's "Explained by Team Anthropic" explainer). Verdict per pattern:

| Bundle term | Official grounding | Verdict |
|---|---|---|
| classify-and-act | Not named in S1/S2. Consistent with Anthropic's older "routing" pattern (Building Effective Agents) | **inferred** — usable, but cite as community vocabulary |
| fan-out-synthesize | S1: `/deep-research` "fans out web searches… synthesizes a cited report"; S2: "breaks it into subtasks and fans the work out" | **witnessed** — mechanism official, name informal |
| adversarial-verification | S1: "independent agents adversarially review each other's findings"; S2: "adversarial agents working to break the result" | **witnessed** — strongest-grounded pattern |
| generate-and-filter | S1: `/deep-research` "votes on each claim… claims that didn't survive cross-checking filtered out" | **witnessed** — mechanism official, name informal |
| tournament | S1: "draft a plan from several angles and weigh them against each other" | **inferred** — multi-angle drafting is official; pairwise-tournament naming is secondary |
| loop-until-done | S2: "the run keeps iterating until the answers converge"; S4: Ralph loop + native `/loop` | **witnessed** |

Failure modes:

| Bundle term | Official grounding | Verdict |
|---|---|---|
| agentic-laziness | S4 names and defines it; `/loop`-style patterns are the documented counter | **witnessed** — official Anthropic term |
| self-preferential-bias | Not found in any official source. The adversarial-review mechanism ("**independent** agents", "other agents try to refute") implicitly targets it | **inferred** — treat as community framing of an official design choice |
| goal-drift | S2: "the plan stays on track no matter how big the task gets" (coordination outside the conversation) — the term itself is research-literature vocabulary | **inferred** — mechanism official, term external |

**So what:** the patterns are safe to use as our internal vocabulary, but any
ADR or PLAYBOOK text must cite the *mechanisms* to S1/S2 and mark the
six-name list as informal taxonomy. Do not write "Anthropic's six patterns"
into a living doc — that would be exactly the kind of unverifiable hardcode
the drift-proofing principle exists to prevent.

## 4 · Load-bearing facts for our use [all witnessed — S1 unless noted]

- **Availability:** research preview; requires **Claude Code v2.1.154+**;
  available on **all paid plans** (on Pro: toggle in `/config`) plus API,
  Bedrock, Vertex, Foundry. ⚠️ S2 (launch blog) said Max/Team/Enterprise only —
  **S1 supersedes**; access has widened since launch.
- **Triggering:** keyword `ultracode` in a prompt (or natural language "use a
  workflow"); or `/effort ultracode` = xhigh effort + Claude auto-decides per
  task. Pre-v2.1.160 the literal keyword was `workflow`.
- **Bundled:** `/deep-research` ships built-in. **Saved workflows become slash
  commands**: `.claude/workflows/` (project-shared, wins name conflicts) or
  `~/.claude/workflows/` (personal). Saved workflows accept structured input
  via an `args` global.
- **Hard limits:** ≤16 concurrent agents (fewer on weak CPUs); ≤1,000 agents
  per run; **no mid-run user input** — staged sign-off means one workflow per
  stage; the script itself has no filesystem/shell access (only its agents do).
- **⚠️ The permission fact that matters most to us:** workflow subagents
  **always run in `acceptEdits` mode** and **file edits are auto-approved**,
  regardless of the session's permission mode. The launch prompt is the only
  default gate. Read-only behavior is therefore **not guaranteed by the
  permission system** — it must be engineered (see §6, risk R1).
- **Resumability:** completed agents return cached results on resume — within
  the same CC session only; exiting CC restarts the workflow fresh.
- **Cost:** substantially more tokens than a normal session; official guidance
  is to pilot on a small slice (one directory, one narrow question). Per-stage
  model routing is supported ("use a smaller model for stages that don't need
  the strongest one") — our Sonnet/Opus selection rule extends naturally to
  *workflow stages*.
- **Org/user kill switches:** `/config` toggle, `"disableWorkflows": true`,
  `CLAUDE_CODE_DISABLE_WORKFLOWS=1`, managed settings.

## 5 · Pattern → use-case mapping (our conformance/review needs)

| Pattern | Our use case | Notes |
|---|---|---|
| fan-out-synthesize | **#81 core**: verifier-per-rule fan-out across `.dev-knowledge` conventions; one agent per PLAYBOOK/ESSENTIALS rule, structured findings merged | Exactly the bundle's design; the docs confirm it's the canonical workflow shape |
| adversarial-verification | **#81 skeptic persona**: independent refuter agents challenge each finding before it reaches the report — false-positive suppression is a *first-class documented mechanism*, not our invention | Also: handoff **Phase-2 verification** — assign one agent per load-bearing claim, adversarially check against repo state (deep-verification shape) |
| loop-until-done | **#81 continuity**: `/loop` (native, S4) drives the conformance run until "no new findings" — this is the mechanization of "no dead docs" | Counter to agentic-laziness; stop condition must be explicit |
| generate-and-filter | **LESSONS candidate mining**: generate rule-candidates from session journals/diffs, dedupe, verify each against actual incidents, keep survivors | Matches the documented "mine sessions for recurring corrections → CLAUDE.md rules" use case |
| tournament / multi-angle drafting | **#70 adjacency**: AI Council remains the heavy-*decision* organ (judgment, ADRs); tournament workflows suit *artifact* selection (e.g. competing template drafts judged pairwise) — don't let workflows creep into Council's role | Boundary worth one PLAYBOOK sentence when #74 is written |
| classify-and-act | **#82 routing**: classify each repo's docs/state, route to the applicable verifier profile | Weakest-grounded pattern; fine for internal design language |

**The #74 escalation rule falls straight out of S1's comparison table.** Use a
workflow when: (a) the task needs more agents than one conversation can
coordinate, (b) you want the orchestration codified as a rerunnable artifact,
or (c) result quality justifies adversarial cross-checking. Stay with a
subagent/skill when the task is bounded, the split is known, and token economy
matters. This maps cleanly onto our existing rule shape: *"do X the way we
always do it" → Sonnet; "figure out the approach" → Opus;* now extended with
*"too big for one pass / needs independent verification" → workflow*.

## 6 · Risks & open questions (verify in CC before #81 design hardens)

- **R1 — acceptEdits vs read-only [the big one].** #81 mandates read-only
  proposals; the runtime auto-approves subagent file edits. Candidate
  mitigations, in drift-proofing precedence order: (source) prompt/script
  design that gives agents no write tasks; (gate) **permission deny rules for
  Write/Edit on sibling paths — whether deny rules bind workflow subagents is
  `unknown`, verify in CC**; (agent) post-run `git status --porcelain` across
  the fleet as a tripwire. Until R1 is resolved, pilot #81 against
  `.dev-knowledge` itself only, never across siblings.
- **R2 — saved workflows vs "Layer 2 never executes."** A saved
  `.claude/workflows/conformance.js` is committed orchestration living in the
  hub. Does it violate the boundary? My reading: no — the boundary forbids
  *scripts that drive child-repo state*; a read-only conformance workflow is a
  validator in new clothing, and `.claude/workflows/` ≠ `scripts/`. But this
  is **ADR territory — Council question, not a unilateral call**.
- **R3 — version gate.** Workflows need CC ≥2.1.154 (`ultracode` keyword
  semantics changed at 2.1.160). Local CC version: `unknown` — verify
  (`claude --version`) before any pilot.
- **R4 — no mid-run input.** A gated conformance run (findings → Rob sign-off
  → next stage) must be **one workflow per stage**, not one mega-run. Shapes
  #81's architecture directly.
- **R5 — cost discipline.** Pilot scope: one protocol file's rules, not the
  whole rulebook. The Sonnet-for-verifiers / Opus-for-skeptic split is the
  obvious stage-routing to test.

## 7 · One-line synthesis

Dynamic workflows give us the missing execution organ: **orchestration as a
saved, diffable, rerunnable artifact** with adversarial verification built in —
#81's verifier-fan-out + skeptic + `/loop` design is not just compatible with
the feature, it is the feature's canonical documented shape. The two things
standing between us and a pilot are R1 (read-only enforcement) and R2 (the
Layer-2 ruling), both resolvable before any agent runs.

---

## AMENDMENT A — 2026-06-03 (same day, post-§3 correction)

**§3's central verdict is overturned by better evidence and is superseded.**
Rob supplied the Anthropic engineering post *"A harness for every task: dynamic
workflows in Claude Code"* by Thariq Shihipar and Sid Bidasaria (Anthropic,
Claude Code team; cross-posted to the official Claude Blog). It names **all six
patterns verbatim** (classify-and-act, fan-out-and-synthesize, adversarial
verification, generate-and-filter, tournament, loop-until-done) **and all three
failure modes verbatim** (agentic laziness, self-preferential bias, goal
drift). The taxonomy IS official Anthropic vocabulary. [witnessed — full text
read this session; designate **S5**]

Root cause of the §3 error: my web searches surfaced S1/S2 (product docs +
launch blog) but not S5 (engineering post), and I generalized "not in the
sources I found" into "not official." Lesson: *absence in retrieved sources is
not absence in the canon — bound the claim to the corpus actually searched.*

Corrected verdicts: all six patterns → **witnessed (S5)**; all three failure
modes → **witnessed (S5)**. The §3 caution about hardcoding still stands in
softened form: cite S5 by URL/title when the taxonomy enters living docs.

**New load-bearing facts from S5 (not in S1/S2):**
- Core API: `agent()`, `parallel()` (barrier — waits for all), `pipeline()`
  (streaming per item). Standard JS (JSON/Math/Array) available for data.
- **Per-agent model choice** (incl. Haiku for cheap fan-out) and **per-agent
  isolation level: worktree (isolated git checkout) or no-checkout** — the
  isolation control is a new, structural R1 mitigation candidate.
- `/goal` = hard completion requirement (anti-agentic-laziness); `/loop` =
  recurring schedule; **explicit token budgets in the prompt** ("use 10k
  tokens") cap a run.
- **Quarantine pattern**: agents reading untrusted content are barred from
  high-privilege actions; separate unexposed agents act.
- "Memory and rule adherence" use case describes #81's design verbatim
  (verifier-per-rule + skeptic persona) — #81 is now grounded in an official
  source, not just the bundle.
- Distribution: save to `~/.claude/workflows` **or ship inside a Skill**
  (JS files in the skill folder, referenced from SKILL.md, treated as a
  *template* Claude adapts, not a verbatim script).
- ⚠️ **Source conflict on resumability:** S5 says an interrupted workflow
  (incl. quitting the terminal) resumes on session resume; S1 (product docs,
  newer) says resume works only within the same session and exiting CC
  restarts fresh. Unresolved — verify empirically (Phase 0); load-bearing for
  the night-run architecture.

---

## AMENDMENT B — 2026-06-05 (records-only reconciliation)

Written from repo records only — Phase-0 gate findings, LESSONS, PLAYBOOK, and
the commit log; no new web research. Closes the open verification items the
original note flagged and records one new load-bearing fact discovered since.

**(a) R3 resolved — CC version verified at Phase-0.** Local Claude Code is
`2.1.162` (≥ 2.1.154 required; past the v2.1.160 `ultracode`-semantics cutover).
Phase-0 gate 1 (version/env) **PASS**, with the Workflow tool empirically
functional (a workflow executed, Run ID `wf_660342a4-3c0`). The §6 R3 open
question ("Local CC version: `unknown` — verify") is therefore closed.
[docs/audits/2026-06-03-phase0-workflow-gates-findings.md]

**(b) The S1-vs-S5 resumability conflict (§4 / Amendment A) is RESOLVED
empirically — S1 wins.** Phase-0 gate 5 (operator TUI, 2026-06-03): after a CC
quit + `claude --resume`, the *session* restored but the workflow run showed
**terminated** in `/workflows` (✘, 2 of 3 agents, 28.6k tok) with **no resume
option — only view/save**. Workflow runs **do not survive a CC exit**; S5's
"quit→resume" claim does not hold on 2.1.162. The architectural consequence is
the **fire-and-complete doctrine** — one uninterrupted process per stage, no
cross-restart resume — now carried in #85's body (LOCAL night-run track).

**(c) NEW load-bearing fact — the cloud Routines runtime does NOT run workflows
natively.** A nightly re-probe confirms the cloud runner does not execute
Dynamic Workflows natively; the deployment falls back to **spec-orchestration**
(the `.js` harness is read as a *spec* the top-level session follows, not run
by the workflow engine as code). Consequence for any in-script guarantee:
**in-script validators are inert there** — a code validation step in the
harness fires only on the native Workflow path, never on the cloud fallback. The
load-bearing cloud backstop is therefore **parser-side fail-closed** (the
consumer/Action side that runs unconditionally), not the generator-side
in-script validator. [LESSONS 2026-06-05 — "Locate contract guarantees on the
path that ACTUALLY executes"]

**(d) The PLAYBOOK Routine/night deployment standard landed** (#84 part (d) —
commit `7a3e48b`). The cloud-night safety envelope (allow-only platform guards,
*no* committed Write/Edit deny — distinct from the local #85 committed-deny),
the spec-orchestration doctrine (native-attempt-first + nightly re-probe), the
outcome loop (Action diff-guard → nightly-triage Issues → SessionStart
surfacing), t-shirt model-routing pins, and cloud-session closeout (stranded
`claude/*` branches) are now PLAYBOOK standard. This flips the PLAYBOOK row
toward CURRENT in `docs/audits/2026-06-05-living-doc-staleness.md`.
