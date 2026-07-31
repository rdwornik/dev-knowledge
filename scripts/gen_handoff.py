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

The cold<->FILLED framing flip is deterministic: the fill-state is read via
assemble_paste._extract_answers (ONE shared definition), so the four framing sites
and the assembler's fold decision can never disagree.

Layer-2 / read-only w.r.t. tracked spine files: writes ONLY <bundle>/*; never edits
JOURNAL.md / BACKLOG.md (the operator prepends the printed draft at wrap).
"""
from __future__ import annotations

import datetime as _dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import click

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
    rather than inventing prose."""
    vision = repo_root / "VISION.md"
    if not vision.exists():
        return "(VISION.md `## Vision` section not found — fix VISION.md before using this boot)"
    text = vision.read_text(encoding="utf-8")
    m = re.search(r"^## Vision\s*\n(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE)
    if not m:
        return "(VISION.md `## Vision` section not found — fix VISION.md before using this boot)"
    return m.group(1).strip()


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
    bundle_dir.mkdir(parents=True, exist_ok=True)

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

    _render("HANDOFF_BOOT.md.tmpl", tokens, bundle_dir, "HANDOFF_BOOT.md")
    _render("RESIDUAL.md.tmpl", tokens, bundle_dir, "RESIDUAL.md")
    _render("PROBES.md.tmpl", tokens, bundle_dir, "PROBES.md")

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
    except BundleCollisionError as exc:
        # RM-8: a REFUSAL, not a crash — one diagnostic line, non-zero exit, nothing written.
        raise SystemExit(f"[error] {exc}") from exc
    click.echo(f"Generated bundle: {res.bundle_dir}  (fill-state: {'FILLED' if res.filled else 'cold'})")
    if emit_journal:
        click.echo("\n----- JOURNAL generation-entry DRAFT (prepend to JOURNAL.md at wrap; "
                   "NOT auto-appended, NOT in the bundle) -----")
        click.echo(res.journal_draft)


if __name__ == "__main__":
    main()
