"""Tests for the canonical-doc-name registry — `scripts/canonical_docs.py`.

CLOUD-4 v2's answer to `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md`
§1.5 GO-(b): ONE table the ten machine constants read, instead of ten independent literals.

**These tests still do not assert a RENAME — because none happened.** `cdocs.VISION` is
still the string `"VISION.md"`; that identity is deliberately UNCHANGED by the hub's own
relocation ([#614] lane-e-5, 2026-09-01: `git mv VISION.md docs/archive/VISION.md`,
byte-identical). What moved is the file's LOCATION at the hub, not the canonical NAME the
registry holds for it — the two are different questions, and every one of the ten sites
that reads `cdocs.VISION` already tolerates root-absence via the `CANONICAL_RETIRED`
degrade path (built by DC-1 before this lane), so the relocation needed no synchronized
edit to the name. `CANONICAL_RETIRED_LOCATIONS` is the one addition: it maps a retired
name to where its hub copy actually lives, for the two sites (`nopack_sandbox.py`,
`consumer_at_landing.py`) that matched a literal path rather than reading this registry.
What `[#614]` lane-a changed earlier was the doc's **TIER**, not its name: `VISION.md` left
`CANONICAL_MANDATORY` for `CANONICAL_RETIRED`, and `README.md` became MUST at the hub via
`CANONICAL_HUB_MANDATORY`. R2 §1.5 verdicted the *rename* NO-GO as briefed and that verdict
is untouched; the sequenced FLEET-WIDE filename migration (ADR-114 option (C), the other
eight members) is still future work — this lane executed only the hub's own step one.
What these tests assert, as before, is that the ten sites name the SAME
strings — which is exactly what made a tier decision landable in one file.

Three groups:

* **Repoint** — each of the eight hub-local constants IS the registry's value.
* **Carried-copy fallback** — `canonical_freshness_gate` and `session_end_backpressure` are
  byte-copied into consumers by `deploy/carrier_mesh.py` as standalone single files, so they
  import the registry SOFTLY and keep a literal fallback. The fallback is parsed out of the
  source text and compared to the registry, so hub-side drift between the two reds here
  rather than going silent at a consumer.
* **Cross-language** — `.claude/workflows/conformance-hub.js` (R2 seam S11) is a JavaScript
  string list that cannot import Python at all; it is held in agreement by reading the file.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
from datetime import date
from pathlib import Path

import pytest

import canonical_docs as cdocs  # noqa: E402
import canonical_freshness_gate as cfg  # noqa: E402
import gen_handoff as gh  # noqa: E402
import session_end_backpressure as seb  # noqa: E402
import validate_doc_rot as vdr  # noqa: E402
import validate_doc_structure as vds  # noqa: E402
import validate_hermetization as vh  # noqa: E402
from audit_checks.check_canonical_md_visibility import _CANONICAL_ALL, _CANONICAL_MANDATORY
from audit_checks.check_canonical_structure import _CANONICAL_SPINE

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFORMANCE_HUB = ".claude/workflows/conformance-hub.js"


# --- the value is unchanged ----------------------------------------------------------------

def test_the_registry_still_says_vision_md():
    """A tier moved, and (2026-09-01) a hub LOCATION moved -- the canonical NAME did not.
    If this line ever changes it is a ruled decision (ADR-114 option (C)'s nine-repo
    filename migration), not a lane.

    Pinned deliberately alongside the retirement: retiring `VISION.md` from the mandatory
    set, relocating the hub's own copy, and RENAMING the canonical identity are three
    different acts, and this line is what keeps the third from riding in on the first two.
    """
    assert cdocs.VISION == "VISION.md"


def test_the_retired_location_map_names_where_the_hub_copy_actually_lives():
    """[#614] lane-e-5 (2026-09-01): the NAME (`cdocs.VISION`) and the hub's current PATH
    are deliberately two different questions -- see `test_the_registry_still_says_vision_md`.
    This is the registry entry the two literal-path sites (`nopack_sandbox.NEVER_REMOVE`,
    `consumer_at_landing.POOL_ROOT_FILES`) now read instead of a bare "VISION.md" string.
    """
    assert cdocs.CANONICAL_RETIRED_LOCATIONS[cdocs.VISION] == "docs/archive/VISION.md"
    assert set(cdocs.CANONICAL_RETIRED_LOCATIONS) <= set(cdocs.CANONICAL_RETIRED)


@pytest.mark.live_repo
def test_the_relocated_vision_file_exists_where_the_map_says():
    assert (_REPO_ROOT / cdocs.CANONICAL_RETIRED_LOCATIONS[cdocs.VISION]).is_file()


def test_the_mandatory_set_is_the_adr38_a6_seven_minus_the_retired_vision():
    """ADR-38 A6's seven, minus `VISION.md` — retired by ADR-114 (Accepted 2026-08-29,
    AMENDMENT 1), executed here by `[#614]` lane-a.

    The pin is written as an explicit six rather than a derivation so that a name
    re-entering the mandatory set is a visible edit to THIS line. Retirement is a
    subtraction, and the direction is the safety argument: dropping a presence
    requirement cannot RED a member that still carries the file, whereas ADDING one
    (promoting `README.md` here) would RED the six ADR-104 children that have none.
    """
    assert cdocs.CANONICAL_MANDATORY == (
        "ARCHITECTURE.md", "CLAUDE.md", "BACKLOG.md",
        "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md",
    )
    assert cdocs.VISION not in cdocs.CANONICAL_MANDATORY
    assert cdocs.CANONICAL_RETIRED == ("VISION.md",)


def test_readme_is_hub_mandatory_and_deliberately_not_fleet_mandatory():
    """The seam that lets ADR-114 option (C) be SEQUENCED instead of taken in one commit.

    `README.md` is MUST at the hub and unchanged for the fleet. If these two assertions
    ever have to move together, the fleet-wide migration has happened and it is a ruled
    act, not a lane's drive-by.
    """
    assert cdocs.README in cdocs.CANONICAL_HUB_MANDATORY
    assert cdocs.README not in cdocs.CANONICAL_MANDATORY
    assert cdocs.README not in cdocs.ADR38_BASELINE_REQUIRED
    # Nothing fleet-wide may read the hub tuple — that is what makes it hub-scoped.
    assert cdocs.CANONICAL_HUB_MANDATORY == cdocs.CANONICAL_MANDATORY + (cdocs.README,)


def test_retired_and_hub_scoped_names_keep_their_casing_check():
    """A retired name is not a deleted one, and a hub-scoped one is not a fleet one —
    but BOTH stay name-checked. `CANONICAL_ALL` is the casing surface
    (`check_canonical_md_visibility`), and dropping either from it would silently stop
    catching a `Vision.md` / `Readme.md` mis-casing anywhere in the fleet."""
    assert cdocs.VISION in cdocs.CANONICAL_ALL
    assert cdocs.README in cdocs.CANONICAL_ALL
    assert len(cdocs.CANONICAL_ALL) == len(set(cdocs.CANONICAL_ALL)), "no duplicate names"


# --- the eight hard repoints ---------------------------------------------------------------

def test_check_canonical_md_visibility_reads_the_registry():
    assert _CANONICAL_MANDATORY == list(cdocs.CANONICAL_MANDATORY)
    assert _CANONICAL_ALL == list(cdocs.CANONICAL_ALL)
    # The re-export contract is a name, a value AND a type: tests/test_audit.py reads
    # `aud._CANONICAL_MANDATORY` and a tuple would be a silent behaviour change.
    assert isinstance(_CANONICAL_MANDATORY, list)


def test_check_adr38_baseline_reads_the_registry():
    from audit_checks import check_adr38_baseline as mod
    src = Path(mod.__file__).read_text(encoding="utf-8")
    assert "canonical_docs.ADR38_BASELINE_REQUIRED" in src
    assert cdocs.ADR38_BASELINE_REQUIRED == (
        "ARCHITECTURE.md", "BACKLOG.md",
        "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md",
    )
    assert cdocs.CLAUDE not in cdocs.ADR38_BASELINE_REQUIRED, "check_claude_md owns CLAUDE.md"
    # This check runs FLEET-WIDE (its own docstring says so), which is the whole reason the
    # retirement is a subtraction here: `terminal-setup` is a declared ADR-104 member that
    # has never carried a VISION.md, so this line turns a latent divergence GREEN.
    assert cdocs.VISION not in cdocs.ADR38_BASELINE_REQUIRED


def test_check_canonical_structure_keys_come_from_the_registry():
    assert set(_CANONICAL_SPINE) == set(cdocs.CANONICAL_SPINE)
    assert _CANONICAL_SPINE[cdocs.VISION] == [
        "## Vision", "## Scope", "## Values", "## Lifecycle", "## References"]
    # README is deliberately NOT keyed here, and this pins the absence so it stays a
    # decision instead of decaying into an oversight. `release_lint` C7 mirrors this dict
    # into every RELEASED manifest's `doc_shapes` and lints the live constants against
    # v1.1.0 and v1.2.0, so adding the key REDs shipped specs; the sanctioned answer is a
    # manifest version bump, which rides ADR-114 option (C), not this lane.
    assert cdocs.README not in _CANONICAL_SPINE


def test_check_vision_md_uses_the_registry_name():
    """The absence message names the registry's string, not a literal.

    The message changed shape in [#614] (2026-09-01): `VISION` is now in
    `CANONICAL_RETIRED`, so absence reports NOT-APPLICABLE rather than FAIL. The
    assertion this test exists to make is unchanged -- the NAME comes from the registry --
    and it is now evidenced twice over, since the message also names the registry
    constant that decided the verdict.
    """
    from audit_checks.check_vision_md import check_vision_md
    findings = check_vision_md(Path("/nonexistent-repo-root"))
    assert cdocs.VISION in findings[0].evidence
    assert "CANONICAL_RETIRED" in findings[0].evidence


def test_validate_doc_rot_reads_the_registry():
    assert vdr._SECTION_HISTORY_DOCS == list(cdocs.SECTION_HISTORY_DOCS)
    assert vdr._FILE_SIZE_BUDGETS == {cdocs.CLAUDE: 200}


def test_validate_doc_structure_reads_the_registry():
    assert vds._STRUCTURE_DOCS == list(cdocs.STRUCTURE_DOCS)


def test_validate_hermetization_seals_exactly_the_registry_living_docs():
    """ADR-101 §1's Tier-1 `.md` set = the ADR-38 canonical set PLUS `AGENTS.md`
    and `README.md`.

    ADR-115 admits `AGENTS.md` as a Tier-1 file WITHOUT making it a canonical living
    doc: it is portable-instruction payload, not a freshness-stamped governance
    surface. **ADR-114 (Accepted 2026-08-29, AMENDMENT 1) admits `README.md`** on its
    `Amends` line — *"the closed Tier-1 file enum in `SANCTIONED_TIER1_FILES` would
    gain `README.md`"* — for the opposite reason: it IS canonical in substance at the
    hub (it supersedes `VISION.md`), but promoting it into `CANONICAL_MANDATORY` would
    enrol it in `ADR38_BASELINE_REQUIRED` and in every consumer's canonical-set check
    while only 2 of the 8 ADR-104 children carry one. That promotion is the sequenced
    fleet migration, `[#621]`.

    Each divergence is written as an explicit **named** exception, with the ADR that
    admitted it, so that a third one cannot slip in unnamed. Executed by `[#614]`.
    """
    md_members = {n for n in vh.SANCTIONED_TIER1_FILES if n.endswith(".md")}
    assert md_members == set(cdocs.CANONICAL_MANDATORY) | {"AGENTS.md", "README.md"}


def test_gen_handoff_name_and_degrade_string_move_together():
    """R2 §1.4 R2: this generator does not crash on a missing section — it stamps a
    placeholder into a bundle that is immutable the moment it is committed. So the filename
    and its degrade contract live in one place, and this pins that they do."""
    assert gh._vision_extract(Path("/nonexistent-repo-root")) == cdocs.VISION_EXTRACT_MISSING
    assert cdocs.VISION in cdocs.VISION_EXTRACT_MISSING
    assert cdocs.VISION_EXTRACT_HEADING == "## Vision"


def test_gen_handoff_readme_fallback_only_fires_when_vision_is_ABSENT(tmp_path: Path):
    """A PRESENT VISION missing its `## Vision` section must DEGRADE, never fall through.

    The retired-tier fallback exists for a ruled RELOCATION -- VISION gone, README carrying
    the live section. Letting it also fire for a present-but-malformed VISION would
    substitute README's prose for a broken file and hide the breakage, which is precisely
    what the degrade contract exists to prevent. Three cases, one predicate:

      * VISION present and well-formed -> VISION's own section wins, though README has one.
      * VISION present and BROKEN      -> the placeholder, NOT README's section.
      * VISION absent (and retired)    -> README's section.
    """
    assert cdocs.VISION in cdocs.CANONICAL_RETIRED
    readme = tmp_path / cdocs.README
    vision = tmp_path / cdocs.VISION
    readme.write_text("# R\n\n## Vision\n\nreadme-body\n", encoding="utf-8")

    vision.write_text("# V\n\n## Vision\n\nvision-body\n", encoding="utf-8")
    assert gh._vision_extract(tmp_path) == "vision-body"

    vision.write_text("# V\n\nno heading here\n", encoding="utf-8")
    assert gh._vision_extract(tmp_path) == cdocs.VISION_EXTRACT_MISSING

    vision.unlink()
    assert gh._vision_extract(tmp_path) == "readme-body"


@pytest.mark.live_repo
def test_gen_handoff_still_extracts_the_live_vision_section():
    extract = gh._vision_extract(_REPO_ROOT)
    assert extract and extract != cdocs.VISION_EXTRACT_MISSING


# --- the two deploy-carried copies ----------------------------------------------------------

def _literal_fallback(module, symbol: str):
    """Parse the `else:` fallback assignment out of a guarded-import module's source.

    Read from the SOURCE, deliberately: at the hub the guarded import succeeds, so the live
    attribute is the registry's value and comparing it to itself proves nothing. The consumer
    runs the other branch, and the other branch is only visible in the text.
    """
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        for stmt in node.orelse:
            if isinstance(stmt, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == symbol for t in stmt.targets):
                return ast.literal_eval(stmt.value)
    raise AssertionError(f"no literal fallback for {symbol} in {module.__file__}")


def test_freshness_gate_live_value_is_the_registry():
    assert cfg.DEFAULT_FRESHNESS_FILES == list(cdocs.FRESHNESS_FILES)


def test_freshness_gate_consumer_fallback_equals_the_registry():
    assert _literal_fallback(cfg, "DEFAULT_FRESHNESS_FILES") == list(cdocs.FRESHNESS_FILES)


def test_vision_leaves_the_freshness_files_registry_in_both_places():
    """[#621] lane-g-621-c7 closure 2: VISION retired from freshness, in BOTH places.

    Retirement from the mandatory set (ADR-114) does not by itself retire VISION from the
    A1/A2 freshness cadence -- it kept its FRESHNESS_FILES membership through [#614]. This
    closure removes it there too; the equality test above (registry <-> fallback) stays and
    still must pass, so both places move together.
    """
    assert cdocs.VISION not in cdocs.FRESHNESS_FILES
    assert "VISION.md" not in cfg.DEFAULT_FRESHNESS_FILES


def test_backpressure_live_values_are_the_registry():
    assert seb._CANON == tuple(cdocs.BACKPRESSURE_CANON)
    assert seb._JOURNAL == cdocs.JOURNAL
    assert seb._BACKLOG == cdocs.BACKLOG


def test_backpressure_consumer_fallback_equals_the_registry():
    assert _literal_fallback(seb, "_CANON") == tuple(cdocs.BACKPRESSURE_CANON)
    assert _literal_fallback(seb, "_JOURNAL") == cdocs.JOURNAL
    assert _literal_fallback(seb, "_BACKLOG") == cdocs.BACKLOG


def test_the_fallback_parser_would_notice_a_drifted_fallback(tmp_path):
    """Teeth for the parser itself — a helper that silently returns nothing on a shape it does
    not understand would make the two tests above vacuous."""
    mod = tmp_path / "m.py"
    mod.write_text("if x:\n    A = ['live']\nelse:\n    A = ['drifted']\n", encoding="utf-8")

    class _Fake:
        __file__ = str(mod)

    assert _literal_fallback(_Fake, "A") == ["drifted"]
    with pytest.raises(AssertionError):
        _literal_fallback(_Fake, "B")


# --- the cross-language site (R2 seam S11) ---------------------------------------------------

@pytest.mark.live_repo
def test_the_conformance_hub_scan_list_agrees_with_the_registry():
    """Seam S11. A JavaScript string list cannot import Python, so the coupling is a read."""
    text = (_REPO_ROOT / _CONFORMANCE_HUB).read_text(encoding="utf-8")
    m = re.search(r"Scan these files for VERIFIABLE FACTUAL claims[^:]*:\s*(.+?)\.\s+Do NOT scan",
                  text)
    assert m, "the V2 verifier scan-list sentence was not found"
    listed = [tok.strip() for tok in m.group(1).split(",")]
    assert listed == list(cdocs.CONFORMANCE_V2_SCAN)


# --- HY-1: freshness DERIVED from git, for every living doc ---------------------------------
#
# WHY THESE LIVE HERE and not in `tests/test_audit.py`. The batch-E frozen contract
# `LANE-k-11-derived-doc-freshness.md` names a three-file write scope — `scripts/canonical_docs.py`,
# `scripts/audit.py`, `tests/test_canonical_docs.py` — so this file is the lane's ONLY test home.
# That is a scope fact, stated rather than disguised: the registry half (the living-doc predicate)
# is native here, the derivation half is `audit.py`'s and would otherwise sit beside
# `test_audit.py`'s check-#10 block at its line 1027.
#
# WHAT IS BEING TESTED. `docs/audits/2026-08-31-census-doc-freshness-derivation.md` (the tier-(A)
# A4 harvest) measured the problem and drafted the design; these tests are the acceptance
# contract for the build half. A4's own recommendations 3 and 5 are pinned as tests below
# (structural predicates only, no commit-subject matching; fail-closed on a shallow clone),
# because both are places where a shipped classifier silently marks a stale doc fresh.


def _living_git_repo(root: Path) -> Path:
    """A minimal repo whose commits have CONTROLLED author dates, so `%as` is assertable.

    `core.autocrlf false` and byte writes, deliberately: a CRLF round-trip would make every
    `-w`-blind diff non-empty and quietly invert the T1 predicate under test.
    """
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "core.autocrlf", "false")
    _git(root, "config", "user.email", "lane@example.invalid")
    _git(root, "config", "user.name", "lane")
    return root


def _git(repo: Path, *args: str, when: str | None = None) -> str:
    env = dict(os.environ)
    for var in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX"):
        env.pop(var, None)
    if when:
        env["GIT_AUTHOR_DATE"] = f"{when}T12:00:00+00:00"
        env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"]
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    assert p.returncode == 0, f"git {' '.join(args)} -> {p.returncode}: {p.stderr}"
    return p.stdout


def _put(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _commit(repo: Path, subject: str, when: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", subject, when=when)
    return _git(repo, "rev-parse", "HEAD").strip()


_DOC = (
    "---\n"
    "last_reviewed: 2026-01-01\n"
    "reconciled_with: handoff-process@6.3.0\n"
    "---\n"
    "\n"
    "# A living doc\n"
    "\n"
    "> Last updated: 2026-01-01\n"
    "\n"
    "Body prose that a reviewer would have to read.\n"
)


# --- the registry half: WHICH files a derivation may speak about -----------------------------

def test_the_living_doc_predicate_admits_the_a4_census_classes():
    """A4 §2's living set = root canon + protocols + `.claude/` instruction surfaces + deploy +
    plugins + `docs/handoffs/README.md`. Admission is by PREDICATE, never by a frozen roster:
    a 39-name tuple is a count restated in code and goes stale at the next file added
    (CLAUDE.md §4, "never restate a count or roster")."""
    for path in ("README.md", "ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md", "VISION.md",
                 "AGENTS.md", "protocols/PLAYBOOK.md", "protocols/ESSENTIALS.md",
                 "protocols/HANDOFF_PROCESS.md", ".claude/commands/save.md",
                 ".claude/skills/verify/SKILL.md", ".claude/rules/git-discipline.md",
                 "deploy/global-instructions-codex.md", "plugins/tier1-lifecycle/INSTALL.md",
                 cdocs.HANDOFFS_README_PATH):
        assert cdocs.is_living_doc(path), path


def test_the_living_doc_predicate_excludes_every_class_a4_named_underivable():
    """A4 §5: 29 of the 39 STAMPED files cannot be derived at all, in four classes — immutable
    handoff-bundle copies, template placeholders, test fixtures, and an immutable audit. Each
    would be CORRUPTED rather than improved by a derived date, so the predicate must refuse them
    up front; a derivation that reaches an immutable artifact is a CLAUDE.md rule-3 violation the
    gate would be performing on itself.

    The append-only and generated classes go with them for the reason `canonical_freshness_gate`
    already states about JOURNAL/LESSONS/BACKLOG: their freshness is intrinsic to how they are
    written, so an edited-since-review signal fires every session by design."""
    for path in ("docs/handoffs/2026-05-19-cut/02_VISION.md",       # immutable bundle copy
                 "templates/CLAUDE-md-template.md",                  # <YYYY-MM-DD> placeholder
                 "tests/fixtures/repo-with-structural-checks/VISION.md",   # fixture determinism
                 "docs/audits/2026-05-28-universalization-durability-audit.md",  # immutable
                 "docs/decisions/ADR-114-readme.md",
                 "protocols/archive/HANDOFF_PROCESS_v4.4.md",
                 "tasks/614-vision-superseded.md",
                 ".claude/generated/recent-adrs.md",
                 "ecosystem/doc-counts.md",
                 "logs/TOKEN-LOG.md",
                 cdocs.JOURNAL, cdocs.LESSONS, cdocs.BACKLOG,
                 "pyproject.toml"):
        assert not cdocs.is_living_doc(path), path


@pytest.mark.live_repo
def test_every_gated_freshness_file_is_a_living_doc():
    """The derivation must SUBSUME the gate it strengthens. If a file A2 gates today were not a
    living doc, the derived leg would be silent exactly where the repo already cares most."""
    import audit as aud
    for fname in aud._FRESHNESS_FILES:
        assert cdocs.is_living_doc(fname), f"{fname} is gated but not derivable"


# --- CONTENT vs TOUCH (done-contract item 2) --------------------------------------------------

def test_a_whitespace_only_commit_is_a_touch(tmp_path):
    """T1 — empty under whitespace-blindness. A reflow does not invalidate a review."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC.replace("# A living doc", "# A living doc   "))
    sha = _commit(repo, "chore: reflow", "2026-02-02")
    assert aud._touch_reason(repo, sha, "DOC.md") == aud.TOUCH_WHITESPACE


def test_a_frontmatter_only_commit_is_a_touch(tmp_path):
    """T2 — the load-bearing one. This is exactly the re-stamp / version-bump commit, and a
    delta computed off `git log -1` alone counts it as an edit, which is how a doc that was
    only re-stamped reports itself edited-since-review."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    bumped = _DOC.replace("reconciled_with: handoff-process@6.3.0",
                          "reconciled_with: handoff-process@6.4.0\nowner: rob")
    _put(repo, "DOC.md", bumped)
    sha = _commit(repo, "docs: bump the reconciled spec", "2026-02-03")
    assert aud._touch_reason(repo, sha, "DOC.md") == aud.TOUCH_FRONTMATTER


def test_a_stamp_line_only_commit_is_a_touch(tmp_path):
    """T3 — a PROSE stamp bump, outside frontmatter. Three of A4's four stale docs declare
    only in prose, so a frontmatter-only predicate would miss their re-stamp commits."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC.replace("> Last updated: 2026-01-01", "> Last updated: 2026-02-04"))
    sha = _commit(repo, "docs: re-stamp", "2026-02-04")
    assert aud._touch_reason(repo, sha, "DOC.md") == aud.TOUCH_STAMP_LINE


def test_a_prose_edit_is_content(tmp_path):
    """The other direction, and the one that matters: a real edit must NOT be excused."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC + "\nA new paragraph asserting something new.\n")
    sha = _commit(repo, "docs: say more", "2026-02-05")
    assert aud._touch_reason(repo, sha, "DOC.md") is None


def test_the_classifier_never_reads_the_commit_subject(tmp_path):
    """A4 recommendation 3, pinned. A4's own T4 keyed partly on the commit SUBJECT — author-
    controlled text — and A4 rules it out of a SHIPPED classifier for that reason: under
    derivation a misclassification silently marks a doc fresh, so the one input an author can
    write freely must not be able to buy that verdict.

    A subject that declares a regeneration over a body that is plain prose is CONTENT."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC + "\nSubstantive new doctrine nobody has reviewed.\n")
    sha = _commit(repo, "chore(regen): mechanical regeneration, no content change",
                  "2026-02-06")
    assert aud._touch_reason(repo, sha, "DOC.md") is None


def test_the_derived_date_walks_back_past_a_trailing_touch_run(tmp_path):
    """The whole point of item 2: the derived date is the last CONTENT commit, not the last
    commit. Two re-stamps on top of one real edit must derive to the EDIT's date."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC + "\nReal content.\n")
    _commit(repo, "docs: real edit", "2026-03-01")
    body = _DOC + "\nReal content.\n"
    _put(repo, "DOC.md", body.replace("> Last updated: 2026-01-01", "> Last updated: 2026-03-02"))
    _commit(repo, "docs: re-stamp", "2026-03-02")
    _put(repo, "DOC.md", body.replace("> Last updated: 2026-01-01", "> Last updated: 2026-03-03")
                             .replace("last_reviewed: 2026-01-01", "last_reviewed: 2026-03-03"))
    _commit(repo, "docs: re-stamp again", "2026-03-03")

    sha, derived, skipped = aud._last_content_commit(repo, "DOC.md")
    assert derived == date(2026, 3, 1), "the two re-stamps are TOUCH, not CONTENT"
    assert skipped == 2
    assert sha


# --- the derivation as a whole, and its three classes (items 1, 3, 5) -------------------------

def _three_class_repo(tmp_path) -> Path:
    """One repo carrying one member of each class A4 §3 separates, plus an unstamped doc."""
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "CLAUDE.md", _DOC.replace("last_reviewed: 2026-01-01", "last_reviewed: 2026-04-01"))
    _put(repo, "ARCHITECTURE.md", _DOC.replace("last_reviewed: 2026-01-01",
                                               "last_reviewed: 2026-04-01"))
    _put(repo, "protocols/PLAYBOOK.md", _DOC)          # prose + frontmatter, ungated
    _put(repo, "protocols/README.md", "# no stamp anywhere\n\nprose\n")
    _commit(repo, "feat: the corpus", "2026-04-01")
    _put(repo, "ARCHITECTURE.md", _DOC.replace("last_reviewed: 2026-01-01",
                                               "last_reviewed: 2026-04-01") + "\nunreviewed.\n")
    _put(repo, "protocols/PLAYBOOK.md", _DOC + "\nunreviewed doctrine.\n")
    _commit(repo, "docs: edits nobody re-reviewed", "2026-05-01")
    return repo


def test_the_derivation_preserves_the_three_classes_a4_separates(tmp_path, monkeypatch):
    """Done-contract item 3. gated-and-stale / gated-and-fresh / ungated-and-stale — and the
    third is what funds this lane, because it is the part no gate watches."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md", "ARCHITECTURE.md"])
    rows = {r.path: r for r in aud.derive_doc_freshness(repo)}

    assert rows["ARCHITECTURE.md"].doc_class == aud.CLASS_GATED_STALE
    assert rows["CLAUDE.md"].doc_class == aud.CLASS_GATED_FRESH
    assert rows["protocols/PLAYBOOK.md"].doc_class == aud.CLASS_UNGATED_STALE
    assert rows["protocols/README.md"].doc_class == aud.CLASS_UNSTAMPED


def test_a_doc_with_no_stamp_is_listed_not_skipped(tmp_path, monkeypatch):
    """Done-contract item 5, stated in A4's own words: an absent stamp is not a fresh one.
    The 26 unstamped living docs are the LARGEST class, and the pre-derivation gate skipped
    every one of them into a WARN it never itemised."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    row = {r.path: r for r in aud.derive_doc_freshness(repo)}["protocols/README.md"]
    assert row.declared is None
    assert row.surface == aud.SURFACE_NONE
    assert row.derived == date(2026, 4, 1), "an unstamped doc still gets a derived floor"


def test_a_prose_last_updated_line_counts_as_a_declared_stamp(tmp_path):
    """A4 decided this per contract defaults and said so: three of the four stale docs declare
    ONLY in prose, so without it PLAYBOOK — the lane's own subject — has no declared value to
    compare against and would misreport as unstamped."""
    import audit as aud
    assert aud.parse_declared_freshness("> Last updated: 2026-08-01\n") == (
        date(2026, 8, 1), aud.SURFACE_PROSE)
    assert aud.parse_declared_freshness("**Last updated:** 2026-08-26\n") == (
        date(2026, 8, 26), aud.SURFACE_PROSE)
    assert aud.parse_declared_freshness(_DOC)[1] == aud.SURFACE_FRONTMATTER, (
        "frontmatter is machine-readable and wins where both surfaces exist")
    assert aud.parse_declared_freshness("no stamp here\n") == (None, aud.SURFACE_NONE)


# --- the ancestry test: A4 section 3's same-day hole ------------------------------------------

def test_same_day_content_after_the_stamp_is_seen(tmp_path, monkeypatch):
    """A4 §3's finding, and the sharpest thing this leg does. `%as` is DAY-granular and A2 fails
    only when `reviewed < git_date`, so content committed LATER THE SAME DAY as the stamp passes.
    A4 measured 4 of the 9 gated files carrying exactly that — including the CLAUDE.md re-genre
    that deleted 40% of the file after the stamp claiming it had been read end-to-end.

    Commit ORDER is total; calendar dates are not. Same date, later commit -> stale."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "CLAUDE.md", _DOC)
    _commit(repo, "feat: the doc", "2026-04-01")
    _put(repo, "CLAUDE.md", _DOC.replace("last_reviewed: 2026-01-01",
                                         "last_reviewed: 2026-04-02"))
    _commit(repo, "docs: reviewed end-to-end", "2026-04-02")
    _put(repo, "CLAUDE.md", _DOC.replace("last_reviewed: 2026-01-01",
                                         "last_reviewed: 2026-04-02")
                                + "\nDoctrine nobody has read.\n")
    _commit(repo, "docs: a big edit, same day", "2026-04-02")

    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    row = {r.path: r for r in aud.derive_doc_freshness(repo)}["CLAUDE.md"]
    assert row.declared == date(2026, 4, 2) and row.derived == date(2026, 4, 2), (
        "the DATE compare sees nothing here - that is the whole point")
    assert row.delta_days == 0
    assert row.unreviewed_after_stamp == 1
    assert row.stamp_sha
    assert row.doc_class == aud.CLASS_GATED_STALE, (
        "0d by the date compare, STALE by the predicate the gate intends")

    warned = " ".join(f.evidence for f in aud.check_canonical_freshness(repo)
                      if f.status == "warn")
    assert aud.CLASS_GATED_STALE in warned and "AFTER it" in warned


def test_a_restamp_after_the_content_clears_the_ancestry_finding(tmp_path, monkeypatch):
    """The other direction, so the test above is not passing for a trivial reason: when the
    review lands AFTER the edit, there is nothing unreviewed and the doc is fresh."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "CLAUDE.md", _DOC)
    _commit(repo, "feat: the doc", "2026-04-01")
    _put(repo, "CLAUDE.md", _DOC + "\nNew doctrine.\n")
    _commit(repo, "docs: a big edit", "2026-04-02")
    _put(repo, "CLAUDE.md", (_DOC + "\nNew doctrine.\n").replace(
        "last_reviewed: 2026-01-01", "last_reviewed: 2026-04-02"))
    _commit(repo, "docs: reviewed end-to-end, after the edit", "2026-04-02")

    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    row = {r.path: r for r in aud.derive_doc_freshness(repo)}["CLAUDE.md"]
    assert row.unreviewed_after_stamp == 0
    assert row.doc_class == aud.CLASS_GATED_FRESH


def test_the_batched_and_single_commit_feeds_classify_identically(tmp_path):
    """ONE classifier, TWO feeds — `_touch_reason` (one `git show`) and `_diff_index` (one
    batched `git log -p`). They must never drift into two different notions of "content": the
    batched feed is what every verdict is actually computed from, and the single-commit feed is
    what the predicate tests above exercise. If these disagree, the tests are testing something
    the gate does not run."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC.replace("# A living doc", "# A living doc   "))
    _commit(repo, "chore: reflow", "2026-02-02")
    _put(repo, "DOC.md", _DOC.replace("> Last updated: 2026-01-01",
                                      "> Last updated: 2026-02-03"))
    _commit(repo, "docs: re-stamp", "2026-02-03")
    _put(repo, "DOC.md", _DOC + "\nreal prose.\n")
    _commit(repo, "docs: real edit", "2026-02-04")

    diffs = aud._diff_index(repo, ["DOC.md"])["DOC.md"]
    for d in diffs:
        batched = aud._classify_touch(d.hunks, d.changed, d.created,
                                      aud._blob_pair(repo, d.sha, "DOC.md"))
        assert batched == aud._touch_reason(repo, d.sha, "DOC.md"), d.sha

    # The COUNTS differ, deliberately, and this pins WHY rather than papering over it: under
    # `-w` the whitespace-only commit's diff is empty, so `git log -p` emits no header for it
    # and it never enters the batched index — git applies T1 upstream of the classifier. The
    # commit that is missing must be exactly that one, and `_touch_reason` must independently
    # agree it is a TOUCH.
    everything = aud._derive_git(repo, ["log", "--format=%H", "--", "DOC.md"]).split()
    missing = [s for s in everything if s not in {d.sha for d in diffs}]
    assert len(missing) == 1, "exactly one commit is filtered by -w here"
    assert aud._touch_reason(repo, missing[0], "DOC.md") == aud.TOUCH_WHITESPACE


def test_the_t2_prefilter_only_ever_declines(tmp_path):
    """The pre-filter in front of T2 exists for speed, and a speed filter in front of a
    CORRECTNESS predicate is only admissible if it fails one way. It may make T2 decline
    (-> CONTENT -> a doc reported STALE); it must never excuse a real edit as a TOUCH.

    A prose-only commit must be CONTENT with or without it."""
    import audit as aud
    repo = _living_git_repo(tmp_path / "r")
    _put(repo, "DOC.md", _DOC)
    _commit(repo, "feat: the doc", "2026-02-01")
    _put(repo, "DOC.md", _DOC + "\nPlain prose, no colon at all\n")
    sha = _commit(repo, "docs: prose", "2026-02-02")
    assert aud._touch_reason(repo, sha, "DOC.md") is None
    # And a line that LOOKS yaml-ish in prose still cannot buy a TOUCH: it is below the
    # frontmatter, so the span check rejects it.
    _put(repo, "DOC.md", _DOC + "\nNote: a yaml-ish prose line\n")
    sha = _commit(repo, "docs: yaml-ish prose", "2026-02-03")
    assert aud._touch_reason(repo, sha, "DOC.md") is None


# --- the doctrine row (item 4) -----------------------------------------------------------------

def test_the_doctrine_table_shows_the_live_version_and_the_derived_date(tmp_path, monkeypatch):
    """Done-contract item 4. PLAYBOOK's declared date is a PROSE line no gate parses and its
    version rides `reconciled_with:`; the doctrine row must show the LIVE pair — the derived
    content date beside the declared one — so the table stops asserting a date that git refutes."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    table = aud.doctrine_table(repo)
    row = next(line for line in table.splitlines() if line.startswith("protocols/PLAYBOOK.md"))
    assert "handoff-process@6.4.0" in row or "handoff-process@6.3.0" in row, row
    assert "2026-05-01" in row, "the DERIVED date, which is what the declared one contradicts"
    assert "2026-01-01" in row, "the DECLARED date, kept beside it rather than overwritten"


def test_a_docs_own_version_outranks_the_spec_it_reconciles_against():
    """`reconciled_with:` names which SPEC generation a doc was re-reasoned against; it is not
    the doc's version. Read first, it rendered CLAUDE.md as `handoff-process@6.3.0` when its own
    version is 2.69 — a doctrine table that misreports the version is worse than none."""
    import audit as aud
    assert aud.parse_declared_version(
        "---\nversion: 1.1\nreconciled_with: handoff-process@6.3.0\n---\n") == "1.1"
    assert aud.parse_declared_version(
        "---\nreconciled_with: handoff-process@6.3.0\n---\n") == "handoff-process@6.3.0"
    assert aud.parse_declared_version("# Doc\n\nVersion: 6.3.0\n") == "6.3.0"
    assert aud.parse_declared_version("# Doc\n<!-- version: 2.69 - 2026-08-29 -->\n") == "2.69"


def test_a_per_section_version_sentinel_is_not_the_documents_version():
    """The live regression this pins: `protocols/PLAYBOOK.md` carries per-SECTION
    `<!-- version: 1.0 - 2026-04-26 -->` sentinels from line 477 down, and a whole-file search
    read the first of them as the DOCUMENT's version — reporting PLAYBOOK as `1.0` where its
    only real version claim is its `reconciled_with` spec. A prose version is a HEADER fact, and
    the header ends at the first `## `."""
    import audit as aud
    text = ("---\nreconciled_with: handoff-process@6.3.0\n---\n"
            "# Playbook\n\n> Last updated: 2026-08-01\n\n"
            "## Ch1\n\n<!-- version: 1.0 - 2026-04-26 -->\nsection prose\n")
    assert aud.parse_declared_version(text) == "handoff-process@6.3.0"


@pytest.mark.live_repo
def test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date():
    """Done-contract item 4 against the LIVE tree, not a fixture. PLAYBOOK is the doc that names
    the problem: its date is a prose line no gate parses and its version rides `reconciled_with`,
    so its own table could assert a date git refutes and nothing would notice."""
    import audit as aud
    row = {r.path: r for r in aud.derive_doc_freshness(_REPO_ROOT)}[cdocs.PLAYBOOK_PATH]
    assert row.version and row.version.startswith("handoff-process@")
    assert row.surface == aud.SURFACE_PROSE, "PLAYBOOK declares in prose, which no gate reads"
    assert row.derived is not None and row.declared is not None
    assert row.doc_class == aud.CLASS_UNGATED_STALE, (
        "if this ever flips, PLAYBOOK was either re-stamped or gated - both are real events "
        "that should be seen, not absorbed")


# --- the gate's posture (item 1: the derivation is GATED) --------------------------------------

def test_a_shallow_clone_refuses_rather_than_passes(tmp_path, monkeypatch):
    """A4 recommendation 5, and A4 witnessed the failure live: under a graft at 2026-08-25 its
    own first pass mis-dated `protocols/ESSENTIALS.md` and 14 others. A date compare degrades
    QUIETLY on a shallow clone; an ancestry test must not — so this is `fail`, never a skip.

    Same Z-G4 rule `check_intake_lifecycle` states: a failed computation of an AVAILABLE ground
    truth blocks, because `unavailable` renders as N/A and ships green having measured nothing."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_git_is_shallow", lambda p: True)
    with pytest.raises(aud.DerivationRefused):
        aud.derive_doc_freshness(repo)

    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    fails = [f for f in aud.check_canonical_freshness(repo) if f.status == "fail"]
    assert any("shallow" in f.evidence for f in fails), "refusal must reach the gate as a FAIL"


def test_no_git_history_degrades_to_na_not_to_a_false_pass(tmp_path, monkeypatch):
    """The OTHER degrade, and the distinction is the point. Git absent = the ground truth does
    not exist (a non-git consumer), which is a legitimate `n/a`. Git present but grafted = the
    ground truth exists and is lying, which is the FAIL above."""
    import audit as aud
    (tmp_path / "CLAUDE.md").write_bytes(_DOC.encode("utf-8"))
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    with pytest.raises(aud.DerivationUnavailable):
        aud.derive_doc_freshness(tmp_path)
    findings = aud.check_canonical_freshness(tmp_path)
    assert not [f for f in findings if f.status == "fail"]
    assert any(f.status == "n/a" for f in findings[1:])


def test_the_derived_leg_is_warn_class_on_arrival(tmp_path, monkeypatch):
    """The RATCHET is declared, not remembered. A4 §3 measured 4 of 9 GATED files already
    carrying unreviewed content the date-granular A2 cannot see; promoting the derived leg to
    FAIL on arrival would therefore wedge `audit-health` — the PRE-COMMIT gate — on four
    pre-existing docs, which is an operator ratchet decision and not a lane's.

    So: WARN on arrival, ship-gate teeth (`cmd_ship_gate` REDs on any undispositioned warn),
    and the promotion condition is one line — see `check_canonical_freshness`'s docstring."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md", "ARCHITECTURE.md"])
    findings = aud.check_canonical_freshness(repo)
    derived = findings[1:]
    assert derived, "the derived legs must reach the gate"
    assert not [f for f in derived if f.status == "fail"]
    warned = " ".join(f.evidence for f in derived if f.status == "warn")
    assert aud.CLASS_GATED_STALE in warned
    assert aud.CLASS_UNGATED_STALE in warned
    assert aud.CLASS_UNSTAMPED in warned


def test_check_canonical_freshness_keeps_its_first_finding_as_the_a1_a2_verdict(tmp_path,
                                                                                monkeypatch):
    """A REGRESSION PIN, and it is load-bearing: ten call sites in `tests/test_audit.py` read
    `check_canonical_freshness(...)[0]`, and `tests/test_enforcement_coverage.py`'s fire-test
    greps the leg's fails. The derived findings APPEND; index 0 stays the A1/A2 verdict it has
    always been, so nothing outside this lane's write scope has to move."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["ARCHITECTURE.md"])
    first = aud.check_canonical_freshness(repo)[0]
    assert first.check_name == "canonical_freshness"
    assert first.status == "fail", "ARCHITECTURE.md is A2-stale in this fixture"
    assert "predates last edit" in first.evidence


def test_no_finding_carries_a_literal_pipe(tmp_path, monkeypatch):
    """`Finding.evidence` is markdown-table-safe by contract (`audit_checks/_common.Finding`),
    and a doctrine ROW is exactly the shape that reintroduces a pipe by accident."""
    import audit as aud
    repo = _three_class_repo(tmp_path)
    monkeypatch.setattr(aud, "_FRESHNESS_FILES", ["CLAUDE.md"])
    for f in aud.check_canonical_freshness(repo):
        assert "|" not in f.evidence, f.evidence
