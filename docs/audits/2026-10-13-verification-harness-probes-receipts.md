# ADR-123 step 0 -- probe receipts P-1, P-2, P-3 for N=1 `corp-monorepo` (read-only in the consumer)

- **Date:** 2026-10-13 · **Lane:** `lane-bw-670-harness-probes` (batch BW wave D, D6) · **Row:** `[#670]` nearest
- **Decision served:** `docs/decisions/ADR-123-the-harness-ships-as-one-versioned-artefact-pinned-in-each-consumer.md` §Migration step 0 ("Probes before build")
- **Driver:** `scripts/harness_probes.py remote` (run inside the codespace), checked by `scripts/harness_probes.py check <this file>`
- **Package under test:** the stand-in `tests/fixtures/harness-probe-pkg/` (`dk-harness-probe` 0.0.1), not the harness -- `packages/harness/` does not exist yet (ADR-123 step 1 carves it)

## Verdict

**P-1 PASS · P-2 PASS · P-3 PASS.** No probe FAILed, so no ADR-123 §Flip-condition route fires: O9 (one uv package
carrying all three surfaces) stands as proposed going into step 1. The receipts are the fenced JSON block below; it is
the run of record (run 2).

## How it ran

- **Codespace (run of record):** `harness-probes-670-r2-7r5j6v45q9jfpqpq`, repo `rdwornik/corp-monorepo` @ `main`,
  machine `basicLinux32gb`, created 2026-10-13T11:15:51Z, deleted 2026-10-13T11:19:16Z (3.42 metered minutes;
  `logs/CODESPACE-RECEIPTS.jsonl`). Image: the GitHub default (corp-monorepo has no `.devcontainer/`), Ubuntu glibc
  2.39, CPython 3.14.2.
- **Setup (stands in for a `postCreateCommand`, which corp-monorepo does not declare):** uv pinned to
  `uv 0.11.19 (x86_64-unknown-linux-gnu)` via `curl -LsSf https://astral.sh/uv/0.11.19/install.sh | sh`; Claude Code
  `2.1.296 (Claude Code)` via `npm install -g @anthropic-ai/claude-code`. Claude authenticated with the user-level
  Codespaces secret `CLAUDE_CODE_OAUTH_TOKEN`, already scoped to `rdwornik/corp-monorepo` -- no credential was added.
- **Driver command:** `uv run --no-project --with click python /tmp/harness_probes.py remote --ref c85ff2c249d72538bb0fefd7cd0b8d083741a22e --codespace harness-probes-670-r2-7r5j6v45q9jfpqpq --out /tmp/harness-probe-receipts.json` -> exit 0.
- **Spec installed:** `dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@c85ff2c249d72538bb0fefd7cd0b8d083741a22e#subdirectory=tests/fixtures/harness-probe-pkg`
- **Run 1** (`harness-probes-670-9q5gr745v6wfprgx`, created 11:03:43Z, deleted 11:08:04Z, 4.35 min, driver @ `13ef3d98`)
  also passed all three; it is superseded because its P-3 excerpt kept only the tail of a long stream-json log and so
  lost the hub refusal line (fixed in `c85ff2c2`, with a RED-first test). Between the runs, a by-hand variant on run 1
  showed the plugin also loads when installed at `--scope project` -- the route run 2 then used as P-1's primary.

## What each probe proves, and what it does not

- **P-1** -- the plugin's three files are written by `dk-harness-probe install` from **package data** of the installed
  wheel into a one-plugin marketplace, installed with `claude plugin install ... --scope project` (which writes
  `enabledPlugins` into the scratch project's `.claude/settings.json` -- the ADR's "project `.claude/`" route), and a
  headless `claude -p` run lists it in `init.plugins` while its `SessionStart`, `UserPromptSubmit` and `Stop` hooks
  each fire once (witness file, one session id). **Not proved:** the `CLAUDE_CODE_PLUGIN_SEED_DIR` route (not
  exercised); the marketplace registration is still user-scoped (`claude plugin marketplace add`). **Finding:** a plugin
  `SessionStart` hook DID fire on CLI 2.1.296, contrary to the 2026-06-02 note in `plugins/tier1-lifecycle/hooks/hooks.json`.
- **P-2** -- `uv add --no-sync` of the git-URL + `#subdirectory=` spec, run in a **copy** of the consumer checkout under
  `/tmp/p2-corp` (`.git`, `.venv`, `.worktrees` excluded), resolved the consumer's whole dependency set plus the stand-in
  (105 packages, exit 0) under uv 0.11.19, and `uv.lock` pins `rev=` to the exact commit. **Not proved:** a resolve of
  the real `dk-harness` (it does not exist) or of a tag ref; the hub repository is public, so no private-repo git
  credential was exercised.
- **P-3** -- after the codespace finished configuring (`creation.log`: "Finished configuring codespace" 11:17:33.229Z;
  P-3's receipt is stamped 11:17:43Z), the hub was made unreachable at the git transport
  (`url.https://hub-unreachable.invalid/rdwornik/dev-knowledge.insteadOf`), the driver proved it
  (`git ls-remote` exit 128, "Could not resolve host"), and a headless lane (`claude -p --allowedTools Bash`) ran the
  harness organ `uv run --locked dk-harness-probe check` and returned `dk-harness-probe check ok version=0.0.1`, with
  the plugin's three hooks firing. **Not proved:** unreachability of the hub over the GitHub HTTPS API (only the git
  transport to the hub URL was cut; github.com stayed reachable for everything else), and a lane that commits or
  merges -- that is step 2's exit (3/3 merged), not step 0's.

## Read-only in the consumer

- **Local checkout** `C:/Users/1028120/Documents/Dev/corp-monorepo`: before (2026-10-13T11:03:13Z) HEAD
  `37b8aa15a8f62198d81dd6f2efa1ce7900275e94`, `git status --porcelain` empty; after (after both codespaces were
  deleted) HEAD `37b8aa15a8f62198d81dd6f2efa1ce7900275e94`, `git status --porcelain` empty. No change.
- **Codespace checkout** `/workspaces/corp-monorepo`: HEAD `cf282130ba23d9becabdba85512f970f0b6fe5e5` before and after; porcelain
  before `(empty)`, after `?? poetry.lock`. The
  `poetry.lock` is **not this lane's**: its mtime is 11:16:58.26Z, inside the codespace's own "Running oryx..." step
  (11:15:58Z-11:17:00Z in `creation.log`, GitHub's default-image auto-build), and the driver writes only under `/tmp`.
  Run 1 showed the same untracked `poetry.lock` already at the driver's first measurement. Nothing was committed or
  pushed to `corp-monorepo` from either codespace, and both codespaces are deleted (`gh codespace list` -> `[]`).

## Receipts (run of record)

```json
[
  {
    "probe": "P-2",
    "command": "cd /tmp/p2-corp (copy of /workspaces/corp-monorepo) && uv add --no-sync 'dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@c85ff2c249d72538bb0fefd7cd0b8d083741a22e#subdirectory=tests/fixtures/harness-probe-pkg'",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "Using CPython 3.14.2 interpreter at: /home/codespace/.python/current/bin/python3\n   Updating https://github.com/rdwornik/dev-knowledge (c85ff2c249d72538bb0fefd7cd0b8d083741a22e)\n    Updated https://github.com/rdwornik/dev-knowledge (c85ff2c249d72538bb0fefd7cd0b8d083741a22e)\nResolved 105 packages in 24.23s",
      "codespace": "harness-probes-670-r2-7r5j6v45q9jfpqpq",
      "timestamp": "2026-10-13T11:17:22+00:00",
      "uv_lock_lines": [
        "    { name = \"dk-harness-probe\" },",
        "    { name = \"dk-harness-probe\", git = \"https://github.com/rdwornik/dev-knowledge?subdirectory=tests%2Ffixtures%2Fharness-probe-pkg&rev=c85ff2c249d72538bb0fefd7cd0b8d083741a22e\" },",
        "name = \"dk-harness-probe\"",
        "source = { git = \"https://github.com/rdwornik/dev-knowledge?subdirectory=tests%2Ffixtures%2Fharness-probe-pkg&rev=c85ff2c249d72538bb0fefd7cd0b8d083741a22e#c85ff2c249d72538bb0fefd7cd0b8d083741a22e\" }"
      ],
      "uv_version": "uv 0.11.19 (x86_64-unknown-linux-gnu)"
    },
    "verdict": "PASS",
    "blocker": null,
    "flip_route": null
  },
  {
    "probe": "P-1",
    "command": "uv init --bare --name harness-consumer-probe && uv add 'dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@c85ff2c249d72538bb0fefd7cd0b8d083741a22e#subdirectory=tests/fixtures/harness-probe-pkg' && uv run --locked dk-harness-probe install /tmp/harness-consumer/.harness/marketplace && claude plugin marketplace add /tmp/harness-consumer/.harness/marketplace && claude plugin install dk-harness-probe@dk-harness-probe-local --scope project && HARNESS_PROBE_WITNESS=/tmp/harness-probe-witness.jsonl claude -p 'Reply with the single word OK.' --output-format stream-json --verbose --max-turns 1",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "init.plugins=['dk-harness-probe', 'cc-plugin-agents-md', 'cc-plugin-telemetry', 'cc-plugin-plugin-authoring']\nresult='OK' is_error=False num_turns=1\nwitness={\"event\": \"SessionStart\", \"session_id\": \"7b378e4a-3c28-4027-b308-b7c711e4033b\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:17:31.932675+00:00\"}\n{\"event\": \"UserPromptSubmit\", \"session_id\": \"7b378e4a-3c28-4027-b308-b7c711e4033b\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:17:32.314682+00:00\"}\n{\"event\": \"Stop\", \"session_id\": \"7b378e4a-3c28-4027-b308-b7c711e4033b\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:17:33.853898+00:00\"}\nproject .claude/settings.json={\n  \"enabledPlugins\": {\n    \"dk-harness-probe@dk-harness-probe-local\": true\n  }\n}\nsetup tail: che and target directories are on different filesystems, hardlinking may not be supported.\n         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.\nInstalled 1 package in 2ms\n + dk-harness-probe==0.0.1 (from git+https://github.com/rdwornik/dev-knowledge@c85ff2c249d72538bb0fefd7cd0b8d083741a22e#subdirectory=tests/fixtures/harness-probe-pkg)",
      "codespace": "harness-probes-670-r2-7r5j6v45q9jfpqpq",
      "timestamp": "2026-10-13T11:17:36+00:00",
      "init_plugins": [
        "dk-harness-probe",
        "cc-plugin-agents-md",
        "cc-plugin-telemetry",
        "cc-plugin-plugin-authoring"
      ],
      "witness_events": [
        "SessionStart",
        "UserPromptSubmit",
        "Stop"
      ]
    },
    "verdict": "PASS",
    "blocker": null,
    "flip_route": null
  },
  {
    "probe": "P-3",
    "command": "git config --global url.https://hub-unreachable.invalid/rdwornik/dev-knowledge.insteadOf https://github.com/rdwornik/dev-knowledge && git ls-remote https://github.com/rdwornik/dev-knowledge HEAD && HARNESS_PROBE_WITNESS=/tmp/harness-probe-witness.jsonl claude -p 'Run the shell command `uv run --locked dk-harness-probe check` in the current directory and reply with its output verbatim.' --output-format stream-json --verbose --max-turns 4 --allowedTools Bash",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "[hub probe exit 128] fatal: unable to access 'https://hub-unreachable.invalid/rdwornik/dev-knowledge/': Could not resolve host: hub-unreachable.invalid\ninit.plugins=['dk-harness-probe', 'cc-plugin-agents-md', 'cc-plugin-telemetry', 'cc-plugin-plugin-authoring']\nresult='dk-harness-probe check ok version=0.0.1' is_error=False num_turns=2\nwitness=['SessionStart', 'UserPromptSubmit', 'Stop']",
      "codespace": "harness-probes-670-r2-7r5j6v45q9jfpqpq",
      "timestamp": "2026-10-13T11:17:43+00:00",
      "hub_probe_exit": 128,
      "witness_events": [
        "SessionStart",
        "UserPromptSubmit",
        "Stop"
      ]
    },
    "verdict": "PASS",
    "blocker": null,
    "flip_route": null
  }
]
```
