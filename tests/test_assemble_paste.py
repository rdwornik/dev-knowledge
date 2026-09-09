"""Tests for scripts/assemble_paste.py."""
from __future__ import annotations

import os
import re
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
    bundle_rel: str = "bundle",
    residual: str = "# Residual\n\nDrift flags.",
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
    # v6.3.0: the ROLE PIN names the LIVE spec version, so the spec must exist. The
    # assembler exits 1 without it, deliberately -- a pin whose version is unknown is
    # worse than no pin, because it asserts an identity it cannot vouch for.
    (protocols / "HANDOFF_PROCESS.md").write_text(
        "# HANDOFF_PROCESS v6\n\nVersion: 6.3.0\nStatus: stable\n", encoding="utf-8")

    # fake bundle. `bundle_rel` defaults to a bare `bundle/`, which is deliberately NOT under
    # `docs/handoffs/` — the [#643] leg-2 carriage gate is scoped to a real bundle home, so the
    # default keeps every test above it ungated. Pass `docs/handoffs/<slug>` to exercise it.
    bundle = tmp_path / bundle_rel
    bundle.mkdir(parents=True)

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

    (bundle / "RESIDUAL.md").write_text(residual, encoding="utf-8")
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
    # ...and gen_handoff itself now reads the canonical-doc-name registry (CLOUD-4 v2, R2
    # §1.5 GO-b), so the sibling set is two deep. Copied rather than papered over with a
    # fallback import in gen_handoff: that module is precisely the site R2 §1.4 R2 prices as
    # the silent-failure one — a miss stamps a placeholder into a bundle that is immutable on
    # commit — so its filename and degrade string are deliberately allowed exactly one home.
    shutil.copy(SCRIPT.parent / "canonical_docs.py", scripts_dir / "canonical_docs.py")

    return bundle, script_copy


def _run(script: Path, bundle: Path,
         transport: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = None
    if transport is not None:
        env = {**os.environ, "CLAUDE_PROMPTS_DIR": str(transport)}
    return subprocess.run(
        [sys.executable, str(script), str(bundle)],
        capture_output=True,
        text=True,
        env=env,
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
        "ROLE PIN (protocols/HANDOFF_BOOT.md — RESIDENT, not inlined)",
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
# v6.3.0 role residency — the ROLE PIN (operator ruling D-R1, census R1)
# ------------------------------------------------------------------ #

def test_role_pin_is_three_lines_with_version_sha_and_refusal(tmp_path: Path) -> None:
    """The pin is identity + integrity + REFUSAL. All three, or it is not a pin."""
    import hashlib
    bundle, script = _make_bundle(tmp_path)
    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    role = tmp_path / "protocols" / "HANDOFF_BOOT.md"
    digest = hashlib.sha256(role.read_bytes()).hexdigest()

    pin = [ln for ln in paste.splitlines() if ln.startswith("ROLE PIN")]
    assert len(pin) == 1
    assert pin[0] == "ROLE PIN — HANDOFF_BOOT.md @ handoff-process v6.3.0"
    assert f"sha256: {digest}" in paste
    assert "say so before answering" in paste, (
        "the refusal line is the pin's teeth; without it residency drifts SILENTLY"
    )


def test_pin_sha_tracks_the_role_file(tmp_path: Path) -> None:
    """Change the role file, and the pin must change with it — else it vouches for nothing."""
    import hashlib
    bundle, script = _make_bundle(tmp_path)
    _run(script, bundle)
    first = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    role = tmp_path / "protocols" / "HANDOFF_BOOT.md"
    role.write_text("# Boot" + chr(10) + chr(10) + "Role content, EDITED.", encoding="utf-8")
    _run(script, bundle)
    second = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    assert hashlib.sha256(role.read_bytes()).hexdigest() in second
    assert [ln for ln in first.splitlines() if ln.startswith("sha256:")] !=            [ln for ln in second.splitlines() if ln.startswith("sha256:")]


def test_paste_shrinks_by_the_role_file_minus_the_pin(tmp_path: Path) -> None:
    """The saving is real and bounded: role bytes out, a few hundred pin bytes in."""
    bundle, script = _make_bundle(tmp_path)
    _run(script, bundle)
    paste = (bundle / "PASTE_THIS.md").read_bytes()
    role = (tmp_path / "protocols" / "HANDOFF_BOOT.md").read_bytes()
    assert role not in paste, "the role body must not be present in any form"
    assert b"ROLE PIN" in paste


def test_missing_spec_refuses_rather_than_pinning_an_unknown_version(tmp_path: Path) -> None:
    """A pin whose version cannot be read asserts an identity it cannot vouch for."""
    bundle, script = _make_bundle(tmp_path)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").unlink()
    result = _run(script, bundle)
    assert result.returncode == 1
    assert "Version" in result.stderr


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
    # v6.3.0 INVERTS this assertion, deliberately and on the record. Through v6.2.0 the
    # role file body had to be INLINED (the original defect was a bundle that merely
    # POINTED at it, giving the file-less browser a partial boot). Since the residency
    # flip the role is held by the browser project itself, so its body must be ABSENT and
    # the PIN present. The old concern is not abandoned -- it is now served by the pin's
    # refusal line, which makes a missing-or-drifted resident role loud instead of silent.
    assert "Role content." not in paste, (
        "role file body inlined -- v6.3.0 ships a PIN, not the role text"
    )
    assert "ROLE PIN — HANDOFF_BOOT.md @ handoff-process v6.3.0" in paste
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
    """The assembled byte-size AND the window-specific ratio are printed on the same Written
    line (so paste growth and the ratio are never two separate numbers to go compute) — a
    normal-sized bundle stays under the threshold — no false [warn]."""
    bundle, script = _make_bundle(tmp_path, mode="architect")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert " bytes; window-specific " in result.stdout   # size + ratio, same Written line
    assert re.fullmatch(r"\d+/\d+ B = \d+%",
                        result.stdout.split("window-specific ")[1].split(")")[0])
    assert "[warn]" not in result.stderr        # a small bundle must not trip the bloat warn


# ------------------------------------------------------------------ #
# Test 14: An oversized paste trips a non-gating [warn] (RF-2: arrest paste growth)
# ------------------------------------------------------------------ #

def test_oversized_paste_emits_size_warn(tmp_path: Path) -> None:
    """A paste past PASTE_BYTE_CEILING trips a [warn] — but assembly still succeeds (a WARN,
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


# ------------------------------------------------------------------ #
# Test 19: --pin-only (v7 /boot-session use, HANDOFF_PROCESS.md §17.4) —
# the same pin mechanism §4 uses, reused rather than re-implemented.
# ------------------------------------------------------------------ #

def test_pin_only_prints_just_the_three_line_pin(tmp_path: Path) -> None:
    _bundle, script = _make_bundle(tmp_path)
    result = subprocess.run(
        [sys.executable, str(script), "--pin-only"], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip("\n").splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("ROLE PIN — HANDOFF_BOOT.md @ handoff-process v6.3.0")
    assert lines[1].startswith("sha256: ")
    assert "If your project instructions do not carry this contract" in lines[2]


def test_pin_only_needs_no_bundle_dir(tmp_path: Path) -> None:
    """--pin-only never touches RESIDUAL.md/PROBES.md/SUPPLEMENT.md — no BUNDLE_DIR needed."""
    _bundle, script = _make_bundle(tmp_path)
    result = subprocess.run(
        [sys.executable, str(script), "--pin-only"],
        capture_output=True, text=True, cwd=str(tmp_path),
    )
    assert result.returncode == 0, result.stderr


def test_missing_bundle_dir_without_pin_only_is_a_usage_error(tmp_path: Path) -> None:
    _bundle, script = _make_bundle(tmp_path)
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "BUNDLE_DIR is required unless --pin-only is given" in result.stderr


def test_pin_only_missing_spec_still_refuses_cleanly(tmp_path: Path) -> None:
    _bundle, script = _make_bundle(tmp_path)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").unlink()
    result = subprocess.run(
        [sys.executable, str(script), "--pin-only"], capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "the ROLE PIN needs its Version line" in result.stderr


# ------------------------------------------------------------------ #
# [#611] window-specific ratio -- derivation:
# docs/audits/2026-09-02-technical-lane-g-611-bundle-thinning.md §1.2
# ------------------------------------------------------------------ #

def test_window_specific_ratio_counts_fill_in_bodies_and_folded_answers(tmp_path: Path) -> None:
    """The printed ratio counts FILL-IN region BODIES (never the marker comments) plus the
    folded SUPPLEMENT ANSWERS, over content_bytes -- and PROBES.md (no FILL-IN regions)
    contributes 0, exactly the census's own finding that PROBES.md is 96% invariant."""
    bundle, script = _make_bundle(tmp_path, mode="architect", supplement_answers="Real answer text.")
    driftflags_body = "Shipped the thing because of the reason."
    (bundle / "RESIDUAL.md").write_text(
        "# Residual\n\n"
        "<!-- FILL-IN:driftflags START (hand-authored) -->"
        f"{driftflags_body}"
        "<!-- FILL-IN:driftflags END -->\n",
        encoding="utf-8",
    )
    # PROBES.md carries no FILL-IN region -- 0 window-specific bytes, by construction.
    (bundle / "PROBES.md").write_text("# Probes\n\nP1 probe here, no FILL-IN.", encoding="utf-8")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr

    m = re.search(r"window-specific (\d+)/(\d+) B = (\d+)%", result.stdout)
    assert m, result.stdout
    ws_bytes, content_bytes, pct = int(m.group(1)), int(m.group(2)), int(m.group(3))

    # driftflags body + the folded answers text -- nothing from PROBES.md or the scaffolding.
    expected = len(driftflags_body.encode("utf-8")) + len("Real answer text.".encode("utf-8"))
    assert ws_bytes == expected
    assert pct == round(expected * 100 / content_bytes)


def test_window_specific_ratio_excludes_unfilled_placeholder(tmp_path: Path) -> None:
    """An unfilled FILL-IN region -- the generator's own `_(fill: ...)_` placeholder prompt --
    is generic boilerplate, not window content, and counts 0 rather than inflating the ratio."""
    bundle, script = _make_bundle(tmp_path, mode="architect", with_supplement=False)
    (bundle / "RESIDUAL.md").write_text(
        "# Residual\n\n"
        "<!-- FILL-IN:frontier START (hand-authored) -->"
        "_(fill: the open design questions the next session should resume)_"
        "<!-- FILL-IN:frontier END -->\n",
        encoding="utf-8",
    )

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    m = re.search(r"window-specific (\d+)/(\d+) B = (\d+)%", result.stdout)
    assert m, result.stdout
    assert int(m.group(1)) == 0
    assert int(m.group(3)) == 0


# ------------------------------------------------------------------ #
# [#643] leg 2 — P11 decision carriage, the ASSEMBLE-TIME half
# ------------------------------------------------------------------ #
#
# RED-FIRST (ADR-108 §B): watched to fail against a tree where the assembler read no transport
# file at all. THE TWO LEGS GATE AT DIFFERENT STAGES and that is the design content of the
# row, not an afterthought. Leg 1 (an anchored `carried-by:` whose value resolves on `main`)
# reads only the transport and `main`, so it refuses at PREFLIGHT, before the cut — its tests
# are in tests/test_gen_handoff_preflight.py. Leg 2 is the `OPEN` conjunct: a decision file
# stating the literal `OPEN` discharges P11 only by being NAMED in this bundle's residual, and
# the residual does not exist until the operator fills it. Assembly is the first moment both
# operands exist, so it is the first moment the conjunct is checkable — and a single preflight
# row claiming to cover both would be exactly the false completeness P11 exists to catch.
#
# Family precedent for refusing debt at a handoff, cited in the gate's own message:
# `DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08` / `DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08`.

_OPEN_DECISION = "BATCH-2026-09-07-CLOSE-CONTRACTS.md"


def _transport_with_open_carrier(tmp_path: Path, name: str = _OPEN_DECISION) -> Path:
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc" / name).write_text(
        f"# {name}\ncarried-by: OPEN -- the batch is in flight; no carrier resolves yet\n",
        encoding="utf-8")
    return transport


def test_an_open_carrier_absent_from_the_filled_residual_blocks_assembly(tmp_path: Path) -> None:
    """The defect two consecutive bundles shipped: the `-1` and `-2` residuals named none of
    the five OPEN decision files, and both were discovered only by `/handoff-verify`, AFTER the
    cut was committed and merged. A merged handoff is immutable, so the only repair was a
    superseding cut. Blocking assembly is where that stops."""
    bundle, script = _make_bundle(tmp_path, bundle_rel="docs/handoffs/2026-09-08-x")
    result = _run(script, bundle, transport=_transport_with_open_carrier(tmp_path))
    assert result.returncode == 1, result.stdout
    assert _OPEN_DECISION in result.stderr
    assert not (bundle / "PASTE_THIS.md").exists()


def test_naming_the_open_carrier_in_the_residual_lets_assembly_through(tmp_path: Path) -> None:
    """The negative control. Without it the refusal above proves only that the gate can fire,
    never that a correctly-carried window can still hand off — which is the deadlock the
    2026-09-08 rulings on rows 1 and 7 were both issued to prevent."""
    bundle, script = _make_bundle(
        tmp_path, bundle_rel="docs/handoffs/2026-09-08-y",
        residual=f"# Residual\n\nCarried OPEN: `to-cc/{_OPEN_DECISION}` — owned by [#643].\n")
    result = _run(script, bundle, transport=_transport_with_open_carrier(tmp_path))
    assert result.returncode == 0, result.stderr
    assert (bundle / "PASTE_THIS.md").exists()


def _commit_as_main(repo_root: Path) -> None:
    """Make `repo_root` a git repo whose `main` carries its files, so `git cat-file -e
    main:<path>` can actually resolve.

    WITHOUT THIS the resolving-carrier test below was a FALSE GREEN, and how it failed is the
    point. `_resolves_on_main` asks git; in a plain tmp_path there is no repo, so every
    candidate came back UNRESOLVED -- and the test still passed, because assembly judges only
    the `OPEN` kind and ignores UNRESOLVED and RESOLVES alike. It asserted nothing about the
    state its own name claims and would have stayed green through any regression in resolution
    handling. Terra's sibling finding, 2026-09-09.

    `-c user.*` is passed inline rather than assumed: a fixture must not depend on the
    machine's global git identity, and a commit is what actually puts a `main` ref on disk.
    """
    ident = ["-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-b", "main"], cwd=repo_root, check=True,
                   capture_output=True)
    subprocess.run(["git", *ident, "add", "-A"], cwd=repo_root, check=True, capture_output=True)
    subprocess.run(["git", *ident, "commit", "-m", "fixture"], cwd=repo_root, check=True,
                   capture_output=True)


def test_a_resolving_carrier_is_leg_1s_subject_and_does_not_gate_assembly(tmp_path: Path) -> None:
    """Only the `OPEN` conjunct gates here. A file whose value names a home is leg 1's subject
    and was already judged before the cut; re-judging it at assemble would put one predicate in
    two places, free to disagree.

    TWO ASSERTIONS, and the first is what makes the second mean anything. `carriage_verdicts`
    must actually return `resolves` for this file -- otherwise `returncode == 0` proves only
    that assembly ignores whatever verdict it happened to get, which is precisely how this test
    passed for the wrong reason before. With the first assert in place, a regression in
    resolution handling turns the fixture's carrier UNRESOLVED (or OPEN) and this goes RED.
    """
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-cc" / "DECLARE-CARRIED.md").write_text(
        "# carried\ncarried-by: protocols/HANDOFF_PROCESS.md\n", encoding="utf-8")
    bundle, script = _make_bundle(tmp_path, bundle_rel="docs/handoffs/2026-09-08-z")
    _commit_as_main(tmp_path)

    import gen_handoff as gh

    verdicts = gh.carriage_verdicts(transport, tmp_path)
    assert [v.kind for v in verdicts] == [gh.CARRIAGE_RESOLVES], \
        [f"{v.path.name}: {v.kind} -- {v.detail}" for v in verdicts]

    result = _run(script, bundle, transport=transport)
    assert result.returncode == 0, result.stderr
    assert (bundle / "PASTE_THIS.md").exists()


def test_a_bundle_outside_the_repo_bundle_home_is_not_gated(tmp_path: Path) -> None:
    """THE HONEST LIMIT, stated as a test rather than left to be discovered. The gate binds a
    bundle under `<repo_root>/docs/handoffs/`, which is the only place a real cut lands. An
    ad-hoc directory assembled elsewhere is not a window's handoff and has no residual duty."""
    bundle, script = _make_bundle(tmp_path)          # tmp_path/bundle — the default
    result = _run(script, bundle, transport=_transport_with_open_carrier(tmp_path))
    assert result.returncode == 0, result.stderr
    assert _OPEN_DECISION not in result.stderr
