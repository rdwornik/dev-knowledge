# Codespace admission report — independent witness for [#632]

**Lane:** `[#632]` · **Date:** 2026-09-01 · **Substrate:** GitHub Codespace devcontainer,
dispatched via `dispatch-run.sh` running `claude -p "Read
/workspaces/dev-knowledge/LANE-632-codespace-admission-report.md and execute it exactly."
--permission-mode bypassPermissions --output-format stream-json --verbose`.

This report measures the container by hand, from inside a running lane, as an independent
check against `dispatch-run.sh`'s own STEP 0 admission self-test (lines 42–107 of that script).
It runs no suite and changes no behaviour beyond writing this file.

## Admission table

| Tool | Present | Version | Evidence |
|---|---|---|---|
| `claude` | yes | 2.1.252 | `command -v claude` → `/home/vscode/.local/bin/claude`; `claude --version` → `2.1.252 (Claude Code)` |
| `uv` | yes | 0.11.19, **matches ADR-106 pin** | `command -v uv` → `/usr/bin/uv`; `uv --version` → `uv 0.11.19 (x86_64-unknown-linux-musl)`; `pyproject.toml:25` → `required-version = "==0.11.19"` — exact match |
| `python3` | yes | 3.12.11 | `command -v python3` → `/usr/local/bin/python3`; `python3 --version` → `Python 3.12.11` |
| `gh` | **no** | n/a | `gh auth status` → `/bin/bash: line 30: gh: command not found`. Consistent with `dispatch-run.sh`'s own comment (line 54 area): this devcontainer class has no `gh` at all, and the script's admission gate does not require one — it gates on `git ls-remote` reachability instead |
| git remote reachability | yes | n/a | `git fetch origin main` succeeded (returned `FETCH_HEAD`, no error) |

## Login-shell PATH

```
/home/vscode/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/share/nvm/current/bin:/usr/local/bin:/home/vscode/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/share/nvm/current/bin:/usr/local/bin:/home/vscode/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/share/nvm/current/bin:/usr/local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/share/nvm/current/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Note the visible defect in this evidence, reported as captured rather than cleaned up: the
same four directories (`/home/vscode/.local/bin`, `/usr/local/python/current/bin`,
`/usr/local/py-utils/bin`, `/usr/local/jupyter`, `/usr/local/share/nvm/current/bin`,
`/usr/local/bin`) are duplicated four times in a row before the tail resolves normally. This
does not change which binaries resolve (first match wins and it's the same path each time),
but it means whatever sources this login shell's profile is being re-sourced repeatedly
per login rather than being additive-idempotent.

## Token env — names only, never values

```
GITHUB_TOKEN
```

`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`, and `GH_TOKEN` are
**unset** in this shell's environment. Only `GITHUB_TOKEN` is set. This matches the L2 caveat
recorded in `docs/audits/2026-09-01-verification-codespace-longrun-proof.md`: the dispatched
`claude` process is plainly authenticated (it has been calling tools this whole run) via
some channel other than a locally-visible `CLAUDE_CODE_OAUTH_TOKEN`/`ANTHROPIC_*` variable —
most likely the messaging-socket channel that prior audit also observed, not a value this
report is positioned to see or would print if it could.

## Git heads (after `git fetch origin main`)

```
HEAD:        a1da45511c39e5130c0f0085dd4ed26df3f4991d
origin/main: a1da45511c39e5130c0f0085dd4ed26df3f4991d
```

Identical — this checkout is exactly at `origin/main`, no divergence.

## ADMISSION: GREEN

Every gating condition `dispatch-run.sh`'s STEP 0 checks (`adm_uv`, `adm_py`, `adm_remote`,
`adm_token`) is satisfied: `uv` and `python3` resolve on the login PATH, `git ls-remote`-class
reachability is confirmed via `git fetch`, and at least one token (`GITHUB_TOKEN`) is named in
the environment. `gh` is absent but, per the script's own documented reasoning, this is
measured and non-gating rather than a defect.

## Honest limit

This snapshot proves the container's tools and reachability were correct **at the moment this
lane ran** — it does not prove they were correct at container start (the PROVISION RACE the
dispatch script itself guards against with the bounded stamp-poll), and it does not prove
they will still be correct for the *next* lane dispatched into the same or a sibling
container. It is a point-in-time cross-check of one instance of the self-test, not a
standing guarantee, and it cannot see or vouch for the value behind any of the token names
it reports.
