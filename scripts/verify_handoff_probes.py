#!/usr/bin/env python
"""verify_handoff_probes.py — #163 read-only handoff-probe TEETH validator.

Structurally prove every probe in a v5 handoff bundle's PROBES.md *binds to live
state*, so a toothless probe cannot ship. RESOLVE-ONLY — never executes the probe
commands (operator ruling; Critical Rule #4 "Layer 2 never executes / read-only
validators only"; zero false positives). It reinterprets the manual gate's "CC runs
the command" as STRUCTURAL RESOLVABILITY of the command's targets.

The §10 ladder it mechanizes (HANDOFF_PROCESS.md §10 — degrade loudly), per probe:
  - any load-bearing cell empty (question / source / why / command)   -> FAIL (malformed)
  - a named source/command-target file does not exist                 -> FAIL (missing source)
  - a named source file exists but its `#`-anchor is reworded/moved   -> WARN anchor-missing
  - the command's lead executable is absent from PATH                 -> skipped (degraded)
  - well-formed, every named file + anchor resolves, exe present      -> PASS
A FAIL is always STRUCTURAL (missing file / errored target / malformed row), never a
judgment of the probe's rationale — the "Why" column is checked for PRESENCE ONLY, its
content is never inspected (that stays the manual gate, HANDOFF_PROCESS §5).

Parser notes: `split_row` treats `|` inside a backtick span as literal (the named
failure mode); columns are mapped by HEADER NAME (live tables carry a leading `#` id
column §5's 4-col example omits); command targets come from the FIRST backtick span
only (a secondary span may hold a non-path shorthand that would false-FAIL), while
source-locator targets use ALL spans (the file often sits in the 2nd span).

Read-only (Layer-2, ADR-28/36): reads PROBES.md + resolves repo paths; writes nothing;
never orchestrates. The audit adapter (scripts/audit.py check_handoff_probes) maps a
FAIL to a gating Finding so /ship blocks; anchor-missing / skipped -> WARN.
"""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# A repo-relative file path token: optional dir segments + a name with a known ext.
_FILE_RE = re.compile(r"(?:[\w.-]+/)*[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1)")

# The four load-bearing columns a well-formed probe row must carry (non-empty).
_LOAD_BEARING = ("question", "source", "why", "command")

# Dirs excluded from the unique-basename fallback in _resolve_path: VCS internals,
# nested CC worktree checkouts (`.claude/worktrees/<name>/…` are full duplicate trees),
# vendored deps, and immutable/aborted/in-progress handoff bundles. A duplicate copy of
# a live file under any of these would otherwise create a false-ambiguity FAIL.
# `archive` is matched by prefix (archive/, archives/, archived-…); mirrors the bundle
# exclude set in audit.py (_BUNDLE_EXCLUDE_DIRS).
_FALLBACK_EXCLUDE_DIRS = {".git", ".claude", "node_modules", "aborted", "in-progress"}


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str   # the table's `#` column, e.g. "P2" (or "" when absent)
    status: str     # 'pass' | 'fail' | 'anchor-missing' | 'skipped'
    detail: str     # evidence (pipe-free)
    bundle: str     # bundle dir name


# --- extractors (pure) ------------------------------------------------------

def split_row(line: str) -> list[str]:
    """Split a markdown table row into cell strings, treating `|` inside a backtick
    code span as a literal (NOT a delimiter). Leading/trailing border pipes dropped."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_tick = False
    for ch in s:
        if ch == "`":
            in_tick = not in_tick
            buf.append(ch)
        elif ch == "|" and not in_tick:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def backtick_spans(text: str) -> list[str]:
    """Contents of every `...` inline code span, in order (backticks stripped)."""
    return [m.strip() for m in re.findall(r"`([^`]+)`", text)]


def first_span(text: str) -> str:
    """Contents of the FIRST backtick span (the canonical command), or "" if none.

    Command targets come from this span ALONE: a probe's verification cell may carry a
    secondary span (e.g. `audit.py health`, a root-relative shorthand that does not
    exist as a path) — resolving those would false-FAIL. Source-locators, by contrast,
    use ALL spans (the file often sits in the 2nd span: `ALL_CHECKS` in `scripts/audit.py`).
    """
    m = re.search(r"`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def file_tokens(text: str) -> list[str]:
    """Repo-relative file-path tokens in `text` (precision-over-recall: only tokens
    ending in a known source/doc extension — never bare symbols or command args)."""
    return _FILE_RE.findall(text)


def header_tokens(text: str) -> list[str]:
    """Backtick spans that are markdown headers (`## …`) — the anchors to resolve."""
    return [s for s in backtick_spans(text) if s.startswith("#")]


def lead_exe(command: str) -> str:
    """The lead executable of a command string (first whitespace token), or ""."""
    command = command.strip()
    return command.split()[0] if command else ""


def _exe_available(name: str) -> bool:
    """True if `name` resolves on PATH. Wrapped (not inlined) so tests can stub it."""
    return shutil.which(name) is not None


# --- probe-manifest table parser --------------------------------------------

def _is_table_row(line: str) -> bool:
    return line.strip().startswith("|")


def _is_separator(line: str) -> bool:
    s = line.strip()
    return bool(s) and set(s) <= set("|-: ")


def _map_columns(header: list[str]) -> dict | None:
    """Map a header row to column indices by NAME. Returns None unless all four
    load-bearing columns (question / source / why / command) are present."""
    cols: dict[str, int] = {}
    for idx, cell in enumerate(header):
        c = cell.lower()
        if "binds" in c and "source" not in cols:
            cols["source"] = idx
        elif "verif" in c and "command" not in cols:
            cols["command"] = idx
        elif "why" in c and "why" not in cols:
            cols["why"] = idx
        elif ("probe" in c or "question" in c) and "question" not in cols:
            cols["question"] = idx
        elif c.strip() == "#" and "id" not in cols:
            cols["id"] = idx
    if set(_LOAD_BEARING) <= cols.keys():
        return cols
    return None


def _row_to_probe(cells: list[str], cols: dict) -> dict:
    def get(key: str) -> str:
        idx = cols.get(key)
        return cells[idx] if idx is not None and idx < len(cells) else ""
    return {k: get(k) for k in ("id", "question", "source", "why", "command")}


def parse_probes(md_text: str) -> list[dict]:
    """Parse every probe-table row in a PROBES.md into mapped-field dicts.

    Handles multiple tables per file (P1 orientation + P2–P7 teeth) and skips any
    non-probe table (one whose header lacks the four load-bearing columns)."""
    rows: list[dict] = []
    lines = md_text.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        if _is_table_row(lines[i]) and i + 1 < n and _is_separator(lines[i + 1]):
            cols = _map_columns(split_row(lines[i]))
            i += 2  # past header + separator
            while i < n and _is_table_row(lines[i]):
                if cols is not None:
                    rows.append(_row_to_probe(split_row(lines[i]), cols))
                i += 1
            continue
        i += 1
    return rows


# --- classifier (the §10 ladder, resolve-only) ------------------------------

def _resolve_path(repo_root: Path, rel: str) -> Path | None:
    """Resolve a probe's file token to a real repo file, or None.

    Primary: the literal repo-relative path (`protocols/HANDOFF_PROCESS.md`). Fallback:
    a probe may name a uniquely-basenamed repo file WITHOUT its dir prefix (a real
    authoring style — source-cell `HANDOFF_PROCESS.md` for the file that lives at
    `protocols/HANDOFF_PROCESS.md`); resolve it IFF exactly one non-excluded file in the
    tree carries that basename. Zero matches (a real miss) or >1 (genuinely ambiguous,
    after excluding VCS/vendor/archived/aborted dirs) -> None, so teeth are preserved:
    a missing or ambiguous token still FAILs. Precision-over-recall."""
    direct = repo_root / rel
    if direct.exists():
        return direct
    name = Path(rel).name
    hits = [
        p for p in repo_root.rglob(name)
        if p.is_file()
        and not any(part in _FALLBACK_EXCLUDE_DIRS or part.startswith("archive")
                    for part in p.relative_to(repo_root).parts)
    ]
    return hits[0] if len(hits) == 1 else None


def _header_present(header: str, src_files: list[str], repo_root: Path) -> bool:
    """True if a markdown-header line `header` appears in any resolvable source file."""
    pat = re.compile(r"^" + re.escape(header) + r"(\s|$)", re.MULTILINE)
    for rel in src_files:
        p = _resolve_path(repo_root, rel)
        if p is not None and pat.search(p.read_text(encoding="utf-8")):
            return True
    return False


def _classify(probe: dict, repo_root: Path, bundle: str) -> ProbeResult:
    pid = probe["id"]
    # 1. malformed — any load-bearing cell empty (Why: presence only, never content).
    for col in _LOAD_BEARING:
        if not probe[col].strip():
            return ProbeResult(pid, "fail", f"malformed: empty {col} cell", bundle)
    # 2. missing source/target — source uses ALL spans; command the FIRST span only.
    cmd = first_span(probe["command"])
    for rel in file_tokens(probe["source"]) + file_tokens(cmd):
        if _resolve_path(repo_root, rel) is None:
            return ProbeResult(pid, "fail", f"missing source/target: {rel}", bundle)
    # 3. anchor — a named `#`-header must resolve in a bound (existing) source file.
    src_files = file_tokens(probe["source"])
    for hdr in header_tokens(probe["source"]):
        if not _header_present(hdr, src_files, repo_root):
            return ProbeResult(pid, "anchor-missing", f"anchor not found: {hdr}", bundle)
    # 4. tool absent -> skipped (degraded coverage visible, never a synthesized pass).
    exe = lead_exe(cmd)
    if exe and not _exe_available(exe):
        return ProbeResult(pid, "skipped", f"tool absent: {exe}", bundle)
    # 5. well-formed; every named file + anchor resolves; exe present.
    return ProbeResult(pid, "pass", "binds to live state", bundle)


def verify(bundle_path, repo_root=None) -> list[ProbeResult]:
    """Classify every probe in <bundle_path>/PROBES.md. Read-only; resolve-only.

    `repo_root` defaults to the repo containing the bundle (<repo>/docs/handoffs/<slug>
    -> parents[2]); pass it explicitly to resolve against a different root. Returns []
    when the bundle has no PROBES.md (a non-v5 bundle)."""
    bundle_path = Path(bundle_path)
    if repo_root is None:
        parents = bundle_path.parents
        repo_root = parents[2] if len(parents) >= 3 else bundle_path
    repo_root = Path(repo_root)
    probes_file = bundle_path / "PROBES.md"
    if not probes_file.exists():
        return []
    md = probes_file.read_text(encoding="utf-8")
    return [_classify(p, repo_root, bundle_path.name) for p in parse_probes(md)]


def format_findings(results: list[ProbeResult]) -> str:
    """One flat line per FAILing probe (markdown-table-safe — no `|`)."""
    parts = [f"{r.probe_id}: {r.detail}" for r in results if r.status == "fail"]
    return "; ".join(parts).replace("|", "/")


def main(argv=None) -> int:
    """Standalone CLI: `python scripts/verify_handoff_probes.py <bundle-dir>`.
    Prints per-probe status; exits 1 if any probe FAILs, else 0."""
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: python scripts/verify_handoff_probes.py <bundle-dir>", file=sys.stderr)
        return 2
    bundle = Path(argv[0])
    results = verify(bundle)
    if not results:
        print(f"verify_handoff_probes: no probes found in {bundle}")
        return 0
    for r in results:
        print(f"  {r.status:>14}  {r.probe_id or '-':<5} {r.detail}")
    fails = sum(1 for r in results if r.status == "fail")
    warns = sum(1 for r in results if r.status in ("anchor-missing", "skipped"))
    passes = sum(1 for r in results if r.status == "pass")
    print(f"verify_handoff_probes: {len(results)} probe(s) — "
          f"{passes} pass, {fails} fail, {warns} warn ({bundle.name})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
