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
     file;
  4. **no GO artifact names this lane on `main` ([#685]).** The operator GO was a spoken
     ceremony, leaving no artifact an auditor could read back from the tree -- a dispatched lane
     looked identical to one that dispatched itself. The fix names the GO in the one place it
     already lands in this repo's live protocol: a table row in the OPEN batch's manifest, or one
     of its `<manifest-stem>-amendment-N.md` siblings (`docs/audits/2026-09-16-technical-batch-ab-
     manifest-amendment-1.md` is the live instance -- its lane table carries a `State` cell
     reading `fire now` / `FIRED ...` / `HELD: ...` per row). A row naming this lane with a HELD
     state, or no row at all, refuses. Amendments are read in numeric order and a later one's row
     wins, because an amendment supersedes the manifest it amends. This is deliberately narrower
     than `[#685]`'s prose, which also names a `RATIFICATION-<date>.md` on the operator's own
     transport -- that half needs `CLAUDE_PROMPTS_DIR` resolved to an operator-disk directory this
     module cannot see from a hermetic test, so it is left as a documented gap rather than built
     untested (`check_go_artifact`'s own docstring repeats this limit);
  5. ANOTHER session already owns this lane and is `live` (`seat_refusals.refuse_lane_owned`,
     `[#833]`) -- on 2026-09-17 a second session was dispatched onto lane ab-833 and found its live
     owner only by reading staged files and scanning processes;
  6. the batch has no `live` integrator seat (`seat_refusals.refuse_no_live_integrator`, `[#833]`)
     -- a lane that boots now hands back to nobody.

  Refusals 5 and 6 read `seat_registry.seats()`, whose `state` is written by hook events and never
  by a model. They run AFTER the manifest and GO refusals: a lane with no open batch has no batch whose
  integrator could be asked about.

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

import os
import re
import subprocess
import sys
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

from batch_manifest import open_batches  # noqa: E402
from preflight_contract import check_open_batch  # noqa: E402
from seat_refusals import SeatRefusal, refuse_lane_owned, refuse_no_live_integrator  # noqa: E402
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


def seat_preflight(lane: str, seats: list, *, own_session: str) -> str:
    """Refusals 4 and 5 over the seat registry (`[#833]`). Return the OK line, or exit 1."""
    batch = lane.split("-")[1].upper()
    try:
        refuse_lane_owned(lane, seats, own_session=own_session)
        integrator = refuse_no_live_integrator(batch, seats)
    except SeatRefusal as exc:
        _refuse(str(exc))
    return (f"OK   seats: batch {batch} is received by integrator {integrator.session_id}; "
            f"no other live session holds {lane}")


def _read_ref(repo: Path, ref: str, rel: str) -> str | None:
    """Committed content of `rel` at `ref`, or `None` if it does not exist there."""
    proc = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{rel}"],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=30)
    return proc.stdout if proc.returncode == 0 else None


_AMENDMENT_RE_TMPL = r"^{dir}/{stem}-amendment-(\d+)\.md$"


def _committed_amendment_paths(repo: Path, ref: str, manifest_rel: str) -> list[str]:
    """Sibling `<manifest-stem>-amendment-N.md` paths committed at `ref`, numeric order.

    An amendment does not match `batch_manifest.MANIFEST_GLOB` on purpose (it "declares no
    second batch") -- so it never surfaces through `open_batches()` and has to be found beside
    the manifest it amends instead.
    """
    directory = str(Path(manifest_rel).parent).replace("\\", "/")
    stem = Path(manifest_rel).stem
    proc = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", ref, "--",
                           directory], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=30)
    if proc.returncode != 0:
        return []
    pattern = re.compile(_AMENDMENT_RE_TMPL.format(dir=re.escape(directory),
                                                    stem=re.escape(stem)))
    hits: list[tuple[int, str]] = []
    for line in proc.stdout.splitlines():
        rel = line.replace("\\", "/")
        m = pattern.match(rel)
        if m:
            hits.append((int(m.group(1)), rel))
    return [p for _, p in sorted(hits)]


def _go_row_for_lane(lane: str, texts: list[str]) -> str | None:
    """The LAST markdown table-row line naming `lane`, across `texts` in order.

    `None` means no artifact ever named this lane. Later texts win over earlier ones on
    purpose: an amendment row supersedes the manifest row it amends, the same rule
    `batch_manifest` and the amendment file itself both state in prose.
    """
    row = None
    for text in texts:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and lane in line:
                row = line
    return row


def check_go_artifact(repo: Path, lane: str, batches: list, main_ref: str = "main") -> None:
    """`[#685]`: refuse a lane no GO artifact names, on `main`.

    Reads each open batch's manifest plus its committed amendment siblings, in numeric order,
    for a table row naming `lane`. No row at all, or a row whose state reads `HELD`, refuses.
    Never falls back to a `RATIFICATION-<date>.md` on the operator's transport -- see the
    module docstring's honest limit on that half.
    """
    for batch in batches:
        manifest_text = _read_ref(repo, main_ref, batch.path)
        if manifest_text is None:
            continue
        amendments = [_read_ref(repo, main_ref, p)
                     for p in _committed_amendment_paths(repo, main_ref, batch.path)]
        row = _go_row_for_lane(lane, [manifest_text, *[a for a in amendments if a is not None]])
        if row is None:
            continue
        if "HELD" in row.upper():
            _refuse(f"{lane} is HELD in {batch.path} (or an amendment): {row.strip()} "
                    f"([#685] -- the GO artifact must authorize this lane, not hold it)")
        return  # a non-HELD row naming this lane is the GO
    named = ", ".join(b.path for b in batches)
    _refuse(f"no GO artifact names {lane} in {named} or a `<manifest-stem>-amendment-N.md` "
            f"sibling on {main_ref} ([#685] -- the operator GO must be a file `/lane-boot` "
            f"reads, not a spoken ceremony)")


def preflight(lane: str, repo: Path, main_ref: str = "main", *,
              registry: Path | None = None) -> str:
    """Run the six refusals. Return the OK lines, or exit through `_refuse`."""
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

    check_go_artifact(repo, lane, open_on_main, main_ref)

    names = ", ".join(f"{b.path} (batch {b.batch})" for b in open_on_main)
    import seat_registry  # noqa: PLC0415 -- lazy: only a lane past the manifest refusals reads it
    seat_line = seat_preflight(lane, seat_registry.seats(registry),
                               own_session=os.environ.get("CLAUDE_CODE_SESSION_ID", ""))
    return f"OK   {lane} -> branch worktree-{lane}; open on {main_ref}: {names}\n{seat_line}"


@click.group(help="/lane-boot's pre-flight, as one command whose refusals block ([#804]).")
def cli() -> None:
    pass


@cli.command("preflight")
@click.option("--lane", required=True, help="the lane WORKTREE name, lane-<batch>-<id>-<slug>")
@click.option("--repo", default=".", type=click.Path(file_okay=False, path_type=Path),
              show_default=True, help="the primary checkout the lane dispatches from")
@click.option("--main-ref", default="main", show_default=True,
              help="the ref a manifest must be committed on")
@click.option("--registry", default=None, type=click.Path(dir_okay=False, path_type=Path),
              help="the seat registry to read (default: seat_registry.REGISTRY_PATH)")
def cmd_preflight(lane: str, repo: Path, main_ref: str, registry: Path | None) -> None:
    """Refuse to boot a lane without an open batch on main or a live integrator, or onto a lane
    another live session already owns. Exit 0/1/2."""
    try:
        click.echo(preflight(lane, repo, main_ref, registry=registry))
    except click.ClickException as exc:
        click.echo(f"LANE-BOOT INTERNAL ERROR: {exc.format_message()} -- refusing to report "
                   f"clean", err=True)
        sys.exit(INTERNAL_ERROR)


if __name__ == "__main__":
    cli()
