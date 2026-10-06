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
It is NOT a poller. `classify_lane` stays a pure cross over (container_state, progress_age); the
architectural question of how state reaches it (intake #102) is still the decision engine's, so
this module reads ONE moment and never loops. What b2-codespace-green (R65) added is the part every
option shares: the bounded reads (`fetch_creation_log`, `fetch_state`, `fetch_progress`, each with a
timeout), an ABSENT state for a deleted box (not UNKNOWN), and `assess_lane`, which crosses state,
a heartbeat reading and an unreachable duration into a state AND a fate. The observer verb in
`dispatch.py` (`codespace-observe`) calls them once per invocation.

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
import shlex
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
    ABSENT = "absent"
    DISCONNECTED = "disconnected"
    UNKNOWN = "unknown"


#: The container state this module reports for a Codespace that a SUCCESSFUL listing does not
#: contain. GitHub has no such `state` value (a deleted codespace is simply not listed), so the
#: sentinel is ours; `fetch_state` returns it only when the listing itself was read.
ABSENT_STATE = "Absent"

#: Where the platform keeps its own account of the build, inside the container.
CREATION_LOG_PATH = "/workspaces/.codespaces/.persistedshare/creation.log"

#: A read over ssh is bounded: the night's `gh codespace logs` hung over 300 s on a recovery
#: container. 60 s is generous for a `cat` and a `stat`; a box that cannot answer in that time is
#: not answering, which the callers read as unreachable, never as health.
SSH_TIMEOUT_S = 60

#: THE STATED BOUNDS (R65, intake #102). `STALE_AFTER_S` is the age of the run log past which a lane
#: that is up is HUNG: 15 minutes is longer than the longest quiet stretch a real lane showed in
#: the night's 15-minute runs (a tool call with output only at its end), and short enough that a
#: stalled lane burns well under a core-hour before it is given a fate. `DISCONNECT_AFTER_S` is how
#: long a box may stay unreachable over ssh before the lane is DISCONNECTED: 5 minutes spans several
#: probe timeouts and a reconnect. Neither number is tuned to make a run pass.
STALE_AFTER_S = 900.0
DISCONNECT_AFTER_S = 300.0

#: The runner's heartbeat period, seconds (written by the runner `dispatch.py` ships in).
HEARTBEAT_S = 30
#: A heartbeat older than this means the runner process itself is gone.
HEARTBEAT_DEAD_AFTER_S = 3 * HEARTBEAT_S

#: The closed set of fates (R65). RUNNING and HANDBACK are not endings; FAILED carries a reason and
#: the step that failed; WAITING names the gate it waits on in its reason; TORN-DOWN is the clean
#: end of a lane whose box this line deleted.
FATES = ("RUNNING", "HANDBACK", "FAILED", "WAITING", "TORN-DOWN")


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

    if state == ABSENT_STATE:
        return LaneState.ABSENT
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


def creation_log_args(codespace: str) -> list[str]:
    """The `gh` arguments (no leading `gh`) that read the creation log over ssh. `dispatch.py`
    runs the same arguments through its own `run_gh` seam, so the two readers cannot drift."""
    return ["codespace", "ssh", "-c", codespace, "--", "cat", CREATION_LOG_PATH]


def fetch_creation_log(codespace: str, *, runner=subprocess.run,
                       timeout: float = SSH_TIMEOUT_S) -> str:
    """The platform's own account of the build, read over `gh codespace ssh -- cat`.

    NOT `gh codespace logs`: on the night of 2026-10-04 that call answered `Permission denied
    (publickey,password)` (exit 255) on a healthy box and hung over 300 s on a recovery
    container, while the ssh `cat` of the same file worked every time (night leg 5, D3). The read
    is bounded; a failure, a timeout or an empty file is the EMPTY string, which
    `classify_creation_log` reads as INDETERMINATE -- never as health.

    Injected runner so the classifier above stays testable without a live codespace; this
    function is the only part of the module that talks to the network.
    """
    try:
        proc = runner(["gh", *creation_log_args(codespace)], capture_output=True, text=True,
                      check=False, timeout=timeout, stdin=subprocess.DEVNULL)
    except (subprocess.TimeoutExpired, OSError):
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout or ""


def fetch_state(codespace: str, *, runner=subprocess.run,
                timeout: float = SSH_TIMEOUT_S) -> str | None:
    """The container's platform state from a LISTING, or `ABSENT_STATE`, or None.

    `gh codespace view` of a deleted codespace fails like any other error, which is why the view
    could not tell DELETED from UNREACHABLE and the classifier read `unknown` for both (D4). A
    listing that SUCCEEDS and does not contain the name is the proof of absence; a listing that
    could not be read says nothing (None) -- 'could not look' is not 'gone', the rule
    `codespace_parity.verify_cleanup` applies to the same listing."""
    try:
        proc = runner(["gh", "codespace", "list", "--json", "name,state"], capture_output=True,
                      text=True, check=False, timeout=timeout, stdin=subprocess.DEVNULL)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0:
        return None
    try:
        rows = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return None
    if not isinstance(rows, list):
        return None
    return state_from_listing(rows, codespace)


def state_from_listing(rows: list, codespace: str) -> str:
    """`codespace`'s state in an already-read listing, `ABSENT_STATE` when it is not in it."""
    for row in rows:
        if isinstance(row, dict) and row.get("name") == codespace:
            return str(row.get("state") or "")
    return ABSENT_STATE


@dataclass(frozen=True)
class ProgressReading:
    """One read of the lane's progress signal over ssh, on the REMOTE clock.

    `age_s` is the age of `run.log` (the lane's stdout and stderr): a lane that works writes it.
    `runner_alive` is the runner's own heartbeat file's freshness. `receipt_present` is the
    completion signal. `reachable` False means the read itself failed or came back unreadable."""

    reachable: bool
    age_s: float | None = None
    runner_alive: bool | None = None
    receipt_present: bool = False
    error: str = ""


def progress_script(workdir: str) -> str:
    """The one shell line the probe runs in the container: remote `now`, the mtimes of `run.log`
    and `heartbeat`, and whether `receipt.json` exists -- one `key=value` line, no secrets."""
    log, hb, receipt = (shlex.quote(f"{workdir}/{name}")
                        for name in ("run.log", "heartbeat", "receipt.json"))
    return ("echo now=$(date +%s)"
            f" log=$(stat -c %Y {log} 2>/dev/null || echo -)"
            f" hb=$(stat -c %Y {hb} 2>/dev/null || echo -)"
            f" receipt=$([ -f {receipt} ] && echo 1 || echo 0)")


def progress_args(codespace: str, workdir: str) -> list[str]:
    """The `gh` arguments (no leading `gh`) for the progress probe. `gh codespace ssh` hands the
    words after `--` to ssh, which joins them with spaces for the REMOTE shell to parse again, so
    the script is quoted once here -- a bare script would be split into `sh -c echo`."""
    return ["codespace", "ssh", "-c", codespace, "--", "sh", "-c",
            shlex.quote(progress_script(workdir))]


def parse_progress(stdout: str) -> ProgressReading:
    """Read the probe's one line. Anything else is UNREACHABLE: an unreadable answer is not a
    progress reading, and a missing `run.log` is no age at all (never zero seconds)."""
    fields: dict[str, str] = {}
    for token in (stdout or "").split():
        key, sep, value = token.partition("=")
        if sep:
            fields[key] = value
    try:
        now = float(fields["now"])
        if fields["receipt"] not in ("1", "0"):
            raise ValueError("receipt")
        receipt = fields["receipt"] == "1"
        log = None if fields["log"] == "-" else float(fields["log"])
        hb = None if fields["hb"] == "-" else float(fields["hb"])
    except (KeyError, ValueError):
        return ProgressReading(reachable=False, error="the probe's answer was unreadable")
    return ProgressReading(
        reachable=True,
        age_s=None if log is None else max(now - log, 0.0),
        runner_alive=hb is not None and (now - hb) <= HEARTBEAT_DEAD_AFTER_S,
        receipt_present=receipt)


def fetch_progress(codespace: str, workdir: str, *, runner=subprocess.run,
                   timeout: float = SSH_TIMEOUT_S) -> ProgressReading:
    """The progress probe over ssh, bounded. A failure or a timeout is UNREACHABLE."""
    try:
        proc = runner(["gh", *progress_args(codespace, workdir)], capture_output=True, text=True,
                      check=False, timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return ProgressReading(reachable=False, error=f"the probe timed out after {timeout}s")
    except OSError as exc:
        return ProgressReading(reachable=False, error=f"gh could not be run: {exc}")
    if proc.returncode != 0:
        return ProgressReading(reachable=False, error=f"ssh exited {proc.returncode}")
    return parse_progress(proc.stdout or "")


@dataclass(frozen=True)
class LaneAssessment:
    """The lane's state and what follows from it (R65): its fate, the reason, the failing step."""

    state: LaneState
    fate: str
    reason: str
    step: str = ""


def assess_lane(
    container_state: str | None,
    reading: ProgressReading | None,
    *,
    unreachable_for_s: float = 0.0,
    expected_gone: bool = False,
    stale_after_s: float = STALE_AFTER_S,
    disconnect_after_s: float = DISCONNECT_AFTER_S,
) -> LaneAssessment:
    """Cross the platform state, the progress reading and how long the box has been unreachable
    into a state AND a fate. Every input has an answer in `FATES`: a stalled or disconnected lane
    is FAILED with its reason and the step that failed; what cannot be read is WAITING, with the
    gate named; nothing is `unknown` without a fate.

    `expected_gone` is the caller's statement that THIS line deleted the codespace (so absence is
    the clean end, TORN-DOWN, rather than a box that vanished)."""
    up = (container_state or "").strip() == "Available"
    readable = reading is not None and reading.reachable
    state = classify_lane(
        container_state,
        reading.age_s if readable else None,
        stale_after_s=stale_after_s,
        completed=bool(readable and reading.receipt_present),
    )
    if state is LaneState.ABSENT:
        if expected_gone:
            return LaneAssessment(state, "TORN-DOWN",
                                  "the codespace is not listed and this line deleted it")
        return LaneAssessment(state, "FAILED",
                              "the codespace is not listed but this line never deleted it",
                              step="observe")
    if state is LaneState.DIED:
        return LaneAssessment(state, "FAILED",
                              f"the container is {container_state}: the lane cannot be running",
                              step="run")
    if state is LaneState.STARTING:
        return LaneAssessment(state, "RUNNING", f"the container is {container_state}")
    if state is LaneState.FINISHED:
        return LaneAssessment(state, "HANDBACK", "receipt.json is on the box: harvest, then delete")
    if state is LaneState.HUNG:
        if reading is not None and reading.runner_alive is False:
            return LaneAssessment(
                LaneState.DIED, "FAILED",
                f"the runner stopped heartbeating and no receipt was written; the run log is "
                f"{reading.age_s:.0f}s old", step="run")
        return LaneAssessment(
            state, "FAILED",
            f"hung: no progress for {reading.age_s:.0f}s (bound {stale_after_s:.0f}s)", step="run")
    if state is LaneState.WORKING:
        return LaneAssessment(state, "RUNNING",
                              f"progress {reading.age_s:.0f}s ago (bound {stale_after_s:.0f}s)")
    # UNKNOWN from here: the box is up (or its state unreadable) and no progress was read.
    if up and not readable and unreachable_for_s >= disconnect_after_s:
        return LaneAssessment(
            LaneState.DISCONNECTED, "FAILED",
            f"disconnected: unreachable over ssh for {unreachable_for_s:.0f}s "
            f"(bound {disconnect_after_s:.0f}s)", step="observe")
    if container_state is None:
        gate = "a readable `gh codespace list` (the platform state could not be read)"
    elif not readable:
        gate = (f"a readable progress probe over ssh (unreachable {unreachable_for_s:.0f}s of "
                f"{disconnect_after_s:.0f}s)")
    else:
        gate = "a run log: nothing has written one yet"
    return LaneAssessment(LaneState.UNKNOWN, "WAITING", f"waiting on {gate}", step="observe")


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
