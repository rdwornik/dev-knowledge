"""L1 of the substrate-as-infrastructure lane: POSITIVE proof of identity ([#554]).

RED-FIRST, and the ordering is the acceptance criterion rather than a style note. Every test
below was written and RUN against a tree with no `scripts/substrate_provenance.py` in it; the
whole module collected as one `ModuleNotFoundError` before a line of the implementation
existed. A test written after the code witnesses nothing.

WHAT IS BEING WITNESSED. The measured defect was never `provision.sh` calling a dead module.
It was that a BROKEN CONTAINER REPORTED HEALTHY: `postCreateCommand` failed, Codespaces
silently substituted a bare recovery container, and the platform said Available throughout
(`[#746]`, witnessed 2026-09-14 23:37Z). Gates there were VACUOUS, not absent — which is the
dangerous shape, because an absent gate announces itself and a vacuous one does not. So the
property under test is not "no error was raised". It is "the marker is present, parseable, and
AGREES with the live environment", and a recovery container cannot produce one.

THE SHARED-PATH DEFECT, measured by a sibling lane 2026-09-15 and folded in here as evidence
rather than as a footnote. A read-only lane running concurrently with seven others wrote a
marker to a FIXED path (`/tmp/substrate-provenance.json`), re-read it later, and got ANOTHER
LANE'S VALUES: an honest neighbour had overwritten it. That defeats L1's whole security
property WITHOUT anybody attacking it — "a substrate that is not ours passes as ours", arriving
by collision rather than by malice. `test_marker_from_another_identity_is_REFUSED` and
`test_two_markers_present_verify_refuses_rather_than_reading_the_first` are that defect as
witnesses; `test_provenance_dir_under_the_system_temp_dir_is_REFUSED` is the home rule.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import substrate_provenance as sp

_REPO_ROOT = Path(__file__).resolve().parent.parent


# --- the injectable live-environment seam ---------------------------------------------------

class FakeProbe:
    """Everything the module learns about the machine it is on, under test control.

    A seam object rather than a monkeypatch pile: the module holds ONE adapter, so a test
    cannot patch a name the adapter does not actually read (the failure mode recorded as
    "monkeypatch the module the adapter holds").
    """

    def __init__(self, *, tools=None, python="3.12.10", node_name="host-a",
                 machine="mach-a", head="a" * 40, ancestors=None):
        self.tools = {"git": "2.43.0", "uv": "0.11.19", "node": "20.11.1",
                      "claude": "1.0.0", "pre-commit": "3.7.0"}
        if tools is not None:
            self.tools.update(tools)
        self._python = python
        self._node_name = node_name
        self._machine = machine
        self._head = head
        # {(older, newer)} pairs for which `is_ancestor` answers True.
        self._ancestors = set(ancestors or ())

    def tool_version(self, exe):
        return self.tools.get(exe)

    def python_version(self):
        return self._python

    def host_name(self):
        return self._node_name

    def machine_token(self):
        return self._machine

    def head(self, repo_root):
        return self._head

    def is_ancestor(self, repo_root, older, newer):
        if older == newer:
            return True
        return (older, newer) in self._ancestors


@pytest.fixture()
def substrate(tmp_path):
    """A repo root plus a private provenance dir, wired through the env."""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        '[tool.uv]\nrequired-version = "==0.11.19"\n', encoding="utf-8")
    (root / ".python-version").write_text("3.12.10\n", encoding="utf-8")
    store = tmp_path / "state"
    store.mkdir()
    env = {"DEV_KNOWLEDGE_PROVENANCE_DIR": str(store), "HOME": str(tmp_path)}
    return root, store, env


# --- the acceptance criterion: no marker, in a managed substrate, is a REFUSAL --------------

def test_a_container_without_a_marker_is_REFUSED(substrate):
    """THE lane acceptance criterion, in one test.

    A recovery container is a codespace the platform reports as Available and provisioning
    never finished in. `CODESPACES=true` is injected by the PLATFORM, not by our provisioning
    — so the substrate itself says "I am a managed container" while carrying no proof that it
    was provisioned. That pairing is the refusal.
    """
    root, _store, env = substrate
    env["CODESPACES"] = "true"
    env["CODESPACE_NAME"] = "recovery-abc123"

    verdict = sp.verify(root, env=env, probe=FakeProbe())

    assert verdict.status == "refused"
    assert any("no provenance marker" in r.lower() for r in verdict.refusals), verdict.refusals


def test_an_unmanaged_host_without_a_marker_is_not_refused(substrate):
    """The operator's workstation is not a provisioned container and must not read as one.

    Without this the verifier would refuse every LOCAL lane's step 0 — a gate that refuses
    everything is the same non-signal as a gate that refuses nothing.
    """
    root, _store, env = substrate

    verdict = sp.verify(root, env=env, probe=FakeProbe())

    assert verdict.status == "absent-ok"
    assert verdict.refusals == []


def test_require_marker_refuses_on_an_unmanaged_host_too(substrate):
    """`--require-marker` is what the pre-dispatch leg uses: the caller, not the host, decides."""
    root, _store, env = substrate

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "refused"


# --- positive verification: present is not enough ------------------------------------------

def test_written_marker_verifies_against_the_same_substrate(substrate):
    root, _store, env = substrate
    probe = FakeProbe()
    sp.write_marker(root, env=env, probe=probe)

    verdict = sp.verify(root, env=env, probe=probe, require_marker=True)

    assert verdict.status == "ok", verdict.refusals


def test_marker_records_the_facts_the_contract_names(substrate):
    """repo commit, uv version, Python version, node presence, and the lane's tool list."""
    root, _store, env = substrate
    path = sp.write_marker(root, env=env, probe=FakeProbe())
    marker = json.loads(path.read_text(encoding="utf-8"))

    assert marker["schema"] == sp.SCHEMA
    assert marker["head"] == "a" * 40
    assert marker["tools"]["uv"] == "0.11.19"
    assert marker["python_version"] == "3.12.10"
    assert marker["tools"]["node"] == "20.11.1"
    for tool in sp.TRACKED_TOOLS:
        assert tool in marker["tools"]


def test_a_marker_that_disagrees_with_live_uv_is_REFUSED(substrate):
    """"A marker that merely exists but disagrees with `uv --version` is a refusal."""
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())

    verdict = sp.verify(root, env=env, probe=FakeProbe(tools={"uv": "0.9.0"}),
                        require_marker=True)

    assert verdict.status == "refused"
    assert any("uv" in r for r in verdict.refusals), verdict.refusals


def test_a_tool_the_marker_recorded_and_the_container_lost_is_REFUSED(substrate):
    """The measured shape: node's ABSENCE, not authentication, is what blocked copilot/codex."""
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())

    verdict = sp.verify(root, env=env, probe=FakeProbe(tools={"node": None}),
                        require_marker=True)

    assert verdict.status == "refused"
    assert any("node" in r for r in verdict.refusals), verdict.refusals


def test_a_floating_tool_version_is_a_WARN_not_a_refusal(substrate):
    """`claude` auto-updates inside the container BY DESIGN (devcontainer.json says so).

    Refusing on its version would refuse a healthy container, so presence is refusal-grade and
    version equality is refusal-grade only for the ONE exactly-pinned tool (`uv`, ADR-106).
    """
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())

    verdict = sp.verify(root, env=env, probe=FakeProbe(tools={"claude": "1.9.9"}),
                        require_marker=True)

    assert verdict.status == "ok", verdict.refusals
    assert any("claude" in w for w in verdict.warnings), verdict.warnings


def test_an_interpreter_that_moved_is_REFUSED(substrate):
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())

    verdict = sp.verify(root, env=env, probe=FakeProbe(python="3.11.9"), require_marker=True)

    assert verdict.status == "refused"


def test_an_unparseable_marker_is_REFUSED_not_ignored(substrate):
    root, store, env = substrate
    path = sp.write_marker(root, env=env, probe=FakeProbe())
    path.write_text("{ not json", encoding="utf-8")

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "refused"
    assert store.exists()


def test_a_marker_of_an_unknown_schema_is_REFUSED(substrate):
    root, _store, env = substrate
    path = sp.write_marker(root, env=env, probe=FakeProbe())
    marker = json.loads(path.read_text(encoding="utf-8"))
    marker["schema"] = "dev-knowledge-substrate-provenance/99"
    path.write_text(json.dumps(marker), encoding="utf-8")

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "refused"


# --- the discriminator: the sibling lane's measured defect ---------------------------------

def test_substrate_id_separates_two_checkouts_on_one_machine(tmp_path):
    """The sibling lane's collision, as a property.

    Seven lanes on one workstation are SEVEN substrates by this definition, because a substrate
    is the pairing of a host and the checkout it serves — which is exactly the discrimination
    the fixed `/tmp` path did not have.
    """
    probe = FakeProbe()
    a = sp.substrate_id(tmp_path / "lane-a", env={}, probe=probe)
    b = sp.substrate_id(tmp_path / "lane-b", env={}, probe=probe)

    assert a != b
    assert a == sp.substrate_id(tmp_path / "lane-a", env={}, probe=probe)


def test_substrate_id_separates_two_hosts(tmp_path):
    root = tmp_path / "repo"
    assert (sp.substrate_id(root, env={}, probe=FakeProbe(node_name="host-a"))
            != sp.substrate_id(root, env={}, probe=FakeProbe(node_name="host-b")))


def test_codespace_name_discriminates_when_the_platform_supplies_it(tmp_path):
    root = tmp_path / "repo"
    one = sp.substrate_id(root, env={"CODESPACE_NAME": "aa-1"}, probe=FakeProbe())
    two = sp.substrate_id(root, env={"CODESPACE_NAME": "aa-2"}, probe=FakeProbe())
    assert one != two


def test_the_marker_path_is_discriminated_not_fixed(substrate, tmp_path):
    """Two lanes writing markers must not land on ONE file. The collision is structural."""
    root, _store, env = substrate
    other = tmp_path / "repo-2"
    other.mkdir()
    (other / "pyproject.toml").write_text(
        '[tool.uv]\nrequired-version = "==0.11.19"\n', encoding="utf-8")
    (other / ".python-version").write_text("3.12.10\n", encoding="utf-8")

    assert sp.marker_path(root, env=env, probe=FakeProbe()) != \
        sp.marker_path(other, env=env, probe=FakeProbe())


def test_marker_from_another_identity_is_REFUSED(substrate):
    """A well-formed marker is not proof. It must be the marker THIS substrate wrote.

    This is the sibling lane's defect with the path collision removed and the content attack
    left in: something put a valid marker where this substrate looks. Verifying that it reads
    back proves only that SOMETHING wrote it.
    """
    root, _store, env = substrate
    path = sp.write_marker(root, env=env, probe=FakeProbe())
    marker = json.loads(path.read_text(encoding="utf-8"))
    marker["substrate_id"] = "0" * 16          # another lane's identity, everything else fine
    path.write_text(json.dumps(marker), encoding="utf-8")

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "refused"
    assert any("identity" in r.lower() or "substrate" in r.lower()
               for r in verdict.refusals), verdict.refusals


def test_two_markers_present_verify_refuses_rather_than_reading_the_first(substrate, tmp_path):
    """The sibling lane's exact request: TWO markers, one foreign — REFUSE, do not pick one.

    The neighbour's marker is valid, current and complete; it is simply not ours. A verifier
    that scans the directory and accepts the first well-formed file it finds would pass here,
    which is the vacuous green this layer exists to abolish.
    """
    root, store, env = substrate
    other = tmp_path / "repo-2"
    other.mkdir()
    (other / "pyproject.toml").write_text(
        '[tool.uv]\nrequired-version = "==0.11.19"\n', encoding="utf-8")
    (other / ".python-version").write_text("3.12.10\n", encoding="utf-8")
    sp.write_marker(other, env=env, probe=FakeProbe())      # the neighbour's, written first

    env["CODESPACES"] = "true"
    verdict = sp.verify(root, env=env, probe=FakeProbe())   # ours has never been written

    assert len(list(store.glob("*.json"))) == 1             # a marker IS present in the dir
    assert verdict.status == "refused"


# --- the home rule ---------------------------------------------------------------------------

def test_provenance_dir_under_the_system_temp_dir_is_REFUSED(substrate):
    """A world-writable tmp path is the wrong home for an identity claim — ruled, not implied."""
    import tempfile
    root, _store, env = substrate
    env["DEV_KNOWLEDGE_PROVENANCE_DIR"] = str(Path(tempfile.gettempdir()) / "prov")

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "undetermined"
    assert any("tmp" in r.lower() or "temp" in r.lower() for r in verdict.refusals)


def test_an_unexpanded_variable_in_the_dir_is_REFUSED(substrate):
    """The class `provision.sh` already closed for its stamp, closed here too rather than twice.

    A host that hands us `${containerEnv:HOME}/...` literally created a junk directory in the
    working tree last time (`docs/audits/2026-08-19-technical-554-proof.md` §2.1).
    """
    root, _store, env = substrate
    env["DEV_KNOWLEDGE_PROVENANCE_DIR"] = "${containerEnv:HOME}/prov"

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "undetermined"


def test_the_default_home_is_not_the_system_temp_dir():
    """Nothing about the default may fall back to the shape the sibling lane measured."""
    import tempfile
    resolved = sp.provenance_dir(env={"HOME": "/home/vscode", "XDG_STATE_HOME": ""})
    assert Path(tempfile.gettempdir()) not in resolved.parents
    assert resolved != Path(tempfile.gettempdir())


# --- the staleness rule, stated rather than left to the reader --------------------------------

def test_a_marker_behind_the_live_tree_is_a_WARN_not_a_refusal(substrate):
    """THE RULE, and it is a decision: an ANCESTOR head is currency, not half-provisioning.

    `refresh_source_tree` fast-forwards the checkout AFTER provisioning by design, so a marker
    written one commit earlier is the NORMAL healthy state of a correct container. Refusing it
    would refuse every healthy container, which is how a gate becomes noise and then gets
    bypassed.
    """
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe(head="a" * 40))

    verdict = sp.verify(root, require_marker=True, env=env,
                        probe=FakeProbe(head="b" * 40, ancestors=[("a" * 40, "b" * 40)]))

    assert verdict.status == "ok", verdict.refusals
    assert any("behind" in w or "ancestor" in w for w in verdict.warnings), verdict.warnings


def test_a_marker_head_that_is_not_an_ancestor_is_REFUSED(substrate):
    """The other half of the rule. A DIVERGENT head describes a different history, so the
    marker is evidence about a tree this is not — which is the forgery shape arriving by
    accident (a prebuilt image serving a branch nobody is on)."""
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe(head="a" * 40))

    verdict = sp.verify(root, require_marker=True, env=env,
                        probe=FakeProbe(head="c" * 40, ancestors=[]))

    assert verdict.status == "refused"
    assert any("ancestor" in r or "diverge" in r for r in verdict.refusals), verdict.refusals


def test_a_moved_repo_pin_is_REFUSED(substrate):
    """`provision.sh --gate`'s staleness leg, preserved rather than lost in the port."""
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())
    (root / ".python-version").write_text("3.13.1\n", encoding="utf-8")

    verdict = sp.verify(root, env=env, probe=FakeProbe(), require_marker=True)

    assert verdict.status == "refused"


# --- exit codes: the repo's declared 0 / 1 / 2 split ------------------------------------------

def test_cli_exit_codes(substrate, capsys):
    """0 clean · 1 a real violation · 2 could not look (STANDING_RULINGS F4)."""
    root, _store, env = substrate
    sp.write_marker(root, env=env, probe=FakeProbe())

    assert sp.main(["verify", "--repo-root", str(root)], env=env, probe=FakeProbe()) == 0
    assert sp.main(["verify", "--repo-root", str(root), "--require-marker"],
                   env=env, probe=FakeProbe(tools={"uv": "0.1.0"})) == 1

    env2 = dict(env, DEV_KNOWLEDGE_PROVENANCE_DIR="${oops}/x")
    assert sp.main(["verify", "--repo-root", str(root)], env=env2, probe=FakeProbe()) == 2


@pytest.mark.live_repo
def test_provision_sh_writes_and_the_gate_verifies_the_marker():
    """L1 is WIRED, not merely written. A verifier nothing calls proves nothing.

    Asserted against the real `provision.sh` rather than a fixture, because the defect class
    here is a mechanism that exists beside the thing it is supposed to guard.
    """
    text = (_REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8")
    assert "scripts/substrate_provenance.py write" in text
    assert "scripts/substrate_provenance.py verify" in text
