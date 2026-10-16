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

---

## Amendment 1 (2026-10-10, after commit `b6f26d04`) -- the Codex re-review ran once the window reopened: VERDICT: FAIL

The "Re-review" section above is left as written; it recorded a usage-limit refusal at 15:41:03Z. The Codex window reopened (the
refusal text's reading was 19:40Z; the operator confirmed it at 19:44Z) and the re-review was run for real.

- **Run:** `deploy/codex-review.ps1 -Topic b2w2-codespace-finish-rereview3 -DiffRange 26daf704..HEAD -Consumer "[#1423]" -Force`,
  HEAD `b6f26d04`, both key variables removed from the child, started 2026-10-10T19:46:03Z, exit 0 at 19:48:39Z. Codex session
  `01a1275a-152a-7e93-b8b7-d8497bf4ae98` (rollout log `rollout-2026-10-10T21-46-19-...`, `gpt-6-astra`, `sandbox: read-only`, 83,935 tokens).
  The wrapper wrote its own record outside the repository (job tmp); the reviewer's findings are pasted below verbatim.
- **Proof of reading:** nonce `CLOSEREV3-b8d0f16c647f` and `TREE: a4d2f03d910705681f3cc2c53dac9ff759eb4a36` returned; my own
  `git rev-parse b6f26d04^{tree}` = `a4d2f03d910705681f3cc2c53dac9ff759eb4a36` -- equal.
- **Tally: 1/1/0/1** (Critical/High/Medium/Low), VERDICT: FAIL. (The wrapper's console summary printed `0/0/0/0` and its file kept the
  unfilled `TBD`; neither is a count -- the findings below are.)

### Findings of the re-review (verbatim)

### Findings
REREVIEW-NONCE: CLOSEREV3-b8d0f16c647f
TREE: a4d2f03d910705681f3cc2c53dac9ff759eb4a36

### Critical

**.devcontainer/provision.sh:816 — Atomic replacement widens existing permissions**

**What:** With umask `022`, rewriting an existing `0600` config creates a `0644` temporary file and replaces the private original with it.
**Why:** Other users can then read previously protected configuration contents wherever directory permissions permit; sensitive configuration is also exposed through the temporary file before replacement.
**Fix direction:** Create the temporary file privately, preserve the existing file’s permissions before writing its contents, and test permission preservation.

Copilot’s observation is real, but **Medium understates it**: this changes access control, rather than violating a convention. Under the repository’s “security issues” definition, it is Critical and should block this lane.

### High

**scripts/codespace_parity.py:887 — Unconditional stripping breaks two existing POSIX tests**

**What:** `_probe_one()` now always records `env -u CODEX_API_KEY -u OPENAI_API_KEY codex exec …` on POSIX, but `tests/test_codespace_parity.py:3146` and `:3180` still require the command to start with `codex exec `.
**Why:** Both assertions deterministically fail on the Codespace, including with neither key present in the parent; Windows can remain green.
**Fix direction:** Update both assertions to verify the platform-appropriate command, preserving checks for both forbidden keys on POSIX.

This is the concrete regression the second reviewer missed.

### Medium

(none)

### Low

**tests/test_provision_sh.py:749 — Login reinjection test covers only the version probe**

**What:** The real-bash test executes `_tool_probe()`, while the model probe’s separate `_probe_one()` wrapper has no equivalent executable reinjection test.
**Why:** The model environment tests inspect the runner’s parent environment and would still pass if its inner wrapper disappeared; the existing POSIX witness assertion provides partial structural coverage, not executable isolation proof.
**Fix direction:** Exercise `_probe_one()` through a login shell that introduces both keys, using the boolean-recording stub and an unguarded control.

Copilot’s observation is real; **Low is reasonable** because the implementation is correct and has partial coverage.

The requested closure checks, in order:

1. **Earlier Critical: closed in the implementation.** `unused_keys()` always returns both names. `_probe_one()` strips the parent environment and applies `env -u` after login initialization. `_tool_probe()` uses `keyless_command()` inside `bash -lc`, and `collect_environment()` additionally supplies `probe_env()`. `read_laptop_versions()` supplies that scrubbed environment directly, without a login shell. There is no separate Codex authentication subprocess. I found no remaining path through these boundaries that passes either key to Codex.

   The real-bash version test records both presence booleans, checks sentinel non-disclosure, and has an unguarded control; removing its wrapper breaks the final assertions. The model tests have the coverage limitation above.

2. **Earlier High: closed for TOML scope and false success.** Parsed top-level lookup, candidate re-parsing, whole-dictionary comparison, and final verification prevent the original nested/string confusion. Invalid or unsupported layouts refuse rather than report success. I found no false-success or hanging path. Replacement preserves CRLF; adding an absent key prepends an LF line.

   There are **six newly added F6 tests**, covering the listed cases, plus two existing F6 tests whose interpreter setup changed. Their assertions can fail, but not every case distinguishes the old implementation: no-file creation already worked previously. Atomic replacement introduces the permission finding above.

3. **J-S41 remains evidence-only.** The branch deciding whether to append an expiry failure is unchanged. Expired laptop credentials still fail; a missing mirrored Codex cache still fails. The changed evidence cannot turn a FAIL into a PASS.

4. **Other regressions/secrets:** The POSIX assertion failures are newly introduced. I found no additional secret-value logging path in the reviewed changes.

Validation was static. `git diff --check` passed. An attempted in-memory check through `uv` was blocked during cache initialization by read-only permissions; tests were not executed.

VERDICT: FAIL

### Disposition of Amendment 1 (lane `b2w2-codespace-finish`)

Both findings are real, in this lane's own diff, and were fixed RED-first in separate commits; the earlier Critical and High were
confirmed closed by the reviewer ("Earlier Critical: closed in the implementation", "Earlier High: closed for TOML scope and false success")
and J-S41 confirmed evidence-only.

- **Critical -- `f6_config` widens an existing config's mode: REAL, FIXED `443f1bcb`.** (The Copilot second route had rated it MEDIUM; the
  reviewer's reasoning -- it changes access control -- is accepted and the severity corrected.) The temp file is created `0600` through
  `os.open` with `O_EXCL`, takes the original's mode just before `os.replace`, and a file that is new stays `0600`. 2 tests, RED at
  `b6f26d04` (it only called `os.replace`): the helper's `os.open`/`os.chmod`/`os.replace` calls recorded in order and value (the same on
  every host -- a Windows interpreter cannot represent `0600`) plus the real bits read back on a POSIX host.
- **High -- two POSIX-only assertions: REAL, FIXED `0ab582d0`.** `unused_keys` now names both keys unconditionally, so on POSIX every codex
  probe is recorded behind `env -u CODEX_API_KEY -u OPENAI_API_KEY`; `startswith("codex exec ")` held only on Windows, the one host the lane
  ran on. The module's `os` is shown to the tests as `nt` or `posix` (pathlib untouched) and both tests are parametrized over the two.
  RED evidence: the old test file at `b6f26d04` under a POSIX view of the module fails exactly these two tests and passes the other 351;
  the corrected file passes all 355 under that view.
- **Low -- no executable test of `_probe_one`'s `env -u` wrapper: REAL, NOT built** (J-FIRST (3); owed as a row). Unchanged from the first re-review.
- **Verification of these two fixes** was done on the Copilot `gpt-6.1-sol` route (a further Codex call was barred while the batch's
  second Codex slot was held by another lane): `docs/audits/2026-10-10-verification-b2w2-codespace-finish-review.md`, Amendment 1.
  There is therefore **no Codex PASS on the final tree**; the last Codex verdict on file is this FAIL, whose two findings are fixed.
