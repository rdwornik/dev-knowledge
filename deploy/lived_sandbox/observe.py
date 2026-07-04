"""Lived-workflow sandbox — the OUTER DETERMINISTIC OBSERVER (Slice B; [#252]).

Derives a verdict on a real ``branch->edit->commit->wrap`` arc from THREE EXTERNAL
channels only — and NEVER from the inner session's narration (C1; LESSONS 2026-06-04
"verify by state, never by agent narration"):

  1. hook-stdout    — STRUCTURED tool-result + system/hook event payloads. **[NB-2]:
                      event-type keyed, NOT a text-grep over the transcript blob — an
                      assistant *text* item (narration) is excluded from this channel, so
                      a model saying "floor hash OK" can never masquerade as a hook firing.
  2. git-state      — real ``git`` probes on the clone (branch/commit/file present).
  3. transcript-event — structured ``tool_use`` invocations (the >=1 command act, the edit).

Against the ``engages`` oracle it classifies each expectation and GATES only the deployed
mesh (the six firing hooks + the ruff tombstone); everything else is OBSERVED-not-gated
(watched + reported, never pass/fail — the operator's [#252] ruling). ``passed`` is true iff
every gated firing hook FIRED and every gated tombstone is CORRECTLY-ABSENT.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from . import oracle as _oracle

# Verdicts.
FIRED = "FIRED"
SILENT = "EXPECTED-BUT-SILENT"          # a gated firing hook that did not fire — the C4 catch
UNEXPECTED = "UNEXPECTED"               # a must-be-absent tombstone that fired (prune regression)
ABSENT_OK = "CORRECTLY-ABSENT"          # a gated tombstone that did not fire (prune conformance)
OBSERVED = "OBSERVED"                   # non-gated, signal present
NOT_OBSERVED = "NOT-OBSERVED"           # non-gated, signal absent

_GATED_OK = frozenset({FIRED, ABSENT_OK})
_GATED_FLAG = frozenset({SILENT, UNEXPECTED})


# ---------------------------------------------------------------------------
# Channel extraction — the heart of C1 / [NB-2]. Assistant narration NEVER enters
# the hook-stdout or git-state channels; only structured, externally-produced text.
# ---------------------------------------------------------------------------


def _stringify(content: object) -> str:
    """A tool_result's content is a string or a list of {type,text} blocks — flatten to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text", item.get("content", ""))))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(content, dict):
        return str(content.get("text", content.get("content", "")))
    return "" if content is None else str(content)


def _message(ev: dict) -> dict:
    m = ev.get("message")
    return m if isinstance(m, dict) else ev


def _role(ev: dict) -> str:
    return str(_message(ev).get("role") or ev.get("role") or ev.get("type") or "")


def hook_stdout_surface(events: list[dict]) -> str:
    """Concatenate ONLY externally-produced text: tool_result contents + system/hook/result
    stdout. Assistant *text* content items are EXCLUDED — narration is not evidence ([NB-2])."""
    parts: list[str] = []
    for ev in events:
        role = _role(ev)
        content = _message(ev).get("content")
        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                itype = item.get("type")
                if itype == "tool_result":
                    parts.append(_stringify(item.get("content")))
                # type == "text" (assistant/user prose) is narration -> skip.
                # type == "tool_use" is a command/edit -> the transcript-event channel, not here.
        elif isinstance(content, str) and role not in ("assistant",):
            # A bare-string system/hook/user payload (non-assistant) is external stdout.
            parts.append(content)
        # Top-level hook/system stdout fields (some event shapes surface hook output here).
        if ev.get("type") in ("system", "hook", "result"):
            for k in ("stdout", "output", "hookOutput", "result"):
                v = ev.get(k)
                if isinstance(v, str):
                    parts.append(v)
    return "\n".join(parts)


def tool_use_surface(events: list[dict]) -> str:
    """Structured tool_use invocations (names + inputs) — the transcript-event channel for
    observing the >=1 command act and the edit. Not narration: these are machine records of
    what the session DID, keyed by content type == tool_use."""
    parts: list[str] = []
    for ev in events:
        content = _message(ev).get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    parts.append(str(item.get("name", "")))
                    parts.append(json.dumps(item.get("input", ""), default=str))
    return "\n".join(parts)


def events_from_spawn(result) -> list[dict]:
    """Unify a SpawnResult's evidence into one event list: the stdout stream-json events plus
    every line of the on-disk transcript jsonl (parsed structurally, not blob-concatenated)."""
    events: list[dict] = list(getattr(result, "events", None) or [])
    proj = Path(result.config_dir) / "projects"
    if proj.exists():
        for jsonl in proj.rglob("*.jsonl"):
            for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return events


# ---------------------------------------------------------------------------
# git-state channel — real git probes on the clone (corroborates the arc happened).
# ---------------------------------------------------------------------------


def _git(clone: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603 — fixed argv, no shell
        ["git", *args], cwd=str(clone), capture_output=True, text=True)


def branch_exists(clone: Path, branch: str) -> bool:
    return _git(clone, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0


def head_commit(clone: Path) -> str | None:
    r = _git(clone, "rev-parse", "--verify", "--quiet", "HEAD")
    return r.stdout.strip() or None if r.returncode == 0 else None


def file_in_head(clone: Path, path: str) -> bool:
    return _git(clone, "cat-file", "-e", f"HEAD:{path}").returncode == 0


def path_present(clone: Path, path: str) -> bool:
    return (Path(clone) / path).exists()


# ---------------------------------------------------------------------------
# Classification.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Finding:
    component_id: str
    gated: bool
    verdict: str
    channel: str
    evidence: str


def _classify(exp: _oracle.Expectation, *, hook_surface: str, event_surface: str,
              clone: Path | None) -> Finding:
    if exp.observable == "hook-stdout":
        present = exp.signature in hook_surface
        if exp.absent:  # tombstone / prune-conformance
            verdict = UNEXPECTED if present else ABSENT_OK
        else:
            verdict = FIRED if present else SILENT
        ev = f"{'found' if present else 'absent'} signature {exp.signature!r} in hook-stdout"
        return Finding(exp.component_id, exp.is_gated, verdict, "hook-stdout", ev)
    if exp.observable == "transcript-event":
        present = exp.signature in event_surface
        return Finding(exp.component_id, exp.is_gated,
                       OBSERVED if present else NOT_OBSERVED, "transcript-event",
                       f"{'found' if present else 'absent'} {exp.signature!r} in tool_use events")
    # git-state — best-effort file-presence over the clone (observed-only; never gated).
    present = False
    if clone is not None:
        token = exp.signature.split()[0] if exp.signature.split() else exp.signature
        present = path_present(clone, token) or file_in_head(clone, token)
    return Finding(exp.component_id, exp.is_gated,
                   OBSERVED if present else NOT_OBSERVED, "git-state",
                   f"{'present' if present else 'absent'} {exp.signature!r} in clone")


@dataclass(frozen=True)
class ObservationResult:
    findings: tuple[Finding, ...]

    @property
    def gated_findings(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.gated)

    @property
    def flags(self) -> tuple[Finding, ...]:
        """The gated failures: a should-fire hook that was SILENT, or a tombstone that fired."""
        return tuple(f for f in self.gated_findings if f.verdict in _GATED_FLAG)

    @property
    def silences(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.gated_findings if f.verdict == SILENT)

    @property
    def observed_not_gated(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if not f.gated)

    @property
    def commands_observed(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings
                     if f.channel == "transcript-event" and f.verdict == OBSERVED)

    @property
    def passed(self) -> bool:
        """Every gated firing hook FIRED and every gated tombstone is CORRECTLY-ABSENT.
        A single SILENT or UNEXPECTED gated finding fails the verdict (no false-green)."""
        gated = self.gated_findings
        return bool(gated) and all(f.verdict in _GATED_OK for f in gated)

    def summary(self) -> str:
        verdict = "GREEN" if self.passed else "FLAGGED"
        flagged = ", ".join(f"{f.component_id}:{f.verdict}" for f in self.flags) or "none"
        return (f"observer {verdict}: {len(self.gated_findings)} gated "
                f"({sum(f.verdict in _GATED_OK for f in self.gated_findings)} ok), "
                f"flags: {flagged}; commands observed: {len(self.commands_observed)}")


def observe(events: list[dict], oracle: _oracle.Oracle, *, clone: Path | None = None
            ) -> ObservationResult:
    """Classify every oracle expectation against the external channels. Deterministic;
    reads only structured events + git-state, never inner narration (C1)."""
    hook_surface = hook_stdout_surface(events)
    event_surface = tool_use_surface(events)
    findings = tuple(
        _classify(exp, hook_surface=hook_surface, event_surface=event_surface, clone=clone)
        for exp in oracle.expectations
    )
    return ObservationResult(findings=findings)


def observe_spawn(result, oracle: _oracle.Oracle, *, clone: Path | None = None
                  ) -> ObservationResult:
    """Observe a live SpawnResult (extracts structured events from it, then observe())."""
    return observe(events_from_spawn(result), oracle, clone=clone)


# Keep the deploy dir importable when run as a script (mirrors spawn.py's path shim).
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
