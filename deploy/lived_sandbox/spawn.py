"""Lived-workflow sandbox — SPAWN + clone/teardown layer (Slice A; Fable review §6).

Runs a headless `claude -p` session under an ISOLATED CLAUDE_CONFIG_DIR so the child does NOT
inherit the outer machine's ~/.claude L0 hooks — THE correctness property (proven by
isolation.py). Reuses the floor_conformance / enforcement_coverage clone+teardown precedent
verbatim: own `.git`, per-run PRE_COMMIT_HOME, `_rmtree_guarded` blast-radius teardown. Not a
worktree (ADR-68 shared .git/stash), not a container (Windows-native fidelity is the point).

Auth (change #4): the child authenticates by ANTHROPIC_API_KEY (from the env, which the
operator's profile loads from .secrets/.env) — NEVER a copied ~/.claude credential, which would
risk dragging outer settings/hooks into the "isolated" config and measuring the workstation.
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

# Reuse floor_conformance's clone/teardown helpers. enforcement_coverage._cloned_consumer imports
# the same privates the same way (deploy/ is on sys.path, not a package) — sanctioned reuse.
_DEPLOY = Path(__file__).resolve().parent.parent
if str(_DEPLOY) not in sys.path:
    sys.path.insert(0, str(_DEPLOY))
import floor_conformance as _fc  # noqa: E402

DEFAULT_MODEL = "sonnet"
CLAUDE_BIN = "claude"

# Env keys the child KEEPS (Windows-native fidelity: profile/system vars stay). Everything else —
# notably the outer CLAUDE_CONFIG_DIR / CLAUDE_PROJECT_DIR — is dropped so nothing leaks the
# outer session (environment-is-spec, LESSONS 2026-06-05; the $CLAUDE_PROJECT_DIR trap, #237).
_KEEP_ENV = (
    "PATH", "SYSTEMROOT", "SystemRoot", "USERPROFILE", "HOMEDRIVE", "HOMEPATH",
    "TEMP", "TMP", "APPDATA", "LOCALAPPDATA", "COMSPEC", "PATHEXT", "WINDIR", "NUMBER_OF_PROCESSORS",
)


class SandboxError(RuntimeError):
    """A spawn/isolation precondition failed (auth missing, clone failed, etc.)."""


def load_api_key() -> str:
    """The child's ANTHROPIC_API_KEY (change #4: from .secrets/.env, never a copied cred file).

    Env first (the operator's PowerShell profile loads .secrets/.env into it); then a `.env`
    file pointed at by DEV_SECRETS_ENV. No secrets path is hardcoded in the committed module.
    """
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    secrets = os.environ.get("DEV_SECRETS_ENV", "").strip()
    if secrets and Path(secrets).exists():
        for line in Path(secrets).read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\s*(?:export\s+)?ANTHROPIC_API_KEY\s*=\s*(.+)", line)
            if m:
                return m.group(1).strip().strip('"').strip("'").rstrip("\r")
    raise SandboxError(
        "ANTHROPIC_API_KEY not in env and DEV_SECRETS_ENV unset/keyless — the isolated child "
        "cannot authenticate. Run from a shell whose profile loaded the key, or set "
        "DEV_SECRETS_ENV to a .env carrying ANTHROPIC_API_KEY (change #4).")


def _hook_print(marker: str) -> str:
    """A portable SessionStart-hook command that prints `marker` to stdout (JSON-embeddable).

    json.dumps escapes the inner double quotes; the empirically-verified form is
    `python -c "print('<marker>')"`, which fires under `claude -p` on Windows.
    """
    if not re.fullmatch(r"[A-Za-z0-9_]+", marker):
        raise SandboxError(f"marker must be [A-Za-z0-9_]+ (got {marker!r})")
    return f"python -c \"print('{marker}')\""


def write_isolated_config(config_dir: Path, *, session_start_marker: str | None = None,
                          allow_rules: tuple[str, ...] | None = None) -> Path:
    """Create an ISOLATED CLAUDE_CONFIG_DIR seeded with a minimal settings.json.

    Empty hooks by default. If `session_start_marker` is given, install ONE SessionStart hook
    that prints it — the isolation POSITIVE control (a user-level hook that fires iff this config
    is the one the child reads). Because CLAUDE_CONFIG_DIR points here, the child never consults
    the real ~/.claude, so an outer L0 hook living only there cannot fire.

    `allow_rules` ([#253a]): the harness OWNS this config, so it seeds a SCOPED permission
    allowlist — exactly the operations the sanctioned arc needs, enumerated by the caller.
    NEVER a bypass: no bypassPermissions / defaultMode escape is ever written here; anything
    outside the allowlist still hits the normal permission wall.
    """
    config_dir = Path(config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    settings: dict = {"hooks": {}}
    if session_start_marker:
        settings["hooks"] = {"SessionStart": [
            {"matcher": "", "hooks": [{"type": "command", "command": _hook_print(session_start_marker)}]}]}
    if allow_rules:
        settings["permissions"] = {"allow": list(allow_rules)}
    (config_dir / "settings.json").write_text(
        json.dumps(settings, indent=2), encoding="utf-8", newline="\n")
    return config_dir


@dataclass
class SpawnResult:
    """The captured, deterministic evidence of one child run — the inner agent's narration is
    never consulted for a verdict; only these channels are."""
    exit_code: int
    stdout: str
    events: list[dict]
    transcript_path: Path | None
    config_dir: Path
    work_dir: Path

    def transcript_text(self) -> str:
        """stdout + every on-disk transcript under this run's isolated config — the substring
        surface for marker/hook scans (robust to which project-slug the transcript landed under)."""
        parts = [self.stdout]
        proj = Path(self.config_dir) / "projects"
        if proj.exists():
            for jsonl in proj.rglob("*.jsonl"):
                parts.append(jsonl.read_text(encoding="utf-8", errors="replace"))
        return "\n".join(parts)

    def contains(self, needle: str) -> bool:
        return needle in self.transcript_text()


def _child_env(config_dir: Path, api_key: str, extra_env: dict | None) -> dict:
    env = {k: v for k, v in os.environ.items() if k in _KEEP_ENV}
    if extra_env:
        env.update(extra_env)
    # Pin the isolation-critical keys LAST so extra_env can NEVER override them (Codex HIGH
    # 2026-07-04): a caller may add e.g. PRE_COMMIT_HOME, but cannot redirect the isolated config,
    # swap the credential, or reintroduce the outer CLAUDE_PROJECT_DIR (#237).
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    env["ANTHROPIC_API_KEY"] = api_key
    env.pop("CLAUDE_PROJECT_DIR", None)
    return env


def _parse_stream(stdout: str) -> list[dict]:
    events: list[dict] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        with contextlib.suppress(json.JSONDecodeError):
            events.append(json.loads(line))
    return events


def _find_transcript(config_dir: Path) -> Path | None:
    proj = Path(config_dir) / "projects"
    if not proj.exists():
        return None
    jsonls = sorted(proj.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return jsonls[0] if jsonls else None


def spawn(work_dir: Path, prompt: str, *, config_dir: Path, api_key: str,
          model: str = DEFAULT_MODEL, extra_env: dict | None = None,
          timeout: int = 180) -> SpawnResult:
    """Run a headless `claude -p` session in `work_dir` under the isolated `config_dir`.

    Sonnet by default (budget: mechanical lifecycle-driving; never Opus-by-inheritance). Captures
    the stream-json stdout, the parsed events, and the on-disk transcript. The env is scrubbed to
    `_KEEP_ENV` + the isolated CLAUDE_CONFIG_DIR + the API key; the outer CLAUDE_* are dropped.
    """
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    env = _child_env(Path(config_dir), api_key, extra_env)
    # Normalize launch failures to SandboxError — the CLI is the operator stop point, so a missing
    # `claude` / timeout / OS error must surface cleanly, not as a raw traceback (Codex HIGH 2026-07-04).
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose"],
            cwd=str(work_dir), env=env, capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise SandboxError(f"`{CLAUDE_BIN}` not found on PATH — cannot spawn the child session") from exc
    except subprocess.TimeoutExpired as exc:
        raise SandboxError(f"child `claude -p` timed out after {timeout}s") from exc
    except OSError as exc:
        raise SandboxError(f"failed to launch `{CLAUDE_BIN}`: {exc}") from exc
    return SpawnResult(
        exit_code=proc.returncode,
        stdout=proc.stdout + ("\n" + proc.stderr if proc.stderr else ""),
        events=_parse_stream(proc.stdout),
        transcript_path=_find_transcript(Path(config_dir)),
        config_dir=Path(config_dir),
        work_dir=work_dir,
    )


@contextlib.contextmanager
def sandbox_clone(source_repo: Path, prefix: str = "lived-sandbox-") -> Iterator[tuple[Path, dict[str, str]]]:
    """Yield (clone_path, env) — a throwaway clone of `source_repo` with its OWN .git, plain-delete
    teardown, and a per-run PRE_COMMIT_HOME. The clone/teardown deliverable (Slice B's arc will
    edit+commit inside the clone). Reuses floor_conformance's `_run` (LF-safe clone) + git config
    + `_rmtree_guarded` (refuses to delete outside the temp root — "no leftovers" with blast-radius).
    """
    source_repo = Path(source_repo).resolve()
    if not (source_repo / ".git").exists():
        raise SandboxError(f"source is not a git repo: {source_repo}")
    temp_root = Path(tempfile.mkdtemp(prefix=prefix))
    env = {"PRE_COMMIT_HOME": str(temp_root / ".pc-home")}
    try:
        clone = temp_root / "clone"
        r = _fc._run(
            ["git", "-c", "core.autocrlf=false", "clone", "--quiet", str(source_repo), str(clone)],
            temp_root)
        if r.returncode != 0:
            raise SandboxError(f"clone failed: {r.stderr.strip()}")
        _fc._run(["git", "config", "core.autocrlf", "false"], clone, env)
        _fc._run(["git", "config", "user.email", "sandbox@example.com"], clone, env)
        _fc._run(["git", "config", "user.name", "Lived Sandbox"], clone, env)
        _fc._run(["git", "config", "commit.gpgsign", "false"], clone, env)
        yield clone, env
    finally:
        teardown(temp_root)


def teardown(temp_root: Path) -> None:
    """Plain-delete a sandbox temp root — but ONLY when it lives under the system temp dir
    (mkdtemp's home). The trusted parent is the SYSTEM TEMP root, not `temp_root.parent` (which
    would make the guard vacuous — every path is under its own parent), so `teardown(an_important_dir)`
    REFUSES rather than deletes (Codex CRITICAL 2026-07-04; "ask before destructive" + no-leftovers)."""
    root = Path(temp_root).resolve()
    sys_temp = Path(tempfile.gettempdir()).resolve()
    if sys_temp != root and sys_temp not in root.parents:
        raise SandboxError(f"refusing to teardown a path outside the system temp dir: {root}")
    _fc._rmtree_guarded(root, sys_temp)
