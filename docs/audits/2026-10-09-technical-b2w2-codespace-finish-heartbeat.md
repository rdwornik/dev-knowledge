# The substrate heartbeat on lane `b2w2-codespace-finish`: two reds, both cured, green on the branch

Consumers: `[#1423]`, `[#1335]`
Batch B2-W2, lane 5 (`b2w2-codespace-finish`), seat Tech-Architect-44. Contract `LANE-1423-b2w2-codespace-finish.md`, Done 1 and Done 8.
Every number below was read from a run or a command output in this lane's session file; nothing is restated from memory.

## The runs

| run | event, branch, sha | created (UTC) | result |
|---|---|---|---|
| `37783214793` | schedule, `main` `6d79ef08` | 2026-10-08T13:17:40Z | failure: `agy is 1.3.1, pinned 1.2.17` -> `REFUSED: L-F5 FAILED` |
| `37934432204` | schedule, `main` `03d21ff8` (the contract's base) | 2026-10-09T13:05:48Z | failure: `agy is 1.3.2, pinned 1.2.17` -> `REFUSED: L-F5 FAILED` |
| `37968009244` | workflow_dispatch, lane branch `ff712034` (the pre-fix tip: base + the W1-13 merge) | 2026-10-09T17:41:06Z | failure: the same refusal, `agy is 1.3.2, pinned 1.2.17` |
| `37983101579` | workflow_dispatch, lane branch `822ea7f0` (S4) | 2026-10-09T19:51:44Z | failure, **a different line**: `codespace-admission: REFUSED -- gh_not_broken` |
| `37993356450` | workflow_dispatch, lane branch `8d3013e5` (S9) | 2026-10-09T21:25:25Z | **success**, both jobs (finished 21:28:04Z) |

Session-file counting, one line per run (common rules 2 (p)):

```
ATTEMPT 1 1 agy-installer-skew start=2026-10-09T17:41:06Z end=2026-10-09T17:44:03Z outcome=FAIL
ATTEMPT 1 1 gh_not_broken start=2026-10-09T19:51:44Z end=2026-10-09T19:54:50Z outcome=FAIL
ATTEMPT 1 2 gh_not_broken start=2026-10-09T21:25:25Z end=2026-10-09T21:28:04Z outcome=PASS
```

The `agy-installer-skew` signature is cured (no attempt 2 was needed); `gh_not_broken` took two attempts, the second after the seat widened the lane's files (below). The 4 h cycle cap (2026-10-09T21:41Z, counted from the first run at 17:41:06Z) was not reached: the passing run ended at 21:28:04Z.

## Red 1, cured by S4 (`822ea7f0`): the agy installer cannot select a version

The vendor installer serves only its latest. A typed pin (`1.2.17`) therefore breaks the day the vendor ships, and `leg_f5_agy` answered with `die`, which refused the whole container. The claude pin had the same shape (typed `2.1.290` against a laptop on `2.1.295`/`2.1.296`).

What S4 changed (R70: a volatile fact is generated from one source, never typed):

- `codespace_parity.py pin show | check | write` reads each tool's own `--version` on the laptop and rewrites the typed `version:` lines of `.devcontainer/provisioning.yaml` plus a top-level generated `pins_record:` block (source, `measured_at`, versions, sha256 of the sorted `name=version` lines). `pin write` writes nothing if any tool cannot be read.
- `substrate_heartbeat.py` declaration finding **D6**: the typed pins must equal the record, and the record its own digest. A hand-edited pin is DEAD and names the tool. Actions cannot read the laptop, so the committed record is what it can check; `pin check` is the laptop-side half.
- `leg_f5_agy` ends in a recorded state (present at the pin, or present with a version skew plus BLOCKED-AUTH and one `OPERATOR-ACTION` line, R88c); absence still dies. The seven pre-install probes run with stderr silenced, so a `SKEW` or `ABSENT` line in the container log is an end state.

Evidence in run `37983101579` (job `devcontainer build + L1 marker verify`, the log kept as `hb-37983101579.log`): `grep -c "tools: SKEW\|tools: ABSENT"` = **0**; seven `tools: OK - <tool> == pin` lines: claude `2.1.296`, gh `2.93.0`, codex `0.155.0`, rclone `1.73.2`, agy `1.3.2`, grok `1.0.46`, copilot `1.0.94`; `ecosystem: OK - 1 repo(s) registered: .dev-knowledge`; `L-F6 OK -- codex is forced to the ChatGPT sign-in and no login shell carries a codex API key`; `[provision] gate OK`. Job `substrate declaration probe` (D1-D6): success. Laptop side: `pin check` -> `pins: clean`, exit 0, with the laptop's `claude --version` = `2.1.296 (Claude Code)` immediately before the live parity run.

## Red 2, found behind it: `gh_not_broken` in a credential-free container

The last step of the container job runs `bash -l -c 'python3 scripts/codespace_admission.py'`. Every condition prints OK (claude, uv, python3, pre-commit, git remote, hooks armed, contract n/a) except

```
codespace-admission: REFUSED gh_not_broken  gh is installed but gh auth status fails -- an unauthenticated gh is a broken tool, not an absent one
```

then `Dev container exec failed: (exit code: 1)`.

**Cause, from three sources.** (1) The container job is credential-free on purpose (`.github/workflows/substrate-heartbeat.yml` lines 203-206: "no model credential is referenced"), it passes no `GH_TOKEN`, and the log shows `L-F2 SKIP -- no GITHUB_TOKEN/GH_TOKEN in this environment`. (2) `scripts/codespace_admission.py::check_gh_not_broken`: gh absent -> not gated; gh present and `gh auth status` non-zero -> gating. (3) The pinned toolset installs gh (commit `aec1d23a`, foundation-13, 2026-10-04 03:24 +0200). The last green scheduled run, `37120001281` (2026-10-03), logs `codespace-admission: OK gh_not_broken  gh is absent -- not gated`.

**It is older than the agy red, and the agy red hid it.** The first scheduled red after that green, `37201398677` (2026-10-04), has no provisioning refusal at all and fails on exactly this line. The runs from `37324479187` to `37934432204` stop earlier in provisioning (agy or claude skew), so they never reached it. The contract's note N1 ("failed on one finding") is true of what stopped provisioning and not of the whole heartbeat; this record retracts the one-finding reading.

**Why attempt 1 did not edit it.** The two places that decide it are outside **Files you own**: `.github/workflows/substrate-heartbeat.yml` (the contract: no workflow edit) and `scripts/codespace_admission.py` (it mirrors the dispatcher's deployed admission test, and loosening it weakens a gate). Nothing the lane owns can make `gh auth status` pass in a container that is given no token, short of not installing gh, and Done 1 requires gh to be present. The same commit run again changes nothing, so no attempt 2 was made on it (R59 section 0a: diagnose, then OPERATOR-ACTION); attempt 2 came only with the widening below.

The OPERATOR-ACTION written at that point (kept as written):

```
OPERATOR-ACTION (Done 1, heartbeat container leg): choose ONE -- (a) in .github/workflows/substrate-heartbeat.yml give the "Build the devcontainer" step the default Actions token (env GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}, forwarded into the container), the same R2 token the prebuild step already uses and no stored secret; or (b) in scripts/codespace_admission.py make check_gh_not_broken non-gating when the environment declares no token (the log's L-F2 SKIP line); then re-dispatch substrate-heartbeat on this branch. Until then the first scheduled heartbeat after merge stays RED on this one line.
```

The dispatcher was told by a peer message after run `37983101579`; it recorded the OPERATOR-ACTION and then delivered `to-cc/AMEND-BATCH-B2-W2-ROUND2-2026-10-09.md`, whose **S-20** (read in the file itself before any edit) widens this lane's Files-you-own to `.github/workflows/substrate-heartbeat.yml`, `scripts/codespace_admission.py` (function `check_gh_not_broken` only) and the test file covering that function, with the instruction: pick the smaller fix, write a RED-first test that reproduces the red, change nothing else there.

## Attempt 2 (S9, `8d3013e5`): the fix, and the run that passed

**Choice.** Option (a) was to pass the default Actions token into the container step (workflow). Option (b), taken, is to change `check_gh_not_broken`: a failing `gh auth status` is non-gating when NO token is offered (`GH_TOKEN`, `GITHUB_TOKEN` and `GH_ENTERPRISE_TOKEN` all unset or empty), and still gating when a token was offered and gh rejects it. Reasons: (b) keeps the container job credential-free, which the workflow's own header rules (lines 203-206) and which is what makes the leg runnable in a repo with no Actions secrets; (a) would also switch on `leg_f2_git_credential` inside CI and hand a token to a third-party action's container; a Codespace always carries `GITHUB_TOKEN`, so (b) leaves its admission unchanged. The cost of (b) is stated in the commit: an environment with gh installed and no token at all is no longer refused by this check; `git_remote_reachable` and the other conditions still gate.

**RED-first.** `test_gh_installed_in_a_build_that_offers_it_no_token_is_not_gated` failed before the change (`gh is installed but gh auth status fails ... broken tool`). The existing `test_gh_present_and_broken_refuses` had built its probe with no token in the environment, which is the very red; it now supplies `GH_TOKEN`, and a parametrised test keeps the refusal for each of the three variables. `tests/test_codespace_admission.py`: 29 passed. `.github/workflows/substrate-heartbeat.yml` is untouched.

**Run `37993356450` (log kept as `hb-37993356450.log`).** Both jobs succeeded. In the container job: `grep -c "tools: SKEW|tools: ABSENT"` = **0**; `tools: OK - <tool> == pin` for claude `2.1.296`, gh `2.93.0`, codex `0.155.0`, rclone `1.73.2`, agy `1.3.2`, grok `1.0.46`, copilot `1.0.94` (14 lines, two provisioning passes); `ecosystem: OK - 1 repo(s) registered: .dev-knowledge`; `L-F6 OK`; `[provision] gate OK`; `substrate-provenance: ok`; and the line that was red:

```
codespace-admission: OK     gh_not_broken        gh is installed and `gh auth status` fails, but no token is offered in this environment (GH_TOKEN, GITHUB_TOKEN an...
codespace-admission: admission: OK -- every gating condition satisfied; Dispatch-Codespace would admit a lane here
```

agy was installed at the pin (1.3.2 == pin 1.3.2), so no BLOCKED-AUTH line was needed in the heartbeat; the Codespace's own agy sign-in is the separate R88c item in the parity record.

**Done 1 on the branch: MET** (a heartbeat run passes; the repo is registered; the claude pin is the generated record and equals the laptop's `2.1.296`, no SKEW; gh, codex, rclone present; agy present). What remains the integrator's, not the lane's: "the first scheduled heartbeat after merge is green".

## RED-first (Done 8)

The lane's tip test files were run against two older source trees, in throwaway detached worktrees under the job tmp, through `scripts/memory_admission_gate.py run`; each worktree was removed and `git worktree list` re-read (the throwaway no longer listed, path gone).

- Against the contract's base `03d21ff8` (the W1-13 work not yet merged): **88 failed, 570 passed** (3 min 04 s) over `tests/test_codespace_parity.py`, `test_dispatch_codespace.py`, `test_provision_sh.py`, `test_provision_legs.py`, `test_substrate_heartbeat.py`.
- Against the merged pre-fix tip `ff712034`: **56 failed, 602 passed** (2 min 51 s).
- The codex-environment test the contract names (an invocation's environment still carries `CODEX_API_KEY`) is red at both: `test_codex_api_key_is_no_runner_secret_and_the_never_set_names_are_the_two_keys`, `test_the_runner_hands_a_codex_head_neither_api_key_with_or_without_a_mirror[no-mirror]` and `[mirror-configured]`, `test_the_runner_script_unsets_the_two_keys_on_every_launch_and_never_expands_them`, `test_the_credential_tools_status_call_runs_codex_without_either_key`, `test_a_codex_probe_never_sees_an_api_key_even_where_the_cache_is_missing`, `test_main_scrubs_the_model_keys_first_and_writes_the_codex_policy_before_any_codex_call`, `test_leg_f6_makes_every_login_shell_unset_the_keys_and_forces_the_chatgpt_sign_in`. They pass on the lane tip (see the parity-run record for the tallies).
- Heartbeat: D6 tests (`test_a_declaration_with_typed_pins_and_no_record_is_DEAD_with_a_D6_finding`, `test_a_hand_edited_claude_pin_is_DEAD_and_names_the_tool`) are red at both and pass on the tip.
