"""CLI entry point for the auto-TOC tool (mirrors scripts/codemap/cli.py).

Unlike the codemap (hardwired to ARCHITECTURE.md), the TOC tool takes the
target markdown file as an argument so the same mechanism can be applied to
any large canonical doc.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .check import check_toc
from .generator import generate_toc

_START_MARKER = "<!-- TOC:START -->"
_END_MARKER = "<!-- TOC:END -->"


def _cmd_generate(args: argparse.Namespace) -> int:
    md_file = Path(args.file).resolve()
    if not md_file.exists():
        print(f"error: file not found at {md_file}", file=sys.stderr)
        return 2

    try:
        toc = generate_toc(md_file)
    except OSError as exc:
        print(f"error: cannot read {md_file}: {exc}", file=sys.stderr)
        return 2

    if not args.write:
        print(toc, end="")
        return 0

    content = md_file.read_text(encoding="utf-8")
    start_idx = content.find(_START_MARKER)
    end_idx = content.find(_END_MARKER)
    if start_idx == -1 or end_idx == -1:
        print(f"error: TOC markers not found in {md_file}", file=sys.stderr)
        return 3

    new_content = (
        content[: start_idx + len(_START_MARKER)]
        + "\n"
        + toc
        + content[end_idx:]
    )
    try:
        md_file.write_text(new_content, encoding="utf-8", newline="\n")
    except OSError as exc:
        print(f"error: cannot write {md_file}: {exc}", file=sys.stderr)
        return 2
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    md_file = Path(args.file).resolve()
    code, output = check_toc(md_file)
    if output:
        print(output, end="")
    return code


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="toc",
        description="Auto-TOC generator for large canonical docs (mirrors codemap, ADR-51)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen_p = sub.add_parser("generate", help="Generate a nested anchor-link TOC")
    gen_p.add_argument("file", help="Path to the markdown file")
    gen_p.add_argument("--write", action="store_true", help="Write output between TOC markers in the file")
    gen_p.set_defaults(func=_cmd_generate)

    chk_p = sub.add_parser("check", help="Check a markdown file's TOC freshness")
    chk_p.add_argument("file", help="Path to the markdown file")
    chk_p.set_defaults(func=_cmd_check)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
