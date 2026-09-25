#!/usr/bin/env python
"""learning_distiller.py -- 5e v0: a batch's REFUSED / repair / FAILED / dispatcher-fault
receipts, turned into candidate rows with a runnable regression check (LANE-5B2-13).

THE GAP THIS CLOSES, stated in the contract's own words: "N1's two refusals and the
dispatcher's watcher fault were each fixed by hand and remembered by nobody." An
integrator's `REFUSED-<slug>.md` file and a dispatcher's `**HH:MM:SS DISPATCHER FAULT**`
marker already carry a title, a cause and a cure in prose -- this module reads that prose
and renders it as a candidate row a human or a filing lane can act on, instead of leaving
it to evaporate at the end of the session that found it.

LIBRARY-FIRST (O-12): regex + `pathlib` (stdlib) do the parsing; `click` is the CLI, already
an established dependency for this exact shape (`check_post_merge.py`, `batch_janitor.py`,
`lane_cost.py`) -- no new dependency. A markdown parser was not tried: the three source
shapes (a REFUSED file's two fixed headings, a `STATE ... FAILED` line, a `**DISPATCHER
FAULT**` marker) are narrow enough that a full parser would buy nothing a handful of
anchored regexes do not already give, and the fixtures pin the exact text those regexes
must survive.

RULING (a): this organ FILES NOTHING (ruling (h) reserves row filing to two named lanes).
It only emits candidate rows as text or JSON; turning a row into a `tasks/` file is a
separate, later act by whichever lane owns filing that day.

HONEST LIMITS:
  * A candidate row's regression check is DERIVED, not invented: a `repair` row's check is
    the `tests/*.py::test_*` node id(s) named in the REFUSED file's own "What failed"
    section, reduced to file scope. When none is named, the check says so rather than
    guessing a file that was never mentioned.
  * A `dispatcher_fault` row has no failing test to point at by construction -- the fault is
    a launcher/scripting defect, not a red test -- so its check names the regression test
    that does not exist yet (RED-first, ADR-108 §B), not a passing command today.
  * `find_failed_lanes` reads `STATE <slug> FAILED <sha>` lines; no batch fixture exercises
    it yet (N1 had no outright FAILED lane), so it is unit-tested against a synthetic
    string rather than pinned to a fixture.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import click

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


def _relpath(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(_REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# The candidate row -- the one shape every source below converges on
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CandidateRow:
    """One learning, ready to become a `tasks/` row (by a lane that owns filing).

    `kind` is one of `repair` (a REFUSED file whose lane went on to repair and merge),
    `failed` (a lane that ended `STATE ... FAILED`), or `dispatcher_fault` (a `**DISPATCHER
    FAULT**` marker in the dispatcher's own session file). `check` is always a single
    runnable command line -- a real one where the receipts named a failing test, a
    proposed-but-not-yet-written one otherwise (see module docstring).
    """

    kind: str
    slug: str
    title: str
    provenance: str
    check: str
    detail: str = ""

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "slug": self.slug,
            "title": self.title,
            "provenance": self.provenance,
            "check": self.check,
            "detail": self.detail,
        }

    def render(self) -> str:
        lines = [
            f"## candidate row: {self.kind} -- {self.slug}",
            f"title: {self.title}",
            f"provenance: {self.provenance}",
            f"check: {self.check}",
        ]
        if self.detail:
            lines.append(f"detail: {self.detail}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# REFUSED files -> `repair` rows
# ---------------------------------------------------------------------------

_REFUSED_HEADING_RE = re.compile(
    r"^#\s*REFUSED\s*[\u2014-]\s*(?P<slug>\S+?),\s*repair\s*(?P<n>\d+)\s*of\s*(?P<m>\d+)",
    re.M,
)
_FRONTMATTER_FROM_RE = re.compile(r"^from:\s*(.+)$", re.M)
_FRONTMATTER_BATCH_RE = re.compile(r"^batch:\s*(.+)$", re.M)
_FRONTMATTER_DATE_RE = re.compile(r"^date:\s*(.+)$", re.M)
_WHAT_FAILED_RE = re.compile(r"^##\s*What failed\s*$(?P<body>.*?)(?=^##\s|\Z)", re.M | re.S)
_FENCE_RE = re.compile(r"```.*?```", re.S)
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
# A concrete pytest node id: `tests/<...>.py::<test...>` -- the `::` is required so a bare
# prose mention of a test FILE (a suggestion, not a failure) is never mistaken for evidence.
_TEST_NODE_RE = re.compile(r"\btests/[\w./-]+\.py::[\w:\[\]./-]+")


def _test_files(text: str) -> list[str]:
    """Test files named by a concrete (`::`-qualified) node id, first-seen order."""
    out: list[str] = []
    for m in _TEST_NODE_RE.finditer(text):
        file = m.group(0).split("::", 1)[0]
        if file not in out:
            out.append(file)
    return out


def _title_from_what_failed(slug: str, body: str) -> str:
    """`<slug>: <first bold phrase outside a code fence>`, or a bare fallback."""
    stripped = _FENCE_RE.sub("", body)
    m = _BOLD_RE.search(stripped)
    phrase = " ".join(m.group(1).split()) if m else ""
    return f"{slug}: {phrase}" if phrase else f"{slug}: refused, cause not extractable"


def parse_refused(text: str, path: Path) -> Optional[CandidateRow]:
    """One `repair` row from a `REFUSED-<slug>.md` file's own `## What failed`."""
    heading = _REFUSED_HEADING_RE.search(text)
    if not heading:
        return None
    slug, n, m = heading.group("slug"), heading.group("n"), heading.group("m")
    from_m = _FRONTMATTER_FROM_RE.search(text)
    batch_m = _FRONTMATTER_BATCH_RE.search(text)
    date_m = _FRONTMATTER_DATE_RE.search(text)
    what_failed_m = _WHAT_FAILED_RE.search(text)
    body = what_failed_m.group("body").strip() if what_failed_m else ""

    test_files = _test_files(body)
    check = (f"uv run --locked pytest {' '.join(test_files)} -q" if test_files
             else f"# no `tests/*.py::test_*` node id found in {path.name}'s "
                  f"'What failed' -- name a regression check by hand")
    provenance = (
        f"{_relpath(path)} (from: {from_m.group(1).strip() if from_m else '?'}, "
        f"repair {n} of {m}, batch {batch_m.group(1).strip() if batch_m else '?'}, "
        f"{date_m.group(1).strip() if date_m else '?'})"
    )
    return CandidateRow(
        kind="repair", slug=slug, title=_title_from_what_failed(slug, body),
        provenance=provenance, check=check, detail=body[:600],
    )


# ---------------------------------------------------------------------------
# The integrator session -> `failed` rows (`STATE <slug> FAILED <sha>`)
# ---------------------------------------------------------------------------

_STATE_FAILED_RE = re.compile(r"^STATE\s+(?P<slug>\S+)\s+FAILED\s+(?P<sha>\S+)?", re.M)


def find_failed_lanes(text: str, path: Path) -> list[CandidateRow]:
    """One `failed` row per `STATE <slug> FAILED <sha>` line in an integrator session."""
    rows: list[CandidateRow] = []
    for m in _STATE_FAILED_RE.finditer(text):
        slug = m.group("slug")
        sha = m.group("sha") or "?"
        window_start = text.rfind("\n\n", 0, m.start())
        context = text[(window_start + 2 if window_start != -1 else 0):m.start()].strip()
        rows.append(CandidateRow(
            kind="failed", slug=slug, title=f"{slug}: lane FAILED at {sha}",
            provenance=f"{_relpath(path)} (STATE {slug} FAILED {sha})",
            check=f"# name the regression check for {slug}'s FAILED cause by hand",
            detail=context[-600:],
        ))
    return rows


# ---------------------------------------------------------------------------
# The dispatcher session -> `dispatcher_fault` rows (`**HH:MM:SS DISPATCHER FAULT**`)
# ---------------------------------------------------------------------------

_FAULT_MARKER_RE = re.compile(r"\*\*(?P<time>\d{2}:\d{2}(?::\d{2})?)\s+DISPATCHER FAULT\*\*")
_FAULT_MARKER_STRIP_RE = re.compile(
    r"\*\*\d{2}:\d{2}(?::\d{2})?\s+DISPATCHER FAULT\*\*\s*(?:\u2014|--)?\s*")
_LANE_TOKEN_RE = re.compile(r"`(lane-[\w-]+)`")
_REPAIR_SUFFIX_RE = re.compile(r"-repair-\d+[a-z]?$")
_SENTENCE_RE = re.compile(r"(.{20,220}?[.:;])(?:\s|$)")


def _bullet_block(lines: list[str], start: int) -> str:
    """The full bullet item containing `lines[start]`: itself plus every continuation
    line, stopping at the next sibling bullet (same or shallower indent), a blank line,
    or a heading."""
    indent = len(lines[start]) - len(lines[start].lstrip(" "))
    out = [lines[start]]
    for line in lines[start + 1:]:
        if not line.strip():
            break
        this_indent = len(line) - len(line.lstrip(" "))
        stripped = line.lstrip(" ")
        if stripped.startswith("- ") and this_indent <= indent:
            break
        if stripped.startswith("#"):
            break
        out.append(line)
    return "\n".join(out)


def _slug_from_fault_block(block: str) -> str:
    m = _LANE_TOKEN_RE.search(block)
    if not m:
        return "dispatcher"
    return _REPAIR_SUFFIX_RE.sub("", m.group(1))


def _title_from_fault_block(block: str) -> str:
    text = _FAULT_MARKER_STRIP_RE.sub("", block, count=1)
    text = re.sub(r"^\s*-\s*", "", text.strip())
    text = " ".join(text.split())
    m = _SENTENCE_RE.match(text)
    return (m.group(1) if m else text[:220]).strip()


def find_dispatcher_faults(text: str, path: Path) -> list[CandidateRow]:
    """One `dispatcher_fault` row per `**HH:MM:SS DISPATCHER FAULT**` marker."""
    lines = text.splitlines()
    rows: list[CandidateRow] = []
    for i, line in enumerate(lines):
        m = _FAULT_MARKER_RE.search(line)
        if not m:
            continue
        block = _bullet_block(lines, i)
        time = m.group("time")
        slug = _slug_from_fault_block(block)
        check = (f"uv run --locked pytest tests/test_dispatch_repair_launch.py -q  "
                 f"# proposed regression test (not yet written) for the {time} dispatcher fault")
        rows.append(CandidateRow(
            kind="dispatcher_fault", slug=slug, title=_title_from_fault_block(block),
            provenance=f"{_relpath(path)} @ {time} (DISPATCHER FAULT)",
            check=check, detail=block.strip()[:600],
        ))
    return rows


# ---------------------------------------------------------------------------
# Distill + render
# ---------------------------------------------------------------------------

def distill(integrator_path: Path, dispatcher_path: Path,
            refused_paths: Sequence[Path] = ()) -> list[CandidateRow]:
    """Every candidate row across one batch's receipts. Read-only."""
    rows: list[CandidateRow] = []
    for p in refused_paths:
        p = Path(p)
        row = parse_refused(p.read_text(encoding="utf-8", errors="replace"), p)
        if row is not None:
            rows.append(row)
    integrator_text = Path(integrator_path).read_text(encoding="utf-8", errors="replace")
    rows.extend(find_failed_lanes(integrator_text, Path(integrator_path)))
    dispatcher_text = Path(dispatcher_path).read_text(encoding="utf-8", errors="replace")
    rows.extend(find_dispatcher_faults(dispatcher_text, Path(dispatcher_path)))
    return rows


def render_rows(rows: Sequence[CandidateRow]) -> str:
    if not rows:
        return ("learning_distiller: no REFUSED, repair, FAILED or dispatcher-fault event "
                "found in the given receipts.")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.kind] = counts.get(r.kind, 0) + 1
    header = (f"learning_distiller: {len(rows)} candidate row(s) -- "
              + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    return header + "\n\n" + "\n\n".join(r.render() for r in rows)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group(context_settings={"help_option_names": ["-h", "--help"]},
             help="Turn a batch's REFUSED / repair / FAILED / dispatcher-fault receipts into "
                  "candidate rows with a runnable regression check. Emits only -- files nothing "
                  "(ruling h).")
def cli() -> None:
    pass


@cli.command("run")
@click.option("--integrator", "integrator_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="the integrator's SESSION-*.md")
@click.option("--dispatcher", "dispatcher_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="the dispatcher's SESSION-*.md")
@click.option("--refused", "refused_paths", multiple=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="a REFUSED-<slug>.md file; repeatable")
@click.option("--format", "fmt", type=click.Choice(["text", "json"]), default="text",
              show_default=True)
def cmd_run(integrator_path: Path, dispatcher_path: Path, refused_paths: tuple,
            fmt: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a piped Windows stdout is cp1252
    rows = distill(integrator_path, dispatcher_path, list(refused_paths))
    if fmt == "json":
        click.echo(json.dumps([r.to_dict() for r in rows], indent=2))
    else:
        click.echo(render_rows(rows))


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
