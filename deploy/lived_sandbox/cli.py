"""Lived-workflow sandbox — Layer-2 operator CLI (Slice A).

    PYTHONPATH=deploy python -m lived_sandbox.cli prove-isolation [--freeze] [--haiku]

Runs the REAL isolated `claude -p` isolation proof and prints the verdict. `--freeze` copies the
captured transcripts into tests/fixtures/lived-workflow/ (secret-scrubbed) and appends a line to
logs/LIVED-WORKFLOW.md (the gitignored operator funnel). Exits NON-ZERO on a FAILED proof — a
facade must STOP, not be measured (Fable review §6). Requires ANTHROPIC_API_KEY in the env
(change #4); the child authenticates by key so its isolated config pulls in zero outer hooks.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from . import isolation as _iso
from . import spawn as _spawn

_REPO = Path(__file__).resolve().parent.parent.parent
_FIXTURES = _REPO / "tests" / "fixtures" / "lived-workflow"
_REPORT = _REPO / "logs" / "LIVED-WORKFLOW.md"
_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}")


def _scrub_check(text: str, label: str) -> None:
    if _SECRET_RE.search(text):
        raise _spawn.SandboxError(
            f"refusing to freeze {label}: it contains an 'sk-ant-' secret pattern "
            "(a transcript fixture must never carry a key)")


def _freeze(result: _iso.IsolationResult) -> list[str]:
    _FIXTURES.mkdir(parents=True, exist_ok=True)
    frozen: list[str] = []
    for src, name in ((result.transcriptA, "isolation-configA-sentinel.jsonl"),
                      (result.transcriptB, "isolation-configB-isolated.jsonl")):
        if src and Path(src).exists():
            text = Path(src).read_text(encoding="utf-8", errors="replace")
            _scrub_check(text, name)
            (_FIXTURES / name).write_text(text, encoding="utf-8", newline="\n")
            frozen.append(name)
    return frozen


def _append_report(result: _iso.IsolationResult, frozen: list[str]) -> None:
    _REPORT.parent.mkdir(parents=True, exist_ok=True)
    header = "" if _REPORT.exists() else "# Lived-workflow sandbox — operator funnel (gitignored)\n\n"
    line = (f"- isolation proof: {'PROVEN' if result.passed else 'FAILED'} — "
            f"configA-present={result.present_in_configA} (exit {result.exitA}) / "
            f"configB-absent={result.absent_in_configB} (exit {result.exitB}); "
            f"frozen: {', '.join(frozen) or 'none'}\n")
    with _REPORT.open("a", encoding="utf-8") as fh:
        fh.write(header + line)


def cmd_prove_isolation(freeze: bool, model: str) -> int:
    result = _iso.prove_isolation(model=model, keep=freeze)
    print(result.summary())
    try:
        if freeze:
            frozen = _freeze(result)
            _append_report(result, frozen)
            print(f"froze {len(frozen)} fixture(s): {', '.join(frozen)}  ->  {_FIXTURES}")
            print(f"report -> {_REPORT}")
    finally:
        if freeze:
            _spawn.teardown(result.tempdir)
    if not result.passed:
        print("ISOLATION NOT PROVEN — STOP: the sandbox would measure a facade, not the deployment.",
              file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] != "prove-isolation":
        print("usage: PYTHONPATH=deploy python -m lived_sandbox.cli prove-isolation [--freeze] [--haiku]",
              file=sys.stderr)
        return 2
    freeze = "--freeze" in argv
    model = "haiku" if "--haiku" in argv else _spawn.DEFAULT_MODEL
    return cmd_prove_isolation(freeze, model)


if __name__ == "__main__":
    raise SystemExit(main())
