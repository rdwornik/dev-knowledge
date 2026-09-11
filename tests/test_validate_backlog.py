"""Unit tests for scripts/validate_backlog.py (ADR-66 story-map hierarchy validator)."""

import importlib.util
from pathlib import Path
import pytest

_VB = Path(__file__).resolve().parent.parent / "scripts" / "validate_backlog.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_backlog", _VB)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vb = _load()

VALID = """# .dev-knowledge BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### [S1] Story one
So that reasons hold.
- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1
### [S2] Story two
So that more reasons.
- [#2] [P3][S] do another thing · Done when: criterion met
"""


def _run(text):
    return vb.validate(*vb.parse(text))


def test_valid_passes():
    hard, _ = _run(VALID)
    assert hard == []


def test_missing_big_picture_fails():
    hard, _ = _run(VALID.replace("## Big picture", "## Overview"))
    assert any("Big picture" in h for h in hard)


def test_duplicate_big_picture_fails():
    hard, _ = _run(VALID.replace("## Theme A", "## Big picture", 1))
    assert any("Big picture" in h for h in hard)


def test_story_missing_so_that_fails():
    hard, _ = _run(VALID.replace("So that reasons hold.\n", ""))
    assert any("So that" in h for h in hard)


def test_task_missing_done_when_fails():
    hard, _ = _run(VALID.replace(" · Done when: it is done · refs ADR-1", ""))
    assert any("Done when" in h for h in hard)


def test_task_missing_band_fails():
    hard, _ = _run(VALID.replace("[#1] [P1][M] ", "[#1] "))
    assert any("band" in h for h in hard)


def test_duplicate_id_fails():
    hard, _ = _run(VALID.replace("[#2]", "[#1]"))
    assert any("duplicate id" in h for h in hard)


def test_orphan_task_fails():
    orphan = """# B
## Big picture
x
## Theme A
> As a p, I want g.
- [#9] [P1][M] orphan task · Done when: x
"""
    hard, _ = _run(orphan)
    assert any("not under a user story" in h for h in hard)


def test_structured_done_marker_fails():
    hard, _ = _run(VALID.replace(" · refs ADR-1", " · status:done"))
    assert any("done task" in h for h in hard)


def test_legit_bracket_x_in_prose_passes():
    # a literal [x] inside task prose is NOT a done marker
    hard, _ = _run(VALID.replace("do a thing", "document the [x] checkbox syntax"))
    assert hard == []


def test_empty_story_warns_not_fails():
    text = VALID + "### [S3] Empty story\nSo that nothing.\n"
    hard, warn = _run(text)
    assert hard == []
    assert any("no tasks" in w for w in warn)


# --- #286 stable [S<n>] story-id grammar ------------------------------------

def test_parse_extracts_story_sid():
    _, stories, _ = vb.parse(VALID)
    assert [s["sid"] for s in stories] == ["1", "2"]


def test_story_missing_sid_fails():
    # strip the [S1] prefix off the first story heading.
    hard, _ = _run(VALID.replace("### [S1] Story one", "### Story one"))
    assert any("[S<n>] id" in h for h in hard)


def test_duplicate_story_sid_fails():
    # collide S2 onto S1.
    hard, _ = _run(VALID.replace("### [S2] Story two", "### [S1] Story two"))
    assert any("duplicate story id [S1]" in h for h in hard)


def test_valid_story_sids_pass():
    # both stories carry distinct [S<n>] ids -> no story-id hard fail.
    hard, _ = _run(VALID)
    assert not any("[S<n>] id" in h or "duplicate story id" in h for h in hard)


def test_story_sid_must_have_title_after_it():
    # a bare [S1] with no title is not a valid story-id prefix -> missing-id fail.
    hard, _ = _run(VALID.replace("### [S1] Story one", "### [S1]"))
    assert any("[S<n>] id" in h for h in hard)


# --- #83: in-place RESOLVED / struck-through task lines (ADR-65 done-items-leave) ---
# Fixture shape from commit 052e311 (the #79 stub finding F2 exposed): a task struck
# through in place + a bold **RESOLVED** marker, instead of the item LEAVING the file.

def test_struck_through_task_fails():
    hard, _ = _run(VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] ~~[P1][M] do a thing · Done when: it is done · refs ADR-1~~ "
        "**RESOLVED 2026-06-03 — no build needed.**",
    ))
    assert any("ADR-65" in h and "resolved" in h.lower() for h in hard)


def test_inplace_resolved_marker_fails():
    hard, _ = _run(VALID.replace(
        " · refs ADR-1",
        " · refs ADR-1 **RESOLVED 2026-06-05 — landed.**",
    ))
    assert any("ADR-65" in h and "resolved" in h.lower() for h in hard)


def test_clean_task_with_done_when_passes_inplace_check():
    # the unmodified VALID has no strike/RESOLVED marker -> no in-place finding
    # ("Done when:" is title-case and must NOT trip the all-caps DONE marker)
    hard, _ = _run(VALID)
    assert not any("in-place" in h for h in hard)


@pytest.mark.live_repo
def test_live_backlog_passes_inplace_check():
    text = (Path(vb.__file__).resolve().parent.parent / "BACKLOG.md").read_text(encoding="utf-8")
    hard, _ = _run(text)
    assert not any("in-place" in h for h in hard)


# --- #156: durable task-graph — depends-on (reference-existence + no-cycle) + serialize-group ---
# depends-on = HARD blocked-by; serialize-group = shared-file mutual-exclusion label (surfaced,
# never a failure). Cases that assert a FAIL is *produced* are xfail(strict) until the impl commit
# lands; the impl commit REMOVES these markers (strict => an XPASS fails, forcing their removal).
# Cases that assert valid input passes / no false-positive stay green throughout (no marker).

# Three tasks under one story; {dep1..dep3} inject trailing inline clauses per task.
DEP3 = """# .dev-knowledge BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### [S1] Story one
So that reasons hold.
- [#1] [P1][M] task one · Done when: x{dep1}
- [#2] [P1][M] task two · Done when: x{dep2}
- [#3] [P1][M] task three · Done when: x{dep3}
"""


def _dep3(dep1="", dep2="", dep3=""):
    return DEP3.format(dep1=dep1, dep2=dep2, dep3=dep3)


def test_valid_depends_on_passes():
    # edges into existing live ids, acyclic -> no hard fails
    hard, _ = _run(_dep3(dep1=" · depends-on: #2", dep2=" · depends-on: #3"))
    assert hard == []


def test_serialize_group_is_not_a_failure():
    # two tasks sharing a serialize-group is a legitimate mutual-exclusion label, not a fail
    hard, _ = _run(_dep3(dep1=" · serialize-group: audit-py", dep2=" · serialize-group: audit-py"))
    assert hard == []


def test_refs_or_prose_id_not_treated_as_dependency():
    # a non-existent id appearing only in refs/prose (NOT in a depends-on clause) must NOT
    # trip reference-existence — guards the clause-scoped parse against false positives
    hard, _ = _run(_dep3(dep1=" · refs ADR-1, #999 (mentioned in prose, not a dependency)"))
    assert not any("non-existent" in h for h in hard)


def test_depends_on_nonexistent_id_fails():
    hard, _ = _run(_dep3(dep1=" · depends-on: #999"))
    assert any("non-existent" in h and "999" in h for h in hard)


def test_direct_cycle_fails():
    hard, _ = _run(_dep3(dep1=" · depends-on: #2", dep2=" · depends-on: #1"))
    assert any("cycle" in h.lower() for h in hard)


def test_indirect_cycle_fails():
    # A -> B -> C -> A : a direct-only detector would miss this
    hard, _ = _run(_dep3(dep1=" · depends-on: #2", dep2=" · depends-on: #3", dep3=" · depends-on: #1"))
    assert any("cycle" in h.lower() for h in hard)


def test_indirect_cycle_reports_full_path():
    hard, _ = _run(_dep3(dep1=" · depends-on: #2", dep2=" · depends-on: #3", dep3=" · depends-on: #1"))
    cyc = [h for h in hard if "cycle" in h.lower()]
    assert cyc and all(f"#{n}" in cyc[0] for n in ("1", "2", "3"))


def test_self_loop_fails():
    hard, _ = _run(_dep3(dep1=" · depends-on: #1"))
    assert any("itself" in h.lower() for h in hard)


def test_parse_deps_is_clause_scoped():
    # only the depends-on clause counts; refs/prose #ids are ignored; ids are BARE strings
    deps = vb._parse_deps("do x · Done when: y · refs ADR-1, #2 · depends-on: #3, #4 · note #2")
    assert deps == ["3", "4"]


# --- [#424]: `_DEPID_RE` required a `#`, so a BARE id in a depends-on clause parsed to
# nothing and the edge was INERT -- present in the text, absent from the graph, gating
# nothing. Live at the fix: 5 clauses, 3 parsed (`#171` `#23` `#604`), 2 inert (`383`
# `390`). These pin the bare form AND the boundary that keeps it from over-reading.

def test_parse_deps_accepts_bare_id():
    # the [#424] defect proper: no `#`, still a dependency
    assert vb._parse_deps("do x · depends-on: 383") == ["383"]
    assert vb._parse_deps("do x · depends-on: 390 · refs y") == ["390"]


def test_parse_deps_bare_and_hashed_mix():
    assert vb._parse_deps("do x · depends-on: #3, 4, [#5] · note z") == ["3", "4", "5"]


def test_parse_deps_bare_id_edge_is_live_end_to_end():
    # not just the regex -- a bare edge must reach reference-existence and cycle detection,
    # which is the whole point of the row (an edge that parses but never gates is the defect)
    hard, _ = _run(_dep3(dep1=" · depends-on: 999"))
    assert any("non-existent" in h and "999" in h for h in hard)
    hard, _ = _run(_dep3(dep1=" · depends-on: 2", dep2=" · depends-on: 1"))
    assert any("cycle" in h.lower() for h in hard)


def test_parse_deps_bare_id_does_not_over_read():
    # the widening must not turn embedded digits into phantom edges. A date, a version, and
    # a digit glued to a word are NOT ids -- without the boundary, `2026-08-27` alone would
    # manufacture three.
    assert vb._parse_deps("do x · depends-on: #5 since 2026-08-27") == ["5"]
    assert vb._parse_deps("do x · depends-on: #7 v1.4.0") == ["7"]
    assert vb._parse_deps("do x · depends-on: #9 (blocked until W2)") == ["9"]


def test_parse_serialize_groups():
    # single clause -> 1-list; works mid-line (trailing ·) and at end-of-line ($ anchor)
    assert vb._parse_serialize_groups("do x · serialize-group: audit-py · refs y") == ["audit-py"]
    assert vb._parse_serialize_groups("do x · refs y · serialize-group: audit-py") == ["audit-py"]
    assert vb._parse_serialize_groups("do x · refs y") == []


# --- #167: multi-surface collisions (≥2 serialize-group clauses) + delimiter-anchored parse ---

def test_parse_serialize_groups_multi():
    # a task colliding on TWO shared surfaces carries two clauses; BOTH are read (finditer,
    # not search) — the dropped-edge fix (#105↔#112, #5↔#77 were silently dropped pre-#167)
    labels = vb._parse_serialize_groups(
        "do x · serialize-group: block-immutable · serialize-group: settings-json · refs y")
    assert labels == ["block-immutable", "settings-json"]


def test_serialize_groups_places_task_in_every_group():
    # serialize_groups() summary places a multi-clause task in EACH named group
    text = _dep3(dep1=" · serialize-group: alpha · serialize-group: beta",
                 dep2=" · serialize-group: beta")
    hard, _ = _run(text)
    assert hard == []
    _, _, tasks = vb.parse(text)
    groups = vb.serialize_groups(tasks)
    assert groups.get("alpha") == ["1"]
    assert sorted(groups.get("beta", [])) == ["1", "2"]


def test_serialize_group_prose_mention_not_a_clause():
    # #167 self-trip guard (the 2026-06-14 incident): a task body that NAMES the clause in
    # prose — both a mid-segment mention AND a clause-shaped form with TRAILING prose after
    # the token — must NOT register a phantom group. The delimiter anchor (?=·|$) requires
    # the label to butt the next ·/EOL, so "foo and trailing notes" is rejected, not captured.
    text = _dep3(dep1=" · Done when: support multiple serialize-group clauses per task, "
                      "so a · serialize-group: foo and trailing notes mention stays inert")
    hard, _ = _run(text)
    assert hard == []
    _, _, tasks = vb.parse(text)
    assert vb.serialize_groups(tasks) == {}  # no "foo", no "foo and trailing notes"


# --- #187: dedup-on-entry — deterministic near-duplicate WARN (normalized-title token-overlap) ---
# A WARN (never a hard-fail), no LLM. STATED LIMIT: token-overlap only; does NOT catch
# low-title-overlap semantic dups. Sensitivity (a near-dup WARNs) + specificity (distinct
# items, and the live BACKLOG, do not) are the #187 closure.

DUP2 = """# .dev-knowledge BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### [S1] Story one
So that reasons hold.
- [#1] [P1][M] {t1} · Done when: x
- [#2] [P1][M] {t2} · Done when: y
"""


def _dup2(t1, t2):
    return DUP2.format(t1=t1, t2=t2)


def _dupN(titles):
    # synthetic BACKLOG with one row per title (ids #1..#N) under one story — a fixture for
    # dedup-heuristic behaviour tests that must NOT read the mutable live BACKLOG.
    rows = "\n".join(f"- [#{i + 1}] [P1][M] {t} · Done when: x" for i, t in enumerate(titles))
    return (
        "# .dev-knowledge BACKLOG\n"
        "## Big picture\n"
        "A short paragraph.\n"
        "**Themes (backbone):** Theme A\n"
        "## Theme A\n"
        "> As a persona, I want a goal.\n"
        "### [S1] Story one\n"
        "So that reasons hold.\n"
        f"{rows}\n"
    )


def test_near_duplicate_title_warns():
    # two tasks with near-identical action titles -> a dedup WARN naming both ids
    text = _dup2(
        "sync the task-graph checks into the distributed plugin floor validator",
        "sync the task-graph checks into the distributed plugin floor validator copy")
    _, warn = _run(text)
    assert any("possible duplicate" in w and "#1" in w and "#2" in w for w in warn)


def test_distinct_titles_no_dup_warn():
    # genuinely distinct titles -> NO dedup WARN (the false-positive guard)
    text = _dup2(
        "sync the task-graph reference-existence checks into the distributed plugin floor",
        "render a child methodology floor bundle for the browser carrier distribution")
    _, warn = _run(text)
    assert not any("possible duplicate" in w for w in warn)


def test_dup_warn_is_never_a_hard_fail():
    # a near-duplicate is surfaced as a WARN, never blocks (Layer-2-safe)
    text = _dup2("audit the audit-py health check gate",
                 "audit the audit-py health check gate again")
    hard, warn = _run(text)
    assert hard == []
    assert any("possible duplicate" in w for w in warn)


def test_title_tokens_strips_band_and_stopwords():
    # band + post-`·` clauses excluded; stopwords + <3-char tokens dropped; lowercased set
    toks = vb._title_tokens(
        "[P1][M] Sync the floor validator NOW · Done when: it works · refs ADR-1")
    assert toks == {"sync", "floor", "validator"}


def test_dedup_specificity_holds_on_a_distinct_fixture():
    # SPECIFICITY (fixture-bound; does NOT read the live BACKLOG). A heuristic-behaviour test
    # must not depend on mutable production content: a legitimate near-duplicate filing (e.g.
    # the ruled #409/#410/#411 night-batch triple) would otherwise turn the suite red. The
    # live-corpus signal already lives where it belongs — validate_backlog's runtime advisory
    # WARN, exit 0 (see test_dup_warn_is_never_a_hard_fail). Here we assert the heuristic's
    # SPECIFICITY on a fixture: genuinely-distinct rows that share incidental domain vocabulary
    # — including a deliberately near-boundary pair (rows 0/1 externalize distinct registries;
    # max pairwise Jaccard ~0.545, below the 0.70 threshold) — must NOT be flagged.
    # Teeth: this goes RED if the heuristic regresses into false positives. Witnessed by
    # lowering _DUP_TITLE_THRESHOLD 0.70 -> 0.50 (< the 0.545 pair): the pair is then flagged
    # and this assertion fails (see the arc's terra/verify record).
    text = _dupN([
        "externalize the hermetization frozenset registry into a machine-readable path pattern",
        "externalize the parity-surface frozenset registry into a machine-readable gate pattern",
        "render a child methodology floor bundle for the browser carrier distribution channel",
        "wire the coherence forgotten-version-bump nudge behind a deferred-hash escape gate",
    ])
    _, warn = _run(text)
    assert not any("possible duplicate" in w for w in warn)


# --- #524 leg (b): body-date scan (review_date=<past date> WARN) ------------------------

def test_past_review_date_warns():
    text = VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] [P1][M] do a thing · Done when: it is done · review_date=2026-08-13",
    )
    hard, warn = vb.validate(*vb.parse(text), today=vb.date(2026, 8, 14))
    assert hard == []
    assert any("past review_date=2026-08-13" in w and "#1" in w for w in warn)


def test_future_review_date_is_silent():
    text = VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] [P1][M] do a thing · Done when: it is done · review_date=2026-08-26",
    )
    hard, warn = vb.validate(*vb.parse(text), today=vb.date(2026, 8, 14))
    assert hard == []
    assert not any("review_date" in w for w in warn)


# --- [#689] conductor E: the `· phase:` clause and its enum ----------------------------
# RED-FIRST (ADR-108 §B). These five were authored and witnessed FAILING before
# `_PHASE_ENUM` / `_parse_phase` / `_check_phase` existed in the module -- the RED output is
# quoted in the landing commit body. The enum itself is not invented here: it is the
# operator's own delivery spine, carried verbatim from the header of
# `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` ("one spine over intake -> task -> build
# with tests -> review -> merge -> docs -> deploy -> telemetry -> archive").


def _phased(value):
    """VALID with a `· phase: <value>` clause on row [#1]."""
    return VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        f"- [#1] [P1][M] do a thing · Done when: it is done · phase: {value} · refs ADR-1",
    )


def test_phase_enum_is_the_operator_delivery_spine():
    # Order is load-bearing: the workflow's phase gate reads the index to answer "which
    # phase comes next", so a re-ordered enum silently re-orders the process.
    assert vb._PHASE_ENUM == (
        "intake", "task", "build", "review", "merge", "docs", "deploy", "telemetry", "archive")


@pytest.mark.parametrize("value", ["intake", "task", "build", "review", "merge",
                                   "docs", "deploy", "telemetry", "archive"])
def test_every_enum_member_is_accepted(value):
    hard, warn = _run(_phased(value))
    assert hard == []
    assert not any("phase" in w for w in warn)


def test_phase_outside_the_enum_hard_fails_and_names_the_enum():
    hard, _ = _run(_phased("shipped"))
    assert any("phase" in h and "shipped" in h and "#1" in h for h in hard)
    # The refusal must NAME the admitted set -- a gate that rejects without naming the
    # vocabulary makes the author guess, which is how a second spelling gets invented.
    assert any("telemetry" in h for h in hard if "shipped" in h)


def test_two_phase_clauses_on_one_row_hard_fail():
    text = VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] [P1][M] do a thing · Done when: it is done · phase: build · phase: review",
    )
    hard, _ = _run(text)
    assert any("one phase" in h.lower() and "#1" in h for h in hard)


def test_a_row_with_no_phase_clause_is_silent():
    # ABSENCE IS LEGAL, deliberately, and this is the assertion that keeps it so. Making the
    # clause mandatory would (a) demand a mass edit of every live row and (b) break
    # tests/test_validate_backlog_twin_parity.py, whose shared fixtures carry no phase clause
    # and whose plugin twin has no phase check -- the hub would invent findings the twin
    # cannot. Adoption is MEASURED by the workflow's `unphased` count, not mandated here.
    hard, warn = _run(VALID)
    assert hard == []
    assert not any("phase" in w for w in warn)


def test_phase_clause_is_delimiter_anchored_so_prose_cannot_fake_one():
    # Same defence as `_SERIALIZE_CLAUSE_RE`: a body that MENTIONS the word must not register
    # a phantom clause, or every row discussing the phase table would acquire one.
    text = VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] [P1][M] do a thing · Done when: the phase: gate fires · refs ADR-1",
    )
    hard, _ = _run(text)
    assert hard == []
    assert vb._parse_phase("Done when: the phase: gate fires") is None


def test_phase_census_counts_phased_and_unphased():
    _, _, tasks = vb.parse(_phased("build"))
    census = vb.phase_census(tasks)
    assert census["build"] == ["1"]
    assert census["unphased"] == ["2"]
