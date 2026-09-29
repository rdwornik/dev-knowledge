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

HONEST LIMIT (repair 1, Codex terra review P1, verified rather than assumed; narrowed by
LANE-5B5R-2-scope-guard-2): this guard reads the tool call's OWN literal text; it does not
execute or interpret shell semantics. Two constructions repair 1 left `allow` are now CLOSED
without needing execution, because both assemble the excluded root's name from LITERAL text
already present in the command -- reading a literal twice is not interpretation:
- A quoted-string CONCATENATION (`"OneDrive" + " - Blue Yonder"`, the `+` operator PowerShell
  and other shells use to join literals) is folded into one candidate string
  (`_command_candidates`'s concatenation scan) and resolved the ordinary way.
- A same-line cmd.exe `set VAR=value` assignment followed later in the SAME command text by
  `%VAR%` (`set X=OneDrive - Blue Yonder& type ...%X%...`) is resolved by substituting the
  assignment's own literal VALUE for `%VAR%` (`_local_set_vars`) before normalization --
  again reading the same literal twice, never executing `set`.
What remains a genuine, un-closed limit: a value computed by something this guard cannot read
as literal text at all -- the output of another command, a loop, a registry/environment
lookup this guard's own process does not share (a DIFFERENT session's `set`, a `Get-Date`
concatenation, an obfuscated/encoded command line). Interpreting THAT would mean partially
executing the command to know what it resolves to, a categorically bigger mechanism than a
pre-exec text guard, and stays out of proportion to fix unilaterally here -- recorded as
`ROWS-OWED`, not silently dropped. What repair 1 DID close, because it does not need shell
interpretation either: an MCP/LSP/`Monitor` tool's path argument under an unnamed field
(`candidate_tokens`' string-leaf fallback) and a shell glob character standing in for the root
name (`excluded_root_hit`'s `fnmatch` leg) -- both verified bypasses, both now blocked.

CROSS-OS NORMALIZATION (LANE-5B5R-2-scope-guard-2, closing the N4 redo's second refusal): the
CI verdict is both OSes, and a Windows-syntax token (`%VAR%`, a backslash separator) must
resolve the SAME way whichever OS the guard's own process runs on -- the payload describes a
call the operator's OWN box will make, not necessarily the box running this test. `%VAR%` and
`$VAR`/`${VAR}` are therefore expanded by this module's OWN regex substitution against
`os.environ` (`_expand_env_vars`), never `os.path.expandvars` (whose `%VAR%` support is
Windows-only in the stdlib -- verified: `posixpath.expandvars` does not implement it, which is
why the N4 redo's env-var test only passed on the Windows CI leg). A backslash is normalized to
`/` before the token becomes a `Path` (`normalize`), for the same reason: `PosixPath` never
splits on `\\`, so a Windows-style token would arrive as one unsplittable part and never match a
bare-name root as a path COMPONENT on the ubuntu leg.

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

import fnmatch
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

#: Tools whose path argument (if any) lives at a KNOWN field name, checked via `PATH_FIELDS`
#: above. Any tool the settings.json matcher fires on but that is NOT in this set -- an MCP
#: resource tool, LSP, or a future addition to the matcher -- has an unknown payload shape
#: (Codex terra review, P1, this lane's repair 1: the named-field list alone left MCP/LSP
#: path-bearing fields, whatever a given server calls them, outside this guard's reach), so
#: `candidate_tokens` falls back to scanning every string leaf of `tool_input` for one instead
#: of guessing a field name.
NAMED_FIELD_TOOLS = frozenset({"Read", "Write", "Edit", "MultiEdit", "NotebookEdit", "Glob", "Grep"})


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

#: PowerShell's `$env:VAR` has no cross-OS stdlib equivalent -- rewritten to `%VAR%` first,
#: which `_expand_env_vars` below then handles the same as a native `%VAR%` token.
_PS_ENV_VAR = re.compile(r"\$env:([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE)

#: `%VAR%` (cmd.exe/PowerShell) and `$VAR`/`${VAR}` (POSIX shells) -- matched and expanded by
#: THIS module's own regex, never `os.path.expandvars`: that stdlib function dispatches on the
#: HOST os (`ntpath` understands `%VAR%`, `posixpath` does not, and neither understands the
#: other's form at all), so the same token would resolve on Windows and silently NOT resolve on
#: Linux -- exactly the gap the N4 redo's ubuntu CI leg found (Done-contract item 8).
_PCT_VAR = re.compile(r"%([A-Za-z_][A-Za-z0-9_]*)%")
_DOLLAR_VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")

#: A cmd.exe same-line `set VAR=value` assignment -- `&`/`;`/newline-delimited, matching the
#: repair-1 Codex terra review's own reproduction (`set X=...& type ...%X%...`). Two forms,
#: tried in order: the QUOTED whole-assignment form cmd.exe itself recommends
#: (`set "X=OneDrive - Blue Yonder"`, closing quote delimits the value even with trailing
#: spaces) and the bare form. Fresh Codex terra review (this redo, item 6): the bare-only
#: pattern missed the quoted form entirely, leaving its same-line expansion unresolved and
#: allowed. The VALUE is itself a literal already present in the command text, so
#: substituting it for a later `%VAR%` on the same line needs no shell execution -- see the
#: module docstring, "HONEST LIMIT".
_CMD_SET = re.compile(
    r'(?:^|[&;\n])\s*set\s+(?:"([A-Za-z_][A-Za-z0-9_]*)=([^"]*)"'
    r'|([A-Za-z_][A-Za-z0-9_]*)=(.*?)(?=[&;\n]|$))',
    re.IGNORECASE)


def _local_set_vars(command: str) -> dict[str, str]:
    """Every `set VAR=value` this command text assigns, keyed upper-case (Windows env-var
    names are case-insensitive) -- `{}` for a command with no `set` at all, the common case,
    so callers can skip the substitution pass entirely."""
    out: dict[str, str] = {}
    for m in _CMD_SET.finditer(command):
        name = m.group(1) or m.group(3)
        value = m.group(2) if m.group(1) is not None else m.group(4)
        out[name.upper()] = value.strip()
    return out


def _ci_environ_get(name: str) -> str | None:
    """`os.environ.get`, but a Windows-style `%VAR%`/`$env:VAR` lookup is case-INSENSITIVE
    (Windows environment-variable names are, unlike POSIX's) -- fresh Codex terra review (this
    redo, item 6): a plain `os.environ.get` left `%dk_test_root%` unresolved against a
    `DK_TEST_ROOT` set by `monkeypatch.setenv`, contradicting this module's own claimed
    cross-OS Windows-token behaviour whenever the two cases disagree. Exact match tried first
    (the common, cheap case); the case-insensitive scan only runs on a miss."""
    value = os.environ.get(name)
    if value is not None:
        return value
    upper = name.upper()
    for key, val in os.environ.items():
        if key.upper() == upper:
            return val
    return None


def _expand_env_vars(token: str, local_vars: dict[str, str]) -> str:
    """`%VAR%`/`$env:VAR` (Windows-style, case-insensitive) and `$VAR`/`${VAR}` (POSIX,
    case-sensitive -- POSIX environment-variable names are, and a case-insensitive lookup
    there would be a WRONG semantic, not a portability fix) expanded against `local_vars`
    first (a same-line `set` this command text itself made), then `os.environ` -- an
    unresolvable reference is left as-is (the existing candidate/normalize/match pipeline
    still evaluates the literal text, it just will not happen to land in the excluded root,
    the same posture an absent env var takes today)."""

    def _pct_sub(match: re.Match) -> str:
        name = match.group(1)
        if name.upper() in local_vars:
            return local_vars[name.upper()]
        value = _ci_environ_get(name)
        return value if value is not None else match.group(0)

    def _dollar_sub(match: re.Match) -> str:
        name = match.group(1) or match.group(2)
        if name.upper() in local_vars:
            return local_vars[name.upper()]
        return os.environ.get(name, match.group(0))

    token = _PCT_VAR.sub(_pct_sub, token)
    token = _DOLLAR_VAR.sub(_dollar_sub, token)
    return token


def _expand_vars_and_home(token: str, local_vars: dict[str, str] | None = None) -> str:
    token = _PS_ENV_VAR.sub(r"%\1%", token)
    token = _expand_env_vars(token, local_vars or {})
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


def normalize(token: str, cwd: str, local_vars: dict[str, str] | None = None) -> list[Path]:
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

    A backslash is normalized to `/` BEFORE the `Path` is built, whatever OS this process runs
    on: `PosixPath` never treats `\\` as a separator, so a Windows-syntax token (drive letter,
    `\\`-joined segments) would otherwise arrive as one unsplittable part on the ubuntu CI leg
    and never match a bare-name root as a path COMPONENT (Done-contract item 8) -- done AFTER
    the 8.3 short-name expansion above, which needs the original backslash form for the Win32
    call it makes only on `nt` anyway.
    """
    expanded = _long_form(_expand_vars_and_home(token, local_vars)).replace("\\", "/")
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


#: A single quoted literal, EITHER quote style -- PowerShell allows each concatenated operand
#: its own independent choice of `"..."` or `'...'`.
_QUOTED_LITERAL = r'"[^"]*"|\'[^\']*\''
_QUOTED_LITERAL_PIECE = re.compile(r'"([^"]*)"|\'([^\']*)\'')

#: A run of two-or-more quoted literals joined by `+` (PowerShell/JS-style string
#: concatenation) -- `"C:\...\" + "OneDrive" + " - Blue Yonder" + "\f.txt"` never places the
#: root's literal name in one shell WORD, so `shlex` alone cannot see it, but every piece is
#: still literal text this guard can read and join without executing anything (Codex terra
#: review P1, repair 1 -- the reviewer's own reproduction; Done-contract item 9). SINGLE
#: quotes matter here too, not just double: fresh Codex terra review (this redo, item 6)
#: found `Get-Item ('OneDrive' + ' - Blue Yonder')` -- a valid PowerShell single-quoted
#: concatenation -- unmatched by a double-quote-only pattern.
_STRING_CONCAT = re.compile(rf'(?:(?:{_QUOTED_LITERAL})\s*\+\s*)+(?:{_QUOTED_LITERAL})')


def _neutralize_nested_quote_chars(line: str) -> str:
    """A quote character that appears WHILE a DIFFERENTLY-typed quote is already open is not
    a real delimiter -- it is a literal character inside that outer quoted region (ordinary
    shell/PowerShell quoting: a `'` inside `"..."` never closes anything, and vice versa).
    Every such inert quote char is replaced with NUL so `_STRING_CONCAT` below can never
    mistake prose-inside-one-big-argument for a separate literal.

    Fresh Codex terra review (this redo, second pass): a PowerShell command running
    `git commit -m "document 'OneDrive' + ' - Blue Yonder' handling"` has the WHOLE `-m`
    argument as one double-quoted string; the single quotes around `'OneDrive'` inside it are
    literal text, not PowerShell string delimiters, so the `+` between them is not the
    concatenation operator either -- this is prose describing the construction, the same
    class the existing anti-false-positive test already covers for a single quoted literal,
    just with an inner `+` this time. A GENUINELY separate pair of top-level literals
    (`"OneDrive" + " - Blue Yonder"`, no enclosing outer quote) is left untouched: neither
    quote char is ever nested inside another OPEN quote of a different type.

    A PowerShell backtick escapes the character right after it (`` `" `` is a literal quote
    that does NOT close or open a string) -- third-pass Codex terra review, this redo: a
    scanner blind to this treats an escaped quote as a real delimiter, desyncing `state` for
    every character after it and wrongly neutralizing a GENUINE concatenation later on the
    same line (`Write-Output "x`""; Remove-Item ('OneDrive' + ' - Blue Yonder')` -- the
    escaped `"` inside the first string must never toggle `state`, or the real single-quoted
    concatenation after it is misread as nested prose and allowed through). The escaped
    character itself is also blanked -- it is not a real delimiter for `_STRING_CONCAT`
    either, whichever quote type it happens to be.

    BUT ONLY inside a double-quoted (PowerShell calls this "expandable") string, or bare --
    fourth-pass Codex terra review, this redo: PowerShell's backtick is NOT an escape
    character inside a SINGLE-quoted ("literal") string at all; treating it as one there
    (`Write-Output 'x`'; Remove-Item ("OneDrive" + " - Blue Yonder")`) skips the real closing
    `'`, leaving `state` stuck open and wrongly neutralizing the genuine DOUBLE-quoted
    concatenation that follows. `state == "'"` is therefore excluded from escape handling."""
    out = list(line)
    state: str | None = None
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if ch == "`" and i + 1 < n and state != "'":
            escaped = line[i + 1]
            if escaped in "\"'":
                out[i + 1] = "\0"
            i += 2
            continue
        if state is None:
            if ch in "\"'":
                state = ch
        elif ch == state:
            state = None
        elif ch in "\"'":
            out[i] = "\0"
        i += 1
    return "".join(out)


def _concatenated_literal_candidates(command: str) -> list[str]:
    """Not gated by `_looks_like_path`: the concatenation SYNTAX itself (two-or-more quoted
    literals joined by `+`, a narrow and deliberate shape no ordinary prose or single-string
    command hits -- see `test_a_word_that_merely_mentions_the_zone_name_in_prose...`) is
    already a strong enough signal, and a bare root name joined from pieces
    (`"OneDrive" + " - Blue Yonder"`) carries no separator to trigger the path-hint filter at
    all despite being exactly the construction Done-contract item 9 names.

    ONLY called for the `PowerShell` tool (see `_command_candidates`) -- `+` between two
    quoted strings is PowerShell's own concatenation OPERATOR, evaluated by that interpreter;
    in POSIX shell syntax it is not special at all, so the identical text inside an equivalent
    Bash command is prose, never code, and must not be treated as a candidate. Matched against
    `_neutralize_nested_quote_chars`'s output, not the raw text (see that function)."""
    out: list[str] = []
    for match in _STRING_CONCAT.finditer(_neutralize_nested_quote_chars(command)):
        joined = "".join(
            piece.group(1) if piece.group(1) is not None else piece.group(2)
            for piece in _QUOTED_LITERAL_PIECE.finditer(match.group(0))
        )
        if joined:
            out.append(joined)
    return out


def _command_candidates(command: str, tool: str) -> list[str]:
    """Every path-shaped shell word in `command`, scanned one LINE at a time, PLUS -- for the
    `PowerShell` tool ONLY -- any string-concatenation candidates the whole command text
    assembles (`_concatenated_literal_candidates`, not line-scoped since PowerShell allows the
    `+` chain to wrap; tool-scoped because `+` between quoted strings is PowerShell's own
    operator, not POSIX shell syntax -- see that function's docstring).

    A newline ends a command; `shlex` treats it as ordinary whitespace, so scanning the whole
    command as one `shlex` stream would let a path on the line after a heredoc marker fold into
    the wrong segment (`deny_and_point._line_segments`'s own documented reason for the same
    per-line split). posix=False: a backslash is a Windows path separator, and POSIX lexing
    treats it as an escape -- `deny_and_point._line_segments` hit exactly this on PowerShell and
    fixed it the same way. An unparseable line yields no candidates from it (never raises), the
    same "a search that cannot be tokenized allows" posture `deny_and_point.py` takes.
    """
    out: list[str] = list(_concatenated_literal_candidates(command)) if tool == "PowerShell" else []
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


def _string_leaves(value: object) -> list[str]:
    """Every non-empty string leaf in a JSON-shaped value, depth-first.

    An unrecognised tool's path argument can live under any field name at any nesting depth
    (an MCP server's own schema, not this repo's), so this does not guess one -- it collects
    every string in the payload and lets `_looks_like_path` (the same cheap prefilter shell
    scanning already uses) decide which are worth resolving."""
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, dict):
        out: list[str] = []
        for v in value.values():
            out.extend(_string_leaves(v))
        return out
    if isinstance(value, list):
        out = []
        for v in value:
            out.extend(_string_leaves(v))
        return out
    return []


def candidate_tokens(payload: dict) -> list[str]:
    """What this tool call names as a path, whatever tool it came in on. `[]` = never refused
    by this hook (Done-contract item 2: "a call with no path argument is never refused")."""
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return []
    if tool in SHELL_TOOLS:
        command = tool_input.get("command")
        return (_command_candidates(command, tool)
                if isinstance(command, str) and command.strip() else [])
    if tool in NAMED_FIELD_TOOLS:
        out = []
        for field in PATH_FIELDS:
            value = tool_input.get(field)
            if isinstance(value, str) and value:
                out.append(value)
        return out
    # An unrecognised tool (MCP resource tools, LSP, Monitor, or anything else the matcher in
    # .claude/settings.json fires on beyond the named set above): scan every string leaf,
    # same cheap path-hint prefilter as shell command scanning, rather than never checking it.
    return [s for s in _string_leaves(tool_input) if _looks_like_path(s)]


# ----------------------------------------------------------------------------------- matching

def excluded_root_hit(path: Path, roots: list[str]) -> str | None:
    """The root `path` resolves under, or `None`.

    A root carrying a separator is an ABSOLUTE PREFIX, matched after normalizing both sides. A
    bare name (no separator) matches as a whole PATH COMPONENT anywhere in `path`'s parts --
    the shape that lets one entry ("OneDrive - Blue Yonder") cover the zone wherever it is
    mounted (a different drive letter, a fresh profile, a future machine) without a
    machine-specific absolute root baked into the registry. Case-insensitive throughout:
    Windows path comparison is not case-sensitive and this guard must not be defeatable by case.

    A part carrying a shell GLOB CHARACTER (`*`, `?`, `[`) is matched with `fnmatch` -- the
    literal part text will never equal the root name, but the shell (`Get-ChildItem "...\\
    OneDrive*\\f.txt"`) would still expand it onto the zone (Codex terra review, P1, this
    lane's repair 1). Checked as "does this pattern match the root name", not the reverse, so
    an ordinary part with no glob character is unaffected and still needs an exact match.

    A BARE wildcard (`*`, `**`, `?`, any combination of only those, no literal character at
    all) is NARROWED to the one position it is an actual bypass risk (LANE-5B5-1, closing the
    four false positives that same fifth Codex terra review pass's blanket fail-closed cost
    -- `DIGEST-N5-DRAFT-2026-09-29.md` \u00a76, `SESSION-launch-cycle-2-2026-09-29.md`
    ROWS-OWED, `SESSION-lane-scope-guard-2.md:333-342`): the real excluded root can only ever
    sit as the DIRECT CHILD of a conventional OS user-home parent -- `Users\\<name>\\OneDrive
    - Blue Yonder` (Windows) or `/home/<name>/OneDrive - Blue Yonder` (POSIX); R15's own text
    names it as one of "the operator's employer folders" living directly under the profile.
    A bare wildcard is therefore still treated as "could stand in for the root" ONLY when the
    path component two positions before it (the wildcard's own would-be SIBLING position's
    parent) is literally `users` or `home` (case-insensitive) -- `_BARE_WILDCARD_HOME_PARENTS`
    below -- which is exactly the shape `Get-ChildItem 'C:\\Users\\x\\*\\secret.txt'` has (the
    real bypass a prior Codex round found; kept blocked, see
    `test_a_bare_wildcard_standing_in_for_the_root_at_its_own_parent_is_refused`). A bare
    wildcard ANYWHERE else -- inside a `grep` regex's own literal text (never a path at all),
    under `~/.claude/projects/*` (a sanctioned zone, LANE-5B5-1's own "Do not" list), or a git
    pathspec like `templates/**` -- is nowhere near that boundary and is no longer treated as
    a hit. A GLOB WITH LITERAL CONTENT (`OneDrive*`, `repo*`) is unaffected either way: it
    still needs an actual `fnmatch` match against the root name regardless of position, since
    literal text is already a strong enough signal on its own (see
    `test_a_shell_glob_wildcard_standing_in_for_the_root_name_is_refused`)."""
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
        elif _bare_wildcard_hit(root_cf, parts_cf):
            return root
    return None


#: The only OS convention under which the excluded root can be a direct child -- a
#: user-profile/home directory (`Users` on Windows, `home` on POSIX). A bare wildcard
#: sitting exactly one level below one of these is the shape a real `OneDrive - Blue Yonder`
#: folder would occupy; anywhere else it is not a plausible stand-in for it.
_BARE_WILDCARD_HOME_PARENTS = frozenset({"users", "home"})

#: A path component made ENTIRELY of glob metacharacters -- no literal text at all -- is the
#: degenerate case `fnmatch.fnmatchcase(root, part)` matches unconditionally, whatever `root`
#: is (see `excluded_root_hit`'s docstring).
_PURE_WILDCARD = re.compile(r"^[*?]+$")


def _bare_wildcard_hit(root_cf: str, parts_cf: list[str]) -> bool:
    for i, part in enumerate(parts_cf):
        if not any(ch in part for ch in "*?["):
            continue
        if _PURE_WILDCARD.fullmatch(part):
            if i >= 2 and parts_cf[i - 2] in _BARE_WILDCARD_HOME_PARENTS:
                return True
            continue
        if fnmatch.fnmatchcase(root_cf, part):
            return True
    return False


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
    # A same-line `set VAR=value` (cmd.exe syntax) is a literal already in the shell command's
    # OWN text -- resolved here, once, rather than re-parsed per token (Done-contract item 9).
    local_vars: dict[str, str] = {}
    tool_input = payload.get("tool_input")
    if payload.get("tool_name") in SHELL_TOOLS and isinstance(tool_input, dict):
        command = tool_input.get("command")
        if isinstance(command, str):
            local_vars = _local_set_vars(command)
    for token in tokens:
        try:
            forms = normalize(token, cwd, local_vars)
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
