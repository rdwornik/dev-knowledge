# corp-monorepo Governance Trim — Rollout Plan

<!-- scope: meta -->

**Date:** 2026-05-17
**Subject repo:** `C:\Users\1028120\Documents\Dev\corp-monorepo`
**Author:** Claude Code (Opus 4.7) in `.dev-knowledge` (this repo)
**Purpose:** Plan a future session that rolls the `.dev-knowledge`
documentation-governance simplification (ADR-48 / ADR-49 / ADR-50 +
decommissioning discipline) into `corp-monorepo`, scaled to its size.
**Status:** Preparation only — this document does not execute changes
against `corp-monorepo`. A future Claude-Code session executes the
rollout using this document as its design spec.
**Anchor ADRs:** ADR-33 (VISION universalization), ADR-38 +A3 (universal
repo architecture, ARCHITECTURE.md root-placement amendment), ADR-48
(audit trim + governance-admission rule), ADR-49 (CHANGELOG /
BACKLOG_ARCHIVE retirement), ADR-50 (machine-document encoding).
**Reference audit:**
`docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`
(the only prior systematic read of corp-monorepo's governance surface;
treat as historical — discovery in §4 supersedes any state claim here).

---

## 1. Goal & context

### 1.1 What the rollout achieves

Shrink `corp-monorepo`'s documentation-governance surface to match the
ecosystem-wide trim already accepted in `.dev-knowledge` and proven on
`ai-council`:

- Audit machinery (any in-repo doc-format checks) reduced to
  structural-only checks per ADR-48.
- `CHANGELOG.md` and `BACKLOG_ARCHIVE.md` retired per ADR-49; git
  history + JOURNAL `Did/Result/Changes/Abandoned/Next` shape replaces
  CHANGELOG; done backlog items leave the file with no archive
  tombstone; significant abandons → lightweight decision-note in
  `docs/decisions/`.
- Any locally-defined enforced doc-format ADRs (corp-monorepo
  equivalents of `.dev-knowledge`'s ADR-46/47, if any exist) demoted to
  non-enforced conventions.
- Scope-tag enforcement retired wherever it exists (corp-monorepo's
  `.dev-knowledge`-style `<!-- scope: X -->` HTML tags, if any).
- Deterministic header normalizer adopted in place of cosmetic audit
  checks.
- Decommissioning discipline adopted: every supersession or relocation
  carries a `Decommission:` field on the new ADR + matching status
  flips on the superseded artifact.

### 1.2 Why corp-monorepo is the next target

- Only Scale-L repo in the ecosystem (per `ARCHITECTURE.md` /
  `VISION.md` tier classification).
- Largest accumulated governance debt — the 2026-04-21 audit catalogued
  numerical drift, reference drift to non-existent files, and stale
  pre-consolidation language across CLAUDE.md, HANDOFF.md,
  CHANGELOG.md, and README.md.
- Highest leverage consumer of the trim: every saved
  format-housekeeping hour is amortised across the ecosystem's largest
  doc surface.

### 1.3 Scope of THIS plan document

- This document is the design spec for a future executing session.
- It does not perform the rollout. It does not write a Claude-Code
  prompt for the rollout.
- The executing session's prompt is authored separately, by the
  operator, after this plan is reviewed.

---

## 2. The proven model — recap

The model below is what an executing session implements. It is what
`.dev-knowledge` already runs on itself and what `ai-council` adopted in
the 2026-05-17 session-sync rollout.

### 2.1 Audit tool — structural-only

- An audit check is admitted only if it verifies a binary, deterministic
  structural fact (file present / section present / required key
  present).
- Format-detail checks (header levels, blank-line counts, ordering,
  heading-text patterns, entry-body required fields) are removed.
- Cosmetic uniformity that is still wanted (uniform header levels) is
  handled by a deterministic auto-format normalizer at write-time, not
  by an audit at read-time.

### 2.2 ADR-48 governance-admission rule

A new check or rule is admitted only if all three are true:

1. It solves a recurring real failure (not a hypothetical or one-off).
2. It is fully automatable (no human-judgement step).
3. It has low ongoing cost (no recurring maintenance burden
   proportional to repo growth).

Otherwise it remains a non-binding convention. This rule applies to
every check / rule proposed during the rollout itself.

### 2.3 Past-recording file consolidation (ADR-49)

- `CHANGELOG.md` is removed. The change record is git history
  (descriptive Conventional-Commits messages) + the `Changes:` line in
  each JOURNAL entry. Commit-message quality becomes load-bearing.
- `BACKLOG_ARCHIVE.md` is removed. Done backlog items simply leave
  `BACKLOG.md`; their trace is git history.
- A *significant* abandoned backlog item is recorded as a lightweight
  decision-note in `docs/decisions/`, not as a JOURNAL line — preserving
  structured rationale that git cannot hold.
- JOURNAL is the single human past-narrative, per-entry structure
  `Did / Result / Changes / Abandoned / Next`.
- LESSONS (if present in corp-monorepo's governance — discovery §4) is
  kept standalone as an agent-consumed file.

### 2.4 Machine-document encoding (ADR-50)

- Machine-layer files (CLAUDE.md, LESSONS, ARCHITECTURE, ADRs, handoff
  bundles) use restricted structured markdown — fixed section headers,
  bullet lists, key-value blocks, minimal prose, minimal tables.
- English, reliability over token-efficiency when they conflict.
- Per-file-type schemas remain advisory, not CI-enforced.
- Handoff bundle keeps multi-file structure (operator override of
  debate) — optimisation within that structure.

### 2.5 Scope-tag retirement

- The `.dev-knowledge` ADR-27 scope-tag vocabulary
  (`dev | llm | hybrid | runtime | meta`) and its pre-commit validation
  are retired.
- Existing `<!-- scope: X -->` HTML comments and `[scope: X]` LESSONS
  tags are LEFT IN PLACE as informal metadata. Nothing automated
  enforces or audits them.
- New sections do not require scope tags.

### 2.6 Decommissioning discipline

- Every ADR that supersedes or relocates an artifact MUST carry a
  `Decommission:` header field listing the prior artifact + its
  disposition (deleted / archived / status-flipped).
- The superseded artifact MUST receive a status flip (e.g.,
  `Status: Demoted` / `Superseded by ADR-NN`) in the same PR — orphans
  are the failure mode this discipline prevents.
- Codified in `.dev-knowledge` PLAYBOOK ("Supersession & decommissioning"
  subsection), ESSENTIALS (condensed rule), and `templates/ADR-template.md`
  (the `Decommission:` field is templated).

### 2.7 ai-council as the proof point

ai-council adopted the model in the 2026-05-17 session-sync rollout
(see `JOURNAL.md` entries for that date and the 13-file handoff bundle
at `docs/handoffs/2026-05-17-ai-council-session-sync/`). The rollout was
fast because ai-council's governance surface is small: no CHANGELOG with
meaningful history, no BACKLOG_ARCHIVE, no AGENTS.md / CONTRIBUTING.md,
no Tach, no scope tags, ~28 tests. corp-monorepo will be slower for
structural reasons enumerated in §3.

---

## 3. Monorepo-scale delta analysis

This is the core of the plan. For each delta dimension: the difference
from ai-council, and what that difference means for the rollout.

### 3.1 Scale-L test suite (~2,500+ tests vs ai-council ~28)

- Every phase commit MUST be gated on
  `pytest -x --tb=short && ruff check && tach check && git status`
  before proceeding (per core-invariants #2).
- Test-suite breakage at any phase is grounds for revert, not patch.
- The rollout MUST NOT touch test files.

### 3.2 `src/corp/` Python namespace + Tach enforcement

- `tach.toml` is the authoritative module-to-layer assignment.
  `.pre-commit-config.yaml` runs `tach check`. `.github/workflows/tach.yml`
  enforces in CI.
- None of these are documentation-governance machinery. The trim MUST
  NOT touch them.
- AGENTS.md currently delegates the import-direction check to Tach
  (`AGENTS.md:89` per the 2026-04-21 audit). This delegation is correct
  and stays.

### 3.3 CHANGELOG.md history depth (asymmetric with ai-council)

corp-monorepo's `CHANGELOG.md` carries semver lineage starting from
`[1.0.0] 2026-03-28` (consolidation baseline) with subsequent dated
entries (Apr-21 hotfix, ADR-27 drafting note, etc.). ai-council's was
effectively empty.

- Hard deletion is not symmetric.
- Three options for preservation, decision deferred to operator
  (see §9):
  1. **Hard delete** — git history is authoritative; the final
     deletion commit body itemises what was removed.
  2. **One-time archive snapshot** — copy `CHANGELOG.md` to
     `docs/archive/CHANGELOG_AS_OF_2026-MM-DD.md` as a frozen point-in-time
     record, then delete the live file.
  3. **Final commit body manifest** — include the file's last content
     inline in the deletion commit message.
- Whichever option wins, the deletion is one commit, reverted by one
  revert.

### 3.4 BACKLOG.md state (unknown from this bundle)

- Discovery (§4) must determine whether `BACKLOG.md` exists, whether
  any `BACKLOG_ARCHIVE.md` exists, and the shape of any entries.
- If `BACKLOG_ARCHIVE.md` is absent, ADR-49's "archive retired" step is
  a no-op.
- If present, retirement follows the same delete pattern as §3.3.
- The `[done]→leave-file` discipline is a forward-only convention
  change; existing entries are not retroactively rewritten.

### 3.5 ADR inventory + ADR-46/47 equivalents

- The 2026-04-21 audit identified ~29 ADRs. corp-monorepo's ADR-27 is
  `safety-invariants`, unrelated to `.dev-knowledge`'s ADR-27 (scope
  tags) or ADR-46/47 (cross-repo dated-entries / BACKLOG organization).
- Discovery must scan `docs/decisions/` to determine whether
  corp-monorepo carries any ADRs that enforce doc-format checks
  retired by ADR-48 — if not, no demotions are needed.
- Demotion (if needed) means adding `Status: Demoted to convention
  (superseded by .dev-knowledge ADR-48)` and a `Decommission:` field
  to each demoted ADR.

### 3.6 Audit machinery — distinguishing in scope from out of scope

corp-monorepo carries audit-adjacent scripts. The trim addresses each
by name:

| Script | Scope of trim |
|---|---|
| `scripts/dev-check.ps1` | OUT — pre-merge quality gate (tests + lint + tach). Mechanical, not doc-format. |
| `scripts/run-all-tests.ps1` | OUT — test runner. |
| `scripts/update_handoff.py` | CONDITIONAL — if it writes any CHANGELOG.md reference, the reference is updated/removed; the script itself may stay. |
| Tach pre-commit / CI | OUT — architectural enforcement. |
| Any `scripts/validate_*` doc-format scripts | IN — candidates for removal per ADR-48. Discovery enumerates. |
| Codex audits in `docs/audits/` | OUT — frozen-on-write artifacts, not machinery. |

### 3.7 Two coexisting handoff patterns (adjacent debt, NOT in scope)

- `docs/HANDOFF.md` (master, scripted by `update_handoff.py`, last
  regenerated 2026-03-29 per the 2026-04-21 audit) AND
  `docs/handoffs/YYYY-MM-DD-handoff.md` (per-session, frozen,
  n=1 as of the 2026-04-21 audit) coexist with no canonicality
  declaration.
- This collision predates ADR-48/49/50 and is unrelated to the trim.
- Routed to a SEPARATE future session. The trim updates references in
  these files only where the trim touches their content (e.g., a
  CHANGELOG.md reference).

### 3.8 Six-layer governance stack (vs ai-council's slim stack)

corp-monorepo carries (per the 2026-04-21 audit): `CLAUDE.md`,
`AGENTS.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`,
`.claude/skills/gotchas/gotchas.md`, plus `docs/decisions/ADR-NN-*.md`
(~29 ADRs). ai-council has CLAUDE.md, VISION.md, and ADRs — no
AGENTS.md, no CONTRIBUTING.md (per Council #28 gap).

- The trim touches at least: any file that references `CHANGELOG.md` or
  `BACKLOG_ARCHIVE.md`, plus the file(s) describing the JOURNAL entry
  shape, plus any file describing audit checks being retired.
- Likely edits (subject to discovery): CLAUDE.md (numerical drift +
  deleted-file refs + JOURNAL shape), CONTRIBUTING.md
  (CHANGELOG references), `docs/HANDOFF.md` (CHANGELOG references,
  count refs).
- AGENTS.md may be untouched if it does not reference past-recording
  files — discovery confirms.
- `.claude/skills/gotchas/gotchas.md` is not in scope (it is an
  empirical pattern memory, not a doc-format file).

### 3.9 Scope-tag presence (discovery-gated)

- corp-monorepo never adopted `.dev-knowledge`'s scope-tag vocabulary
  (the 2026-04-21 audit does not surface any `<!-- scope: X -->`
  occurrences).
- Discovery confirms via `grep -r "<!-- scope: " corp-monorepo/` and
  `grep -r "\[scope:" corp-monorepo/`.
- If absent: this delta is a no-op, recorded as such.
- If present (e.g., recently introduced): retire enforcement, leave the
  tags in place as informal metadata.

### 3.10 Decommissioning debt surface

The 2026-04-21 audit catalogues several reference-drift incidents:
- `docs/ARCHITECTURE.md:423-426` cites the non-existent
  `docs/audits/2026-04-21-p1-verification.md`.
- `docs/HANDOFF.md:393` cites the wrong directory (`decisions/`
  instead of `docs/decisions/`).
- `docs/HANDOFF.md:194-195` cites old `.ecosystem/` paths from before
  the 2026-03-30 elimination.
- `docs/decisions/README.md:29` index ends at ADR-21.
- `docs/diagrams/conventions.yaml:18-23` uses obsolete layer name
  "Composition" instead of canonical "interface".

The decommissioning discipline is the right hammer for this class of
debt. The rollout's scope decision (see §9) is whether to clean up:
- ONLY the references touched by the trim itself, OR
- opportunistically the full audit's drift list.

Default in this plan: trim-touched references only. Adjacent drift is
routed to a separate cleanup session unless operator chooses otherwise.

---

## 4. Discovery phase (execution step ONE)

The executing session MUST complete discovery and commit its findings
BEFORE applying any trim. This is a non-negotiable phase boundary.

### 4.1 Discovery checklist

The executing session produces a discovery report capturing, for each
item below, the current observed state:

- **`CHANGELOG.md`** — exists? line count, last entry date, oldest
  entry date, semver lineage present? Y/N + evidence path:line.
- **`BACKLOG_ARCHIVE.md`** — exists? line count, entry count.
- **`BACKLOG.md`** — exists? line count, `[done]` token count
  (`grep -c "\[done\]" BACKLOG.md`), structural shape (whether entries
  match `[P{N}] [open|superseded]` pattern or some other shape).
- **ADR inventory** — count (`ls docs/decisions/ADR-*.md | wc -l`); list
  any ADR whose Status references doc-format enforcement; list any ADRs
  with no `Decommission:` field that supersede prior ADRs.
- **Audit-check inventory** — every `scripts/*.py` and `scripts/*.ps1`
  enumerated with a one-line classification (test runner / pre-merge
  gate / handoff updater / doc-format check / other). Doc-format checks
  are the rollout's targets.
- **Scope-tag presence** — `grep -rn "<!-- scope: " . --include="*.md"`
  and `grep -rn "\[scope:" . --include="*.md"` results. Zero matches
  → §3.9 is a no-op.
- **`VISION.md`** — exists? frontmatter `tier:` value? `scale:` value?
  `last_reviewed:` date? If missing, the rollout is GATED on a prior
  VISION-creation session — STOP and report.
- **`ARCHITECTURE.md` location** — repo root (compliant per ADR-38 A3)
  or `docs/ARCHITECTURE.md` (non-compliant)? Relocation is adjacent
  debt, NOT part of this trim.
- **Past-recording references** — `grep -rn "CHANGELOG.md" . --include="*.md" --include="*.py" --include="*.ps1"`
  and same for `BACKLOG_ARCHIVE.md`. Every match becomes a candidate
  edit in Phase 2/3.
- **Decommissioning debt** — limited to references that the trim will
  touch. Full reference-drift cleanup is out of scope unless operator
  expands per §9.
- **Baseline** — `pytest -x --tb=short`, `ruff check`,
  `tach check`, `git status` ALL captured to the discovery report as
  the "before" state.

### 4.2 Discovery commit

- New file:
  `docs/audits/2026-MM-DD-corp-monorepo-trim-discovery.md` (date set at
  execution time).
- One commit:
  `docs(audits): inventory corp-monorepo governance surface for trim`.
- This commit lands on the rollout branch BEFORE any trim commit. It
  is the data input for every subsequent phase decision.

### 4.3 STOP conditions surfaced by discovery

The executing session MUST stop and surface to operator (no further
phases) if discovery finds:

- `VISION.md` absent or `tier: lite` (Scale-L requires `tier: standard`
  per ADR-33). VISION creation/upgrade is a prerequisite, not a phase
  of this rollout.
- Test-suite baseline failing. Trim never starts on a red tree.
- Tach baseline failing. Same reason.
- `git status` dirty.

---

## 5. ADR-33 compliance

- Scale-L → `VISION.md` is mandatory AND must be `tier: standard` (full
  6-section template + frontmatter version, last_reviewed, owner,
  status, tier).
- Discovery (§4.1) determines current state.
- If non-compliant: rollout is gated on a prior session that creates /
  upgrades `VISION.md`. This plan does not design that work.
- If compliant: a one-line frontmatter `last_reviewed:` bump may be
  in scope for the final phase; the content is not edited by this
  rollout.

The rollout MUST NOT design or write `VISION.md` content. VISION
authorship is operator-driven and may trigger AI Council debate per
the `.dev-knowledge` model.

---

## 6. ADR-38 Scale-L compliance gaps

### 6.1 Mandatory file set (per ADR-38, including A3 amendment)

| File | Tier L mandate | corp-monorepo current state (per audit, subject to discovery) | Action in this rollout |
|---|---|---|---|
| `README.md` | YES | Present (~has module/test table) | None |
| `VISION.md` | YES (Standard tier) | UNKNOWN from this bundle — must discover | Gate per §5 |
| `CHANGELOG.md` | YES per ADR-38 — **but ADR-49 retires this** | Present | Retire per Phase 2 |
| `ARCHITECTURE.md` at repo root (A3) | YES | At `docs/ARCHITECTURE.md` (non-compliant) | ADJACENT — A3 explicitly defers |
| `BACKLOG.md` | YES (≥M) | UNKNOWN — discover | If absent, create empty per separate session |
| `src/` + `pyproject.toml` | YES | Compliant (`src/corp/`) | None |
| `docs/decisions/` (ADRs) | YES | Compliant (~29 ADRs) | None except demotions per §3.5 |

### 6.2 ADR-38 ↔ ADR-49 conflict

ADR-38 marks `CHANGELOG.md` as mandatory at Tier M+. ADR-49 retires
`CHANGELOG.md`. The conflict is real and must be resolved.

- Resolution applied in this rollout: ADR-49 supersedes ADR-38's
  CHANGELOG cell for the scope of the trim. The retirement proceeds.
- A separate ADR-38 amendment (in `.dev-knowledge`) is the proper
  long-term fix. Timing is an operator decision (see §9).

### 6.3 ARCHITECTURE.md root migration (ADJACENT)

- ADR-38 A3 (2026-05-11) mandated root placement and EXPLICITLY
  deferred the corp-monorepo migration to a separate Phase-2 prompt.
- This rollout MUST NOT migrate `docs/ARCHITECTURE.md` to root. Flag in
  the discovery report; route to a separate session.

---

## 7. Phased, revertable rollout sequence

Each phase = one commit (or a tight commit group) = independently
revertable. Each phase ends with the full verify cadence
(`pytest -x --tb=short && ruff check && tach check && git status`). A
phase that fails verification is reverted, not patched forward.

Branch: `docs/govern-trim-corp-monorepo` (or operator's preferred name).

### Phase 0 — Discovery (mandatory, blocking)

- Produce `docs/audits/2026-MM-DD-corp-monorepo-trim-discovery.md`.
- Commit:
  `docs(audits): inventory corp-monorepo governance surface for trim`.
- STOP conditions per §4.3 enforced before any subsequent phase.

### Phase 1 — Audit-tool trim

- Scope: any in-repo doc-format check (per discovery §4.1
  audit-check inventory).
- Action: delete checks that fail the ADR-48 governance-admission
  rule; keep checks that pass it.
- Affected files: `scripts/validate_*.py` (if any), associated tests,
  pre-commit config entries pointing to them.
- Commit: `chore(audit): trim doc-format checks per ADR-48`.
- Verify: tests + ruff + tach + `git status`.

### Phase 2 — CHANGELOG.md retirement

- Apply preservation policy from operator decision §9.
- Delete `CHANGELOG.md`.
- Update every reference found in discovery — CLAUDE.md, CONTRIBUTING.md,
  `docs/HANDOFF.md`, `scripts/update_handoff.py` (if it touches the
  file), README.md.
- If a relevant ADR exists in corp-monorepo, add a new ADR (or
  decision-note) recording the retirement with a `Decommission:` field
  pointing to `CHANGELOG.md` + disposition (deleted | archived
  to `docs/archive/CHANGELOG_AS_OF_2026-MM-DD.md`).
- Commit: `chore(docs): retire CHANGELOG.md per ADR-49`.
- Verify.

### Phase 3 — BACKLOG_ARCHIVE.md retirement (conditional)

- Skip if discovery shows file absent.
- Otherwise: delete the file; update references; same `Decommission:`
  discipline as Phase 2.
- Forward-only convention change for `[done]→leave-file` —
  existing entries not rewritten.
- Commit: `chore(docs): retire BACKLOG_ARCHIVE.md per ADR-49`.

### Phase 4 — ADR demotions (conditional)

- Skip if discovery surfaces no ADRs to demote.
- Otherwise: per demoted ADR, status flip to
  `Demoted to non-enforced convention (superseded by .dev-knowledge
  ADR-48)` + `Decommission:` field added.
- One commit per demoted ADR OR one combined commit named per the
  ADRs touched. Operator preference.

### Phase 5 — Scope-tag retirement (conditional)

- Skip if discovery shows zero `<!-- scope: ` or `[scope:` matches.
- Otherwise: remove any pre-commit hook entry that validates scope
  tags; leave the tags themselves in place as informal metadata.
- Commit: `chore(governance): retire scope-tag enforcement (tags
  remain informal)`.

### Phase 6 — Header normalizer + decommissioning discipline adoption

- Port the deterministic header normalizer
  (`.dev-knowledge/scripts/normalize_headers.py` is the reference)
  into corp-monorepo's `scripts/` and wire to `.pre-commit-config.yaml`
  as an auto-format hook (not an audit).
- Add a `templates/ADR-template.md` for corp-monorepo (template path
  per repo convention) carrying the `Decommission:` field.
- Add or update CONTRIBUTING.md / ARCHITECTURE.md (whichever holds the
  ADR authoring guidance) with a condensed supersession-and-
  decommissioning rule (≤5 lines, matching the ESSENTIALS pattern in
  `.dev-knowledge`).
- Commits: one for the normalizer, one for the template, one for the
  guidance edit. Each verified independently.

### Phase 7 — JOURNAL shape adoption (forward-only)

- corp-monorepo's `JOURNAL.md` exists (per 2026-04-21 audit). Adopt
  `Did / Result / Changes / Abandoned / Next` for FORWARD entries.
- Existing entries are append-only (core invariant); they are NOT
  rewritten.
- Update the JOURNAL intro blockquote (or the equivalent in
  corp-monorepo's JOURNAL convention) to describe the new shape AND
  the deprecation of the old `Did / Failed / Next` shape from the same
  date forward.
- Commit: `docs(journal): adopt Did/Result/Changes/Abandoned/Next shape`.

### Phase 8 — Verification (corp-monorepo only, no cross-repo write)

- Run `.dev-knowledge/scripts/audit.py` against corp-monorepo as a
  read-only verification step.
- Expected outcome: `vision_md` PASS (assuming §5 prerequisite met),
  `adr38_baseline` PASS, `claude_md` PASS. No format-detail checks
  exist in the trimmed audit, so no new FAILs from the trim itself.
- Record the audit result INSIDE corp-monorepo — in the closing
  JOURNAL entry's `Result:` line, and/or the trim discovery/closing
  doc under corp-monorepo's own `docs/`.
- The executing session MUST NOT write the result into
  `.dev-knowledge/docs/audits/`. A Layer-3 (Claude Code) session does
  not directly edit Layer-2 (`.dev-knowledge`) files — write-back is
  via Layer-1 handoff only (PLAYBOOK three-layer rule) — and a
  cross-repo path cannot land on the corp-monorepo rollout branch.
- Propagating the audit result back to `.dev-knowledge`, if wanted, is
  a separate Layer-1 handoff at session close, not part of this phase.
- Final commit: `docs: record post-trim verification result` (lands in
  corp-monorepo).

### Phase boundaries are commit boundaries

Each phase is one self-contained, revertable commit (or tight group).
A revert of Phase N does not disturb Phases 0..N-1. The branch can be
merged in full or partially (operator may merge through Phase 2 and
defer Phases 3-8) without leaving the repo in an inconsistent state.

---

## 8. Boundaries (what the rollout MUST NOT do)

- **MUST NOT reintroduce scope-tag enforcement** anywhere, in any form.
  Tags themselves are informal metadata only.
- **MUST NOT resurrect `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** in any
  follow-up or downstream action.
- **MUST NOT touch `tach.toml`, `.pre-commit-config.yaml` tach
  entries, or `.github/workflows/tach.yml`.** Tach is architectural
  enforcement, not documentation governance.
- **MUST NOT touch `pyproject.toml`, `src/corp/`, or `tests/`.**
- **MUST NOT add new audit checks casually.** Every proposed new
  check passes the ADR-48 governance-admission rule (recurring real
  failure + fully automatable + low ongoing cost) — explicit
  justification in the commit body, or the check stays out.
- **MUST NOT delete `docs/handoffs/`, `docs/HANDOFF.md`, or
  `scripts/update_handoff.py`.** The handoff-pattern collision is
  routed to a separate session.
- **MUST NOT migrate `docs/ARCHITECTURE.md` to repo root.** ADR-38
  A3 explicitly defers this.
- **MUST NOT make ecosystem-wide policy changes.** Any change to
  ADR-38, any new universal rule, requires Council debate. Surface as
  an operator question (§9), not as a rollout action.
- **MUST NOT delete files without explicit operator approval**
  per core invariant #3.
- **MUST NOT skip the per-step verify cadence** per core invariant #2.
- **MUST NOT push the branch or open a PR** without operator
  approval.
- **MUST NOT write a corp-monorepo handoff bundle** as part of this
  rollout. If a handoff is wanted at completion, it is a separate
  session under ADR-42 v3.x.
- **MUST NOT copy the ai-council rollout verbatim.** The §3 delta
  analysis exists precisely so it isn't.

---

## 9. Open questions for operator (decisions needed before execution)

1. **CHANGELOG.md preservation policy.** Hard delete (git is
   authoritative)? Or one-time archive snapshot to `docs/archive/`?
   Or final commit body carries the file's last content as a
   manifest? Default in this plan: hard delete with deletion-commit
   body listing the file's prior structure.
2. **ADR-38 amendment timing.** ADR-49 contradicts ADR-38's
   "CHANGELOG.md MANDATORY tier M+" cell. Amend ADR-38 in
   `.dev-knowledge` BEFORE this rollout, AFTER, or batched with a
   future ADR cleanup? Default: after, batched.
3. **Codex review.** Run Codex CLI review on each phase PR, only on
   the final phase, or skip entirely? Default: each
   phase PR (small enough to review), with severity calibration per
   existing AGENTS.md.
4. **VISION.md prerequisite.** Has corp-monorepo's `VISION.md` been
   created and tier-upgraded to Standard since the 2026-04-21 audit?
   If no, this rollout is GATED on a prior VISION-creation session.
   Operator must confirm before execution begins.
5. **Decommissioning debt scope.** Limit to references the trim
   itself touches, OR opportunistically clean the adjacent
   reference-drift list from the 2026-04-21 audit? Default: trim-touched
   only.
6. **Per-phase merge cadence.** Each phase merged sequentially via
   its own PR, OR a single long-lived branch with phase commits
   merged at the end? Default: single long-lived branch with phase
   commits; one merge at the end. Allows partial-merge fallback if
   any late phase blocks.
7. **Branch naming.** `docs/govern-trim-corp-monorepo` proposed;
   operator may override.
8. **ARCHITECTURE.md root migration.** Confirm it remains adjacent
   and routed to a separate session (default in this plan).
9. **Handoff-pattern collision.** Confirm it remains adjacent and
   routed to a separate session (default in this plan).
10. **JOURNAL shape backward-edit.** Confirm forward-only adoption is
    desired (default, matching append-only core invariant) vs.
    rewriting recent entries to the new shape.

---

## 10. Boundaries between this plan and execution

- This plan is a design spec. It does not execute.
- The executing session uses this plan as its read-first artifact and
  may DIVERGE from it only with explicit operator approval, recorded
  in the JOURNAL entry that closes the execution.
- The executing session's Claude-Code prompt is authored separately
  by the operator. This document does not author that prompt.
- The executing session begins with discovery (§4) and proceeds
  through phases (§7) only as discovery permits.

---

## 11. References

- `docs/decisions/ADR-33-vision-universalization.md`
- `docs/decisions/ADR-38-universal-repo-architecture.md`
  (including 2026-05-11 A3 amendment)
- `docs/decisions/ADR-48-trim-documentation-governance.md`
- `docs/decisions/ADR-49-consolidate-past-recording-files.md`
- `docs/decisions/ADR-50-machine-document-encoding.md`
- `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`
  (historical state — superseded by discovery in §4)
- `JOURNAL.md` 2026-05-16 (Council Simplification slice) and 2026-05-17
  (ai-council session-sync handoff Stage 3)
- `~/.claude/rules/core-invariants.md` (test-after-each-step, no-delete-
  without-asking, clean-git-status-before-task)
