#!/usr/bin/env python
"""verify_handoff_probes.py — #163 read-only handoff-probe TEETH validator.

Structurally prove every probe in a v5 handoff bundle's PROBES.md *binds to live
state*, so a toothless probe cannot ship. RESOLVE-ONLY — never executes the probe
commands (operator ruling; Critical Rule #4 "Layer 2 never executes / read-only
validators only"; zero false positives). It reinterprets the manual gate's "CC runs
the command" as STRUCTURAL RESOLVABILITY of the command's targets.

The §10 ladder it mechanizes (HANDOFF_PROCESS.md §10 — degrade loudly), per probe:
  - any load-bearing cell empty (question / source / why / command)   -> FAIL (malformed)
  - NO file/anchor token AND a trivial (value-less) command           -> FAIL (toothless)
  - a named source/command-target file does not exist (ANY span)      -> FAIL (missing source)
  - a named source file exists but its `#`-anchor is reworded/moved   -> WARN anchor-missing
  - the command's lead executable is absent from PATH                 -> skipped (degraded)
  - well-formed, a binding token resolves (or value-bearing cmd), exe -> PASS
A FAIL is always STRUCTURAL (missing file / errored target / malformed / toothless row),
never a judgment of the probe's rationale — the "Why" column is checked for PRESENCE ONLY,
its content is never inspected (that stays the manual gate, HANDOFF_PROCESS §5).

Toothless rung (#207 / GAP-4): a resolve-only validator cannot give a probe teeth that
binds to NO resolvable target — a row with no file token (source OR any command span), no
source `#`-anchor, AND a trivial command (a bare exe / `exe subcommand` that asserts no
specific live value, e.g. `git rev-parse`) -> FAIL, never a silent PASS on "the tool is on
PATH". A no-token probe whose command IS value-bearing (`git rev-parse --short HEAD`,
`git status -sb`) keeps its teeth via the surfaced live value and is NOT failed here.

Parser notes: `split_row` treats `|` inside a backtick span as literal (the named
failure mode); columns are mapped by HEADER NAME (live tables carry a leading `#` id
column §5's 4-col example omits); command FILE-targets are resolved from ALL backtick
spans (so a broken path in a SECONDARY span is caught, not silent-passed — #207/GAP-4;
a non-path shorthand in a later span is harmless: `file_tokens` is precision-over-recall
and a real path resolves directly or via the unique-basename fallback), while the lead
executable + the triviality test read the FIRST span only.

Read-only (Layer-2, ADR-28/36): reads PROBES.md + resolves repo paths; writes nothing;
never orchestrates. The audit adapter (scripts/audit.py check_handoff_probes) maps a
FAIL to a gating Finding so /ship blocks; anchor-missing / skipped -> WARN.
"""

from __future__ import annotations

import os
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

    The lead executable and the triviality test (`_is_trivial_command`) read this span
    ALONE. Command FILE-target resolution, by contrast, scans ALL spans (see
    `_command_file_tokens`) so a broken path in a secondary span is caught (#207/GAP-4)."""
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

def _excluded(parts: tuple[str, ...]) -> bool:
    """True if any path segment is an excluded dir (VCS/vendor/worktree/archived/aborted)."""
    return any(p in _FALLBACK_EXCLUDE_DIRS or p.startswith("archive") for p in parts)


def _within_repo_file(repo_root: Path, p: Path) -> Path | None:
    """Return `p` IFF it resolves to a real FILE CONTAINED in repo_root and not under an
    excluded tree; else None. Containment (resolve + relative_to) blocks a `../` escape or
    a symlink whose target leaves the repo from binding a probe — applied to the literal
    path too, so a probe can't bind to an out-of-repo / excluded-dir file by naming it
    directly (only the unique-basename fallback may omit the dir prefix)."""
    try:
        rp = p.resolve()
        parts = rp.relative_to(repo_root.resolve()).parts
    except (ValueError, OSError):
        return None  # escapes repo_root (../, symlink target outside) or unresolvable
    if not rp.is_file() or _excluded(parts):
        return None
    return p


def _basename_matches(repo_root: Path, name: str) -> list[Path]:
    """Files named `name` under repo_root, PRUNING excluded dirs during the walk so
    .git/.claude(worktrees)/node_modules/archive*/aborted/in-progress are never descended
    (the costly full-tree walk skips the duplicate-bearing trees — correctness + cost)."""
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if not _excluded((d,))]
        if name in filenames:
            out.append(Path(dirpath) / name)
    return out


def _resolve_path(repo_root: Path, rel: str) -> Path | None:
    """Resolve a probe's file token to a real repo file, or None.

    Primary: the literal repo-relative path (`protocols/HANDOFF_PROCESS.md`). Fallback:
    a probe may name a uniquely-basenamed repo file WITHOUT its dir prefix (a real
    authoring style — source-cell `HANDOFF_PROCESS.md` for `protocols/HANDOFF_PROCESS.md`);
    resolve it IFF exactly one match survives. BOTH paths pass the same gate — contained
    in repo_root, is-a-file, not under an excluded tree (`_within_repo_file`) — so a probe
    cannot bind to a file outside the repo (`../x.md`), a non-file, or a duplicate under
    .git/.claude/node_modules/archive*/aborted/in-progress, even by naming it directly.
    Zero matches (a real miss) or >1 (genuinely ambiguous) -> None: teeth preserved."""
    direct = _within_repo_file(repo_root, repo_root / rel)
    if direct is not None:
        return direct
    hits = [m for m in _basename_matches(repo_root, Path(rel).name)
            if _within_repo_file(repo_root, m) is not None]
    return hits[0] if len(hits) == 1 else None


def _header_present(header: str, src_files: list[str], repo_root: Path) -> bool:
    """True if a markdown-header line `header` appears in any resolvable source file."""
    pat = re.compile(r"^" + re.escape(header) + r"(\s|$)", re.MULTILINE)
    for rel in src_files:
        p = _resolve_path(repo_root, rel)
        if p is not None and pat.search(p.read_text(encoding="utf-8")):
            return True
    return False


def _command_file_tokens(command_cell: str) -> list[str]:
    """File-path tokens from EVERY backtick span of a command cell (not just the first).

    Command-target resolution scans ALL spans so a broken path in a SECONDARY span is
    caught, not silent-passed (#207 / GAP-4): a probe like `cat X.md` … `ghost/Y.md` must
    FAIL on the dangling `ghost/Y.md`. A non-path shorthand in a later span (e.g.
    `audit.py health`) is harmless — `file_tokens` is precision-over-recall (real-extension
    paths only), so a real path either resolves (directly or via the unique-basename
    fallback) or is a genuine miss. The lead exe + triviality still read the FIRST span."""
    return [tok for span in backtick_spans(command_cell) for tok in file_tokens(span)]


# Introspection operands that surface NO state-specific value even when present: a
# version banner (tool exists) or an environment-constant predicate that is invariant in
# the probe's own execution context (`--is-inside-work-tree` is always true when a probe
# runs inside the repo). Earned-by-value (#207/GAP-4): operand PRESENCE alone is too weak
# a proxy — a command whose only operands are drawn from this set is still vacuous and
# must FAIL, not silent-PASS. Precision-over-recall: only these named flags are downgraded
# (a non-listed operand like `--short`/`-sb` keeps the command value-bearing).
_VACUOUS_OPERANDS = frozenset({
    "--version", "-v", "--help", "-h",
    "--is-inside-work-tree", "--is-inside-git-dir", "--is-bare-repository",
})


def _is_trivial_command(cmd: str) -> bool:
    """True if `cmd` (the first span) is 'trivial' — it surfaces NO specific live value,
    only that the tool/repo exists: a bare executable or `exe subcommand` with no further
    operand (`git rev-parse`, `pytest`), OR a command whose every operand beyond
    `exe subcommand` is a vacuous introspection flag (`git rev-parse --is-inside-work-tree`,
    `git --version`) — operand presence alone does not earn teeth (#207/GAP-4). A command
    carrying any state-specific operand surfaces a live value (`git rev-parse --short HEAD`,
    `git status -sb`, `git log | grep x`) and is NOT trivial. Used ONLY together with 'no
    binding token' to classify a toothless probe: a resolve-only validator cannot give such
    a probe teeth, so it must not silent-PASS on 'the tool is on PATH' alone."""
    tokens = cmd.split()
    if len(tokens) <= 2:
        return True
    # 3+ tokens, but earned-by-value: still trivial if every operand beyond the
    # `exe subcommand` lead is a known vacuous introspection flag (surfaces no live value).
    return all(t in _VACUOUS_OPERANDS for t in tokens[2:])


def _classify(probe: dict, repo_root: Path, bundle: str) -> ProbeResult:
    pid = probe["id"]
    # 1. malformed — any load-bearing cell empty (Why: presence only, never content).
    for col in _LOAD_BEARING:
        if not probe[col].strip():
            return ProbeResult(pid, "fail", f"malformed: empty {col} cell", bundle)
    # 2. command must ship a runnable `backtick`-delimited command (else nothing binds).
    cmd = first_span(probe["command"])
    if not cmd:
        # a non-empty command cell with no `backtick` span ships no runnable command —
        # nothing binds to live state -> malformed (never falls through to a silent PASS).
        return ProbeResult(pid, "fail",
                           "malformed: command cell has no `backtick`-delimited command", bundle)
    # Binding tokens: a file token (source OR any command span) or a source `#`-anchor.
    src_files = file_tokens(probe["source"])
    cmd_files = _command_file_tokens(probe["command"])
    src_anchors = header_tokens(probe["source"])
    # 3. toothless (#207/GAP-4) — NO binding token AND a trivial command resolves nothing in
    #    live state; a resolve-only validator can't give it teeth -> FAIL, never a silent
    #    PASS on 'git is on PATH'. The AND of both conditions (frozen contract): a no-token
    #    probe with a value-bearing command (`live git` + `git rev-parse --short HEAD`) keeps
    #    its teeth via the surfaced live value and is NOT failed here.
    if not (src_files or cmd_files or src_anchors) and _is_trivial_command(cmd):
        return ProbeResult(pid, "fail",
                           "toothless: no file/anchor token + trivial command "
                           "(binds to no resolvable live state)", bundle)
    # 4. missing source/target — source uses ALL spans; command now uses ALL spans too, so a
    #    broken path in a SECONDARY command span is caught (#207/GAP-4), not silent-passed.
    for rel in src_files + cmd_files:
        if _resolve_path(repo_root, rel) is None:
            return ProbeResult(pid, "fail", f"missing source/target: {rel}", bundle)
    # 5. anchor — a named `#`-header must resolve in a bound (existing) source file.
    for hdr in src_anchors:
        if not _header_present(hdr, src_files, repo_root):
            return ProbeResult(pid, "anchor-missing", f"anchor not found: {hdr}", bundle)
    # 6. tool absent -> skipped (degraded coverage visible, never a synthesized pass).
    exe = lead_exe(cmd)
    if exe and not _exe_available(exe):
        return ProbeResult(pid, "skipped", f"tool absent: {exe}", bundle)
    # 7. well-formed; a binding token resolves (or a value-bearing command); exe present.
    return ProbeResult(pid, "pass", "binds to live state", bundle)


# rule: handoff-probes-bind
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
