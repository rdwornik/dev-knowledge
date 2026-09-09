"""gen_ledger.py -- the operator's read surface, GENERATED from repo state.

WHY THIS IS GENERATED. `to-browser/LEDGER-<repo>.md` is the one file the operator opens to ask
"where is this repo, what is stuck, what is next". Every version of it so far was hand-written by
a browser seat, and each one carried the seat's own provenance disclaimer explaining which
numbers it had actually witnessed and which it had transcribed from a packet. That disclaimer is
the tell: a read surface whose author has to say which of its facts are second-hand is a surface
whose facts go stale between windows, silently, in the direction of "still true when written".
This repo already refuses that everywhere else -- never restate a count or roster in prose, cite
the surface that computes it -- and the LEDGER was the largest remaining exception.

READS, NEVER WRITES. This generator's only write is the ledger file itself. It runs `git` in
read-only forms (`rev-parse`, `ls-remote`, `worktree list`, `branch`, `tag`, `log`) and reads
`tasks/` through the organs that already own it. It regenerates no index, touches no state file,
and commits nothing -- the lane contract that commissioned it says so in terms, and
`tests/test_gen_ledger.py` asserts a render leaves `git status` byte-identical.

WHAT IS DERIVED vs WHAT IS DECLARED:
  * DERIVED (everything a reader would otherwise have to trust): the SHAs, the worktree list, the
    branch and tag rosters, the open-batch set, the open-row count, the blocked set and its
    reasons, and the proposed next batch. All of it read at render time.
  * DECLARED: the three section names and their order -- STATE, BLOCKED BY, NEXT -- which are the
    lane contract's own grammar, and the sentence under each saying what it is measuring.

THE PROPOSAL IS NOT A DISPATCH. The NEXT section is `boot_frontier.propose_batch`, and that
module's own contract is explicit that adjudication stays a human act. The rendered section says
so on its own line rather than leaving a reader to infer it from a heading.

OUTPUT SHAPE. Flat -- `key: value` lines and bullets, no column-padded tables. The LEDGER is
pasted into a browser chat and re-billed on every turn of that window, and a padded markdown
table costs roughly three times its content in tokens for a border the reader's client draws
anyway (PLAYBOOK §8, "Output the operator copies into browser chat").

HONEST LIMITS, stated because a generated surface reads as more authoritative than a hand-written
one and therefore owes a clearer account of what it does not know:
  * It runs NO gate and NO suite. There is no ship-gate verdict, no test count and no WARN
    census here, because producing one would mean running it, and this generator is read-only by
    contract. A reader wanting those numbers runs `audit.py health` and owns the result.
  * `origin/main` is read with `git ls-remote`, which is a network call. When it fails the row
    says UNREACHABLE rather than falling back to the cached `origin/main` ref -- a cached ref is
    a fact about the last fetch, not about the remote, and the two look identical.
  * The BLOCKED set is `depends-on` blockage among OPEN rows. A row blocked by something that is
    not a row -- an unlanded ruling, an operator act, a vendor outage -- is invisible to it, and
    that is the majority of what actually blocks this repo.
"""
from __future__ import annotations

import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import boot_frontier as _bf
    import gen_handoff as _gh
    import gen_task_tree as _gtt
except ImportError:                                  # imported as `scripts.gen_ledger`
    from scripts import boot_frontier as _bf         # type: ignore[no-redef]
    from scripts import gen_handoff as _gh           # type: ignore[no-redef]
    from scripts import gen_task_tree as _gtt        # type: ignore[no-redef]

_REPO_ROOT = _SCRIPTS.parent

#: The transport filename grammar (OPERATOR-INTERFACE §1): `LEDGER-<repo>.md`, in `to-browser/`.
#: The leading dot of `.dev-knowledge` is stripped, matching `gen_handoff._row_ledger_refreshed`
#: -- the freshness row that READS this file, so the two agree on where it lives by construction.
def out_relpath(repo_name: str) -> str:
    return f"to-browser/LEDGER-{repo_name.lstrip('.')}.md"


#: How many proposed rows the NEXT section renders. `boot_frontier`'s own ledger bound, reused.
NEXT_BOUND = _bf.LEDGER_BOUND
#: How many held-back ids are sampled before the line says "and N more". The COUNT is the fact a
#: reader acts on; the roster is `boot_frontier`'s and is one command away.
HELD_BACK_SHOWN = 8

_UNKNOWN = "UNAVAILABLE"


def _git(repo_root: Path, *args: str) -> str:
    """One read-only git read. Returns `_UNKNOWN` rather than raising -- a ledger that refuses to
    render because one probe failed is less useful than one that says which probe failed."""
    try:
        done = subprocess.run(["git", "-C", str(repo_root), *args],
                              capture_output=True, text=True, check=False)
    except OSError:
        return _UNKNOWN
    return done.stdout.strip() if done.returncode == 0 else _UNKNOWN


def _origin_main(repo_root: Path, *, offline: bool = False) -> str:
    """`origin/main` read from the REMOTE, not from the cached ref.

    `git ls-remote` asks the server; `git rev-parse origin/main` reports whatever the last fetch
    left behind. The two are indistinguishable in the output and differ exactly when it matters.
    """
    if offline:
        return "not read (offline)"
    out = _git(repo_root, "ls-remote", "origin", "refs/heads/main")
    if out == _UNKNOWN or not out:
        return "UNREACHABLE -- ls-remote failed; NOT falling back to the cached ref"
    return out.split()[0]


def _worktrees(repo_root: Path) -> list[str]:
    out = _git(repo_root, "worktree", "list", "--porcelain")
    if out == _UNKNOWN:
        return []
    return [line.split(" ", 1)[1].strip() for line in out.splitlines()
            if line.startswith("worktree ")]


#: JOURNAL entries are `### <date> (<letter>) - ...`. Matched as a PATTERN rather than by
#: heading depth: the file's `# Journal` title is depth 1 and its entries are depth 3, so a
#: "first `##`" read returns nothing at all and renders as UNAVAILABLE while the file is fine.
_JOURNAL_ENTRY_RE = re.compile(r"^#{2,4}\s+(\d{4}-\d{2}-\d{2}\b.*)$")


def _journal_head(repo_root: Path) -> str:
    """The newest JOURNAL entry's heading -- `JOURNAL.md` is append-only NEWEST-FIRST."""
    path = repo_root / "JOURNAL.md"
    if not path.exists():
        return _UNKNOWN
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _JOURNAL_ENTRY_RE.match(line)
        if m:
            return m.group(1).strip()
    return _UNKNOWN


def _open_batches(repo_root: Path) -> list:
    """Committed manifests declaring a batch open right now, via the shared reader."""
    try:
        from batch_manifest import open_batches  # noqa: PLC0415
    except ImportError:                          # pragma: no cover -- reader unavailable
        return []
    try:
        return list(open_batches(repo_root))
    except Exception:                            # noqa: BLE001 -- an unknown state is no batch
        return []


def _row_label(row) -> str:
    return f"[#{row.id}] {_gtt.derive_priority(row.raw) or 'P?'} - {_gtt.derive_title(row.raw)}"


def collect(repo_root: Path | None = None, *, offline: bool = False) -> dict:
    """Every fact the ledger renders, read in one pass. Pure read -- writes nothing."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    try:
        rows = _bf.load_open_rows(root)
        frontier = _bf.unblocked_frontier(rows)
        proposal = _bf.select_batch(_bf.score_frontier(frontier, rows),
                                    ledger_bound=NEXT_BOUND)
        queue_error = None
    except Exception as exc:                     # noqa: BLE001 -- a cyclic or unreadable queue
        rows, frontier, proposal, queue_error = [], [], None, str(exc)
    unblocked_ids = {row.id for row in frontier}
    open_ids = {row.id for row in rows}
    blocked = []
    for row in rows:
        if row.id in unblocked_ids:
            continue
        waiting = sorted(_bf.depends_on_ids(row.raw) & open_ids)
        blocked.append((row, waiting))
    return {
        "repo_root": root,
        "main": _git(root, "rev-parse", "main"),
        "head": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
        "origin_main": _origin_main(root, offline=offline),
        "status": _git(root, "status", "--porcelain"),
        "worktrees": _worktrees(root),
        "branches": _git(root, "branch", "--format=%(refname:short)"),
        "newest_tag": _git(root, "describe", "--tags", "--abbrev=0"),
        "journal_head": _journal_head(root),
        "open_batches": _open_batches(root),
        "open_rows": rows,
        "blocked": blocked,
        "proposal": proposal,
        "queue_error": queue_error,
    }


def render(state: dict, *, date: str, repo_name: str = ".dev-knowledge") -> str:
    """The ledger text. Flat by design -- no padded tables; this file is pasted into a chat."""
    root = state["repo_root"]
    lines: list[str] = [
        f"# LEDGER - {repo_name.lstrip('.')} - the operator's read surface",
        "",
        f"<!-- GENERATED by scripts/gen_ledger.py from repo state; refreshed {date}.",
        "     Do not hand-edit: the next run overwrites it, and a hand-edited row is a claim",
        "     with no surface behind it. Every fact below was read at generation time from git",
        "     and from `tasks/`; NO gate and NO suite was run, so there is no ship-gate verdict,",
        "     test count or WARN census here. Read-only: this generator's one write is this",
        "     file. -->",
        "",
        "## STATE - read from git and `tasks/` at generation time",
        "",
        f"- main: {state['main']}",
        f"- origin/main: {state['origin_main']}",
        f"- generated from: {root} (HEAD {state['head']})",
        f"- working tree: {'clean' if state['status'] == '' else 'DIRTY'}"
        + (f" - {len(state['status'].splitlines())} path(s)" if state["status"] else ""),
        f"- newest tag: {state['newest_tag']}",
        # `git worktree list` puts the PRIMARY first, so the tail is the lane trees. Counted as
        # "primary + N" rather than a bare N: a reader asking "how many lanes are live" and a
        # reader asking "how many trees exist" get different numbers out of the same word.
        f"- worktrees: primary + {max(len(state['worktrees']) - 1, 0)} "
        + ("(primary only)" if len(state["worktrees"]) <= 1
           else "- " + ", ".join(Path(w).name for w in state["worktrees"][1:])),
        f"- branches: {len(state['branches'].splitlines()) if state['branches'] != _UNKNOWN else 0}"
        + (f" - {', '.join(state['branches'].split())}" if state["branches"] != _UNKNOWN else ""),
        f"- newest JOURNAL entry: {state['journal_head']}",
        f"- open rows: {len(state['open_rows'])}",
    ]
    if state["open_batches"]:
        for batch in state["open_batches"]:
            lines.append(
                f"- OPEN BATCH `{batch.batch}`: {batch.path} - the ADR-110 integration-arc "
                f"exemption is LIVE until `{batch.closed_by}` lands"
            )
    else:
        lines.append("- open batches: none - no integration-arc exemption is live")

    lines += [
        "",
        "## BLOCKED BY - open rows waiting on another OPEN row, and what each waits for",
        "",
        "Blockage here is `depends-on` among open rows and nothing else. A row held by an "
        "unlanded ruling, an operator act or a vendor is invisible to this section, and that is "
        "most of what actually blocks this repo.",
        "",
    ]
    if state["queue_error"]:
        lines.append(f"- the queue could not be read: {state['queue_error']}")
    elif not state["blocked"]:
        lines.append("- nothing - every open row is on the unblocked frontier")
    else:
        for row, waiting in state["blocked"]:
            names = ", ".join(f"#{i}" for i in waiting) or "a row outside the open set"
            lines.append(f"- {_row_label(row)} - waits on {names}")

    lines += [
        "",
        "## NEXT - the unblocked frontier, scored and bounded. A PROPOSAL, not a dispatch",
        "",
        "Nothing below is booted by this file. Every lane needs an explicit operator GO, and the "
        f"set is capped at {NEXT_BOUND} rows by the never-endless bound rather than by how much "
        "unblocked work exists.",
        "",
    ]
    proposal = state["proposal"]
    if proposal is None:
        lines.append("- unavailable - the queue could not be read")
    elif not proposal.selected:
        lines.append("- nothing unblocked and eligible - no batch to propose")
    else:
        for row in proposal.selected:
            lines.append(f"- {_row_label(row)}")
        if proposal.held_back_disjointness:
            # COUNT FIRST, then a bounded sample. The live figure is ~60 ids; a full roster
            # would be the longest line in the file and would tell a reader nothing the count
            # does not. The count is the fact; `boot_frontier` holds the roster.
            held = proposal.held_back_disjointness
            shown = ", ".join(f"#{r.id}" for r in held[:HELD_BACK_SHOWN])
            more = f", and {len(held) - HELD_BACK_SHOWN} more" if len(held) > HELD_BACK_SHOWN \
                else ""
            lines.append(f"- held back by serialize-group disjointness: {len(held)} row(s) - "
                         f"{shown}{more} (full roster: `boot_frontier.py`)")
        if proposal.truncated_by_ledger:
            lines.append("- more unblocked work exists beyond the bound - not endless by design")
    return "\n".join(lines).rstrip() + "\n"


def default_out(repo_root: Path, repo_name: str) -> "Path | None":
    """The transport home for this repo's ledger, or None when no transport is resolvable."""
    transport = _gh.transport_root()
    return Path(transport) / out_relpath(repo_name) if transport else None


@click.command(help="Generate the operator's LEDGER read surface from repo state (read-only).")
@click.option("--out", "out_path", type=click.Path(dir_okay=False), default=None,
              help="where to write; defaults to the transport's to-browser/LEDGER-<repo>.md")
@click.option("--repo-root", type=click.Path(exists=True, file_okay=False), default=None)
@click.option("--repo-name", default=".dev-knowledge", show_default=True)
@click.option("--date", default=None, help="the window date; defaults to today")
@click.option("--offline", is_flag=True, help="skip the ls-remote read of origin/main")
@click.option("--dry-run", is_flag=True, help="print to stdout and write nothing")
def cli(out_path: "str | None", repo_root: "str | None", repo_name: str,
        date: "str | None", offline: bool, dry_run: bool) -> None:
    root = Path(repo_root) if repo_root else _REPO_ROOT
    when = date or _dt.date.today().isoformat()
    text = render(collect(root, offline=offline), date=when, repo_name=repo_name)
    if dry_run:
        click.echo(text)
        return
    target = Path(out_path) if out_path else default_out(root, repo_name)
    if target is None:
        click.echo("gen_ledger: no transport resolvable and no --out given; nothing written",
                   err=True)
        raise SystemExit(1)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    click.echo(f"{target} ({len(text.encode('utf-8'))} B, refreshed {when})")


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
