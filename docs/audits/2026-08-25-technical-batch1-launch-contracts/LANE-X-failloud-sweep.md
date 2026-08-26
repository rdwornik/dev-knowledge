# LANE X — Fail-loud fix · green-by-skip sweep · closure-detector repair · wall-times

| Model | Mode | Effort |
|---|---|---|
| Opus (opusplan default) | Execute per this contract — **no plan mode**; the contract is the plan | High |

**Repo:** `.dev-knowledge` · **Branch:** `lane/x-failloud` (cut fresh from `origin/main`) ·
**Substrate:** **Codespaces devcontainer — MANDATORY** (gates armed; this lane doubles as the
substrate measurement) · **Session:** fresh CC session, boot via `/lane-boot` with this contract.
Commit-and-**STOP** — never merge.

**Purpose.** Three code repairs to owned audit organs plus a one-time sweep, closing the
green-by-skip failure class section U assigns to wave 1 — and recording the wall-times that turn
the substrate question (D1) from opinion into measurement. Serves `[E4]`/`[E7]`; authority =
section U (immutable). This is the batch's only code-impact lane: **terra review is mandatory
pre-STOP.**

## Read first
`CLAUDE.md` · `protocols/STANDING_RULINGS.md` section U (the defect note on `audit_check_count`) ·
`scripts/audit.py` (esp. `cmd_checks` and ~line 4639) · `scripts/validate_doc_claims.py` ·
`scripts/propose_closures.py` · the 2026-08-23 husk artifact proving its `FileNotFoundError`.
**Gotchas:** the cp1252 crash reproduces only on a bare Windows console — in the devcontainer,
reproduce via an ASCII-forced encoding test, not by assuming · GAP-1 is a **separate** defect from
cp1252 (standalone CLI injects `None` for `len(ALL_CHECKS)`); neither causes the other · both
currently read 46 — the defect is latent, so tests must simulate drift, not observe it.

## Git workflow
Branch from fresh `origin/main` · one commit per step at the COMMIT markers · pytest + `python
scripts/audit.py health` before each commit · push · **STOP**.

## UNDERSTAND (before step 1)
- **Problem:** a check that cannot compute its ground truth reports `skipped` while the run prints
  `OK` — green-by-skip. Third paid instance of the shape (pre-push degraded-allow, removed by
  ADR-85 §A6; `block_commit_on_main` silent-allow; now `audit_check_count`).
- **Scope:** fail-closed the leg · fix the encoding crash · sweep all 46 checks once · repair
  `propose_closures.py` · record wall-times. Nothing else.
- **Risks:** (a) fixing the instance and skipping the sweep — the sweep IS core scope; (b) a
  fail-closed change that REDs the pre-commit gate for unrelated work — verify `audit.py health`
  stays green on a clean tree; (c) touching governance surfaces — out of scope, a sibling lane
  owns them.
- **Failure mode:** writing anywhere except `scripts/`, tests, and the ONE frozen artifact path.

## Steps

**0. Start the clock.** Record ISO timestamps for: codespace provision-to-ready, first full
`pytest` wall-time, first commit wall-time (hook-inclusive). These go into the step-4 artifact.

**1. Fail-closed `audit_check_count` + cp1252 fix.**
- `validate_doc_claims`: when the injected ground truth is unavailable (`None`), the leg **FAILS
  with a named reason** — never `skipped`+`OK`. Preserve the GAP-1 cycle-break design (the
  standalone CLI may still not compute the count — then it fails loudly and the message names
  `audit health` / `audit run` as the computing paths).
- `audit.py` ~4639 (`cmd_checks`): remove the encoding landmine (ASCII-safe output or explicit
  UTF-8 handling) so a bare cp1252 console lists checks without crashing.
- Tests for both: simulated-drift test (claim ≠ live count ⇒ FAIL), unavailable-ground-truth test
  (⇒ FAIL, not skip), encoding smoke test. **COMMIT.**

**2. `propose_closures.py` `FileNotFoundError` repair.**
Reproduce from the husk-artifact conditions, fix, add a regression test. The closure detector
funds births — its output must be trustworthy or fail loudly, same rule. **COMMIT.**

**3. The sweep — all 46 checks, one pass.**
Audit every check in `ALL_CHECKS` against the rule: *"a check that cannot compute its ground truth
must FAIL, never skip."* Classify each: CONFORMS / VIOLATES (with the skip path quoted) / N-A
(no external ground truth). Fix trivial violations in this lane ONLY if the fix is a
fail-closed one-liner; anything larger is FINDINGS, not fixes. **COMMIT** (code, if any).

**4. Author the sweep artifact at the FROZEN path — do not rename it.**
`docs/audits/2026-08-25-green-by-skip-sweep.md` — the classification table, fixes applied,
violations deferred (each with file:line), and the step-0 wall-times block (provision · pytest ·
commit, devcontainer, dated). A sibling lane's backlog row cites this exact path; the path is
contract-frozen in both lanes. Regenerate the audits index per repo convention. **COMMIT.**

**5. terra review — mandatory, pre-STOP.**
Run `/codex-review` (terra) on the lane's full diff. Severity tally goes **into the sweep
artifact** (persisted, not chat). Address or explicitly disposition every finding ≥ medium.
**COMMIT** any resulting fixes.

**Final.** Full pytest + `audit.py health` green on the branch · push · lane report per `/save`
convention · **STOP.**

## Decision budget
Ask ONLY about: (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) unruled fork
classes. Sweep-classification judgment calls: decide, record in the artifact, batch into ONE
end-of-lane packet. Standing rulings apply silently.

## What NOT to do
- Do NOT touch `docs/decisions/`, `docs/intake/`, `tasks/`, `BACKLOG.md`, `ecosystem/*.yaml`,
  `CLAUDE.md`, protocols — sibling lanes own them. The ONE doc you write is the frozen artifact
  path (+ its index regen).
- Do NOT birth backlog rows (a sibling lane births the sweep row citing your artifact).
- Do NOT widen fail-closed semantics beyond the swept class; do NOT "improve" unrelated checks.
- Do NOT merge or touch `main`. Commit-and-STOP.
- **Sibling-hook clause:** end-of-session hooks may attribute a CONCURRENT session's commits to
  this lane and demand anchors — **decline with the stated reason**; hooks cannot tell sessions
  apart within a checkout.
