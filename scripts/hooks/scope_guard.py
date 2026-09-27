#!/usr/bin/env python
r"""scope_guard.py -- PreToolUse frame guard (R15): a tool call whose path argument resolves
under an excluded root (`ecosystem/excluded-roots.yaml`) is refused before it runs.

R15's own text: "A subagent or tool works inside the frame its task sets ... The operator's
employer folders (e.g. `OneDrive - Blue Yonder`) are outside every frame unless a brief names
them. Enforced by mechanism ... not by prompt text." This is that mechanism, for THIS harness's
own tool calls (Copilot's separate, unrelated mechanism is the `--deny-tool` argv in
`scripts/dispatch.py`'s `build_plan`, since Copilot is a foreign process this hook never sees).

FOLLOWS `block_immutable_edits.py`'S PRECEDENT (ADR-77) almost exactly: read the hook payload
as JSON on stdin; to DENY print `{"decision":"block",...}` on stdout and exit 2; to ALLOW exit 0
silently. The same asymmetric fail posture too: OUTSIDE the zone (no candidate path token at
all, or the payload will not parse) a guard malfunction must never block normal work -> ALLOW;
once a candidate token is a real path argument, an inability to EVALUATE it (a normalization
crash) fails CLOSED, same doctrine as `deny_and_point.py` (AX24-2) and `fleet_health.prompts_guard`
(AX15-1): "a guard that permits what it cannot check is declared enforcement without
enforcement." What is NEW here relative to `block_immutable_edits.py`: this guard also reads
Bash/PowerShell `command` text (that guard deliberately does not, an honest limit its own
docstring names), because the Done-contract requires "Fail-closed for Read/Edit/Write/Bash path
arguments"; and it normalizes environment variables, `~`, and Windows 8.3 short names before
matching, because a raw string match is trivially defeated by any of the three (verified live:
`GetShortPathNameW`/`GetLongPathNameW` round-trip `ONEDRI~1` back to the long form on this
filesystem -- ecosystem/excluded-roots.yaml's own header cites the same finding).

THE STORE (`ecosystem/excluded-roots.yaml`) IS READ, NEVER BUILT. An absent, empty or malformed
file is "not governed yet" and ALLOWS, the same posture `deny_and_point.py` takes for an absent
FPG-1 store -- a guard whose expensive error on a missing registry would be blocking every tool
call on a tree that has never added one is the wrong failure direction.

BASH/POWERSHELL TOKEN SCANNING IS A CHEAP PRE-FILTER, THEN A REAL RESOLVE. A command line is
split into shell words (`shlex`, one line at a time -- `shlex` in POSIX mode eats a backslash,
which is a path separator on Windows, so PowerShell lines are lexed non-POSIX, matching
`deny_and_point.py`'s own finding for the same reason); a token that carries no path-shaped
character (`/`, `\`, a drive letter, `~`, `$`, `%`) is never normalized or touched by the
filesystem, so an ordinary call with no path token at all (`pytest -x`, `ls`) pays only the
regex scan, keeping the p95 bound cheap. A token that DOES look like a path is resolved
(environment variables, `~`, 8.3 short names, `..`) relative to the tool call's own `cwd` and
checked against the excluded-root list.

WEDGE ESCAPE (Done-contract item 3): `DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE=1` in the environment
allows every call unconditionally, checked before the store is even read -- a PreToolUse hook
that refuses everything (the 2026-09-17 emergency-disable incident this repo's own history
names) must leave a session a way out that needs no code or data edit, only an environment
variable for the one session that needs it. The bypass is not silent: a line naming it goes to
stderr (informational only; it never changes the exit code), so a transcript still shows a
guard that is switched off rather than one that quietly stopped mattering.

Stdlib + PyYAML only (`pyproject.toml` already declares `pyyaml` for `scripts/` validators --
library-first, O-12: no new dependency). `ctypes.windll` is Windows-only and used only for the
8.3 short-name expansion; it is a no-op (returns the input unchanged) on any other platform, so
the guard degrades to environment-variable/`~`/`..` normalization there rather than failing.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOTS_FILE = REPO_ROOT / "ecosystem" / "excluded-roots.yaml"

#: The wedge escape (Done-contract item 3). Checked before the store is read at all.
DISABLE_ENV = "DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE"
_TRUE = frozenset({"1", "true", "yes", "on"})

#: Path fields a non-shell tool call may carry. `file_path`/`notebook_path` mirror
#: `block_immutable_edits.PATH_FIELDS`; `path` covers Grep/Glob's own field name.
PATH_FIELDS = ("file_path", "notebook_path", "path")

#: Tools whose `tool_input.command` is a shell command line, scanned token-by-token.
SHELL_TOOLS = ("Bash", "PowerShell")


# --------------------------------------------------------------------------------- the store

def load_roots(path: Path | None = None) -> list[str]:
    """The excluded-root entries, or `[]` on an absent/empty/malformed file -- "not governed
    yet" allows, same posture `deny_and_point.load_processes` takes for an absent FPG-1 store.

    `path` defaults to the MODULE GLOBAL `ROOTS_FILE`, looked up at CALL time rather than
    bound once as a parameter default -- a test that does `guard.ROOTS_FILE = tmp_file` (the
    same monkeypatch shape every other test in this file uses) must reach this function too.
    """
    if path is None:
        path = ROOTS_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    roots = data.get("roots")
    if not isinstance(roots, list):
        return []
    return [r.strip() for r in roots if isinstance(r, str) and r.strip()]


def guard_disabled(env: dict | None = None) -> bool:
    env = os.environ if env is None else env
    return env.get(DISABLE_ENV, "").strip().lower() in _TRUE


# ----------------------------------------------------------------------------- normalization

#: PowerShell's `$env:VAR` has no `expandvars` equivalent -- rewritten to `%VAR%` first, which
#: `os.path.expandvars` already understands on every platform.
_PS_ENV_VAR = re.compile(r"\$env:([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE)


def _expand_vars_and_home(token: str) -> str:
    token = _PS_ENV_VAR.sub(r"%\1%", token)
    token = os.path.expandvars(token)
    return os.path.expanduser(token)


def _long_form(path: str) -> str:
    """Expand a Windows 8.3 short name (`ONEDRI~1`) to its long form when the path exists.

    Never raises: `GetLongPathNameW` returns 0 on a path that does not exist (short or long),
    and the input is returned unchanged in that case -- a nonexistent path still normalizes via
    the lexical steps in `normalize`, it just cannot be un-shortened without asking the
    filesystem, and there is nothing to ask about a path with nothing on disk.
    """
    if os.name != "nt":
        return path
    import ctypes  # noqa: PLC0415 -- Windows-only, kept off every non-Windows import path

    buf = ctypes.create_unicode_buffer(32768)
    try:
        n = ctypes.windll.kernel32.GetLongPathNameW(path, buf, len(buf))  # type: ignore[attr-defined]
    except OSError:
        return path
    return buf.value if n else path


def normalize(token: str, cwd: str) -> list[Path]:
    """The absolute, long-form path form(s) a raw candidate token names, resolved against the
    tool call's OWN `cwd` (never this hook's).

    Returns BOTH a LEXICAL form (`..`/relative resolved via `os.path.normpath`, no filesystem
    access needed, so a nonexistent path still normalizes -- `block_immutable_edits`'s own
    precedent for why) and, when it differs, a REALPATH form (symlinks and Windows junctions
    followed). Both are needed: normpath alone lets a junction whose own name sits outside the
    zone but that POINTS INTO it slip past a lexical-only match (Codex terra review, P1, this
    lane -- the same reason `block_immutable_edits._canonical_forms` checks both forms too).
    `os.path.realpath` never raises on a path that does not exist; it simply returns the input
    unresolved, so the lexical form is never lost even when there is nothing on disk to resolve.
    """
    expanded = _long_form(_expand_vars_and_home(token))
    candidate = Path(expanded)
    if not candidate.is_absolute():
        candidate = Path(cwd or os.getcwd()) / candidate
    lexical = Path(os.path.normpath(str(candidate)))
    forms = [lexical]
    real = Path(os.path.realpath(str(candidate)))
    if real != lexical:
        forms.append(real)
    return forms


# --------------------------------------------------------------------------------- candidates

#: A token is worth resolving only if it carries a path-shaped character -- a separator, a
#: drive letter, `~`, or an environment-variable marker. An ordinary word (`status`, `commit`,
#: `-m`) never reaches `normalize`, which is what keeps a no-path call cheap.
_PATH_HINT = re.compile(r"[\\/~]|^[A-Za-z]:|\$env:|\$[A-Za-z_]|%[A-Za-z_]", re.IGNORECASE)


def _looks_like_path(token: str) -> bool:
    return bool(_PATH_HINT.search(token))


def _command_candidates(command: str) -> list[str]:
    """Every path-shaped shell word in `command`, scanned one LINE at a time.

    A newline ends a command; `shlex` treats it as ordinary whitespace, so scanning the whole
    command as one `shlex` stream would let a path on the line after a heredoc marker fold into
    the wrong segment (`deny_and_point._line_segments`'s own documented reason for the same
    per-line split). posix=False: a backslash is a Windows path separator, and POSIX lexing
    treats it as an escape -- `deny_and_point._line_segments` hit exactly this on PowerShell and
    fixed it the same way. An unparseable line yields no candidates from it (never raises), the
    same "a search that cannot be tokenized allows" posture `deny_and_point.py` takes.
    """
    out: list[str] = []
    for line in command.split("\n"):
        if not line.strip():
            continue
        try:
            tokens = shlex.split(line, posix=False)
        except ValueError:
            continue
        for tok in tokens:
            cleaned = tok.strip("\"'")
            if cleaned and _looks_like_path(cleaned):
                out.append(cleaned)
    return out


def candidate_tokens(payload: dict) -> list[str]:
    """What this tool call names as a path, whatever tool it came in on. `[]` = never refused
    by this hook (Done-contract item 2: "a call with no path argument is never refused")."""
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return []
    if tool in SHELL_TOOLS:
        command = tool_input.get("command")
        return _command_candidates(command) if isinstance(command, str) and command.strip() else []
    out = []
    for field in PATH_FIELDS:
        value = tool_input.get(field)
        if isinstance(value, str) and value:
            out.append(value)
    return out


# ----------------------------------------------------------------------------------- matching

def excluded_root_hit(path: Path, roots: list[str]) -> str | None:
    """The root `path` resolves under, or `None`.

    A root carrying a separator is an ABSOLUTE PREFIX, matched after normalizing both sides. A
    bare name (no separator) matches as a whole PATH COMPONENT anywhere in `path`'s parts --
    the shape that lets one entry ("OneDrive - Blue Yonder") cover the zone wherever it is
    mounted (a different drive letter, a fresh profile, a future machine) without a
    machine-specific absolute root baked into the registry. Case-insensitive throughout:
    Windows path comparison is not case-sensitive and this guard must not be defeatable by case.
    """
    parts_cf = [part.casefold() for part in path.parts]
    text_cf = str(path).casefold()
    for root in roots:
        root_cf = root.casefold()
        if "/" in root_cf or "\\" in root_cf:
            norm_root = os.path.normpath(root_cf)
            if text_cf == norm_root or text_cf.startswith(norm_root.rstrip("\\/") + os.sep):
                return root
        elif root_cf in parts_cf:
            return root
    return None


# --------------------------------------------------------------------------------- messages

def _denied(token: str, resolved: Path, root: str) -> str:
    return (
        f"DENIED: this tool call's path argument resolves under the excluded root {root!r} "
        f"(R15) -- token {token!r} normalizes to {resolved}.\n"
        "The operator's employer folders are outside every frame unless a brief names them "
        "(ratified: RATIFICATION-2026-09-25.md v10 R15).\n"
        "If this call genuinely needs that path, the brief must name it explicitly and the "
        "operator-settable switch (DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE=1) is the escape -- edit "
        "ecosystem/excluded-roots.yaml only if the root itself is wrong."
    )


def _cannot_evaluate(token: str, exc: BaseException) -> str:
    """Fails CLOSED once a candidate token is a real path argument this guard cannot resolve
    (AX24-2/AX15-1 doctrine: permitting what it cannot check is enforcement without
    enforcement) -- but ONLY here, past the free `candidate_tokens`/`_looks_like_path` filter,
    so an ordinary call with no path-shaped token never risks this path at all."""
    return (
        "DENIED: this guard could not evaluate a path-shaped argument, and it fails CLOSED "
        f"rather than permit what it cannot check.\nToken: {token!r}. Cause: {exc!r}.\n"
        "Fix: report this as a bug in scripts/hooks/scope_guard.py; the operator-settable "
        "switch (DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE=1) is the immediate way through."
    )


# --------------------------------------------------------------------------------- the wire

def decide(payload: dict, roots: list[str]) -> tuple[str, str]:
    """The pure core: ('block'|'allow', reason). No I/O; roots injected."""
    if not isinstance(payload, dict):
        return "allow", "unrecognised payload"
    tokens = candidate_tokens(payload)
    if not tokens:
        return "allow", "no path argument"
    cwd = payload.get("cwd")
    for token in tokens:
        try:
            forms = normalize(token, cwd)
        except Exception as exc:  # noqa: BLE001 -- fails CLOSED, see _cannot_evaluate
            return "block", _cannot_evaluate(token, exc)
        for resolved in forms:
            hit = excluded_root_hit(resolved, roots)
            if hit:
                return "block", _denied(token, resolved, hit)
    return "allow", "no candidate resolves under an excluded root"


def decide_with_config(payload: dict) -> tuple[str, str]:
    """`decide`, with the wedge escape and the store load folded in -- the impure entry point
    `main` and the integration tests call."""
    if guard_disabled():
        print(
            "[scope-guard] DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE is set -- this call was NOT "
            "evaluated against ecosystem/excluded-roots.yaml.",
            file=sys.stderr,
        )
        return "allow", "guard disabled by the operator-settable switch"
    return decide(payload, load_roots())


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:  # noqa: BLE001 -- unparseable payload: outside the zone by construction
        payload = None
    decision, reason = decide_with_config(payload)
    if decision == "block":
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=True))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
