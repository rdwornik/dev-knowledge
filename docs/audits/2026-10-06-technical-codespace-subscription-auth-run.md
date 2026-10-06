# Codespace sign-in mirror -- run record (b2-codespace-subscription-auth, batch B2-W1, lane W1-13)

Consumer and contract: `LANE-B2-W1-b2-codespace-subscription-auth` (batch B2-W1, lane W1-13; ADR-126, R63, R65, R82, R83, R87; related rows [#1335], [#1379], [#1410], [#1411]). This record is the run record Done-item 6 asks for; it files and closes no row.

> **Status: run 1 complete and read; run 2 (a codex diagnostic) was killed by the host's memory reaper
> four minutes in, before its runner started, and its Codespace was harvested and deleted; run 3 (repair 1, the same
> diagnostic) was refused by the recovery-container check on an agy installer/pin skew before any runner started, and
> was deleted too (see "Run 3").** Nothing in
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

## Vendor documentation (retrieved 2026-10-06; passages exactly as the fetch returned them)

Each passage is a short quote from the vendor page named; none is a credential. A fetch that returned a summary rather than
page text is marked **(fetch summary)**: it is evidence of what the page says, not a verbatim quote. Page names are as fetched
on 2026-10-06 (`developers.openai.com/codex/auth` answered 308 to `learn.chatgpt.com/docs/auth`).

**OpenAI Codex auth** -- `https://learn.chatgpt.com/docs/auth`:

> "Codex caches login details locally in a plaintext file at `~/.codex/auth.json` or in your OS-specific credential store."

> "`file` stores credentials in `auth.json` under `CODEX_HOME` (defaults to `~/.codex`). `keyring` stores credentials in your operating system credential store and fails if it is unavailable. `auto` uses the OS credential store when available, otherwise falls back to `auth.json`. `ephemeral` keeps credentials in memory only for the current process."

> "Treat `~/.codex/auth.json` like a password: it contains access tokens. Don't commit it, paste it into tickets, or share it in chat."

> "In the terminal where you're running Codex, choose one of these options: In the interactive login UI, select **Sign in with Device Code**. Run `codex login --device-auth`."

> "On a machine where you can use the browser-based login flow, run `codex login`. Confirm the login cache exists at `~/.codex/auth.json`. Copy `~/.codex/auth.json` to `~/.codex/auth.json` on the headless machine."

> "Codex refreshes tokens automatically during use before they expire, so active sessions usually continue without requiring another browser login."

**OpenAI Codex CI/CD auth** -- `https://learn.chatgpt.com/docs/auth/ci-cd-auth` **(fetch summary** of the page's bolded rules**)**:

> "Do not share the same file across concurrent jobs or multiple machines."

> "Use one `auth.json` per runner or per serialized workflow stream."

> "another machine or concurrent job rotated the token first" (given as a reason a refresh stops working)

The same fetch states the page "does not explicitly address whether refresh tokens are single-use or rotating" and names about 8 days
as when a ChatGPT session goes stale. **This is the point the review record addresses:** the lane copies the laptop's file to each
Codespace launch, which puts a second machine on the same file, guarded only by a cache age under 7 days.

**GitHub Copilot CLI authenticate** -- `https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli`:

> "the CLI stores your OAuth token in your operating system's keychain under the service name `copilot-cli`"

> "If the system keychain is unavailable for example, on a headless Linux server without `libsecret` installed the CLI prompts you to store the token in a plaintext configuration file at `~/.copilot/config.json`"

Token precedence on the page: `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`, the keychain OAuth token, the GitHub CLI fallback.
Supported: `gho_` OAuth, `github_pat_` fine-grained PAT, `ghu_` App user-to-server; classic `ghp_` is not supported.

**GitHub Copilot CLI install** -- `https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli`: `npm install -g @github/copilot`; "Node.js 22 or later".

**Gemini CLI authentication** -- `https://geminicli.com/docs/get-started/authentication.md` **(fetch summary)**:

> "Headless mode will use your existing authentication method, if an existing authentication credential is cached."

> "Your credentials will be cached locally for future sessions" (the page does not name the path, and the fetch found nothing on copying credentials to another machine)

**Gemini CLI install** -- `https://github.com/google-gemini/gemini-cli`: `npm install -g @google/gemini-cli` (no Node version stated in the fetched text).

**Antigravity CLI (agy)** -- `https://antigravity.google/docs/cli/install`:

> "When launching `agy` on your local machine, the CLI attempts to access your operating system's native secure keyring (such as Apple Keychain, Linux Secret Service/D-Bus, or Windows Credential Manager)."

Same page (fetch summary): a headless/SSH host gets "a manual URL loop"; `GEMINI_API_KEY` works only with `modelProvider` set to `gemini` in
`~/.gemini/antigravity-cli/settings.json` ("Setting a `GEMINI_API_KEY` environment variable on its own has no effect"); that settings file holds configuration, not a credential.

**Claude Code setup token** (`claude setup-token`, `https://code.claude.com/docs/en/setup`): the page fetch is not among the tool results
recovered from transcript `2ee71b9b`, so the earlier sentence (a long-lived token for headless use, supplied as `CLAUDE_CODE_OAUTH_TOKEN`) stands as a
**paraphrase, not a quote**. This is the one passage still owed: `ROWS-OWED` (re-fetch and quote it).

**xAI grok** (a web-search result summary; no vendor page was fetched): the xAI CLI authenticates by `--api-key` or `XAI_API_KEY`, and
"In a headless environment, you can run `grok login --device-code`." The laptop itself uses the key variable, so the Codespace uses the same env key (R87: a key only where the laptop uses one).

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

### Run 3 (repair 1) -- `b2-sub-auth-run3-q945j7g69vqf69v`, created 09:27:35Z, deleted 09:39:50Z

The one extra Codespace the dispatcher allowed (3rd of 6): the codex diagnostic, run through `dispatch.py codespace-exec` after
`quota_watch.py check --projected-core-hours 16` -> `OK: 44.30 used + 16.00 projected = 60.30 of 180`.

- **Result: the launch was refused by its own recovery-container check; no runner started, so codex was not read.** The creation
  log shows `provision.sh` ending `REFUSED: L-F5 FAILED -- agy is not the pinned 1.2.17 in a login shell` (`agy is 1.3.0`): the
  Antigravity installer "takes no version" (the pin's own comment), serves its latest, and the vendor has moved from 1.2.17 to 1.3.0
  since the pin was typed. The laptop still reads `agy --version` 1.2.17. The legs before it passed (claude re-pinned to 2.1.290,
  gh 2.93.0, codex 0.155.0, rclone 1.73.2); the gemini and copilot legs come after agy and were **not reached**, so this run says
  nothing about them.
- This is not caused by this lane's diff: `origin/main` carries the same agy pin and the same installer, so **any fresh Codespace on
  `main` fails the same leg today.** The same class was recorded once before (W1-12: `agy is not the pinned 1.2.16`, re-typed to
  1.2.17). Not worked around here: re-typing the pin to 1.3.0 makes C1 read an agy version skew against the laptop (1.2.17), and
  whether the pin follows the vendor's latest or the laptop is not this lane's call -- it is the WAITING gate below.
- The mirror's record before the box existed read the same as run 1: codex `mirrored` (last refreshed 2.7 days ago, verdict `guarded`).
- Harvest (creation log only), `codespace-delete` (exit 0, manifest verified), `verify-cleanup`: `codespace_listed_after: false`; no run
  branch on origin.

### Cost and cleanup, all three runs

- Wall time 14.1 min (run 1), 7.7 min (run 2) and 12.3 min (run 3) on an 8-core machine: about 1.9 + 1.0 + 1.6 = **4.5 core-hours**
  (the projection was 16 per run). All three `verify-cleanup` records read `codespace_listed_after: false`; `git ls-remote --heads origin`
  shows no run or scratch branch (the only `worktree-b2-codespace-subscription-auth` is this lane's deliverable). 3 of 6 Codespaces used.

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

0. **agy installer vs pin (found by run 3, blocks every fresh Codespace, not only this lane's):** the vendor installer serves agy 1.3.0 and
   takes no version; the pin and the laptop read 1.2.17. Which is the rule: the pin follows the laptop (then the installer cannot meet it
   until the laptop updates agy, or the leg takes a versioned binary URL if the vendor has one), or the pin follows the vendor's latest
   (then C1's agy equality needs a ruling)? Until ruled, no fresh Codespace provisions, so the codex run cannot be repeated.

1. codex in the Codespace answered `no-credits` on the mirrored subscription while the laptop's same cache answers. Is
   the ChatGPT plan's Codex allowance the cause? Until it is read in the box, codex is not proven (item 1 and 5 for codex unmet).
2. copilot's Codespace uses a PAT secret while the laptop uses the keyring: accept the secret as the laptop-equivalent, or leave it WAITING?
3. gemini: set provider google's `cli` to null in the registry (outside this lane's files) so C1 stops expecting a retired CLI?

## OPERATOR-ACTION

- OPERATOR-ACTION: if codex stays unserved, seed a separate login: `codex login --device-auth` with `CODEX_HOME` pointing at an empty scratch folder, then `gh secret set CODEX_AUTH_JSON --user < <scratch>/auth.json`.
- OPERATOR-ACTION: run `copilot login` once in the Codespace (`gh codespace ssh`), or rule that `COPILOT_GITHUB_TOKEN` is the laptop-equivalent.
- OPERATOR-ACTION: sign in to agy in the Codespace once (`gh codespace ssh`, open the URL it prints) -- `BLOCKED-AUTH` stays (R83).
- OPERATOR-ACTION: turn the laptop's claude and grok auto-update off, or accept that each launch re-derives claude to the laptop's version (laptop claude moved 2.1.290 -> 2.1.291 and grok 1.0.44 -> 1.0.46 during this lane).
- OPERATOR-ACTION: rule the agy pin (QUESTION 0): either update the laptop's agy to the version the vendor installer serves (1.3.0) so the pin and the laptop agree, or tell the lane that the pin follows the vendor installer; until then every fresh Codespace refuses at `provision.sh` leg L-F5.
