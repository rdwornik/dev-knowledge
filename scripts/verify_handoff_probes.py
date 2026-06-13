#!/usr/bin/env python
"""verify_handoff_probes.py — #163 read-only handoff-probe TEETH validator.

STUB (step 1 / #163): signatures + dataclass only so the test matrix collects and
goes red. The parser (step 2) and the §10 classifier (step 3) replace these bodies.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str   # the table's `#` column, e.g. "P2" (or "" when absent)
    status: str     # 'pass' | 'fail' | 'anchor-missing' | 'skipped'
    detail: str     # evidence (pipe-free)
    bundle: str     # bundle dir name


# --- extractors (pure; step 2) ----------------------------------------------

def split_row(line: str) -> list[str]:
    raise NotImplementedError


def backtick_spans(text: str) -> list[str]:
    raise NotImplementedError


def first_span(text: str) -> str:
    raise NotImplementedError


def file_tokens(text: str) -> list[str]:
    raise NotImplementedError


def header_tokens(text: str) -> list[str]:
    raise NotImplementedError


def lead_exe(command: str) -> str:
    raise NotImplementedError


def _exe_available(name: str) -> bool:
    raise NotImplementedError


def parse_probes(md_text: str) -> list[dict]:
    raise NotImplementedError


# --- classifier (step 3) ----------------------------------------------------

def verify(bundle_path, repo_root=None) -> list[ProbeResult]:
    raise NotImplementedError


def format_findings(results: list[ProbeResult]) -> str:
    raise NotImplementedError


def main(argv=None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
