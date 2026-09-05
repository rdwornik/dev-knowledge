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
from validate_branch_naming import LANE_BRANCH_RE   # noqa: E402

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

#: `git merge --no-ff <branch>` writes this subject; `/lane-integrate` relies on it too.
_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")

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


def _committed_manifests(repo_path: Path) -> list[str]:
    """Manifest paths present in the COMMITTED tree at HEAD, matching the manifest grammar."""
    out = _git(repo_path, "ls-tree", "-r", "--name-only", "HEAD", "--", "docs/audits/")
    if out is None:
        return []
    pat = MANIFEST_GLOB.split("/")[-1]
    return sorted(p.strip() for p in out.splitlines()
                  if p.strip() and PurePosixPath(p.strip()).match(pat))


def _committed_text(repo_path: Path, rel: str) -> Optional[str]:
    """The blob at `HEAD:<rel>`, or None. Reading the COMMITTED blob is the whole point.

    EVERYTHING HERE IS HEAD-BASED, and the second terra HIGH of 2026-08-07 is why. The first
    fix used `git ls-files` (tracked-ness) and still read CONTENT from the working tree —
    which `ls-files` also satisfies for a merely STAGED addition. So a staged-but-uncommitted
    manifest, or an unstaged edit to a committed one, could still declare a batch open. The
    rule says COMMITTED; the only implementation that means it reads the committed blob.
    """
    return _git(repo_path, "show", f"HEAD:{rel}")


def _closer_committed(repo_path: Path, closed_by: str) -> bool:
    """Does the closing packet exist in the COMMITTED tree? Same reason as above: a packet
    merely present on disk (or staged) has not closed the batch."""
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
    """
    found: list[OpenBatch] = []
    for rel in _committed_manifests(repo_path):
        text = _committed_text(repo_path, rel)
        if text is None:
            continue
        fm = _frontmatter(text)
        if fm.get("status", "").lower() != "open":
            continue
        closed_by = fm.get("closed_by", "")
        if not _valid_closer(closed_by):
            continue          # no resolvable expiry => opens nothing (see module docstring)
        if _closer_committed(repo_path, closed_by):
            continue          # the closing packet is committed: the batch is over
        found.append(OpenBatch(batch=fm.get("batch", "?"), path=rel, closed_by=closed_by))
    return found


def merged_branch_name(repo_path: Path, sha: str) -> Optional[str]:
    """The branch a merge commit merged IN, read from its subject — or None.

    None for a non-merge commit, for a merge whose subject does not carry the
    `Merge branch '<name>'` form, and for any git read failure. Every None is the
    no-exemption direction.
    """
    import journal_anchor as _ja          # local: shared git-read shape, one definition
    try:
        parents = _ja._git(repo_path, "rev-list", "--parents", "-n", "1", sha).split()
        if len(parents) < 3:              # sha + <2 parents => not a merge
            return None
        subject = _ja._git(repo_path, "log", "-1", "--format=%s", sha).strip()
    except Exception:                     # noqa: BLE001 -- unknown => not exempt
        return None
    m = _MERGE_SUBJECT_RE.match(subject)
    return m.group(1) if m else None


def is_lane_merge(repo_path: Path, sha: str) -> bool:
    """True iff `sha` is a merge commit whose merged branch matches the RATIFIED lane grammar.

    "The lane shape" is `validate_branch_naming.LANE_BRANCH_RE` and nothing else ([#514]) — the
    same constant `classify()` uses to call a branch `batch-lane`, so the exemption and the
    naming enum can no longer disagree about what a lane is. They did, on 9 of 16 real merged
    lane branches, which is what made both organs unenforceable at once.

    Fails CLOSED in every unknown case: a non-merge, an unparseable merge subject, a git read
    failure and an off-grammar name all return False, i.e. no exemption.
    """
    name = merged_branch_name(repo_path, sha)
    return bool(name and LANE_BRANCH_RE.match(name))


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
    try:
        import journal_anchor as _ja
        parents = _ja._git(repo_path, "rev-list", "--parents", "-n", "1", sha).split()
        if len(parents) < 3:
            return None                    # not a merge at all -- not this function's business
        subject = _ja._git(repo_path, "log", "-1", "--format=%s", sha).strip()
    except Exception:                      # noqa: BLE001 -- a read failure is not a style miss
        return None
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


def links_artifact(links: ManifestLinks, name: str) -> Optional[str]:
    """The link kind by which `name` is reachable, or None. `'explicit'` beats `'lane-slug'`."""
    stem = name[:-3] if name.endswith(".md") else name
    if name in links.explicit or stem in links.explicit:
        return "explicit"
    for slug in links.lane_slugs:
        if slug in stem:
            return "lane-slug"
    return None
