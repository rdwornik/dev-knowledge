#!/usr/bin/env python
"""hook_expiry_verdict.py -- the 2026-09-25 "0 catches in-window -> REMOVE, never tune" verdict
for the `telemetry_emit.py wrap`-instrumented pre-commit / commit-msg hooks (lane-hooks-urgent,
LANE-5A-7, done-contract item 2).

THE DEFECT THIS CLOSES. `.pre-commit-config.yaml` states the rule in prose, thirteen times, next
to each hook it wraps: "Expiry 2026-09-25 -- 0 catches in-window -> REMOVE, never tune." No code
ever computed that verdict. Read naively, "0 catches" and "0 runs" are the same bit -- and they
are not the same finding (DIGEST-HOOK-ARCHITECTURE-2026-09-23-APPENDIX.md A3: four of the thirteen
armed hooks show ZERO ROWS AT ALL in `logs/TELEMETRY.db`, because their `files:` selector rarely
matches in a seven-day window, not because they were exercised and never caught anything). Judging
those four "REMOVE" would delete a gate for having had no opportunity to fire, which is the
opposite of what "0 catches in-window" is supposed to mean.

THE RULE, ENCODED. A hook's `hook_run` history must SPAN at least `JUDGMENT_WINDOW_H` (168h / 7
days -- the same window `bounded_hook.py`'s own bypass-rate judgment uses, `RATE_WINDOW_H`, and
the span from the 2026-09-18 B2-lane4 arming to the 2026-09-25 expiry this contract answers)
before "0 catches" means anything. Shorter than that -- including the degenerate case of zero rows
-- is UNMEASURED, never REMOVE. Only a hook whose EARLIEST recorded run is at least the window old
gets a REMOVE/KEEP verdict from its catch count.

WHAT THIS DOES NOT DO. It does not remove a hook, edit `.pre-commit-config.yaml`, or file a row --
it prints a verdict per hook and exits 0 always (a report, not a gate); acting on a REMOVE verdict
is an operator/architect act, same posture as `bounded_hook.py`'s drafted-not-filed rows. It also
does not invent a judged hook list: `JUDGED_HOOK_IDS` is parsed live from `.pre-commit-config.yaml`
(every `id:` whose `entry:` calls `telemetry_emit.py wrap <id>`), so a hook added to or dropped
from that wrapping pattern is picked up here without a second list to keep in sync.
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import telemetry_emit as _te
except ImportError:
    from scripts import telemetry_emit as _te

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PRECOMMIT_CONFIG = _REPO_ROOT / ".pre-commit-config.yaml"

#: The window a hook's counter history must SPAN before "0 catches" is a finding rather than an
#: absence of opportunity. 168h, matching `bounded_hook.RATE_WINDOW_H` and the 2026-09-18 arming
#: -> 2026-09-25 expiry span this contract answers.
JUDGMENT_WINDOW_H = 168.0

EXPIRY_DATE = "2026-09-25"

VERDICT_REMOVE = "REMOVE"
VERDICT_KEEP = "KEEP"
VERDICT_UNMEASURED = "UNMEASURED"

_WRAP_ID_RE = re.compile(
    r"entry:\s*uv run --locked python scripts/telemetry_emit\.py wrap (\S+) --")


def judged_hook_ids(config_path: Path = _PRECOMMIT_CONFIG) -> tuple[str, ...]:
    """Every hook id whose `.pre-commit-config.yaml` entry routes through `telemetry_emit.py
    wrap <id>` -- the exact set the 2026-09-25 expiry prose is written beside. A regex over the
    `entry:` line rather than a full YAML parse: the shape is one fixed CLI invocation form, and
    matching it directly means a hook added in this shape is judged automatically, with nothing
    here to remember to update.
    """
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError:
        return ()
    return tuple(_WRAP_ID_RE.findall(text))


@dataclass(frozen=True)
class HookVerdict:
    hook_id: str
    runs: int
    blocks: int
    earliest_ts: str | None
    latest_ts: str | None
    history_hours: float
    verdict: str
    reason: str


def _hook_run_rows(db_path: Path, hook_id: str) -> list[tuple[str, str]]:
    """`(ts, outcome)` for every `hook_run` row of `hook_id`, oldest first. Empty on a missing
    store, a missing table, or a locked file -- an unmeasured tree is zero evidence, not a
    crash, and this report must never fail a commit or a boot over a read it cannot make."""
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=5.0)
    except sqlite3.Error:
        return []
    try:
        return list(conn.execute(
            "SELECT ts, outcome FROM events WHERE event_type = 'hook_run' AND name = ? "
            "ORDER BY ts", (hook_id,)))
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def verdict_for(hook_id: str, rows: list[tuple[str, str]], now: datetime,
                window_h: float = JUDGMENT_WINDOW_H) -> HookVerdict:
    """The rule, in code. `rows` oldest-first; `now` is injected (never `datetime.now()` read
    internally) so a test can pin the clock without patching a module global."""
    runs = len(rows)
    blocks = sum(1 for _, outcome in rows if outcome == "block")
    if runs == 0:
        return HookVerdict(
            hook_id, 0, 0, None, None, 0.0, VERDICT_UNMEASURED,
            "0 runs recorded -- a hook that has not been exercised is not evidence it never "
            "catches anything; REMOVE would delete it for having had no opportunity to fire")

    earliest_ts, _ = rows[0]
    latest_ts, _ = rows[-1]
    earliest = datetime.fromisoformat(earliest_ts)
    if earliest.tzinfo is None:
        earliest = earliest.replace(tzinfo=timezone.utc)
    history_hours = (now - earliest).total_seconds() / 3600.0

    if history_hours < window_h:
        return HookVerdict(
            hook_id, runs, blocks, earliest_ts, latest_ts, history_hours, VERDICT_UNMEASURED,
            f"counter history spans {history_hours:.1f}h ({runs} runs), short of the "
            f"{window_h:g}h judgment window -- too young to judge, not measured-and-clean")

    if blocks == 0:
        return HookVerdict(
            hook_id, runs, blocks, earliest_ts, latest_ts, history_hours, VERDICT_REMOVE,
            f"{runs} runs over {history_hours:.1f}h (>= the {window_h:g}h window), 0 blocks -- "
            "a full judgment window with no catch")

    return HookVerdict(
        hook_id, runs, blocks, earliest_ts, latest_ts, history_hours, VERDICT_KEEP,
        f"{blocks} of {runs} runs blocked over {history_hours:.1f}h -- caught something")


def compute_verdicts(db_path: Path | None = None, now: datetime | None = None,
                     hook_ids: tuple[str, ...] | None = None,
                     window_h: float = JUDGMENT_WINDOW_H) -> list[HookVerdict]:
    resolved_db = db_path if db_path is not None else _te.default_db_path()
    resolved_now = now if now is not None else datetime.now(timezone.utc)
    resolved_ids = hook_ids if hook_ids is not None else judged_hook_ids()
    return [verdict_for(hook_id, _hook_run_rows(resolved_db, hook_id), resolved_now, window_h)
            for hook_id in resolved_ids]


def report_lines(verdicts: list[HookVerdict]) -> list[str]:
    lines = [f"[hook-expiry] {EXPIRY_DATE} verdict, judgment window {JUDGMENT_WINDOW_H:g}h "
             f"({len(verdicts)} judged hook(s)):"]
    for v in sorted(verdicts, key=lambda v: (v.verdict != VERDICT_REMOVE, v.hook_id)):
        lines.append(f"[hook-expiry]   {v.hook_id}: {v.verdict} -- {v.reason}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("--db", type=Path, default=None,
                        help="override the telemetry store (default: telemetry_emit.default_db_path())")
    args = parser.parse_args(argv)
    verdicts = compute_verdicts(db_path=args.db)
    sys.stdout.write("\n".join(report_lines(verdicts)) + "\n")
    return 0  # a report, never a gate -- exits 0 regardless of what it finds


if __name__ == "__main__":
    raise SystemExit(main())
