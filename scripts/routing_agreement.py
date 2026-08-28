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
