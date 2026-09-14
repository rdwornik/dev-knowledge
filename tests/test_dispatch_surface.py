"""Tests for scripts/dispatch_surface.py + audit.py::check_dispatch_verb_agreement (R5).

THE DEFECT, as `protocols/STANDING_RULINGS.md` §V measured it: the hub carried FOUR rival
literal launch commands for one act, `/lane-boot` emitted the form Ch8 itself labels a fallback
while silently dropping `--model` and `--effort`, and roughly thirty consecutive browser seats
failed to launch a lane — "not uninformed; informed by four sources that disagreed." §V's own
closing line calls the organ that would catch this "owed and unbuilt". This is the tree-side
half of it.

Every test that asserts a violation seeds a RIVAL into a temp copy of the two real files, so the
RED is produced by the condition the gate exists to refuse rather than by a stub.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import audit as aud  # noqa: E402
import dispatch_surface as ds  # noqa: E402

_REPO = Path(__file__).resolve().parents[1]


def _mirror(tmp_path: Path) -> Path:
    """A temp repo carrying the three REAL files this gate reads, so a seeded rival is a
    mutation of live content rather than a fixture that merely resembles it."""
    root = tmp_path / "repo"
    for rel in (ds.PLAYBOOK_PATH, *ds.AGREEMENT_SITES):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_REPO / rel, dst)
    return root


def _seed_rival(root: Path, rel: str, line: str) -> None:
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8") + f"\n```\n{line}\n```\n", encoding="utf-8")


# --- reading the SOLE literal-command site ----------------------------------

def test_ruled_form_is_read_from_ch8_not_hardcoded():
    lines = ds.ruled_form(_REPO)
    assert lines, "Ch8's LOCAL-lane form must be readable"
    assert lines[0].startswith("dispatch ")


def test_ruled_verb_is_the_lead_token():
    assert ds.ruled_verb(_REPO) == "dispatch"


def test_local_row_search_is_bounded_to_the_dispatch_table(tmp_path):
    """If the LOCAL row leaves the table but its marker survives later in the chapter as prose,
    an unbounded search would render whatever fence followed THAT as the ruled command — the
    exact drift this reader exists to detect, answered confidently and wrongly. (terra pass 4.)"""
    root = tmp_path / "moved"
    (root / "protocols").mkdir(parents=True)
    (root / ds.PLAYBOOK_PATH).write_text(
        f"# P\n\n{ds._TABLE_HEADING}\n\nthe table, with its LOCAL row removed\n\n"
        "## A later chapter\n\n"
        f"Historical note: {ds._LOCAL_ROW} used to read:\n\n```\nnot-the-ruled-verb X.md\n```\n",
        encoding="utf-8")
    assert ds.ruled_form(root) is None


def test_local_row_is_still_found_inside_its_own_subsections(tmp_path):
    """Negative control for the bound: the live table nests the row under a `#####` sub-heading,
    so the section boundary has to admit deeper headings or the reader stops working entirely."""
    root = tmp_path / "nested"
    (root / "protocols").mkdir(parents=True)
    (root / ds.PLAYBOOK_PATH).write_text(
        f"# P\n\n{ds._TABLE_HEADING}\n\n##### Layer 2 — the commands\n\n"
        f"{ds._LOCAL_ROW} (own worktree)\n\n```\ndispatch <FILE.md>\n```\n",
        encoding="utf-8")
    assert ds.ruled_form(root) == ["dispatch <FILE.md>"]


def test_ruled_form_returns_none_rather_than_a_remembered_command(tmp_path):
    """A second copy of the line is the defect §V ruled on, so the degrade path is a POINTER,
    never a fallback string. None is the signal that produces one."""
    assert ds.ruled_form(tmp_path) is None                       # no PLAYBOOK at all
    root = tmp_path / "reworded"
    (root / "protocols").mkdir(parents=True)
    (root / ds.PLAYBOOK_PATH).write_text("# P\n\n## Something else\n", encoding="utf-8")
    assert ds.ruled_form(root) is None                           # heading moved/reworded


# --- the fence split, which the whole rival test rests on -------------------

def test_fenced_lines_ignores_prose_backticks():
    text = "a line mentioning `claude --bg` in prose\n\n```\ndispatch FILE.md\n```\n"
    assert ds.fenced_lines(text) == ["dispatch FILE.md"]


# --- agreement, live -------------------------------------------------------

def test_live_surfaces_agree_with_the_ruled_verb():
    """The tree as it stands: both point-of-use sites name `dispatch` in a fence and carry no
    rival form in one. A regression here is the exact §V recurrence."""
    assert ds.agreement_findings(_REPO) == []


def test_check_is_green_on_the_live_repo():
    findings = aud.check_dispatch_verb_agreement(_REPO)
    assert [f.status for f in findings] == ["pass"]


def test_check_is_registered_in_all_checks():
    assert aud.check_dispatch_verb_agreement in aud.ALL_CHECKS


# --- RED against a seeded rival --------------------------------------------

def test_seeded_raw_claude_bg_form_in_lane_boot_is_refused(tmp_path):
    """§V V4: the raw form "does not appear in a command file or a template". This is the exact
    line `/lane-boot` emitted until 2026-08-25 — the one that dropped --model and --effort."""
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md",
                "claude --worktree lane-x --bg --permission-mode bypassPermissions")
    hits = ds.agreement_findings(root)
    assert any("lane-boot.md" in h and "rival" in h for h in hits), hits


def test_seeded_rival_in_the_template_is_refused(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, "templates/prompt-template.md", "claude --bg --model opus --effort high")
    hits = ds.agreement_findings(root)
    assert any("prompt-template.md" in h and "rival" in h for h in hits), hits


def test_seeded_superseded_alias_is_refused(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "Dispatch-CloudBrief BRIEF.md")
    assert any("Dispatch-CloudBrief" in h for h in ds.agreement_findings(root))


def test_seeded_version_named_alias_is_refused(tmp_path):
    """§V V3: substrate-named verbs are canonical, version-named ones are deprecated aliases."""
    root = _mirror(tmp_path)
    _seed_rival(root, "templates/prompt-template.md", "Dispatch-Lane lane-x FILE.md")
    assert any("Dispatch-Lane" in h for h in ds.agreement_findings(root))


def test_prose_mention_of_the_raw_form_is_NOT_refused(tmp_path):
    """The negative control that matters. Both files RECORD the correction in prose — "this line
    used to emit a raw `claude --worktree … --bg …` form" — and a gate that refused the mention
    would force them to delete the history explaining why they changed."""
    root = _mirror(tmp_path)
    p = root / ".claude/commands/lane-boot.md"
    p.write_text(p.read_text(encoding="utf-8")
                 + "\nUntil 2026-08-25 this emitted a raw `claude --worktree x --bg` form.\n",
                 encoding="utf-8")
    assert ds.agreement_findings(root) == []


def test_dispatch_local_fallback_is_not_a_rival(tmp_path):
    """§V V2 makes `Dispatch-Local` the documented manual fallback, so it stays legal."""
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "Dispatch-Local lane-x FILE.md -Effort high")
    assert ds.agreement_findings(root) == []


def test_site_that_stops_naming_the_ruled_verb_is_refused(tmp_path):
    """The other §V class: a pointer that stopped pointing."""
    root = _mirror(tmp_path)
    p = root / "templates/prompt-template.md"
    p.write_text(p.read_text(encoding="utf-8").replace("dispatch <THIS-CONTRACT-FILENAME>.md",
                                                       "somethingelse <FILE>.md"),
                 encoding="utf-8")
    assert any("no fenced line names the ruled verb" in h for h in ds.agreement_findings(root))


def test_unreadable_ch8_is_reported_not_waved_through(tmp_path):
    """A gate whose anchor moved says so. It never passes because it could not look."""
    hits = ds.agreement_findings(tmp_path)
    assert len(hits) == 1 and "unreadable" in hits[0]


def test_unreadable_playbook_is_not_reported_as_not_applicable(tmp_path, monkeypatch):
    """"There is no dispatch table" and "the canonical command source could not be opened" are
    different answers, and `Path.is_file()` collapses them into the first. Only genuine absence
    is n/a. (terra pass 5.)"""
    import os

    import audit as aud_mod
    root = _mirror(tmp_path)
    real_stat, real_read = os.stat, Path.read_text

    def _is_playbook(p) -> bool:
        return str(p).replace("\\", "/").endswith(ds.PLAYBOOK_PATH)

    def fake_stat(path, *a, **kw):
        if _is_playbook(path):
            raise PermissionError(13, "locked")
        return real_stat(path, *a, **kw)

    def fake_read(self, *a, **kw):
        if _is_playbook(self):
            raise PermissionError(13, "locked")
        return real_read(self, *a, **kw)
    monkeypatch.setattr(aud_mod.os, "stat", fake_stat)
    monkeypatch.setattr(Path, "read_text", fake_read)
    findings = aud_mod.check_dispatch_verb_agreement(root)
    # The stat failure alone would have short-circuited to n/a before the predicate ever ran;
    # it now falls through, and the predicate reports the canonical source as unreadable.
    assert [f.status for f in findings] == ["fail"]
    assert "unreadable" in findings[0].evidence


def test_check_is_fail_class_on_a_seeded_rival(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "claude --bg --model opus")
    findings = aud.check_dispatch_verb_agreement(root)
    assert [f.status for f in findings] == ["fail"]
    assert "|" not in findings[0].evidence


# ===============================================================================================
# RED-FIRST WITNESSES (ADR-108 §B) -- `[#752]`, the DECLARED-vs-HONOURED gap.
#
# THE MEASURED NO-OP. `lane-x-689-conductor-e-proof` froze `| opusplan | execute | high |` under
# `**Shape:** local`, the operator ruled that tier onto the line deliberately, `MODEL_ENUM` was
# widened RED-first to admit it, the dry run printed it -- and the lane ran **84 of 84 assistant
# messages on `claude-sonnet-5`, zero Opus** (batch X3 manifest §6 finding 7). `opusplan` is a
# SPLIT tier -- Opus while the session is in plan mode, Sonnet after -- and every dispatch constant
# puts a lane on `--permission-mode bypassPermissions`, which NEVER enters plan mode. No plan
# phase, no Opus phase. Every surface agreed; only the behaviour dissented, and every routing
# decision in that window was advisory.
#
# WHY THE EXISTING GATES COULD NOT CATCH IT, which is what these tests are for. `MODEL_ENUM`
# admits `opusplan` because the CLI RESOLVES it -- measured: a bogus id returns
# `[claude-code:unrecognized_model]`, this one returns a normal completion -- and
# `gen_lane_contract.check_contract` asserts the routing row and the dispatch line AGREE. Both
# were true here. Agreement between two surfaces that are wrong about the same thing is not a
# check: the missing question was never "do these two strings match" but "can the launcher this
# SHAPE uses actually HONOUR this value".
#
# THE MODE COLUMN IS THE SAME DEFECT ONE COLUMN OVER. `MODE_ENUM` has always carried `plan`, and
# nothing anywhere resolved it into a flag -- a contract declaring `| opus | plan | high |` under
# `**Shape:** local` dispatched identically to `execute`, because the mode column reached no
# launcher argument at all. A declared field no code reads is a decision the tree records and
# does not make.
# ===============================================================================================

_X689 = ("docs/audits/2026-09-13-technical-batch-x3-launch-contracts/"
         "LANE-x-689-conductor-e-proof.md")
_THIS_LANE = ("docs/audits/2026-09-14-technical-batch-y-launch-contracts/"
              "LANE-y-752-declared-model-runs.md")


def _flagval(launch, flag: str):
    """The value following `flag` in a resolved launch, or None."""
    flags = list(launch.flags)
    return flags[flags.index(flag) + 1] if flag in flags else None


# --- the model half: a tier the background launcher does not honour ---------

def test_opusplan_on_a_background_lane_is_refused_with_its_measurement():
    """The witnessed no-op, refused at the surface that resolves it.

    Not "warned about": firing it literally does NOT honour the order either -- it yields Sonnet,
    which the contract never names -- so there is no faithful-literal option, and passing the flag
    through is itself a deviation. A refusal is what makes the seat choose one out loud."""
    launch = ds.resolve_launch(model="opusplan", mode="execute", effort="high",
                               shape="local", slug="lane-x-689-conductor-e-proof")
    assert not launch.ok
    joined = " ".join(launch.refusals).lower()
    assert "opusplan" in joined
    assert "sonnet" in joined, "the refusal must carry WHAT it actually runs"
    assert "--model" not in launch.flags, "a refused tier must not also be emitted"


def test_opusplan_is_NOT_refused_for_an_attended_seat():
    """The negative control, and the scope is narrower than the refusal looks. `opusplan` is
    CORRECT for an interactive seat -- an attended session can enter plan mode, so the split tier
    has both halves -- and AX22-3 routes the integrator seat to it. Same word, two populations; a
    gate that refused both would break a live routing decision in order to fix a different one."""
    launch = ds.resolve_launch(model="opusplan", mode="plan", effort="high",
                               shape="interactive", slug="integrator")
    assert launch.ok, launch.refusals
    assert _flagval(launch, "--model") == "opusplan"


# --- the mode half: a declared column that reached no flag -----------------

def test_execute_mode_resolves_to_the_permission_mode_a_bg_lane_can_run():
    """`execute` -> `bypassPermissions`, and the resolution is what makes the column MEAN
    something. A `--bg` lane has nobody to answer a permission prompt."""
    launch = ds.resolve_launch(model="opus", mode="execute", effort="xhigh",
                               shape="local", slug="lane-y-752-declared-model-runs")
    assert launch.ok, launch.refusals
    assert _flagval(launch, "--permission-mode") == ds.BACKGROUND_PERMISSION_MODE


def test_plan_mode_on_a_background_lane_is_refused_rather_than_silently_ignored():
    """The mode column's own version of the same defect. `plan` is a real `--permission-mode`
    value and a real `MODE_ENUM` member, and a background lane cannot run it: there is nobody to
    approve the plan, and bypassPermissions -- the standing dispatch constant -- is precisely the
    mode that never enters one. Declaring it and dispatching `execute` anyway is the opusplan
    shape exactly, moved one column over."""
    launch = ds.resolve_launch(model="opus", mode="plan", effort="high",
                               shape="local", slug="lane-z-000-planner")
    assert not launch.ok
    assert any("plan" in r for r in launch.refusals), launch.refusals


def test_plan_mode_IS_honoured_for_an_attended_seat():
    launch = ds.resolve_launch(model="opus", mode="plan", effort="high",
                               shape="interactive", slug="seat")
    assert launch.ok, launch.refusals
    assert _flagval(launch, "--permission-mode") == "plan"


# --- the closed enums, refused with the enum named -------------------------

def test_effort_outside_the_closed_enum_is_refused_naming_the_enum():
    launch = ds.resolve_launch(model="opus", mode="execute", effort="extreme",
                               shape="local", slug="lane-z")
    assert not launch.ok
    assert any("xhigh" in r for r in launch.refusals), "name the enum, never round to a neighbour"


def test_model_outside_the_enum_is_refused_naming_the_enum():
    launch = ds.resolve_launch(model="gpt", mode="execute", effort="high",
                               shape="local", slug="lane-z")
    assert not launch.ok
    assert any("gpt" in r for r in launch.refusals)


def test_an_off_enum_shape_is_refused_rather_than_rounded_to_local():
    """Rounding `remote` to `local` would emit a CONFIDENTLY WRONG command, which is strictly
    worse than emitting none -- `validate_shape`'s own reasoning, reused rather than restated."""
    launch = ds.resolve_launch(model="opus", mode="execute", effort="high",
                               shape="remote", slug="lane-z")
    assert not launch.ok


# --- what a clean resolution actually produces -----------------------------

def test_the_resolved_line_carries_every_dispatch_constant():
    """§V's measured defect was a launch form that SILENTLY DROPPED `--model` and `--effort`.
    A resolution that omitted one would reintroduce it, so every constant is asserted by name."""
    launch = ds.resolve_launch(model="opus", mode="execute", effort="xhigh",
                               shape="local", slug="lane-y-752-declared-model-runs")
    assert launch.ok, launch.refusals
    assert "--bg" in launch.flags
    assert _flagval(launch, "--model") == "opus"
    assert _flagval(launch, "--effort") == "xhigh"
    assert _flagval(launch, "--worktree") == "lane-y-752-declared-model-runs"
    assert _flagval(launch, "--permission-mode") == ds.BACKGROUND_PERMISSION_MODE


def test_an_attended_seat_gets_no_bg_and_no_worktree():
    launch = ds.resolve_launch(model="opus", mode="execute", effort="high",
                               shape="interactive", slug="seat")
    assert launch.ok and "--bg" not in launch.flags and "--worktree" not in launch.flags


# --- reading a CONTRACT, which is where the declaration actually lives ------

def test_a_contracts_routing_row_and_shape_are_read_from_the_file():
    text = (_REPO / _THIS_LANE).read_text(encoding="utf-8")
    assert ds.contract_routing(text) == {"model": "opus", "mode": "execute", "effort": "xhigh"}
    assert ds.contract_shape(text) == "local"


def test_this_lanes_own_frozen_contract_resolves_clean():
    """The live positive control. This contract is `opus`/`execute`/`xhigh` under `local`, every
    value honourable, so the organ that refuses x-689 must not refuse this one."""
    assert ds.contract_findings(_REPO / _THIS_LANE) == []


def test_the_x689_contract_IS_refused_by_this_organ():
    """THE LIVE HISTORICAL WITNESS, and the reason it is a real file rather than a fixture: this
    contract passed its freeze gate, passed its dry run, printed the ordered tier on the resolved
    line, and produced a lane that ran Sonnet end to end. Every existing check said yes. If this
    assertion ever passes by finding nothing, the organ has stopped asking the one question that
    caught it."""
    hits = ds.contract_findings(_REPO / _X689)
    assert any("opusplan" in h for h in hits), hits


def test_a_contract_with_no_routing_row_is_reported_not_defaulted():
    """Silence is not a declaration. Defaulting the missing column would make the dispatcher
    decide the most expensive constant on the line (`[#717]`) on the contract's behalf."""
    assert ds.contract_routing("# LANE x\n\nno table here\n") is None


def test_a_bg_fence_that_drops_model_or_effort_is_refused(tmp_path):
    """§V's own defect, asserted on the fence rather than on the two point-of-use sites: the form
    `/lane-boot` emitted silently dropped `--model` and `--effort`, and roughly thirty consecutive
    seats launched lanes at a tier nobody chose."""
    p = tmp_path / "LANE-z-000-thin.md"
    p.write_text(
        "# LANE lane-z-000-thin\n\n| Model | Mode | Effort |\n|---|---|---|\n"
        "| opus | execute | high |\n\n## Dispatch\n\n**Shape:** `local`\n\n"
        "```\nclaude --bg --permission-mode bypassPermissions --worktree lane-z-000-thin \"go\"\n"
        "```\n\n## Worktree pairing\n\nslug `lane-z-000-thin` -> branch `worktree-lane-z-000-thin`"
        " -> contract `LANE-z-000-thin.md`\n", encoding="utf-8")
    hits = ds.contract_findings(p)
    assert any("--model" in h for h in hits), hits
    assert any("--effort" in h for h in hits), hits


def test_a_bg_fence_carrying_opusplan_is_refused_even_when_the_row_is_clean(tmp_path):
    """The two sources are free to disagree in BOTH directions, and `check_contract` reads the
    disagreement only as a mismatch. A clean routing row does not license an inert tier on the
    line the launcher actually receives."""
    p = tmp_path / "LANE-z-001-split.md"
    p.write_text(
        "# LANE lane-z-001-split\n\n| Model | Mode | Effort |\n|---|---|---|\n"
        "| opus | execute | high |\n\n## Dispatch\n\n**Shape:** `local`\n\n"
        "```\nclaude --bg --model opusplan --effort high --permission-mode bypassPermissions "
        "--worktree lane-z-001-split \"go\"\n```\n\n## Worktree pairing\n\n"
        "slug `lane-z-001-split` -> branch `worktree-lane-z-001-split` "
        "-> contract `LANE-z-001-split.md`\n", encoding="utf-8")
    assert any("opusplan" in h for h in ds.contract_findings(p))
