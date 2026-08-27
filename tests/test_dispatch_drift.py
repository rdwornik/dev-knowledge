"""`[#592]` — the dispatch drift organ. RED-first, with a seeded rival-command fixture.

The row's done-when, leg by leg:

  * every literal command in PLAYBOOK Ch8's table resolves via `Get-Command` at commit time
  * `.claude/commands/lane-boot.md` is asserted to contain the ruled verb
  * **a fire-test proves the check REDs on a planted dead command**
  * the machine-dependence is handled explicitly — in CI or a container the check reports
    `info` and NEVER green-by-skip

Nothing here spawns a PowerShell. The resolver is injected, so the fire-test plants a dead
command on every host including the ones that have no shell at all — which is the same
family-3 discipline `[#596]` names: a guard whose firing is conditional on the environment it
polices proves nothing on the machine that breaks it.
"""
from __future__ import annotations

import textwrap

import pytest

import dispatch_drift as dd


# --- fixtures ---------------------------------------------------------------

_PLAYBOOK_TEMPLATE = textwrap.dedent("""\
    ## Ch8. Session boundaries

    {start} — the SOLE literal-command site

    Some framing prose that names nothing.

    ```
    {fence_commands}
    ```

    {prose}
    {end}

    - A standing rule that names no command.
    """)


def _playbook(*, fence_commands: str = "dispatch <FILE.md>",
              prose: str = "",
              start: str = dd.SECTION_START,
              end: str = dd.SECTION_END) -> str:
    """A PLAYBOOK-shaped fixture carrying exactly one dispatch-table section.

    Substituted AFTER the dedent, not inside an f-string: a multi-line `fence_commands` whose
    later lines carry no indentation makes `dedent` compute an empty common prefix, so the
    fence markers move off column 0 and `_FENCE_BLOCK_RE` — which is `^```` under MULTILINE —
    matches nothing. The scan then reports an EMPTY corpus, which is indistinguishable from a
    clean one. That is exactly the failure this organ exists to refuse, reached through its
    own test fixture.
    """
    return _PLAYBOOK_TEMPLATE.format(start=start, end=end, prose=prose,
                                     fence_commands=fence_commands.rstrip())


_LANE_BOOT_OK = textwrap.dedent("""\
    # /lane-boot

    From a fresh terminal at the repo root:

    ```
    dispatch <contract-path>
    ```

    **This is the ruled verb** (STANDING_RULINGS section V).
    """)


def _resolver(missing: set[str]):
    """An injected `Get-Command` stand-in: everything resolves except `missing`."""
    def resolve(names):
        return [dd.Resolution(n, n not in missing,
                              "MISSING" if n in missing else "Application")
                for n in names]
    return resolve


# --- extraction -------------------------------------------------------------

def test_section_is_bounded_by_its_two_headings():
    section = dd.dispatch_table_section(_playbook())
    assert dd.SECTION_START in section
    assert dd.SECTION_END not in section
    assert "A standing rule that names no command." not in section


def test_a_renamed_start_heading_raises_rather_than_scanning_nothing():
    """A renamed heading is the drift this organ exists to notice — an empty scan reports
    zero drift, which is exactly what a broken scan looks like."""
    with pytest.raises(dd.DispatchDriftError):
        dd.dispatch_table_section(_playbook(start="#### Some other heading"))


def test_a_missing_end_heading_raises():
    with pytest.raises(dd.DispatchDriftError):
        dd.dispatch_table_section(_playbook(end="#### Not the end boundary"))


def test_fenced_first_tokens_are_commands_and_flags_are_not():
    section = dd.dispatch_table_section(_playbook(
        fence_commands="dispatch <FILE.md> -DryRun\n           [-Machine basicLinux32gb]\n"))
    names = [c.name for c in dd.extract_commands(section)]
    assert names == ["dispatch"]


def test_the_interactive_first_message_is_not_a_command():
    """Ch8 says in terms *"the second line is its first message, not a shell command"*."""
    section = dd.dispatch_table_section(_playbook(
        fence_commands="claude\nRead <PROMPTS_DIR>\\<FILE>.md and execute it exactly.\n"))
    names = [c.name for c in dd.extract_commands(section)]
    assert names == ["claude"]
    assert "Read" not in names


def test_prose_verb_nouns_are_commands_in_both_backtick_shapes():
    section = dd.dispatch_table_section(_playbook(
        prose="Manage: `Get-CloudSession cse_01ABC` and `Stop-DispatchCodespace`.\n"))
    names = [c.name for c in dd.extract_commands(section)]
    assert "Get-CloudSession" in names
    assert "Stop-DispatchCodespace" in names


def test_a_command_is_reported_once_with_its_first_surface():
    section = dd.dispatch_table_section(_playbook(
        fence_commands="Dispatch-Cloud <FILE.md>\n",
        prose="The alias `Dispatch-Cloud` is canonical.\n"))
    refs = dd.extract_commands(section)
    assert [r.name for r in refs] == ["Dispatch-Cloud"]
    assert refs[0].surface == "fence"


# --- THE FIRE-TEST: a planted dead command REDs the check -------------------

def test_a_planted_dead_command_reds_the_check():
    """The row's own words: *"a fire-test proves the check REDs on a planted dead command"*."""
    section = dd.dispatch_table_section(_playbook(
        fence_commands="dispatch <FILE.md>\nDispatch-Ghost <FILE.md>\n"))
    commands = dd.extract_commands(section)
    findings = dd.check_commands(commands, tier=dd.TIER_HOST,
                                 resolver=_resolver({"Dispatch-Ghost"}))
    assert [f.status for f in findings] == ["fail"]
    assert "Dispatch-Ghost" in findings[0].detail


def test_a_live_command_set_is_clean():
    section = dd.dispatch_table_section(_playbook())
    findings = dd.check_commands(dd.extract_commands(section), tier=dd.TIER_HOST,
                                 resolver=_resolver(set()))
    assert findings == []


def test_a_name_get_command_answers_nothing_about_is_unresolved(monkeypatch):
    """A name producing no output line is UNRESOLVED, not silently dropped.

    The real resolver's own gap-filling, exercised against a stubbed subprocess: a
    `Get-Command` run answering about fewer names than it was asked about has given a PARTIAL
    answer, and treating a missing line as "fine" is how a dead command ships green.
    """
    class _Out:
        stdout = "dispatch\tApplication\n"    # asked about two, answered about one

    monkeypatch.setattr(dd.subprocess, "run", lambda *a, **k: _Out())
    results = dd.resolve_via_get_command(["dispatch", "Dispatch-Ghost"], shell="pwsh")
    assert [(r.name, r.resolved) for r in results] == [
        ("dispatch", True), ("Dispatch-Ghost", False)]
    assert "no answer" in results[1].detail


def test_an_empty_command_table_fails():
    """The section whose whole purpose is to be the sole literal-command site is empty."""
    findings = dd.check_commands([], tier=dd.TIER_HOST, resolver=_resolver(set()))
    assert [f.status for f in findings] == ["fail"]
    assert "NO literal command" in findings[0].detail


# --- machine-dependence: declared, never green-by-skip ----------------------

def test_a_shell_less_host_warns_and_names_every_unresolved_command():
    section = dd.dispatch_table_section(_playbook(
        fence_commands="dispatch <FILE.md>\nDispatch-Cloud <FILE.md>\n"))
    findings = dd.check_commands(dd.extract_commands(section), tier=dd.TIER_NO_SHELL)
    assert [f.status for f in findings] == ["warn"]
    assert "dispatch" in findings[0].detail
    assert "Dispatch-Cloud" in findings[0].detail


def test_the_shell_less_tier_is_never_a_green_rendering_status():
    """`unavailable` renders as N/A and projects onto `pass`, so it SHIPS. `warn` does not."""
    findings = dd.check_commands([dd.CommandRef("dispatch", "fence")], tier=dd.TIER_NO_SHELL)
    assert findings
    for finding in findings:
        assert finding.status not in {"pass", "unavailable", "n/a"}


def test_host_tier_is_derived_from_a_real_shell_lookup():
    assert dd.host_tier(shell="/usr/bin/pwsh") == dd.TIER_HOST
    assert dd.host_tier(shell=None) in {dd.TIER_HOST, dd.TIER_NO_SHELL}


def test_resolving_without_a_shell_raises_rather_than_returning_all_clear(monkeypatch):
    """The shell-less path RAISES so the caller has to pick a tier deliberately — an empty
    resolution list would read as "every command resolved"."""
    monkeypatch.setattr(dd, "find_powershell", lambda: None)
    with pytest.raises(dd.DispatchDriftError):
        dd.resolve_via_get_command(["dispatch"])


# --- leg 2: /lane-boot names the ruled verb ---------------------------------

def test_lane_boot_naming_the_ruled_verb_is_clean():
    assert dd.check_lane_boot(_LANE_BOOT_OK) == []


def test_lane_boot_without_the_ruled_verb_in_a_fence_fails():
    text = _LANE_BOOT_OK.replace("dispatch <contract-path>", "Dispatch-Lane <slug> <file>")
    findings = dd.check_lane_boot(text)
    assert [f.status for f in findings] == ["fail"]
    assert dd.RULED_VERB in findings[0].detail


def test_a_rival_raw_form_in_a_fence_fails():
    """V4: the raw form does not appear in a command file — a fence is a line a seat copies."""
    text = _LANE_BOOT_OK.replace("dispatch <contract-path>",
                                 "dispatch <contract-path>\nclaude --worktree foo --bg")
    findings = dd.check_lane_boot(text)
    assert any(f.status == "fail" and "FENCE" in f.detail for f in findings)


def test_a_labelled_prose_mention_of_the_rival_form_is_sanctioned():
    """The live file's own supersession note — the record that makes the fix legible."""
    text = _LANE_BOOT_OK + (
        "\nUntil 2026-08-25 this line emitted a raw `claude --worktree ... --bg ...` form, "
        "the form PLAYBOOK Ch8 itself calls the FALLBACK form.\n")
    assert dd.check_lane_boot(text) == []


def test_an_unlabelled_prose_mention_of_the_rival_form_warns():
    text = _LANE_BOOT_OK + "\nBoot it with `claude --worktree <name> --bg`.\n"
    findings = dd.check_lane_boot(text)
    assert [f.status for f in findings] == ["warn"]
    assert "UNLABELLED" in findings[0].detail.upper()


# --- the live repo ----------------------------------------------------------

@pytest.mark.live_repo
def test_the_live_dispatch_table_extracts_the_documented_command_set():
    """The organ's corpus on the live tree, asserted by PROPERTY rather than by a roster.

    A hard-coded list of twelve names would be a restated roster that rots at the next Ch8
    edit (CLAUDE.md Sec.4 M2). What is asserted is what the ruling guarantees: the ruled verb
    and the three substrate verbs of STANDING_RULINGS V3 are all in the extracted set.
    """
    root = dd.Path(__file__).resolve().parent.parent
    section = dd.dispatch_table_section(
        (root / dd.PLAYBOOK_RELPATH).read_text(encoding="utf-8"))
    names = {c.name for c in dd.extract_commands(section)}
    assert {"dispatch", "Dispatch-Local", "Dispatch-Cloud", "Dispatch-Codespace"} <= names


@pytest.mark.live_repo
def test_the_live_lane_boot_names_the_ruled_verb():
    root = dd.Path(__file__).resolve().parent.parent
    text = (root / dd.LANE_BOOT_RELPATH).read_text(encoding="utf-8")
    assert [f for f in dd.check_lane_boot(text) if f.status == "fail"] == []
