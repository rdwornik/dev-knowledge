"""Tests for scripts/gen_intake_index.py (#307 status-grouped intake index).

Firing tests: frontmatter parse, status grouping in canonical lifecycle order, the loud
OTHER bucket for unknown states, marker-splice (never overwrites the doctrine sections),
the regen-and-diff drift check, and the "moves no file" contract.
"""

import importlib.util
import sys
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "scripts" / "gen_intake_index.py"


def _load():
    spec = importlib.util.spec_from_file_location("gen_intake_index", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_intake_index"] = module
    spec.loader.exec_module(module)
    return module


gi = _load()


def _doc(status: str, intake_id: str, title: str) -> str:
    return (f"---\nintake-id: {intake_id}\nstatus: {status}\norigin: test\n---\n\n"
            f"# {title}\n\nbody\n")


def _make_intake_dir(tmp_path: Path, docs: dict[str, str]) -> Path:
    d = tmp_path / "intake"
    d.mkdir()
    for name, content in docs.items():
        (d / name).write_text(content, encoding="utf-8")
    return d


# --- frontmatter + collect ---------------------------------------------------

def test_parse_frontmatter_extracts_status_and_id():
    fm = gi._parse_frontmatter(_doc("SEED", "7", "A thing"))
    assert fm["status"] == "SEED"
    assert fm["intake-id"] == "7"


def test_parse_frontmatter_absent_is_empty():
    assert gi._parse_frontmatter("# no frontmatter\n") == {}


# --- the underscore blind spot (vacuous green: the parser looked at zero such keys) -------

def test_parse_frontmatter_sees_underscore_keys():
    """`_FM_KV_RE`'s key class `[a-z0-9-]` had NO underscore, so an underscore-bearing key
    matched NOTHING and was silently dropped from a dict the docstring calls "the leading
    ---...--- YAML frontmatter as a flat {key: value} dict".

    Failing-test shape, not a baseline pin: the correct behaviour here is knowable and
    desirable (a YAML frontmatter parser must see a legal YAML key), so the test asserts the
    right answer and went RED, rather than freezing the wrong one.
    """
    fm = gi._parse_frontmatter(
        "---\nstatus: SEED\nlast_reviewed: 2026-08-03\nreview_date: 2026-07-20\n---\n\n# t\n")
    assert fm["status"] == "SEED"
    assert "last_reviewed" in fm, "underscore key silently dropped"
    assert "review_date" in fm, "underscore key silently dropped"


def test_parse_frontmatter_covers_the_key_shapes_this_repo_actually_uses():
    """Structural, not enumerated: the key names are DERIVED from the repo's own canonical
    frontmatter on disk (`canonical_freshness_gate.DEFAULT_FRESHNESS_FILES`), never a
    hand-built literal. A parser blind to a key shape the repo genuinely uses is reporting
    on a corpus it cannot see.

    Guarded against becoming vacuous itself: if the derivation yields no underscore key, the
    test FAILS rather than passing on an empty set — the exact failure mode under repair.
    """
    repo_root = Path(__file__).resolve().parent.parent
    import canonical_freshness_gate as cfg

    live_keys: set[str] = set()
    for rel in cfg.DEFAULT_FRESHNESS_FILES:
        p = repo_root / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        for line in text.splitlines()[1:]:
            if line.strip() == "---":
                break
            if ":" in line and not line.startswith((" ", "\t", "#")):
                live_keys.add(line.split(":", 1)[0].strip())

    underscored = {k for k in live_keys if "_" in k}
    assert underscored, (
        "derivation produced no underscore-bearing key — this test would be vacuous; "
        f"canonical frontmatter keys found: {sorted(live_keys)}")

    body = "".join(f"{k}: x\n" for k in sorted(live_keys))
    fm = gi._parse_frontmatter(f"---\n{body}---\n\n# t\n")
    missing = {k.lower() for k in live_keys} - fm.keys()
    assert not missing, f"parser cannot see key shapes the repo uses: {sorted(missing)}"


def test_collect_excludes_readme_and_reads_status(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "2026-07-06-a.md": _doc("CONSUMED", "1", "Alpha"),
        "2026-07-07-b.md": _doc("SEED", "2", "Beta"),
        "README.md": "# readme\n",
    })
    rows = gi.collect_intakes(d)
    names = {r[2] for r in rows}
    assert names == {"2026-07-06-a.md", "2026-07-07-b.md"}
    statuses = {r[2]: r[0] for r in rows}
    assert statuses["2026-07-06-a.md"] == "CONSUMED"


# --- render: grouping, order, counts, OTHER bucket ---------------------------

def test_render_groups_in_canonical_lifecycle_order(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "c.md": _doc("CONSUMED", "3", "Cee"),
        "s.md": _doc("SEED", "1", "Ess"),
        "r.md": _doc("REJECTED", "2", "Arr"),
    })
    out = gi.render_contents(d)
    # SEED must render before CONSUMED before REJECTED regardless of file order.
    assert out.index("### SEED") < out.index("### CONSUMED") < out.index("### REJECTED")
    assert "**3 intake documents.**" in out
    assert "### SEED (1)" in out
    assert "[#1](s.md) — Ess" in out


def test_status_order_is_the_ruled_enum():
    # The [#398]-deployed enum (2026-07-19 ruling, SUPPLEMENT.md:68-70) — the
    # gate-readable canon a status-coupled validator will consume.
    assert gi._STATUS_ORDER == (
        "SEED", "DRAFT", "READY", "ACCEPTED", "CONSUMED", "SUPERSEDED", "REJECTED")


def test_render_groups_new_states_in_lifecycle_order(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "u.md": _doc("SUPERSEDED", "2", "Sup"),
        "a.md": _doc("ACCEPTED", "1", "Acc"),
        "y.md": _doc("READY", "3", "Red"),
    })
    out = gi.render_contents(d)
    # READY < ACCEPTED < SUPERSEDED, and none of the ruled states leaks into OTHER.
    assert out.index("### READY") < out.index("### ACCEPTED") < out.index("### SUPERSEDED")
    assert "### OTHER" not in out


def test_render_unknown_status_lands_in_loud_other_bucket(tmp_path):
    d = _make_intake_dir(tmp_path, {"x.md": _doc("BOGUS", "9", "Weird")})
    out = gi.render_contents(d)
    assert "### OTHER (1)" in out
    assert "[#9](x.md) — Weird" in out  # NOT dropped


def test_render_is_deterministic(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "a.md": _doc("SEED", "2", "A"), "b.md": _doc("SEED", "1", "B")})
    assert gi.render_contents(d) == gi.render_contents(d)
    out = gi.render_contents(d)
    # within a group, sorted by numeric intake-id: #1 before #2
    assert out.index("[#1](b.md)") < out.index("[#2](a.md)")


# --- splice: preserves doctrine, drift check, moves no file ------------------

_README = ("# docs/intake/\n\nintro\n\n"
           "## Contents\n\n"
           f"{gi._START_MARKER}\n(stale)\n{gi._END_MARKER}\n\n"
           "## 1. What this folder is\n\ndoctrine stays\n")


def test_splice_replaces_only_between_markers():
    spliced = gi._splice(_README, "FRESH BLOCK\n")
    assert "FRESH BLOCK" in spliced
    assert "(stale)" not in spliced
    assert "## 1. What this folder is" in spliced  # doctrine preserved
    assert "doctrine stays" in spliced


def test_splice_raises_without_markers():
    import pytest
    with pytest.raises(RuntimeError):
        gi._splice("# no markers here\n", "x\n")


def test_cmd_check_and_write_roundtrip(tmp_path, monkeypatch):
    d = _make_intake_dir(tmp_path, {"s.md": _doc("SEED", "1", "Ess")})
    readme = d / "README.md"
    readme.write_text(_README, encoding="utf-8")
    monkeypatch.setattr(gi, "_INTAKE_DIR", d)
    monkeypatch.setattr(gi, "_TARGET", readme)
    monkeypatch.setattr(gi, "_REPO_ROOT", tmp_path)

    assert gi._cmd_check() == 1          # (stale) block drifts from disk
    assert gi._cmd_write() == 0          # regenerate
    assert gi._cmd_check() == 0          # now clean
    # moved no file: the intake doc is untouched, doctrine section survives
    body = readme.read_text(encoding="utf-8")
    assert "## 1. What this folder is" in body
    assert (d / "s.md").exists()
    assert "[#1](s.md) — Ess" in body


def test_cmd_check_missing_markers_is_2(tmp_path, monkeypatch):
    d = _make_intake_dir(tmp_path, {"s.md": _doc("SEED", "1", "Ess")})
    readme = d / "README.md"
    readme.write_text("# no markers\n", encoding="utf-8")
    monkeypatch.setattr(gi, "_INTAKE_DIR", d)
    monkeypatch.setattr(gi, "_TARGET", readme)
    monkeypatch.setattr(gi, "_REPO_ROOT", tmp_path)
    assert gi._cmd_check() == 2


# --- codex-review 2026-07-11 hardening ---------------------------------------

def test_parse_frontmatter_unterminated_is_empty():
    # `---` with no closing `---` is INVALID -> empty (not silently parsed from the body).
    assert gi._parse_frontmatter("---\nstatus: SEED\nintake-id: 3\n\n# body, no close\n") == {}


def test_missing_intake_id_renders_loud_label(tmp_path):
    # A doc lacking intake-id must render a LOUD MISSING-ID label, never a `[2026]` fragment.
    d = _make_intake_dir(tmp_path, {"2026-07-07-x.md": "---\nstatus: SEED\n---\n\n# X\n"})
    out = gi.render_contents(d)
    assert "MISSING-ID" in out
    assert "[2026]" not in out


def test_splice_rejects_duplicate_markers():
    import pytest
    dup = f"# t\n{gi._START_MARKER}\na\n{gi._END_MARKER}\n{gi._START_MARKER}\nb\n{gi._END_MARKER}\n"
    with pytest.raises(RuntimeError):
        gi._splice(dup, "x\n")


def test_splice_rejects_reversed_markers():
    import pytest
    rev = f"# t\n{gi._END_MARKER}\nmid\n{gi._START_MARKER}\n"
    with pytest.raises(RuntimeError):
        gi._splice(rev, "x\n")


# --- the intake-id allocation ledger (NIGHT-2 lane W1-5; filings Q-3 finding F1) -----------
#
# F1, verbatim from `to-cc/ANSWER-filings-Q3.md`: "nothing enforces `intake-id` uniqueness.
# Both mandatory generators were run against a tree carrying a duplicate and BOTH wrote output
# without a word. `docs/intake/README.md` section 3 calls the id a 'stable integer, next free
# across all history'. That property is STATED, not enforced -- prose with no organ behind it."

def _archived(intake_dir: Path, docs: dict[str, str]) -> Path:
    a = intake_dir / "archive"
    a.mkdir(exist_ok=True)
    for name, content in docs.items():
        (a / name).write_text(content, encoding="utf-8")
    return a


def test_two_active_docs_on_one_id_is_a_collision(tmp_path):
    """The shape that actually happened: id 70 on BOTH the AJ second pass and
    roles-with-a-carrier, landed on main, with nothing detecting it."""
    d = _make_intake_dir(tmp_path, {
        "aj.md": _doc("DRAFT", "70", "AJ second pass"),
        "roles.md": _doc("DRAFT", "70", "Session roles with a carrier"),
    })
    reasons = gi.duplicate_id_reasons(d)
    assert len(reasons) == 1
    assert "70" in reasons[0] and "aj.md" in reasons[0] and "roles.md" in reasons[0]
    assert "ACTIVE" in reasons[0]


def test_archived_doc_sharing_an_active_id_is_the_join_key_not_a_collision(tmp_path):
    """Intake #14's real shape, and the one this predicate must NOT report: two independent
    derivations archived as CONSUMED provenance under the id of the ruled pack that unioned
    them. README section 5 -- "their `intake-id` join keys stay valid at the archive path".
    A naive "no id appears twice" rule renumbers a deliberate structure, so it is tested."""
    d = _make_intake_dir(tmp_path, {"ruled-pack.md": _doc("ACCEPTED", "14", "Ruled pack")})
    _archived(d, {
        "draft-fable.md": _doc("CONSUMED", "14", "Fable derivation"),
        "draft-codex.md": _doc("CONSUMED", "14", "Codex derivation"),
    })
    assert gi.duplicate_id_reasons(d) == []


def test_two_archived_docs_on_one_id_with_no_live_holder_is_a_collision(tmp_path):
    """The join key only joins if something live holds the id. With no active holder the two
    archived docs are simply ambiguous -- a join key pointing at nothing."""
    d = _make_intake_dir(tmp_path, {"live.md": _doc("SEED", "9", "Live")})
    _archived(d, {
        "old-a.md": _doc("REJECTED", "3", "Old A"),
        "old-b.md": _doc("SUPERSEDED", "3", "Old B"),
    })
    reasons = gi.duplicate_id_reasons(d)
    assert len(reasons) == 1
    assert "ARCHIVED" in reasons[0] and "3" in reasons[0]


def test_next_free_id_is_a_high_water_mark_and_never_refills_a_gap(tmp_path):
    """README section 3: "closed ids are not reused -- same discipline as BACKLOG ids". Handing
    back a gap would resurrect exactly the ambiguity a renumbering was performed to remove."""
    d = _make_intake_dir(tmp_path, {
        "a.md": _doc("SEED", "1", "A"), "c.md": _doc("SEED", "9", "C")})
    assert gi.next_free_id(d, scan_refs=False) == 10


def test_next_free_id_counts_an_archived_id_no_live_doc_holds(tmp_path):
    """An archived-only id is SPENT, not free -- the folder listing under-reports by exactly
    these docs, which is why an author reading it allocates a colliding id."""
    d = _make_intake_dir(tmp_path, {"a.md": _doc("SEED", "2", "A")})
    _archived(d, {"gone.md": _doc("REJECTED", "40", "Gone")})
    assert gi.next_free_id(d, scan_refs=False) == 41


def test_write_REFUSES_on_a_colliding_tree_instead_of_writing_silently(tmp_path, monkeypatch):
    """FINDING F1 ITSELF, as a regression. Before this, `--write` rendered an index over a
    colliding tree and reported success -- laundering a duplicate join key into a generated
    artifact that then reads as authoritative. Exit 3 is its own class: 1 (stale) and 2
    (missing markers) both name remedies that do not apply, and regenerating is not the fix."""
    d = _make_intake_dir(tmp_path, {
        "one.md": _doc("DRAFT", "70", "One"), "two.md": _doc("DRAFT", "70", "Two")})
    target = d / "README.md"
    before = f"# t\n\n{gi._START_MARKER}\n{gi._END_MARKER}\n\n## doctrine\n"
    target.write_text(before, encoding="utf-8", newline="")
    monkeypatch.setattr(gi, "_INTAKE_DIR", d)
    monkeypatch.setattr(gi, "_TARGET", target)
    monkeypatch.setattr(gi, "_REPO_ROOT", tmp_path)  # _cmd_check renders paths relative to it
    assert gi.main(["--write"]) == 3
    assert target.read_text(encoding="utf-8") == before, "a refusal must not write"
    assert gi.main(["--check"]) == 3


def test_next_free_counts_an_id_that_exists_ONLY_on_an_unmerged_ref(tmp_path):
    """D8's MECHANISM ROW, and the half that makes the collision recur if it is dropped:
    "next-free computed across ALL refs (local + origin branches), not `main` only". A
    colliding doc is BY DEFINITION not yet on main -- it is on the branch about to allocate
    the same id -- so a tree-only max() reproduces the collision it exists to prevent.

    Witnessed on 2026-09-06: id 76 was live on `docs/intake-031-two-chats` and on no other
    ref, so the tree-only answer was 76 and the correct answer was 77.
    """
    import subprocess
    repo = tmp_path / "repo"
    (repo / "docs" / "intake").mkdir(parents=True)

    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    intake = repo / "docs" / "intake"
    (intake / "on-main.md").write_text(_doc("SEED", "5", "On main"), encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "main doc")
    git("checkout", "-qb", "side")
    (intake / "only-on-side.md").write_text(_doc("SEED", "76", "Side"), encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "side doc")
    git("checkout", "-q", "main")
    (intake / "only-on-side.md").unlink(missing_ok=True)

    # The working tree now sees ONLY id 5; id 76 lives on the unmerged `side` branch.
    assert gi.next_free_id(intake, scan_refs=False, repo_root=repo) == 6
    assert gi.next_free_id(intake, scan_refs=True, repo_root=repo) == 77


def test_a_ref_carrying_no_intake_docs_is_not_mistaken_for_an_unreadable_one(tmp_path):
    """`git grep` exits 1 for NO MATCH, which is the ordinary answer for a branch with no
    intake docs. Treating that as an error would refuse on every healthy repo; treating a real
    error as no-match is the silent degrade below. Both directions are live here."""
    import subprocess
    repo = tmp_path / "repo"
    (repo / "docs" / "intake").mkdir(parents=True)

    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (repo / "README.md").write_text("no intake docs here\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "a ref with zero intake docs")
    intake = repo / "docs" / "intake"
    (intake / "only-on-disk.md").write_text(_doc("SEED", "3", "Disk"), encoding="utf-8")

    assert gi.next_free_id(intake, scan_refs=True, repo_root=repo) == 4


def test_the_allocator_REFUSES_rather_than_silently_degrading_to_the_working_tree(tmp_path):
    """codex-review HIGH, 2026-09-07, and the defect this whole module exists to end. The first
    cut swallowed every git failure and returned the working-tree answer while still reporting
    "working tree + all refs" -- so a missing git or one unreadable ref hands out an id a branch
    already holds. `--no-refs` is the labelled opt-out; silence is not."""
    import pytest
    d = _make_intake_dir(tmp_path, {"a.md": _doc("SEED", "5", "A")})
    not_a_repo = tmp_path / "nowhere"
    not_a_repo.mkdir()

    with pytest.raises(gi.RefScanError):
        gi.next_free_id(d, scan_refs=True, repo_root=not_a_repo)
    # ... and the CLI turns that into a refusal, never an answer.
    assert gi.next_free_id(d, scan_refs=False, repo_root=not_a_repo) == 6
