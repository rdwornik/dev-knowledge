#!/usr/bin/env python
"""aj_scan.py -- the Architekt Jutra delta scan, as a mechanism (LANE-5B2-15, `to-browser/
DIGEST-AJ-DELTA-2026-09-25.md`).

Until this lane, every Architekt Jutra comparison was a one-off Gemini read whose result lived
only on the transport (`docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md`,
`docs/audits/2026-09-21-technical-aj-all-front.md`). This module turns that into a command: given
the course folder and the reference-repository names, it lists what changed since the last
recorded scan and emits candidate rows against it, recording a new high-water mark.

=================================================================================================
WHAT "CHANGED" MEANS, AND WHAT DOES NOT NEED A FRESH READ
=================================================================================================

Three kinds of delta, and each is handled differently on purpose:

  * COURSE FILES newer than the state's `course_high_water` -- a plain `stat().st_mtime` walk,
    mechanical, no LLM needed to detect them.
  * REFERENCE-REPO COMMITS since the state's per-repo `since` -- `gh api repos/<repo>/commits`,
    mechanical, no LLM needed to list them.
  * CARRIED CANDIDATES -- rows an earlier scan already derived from a large read (course lesson
    content, a commit diff) that no lane has yet turned into a filed backlog row. These are NOT
    re-derived: the state file keeps them verbatim until an operator files them, because
    re-reading the same lesson content on every scan would burn the exact large-read cost this
    module exists to avoid paying twice.

Only a GENUINELY NEW delta (a course file or a commit this state has never seen) triggers a
fresh large-read leg, and per the contract that leg is DELEGATED rather than read in-process --
`delegate_describe` shells out to a subagent CLI (`agy` by default, the same one
`scripts/provider_bench.py` already benches) rather than this script parsing PDF/MP3/diff
content itself. The served model is recorded on the row; `agy` 1.2.x discloses no model id in
its JSON envelope (measured in `scripts/provider_bench.py::AGY_ATTESTATION_NONE` and in this
lane's own DIGEST-AJ-DELTA input), so that case records `"undisclosed"` rather than a guess.

=================================================================================================
PORTABILITY -- NO OPERATOR-DISK PATH IN THE STATE FILE
=================================================================================================

`--course` is a CLI argument, never a literal in this module or in `ecosystem/aj-scan-state.yaml`
(ruling (a), LANE-5B2-15). The state file records only a timestamp (the course high-water mark)
and repo slugs (`owner/name`, already public identifiers) -- never the course directory path
itself, so the state file, this module and the skill that invokes it stay portable to a
different operator's disk.

=================================================================================================
CALL SURFACE
=================================================================================================

    uv run --locked python scripts/aj_scan.py scan --course "<course dir>" \
        --repos Architekt-Jutra/architekt-jutra-code,TheSoftwareHouse/copilot-collections,SkillPanel/maister \
        --since-state ecosystem/aj-scan-state.yaml
    uv run --locked python scripts/aj_scan.py scan ... --json
    uv run --locked python scripts/aj_scan.py scan ... --dry-run   # do not write the state file
"""
from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

import click
import yaml

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("aj-scan")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

#: Default location of the state file relative to the repo root -- the one path named in the
#: lane's "Files you own" list.
DEFAULT_STATE_RELPATH = "ecosystem/aj-scan-state.yaml"

GH_TIMEOUT_S = 120
DELEGATE_TIMEOUT_S = 600


class ScanError(RuntimeError):
    """A source the scan needs (state file, course dir, `gh`, the delegate CLI) could not be
    read. Raised rather than degraded: a scan that silently treated an unreadable source as
    "nothing changed" would under-report exactly like a missed high-water mark, and the whole
    point of recording one is to never miss a delta silently."""


# --- state ---------------------------------------------------------------------------------


@dataclass
class RepoState:
    """One reference repo's high-water mark. `since` is an ISO 8601 timestamp used verbatim as
    `gh api repos/<repo>/commits?since=<since>`."""

    since: str


@dataclass
class CarriedCandidate:
    """A candidate row an earlier scan already derived (via a delegated large read) and no lane
    has filed yet. Carried forward byte-for-byte until an operator removes it from the state
    file (by filing the row) -- this module never edits or drops one on its own."""

    id: str
    already_in: str
    what: str
    cost: str


@dataclass
class ScanState:
    last_scan_date: Optional[str]
    course_high_water: Optional[str]
    repos: dict[str, RepoState] = field(default_factory=dict)
    carried_candidates: list[CarriedCandidate] = field(default_factory=list)
    #: The next `C-<n>` suffix this scan may assign to a genuinely new candidate. Kept
    #: monotonic across scans so a repeat run never reuses an id a prior scan already emitted.
    next_candidate_seq: int = 1

    @classmethod
    def load(cls, path: Path) -> "ScanState":
        if not path.exists():
            raise ScanError(
                f"no state file at {path} -- seed one (last_scan_date, course_high_water, "
                f"repos, carried_candidates, next_candidate_seq) before the first scan"
            )
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise ScanError(f"state file at {path} is not valid YAML: {exc}") from exc
        repos = {
            name: RepoState(since=str(block.get("since", "")))
            for name, block in (raw.get("repos") or {}).items()
        }
        carried = [
            CarriedCandidate(
                id=str(c["id"]), already_in=str(c["already_in"]), what=str(c["what"]),
                cost=str(c["cost"]),
            )
            for c in raw.get("carried_candidates") or []
        ]
        return cls(
            last_scan_date=raw.get("last_scan_date"),
            course_high_water=raw.get("course_high_water"),
            repos=repos,
            carried_candidates=carried,
            next_candidate_seq=int(raw.get("next_candidate_seq", 1)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "last_scan_date": self.last_scan_date,
            "course_high_water": self.course_high_water,
            "repos": {name: {"since": r.since} for name, r in self.repos.items()},
            "carried_candidates": [
                {"id": c.id, "already_in": c.already_in, "what": c.what, "cost": c.cost}
                for c in self.carried_candidates
            ],
            "next_candidate_seq": self.next_candidate_seq,
        }

    #: Written back on every save, ahead of the data -- the file is machine-rewritten each
    #: scan, so a header baked into the data (rather than typed once by a human) is the only
    #: kind that survives a re-run.
    HEADER = (
        "# ecosystem/aj-scan-state.yaml -- scripts/aj_scan.py's own state: the last recorded\n"
        "# scan (course high-water mark, per-repo commit high-water marks, carried candidate\n"
        "# rows not yet filed). Rewritten by every `aj_scan.py scan` run; do not hand-edit\n"
        "# except to remove a candidate once its row is filed. No operator-disk path lives\n"
        "# here -- the course directory is always a CLI argument (ruling (a), LANE-5B2-15).\n"
    )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        body = yaml.safe_dump(self.to_dict(), sort_keys=False, allow_unicode=True)
        path.write_text(self.HEADER + body, encoding="utf-8")


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# --- course delta ----------------------------------------------------------------------------


def scan_course(course_dir: Path, since: Optional[datetime]) -> list[Path]:
    """Files under `course_dir` with an mtime after `since` (or every file, if `since` is
    None). A plain walk -- detecting a new file needs no delegated read; DESCRIBING one does
    (see `delegate_describe`)."""
    if not course_dir.is_dir():
        raise ScanError(f"course dir not found: {course_dir}")
    newer: list[Path] = []
    for path in sorted(course_dir.rglob("*")):
        if not path.is_file():
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        if since is None or mtime > since:
            newer.append(path)
    return newer


# --- reference-repo delta ---------------------------------------------------------------------


def scan_repo_commits(
    repo: str,
    since_iso: str,
    *,
    repo_root: Optional[Path] = None,
    runner: Callable[..., Any] = subprocess.run,
) -> list[dict[str, Any]]:
    """`gh api repos/<repo>/commits?since=<since_iso>`, parsed. Empty state (`[]`) and "no
    commits" are the same fact and both return `[]`; only an unreadable `gh` result raises."""
    command = ["gh", "api", f"repos/{repo}/commits?since={since_iso}"]
    try:
        proc = runner(
            command, cwd=str(repo_root or _REPO_ROOT), capture_output=True, text=True,
            timeout=GH_TIMEOUT_S, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ScanError(f"gh could not be run for {repo}: {exc}") from exc
    if proc.returncode != 0:
        raise ScanError(
            f"gh api commits for {repo} exited {proc.returncode}: {proc.stderr.strip()[:200]}"
        )
    try:
        commits = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ScanError(f"gh returned unreadable JSON for {repo}: {exc}") from exc
    if not isinstance(commits, list):
        raise ScanError(
            f"gh api commits for {repo} did not return a list: {str(proc.stdout)[:200]}"
        )
    return commits


# --- the delegated large-read leg -------------------------------------------------------------


@dataclass(frozen=True)
class DelegateResult:
    response: str
    served_model: str


#: `agy` 1.2.x's JSON envelope carries no model id (measured in `scripts/provider_bench.py`'s
#: `AGY_ATTESTATION_NONE` and restated by this lane's own digest input, which read its served
#: model as "not disclosed"). Recording this string rather than guessing keeps the attestation
#: honest about what the CLI actually discloses today.
UNDISCLOSED_MODEL = "undisclosed"


def delegate_describe(
    prompt: str,
    *,
    cli: str = "agy",
    runner: Callable[..., Any] = subprocess.run,
) -> DelegateResult:
    """The large-read leg: hand a describe prompt to a subagent CLI rather than read course or
    diff content in-process. Mirrors `scripts/provider_bench.py`'s agy invocation
    (`--dangerously-skip-permissions` is required in print mode or every tool call soft-denies,
    per that module's measurement)."""
    argv = [
        cli, "--output-format", "json", "--print-timeout=10m",
        "--dangerously-skip-permissions", f"--print={prompt}",
    ]
    try:
        proc = runner(argv, capture_output=True, text=True, timeout=DELEGATE_TIMEOUT_S,
                       check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ScanError(f"{cli} could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise ScanError(f"{cli} exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ScanError(f"{cli} returned unreadable JSON: {exc}") from exc
    response = str(envelope.get("response") or "").strip()
    served_model = str(envelope.get("model") or UNDISCLOSED_MODEL)
    return DelegateResult(response=response or "(empty response)", served_model=served_model)


# --- candidate rows ----------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateRow:
    id: str
    already_in: str
    what: str
    cost: str
    served_model: Optional[str] = None


def _id_sort_key(row_id: str) -> tuple[int, int]:
    if row_id.startswith("C-") and row_id[2:].isdigit():
        return (0, int(row_id[2:]))
    return (1, 0)


def build_candidates(
    state: ScanState,
    course_new: Sequence[Path],
    repo_commits: dict[str, list[dict[str, Any]]],
    *,
    course_dir_label: str = "course delta",
    delegate: Callable[[str], DelegateResult] = delegate_describe,
) -> tuple[list[CandidateRow], ScanState]:
    """Union of the carried candidates with any genuinely new delta this scan found. Returns
    the rows (id order) and the state as it should be saved -- callers decide whether to."""
    rows: list[CandidateRow] = [
        CandidateRow(id=c.id, already_in=c.already_in, what=c.what, cost=c.cost)
        for c in state.carried_candidates
    ]
    next_seq = state.next_candidate_seq
    new_carried = list(state.carried_candidates)

    if course_new:
        names = ", ".join(str(p.name) for p in course_new)
        prompt = (
            f"Course files changed since the last scan ({course_dir_label}): {names}. "
            "In one sentence, what would this change in the harness?"
        )
        result = delegate(prompt)
        new_id = f"C-{next_seq}"
        row = CandidateRow(
            id=new_id, already_in=f"{course_dir_label} ({len(course_new)} file(s)): {names}",
            what=result.response, cost="S -- one scoped read (delegated)",
            served_model=result.served_model,
        )
        rows.append(row)
        new_carried.append(CarriedCandidate(id=row.id, already_in=row.already_in, what=row.what,
                                             cost=row.cost))
        next_seq += 1

    for repo, commits in repo_commits.items():
        if not commits:
            continue
        shas = ", ".join(str(c.get("sha", ""))[:9] for c in commits)
        new_id = f"C-{next_seq}"
        row = CandidateRow(
            id=new_id, already_in=f"{repo} {shas}", what="unknown until the diff is read",
            cost="S -- one scoped diff read (delegated), ~15 min",
        )
        rows.append(row)
        new_carried.append(CarriedCandidate(id=row.id, already_in=row.already_in, what=row.what,
                                             cost=row.cost))
        next_seq += 1

    rows.sort(key=lambda r: _id_sort_key(r.id))

    new_state = ScanState(
        last_scan_date=state.last_scan_date, course_high_water=state.course_high_water,
        repos=dict(state.repos), carried_candidates=new_carried, next_candidate_seq=next_seq,
    )
    return rows, new_state


# --- orchestration -------------------------------------------------------------------------


@dataclass(frozen=True)
class ScanResult:
    rows: list[CandidateRow]
    state: ScanState
    course_new: list[Path]
    repo_commits: dict[str, list[dict[str, Any]]]


def run_scan(
    *,
    course_dir: Path,
    repos: Sequence[str],
    state: ScanState,
    scan_date: Optional[str] = None,
    course_scanner: Callable[[Path, Optional[datetime]], list[Path]] = scan_course,
    commit_scanner: Callable[..., list[dict[str, Any]]] = scan_repo_commits,
    delegate: Callable[[str], DelegateResult] = delegate_describe,
) -> ScanResult:
    """Run the whole scan: course delta, every repo's commit delta, the candidate union, and
    the new state (new high-water marks, unchanged carried set, any newly-assigned ids)."""
    since = _parse_iso(state.course_high_water)
    course_new = course_scanner(course_dir, since)

    repo_commits: dict[str, list[dict[str, Any]]] = {}
    for repo in repos:
        # An unseen repo has no recorded high-water mark of its own -- scan it from the epoch
        # rather than silently reusing the course mark, which would under-report a repo this
        # state has never tracked.
        repo_since = state.repos.get(repo, RepoState(since="1970-01-01T00:00:00Z")).since
        repo_commits[repo] = commit_scanner(repo, repo_since)

    rows, next_state = build_candidates(state, course_new, repo_commits, delegate=delegate)

    # `scan_date` is the ISO timestamp this run treats as "now" -- it stamps every repo's new
    # high-water mark and, sliced to its first 10 characters, `last_scan_date`. Tests pin it;
    # a live run leaves it unset and gets the wall clock.
    now_iso = scan_date or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_course_high_water = state.course_high_water
    if course_new:
        newest = max(p.stat().st_mtime for p in course_new)
        new_course_high_water = datetime.fromtimestamp(newest, tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    elif since is None:
        new_course_high_water = now_iso

    new_repos = dict(next_state.repos)
    for repo in repos:
        new_repos[repo] = RepoState(since=now_iso)

    final_state = ScanState(
        last_scan_date=now_iso[:10],
        course_high_water=new_course_high_water,
        repos=new_repos,
        carried_candidates=next_state.carried_candidates,
        next_candidate_seq=next_state.next_candidate_seq,
    )
    return ScanResult(rows=rows, state=final_state, course_new=course_new,
                       repo_commits=repo_commits)


def render_table(rows: Sequence[CandidateRow]) -> str:
    header = "| id | already in | what it would change | cost / time | served model |"
    sep = "|---|---|---|---|---|"
    lines = [header, sep]
    for row in rows:
        lines.append(
            f"| {row.id} | {row.already_in} | {row.what} | {row.cost} | "
            f"{row.served_model or '(carried)'} |"
        )
    return "\n".join(lines)


# --- CLI -------------------------------------------------------------------------------------


@click.group(help=__doc__.split("\n\n")[0] if __doc__ else None)
def cli() -> None:
    """Entry point. One subcommand: `scan`."""


@cli.command("scan")
@click.option("--course", "course_dir", required=True, type=click.Path(path_type=Path),
              help="The course folder to scan. Never written into the state file (portability).")
@click.option("--repos", required=True,
              help="Comma-separated owner/name list of reference repositories.")
@click.option("--since-state", "state_path", default=DEFAULT_STATE_RELPATH,
              type=click.Path(path_type=Path),
              help=f"The state file (default {DEFAULT_STATE_RELPATH}).")
@click.option("--json", "as_json", is_flag=True, help="Emit the candidate rows as JSON.")
@click.option("--dry-run", is_flag=True, help="Do not write the state file back.")
def scan_cmd(course_dir: Path, repos: str, state_path: Path, as_json: bool,
             dry_run: bool) -> None:
    """List course files and reference-repo commits newer than the state's high-water mark,
    emit candidate rows (carried + new), and record the new high-water mark."""
    repo_list = [r.strip() for r in repos.split(",") if r.strip()]
    state = ScanState.load(state_path)
    result = run_scan(course_dir=course_dir, repos=repo_list, state=state)

    if as_json:
        payload = {
            "rows": [row.__dict__ for row in result.rows],
            "course_new": [str(p) for p in result.course_new],
            "repo_commits": {k: len(v) for k, v in result.repo_commits.items()},
        }
        click.echo(json.dumps(payload, indent=2))
    else:
        click.echo(render_table(result.rows))
        click.echo(f"\ncourse delta: {len(result.course_new)} file(s)")
        for repo, commits in result.repo_commits.items():
            click.echo(f"{repo}: {len(commits)} commit(s) since {state.repos.get(repo, RepoState(since='(none)')).since}")

    if not dry_run:
        result.state.save(state_path)
        logger.info("state written to %s (course_high_water=%s)", state_path,
                    result.state.course_high_water)


if __name__ == "__main__":
    cli()
