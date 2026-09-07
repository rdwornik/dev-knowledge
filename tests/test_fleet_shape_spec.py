"""Tests for `ecosystem/fleet-shape-spec.yaml` and its wiring into the tree seal.

The spec exists to end one substitution: `scripts/validate_hermetization.py` used to carry
the fleet's shape as four module literals its own comments described as "DERIVED FROM THE
LIVE TAXONOMY" of this repo, so the hub's tree stood in for a spec nobody had written.
Operator amendment D5 of 2026-09-06 ruled the sanctioned set is "the fleet grammar, not the
hub's tree snapshot", with homes for `src/ eval/ models/`.

These tests are FIRING tests, not presence tests. The load-bearing one is
`test_the_seal_reads_the_file_and_not_a_literal`: it builds a whole doctored repo in a temp
directory, points the gate at ITS spec, and asserts the constants follow the file. A test
that only read the live spec would pass just as happily against a module that had kept its
literals and gained a decorative YAML beside them.
"""

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent
_SPEC = _ROOT / "ecosystem" / "fleet-shape-spec.yaml"

# A PLAIN import, deliberately, rather than the file-location loader the sibling
# hermetization tests use. `scripts/batch_manifest.py` refuses a shadowed
# `validate_hermetization` and `tests/test_manifest_link_route.py` asserts the two names
# resolve to the SAME frozenset object; re-executing the module under its canonical name
# here would rebind `sys.modules` mid-session and break that identity from the outside.
import validate_hermetization as vh  # noqa: E402


def _load_under(path: Path, name: str):
    """Execute a COPY of the module under a throwaway name -- never the canonical one."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
SPEC_DOC = yaml.safe_load(_SPEC.read_text(encoding="utf-8"))
CLAUSES = SPEC_DOC["clauses"]


# --- the file itself ----------------------------------------------------------------

def test_every_clause_is_asserted_or_says_why_not():
    """The anti-decoration rule: a clause names a live surface, or names its gap.

    Without this, the spec becomes a place to write intentions -- an aspirational key with
    no reader looks identical to an enforced one, and the fleet's shape would be back to
    being whatever the code happens to do. `asserted_by: null` is a legitimate answer (M6's
    report-first posture and the Python layout genuinely have no organ today); an EMPTY
    answer is not.
    """
    for name, clause in CLAUSES.items():
        assert "leg" in clause, f"clause `{name}` names no intake leg"
        assert "asserted_by" in clause, f"clause `{name}` carries no `asserted_by` key"
        if clause["asserted_by"] is None:
            reason = clause.get("unasserted_reason")
            assert reason and reason.strip(), (
                f"clause `{name}` is unasserted and gives no reason -- an honest gap is "
                f"stated, not left blank")


def test_every_locator_the_spec_cites_resolves_on_disk():
    """A `file.py::NAME` a reader has not opened is a claim, not evidence.

    The spec cites its asserting surfaces by path. If one is renamed away, the clause
    silently starts pointing at nothing and the gap becomes invisible -- which is the exact
    failure this file was written to end, one level up.
    """
    cited: list[str] = []
    for clause in CLAUSES.values():
        for key in ("asserted_by", "source", "files_from",
                    "workspace_required_settings_from"):
            value = clause.get(key)
            if isinstance(value, str):
                cited.append(value)
    assert cited, "no locators found -- the harvest itself is broken"
    for locator in cited:
        # `a.py::NAME`, and `a.py + b` for a clause asserted by two surfaces.
        for token in locator.replace("+", " ").split():
            path = token.split("::")[0].strip()
            if not path.endswith(".py"):
                continue
            assert (_ROOT / path).exists(), f"spec cites a path that does not exist: {path}"


def test_the_source_intake_resolves():
    assert (_ROOT / SPEC_DOC["source_intake"]).exists()


# --- D5 / D6: what the ruling ordered -------------------------------------------------

@pytest.mark.parametrize("top", ["src", "eval", "models"])
def test_d5_admits_a_code_repos_source_homes(top):
    """The D5 amendment, end to end.

    `corp-monorepo`'s `src/` (214 files), `eval/` (54) and `models/` (6) were each refused
    by the seal for one reason: a governance hub keeps its code in `scripts/`, and the
    sanctioned set had been read off that tree. The alternative to this clause was three
    WAIVEs per code repo in perpetuity.
    """
    assert top in vh.SANCTIONED_TIER1_DIRS
    assert vh.classify(f"{top}/pkg/module.py") is None
    assert vh.classify(f"{top}/toplevel.py") is None


def test_d6_admits_the_dashboard_genre_without_creating_it():
    """D6: `docs/dashboard/` is ADMITTED "via #73, as a folder-grammar entry, not ad hoc".

    Admission and existence are different acts, and keeping them apart is the whole point of
    a spec that is not a tree snapshot: the genre is in-pattern here while no such directory
    exists in this repo.
    """
    assert "dashboard" in vh.SANCTIONED_GENRES
    assert vh.classify("docs/dashboard/2026-09-07-technical-x.md") is None
    assert not (_ROOT / "docs" / "dashboard").exists()


def test_the_workspace_file_is_a_fleet_glob_not_the_hubs_own_name():
    """Leak class 2 of the 78 measured items.

    The seal used to hold the literal `.dev-knowledge.code-workspace`, so it refused a
    consumer's own workspace file -- one repo's name doing duty as a fleet rule. The dot
    prefix is kept because ADR-59 Decision 3 puts root tool config behind one, so a
    dot-less name is still refused.
    """
    assert vh.rule_a_violation(".corp-monorepo.code-workspace") is None
    assert vh.rule_a_violation(".dev-knowledge.code-workspace") is None
    assert vh.rule_a_violation(".corp-ops.code-workspace") is None
    assert vh.rule_a_violation("my-repo.code-workspace") is not None
    # The hub literal is GONE from the frozenset -- the glob is now the only admitting leg,
    # so the two cannot drift apart.
    assert ".dev-knowledge.code-workspace" not in vh.SANCTIONED_TIER1_FILES


# --- the wiring: the values come from the FILE ----------------------------------------

def test_constants_equal_the_spec_payload():
    assert vh.SANCTIONED_TIER1_DIRS == frozenset(CLAUSES["root_allowlist"]["directories"])
    assert vh.SANCTIONED_GENRES == frozenset(CLAUSES["genre_folders"]["genres"])
    assert vh._HOME_PATTERNS == tuple(CLAUSES["home_grammar"]["patterns"])
    assert vh.AUDIT_CLASS_ENUM == frozenset(CLAUSES["naming_grammar"]["audit_class_enum"])
    assert vh.SANCTIONED_TIER1_FILE_GLOBS == tuple(CLAUSES["root_allowlist"]["file_globs"])


def test_the_canonical_living_docs_are_joined_in_not_restated():
    """The one roster the spec deliberately does NOT carry.

    CLOUD-4 v2 made ADR-101 §1's file enum and the ADR-38 canonical set provably the same
    strings by reading both from `canonical_docs`. Copying those names into YAML would undo
    that, so the spec cites the registry (`files_from`) and the union happens in code.
    """
    from scripts import canonical_docs as cdocs
    assert set(cdocs.CANONICAL_MANDATORY) <= vh.SANCTIONED_TIER1_FILES
    assert not set(cdocs.CANONICAL_MANDATORY) & set(CLAUSES["root_allowlist"]["files"])
    assert CLAUSES["root_allowlist"]["files_from"].endswith("CANONICAL_MANDATORY")


def test_the_seal_reads_the_file_and_not_a_literal(tmp_path):
    """THE LOAD-BEARING TEST: doctor the spec, and the gate's verdicts follow it.

    A whole repo is staged in `tmp_path` -- the real `scripts/` tree beside a spec whose
    payload has been edited -- and the module is imported from THERE, so its
    `Path(__file__).parent.parent` resolves to the doctored root. If the constants were
    still literals with a decorative YAML beside them, every assertion below would fail.
    """
    shutil.copytree(_ROOT / "scripts", tmp_path / "scripts",
                    ignore=shutil.ignore_patterns("__pycache__"))
    doc = yaml.safe_load(_SPEC.read_text(encoding="utf-8"))
    doc["clauses"]["root_allowlist"]["directories"] = ["scripts", "warehouse"]
    doc["clauses"]["genre_folders"]["genres"] = ["ledgers"]
    doc["clauses"]["home_grammar"]["patterns"] = ["warehouse", "warehouse/**"]
    doc["clauses"]["root_allowlist"]["file_globs"] = ["*.sublime-project"]
    doc["clauses"]["naming_grammar"]["audit_class_enum"] = ["inventory"]
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "fleet-shape-spec.yaml").write_text(
        yaml.safe_dump(doc), encoding="utf-8")

    doctored = _load_under(tmp_path / "scripts" / "validate_hermetization.py",
                           "vh_doctored")
    try:
        # The doctored grammar is in force...
        assert doctored.SANCTIONED_TIER1_DIRS == frozenset({"scripts", "warehouse"})
        assert doctored.rule_c_violation("warehouse/bay/4/crate.md") is None
        assert doctored.rule_a_violation("project.sublime-project") is None
        # ...and this repo's real shape is NOT, which is what proves the file is the source.
        assert doctored.rule_a_violation("protocols/PLAYBOOK.md") is not None
        assert doctored.rule_a_violation("docs/audits/2026-09-07-technical-x.md") is not None
        assert doctored.rule_a_violation(".dev-knowledge.code-workspace") is not None
    finally:
        sys.modules.pop("vh_doctored", None)


def test_a_missing_or_malformed_spec_refuses_rather_than_admitting_everything(tmp_path):
    """FAIL-CLOSED, deliberately against this module's fail-open git posture.

    A git failure is an environment accident and the gate steps aside for it. A spec that
    will not load means the seal has NO RULES, and a tree seal that silently admits
    everything is worse than one that refuses to start.
    """
    with pytest.raises(vh.ShapeSpecError, match="absent"):
        vh.load_shape_spec(tmp_path / "nope.yaml")

    broken = tmp_path / "broken.yaml"
    broken.write_text("clauses: [not, a, mapping]\n", encoding="utf-8")
    with pytest.raises(vh.ShapeSpecError, match="clauses"):
        vh.load_shape_spec(broken)

    partial = tmp_path / "partial.yaml"
    partial.write_text("clauses:\n  root_allowlist: {}\n", encoding="utf-8")
    with pytest.raises(vh.ShapeSpecError, match="genre_folders"):
        vh.load_shape_spec(partial)

    wrong_type = tmp_path / "wrong.yaml"
    wrong_type.write_text(
        "clauses:\n"
        "  root_allowlist: {directories: 'not-a-list'}\n"
        "  genre_folders: {}\n  home_grammar: {}\n  naming_grammar: {}\n",
        encoding="utf-8")
    clauses = vh.load_shape_spec(wrong_type)
    with pytest.raises(vh.ShapeSpecError, match="list of strings"):
        vh._clause_list(clauses, "root_allowlist", "directories")


# --- the 2026-09-07 adversarial round (terra), both HIGHs ------------------------------

def test_a_valid_but_wrong_regex_is_refused_at_load_not_silently_obeyed():
    """terra HIGH 1: moving the grammar into YAML made silent-pass possible.

    `'^'` is a perfectly valid regex and the wrong one: it matches everything, so every
    casing and slug refusal would quietly become a pass. A seal that stops refusing looks
    exactly like a clean tree, which is why this class had to be caught at load rather than
    left to a reviewer. The sentinels live in code on purpose -- a spec-supplied sentinel
    could be doctored to agree with the broken pattern and would prove nothing.
    """
    clauses = vh.load_shape_spec(_SPEC)

    for key, permissive in (("filename_charset", "^"), ("slug", "^"), ("date_prefix", "")):
        broken = {**clauses, "naming_grammar": {**clauses["naming_grammar"], key: permissive}}
        with pytest.raises(vh.ShapeSpecError, match="accepts"):
            vh._compile_checked(broken, key)

    # The other direction: a pattern so strict it refuses conformant names is equally wrong,
    # and is caught by the same proof rather than by a commit that mysteriously blocks.
    too_strict = {**clauses,
                  "naming_grammar": {**clauses["naming_grammar"], "slug": "^zzz$"}}
    with pytest.raises(vh.ShapeSpecError, match="refuses"):
        vh._compile_checked(too_strict, "slug")

    # A string that is not a regex at all fails as a spec error, not a raw `re.error`.
    malformed = {**clauses,
                 "naming_grammar": {**clauses["naming_grammar"], "slug": "([unclosed"}}
    with pytest.raises(vh.ShapeSpecError, match="not a valid regex"):
        vh._compile_checked(malformed, "slug")


def test_a_depth_wildcard_does_not_readmit_a_dot_directory():
    """terra HIGH 2, the concrete escape it named.

    D5 admits `src/ eval/ models/` with `**` homes because a source tree nests by its own
    package structure. Left open, that also admits `src/.github/workflows/` -- a
    dot-directory Rule A refuses at the root, reintroduced one level down with the top-level
    seal silent about it. Dot homes are what ADR-59 governs by name, so they stay a surfaced
    act: nameable by a literal or `*` pattern, never by an open depth wildcard.
    """
    assert vh.rule_c_violation("src/pkg/deep/mod.py") is None
    assert vh.rule_c_violation("src/.github/workflows/ci.yml") is not None
    assert vh.rule_c_violation("models/.hidden/weights.bin") is not None
    assert vh.rule_c_violation("tests/fixtures/.git/config") is not None
    # ...and the two dot homes the repo REALLY has ride explicit `*` patterns, so the new
    # leg leaves them untouched. Measured over all tracked paths before it was written.
    assert vh.rule_c_violation("ecosystem/.dev-knowledge/history/2026-01-01.md") is None
    assert vh.rule_c_violation("plugins/tier1-lifecycle/.claude-plugin/plugin.json") is None


# --- the closure clause: the hub passes its own seal FROM THE DATA ---------------------

def test_the_hub_passes_its_own_seal_from_the_spec():
    """The lane's closure clause, asserted directly.

    `tests/test_validate_hermetization.py` already sweeps every tracked path against Rule C.
    This runs the STRUCTURAL seal -- Rule A (root allowlist, file globs, genre folders) and
    Rule C (home grammar) -- over the whole tracked tree and states what it now means: the
    hub is one INSTANCE of the fleet grammar, and it conforms to a spec it no longer defines
    by simply existing. A path refused here is a real divergence between the hub's tree and
    the written shape, where before the same sweep was a tautology.

    RULE B IS DELIBERATELY OUT OF SCOPE, and saying so is the honest half. It is
    prospective-only by ADR-101 §6, which grandfathers the legacy `docs/audits/` names
    predating the class grammar -- 137 of them at this commit. Sweeping them would fail on
    files the ruling explicitly exempted from retroactive renaming, so the count is
    asserted as a known ceiling instead: it may shrink, and a rise means a new off-grammar
    name got in past the prospective gate.
    """
    import subprocess
    out = subprocess.run(["git", "ls-files"], cwd=_ROOT, capture_output=True,
                         text=True, encoding="utf-8")
    assert out.returncode == 0, out.stderr
    tracked = [p for p in out.stdout.splitlines() if p.strip()]
    assert len(tracked) > 500, "git ls-files returned an implausibly small tree"

    refused = [(p, r) for p in tracked
               if (r := (vh.rule_a_violation(p) or vh.rule_c_violation(p))) is not None]
    assert refused == [], (
        f"{len(refused)} tracked path(s) diverge from the fleet shape spec: {refused[:5]}")

    grandfathered = [p for p in tracked if vh.rule_b_violation(p) is not None]
    assert len(grandfathered) <= 137, (
        f"{len(grandfathered)} off-grammar audit names, above the 137 ADR-101 §6 "
        f"grandfathers -- a new one got past the prospective gate")
