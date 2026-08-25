# PROBE-PROVIDERS — report

| Field | Value |
|---|---|
| **Run** | 2026-08-25, local Windows 11, read-only |
| **Host** | `C:\Users\1028120` |
| **Repo writes** | none (registry read only; sole write is this file) |
| **Credentials** | none entered, requested, pasted or refreshed |
| **Registry compared** | `Documents\Dev\.dev-knowledge\ecosystem\provider-registry.yaml` |

## 1. Provider table

| Provider | CLI present (path / version) | Auth | Command used → verbatim output line | Config root | Registry state | Gap (one line) |
|---|---|---|---|---|---|---|
| **Claude** (Anthropic) | YES — two installs. PS: `C:\Users\1028120\AppData\Roaming\npm\claude.cmd`; git-bash: `C:\Users\1028120\.local\bin\claude.exe`. Both `2.1.245 (Claude Code)` | **ALIVE** | `claude auth status` → `"loggedIn": true`, `"authMethod": "claude.ai"`, `"subscriptionType": "max"` | `~/.claude` — exists, 2026-08-25 11:34 (`.credentials.json` 10:49) | `providers.anthropic` `cli: claude` — **accurate** | Two installs on PATH; npm shim prints `'m' is not recognized...` to stderr on every call |
| **Codex** (OpenAI) | YES — `C:\Users\1028120\AppData\Roaming\npm\codex.ps1`, `codex-cli 0.145.0` | **ALIVE** | `codex login status` → `Logged in using ChatGPT` (exit 0) | `~/.codex` — exists, 2026-08-24 19:11 (`auth.json` 2026-08-24 01:13) | `providers.openai` `cli: codex` — **accurate** | None found |
| **Gemini** (Google) | YES — `C:\Users\1028120\AppData\Roaming\npm\gemini.ps1`, `0.56.0` | **ABSENT** (creds on disk, server-rejected) | no status/whoami subcommand exists in `gemini --help`; probe `gemini -p "ok" -o json` → `Error authenticating: IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals` (`reasonCode: UNSUPPORTED_CLIENT`, `tierId: free-tier`) | `~/.gemini` — exists, 2026-08-20 14:14 (`oauth_creds.json` 2026-08-20 13:54) | `providers.google` `cli: gemini` + comment *"The CLI is live on this surface and was verified rather than assumed"* — **CONFIGURED-BUT-DEAD** | Registry asserts liveness; binary runs but the account tier is refused. Version claim still true, liveness claim now false |
| **Grok** (xAI) | YES — `C:\Users\1028120\.grok\bin\grok.exe`, `grok 1.0.5 (5115b46bc9)` | **ALIVE** (credential present; validity unproven) | `grok models` → `You are using XAI_API_KEY.` + `Default model: grok-4.6` (exit 0) | `~/.grok` — exists, 2026-08-25 11:59 (`auth.json` 11:58) | `providers.xai` `cli: null` + comment *"Re-verified 2026-08-23: `grok` is not on PATH"* — **LIVE-BUT-UNREGISTERED** | Registry says no CLI; a live one is on PATH and self-updated during this probe |
| **Cursor** | **NO** — `cursor` and `cursor-agent` do not resolve; no install root under `AppData\Local\Programs`, `Program Files` | **ABSENT** (nothing to authenticate) | not run — no binary | none | **no `cursor` row exists** in the registry | Documented binary name is `agent`, which resolves here to Grok — see §2 |
| **DeepSeek** | **No official CLI exists** (vendor ships none; all community projects). Third-party present: `deepcode` → `C:\Users\1028120\AppData\Roaming\npm\deepcode.ps1`, `0.1.33` (`@vegamo/deepcode-cli`) | **ABSENT** | no status/whoami command in `deepcode --help`; documented key home `~/.deepcode/settings.json` **does not exist** | `~/.deepcode` — exists, 2026-07-17 16:24, holds only `machine-id` + `update-check.json` | `providers.deepseek` `cli: null` — **accurate** | `DEEPSEEK_API_KEY` is set in env but `deepcode` reads `settings.json`, so the key is likely unused; `deepseek-tui@0.8.47` is installed with **no bin at all** (legacy stub, renamed `codewhale`) |
| **Antigravity** (`agy`) — *not in the six, found live* | YES — `C:\Users\1028120\AppData\Local\agy\bin\agy.exe`, `1.1.16` | **ALIVE** (strongest evidence of the run — real server round-trip) | no status subcommand in `agy --help`; probe `agy models` → `Fetching available models...` then a served list (`gemini-3.7-flash-high`, `claude-opus-4-6-thinking`, …), exit 0 | `AppData\Local\antigravity` (2026-07-03) + `AppData\Roaming\antigravity`; **not** `~/.agy` or `~/.antigravity` | **absent entirely** from the registry | The migration target Google's own error message names is live, authenticated, first on PATH, and unrecorded |

## 2. Name-collision check

`Get-Command <name> -All`, every resolution in PATH order, full paths:

| Name | # | Type | Resolves to |
|---|---|---|---|
| `agent` | 1 (only) | Application | `C:\Users\1028120\.grok\bin\agent.exe` |
| `cursor-agent` | — | — | **no resolution (absent)** |
| `grok` | 1 (only) | Application | `C:\Users\1028120\.grok\bin\grok.exe` |

**`agent.exe` and `grok.exe` are the same program**, not merely similarly named:

- identical size — `142651720` bytes each
- identical SHA256 — `4B924DAA801663EA20E96382408B1F2B5BA39EFAD62C14D20D88618A9EB0BE64`
- `agent --version` → `grok 1.0.5 (5115b46bc9) [stable]`

Why this matters, measured rather than asserted:

1. **Cursor's own documentation names the binary `agent`** — install `curl https://cursor.com/install -fsS | bash`, verify `agent --version`, installed into `~/.local/bin`. Source: <https://cursor.com/docs/cli/installation>.
2. Cursor is **not installed** on this host, yet `agent --version` **succeeds** and prints a version. Cursor's documented verification step therefore returns a **false positive naming a different vendor**.
3. Installing Cursor correctly would **not** fix it. PATH order is `C:\Users\1028120\.grok\bin` at index **19** and `C:\Users\1028120\.local\bin` at index **28**, so a Cursor binary landing in `~/.local/bin\agent` stays **shadowed by Grok** until PATH is reordered.

### Fleet rule

> Only unambiguous names — `cursor-agent`, `grok` — are ever pinned. The bare name **`agent` is poisoned and never appears in contracts, docs, or the registry.**

`cursor-agent` is safe to pin precisely because it resolves to nothing today: it cannot be silently captured. `agent` cannot be pinned at all, because on this host it already belongs to xAI.

## 3. Registry findings (read-only; presence only, no role opinions)

- **Stale liveness claim — `xai`.** `cli: null` with an inline *"Re-verified 2026-08-23: `grok` is not on PATH"*. Grok is on PATH now, authenticated, and self-updated mid-probe. Configured-as-absent, measured-as-live.
- **Stale liveness claim — `google`.** The row asserts *"The CLI is live on this surface and was verified rather than assumed"*. The **version** half still holds (`0.56.0`); the **liveness** half does not — the account tier is refused by the server.
- **Unregistered live provider — Antigravity/`agy`.** Live, authenticated, PATH index 18 (ahead of every other provider dir), and entirely absent from the registry.
- **No `cursor` row.** Absent from the registry and absent from disk — internally consistent, but the `agent` collision above is recorded nowhere.
- **`deepseek` row accurate.** `cli: null` is correct; no official vendor CLI exists.
- Model row `gemini-3.7-flash` is registered with a refused fan-out verdict. The same id family is now served through `agy` (`gemini-3.7-flash-{high,medium,low}`) — i.e. reachable via a CLI other than the one the refusal was measured through. **Stated as presence only; the R3 gate owns roles.**

## 4. Honest limits

- **Grok auth is weaker evidence than the others.** `grok models` echoes a locally-present `XAI_API_KEY` and printed a static default; it is **not** proven to be a server round-trip, so the key's validity is unverified. `agy models` and `codex login status` did contact their servers.
- **Grok self-updated during the probe.** First `grok --version` read `[alpha]`; the binary rewrote itself (mtime 11:58, `version.json` 11:59) and both names now read `[stable]`. Same build id `5115b46bc9` throughout. Recorded because the first reading is in this transcript and does not match a re-run.
- **Gemini's probe consumed a request.** No status command exists, so liveness could only be measured by attempting one minimal headless call. It failed at authentication, before any model work.
- **No content was dumped** from any credential file; config roots are reported as existence + last-modified only.
- `copilot` (`@github/copilot@1.0.79`) is also on PATH with a `~/.copilot` config root. Outside the six; not probed.
