"""Unit tests for scripts/check_seal_identity.py ([#475] — seal identity as a pre-commit gate).

[#473] made `gen_handoff` refuse to SEAL a bundle whose internal slug != its own directory,
but that refusal governs only the machine generation path. A hand-renamed directory, an
edited Slug row, or a copied bundle all reach `git commit` unchecked — and a committed
bundle is immutable, so the defect is permanent (live proof: the 2026-08-02 boot absorbed
three sealed probe rows naming the un-suffixed sibling bundle). This gate runs
`verify_seal_identity` over the bundle dirs of staged `docs/handoffs/**` files at
pre-commit, where the artifact becomes durable.

FR map ([#475] execution contract):
  FR1 — fires only via staged docs/handoffs/** paths (no paths -> no-op, exit 0)
  FR2 — violation FAILS loudly, naming the file, the expected identity, the found locator
  FR3 — integrates with the existing .pre-commit-config.yaml local-hook mechanism
  FR4 — exit codes honest: 0 clean, 1 violation, 2 internal error (never a silent pass)
  FR5 — the live defect class (internal locator naming a sibling directory) has a fixture
"""

import importlib.util
import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "check_seal_identity.py"


@pytest.fixture(scope="module")
def gate():
    assert _SCRIPT.exists(), "scripts/check_seal_identity.py does not exist — the gate is unbuilt"
    spec = importlib.util.spec_from_file_location("check_seal_identity", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _bundle(tmp_path: Path, dirname: str, declared_slug: str) -> Path:
    """A minimal handoff bundle whose HANDOFF_BOOT.md declares `declared_slug`."""
    d = tmp_path / "docs" / "handoffs" / dirname
    d.mkdir(parents=True)
    (d / "HANDOFF_BOOT.md").write_text(
        f"# boot\n\n| **Slug** | `{declared_slug}` |\n", encoding="utf-8")
    return d


# --- FR5: the live defect class — internal locator names a sibling directory ---
def test_mismatched_slug_blocks_and_names_the_file(gate, tmp_path, capsys):
    d = _bundle(tmp_path, "2026-08-02-w2-arc", "2026-08-02-w2-arc-2")
    rc = gate.main([str(d / "HANDOFF_BOOT.md")])
    err = capsys.readouterr().err
    assert rc == 1
    assert "HANDOFF_BOOT.md" in err                    # the offending file
    assert "2026-08-02-w2-arc-2" in err                # the found locator
    assert "2026-08-02-w2-arc" in err                  # the expected identity


# --- FR4/clean: a conforming bundle passes ------------------------------------
def test_clean_bundle_passes(gate, tmp_path):
    d = _bundle(tmp_path, "2026-08-02-w2-arc", "2026-08-02-w2-arc")
    assert gate.main([str(d / "HANDOFF_BOOT.md")]) == 0


# --- FR1: no docs/handoffs/** staged -> no-op ---------------------------------
def test_no_staged_handoff_files_is_a_noop(gate, capsys):
    assert gate.main([]) == 0
    out = capsys.readouterr()
    assert out.err == ""


def test_non_bundle_handoff_paths_are_skipped(gate, tmp_path):
    # docs/handoffs/README.md sits at the root of the genre dir — it is not a bundle
    # and must never invent one (verify_seal_identity would no-op anyway, but the
    # path->bundle derivation itself must not map it to docs/handoffs).
    root_doc = tmp_path / "docs" / "handoffs" / "README.md"
    root_doc.parent.mkdir(parents=True)
    root_doc.write_text("index\n", encoding="utf-8")
    assert gate.main([str(root_doc)]) == 0


def test_many_staged_files_verify_each_bundle_once(gate, tmp_path, monkeypatch):
    d = _bundle(tmp_path, "2026-08-02-w2-arc", "2026-08-02-w2-arc")
    (d / "PROBES.md").write_text("p\n", encoding="utf-8")
    seen = []
    real = gate.verify_seal_identity
    monkeypatch.setattr(gate, "verify_seal_identity",
                        lambda bundle: (seen.append(Path(bundle)), real(bundle))[1])
    assert gate.main([str(d / "HANDOFF_BOOT.md"), str(d / "PROBES.md")]) == 0
    assert len(seen) == 1  # deduped: one bundle, one verification


# --- FR4: an internal error is a BLOCK, never a silent pass -------------------
def test_internal_error_is_nonzero_not_a_pass(gate, tmp_path, monkeypatch, capsys):
    d = _bundle(tmp_path, "2026-08-02-w2-arc", "2026-08-02-w2-arc")

    def boom(bundle):
        raise RuntimeError("synthetic verifier crash")

    monkeypatch.setattr(gate, "verify_seal_identity", boom)
    rc = gate.main([str(d / "HANDOFF_BOOT.md")])
    assert rc == 2
    assert "INTERNAL ERROR" in capsys.readouterr().err


# --- FR3: the hook leg is wired into the EXISTING pre-commit mechanism --------
def test_hook_is_registered_and_its_pattern_derives_the_gated_paths():
    """Structural, not enumerated: the gated-path assertions compile the hook's OWN
    `files:` regex out of .pre-commit-config.yaml rather than hand-mirroring it."""
    import yaml

    cfg = yaml.safe_load((_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = [h for repo in cfg["repos"] for h in repo["hooks"]]
    matches = [h for h in hooks if h.get("id") == "check-seal-identity"]
    assert matches, "check-seal-identity hook is not registered in .pre-commit-config.yaml"
    hook = matches[0]
    assert "check_seal_identity" in hook["entry"]
    # pre-commit passes the staged filenames (its default; stated explicitly here so a
    # config edit flipping it off fails this test rather than silently un-arming FR1).
    assert hook.get("pass_filenames", True) is True
    pattern = re.compile(hook["files"])
    assert pattern.search("docs/handoffs/2026-08-02-x/HANDOFF_BOOT.md")
    assert pattern.search("docs/handoffs/2026-08-02-x/PROBES.md")
    assert not pattern.search("BACKLOG.md")
    assert not pattern.search("protocols/HANDOFF_PROCESS.md")
