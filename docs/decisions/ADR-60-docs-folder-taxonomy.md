# ADR-60: docs/ Folder Taxonomy — Semantic Roles

- **Status:** Accepted
- **Date:** 2026-05-27
- **Amends:** Builds on ADR-34 (file naming), ADR-43 (transcript routing — unchanged), ADR-48 (governance proportionality). Implements Option B of `docs/audits/2026-05-25-council-pipeline-proposal.md`.
- **Decommission:** none (additive convention + one folder created, one archived). The `research/` catch-all role is narrowed, not removed.
- **Source:** Operator decision (Rob, 2026-05-27). No Council transcript. Grounded in the 2026-05-25 Council-pipeline audit (finding A1 HIGH) and operator friction ("research są niektóre inputem, outputem — zupełnie nie ma sensu").

## Context

The 2026-05-25 Council-pipeline audit (`docs/audits/2026-05-25-council-pipeline-audit.md`, finding A1 HIGH; reinforced by A2/A3/G) found that `docs/research/` conflated three different semantic roles:

- **INPUTS** — Council debate question sets, evidence files, set indexes (Stage-0/1 working artifacts for the pipeline).
- **OUTPUTS** — finished audit chains, validation reports, forensics, mechanism-discovery references.
- **TRANSIENT** — preflight snapshots and other historical-only scratch.

Because the folder name carried no role, neither a reader nor an agent could tell what a file *was* from where it lived. The operator's requirement, mirroring ADR-59's visual-consistency goal but at the semantic level: a file's folder should tell you what it is.

A secondary undecided artifact class — `docs/tech-radar/` — held a single dormant entry (`2026-Q2.md`) with no review cadence (BACKLOG "Decide future of `docs/tech-radar/`").

The Option B proposal recommended the smallest change that fixes the root: a dedicated staging home for pipeline inputs, reclassification of the mis-filed 2026-05-25/26 artifacts, and a codifying ADR so the convention does not re-drift. Per the proposal's proportionality principle (ADR-48), the heavier Option C (stage-named folders + manifest) was rejected as disproportionate to a low-volume solo pipeline.

## Decision

Each `docs/` subfolder serves **one** semantic role. The role is the contract; the folder name encodes it.

### Roles

| Folder | Role | Contents |
|--------|------|----------|
| `audits/` | OUTPUTS | Audit reports, validation reports, refresh docs, forensics, mechanism-discovery references — finished, date-prefixed, immutable post-merge |
| `council-questions/` | INPUTS | Council debate question sets, evidence files, set indexes — staging for the pipeline |
| `decisions/` | OUTPUTS | ADRs (`ADR-NNN-topic.md`) + `transcripts/` subfolder (Council debate outputs, routed per ADR-43) |
| `handoffs/` | OUTPUTS | Per-session handoff bundles (dated directories) — out of scope here, already operator-clear |
| `research/` | WORKING | Exploratory pre-decision scratchpad; matures into the folders above |
| `archive/` | ARCHIVED | Superseded, dormant, or transient artifacts; reversible — anything can resurface |

### Rules

1. **One role per folder.** A file's location declares its semantic role.
2. **Documented purpose.** Each subfolder's role is self-evident from its name except `research/`, which carries a `README.md` because "working scratchpad" is non-obvious. `council-questions/` also carries a `README.md` describing the pipeline lifecycle and the Council CLI frontmatter contract.
3. **Date-prefixed naming** (`YYYY-MM-DD-{slug}.md`) for time-sequenced artifacts (consistent with ADR-34 and ADR-59's date-sorted-folder note).
4. **Lifecycle — files migrate as their role resolves** (always `git mv`, preserving history):
   - `research/` → `audits/` when matured into a finished audit/report/validation
   - `research/` → `decisions/` when matured into an ADR
   - `research/` → `council-questions/` when becoming a Council debate input
   - any folder → `archive/` when dormant or superseded
5. **Append-only / immutable records are not rewritten on move.** ADRs, transcripts, handoffs, and `JOURNAL.md` entries that reference a since-moved file are point-in-time records — they were accurate when written and are left intact (repo critical rules #2/#3). Only living docs (BACKLOG, PLAYBOOK, HANDOFF_PROCESS, READMEs) and a migrated file's own internal cross-references are updated to current paths.
6. **ADR-43 routing is unchanged.** Council transcripts continue to land in `docs/decisions/transcripts/` via `target-project:`. This taxonomy does not touch routing.

### `tech-radar/` disposition

Archived to `docs/archive/tech-radar/` (operator decision 2026-05-27). The single dormant entry is preserved, not deleted — reversible if quarterly tech-radar work resumes.

### `research/` retained semantic

The folder is **kept** (not deleted) with an explicit `README.md` codifying its WORKING role. Genuinely exploratory pre-2026-05-25 content (council research debates, external research, best-practices and scoping drafts) legitimately remains; only the mis-filed inputs/outputs/transient artifacts were reclassified.

## Consequences

**Positive:**
- Folder name encodes semantic role; operator and agents reason about a file's lifecycle by location.
- Pipeline-audit finding A1 (HIGH) closed; `council-questions/` separates inputs from outputs.
- A future audit-tool check can validate folder semantics (BACKLOG candidate — out of scope here).

**Risks / trade-offs:**
- Reclassification touched cross-references; mitigated by per-phase commits (independently revertable) and a comprehensive grep, with append-only/immutable records intentionally left as point-in-time history (Rule 5) rather than edited.
- Retaining `research/` adds a sliver of taxonomy complexity vs. a flat delete, but reflects the real workflow (early exploratory work happens before a destination is known).
- Some artifacts have a hybrid lineage (e.g., the multi-stage pipeline chain); the destination is a judgment call, documented per-file in the 2026-05-27 JOURNAL entry.

## Migration scope (2026-05-27 session)

- Created `docs/council-questions/` (+ README); migrated 5 Council Q-files + evidence + set index from `research/`.
- Migrated the pipeline audit chain (discovery/audit/proposal/index), debate forensics, mechanism discovery, and handoff-stabilization discovery + validation from `research/` to `audits/`.
- Archived the consolidation preflight (transient) to `docs/archive/2026/`.
- Archived `docs/tech-radar/` to `docs/archive/tech-radar/`.
- Retained `research/` with a WORKING-semantic README.

Full file-by-file record in the 2026-05-27 `JOURNAL.md` entry.

## Future work

- Audit-tool extension to validate folder semantics (BACKLOG candidate).
- Periodic review of `archive/` contents.

## Related

- `docs/audits/2026-05-25-council-pipeline-audit.md` — finding A1 (HIGH)
- `docs/audits/2026-05-25-council-pipeline-proposal.md` — Option B (recommended)
- ADR-59 — universal visual repository pattern (the visual-consistency sibling to this semantic-consistency decision)
- ADR-43 — cross-project transcript routing (unchanged)
