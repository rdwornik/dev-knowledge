"""Unit tests for scripts/probe_child_backlogs.py (#120 child-BACKLOG conformance probe).

The probe is floor-faithful: it classifies against the PLUGIN floor validator
(plugins/tier1-lifecycle/scripts/validate_backlog.py, which lacks the hub's #156
task-graph checks), so a child is greenlit iff it would pass the hook it would actually
install. The depends-on drift-guard test below is the load-bearing proof of that.
"""

import importlib.util
from pathlib import Path

import yaml

_PCB = Path(__file__).resolve().parent.parent / "scripts" / "probe_child_backlogs.py"


def _load():
    spec = importlib.util.spec_from_file_location("probe_child_backlogs", _PCB)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pcb = _load()
# The REAL floor validator — most verdict tests run against it so the reuse is exercised end-to-end.
floor = pcb.load_floor_validator()


CONFORMANT = """# X BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### Story one
So that reasons hold.
- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1
"""

# A floor-conformant task carrying a depends-on edge to a NON-EXISTENT id. The hub's #156
# reference-existence check would hard-fail this; the plugin floor has no such check, so a
# child's installed hook would accept it. The probe must agree -> conformant (zero drift).
DEPENDS_ON_ABSENT = """# X BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### Story one
So that reasons hold.
- [#1] [P1][M] do a thing · Done when: it is done · depends-on: #999 · refs ADR-1
"""


def _repo(tmp_path, text, name="child"):
    d = tmp_path / name
    d.mkdir()
    (d / "BACKLOG.md").write_text(text, encoding="utf-8")
    return d


def _mk_index(eco_dir, repos):
    eco_dir.mkdir(parents=True, exist_ok=True)
    idx = eco_dir / "index.yaml"
    idx.write_text(yaml.safe_dump({"repos": repos}), encoding="utf-8")
    return idx


def _mk_state(eco_dir, name, path):
    d = eco_dir / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "state.yaml").write_text(
        yaml.safe_dump({"name": name, "path": str(path), "last_audit": None, "findings": []}),
        encoding="utf-8")


# --- conformance classification (against the real floor) ---

def test_classify_conformant(tmp_path):
    verdict, detail, n_hard, _ = pcb.classify_backlog(_repo(tmp_path, CONFORMANT), floor)
    assert verdict == "conformant"
    assert n_hard == 0
    assert "tasks)" in detail


def test_classify_needs_migration_missing_so_that(tmp_path):
    text = CONFORMANT.replace("So that reasons hold.\n", "")
    verdict, detail, n_hard, _ = pcb.classify_backlog(_repo(tmp_path, text), floor)
    assert verdict == "needs-migration"
    assert n_hard >= 1
    assert "So that" in detail


def test_depends_on_absent_id_is_conformant_floor_has_no_156(tmp_path):
    # THE drift guard: floor lacks #156, so a dangling depends-on edge is NOT a hard-fail.
    verdict, _, _, _ = pcb.classify_backlog(_repo(tmp_path, DEPENDS_ON_ABSENT), floor)
    assert verdict == "conformant"


def test_classify_absent(tmp_path):
    d = tmp_path / "child"
    d.mkdir()
    verdict, detail, _, _ = pcb.classify_backlog(d, floor)
    assert verdict == "absent"
    assert "no BACKLOG.md" in detail


def test_classify_unreachable_missing_dir(tmp_path):
    verdict, detail, _, _ = pcb.classify_backlog(tmp_path / "nope", floor)
    assert verdict == "unreachable"
    assert "not found" in detail


def test_classify_unreachable_none_path():
    verdict, _, _, _ = pcb.classify_backlog(None, floor)
    assert verdict == "unreachable"


def test_classify_unparseable_on_raise(tmp_path):
    class _Boom:
        BIG_PICTURE = "Big picture"

        def parse(self, text):
            raise RuntimeError("boom")

        def validate(self, *a):
            return [], []

    verdict, detail, _, _ = pcb.classify_backlog(_repo(tmp_path, CONFORMANT), _Boom())
    assert verdict == "unparseable"
    assert "RuntimeError" in detail


def test_warnings_do_not_block_conformant(tmp_path):
    # a zero-task story is a floor WARN, not a hard-fail -> still conformant
    text = CONFORMANT + "### Empty story\nSo that nothing.\n"
    verdict, _, n_hard, n_warn = pcb.classify_backlog(_repo(tmp_path, text), floor)
    assert verdict == "conformant"
    assert n_hard == 0
    assert n_warn >= 1


def test_real_floor_loads_and_canonical_fixture_is_conformant():
    # reuse the committed conformant exemplar; proves real floor + real fixture agree
    fixture_repo = Path(__file__).resolve().parent / "fixtures" / "repo-with-structural-checks"
    verdict, _, _, _ = pcb.classify_backlog(fixture_repo, floor)
    assert verdict == "conformant"


# --- discovery (fake ecosystem trees; no real-child access) ---

def test_discover_from_index_yaml_excludes_hub(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"
    (tmp_path / "ai-council").mkdir()
    (tmp_path / "corp-ops").mkdir()
    idx = _mk_index(eco, [
        {"name": ".dev-knowledge", "path": str(hub)},
        {"name": "ai-council", "path": str(tmp_path / "ai-council")},
        {"name": "corp-ops", "path": str(tmp_path / "corp-ops")},
    ])
    children = pcb.discover_children(hub, idx, eco)
    assert [c.name for c in children] == ["ai-council", "corp-ops"]
    assert all(c.path.exists() for c in children)


def test_discover_excludes_hub_when_run_from_worktree(tmp_path):
    # running dir is a dev-knowledge-NNN worktree; the registry self-entry is `.dev-knowledge`.
    hub = tmp_path / "dev-knowledge-120"
    hub.mkdir()
    eco = hub / "ecosystem"
    (tmp_path / ".dev-knowledge").mkdir()
    (tmp_path / "ai-council").mkdir()
    idx = _mk_index(eco, [
        {"name": ".dev-knowledge", "path": str(tmp_path / ".dev-knowledge")},
        {"name": "ai-council", "path": str(tmp_path / "ai-council")},
    ])
    children = pcb.discover_children(hub, idx, eco)
    assert [c.name for c in children] == ["ai-council"]


def test_discover_repo_path_override_bypasses_registry(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"
    idx = _mk_index(eco, [{"name": "ai-council", "path": str(tmp_path / "ai-council")}])
    target = tmp_path / "explicit"
    target.mkdir()
    children = pcb.discover_children(hub, idx, eco, explicit_paths=[str(target)])
    assert [c.name for c in children] == ["explicit"]
    assert children[0].path.resolve() == target.resolve()


def test_discover_empty_is_fail_soft(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"  # never created
    assert pcb.discover_children(hub, eco / "index.yaml", eco) == []


def test_state_yaml_path_refines_stale_index_path(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"
    idx = _mk_index(eco, [{"name": "ai-council", "path": str(tmp_path / "stale")}])
    real = tmp_path / "real-ai-council"
    real.mkdir()
    _mk_state(eco, "ai-council", real)
    children = pcb.discover_children(hub, idx, eco)
    assert len(children) == 1
    assert children[0].path.resolve() == real.resolve()


def test_malformed_index_falls_through_to_state_dirs(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"
    eco.mkdir()
    (eco / "index.yaml").write_text("{[}", encoding="utf-8")  # invalid YAML
    (tmp_path / "ai-council").mkdir()
    _mk_state(eco, "ai-council", tmp_path / "ai-council")
    children = pcb.discover_children(hub, eco / "index.yaml", eco)
    assert [c.name for c in children] == ["ai-council"]


def test_discover_dedups_by_name(tmp_path):
    hub = tmp_path / ".dev-knowledge"
    hub.mkdir()
    eco = hub / "ecosystem"
    (tmp_path / "ai-council").mkdir()
    idx = _mk_index(eco, [
        {"name": "ai-council", "path": str(tmp_path / "ai-council")},
        {"name": "ai-council", "path": str(tmp_path / "ai-council")},
    ])
    children = pcb.discover_children(hub, idx, eco)
    assert [c.name for c in children] == ["ai-council"]


# --- CLI / output ---

def test_main_exit_zero_no_children(monkeypatch, capsys):
    monkeypatch.setattr(pcb, "discover_children", lambda *a, **k: [])
    assert pcb.main([]) == 0
    assert "nothing to probe" in capsys.readouterr().out


def test_main_exit_zero_with_findings(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(pcb, "discover_children",
                        lambda *a, **k: [pcb.Child("fake", tmp_path / "nope")])
    assert pcb.main([]) == 0
    out = capsys.readouterr().out
    assert "UNREACHABLE" in out and "fake" in out


def test_main_nonzero_on_floor_load_failure(monkeypatch, capsys):
    def _boom(*a, **k):
        raise ImportError("nope")

    monkeypatch.setattr(pcb, "load_floor_validator", _boom)
    assert pcb.main([]) == 1
    assert "could not load the floor validator" in capsys.readouterr().err


def test_report_is_cp1252_encodable():
    # the floor's real hard-fail messages carry em-dash + middot (both cp1252); the probe's
    # own strings stay ASCII. Encoding must not raise (the U+2192-arrow Windows-console trap).
    results = [
        pcb.ChildResult("ai-council", None, "conformant", "(4 themes, 9 stories, 14 tasks)", 0, 1),
        pcb.ChildResult("corp-ops", None, "needs-migration",
                        '1 hard-fail(s): user story missing a "So that" line — story "x" line 12', 1, 0),
        pcb.ChildResult("x", None, "absent", "no BACKLOG.md at repo root", 0, 0),
    ]
    pcb.format_report(results).encode("cp1252")


def test_summary_line_counts():
    results = [
        pcb.ChildResult("a", None, "conformant", "x", 0, 0),
        pcb.ChildResult("b", None, "conformant", "x", 0, 0),
        pcb.ChildResult("c", None, "needs-migration", "x", 2, 0),
        pcb.ChildResult("d", None, "absent", "x", 0, 0),
    ]
    report = pcb.format_report(results)
    assert "2 conformant, 1 needs-migration, 1 absent, 0 unreachable (of 4 children)" in report


def test_summary_includes_unparseable_only_when_present():
    base = [pcb.ChildResult("a", None, "conformant", "x", 0, 0)]
    assert "unparseable" not in pcb.format_report(base)
    withbad = base + [pcb.ChildResult("b", None, "unparseable", "x", 0, 0)]
    assert "1 unparseable" in pcb.format_report(withbad)
