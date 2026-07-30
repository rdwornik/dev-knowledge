"""[#446] FROZEN CONTRACT — RED-first (G-TDD) tests for the v6 rulings R1..R7.

Ruling source of truth: `docs/audits/2026-07-31-technical-v6-open-rulings.md` (R1..R7).
Spec source: `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md` (its "OPEN questions"
block, items 1-7 — the questions R1..R7 close).

FR numbering: **FR<n> == R<n>**. There is no pre-existing FR1..FR7 register for this work
(the fleet's other `FR-<n>` series belongs to intake #14 / #328 and is unrelated); this
module IS the register.

**This module is INTENTIONALLY RED at freeze.** Every test below asserts a mechanism the
[#446] build has not written yet, so `pytest tests/test_v6_frozen_contract.py` fails wholesale
until the build lands. That is the point: the architect reviews the frozen set before any
build code exists, and a test that passes at freeze is malformed (it is asserting something
already true, i.e. it has no teeth).

Suite-colour note: the freeze deliberately reds the repo suite. Collection is unaffected
(`validate_doc_claims` claim 3 uses `pytest --collect-only`, and is skipped in gate mode), so
no commit gate is blocked by the RED. If the architect prefers a green-suite freeze instead,
the one-line-per-test conversion is `@pytest.mark.xfail(strict=True)` — which then flips to
XPASS-fails-the-suite the moment the build lands. Not applied here: the operator's freeze
instruction is an explicit RED table.
"""
from __future__ import annotations

import inspect
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_handoff as gh  # noqa: E402
import verify_handoff_probes as vhp  # noqa: E402

_REPO = gh._REPO_ROOT
_COMMANDS = _REPO / ".claude" / "commands"

# --- R4 ruling pin ----------------------------------------------------------------
# The operator's R4 ruling text reads "<number> bytes on protocols/HANDOFF_BOOT.md" — a
# PLACEHOLDER, not a number. The sol draft is explicit that "A10 cannot close on a
# placeholder" (its OPEN question 4). So the ruled value is pinned here, in ONE place, and
# `test_fr4b_ruled_budget_is_pinned` stays RED until the architect supplies it. Do NOT
# invent a number to turn FR4b green.
#
# RULED 2026-07-31 (architect technical lane): 18,000 bytes. The rulings artifact records it
# as an APPENDED amendment (A1), not an in-place rewrite of the committed R4 placeholder line
# — `docs/audits/*` is immutable (CLAUDE.md §5 rule 3); `tests/` is not, so this pin moves in
# place. Live boot at freeze was 16,156 B, so the number is headroom over a measured file,
# never invented here.
_R4_RULED_BUDGET: int | None = 18000

# --- shared stub repo (mirrors tests/test_gen_handoff.py's harness) ---------------

_STUB_FILES = {
    "VISION.md": "# V\n\n## Vision\nWhat .dev-knowledge is.\n",
    "ARCHITECTURE.md": "# A\n\n## Purpose [CORE]\nLayer 2 of the ADR-28 model.\n",
    "scripts/audit.py": "ALL_CHECKS = []\n",
    "scripts/validate_git_backlog.py": "x\n",
    "scripts/validate_doc_claims.py": "x\n",
    "scripts/validate_backlog.py": "x\n",
    "scripts/gen_task_tree.py": "x\n",
    "BACKLOG.md": "x\n",
    "protocols/HANDOFF_PROCESS.md": "# H\n\nno per-bundle README\n",
    "ecosystem/doc-counts.md": "- tests: **1 collected**\n",
    "ecosystem/disposition-register.yaml": "dispositions: []\n",
    "docs/intake/README.md": "# INTAKE AREA DEFINITION\n",
    "docs/intake/2026-01-01-first.md": (
        "---\nintake-id: 1\nstatus: SEED\norigin: test\nconsumed-by:\n---\n\n"
        "# First Stub Intake\n"
    ),
}


def _stub_repo(tmp_path):
    repo = tmp_path / "repo"
    for rel, content in _STUB_FILES.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return repo


def _gen(tmp_path, *, mode="architect", slug="0000-00-00-t", **kw):
    repo = _stub_repo(tmp_path)
    return gh.generate(repo, mode=mode, slug=slug, repo=".dev-knowledge", date="2026-07-04",
                       bundle_root=repo / "docs" / "handoffs", **kw)


def _rows(bundle_dir):
    return {r["id"]: r for r in vhp.parse_probes((bundle_dir / "PROBES.md").read_text(encoding="utf-8"))}


def _row_text(row) -> str:
    return " ".join(row[c] for c in ("question", "source", "why", "command"))


# --- FR1 (R1) — /handoff-verify is a separate command, not a /handoff flag --------

def test_fr1_handoff_verify_is_a_separate_command():
    """R1: the one-round-trip boot is exposed as `/handoff-verify`, a SEPARATE command file.

    The generator stays answer-free, the checker answer-producing; a `--verify` flag on
    /handoff would recouple the ferry/proof boundary the anti-bluff contract protects.
    """
    cmd = _COMMANDS / "handoff-verify.md"
    assert cmd.is_file(), f"R1 unbuilt: {cmd.relative_to(_REPO)} absent"

    body = cmd.read_text(encoding="utf-8")
    # Sol draft §2: ONE command runs the whole gate and emits EXACTLY ONE evidence block.
    assert "evidence block" in body.lower(), "handoff-verify does not declare the single-evidence-block contract"

    # The generator must NOT grow a verify flag (R1's negative half).
    handoff = (_COMMANDS / "handoff.md").read_text(encoding="utf-8")
    assert "--verify" not in handoff, "/handoff grew a --verify flag; R1 rules a separate command"

    # /boot stays archived (R1's third clause).
    assert not (_COMMANDS / "boot.md").exists(), "/boot resurrected; R1 keeps it archived"


# --- FR2 (R2) — P0a/P0b/P0c standing-topic legs, with P0a's currency assertion ----

def test_fr2_p0_standing_topic_legs_are_emitted(tmp_path):
    """R2: adopt the intake definitions (proposal :110-112) with terra-H3 narrowing.

    P0a additionally asserts CURRENCY (`gen_task_tree --check` passes) alongside the ratified
    content assertion: BACKLOG.md is generated post-[#436], so a probe that can PASS on stale
    generated content is bluffable.
    """
    rows = _rows(_gen(tmp_path).bundle_dir)
    missing = [pid for pid in ("P0a", "P0b", "P0c") if pid not in rows]
    assert missing == [], f"R2 unbuilt: standing-topic legs absent from generated PROBES.md: {missing}"

    # §13(c) sequence: role -> vision -> standing topics -> backlog. P0 sits ABOVE P1.
    order = [r["id"] for r in vhp.parse_probes((_gen(tmp_path, slug="0000-00-00-u").bundle_dir
                                                / "PROBES.md").read_text(encoding="utf-8"))]
    assert order.index("P0a") < order.index("P1a"), f"P0 legs must precede P1: {order}"

    # P0a — the epic-theme preamble quote PLUS the generated-currency assertion.
    p0a = _row_text(rows["P0a"])
    assert "BACKLOG.md" in p0a, "P0a does not bind to BACKLOG.md's [E#] preambles"
    assert "gen_task_tree" in p0a and "--check" in p0a, \
        "P0a lacks the R2 SECOND assertion (gen_task_tree --check currency)"

    # P0b — live ACCEPTED/active intakes, TITLE lines only (terra-H3: no wave detail).
    p0b = _row_text(rows["P0b"])
    assert "docs/intake" in p0b, "P0b does not bind to docs/intake/*.md frontmatter"
    assert "ACCEPTED" in p0b, "P0b does not enumerate status: ACCEPTED intakes"

    # P0c — the bundle's own Purpose vs the P0a/P0b enumeration; unquotable = FAIL.
    p0c = _row_text(rows["P0c"])
    assert "FAIL" in p0c, "P0c does not state the unquotable/contradicted = FAIL outcome"


# --- FR3 (R3) — P3 compares live branch against the Destination row's branch ------

def test_fr3_p3_compares_live_branch_to_the_destination_row(tmp_path):
    """R3 (Option A): P3 compares `git branch --show-current` to the Destination row's branch
    field; mismatch = FAIL. Write-scope and MODE stay PROSE, outside P3 — a probe leg with no
    mechanical counterpart cannot fail honestly and discredits the block.
    """
    boot = (_REPO / "templates" / "handoff" / "v5" / "HANDOFF_BOOT.md.tmpl").read_text(encoding="utf-8")
    assert "Destination" in boot, "R3/A4 unbuilt: boot header carries no `Destination` row (P3's second operand)"

    rows = _rows(_gen(tmp_path).bundle_dir)
    p3 = _row_text(rows["P3"])
    assert "git branch --show-current" in p3, "P3 lost its live-branch command (R3 first operand)"
    assert "Destination" in p3, "R3 unbuilt: P3 names no Destination-row comparison target"
    # The negative half: no write-scope / MODE leg inside P3.
    assert "write-scope" not in p3.lower(), "P3 grew a write-scope leg; R3 keeps it prose"


# --- FR4 (R4) — HANDOFF_BOOT byte budget, mechanically enforced -------------------

def test_fr4a_boot_byte_budget_is_mechanically_enforced():
    """R4: a numeric byte budget on protocols/HANDOFF_BOOT.md, mechanically enforced.

    Home is the assembler's existing size machinery (`assemble_paste._SIZE_WARN_BYTES` at
    :32 is the precedent). Sol draft §5: the assembler action is a WARNING, not a blocking
    gate — so this test asserts the budget constant exists and the live boot is within it.
    """
    import assemble_paste as ap

    assert hasattr(ap, "HANDOFF_BOOT_BYTE_BUDGET"), \
        "R4 unbuilt: assemble_paste exposes no HANDOFF_BOOT_BYTE_BUDGET"
    budget = ap.HANDOFF_BOOT_BYTE_BUDGET
    assert isinstance(budget, int) and budget > 0, f"budget must be a positive int; got {budget!r}"

    live = (_REPO / "protocols" / "HANDOFF_BOOT.md").read_bytes()
    assert len(live) <= budget, f"protocols/HANDOFF_BOOT.md is {len(live)} bytes (> budget {budget})"


def test_fr4b_ruled_budget_is_pinned():
    """R4's NUMBER, not its mechanism. The ruling text supplied `<number>` — a placeholder.

    Per the sol draft's OPEN question 4, "A10 cannot close on a placeholder". This test is
    the mechanical record of that gap: it goes green when the architect rules the value and
    `_R4_RULED_BUDGET` is set here (one place), never by inventing a number in code.
    """
    assert _R4_RULED_BUDGET is not None, \
        "R4 numeric budget UNRULED (ruling text says `<number>`) - architect-blocked; A10 cannot close"

    import assemble_paste as ap
    assert ap.HANDOFF_BOOT_BYTE_BUDGET == _R4_RULED_BUDGET, \
        "the built budget diverges from the ruled number"


# --- FR5 (R5) — RM-8 overwrite refusal at the creation site -----------------------

def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def test_fr5_generation_refuses_a_bundle_dir_holding_tracked_files(tmp_path):
    """R5 (Option D): the target set is any bundle directory containing GIT-TRACKED files,
    guarded at the creation site (gen_handoff.py:436 — `exist_ok=True` removed). Default is
    REFUSE with a diagnostic naming the colliding directory and the escape hatch;
    `--allow-suffix` is explicit opt-in.

    Silent suffixing would convert today's collision into tomorrow's `_select_active_bundle`
    ambiguous-FAIL (audit.py:1575).
    """
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-collide"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    (bundle / "RESIDUAL.md").write_text("prior-window content\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "seed a TRACKED file inside the bundle dir")

    with pytest.raises(Exception) as exc:  # noqa: PT011 — the exception TYPE is the build's call
        gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge", date="2026-07-04",
                    bundle_root=repo / "docs" / "handoffs")
    msg = str(exc.value)
    assert slug in msg, f"the refusal diagnostic must name the colliding directory; got: {msg!r}"
    assert "--allow-suffix" in msg, f"the refusal diagnostic must name the escape hatch; got: {msg!r}"

    # The explicit opt-in proceeds (and does not clobber the tracked file).
    res = gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge", date="2026-07-04",
                      bundle_root=repo / "docs" / "handoffs", allow_suffix=True)
    assert res.bundle_dir != bundle, "--allow-suffix must write a NEW directory, not the collider"
    assert (bundle / "RESIDUAL.md").read_text(encoding="utf-8") == "prior-window content\n"


# --- FR6 (R6) — repo_root / cross_repo codified + CLI-mapped ----------------------

def test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped(tmp_path):
    """R6: codify the EXISTING semantics — `verify(bundle_path, repo_root=None,
    cross_repo=False)`, the :444 default call intact — and map them onto the CLI as
    `--repo-root PATH` / `--cross-repo`, with `--cross-repo` sans `--repo-root` a HARD ERROR.

    No silent root inference: that reproduces the original false-FAIL class.

    Codification half (signature) is already satisfied at freeze; the CLI half is the build.
    """
    sig = inspect.signature(vhp.verify)
    assert list(sig.parameters) == ["bundle_path", "repo_root", "cross_repo"], f"signature drifted: {sig}"
    assert sig.parameters["repo_root"].default is None
    assert sig.parameters["cross_repo"].default is False

    bundle = tmp_path / "b"
    bundle.mkdir()
    (bundle / "PROBES.md").write_text("no rows here\n", encoding="utf-8")

    # --cross-repo WITHOUT --repo-root is a hard error (not a silent inference, not a pass).
    rc = vhp.main([str(bundle), "--cross-repo"])
    assert rc not in (0, 1), \
        f"R6 unbuilt: `--cross-repo` without `--repo-root` returned {rc}; must be a HARD ERROR"

    # Both flags together are accepted and resolve against the passed root.
    rc = vhp.main([str(bundle), "--repo-root", str(tmp_path), "--cross-repo"])
    assert rc == 0, f"R6 unbuilt: `--repo-root` + `--cross-repo` rejected (rc={rc})"


# --- FR7 (R7) — [#421] absorption: BOTH tokenizer variants ------------------------

def test_fr7_v1_file_re_binds_repo_root_dotfiles():
    """R7 v1: `_FILE_RE` (:54) loses a leading dot in the FINAL path segment, so a repo-root
    dotfile fails to bind (`.pre-commit-config.yaml` -> `pre-commit-config.yaml`). A nested
    dotfile binds today because only the final segment is affected.
    """
    assert vhp.file_tokens("`.pre-commit-config.yaml`") == [".pre-commit-config.yaml"]
    assert vhp.file_tokens("`.markdownlint.json`") == [".markdownlint.json"]
    # Non-regression: already-working shapes must keep binding, unchanged.
    assert vhp.file_tokens("`.claude/settings.json`") == [".claude/settings.json"]
    assert vhp.file_tokens("`scripts/audit.py`") == ["scripts/audit.py"]


def test_fr7_v2_header_tokens_ignores_a_bare_id():
    """R7 v2: `header_tokens` (:131-133) treats any backtick span starting with `#` as a
    markdown header anchor, so a backticked ticket id (`#421`) mis-tokenizes as an anchor to
    resolve. A header is `#` + whitespace; a bare `#<digits>` is an id.
    """
    assert vhp.header_tokens("absorbed into `#421` this window") == []
    assert vhp.header_tokens("closes `#446`") == []
    # Non-regression: real headers must still tokenize.
    assert vhp.header_tokens("see `## Vision` here") == ["## Vision"]
    assert vhp.header_tokens("`## Purpose [CORE]`") == ["## Purpose [CORE]"]
