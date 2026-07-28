"""Coverage for scripts/gen_task_tree.py.

[#433] STEP 1-2 (the verbatim split + byte-identity proofs) and [#439] STEP 3 (the
source-of-truth flip: tasks/ is the source, BACKLOG.md is generated).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_task_tree as gtt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKLOG = REPO_ROOT / "BACKLOG.md"
TREE = REPO_ROOT / "tasks"


def test_roundtrip_live_backlog_byte_identity():
    raw = BACKLOG.read_bytes()
    text = raw.decode("utf-8")
    model = gtt.parse_backlog(text)
    assert gtt.reassemble_from_model(model) == text
    assert gtt.reassemble_from_model(model).encode("utf-8") == raw


def test_disk_roundtrip_tmp_tree_byte_identity(tmp_path):
    """THE core acceptance test: live BACKLOG.md -> tree on disk -> byte-identical text."""
    raw = BACKLOG.read_bytes()
    text = raw.decode("utf-8")
    model = gtt.parse_backlog(text)
    out_dir = tmp_path / "tasks"
    gtt.write_tree(model, out_dir)
    result = gtt.reassemble_from_tree(out_dir)
    assert result == text
    assert result.encode("utf-8") == raw


def test_committed_tree_coherent_with_backlog():
    if not (TREE / "manifest.json").exists():
        pytest.skip("tasks/ not yet generated (module 3 commits it)")
    text = BACKLOG.read_bytes().decode("utf-8")
    assert gtt.reassemble_from_tree(TREE) == text


# --- [#439] the flip -------------------------------------------------------------

def test_emit_source_regenerates_backlog_byte_identically(tmp_path):
    """THE post-flip acceptance test, and the inverse of the STEP 1-2 one above: the tree
    is the source, so emitting must reproduce the live BACKLOG.md bytes exactly."""
    raw = BACKLOG.read_bytes()
    out_dir = tmp_path / "tasks"
    gtt.write_tree(gtt.parse_backlog(raw.decode("utf-8")), out_dir)
    target = tmp_path / "BACKLOG.md"
    assert gtt.main(["--emit-source", "--source", str(target), "--out", str(out_dir)]) == 0
    assert target.read_bytes() == raw


def test_emit_source_is_idempotent_and_leaves_a_current_file_alone(tmp_path):
    """A no-op regen must not rewrite the file: an mtime-only churn would show up as a
    working-tree diff and trip the coherence gate's index/worktree guard for no reason."""
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir, target = tmp_path / "tasks", tmp_path / "BACKLOG.md"
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    assert gtt.main(["--emit-source", "--source", str(target), "--out", str(out_dir)]) == 0
    first = target.stat().st_mtime_ns
    assert gtt.main(["--emit-source", "--source", str(target), "--out", str(out_dir)]) == 0
    assert target.stat().st_mtime_ns == first, "a current file must not be rewritten"


def test_emit_source_refuses_when_the_source_tree_is_missing(tmp_path):
    """Fail-closed: with no manifest there is no source of truth, so refuse rather than
    write an empty or half-built BACKLOG.md over a good one."""
    target = tmp_path / "BACKLOG.md"
    target.write_bytes(b"# real content\n")
    assert gtt.main(["--emit-source", "--source", str(target),
                     "--out", str(tmp_path / "nope")]) == 1
    assert target.read_bytes() == b"# real content\n", "must not clobber on refusal"


def test_check_reds_when_backlog_diverges_from_the_tree(tmp_path):
    """The flipped direction: the TREE is the expectation now."""
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir, source = tmp_path / "tasks", tmp_path / "BACKLOG.md"
    source.write_bytes(text.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    assert gtt.find_incoherences(source, out_dir) == []

    source.write_bytes((text + "a hand edit to the generated file\n").encode("utf-8"))
    problems = gtt.find_incoherences(source, out_dir)
    assert any("does not match what tasks/ generates" in p for p in problems), problems
    assert gtt.main(["--check", "--source", str(source), "--out", str(out_dir)]) == 1


def test_check_reds_on_frontmatter_that_disagrees_with_its_body(tmp_path):
    """The leg the flip made necessary. Frontmatter is DERIVED from the body, so in a
    source-of-truth file it is editable, inert, and — without this check — silently wrong.
    A hand-edited `status:` must RED rather than sit there looking authoritative."""
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir, source = tmp_path / "tasks", tmp_path / "BACKLOG.md"
    source.write_bytes(text.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    assert gtt.find_incoherences(source, out_dir) == []

    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    original = task_file.read_bytes().decode("utf-8")
    task_file.write_text(original.replace("status: open", "status: done", 1),
                         encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("frontmatter disagrees with its own body" in p for p in problems), problems


def test_check_reds_when_the_manifest_references_a_missing_file(tmp_path):
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir, source = tmp_path / "tasks", tmp_path / "BACKLOG.md"
    source.write_bytes(text.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    next(p for p in out_dir.iterdir() if p.name.startswith("1-")).unlink()
    problems = gtt.find_incoherences(source, out_dir)
    assert any("missing task file" in p for p in problems), problems


def test_task_files_carry_the_post_flip_provenance(tmp_path):
    """`source: BACKLOG.md` + `derived: true` were TRUE pre-flip and FALSE after it. The
    tree is the source now, so it says what it generates instead of what it came from."""
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir = tmp_path / "tasks"
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    body = next(p for p in out_dir.iterdir()
                if p.name.startswith("1-")).read_bytes().decode("utf-8")
    assert "generates: BACKLOG.md" in body
    assert "derived: true" not in body
    assert "source: BACKLOG.md" not in body


def _seed(tmp_path, text):
    out_dir, source = tmp_path / "tasks", tmp_path / "BACKLOG.md"
    source.write_bytes(text.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)])
    return source, out_dir


_TWO_THEMES = (
    "# T\n\n## [E1] One\n\n### [S1] Story\n- [#1] [P1][S] **A** — b\n"
    "\n## [E2] Two\n\n### [S2] Other\n- [#2] [P2][M] **B** — b\n"
)


def test_emit_source_refreshes_derived_frontmatter_after_a_body_edit(tmp_path):
    """terra P1 (2026-07-28) — the documented normal workflow could not reach green.

    Frontmatter is DERIVED from the body, so editing a task body (priority/size/status/
    title/deps) left it stale and the honesty leg RED-ed on exactly the edit the workflow
    asks for. The only escape was `--write`, the warned recovery direction. --emit-source
    now re-renders derived frontmatter as part of the regen; the BODY is never touched.
    """
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    assert gtt.find_incoherences(source, out_dir) == []

    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    original = task_file.read_bytes().decode("utf-8")
    task_file.write_text(original.replace("- [#1] [P1][S]", "- [#1] [P3][S]", 1),
                         encoding="utf-8", newline="\n")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 0
    assert gtt.find_incoherences(source, out_dir) == [], "the normal path must reach green"
    refreshed = task_file.read_bytes().decode("utf-8")
    assert "priority: P3" in refreshed, "derived frontmatter must follow the body"
    assert "- [#1] [P3][S]" in source.read_bytes().decode("utf-8")


def test_check_reds_on_a_stale_generated_sha256(tmp_path):
    """terra P1 — schema 2 advertises generated_sha256 as an integrity pin, but nothing
    validated it and --emit-source did not maintain it. An unchecked, unmaintained hash
    is decoration that drifts on the first edit and still reports green."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    manifest["generated_sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("generated_sha256" in p for p in problems), problems
    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 0
    assert gtt.find_incoherences(source, out_dir) == [], "--emit-source must re-pin it"


def test_check_reds_on_lineage_stale_against_manifest_placement(tmp_path):
    """terra P1 — theme/story were read back OUT of the task file, which made the honesty
    check tautological for them: move a task node under a different heading and the file's
    stale `theme:` still matched itself. Reassembly uses manifest PLACEMENT, not
    frontmatter, so the output leg passed too and the staleness survived both legs.
    Lineage is now derived from the manifest, which is its actual authority."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    assert gtt.find_incoherences(source, out_dir) == []

    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    nodes = manifest["nodes"]
    first_task = next(i for i, n in enumerate(nodes) if "task" in n)
    later_theme = next(i for i, n in enumerate(nodes)
                       if i > first_task and "prose" in n and n["prose"].startswith("## [E2]"))
    nodes.insert(later_theme, nodes.pop(first_task))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("manifest placement" in p for p in problems), problems


def test_lineage_from_manifest_matches_the_parser(tmp_path):
    """The lineage walker must agree with parse_backlog's heading/fence rules, or the
    honesty leg and the emitted tree would disagree about where a task lives."""
    import json
    _, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest = json.loads((out_dir / "manifest.json").read_bytes().decode("utf-8"))
    lineage = gtt.lineage_from_manifest(manifest)
    by_id = {row.id: row for kind, row in gtt.parse_backlog(_TWO_THEMES).nodes if kind == "task"}
    for fname, (theme, story) in lineage.items():
        row = by_id[gtt._id_from_filename(fname)]
        assert (theme, story) == (row.theme, row.story), fname


def test_check_reds_when_the_id_disagrees_across_filename_body_and_manifest(tmp_path):
    """terra P1 (2026-07-28, 2nd pass) — the expected frontmatter was rebuilt from the
    FILENAME alone, so editing a body's `[#N]` was invisible: expected id came from the
    filename, matched the unchanged actual, and the emitted BACKLOG.md carried the NEW id.
    File, manifest and document then disagreed about which id the task is, with every leg
    green. Identity is byte-exact (ADR-107 §2) and must agree in all three places."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    assert gtt.find_incoherences(source, out_dir) == []

    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    original = task_file.read_bytes().decode("utf-8")
    task_file.write_text(original.replace("- [#1] ", "- [#500] ", 1),
                         encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("task id disagrees across filename/body/manifest" in p for p in problems), problems


def test_check_reds_when_a_retired_id_is_re_issued(tmp_path):
    """terra P1 (2nd pass) — retire-not-delete only buys an allocation ledger if a spent id
    cannot come back. Unreferenced engine-managed files were skipped silently, so a retired
    `1-old.md` beside a new active `1-new.md` re-issued a spent id and the gate passed —
    defeating the exact guarantee §6.3 keeps those files for."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    active = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    # a RETIRED record (engine-managed, outside the manifest) holding the same id
    (out_dir / "1-a-retired-record.md").write_text(
        active.read_bytes().decode("utf-8"), encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("re-issued" in p and "[#1]" in p for p in problems), problems


def test_retired_record_with_a_distinct_id_stays_silent(tmp_path):
    """The complement: retirement itself must stay silent, or every closure REDs the gate."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    active = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    body = active.read_bytes().decode("utf-8").replace("[#1]", "[#77]")
    (out_dir / "77-a-retired-record.md").write_text(body, encoding="utf-8", newline="\n")
    assert gtt.find_incoherences(source, out_dir) == []


@pytest.mark.parametrize("evil", [
    "1-../../escaped.md", "../evil.md", "sub/1-x.md", "1-x\\..\\y.md", "", 42,
])
def test_manifest_filename_traversal_is_refused(tmp_path, evil):
    """terra P1 (2nd pass) — `file` values come from manifest.json, which the flip made a
    HAND-EDITED source artifact, and refresh_task_frontmatter WRITES through them. A
    traversing or malformed path would read and rewrite outside tasks/ during the ordinary
    --emit-source workflow. `_ORPHAN_RE` never guarded this: it walks real dirents, not
    manifest strings."""
    assert gtt.manifest_filename_problem(evil) is not None


def test_manifest_filename_accepts_a_normal_task_basename():
    assert gtt.manifest_filename_problem("439-adr-107-strangler-step-3.md") is None


def test_emit_source_refuses_a_traversing_manifest_path(tmp_path):
    """End-to-end: the guard must stop the WRITE path, not just exist as a helper."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    for node in manifest["nodes"]:
        if "task" in node:
            node["file"] = "1-../../escaped.md"
            break
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    assert not (tmp_path.parent / "escaped.md").exists()
    problems = gtt.find_incoherences(source, out_dir)
    assert any("unsafe manifest" in p for p in problems), problems


def test_check_reds_on_duplicate_ids_among_active_files(tmp_path):
    """terra P1 (4th pass) — ADR-107 §6.3's OWN named requirement: "a tasks/-level
    duplicate-id check makes a collision a gate failure at merge time rather than a silent
    one". This is the concurrent-branch collision the ADR records as a residual it does not
    PREVENT: two branches allocate the same next-free id, write differently-slugged files,
    and git merges them cleanly. Both can be internally consistent, so without this leg
    every other check passes and the collision ships."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    original = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    twin = out_dir / "1-a-colliding-sibling.md"
    twin.write_text(original.read_bytes().decode("utf-8"), encoding="utf-8", newline="\n")

    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    for i, node in enumerate(manifest["nodes"]):
        if node.get("file") == original.name:
            manifest["nodes"].insert(i + 1, {"task": 1, "file": twin.name})
            break
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("two ACTIVE task files" in p and "[#1]" in p for p in problems), problems


def test_emit_source_writes_nothing_when_the_plan_is_invalid(tmp_path):
    """terra P1 (4th pass) — rendering file-by-file-and-writing left the SOURCE OF TRUTH
    partially mutated when a later file was missing or malformed: earlier files were
    already rewritten, the command then failed, and the tree sat in neither the old state
    nor the new one. Tolerable for a derived tree; not for the source. Plan fully, then
    write."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    stale = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    # one file with STALE derived frontmatter (would be rewritten) ...
    stale.write_text(stale.read_bytes().decode("utf-8").replace("priority: P1", "priority: P9", 1),
                     encoding="utf-8", newline="\n")
    before = stale.read_bytes()
    # ... and another that is MALFORMED, so the plan must abort before any write
    broken = next(p for p in out_dir.iterdir() if p.name.startswith("2-"))
    broken.write_text("not a frontmattered task file at all\n", encoding="utf-8", newline="\n")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    assert stale.read_bytes() == before, "a failed regen must leave the source tree untouched"


@pytest.mark.parametrize("node", [
    {"prose": 7}, {"prose": None}, ["not", "an", "object"], 42,
    {"task": 1, "prose": "both"}, {}, {"task": "1", "file": "1-x.md"},
    {"task": True, "file": "1-x.md"}, {"task": 1, "file": "../escape.md"},
])
def test_malformed_manifest_nodes_are_rejected(node):
    """terra P1 (6th pass) — the manifest is HAND-EDITED source now, so "valid JSON" is
    not "valid manifest". `{"prose": 7}` raised AttributeError inside the heading walk and
    a non-object node raised TypeError; neither is in the exception set _cmd_emit_source or
    the audit gate catch, so a malformed source artifact CRASHED the regen and the
    ship-gate instead of reporting a controlled failure."""
    assert gtt.manifest_node_problem(node) is not None


def test_well_formed_manifest_nodes_are_accepted():
    assert gtt.manifest_node_problem({"prose": "## [E1] Theme"}) is None
    assert gtt.manifest_node_problem({"prose": ""}) is None
    assert gtt.manifest_node_problem({"task": 439, "file": "439-a-slug.md"}) is None


def test_malformed_manifest_is_a_controlled_failure_not_a_crash(tmp_path):
    """End-to-end: both the regen and the check must REPORT it, not raise."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    manifest["nodes"].insert(0, {"prose": 7})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    problems = gtt.find_incoherences(source, out_dir)   # must not raise
    assert any("prose node value is not a string" in p for p in problems), problems


def test_emit_source_rolls_back_a_torn_write(tmp_path, monkeypatch):
    """terra P1 (6th pass) — planning first covers DATA errors only. A mid-loop I/O
    failure (full disk, permissions) would still leave the source tree half-rewritten
    while BACKLOG.md and the hash never updated, which is exactly the state the
    plan-before-write guarantee claims to prevent."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    for p in out_dir.iterdir():                      # make EVERY task file need a refresh
        if p.name.endswith(".md"):
            p.write_text(p.read_bytes().decode("utf-8").replace("status: open", "status: x", 1),
                         encoding="utf-8", newline="\n")
    before = {p.name: p.read_bytes() for p in out_dir.iterdir() if p.name.endswith(".md")}
    assert len(before) >= 2, "need >=2 files so the failure can land mid-loop"

    real_write_text = Path.write_text
    calls = {"n": 0}

    def flaky(self, *a, **kw):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("simulated disk full")
        return real_write_text(self, *a, **kw)

    monkeypatch.setattr(Path, "write_text", flaky)
    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    monkeypatch.undo()

    after = {p.name: p.read_bytes() for p in out_dir.iterdir() if p.name.endswith(".md")}
    assert after == before, "a torn write must roll back to the prior bytes"


def test_manifest_declares_the_post_flip_direction(tmp_path):
    import json
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    out_dir = tmp_path / "tasks"
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_bytes().decode("utf-8"))
    assert manifest["schema"] == 2
    assert manifest["role"] == "source-of-truth"
    assert manifest["generates"] == "BACKLOG.md"
    assert "generated_sha256" in manifest
    assert "source_sha256" not in manifest, "schema-1 key must not linger with flipped meaning"


def test_live_parse_structural_properties():
    text = BACKLOG.read_bytes().decode("utf-8")
    model = gtt.parse_backlog(text)
    tasks = [row for kind, row in model.nodes if kind == "task"]
    ids = [t.id for t in tasks]
    assert len(ids) == len(set(ids))  # unique
    for t in tasks:
        assert t.raw.startswith(f"- [#{t.id}] ")
        assert t.theme is not None
        assert t.story is not None
    assert len(tasks) > 100  # no pin on the exact live count -- known test-smell avoidance


def test_fence_guard_synthetic():
    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme One",
            "",
            "### [S1] Story One",
            "- [#1] [P1][S] **Real task** — body text",
            "",
            "```",
            "- [#999] looks like a task",
            "## [E9] fenced theme-shaped line (must NOT pollute lineage)",
            "### [S9] fenced story-shaped line (must NOT pollute lineage)",
            "```",
            "",
            "| **R1** | x |",
            "",
            "- [#2] [P1][S] **Second task** — after the fence",
            "",
            "Footer text.",
            "",
        ]
    )
    model = gtt.parse_backlog(text)
    tasks = [row for kind, row in model.nodes if kind == "task"]
    ids = [t.id for t in tasks]
    assert ids == [1, 2]
    assert 999 not in ids
    assert tasks[0].theme == "[E1] Theme One"
    assert tasks[0].story == "[S1] Story One"
    # the fenced theme/story-shaped lines are prose: lineage carries across the fence
    assert tasks[1].theme == "[E1] Theme One"
    assert tasks[1].story == "[S1] Story One"
    assert gtt.reassemble_from_model(model) == text


def test_frontmatter_shape_and_body(tmp_path):
    raw = (
        "- [#42] [P2][M] **Bold title** — rest of description "
        "· serialize-group: audit-py · depends-on: 270 · DEFER — peg: x"
    )
    task = gtt.TaskRow(id=42, raw=raw, theme=None, story=None)
    model = gtt.Model(nodes=[("task", task)], source_text=raw)
    gtt.write_tree(model, tmp_path)

    fname = gtt.task_filename(task)
    file_text = (tmp_path / fname).read_bytes().decode("utf-8")
    lines = file_text.splitlines()

    assert 'id: "[#42]"' in lines
    assert "status: deferred" in lines
    assert "priority: P2" in lines
    assert "size: M" in lines
    assert "serialize-group: audit-py" in lines
    assert 'depends-on: "270"' in lines  # raw preserved, never normalized to "#270"

    assert gtt.extract_body(file_text) == raw
    assert file_text.endswith("\n")
    assert not file_text.endswith("\n\n")


def test_extract_body_rejects_malformed():
    with pytest.raises(ValueError):
        gtt.extract_body("---\nid: 1\nno closing fence in this text\n")
    with pytest.raises(ValueError):
        gtt.extract_body("id: 1\n---\n\nbody\n")


def test_crlf_rejected():
    with pytest.raises(ValueError):
        gtt.parse_backlog("a\r\nb")


def test_write_tree_never_deletes(tmp_path, capsys):
    out_dir = tmp_path / "tasks"
    out_dir.mkdir()
    (out_dir / "README.md").write_text("keep me\n", encoding="utf-8", newline="\n")
    (out_dir / "9999-stray.md").write_text("stray content\n", encoding="utf-8", newline="\n")
    (out_dir / "notes.txt").write_text("notes\n", encoding="utf-8", newline="\n")

    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme",
            "",
            "### [S1] Story",
            "- [#1] [P1][S] **A task** — body",
            "",
        ]
    )
    model = gtt.parse_backlog(text)
    gtt.write_tree(model, out_dir)

    assert (out_dir / "README.md").read_text(encoding="utf-8") == "keep me\n"
    assert (out_dir / "9999-stray.md").read_text(encoding="utf-8") == "stray content\n"
    assert (out_dir / "notes.txt").read_text(encoding="utf-8") == "notes\n"

    out = capsys.readouterr().out
    untouched = [line for line in out.splitlines() if "left untouched" in line]
    assert len(untouched) == 1
    assert "9999-stray.md" in untouched[0]
    # post-flip ([#439]) the report classifies: this one carries no provenance marker
    assert "FOREIGN file" in untouched[0]


def test_prune_is_refused_after_the_flip():
    """[#439] — --prune deleted retired task files. Post-flip those files ARE the source,
    so deleting one destroys source AND frees its id for re-issue, which is precisely what
    ADR-107 §6.3's retire-not-delete rule forbids. The verb refuses rather than lingering
    as a footgun, with or without --write."""
    assert gtt.main(["--prune"]) == 2
    assert gtt.main(["--write", "--prune"]) == 2


def test_retirement_keeps_the_file_and_stays_silent(tmp_path, capsys):
    """ADR-107 §6.3 retire-not-delete, realized: a task leaving the QUEUE drops out of
    manifest.json, and its file REMAINS as the allocation record that keeps its id spent.
    The coherence check must treat that as normal — if retirement RED-ed the gate, every
    closure would break the build."""
    out_dir = tmp_path / "tasks"
    source = tmp_path / "BACKLOG.md"
    two = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n- [#2] [P1][S] **Two** — b\n"
    source.write_bytes(two.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(two), out_dir)
    retired = gtt.task_filename(
        next(r for k, r in gtt.parse_backlog(two).nodes if k == "task" and r.id == 2))
    assert (out_dir / retired).exists()

    # retire [#2]: it leaves the queue, its file stays put
    one = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    source.write_bytes(one.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(one), out_dir)

    assert (out_dir / retired).exists(), "retire-not-delete: the allocation record must survive"
    assert gtt.find_incoherences(source, out_dir) == [], \
        "a retired allocation record is legitimate and must not RED the gate"
    assert "retired allocation record" in capsys.readouterr().out


def test_foreign_task_shaped_file_is_reported_not_silently_kept(tmp_path):
    """The flip side of the test above: silence is only for OUR retired records. A
    task-shaped file with no provenance marker is foreign and must still be surfaced,
    or 'retired' becomes a hiding place for anything."""
    out_dir = tmp_path / "tasks"
    source = tmp_path / "BACKLOG.md"
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    source.write_bytes(text.encode("utf-8"))
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    assert gtt.find_incoherences(source, out_dir) == []

    (out_dir / "7777-hand-authored.md").write_text("my own notes\n", encoding="utf-8", newline="\n")
    problems = gtt.find_incoherences(source, out_dir)
    assert any("foreign" in p.lower() and "7777" in p for p in problems), problems


def test_check_detects_body_corruption(tmp_path):
    source = tmp_path / "BACKLOG.md"
    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme",
            "",
            "### [S1] Story",
            "- [#1] [P1][S] **A task** — body",
            "",
        ]
    )
    source.write_bytes(text.encode("utf-8"))
    out_dir = tmp_path / "tasks"
    model = gtt.parse_backlog(text)
    gtt.write_tree(model, out_dir)

    task = next(row for kind, row in model.nodes if kind == "task")
    fname = gtt.task_filename(task)
    target = out_dir / fname
    corrupted = target.read_bytes().decode("utf-8").replace("body", "bidy")
    target.write_text(corrupted, encoding="utf-8", newline="\n")

    rc = gtt.main(["--check", "--source", str(source), "--out", str(out_dir)])
    assert rc == 1
