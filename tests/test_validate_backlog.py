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
### Story one
So that reasons hold.
- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1
### Story two
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
    text = VALID + "### Empty story\nSo that nothing.\n"
    hard, warn = _run(text)
    assert hard == []
    assert any("no tasks" in w for w in warn)


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
### Story one
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
### Story one
So that reasons hold.
- [#1] [P1][M] {t1} · Done when: x
- [#2] [P1][M] {t2} · Done when: y
"""


def _dup2(t1, t2):
    return DUP2.format(t1=t1, t2=t2)


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


@pytest.mark.live_repo
def test_live_backlog_no_spurious_dup_warn():
    # specificity regression: the real BACKLOG has no near-duplicate pairs at the tuned
    # threshold (max distinct-pair Jaccard is well below it) -> zero dedup WARNs
    text = (Path(vb.__file__).resolve().parent.parent / "BACKLOG.md").read_text(encoding="utf-8")
    _, warn = _run(text)
    assert not any("possible duplicate" in w for w in warn)
