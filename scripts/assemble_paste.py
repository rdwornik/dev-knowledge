#!/usr/bin/env python3
"""Assemble PASTE_THIS.md from a v5 handoff bundle's canonical sources.

Usage: python scripts/assemble_paste.py <bundle_dir>

Manifest (in order):
  0. <bundle>/HANDOFF_BOOT.md session-header (optional; extracted from the bundle's
     own HANDOFF_BOOT.md up to the first '##' heading — slug/mode/purpose/generated-at)
  1. protocols/HANDOFF_BOOT.md  (required — browser role file + boot line)
  2. <bundle>/RESIDUAL.md       (required — drift-flags + planning why + task-graph)
  3. <bundle>/PROBES.md         (required — orientation + teeth probes)
  4. <bundle>/SUPPLEMENT.md     (architect's outgoing strategic brief — the v5.1
     interview answers; expected in architect mode [warn if absent], optional otherwise)

Output: <bundle>/PASTE_THIS.md  (UTF-8, LF, never hand-edited)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import click

_SECTION_SEP = "\n\n---\n\n"


def _extract_session_header(text: str) -> str:
    """Return the session-header block from a bundle HANDOFF_BOOT.md.

    Extracts everything up to (but not including) the first '## ' heading —
    the title line, scope comment, and the Field/Value table. Strips trailing
    whitespace so the block ends cleanly.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        if re.match(r"^## ", line):
            break
        out.append(line)
    return "".join(out).rstrip()


_MODE_RE = re.compile(
    r"(?im)^\|\s*\*{0,2}mode\*{0,2}\s*\|\s*\*{0,2}(architect|execution)\b")


def _extract_mode(text: str) -> str | None:
    """Return the handoff mode ('architect' | 'execution') from a bundle HANDOFF_BOOT.md.

    Parses the `| **Mode** | **architect** ... |` row of the session-header Field/Value
    table (the row v5 §13 bundles emit). Returns the lowercased mode, or None when no
    parseable Mode row is present — the caller then treats the bundle as non-architect
    (the supplement stays a silent [skip], the pre-v5.1 behaviour).
    """
    m = _MODE_RE.search(text)
    return m.group(1).lower() if m else None


@click.command()
@click.argument("bundle_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def main(bundle_dir: Path) -> None:
    """Assemble PASTE_THIS.md for BUNDLE_DIR from canonical sources."""
    repo_root = Path(__file__).parent.parent

    sections: list[tuple[str, str]] = []

    # 0. Optional: bundle session-header (slug/mode/purpose/generated-at). The Mode row
    #    also drives the architect-mode supplement expectation in the manifest loop below.
    mode: str | None = None
    bundle_boot = bundle_dir / "HANDOFF_BOOT.md"
    if bundle_boot.exists():
        boot_text = bundle_boot.read_text(encoding="utf-8")
        mode = _extract_mode(boot_text)
        header = _extract_session_header(boot_text)
        if header:
            sections.append(("HANDOFF_BOOT.md (session header)", header))

    # Manifest: (label, path, required)
    manifest: list[tuple[str, Path, bool]] = [
        ("protocols/HANDOFF_BOOT.md", repo_root / "protocols" / "HANDOFF_BOOT.md", True),
        ("RESIDUAL.md", bundle_dir / "RESIDUAL.md", True),
        ("PROBES.md", bundle_dir / "PROBES.md", True),
        ("SUPPLEMENT.md", bundle_dir / "SUPPLEMENT.md", False),
    ]

    for label, path, required in manifest:
        if not path.exists():
            if not required:
                # Architect mode expects the v5.1 strategic supplement; warn (non-fatal —
                # the supplement is advisory). Any other mode keeps the silent [skip].
                if label == "SUPPLEMENT.md" and mode == "architect":
                    click.echo(
                        f"[warn] {label} not found — architect mode expects the v5.1 "
                        "strategic supplement (interview answers); assembling without it",
                        err=True)
                else:
                    click.echo(f"[skip] {label} not found — no supplement section", err=True)
                continue
            click.echo(f"[error] Required source missing: {path}", err=True)
            sys.exit(1)
        sections.append((label, path.read_text(encoding="utf-8").rstrip()))

    body = _SECTION_SEP.join(f"=== {label} ===\n\n{content}" for label, content in sections)
    paste_path = bundle_dir / "PASTE_THIS.md"
    paste_path.write_text(body + "\n", encoding="utf-8", newline="\n")
    click.echo(f"Written: {paste_path}")


if __name__ == "__main__":
    main()
