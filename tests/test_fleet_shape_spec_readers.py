"""Reader-proof tests for `ecosystem/fleet-shape-spec.yaml` — a clause an organ CLAIMS is a
clause an organ OPENS.

WHY THIS FILE EXISTS, separately from `tests/test_fleet_shape_spec.py`. That file proves the
tree seal reads the file rather than a literal, clause by clause for the four clauses the
seal derives. It does not ask the census question: *of every clause in the spec, which ones
does the organ named in `asserted_by` actually open?* Measured at `33bcb0bd`
(`docs/audits/2026-09-09-technical-shape-spec-clause-readers.md`) the answer was **4 of 9**,
and **three** clauses named an organ that never opened them — `required_docs`, `vscode` and
`sorting`. A clause with an asserting surface that does not read it is worse than an
unasserted one: `asserted_by: null` is visible in the file and admitted by
`test_every_clause_is_asserted_or_says_why_not`, while a decorative locator reads as enforced.

THE PROOFS ARE BEHAVIOURAL, NEVER A NAME-GREP. A grep over an organ's source proves the
clause name appears in it; it cannot prove the value is consumed. Every proof below doctors
the clause's payload and asserts the organ's behaviour follows — so an organ that stops
reading its clause makes these tests FAIL rather than pass more quietly.

Two mechanisms, chosen by WHEN the organ reads:
  * load-time readers (`validate_hermetization`) are proven by staging a whole doctored repo
    in `tmp_path` and importing the module from THERE, the house pattern
    `test_the_seal_reads_the_file_and_not_a_literal` established. ONE doctored load carries
    every load-time clause, so the suite pays for one `copytree` rather than six.
  * call-time readers (`check_workspace_settings`) are proven by monkeypatching the module
    attribute the organ holds — `validate_hermetization.SHAPE_SPEC` — which is why that organ
    reads the clauses through the module rather than through a `from`-import binding.
"""

import importlib.util
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent
_SPEC = _ROOT / "ecosystem" / "fleet-shape-spec.yaml"

# A PLAIN import, for the reason `tests/test_fleet_shape_spec.py` records: `batch_manifest`
# refuses a shadowed `validate_hermetization` and `test_manifest_link_route` asserts the two
# names resolve to the SAME frozenset object.
import validate_hermetization as vh  # noqa: E402

from audit_checks.check_workspace_settings import (  # noqa: E402
    _WORKSPACE_REQUIRED_SETTINGS,
    check_workspace_settings,
)

CLAUSES: dict[str, Any] = yaml.safe_load(_SPEC.read_text(encoding="utf-8"))["clauses"]

#: The six kinds, in code rather than read from the file it checks. Same mechanism as
#: `validate_hermetization._REGEX_SENTINELS`: a proof the spec supplied could be doctored to
#: agree with a broken spec, and would prove nothing.
SIX_KINDS = {"source", "test", "data", "model", "eval", "tooling"}

GOOD_WS = """\
{
  "folders": [{ "path": "." }],
  "settings": {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper",
  },
}"""


def _load_under(path: Path, name: str):
    """Execute a COPY of the module under a throwaway name -- never the canonical one."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# --- the census: no clause names an organ that does not open it ------------------------

#: Every clause whose read is proven below, mapped to the test that proves it. A clause that
#: gains an `asserted_by` without gaining a proof fails `test_the_census_is_complete`.
PROVEN_READS = {
    "root_allowlist": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "genre_folders": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "home_grammar": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "naming_grammar": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "python_layout": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "required_docs": "test_one_doctored_load_proves_every_load_time_clause_is_read",
    "vscode": "test_the_vscode_clause_is_read_at_call_time",
    "sorting": "test_the_sorting_clause_is_read_at_call_time",
}


def test_the_census_is_complete():
    """Done-contract line 2: clauses whose `asserted_by` names a non-reading organ -> 0.

    The census is derived from the FILE, not from a list kept beside it, so a clause added
    with an asserting surface and no reader surfaces here on the next run instead of joining
    the decorative set unnoticed.
    """
    claimed = {name for name, clause in CLAUSES.items()
               if clause.get("asserted_by") is not None}
    unproven = sorted(claimed - set(PROVEN_READS))
    assert not unproven, (
        f"clauses name an asserting organ with no proof that the organ OPENS them: "
        f"{unproven} -- either wire a reader or state the gap as `asserted_by: null` with "
        f"an `unasserted_reason`")
    # The other direction: a proof for a clause the spec no longer asserts is dead weight.
    assert not sorted(set(PROVEN_READS) - claimed - set(CLAUSES))


def test_only_report_first_remains_unasserted():
    """The honest gap, named. `report_first` is a posture, not a mechanism, and says so."""
    unasserted = sorted(name for name, clause in CLAUSES.items()
                        if clause.get("asserted_by") is None)
    assert unasserted == ["report_first"], (
        f"expected report_first as the only declared-unasserted clause, got {unasserted}")


# --- load-time readers: one doctored repo, every clause at once ------------------------

def test_one_doctored_load_proves_every_load_time_clause_is_read(tmp_path):
    """THE LOAD-BEARING TEST. Doctor every load-time clause; the module's surfaces follow.

    If any derivation below were re-frozen into a module literal, its assertion would fail
    while the rest kept passing -- which is what makes this a census rather than a smoke
    test. One `copytree`, six clauses.
    """
    shutil.copytree(_ROOT / "scripts", tmp_path / "scripts",
                    ignore=shutil.ignore_patterns("__pycache__"))
    doc = yaml.safe_load(_SPEC.read_text(encoding="utf-8"))
    c = doc["clauses"]

    c["root_allowlist"]["directories"] = ["scripts", "warehouse"]
    c["root_allowlist"]["files_from"] = "scripts/canonical_docs.py::LEDGER_MANDATORY"
    c["genre_folders"]["genres"] = ["ledgers"]
    c["naming_grammar"]["audit_class_enum"] = ["inventory"]
    c["home_grammar"]["patterns"] = ["warehouse", "warehouse/**", "bays", "crates"]
    c["home_grammar"]["kinds"] = {
        "source": "python_layout.source_home_by_layout",
        "test": "bays",
        "data": "crates",
        "model": "warehouse",
        "eval": "warehouse",
        "tooling": "warehouse",
    }
    c["home_grammar"]["declared_kinds"] = ["source", "test"]
    c["python_layout"]["declared_layout"] = "src"
    c["python_layout"]["source_home_by_layout"] = {"src": "warehouse", "flat": "warehouse"}
    c["python_layout"]["tests_home"] = "bays"
    c["required_docs"]["source"] = "scripts/canonical_docs.py::LEDGER_MANDATORY"

    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "fleet-shape-spec.yaml").write_text(
        yaml.safe_dump(doc), encoding="utf-8")

    doctored = _load_under(tmp_path / "scripts" / "validate_hermetization.py", "vh_readers")
    try:
        # root_allowlist / genre_folders / naming_grammar / home_grammar.patterns -- the
        # four already-read clauses, re-proven here so the census is one surface.
        assert frozenset({"scripts", "warehouse"}) == doctored.SANCTIONED_TIER1_DIRS
        assert frozenset({"ledgers"}) == doctored.SANCTIONED_GENRES
        assert frozenset({"inventory"}) == doctored.AUDIT_CLASS_ENUM
        assert doctored._HOME_PATTERNS == ("warehouse", "warehouse/**", "bays", "crates")

        # python_layout -- NEWLY read. The declared layout selects the source home.
        assert doctored.PYTHON_LAYOUT["layout"] == "src"
        assert doctored.PYTHON_LAYOUT["source_home"] == "warehouse"
        assert doctored.PYTHON_LAYOUT["tests_home"] == "bays"

        # home_grammar.kinds -- the kind parameter, with `source` resolved through the CITE
        # into python_layout rather than copied.
        assert set(doctored.KIND_HOMES) == SIX_KINDS
        assert doctored.KIND_HOMES["source"] == "warehouse"
        assert doctored.KIND_HOMES["test"] == "bays"
        assert doctored.KIND_HOMES["data"] == "crates"
        assert doctored.DECLARED_KINDS == ("source", "test")

        # required_docs -- NEWLY read: one registry, cited by two clauses, proven identical.
        assert doctored.REQUIRED_DOCS_REGISTRY == (
            "scripts/canonical_docs.py::LEDGER_MANDATORY")
    finally:
        sys.modules.pop("vh_readers", None)


# --- load-time readers, the fail-closed half ------------------------------------------

def _doctor(clause: str, **keys) -> dict[str, Any]:
    """The live clauses with ONE clause's keys overridden -- never mutating the live dict."""
    live = vh.load_shape_spec(_SPEC)
    return {**live, clause: {**live[clause], **keys}}


def test_a_layout_the_spec_does_not_declare_is_refused_at_load():
    """A `declared_layout` outside `source_layouts` is a spec that names a home it never
    defined. Refused loudly, rather than resolving to `None` five frames deeper."""
    with pytest.raises(vh.ShapeSpecError, match="declared_layout"):
        vh._python_layout(_doctor("python_layout", declared_layout="cathedral"))


def test_a_source_home_outside_the_home_grammar_is_refused_at_load():
    """The clause cannot admit a home the home grammar refuses -- that pair IS the seal."""
    live = vh.load_shape_spec(_SPEC)
    broken = {**live, "python_layout": {
        **live["python_layout"],
        "source_home_by_layout": {**live["python_layout"]["source_home_by_layout"],
                                  live["python_layout"]["declared_layout"]: "warehouse"}}}
    with pytest.raises(vh.ShapeSpecError, match="home grammar"):
        vh._python_layout(broken)


def test_the_kind_set_must_be_exactly_the_six():
    """Six kinds, no more and no fewer. A seventh kind is a spec change, not a drive-by."""
    live = vh.load_shape_spec(_SPEC)
    short = {**live, "home_grammar": {
        **live["home_grammar"],
        "kinds": {k: v for k, v in live["home_grammar"]["kinds"].items() if k != "eval"}}}
    with pytest.raises(vh.ShapeSpecError, match="six kinds"):
        vh._kind_homes(short, vh.PYTHON_LAYOUT)

    extra = {**live, "home_grammar": {
        **live["home_grammar"],
        "kinds": {**live["home_grammar"]["kinds"], "prose": "docs"}}}
    with pytest.raises(vh.ShapeSpecError, match="six kinds"):
        vh._kind_homes(extra, vh.PYTHON_LAYOUT)


def test_a_kind_carries_exactly_one_home():
    """`ONE home each` (AMEND-SESSION-PLAN-001 §2) -- a list is not a home."""
    live = vh.load_shape_spec(_SPEC)
    two = {**live, "home_grammar": {
        **live["home_grammar"],
        "kinds": {**live["home_grammar"]["kinds"], "data": ["config", "ecosystem"]}}}
    with pytest.raises(vh.ShapeSpecError, match="one home"):
        vh._kind_homes(two, vh.PYTHON_LAYOUT)


def test_a_declared_kind_outside_the_six_is_refused():
    live = vh.load_shape_spec(_SPEC)
    broken = {**live, "home_grammar": {**live["home_grammar"],
                                       "declared_kinds": ["test", "prose"]}}
    with pytest.raises(vh.ShapeSpecError, match="declared_kinds"):
        vh._kind_homes(broken, vh.PYTHON_LAYOUT)


def test_two_clauses_citing_one_registry_by_two_strings_is_refused():
    """`required_docs.source` and `root_allowlist.files_from` name the SAME registry.

    Two clauses citing one registry by two strings is a drift pair; one string checked at
    load is not. This is the whole read the clause can carry without restating a roster --
    and it is why `required_docs` is no longer a clause naming an organ that never opens it.
    """
    live = vh.load_shape_spec(_SPEC)
    broken = {**live, "required_docs": {**live["required_docs"],
                                        "source": "scripts/canonical_docs.py::SOMETHING_ELSE"}}
    with pytest.raises(vh.ShapeSpecError, match="same registry"):
        vh._require_one_registry(broken)


# --- call-time readers: check_workspace_settings ---------------------------------------

def _ws_repo(root: Path, vscode_files: tuple[str, ...] = ()) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / ".my-repo.code-workspace").write_text(GOOD_WS, encoding="utf-8")
    if vscode_files:
        (root / ".vscode").mkdir(exist_ok=True)
        for name in vscode_files:
            (root / ".vscode" / name).write_text("{}", encoding="utf-8")
    return root


def test_the_vscode_clause_is_read_at_call_time(tmp_path, monkeypatch):
    """Doctor `vscode.dir_allowed`, and the organ's verdict follows the file.

    `settings.json` is admitted by the live clause and refused by the doctored one, on the
    same tree -- so the difference can only have come from the spec.
    """
    repo = _ws_repo(tmp_path, ("settings.json",))
    assert check_workspace_settings(repo)[0].status == "pass"

    live = vh.load_shape_spec(_SPEC)
    doctored = {**live, "vscode": {**live["vscode"], "dir_allowed": ["extensions.json"]}}
    monkeypatch.setattr(vh, "SHAPE_SPEC", doctored)
    finding = check_workspace_settings(repo)[0]
    assert finding.status == "warn"
    assert "settings.json" in finding.evidence


def test_a_forbidden_vscode_member_is_refused_by_the_specs_glob(tmp_path, monkeypatch):
    """`dir_forbidden` carries fnmatch globs (`*.log`), and the organ applies them."""
    repo = _ws_repo(tmp_path / "live", ("settings.json", "workspace.log"))
    finding = check_workspace_settings(repo)[0]
    assert finding.status == "warn"
    assert "workspace.log" in finding.evidence

    # `launch.json` is ADMITTED by the live clause and FORBIDDEN by the doctored one, on the
    # same tree -- so the difference in verdict can only have come from the file.
    clean = _ws_repo(tmp_path / "clean", ("launch.json",))
    assert check_workspace_settings(clean)[0].status == "pass"

    live = vh.load_shape_spec(_SPEC)
    doctored = {**live, "vscode": {**live["vscode"], "dir_forbidden": ["launch.json"]}}
    monkeypatch.setattr(vh, "SHAPE_SPEC", doctored)
    finding = check_workspace_settings(clean)[0]
    assert finding.status == "warn"
    assert "launch.json" in finding.evidence


def test_the_sorting_clause_is_read_at_call_time(tmp_path, monkeypatch):
    """`sorting.asserted_by_setting` names the key that delivers the asserted half.

    The clause states an asserted half (`LESSONS / ARCHITECTURE at the top`) and an
    unassertable one (`smallest first`). The asserted half is delivered by exactly one VS
    Code setting, and if the clause and `_WORKSPACE_REQUIRED_SETTINGS` ever name different
    keys, the clause is claiming an assertion the organ does not make. Refused, not warned:
    a sorting clause that asserts nothing is the decorative shape this file exists to end.
    """
    repo = _ws_repo(tmp_path)
    assert check_workspace_settings(repo)[0].status == "pass"
    assert CLAUSES["sorting"]["asserted_by_setting"] in _WORKSPACE_REQUIRED_SETTINGS

    live = vh.load_shape_spec(_SPEC)
    drifted = {**live, "sorting": {**live["sorting"],
                                   "asserted_by_setting": "explorer.compactFolders"}}
    monkeypatch.setattr(vh, "SHAPE_SPEC", drifted)
    finding = check_workspace_settings(repo)[0]
    assert finding.status == "fail"
    assert "explorer.compactFolders" in finding.evidence


def test_the_workspace_file_glob_comes_from_the_spec(tmp_path, monkeypatch):
    """The dot-prefix rule is the spec's `root_allowlist.file_globs` member, not a literal
    `startswith('.')` in the organ. Leak class 2 of the 78 measured corp items was exactly
    one repo's copy of a fleet rule."""
    (tmp_path / "my-repo.code-workspace").write_text(GOOD_WS, encoding="utf-8")
    assert check_workspace_settings(tmp_path)[0].status == "warn"

    live = vh.load_shape_spec(_SPEC)
    permissive = {**live, "vscode": {**live["vscode"],
                                     "workspace_file_glob": "*.code-workspace"}}
    monkeypatch.setattr(vh, "SHAPE_SPEC", permissive)
    assert check_workspace_settings(tmp_path)[0].status == "pass"


# --- the kind parameter against the LIVE spec ------------------------------------------

def test_home_grammar_carries_the_six_kinds_with_one_home_each():
    """Done-contract line 3, read off the file rather than off the module."""
    kinds = CLAUSES["home_grammar"]["kinds"]
    assert set(kinds) == SIX_KINDS
    for kind, home in kinds.items():
        assert isinstance(home, str) and home, f"kind `{kind}` carries no single home"


def test_this_repo_declares_which_kinds_it_has():
    declared = CLAUSES["home_grammar"]["declared_kinds"]
    assert declared, "a repo that declares no kind cannot be measured against the grammar"
    assert set(declared) <= SIX_KINDS
    assert len(set(declared)) == len(declared), "a kind is declared once"


@pytest.mark.live_repo
def test_every_declared_kinds_home_is_admitted_and_exists_here():
    """The grammar admits a shape; the declaration says this repo HAS it. Both are checked.

    `src/`, `eval/` and `models/` are admitted by the spec and exist in no directory of this
    repo -- which is the point of separating the spec from the tree, and exactly why the
    existence half is scoped to the kinds this repo DECLARES.
    """
    for kind in vh.DECLARED_KINDS:
        home = vh.KIND_HOMES[kind]
        assert vh.is_allowed_home(home), (
            f"kind `{kind}` declares home `{home}`, which the home grammar refuses")
        assert (_ROOT / home).is_dir(), (
            f"kind `{kind}` is declared but its home `{home}` does not exist here")
