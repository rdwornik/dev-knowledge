"""L3: provisioning joins the repo graph ([#664] clause 2, [#554] substrate).

RED-FIRST. Every test below was written and run before `.devcontainer/provision.sh` was a
wiring surface, before `_surface_strings` could read a shell script, and before `safe_remove`
had a wiring leg. The refusal test failed with `status == 'safe'` — the exact false PASS that
deleted `scripts/cloud_provisioning.py` — and the census tests failed on a `WIRING_SURFACES`
tuple that did not carry the path.

WHY THIS IS ONE MECHANISM AND NOT TWO SPECIAL CASES. The lane contract's words: *"This is the
same invisible-edge class as the module loaded by name that `safe_remove` declared SAFE — one
mechanism, two instances. Build it as one mechanism; if you find yourself writing a second
special case, stop and generalise."* The register already carried the first special case in
prose: `graph_queries.ORPHAN_DISPOSITIONS["scripts/provision_legs.py"]` said in as many words
that the file IS machine-triggered, that `.devcontainer/provision.sh` is the trigger, that the
enum simply does not list it, and that *"the underlying WIRING_SURFACES gap is a finding
against the enum"*. This is the enum fix that discharges the finding, so the disposition row
goes with it — a register entry for a file that now has a real edge would launder its own
subject (`test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`).

THE COST, MEASURED RATHER THAN ASSUMED, because the deferral above was made on a guess about
it: the worry recorded in that disposition was that widening the enum means *"every
`scripts/*.py` any shell script names stops being an orphan at once"*. It does not. The
widening is to the DECLARED PROVISIONING SURFACES — a closed, named tuple — not to shell
scripts as a class, and `test_widening_the_enum_moves_only_the_provisioning_chain` measures
exactly which nodes changed side.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import file_purpose_graph as fpg
import graph_queries as gq
import safe_remove as sr

REPO_ROOT = Path(__file__).resolve().parent.parent
PROVISION_SH = ".devcontainer/provision.sh"


# --- the enum ---------------------------------------------------------------------------------

def test_provisioning_is_a_declared_wiring_surface():
    """A container creation fires provisioning with no human deciding in the moment — which is
    the process-trigger census's OWN predicate for a wiring surface, applied consistently."""
    for rel in (PROVISION_SH, ".devcontainer/devcontainer.json"):
        assert rel in fpg.WIRING_SURFACES, f"{rel} is not a declared wiring surface"
        assert (REPO_ROOT / rel).is_file(), f"{rel} is declared but not on disk"


@pytest.mark.live_repo
def test_devcontainer_json_triggers_the_provisioning_script():
    """The chain's first hop. `onCreateCommand` / `postCreateCommand` / `postStartCommand` all
    read `bash .devcontainer/provision.sh`, so the JSON is a consumer of the script."""
    graph = fpg.build(REPO_ROOT)
    key = graph.key_for_path(PROVISION_SH)
    assert key, "provision.sh has no node"
    sources = {node.path for edge, node in graph.consumers(key)
               if edge.kind == fpg.EDGE_TRIGGERS}
    assert ".devcontainer/devcontainer.json" in sources, sources


@pytest.mark.live_repo
def test_provisioning_triggers_every_script_it_actually_calls():
    """The chain's second hop, and the one the census could not see.

    `scripts/provision_legs.py` is the file whose predecessor was deleted for looking like an
    orphan while six shell call sites named it. `scripts/arm_hooks.py`, `validate_backlog.py`
    and `gen_task_tree.py` are the other live call sites in the same script.
    """
    graph = fpg.build(REPO_ROOT)
    called = {node.path for edge, node in
              graph.edges_out(graph.key_for_path(PROVISION_SH))
              if edge.kind == fpg.EDGE_TRIGGERS}
    for expected in ("scripts/provision_legs.py", "scripts/arm_hooks.py",
                     "scripts/validate_backlog.py", "scripts/gen_task_tree.py",
                     "scripts/substrate_provenance.py"):
        assert expected in called, f"{expected} is called by provision.sh but has no edge"


@pytest.mark.live_repo
def test_the_provision_legs_disposition_is_discharged_not_carried():
    """The special case is REMOVED, not left beside the general mechanism.

    A disposition saying "this has no trigger the census can see" is false the moment the
    census can see it, and a register that contradicts the graph is worse than no register.
    """
    assert "scripts/provision_legs.py" not in gq.ORPHAN_DISPOSITIONS, (
        "provision_legs.py now has a real triggers edge; its ORPHAN_DISPOSITIONS row is a "
        "stale special case and must go with the enum fix that discharged it")


# --- the extractor: a comment is not a call site ------------------------------------------------

def _mini_repo(tmp_path: Path, provision_body: str) -> Path:
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / ".devcontainer").mkdir()
    (root / "scripts" / "widget.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / ".devcontainer" / "provision.sh").write_text(provision_body, encoding="utf-8")
    return root


def _shell_targets(root: Path) -> set[str]:
    modules = fpg._script_module_map(root)
    targets: set[str] = set()
    for value in fpg._surface_strings(root / ".devcontainer" / "provision.sh"):
        targets |= fpg._resolved_targets(value, modules, root, (".devcontainer",))
    return targets


def test_a_shell_call_site_is_read_as_an_edge(tmp_path):
    root = _mini_repo(tmp_path, "#!/usr/bin/env bash\nuv run python scripts/widget.py --check\n")
    assert "scripts/widget.py" in _shell_targets(root)


def test_a_comment_naming_a_script_does_NOT_manufacture_an_edge(tmp_path):
    """THE REASON THE CONFIG READERS PARSE RATHER THAN GREP, carried into the shell reader.

    `_config_strings`' own docstring states it: a text scan reads prose as call sites and
    manufactures triggers, *"which under-reports orphans, the exact direction an orphan census
    must never be wrong in."* `.devcontainer/provision.sh` is roughly half comment prose and
    names retired module paths ON PURPOSE as its own retirement record, so a naive grep over it
    would be worse here than anywhere else in the tree.
    """
    root = _mini_repo(tmp_path, (
        "#!/usr/bin/env bash\n"
        "# RETIRED: scripts/widget.py was removed at abc1234 and must not be called.\n"
        "echo done   # see scripts/widget.py for why\n"))
    assert _shell_targets(root) == set()


def test_an_unlexable_line_costs_only_that_line(tmp_path):
    """Fail-soft, but per LINE. Whole-file fail-soft would silently report zero edges for a
    script with one stray quote, and zero edges is the under-reporting direction."""
    root = _mini_repo(tmp_path, (
        "#!/usr/bin/env bash\n"
        "awk 'BEGIN { print \"unterminated\n"
        "uv run python scripts/widget.py\n"))
    assert "scripts/widget.py" in _shell_targets(root)


# --- the refusal ---------------------------------------------------------------------------------

def _no_referrers(symbol, module, repo_root, **kwargs):
    """A stub oracle that finds NOTHING — so any refusal below comes from the wiring leg."""
    return {"resolution": {"status": "resolved"}, "reverse_dependents": [],
            "provenance": {"completeness": "complete"}}


def test_retiring_a_file_provisioning_calls_is_REFUSED(tmp_path):
    """THE L3 ACCEPTANCE CRITERION, on a repo built for the purpose.

    The static importer oracle finds zero referrers — correctly, because there are none in
    Python. The shell call site is the whole referrer, and it is exactly the referrer whose
    invisibility cost a codespace a recovery container on 2026-09-14.
    """
    root = _mini_repo(tmp_path, "#!/usr/bin/env bash\nuv run python scripts/widget.py\n")

    verdict = sr.evaluate_removal(["scripts/widget.py"], root, oracle=_no_referrers)

    assert verdict.status == "unsafe", verdict.reason
    referrers = {r["referrer"] for r in verdict.surviving_referrers}
    assert ".devcontainer/provision.sh" in referrers, verdict.surviving_referrers


def test_retiring_a_file_provisioning_only_MENTIONS_is_allowed(tmp_path):
    """The inverse, so the refusal is a mechanism and not a blanket. A retirement record that
    names the file it retired must not keep the file alive forever."""
    root = _mini_repo(tmp_path, (
        "#!/usr/bin/env bash\n"
        "# scripts/widget.py was retired; this comment is the record, not a call.\n"
        "echo ok\n"))

    verdict = sr.evaluate_removal(["scripts/widget.py"], root, oracle=_no_referrers)

    assert verdict.status != "unsafe", verdict.reason


def test_co_removing_the_call_site_is_allowed(tmp_path):
    """Removing the script AND the surface that calls it is a legitimate retirement."""
    root = _mini_repo(tmp_path, "#!/usr/bin/env bash\nuv run python scripts/widget.py\n")

    verdict = sr.evaluate_removal(["scripts/widget.py", ".devcontainer/provision.sh"], root,
                                  oracle=_no_referrers)

    assert verdict.status != "unsafe", verdict.reason


def test_the_wiring_leg_is_not_a_provisioning_special_case(tmp_path):
    """ONE MECHANISM. The leg reads the GRAPH, so every wiring surface protects what it names —
    a pre-commit hook's `entry:` and a workflow's `run:` line get the same teeth, for free and
    without a second code path. Witnessed on a pre-commit config rather than on provisioning."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "widget.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / ".pre-commit-config.yaml").write_text(
        "repos:\n  - repo: local\n    hooks:\n      - id: w\n        name: w\n"
        "        entry: python scripts/widget.py\n        language: system\n", encoding="utf-8")

    verdict = sr.evaluate_removal(["scripts/widget.py"], root, oracle=_no_referrers)

    assert verdict.status == "unsafe", verdict.reason
    assert ".pre-commit-config.yaml" in {r["referrer"] for r in verdict.surviving_referrers}


@pytest.mark.live_repo
def test_retiring_provision_legs_from_the_LIVE_repo_is_REFUSED():
    """The same refusal against the real tree — the regression case, by name.

    `scripts/cloud_provisioning.py` was retired at `3c9418cc` on a static reading that said
    SAFE. Its successor carries the same shape. This is the test that would have stopped it.
    """
    verdict = sr.evaluate_removal(["scripts/provision_legs.py"], REPO_ROOT,
                                  oracle=_no_referrers)
    assert verdict.status == "unsafe", verdict.reason
    assert ".devcontainer/provision.sh" in {r["referrer"] for r in verdict.surviving_referrers}


# --- the measured cost of the widening ------------------------------------------------------------

@pytest.mark.live_repo
def test_widening_the_enum_moves_only_the_provisioning_chain():
    """The deferral that filed the disposition rested on a guess about blast radius. Measure it.

    Every node that gained a trigger from the two new surfaces is named here, so a later
    widening that quietly sweeps half of `scripts/` in cannot pass as this one.
    """
    graph = fpg.build(REPO_ROOT)
    gained: set[str] = set()
    for rel in (PROVISION_SH, ".devcontainer/devcontainer.json"):
        key = graph.key_for_path(rel)
        if key:
            gained |= {node.path for edge, node in graph.edges_out(key)
                       if edge.kind == fpg.EDGE_TRIGGERS and node.path}
    assert gained <= {
        ".devcontainer/provision.sh",
        "scripts/provision_legs.py",
        "scripts/arm_hooks.py",
        "scripts/validate_backlog.py",
        "scripts/gen_task_tree.py",
        "scripts/substrate_provenance.py",
    }, f"the widening reached further than the provisioning chain: {sorted(gained)}"
