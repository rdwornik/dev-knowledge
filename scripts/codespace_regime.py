#!/usr/bin/env python
"""codespace_regime.py -- the CLOUD regime: a METER, not a ceiling (`[#792]`).

WHY THIS IS A THIRD FILE
=================================================================================================
`scripts/resource_lifecycle.py` owns the LOCAL regime and `scripts/context_reclamation.py` owns
context. This owns the cloud one, and the separation is the frozen contract's hardest rule:

    **DO NOT SHARE THRESHOLDS BETWEEN THEM.** The economics differ in kind -- local is a fixed
    ceiling you allocate against, cloud is a meter you run down. A single number tuned for one
    is wrong for the other, and a mechanism that pretends they are one resource is why neither
    is managed today.

So there is no memory figure here and there can never be one. `tests/test_codespace_regime.py`
asserts all three modules' `THRESHOLD_UNITS` are pairwise disjoint, which is that rule as a
property rather than as a comment.

TOKENS PRICE THE WRONG RESOURCE HERE
=================================================================================================
A container sitting attached and idle burns budget while its token count stays flat, so an idle
lane reads as a cheap one. That is why `write_receipt` REFUSES a receipt with no uptime rather
than writing a blank: the number that means "not measured" must never be the number that means
"free", which is `QR-OBS-002`'s rule applied one resource over.

MEASURED, NOT ASSUMED
=================================================================================================
Every constant below comes from one probe container provisioned and deleted 2026-09-15 --
`lane-aa-14-probe`, 11.97 minutes of metered uptime, the whole cost of the measurement. The
figures and the substrate evidence are in
`docs/audits/2026-09-15-technical-lane-aa-14-resource-lifecycle.md` section 6.

WHAT IS NOT DECIDABLE HERE, AND SAYS SO
=================================================================================================
`prebuild_ruling` returns `decidable=False`. The time side is measured; the money side is not
readable from this account (`gh api user/settings/billing/shared-storage` -> 404), and the
contract's instruction is to answer with measured figures rather than in principle. So it
returns a RECOMMENDATION carrying its flip frequency and names the input it is missing. A
prebuild ruling made without the storage line would be exactly the thing the contract forbids.

CALL SURFACE
=================================================================================================

    uv run --locked python scripts/codespace_regime.py session-start
    uv run --locked python scripts/codespace_regime.py prebuild --creations-per-week 2
    uv run --locked python scripts/codespace_regime.py receipt --slug S --codespace C \\
        --created ISO --deleted ISO --machine basicLinux32gb
"""
from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("codespace-regime")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

#: The cloud receipt ledger. IN the repo and tracked, unlike the local sampler: a cloud lane's
#: minutes are a FLEET fact that an integrator, a batch close and a cost report all read, and
#: the bill it prices is not this box's. Append-only in the ADR-29/39 sense.
#:
#: THE NAME CARRIES NO DATE, AND THAT IS LOAD-BEARING. `logs_retention.py` relocates a file
#: matching `<STEM>-YYYY-MM-DD.<ext>` directly under `logs/` into a month bucket, while the
#: `.gitignore` exemption for those buckets is `.md`-ONLY -- so a dated `.jsonl` here would be
#: moved by a SessionStart hook and DIRTY THE TREE on every fresh session. That trap fired
#: twice in this lane's own session against `logs/PROVIDER-*-2026-09-15.json`, and `[#785]`
#: records the underlying disagreement. This ledger ROUTES AROUND it deliberately rather than
#: resolving it: an undated cumulative name is also the honest shape for an append-only
#: ledger, which is not a dated artifact.
RECEIPT_LEDGER_RELPATH = "logs/CODESPACE-RECEIPTS.jsonl"


# ================================================================== the thresholds, CLOUD regime

#: Longest a container may live before it has outlived somebody's handback.
MAX_CONTAINER_AGE_DAYS = 1.0
#: Cold path: image build + the full 8-leg provisioning run, measured on the prebuild bake.
COLD_CREATION_SECONDS = 155.8
#: Warm path: the same creation off a prebuilt image.
PREBUILT_CREATION_SECONDS = 34.1
#: Creations per week above which the prebuild question is worth re-asking.
PREBUILD_FLIP_CREATIONS_PER_WEEK = 7.0

THRESHOLD_UNITS: dict[str, str] = {
    "MAX_CONTAINER_AGE_DAYS": "days-of-container-life",
    "COLD_CREATION_SECONDS": "seconds-of-container-creation",
    "PREBUILT_CREATION_SECONDS": "seconds-of-container-creation",
    "PREBUILD_FLIP_CREATIONS_PER_WEEK": "container-creations-per-week",
}

THRESHOLD_PROVENANCE: dict[str, str] = {
    "MAX_CONTAINER_AGE_DAYS": (
        "DERIVED from this repo's own batch cadence rather than from a cloud convention. The "
        "measured merge-queue spans are 3.83 h (batch Y) and 4.94 h (batch Z), so a whole "
        "batch fits inside a day with room over; a container alive longer than that was not "
        "torn down at anybody's handback. The measured breach is "
        "`suite-baseline-2026-09-08`, alive 7 days."
    ),
    "COLD_CREATION_SECONDS": (
        "MEASURED 2026-09-15 from the probe's `/workspaces/.codespaces/.persistedshare/"
        "creation.log`, prebuild-bake segment 02:55:46 -> 02:58:22 = 155.8 s, of which "
        "`docker buildx build` is 82.1 s (02:56:02 -> 02:57:24) and the 8-leg "
        "`onCreateCommand` provisioning run is 55.0 s."
    ),
    "PREBUILT_CREATION_SECONDS": (
        "MEASURED 2026-09-15 from the same log, creation segment 12:21:02 -> 12:21:37 = "
        "34.1 s: `postCreateCommand` 25.9 s (the 2 legs that cannot be baked) plus a 1.4 s "
        "`postStartCommand` gate. End to end from the create API call to 'Finished "
        "configuring' was 57.0 s."
    ),
    "PREBUILD_FLIP_CREATIONS_PER_WEEK": (
        "A FLIP CONDITION, not a measurement, and it is labelled as one. At the measured "
        "2.0 creations/week the prebuild saves about 4 minutes a week, which does not "
        "justify continuous paid storage. 7.0/week (one a day) is where the saving crosses "
        "15 minutes a week and the question is worth re-asking AGAINST THE STORAGE LINE -- "
        "which is the input this module cannot read. A recommendation with no flip condition "
        "is an opinion, so the condition is declared even though the number behind it is not "
        "yet takeable."
    ),
}


# ======================================================================== the metered quantity

def uptime_minutes(created: Optional[datetime], deleted: Optional[datetime] = None,
                   now: Optional[datetime] = None) -> float:
    """Minutes of metered container life.

    AN OPEN CONTAINER IS MEASURED AGAINST NOW, never reported as zero. A container still
    running has burned budget, and reporting 0 until it is deleted makes the number that
    means "not measured" identical to the number that means "free" -- the exact error
    `QR-OBS-002` refuses one resource over.
    """
    if created is None:
        raise ValueError("uptime needs a creation timestamp; there is no uptime without one")
    end = deleted if deleted is not None else (now or datetime.now(timezone.utc))
    seconds = (end - created).total_seconds()
    if seconds < 0:
        raise ValueError(
            f"the container was deleted at {end.isoformat()}, BEFORE it was created at "
            f"{created.isoformat()} -- a negative uptime is a clock or an ordering defect, "
            f"never a measurement")
    return seconds / 60.0


# =============================================================================== the receipt

class ReceiptIncomplete(RuntimeError):
    """A cloud receipt that prices the wrong resource is refused rather than written."""


def write_receipt(slug: str, batch: str, codespace: str,
                  created: Optional[datetime], deleted: Optional[datetime],
                  machine: str, prebuild: bool, tokens: Mapping[str, int],
                  ledger_path: Optional[Path] = None,
                  now: Optional[datetime] = None) -> dict:
    """Append one cloud-lane receipt, carrying uptime MINUTES alongside tokens.

    THE REFUSAL IS THE POINT. The frozen contract's clause is that a Codespace lane's receipt
    records uptime minutes alongside tokens, and a receipt that quietly omitted the minutes
    would satisfy every reader that only looks at tokens while pricing the wrong resource.
    So an absent creation timestamp raises instead of writing a blank, and NOTHING is
    appended -- a partial row in an append-only ledger cannot be taken back.
    """
    try:
        minutes = uptime_minutes(created, deleted, now=now)
    except ValueError as exc:
        raise ReceiptIncomplete(
            f"refusing to write a receipt for {slug!r} with no uptime: {exc}. Tokens alone "
            f"price the wrong resource in this regime -- an attached idle container burns "
            f"budget while its token count stays flat") from exc

    row = {
        "kind": "codespace",
        "slug": slug,
        "batch": batch,
        "codespace": codespace,
        "machine": machine,
        "prebuild": bool(prebuild),
        "created": created.isoformat() if created else None,
        "deleted": deleted.isoformat() if deleted else None,
        "open": deleted is None,
        "uptime_minutes": round(minutes, 2),
        "tokens": dict(tokens),
        "recorded": (now or datetime.now(timezone.utc)).isoformat(timespec="seconds"),
    }
    path = Path(ledger_path) if ledger_path else (_REPO_ROOT / RECEIPT_LEDGER_RELPATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def open_receipts(ledger_path: Optional[Path] = None) -> list[dict]:
    """Rows whose container was never recorded as deleted -- our own record of what is live."""
    path = Path(ledger_path) if ledger_path else (_REPO_ROOT / RECEIPT_LEDGER_RELPATH)
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("open"):
            out.append(row)
    return out


# ============================================================================= the idle policy

@dataclass(frozen=True)
class IdleVerdict:
    breach: bool
    reason: str


def idle_verdict(state: str, age_days: float) -> IdleVerdict:
    """Attached while a lane runs; TORN DOWN at handback, never left warm "in case".

    `Shutdown` NEVER SCORES CLEAN, however young. Stopping a codespace stops the compute
    meter and not the storage one -- it bills storage for up to its retention period (30 days
    on this account) -- so a policy that accepted `Shutdown` would read "stop it at handback"
    as compliance while the bill continued. The measured instance is
    `suite-baseline-2026-09-08`, sat Shutdown for 7 days.
    """
    normalised = (state or "").strip().lower()
    if normalised == "shutdown":
        return IdleVerdict(True, (
            f"a Shutdown codespace is not free -- it bills STORAGE for up to its retention "
            f"period, and this one is {age_days:.1f} day(s) old. The policy is torn down at "
            f"handback, not stopped"))
    if age_days > MAX_CONTAINER_AGE_DAYS:
        return IdleVerdict(True, (
            f"alive {age_days:.1f} day(s), past the {MAX_CONTAINER_AGE_DAYS:.1f}-day bound -- "
            f"a whole batch's merge queue fits in under 5 hours, so a container older than "
            f"this outlived somebody's handback"))
    return IdleVerdict(False, f"{state}, {age_days:.2f} day(s) old -- within a batch")


# ========================================================================== the prebuild ruling

@dataclass(frozen=True)
class PrebuildRuling:
    decidable: bool
    saved_seconds_per_creation: float
    saved_minutes_per_week: float
    creations_per_week: float
    missing_input: str
    recommendation: str


def prebuild_ruling(creations_per_week: float) -> PrebuildRuling:
    """Do prebuilds pay for themselves at OUR batch frequency?

    Answered with the measured build time and the measured frequency, as the contract asks,
    and NOT answered on money, which the contract also asks -- so it returns
    `decidable=False` and names the input it lacks rather than substituting a plausible
    number. The time arithmetic is real; the storage cost is a 404 on this account.

    THE COUNTER-ARGUMENT IS CARRIED, not suppressed: the prebuild is what made `[#746]`'s
    repair reach the probe container at all, because `on_configuration_change` fired on the
    `devcontainer.json` edit and baked a repaired image. Without a prebuild every creation
    runs the tree's own current `provision.sh`, which REMOVES the stale-snapshot failure class
    rather than repairing it -- an argument for disabling prebuilds, not against.
    """
    saved = COLD_CREATION_SECONDS - PREBUILT_CREATION_SECONDS
    per_week = saved * creations_per_week / 60.0
    if creations_per_week >= PREBUILD_FLIP_CREATIONS_PER_WEEK:
        rec = (f"KEEP the prebuild and re-measure: at {creations_per_week:.1f} creations/week "
               f"it saves {per_week:.1f} min/week, past the {PREBUILD_FLIP_CREATIONS_PER_WEEK:.0f}"
               f"/week flip condition. Re-ask against the storage line before making it a rule")
    else:
        rec = (f"DISABLE the prebuild: at {creations_per_week:.1f} creations/week it saves "
               f"{per_week:.1f} min/week, which is not a defensible reason to hold an image in "
               f"continuous paid storage. Re-ask above "
               f"{PREBUILD_FLIP_CREATIONS_PER_WEEK:.0f} creations/week. Disabling also removes "
               f"the stale-snapshot failure class [#746] repaired, rather than repairing it")
    return PrebuildRuling(
        decidable=False,
        saved_seconds_per_creation=saved,
        saved_minutes_per_week=per_week,
        creations_per_week=creations_per_week,
        missing_input=(
            "the prebuild image's continuous STORAGE cost, plus the Actions minutes each bake "
            "spends. Neither is readable from this account: `gh api "
            "user/settings/billing/shared-storage` and `repos/.../codespaces/prebuilds` both "
            "return 404. What would make it takeable: the Codespaces billing page's monthly "
            "storage line, or an org-level billing endpoint"),
        recommendation=rec)


# ============================================================================================ CLI

def _parse_ts(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@click.group()
def cli() -> None:
    """The CLOUD regime ([#792]) -- a meter, never a ceiling."""


@cli.command("session-start")
def cmd_session_start() -> None:
    """Surface any container OUR OWN LEDGER says is still open.

    READS THE LEDGER, NEVER THE NETWORK, and that is deliberate rather than a limitation. A
    `gh codespace list` on every session start would add a network round-trip to the boot of
    a box whose binding constraint is already resources, to answer a question our own receipts
    can answer: a row with a creation and no deletion IS, by our record, a container nobody
    tore down. Fail-soft in full.
    """
    try:
        rows = open_receipts()
        if not rows:
            click.echo("[codespace] no open container in the receipt ledger")
            return
        now = datetime.now(timezone.utc)
        for row in rows:
            created = _parse_ts(row.get("created"))
            age_days = ((now - created).total_seconds() / 86400.0) if created else 0.0
            verdict = idle_verdict("Available", age_days)
            flag = "BREACH" if verdict.breach else "open"
            click.echo(f"[codespace] {flag}: {row.get('codespace')} ({row.get('slug')}) "
                       f"{uptime_minutes(created, None, now=now):.0f} min -- {verdict.reason}")
    except Exception as exc:  # noqa: BLE001 -- a reporter never blocks a session start
        click.echo(f"[codespace] surfacing skipped: {type(exc).__name__}: {exc}")


@cli.command("prebuild")
@click.option("--creations-per-week", type=float, required=True)
def cmd_prebuild(creations_per_week: float) -> None:
    """The prebuild ruling, with its missing input named."""
    r = prebuild_ruling(creations_per_week)
    click.echo(f"saved per creation   {r.saved_seconds_per_creation:.1f} s "
               f"({COLD_CREATION_SECONDS:.1f} cold - {PREBUILT_CREATION_SECONDS:.1f} prebuilt)")
    click.echo(f"saved per week       {r.saved_minutes_per_week:.1f} min "
               f"at {r.creations_per_week:.1f} creations/week")
    click.echo(f"decidable            {r.decidable}")
    click.echo(f"missing input        {r.missing_input}")
    click.echo(f"RECOMMENDATION       {r.recommendation}")


@cli.command("receipt")
@click.option("--slug", required=True)
@click.option("--batch", required=True)
@click.option("--codespace", required=True)
@click.option("--created", required=True, help="ISO-8601 creation timestamp.")
@click.option("--deleted", default=None, help="ISO-8601 deletion timestamp; omit while open.")
@click.option("--machine", required=True)
@click.option("--prebuild/--no-prebuild", default=False)
def cmd_receipt(slug: str, batch: str, codespace: str, created: str,
                deleted: Optional[str], machine: str, prebuild: bool) -> None:
    """Append one cloud-lane receipt. Exit 1 when it would price the wrong resource."""
    try:
        row = write_receipt(slug=slug, batch=batch, codespace=codespace,
                            created=_parse_ts(created), deleted=_parse_ts(deleted),
                            machine=machine, prebuild=prebuild, tokens={})
    except ReceiptIncomplete as exc:
        click.echo(f"REFUSED: {exc}")
        sys.exit(1)
    click.echo(f"receipt written: {row['slug']} {row['uptime_minutes']} min")


if __name__ == "__main__":
    cli()
