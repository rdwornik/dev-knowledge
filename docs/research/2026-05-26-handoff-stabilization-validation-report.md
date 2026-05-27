---
type: validation-report
scope: handoff process stabilization implementation vs Council Q1-Q5 decisions
date: 2026-05-26
basis: 5 Council transcripts + 4 new ADRs (55-58) + ADR-42 Q5 amendment + template/protocol amendments
status: validation (closes Phase 1 of handoff stabilization, pending operator merge + measurement)
---

# Handoff Stabilization — Implementation vs Council Decisions Report

## Method

Each Council question's action items are mapped to the implemented artifact (ADR +
template/protocol change) and its commit SHA. Divergences from the literal prompt
are explicit. Branch: `docs/handoff-process-stabilization-2026-05-26` off `main`
(`31a95b9`). All commits verified with `pytest` (72 passed) + `ruff` clean.

## Commit ledger

| Commit | Subject |
|---|---|
| `26a24fa` | Phase A discovery snapshot |
| `74da327` | ADR-55 applied-task internalization gate (Q1) |
| `8d04b02` | ADR-56 inline Prompt Generation Card (Q3) |
| `9e94930` | ADR-57 two-layer bundle contract (Q2) |
| `8a2259e` | ADR-58 structured claims + symmetric verification (Q4) |
| `e1fc7f5` | ADR-42 amendment — full invariants + mechanical enforcement (Q5) |
| `4aaaeb6` | template: 10_GATE_PROBE.md section (Q1) |
| `322d0b9` | template: 11_CLAIMS.md section (Q4) |
| `72c202d` | template: two-layer contract + gate/claims integration (Q2+Q1+Q4) |
| `9a5efd3` | template: applied-task gate + Prompt Generation Card (Q1+Q3 + extensions) |
| `b9e2c73` | template fix: gate-probe drafted by CC + sender-reviewed (operator decision) |
| `9f5a7d4` | HANDOFF_PROCESS v3.4 — contract + gate + ratification + trigger rule (Q1+Q2+Q4) |
| `24f5a5c` | template: manifest invariant hashes + next_session_scope + file entries (Q5) |
| `9753e3f` | PLAYBOOK Prompt Generation Card maintenance rule (Q3) |
| `da4d4a7` | BACKLOG P2 deferred mechanical gate code (Q5) |

## Q1 — Internalization assurance (applied-task gate)

| Council action item (L864-895) | Implementation | Status |
|---|---|---|
| AI1 Replace 4-item paraphrase gate (role+constraints citations + applied proof) | `00_first-message.md` section `9a5efd3` + ADR-55 `74da327` | done |
| AI2 Amend `00_first-message.md` gate format + confirmation wording | `9a5efd3` (`role confirmed + probe passed`) | done |
| AI3 Add `08_GATE_PROBE.md` artifact (scenario + operator-only key) | `10_GATE_PROBE.md` section `4aaaeb6` | done (renumbered 08→10) |
| AI4 Failure protocol (retry once → regenerate) | HANDOFF_PROCESS `9f5a7d4` | done |
| AI5 Minimal operator audit trace | HANDOFF_PROCESS structured-ratification checklist `9f5a7d4` | done |
| AI6 Review after 5-10 handoffs | — | deferred (measurement BACKLOG) |

## Q2 — Bundle content composition (two-layer contract)

| Council action item (L910-936) | Implementation | Status |
|---|---|---|
| AI1 Two-layer contract in PROCESS + FOLDER_TEMPLATE | `72c202d` + `9f5a7d4` + ADR-57 `9e94930` | done |
| AI2 Add `next_session_scope` (enum + mixed-uncertain fail-safe) | template `72c202d` + manifest `24f5a5c` | done |
| AI3 First scope → artifact mapping table | template `72c202d` + PROCESS `9f5a7d4` | done |
| AI4 Add skills/gotchas/JOURNAL to bundle inventory | template `72c202d` (operational layer) | done |
| AI5 Record in a new ADR | ADR-57 `9e94930` | done |
| AI6 Open Q5 follow-up with urgency | Q5 implemented this session (ADR-42 amendment) | done |
| AI7 Validate prompt-gen tooling in-bundle dependency | resolved: browser cannot read FS → in-bundle required (ADR-57 Trace) | done |

## Q3 — Procedural competence transfer (Prompt Generation Card)

| Council action item (L885-931) | Implementation | Status |
|---|---|---|
| AI1 Replace PLAYBOOK-pointer with inline card | `00_first-message.md` `9a5efd3` + ADR-56 `8d04b02` | done |
| AI2 Design card (checklist + model/effort table + fallback + exemplars) | `9a5efd3` | done |
| AI3 Define mandatory prompt skeleton | `9a5efd3` (12-item skeleton incl. operator extensions) | done |
| AI4 Require card in every bundle (FOLDER_TEMPLATE) | `9a5efd3` (`### 00_first-message.md` section) | done |
| AI5 Create short ADR | ADR-56 `8d04b02` | done |
| AI6 Measurement plan (≥10 handoffs) | — | deferred (measurement BACKLOG) |
| AI7 Maintenance rule (update PLAYBOOK + card) | PLAYBOOK `9753e3f` + card maintenance note `9a5efd3` | done |
| AI8 Optional compact structured schema | — | not implemented (optional) |

## Q4 — Sender verification symmetry (structured claims)

| Council action item (L931-955) | Implementation | Status |
|---|---|---|
| AI1 Stage 2 sender structured claim artifact (`CLAIMS.md`) | `11_CLAIMS.md` section `322d0b9` + PROCESS Stage 2 `9f5a7d4` + ADR-58 `8a2259e` | done (numbered 11_) |
| AI2 Encode trigger rule | HANDOFF_PROCESS "Verification trigger rule" `9f5a7d4` | done |
| AI3 Amend Stage 3 — replace bare `role confirmed` | HANDOFF_PROCESS structured ratification `9f5a7d4` | done |
| AI4 Executor-side citation validation | PROCESS Stage 3 step 8a `9f5a7d4` + template gen step `72c202d` | done (contract; mechanical wiring deferred) |
| AI5 Sender expected-articulation contract | `11_CLAIMS.md` section `322d0b9` | done |

## Q5 — Delivery custody abstraction (full invariants + mechanical enforcement)

| Council action item (L891-928) | Implementation | Status |
|---|---|---|
| AI1 ADR-42 amendment (full invariants; ADR-45 not reopened; gates approved) | `e1fc7f5` | done |
| AI2 Define validator contract (mechanical only; no sequencing) | ADR-42 amendment `e1fc7f5` | done |
| AI3 Implement executor-side gates (pre-commit/PreToolUse//save) | — | deferred (BACKLOG `da4d4a7`) |
| AI4 Invariant integrity tracking in manifest | manifest `invariant_integrity` `24f5a5c` | done |
| AI5 Browser-side active checkpoint | operationalized via Q1 applied-task gate (ADR-55) | done |
| AI6 Instrument and review | — | deferred (measurement) |

## Operator extensions (Council did not cover)

| Extension | Implementation | Justification |
|---|---|---|
| Hook selection guidance | Prompt Generation Card "Hook selection" table `9a5efd3` | Operator-specific; Council did not address |
| JOURNAL update mandate | Skeleton item 9 `9a5efd3` | Per ADR-49 |
| Workflow update mandate | Skeleton item 10 `9a5efd3` | Operator engineering mandate |
| Git workflow (branch + revertable commits + no auto-push) | Skeleton item 5 `9a5efd3` | Operator engineering mandate |

## Deferred items (with rationale)

| Item | Source | Why deferred | Where tracked |
|---|---|---|---|
| Mechanical gate code (hooks wiring) | Q5 AI3 | This session = ADR + contract only | BACKLOG P2 `da4d4a7` |
| Measurement plan execution | Q1 AI6 / Q3 AI6 / Q5 AI6 | Needs 5-10 real handoffs as evidence | post-rollout (measurement BACKLOG — to create at first handoff) |
| ADR-45 payload-shrink reopen thresholds | Q5 risk #6 | Define alongside mechanical gate work | BACKLOG P2 `da4d4a7` |
| Optional prompt mini-schema | Q3 AI8 | Optional; card prose sufficient for now | not tracked |

## Divergences from the implementation prompt

1. **File numbers 10/11, not 08/09.** Prompt named `08_GATE_PROBE.md` /
   `09_CLAIMS.md`; those collide with existing `08_TREE.txt` /
   `09_EXECUTION_EVIDENCE.md`. Operator decision 2026-05-26: use `10_`/`11_`, no
   renumber. Recorded in ADR-55/ADR-58 and the discovery snapshot.
2. **Bundle-file definitions live as sections in `HANDOFF_FOLDER_TEMPLATE.md`,
   not standalone `templates/handoff/*.md` files.** The repo has no
   `templates/handoff/` directory; every bundle file is defined as a `### NN_name`
   section and generated per-handoff into `docs/handoffs/{slug}/`. Operator
   decision 2026-05-26. Avoids a competing definition surface.
3. **Gate-probe authorship: CC-drafts + sender-reviews** (operator baked decision),
   not sender-authored as Council Q1 AI3 literally stated. Mitigates the probe
   authoring + sender-hallucination risks the Council flagged.
4. **Card mirrors PLAYBOOK's full Model/Mode/Effort taxonomy** (incl. Mode and
   `xhigh`), not the prompt's reduced Model+Effort table — to honor the Q3 anti-drift
   maintenance rule.
5. **Added (beyond prompt steps), for consistency:** registered ADR-55..58 in
   `docs/decisions/README.md` (index + traceability tables); bumped
   `HANDOFF_PROCESS.md` v3.3.3 → v3.4 with a changelog entry (the doc's strict
   versioning convention). No ADR-39 registry change needed — the new bundle files
   are sections of an already-registered template, not new tracked files.

Otherwise no substantive divergence. Operator extensions are additions Council did
not preclude.

## Architectural contract

- **Zero ai-council writes.** All writes are in `.dev-knowledge` (`docs/decisions/`,
  `docs/research/`, `templates/`, `protocols/`, `BACKLOG.md`). ai-council was
  read-only context only (ADR-45 filesystem-constraint verification for Q2 AI7).
- **Layer-2 invariant intact.** No orchestration/executable code added; the
  mechanical validator is a documented contract, deferred to BACKLOG. The validator
  contract explicitly forbids workflow sequencing (ADR-28 cited).
- **ADR-45 not reopened.** Q5 keeps full invariants; ADR-45 stays explored-not-adopted.

## Conformance assessment

- 5/5 Council decisions implemented as ADR + template/protocol amendment.
- 4/4 operator extensions embedded in the card + skeleton.
- 2 items deferred (mechanical gate code → BACKLOG; measurement → post-rollout),
  both explicitly captured.

**Phase 1 of handoff process stabilization: COMPLETE pending operator merge +
measurement.**

## Open follow-ups

1. Run the measurement plan after 5-10 real handoffs (gate pass/fail rate, retry
   frequency, post-gate failures, wrong model/effort, bundle token load).
2. Implement mechanical gate code (BACKLOG P2 `da4d4a7`) when ready; Codex review per ADR-54.
3. Consider skill-based handoff pattern (chat Option D) only if card bloat materializes.
4. Consider sender-role rethink (chat Option C) only if a browser-chat bottleneck persists.
