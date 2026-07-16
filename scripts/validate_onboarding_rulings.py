#!/usr/bin/env python
"""validate_onboarding_rulings.py -- read-only advisory checker for the satellite
onboarding-profile rulings register (``ecosystem/satellite-onboarding-rulings.yaml``).

POSTURE (v1): informational/advisory, NON-BLOCKING -- the same posture as the [#337]
fleet_parity ship-gate surfacing. It is NOT an ``audit.py`` ``ALL_CHECKS`` member and
is wired into no blocking gate (a future ALL_CHECKS promotion would be its own one-line
arc). Read-only (Layer-2, ADR-28/36): it parses + schema-checks the register and prints
ONE ASCII surface line; it writes nothing.

Exit contract (never-silently-green -- the fleet_parity pattern):
  * 0  -- register well-formed (surface line printed).
  * 1  -- register parses but has SCHEMA DEFECT(S); each is printed (advisory-loud, so a
          malformed ruling can never render as a green "all good"). Non-blocking: nothing
          wires this exit into a gate.
  * 2  -- register unreadable / structurally unusable (no digest of rulings is possible);
          a broken contract must never look green.

Schema (per ruling entry): ``profile`` in {full, floor-only} + ``ruled_by`` + ``ruled_date``
(YYYY-MM-DD) + ``census_ref``; an ``override`` block (REQUIRED when the ruling overrides
the census proposal) must name BOTH sides -- ``proposed`` + ``ruled`` + a reason.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import click
import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
DEFAULT_REGISTER = _REPO_ROOT / "ecosystem" / "satellite-onboarding-rulings.yaml"

_PROFILES = frozenset({"full", "floor-only"})
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class RegisterUnusable(Exception):
    """The register itself is unreadable/shapeless -- exit-2 class (never silent-green)."""


def load_register(path: Path) -> dict:
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, UnicodeDecodeError, ValueError) as exc:
        raise RegisterUnusable(f"register unreadable ({path}): {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("rulings"), dict):
        raise RegisterUnusable(f"register missing a rulings: map ({path})")
    return data


def schema_defects(data: dict) -> list[str]:
    """Return a list of human-readable schema defects (empty == well-formed)."""
    defects: list[str] = []
    rulings = data["rulings"]
    if not rulings:
        return ["rulings: map is empty -- no ruling recorded (expected >= 1)"]
    for repo, entry in sorted(rulings.items()):
        if not isinstance(entry, dict):
            defects.append(f"{repo}: entry is not a mapping")
            continue
        profile = entry.get("profile")
        if profile not in _PROFILES:
            defects.append(f"{repo}: profile {profile!r} not in {sorted(_PROFILES)}")
        if not entry.get("ruled_by"):
            defects.append(f"{repo}: missing ruled_by")
        rd = entry.get("ruled_date")
        if not (isinstance(rd, str) and _DATE_RE.match(rd)):
            defects.append(f"{repo}: ruled_date {rd!r} is not YYYY-MM-DD")
        if not entry.get("census_ref"):
            defects.append(f"{repo}: missing census_ref")
        ov = entry.get("override")
        if ov is not None:
            if not isinstance(ov, dict):
                defects.append(f"{repo}: override is not a mapping")
            else:
                # An override must name BOTH sides (proposed vs ruled) + a reason.
                for field in ("proposed", "ruled", "ruled_reason"):
                    if not ov.get(field):
                        defects.append(f"{repo}: override missing {field}")
                if ov.get("proposed") == ov.get("ruled"):
                    defects.append(f"{repo}: override proposed == ruled (not an override)")
    return defects


def surface_line(data: dict) -> str:
    rulings = data["rulings"]
    full = sum(1 for e in rulings.values()
               if isinstance(e, dict) and e.get("profile") == "full")
    floor = sum(1 for e in rulings.values()
                if isinstance(e, dict) and e.get("profile") == "floor-only")
    overrides = sorted(r for r, e in rulings.items()
                       if isinstance(e, dict) and e.get("override"))
    ov = f"; overrides: {', '.join(overrides)}" if overrides else ""
    return (f"[onboarding-rulings] {len(rulings)} satellite(s) ruled: "
            f"{full} full, {floor} floor-only{ov} "
            f"-- ecosystem/satellite-onboarding-rulings.yaml")


@click.command()
@click.option("--path", "path", default=str(DEFAULT_REGISTER), show_default=False,
              help="Rulings register path (tests may override).")
def main(path: str) -> None:
    """Advisory read-only validation of the satellite onboarding-profile rulings."""
    try:
        data = load_register(Path(path))
    except RegisterUnusable as exc:
        click.echo(f"onboarding-rulings: UNUSABLE -- {exc}", err=True)
        sys.exit(2)
    defects = schema_defects(data)
    if defects:
        click.echo("onboarding-rulings: SCHEMA DEFECT(S) (advisory -- not a gate):")
        for d in defects:
            click.echo(f"  - {d}")
        sys.exit(1)
    click.echo(surface_line(data))
    sys.exit(0)


if __name__ == "__main__":
    main()
