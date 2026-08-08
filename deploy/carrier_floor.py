"""deploy/carrier_floor.py — the per-repo methodology-floor carrier (ADR-92 C4, ADR-93).

Reconciles the consumer repo's methodology floor (ADR-78) AND **arms** it (ADR-93):
it does not merely drop the floor bytes, it makes a fresh clone **self-arming**.

Artifacts this carrier writes/stages into the consumer tree (ADR-92 write-yes /
commit-no — the operator ratifies the commit):

1. ``.claude/CLAUDE-FLOOR.md`` — the floor body (byte-for-byte the shipped template).
2. ``.claude/CLAUDE-FLOOR.md.sha256`` — its content-integrity sidecar.
3. ``.claude/check_floor_hash.py`` — the single canonical hash-guard script
   (``generate_floor.CHECK_FLOOR_HASH_SCRIPT``), run by BOTH guard legs.
4. ``CLAUDE.md`` — an ``@.claude/CLAUDE-FLOOR.md`` include so CC auto-loads the floor.
5. ``.gitignore`` — the ``.claude/*`` + negation block so the floor/sidecar/hook are
   TRACKABLE (model A: committed, not gitignored) without a fragile ``git add -f``.
6. ``.claude/settings.json`` — a ``SessionStart`` hook block with two command legs:
   (a) ``python .claude/check_floor_hash.py`` — the session-start VERIFY leg (fires every
   session, travels with the clone, un-suppressible by ``git commit --no-verify``);
   (b) ``python -m pre_commit install -t ...`` — idempotently bootstraps the commit-time git
   hooks, which git never lets travel with a clone. The first CC session auto-arms it.
   Both legs are ASSERTED by detect/verify, and the arm leg is asserted at full stage
   cardinality: it must name EVERY managed stage in ``ARM_HOOK_TYPES`` (#290 — an arm leg
   that names fewer arms the rest wired-but-dormant, the #275 defect). ``apply`` SELF-HEALS
   a stale under-armed leg in place, so no verdict reports drift ``apply`` cannot repair.

The **commit-time** leg itself — the ``floor-hash-verify`` entry in the consumer's
``.pre-commit-config.yaml`` — is owned by the **precommit carrier** (single-writer-per-
file; operator ruling), NOT this carrier. This carrier writes the script both legs run
and the settings.json that bootstraps the git hook (ADR-93 records why arming spans two
carriers).

Generation is REUSED from the hub's ``scripts/generate_floor.py`` by IMPORTING its
building blocks — ``render_floor`` (the floor body), ``floor_sha256`` (LF-normalized,
autocrlf-proof hash), ``validate`` (token-ceiling / F5 / zero-URL gate) and
``CHECK_FLOOR_HASH_SCRIPT`` (the canonical guard, single-sourced from the paste-ready
INSTALL_NOTE so the automated arm and the manual runbook can never disagree). No
subprocess is needed; importing the pieces is the CORRECT scope (the CLI additionally
refreshes the hub SHA anchor + prints an install note — side-effects a consumer-only
carrier must NOT cause). This carrier writes ONLY the consumer tree; it never mutates
the hub and never refactors the generator (ADR-92 build-slice constraint).

Three contract states (the ``.sha256`` is content-integrity, not a version anchor — so
no PRESENT_WRONG_VERSION): ``ABSENT`` (floor missing), ``PRESENT_CORRECT`` (floor +
sidecar hash to the corpus floor AND every arming artifact is in place),
``PRESENT_DRIFTED`` (floor edited, corpus moved, sidecar missing/stale, or any arming
artifact missing/wrong — including a SessionStart arm leg that arms fewer than every
managed hook stage).

D9 (ADR-92 Decision 9): ``_classify_floor`` (detect's judgment) and ``_verify_floor``
(verify's judgment) are distinct functions with no shared correctness-judgment helper.
``render_floor``/``floor_sha256``/``_read_sidecar_hash`` + the arming READ helpers are
shared SPEC reads/parsers (D9-permitted, like target-parsing) — the JUDGMENT
(compare-to-corpus, presence checks) is implemented twice, independently.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import logging
import re
import shlex
import sys
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

# Reuse the hub generator's importable building blocks. scripts/ lives beside deploy/
# under the hub root; add it to the path so `import generate_floor` resolves.
_HUB_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = _HUB_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import arm_hooks  # noqa: E402
import generate_floor as gf  # noqa: E402

log = logging.getLogger(__name__)

CARRIER_ID = "floor"

# Defaults mirror generate_floor.py's own constants (the floor under the consumer's
# .claude/). The manifest target may override the relative floor/sidecar paths.
DEFAULT_FLOOR_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/{gf.FLOOR_FILENAME}"
DEFAULT_SIDECAR_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/{gf.SIDECAR_FILENAME}"

# Arming-artifact locations (consumer-root-relative; fixed — not target-overridable).
HOOK_SCRIPT_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/check_floor_hash.py"
CLAUDE_MD_REL = "CLAUDE.md"
GITIGNORE_REL = ".gitignore"
SETTINGS_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/settings.json"

# The @-include line CC auto-resolves at session start (transitive, fail-soft).
INCLUDE_LINE = f"@{DEFAULT_FLOOR_REL}"

# The .gitignore block model A requires: contents-form exclusion + three negations, so
# the tracked files re-include without `git add -f`. The bare `.claude/` DIRECTORY form
# defeats negations (git won't re-include under an excluded dir), so it must be
# `.claude/*` (#138 empirical).
_GITIGNORE_CONTENTS_FORM = f"{gf.CHILD_CLAUDE_DIRNAME}/*"
_GITIGNORE_NEGATIONS = (
    f"!{DEFAULT_FLOOR_REL}",
    f"!{DEFAULT_SIDECAR_REL}",
    f"!{HOOK_SCRIPT_REL}",
)

# The two SessionStart command legs (relative invocation — CC runs SessionStart hooks
# with cwd = the project root, and the guard script itself uses repo-relative paths).
# The verify leg runs --require-present so a deleted-but-tracked floor fails LOUD at
# session-start (the commit-time pre-commit leg cannot catch a pure deletion — it is the
# backstop; ADR-93). The bootstrap leg idempotently arms the commit-time git hook.
_SESSIONSTART_VERIFY_CMD = f"python {HOOK_SCRIPT_REL} --require-present"

# The managed git-hook stages the arm leg must install (#275b). A bare `pre_commit install`
# arms the pre-commit stage ONLY, so commit-msg / pre-push stage hooks land
# wired-but-dormant on a fresh consumer.
#
# SINGLE-SOURCED from the hub's own self-arm (`scripts/arm_hooks.py::HOOK_TYPES`): stage
# cardinality has exactly ONE source of truth in the tree, and the deployed consumer arm can
# no longer drift from the hub arm it mirrors. This module must never re-declare the stage
# list — derive the command, the detect predicate and the verify predicate from here (#290).
ARM_HOOK_TYPES: tuple[str, ...] = arm_hooks.HOOK_TYPES
_ARM_STAGES = frozenset(ARM_HOOK_TYPES)

# pre-commit's OWN enum of installable hook types — needed to tell a VALID stage this carrier
# does not manage (`post-commit`: fine, arms nothing of ours) from an INVALID one (`bogus`:
# `-t` is choices-constrained, so the whole `install` exits non-zero and arms NOTHING). Not a
# second cardinality source: ARM_HOOK_TYPES above stays the sole statement of what we require.
try:  # library-first — the authority whenever pre-commit is importable
    from pre_commit.clientlib import HOOK_TYPES as _PRECOMMIT_HOOK_TYPES
except Exception:  # pragma: no cover - env without pre-commit; mirror of the above (4.x)
    _PRECOMMIT_HOOK_TYPES = (
        "commit-msg", "post-checkout", "post-commit", "post-merge", "post-rewrite",
        "pre-commit", "pre-merge-commit", "pre-push", "pre-rebase", "prepare-commit-msg",
    )
_VALID_HOOK_TYPES = frozenset(_PRECOMMIT_HOOK_TYPES)

def _install_arg_parser() -> argparse.ArgumentParser:
    """A parser mirroring `pre-commit install`'s own option surface (from its `--help`).

    Whether an arm command actually installs anything is an ARGPARSE question, so it is
    answered BY argparse rather than re-derived. Nine review passes over this lane each found
    one more way a hand-rolled flag walk disagreed with the real thing — bundled `-ft`, `-tX`,
    `-t=X`, `-t==X`, unambiguous long abbreviations (`--col`), `choices=` rejection on `-t` and
    `--color`, `-h` terminating before dispatch, a missing option value, an unknown option, and
    positionals after `--`. Delegating makes that whole class structurally impossible instead
    of enumerated: argparse decides here exactly what it decides at runtime.

    Drift-guarded by test_install_option_surface_matches_pre_commit_help — if pre-commit adds
    an option, that test FAILS loudly rather than a consumer using it reading as un-armed and
    having its command rewritten.
    """
    parser = argparse.ArgumentParser(prog="pre-commit install", add_help=True)
    parser.add_argument("--color", choices=("auto", "always", "never"))
    parser.add_argument("-c", "--config")
    parser.add_argument("-f", "--overwrite", action="store_true")
    parser.add_argument("--install-hooks", action="store_true")
    parser.add_argument("-t", "--hook-type", action="append", choices=_PRECOMMIT_HOOK_TYPES)
    parser.add_argument("--allow-missing-config", action="store_true")
    return parser


_INSTALL_PARSER = _install_arg_parser()

# Shell redirection operators. These belong to the SHELL, not to `install`'s argument list —
# leaving `>` / `install.log` among the args made a genuinely-arming command read as stale
# (terra pass-9 FALSE-UNARMED). `2>&1` lexes as `2`, `>&`, `1`, hence the fd rule below.
_REDIRECT_OPS = frozenset({">", ">>", "<", "<<", "<<<", ">&", "<&", "&>", "&>>"})
_FD_RE = re.compile(r"^\d+$")
_SESSIONSTART_ARM_CMD = "python -m pre_commit install " + " ".join(
    f"-t {stage}" for stage in ARM_HOOK_TYPES
)
# Stable sentinel used to detect the verify leg in an armed settings.json (idempotency).
_SESSIONSTART_SENTINEL = "check_floor_hash.py"
# Both spellings of the arm leg a consumer may carry — `python -m pre_commit install` and the
# `pre-commit install` console script (deploy/floor_conformance.py reads the same pair). These
# are TOKENS, matched against the token preceding `install`, never substrings of the whole
# command: a substring test credits `install-hooks` and `echo "pre_commit install"` as arming.
_PRECOMMIT_TOKENS = ("pre_commit", "pre-commit")
_ARM_SUBCOMMAND = "install"
# Shell separators that end an invocation's argument list, so a stage flag in a neighbouring
# segment is never credited to `install` (terra HIGH, 2026-08-08). Newlines are boundaries too
# (terra pass-2 CRITICAL: a flag on a LATER line was credited to an earlier `install`).
_SHELL_SEPARATORS = frozenset({";", "&&", "||", "|", "&", "\n"})
# Leading `VAR=value` environment assignments, skipped when locating the command word.
_ENV_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
# The BOUNDED runner prefixes tolerated before the pre-commit word. Matched as SEQUENCES, not
# as a bag of allowed words (terra pass-3 CRITICAL: a word-set let `python pre-commit install`
# and `uv pre-commit install` through — neither invokes the pre-commit CLI, so both were a
# false PRESENT_CORRECT; a bare `run pre-commit install`, found while refuting, likewise).
_MODULE_RUNNERS = frozenset({"python", "python3", "py"})   # require `-m` before pre_commit
_SUBCOMMAND_RUNNERS = {"uv": "run", "poetry": "run", "pipx": "run"}  # require their subcommand
_BARE_RUNNERS = frozenset({"uvx"})                          # `uvx pre-commit ...`
_PY_VERSION_RE = re.compile(r"^-\d+(\.\d+)?$")              # `py -3` / `py -3.12`
# A trailing lone backslash continues the command on the next physical line (POSIX). Joined
# before segmentation so a continued arm command is not read as two under-armed segments.
# The backslash-newline is REMOVED, inserting nothing and consuming no following whitespace —
# POSIX deletes exactly those two characters, so `pre-\<newline>commit` is the single word
# `pre-commit`. Substituting a space split it into `pre-` + `commit` and argparse rejected the
# result, reading a correct consumer as stale (terra pass-10 FALSE-UNARMED). The space before
# the backslash and the next line's indentation are real separators and stay.
_LINE_CONTINUATION_RE = re.compile(r"\\\r?\n")
# Shell prefixes that transparently execute the command after them (`exec pre-commit install`
# really does install). Bounded on purpose: each of these EXECS what follows, unlike `echo`,
# which is why a permissive word bag was removed in pass 3 (terra pass-10).
_TRANSPARENT_PREFIXES = frozenset({"exec", "command", "env", "nohup"})
# pre-commit's own default stage when `install` names none. NOT a cardinality declaration —
# a recorded fact about the external tool, so a bare arm leg's diagnostic names the stages
# that are ACTUALLY dormant rather than claiming all of them are.
_PRECOMMIT_DEFAULT_STAGE = "pre-commit"

_SHA_RE = re.compile(r"[0-9a-f]{64}")


# ---------------------------------------------------------------------------
# Spec generation + arming READS. SHARED between detect/verify is D9-fine: these
# render/hash the SPEC (the corpus-state floor + the canonical guard bytes) and PARSE
# consumer files — they do not JUDGE the consumer's overall state (that is
# _classify_floor / _verify_floor, implemented twice).
# ---------------------------------------------------------------------------


def _corpus_floor() -> tuple[str, str]:
    """Render the floor from the hub template at corpus state -> (body, sha256).

    The template content IS the shipped floor body (deterministic — same template ->
    same hash). Refuses if the hub template violates a binding rule (it never should;
    the shipped template is canonical), so a broken hub floor fails loud rather than
    silently deploying garbage.
    """
    floor = gf.render_floor()
    issues = gf.validate(floor)
    if issues:
        raise RuntimeError(f"hub floor template failed validation: {issues}")
    return floor, gf.floor_sha256(floor)


def _guard_script() -> str:
    """The canonical guard-script bytes both legs run (LF, single trailing newline)."""
    return gf.CHECK_FLOOR_HASH_SCRIPT


def _read_sidecar_hash(sidecar_path: Path) -> str:
    """Extract the 64-hex digest recorded in the sidecar ('' if absent/unparsable)."""
    if not sidecar_path.exists():
        return ""
    m = _SHA_RE.search(sidecar_path.read_text(encoding="utf-8"))
    return m.group(0) if m else ""


def _read_text(path: Path) -> str:
    """Read a consumer file's text ('' if absent). LF-normalized so checks are
    autocrlf-proof (a Windows checkout can't flip a byte-clean match to a miss)."""
    if not path.exists():
        return ""
    return gf.normalize(path.read_text(encoding="utf-8"))


def _load_settings(path: Path) -> dict[str, Any]:
    """Parse the consumer's .claude/settings.json ({} if absent/blank/non-object)."""
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    data = json.loads(raw)
    return data if isinstance(data, dict) else {}


def _sessionstart_groups(data: dict[str, Any]) -> list[dict[str, Any]]:
    """The SessionStart matcher groups in a parsed settings.json (live references, so the
    apply path can repair a leg in place rather than appending a duplicate block)."""
    return [
        g
        for g in (data.get("hooks", {}) or {}).get("SessionStart", []) or []
        if isinstance(g, dict)
    ]


def _sessionstart_hooks(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Every SessionStart hook dict, flattened across matcher groups (live references)."""
    hooks: list[dict[str, Any]] = []
    for group in _sessionstart_groups(data):
        hooks.extend(h for h in group.get("hooks", []) or [] if isinstance(h, dict))
    return hooks


def _hook_command(hook: dict[str, Any]) -> str:
    """One hook dict's command string ('' when absent or not a string)."""
    cmd = hook.get("command")
    return cmd if isinstance(cmd, str) else ""


def _settings_sessionstart_commands(data: dict[str, Any]) -> list[str]:
    """Every SessionStart hook command string in a parsed settings.json (order-free)."""
    return [c for c in (_hook_command(h) for h in _sessionstart_hooks(data)) if c]


def _basename(tok: str) -> str:
    """A command token reduced to its comparable program name: path stripped, `.exe` dropped,
    casefolded (Windows executable names are case-insensitive)."""
    base = tok.replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return base[:-4] if base.endswith(".exe") else base


def _is_precommit_exe(tok: str) -> bool:
    """True when a token names pre-commit itself (`pre_commit`, `pre-commit`, a path to
    either, or the Windows `.exe` shim) — not merely mentions it.

    Case-INSENSITIVE: Windows executable names are, so `...\\PRE-COMMIT.EXE` is the same
    program as `pre-commit` and must not read as un-armed (terra pass-3 HIGH). The cost is
    that a POSIX file deliberately named `PRE-COMMIT` would also match — accepted, since
    such a file being something OTHER than pre-commit is not a real configuration.
    """
    return _basename(tok) in _PRECOMMIT_TOKENS


def _command_segments(cmd: str) -> list[list[str]] | None:
    """A SessionStart command string as one token list per shell segment, or None if the
    command is not valid shell at all (so nothing in it runs).

    Shell-aware (terra pass-2, 2026-08-08): quoting is resolved, so ``-t 'pre-commit'`` names
    the stage it obviously names — a naive ``.split()`` kept the quotes, read the command as
    under-armed, and would have had `apply` REWRITE a genuinely correct consumer, which is
    the more damaging direction of error. Separators (including newlines) end a segment so a
    flag on one line or after a ``;`` is never credited to an `install` on another.

    An unparsable command (unbalanced quotes) falls back to whitespace splitting: an
    imperfect read that under-counts is safe here — it can only produce a repairable
    not-armed verdict, never a false armed one.
    """
    segments: list[list[str]] = []
    current: list[str] = []
    for line in _LINE_CONTINUATION_RE.sub("", cmd).splitlines():
        try:
            lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
            lexer.whitespace_split = True
            # Backslash is a PATH separator here, not an escape: this fleet is Windows-primary
            # and posix lexing otherwise turns `C:\venv\Scripts\pre-commit.exe` into
            # `C:venvScriptspre-commit.exe`, so a correctly-armed Windows consumer would read
            # as not-armed. Quote handling (the reason for posix=True) is unaffected.
            lexer.escape = ""
            toks = list(lexer)
        except ValueError:
            # Unbalanced quotes: fall back to whitespace splitting, stripping the quotes the
            # lexer would have resolved so a stage name is still readable.
            toks = [t.strip("'\"") for t in line.split()]
        for tok in toks:
            if tok in _SHELL_SEPARATORS:
                segments.append(current)
                current = []
            else:
                current.append(tok)
        segments.append(current)  # end of line == end of segment
        current = []
    cleaned: list[list[str]] = []
    for segment in segments:
        without_redirects = _strip_redirections(segment)
        if without_redirects is None:
            return None  # a shell syntax error anywhere means the command never runs
        if without_redirects:
            cleaned.append(without_redirects)
    return cleaned


def _strip_redirections(toks: list[str]) -> list[str] | None:
    """A segment's tokens with shell redirections removed, or None if it is a SYNTAX ERROR.

    `pre-commit install -t … >install.log` really does install; the redirection is the shell's
    business, not an argument to `install`. Leaving `>` and `install.log` in the argument list
    made argparse reject them as positionals, so a genuinely-arming consumer read as stale and
    `apply` would rewrite its command (terra pass-9 FALSE-UNARMED).

    A redirection operator with NO target (`… -t pre-push >`) is a shell syntax error: the
    shell never runs the command, so nothing is installed. Dropping the operator left a
    well-formed argument list behind and the command read as fully armed — a false
    PRESENT_CORRECT (terra pass-11). Such a segment now poisons the whole command.
    """
    out: list[str] = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        # `2>&1` lexes as `2`, `>&`, `1` — a bare fd number before an operator belongs to it
        if _FD_RE.match(tok) and i + 1 < len(toks) and toks[i + 1] in _REDIRECT_OPS:
            i += 1
            continue
        if tok in _REDIRECT_OPS:
            if i + 1 >= len(toks):
                return None  # dangling operator -> shell syntax error -> nothing runs
            i += 2  # the operator and its target
            continue
        out.append(tok)
        i += 1
    return out


def _install_invocations(cmd: str) -> list[list[str]]:
    """The ARGUMENT list of each real `pre-commit install` invocation inside a command string.

    Requires pre-commit to be the command being INVOKED, not merely a token that appears
    somewhere (terra 2026-08-08, both passes — the first draft scanned every token, so
    ``pre_commit install-hooks -t ...`` read as fully armed; the second bound flags to the
    preceding token only, so ``echo pre-commit install -t ...`` did too. A false
    PRESENT_CORRECT is precisely the dormant-stage defect these teeth exist to catch):

    - per segment, leading ``VAR=value`` assignments are skipped, then a BOUNDED runner
      prefix (``python -m``, ``uv run``, ...) is walked to reach the command word;
    - anything else in command position means pre-commit is not being invoked -> no invocation;
    - the subcommand must be exactly ``install`` — which rejects ``install-hooks`` and ``run``;
    - the invocation's arguments are the rest of its segment.

    Returns [] when the command performs no `pre-commit install`. **Stated limit:** a command
    that hides the invocation from static reading (``sh -c '...'``, a shell function, a
    wrapper script) is NOT recognised, so it reads as no arm leg. That is deliberate and
    fail-safe: `apply` then ADDS a canonical arm leg beside it and never rewrites the opaque
    command, so a wrapper's behaviour is preserved even when it cannot be understood.
    """
    invocations: list[list[str]] = []
    for toks in _command_segments(cmd) or ():
        rest = _precommit_args(toks)
        if rest is not None and rest[:1] == [_ARM_SUBCOMMAND]:
            invocations.append(rest[1:])
    return invocations


def _precommit_args(toks: list[str]) -> list[str] | None:
    """One segment's tokens after the pre-commit invocation, or None if it invokes something
    else. The runner prefix is matched as a SEQUENCE — a permissive word-set accepted
    `python pre-commit install` and `run pre-commit install`, neither of which reaches the
    pre-commit CLI, so both read as armed (terra pass-3 CRITICAL + one found refuting it)."""
    i = 0
    # Leading `VAR=value` assignments and transparent exec prefixes (`exec`, `env`, ...) —
    # neither changes WHICH command runs, so skip past them to the real command word.
    while i < len(toks) and (
        _ENV_ASSIGN_RE.match(toks[i]) or _basename(toks[i]) in _TRANSPARENT_PREFIXES
    ):
        i += 1
    if i >= len(toks):
        return None
    if _is_precommit_exe(toks[i]):            # `pre-commit install ...`
        return toks[i + 1 :]
    head = _basename(toks[i])
    if head in _MODULE_RUNNERS:               # `python [-3.12] -m pre_commit install ...`
        j = i + 1
        while j < len(toks) and _PY_VERSION_RE.match(toks[j]):
            j += 1
        if toks[j : j + 1] == ["-m"] and j + 1 < len(toks) and _is_precommit_exe(toks[j + 1]):
            return toks[j + 2 :]
        return None
    if head in _SUBCOMMAND_RUNNERS:           # `uv run pre-commit install ...`
        if (
            toks[i + 1 : i + 2] == [_SUBCOMMAND_RUNNERS[head]]
            and i + 2 < len(toks)
            and _is_precommit_exe(toks[i + 2])
        ):
            return toks[i + 3 :]
        return None
    if head in _BARE_RUNNERS:                 # `uvx pre-commit install ...`
        if i + 1 < len(toks) and _is_precommit_exe(toks[i + 1]):
            return toks[i + 2 :]
        return None
    return None


def _stage_flags(args: list[str]) -> set[str] | None:
    """Stage names one install invocation names, or None if that invocation would FAIL.

    Asks **argparse**, because argparse is what decides this at runtime. None means the
    invocation installs NOTHING — a rejected argument (unknown option, missing value, a value
    outside pre-commit's `choices=` for `-t` or `--color`, a positional, an ambiguous
    abbreviation) exits non-zero BEFORE anything is installed, and `-h/--help` prints usage and
    exits without dispatching. Crediting such a command's valid stage flags is a false
    PRESENT_CORRECT — the dormant-stage defect these teeth exist to catch.

    An empty set means the invocation SUCCEEDS but names no stage, which is the #275 under-arm
    (pre-commit's own default is the pre-commit stage alone). A valid but unmanaged type
    (``post-commit``) is no error and simply contributes no managed stage.
    """
    try:
        # argparse writes usage/errors to the real streams and exits; swallow both.
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            parsed = _INSTALL_PARSER.parse_args(args)
    except (SystemExit, argparse.ArgumentError):
        return None
    return set(parsed.hook_type or ())


def _is_arm_command(cmd: str) -> bool:
    """True when a SessionStart command string performs a real `pre-commit install`."""
    return bool(_install_invocations(cmd))


def _armed_stages(cmd: str) -> frozenset[str]:
    """The managed hook stages ONE SessionStart command actually installs.

    An invocation naming no stage falls back to pre-commit's own default (the pre-commit
    stage alone) — precisely the #275 under-arm. A command performing NO install returns the
    EMPTY set: the default-stage fallback is a property of an invocation, never of a command
    that has none, or an unrelated SessionStart hook would contribute a phantom stage to the
    coverage union. An invocation that would FAIL argument parsing contributes nothing, since
    it installs nothing. Valid-but-unmanaged stages are ignored.
    """
    stages: set[str] = set()
    for args in _install_invocations(cmd):
        named = _stage_flags(args)
        if named is None:
            continue  # this invocation errors out -> it arms nothing
        stages |= named or {_PRECOMMIT_DEFAULT_STAGE}
    return frozenset(stages) & _ARM_STAGES


# ---------------------------------------------------------------------------
# detect path — _classify_floor (detect's correctness judgment). Its OWN presence
# checks; shares no judgment helper with _verify_floor (D9).
# ---------------------------------------------------------------------------


def _classify_floor(
    corpus_digest: str,
    floor_path: Path,
    sidecar_path: Path,
    claude_md_path: Path,
    hook_script_path: Path,
    gitignore_path: Path,
    settings_path: Path,
) -> CarrierState:
    """detect's judgment: floor + sidecar + every arming artifact -> CarrierState.

    absent floor -> ABSENT; floor content AND sidecar both hash to the corpus floor AND
    every arming artifact present/correct -> PRESENT_CORRECT; anything else (floor
    edited, corpus moved, sidecar missing/stale, or an arming artifact missing/wrong) ->
    PRESENT_DRIFTED.
    """
    if not floor_path.exists():
        return CarrierState.ABSENT
    actual = gf.floor_sha256(floor_path.read_text(encoding="utf-8"))
    recorded = _read_sidecar_hash(sidecar_path)
    floor_ok = actual == corpus_digest and recorded == corpus_digest

    # Arming presence checks (detect's own expressions).
    include_ok = INCLUDE_LINE in _read_text(claude_md_path)
    hook_ok = _read_text(hook_script_path) == gf.normalize(_guard_script())
    gi_lines = [ln.strip() for ln in _read_text(gitignore_path).splitlines()]
    gitignore_ok = _GITIGNORE_CONTENTS_FORM in gi_lines and all(
        neg in gi_lines for neg in _GITIGNORE_NEGATIONS
    )
    ss_cmds = _settings_sessionstart_commands(_load_settings(settings_path))
    # BOTH legs, and the arm leg at full stage cardinality (#290): a verify-leg-only check
    # passes a consumer whose commit-msg / pre-push stages never arm. detect accumulates and
    # compares with its OWN expressions (a subset test over its own union) — only the
    # per-command PARSE is shared with verify, the same latitude _read_sidecar_hash takes.
    detect_armed: set[str] = set()
    for cmd in ss_cmds:
        detect_armed |= _armed_stages(cmd)
    settings_ok = any(_SESSIONSTART_SENTINEL in cmd for cmd in ss_cmds) and _ARM_STAGES.issubset(
        detect_armed
    )

    if floor_ok and include_ok and hook_ok and gitignore_ok and settings_ok:
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN re-reads + its OWN checks;
# shares no correctness-judgment helper with _classify_floor.
# ---------------------------------------------------------------------------


def _verify_floor(
    corpus_digest: str,
    floor_path: Path,
    sidecar_path: Path,
    claude_md_path: Path,
    hook_script_path: Path,
    gitignore_path: Path,
    settings_path: Path,
) -> list[str]:
    """verify's independent judgment: re-check fresh, return unmet requirements.

    Built so a bug in detect's _classify_floor cannot be mirrored here: it re-derives
    each requirement directly + separately. Empty list => target satisfied + armed.
    """
    failures: list[str] = []
    if not floor_path.exists():
        failures.append(f"floor absent: {floor_path}")
        return failures
    actual = gf.floor_sha256(floor_path.read_text(encoding="utf-8"))
    if actual != corpus_digest:
        failures.append(
            f"floor content hash {actual[:12]} != corpus floor {corpus_digest[:12]}"
        )
    if not sidecar_path.exists():
        failures.append(f"sidecar absent: {sidecar_path}")
    else:
        recorded = _read_sidecar_hash(sidecar_path)
        if recorded != corpus_digest:
            failures.append(
                f"sidecar hash {recorded[:12] or '(none)'} != corpus floor "
                f"{corpus_digest[:12]}"
            )
    # Arming requirements — verify's own independent reads.
    if INCLUDE_LINE not in _read_text(claude_md_path):
        failures.append(f"CLAUDE.md missing @-include: {claude_md_path}")
    if _read_text(hook_script_path) != gf.normalize(_guard_script()):
        failures.append(f"hash-guard script missing/wrong: {hook_script_path}")
    gi = [ln.strip() for ln in _read_text(gitignore_path).splitlines()]
    missing_gi = [n for n in _GITIGNORE_NEGATIONS if n not in gi]
    if _GITIGNORE_CONTENTS_FORM not in gi or missing_gi:
        failures.append(f".gitignore missing floor negation block: {gitignore_path}")
    ss_cmds = _settings_sessionstart_commands(_load_settings(settings_path))
    if not any(_SESSIONSTART_SENTINEL in c for c in ss_cmds):
        failures.append(f"settings.json missing SessionStart guard hook: {settings_path}")
    # The arm leg, asserted at full stage cardinality (#290) and NAMING the dormant stages —
    # verify's own expression of the requirement, not detect's subset test.
    arm_cmds = [c for c in ss_cmds if _is_arm_command(c)]
    if not arm_cmds:
        failures.append(f"settings.json missing SessionStart arm hook: {settings_path}")
    else:
        armed: set[str] = set()
        for cmd in arm_cmds:
            armed.update(_armed_stages(cmd))
        dormant = [stage for stage in ARM_HOOK_TYPES if stage not in armed]
        if dormant:
            failures.append(
                f"SessionStart arm leg arms {len(armed)}/{len(ARM_HOOK_TYPES)} managed hook "
                f"stage(s) — {', '.join(dormant)} would land wired-but-dormant: "
                f"{settings_path}"
            )
    return failures


# ---------------------------------------------------------------------------
# apply path — idempotent per-artifact ensures. Each returns a change description or
# None (already correct). apply writes/stages only; the operator commits (commit-no).
# ---------------------------------------------------------------------------


def _write_lf(path: Path, text: str) -> None:
    """Write text with LF newlines (no platform translation) so on-disk bytes match."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _ensure_hook_script(path: Path) -> str | None:
    desired = gf.normalize(_guard_script())
    if _read_text(path) == desired:
        return None
    existed = path.exists()
    _write_lf(path, desired)
    return f"{'updated' if existed else 'wrote'} {path}"


def _insert_include(text: str) -> str:
    """Return CLAUDE.md text with the @-include added. After the YAML frontmatter block
    if present, else at the top. Idempotency is the caller's (checks INCLUDE_LINE first).
    """
    block = f"{INCLUDE_LINE}\n"
    if not text.strip():
        return block
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                head = "".join(lines[: i + 1])
                tail = "".join(lines[i + 1 :])
                return f"{head}\n{block}{tail}"
    return f"{block}\n{text}"


def _ensure_include(path: Path) -> str | None:
    text = _read_text(path)
    if INCLUDE_LINE in text:
        return None
    existed = path.exists()
    _write_lf(path, _insert_include(text))
    return f"{'updated' if existed else 'wrote'} {path} (@-include)"


def _reconcile_gitignore(lines: list[str]) -> list[str]:
    """Return .gitignore lines with the `.claude/*` + negation block ensured.

    A bare `.claude/` DIRECTORY line is replaced by the contents-form + negations
    (a bare dir exclusion defeats negations, #138). An existing `.claude/*` gets any
    missing negations inserted right after it. Neither present -> append the block.
    """
    block = [_GITIGNORE_CONTENTS_FORM, *_GITIGNORE_NEGATIONS]
    stripped = [ln.strip() for ln in lines]
    bare = f"{gf.CHILD_CLAUDE_DIRNAME}/"
    if bare in stripped:
        i = stripped.index(bare)
        return lines[:i] + block + lines[i + 1 :]
    if _GITIGNORE_CONTENTS_FORM in stripped:
        i = stripped.index(_GITIGNORE_CONTENTS_FORM)
        missing = [n for n in _GITIGNORE_NEGATIONS if n not in stripped]
        return lines[: i + 1] + missing + lines[i + 1 :]
    return lines + block


def _ensure_gitignore(path: Path) -> str | None:
    lines = _read_text(path).splitlines()
    stripped = [ln.strip() for ln in lines]
    if _GITIGNORE_CONTENTS_FORM in stripped and all(
        n in stripped for n in _GITIGNORE_NEGATIONS
    ):
        return None
    existed = path.exists()
    _write_lf(path, "\n".join(_reconcile_gitignore(lines)) + "\n")
    return f"{'updated' if existed else 'wrote'} {path} (floor negation block)"


def _host_group(
    data: dict[str, Any], known: list[dict[str, Any]]
) -> dict[str, Any] | None:
    """The SessionStart group already carrying one of ``known`` (identity match), so a missing
    leg joins the existing guard block instead of appending a second one. None if there is no
    guard block yet (the greenfield case)."""
    for group in _sessionstart_groups(data):
        entries = group.get("hooks")
        if isinstance(entries, list) and any(e is k for e in entries for k in known):
            return group
    return None


def _verify_leg() -> dict[str, Any]:
    return {"type": "command", "command": _SESSIONSTART_VERIFY_CMD, "timeout": 10}


def _arm_leg() -> dict[str, Any]:
    return {"type": "command", "command": _SESSIONSTART_ARM_CMD, "timeout": 30}


def _ensure_settings(path: Path) -> str | None:
    """Ensure the SessionStart block carries the verify leg AND a FULLY-armed arm leg.

    The narrowest repair that closes each gap — #290 (b), the self-heal that makes every
    verdict the (a) teeth can now return REPAIRABLE (a DRIFTED `apply` cannot fix was the
    stated reason this pair was deferred together):

    - both legs present and every managed stage covered -> ``None`` (idempotent no-op);
    - an arm leg present but under-armed (a pre-#275b 1-stage arm) -> **only that command
      string** is rewritten to the full-cardinality form. The hook's other keys, the verify
      leg, sibling hooks, matcher groups, ordering, and every unrelated ``settings.json`` key
      are left exactly as found — a re-deploy must not rewrite config this carrier does not
      own;
    - exactly one leg present -> the missing leg is appended to the group already carrying
      one, not as a duplicate guard block;
    - no guard block at all (greenfield) -> append the canonical two-leg block.

    Stage coverage is judged as a UNION across arm legs (a consumer may legitimately split
    arming across two commands), so a split-but-complete arm is correctly a no-op.
    """
    data = _load_settings(path)
    hooks = _sessionstart_hooks(data)
    verify_legs = [h for h in hooks if _SESSIONSTART_SENTINEL in _hook_command(h)]
    arm_legs = [h for h in hooks if _is_arm_command(_hook_command(h))]
    covered: set[str] = set()
    for hook in arm_legs:
        covered.update(_armed_stages(_hook_command(hook)))
    dormant = sorted(_ARM_STAGES - covered)

    if verify_legs and arm_legs and not dormant:
        return None

    existed = path.exists()
    notes: list[str] = []

    if arm_legs and dormant:
        # Self-heal IN PLACE: rewrite the command STRING of the first under-armed leg and
        # nothing else. Coverage is a union, so healing one leg restores every dormant stage.
        stale = next(
            h for h in arm_legs if not _ARM_STAGES.issubset(_armed_stages(_hook_command(h)))
        )
        stale["command"] = _SESSIONSTART_ARM_CMD
        notes.append(f"self-healed stale arm leg (dormant: {', '.join(dormant)})")

    missing = [("verify", _verify_leg())] if not verify_legs else []
    if not arm_legs:
        missing.append(("arm", _arm_leg()))
    if missing:
        host = _host_group(data, verify_legs + arm_legs)
        if host is None:
            # No guard block at all -> the canonical block (greenfield: both legs).
            data.setdefault("hooks", {}).setdefault("SessionStart", []).append(
                {"matcher": "", "hooks": [leg for _, leg in missing]}
            )
            notes.append("SessionStart guard hook")
        else:
            host["hooks"].extend(leg for _, leg in missing)
            notes.append(f"added the missing {' + '.join(n for n, _ in missing)} leg(s)")

    _write_lf(path, json.dumps(data, indent=2) + "\n")
    return f"{'updated' if existed else 'wrote'} {path} ({'; '.join(notes)})"


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class FloorCarrier(Carrier):
    """Per-repo methodology-floor carrier — bound to one consumer repo."""

    carrier_id = CARRIER_ID

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def _floor_path(self, target: Any) -> Path:
        return self.repo_root / (target or {}).get("floor_path", DEFAULT_FLOOR_REL)

    def _sidecar_path(self, target: Any) -> Path:
        return self.repo_root / (target or {}).get("sidecar_path", DEFAULT_SIDECAR_REL)

    def _hook_script_path(self) -> Path:
        return self.repo_root / HOOK_SCRIPT_REL

    def _claude_md_path(self) -> Path:
        return self.repo_root / CLAUDE_MD_REL

    def _gitignore_path(self) -> Path:
        return self.repo_root / GITIGNORE_REL

    def _settings_path(self) -> Path:
        return self.repo_root / SETTINGS_REL

    def detect(self, target: Any) -> CarrierState:
        _, corpus_digest = _corpus_floor()
        state = _classify_floor(
            corpus_digest,
            self._floor_path(target),
            self._sidecar_path(target),
            self._claude_md_path(),
            self._hook_script_path(),
            self._gitignore_path(),
            self._settings_path(),
        )
        log.debug("floor detect: %s -> %s", self._floor_path(target), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        floor, corpus_digest = _corpus_floor()
        fpath = self._floor_path(target)
        spath = self._sidecar_path(target)
        changes: list[str] = []

        # Floor + sidecar (idempotent: only write on a real change).
        floor_ok = (
            fpath.exists()
            and gf.floor_sha256(fpath.read_text(encoding="utf-8")) == corpus_digest
        )
        sidecar_ok = _read_sidecar_hash(spath) == corpus_digest
        if not (floor_ok and sidecar_ok):
            floor_existed = fpath.exists()
            sidecar_existed = spath.exists()
            # render_floor already returns LF-normalized text w/ a single trailing NL;
            # newline="\n" prevents Windows CRLF translation so on-disk bytes match the
            # hash (byte-identical to what generate_floor.py --out-dir would write,
            # minus the hub-SHA refresh this carrier deliberately omits).
            _write_lf(fpath, floor)
            _write_lf(spath, f"{corpus_digest}\n")
            changes.append(f"{'updated' if floor_existed else 'wrote'} {fpath}")
            changes.append(f"{'updated' if sidecar_existed else 'wrote'} {spath}")

        # Arming artifacts (each idempotent; None => already correct).
        for change in (
            _ensure_hook_script(self._hook_script_path()),
            _ensure_include(self._claude_md_path()),
            _ensure_gitignore(self._gitignore_path()),
            _ensure_settings(self._settings_path()),
        ):
            if change is not None:
                changes.append(change)

        if not changes:
            return ApplyResult(changed=False, detail="floor already armed at corpus state")
        log.info("floor apply: %s -> %d change(s)", fpath, len(changes))
        return ApplyResult(
            changed=True,
            changes=tuple(changes),
            detail=f"floor armed at {corpus_digest[:12]} ({len(changes)} change(s))",
        )

    def verify(self, target: Any) -> VerifyResult:
        # Independent re-check — does NOT call _classify_floor (D9).
        _, corpus_digest = _corpus_floor()
        failures = _verify_floor(
            corpus_digest,
            self._floor_path(target),
            self._sidecar_path(target),
            self._claude_md_path(),
            self._hook_script_path(),
            self._gitignore_path(),
            self._settings_path(),
        )
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail="floor armed at corpus state"
            if ok
            else f"{len(failures)} unmet requirement(s)",
        )
