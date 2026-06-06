# Audit — Methodology-transfer friction: the transfer matrix (who carries the method, where)

**Date:** 2026-06-07 · **Type:** read-only analysis (report persisted post-hoc) · **Session:** terminal C (Opus/high) · **Status:** Q1–Q3 + G1–G3 captured to BACKLOG via `docs/audit-trio-capture`; F1–F5 feed the Council brief; matrix feeds #91 and the repo-onboarding runbook.

---

**Source inventory confirmed (all read-only):** hub .claude/ (hooks: SessionStart fleet_health + surface_triage + billing_leak, PreToolUse block_immutable_edits; skills: verify; commands: /save /ship /handoff; agent: artifact-reader; workflow: conformance-hub.js; tier1-lifecycle plugin enabled) · templates/ (prompt-template, handoff/*, CLAUDE/ARCHITECTURE/ADR templates) · protocols/ (PLAYBOOK, ESSENTIALS, HANDOFF_PROCESS v4.4) · codex/AGENTS.md · distribution doctrine ADR-71/72/73/74/76/77 · latest handoff bundle 2026-06-06 (8 files, 02_METHODOLOGY = the browser card) · live child datapoint corp-monorepo (.claude/ = settings.json SessionStart surface-conformance + skills/gotchas + workflows/conformance-corp.js; tier1 plugin enabled; .pre-commit-config.yaml consumes hub toc-freshness @ 69558c7; CLAUDE.md v2.2 points to ../.dev-knowledge/protocols/ESSENTIALS+PLAYBOOK; no commands/, no validate-backlog/backlog-id hooks).

**Two facts that sharpened the buckets:** (1) the hub's .pre-commit-hooks.yaml exports only four doc-tooling hooks (codemap×2, toc×2) — validate-backlog, backlog-id-on-close, audit-health are hub-local .pre-commit-config.yaml entries, not published to the source-repo carrier. (2) /ship (ship.md) is repo-agnostic — generic git + pytest/ruff only, embeds branch→--no-ff→clean-tree→validators-green discipline.

## Step 1 — The transfer matrix

LEGEND: HOOK = enforced hook (auto-fires/gates) · USER = user-level ~/.claude (fleet-wide L0) · SKILL = auto-consulted skill · OP = operator-carried (hand-explain/paste/upload) · FILE = committed in-repo (auto-read/ref'd) · DNW = designed-not-wired · BUNDLE = carried in handoff bundle · — = absent · PLAT = cloud-platform guard · N/A = no agent / no-LLM path / irrelevant by design

CONTEXTS: H-CC=hub CC · C-CC=child CC · H-Br=hub browser · C-Br=child browser · Cloud=cloud routine · Local=scheduled local job (no-LLM, ADR-76) · New=brand-new repo day-0

```
ELEMENT                         | H-CC      | C-CC          | H-Br   | C-Br  | Cloud | Local | New
--------------------------------|-----------|---------------|--------|-------|-------|-------|------
R1 Prompt format & valve        | OP        | OP            | BUNDLE | BUNDLE| N/A   | N/A   | OP
R2 Model/Mode/Effort doctrine   | USER      | USER          | BUNDLE | BUNDLE| FILE  | N/A   | USER
R3 Check cadence (verify)       | SKILL     | USER/skill DNW| BUNDLE | BUNDLE| N/A   | N/A   | USER/—
R4 Git workflow /ship+no-ff     | FILE+HOOK | OP /ship —    | BUNDLE | BUNDLE| PLAT  | N/A   | OP
R5 Context-budget rule          | OP        | OP            | OP     | OP    | FILE  | N/A   | OP
R6 Review organ (Codex)         | USER      | USER          | BUNDLE | BUNDLE| N/A   | N/A   | USER
R7 Scheduling doctrine          | FILE      | FILE          | OP     | OP    | FILE  | FILE  | — (DNW)
R8 Gotchas corpus               | SKILL     | SKILL         | OP     | OP    | FILE/—| N/A   | SKILL/—
R9 ADR/JOURNAL/LESSONS          | FILE+HOOK | FILE+HOOK     | BUNDLE | BUNDLE| FILE  | code  | USER/—
R10 Guards OneDrive+immutable   | HOOK      | HOOK/immut DNW| N/A    | N/A   | PLAT  | N/A   | HOOK/immut —
R11 Handoff protocol            | FILE      | — (central'd) | BUNDLE | BUNDLE| N/A   | N/A   | FILE(hub)
R12 Backlog conventions         | HOOK      | HOOK/gate DNW | BUNDLE | BUNDLE| FILE  | N/A   | — (rollout)
```

**Key evidence per non-obvious cell:**
- R-all C-CC: child CLAUDE.md (corp §1.2/1.3) only POINTS to ../.dev-knowledge/protocols/*; CC auto-reads the repo's OWN CLAUDE.md → the floor is an instruction-to-go-read, NOT resident text. This is the operator's "re-explain in child context" pain.
- R2 Cloud: per-stage model pins (S=Haiku/M=Sonnet/L=Opus) committed in workflow .js (ADR-70).
- R3 C-CC: cadence-as-RULE travels via ~/.claude/core-invariants.md #2; the `verify` SKILL is hub-local (SKILL.md: "canonical-home deliberately open — refs #9").
- R4 C-CC: /ship is a hub .claude/commands file (corp has NO commands/); the --no-ff "universal" rule lives only in the HUB PROJECT'S auto-memory namespace → invisible in child CC.
- R4 Cloud: Routines push claude/* → PR, no auto-merge, Action diff-guard (settings.json //perm).
- R5 Cloud: spec-orchestration machine-markers + Explore-fan-out encoded in conformance .js.
- R7 Local: Windows Task Scheduler → python fleet_health.py, NO LLM on path (ADR-76); setup script version-controlled. Local column is N/A for LLM-instruction rows BY DESIGN.
- R8 Cloud: ADR-72 Class D — committed repo-local gotchas resolves (corp HAS one); hub's is user-level only → ABSENT in a hub cloud clone.
- R10 C-CC: block-onedrive is ~/.claude (fleet-wide); block_immutable_edits is HUB settings.json ONLY → child ADRs/transcripts have no in-place-edit block.
- R11 C-CC: handoffs centralized in .dev-knowledge by design (ESSENTIALS/ADR-60) — child absence is intentional, not friction.
- R12 C-CC: tier1 plugin closure loop TRAVELS (enabled in corp); validate-backlog + backlog-id-on-close are hub-local pre-commit, NOT in the exported .pre-commit-hooks.yaml.

## Step 2 — Friction ranking (OPERATOR-CARRIED + ABSENT/DNW cells, by context-use frequency)

**Tier A — child-repo CC session (DAILY; the operator's stated pain):**
1. Methodology floor not auto-resident (spans R1/R3/R5) — child CLAUDE.md points to hub PLAYBOOK/ESSENTIALS but CC only auto-loads the repo's own CLAUDE.md. The agent gets an instruction-to-read, not the text → operator re-explains the method each session.
2. R1 prompt format (OP) — operator hand-writes Model/Mode/Effort + structure every prompt; templates/prompt-template.md is hub-only.
3. R5 context-budget (OP) — grep-before-read absent from auto-context → CC full-reads large files, token blow-up, unless operator states it.
4. R4 /ship + no-ff (OP / —) — /ship absent in child; the --no-ff universal rule sits in hub-project memory only → risk of direct-to-main or ff merge.
5. R3 verify skill (DNW) — one-command cadence is hub-only; operator hand-runs pytest+ruff+git per step.
6. R12 validate-backlog + backlog-id gate (DNW) — schema + [#id]-on-close gates not exported → child backlog drifts or closes silently without an id.
7. R10 immutability guard (DNW) — hub-only PreToolUse; a child ADR/transcript edits in place with no block.

**Tier B — hub CC session (DAILY):** 8. R1 prompt format (OP) · 9. R5 context-budget (OP) — pure operator discipline, no gate either place.

**Tier C — browser chat, hub + child (DAILY-ish):** standing tax = re-upload ESSENTIALS + PLAYBOOK + bundle every session. Specific OP cells: 10. R8 gotchas (upload or lose corpus) · 11. R5 context-budget (PLAYBOOK upload) · 12. R7 scheduling (not in bundle card).

**Tier D — nightly (cloud routine / local job):** no friction — N/A cells inert-by-design (cloud read-only per ADR-72; local no-LLM per ADR-76).

**Tier E — brand-new repo day-zero (RARE):** R7 scheduling / R12 backlog / R10 immutability all ABSENT until a rollout moment (ADR-73). Free inheritance: gotchas, ROUTING, Codex, block-onedrive arrive day-zero via ~/.claude.

## Step 3 — Fix classification

**QUICK-WIRE (carrier exists; wiring mechanical; consumer-pull, no hub→sibling write)**
- Q1 backlog-id-on-close → publish in hub .pre-commit-hooks.yaml (ADR-71 source-repo carrier corp already consumes for TOC). Schema-agnostic (fires only when a task line is removed). Children add one stanza. Closes Tier-A #6 (the id half).
- Q2 /ship → move into the tier1-lifecycle plugin (carrier already ships /review-closures fleet-wide). ship.md verified repo-agnostic. Closes Tier-A #4 (/ship half) + carries no-ff.
- Q3 Promote the --no-ff "universal" rule from hub-project auto-memory → ~/.claude (where block-onedrive already lives, fleet-wide). Closes Tier-A #4 (no-ff half).

**DESIGN-FORK (genuine architecture choice — operator/Council rules; stated neutrally)**
- F1 Browser-side methodology carrier — Projects stable-knowledge layer vs per-session bundle vs hybrid? Decider: how often the methodology floor changes (stable layer goes stale silently) vs the per-upload tax measured across a week of browser sessions.
- F2 Minimum methodology surface a CHILD CC session should auto-SEE — pointer-only (status quo, leanest, operator pulls) vs a committed condensed floor that auto-loads vs distributed ESSENTIALS via the source-repo/plugin carrier? Decider: drift cost vs re-explain cost vs scope-bleed risk (F5).
- F3 `verify` skill canonical home (#9, already open) — hub-local pilot vs fleet-distributed skill vs fold into the plugin? Decider: whether the cadence belongs to every repo identically or stays a hub experiment.
- F4 Prompt-format transfer — keep as operator discipline (no gate, status quo) vs a scaffolding command/gate that emits the Model/Mode/Effort skeleton? Decider: error rate of hand-written headers vs the cost of a new command surface.
- F5 Scope visibility per context — what a child should explicitly NOT see (hub BACKLOG, LESSONS, handoffs, hub-only ADRs). This bounds F2: the floor a child gets must exclude these. Decider: the ADR-75 exclusion/zone register extended to "methodology surface per repo."

**GAP (nothing exists; needs a new organ)**
- G1 No organ makes a condensed methodology floor auto-resident in a child CC session. If F2 rules "child should auto-see a floor," a generated/synced child-floor file is net-new. Home: Cross-repo universalization theme.
- G2 No automation persists methodology into browser context. If F1 rules hybrid/Projects, the stable-layer sync is net-new; today it's 100% manual re-upload.
- G3 validate-backlog distribution is blocked NOT by a missing carrier but by unverified child schema compatibility (does every child use the ADR-66 story-map?). Needs a schema-conformance probe before the hook can travel. (Why validate-backlog is NOT a quick-wire.)

## Step 4 — Self-skeptic kill pass on QUICK-WIRE

KILL COUNT: 1 downgrade. **Q4 (proposed) Promote block_immutable_edits PreToolUse → ~/.claude fleet-wide — KILLED** as a pure quick-wire. A blind hub-path copy hard-codes docs/decisions/transcripts/**; children with different immutable zones get a hook that's wired-but-inert — the exact DESIGNED-NOT-WIRED smell this audit exists to kill. Correct scoping requires the ADR-75 zone register to enumerate each repo's immutable paths FIRST → gated on a register decision, not mechanical. Reclassified into F5 / ADR-75 register work.

**Survivors (re-checked against scoping / Layer-2 read-only / single-writer):** Q1 SURVIVES (schema-agnostic, fail-safe, consumer-pull; hub never writes the sibling). Q2 SURVIVES (repo-agnostic; refuses cleanly on a repo lacking validators; plugin carrier proven; child runs its own copy). Q3 SURVIVES (operator's own config layer; labeled "universal" in 02_METHODOLOGY; caveat: USER-layer change requiring operator approval, not an auto-wire).

## Step 5 — Clean confirmation

ZERO repo changes; hub git status --porcelain empty, exit 0. No writes anywhere: hub, corp-monorepo, ~/.claude all read-only this session. No temp files. No OneDrive path touched. Ratified doctrine (ADR-71/72/73/74/76/77) treated as constraints, not relitigated. Design forks left neutral.

**One-line takeaway:** the friction is concentrated in exactly one cell-column — child-repo CC sessions, where the methodology floor is a pointer the agent must choose to follow, not resident text — and three sub-elements (prompt format, /ship+no-ff, verify cadence) that live hub-locally and don't travel. Three are mechanical quick-wires (Q1–Q3); the rest is the genuine fork F2 (minimum auto-visible floor), bounded by F5 (what a child must not see). That fork + F1 (browser carrier) + F3 (#9) are the AI Council brief.
