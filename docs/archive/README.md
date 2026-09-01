# archive/ — Pending-Classification Zone

Per ADR-60 amendment 2026-05-27.

Holding zone for artifacts whose destination isn't yet decided. Reviewed periodically; each item is either:

- deleted (git history retains it), or
- promoted to `decisions/`, `audits/`, `handoffs/`, `diagrams/`, or authored into an ADR.

Not a dumping ground — a triage queue. If something sits here across two reviews with no decision, default to deletion.

**Exemption class, added 2026-08-26 by operator ruling (register `protocols/STANDING_RULINGS.md` section W, ruling W6).** A file may be stamped `retention: exempt-permanent · next-review: none` when it is cited **only** by immutable or append-only surfaces — ADRs, audits, handoffs, `JOURNAL.md`, `LESSONS.md`. For such a file deletion is not a judgement call but a **structural impossibility**: the citing surfaces cannot be re-pointed, so deleting the target manufactures dead locators that no later act can repair. This is the same referential argument **ADR-100** ratified for `docs/audits/`. A stamped file has had its review — the rule FIRED and returned KEEP — and it does **not** re-enter the past-due queue. The stamp is a blockquote at the top of the file naming the reviewer, the date, the citation count and the ADRs among the citers.

## Current contents (newest first)

Entered as 14 files from `research/` and `council-questions/` (2026-05-27 taxonomy-simplification).
**First review: 2026-05-28** — 7 council-out transcripts promoted; 7 external-research / scoping / evidence files kept pending second review.
**Second review: 2026-08-26 — FIRED, and the verdict is KEEP for all seven.** The operator acted as reviewer 2 in the endgame governance session. Measured before deciding, not asserted: the seven carry **45 citations between them (4–13 each), and every real citer is an immutable or append-only file** — including **ADR-32** (handoff-patterns-external-research) and **ADR-55/56/57/58** (handoff-failures-evidence), plus `JOURNAL.md`, `protocols/archive/HANDOFF_PROCESS_v3.4.md` and a handoff bundle manifest. All seven are stamped `exempt-permanent`. **This closes the drift recorded at `docs/audits/2026-08-26-technical-hub-diagnostic.md` §6.3** — the rule had never fired in 90 days; it has now fired, and it returned the branch the rule always had (*"either deleted … or promoted"*) rather than the deletion default.
**2026-08-09 research corpus landed 2026-08-10** — 6 external research memos (below), first review pending; they are the evidence base the plan-v3 ratification batch rules from.
**Usage-telemetry design landed 2026-08-14** — a 7th memo from the same 2026-08-09 commissioning wave, landed separately (see below); carries a 3-line provenance header, unlike the byte-identical six.

### 2026-08-14 — usage-telemetry design (1 memo, commissioned 2026-08-09, landed 2026-08-14)

- `2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md` — usage telemetry for a solo local-first methodology ecosystem: SQLite WAL + structlog event log (8 event types: `check_run`/`hook_run`/`blocker_fired`/`dispatch_invoked`/`agent_session`/`test_run`/`mutation_run`/`dep_scan`), `rich`/`plotext` + Datasette read surfaces; explicit do-not-adopt verdicts on OpenTelemetry/Prometheus+Grafana/Zabbix/Splunk; feeds intake #29 §S3a (Fold A)

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

## Retired-canonical-doc class (added 2026-09-01, [#614] lane-e-5)

**`VISION.md` does NOT enter the pending-classification queue above, and the distinction
matters.** Every other entry in this folder sits here because its destination is
*undecided* — the periodic-review default (§"How to review") is to delete or promote
once a decision is reached. `VISION.md`'s disposition is **already decided**: ADR-114
(Accepted 2026-08-29) retired it from the mandatory canonical set, `canonical_docs.py`'s
`CANONICAL_RETIRED` registers the retirement, and this lane executed the hub's own
relocation — `git mv VISION.md docs/archive/VISION.md`, byte-identical — as step one of
ADR-114 option (C)'s sequenced nine-repo filename migration (`docs/audits/2026-09-01-technical-dc3-split.md`
§4). It is exempt from the "sits here across two reviews → default to deletion" rule for
the same referential reason the 2026-08-26 exemption class states: it is still read by
`gen_handoff._vision_extract`'s retired-tier fallback and still shape-checked by
`canonical_docs.CANONICAL_SPINE`, so deleting it is not this folder's call to make. It
also does not follow this folder's `YYYY-MM-DD-{slug}.md` naming convention below — a
relocated canonical doc keeps its own name (`git log --follow` needs the identity stable),
the same way a promoted file keeps its name on the way *out* of this folder.

Next act on this file, if any, is [#621]/[#622] (the fleet-wide migration) or a further
ADR-114 ruling — not a periodic archive review.

## Naming convention

`YYYY-MM-DD-{descriptive-slug}.md` — same as the live `docs/` folders, so a file's date is visible on archive too.

## How to review

1. Open the file. Skim for what's still actionable.
2. If actionable → `git mv` to the correct live folder (preserves history).
3. If superseded / one-shot value already extracted → `git rm`.
4. If still genuinely "don't know" after two passes → `git rm` (the periodic-review threshold).
5. **Before any `git rm`, resolve the file's citers.** If every citer is immutable or append-only, the answer is not deletion — stamp it `exempt-permanent` per the exemption class above and record the count. Deleting a file cited from an ADR breaks that ADR permanently.

The full archive lifecycle is in `protocols/PLAYBOOK.md` "docs/ folder taxonomy".
