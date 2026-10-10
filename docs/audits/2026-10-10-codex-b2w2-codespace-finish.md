# Codex Review — b2w2-codespace-finish

**Date:** 2026-10-10
**Branch:** `worktree-b2w2-codespace-finish`
**HEAD:** `26daf704`
**Diff range:** `0bb0962b...2fee6fce`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low -- counted from the Findings section below: one Critical, one High, Medium (none), Low (none). -->
**Codex session:** `01a12642-0f32-7a10-bff0-32c0eb15682f` (served `gpt-6-astra`, read from the tool's own log)

**Model used:** `gpt-6-astra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#1423]

---

## Focus

CONTRACT: LANE-1423-b2w2-codespace-finish (row [#1423], batch B2-W3, lane `codespace-finish`). This is the close-out diff review (Done 9) of the lane's branch against main's base 0bb0962b; the range is the lane's own work (12 steps plus the W1-13 tag merge).

PROOF OF READING: begin your answer with the line `CLOSEREV-NONCE: CLOSEREV-3e91a7c05d42` and a second line `TREE: ` followed by the output of `git rev-parse 2fee6fce^{tree}` that you ran yourself.

REVIEW AT LEAST THESE, IN THIS ORDER (read the code, do not infer from commit messages):
1. Done 2 -- codex must never see an API key on any Codespace-side launch path. Enumerate every place codex is invoked or its environment is built in the diff (scripts/dispatch.py RUNNER_SECRETS / RUNNER_NEVER_SET / _codespace_runner_script / _credential_tools_script / codespace_exec; .devcontainer/provision.sh scrub_model_keys and leg_f6_codex_subscription; scripts/codespace_parity.py codex probes) and say, per path, whether CODEX_API_KEY or OPENAI_API_KEY can reach codex. Does `forced_login_method = "chatgpt"` get written without clobbering an existing config? Can any path print, log or commit a secret value?
2. Done 5 -- scripts/codespace_parity.py: each condition keeps its RAW outcome (PASS | FAIL | NOT-RUN); `disposition` WAITING <gate> may only be DERIVED from a raw NOT-RUN with a named outside gate; a raw FAIL must never become WAITING. Look for any path where FAIL is relabelled, where a NOT-RUN carries no reason, or where exit codes changed for an existing flag. Check the new `pin show|check|write` subcommand and the `usage-limit` probe state.
3. Done 9 / hygiene -- scripts/substrate_heartbeat.py D6, scripts/codespace_admission.py (check_gh_not_broken only is in scope: a token-less build is not gated, a build that offers GH_TOKEN/GITHUB_TOKEN/GH_ENTERPRISE_TOKEN is still gated), .devcontainer/provision.sh leg_f5_agy (a version skew is recorded as BLOCKED-AUTH, absence still dies), ecosystem/provider-registry.yaml (gemini out of the expectations; providers.google.cli null).
4. Tests: do the new tests assert what their names claim (seeded key reaching a stub codex; the FAIL-never-WAITING plant)? Report any test that cannot fail.

Report findings with severity Critical / High / Medium / Low, file:line, what, why, fix direction. A band with none is written "(none)". Finish with one line `VERDICT: PASS` (no Critical or High) or `VERDICT: FAIL`.


---

## Findings
CLOSEREV-NONCE: CLOSEREV-3e91a7c05d42
TREE: f07122dc9b6f9c1ae5ca01c89fe9e39e72ddcb5e

## Critical

**scripts/codespace_parity.py:860 — Codex key isolation is incomplete**

**What:** `unused_keys()` removes only keys present in the parent environment; a login shell can subsequently introduce either key without an `env -u` guard. Version collection at line 1106 and `pin show|check|write` through line 2385 also invoke Codex without explicitly scrubbing either key.
**Why:** These paths can deliver API keys to Codex, violating Done 2; a model probe can consequently exercise API authentication instead of proving subscription authentication.
**Fix direction:** Apply both forbidden names unconditionally at every Codex process boundary, including after login initialization, and test profile-only injection and version probes against a stub Codex.

## High

**.devcontainer/provision.sh:765 — Config enforcement ignores TOML scope**

**What:** The whole-file `grep` accepts `forced_login_method = "chatgpt"` inside a table or multiline string as proof of the top-level setting; `sed` likewise rewrites matching lines regardless of scope.
**Why:** Provisioning can report success while leaving the top-level policy absent or set to `"api"`, and can modify unrelated existing configuration content.
**Fix direction:** Locate and verify the actual top-level TOML key while preserving other values; cover nested and multiline occurrences in tests.

## Medium

(none)

## Low

(none)

Credential-path coverage:

| Path | Can either key reach Codex? |
|---|---|
| `RUNNER_SECRETS` / `RUNNER_NEVER_SET` | Neither is a runner secret; both are forbidden. |
| `_codespace_runner_script` | No through its direct head launch: both are unconditionally unset. |
| `_credential_tools_script` | No through `status codex`: explicit `env -u` removes both. |
| `codespace_exec` | Its helper and runner launches use the protections above, including without a mirror. |
| `scrub_model_keys` | Direct children inherit neither key. |
| `leg_f6_codex_subscription` | The appended login block removes both; config enforcement has the finding above. |
| Parity model/version/pin probes | Yes under the conditions in the Critical finding. |

No direct secret-value logging or committing was found in the reviewed additions: presence logging uses booleans, mirrored credentials travel through stdin, and fallback credentials are written to the authentication file.

Done 5 preserves raw outcomes and existing exit-code logic. WAITING is derived only from named-gate NOT-RUN outcomes; `usage-limit` remains FAIL. D6 checks pin-record consistency. Token-less admission is non-gating, rejected offered tokens remain gating, agy skew records BLOCKED-AUTH while absence refuses, and Google’s CLI fields are null.

The runner/helper/provision tests execute seeded stubs; parity’s key tests only inspect mocked environments and miss login-shell reinjection. The FAIL-never-WAITING test checks both a planted verdict and a real tree mismatch. No unconditionally passing added test was found.

Static review only; tests were not executed under the read-only constraints.

VERDICT: FAIL

---

## Disposition (lane `b2w2-codespace-finish`, B2-W3 cycle)

Both findings are in lane-owned files and are real; each was fixed RED-first (the test existed and failed
at `2fee6fce` before the change) in its own commit. The Codex diff review ran at HEAD `26daf704`; the
fixes land after it.

- **Critical -- `scripts/codespace_parity.py` codex key isolation: FIXED, `77293b87`.** `unused_keys()` now names
  both forbidden variables unconditionally; the version probes (`collect_environment`, `read_laptop_versions`)
  run codex with a scrubbed environment (`probe_env`) and, on POSIX, behind `env -u CODEX_API_KEY -u
  OPENAI_API_KEY` inside the `bash -lc` probe (`keyless_command`), so a profile that re-exports a key cannot
  reach it. Witnesses: 6 tests RED at `2fee6fce`, and a real-bash login-shell reinjection test in
  `tests/test_provision_sh.py` (stub codex records booleans only; its control arm shows the keys do arrive
  without the guard). `pin show|check|write` read the laptop's versions through `read_laptop_versions`
  (`pin_show_cmd`, `pin_check_cmd`, `pin_write_cmd`), which ran codex unscrubbed -- the review's reference to
  the pin subcommand was correct; that one call site now carries the scrubbed environment.
- **High -- `.devcontainer/provision.sh` L-F6 TOML scope: FIXED, `ce193965`.** The leg parses the file
  (stdlib `tomllib`), edits only the top-level key, re-parses and requires the result to equal the original
  plus that one key; it refuses, touching nothing, on invalid TOML or a layout it cannot edit safely.
  8 tests: nested table, multiline string, quoted copy, CRLF + idempotence, invalid file, no file.
- **J-S41 (not a Codex finding): `cfbb8bb0`.** The `credential claude codespace: expired (...)` line was a
  false-negative evidence line, not a probe defect: the Codespace-side cache is absent by design.

## Re-review (J5: one revision, one re-review)

- **Codex re-review: `WAITING codex` -- refused, no verdict.** `deploy/codex-review.ps1 -Topic b2w2-codespace-finish-rereview
  -DiffRange 26daf704..HEAD -Consumer "[#1423]" -Force` at 2026-10-10T15:40:39Z (HEAD `cfbb8bb0`), both key variables removed
  from the child. Codex session `01a12679-6fa0-7492-9950-183322430f26` (`gpt-6-astra`, read from the tool's own rollout log)
  ended in 4.7 s with `usage_limit_exceeded`; the tool printed `ERROR: You've hit your usage limit. Upgrade to Pro
  (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at
  9:40 PM.` and exited 1. The text carries no date or zone; the machine is UTC+2, so the reading is 21:40 local = **19:40Z** --
  a reading, not a datum. Not retried inside that window (S-32/S-38). The wrapper wrote no record at its output path.
- **Second route taken (common rules 2(e)): Copilot CLI `gpt-6.1-sol`**, recorded in
  `docs/audits/2026-10-10-verification-b2w2-codespace-finish-review.md`: **VERDICT: PASS** (no Critical or High remains), with
  one MEDIUM and one LOW that are recorded there and not built in this cycle (J-FIRST (3) bars building beyond the Critical and
  High findings and J-S41).
- Honest limit: no Codex verdict exists for the fixed tree. The Codex record above is a FAIL (1 Critical, 1 High) whose two
  findings were fixed; the PASS on the fix delta is the Copilot route's.
