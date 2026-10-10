# Close-out re-review (Copilot second route) -- b2w2-codespace-finish

- **Class:** verification (ADR-101 enum) · **Date:** 2026-10-10 · **Slug:** b2w2-codespace-finish-review
- **Consumer:** [#1423]
- **Contract:** `LANE-1423-b2w2-codespace-finish` (row [#1423], batch B2-W3, lane `b2w2-codespace-finish`), Done 9, J5 and J7;
  the second route named by the batch common rules 2(e) after a Codex usage-limit refusal.
- **Status:** a measurement of three lane commits by a read-only reviewer; it closes no row and grants no authorization.

## What was reviewed

The three fix commits made after the Codex close-out review (`docs/audits/2026-10-10-codex-b2w2-codespace-finish.md`, VERDICT: FAIL,
1 Critical + 1 High): `77293b87` (Critical: codex key isolation at every parity probe boundary), `ce193965` (High: L-F6 sets and
verifies the TOP-LEVEL `forced_login_method`), `cfbb8bb0` (J-S41: evidence wording). Diff `26daf704..cfbb8bb0` over
`.devcontainer/provision.sh`, `scripts/codespace_parity.py`, `tests/test_codespace_parity.py`, `tests/test_provision_sh.py`.

## Route and proof

- **Why this route.** The Codex re-review was refused (`usage_limit_exceeded`, 2026-10-10T15:41:03Z, reset text `9:40 PM`, read as
  19:40Z) and is recorded `WAITING codex` in the Codex record's Re-review section; it was not retried inside that window.
- **Command** (run from an isolated copy folder, which held `contract.md`, `first-review.md`, `fix-delta.diff` and the four full
  current files; no repository access): `copilot -p <prompt> --model gpt-6.1-sol --add-dir <folder> --allow-all-tools
  --no-ask-user -s --no-color --usage-output-file <file>`, started 2026-10-10T15:53:53Z, exit 0 at 15:57:37Z.
- **Served model: `gpt-6.1-sol`**, read from the usage file's `currentModel` (usage file sha256 prefix `17816aab3f7a`; its
  `sessionStartTime` 2026-10-10T15:53:59.220Z matches the `~/.copilot/session-state` folder `f230f4f2-8dd1-40ec-91fe-99453c3d5299`
  created at 15:53:59Z -- the tool records no session id of its own).
- **Nonce returned:** `CLOSEREV2-CP-ec623958df52` (mine: the same). **Hash prefixes returned, computed by the reviewer, equal to mine:**
  `fix-delta.diff 2c8b03f5e7e3 | first-review.md 2b1cb1329ee5 | provision.sh 47453a07180e | codespace_parity.py f427c8650d59`.
  Prompt sha256 prefix `27760cc22193`; answer file sha256 prefix `ee40f85e495d` (console mojibake of dashes/arrows normalised to ASCII below).

## The reviewer's answer (verbatim apart from that normalisation)

NONCE: CLOSEREV2-CP-ec623958df52
PREFIXES: fix-delta.diff 2c8b03f5e7e3 | first-review.md 2b1cb1329ee5 | provision.sh 47453a07180e | codespace_parity.py f427c8650d59

### a. Critical key isolation -- closed by 77293b87

**CRITICAL: (none). HIGH: (none). MEDIUM: (none).**

| Checked path | Can either key reach Codex? |
|---|---|
| `unused_keys`, `files\codespace_parity.py:881-893` | No through its consumers: both forbidden names are returned unconditionally, including with neither key in the parent and with no cache. |
| `collect_models` -> `_probe_one` -> `_status_probe`, `files\codespace_parity.py:914-923` | No. Both are removed from the subprocess environment; on POSIX, `env -u CODEX_API_KEY -u OPENAI_API_KEY` executes **inside** the login shell, after profiles run. |
| `collect_environment` -> `_tool_probe`, `files\codespace_parity.py:562-571,1133-1135` | No. The parent environment is scrubbed; POSIX version probes additionally unset both names after login initialization. Windows executes directly with the scrubbed environment. |
| `collect_auth`, `files\codespace_parity.py:229,587-594` | No Codex invocation exists here: `AUTH_PROBES["codex"]` is `None`. |
| `read_laptop_versions`, `files\codespace_parity.py:2419-2427` | No. Codex executes directly with both names removed; this path does not start a login shell. |
| `pin show`, `files\codespace_parity.py:2688` | No; delegates to the protected laptop-version reader. |
| `pin check`, `files\codespace_parity.py:2699` | No; delegates to that reader. `--record-only` invokes no CLI. |
| `pin write`, `files\codespace_parity.py:2715` | No; delegates to that reader. |

The new tests cannot collectively pass if the unconditional-name fix, version-command guard, or environment scrubbing is removed. The login-shell test at `files\test_provision_sh.py:717-754` executes the generated version probe against a boolean-recording Codex stub. Its unguarded control proves reinjection actually occurred; removing the version guard fails the final assertions.

**LOW -- `files\test_codespace_parity.py:3236-3295`; `files\test_provision_sh.py:717-754`: model-boundary mutation remains uncovered.** Removing only `_probe_one`'s runtime `env -u` wrapper at `files\codespace_parity.py:919-922` can leave these new tests passing: model tests inspect scrubbed environments through mocks, while the executable reinjection test exercises only `_tool_probe`. This is a coverage gap, not a remaining leak in the current implementation. **Fix direction:** exercise the actual model-probe boundary against a profile-reinjecting shell and boolean-recording stub.

### b. High top-level TOML enforcement -- closed by ce193965

**CRITICAL: (none). HIGH: (none). MEDIUM: (none). LOW: (none).**

`files\provision.sh:778-818,853-854` parses the original TOML before deciding whether the **top-level** key already equals `"chatgpt"`. Candidate discovery uses regexes, but those are not the correctness proof: each candidate must re-parse to exactly `{**original_data, forced_login_method: "chatgpt"}` before replacement. The final check independently re-parses the written file.

Consequently, misleading nested or multiline occurrences cannot establish success, and candidates altering another parsed setting are rejected. Invalid TOML refuses before any write. Unsupported valid layouts can also refuse safely--for example, a table-looking line inside a multiline string can stop candidate discovery prematurely. I found no ordinary finite TOML input that reports success with the wrong top-level value, changes another parsed setting, or creates an infinite loop.

The write uses a same-directory temporary file and atomic `os.replace`. Existing CRLF is retained when rewriting the matched line; when adding a previously absent key, the new prefix uses LF while the original bytes remain intact.

The executable tests at `files\test_provision_sh.py:658-714` cover nested tables, multiline strings, repeated copies inside strings/tables, CRLF plus idempotence, invalid input left untouched, and an absent file. Each has substantive assertions that can fail. Coverage does **not** include an actually quoted top-level key such as `"forced_login_method"`, duplicate TOML definitions, or a false table boundary inside a multiline string.

### c. J-S41 -- evidence-only confirmed

**CRITICAL: (none). HIGH: (none). MEDIUM: (none). LOW: (none).**

`files\codespace_parity.py:1797-1827` changes only evidence construction within the existing non-mirrored-Codespace branch. Its `continue` already existed; the conditions and additions to `problems` are unchanged. Therefore this commit cannot turn an existing FAIL into PASS.

Laptop-side expired credentials still append a failure, and the independent laptop served-model comparison still rejects a dead sign-in. Codex remains `route="mirror", refresh="guarded"`; a missing Codespace cache records `expired` and still fails. Tests at `files\test_codespace_parity.py:3327-3342` explicitly assert both cases. The revised Claude evidence retains the underlying cache-reading detail rather than discarding it.

### d. Newly introduced regression / secret output

**CRITICAL: (none). HIGH: (none).**

**MEDIUM -- `files\provision.sh:815-818`: atomic replacement loses restrictive file permissions.** With umask `022`, rewriting an existing mode-`0600` config creates a mode-`0644` temporary file and replaces the protected original with it. Previously, the rewrite branch used `sed -i`, preserving its mode. Configurations containing secret-valued MCP environment/header settings can consequently become readable by other local users where directory permissions permit access. **Fix direction:** create the temporary file securely, preserve the existing file's restrictive mode before replacement, use a private mode for new files, and add a permission-preservation test.

**LOW: (none).**

No new direct secret-value printing or logging was found in the normal reviewed flows. Commands and evidence contain variable names, paths, states, and boolean presence readings--not credential values.

Static re-review only: the full first review and diff were read, hashes were shell-computed, no files were edited, and no tests were executed.

VERDICT: PASS

## Disposition (lane `b2w2-codespace-finish`)

- **Critical, High: none remain** -- the reviewer's own words for the Critical ("closed by 77293b87", every path tabulated) and the High
  ("closed by ce193965"). J-S41 confirmed evidence-only. VERDICT: PASS by the J5 calibration (PASS unless a CRITICAL or HIGH remains).
- **MEDIUM `provision.sh:815-818` -- the atomic replace loses an existing config's restrictive mode: REAL, NOT built in this cycle.**
  The rewrite branch used `sed -i` before (which keeps the file's mode); `os.replace` of a fresh temp file gives it the umask's mode,
  so an existing `0600` `~/.codex/config.toml` that is rewritten (a forced `api` -> `chatgpt`) becomes `0644`. (The add-the-key branch
  already created its file with the umask's mode before this change, so nothing new there.) Why not built: J-FIRST (3) bars building
  beyond the Critical/High findings and J-S41, and a further commit would be a tree no reviewer has read. Fix direction for the row:
  open the temp file `0600`, `chmod` it to the original's mode before `os.replace`, a private mode for a new file, and a mode-preservation
  test that is meaningful only on a mode-capable host (CI Linux; a Windows host cannot represent `0600`). **ROWS-OWED.**
- **LOW -- no executable test of `_probe_one`'s runtime `env -u` wrapper (model boundary): REAL coverage gap, not a leak.** The login-shell
  reinjection test exercises `_tool_probe`; the model probe's wrapper is covered by environment-inspecting mocks only. **ROWS-OWED.**
- **Not covered, stated by the reviewer and accepted as stated:** a quoted top-level key `"forced_login_method"`, duplicate TOML
  definitions, and a table-looking line inside a multiline string can make `f6_config` REFUSE (it never reports a false success); the
  refusal is the designed fail-closed behaviour.
