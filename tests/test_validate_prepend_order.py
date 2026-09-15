"""Tests for scripts/validate_prepend_order.py — the gate that makes
`protocols/PLAYBOOK.md` §Ch6 "### Order conventions" (PLAYBOOK.md:1399) refuse rather
than merely instruct. Row `[#786]`.

WHAT THE HEADING SAYS, AND WHAT THIS PINS. The heading declares four file classes. Two
of them are mechanically decidable from the tree alone and are what this gate enforces:

    - **Newest-first (prepend):** TOKEN-LOG, JOURNAL
    - **Append-only, newest-first (prepend):** LESSONS

For all three the decidable property is one line of algebra: with `tail(x)` = the text
of `x` from its FIRST dated entry heading onward,

    tail(staged) must END WITH tail(HEAD)

which simultaneously refuses (a) editing or deleting any pre-existing entry and (b)
inserting a new entry anywhere but the top of the entries region. The header block
ABOVE the first dated heading is deliberately outside the tail, so a `Last updated:`
stamp bump stays legal — that is the single most common real edit to these files and a
gate that blocked it would teach `--no-verify`.

RED-FIRST. Every test below was written and run against a stub `check_prepend` that
returns None unconditionally. The true-positive cases (P1..P5) FAILED; the
true-negative cases (N1..N6) PASSED — which is the point of the pairing: a gate that
refuses nothing passes every negative test, so negatives alone prove nothing.

BREACH HISTORY (why this heading and not an elegant one with no breaches). Measured on
this repo with `git log --numstat -- LESSONS.md`, three commits rewrote a file this
heading declares append-only, each authored by a seat that had read the prose:
    eb08075c 2026-05-16  155+/157-  "remove non-ISO ## Entries H2 + reorder pre-convention tail"
    99a104ed 2026-05-14   20+/20-   "rewrite 9 same-day LESSONS to canonical schema + relocate to file top"
    febafcac 2026-04-28    7+/25-   "docs(lessons): standardize entry format per ESSENTIALS spec"
P1 below is `99a104ed`'s shape, reduced to a two-entry fixture.

SELF-MATCH HAZARD (S1). A gate predicate that passes merely by reading the document
that declares it is decoration. This one cannot: the guarded set is three LOG files and
the declaring document is `protocols/PLAYBOOK.md`, which is not in it and is never
read. S1 pins that as a property rather than an observation.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import validate_prepend_order as vpo

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_prepend_order.py"

LESSONS_RE = r"^### \d{4}-\d{2}-\d{2}"

HEADER = (
    "# Lessons Learned — Append-Only Log\n"
    "\n"
    "> **Format:** `### YYYY-MM-DD | source | lesson | category | action taken`\n"
    "> New entries go at the top of the Entries section. Never edit old entries.\n"
    "> Last updated: 2026-05-13\n"
    "\n"
    "---\n"
    "\n"
)
E_OLD = "### 2026-05-12 | session | the oldest lesson | process | acted\n\n"
E_MID = "### 2026-05-13 | session | the middle lesson | process | acted\n\n"
E_NEW = "### 2026-05-14 | session | a brand new lesson | process | acted\n\n"

BASE = HEADER + E_MID + E_OLD


def _check(old, new, archives=()):
    return vpo.check_prepend(old, new, LESSONS_RE, archives)


# --- the acceptance matrix -------------------------------------------------
# P = true positive (a real violation, must be REFUSED)
# N = true negative (a conforming case, must be ALLOWED)

def test_p1_rewriting_an_existing_entry_in_place_is_refused():
    """P1 — `99a104ed`'s shape: an old entry's TEXT is rewritten. THE headline case."""
    mangled = HEADER + E_MID + "### 2026-05-12 | session | REWRITTEN in place | process | acted\n\n"
    v = _check(BASE, mangled)
    assert v is not None, "rewriting a pre-existing LESSONS entry must be REFUSED"
    assert "2026-05-12" in v.detail


def test_p2_deleting_an_existing_entry_is_refused():
    """P2 — `febafcac`'s shape: net deletion of pre-existing entry lines."""
    v = _check(BASE, HEADER + E_MID)
    assert v is not None, "deleting a pre-existing entry must be REFUSED"


def test_p3_appending_at_the_bottom_violates_newest_first():
    """P3 — the ORDER half of the heading, not the append-only half. Content is only
    ADDED (a naive no-deletions gate would allow it), but it lands at the wrong end."""
    v = _check(BASE, BASE + E_NEW)
    assert v is not None, "a new entry appended at the BOTTOM must be REFUSED"


def test_p4_inserting_between_two_existing_entries_is_refused():
    """P4 — insertion below the top splits the pre-existing tail."""
    v = _check(BASE, HEADER + E_MID + E_NEW + E_OLD)
    assert v is not None, "an entry inserted between two existing entries must be REFUSED"


def test_p5_archival_that_is_not_byte_identical_is_refused():
    """P5 — the ADR-29 escape is BYTE-IDENTICAL relocation. A relocation that edits
    while it moves is the exact thing the amendment does not license."""
    kept = HEADER + E_MID
    edited_archive = "# legacy\n\n### 2026-05-12 | session | the oldest lesson TWEAKED | process | acted\n\n"
    v = _check(BASE, kept, archives=(edited_archive,))
    assert v is not None, "a non-byte-identical archival must be REFUSED"


def test_n1_prepending_a_new_entry_at_the_top_is_allowed():
    """N1 — the normal, overwhelmingly common act. Must stay cheap and legal."""
    assert _check(BASE, HEADER + E_NEW + E_MID + E_OLD) is None


def test_n2_bumping_the_header_stamp_is_allowed():
    """N2 — `c099e783` is a real commit that did exactly this. The header block sits
    above the first dated heading and is outside the protected tail by construction."""
    bumped = BASE.replace("> Last updated: 2026-05-13", "> Last updated: 2026-05-14")
    assert bumped != BASE
    assert _check(BASE, bumped) is None


def test_n3_a_file_absent_from_head_is_allowed():
    """N3 — a newly created log has no pre-existing entries to protect."""
    assert _check("", BASE) is None


def test_n4_byte_identical_adr29_archival_is_allowed():
    """N4 — the ADR-29 amend. 2026-07-17 carve-out: a contiguous OLDER block may be
    relocated byte-identically into LESSONS-legacy-<span>.md."""
    kept = HEADER + E_MID
    archive = "# LESSONS-legacy-2026-05\n\n" + E_OLD
    assert _check(BASE, kept, archives=(archive,)) is None


def test_n5_prepend_plus_archive_in_one_commit_is_allowed():
    """N5 — the two legal moves composed: prepend at the top, archive from the bottom."""
    kept = HEADER + E_NEW + E_MID
    archive = "# LESSONS-legacy-2026-05\n\n" + E_OLD
    assert _check(BASE, kept, archives=(archive,)) is None


def test_n6_an_unchanged_file_is_allowed():
    """N6 — idempotence: --all over a clean tree must be silent, not noisy."""
    assert _check(BASE, BASE) is None


# --- the guarded set, the self-match hazard, and the vacuous run -----------

def test_s1_the_declaring_document_is_not_in_the_guarded_set():
    """S1 — SELF-MATCH GUARD. The predicate must not be satisfiable by reading the doc
    that specifies it. `protocols/PLAYBOOK.md` declares the rule; it is not guarded and
    is never opened by this gate. Pinned as a property so a later 'helpful' widening of
    GUARDED to protocols/ is a RED, not a silent tautology."""
    assert "protocols/PLAYBOOK.md" not in vpo.GUARDED
    assert not any(p.startswith("protocols/") for p in vpo.GUARDED)
    assert set(vpo.GUARDED) == {"LESSONS.md", "JOURNAL.md", "logs/TOKEN-LOG.md"}


def test_s2_the_verdict_does_not_depend_on_the_declaring_document():
    """S2 — the other half of S1, as behaviour: P1's verdict is computed from the log
    blobs alone, so it is identical whether PLAYBOOK.md is present, absent or lying."""
    mangled = HEADER + E_MID + "### 2026-05-12 | session | REWRITTEN in place | process | acted\n\n"
    first = _check(BASE, mangled)
    second = _check(BASE, mangled)
    assert first is not None and second is not None
    assert first.detail == second.detail


def test_each_guarded_file_uses_its_own_real_heading_pattern():
    """TOKEN-LOG's entry heading is `## YYYY-MM-DD`, not `### ` — a single shared
    pattern would silently protect nothing in that file (its tail would be empty, and
    an empty tail is a suffix of everything)."""
    tl_re = vpo.GUARDED["logs/TOKEN-LOG.md"]
    old = "# Token Usage Log\n\n## 2026-08-04 (delta)\nbody\n"
    mangled = "# Token Usage Log\n\n## 2026-08-04 (delta)\nEDITED\n"
    assert vpo.check_prepend(old, mangled, tl_re) is not None
    assert vpo.check_prepend(old, "# Token Usage Log\n\n## 2026-09-14 (delta)\nnew\n" + old.split("\n\n", 1)[1], tl_re) is None


def test_journal_heading_pattern_refuses_an_edited_entry():
    j_re = vpo.GUARDED["JOURNAL.md"]
    old = "# Journal\n\n---\n\n### 2026-09-14 (a) - CC: did a thing\nbody\n"
    mangled = old.replace("did a thing", "did a DIFFERENT thing")
    assert vpo.check_prepend(old, mangled, j_re) is not None


@requires_git
def test_a_bare_run_with_no_paths_and_no_all_refuses_to_be_vacuous(tmp_path):
    """Repo rule: 'a validator run with no args is a vacuous pass'. This one exits 2
    and says so rather than exiting 0 having inspected nothing."""
    r = subprocess.run([sys.executable, str(_SCRIPT)], cwd=str(tmp_path),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 2, r.stdout + r.stderr
    assert "--all" in (r.stdout + r.stderr)


# --- end-to-end: the gate armed as a REAL pre-commit hook ------------------
# The closure metric is not "the function returned a Violation" but "git refused the
# commit". A gate that returns 1 while git commits anyway passes the weaker test.

def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   text=True, encoding="utf-8", errors="replace")


def _try(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _init_repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    # ABSOLUTE hooks path: a relative spelling, or a global core.hooksPath on the
    # developer's box, disarms the hook and the test goes green proving nothing.
    _run(repo, "config", "core.hooksPath", str((repo / ".git" / "hooks").resolve()))
    (repo / "LESSONS.md").write_text(BASE, encoding="utf-8", newline="")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "seed")
    _run(repo, "branch", "-M", "main")
    return repo


def _arm(repo):
    hooks = repo / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    hook.write_text(
        "#!/bin/sh\n"
        f'exec "{Path(sys.executable).as_posix()}" "{_SCRIPT.as_posix()}" --all\n',
        encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    return hook


@requires_git
def test_e2e_armed_hook_refuses_a_real_in_place_rewrite(tmp_path):
    """E2E-P — the acceptance witness. A real `git commit` that rewrites a pre-existing
    LESSONS entry is REFUSED by a really-armed hook, and HEAD does not move."""
    repo = _init_repo(tmp_path)
    before = _try(repo, "rev-parse", "HEAD").stdout.strip()
    _arm(repo)
    (repo / "LESSONS.md").write_text(
        HEADER + E_MID + "### 2026-05-12 | session | REWRITTEN in place | process | acted\n\n",
        encoding="utf-8", newline="")
    _run(repo, "add", "-A")
    r = _try(repo, "commit", "-m", "rewrite an old entry")
    assert r.returncode != 0, "the armed hook must REFUSE the commit"
    assert _try(repo, "rev-parse", "HEAD").stdout.strip() == before, "HEAD must not move"
    assert "LESSONS.md" in (r.stdout + r.stderr)


@requires_git
def test_e2e_armed_hook_allows_a_real_prepend(tmp_path):
    """E2E-N — the same armed hook lets the normal act through. Without this, E2E-P is
    satisfied by a hook that refuses everything."""
    repo = _init_repo(tmp_path)
    before = _try(repo, "rev-parse", "HEAD").stdout.strip()
    _arm(repo)
    (repo / "LESSONS.md").write_text(HEADER + E_NEW + E_MID + E_OLD, encoding="utf-8", newline="")
    _run(repo, "add", "-A")
    r = _try(repo, "commit", "-m", "prepend a new entry")
    assert r.returncode == 0, r.stdout + r.stderr
    assert _try(repo, "rev-parse", "HEAD").stdout.strip() != before, "HEAD must move"
