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

---

## Amendment 1 (2026-10-10) -- verification of the fixes for the Codex re-review's Critical and High: VERDICT: PASS

The text above is left as written. After the Codex re-review (`docs/audits/2026-10-10-codex-b2w2-codespace-finish.md`, Amendment 1:
1 Critical, 1 High, VERDICT: FAIL) two more fixes were made: `0ab582d0` (the two POSIX-only test assertions) and `443f1bcb` (`f6_config`
keeps an existing config's mode; then `82d4b2de`, a lint tidy). They were verified on this route, not on Codex, because the
dispatcher barred a second Codex call while another lane held the batch's other Codex slot.

- **Reviewed:** `git diff b6f26d04..82d4b2de` over `.devcontainer/provision.sh`, `tests/test_provision_sh.py`, `tests/test_codespace_parity.py`;
  the reviewer also had the Codex findings, the contract and the four full current files. Final tree at review `dd967ba9` (the merge of
  `origin/main` and a doc-counts regeneration after `82d4b2de` touch none of these files).
- **Command:** same as above, from an isolated copy folder; started 2026-10-10T20:06:32Z, exit 0 at 20:08:22Z.
- **Served model: `gpt-6.1-sol`**, from the usage file's `currentModel` (usage file sha256 prefix `b36ceeb926c0`; its `sessionStartTime`
  2026-10-10T20:06:44.361Z matches the `~/.copilot/session-state` folder `9d43b5ab-fad0-4850-84a9-ca6320682be1` created at 20:06:44Z).
- **Nonce returned:** `CLOSEREV4-CP-c7a96b0fdf5b` (mine: the same). **Hash prefixes returned, computed by the reviewer, equal to mine:**
  `fix-delta.diff 94bc5407bde7 | codex-findings.md b2b7e665f647 | provision.sh 2a804f71145a | test_codespace_parity.py 76332e3235d3`.

### The reviewer's answer (verbatim apart from console mojibake normalised to ASCII)

NONCE: CLOSEREV4-CP-c7a96b0fdf5b
PREFIXES: fix-delta.diff 94bc5407bde7 | codex-findings.md b2b7e665f647 | provision.sh 2a804f71145a | test_codespace_parity.py 76332e3235d3

### a. HIGH -- POSIX-only test failures

**HIGH: (none). Closed.** `tests/test_codespace_parity.py:3140-3176,3204-3212` swaps only `cp.os` for a forwarding proxy with the requested `name`. Both parameterized tests therefore exercise the POSIX command-generation branch on Windows and the nt branch on POSIX, without changing pathlib's actual platform. `_ModelRun` unwraps both the login shell and `env -u`; the witness assertions independently check the platform-specific prefix, including both forbidden names.

No additional assertion fails because of the unconditional stripping change. `tests/test_codespace_parity.py:3200-3201` deliberately asserts the POSIX wrapper only on POSIX; that is appropriate, not a remaining regression. Other model argv assertions inspect normalized argv, laptop version probes retain direct argv, and the executable version test in `tests/test_provision_sh.py:804` explicitly requests `posix=True`.

### b. CRITICAL -- Existing config permissions widened

**CRITICAL: (none). Closed for POSIX mode preservation.** `.devcontainer/provision.sh:819-827` captures `stat.S_IMODE`, exclusively creates the temporary file with requested mode `0600`, writes and closes it, restores the original mode with `chmod`, then replaces the destination. Under Linux umask `022` or `077`, creation remains `0600`; subsequent `chmod` is not umask-reduced. Existing permissions, including special mode bits, are restored after writing.

There is no newly introduced read access for an existing private config. For an originally group-readable config such as `0640`, the temporary file becomes group-readable immediately before replacement, matching the original policy--not the comment's literal claim that another user can *never* read it.

On Windows, `O_BINARY` prevents CRT newline translation; `fdopen(newline="")` preserves existing CRLF without doubling carriage returns. Windows `chmod` preserves its representable read-only/writable state, **not POSIX privacy or an exact ACL**; the tests correctly avoid claiming real `0600` bits there.

The tests at `tests/test_provision_sh.py:769-801` assert actual `open -> chmod -> replace` calls, modes, targets, and resulting TOML. Both fail against the previous implementation, which uses built-in `open` and lacks `chmod`. Their Linux real-bit assertions hold under both specified umasks.

### c. Remaining findings and introduced risks

**MEDIUM: (none).**

**LOW -- `.devcontainer/provision.sh:822-827`: Failed writes leave temporary files.** An existing temp path causes `O_EXCL` to fail explicitly without truncating it or replacing the original. However, failure after successful creation leaves the temp behind; PID reuse can then block a later attempt. **Fix direction:** clean up only the temp successfully created by this invocation, using failure-safe cleanup that preserves the original exception and never removes a pre-existing collision.

**LOW -- `tests/test_provision_sh.py:744-745,781-786`: Permission tests do not record flags or the write boundary.** They can fail and distinguish the previous implementation, but would miss removal of `O_EXCL`/`O_BINARY` or moving `chmod` before the content write. **Fix direction:** record/assert flags and write ordering; add collision and injected-failure cases.

**LOW -- `tests/test_provision_sh.py:804`: Previously reported model reinjection coverage gap remains.** The executable login-reinjection test covers `_tool_probe`, not `_probe_one`; the corrected model tests verify command structure rather than executing isolation. **Fix direction:** add an executable model-probe reinjection test with a boolean-only stub and unguarded control.

No new secret-value printing/logging path or newly added test incapable of failing was found. Review was static; no tests were executed and no files were edited.

VERDICT: PASS

### Disposition of Amendment 1

- **Critical, High: none remain** (the reviewer: "HIGH: (none). Closed." and "CRITICAL: (none). Closed for POSIX mode preservation").
- **Comment accuracy (the reviewer's observation in 3b):** the code comment said the new content was never readable by another user; it is
  readable, after the `chmod`, by exactly whom the original was. The comment and one assertion message were reworded in a text-only commit.
- **LOW x3, REAL, NOT built (J-FIRST (3)); ROWS-OWED:** (1) a failed write leaves the temp file behind and PID reuse could collide with it later;
  (2) the mode tests record no flags (`O_EXCL`, `O_BINARY`) and not the write/chmod boundary; (3) no executable test of `_probe_one`'s
  `env -u` wrapper (the same gap the Codex re-review rated Low).
- Still no Codex PASS on the final tree.
