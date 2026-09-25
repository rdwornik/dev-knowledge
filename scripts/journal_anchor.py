#!/usr/bin/env python
"""journal_anchor.py — the ADR-85 anchoring predicate, defined ONCE.

ADR-85 amendment 2026-08-03. Two organs enforce that amendment:

  * `block_unanchored_push.py` — the HARD leg at pre-push (§A5 / FR1-FR2), over the
    range git hands the hook.
  * `audit.check_journal_spine_anchor` — the audit backstop (§A8 / FR4), over
    `git log --first-parent main` above the dated disposition floor.

They MUST agree about what "anchored" means, so the predicate lives here and both import
it — the same reuse-integrity shape `block_ff_push` already uses for its FF-signature
(`validate_no_ff.find_violations`). A second definition is a drift edge, not a convenience.

THE PREDICATE (ADR-85 §A7, ratified 2026-08-03):

    A first-parent spine entry is ANCHORED when JOURNAL.md names >= 1 SHA that the entry
    INTRODUCED -- not the entry's own SHA.

A merge commit cannot name its own hash: the JOURNAL entry it carries is authored before
the merge exists. Measured at 4f3f8531, the naive "spine SHA is named" predicate reports
686 of 1292 spine entries unanchored INCLUDING HEAD ITSELF; the correct predicate gives a
contiguous anchored run of 11 from HEAD. An implementation on the naive predicate fails on
its own merge — which is why this docstring states it rather than leaving it to a reader.

Matching is on the 7-char short prefix, so any reference length (7..40) is caught — the
same convention `session_end_backpressure._commit_anchors_journal` has always used.

Layer-2 contract (ADR-28/36): read-only. This module runs git plumbing reads and string
matches; it writes nothing, anywhere.

FAIL-LOUD: every helper raises `AnchorError` on a git failure. Callers decide the posture
-- the hard organs fail CLOSED (ADR-85 §A6 / FR6), never swallowing an error into a pass.
"""
from __future__ import annotations

import functools
import heapq
import re
import subprocess
from pathlib import Path
from typing import NamedTuple

_JOURNAL = "JOURNAL.md"
#: Rotation tiling ([#608], ruling X5: rotate the FILE, not the PREDICATE). The
#: anchoring universe is `JOURNAL.md` PLUS any `JOURNAL-legacy-*.md`, so a future
#: split changes which file a byte lives in and changes nothing a gate can observe.
#: No gate is re-taught a new concept -- that is the whole point of landing the seam
#: before any content moves.
#: A legacy tile is `JOURNAL-legacy-<ISO-span>.md`. The ISO prefix is REQUIRED, not
#: decorative: it is what makes a plain lexical sort equal date order, and it is what
#: keeps a stray `JOURNAL-legacy-notes.md` out of the anchoring universe. A file swept
#: in by accident can mark a spine entry anchored that nothing actually anchors --
#: a FALSE GREEN on the ADR-85 hard leg (terra HIGH, 2026-08-28).
_LEGACY_RE = re.compile(r"^JOURNAL-legacy-\d{4}(?:-\d{2}){0,2}[A-Za-z0-9._-]*\.md$")
_SHORT = 7


# --- the ADR-85 message, defined ONCE alongside the predicate it describes ------------------
#
# The predicate above is shared as CODE (`introduced`, `is_anchored`). What follows is the same
# rule shared as TEXT, and it needs its own single source for exactly the reason the code does:
# AF-1 records EIGHT false alarms in one day, each from a seat that inferred this predicate from
# the shape of a failure, and two successive drafts of AF-1 itself restating it wrongly in two
# different ways. A rule its own scribe could not restate correctly twice running is not one two
# organs should be paraphrasing independently.
#
# BOTH ORGANS PRINT THESE. `audit.check_journal_spine_anchor` (the backstop) appends them to its
# FAIL evidence; `block_unanchored_push` (the hard leg) prints them on its refusal, where the
# reader is a seat whose push was just rejected and who has no other surface to consult. Before
# this lane the hard leg printed a two-line PARAPHRASE of its own -- "add a JOURNAL entry naming
# >=1 SHA this push introduces" -- which is true, omits both exclusions, and is the same class of
# restatement AF-1 was filed about.

# AF-1 (`protocols/STANDING_RULINGS.md` §AF, filed 2026-09-05): a check states its predicate in
# its own failure text and hands over ONE diagnostic command. Filed from witnessed cost -- this
# predicate produced EIGHT false alarms across SIX seats in a single day, one of which reached the
# operator and stopped the merge queue. Every one of the eight substituted a SHA the entry did NOT
# introduce (most often the entry's own merge SHA, or one already sitting on the scanned ref), or
# read a lagging worktree as truth. No seat was careless: each inferred a predicate this message
# never stated, and each inferred a DIFFERENT one.
#
# THE WORDING IS QUOTED FROM AF-1 RATHER THAN RESTATED, which is deliberate. AF-1 records two
# successive drafts of ITSELF misstating this rule in two different ways -- "never a branch tip"
# (false: a merged branch's tip normally does qualify) and "a merge does not introduce itself"
# (false: `journal_anchor.introduced` is `firstparent..sha` PLUS the entry, and the exclusion is
# temporal). A rule its own scribe could not restate correctly twice running is not one a reader
# should be asked to infer from the shape of a failure.
SPINE_PREDICATE = (
    "; PREDICATE (ADR-85 amendment 2026-08-03 section A7; STANDING_RULINGS AF-1) -- a spine "
    "entry is anchored when the JOURNAL names AT LEAST ONE SHA THAT THE ENTRY INTRODUCED. "
    "That is the entire test. The "
    "introduced set is `<first-parent>..<sha>` PLUS the entry itself "
    "(`scripts/journal_anchor.py`, `introduced`). Three readings that are NOT the test: "
    "(1) BRANCH-TIP STATUS forms no part of it -- the tip of the branch being merged normally "
    "does qualify, but because the merge introduces it, not because it is a tip; "
    "(2) THE ENTRY'S OWN MERGE SHA is in the introduced set and still cannot be used, for a "
    "temporal reason rather than a set-theoretic one: its hash does not exist when the JOURNAL "
    "text is authored and committed, so it is unavailable to name; "
    "(3) A SHA ALREADY ON THE SCANNED REF before the entry fails the test itself, because naming "
    "it introduces nothing"
)
SPINE_DIAGNOSTIC = (
    "; DIAGNOSTIC -- run unmodified from the repo root, substituting one <sha> named above: "
    "uv run --locked python -c \"import sys,pathlib;sys.path.insert(0,'scripts');"
    "import journal_anchor as j;r=pathlib.Path('.');s='<sha>';"
    "print('introduced:',j.introduced(r,s));"
    "print('anchored in this tree:',j.is_anchored(r,s,j.journal_text(r)));"
    "print('anchored at main:',j.is_anchored(r,s,j.journal_text(r,'main')))\"; "
    "THE TREE ASYMMETRY, which turned one of the eight into an operator stop: this check reads the "
    "JOURNAL from the COMMITTING TREE and the spine from the shared ref, so a tree that is behind "
    "reports gaps that do not exist on main. False here with True at main means SYNC THIS TREE -- "
    "there is no gap on main, and a drain entry would not reach a lagging tree anyway. One further "
    "fact settles the common case on its own: `block-unanchored-push` fails CLOSED, so a range "
    "that has already pushed clean cannot be unanchored"
    "; THE SECOND ASYMMETRY, in the ADR-110 exemption rather than the anchor predicate (measured 2026-09-06): the backstop resolves the SPINE against `main` -- a ref shared through the common git dir -- while resolving the open-batch manifest from THIS branch's `HEAD` (`batch_manifest.open_batches` -> `git show HEAD:<manifest>`, the committed-blob rule). A worktree branched before the manifest landed therefore sees the integrator's lane merges on the shared spine and cannot exempt them, and reports gaps for merges it did not make. Same command fixes it -- `git merge origin/main` -- and the exemption clause below says which batch it read, so an unexpected EMPTY batch list is the tell"
    "; SYNC COMMAND, for exactly that case -- `git merge origin/main`, run IN THE TREE that reported the gap, then re-read. This is the recorded fix for the tree-lag class rather than a suggestion: on the night of 2026-09-05 it resolved the spine blocks that were lag and not gaps, repeatedly, while every other remedy tried (re-anchoring an already-anchored SHA, --no-verify, re-running the check) addressed a gap that was not there. Run the diagnostic above FIRST: it is the discriminator, and `git merge` is the fix for only one of its two answers"
)

# Only a FULL 40-hex object name is an immutable cache key. A ref (`main`, `HEAD`, a short
# prefix that could later become ambiguous) can resolve to a different commit tomorrow, so
# `introduced` refuses to memoize one -- see its docstring.
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# Ceiling for the `_introduced_tuple` memo. This repo's whole first-parent spine is ~1300
# entries and the two spine-walking checks each traverse it, so 2048 holds a full double walk
# with headroom. Each value is a short tuple of hex strings -- kilobytes, not megabytes, which
# is why this ceiling is generous where `_ENTRIES_CACHE_MAXSIZE` is tight.
_INTRODUCED_CACHE_MAXSIZE = 2048

# ADR-85's dated disposition floor is read FROM THE ADR, never hardcoded here and never
# re-derived. FR4: "Floor read from the ADR, never re-derived and never widened in code."
# Keeping the constant out of code is the point: a floor that lives in a Python literal can
# be widened in a commit that reads like a refactor, whereas widening it here requires
# editing the ratified ADR, which is a visible governance act.
_ADR_PATH = "docs/decisions/ADR-85-session-lifecycle-enforcement.md"
_FLOOR_RE = re.compile(r"Dated disposition floor:\s*`([0-9a-f]{7,40})`")


class AnchorError(RuntimeError):
    """A git read failed, or a required governance input is missing/unparseable."""


def _git(repo: Path, *args: str) -> str:
    """Run a read-only git command in `repo`; raise AnchorError on failure.

    Deliberately NOT fail-soft. An unreadable history is an unknown anchoring state, and
    an unknown state must never render as "anchored" -- that is the exact defect class the
    ADR-85 amendment exists to remove.
    """
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
    except Exception as exc:  # noqa: BLE001 -- surfaced, never swallowed
        raise AnchorError(f"git {' '.join(args)} failed to run: {exc!r}") from exc
    if r.returncode != 0:
        raise AnchorError(f"git {' '.join(args)} exited {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def floor_sha(repo: Path) -> str:
    """The dated disposition floor SHA, parsed from the ratified ADR-85 amendment.

    Raises AnchorError when the ADR is missing or the floor line is unparseable. That is
    deliberate: a backstop that silently defaults to "no floor" would either flood on
    inherited history or, worse, quietly widen its own exemption.
    """
    path = repo / _ADR_PATH
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AnchorError(f"cannot read {_ADR_PATH}: {exc!r}") from exc
    # EXACTLY ONE declaration, never "the first match" (terra HIGH, 2026-08-03). With
    # `search()` a second floor line -- an amendment that adds one without removing the old,
    # or a malformed line beside a valid one -- silently selects whichever appears first,
    # quietly changing which history is exempted. An ambiguous exemption boundary is not a
    # boundary; it fails closed like a missing one.
    found = _FLOOR_RE.findall(text)
    if not found:
        raise AnchorError(
            f"no 'Dated disposition floor: `<sha>`' line found in {_ADR_PATH} -- the "
            "ADR-85 backstop cannot run without its ratified floor")
    if len(set(found)) > 1:
        raise AnchorError(
            f"{len(found)} DIFFERENT disposition floors declared in {_ADR_PATH} "
            f"({', '.join(sorted(set(found)))}) -- an ambiguous exemption boundary is not a "
            "boundary; resolve the ADR to exactly one")
    return found[0]


def _legacy_names(names: "list[str]") -> list[str]:
    """`JOURNAL-legacy-*.md` names from `names`, sorted -- date order by construction.

    The rotation convention is `JOURNAL-legacy-<span>.md` with an ISO-prefixed span, and the
    prefix is ENFORCED (`_LEGACY_RE`) rather than assumed -- which is what earns the claim that
    a plain lexical sort IS date order. Sorting explicitly (rather than trusting the order git
    or the filesystem hands back) is what makes the tiled read deterministic across platforms
    -- the same reasoning `silent_rule_detector` records for its own corpus ordering.

    HONEST LIMIT (terra HIGH, 2026-08-28, accepted rather than papered over): this discovers
    the tiles that ARE there. A tile that was rotated out and then DELETED is not detectable
    here, because nothing declares which tiles ought to exist -- and the failure is the bad
    direction, a SHRUNKEN anchoring universe reporting a false gap. Closing it needs a
    declared tile manifest, which is a design act with a governance cost; `[#608]` is scoped
    to a seam that moves zero bytes and takes no such act. Handed on as a candidate rather
    than silently owned.
    """
    return sorted(n for n in names if _LEGACY_RE.match(n))


def journal_text(repo: Path, rev: str | None = None) -> str:
    """The JOURNAL universe -- `JOURNAL.md` tiled with sorted `JOURNAL-legacy-*.md`.

    At `rev` when given, else the working tree. The pre-push organ reads it at the LOCAL TIP
    being pushed (the anchor commit is inside the range, so the working tree and the tip can
    differ); the audit backstop reads the working tree, which is what a ship-gate run is
    judging.

    TILING ([#608], ruling X5 -- rotate the FILE, not the PREDICATE). Both anchoring organs
    ask one question: does the JOURNAL name this SHA? Rotation must not change the answer, so
    the tiling happens HERE, at the single read both organs already share, rather than in a
    predicate either of them would have to be re-taught.

    ZERO BYTES MOVE when no legacy file exists, and that is a property rather than a
    coincidence: with an empty legacy list the return value is the single-file read, byte for
    byte -- no separator is introduced, no trailing newline is normalised. The seam is
    therefore inert until a rotation actually happens, which is exactly why it can land ahead
    of one. `test_tiled_read_is_byte_identical_with_no_legacy_files` pins that.

    A legacy file that exists but cannot be read is an ERROR, never a silent omission: a
    dropped tile silently SHRINKS the anchoring universe, which turns an anchored spine entry
    into a reported gap. Same fail-loud posture as the rest of this module.
    """
    if rev is None:
        try:
            names = _legacy_names([p.name for p in repo.iterdir() if p.is_file()])
        except OSError as exc:
            raise AnchorError(f"cannot enumerate {repo} for legacy journals: {exc!r}") from exc
        try:
            parts = [(repo / _JOURNAL).read_text(encoding="utf-8")]
            parts += [(repo / n).read_text(encoding="utf-8") for n in names]
        except OSError as exc:
            raise AnchorError(f"cannot read {_JOURNAL} (or a legacy tile): {exc!r}") from exc
    else:
        listing = _git(repo, "ls-tree", "--name-only", rev)
        names = _legacy_names(listing.splitlines())
        parts = [_git(repo, "show", f"{rev}:{_JOURNAL}")]
        parts += [_git(repo, "show", f"{rev}:{n}") for n in names]

    if len(parts) == 1:
        return parts[0]          # byte-identical to the pre-tiling read
    return "\n".join(parts)


def spine_entries(repo: Path, rev_range: str) -> list[str]:
    """First-parent spine entries in `rev_range`, newest-first.

    `rev_range` is any git log positional -- `A..B` for a push range, or a bare ref like
    `main` for the backstop. `--first-parent` is what makes this the SPINE (ADR-85 §A7:
    the anchored object is the spine entry, not every reachable commit).
    """
    out = _git(repo, "log", "--first-parent", "--format=%H", rev_range)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _introduced_uncached(repo: Path, sha: str) -> list[str]:
    """The uncached body of `introduced`. Two `git rev-list` reads, no memory.

    Kept as the FALLBACK and as the oracle after [#588] moved the fast path onto a batched
    parent map: it is the definition of the answer -- git's own -- and `_introduced_from_map`
    is only ever an optimisation of it, so anything the map cannot answer comes back here
    rather than being guessed at, and the parity tests compare against this and not against a
    restatement of the map.
    """
    parents = _git(repo, "rev-list", "--parents", "-n", "1", sha).split()
    if len(parents) < 2:          # root commit: no first parent
        return [sha]
    first_parent = parents[1]
    out = _git(repo, "rev-list", f"{first_parent}..{sha}")
    brought = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return brought or [sha]


# =========================================================================================
# [#588] ONE GIT PROCESS FOR THE WHOLE SPINE.
#
# WHAT WAS WRONG, and this module recorded it against itself before the fix existed (see
# `introduced`'s docstring): a single `audit.py health` run spawned 808 `git rev-list`
# processes at ~144 ms each -- 116.8 s. The [#533] memo removed the duplicate half; the
# per-unique-SHA pair remained, and the 2026-08-26 parity harness measured what was left at
# 82.6 s for 312 spine entries, i.e. essentially all of the residual cost of the #1 check.
# ~144 ms is a WINDOWS process-creation tax, which is why this dominates on the operator's
# host and would not on a Linux runner.
#
# THE BATCH. `git rev-list --parents --all` returns the ENTIRE parent map in ONE process.
# `firstparent..sha` is then a graph walk in Python: mark everything reachable from the first
# parent, then walk from `sha` and keep what the mark did not cover. Process count per health
# run goes from O(spine) to O(1).
#
# WHY `--all` AND NOT A REF. `introduced` takes a bare SHA and has no ref to walk from, and a
# map built per query would be the per-SHA spawn again under a new name. `--all` is ancestry-
# closed over every ref, so ONE map answers every SHA any caller in this repo can hand it.
#
# WHY THE MAP MAY BE TRUSTED ONCE BUILT -- the same immutability argument `introduced` already
# rests on, one level down: what a commit introduced is fixed forever by the commit's own hash,
# because its parents and their whole ancestry are part of what the hash commits to. So if
# `sha` is IN the map, the derived answer cannot go stale. If it is NOT, the map is simply
# older than the commit (a process that outlived a `git commit` -- a test, an operator
# mid-session), which is a MISS and not an error: rebuild once, then believe it. A SHA still
# absent after a fresh read is unreachable from every ref, and that falls back to git.
#
# ORDER IS OUTPUT, NOT AN IMPLEMENTATION DETAIL. `mention_not_record_warnings` emits one string
# per introduced commit IN THIS ORDER, and `check_journal_spine_anchor` joins the FIRST FIVE
# into its WARN evidence -- so reproducing git's order is part of the answer, not polish. The
# walk below is therefore git's own traversal rather than any convenient one: a commit-date
# priority queue seeded with `sha`, popping newest-first and breaking ties by insertion order,
# which is `commit_list_insert_by_date`'s rule (it inserts AFTER equal dates).
#
# THE ORDERING WAS GOT WRONG ONCE HERE, and the wrong version is recorded because it looked
# right: sorting the introduced set by each commit's index in the global `--all` output. That
# reproduces git whenever commit dates are distinct and DIVERGES the moment they tie -- and
# they tie constantly, because git stamps at one-second granularity and a scripted burst of
# commits lands inside one second. Measured on a synthetic repo whose commits share a
# timestamp: 3 of 5 spine entries came back in a different order, git putting the merge first
# where the global index did not. Distinct dates are what a hand-made repo has and a machine-
# made one does not, which is exactly the shape of bug that survives a green test suite.
# =========================================================================================

#: The ONE read. `--parents` puts the parents on each line and `--timestamp` prefixes the commit
#: date, so a single process yields BOTH the graph and the ordering key; `--all` makes it closed
#: over every ref, so a caller's SHA is present whenever it is reachable at all. Line shape:
#: `<commit-date> <sha> <parent>...`.
_PARENT_MAP_ARGS = ("rev-list", "--parents", "--timestamp", "--all")

#: Ceiling for `_parent_map`. One live process sees one repo (the audit runner, a git hook);
#: the suite sees a tmp repo at a time, and a rebuild-on-miss makes a SECOND entry for the same
#: repo, so the floor is 2 and 4 leaves headroom. Named for the `_ENTRIES_CACHE_MAXSIZE`
#: reason -- the memory it commits should be a stated number, not a literal buried in a
#: decorator. Measured on this repo (2026-08-26): 5,995 commits and 7,329 parent edges, order
#: 1 MB per entry. Megabytes rather than tens of megabytes, which is why this ceiling can be
#: generous where `_ENTRIES_CACHE_MAXSIZE`'s multi-MiB values force it tight.
_PARENT_MAP_CACHE_MAXSIZE = 4


class _SpineMap(NamedTuple):
    """`parents`: commit -> its parents, first parent first. `stamp`: commit -> commit date,
    which is the key git's own traversal orders by and therefore the key this one must."""
    parents: dict[str, tuple[str, ...]]
    stamp: dict[str, int]


#: Per-repo snapshot counter. Bumped only when a lookup misses, so a rebuild is caused by a
#: commit the snapshot predates rather than by a timer. Holds one small int per repo path
#: string seen in the process -- the one unbounded structure here, and deliberately the
#: cheapest thing to leave unbounded.
#:
#: THREADS, because this module runs inside one: `audit.run_checks` is a ThreadPoolExecutor and
#: `check_journal_spine_anchor` and `check_review_artifact_coverage` reach `introduced`
#: CONCURRENTLY in the same process. `lru_cache` is thread-safe, and the read-bump-read here is
#: not atomic -- but the worst a lost update can do is build the map twice, because the answer
#: is taken only after `sha in smap.parents` is re-checked against whichever map came back. An
#: extra git process, never a wrong answer.
_MAP_GENERATION: dict[str, int] = {}


@functools.lru_cache(maxsize=_PARENT_MAP_CACHE_MAXSIZE)
def _parent_map(repo_key: str, generation: int) -> _SpineMap:
    """The batched read, memoized per (repo, snapshot). `generation` is the cache-buster:
    it is not read inside, it exists so a rebuild is a different key.

    `lru_cache` does not cache exceptions, so an unreadable history re-reads and re-raises --
    the fail-CLOSED posture is untouched, exactly as for `_introduced_tuple`.
    """
    parents: dict[str, tuple[str, ...]] = {}
    stamp: dict[str, int] = {}
    for line in _git(Path(repo_key), *_PARENT_MAP_ARGS).splitlines():
        ids = line.split()
        if len(ids) < 2:          # blank line; `--timestamp` guarantees at least date + sha
            continue
        try:
            stamp[ids[1]] = int(ids[0])
        except ValueError as exc:
            # FAIL-LOUD, per this module's posture: an unparseable graph is an UNKNOWN
            # anchoring state, and an unknown state must never render as "anchored".
            raise AnchorError(
                f"unparseable `git {' '.join(_PARENT_MAP_ARGS)}` line: {line!r}") from exc
        parents[ids[1]] = tuple(ids[2:])
    return _SpineMap(parents, stamp)


def _spine_map_for(repo: Path, sha: str) -> _SpineMap | None:
    """The snapshot that contains `sha`, rebuilding ONCE on a miss -- or None if it is
    unreachable from every ref even after a fresh read.

    HONEST LIMIT, raised as a CRITICAL by the 2026-08-26 terra review and kept here with the
    measurement that sized it. A rebuild fires on a MISS, so a SHA already in the snapshot is
    answered from it for the life of the process. What a commit introduced is immutable in the
    OBJECT graph, but git reports a VIEW of that graph, and two things move a view: a shallow
    boundary being deepened, and `replace`/graft refs. So a view mutation INSIDE one process
    can make the snapshot disagree with a fresh `git rev-list`.

    Measured rather than argued, because the direction decides whether it matters
    (`tests/test_journal_anchor.py::test_a_shallow_clone_*`):

      * In a STATIC shallow clone the map and `_introduced_uncached` agree EXACTLY -- git's own
        `rev-list firstparent..sha` is truncated at the same boundary. The batch introduces no
        divergence; truncation is git's answer, not the map's.
      * Under a deepen mid-process the stale snapshot yields a set that is a SUBSET of the
        fresh one (2 missing, 0 extra on the fixture). `is_anchored` is `any(...)` over that
        set, so a subset can only turn TRUE into FALSE -- it over-reports UNANCHORED and
        BLOCKS. That is fail-CLOSED, the direction this module's whole posture demands, and
        the opposite of the "returns ANCHORED, lets an unanchored push through" the review
        described.

    Not closed in code, and the reason is that closing it would undo [#588]: detecting a view
    mutation needs a git read PER CALL, which is the per-SHA spawn the row exists to remove.
    The residual is a `replace`/graft ref created inside the seconds-long lifetime of a gate
    process -- and that window is not new: `_introduced_tuple`'s memo has fixed answers for a
    whole process since [#533].
    """
    key = str(repo)
    smap = _parent_map(key, _MAP_GENERATION.get(key, 0))
    if sha in smap.parents:
        return smap
    _MAP_GENERATION[key] = _MAP_GENERATION.get(key, 0) + 1
    smap = _parent_map(key, _MAP_GENERATION[key])
    return smap if sha in smap.parents else None


def _introduced_from_map(repo: Path, sha: str) -> list[str] | None:
    """`firstparent..sha` derived from the batched map -- or None, meaning "ask git".

    None is returned for every case the map cannot answer with certainty: an unreachable SHA,
    or a map that is not ancestry-closed where the walk needs it (a shape `--all` should not
    produce, so it defers rather than silently returning a too-large set -- a too-large
    introduced set would report a spine entry ANCHORED that is not).
    """
    smap = _spine_map_for(repo, sha)
    if smap is None:
        return None
    parents = smap.parents[sha]
    if not parents:               # root commit: no first parent, introduces only itself
        return [sha]

    excluded: set[str] = set()
    stack = [parents[0]]
    while stack:
        commit = stack.pop()
        if commit in excluded:
            continue
        known = smap.parents.get(commit)
        if known is None:
            return None           # not ancestry-closed here -- defer to git, never guess
        excluded.add(commit)
        stack.extend(known)

    # git's traversal, not a convenient one: a commit-date priority queue seeded with `sha`,
    # newest-first, ties broken by insertion order. `heapq` is a MIN-heap, so the key is
    # `(-date, seq)` -- `-date` pops the newest, and a rising `seq` makes the earlier-queued of
    # two equal-dated commits pop first, which is what `commit_list_insert_by_date` does by
    # inserting after equals. `queued` is git's ADDED flag: a commit enters the queue once, at
    # its first insertion, so a second child cannot re-order it.
    brought: list[str] = []
    queued: set[str] = {sha}
    heap = [(-smap.stamp[sha], 0, sha)]
    seq = 1
    while heap:
        _, _, commit = heapq.heappop(heap)
        known = smap.parents.get(commit)
        if known is None:
            return None
        brought.append(commit)
        for parent in known:
            if parent in excluded or parent in queued:
                continue
            if parent not in smap.stamp:
                return None
            queued.add(parent)
            heapq.heappush(heap, (-smap.stamp[parent], seq, parent))
            seq += 1
    return brought or [sha]


@functools.lru_cache(maxsize=_INTRODUCED_CACHE_MAXSIZE)
def _introduced_tuple(repo_key: str, sha: str) -> tuple[str, ...]:
    """The memoized answer for an IMMUTABLE key. Guarded by `introduced` below.

    `repo_key` is `str(repo)` rather than a `Path`: two spellings of the same directory are
    two keys, which costs a miss and never a wrong answer, whereas resolving the path on every
    call would add a syscall to a function whose entire purpose is to avoid work.

    `lru_cache` does NOT cache exceptions, so an `AnchorError` from an unreadable history is
    re-raised from a real git read every time -- the fail-CLOSED posture is untouched.

    Served from the [#588] batched parent map, falling back to the two-spawn `git` body for
    anything the map cannot answer. The memo is kept ON TOP of the map rather than replaced by
    it: the map removes the process spawns, the memo removes the graph walk.
    """
    repo = Path(repo_key)
    brought = _introduced_from_map(repo, sha)
    if brought is None:
        return tuple(_introduced_uncached(repo, sha))
    return tuple(brought)


def introduced(repo: Path, sha: str) -> list[str]:
    """The commits a spine entry INTRODUCED: `firstparent..sha`, plus the entry itself.

    For a `--no-ff` merge this is the merge plus every commit the merged branch brought
    in -- which is where the branch's JOURNAL anchor lives. For a non-merge spine entry
    (§A9) it is just the entry: structurally unanchorable at push time, since no JOURNAL
    can name a SHA that does not yet exist. A root commit has no first parent and likewise
    introduces only itself.

    MEMOIZED, BUT ONLY ON A FULL 40-HEX SHA ([#533] leg 2). What a commit introduced is
    fixed forever by the commit's own hash -- its parents, and their ancestry, are part of
    what the hash commits to -- so for a full SHA this answer cannot go stale and the memo is
    safe by construction, not by policy. A REF is a different matter: `main` moves, so a
    `main`-keyed entry could outlive its own truth, and any argument other than a full SHA
    therefore bypasses the cache entirely rather than being cached under a caveat. Callers in
    this repo pass `%H` from `spine_entries`, so the fast path is the one that runs.

    WHY IT EXISTS, measured rather than assumed ([#533] leg 2, STEP 1): a single
    `audit.py health` run called this 404 times and spawned 808 `git rev-list` processes at
    ~144 ms each, 116.8 s in all -- because `check_journal_spine_anchor` reaches it TWICE for
    every spine entry, once via `unanchored_on_spine -> is_anchored` and again via
    `mention_not_record_warnings`. About half of those spawns recomputed an answer the process
    already held. `check_review_artifact_coverage` walks the same spine and calls it again.

    Returns a fresh `list` so a caller mutating the result cannot corrupt later readers.
    """
    if not _FULL_SHA_RE.match(sha):
        return _introduced_uncached(repo, sha)
    return list(_introduced_tuple(str(repo), sha))


# Cache-management surface, forwarded for the same reason as `_entries`'.
introduced.cache_info = _introduced_tuple.cache_info
introduced.cache_clear = _introduced_tuple.cache_clear


def is_anchored(repo: Path, sha: str, journal: str) -> bool:
    """True iff `journal` names >= 1 SHA the spine entry `sha` introduced (§A7).

    Answered from `_anchor_index` (defined below, with the WARN machinery that shares it) --
    ONE pass over the journal per distinct text, memoized, instead of a fresh substring scan of
    a ~2.9 MB string per introduced commit ([#587]). The index holds every 7-char lowercase-hex
    substring the journal contains, so `short in index.present` is the SAME question
    `short in journal` asked; a short that is not an object-name prefix is outside the index's
    domain by construction and falls back to the original raw test, so the answer is identical
    for every input rather than only for the inputs today's callers produce.
    """
    index = _anchor_index(journal)
    return any((c[:_SHORT] in index.present) if _SHORT_HEX_RE.match(c[:_SHORT])
               else (c[:_SHORT] in journal)
               for c in introduced(repo, sha))


def unanchored_in_range(repo: Path, rev_range: str, journal: str) -> list[str]:
    """Spine entries in `rev_range` that no JOURNAL text anchors -- newest-first.

    NOTE the asymmetry with `unanchored_on_spine`, and it is intentional per FR2: the
    pre-push organ's discharge is RANGE-level ("a JOURNAL entry naming >= 1 SHA in that
    range"), so callers treat a non-empty return as a refusal only when NO entry in the
    range is anchored. This function reports per-entry facts; the range verdict is
    `range_is_anchored` below, so the two rules cannot drift apart in a caller.
    """
    return [s for s in spine_entries(repo, rev_range) if not is_anchored(repo, s, journal)]


def range_is_anchored(repo: Path, rev_range: str, journal: str) -> bool:
    """FR2's range-level discharge: >= 1 spine entry in the range is anchored.

    An empty range is vacuously anchored -- there is nothing being integrated, so there is
    no obligation (§A1: the obligation is created by integration, not by authorship).
    """
    entries = spine_entries(repo, rev_range)
    if not entries:
        return True
    return any(is_anchored(repo, s, journal) for s in entries)


def unanchored_on_spine(repo: Path, ref: str, floor: str, journal: str) -> list[str]:
    """Backstop scan (FR4): unanchored spine entries on `ref` at/above the dated `floor`.

    Per-entry, not range-level: the backstop's job is to make a `--no-verify` bypass
    visible after the fact, so it asks the stricter question of every entry above the
    floor. Entries strictly older than `floor` are dispositioned once by the ADR-85
    amendment §A8 and are not scanned.

    Raises AnchorError when `floor` is not an ancestor of `ref` -- an unverifiable floor is
    an error, never an empty (clean-looking) result.
    """
    try:
        _git(repo, "merge-base", "--is-ancestor", floor, ref)
    except AnchorError as exc:
        raise AnchorError(
            f"disposition floor {floor[:9]} is not an ancestor of {ref}: {exc}") from exc
    entries = spine_entries(repo, f"{floor}..{ref}")
    floor_full = _git(repo, "rev-parse", floor).strip()
    entries = [s for s in entries if s != floor_full]
    return [s for s in entries if not is_anchored(repo, s, journal)]


# N2-L5 (#524 leg c): "anchored by mention, not by record" WARN. `is_anchored` above is the
# HARD predicate (§A7: a SHA occurring anywhere in JOURNAL text) and stays unchanged -- this
# is a strictly weaker, advisory question layered on top: among the SHAs that satisfy
# `is_anchored`, which were only ever MENTIONED in prose (e.g. "Confirmed ... `59d05dd0` ...
# recorded here only to discharge the shared spine-anchor gate", the live 2026-08-13 (d)
# shape) versus explicitly RECORDED on a declarative line -- this repo's own live convention,
# e.g. "**Anchors:** `b8f4004`." or "Anchors this arc's own spine: `52d230cc` ...". A WARN by
# design (STANDING_RULINGS L-10): it catches the SHAPE (no record line), not the INTENT (a
# mention can be a legitimate, deliberate discharge, per repo convention) -- so it never
# changes `is_anchored` or the hard pass/fail verdict, only flags the weaker shape for a
# human's second look.
_RECORD_LINE_RE = re.compile(r"^\*{0,2}Anchors?\b", re.IGNORECASE)
_ENTRY_SPLIT_RE = re.compile(r"(?=^### )", re.MULTILINE)

# Ceiling for the `_entries_tuple` memo. Named rather than inlined so the memory it commits is
# a stated number: a live run holds at most two distinct journal texts (the working tree, plus a
# `rev` when the pre-push organ reads the tip it is pushing), so 4 leaves headroom without
# letting a pathological caller pin an unbounded number of multi-megabyte strings.
_ENTRIES_CACHE_MAXSIZE = 4


@functools.lru_cache(maxsize=_ENTRIES_CACHE_MAXSIZE)
def _entries_tuple(journal: str) -> tuple[str, ...]:
    """The memoized split. Returns a TUPLE so the cached object cannot be mutated in place.

    KEYED ON THE JOURNAL TEXT, deliberately -- not on a path, an mtime or a run counter. That
    choice is what makes the memo safe rather than merely fast: a journal that has grown is a
    DIFFERENT key, so a grown file cannot register a hit against the old entries. There is
    nothing to invalidate, so there is no invalidation to get wrong. ([#533] leg 2, STEP 3.)

    Hashing a ~2.6 MiB key is not the cost it looks like: CPython memoizes `str.__hash__` on
    the object, and every call in the hot loop passes the SAME string object -- the one
    `check_journal_spine_anchor` read once -- so the hash is computed once and the dict lookup
    then short-circuits on pointer identity.

    Bounded on purpose (`_ENTRIES_CACHE_MAXSIZE`): the key is ~2.6 MiB and the value is another
    ~2.6 MiB of fresh strings, and the audit runner holds ONE process across all 43 checks. An
    unbounded cache here would be a leak dressed as an optimization. A live run sees at most two
    distinct texts (the working tree, and a `rev` for the pre-push organ), so a small ceiling
    costs nothing and caps the worst case.
    """
    return tuple(p for p in _ENTRY_SPLIT_RE.split(journal) if p.strip())


def _entries(journal: str) -> list[str]:
    """JOURNAL text split into per-entry chunks at `### ` headings (order-preserving).

    Memoized via `_entries_tuple`. The public shape is unchanged -- a fresh `list[str]`, so no
    caller sees a behaviour change and no caller can corrupt the cache for every later reader by
    mutating what it got back. Copying ~1.3k pointers is free next to re-running the split.

    WHY THE MEMO EXISTS, measured rather than assumed ([#533] leg 2, STEP 1): the ADR-85
    backstop called this 934 times in a single `audit.py health` run, re-splitting the same
    immutable 2607 KiB `JOURNAL.md` every time -- 2.47 GB of regex for one answer, 76.9 s, 37%
    of `check_journal_spine_anchor` and 23% of the whole 43-check loop.
    """
    return list(_entries_tuple(journal))


# The cache-management surface, forwarded onto `_entries` so a caller reasons about the memo
# through the function it actually calls instead of reaching past it into a private helper.
_entries.cache_info = _entries_tuple.cache_info
_entries.cache_clear = _entries_tuple.cache_clear


# =========================================================================================
# [#587] THE SINGLE-PASS ANCHOR INDEX -- the inversion, and the whole point of this section.
#
# WHAT WAS WRONG, measured rather than assumed (PERF-RECON 2026-08-26, B1/B3; telemetry run
# f0caf15a, `check_journal_spine_anchor` = 197.8 s, rank 1 of 46 and 35% of the health loop):
# both consumers below asked their question ONCE PER INTRODUCED COMMIT, and each asking
# re-walked the whole journal. `mention_not_record_warnings` looped introduced-commit -> entry
# -> `entry.splitlines()` -> substring test per line; `_entries` was memoized ([#533]) but
# `.splitlines()` was NOT, so every outer iteration re-split and re-allocated 2.9 MB. Over this
# repo's 312 spine entries above the floor and the ~5k commits they introduce, that is tens of
# GB of line-splitting for one advisory list. `is_anchored` had the same shape one layer down:
# a substring scan of the same 2.9 MB string per introduced commit.
#
# THE INVERSION. The journal does not change while a scan runs, so the direction is backwards:
# read it ONCE and build {short -> (present, recorded)}, then answer every commit's question
# with a set lookup. Cost goes from O(commits x journal) to O(journal) + O(commits).
#
# WHY IT IS SAFE, on exactly the [#533] argument this module already rests on: the index is
# keyed on the journal TEXT. A journal that has grown is a DIFFERENT key, so a grown file
# cannot register a hit against a stale index. There is nothing to invalidate, so there is no
# invalidation to get wrong -- and a stale anchor answer is worse than a slow one, because it
# produces false push-gate verdicts.
#
# WHY IT IS EQUIVALENT, and not merely similar. The keys are every 7-char LOWERCASE-HEX
# substring of the journal, which is exactly the domain of the `short in <text>` test it
# replaces: a 7-char lowercase-hex needle can only occur inside a maximal hex run of length
# >= 7, so enumerating those runs' windows enumerates every possible match and nothing else.
# Line-level classification is preserved because the index walks the same `_entries(journal)`
# -> `entry.splitlines()` sequence the old inner loop walked, so the two see the SAME lines.
# A needle that is not an object-name prefix is outside this domain: both consumers fall back
# to their own pre-inversion scan for it rather than reporting a confident "absent".
# =========================================================================================

#: A maximal run of lowercase hex. `finditer` over the runs, then a sliding window inside each,
#: enumerates every 7-char hex substring of a line -- including the ones that straddle no token
#: boundary (`0badf00d` contains `0badf00` AND `badf00d`), which is what keeps this identical to
#: a substring test rather than to a tokenizer. Prose can qualify (`defaced` is seven hex
#: letters); that is correct, because the test being replaced would have matched it too.
_HEX_RUN_RE = re.compile(rf"[0-9a-f]{{{_SHORT},}}")

#: Is this needle inside the index's domain at all? Callers pass `c[:_SHORT]` where `c` came
#: from `introduced` -- a git object name -- so the fast path is the one that runs.
_SHORT_HEX_RE = re.compile(rf"^[0-9a-f]{{{_SHORT}}}$")

#: Ceiling for `_anchor_index_tuple`, the same number and the same reasoning as
#: `_ENTRIES_CACHE_MAXSIZE`: a live run holds at most two distinct journal texts (the working
#: tree, plus a `rev` when the pre-push organ reads the tip it is pushing). Measured on the live
#: corpus (2,952,618 bytes of JOURNAL.md, 2026-08-26): 5,278 `present` keys and 457 `recorded`,
#: order 0.4 MB -- an order of magnitude under the ~5 MiB `_entries` commits for the same text,
#: because this holds 7-char windows and that holds the whole file twice over.
_ANCHOR_INDEX_CACHE_MAXSIZE = 4


class _AnchorIndex(NamedTuple):
    """Every 7-char hex substring of a journal, split by the line class it was seen on.

    `present` -- seen on ANY line. `recorded` -- seen on at least one explicit record line
    (`_RECORD_LINE_RE`). The old code's third state, `mentioned` ("seen on at least one
    NON-record line"), is not stored because it is not needed: the only question asked of it
    is `mentioned and not recorded`, and `present - recorded` is exactly that set. A short in
    `present` but not in `recorded` has every one of its occurrences on non-record lines, so it
    was mentioned; a short that was mentioned is by definition present.

    Frozensets, so the memoized object cannot be mutated by a caller -- the hazard `_entries`
    answers by copying, answered here by immutability instead.
    """
    present: frozenset[str]
    recorded: frozenset[str]


def _hex_shorts(line: str) -> set[str]:
    """Every 7-char lowercase-hex substring of `line` (empty set for the overwhelming majority
    of lines, which contain no hex run that long)."""
    shorts: set[str] = set()
    for m in _HEX_RUN_RE.finditer(line):
        run = m.group()
        for i in range(len(run) - _SHORT + 1):
            shorts.add(run[i:i + _SHORT])
    return shorts


@functools.lru_cache(maxsize=_ANCHOR_INDEX_CACHE_MAXSIZE)
def _anchor_index_tuple(journal: str) -> _AnchorIndex:
    """The memoized single pass. Keyed on the journal TEXT for the `_entries_tuple` reason."""
    present: set[str] = set()
    recorded: set[str] = set()
    for entry in _entries(journal):
        for line in entry.splitlines():
            shorts = _hex_shorts(line)
            if not shorts:
                continue
            present |= shorts
            if _RECORD_LINE_RE.match(line.strip()):
                recorded |= shorts
    return _AnchorIndex(frozenset(present), frozenset(recorded))


def _anchor_index(journal: str) -> _AnchorIndex:
    """`_anchor_index_tuple` under the name callers use, mirroring `_entries`' shape.

    No defensive copy, because there is nothing a caller could corrupt: the fields are
    frozensets and the container is a NamedTuple.
    """
    return _anchor_index_tuple(journal)


# The cache-management surface, forwarded for the same reason as `_entries`': a caller reasons
# about the memo through the function it actually calls.
_anchor_index.cache_info = _anchor_index_tuple.cache_info
_anchor_index.cache_clear = _anchor_index_tuple.cache_clear


def _scan_short_uncached(journal: str, short: str) -> tuple[bool, bool]:
    """`(present, recorded)` for a needle OUTSIDE the index's hex domain -- the pre-inversion
    inner loop, verbatim in behaviour, kept so the fallback is identical rather than merely
    close. Unreachable from any caller in this repo (`introduced` yields git object names);
    it exists so the equivalence claim above is total, not conditional."""
    present = recorded = False
    for entry in _entries(journal):
        for line in entry.splitlines():
            if short not in line:
                continue
            present = True
            if _RECORD_LINE_RE.match(line.strip()):
                recorded = True
    return present, recorded


def mention_not_record_warnings(repo: Path, sha: str, journal: str) -> list[str]:
    """Advisory strings, one per introduced commit of `sha` that is `is_anchored` (mentioned
    somewhere in `journal`) but never appears on an explicit record line (`_RECORD_LINE_RE`)
    anywhere in `journal`. Never raises -- a scan of already-fetched text, not a git read.

    Reads the [#587] single-pass index instead of re-walking the journal per commit. Order is
    preserved (it follows `introduced`) and so are the strings, byte for byte: the check joins
    the FIRST FIVE of these into its WARN evidence, so the order of this list is load-bearing
    output, not an implementation detail.
    """
    index = _anchor_index(journal)
    warnings = []
    for c in introduced(repo, sha):
        short = c[:_SHORT]
        if _SHORT_HEX_RE.match(short):
            present, recorded = short in index.present, short in index.recorded
        else:
            present, recorded = _scan_short_uncached(journal, short)
        if present and not recorded:
            warnings.append(
                f"anchored by mention, not by record: {short} appears outside an "
                "explicit 'Anchors:' record line")
    return warnings


def describe(repo: Path, sha: str) -> str:
    """`<short> (<date>) <subject>` for an operator-facing refusal line."""
    try:
        return _git(repo, "log", "-1", "--format=%h (%ad) %s", "--date=short", sha).strip()
    except AnchorError:
        return sha[:9]
