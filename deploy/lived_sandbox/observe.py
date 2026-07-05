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
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from . import oracle as _oracle

# Verdicts.
FIRED = "FIRED"
SILENT = "EXPECTED-BUT-SILENT"          # a gated firing hook that did not fire — the C4 catch
SKIPPED_ARMED = "ARMED-BUT-SKIPPED"     # G4a: pre-commit reported the hook but Skipped it —
#   wired + consulted (enforcing for its file scope), yet the check did NOT execute on this
#   commit; counted ok, never conflated with FIRED (measurement-#2 root ruling: a skip
#   name-echo must not inflate the FIRED reading).
UNEXPECTED = "UNEXPECTED"               # a must-be-absent tombstone that fired (prune regression)
ABSENT_OK = "CORRECTLY-ABSENT"          # a gated tombstone that did not fire (prune conformance)
VACUOUS = "VACUOUS"                     # G4b: a tombstone whose stage never ran — absence proves
#   nothing (no commit was attempted, so the hook never had the chance to appear).
OBSERVED = "OBSERVED"                   # non-gated, signal present
NOT_OBSERVED = "NOT-OBSERVED"           # non-gated, signal absent

_GATED_OK = frozenset({FIRED, ABSENT_OK, SKIPPED_ARMED})
# VACUOUS is a gated failure class (Codex MED 2026-07-06): `passed` already fails on it,
# and `flags` must SURFACE it — an unproven tombstone silently missing from the flag list
# would print "FLAGGED ... flags: none" for the exact failure G4 added.
_GATED_FLAG = frozenset({SILENT, UNEXPECTED, VACUOUS})

# G4a: pre-commit prints a hook's NAME even when it Skipped it (files-filter miss) — a line
# is a skip-echo, not execution evidence, when it matches PRE-COMMIT'S REPORT SHAPE: the
# dot-leader + "(no files to check)" / a dot-leader ending in the Skipped trailer. Codex
# HIGH 2026-07-06: anchored to that shape so a NON-pre-commit hook whose real output merely
# ends with the word "Skipped" is never soft-classified.
_SKIP_ECHO_RE = re.compile(r"\(no files to check\)|\.{4,}.*Skipped\s*$")
# G4b: evidence the pre-commit stage ran at all — ONLY pre-commit's per-hook report shape
# (dot-leader + Passed/Failed/Skipped trailer) counts. Codex HIGH 2026-07-06: a bare
# "...Passed" in unrelated Bash output must not fake the stage into having run.
_STAGE_RAN_RE = re.compile(r"\.{4,}.*(Passed|Failed|Skipped)\s*$", re.MULTILINE)


def signature_lines(surface: str, signature: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split the surface lines carrying `signature` into (executed, skip_echo) — the G4a
    discriminator between a hook that RAN and one pre-commit merely reported as Skipped.
    Skip-echo semantics are pre-commit report semantics: the CALLER applies the skipped
    bucket only to pre-commit-stage expectations (Codex HIGH 2026-07-06)."""
    executed: list[str] = []
    skipped: list[str] = []
    for ln in surface.splitlines():
        if signature in ln:
            (skipped if _SKIP_ECHO_RE.search(ln) else executed).append(ln)
    return tuple(executed), tuple(skipped)


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


def _bash_tool_use_ids(events: list[dict]) -> set:
    """The tool_use ids of Bash invocations — the ONLY tool whose results can carry hook
    stdout (pre-commit prints into the `git commit` result). A Read/Grep result echoes
    repo CONTENT: witnessed at Step-7 leg-e, the child Read JOURNAL.md and the echo of a
    signature string false-FIRED a disabled hook ([#253c]'s content-echo variant)."""
    ids = set()
    for ev in events:
        content = _message(ev).get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use" \
                        and item.get("name") == "Bash":
                    ids.add(item.get("id"))
    return ids


def hook_stdout_surface(events: list[dict]) -> str:
    """Concatenate ONLY text that can carry hook stdout: Bash tool_result contents +
    hook-event payloads (attachment hook_* / top-level system/hook stdout). Assistant
    narration, stream-json `result` events ([#253b]), bare prompt strings, and non-Bash
    tool_results (file-read echoes of repo content) are ALL excluded ([NB-2])."""
    bash_ids = _bash_tool_use_ids(events)
    parts: list[str] = []
    for ev in events:
        if ev.get("type") == "result":
            # A stream-json result event's `result` field IS the child's final narration
            # ([#253b]) — C1 forbids it as evidence, so the whole event is excluded.
            continue
        content = _message(ev).get("content")
        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "tool_result" and item.get("tool_use_id") in bash_ids:
                    parts.append(_stringify(item.get("content")))
                # type == "text" (assistant/user prose) is narration -> skip.
                # type == "tool_use" is a command/edit -> the transcript-event channel, not here.
                # a non-Bash tool_result is a content echo (Read/Grep/Write ack) -> skip.
        # Top-level hook/system stdout fields (some event shapes surface hook output here).
        # NOT "result" events — excluded above ([#253b]: their `result` field is narration).
        if ev.get("type") in ("system", "hook"):
            for k in ("stdout", "output", "hookOutput", "result"):
                v = ev.get(k)
                if isinstance(v, str):
                    parts.append(v)
        # Attachment-wrapped hook events — the on-disk transcript shape for hook firings
        # (witnessed at Step-7: {"attachment": {"type": "hook_success", "stdout": ...}}).
        # Only hook_* attachment types, and NEVER the `command` field: a hook's command
        # line names its script path (e.g. session_end_backpressure.py), which would
        # self-match the signature without the hook producing any output.
        att = ev.get("attachment")
        if isinstance(att, dict) and str(att.get("type", "")).startswith("hook_"):
            # stdout/stderr/content ONLY — NEVER the command field. Witnessed at Step-7:
            # a hook that succeeds SILENTLY leaves no transcript record at all (every
            # logged hook_success carries output), so a command string can never be
            # execution evidence — matching it would fire on a mere config echo.
            for k in ("stdout", "stderr", "content"):
                v = att.get(k)
                if isinstance(v, str):
                    parts.append(v)
            # A blocking Stop hook's reason rides nested: attachment.blockingError
            # .blockingError (witnessed at Step-7). Take the MESSAGE only — the sibling
            # `command` key is config echo, excluded like every command field.
            be = att.get("blockingError")
            if isinstance(be, dict):
                be = be.get("blockingError")
            if isinstance(be, str):
                parts.append(be)
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
              clone: Path | None, precommit_ran: bool) -> Finding:
    if exp.observable == "hook-stdout":
        executed, skipped = signature_lines(hook_surface, exp.signature)
        if exp.trigger != "pre-commit":
            # Skip-echo semantics exist only at the pre-commit stage (Codex HIGH
            # 2026-07-06): for session-start/stop hooks a matching line IS real output.
            executed, skipped = (*executed, *skipped), ()
        if exp.absent:  # tombstone / prune-conformance
            if executed or skipped:
                # A skip-echo still means the hook is WIRED — prune regression either way.
                verdict, ev = UNEXPECTED, (
                    f"found tombstone signature {exp.signature!r} in hook-stdout")
            elif exp.trigger == "pre-commit" and not precommit_ran:
                verdict, ev = VACUOUS, (
                    "no pre-commit stage output observed — absence proves nothing "
                    "(no commit attempted)")  # G4b
            else:
                verdict, ev = ABSENT_OK, f"absent signature {exp.signature!r} in hook-stdout"
        elif executed:
            verdict, ev = FIRED, f"found signature {exp.signature!r} in hook-stdout"
        elif skipped:
            verdict, ev = SKIPPED_ARMED, (
                f"pre-commit reported {exp.signature!r} but Skipped it "
                "(wired + consulted; file scope not exercised by this commit)")  # G4a
        else:
            verdict, ev = SILENT, f"absent signature {exp.signature!r} in hook-stdout"
        return Finding(exp.component_id, exp.is_gated, verdict, "hook-stdout", ev)
    if exp.observable == "transcript-event":
        present = exp.signature in event_surface
        return Finding(exp.component_id, exp.is_gated,
                       OBSERVED if present else NOT_OBSERVED, "transcript-event",
                       f"{'found' if present else 'absent'} {exp.signature!r} in tool_use events")
    # git-state — best-effort declared/present state over the clone (observed-only; never
    # gated). G4c: no first-token path artifacts — a machine-level (~-rooted) signature is
    # honestly unprobeable from a clone, path-shaped tokens are tried as paths, and a
    # settings-declared expectation is checked against the clone's .claude/settings.json.
    sig = exp.signature
    if sig.startswith("~"):
        return Finding(exp.component_id, exp.is_gated, NOT_OBSERVED, "git-state",
                       f"machine-level path {sig!r} — unobservable from a clone (not probed)")
    present, ev = False, f"absent {sig!r} in clone"
    tokens = sig.split()
    if clone is not None:
        for tok in tokens:
            if ("/" in tok or "\\" in tok or "." in tok) and (
                    path_present(clone, tok) or file_in_head(clone, tok)):
                present, ev = True, f"path {tok!r} present in clone"
                break
        if not present and tokens and tokens[0] == "enabledPlugins" and len(tokens) > 1:
            # Settings-DECLARED expectation: exact JSON check, never a substring (Codex
            # MED 2026-07-06 — `enabledPlugins` with a DIFFERENT plugin must not match).
            settings = Path(clone) / ".claude" / "settings.json"
            if settings.exists():
                try:
                    data = json.loads(settings.read_text(encoding="utf-8", errors="replace"))
                except (json.JSONDecodeError, OSError):
                    data = {}
                enabled = data.get("enabledPlugins")
                if isinstance(enabled, dict) and enabled.get(tokens[1]) is True:
                    present, ev = True, (
                        f"enabledPlugins[{tokens[1]!r}] declared in .claude/settings.json")
    return Finding(exp.component_id, exp.is_gated,
                   OBSERVED if present else NOT_OBSERVED, "git-state", ev)


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
    def armed_skipped(self) -> tuple[Finding, ...]:
        """G4a: gated hooks pre-commit consulted but Skipped — enforcing-for-their-scope,
        reported distinctly so they never inflate the FIRED count."""
        return tuple(f for f in self.gated_findings if f.verdict == SKIPPED_ARMED)

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
        armed = f", {len(self.armed_skipped)} armed-but-skipped" if self.armed_skipped else ""
        return (f"observer {verdict}: {len(self.gated_findings)} gated "
                f"({sum(f.verdict in _GATED_OK for f in self.gated_findings)} ok{armed}), "
                f"flags: {flagged}; commands observed: {len(self.commands_observed)}")


def observe(events: list[dict], oracle: _oracle.Oracle, *, clone: Path | None = None
            ) -> ObservationResult:
    """Classify every oracle expectation against the external channels. Deterministic;
    reads only structured events + git-state, never inner narration (C1)."""
    hook_surface = hook_stdout_surface(events)
    event_surface = tool_use_surface(events)
    precommit_ran = bool(_STAGE_RAN_RE.search(hook_surface))  # G4b: any per-hook report line
    findings = tuple(
        _classify(exp, hook_surface=hook_surface, event_surface=event_surface, clone=clone,
                  precommit_ran=precommit_ran)
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
