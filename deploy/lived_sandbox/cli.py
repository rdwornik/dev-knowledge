"""Lived-workflow sandbox — Layer-2 operator CLI (Slice A + Slice B).

    PYTHONPATH=deploy python -m lived_sandbox.cli prove-isolation [--freeze] [--haiku]
    PYTHONPATH=deploy python -m lived_sandbox.cli observe-arc [--freeze] [--haiku] [--leg-e <hook_id>]

`prove-isolation` (Slice A): the REAL isolated `claude -p` isolation proof.
`observe-arc` (Slice B, [#252]): clone+consumer-shape the hub, run the six-hook
branch->edit->commit->wrap arc, evaluate GATE-0 (isolation-only, [MF-1]) and the OUTER
observer, and `--freeze` the transcript as tests/fixtures/lived-workflow/arc-green.jsonl
(or arc-silent.jsonl with `--leg-e`, which disables one gated hook to seed the C4 catch).

`--freeze` writes the captured transcript (secret-scrubbed, [MC-2]) + appends a line to
logs/LIVED-WORKFLOW.md (the gitignored operator funnel). GATE-0 failure STOPs non-zero — a
facade must never be measured (Fable §6). Requires ANTHROPIC_API_KEY in the env (the child
authenticates by key so its isolated config pulls in zero outer hooks). [MC-1]: the live
freeze is the first real key call — run it only on a rotated key.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from . import arc as _arc
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


_LEG_E_DEFAULT = "canonical_freshness"  # a pre-commit-stage gated hook — the cleanest silence


def _freeze_arc(run: _arc.ArcRun, name: str) -> str | None:
    """Scrub-check the REAL transcript ([MC-2]) then freeze it as the named fixture."""
    if not run.transcript_jsonl.strip():
        return None
    _FIXTURES.mkdir(parents=True, exist_ok=True)
    _scrub_check(run.transcript_jsonl, name)  # a key must never reach a committed fixture
    (_FIXTURES / name).write_text(run.transcript_jsonl, encoding="utf-8", newline="\n")
    return name


def _append_arc_report(run: _arc.ArcRun, frozen: str | None, leg_e: str | None) -> None:
    _REPORT.parent.mkdir(parents=True, exist_ok=True)
    header = "" if _REPORT.exists() else "# Lived-workflow sandbox — operator funnel (gitignored)\n\n"
    mode = f"leg-e:{leg_e}" if leg_e else "green"
    line = (f"- arc observe ({mode}): {run.gate.summary()}; observer "
            f"{'GREEN' if run.observation.passed else 'FLAGGED'} "
            f"(flags {[f.component_id for f in run.observation.flags] or 'none'}); "
            f"frozen: {frozen or 'none'}\n")
    with _REPORT.open("a", encoding="utf-8") as fh:
        fh.write(header + line)


def cmd_observe_arc(freeze: bool, model: str, leg_e: str | None) -> int:
    """Run the six-hook arc (GATE-0 + observer) and optionally freeze the fixture.

    GATE-0 gates the CLI (isolation must hold under real work, [MF-1]); on failure it STOPs
    non-zero and does NOT freeze — a facade is never measured. The observation VERDICT is
    reported but does NOT gate the exit: a --leg-e run is EXPECTED to observe FLAGGED (that
    is the seeded silence C4 freezes)."""
    run = _arc.run_arc(model=model, leg_e_hook_id=leg_e)
    print(run.gate.summary())
    print(run.observation.summary())
    if not run.gate.passed:
        print("GATE-0 FAILED — STOP: isolation unproven under real work; the observer is not "
              "trusted (do not freeze a facade).", file=sys.stderr)
        return 1
    name = "arc-silent.jsonl" if leg_e else "arc-green.jsonl"
    if freeze:
        frozen = _freeze_arc(run, name)
        _append_arc_report(run, frozen, leg_e)
        print(f"froze {frozen or 'nothing (empty transcript)'}  ->  {_FIXTURES}")
        print(f"report -> {_REPORT}")
    return 0


def _leg_e_target(argv: list[str]) -> str | None:
    """--leg-e <hook_id> (or bare --leg-e -> the default gated hook). None when absent."""
    if "--leg-e" not in argv:
        return None
    i = argv.index("--leg-e")
    nxt = argv[i + 1] if i + 1 < len(argv) else ""
    return nxt if nxt and not nxt.startswith("--") else _LEG_E_DEFAULT


_USAGE = ("usage: PYTHONPATH=deploy python -m lived_sandbox.cli "
          "{prove-isolation | observe-arc} [--freeze] [--haiku] [--leg-e <hook_id>]")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in ("prove-isolation", "observe-arc"):
        print(_USAGE, file=sys.stderr)
        return 2
    freeze = "--freeze" in argv
    model = "haiku" if "--haiku" in argv else _spawn.DEFAULT_MODEL
    if argv[0] == "prove-isolation":
        return cmd_prove_isolation(freeze, model)
    return cmd_observe_arc(freeze, model, _leg_e_target(argv))


if __name__ == "__main__":
    raise SystemExit(main())
