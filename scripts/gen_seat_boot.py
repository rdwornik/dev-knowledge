"""gen_seat_boot.py -- render the five SEAT-BOOT pastes from PLAYBOOK Ch8, at bundle-cut time.

WHY THIS IS GENERATED AND NEVER COMPOSED. Two consecutive browser seats did not know how a
dispatcher / integrator / filings / handoff session is booted, composed a boot paste anyway, and
both were withdrawn (operator ruling INBOX-dev-knowledge-2026-09-08-038; AMEND-BATCH-V-001 §1).
The knowledge was already in the repo -- Ch8's batch protocol and dispatch table -- and never
reached the operator as a paste-ready form. A composed paste is a second copy of Ch8, free to
drift from it, and the drift is invisible: a boot that quotes a superseded ceiling reads exactly
like one that quotes the live one.

So: **Ch8 is the source, the render is the only path, and drift is a test failure.** The seat
template supplies STRUCTURE (which refusal at which step, where each Ch8 region lands); every
byte of doctrine is machine-extracted by `seat_ch8` at the moment of the cut; probe **P12**
re-extracts and byte-compares, so a Ch8 edit re-issues the pastes automatically and a bundle
carrying a stale one FAILS.

WHAT THIS MODULE REFUSES, and each is a way the guarantee dies quietly:

  * **A template whose `{{CH8:...}}` set disagrees with `seat_ch8.SEAT_BLOCKS`.** Either a
    declared block renders nowhere (doctrine that never reaches the seat) or the template asks
    for one the map does not give it. Both look fine in the output.
  * **A rendered artifact carrying `<PROMPTS_DIR>` or a typed path.** AMEND-BATCH-V-002 §3(b):
    every rendered boot resolves `CLAUDE_PROMPTS_DIR` from User scope itself -- no placeholder,
    no path typed by the operator, ever. The closure is N -> 0 with a render test that fails on
    either, and this is that test's enforcement half.
  * **An unresolved `{{TOKEN}}`.** A paste shipped with a live token is a paste the seat cannot
    run, and it ships looking complete.
  * **A rendered boot that fails the seat refusals it carries.** The boots are the first
    consumer of `seat_refusals`; a boot telling a seat to write its waits as code while stating
    its own as an intention would be the exact failure it is teaching against.

HONEST LIMIT. P12 proves a rendered file equals a fresh render of the CURRENT Ch8. It does not
prove Ch8 is right, and it does not prove the render reached anyone: a bundle carrying five
perfect SEAT-BOOT files that no seat opens is a green probe over an unread artifact. What closes
that leg is the incoming seat's first dispatch using one verbatim, which is INBOX 038's own
Done-when and is not a property any test in this repo can hold.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import seat_ch8
    import seat_refusals
except ImportError:                                  # imported as `scripts.gen_seat_boot`
    from scripts import seat_ch8, seat_refusals      # type: ignore[no-redef]

_REPO_ROOT = _SCRIPTS.parent

TMPL_RELPATH = "templates/handoff/seats"
TMPL_SUFFIX = ".md.tmpl"

#: The token a template uses to place one Ch8 region: `{{CH8:<key>}}`.
_CH8_TOKEN_RE = re.compile(r"\{\{CH8:(?P<key>[a-z0-9\-]+)\}\}")
#: Any token still live after substitution -- a paste that cannot be run, shipped looking whole.
_LEFTOVER_TOKEN_RE = re.compile(r"\{\{[A-Z0-9_:\-]+\}\}")
#: A leading `<!-- ... -->` authoring note, dropped at render exactly as `gen_handoff` drops one.
_LEADING_NOTE_RE = re.compile(r"\A<!--.*?-->\s*(?=#)", re.DOTALL)

#: AMEND-BATCH-V-002 §3(b) -- what a rendered boot may not carry. A Windows drive path, a POSIX
#: home path and the placeholder itself: the three shapes that make a paste machine-specific.
_FORBIDDEN_IN_RENDER: tuple[tuple[str, str], ...] = (
    (r"<PROMPTS_DIR>", "the `<PROMPTS_DIR>` placeholder"),
    (r"[A-Za-z]:[\\/](?:Users|My Drive)", "a literal Windows path"),
    (r"/(?:home|Users)/[A-Za-z0-9._-]+/", "a literal POSIX home path"),
)

#: §0 for every rendered boot. NOT composed here: `to-browser/SEAT-BOOT-integrator.md` §0 is the
#: form AMEND-BATCH-V-002 §3(b) names as "the corrected form", and the same ruling says "the
#: generator makes it structural" -- so generalising that block is applying the ruling. Three
#: lines because all three are load-bearing: an unset variable falls back LOUDLY (a silent
#: Downloads fallback is how "to-cc is empty" gets read as "nothing filed"), a stale inherited
#: PROCESS value is REPAIRED rather than reported (a long-lived daemon's environment block
#: predates the User setting), and the resolved directory is echoed so no later step has to
#: assume which one it read.
TRANSPORT_BLOCK = """```powershell
$d = [Environment]::GetEnvironmentVariable("CLAUDE_PROMPTS_DIR","User")
if (-not $d) { "CLAUDE_PROMPTS_DIR unset - Downloads fallback"; $d = "$env:USERPROFILE\\Downloads" }
if ($env:CLAUDE_PROMPTS_DIR -ne $d) { $env:CLAUDE_PROMPTS_DIR = $d; "process value OVERRIDDEN" }
"transport: $d"
```

Repair a stale process value; do not merely report it. Every path this boot names below is
relative to `$d` -- the variable is the source, and a directory typed by hand is a fact this
paste cannot keep current."""

#: Which Ch8 region states each seat's stop condition. The rendered line POINTS at it rather
#: than restating it: a second statement of a stop condition is a second thing to keep true.
SEAT_STOP_BLOCK: dict[str, str] = {
    "dispatcher": "two-touch",
    "integrator": "refuse-to-finish",
    "filings": "wave-close",
    "handoff": "window-equals-batch",
    "lane": "per-lane-requirements",
}

#: One runnable line per refusal, `{seat}`-agnostic. The seat boot carries the LINE, not the
#: sentiment -- a boot that says "remember the ceiling" has said what this repo already said in
#: prose and then watched be broken.
_REFUSAL_LINES: dict[str, tuple[str, str]] = {
    "lane-ceiling": (
        "uv run --locked python scripts/seat_refusals.py lane-ceiling --check-worktrees "
        "--lane <slug> [--lane <slug> ...]",
        "STEP 0, before the first worktree exists. `--check-worktrees` reads the live list "
        "rather than asking you to self-report what you have already provisioned.",
    ),
    # TWO lines, and the ORDER inside the block is the ruling. The checker runs first, against
    # this step 0's own text; the DryRun of every generated contract is then the LAST thing step
    # 0 does (AMEND-BATCH-V-002 §1). A block that ended on the checker would have moved the
    # DryRun off the boundary it guards, which is the failure the ruling names.
    "dryrun-step0": (
        "uv run --locked python scripts/seat_refusals.py dryrun-step0 --step0 <this file> "
        "--contract <LANE-*.md> [--contract ...]\n"
        "dispatch <LANE-*.md> -DryRun          # once per generated contract, and nothing after",
        "The LAST line of step 0 (AMEND-BATCH-V-002 §1). Present, last, and covering every "
        "generated contract -- the one left out is the one that fails at dispatch. Batch V froze "
        "six contracts the live verb refused and found out by running this.",
    ),
    "carried-by": (
        "uv run --locked python scripts/seat_refusals.py carried-by "
        "$d/to-cc/DECLARE-*.md $d/to-cc/AMEND-*.md $d/to-cc/BATCH-*.md",
        "Before the write, not after it. Flush-left `carried-by:` in the head window, valued "
        "with a repo path or the literal OPEN; a bare substring match is a different check.",
    ),
    "reviewer-mismatch": (
        "uv run --locked python scripts/seat_refusals.py reviewer --contracted <exact model id> "
        "<review artifact>",
        "The tally names the reviewer that actually ran, exactly. A substitution that does not "
        "report `review=NONE` is refused: `gpt-5.6` for `gpt-5.6-terra` is a mismatch.",
    ),
    "sleeping-poll": (
        "uv run --locked python scripts/seat_refusals.py sleeping-poll <your own working notes>",
        "Every wait you write is a loop with an interval, a bound and a predicate read from the "
        "file surface. A turn that ends on an intention has no next tick.",
    ),
}


class RenderRefusal(RuntimeError):
    """A seat boot could not be rendered honestly. Raised -- the caller gets no file."""


def _template_path(seat: str, repo_root: Path) -> Path:
    return repo_root / TMPL_RELPATH / f"SEAT-BOOT-{seat}{TMPL_SUFFIX}"


def out_name(seat: str) -> str:
    """The rendered artifact's filename, per INBOX 038 (`SEAT-BOOT-<role>.md`)."""
    return f"SEAT-BOOT-{seat}.md"


def _provenance(seat: str, batch: str, date: str, ch8_sha: str) -> str:
    """The render header. Machine-readable, because `verify()` reads `batch`/`date` back out of
    it to re-render under the same inputs -- a comparison against a render with different tokens
    would report drift that is not there."""
    return (
        "<!-- GENERATED by scripts/gen_seat_boot.py from protocols/PLAYBOOK.md Ch8.\n"
        "     Do not hand-edit, and do not compose a rival: a composed boot paste is the defect\n"
        "     operator ruling INBOX-dev-knowledge-2026-09-08-038 withdrew.\n"
        f"     seat: {seat} | batch: {batch} | date: {date} | ch8-sha256: {ch8_sha}\n"
        "     Probe P12 re-extracts every ch8: region below and byte-compares; drift = FAIL. -->"
    )


_HEADER_RE = re.compile(
    r"seat:\s*(?P<seat>\S+)\s*\|\s*batch:\s*(?P<batch>.*?)\s*\|\s*date:\s*(?P<date>\S+)\s*\|"
)


def _refusal_block(seat: str) -> str:
    """The seat's refusals, as runnable lines with one clause each on where and why."""
    lines: list[str] = []
    for name in seat_refusals.SEAT_REFUSALS[seat]:
        command, clause = _REFUSAL_LINES[name]
        lines.append(f"**`{name}`** -- {clause}\n\n```\n{command}\n```")
    return "\n\n".join(lines)


def _stop_condition(seat: str) -> str:
    """A POINTER at the region in this same file that states the stop, plus Ch8 point 6's file."""
    key = SEAT_STOP_BLOCK[seat]
    title = seat_ch8.BLOCKS[key].title
    return (
        f"Stated above, by the Ch8 region **{title}** -- this line adds nothing to it and is a "
        "pointer so there is one statement of it rather than two.\n\n"
        f"On stop, write `$d/to-browser/SESSION-{seat}.md` (Ch8 point 6, the STATE IS FILES "
        "region): a session that coordinated only by message leaves no state behind it."
    )


def _ch8_sha(playbook_text: str) -> str:
    """A short digest of the CHAPTER, so the header changes exactly when Ch8 does."""
    chapter = seat_ch8.chapter_text(playbook_text)
    return hashlib.sha256(chapter.encode("utf-8")).hexdigest()[:12]


def render(seat: str, *, batch: str, date: str, repo_root: Path | None = None,
           playbook_text: str | None = None) -> str:
    """One rendered SEAT-BOOT file, as text. Refuses rather than emitting a dishonest paste."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    if seat not in seat_ch8.SEAT_BLOCKS:
        raise RenderRefusal(
            f"REFUSED: {seat!r} is not a declared seat; the enum is {', '.join(seat_ch8.SEATS)}"
        )
    tmpl_path = _template_path(seat, root)
    if not tmpl_path.exists():
        raise RenderRefusal(f"REFUSED: no seat template at {tmpl_path}")
    template = tmpl_path.read_text(encoding="utf-8")

    declared = set(seat_ch8.SEAT_BLOCKS[seat])
    placed = {m.group("key") for m in _CH8_TOKEN_RE.finditer(template)}
    if placed != declared:
        raise RenderRefusal(
            f"REFUSED: {seat} template and seat_ch8.SEAT_BLOCKS disagree -- "
            f"declared-but-unplaced: {sorted(declared - placed) or 'none'}; "
            f"placed-but-undeclared: {sorted(placed - declared) or 'none'}. A declared block that "
            "renders nowhere is doctrine that never reaches the seat, and the output looks fine "
            "either way"
        )

    text = playbook_text if playbook_text is not None else seat_ch8.playbook_text(root)
    rendered = _LEADING_NOTE_RE.sub("", template, count=1)
    for key in declared:
        body = seat_ch8.extract(key, text)
        region = (f"<!-- ch8:begin {key} -->\n{seat_ch8.BLOCKS[key].label}\n\n{body}\n"
                  f"<!-- ch8:end {key} -->")
        rendered = rendered.replace("{{CH8:" + key + "}}", region)
    for token, value in (
        ("BATCH", batch),
        ("DATE", date),
        ("SEAT", seat),
        ("PROVENANCE", _provenance(seat, batch, date, _ch8_sha(text))),
        ("TRANSPORT_BLOCK", TRANSPORT_BLOCK),
        ("REFUSAL_BLOCK", _refusal_block(seat)),
        ("STOP_CONDITION", _stop_condition(seat)),
    ):
        rendered = rendered.replace("{{" + token + "}}", value)

    leftover = sorted({m.group(0) for m in _LEFTOVER_TOKEN_RE.finditer(rendered)})
    if leftover:
        raise RenderRefusal(
            f"REFUSED: {out_name(seat)} still carries {', '.join(leftover)} -- a paste shipped "
            "with a live token is one the seat cannot run, and it ships looking complete"
        )
    for pattern, what in _FORBIDDEN_IN_RENDER:
        m = re.search(pattern, rendered)
        if m:
            raise RenderRefusal(
                f"REFUSED: {out_name(seat)} carries {what} ({m.group(0)!r}) -- "
                "AMEND-BATCH-V-002 §3(b): a rendered boot resolves CLAUDE_PROMPTS_DIR from User "
                "scope itself, with no placeholder and no path typed by the operator"
            )
    seat_refusals.refuse_sleeping_poll(rendered, site=out_name(seat))
    return rendered.rstrip() + "\n"


def write_bundle(bundle_dir: "str | Path", *, batch: str, date: str,
                 repo_root: Path | None = None) -> list[Path]:
    """Render all five boots into `bundle_dir`. Returns the written paths, in seat order."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    target = Path(bundle_dir)
    target.mkdir(parents=True, exist_ok=True)
    text = seat_ch8.playbook_text(root)
    written: list[Path] = []
    for seat in seat_ch8.SEATS:
        path = target / out_name(seat)
        path.write_text(render(seat, batch=batch, date=date, repo_root=root, playbook_text=text),
                        encoding="utf-8", newline="\n")
        written.append(path)
    return written


def verify(bundle_dir: "str | Path", *, repo_root: Path | None = None) -> list[str]:
    """PROBE P12 -- every SEAT-BOOT file in the bundle equals a fresh render from Ch8.

    Returns a list of drift descriptions; empty means PASS. `batch` and `date` are read back out
    of each file's own render header rather than supplied, so a re-render is compared under the
    inputs it was made with -- otherwise every file would report drift the moment the date rolled.

    A MISSING file is drift too. INBOX 038's closure is 0/5 -> 5/5, and a bundle carrying four
    correct boots passes any check that only compares the files that are there.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    target = Path(bundle_dir)
    text = seat_ch8.playbook_text(root)
    drift: list[str] = []
    for seat in seat_ch8.SEATS:
        path = target / out_name(seat)
        if not path.exists():
            drift.append(f"{out_name(seat)}: ABSENT -- the bundle carries no boot for this seat")
            continue
        found = path.read_text(encoding="utf-8")
        header = _HEADER_RE.search(found)
        if header is None:
            drift.append(f"{out_name(seat)}: no render header -- hand-written or hand-edited")
            continue
        try:
            fresh = render(seat, batch=header.group("batch"), date=header.group("date"),
                           repo_root=root, playbook_text=text)
        except (RenderRefusal, seat_ch8.ExtractionError, seat_refusals.SeatRefusal) as exc:
            drift.append(f"{out_name(seat)}: a fresh render REFUSES -- {exc}")
            continue
        if fresh != found:
            drift.append(
                f"{out_name(seat)}: DRIFT from Ch8 -- the file differs from a fresh render "
                f"({len(found)} B on disk, {len(fresh)} B fresh); regenerate with "
                "`python scripts/gen_seat_boot.py write --bundle <dir>`"
            )
    return drift


@click.group(help="Render the five SEAT-BOOT pastes from PLAYBOOK Ch8 (INBOX 038).")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("write")
@click.option("--bundle", required=True, type=click.Path(file_okay=False),
              help="the handoff bundle directory to render into")
@click.option("--batch", required=True, help="the batch this cut belongs to, e.g. V")
@click.option("--date", required=True, help="the window date, YYYY-MM-DD")
def cmd_write(bundle: str, batch: str, date: str) -> None:
    """Render SEAT-BOOT-{dispatcher,integrator,filings,handoff,lane}.md into BUNDLE."""
    try:
        written = write_bundle(bundle, batch=batch, date=date)
    except (RenderRefusal, seat_ch8.ExtractionError, seat_refusals.SeatRefusal) as exc:
        click.echo(str(exc), err=True)
        raise SystemExit(1) from exc
    for path in written:
        click.echo(f"{path} ({path.stat().st_size} B)")


@cli.command("verify")
@click.option("--bundle", required=True, type=click.Path(exists=True, file_okay=False))
def cmd_verify(bundle: str) -> None:
    """Probe P12: every SEAT-BOOT file equals a fresh render from Ch8."""
    drift = verify(bundle)
    for line in drift:
        click.echo(line, err=True)
    if drift:
        click.echo(f"P12: FAIL -- {len(drift)} of {len(seat_ch8.SEATS)} seat boot(s) drifted",
                   err=True)
        raise SystemExit(1)
    click.echo(f"P12: PASS -- {len(seat_ch8.SEATS)} seat boot(s) equal a fresh render from Ch8")


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
