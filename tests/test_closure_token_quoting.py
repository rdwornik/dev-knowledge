"""[#437] closure-token quoting semantics — the shared detection core.

A closes-directive counts ONLY as a directive: occurrences inside backtick code
spans, fenced blocks, block-quote lines, or same-line (double-)quotation contexts
never match; genuine plain-text `closes [#N]` directives match exactly as before.

TDD fixtures per the design note (docs/audits/2026-07-28-technical-437-closure-
token-design.md + its same-day amendment): the two live reproductions on record
(`12e6b45b`, `d993922e` — both verbatim-excerpted AND re-read from git), the
reconstructed `096364ac` pre-amend quoting form, the seeded quoted tag from
[#437]'s Done-when, and the true-positive forms actually present in history.

Documented residuals (asserted here so scope changes are loud): multi-line paired
quotes and multi-line inline code spans stay DETECTED — pairing across lines could
blank real text and hide a REAL directive, the worse failure direction for a
drift detector.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_P = _REPO / "scripts" / "propose_closures.py"


def _load():
    spec = importlib.util.spec_from_file_location("propose_closures_qt", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pc = _load()


def ids(text):
    return pc.closure_ids(text)


# --- live reproduction 1: 12e6b45b (verbatim excerpt, [#437] row n=1) ----------

_12E6B45B_EXCERPT = (
    "NOT touched: the three commit-message [#370] citations (40c7bce3, b0443523,\n"
    "36ca03f0) — operator-ruled acceptable as stale rather than rewriting history.\n"
    "Verified inert: no commit carries a `closes [#370]` tag, so the stale references\n"
    "have no closure semantics and cannot trip git_backlog_drift against the\n"
    "surviving ownership ticket.\n"
)


def test_live_fixture_12e6b45b_backtick_denial_is_not_a_closure():
    assert ids(_12E6B45B_EXCERPT) == []


# --- live reproduction 2: d993922e ([#437]'s own filing commit, self-match) ----

_D993922E_EXCERPT = (
    "  [#437] CLOSES_RE quoting defect - propose_closures.py:51/:80 scans raw commit\n"
    "  text, so backtick-quoted `closes [#N]` convention-prose reads as a real\n"
    "  closure. Verified live, not asserted: 12e6b45b's body says \"no commit carries\n"
    "  a `closes [#370]` tag\" and that sentence alone makes [#370] the STRONG\n"
    "  proposal in every window sampled - today's logs/PROPOSALS-2026-07-28.md cites\n"
    "  12e6b45b7 as its evidence.\n"
)


def test_live_fixture_d993922e_filing_commit_does_not_self_match():
    assert ids(_D993922E_EXCERPT) == []


# --- live reproduction 3: 096364ac pre-amend form ([#437] row n=2) -------------
# The draft quoted the removed README index-row clause verbatim in quotation marks.

_096364AC_PRE_AMEND = (
    "Also corrects a false clause in the ADR-107 index row, which asserted\n"
    'that the ADR "Closes [#433] on ruling" - ADR-107 section 7.5 says the opposite.\n'
)


def test_live_fixture_096364ac_pre_amend_quoted_clause_is_not_a_closure():
    assert ids(_096364AC_PRE_AMEND) == []


# --- the two live reproductions re-read from git (full real messages) ----------

def _git_message(sha):
    r = subprocess.run(
        ["git", "-C", str(_REPO), "show", "--format=%B", "--no-patch", sha],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0 or not r.stdout.strip():
        pytest.skip(f"commit {sha} not reachable (shallow clone / detached fixture)")
    return r.stdout


@pytest.mark.parametrize("sha", ["12e6b45b", "d993922e"])
def test_live_history_reproductions_yield_no_closure(sha):
    assert ids(_git_message(sha)) == []


def test_live_history_amended_096364ac_stays_clean():
    # the committed (amended) message never matched; it must stay clean post-fix
    assert ids(_git_message("096364ac")) == []


# --- seeded quoted forms (the [#437] Done-when "seeded quoted tag") ------------

def test_inline_code_span_never_matches():
    assert ids("docs: explain the `closes [#99]` convention") == []


def test_fenced_block_never_matches():
    assert ids("body\n```\nfeat: x, closes [#12]\n```\ntail") == []


def test_block_quote_line_never_matches():
    assert ids("> the merge said closes [#13] but was reverted") == []


def test_block_quote_with_leading_spaces_never_matches():
    assert ids("  > closes [#17] per the old ruling") == []


def test_same_line_double_quoted_span_never_matches():
    assert ids('the row said "closes [#15] on ruling" which was false') == []


def test_same_line_curly_quoted_span_never_matches():
    assert ids("the row said “closes [#14] on ruling” which was false") == []


# --- true positives: forms actually present in history (no regression) ---------

@pytest.mark.parametrize("msg,expected", [
    ("chore(backlog): closes [#434] — conformance-branch extraction pass", ["434"]),
    ("docs(backlog): close [#386] — the delivery loop is codified", ["386"]),
    ("Merge docs/lane-d-rulings — closes [#262], closes [#295]", ["262", "295"]),
    ("Merge docs/vision-reread — closes [#368]; terra clean @ 5767232a", ["368"]),
    ("Closes [#5]", ["5"]),
    ("fix: fixes [#7]", ["7"]),
    ("fix: fixed [#8]", ["8"]),
    ("chore: closed [#9]", ["9"]),
])
def test_real_directive_forms_still_match(msg, expected):
    assert ids(msg) == expected


def test_mixed_quoted_and_real_directive_keeps_only_the_real_one():
    assert ids("fix `quoted closes [#5]` handling, closes [#6]") == ["6"]


def test_unpaired_backtick_cannot_hide_a_real_directive():
    assert ids("fix `dangling span, closes [#7]") == ["7"]


def test_unpaired_double_quote_cannot_hide_a_real_directive():
    assert ids('he said "unfinished, closes [#15]') == ["15"]


def test_crlf_real_directive_matches():
    assert ids("done\r\ncloses [#10]\r\n") == ["10"]


def test_crlf_backticked_token_does_not_match():
    assert ids("note the `closes [#10]` form\r\ncloses [#11]\r\n") == ["11"]


def test_directive_in_body_after_quoted_subject_form():
    assert ids('docs: fix "closes [#5]" handling\n\ncloses [#6]\n') == ["6"]


# --- documented residuals (same-line principle — asserted so scope is loud) ----

def test_residual_multi_line_paired_quotes_stay_detected():
    # OUT of scope by design (amendment M1): cross-line quote pairing could hide
    # a real directive between unrelated quote characters.
    assert ids('she wrote "first line\ncloses [#16] second" done') == ["16"]


def test_residual_multi_line_inline_span_stays_detected():
    # inline spans are same-line only (amendment M1): an unpaired backtick must
    # never blank across lines.
    assert ids("`start of span\ncloses [#11] more` tail") == ["11"]


# --- detection-core integration (find_strong / find_weak use the shared core) --

def test_find_strong_ignores_quoted_only_commit():
    c = pc.Commit("a" * 9, "docs: about the `closes [#5]` convention")
    assert pc.find_strong({"5"}, [c]) == {}


def test_find_strong_still_fires_on_real_directive():
    c = pc.Commit("a" * 9, "chore: done, closes [#5]")
    assert "5" in pc.find_strong({"5"}, [c])


def test_find_weak_treats_quoted_only_commit_as_plain():
    # a commit whose ONLY closes-token is quoted is not a closure declaration,
    # so it stays eligible as WEAK file-touch evidence
    c = pc.Commit("a" * 9, "docs: about `closes [#5]`", files=["scripts/x.py"])
    weak = pc.find_weak({"7": "touches scripts/x.py"}, [c], strong_ids=set())
    assert "7" in weak
