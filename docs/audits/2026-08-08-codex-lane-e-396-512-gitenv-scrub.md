# Codex Review — lane-e-396-512-gitenv-scrub

**Date:** 2026-08-08
**Branch:** `worktree-lane-e-gitenv-scrub`
**HEAD:** `1512f9ba` (final reviewed state; pass 5 clean)
**Diff range:** `main..worktree-lane-e-gitenv-scrub`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/5/0/0 <!-- Critical/High/Medium/Low, CUMULATIVE across the 5-pass loop. The final pass returned 0/0/0/0; recording only that would erase five real findings, four of which were reproduced live. Per-pass breakdown in the loop table below. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Passes:** 5 (each re-run against the fixed diff; the loop ran until a pass graded clean)

> **Note on the script's heuristic tally.** `codex-review.ps1` prints a *suggested* tally by
> counting severity-word mentions. It read `0/0/0/0` on pass 3 and `0/2/0/0` on pass 4 while
> both passes carried findings the run itself had written into the Findings section. The
> numbers above are counted from the findings, not from the heuristic.

---

## Focus

Each pass carried the frozen acceptance constraints (leaf-ness of `scripts/gitenv.py`;
byte-equivalent scrub semantics — the 15-name fallback tuple, the 2-name `_EXTRA` pair,
derivation from `git rev-parse --local-env-vars`, scrub BY NAME; WHERE the scrub fires must
be unchanged, in particular `audit.py`'s deliberate `GIT_INDEX_FILE` path; `batch_manifest`
read-only + None-on-failure unchanged; and "are any of these tests vacuous?"). Passes 2–5
additionally carried the prior passes' findings and their fixes, with an instruction to
attack the fix rather than re-report the finding.

---

## Findings

## CRITICAL

(none, any pass)

## HIGH

### Pass 1 — `tests/test_gitenv.py` — identity assertions encode the import layout

**What:** `audit`/`fleet_parity` may load `scripts.gitenv` while the test imports bare
`gitenv`; those are distinct module objects when both the repo root and `scripts/` are
importable.
**Why:** The five identity assertions fail in that layout. Two caches are behaviourally
harmless (at most one extra `rev-parse`), so the defect was the test asserting an
import-layout fact while claiming to assert the single-definition invariant.
**Verdict:** CONFIRMED by reproduction — `python -m pytest` from the repo root, and the
`-n auto` xdist layout the full suite runs under, both went RED on it.
**Disposition:** FIXED at `c94e7fdb`. Assertions are now on the defining FILE
(`inspect.getfile` vs `scripts/gitenv.py`), which is layout-independent and is what the
invariant actually says.

### Pass 2 — `scripts/audit.py` (+ `fleet_parity`, `batch_manifest`) — bare-first import can resolve a foreign `gitenv`

**What:** Package-mode (`python -m scripts.audit`) puts the repo ROOT on `sys.path`, not
`scripts/`, so a bare `import gitenv` searches `PYTHONPATH`/site-packages and any foreign
module of that name wins.
**Verdict:** CONFIRMED by reproduction. With a decoy `gitenv.py` on `PYTHONPATH`,
`audit._gitenv.__file__` resolved to the decoy and `audit._git_location_env()` returned the
**EMPTY set** — [#355] silently re-opened by the module that exists to close it, nothing
raised.
**Disposition:** superseded by pass 3 (see below). The interim fix at `75042968` reversed the
order; pass 3 showed ordering alone cannot close it.

### Pass 3 — same sites — the *package* spelling has the mirror-image hole

**What:** Script-mode (`python scripts/audit.py`) puts `scripts/` at `sys.path[0]` and
therefore cannot resolve a top-level `scripts` package there; a foreign package-shaped
`scripts/gitenv.py` on `PYTHONPATH` satisfies `from scripts import gitenv` instead.
**Verdict:** CONFIRMED by reproduction (emulating true script-mode by *replacing*
`sys.path[0]` rather than inserting, so the cwd entry is absent as it is for a real script
run). Scrub size again collapsed to **0**.
**Disposition:** FIXED at `a80976d2`. Both name-based spellings are gone: `audit.py`,
`fleet_parity.py` and `batch_manifest.py` resolve the file with
`importlib.util.spec_from_file_location` against `Path(__file__).with_name("gitenv.py")`,
which no `sys.path` entry can intercept. Affordable only because `gitenv` is a leaf —
executing it runs nothing else. `fleet_analytics` deliberately keeps `import gitenv`: it puts
`scripts/` at `sys.path[0]` itself, so nothing can precede it; its immunity is asserted, not
assumed.

### Pass 4a — `scripts/batch_manifest.py` — lane-merge lookup bypasses the scrub

**What:** `merged_branch_name()` delegates the merge-parent and merge-subject reads to
`journal_anchor._git()`, which carries no scrub. Under an inherited `GIT_DIR` the manifest is
read from the intended repo while the merge is looked up in the foreign one, so a valid lane
merge loses its exemption.
**Verdict:** CONFIRMED — a **sixth** unscrubbed site, distinct from the fifth
(`audit.py:3004`) already reported.
**Disposition:** NOT FIXED — deliberately out of this lane's frozen scope.
`scripts/journal_anchor.py` is the shared predicate the pre-push organ
`block_unanchored_push` also imports, so scrubbing it has a wider blast radius than a lane
takes unilaterally. Recorded at `1512f9ba` as a **strict xfail**
(`test_exempt_still_fires_under_an_inherited_GIT_DIR`) so the gap is a live, self-retiring
witness: the day that site is scrubbed the test XPASSes, `strict=True` turns it RED, and the
marker cannot be forgotten. Reported for a row at integration.

### Pass 4b — `tests/test_batch_manifest.py` — the regression test built its merge under the foreign `GIT_DIR`

**What:** step (4) of the [#512] regression test created its lane merge *after* exporting
`GIT_DIR`, so the fixture's own unscrubbed helper created that merge in the FOREIGN repo. The
production lookup then read the foreign repo too — both halves agreed about the wrong tree
and the assertion passed while proving nothing, masking pass 4a.
**Verdict:** CONFIRMED — building the merge first, in the intended repo, makes the assertion
fail.
**Disposition:** FIXED at `1512f9ba`. The merge is built with a clean env before the export,
the fixture now proves the foreign repo does not know that SHA (so a misdirected lookup
cannot answer correctly by luck), and the assertion moved into the strict xfail above.

## MEDIUM

(none, any pass)

## LOW

(none, any pass)

---

## Loop record

| Pass | HEAD reviewed | Findings | Outcome |
|---|---|---|---|
| 1 | `f95e7fbd` | 1 HIGH | reproduced, fixed at `c94e7fdb` |
| 2 | `c94e7fdb` | 1 HIGH | reproduced, interim fix `75042968`, superseded by pass 3 |
| 3 | `75042968` | 1 HIGH | reproduced, fixed at `a80976d2` |
| 4 | `a80976d2` | 2 HIGH | both reproduced; 4b fixed at `1512f9ba`, 4a recorded as a strict xfail (out of frozen scope) |
| 5 | `1512f9ba` | none | **clean pass** — loop terminated |

Pass 5 also independently verified `class Finding` at `scripts/audit.py:344`, confirming the
re-pinned 0-based `d.line == 343` in `tests/test_reverse_dep_oracle.py`, and confirmed the
strict xfail accurately records the `journal_anchor._git` gap.

**Honest limit of this artifact:** the reviewer ran read-only and could not execute `pytest`
(its sandbox disallows cache/temp creation). Every "CONFIRMED by reproduction" above is the
lane's own reproduction, run in this worktree and cited in the fixing commit; the reviewer's
contribution is the finding, not the proof.
