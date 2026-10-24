"""Handoff intake and KPI (H-Q1 / H-Q5 of RATIFICATION-2026-10-24; lane l12-acceptance, [#1640]).

Two hub-local, read-only computations for the handoff cut:

* `build_intake` turns a plan's item list into ONE bounded FINDING: a disposition ledger
  (ASK / OWED / ASSUME), a flush-left `owed:` line of decision ids, and at most seven questions
  (the rest are deferred -- no second round).
* `kpi` computes the handoff KPI from counted inputs; nothing is typed in as a verdict.

Run: `python scripts/handoff_intake.py kpi --escaped-file F --irreducible-file G --rounds N ...`
or, through the cut, `gen_handoff.py --intake --plan FILE`.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date as _date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import transport_lint  # noqa: E402

MAX_QUESTIONS = 7
DEFAULT_SEAT = "handoff-cut"
_BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$")
_ID_TABLE_ROW_RE = re.compile(r"^\|\s*(" + transport_lint._DECISION_ID_RE.pattern + r")\s*\|")


def plan_items(plan_text: str) -> list[str]:
    items = []
    for line in plan_text.splitlines():
        m = _BULLET_RE.match(line)
        if m:
            items.append(m.group(1).strip())
    return items


def _unique(ids: list[str]) -> list[str]:
    seen: list[str] = []
    for i in ids:
        if i not in seen:
            seen.append(i)
    return seen


def build_intake(plan_text: str, *, owed_sources: list[str], seat: str, today: str) -> str:
    items = plan_items(plan_text)
    owed_set = {s.strip() for s in owed_sources}
    rows: list[tuple[int, str, str]] = []
    ids: list[str] = []
    for n, item in enumerate(items, 1):
        found = transport_lint.decision_id_tokens(item)
        if found or item in owed_set:
            disposition = "OWED"
            ids.extend(found)
        elif item.endswith("?"):
            disposition = "ASK"
        else:
            disposition = "ASSUME"
        rows.append((n, item, disposition))
    for src in owed_sources:
        ids.extend(transport_lint.decision_id_tokens(src))
    ids = _unique(ids)
    asks = [item for _, item, d in rows if d == "ASK"]
    out = [
        "kind: FINDING",
        f"date: {today}",
        f"by: {seat}",
        f"owed: {' '.join(ids) if ids else 'none'}",
        "",
        f"# FINDING-{seat}-INTAKE-{today}",
        "",
        "## Disposition ledger",
        "",
        "| n | item | disposition |",
        "|---|---|---|",
    ]
    out += [f"| {n} | {item} | {d} |" for n, item, d in rows]
    out += ["", "## Questions", ""]
    out += [f"- {q}" for q in asks[:MAX_QUESTIONS]] or ["- none"]
    if len(asks) > MAX_QUESTIONS:
        out += ["", "## Deferred (round 2 not allowed)", ""]
        out += [f"- {q}" for q in asks[MAX_QUESTIONS:]]
    return "\n".join(out) + "\n"


def carry_ledger_owed(path: Path) -> list[str]:
    lines = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("owed:") or _ID_TABLE_ROW_RE.match(line):
            lines.append(line)
    return lines


def intake_name(seat: str, today: str) -> str:
    return f"FINDING-{seat}-INTAKE-{today}.md"


def write_intake(transport_root: Path, plan_text: str, *, seat: str = DEFAULT_SEAT,
                 today: str | None = None, owed_sources: list[str] | None = None) -> Path:
    import transport  # noqa: PLC0415  (module attribute, so the registered writer path is the one used)
    today = today or _date.today().isoformat()
    body = build_intake(plan_text, owed_sources=owed_sources or [], seat=seat, today=today)
    dest = Path(transport_root) / "to-browser" / intake_name(seat, today)
    return transport.write("lane", dest, body)


def kpi(*, escaped: list[str], irreducible: list[str], rounds: int,
        hypercare_minutes: float | None, timebox_minutes: float | None) -> dict:
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    if hypercare_minutes is None:
        hypercare = {"duration_minutes": None,
                     "status": "unmeasured — no hypercare duration recorded", "met": None}
    elif timebox_minutes is None:
        hypercare = {"duration_minutes": hypercare_minutes,
                     "status": "unmeasured — no declared timebox", "met": None}
    else:
        hypercare = {"duration_minutes": hypercare_minutes, "timebox_minutes": timebox_minutes,
                     "target": "<= timebox", "met": hypercare_minutes <= timebox_minutes}
    return {
        "escaped_questions": {"count": len(escaped), "items": list(escaped), "target": 0,
                              "met": len(escaped) == 0},
        "irreducible": {"items": list(irreducible), "owner": "operator",
                        "route": "RATIFICATION"},
        "rounds": {"value": rounds, "target": 1, "met": rounds <= 1},
        "hypercare": hypercare,
    }


def kpi_lines(k: dict) -> str:
    out = []
    for section, fields in k.items():
        for key, value in fields.items():
            if isinstance(value, list):
                value = "; ".join(value) if value else "none"
            out.append(f"{section}.{key}: {str(value).replace('|', '/')}")
    return "\n".join(out) + "\n"


def _read_lines(path: str | None) -> list[str]:
    if not path:
        return []
    return [ln.strip() for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="handoff_intake")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("kpi", help="compute the handoff KPI from counted inputs")
    p.add_argument("--escaped-file")
    p.add_argument("--irreducible-file")
    p.add_argument("--rounds", type=int, required=True)
    p.add_argument("--hypercare-minutes", type=int, default=None)
    p.add_argument("--timebox-minutes", type=int, default=None)
    args = parser.parse_args(argv)
    result = kpi(escaped=_read_lines(args.escaped_file),
                 irreducible=_read_lines(args.irreducible_file), rounds=args.rounds,
                 hypercare_minutes=args.hypercare_minutes,
                 timebox_minutes=args.timebox_minutes)
    sys.stdout.write(kpi_lines(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
