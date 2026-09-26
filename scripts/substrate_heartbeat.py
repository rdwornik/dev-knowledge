#!/usr/bin/env python
"""substrate_heartbeat.py — L2: the substrate is proven live on a SCHEDULE ([#554], [#746]).

THE FACT THIS LAYER IS BUILT ON. The substrate died at one commit and nobody noticed for two
weeks BECAUSE NOTHING RAN THERE. `provision.sh` reached a call site for a module retired twelve
days earlier, exited non-zero, and Codespaces substituted a bare recovery container while the
platform reported Available throughout. Nobody dispatched to it in the interval, so nobody found
out. A health signal that only fires when someone happens to use the thing is not a health
signal — it is a usage log. Removing the dependency on usage is the whole point of this module.

TWO LEGS, AND THE SECOND IS THE ONE THAT MUST NOT BE OPTIONAL:

  * the SCHEDULED leg (`.github/workflows/substrate-heartbeat.yml`) runs `probe` on a cron and
    writes a receipt, whether or not anybody is using the substrate;
  * the PRE-DISPATCH leg (`predispatch`, wired into `validate_substrate`'s rule surface) turns
    that receipt into a REFUSAL AT DISPATCH rather than a discovery mid-batch.

Wired where dispatch actually reads it: `validate_substrate.validate_contract` is the organ that
refuses a lane contract before it is dispatched, so the leg lives there and not in prose beside
it. It fires for OFF-MACHINE substrates only — a `local` lane runs on the operator's machine,
whose liveness is not in question because the operator is sitting at it, and gating it on a
cloud probe would refuse the one substrate that is definitely alive.

--------------------------------------------------------------------------------------------
CREDENTIAL-FREE, BY MEASUREMENT AND NOT BY PREFERENCE
--------------------------------------------------------------------------------------------
This repo has NO ACTIONS SECRETS AT ALL: `gh secret list` returns `[]` and
`repos/rdwornik/dev-knowledge/actions/secrets` returns `total_count: 0`; `conductor.yml:178`
already guards for the absence of both `CODEX_API_KEY` and `ANTHROPIC_API_KEY`. A scheduled leg
that needed a model credential would be permanently red, so this one needs none — checking
toolchain and declaration identity is not a task a model does.

WHAT A CREDENTIAL-FREE PROBE CAN HONESTLY ASSERT, stated as a boundary rather than glossed. It
reads the DECLARATION — the provisioning chain as the repo declares it — and it catches the
class that actually killed the container:

  D1  every repo file the provisioning surfaces NAME in executable position still exists.
      This IS the 2026-09-14 outage. No container, no credential, no network.
  D2  the pins have single sources and are readable (an exact `==` uv pin, ADR-106).
  D3  the provisioning entrypoint is reachable from `devcontainer.json`'s lifecycle commands.
  D4  the provisioning surfaces are still declared in FPG-1's `WIRING_SURFACES`, so L3's
      protection cannot regress silently underneath this.
  D5  `provision.sh` still writes AND verifies the L1 marker — because a provision.sh that
      stopped writing it would make every later `verify` refuse a container that is fine.

WHAT IT CANNOT ASSERT, and the honest limit bounds what a green reading means: it does not
BUILD the container. A declaration can be perfectly coherent and the image still fail to build,
and only a real build answers that. The build leg is DECLARED and NOT ARMED at the foot of
`.github/workflows/substrate-heartbeat.yml` — it needs a third-party action this repo does not
use and Actions minutes against a live spend ruling, both operator decisions — so a green
reading here means "the declaration is coherent" and never "the image builds".

WHERE THE RECEIPT LIVES, and why it is not repo state at all — it is not even IN the repo.
It sits beside L1's provenance marker in the user state directory, because it records a fact
about THIS MACHINE rather than about the corpus. `predispatch` reads MACHINE-LOCAL state:
the question it asks is "has THIS machine proven the substrate live recently", and the scheduled
run answers a different one — "is it broken for everyone" — by going red. The workflow runs
`contents: read` and commits nothing; pushing a bot commit to `main` would drive through the
repo's own never-commit-to-main invariant for a file that goes stale the moment it lands.

EXIT CODES. 0 clean · 1 a real violation · 2 could not look (STANDING_RULINGS F4).

Layer-2 / read-only (ADR-28/36): reads the repo, and writes exactly one file — the receipt,
outside the working tree by construction.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("substrate-heartbeat")

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

SCHEMA = "dev-knowledge-substrate-heartbeat/1"

#: The receipt's filename inside the machine-local state directory. It lives OUTSIDE the
#: working tree, in the same home as L1's provenance marker, and the reasons are the same
#: three: it is a fact about THIS MACHINE and not about the corpus; a Layer-2 module writing
#: repo state on every probe would dirty the tree and trip session-end backpressure; and one
#: machine's reading committed as everyone's is the shared-slot defect the per-substrate
#: keying exists to avoid.
RECEIPT_FILENAME = "substrate-heartbeat.json"

#: How old a proof may be before dispatch refuses. The scheduled leg runs DAILY, so 36 h is one
#: missed run of slack and no more: two consecutive silent days is exactly the state that let a
#: dead substrate look alive, and a window wide enough to absorb it would re-open the hole this
#: module closes.
MAX_AGE_HOURS = 36

#: The surfaces whose declaration this probe reads. Imported from FPG-1 at call time rather than
#: restated — the enum is the graph's, and a second copy here would be free to drift from the
#: one `safe_remove` and the orphan census actually enforce.
PROVISIONING_SURFACES: tuple[str, ...] = (
    ".devcontainer/devcontainer.json",
    ".devcontainer/provision.sh",
)


@dataclass(frozen=True)
class Reading:
    """One substrate's health at one moment. `findings` is the evidence a refusal must name."""

    substrate: str
    status: str                 # "live" | "dead" | "undetermined"
    measured_at: str
    findings: list[str] = field(default_factory=list)
    source: str = "local"

    def as_dict(self) -> dict:
        return {"status": self.status, "measured_at": self.measured_at,
                "findings": list(self.findings), "source": self.source}


@dataclass(frozen=True)
class Receipt:
    """The readings, keyed by substrate. PER-SUBSTRATE for the same reason L1's marker is
    per-substrate: one shared slot means the last writer's answer is read as everyone's."""

    readings: dict[str, dict]

    @classmethod
    def empty(cls) -> "Receipt":
        return cls({})

    def reading(self, substrate: str) -> dict | None:
        return self.readings.get(substrate)

    def as_dict(self) -> dict:
        return {"schema": SCHEMA, "readings": self.readings}


# --- the credential-free declaration probe ----------------------------------------------------

def _fpg():
    """FPG-1, imported at call time. The graph pulls in rustworkx and four sibling validators,
    and a heartbeat that paid that at import would be a heavy import for every consumer."""
    try:
        from scripts import file_purpose_graph as module
    except ImportError:  # pragma: no cover - exercised by the alternate launch path
        import file_purpose_graph as module
    return module


def _provenance():
    try:
        from scripts import substrate_provenance as module
    except ImportError:  # pragma: no cover - exercised by the alternate launch path
        import substrate_provenance as module
    return module


def declaration_findings(repo_root: Path) -> list[str]:
    """D1-D5. Empty means the declared provisioning chain is coherent. Never raises."""
    root = Path(repo_root)
    fpg = _fpg()
    findings: list[str] = []

    # --- D1: a call site pointing at a file that is not there -----------------------------
    #
    # THE OUTAGE, as a predicate. `_SCRIPT_PATH_RE` is FPG-1's own definition of a path in
    # executable position, reused rather than re-expressed: a private regex here could admit a
    # spelling the graph refuses (or the reverse), and then the probe and the removal gate
    # would disagree about what "provisioning calls this" means.
    for rel in PROVISIONING_SURFACES:
        path = root / rel
        if not path.is_file():
            findings.append(f"D1 {rel} is declared provisioning and is not on disk")
            continue
        for value in fpg._surface_strings(path):
            for named in fpg._SCRIPT_PATH_RE.findall(value):
                if not (root / named).is_file():
                    findings.append(
                        f"D1 {rel} names {named} in executable position and it is not on "
                        f"disk — this is the 2026-09-14 shape: the call exits non-zero, "
                        f"provisioning dies, and the platform substitutes a recovery container")

    # --- D2: the pins have single sources and are readable ---------------------------------
    provenance = _provenance()
    try:
        provenance.read_pins(root)
    except provenance.ProvenanceError as exc:
        findings.append(f"D2 {exc}")

    # --- D3 / D4: the chain is reachable, and FPG-1 still declares it -----------------------
    for rel in PROVISIONING_SURFACES:
        if rel not in fpg.WIRING_SURFACES:
            findings.append(
                f"D4 {rel} is not in file_purpose_graph.WIRING_SURFACES — L3's protection "
                f"regressed, so retiring a file provisioning calls would pass as safe again")
    targets = fpg.wiring_targets(root)
    entry = ".devcontainer/provision.sh"
    if entry not in targets.get(".devcontainer/devcontainer.json", set()):
        findings.append(
            "D3 devcontainer.json's lifecycle commands do not reach "
            f"{entry} — the substrate would come up with no provisioning run at all")

    # --- D5: L1 is still wired into provisioning -------------------------------------------
    provision = root / entry
    if provision.is_file():
        text = provision.read_text(encoding="utf-8", errors="replace")
        for verb in ("write", "verify"):
            if f"scripts/substrate_provenance.py {verb}" not in text:
                findings.append(
                    f"D5 provision.sh no longer runs `substrate_provenance.py {verb}` — L1 is "
                    f"unwired, so either no container can prove its identity or every "
                    f"container is refused for a marker nothing writes")
    return findings


def probe(repo_root: Path, substrate: str, *, now: dt.datetime | None = None,
          source: str = "local") -> Reading:
    """Is this substrate's declared provisioning chain coherent right now? Never raises."""
    now = now or dt.datetime.now(dt.timezone.utc)
    try:
        findings = declaration_findings(Path(repo_root))
    except Exception as exc:                      # the probe must report, never crash a schedule
        return Reading(substrate, "undetermined", _stamp(now),
                       [f"the probe could not look ({exc.__class__.__name__}: {exc})"], source)
    return Reading(substrate, "dead" if findings else "live", _stamp(now), findings, source)


def _stamp(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(stamp: str) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


# --- the receipt ---------------------------------------------------------------------------------

def receipt_path(repo_root: Path, env: dict | None = None) -> Path:
    """Where this machine's readings live — NOT in the repo.

    Reuses `substrate_provenance.provenance_dir`, so "where machine-local substrate state
    lives" has ONE definition, including its refusal of the world-writable temp root. Two
    answers to that question would be two places for a reader to look and one of them stale.
    """
    return _provenance().provenance_dir(env) / RECEIPT_FILENAME


def read_receipt(repo_root: Path, path: Path | None = None,
                 env: dict | None = None) -> Receipt:
    """The receipt, or an EMPTY one. Absence is not an error — it is the reading "never proven
    live", which `predispatch` treats as the refusal it is."""
    try:
        target = Path(path) if path else receipt_path(repo_root, env)
    except Exception:
        return Receipt.empty()
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return Receipt.empty()
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        return Receipt.empty()
    readings = payload.get("readings")
    return Receipt(readings if isinstance(readings, dict) else {})


def write_receipt(repo_root: Path, reading: Reading, path: Path | None = None,
                  env: dict | None = None) -> Path:
    """MERGE, never replace. A probe of one substrate must not erase what is known about the
    others — the per-substrate separation is worthless if the writer collapses it."""
    target = Path(path) if path else receipt_path(repo_root, env)
    receipt = read_receipt(repo_root, target)
    readings = dict(receipt.readings)
    readings[reading.substrate] = reading.as_dict()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(Receipt(readings).as_dict(), indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    return target


# --- the pre-dispatch leg ---------------------------------------------------------------------

def predispatch(repo_root: Path, substrate: str, *, now: dt.datetime | None = None,
                receipt: Receipt | None = None, env: dict | None = None,
                max_age_hours: int = MAX_AGE_HOURS) -> list[str]:
    """Why dispatch to `substrate` must be refused, or `[]`. Never raises.

    ABSENCE IS A REFUSAL, not an "unknown, proceed". A substrate nothing has ever proven live is
    precisely the state the codespace was in for two weeks while the platform said Available,
    and treating that as neutral is how the defect survived. The refusal is discharged by
    running the probe, which is cheap and needs no credential.
    """
    now = now or dt.datetime.now(dt.timezone.utc)
    receipt = read_receipt(repo_root, env=env) if receipt is None else receipt
    reading = receipt.reading(substrate)
    if reading is None:
        return [f"substrate {substrate!r} has no heartbeat reading — it has NEVER been proven "
                f"live. Run: uv run --locked python scripts/substrate_heartbeat.py probe "
                f"--substrate {substrate} --write-receipt"]

    out: list[str] = []
    status = reading.get("status")
    if status != "live":
        findings = reading.get("findings") or []
        out.append(f"substrate {substrate!r} last probed {status!r}: "
                   + ("; ".join(findings) if findings else "no finding recorded"))

    measured = _parse(reading.get("measured_at", ""))
    if measured is None:
        out.append(f"substrate {substrate!r} carries an unparseable measurement time "
                   f"{reading.get('measured_at')!r} — a reading whose age cannot be read is "
                   f"not a proof of currency")
    else:
        age = (now - measured).total_seconds() / 3600
        if age > max_age_hours:
            out.append(
                f"substrate {substrate!r} was last proven live {age:.0f} h ago, which is stale "
                f"against the {max_age_hours} h window — the scheduled probe runs daily, so "
                f"this means two consecutive runs are missing, which is the silence the "
                f"heartbeat exists to break")
    return out


# --- the prebuild-freshness leg (LANE-5B2-23 / LANE-5B3-9 Done-contract item 3) -----------------
#
# THE MEASURED DEFECT THIS CHECKS FOR (close packet §11 defect 3, 2026-08-26, cited in
# `provision.sh`'s own header): a codespace created from the prebuilt image came up at a
# 2026-08-22 commit while the pushed tip was three days newer, with `git status -sb` reporting
# no divergence because the clone had never fetched. `provision.sh::refresh_source_tree` fixes
# that AFTER a container starts; this leg is what catches it BEFORE one is ever created — a
# heartbeat run that asks whether the prebuilt image itself is still current.
#
# THE ENDPOINT, measured 2026-09-26 live against rdwornik/dev-knowledge (this lane).
# `.devcontainer/provisioning.yaml`'s own header already records two dead ends so a future
# reader does not re-probe them: the prebuild CONFIGURATION endpoint 404s
# (`GET /repos/{repo}/codespaces/prebuilds`), and nothing reads the `prebuild:` block it
# declares. Neither is what this reads. GitHub auto-generates an internal Actions workflow the
# moment a repo's prebuild is actually turned on in Settings -> Codespaces (docs.github.com,
# "Configuring prebuilds"), and every PREBUILD BUILD is a real run of it — surfaced by the
# ordinary Actions API at the synthetic path `dynamic/codespaces/create_codespaces_prebuilds`,
# readable with the workflow's own default `GITHUB_TOKEN` given `actions: read` (a workflow
# PERMISSION, declared in the workflow file — never a stored secret; R2 untouched).


def _gh_json(argv: list[str], *, env: dict | None = None,
            timeout: int = 30) -> object | None:
    """`gh <argv>`, parsed as JSON, or `None` on ANY failure — absent `gh`, a non-zero exit, or
    unparseable output all collapse to the one "could not look" outcome, so no caller ever
    mistakes "the read failed" for "the read succeeded and found nothing"."""
    try:
        proc = subprocess.run(["gh", *argv], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, env=env)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except ValueError:
        return None


def _prebuild_declaration(repo_root: Path) -> dict:
    """The repo-side record — `.devcontainer/provisioning.yaml`'s `prebuild:` block — the single
    source for which repository and ref this leg asks about (never re-typed here)."""
    import yaml  # lazy: this module stays a light import for every OTHER caller (see header)

    path = Path(repo_root) / ".devcontainer" / "provisioning.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):
        return {}
    return data.get("prebuild", {}) if isinstance(data, dict) else {}


def _newest_devcontainer_commit(repo_root: Path) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "log", "-1", "--format=%H", "--", ".devcontainer"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    sha = proc.stdout.strip()
    return sha or None


def _is_ancestor(repo_root: Path, older: str, newer: str) -> bool | None:
    """`True` / `False`, or `None` when the question cannot be answered here (a commit this
    clone never fetched is not a diverged one — see `substrate_provenance.LiveProbe.is_ancestor`,
    the same shape reused rather than re-derived)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", older, newer],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    return None


@dataclass(frozen=True)
class PrebuildVerdict:
    """`status`: `ok` (fresh) / `refused` (looked, found staleness or the specific 2026-08-26
    defect shape) / `undetermined` (could not look at all — the 1/2 exit split every module in
    this family already uses, STANDING_RULINGS F4)."""

    status: str
    findings: list[str] = field(default_factory=list)
    prebuild_run_id: int | None = None
    prebuild_sha: str | None = None

    @property
    def exit_code(self) -> int:
        return {"ok": 0, "refused": 1}.get(self.status, 2)


def _prebuild_fallback(repo: str, declared: dict, env: dict | None,
                       *, reason: str) -> PrebuildVerdict:
    """The read path the token DOES have when it cannot read Actions runs (Done-contract item
    3's named escape valve). `prebuild_availability` on the machines endpoint is a live yes/no
    with NO commit sha attached, so this can only ever report UNDETERMINED, never "fresh" — it
    is strictly weaker than the primary path and used only when that path is unavailable."""
    import urllib.parse

    ref = declared.get("ref", "main")
    # Inline query string, not `-f` — see the sibling call in `prebuild_freshness` for why.
    machines = _gh_json(
        ["api", f"repos/{repo}/codespaces/machines?ref={urllib.parse.quote(ref)}"], env=env)
    if machines is None:
        return PrebuildVerdict("undetermined", [
            f"{reason}; the fallback read (GET /repos/{{owner}}/{{repo}}/codespaces/machines, "
            "docs.github.com 'Get available machine types for a repository') also failed — "
            "neither read path answered"])
    avail = {m.get("name"): m.get("prebuild_availability")
            for m in (machines.get("machines") or []) if isinstance(m, dict)}
    return PrebuildVerdict("undetermined", [
        f"{reason}; used the fallback read instead (GET /repos/{{owner}}/{{repo}}/codespaces/"
        f"machines): prebuild_availability = {avail!r} — this field carries no commit sha, so "
        "it can report available/none but never FRESH; recorded as undetermined, not clean"])


def prebuild_freshness(repo_root: Path, *, env: dict | None = None) -> PrebuildVerdict:
    """Does the newest successful Codespaces prebuild contain the newest commit on `main` that
    touches `.devcontainer/**`? Never raises."""
    declared = _prebuild_declaration(repo_root)
    repo = declared.get("repository")
    if not repo:
        return PrebuildVerdict("undetermined", [
            "'.devcontainer/provisioning.yaml' prebuild.repository is not set — nothing to "
            "check prebuild freshness against"])

    workflows = _gh_json(["api", f"repos/{repo}/actions/workflows"], env=env)
    if workflows is None:
        return _prebuild_fallback(
            repo, declared, env,
            reason=f"could not list Actions workflows via `gh api repos/{repo}/actions/"
                   "workflows` — is GH_TOKEN set, and does it carry `actions: read`?")

    prebuild_wf = next(
        (w for w in (workflows.get("workflows") or [])
         if isinstance(w, dict) and str(w.get("path", "")).startswith("dynamic/codespaces/")),
        None)
    if prebuild_wf is None:
        return PrebuildVerdict("undetermined", [
            "no auto-generated 'Codespaces Prebuilds' workflow exists under "
            "dynamic/codespaces/… — GitHub creates this only once a prebuild configuration is "
            "actually saved in repo Settings > Codespaces; none is live, so there is no "
            "prebuild to check freshness against"])

    # THE QUERY STRING IS INLINE, never `-f`/`-F`: `gh api` switches its HTTP method to POST the
    # moment any `-f`/`-F` parameter is given (measured 2026-09-26 against this exact call — a
    # bare `-f status=success -f per_page=1` 404s, because there is no POST on this endpoint;
    # `-X GET` alongside `-f` also works, but an inline query string needs neither flag and
    # cannot silently regress if a later edit drops the `-X`).
    runs = _gh_json(
        ["api", f"repos/{repo}/actions/workflows/{prebuild_wf['id']}/runs"
                "?status=success&per_page=1"], env=env)
    if runs is None:
        return _prebuild_fallback(
            repo, declared, env,
            reason=f"could not list runs of workflow {prebuild_wf['id']} "
                   f"({prebuild_wf.get('path')})")

    run_list = [r for r in (runs.get("workflow_runs") or []) if isinstance(r, dict)]
    if not run_list:
        return PrebuildVerdict("undetermined", [
            "the 'Codespaces Prebuilds' workflow exists but has never completed a successful "
            "run — no prebuilt image to check freshness against"])

    newest_run = run_list[0]
    prebuild_sha = newest_run.get("head_sha")
    run_id = newest_run.get("id")
    if not prebuild_sha:
        return PrebuildVerdict("undetermined", [
            f"the newest successful prebuild run (id {run_id}) carries no head_sha"],
            prebuild_run_id=run_id)

    newest_devcontainer = _newest_devcontainer_commit(repo_root)
    if newest_devcontainer is None:
        # Nothing under .devcontainer/** has ever been committed in this clone — there is
        # nothing for the prebuild to be stale AGAINST, so this is clean rather than refused.
        return PrebuildVerdict("ok", [], prebuild_run_id=run_id, prebuild_sha=prebuild_sha)

    ancestry = _is_ancestor(repo_root, newest_devcontainer, prebuild_sha)
    if ancestry is True:
        return PrebuildVerdict("ok", [], prebuild_run_id=run_id, prebuild_sha=prebuild_sha)
    if ancestry is False:
        return PrebuildVerdict("refused", [
            f"the newest successful Codespaces prebuild (run {run_id}, sha "
            f"{prebuild_sha[:12]}) does NOT contain {newest_devcontainer[:12]}, the newest "
            "commit on main touching .devcontainer/** — a codespace created from this "
            "prebuild would run provisioning older than main, the exact shape of the "
            "2026-08-26 close-packet defect 3"], prebuild_run_id=run_id,
            prebuild_sha=prebuild_sha)
    return PrebuildVerdict("undetermined", [
        f"git merge-base --is-ancestor could not resolve {newest_devcontainer[:12]} against "
        f"the prebuild's {prebuild_sha[:12]} in this clone — one of the two is not reachable "
        "here"], prebuild_run_id=run_id, prebuild_sha=prebuild_sha)


# --- CLI ---------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="substrate_heartbeat.py",
        description="L2 — prove a substrate live on a schedule, and refuse dispatch when it "
                    "is not ([#554])")
    parser.add_argument("command", choices=("probe", "predispatch", "show", "prebuild"))
    parser.add_argument("--repo-root", default=str(_REPO_ROOT))
    parser.add_argument("--substrate", default="codespace")
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--receipt-path", default=None,
                        help="write/read the receipt HERE instead of the machine-local state "
                             "directory. For an ephemeral runner with no tree to dirty — the "
                             "scheduled workflow uses it so upload-artifact has something to "
                             "collect. Not for a workstation: a receipt inside the repo is one "
                             "machine's reading sitting where everyone's would be read.")
    parser.add_argument("--source", default="local",
                        help="what produced this reading (local, actions, in-container)")
    parser.add_argument("--max-age-hours", type=int, default=MAX_AGE_HOURS)
    args = parser.parse_args(argv)
    root = Path(args.repo_root)
    where = Path(args.receipt_path) if args.receipt_path else None

    if args.command == "show":
        print(json.dumps(read_receipt(root, where).as_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "prebuild":
        import os
        verdict = prebuild_freshness(root, env=os.environ.copy())
        for finding in verdict.findings:
            (logger.error if verdict.status == "refused" else logger.info)("%s", finding)
        if verdict.prebuild_run_id is not None:
            logger.info("prebuild: newest successful run id=%s head_sha=%s",
                       verdict.prebuild_run_id, verdict.prebuild_sha)
        logger.info("prebuild freshness: %s", verdict.status)
        return verdict.exit_code

    if args.command == "probe":
        reading = probe(root, args.substrate, source=args.source)
        for finding in reading.findings:
            logger.error("REFUSED: %s", finding)
        if args.write_receipt:
            logger.info("receipt written: %s", write_receipt(root, reading, where))
        logger.info("substrate %s: %s", reading.substrate, reading.status)
        return {"live": 0, "dead": 1}.get(reading.status, 2)

    refusals = predispatch(root, args.substrate, max_age_hours=args.max_age_hours,
                           receipt=read_receipt(root, where) if where else None)
    for line in refusals:
        logger.error("REFUSED: %s", line)
    if not refusals:
        logger.info("substrate %s: dispatch admitted", args.substrate)
    return 1 if refusals else 0


if __name__ == "__main__":       # pragma: no cover - exercised by the workflow and the gate
    sys.exit(main())
