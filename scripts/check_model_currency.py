#!/usr/bin/env python
"""check_model_currency.py -- list every pinned model id and flag what the registry cannot vouch for.

R61: the harness checks model currency from served evidence, not from anyone's memory. Before
this script the registry pinned `claude-sonnet-5` in roles that already served `claude-sonnet-5-5`
and nothing noticed when an id went stale or appeared in a file the registry had not heard of.

WHAT IT READS, three sources, and where each comes from:

    registry   `ecosystem/provider-registry.yaml` -- every model key, every role-order `model:`
               pin and the dispatcher pin.
    template   every text file under `templates/`.
    contract   every tracked `LANE-*.md` (the repository's own contracts), plus every path passed
               as `--contracts <path>...`. Live lane contracts sit on the operator's transport,
               outside the repository, so CI cannot read them: they are named by path.

WHAT IT FLAGS, each a `FLAG <kind> <id>` line and each a fact, never a ruling:

    unknown-id        an id pinned in a template or contract that the registry has no row for.
    unverified        a registry row with no `last_verified`. No evidence is not fresh (R59).
    stale             a registry row whose `last_verified` is more than 14 days before today.
    evidence-missing  a registry row naming an in-repo evidence path that does not exist.

A bare alias (`sonnet`, `opus`, `haiku`, `fable`, `opusplan`) is reported as an ALIAS, never as an
unknown id: it names no version, so nothing in the registry could contradict it.

An id is known when the registry has a row for it, or for the row it abbreviates: a dated suffix
(`claude-haiku-4-5` for `claude-haiku-4-5-20251001`) and an effort suffix (`gemini-3.8-flash-high`
for `gemini-3.8-flash`) both resolve. Globs (`gpt-6-*`) and date-shaped tokens
(`grok-2026-10-03`) are not ids.

Exit 0 when nothing is flagged, 1 when something is, 2 on an internal error -- an unreadable
registry or a `--contracts` path that does not exist is an error, never a pass. The script is a
CLI and the input to the `audit.py health` finding (`scripts/audit_checks/model_currency.py`,
WARN tier: it informs and blocks nothing). It is wired into no hook. Read-only, ASCII output.

Library-first: the registry loader and its validating schema are `scripts/provider_registry.py`
and `ecosystem/schema/provider_registry.py` (reused, not re-parsed); the dual-import shape is
`scripts/check_provider_registry.py`'s and the exit-code posture is `check_derived_copies.py`'s.
Date arithmetic is `datetime`, path discovery is `git ls-files` with an `os.walk` fallback for a
tree that is not a repository. A model-id grammar library does not exist for this closed set of
four vendor families, so the five shapes below are the one hand-rolled part.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from scripts import provider_registry as _preg
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import provider_registry as _preg

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: A registry row older than this many days is stale.
MAX_AGE_DAYS = 14

REGISTRY_REL = "ecosystem/provider-registry.yaml"
TEMPLATES_REL = "templates"
TRANSPORT_PREFIX = "transport:"

#: Bare Claude Code aliases: a name with no version in it.
BARE_ALIASES = frozenset({"opus", "sonnet", "haiku", "fable", "opusplan"})

_TEXT_SUFFIXES = frozenset({
    ".md", ".txt", ".yaml", ".yml", ".json", ".tmpl", ".toml", ".ps1", ".sh", ".py", ".js",
    ".html", ".cfg", ".ini", "",
})
_SKIP_DIRS = frozenset({".git", ".claude", ".venv", "node_modules", "__pycache__", ".pytest_cache"})

# A candidate is a vendor-prefixed token; the strict shapes below decide whether it is an id.
_CANDIDATE_RE = re.compile(r"(?<![\w./-])(?:claude|gpt|grok|gemini)-[\w.*-]+")
_ID_SHAPES = (
    re.compile(r"^claude-(?:opus|sonnet|haiku|fable)-\d+(?:[.-]\d+)*(?:-[a-z][a-z0-9]*)*$"),
    re.compile(r"^gpt-\d+(?:\.\d+)*(?:-[a-z][a-z0-9]*)*$"),
    re.compile(r"^grok-\d{1,2}(?:\.\d+)?(?:-[a-z0-9]+)*$"),
    re.compile(r"^gemini-\d+(?:\.\d+)*(?:-[a-z][a-z0-9]*)*$"),
)
_EFFORT_SUFFIX_RE = re.compile(r"-(?:minimal|low|medium|high|xhigh|max)$")
_DATE_SUFFIX_RE = re.compile(r"^\d{8}$")

_ALIAS_ALT = "|".join(sorted(BARE_ALIASES))
_ALIAS_RES = (
    re.compile(rf"--model[ =]+[\"']?({_ALIAS_ALT})\b"),
    re.compile(rf"^\s*model:\s*[\"']?({_ALIAS_ALT})\b", re.IGNORECASE),
    re.compile(rf"^\s*\|\s*({_ALIAS_ALT})\s*\|", re.IGNORECASE),
)


@dataclass(frozen=True)
class Pin:
    """One place a model id (or bare alias) is pinned."""

    model_id: str
    kind: str       # "id" | "alias"
    source: str     # "registry" | "template" | "contract"
    where: str      # "<path>:<line>" (the registry's `where` carries the key it came from)


@dataclass(frozen=True)
class Flag:
    kind: str       # "unknown-id" | "unverified" | "stale" | "evidence-missing"
    model_id: str
    detail: str


@dataclass
class Report:
    pins: list[Pin] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)
    today: datetime.date | None = None


class CurrencyError(RuntimeError):
    """The scan could not run: an unreadable registry or a contract path that is not there."""


# --- id extraction ------------------------------------------------------------------------

def _id_candidates(line: str):
    for match in _CANDIDATE_RE.finditer(line):
        token = match.group(0)
        end = match.end()
        if "*" in token or line[end:end + 1] == "*":
            continue                                    # a glob such as `gpt-6-*`
        token = token.rstrip(".-")
        if any(shape.match(token) for shape in _ID_SHAPES):
            yield token


def scan_text(text: str, where: str, source: str) -> list[Pin]:
    """Every model id and bare alias pinned in `text`, each with `where:<line>`."""
    pins: list[Pin] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for token in _id_candidates(line):
            pins.append(Pin(token, "id", source, f"{where}:{number}"))
        for alias_re in _ALIAS_RES:
            match = alias_re.search(line)
            if match:
                pins.append(Pin(match.group(1).lower(), "alias", source, f"{where}:{number}"))
                break
    return pins


# --- the three sources --------------------------------------------------------------------

def _model_pins_of_registry(data: dict) -> list[Pin]:
    pins = [Pin(mid, "id", "registry", f"{REGISTRY_REL}:models.{mid}") for mid in data["models"]]
    for role, spec in (data.get("roles") or {}).items():
        for entry in spec.get("order") or []:
            if entry.get("model"):
                pins.append(Pin(str(entry["model"]), "id", "registry",
                                f"{REGISTRY_REL}:roles.{role}"))
    dispatcher = data.get("dispatcher") or {}
    if dispatcher.get("model"):
        pins.append(Pin(str(dispatcher["model"]), "id", "registry", f"{REGISTRY_REL}:dispatcher"))
    return pins


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _walk(base: Path):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in _SKIP_DIRS)
        for name in sorted(filenames):
            yield Path(dirpath) / name


def template_pins(root: Path) -> list[Pin]:
    base = root / TEMPLATES_REL
    pins: list[Pin] = []
    if not base.is_dir():
        return pins
    for path in _walk(base):
        if path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        text = _read(path)
        if text is not None:
            pins.extend(scan_text(text, path.relative_to(root).as_posix(), "template"))
    return pins


def _tracked_contract_paths(root: Path) -> list[Path]:
    """Tracked `LANE-*.md` files: `git ls-files` when `root` is a repository, else a walk.

    The walk skips dot-directories on purpose -- a hub checkout carries one full copy of itself
    per live lane under `.claude/worktrees/`, and counting those would multiply every pin."""
    try:
        done = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--", "LANE-*.md", "**/LANE-*.md"],
            capture_output=True, check=False, timeout=60)
        if done.returncode == 0 and (root / ".git").exists():
            names = [n for n in done.stdout.decode("utf-8", "replace").split("\0") if n]
            return sorted(root / n for n in names)
    except (OSError, subprocess.SubprocessError):
        pass
    return [p for p in _walk(root) if _is_lane_contract(p.name)]


def _is_lane_contract(name: str) -> bool:
    return name.startswith("LANE-") and name.endswith(".md")


def tracked_contract_pins(root: Path) -> list[Pin]:
    pins: list[Pin] = []
    for path in _tracked_contract_paths(root):
        text = _read(path)
        if text is not None:
            pins.extend(scan_text(text, path.relative_to(root).as_posix(), "contract"))
    return pins


def contract_pins(paths) -> list[Pin]:
    """Live contracts, named by path. A path that is not a readable file is an error."""
    pins: list[Pin] = []
    for raw in paths:
        path = Path(raw)
        text = _read(path) if path.is_file() else None
        if text is None:
            raise CurrencyError(f"live contract not readable: {path}")
        pins.extend(scan_text(text, path.name, "contract"))
    return pins


# --- the verdicts -------------------------------------------------------------------------

def _as_date(value) -> datetime.date | None:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        return None


def is_known(model_id: str, registered: set[str]) -> bool:
    """A registry row exists for `model_id`, or for the row it abbreviates."""
    candidates = {model_id, _EFFORT_SUFFIX_RE.sub("", model_id)}
    for candidate in candidates:
        if candidate in registered:
            return True
        for key in registered:
            if key.startswith(candidate + "-") and _DATE_SUFFIX_RE.match(key[len(candidate) + 1:]):
                return True
    return False


def _evidence_flags(root: Path, model_id: str, evidence) -> list[Flag]:
    flags: list[Flag] = []
    for ref in evidence or []:
        ref = str(ref)
        if ref.startswith(TRANSPORT_PREFIX):
            continue            # CI cannot read the transport; presence there is the operator's
        if not (root / ref).is_file():
            flags.append(Flag("evidence-missing", model_id, f"evidence `{ref}` is not a file"))
    return flags


def analyse(root: Path, contracts=(), today: datetime.date | None = None,
            max_age_days: int = MAX_AGE_DAYS) -> Report:
    """Scan the registry, the templates, the tracked contracts and `contracts` (live, by path)."""
    root = Path(root)
    today = today or datetime.date.today()
    try:
        data = _preg.load_registry(root / REGISTRY_REL)
    except _preg.RegistryError as exc:
        raise CurrencyError(str(exc)) from exc

    report = Report(today=today)
    report.pins.extend(_model_pins_of_registry(data))
    report.pins.extend(template_pins(root))
    report.pins.extend(tracked_contract_pins(root))
    report.pins.extend(contract_pins(contracts))

    registered = set(data["models"])
    seen_unknown: set[str] = set()
    for pin in report.pins:
        if pin.kind != "id" or pin.source == "registry" or pin.model_id in seen_unknown:
            continue
        if not is_known(pin.model_id, registered):
            seen_unknown.add(pin.model_id)
            report.flags.append(Flag("unknown-id", pin.model_id, f"pinned at {pin.where}"))

    for model_id, row in data["models"].items():
        verified = _as_date(row.get("last_verified"))
        if verified is None:
            report.flags.append(Flag("unverified", model_id, "no last_verified"))
        else:
            age = (today - verified).days
            if age > max_age_days:
                report.flags.append(Flag(
                    "stale", model_id,
                    f"last_verified {verified.isoformat()} is {age} days old (limit {max_age_days})"))
        report.flags.extend(_evidence_flags(root, model_id, row.get("evidence")))
    return report


# --- output -------------------------------------------------------------------------------

def render(report: Report) -> str:
    ids = sorted({p.model_id for p in report.pins if p.kind == "id"})
    aliases = sorted({p.model_id for p in report.pins if p.kind == "alias"})
    sources = {s: sum(1 for p in report.pins if p.source == s)
               for s in ("registry", "template", "contract")}
    lines = [
        f"model-currency: {len(ids)} ids and {len(aliases)} aliases pinned "
        f"(registry {sources['registry']}, template {sources['template']}, "
        f"contract {sources['contract']}) as of {report.today.isoformat()}",
        "ids:",
    ]
    for model_id in ids:
        places = [p for p in report.pins if p.model_id == model_id and p.kind == "id"]
        by_source: dict[str, list[str]] = {}
        for pin in places:
            by_source.setdefault(pin.source, []).append(pin.where)
        shown = "; ".join(f"{src} {wheres[0]}" + (f" (+{len(wheres) - 1})" if len(wheres) > 1 else "")
                          for src, wheres in sorted(by_source.items()))
        lines.append(f"  {model_id}  {shown}")
    if aliases:
        lines.append("aliases (a bare alias names no version):")
        for alias in aliases:
            first = next(p for p in report.pins if p.model_id == alias and p.kind == "alias")
            lines.append(f"  ALIAS {alias}  {first.source} {first.where}")
    if report.flags:
        lines.append(f"flags: {len(report.flags)}")
        for flag in report.flags:
            lines.append(f"FLAG {flag.kind} {flag.model_id}  {flag.detail}")
    else:
        lines.append("flags: none")
    return "\n".join(lines).encode("ascii", "replace").decode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_model_currency.py",
        description="List every pinned model id and flag unknown ids and unverified or stale "
                    "registry rows.")
    parser.add_argument("--root", type=Path, default=_REPO_ROOT,
                        help="repository root (default: this repository)")
    parser.add_argument("--contracts", nargs="*", default=[], metavar="PATH",
                        help="live lane contracts, by path (they live outside the repository)")
    parser.add_argument("--today", type=datetime.date.fromisoformat, default=None,
                        help="the date to measure age against (default: today)")
    parser.add_argument("--max-age-days", type=int, default=MAX_AGE_DAYS)
    args = parser.parse_args(argv)
    try:
        report = analyse(args.root, args.contracts, args.today, args.max_age_days)
    except CurrencyError as exc:
        print(f"model-currency: ERROR {exc}".encode("ascii", "replace").decode("ascii"),
              file=sys.stderr)
        return 2
    print(render(report))
    return 1 if report.flags else 0


if __name__ == "__main__":
    sys.exit(main())
