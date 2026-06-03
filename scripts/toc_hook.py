#!/usr/bin/env python3
"""pre-commit hook-source entry for the TOC tool (ADR-71).

Thin wrapper so `.pre-commit-hooks.yaml` can expose `scripts/toc/` as an
installable hook (`language: script`). Puts this script's own directory
(`scripts/`, inside the *cloned* hook repo when a consumer runs it) on
sys.path, then delegates to the real CLI — no check logic is duplicated here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from toc.cli import main  # noqa: E402

main()
