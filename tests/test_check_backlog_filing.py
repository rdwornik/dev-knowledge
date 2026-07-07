"""Unit tests for scripts/check_backlog_filing.py (filing-backpressure + #279 intake WARN).

Contract-1 (leg 1): a commit ADDING a new task id must carry a `kill-candidates:` line.
Contract-3 (leg 3 / #279): a new L-sized new-feature epic lacking an intake-id -> advisory WARN.

Anti-vacuous-pass pin: the REAL_* fixtures are copied VERBATIM from live BACKLOG.md so the
L-band detection is pinned against the on-disk format, not a hand-mirror of the regex.
"""

import importlib.util
from pathlib import Path

_H = Path(__file__).resolve().parent.parent / "scripts" / "check_backlog_filing.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_backlog_filing", _H)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = _load()

# --- synthetic -U0 diff fragments (removed '-', added '+') --------------------
D_ADD_S = "@@ -0 +1 @@\n+- [#900] [P3][S] small new task · Done when: x\n"
D_ADD_M = "@@ -0 +1 @@\n+- [#901] [P2][M] medium task · Done when: y\n"
D_ADD_L = "@@ -0 +1 @@\n+- [#902] [P2][L] big new-feature epic · Done when: z\n"
D_ADD_L_INTAKE = "@@ -0 +1 @@\n+- [#903] [P2][L] big epic (intake-id 3) · Done when: z\n"
D_ADD_L_CHORE = "@@ -0 +1 @@\n+- [#904] [P2][L] chore: bulk relabel of stale bands · Done when: z\n"
D_ADD_L_NA = "@@ -0 +1 @@\n+- [#905] [P2][L] big epic · intake: n/a -- pure infra migration · Done when: z\n"
D_REWORD = "@@ -10 +10 @@\n-- [#900] [P3][S] old · Done when: x\n+- [#900] [P3][S] new · Done when: x\n"
D_REMOVE = "@@ -10 +9 @@\n-- [#900] [P3][S] gone · Done when: x\n"

_KILL = "feat: add a task\n\nkill-candidates: #12"
_KILL_NONE = "feat: add a task\n\nkill-candidates: none -- nothing stale to prune"
_NOKILL = "feat: add a task"

# --- REAL lines copied VERBATIM from live BACKLOG.md (anti-vacuous pin) --------
# L-sized (#2) -- must be detected as an L-epic:
REAL_L = ("@@ -0 +1 @@\n+- [#2] [P2][L] Add contradiction-detection across decisions + an "
          "ownership model (amend vs new ADR vs clarification) · Done when: a detection "
          "mechanism + ownership rule exist · refs ADR-64 (consolidated-index sub-item done)\n")
# M-sized (#15) -- must NOT be detected as an L-epic (size gate excludes it):
REAL_M = ("@@ -0 +1 @@\n+- [#15] [P2][M] Add hyphen-only-separator enforcement (pre-commit + "
          "Action) with a scoped path set + exceptions · Done when: a non-conforming new "
          "filename is blocked · refs ADR-34 · serialize-group: pre-commit-config\n")


# --- Leg 1: filing backpressure (BLOCK) ---------------------------------------
def test_add_without_kill_candidates_blocks():
    block, _ = hook.check(_NOKILL, D_ADD_S)
    assert block  # non-empty -> commit rejected


def test_add_with_kill_id_passes():
    block, _ = hook.check(_KILL, D_ADD_S)
    assert block == []


def test_add_with_kill_none_passes():
    block, _ = hook.check(_KILL_NONE, D_ADD_S)
    assert block == []


def test_reword_does_not_trigger_block():
    block, _ = hook.check(_NOKILL, D_REWORD)
    assert block == []


def test_remove_only_does_not_trigger_block():
    block, _ = hook.check(_NOKILL, D_REMOVE)
    assert block == []


def test_no_backlog_change_passes():
    block, warn = hook.check(_NOKILL, "")
    assert block == [] and warn == []


# --- Leg 3: #279 intake-id advisory (WARN, never blocks) ----------------------
def test_new_l_epic_without_intake_warns():
    _, warn = hook.check(_KILL, D_ADD_L)
    assert warn  # advisory WARN present


def test_new_l_epic_warn_never_blocks():
    block, warn = hook.check(_KILL, D_ADD_L)
    assert warn and block == []  # advisory only -- WARN does not gate


def test_new_l_epic_with_intake_no_warn():
    _, warn = hook.check(_KILL, D_ADD_L_INTAKE)
    assert warn == []


def test_new_l_epic_na_escape_no_warn():
    _, warn = hook.check(_KILL, D_ADD_L_NA)
    assert warn == []


def test_l_chore_is_exempt():
    _, warn = hook.check(_KILL, D_ADD_L_CHORE)
    assert warn == []


def test_small_and_medium_no_warn():
    _, warn_s = hook.check(_KILL, D_ADD_S)
    _, warn_m = hook.check(_KILL, D_ADD_M)
    assert warn_s == [] and warn_m == []


# --- Anti-vacuous pin: REAL BACKLOG lines verbatim ----------------------------
def test_real_l_line_is_detected_as_l_epic():
    # #2 is a real [P2][L] entry with no intake citation -> must WARN.
    _, warn = hook.check(_KILL, REAL_L)
    assert warn


def test_real_m_line_is_not_flagged():
    # #15 is a real [P2][M] entry -> size gate excludes it, no WARN.
    _, warn = hook.check(_KILL, REAL_M)
    assert warn == []
