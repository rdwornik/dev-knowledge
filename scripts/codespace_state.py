#!/usr/bin/env python
"""codespace_state.py — the recovery-container DISCRIMINATOR, and the lane-state cross ([#746]).

WHAT THIS CLOSES. A recovery container is externally indistinguishable from ours. GitHub's
documented `state` enum carries no value for it, no API field reports it, and it is reachable and
reports a live state throughout — so "the codespace is Available" has never been evidence that the
container is the one `devcontainer.json` describes. The only discriminator GitHub documents is the
CREATION LOG, which until now this repo had never fetched
(`DIGEST-2026-09-15-codespaces-reference.md` §b, §g, with sources).

WHY THE SYMPTOM GUARD WAS NOT ENOUGH. The dispatcher already refuses a container where `claude` is
missing (exit 91). That fires on a recovery container — but it names the wrong thing. A month of
repair went into the symptom (a retired call, a provenance marker, a heartbeat) because nothing
ever read the log that says, in the platform's own words, what happened.

THE MARKERS ARE MEASURED IN THIS REPO, NOT ANTICIPATED. Every entry in `RECOVERY_MARKERS` was
emitted by GitHub into this repository's own creation log on the operator's probe codespace
`lane-z-substrate-probe` (created 2026-09-14 23:36Z), read at
`/workspaces/.codespaces/.persistedshare/creation.log` and transcribed verbatim into the [#746]
amendment. That provenance is carried per-marker in the table rather than asserted in prose here,
because a marker someone EXPECTED the platform to print is a guess, and this module's whole value
is that it is not guessing. `PROVENANCE_VALUES` is a closed set so a future marker cannot be added
without saying which kind it is.

--------------------------------------------------------------------------------------------
WHAT THIS MODULE DELIBERATELY IS NOT
--------------------------------------------------------------------------------------------
It is NOT a poller, and it does not decide how state reaches it. `classify_lane` is a pure cross
over (container_state, progress_age) — whether those two inputs arrive by polling from outside, by
the lane pushing from inside, or by both, is the open architectural question filed as intake #102
and routed to the decision engine by operator directive. Building the observer here would decide
that question in a diff, which is exactly what the directive forbade. What is built is the part
every option shares: the classifier they would all call.

HONEST LIMIT, stated because the register would otherwise imply it away. `classify_creation_log`
is validated against ONE measured recovery event and one healthy log. It will name the failure
shape that killed us; it is not a proof that every recovery container GitHub can produce announces
itself with these strings. A marker set is a ratchet — it gets stronger each time a real container
teaches it a new line — and an unmatched log is reported INDETERMINATE rather than OURS, so the
unknown case fails toward suspicion instead of toward a false green.
"""
from __future__ import annotations

import enum
import json
import subprocess
from dataclasses import dataclass, field

import click

# ---------------------------------------------------------------------------------------------
# provenance vocabulary — closed, so a marker cannot be added without declaring its kind
# ---------------------------------------------------------------------------------------------
PROVENANCE_MEASURED_HERE = "measured-in-this-repo"
PROVENANCE_DOCUMENTED = "github-documented"

PROVENANCE_VALUES = frozenset({PROVENANCE_MEASURED_HERE, PROVENANCE_DOCUMENTED})


class ContainerVerdict(enum.Enum):
    """What the creation log says this container IS."""

    OURS = "ours"
    RECOVERY_CONTAINER = "recovery-container"
    CREATION_FAILED = "creation-failed"
    INDETERMINATE = "indeterminate"


class LaneState(enum.Enum):
    """What the lane inside it is DOING."""

    STARTING = "starting"
    WORKING = "working"
    HUNG = "hung"
    FINISHED = "finished"
    DIED = "died"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Marker:
    """One literal the platform emits, with the verdict it implies and where it came from."""

    text: str
    verdict: ContainerVerdict
    provenance: str
    note: str = ""


# ORDER IS SIGNIFICANT: the first match wins, and RECOVERY_CONTAINER is listed before
# CREATION_FAILED deliberately. A log that carries both lines describes one event — the creation
# failed AND the platform substituted a recovery container — and the recovery substitution is the
# stronger, more specific statement about what is now running.
RECOVERY_MARKERS: tuple[Marker, ...] = (
    Marker(
        text="Creating recovery container.",
        verdict=ContainerVerdict.RECOVERY_CONTAINER,
        provenance=PROVENANCE_MEASURED_HERE,
        note="lane-z-substrate-probe creation.log, 2026-09-14 23:37Z ([#746] amendment)",
    ),
    Marker(
        text="recovery mode",
        verdict=ContainerVerdict.RECOVERY_CONTAINER,
        provenance=PROVENANCE_DOCUMENTED,
        note='docs.github.com: "running in recovery mode due to a container error"',
    ),
    Marker(
        text="Container creation failed.",
        verdict=ContainerVerdict.CREATION_FAILED,
        provenance=PROVENANCE_MEASURED_HERE,
        note="same log, the line immediately before the recovery substitution",
    ),
    Marker(
        text="failed with exit code",
        verdict=ContainerVerdict.CREATION_FAILED,
        provenance=PROVENANCE_MEASURED_HERE,
        note="'postCreateCommand failed with exit code 1.' — the lifecycle failure itself",
    ),
)

# A log that matched nothing is only OURS if it actually shows the platform finishing. Anything
# else is INDETERMINATE: an absent or truncated log is not evidence of health, and treating it as
# health is the vacuous-gate shape this repo refuses.
HEALTHY_MARKERS: tuple[str, ...] = (
    "Finished configuring codespace.",
)


@dataclass(frozen=True)
class CreationLogVerdict:
    verdict: ContainerVerdict
    reason: str
    evidence: tuple[str, ...] = field(default_factory=tuple)


def classify_creation_log(
    text: str,
    markers: tuple[Marker, ...] | None = None,
) -> CreationLogVerdict:
    """Name what a codespace's creation log says the container is.

    Pure: takes the log text, returns a verdict plus the lines it fired on, so a caller can print
    the evidence rather than ask the reader to trust the verdict.

    `markers` is injectable, and that is not a test affordance dressed up as an API. The register's
    trip-test for this organ must prove the refusal fails WHEN THE MARKER TABLE IS EMPTIED, and a
    table read only from the module global cannot be reached by `NeuteredOrgan`, which proxies
    attributes rather than rewriting the function body. Default-reading the global at CALL time
    keeps `monkeypatch.setattr(cs, "RECOVERY_MARKERS", ())` working too.
    """
    if not text or not text.strip():
        return CreationLogVerdict(
            verdict=ContainerVerdict.INDETERMINATE,
            reason="creation log is empty or absent — that is not evidence of health",
        )

    lines = text.splitlines()
    table = RECOVERY_MARKERS if markers is None else markers

    for marker in table:
        hits = tuple(line.strip() for line in lines if marker.text in line)
        if hits:
            return CreationLogVerdict(
                verdict=marker.verdict,
                reason=(
                    f"creation log matched {marker.text!r} "
                    f"({marker.provenance}) -> {marker.verdict.value}"
                ),
                evidence=hits,
            )

    for healthy in HEALTHY_MARKERS:
        hits = tuple(line.strip() for line in lines if healthy in line)
        if hits:
            return CreationLogVerdict(
                verdict=ContainerVerdict.OURS,
                reason=f"creation log matched {healthy!r} and no failure marker",
                evidence=hits,
            )

    return CreationLogVerdict(
        verdict=ContainerVerdict.INDETERMINATE,
        reason=(
            "creation log matched no known marker — neither a failure line nor a completion "
            "line; report it rather than assume health"
        ),
    )


def classify_lane(
    container_state: str | None,
    progress_age_s: float | None,
    *,
    stale_after_s: float = 900.0,
    completed: bool = False,
) -> LaneState:
    """Cross the container's platform state with the age of the lane's own progress signal.

    THE CROSS IS THE POINT, and it is why one signal cannot do this job:

        container up   + progress fresh  -> WORKING
        container up   + progress stale  -> HUNG   (burning paid minutes)
        container up   + no progress     -> UNKNOWN, never WORKING
        container down + anything        -> DIED

    `Available` alone is NOT working — the platform reports the machine, not the workload
    (`DIGEST-2026-09-15-codespaces-reference.md` §g). Reading it as working is the false green
    that let two detached lanes produce zero work with nobody noticing.

    Which mechanism supplies `progress_age_s` is intake #102's open question; this function does
    not care, which is what keeps the choice open.
    """
    state = (container_state or "").strip()

    dead_states = {"Shutdown", "ShuttingDown", "Failed", "Unavailable", "Deleted", "Archived"}
    starting_states = {"Queued", "Provisioning", "Starting", "Created", "Awaiting"}

    if state in dead_states:
        return LaneState.DIED
    if state in starting_states:
        return LaneState.STARTING
    if state != "Available":
        return LaneState.UNKNOWN

    if completed:
        return LaneState.FINISHED
    if progress_age_s is None:
        # Up, but nothing has ever reported progress. Deliberately not WORKING.
        return LaneState.UNKNOWN
    if progress_age_s > stale_after_s:
        return LaneState.HUNG
    return LaneState.WORKING


def fetch_creation_log(codespace: str, *, runner=subprocess.run) -> str:
    """`gh codespace logs -c <name>` — the platform's own account of the build.

    Injected runner so the classifier above stays testable without a live codespace; this
    function is the only part of the module that talks to the network.
    """
    proc = runner(
        ["gh", "codespace", "logs", "-c", codespace],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout or ""


def fetch_view(codespace: str, *, runner=subprocess.run) -> dict:
    """`gh codespace view --json ...` — state and the timestamps that bound it."""
    fields = "name,state,lastUsedAt,createdAt,idleTimeoutMinutes,retentionExpiresAt,prebuild"
    proc = runner(
        ["gh", "codespace", "view", "-c", codespace, "--json", fields],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not (proc.stdout or "").strip():
        return {}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}


@click.group()
def cli() -> None:
    """Read what a codespace actually is, and what the lane inside it is doing."""


@cli.command("classify")
@click.option("--codespace", "-c", help="Codespace NAME (not display name).")
@click.option(
    "--log-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Classify a creation log already on disk instead of fetching it.",
)
def classify_cmd(codespace: str | None, log_file: str | None) -> None:
    """Name the container from its creation log, with the evidence that named it."""
    if not codespace and not log_file:
        raise click.UsageError("give --codespace or --log-file")

    if log_file:
        text = open(log_file, encoding="utf-8", errors="replace").read()
    else:
        text = fetch_creation_log(codespace)

    result = classify_creation_log(text)
    click.echo(f"verdict: {result.verdict.value}")
    click.echo(f"reason : {result.reason}")
    for line in result.evidence:
        click.echo(f"  evidence| {line}")

    # A recovery container is a FAILURE, and the exit code says so — a caller that branches on
    # this must not have to parse the prose above.
    if result.verdict in (ContainerVerdict.RECOVERY_CONTAINER, ContainerVerdict.CREATION_FAILED):
        raise SystemExit(1)
    if result.verdict is ContainerVerdict.INDETERMINATE:
        raise SystemExit(2)


if __name__ == "__main__":  # pragma: no cover - exercised via the CLI
    cli()
