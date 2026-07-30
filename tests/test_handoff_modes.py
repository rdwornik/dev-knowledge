"""Live-file structural fence for the two-mode handoff (#150).

Unlike the hermetic tmp_path fixtures elsewhere, these tests read the ACTUAL repo
surfaces — that is deliberate. The operator's binding condition for #150 was "no
fake-green": the spec must not *claim* a capability it doesn't carry. So these assert
that the architect|execution mode switch, the §5 exact-line orientation probe (NOT a
paraphrasable answer), the honest ephemeral-task-graph framing, and the "no new
artifact" return channel are actually PRESENT in the v5 spec / boot / command — and
that PLAYBOOK pointerizes rather than re-describes them. They go RED on silent drift.
"""

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.live_repo  # whole file asserts live protocol/command docs

_REPO = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


# --- HANDOFF_PROCESS.md §13 (canonical v5) ------------------------------------

def test_v5_spec_defines_both_modes() -> None:
    spec = _read("protocols/HANDOFF_PROCESS.md")
    assert "13. Modes" in spec
    assert "architect | execution" in spec
    assert "### Execution mode" in spec
    assert "### Architect mode" in spec


def test_v5_orientation_is_exact_line_probe_not_paraphrase() -> None:
    """The precision fix: orientation is a §5 exact-line/substring quote, explicitly NOT a
    paraphrasable plain-language answer (which would be summary-bluffable, re-opening scope-D).
    """
    spec = _read("protocols/HANDOFF_PROCESS.md").lower()
    assert "exact-line" in spec
    assert "substring" in spec
    assert "paraphrase" in spec          # paraphrase explicitly rejected
    assert "vision.md" in spec
    assert "architecture.md" in spec


def test_v5_task_graph_framed_honestly_ephemeral() -> None:
    """No fake-green: the architect task-graph is ephemeral-in-residual this pass, NOT a
    durable BACKLOG-resident graph; durable encoding is named-successor #156."""
    spec = _read("protocols/HANDOFF_PROCESS.md")
    low = spec.lower()
    assert "#156" in spec
    assert "ephemeral" in low
    assert "durable" in low


def test_v5_return_channel_adds_no_new_artifact() -> None:
    spec = _read("protocols/HANDOFF_PROCESS.md").lower()
    assert "return channel" in spec
    assert "no new artifact" in spec


def test_v5_architect_carries_operator_context_beat() -> None:
    """Architect mode adds a lightweight operator-context beat: ONE off-repo-only ask
    (intent / priorities / off-repo findings / changed decisions) AFTER orient, BEFORE design —
    the channel a repo-derived residual structurally cannot carry. Architect-only; NOT the
    residual; NOT the v4 interview."""
    spec = _read("protocols/HANDOFF_PROCESS.md").lower()
    assert "operator-context" in spec          # the beat is named
    assert "off-repo" in spec                  # off-repo-only scope
    assert "architect mode only" in spec       # architect-only, not execution
    assert "eight-file interview" in spec      # framed as explicitly NOT the heavy v4 interview
    assert "residual" in spec                  # framed against (distinct from) the residual


# --- HANDOFF_BOOT.md: both postures travel in the one boot file ----------------

def test_boot_carries_both_postures() -> None:
    boot = _read("protocols/HANDOFF_BOOT.md")
    low = boot.lower()
    assert "execution mode (default)" in low          # the reactive role, mode-labelled
    assert "Architect mode" in boot
    assert "generative posture" in low
    assert "understand the vision" in low             # opening sequence: role -> vision -> backlog
    assert "navigation gate" in low                   # grep demoted to a tool, backlog navigates
    assert "orientation probe" in low
    assert "substring-check" in low                   # exact-line probe, not a paraphrase


def test_boot_ack_is_mode_neutral() -> None:
    """The on-load ack fires BEFORE the browser knows its mode (mode comes from CC's
    handoff, read at step 3), so the ack must name the Layer-1 actor, not a mode — it
    must never claim 'architect' on load (the execution-session mislabel this fixes)."""
    boot = _read("protocols/HANDOFF_BOOT.md")
    ack = next(line for line in boot.splitlines() if "Booted" in line)
    assert "Layer-1 browser" in ack
    assert "architect" not in ack.lower()


def test_boot_architect_posture_carries_operator_context_step() -> None:
    """The architect posture carries the operator-context step: ONE off-repo-only ask, after
    orient and before decomposition (HANDOFF_PROCESS v5 §13)."""
    boot = _read("protocols/HANDOFF_BOOT.md").lower()
    assert "ask the operator for off-repo context" in boot
    assert "off-repo" in boot


# --- .claude/commands/handoff.md: mode param + coupled-surface preserved -------

def test_command_carries_mode_param() -> None:
    cmd = _read(".claude/commands/handoff.md")
    assert "Mode:" in cmd
    assert "architect" in cmd and "execution" in cmd
    assert "v5 architect" in cmd


def test_command_coupled_surface_is_canonical_major() -> None:
    """The command's coupled-surface declaration (read by audit.py check_amendment_coherence)
    names the CANONICAL major. Post-#149 flip that was v5; [#446] cut v6, and the declaration
    moved with it — check_amendment_coherence FAILs the straggler otherwise, which is how this
    drift was caught. Derived from the live spec header, never hardcoded twice."""
    spec = _read("protocols/HANDOFF_PROCESS.md")
    major = re.search(r"^Version:\s*(\d+)\.", spec, re.MULTILINE).group(1)
    cmd = _read(".claude/commands/handoff.md")
    assert f"per HANDOFF_PROCESS.md v{major}" in cmd


# --- PLAYBOOK §8: pointerize, do NOT re-describe -------------------------------

def test_playbook_pointerizes_modes_not_describes() -> None:
    pb = _read("protocols/PLAYBOOK.md")
    assert "HANDOFF_PROCESS.md` §13" in pb          # the pointer (canonical v5)
    # the modes are NOT re-described as sections here (resident-copy drift is the failure)
    assert "### Architect mode" not in pb
    assert "### Execution mode" not in pb
