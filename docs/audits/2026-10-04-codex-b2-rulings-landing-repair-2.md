# Codex Review — b2-rulings-landing, repair 2

**Date:** 2026-10-04
**Branch:** `worktree-b2-rulings-landing`
**Diff range:** the repair-2 working-tree delta over the sync merge of origin/main `1546090c` (`decision_coverage.py`, `audit_checks/check_rulings_carried.py`, `tests/test_decision_coverage.py`)
**Mode:** diff-review, isolated read-only session (the diff, the three post-change files and the integrator refusal in an empty job-tmp folder, not the lane)
**Consumer:** governance row `[#1378]` (the rulings gate armed at batch close and the handoff cut) and `LANE-B2-W1-b2-rulings-landing.md` (Done-contract item 5) as repaired under `to-browser/REFUSED-b2-rulings-landing.md` (INTEGRATOR, repair 2 of 2); it continues `docs/audits/2026-10-04-codex-b2-rulings-landing-repair-1.md`

**Model used:** `gpt-5.6-terra` (served: `provider: openai`, `-c model=gpt-5.6-terra`, from the tool's own log header)
**Command:** from an empty job-tmp folder, `codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check --output-last-message codex-out.txt -` with the prompt on stdin, run detached.

| nonce returned | first line quoted | verdict |
|---|---|---|
| `NONCE-6113d894b5a1` | `diff --git a/scripts/audit_checks/check_rulings_carried.py b/scripts/audit_checks/check_rulings_carried.py` | accept |

## What the refusal named, and what was done

The N2 reviewer (grok-4.7, `NONCE-35dba578e489`) ruled REWRITE on the pass-4 P1: `None` as the leg-(a) "not measured" marker is falsy, so `not report.unlanded` reads an unmeasured leg as clean.

| refusal item | disposition |
|---|---|
| `RulingsReport.unlanded` sentinel | **Fixed**: a module-level `UNMEASURED` (an instance of `_Unmeasured`, `__bool__` is `True`, not iterable, no length). `_findings` (no `or []` collapse), `passed`, `exit_code`, `render` and both `rulings_report` returns use it. `exit_code(no_transport=True)` is unchanged. |
| `check_rulings_carried` | **Fixed**: `report.unlanded is _dc.UNMEASURED` replaces `is None`; the `n/a` finding ("leg (a) not measured, so not a pass") is kept. |
| RED tests reading the object | **Fixed, RED-first**: the tests assert `report.unlanded is dc.UNMEASURED`, `bool(report.unlanded)` and `report.passed is False` on an unmeasured report, and `measured.unlanded == []` with `not measured.unlanded` on a measured-clean one. RED at the sync merge: 6 failed (`module 'decision_coverage' has no attribute 'UNMEASURED'`) of the 20 selected; GREEN after the change. |
| Review record carries a governance `[#id]` | **Done**: `[#1378]` here, and as a dated appended amendment line in the repair-1 record. |

## Review result

No P1, no P2. Verdict line: `VERDICT: accept`.

## What the review did not examine

The reviewer saw the repair diff and the three post-change files only; it did not run the tests. The targeted tests were run on the tip, detached, through `scripts/memory_admission_gate.py run`; tallies are in `to-browser/SESSION-b2-rulings-landing.md`.
