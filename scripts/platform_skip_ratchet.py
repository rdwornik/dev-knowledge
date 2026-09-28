#!/usr/bin/env python
"""platform_skip_ratchet.py — the platform-skip ratchet (row L4, D7 hub half).

WHY THIS EXISTS, AND WHY `proof_layer.py` CANNOT BE REUSED FOR IT. `proof_layer.py`'s
counter-rule (`_COUNTER_RES`, module docstring "THE COUNTER-RULE IS ENFORCED TOO") deliberately
EXEMPTS a `skipif` gated on `sys.platform`/`sys.version_info`/`platform.*` — that gate is
"what the code can run under", not family 3's "the presence of the thing being policed". Family
3's ratchet is therefore structurally blind to platform skips by design, and staying blind to
them is correct for THAT class. But nothing else counts them either, so a new
`skipif(sys.platform == "win32")` can be added anywhere with no gate noticing — the exact gap
`to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` D7 names: "a
**platform-skip ratchet** ... `proof_layer.py:58-60` deliberately exempts these, so it cannot be
reused."

THE CLASS THIS MODULE COUNTS: a test whose enforcement is gated, by `skipif` or a body
`pytest.skip()`, on `sys.platform` or `os.name` — i.e. the counter-rule's own carve-out, counted
rather than exempted. This is a SEPARATE, ADDITIVE ratchet, not a broadened `proof_layer`: a
guard can be in exactly one of the two classes (the counter-rule is mutually exclusive by
construction — see `proof_layer._probed_tools`/`_resolve_tools`, which return `[]` whenever a
platform/version condition is present), so a member counted here is never double-counted there.

LIBRARY-FIRST (O-12): the AST resolution of "which decorator/pytestmark IS a skipif, including
through a module-level alias" is already written, reviewed across 14 terra passes, and measured
against this tree at `scripts/proof_layer.py` (`_skipif_condition`, `_resolve_marker`,
`_module_assignment_nodes`). Re-implementing it here would re-open bugs that module's history
already paid to close (the alias form, compound conditions, the pytestmark-list form). This
module imports those helpers rather than duplicating them; the only new logic is (a) which
condition counts as PLATFORM rather than TOOL-PRESENCE, and (b) the body-`pytest.skip()` form,
which `proof_layer` explicitly does not attempt (its own "HONEST LIMITS": "A bare `pytest.skip()`
inside a test body ... is NOT detected").

WHAT COUNTS, exactly:
  * a `pytest.mark.skipif(condition, ...)` decorator (direct, or through a module-level alias)
    on a `test_*` function, or a module-level `pytestmark = pytest.mark.skipif(...)` /
    `pytestmark = [pytest.mark.skipif(...), ...]`, whose CONDITION SOURCE contains `sys.platform`
    or `os.name`;
  * a body `pytest.skip(...)` call reached only through an `if` (or `elif`) branch whose test
    contains `sys.platform` or `os.name` — the shape `if sys.platform == "win32": pytest.skip(...)`.

WHAT DOES NOT COUNT, on purpose: a bare `if os.name == "nt": ...` branch that does something OTHER
than skip (most of this repo's `os.name`/`sys.platform` branches choose between two working
code paths — that is the honest cross-platform arm ADR-CI-VERIFICATION's T3 already found "every
one has a working POSIX arm" for, and ratcheting IT would penalise portability rather than
measure its absence). Only a branch that ends in `pytest.skip(...)` is a site.

THE RATCHET, unlike `proof_layer`'s WARN-tier posture: THIS ONE FAILS. Row L4's Done-when is
explicit — "ratchet RED-first: an added platform skip fails" — so a key present now but absent
from the committed baseline is a FAIL finding, and the CLI exits 1. A key that has left the tree
(a fixed portability defect) is not reported at all; the baseline shrinks by re-running
`--write-baseline`, which is the only way the committed set gets smaller, matching row L4's "the
count of platform skips can only fall" (a `--write-baseline` that would GROW the set already-
committed baseline is refused — see `render_baseline`).

Read-only (Layer 2) except under `--write-baseline`: parses files, writes nothing else.
"""
from __future__ import annotations

import argparse
import ast
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from proof_layer import (  # noqa: E402 -- sys.path must be set first
    _module_assignment_nodes,
    _resolve_marker,
    _skipif_condition,
)

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("platform-skip-ratchet")

CHECK_NAME = "platform_skip_ratchet"
BASELINE_RELPATH = "ecosystem/platform-skip-baseline.json"
DETECTOR_ID = "platform-skip-ratchet/v1"

SCOPE_MODULE = "module"
SCOPE_FUNCTION = "function"
KIND_SKIPIF = "skipif"
KIND_BODY_SKIP = "body-skip"

#: The counter-rule's own carve-out (`proof_layer._COUNTER_RES` includes `sys.platform` but not
#: `os.name`; D7's row names both explicitly: "skipif(sys.platform|os.name)").
_PLATFORM_RE = re.compile(r"\bsys\.platform\b|\bos\.name\b")


@dataclass(frozen=True)
class PlatformSkip:
    """One platform-conditioned skip site."""

    module: str
    scope: str
    kind: str
    gated_tests: int
    target: str = "<module>"
    reason: str = ""

    @property
    def key(self) -> str:
        """Identity for the ratchet: module plus the gated target plus the KIND.

        The kind suffix matters here in a way it does not for `proof_layer.Guard`: a single
        function can carry both a `skipif` decorator and, in a different branch, a body
        `pytest.skip()` guarded on platform — two distinct sites this ratchet must not collapse
        into one key (collapsing them would let one disappear while the other grows unnoticed).
        """
        return f"{self.module}::{self.target}:{self.kind}"


@dataclass(frozen=True)
class Baseline:
    """The committed platform-skip population at arm time, keyed on identity."""

    sites: tuple[str, ...] = ()
    detector_id: str = DETECTOR_ID


def repo_root() -> Path:
    return _SCRIPTS.parent


def _is_platform_condition(condition: ast.expr) -> bool:
    return bool(_PLATFORM_RE.search(ast.unparse(condition)))


def _reason_of(node: ast.expr) -> str:
    if not isinstance(node, ast.Call):
        return ""
    for kw in node.keywords:
        if kw.arg == "reason" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    return ""


def _count_tests(tree: ast.Module) -> int:
    return sum(1 for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name.startswith("test_"))


def _is_pytest_skip_call(node: ast.expr) -> bool:
    """`pytest.skip(...)` — the exact attribute chain, not `pytest.mark.skipif`."""
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
        return False
    return node.func.attr == "skip" and isinstance(node.func.value, ast.Name) \
        and node.func.value.id == "pytest"


def _find_platform_body_skips(body: list[ast.stmt]) -> bool:
    """Is there a `pytest.skip(...)` call reachable only inside a platform-conditioned `if`?

    Walks every `ast.If` in `body` (at any depth) whose test mentions `sys.platform`/`os.name`,
    and looks for a `pytest.skip(...)` call anywhere within that `if`'s own body/orelse (NOT the
    surrounding function — a platform check that guards something else, with an unconditional
    skip elsewhere in the function, is not this class).
    """
    for node in ast.walk(ast.Module(body=body, type_ignores=[])):
        if not isinstance(node, ast.If):
            continue
        if not _is_platform_condition(node.test):
            continue
        for inner in ast.walk(ast.Module(body=node.body + node.orelse, type_ignores=[])):
            if isinstance(inner, ast.Expr) and _is_pytest_skip_call(inner.value):
                return True
            if isinstance(inner, ast.Call) and _is_pytest_skip_call(inner):
                return True
    return False


def scan_sites(tests_dir: Path, *, report_unreadable: bool = False):
    """Every platform-conditioned skip site under `tests_dir` (non-recursive, `*.py` only —
    matches `proof_layer.scan_guards`'s scope). Returns `list[PlatformSkip]`, or
    `(list[PlatformSkip], list[str])` when `report_unreadable` is set.
    """
    sites: list[PlatformSkip] = []
    unreadable: list[str] = []
    for path in sorted(Path(tests_dir).glob("*.py")):
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            unreadable.append(path.name)
            continue

        alias_nodes = _module_assignment_nodes(tree)
        total_tests = _count_tests(tree)

        # --- skipif / pytestmark, module-level ---------------------------------------------
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
                continue
            for element in (node.value.elts if isinstance(node.value, (ast.List, ast.Tuple))
                            else [node.value]):
                candidate = _resolve_marker(element, alias_nodes)
                if candidate is None:
                    continue
                condition = _skipif_condition(candidate)
                if condition is None or not _is_platform_condition(condition):
                    continue
                sites.append(PlatformSkip(
                    module=path.name, scope=SCOPE_MODULE, kind=KIND_SKIPIF,
                    gated_tests=total_tests, target="<module>",
                    reason=_reason_of(candidate)))

        # --- skipif, function-level (direct or via alias) --------------------------------------
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test_"):
                continue
            for raw_decorator in node.decorator_list:
                decorator = _resolve_marker(raw_decorator, alias_nodes)
                if decorator is None:
                    continue
                condition = _skipif_condition(decorator)
                if condition is None or not _is_platform_condition(condition):
                    continue
                sites.append(PlatformSkip(
                    module=path.name, scope=SCOPE_FUNCTION, kind=KIND_SKIPIF,
                    gated_tests=1, target=node.name, reason=_reason_of(decorator)))

            # --- body pytest.skip(), reached only through a platform-conditioned `if` ------
            if _find_platform_body_skips(node.body):
                sites.append(PlatformSkip(
                    module=path.name, scope=SCOPE_FUNCTION, kind=KIND_BODY_SKIP,
                    gated_tests=1, target=node.name, reason=""))

    return (sites, unreadable) if report_unreadable else sites


# --- the ratchet -----------------------------------------------------------------------------

def ratchet_findings(sites, baseline: Baseline | None,
                     unreadable: list[str] | None = None) -> list[tuple[str, str]]:
    """The verdict as `(status, evidence)` pairs. PURE — no filesystem.

    Unlike `proof_layer.ratchet_findings` (WARN-tier, because family 3 is pre-existing debt this
    row did not create), a NEW platform-skip site is `fail`: row L4's Done-when requires the
    ratchet to be RED-first on a growth. A missing/malformed baseline is ALSO `fail` — an inert
    ratchet reads as "0 findings", which is indistinguishable from "nothing new was added", and
    row L4's mechanism has to be able to tell those apart.
    """
    out: list[tuple[str, str]] = []
    for name in (unreadable or []):
        out.append(("fail",
                    f"tests/{name} could not be parsed, so it was not scanned for "
                    f"platform-conditioned skips — reported rather than counted clean"))
    if baseline is None:
        out.append(("fail",
                    f"no readable {BASELINE_RELPATH} — the platform-skip ratchet cannot tell a "
                    f"new skip from the committed set ({len(sites)} platform-conditioned skip(s) "
                    f"live); regenerate with --write-baseline"))
        return out
    if baseline.detector_id != DETECTOR_ID:
        out.append(("fail",
                    f"detector mismatch: baseline stamped {baseline.detector_id!r} but this "
                    f"measurement was produced by {DETECTOR_ID!r} — not commensurable; "
                    f"re-measure and re-stamp rather than comparing them"))
        return out

    known = set(baseline.sites)
    for site in sorted(sites, key=lambda s: s.key):
        if site.key in known:
            continue
        out.append(("fail",
                    f"{site.module} gates {site.gated_tests} test(s) behind a NEW "
                    f"{site.scope}-level platform {site.kind} — the platform-skip count may only "
                    f"fall (row L4). Site key: {site.key}. If this portability gap is genuinely "
                    f"unavoidable, it still has to be a DECIDED, committed addition: fix the "
                    f"underlying test instead, or re-run --write-baseline with the operator's "
                    f"ruling recorded, never silently."))
    return out


def render_baseline(sites, measured_at: str, measured_at_sha: str, provenance: str,
                    *, previous: Baseline | None = None) -> str:
    """Render the baseline JSON. Refuses (raises `ValueError`) a write that would GROW a set
    already committed with the SAME `DETECTOR_ID` — the only door row L4's "may only fall" has;
    an operator ruling that must widen it re-runs with `previous=None` (a fresh file) instead of
    silently overwriting a shrink-only contract.
    """
    current = sorted(s.key for s in sites)
    if previous is not None and previous.detector_id == DETECTOR_ID:
        grown = set(current) - set(previous.sites)
        if grown:
            raise ValueError(
                f"--write-baseline would GROW the committed platform-skip set by "
                f"{sorted(grown)} — the ratchet may only shrink; fix the site(s) instead, or "
                f"delete {BASELINE_RELPATH} first if an operator ruling truly re-bases it")
    payload = {
        "_": ("Committed baseline for the platform-skip ratchet (row L4, D7 hub half). "
              "Regenerate: python scripts/platform_skip_ratchet.py --write-baseline. The class "
              "and why proof_layer.py cannot carry it: scripts/platform_skip_ratchet.py (module "
              "docstring)."),
        "detector_id": DETECTOR_ID,
        "measured_at": measured_at,
        "measured_at_sha": measured_at_sha,
        "site_count": len(current),
        "provenance": provenance.strip(),
        "sites": current,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def load_baseline(repo_path: Path) -> Baseline | None:
    """The committed baseline, or None when absent/unreadable/malformed.

    Integrity rules mirror `proof_layer.load_baseline`: the declared count agrees with the list
    it counts, and duplicates are refused because the ratchet compares SETS.
    """
    path = Path(repo_path) / BASELINE_RELPATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("sites"), list):
        return None
    if not all(isinstance(s, str) for s in data["sites"]):
        return None
    if len(set(data["sites"])) != len(data["sites"]):
        return None
    declared = data.get("site_count")
    if not isinstance(declared, int) or isinstance(declared, bool):
        return None
    if declared != len(data["sites"]):
        return None
    return Baseline(sites=tuple(data["sites"]), detector_id=str(data.get("detector_id", "")))


# --- CLI ---------------------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The platform-skip ratchet (row L4, D7 hub half) — counts "
                    "skipif(sys.platform|os.name) and body pytest.skip() on platform; may only "
                    "shrink.")
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--measured-at", default="")
    parser.add_argument("--sha", default="")
    parser.add_argument("--provenance", default="arm-time measurement")
    args = parser.parse_args(argv)

    sites, unreadable = scan_sites(Path(args.repo_root) / "tests", report_unreadable=True)

    if args.write_baseline:
        target = Path(args.repo_root) / BASELINE_RELPATH
        previous = load_baseline(args.repo_root)
        try:
            rendered = render_baseline(sites, args.measured_at, args.sha, args.provenance,
                                       previous=previous)
        except ValueError as exc:
            logger.error("%s", exc)
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8", newline="\n")
        logger.info("wrote %s — %d platform-conditioned skip site(s)", target, len(sites))
        return 0

    findings = ratchet_findings(sites, load_baseline(args.repo_root), unreadable)
    for status, evidence in findings:
        (logger.error if status == "fail" else logger.warning)("%s", evidence)
    if not findings:
        logger.info("%d platform-conditioned skip site(s), all at or below baseline",
                    len(sites))
    return 1 if any(s == "fail" for s, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(_main())
