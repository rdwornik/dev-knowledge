# TERRA REVIEW — BATCH 1 BRANCH A (`worktree-lane-a-533-leg2`)

**Branch:** `worktree-lane-a-533-leg2`
**HEAD:** `cb452ff1`
**Base:** `main` @ `328d1086`
**Reviewer seat:** batch-1 integrator (P3 duty of the integrator contract of record)
**Instrument:** `codex exec review --base main` (codex-cli 0.145.0, `gpt-5.6-sol`), plus a
direct integrator read of both changed source files. Codex is the instrument, not the verdict.

> **Filename deviation, recorded.** The contract names this artifact
> `docs/audits/2026-08-18-review-batch1-a.md`. `review` is **not** a member of
> `validate_hermetization.AUDIT_CLASS_ENUM`, so that name is refused by the ADR-101 Rule B
> gate at commit time. Landed under the `codex` class instead — the same shape lane H's
> artifact already uses (`2026-08-18-codex-review-batch1-c-e.md`).

## 0. Why this review exists

Branch A was frozen after lane H's review scope closed, so no lane reviewed it. The integrator
contract makes a terra review of A a **mandatory pre-merge duty**, honored under the same
three-verdict enum as H's verdicts for C and E.

## 1. Scope

| Path | +/- | Nature |
|---|---|---|
| `scripts/journal_anchor.py` | +118/-8 | two memos (`_entries`, `introduced`) |
| `scripts/audit.py` | +86/-12 | `run_checks` seam + opt-in `--parallel`/`--workers` |
| `tests/test_journal_anchor.py` | +450 | RED-first memo tests |
| `tests/test_audit_parallel.py` | +290 | RED-first parity tests |
| `docs/audits/2026-08-18-technical-533-leg2-lane-contract.md` | +95 | contract of record |
| `docs/audits/2026-08-18-technical-533-leg2-measurements.md` | +306 | STEP 1 / STEP 6 evidence |
| `docs/audits/README.md` | +/-4 | generated index |

Nine commits, RED-tests-first ordering visible in the log (`a210708d` and `9181e88e` precede
their implementations).

## 2. Findings

### A-1 · P3 · `scripts/audit.py::run_checks` — a raising check is re-raised only after every other check finishes

`as_completed` re-raises the first failed future on the calling thread, but the `with
ThreadPoolExecutor(...)` block then calls `shutdown(wait=True)` on the way out, so the
exception surfaces only once all in-flight checks have completed. Behaviourally correct — the
exception is *not* swallowed, which is the property the docstring claims and the property that
matters — but a crash in check 3 of 43 will not be visible until the slowest sibling returns.
**Not blocking:** the parallel path is opt-in and no gate uses it.

### A-2 · P3 · `scripts/journal_anchor.py` — memo memory ceiling is real but stated

`_entries_tuple` holds a ~2.6 MiB key and a ~2.6 MiB value per slot at `maxsize=4`, i.e. up to
~21 MiB retained for the life of the process. This is documented in the docstring with the
reasoning for the ceiling, and the audit runner is a short-lived process. **Not blocking** —
recorded because it is a memory commitment a future reader should be able to find, and the
branch already makes it findable.

### Explicitly checked and found SOUND (no finding)

- **Memo-key immutability.** `_introduced_tuple` is keyed on a full 40-hex SHA, gated by
  `_FULL_SHA_RE`; what a commit introduced is fixed by its own hash, since parents are part of
  what the hash commits to. A ref (`main`, `HEAD`, a short prefix) bypasses the cache entirely
  rather than being cached under a caveat. This is safe **by construction**, not by policy —
  the strongest available form of the claim.
- **`_entries_tuple` invalidation.** Keyed on the journal *text*, not a path or mtime. A grown
  journal is a different key, so there is no invalidation to get wrong.
- **Fail-closed posture preserved.** `lru_cache` does not cache exceptions, so an `AnchorError`
  from unreadable history is re-raised from a real git read on every call. Verified against
  CPython semantics, not merely asserted.
- **Mutation safety.** Both memos store tuples and both public functions return a fresh `list`,
  so a caller mutating a result cannot corrupt later readers.
- **Cross-repo bleed.** `_introduced_tuple` keys include `str(repo)`, so a fleet walk over
  several repos cannot serve one repo's answer to another. Two spellings of one path cost a
  miss, never a wrong answer.
- **Output-order contract.** `run_checks` collects into per-check slots indexed by submission
  order and flattens in that order — never appends as work completes — so `CHECK_ORDER` and the
  byte-identical output the git hooks read are preserved under `--parallel`. Multi-finding
  checks stay contiguous.
- **Default behaviour unchanged.** `parallel=False` is the default on every caller;
  `audit_repo` and `cmd_ship_gate` route through the seam serially. Nothing flips a gate.
- **`ALL_CHECKS` read at call time**, not bound as a default argument, so the seam the tests
  monkeypatch stays attached.
- **`_GATE_MODE`** is set before the pool and restored in a `finally` after it; workers only
  read it. No write contention.

## 3. Severity tally

Critical/High/Medium/Low = **0 / 0 / 0 / 2** (A-1, A-2).
Codex's own summary: *"No critical or high-severity issues were found. The memoization
preserves freshness and mutation safety, while the opt-in parallel runner propagates failures
and retains registry-order output."* The integrator's independent read agrees and adds the two
P3 notes above, neither of which codex raised.

## 4. Verdict — branch A

> ## `MERGE-CLEAN`

No itemized fix is owed. Both findings are P3 observations on an opt-in code path that no gate
invokes; neither changes behaviour that ships by default.

## 5. Honest limits of this review

- Codex's run ended with an `rg` invocation error (`scripts/audit_checks/*.py`, os error 123 —
  a Windows glob-quoting failure in its own tool call), so its file sweep was **not** exhaustive
  over the `audit_checks/` package. The integrator's direct read of the two changed source files
  covers the diff in full, which is the surface a review of this branch is responsible for; but
  the codex leg alone should not be read as complete coverage.
- The branch's own performance claims (1.87x memoized, 4.28x parallel) are **not** verified by
  this review. The integrator contract verifies them separately as a post-merge measurement.
- This is a review of the diff, not of the pre-existing behaviour of the checks being memoized.
