#!/usr/bin/env python
"""batch_manifest.py — the ADR-110 declared-integration-arc exemption (amendment 2026-08-07).

WHAT THIS EXISTS FOR (batch-1 F1). A batch's JOURNAL entry names the lane MERGE SHAs, so it
is writable only AFTER the merges. Each merge meanwhile lands an unanchored first-parent
spine entry, and `audit-health` evaluates PER-COMMIT. Anchoring is retrospective; the
commit-time backstop is not. Between merges the two cannot both be satisfied, and batch 1
resolved it with `SKIP=audit-health` — which disables EVERY check in the registry, not the
one that cannot pass, at the exact moment the protocol makes it fire. At width 6 that is
five times per batch.

THE EXEMPTION. A first-parent spine entry is exempt from `check_journal_spine_anchor` when
BOTH hold:

  1. it is a `--no-ff` merge of a branch matching the RATIFIED lane grammar
     `worktree-lane-<letter>-<id>-<slug>` -- `validate_branch_naming.LANE_BRANCH_RE`, imported,
     the single definition of that grammar in the repo ([#514]), AND
  2. a committed batch manifest declares an OPEN batch.

Neither alone. Condition 1 without 2 would exempt any lane merge forever; condition 2
without 1 would amnesty every merge landed during a batch, including the integrator's own.

WHY A MANIFEST IS THE KEY. It is the only artifact that makes "a batch is open" a FACT IN
THE TREE rather than a claim in a chat — and it is the same artifact Ch8 already requires at
dispatch, so the exemption costs no new ceremony.

HOW OPENNESS EXPIRES, and why it is NOT a mutable `status:` flag. Manifests live under
`docs/audits/`, which is IMMUTABLE (CLAUDE.md §5 rule 3) — an exemption whose expiry
required editing an immutable artifact would either never expire or corrupt the record. So
the manifest names, at dispatch, the artifact that will CLOSE it (`closed_by:`), and the
batch is open only while that path is ABSENT from the COMMITTED tree. The end-of-batch packet landing
is what ends the exemption, automatically, with no edit anywhere. Extending an exemption
therefore takes a visible act — deleting the packet, or committing a new manifest — never
silence. A manifest carrying no `closed_by:` opens nothing at all, because an exemption with
no declared expiry is the permanent hole the draft's own honest-limit warns about.

WHAT IS DELIBERATELY UNCHANGED (the draft's safety argument, and the reason nothing ships
unanchored): the range-level pre-push organ `block_unanchored_push.py` and the shared
predicate `journal_anchor.py` do NOT import this module and never consult a manifest. The
push-time refusal stays unconditional; only the commit-time verdict about an
already-declared, still-open batch is deferred to the boundary where the JOURNAL can
actually name the merges. `tests/test_batch_manifest.py` asserts the non-import on the AST.

HONEST LIMITS, four, none of them hidden:
  * The merged-branch name is read from the MERGE SUBJECT (`Merge branch 'x'`), which is what
    `git merge --no-ff` writes and what `/lane-integrate` produces. A hand-written merge
    message that omits the branch name is not recognised as a lane merge — it fails CLOSED
    (no exemption), which is the safe direction.
  * SCOPE, as of [#514]/[#510] W1 — NARROWED, NOT CLOSED, and the difference is the point.
    The exemption now covers only branches matching the RATIFIED lane grammar
    `worktree-lane-<letter>-<id>-<slug>` (the imported `LANE_BRANCH_RE`), where it previously
    covered any `worktree-lane-*` shape at all. Measured on main's first-parent spine, that is
    9 of 16 historical lane-shaped merges no longer qualifying. What it is STILL not scoped to
    is the roster of lanes the open manifest ENUMERATES: any conforming lane branch qualifies
    while a batch is open, so the self-grant `[#510]` describes — *"one `git branch -m` away"* —
    is made harder to reach by accident, not impossible to reach on purpose. Closing it needs a
    machine-readable roster FIELD on the manifest, which in turn needs `PLAYBOOK.md` Ch8 and the
    manifest template to carry it; shipping the field without those carriers would be exactly
    the half-landed adoption `[#513]` exists to detect, so `[#510]` stays OPEN on that leg
    rather than being closed on this one.
  * The grammar is enforced NOWHERE AT PROVISIONING. `validate_branch_naming` is read-only and
    wired into no gate (its own posture note), and a batch lane dispatched straight through
    `claude --worktree <name>` never passes `/lane-boot` step 1. So an off-enum lane name is
    still creatable; what changed is that it now silently gets NO exemption instead of silently
    getting one. That direction is the safe one — a missing exemption is a loud gate FAIL at the
    integrator's first merge, not a hole — but it is a trade, and it is stated rather than
    implied.
  * This adds a second exemption surface to a gate whose value is having none. Recorded in
    the ADR-110 amendment as an accepted cost, weighed against a standing instruction to turn
    the whole registry off twice per batch.

EVERY INPUT IS READ FROM `HEAD`, NEVER FROM THE WORKING TREE (terra HIGH ×2, 2026-08-07).
The manifest list, the manifest CONTENT, and the closing packet's existence all resolve
through git plumbing against the committed tree. The first attempt at this used a working-tree
glob (any file, committed or not, granted the exemption); the second used `git ls-files` for
tracked-ness but still read content off disk — and `ls-files` is satisfied by a merely STAGED
addition, so a staged manifest or an unstaged edit to a committed one still declared a batch
open. The rule says COMMITTED, and only a HEAD-based read means it.

Layer-2 contract (ADR-28/36): READ-ONLY. Filesystem reads and git plumbing reads only.
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Mapping, NamedTuple, Optional

# The [#355] git-env scrub, single-sourced in the LEAF module `scripts/gitenv.py` ([#396]).
# A leaf — stdlib-only, zero repo imports — so this adds no import edge that could reach the
# pre-push organ; the containment property this module's own tests assert is unaffected.
#
# Loaded BY PATH, never by name -- every name-based spelling has a shadow hole that silently
# empties the scrub, which would re-open [#512] through the module that closes it. Full
# argument and the two reproductions are in gitenv.py's docstring.
_gitenv_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_gitenv", Path(__file__).resolve().with_name("gitenv.py"))
_gitenv = importlib.util.module_from_spec(_gitenv_spec)
_gitenv_spec.loader.exec_module(_gitenv)

#: Where a batch manifest lives and what it is called. The `-manifest` suffix keeps it
#: distinguishable from the end-of-batch packet that closes it, and the ADR-101 class token
#: (`-technical-`) is what lets it exist under `docs/audits/` at all.
MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"

#: The lane-branch shape the exemption covers -- THE ENUM'S OWN CONSTANT, imported, never a
#: second spelling of it ([#514]). A REFINEMENT of `worktree-<name>` (Ch8), so it needs no new
#: prefix-enum ruling to exist.
#:
#: This module used to define its own, looser rival: `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`.
#: Two constants shared one name and one purpose and disagreed on grammar, so the exemption rode
#: the loose one while `validate_branch_naming.classify` called the same branches `unknown` --
#: both organs could not be enforced. Re-measured on this branch over every lane-shaped merge on
#: main's first-parent spine: 16 merges, loose matches 16, strict matches 7, DISAGREE 9/16.
#:
#: Imported BY NAME rather than through the by-path loader used for `gitenv` above, because the
#: object identity a name-import preserves is what lets a test assert that this module and the
#: enum module hold the SAME regex -- a by-path load builds a second module object and defeats
#: that pin by construction.
#:
#: THE SHADOW HOLE THAT BUYS, AND THE GUARD THAT CLOSES IT (terra HIGH, 2026-08-11). The first
#: version of this comment claimed the identity test also catches a shadowed
#: `validate_branch_naming`. IT DOES NOT, and the claim was reproduced false: preload any module
#: under that name into `sys.modules` and BOTH this module and the test receive the shadow, so
#: `bm.LANE_BRANCH_RE is vbn.LANE_BRANCH_RE` still holds while a LOOSE regex silently governs the
#: exemption -- the `gitenv` failure mode exactly, arriving through the door left open by the
#: argument that it could not. So provenance is checked here instead of asserted in prose: the
#: resolved module has to be this file's own sibling, and anything else raises at import. That
#: is the loud failure the earlier comment promised -- `audit.py`'s FR6 `except` renders it as a
#: `journal_spine_anchor` FAIL, never a silent pass. Regression: the subprocess shadow test in
#: `tests/test_batch_manifest.py`.
import validate_branch_naming as _vbn   # noqa: E402  (after the by-path gitenv load)
# RE-EXPORTED, not used here any more: `is_lane_merge` reads the whole lane SET, but the
# batch-lane GRAMMAR is still what `tests/test_batch_manifest.py` compares against when it
# pins that no rival regex has been reintroduced, and it is still the shape a seeded
# worktree carries. Dropping the name would delete that test's subject, not tidy an import.
from validate_branch_naming import LANE_BRANCH_RE   # noqa: E402,F401
from validate_branch_naming import is_lane_branch  # noqa: E402

if Path(getattr(_vbn, "__file__", "") or "").resolve().parent != Path(__file__).resolve().parent:
    raise ImportError(
        f"validate_branch_naming resolved to {getattr(_vbn, '__file__', None)!r}, which is not "
        f"this module's sibling in {Path(__file__).resolve().parent}. Refusing to import a "
        f"shadowed lane grammar: the ADR-110 exemption would be decided by an unknown regex "
        f"([#514]).")

#: `[#630]`'s Refusal shape and slug reader -- imported BY NAME, no by-path/provenance guard.
#: `validate_substrate` does not import `batch_manifest` (checked: no cycle), and there is no
#: shadow-hole argument to make here the way there was for `LANE_BRANCH_RE` -- that guard
#: exists because a shadowed ENUM silently governs an EXEMPTION; a shadowed `Refusal`/
#: `contract_slug` would break loudly (an `AttributeError` or a wrong-shaped object) rather
#: than silently widen anything.
from validate_substrate import Refusal, contract_slug   # noqa: E402

#: The ADR-101 audit-name grammar's ruled CLASS ENUM, imported BY NAME from the module that
#: owns it. `validate_hermetization` does not import this module (checked: no cycle) and pulls
#: only stdlib, so this is cheap.
#:
#: PROVENANCE-GUARDED, on the `LANE_BRANCH_RE` precedent above and for that comment's exact
#: reason: a shadowed ENUM silently governs an EXEMPTION. Widen this enum and
#: `2026-09-05-technical-review-of-lane-g-276-deploy-waiver` splits at a longer class, its tail
#: becomes `lane-g-276-...`, and a document ABOUT a lane is admitted as that lane's own
#: artifact -- the precise false coverage `links_artifact`'s anchor exists to refuse. A shadow
#: that NARROWS is harmless (the single-segment fallback below IS the pre-enum behaviour), so
#: the hole is one-directional; the guard is not, because "only the widening direction is
#: dangerous" is an argument about today's enum, not a property of the seam.
import validate_hermetization as _vh   # noqa: E402
from validate_hermetization import AUDIT_CLASS_ENUM   # noqa: E402

if Path(getattr(_vh, "__file__", "") or "").resolve().parent != Path(__file__).resolve().parent:
    raise ImportError(
        f"validate_hermetization resolved to {getattr(_vh, '__file__', None)!r}, which is not "
        f"this module's sibling in {Path(__file__).resolve().parent}. Refusing to import a "
        f"shadowed audit-class enum: the manifest-link exemption would be decided by an "
        f"unknown class grammar.")

#: `git merge --no-ff <branch>` writes this subject; `/lane-integrate` relies on it too.
_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")

#: A full 40-hex object name. The memo below admits nothing shorter, for the reason
#: `journal_anchor` records against the same constant there: an abbreviation is a query, not
#: an identity, and the commit it names can change as history grows.
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


class OpenBatch(NamedTuple):
    """One manifest declaring a batch that is open right now."""
    batch: str
    path: str
    closed_by: str


def _frontmatter(text: str) -> dict[str, str]:
    """Flat `key: value` frontmatter, lowercased keys, stripped values.

    Deliberately NOT a YAML parse: the three fields consumed here are scalars, and taking a
    yaml dependency into a gate path to read three strings buys nothing. Unparseable input
    yields `{}`, which opens no batch.

    INLINE COMMENTS ARE STRIPPED (terra HIGH, 2026-08-07). `closed_by: docs/x.md  # later`
    would otherwise carry the comment into the path, which then never resolves on disk — and a
    `closed_by` that can never resolve is a NON-EXPIRING exemption. Only an unquoted ` #` is
    treated as a comment, so a legitimate `#` inside a quoted value survives.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if not (v.startswith(('"', "'"))):
            v = re.split(r"\s+#", v, maxsplit=1)[0].strip()
        out[k.strip().lower()] = v.strip('"').strip("'")
    return out


def _valid_closer(closed_by: str) -> bool:
    """Is `closed_by` a shape that CAN resolve, and therefore CAN expire the exemption?

    The whole safety of the exemption rests on the closer eventually existing. A value that
    can never resolve to a real in-repo path — absolute, drive-lettered, escaping via `..`,
    or outside `docs/audits/` — would grant a permanent exemption while looking well-formed
    (terra HIGH, 2026-08-07). Rejected here, which means the manifest opens NOTHING rather
    than opening something that never closes.
    """
    if not closed_by or closed_by != closed_by.strip():
        return False
    p = PurePosixPath(closed_by.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts or ":" in closed_by:
        return False
    return p.parts[:2] == ("docs", "audits") and p.suffix == ".md"


def _git(repo_path: Path, *args: str) -> Optional[str]:
    """Read-only git in a SCRUBBED env, or None on any failure. None always reduces to
    "no exemption".

    The `env=` is [#512], and it is not cosmetic. `GIT_DIR` overrides BOTH `cwd=` and the
    `-C` above, so a caller that inherited one — a hook, a nested invocation — read a
    FOREIGN repo through this helper and got `None`/empty back for every probe. Every such
    answer reduces to "no batch is open", which is the SAFE direction for the exemption but
    the UNSAFE one for `gen_handoff`'s open-batch refusal: the refusal that protects a
    handoff cut mid-batch silently saw nothing to refuse. Same [#355] class, fourth call
    site — it was the only git caller in this fleet's batch machinery with no scrub at all.

    Read-only and None-on-failure are unchanged; only the environment the probe runs in is.
    """
    try:
        r = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=15,
                           env=_gitenv.scrubbed_git_env())
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _committed_audits(repo_path: Path) -> Optional[set[str]]:
    """Every path committed under `docs/audits/` at HEAD, or None when git could not answer.

    P2 (intake #71): ONE `ls-tree` already answers both questions `open_batches` asks of the
    tree -- which manifests exist, and whether a given `closed_by:` packet exists. The listing
    was previously filtered to manifests and the rest thrown away, so each `closed_by:` probe
    paid its own `git cat-file -e` spawn. Returning the whole set costs nothing extra and
    makes `_closer_committed` a membership test.

    None (git failed) is kept DISTINCT from the empty set, because the two must reduce
    differently: an unreadable tree may not be read as "the packet is absent, so the batch is
    open". Every caller below preserves that distinction; the module's fail-toward-no-exemption
    posture depends on it.
    """
    out = _git(repo_path, "ls-tree", "-r", "--name-only", "HEAD", "--", "docs/audits/")
    if out is None:
        return None
    return {p.strip() for p in out.splitlines() if p.strip()}


def _manifests_in(paths: set[str]) -> list[str]:
    """The manifest-grammar members of `paths`, oldest path first."""
    pat = MANIFEST_GLOB.split("/")[-1]
    return sorted(p for p in paths if PurePosixPath(p).match(pat))


def _committed_manifests(repo_path: Path) -> list[str]:
    """Manifest paths present in the COMMITTED tree at HEAD, matching the manifest grammar."""
    paths = _committed_audits(repo_path)
    return [] if paths is None else _manifests_in(paths)


def _committed_text(repo_path: Path, rel: str) -> Optional[str]:
    """The blob at `HEAD:<rel>`, or None. Reading the COMMITTED blob is the whole point.

    EVERYTHING HERE IS HEAD-BASED, and the second terra HIGH of 2026-08-07 is why. The first
    fix used `git ls-files` (tracked-ness) and still read CONTENT from the working tree —
    which `ls-files` also satisfies for a merely STAGED addition. So a staged-but-uncommitted
    manifest, or an unstaged edit to a committed one, could still declare a batch open. The
    rule says COMMITTED; the only implementation that means it reads the committed blob.
    """
    return _git(repo_path, "show", f"HEAD:{rel}")


def _committed_texts(repo_path: Path, rels: list[str]) -> dict[str, Optional[str]]:
    """`{rel: blob text at HEAD}` for every `rel`, in ONE `git cat-file --batch` spawn.

    P2 (intake #71): `open_batches` read one blob per committed manifest, one `git show`
    each. `--batch` is git's own answer to exactly that shape -- it takes the names on stdin
    and streams the objects back -- so N spawns become 1 with no change to what is read.

    DECODING IS MATCHED TO `_committed_text`, NOT CHOSEN AFRESH, because a verdict must not
    move when its transport does. That helper reads through `subprocess` in TEXT mode, which
    is `utf-8` + `errors="replace"` + UNIVERSAL NEWLINES; `--batch` hands back raw bytes, so
    both the decode and the newline translation are reapplied here by hand. Skipping the
    newline half would leave `\\r` on the end of every frontmatter value on a CRLF checkout
    and quietly stop `status: open` from ever matching -- the batch would read as closed and
    the exemption would vanish. Any object git reports `missing` maps to None, the same value
    an unreadable `git show` produced.

    Falls back to the per-blob path on any transport failure, so this is a speed change and
    never a new failure mode.
    """
    if not rels:
        return {}
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_path), "cat-file", "--batch"],
            input="".join(f"HEAD:{r}\n" for r in rels).encode("utf-8"),
            capture_output=True, timeout=60, env=_gitenv.scrubbed_git_env())
    except (OSError, subprocess.SubprocessError):
        proc = None
    if proc is None or proc.returncode != 0:
        return {rel: _committed_text(repo_path, rel) for rel in rels}

    out: dict[str, Optional[str]] = {}
    buf, pos = proc.stdout, 0
    for rel in rels:
        nl = buf.find(b"\n", pos)
        if nl < 0:
            out[rel] = None
            continue
        header = buf[pos:nl].split(b" ")
        pos = nl + 1
        if len(header) < 3 or header[1] == b"missing":
            out[rel] = None            # `<name> missing` — no trailing content line
            continue
        try:
            size = int(header[2])
        except ValueError:
            out[rel] = None
            continue
        raw = buf[pos:pos + size]
        pos += size + 1                # git writes one LF after every object body
        out[rel] = (raw.decode("utf-8", errors="replace")
                    .replace("\r\n", "\n").replace("\r", "\n"))
    return out


def _closer_committed(repo_path: Path, closed_by: str) -> bool:
    """Does the closing packet exist in the COMMITTED tree? Same reason as above: a packet
    merely present on disk (or staged) has not closed the batch.

    NO LONGER ON THE HOT PATH as of P2 (intake #71) -- `open_batches` answers the same
    question from the `_committed_audits` listing it already holds. Kept, not deleted: it is
    the single-path spelling of the probe the listing now performs in bulk, and
    `tests/test_batch_manifest.py` pins the two against each other so the bulk form cannot
    drift from the definition. RETIRE-PROPOSED if that test is ever dropped.
    """
    return _git(repo_path, "cat-file", "-e", f"HEAD:{closed_by}") is not None


def open_batches(repo_path: Path) -> list[OpenBatch]:
    """Every committed manifest that declares a batch open RIGHT NOW, oldest path first.

    Open means all four: the manifest is TRACKED by git, `status: open`, a `closed_by:` whose
    shape can actually resolve, and that `closed_by` path ABSENT from the tree. The absence
    probe is what makes expiry automatic; the other three are what stop the exemption being
    granted by a file nobody committed, or expiring never.

    FAILS TOWARD NO-EXEMPTION. An unreadable manifest, missing frontmatter, or a bad field
    is skipped rather than raised or treated as open — an unknown exemption state must never
    render as 'exempt' (the FR6 discipline ADR-85 established for the anchoring organs). The
    cost of the safe direction is a spurious gate FAIL during a batch, which is loud and
    fixable; the cost of the unsafe one is a silent hole.

    P2 (intake #71) COLLAPSED THE TRANSPORT, NOT THE PREDICATE. The four conditions and the
    order they are tested in are untouched; what changed is that the tree is now read in two
    git spawns (one `ls-tree`, one `cat-file --batch`) instead of one per manifest plus one per
    `closed_by:` probe. The absence probe is answerable from the `ls-tree` listing because
    `_valid_closer` has ALREADY required the closer to live under `docs/audits/`, which is
    exactly what that listing enumerates — so membership decides it as precisely as
    `cat-file -e` did, and only for closers that reached the probe at all.
    """
    audits = _committed_audits(repo_path)
    if audits is None:
        return []             # git unreadable => no exemption (see the fail-toward rule above)
    manifests = _manifests_in(audits)
    texts = _committed_texts(repo_path, manifests)

    found: list[OpenBatch] = []
    for rel in manifests:
        text = texts.get(rel)
        if text is None:
            continue
        fm = _frontmatter(text)
        if fm.get("status", "").lower() != "open":
            continue
        closed_by = fm.get("closed_by", "")
        if not _valid_closer(closed_by):
            continue          # no resolvable expiry => opens nothing (see module docstring)
        if closed_by in audits:
            continue          # the closing packet is committed: the batch is over
        found.append(OpenBatch(batch=fm.get("batch", "?"), path=rel, closed_by=closed_by))
    return found


#: `(repo, full sha) -> (parent shas, subject)`. A memo across the whole PROCESS, which is
#: sound here for a reason that does not generalise to the file caches elsewhere in this
#: fleet: a commit's parents and subject are fixed by its hash, so unlike a path this key
#: cannot go stale while the process runs. Only FULL 40-hex shas are admitted (`_FULL_SHA_RE`)
#: -- an abbreviation can start resolving to a different commit as history grows, which is the
#: same refusal `journal_anchor.introduced` records for itself.
_COMMIT_META: dict[tuple[str, str], tuple[list[str], str]] = {}
_COMMIT_META_MAXSIZE = 4096

#: One record per commit: `<sha> <parents...>` NUL `<subject>`. `%s` is the subject's FIRST
#: line by definition, so a newline can never appear inside a record and plain `splitlines()`
#: is a sound framing.
_META_FORMAT = "%H %P%x00%s"


def warm_commit_meta(repo_path: Path, shas: "list[str]") -> None:
    """Populate `_COMMIT_META` for `shas` in ONE `git log --no-walk`, best-effort.

    P2 (intake #71). Each sha previously cost a `rev-list --parents -n 1` plus a
    `log -1 --format=%s`, and the spine walk asks about the same sha from more than one place,
    so a batch of N merges spent 2N spawns and then spent them again. `--no-walk` is git's own
    "tell me about exactly these commits" mode: it reads the list and emits one record each.

    BEST-EFFORT BY CONSTRUCTION. Anything unreadable -- a bad sha, a git failure, a truncated
    record -- simply leaves that sha unwarmed, and `_commit_meta` falls back to the per-sha
    reads it always used. So this can make the walk faster and cannot make it answer
    differently; there is no failure mode where a warmed entry is consulted but wrong.
    """
    want = [s for s in dict.fromkeys(shas)
            if _FULL_SHA_RE.match(s) and (str(repo_path), s) not in _COMMIT_META]
    if not want or len(_COMMIT_META) >= _COMMIT_META_MAXSIZE:
        return
    out = _git(repo_path, "log", "--no-walk", f"--format={_META_FORMAT}", *want, "--")
    if out is None:
        return
    for line in out.splitlines():
        head, sep, subject = line.partition("\x00")
        if not sep:
            continue
        parts = head.split()
        if not parts or not _FULL_SHA_RE.match(parts[0]):
            continue
        _COMMIT_META[(str(repo_path), parts[0])] = (parts, subject.strip())


def _commit_meta(repo_path: Path, sha: str) -> Optional[tuple[list[str], str]]:
    """`(rev-list --parents output, subject)` for `sha`, from the memo or from git.

    The tuple's first element keeps `rev-list --parents -n 1`'s exact shape -- the commit
    followed by its parents -- because both callers below test `len(...) < 3` against it, and
    a helper that quietly changed that shape would move the merge/non-merge boundary.
    """
    key = (str(repo_path), sha)
    hit = _COMMIT_META.get(key)
    if hit is not None:
        return hit
    import journal_anchor as _ja          # local: shared git-read shape, one definition
    try:
        parents = _ja._git(repo_path, "rev-list", "--parents", "-n", "1", sha).split()
        subject = _ja._git(repo_path, "log", "-1", "--format=%s", sha).strip()
    except Exception:                     # noqa: BLE001 -- unknown => caller fails closed
        return None
    if _FULL_SHA_RE.match(sha) and len(_COMMIT_META) < _COMMIT_META_MAXSIZE:
        _COMMIT_META[key] = (parents, subject)
    return parents, subject


def merged_branch_name(repo_path: Path, sha: str) -> Optional[str]:
    """The branch a merge commit merged IN, read from its subject — or None.

    None for a non-merge commit, for a merge whose subject does not carry the
    `Merge branch '<name>'` form, and for any git read failure. Every None is the
    no-exemption direction.
    """
    meta = _commit_meta(repo_path, sha)
    if meta is None:
        return None
    parents, subject = meta
    if len(parents) < 3:                  # sha + <2 parents => not a merge
        return None
    m = _MERGE_SUBJECT_RE.match(subject)
    return m.group(1) if m else None


def is_lane_merge(repo_path: Path, sha: str) -> bool:
    """True iff `sha` is a merge commit whose merged branch is in the RATIFIED lane SET.

    "The lane shape" is `validate_branch_naming` and nothing else ([#514]) — the same module
    `classify()` reads, so the exemption and the naming enum cannot disagree about what a lane
    is. They did, on 9 of 16 real merged lane branches, which is what made both organs
    unenforceable at once.

    WIDENED to `is_lane_branch` from `LANE_BRANCH_RE` (batch U, lane-u-000-branch-enum-parity),
    and the reason is that the narrow version had rebuilt the same disagreement one seam over.
    `validate_substrate` leg 5 refuses a contract whose branch an enum-iterating teardown
    cannot see, and its refusal names THIS exemption as one of the two iterators. Fixing leg 5
    to admit the whole ruled lane set — `claude/<slug>`, `epic/<slug>`, `automation/<slug>` —
    while leaving the exemption on the batch grammar alone would have produced a FALSE GREEN:
    a cloud lane passing the freeze-time check that promises the exemption reaches it, and
    then not receiving it (terra HIGH, 2026-09-07, caught pre-merge). The two must widen
    together or not at all, so they now read one predicate.

    WHAT THIS DOES AND DOES NOT WIDEN. `exempt()` feeds exactly one consumer, the audit
    BACKSTOP `audit.check_journal_spine_anchor`, and the exemption still requires BOTH
    conditions: a lane merge AND a committed manifest declaring an open batch. It still
    self-expires when that manifest's `closed_by:` packet lands. It still does not reach
    `block_unanchored_push` — the range-level pre-push refusal stays unconditional, which is
    the property the R-1 containment argument rests on and which two ratified tests pin. The
    ADR-110 rationale is what carries the widening: a batch's JOURNAL entry names its lane
    merge SHAs and so cannot exist until after them, and that is exactly as true of a cloud
    lane merged in the same queue as of a `worktree-lane-*` one. ADR-116 is the recorded cost
    of it not being — it sat stranded on `claude/lane-f` until a window close.

    Fails CLOSED in every unknown case: a non-merge, an unparseable merge subject, a git read
    failure, and any name outside the set (`classify()` -> `unknown`, a bare `worktree-<name>`,
    a `feat/` or `docs/` arc) all return False, i.e. no exemption.
    """
    name = merged_branch_name(repo_path, sha)
    return bool(name and is_lane_branch(name))


# The lane-ish shapes a NON-conforming merge subject still leaks, used only to tell a
# message-style miss apart from a genuine non-lane merge. Deliberately loose: it is a
# diagnostic, never an exemption path -- nothing widens `is_lane_merge` by matching here.
_LANEISH_IN_SUBJECT_RE = re.compile(r"(?:worktree-)?lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*")


def subject_style_miss(repo_path: Path, sha: str) -> Optional[str]:
    """The lane name a merge subject NAMES but does not expose to the parser, or None.

    THE TRAP THIS EXISTS TO END (measured 2026-08-31, [#614] integration). The exemption reads
    the merged branch out of the subject via `_MERGE_SUBJECT_RE`, i.e. git's DEFAULT
    `Merge branch '<name>'` form. An integrator who writes a descriptive subject instead --
    `Merge DC-1 (lane-a-1-vision-to-readme) -- ...` -- drops the prefix, so `merged_branch_name`
    returns None, `is_lane_merge` is False, and the exemption silently does not apply. It fails
    CLOSED, which is the safe direction and exactly why nobody notices: the cost lands later, as
    an anchor-gate deadlock in a different command, with nothing anywhere saying an exemption was
    expected and missed. That is what happened on the mechanism's first live test.

    So: when a merge is NOT recognised as a lane merge but its subject still mentions a
    lane-shaped branch name, that is almost certainly message style rather than a real non-lane
    merge, and the caller can say so out loud. Returns the leaked name for the message.

    Deliberately NOT an exemption path. Recognising a lane here would make the grammar the
    subject-writer's to choose, which is the coupling `[#514]` removed. The ruled procedure is
    still "keep git's default `Merge branch '<name>'` prefix and append prose after it"; this
    only makes a miss LOUD instead of silent.
    """
    if merged_branch_name(repo_path, sha) is not None:
        return None                        # parsed fine -- nothing to warn about
    meta = _commit_meta(repo_path, sha)    # same two reads `merged_branch_name` just made
    if meta is None:                       # a read failure is not a style miss
        return None
    parents, subject = meta
    if len(parents) < 3:
        return None                        # not a merge at all -- not this function's business
    m = _LANEISH_IN_SUBJECT_RE.search(subject)
    return m.group(0) if m else None


def exempt(repo_path: Path, shas: list[str],
           batches: Optional[list[OpenBatch]] = None) -> set[str]:
    """The subset of `shas` the declared-integration-arc exemption covers.

    Empty set when no batch is open — which is the overwhelmingly common state, and costs
    one glob. `batches` is injectable so a caller that already resolved them (to report
    WHICH batch granted the exemption) does not resolve them twice.
    """
    live = open_batches(repo_path) if batches is None else batches
    if not live:
        return set()
    # P2 (intake #71): read every candidate's parents and subject in one spawn BEFORE the
    # per-sha loop asks for them one at a time. Placed here rather than inside
    # `is_lane_merge` because this is the only site that holds the whole list -- and it is
    # deliberately AFTER the `if not live` short-circuit, so the common no-open-batch case
    # still costs zero commit reads.
    warm_commit_meta(repo_path, shas)
    return {s for s in shas if is_lane_merge(repo_path, s)}


# --- `[#630]`: the manifest's lane table and the batch's contract slugs must AGREE ----------
#
# THE MEASURED BATCH-E DEFECT (integrator defect (b), 2026-09-01). The manifest's lane table
# named `lane-b-2-essentials-and-claude-md`; what was actually dispatched, and what carries
# the commit, pairs to `lane-b-3-claude-md-genre`. The slug was renumbered between draft and
# dispatch and nothing anywhere compared the two -- so the manifest, the surface the ADR-110
# exemption reads and the teardown iterates, named a lane that did not exist, while the lane
# that did exist was unnamed. THE SAME CLASS as the teardown-enum defect
# (`RULE_TEARDOWN_ENUM`) that predicate 5 already catches -- a name that appears in two
# places with only a human keeping them equal -- except nothing crosses from the CONTRACT to
# the MANIFEST at all. This is that comparison.

#: Rule id for the freeze-time refusal below. Not a member of `validate_substrate.RULE_IDS`:
#: that closed set is CONTRACT-vs-REGISTRY/CONTRACT-vs-CONTRACT consistency; this is a
#: MANIFEST-vs-CONTRACT-DIRECTORY comparison, a different surface pair, homed in the module
#: that already owns "batch" and "manifest" as concepts.
RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT = "batch-manifest-contract-slug-agreement"

#: Same per-leg arm-date convention as `validate_substrate.LEG_ARM_DATES` ([#629]'s own entry,
#: same reasoning): a leg written today cannot honestly gate a manifest frozen before it
#: existed. FREEZE stays unscoped by date -- this dict is for a future commit-time adapter.
LEG_ARM_DATES: dict[str, _dt.date] = {
    RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT: _dt.date(2026, 9, 1),
}

#: The manifest's own `## THE LANES` heading, however many hyphens/words follow it on the
#: same line (`— 7 committing, frozen 2026-09-01`, `-- 15 committing, frozen 2026-08-31`).
_LANES_HEADING_RE = re.compile(r"^ {0,3}#{1,6}\s*THE LANES\b.*$", re.I | re.M)
#: Any heading, used to bound the LANES section the same way `validate_substrate` bounds its
#: own sections -- the next heading ends the block.
_ANY_HEADING_RE = re.compile(r"^ {0,3}#{1,6}\s+\S", re.M)
#: A lane-slug-shaped token: `lane-<letter>-<digits>-<slug>`. Deliberately NOT
#: `validate_branch_naming.LANE_BRANCH_RE` -- that matches a BRANCH (`worktree-lane-...`), and
#: a manifest's lane table names the SLUG, not the branch. The two are related by a fixed
#: prefix, never by identity.
_SLUG_TOKEN_RE = re.compile(r"\blane-[a-z]-\d+(?:-[a-z0-9]+)+\b", re.I)


def manifest_lane_slugs(text: str) -> set[str]:
    """The set of lane slugs a manifest's `## THE LANES` table declares, lower-cased.

    ONE slug per row: the FIRST lane-shaped token on each line. A row that also happens to
    mention a branch name later on the same line (`worktree-lane-a-1-x`) does not double
    count or disagree -- the substring it carries resolves to the identical slug token.

    Returns the empty set when the manifest carries no `## THE LANES` heading at all, which
    is not a parse failure: it just means this manifest declares no slugs to compare.
    """
    heading = _LANES_HEADING_RE.search(text)
    if heading is None:
        return set()
    start = heading.end()
    nxt = _ANY_HEADING_RE.search(text, start)
    body = text[start:nxt.start()] if nxt else text[start:]
    out: set[str] = set()
    for line in body.splitlines():
        match = _SLUG_TOKEN_RE.search(line)
        if match:
            out.add(match.group(0).lower())
    return out


def freeze_manifest_contract_agreement(manifest_text: str,
                                       contracts: Mapping[str, str]) -> list[Refusal]:
    """`[#630]` -- the manifest's declared lane slugs and the batch's contract slugs must be
    the SAME SET, at freeze.

    `contracts` is `{source: contract_text}`, the same shape `validate_substrate.validate_batch`
    takes -- a contract's own slug is read from its pairing line via `contract_slug`, not
    guessed from its filename, so a filename/pairing-line mismatch (a different defect) does
    not mask or fake this one. A contract whose pairing line does not resolve to a slug at all
    is skipped here: that contract already fails layer 1 shape or `[#591]`'s own checks
    elsewhere, and stacking a second finding on the same defect helps nobody.

    SET EQUALITY BOTH WAYS: a manifest naming a phantom lane fails as loudly as a contract no
    manifest names. Both sides are named in the ONE refusal, never reduced to a count.
    """
    manifest_slugs = manifest_lane_slugs(manifest_text)
    contract_slugs = {slug for slug in (contract_slug(text) for text in contracts.values())
                      if slug is not None}
    manifest_only = manifest_slugs - contract_slugs
    contracts_only = contract_slugs - manifest_slugs
    if not manifest_only and not contracts_only:
        return []

    parts: list[str] = []
    if manifest_only:
        parts.append(f"the manifest names {sorted(manifest_only)} with no matching contract")
    if contracts_only:
        parts.append(f"contract(s) {sorted(contracts_only)} are named by no manifest row")
    detail = (" · ".join(parts) + " — set equality is required both ways at freeze "
              "(the measured batch-E defect: a slug renumbered between draft and dispatch, "
              "with nothing comparing the two)")
    return [Refusal(rule=RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT, source="<manifest>",
                    detail=detail)]


# --- manifest-linked artifacts (the 2026-09-05 operator ruling) --------------------------------

#: The manifest and the packet it names via `closed_by:` are BOTH linking surfaces. The ruling
#: names three link kinds -- `closed_by`, lane packets, close packets -- and the close packet is
#: where a batch records what its lanes actually produced, so scanning the manifest alone would
#: miss every artifact the batch enumerated at close rather than at freeze. Measured on batch G:
#: manifest-only reaches 3 artifacts, manifest + closer reaches 4.
#:
#: PRECISION ABOUT THE PRECEDENT (terra, record-only): reading the closer's CONTENT is THIS
#: ruling's extension, not something ADR-110 already does. That gate reads the manifest's
#: committed frontmatter and merely PROBES whether the `closed_by:` path exists; it never
#: consumes the closer's body. The argument for treating a manifest as load-bearing stands on
#: the manifest itself, and the closer rides on the ruling that named close packets.
_AUDITS_PATH_RE = re.compile(r"docs/audits/([A-Za-z0-9._/-]+\.md)")
_LINKED_STEM_RE = re.compile(
    r"(?<![A-Za-z0-9._-])(\d{4}-\d{2}-\d{2}-[A-Za-z0-9._-]+)(?![A-Za-z0-9._-])")


class ManifestLinks(NamedTuple):
    """What the committed batch manifests link, split by HOW they link it.

    Two sets rather than one, because they carry different false-positive surfaces and a
    caller may reasonably want to report them apart. `explicit` is a path or dated stem the
    manifest actually wrote down; `lane_slugs` is the batch's declared lane roster, which
    resolves to an artifact by containment (`lane-g-276-deploy-waiver` is a substring of
    `2026-09-02-technical-lane-g-276-deploy-waiver.md`).
    """
    explicit: frozenset[str]
    lane_slugs: frozenset[str]
    manifests: tuple[str, ...]


def manifest_links(repo_path: Path) -> ManifestLinks:
    """Every artifact identifier reachable from a committed batch manifest.

    READS THE WORKING TREE, not git, because both callers measure the working tree and a
    number taken from a different snapshot than the corpus it is compared against is not a
    measurement. `open_batches` reads committed text for a different reason -- it decides
    whether a batch is open, where an unstaged edit flipping `status:` would be a bypass.

    HONEST LIMITS. Containment on a lane slug is a substring test, so an artifact whose name
    merely contains a declared slug counts as linked; the slug grammar (`lane-<letter>-<id>-`)
    plus the batch-scoped letter makes a collision unlikely but does not exclude it. And this
    resolves LINKAGE only -- it says a governance surface named the artifact, never that the
    naming was apt.
    """
    explicit: set[str] = set()
    slugs: set[str] = set()
    seen: list[str] = []
    for manifest in sorted(Path(repo_path).glob(MANIFEST_GLOB)):
        try:
            text = manifest.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            # A manifest that cannot be read links nothing. Deliberately not raising: this is
            # an ADDITIVE coverage route, so an unreadable manifest costs coverage it would
            # have granted and can never invent any.
            continue
        seen.append(manifest.name)
        surfaces = [text]
        closer = _frontmatter(text).get("closed_by", "")
        if closer and _valid_closer(closer):
            closer_path = Path(repo_path) / closer
            try:
                surfaces.append(closer_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                pass
        for surface in surfaces:
            for hit in _AUDITS_PATH_RE.findall(surface):
                name = hit.rsplit("/", 1)[-1]
                explicit.add(name)
                explicit.add(name[:-3] if name.endswith(".md") else name)
            for stem in _LINKED_STEM_RE.findall(surface):
                explicit.add(stem)
                explicit.add(stem[:-3] if stem.endswith(".md") else stem)
            slugs |= manifest_lane_slugs(surface)
    return ManifestLinks(frozenset(explicit), frozenset(slugs), tuple(seen))


#: An artifact stem's descriptive tail: everything after `<date>-<class>-`. A lane's own
#: packet begins its tail WITH the lane slug; a document merely ABOUT that lane does not.
_ARTIFACT_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_DATE_PREFIX_LEN = len("YYYY-MM-DD-")
#: Fallback class: ONE kebab segment, DIGITS ADMITTED. Off-enum classes are real on disk --
#: `arc5` (x3), `phase0`, `stage3`, `pilot81`, `cohort1` -- so an enum-only split would refuse
#: a lane artifact landing under any of them.
_FALLBACK_CLASS_RE = re.compile(r"^[a-z0-9]+-(?P<tail>.+)$")
#: Longest-match first, so `ecosystem-audit` wins over a bare `ecosystem` split. Same ordering
#: `validate_hermetization` applies to the same enum, for the same reason.
_CLASS_BY_LEN = tuple(sorted(AUDIT_CLASS_ENUM, key=len, reverse=True))


def artifact_tail(stem: str) -> Optional[str]:
    """The descriptive tail of `stem` -- what follows `<date>-<class>-` -- or None.

    THE SPLIT IS ENUM-FIRST, THEN ONE SEGMENT (terra HIGH, pass 2). A single `[a-z]+` class
    got both ends of the real grammar wrong. It cannot match a HYPHENATED ruled class:
    `...-ecosystem-audit-lane-a-1-x` splits after `ecosystem`, leaving the tail as
    `audit-lane-a-1-x`, which begins with no slug. And it cannot match a DIGIT-BEARING one:
    `arc5`, `phase0`, `stage3`, `pilot81`, `cohort1` are all on disk today. Under either shape
    a lane's OWN artifact is refused -- a false NEGATIVE introduced while fixing a false
    positive, which is the failure mode a narrowing fix has to be checked for.

    BOTH WERE LATENT, NOT LIVE. No artifact in the corpus today has a lane-slug tail under
    either shape, so `manifest_linked` is unchanged by this: it is a robustness fix, and
    claiming it recovered coverage would be false. It widens strictly -- an enum class that is
    a single segment splits identically to the fallback, so no currently-admitted artifact can
    become refused.
    """
    if not _ARTIFACT_DATE_RE.match(stem):
        return None
    rest = stem[_DATE_PREFIX_LEN:]
    for cls in _CLASS_BY_LEN:
        if rest.startswith(f"{cls}-"):
            return rest[len(cls) + 1:] or None
    match = _FALLBACK_CLASS_RE.match(rest)
    return match.group("tail") if match else None


def links_artifact(links: ManifestLinks, name: str) -> Optional[str]:
    """The link kind by which `name` is reachable, or None. `'explicit'` beats `'lane-slug'`.

    THE LANE-SLUG LEG IS ANCHORED, NOT CONTAINMENT (terra HIGH, pre-merge). It was
    `slug in stem`, which admitted `2026-09-05-technical-review-of-lane-g-276-deploy-waiver.md`
    -- a document ABOUT a lane -- as if it were that lane's own packet, granting it both
    DISPOSITIONED and CITED and silencing both ratchets. That is SILENT false coverage, which
    `funnel_coverage`'s docstring already names as the failure mode to prefer loud false WARNs
    over: a spurious WARN is noticed and fixed in one edit, invented coverage is never noticed
    at all.

    The anchor: strip the `<date>-<class>-` prefix (`artifact_tail`, enum-first) and require the
    remaining tail to BEGIN with the slug, at a `-` or end-of-string boundary. A lane's artifacts are named for their lane
    (`…-technical-lane-g-614-hygiene-close-packet.md` tails as `lane-g-614-hygiene-…`); a
    commentary names something else first. A stem that carries no dated `<date>-<class>-`
    prefix has no tail to anchor against and is refused rather than fuzzily matched.
    """
    stem = name[:-3] if name.endswith(".md") else name
    if name in links.explicit or stem in links.explicit:
        return "explicit"
    tail = artifact_tail(stem)
    if tail is None:
        return None
    for slug in links.lane_slugs:
        if tail == slug or tail.startswith(f"{slug}-"):
            return "lane-slug"
    return None
