# Lane ab-810 — the substrate proven live, a model that reaches the Codespace runner, and four findings from the road

**Lane:** `lane-ab-810-substrate-repair` · **Branches:** `worktree-lane-ab-810-substrate-repair`
(`.dev-knowledge`, pushed) · `worktree-lane-ab-810-substrate-repair` (`win-tooling`, local only —
never pushed, per contract footprint) · **Batch:** AB
(`docs/audits/2026-09-16-technical-batch-ab-manifest.md`) · **Date:** 2026-09-16/17

Consumers: [#810] [#717] [#819] [#820] [#821] [#822]

## 1 · Premise

**Contract identity.** `sha256` of the frozen contract at
`H:\My Drive\CLAUDE PROMPT DIR\LANE-ab-810-substrate-repair.md`:
`322250264a30056c0868048be1f89885b54a818a108bd5c790abadad32499c33`.

Operator ruling on record before any build: "Codespace is proven live" was carried from a lane
packet the repo could not itself read. A proof an organ cannot read is not a proof — this lane
exists to close that gap, not to re-assert the premise it inherited.

## 2 · Done-contract, item by item

**1 — uv pin (commit `de6157d1`).** `.github/workflows/substrate-heartbeat.yml` reads
`required-version` from `pyproject.toml [tool.uv]` via `setup-uv`'s version-file input, replacing
the hardcoded `"latest"` that pulled 0.12.15 against a `==0.11.19` pin (both prior runs, 35017551689
and 35090026934, failed exit 2). **Verified against a real run, not just the diff**: heartbeat run
35160586877 (§3) built the devcontainer green — the uv step that used to fail exit 2 now passes.

**2 — explicit model on the Codespace runner.**
- `win-tooling` tracked source (`config/dispatch-helpers/DispatchHelpers.psm1`, commit `e22afad`):
  `Start-DispatchCodespace` gains a `[string]$Model` parameter with no default; a new guard 1c
  refuses (`REFUSED -- no -Model declared`) before `gh` is touched when it is absent; the runner's
  `claude -p` line now carries `--model $Model`. Re-deployed via `Apply-DispatchHelpers.ps1` and
  independently re-verified byte-identical (CRLF-normalized) to the tracked source.
- `.dev-knowledge` (`scripts/gen_lane_contract.py`, commit `adf7eeed`): the codespace dispatch-line
  regex widened to admit an optional `-Model` group (codespace had one spelling historically,
  unlike local's two — no amnesty machinery invented); `dispatch_command()`'s codespace branch now
  emits `-Model {model}`; `parse_contract()` validates it against the same enum and routing-row
  conjunction the local form already used.
- Both sides RED-first: 4 new tests per repo, confirmed failing before the build code, green after.

**3 — the heartbeat receipt, both legs.**
- **(a)** Lane branch pushed (`git ls-remote` confirmed `e99695e3` at
  `refs/heads/worktree-lane-ab-810-substrate-repair` on `.dev-knowledge` origin);
  `gh workflow run substrate-heartbeat.yml --ref worktree-lane-ab-810-substrate-repair` dispatched
  run **35160586877**; `gh run watch --exit-status` returned 0 — both jobs green (devcontainer
  build + L1 marker verify in 2m5s; substrate declaration probe in 13s).
- **(b)** `uv run --locked python scripts/substrate_heartbeat.py probe --substrate codespace
  --write-receipt` on this machine, then independently read back via `... show`:
  ```json
  {"readings": {"codespace": {"findings": [], "measured_at": "2026-09-16T23:06:26Z",
   "source": "local", "status": "live"}}, "schema": "dev-knowledge-substrate-heartbeat/1"}
  ```
  Non-empty, written by the probe verb itself (never hand-written). No PAUSE needed — the probe is
  a credential-free declaration check (D1-D5 in `substrate_heartbeat.py`'s own docstring) and does
  not require an actual codespace to exist on this machine; that honest limit is stated in the
  module, not glossed over here.

**4 — targeted pytest, both repos, green.**
- `.dev-knowledge`: `tests/test_gen_lane_contract.py` + `tests/test_substrate_heartbeat.py` —
  **174 passed**.
- `win-tooling`: `tests/test_dispatch_helpers_codespace.py` — **109 passed**;
  `tests/test_dispatch_lane_witness.py` — **39 passed** (after the fix in §4 below).
- Full suite not run on this workstation, per the operator's batch AB constraint.

## 3 · A defect found running Done-when 4, and fixed in-lane

The first `win-tooling` targeted run used a bare `pytest` and crashed on plugin import
(`ImportError: No module named 'tests'`) — it had resolved `pytest.exe` from the
**`.dev-knowledge`** venv, not win-tooling's own; win-tooling's own convention (`CLAUDE.md`) is
`py -m pytest -q`. Re-run correctly, it surfaced a real regression: guard 1c (§2) now refuses
before `gh` is touched when `-Model` is absent, and `test_dispatch_lane_witness.py` carries its
**own** `GhRecorder` (not shared with the sibling codespace test file) whose `run()` never passed
`-Model`. Eleven call sites were silently exercising the new refusal instead of each test's actual
scenario; only the first (`test_the_boot_check_gates_on_pre_commit`, which asserts on
`gh.calls()`) failed loudly rather than passing vacuously. Fixed to match the sibling file exactly:
`run()` gained `model: str | None = "sonnet"`, appended unless a test opts out with `model=None`.
Committed `35280a3`. Re-confirmed: 39/39 (this file), 109/109 (sibling, to rule out a regression
there).

## 4 · Rulings and deviations this session

- **The "no index regeneration" contract clause was withdrawn by the architect**, not excepted:
  filing a row and never regenerating `BACKLOG.md` are structurally incompatible (it is a rendered
  view of `tasks/`). Regeneration stayed **scoped to this lane's own rows**, per the same ruling's
  reasoning that the integrator's regeneration is for cross-lane reconciliation, not a lane's own
  tree coherence. `gen_task_tree.py --emit-source` was run twice: once for `[#819]`-`[#821]`
  (commit `6a78a742`), once for `[#822]` (commit `e99695e3`).
- **Three findings ordered filed, in priority order given by the ruling:** `[#822]` (a pipe masks
  the exit code of the command it wraps — filed, the ruling's own words: "the most valuable thing
  in your report"). The other two — audit-health's all-or-nothing bundling, and a contract clause
  needing verification against the gates at freeze time — are **written but unfiled**: this lane's
  granted block (819-822) is exhausted, 823-826 belongs to the integrator and was already consumed
  (`6ab764fc`), and 828-830 is actively held by a concurrent lane (`lane-ab-828-closure-census`,
  confirmed via `id_allocator.py holder`). Taking either is the exact collision class
  `id_allocator.py` ([#788]/[#804]) exists to prevent. **The integrator owes a block extension**
  for these two findings; their text is not yet committed anywhere and needs recovering from this
  session's transcript when that extension lands.
- **A pipe masked a real git-commit failure early in this session** (`| tail -40` reported
  `tail`'s exit code, not git's; the commit had never landed, caught only via the Stop hook's
  persistent dirty-tree flag). Fixed going forward: every command whose exit code decides
  subsequent behavior was redirected to a file with `$?` checked as a separate statement, never
  through a pipe. This is `[#822]` itself.
- **`[#819]`/`[#820]`/`[#821]`** (filed `6a78a742`, systemic findings from reconciling
  tracked-vs-deployed drift on `DispatchHelpers.psm1`): a two-repo lane's halves can merge
  independently and undetected; a HANDBACK can address a seat that no longer exists;
  `dispatch_drift` validates against one machine's local deployed state, not the repo's own
  tracked source.
- **`[#12]`/`[#13]`** filed in `win-tooling` (`c4bc882`): the deploy verb overwrites unsafely, and
  tracked/deployed drift has no automatic detection — both found while resolving Step 1's drift
  direction (deployed strictly ahead of tracked; back-ported via a proper `--no-ff` merge
  preserving authorship, not hand-splicing).
- **Stop-hook JOURNAL backpressure was correctly not acted on.** Its `(hard)` label is stale for a
  lane (`session_end_backpressure.py` is advisory in full since ADR-85 §A5; the real obligation is
  `block_unanchored_push.py`, pre-push, scoped to `main`, which never binds a lane that commits and
  stops). The frozen contract's "No JOURNAL entry" clause stands — unlike the BACKLOG-regeneration
  clause above, this one was never in genuine conflict with a gate.

## 5 · Verdict and stash state

**Both worktrees end clean.** `.dev-knowledge`: `git stash list` empty, HEAD `e99695e3`, pushed.
`win-tooling`: `git stash list` empty, HEAD `35280a3`, **not pushed** — outside this lane's
declared footprint (Step 1 only authorizes committing there; the contract's dispatch/push
instructions name only this repo's branch).

**Rows.**
- `[#810]`: Done-contract items 1-4 all met, evidenced above. Closeable.
- `[#717]`'s pattern (routing-row-declared model reaching the actual dispatch line) now covers
  both the local and codespace dispatch shapes.
- `[#819]`, `[#820]`, `[#821]`, `[#822]`: filed, open, Done-when stated in each row.

**What the integrator owes:**
1. Merge order: this lane touches `win-tooling` and `.dev-knowledge` independently — merge each
   repo's half and confirm both land, which is itself an instance of the exact hazard `[#819]`
   names. Do not let one merge without the other going unnoticed.
2. A block extension for the two still-unfiled findings (§4), and recovery of their text from
   this session's transcript.
3. `win-tooling`'s `worktree-lane-ab-810-substrate-repair` branch was never pushed (out of this
   lane's footprint) — confirm whether the integrator pushes it before merging, or merges from the
   local worktree directly.
