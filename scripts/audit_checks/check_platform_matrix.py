"""`check_platform_matrix` — the consumer platform-matrix floor (D7 consumers, row L9).

WHY THIS EXISTS. `to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` D7:
"the deploy manifest ships a consumer CI template with the same OS matrix and a floor check
that the consumer declares its supported platforms and runs CI on each; a consumer is
compliant when its matrix is present and green-or-ratcheted." Ratified R11
(RATIFICATION-2026-09-25 v9, superseded by v10/.../v14 unchanged). In-repo home:
`docs/decisions/ADR-127-ci-os-verification.md`, `protocols/STANDING_RULINGS.md` §AN.

WHAT IT CHECKS. Every `.github/workflows/*.yml` / `*.yaml` in `repo_path`, parsed as YAML, for
at least one job whose `strategy.matrix.os` is a non-empty list — the shape
`templates/consumer-ci-matrix.yml` ships and the hub's own `.github/workflows/conductor.yml`
already carries (`strategy: matrix: os: [ubuntu-latest, windows-latest]`, job `pytest`).
Presence only — this is the FLOOR ("declares its supported platforms"), not a richness or
green-ness check; D7's own words are "compliant when its matrix is present and
green-or-ratcheted", and green-or-ratcheted is D2's job (`scripts/known_reds.py`), not this
one's.

HONEST LIMITS.
  * A YAML file that fails to parse is reported as its own `fail` Finding, never silently
    skipped — a consumer whose only workflow is broken has not declared anything either.
  * The check reads only `.github/workflows/*.yml`/`*.yaml`; a matrix declared anywhere else
    (a Makefile, a tox.ini, a README) is invisible to it — GitHub Actions is what D1 makes the
    verification verdict, so that is where D7 asks the declaration to live.
  * A single-OS matrix (e.g. `os: [ubuntu-latest]`) satisfies the floor: a consumer that
    deliberately supports one platform has still DECLARED it, which is what D7 asks for. This
    check does not judge whether the declared set is the RIGHT one.
  * The job name is not fixed — every job under `jobs:` is searched, because a consumer may
    not call its matrix job `pytest` the way the hub does.

Child-repo-safe by construction, and deliberately carries no `n/a` leg: D7 makes the
declaration itself the requirement, not a pre-existing surface a repo might legitimately lack,
so a repo with no `.github/workflows/` directory at all is exactly the FAIL case this check
exists to report — the Done-when's own words ("a consumer without a declared platform matrix
reports FAIL").
Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ._common import Finding

CHECK_NAME = "platform_matrix"
WORKFLOWS_RELPATH = ".github/workflows"


def _matrix_os_lists(doc: object) -> list[list[object]]:
    """Every non-empty `strategy.matrix.os` list in a parsed workflow document, one per job
    that declares one. Searches every job under `jobs:` rather than a fixed job name."""
    out: list[list[object]] = []
    if not isinstance(doc, dict):
        return out
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        return out
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        strategy = job.get("strategy")
        if not isinstance(strategy, dict):
            continue
        matrix = strategy.get("matrix")
        if not isinstance(matrix, dict):
            continue
        os_list = matrix.get("os")
        if isinstance(os_list, list) and os_list:
            out.append(os_list)
    return out


def check_platform_matrix(repo_path: Path) -> list[Finding]:
    """D7 consumer floor: `repo_path` declares a platform matrix, or it FAILs.

    Per-file YAML/read failures are their own `fail` Finding, never folded silently into "no
    matrix found" — an unreadable workflow has proven nothing either way. A `pass` summary is
    added whenever at least one matrix was found ANYWHERE, even beside a broken sibling file;
    the generic "no matrix declared" `fail` is added only when nothing else has already
    explained the absence.
    """
    root = Path(repo_path)
    workflows_dir = root / WORKFLOWS_RELPATH
    out: list[Finding] = []
    declared: list[str] = []

    if workflows_dir.is_dir():
        paths = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
        for path in paths:
            rel = path.relative_to(root).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                out.append(Finding(CHECK_NAME, "fail",
                                   f"{rel} could not be read: {exc!r}".replace("|", "/")))
                continue
            try:
                doc = yaml.safe_load(text)
            except yaml.YAMLError as exc:
                out.append(Finding(CHECK_NAME, "fail",
                                   f"{rel} is not valid YAML, so its platform matrix (if any) "
                                   f"could not be read: {exc}".replace("|", "/")))
                continue
            for os_list in _matrix_os_lists(doc):
                declared.append(f"{rel}: {os_list!r}")

    if declared:
        out.append(Finding(CHECK_NAME, "pass",
                           f"{len(declared)} declared platform matrix/matrices under "
                           f"{WORKFLOWS_RELPATH}/: {'; '.join(declared)}"))
    elif not out:
        out.append(Finding(CHECK_NAME, "fail",
                           f"no job in {WORKFLOWS_RELPATH}/*.yml declares a "
                           f"`strategy.matrix.os` list — this repo has not declared its "
                           f"supported platforms (D7, protocols/STANDING_RULINGS.md §AN R11; "
                           f"start from templates/consumer-ci-matrix.yml)"))
    return out
