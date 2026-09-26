"""`templates/dispatcher-order-template.md` launches only through `dispatch.py queue --watch` and
repairs only through `dispatch.py repair` (LANE-5B3-1-wire-queue, successor to N2 lane 24, never
launched -- LANE-5B2-24-dispatcher-adopts-queue.md).

Two things are proved here, RED-first in the words of the Done-contract's item 1:

  * the TEMPLATE TEXT itself names no per-lane hand launch verb any more -- the only
    `dispatch.py <verb>` mentions are `queue` (the launch surface) and `repair` (the repair
    surface), plus the one documented, recorded FALLBACK to the contract's own raw `## Dispatch`
    line when the verb itself refuses               -> test_template_*
  * the exact queue command line the template's Launcher bullet prescribes is not merely prose: it
    is REAL and EXECUTABLE. This test extracts that fenced command, fills its placeholders for a
    small synthetic ("dry") batch -- a local lane, a local lane that depends on it, and a codespace
    lane -- and runs it (with `--dry-run`, so nothing is spawned) to prove it computes a real,
    dependency-respecting order over that batch, the same way a live dispatcher session would
    invoke it verbatim out of the rendered order         -> test_the_templates_own_queue_line_*
"""
from __future__ import annotations

import re
import shlex
from pathlib import Path

from click.testing import CliRunner

import dispatch as d

TEMPLATE_PATH = (Path(__file__).resolve().parents[1] / "templates"
                / "dispatcher-order-template.md")


def _template_text() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


# --- the template's own text: `queue` and `repair` are the whole launch/repair surface -----------

def test_template_names_queue_as_its_launcher():
    text = _template_text()
    assert "dispatch.py queue --watch" in text


def test_template_leaves_no_per_lane_hand_launch_verb():
    """The old shape called `dispatch.py launch` once per lane, once per wave (N2 lane 9's own
    Value line: "the dispatcher still launches by hand"). Nothing in the template may invoke
    `launch` any more -- `queue` is the only verb that starts a local lane."""
    text = _template_text()
    assert "dispatch.py launch" not in text


def test_template_names_repair_as_its_repair_verb():
    text = _template_text()
    assert "dispatch.py repair <slug>" in text


def test_template_sequence_has_exactly_one_launch_step_and_one_repair_step():
    """The old Sequence enumerated three separate launch steps (wave alpha/beta/gamma), each a
    hand-invocation point. The new Sequence collapses that to ONE launch step; repairs are their
    own, separate step -- neither may re-appear."""
    text = _template_text()
    sequence = text.split("## Sequence", 1)[1]
    launch_steps = re.findall(r"^\d+\. \*\*Launch through the queue", sequence, re.MULTILINE)
    repair_steps = re.findall(r"^\d+\. \*\*Repairs\.\*\*", sequence, re.MULTILINE)
    assert len(launch_steps) == 1
    assert len(repair_steps) == 1


def test_template_documents_exactly_one_hand_launch_fallback():
    """"No hand launch line remains except the recorded fallback when the launcher refuses"
    (Done-contract item 1). The fallback is named, singular, and tied to the verb's own refusal --
    not a second, independent way to launch a lane."""
    text = _template_text()
    assert text.count("FALLBACK <slug>:") == 1
    assert "on the verb's own refusal" in text.lower()


def test_template_never_adds_a_normative_keyword():
    """Common rules lesson (a): `must`/`shall`/`never` add to `templates/**` at zero silent-rule
    headroom. The template carried none of the three before this lane touched it (grepped at the
    contract's read-first step) -- this diff must not introduce one either."""
    text = _template_text()
    assert re.search(r"\b(must|shall|never)\b", text, re.IGNORECASE) is None


# --- the template's queue line is executable, not only prose -------------------------------------

def _extract_queue_command(text: str) -> str:
    """The fenced command block right after the Launcher bullet's lead-in sentence."""
    marker = "Launcher — ONE call, not one per lane:"
    after = text.split(marker, 1)[1]
    fence = after.split("```\n", 1)[1]
    body = fence.split("```", 1)[0]
    return body.replace("\\\n", " ")   # join the line-continuations the doc uses for readability


def _dry_contract(tmp_path: Path, filename: str, slug: str, *, starts_after: tuple = (),
                  codespace: bool = False) -> Path:
    """The minimal `LANE-*.md` grammar `plan_lint.load_contracts` (and so `dispatch.py queue`)
    reads: the Model table, a `## Dispatch` fence, an optional `Starts after` clause, and the slug
    pairing line every real contract carries -- the same minimal shape
    `tests/test_dispatch_queue.py`'s own `_contract` fixture writes, kept independent here on
    purpose (this file proves the TEMPLATE's own command line, not `queue`'s unit behaviour, which
    that file already covers)."""
    lines = [f"# LANE {slug} -- a dry-batch synthetic lane\n",
             "| Model | Mode | Effort |\n|---|---|---|\n| claude-sonnet-5 | execute | high |\n"]
    if codespace:
        dispatch_line = f"Dispatch-Codespace {filename} -Slug {slug} -Model claude-sonnet-5 -Detach"
    else:
        dispatch_line = (f'claude --bg -n {slug} --model claude-sonnet-5 --effort high '
                         f'--permission-mode bypassPermissions --worktree {slug} "..."')
    lines.append(f"## Dispatch\n\n```\n{dispatch_line}\n```\n")
    if starts_after:
        joined = " and ".join(f"`{dep}`" for dep in starts_after)
        verb = "is" if len(starts_after) == 1 else "are"
        lines.append(f"**Starts after {joined} {verb} merged.**\n")
    lines.append(f"slug `{slug}` -> branch `worktree-{slug}` -> contract `{filename}`\n")
    lines.append("**Files you own:** `scripts/nothing.py`.\n")
    path = tmp_path / filename
    path.write_text("\n\n".join(lines), encoding="utf-8")
    return path


def test_the_templates_own_queue_line_renders_and_computes_a_dry_batch_order(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))
    a = _dry_contract(tmp_path, "LANE-dry-a.md", "lane-dry-a")
    b = _dry_contract(tmp_path, "LANE-dry-b.md", "lane-dry-b", starts_after=("lane-dry-a",))
    cs = _dry_contract(tmp_path, "LANE-dry-cs.md", "lane-dry-cs", codespace=True)
    state_file = tmp_path / "SESSION-integrator-dry-2026-09-26.md"
    state_file.write_text("STATE lane-dry-a MERGED abc12345 12:00 5\n", encoding="utf-8")

    command = _extract_queue_command(_template_text())
    assert "dispatch.py queue --watch" in command
    filled = (command
             .replace("<BATCH>", "DRY")
             .replace("<M>", "4")
             .replace("<N_MB>", "0")
             .replace("<STATE_FILE>", str(state_file))
             .replace("<DEADLINE_S>", "5")
             .replace("<HUB_ROOT>", str(tmp_path))
             .replace("<CONTRACT_1> <CONTRACT_2> ...", f"{a} {b} {cs}"))
    tokens = shlex.split(filled, posix=False)
    assert tokens[:5] == ["uv", "run", "--locked", "python", "scripts/dispatch.py"]
    argv = [t.strip('"') for t in tokens[5:]]   # drop the `uv run --locked python scripts/` shim
    assert argv[0] == "queue"

    # `--dry-run` proves the SAME argv the rendered order would carry computes a real order,
    # without this test spawning anything -- `queue`'s own live-fire path is `test_dispatch_queue`'s
    # job, not this file's.
    out = CliRunner().invoke(d.cli, argv + ["--dry-run"])
    assert out.exit_code == 0, out.output
    assert "lane-dry-a" in out.output
    assert "lane-dry-b" in out.output
    assert "lane-dry-cs" in out.output
    a_pos = out.output.index("lane-dry-a")
    b_pos = out.output.index("lane-dry-b")
    assert a_pos < b_pos   # the dependency is still respected once the line is actually run


# --- the repair line is executable, not only prose ------------------------------------------------

def test_the_templates_repair_line_relaunches_into_the_existing_worktree(tmp_path):
    command_line = [ln for ln in _template_text().splitlines()
                    if "dispatch.py repair <slug>" in ln][0]
    filled = (command_line.strip()
             .replace("<slug>", "lane-dry-a")
             .replace("<CONTRACT>.md", "LANE-dry-a.md")
             .replace("<MODEL>", "claude-sonnet-5")
             .replace("<EFFORT>", "high"))
    tokens = shlex.split(filled, posix=False)
    argv = [t.strip('"') for t in tokens[5:]]
    assert argv[0] == "repair"

    tree = tmp_path / ".claude" / "worktrees" / "lane-dry-a"
    tree.mkdir(parents=True)
    calls = []

    def fake_spawn(spawn_argv, env, cwd, log_path=None):
        calls.append(Path(cwd))
        return d.Spawned(0, "backgrounded deadbeef", None)

    request = d.RepairRequest(slug=argv[1], attempt=1, model="claude-sonnet-5", effort="high",
                              contract=tmp_path / "LANE-dry-a.md")
    result = d.repair_lane(request, repo_root=tmp_path, spawn=fake_spawn, environ={})
    assert result.returncode == 0
    assert calls == [tree]
