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
   (b) ``python -m pre_commit install`` — idempotently bootstraps the commit-time git
   hook, which git never lets travel with a clone. The first CC session auto-arms it.

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
artifact missing/wrong).

D9 (ADR-92 Decision 9): ``_classify_floor`` (detect's judgment) and ``_verify_floor``
(verify's judgment) are distinct functions with no shared correctness-judgment helper.
``render_floor``/``floor_sha256``/``_read_sidecar_hash`` + the arming READ helpers are
shared SPEC reads/parsers (D9-permitted, like target-parsing) — the JUDGMENT
(compare-to-corpus, presence checks) is implemented twice, independently.
"""

from __future__ import annotations

import json
import logging
import re
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
# Arm ALL THREE managed hook stages (#275b): a bare `pre_commit install` arms the
# pre-commit stage ONLY, so commit-msg / pre-push stage hooks land wired-but-dormant on a
# fresh consumer. The `-t` flags mirror the hub's own 3-stage self-arm (scripts/arm_hooks.py).
_SESSIONSTART_ARM_CMD = "python -m pre_commit install -t pre-commit -t commit-msg -t pre-push"
# Stable sentinel used to detect an already-armed settings.json (idempotency).
_SESSIONSTART_SENTINEL = "check_floor_hash.py"

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


def _settings_sessionstart_commands(data: dict[str, Any]) -> list[str]:
    """Every SessionStart hook command string in a parsed settings.json (order-free)."""
    cmds: list[str] = []
    for group in (data.get("hooks", {}) or {}).get("SessionStart", []) or []:
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []) or []:
            if isinstance(hook, dict) and isinstance(hook.get("command"), str):
                cmds.append(hook["command"])
    return cmds


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
    settings_ok = any(
        _SESSIONSTART_SENTINEL in cmd
        for cmd in _settings_sessionstart_commands(_load_settings(settings_path))
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


def _ensure_settings(path: Path) -> str | None:
    data = _load_settings(path)
    if any(
        _SESSIONSTART_SENTINEL in c for c in _settings_sessionstart_commands(data)
    ):
        return None
    existed = path.exists()
    hooks = data.setdefault("hooks", {})
    sessionstart = hooks.setdefault("SessionStart", [])
    sessionstart.append(
        {
            "matcher": "",
            "hooks": [
                {"type": "command", "command": _SESSIONSTART_VERIFY_CMD, "timeout": 10},
                {"type": "command", "command": _SESSIONSTART_ARM_CMD, "timeout": 30},
            ],
        }
    )
    _write_lf(path, json.dumps(data, indent=2) + "\n")
    return f"{'updated' if existed else 'wrote'} {path} (SessionStart guard hook)"


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
