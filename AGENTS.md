# AGENTS.md — `.dev-knowledge`

> **Portable instruction layer** (ADR-115, superseding ADR-53 Decision 2). Non-inferable
> facts only: how to build, test and land a change here. Claude-runtime specifics live in
> `CLAUDE.md`, which imports this file — the relation is an **importer, never a symlink**
> (git materialises symlinks as plain text under `core.symlinks=false` on Windows).

## Precedence — resolved BY SCOPE, not by position

> This section is **required by ADR-115 §3.2** ("the `~/.codex` precedence collision is
> resolved BY SCOPE, stated in the file header"). It names provider-specific paths because
> resolving a collision requires naming its parties — it is not portable-layer drift.

Three instruction layers can be in play at once. They are separated by **scope**, so the
question "which wins" has one answer per subject rather than one answer overall:

| Layer | Governs |
|---|---|
| `~/.codex/AGENTS.md` (L0, operator disk) | the **reviewer role** — the model/effort pin a review runs under |
| **this file** (repo root) | **in-repo work** — building, testing and landing changes here |
| `codex/AGENTS.md` (intermediate dir) | its own subtree only |

The third layer is a **known trap**: a cwd at or below `codex/` yields
`role → doctrine → role`, and the role wins **by position rather than by intent**. If you
are working on repo doctrine, run from the repo root.

**Size guard is stated in BYTES, not lines.** Codex's `project_doc_max_bytes` cap is
32 KiB and this corpus averages ~117 B/line, so a line ceiling does not bound what the cap
measures. Copying `CLAUDE.md` wholesale lands at 43.50 KiB — 11.50 KiB over the cap — and
Codex **truncates silently**.

## What this repo is

A governance and methodology hub, not a code project: markdown governance files plus
hub-local validators, generators and gates. It is Layer 2 of a three-layer ecosystem model
and **never executes** — no script here drives state in a child repo. Validators,
generators and gates are in scope; orchestration scripts are not.

Structural map: `ARCHITECTURE.md`. Read it before any structural change.

## Environment

The environment is **declared**, not discovered:

- `pyproject.toml` + `uv.lock` + `.python-version`
- `uv` itself is pinned **exactly** (`required-version = "==0.11.19"`); a uv bump is its own
  gated change, never incidental
- rebuild with `uv sync --locked`

Every command below goes through `uv run --locked`. A bare `python` or `pytest` resolves
nothing on a clean checkout — that is a defect in a doc, not a shorthand.

## Build / test / lint

```bash
uv sync --locked                                   # rebuild the declared environment
uv run --locked pytest -x --tb=short               # the suite
uv run --locked ruff check --fix                   # lint (also a pre-commit gate)
uv run --locked python scripts/audit.py health     # self-conformance gate
```

**Suite cadence.** In a lane, run the **targeted** tests covering that lane's diff. The
**full suite runs once, at integration** — not per lane.

## Landing a change

- **Never commit directly to `main`.** Branch, then merge with `--no-ff`. A pre-commit hook
  refuses a direct non-merge commit on `main`; a pre-push hook refuses a fast-forward onto
  main's first-parent spine.
- **Branch prefixes are a closed enum.** Author-chosen: `feat/ fix/ docs/ chore/`.
  Machine-produced lanes: `worktree-<name>`, `epic/<slug>`, `claude/<slug>`,
  `automation/<slug>`. A new prefix enters the enum only via a recorded ruling.
  Checkable surface: `scripts/validate_branch_naming.py`.
- **Commit types** follow Conventional Commits, plus `refactor` and `test`. Commit types are
  **not** branch prefixes.
- **A commit that adds a backlog id** carries a `kill-candidates:` line (≥1 open `#id`, or
  `none — <reason>`), flush-left. A commit that closes one carries `[#id]`.
- **Parallel work in this repo needs a worktree.** One checkout = one committing session.
  Worktrees live at `.claude/worktrees/<name>` on branch `worktree-<name>`; seed
  `ecosystem/*/state.yaml` from the primary or the first commit is blocked. Remove the
  worktree and verify the removal — a provision→cleanup round-trip leaves the tree identical.

## File rules that will bite you

- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit old entries);
  `JOURNAL.md` is append-only **newest-first**.
- **Immutable:** ADRs, transcripts, handoffs, audits — supersede with a new file or an
  in-file amendment marker. An ADR's *status line* is the one in-place exception.
- **Generated — never hand-edit:** `BACKLOG.md` (edit `tasks/`, then
  `uv run --locked python scripts/gen_task_tree.py --emit-source`), and the generated
  rosters and indices under `.claude/generated/` and `ecosystem/`.
- **Never restate a count or roster in prose** — cite the surface that computes it. A number
  typed into a doc is stale at the next commit.
- **Resolve a locator before acting on it.** A `file:line`, heading, SHA or `[#id]` you have
  not opened is a claim, not evidence.

## Gates

Gates are pre-commit, commit-msg and pre-push hooks plus a self-conformance audit. They are
**not** advisory: a FAIL blocks. Arm them once per clone with

```bash
uv run --locked pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

If a gate fires, fix the cause. Do not reach for `--no-verify`; where a bypass is genuinely
sanctioned it is one named hook, declared in the commit body, and it is the exception.
