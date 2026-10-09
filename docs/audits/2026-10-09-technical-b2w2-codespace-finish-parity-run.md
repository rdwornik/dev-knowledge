# The Codespace parity run on lane `b2w2-codespace-finish`: run 1 recorded raw, run 2 waits on the Codex usage window

Consumers: `[#1423]`, `[#1335]`
Batch B2-W2, lane 5 (`b2w2-codespace-finish`), seat Tech-Architect-44. Contract `LANE-1423-b2w2-codespace-finish.md`, Done 2, 4 and 5 (P-L5-1, P-L5-2, P-L5-3).
Every figure below is copied from `check` output, the runner's own log or a command result kept in the lane's session file; the raw outcome of each condition is recorded unchanged and a FAIL stays a FAIL.

## What was run

- One fresh Codespace, `b2w2-codespace-finish-parity-x9pg75qpj66f9q` (`standardLinux32gb`), created 2026-10-09T20:10:51Z from branch `worktree-b2w2-codespace-finish` at `3bee6f6b4d2a3552ee59055e47d54c23ec1b3ab4` through `dispatch.py codespace-exec`; the head was `codespace_parity.py collect --side codespace --push-branch worktree-b2w2-codespace-finish-cs`. The laptop side was `collect --via-gate` (7 hooks, `audit.py health`, the fixed pytest selection through `memory_admission_gate.py`).
- Before the call: `quota_watch.py check --projected-core-hours 4` -> `OK: 45.11 used + 4.00 projected = 49.11 of 180 core-hours`; `pin check` -> `pins: clean`; laptop `claude --version` 2.1.296; `gh codespace list` empty.
- Secrets in the box (names only): `CLAUDE_CODE_OAUTH_TOKEN`, `CODEX_API_KEY`, `COPILOT_GITHUB_TOKEN`, `RCLONE_CONFIG_GDRIVE_*`, `XAI_API_KEY`. `CODEX_API_KEY` WAS in the box's environment (the creation log: `[provision] scrub: CODEX_API_KEY was set in the environment and is now unset (R87.3)` at 20:11:12Z, again 20:12:34Z and 20:12:36Z), so the unset is not vacuous.
- Cost: 24.7 min wall on `standardLinux32gb`. The check printed `core-hours 1.65 (4 cores)`; the figure I recorded in the session file at the time was about 3.3 core-hours (the projection was 4). The two disagree on the machine's core count; I did not resolve which is right, so the cost is a range, 1.65 to 3.3 core-hours.

## The five conditions, raw (`check --json-out`; the command and exit code are in each record)

| condition | raw outcome | derived disposition | note |
|---|---|---|---|
| 1 environment | `FAIL` | `FAIL` | codex returned no served id on either side (Codex usage window spent); agy BLOCKED-AUTH on the Codespace |
| 2 gates | `FAIL` | `FAIL` | 568 verdicts compared, 1 differs: `tests.test_provision_sh::test_provision_scrubs_the_keys_before_any_child_it_starts` (local passed, codespace failed) |
| 3 landing | `NOT-RUN` | `WAITING the merge gate` | the integrator's local `--no-ff` merge and the CI push verdict; no integration record exists before the merge |
| 4 transport | `NOT-RUN` | `WAITING a contract-named probe path` | read leg PASS (300 entries both sides); write leg needs `collect --probe-write NAME` and this contract names no path |
| 5 cleanup | `PASS` | `PASS` | Codespace and the scratch branch gone |

`check` exit code 1. The raw text of the check is kept in the lane's session file (`### Live parity RUN 1`).

## What run 1 found

1. **codex: `no-answer` on both sides, then diagnosed.** The identical probe run by hand on the laptop with the keys removed from the child printed, in the CLI's own words, `ERROR: You've hit your usage limit. ... try again at Oct 10th, 2026 12:38 AM.` exit 1. The ChatGPT plan's Codex window was spent; it is neither a missing login nor an API credit. `usage-limit` is now its own probe state that names the reset (commit `979d5049`). **P-L5-1 (a codex served model id with the command, the raw exit and the id) is NOT obtained by run 1.** Condition 1 stays `FAIL` for codex. The call repeats after the window clears; gate: the plan's usage window, reset about 2026-10-09T22:38Z.
2. **My own test failed only in the Codespace.** `test_provision_scrubs_the_keys_before_any_child_it_starts` asserted that a LOGIN child sees no `CODEX_API_KEY`. Inside the box a login shell re-exports the user secrets from `/workspaces/.codespaces/shared/user-secrets-envs.json`; leg_f6's `~/.profile` block is what protects a login shell, and `scrub_model_keys` protects the processes provision.sh starts. The test now probes a non-login child and its docstring says where the login-shell guarantee lives (`979d5049`). This is the difference condition 2 exists to catch.
3. **agy is BLOCKED-AUTH (R88c).** One line: `OPERATOR-ACTION: BLOCKED-AUTH: sign in to agy in the Codespace once (gh codespace ssh, open the URL it prints)`. Condition 1 cannot be PASS while it holds. **ROWS-OWED:** a headless agy sign-in lane, or a declared accepted-divergence row for agy; this lane files neither (contract: no new row).
4. **Copilot (P-L5-2) IS witnessed**, in a fresh box with nothing signed in and only the `COPILOT_GITHUB_TOKEN` secret: `copilot -p '<probe-prompt>' --model gpt-6-luna --output-format json` -> exit 0, served `gpt-6-luna`, auth mechanism `subscription (env COPILOT_GITHUB_TOKEN)`. The registry selector for the Gemini CLI that R88b removes is `providers.google.cli`, now `null`.
5. **Pins.** `claude --version` equals the generated pin on both sides (2.1.296); codex 0.155.0, copilot 1.0.94, grok 1.0.46, agy 1.3.2, gh 2.93.0 and rclone 1.73.2 are equal on both sides.

## Cleanup (P-L5-3 and the contract's teardown)

`verify-cleanup` printed `codespace_listed_after: false` and `branch_listed_after: false` (Codespace deleted 2026-10-09T20:35:33Z through the manifest-gated `codespace-delete`); the scratch branch `worktree-b2w2-codespace-finish-cs` (tip `3bee6f6b`, an ancestor of the lane branch) was deleted from origin and `git ls-remote --heads origin worktree-b2w2-codespace-finish-cs` printed nothing.

## What is not done, and why

- **Run 2 (a clean five-condition record), the codex served-id witness and the Codex review record** wait on one outside gate: the ChatGPT plan's Codex usage window (reset about 22:38Z), which falls after the 4 h cycle cap of this lane (21:41Z). Each is recorded `WAITING codex-usage-limit` in the lane's handback; none is relabelled from a FAIL.
