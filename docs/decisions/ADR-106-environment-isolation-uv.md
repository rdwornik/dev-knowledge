# ADR-106: Environment isolation via uv — pinned toolchain, locked gate environment, per-repo gated rollout

**Status:** Accepted
**Date:** 2026-07-27
**Decision tier:** Architecture (operator ruling 2026-07-26 — uv adopted fleet-wide in principle; hub execution mandated as arc [#432], 2026-07-27 execution brief)
**Related:** [#432] (the hub adoption arc this ADR is a deliverable of), [#429] (worktree provisioning — distinct concern), [#317] (test-invocation tiering — same surface, orthogonal axis), ADR-101 (Amendment 2026-07-27 sanctions `uv.lock` + `.python-version` as Tier-1 files), #257 (the no-venv policy this SUPERSEDES), methodology-intake commissions A and E (environment isolation, gate reproducibility)

## Context

Until this arc the hub ran its entire enforcement surface — 14 `language: system`
pre-commit hooks, the Stop/SessionStart session hooks, pytest, ruff, the ship gate —
on the **global system Python 3.12 site-packages**: no venv, no lockfile, dependency
floors declared (PEP 735 `[dependency-groups]`) but never resolved to pinned versions
anywhere. That was a deliberate 2026-07-05 decision (#257, recorded in the
`pyproject.toml` header): with every surface invoking the system interpreter, a venv
would have forked interpreter paths for "zero isolation gain."

The trade rotted from two directions: (a) gate verdicts depended on whatever the
machine's global site-packages happened to hold (undeclared `rich`, `click` only in a
side-file `config/requirements-dev.txt`, a global ruff free to drift off the pinned
pre-commit rev) — **environment/test isolation** defect class; (b) a clean checkout
could not reproduce the gate environment from committed state at all —
**gate-reproducibility** defect class. These are methodology-intake commissions A and E,
and they stop being per-repo folklore only when the toolchain itself declares the
environment.

## Decision

1. **uv is the environment/dependency toolchain for `.dev-knowledge`.** The committed
   surface is: `pyproject.toml` (`[project]` + `[tool.uv]` + `[dependency-groups]`),
   `uv.lock` (the full resolved graph), and `.python-version` (interpreter pin,
   CPython **3.12.10**). `uv sync --locked` rebuilds the gate environment from a clean
   checkout with no network-time resolution decisions. The repo stays a **non-package**
   (`[tool.uv] package = false`) — flat-layout governance repo, only dependency groups
   are synced (Layer-2: validators only, nothing installable).

2. **uv itself is pinned EXACTLY: `uv==0.11.19`** via `[tool.uv] required-version ==0.11.19`
   in `pyproject.toml` (the committed pin; any other uv version refuses to operate on the
   project). Rationale: uv is pre-1.0 and ships roughly every three days with behavioural
   drift in point releases — the 2026-07-23 release changed `--locked` semantics (rejects
   non-canonically formatted lockfiles). An unpinned uv re-imports the exact
   reproducibility defect class this adoption removes.

3. **A uv upgrade is its OWN gated change, never an incidental one.** Bumping the pin =
   a dedicated reviewed commit that changes `required-version`, regenerates `uv.lock`
   with the new version, and re-runs the full gate set (pytest count + ship-gate +
   all pre-commit hooks) green before merge. No session upgrades uv mid-arc because a
   tool happened to update; no hook, script, or agent may call a floating uv.

4. **Gate invocation runs through the locked environment.** Migrated this arc to
   `uv run --locked …` (refuse-don't-resync posture: a stale lockfile fails loudly,
   it is never silently re-resolved):
   - all 14 local pre-commit hook entries (`.pre-commit-config.yaml`);
   - the Stop session gate (`session_end_backpressure.py`) and the python SessionStart
     hooks (`fleet_health.py`, `changelog_sentinel.py`, `arm_hooks.py`) in
     `.claude/settings.json` — `arm_hooks` now arms pre-commit from the venv
     (`sys.executable`), so the git-hook shims themselves bind to the locked env;
   - the `verify` skill cadence (`uv run --locked pytest -x --tb=short`,
     `uv run --locked ruff check`);
   - `CONTRIBUTING.md` setup (`uv sync --locked` + `uv run pre-commit install`
     replaces `pip install -r config/requirements-dev.txt`).
   Scripts that spawn Python re-invoke `sys.executable`, so subprocess trees inherit
   the venv interpreter without further changes.

5. **Deliberate exceptions (recorded, not oversights):**
   - the **ADR-77 PreToolUse immutability guard** (`block_immutable_edits.py`) stays on
     the bare system interpreter: it is stdlib-only and fail-closed, and a stale
     lockfile must never be able to block every Edit/Write call in a session
     (self-DoS). It gains nothing from the venv (zero third-party imports).
   - the **tier1-lifecycle plugin** hook (`propose_closures.py`) and plugin command
     docs keep bare `python`: the plugin is fleet-distributed from the hub marketplace;
     migrating it is a consumer-facing change that belongs to the per-repo rollout
     (point 7), not the hub arc.
   - **hub-methodology prose surfaces** (PLAYBOOK, ESSENTIALS, hub-owned CLAUDE.md
     regions, templates, generator stderr hints) keep their `python …` invocation
     wording this arc: rewording them is de-facto fleet rollout via the methodology
     layer and is executed with it. The commands remain functional (and runnable as
     `uv run python …`) meanwhile.
   - `config/requirements-dev.txt` is superseded but **retained** (deletion needs an
     explicit operator ask — no-delete invariant); retire-candidate for the rollout.

6. **Defect classes this closes (hub scope):** environment/test isolation — gate and
   test verdicts bind to a committed, resolved dependency graph and a pinned
   interpreter, not to global site-packages state; gate reproducibility — a clean
   checkout reaches the identical gate environment via `uv sync --locked`
   (verified this arc: same pytest collection count 1763, ship-gate GREEN, all 15
   pre-commit hooks passing, from a from-scratch `.venv`).

7. **Fleet rollout shape: per-repo GATED adoption, never a bulk sweep.** This ADR
   defines the shape; each consumer (corp-monorepo, ai-council, …) adopts in its own
   gated arc: own pyproject/lock, own exact-uv pin (same version unless its arc rules
   otherwise), own gate-parity proof (its full gate set green under `uv run` before
   merge), landed per that repo's review discipline. The hub deploy/manifest carriers
   are NOT extended by this ADR — a uv carrier/component, if ever wanted, is a
   separate manifest decision.

8. **The ai-council `conftest.py` import guard remains as a SECOND leg, not the only
   one.** Its in-process guard (blocking cross-env imports at test time) stays armed
   after ai-council's uv adoption: uv isolates the environment a process starts in;
   the conftest guard polices what the test process does inside it. Belt and braces —
   neither substitutes for the other.

## Consequences

- Every gate invocation now carries a small uv resolution check (~tens of ms warm);
  first invocation on a fresh clone/worktree materialises `.venv` (seconds from a warm
  cache). Worktrees get their own `.venv` on first hook fire; `.venv/` is gitignored
  and dies with the worktree (no-leftovers rule unaffected).
- A stale `uv.lock` (pyproject edited without re-lock) blocks commits loudly at the
  first hook — intended backpressure, same family as the roster-freshness gates. Fix:
  `uv lock` (a reviewed change), never `--no-verify`.
- The venv ruff is pinned **exactly** to the pre-commit rev (`ruff==0.15.5` in the dev
  group) so manual `uv run ruff check` and the hook render one verdict (kills the
  venv-vs-hook version-mismatch gotcha class).
- `pytest` resolved to 9.1.1 in the lock (floor `>=9.0` unchanged); the fleet pytest
  floor declaration in `[tool.pytest.ini_options]` is untouched.
- ADR-101's sanctioned Tier-1 file set grew by amendment (2026-07-27) to admit
  `uv.lock` + `.python-version` — the closed-set discipline held (the gate refused the
  add until the amendment landed in lockstep).
