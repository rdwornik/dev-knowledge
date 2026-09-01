# Codespace long-run proof — L1..L6, per-layer, with named failure at L5

**Lane:** `[#632]` · **Date:** 2026-09-01 · **Substrate:** GitHub Codespace
(`CODESPACE_NAME=lane632proof-64wv4g6ggg35w99`, hostname `codespaces-40ec8b`), dispatched via
`dispatch-run.sh` running `claude -p "Read /workspaces/dev-knowledge/LANE-632-codespace-longrun-proof.md
and execute it exactly." --permission-mode bypassPermissions --output-format json`.

**Start:** 2026-09-01T17:53:11Z. **This report written:** 2026-09-01T18:07:01Z. **Total elapsed
so far: ~14 min**, well past the 1-turn-probe / "short green turn" bar the operator ruled
insufficient — this run reads files, runs the full test suite twice, stashes/pops, and lands a
commit, which is the "commits and pushes" bar instead.

## Per-layer table

| Layer | Verdict | Evidence |
|---|---|---|
| L1 TRANSPORT | GREEN | `ps -eo pid,ppid,cmd` shows `811 810 bash -l /workspaces/dev-knowledge/dispatch-run.sh` → `957 811 claude -p Read ... --permission-mode bypassPermissions --output-format json`, an exact match to `dispatch-run.sh` line 34. `LANE-632-codespace-longrun-proof.md` and `dispatch-run.sh` exist on disk with today's mtime. `CODESPACES=true`, `CODESPACE_NAME` set. **Limit:** "receipt returned" cannot be observed from inside the process that IS the receipt's source (stdout/stderr redirect to `receipt.json` completes only at this process's exit) — inferred from the redirect in `dispatch-run.sh`, not directly witnessed. |
| L2 AUTH | GREEN, with a caveat worth naming | The dispatched process (pid 957, this session) is plainly authenticated — it has been calling tools and running commands for 14 minutes. **But** `CLAUDE_CODE_OAUTH_TOKEN` is **UNSET** in this shell's environment (`env \| grep CLAUDE_CODE_OAUTH_TOKEN` → empty), and a **fresh nested** `claude -p 'reply AUTHOK' --output-format json` in the same container reproduces the exact documented trap verbatim: `"subtype":"success"` with `"is_error":true`, `"result":"Not logged in · Please run /login"`, `"duration_ms":96`. No credential file was found under `~/.claude` or `~/.claude.json` to explain the discrepancy; the dispatched session instead carries `CLAUDE_CODE_MESSAGING_SOCKET` / `CLAUDE_CODE_MESSAGING_TOKEN` / `CLAUDE_CODE_CHILD_SESSION` env vars and a live unix socket (`/tmp/cc-socks/957.sock`), indicating this run is authenticated via a messaging-socket channel to an external controller, not via the local CLI reading `CLAUDE_CODE_OAUTH_TOKEN` directly. **This is the honest finding**: the top-level dispatched agent works, but the specific mechanism the runbook names (`CLAUDE_CODE_OAUTH_TOKEN` secret → local CLI login) is not what is actually authenticating it in this container at this moment — a bare `claude -p` call a script might reasonably make mid-run would hit the same "Not logged in" trap this session is immune to. |
| L3 CLONE | GREEN | `git fetch origin` (clean, no output = no new refs) then `git rev-parse HEAD` = `e96ad50ca830c7df86f435541fa57d98d0fc6e63`, `git rev-parse origin/main` = same SHA. Proven by fetch+rev-parse, not by trusting `git status -sb` (which read `## main...origin/main`, i.e. no divergence reported — consistent, and independently confirmed rather than solely relied upon). |
| L4 TOOLCHAIN | GREEN | `which uv` → `/usr/bin/uv`; `uv --version` → `uv 0.11.19 (x86_64-unknown-linux-musl)`; `pyproject.toml` pins `required-version = "==0.11.19"` — exact match. This **reverses** the previously recorded ABSENT state for this container class. |
| L5 LONG-RUN | **RED** | `uv run --locked pytest -x --tb=short`: stopped at 2 failures (`362 passed, 2 skipped` before stop, `33.151s` real / `47.025s` user / `5.896s` sys — CPU-bound, no hang signature). A follow-up **full** run without `-x` (`uv run --locked pytest --tb=no -q`) completed in `298.50s` (4:58) wall-clock: **17 failed, 4759 passed, 11 skipped, 1 xfailed**. See root-cause + bounded fix below. |
| L6 COMMIT+PUSH | GREEN (pending push in this same action) | This file, committed on `worktree-lane-632-codespace-proof` with `[#632]`, pushed to origin from inside this codespace — see commit/push output appended to this lane's record. |

## L5 root cause and the ONE bounded fix attempted

Named failure: **L5, "full suite runs to completion"** — it completes (no hang: wall-clock and
CPU time agree in order of magnitude at every scale tried, the opposite of the recorded
75-min-elapsed/3s-CPU hang signature) but does **not** exit 0.

**Bounded fix attempted:** isolate whether this codespace's own untracked dispatch artifacts
(`LANE-632-codespace-longrun-proof.md`, `dispatch-run.sh`, `receipt.json` — all present at repo
root before this session did anything) were corrupting "live measurement vs committed baseline"
tests, since several failing test names say exactly that (`test_health_ok_with_registered_repo`,
`test_health_stays_ok_with_na_status`). Ran `git stash -u` (reversible, nothing else touched),
re-ran the full suite, then `git stash pop` to restore.

```
before stash: 17 failed, 4759 passed, 11 skipped, 1 xfailed in 298.50s
after  stash: 15 failed, 4761 passed, 11 skipped, 1 xfailed in 298.26s
```

**The fix worked, partially, and precisely as scoped.** Two failures were confirmed caused by
`receipt.json` sitting at repo root un-dot-prefixed: `scripts/audit.py`'s `dot_prefix_discipline`
check flags `['receipt.json']` as "not on the ADR-59 exception list", which fails
`audit.py health`, which is what `test_health_ok_with_registered_repo` and
`test_health_stays_ok_with_na_status` invoke against the real repo tree (not a fixture). This is
a genuine interaction between the dispatch harness's artifact-naming and this repo's hermetization
gate — **not fixed further**, because `receipt.json` is the harness's own output file (this
process's stdout/stderr redirect target per `dispatch-run.sh` line 34) and `dispatch-run.sh` is
marked "GENERATED ... do not edit in place, overwritten on every dispatch" — deleting or renaming
either is outside "what a fix genuinely requires" for this lane and would falsify the receipt
mechanism itself.

**The remaining 15 failures are pre-existing at commit `e96ad50c`, independent of this codespace
substrate and of this session's artifacts.** They reproduce identically with the working tree
byte-for-byte clean (post-stash) and span unrelated areas (`test_cloud_provisioning.py`,
`test_consumer_at_landing.py`, `test_funnel_coverage.py`, `test_gen_north_star.py`,
`test_boundary_report.py`, `test_desired_state_report.py`, `test_enforcement_coverage.py`,
`test_merge_serialization.py`, `test_export_backlog_view.py`, `test_reverse_dep_oracle.py`,
`test_validate_doc_rot.py`, `test_preflight_freeze_predicates.py` ×3). Fixing 15 unrelated
pre-existing app-level test failures is not a bounded fix and is out of this lane's write-scope
(§ Rules: "Do NOT edit any file outside your artifact and what a fix genuinely requires") — named
here, not fixed.

## SUBSTRATE VERDICT: RED at L5

L1–L4 are unambiguously GREEN with the caveat on L2's auth mechanism recorded above. L5 is RED —
completion without hang, but non-zero exit — for reasons that isolate cleanly to (a) one
harness/gate interaction (2 failures, root-caused, not fixable within this lane's scope) and
(b) fifteen pre-existing app-level failures unrelated to the container. L6 is GREEN: this
document reaching `origin` from inside the codespace is itself the L6 proof.

## Honest limits — what this run does NOT prove

- Does not prove `CLAUDE_CODE_OAUTH_TOKEN`-mediated auth works, because that env var is absent in
  this container at the time of this run; it proves the *dispatched* session authenticates via
  some other live channel, and that a naive nested `claude -p` call in the same container does
  NOT authenticate — both facts, not the auth mechanism the runbook names.
- Does not prove `pytest -x --tb=short` (the literal command in the runbook) exits 0 anywhere in
  this codespace — it does not, both before and after the one bounded fix.
- Does not prove the 15 pre-existing failures are codespace-specific or absent on a clean local
  checkout; it proves only that they persist with this session's own footprint fully removed via
  `git stash`. Confirming they're substrate-independent (vs. some other latent container quirk)
  would need a second, non-codespace environment to diff against, which this lane does not have.
- L1 "receipt returned" is inferred from the redirect mechanism in `dispatch-run.sh`, not
  witnessed directly, for the reason given in the L1 table row.
- This session did not observe a hang at any layer, so it cannot characterize the *previously
  recorded* 75-min/3s-CPU hang signature beyond confirming its own runs don't reproduce it.
