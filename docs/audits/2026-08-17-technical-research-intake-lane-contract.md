# Lane R — research-intake: contract of record, committed AT STEP 0

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-17 · **Slug:** research-intake-lane-contract
- **Worktree:** `.claude/worktrees/lane-r-412-research-intake` · **Branch:** `worktree-lane-r-412-research-intake`
- **Branch point:** `397cfdae` — the merge that opened batch 7a.
- **Authority:** the operator prompt quoted verbatim in §1 below. This lane is **NOT in the batch-7a
  roster** (`docs/audits/2026-08-17-technical-batch-7a-manifest.md` lists lanes a, b, c only); it is a
  fourth, out-of-roster lane dispatched alongside them. §4 states what that means for the merge queue,
  because an unrostered lane inherits no ADR-110 exemption and must not be assumed to.
- **Committed at step 0** per `[#505]` clause 1 / STANDING_RULINGS I-D3 — the contract reaches the tree
  before the work, not after it.

## 1. The prompt, verbatim

> `[dk · research-intake · 5-artifacts]` Land the five browser-research artifacts and convert them into
> intake DRAFTS. STRICT: create ONLY new files; touch NO existing file except regen surfaces; ZERO
> backlog row births; zero register/ADR/PLAYBOOK edits; do not merge or push main; commit-and-STOP.
> Batch 7a is mid-integration — a births/edits collision is the failure mode this contract exists to
> avoid. Steps: (0) commit this prompt as contract of record. (1) Copy the five files from
> `C:\Users\1028120\Downloads\` (compass_artifact_wf-50111a08... = cross-vendor agent instruction layers
> + prompt distillation; wf-76d68c06... = repository autonomy / policy-as-code / self-healing;
> wf-bfb9405b... = machine-verifiable Done-when specification; wf-460fee76... = multi-repo config
> standardization / fleet conformance; wf-fe444def... = off-machine agent fleet substrate, verified Aug
> 2026) into `docs/audits/` (or the taxonomy-correct home — DERIVE it from quoted governance, ADR-101
> naming, never invent a path) with EXTERNAL EVIDENCE headers stating: browser-produced, advisory until
> ratified, binds nothing. Byte-faithful copies; add only the header. (2) For each, write ONE
> `docs/intake/<date>-<slug>.md` with `status: DRAFT` per the live intake template: Section A = the
> artifact's own TL;DR quoted, Section B = the decisions it would force on THIS repo (each as a proposed
> row title + one-line Done-when in testable form + a proposed kill-candidates line — as TEXT in the
> intake, NOT as a birth), Section C = what it supersedes or contradicts in current doctrine with
> locators, Section D = the smallest first build it names. (3) Cross-link the five intakes to each other
> where they overlap. (4) Update `docs/intake/README.md` index if the live convention requires it. Final
> line: artifacts landed 5/5 · intakes drafted N · proposed rows enumerated M (NOT born). Commit per
> artifact, STOP.

## 2. The destination is DERIVED, and it is `docs/archive/` — not `docs/audits/`

The prompt offered `docs/audits/` but instructed the lane to derive the taxonomy-correct home from
quoted governance rather than accept the suggestion. The derivation lands elsewhere, so it is recorded
here in full rather than performed silently:

- **ADR-101 §1 Tier-2** — `archive/` is inside the sanctioned closed genre set. Confirmed against the
  live parser, not the prose: `scripts/validate_hermetization.py::SANCTIONED_GENRES` =
  `{"archive", "audits", "decisions", "handoffs", "intake"}`, and `docs/archive` is in the Rule C
  allowlist of admissible homes (`scripts/validate_hermetization.py`). Landing here invents no path.
- **ADR-60 amendment 2026-05-27** — `docs/archive/README.md` opens: *"Holding zone for artifacts whose
  destination isn't yet decided"*; *"Not a dumping ground — a triage queue."* That is exactly the status
  of an unratified external research memo.
- **ADR-101 Rule B is scoped to `docs/audits/*.md` only** and enforces the closed 11-class enum
  (`AUDIT_CLASS_ENUM`). **No class in that enum describes an external research memo** — `technical`,
  `functional`, `qa`, `census`, `verification`, `ecosystem-audit`, `conformance-nightly-digest`,
  `changelog-review`, `codex`, `fresh-eyes`, `incident`. Filing browser research as
  `docs/audits/…-technical-…` would misdeclare a memo nobody in this repo authored or verified as a
  first-party audit finding. The genre line `docs/intake/README.md` §4 draws — *"`docs/audits/` =
  evidence (what a read-only census/audit found)"* — is a claim about **this repo's own** evidence.
- **Class precedent, 8 files, unbroken:** `docs/archive/` already holds
  `2026-08-09-research-*-wf-<id8>.md` ×6 (landed 2026-08-10) and
  `2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`, all from this same commissioning pipeline —
  a `compass_artifact_wf-<id>_text_markdown.md` in `~/Downloads`. The 2026-08-14 file is the direct
  precedent for **a landed memo carrying a provenance header**, which is what this contract requires;
  the six from 2026-08-09 landed header-free with provenance held in the README list instead.
- **Naming:** `docs/archive/README.md` §"Naming convention" — `YYYY-MM-DD-{descriptive-slug}.md`. The
  trailing `wf-<id8>` token follows the landed precedent so each file resolves back to its commissioning
  artifact without depending on an index surviving.

**A distillate ABOUT these memos would be the `docs/audits/` artifact** (precedent:
`docs/audits/2026-08-10-technical-research-corpus-distillate.md`). The memos themselves are not.

## 3. Scope — what this lane writes, and what it deliberately does not

**Writes (all NEW files):**

- 1 × `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` — this file.
- 5 × `docs/archive/2026-08-17-research-<slug>-wf-<id8>.md` — byte-faithful bodies, header only added.
- 5 × `docs/intake/2026-08-17-tech-<slug>.md` — `status: DRAFT`, intake-ids **35–39**.

**Touches (regen surfaces only, each hook-gated or coherence-gated):**

- `docs/audits/README.md` — `gen_audit_index.py --check` is the `audit-index-freshness` pre-commit gate.
- `docs/intake/README.md` — `gen_intake_index.py --check` is the `intake-index-freshness` pre-commit gate.
- `docs/intake/manifest.json` — `gen_intake_tree.py --write`; NOT hook-gated, and omitting it FAILs the
  `intake_tree_coherence` audit check. Regenerated for that reason, not optionally.

**Does NOT do, and each omission is a decision rather than an oversight:**

- **Births ZERO backlog rows.** Section B of each intake enumerates proposed rows as TEXT — a title, a
  testable one-line Done-when, and a proposed `kill-candidates:` line. Nothing is written to
  `BACKLOG.md`, no `tasks/` file is created, and no id is consumed. Lane R holds **no reserved id block**
  (the batch-7a manifest reserves 534–545 for lane a and 546–557 for lane b; lane R is unrostered and
  therefore entitled to none). Proposing in prose is the only birth-free channel available to it.
- **Edits no register, ADR, PLAYBOOK, ESSENTIALS, CLAUDE.md, ARCHITECTURE.md, or VISION.md.** Where a
  memo contradicts standing doctrine, Section C of the intake records the contradiction **with a
  locator** and stops there. Recording a contradiction is not resolving it.
- **Does not update `docs/archive/README.md`.** Its "Current contents" list is hand-authored prose, not a
  regen surface, and it carries no `last_reviewed` stamp and no gate. The contract's "touch NO existing
  file except regen surfaces" therefore excludes it. **This leaves a real gap and it is named rather than
  smoothed over:** the eight already-landed research memos are indexed there and these five are not.
  The EXTERNAL EVIDENCE header this contract mandates puts provenance *inside each file*, which is why
  the gap is tolerable — but it is owed work, not absent work.
- **Does not merge, does not push, does not touch `main`.** Commit-and-STOP.

## 4. Collision analysis against live batch 7a — the actual risk, stated plainly

Four worktrees are live at this instant, not three:

```
main                                 397cfdae  (primary)
worktree-lane-a-534-audit-dispositions  606e9b11
worktree-lane-b-546-currency-archival   fffba0bd   locked
worktree-lane-c-505-north-star-inventory 217b5001  locked
worktree-lane-r-412-research-intake      397cfdae  locked   <- this lane, UNROSTERED
```

The batch-7a manifest's 3×3 disjointness proof was computed over lanes a, b, c. **Lane R was not in that
matrix, so no proof covers it** — the intersection below is derived here instead:

| Surface | Lane R | Rostered owner | Verdict |
|---|---|---|---|
| `docs/archive/*.md` (5 new) | writes | nobody | **clear** |
| `docs/intake/2026-08-17-tech-*.md` (5 new) | writes | lane b writes `docs/intake/**` | **clear** — disjoint filenames; lane b archives *terminal* docs, lane R adds *new DRAFT* docs |
| `docs/audits/…-research-intake-lane-contract.md` | writes | lanes a + c write `docs/audits/` | **clear** — distinct file; a shared directory is not a collision (manifest §"3×3") |
| `docs/audits/README.md` | regen | ambient — every lane | **expected churn**, manifest names it an ambient regen surface |
| `docs/intake/README.md` + `manifest.json` | regen | **lane b, assigned explicitly** | **OVERLAP — see below** |
| `BACKLOG.md`, `tasks/**` | never | lanes a + b | **clear by construction** — lane R births nothing |

**The one genuine overlap is `docs/intake/README.md` + `docs/intake/manifest.json`.** The batch-7a
manifest assigns both to lane b *specifically so they are not ambient*. Lane R cannot avoid them: the
`intake-index-freshness` pre-commit hook **refuses the commit** if five intake docs are added without
regenerating the index, and `intake_tree_coherence` FAILs the audit if `manifest.json` is not re-derived.
So the choice is not "touch it or not" — it is "regenerate it or do not commit at all."

**Consequence for the integrator, stated ex-ante so it is not discovered at merge:** whichever of lane b
and lane R merges second will conflict inside the `<!-- INTAKE-INDEX:START/END -->` block and inside
`manifest.json`. **Both are machine-generated and neither should be hand-merged.** The resolution is
mechanical: take either side, then re-run

```
python scripts/gen_intake_index.py --write
python scripts/gen_intake_tree.py  --write
```

on the merged tree and commit the regenerated result. The intake-ids do not collide (lane b changes
`status:` on existing docs and moves terminal ones; lane R adds ids 35–39, which no rostered lane
allocates), so the conflict is index-shaped only, never content-shaped.

**Lane R is unrostered, so the ADR-110 batch exemption does not cover its merge.** Its branch tip must be
JOURNAL-anchored on its own account before it merges to `main`, per the standing anchor-the-queue
discipline. This lane does not journal — the integrator does.

## 5. Id derivation — intake-ids 35–39

Derived live across live + archived intake docs before any file was written:

```
grep '^intake-id:' docs/intake/*.md docs/intake/archive/*.md
observed: 1..34 contiguous  (14 appears 3x -- #14 plus two same-pack siblings)
MAX = 34   ->   NEXT FREE = 35
LANE R ALLOCATES: 35 36 37 38 39   (five docs, one per artifact)
```

These are **intake-ids, not BACKLOG ids** — a separate, non-overlapping numbering space
(`docs/intake/README.md` §3). Lane R consumes no BACKLOG id and clashes with neither reserved block.

## 6. What "advisory until ratified" means on these five files

Each landed memo carries a three-line header stating it is browser-produced, advisory until ratified, and
binds nothing. That is a statement about **authority, not quality**. These memos are commissioned
external research; several make claims that contradict live doctrine in this repo (enumerated per-intake
in Section C). None of those contradictions is resolved by this lane, and none becomes doctrine by virtue
of having landed in the tree. The ratification channel is the intake spine — DRAFT → READY → ACCEPTED —
and every one of these five sits at **DRAFT**, the status that means "a conversation is structuring it;
not yet operator-approved" (`docs/intake/README.md` §5).
