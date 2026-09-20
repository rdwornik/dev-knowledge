#!/usr/bin/env python
"""stage_prior_art.py -- spine stage 2 (prior-art): search our own archive before we pay for an answer twice.

WHY. RECON-NIGHT-2026-09-20 §3 read stage 2's old argv -- `git log --grep=<subject> -- tasks scripts
protocols` -- and found it searched commit MESSAGES over three code roots. It never looked at
`docs/audits/` or `docs/archive/`, which is where the answers re-bought seven times in two days were
sitting, and it never searched content. Stage 6 shows the sanctioned shape for a stage that outgrows
one line of argv: a click script with an `emit` verb, exit 0/1, run through `uv run --locked python`.
This module copies that shape and its conventions (module docstring with LIBRARY-FIRST and
ANTI-CLAIMS, `--root`, read-only, deterministic).

Two sources, three roots, nothing recursive over the repo:
  1. commit history, exactly as before -- the last 20 commits whose MESSAGE holds the subject, over
     the pathspec `tasks scripts protocols`;
  2. the CONTENT (and file names) of `docs/audits/` and `docs/archive/`.

Output is flat `key: value` lines (one stage output, captured by the wrapper into the receipt):
  prior-art: term=... / one `root` line per root / `found= shown= truncated= runtime_ms=`
  candidate: <path>:<line>: <snippet>            (a file)
  candidate: commit <sha>: <subject> [<path>]    (a commit; `git show <sha>` opens it)
  prior-art: NONE FOUND -- ...                   (nothing matched: names the roots, counts and term)
Nothing found is an ANSWER, so it exits 0 and says what ran. A search that could not run (git
missing, unreadable root) exits 1: "no prior art" must never be a synonym for "did not look".

BOUNDS. At most `--limit` candidates per source (default 10); the header says how many matched and
whether it truncated. Its own runtime is printed; the wrapper records the wall time as well.

LIBRARY-FIRST, as a command and its output (2026-09-20):
  $ git ls-files docs/audits docs/archive | wc -l      ->  ~1,110 files, ~25 MB
  $ uv run --locked python scripts/stage_prior_art.py emit --subject <absent term>
                                                       ->  runtime_ms=1.3-1.7 s on this box
                                                           (git log 0.6 s + reading 1,250 files 0.6 s)
  stdlib `pathlib` + `str.lower` chosen over `git grep` (needs a second parse of `path:line:text`, and
  skips untracked files a lane has just written) and over `rg` (not a declared dependency). REJECTED:
  ranking, stemming or a model to "summarise" candidates -- the stage is deterministic, the reader
  judges relevance.

ANTI-CLAIMS. This proves the subject string was FOUND OR NOT FOUND in two archive roots and the
commit messages -- not that a hit is relevant, nor that a differently-worded record is absent. It is
a case-insensitive whole-phrase match; a subject spelled differently in the archive is a miss.

Layer-2 / read-only: reads the tree and `git log`, writes nothing.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import click

STAGE = 2

#: The archive roots whose CONTENT is searched, in output order.
CONTENT_ROOTS = ("docs/audits", "docs/archive")
#: The git leg is exactly the old stage 2: last N commits whose message holds the subject, over these paths.
GIT_PATHSPEC = ("tasks", "scripts", "protocols")
GIT_COMMITS = 20
DEFAULT_LIMIT = 10
_SNIPPET = 160


class SearchError(RuntimeError):
    """The search could not run. Distinct from 'nothing found', which is an answer."""


def _snippet(line: str) -> str:
    line = " ".join(line.split())
    return line if len(line) <= _SNIPPET else line[:_SNIPPET - 3] + "..."


def search_root(root: Path, sub: str, term: str) -> "tuple[int, list[tuple[str, int, str]]]":
    """Scan one content root. Returns (files scanned, [(path, line, snippet)] -- one per matching file).

    Line 0 means the match was on the file NAME only. Newest-first by name (the roots use
    date-slug names), so a truncated list keeps the most recent records."""
    base = root / sub
    needle = term.lower()
    needle_b = needle.encode("ascii") if needle.isascii() else None
    scanned, hits = 0, []
    for path in sorted((p for p in base.rglob("*") if p.is_file()), reverse=True):
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise SearchError(f"cannot read {path.relative_to(root).as_posix()}: {exc}") from exc
        if b"\x00" in data[:4096]:
            continue  # binary: not searchable text
        scanned += 1
        rel = path.relative_to(root).as_posix()
        # ASCII terms (the norm) test the raw bytes, so only a matching file is ever decoded.
        matched = needle_b in data.lower() if needle_b else needle in data.decode("utf-8", errors="replace").lower()
        if matched:
            text = data.decode("utf-8", errors="replace")
            for n, line in enumerate(text.splitlines(), 1):
                if needle in line.lower():
                    hits.append((rel, n, _snippet(line)))
                    break
        elif needle in rel.lower():
            hits.append((rel, 0, "(file name matches)"))
    return scanned, hits


def search_git(root: Path, term: str) -> "list[tuple[str, str, str]]":
    """The old stage 2, kept: [(sha, subject, first touched path)] for the last GIT_COMMITS matches."""
    cmd = ["git", "--no-pager", "log", "-n", str(GIT_COMMITS), "-i", "-F", f"--grep={term}",
           "--name-only", "--format=%x1e%h%x1f%s", "--", *GIT_PATHSPEC]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                              cwd=root)
    except OSError as exc:
        raise SearchError(f"git could not start: {exc}") from exc
    if proc.returncode != 0:
        raise SearchError(f"git log failed (exit {proc.returncode}): {proc.stderr.strip()[:200]}")
    commits = []
    for record in proc.stdout.split("\x1e")[1:]:
        head, _, files = record.partition("\n")
        sha, _, subject = head.partition("\x1f")
        touched = next((f for f in files.splitlines() if f.strip()), "")
        commits.append((sha.strip(), subject.strip(), touched.strip()))
    return commits


def emit_lines(root: Path, subject: str, limit: int) -> "list[str]":
    term = subject.strip()
    if not term:
        raise SearchError("an empty subject matches everything and proves nothing")
    started = time.perf_counter()
    commits = search_git(root, term)
    per_root: "list[tuple[str, int | None, list]]" = []
    for sub in CONTENT_ROOTS:
        if not (root / sub).is_dir():
            per_root.append((sub, None, []))  # absent: recorded, never counted as searched
            continue
        scanned, hits = search_root(root, sub, term)
        per_root.append((sub, scanned, hits))
    found = len(commits) + sum(len(h) for _, _, h in per_root)
    shown = min(len(commits), limit) + sum(min(len(h), limit) for _, _, h in per_root)
    ran = [f"git-log (last {GIT_COMMITS} commits, message match, over {' '.join(GIT_PATHSPEC)})"]
    lines = [f'prior-art: term="{term}" limit={limit} per source',
             f"prior-art: root git-log: searched last {GIT_COMMITS} commits over "
             f"{' '.join(GIT_PATHSPEC)}, found={len(commits)}"]
    for sub, scanned, hits in per_root:
        if scanned is None:
            lines.append(f"prior-art: root {sub} (absent, not searched)")
        else:
            lines.append(f"prior-art: root {sub}: searched {scanned} files, found={len(hits)}")
            ran.append(f"{sub} ({scanned} files, content and name)")
    truncated = shown < found
    runtime_ms = round((time.perf_counter() - started) * 1000)
    lines.append(f"prior-art: found={found} shown={shown} truncated={'yes' if truncated else 'no'} "
                 f"runtime_ms={runtime_ms}")
    for sub, scanned, hits in per_root:
        for path, line, snip in hits[:limit]:
            lines.append(f"candidate: {path}:{line}: {snip}" if line else f"candidate: {path} {snip}")
    for sha, subj, touched in commits[:limit]:
        lines.append(f"candidate: commit {sha}: {subj}" + (f" [{touched}]" if touched else ""))
    if not found:
        lines.append(f'prior-art: NONE FOUND -- the search ran over {"; ".join(ran)} for term "{term}"; '
                     "nothing matched. This is a recorded answer, not a skipped step.")
    return lines


@click.group(help="Spine stage 2 (prior-art). Exit 0 = the search ran (found or not); 1 = it could not run.")
def cli() -> None:
    pass


@cli.command("emit")
@click.option("--subject", envvar="HARNESS_SUBJECT", required=True, help="the contract's subject (phrase)")
@click.option("--root", default=".", type=click.Path(file_okay=False))
@click.option("--limit", default=DEFAULT_LIMIT, show_default=True, type=click.IntRange(min=1),
              help="max candidates per source")
def cmd_emit(subject: str, root: str, limit: int) -> None:
    """The stage-2 FILL: print the candidates, or the explicit negative, for SUBJECT."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a piped Windows stdout is cp1252
    try:
        click.echo("\n".join(emit_lines(Path(root).resolve(), subject, limit)))
    except SearchError as exc:
        click.echo(f"REFUSED [stage {STAGE}]: {exc}", err=True)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover -- CLI entry
    cli()
