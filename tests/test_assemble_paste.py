"""Tests for scripts/assemble_paste.py."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "assemble_paste.py"
TEMPLATE = (
    Path(__file__).parent.parent / "templates" / "handoff" / "v5" / "SUPPLEMENT.md.tmpl"
)

# The fixed divider the generated SUPPLEMENT.md carries between the QUESTIONS (for the
# OUTGOING browser) and the operator-pasted ANSWERS (folded into the next paste). The
# assembler keys on this substring; tests assert answers fold and questions/divider do not.
_ANSWERS_MARKER = (
    "===================== PASTE CHAT ANSWERS BELOW THIS LINE ====================="
)
# A distinctive QUESTIONS-section substring that must NOT leak into PASTE_THIS (the
# questions are for the outgoing browser, never the incoming session).
_QUESTIONS_MARKER = "QUESTIONS — paste these to the outgoing architect chat"


def _supplement_text(answers: str = "Strategic brief.") -> str:
    """A SUPPLEMENT.md in the v5.2 fillable shape: questions + divider + answers region.

    `answers` is the text below the divider (what the operator pastes). Pass "" (or a
    comment-only / whitespace string) to model an unfilled cold-handoff supplement.
    """
    return (
        "# Architect strategic supplement — test\n\n"
        f"## {_QUESTIONS_MARKER}\n\n"
        "1. **Strategic intent** — ...\n"
        "6. **Off-repo context** — ...\n\n"
        f"{_ANSWERS_MARKER}\n"
        "<!-- operator: paste answers here; leave empty if there is no outgoing chat -->\n"
        f"{answers}\n"
    )


def _make_bundle(
    tmp_path: Path,
    *,
    with_handoff_boot: bool = True,
    with_supplement: bool = True,
    supplement_answers: str = "Strategic brief.",
    mode: str | None = None,
) -> tuple[Path, Path]:
    """Create a minimal fake repo tree under tmp_path.

    Returns (bundle_dir, script_copy) where script_copy is placed under
    tmp_path/scripts/ so that Path(__file__).parent.parent resolves to tmp_path
    (making repo_root point at our fake protocols/ dir).
    """
    # fake protocols/HANDOFF_BOOT.md
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    (protocols / "HANDOFF_BOOT.md").write_text("# Boot\n\nRole content.", encoding="utf-8")

    # fake bundle
    bundle = tmp_path / "bundle"
    bundle.mkdir()

    if with_handoff_boot:
        # mode=None reproduces the pre-v5.1 header byte-for-byte (no Mode row); a set
        # mode injects the `| **Mode** | **architect** ... |` row v5 §13 bundles emit.
        mode_row = f"| **Mode** | **{mode}** (test) |\n" if mode else ""
        (bundle / "HANDOFF_BOOT.md").write_text(
            "# Handoff boot\n\n| Field | Value |\n|---|---|\n| **Slug** | test |\n"
            + mode_row
            + "\n## What the operator does\n\nSteps go here.\n",
            encoding="utf-8",
        )

    (bundle / "RESIDUAL.md").write_text("# Residual\n\nDrift flags.", encoding="utf-8")
    (bundle / "PROBES.md").write_text("# Probes\n\nP1 probe here.", encoding="utf-8")

    if with_supplement:
        (bundle / "SUPPLEMENT.md").write_text(
            _supplement_text(supplement_answers), encoding="utf-8"
        )

    # copy the script into tmp_path/scripts/ so repo_root = tmp_path
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    script_copy = scripts_dir / "assemble_paste.py"
    shutil.copy(SCRIPT, script_copy)
    # assemble_paste.py resolves `from gen_handoff import reflow_framing` at runtime via
    # sys.path[0] = its own dir, so its sibling must sit beside it in the temp scripts/ dir.
    shutil.copy(SCRIPT.parent / "gen_handoff.py", scripts_dir / "gen_handoff.py")

    return bundle, script_copy


def _run(script: Path, bundle: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), str(bundle)],
        capture_output=True,
        text=True,
    )


def _labels(paste: str) -> list[str]:
    # The terminal END sentinel (intake #18 A1) is not a section — excluded here; its own
    # tests assert it directly.
    return [
        line.removeprefix("=== ").removesuffix(" ===")
        for line in paste.splitlines()
        if line.startswith("=== ") and not line.startswith("=== END OF PASTE")
    ]


# ------------------------------------------------------------------ #
# Test 1: All five sections present in order (session header + 4 manifest)
# ------------------------------------------------------------------ #

def test_all_sections_in_order(tmp_path: Path) -> None:
    """PASTE_THIS.md contains 5 sections in correct order when all sources exist.

    The default bundle's supplement carries pasted answers, so its ANSWERS region folds
    in as the `SUPPLEMENT.md` section.
    """
    bundle, script = _make_bundle(tmp_path)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    assert _labels(paste) == [
        "HANDOFF_BOOT.md (session header)",
        "protocols/HANDOFF_BOOT.md",
        "RESIDUAL.md",
        "PROBES.md",
        "SUPPLEMENT.md",
    ], f"Unexpected section order: {_labels(paste)}"

    # 4 between the 5 sections + 1 before the END sentinel (intake #18 A1)
    assert paste.count("\n\n---\n\n") == 5


# ------------------------------------------------------------------ #
# Test 2: Missing SUPPLEMENT (non-architect) skips gracefully
# ------------------------------------------------------------------ #

def test_missing_supplement_skips_gracefully(tmp_path: Path) -> None:
    """Missing SUPPLEMENT.md: exits 0, [skip] on stderr, 4 sections in paste."""
    bundle, script = _make_bundle(tmp_path, with_supplement=False)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[skip]" in result.stderr

    labels = _labels((bundle / "PASTE_THIS.md").read_text(encoding="utf-8"))
    assert "SUPPLEMENT.md" not in labels
    assert "RESIDUAL.md" in labels
    assert "PROBES.md" in labels
    assert len(labels) == 4


# ------------------------------------------------------------------ #
# Test 3: Missing required source exits nonzero, no PASTE_THIS.md written
# ------------------------------------------------------------------ #

def test_missing_required_source_exits_nonzero(tmp_path: Path) -> None:
    """Missing RESIDUAL.md (required): exits nonzero, PASTE_THIS.md not created."""
    bundle, script = _make_bundle(tmp_path)
    (bundle / "RESIDUAL.md").unlink()

    result = _run(script, bundle)

    assert result.returncode != 0, "Expected nonzero exit on missing required source"
    assert not (bundle / "PASTE_THIS.md").exists(), (
        "PASTE_THIS.md must not be written when a required source is missing"
    )


# ------------------------------------------------------------------ #
# Test 4: Self-containment — each source BODY is inlined verbatim
# ------------------------------------------------------------------ #

def test_each_source_body_is_inlined_verbatim(tmp_path: Path) -> None:
    """A distinctive body substring from every source must appear in the output.

    The original defect was the bundle *pointing at* protocols/HANDOFF_BOOT.md
    instead of inlining it — a partial boot for the file-less browser. A label-only
    check (test_all_sections_in_order) would not catch a pointer regression, since
    the section header would still be present. This asserts the actual file BODIES
    are inlined, so a pointer swapped in under the correct section label FAILS — the
    hard self-containment metric, not just section presence.
    """
    bundle, script = _make_bundle(tmp_path)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    # the load-bearing one: the resident role file body must be INLINED, not pointed at
    assert "Role content." in paste, (
        "protocols/HANDOFF_BOOT.md body not inlined — pointer regression (the original flaw)"
    )
    # the other source bodies must each appear verbatim
    assert "Drift flags." in paste       # RESIDUAL.md
    assert "P1 probe here." in paste     # PROBES.md
    assert "Strategic brief." in paste   # SUPPLEMENT.md — the folded ANSWERS region
    # the session-header is extracted only up to the first '## ' heading:
    # the slug (before the heading) is inlined; body under the heading is excluded
    assert "test" in paste                  # slug, from the Field/Value table
    assert "Steps go here." not in paste     # body under '## What the operator does' — out


# ------------------------------------------------------------------ #
# Test 5: Idempotency — two regenerations are byte-identical
# ------------------------------------------------------------------ #

def test_regeneration_is_byte_identical(tmp_path: Path) -> None:
    """Re-running the assembler on unchanged sources yields byte-identical output.

    HANDOFF_PROCESS §13 instructs "regenerate each handoff by re-running the
    assembler"; idempotency is what makes that a safe no-op (no churn, clean tree).
    """
    bundle, script = _make_bundle(tmp_path)

    assert _run(script, bundle).returncode == 0
    first = (bundle / "PASTE_THIS.md").read_bytes()
    assert _run(script, bundle).returncode == 0
    second = (bundle / "PASTE_THIS.md").read_bytes()

    assert first == second, "assembler output is not idempotent (regeneration churns)"


# ------------------------------------------------------------------ #
# Test 6: Architect mode + absent SUPPLEMENT skips softly (v5.2)
# ------------------------------------------------------------------ #

def test_architect_mode_absent_supplement_skips_softly(tmp_path: Path) -> None:
    """Architect mode + missing SUPPLEMENT.md: exit 0, a [skip], NOT a [warn].

    v5.2: the supplement is now *always generated*, so a genuinely-absent file is an
    anomaly but still non-fatal (advisory) — a soft [skip] noting it is expected, never
    the old [warn]. PASTE_THIS.md is still written.
    """
    bundle, script = _make_bundle(tmp_path, with_supplement=False, mode="architect")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[skip]" in result.stderr
    assert "[warn]" not in result.stderr
    assert "architect" in result.stderr.lower()

    labels = _labels((bundle / "PASTE_THIS.md").read_text(encoding="utf-8"))
    assert "SUPPLEMENT.md" not in labels  # advisory — still assembles without it


# ------------------------------------------------------------------ #
# Test 7: Architect mode + answered SUPPLEMENT folds ANSWERS only (v5.2)
# ------------------------------------------------------------------ #

def test_architect_mode_answered_supplement_folds_answers_only(tmp_path: Path) -> None:
    """Architect + answered SUPPLEMENT.md: ANSWERS fold in; QUESTIONS + divider do not."""
    bundle, script = _make_bundle(tmp_path, mode="architect")  # default answers present

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[warn]" not in result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "Strategic brief." in paste            # the ANSWERS region folded in
    assert _ANSWERS_MARKER not in paste           # the divider is stripped, never folded
    assert _QUESTIONS_MARKER not in paste          # the questions are for the outgoing browser


# ------------------------------------------------------------------ #
# Test 8: Execution mode keeps the silent [skip] (no architect framing)
# ------------------------------------------------------------------ #

def test_execution_mode_missing_supplement_stays_skip(tmp_path: Path) -> None:
    """Execution mode keeps the silent [skip] — no architect-specific note, no [warn]."""
    bundle, script = _make_bundle(tmp_path, with_supplement=False, mode="execution")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[skip]" in result.stderr
    assert "[warn]" not in result.stderr


# ------------------------------------------------------------------ #
# Test 9: Empty ANSWERS — not folded, no-answers note printed (v5.2 core change)
# ------------------------------------------------------------------ #

def test_empty_answers_not_folded_and_note_printed(tmp_path: Path) -> None:
    """A generated-but-unfilled SUPPLEMENT.md (cold handoff): present, ANSWERS empty.

    Its QUESTIONS must NOT fold into the paste (they are for the outgoing browser); the
    assembler prints the defined cold-handoff note instead of folding. This is the core
    fold-if-answered behaviour change — RED against the pre-v5.2 whole-file fold.
    """
    bundle, script = _make_bundle(
        tmp_path, mode="architect", supplement_answers=""
    )

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "ANSWERS empty" in result.stderr  # the defined cold-handoff note

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "SUPPLEMENT.md" not in _labels(paste)   # nothing folded
    assert _QUESTIONS_MARKER not in paste           # questions never leak into the paste
    assert _ANSWERS_MARKER not in paste


# ------------------------------------------------------------------ #
# Test 10: Non-empty ANSWERS fold in, questions/divider excluded (v5.2 core change)
# ------------------------------------------------------------------ #

def test_nonempty_answers_fold_into_paste(tmp_path: Path) -> None:
    """Filled SUPPLEMENT.md: the pasted answers reach the next session's PASTE_THIS."""
    bundle, script = _make_bundle(
        tmp_path, mode="architect", supplement_answers="The why: chose X over Y because Z."
    )

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "ANSWERS empty" not in result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "SUPPLEMENT.md" in _labels(paste)
    assert "The why: chose X over Y because Z." in paste
    assert _ANSWERS_MARKER not in paste
    assert _QUESTIONS_MARKER not in paste


# ------------------------------------------------------------------ #
# Test 11: Robustness — comment-only / whitespace ANSWERS counts as empty
# ------------------------------------------------------------------ #

def test_comment_only_answers_counts_as_empty(tmp_path: Path) -> None:
    """ANSWERS containing only an HTML comment + whitespace is treated as unfilled."""
    bundle, script = _make_bundle(
        tmp_path, mode="architect", supplement_answers="<!-- nothing yet -->   \n  \t",
    )

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "ANSWERS empty" in result.stderr
    assert "SUPPLEMENT.md" not in _labels((bundle / "PASTE_THIS.md").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ #
# Test 12: The canonical template carries the 6 questions + the divider
# ------------------------------------------------------------------ #

def test_template_carries_questions_and_marker() -> None:
    """templates/handoff/v5/SUPPLEMENT.md.tmpl is the portable source of the schema."""
    text = TEMPLATE.read_text(encoding="utf-8")

    assert "PASTE CHAT ANSWERS BELOW THIS LINE" in text       # the fold divider
    assert "{{SLUG}}" in text                                  # kept generic/portable
    # the 6 *why*-only questions (substrings inside the bold markers, no marker-crossing)
    for q in (
        "Strategic intent",
        "Tensions weighed",
        "Considered + rejected",
        "Open questions",
        "Decomposition rationale",
        "Off-repo context",
    ):
        assert q in text, f"template missing question: {q}"


# ------------------------------------------------------------------ #
# Test 13: Paste byte-size is surfaced; a normal bundle does not warn (RF-2 item 2)
# ------------------------------------------------------------------ #

def test_normal_bundle_surfaces_size_without_warn(tmp_path: Path) -> None:
    """The assembled byte-size is printed (so paste growth is visible) but a normal-sized
    bundle stays under the threshold — no false [warn]."""
    bundle, script = _make_bundle(tmp_path, mode="architect")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "bytes)" in result.stdout          # size surfaced on the Written line
    assert "[warn]" not in result.stderr        # a small bundle must not trip the bloat warn


# ------------------------------------------------------------------ #
# Test 14: An oversized paste trips a non-gating [warn] (RF-2: arrest paste growth)
# ------------------------------------------------------------------ #

def test_oversized_paste_emits_size_warn(tmp_path: Path) -> None:
    """A paste past _SIZE_WARN_BYTES trips a [warn] — but assembly still succeeds (a WARN,
    not a gate), so an over-budget bundle surfaces the bloat without blocking regeneration."""
    bundle, script = _make_bundle(tmp_path, mode="architect")
    (bundle / "RESIDUAL.md").write_text("# R\n\n" + ("padding " * 12000), encoding="utf-8")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr   # WARN, never a gate
    assert "[warn]" in result.stderr
    assert "heavy boot" in result.stderr


# ------------------------------------------------------------------ #
# Test 15: END sentinel (intake #18 A1) — terminal, correct count + bytes
# ------------------------------------------------------------------ #

def test_end_sentinel_terminal_with_count_and_bytes(tmp_path: Path) -> None:
    """PASTE_THIS.md ends with `=== END OF PASTE — {n} sections · {b} bytes ===` where n is
    the folded-section count and b measures the body BEFORE the sentinel (deterministic,
    never self-referential). A paste not ending in this line is visibly truncated (BW-a)."""
    import re as _re

    bundle, script = _make_bundle(tmp_path)
    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    last_line = paste.rstrip("\n").splitlines()[-1]
    m = _re.fullmatch(r"=== END OF PASTE — (\d+) sections · (\d+) bytes ===", last_line)
    assert m, f"terminal line is not the END sentinel: {last_line!r}"
    assert int(m.group(1)) == len(_labels(paste)), "sentinel count != folded sections"
    body_before = paste.rstrip("\n").rsplit("\n\n---\n\n", 1)[0]
    assert int(m.group(2)) == len(body_before.encode("utf-8")), "sentinel bytes drifted"


# ------------------------------------------------------------------ #
# Test 16: END sentinel excluded from the section count it reports
# ------------------------------------------------------------------ #

def test_end_sentinel_not_a_section(tmp_path: Path) -> None:
    """The sentinel reports 4 sections on a supplement-less bundle — it never counts itself."""
    bundle, script = _make_bundle(tmp_path, with_supplement=False)
    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "=== END OF PASTE — 4 sections" in paste


# ------------------------------------------------------------------ #
# Test 17: PROMOTION DEBT block (intake #18 A8) — advisory, verbatim lines
# ------------------------------------------------------------------ #

def test_promotion_debt_block_on_ruling_bearing_answers(tmp_path: Path) -> None:
    """A folded ANSWERS region carrying ruling markers prints the [promotion-debt] block
    (matched lines verbatim + the ladder prompt) and NEVER blocks the fold."""
    answers = (
        "General context line.\n"
        "BINDING: letters are assigned at integration.\n"
        "Do not relitigate the v6 label.\n"
    )
    bundle, script = _make_bundle(tmp_path, mode="architect", supplement_answers=answers)
    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr           # advisory, never a gate
    assert "[promotion-debt] 2 ruling-bearing line(s)" in result.stderr
    assert "BINDING: letters are assigned at integration." in result.stderr
    assert "Do not relitigate the v6 label." in result.stderr
    assert "durable home: ADR / PLAYBOOK / ESSENTIALS one-liner / carrier?" in result.stderr


# ------------------------------------------------------------------ #
# Test 18: No PROMOTION DEBT block on marker-free answers
# ------------------------------------------------------------------ #

def test_no_promotion_debt_block_without_markers(tmp_path: Path) -> None:
    """Marker-free ANSWERS fold silently — no [promotion-debt] noise on a normal handoff."""
    bundle, script = _make_bundle(
        tmp_path, mode="architect", supplement_answers="Plain strategic context only."
    )
    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[promotion-debt]" not in result.stderr
