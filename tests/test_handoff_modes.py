"""Live-file structural fence for the two-mode handoff (#150).

Unlike the hermetic tmp_path fixtures elsewhere, these tests read the ACTUAL repo
surfaces — that is deliberate. The operator's binding condition for #150 was "no
fake-green": the spec must not *claim* a capability it doesn't carry. So these assert
that the architect|execution mode switch, the §5 exact-line orientation probe (NOT a
paraphrasable answer), the honest ephemeral-task-graph framing, and the "no new
artifact" return channel are actually PRESENT in the v5 spec / boot / command — and
that PLAYBOOK pointerizes rather than re-describes them. They go RED on silent drift.
"""

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


# --- HANDOFF_PROCESS_v5.md §13 -------------------------------------------------

def test_v5_spec_defines_both_modes() -> None:
    spec = _read("protocols/HANDOFF_PROCESS_v5.md")
    assert "13. Modes" in spec
    assert "architect | execution" in spec
    assert "### Execution mode" in spec
    assert "### Architect mode" in spec


def test_v5_orientation_is_exact_line_probe_not_paraphrase() -> None:
    """The precision fix: orientation is a §5 exact-line/substring quote, explicitly NOT a
    paraphrasable plain-language answer (which would be summary-bluffable, re-opening scope-D).
    """
    spec = _read("protocols/HANDOFF_PROCESS_v5.md").lower()
    assert "exact-line" in spec
    assert "substring" in spec
    assert "paraphrase" in spec          # paraphrase explicitly rejected
    assert "vision.md" in spec
    assert "architecture.md" in spec


def test_v5_task_graph_framed_honestly_ephemeral() -> None:
    """No fake-green: the architect task-graph is ephemeral-in-residual this pass, NOT a
    durable BACKLOG-resident graph; durable encoding is named-successor #156."""
    spec = _read("protocols/HANDOFF_PROCESS_v5.md")
    low = spec.lower()
    assert "#156" in spec
    assert "ephemeral" in low
    assert "durable" in low


def test_v5_return_channel_adds_no_new_artifact() -> None:
    spec = _read("protocols/HANDOFF_PROCESS_v5.md").lower()
    assert "return channel" in spec
    assert "no new artifact" in spec


# --- HANDOFF_BOOT.md: both postures travel in the one boot file ----------------

def test_boot_carries_both_postures() -> None:
    boot = _read("protocols/HANDOFF_BOOT.md")
    low = boot.lower()
    assert "execution mode (default)" in low          # the reactive role, mode-labelled
    assert "Architect mode" in boot
    assert "generative posture" in low
    assert "orient first" in low                      # orientation is the first move
    assert "orientation probe" in low
    assert "substring-check" in low                   # exact-line probe, not a paraphrase


# --- .claude/commands/handoff.md: mode param + coupled-surface preserved -------

def test_command_carries_mode_param() -> None:
    cmd = _read(".claude/commands/handoff.md")
    assert "Mode (v5 only)" in cmd
    assert "architect" in cmd and "execution" in cmd
    assert "v5 architect" in cmd


def test_command_v4_coupled_surface_untouched() -> None:
    """The line-2 v4 declaration is an audit.py coupled surface — adding the v5 mode param
    must not disturb it (it moves only at the #149/ADR-82 flip)."""
    cmd = _read(".claude/commands/handoff.md")
    assert "per HANDOFF_PROCESS.md v4" in cmd


# --- PLAYBOOK §8: pointerize, do NOT re-describe -------------------------------

def test_playbook_pointerizes_modes_not_describes() -> None:
    pb = _read("protocols/PLAYBOOK.md")
    assert "HANDOFF_PROCESS_v5.md` §13" in pb          # the pointer
    # the modes are NOT re-described as sections here (resident-copy drift is the failure)
    assert "### Architect mode" not in pb
    assert "### Execution mode" not in pb
