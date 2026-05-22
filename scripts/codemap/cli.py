"""CLI entry point for the codemap generator tool (ADR-51)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .check import check_codemap
from .generator import generate_codemap

_START_MARKER = "<!-- CODEMAP:START -->"
_END_MARKER = "<!-- CODEMAP:END -->"


def _cmd_generate(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo_path).resolve()
    mermaid, warnings = generate_codemap(repo_path, args.source_root)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    if not args.write:
        print(mermaid, end="")
        return 0

    arch_file = repo_path / "ARCHITECTURE.md"
    if not arch_file.exists():
        print(f"error: ARCHITECTURE.md not found at {arch_file}", file=sys.stderr)
        return 2

    content = arch_file.read_text(encoding="utf-8")
    start_idx = content.find(_START_MARKER)
    end_idx = content.find(_END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print(
            f"error: CODEMAP markers not found in {arch_file}",
            file=sys.stderr,
        )
        return 3

    new_content = (
        content[: start_idx + len(_START_MARKER)]
        + "\n"
        + mermaid
        + content[end_idx:]
    )
    arch_file.write_text(new_content, encoding="utf-8")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo_path).resolve()
    code, output = check_codemap(repo_path, args.source_root)
    if output:
        print(output, end="")
    return code


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="codemap",
        description="Codemap generator for ARCHITECTURE.md (ADR-51)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen_p = sub.add_parser("generate", help="Generate Mermaid codemap")
    gen_p.add_argument("repo_path", help="Path to repository root")
    gen_p.add_argument("--source-root", default="src", help="Source root directory (default: src)")
    gen_p.add_argument("--write", action="store_true", help="Write output into ARCHITECTURE.md")
    gen_p.set_defaults(func=_cmd_generate)

    chk_p = sub.add_parser("check", help="Check ARCHITECTURE.md codemap freshness")
    chk_p.add_argument("repo_path", help="Path to repository root")
    chk_p.add_argument("--source-root", default="src", help="Source root directory (default: src)")
    chk_p.set_defaults(func=_cmd_check)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
