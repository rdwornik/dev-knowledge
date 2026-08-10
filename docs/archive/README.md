# archive/ — Pending-Classification Zone

Per ADR-60 amendment 2026-05-27.

Holding zone for artifacts whose destination isn't yet decided. Reviewed periodically; each item is either:

- deleted (git history retains it), or
- promoted to `decisions/`, `audits/`, `handoffs/`, `diagrams/`, or authored into an ADR.

Not a dumping ground — a triage queue. If something sits here across two reviews with no decision, default to deletion.

## Current contents (newest first)

Entered as 14 files from `research/` and `council-questions/` (2026-05-27 taxonomy-simplification).
**First review: 2026-05-28** — 7 council-out transcripts promoted; 7 external-research / scoping / evidence files kept pending second review.
**2026-08-09 research corpus landed 2026-08-10** — 6 external research memos (below), first review pending; they are the evidence base the plan-v3 ratification batch rules from.

### 2026-08-09 research corpus (6 memos, landed 2026-08-10)

External research memos commissioned by the operator 2026-08-09 and landed byte-identical from
the source artifacts (no header injected — provenance is this list). Each filename carries its
source `wf-` id as a trailing token, so the landed file resolves back to the commissioning
artifact without depending on this list surviving. Distillate: `docs/audits/2026-08-10-technical-research-corpus-distillate.md`.
Promotion target is the intake / ADR each proposal feeds — not promotion of the memo itself.

- `2026-08-09-research-code-style-doctrine-wf-8a83eb70.md` — code-style doctrine for an LLM-written Python fleet: what is mechanizable (size/complexity ceilings, import contracts, ratchets) vs unenforceable taste (OO vs functional); feeds intake #31
- `2026-08-09-research-dependency-ontology-graph-wf-f6851745.md` — one queryable dependency/ontology graph: derive-and-commit JSONL edge log + DuckDB/SQLite, grimp for the import graph; names the task↔file `footprint:` gap as highest-leverage
- `2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md` — agent telemetry + fair model comparison: JSONL transcript / OTel extraction, paired within-task measurement design, and **the seeded-defect corpus spec** (gates `[#491]`/`[#492]`/Copilot)
- `2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` — multi-provider portability: AGENTS.md as the one portable layer, `@AGENTS.md` import for Claude Code, generation-plus-checksum over symlinks on Windows; Kimi swap as validated fallback with a ToS boundary
- `2026-08-09-research-session-continuity-decision-lifecycle-wf-fafd931b.md` — session continuity + decision lifecycle: the bundle design is ahead of practice, retirement is behind; capped intake with Parked/Rejected, ADR sunset dates, ADR-landing predicates
- `2026-08-09-research-compute-placement-wf-1dc18e42.md` — compute placement: fix the laptop first (Stage 0, $0), then one CLI-provisioned Linux VPS; toolchain-pinning + gates-ran attestation is the gating precondition

### Pre-existing contents

- `2026-06-05-agent-automation-external-research-note.md` — external research: cloud-agent infrastructure (E1/CREAO) + CC automation stack (E2 Desktop scheduler, E3 /goal principles); encodes dispositions for #85/#86/#84(a); verify-before-encode applies to all E2 platform claims — keep pending promotion / n=2-gate clearance
- `2026-06-03-dynamic-workflows-research-note.md` — #80 deliverable: Dynamic Workflows feature research + pattern→use-case mapping (Amendments A 2026-06-03 + B 2026-06-05); landed 2026-06-05 per the external-research convention — keep pending promotion to the adoption ADR (#84(b))
- `2026-05-25-handoff-failures-evidence.md` — empirical evidence cited by the 5 handoff-methodology Council questions; referenced in ADR-55/56/57/58 and HANDOFF_PROCESS.md — keep until superseded
- `2026-05-25-handoff-methodology-council-index.md` — index of the Council question set that produced ADR-55–58; keep as provenance record pending second review
- `2026-05-17-kimi-k2-scoping.md` — Kimi K2 model scoping (BACKLOG #243; awaiting promotion to ADR or audit)
- `2026-04-27-handoff-patterns-external-research.md` — external Perplexity research on handoff patterns; referenced in ADR-32
- `2026-04-24-multi-agent-debate-patterns.md` — external research on multi-agent LLM debate frameworks
- `2026-04-24-claude-md-best-practices.md` — external research on CLAUDE.md structuring best practices
- `2026-04-23-llm-dev-patterns-2026.md` — external Perplexity research on LLM dev patterns 2026

## Promoted (2026-05-28 first review) → `docs/decisions/transcripts/` (destination since DELETED)

All 7 are AI Council debate outputs (identical structure to the council-out-* files that lived in transcripts/). Original filenames retained.

> **Pointer correction 2026-07-25.** The destination folder `docs/decisions/transcripts/` was **deleted 2026-07-22** (operator ruling — council-in-ADR output retired; decisions live in the ADRs, git history retains the raw transcripts; the ADR-77 guard stays armed and the folder must not be recreated — CLAUDE.md §4). The seven files below are therefore **no longer on disk**; this section is retained as the historical record of where they went, not as a live path. Recover any of them from git history.

- `2026-04-27-handoff-patterns-council-research.md` — Council research debate: handoff patterns for solo developers
- `2026-04-24-council-29-spec-kit-kiro.md` — Council debate #29: Spec Kit / Kiro spec-driven workflows
- `2026-04-23-council-28-community-patterns.md` — Council debate #28: community LLM dev patterns
- `2026-04-15-council-26-tach-adoption-corp-monorepo.md` — Council debate #26: Tach import enforcement adoption
- `2026-03-30-council-25-diagrams-corp-monorepo.md` — Council debate #25: architecture diagram format/location
- `2026-03-29-council-research-new-models.md` — Council research: new LLM models/APIs Mar 2026
- `2026-03-29-council-browser-handoff.md` — Council debate: browser→CLI handoff strategy

## Naming convention

`YYYY-MM-DD-{descriptive-slug}.md` — same as the live `docs/` folders, so a file's date is visible on archive too.

## How to review

1. Open the file. Skim for what's still actionable.
2. If actionable → `git mv` to the correct live folder (preserves history).
3. If superseded / one-shot value already extracted → `git rm`.
4. If still genuinely "don't know" after two passes → `git rm` (the periodic-review threshold).

The full archive lifecycle is in `protocols/PLAYBOOK.md` "docs/ folder taxonomy".
