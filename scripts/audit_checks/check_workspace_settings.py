"""`check_workspace_settings` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL at extraction, together with `_WORKSPACE_REQUIRED_SETTINGS` and the
`_strip_jsonc` helper it exclusively owns; `audit.py` re-exports all three names —
`tests/test_audit.py` calls `aud._strip_jsonc` directly.

THE 2026-09-09 CHANGE (batch V, lane `lane-v-000-shape-spec-clauses`). This module is the
surface `ecosystem/fleet-shape-spec.yaml` names in the `asserted_by` of BOTH its `vscode`
and its `sorting` clause, and until now it opened neither — measured at `33bcb0bd` in
`docs/audits/2026-09-09-technical-shape-spec-clause-readers.md`, where it was two of the
three clauses whose asserting organ never read them. A decorative locator is worse than an
honest gap: `asserted_by: null` is visible in the file, a locator reads as enforced. Three
payloads are now consumed rather than restated here —

  * `vscode.workspace_file_glob`   the dot-prefix rule, which was the literal
                                   `startswith(".")`. Leak class 2 of the 78 measured
                                   corp-monorepo items was exactly one repo's copy of a
                                   fleet rule, so the rule stays in the fleet grammar.
  * `vscode.dir_allowed/_forbidden` what may sit in `.vscode/`: shared editor configuration
                                   yes, per-developer or machine-generated state no.
  * `sorting.asserted_by_setting`  the ONE setting that delivers the clause's asserted half.
                                   A clause naming a key this module does not require is
                                   claiming an assertion nobody makes, and is refused.

`_WORKSPACE_REQUIRED_SETTINGS` stays HERE and is cited BY the spec
(`vscode.workspace_required_settings_from`), rather than moving into it: that is this
repo's convention for a roster — name the surface that computes it — and inverting it would
put the same two keys in two files.

The spec is read through the module attribute `validate_hermetization.SHAPE_SPEC` at CALL
time, deliberately: a `from`-import binding would freeze the clauses at import and could not
be doctored, and `tests/test_fleet_shape_spec_readers.py` proves the read by doctoring the
clause and asserting this check's verdict follows.
"""

from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path

from ._common import Finding

# Dual-import, the shim `check_adr38_baseline` / `check_vision_md` already use: script mode
# (`python scripts/audit.py`) puts scripts/ on sys.path, package mode puts the repo ROOT
# there. The bare name is tried FIRST so this resolves to the SAME module object the tests
# and `scripts/batch_manifest.py` hold — a second execution under a package name would parse
# the spec twice and hand out constants that are equal but not identical.
try:
    import validate_hermetization as _vh
except ImportError:  # pragma: no cover - exercised by the repo-root import path
    from scripts import validate_hermetization as _vh

# Required VS Code workspace settings (ADR-59 Decision 3). "upper" (not "default")
# is what clusters ALL-CAPS canonical .md files ahead of lowercase configs.
_WORKSPACE_REQUIRED_SETTINGS = {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper",
}


def _strip_jsonc(text: str) -> str:
    """Strip // and /* */ comments and trailing commas from JSON-with-comments.

    VS Code .code-workspace files are JSONC; json.loads cannot parse them. Comment
    stripping respects string literals so a `//` inside a string value survives.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def _vscode_dir_issues(repo_path: Path, vscode_clause_allowed: list[str],
                       vscode_clause_forbidden: list[str]) -> list[str]:
    """`.vscode/` members measured against the spec's allowed / forbidden lists.

    An absent `.vscode/` is not an issue: the clause says what may sit there, not that the
    directory has to exist. `dir_forbidden` carries fnmatch globs (`*.log`) and is tested
    first, so a member that is both unlisted and forbidden reports the sharper reason.
    """
    vscode_dir = repo_path / ".vscode"
    if not vscode_dir.is_dir():
        return []
    issues: list[str] = []
    for entry in sorted(vscode_dir.iterdir(), key=lambda p: p.name):
        name = entry.name
        if any(fnmatch.fnmatch(name, pat) for pat in vscode_clause_forbidden):
            issues.append(f".vscode/{name} is per-developer or machine state "
                          f"(vscode.dir_forbidden)")
        elif name not in vscode_clause_allowed:
            issues.append(f".vscode/{name} is not shared editor configuration "
                          f"(vscode.dir_allowed)")
    return issues


def check_workspace_settings(repo_path: Path) -> list[Finding]:
    """Dot-prefixed .code-workspace carrying required sort settings (ADR-59 D3).

    FAIL if absent or unparseable, or if the shape spec cannot be read or claims a sorting
    assertion this module does not make; WARN if present but off the spec's workspace glob,
    a required setting is missing/wrong, or `.vscode/` carries a member the spec's `vscode`
    clause does not admit; PASS otherwise.

    The `vscode` and `sorting` clauses are read HERE, at call time, from
    `validate_hermetization.SHAPE_SPEC` — see the module docstring for why that is the
    attribute rather than a `from`-import.
    """
    try:
        clauses = _vh.SHAPE_SPEC
        ws_glob = _vh._clause_str(clauses, "vscode", "workspace_file_glob")
        dir_allowed = _vh._clause_list(clauses, "vscode", "dir_allowed")
        dir_forbidden = _vh._clause_list(clauses, "vscode", "dir_forbidden")
        sort_setting = _vh._clause_str(clauses, "sorting", "asserted_by_setting")
    except _vh.ShapeSpecError as e:
        return [Finding("workspace_settings", "fail",
                        f"fleet shape spec clause unreadable: {e}")]

    # The sorting clause names the ONE setting that delivers its asserted half. If that key
    # is not among the settings this module requires, the clause is claiming an assertion
    # nobody makes — the decorative shape the reader census exists to end, and a spec defect
    # rather than a repo defect, so it refuses instead of warning about the tree.
    if sort_setting not in _WORKSPACE_REQUIRED_SETTINGS:
        return [Finding("workspace_settings", "fail",
                        f"shape spec `sorting.asserted_by_setting` is {sort_setting!r}, "
                        f"which this check does not require — the clause claims an "
                        f"assertion no organ makes")]

    workspaces = sorted(p for p in repo_path.iterdir()
                        if p.is_file() and p.name.endswith(".code-workspace"))
    if not workspaces:
        return [Finding("workspace_settings", "fail",
                        "No .code-workspace file at repo root")]

    ws = workspaces[0]
    try:
        data = json.loads(_strip_jsonc(ws.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValueError) as e:
        return [Finding("workspace_settings", "fail",
                        f"{ws.name} is not parseable JSON(C): {e}")]

    issues = []
    # Discovery stays broad (`*.code-workspace`) and CONFORMANCE comes from the spec, so a
    # non-dot-prefixed file is found and reported rather than read as "no workspace at all".
    if not fnmatch.fnmatch(ws.name, ws_glob):
        issues.append(f"workspace file '{ws.name}' is not dot-prefixed "
                      f"(vscode.workspace_file_glob {ws_glob!r})")

    settings = data.get("settings", {})
    if not isinstance(settings, dict):
        settings = {}
    for key, expected in _WORKSPACE_REQUIRED_SETTINGS.items():
        actual = settings.get(key, "<absent>")
        if actual != expected:
            issues.append(f"{key}={actual!r} (expected {expected!r})")

    issues += _vscode_dir_issues(repo_path, dir_allowed, dir_forbidden)

    if issues:
        return [Finding("workspace_settings", "warn", f"{ws.name}: " + "; ".join(issues))]
    return [Finding("workspace_settings", "pass",
                    f"{ws.name} present, dot-prefixed, required sort settings correct "
                    f"({sort_setting} carries the sorting clause's asserted half), "
                    f".vscode/ in-pattern")]
