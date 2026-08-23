# L6 LANDING REPORT — the rulings, the write-scope correction, the `#34` provenance correction

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-24 · **Slug:** l6-rulings-landing
- **Lane:** `rulings-landing` (LOCAL background lane, worktree `worktree-rulings-landing`)
- **Contract:** `LANE-L6-rulings-landing.md` (frozen)
- **Source landed:** `RULINGS-and-AMENDMENTS-2026-08-23.md` v2 reissue, operator disk — the reason
  this lane is LOCAL and not cloud
- **Merge base:** `aeec0fd1` · **Branch footprint:** three files, all `.md`
- **What this lane did NOT do:** rule anything, flip anything, edit anything in place, touch
  `tasks/` or `BACKLOG.md`, self-merge

## 1. The three acts — all appends, none an in-place edit

| # | Target | Act | Commit |
|---|---|---|---|
| 1 | `docs/audits/2026-08-23-technical-phase0-preconditions.md` | Parts 1–3 of the ruling sheet appended **verbatim** under a dated architect-amendment heading | `4b19c375` |
| 2 | `docs/handoffs/2026-08-23-dev-knowledge-architect/HANDOFF_BOOT.md` | `AMENDMENT A2` appended beneath `AMENDMENT A1` — `docs/adr/` reads `docs/decisions/` | `a634e00e` |
| 3 | `docs/intake/2026-08-16-code-architecture-enforcement.md` | provenance correction appended; **`status:` unchanged, no `decided-by`, false sentence left visible** | `41cb9ccd` |

### Verbatim, proven rather than asserted

Parts 1–3 are source lines 20–282 (Part 4, the landing sequence, is procedural and was not
carried — stated in the appended header rather than left as a silent omission). The landed block
was extracted back out of the packet and diffed against the source:

```
diff <source lines 20-282> <packet lines 1100-1362>   ->   no output
```

No paraphrase, no reordering, no re-wrapping. Em-dashes and the `"silent_rule_ratchet"` quoting
survive byte-identical.

### Why append and not edit, in all three cases

`CLAUDE.md` §5 rule 3 (ADRs, transcripts, handoffs and audits are immutable — supersede or mark an
in-file amendment) and `protocols/STANDING_RULINGS.md` **J-3** (an amendment lands as an appended
marker; a silent in-place rewrite is out). In acts 2 and 3 the original wrong text is additionally
**evidence**: A1's `docs/adr/` is the evidence for architect error **E1** (third occurrence of the
inferred-path class), and `#34`'s "not in the repo today" is the evidence for R6's funnel finding.
Deleting either would destroy the finding it supports.

## 2. `#34` — what changed and what deliberately did not

**Changed:** characterization only. Ratification checklist **item 1 is discharged** — the source
artifact is in-repo at `docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md`, on
three independent identity checks re-verified live by this lane against the Phase 0 packet §6.1:

1. **Title** — H1 matches the `origin:` field's quoted title character-for-character.
2. **Content** — intake §A reproduces the archive `## TL;DR` exactly, all three bullets.
3. **Chronology** — git-added `f571ac3c`, **2026-08-10** — six days before the intake was routed
   (2026-08-16). *"docs(archive): land the six 2026-08-09 research memos byte-identical + index them."*

**Item 3** (ratchet vs flag-day for ruff enablement) is recorded as **ruled RATCHET** by the
architect on standing precedent. **Items 2, 4 and 5 remain the operator's.**

**Unchanged, deliberately:** `status: DRAFT`. No `decided-by`. No deletion or rewrite of the false
provenance sentence, in the frontmatter or in the Provenance section.

## 3. Suite — the A2 baseline is NOT matched, and the delta is named

Run unpiped (`PYTHONUTF8=1 python -m pytest -q --tb=short`, git-bash), exit code captured directly:

```
2 failed, 3561 passed, 9 skipped, 1 xfailed in 1423.98s (0:23:43)
PYTEST_EXIT=1

FAILED tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary
FAILED tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
```

**A2 baseline:** 1 failed / 3567 passed / 4 skipped / 1 xfailed. **This run:** 2 / 3561 / 9 / 1.
Delta: **+1 RED, +5 skipped, −6 passed** — and `2 + 3561 + 9 + 1 = 3573`, exactly the collected
count pinned in `ecosystem/doc-counts.md`. **No test was added, removed or lost.**

### RED 1 — the baseline RED, inherited

`test_anchor_gate_probe_distinguishes_installed_from_absent`, named in A2 itself and in the
2026-08-23 window seal, rooted in its `tmp_path` fixture. Expected.

### RED 2 — additional, and proven NOT this branch's

`tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` asserts
`Path(aud._REPO_ROOT).resolve() not in paths`. Run **from inside a linked worktree**,
`_REPO_ROOT` resolves to that worktree — which is in the linked-worktree list by construction.
The assertion names the lane's own directory:

```
AssertionError: assert WindowsPath('.../.claude/worktrees/rulings-landing') not in
  {.../worktrees/dashboard-commit-path, .../worktrees/rulings-landing, .../worktrees/status-grammar}
```

**Proven against the merge base**, which is what A2 asks for, rather than argued:

- `git diff main...HEAD -- tests/ scripts/ .pre-commit-config.yaml .claude/` is **empty** — the
  branch is three markdown files and touches no test, script, hook config or `.claude/` surface.
- Detached to bare `main` (`aeec0fd1`, none of this lane's commits present) **in this same
  worktree** and ran the single test: **fails identically, in 1.36s.**

So it is an artifact of *where* the suite runs, not of *what* this branch changed. It would fail
for any lane running the full suite from a worktree, and it is a second instance of the same class
as the baseline RED: a test that reads live tree state and cannot distinguish "wrong" from
"measured somewhere else."

### The five extra skips — reported, not explained

Six tests that pass in the primary become one RED plus five skips here. The five skip identities
were **not** enumerated: `-q` prints no skip reasons, and naming them costs a second ~24-minute
full run for information that changes nothing about this branch. Stated as an open loose end
rather than left to look like a clean baseline. The collected-count reconciliation above is the
evidence that nothing was lost.

**Bottom line for the integrator:** this branch is markdown-only and introduces **zero** REDs. The
suite carries the one inherited baseline RED plus one worktree-context artifact, both reproducible
on bare `main`.

## 4. Closure contract — status

| Contract item | Status |
|---|---|
| 1 — Parts 1–3 appended to the Phase 0 packet, clearly marked | **DONE**, verbatim-diff clean |
| 2 — write-scope correction appended, A1 untouched | **DONE** |
| 3 — `#34` provenance correction appended, status not flipped, false sentence visible | **DONE** |
| 4 — suite matches the A2 baseline | **NOT MATCHED** — +1 RED, proven inherited at `aeec0fd1`; +5 skips unidentified |

Commit-and-STOP. Not pushed, not merged, not self-merged: Part 4 item 5 of the ruling sheet makes
the merge the **operator's** serial gate, and the five-lane batch dispatches only after it.
