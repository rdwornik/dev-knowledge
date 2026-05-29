# ADR-56: Inline Prompt Generation Card

- **Status:** Accepted
- **Date:** 2026-05-26
- **Related:** ADR-42 (handoff format v3), ADR-55 (applied-task gate — same `00_first-message.md`), `protocols/PLAYBOOK.md` (model/mode/effort selection — rationale source)
- **Decommission:** the "generate prompt(s) per `03_PLAYBOOK` conventions" pointer in `templates/HANDOFF_FOLDER_TEMPLATE.md` `### 00_first-message.md` Prompt-generation block (replaced by the inline card in this session's Phase C amendment)
- **Source:** AI Council debate Q3, 2026-05-26 — `docs/decisions/transcripts/council-out-20260526_144228-pick-2026-05-25-handoff-council-Q3-procedural-competence-transfer.md` (Recommended Decision L820-863; Action Items L885-931)

## Context

The handoff bundle ships full `PLAYBOOK.md` and tells the NEW chat to "generate
prompt(s) per `03_PLAYBOOK` conventions." This does not reliably reproduce the
procedure.

- `docs/research/2026-05-25-handoff-failures-evidence.md`: operator observed the
  NEW chat "forgets how to create prompts" ("czat zapomina jak tworzyć promty,
  nie wiem, jaki algorytm ma dokonywania decyzji, czy te prompty są, z jakim
  modelem"). Shipping the full reference doc did not transfer the procedure.
- Constraint (ADR-45 Context L79-86): the browser chat **cannot read the
  filesystem**, so a pointer to a doc is only useful if the doc is uploaded — and
  even uploaded, the full PLAYBOOK did not reproduce the procedure at point of
  use.

The procedure must be **in the actual chat context at the point of use**, as a
compact operational extract — not a pointer, not the full rationale doc.

## Decision

Keep prompt-generation authority in the **NEW browser chat**. Replace the
PLAYBOOK-pointer with a **self-contained inline Prompt Generation Card** in
`00_first-message.md`.

Card mandatory components:
- **Decision algorithm:** classify task → choose model/mode/effort → fill
  skeleton → validate.
- **Task archetype → model + mode + effort table**, mirroring the live PLAYBOOK
  taxonomy (Model: Sonnet/Opus; Mode: auto-accept/plan-then-auto/plan; Effort:
  low/medium/high/xhigh).
- **Mandatory prompt skeleton sections** every generated Claude Code prompt must
  contain — including the operator extensions (hook selection, JOURNAL update per
  ADR-49, workflow-update mandate, git workflow).
- **Fallback rule:** `uncertain/mixed -> Opus + higher effort + operator review`.
- **2-3 worked exemplars** (one mechanical/Sonnet, one judgment-heavy/Opus,
  optionally one escalation case).

Authority and duplication:
- The card is the **operational extract**; PLAYBOOK remains the **rationale and
  edge-case source**. This is an intentional duplication pattern.
- **Maintenance rule:** any change to prompt conventions must update BOTH the
  PLAYBOOK rationale and the inline card. Drift between them is a process bug.
- **Size budget:** ≤200 lines for the card. If it cannot fit, revisit
  authority/mechanism rather than letting it sprawl.

**Deviation from prompt's example card.** The card mirrors PLAYBOOK's actual
Model/Mode/Effort taxonomy (including Mode and `xhigh`), not a reduced
Model+Effort table, precisely to honor the anti-drift maintenance rule.

## Consequences

- The procedure reaches the NEW chat where it is used; no filesystem
  dereference required.
- Authority is unchanged (browser chat), avoiding an unevidenced architectural
  move to Claude Code.
- Introduces a maintained duplication (card vs PLAYBOOK) — accepted, governed by
  the maintenance rule + length budget.

## Risks (from Q3 risk register, L865-883)

- **Card bloat recreates the PLAYBOOK problem** → strict size budget; if it can't
  fit, revisit mechanism rather than sprawl.
- **Drift between PLAYBOOK and card** → explicit maintenance rule + generation
  checklist.
- **Exemplars become overfit templates** → keep few and varied; algorithm/table
  outrank examples.
- **Mixed/ambiguous tasks forced into wrong row** → explicit uncertain/mixed
  escalation rule.
- **Receiver still ignores the inline procedure** → measure over real handoffs;
  if failure persists, revisit splitting/relocating authority.
- **Skeleton underspecified** → mandatory fields defined in the skeleton, not
  high-level advice.

## Alternatives considered

- **Keep PLAYBOOK pointer** — rejected: proven not to reproduce the procedure.
- **Move authority to Claude Code** — rejected: unevidenced architectural change;
  browser chat is where operator intent is shaped.
- **Separate card file** — rejected: reintroduces filesystem indirection the
  browser chat cannot resolve.

## Trace

Measurement plan (≥10 handoffs: malformed structure, wrong model/effort, operator
"forgot procedure" reports, predefined reconsideration thresholds) deferred to a
BACKLOG measurement entry per Council AI6.

---

## Amendment 2026-05-29 — evidence file relocation

> Append-only reference correction per ADR-39 (immutable body preserved). Grounds:
> `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` finding E1.

The Context section above cites the empirical-basis evidence file at
`docs/research/2026-05-25-handoff-failures-evidence.md`. That file was relocated to
**`docs/archive/2026-05-25-handoff-failures-evidence.md`** by the 2026-05-28
ADR-60 archive triage. The original path in the body is retained for historical
accuracy; the current canonical path is the `docs/archive/` one.
---

## Amendment 2026-05-29 — Superseded by v4

HANDOFF_PROCESS.md was rewritten as v4 on 2026-05-29 as a radical
simplification. v3.x content preserved at protocols/archive/HANDOFF_PROCESS_v3.4.md
for historical reference. The Q1-Q5 architectural concepts captured in this ADR
(claims / scope / probe / manifest / ratification) are simplified in v4:
- Claims -> inline narrative in 04_RECENT, cross-verified by CC in Phase 2
- Scope -> embedded in 05_NOW narrative
- Gate probe -> replaced by operator-side comprehension check at 06_QUESTIONS
- Manifest -> no JSON sidecar; bundle structure declared in README.md
- Ratification -> replaced by operator escalation ladder (Tier 1/2/3)

Decision body preserved as historical record.
