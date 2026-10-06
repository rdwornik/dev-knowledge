# Codespace sign-in mirror -- run record (b2-codespace-subscription-auth, batch B2-W1, lane W1-13)

> **Status: run 1 complete and read; run 2 (a codex diagnostic) was killed by the host's memory reaper
> four minutes in, before its runner started, and its Codespace was harvested and deleted.** Nothing in
> this record is a value: names, paths, modes, booleans and served model ids only (R13).

## What the laptop signs in with (measured 2026-10-06; booleans and paths only, no value read)

- claude: subscription, by the file `.claude/.credentials.json` (refresh token live); no API-key variable.
- codex: subscription (ChatGPT), by the file `.codex/auth.json`, `last_refresh` 2.5 days ago; a `CODEX_API_KEY`
  variable IS set in the laptop's environment and is not what answers (the served-id probe strips it).
- gemini: a file `.gemini/oauth_creds.json` exists with a refresh token, but the call exits 1 and the CLI
  reports `IneligibleTierError`; the registry itself calls the gemini CLI retired.
- grok: API key, by `XAI_API_KEY`; no sign-in file, no keyring entry.
- agy: OS keyring (Windows Credential Manager entry `gemini:antigravity`); no file, no key variable.
- copilot: OS keyring (Windows Credential Manager entry `copilot-cli`); no file, no key variable.
- gh: OS keyring. rclone: a `rclone.conf` that also holds other remotes (an employer drive) and so is never copied.
- deepseek: the registry names no CLI for this provider.
- Versions at the run: claude 2.1.291, codex 0.155.0, copilot 1.0.92, grok 1.0.46, gemini 0.56.0, agy 1.2.17,
  gh 2.93.0, rclone 1.73.2.

## Vendor documentation (retrieved 2026-10-06)

Read, not quoted here word for word -- the exact passages are in the lane's session transcript, and this
section is therefore a **paraphrase with the page named**, which is a gap against the contract's "dated quotes":

- OpenAI Codex auth (`https://developers.openai.com/codex/auth`, `.../auth/ci-cd-auth`): a ChatGPT sign-in is
  stored in `~/.codex/auth.json`, copying it to a headless machine is a documented path, and the same page
  says not to share that file across concurrent machines because the refresh token is single-use. This is why
  codex is mirrored only while the file is fresh (under 7 days; the vendor refreshes at 8), so the Codespace
  never has to refresh it.
- Claude Code (`https://code.claude.com/docs/en/setup`, `claude setup-token`): a long-lived token for headless
  use, supplied as `CLAUDE_CODE_OAUTH_TOKEN`. The laptop's OAuth file rotates its refresh token, so it is not copied.
- Gemini CLI (`https://github.com/google-gemini/gemini-cli`): headless mode uses the cached credential.
- GitHub Copilot CLI (`https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli`):
  the sign-in lives in the OS keychain, with a plaintext config fallback only on a host that has none.
- agy (`https://codelabs.developers.google.com/antigravity-cli-hands-on`): the OS keyring, or `GEMINI_API_KEY`
  with `modelProvider=gemini`, which the laptop does not use.

## The run

- Quota first: `quota_watch.py check --projected-core-hours 16` -> `OK: 42.86 used + 16.00 projected = 58.86 of 180`.
- Driver: `dispatch.py codespace-exec` (the launch mirrors, checks expiry before a box exists, derives claude's
  version, proves no credential leaked), then `codespace_parity.py check`, `dispatch.py codespace-harvest`,
  `codespace-delete`, `codespace_parity.py verify-cleanup`. The head command was the parity `collect` itself, so
  no production lane ran in a Codespace.

### Run 1 -- `b2-sub-auth-run-x9pg75qx5j4f96r9`, `standardLinux32gb`, created 04:46Z, deleted 05:00Z

Launch mirror, per CLI (action / route):
- claude: not mirrored; setup-token route; the Codespace's claude was re-installed to the laptop's version
  (laptop 2.1.291, Codespace 2.1.291 after `claude-install`; the box was provisioned at the 2.1.290 pin).
- codex: **mirrored**, `.codex/auth.json`, mode 600, cache age 2.5 days, refresh verdict `guarded`.
- copilot: waiting (keyring entry, nothing to mirror). gemini: not mirrored (refresh verdict `unknown`; sign-in dead).
- agy: waiting (keyring). grok: env-key (the laptop uses the key too). gh: the Codespace's own `GITHUB_TOKEN`.
  rclone: the Drive token secret. deepseek: no CLI.
- No credential reached any artefact (hash and string-leaf leak check, names only).

Per-provider served id and sign-in on the Codespace, from the Codespace's own record:
- claude: served `claude-sonnet-5`, subscription via `CLAUDE_CODE_OAUTH_TOKEN` (the laptop: subscription via file) -- same class.
- codex: **no served id**, state `no-credits`; sign-in subscription via `.codex/auth.json` and no key variable present.
  Not explained: the same cache served `gpt-6-astra` on the laptop minutes earlier. Run 2 was to read the CLI's own
  message in the box and was killed before it ran.
- copilot: served `gpt-6-luna`, **api-key via `COPILOT_GITHUB_TOKEN`** against keyring on the laptop -> R87 FAIL.
- grok: served `grok-4.7`, api-key via `XAI_API_KEY` -- same as the laptop.
- gemini: no served id (exit 41); no sign-in on the Codespace (laptop: subscription, but dead) -> FAIL.
- agy: not probed, login missing (named auth item); `BLOCKED-AUTH` stands (R83).
- gh and rclone authenticated (env token / the Drive token secret).

`check` verdicts: condition 1 FAIL (the named reasons above; every tool version equal on both sides), condition 2
FAIL because both gates legs were skipped on purpose (`--skip-gates`; not this lane's condition), condition 3 FAIL
because the laptop record was taken at `6d0cb33a` and the branch tip had moved to `5968b538` (a stamp mismatch of my
own making, not a landing defect), condition 4 read PASS (294 entries) and write NOT-RUN, condition 5 not given a cleanup record
until after teardown.

**Defect found by the run and fixed (`05bc62a4`):** C1 printed "the claude credential on the codespace side has
expired" because `.claude/.credentials.json` is absent there by design. Only a cache the launch mirrors can expire on
the Codespace side now (RED-first test `test_a_cache_file_the_codespace_never_receives_is_not_an_expired_credential`).

Cleanup (`verify-cleanup`): `codespace_listed_after: false`. The lane branch is still on origin because it is this
lane's deliverable branch, not a run branch.

### Run 2 -- `b2-sub-auth-run2-54r7jgp5gqpcvqrp`, created 05:25Z, deleted 05:33Z

A codex diagnostic (the CLI's own message under lane conditions). The host's memory reaper killed the launching
process while the box was still being set up; `codespace-observe` read `runner_alive: false, receipt_present: false`,
so no head command ever ran. Harvested (creation log only) and deleted; `gh codespace list` was empty afterwards.

### Cost and cleanup, both runs

- Wall time 14.1 min (run 1) and 7.7 min (run 2) on an 8-core machine: about 1.9 + 1.0 = **2.9 core-hours** (the
  projection was 16). Both `verify-cleanup` records read `codespace_listed_after: false`; `git ls-remote --heads origin`
  shows no run or scratch branch (the only `worktree-b2-codespace-subscription-auth` is this lane's deliverable).

## DECIDED-BY-LANE

- Channel: the credential bytes travel on `gh codespace ssh` stdin to an allow-listed helper (`credential-tools.sh`,
  umask 077, dir 700, file 600, prints only the mode). No credential file is written under the worktree or `~/.claude`.
- Per-CLI routes are the `SIGN_IN` table in `scripts/codespace_parity.py`; the provider list is generated from the registry (R70).
- gh and rclone: not mirrored. gh uses the Codespace's issued token; rclone's config holds other remotes.
- claude: the long-lived setup token (a Codespaces secret), because the OAuth file's refresh token rotates.
- No destructive refresh probe was run on codex or claude: a refresh from a second machine could sign the laptop out.
- gemini is treated as retired per the registry; no gemini credential is mirrored.
- The devcontainer now installs the gemini (0.56.0) and copilot (1.0.92) CLIs at the laptop's pins; grok's pin moved 1.0.44 -> 1.0.46.

## QUESTION (functional; operator or architect)

1. codex in the Codespace answered `no-credits` on the mirrored subscription while the laptop's same cache answers. Is
   the ChatGPT plan's Codex allowance the cause? Until it is read in the box, codex is not proven (item 1 and 5 for codex unmet).
2. copilot's Codespace uses a PAT secret while the laptop uses the keyring: accept the secret as the laptop-equivalent, or leave it WAITING?
3. gemini: set provider google's `cli` to null in the registry (outside this lane's files) so C1 stops expecting a retired CLI?

## OPERATOR-ACTION

- OPERATOR-ACTION: if codex stays unserved, seed a separate login: `codex login --device-auth` with `CODEX_HOME` pointing at an empty scratch folder, then `gh secret set CODEX_AUTH_JSON --user < <scratch>/auth.json`.
- OPERATOR-ACTION: run `copilot login` once in the Codespace (`gh codespace ssh`), or rule that `COPILOT_GITHUB_TOKEN` is the laptop-equivalent.
- OPERATOR-ACTION: sign in to agy in the Codespace once (`gh codespace ssh`, open the URL it prints) -- `BLOCKED-AUTH` stays (R83).
- OPERATOR-ACTION: turn the laptop's claude and grok auto-update off, or accept that each launch re-derives claude to the laptop's version (laptop claude moved 2.1.290 -> 2.1.291 and grok 1.0.44 -> 1.0.46 during this lane).
