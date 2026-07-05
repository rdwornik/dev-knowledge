#!/usr/bin/env python3
"""gen_handoff.py — the v5 handoff bundle generator (#164 RF-2 / RF-1 option b).

Assembles a valid v5 bundle (HANDOFF_BOOT + RESIDUAL + PROBES + SUPPLEMENT, then
PASTE_THIS via scripts/assemble_paste.py) from COMMITTED repo state, replacing the
hand-copy that let the handoff's prose-held properties erode. Two structural invariants:

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


# --- committed state + generation hints -------------------------------------

@dataclass(frozen=True)
class _State:
    """The STRUCTURAL surface that may enter the bundle. `branch` is the only field the render
    functions receive (a §5-sanctioned "which branch" pointer). `dirty` gates generation
    (a bundle is cut from COMMITTED state)."""
    branch: str
    dirty: bool


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped, or "" on any error."""
    try:
        out = subprocess.run(["git", *args], cwd=str(repo_root), capture_output=True,
                             text=True, timeout=30)
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def collect_state(repo_root: Path) -> _State:
    branch = _git(repo_root, "branch", "--show-current") or "(detached)"
    dirty = bool(_git(repo_root, "status", "--porcelain"))
    return _State(branch=branch, dirty=dirty)


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


def detect_fill_state(bundle_dir: Path) -> bool:
    """True => FILLED framing, False => cold. Reuses assemble_paste._extract_answers so the
    framing flip matches EXACTLY what the assembler folds (one fill-state definition)."""
    sup = bundle_dir / "SUPPLEMENT.md"
    if not sup.exists():
        return False
    sys.path.insert(0, str(_SCRIPTS))
    from assemble_paste import _extract_answers  # noqa: PLC0415
    return _extract_answers(sup.read_text(encoding="utf-8")) is not None


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
    framing. (Verified by the recurring dogfood: no rendered row carries an answer-hint.)"""
    return {
        "MODE": mode,
        "SLUG": slug,
        "REPO": repo,
        "DATE": date,
        "BRANCH": state.branch,
        "MODE_SCOPE": _MODE[mode]["scope"],
        "MODE_POSTURE": _MODE[mode]["posture"],
        "SUPPLEMENT_BANNER": _framing("SUPPLEMENT_BANNER", filled),
        "P1_GATE_NOTE": _framing("P1_GATE_NOTE", filled),
        "PASTE_STEP6": _framing("PASTE_STEP6", filled),
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
             epic_slug: str | None = None) -> GenResult:
    """Emit a v5 bundle from committed repo state. Returns the bundle dir + the JOURNAL draft.

    force_filled overrides the auto-detected fill-state (RF-2's `--filled`). bundle_root defaults
    to <repo_root>/docs/handoffs (overridable for tests). SUPPLEMENT.md is written only if absent
    (an operator-filled supplement is never clobbered).

    mode="epic" (§14a, ADR-97) emits the epic-lane scope-contract bundle instead:
    EPIC_BOOT.md (root-authored FILL-IN contract scaffold) + PROBES.md (boundary-scoped
    teeth) + EPIC_RETURN.md (§14b closing-report skeleton, write-if-absent — a lane-filled
    return is never clobbered). It reuses this generator's v5 assembly machinery (render /
    FILL-IN splice / structural tokens / the answer-free invariant) but assembles NO
    PASTE_THIS.md: scripts/assemble_paste.py's manifest is v5-shaped (requires RESIDUAL.md);
    the EPIC_BOOT scope-contract is the paste. `epic_slug` names the epic (branch
    `epic/<epic_slug>`, worktree `epic-<epic_slug>`); defaults to the bundle slug.
    """
    if mode not in _MODE:
        raise ValueError(f"mode must be one of {sorted(_MODE)}; got {mode!r}")
    repo = repo or repo_root.name
    date = date or _dt.date.today().isoformat()
    slug = slug or f"{date}-{repo.lstrip('.')}-{mode}"
    bundle_root = bundle_root or (repo_root / "docs" / "handoffs")
    bundle_dir = bundle_root / slug
    bundle_dir.mkdir(parents=True, exist_ok=True)

    state = collect_state(repo_root)
    filled = force_filled if force_filled is not None else detect_fill_state(bundle_dir)
    tokens = _tokens(mode, slug, repo, date, state, filled)

    if mode == "epic":
        eslug = epic_slug or slug
        tokens.update({"EPIC_SLUG": eslug, "EPIC_BRANCH": f"epic/{eslug}"})
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
@click.option("--mode", type=click.Choice(["architect", "execution", "epic"]), default="architect",
              show_default=True)
@click.option("--epic-slug", default=None,
              help="epic mode only: the epic name (branch epic/<slug>, worktree epic-<slug>); "
                   "default the bundle slug")
@click.option("--slug", default=None, help="bundle slug; default <date>-<repo>-<mode>")
@click.option("--repo", default=None, help="repo display name; default the repo dir name")
@click.option("--date", default=None, help="handoff date YYYY-MM-DD; default today")
@click.option("--filled/--cold", "force_filled", default=None,
              help="override the auto-detected supplement fill-state for the four framing sites")
@click.option("--assemble/--no-assemble", default=True, help="run assemble_paste to emit PASTE_THIS.md")
@click.option("--emit-journal/--no-emit-journal", default=True,
              help="print the JOURNAL generation-entry DRAFT to stdout (never writes JOURNAL.md)")
def main(mode: str, epic_slug: str | None, slug: str | None, repo: str | None, date: str | None,
         force_filled: bool | None, assemble: bool, emit_journal: bool) -> None:
    """Generate a v5 handoff bundle from committed repo state."""
    state = collect_state(_REPO_ROOT)
    if state.dirty:
        click.echo("[warn] working tree is DIRTY — a v5 bundle is cut from COMMITTED state; "
                   "commit first or the probes bind to un-committed drift.", err=True)
    res = generate(_REPO_ROOT, mode=mode, slug=slug, repo=repo, date=date, force_filled=force_filled,
                   assemble=assemble, epic_slug=epic_slug)
    click.echo(f"Generated bundle: {res.bundle_dir}  (fill-state: {'FILLED' if res.filled else 'cold'})")
    if emit_journal:
        click.echo("\n----- JOURNAL generation-entry DRAFT (prepend to JOURNAL.md at wrap; "
                   "NOT auto-appended, NOT in the bundle) -----")
        click.echo(res.journal_draft)


if __name__ == "__main__":
    main()
