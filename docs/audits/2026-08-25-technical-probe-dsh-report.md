# PROBE-DSH — DeepSeek Harness probe report

- **Date:** 2026-08-25 (probe ran 11:29–12:16 local)
- **Machine:** Windows 11 Enterprise 10.0.26200, `C:\Users\1028120`
- **Shape:** interactive · local · outside the repo · zero repo writes
- **Scope note:** R3 measures, this report states. No role-admission opinion is offered.

---

## Step 1 — versions and launch — **DID NOT COMPLETE**

Toolchain (measured):
- `node --version` = **v25.2.1**
- `npm --version` = **11.18.0**
- `npx --version` = **11.18.0**

Package (from the npm registry, `npm view`):
- **`@deepseek-ai/dsh@0.1.1-rc.2`** — MIT; `dist-tags` latest **and** next both `0.1.1-rc.2`
- published **4 days before this probe**, by `imccyu`; maintainers `imccyu`, `tianyicui-deepseek`
- `bin` = `dsh` → `lib/bin.js`; unpacked size 120.0 kB; **62 direct deps** (registry printed 24, "…and 38 more")
- **no `engines` field** — the package declares no Node floor
- 10 published versions, all `-rc`

Launch attempt — **failed to complete; no error to quote**:
- exact command: `npx -y @deepseek-ai/dsh@latest --version`
- ran **46 minutes wall**, **2688 s CPU** (~100% of one core, sustained)
- RSS climbed 1.59 GB → 3.41 GB, then plateaued ~3.37 GB for the final ~10 min
- **zero bytes** of stdout or stderr for the entire run
- `node_modules` **never materialized** in the npx cache dir
- a CPU-delta probe (19.2 s CPU per 20 s wall) proved it was **compute-bound, not deadlocked** — a livelock in npm's dependency-tree resolution, not a hang on I/O or on a lock
- terminated deliberately at 12:15:43 to stop it contending for the workstation

**There is no verbatim error message, because none was ever emitted.** The failure mode is
non-termination, not a non-zero exit.

**Consequence, stated plainly:** `npx @deepseek-ai/dsh web` was **never launched**, and **no dsh
process was ever observed running**. Everything in steps 2–4 below is read from the **published
tarballs** (fetched with `npm pack`, extracted outside the repo) plus the official docs — not from
observed runtime behaviour. Citations are `file:line` inside each package's shipped `lib/`.

---

## Step 2 — config / state path — **answered from shipped source**

- **`$DSH_HOME` if set, else `join(homedir(), ".dsh")`** → on this machine **`C:\Users\1028120\.dsh`**
  - `@deepseek-ai/dsh-home-paths` `lib/index.js:11` (`DSH_HOME_DIR_NAME = ".dsh"`), `:15`, `:50`, `:73-74`
  - an empty or whitespace-only `$DSH_HOME` is treated as unset
- `$DSH_HOME` is **currently unset** on this machine.
- Files under that root (**from docs — not observed**, since dsh never ran):
  `.credentials.yaml`, `settings.yaml`, `AGENTS.md`, `.sessions/` (JSONL session logs),
  `profiles/<name>/{package.json, cordis.patch.yml}`, and a home-level `cordis.patch.yml`
- Related root: `$DSH_AGENTS_HOME`, default `~/.agents` (also unset here)

**`~/.dsh` was NOT created by this probe.** A before/after listing of every dotfolder in
`%USERPROFILE%` is **byte-identical** (55 entries, `diff` clean) — dsh never executed.

---

## Step 3 — AGENTS.md consumption — **YES, and `CLAUDE.md` as well**

Determined by reading `@deepseek-ai/dsh-agent-instructions@0.1.1-rc.2`. **No experiment was run,
and DSH was never pointed at any folder** — the shipped source is decisive, which is stronger
evidence than a throwaway-folder trial would have been.

- base candidates: **`["AGENTS.md", "CLAUDE.md"]`** — `lib/index.js:16`
- local overlays: **`["AGENTS.local.md", "CLAUDE.local.md"]`** — `:17`
- project-root marker: **`[".git"]`** — `:15`
- load order — `:571`, and the package README:
  1. `$DSH_HOME/AGENTS.md` (user-global, **fixed name, no overlay**) — `:140`
  2. then, for **each directory from the project root down to the session cwd**, every existing
     base candidate, then every existing local overlay
- **de-duplication:** within one directory, candidates whose content is byte-identical after
  trimming leading/trailing whitespace collapse to the earliest candidate in configured order — so
  a `CLAUDE.md` that merely duplicates its sibling `AGENTS.md` is rendered once
- **byte budget:** the shipped `standard` preset sets `maxBytes: 65536`. It is a **batch** budget;
  over-budget files are truncated or omitted, and the prompt carries an explicit marker
  (`omitted <paths>` / `truncated <path> from N to M bytes`)
- **presets that mount the loader:** `code`, `cordis`, `standard` — **not** `minimal`
- the loader also **re-scans after successful `read`/`write`/`edit` tool calls**, queueing
  additions / replacements / removals as files appear or change mid-session
- instructions are injected as durable user-role messages inside a `<system-reminder>` block
- both candidate lists are configurable (`instructionFileCandidates`,
  `localInstructionFileCandidates`), as is `projectRootMarkers`

**Bearing on this ecosystem:** a repo carrying only `CLAUDE.md` and no `AGENTS.md` is still fully
consumed, from the `.git` root downward.

---

## Step 4 — auth / model requirements — **no key was entered**

- API key env var: **`DEEPSEEK_API_KEY`** — `@deepseek-ai/dsh-llm-deepseek` `lib/index.js:1589`,
  with `:1625` (`apiKeyEnv` defaults to it; each route may override the variable name)
- resolution order (**docs**): inherited environment → `$DSH_HOME/.credentials.yaml` →
  the invoking directory's `.env` → `$DSH_HOME/.env`
- an absent key raises **`MISSING_CREDENTIAL`**; the web **Settings → Models** page writes the key
- endpoint: **`https://api.deepseek.com`** (`:1651`), overridable via **`DEEPSEEK_BASE_URL`** (`:1653`)
- advertised model routes: **`deepseek-v4-flash`**, **`deepseek-v4-pro`**,
  **`deepseek-v4-flash-vision-exp`** (`:1594`, `:1599`, `:1604`)
- other providers and custom OpenAI-compatible endpoints are supported per the docs

**No credential was entered at any point.** Worth flagging, though: **`DEEPSEEK_API_KEY` is already
SET in this machine's environment** (pre-existing, presumably via the `keys` profile loader — its
value was neither read nor printed). Because the resolver consults the **inherited environment
first**, a `dsh` launched from a normal shell here would authenticate **with no key entry and no
prompt**.

---

## Other measured facts bearing on the R3 gate

- `dsh web` is a **hardcoded alias for `--profile web`**; profiles live at `$DSH_HOME/profiles/<name>`
- web UI default **`http://127.0.0.1:3080`**; flags `--host`, `--port`, `--trusted-host`
  (repeatable), `--no-open`, `--patch`, `--dump-config` (composes config **without booting** —
  the cheapest way to inspect a resolved tree on a retry)
- non-loopback access is refused unless `trustedHosts` is declared
- the **`web` and `headless` profiles auto-initialize from shipped templates**; **any other profile
  must be created through `dsh plugin`, which requires `pnpm`** — and **`pnpm` is ABSENT on this
  machine** (`pnpm: command not found`)
- **"The invoking directory is the default workspace root"** (shipped `README.md`). There is no
  launcher flag to set the project root: it follows cwd, and the instruction loader then walks up
  to the nearest `.git`.

---

## R3-gate readiness — one line

**Not assessable on runtime evidence:** the shipped `npx` path never completed on this machine
(46 min, 2688 s CPU, zero output), so no dsh process was observed; the config path (`~/.dsh`) and
the instruction-file behaviour are answered from shipped source only, and the fact that the loader
consumes **`CLAUDE.md` as well as `AGENTS.md`** from the `.git` root down is the measurement that
bears directly on the workspace-folder decision.

---

## Machine state after the probe

- **`~/.dsh` not created**; `%USERPROFILE%` dotfolder set identical before and after
- **no repo file was read or written.** Disclosure: `git status` / `git log` *were* run in
  `.dev-knowledge`, solely to verify that session-end hook advisories (a dirty tree, and a "hard"
  JOURNAL-anchor demand) referred to a **concurrent session's** commits rather than to this probe.
  They did — `a6698ca6` / `fac96321`, authored 11:56–12:01. Nothing was committed, staged or stashed.
- **one leftover, NOT removed** (deleting it needs your approval):
  `C:\Users\1028120\AppData\Local\npm-cache\_npx\b86ed90107c62dab\concurrency.lock` — an empty lock
  **directory** orphaned when the livelocked npx was killed. It may need clearing before a retry.
- four package tarballs were fetched and extracted under the job's temp dir (removed with the job);
  the npm content cache grew ~55 MB, which is normal cache behaviour.

## If retrying step 1

The livelock is in npm's resolver, not in dsh itself. Worth trying, in order: a **pinned exact
version** instead of `@latest` (`npx -y @deepseek-ai/dsh@0.1.1-rc.2 web`); a global install
(`npm i -g @deepseek-ai/dsh`, then `dsh web`); or `--prefer-offline`, now that much of the tree is
cached. Clear the stale lock directory above first.
