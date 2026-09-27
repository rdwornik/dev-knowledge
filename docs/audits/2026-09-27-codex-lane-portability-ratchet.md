# Codex Review — lane-portability-ratchet

**Date:** 2026-09-27
**Branch:** `worktree-lane-portability-ratchet`
**HEAD:** `1b92545c`
**Diff range:** `main..worktree-lane-portability-ratchet`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: LANE-5B4-7-portability-ratchet.md (Done-contract, row L4).
Focus areas:
- scripts/fleet_health.py _norm_dir: posixpath-based case/sep fold replacing os.path.normcase
- scripts/reverse_dep_oracle.py uri(): drive-letter vs POSIX absolute path branch
- scripts/offload_admission.py _reservation_identity: st_ctime_ns added to (st_dev, st_ino) to defeat POSIX inode reuse
- scripts/dispatch_conformance.py head_token: PureWindowsPath replacing native Path
- tests/test_gen_handoff_preflight.py: POSIX/Windows branch in the session-slug pin
- scripts/platform_skip_ratchet.py + tests/test_platform_skip_ratchet.py + ecosystem/platform-skip-baseline.json: new FAIL-tier shrink-only ratchet on sys.platform/os.name-conditioned pytest skips

---

## Findings
## CRITICAL

## [CRITICAL] scripts/offload_admission.py:1011 — Successful corpus creation is always treated as a directory replacement

**What:** The saved identity now includes the destination directory’s `st_ctime_ns`, but publishing each file with `os.link(..., root / rel)` changes that directory metadata before the final comparison.  
**Why:** A normal successful write therefore has a different ctime and raises `REPLACED`; the existing positive corpus-write paths will fail, including on the new Ubuntu CI matrix leg.  
**Fix direction:** Do not use mutable directory ctime as an unchanged identity across writes; use a stable ownership mechanism (for example, a directory handle/descriptor) or redesign the replacement check around expected mutations.

**OUTCOME: FIXED**, same lane, same session (commit after this review). `_reservation_identity`
now returns a held-open POSIX file descriptor (`os.open(root, os.O_RDONLY | os.O_DIRECTORY)`)
instead of a ctime snapshot; `_reservation_still_holds(root, reservation)` compares
`os.fstat(fd)` against a fresh `os.lstat(root)` via `os.path.samestat`. Holding the descriptor
makes the original inode number unavailable for reuse for the life of the call, which closes
the original T2 inode-reuse gap WITHOUT touching ctime, so a legitimate write through the
descriptor's own name no longer moves the identity it is compared against. Windows keeps the
pre-existing `(st_dev, st_ino)` tuple (no descriptor) since the reuse gap never existed there.
Proof: `tests/test_offload_admission.py::test_reservation_survives_writes_made_through_its_own_directory`
(the exact happy-path case Codex names) and
`::test_reservation_does_not_survive_a_real_swap` (the original T2 property, now proved with
real filesystem operations instead of a monkeypatched stat object). Full suite re-run:
`tests/test_offload_admission.py` 93 passed.

## HIGH

## [HIGH] scripts/platform_skip_ratchet.py:355 — The “shrink-only” baseline can be rebased to admit new skips

**What:** `--write-baseline` permits writing the current population when the previous baseline is absent or has a different detector, while the live test compares only against the current checkout’s baseline.  
**Why:** A diff can add a platform-conditioned skip and add/rebase its baseline entry in the same change, passing CI despite the stated “may only fall” contract.  
**Fix direction:** Add an integration/CI check that compares the baseline’s site set and detector against the merge base or target branch and refuses additions, deletion-based rebases, and detector-mismatch rebases.

**OUTCOME: NOT FIXED this lane — ROWS-OWED.** This is the same shape `scripts/proof_layer.py`
already ships with (its own `render_baseline` has no growth-refusal at all; this ratchet's
does, which is already stricter). Closing it fully needs a git-history-aware check (the
committed baseline compared against the merge-base's own committed baseline, not just
self-consistency within one checkout) — a CI-time or pre-commit-time mechanism, not a change
`ratchet_findings`/`render_baseline` can make from inside a unit test with no git call. Row
L4's Done-when ("a test proves an added skip fails and a removed one passes") is met as
written and is verified by this lane's test suite; the same-commit add+rebase gap is a
follow-up hardening step, not a regression this lane introduced. Filed below as ROWS-OWED.

## MEDIUM

(none)

## LOW

(none)