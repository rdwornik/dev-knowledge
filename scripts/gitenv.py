#!/usr/bin/env python
"""gitenv.py — the ONE definition of the subprocess-git environment scrub ([#396]).

WHY THIS EXISTS. An inherited `GIT_DIR` overrides BOTH `cwd=` and `git -C`: a validator run
from a hook (or any nested git invocation) then reads the PARENT's repo while labelling the
answer with the target's id. That bit this fleet live ([#355]), and it is how `gen_handoff`'s
RM-8 open-batch refusal was silently disarmed. Every git call whose answer is *about a
particular repo* must therefore run with the repo-location vars removed.

WHY A LEAF MODULE. Until [#396] this scrub lived in three hand-copied places
(`audit.py`, `fleet_parity.py`, `fleet_analytics.py`) and a fourth git caller
(`batch_manifest._git`) had none at all — the shape where one copy gets a fix and the others
rot. Consolidating was blocked by one real constraint: `audit.py` imports `fleet_parity`
LAZILY (dual script/package mode) and bundle selection must not acquire a dependency on that
import path. So this module is deliberately a **leaf**: stdlib-only, ZERO repo imports, no
package-relative imports, no side effects at import time beyond defining names. Importing it
from anywhere — including `audit.py`'s module top-level — adds no import-path risk, which is
what makes the single source of truth affordable.

WHAT IS SCRUBBED, and what is NOT. Scrubbed BY NAME, never a `startswith("GIT_")` strip — a
blanket strip would also drop `GIT_CONFIG_GLOBAL` / `GIT_AUTHOR_*` / `GIT_SSH_COMMAND`, which
fails quietly. The set is DERIVED from `git rev-parse --local-env-vars`, git's own canonical
list of repository-local vars (and git's documented advice for hooks touching a foreign repo
is to clear exactly these). Deriving rather than hand-listing removes the rot mode: a
hand-maintained tuple silently misses vars a newer git adds — the first hand-written version
of this list omitted 8 of git's 15 (`GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_GRAFT_FILE`,
`GIT_SHALLOW_FILE`, ...), caught in review. `_EXTRA` covers repo-SCOPING vars git does not
class as local-env; `_FALLBACK` applies only when git itself is unavailable.

WHERE IT FIRES is each caller's decision, NOT this module's. `audit.py`'s fleet-automation
commit path sets `GIT_INDEX_FILE` ON PURPOSE through its own explicit `env=` dict; routing
that through this scrub would silently break it. This module says what the scrub set IS; it
never decides which call sites take it.

HOW CONSUMERS LOAD IT: **by PATH, never by name** (terra HIGH x3, 2026-08-08 — every
name-based spelling was tried and every one had a shadow hole, each reproduced live):

  * `import gitenv` loses to a foreign top-level `gitenv.py` on `PYTHONPATH`/site-packages
    whenever `scripts/` is NOT sys.path[0] — which is exactly package-mode
    (`python -m scripts.audit`), where the repo ROOT is on the path instead.
  * `from scripts import gitenv` loses to a foreign package-shaped `scripts/gitenv.py` on
    `PYTHONPATH` in script-mode (`python scripts/audit.py`), where sys.path[0] is
    `scripts/` itself and therefore cannot resolve a top-level `scripts` package at all.
  * Ordering the two only moves the hole; there is no order in which both are covered.

Both holes end identically and SILENTLY: the decoy satisfies the import, the scrub becomes
the EMPTY set, and [#355] is re-opened by the module that exists to close it. Nothing
raises. So consumers resolve this file with `importlib.util.spec_from_file_location` against
`Path(__file__).with_name("gitenv.py")`, which no `sys.path` entry can intercept. That is
affordable ONLY because this module is a leaf: executing it runs nothing else. Each consumer
gets its own module object and therefore its own cache — behaviourally identical (at most
one extra `git rev-parse`), and `tests/test_gitenv.py` asserts the invariant that matters,
which is the defining FILE, never object identity.

The one exception is `fleet_analytics.py`, which puts `scripts/` at `sys.path[0]` itself
before importing and so cannot be shadowed by either decoy shape. Its immunity is asserted
alongside the others rather than assumed.
"""

from __future__ import annotations

import os
import subprocess

# Repo-SCOPING vars git does not class as local-env, so `--local-env-vars` never names them.
GIT_LOCATION_ENV_EXTRA = ("GIT_CEILING_DIRECTORIES", "GIT_NAMESPACE")

# Used ONLY when `git rev-parse --local-env-vars` cannot be run (git absent / errored).
GIT_LOCATION_ENV_FALLBACK = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
    "GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS", "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
)

_GIT_LOCATION_ENV_CACHE: frozenset[str] | None = None


def git_location_env() -> frozenset[str]:
    """git's own repo-local env vars (+ `_EXTRA`). Queried once, cached; falls back to the
    pinned list if git is unavailable. Never scrubbed itself -- the query is repo-agnostic."""
    global _GIT_LOCATION_ENV_CACHE
    if _GIT_LOCATION_ENV_CACHE is None:
        names: set[str] = set(GIT_LOCATION_ENV_FALLBACK)
        try:
            p = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            if p.returncode == 0:
                names |= {ln.strip() for ln in p.stdout.split() if ln.strip()}
        except OSError:
            pass  # git missing -- the pinned fallback stands
        _GIT_LOCATION_ENV_CACHE = frozenset(names | set(GIT_LOCATION_ENV_EXTRA))
    return _GIT_LOCATION_ENV_CACHE


def scrubbed_git_env() -> dict[str, str]:
    """os.environ minus the repo-location vars, so ``cwd=``/``-C`` alone decides which repo
    git reads."""
    scrub = git_location_env()
    return {k: v for k, v in os.environ.items() if k not in scrub}
