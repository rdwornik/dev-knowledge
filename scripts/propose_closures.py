#!/usr/bin/env python
"""propose_closures.py — ADR-70 Tier-1 session-end closure detector.

Deterministic and read-only. At session Stop, detect backlog items whose work
appears complete and write a dated PROPOSALS artifact for review at the next
session-start (/boot — Unit 3). **DETECT-AND-PROPOSE ONLY**: this script never
closes, removes, or modifies a backlog item. The human approves later.

Evidence tiers (precision over recall — surface only real evidence; a false
positive every session kills adoption, so under-surfacing is the safer error):

  STRONG — a commit message in the window says `closes [#N]` for an `[#N]` that
           is still present (open) in BACKLOG.md. The closing commit fired but
           the item was never removed (the exact staleness LESSON behind ADR-70).
  WEAK   — an open task names a concrete repo-relative file in its text, and a
           commit in the window modified that exact file with no `closes` for any
           id. The referenced area moved (inferred completion — needs judgment).

Observable / anti-vacuous: ALWAYS writes `logs/PROPOSALS-YYYY-MM-DD.md`, even when
nothing is detected. The file's presence proves the detector ran; its ABSENCE is
the loud failure signal. The artifact is gitignored — it is ephemeral session
scaffolding, not the durable record (that stays the eventual `closes [#N]` commit
+ the JOURNAL entry, ADR-65).

Window: commits since the HEAD recorded in the most recent prior PROPOSALS file
(`head_commit:` frontmatter); falls back to `HEAD~N..HEAD` when no prior file.

Layer-2 / read-only contract: reads git + BACKLOG.md; writes only
`logs/PROPOSALS-*.md`. NEVER mutates BACKLOG. On any error it prints loudly to
stderr and exits 0 — a Stop hook must not wedge session-end. Reuses
`validate_backlog.parse` (loaded by path) for the backlog hierarchy; does not
build a parallel parser. Wired via `.claude/settings.json` Stop hook.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_BACKLOG = _REPO_ROOT / "BACKLOG.md"
_LOGS_DIR = _REPO_ROOT / "logs"

# A closing keyword immediately before a [#id] — the documented convention is
# `closes [#N]` (mirrors check_backlog_commit_msg.py / `git log --grep`).
CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)

# [#437] — a closes-token counts ONLY as a plain-text directive (CONTRIBUTING.md:
# `feat: …, closes [#57]`). Occurrences inside quoting contexts are prose ABOUT the
# convention (constant in this methodology repo) and must never read as a closure:
# two live false positives are on record (`12e6b45b` backtick-quoted denial,
# `096364ac` pre-amend draft quoting a doc clause). Same-line principle for inline
# contexts (design amendment M1): pairing across lines could blank real text and
# hide a REAL directive — the worse failure direction — so only fenced blocks span
# lines. Inline code pairs EQUAL-LENGTH backtick runs (diff-review H-B: ``…`` is a
# standard quoted form). Order: fenced → inline code → block-quote lines →
# double-quoted spans.
_STRIP_RES = (
    re.compile(r"```.*?```", re.S),      # fenced block (multi-line by nature)
    re.compile(r"~~~.*?~~~", re.S),      # tilde fence — the other CommonMark delimiter
    re.compile(r"(`+)[^`\r\n]*?\1"),     # inline span, same line, equal-length runs
    re.compile(r"^[ \t]*>.*$", re.M),    # block-quote line (quoted ruling/doc text)
    re.compile(r'"[^"\r\n]*"'),          # straight-double-quoted span, same line
    re.compile(r"“[^”\r\n]*”"),  # curly-double-quoted span “…”
)

# Stripped spans are replaced by a NON-WHITESPACE barrier, never blanks: CLOSES_RE
# bridges its keyword and `[#N]` across `\s+`, so whitespace substitution would
# SYNTHESIZE directives the raw text never had (diff-review H-A: `closes "x" [#5]`).
# NUL cannot appear in a git commit message, so the barrier is collision-free.
_STRIP_BARRIER = "\x00"


def strip_quoted_contexts(text: str) -> str:
    """Barrier-out every quoted context so only plain-text directives remain
    matchable — and no new match can be assembled across a stripped span."""
    for rx in _STRIP_RES:
        text = rx.sub(_STRIP_BARRIER, text)
    return text


def closure_ids(text: str) -> list:
    """THE closure-token detector ([#437] shared core): ids declared closed by
    `text`, counting a token only as a plain-text directive (quoted contexts
    stripped). Both scanners — this module's STRONG/WEAK detection and
    validate_git_backlog.reconcile — flow through here; do not re-derive."""
    return CLOSES_RE.findall(strip_quoted_contexts(text or ""))

# A repo-relative file path token: at least one directory component + a known
# code/doc extension. Requiring the slash is the precision lever — bare refs like
# `ADR-35` or `coherence-audit HK-1` do not match, so WEAK stays conservative.
_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+\.(?:py|md|ya?ml|toml|cfg|ini|json|ps1))"
)

# High-churn canonical files: they change almost every session, so a path-match
# against them would false-positive constantly. Excluded from WEAK detection.
_CHURN_FILES = {"BACKLOG.md", "JOURNAL.md", "LESSONS.md"}


class Commit:
    """One commit in the window. `files` = paths it touched (git --name-only).

    A plain class (not a dataclass) so the module loads robustly under any import
    mechanism — including importlib-by-path (tests, and the Unit-5 plugin) where a
    dataclass's annotation scan would fail on the unregistered module.
    """

    def __init__(self, sha: str, subject: str, body: str = "", files=None):
        self.sha = sha
        self.subject = subject
        self.body = body
        self.files = files or []

    @property
    def message(self) -> str:
        return f"{self.subject}\n{self.body}"

    def __repr__(self) -> str:
        return f"Commit({self.sha[:9]!r}, {self.subject!r})"


# ---------------------------------------------------------------------------
# Pure detection core (no git, no I/O — unit-tested directly)
# ---------------------------------------------------------------------------

def task_paths(text: str) -> set:
    """Concrete repo-relative file paths named in a task's text (churn excluded)."""
    out = set()
    for m in _PATH_RE.findall(text):
        if m.rsplit("/", 1)[-1] not in _CHURN_FILES:
            out.add(m)
    return out


def find_strong(open_ids: set, commits: list) -> dict:
    """STRONG hits: id -> [(sha, subject), ...] where `closes [#id]` and id still open."""
    hits: dict = {}
    for c in commits:
        for cid in closure_ids(c.message):
            if cid in open_ids:
                hits.setdefault(cid, []).append((c.sha, c.subject))
    return hits


def find_weak(open_tasks: dict, commits: list, strong_ids: set) -> dict:
    """WEAK hits: id -> [(path, sha, subject), ...].

    A no-`closes` commit modified a concrete file the open task names. Skips ids
    already STRONG (no double-listing) and commits that close anything (those are
    STRONG signal, not inferred).
    """
    plain = [c for c in commits if not closure_ids(c.message)]
    weak: dict = {}
    for cid, text in open_tasks.items():
        if cid in strong_ids:
            continue
        paths = task_paths(text)
        if not paths:
            continue
        for c in plain:
            for mf in sorted(set(c.files) & paths):
                weak.setdefault(cid, []).append((mf, c.sha, c.subject))
    return weak


def _first_clause(text: str) -> str:
    """The leading action clause of a task (before the first ` · `)."""
    return text.split(" · ")[0].strip() if text else "(task text unavailable)"


def render(strong: dict, weak: dict, run_date: date, head: str, since,
           n_commits: int, open_tasks: dict, weak_suppressed: bool = False) -> str:
    """Render the PROPOSALS markdown. Flat/plain so it is cheap to scan."""
    since_disp = since if since else "(none — cold start / no prior baseline)"
    lines = [
        "---",
        f"generated: {run_date.isoformat()}",
        f"head_commit: {head}",
        f"since_commit: {since_disp}",
        f"window_commits: {n_commits}",
        "kind: closure-proposals",
        "---",
        "",
        f"# Closure proposals — {run_date.isoformat()}",
        "",
        "> ADR-70 Tier-1 · **detect-and-propose only** — this file never closes",
        "> anything. Review at the next /boot. **Nothing has been removed from",
        "> BACKLOG.md.** Gitignored, ephemeral; the durable record is the eventual",
        "> `closes [#N]` commit + JOURNAL entry (ADR-65).",
        "",
    ]
    if weak_suppressed:
        lines += [
            "> _WEAK detection suppressed: no prior session baseline (cold start), so",
            "> a file-touch window would span the whole history and over-surface._",
            "> _STRONG (closing-commit) detection is precise regardless and still ran._",
            "",
        ]

    if not strong and not weak:
        lines += [
            "**No closures detected** in this window.",
            "",
            "(This file's presence proves the session-end detector ran; its absence",
            "is the failure signal.)",
            "",
        ]
        return "\n".join(lines)

    if strong:
        lines += [
            "## STRONG — closing commit landed, item still open",
            "",
            "Each item below has a `closes [#N]` commit in the window, yet `[#N]` is",
            "still present in BACKLOG.md. **Approve all:** reply `y`, then remove each",
            "from BACKLOG (done-items-leave, ADR-65; reference the id in the commit).",
            "",
        ]
        for cid in sorted(strong, key=int):
            lines.append(f"- [ ] **#{cid}** — {_first_clause(open_tasks.get(cid, ''))}")
            for sha, subj in strong[cid]:
                lines.append(f"    - evidence: `{sha[:9]}` {subj}")
        lines.append("")

    if weak:
        lines += [
            "## WEAK — referenced file changed, no explicit closure (inferred)",
            "",
            "Lower confidence — a file the task names was modified, but no `closes`",
            "fired. **Confirm one:** type its `#N`; ignore the rest. No bulk-approve",
            "(precision guard — these are inferences, not declarations).",
            "",
        ]
        for cid in sorted(weak, key=int):
            lines.append(f"- [ ] **#{cid}** — {_first_clause(open_tasks.get(cid, ''))}")
            for path, sha, subj in weak[cid]:
                lines.append(f"    - evidence: `{path}` changed in `{sha[:9]}` {subj}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Git + backlog adapters (thin, impure)
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def git_head(repo: Path):
    r = _git(repo, "rev-parse", "HEAD")
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def git_valid_rev(repo: Path, rev: str) -> bool:
    r = _git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return r.returncode == 0 and bool(r.stdout.strip())


def git_log_commits(repo: Path, rev_range: str, first_parent: bool = False) -> list:
    """Parse `git log <range>` into Commit objects (subject/body/files).

    Field-separated with control chars so subjects/bodies/files survive newlines:
    record = \\x1e, fields = \\x1f, then the --name-only file list follows.

    first_parent=True restricts to the main-line history (`--first-parent`) — the
    `--no-ff` merge spine (core-invariants rule 5). Used by validate_git_backlog to
    keep `closes [#id]` detection to real ship-time closures, excluding branch-internal
    fixture/example `closes` text. Default False preserves the all-ancestors behaviour.
    """
    fmt = "%x1e%H%x1f%s%x1f%b%x1f"
    args = ["log", rev_range, f"--format={fmt}", "--name-only"]
    if first_parent:
        args.append("--first-parent")
    r = _git(repo, *args)
    if r.returncode != 0:
        return []
    commits = []
    for rec in r.stdout.split("\x1e"):
        if not rec.strip():
            continue
        parts = rec.split("\x1f")
        if len(parts) < 4:
            continue
        files = [ln.strip() for ln in parts[3].splitlines() if ln.strip()]
        commits.append(Commit(parts[0].strip(), parts[1], parts[2], files))
    return commits


def find_last_proposals_head(logs_dir: Path):
    """HEAD sha recorded in the most recent prior PROPOSALS file, or None.

    `**/PROPOSALS-*.md` matches a file sitting flat under `logs_dir` (today's, not yet
    archived) AND one already relocated into a `logs/YYYY-MM/` bucket by
    `logs_retention.py`, so the search stays correct across that move. Sorted by
    FILENAME, not full path -- the date lives in the name (`PROPOSALS-YYYY-MM-DD.md`),
    and a bucket prefix (`2026-08/...`) would otherwise sort ahead of a flat sibling
    from a later month purely on directory-name text.
    """
    files = sorted(logs_dir.glob("**/PROPOSALS-*.md"), key=lambda p: p.name)
    if not files:
        return None
    text = files[-1].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"head_commit:\s*([0-9a-fA-F]{7,40})", text)
    return m.group(1) if m else None


# An unchecked proposal line is "- [ ] **#N** — ..."; a checked one is "- [x] ...".
# An id is "pending" when it is unchecked in a PROPOSALS file AND still open in
# BACKLOG (once it is closed/removed it stops pinning the baseline). #98.
_UNCHECKED_RE = re.compile(r"-\s+\[ \]\s+\*\*#(\d+)\*\*")
_HEAD_RE = re.compile(r"head_commit:\s*([0-9a-fA-F]{7,40})")
_SINCE_RE = re.compile(r"since_commit:\s*([0-9a-fA-F]{7,40})")


def _proposals_meta(text: str):
    """(head_sha|None, since_sha|None, {unchecked_ids}) for one PROPOSALS file."""
    h = _HEAD_RE.search(text)
    s = _SINCE_RE.search(text)
    return (
        h.group(1) if h else None,
        s.group(1) if s else None,
        set(_UNCHECKED_RE.findall(text)),
    )


def resolve_window(repo: Path, logs_dir: Path, open_ids: set):
    """Return (since_sha_or_None, rev_range) for the commit window.

    #98 — the baseline must NOT advance past proposals that are still PENDING
    (unchecked in some PROPOSALS file AND still open in BACKLOG). While any prior
    proposal is pending, re-cover from the EARLIEST pending file's window start, so
    a re-run RE-DETECTS it instead of erasing it (the self-erasure bug: a same-day
    second run read the just-written file's head_commit, got an empty HEAD..HEAD
    window, and overwrote the morning's proposals with "no closures"). Only once
    every prior proposal is reviewed/closed does the baseline advance to the latest
    file's head_commit.

    `**/PROPOSALS-*.md`, sorted by filename not full path -- see
    `find_last_proposals_head` above for why (bucketed AND flat files both count).
    """
    files = (sorted(logs_dir.glob("**/PROPOSALS-*.md"), key=lambda p: p.name)
             if logs_dir.exists() else [])
    metas = []
    for f in files:
        try:
            metas.append(_proposals_meta(f.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    pending = [(head, since) for (head, since, unchecked) in metas if unchecked & open_ids]
    if pending:
        # files are date-sorted, so pending[0] is the earliest -> widest safe window
        _, since = pending[0]
        if since and git_valid_rev(repo, since):
            return since, f"{since}..HEAD"
        # earliest pending file was a cold start (no baseline): re-cover whole
        # history. STRONG stays precise (still-open guard); WEAK suppressed.
        return None, "HEAD"
    # nothing pending -> safe to advance to the most recent file's head
    last = metas[-1][0] if metas else None
    if last and git_valid_rev(repo, last):
        return last, f"{last}..HEAD"
    return None, "HEAD"


def _load_validate_backlog():
    """Load validate_backlog by path (cwd-independent; no codemap import edge)."""
    spec = importlib.util.spec_from_file_location(
        "validate_backlog", _SCRIPTS_DIR / "validate_backlog.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def open_tasks_from_backlog(text: str, parse_fn) -> dict:
    """{id: task_text} for every open task (reuses validate_backlog.parse)."""
    tasks = parse_fn(text)[2]
    return {t["id"]: t["rest"] for t in tasks}


def _existing_anywhere(logs_dir: Path, name: str) -> bool:
    """True if `name` is present flat under logs_dir OR inside a month bucket.

    Both locations count, and that is the whole point: the wedge this function exists to
    prevent was a FLAT file written with a name that was already ARCHIVED, which
    `logs_retention.apply_moves` then correctly refused to overwrite -- aborting the entire
    plan and queueing every later day behind a collision that never clears itself.
    """
    if (logs_dir / name).exists():
        return True
    return any(p.name == name for p in logs_dir.glob("*/" + name))


def _next_free_dated_path(logs_dir: Path, prefix: str, ext: str = "md",
                          today: "date | None" = None) -> Path:
    """First free `<prefix>-<YYYY-MM-DD>-<NN>.<ext>`, checking flat AND bucketed.

    PER-RUN GRAMMAR (operator declaration 2026-09-04): every run carries a sequence, starting
    at `-01`. The old `PROPOSALS-<date>.md` was day-granular for a per-RUN artifact, so a
    second run on one day silently overwrote the first -- and once one copy had been archived,
    `logs_retention.apply_moves` correctly REFUSED to overwrite it, aborting the whole plan and
    queueing every later day behind a collision that never cleared itself.

    Sequencing EVERY run (rather than only the second) is what keeps name order equal to time
    order: `-` is 0x2D and `.` is 0x2E, so a bare `<date>.md` sorts AFTER `<date>-02.md`. With
    all runs sequenced there is no bare name to sort last, and the six `sorted(...)[-1]`
    "latest" sites across propose_closures / review_closures / fleet_health stay correct with
    no custom key. Legacy bare files predate the grammar and are never rewritten.
    """
    stamp = (today or date.today()).isoformat()
    for n in range(1, 100):
        cand = f"{prefix}-{stamp}-{n:02d}.{ext}"
        if not _existing_anywhere(logs_dir, cand):
            return logs_dir / cand
    raise RuntimeError(
        f"{prefix}: 99 runs already recorded for {stamp} -- refusing to guess a 100th name")


def _write_artifact(content: str) -> Path:
    _LOGS_DIR.mkdir(exist_ok=True)
    out = _next_free_dated_path(_LOGS_DIR, "PROPOSALS")
    out.write_text(content, encoding="utf-8", newline="\n")
    return out


_ERROR_HEADING = "# Closure proposals - DETECTOR ERROR"


def _describe_precondition_failure() -> str:
    """Name WHICH input is missing, or "" when the inputs are all present.

    The husk artifact this replaces read, in full:

        The session-end detector raised: `FileNotFoundError(2, 'No such file or directory')`

    -- which names no path, so it is undiagnosable: repr(FileNotFoundError) drops the
    `filename` that Path.read_text set, and the reader cannot tell a missing BACKLOG.md
    from a missing validate_backlog.py from a misresolved repo root. Checking the inputs
    up front turns an anonymous errno into a sentence naming the file and the root it was
    resolved against.

    THIS copy resolves `_REPO_ROOT` from `__file__`, so its root is structurally correct
    and only a genuinely absent input trips these branches. The exposed twin is the
    PLUGIN copy (the live Stop-hook scanner), which resolves the host repo from
    $CLAUDE_PROJECT_DIR and falls back to cwd -- so a run with that env unset points
    BACKLOG at a tree that has none, which is how the recorded husk was produced. The
    check is kept identical in both copies rather than only in the exposed one.
    """
    if not _REPO_ROOT.exists():
        return f"resolved repo root does not exist: {_REPO_ROOT}"
    if not _BACKLOG.is_file():
        return (f"BACKLOG.md not found at {_BACKLOG} "
                f"(repo root resolved to {_REPO_ROOT}) - the detector was pointed at a "
                f"tree that is not the host repo")
    vb = _SCRIPTS_DIR / "validate_backlog.py"
    if not vb.is_file():
        return f"validate_backlog.py not found at {vb} (the bundled parser is missing)"
    return ""


def _write_error_marker(reason: str) -> Path:
    """Record a detector failure at `DETECTOR-ERROR-<date>.md` -- NEVER as a PROPOSALS file.

    The marker does not occupy the `PROPOSALS-*` namespace AT ALL. Writing it there (what
    the original error path did unconditionally) breaks this module's own contract in three
    ways -- the first two found by terra review 2026-08-25, the third stated in the module
    docstring above:

      1. It SHADOWS real pending proposals. `review_closures.latest_proposals()` globs the
         same `PROPOSALS-*.md` namespace (flat and bucketed, sorted by filename) and takes
         the last one, so a failed run TODAY hides YESTERDAY's genuine unreviewed proposals
         behind an empty marker. Preserving only the same-DAY file (this lane's first
         attempt) does not reach that.
      2. It CORRUPTS the window. `resolve_window` globs the same pattern, and a file
         carrying no `head_commit:` collapses the baseline to a cold start -- whole-history
         rescan with WEAK suppressed.
      3. It INVERTS the loud-failure signal. This module promises "ALWAYS writes
         logs/PROPOSALS-YYYY-MM-DD.md ... its ABSENCE is the loud failure signal". A husk
         at that path makes the file PRESENT while the detector did not run, which is
         precisely backwards. Keeping the namespace clean RESTORES the signal: on failure
         today's PROPOSALS file is absent (so the signal fires) and a named diagnosis sits
         beside it.

    UPPERCASE-KEBAB stem per the logs/ naming ruling 2026-07-22, deliberately outside the
    `PROPOSALS-*.md` glob. Rewriting the same path on a second failure is intended: two
    broken runs in one day leave one marker, not an accumulating pile.
    """
    _LOGS_DIR.mkdir(exist_ok=True)
    body = (f"{_ERROR_HEADING} ({date.today().isoformat()})\n\n"
            f"The session-end detector did not run: {reason}\n\n"
            f"BACKLOG was not touched, and NO closure proposals were produced -- this\n"
            f"file is the absence of a result, not a result. Investigate\n"
            f"propose_closures.py.\n")
    out = _LOGS_DIR / f"DETECTOR-ERROR-{date.today().isoformat()}.md"
    out.write_text(body, encoding="utf-8", newline="\n")
    return out


def main() -> int:
    # Preconditions FIRST, named. The detector's inputs are checked before any work so a
    # missing one is reported as a sentence naming the file, not as an anonymous errno
    # surfacing from deep inside read_text (STANDING_RULINGS section U: the closure
    # detector funds births -- its output must be trustworthy or fail loudly).
    problem = _describe_precondition_failure()
    if problem:
        print(f"propose_closures: ERROR - detector did NOT run: {problem}", file=sys.stderr)
        try:
            marker = _write_error_marker(problem)
            print(f"propose_closures: recorded the failure at {marker}", file=sys.stderr)
        except OSError as exc:
            print(f"propose_closures: could not record the failure: {exc!r}", file=sys.stderr)
        # exit 0 is deliberate: this runs as the Stop hook, declared non-blocking in
        # hooks.json, and must never wedge session-end. Loud + diagnosable +
        # non-destructive, NOT a new gate.
        return 0
    try:
        vb = _load_validate_backlog()
        open_tasks = open_tasks_from_backlog(
            _BACKLOG.read_text(encoding="utf-8", errors="replace"), vb.parse
        )
        open_ids = set(open_tasks)
        head = git_head(_REPO_ROOT) or "UNKNOWN"
        since, rev_range = resolve_window(_REPO_ROOT, _LOGS_DIR, open_ids)
        commits = git_log_commits(_REPO_ROOT, rev_range)
        strong = find_strong(open_ids, commits)
        # WEAK (inferred file-touch) needs a trustworthy session window. On cold
        # start there is no baseline, so suppress it rather than over-surface.
        cold_start = since is None
        weak = {} if cold_start else find_weak(open_tasks, commits, set(strong))

        # #98 safety net: never let an EMPTY regeneration erase a PROPOSALS file
        # that still holds pending (unchecked + still-open) items. The baseline
        # rule above normally re-detects them; this guards the residual edge (e.g.
        # a pending WEAK item suppressed on a cold-start re-cover).
        target = _LOGS_DIR / f"PROPOSALS-{date.today().isoformat()}.md"
        if not strong and not weak and target.exists():
            try:
                existing = target.read_text(encoding="utf-8", errors="replace")
            except OSError:
                existing = ""
            if _proposals_meta(existing)[2] & open_ids:
                print("propose_closures: WARNING - empty regeneration would erase "
                      f"unreviewed proposals in {target.name}; preserving it (no "
                      "overwrite).", file=sys.stderr)
                return 0

        out = _write_artifact(
            render(strong, weak, date.today(), head, since, len(commits),
                   open_tasks, weak_suppressed=cold_start)
        )
        print(f"propose_closures: {len(strong)} strong, {len(weak)} weak "
              f"over {len(commits)} commit(s) -> {out.name}"
              + (" (weak suppressed: cold start)" if cold_start else ""))
        return 0
    except Exception as exc:  # never wedge session-end; fail loud, leave a marker
        # repr() alone is what made the husk undiagnosable (a bare
        # `FileNotFoundError(2, 'No such file or directory')` names no path), so the
        # OSError filename -- which repr drops -- is recovered explicitly here.
        detail = f"{exc!r}"
        fname = getattr(exc, "filename", None)
        if fname:
            detail += f" on {fname}"
        print(f"propose_closures: WARNING - detector failed: {detail}", file=sys.stderr)
        try:
            _write_error_marker(f"raised {detail}")
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
