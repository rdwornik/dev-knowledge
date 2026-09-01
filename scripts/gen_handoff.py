#!/usr/bin/env python3
"""gen_handoff.py — the v5 handoff bundle generator (#164 RF-2 / RF-1 option b).

Assembles a valid v5 bundle (HANDOFF_BOOT + RESIDUAL + PROBES + SUPPLEMENT, then
PASTE_THIS via scripts/assemble_paste.py) from COMMITTED repo state, replacing the
hand-copy that let the handoff's prose-held properties erode. ADR-98 adds two more
modes on top of the v5/epic pair: `functional` (a minimal, probe-free, one-file
intake-capture boot) and `developer` (a pure additive alias of `epic`). Two
structural invariants:

  * ANSWER-FREE BY CONSTRUCTION (RF-1 option b). The browser-visible files
    (PROBES / RESIDUAL / BOOT) never receive a generation-time ANSWER value (a
    count, sha, verdict, date-relation, or group-membership). The render functions
    are literally not given the hint values — `collect_hints` output flows ONLY to
    the JOURNAL generation-entry DRAFT, which is printed to stdout, never written
    into the bundle and never auto-appended to JOURNAL.md.
  * SCAFFOLD, NOT NARRATION (RF-6). BOOT / RESIDUAL are state-filled scaffolds:
    the generator fills the deterministic surface (header / framing) and leaves the
    session narrative (Purpose, shipped-map, next-frontier, drift-flag context) as
    explicit FILL-IN regions for CC. It never authors the strategic "why", and a
    --filled re-render copies each FILL-IN region byte-for-byte from the on-disk
    file, so re-generation never clobbers what CC wrote.

Two BOUNDARY invariants gate generation itself (never the bundle's content):
WINDOW = BATCH — a cut refuses while a committed manifest declares an open batch — and
no-leftovers — a cut refuses over a linked worktree or a live stash, naming each. Both
fire before anything is written; see `assert_batch_boundary` / `assert_boundary_hygiene`.

The cold<->FILLED framing flip is deterministic: the fill-state is read via
assemble_paste._extract_answers (ONE shared definition), so the four framing sites
and the assembler's fold decision can never disagree.

Layer-2 / read-only w.r.t. tracked spine files: writes ONLY <bundle>/*; never edits
JOURNAL.md / BACKLOG.md (the operator prepends the printed draft at wrap).
"""
from __future__ import annotations

import datetime as _dt
import importlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import click

#: The module's public API, declared rather than inferred.
#:
#: RULED 2026-08-29 (architect, post-night A1). FM-5 (`scripts/governance_health.py`) resolves
#: FM-4's emitter by CAPABILITY — a *public* callable whose name carries both "funnel" and
#: "health" — and this module exposed THREE, so `resolve_fm4_emitter` refused the ambiguity
#: rather than guessing. The tie-break is `live consumer wins > registry entry wins > else
#: FAIL`, and the live consumer settles it mechanically, not by preference: FM-5 calls
#: `parse_shared_fields(src.render(root))` — ONE positional argument, return value parsed as a
#: rendered text block. Only `funnel_health_block(repo_root) -> str` has that shape.
#: `_funnel_health_numbers` returns a tuple, and `_write_funnel_health` takes two arguments and
#: WRITES A FILE, which a reporter must never do.
#:
#: So `funnel_health_block` is the single public emitter and the other two are `_`-private
#: delegates. The RENAME is the operative half — `resolve_fm4_emitter` scans `dir(mod)` and
#: excludes `_`-private names, and `dir()` does not consult `__all__`. This list is the
#: declaration that makes the intent legible; `test_exactly_one_public_funnel_health_emitter`
#: is what actually holds the line, and it imports FM-5's own regex so the two cannot drift.
__all__ = [
    "BoundaryHygieneError",
    "BundleCollisionError",
    "BundleIdentityError",
    "GenResult",
    "OpenBatchError",
    "assert_batch_boundary",
    "assert_boundary_hygiene",
    "collect_hints",
    "collect_state",
    "detect_fill_state",
    "dispatch_form",
    "funnel_health_block",
    "generate",
    "journal_draft",
    "reflow_framing",
    "standing_vs_new",
    "verify_seal_identity",
]

# CLOUD-4 v2 (R2 §1.5 GO-b) — the canonical filename and the `_vision_extract` degrade string
# come from the one registry. R2 §1.4 R2 is why they live TOGETHER there: this generator does
# not crash on a missing section, it stamps a placeholder into a bundle that is immutable the
# moment it is committed, so the name and its degrade contract cannot be allowed to move apart.
try:
    from scripts import canonical_docs as _cdocs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import canonical_docs as _cdocs

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
_TMPL_DIR = _REPO_ROOT / "templates" / "handoff" / "v5"
_TMPL_DIR_EPIC = _REPO_ROOT / "templates" / "handoff" / "epic"
_TMPL_DIR_FUNCTIONAL = _REPO_ROOT / "templates" / "handoff" / "functional"

# HANDOFF_PROCESS §13(c″) (v6.0.1): the `Destination` row's branch field is the BOOT DESTINATION —
# where the seat LANDS when it boots, not where its work is eventually committed — and `main` is
# legal for a primary-tree seat, which boots there and branches per act thereafter.
#
# Deliberately NOT `state.branch`. That is a different question ("which branch was this cut on?"),
# answered by the `Generated at` row, and answering both from one token shipped the 2026-08-01
# bundle a Destination naming its own `docs/…` generation branch — which MERGE IS ATOMIC deleted at
# finalize, leaving P3 to compare live `main` against a dead ref and block an otherwise-clean
# bundle. Epic lanes declare their destination in `EPIC_BOOT` (§14a, separate template).
_PRIMARY_TREE_BOOT_DESTINATION = "main"

# Per-mode framing that is structural (never an answer value).
_MODE = {
    "architect": {
        "scope": "planning / way-of-working scope",
        "posture": ("orient first, ask the operator for off-repo context, drive decomposition, hold "
                    "the whole-system view, surface design tensions — not the reactive-filter default"),
    },
    "execution": {
        "scope": "execution / task scope",
        "posture": ("the reactive-filter posture — execute the named task-graph against live state and "
                    "verify after each step, escalating on any drift"),
    },
    # §14a epic-lane mode (ADR-97): a scope-contract bundle, not a v5 architect/execution one.
    "epic": {
        "scope": "one epic end-to-end, inside a root-provisioned worktree (ADR-97; HANDOFF_PROCESS §14a)",
        "posture": ("the epic-lane posture — decompose the epic into user stories, delegate to CC, "
                    "review, keep own-epic BACKLOG checkboxes current, commit-and-STOP on the epic "
                    "branch; escalate ADR-worthy forks / boundary needs / cross-epic deps to the root"),
    },
    # §16 functional-architect mode (ADR-98): requirements-capture only, no probes.
    "functional": {
        "scope": ("requirements intake — a fluid functional-architect conversation whose sole "
                  "product is an intake doc (ADR-98; HANDOFF_PROCESS §16)"),
        "posture": ("the functional-architect posture — listen, probe with scenario questions, "
                    "structure the operator's intent into an intake doc; never solutionize, never "
                    "probe live state; technical-factual questions are recorded as open questions, "
                    "not answered"),
    },
}

# The cold<->FILLED framing sites (RF-2 item 3). Each is a two-valued literal selected by the
# fill-state boolean, so the flip is deterministic, never hand-set. Index 0 = cold, 1 = filled.
_FRAMING = {
    "SUPPLEMENT_BANNER": (
        "> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the "
        "ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context "
        "beat fires **FULL** (a full off-repo ask), not the narrowed *\"anything changed since?\"*.",
        "> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) "
        "operator-context beat **NARROWS** to *\"anything changed since the supplement was written?\"*.",
    ),
    "P1_GATE_NOTE": (
        "This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *\"what off-repo "
        "context: intent, priorities, findings not in the repo, changed decisions?\"* — not a narrowed "
        "\"anything changed since?\". (If the operator runs `supplement filled`, its ANSWERS fold in and "
        "the beat narrows.)",
        "The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat "
        "**NARROWS** to *\"anything changed since the supplement was written?\"*.",
    ),
    "PASTE_STEP6": (
        "6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless "
        "the operator fills it first the beat fires **FULL**: *\"what off-repo context — intent, "
        "priorities, findings not in the repo, changed decisions?\"*",
        "6. **Then the operator-context beat (§13d).** The supplement is **FILLED**; its ANSWERS are in "
        "the paste, so the beat **NARROWS** to *\"anything changed since the supplement was written?\"*.",
    ),
}


def _framing(site: str, filled: bool) -> str:
    return _FRAMING[site][1 if filled else 0]


# Per-mode chat-title role (#287). The browser chat name the operator copies from the bundle
# header so a fleet of parallel sessions is nameable-at-a-glance. STRUCTURAL identity only.
_TITLE_ROLE = {
    "functional": "Functional Architect",
    "architect": "Technical Architect",
    "execution": "Developer",
    "epic": "Developer",  # "developer" is normalized to "epic" before this is reached
}


def _chat_title(mode: str, repo: str, ident: str) -> str:
    """The proposed browser chat-title for the bundle header (#287; #164 leg e).

    Grammar (frozen — #164 closure contract): `[REPO] <role> <ident> · SEQ 1`, role per mode
    (functional->Functional Architect, architect->Technical Architect,
    execution/epic/developer->Developer). For epic/developer `ident` is the epic slug (name +
    number, the live [S<n>] story-id era, #286) and `EPIC <n>` is derived from its leading
    number; other modes carry the bundle slug as `<ident>`.

    ANSWER-FREE (RF-1): every part is session IDENTITY already present in the bundle (repo,
    mode-role, slug/epic-slug) plus the literal `SEQ 1` naming slot the operator increments —
    NO probe answer (count / sha / verdict / date-relation). So this token never breaches the
    answer-free invariant, the same as {{SLUG}} / {{REPO}} / {{MODE}}."""
    name = repo.lstrip(".")
    role = _TITLE_ROLE[mode]
    if mode == "epic":
        m = re.match(r"(\d+)", ident)
        epic_no = f" EPIC {m.group(1)}" if m else ""
        return f"[{name}] {role} {ident}{epic_no} · SEQ 1"
    return f"[{name}] {role} — {ident} · SEQ 1"


# --- committed state + generation hints -------------------------------------

@dataclass(frozen=True)
class _State:
    """The STRUCTURAL surface that may enter the bundle. `branch` is the only field the render
    functions receive (a §5-sanctioned "which branch" pointer). `dirty` gates generation
    (a bundle is cut from COMMITTED state)."""
    branch: str
    dirty: bool


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped, or "" on any error.

    Lossy by design for the STRUCTURAL callers (branch / dirty), which have a sane default
    either way. Any caller that must distinguish "empty result" from "the command failed"
    uses `_git_status` below — conflating those two is what silently disarmed RM-8."""
    ok, out = _git_status(repo_root, *args)
    return out if ok else ""


# git's own repo-local env vars, scrubbed before any git call whose answer is about THIS repo.
# An inherited GIT_DIR (a hook, a nested invocation) otherwise redirects the query to a FOREIGN
# repo and the answer is silently about the wrong tree — the [#355] class, and exactly how the
# RM-8 refusal was disarmed. Derived from git itself (never hand-listed: the first hand-written
# version of the audit.py list omitted 8 of git's 15), cached, with a pinned fallback if git is
# unavailable. Mirrors audit.py `_git_location_env`, the established precedent.
_GIT_LOCATION_ENV_FALLBACK = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX", "GIT_CONFIG", "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS", "GIT_GRAFT_FILE", "GIT_IMPLICIT_WORK_TREE",
    "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_SHALLOW_FILE",
    "GIT_CEILING_DIRECTORIES", "GIT_NAMESPACE",
)
_GIT_LOCATION_ENV_CACHE: frozenset[str] | None = None


def _git_location_env() -> frozenset[str]:
    """git's own repo-local env-var names (+ the scoping extras). Queried once, cached."""
    global _GIT_LOCATION_ENV_CACHE
    if _GIT_LOCATION_ENV_CACHE is None:
        names = set(_GIT_LOCATION_ENV_FALLBACK)
        try:
            p = subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True,
                               text=True, timeout=30)
            if p.returncode == 0:
                names |= {ln.strip() for ln in p.stdout.split() if ln.strip()}
        except (OSError, subprocess.SubprocessError):
            pass
        _GIT_LOCATION_ENV_CACHE = frozenset(names)
    return _GIT_LOCATION_ENV_CACHE


def _git_status(repo_root: Path, *args: str) -> tuple[bool, str]:
    """Run a read-only git command in a SCRUBBED env; return `(ok, stdout-stripped)`.

    `ok` is False when git is absent, errored, or timed out — so a caller can tell "the answer
    is empty" from "there is no answer", which `_git` alone cannot. Wrapped (not inlined) so
    tests can stub the failure mode."""
    env = {k: v for k, v in os.environ.items() if k not in _git_location_env()}
    try:
        out = subprocess.run(["git", *args], cwd=str(repo_root), capture_output=True,
                             text=True, timeout=30, env=env)
    except (OSError, subprocess.SubprocessError):
        return (False, "")
    return (out.returncode == 0, out.stdout.strip())


def collect_state(repo_root: Path) -> _State:
    branch = _git(repo_root, "branch", "--show-current") or "(detached)"
    dirty = bool(_git(repo_root, "status", "--porcelain"))
    return _State(branch=branch, dirty=dirty)


# --- RM-8 overwrite refusal (R5, [#446]) ------------------------------------

class BundleCollisionError(RuntimeError):
    """Generation refused: the target bundle directory already holds git-tracked files.

    R5 (Option D, ruled 2026-07-31): the guarded target set is any bundle directory
    containing GIT-TRACKED files — a committed bundle is an immutable artifact, so
    re-rendering over it is a silent overwrite of shipped state. The refusal is the
    DEFAULT; `--allow-suffix` is the explicit opt-in. Silent suffixing was rejected
    because it converts today's collision into tomorrow's `_select_active_bundle`
    ambiguous-FAIL (audit.py:1575)."""


def _tracked_under(repo_root: Path, path: Path) -> list[str]:
    """Repo-relative paths of GIT-TRACKED files under `path` ([] when none).

    Raises `BundleCollisionError` when tracking status cannot be DETERMINED — see
    `_resolve_bundle_dir`. Three outcomes, deliberately distinct (codex HIGH, 2026-07-31):

      not a git repo      -> []      nothing can be tracked; generation proceeds
      git answered, empty -> []      genuinely untracked; generation proceeds
      git errored/absent  -> RAISE   status UNKNOWN; refusing beats guessing

    The first draft returned [] for all three, so any git failure authorized the target and
    an inherited bogus GIT_DIR silently disarmed the RM-8 refusal against a genuinely tracked
    bundle ([#355]'s class). The env is now scrubbed via `_git_status`, so that redirection
    cannot happen at all; this split is the belt to that braces."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return []                       # outside the repo -> git could not track it anyway
    if not (repo_root / ".git").exists():
        return []                       # not a git repo: a knowable, legitimate empty answer
    ok, out = _git_status(repo_root, "ls-files", "--", rel)
    if not ok:
        raise BundleCollisionError(
            f"refusing to generate into {path}: git could not report whether that directory "
            f"holds tracked files, so its status could not be determined. An unknown status is "
            f"not an empty one — proceeding could silently overwrite a committed bundle. Fix "
            f"the git environment (an inherited GIT_DIR is the usual cause) and re-run."
        )
    return [ln for ln in out.splitlines() if ln.strip()]


def _resolve_bundle_dir(repo_root: Path, bundle_root: Path, slug: str,
                        allow_suffix: bool) -> Path:
    """The directory this generation may write, or raise `BundleCollisionError` (R5).

    Clean target (absent, or present-but-untracked — the in-flight bundle being
    regenerated, the `--filled` reflow) -> returned unchanged, so re-rendering an
    uncommitted bundle keeps working. Tracked target -> REFUSE by default; with
    `allow_suffix` -> the first NONEXISTENT `-2`, `-3`, … sibling (the repo's own
    witnessed convention, e.g. `2026-07-02-dev-knowledge-architect-2`).

    The suffix scan tests EXISTENCE, not tracked-ness (codex HIGH, 2026-07-31). Scanning
    for "no tracked files" selected an EXISTING directory holding untracked in-progress
    work and then wrote into it — reproduced with real data loss. `--allow-suffix` promises
    a NEW sibling, so nothing that already exists is selectable, tracked or not."""
    target = bundle_root / slug
    tracked = _tracked_under(repo_root, target)
    if not tracked:
        return target
    if not allow_suffix:
        raise BundleCollisionError(
            f"refusing to generate into {target}: that bundle directory already holds "
            f"{len(tracked)} git-tracked file(s) (e.g. {tracked[0]}). A committed bundle is "
            f"an immutable artifact — re-rendering would silently overwrite shipped state. "
            f"Pass a different --slug, or re-run with --allow-suffix to write a NEW sibling "
            f"directory and leave {slug} untouched."
        )
    n = 2
    while (bundle_root / f"{slug}-{n}").exists():
        n += 1
    return bundle_root / f"{slug}-{n}"


class BundleIdentityError(RuntimeError):
    """Seal refused: a bundle's own internal slug does not name its own directory.

    [#473] B. A bundle that mislabels itself is a plausible-but-wrong artifact — it renders
    cleanly, it commits cleanly, and its probe locators RESOLVE (they name a sibling that
    exists), so nothing downstream can tell it is pointing at the wrong bundle. The system
    already refuses this class rather than shipping it (the `residual_completeness` gate on
    unfilled FILL-IN regions is the precedent), so the refusal belongs at seal time, where a
    defect is still cheap. Once a bundle is committed it is immutable and the defect is
    permanent — absorbed at check time by the verifier's locator rebase, but never fixable."""


# The HANDOFF_BOOT / EPIC_BOOT `Slug` row: `| **Slug** | `<slug>` |`.
_SLUG_ROW_RE = re.compile(r"^\|\s*\*\*Slug\*\*\s*\|\s*`(?P<slug>[^`]+)`\s*\|", re.MULTILINE)

# The boot file each mode seals its identity in. `functional` carries no Slug row (a single
# minimal FUNCTIONAL_BOOT.md, §16) and so is not identity-gated.
_BOOT_FILES = ("HANDOFF_BOOT.md", "EPIC_BOOT.md")


def verify_seal_identity(bundle_dir: Path) -> None:
    """Refuse to seal a bundle whose internal slug != its own directory name ([#473] B).

    A no-op when the bundle carries no boot file with a `Slug` row (functional mode), so the
    gate never invents a requirement a mode does not have. Raises `BundleIdentityError`
    otherwise — naming BOTH values, because "they disagree" without the two strings is a
    message that cannot be acted on."""
    bundle_dir = Path(bundle_dir)
    for name in _BOOT_FILES:
        boot = bundle_dir / name
        if not boot.is_file():
            continue
        m = _SLUG_ROW_RE.search(boot.read_text(encoding="utf-8"))
        if m is None:
            continue
        declared = m.group("slug").strip()
        if declared != bundle_dir.name:
            raise BundleIdentityError(
                f"refusing to seal {bundle_dir}: its {name} declares slug '{declared}' but the "
                f"bundle directory is '{bundle_dir.name}'. A bundle whose internal slug names a "
                f"DIFFERENT directory points every self-reference it carries (the Slug field, "
                f"the PROBES P0c/P3/P8 locators, the embedded /handoff-verify command) at "
                f"another bundle — which then verifies green about the wrong file, because the "
                f"sibling exists. Regenerate; do not hand-patch the sealed artifact."
            )


# --- boundary invariants: WINDOW = BATCH + no leftovers (ARC-HANDOFF-ENGINE) ----

class OpenBatchError(RuntimeError):
    """Generation refused: a committed batch manifest declares an OPEN batch.

    WINDOW = BATCH (PLAYBOOK Ch8; ADR-110 records it as the batch protocol's Rhythm row).
    One batch is one window and the seal fires at true batch boundaries, because a
    mid-batch cut produces a bundle describing a tree nobody has integrated yet — the
    successor then boots against a manifest the rest of the batch is about to invalidate.
    That was doctrine with no organ behind it at the one site where the cost is permanent:
    `docs/handoffs/` is immutable, so a bundle sealed mid-batch is wrong forever.

    The refusal reuses `batch_manifest.open_batches` rather than re-deriving openness. A
    second notion of "a batch is open" would drift from the one `audit.py` reads, and the
    two would disagree exactly when it mattered.
    """


class BoundaryHygieneError(RuntimeError):
    """Generation refused: the tree is not at a clean session boundary.

    CLAUDE.md §5 rule 9 (no leftovers) and the batch protocol's refuse-to-finish items
    3 and 5, applied at the cut. A bundle taken over an un-torn-down lane worktree or a
    live stash seals a claim about a boundary the tree has not reached, and the stash leg
    is the one the others structurally cannot cover: `refs/stash` lives in the COMMON git
    directory, so a lane's stash survives every worktree- and branch-shaped teardown
    (batch-1 F4).

    HONEST LIMIT, stated rather than papered over: `git stash list` reports no worktree of
    origin, so this cannot tell a forgotten lane stash from the operator's deliberate one.
    It refuses either way and names the entry, because guessing is how real work gets
    dropped — and clearing a deliberate stash is a decision, not a default.
    """


def _open_batches(repo_root: Path) -> list:
    """Committed manifests declaring an open batch right now — via the ONE shared reader.

    Degrades to `[]` when the reader is unavailable, matching `open_batches`' own
    fail-toward-no-exemption posture: an unknown batch state renders as "no batch", the
    same direction the gate side already takes.
    """
    sys.path.insert(0, str(_SCRIPTS))
    try:
        from batch_manifest import open_batches  # noqa: PLC0415
    except Exception:                            # noqa: BLE001 -- unavailable => no batch
        return []
    return list(open_batches(Path(repo_root)))


def assert_batch_boundary(repo_root: Path) -> None:
    """Raise `OpenBatchError` when a committed manifest declares a batch still open."""
    live = _open_batches(repo_root)
    if not live:
        return
    named = "; ".join(
        f"batch {b.batch} (declared by {b.path}, closes when {b.closed_by} lands)"
        for b in live
    )
    raise OpenBatchError(
        f"refusing to cut a bundle while a batch is open: {named}. WINDOW = BATCH — the "
        f"seal fires at a true batch boundary, because a bundle cut now describes a tree "
        f"the rest of the batch has not been integrated into, and a committed bundle is "
        f"immutable. Land the closing packet, then cut."
    )


def _linked_worktrees(repo_root: Path) -> list[str]:
    """Paths of LINKED worktrees ([] when the primary is the only one).

    `git worktree list --porcelain` always emits the primary first; counting it as a
    leftover would refuse every cut ever taken, so it is the baseline rather than a
    finding. A git failure raises — see `assert_boundary_hygiene`.
    """
    ok, out = _git_status(repo_root, "worktree", "list", "--porcelain")
    if not ok:
        raise BoundaryHygieneError(
            "refusing to generate: `git worktree list` failed, so whether this tree carries "
            "leftover worktrees could not be determined. An unknown boundary is not a clean "
            "one. Fix the git environment and re-run."
        )
    paths = [ln.split(" ", 1)[1].strip()
             for ln in out.splitlines() if ln.startswith("worktree ")]
    return paths[1:]


def _stash_entries(repo_root: Path) -> list[str]:
    """`git stash list` entries ([] when empty). A git failure raises, same reason."""
    ok, out = _git_status(repo_root, "stash", "list")
    if not ok:
        raise BoundaryHygieneError(
            "refusing to generate: `git stash list` failed, so whether this tree carries a "
            "live stash could not be determined. An unknown boundary is not a clean one. "
            "Fix the git environment and re-run."
        )
    return [ln for ln in out.splitlines() if ln.strip()]


def assert_boundary_hygiene(repo_root: Path) -> None:
    """Raise `BoundaryHygieneError` naming EVERY leftover, or return cleanly.

    Degrade contract, matching `_tracked_under`: not a git repo -> nothing can be
    provisioned or stashed -> proceed. git present but erroring -> refuse (the RM-8
    ruling: an undetermined status is not an empty one). Every leftover is reported in
    one refusal, because naming only the first invites a fix-and-retry loop that reveals
    the next one.
    """
    if not (Path(repo_root) / ".git").exists():
        return
    leftovers = [f"linked worktree {p}" for p in _linked_worktrees(repo_root)]
    leftovers += [f"stash entry {s}" for s in _stash_entries(repo_root)]
    if leftovers:
        raise BoundaryHygieneError(
            "refusing to generate: the tree is not at a clean session boundary — "
            + "; ".join(leftovers)
            + ". A bundle cut here seals a claim about a boundary the tree has not reached "
              "(CLAUDE.md §5 rule 9; the batch protocol's refuse-to-finish items 3 and 5). "
              "Tear down or dispose of each, then cut."
        )


def collect_hints(repo_root: Path) -> dict[str, str]:
    """Best-effort generation-time drift-reference VALUES — for the JOURNAL draft ONLY.

    These are exactly the probes' answers (HEAD sha, ALL_CHECKS count, backlog counts,
    ship-gate verdict). They are collected here and returned ONLY to `journal_draft`; no
    render function is ever handed this dict, which is what makes the bundle answer-free by
    construction. Every leg degrades to a "run <command>" pointer on failure — a generator
    that cannot compute a hint must never guess it into the bundle.
    """
    h: dict[str, str] = {}
    head = _git(repo_root, "rev-parse", "--short", "HEAD")
    status = _git(repo_root, "status", "-sb")
    h["head"] = head or "unknown (run `git rev-parse --short HEAD`)"
    h["tree"] = "clean" if not _git(repo_root, "status", "--porcelain") else "DIRTY"
    h["status_line"] = status.splitlines()[0] if status else "unknown (run `git status -sb`)"
    # ALL_CHECKS count + last name via import (cheap, no side effects at import).
    try:
        sys.path.insert(0, str(repo_root / "scripts"))
        import audit as _aud  # noqa: PLC0415
        h["all_checks"] = f"{len(_aud.ALL_CHECKS)} (last `{_aud.ALL_CHECKS[-1].__name__.removeprefix('check_')}`)"
    except Exception:  # noqa: BLE001 — best-effort; never fail generation on a hint
        h["all_checks"] = "unknown (run `python scripts/audit.py checks`)"
    # ship-gate + backlog counts are expensive/verbose — the draft points at the command
    # rather than baking a possibly-stale value (and never blocks generation on them).
    h["ship_gate"] = "run `python scripts/audit.py ship-gate` (GREEN/RED + dispositioned-WARN count + any [stale])"
    h["backlog"] = "run `python scripts/validate_backlog.py` (themes/stories/tasks + serialize-groups)"
    return h


def _vision_extract(repo_root: Path) -> str:
    """The committed body of VISION.md's `## Vision` section (text after the `## Vision`
    line up to the next `## `-level heading or EOF, stripped). Degrade contract: a
    generator that cannot compute this must never guess it — on a missing file or a
    missing `## Vision` section, return a literal, unmistakably-a-placeholder string
    rather than inventing prose.

    RETIRED-TIER FALLBACK, REGISTRY-DRIVEN ([#614], 2026-09-01). When the registry has
    retired VISION (`canonical_docs.CANONICAL_RETIRED`) and the root file is gone, the live
    `## Vision` H2 is README.md's — ADR-114 made README the front door, DC-1 moved the
    content there, and `templates/handoff/v5/PROBES.md.tmpl` P1a already points at it.
    Falling back keeps the degrade contract honest in the direction that matters: the
    placeholder means "cannot compute", and after a ruled relocation it CAN be computed, so
    degrading every new handoff bundle would be inventing an absence rather than reporting
    one. The fallback fires ONLY for a retired name — a non-retired VISION that goes
    missing still degrades, because that is a real defect a boot should surface."""
    def _section(path: Path) -> "str | None":
        if not path.exists():
            return None
        text = path.read_text(encoding="utf-8")
        m = re.search(rf"^{re.escape(_cdocs.VISION_EXTRACT_HEADING)}\s*\n(.*?)(?=^## |\Z)",
                      text, re.DOTALL | re.MULTILINE)
        return m.group(1).strip() if m else None

    found = _section(repo_root / _cdocs.VISION)
    if found is not None:
        return found
    if _cdocs.VISION in _cdocs.CANONICAL_RETIRED:
        found = _section(repo_root / _cdocs.README)
        if found is not None:
            return found
    return _cdocs.VISION_EXTRACT_MISSING


def _intake_index(repo_root: Path) -> str:
    """Enumerate `docs/intake/*.md` (excluding README.md) as a committed-state bullet index —
    filename, `intake-id` + `status` from the leading frontmatter, and the doc title (its
    first `# ` heading, falling back to the filename stem). Degrade contract: an absent or
    empty docs/intake/ directory returns a literal "no intake docs yet" marker, never a guess;
    a doc that fails to parse still gets a bullet (fallback fields), never gets dropped
    silently. Deliberately no count/total line (answer-free scoping, §16)."""
    intake_dir = repo_root / "docs" / "intake"
    if not intake_dir.is_dir():
        return "(no intake docs yet)"
    docs = sorted(p for p in intake_dir.glob("*.md") if p.name != "README.md")
    if not docs:
        return "(no intake docs yet)"
    lines = []
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        intake_id = "?"
        status = "?"
        title = doc.stem
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                frontmatter = text[3:end]
                for line in frontmatter.splitlines():
                    if ":" not in line:
                        continue
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip()
                    if key == "intake-id" and value:
                        intake_id = value
                    elif key == "status" and value:
                        status = value
                body = text[end + len("\n---"):]
            else:
                body = text
        else:
            body = text
        heading = re.search(r"^# (.+)$", body, re.MULTILINE)
        if heading:
            title = heading.group(1).strip()
        lines.append(f"- `{doc.name}` — intake-id {intake_id} · {status} · {title}")
    return "\n".join(lines)


# --- R2: the generated Standing-vs-NEW attribution frame --------------------
#
# 47 of 86 bundles hand-authored a standing-WARN paragraph (avg 1,847 B) saying the same thing
# in different words every window: which drift-flags are standing and which are this window's
# (2026-08-26 handoff census, item R2/b1 — the largest single mechanizable class it measured).
# The discriminator was already written down, in the 2026-08-25 driftflags region: "attribute a
# WARN by asking whether the arc's diff touched the file it fires against, not by counting."
# That is computable, so it is computed here and the hand region narrows to the one judgment a
# generator cannot make — which NEW flag is a DECISION rather than a defect.
#
# WHAT THIS BLOCK DOES NOT DO, and the reason it is safe to put in a browser-visible file: it
# never runs the audit. It carries no ship-gate verdict, no WARN count, no [stale] line, no sha,
# no #id — nothing that is any probe's ANSWER. It is an ATTRIBUTION FRAME over two committed
# inputs (the disposition register and the window's own diff), which is exactly what the hand
# paragraph was, minus the seat having to re-derive it from memory. The values stay live and
# stay P7/P4/P6/P9's to produce at check-time. `collect_hints` remains the only place that
# touches answer values, and it still reaches only `journal_draft`.
_HISTORY_BINDING = ":git-history:"

# The standing-WARN family, bound to what each organ reads. CURATED, with a reason per row —
# the "kept-as-manifest with a reason" form `ecosystem/disposition-register.yaml`'s own header
# blesses — because there is no auto-enumerable organ->corpus map to derive it from.
#
# SCOPE IS DELIBERATE AND STATED IN THE RENDERED BLOCK: these are the organs bundles actually
# narrate (census 1.2 — no_ff_merges 25, undeclared_edges 22, doc_rot 21, reconciled_versions
# 15, fleet_parity 10, journal_spine_anchor 7, plus funnel_coverage, which carries 34 of the
# register's entries). An organ outside the family is not silently attributed; it stays the
# FILL-IN's business, and the block says so rather than reading as exhaustive.
# tests/test_gen_handoff.py asserts every key is a live ALL_CHECKS registry name, so the
# manifest cannot rot into naming a retired organ.
_DRIFT_ORGAN_BINDINGS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("no_ff_merges", (_HISTORY_BINDING,),
     "fires against main's first-parent spine, not against a file"),
    ("journal_spine_anchor", (_HISTORY_BINDING, "JOURNAL.md"),
     "fires against the spine ∩ JOURNAL anchors, not against a file alone"),
    ("doc_rot", ("BACKLOG.md", "CLAUDE.md", "ARCHITECTURE.md", "VISION.md", "CONTRIBUTING.md",
                 "protocols/", "docs/decisions/"),
     "reads BACKLOG.md + the hub living docs"),
    ("undeclared_edges", ("scripts/", "pyproject.toml", "ecosystem/dependency-baseline.yaml"),
     "reads the code edge — scripts/ against the declared dependency surfaces"),
    ("reconciled_versions", ("protocols/HANDOFF_PROCESS.md", "templates/prompt-template.md",
                             "docs/handoffs/README.md", "CLAUDE.md"),
     "reads the registered specs and the docs declaring a `reconciled_with:` edge"),
    ("fleet_parity", ("ecosystem/", "deploy/", ".claude/", "templates/"),
     "reads the parity-surface manifest and the surfaces it names"),
    ("funnel_coverage", ("docs/audits/",),
     "reads docs/audits/ disposition coverage"),
)


def _register_organs(repo_root: Path) -> list[str]:
    """Distinct `organ:` names in `ecosystem/disposition-register.yaml`, sorted.

    Parsed line-wise rather than via yaml so this stays a pure read with no import cost and
    no failure mode of its own; the field is a flat scalar in every entry. Returns [] when the
    register is absent or unreadable, and the caller degrades loudly rather than guessing."""
    register = repo_root / "ecosystem" / "disposition-register.yaml"
    try:
        text = register.read_text(encoding="utf-8")
    except OSError:
        return []
    return sorted({m.group(1) for m in re.finditer(r"^\s+organ:\s*(\S+)\s*$", text, re.M)})


def _window(repo_root: Path) -> tuple[str, list[str]] | None:
    """`(previous-bundle-slug, changed-paths)` for this handoff's window, or None.

    The window is the diff since the PREVIOUS bundle was added — the same boundary the
    residual's "shipped this window" map describes, resolved from git rather than from the
    seat's memory of when the last handoff was. The bundle being generated now is untracked, so
    the newest ADD of a `docs/handoffs/*/HANDOFF_BOOT.md` is the previous one by construction.

    Returns None when git is unavailable or there is no prior bundle — a generator that cannot
    compute the window says so; it never guesses a range."""
    ok, sha = _git_status(repo_root, "log", "-1", "--format=%H", "--diff-filter=A",
                          "--", "docs/handoffs/*/HANDOFF_BOOT.md")
    if not ok or not sha:
        return None
    ok, paths = _git_status(repo_root, "show", "--name-only", "--format=", sha)
    prev = ""
    for rel in (paths.splitlines() if ok else []):
        parts = rel.strip().split("/")
        if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "handoffs":
            prev = parts[2]
            break
    ok, diff = _git_status(repo_root, "diff", "--name-only", f"{sha}..HEAD")
    if not ok:
        return None
    return (prev or "the previous bundle",
            [ln.strip() for ln in diff.splitlines() if ln.strip()])


def _touched(bindings: tuple[str, ...], changed: list[str]) -> bool:
    """True if the window's diff touched anything an organ with these bindings reads.

    `_HISTORY_BINDING` means the organ fires against git history rather than a file, so ANY
    non-empty window can have introduced its concern — fail-toward-NEW, which puts the organ in
    front of the seat instead of quietly filing it as standing."""
    for b in bindings:
        if b == _HISTORY_BINDING:
            if changed:
                return True
        elif b.endswith("/"):
            if any(c.startswith(b) for c in changed):
                return True
        elif b in changed:
            return True
    return False


def standing_vs_new(repo_root: Path) -> str:
    """Render the generated `Standing vs NEW` block for RESIDUAL.md §1 (census R2).

    Three lists of ORGAN NAMES and nothing else: dispositioned-by-register /
    dispositioned-by-absence-from-the-window-diff / NEW-and-undispositioned. No verdict, no
    count, no sha, no `#id` — the anti-bluff contract is untouched, and the block says so in
    its own first line so a seat reading it cannot mistake a frame for an answer."""
    header = ("> **Standing vs NEW — generated, names only.** Three lists computed from "
              "`ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, "
              "count, stale-disposition line, sha or backlog id appears here** — those are "
              "P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the "
              "standing-WARN family only; an organ outside it is the FILL-IN's business, not "
              "silently filed as standing.\n")
    win = _window(repo_root)
    if win is None:
        return (header + "\n_Window unresolved (git unavailable, or no prior bundle to measure "
                "from) — the frame is not computed. Re-derive by hand: compare the window's "
                "changed paths against what each organ reads._")
    prev, changed = win
    registered = set(_register_organs(repo_root))
    if not registered:
        return (header + "\n_Disposition register unreadable — the frame is not computed, "
                "rather than computed against an empty register (which would file every organ "
                "as NEW)._")
    by_register, by_absence, new = [], [], []
    for organ, bindings, why in _DRIFT_ORGAN_BINDINGS:
        if organ in registered:
            by_register.append(f"`{organ}`")
        elif _touched(bindings, changed):
            new.append(f"`{organ}` ({why})")
        else:
            by_absence.append(f"`{organ}` ({why})")

    def _list(items: list[str]) -> str:
        return "\n".join(f"- {i}" for i in items) if items else "- _(none)_"

    return (
        f"{header}\n"
        f"**Window** — the diff since `docs/handoffs/{prev}/` was added.\n\n"
        "**Dispositioned by the register.** The register already carries an entry for these "
        "organs, so a WARN from one is standing unless its evidence signature is new:\n"
        f"{_list(by_register)}\n\n"
        "**Dispositioned by absence from the window diff.** This window touched nothing these "
        "organs read, so a WARN from one is not this window's doing:\n"
        f"{_list(by_absence)}\n\n"
        "**NEW-and-undispositioned.** No register entry, and this window DID touch what they "
        "read — so a WARN from one of these is this window's, and the note below says which is "
        "a decision rather than a defect:\n"
        f"{_list(new)}"
    )


# --- R5: the ruled dispatch verb, rendered rather than copied ---------------

def dispatch_form(repo_root: Path) -> str:
    """The forms card's dispatch line, READ from PLAYBOOK Ch8's dispatch table at generation.

    The forms card exists because "a pointer works for prose a seat reads once, and fails for a
    command a seat types" — but a copied command is what STANDING_RULINGS §V ruled on, after four
    rival copies of this exact line cost roughly thirty consecutive seats a lane. Rendering
    resolves the two: the seat gets the literal line, resident in its paste, and the tree still
    has exactly one source for it.

    DEGRADE TO A POINTER, never to a remembered command. If Ch8's table cannot be read the card
    tells the seat to open it — a stale copy that renders confidently is the failure mode."""
    try:
        from scripts import dispatch_surface as _ds  # noqa: PLC0415
    except ImportError:
        try:
            import dispatch_surface as _ds           # noqa: PLC0415
        except ImportError:
            _ds = None
    lines = _ds.ruled_form(repo_root) if _ds is not None else None
    if not lines:
        return ("> **The literal line could not be rendered from Ch8** — read it live at "
                "`protocols/PLAYBOOK.md` \"The dispatch table — the SOLE literal-command site\". "
                "This card deliberately carries no copy of its own.")
    body = "\n".join(lines)
    return f"```\n{body}\n```"


def detect_fill_state(bundle_dir: Path) -> bool:
    """True => FILLED framing, False => cold. Reuses assemble_paste._extract_answers so the
    framing flip matches EXACTLY what the assembler folds (one fill-state definition)."""
    sup = bundle_dir / "SUPPLEMENT.md"
    if not sup.exists():
        return False
    sys.path.insert(0, str(_SCRIPTS))
    from assemble_paste import _extract_answers  # noqa: PLC0415
    return _extract_answers(sup.read_text(encoding="utf-8")) is not None


def reflow_framing(bundle_dir: Path) -> list[str]:
    """Flip the fill-state framing blocks (SUPPLEMENT_BANNER / P1_GATE_NOTE / PASTE_STEP6) from
    their COLD text to their FILLED text, IN PLACE, in an already-rendered bundle whose SUPPLEMENT
    was FILLED *after* a cold generation. This is what lets the documented fill step
    (`assemble_paste.py`) actually flip the boilerplate the operator sees — §13's "the cold->FILLED
    flip is mechanized via the assembler" — WITHOUT a full template re-render, so hand-authored
    FILL-IN narrative is never clobbered: it replaces only the exact framing block, so differently
    worded prose that merely mentions "generated EMPTY" is not matched. No-op (returns []) on a cold
    / unfilled supplement, and idempotent once flipped. Returns the file names it changed."""
    if not detect_fill_state(bundle_dir):
        return []
    flipped: list[str] = []
    for name in ("HANDOFF_BOOT.md", "RESIDUAL.md", "PROBES.md"):
        f = bundle_dir / name
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        new = text
        for cold, warm in _FRAMING.values():
            new = new.replace(cold, warm)
        if new != text:
            f.write_text(new, encoding="utf-8", newline="\n")
            flipped.append(name)
    return flipped


# --- rendering (fence-aware; framing tokens only, never a hint value) --------

# A FILL-IN region: <!-- FILL-IN:<name> START ... --> body <!-- FILL-IN:<name> END -->.
_FILL_RE = re.compile(
    r"(?P<open><!-- FILL-IN:(?P<name>[\w-]+) START.*?-->)"
    r"(?P<body>.*?)"
    r"(?P<close><!-- FILL-IN:(?P=name) END -->)",
    re.DOTALL,
)


def _splice_fill_regions(rendered: str, existing: str | None) -> str:
    """Copy each FILL-IN region's body BYTE-FOR-BYTE from `existing` into `rendered` (RF-6:
    a re-render / --filled flip never clobbers hand-authored narrative). Regions present only
    in the template keep their placeholder; only same-named regions are carried over."""
    if not existing:
        return rendered
    prior = {m.group("name"): m.group("body") for m in _FILL_RE.finditer(existing)}
    def _repl(m: re.Match) -> str:
        name = m.group("name")
        if name in prior:
            return m.group("open") + prior[name] + m.group("close")
        return m.group(0)
    return _FILL_RE.sub(_repl, rendered)


def _tokens(mode: str, slug: str, repo: str, date: str, state: _State, filled: bool) -> dict[str, str]:
    """The structural / framing substitutions. NO probe-answer value appears here — only the
    session identity, the mode framing, the sanctioned {{BRANCH}} pointer, and the fill-state
    framing. (Verified by the recurring dogfood: no rendered row carries an answer-hint.)

    {{BRANCH}} and {{BOOT_DESTINATION}} answer DIFFERENT questions and must stay separate tokens:
    the first is "which branch was this cut on?" (the `Generated at` pointer / PROBES branch note),
    the second is "where does the seat land at boot?" (the `Destination` row, P3's operand)."""
    return {
        "MODE": mode,
        "SLUG": slug,
        "REPO": repo,
        "DATE": date,
        "BRANCH": state.branch,
        "BOOT_DESTINATION": _PRIMARY_TREE_BOOT_DESTINATION,
        "MODE_SCOPE": _MODE[mode]["scope"],
        "MODE_POSTURE": _MODE[mode]["posture"],
        "SUPPLEMENT_BANNER": _framing("SUPPLEMENT_BANNER", filled),
        "P1_GATE_NOTE": _framing("P1_GATE_NOTE", filled),
        "PASTE_STEP6": _framing("PASTE_STEP6", filled),
        # #287: slug-based title for architect/execution/functional; the epic branch of
        # generate() overrides this with an epic-slug-aware title after EPIC_SLUG is resolved.
        "CHAT_TITLE": _chat_title(mode, repo, slug),
    }


def _substitute(template: str, tokens: dict[str, str]) -> str:
    out = template
    for k, v in tokens.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def _strip_leading_comment(text: str) -> str:
    """Drop a leading `<!-- ... -->` template-authoring note (it explains the .tmpl, not the
    bundle) so it does not ship in the rendered file. Anchors the close to the `-->` that
    precedes the first markdown heading, so a stray `-->` inside the note cannot truncate it
    early (HTML comments don't nest); if no heading follows, the text is left unchanged."""
    return re.sub(r"\A<!--.*?-->\s*(?=#)", "", text, count=1, flags=re.DOTALL)


def _render(tmpl_name: str, tokens: dict[str, str], bundle_dir: Path, out_name: str,
            tmpl_dir: Path = _TMPL_DIR) -> None:
    tmpl = (tmpl_dir / tmpl_name).read_text(encoding="utf-8")
    rendered = _strip_leading_comment(_substitute(tmpl, tokens))
    existing = bundle_dir / out_name
    prior = existing.read_text(encoding="utf-8") if existing.exists() else None
    rendered = _splice_fill_regions(rendered, prior)
    existing.write_text(rendered, encoding="utf-8", newline="\n")


# --- FM-4: the FUNNEL HEALTH block ------------------------------------------
#
# WHAT IT IS. Eleven numbers about the governance funnel, emitted into every bundle that has
# more than one file, so the seat that boots a window can see the funnel's state without
# asking. Numbers ONLY: no verdict, no sha, no backlog id. "funnel healthy" is a claim the
# reader cannot check; "leg a1 intakes terminal-unarchived: 7" is one they can.
#
# ONE TRUTH — DERIVED, NEVER RECOMPUTED. The numbers come from FM-2's derivation module, the
# same one `check_funnel_lifecycle` uses. This file re-implements NOTHING: a second answer to
# "is this intake consumed?" is precisely the defect the FM batch exists to remove. The whole
# coupling is the module name + entry point below and the keys in `_FUNNEL_FIELDS`.
#
# THE COUPLING WAS DEAD ON ARRIVAL, and the repair is `[#619]`. FM-2 (lane I) had not landed
# when this block was written, so its six fields were authored against a DECLARED shape and
# never against a file that was read. Lane I landed a different one: six attribute names read,
# zero of them present, every field rendering `unavailable` in every bundle ever cut — an
# intersection of EMPTY, held green by nothing but a golden test that pinned the labels rather
# than the coupling. The mapping is now RULED, field by field, at
# `docs/audits/2026-08-29-technical-batchd-a-619-fm-coupling-packet.md` §2.
#
# THE RULE, so the mapping is checkable rather than hand-kept: this block renders EVERY
# `int`-typed field of `funnel_lifecycle.Measurement`, plus ONE count per `LEG_*` constant.
# Nothing else, nothing less. `test_funnel_fields_cover_fm2s_whole_int_and_leg_surface`
# asserts that set equality BOTH ways against the live module, so a field added to FM-2,
# removed from it, or renamed REDs this file instead of silently re-opening the empty
# intersection. Excluded, deliberately: `detector` (a string, already on the `source:` line),
# `threshold_days` / `threshold_locator` (annotated `int | None` / `str | None` — leg (d)'s
# PARAMETERS, and a `None` would render `unavailable` by default, which the repair bars), and
# `violations` (rendered as the five per-leg counts; one total would hide which leg moved).
_FUNNEL_MODULE = "funnel_lifecycle"
_FUNNEL_ENTRY = "measure"
_FUNNEL_SOURCE = f"scripts/{_FUNNEL_MODULE}.py::{_FUNNEL_ENTRY} (FM-2)"

#: How a field reads its number off FM-2's measurement.
_FUNNEL_ATTR = "attr"   #: an `int`-typed dataclass field, read directly
_FUNNEL_LEG = "leg"     #: the violation count for one of FM-2's failure legs, via `by_leg()`

# (rendered label, kind, key on FM-2's measurement). ORDER IS THE CONTRACT'S ORDER and the
# golden test pins it: the corpus this measurement was taken over first, then one count per
# failure leg. The denominators are NOT decoration — `0` violations out of `0` post-cutoff rows
# and `0` out of `13` are different facts, and a bare zero cannot tell them apart.
_FUNNEL_FIELDS = (
    ("intakes live", _FUNNEL_ATTR, "live_intakes"),
    ("intakes archived", _FUNNEL_ATTR, "archived_intakes"),
    ("intakes READY", _FUNNEL_ATTR, "ready_intakes"),
    ("ADRs live", _FUNNEL_ATTR, "live_adrs"),
    ("rows", _FUNNEL_ATTR, "rows"),
    ("rows post-cutoff", _FUNNEL_ATTR, "post_cutoff_rows"),
    ("leg a1 intakes terminal-unarchived", _FUNNEL_LEG, "terminal-not-archived"),
    ("leg a2 intakes ACCEPTED, every named row terminal", _FUNNEL_LEG, "accepted-rows-terminal"),
    ("leg b ADRs terminal-unarchived", _FUNNEL_LEG, "adr-terminal-not-archived"),
    ("leg c rows post-cutoff, provenance unresolved", _FUNNEL_LEG, "row-provenance-unresolved"),
    ("leg d READY intakes past threshold", _FUNNEL_LEG, "ready-past-threshold"),
)

_FUNNEL_BEGIN = "<!-- FUNNEL-HEALTH:BEGIN (generated by gen_handoff — do not edit) -->"
_FUNNEL_END = "<!-- FUNNEL-HEALTH:END -->"
_FUNNEL_UNAVAILABLE = "unavailable"
_FUNNEL_FILE = "FUNNEL_HEALTH.md"


def _load_funnel_measure():
    """Resolve FM-2's derivation entry point. Returns `(module | None, callable | None, note)`.

    The MODULE is returned alongside the callable because the leg keys in `_FUNNEL_FIELDS` are
    validated against FM-2's own `LEG_*` constants at render time (`_funnel_leg_names`). Without
    that, a renamed leg would make `by_leg("<old name>")` return `[]` and this block would
    publish a confident `0` — a false clean, which is strictly worse than `unavailable` and is
    the exact failure class `[#619]` was filed for.

    Both import spellings are tried because this module is reached BOTH as `scripts.gen_handoff`
    (package import) and as bare `gen_handoff` with `scripts/` on `sys.path` — the same
    dual-entry the `canonical_docs` import at the top of this file handles. The PACKAGE-qualified
    spelling is tried FIRST, deliberately: the bare name resolves against the whole of `sys.path`,
    so an unrelated `funnel_lifecycle` installed anywhere on it would be loaded and its numbers
    published under FM-2's name (terra HIGH, 2026-08-29). `scripts.` names this repo or nothing.

    A module that EXISTS but cannot import (a broken transitive dependency) is reported as such
    rather than as "has not landed" — the two are different facts and the block must not assert
    the wrong one."""
    mod = None
    for name in (f"scripts.{_FUNNEL_MODULE}", _FUNNEL_MODULE):
        try:
            mod = importlib.import_module(name)
            break
        except ModuleNotFoundError as exc:
            if exc.name not in (name, _FUNNEL_MODULE, "scripts"):
                return None, None, (f"present, but its own import raised "
                                    f"ModuleNotFoundError: {exc.name}")
        except ImportError as exc:
            return None, None, f"present, but its import raised {type(exc).__name__}"
    if mod is None:
        return None, None, "not importable — FM-2 has not landed; this coupling is unproven"
    fn = getattr(mod, _FUNNEL_ENTRY, None)
    if not callable(fn):
        return mod, None, f"imported, but exposes no callable `{_FUNNEL_ENTRY}`"
    return mod, fn, ""


def _funnel_leg_names(mod) -> frozenset:
    """FM-2's OWN leg names, read off its `LEG_*` constants.

    The render-time half of the anti-drift guard. `Measurement.by_leg` filters a list and so
    answers `[]` for a name it has never heard of, which is indistinguishable from `[]` for a
    leg with no violations. Asking the module which legs it actually has turns that silent
    false-`0` into an honest `unavailable`.
    """
    return frozenset(v for k, v in vars(mod).items()
                     if k.startswith("LEG_") and isinstance(v, str))


def _funnel_health_numbers(repo_root: Path) -> tuple[dict[str, str], str]:
    """The numbers as rendered strings, plus a note when any of them could not be derived.

    Every field degrades INDEPENDENTLY to `unavailable`: a measurement that grows a field this
    module does not know about still renders, and one that loses a field says so instead of
    printing a stale or invented value. `bool` is excluded deliberately — `True` is an `int`
    in Python and a boolean rendered as `1` would be a verdict wearing a number's clothes."""
    values = {label: _FUNNEL_UNAVAILABLE for label, _kind, _key in _FUNNEL_FIELDS}
    mod, fn, note = _load_funnel_measure()
    if fn is None:
        return values, note
    try:
        m = fn(repo_root)
    except Exception as exc:                                    # noqa: BLE001
        # A derivation that raises must not take the bundle cut down with it: the generator's
        # job is to emit the bundle, and an honest `unavailable` is the right degrade.
        return values, f"the call raised {type(exc).__name__}"
    legs = _funnel_leg_names(mod) if mod is not None else frozenset()
    by_leg = getattr(m, "by_leg", None)
    absent: list[str] = []
    for label, kind, key in _FUNNEL_FIELDS:
        v = None
        if kind == _FUNNEL_ATTR:
            v = getattr(m, key, None)
        elif kind == _FUNNEL_LEG and key in legs and callable(by_leg):
            try:
                v = len(by_leg(key))
            except Exception:                                   # noqa: BLE001
                v = None
        if isinstance(v, int) and not isinstance(v, bool):
            values[label] = str(v)
        else:
            absent.append(key)
    return values, (f"fields absent from the measurement: {', '.join(absent)}" if absent else "")


def funnel_health_block(repo_root: Path) -> str:
    """The delimited block, verbatim as it lands in the bundle. Shape-pinned by a golden test."""
    values, note = _funnel_health_numbers(repo_root)
    source = _FUNNEL_SOURCE + (f" — {note}" if note else "")
    lines = [_FUNNEL_BEGIN, "## FUNNEL HEALTH (generated — numbers only)", "",
             f"source: {source}", ""]
    lines += [f"{label}: {values[label]}" for label, _kind, _key in _FUNNEL_FIELDS]
    lines += [_FUNNEL_END]
    return "\n".join(lines) + "\n"


def _write_funnel_health(bundle_dir: Path, repo_root: Path) -> Path:
    """Write the block to `<bundle>/FUNNEL_HEALTH.md`, WHOLE, every generation.

    Never spliced and never appended to — a stale block is worse than none, so the file is
    overwritten rather than merged. It is a bundle artifact, NOT a browser-visible one: it is
    absent from `assemble_paste`'s v5 manifest, so the answer-free invariant that governs
    BOOT / RESIDUAL / PROBES and the assembled paste is untouched by it."""
    out = bundle_dir / _FUNNEL_FILE
    out.write_text(funnel_health_block(repo_root), encoding="utf-8", newline="\n")
    return out


def journal_draft(slug: str, date: str, state: _State, hints: dict[str, str]) -> str:
    """The JOURNAL generation-entry DRAFT — printed to stdout, NEVER written into the bundle or
    auto-appended to JOURNAL.md. This is where the drift-reference VALUES live (browser never
    sees the repo), so the bundle can stay answer-free while CC still has a drift reference."""
    return (
        f"### {date} — CC: handoff `{slug}` generated (drift-reference hints — NOT in the bundle)\n\n"
        "Generation-time state, for the JOURNAL entry only (the browser has no file access and "
        "never sees this; the bundle states none of it):\n"
        f"- HEAD: `{hints['head']}` on `{state.branch}`, tree {hints['tree']} ({hints['status_line']})\n"
        f"- ALL_CHECKS: {hints['all_checks']}\n"
        f"- ship-gate: {hints['ship_gate']}\n"
        f"- backlog: {hints['backlog']}\n"
    )


# --- orchestration ----------------------------------------------------------

@dataclass(frozen=True)
class GenResult:
    bundle_dir: Path
    journal_draft: str
    filled: bool


def generate(repo_root: Path = _REPO_ROOT, *, mode: str = "architect", slug: str | None = None,
             repo: str | None = None, date: str | None = None, force_filled: bool | None = None,
             assemble: bool = True, bundle_root: Path | None = None,
             epic_slug: str | None = None, allow_suffix: bool = False) -> GenResult:
    """Emit a v5 bundle from committed repo state. Returns the bundle dir + the JOURNAL draft.

    force_filled overrides the auto-detected fill-state (RF-2's `--filled`). bundle_root defaults
    to <repo_root>/docs/handoffs (overridable for tests). SUPPLEMENT.md is written only if absent
    (an operator-filled supplement is never clobbered).

    RM-8 (R5, [#446]): generation REFUSES a target bundle directory that already holds
    git-tracked files (`BundleCollisionError`, naming the directory and the escape hatch);
    `allow_suffix=True` is the explicit opt-in that writes a fresh `-<n>` sibling instead.
    An untracked target — the bundle being generated now — is written in place as before.

    mode="epic" (§14a, ADR-97) emits the epic-lane scope-contract bundle instead:
    EPIC_BOOT.md (root-authored FILL-IN contract scaffold) + PROBES.md (boundary-scoped
    teeth) + EPIC_RETURN.md (§14b closing-report skeleton, write-if-absent — a lane-filled
    return is never clobbered). It reuses this generator's v5 assembly machinery (render /
    FILL-IN splice / structural tokens / the answer-free invariant) but assembles NO
    PASTE_THIS.md: scripts/assemble_paste.py's manifest is v5-shaped (requires RESIDUAL.md);
    the EPIC_BOOT scope-contract is the paste. `epic_slug` names the epic (branch
    `epic/<epic_slug>`, worktree `epic-<epic_slug>`); defaults to the bundle slug.

    mode="developer" (ADR-98) is a pure additive ALIAS of "epic" — normalized to "epic"
    before anything else runs, so a developer-mode bundle is byte-identical to an
    epic-mode one (the naming flip to "developer" is a deferred deprecation arc; {{MODE}}
    still renders "epic" here, intentionally).

    mode="functional" (ADR-98; HANDOFF_PROCESS §16) emits ONE file, FUNCTIONAL_BOOT.md —
    a minimal requirements-intake boot for a browser "functional architect" chat. No
    live-state probes, so no PROBES.md / RESIDUAL.md / SUPPLEMENT.md / PASTE_THIS.md and
    no assembler call: the boot IS the paste (the epic-mode precedent). It carries
    committed-state copies (a VISION.md extract, a docs/intake/ index) rather than probe
    answers — still no counts/SHAs/verdicts (the answer-free invariant, narrowed to this
    mode's shape).
    """
    # ADR-98 alias-first: "developer" is additive sugar for "epic" — normalized here,
    # before the _MODE membership check, so every downstream branch (tokens, rendering,
    # slug default) sees "epic" and the two modes' bundles are byte-identical.
    if mode == "developer":
        mode = "epic"
    if mode not in _MODE:
        raise ValueError(f"mode must be one of {sorted(_MODE)}; got {mode!r}")
    repo = repo or repo_root.name
    date = date or _dt.date.today().isoformat()
    slug = slug or f"{date}-{repo.lstrip('.')}-{mode}"
    bundle_root = bundle_root or (repo_root / "docs" / "handoffs")
    # RM-8 / R5: refuse a target that already holds git-tracked files (or, with the
    # explicit opt-in, divert to a fresh sibling). `exist_ok=True` survives ONLY on the
    # path this guard has cleared — the in-flight, not-yet-committed bundle — so the
    # documented `--filled` re-render and the FILL-IN splice keep working.
    bundle_dir = _resolve_bundle_dir(repo_root, bundle_root, slug, allow_suffix)
    # The two boundary invariants, AFTER target resolution and BEFORE anything is created:
    # a refused cut leaves no half-written directory behind (which would itself be the
    # untracked in-flight target RM-8 sanctions). RM-8 resolves first because its complaint
    # is the more specific one — it names the colliding directory.
    assert_batch_boundary(repo_root)
    assert_boundary_hygiene(repo_root)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    # [#473] B — THE FIX, and it is this one line. `_resolve_bundle_dir` may DIVERT the write
    # to a `-<n>` sibling under `--allow-suffix`, but every render token below was built from
    # the REQUESTED slug, so a diverted bundle sealed with all of its internal self-references
    # — the HANDOFF_BOOT `Slug` field, the PROBES P0c/P3/P8 locators, PASTE_THIS's embedded
    # /handoff-verify command — pointing at the SIBLING directory. Rebinding the slug to the
    # FINAL directory name makes every downstream reference derive from where the bundle
    # actually landed. `journal_draft` below picks this up too, so the JOURNAL entry names the
    # real directory rather than the one that was asked for.
    slug = bundle_dir.name

    state = collect_state(repo_root)
    filled = force_filled if force_filled is not None else detect_fill_state(bundle_dir)
    tokens = _tokens(mode, slug, repo, date, state, filled)

    if mode == "epic":
        eslug = epic_slug or slug
        tokens.update({"EPIC_SLUG": eslug, "EPIC_BRANCH": f"epic/{eslug}"})
        # #287: re-render the chat-title against the resolved epic slug (name + number), so an
        # epic/developer bundle's title carries `<epic-slug> EPIC <n>`, not the bundle slug.
        tokens["CHAT_TITLE"] = _chat_title("epic", repo, eslug)
        # §14b return skeleton: write-if-absent — the SUPPLEMENT.md never-clobber precedent.
        if not (bundle_dir / "EPIC_RETURN.md").exists():
            ret = _strip_leading_comment(_substitute(
                (_TMPL_DIR_EPIC / "EPIC_RETURN.md.tmpl").read_text(encoding="utf-8"), tokens))
            (bundle_dir / "EPIC_RETURN.md").write_text(ret, encoding="utf-8", newline="\n")
        _render("EPIC_BOOT.md.tmpl", tokens, bundle_dir, "EPIC_BOOT.md", tmpl_dir=_TMPL_DIR_EPIC)
        _render("PROBES.md.tmpl", tokens, bundle_dir, "PROBES.md", tmpl_dir=_TMPL_DIR_EPIC)
        verify_seal_identity(bundle_dir)                     # [#473] B seal gate
        _write_funnel_health(bundle_dir, repo_root)           # FM-4 — AFTER the seal (see below)
        hints = collect_hints(repo_root)
        return GenResult(bundle_dir=bundle_dir,
                         journal_draft=journal_draft(slug, date, state, hints), filled=filled)

    if mode == "functional":
        # Committed-state COPIES, not probe answers (§16 scoping) — no counts/shas/verdicts;
        # those stay collect_hints-only, below, same as every other mode.
        tokens.update({
            "VISION_EXTRACT": _vision_extract(repo_root),
            "INTAKE_INDEX": _intake_index(repo_root),
        })
        _render("FUNCTIONAL_BOOT.md.tmpl", tokens, bundle_dir, "FUNCTIONAL_BOOT.md",
                tmpl_dir=_TMPL_DIR_FUNCTIONAL)
        verify_seal_identity(bundle_dir)          # [#473] B — a no-op: §16 carries no Slug row
        hints = collect_hints(repo_root)
        # Never reaches the SUPPLEMENT/v5 render path below and never assembles — the
        # single FUNCTIONAL_BOOT.md file IS the bundle.
        return GenResult(bundle_dir=bundle_dir,
                         journal_draft=journal_draft(slug, date, state, hints), filled=filled)

    # SUPPLEMENT first (architect mode) — but never clobber an operator-filled one. Its presence
    # feeds detect_fill_state on a later re-run; on this run `filled` already reflects it.
    if mode == "architect" and not (bundle_dir / "SUPPLEMENT.md").exists():
        sup = _strip_leading_comment(
            _substitute((_TMPL_DIR / "SUPPLEMENT.md.tmpl").read_text(encoding="utf-8"), tokens))
        (bundle_dir / "SUPPLEMENT.md").write_text(sup, encoding="utf-8", newline="\n")

    # R2: the generated attribution frame for RESIDUAL §1. Computed from COMMITTED state (the
    # register + the window's diff) and carrying no answer value — see `standing_vs_new`.
    tokens["STANDING_VS_NEW"] = standing_vs_new(repo_root)
    # R5: the forms card's dispatch line, RENDERED from Ch8's dispatch table rather than held as
    # a second copy — the whole point of STANDING_RULINGS §V.
    tokens["DISPATCH_FORM"] = dispatch_form(repo_root)

    _render("HANDOFF_BOOT.md.tmpl", tokens, bundle_dir, "HANDOFF_BOOT.md")
    _render("RESIDUAL.md.tmpl", tokens, bundle_dir, "RESIDUAL.md")
    _render("PROBES.md.tmpl", tokens, bundle_dir, "PROBES.md")
    # [#473] B seal gate — BEFORE assemble_paste, so a mislabelled bundle can never reach the
    # assembled paste (the one file the operator actually ships to the browser).
    verify_seal_identity(bundle_dir)

    # FM-4: the FUNNEL HEALTH block, written WHOLE (never spliced, never carried) and AFTER the
    # seal gate rather than before it — a refused or failed cut must not leave a bundle carrying
    # a FRESH health block beside STALE renders, which is the mixed state a reader cannot detect
    # (terra HIGH, 2026-08-29). `functional` mode never reaches here and that is the scoping:
    # HANDOFF_PROCESS §16 (`protocols/HANDOFF_PROCESS.md`, "The boot (one file, generated)")
    # pins that mode at ONE file and narrows the answer-free invariant to "no counts ... enter
    # the boot". Amending §16 is outside this lane's write-scope; it is the architect's call.
    _write_funnel_health(bundle_dir, repo_root)

    hints = collect_hints(repo_root)
    draft = journal_draft(slug, date, state, hints)

    if assemble:
        subprocess.run([sys.executable, str(_SCRIPTS / "assemble_paste.py"), str(bundle_dir)],
                       check=False)
    return GenResult(bundle_dir=bundle_dir, journal_draft=draft, filled=filled)


@click.command()
@click.option("--mode",
              type=click.Choice(["architect", "execution", "epic", "developer", "functional"]),
              default="architect", show_default=True)
@click.option("--epic-slug", default=None,
              help="epic/developer mode only: the epic name (branch epic/<slug>, worktree "
                   "epic-<slug>); default the bundle slug")
@click.option("--slug", default=None, help="bundle slug; default <date>-<repo>-<mode>")
@click.option("--repo", default=None, help="repo display name; default the repo dir name")
@click.option("--date", default=None, help="handoff date YYYY-MM-DD; default today")
@click.option("--filled/--cold", "force_filled", default=None,
              help="override the auto-detected supplement fill-state for the four framing sites")
@click.option("--assemble/--no-assemble", default=True, help="run assemble_paste to emit PASTE_THIS.md")
@click.option("--allow-suffix", is_flag=True, default=False,
              help="RM-8 opt-in: when the target bundle dir already holds git-tracked files, "
                   "write a NEW `-<n>` sibling instead of refusing (never overwrites)")
@click.option("--emit-journal/--no-emit-journal", default=True,
              help="print the JOURNAL generation-entry DRAFT to stdout (never writes JOURNAL.md)")
def main(mode: str, epic_slug: str | None, slug: str | None, repo: str | None, date: str | None,
         force_filled: bool | None, assemble: bool, allow_suffix: bool, emit_journal: bool) -> None:
    """Generate a v5 handoff bundle from committed repo state."""
    state = collect_state(_REPO_ROOT)
    if state.dirty:
        click.echo("[warn] working tree is DIRTY — a v5 bundle is cut from COMMITTED state; "
                   "commit first or the probes bind to un-committed drift.", err=True)
    try:
        res = generate(_REPO_ROOT, mode=mode, slug=slug, repo=repo, date=date,
                       force_filled=force_filled, assemble=assemble, epic_slug=epic_slug,
                       allow_suffix=allow_suffix)
    except (BundleCollisionError, OpenBatchError, BoundaryHygieneError) as exc:
        # A REFUSAL, not a crash — one diagnostic line, non-zero exit, nothing written.
        # RM-8 (target collision) and the two boundary invariants share this exit: each
        # names what it found, and none of them is recoverable by re-running unchanged.
        raise SystemExit(f"[error] {exc}") from exc
    click.echo(f"Generated bundle: {res.bundle_dir}  (fill-state: {'FILLED' if res.filled else 'cold'})")
    if emit_journal:
        click.echo("\n----- JOURNAL generation-entry DRAFT (prepend to JOURNAL.md at wrap; "
                   "NOT auto-appended, NOT in the bundle) -----")
        click.echo(res.journal_draft)


if __name__ == "__main__":
    main()
