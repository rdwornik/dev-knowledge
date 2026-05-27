---
type: research-discovery
scope: handoff process stabilization — pre-implementation discovery snapshot
date: 2026-05-26
status: snapshot (Phase A input to the 5-Council-decision implementation)
contract: read-only discovery; no files modified before this snapshot
basis: 5 Council transcripts (Q1-Q5) on main since 31a95b9 + current handoff machinery + governing ADRs
---

# Handoff Stabilization — Discovery Snapshot 2026-05-26

Phase A of implementing all 5 AI Council debate decisions (Q1-Q5) for handoff
process stabilization. Captures Council action items verbatim with line refs,
the live state of each handoff-machinery file, the next ADR numbers, the four
operator extensions, and the conflicts found between the implementation prompt's
assumptions and live repo state (resolved with operator before execution).

## Pre-execution gate — PASSED

- Consolidation merged to `main`: `31a95b9 merge: consolidation + ADR-43 governance truth-up + BACKLOG codification 2026-05-26`. HEAD of `main` at discovery.
- All 5 Council transcripts present on `main` under `docs/decisions/transcripts/council-out-20260526_*`.
- Branch for this work: `docs/handoff-process-stabilization-2026-05-26` off `main`.

## Council action items (verbatim, with transcript line refs)

### Q1 — Internalization assurance (applied-task gate)
Source: `council-out-20260526_142806-...-Q1-internalization-assurance.md`, Recommended Decision L796-862, Action Items L864-898.
- AI1 — Amend `HANDOFF_FOLDER_TEMPLATE.md`: replace 4-item paraphrase gate with role + top-3 constraints (file/section citations) + one applied-task proof (L866-869).
- AI2 — Amend `00_first-message.md`: new gate format; confirmation wording paraphrase-pass → internalization/application-pass (L871-873).
- AI3 — Add required bundle artifact `08_GATE_PROBE.md` (mini-scenario + operator-only answer key) (L875-878). **Deviation:** numbered `10_GATE_PROBE.md` — 08/09 already used by TREE/EXECUTION_EVIDENCE (operator decision 2026-05-26).
- AI4 — Define failure protocol in process doc: first fail → point to contradiction + retry once; second fail → stop + regenerate (L880-882).
- AI5 — Add minimal operator audit trace (citation checked / probe matched / retry needed) (L884-888).
- AI6 — Review after 5-10 handoffs (pass/fail, retries, post-gate failures) (L890-895). **Deferred** to measurement BACKLOG.

### Q2 — Bundle content composition (two-layer contract)
Source: `council-out-20260526_143605-...-Q2-bundle-content-composition.md`, Recommended Decision L840-884, Action Items L910-936.
- AI1 — Amend `HANDOFF_PROCESS.md` + `HANDOFF_FOLDER_TEMPLATE.md`: define two-layer contract — unconditional floor VISION/PLAYBOOK/ESSENTIALS; scoped operational layer skills/gotchas/JOURNAL (L912-915).
- AI2 — Add `next_session_scope` to template; small enumerated vocabulary; `uncertain/mixed` fail-safe (L917-919).
- AI3 — Create first scope → artifact mapping table, ships with the rule change (L921-923).
- AI4 — Add skills/gotchas/JOURNAL to formal bundle inventory (L925-926).
- AI5 — Record in a new ADR (changes the bundle contract beyond ADR-42 invariant-only rule) (L928-929).
- AI6 — Open follow-up for Q5 with urgency (L931-932) — satisfied: Q5 is implemented this session.
- AI7 — Validate whether prompt-gen tooling needs PLAYBOOK/ESSENTIALS physically in-bundle vs operator-available (L934-936). Verified: browser chat cannot read filesystem (ADR-45 Context L79-86) → must be in-bundle; resolved in favor of keeping full copies.

### Q3 — Procedural competence transfer (inline Prompt Generation Card)
Source: `council-out-20260526_144228-...-Q3-procedural-competence-transfer.md`, Recommended Decision L820-863, Action Items L885-931.
- AI1 — Amend `00_first-message.md` gen rules: replace "generate per 03_PLAYBOOK" with inline Prompt Generation Card (L887-888).
- AI2 — Design card: checklist + model/effort table + `uncertain/mixed -> Opus + higher effort + operator review` fallback + 2-3 exemplars (L890-895).
- AI3 — Define mandatory prompt skeleton — exact sections every generated prompt must contain (L897-898).
- AI4 — Update `HANDOFF_FOLDER_TEMPLATE.md`: require card in every bundle (L900-901).
- AI5 — Create short ADR (problem, why pointer failed, why authority stays in browser, why duplicated inline, length budget, revisit criteria) (L903-909).
- AI6 — Measurement plan over ≥10 handoffs (L911-916). **Deferred.**
- AI7 — Maintenance rule: any change to prompt conventions updates BOTH PLAYBOOK rationale + inline card (L918-921).
- AI8 — Optional compact structured schema (L923-931). Not implemented (optional).

### Q4 — Sender verification symmetry (structured claims)
Source: `council-out-20260526_144851-...-Q4-sender-verification-symmetry.md`, Recommended Decision L826-892, Action Items L931-955.
- AI1 — Amend `HANDOFF_PROCESS.md` Stage 2: require sender-side structured claim artifact (`CLAIMS.md` or equivalent); each load-bearing claim has citation OR explicit assumption marker (L933-937). **Deviation:** numbered `11_CLAIMS.md` (operator decision).
- AI2 — Encode trigger rule: "Confident claim about an unread or unverified source requires verification + citation" (L939-941).
- AI3 — Amend Stage 3: replace bare `role confirmed`; operator ratifies against claims artifact + executor validation + receiver articulation (L943-948).
- AI4 — Add executor-side validation: cited file existence / line-range locatability / decision reference format (L950-952).
- AI5 — Require sender-produced expected-articulation contract (L954-955).

### Q5 — Delivery custody abstraction (full invariants + mechanical enforcement)
Source: `council-out-20260526_145439-...-Q5-delivery-custody-abstraction.md`, Recommended Decision L799-847, Action Items L891-928.
- AI1 — Record decision formally: ADR-42 amendment — full invariants stay in every bundle; ADR-45 payload-shrink NOT reopened; executor-side mechanical gates approved (L893-897).
- AI2 — Define validator contract: presence, integrity/hash/version, naming/shape/link only; forbid workflow sequencing (L899-905).
- AI3 — Implement executor-side gates (pre-commit, PreToolUse, `/save`); ≥1 non-bypassable backstop (L907-912). **Deferred** to BACKLOG (mechanical code out of scope; contract only this session).
- AI4 — Add invariant integrity tracking: canonical hashes/version IDs for VISION/PLAYBOOK/ESSENTIALS in manifest; fail on mismatch (L914-916).
- AI5 — Add browser-side active checkpoint (structured constraint extraction before proceeding) (L918-920) — operationalized via Q1 applied-task gate.
- AI6 — Instrument and review (L922-928). **Deferred** to measurement.

## Current state of handoff-machinery files

- `protocols/HANDOFF_PROCESS.md` — v3.3.3 (2026-05-15). Canonical process doc. Stage 1/2/2.5/3 flow. Stage 2 pre-send coherence checklist L64-71. Stage 3 generation steps L335-418. Bundle = 11 files (self) / 12 (cross-repo). Validation-checkpoints table L530-540.
- `templates/HANDOFF_FOLDER_TEMPLATE.md` — single template defining EVERY bundle file as a `### NN_name` section. `### 00_first-message.md` L88-227 holds the current 4-item paraphrase gate (L113-144) and prompt-generation pointer to 03_PLAYBOOK (L201-216). `### 01_MANIFEST.md` L229-239. `### 01_manifest.json` L241-278 (schema + file list). `### 08_TREE.txt` L393, `### 09_EXECUTION_EVIDENCE.md` L400. Content invariants L521-529.
- There is **no `templates/handoff/` directory** and **no standalone `00_first-message.md` / `01_MANIFEST.md` template files.** Those are generated per-handoff into `docs/handoffs/{slug}/`. The prompt's `templates/handoff/08_GATE_PROBE.md` path does not match repo structure.
- `docs/decisions/ADR-42-handoff-format-v3.md` — Accepted, amended 3× (all 2026-05-09). Authority for handoff format. Amendment target for Q5.
- `docs/decisions/ADR-45-handoff-architecture-v4.md` — "Explored, not adopted"; supersession claim withdrawn 2026-05-25. Q5 explicitly does NOT reopen it.
- `protocols/PLAYBOOK.md` — model/mode/effort selection at L1245-1344 (Model Sonnet/Opus; Mode auto-accept/plan-then-auto/plan; Effort low/medium/high/xhigh; archetype examples table L1320-1331). Card extracts from here; maintenance rule (Q3 AI7) slots in after this block.
- `templates/ADR-template.md` — bullet header: Status / Date / Amends / Supersedes / Related / Decommission / Source. No tier/scale. New ADRs follow this.
- `docs/council-questions/2026-05-25-handoff-failures-evidence.md` — N=7 sender misses + 2 NEW-chat post-gate failures; "what's NOT broken" list (3-stage flow, self-containment, SHA-256, HEAD ancestor, epistemic markers). Grounds Q1/Q3/Q4 context.

## Next ADR numbers

Highest existing = ADR-54. Assigned in Phase B creation order (prompt sequencing Q1→Q3→Q2→Q4→Q5):
- ADR-55 — Q1 applied-task internalization gate
- ADR-56 — Q3 inline Prompt Generation Card
- ADR-57 — Q2 two-layer bundle contract
- ADR-58 — Q4 structured claims + symmetric verification
- ADR-42 amendment 2026-05-26 — Q5 full invariants + mechanical enforcement contract

## Operator extensions (Council did not cover)

| Extension | Where it goes |
|---|---|
| Hook selection guidance (pre-commit / PreToolUse / SessionStart-Stop / /save) | Prompt Generation Card section in `### 00_first-message.md` |
| JOURNAL update mandate per prompt (per ADR-49) | Mandatory prompt skeleton section |
| Workflow update mandate (PLAYBOOK/templates when process changes) | Mandatory prompt skeleton section |
| Git workflow (feature branch + multiple revertable commits + no auto-push) | Mandatory prompt skeleton section |

## Conflicts / deviations resolved with operator before execution

1. **Template form.** Prompt assumed standalone `templates/handoff/08_GATE_PROBE.md` etc. Repo defines all bundle files as sections inside `templates/HANDOFF_FOLDER_TEMPLATE.md`. **Resolution:** add new `### 10_GATE_PROBE.md` / `### 11_CLAIMS.md` sections and edit `### 00_first-message.md` / `### 01_MANIFEST.md` / `### 01_manifest.json` sections in place. Avoids a competing definition surface (CLAUDE.md anti-pattern: duplicate content between files).
2. **File-number collision.** Prompt's `08_GATE_PROBE.md` / `09_CLAIMS.md` collide with existing `08_TREE.txt` / `09_EXECUTION_EVIDENCE.md`. **Resolution:** use `10_GATE_PROBE.md` / `11_CLAIMS.md`; no renumber of existing files. Bundle count 11/12 → 13/14.
3. **Card taxonomy.** Prompt's example card omits Mode and `xhigh`. Live PLAYBOOK uses Model/Mode/Effort with `xhigh`. **Resolution:** card mirrors PLAYBOOK's actual taxonomy to honor Q3 anti-drift mandate (AI7).
4. **No ADR-39 registry churn.** GATE_PROBE/CLAIMS are sections of an already-registered template (not new tracked files), so no ADR-39 registry amendment is required.

## No conflicts between Council decisions and existing ADRs

- Q5 vs ADR-42: amendment, not contradiction — ADR-42 already mandates full invariants; Q5 adds integrity tracking + executor-gate contract.
- Q5 vs ADR-45: aligned — both keep full invariants; ADR-45 stays not-adopted.
- Q2 vs ADR-42: ADR-57 extends the bundle contract (adds operational layer) — recorded as new ADR per Council AI5.
- Q1/Q3/Q4 vs ADR-42/HANDOFF_PROCESS: template/process amendments, consistent with the v3.x amendment history pattern.
