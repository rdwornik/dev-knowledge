#!/usr/bin/env python
"""substrate_provenance.py — L1: POSITIVE proof that this substrate is the provisioned one ([#554]).

THE DEFECT THIS CLOSES WAS NEVER A DEAD CALL. It was that a BROKEN CONTAINER REPORTED HEALTHY.
On 2026-09-14 23:37Z `postCreateCommand` failed, Codespaces silently substituted a bare recovery
container, and the platform said Available throughout ([#746]). The gates in that container were
VACUOUS, not absent — and that is the dangerous shape, because an absent gate announces itself
and a vacuous one does not. Fixing the call closes one cause; the next cause kills the same
silent way. So what is built here is the layer, not the patch.

POSITIVE, NOT AN ABSENCE OF ERROR. "No error was raised" is not evidence. The build WRITES a
marker and a lane's step 0 VERIFIES it: present, parseable, and in AGREEMENT with the live
environment. A marker that merely exists but disagrees with `uv --version` is a REFUSAL, not a
warning. A recovery container CANNOT produce the marker, which is what turns the lie from
unlikely into impossible.

--------------------------------------------------------------------------------------------
THE DISCRIMINATOR, and why the marker is not one well-known file
--------------------------------------------------------------------------------------------
MEASURED 2026-09-15 by a sibling lane, and folded in here as evidence rather than a footnote: a
read-only lane running concurrently with seven others wrote a marker to a FIXED path
(`/tmp/substrate-provenance.json`), re-read it later, and got ANOTHER LANE'S VALUES. Its own
words: *"the path is shared across all concurrently-running lanes, so a marker read from that
fixed path is not proof of the reading lane's own substrate — it can be another lane's."*

That defeats L1's whole property WITHOUT anybody attacking it. The failure mode being built
against is "a substrate that is not ours passes as ours", and a shared-path marker is exactly
that, arriving by collision rather than by malice. Verifying that a marker reads back proves
only that SOMETHING wrote it.

So a substrate is DEFINED here as the pairing of a host and the checkout it serves, and
`substrate_id` is a digest over:

  * `CODESPACE_NAME` when the platform supplies it — unique per codespace, issued by GitHub and
    not by us, so it is the strongest discriminator available in the substrate we actually run
    lanes in;
  * the host name;
  * a machine token (`/etc/machine-id`, else the boot id) where the OS exposes one;
  * the REAL PATH OF THE CHECKOUT.

The checkout is in the digest because that is what separates seven concurrent lane worktrees on
one workstation into seven substrates — the discrimination the fixed `/tmp` path did not have.
The marker then lives at a path DERIVED from that id, so two lanes cannot collide at the
filesystem level at all, and the id is ALSO written INSIDE the marker and re-checked on read, so
a marker that is copied, inherited from an image, or dropped there by a neighbour is refused on
content even when it lands at the right path.

WHERE IT LIVES, and this is a ruling rather than a default. A world-writable tmp path is the
wrong home for an identity claim, so `provenance_dir` refuses the system temp root and its
immediate children outright (a `mkdtemp()` directory deeper inside temp is process-private by
construction, which is why a test harness's own tree is not caught). The default is the user
state directory — `$XDG_STATE_HOME`, `%LOCALAPPDATA%`, or `$HOME/.local/state` — and
`DEV_KNOWLEDGE_PROVENANCE_DIR` relocates it for a host that needs to.

HONEST LIMIT, stated because claiming more of it would be the vacuous-gate failure this module
exists to refuse. The lane runs as the SAME OS user that provisioning ran as, so the marker is
not beyond that user's reach: this is not proof against a deliberate forger. The threat model
here is SILENT BREAKAGE, not malice — a recovery container, a resumed image, a neighbour's
overwrite — and against that the marker is dispositive. The stronger shape (root-owned, written
at image-build time, `sudo`-only) is not taken because it is unavailable on the LOCAL substrate
this same verifier has to run on, and one verifier that works everywhere beats two that disagree.

--------------------------------------------------------------------------------------------
THE STALENESS RULE — decided and recorded, not left to the reader
--------------------------------------------------------------------------------------------
A container built against an older commit is the NORMAL state of a correct container:
`provision.sh::refresh_source_tree` fast-forwards the checkout AFTER provisioning, by design. So

  * marker head == live head                  -> ok
  * marker head is an ANCESTOR of live head   -> ok, with a WARNING naming the drift
  * marker head does not resolve here, or is
    not an ancestor (a diverged history)      -> REFUSED

Refusing the ancestor case would refuse every healthy container, and a gate that refuses
everything is the same non-signal as one that refuses nothing — it gets bypassed, and then the
next real refusal is bypassed with it.

TOOLS: PRESENCE IS REFUSAL-GRADE, VERSION EQUALITY IS NOT — with one exception. `uv` is pinned
EXACTLY by ADR-106, so a version mismatch there is a refusal. `claude` auto-updates inside the
container by design (`devcontainer.json` says so in as many words), so refusing on its version
would refuse a healthy container. Every other tracked tool: present/absent decides, version
drift warns. `node` is tracked because the ABSENCE OF NODE — not authentication — is what
blocked copilot and codex in the container, a misdiagnosis this marker makes unrepeatable.

EXIT CODES. 0 clean · 1 a real violation (looked, and found drift) · 2 could not look (bad
provenance dir, unreadable pins, internal error). The 1/2 split is the repo's
declared-absence-over-false-resolves rule (STANDING_RULINGS F4).

Layer-2 / read-only (ADR-28/36): reads the repo and the machine, writes exactly ONE file, and
that file is outside the working tree by construction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("substrate-provenance")

SCHEMA = "dev-knowledge-substrate-provenance/1"

#: The tool list a lane needs, and the whole of it — a marker that tracked more would refuse on
#: tools no lane depends on, and one that tracked fewer would let the measured `node` gap back in.
TRACKED_TOOLS: tuple[str, ...] = ("git", "uv", "node", "claude", "pre-commit")

#: The ONE tool whose VERSION is refusal-grade. `pyproject.toml` pins it with `==` (ADR-106) and
#: a uv bump is its own gated change, so a container running another one is half-provisioned by
#: the repo's own definition. Everything else floats deliberately; see the module header.
EXACT_VERSION_TOOLS: frozenset[str] = frozenset({"uv"})

_ENV_DIR = "DEV_KNOWLEDGE_PROVENANCE_DIR"
_VERSION_RE = re.compile(r"(\d+\.\d+(?:\.\d+)*)")

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


class ProvenanceError(RuntimeError):
    """Could not LOOK — never "looked and found drift". Maps to exit 2, never exit 1."""


# --- the live-environment adapter -------------------------------------------------------------

class LiveProbe:
    """Everything this module learns about the machine it is on, behind ONE seam.

    A single adapter rather than scattered `subprocess` calls, so a test drives the module
    through the same surface the module actually reads — the recorded failure being a
    monkeypatch of a name the adapter never consulted.
    """

    _TIMEOUT = 20

    def _run(self, argv: list[str]) -> str | None:
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=self._TIMEOUT)
        except (OSError, subprocess.SubprocessError):
            return None
        if proc.returncode != 0:
            return None
        return (proc.stdout or proc.stderr or "").strip()

    def tool_version(self, exe: str) -> str | None:
        """The tool's version, or None when the tool is not on PATH / does not answer.

        None means ABSENT for verification purposes. A tool that is present but whose
        `--version` cannot be parsed is reported as the literal `"present"` rather than as
        absent: "we could not read its version" and "it is not there" are different facts, and
        collapsing them would manufacture a refusal out of an unparseable banner.
        """
        if shutil.which(exe) is None:
            return None
        out = self._run([exe, "--version"])
        if out is None:
            return "present"
        match = _VERSION_RE.search(out)
        return match.group(1) if match else "present"

    def python_version(self) -> str:
        return platform.python_version()

    def host_name(self) -> str:
        return platform.node() or ""

    def machine_token(self) -> str:
        """A per-machine (or per-boot) token where the OS exposes one; `""` where it does not.

        Absence is not an error: the host name and the checkout path already discriminate, and
        a token that is empty on every Windows host would otherwise make the whole digest look
        conditional on a Linux-only file.
        """
        for candidate in ("/etc/machine-id", "/proc/sys/kernel/random/boot_id"):
            try:
                return Path(candidate).read_text(encoding="utf-8").strip()
            except OSError:
                continue
        return ""

    def head(self, repo_root: Path) -> str | None:
        return self._run(["git", "-C", str(repo_root), "rev-parse", "HEAD"])

    def is_ancestor(self, repo_root: Path, older: str, newer: str) -> bool | None:
        """True / False, or None when the question CANNOT BE ANSWERED here.

        None is the third answer on purpose: a commit this clone has never fetched is not a
        diverged commit, and reporting it as one would refuse a container for being new.
        """
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", older, newer],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=self._TIMEOUT)
        except (OSError, subprocess.SubprocessError):
            return None
        if proc.returncode == 0:
            return True
        if proc.returncode == 1:
            return False
        return None      # 128: not a valid object in this repo


# --- where the marker lives -------------------------------------------------------------------

def provenance_dir(env: dict | None = None) -> Path:
    """The marker's home. Raises `ProvenanceError` rather than guessing.

    THE TWO REFUSALS ARE BOTH MEASURED CLASSES, not hypotheticals:

      * an UNEXPANDED `${...}` — `devcontainer.json` handed `provision.sh` the literal string
        `${containerEnv:HOME}/...` and a `mkdir -p` then created a junk directory named
        `${containerEnv:HOME}` inside the working tree on every container start
        (`docs/audits/2026-08-19-technical-554-proof.md` §2.1). `provision.sh` closed the class
        for its stamp; closing it once more here is cheaper than a second host rediscovering it.
      * the SYSTEM TEMP ROOT or an immediate child of it — the sibling lane's measured
        collision. A well-known path under a world-writable root is not a home for an identity
        claim. A directory DEEPER inside temp is not caught, because `mkdtemp()` names are
        process-private and unguessable, which is the property the shared path lacked.
    """
    env = os.environ if env is None else env
    explicit = (env.get(_ENV_DIR) or "").strip()
    if explicit:
        resolved = Path(explicit)
    else:
        base = None
        for key, suffix in ((("XDG_STATE_HOME"), ()), ("LOCALAPPDATA", ()),
                            ("HOME", (".local", "state")),
                            ("USERPROFILE", ("AppData", "Local"))):
            value = (env.get(key) or "").strip()
            if value:
                base = Path(value).joinpath(*suffix)
                break
        if base is None:
            raise ProvenanceError(
                "no state directory could be resolved — set "
                f"{_ENV_DIR}, or export HOME / LOCALAPPDATA")
        resolved = base / "dev-knowledge" / "provenance"

    if "${" in str(resolved) or "%" in resolved.name:
        raise ProvenanceError(
            f"{_ENV_DIR} is {resolved} — an UNEXPANDED variable path. Creating it would put a "
            "junk directory where an identity claim is supposed to live. Unset the variable or "
            "export a literal path.")

    temp_root = Path(tempfile.gettempdir()).resolve()
    try:
        candidate = resolved.resolve()
    except OSError:                                  # pragma: no cover - unreadable parent
        candidate = resolved
    if candidate == temp_root or candidate.parent == temp_root:
        raise ProvenanceError(
            f"refusing {resolved}: the system temp root is world-writable and its immediate "
            "children are well-known paths. A neighbour overwriting an identity claim by "
            "accident is the exact defect this marker exists to make impossible (measured "
            "2026-09-15). Point %s at a user-private directory." % _ENV_DIR)
    return resolved


def substrate_tokens(repo_root: Path, env: dict | None = None,
                     probe: LiveProbe | None = None) -> list[str]:
    """The ordered facts the identity digests. Exposed so a refusal can NAME what differed."""
    env = os.environ if env is None else env
    probe = LiveProbe() if probe is None else probe
    try:
        checkout = str(Path(repo_root).resolve())
    except OSError:                                  # pragma: no cover
        checkout = str(repo_root)
    return [
        f"codespace={(env.get('CODESPACE_NAME') or '').strip()}",
        f"host={probe.host_name()}",
        f"machine={probe.machine_token()}",
        f"checkout={os.path.normcase(checkout)}",
    ]


def substrate_id(repo_root: Path, env: dict | None = None,
                 probe: LiveProbe | None = None) -> str:
    """A stable 16-hex identity for THIS host + THIS checkout. See the module header."""
    joined = "\0".join(substrate_tokens(repo_root, env=env, probe=probe))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


def marker_path(repo_root: Path, env: dict | None = None,
                probe: LiveProbe | None = None) -> Path:
    """DERIVED from the identity, never fixed — two substrates cannot collide on one file."""
    sid = substrate_id(repo_root, env=env, probe=probe)
    return provenance_dir(env) / f"substrate-{sid}.json"


def substrate_kind(env: dict | None = None) -> str:
    """`codespace` / `container` / `host` — and the platform, not our provisioning, decides.

    THIS IS WHAT MAKES A RECOVERY CONTAINER REFUSABLE. `CODESPACES` and `CODESPACE_NAME` are
    injected by GitHub into every codespace including a recovery one, so the substrate itself
    asserts "I am a managed container" while carrying no proof it was ever provisioned. That
    pairing — managed, unmarked — is the refusal. On an unmanaged host the marker is optional,
    because the operator's workstation is not a provisioned container and must not read as one:
    a verifier that refused every LOCAL lane's step 0 would be turned off within the day.
    """
    env = os.environ if env is None else env
    if (env.get("CODESPACES") or env.get("CODESPACE_NAME") or "").strip():
        return "codespace"
    if (env.get("REMOTE_CONTAINERS") or env.get("DEVCONTAINER") or "").strip():
        return "container"
    for marker in ("/.dockerenv", "/run/.containerenv"):
        if Path(marker).exists():
            return "container"
    return "host"


MANAGED_KINDS = frozenset({"codespace", "container"})


# --- the repo's own pins ------------------------------------------------------------------------

def read_pins(repo_root: Path) -> dict[str, str]:
    """`{uv_pin, python_pin}` from their single sources. Raises `ProvenanceError` on absence.

    Read here rather than restated: `pyproject.toml [tool.uv] required-version` and
    `.python-version` are the homes, and a pin typed into this module would be a second answer
    to a settled question. The `[tool.uv]` section scoping is not decoration — `[tool.ruff]`
    carries a `required-version` too, and a naive scan reads the ruff floor as the uv pin.
    """
    repo_root = Path(repo_root)
    pyproject = repo_root / "pyproject.toml"
    try:
        text = pyproject.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProvenanceError(f"cannot read {pyproject}: {exc}") from exc

    section = None
    spec = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            section = stripped
        elif section == "[tool.uv]" and stripped.startswith("required-version"):
            match = re.search(r'"([^"]*)"', stripped)
            if match:
                spec = match.group(1)
                break
    if not spec:
        raise ProvenanceError(
            "pyproject.toml [tool.uv] required-version not found — the uv pin has no single "
            "source to verify against")
    if not spec.startswith("=="):
        raise ProvenanceError(
            f"pyproject.toml pins uv as {spec!r}, which is a range and not a pin (ADR-106)")

    try:
        python_pin = (repo_root / ".python-version").read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ProvenanceError(f"cannot read .python-version: {exc}") from exc
    if not python_pin:
        raise ProvenanceError(".python-version is empty — no interpreter to verify against")
    return {"uv_pin": spec[2:], "python_pin": python_pin}


# --- write ---------------------------------------------------------------------------------------

def collect(repo_root: Path, env: dict | None = None, probe: LiveProbe | None = None,
            writer: str = "unknown") -> dict:
    """The facts, measured LIVE. Nothing here is copied from a declaration."""
    env = os.environ if env is None else env
    probe = LiveProbe() if probe is None else probe
    pins = read_pins(repo_root)
    return {
        "schema": SCHEMA,
        "substrate_id": substrate_id(repo_root, env=env, probe=probe),
        "substrate_kind": substrate_kind(env),
        "repo_root": str(Path(repo_root).resolve()),
        "head": probe.head(Path(repo_root)),
        "python_version": probe.python_version(),
        "python_pin": pins["python_pin"],
        "uv_pin": pins["uv_pin"],
        "tools": {tool: probe.tool_version(tool) for tool in TRACKED_TOOLS},
        "written_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "writer": writer,
    }


def write_marker(repo_root: Path, env: dict | None = None, probe: LiveProbe | None = None,
                 writer: str = "unknown") -> Path:
    """Write the marker for THIS substrate and return its path. The only write this module does."""
    path = marker_path(repo_root, env=env, probe=probe)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = collect(repo_root, env=env, probe=probe, writer=writer)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


# --- verify ---------------------------------------------------------------------------------------

@dataclass
class Verdict:
    """`status` is the decision; the rest is the evidence a refusal has to name.

    status:
      * `ok`            — marker present, parseable, and in agreement with the live environment.
      * `absent-ok`     — no marker, on an UNMANAGED host, and none was required. Not a pass
                          about the marker: a statement that this substrate makes no claim.
      * `refused`       — looked, and found drift. Exit 1.
      * `undetermined`  — could not look at all. Exit 2, never 1.
    """

    status: str
    refusals: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    marker_path: Path | None = None
    marker: dict | None = None
    substrate_kind: str = "host"

    @property
    def exit_code(self) -> int:
        return {"ok": 0, "absent-ok": 0, "refused": 1}.get(self.status, 2)


def verify(repo_root: Path, *, env: dict | None = None, probe: LiveProbe | None = None,
           require_marker: bool = False) -> Verdict:
    """Is this substrate the one provisioning built? Never raises.

    The order below is deliberate: IDENTITY is checked before content, because a marker that
    belongs to another substrate is not stale evidence about this one — it is evidence about a
    different machine, and reading its toolchain fields at all would be reading a neighbour's
    answers off their paper.
    """
    env = os.environ if env is None else env
    probe = LiveProbe() if probe is None else probe
    repo_root = Path(repo_root)
    kind = substrate_kind(env)

    try:
        pins = read_pins(repo_root)
        path = marker_path(repo_root, env=env, probe=probe)
        sid = substrate_id(repo_root, env=env, probe=probe)
    except ProvenanceError as exc:
        return Verdict("undetermined", [str(exc)], [], None, None, kind)

    required = require_marker or kind in MANAGED_KINDS
    if not path.exists():
        if not required:
            return Verdict("absent-ok", [], [
                f"no provenance marker at {path}; this substrate reports kind {kind!r} and "
                "none is required here"], path, None, kind)
        return Verdict("refused", [
            f"no provenance marker at {path} — substrate kind {kind!r} requires one. A "
            "container that was never provisioned, or a recovery container the platform "
            "substituted, cannot produce this file. Re-provision: "
            "bash .devcontainer/provision.sh"], [], path, None, kind)

    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(marker, dict):
            raise ValueError("marker is not an object")
    except (OSError, ValueError) as exc:
        return Verdict("refused", [
            f"provenance marker at {path} is unparseable ({exc.__class__.__name__}: {exc}). An "
            "unreadable identity claim is a refusal, never a skip."], [], path, None, kind)

    refusals: list[str] = []
    warnings: list[str] = []

    if marker.get("schema") != SCHEMA:
        return Verdict("refused", [
            f"provenance marker schema is {marker.get('schema')!r}, expected {SCHEMA!r} — "
            "re-provision rather than interpreting a shape this code does not define."],
            [], path, marker, kind)

    # --- identity, first and on its own ---
    claimed = marker.get("substrate_id")
    if claimed != sid:
        return Verdict("refused", [
            f"provenance marker at {path} carries substrate identity {claimed!r}, but this "
            f"substrate is {sid!r}. The marker is NOT this substrate's — a neighbour's marker, "
            "an image-inherited one, or a copy. A well-formed marker is not proof; being OURS "
            f"is. Tokens: {substrate_tokens(repo_root, env=env, probe=probe)}"],
            [], path, marker, kind)

    # --- the repo's pins have not moved under the container ---
    if marker.get("uv_pin") != pins["uv_pin"]:
        refusals.append(
            f"marker was written against uv pin {marker.get('uv_pin')} but the repo now pins "
            f"{pins['uv_pin']} — the pin moved; re-provision")
    if marker.get("python_pin") != pins["python_pin"]:
        refusals.append(
            f"marker was written against interpreter {marker.get('python_pin')} but "
            f".python-version now says {pins['python_pin']} — re-provision")

    # --- the marker says what WAS true; these say what IS true ---
    live_python = probe.python_version()
    if marker.get("python_version") != live_python:
        refusals.append(
            f"marker records Python {marker.get('python_version')}, live interpreter is "
            f"{live_python}")

    live_uv = probe.tool_version("uv")
    if live_uv is not None and live_uv != "present" and live_uv != pins["uv_pin"]:
        refusals.append(
            f"live uv is {live_uv}, the repo pins {pins['uv_pin']} exactly (ADR-106)")

    recorded_tools = marker.get("tools") or {}
    for tool in TRACKED_TOOLS:
        was = recorded_tools.get(tool)
        now = probe.tool_version(tool)
        if was is not None and now is None:
            refusals.append(
                f"{tool} was present at provisioning ({was}) and is ABSENT now — this substrate "
                "has lost a tool a lane needs")
        elif was is None and now is not None:
            warnings.append(f"{tool} is present ({now}) but was absent at provisioning")
        elif was != now and was is not None:
            if tool in EXACT_VERSION_TOOLS:
                refusals.append(f"{tool} was {was} at provisioning and is {now} now — "
                                "this tool is pinned exactly, so the drift is a refusal")
            else:
                warnings.append(f"{tool} drifted {was} -> {now} (floats by design)")

    # --- the staleness rule (see the module header) ---
    marked_head = marker.get("head")
    live_head = probe.head(repo_root)
    if marked_head and live_head and marked_head != live_head:
        ancestry = probe.is_ancestor(repo_root, marked_head, live_head)
        if ancestry is True:
            warnings.append(
                f"marker head {marked_head[:12]} is BEHIND the live tree {live_head[:12]} — an "
                "ancestor, which is the normal state after refresh_source_tree fast-forwards")
        elif ancestry is False:
            refusals.append(
                f"marker head {marked_head[:12]} is NOT an ancestor of the live head "
                f"{live_head[:12]} — the histories diverge, so the marker describes a tree this "
                "is not")
        else:
            refusals.append(
                f"marker head {marked_head[:12]} does not resolve in this repository — the "
                "marker cites a commit this clone has never had, so it is not evidence about "
                "this checkout")

    status = "refused" if refusals else "ok"
    return Verdict(status, refusals, warnings, path, marker, kind)


# --- CLI -------------------------------------------------------------------------------------------

def _render(verdict: Verdict) -> None:
    for line in verdict.refusals:
        logger.error("REFUSED: %s", line)
    for line in verdict.warnings:
        logger.info("warn: %s", line)
    if verdict.status == "ok":
        marker = verdict.marker or {}
        logger.info("ok — substrate %s (%s), uv %s, python %s, head %s",
                    marker.get("substrate_id"), verdict.substrate_kind,
                    (marker.get("tools") or {}).get("uv"), marker.get("python_version"),
                    (marker.get("head") or "?")[:12])
    elif verdict.status == "absent-ok":
        logger.info("no marker required on substrate kind %r", verdict.substrate_kind)


def main(argv: list[str] | None = None, *, env: dict | None = None,
         probe: LiveProbe | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="substrate_provenance.py",
        description="L1 — write or verify this substrate's provenance marker ([#554])")
    parser.add_argument("command", choices=("write", "verify", "path", "show"))
    parser.add_argument("--repo-root", default=str(_REPO_ROOT))
    parser.add_argument("--writer", default="unknown",
                        help="what produced the marker (provision.sh, a heartbeat run, ...)")
    parser.add_argument("--require-marker", action="store_true",
                        help="refuse an absent marker even on an unmanaged host — what the "
                             "pre-dispatch leg uses, because the CALLER decides there")
    args = parser.parse_args(argv)
    root = Path(args.repo_root)

    try:
        if args.command == "path":
            print(marker_path(root, env=env, probe=probe))
            return 0
        if args.command == "write":
            path = write_marker(root, env=env, probe=probe, writer=args.writer)
            logger.info("provenance marker written: %s", path)
            return 0
        if args.command == "show":
            path = marker_path(root, env=env, probe=probe)
            if not path.exists():
                logger.error("no marker at %s", path)
                return 2
            print(path.read_text(encoding="utf-8"), end="")
            return 0
    except ProvenanceError as exc:
        logger.error("REFUSED (could not look): %s", exc)
        return 2
    except OSError as exc:
        logger.error("REFUSED (could not look): %s", exc)
        return 2

    verdict = verify(root, env=env, probe=probe, require_marker=args.require_marker)
    _render(verdict)
    return verdict.exit_code


if __name__ == "__main__":       # pragma: no cover - exercised by provision.sh and the gate
    sys.exit(main())
