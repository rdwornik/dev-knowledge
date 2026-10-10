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
import importlib.util
import os
import re
import shutil
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
    "AssemblyRefusedError",
    "BoundaryHygieneError",
    "BundleCollisionError",
    "CarriageVerdict",
    "PreflightError",
    "PreflightRow",
    "BundleIdentityError",
    "DryCutTargetError",
    "GenResult",
    "OpenBatchError",
    "SupplementSlotError",
    "assert_batch_boundary",
    "assert_boundary_hygiene",
    "assert_preflight",
    "assert_supplement_fixed_slots",
    "boot_cost",
    "boot_data_block",
    "boot_data_rows",
    "bundle_manifest",
    "carriage_shortfall",
    "carriage_verdicts",
    "carried_by_value",
    "collect_hints",
    "collect_state",
    "decision_files",
    "detect_fill_state",
    "dispatch_form",
    "fixed_slots",
    "funnel_health_block",
    "generate",
    "journal_draft",
    "preflight_rows",
    "publish_bundle",
    "reflow_framing",
    "spec_version",
    "standing_vs_new",
    "verify_published",
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

# lane-handoff-min (Part A): the boot's live STATE rows are a separate reader module — it
# defines no registry of its own and calls only organs that already exist (ci_verdict,
# batch_manifest, seat_registry, the two ecosystem registries, the newest transport
# RATIFICATION / DIGEST-CAPABILITY-MAP). No cycle risk (handoff_state never imports this
# module).
#
# Imported at USE time, not at module load (lane-handoff-min-2, repair of the second refusal):
# a top-level import made this module unimportable from a copied `scripts/` dir that lacks the
# sibling — `assemble_paste.py` run that way (tests/test_assemble_paste.py's fixture, which
# copies only assemble_paste.py / gen_handoff.py / canonical_docs.py) hit a bare
# ModuleNotFoundError in 41 tests that only need `reflow_framing` / `detect_fill_state`, neither
# of which touches STATE rows. Same shape as the `_vhp()` deferral below, chosen over adding
# handoff_state.py to the fixture's copy list because the fixture's Owns is "assemble_paste.py's
# own dependency closure", not every module gen_handoff.py happens to import — widening it papers
# over the real coupling instead of removing it.
def _hstate():
    """`handoff_state`, resolved under both entry shapes (package, or `scripts/` on `sys.path`) —
    the same dual shim as `canonical_docs`, run when first needed."""
    try:
        from scripts import handoff_state as hstate  # noqa: PLC0415
    except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
        import handoff_state as hstate  # noqa: PLC0415
    return hstate

# lane-boot-contract (WAVE5B-N2 row 12): the boot's DATA/PROSE contract is the VERIFIER's — it
# decides what "probe-checked" means — so the delimiters, the receipt name and the boot-cost
# metric are read from it, never restated here.
#
# Imported at USE time, not at module load (repair 1, WAVE5B-N2): a top-level import made every
# importer of this module need `verify_handoff_probes` beside it, and `assemble_paste.py` run as
# a script from a copied `scripts/` dir (tests/test_assemble_paste.py) had neither the package
# nor the sibling — 41 reds that only need `reflow_framing` / `detect_fill_state`. Deferred, the
# dependency binds only the code paths that render or receipt a boot, and a miss there still
# raises (no fallback value): the silent-placeholder hazard `canonical_docs` is kept whole for
# does not reopen. The six names below stay module attributes via `__getattr__` (PEP 562).
_VERIFIER_NAMES = frozenset({"BOOT_DATA_BEGIN", "BOOT_DATA_END", "BOOT_PROSE_BEGIN",
                             "BOOT_PROSE_END", "RECEIPT_FILE", "BOOT_COST_METRIC"})


def _vhp():
    """`verify_handoff_probes`, resolved under both entry shapes (package, or `scripts/` on
    `sys.path`) — the same dual shim as `canonical_docs`, run when first needed."""
    try:
        from scripts import verify_handoff_probes as vhp  # noqa: PLC0415
    except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
        import verify_handoff_probes as vhp  # noqa: PLC0415
    return vhp


def __getattr__(name: str):
    if name in _VERIFIER_NAMES:
        return getattr(_vhp(), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

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
                f"the PROBES P0c/P3/P8 locators, the PROBES note's own self-reference) at "
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


# --- PREFLIGHT: the nine pre-cut hygiene rows (ratified register, SUPPLEMENT ANSWERS Q7) --
#
# Pre-handoff hygiene was a CHECKLIST the operator re-derived every window. This is the same
# nine items as a MECHANISM, in the idiom the two boundary invariants above already set: each
# row is PASS / FAIL / n-a with a locator, every FAIL is named in ONE refusal, and a FAIL
# refuses the cut before anything is written.
#
# TWO OF THE NINE WERE MIS-SPECIFIED AS REGISTERED, and both are implemented as corrected —
# a row that cannot fail is worse than no row, because it reports a safety it does not provide:
#
#   * Row 7, registered as "no QUESTION-* unanswered", became unfalsifiable on 2026-09-07 when
#     all 20 outstanding QUESTION files were ARCHIVED and none was answered. An empty directory
#     satisfies it, so it passes forever. Implemented as "no QUESTION file without a
#     DISPOSITION": answered, or explicitly carried with a resolving locator. Archiving alone
#     discharges nothing, and an undispositioned question does not age out of the population.
#   * Row 8, registered as "MEMORY.md within cap", names a cap that is DECLARED NOWHERE (no
#     MEMORY byte budget exists in scripts/, protocols/ or tests/; the live file measures
#     ~23,851 B). Inventing a number would be making a decision this lane does not own, so the
#     row reads a declared constant and renders NOT-APPLICABLE WITH THE REASON when none is
#     declared. It never passes silently, and it arms itself with no code change the moment the
#     operator declares the budget.
#
# ROW 1 WAS AMENDED 2026-09-08 by operator ruling, and the amendment is a DISTINCTION, not a
# relaxation: a HANDOFF IS NOT A RELEASE. The row was registered as "ship-gate GREEN", which is
# the TAG gate's criterion -- 0 hard-fail AND 0 undispositioned, NC1 / 028 criterion A, and that
# criterion is unchanged where it belongs. Applied to a CUT it deadlocks by design: a window
# carrying any open finding could never hand off, and the first live run of this preflight
# demonstrated exactly that (it refused the 2026-09-08 cut over [#638]'s 4 WARNs). The row now
# reads:
#
#     hard-fail = 0 AND every undispositioned WARN is named in the residual with its owning row
#
# so the debt travels to the next seat EXPLICITLY -- the P11 residual shape already carries it --
# instead of the window being unable to close. Only the FIRST conjunct is mechanically checkable
# here: the residual is written after preflight clears, so the row passes on the count and states
# the carried obligation in its evidence line, which is where the seat cutting the bundle reads
# it. Saying that plainly is the same discipline rows 7 and 8 above are implemented under -- a
# row must not report a safety it does not provide, and it must not hide one it only asserts.
# Ruling: `to-cc/DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08.md` on the transport, ratified by the
# operator's paste 2026-09-08.
#
# ROW 7 WAS AMENDED 2026-09-08 by operator ruling, in the same shape as row 1 and on the same
# day, because it had the same defect pointing the other way. Row 7 demanded that a question be
# RESOLVED. Eleven of this window's were batch T/U dawn-list questions awaiting an operator
# sitting that had not happened, so the row could only be cleared by inventing dispositions --
# and the seat that hit it correctly refused to. The row now reads:
#
#     ANSWERED (an ANSWER-*/DECLARE-* answers it)
#       OR CARRIED (named in the residual with the OPEN backlog row that owns it)
#
# with two refusals that are the whole point of the carry leg: a CLOSED row does NOT carry (a
# closed row cannot own an open question), and NO OWNER is a FAIL. The principle both amendments
# share, stated once: A WINDOW MAY HAND OFF WITH DEBT ONLY WHEN THE DEBT IS EXPLICIT AND OWNED;
# IT MAY NEVER HAND OFF WITH DEBT THAT IS SILENT.
#
# And, exactly as in row 1, the residual half is an OBLIGATION THIS ROW STATES AND DOES NOT
# VERIFY -- the residual does not exist at preflight time. Saying so in the evidence line is the
# discipline; implying a check that is absent is the defect rows 7 and 8 were corrected for.
# Ruling: `to-cc/DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`, ratified by the operator's paste.
#
# COST, SUPERSEDED (ADR-129, 2026-10-01): row 1 no longer runs the whole ship-gate (the
# 4m30s-to-17m08s subprocess this comment used to cost-justify, 2026-09-07 through 2026-10-01).
# It runs the 11-organ handoff set in-process, in parallel, measured at about 58s serial /
# faster parallel per-organ (PROPOSAL-ADR-HANDOFF-REDESIGN-2026-09-30 §1.3) -- cheap enough
# that "a once-per-window act" is no longer the reason it is affordable here and nowhere else.
# The whole-repository verdict is still read, never run, for the bundle's notes -- see
# `_whole_repo_verdict`.

PREFLIGHT_PASS = "PASS"
PREFLIGHT_FAIL = "FAIL"
PREFLIGHT_NA = "n/a"

#: 5,000 DECIMAL, and it is CITED rather than re-litigated: `protocols/HANDOFF_PROCESS.md` §5
#: ("P8's two legs, and P11") settles it explicitly -- "**5,000**, matching the decimal
#: convention the repo's other two byte budgets already use" -- because "5 KB" reads as either
#: 5,000 or 5,120 and a file measured at 5,114 bytes sits between them.
STATUS_BYTE_BUDGET = 5_000

#: Where a MEMORY.md byte budget WOULD be declared. Nothing declares it today; row 8 reads this
#: name via getattr and renders n-a-with-reason while it is absent. Filed for the operator.
MEMORY_BUDGET_DECLARATION_SITE = "canonical_docs.MEMORY_BYTE_BUDGET"

#: SUPERSEDED (ADR-129, 2026-10-01): row 1 no longer shells out to a subprocess, so no local
#: ceiling bounds it any more. `SHIP_GATE_TIMEOUT_S` (A2, [#1330]'s batch) governed that
#: subprocess from 2026-09-09 to 2026-10-01; see `scripts/handback.py`'s OWN constant of the
#: same name for the unrelated self-check subprocess that still needs one. The handoff organ
#: set runs IN-PROCESS via `audit.run_checks(checks=audit.handoff_organs(), parallel=True)` --
#: see `_row_ship_gate` below -- at about 58s measured per-organ serially (far under any
#: ceiling this constant ever set), so a timeout here would be a solution hunting the problem
#: it used to solve.

#: The row order, declared so the report is stable and a test can assert the roster.
PREFLIGHT_ROW_NAMES = (
    "ship_gate", "ledger_refreshed", "ratification_present", "status_byte_budget",
    "living_docs_stamped", "journal_anchored", "question_disposition",
    "memory_within_cap", "worktree_owners",
    # Row 10, added 2026-09-08 by [#643]. APPENDED rather than inserted so the ratified
    # register's own 1-9 numbering -- which two operator rulings and this module's own
    # docstrings cite by number -- keeps meaning what it meant.
    "p11_carriage",
)


@dataclass(frozen=True)
class PreflightRow:
    """One hygiene row: a verdict, the locator to act on, and the evidence behind it."""
    name: str
    status: str
    locator: str
    detail: str

    @property
    def failed(self) -> bool:
        return self.status == PREFLIGHT_FAIL

    def render(self) -> str:
        return f"[{self.status:^4}] {self.name}: {self.detail} -- {self.locator}"


class PreflightError(RuntimeError):
    """Generation refused: at least one pre-cut hygiene row FAILED.

    Every failing row is named in ONE refusal, for the reason `assert_boundary_hygiene` already
    states about leftovers: reporting only the first invites a fix-and-retry loop that reveals
    the next one. The refusal fires after the two boundary invariants and before anything is
    written, so a refused cut leaves no half-written bundle behind.
    """


class AssemblyRefusedError(RuntimeError):
    """Generation refused at the ASSEMBLE step: the child assembler exited non-zero.

    The LAST refusal in the family and the only one that fires AFTER the bundle is written,
    because the thing it judges -- a filled RESIDUAL.md against the transport window -- does
    not exist until the render has run. `assemble_paste.py` owns the judgment and prints its
    own diagnostic; this class exists so the exit code SURVIVES the process boundary.

    Terra HIGH, 2026-09-09. Before it, `generate()` spawned that child with `check=False` and
    returned a GenResult regardless, so `gen_handoff --assemble` -- the default, and the path
    an operator actually runs -- printed `Generated bundle` and exited 0 on a bundle leg 2 had
    just refused. The refusal was real and the receipt contradicted it, which is strictly worse
    than having no gate: a false witness is acted on, an absent one is not.

    HONEST LIMIT: this propagates ANY non-zero exit from the assembler, not leg 2's
    specifically. That is deliberate -- the parent has no business re-deciding which of the
    child's refusals count, and every one of them means the same thing here (no PASTE_THIS.md
    was written, so there is nothing to hand to a browser).
    """


def _is_hub(repo_root: Path) -> bool:
    """True when `repo_root` is the checkout THIS gen_handoff.py belongs to.

    HUB-ONLY BY REPO IDENTITY, the same scoping `audit.check_journal_spine_anchor` declares for
    ADR-85's floor: a consumer carries neither this transport window, nor these stamped docs,
    nor ADR-85's JOURNAL shape, so judging one against them would manufacture a fleet gap
    (the enforcement-organs-are-not-homogeneous class). A cross-repo cut is read-only on its
    target (ADR-36/41) and does not own the operator's window either.
    """
    try:
        return Path(repo_root).resolve() == Path(_REPO_ROOT).resolve()
    except OSError:
        return False


def transport_root(env: "dict | None" = None, downloads: "Path | None" = None) -> "Path | None":
    """The operator's prompts directory, or None when it cannot be resolved.

    OPERATOR-INTERFACE §1: **THE VARIABLE IS THE SOURCE** (`CLAUDE_PROMPTS_DIR`, currently a
    Drive-synced folder), with `~/Downloads` as the documented per-file fallback. A path is
    never hardcoded here -- the folder is the operator's and may move without this file moving.

    None means UNRESOLVED, and the four transport rows treat that as a REFUSAL rather than a
    pass: DEFECT E-29 is exactly the failure a permissive reading produces -- a seat inheriting
    a stale value resolves to Downloads, finds `to-cc/` present but EMPTY, and reads that as
    "nothing filed" rather than as a misresolved variable.
    """
    env = os.environ if env is None else env
    declared = (env.get("CLAUDE_PROMPTS_DIR") or "").strip().strip('"')
    if declared and Path(declared).is_dir():
        return Path(declared)
    fallback = Path.home() / "Downloads" if downloads is None else Path(downloads)
    return fallback if fallback.is_dir() else None


def _stamped_docs() -> tuple[str, ...]:
    """The living docs carrying a `last_reviewed` stamp -- COMPUTED, never a roster typed here.

    `canonical_docs.FRESHNESS_FILES` (the portable base) plus `audit._HUB_ONLY_FRESHNESS_FILES`
    (the hub governance extras). A literal list in this module would be a count restated in
    code -- stale at the next commit, and silently, because a doc missing from a roster produces
    no finding at all. HONEST LIMIT: an unimportable `audit` degrades to the portable base
    alone, which narrows the row rather than wedging it.
    """
    files = list(_cdocs.FRESHNESS_FILES)
    try:
        sys.path.insert(0, str(_SCRIPTS))
        import audit as _aud  # noqa: PLC0415
        files += list(_aud._HUB_ONLY_FRESHNESS_FILES)
    except Exception:  # noqa: BLE001 -- narrower set, never a wedge
        pass
    return tuple(dict.fromkeys(files))


#: Reused below by `_whole_repo_verdict` to read the SAME verdict line out of CI's job log --
#: `cmd_ship_gate` prints `ship-gate: GREEN|RED ...` wherever it runs, local or Actions, so one
#: pattern reads both. The hard-fail/undispositioned-WARN sub-counts that used to be parsed out
#: of this tail (`_SHIP_GATE_HARD_FAIL_RE` / `_SHIP_GATE_UNDISPOSITIONED_RE`, removed with
#: ADR-129) are gone: row 1 no longer derives its own pass/fail from this text at all -- see
#: `_row_ship_gate` -- so only the verdict word and the tail survive, for the drift notes.
_SHIP_GATE_VERDICT_RE = re.compile(r"^ship-gate:\s*(GREEN|RED)\b(.*)$", re.MULTILINE)

#: This is a REPORTING read, never part of row 1's pass/fail (ADR-129 item 2; "do not" line
#: 2), and it NEVER WAITS: unlike `ci_verdict.verdict_for` (which polls up to 900s for an
#: in-progress run to finish), this reads whatever `gh` can answer in one list/jobs/log round
#: trip, each capped at `ci_verdict.GH_TIMEOUT_S` (120s) by the wrappers it reuses, and a run
#: still in progress is reported `"not run"` immediately rather than awaited.
#:
#: The CI job this reads -- the SAME advisory `continue-on-error` job `.github/workflows/
#: conductor.yml` runs on every push (`ship-gate:`), never a local run (ADR-129 item 2).
_WHOLE_REPO_VERDICT_JOB_NAME = "ship-gate"


def _whole_repo_verdict(repo_root: Path, sha: "str | None" = None) -> dict:
    """The latest CI `ship-gate` job's verdict for `sha` (default HEAD) -- READ, NEVER RUN.

    ADR-129 item 2: the whole-repository verdict goes into the bundle's notes / the residual's
    drift flags, and it NEVER blocks the cut (`_row_ship_gate` never calls this). Its source is
    the CI `ship-gate` job for the cut sha when one exists, otherwise a named `"not run"` --
    never a local re-run of the 57-organ registry (the "do not" this lane is bound by).

    Reuses `ci_verdict.py`'s `gh` wrappers (`find_run` / `fetch_jobs` / `fetch_job_log`) rather
    than opening a second `gh`-calling surface -- library-first (R38). It does NOT reuse
    `ci_verdict.verdict_for`/`wait_for_run`: those POLL up to 900s for an in-progress run, which
    this reporting-only read must never do (the 120s cut budget is the whole point of ADR-129).
    This function never waits: a run still in progress, or any `gh` failure, reads as
    `"not run"` with the reason named -- it NEVER raises, so a CI outage can never refuse or
    even slow the cut by more than one short, bounded `gh` round trip.

    The `ship-gate` job runs `continue-on-error: true` (`.github/workflows/conductor.yml`), so
    its OWN job-level conclusion -- not the workflow run's overall conclusion -- is what is
    read; the job's log carries the same `ship-gate: GREEN|RED ...` tail a local run would
    print, parsed with the same `_SHIP_GATE_VERDICT_RE` a local run used to produce.
    """
    try:
        sys.path.insert(0, str(_SCRIPTS))
        import ci_verdict as _civ  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001 -- reporting-only; never a cut blocker
        return {"source": "CI ship-gate job", "verdict": "not run",
                "detail": f"ci_verdict unreadable: {exc!r}"}
    resolved_sha = sha or _git_status(repo_root, "rev-parse", "HEAD")[1].strip() or "HEAD"
    try:
        run = _civ.find_run(resolved_sha, repo_root=repo_root, workflow=_civ.WORKFLOW)
        if run is None:
            return {"source": "CI ship-gate job", "verdict": "not run", "sha": resolved_sha,
                    "detail": f"no Actions run matched {resolved_sha[:12]}"}
        if run.get("status") != "completed":
            return {"source": "CI ship-gate job", "verdict": "not run", "sha": resolved_sha,
                    "run_url": run.get("url"),
                    "detail": f"run {run.get('databaseId')} is still {run.get('status')}"}
        run_id = run.get("databaseId")
        jobs = _civ.fetch_jobs(run_id, repo_root=repo_root) or []
        job = next((j for j in jobs if j.get("name") == _WHOLE_REPO_VERDICT_JOB_NAME), None)
        if job is None or job.get("databaseId") is None:
            return {"source": "CI ship-gate job", "verdict": "not run", "sha": resolved_sha,
                    "run_url": run.get("url"),
                    "detail": f"run {run_id} carries no '{_WHOLE_REPO_VERDICT_JOB_NAME}' job"}
        log_text = _civ.fetch_job_log(run_id, job["databaseId"], repo_root=repo_root)
        hits = _SHIP_GATE_VERDICT_RE.findall(log_text or "")
        if not hits:
            return {"source": "CI ship-gate job", "verdict": "not run", "sha": resolved_sha,
                    "run_url": run.get("url"), "job_conclusion": job.get("conclusion"),
                    "detail": (f"'{_WHOLE_REPO_VERDICT_JOB_NAME}' job (conclusion="
                              f"{job.get('conclusion')}) emitted no verdict line in its log")}
        verdict, tail = hits[-1]
        return {"source": "CI ship-gate job", "verdict": verdict, "sha": resolved_sha,
                "run_url": run.get("url"), "job_conclusion": job.get("conclusion"),
                "detail": f"ship-gate: {verdict}{tail}".strip()}
    except Exception as exc:  # noqa: BLE001 -- reporting-only; never a cut blocker
        return {"source": "CI ship-gate job", "verdict": "not run", "sha": resolved_sha,
                "detail": f"{exc!r}"}


# --- item 14/L9: the refusal log -----------------------------------------------------------
#
# DECIDED-BY-LANE (N3): the log lives under the TRANSPORT, never under the repository. A file
# this generator appended to on every refusal, if it lived inside the git work tree, would be
# an uncommitted change the NEXT cut attempt's own `state.dirty` check would refuse on -- the
# mechanism would poison its own next run. The transport is outside every git work tree by
# construction (`transport_root()`'s docstring), so appending there can never dirty the tree
# the cut checks. Same reasoning CLAUDE.md's LEDGER files already rely on: cross-window,
# cross-session state belongs on the transport, not in the repo, when the repo's own
# cleanliness is itself a gate input.
#
# Scope: a REAL cut's `PreflightError` refusals only (`not dry_cut`). A dry cut is a CI/test
# proof of the cut path (ADR-129 item 1/L1), not an operator's actual cut attempt, and proposal
# §7 step 5 / PM8's "refusal count since the previous cut" is about the operator's own retry
# loop -- counting dry-cut noise into it would make the count answer a question nobody asked.
_REFUSAL_LOG_RELPATH = Path("logs") / "HANDOFF-REFUSALS.jsonl"


def _refusal_log_path(transport: "Path | None") -> "Path | None":
    return (transport / _REFUSAL_LOG_RELPATH) if transport is not None else None


def _append_refusal_log(transport: "Path | None", *, repo_root: Path, reason: str) -> None:
    """Best-effort append of one REFUSAL line; never raises (a logging failure is not a cut
    failure, and the exception this is called from is already on its way out)."""
    path = _refusal_log_path(transport)
    if path is None:
        return
    try:
        import json  # noqa: PLC0415
        _, sha = _git_status(repo_root, "rev-parse", "HEAD")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({
                "kind": "REFUSAL", "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(
                    timespec="seconds"), "sha": (sha or "").strip() or None, "reason": reason,
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _append_cut_log(transport: "Path | None", *, repo_root: Path, slug: str) -> None:
    """Best-effort append of one CUT line, marking a real (never dry) cut's success. Never
    raises -- a logging failure must not turn a succeeded cut into a failed one."""
    path = _refusal_log_path(transport)
    if path is None:
        return
    try:
        import json  # noqa: PLC0415
        _, sha = _git_status(repo_root, "rev-parse", "HEAD")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({
                "kind": "CUT", "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(
                    timespec="seconds"), "sha": (sha or "").strip() or None, "slug": slug,
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _refusal_count_since_previous_cut(transport: "Path | None") -> "int | None":
    """Count of REFUSAL entries after the last CUT entry (or in the whole log, when no CUT
    entry exists yet). None when the log is absent or unreadable -- ABSENT, not zero, because
    zero would read as "no refusals" rather than as "never measured" (the same honesty the
    other unmeasured receipt fields already keep)."""
    path = _refusal_log_path(transport)
    if path is None or not path.is_file():
        return None
    try:
        import json  # noqa: PLC0415
        count = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if entry.get("kind") == "CUT":
                count = 0
            elif entry.get("kind") == "REFUSAL":
                count += 1
        return count
    except OSError:
        return None


def _journal_spine_gaps(repo_root: Path) -> "list[str] | None":
    """Unanchored spine entries not covered by the ADR-110 exemption; None when undetermined.

    The predicate is IMPORTED from `journal_anchor` -- the same module the pre-push organ and
    `audit.check_journal_spine_anchor` use -- so this row cannot drift from them about what
    "anchored" means. The declared-integration-arc exemption is applied through
    `batch_manifest.exempt` for the same reason.
    """
    try:
        sys.path.insert(0, str(_SCRIPTS))
        import batch_manifest as _bm  # noqa: PLC0415
        import journal_anchor as _ja  # noqa: PLC0415
        root = Path(repo_root)
        unanchored = _ja.unanchored_on_spine(root, "main", _ja.floor_sha(root),
                                             _ja.journal_text(root))
        exempted = _bm.exempt(root, list(unanchored), batches=_bm.open_batches(root))
        return [s for s in unanchored if s not in exempted]
    except Exception:  # noqa: BLE001 -- undetermined, reported as a FAIL by the row
        return None


def _session_slug(path) -> str:
    r"""The Claude Code session-store directory name for a working directory.

    `C:\Users\x\Dev\repo\.claude\worktrees\lane-a` ->
    `C--Users-x-Dev-repo--claude-worktrees-lane-a`: drive colon, both separators and the dot
    Every character outside `[A-Za-z0-9_-]` becomes one dash -- which is what produces the
    doubled dash after the drive letter and before `claude`. Written as a NEGATED class on
    purpose: an enumerated one has to spell a literal backslash, and this repo has already
    lost that backslash once in transit, silently, leaving a slug that matched nothing.
    """
    return re.sub(r"[^A-Za-z0-9_-]", "-", str(Path(path).resolve()))


def _main_checkout(repo_root: Path) -> Path:
    """The PRIMARY working tree, given any checkout of this repo (a linked worktree included).

    A lane runs in `.claude/worktrees/<name>`, so `repo_root.name` there is the LANE's name, not
    the repo's -- and a row keyed on it looks for `LEDGER-c4-handoff-preflight-rows.md` and a
    session store that does not exist. The common git dir is the one surface that answers this
    from inside either tree. Degrades to `repo_root` when git cannot answer.
    """
    ok, out = _git_status(repo_root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if ok and out.strip():
        common = Path(out.strip())
        if common.name == ".git":
            return common.parent
    return Path(repo_root)


def _memory_path(repo_root: "Path | None" = None) -> Path:
    """This repo's auto-memory index, in the per-project session store."""
    slug = _session_slug(_main_checkout(Path(repo_root or _REPO_ROOT)))
    return Path.home() / ".claude" / "projects" / slug / "memory" / "MEMORY.md"


def _na_row(name: str, reason: str, detail: str, locator: str) -> PreflightRow:
    """An n-a row carrying its reason in the codebase's `[n/a-reason:...]` form."""
    return PreflightRow(name, PREFLIGHT_NA, locator, f"[n/a-reason:{reason}] {detail}")


def _no_transport(name: str) -> PreflightRow:
    return PreflightRow(name, PREFLIGHT_FAIL, "OPERATOR-INTERFACE.md §1 (CLAUDE_PROMPTS_DIR)",
                        "the transport dir is UNRESOLVED, so this row could not be measured; "
                        "an unknown boundary is not a clean one (DEFECT E-29)")


_LEDGER_REFRESHED_RE = re.compile(r"refreshed\s+(\d{4}-\d{2}-\d{2})")


#: [#1123] the ONLY files a `--filled` re-render legitimately changes: the operator's hand-fills
#: (SUPPLEMENT/RESIDUAL/HANDOFF_BOOT) and the second assemble's own PASTE_THIS.md. Codex P1
#: (this row, first draft): checking only "BD-manifest is the sole failing probe" let ANY sole
#: manifest mismatch through -- an added/removed file, or a tampered file OUTSIDE this set,
#: still left `BD-manifest` as the only failing probe, and `_bundle_file_shas` would then
#: re-stamp the tamper as the new truth. `_self_inflicted_bd_manifest` requires every mismatch
#: to be a CONTENT change (never an add/remove) to a file in this set.
#:
#: R54 (2026-10-02): PROBES.md joins the set. `assemble_paste`'s documented fill-state flip
#: (`reflow_framing`) rewrites exactly HANDOFF_BOOT.md, RESIDUAL.md and PROBES.md, so with
#: PROBES.md missing, every bundle whose SUPPLEMENT was filled was refused by the very flow this
#: waiver exists for (the 2026-10-02 cut). Admitting it opens no tamper path: PROBES.md carries
#: no FILL-IN region, so `_splice_fill_regions` keeps nothing and the re-render this waiver lets
#: through rewrites it whole from the template
#: (`test_filled_rerender_regenerates_probes_md_so_a_tamper_cannot_survive`).
_BD_MANIFEST_FILL_SURFACE = frozenset({"SUPPLEMENT.md", "RESIDUAL.md", "HANDOFF_BOOT.md",
                                       "PASTE_THIS.md", "PROBES.md"})

#: R54: the LIVE-DRIFTS BOOT-DATA probes a `--filled` re-render re-derives, and so may waive --
#: by IDENTITY, never by live state. Each one compares a cut-time snapshot of live state with a
#: re-derivation now, so ANY movement between cut and re-render fails it (a merge landing on
#: main moves BD-ci; a seat wedging moves BD-seats) -- a staleness the re-render's fresh rows
#: fix by construction, exactly like the manifest. What must still hold is that the RECORDED
#: row is the cut's own record (`_recorded_row_identity`): a tampered row is never waived.
_FILLED_REDERIVED_PROBES = frozenset({"BD-ci", "BD-seats"})

_CI_ROW_SHA_RE = re.compile(r"^`([0-9a-f]{7,40})`")


def _recorded_row_identity(bundle_dir: Path, probe_id: str, source_sha: "str | None",
                           ) -> "tuple[bool, str]":
    """R54: is the RECORDED `BD-ci` / `BD-seats` row in `bundle_dir`'s HANDOFF_BOOT.md the cut's
    own record? Identity, not live state:

      * BD-ci   -- the row names the commit the bundle was cut from (the receipt's
                   `manifest.source_sha`). A row naming any other commit, or none, is refused;
                   so is a cut with no recorded `source_sha` (fail closed: no identity to check).
      * BD-seats -- the row carries a `seat_health_line`'s own shape ([#1124]'s shape rung,
                   reused: `verify_handoff_probes._seat_line_fully_shaped`), or the
                   "nothing observed" literal.
    """
    vhp = _vhp()
    try:
        rows, _prose = vhp.parse_boot_blocks(
            (bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8"))
    except OSError as exc:
        return False, f"HANDOFF_BOOT.md unreadable ({type(exc).__name__})"
    key = {"BD-ci": "CI", "BD-seats": "Seats"}[probe_id]
    value = dict(rows or []).get(key)
    if value is None:
        return False, f"no recorded `{key}` row"
    stripped = value.strip()
    tail = vhp._RENDERED_TAIL_RE.match(stripped)
    underlying = (tail.group("val") if tail else stripped).strip()
    if probe_id == "BD-ci":
        m = _CI_ROW_SHA_RE.match(underlying)
        if not source_sha:
            return False, "the receipt records no source_sha, so the CI row's identity is unknown"
        if m is None or not source_sha.startswith(m.group(1)):
            return False, (f"the recorded CI row does not name the cut's own commit "
                           f"{source_sha[:7]}: {underlying!r}")
        return True, f"CI row names the cut's own commit {m.group(1)}"
    hs = _hstate()
    if underlying == hs.NO_SEATS_OBSERVED or vhp._seat_line_fully_shaped(underlying):
        return True, "Seats row carries a seat_health_line's own shape"
    return False, f"the recorded Seats row is not a seat_health_line: {underlying!r}"


def _self_inflicted_bd_manifest(repo_root: Path, bundle_dir: Path) -> "tuple[bool, str]":
    """[#1123] True only when the ONE thing wrong with `bundle_dir` right now is `BD-manifest`,
    AND every mismatch it reports is a CONTENT change to a file in `_BD_MANIFEST_FILL_SURFACE`
    -- the cold-cut manifest a `--filled` re-render is about to replace with a fresh census over
    the filled tree. That re-render fixes this by construction, so a `--filled` call is never
    refused by the very staleness it is here to repair.

    Reads `bundle_dir` DIRECTLY (`verify_handoff_probes.verify` for the probe-set check, the
    receipt's own manifest vs `_bundle_file_shas` for the file-level one), never re-derives "the
    active bundle" -- `generate()` already knows which directory it is about to re-render, so
    there is nothing to rediscover, and no `_select_active_bundle` ambiguity can leak in here.

    Fails CLOSED (False) on any error, on any OTHER failing probe, or on any mismatch outside
    the fill surface -- an unreadable receipt, a genuine defect the fill window did not cause,
    an added/removed file, or a tampered file the documented fill step never touches, is never
    grounds to waive a hard-fail. Callers still owe the separate check that the ship-gate's
    hard-fail COUNT is exactly the handoff_probes contribution this function accounts for --
    this function only answers for `bundle_dir`'s own probes, never for an unrelated organ
    failing elsewhere in the same run.
    """
    ok, why, _count = _filled_waivable_fails(repo_root, bundle_dir)
    return ok, why


def _filled_waivable_fails(repo_root: Path, bundle_dir: Path) -> "tuple[bool, str, int]":
    """`(waivable, why, failing-probe count)` -- `_self_inflicted_bd_manifest`'s body, also
    returning how many of `bundle_dir`'s probes fail, so `_row_ship_gate` can hold the ship-gate's
    hard-fail COUNT equal to exactly this bundle's own (R54: `check_handoff_probes` emits ONE
    finding per failing probe, so a waivable run is no longer always exactly one finding).

    R54 widens WHICH probes may fail: `BD-manifest` (fill-surface content changes only, as
    before) plus the LIVE-DRIFTS rows a re-render re-derives (`_FILLED_REDERIVED_PROBES`), each
    only when its RECORDED row passes `_recorded_row_identity`. Any other failing probe -- or
    any check that cannot be completed -- still refuses (fail closed)."""
    try:
        results = _vhp().verify(bundle_dir, repo_root=repo_root)
    except Exception as exc:  # noqa: BLE001 -- fail closed, never waives silently
        return False, f"verify_handoff_probes could not be read ({type(exc).__name__}): {exc}", 0
    fails = [r for r in results if r.status == "fail"]
    if not fails:
        return False, (f"no probe in {bundle_dir.name} is failing -- the ship-gate hard-fail "
                       "is not this bundle's manifest"), 0
    waivable_ids = {"BD-manifest"} | _FILLED_REDERIVED_PROBES
    unknown = [r for r in fails if r.probe_id not in waivable_ids]
    if unknown:
        return False, (f"{bundle_dir.name} fails beyond the known --filled circularity: "
                       + "; ".join(f"{r.probe_id}: {r.detail}" for r in unknown)), len(fails)

    import json  # noqa: PLC0415
    try:
        receipt = json.loads((bundle_dir / _vhp().RECEIPT_FILE).read_text(encoding="utf-8"))
        manifest = receipt.get("manifest") or {}
        recorded = manifest.get("files") or {}
        if not recorded:
            raise ValueError("receipt carries no manifest.files")
        current = _bundle_file_shas(bundle_dir)
    except Exception as exc:  # noqa: BLE001 -- fail closed
        return False, (f"{bundle_dir.name}'s receipt/current census could not be compared "
                       f"({type(exc).__name__}): {exc}"), len(fails)

    notes = []
    for r in fails:
        if r.probe_id in _FILLED_REDERIVED_PROBES:
            same, about = _recorded_row_identity(bundle_dir, r.probe_id,
                                                 manifest.get("source_sha"))
            if not same:
                return False, (f"{bundle_dir.name} {r.probe_id} is not waivable by identity: "
                               f"{about}"), len(fails)
            notes.append(f"{r.probe_id}: {about} (live drift; the re-render re-derives it)")
    if not any(r.probe_id == "BD-manifest" for r in fails):
        return True, "; ".join(notes), len(fails)

    added = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    if added or removed:
        return False, (f"{bundle_dir.name}'s file SET changed, not just fill contents -- "
                       f"added: {added or 'none'}, removed: {removed or 'none'}; a structural "
                       "change is never the [#1123] circularity"), len(fails)
    changed = sorted(rel for rel in recorded if recorded[rel] != current.get(rel))
    outside = [rel for rel in changed if rel not in _BD_MANIFEST_FILL_SURFACE]
    if outside:
        return False, (f"{bundle_dir.name} has content changes outside the documented fill "
                       f"surface {sorted(_BD_MANIFEST_FILL_SURFACE)}: {outside}"), len(fails)
    if not changed:
        return False, (f"{bundle_dir.name}'s BD-manifest probe fails but the receipt's own "
                       "census matches the current tree byte-for-byte -- an unreadable or "
                       "escaping manifest entry, never the [#1123] circularity"), len(fails)
    notes.insert(0, f"BD-manifest: {len(changed)} fill-surface file(s) changed in "
                    f"{bundle_dir.name} ({', '.join(changed)}) -- the [#1123] "
                    "cold-manifest-vs-filled-tree circularity, fixed by this re-render's own "
                    "fresh census")
    return True, "; ".join(notes), len(fails)


def _handoff_organ_findings(repo_root: Path) -> list:
    """The handoff organ set's findings, run IN-PROCESS and IN PARALLEL -- ADR-129 D1.

    No subprocess, no `audit.py ship-gate` child process, no local whole-57-organ run: this
    imports the hub's own `audit.py` the same way `_stamped_docs` already does (`sys.path`
    insert, then `import audit`) and calls `run_checks(checks=handoff_organs(), parallel=True)`
    -- the selection seam and the thread-pool parallelism `run_checks` already provides
    (`scripts/audit.py:5868` / `:5973`), reused rather than reimplemented (R38/library-first).
    """
    sys.path.insert(0, str(_SCRIPTS))
    import audit as _aud  # noqa: PLC0415
    return _aud.run_checks(repo_root, checks=_aud.handoff_organs(), parallel=True)


def _row_ship_gate(repo_root: Path, *, bundle_dir: "Path | None" = None,
                    force_filled: bool = False) -> PreflightRow:
    """Row 1 -- ADR-129: the handoff organ set, run in-process and in parallel, not the whole
    57-organ registry run as a 900-1800s subprocess.

    PASS on `hard-fail = 0` across the set. `check_doc_claims` is the ONE named exception
    (`audit.HANDOFF_ORGAN_WARN_ONLY`): it is WARN-tier BY RULING and structurally cannot emit
    `"fail"` (`scripts/audit.py:2120`), so its findings never enter the hard-fail count -- they
    are carried in this row's evidence, exactly as an undispositioned WARN always was.

    A hard-fail in ANY OTHER organ -- an unreadable run, or `bundle_dir` failing for a reason
    fills do not explain -- FAILs, UNLESS `force_filled` names `bundle_dir` and the run's hard
    fails are EXACTLY that bundle's own `BD-manifest` circularity ([#1123];
    `_self_inflicted_bd_manifest`): the manifest a `--filled` re-render is about to re-stamp is
    stale by construction the moment the operator's fills touch the bundle, and refusing the
    re-render that fixes it is the circularity row [#1123] exists to break.

    The WHOLE-REPOSITORY verdict (the other 46 organs) is NEVER read here, and never blocks
    this row -- see `_whole_repo_verdict`, called elsewhere for the bundle's notes only
    (ADR-129 item 2; the "do not" against re-adding the whole gate to the cut path).
    """
    locator = "`audit.run_checks(checks=audit.handoff_organs(), parallel=True)` (in-process)"
    try:
        findings = _handoff_organ_findings(repo_root)
    except Exception as exc:  # noqa: BLE001 -- unreadable is a FAIL, not a crash
        return PreflightRow("ship_gate", PREFLIGHT_FAIL, locator,
                            f"the handoff organ set could not be run: {exc!r}")

    warn_only = set(_handoff_organ_warn_only_check_names(repo_root))
    hard_fails = [f for f in findings if f.status == "fail" and f.check_name not in warn_only]
    warn_carried = [f for f in findings if f.status == "warn"]

    if not hard_fails:
        tail = ""
        if warn_carried:
            names = ", ".join(sorted({f.check_name for f in warn_carried}))
            tail = (f". CARRIED, and the cut is only honest if it holds: each WARN ({names}) "
                    "is named in the residual with its owning row "
                    "(DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08)")
        return PreflightRow("ship_gate", PREFLIGHT_PASS, locator,
                            f"{len(findings)} handoff organ(s) run, 0 hard-fail{tail}")

    # [#1123] / R54: every hard-fail-counted finding across the SET is `handoff_probes`, AND
    # their COUNT equals bundle_dir's own failing probes (`check_handoff_probes` emits one finding
    # per failing probe), AND each of those probes is waivable -- otherwise this is (or may hide)
    # an unrelated hard-fail, which still refuses.
    if (force_filled and bundle_dir is not None
            and all(f.check_name == "handoff_probes" for f in hard_fails)):
        known, why, count = _filled_waivable_fails(repo_root, bundle_dir)
        if known and count == len(hard_fails):
            return PreflightRow("ship_gate", PREFLIGHT_PASS, locator,
                f"{len(hard_fails)} handoff_probes hard-fail(s), ACCEPTED under --filled: "
                f"{why} ([#1123]/R54 a --filled re-render accepts only the cut's own known "
                "hard-fails; the manifest and LIVE-DRIFTS rows it writes below are fresh)")
    names = ", ".join(sorted({f.check_name for f in hard_fails}))
    return PreflightRow("ship_gate", PREFLIGHT_FAIL, locator,
                        f"{len(hard_fails)} hard-fail finding(s) in the handoff organ set "
                        f"({names}); a hard-fail is never carryable, and no residual line "
                        "disposes of one")


def _handoff_organ_warn_only_check_names(repo_root: Path) -> tuple:
    """`Finding.check_name` values for `audit.HANDOFF_ORGAN_WARN_ONLY` -- the stripped
    `check_` names (`"doc_claims"`, not `"check_doc_claims"`), resolved from the live module
    rather than hand-duplicated, so a rename on either side cannot desync the two."""
    sys.path.insert(0, str(_SCRIPTS))
    import audit as _aud  # noqa: PLC0415
    return tuple(name.removeprefix("check_") for name in _aud.HANDOFF_ORGAN_WARN_ONLY)


def _row_ledger_refreshed(transport, repo_name: str, today: str) -> PreflightRow:
    """Row 2 -- the operator's read surface names THIS window's date.

    The date is read from an anchored `refreshed <YYYY-MM-DD>` token in the file head, which is
    the form the live LEDGER already carries; mtime is the fallback and the evidence line says
    which was used, so a reader never has to guess what was measured.
    """
    if transport is None:
        return _no_transport("ledger_refreshed")
    path = Path(transport) / "to-browser" / f"LEDGER-{repo_name.lstrip('.')}.md"
    if not path.exists():
        return PreflightRow("ledger_refreshed", PREFLIGHT_FAIL, str(path),
                            "absent -- the operator's read surface was never written")
    m = _LEDGER_REFRESHED_RE.search(path.read_text(encoding="utf-8", errors="replace")[:4000])
    if m:
        found, src = m.group(1), "declared `refreshed` token"
    else:
        found = _dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
        src = "file mtime (no `refreshed` token in the head)"
    status = PREFLIGHT_PASS if found == today else PREFLIGHT_FAIL
    return PreflightRow("ledger_refreshed", status, str(path),
                        f"{src} = {found}; window = {today}")


def _row_ratification_present(transport, today: str) -> PreflightRow:
    """Row 3 -- the sitting's decision list exists for the window being closed."""
    if transport is None:
        return _no_transport("ratification_present")
    path = Path(transport) / "to-browser" / f"RATIFICATION-{today}.md"
    status = PREFLIGHT_PASS if path.exists() else PREFLIGHT_FAIL
    return PreflightRow("ratification_present", status, str(path),
                        "present" if status == PREFLIGHT_PASS
                        else f"absent -- no ratification file for window {today}")


def _row_status_budget(transport) -> PreflightRow:
    """Row 4 -- every `STATUS-<seat>.md` at or under 5,000 BYTES (decimal; §5 pins it)."""
    if transport is None:
        return _no_transport("status_byte_budget")
    to_browser = Path(transport) / "to-browser"
    files = sorted(p for p in to_browser.glob("STATUS*.md") if p.is_file())
    if not files:
        return _na_row("status_byte_budget", "SUBJECT-ABSENT",
                       "no STATUS file on the transport -- nothing to measure", str(to_browser))
    over = [(p.name, p.stat().st_size) for p in files if p.stat().st_size > STATUS_BYTE_BUDGET]
    if over:
        named = "; ".join(f"{n} = {s:,} B" for n, s in over)
        return PreflightRow("status_byte_budget", PREFLIGHT_FAIL, str(to_browser),
                            f"over the {STATUS_BYTE_BUDGET:,}-byte budget: {named}")
    return PreflightRow("status_byte_budget", PREFLIGHT_PASS, str(to_browser),
                        f"{len(files)} STATUS file(s), all at or under {STATUS_BYTE_BUDGET:,} B")


def _row_living_docs_stamped(repo_root: Path) -> PreflightRow:
    """Row 5 -- every COMPUTED stamped doc exists and carries a parseable `last_reviewed`."""
    docs = _stamped_docs()
    missing, unstamped = [], []
    for rel in docs:
        p = Path(repo_root) / rel
        if not p.exists():
            missing.append(rel)
            continue
        if _frontmatter_date(p) is None:
            unstamped.append(rel)
    if missing or unstamped:
        parts = []
        if missing:
            parts.append("absent: " + ", ".join(missing))
        if unstamped:
            parts.append("no parseable `last_reviewed`: " + ", ".join(unstamped))
        return PreflightRow("living_docs_stamped", PREFLIGHT_FAIL,
                            "canonical_docs.FRESHNESS_FILES + audit._HUB_ONLY_FRESHNESS_FILES",
                            "; ".join(parts))
    return PreflightRow("living_docs_stamped", PREFLIGHT_PASS,
                        "canonical_docs.FRESHNESS_FILES + audit._HUB_ONLY_FRESHNESS_FILES",
                        f"{len(docs)} computed stamped doc(s), all stamped")


_FRONTMATTER_DATE_RE = re.compile(r"^last_reviewed:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _frontmatter_date(path: Path) -> "_dt.date | None":
    """The `last_reviewed` date from a file's YAML frontmatter, or None when unstamped."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    m = _FRONTMATTER_DATE_RE.search(text[:end] if end != -1 else text)
    if not m:
        return None
    try:
        return _dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def _row_journal_anchored(repo_root: Path) -> PreflightRow:
    """Row 6 -- no unanchored entry on main's first-parent spine above ADR-85's dated floor."""
    gaps = _journal_spine_gaps(repo_root)
    locator = "journal_anchor.unanchored_on_spine + batch_manifest.exempt (ADR-85 §A8)"
    if gaps is None:
        return PreflightRow("journal_anchored", PREFLIGHT_FAIL, locator,
                            "the anchor predicate could not be evaluated -- an undetermined "
                            "spine is not an anchored one")
    if gaps:
        head = ", ".join(s[:8] for s in gaps[:5])
        more = f" +{len(gaps) - 5} more" if len(gaps) > 5 else ""
        return PreflightRow("journal_anchored", PREFLIGHT_FAIL, locator,
                            f"{len(gaps)} unanchored spine entr(ies): {head}{more}")
    return PreflightRow("journal_anchored", PREFLIGHT_PASS, locator,
                        "no unexempted unanchored spine entry above the floor")


#: A `disposition:` VALUE has to look like a resolving locator, not merely be present. The P11
#: lesson, in this file's own words: a predicate that matches the DESCRIPTION of an event cannot
#: distinguish the event from its specification. Anchored (flush-left key) AND valued.
_DISPOSITION_KEY_RE = re.compile(r"^disposition:[ \t]*(\S.*)$", re.MULTILINE)
_LOCATOR_SHAPE_RE = re.compile(r"(\.md\b|/|\[#\d+\]|ADR-\d+|\d{4}-\d{2}-\d{2})")

#: The CARRIED leg's owner reference: a backlog id anywhere in the disposition VALUE.
_BACKLOG_ID_RE = re.compile(r"\[#(\d+)\]")

#: OPEN rows in the GENERATED BACKLOG.md, anchored at the row bullet. Read from BACKLOG.md
#: and NOT from tasks/, for the reason `preflight_contract._open_backlog_ids` already
#: records: a closed row KEEPS its task file as the id-allocation record (ADR-107 6.3,
#: retire-not-delete), so the file's existence says nothing about whether the row is open.
_OPEN_BACKLOG_ROW_RE = re.compile(r"(?m)^- \[#(\d+)\]")


def _open_backlog_ids(repo_root) -> "set[str] | None":
    """Ids carried as OPEN rows in `BACKLOG.md`; None when it cannot be read.

    None is distinct from the empty set on purpose: an unreadable BACKLOG cannot judge an
    owner, and row 7 refuses on that rather than silently treating every owner as closed.
    """
    if repo_root is None:
        return None
    try:
        text = (Path(repo_root) / "BACKLOG.md").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return set(_OPEN_BACKLOG_ROW_RE.findall(text))


def _question_files(transport) -> list[Path]:
    """EVERY QUESTION file on the transport -- live and in every archive window.

    Scanning only the live directory is the hole the registered wording had: archiving is not a
    disposition, so an archived-and-unanswered question must not age out of the population.
    """
    to_browser = Path(transport) / "to-browser"
    found = [p for p in to_browser.glob("QUESTION*.md") if p.is_file()]
    found += [p for p in to_browser.glob("archive/*/QUESTION*.md") if p.is_file()]
    return sorted(found)


def _question_disposition_verdict(path: Path, transport,
                                  open_ids: "set[str] | None") -> "tuple[bool, str]":
    """`(dispositioned, why)` for ONE QUESTION file -- the two legs of the 2026-09-08 ruling.

    Ruling: `to-cc/DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`. A question discharges when it
    is either

      ANSWERED -- an `ANSWER-*`/`DECLARE-*` answers it: an `ANSWER-<seat>.md` on the transport,
                  or a flush-left `disposition:` whose value cites a resolving locator; or
      CARRIED  -- the `disposition:` value names the OPEN backlog row that OWNS it.

    Two refusals are the point of the carry leg, and neither is incidental. **A CLOSED row does
    not carry** -- a closed row cannot own an open question, so a disposition naming only closed
    ids FAILs even though the value is locator-shaped. **No owner at all is a FAIL** -- that is
    the silent debt the row exists to refuse. And an unreadable BACKLOG makes an owner
    unjudgeable, which is not the same as absent: it FAILs too, the direction every other row
    here already takes on an unknown.

    The ORDER matters. Ids are read BEFORE the locator-shape leg, because `[#123]` is itself a
    locator shape: checking shape first would let a closed row pass as an ANSWERED citation and
    silently void the carry condition the ruling turns on.
    """
    seat = path.name[len("QUESTION-"):-len(".md")] if path.name.startswith("QUESTION-") else ""
    to_cc = Path(transport) / "to-cc"
    if seat:
        answers = [to_cc / f"ANSWER-{seat}.md", *to_cc.glob(f"archive/*/ANSWER-{seat}.md")]
        hit = next((p for p in answers if p.exists()), None)
        if hit is not None:
            return (True, f"ANSWERED by {hit.name}")
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError as exc:
        return (False, f"unreadable ({exc.__class__.__name__}) -- an unreadable question is not "
                       "a dispositioned one")
    m = _DISPOSITION_KEY_RE.search(head)
    if m is None:
        return (False, "no flush-left `disposition:` key -- unanswered and uncarried")
    value = m.group(1).strip()

    ids = _BACKLOG_ID_RE.findall(value)
    if ids:
        named = ", ".join(f"[#{i}]" for i in dict.fromkeys(ids))
        if open_ids is None:
            return (False, f"names {named}, but BACKLOG.md could not be read -- an owner this "
                           "row cannot judge is not an owner")
        live = [i for i in dict.fromkeys(ids) if i in open_ids]
        if live:
            return (True, "CARRIED by OPEN "
                          + ", ".join(f"[#{i}]" for i in live))
        return (False, f"names only CLOSED row(s) {named} -- a closed row does not carry an "
                       "open question")

    if _LOCATOR_SHAPE_RE.search(value):
        return (True, "ANSWERED -- `disposition:` cites a resolving locator")
    return (False, "`disposition:` names neither a resolving locator nor an owning row")


def _row_question_disposition(transport, today: str, repo_root=None) -> PreflightRow:
    """Row 7 -- every QUESTION file is ANSWERED or CARRIED by an OPEN row that owns it.

    Amended 2026-09-08 by operator ruling (`DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`), the
    same shape as row 1's amendment on the same day and for the same reason: **a window may hand
    off with debt only when the debt is explicit and owned; it may never hand off with debt that
    is silent.** Before the ruling the row demanded a resolution, which deadlocks a window whose
    open questions need an operator sitting that has not happened.

    As in row 1, only the mechanically checkable half is checked here: that a carried question
    names an OPEN owning row. **That the residual actually NAMES each carried question with its
    row is an obligation this row states and does not verify** -- the residual does not exist at
    preflight time. The evidence line carries the obligation to the seat cutting the bundle,
    which is where it can still be acted on.

    The registered wording ("no QUESTION-* unanswered") remains corrected, for the reason the
    block header gives: an empty directory satisfied it forever, so archiving discharged nothing.
    """
    if transport is None:
        return _no_transport("question_disposition")
    files = _question_files(transport)
    locator = str(Path(transport) / "to-browser") + " (+ archive/*/)"
    if not files:
        return _na_row("question_disposition", "SUBJECT-ABSENT",
                       f"no QUESTION file on the transport -- nothing to disposition "
                       f"(window {today})", locator)
    open_ids = _open_backlog_ids(repo_root)
    verdicts = [(p, _question_disposition_verdict(p, transport, open_ids)) for p in files]
    failing = [(p.name, why) for p, (ok, why) in verdicts if not ok]
    if failing:
        shown = "; ".join(f"{n} ({why})" for n, why in failing[:4])
        more = f" +{len(failing) - 4} more" if len(failing) > 4 else ""
        return PreflightRow("question_disposition", PREFLIGHT_FAIL, locator,
                            f"{len(failing)} of {len(files)} QUESTION file(s) are neither "
                            f"ANSWERED nor CARRIED by an OPEN owning row: {shown}{more}")
    carried = [p.name for p, (ok, why) in verdicts if ok and why.startswith("CARRIED")]
    tail = ""
    if carried:
        tail = (f". CARRIED, and the cut is only honest if it holds: each of the {len(carried)} "
                "carried question(s) is named in the residual with the OPEN row that owns it "
                "(DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08)")
    return PreflightRow("question_disposition", PREFLIGHT_PASS, locator,
                        f"all {len(files)} QUESTION file(s) dispositioned "
                        f"({len(files) - len(carried)} answered, {len(carried)} carried; "
                        f"window {today}){tail}")
    return PreflightRow("question_disposition", PREFLIGHT_PASS, locator,
                        f"all {len(files)} QUESTION file(s) dispositioned (window {today})")


def _row_memory_within_cap(memory_path: "Path | None" = None) -> PreflightRow:
    """Row 8 -- MEMORY.md against a DECLARED budget; n-a-with-reason while none is declared.

    Registered as "MEMORY.md within cap", naming a cap that exists nowhere in this repo. A
    budget is a DECISION, and inventing a number here would be making one this lane does not
    own -- so the row reads the declared constant and reports its absence rather than passing.
    """
    budget = getattr(_cdocs, "MEMORY_BYTE_BUDGET", None)
    path = _memory_path() if memory_path is None else Path(memory_path)
    if budget is None:
        size = f"{path.stat().st_size:,} B" if path.exists() else "not present"
        return _na_row("memory_within_cap", "NO-DECLARED-BUDGET",
                       f"no MEMORY byte budget is declared anywhere in this repo, so this row "
                       f"has no threshold to measure against (live file: {size}). Declaring one "
                       f"arms this row with no code change", MEMORY_BUDGET_DECLARATION_SITE)
    if not path.exists():
        return _na_row("memory_within_cap", "SUBJECT-ABSENT",
                       "no MEMORY.md in this repo's session store", str(path))
    size = path.stat().st_size
    status = PREFLIGHT_PASS if size <= budget else PREFLIGHT_FAIL
    return PreflightRow("memory_within_cap", status, str(path),
                        f"{size:,} B against the declared {budget:,} B budget")


def _worktree_is_owned(tree, sessions_root: Path, repo_root: Path) -> bool:
    """TWO legs, and a tree is owned if EITHER holds. One leg alone is wrong in both directions.

    * A session-store project directory named for the tree is DIRECT evidence of a seat there.
      Not sufficient alone: a background or subagent lane's transcript is filed under its
      LAUNCHING session's cwd, so a live lane can have no directory of its own. Measured
      2026-09-08 -- this row FAILed two worktrees that were both being actively worked in.
    * A branch NOT yet contained in `main` is work in flight, and work in flight cannot be
      declared abandoned without proposing to throw it away.

    The decisive FAIL is therefore the CONJUNCTION: no seat evidence AND already merged. A tree
    whose work has landed and whose seat is gone is a leftover by construction, and that is
    provable from git rather than inferred from a heuristic.
    """
    if any((Path(sessions_root) / _session_slug(tree)).glob("*.jsonl")):
        return True
    branch = _git(Path(tree), "branch", "--show-current")
    if not branch:
        return True                       # detached HEAD -- no branch to prove containment with
    merged, _ = _git_status(repo_root, "merge-base", "--is-ancestor", branch, "main")
    return not merged


def _row_worktree_owners(repo_root: Path, sessions_root: "Path | None" = None) -> PreflightRow:
    """Row 9 -- every linked worktree is owned by a live session.

    Ownership is `_worktree_is_owned` -- seat evidence OR unmerged work; see it for why one leg
    alone is wrong in both directions. HONEST LIMIT: a transcript proves a session EXISTED there,
    not that one is running now, so a just-exited seat on an unmerged branch still reads as
    owned. That is the direction to be wrong in -- a false FAIL costs a refused cut, a false PASS
    costs a leftover, and the merged leg is what makes a leftover PROVABLE rather than guessed.

    `assert_boundary_hygiene` already refuses ANY linked worktree at the cut, so in `generate`
    this row is reached only with an empty list. Its value is in the `--preflight-only` report,
    where it says WHICH tree is abandoned rather than that some tree exists.
    """
    locator = "`git worktree list --porcelain` x ~/.claude/projects/"
    try:
        trees = _linked_worktrees(repo_root)
    except BoundaryHygieneError as exc:
        return PreflightRow("worktree_owners", PREFLIGHT_FAIL, locator, str(exc))
    if not trees:
        return PreflightRow("worktree_owners", PREFLIGHT_PASS, locator,
                            "no linked worktree -- nothing can be unowned")
    root = Path.home() / ".claude" / "projects" if sessions_root is None else Path(sessions_root)
    if not root.is_dir():
        return _na_row("worktree_owners", "SUBJECT-ABSENT",
                       f"{len(trees)} linked worktree(s), but no session store to read "
                       f"ownership from", str(root))
    unowned = [t for t in trees if not _worktree_is_owned(t, root, repo_root)]
    if unowned:
        return PreflightRow("worktree_owners", PREFLIGHT_FAIL, locator,
                            f"{len(unowned)} worktree(s) with no owning session: "
                            + "; ".join(unowned))
    return PreflightRow("worktree_owners", PREFLIGHT_PASS, locator,
                        f"all {len(trees)} linked worktree(s) have an owning session")


# --- ROW 10: P11 DECISION CARRIAGE -- and the leg that is deliberately NOT here ([#643]) --
#
# WHAT WAS MISSING. `[#643]` was filed as "the preflight runs P11's carriage check too late".
# It was worse than that: there was no check to move. `verify_handoff_probes` tested that a
# manifest ROW whose id reads `P11` is PRESENT; no code anywhere opened a transport decision
# file, read a `carried-by:` line, or asked git anything. P11's "how" cell was a recipe a seat
# ran by hand, and the 2026-09-08 verdict "ONBOARDING BLOCKED on P11" was produced by a human
# running that recipe, not by a validator. So this block BUILDS the predicate (AMEND-643-001).
#
# THE TWO LEGS GATE AT DIFFERENT STAGES, and that is the design content of the row rather than
# an afterthought:
#
#   LEG 1 (here) -- a flush-left `carried-by:` in the file HEAD whose value names a repo home
#       that RESOLVES ON `main`. Both operands -- the transport and `main` -- exist before the
#       cut, so this leg is a REFUSAL: it blocks `generate()` before anything is written.
#   LEG 2 (NOT here) -- a value that is the literal `OPEN` discharges only by being NAMED in
#       THIS bundle's residual. The residual does not exist at preflight time; it is filled by
#       the operator afterwards. The first moment both operands exist is ASSEMBLY, so leg 2
#       lives in `scripts/assemble_paste.py`. A single row claiming to cover both would be the
#       false completeness P11 itself exists to catch -- which is why this row PASSES an `OPEN`
#       file and carries the obligation in its evidence line instead of pretending to test it.
#
# THIRD MEMBER OF A FAMILY. Rows 1 and 7 were both amended on 2026-09-08 under one principle:
# A WINDOW MAY HAND OFF WITH DEBT ONLY WHEN THE DEBT IS EXPLICIT AND OWNED; IT MAY NEVER HAND
# OFF WITH DEBT THAT IS SILENT. Row 10 is where P11 joins them -- the precedent for a handoff
# refusing debt at a PREFLIGHT row is `to-cc/DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08.md` and
# `to-cc/DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`, cited in the row's own evidence.
#
# THE LEG ORDER IS LOAD-BEARING and is how the 2026-09-08 `-1` run read a 7-file shortfall as
# 2. THE STATED VALUE DECIDES WHICH LEG APPLIES. Several live decision files carry explanatory
# prose containing paths that DO resolve on `main` while their stated value is the literal
# `OPEN`; a path-first read passes them on evidence that is not their carrier value and
# silently under-counts the OPEN set. `OPEN` is therefore tested FIRST, and only on the value.
#
# WHAT THE VALUE LEG DOES NOT PROVE, so it is not overclaimed (HANDOFF_PROCESS §5): it tests
# that the named home EXISTS on `main`, never that the decision was written INTO it. A carrier
# naming a real file whose body says nothing about the ruling resolves, and that is correct by
# the letter of 031 §2.2. Closing that is a judgment, not a probe.

#: THREE PREFIXES BY DECISION, not by accident (HANDOFF_PROCESS §5): 031 §2 names these because
#: they are the shapes that RULE. `ADDENDUM-`, `FINDING-` and `RULING-RELAY-` are measurements
#: and relays carrying no authority (C-1), so they are outside the enum; widening it is a
#: ruling, not a lane's call.
CARRIAGE_PREFIXES = ("DECLARE-", "AMEND-", "BATCH-")

#: The key is read from the file HEAD -- the first six lines, which is where the live
#: 2026-09-08 measurement read it and what AMEND-643-001 §1(a) specifies. ANCHORED *and*
#: POSITIONED: a `carried-by:` further down is body prose, and P11's own lesson is that a
#: predicate matching the DESCRIPTION of an event cannot distinguish the event from its
#: specification. Measured over the 2026-09-06 window: a bare substring test returned 5 of 13
#: with three of the five matching on prose about something else; the anchored form returned
#: 13 of 13 on the same population.
CARRIAGE_HEAD_LINES = 6

CARRIAGE_RESOLVES = "resolves"
CARRIAGE_OPEN = "open"
CARRIAGE_NO_KEY = "no-key"
CARRIAGE_UNRESOLVED = "unresolved"

_CARRIED_BY_RE = re.compile(r"^carried-by:[ \t]*(\S.*)$", re.MULTILINE)

#: The value states the literal `OPEN` -- tested at the START of the value, and nowhere else.
#: `AMEND-DAY-001` opens with a resolving path and says "carried OPEN" mid-prose; the live
#: measurement counts it among the 18 that RESOLVE, and an unanchored search would not.
_OPEN_VALUE_RE = re.compile(r"^OPEN\b")

#: Repo-home candidates inside a `carried-by:` value. NOT `verify_handoff_probes._FILE_RE`,
#: and the divergence is deliberate rather than an oversight: that tokenizer requires a file
#: EXTENSION, while a repo home may be a DIRECTORY -- `DECLARE-BROWSER-TOPOLOGY-2026-09-06.md`
#: names `docs/intake/` and the live measurement counts it as resolving, because a tree is a
#: home. So: any slash-bearing path, plus a bare root-level file with a known extension
#: (`JOURNAL.md`, `LESSONS.md`). The leading lookbehind is that module's, reused verbatim, so
#: `~/.claude/...` and mid-token matches do not produce phantom candidates.
_CARRIER_TOKEN_RE = re.compile(
    r"(?<![\w.\-/\\:])(?:(?:[\w.-]+/)+[\w.-]*|[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1))"
)

#: A `..` segment is not a clean repo-relative home. Same guard, same reason, as F4 in
#: `verify_handoff_probes`: without it a carrier can name its way out of the tree.
_CARRIER_UNCLEAN_RE = re.compile(r"(?:^|/)\.\.(?:/|$)")


@dataclass(frozen=True)
class CarriageVerdict:
    """One decision file's P11 state: the verdict, the value it was read from, and why."""
    path: Path
    kind: str
    value: "str | None"
    detail: str

    def render(self) -> str:
        return f"{self.path.name} ({self.detail})"


def decision_files(transport) -> list[Path]:
    """Every `DECLARE-`/`AMEND-`/`BATCH-` file on the live transport, `to-cc/` + `to-browser/`.

    NON-RECURSIVE, unlike `_question_files`, and the asymmetry is intended. An unanswered
    question does not age out of its population by being archived -- archiving is not a
    disposition. A decision file is the opposite: it is a SEALED record of the window that
    ruled it, its carriage was judged in that window, and re-judging it here would condemn a
    past window for the present's rule -- the one thing "judged by their own era" forbids. The
    live 2026-09-08 measurement counted the same top-level population (25 files).
    """
    root = Path(transport)
    found: list[Path] = []
    for sub in ("to-cc", "to-browser"):
        d = root / sub
        if not d.is_dir():
            continue
        found += [p for p in d.glob("*.md")
                  if p.is_file() and p.name.startswith(CARRIAGE_PREFIXES)]
    return sorted(found, key=lambda p: (p.parent.name, p.name))


def carried_by_value(path) -> "str | None":
    """The ANCHORED `carried-by:` value from the file head, or None when there is no such key."""
    try:
        head = "".join(Path(path).read_text(encoding="utf-8", errors="replace")
                       .splitlines(keepends=True)[:CARRIAGE_HEAD_LINES])
    except OSError:
        return None
    m = _CARRIED_BY_RE.search(head)
    return m.group(1).strip() if m else None


def _carrier_tokens(value: str) -> list[str]:
    """Repo-home candidates in a carrier VALUE, de-duplicated, in order of appearance."""
    out: list[str] = []
    for tok in _CARRIER_TOKEN_RE.findall(value):
        # A citation dies on a trailing period: `…close-packet.md.` and `…manifest.md,` are the
        # same home as the bare path, and a token keeping the punctuation resolves against
        # nothing. Trailing `/` is KEPT -- it is what marks a directory home.
        tok = tok.rstrip(".-")
        if not tok or _CARRIER_UNCLEAN_RE.search(tok):
            continue
        out.append(tok)
    return list(dict.fromkeys(out))


def _resolves_on_main(repo_root, token: str) -> bool:
    """`git cat-file -e main:<token>` -- one resolution predicate, and it reads `main`.

    NOT the working tree, and that is the whole point of the leg: a carrier naming a file that
    exists only in an unmerged branch or only on disk has not been carried anywhere the next
    seat can read. A trailing `/` is stripped because `main:docs/intake/` is not a valid object
    name while `main:docs/intake` resolves to the tree -- the same home, spelled the way git
    spells it. Isolated as a function so a fixture with no git history can monkeypatch it.
    """
    rel = token.rstrip("/")
    if not rel:
        return False
    ok, _out = _git_status(Path(repo_root), "cat-file", "-e", f"main:{rel}")
    return ok


def carriage_verdicts(transport, repo_root) -> list[CarriageVerdict]:
    """P11's per-file verdict for every decision file on `transport`. Read-only (Layer-2)."""
    verdicts: list[CarriageVerdict] = []
    for path in decision_files(transport):
        value = carried_by_value(path)
        if value is None:
            verdicts.append(CarriageVerdict(
                path, CARRIAGE_NO_KEY, None,
                f"no flush-left `carried-by:` in the first {CARRIAGE_HEAD_LINES} lines -- a key "
                "inside an HTML comment, or in the body, is not anchored"))
            continue
        # LEG ORDER. The STATED VALUE decides the leg; see the block header for the measured
        # under-count a path-first read produced.
        if _OPEN_VALUE_RE.match(value):
            verdicts.append(CarriageVerdict(
                path, CARRIAGE_OPEN, value,
                "states the literal `OPEN` -- discharged only by this bundle's residual naming "
                "the file, which is leg 2 and gates at assemble time"))
            continue
        tokens = _carrier_tokens(value)
        home = next((t for t in tokens if _resolves_on_main(repo_root, t)), None)
        if home is not None:
            verdicts.append(CarriageVerdict(path, CARRIAGE_RESOLVES, value,
                                            f"resolves on `main`: {home}"))
            continue
        verdicts.append(CarriageVerdict(
            path, CARRIAGE_UNRESOLVED, value,
            "names no repo home that resolves on `main` (candidates read from the value: "
            + (", ".join(tokens) if tokens else "none") + ")"))
    return verdicts


def _residual_names(residual: str, path: Path) -> bool:
    """True when `residual` names THIS decision file by its transport-relative path.

    QUALIFIED, not a bare basename, and the difference is not pedantry. The predicate was
    `path.name in residual` — a raw substring search — which reported debt as carried in two
    distinct ways (terra, 2026-09-09):

      1. AMBIGUITY. `to-cc/X.md` and `to-browser/X.md` are different decisions. One mention of
         `X.md` discharged BOTH, so a single sentence cleared a file nobody had considered.
      2. INCIDENTAL MENTION. Any occurrence satisfied it — the filename in an unrelated
         sentence, inside a code fence, cited for some other purpose entirely.

    The rest of the system already speaks this form: the leg-2 refusal prints
    `to-cc/NAME.md`, the acceptance rung prints it, and every residual that discharges a
    carrier in practice writes it that way. Only the predicate was reading the unqualified
    half of its own convention.

    Both separators are accepted because a residual is prose a human types: markdown says
    `to-cc/X.md` and a Windows paste may say `to-cc\\X.md`, and neither is a different claim.
    """
    qualified = f"{path.parent.name}/{path.name}"
    return qualified in residual or qualified.replace("/", "\\") in residual


def carriage_shortfall(transport, repo_root, *,
                       residual: "str | None" = None) -> list[CarriageVerdict]:
    """The files that fall short of P11, across BOTH legs where both are checkable.

    `residual=None` is PREFLIGHT: leg 2's second operand does not exist yet, so an `OPEN` value
    is not judged. Pass the filled residual text -- which is what `assemble_paste` has -- and
    an `OPEN` file the residual does not NAME joins the shortfall. This is the one predicate
    both stages call, so the two can never drift into disagreeing about the same file.
    """
    short: list[CarriageVerdict] = []
    for v in carriage_verdicts(transport, repo_root):
        if v.kind in (CARRIAGE_NO_KEY, CARRIAGE_UNRESOLVED):
            short.append(v)
        elif (v.kind == CARRIAGE_OPEN and residual is not None
              and not _residual_names(residual, v.path)):
            short.append(v)
    return short


def _row_p11_carriage(transport, repo_root) -> PreflightRow:
    """Row 10 -- LEG 1 of P11: every decision file carries an anchored, resolving `carried-by:`.

    An `OPEN` value PASSES here by construction and its obligation is stated, never implied --
    the same discipline rows 1 and 7 are implemented under, and for the same reason: a row must
    not report a safety it does not provide, and it must not hide one it only asserts. The
    residual half is leg 2, in `assemble_paste.py`.
    """
    if transport is None:
        return _no_transport("p11_carriage")
    locator = (f"{Path(transport)} (to-cc/ + to-browser/, "
               + "/".join(CARRIAGE_PREFIXES) + ") x `git cat-file -e main:<path>`")
    verdicts = carriage_verdicts(transport, repo_root)
    if not verdicts:
        return _na_row("p11_carriage", "SUBJECT-ABSENT",
                       "no DECLARE-/AMEND-/BATCH- file on the transport -- this window put no "
                       "decision on it, so there is no carriage to test", locator)
    failing = [v for v in verdicts if v.kind in (CARRIAGE_NO_KEY, CARRIAGE_UNRESOLVED)]
    if failing:
        shown = "; ".join(v.render() for v in failing[:4])
        more = f" +{len(failing) - 4} more" if len(failing) > 4 else ""
        return PreflightRow("p11_carriage", PREFLIGHT_FAIL, locator,
                            f"{len(failing)} of {len(verdicts)} decision file(s) carry no "
                            f"anchored `carried-by:` resolving on `main`: {shown}{more}")
    carried = [v for v in verdicts if v.kind == CARRIAGE_OPEN]
    tail = ""
    if carried:
        tail = (f". CARRIED, and the cut is only honest if it holds: each of the {len(carried)} "
                "`OPEN` carrier(s) is named in this bundle's residual -- checked at assemble "
                "time by leg 2, not here, because the residual does not exist yet "
                "(DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / "
                "DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08 are the family precedent)")
    return PreflightRow("p11_carriage", PREFLIGHT_PASS, locator,
                        f"all {len(verdicts)} decision file(s) anchored "
                        f"({len(verdicts) - len(carried)} resolve on `main`, "
                        f"{len(carried)} OPEN){tail}")


#: Item 12/L7: the two rows keyed to TODAY's transport state. At a cut they are real hygiene;
#: at a batch-close trial cut they are false-red by construction (proposal PM3) -- the
#: transport's ledger/ratification are refreshed once per window, not once per trial cut.
TRIAL_CUT_EXCLUDED_ROWS = ("ledger_refreshed", "ratification_present")

#: AMEND-HANDOFF-REDESIGN-BUILD-2026-10-01 §2: `memory_within_cap` is evaluated live at the
#: real cut (never fixtured there), but a FAIL never blocks -- "it measures the machine, not
#: the repository." `worktree_owners`, the other live-state row, is a genuine precondition
#: and stays out of this tuple (its own FAIL still refuses, its own test says so). A row named
#: here is carried into the receipt's `preflight_notes` instead of raising `PreflightError`.
PREFLIGHT_NON_BLOCKING_ROWS = ("memory_within_cap",)


def preflight_rows(repo_root: Path, *, transport=None, today: "str | None" = None,
                   repo_name: "str | None" = None, sessions_root=None,
                   memory_path=None, bundle_dir: "Path | None" = None,
                   force_filled: bool = False, trial_cut: bool = False) -> list[PreflightRow]:
    """The ten hygiene rows, in `PREFLIGHT_ROW_NAMES` order. Read-only (Layer-2).

    `bundle_dir` / `force_filled` ([#1123]) name the bundle a `--filled` re-render is about to
    write, so row 1 can tell its own known BD-manifest circularity from an unrelated hard-fail
    -- see `_row_ship_gate`. Both default to the prior behaviour (no bundle named, never waived).

    `trial_cut=True` (item 12/L7, the batch-close stage) reports `TRIAL_CUT_EXCLUDED_ROWS` as
    n/a instead of evaluating them -- at batch close there is no real cut window for "ledger
    refreshed today" / "ratification present today" to be a property of, so evaluating them for
    real would false-red the trial cut on every run, by construction, independent of the state
    this lane's diff actually changed.
    """
    if not _is_hub(repo_root):
        return [_na_row(n, "NOT-APPLICABLE",
                        "hub-only -- this transport window, the stamped-doc set and ADR-85's "
                        "JOURNAL shape are all hub-owned", "gen_handoff._is_hub")
                for n in PREFLIGHT_ROW_NAMES]
    today = today or _dt.date.today().isoformat()
    repo_name = repo_name or _main_checkout(Path(repo_root)).name
    transport = transport_root() if transport is None else transport

    def _cut_day_row(name, real) -> PreflightRow:
        if trial_cut and name in TRIAL_CUT_EXCLUDED_ROWS:
            return _na_row(name, "TRIAL-CUT-EXCLUDED",
                           "cut-day row, false-red by construction at a batch-close trial cut "
                           "(item 12/L7) -- excluded, not evaluated", "gen_handoff.preflight_rows")
        return real()

    return [
        _row_ship_gate(repo_root, bundle_dir=bundle_dir, force_filled=force_filled),
        _cut_day_row("ledger_refreshed",
                     lambda: _row_ledger_refreshed(transport, repo_name, today)),
        _cut_day_row("ratification_present",
                     lambda: _row_ratification_present(transport, today)),
        _row_status_budget(transport),
        _row_living_docs_stamped(repo_root),
        _row_journal_anchored(repo_root),
        _row_question_disposition(transport, today, repo_root),
        _row_memory_within_cap(memory_path or _memory_path(repo_root)),
        _row_worktree_owners(repo_root, sessions_root),
        _row_p11_carriage(transport, repo_root),
    ]


def assert_preflight(repo_root: Path, **kw) -> "list[PreflightRow]":
    """Raise `PreflightError` naming EVERY failing row, or return cleanly.

    A row named in `PREFLIGHT_NON_BLOCKING_ROWS` (AMEND §2) is excluded from the raise even
    when it FAILed -- its verdict still comes back in the returned list, so a caller can carry
    it into the bundle notes (`_write_receipt`'s `preflight_notes`) rather than lose it.
    """
    rows = preflight_rows(repo_root, **kw)
    failed = [r for r in rows if r.failed and r.name not in PREFLIGHT_NON_BLOCKING_ROWS]
    if failed:
        raise PreflightError(
            "refusing to cut a bundle: " + str(len(failed)) + " pre-handoff hygiene row(s) "
            "FAILED -- " + " | ".join(r.render() for r in failed)
            + ". Each row is a property of the window this bundle would seal, and a committed "
              "bundle is immutable. Clear the row, then cut.")
    return rows


def _load_target_audit(repo_root: Path):
    """Import `<repo_root>/scripts/audit.py` WITHOUT making it this process's `audit`.

    THE BUG THIS REPLACES, written down so nobody tidies the import back to its obvious
    spelling. `collect_hints` used to do

        sys.path.insert(0, str(repo_root / "scripts"))
        import audit as _aud

    and undo neither half. Against the live hub that is a no-op twice over, so it looked
    harmless for as long as the only caller was the live hub. Against ANY OTHER tree -- above
    all `tests/test_gen_handoff.py`'s stub repo, whose `scripts/audit.py` is the single line
    `ALL_CHECKS = []` -- it published a temp fixture as `sys.modules["audit"]` and left that
    directory FIRST on `sys.path` for the rest of the process.

    MEASURED (2026-09-13): collecting `tests/test_gen_handoff.py` before
    `tests/test_residual_completeness.py` in one process reddened three tests in the second
    file with `module 'audit' has no attribute '_vrc'`; the same file alone was 29/29 green.
    The path half is wider than the module half: that stub directory also carries one-line
    placeholders for `validate_backlog`, `validate_doc_claims`, `validate_git_backlog` and
    `gen_task_tree`, and an import of any of those resolves to a module with nothing in it --
    which does not fail, it passes vacuously.

    WHY THE PATH STILL GOES ON, briefly: a real repo's `audit.py` imports its siblings by bare
    name, so the target's `scripts/` has to be reachable while the module executes. It is put
    there for the length of the exec and taken off again, and every module name the exec
    introduced goes with it. A hint is a READ, and a read has no business changing what the
    rest of the process means by a module name.
    """
    source = Path(repo_root) / "scripts" / "audit.py"
    if not source.is_file():
        return None
    # Never "audit": the name is the whole hazard, so the probe does not claim it even
    # transiently -- a concurrent importer must not be able to observe the stub under it.
    spec = importlib.util.spec_from_file_location("_gen_handoff_audit_probe", source)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    path_before, modules_before = list(sys.path), set(sys.modules)
    sys.path.insert(0, str(source.parent))
    sys.modules[spec.name] = module   # module-level dataclasses resolve their own __module__
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = path_before
        for name in set(sys.modules) - modules_before:
            sys.modules.pop(name, None)
    return module


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
        _aud = _load_target_audit(repo_root)
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
    one. The fallback fires ONLY for a retired name that is ABSENT — a non-retired VISION
    that goes missing still degrades, and so does a PRESENT VISION whose `## Vision` section
    is missing or malformed. That second case is the sharp one: reaching for README there
    would substitute someone else's prose for a broken file and hide the breakage, which is
    the exact failure the degrade contract exists to prevent."""
    def _section(path: Path) -> "str | None":
        if not path.exists():
            return None
        text = path.read_text(encoding="utf-8")
        m = re.search(rf"^{re.escape(_cdocs.VISION_EXTRACT_HEADING)}\s*\n(.*?)(?=^## |\Z)",
                      text, re.DOTALL | re.MULTILINE)
        return m.group(1).strip() if m else None

    vision = repo_root / _cdocs.VISION
    if vision.exists():
        # PRESENT beats retired: a file that is there is the authority on its own content,
        # and a missing section in it degrades rather than falling through to README.
        found = _section(vision)
        return found if found is not None else _cdocs.VISION_EXTRACT_MISSING
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
              "P7/P4/P6/P9's live answers, which CC re-derives from PROBES.md. The frame covers the "
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


# --- SUPPLEMENT fixed slots (lane-handoff-min, Part A Done-when 4) ---------------------------
#
# Decision rule 2: "The outgoing seat's judgement goes in fixed slots of the existing
# SUPPLEMENT (headline · open threads with carriers · next authorized action · contingencies ·
# do-not-repeat)." Part A's scope is the minimum that makes that checkable — five labeled
# lines the operator restates their chat answer as, ADDITIVE to the existing QUESTIONS/ANSWERS
# shape (SUPPLEMENT.md.tmpl's schema is otherwise UNCHANGED: a full schema migration is
# `protocols/HANDOFF_PROCESS.md` §13's call, and touching that file forces a coupled version
# bump — explicitly Not in A). The refusing MOMENT (a harness-wired `seat-release` transaction)
# is Part B; what fires here is a plain function call on the next re-render of an
# already-written supplement, which is the only trigger this lane owns.

#: The five slot labels, exactly as they must open a line in the ANSWERS region. Order is the
#: Decision text's own order.
SUPPLEMENT_FIXED_SLOTS: tuple[str, ...] = (
    "Headline", "Open threads (with carriers)", "Next authorized action", "Contingencies",
    "Do-not-repeat",
)

#: `[ \t]*`, never `\s*`, around the `:` -- `\s` matches `\n` too, so a GREEDY `\s*` after the
#: colon on a BLANK slot (nothing between `:` and end of line) swallows that newline and any
#: leading whitespace of the NEXT line before `(.*)$` captures the rest of THAT line as this
#: slot's own value -- silently absorbing the next label's line into this one's match and
#: making the FOLLOWING label vanish from `finditer` entirely, rather than reading as blank
#: (found by Done-when 4's own acceptance run, 2026-09-27: a blank "Next authorized action:"
#: immediately followed by "Contingencies: none" mis-reported "Contingencies" as the missing
#: slot).
_FIXED_SLOT_LINE_RE = re.compile(
    r"(?im)^[ \t]*(" + "|".join(re.escape(s) for s in SUPPLEMENT_FIXED_SLOTS)
    + r")[ \t]*:[ \t]*(.*)$")


def fixed_slots(answers_text: str) -> dict[str, str]:
    """The fixed-slot labels found in an ANSWERS region, mapped to their content (last match
    wins, so a restated/corrected line overrides an earlier draft of the same slot). A label
    with no content after its `:` maps to `""`, which `assert_supplement_fixed_slots` treats
    the same as the label being altogether absent — see there."""
    found: dict[str, str] = {}
    for m in _FIXED_SLOT_LINE_RE.finditer(answers_text):
        # Canonicalize case/whitespace so "headline:" and "Headline:" are the same slot.
        label = next(s for s in SUPPLEMENT_FIXED_SLOTS if s.lower() == m.group(1).strip().lower())
        found[label] = m.group(2).strip()
    return found


class SupplementSlotError(RuntimeError):
    """Generation refused: a FILLED supplement omits, or leaves empty, a Part A fixed slot.

    Fires only on an already-written SUPPLEMENT.md whose ANSWERS region is non-empty
    (`assemble_paste._extract_answers` returns something) — an untouched or deliberately empty
    supplement is the defined cold-handoff disposition and is never refused (the supplement's
    own lifecycle comment: "the artifact exists even for a cold / cleared handoff")."""


def assert_supplement_fixed_slots(supplement_path: Path) -> None:
    """Raise `SupplementSlotError`, naming every missing/empty slot, when `supplement_path`
    exists, is FILLED, and omits one of `SUPPLEMENT_FIXED_SLOTS` or leaves it blank. A no-op
    when the file is absent or cold."""
    supplement_path = Path(supplement_path)
    if not supplement_path.is_file():
        return
    sys.path.insert(0, str(_SCRIPTS))
    from assemble_paste import _extract_answers  # noqa: PLC0415
    answers = _extract_answers(supplement_path.read_text(encoding="utf-8"))
    if answers is None:
        return                      # cold / unfilled -- the defined, non-refused disposition
    found = fixed_slots(answers)
    missing = [s for s in SUPPLEMENT_FIXED_SLOTS if not found.get(s, "").strip()]
    if missing:
        raise SupplementSlotError(
            f"refusing: {supplement_path} is filled but omits {len(missing)} fixed slot(s): "
            + "; ".join(missing)
            + ". Restate the answer as five labeled lines (`Headline:`, `Open threads (with "
              "carriers):`, `Next authorized action:`, `Contingencies:`, `Do-not-repeat:`), "
              "each non-empty — `\"none\"` is a valid non-empty value, a blank line is not."
        )


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
# PUBLIC (no leading underscore) and imported by scripts/assemble_paste.py's window-specific
# ratio [#611] — one regex, one home, the same cross-module-import pattern already used for
# HANDOFF_BOOT_BYTE_BUDGET (assemble_paste -> audit_checks) and reflow_framing (gen_handoff ->
# assemble_paste). A FILL-IN region's body is, by construction, the only span of a rendered
# bundle file that is hand-authored rather than generator output (RF-6) — the mechanized
# definition of "window-specific" byte the ratio measures against.
FILL_IN_RE = re.compile(
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
    prior = {m.group("name"): m.group("body") for m in FILL_IN_RE.finditer(existing)}
    def _repl(m: re.Match) -> str:
        name = m.group("name")
        if name in prior:
            return m.group("open") + prior[name] + m.group("close")
        return m.group(0)
    return FILL_IN_RE.sub(_repl, rendered)


# --- the boot as DATA + PROSE (lane-boot-contract, WAVE5B-N2 row 12) ----------------------
#
# The pasted header of HANDOFF_BOOT.md is two delimited parts. The DATA block is emitted here,
# row by row, and every row has a rule in `verify_handoff_probes.BOOT_DATA_RULES` — the two sets
# are held equal by a test, so a fact added here without a probe FAILs rather than riding along
# as unchecked text. The PROSE block is the template's, and holds only the hand-authored FILL-IN
# regions (purpose, the destination's worktree / write-scope / mode basis) plus the one
# generated-at line, under the byte budget below. The doctrine pointers that used to ride in
# unverified `>` blocks are DATA rows now; the assembler's shed has nothing left to shed.
#
# ANSWER-FREE, unchanged: every row is an identity (slug, mode, title, destination), the role
# pin's version (already in the paste's ROLE PIN) or a pointer — never a count, sha or verdict.

#: The PROSE block's budget, in bytes of prose a seat reads (HTML comments — the FILL-IN
#: markers — excluded; `verify_handoff_probes.prose_bytes`). MEASURED, not invented: the
#: 2026-09-24 bundle's own hand-authored purpose / worktree / write-scope / mode-basis, re-laid
#: in this shape, measure 1,541 B (an unfilled render: 527 B); the budget is that plus ~30 %
#: headroom, rounded. Checked by probe
#: `BP-budget` at the cut and on every commit that stages the bundle.
BOOT_PROSE_BYTE_BUDGET = 2_000


def spec_version(repo_root: Path) -> "str | None":
    """The live HANDOFF_PROCESS `Version:` — the assembler's ONE regex, read, never hard-coded.
    None when the spec or its line is absent (the Role row then renders `unreadable` and its
    probe FAILs, which is the honest outcome)."""
    spec = Path(repo_root) / "protocols" / "HANDOFF_PROCESS.md"
    if not spec.is_file():
        return None
    sys.path.insert(0, str(_SCRIPTS))
    from assemble_paste import _VERSION_RE  # noqa: PLC0415 (sibling CLI; deferred import)
    m = _VERSION_RE.search(spec.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else None


def boot_data_rows(slug: str, mode: str, chat_title: str, role_version: "str | None", *,
                   state_rows: "list | None" = None) -> list[tuple[str, str]]:
    """The DATA rows, in paste order. Each key has exactly one rule in `BOOT_DATA_RULES`, and
    every pointer, self-pointer and the launcher line is rendered FROM the verifier's tables
    (`BOOT_POINTERS`, `BOOT_SELF_POINTERS`, `LAUNCH_COMMAND`), so the two cannot disagree.

    lane-handoff-min (Part A): `state_rows`, when given, is a list of `handoff_state.StateRow`
    — the live facts (`handoff_state.STATE_ROW_KEYS`) appended after the identity rows above.
    It is computed ONCE by the
    caller (`generate`, via `handoff_state.state_rows`) rather than derived here, because one
    of them is a live CI poll and this function must not repeat a network call per render
    or per test. `state_rows=None` (an epic/functional caller, or a direct unit-test call that
    only cares about the identity rows) renders the identity rows only."""
    def ptr(key: str) -> str:
        return " · ".join(f"`{p}`" for p in _vhp().BOOT_POINTERS[key])

    def own(key: str) -> str:
        return f"`docs/handoffs/{slug}/{_vhp().BOOT_SELF_POINTERS[key]}`"
    rows = [
        ("Slug", f"`{slug}`"),
        ("Chat title", f"`{chat_title}`"),
        ("Mode", f"**{mode}**"),
        ("Destination", f"branch `{_PRIMARY_TREE_BOOT_DESTINATION}`"),
        ("Role", f"{ptr('Role')} @ handoff-process v{role_version or 'unreadable'}"),
        ("Launch", f"`{_vhp().LAUNCH_COMMAND}`"),
        ("Probes", own("Probes")),
        ("Receipt", own("Receipt")),
        ("Seat orders", ptr("Seat orders")),
        ("Routing", ptr("Routing")),
        ("Rules", ptr("Rules")),
        ("Runbook", ptr("Runbook")),
        ("Harness", ptr("Harness")),
    ]
    if state_rows:
        rows += [(row.key, row.rendered()) for row in state_rows]
    return rows


def boot_data_block(rows: list[tuple[str, str]]) -> str:
    """The delimited DATA block, verbatim as it lands in the boot header."""
    body = "\n".join(f"| **{k}** | {v} |" for k, v in rows)
    vhp = _vhp()
    return (f"{vhp.BOOT_DATA_BEGIN}\n| Data | Probe-checked — `verify_handoff_probes` BD-* |\n"
            f"|---|---|\n{body}\n{vhp.BOOT_DATA_END}")


# --- the handoff receipt and its boot-cost field ---------------------------------------------
#
# WHAT IS MEASURED. "Turns to first correct dispatch" of the seat that booted from the bundle
# this cut SUPERSEDES — the plan's P3 gate ("a new seat boots in <= 5 turns") read as the C4
# research's sharper form: turns to a dispatch that held, not to any output. It is measured at
# the NEXT cut because that is the first moment it has happened.
#
# WHY A TALLY, and why it is honest to say so. The architect seat is a browser chat: it keeps no
# transcript the repo can read (HANDOFF_PROCESS §5 — "the browser has no file access"), so no
# organ can count its turns. The one instrument that can is the operator, who watched them; the
# C4 research names that as the honest instrument for a turn count. The generator therefore
# records the operator's count ONLY when it names the dispatch it counts to, and only when that
# dispatch is witnessable: an order under `to-cc/` that exists on the transport and was not
# superseded. Anything less is `unmeasured — <why>`, never a guess and never a zero.

_BOOT_COST_MEASURES = "the seat that booted from the bundle this cut supersedes"


def boot_cost(turns: "int | None" = None, dispatch: "str | None" = None,
              transport: "Path | None" = None) -> dict:
    """The receipt's `boot_cost` field: measured, or `unmeasured — <why>` with no value."""
    norm = dispatch.replace("\\", "/").lstrip("./") if dispatch else None
    base = {"metric": _vhp().BOOT_COST_METRIC, "value": None, "status": "", "dispatch": norm,
            "measures": _BOOT_COST_MEASURES}
    if turns is None and norm is None:
        why = ("no tally recorded at this cut — the browser seat keeps no transcript the repo "
               "can read (HANDOFF_PROCESS §5), so the count is the operator's; pass "
               "--boot-turns N --boot-dispatch to-cc/<order>.md when cutting")
    elif turns is None:
        why = f"a dispatch (`{norm}`) with no turn count"
    elif isinstance(turns, bool) or not isinstance(turns, int) or turns < 1:
        why = f"not a turn count: {turns!r}"
    elif norm is None:
        why = "a turn count that names no dispatch cannot say which dispatch was correct"
    elif not (norm.startswith("to-cc/") and norm.endswith(".md")):
        why = f"`{norm}` is not a dispatch order (a `to-cc/<order>.md` file)"
    elif "superseded" in norm.lower():
        why = f"`{norm}` was superseded — a withdrawn order is not a correct dispatch"
    elif transport is None:
        why = f"the transport is unresolved, so `{norm}` cannot be witnessed"
    elif not (Path(transport) / norm).is_file():
        why = f"`{norm}` does not exist on the transport"
    else:
        # The count is the operator's and says so (terra HIGH, 2026-09-25: a CLI value must not
        # read as machine-witnessed). What IS witnessed is the dispatch, and it is bound by
        # content hash, so a later edit or rename of that order is detectable from the receipt.
        import hashlib  # noqa: PLC0415
        digest = hashlib.sha256((Path(transport) / norm).read_bytes()).hexdigest()
        return {**base, "value": turns, "status": "measured", "dispatch_sha256": digest,
                "source": ("operator tally (--boot-turns) — the count is the operator's, not "
                           "machine-witnessed; the dispatch is witnessed on the transport and "
                           "bound by dispatch_sha256")}
    return {**base, "status": _vhp()._UNMEASURED_PREFIX + why, "source": None}


def _write_receipt(bundle_dir: Path, *, slug: str, mode: str, date: str, cut: str,
                   cost: dict, paste: dict, manifest: "dict | None" = None,
                   repo_root: "Path | None" = None,
                   transport: "Path | None" = None,
                   preflight_notes: "list[str] | None" = None) -> Path:
    """Write `<bundle>/HANDOFF_RECEIPT.json`, WHOLE, every generation (the FUNNEL_HEALTH
    contract: overwritten, never merged). A bundle artifact, not a browser-visible one — the
    assembler never reads it — so its numbers do not touch the answer-free paste.

    `repo_root`/`transport` (ADR-129 item 14/L9): gated on `transport`, not `repo_root` alone
    (every caller passes a real `repo_root`, stub or not — gating there would make every test's
    `generate()` call pay for a `gh` subprocess it never asked for, see the comment at the gate
    below). `transport is not None` is what makes the receipt also carry `whole_repo_verdict`
    (`_whole_repo_verdict`, read-only, never run — item 8/L3) and
    `refusal_count_since_previous_cut` (`_refusal_count_since_previous_cut`, read from the
    transport-side refusal log — item 14/L9). `transport=None` (the default; every caller
    that does not explicitly opt in) omits both fields rather than resolving a live transport
    or spawning a `gh` subprocess the caller never asked for.

    `manifest` (lane-handoff-min, Part A; ADR-HANDOFF-SYSTEM Decision rule 1) is the per-file
    sha256 census a publish step verifies against — see `bundle_manifest` / `publish_bundle` /
    `verify_published`. `None` for a mode this lane's manifest walk does not cover.

    `preflight_notes` (repair U3, AMEND §2): the rendered verdict of every
    `PREFLIGHT_NON_BLOCKING_ROWS` row from THIS cut's own `assert_preflight` call — carried
    here because a non-blocking row's FAIL is still a fact the next reader needs, even though
    it never raised `PreflightError`. Empty/omitted, never a placeholder key, when the caller
    passes nothing (every pre-U3 caller)."""
    import json  # noqa: PLC0415
    out = bundle_dir / _vhp().RECEIPT_FILE
    body = {"schema": "handoff-receipt/1", "generator": "scripts/gen_handoff.py", "slug": slug,
            "mode": mode, "date": date, "cut": cut, "boot_cost": cost, "paste": paste,
            "manifest": manifest}
    if preflight_notes:
        body["preflight_notes"] = preflight_notes
    # Gated on `transport`, not merely `repo_root` -- caught same-session (terra-style
    # self-catch, the second half of the same incident): gating on `repo_root is not None`
    # alone made EVERY test's successful `generate()` call (which always passes a real
    # `repo_root`, stub or not) spawn a `gh` subprocess via `_whole_repo_verdict` -- the full
    # three-file suite went from ~400s to still running past 20 minutes (78% in, one failure
    # not yet even reached) before this was caught and reverted to the `transport` opt-in that
    # already gates the refusal log, which is explicit and `None` by default everywhere except
    # the CLI `main()` and a test that deliberately wants this leg.
    if transport is not None:
        body["whole_repo_verdict"] = _whole_repo_verdict(repo_root)
        body["refusal_count_since_previous_cut"] = _refusal_count_since_previous_cut(transport)
    out.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
                   newline="\n")
    return out


# --- the cut manifest, and publishing to a transport copy (lane-handoff-min, Part A) ----------
#
# Decision rule 1: "The manifest (cut id, source sha, generation time, per-file sha256,
# per-row freshness class) extends HANDOFF_RECEIPT.json." `seat-release`'s refusing-transaction
# and the CI manifest check are Part B (moments) — NOT IN A. What Part A owns is the manifest's
# DATA and a way to prove a published copy is sha-equal to it, so Part B has something to check
# against once its own trigger exists.

def _sha256_file(path: Path) -> str:
    import hashlib  # noqa: PLC0415
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bundle_file_shas(bundle_dir: Path) -> dict[str, str]:
    """Every bundle file's sha256, keyed by its path relative to the bundle — EXCEPT the
    receipt itself, which cannot hash its own not-yet-written content (the manifest is embedded
    IN the receipt, so the receipt's own bytes are never a manifested file)."""
    receipt_name = _vhp().RECEIPT_FILE
    out: dict[str, str] = {}
    for p in sorted(bundle_dir.rglob("*")):
        if not p.is_file() or p.name == receipt_name:
            continue
        out[p.relative_to(bundle_dir).as_posix()] = _sha256_file(p)
    return out


def bundle_manifest(bundle_dir: Path, *, source_sha: "str | None",
                    state_rows: "list | None" = None) -> dict:
    """The cut manifest: a fresh `cut_id`, the source sha, generation time, every bundle
    file's sha256 (see `_bundle_file_shas`), and the freshness class of each live state row
    this cut carries (`{}` for a mode with no state rows, e.g. epic/functional)."""
    import uuid  # noqa: PLC0415
    return {
        "cut_id": uuid.uuid4().hex[:12],
        "source_sha": source_sha,
        "generation_time": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "files": _bundle_file_shas(bundle_dir),
        "row_freshness": {row.key: row.freshness for row in (state_rows or [])},
    }


class ManifestPathError(ValueError):
    """A manifest `files` key does not resolve under the root it is joined against — an
    absolute path or a `..` escape. The manifest travels inside a JSON receipt, so a tampered
    receipt's keys are untrusted input the moment they drive a filesystem write or read."""


def _manifest_rel_path(root: Path, rel: str) -> Path:
    """`root / rel`, refused (`ManifestPathError`) unless the resolved result stays under
    `root` — the shared guard for `publish_bundle` and `verify_published`."""
    if Path(rel).is_absolute():
        raise ManifestPathError(f"manifest path {rel!r} is absolute, not relative to {root}")
    root_resolved = root.resolve()
    candidate = (root / rel).resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ManifestPathError(f"manifest path {rel!r} escapes {root}")
    return candidate


def publish_bundle(bundle_dir: Path, dest_dir: Path) -> dict:
    """Copy every file the bundle's OWN manifest names from `bundle_dir` into `dest_dir`
    (mirrored relative layout). `dest_dir` is a scratch "transport" copy — this is never the
    real `$CLAUDE_PROMPTS_DIR` (Part A Do-not: no publish from this lane touches the real
    transport). Raises `ValueError` when the bundle carries no manifest to publish from (it
    was never generated by this lane's `generate()`, or its receipt predates this feature), or
    `ManifestPathError` when a manifest key would escape `bundle_dir`/`dest_dir`."""
    receipt_path = bundle_dir / _vhp().RECEIPT_FILE
    import json  # noqa: PLC0415
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"{bundle_dir} carries no readable receipt to publish from: {exc}") from exc
    files = (receipt.get("manifest") or {}).get("files") or {}
    if not files:
        raise ValueError(f"{bundle_dir}'s receipt carries no manifest files to publish")
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    published = []
    for rel in sorted(files):
        src = _manifest_rel_path(bundle_dir, rel)
        dst = _manifest_rel_path(dest_dir, rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        published.append(rel)
    return {"dest": str(dest_dir), "files": published}


def verify_published(bundle_dir: Path, dest_dir: Path) -> list[str]:
    """The relative paths whose PUBLISHED copy no longer sha-matches the bundle's own
    manifest — `[]` means every published copy is sha-equal. A file the manifest names but the
    destination lacks, or cannot read, counts as a mismatch too (never silently skipped).
    Raises `ValueError` when the bundle carries no manifest to verify against (matching
    `publish_bundle`'s own refusal) rather than silently reporting a clean `[]` for a receipt
    that never recorded anything to check, and `ManifestPathError` for an escaping key."""
    import json  # noqa: PLC0415
    receipt = json.loads((bundle_dir / _vhp().RECEIPT_FILE).read_text(encoding="utf-8"))
    files = (receipt.get("manifest") or {}).get("files") or {}
    if not files:
        raise ValueError(f"{bundle_dir}'s receipt carries no manifest files to verify against")
    dest_dir = Path(dest_dir)
    mismatches = []
    for rel, want in sorted(files.items()):
        dst = _manifest_rel_path(dest_dir, rel)
        try:
            got = _sha256_file(dst) if dst.is_file() else None
        except OSError:
            got = None
        if got != want:
            mismatches.append(rel)
    return mismatches


def _paste_record(bundle_dir: Path, assembled: "int | None") -> dict:
    """The receipt's `paste` field: the bytes the gate measured, against the ceiling it states."""
    sys.path.insert(0, str(_SCRIPTS))
    from assemble_paste import PASTE_BYTE_CEILING  # noqa: PLC0415
    rec = {"bytes": None, "ceiling_bytes": PASTE_BYTE_CEILING,
           "ceiling_source": "scripts/assemble_paste.py::PASTE_BYTE_CEILING"}
    paste = bundle_dir / "PASTE_THIS.md"
    if assembled is None:
        return {**rec, "status": "not assembled (--no-assemble)"}
    if assembled != 0 or not paste.is_file():
        return {**rec, "status": f"refused (assembler exit {assembled})"}
    return {**rec, "bytes": paste.stat().st_size, "status": "assembled"}


class DryCutTargetError(ValueError):
    """A dry cut was pointed where its output could be committed — it writes outside every git
    work tree (or into a path that tree ignores), or not at all."""


def _dry_cut_refusal(bundle_root: Path, repo_root: Path) -> "str | None":
    """Why `bundle_root` may not take a dry cut, or None when it may.

    NOT MERELY "outside this repo" (terra CRITICAL, 2026-09-25): a sibling worktree's
    `docs/handoffs/` is outside `repo_root` and is exactly where a bundle gets committed, so a
    cut that skipped the boundary gates could land there. The rule is therefore: the target is
    in NO git work tree, or in one that IGNORES it (a job's tmp under an ignored directory).
    Anything git cannot answer about is refused — an unknown boundary is not a clean one."""
    if _inside(bundle_root, repo_root):
        return f"{bundle_root} is inside {repo_root}"
    target = Path(bundle_root).resolve()
    anchor = target
    while not anchor.exists() and anchor != anchor.parent:
        anchor = anchor.parent
    env = {k: v for k, v in os.environ.items() if k not in _git_location_env()}
    try:
        p = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(anchor),
                           capture_output=True, text=True, timeout=30, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"git could not say whether {target} is in a work tree ({type(exc).__name__})"
    if p.returncode != 0:
        if "not a git repository" in p.stderr:
            return None
        return f"git could not say whether {target} is in a work tree: {p.stderr.strip()}"
    top = Path(p.stdout.strip()).resolve()
    rel = target.relative_to(top).as_posix() if target != top else "."
    ignored, _out = _git_status(top, "check-ignore", "-q", rel)
    if ignored:
        return None
    return (f"{target} is inside the git work tree {top} and not ignored there — a bundle "
            "written there could be committed")


def _inside(path: Path, root: Path) -> bool:
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
    except (ValueError, OSError):
        return False
    return True


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
        # lane-boot-contract: the PROSE block's delimiters, owned by the verifier.
        "BOOT_PROSE_BEGIN": _vhp().BOOT_PROSE_BEGIN,
        "BOOT_PROSE_END": _vhp().BOOT_PROSE_END,
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


def _seat_boot_batch(repo_root: Path, slug: str) -> str:
    """What the five SEAT-BOOT pastes call this cut's batch.

    The manifest is asked first, because a boot titled with the batch it belongs to is the whole
    point of handing one to a dispatcher. Exactly one open batch answers it; zero or several make
    the question ambiguous, and the bundle slug is then the honest fallback -- it names the cut,
    which is a real identity, rather than guessing at a batch letter.
    """
    live = _open_batches(repo_root)
    return live[0].batch if len(live) == 1 else slug


def _write_seat_boots(bundle_dir: Path, repo_root: Path, slug: str, date: str) -> list:
    """CUT-TIME HOOK -- render the five SEAT-BOOT pastes into the bundle (INBOX 038).

    Seat boots are GENERATED BUNDLE ARTIFACTS, not browser prose: two consecutive incoming seats
    composed one by hand on 2026-09-08 and both were withdrawn (AMEND-BATCH-V-001 §1). The render
    lives in `scripts/gen_seat_boot.py`; this is only the call site, so the bundle engine gains a
    hook rather than a second copy of Ch8.

    DEGRADES TO NO FILES, never to a partial set. A render refusal here would otherwise take down
    a cut whose other seven artifacts are fine, and probe P12 reads the bundle afterwards -- an
    absent boot is drift it reports by name, so failing quietly is visible rather than silent.
    """
    sys.path.insert(0, str(_SCRIPTS))
    try:
        from gen_seat_boot import write_bundle  # noqa: PLC0415
        return list(write_bundle(bundle_dir, batch=_seat_boot_batch(repo_root, slug), date=date,
                                 repo_root=repo_root))
    except Exception as exc:                     # noqa: BLE001 -- a refused render is not a cut
        print(f"gen_handoff: SEAT-BOOT render skipped -- {exc}", file=sys.stderr)
        return []


def _write_funnel_health(bundle_dir: Path, repo_root: Path) -> Path:
    """Write the block to `<bundle>/FUNNEL_HEALTH.md`, WHOLE, every generation.

    Never spliced and never appended to — a stale block is worse than none, so the file is
    overwritten rather than merged. It is a bundle artifact, NOT a browser-visible one: it is
    absent from `assemble_paste`'s v5 manifest, so the answer-free invariant that governs
    BOOT / RESIDUAL / PROBES and the assembled paste is untouched by it."""
    out = bundle_dir / _FUNNEL_FILE
    out.write_text(funnel_health_block(repo_root), encoding="utf-8", newline="\n")
    return out


def _write_decision_ledger(bundle_dir: Path, repo_root: Path) -> "Path | None":
    """A9-2: write the DECISION LEDGER to `<bundle>/DECISION_LEDGER.md`, WHOLE, every generation.

    *"The bundle generator emits, from `decision_coverage`, every open decision with its state;
    the incoming seat's plan must dispose each one (executing in batch N | scheduled with a row
    | refused in writing) before its plan is accepted -- a probe, not prose."*
    (`AMEND-SESSION-PLAN-009` A9-2.) The PROBE half is the `P13-decision-ledger` rung in
    `verify_handoff_probes`; this is the half that puts the list in front of the seat writing
    the plan, since a probe that refuses a plan the seat had no way to write is a trap.

    SAME CONTRACT AS `_write_funnel_health` ABOVE, and deliberately the same shape rather than
    a second convention: overwritten rather than spliced or appended (a stale block is worse
    than none), and a BUNDLE artifact rather than a browser-visible one -- absent from
    `assemble_paste`'s v5 manifest, so the answer-free invariant governing BOOT / RESIDUAL /
    PROBES and the assembled paste is untouched by it.

    TWO FAILURE CLASSES, ANSWERED DIFFERENTLY. An unimportable `decision_coverage` is a broken
    checkout, not a boundary -- nothing is written and the cut continues, which is
    `_write_seat_boots`'s posture for the same class. An unreadable STORE or TRANSPORT is a
    boundary, and there the block is still written carrying the reason: a missing ledger reads
    to the incoming seat as "no open decisions", which is the one answer it must never give
    (DEFECT E-29, degraded never absent).

    HUB-ONLY BY REPO IDENTITY (`_is_hub`), the same scoping and the same predicate as the P11
    acceptance rung. The population is three HUB surfaces -- this repo's ADR corpus, this
    repo's intake funnel, and the operator's machine-level `CLAUDE_PROMPTS_DIR` -- so a ledger
    rendered for any other tree is a category error, not a degraded reading.

    It is also load-bearing rather than tidy, and the measurement is why: resolving the
    population calls `graph_store.ensure`, which CREATES `<repo>/.git/fpg-graph/FPG.db`. In a
    tree with no git history that MATERIALISES a `.git` directory, after which `_tracked_under`
    no longer short-circuits on "not a git repo", runs `git ls-files` there, gets a non-zero and
    raises BundleCollisionError. Six regeneration tests found that before this shipped. A
    surfacing artifact may degrade, may be slow and may say nothing useful -- it may not change
    the tree it is reporting on.

    COST, measured 2026-09-11 and stated because a handoff cut is interactive: ~25s, almost all
    of it P11's existing `carriage_verdicts`, which spawns a `git cat-file` per carrier token
    across ~96 transport files. The cut already pays that at assemble time for leg 2; this adds
    a second pass of it. Reducing it means memoizing `_resolves_on_main`, which is P11's own
    surface and outside [#692]'s footprint.
    """
    if not _is_hub(Path(repo_root)):
        return None
    try:
        import decision_coverage as _dc  # noqa: PLC0415 -- deferred sibling import, the idiom
    except Exception as exc:             # noqa: BLE001 -- an unimportable organ never kills a cut
        # NOT just ImportError. The chain reaches `file_purpose_graph` and `validate_backlog`,
        # and a tree whose `scripts/` shadows either raises something else entirely (measured:
        # NameError, from a fixture stub). Whatever it raises, the answer is the same -- there
        # are no constants to render a block with, so nothing is written and the cut goes on.
        print(f"gen_handoff: DECISION LEDGER skipped -- {exc!r}", file=sys.stderr)
        return None
    try:
        text = _dc.render_ledger(_dc.live_decisions(repo_root))
    except Exception as exc:             # noqa: BLE001 -- a surfacing artifact never refuses a cut
        print(f"gen_handoff: DECISION LEDGER degraded -- {exc!r}", file=sys.stderr)
        text = _dc.render_ledger_unavailable(f"{type(exc).__name__}: {exc}")
    out = bundle_dir / _dc.LEDGER_FILE
    out.write_text(text, encoding="utf-8", newline="\n")
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


def _assembler_argv(bundle_dir: Path) -> list[str]:
    """The child assembler's command line. Pure, so a test can read the real argv.

    NO COLD-PASS FLAG, and its absence is the design. An earlier cut passed
    `--in-generation` here to tell the assembler its residual was a fresh render. Terra,
    2026-09-09: a flag on a public CLI is a bypass anyone can type, so the gate could be
    defeated by `assemble_paste.py <filled-bundle> --in-generation`. The assembler now DERIVES
    that state from the residual itself (`_residual_is_an_untouched_render`), which cannot be
    asserted from outside — and is tighter besides, since a partially filled residual is judged
    rather than exempt.
    """
    return [sys.executable, str(_SCRIPTS / "assemble_paste.py"), str(bundle_dir)]


def _run_assembler(bundle_dir: Path) -> int:
    """Spawn `scripts/assemble_paste.py` for `bundle_dir`; return the child's exit code.

    Isolated as a named function for the reason `_resolves_on_main` is: it is the seam a test
    has to stand in for. Monkeypatching `subprocess.run` instead would reach the stdlib module
    every other caller in this process shares, and `_SCRIPTS` is not the seam either -- it is
    also the sibling-import path (five `sys.path.insert` sites above), so repointing it shadows
    the real `assemble_paste` module for anything that imports it later in the same process.

    The cold pass carries no marker: the assembler works out for itself whether the residual is
    still an untouched render. See `_assembler_argv` for why that is derived rather than told.
    """
    return subprocess.run(_assembler_argv(bundle_dir), check=False).returncode


def generate(repo_root: Path = _REPO_ROOT, *, mode: str = "architect", slug: str | None = None,
             repo: str | None = None, date: str | None = None, force_filled: bool | None = None,
             assemble: bool = True, bundle_root: Path | None = None,
             epic_slug: str | None = None, allow_suffix: bool = False,
             boot_turns: "int | None" = None, boot_dispatch: "str | None" = None,
             dry_cut: bool = False, memory_path: "Path | None" = None,
             sessions_root: "Path | None" = None,
             transport: "Path | None" = None) -> GenResult:
    """Emit a v5 bundle from committed repo state. Returns the bundle dir + the JOURNAL draft.

    lane-boot-contract (WAVE5B-N2 row 12): the v5 boot header is a probe-checked DATA block and
    a short PROSE block, and every v5 cut writes `HANDOFF_RECEIPT.json` carrying the paste's
    measured bytes and a `boot_cost` field — `boot_turns` / `boot_dispatch` are the operator's
    tally for the seat this cut supersedes (see `boot_cost`); without them it is `unmeasured`.

    `dry_cut=True` renders and assembles a real bundle OUTSIDE the repository (it refuses a
    `bundle_root` inside it, with ValueError) and skips gates 1-2 — the batch boundary and
    boundary hygiene — because those guard what a COMMITTED bundle claims, and a dry cut can
    never be committed: `docs/handoffs/` is out of its reach. A lane or integration worktree is
    a linked worktree, so gate 2 (`assert_boundary_hygiene`) refuses there by construction —
    this is how that path is exercised without that refusal.

    GATE 3 (the preflight rows) RUNS AT A DRY CUT TOO (ADR-129 item 1/L1). It is a property of
    the window the bundle WOULD seal, not of the commit boundary gates 1-2 guard, so skipping
    it at a dry cut would make `--dry-cut` time rendering alone rather than the cut path it is
    meant to prove end to end. `memory_path` / `sessions_root` (both default `None`, resolved
    live exactly as before) let a caller pin the two LIVE-STATE rows (`memory_within_cap`,
    `worktree_owners`) to a fixture for a deterministic dry cut (AMEND-HANDOFF-REDESIGN-
    BUILD-2026-10-01 item 2 / R47) — every other caller, including the CLI, is unaffected.

    It is how a change to the boot is proven end to end without cutting a handoff. The receipt
    says `"cut": "dry"`.

    `transport` (ADR-129 item 14/L9): the refusal log (`_append_refusal_log` /
    `_append_cut_log` / `_refusal_count_since_previous_cut`) is EXPLICIT-opt-in, not resolved
    live via `transport_root()` inside this function -- `None` (the default, every caller
    that does not pass it, including every test that does not fixture it) makes every one of
    those three a no-op / `None`-valued read, never a live write to the operator's real
    transport as a side effect of a refused test fixture. The CLI `main()` is the one caller
    that passes the live `transport_root()` through.

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
    if dry_cut:
        why = _dry_cut_refusal(bundle_root, repo_root)
        if why is not None:
            raise DryCutTargetError(f"a dry cut writes outside every git work tree (or into an "
                                    f"ignored path); {why} — pass a directory under your job's tmp")
    # RM-8 / R5: refuse a target that already holds git-tracked files (or, with the
    # explicit opt-in, divert to a fresh sibling). `exist_ok=True` survives ONLY on the
    # path this guard has cleared — the in-flight, not-yet-committed bundle — so the
    # documented `--filled` re-render and the FILL-IN splice keep working.
    bundle_dir = _resolve_bundle_dir(repo_root, bundle_root, slug, allow_suffix)
    # The two boundary invariants, AFTER target resolution and BEFORE anything is created:
    # a refused cut leaves no half-written directory behind (which would itself be the
    # untracked in-flight target RM-8 sanctions). RM-8 resolves first because its complaint
    # is the more specific one — it names the colliding directory.
    if not dry_cut:     # a dry cut cannot be committed, so it seals no commit-boundary claim
        assert_batch_boundary(repo_root)
        assert_boundary_hygiene(repo_root)
    # Gate 3, the TEN preflight rows -- runs at EVERY cut, dry or real (ADR-129 item 1/L1): it
    # is a property of the window the bundle would seal, not of the commit boundary gates 1-2
    # guard. Still before mkdir -- a refused cut writes nothing. [#1123]: name the bundle THIS
    # call is about to (re-)write, so row 1 can tell a `--filled` re-render's own known
    # BD-manifest circularity from an unrelated hard-fail. `memory_path` / `sessions_root` pin
    # the two live-state rows for a deterministic dry cut (AMEND-HANDOFF-REDESIGN-
    # BUILD-2026-10-01 item 2); both default `None`, the prior live-resolution behaviour.
    try:
        preflight_result = assert_preflight(
            repo_root, today=date, repo_name=repo, bundle_dir=bundle_dir,
            force_filled=bool(force_filled), memory_path=memory_path,
            sessions_root=sessions_root)
    except PreflightError as exc:
        # item 14/L9: a REAL cut's refusal is logged to the transport-side refusal log (never
        # the repo -- see _append_refusal_log). A dry cut is a proof of the cut path, not an
        # operator's own retry loop, so it is not counted (N3's own scope note, above).
        if not dry_cut:
            _append_refusal_log(transport, repo_root=repo_root, reason=str(exc))
        raise
    bundle_dir.mkdir(parents=True, exist_ok=True)
    # [#473] B — THE FIX, and it is this one line. `_resolve_bundle_dir` may DIVERT the write
    # to a `-<n>` sibling under `--allow-suffix`, but every render token below was built from
    # the REQUESTED slug, so a diverted bundle sealed with all of its internal self-references
    # — the HANDOFF_BOOT `Slug` field, the PROBES P0c/P3/P8 locators, PASTE_THIS's embedded
    # PROBES self-references — pointing at the SIBLING directory. Rebinding the slug to the
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
        _write_decision_ledger(bundle_dir, repo_root)         # A9-2 — same placement, same reason
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
    elif mode == "architect":
        # lane-handoff-min (Part A) Done-when 4: this is a RE-render over an already-written
        # supplement (the documented `--filled` reflow). Refuse before anything else renders
        # when the operator's fill omits a fixed slot -- see `assert_supplement_fixed_slots`.
        assert_supplement_fixed_slots(bundle_dir / "SUPPLEMENT.md")

    # R2: the generated attribution frame for RESIDUAL §1. Computed from COMMITTED state (the
    # register + the window's diff) and carrying no answer value — see `standing_vs_new`.
    tokens["STANDING_VS_NEW"] = standing_vs_new(repo_root)
    # R5: the forms card's dispatch line, RENDERED from Ch8's dispatch table rather than held as
    # a second copy — the whole point of STANDING_RULINGS §V.
    tokens["DISPATCH_FORM"] = dispatch_form(repo_root)
    # lane-boot-contract: the probe-checked DATA block of the boot header. lane-handoff-min
    # (Part A) adds the live STATE rows here — computed ONCE (`transport` resolved once, CI
    # polled once) and reused for the manifest's `row_freshness` field below, so the cut does
    # not re-poll CI or re-glob the transport a second time for the same generation.
    #
    # DELIBERATELY NOT the `transport` PARAMETER (ADR-129 item 14/L9 bug, caught and fixed
    # same-session, terra-style self-catch): a first draft reused that parameter here, which
    # made a caller-supplied fixture ALSO become the refusal log's target -- and, since every
    # pre-existing caller leaves `transport=None` by default, a NAIVE "default None means
    # resolve live" rule for the refusal log would make every ordinary `generate()` test run
    # silently WRITE a `CUT` line to the operator's real transport (caught here: 28 real lines
    # landed in this machine's actual `H:\My Drive\CLAUDE PROMPT DIR\logs\HANDOFF-REFUSALS.jsonl`
    # during this lane's own test runs before this split existed; cleaned up). Reads of state
    # rows are harmless by default; a refusal-log WRITE is not, so the two are kept on separate
    # variables: `_state_transport` always resolves live (state_rows reading the transport is
    # the pre-existing, unrelated-to-this-ADR behaviour) while the `transport` PARAMETER stays
    # exactly what the caller passed -- `None` leaves the refusal log INERT (see
    # `_refusal_log_path`), and only the CLI `main()` passes the live one through on purpose.
    _state_transport = transport_root()
    live_state_rows = _hstate().state_rows(repo_root, _state_transport)
    tokens["BOOT_DATA"] = boot_data_block(
        boot_data_rows(slug, mode, tokens["CHAT_TITLE"], spec_version(repo_root),
                       state_rows=live_state_rows))

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
    # A9-2: the DECISION LEDGER, beside the health block and AFTER the seal gate for the same
    # reason it is -- a refused or failed cut must not leave a bundle carrying a FRESH ledger
    # beside STALE renders. `functional` mode never reaches here, which is HANDOFF_PROCESS
    # §16's one-file scoping and not a judgement about that mode's need for the list.
    _write_decision_ledger(bundle_dir, repo_root)
    # INBOX-dev-knowledge-2026-09-08-038 / AMEND-BATCH-V-001 §1: the five SEAT-BOOT pastes, so
    # the next incoming seat POINTS at a rendered boot instead of composing one. AFTER the seal
    # gate for the same reason the health block is (a refused cut leaves no fresh artifact beside
    # stale renders), and before `assemble_paste` so the forms card can carry them.
    _write_seat_boots(bundle_dir, repo_root, slug, date)

    hints = collect_hints(repo_root)
    draft = journal_draft(slug, date, state, hints)

    # lane-boot-contract: the receipt's boot-cost field. The transport is read only when a
    # tally names a dispatch to witness — an untallied cut never touches it.
    cost = boot_cost(boot_turns, boot_dispatch,
                     transport_root() if boot_dispatch is not None else None)
    code: "int | None" = None
    if assemble:
        # THE COLD PASS. RESIDUAL.md was rendered a few lines above, so leg 2's second operand
        # does not exist yet — the assembler recognises that from the residual itself and
        # defers (loudly) to the post-fill re-run. Any non-zero the child still returns — a
        # missing required source, a broken template — refuses the cut below.
        code = _run_assembler(bundle_dir)
    # Written AFTER the assembler, refused or not, so the paste bytes it records are the ones
    # the gate measured — and a refused cut still leaves the receipt that says it was refused.
    # lane-handoff-min (Part A): the manifest's file census runs LAST, over every file this
    # generation wrote (including PASTE_THIS.md, if assembled), so a refused assembly still
    # gets an honest manifest of whatever the bundle actually holds.
    _, source_sha = _git_status(repo_root, "rev-parse", "HEAD")
    manifest = bundle_manifest(bundle_dir, source_sha=source_sha or None,
                               state_rows=live_state_rows)
    _write_receipt(bundle_dir, slug=slug, mode=mode, date=date,
                   cut="dry" if dry_cut else "real", cost=cost,
                   paste=_paste_record(bundle_dir, code), manifest=manifest,
                   repo_root=repo_root, transport=transport,
                   # `preflight_result or ()`: several tests replace `assert_preflight` with a
                   # bare side-effect stub (e.g. `_preflight_ship_gate_only` in
                   # test_gen_handoff.py) that returns `None` on success -- never iterated
                   # before this repair, now a crash if assumed to always be a list.
                   preflight_notes=[r.render() for r in (preflight_result or ())
                                    if r.name in PREFLIGHT_NON_BLOCKING_ROWS])
    if assemble:
        if code != 0:
            # The bundle is deliberately LEFT ON DISK. Every other refusal in this function
            # fires before `mkdir` and leaves nothing behind; this one fires after the render,
            # and that asymmetry is the point of an assemble-time gate — leg 2's whole reason
            # for gating here is that the bundle is still repairable. Deleting it would take
            # away the thing the operator has to fix.
            raise AssemblyRefusedError(
                f"assembly REFUSED for {bundle_dir} (assemble_paste.py exit {code}); the "
                "diagnostic above is the assembler's own. No PASTE_THIS.md was written, so "
                "there is nothing to hand to a browser. Repair what it names — for the P11 "
                "leg-2 gate that means naming each `carried-by: OPEN` decision file in this "
                "bundle's RESIDUAL.md — then re-run the assembler on the same directory.")
    # item 14/L9: a REAL cut that reaches here succeeded past every refusal, so it resets the
    # refusal count the NEXT cut attempt's receipt will read (`_refusal_count_since_previous_cut`
    # counts REFUSAL entries after the last CUT entry).
    if not dry_cut:
        _append_cut_log(transport, repo_root=repo_root, slug=slug)
    return GenResult(bundle_dir=bundle_dir, journal_draft=draft, filled=filled)


# ================================================ the boot's reading path + the dispatch map ([#1443])
#
# `protocols/HANDOFF_BOOT.md` names five things a fresh seat reads (INDEX, the current lessons,
# the seat exam, the dispatch exam, the dispatch map). `--reading-path` resolves them against the
# transport and `--dispatch-map` generates the fifth, from `dispatch.py --help`,
# `ecosystem/substrate-registry.yaml` and `ecosystem/harness.yaml`. They are flags of this script
# and not a new organ: this CLI already reads the transport and the registries at cut time.
#
# Library-first: stdlib (`ast`, `os`, `re`, `subprocess`) + PyYAML (declared) + click; the
# resolver is `handoff_state.resolve_reading_path`, itself a guard over `_live_transport_docs`.
#
# PROVEN IS NOT A FLAG. A substrate's `live:` boolean is a declaration (the registry says so
# itself); the 2026-10-09 onboarding showed a seat taking it for a run. A substrate is PROVEN
# here only when (a) its start verb is in the live `dispatch.py --help` and (b) at least one
# evidence token cited in `DISPATCH_EVIDENCE` resolves in the tracked tree -- today only
# `test:<file>::<function>`, checked offline with `ast`. Every other state is DECLARED, with the
# reason printed. A `run:<id>` kind is deliberately absent: nothing offline can check a run id.
# PROVEN means a cited test exercises the start verb; it is not production readiness.

DISPATCH_MAP_REL = "to-browser/MAP-DISPATCH.md"
#: substrate -> the `dispatch.py` verb that STARTS a lane there. Cloud and interactive have none:
#: the hub spawns neither (the registry's verbs are operator-side names).
SUBSTRATE_START = {"local": "launch", "codespace": "codespace-exec"}
#: substrate -> evidence tokens, each `test:<repo-relative file>::<function>`. Cited by hand, and
#: re-checked on every generation: a token naming a test that no longer exists drops the
#: substrate to DECLARED, so a rename cannot leave a stale PROVEN behind.
DISPATCH_EVIDENCE = {
    "local": ("test:tests/test_dispatch_launch.py::"
              "test_a_free_slug_spawns_exactly_once_with_n_slug_in_its_argv",),
    "codespace": ("test:tests/test_dispatch_codespace.py::"
                  "test_codespace_exec_happy_path_returns_the_receipt",),
}
_EVIDENCE_RE = re.compile(r"test:([A-Za-z0-9_./-]+\.py)::([A-Za-z_]\w*)")
_MAP_REFRESH = "uv run --locked python scripts/gen_handoff.py --dispatch-map --write"


def _ascii(text: str) -> str:
    return text.encode("ascii", "replace").decode("ascii")


def _run_dispatch_help(verb: "str | None" = None) -> str:
    """`dispatch.py [<verb>] --help` as text. The seam tests replace; it reads, never launches."""
    argv = [sys.executable, str(_SCRIPTS / "dispatch.py"), *([verb] if verb else []), "--help"]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "NO_COLOR": "1"}
    done = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, check=False, timeout=120)
    return done.stdout


def _help_verbs(top_help: str) -> "list[str]":
    """The verb names under `Commands:` of a click `--help`, in the order it prints them."""
    verbs: "list[str]" = []
    in_commands = False
    for line in top_help.splitlines():
        if line.strip() == "Commands:":
            in_commands = True
            continue
        if in_commands:
            m = re.match(r"^  ([a-z][a-z0-9-]*)(?:\s|$)", line)
            if m:
                verbs.append(m.group(1))
            elif line.strip():
                break
    return verbs


def _usage_line(verb_help: str) -> str:
    for line in verb_help.splitlines():
        if line.startswith("Usage:"):
            return _ascii(line.strip())
    return "Usage: (none printed)"


def evidence_resolves(token: str, repo_root: "Path | str") -> bool:
    """True iff `token` is `test:<file>::<function>` and that function is defined in that tracked
    file under `repo_root`. Offline and fail-closed: any other shape, a path outside the tree, an
    unreadable or unparseable file, or a missing function is False."""
    import ast  # noqa: PLC0415 (lazy: only the map reads it)
    m = _EVIDENCE_RE.fullmatch(token or "")
    if m is None:
        return False
    rel, func = m.groups()
    root = Path(repo_root).resolve()
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return False
    if not path.is_file():
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return False
    return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func
               for n in ast.walk(tree))


def dispatch_map_text(repo_root: "Path | str | None" = None, *, help_runner=None,
                      registry: "dict | None" = None, harness: "dict | None" = None,
                      evidence: "dict | None" = None) -> str:
    """The dispatch map: flat `key: value` text, one block per registry substrate in registry
    order, ASCII, LF, deterministic (no date, no sha: a re-render with unchanged inputs is a
    byte-identical file). The five keyword seams make the state rule testable without a launch."""
    import yaml  # noqa: PLC0415 (lazy: PyYAML is declared; only the map reads it)
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    runner = help_runner if help_runner is not None else _run_dispatch_help
    if registry is None:
        registry = yaml.safe_load((root / "ecosystem" / "substrate-registry.yaml")
                                  .read_text(encoding="utf-8")) or {}
    if harness is None:
        harness = yaml.safe_load((root / "ecosystem" / "harness.yaml")
                                 .read_text(encoding="utf-8")) or {}
    cited = DISPATCH_EVIDENCE if evidence is None else evidence
    verbs = _help_verbs(runner(None))
    organs = [str(o.get("id", "")) for m in (harness.get("moments") or [])
              if m.get("name") == "pre-launch" for o in (m.get("organs") or [])]
    out = [
        "by: scripts/gen_handoff.py --dispatch-map (generated; no seat writes this file by hand)",
        "",
        "# DISPATCH MAP -- generated, never hand-edited",
        "",
        f"regenerate: {_MAP_REFRESH}",
        "inputs: `dispatch.py --help`, ecosystem/substrate-registry.yaml, ecosystem/harness.yaml",
        "legend: PROVEN = the substrate's start verb is in `dispatch.py --help` AND a cited test "
        "(`test:<file>::<function>`) resolves in the tracked tree. DECLARED = anything else; a "
        "`live:` flag alone is DECLARED. PROVEN means a test exercises the start verb, not that "
        "the substrate is production-ready.",
        f"dispatch.py verbs: {', '.join(verbs) if verbs else '(none read)'}",
        f"pre-launch organs: {', '.join(organs) if organs else '(none declared)'}",
    ]
    for name, spec in (registry.get("substrates") or {}).items():
        spec = spec or {}
        start = SUBSTRATE_START.get(name)
        tokens = tuple(cited.get(name, ()))
        resolved = [t for t in tokens if evidence_resolves(t, root)]
        reason = ""
        if start is None:
            reason = "no start verb in dispatch.py for this substrate; only the registry's live flag backs it"
        elif start not in verbs:
            reason = f"start verb `{start}` is not in dispatch.py --help"
        elif not tokens:
            reason = "no evidence cited"
        elif not resolved:
            reason = "no cited test resolves in the tracked tree"
        proven = not reason
        out += [
            "",
            f"substrate: {name}",
            f"family: {spec.get('family', '')}",
            f"live: {'true' if spec.get('live') else 'false'}",
            f"operator verbs: {', '.join(str(v) for v in (spec.get('verbs') or [])) or 'none'}",
            f"start: {start or 'none'}",
            f"usage: {_usage_line(runner(start)) if start and start in verbs else 'none'}",
            f"state: {'PROVEN' if proven else 'DECLARED'}",
            f"evidence: {resolved[0] if proven else 'none'}",
        ]
        if not proven:
            out.append(f"reason: {reason}")
    return _ascii("\n".join(out)) + "\n"


def write_dispatch_map(transport: "Path | None", text: str) -> Path:
    """Write the map to `<transport>/to-browser/MAP-DISPATCH.md` through a temp file and
    `os.replace`. An unresolved transport, or one with no `to-browser/`, raises ValueError: a
    folder is never created to make a write succeed (the E-29 posture `transport_root` states)."""
    if transport is None:
        raise ValueError("the transport is unresolved (CLAUDE_PROMPTS_DIR); refusing to write the map")
    dest = Path(transport) / DISPATCH_MAP_REL
    if not dest.parent.is_dir():
        raise ValueError(f"{dest.parent} does not exist; refusing to create it")
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, dest)
    return dest


def reading_path_report(transport: "Path | None", repo_root: "Path | str | None" = None,
                        *, help_runner=None) -> "tuple[list[str], int]":
    """`(lines, exit_code)` for `--reading-path`: each of the boot's five items, its status and
    what it resolved to. Exit 1 on any status but OK. An existing map file whose text differs
    from a fresh generation is STALE -- a PROVEN/DECLARED claim must not outlive the code it was
    generated from -- and the line names the one command that refreshes it."""
    import handoff_state as _hs  # noqa: PLC0415 (sibling; deferred like every sibling import here)
    results = _hs.resolve_reading_path(transport)
    lines: "list[str]" = []
    failed = False
    for i, r in enumerate(results, 1):
        status = r.status
        shown = r.boot_anchor
        if r.path is not None:
            try:
                shown = r.path.relative_to(Path(transport)).as_posix()
            except ValueError:
                shown = r.path.name
            if r.section:
                shown += f" (section: {r.section})"
        if r.key == "map" and status == "OK":
            fresh = dispatch_map_text(repo_root, help_runner=help_runner)
            if r.path.read_text(encoding="utf-8") != fresh:
                status = "STALE"
                shown += f" -- regenerate: {_MAP_REFRESH}"
        elif r.key == "map" and status == "MISSING":
            shown += f" -- generate: {_MAP_REFRESH}"
        failed = failed or status != "OK"
        lines.append(f"  {i} {r.key:<13} {status:<10} {shown}")
    return lines, 1 if failed else 0


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
@click.option("--preflight-only", is_flag=True, default=False,
              help="print the nine pre-handoff hygiene rows and exit (1 on any FAIL); cut nothing")
@click.option("--trial-cut", "trial_cut", is_flag=True, default=False,
              help="batch-close stage (item 12/L7): like --preflight-only, but excludes the "
                   "two cut-day rows (ledger_refreshed, ratification_present), which are "
                   "false-red by construction outside a real cut window; exit 1 on any "
                   "remaining FAIL, which refuses the close")
@click.option("--dry-cut", "dry_cut_dir", default=None,
              type=click.Path(file_okay=False, path_type=Path),
              help="render + assemble a real bundle into DIR (must be OUTSIDE the repo), skipping "
                   "the cut-boundary gates; it is never a handoff and can never be committed")
@click.option("--boot-turns", type=int, default=None,
              help="the operator's tally: turns the superseded bundle's seat took to its first "
                   "correct dispatch (recorded in HANDOFF_RECEIPT.json boot_cost)")
@click.option("--boot-dispatch", default=None,
              help="that first correct dispatch, as a transport path `to-cc/<order>.md`")
@click.option("--reading-path", "reading_path", is_flag=True, default=False,
              help="resolve the five items of the boot's reading path (INDEX, SEAT-LESSONS, the "
                   "seat exam, the dispatch exam, the dispatch map) against the transport and "
                   "print each with its status; exit 1 on any item that is not OK; cut nothing")
@click.option("--dispatch-map", "dispatch_map", is_flag=True, default=False,
              help="print the dispatch map generated from dispatch.py --help, the substrate "
                   "registry and the harness; with --write, write it to "
                   "to-browser/MAP-DISPATCH.md on the transport; cut nothing")
@click.option("--write", "write_map", is_flag=True, default=False,
              help="with --dispatch-map: write the map to the transport instead of printing it")
def main(mode: str, epic_slug: str | None, slug: str | None, repo: str | None, date: str | None,
         force_filled: bool | None, assemble: bool, allow_suffix: bool, emit_journal: bool,
         preflight_only: bool, trial_cut: bool = False, dry_cut_dir: "Path | None" = None,
         boot_turns: "int | None" = None, boot_dispatch: "str | None" = None,
         reading_path: bool = False, dispatch_map: bool = False, write_map: bool = False) -> None:
    """Generate a v5 handoff bundle from committed repo state."""
    if write_map and not dispatch_map:
        raise click.UsageError("--write belongs to --dispatch-map")
    if reading_path:
        transport = transport_root()
        if transport is None:
            click.echo("[error] the transport is unresolved (CLAUDE_PROMPTS_DIR); every "
                       "reading-path item reads MISSING", err=True)
        lines, code = reading_path_report(transport, _REPO_ROOT)
        click.echo("reading path -- the boot's five items (any status but OK exits 1):")
        for line in lines:
            click.echo(line)
        raise SystemExit(1 if transport is None else code)
    if dispatch_map:
        text = dispatch_map_text(_REPO_ROOT)
        if not write_map:
            click.echo(text, nl=False)
            raise SystemExit(0)
        try:
            dest = write_dispatch_map(transport_root(), text)
        except ValueError as exc:
            click.echo(f"[error] {exc}", err=True)
            raise SystemExit(1) from exc
        click.echo(f"Written: {dest} ({len(text.encode('utf-8'))} bytes)")
        raise SystemExit(0)
    if preflight_only or trial_cut:
        rows = preflight_rows(_REPO_ROOT, today=date, trial_cut=trial_cut)
        label = "batch-close trial cut" if trial_cut else "preflight"
        refuses = "the close" if trial_cut else "the cut"
        click.echo(f"{label} -- pre-handoff hygiene rows (any FAIL refuses {refuses}):")
        for row in rows:
            click.echo("  " + row.render())
        failed = [r for r in rows if r.failed]
        raise SystemExit(1 if failed else 0)
    state = collect_state(_REPO_ROOT)
    if state.dirty:
        click.echo("[warn] working tree is DIRTY — a v5 bundle is cut from COMMITTED state; "
                   "commit first or the probes bind to un-committed drift.", err=True)
    try:
        res = generate(_REPO_ROOT, mode=mode, slug=slug, repo=repo, date=date,
                       force_filled=force_filled, assemble=assemble, epic_slug=epic_slug,
                       allow_suffix=allow_suffix, boot_turns=boot_turns,
                       boot_dispatch=boot_dispatch, bundle_root=dry_cut_dir,
                       dry_cut=dry_cut_dir is not None, transport=transport_root())
    except (BundleCollisionError, OpenBatchError, BoundaryHygieneError, PreflightError,
            AssemblyRefusedError, DryCutTargetError) as exc:
        # A REFUSAL, not a crash — one diagnostic line, non-zero exit. RM-8 (target collision)
        # and the two boundary invariants share this exit: each names what it found, and none
        # of them is recoverable by re-running unchanged.
        # AssemblyRefusedError is the one member that differs on both counts, and the
        # difference is stated rather than left for a reader to discover: it fires AFTER the
        # bundle is written (its subject does not exist before the render), and it IS
        # recoverable by re-running — repair what the assembler named, then re-run it. What it
        # shares is the only thing this handler cares about: no `Generated bundle`, exit 1.
        raise SystemExit(f"[error] {exc}") from exc
    click.echo(f"Generated bundle: {res.bundle_dir}  (fill-state: {'FILLED' if res.filled else 'cold'})")
    if emit_journal:
        click.echo("\n----- JOURNAL generation-entry DRAFT (prepend to JOURNAL.md at wrap; "
                   "NOT auto-appended, NOT in the bundle) -----")
        click.echo(res.journal_draft)


if __name__ == "__main__":
    main()
