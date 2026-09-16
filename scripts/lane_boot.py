#!/usr/bin/env python
"""lane_boot.py -- `/lane-boot`'s pre-flight as ONE command, so its refusals are real ([#804]).

THE FALSE CLAIM THIS RETIRES. `protocols/PLAYBOOK.md` ("The manifest opens a batch by
`closed_by:`", RULED 2026-08-29, item 2) says: "`/lane-boot` and the `[#591]` pre-freeze validator
REFUSE to dispatch the first lane while `open_batches()` returns `[]`. The predicate is
`preflight_contract.check_open_batch`". No boot step called it. Its only caller was
`preflight_contract --freeze`, which a seat runs by hand or not at all. Batch AA dispatched six
lanes with no committed manifest, and the absence produced four task-id reallocations, two
quality-register collisions, a JOURNAL letter collision and an unarmed integration exemption.
Nothing noticed until merge.

WHAT `preflight` REFUSES (exit 1), in order, and the first refusal stops the run:

  1. a lane name outside the batch-lane grammar
     (`validate_branch_naming.validate_lane_worktree_name`);
  2. no committed manifest declaring an OPEN batch. This is `preflight_contract.check_open_batch`,
     called here rather than restated;
  3. an open manifest that is committed on THIS checkout but not on `main`, or whose `closed_by:`
     packet `main` already carries. `[#804]` Done-when (1) says "committed on `main` (not merely
     present in a worktree ...)". `open_batches` reads `HEAD`, so a manifest committed on a side
     branch opens the batch for that branch alone, and every lane that bases on `main` would boot
     outside it. That is `[#788]`'s visibility defect at batch scale, and the refusal names the
     file.

Exit 2 is an internal error (git unreadable). It never passes.

HONEST LIMITS
  * `/lane-boot` runs this. The `dispatch` verb does not yet. The verb lives in `win-tooling`
    (`scripts/dispatch/Invoke-Dispatch.ps1`, reached through `~/.dev-terminals/bin/dispatch.ps1`),
    outside this hub. It can call `lane_boot.py preflight` as its first act. Until it does, a seat
    that types `dispatch` WITHOUT `/lane-boot` is not refused. This is recorded in the lane ab-804
    audit as an out-of-footprint follow-up.
  * It checks that a batch is open, not that THIS lane is on its roster. Roster scoping is
    `[#510]`'s.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

from batch_manifest import open_batches  # noqa: E402
from preflight_contract import check_open_batch  # noqa: E402
from validate_branch_naming import validate_lane_worktree_name  # noqa: E402

OK = 0
REFUSED = 1
INTERNAL_ERROR = 2


def _on_ref(repo: Path, ref: str, rel: str) -> bool:
    """True iff `rel` exists in `ref`'s tree. Raises on anything but a clean yes or no."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{rel}"],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise click.ClickException(f"could not run git: {exc!r}") from exc
    if proc.returncode == 0:
        return True
    probe = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet",
                            f"{ref}^{{commit}}"], capture_output=True, text=True, timeout=30)
    if probe.returncode != 0:
        raise click.ClickException(f"{ref!r} does not resolve in {repo}; cannot tell whether "
                                   f"the batch is open there, and that is not a pass")
    return False


def _refuse(message: str) -> None:
    click.echo(f"LANE-BOOT REFUSAL: {message}", err=True)
    sys.exit(REFUSED)


def preflight(lane: str, repo: Path, main_ref: str = "main") -> str:
    """Run the three refusals. Return the OK line, or exit through `_refuse`."""
    reason = validate_lane_worktree_name(lane)
    if reason is not None:
        _refuse(reason)

    claims = check_open_batch(repo)
    failed = [c for c in claims if not c.ok]
    if failed:
        _refuse("; ".join(f"{c.raw}: {c.detail}" for c in failed))

    open_on_main, missing = [], []
    for batch in open_batches(repo):
        if _on_ref(repo, main_ref, batch.path) and not _on_ref(repo, main_ref, batch.closed_by):
            open_on_main.append(batch)
        else:
            missing.append(batch)
    if not open_on_main:
        named = ", ".join(f"{b.path} (batch {b.batch})" for b in missing)
        _refuse(f"{named} opens a batch on this checkout only. `{main_ref}` does not carry it "
                f"open, and every lane that bases on `{main_ref}` would boot outside the batch. "
                f"Merge the manifest to `{main_ref}` before the first lane boots ([#804]).")

    names = ", ".join(f"{b.path} (batch {b.batch})" for b in open_on_main)
    return f"OK   {lane} -> branch worktree-{lane}; open on {main_ref}: {names}"


@click.group(help="/lane-boot's pre-flight, as one command whose refusals block ([#804]).")
def cli() -> None:
    pass


@cli.command("preflight")
@click.option("--lane", required=True, help="the lane WORKTREE name, lane-<batch>-<id>-<slug>")
@click.option("--repo", default=".", type=click.Path(file_okay=False, path_type=Path),
              show_default=True, help="the primary checkout the lane dispatches from")
@click.option("--main-ref", default="main", show_default=True,
              help="the ref a manifest must be committed on")
def cmd_preflight(lane: str, repo: Path, main_ref: str) -> None:
    """Refuse to boot a lane without an open batch committed on main. Exit 0/1/2."""
    try:
        click.echo(preflight(lane, repo, main_ref))
    except click.ClickException as exc:
        click.echo(f"LANE-BOOT INTERNAL ERROR: {exc.format_message()} -- refusing to report "
                   f"clean", err=True)
        sys.exit(INTERNAL_ERROR)


if __name__ == "__main__":
    cli()
