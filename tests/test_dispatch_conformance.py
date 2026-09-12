"""AX25-2 — the generator<->verb conformance test, RED-first (`[#675]` clause 1).

THE CLAUSE, verbatim from `to-cc/AMEND-BATCH-X-ROSTER-025.md` as the lane contract transcribes
it:

    **AX25-2 · The mechanism — a generator<->verb conformance test, RED-first, in the hub**
    (rides `[#675]`'s lane as clause 1, no separate lane): the test generates a contract with
    `gen_lane_contract.py` and runs the ruled verb's DryRun against it, asserting it resolves —
    fence, contract location, model, and base all in one assertion. It fails today (the three
    wave-2 contracts are refused on grammar) and must go green before any later dispatch change
    lands. A commit that changes either side and leaves the test red is refused.

FOUR PROPERTIES, **ONE ASSERTION** — and that is the clause, not a style note. `[#716]` (base),
`[#717]` (model), `[#718]` (location) and `[#740]` (fence) are four symptoms of ONE seam, and
they accumulated while every individual check passed. Four separate test functions can each be
made green against a different half of the seam; a single comparison of the whole
property-record cannot. So `test_the_generators_line_is_a_line_the_ruled_verb_resolves` carries
exactly one `assert`, over all four, and the rest of this module tests the PROBE rather than the
seam.

WHY THIS IS RED TODAY, proven rather than assumed. The writer emits
`Dispatch-Lane <slug> <file> -Effort <e> -Model <m>`; the reader's `Assert-ClaudeCommand` admits
only a `claude` head token. Measured 2026-09-12 against a freshly generated contract:

    Refusing: the contract's ## Dispatch block must invoke 'claude', not 'Dispatch-Lane' --
    this script never runs an arbitrary command from a contract file.
    (Invoke-Dispatch.ps1:285)

and the same refusal is on the record for all three frozen X2 contracts in
`docs/audits/2026-09-12-technical-batch-x2-manifest.md` §4.

NO SKIP TIER. `dispatch_conformance` computes all four properties on every host — the verb's own
DryRun where it resolves, a pinned admission rule where it does not — so this module is RED on
`ubuntu-latest` for the same reason it is RED on the operator's Windows box. The one test that
genuinely cannot run off-host is the PIN-MAINTENANCE leg, which is a different subject (does the
reader still refuse what the pin says it refuses?) and is marked as such.
"""
from __future__ import annotations

import textwrap

import pytest

import dispatch_conformance as dc


# --- THE CLAUSE -------------------------------------------------------------

def test_the_generators_line_is_a_line_the_ruled_verb_resolves(tmp_path):
    """AX25-2: fence, contract location, model and base — all four, in ONE assertion.

    Do not split this into four. The whole point of the clause is that four independently
    green checks are what let four symptoms co-exist with a green suite.
    """
    result = dc.probe(tmp_path, slug="lane-probe-conformance", model="sonnet", effort="high")

    assert result.properties() == dc.CONFORMANT, "\n" + result.report()


@pytest.mark.slow
def test_the_pinned_admission_rule_still_matches_the_live_reader(tmp_path):
    """PIN MAINTENANCE — a different subject from the clause above, so a different leg.

    The lower tiers judge `fence` against `dispatch_conformance.ADMISSION_HEAD_TOKEN`, a value
    measured off a real refusal on a dated host. This asserts the reader has not moved since.
    It is host-only by nature: where the reader is absent there is nothing to re-measure, and
    that is a true unavailability rather than a skipped assertion — the clause's own test above
    still runs and still fails there.
    """
    if dc.host_tier() != dc.TIER_HOST:
        pytest.skip(f"tier {dc.host_tier()}: the ruled verb {dc.RULED_VERB!r} is not on this "
                    f"host, so its admission rule cannot be re-measured. The CONFORMANCE test "
                    f"above is unaffected and still runs.")
    assert dc.verify_admission_live(tmp_path) == []


# --- the probe's own machinery ----------------------------------------------

@pytest.mark.parametrize("head,expected", [
    ("claude --bg --worktree x", "claude"),
    ("claude.cmd --bg", "claude"),
    (r'"C:\Program Files\claude.exe" --bg', "claude"),
    ("Dispatch-Lane slug FILE.md -Effort high", "dispatch-lane"),
    ("", ""),
])
def test_head_token_normalises_the_way_the_reader_normalises(head, expected):
    """`Assert-ClaudeCommand` compares `GetFileNameWithoutExtension(...).ToLowerInvariant()`.
    A probe comparing raw strings would call a legitimate absolute-path invocation
    non-conforming, which is a false RED on the exact property under test."""
    assert dc.head_token(head) == expected


def test_fence_line_joins_a_wrapped_block_the_way_the_reader_joins_it():
    """`Get-DispatchBlockLine` joins every non-blank line of the block with a space. A probe
    that read only the first line would call a wrapped-but-valid block non-conforming."""
    text = textwrap.dedent("""\
        # LANE x

        ## Dispatch

        **Shape:** `local`

        ```
        claude --bg --model sonnet
          --worktree lane-x
        ```

        ## Worktree pairing
        """)
    assert dc.fence_line(text) == "claude --bg --model sonnet --worktree lane-x"


def test_fence_line_is_empty_when_there_is_no_dispatch_block():
    """An absent block is reported as absent, never as an empty-but-fine one: `head_token('')`
    is `''`, which fails the admission comparison, which is the honest answer."""
    assert dc.fence_line("# LANE x\n\n## Steps\n\n1. do a thing\n") == ""


def _probe_from(fence: str, *, evidence="pin", tmp_path=None, **kw) -> dc.Probe:
    """A Probe built from a literal fence line — the fire-test substrate. Nothing spawns a
    PowerShell here, so these run on every host including the ones with no shell at all."""
    return dc.Probe(
        tier=kw.pop("tier", dc.TIER_NO_SHELL), evidence=evidence,
        slug=kw.pop("slug", "lane-x"), model=kw.pop("model", "sonnet"),
        effort=kw.pop("effort", "high"),
        contract_name=kw.pop("contract_name", "LANE-lane-x.md"),
        contract_dir=str(tmp_path) if tmp_path else ".",
        fence=fence, line=kw.pop("line", fence), **kw)


def test_the_probe_REDs_on_the_live_defect_a_Dispatch_Lane_head_token(tmp_path):
    """THE FIRE-TEST. A guard whose firing is conditional on the environment it polices proves
    nothing on the machine that breaks it, so the live defect is planted here directly."""
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    result = _probe_from(
        "Dispatch-Lane lane-x LANE-lane-x.md -Effort high -Model sonnet", tmp_path=tmp_path)
    props = result.properties()

    assert props["fence"] is False
    # The other three are independently readable off the same line, which is what makes the
    # single assertion a conjunction of four real properties rather than one property in a
    # trench coat: this line carries neither `--model` nor `--worktree` in the reader's grammar.
    assert props["model"] is False and props["base"] is False
    assert props["location"] is True, "the writer did name the file it wrote"


def test_a_conforming_claude_line_greens_all_four(tmp_path):
    """The positive control. Without it a probe that returned False unconditionally would pass
    the fire-test above and measure nothing."""
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    result = _probe_from(
        "claude --bg --model sonnet --effort high --permission-mode bypassPermissions "
        "--worktree lane-x \"Read and execute the frozen contract at "
        "$env:CLAUDE_PROMPTS_DIR\\LANE-lane-x.md\"", tmp_path=tmp_path)

    assert result.properties() == dc.CONFORMANT, "\n" + result.report()
    assert result.conforms


def test_a_derived_source_does_not_read_as_a_conforming_fence(tmp_path):
    """`source: derived (fallback ...)` means the reader IGNORED the fenced block and rebuilt a
    line from the Model/Effort table. The resulting line can carry a correct model and worktree
    while the fence itself is unusable — a fallback mechanism passing itself off as conformance,
    and the exact shape of "green while the seam is open"."""
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    conforming_line = ("claude --bg --model sonnet --effort high --worktree lane-x")
    derived = _probe_from("Dispatch-Lane lane-x LANE-lane-x.md", evidence="verb",
                          tier=dc.TIER_HOST, tmp_path=tmp_path, line=conforming_line,
                          source="derived (fallback -- Model/Effort table + filename)")

    assert derived.properties()["fence"] is False, "\n" + derived.report()


def test_an_admission_refusal_is_named_in_the_report(tmp_path):
    """The report has to say WHY, or a red test sends its reader to the wrong owner."""
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    refused = _probe_from("Dispatch-Lane lane-x LANE-lane-x.md", evidence="verb",
                          tier=dc.TIER_HOST, tmp_path=tmp_path, line="",
                          refusal="Refusing: the contract's ## Dispatch block must invoke "
                                  "'claude', not 'Dispatch-Lane' -- this script never runs an "
                                  "arbitrary command from a contract file.",
                          returncode=1)
    report = refused.report()

    assert "ADMISSION refusal" in report and "[#740]" in report
    assert "fence=RED" in report


def test_a_placeholder_that_survives_into_the_resolved_line_REDs_location(tmp_path):
    """THE NEAR-MISS THAT ACTUALLY HAPPENED, pinned (`[#718]` leg 2).

    On 2026-09-12 this probe went GREEN against a generator emitting the INTERACTIVE shape's
    `<PROMPTS_DIR>` prose placeholder into the machine-read local line. The reader substitutes
    exactly one literal, so that placeholder rode through untouched: the verb resolved, the dry
    run printed a plausible line, and the lane it launched would have been handed a prompt
    naming a path no filesystem holds. Everything about that failure looks like success.
    """
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    stranded = _probe_from(
        "claude --bg --model sonnet --effort high --permission-mode bypassPermissions "
        "--worktree lane-x \"Read and execute the frozen contract at "
        "<PROMPTS_DIR>\\LANE-lane-x.md\"",
        evidence="verb", tier=dc.TIER_HOST, tmp_path=tmp_path, returncode=0, source="contract")
    props = stranded.properties()

    assert props["location"] is False, "\n" + stranded.report()
    # The other three are untouched: the head token, the model and the worktree are all
    # correct on this line. That is precisely what made the defect invisible.
    assert props["fence"] and props["model"] and props["base"]
    assert "stranded: <PROMPTS_DIR>" in stranded.report()


def test_the_probe_never_returns_a_skipped_verdict(tmp_path):
    """NO GREEN-BY-SKIP, asserted rather than intended. Whatever tier this host is on, the probe
    returns all four properties and names the evidence it used."""
    result = dc.probe(tmp_path, tier=dc.TIER_NO_SHELL)

    assert set(result.properties()) == set(dc.PROPERTIES)
    assert result.evidence in ("verb", "pin")
    assert result.tier in (dc.TIER_HOST, dc.TIER_NO_VERB, dc.TIER_NO_SHELL)
    assert dc.ADMISSION_MEASURED in result.report(), \
        "a lower-tier verdict must carry the pin's provenance, or its reader cannot weigh it"


# --- the refusal leg --------------------------------------------------------

def test_the_guard_probes_NOTHING_when_no_seam_file_is_staged(monkeypatch, tmp_path):
    """Cheap on an unrelated commit, and provably so: the probe spawns a PowerShell and
    renders a contract, and a gate that pays that on every commit is a gate people bypass."""
    monkeypatch.setattr(dc, "staged_from_git", lambda *_a, **_k: ["README.md", "JOURNAL.md"])
    monkeypatch.setattr(dc, "probe", _never_called)

    code, message = dc.guard(tmp_path)

    assert code == 0
    assert "no seam file staged" in message


@pytest.mark.parametrize("seam_file", dc.SEAM_PATHS)
def test_the_guard_REFUSES_a_seam_commit_that_leaves_the_seam_red(monkeypatch, tmp_path,
                                                                 seam_file):
    """AX25-2's refusal leg, per seam file: *"a commit that changes either side and leaves
    the test red is refused."*

    Parametrized over `SEAM_PATHS` rather than pinned to one, because a gate that watches the
    generator and not its own probe can be disarmed by editing the probe -- the self-disarm
    class `impacted-tests-guard` was corrected for on 2026-09-11.
    """
    monkeypatch.setattr(dc, "staged_from_git", lambda *_a, **_k: [seam_file, "README.md"])
    monkeypatch.setattr(dc, "probe", lambda *_a, **_k: _probe_from(
        "Dispatch-Lane lane-x LANE-lane-x.md -Effort high -Model sonnet", tmp_path=tmp_path))

    code, message = dc.guard(tmp_path)

    assert code == 1, message
    assert "REFUSED" in message and seam_file in message
    assert "fence" in message


def test_the_guard_PASSES_a_seam_commit_that_conforms(monkeypatch, tmp_path):
    """The positive control. A guard that refused unconditionally would pass the test above
    and block every commit, which is indistinguishable from working until someone commits."""
    (tmp_path / "LANE-lane-x.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(dc, "staged_from_git",
                        lambda *_a, **_k: ["scripts/gen_lane_contract.py"])
    monkeypatch.setattr(dc, "probe", lambda *_a, **_k: _probe_from(
        "claude --bg --model sonnet --effort high --permission-mode bypassPermissions "
        "--worktree lane-x \"Read and execute the frozen contract at "
        "$env:CLAUDE_PROMPTS_DIR\\LANE-lane-x.md\"", tmp_path=tmp_path))

    code, message = dc.guard(tmp_path)

    assert code == 0, message
    assert "PASS" in message


def test_a_probe_that_cannot_be_TAKEN_refuses_rather_than_passing(monkeypatch, tmp_path):
    """An unmeasurable seam change is not a seam change that passed.

    The distinction this protects is the one `dispatch_drift` states next door: a check that
    cannot compute its ground truth and renders green IS the defect. Here the render itself
    failed, so there is no record at all -- and no record must not read as a clean one.
    """
    monkeypatch.setattr(dc, "staged_from_git",
                        lambda *_a, **_k: ["scripts/gen_lane_contract.py"])

    def _explode(*_a, **_k):
        raise dc.DispatchConformanceError("the writer would not render a probe contract")

    monkeypatch.setattr(dc, "probe", _explode)

    code, message = dc.guard(tmp_path)

    assert code == 1
    assert "could not be taken" in message


def test_the_guard_watches_BOTH_sides_of_the_hub_half_of_the_seam():
    """`SEAM_PATHS` names the writer AND this probe. The second is not defensive padding: a
    gate that does not watch its own edit can be neutered by the commit that neuters it."""
    assert "scripts/gen_lane_contract.py" in dc.SEAM_PATHS
    assert "scripts/dispatch_conformance.py" in dc.SEAM_PATHS


def _never_called(*_a, **_k):
    raise AssertionError("the guard probed on a commit that touches no seam file")


def test_the_probe_asks_for_a_non_default_model_so_a_default_cannot_fake_the_property(tmp_path):
    """`[#717]` was silent precisely because the surface's default and the contract's declared
    model agreed by accident. A probe that asked for the default would be silent the same way."""
    result = dc.probe(tmp_path, tier=dc.TIER_NO_SHELL)

    assert result.model != dispatch_default_model()


def dispatch_default_model() -> str:
    import gen_lane_contract as glc
    return glc.DEFAULT_MODEL
