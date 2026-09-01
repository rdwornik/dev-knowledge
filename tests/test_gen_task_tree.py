"""Coverage for scripts/gen_task_tree.py.

[#433] STEP 1-2 (the verbatim split + byte-identity proofs), [#439] STEP 3 (the
source-of-truth flip: tasks/ is the source, BACKLOG.md is generated), and [#589] (the
generated file became a one-line-per-row PROJECTION of that source).

READ THIS BEFORE EDITING A BYTE-IDENTITY TEST HERE. Two texts exist now and they are not
interchangeable:

  * `canonical()` -- `reassemble_from_tree(TREE)`, the FULL-BODY text. This is what every
    byte-identity / losslessness proof in this file is about, and what `BACKLOG.md` held on
    disk until [#589]. Those proofs did not weaken; their subject stopped being a file.
  * `BACKLOG.md` -- the committed PROJECTION, one line per row. Byte-identity claims about
    it are claims about `render_view`, never about losslessness.

Pointing a losslessness test at `BACKLOG.md` post-[#589] still PASSES -- `parse_backlog`
preserves whatever lines it is handed, so the projection round-trips trivially -- while
proving nothing at all. That is the trap this note exists to name.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest


import gen_task_tree as gtt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKLOG = REPO_ROOT / "BACKLOG.md"
TREE = REPO_ROOT / "tasks"


def canonical() -> str:
    """The live tree's FULL-BODY text — what BACKLOG.md held before [#589]."""
    return gtt.reassemble_from_tree(TREE)


def test_roundtrip_live_canonical_byte_identity():
    """[#589] re-pointed this from BACKLOG.md to the canonical text — see the module note."""
    text = canonical()
    model = gtt.parse_backlog(text)
    assert gtt.reassemble_from_model(model) == text
    assert gtt.reassemble_from_model(model).encode("utf-8") == text.encode("utf-8")


def test_disk_roundtrip_tmp_tree_byte_identity(tmp_path):
    """THE core acceptance test: canonical text -> tree on disk -> byte-identical text."""
    text = canonical()
    model = gtt.parse_backlog(text)
    out_dir = tmp_path / "tasks"
    gtt.write_tree(model, out_dir)
    result = gtt.reassemble_from_tree(out_dir)
    assert result == text
    assert result.encode("utf-8") == text.encode("utf-8")


def test_committed_view_is_what_the_tree_projects():
    """The post-[#589] coherence claim: BACKLOG.md on disk == `render_view(tasks/)`.

    This is the byte-identity that still concerns a FILE. Its full-body counterpart is
    `test_roundtrip_live_canonical_byte_identity` above.
    """
    if not (TREE / "manifest.json").exists():
        pytest.skip("tasks/ not yet generated (module 3 commits it)")
    assert gtt.render_view(TREE) == BACKLOG.read_bytes().decode("utf-8")


# --- [#439] the flip -------------------------------------------------------------

def test_emit_source_regenerates_backlog_byte_identically(tmp_path):
    """THE post-flip acceptance test, and the inverse of the STEP 1-2 one above: the tree
    is the source, so emitting must reproduce the live BACKLOG.md bytes exactly.

    [#589] changed BOTH halves of this test, and the second change is the interesting one.
    What must come back out is now the PROJECTION — the committed file. And the tree can no
    longer be rebuilt by importing the canonical text: `write_tree` re-derives each filename
    from its title, so a title edited since the file was created yields a DIFFERENT slug, and
    the projection carries that filename in every row's pointer. A re-imported tree therefore
    projects real, correct rows with different pointers. Copying the live tree keeps the
    filenames the live view actually cites, which is what makes this an end-to-end proof
    rather than a proof about a tree nobody has.
    """
    out_dir = tmp_path / "tasks"
    shutil.copytree(TREE, out_dir)
    target = tmp_path / "BACKLOG.md"
    assert gtt.main(["--emit-source", "--source", str(target), "--out", str(out_dir)]) == 0
    assert target.read_bytes() == BACKLOG.read_bytes()


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
    # [#589]: the gate compares BACKLOG.md against `render_view`, so the clean baseline
    # must be EMITTED, not hand-written as full-body text (`_seed` does exactly that).
    source, out_dir = _seed(tmp_path, text)
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
    # [#589]: the gate compares BACKLOG.md against `render_view`, so the clean baseline
    # must be EMITTED, not hand-written as full-body text (`_seed` does exactly that).
    source, out_dir = _seed(tmp_path, text)
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
    body = (active.read_bytes().decode("utf-8")
            .replace("[#1]", "[#77]")
            .replace("status: open", "status: closed", 1))   # terminal, per ADR-107 §6.3
    (out_dir / "77-a-retired-record.md").write_text(body, encoding="utf-8", newline="\n")
    assert gtt.find_incoherences(source, out_dir) == []


def test_check_reds_when_a_retired_record_disagrees_about_its_own_id(tmp_path):
    """terra P1 (14th pass) — retired records were trusted on FILENAME alone while active
    files had all three ids cross-checked. A retired `77-old.md` whose body and frontmatter
    say [#78] registered 77 as spent while actually holding 78, so an active [#78] was not
    caught as re-issued. A record whose whole job is keeping an id spent must be right
    about which id."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    active = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    body = (active.read_bytes().decode("utf-8")
            .replace("[#1]", "[#78]")                       # body + frontmatter say 78
            .replace("status: open", "status: closed", 1))
    (out_dir / "77-a-lying-record.md").write_text(body, encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("does not state its id consistently" in p for p in problems), problems


def test_check_reds_on_a_retired_record_still_marked_open(tmp_path):
    """terra P1 (13th pass) — pass 12 made "mark it terminal" a documented INSTRUCTION but
    not an enforced one, which by this repo's own "no organ = decoration" rule is prose. An
    interrupted retirement left the record `status: open` and --check passed, so a closed
    task went on looking actionable to every consumer of the tree."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    active = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    body = active.read_bytes().decode("utf-8").replace("[#1]", "[#78]")   # left status: open
    (out_dir / "78-an-incomplete-retirement.md").write_text(body, encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("not marked terminal" in p for p in problems), problems


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
    # WHICH leg catches it is an implementation detail — after the 7th-pass split the
    # manifest-level "id referenced more than once" check fires first, which is strictly
    # more precise. What must hold is that the collision cannot ship.
    assert any("[#1]" in p and ("more than once" in p or "two ACTIVE task files" in p)
               for p in problems), problems


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


def test_check_reds_when_the_manifest_references_a_file_twice(tmp_path):
    """terra P1 (7th pass) — collapsing repeats into one dict entry hid them. Reassembly
    emits the body at EVERY occurrence, so a file referenced twice duplicates the task line
    in BACKLOG.md while the ledger leg counts it once, and the whole thing hashes green."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    dup = next(n for n in manifest["nodes"] if "task" in n)
    manifest["nodes"].append(dict(dup))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("same task file twice" in p for p in problems), problems


def test_emit_source_refuses_to_write_a_corrupt_identity(tmp_path):
    """terra P1 (7th pass) — the regen validated nothing. A body edited to a disagreeing id
    was written straight into BACKLOG.md, the hash re-pinned to the corruption, exit 0 —
    and only a LATER --check noticed what the command had already done. A regen cannot fix
    an identity break, so it must refuse rather than propagate it."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    before = source.read_bytes()
    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    task_file.write_text(task_file.read_bytes().decode("utf-8").replace("- [#1] ", "- [#500] ", 1),
                         encoding="utf-8", newline="\n")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    assert source.read_bytes() == before, "a refused regen must not touch BACKLOG.md"


def test_emit_source_rolls_back_a_failed_backlog_write(tmp_path, monkeypatch):
    """terra P1 (7th pass) — the 6th-pass rollback covered only task-frontmatter writes.
    BACKLOG.md and manifest.json (now SOURCE) were written unguarded and in-place, so a
    failure there could leave the artifacts inconsistent or the manifest truncated."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    # a body edit: forces a frontmatter refresh AND a BACKLOG.md rewrite AND a re-pin
    task_file.write_text(task_file.read_bytes().decode("utf-8").replace("[P1][S]", "[P3][S]", 1),
                         encoding="utf-8", newline="\n")
    before = {p: p.read_bytes() for p in (source, manifest_path, task_file)}

    real_write_text = Path.write_text

    def flaky(self, *a, **kw):
        if self.name == source.name:            # fail exactly on the BACKLOG.md write
            raise OSError("simulated disk full")
        return real_write_text(self, *a, **kw)

    monkeypatch.setattr(Path, "write_text", flaky)
    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1
    monkeypatch.undo()

    for path, original in before.items():
        assert path.read_bytes() == original, f"{path.name} must be restored"


@pytest.mark.parametrize("root", ["[1, 2]", "null", '"a string"', "42"])
def test_non_object_manifest_root_is_a_controlled_failure(tmp_path, root):
    """terra P1 (8th pass) — a valid-JSON root that is not an object made `.get` raise
    AttributeError, crashing both the regen and the ship-gate instead of reporting."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    (out_dir / "manifest.json").write_text(root + "\n", encoding="utf-8", newline="\n")
    problems = gtt.find_incoherences(source, out_dir)      # must not raise
    assert any("root is not an object" in p for p in problems), problems
    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 1


def test_check_reds_on_a_multiline_task_body(tmp_path):
    """terra P1 (8th pass) — _TASK_RE validates only the FIRST line while the frontmatter
    render and reassembly preserve the whole body, so extra physical lines rode into
    BACKLOG.md as prose that never passed through manifest.json — the authoritative
    carrier for every non-task line (ADR-107 §2)."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    task_file = next(p for p in out_dir.iterdir() if p.name.startswith("1-"))
    text = task_file.read_bytes().decode("utf-8")
    task_file.write_text(text.rstrip("\n") + "\nsmuggled prose line\n",
                         encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("spans multiple lines" in p for p in problems), problems


def test_write_import_rolls_back_a_torn_write(tmp_path, monkeypatch):
    """terra P1 (8th pass) — --write rewrites the SOURCE post-flip, so an I/O failure
    partway through would leave the authoritative tree half-rewritten: the documented
    recovery command making things worse than the state it was run to repair."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    before = {p.name: p.read_bytes() for p in out_dir.iterdir()}
    assert len(before) >= 3, "need several files so the failure lands mid-loop"

    real_write_text = Path.write_text
    calls = {"n": 0}

    def flaky(self, *a, **kw):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("simulated disk full")
        return real_write_text(self, *a, **kw)

    monkeypatch.setattr(Path, "write_text", flaky)
    with pytest.raises(OSError):
        gtt.write_tree(gtt.parse_backlog(source.read_bytes().decode("utf-8")), out_dir)
    monkeypatch.undo()

    after = {p.name: p.read_bytes() for p in out_dir.iterdir()}
    assert after == before, "a torn import must roll back to the prior bytes"


def test_emit_source_regenerates_over_a_non_utf8_output(tmp_path):
    """terra P1 (9th pass) — an existing BACKLOG.md containing invalid UTF-8 made the
    decode raise BEFORE any write, so the one command able to REPAIR the derived artifact
    was the one command that could not run. Undecodable output is simply stale."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    expected = source.read_bytes()
    source.write_bytes(b"\xff\xfe not valid utf-8 \xff")

    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 0
    assert source.read_bytes() == expected, "regen must repair the corrupt output"
    assert gtt.find_incoherences(source, out_dir) == []


def test_check_reds_on_a_task_row_smuggled_into_manifest_prose(tmp_path):
    """terra P1 (12th pass) — a task-shaped line placed in a `prose` node reassembles into
    BACKLOG.md as a REAL task row while having no managed task file, so it bypasses the id
    ledger entirely: --check, the output hash and duplicate-id enforcement all stay green
    over a row the tree does not know exists."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    manifest["nodes"].append({"prose": "- [#999] [P1][S] **Smuggled** — no task file"})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("is a TASK row" in p for p in problems), problems


def test_fenced_task_shaped_prose_is_still_legitimate(tmp_path):
    """The complement — inside a fenced block `- [#N]` IS prose, which is exactly what
    parse_backlog does. The check must not flag documentation that quotes the row format."""
    fenced = (
        "# T\n\n## [E1] One\n\n### [S1] Story\n- [#1] [P1][S] **A** — b\n\n"
        "```\n- [#123] [P1][S] **Quoted example** — not a real row\n```\n"
    )
    source, out_dir = _seed(tmp_path, fenced)
    assert gtt.find_incoherences(source, out_dir) == []


def test_check_reds_on_a_multiline_prose_node(tmp_path):
    """One node is one physical line, or the line model quietly stops being one-per-line."""
    import json
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    manifest["nodes"].append({"prose": "line one\nline two"})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")

    problems = gtt.find_incoherences(source, out_dir)
    assert any("spans multiple physical lines" in p for p in problems), problems


def test_check_reports_rather_than_crashes_on_a_non_utf8_output(tmp_path):
    """terra P1 (10th pass) — the symmetric half of the pass-9 fix, which I applied only to
    --emit-source: --check still decoded the output under an `except OSError` handler, so
    the VERIFICATION path traceback'd on exactly the state the REGEN path had just learned
    to repair. A corrupt output is a coherence failure to report, not an exception."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    source.write_bytes(b"\xff\xfe not valid utf-8 \xff")

    problems = gtt.find_incoherences(source, out_dir)      # must not raise
    assert any("cannot read generated file" in p for p in problems), problems
    assert gtt.main(["--check", "--source", str(source), "--out", str(out_dir)]) == 1


def test_emit_source_rolls_back_on_keyboard_interrupt(tmp_path, monkeypatch):
    """terra P1 (9th pass) — a Ctrl+C landing mid-write raises KeyboardInterrupt, which an
    `except OSError` rollback does not catch, leaving the SOURCE OF TRUTH partially written
    by the very handler meant to prevent that. The interrupt must still propagate."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    for p in out_dir.iterdir():
        if p.name.endswith(".md"):
            p.write_text(p.read_bytes().decode("utf-8").replace("status: open", "status: x", 1),
                         encoding="utf-8", newline="\n")
    before = {p.name: p.read_bytes() for p in out_dir.iterdir()}

    real_write_text = Path.write_text
    calls = {"n": 0}

    def interrupted(self, *a, **kw):
        calls["n"] += 1
        if calls["n"] == 2:
            raise KeyboardInterrupt
        return real_write_text(self, *a, **kw)

    monkeypatch.setattr(Path, "write_text", interrupted)
    with pytest.raises(KeyboardInterrupt):
        gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)])
    monkeypatch.undo()

    assert {p.name: p.read_bytes() for p in out_dir.iterdir()} == before


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
    assert "retired allocation record" in capsys.readouterr().out

    # The IMPORT path leaves the record `status: open`. ADR-107 §6.3 wants it TERMINAL, and
    # since the 13th-pass fix that is enforced rather than merely documented — so the
    # documented retirement (manifest node out + mark terminal) is the conforming route.
    stale = gtt.find_incoherences(source, out_dir)
    assert any("not marked terminal" in p for p in stale), stale

    rec = out_dir / retired
    rec.write_text(rec.read_bytes().decode("utf-8").replace("status: open", "status: closed", 1),
                   encoding="utf-8", newline="\n")
    # [#589]: the two DERIVED artifacts (the projection + the manifest hash pin) are stale
    # after the direct `write_tree` above, and both are gate legs. Emitting once — the
    # documented retirement route — brings them current without touching the record.
    assert gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)]) == 0
    assert gtt.find_incoherences(source, out_dir) == [], \
        "a properly-retired allocation record is legitimate and must not RED the gate"


def test_foreign_task_shaped_file_is_reported_not_silently_kept(tmp_path):
    """The flip side of the test above: silence is only for OUR retired records. A
    task-shaped file with no provenance marker is foreign and must still be surfaced,
    or 'retired' becomes a hiding place for anything."""
    text = "# T\n\n## [E1] Theme\n\n### [S1] Story\n- [#1] [P1][S] **One** — b\n"
    # [#589]: the gate compares BACKLOG.md against `render_view`, so the clean baseline
    # must be EMITTED, not hand-written as full-body text (`_seed` does exactly that).
    source, out_dir = _seed(tmp_path, text)
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


# --- [#474] the --write guard: warn-then-destroy inverted to warned-means-abort ----------
def _files_snapshot(out_dir):
    if not out_dir.exists():
        return {}
    return {p.name: p.read_bytes() for p in sorted(out_dir.iterdir()) if p.is_file()}


def test_write_refuses_against_a_populated_tree(tmp_path, capsys):
    """FR1 — a warned state ABORTS before touching the source of truth: non-zero exit,
    warning(s) printed, ZERO bytes changed on disk (the [#473] incident class: an
    accidental --write re-slugged 17 task filenames and orphaned the originals)."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    # [#589]: `_seed` leaves the PROJECTION on disk, which trips the earlier, unoverridable
    # view refusal. Restore a full-body source so this test still exercises the condition it
    # is named for (the view refusal has its own test below).
    source.write_bytes(_TWO_THEMES.encode("utf-8"))
    before_tree = _files_snapshot(out_dir)
    before_source = source.read_bytes()

    rc = gtt.main(["--write", "--source", str(source), "--out", str(out_dir)])
    err = capsys.readouterr().err

    assert rc == 2
    assert "REFUSED" in err and "nothing written" in err
    assert "--force" in err  # the refusal names its escape hatch
    assert "--emit-source" in err  # ...and the routine direction
    assert _files_snapshot(out_dir) == before_tree, "a refused --write must change zero bytes"
    assert source.read_bytes() == before_source


def test_default_invocation_is_nonmutating(tmp_path):
    """FR2 — the no-flag default never mutates: byte-identical tree + source after."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    before_tree = _files_snapshot(out_dir)
    before_source = source.read_bytes()

    rc = gtt.main(["--source", str(source), "--out", str(out_dir)])

    assert rc == 2  # no verb -> usage, loudly non-zero (never a silent partial action)
    assert _files_snapshot(out_dir) == before_tree
    assert source.read_bytes() == before_source


def test_force_overrides_a_warned_write_and_names_the_override(tmp_path, capsys):
    """FR3 — the escape hatch works, is loud, and NAMES what it is overriding."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    # Make the import observable: retitle task #1 so the derived filename changes.
    source.write_bytes(_TWO_THEMES.replace("**A**", "**A retitled**").encode("utf-8"))

    rc = gtt.main(["--write", "--force", "--source", str(source), "--out", str(out_dir)])
    err = capsys.readouterr().err

    assert rc == 0
    assert "--force" in err and "OVERRIDE" in err
    assert "manifest.json" in err  # the overridden condition is named, not just counted
    new_files = _files_snapshot(out_dir)
    assert any("retitled" in name for name in new_files), "the forced import must have run"


def test_clean_state_write_is_unchanged(tmp_path, capsys):
    """FR4 — zero warning conditions (bootstrap into an absent tree): --write behaves
    exactly as today — same files, same bytes as a direct write_tree of the source."""
    source = tmp_path / "BACKLOG.md"
    source.write_bytes(_TWO_THEMES.encode("utf-8"))
    out_dir = tmp_path / "tasks"

    rc = gtt.main(["--write", "--source", str(source), "--out", str(out_dir)])
    err = capsys.readouterr().err

    assert rc == 0
    assert "REFUSED" not in err
    ref_dir = tmp_path / "ref"
    gtt.write_tree(gtt.parse_backlog(_TWO_THEMES), ref_dir)
    assert _files_snapshot(out_dir) == _files_snapshot(ref_dir)


def test_force_without_write_is_refused_loudly():
    """--force is only meaningful with --write; alone it must error, never no-op."""
    with pytest.raises(SystemExit) as exc:
        gtt.main(["--force", "--check"])
    assert exc.value.code == 2


def test_check_cli_contract_on_committed_state():
    """FR5 — the handoff gate depends on `--check` exiting 0 on the committed state."""
    if not (TREE / "manifest.json").exists():
        pytest.skip("tasks/ not yet generated")
    assert gtt.main(["--check"]) == 0


# --- [#566] the ranking axis (the accepted [#488] LEAN) ---------------------------

def _rank_line(task_id, priority, group=None, title=None, defer=False):
    """One synthetic task line in the shape the live tree uses."""
    tail = f" · serialize-group: {group}" if group else ""
    tail += " · DEFER — peg: x" if defer else ""
    return f"- [#{task_id}] [{priority}][S] **{title or f'Task {task_id}'}** — body{tail}"


def _rank_doc(lines):
    return "# T\n\n## [E1] One\n\n### [S1] Story\n" + "\n".join(lines) + "\n"


def _ranked_ids(lines):
    model = gtt.parse_backlog(_rank_doc(lines))
    rows = [row for kind, row in model.nodes if kind == "task"]
    return [r.id for r in gtt.rank_tasks(rows)]


def test_rank_pins_the_ordering_of_a_seeded_tie_block():
    """THE done-clause acceptance test ([#566]): a seeded tie block comes out in ONE
    pinned order, and each of the three keys is the thing that decides a step of it.

    Seeded so every key is exercised and none is redundant:
      * #10 is P1 with zero contention — the P key outranks a 3-contention P2.
      * #21/#22/#23 all tie at P2 and are separated ONLY by contention (3 > 1 > 0).
      * #30/#31 tie at P2 AND at contention 1 — the id/age floor breaks what remains.
    """
    lines = [
        _rank_line(31, "P2", group="beta"),
        _rank_line(23, "P2"),
        _rank_line(21, "P2", group="alpha"),
        _rank_line(30, "P2", group="beta"),
        _rank_line(22, "P2", group="gamma"),
        _rank_line(10, "P1"),
        _rank_line(24, "P2", group="alpha"),
        _rank_line(25, "P2", group="alpha"),
        _rank_line(26, "P2", group="alpha"),
        _rank_line(27, "P2", group="gamma"),
        _rank_line(40, "P3", group="alpha"),
    ]
    # alpha holds 5 open rows (contention 4), gamma 2 (contention 1), beta 2 (1).
    assert _ranked_ids(lines) == [10, 21, 24, 25, 26, 22, 27, 30, 31, 23, 40]


def test_rank_priority_stays_the_primary_key():
    """The LEAN layers contention UNDER [P1..P3]; a huge group never lifts a P3."""
    big = [_rank_line(100 + n, "P3", group="huge") for n in range(40)]
    assert _ranked_ids([*big, _rank_line(999, "P1")])[0] == 999


def test_contention_is_group_size_minus_one_and_zero_when_ungrouped():
    """The prework's worked-example shape: the largest group's members score
    (size - 1) — 41 for the live 42-member `audit-py` — and an ungrouped row scores 0."""
    lines = [_rank_line(n, "P2", group="audit-py") for n in range(1, 43)]
    lines.append(_rank_line(500, "P2"))
    model = gtt.parse_backlog(_rank_doc(lines))
    rows = [row for kind, row in model.nodes if kind == "task"]
    scores = gtt.contention_scores(rows)
    assert scores[1] == 41
    assert scores[500] == 0


def test_rank_excludes_deferred_rows_and_scores_contention_over_the_open_ones():
    """A deferred row is out of the queue by operator decision, so it is neither ranked
    nor counted as contending — otherwise a mostly-deferred group inflates its members."""
    lines = [
        _rank_line(1, "P2", group="g"),
        _rank_line(2, "P2", group="g", defer=True),
        _rank_line(3, "P2", group="g", defer=True),
        _rank_line(4, "P2", group="g"),
    ]
    model = gtt.parse_backlog(_rank_doc(lines))
    rows = [row for kind, row in model.nodes if kind == "task"]
    ranked = gtt.rank_tasks(rows)
    assert [r.id for r in ranked] == [1, 4]
    assert [r.contention for r in ranked] == [1, 1], "2 open members, not 4"


def test_rank_sorts_an_unprioritized_row_after_every_p3():
    """A row with no [P#] must not sort into P1 by accident."""
    assert _ranked_ids([
        "- [#7] **No priority field** — body",
        _rank_line(8, "P3"),
    ]) == [8, 7]


def test_rank_cli_reads_the_source_tree_and_writes_nothing(tmp_path, capsys):
    """The verb is a REPORT: exit 0, ranking on stdout, zero bytes changed anywhere."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    before_tree, before_source = _files_snapshot(out_dir), source.read_bytes()

    rc = gtt.main(["--rank", "--source", str(source), "--out", str(out_dir)])
    out = capsys.readouterr().out

    assert rc == 0
    assert "2 open task(s) ranked" in out
    assert "1. [#1]" in out and "2. [#2]" in out  # P1 before P2
    assert _files_snapshot(out_dir) == before_tree
    assert source.read_bytes() == before_source


def test_rank_top_truncates_and_says_how_many_it_hid():
    """A truncated report must never read as the whole queue."""
    ranked = gtt.rank_tasks([
        gtt.TaskRow(id=n, raw=_rank_line(n, "P2"), theme=None, story=None)
        for n in range(1, 6)])
    text = gtt.render_ranking(ranked, top=2)
    assert "1. [#1]" in text and "2. [#2]" in text
    assert "[#3]" not in text
    assert "3 more not shown" in text
    assert "5 open task(s) ranked" in text


def test_rank_top_is_guarded_by_the_cli():
    """--rank-top is meaningless alone and meaningless at zero; both must error loudly."""
    for argv in (["--rank-top", "5"], ["--rank", "--rank-top", "0"]):
        with pytest.raises(SystemExit) as exc:
            gtt.main(argv)
        assert exc.value.code == 2


def test_rank_reports_rather_than_crashes_on_a_broken_tree(tmp_path, capsys):
    """A report must not traceback on a tree `--check` would simply RED."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    (out_dir / "manifest.json").write_text("{ not json", encoding="utf-8", newline="\n")

    rc = gtt.main(["--rank", "--source", str(source), "--out", str(out_dir)])
    err = capsys.readouterr().err

    assert rc == 1
    assert "rank FAIL" in err and "nothing written" in err


def test_rank_reports_the_live_queue():
    """The committed tree ranks without error, and the report is honest about scope."""
    if not (TREE / "manifest.json").exists():
        pytest.skip("tasks/ not yet generated")
    rows = [row for kind, row in gtt.parse_backlog(BACKLOG.read_bytes().decode("utf-8")).nodes
            if kind == "task"]
    ranked = gtt.rank_tasks(rows)
    assert 0 < len(ranked) <= len(rows)
    assert [r.rank for r in ranked] == list(range(1, len(ranked) + 1))
    priorities = [gtt._PRIORITY_RANK.get(r.priority, gtt._UNPRIORITIZED_RANK) for r in ranked]
    assert priorities == sorted(priorities), "the P key must never be violated"


# --- [#589] the view projection + its size assertions ----------------------------

def test_the_live_view_is_under_the_589_done_when_byte_bar():
    """[#589]'s measured claim, asserted rather than left in a closed row.

    Measured at the flip (2026-08-26, 202 rows): 279,814 B -> 66,526 B, a 76% cut.

    RE-BASELINED 2026-09-01 TO 72,000 AFTER A GROOMING PASS, ON THE ARCHITECT'S RULING, and
    the arithmetic is here because the row this asserts says the assertion may not be
    SILENTLY undone. It bound, which this docstring already called the point rather than a
    broken test, and it named the two lawful answers: groom, or re-baseline deliberately.
    Both were taken, in that order.

        corpus at the 2026-09-01 groom   70,276 B   223 rows
          row lines                      32,383 B   mean 145 B/row
          scaffolding (themes/stories/prose)        37,893 B  -- 54% of the file
        old bar                          70,000 B   -> breached by 276 B
        new bar                          72,000 B   -> 1,724 B headroom, ~11 rows

    THE GROOM CAME FIRST AND FOUND NOTHING TO CLOSE, which is why re-baselining is the
    remaining move rather than the easy one. Zero manifest nodes carried a terminal status;
    the tree was coherent; and all three STRONG closure candidates FAILED content
    verification -- #430 is open on half (b) (ship-gate determinism) with only half (a)
    landed, #554's Done-when needs `pytest -m 'not slow'` in-container and a VPS
    `devcontainer up` that no receipt shows, and #614 was a false positive from this arc's
    own reference tags. Closing a row to buy bytes is closing undone work.

    ONLY THE POINT-IN-TIME TOTAL MOVES. `_VIEW_ROW_BYTE_CEILING` -- the per-row, growth-proof
    half that `find_incoherences` enforces on every commit -- is untouched, as is the 100,000
    per-commit gate in `gen_task_tree.py`, which sits deliberately above this bar so ordinary
    queue growth can never wedge a commit.
    """
    assert len(BACKLOG.read_bytes()) < 72_000


def test_the_view_is_one_line_per_row_and_carries_no_bodies():
    """The projection's shape, checked on the live file rather than on the renderer."""
    rows = [line for line in BACKLOG.read_text(encoding="utf-8").split("\n")
            if gtt._TASK_RE.match(line)]
    assert rows, "the live view must carry rows"
    # No `Done when:` in the LIVE view is a fact about today's corpus, asserted here because
    # it is worth knowing if it changes — but deliberately NOT a gate (a title may legitimately
    # contain the words; `view_problems` carries no such leg, see its docstring).
    assert not any("Done when:" in line for line in rows), \
        "a Done-when clause in the live view is worth a look — is it a title, or a leaked body?"
    assert all(gtt.is_projected_row(line) for line in rows), \
        "every row must have the projection shape and end at a resolvable pointer"
    for line in rows:
        pointer = line.rsplit(" \u00b7 ", 1)[1]
        assert (REPO_ROOT / pointer).is_file(), f"unresolvable pointer: {pointer}"


def test_every_projected_row_is_derivable_back_to_its_body():
    """No information loss: id, band and status on the line agree with the body it points
    at, and the body is reachable. This is the [#589] done-when's 'every field the old view
    rendered is either in the new line or reachable from its pointer', checked per row."""
    for kind, row in gtt.parse_backlog(BACKLOG.read_text(encoding="utf-8")).nodes:
        if kind != "task":
            continue
        pointer = row.raw.rsplit(" \u00b7 ", 1)[1]
        file_text = (REPO_ROOT / pointer).read_text(encoding="utf-8")
        body = gtt.extract_body(file_text)
        assert gtt.frontmatter_id(file_text) == row.id
        assert gtt.derive_priority(row.raw) == gtt.derive_priority(body)
        assert gtt.derive_size(row.raw) == gtt.derive_size(body)
        assert gtt.derive_status(row.raw) == gtt.derive_status(body)


def test_check_fails_on_a_deliberately_inflated_view(tmp_path):
    """THE size assertion, planted: an inflated committed view must FAIL `--check`.

    The plant is a real re-inflation -- the full body written back onto the row line, which
    is exactly what a regression to `reassemble_from_tree` as the emit target would produce.
    """
    text = ("# T\n\n## [E1] Theme\n\n### [S1] Story\n"
            "- [#1] [P1][S] **One** \u2014 " + "x" * 900 + " \u00b7 Done when: it is done\n")
    source, out_dir = _seed(tmp_path, text)
    assert gtt.find_incoherences(source, out_dir) == []

    source.write_text(gtt.reassemble_from_tree(out_dir), encoding="utf-8", newline="\n")
    problems = gtt.find_incoherences(source, out_dir)
    assert any("per-row ceiling" in p and "on disk" in p for p in problems), problems
    assert gtt.main(["--check", "--source", str(source), "--out", str(out_dir)]) == 1


def test_the_size_assertion_measures_the_generated_bytes_too():
    """Both faces, so a renderer regression is caught even where the file agrees with it."""
    long_row = "- [#1] [P1][S] **One** \u2014 " + "x" * 900 + " \u00b7 Done when: done"
    over = gtt.view_problems(long_row + "\n", "the generated view")
    assert any("per-row ceiling" in p and "the generated view" in p for p in over)
    assert gtt.view_problems("- [#1] [P1][S] Short \u00b7 tasks/1-short.md\n", "x") == []


def test_emit_source_refuses_to_write_an_over_budget_view(tmp_path, monkeypatch):
    """Refuse rather than write it and let a LATER --check report what was already emitted."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    before = source.read_bytes()
    monkeypatch.setattr(gtt, "_VIEW_ROW_BYTE_CEILING", 5)
    rc = gtt.main(["--emit-source", "--source", str(source), "--out", str(out_dir)])
    assert rc == 1
    assert source.read_bytes() == before, "a refused emit must change zero bytes"


def test_write_refuses_the_projection_and_force_cannot_override_it(tmp_path, capsys):
    """The one refusal `--force` cannot reach: importing the view would replace every task
    body with its own title, and no state makes that the right act."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)   # leaves the PROJECTION on disk
    before_tree = _files_snapshot(out_dir)

    for argv in (["--write"], ["--write", "--force"]):
        assert gtt.main(argv + ["--source", str(source), "--out", str(out_dir)]) == 2
        err = capsys.readouterr().err
        assert "REFUSED" in err and "one-line VIEW" in err
        assert "NOT overridable with --force" in err
        assert _files_snapshot(out_dir) == before_tree, "a refused --write must change zero bytes"


def test_a_full_body_backlog_without_done_when_is_not_mistaken_for_the_view(tmp_path):
    """The guard's false-positive edge, and it is a real shape: a CONSUMER repo's
    hand-authored backlog need not carry `Done when:` (that is a hub ADR-66 rule), and
    `--write` bootstrap is exactly what such a repo needs. One signal alone would refuse it."""
    source = tmp_path / "BACKLOG.md"
    source.write_bytes(_TWO_THEMES.encode("utf-8"))   # no Done-when, no tasks/ pointers
    assert gtt._looks_like_view(source) is False
    assert gtt.main(["--write", "--source", str(source), "--out", str(tmp_path / "tasks")]) == 0


def test_check_fails_when_the_tree_stops_reassembling_losslessly(tmp_path):
    """Leg 6: the projection is only safe to be lossy while the full-body text it projects
    from provably still reassembles. Before [#589] leg 3 proved that for free."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    assert gtt.find_incoherences(source, out_dir) == []

    # Plant a stray CR inside the BODY only. Whole-file CRLF would break `extract_body`
    # and abort at leg 1, which proves the wrong thing: the point is that leg 6 catches a
    # tree that still PARSES and still PROJECTS but no longer reassembles losslessly.
    victim = next(p for p in sorted(out_dir.glob("*.md")) if p.name[0].isdigit())
    victim.write_bytes(victim.read_bytes().replace("—".encode("utf-8"),
                                                   "—\r".encode("utf-8")))
    problems = gtt.find_incoherences(source, out_dir)
    assert any("lossless" in p for p in problems), problems


# --- [#589] terra round 1 (2026-08-26): the refusal predicate and the shape leg ----

def test_a_title_containing_done_when_cannot_smuggle_the_view_past_the_refusal(tmp_path, capsys):
    """terra CRITICAL — the bypass, pinned so it cannot come back.

    `_looks_like_view` used to require that NO row carried `Done when:`. A row whose bold
    TITLE contains those words keeps them through `derive_title` and into the projection, so
    ONE such row made the conjunction False, `--write --force` proceeded, and every
    authoritative body was overwritten by its own one-line title — through the guard whose own
    message says "NOT overridable with --force". A refusal predicate must not be defeatable by
    the content of the thing it protects.
    """
    text = ("# T\n\n## [E1] Theme\n\n### [S1] Story\n"
            "- [#1] [P1][S] **Say Done when: in the title** \u2014 body \u00b7 Done when: it is done\n")
    source, out_dir = _seed(tmp_path, text)
    projected = source.read_text(encoding="utf-8")
    assert "Done when:" in projected, "the fixture must reproduce the bypass shape"

    before = _files_snapshot(out_dir)
    assert gtt._looks_like_view(source, out_dir) is True
    assert gtt.main(["--write", "--force", "--source", str(source), "--out", str(out_dir)]) == 2
    assert "one-line VIEW" in capsys.readouterr().err
    assert _files_snapshot(out_dir) == before, "the bodies must be untouched"


def test_the_refusal_asks_the_tree_first_and_that_answer_is_exact(tmp_path):
    """Leg 1: byte-equality with what the tree projects is not a heuristic and cannot be
    defeated by any row's text. Leg 2 (the identity marker) is the fallback for a stale or
    foreign view."""
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    assert source.read_text(encoding="utf-8") == gtt.render_view(out_dir)
    assert gtt._looks_like_view(source, out_dir) is True
    # Same bytes, no tree handed over -> leg 2 must still recognise it.
    assert gtt._looks_like_view(source) is True


def test_an_over_long_row_does_not_stop_a_view_from_being_recognised(tmp_path):
    """terra CRITICAL, round 2 — the mirror of round 1's bypass.

    The replacement predicate folded the per-row BYTE BUDGET into "is this a projection", so a
    projection carrying one over-long row stopped being recognised as one and `--write --force`
    would import it. Identity is not a size question: a view of a DIFFERENT tree (so leg 1
    cannot answer) with a 900-byte row must still be refused.
    """
    source, out_dir = _seed(tmp_path, _TWO_THEMES)
    view = source.read_text(encoding="utf-8")
    bloated = view.replace("- [#1] [P1][S] A ", "- [#1] [P1][S] " + "A" * 900 + " ")
    other = tmp_path / "OTHER.md"
    other.write_text(bloated, encoding="utf-8", newline="\n")

    assert not any(gtt.is_projected_row(ln) and len(ln.encode("utf-8")) > 400
                   for ln in gtt.task_row_lines(view)), "fixture sanity"
    assert bloated != gtt.render_view(out_dir), "leg 1 must NOT be what answers here"
    assert gtt._looks_like_view(other, out_dir) is True
    assert gtt.main(["--write", "--force", "--source", str(other), "--out", str(out_dir)]) == 2


def test_a_full_body_row_that_cites_its_task_file_last_is_not_refused(tmp_path, capsys):
    """terra HIGH, round 2 — the other side of the same coin.

    Under the shape predicate, ANY full-body row under the byte budget that happened to end
    with ` · tasks/<file>.md` matched, so `--write` refused a legitimate bootstrap input and
    `--force` could not override it. Identity has no such false positive: the row carries real
    body text, and the file carries no marker.
    """
    source = tmp_path / "BACKLOG.md"
    source.write_text(
        "# T\n\n## [E1] One\n\n### [S1] Story\n"
        "- [#1] [P1][S] **A** \u2014 body \u00b7 Done when: done \u00b7 tasks/1-a.md\n",
        encoding="utf-8", newline="\n")
    assert gtt._looks_like_view(source) is False
    assert gtt.main(["--write", "--source", str(source), "--out", str(tmp_path / "tasks")]) == 0


def test_the_live_view_carries_the_generator_owned_identity_marker():
    """The marker is what the destructive-import refusal reads, so its presence in the
    committed file is the guarantee, not an ornament."""
    assert gtt._VIEW_MARKER in BACKLOG.read_text(encoding="utf-8")
    assert gtt._VIEW_MARKER in gtt.render_view(TREE)
    # ...and it is NOT in the full-body canonical text, or the refusal would fire on the one
    # artifact that legitimately IS an import source.
    assert gtt._VIEW_MARKER not in canonical()


def test_view_problems_fires_on_body_appended_after_the_pointer(tmp_path):
    """terra HIGH — the ceilings bound HOW MUCH comes back, the grammar bounds WHAT.

    A row is end-anchored at its `tasks/<file>.md` pointer, so body material appended to it
    breaks the match outright rather than merely making the row longer.
    """
    row = "- [#1] [P1][S] Title \u00b7 tasks/1-title.md \u00b7 Done when: it is done"
    problems = gtt.view_problems(row + "\n", "x")
    assert any("not the [#589] projection shape" in p for p in problems), problems
    assert gtt.view_problems("- [#1] [P1][S] Title \u00b7 tasks/1-title.md\n", "x") == []
    # The GRAMMAR is what fires, not the words: an identical row whose TITLE happens to say
    # "Done when:" is legitimate and must pass, or the gate refuses the regen it demands.
    assert gtt.view_problems(
        "- [#1] [P1][S] Say Done when: in the title \u00b7 tasks/1-t.md\n", "x") == []


def test_view_problems_ignores_task_shaped_prose_inside_a_fence():
    """Fence awareness, shared with `parse_backlog`. `BACKLOG.md` documents its own row
    grammar inside a ``` block; a naive scan reported that documentation as a malformed row
    and REFUSED `--emit-source`. Found by a fixture that predates this arc."""
    text = ("- [#1] [P1][S] Real \u00b7 tasks/1-real.md\n"
            "```\n"
            "- [#id] [P1][M] <action> \u00b7 Done when: <criterion> \u00b7 refs <ADR/file>\n"
            "```\n")
    assert gtt.view_problems(text, "x") == []
    assert gtt.task_row_lines(text) == ["- [#1] [P1][S] Real \u00b7 tasks/1-real.md"]


def test_the_live_view_satisfies_the_projection_grammar_row_by_row():
    """The grammar leg, asserted against the committed file rather than the renderer."""
    text = BACKLOG.read_text(encoding="utf-8")
    assert gtt.view_problems(text, "BACKLOG.md") == []
    rows = [ln for ln in text.split("\n") if gtt._TASK_RE.match(ln)]
    assert rows and all(gtt.is_projected_row(ln) for ln in rows)
