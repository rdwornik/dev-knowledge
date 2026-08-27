#!/usr/bin/env python
"""proof_layer.py — family 3, stated once with its predicate (`[#596]`).

THE DURABLE HOME. `tasks/596-*.md` asks for the class to be *"stated once in a durable home
with its predicate"*. This module is that home, and the predicate is EXECUTABLE rather than
prose — which is the strongest form the ask admits, and the form this repo's own conventions
prefer (cite the surface that computes a thing, do not retype it).

THE CLASS — an ENVIRONMENT-CONDITIONAL GUARD.

    A test or guard whose enforcement is gated, by `skipif` or a tool-presence probe, on the
    presence of the very environment it polices.

Stated by the repo that filed it, and quoted here because it is the whole rule in one line:

    "A hygiene test that can be skipped on the machine that breaks hygiene is not a mechanism."
    — win-tooling, tests/test_repo_root_hygiene.py

WHY IT IS THE SAME DEFECT, ONE LAYER OUT (sweep §9.1, verbatim): §0–§8 swept the `ALL_CHECKS`
members for a check that *"cannot compute its ground truth at run time and reports a
non-failing status anyway. Family 3 is that defect displaced one layer: the **proof that an
enforcement organ fires** is itself gated on the presence of the very environment it polices.
Nothing reports `unavailable` — the test simply never runs, and the suite prints green."*

And why it is WORSE than the `unavailable` it resembles, which is the reason it earns its own
layer rather than a footnote: *"`unavailable` at least renders as N/A in the audit table, so a
reader can see that a cell was not measured. A skipped test renders as a dot in a pytest
summary nobody reads line by line, and the enforcement claim it was written to support
survives in prose entirely unqualified."*

THE TWO ROWS, AND WHY NEITHER ABSORBS THE OTHER (the row's leg 4, recorded here because here
is where both are named). `[#583]` owns the **SITE** layer: every check, validator and gate leg
that can report a non-failing "could not evaluate" status — the thing that RUNS and reports.
`[#596]` owns the **PROOF** layer: whether the thing that proves an organ fires was itself
evaluated. The sweep's close packet (§6 D-8) names them as distinct, and its §9.7 disposition
routes family 3 to `[#583]` as OWNED *at the site layer* while recording that no row was born
for the proof layer — which is the gap this row fills. So: `[#583]`'s sweep rows are
**instances of this class measured at the site layer**, not a separate list; and this row is
the same class measured one layer up. Killing either loses a layer.

THE §9.6 CONFORMING PATTERN, generalised — `proof_status`. The sweep found the remedy already
in-house at `tests/test_legibility_graph_conformance.py`, under an operator contract quoted in
its own source: *"derive the cell status at runtime from the same check the skipif uses — never
hardcode 'proven'"*. `proof_status` is that, made general: a proof whose predicate is false
renders `not-proven`, and there is no argument for which it returns `proven` without the
predicate being true. An unknown environment also renders `not-proven` — the whole point is
that not-measured and measured-good are different facts.

WHAT THE PREDICATE MATCHES, and each token is taken from a measured exemplar rather than
imagined:

  * `importlib.util.find_spec(...)` / `find_spec(...)` — sweep §9.3 and §9.4, both live
    exemplars in this repo;
  * `shutil.which(...)` — sweep §9.2, the win-tooling exemplar;
  * `Path(...).exists()` on a probed interpreter/binary path — §9.2's second half;
  * `os.environ` / `os.getenv` gating — the same shape reached through a variable.

THE COUNTER-RULE IS ENFORCED TOO, because over-applying this predicate would bury the class in
noise. A `skipif` on a PLATFORM or a LANGUAGE VERSION (`sys.platform`, `sys.version_info`) is
not family 3: it gates on what the code can run under, not on the presence of the thing being
policed. `tests/test_proof_layer.py` asserts both directions.

SELF-POLICING is the sharpening — a guard gated on the tool that RUNS the enforcement, which
is what makes §9.3 *"the sharpest instance in the repo"*: the organ built to refuse "files are
present" evidence falls back to exactly that evidence, silently. It is a DECLARED ROSTER
(`ENFORCEMENT_RUNNERS`), not an inference about intent, and the reason is measured: the first
draft inferred intent from how often a module mentioned its gated tool, and on the live tree
that returned True for **all 38** guards — a field that looked measured and discriminated
nothing. The roster reproduces the sweep's two named exemplars exactly (both `pre_commit`) and
correctly excludes its §9.2 one, which the sweep calls load-bearing and CORRECT.

HONEST LIMITS — stated because they bound what a clean run means:
  * It reads `skipif` marks and module-level `pytestmark`. A bare `pytest.skip()` inside a test
    body, or a skip reached through a fixture, is NOT detected. That is a real hole, narrowed
    rather than closed, and named so nobody reads a clean scan as "no family-3 instances".
  * `self_policing` reports the MEASURABLE case — gated on a declared enforcement runner — and
    does not guess the rest. A guard on `git`, `grep` or `pwsh` may still be self-policing in a
    module whose subject IS that tool; `gated_tests` carries the blast radius alongside it.
  * The scanner reports what is GATED, never whether the gate is wrong. §9.2's exemplar is
    load-bearing and correct where it lives; what the sweep praises there is that win-tooling
    *paid to route around it*. A guard on this list is a question, not a verdict.
  * A module that cannot be parsed is reported UNREADABLE, never counted clean — assuming
    clean on an unreadable input is precisely this class, reached through the scanner.

Read-only (Layer 2): parses files, writes nothing. The baseline is regenerated only by an
explicit `--write-baseline`.
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

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("proof-layer")

CHECK_NAME = "proof_layer"
BASELINE_RELPATH = "ecosystem/proof-layer-baseline.json"
DETECTOR_ID = "proof-layer/v1"

#: The two rows, named so the relationship is machine-readable and not only prose.
SITE_LAYER_ROW = "[#583]"
PROOF_LAYER_ROW = "[#596]"
LAYER_RELATIONSHIP = (
    f"{SITE_LAYER_ROW} owns the SITE layer — a check that runs and reports a non-failing "
    f"'could not evaluate'. {PROOF_LAYER_ROW} owns the PROOF layer — whether the thing that "
    f"proves an organ fires was itself evaluated. The sweep's rows are INSTANCES of one class "
    f"measured at two layers; neither row absorbs the other, and killing either loses a layer."
)

#: The sweep artifact's two named live exemplars (§9.3, §9.4). Declared so the acceptance
#: criterion is checkable rather than asserted.
SWEEP_EXEMPLARS: tuple[str, ...] = (
    "tests/test_enforcement_coverage.py",
    "tests/test_floor_conformance.py",
)

SCOPE_MODULE = "module"
SCOPE_FUNCTION = "function"

PROVEN = "proven"
NOT_PROVEN = "not-proven"

#: Tool-presence probes. Each is taken from a measured exemplar — see the module docstring.
_PROBE_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bfind_spec\s*\(\s*[\"'](?P<tool>[A-Za-z0-9_.]+)[\"']"),
    re.compile(r"\bwhich\s*\(\s*[\"'](?P<tool>[A-Za-z0-9_.\-]+)[\"']"),
    re.compile(r"\bgetenv\s*\(\s*[\"'](?P<tool>[A-Za-z0-9_]+)[\"']"),
    re.compile(r"\benviron\s*(?:\.get\s*\(\s*)?\[?\s*[\"'](?P<tool>[A-Za-z0-9_]+)[\"']"),
)
#: A probe reached through a NAME rather than inline — `not _HAS_PRECOMMIT`,
#: `not Path(PWSH).exists()`. The name is resolved against module-level assignments.
_INDIRECT_PROBE_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b")

#: NOT family 3 — gating on what the code can run under, not on the thing being policed.
_COUNTER_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsys\.version_info\b"),
    re.compile(r"\bsys\.platform\b"),
    re.compile(r"\bplatform\.(system|machine|python_version)\b"),
)


@dataclass(frozen=True)
class Guard:
    """One environment-conditional guard."""
    module: str
    scope: str
    tool: str
    gated_tests: int
    self_policing: bool
    target: str = "<module>"
    reason: str = ""

    @property
    def key(self) -> str:
        """Identity for the ratchet: module plus the PROOF that is gated.

        `target` is the gated test's own name — or, for a module-level mark, `<module:tool>`.
        NOT the skip reason, and not a bare `<module>`. Both spellings were tried against the
        live tree and both collapsed real guards: keying on the reason folded six distinct
        `test_audit.py` guards into one identity ("git not available"), and a bare `<module>`
        folded the two module-level marks `test_e2e_consumer_lifecycle.py` carries (`RUN_E2E`
        and `pre-commit`) into one. The ratchet compares SETS, so a collapsed key makes a real
        guard invisible AND makes `load_baseline`'s duplicate check reject the baseline that
        recorded it. Measured, not theorised: 38 guards, 38 distinct keys.
        """
        return f"{self.module}::{self.target}"


@dataclass(frozen=True)
class Baseline:
    """The committed guard population at arm time, keyed on identity rather than a count."""
    guards: tuple[str, ...] = ()
    detector_id: str = DETECTOR_ID


def repo_root() -> Path:
    return _SCRIPTS.parent


def proof_status(guard: Guard, environment_present: bool | None) -> str:
    """Render one gated proof's cell, deriving it from the SAME predicate the skipif uses.

    The §9.6 conforming pattern generalised. `None` — an environment nobody measured — is
    `not-proven`, deliberately: not-measured and measured-good are different facts, and
    collapsing them is the whole defect. There is no code path returning `PROVEN` without
    `environment_present` being true.
    """
    return PROVEN if environment_present is True else NOT_PROVEN


# --- the predicate -------------------------------------------------------------------------

def _skipif_condition(node: ast.expr) -> ast.expr | None:
    """The condition of a `pytest.mark.skipif(...)` expression, or None."""
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    name = []
    while isinstance(func, ast.Attribute):
        name.append(func.attr)
        func = func.value
    if isinstance(func, ast.Name):
        name.append(func.id)
    if "skipif" not in name:
        return None
    if node.args:
        return node.args[0]
    for kw in node.keywords:
        if kw.arg == "condition":
            return kw.value
    return None


def _reason_of(node: ast.expr) -> str:
    if not isinstance(node, ast.Call):
        return ""
    for kw in node.keywords:
        if kw.arg == "reason" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    return ""


def _probed_tools(source: str) -> list[str]:
    """EVERY tool a condition probes for, in order of appearance; `[]` for none.

    ALL of them, not the first. A compound condition is common and it changes the answer:
    `requires_precommit = pytest.mark.skipif(not _HAS_PRECOMMIT or shutil.which("git") is
    None, ...)` probes for BOTH, and returning only the first match classified it as `git`
    and dropped it out of the self-policing cohort it belongs to. Measured on the live tree
    while fixing the terra review's finding 3.

    The counter-rule is applied FIRST: a platform or language-version gate is refused before
    any probe is looked for, so `skipif(sys.version_info < (3, 12))` can never be family 3
    even if the same line also mentions a module name.
    """
    if any(p.search(source) for p in _COUNTER_RES):
        return []
    found: list[str] = []
    for pattern in _PROBE_RES:
        for match in pattern.finditer(source):
            tool = match.group("tool")
            if tool not in found:
                found.append(tool)
    return found


def _module_assignment_nodes(tree: ast.Module) -> dict[str, ast.expr]:
    """`{NAME: value node}` for every module-level assignment.

    Two consumers, and both matter. An indirect PROBE resolves through it
    (`_HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not None`), and so does a
    named MARKER ALIAS (`requires_git = pytest.mark.skipif(...)` used as `@requires_git`).
    """
    out: dict[str, ast.expr] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = node.value
    return out


def _module_assignments(tree: ast.Module) -> dict[str, str]:
    """`{NAME: source}` for module-level assignments, so an indirect probe resolves."""
    return {name: ast.unparse(node) for name, node in _module_assignment_nodes(tree).items()}


def _resolve_marker(node: ast.expr, alias_nodes: dict[str, ast.expr]) -> ast.expr | None:
    """The `pytest.mark.skipif(...)` call this decorator or `pytestmark` element denotes.

    A decorator is EITHER the call itself (`@pytest.mark.skipif(...)`) OR a bare name bound to
    one at module level (`requires_git = pytest.mark.skipif(...)`, used as `@requires_git`).

    THE ALIAS FORM IS NOT AN EDGE CASE HERE — it is the DOMINANT form in this repo, and
    missing it made the first measurement a large undercount: 38 guards found against 18+
    modules using the alias, including two `requires_precommit` aliases (`test_block_ff_push`,
    `test_carrier_hooks_source`) that gate on an enforcement RUNNER and so belong to the
    sharpest cohort. Found by the terra review of this lane, verified by grep before fixing.
    """
    if isinstance(node, ast.Name) and node.id in alias_nodes:
        node = alias_nodes[node.id]
    return node if _skipif_condition(node) is not None else None


def _resolve_tools(condition: ast.expr, assignments: dict[str, str]) -> list[str]:
    """Every probed tool, following ONE level of module-level indirection.

    One level, not arbitrary: `_HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not
    None` (§9.3) and `PWSH = shutil.which("pwsh") or ...` (§9.2) are both one hop, and both are
    live exemplars. Chasing further would trade a real gain for a guess.

    Direct probes come first, then indirect ones, so `primary_tool`'s tie-break reads the
    condition the way it is written.
    """
    source = ast.unparse(condition)
    if any(p.search(source) for p in _COUNTER_RES):
        return []
    found = list(_probed_tools(source))
    for name in _INDIRECT_PROBE_RE.findall(source):
        if name in assignments:
            for tool in _probed_tools(assignments[name]):
                if tool not in found:
                    found.append(tool)
    return found


def primary_tool(tools: list[str]) -> str | None:
    """The tool a guard is REPORTED against.

    An enforcement runner wins the tie. A guard gated on "pre-commit absent OR git absent" is
    gated on the enforcement runner among other things, and reporting it as `git` buries it in
    the 224-strong `git` cohort instead of the 5-strong sharpest one.
    """
    if not tools:
        return None
    for tool in tools:
        if _is_self_policing(tool):
            return tool
    return tools[0]


def _count_tests(tree: ast.Module) -> int:
    return sum(1 for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name.startswith("test_"))


#: The tools whose job is to RUN the enforcement. A guard gated on one of these is gated on
#: the enforcement runner itself — the sharpest form of the class, and the form BOTH of the
#: sweep's named exemplars take (§9.3 and §9.4 are both `pre_commit`).
#:
#: A DECLARED ROSTER, deliberately, rather than an intent heuristic. The first draft here
#: guessed intent — "does the module mention the tool more than the guard needs" — and
#: measured against the live tree it returned True for all 38 guards, i.e. it discriminated
#: nothing. The sweep's own "sharpest instance" call is editorial, and mechanising editorial
#: judgement produces a field that looks measured and is not. This roster reproduces the
#: sweep's two exemplars exactly and correctly excludes its §9.2 one, which the sweep calls
#: LOAD-BEARING AND CORRECT rather than a defect.
ENFORCEMENT_RUNNERS: frozenset[str] = frozenset({"pre_commit", "pre-commit"})


def _is_self_policing(tool: str) -> bool:
    """Is this guard gated on the tool that RUNS the enforcement it proves?

    Honest limit, and it is the reason this is a roster and not an inference: a guard gated on
    `git`, `grep` or `pwsh` may still be self-policing in a module whose subject IS that tool.
    This field reports the measurable case and does not guess the rest; `gated_tests` carries
    the blast radius the sweep emphasised alongside it.
    """
    return tool in ENFORCEMENT_RUNNERS or tool.replace("_", "-") in ENFORCEMENT_RUNNERS


def scan_guards(tests_dir: Path, *, report_unreadable: bool = False):
    """Every environment-conditional guard under `tests_dir`.

    Returns `list[Guard]`, or `(list[Guard], list[str])` when `report_unreadable` is set. A
    module that cannot be parsed is UNREADABLE, never counted clean.
    """
    guards: list[Guard] = []
    unreadable: list[str] = []
    for path in sorted(Path(tests_dir).glob("*.py")):
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            unreadable.append(path.name)
            continue

        alias_nodes = _module_assignment_nodes(tree)
        assignments = {n: ast.unparse(v) for n, v in alias_nodes.items()}
        total_tests = _count_tests(tree)

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
                if condition is None:
                    continue
                tool = primary_tool(_resolve_tools(condition, assignments))
                if tool is None:
                    continue
                guards.append(Guard(
                    module=path.name, scope=SCOPE_MODULE, tool=tool,
                    gated_tests=total_tests, self_policing=_is_self_policing(tool),
                    target=f"<module:{tool}>", reason=_reason_of(candidate)))

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
                if condition is None:
                    continue
                tool = primary_tool(_resolve_tools(condition, assignments))
                if tool is None:
                    continue
                guards.append(Guard(
                    module=path.name, scope=SCOPE_FUNCTION, tool=tool, gated_tests=1,
                    self_policing=_is_self_policing(tool), target=node.name,
                    reason=_reason_of(decorator)))

    return (guards, unreadable) if report_unreadable else guards


# --- the ratchet ---------------------------------------------------------------------------

def ratchet_findings(guards, baseline: Baseline | None,
                     unreadable: list[str] | None = None) -> list[tuple[str, str]]:
    """The verdict as `(status, evidence)` pairs. PURE — no filesystem.

    Tuples rather than `Finding` objects so this module imports nothing from `audit`. ONE
    FINDING PER CONCERN: the `#147` register suppresses an ENTIRE Finding on a substring
    match, so a bundle would let one dispositioned guard wave through every other.

    WARN-tier, and the reason is the one `funnel_coverage` records: the live population is
    pre-existing debt this row did not create, and arming RED against it would turn the gate
    off on day one. The teeth are the named regression and the identity keying.
    """
    out: list[tuple[str, str]] = []
    for name in (unreadable or []):
        out.append(("warn",
                    f"tests/{name} could not be parsed, so it was not scanned for "
                    f"environment-conditional guards — reported rather than counted clean, "
                    f"which is this very class reached through the scanner"))
    if baseline is None:
        out.append(("warn",
                    f"no readable {BASELINE_RELPATH} — the proof-layer ratchet is INERT "
                    f"({len(guards)} environment-conditional guard(s) live); the gate is not "
                    f"measuring growth"))
        return out
    if baseline.detector_id != DETECTOR_ID:
        out.append(("warn",
                    f"detector mismatch: baseline stamped {baseline.detector_id!r} but this "
                    f"measurement was produced by {DETECTOR_ID!r} — not commensurable; "
                    f"re-measure and re-stamp rather than comparing them"))
        return out

    known = set(baseline.guards)
    for guard in sorted(guards, key=lambda g: g.key):
        if guard.key in known:
            continue
        sharp = " and is gated on the very tool it polices" if guard.self_policing else ""
        out.append(("warn",
                    f"{guard.module} gates {guard.gated_tests} test(s) behind a "
                    f"{guard.scope}-level skipif on {guard.tool!r}{sharp} — a proof that can "
                    f"be skipped on the machine that breaks the property is not a mechanism. "
                    f"Move the property that cannot be skipped OUT from behind the guard, or "
                    f"propagate the skip predicate into a reporting surface so a skipped "
                    f"proof renders as {NOT_PROVEN} (sweep sections 9.2 and 9.6)"))
    return out


def render_baseline(guards, measured_at: str, measured_at_sha: str, provenance: str) -> str:
    payload = {
        "_": ("Committed baseline for the family-3 proof-layer ratchet ([#596]). Regenerate: "
              "python scripts/proof_layer.py --write-baseline. The class, its predicate and "
              "its honest limits: scripts/proof_layer.py (module docstring)."),
        "detector_id": DETECTOR_ID,
        "measured_at": measured_at,
        "measured_at_sha": measured_at_sha,
        "guard_count": len(guards),
        "provenance": provenance.strip(),
        "guards": sorted(g.key for g in guards),
        "self_policing": sorted(g.key for g in guards if g.self_policing),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def load_baseline(repo_path: Path) -> Baseline | None:
    """The committed baseline, or None when absent/unreadable/malformed.

    Integrity rules are `funnel_coverage.load_baseline`'s, for the reasons recorded there: the
    declared count agrees with the list it counts, and duplicates are refused because the
    ratchet compares SETS.
    """
    path = Path(repo_path) / BASELINE_RELPATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("guards"), list):
        return None
    if not all(isinstance(g, str) for g in data["guards"]):
        return None
    if len(set(data["guards"])) != len(data["guards"]):
        return None
    declared = data.get("guard_count")
    if not isinstance(declared, int) or isinstance(declared, bool):
        return None
    if declared != len(data["guards"]):
        return None
    return Baseline(guards=tuple(data["guards"]),
                    detector_id=str(data.get("detector_id", "")))


# --- CLI -----------------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Family 3 at the proof layer — a test or guard whose enforcement is gated "
                    "on the presence of the environment it polices ([#596]).")
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--measured-at", default="")
    parser.add_argument("--sha", default="")
    parser.add_argument("--provenance", default="arm-time measurement")
    parser.add_argument("--relationship", action="store_true",
                        help="print the [#583] / [#596] layer relationship and exit")
    args = parser.parse_args(argv)

    if args.relationship:
        print(LAYER_RELATIONSHIP)
        return 0

    guards, unreadable = scan_guards(Path(args.repo_root) / "tests", report_unreadable=True)

    if args.write_baseline:
        target = Path(args.repo_root) / BASELINE_RELPATH
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_baseline(guards, args.measured_at, args.sha, args.provenance),
                          encoding="utf-8", newline="\n")
        logger.info("wrote %s — %d guard(s), %d self-policing", target, len(guards),
                    sum(1 for g in guards if g.self_policing))
        return 0

    findings = ratchet_findings(guards, load_baseline(args.repo_root), unreadable)
    for status, evidence in findings:
        (logger.error if status == "fail" else logger.warning)("%s", evidence)
    if not findings:
        logger.info("%d environment-conditional guard(s), all at baseline; %d self-policing",
                    len(guards), sum(1 for g in guards if g.self_policing))
    return 1 if any(s == "fail" for s, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(_main())
