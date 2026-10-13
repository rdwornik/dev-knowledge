# ADR-123 step 0 -- probe receipts P-1, P-2, P-3 for N=1 `corp-monorepo` (read-only in the consumer)

- **Date:** 2026-10-13 · **Lane:** `lane-bw-670-harness-probes` (batch BW wave D, D6) · **Row:** `[#670]` nearest
- **Decision served:** `docs/decisions/ADR-123-the-harness-ships-as-one-versioned-artefact-pinned-in-each-consumer.md` §Migration step 0 ("Probes before build")
- **Driver:** `scripts/harness_probes.py remote` (run inside the codespace), checked by `scripts/harness_probes.py check <this file>`
- **Package under test:** the stand-in `tests/fixtures/harness-probe-pkg/` (`dk-harness-probe` 0.0.1), not the harness -- `packages/harness/` does not exist yet (ADR-123 step 1 carves it)

## Verdict

**P-1 PASS · P-2 PASS · P-3 PASS.** No probe FAILed, so no ADR-123 §Flip-condition route fires: O9 (one uv package
carrying all three surfaces) stands as proposed going into step 1. The receipts are the fenced JSON block below; they
are run 3, the run of record.

## How it ran

- **Codespace (run of record):** `harness-probes-670-r3-pgw54jqwxv527q6g`, repo `rdwornik/corp-monorepo` @ `main` (HEAD
  `cf282130ba23d9becabdba85512f970f0b6fe5e5`), machine `basicLinux32gb`, created 2026-10-13T11:32:45Z, deleted
  2026-10-13T11:35:03Z (2.3 metered minutes; `logs/CODESPACE-RECEIPTS.jsonl`). Image: the GitHub default
  (corp-monorepo has no `.devcontainer/`), Ubuntu glibc 2.39, CPython 3.14.2.
- **Setup (stands in for a `postCreateCommand`, which corp-monorepo does not declare):** uv pinned to
  `uv 0.11.19 (x86_64-unknown-linux-gnu)` via `curl -LsSf https://astral.sh/uv/0.11.19/install.sh | sh`; Claude Code
  `2.1.296 (Claude Code)` via `npm install -g @anthropic-ai/claude-code`. Claude authenticated with the user-level
  Codespaces secret `CLAUDE_CODE_OAUTH_TOKEN`, already scoped to `rdwornik/corp-monorepo` -- no credential was added
  or changed, and no billing or scope wall was hit.
- **Driver command:** `uv run --no-project --with click python /tmp/harness_probes.py remote --ref cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43 --codespace harness-probes-670-r3-pgw54jqwxv527q6g --out /tmp/harness-probe-receipts.json` -> exit 0.
- **Spec installed:** `dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43#subdirectory=tests/fixtures/harness-probe-pkg`
- **Earlier runs, superseded (all three probes PASSed in each):** run 1 `harness-probes-670-9q5gr745v6wfprgx`
  (11:03:43Z-11:08:04Z, 4.35 min, driver `13ef3d98`) -- its P-3 excerpt kept only the tail of the stream-json log and
  lost the hub refusal line (fixed in `c85ff2c2`); run 2 `harness-probes-670-r2-7r5j6v45q9jfpqpq` (11:15:51Z-11:19:16Z,
  3.42 min, driver `c85ff2c2`) -- Codex review r1 then showed three verdict functions could pass vacuously (fixed in
  `cdefe7e7`, RED-first). Run 3 re-measured everything under the strict verdicts.

## What each probe proves, and what it does not

- **P-1** -- the plugin's three files are written by `dk-harness-probe install` from **package data** of the installed
  wheel into a one-plugin marketplace, installed with `claude plugin install ... --scope project` (which writes
  `enabledPlugins` into the scratch project's `.claude/settings.json` -- the ADR's "project `.claude/`" route), and a
  headless `claude -p` run lists it in `init.plugins` while its `SessionStart`, `UserPromptSubmit` and `Stop` hooks
  each fire once (witness file, one session id). **Not proved:** the `CLAUDE_CODE_PLUGIN_SEED_DIR` route (not
  exercised); the marketplace registration itself is user-scoped (`claude plugin marketplace add`). **Finding:** a plugin
  `SessionStart` hook DID fire on CLI 2.1.296, contrary to the 2026-06-02 note in `plugins/tier1-lifecycle/hooks/hooks.json`.
- **P-2** -- `uv add --no-sync` of the git-URL + `#subdirectory=` spec, run in a **copy** of the consumer checkout under
  `/tmp/p2-corp` (`.git`, `.venv`, `.worktrees` excluded), resolved the consumer's whole dependency set plus the stand-in
  (105 packages, exit 0) under uv 0.11.19; the verdict parses `uv.lock` and requires the package's `source.git` to be the
  hub URL with `subdirectory=tests/fixtures/harness-probe-pkg` at exactly the requested commit. **Not proved:** a resolve
  of the real `dk-harness` (it does not exist) or of a tag ref; the hub repository is public, so no private-repo git
  credential was exercised.
- **P-3** -- after the codespace finished configuring (`creation.log`: "Finished configuring codespace"
  11:34:22.745Z; the P-1 receipt is stamped 11:34:23Z and P-3 runs after it), the hub was made unreachable at the git
  transport (`url.https://hub-unreachable.invalid/rdwornik/dev-knowledge.insteadOf`), the driver proved it (`git
  ls-remote` exit 128 naming the sentinel host), and a headless lane (`claude -p --allowedTools Bash`) issued a Bash
  tool call of `uv run --locked dk-harness-probe check` whose own tool_result is `dk-harness-probe check ok
  version=0.0.1`, with the plugin's three hooks firing. **Not proved:** unreachability of the hub over the GitHub HTTPS
  API (only the git transport to the hub URL was cut; github.com stayed reachable otherwise), and a lane that commits or
  merges -- that is step 2's exit (3/3 merged), not step 0's.

## Read-only in the consumer

- **Local checkout** `C:/Users/1028120/Documents/Dev/corp-monorepo`: before (2026-10-13T11:03:13Z, ahead of run 1)
  HEAD `37b8aa15a8f62198d81dd6f2efa1ce7900275e94`, `git status --porcelain` empty; after (2026-10-13T11:35:31Z, all
  three codespaces deleted) HEAD `37b8aa15a8f62198d81dd6f2efa1ce7900275e94`, `git status --porcelain` empty. No change.
- **Codespace checkout** `/workspaces/corp-monorepo`: HEAD `cf282130ba23d9becabdba85512f970f0b6fe5e5` before and after; porcelain
  before `?? poetry.lock`, after `?? poetry.lock`. The untracked `poetry.lock` is **not this lane's**: in run 3 its mtime is
  11:33:41.88Z, inside the codespace's own "Running oryx..." step (GitHub's default-image auto-build, started
  11:32:51.585Z), before the driver's first measurement; run 2 showed the same file appearing (mtime 11:16:58Z) inside
  its oryx window. The driver writes only under `/tmp` and `~/.claude`. Nothing was committed or pushed to
  `corp-monorepo` from any codespace, and all three codespaces are deleted (`gh codespace list` -> `[]` at 11:35:03Z).

## Receipts (run of record)

```json
[
  {
    "probe": "P-2",
    "command": "cd /tmp/p2-corp (copy of /workspaces/corp-monorepo) && uv add --no-sync 'dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43#subdirectory=tests/fixtures/harness-probe-pkg'",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "Using CPython 3.14.2 interpreter at: /home/codespace/.python/current/bin/python3\n   Updating https://github.com/rdwornik/dev-knowledge (cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43)\n    Updated https://github.com/rdwornik/dev-knowledge (cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43)\nResolved 105 packages in 25.17s",
      "codespace": "harness-probes-670-r3-pgw54jqwxv527q6g",
      "timestamp": "2026-10-13T11:34:15+00:00",
      "uv_lock_lines": [
        "    { name = \"dk-harness-probe\" },",
        "    { name = \"dk-harness-probe\", git = \"https://github.com/rdwornik/dev-knowledge?subdirectory=tests%2Ffixtures%2Fharness-probe-pkg&rev=cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43\" },",
        "name = \"dk-harness-probe\"",
        "source = { git = \"https://github.com/rdwornik/dev-knowledge?subdirectory=tests%2Ffixtures%2Fharness-probe-pkg&rev=cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43#cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43\" }"
      ],
      "uv_version": "uv 0.11.19 (x86_64-unknown-linux-gnu)"
    },
    "verdict": "PASS",
    "blocker": null,
    "flip_route": null
  },
  {
    "probe": "P-1",
    "command": "uv init --bare --name harness-consumer-probe && uv add 'dk-harness-probe @ git+https://github.com/rdwornik/dev-knowledge@cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43#subdirectory=tests/fixtures/harness-probe-pkg' && uv run --locked dk-harness-probe install /tmp/harness-consumer/.harness/marketplace && claude plugin marketplace add /tmp/harness-consumer/.harness/marketplace && claude plugin install dk-harness-probe@dk-harness-probe-local --scope project && HARNESS_PROBE_WITNESS=/tmp/harness-probe-witness.jsonl claude -p 'Reply with the single word OK.' --output-format stream-json --verbose --max-turns 1",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "init.plugins=['dk-harness-probe', 'cc-plugin-agents-md', 'cc-plugin-telemetry', 'cc-plugin-plugin-authoring']\nresult='OK' is_error=False num_turns=1\nwitness={\"event\": \"SessionStart\", \"session_id\": \"f3df1b16-b098-45fd-945f-28e2cd2eeba6\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:34:20.461089+00:00\"}\n{\"event\": \"UserPromptSubmit\", \"session_id\": \"f3df1b16-b098-45fd-945f-28e2cd2eeba6\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:34:20.807985+00:00\"}\n{\"event\": \"Stop\", \"session_id\": \"f3df1b16-b098-45fd-945f-28e2cd2eeba6\", \"source\": \"plugin\", \"ts\": \"2026-10-13T11:34:22.350478+00:00\"}\nproject .claude/settings.json={\n  \"enabledPlugins\": {\n    \"dk-harness-probe@dk-harness-probe-local\": true\n  }\n}\nsetup tail: che and target directories are on different filesystems, hardlinking may not be supported.\n         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.\nInstalled 1 package in 2ms\n + dk-harness-probe==0.0.1 (from git+https://github.com/rdwornik/dev-knowledge@cdefe7e7ea46bc76db1c3b3e95cc12623d02ce43#subdirectory=tests/fixtures/harness-probe-pkg)",
      "codespace": "harness-probes-670-r3-pgw54jqwxv527q6g",
      "timestamp": "2026-10-13T11:34:23+00:00",
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
    "command": "(1) git config --global url.https://hub-unreachable.invalid/rdwornik/dev-knowledge.insteadOf https://github.com/rdwornik/dev-knowledge  (2) GIT_TERMINAL_PROMPT=0 timeout 60 git ls-remote https://github.com/rdwornik/dev-knowledge HEAD  (3) HARNESS_PROBE_WITNESS=/tmp/harness-probe-witness.jsonl claude -p 'Run the shell command `uv run --locked dk-harness-probe check` in the current directory and reply with its output verbatim.' --output-format stream-json --verbose --max-turns 4 --allowedTools Bash",
    "exit_code": 0,
    "evidence": {
      "log_excerpt": "[(1) exit 0] \n[(2) hub probe exit 128, expected nonzero] fatal: unable to access 'https://hub-unreachable.invalid/rdwornik/dev-knowledge/': Could not resolve host: hub-unreachable.invalid\n[(3) lane exit 0] organ tool_result seen=True\ninit.plugins=['dk-harness-probe', 'cc-plugin-agents-md', 'cc-plugin-telemetry', 'cc-plugin-plugin-authoring']\nresult='dk-harness-probe check ok version=0.0.1' is_error=False num_turns=2\nwitness=['SessionStart', 'UserPromptSubmit', 'Stop']",
      "codespace": "harness-probes-670-r3-pgw54jqwxv527q6g",
      "timestamp": "2026-10-13T11:34:31+00:00",
      "block_exit": 0,
      "hub_probe_exit": 128,
      "lane_exit": 0,
      "organ_tool_result_seen": true,
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
