# Lane ab-802 — the conductor judges CI by the frozen suite baseline

**Lane:** `lane-ab-802-conductor-freeze` · **Branch:** `worktree-lane-ab-802-conductor-freeze` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`, amended by
`docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md`) · **Date:** 2026-09-16

Consumers: [#802]

## 1 · Premise — the locators, checked before anything was built

**Contract identity.** `sha256` of the frozen contract read at boot
(`H:\My Drive\CLAUDE PROMPT DIR\LANE-ab-802-conductor-freeze.md`):
`7ecc8b30ee367f25a3cd2dc0b6a148af0cf3847e595208f9f6bc849f6764b944`. That matches the pin in the
batch AB manifest amendment 1's lane table (row `lane-ab-802-conductor-freeze`), so this is the
contract that was dispatched.

**Base.** `f8ca1d40` (merge of batch AB amendment 1 onto `main`).

**`logs/SUITE-BASELINE-FREEZE.md`, read in full.** Frozen at `b5270d636774abedff1b00cb0a9c7fb3698c226e`
(main, batch Y close packet merge), Actions `conductor` run `34901604346`, `push`,
2026-09-14T21:57:23Z. Command `uv run --locked pytest -q --tb=short`, resolved to **4 workers**
(`-n auto` on `ubuntu-latest`). Result **51 failed, 5863 passed, 22 skipped, 2 xfailed** in
229.75s. Two same-day amendments already live in the file:

- **The worker count is PINNED to `-n 4`** (2026-09-15 amendment). A consumer must resolve and
  REPORT its own worker count, REFUSE on mismatch (NOT-COMPARABLE, never a pass), and treat a
  missing/stale freeze file the same way.
- **One node id is SHA-dependent** (`test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable`,
  because `preflight_contract` silently skips an all-digit short SHA). Recorded as NOT absorbed
  into the frozen set — a live, un-ratified CANDIDATE, disposition owned elsewhere.

**Membership rule, stated in the file as load-bearing:** by test node id, never by count. A
failure inside the 51 is PRE-EXISTING; outside is a REGRESSION; a member that passes is the
expected direction, not a rule failure.

**`docs/audits/2026-09-15-technical-batch-z-close-packet.md`, "Defect three".** The freeze file's
own roster rendering is already truncated for one entry —
`tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_normalises[`
— because that parametrize id embeds a space (`"C:\Program Files\claude.exe" --bg-claude`) and
whitespace-delimited extraction breaks on it. The full id lives in
`docs/audits/2026-09-13-technical-lane-x-664-delete-list-execution-evidence.md:293`. The close
packet attributes fixing this to `[#763]` (re-measurement), not to a consumer reading the file as
committed. This lane's gate reads the file AS COMMITTED and does not attempt to reconstruct the
truncated id — see §6 open items.

**`scripts/conductor.py` and `.github/workflows/conductor.yml`, read in full.** `conductor.py` is
Layer-2/read-only, carries the phase gate and the §6 metrics, and a dual-import shim so it works
both as `scripts.conductor` (tests) and as a bare script (the workflow). The `pytest` job in
`conductor.yml` today runs `uv run --locked pytest -q --tb=short` (via `addopts = "-n auto"`, not
the pinned `-n 4`) and its own exit code IS the job's exit code — so main's pre-existing failures
(51 in the frozen file; the batch AB manifest amendment states 62 today, unmeasured by this lane
per contract) make the `pytest` required-check context red on every push, which is [#802]'s
stated symptom ("the conductor emails on every push"). `ruff`, `seal`, `terra` and `phase-gate`
are untouched by this lane's footprint. `deploy/conductor-required-checks.ruleset.json` carries
exactly the three contexts `pytest`, `ruff`, `seal`, `enforcement: disabled` — read, not edited,
per the contract's binding addition.

**Discrepancy against the batch AB manifest amendment, recorded and resolved by contract
primacy.** Amendment 1 §4 ("Checked and NOT sequenced") says *"`actions_verdict.py` is 802's"*.
`scripts/actions_verdict.py` already exists and belongs to `[#675]`/`[#742]` — a job-CONCLUSION
differential the integrator runs at merge time (`gh run view` job list vs. a baseline SHA), a
different layer from this row's node-id comparison inside the `pytest` job itself. The frozen
Done-contract (immutable) states the module explicitly: *"one module (`scripts/conductor.py`)
and one workflow"*. Followed as written; `actions_verdict.py` is not touched by this lane, so the
manifest's sequencing concern is moot in practice regardless of which reading is right.

## 2 · RED-first witnesses

(recorded after the tests are written — see the next commit)
