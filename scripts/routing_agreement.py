#!/usr/bin/env python
"""routing_agreement.py — does the L0 routing copy still agree with the in-repo table?

`[#613]`, under register ruling **Z-G3 amendment A2**: the AUTHORITATIVE role -> CLI routing
table is in-repo (`ecosystem/routing-table.yaml`); `~/.claude/ROUTING.md` at **L0** may hold a
DERIVED copy; and an agreement check asserts the two match. The shape is `[#592]`'s dispatch
drift organ — a logic module plus a thin registered adapter — reused rather than reinvented.

WHY AGREEMENT AND NOT CORRECTNESS. This organ reports that two copies say the same thing. It
does **not** rule on whether the routing itself is right: routing doctrine's canonical table is
L0, outside this repository (ARCHITECTURE Ch3, ruled 2026-08-22). Detection, not adjudication —
the same honest bound `check_provider_registry` states about its own seams.

ABSENCE IS A REPORTED GAP, NOT A PASS — register ruling **Z-G4**, which this organ is a direct
consumer of: *"A check that cannot compute its ground truth FAILs, never skips. A `skipped`
status is a reported gap, never a pass, and no aggregate surface may count it as one."*

The trap Z-G4 names is live here and is worth stating concretely: L0 sits on the operator's
disk, so the L0 file is missing on exactly the hosts where routing drift is least visible — CI,
a container, a cloud lane. A `skipif(L0 missing)` would make this organ absent precisely where
it is needed, and `unavailable` is worse still: `audit.py`'s `_check_outcome` projects that
onto `pass` and `cmd_ship_gate` blocks only on `fail` plus undispositioned `warn`, so an
`unavailable` verdict SHIPS GREEN having measured nothing. This module therefore reports
**warn** when L0 is absent — a named report that blocks ship-gate unless dispositioned — and
**fail** when L0 is present and DIVERGES.

Layer-2 contract (ADR-28/36): read-only. It reads two files and compares strings. It writes
nothing, and it does not write L0 — keeping the derived copy current is the operator's act.

HONEST LIMITS, because they bound a green verdict:
  * agreement is asserted on the ROLE -> CLI mapping, not on prose. L0 is a human-facing
    markdown doc; the in-repo table is machine-read YAML. Comparing them byte-for-byte would
    be a formatting gate, so the comparison is on extracted role rows.
  * a role L0 does not mention at all is a MISS, reported as divergence. Silence is not
    agreement — that is the whole failure mode this organ exists for.
  * a green here says the two copies agree on this host, at this moment. It says nothing about
    a third copy elsewhere, and this organ does not enforce that no third copy exists.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover - declared dependency
    raise SystemExit(f"routing_agreement: pyyaml is required: {exc!r}")

TABLE_RELPATH = "ecosystem/routing-table.yaml"
#: The L0 derived copy. Read from the table itself so the two cannot disagree about where it is.
DEFAULT_L0 = "~/.claude/ROUTING.md"


class RoutingAgreementError(RuntimeError):
    """The corpus could not be read. FAIL-LOUD: callers report, they do not swallow."""


@dataclass(frozen=True)
class Divergence:
    role: str
    expected: str
    detail: str


def load_table(repo_path: Path) -> tuple[dict[str, list[str]], str]:
    """`{role: [cli, ...]}` from the in-repo table, plus the declared L0 path."""
    p = Path(repo_path) / TABLE_RELPATH
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise RoutingAgreementError(f"cannot read {TABLE_RELPATH}: {exc!r}") from exc
    if not isinstance(raw, dict) or not isinstance(raw.get("roles"), dict):
        raise RoutingAgreementError(f"{TABLE_RELPATH} carries no `roles:` mapping")

    roles: dict[str, list[str]] = {}
    for name, row in raw["roles"].items():
        if not isinstance(row, dict) or "cli" not in row:
            raise RoutingAgreementError(f"role {name!r} declares no `cli`")
        cli = row["cli"]
        roles[str(name)] = [str(c) for c in (cli if isinstance(cli, list) else [cli])]
    return roles, str(raw.get("l0_derived_copy") or DEFAULT_L0)


def l0_path(declared: str) -> Path:
    return Path(os.path.expanduser(declared))


#: How far past a role mention a CLI still counts as bound to THAT role. A table row and its
#: values live on one line; a prose paragraph may wrap. Bounded deliberately -- see `compare`.
_REGION_LINES = 3


def _role_regions(role: str, lines: list[str], all_roles: "list[str]") -> list[str]:
    """The text region(s) of `l0_text` that describe `role`, lower-cased.

    A region starts at a line naming the role and ends at whichever comes first: the next line
    naming a DIFFERENT role, or `_REGION_LINES` lines later. That bound is the whole point --
    see `compare`.
    """
    needle = re.compile(role.replace("_", "[ _-]?"), re.I)
    others = [re.compile(r.replace("_", "[ _-]?"), re.I)
              for r in all_roles if r != role]
    regions: list[str] = []
    for i, line in enumerate(lines):
        if not needle.search(line):
            continue
        region = [line]
        for nxt in lines[i + 1:i + 1 + _REGION_LINES]:
            if any(o.search(nxt) for o in others):
                break
            region.append(nxt)
        regions.append("\n".join(region).lower())
    return regions


def compare(roles: dict[str, list[str]], l0_text: str) -> list[Divergence]:
    """Roles whose CLIs the L0 copy does not corroborate, matched WITHIN the role's region.

    Deliberately lenient about FORM and strict about BINDING. L0 is prose, so the check does
    not demand a syntax -- but it does demand that a CLI appear *beside the role it is bound
    to*, not merely somewhere in the document.

    WHY THE REGION BOUND EXISTS (terra HIGH, 2026-08-28). An earlier version searched the
    whole document for each CLI independently. That produces FALSE AGREEMENT, which is the
    one outcome this organ may not produce: an L0 copy reading `reviewer: claude-code` passes
    if the token `codex` appears anywhere else in the file -- under an unrelated role, in a
    footnote, in a changelog line. The check would then certify agreement about exactly the
    binding it got wrong.

    A role L0 omits entirely is still a divergence, because silence is the failure mode rather
    than the absence of one.

    CR TOLERANCE IS MEASURED, NOT ADDED. `str.splitlines` treats a CR-LF pair as ONE boundary and
    leaves no carriage return on the line, and `scan` reads L0 in text mode, where universal
    newlines have already translated. A line-ending flip on the derived copy therefore cannot
    masquerade as a routing divergence, and no stripping step is needed to make that true --
    which is why none was added. The property is witnessed by
    `tests/test_routing_agreement.py::test_a_crlf_l0_copy_agrees_exactly_as_the_lf_one_does`
    rather than asserted here.
    """
    out: list[Divergence] = []
    lines = l0_text.splitlines()
    names = sorted(roles)
    for role in names:
        clis = roles[role]
        regions = _role_regions(role, lines, names)
        if not regions:
            out.append(Divergence(role, ", ".join(clis),
                                  "the L0 copy does not mention this role at all"))
            continue
        missing = [c for c in clis
                   if not any(c.lower() in region for region in regions)]
        if missing:
            out.append(Divergence(
                role, ", ".join(clis),
                f"the L0 copy mentions the role but not {', '.join(missing)} beside it"))
    return out


#: The markers L0 carries the RENDERED table between. A region write replaces what sits between
#: them and touches nothing else, because the derived copy is a human-facing doc whose prose is
#: the operator's -- only the table is derived.
REGION_BEGIN = "<!-- routing-table:begin -->"
REGION_END = "<!-- routing-table:end -->"


def render_table(roles: dict[str, list[str]]) -> str:
    """The L0 region: a marker-delimited markdown table, one ROLE and all its CLIs per LINE.

    ONE LINE PER ROLE IS THE LOAD-BEARING PROPERTY, not a formatting taste. `compare` binds a
    CLI to a role only inside that role's region, and `_role_regions` ends a region at the next
    line naming a DIFFERENT role. A table row therefore renders as a region of exactly one line
    carrying every CLI the role is bound to -- the shape `_REGION_LINES = 3` was written to
    admit, and the reason a rendered table closes the gate that hand-written prose did not.

    RENDERING DOES NOT WRITE L0. This module reads two files and compares them (ADR-28/36, and
    the Layer-2 contract in the module docstring); `--render` emits to stdout so that stays
    true, and placing the region is the operator's act.
    """
    rows = "\n".join(f"| {role} | {', '.join(roles[role])} |" for role in sorted(roles))
    return (f"{REGION_BEGIN}\n"
            f"<!-- GENERATED from {TABLE_RELPATH} by `python scripts/routing_agreement.py\n"
            f"     --render`. Hand edits here are overwritten by the next render. -->\n"
            f"\n"
            f"| Role | CLI |\n"
            f"| --- | --- |\n"
            f"{rows}\n"
            f"\n"
            f"{REGION_END}\n")


def scan(repo_path: Path) -> tuple[str, Optional[list[Divergence]], str]:
    """`(state, divergences, detail)`.

    `state` is one of `agree` / `diverge` / `l0-absent`. `divergences` is None when there was
    nothing to compare against — which the adapter renders as a WARN, never a pass.
    """
    roles, declared = load_table(repo_path)
    target = l0_path(declared)
    if not target.is_file():
        return ("l0-absent", None,
                f"the L0 derived copy {declared} is absent on this host, so agreement could "
                f"not be computed for {len(roles)} role(s) — a reported gap, not a pass "
                f"(Z-G4)")
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise RoutingAgreementError(f"cannot read {declared}: {exc!r}") from exc

    diverged = compare(roles, text)
    if diverged:
        return ("diverge", diverged,
                "; ".join(f"{d.role} (table: {d.expected}) — {d.detail}" for d in diverged))
    return ("agree", [], f"{len(roles)} role(s) in {TABLE_RELPATH} corroborated by {declared}")


def main(argv: Optional[list[str]] = None) -> int:
    """`--render` emits the L0 region; with no flag, report the agreement state.

    Exit code follows the STATE, not the transport: 0 on `agree`, 1 otherwise -- so `l0-absent`
    is non-zero too. Z-G4: a check that cannot compute its ground truth reports a gap, and a gap
    that exited 0 here would read as a pass to anything shelling out to this module.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="routing_agreement",
        description="Report L0/in-repo routing agreement, or render the region L0 carries.")
    parser.add_argument("--render", action="store_true",
                        help="emit the marker-delimited L0 region to stdout and exit")
    parser.add_argument("--repo", default=".", help="repo root (default: the cwd)")
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    if args.render:
        roles, _ = load_table(repo)
        sys.stdout.write(render_table(roles))
        return 0

    state, _, detail = scan(repo)
    print(f"{state}: {detail}")
    return 0 if state == "agree" else 1


if __name__ == "__main__":
    raise SystemExit(main())
