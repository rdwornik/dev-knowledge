#!/usr/bin/env python
"""safe_remove.py — #195 code->code safe-removal gate (the #193 reverse-dep oracle's CONSUMER).

The reverse-dependency oracle (reverse_dep_oracle.py, #193) COMPUTES who references a symbol but
nothing acts on it (GAP-1: an oracle without a gate). This module is that consumer: it BLOCKS
removing a scripts/ Python module while a live EXTERNAL referrer still imports/uses one of its
top-level symbols, and NAMES the referrer. It is the automated form of the manual "scan
references before cutting" (LESSONS 2026-06-03) and a guard against the failure class behind the
2026-03-14 bulk-restore incident (removing still-needed files).

Two consumers of one core (`evaluate_removal`):
  * CLI  — `py scripts/safe_remove.py scripts/foo.py [...]` run BEFORE removing, while the
    module still exists, so the oracle queries the LIVE repo directly (no temp copy -> reliable
    cross-module resolution). Exit non-zero + names referrers when unsafe.
  * Build-time — `check_removal()` is the engine behind audit.py's `check_safe_removal` (in
    ALL_CHECKS). It detects a scripts/*.py deletion in the git diff and, because the module is
    already gone from the working tree (the oracle resolves symbols from the working tree, so a
    deleted symbol is `symbol-not-found`), materializes a query root = a COPY of the current
    working scripts/ + the removed module(s) RESTORED from HEAD, then queries the oracle there.

HONEST LIMIT (inherited from the oracle, ADR-89): static-Python-only. Dynamic dispatch,
getattr/setattr, string-keyed registries, and ALL cross-language edges are INVISIBLE. For a
*removal* gate that risks a false PASS (a real referrer the oracle cannot see), never a false
FAIL. Test-only importers ARE real referrers (removing the module breaks the test) -> blocking on
them is correct; co-removing the test is the escape.

THE FALSE PASS IS OBSERVED, NOT HYPOTHETICAL (2026-09-12, lane `lane-x-734-retire-stage-2`).
This gate returned SAFE over `scripts/desired_state_loader.py`; the deletion landed and the full
suite went RED. `tests/test_membership_agreement.py` loads that module BY NAME through
`importlib` and pins `parse_registry_md` as the reference implementation keeping `audit.py`'s
duplicated inline registry reader honest — precisely the invisible-edge class ADR-89 declares
the static oracle cannot see. The loader was RESTORED. Two consequences for anyone reading a
SAFE verdict here: (1) SAFE is necessary, never sufficient — it was caught only because the lane
ran a paired baseline/tip suite instead of trusting this tool; (2) the loader stays a census
orphan afterwards because it stays a *static* orphan — unreachable to the census and dead are
different facts. Evidence:
`docs/audits/2026-09-12-technical-lane-x-734-retire-stage-2-evidence.md`.

PARTIALLY MITIGATED, AND THE RESIDUE IS NAMED. `_bare_stem_literal_hits` below now downgrades
an otherwise-SAFE verdict to REVIEW when the module's bare stem appears as a quoted literal —
which catches THIS shape (`_load("desired_state_loader")`). It does NOT close the class: a
string-keyed reference built by concatenation, read from a config file, or spelled differently
from the stem is still invisible, and the honest limit above stands unchanged. REVIEW is a
prompt to look, not a second oracle.

When the oracle cannot verify (Pyright absent -> oracle-unavailable, or a symbol resolves
`ambiguous`), the verdict is `unverifiable` -> WARN + ALLOW (fail-open, honest-limit; operator
ruling #195). A hard FAIL is emitted ONLY on a resolved/partial answer with >=1 SURVIVING
referrer (a found referrer is real regardless of completeness).

Layer-2 / read-only (ADR-28/36): reads source + git, spawns the oracle's Pyright subprocess,
writes ONLY into a tempfile.mkdtemp() root cleaned in `finally`. Writes NO repo files (Critical
Rule #4; no leftovers, Critical Rule #9). Never raises to a consuming gate (inherits the oracle's
never-crash contract).
"""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Dual import (same shape as audit.py's sibling imports): `scripts.reverse_dep_oracle` for
# `python -m scripts.safe_remove`; bare for `python scripts/safe_remove.py` and the test path
# (scripts/ on sys.path). Reuse the oracle's entry + building blocks — never reimplement them.
try:
    from scripts.reverse_dep_oracle import (
        DEFAULT_WARM_TIMEOUT,
        run_oracle,
    )
except ImportError:  # pragma: no cover - exercised by the alternate launch path
    from reverse_dep_oracle import (
        DEFAULT_WARM_TIMEOUT,
        run_oracle,
    )

def _wiring_targets(root: Path) -> dict[str, set[str]]:
    """FPG-1's `triggers` relation, CONSUMED and never recomputed here (ADR-118 section 1).

    Imported inside the call rather than at module scope, for two reasons that are both real:
    `file_purpose_graph` pulls in rustworkx and four sibling validators, which is a cost
    `audit.py` should not pay on every run that deletes nothing; and this module is itself
    imported by `audit.py`, so a module-scope edge into the graph's own import fan-out is a
    cycle waiting for the first validator that wants a removal check.
    """
    try:
        from scripts.file_purpose_graph import wiring_targets
    except ImportError:  # pragma: no cover - exercised by the alternate launch path
        from file_purpose_graph import wiring_targets
    return wiring_targets(root)

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


# --- verdict ---------------------------------------------------------------------------

@dataclass
class Verdict:
    """The safe-removal answer. `status` is the gate decision; the rest is the evidence.

    status:
      * "unsafe"       — >=1 surviving referrer (FAIL / block); name them.
      * "safe"         — every removed symbol resolved with zero surviving referrers (PASS).
      * "review"       — otherwise SAFE, but the module's bare stem turned up as a quoted
                         string literal elsewhere in the tree (WARN / allow, downgraded from
                         SAFE — the dynamic-dispatch / string-keyed reference class the
                         oracle cannot see, ADR-89's honest limit; a hit is not proof of a
                         live reference, so this never escalates to a block).
      * "unverifiable" — the oracle could not establish the answer for >=1 symbol
                         (Pyright absent / ambiguous) AND no surviving referrer was found
                         (WARN / allow — fail-open, honest-limit).
    """

    status: str
    removal_set: list[str]
    surviving_referrers: list[dict] = field(default_factory=list)
    unverifiable: list[dict] = field(default_factory=list)
    completeness: str = "not-computed"
    reason: str = ""
    review_hits: list[dict] = field(default_factory=list)


# --- pure helpers ----------------------------------------------------------------------

def _norm(path) -> str:
    """Repo-relative, forward-slash, no leading './' — the one path form compared everywhere."""
    return Path(str(path)).as_posix()


#: Never worth descending into for a bare-stem literal scan — same posture as the oracle's own
#: exclusions, plus `.git` (not source).
_BARE_STEM_SKIP_DIRS = frozenset({".git", "__pycache__", "node_modules", ".venv", "worktrees"})


def _bare_stem_literal_hits(scan_root: Path, module_rel: str) -> list[dict]:
    """Grep `scan_root`'s `*.py` files for `module_rel`'s bare stem inside a quoted string
    literal — the dynamic-dispatch / string-keyed reference class the oracle (static-Python-only,
    ADR-89) cannot see. `_load("desired_state_loader")` is exactly this shape: no `import`, so
    Pyright's `references()` never finds it, and a module reached only this way verdicts SAFE
    while a real caller still depends on it (the false-PASS `docs/audits/
    2026-09-12-technical-lane-x-734-retire-stage-2-evidence.md` names).

    A hit is NOT proof of a live reference (the string could be an unrelated coincidence, a
    comment, or a docstring mention) — it downgrades an otherwise-SAFE verdict to REVIEW rather
    than blocking, the same fail-open honest-limit posture `evaluate_removal` already takes for
    `unverifiable`. Never raises: an unreadable file is skipped, not fatal.
    """
    stem = Path(module_rel).stem
    pattern = re.compile(r"""['"]""" + re.escape(stem) + r"""['"]""")
    module_abs = (scan_root / module_rel).resolve()
    hits: list[dict] = []
    for path in sorted(scan_root.rglob("*.py")):
        try:
            rel_parts = path.relative_to(scan_root).parts
        except ValueError:
            continue
        if _BARE_STEM_SKIP_DIRS & set(rel_parts):
            continue
        try:
            if path.resolve() == module_abs:
                continue  # the module's own file is not a referrer to itself
        except OSError:
            pass
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                hits.append({"file": _norm(path.relative_to(scan_root)), "line": lineno})
    return hits


def _module_top_level_symbols(path: Path) -> list[str]:
    """The module's IMPORT SURFACE: top-level def/async-def/class names (NOT nested/methods).

    Only top-level names are importable from another module, so only they can have a CROSS-module
    (surviving) referrer — a nested function's only referrers are in-file and co-remove with it.
    Underscore-prefixed names ARE included: privacy is by convention, not enforced, so a
    `_helper` can still be imported by a sibling and dangle on removal.
    """
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    return [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]


# --- git plumbing (fail-soft; same pattern as reverse_dep_oracle._git) -----------------

def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
    )


def detect_removed_modules(repo_root: Path, base: str = "HEAD") -> list[str]:
    """scripts/**/*.py files DELETED in the working tree vs `base` (HEAD by default).

    `git diff --diff-filter=D` against HEAD reports both staged and unstaged deletions, so this
    sees what the current working state removes regardless of whether `git rm` staged it. Fail-soft
    -> [] (git absent / not a repo): the gate then finds no removal and PASSes (it never wedges).
    """
    try:
        res = _git(repo_root, "diff", "--diff-filter=D", "--name-only", base, "--")
    except (OSError, subprocess.SubprocessError):
        return []
    if res.returncode != 0:
        return []
    out = []
    for line in res.stdout.splitlines():
        rel = _norm(line.strip())
        if rel.startswith("scripts/") and rel.endswith(".py"):
            out.append(rel)
    return sorted(out)


def _restore_from_base(repo_root: Path, rel_path: str, base: str = "HEAD") -> str | None:
    """The `base` (HEAD) content of a now-deleted file, or None if git can't produce it."""
    try:
        res = _git(repo_root, "show", f"{base}:{rel_path}")
    except (OSError, subprocess.SubprocessError):
        return None
    return res.stdout if res.returncode == 0 else None


def materialize_query_root(repo_root: Path, removal_set, dest: Path, base: str = "HEAD") -> Path:
    """Build the oracle query root = COPY of the current working scripts/ + removed modules RESTORED.

    Why a frankenstein (working-tree + restored), not a pure `base` snapshot: the working tree
    reflects the POST-change referrers (a referrer whose import line was edited away no longer
    references the removed symbol), while the restored module gives the oracle a definition to
    query. Querying a pure HEAD snapshot would re-introduce edited-away references and false-FAIL.
    A deleted referrer is simply absent from the working tree -> absent from the copy (co-removal
    handled for free). Returns the dest root (its scripts/ subtree is the materialized tree).
    """
    src_scripts = repo_root / "scripts"
    dest_scripts = dest / "scripts"
    if src_scripts.is_dir():
        shutil.copytree(src_scripts, dest_scripts, dirs_exist_ok=True)
    else:
        dest_scripts.mkdir(parents=True, exist_ok=True)
    for rel in removal_set:
        content = _restore_from_base(repo_root, rel, base)
        if content is None:
            continue  # cannot restore -> evaluate_removal records it as unverifiable
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    return dest


# --- the CROSS-LANGUAGE leg: a wiring surface is a referrer the oracle cannot see -------

def wiring_referrers(removal_set, scan_root: Path) -> list[dict]:
    """Wiring surfaces that NAME a file in the removal set — the oracle's blind spot, closed.

    `[#664]` clause 2 ([#554] lane aa-1's L3): the delivery spine's `triggers` relation, read
    here as a REMOVAL guard. This module is the consumer; FPG-1 is where the relation lives.

    THE HONEST LIMIT THIS MODULE HAS CARRIED SINCE #195 IS *"ALL cross-language edges are
    INVISIBLE"*, and that limit has a measured body count. `scripts/cloud_provisioning.py` was
    retired at `3c9418cc` as an unreferenced orphan; its six live callers were shell lines in
    `.devcontainer/provision.sh` naming it by PATH. The static importer scan could not see them,
    the verdict came back SAFE, the deletion landed, and on 2026-09-14 a fresh codespace died
    into a recovery container. The limit was real; it was also closable, and this closes it.

    ONE MECHANISM, NOT A PROVISIONING SPECIAL CASE. The relation read here is FPG-1's
    `triggers` input (`file_purpose_graph.wiring_targets`), so EVERY declared wiring surface
    protects what it names with no second code path: a pre-commit hook's `entry:`, a workflow's
    `run:` line, a plugin manifest, and provisioning's shell all arrive through the same
    function. Writing a provisioning-shaped branch here would have been the second special case
    the lane contract says to stop and generalise instead of writing.

    DIRECTION OF ERROR, kept where the module already puts it: a surface listed in the removal
    set is CO-REMOVED and confers nothing, and everything else is a real referrer. Never raises
    — a graph this cannot read yields no referrers, and the existing oracle legs still decide.
    """
    removal = {_norm(p) for p in removal_set}
    try:
        targets = _wiring_targets(Path(scan_root))
    except Exception:            # the gate must not wedge on an unreadable surface
        return []
    found: list[dict] = []
    for surface, named in sorted(targets.items()):
        if _norm(surface) in removal:
            continue             # co-removed: the caller is going too
        for target in sorted(named):
            if _norm(target) in removal:
                found.append({"referrer": _norm(surface), "line": None, "symbol": None,
                              "module": _norm(target), "kind": "wiring"})
    return found


# --- the consumer proper ---------------------------------------------------------------

def evaluate_removal(removal_set, repo_root, *, oracle=run_oracle, langserver=None,
                     timeout: float = DEFAULT_WARM_TIMEOUT, scan_root=None) -> Verdict:
    """Is removing `removal_set` safe? Query the oracle for each removed module's import-surface
    symbols; a referrer SURVIVES iff its file is NOT itself in the removal set.

    `repo_root` is the QUERY root: the LIVE repo for the CLI (module still present) or the
    materialized frankenstein for the build-time path. `oracle` is injectable for deterministic
    tests (the #207 teeth-proof feeds a stub returning a known surviving referrer). `scan_root`
    is where the bare-stem string-literal downgrade greps — defaults to `repo_root`, but
    `check_removal` passes the REAL repo root there, because the build-time `repo_root` is a
    `scripts/`-only materialization and a dynamic reference living under `tests/` or elsewhere
    would otherwise be invisible to the downgrade too. Never raises.
    """
    repo_root = Path(repo_root).resolve()
    scan_root = Path(scan_root).resolve() if scan_root is not None else repo_root
    removal = {_norm(p) for p in removal_set}
    # The cross-language leg runs against `scan_root` and NOT `repo_root`, for the reason the
    # bare-stem downgrade already runs there: the build-time `repo_root` is a `scripts/`-only
    # materialization, and `.devcontainer/` and `.pre-commit-config.yaml` do not exist inside it.
    # Querying the frankenstein would find no wiring surfaces at all and report a clean leg.
    surviving: list[dict] = list(wiring_referrers(removal, scan_root))
    unverifiable: list[dict] = []
    completeness_seen: set[str] = set()

    for module in sorted(removal):
        mod_abs = repo_root / module
        if not mod_abs.is_file():
            unverifiable.append({"module": module, "symbol": None,
                                 "reason": "module not present in query root"})
            continue
        try:
            symbols = _module_top_level_symbols(mod_abs)
        except (OSError, SyntaxError) as exc:
            unverifiable.append({"module": module, "symbol": None,
                                 "reason": f"unparseable ({exc.__class__.__name__})"})
            continue
        for sym in symbols:
            try:
                ans = oracle(sym, module, repo_root, langserver=langserver, timeout=timeout)
            except Exception as exc:  # the oracle promises not to raise; belt-and-suspenders
                unverifiable.append({"module": module, "symbol": sym,
                                     "reason": f"oracle error ({exc.__class__.__name__})"})
                continue
            status = ans.get("resolution", {}).get("status")
            if status == "resolved":
                completeness_seen.add(ans.get("provenance", {}).get("completeness", "not-computed"))
                for dep in ans.get("reverse_dependents", []):
                    ref = _norm(dep.get("file", ""))
                    if ref and ref not in removal:
                        surviving.append({"referrer": ref, "line": dep.get("line"),
                                          "symbol": sym, "module": module})
            elif status in ("oracle-unavailable", "ambiguous"):
                unverifiable.append({"module": module, "symbol": sym, "reason": status})
            # symbol-not-found contributes nothing: no def to dangle on (PASS contribution).

    completeness = ("partial" if "partial" in completeness_seen
                    else "complete" if "complete" in completeness_seen
                    else "not-computed")
    # Order matters: a SURVIVING referrer is a hard FAIL even when other symbols were
    # unverifiable (a found referrer is real); unverifiability only decides safe-vs-WARN.
    if surviving:
        status = "unsafe"
        reason = (f"{len(surviving)} surviving referrer(s) would dangle on removal "
                  f"(completeness: {completeness})")
    elif unverifiable:
        status = "unverifiable"
        reason = (f"{len(unverifiable)} symbol(s)/module(s) the oracle could not verify "
                  f"(WARN + allow; honest-limit)")
    else:
        status = "safe"
        reason = "no surviving referrers; every removed symbol resolved clean"

    review_hits: list[dict] = []
    if status == "safe":
        for module in sorted(removal):
            review_hits.extend(_bare_stem_literal_hits(scan_root, module))
        if review_hits:
            status = "review"
            stems = sorted({Path(m).stem for m in removal})
            reason = (f"{len(review_hits)} bare-stem string-literal hit(s) for "
                      f"{', '.join(stems)} — a possible dynamic/string-keyed reference the "
                      f"oracle cannot see (static-Python-only limit); downgraded from SAFE, "
                      f"human review needed before removing")

    return Verdict(status, sorted(removal), surviving, unverifiable, completeness, reason,
                   review_hits)


def check_removal(repo_root: Path, base: str = "HEAD", *, oracle=run_oracle, langserver=None,
                  timeout: float = DEFAULT_WARM_TIMEOUT) -> Verdict:
    """Build-time engine: detect scripts/*.py deletions vs `base`, then evaluate them against a
    materialized (working-tree + restored) query root. No deletion -> an instant `safe` verdict
    (no Pyright cost). The temp root is removed in `finally` (no leftovers). `oracle` is
    injectable so the deterministic plumbing test drives the full diff->materialize->FAIL path
    without Pyright. Never raises.
    """
    repo_root = Path(repo_root).resolve()
    removal = detect_removed_modules(repo_root, base)
    if not removal:
        return Verdict("safe", [], reason="no scripts/*.py module removal in the diff")
    tmp = Path(tempfile.mkdtemp(prefix="safe-remove-"))
    try:
        query_root = materialize_query_root(repo_root, removal, tmp, base)
        return evaluate_removal(removal, query_root, oracle=oracle, langserver=langserver,
                                timeout=timeout, scan_root=repo_root)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- rendering / CLI -------------------------------------------------------------------

def format_text(verdict: Verdict) -> str:
    """Flat key:value/bullets inside ONE triple-backtick fence (CLAUDE.md S4 render discipline)."""
    out: list[str] = []
    out.append(f"safe-removal verdict: {verdict.status.upper()}")
    out.append(f"removal set: {', '.join(verdict.removal_set) or '(none)'}")
    out.append(f"reason: {verdict.reason}")
    if verdict.surviving_referrers:
        out.append("")
        out.append("surviving referrers (would dangle on removal):")
        for r in verdict.surviving_referrers:
            out.append(f"- {r['referrer']}:{r['line']} -> {r['symbol']} ({r['module']})")
    if verdict.unverifiable:
        out.append("")
        out.append("unverifiable (WARN + allow):")
        for u in verdict.unverifiable:
            tgt = u["symbol"] or u["module"]
            out.append(f"- {tgt}: {u['reason']}")
    if verdict.review_hits:
        out.append("")
        out.append("bare-stem string-literal hits (downgraded from SAFE; WARN + allow):")
        for h in verdict.review_hits:
            out.append(f"- {h['file']}:{h['line']}")
    out.append("")
    out.append("limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are "
               "INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).")
    return "```\n" + "\n".join(out) + "\n```"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="safe_remove",
        description="Code->code safe-removal gate (consumes the #193 reverse-dep oracle). Run "
                    "BEFORE removing a scripts/ module; refuses if a live external referrer remains.",
    )
    parser.add_argument("modules", nargs="+",
                        help="scripts/ module path(s) you intend to remove (e.g. scripts/foo.py)")
    parser.add_argument("--repo-root", default=str(_REPO_ROOT))
    parser.add_argument("--langserver", default=None,
                        help="path to pyright langserver.index.js (override resolution)")
    parser.add_argument("--timeout", type=float, default=DEFAULT_WARM_TIMEOUT)
    args = parser.parse_args(argv)

    # CLI runs against the LIVE repo (the module still exists) -> the oracle resolves directly,
    # no temp copy, reliable cross-module resolution.
    verdict = evaluate_removal(args.modules, Path(args.repo_root),
                               langserver=args.langserver, timeout=args.timeout)
    print(format_text(verdict))
    return 1 if verdict.status == "unsafe" else 0


if __name__ == "__main__":
    sys.exit(main())
