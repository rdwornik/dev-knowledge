#!/usr/bin/env python
"""quota_watch.py -- R7: per-SKU used/quota/%/burn/projected-exhaustion, and the ONE hard veto
(Codespaces core-hours) a launch may hit before everything else just warns.

LANE-5B2-6-quota-watch. Prior art reused, not duplicated: `lane_cost.py` (the ledger/CLI shape,
and the "unpriced/unmeasured is never silently zero" posture, carried here as "an absent
quota is never a free pass") and `billing_leak_sentinel.py` (fail-soft SessionStart posture --
not adopted here, since `check` is a launch-time veto that MUST be able to refuse, but the same
module is where a future SessionStart surfacing of this organ would live).

LIBRARY-FIRST (O-12): stdlib `subprocess` + `json` driving the already-installed `gh` CLI, plus
this repo's existing `click`/`PyYAML` dependencies (`lane_cost.py`, `provider_registry.py`).
No new dependency.

=================================================================================================
WHERE THE NUMBERS COME FROM
=================================================================================================
  Codespaces core-hours  `gh api users/<account>/settings/billing/usage/summary`. Every
                          `codespaces_compute_d<N>` SKU's `grossQuantity` is HOURS; core-hours
                          for that SKU is hours x N, with N read from the SKU NAME itself
                          (`codespaces_core_hours_used`), never a hardcoded per-SKU table --
                          live-verified 2026-09-26: `codespaces_compute_d2` 8.01392 h (x2),
                          `codespaces_compute_d4` 5.91882 h (x4) = 39.703 core-hours used of 180.
  Actions minutes         same summary, SKU `actions_linux`, `grossQuantity` is minutes.
  Codespaces storage      same summary, SKU `codespaces_storage`, `grossQuantity` is
                          gigabyte-HOURS -- normalised to gigabyte-months (see
                          `codespaces_storage_used`).
  Copilot credits         `gh api copilot_internal/user` (the Enterprise login). This endpoint
                          reports ITS OWN included quota alongside usage
                          (`quota_snapshots.premium_interactions.{credits_used,entitlement}`),
                          so it is read LIVE and never declared a second time in
                          `ecosystem/quotas.yaml` (see that file's own header) -- live-verified
                          2026-09-26: entitlement 22,500, credits_used 285.
  Billed dollars          any usage item's `netAmount` > 0 in the billing summary above.

=================================================================================================
THE HARD VETO, AND WHY IT ALONE (R7 Do-not clause)
=================================================================================================
"Veto a launch on a projection alone except the Codespaces core-hour crossing W2 names;
everything else warns." `check` IS that one veto: it refuses (exit 1) only when a prospective
launch's projected core-hours would push CUMULATIVE core-hours past the declared 180-hour
quota. Every other threshold (50/80/100%, first billed dollar) is `record`'s job, and `record`
never exits non-zero for a crossing -- it WARNS, by writing a `QUOTA-WARN-<date>.md` transport
file, which is a report, not a refusal.

=================================================================================================
A CROSSING IS A COMPARISON, NOT A SNAPSHOT
=================================================================================================
"79% then 81%" only means something against a PRIOR reading -- a bare 81% could have been 95%
a minute ago and dropped, or could be this cycle's first read. So `record` appends every read to
`logs/QUOTA-READS.jsonl` (append-only, the `logs/LANE-COSTS.jsonl` class) and compares the new
percentage against the immediately PRIOR row for the same SKU-group and billing cycle -- never
against a fixed baseline, which would re-fire on every later read past a threshold rather than
once at the crossing. `detect_crossings` is the pure predicate this rests on.

=================================================================================================
CALL SURFACE
=================================================================================================
    uv run --locked python scripts/quota_watch.py report
    uv run --locked python scripts/quota_watch.py check --projected-core-hours 16
    uv run --locked python scripts/quota_watch.py record
    uv run --locked python scripts/quota_watch.py line
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import click
import yaml

# The dual package/script import shim (`transport.py`'s own docstring names the same trap):
# `from scripts import transport` (repo root on sys.path) and `import transport` (scripts/ on
# sys.path) are both live entry points here.
_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import transport as _transport
except ImportError:  # pragma: no cover
    import transport as _transport

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("quota-watch")

QUOTAS_REGISTRY_RELPATH = "ecosystem/quotas.yaml"
READS_LEDGER_RELPATH = "logs/QUOTA-READS.jsonl"
DEFAULT_ACCOUNT = "rdwornik"
DEFAULT_COPILOT_ACCOUNT = "Robert-Dwornik_ghub"

#: `transport.write`'s `writer` identity for this organ -- the module's own basename, the same
#: convention every row in `ecosystem/transport-registry.yaml` already uses (`handback`,
#: `gen_ledger`, ...).
WRITER_NAME = "quota_watch"

#: `codespaces_compute_d2` -> 2, `codespaces_compute_d4` -> 4, `..._d8` -> 8, ... -- the core
#: count lives in the SKU name itself, so a machine size this account has not used yet still
#: prices correctly the first time it appears.
_D_CORES_RE = re.compile(r"codespaces_compute_d(\d+)$")

#: `codespaces_storage`'s grossQuantity is gigabyte-HOURS; the declared quota is gigabyte-MONTHS.
#: 730 = 365*24/12, the average hours in a month -- a client-side approximation stated as one,
#: not a bill reconciliation (the same honest-limits posture `lane_cost.py` documents).
_HOURS_PER_MONTH = 730.0


class QuotaWatchError(RuntimeError):
    """The registry, a billing/copilot read, or a ledger row could not be used."""


# ============================================================================ the declared quota

@dataclass(frozen=True)
class SkuQuota:
    group: str
    quota: float
    unit: str
    thresholds: tuple[float, ...]
    account: str
    notes: str = ""


def load_quotas(path: Optional[Path] = None) -> dict[str, SkuQuota]:
    """Every declared SKU-group row. A row with no `quota:` (Copilot -- see
    `ecosystem/quotas.yaml`'s own header) is SKIPPED here, never defaulted to zero: an absent
    quota means "read live", and zero would make every read of it read as already-exhausted.
    """
    p = Path(path) if path is not None else (_REPO_ROOT / QUOTAS_REGISTRY_RELPATH)
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except OSError as exc:
        raise QuotaWatchError(f"could not read {p}: {exc}") from exc
    skus = (raw or {}).get("skus")
    if not isinstance(skus, dict) or not skus:
        raise QuotaWatchError(f"{p} has no non-empty top-level 'skus' mapping")
    default_account = str((raw or {}).get("account", DEFAULT_ACCOUNT))
    out: dict[str, SkuQuota] = {}
    for name, row in skus.items():
        if not isinstance(row, dict) or row.get("quota") is None:
            continue
        out[name] = SkuQuota(
            group=name, quota=float(row["quota"]), unit=str(row.get("unit", "")),
            thresholds=tuple(float(t) for t in row.get("thresholds", (0.5, 0.8, 1.0))),
            account=str(row.get("account", default_account)),
            notes=str(row.get("notes", "")))
    return out


# ============================================================================ the billing read

@dataclass(frozen=True)
class UsageItem:
    product: str
    sku: str
    gross_quantity: float
    net_amount: float
    unit_type: str


def parse_billing_summary(data: dict) -> tuple[list[UsageItem], date]:
    """`usageItems` plus the cycle's start date, from `timePeriod`. A summary with no
    `timePeriod` cannot be dated, so it is a hard `QuotaWatchError` rather than a guessed
    cycle -- burn-per-day and projected-exhaustion are both meaningless without it."""
    tp = data.get("timePeriod")
    if not isinstance(tp, dict) or "year" not in tp or "month" not in tp:
        raise QuotaWatchError("billing summary carries no usable 'timePeriod'")
    items = [UsageItem(product=str(i.get("product", "")), sku=str(i.get("sku", "")),
                       gross_quantity=float(i.get("grossQuantity", 0.0)),
                       net_amount=float(i.get("netAmount", 0.0)),
                       unit_type=str(i.get("unitType", "")))
             for i in data.get("usageItems", []) or []]
    cycle_start = date(int(tp["year"]), int(tp["month"]), 1)
    return items, cycle_start


def codespaces_core_hours_used(items: list[UsageItem]) -> float:
    total = 0.0
    for item in items:
        m = _D_CORES_RE.match(item.sku)
        if m:
            total += item.gross_quantity * int(m.group(1))
    return total


def actions_minutes_used(items: list[UsageItem]) -> float:
    return sum(i.gross_quantity for i in items if i.sku == "actions_linux")


def codespaces_storage_used(items: list[UsageItem]) -> float:
    return sum(i.gross_quantity for i in items if i.sku == "codespaces_storage") / _HOURS_PER_MONTH


#: `{sku-group name in ecosystem/quotas.yaml: reader(items) -> used}`. The single place that
#: connects a declared quota row to the billing-summary column it is measured against.
_USED_READERS = {
    "codespaces_core_hours": codespaces_core_hours_used,
    "codespaces_storage": codespaces_storage_used,
    "actions_minutes": actions_minutes_used,
}


def first_billed_dollar(items: list[UsageItem]) -> Optional[UsageItem]:
    """The first usage item actually billed (`netAmount > 0`), or None. R7's "first billed
    dollar" trigger fires on ANY such item, independent of every percentage threshold."""
    for item in items:
        if item.net_amount > 0:
            return item
    return None


def parse_copilot_credits(data: dict) -> tuple[float, float]:
    """`(credits_used, entitlement)` from `quota_snapshots.premium_interactions` -- the one
    quota snapshot on an Enterprise seat that carries `unlimited: false` and a real entitlement
    (`chat`/`completions` report `unlimited: true` with a meaningless zeroed entitlement)."""
    snap = ((data.get("quota_snapshots") or {}).get("premium_interactions") or {})
    if not snap or snap.get("unlimited"):
        raise QuotaWatchError(
            "copilot_internal/user carries no bounded premium_interactions quota snapshot")
    return float(snap.get("credits_used", 0.0)), float(snap.get("entitlement", 0.0))


# ================================================================================ status + burn

@dataclass(frozen=True)
class SkuStatus:
    group: str
    used: float
    quota: float
    unit: str
    pct: float
    burn_per_day: Optional[float]
    projected_exhaustion: Optional[date]

    def render(self) -> str:
        burn = f"{self.burn_per_day:.3f}/day" if self.burn_per_day is not None else "no burn yet"
        exhaustion = (self.projected_exhaustion.isoformat() if self.projected_exhaustion
                     else "not projected to exhaust this cycle")
        return (f"{self.group}: {self.used:,.2f}/{self.quota:,.2f} {self.unit} "
                f"({self.pct:.1%}), burn {burn}, exhaustion {exhaustion}")


def sku_status(group: str, quota: SkuQuota, used: float, cycle_start: date,
              now: Optional[date] = None) -> SkuStatus:
    """Burn is USED SO FAR divided by days elapsed in the cycle (at least 1, so day one of a
    cycle does not divide by zero) -- a straight-line average, not a trend fit. Exhaustion
    projects forward from `now` at that average rate; a quota already exceeded projects
    exhaustion as `now` itself rather than a nonsensical date in the past."""
    now = now or datetime.now(timezone.utc).date()
    days_elapsed = max((now - cycle_start).days, 1)
    burn = (used / days_elapsed) if used > 0 else None
    pct = (used / quota.quota) if quota.quota else 0.0
    remaining = quota.quota - used
    if remaining <= 0:
        exhaustion: Optional[date] = now
    elif burn:
        exhaustion = now + timedelta(days=remaining / burn)
    else:
        exhaustion = None
    return SkuStatus(group=group, used=used, quota=quota.quota, unit=quota.unit, pct=pct,
                     burn_per_day=burn, projected_exhaustion=exhaustion)


# ============================================================================ crossing detection

def detect_crossings(previous_pct: Optional[float], current_pct: float,
                     thresholds: tuple[float, ...]) -> list[float]:
    """Every threshold that lies in `(previous_pct, current_pct]` -- crossed BETWEEN the two
    reads. A threshold already passed before `previous_pct` never re-fires (it is not in the
    open interval), and one still ahead of `current_pct` has not fired yet. `previous_pct is
    None` (no prior read this cycle) crosses every threshold at or below `current_pct` -- a
    first read landing at 85% has, in effect, already crossed 50% and 80%.
    """
    lower = previous_pct if previous_pct is not None else float("-inf")
    return sorted(t for t in thresholds if lower < t <= current_pct)


def detect_billed_dollar_crossing(was_billed: bool, is_billed: bool) -> bool:
    return is_billed and not was_billed


# ==================================================================================== the ledger

@dataclass(frozen=True)
class QuotaRead:
    group: str
    cycle: str  # cycle_start.isoformat() -- the ledger's dedup key together with `group`
    used: float
    quota: float
    pct: float
    billed: bool
    measured: str

    def to_dict(self) -> dict:
        return {"group": self.group, "cycle": self.cycle, "used": self.used,
                "quota": self.quota, "pct": self.pct, "billed": self.billed,
                "measured": self.measured}

    @classmethod
    def from_dict(cls, d: dict) -> "QuotaRead":
        return cls(group=str(d["group"]), cycle=str(d["cycle"]), used=float(d["used"]),
                  quota=float(d["quota"]), pct=float(d["pct"]),
                  billed=bool(d.get("billed", False)), measured=str(d.get("measured", "")))


def reads_ledger_path(repo_root: Path) -> Path:
    return Path(repo_root) / READS_LEDGER_RELPATH


def read_ledger(ledger_path: Path) -> list[QuotaRead]:
    path = Path(ledger_path)
    if not path.exists():
        return []
    out: list[QuotaRead] = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            out.append(QuotaRead.from_dict(json.loads(raw)))
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("%s line %d unreadable, skipped: %s", path.name, n, exc)
    return out


def append_read(ledger_path: Path, row: QuotaRead) -> None:
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row.to_dict(), sort_keys=True) + "\n")


def last_read(ledger_path: Path, group: str, cycle: str) -> Optional[QuotaRead]:
    rows = [r for r in read_ledger(ledger_path) if r.group == group and r.cycle == cycle]
    return rows[-1] if rows else None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class CrossingResult:
    group: str
    status: SkuStatus
    crossings: tuple[str, ...]  # e.g. ("80%",) or ("FIRST_BILLED_DOLLAR",)

    @property
    def crossed(self) -> bool:
        return bool(self.crossings)


def record_read(ledger_path: Path, group: str, quota: SkuQuota, used: float,
                cycle_start: date, billed: bool, now: Optional[date] = None) -> CrossingResult:
    """Compute this read's status, compare it against the ledger's PRIOR row for the same
    group+cycle, append the new row, and return whatever crossed. Called once per SKU-group per
    invocation of `record`; the ledger is the only state that persists between invocations."""
    status = sku_status(group, quota, used, cycle_start, now=now)
    cycle = cycle_start.isoformat()
    prev = last_read(ledger_path, group, cycle)
    crossings = [f"{t:.0%}" for t in
                detect_crossings(prev.pct if prev else None, status.pct, quota.thresholds)]
    if detect_billed_dollar_crossing(prev.billed if prev else False, billed):
        crossings.append("FIRST_BILLED_DOLLAR")
    append_read(ledger_path, QuotaRead(group=group, cycle=cycle, used=used, quota=quota.quota,
                                       pct=status.pct, billed=billed, measured=_now_iso()))
    return CrossingResult(group=group, status=status, crossings=tuple(crossings))


# ========================================================================== the one hard veto

@dataclass(frozen=True)
class LaunchVerdict:
    refused: bool
    reason: str


def codespaces_launch_check(used_core_hours: float, projected_core_hours: float,
                            quota: float) -> LaunchVerdict:
    """R7's ONE veto: would `used + projected` push CUMULATIVE Codespaces core-hours past the
    declared quota? Nothing else in this module refuses a launch -- see the module docstring."""
    projected_total = used_core_hours + projected_core_hours
    if projected_total > quota:
        return LaunchVerdict(True, (
            f"REFUSED: {used_core_hours:.2f} used + {projected_core_hours:.2f} projected = "
            f"{projected_total:.2f} core-hours would cross the {quota:.0f}-hour quota "
            f"(R7/W2 -- the one hard veto; every other threshold only warns)"))
    return LaunchVerdict(False, (
        f"OK: {used_core_hours:.2f} used + {projected_core_hours:.2f} projected = "
        f"{projected_total:.2f} of {quota:.0f} core-hours, "
        f"{quota - projected_total:.2f} would remain"))


# ================================================================================== the cost line

def cost_line(codespaces_status: Optional[SkuStatus], actions_status: Optional[SkuStatus],
             copilot_used: Optional[float], copilot_quota: Optional[float],
             cloud_sessions: Optional[int]) -> str:
    """The digest's `[quota]` line (R7/F3): Codespaces core-hours used/remaining, Actions
    minutes, Copilot credits, cloud sessions. Every figure that could not be read says so by
    name (`UNREAD` / `not recorded`) rather than reading as zero."""
    parts = ["[quota]"]
    if codespaces_status:
        parts.append(f"Codespaces {codespaces_status.used:.2f}/{codespaces_status.quota:.0f} "
                     f"core-hours used, "
                     f"{codespaces_status.quota - codespaces_status.used:.2f} remaining")
    else:
        parts.append("Codespaces UNREAD")
    if actions_status:
        parts.append(f"Actions {actions_status.used:.0f}/{actions_status.quota:.0f} min used")
    else:
        parts.append("Actions UNREAD")
    if copilot_used is not None and copilot_quota:
        parts.append(f"Copilot {copilot_used:.0f}/{copilot_quota:.0f} credits used "
                     f"({copilot_used / copilot_quota:.1%})")
    else:
        parts.append("Copilot UNREAD")
    parts.append(f"cloud sessions: {cloud_sessions}" if cloud_sessions is not None
                else "cloud sessions: not recorded (pass --cloud-sessions)")
    return " / ".join(parts)


# ======================================================================================== gh api

def _gh_api(path: str, account: str) -> dict:
    """`gh api <path>`, pinned to `account` via a fetched token in the CHILD env only (never
    printed -- R2). Binary-safe decode per the Windows git-subprocess gotcha: no `text=True`,
    explicit UTF-8, strict on stdout (this is data that gets parsed as JSON and must not
    silently absorb a bad byte), lenient on stderr (human error text only)."""
    token_proc = subprocess.run(["gh", "auth", "token", "-u", account], capture_output=True)
    if token_proc.returncode != 0:
        raise QuotaWatchError(
            f"gh auth token -u {account} failed: "
            f"{token_proc.stderr.decode('utf-8', 'replace').strip()}")
    token = token_proc.stdout.decode("utf-8").strip()
    env = dict(os.environ)
    env["GH_TOKEN"] = token
    proc = subprocess.run(["gh", "api", path], capture_output=True, env=env)
    if proc.returncode != 0:
        raise QuotaWatchError(
            f"gh api {path} (account {account}) failed: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    return json.loads(proc.stdout.decode("utf-8"))


def _billing_data(billing_json: Optional[str], account: str) -> dict:
    if billing_json:
        return json.loads(Path(billing_json).read_text(encoding="utf-8"))
    return _gh_api(f"users/{account}/settings/billing/usage/summary", account)


def _copilot_data(copilot_json: Optional[str], account: str) -> dict:
    if copilot_json:
        return json.loads(Path(copilot_json).read_text(encoding="utf-8"))
    return _gh_api("copilot_internal/user", account)


def _resolve_transport_root(explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    root = os.environ.get("CLAUDE_PROMPTS_DIR")
    if not root:
        raise QuotaWatchError("CLAUDE_PROMPTS_DIR is not set; no transport to write to")
    return Path(root)


def render_quota_warn(crossed: list[CrossingResult], billed_item: Optional[UsageItem],
                      on: Optional[date] = None) -> str:
    day = (on or datetime.now(timezone.utc).date()).isoformat()
    lines = ["carried-by: OPEN", "kind: QUOTA-WARN", f"date: {day}", "",
            f"# QUOTA-WARN -- {day}", ""]
    for r in crossed:
        lines.append(f"- {r.group}: {', '.join(r.crossings)} -- {r.status.render()}")
    if billed_item is not None and any("FIRST_BILLED_DOLLAR" in r.crossings for r in crossed):
        lines.append(f"- first billed dollar: {billed_item.sku} "
                     f"netAmount={billed_item.net_amount}")
    return "\n".join(lines) + "\n"


# ============================================================================================ CLI

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """R7 quota watch: per-SKU used/quota/%/burn/projection; one hard veto (Codespaces
    core-hours); everything else warns via a QUOTA-WARN transport file."""


_registry_option = click.option("--registry", type=click.Path(path_type=Path), default=None,
                                help="ecosystem/quotas.yaml path override.")
_billing_json_option = click.option("--billing-json", type=click.Path(exists=True), default=None,
                                    help="A saved billing-summary JSON, instead of a live gh call.")
_copilot_json_option = click.option("--copilot-json", type=click.Path(exists=True), default=None,
                                    help="A saved copilot_internal/user JSON, instead of a live "
                                         "gh call.")
_account_option = click.option("--account", default=DEFAULT_ACCOUNT, show_default=True)
_copilot_account_option = click.option("--copilot-account", default=DEFAULT_COPILOT_ACCOUNT,
                                       show_default=True)


@cli.command("report")
@_registry_option
@_billing_json_option
@_copilot_json_option
@_account_option
@_copilot_account_option
def cmd_report(registry: Optional[Path], billing_json: Optional[str],
              copilot_json: Optional[str], account: str, copilot_account: str) -> None:
    """Per-SKU used/quota/%/burn/projected-exhaustion, plus billed-dollar and Copilot state.
    Read-only -- writes nothing, records nothing to the ledger."""
    quotas = load_quotas(registry)
    data = _billing_data(billing_json, account)
    items, cycle_start = parse_billing_summary(data)
    for group, reader in _USED_READERS.items():
        if group not in quotas:
            continue
        click.echo(sku_status(group, quotas[group], reader(items), cycle_start).render())
    billed = first_billed_dollar(items)
    click.echo(f"billed: {billed.sku} netAmount={billed.net_amount}" if billed
              else "billed: none this cycle")
    try:
        used_c, ent_c = parse_copilot_credits(_copilot_data(copilot_json, copilot_account))
        click.echo(f"copilot: {used_c:.0f}/{ent_c:.0f} credits used "
                  f"({(used_c / ent_c) if ent_c else 0.0:.1%})")
    except QuotaWatchError as exc:
        click.echo(f"copilot: UNREAD ({exc})")


@cli.command("check")
@click.option("--projected-core-hours", type=float, required=True)
@_registry_option
@_billing_json_option
@_account_option
def cmd_check(projected_core_hours: float, registry: Optional[Path],
             billing_json: Optional[str], account: str) -> None:
    """THE ONE HARD VETO. Exit 1 (REFUSED) when `used + projected` would cross the declared
    Codespaces core-hour quota; exit 0 (OK) otherwise. Called before every codespace launch."""
    quotas = load_quotas(registry)
    if "codespaces_core_hours" not in quotas:
        raise click.ClickException(f"{QUOTAS_REGISTRY_RELPATH} has no codespaces_core_hours row")
    items, _ = parse_billing_summary(_billing_data(billing_json, account))
    verdict = codespaces_launch_check(codespaces_core_hours_used(items), projected_core_hours,
                                      quotas["codespaces_core_hours"].quota)
    click.echo(verdict.reason)
    sys.exit(1 if verdict.refused else 0)


@cli.command("record")
@click.option("--sku-group", "sku_groups", multiple=True, default=(),
             help="Repeat to limit to specific groups; default is every declared group.")
@_registry_option
@_billing_json_option
@_account_option
@click.option("--repo-root", type=click.Path(path_type=Path), default=_REPO_ROOT,
             show_default=True)
@click.option("--transport-root", default=None,
             help="Override CLAUDE_PROMPTS_DIR for the QUOTA-WARN write.")
@click.option("--no-write", is_flag=True,
             help="Detect and print crossings; append to the ledger; never write QUOTA-WARN.")
def cmd_record(sku_groups: tuple[str, ...], registry: Optional[Path],
              billing_json: Optional[str], account: str, repo_root: Path,
              transport_root: Optional[str], no_write: bool) -> None:
    """Read once, compare against the ledger's prior read per SKU-group, append, and WARN (a
    QUOTA-WARN transport file) on any 50/80/100% crossing or the first billed dollar. Never
    refuses -- see `check` for the one command that can."""
    quotas = load_quotas(registry)
    items, cycle_start = parse_billing_summary(_billing_data(billing_json, account))
    billed_item = first_billed_dollar(items)
    groups = sku_groups or tuple(_USED_READERS)
    ledger_path = reads_ledger_path(Path(repo_root))
    results: list[CrossingResult] = []
    for group in groups:
        if group not in quotas or group not in _USED_READERS:
            continue
        used = _USED_READERS[group](items)
        result = record_read(ledger_path, group, quotas[group], used, cycle_start,
                             billed=bool(billed_item))
        results.append(result)
        click.echo(f"{result.status.render()} -- crossings: {', '.join(result.crossings) or 'none'}")
    crossed = [r for r in results if r.crossed]
    if crossed and not no_write:
        root = _resolve_transport_root(transport_root)
        dest = root / "to-browser" / f"QUOTA-WARN-{datetime.now(timezone.utc).date().isoformat()}.md"
        _transport.write(WRITER_NAME, dest, render_quota_warn(crossed, billed_item))
        click.echo(f"QUOTA-WARN written: {dest}")


@cli.command("line")
@_registry_option
@_billing_json_option
@_copilot_json_option
@_account_option
@_copilot_account_option
@click.option("--cloud-sessions", type=int, default=None,
             help="Cloud-session count for this batch; the caller counts them (e.g. "
                  "`claude agents --json`), this organ has no visibility of its own.")
def cmd_line(registry: Optional[Path], billing_json: Optional[str],
            copilot_json: Optional[str], account: str, copilot_account: str,
            cloud_sessions: Optional[int]) -> None:
    """The digest's one-line `[quota]` cost line (R7/F3)."""
    quotas = load_quotas(registry)
    items, cycle_start = parse_billing_summary(_billing_data(billing_json, account))
    cs_status = (sku_status("codespaces_core_hours", quotas["codespaces_core_hours"],
                            codespaces_core_hours_used(items), cycle_start)
                if "codespaces_core_hours" in quotas else None)
    ac_status = (sku_status("actions_minutes", quotas["actions_minutes"],
                            actions_minutes_used(items), cycle_start)
                if "actions_minutes" in quotas else None)
    copilot_used = copilot_quota = None
    try:
        copilot_used, copilot_quota = parse_copilot_credits(
            _copilot_data(copilot_json, copilot_account))
    except QuotaWatchError:
        pass
    click.echo(cost_line(cs_status, ac_status, copilot_used, copilot_quota, cloud_sessions))


if __name__ == "__main__":
    cli()
