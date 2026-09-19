"""Retrieval-discipline gate for the boot base -- a pointer is admitted only where a session fetched it.

LEG 1 proposed turning ~50 KB of always-loaded prose into pointers and recorded that "a pointer
reliably gets the right item re-read" was NOT tested. `tests/boot_retrieval.py` is the instrument
(live child-`claude` probe, both arms); this module is the part that runs in the suite and BINDS a
conversion to that evidence:

* the scorer counts a tool call that reads a target, never prose that names one;
* every probe is well formed -- targets exist, the canary is held by the target and NOT leaked by
  the pointer text, the task names neither;
* an item may be pointer-form in CLAUDE.md only if `ecosystem/boot-retrieval-evidence.json`
  admits it (body arm could answer AND the pointer arm OBTAINED it in 2 of 3 runs, witnessed);
* the repo-tracked boot base stays under the ceiling the conversion measured.

HONEST LIMIT: the evidence file is a recorded run on a small model (n=3 per item). This gate proves a
conversion was tested, not that every future seat retrieves. It cannot run the model.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from boot_retrieval import (
    CONTROL,
    EVIDENCE,
    BODY_REV,
    ITEMS,
    REPO,
    POINTER_RUNS,
    Item,
    admitted,
    answer,
    body_form,
    boot_base,
    fetched,
    import_closure,
    pointer_sha,
    touched,
)

pytestmark = pytest.mark.live_repo

# Ceiling for what THIS REPO tracks and loads at boot (CLAUDE.md + @-imports + .claude/rules).
# User-level files and MEMORY.md are per-machine and are excluded so the gate is machine-stable.
# 42,500 B before -> 39,689 B after: only the command and skill rosters survived the retrieval test
# (Claude Code already injects their descriptions). The hook ids, the recent-ADR fragment and the
# methodology roster were probed and REFUSED (fetched 1-2 of 3), so their bodies stayed. The ceiling
# ratchets that small gain; it does not restate LEG 1's ~27 KB projection, which needs the items the
# evidence did not admit (see the JOURNAL entry and the handback).
REPO_BOOT_CEILING = 40_000


def _stream(*blocks: dict, result: str = "") -> str:
    lines = [json.dumps({"type": "assistant", "message": {"content": [b]}}) for b in blocks]
    lines.append(json.dumps({"type": "result", "result": result}))
    return "\n".join(lines)


def test_a_read_of_a_target_counts_as_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Read", "input": {"file_path": str(tmp_path / "a.md")}})
    assert fetched(ev, tmp_path, ("a.md",))


def test_prose_naming_a_target_is_not_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "text", "text": "I would read a.md"}, result="see a.md")
    assert not fetched(ev, tmp_path, ("a.md",))


def test_a_shell_command_naming_a_target_is_not_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Bash", "input": {"command": "echo a.md"}})
    assert not fetched(ev, tmp_path, ("a.md",))


def test_touched_records_the_tool_and_relative_path(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Read", "input": {"file_path": str(tmp_path / "a.md")}})
    assert touched(ev, tmp_path, ("a.md",)) == ["Read:a.md"]


def test_a_glob_listing_is_not_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Glob", "input": {"pattern": "*", "path": str(tmp_path / "a.md")}})
    assert not fetched(ev, tmp_path, ("a.md",))


def test_every_target_lies_under_a_route_the_pointer_names() -> None:
    for it in ITEMS:
        assert it.routes, f"{it.id}: no route"
        assert all(t.startswith(it.routes) for t in it.targets), f"{it.id}: a target outside its routes"


def test_a_read_of_a_different_file_is_not_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Read", "input": {"file_path": str(tmp_path / "b.md")}})
    assert not fetched(ev, tmp_path, ("a.md",))


def test_a_search_inside_a_target_directory_is_a_fetch(tmp_path: Path) -> None:
    ev = _stream({"type": "tool_use", "name": "Grep", "input": {"pattern": "x", "path": str(tmp_path / ".claude" / "skills")}})
    assert fetched(ev, tmp_path, (".claude/skills",))


def test_answer_is_the_result_event() -> None:
    assert answer(_stream(result="final")) == "final"


def test_boot_base_follows_at_imports_and_counts_bytes_on_disk(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n@sub/x.md\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("a" * 10, encoding="utf-8")
    (tmp_path / "sub").mkdir()
    body = "é" * 5 + "\n@../AGENTS.md\n"  # 5 chars = 10 B; the second import is a cycle-safe re-import
    (tmp_path / "sub" / "x.md").write_bytes(body.encode("utf-8"))
    home = tmp_path / "home"
    home.mkdir()
    sizes = boot_base(tmp_path, home)
    assert sizes["import AGENTS.md"] == 10
    assert sizes["import sub/x.md"] == len(body.encode("utf-8"))
    assert [p.name for p in import_closure(tmp_path / "CLAUDE.md")] == ["AGENTS.md", "x.md"]


def test_every_probe_is_well_formed() -> None:
    for it in ITEMS:
        held = [t for t in it.targets if (REPO / t).exists()]
        assert held, f"{it.id}: no declared target exists"
        text = "\n".join(p.read_text(encoding="utf-8") for t in held for p in ([REPO / t] if (REPO / t).is_file() else (REPO / t).rglob("*.md")))
        assert it.canary.lower() in text.lower(), f"{it.id}: canary is not held by its target"
        assert not any(t in it.task for t in it.targets), f"{it.id}: task names a target"
        assert it.canary.lower() not in it.task.lower(), f"{it.id}: task leaks the canary"
    assert "README" in CONTROL


def test_a_pointer_form_item_does_not_leak_its_canary_into_boot_text() -> None:
    claude = REPO / "CLAUDE.md"
    boot_text = "\n".join(p.read_text(encoding="utf-8") for p in [claude, *import_closure(claude)])
    for it in ITEMS:
        if not body_form(it, claude):
            assert it.canary.lower() not in boot_text.lower(), f"{it.id}: pointer form still carries the canary"


def test_every_pointer_form_item_is_admitted_by_recorded_evidence() -> None:
    claude = REPO / "CLAUDE.md"
    converted = [it.id for it in ITEMS if not body_form(it, claude)]
    assert converted, "nothing is pointer-form: the conversion the retrieval test gates has not happened"
    assert EVIDENCE.is_file(), "no recorded probe run: convert nothing without it"
    record = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert record["body_rev"] == BODY_REV
    assert all(r["fetched"] == bool(r["touched"]) for r in record["rows"]), "a fetched flag with no recorded tool call"
    by_id = {it.id: it for it in ITEMS}
    text = claude.read_text(encoding="utf-8")
    unrouted = [i for i in converted if not all(r in text for r in by_id[i].routes)]
    assert not unrouted, f"pointer form does not carry every probed route: {unrouted}"
    stale = [i for i in converted if record.get("pointer_text_sha256", {}).get(i) != pointer_sha(by_id[i], text)]
    assert not stale, f"pointer text changed since the recorded run -- re-run the probe: {stale}"
    refused = [i for i in converted if not admitted(record, by_id[i])]
    assert not refused, f"pointer-form without a demonstrated fetch: {refused}"


def test_repo_tracked_boot_base_is_under_its_ceiling() -> None:
    sizes = boot_base(REPO, home=REPO / "nonexistent-home")
    repo_bytes = sum(v for k, v in sizes.items()
                     if k in ("CLAUDE.md",) or k.startswith(("import ", "rules/")))
    assert repo_bytes <= REPO_BOOT_CEILING, f"{repo_bytes:,} B tracked boot base exceeds {REPO_BOOT_CEILING:,}"


def _record(item: Item, *, runs=(0, 1, 2), admit_at=2, witness=True) -> dict:
    body = [{"item": item.id, "arm": "body", "run": n, "fetched": True, "touched": [f"Read:{item.targets[0]}"],
             "canary": True, "canary_witness": f"..{item.canary}.."} for n in (0, 1, 2)]
    ptr = [{"item": item.id, "arm": "pointer", "run": n, "fetched": True, "touched": [f"Read:{item.targets[0]}"],
            "canary": True, "canary_witness": f"..{item.canary}.." if witness else ""} for n in runs]
    return {"admit_at": admit_at, "rows": [*body, *ptr]}


def test_admission_needs_the_constants_not_the_records_own_threshold() -> None:
    it = ITEMS[0]
    assert admitted(_record(it), it)
    assert not admitted(_record(it, runs=(0,), admit_at=0), it)  # one run, self-lowered threshold


def test_admission_counts_distinct_runs_not_duplicated_rows() -> None:
    it = ITEMS[0]
    assert not admitted(_record(it, runs=(0, 0, 0)), it)
    assert POINTER_RUNS >= 3


def test_a_canary_boolean_without_a_witness_admits_nothing() -> None:
    it = ITEMS[0]
    assert not admitted(_record(it, witness=False), it)


def test_an_answer_with_no_fetch_is_admitted_only_for_a_declared_preload_item() -> None:
    plain = next(i for i in ITEMS if not i.preload)
    exempt = next(i for i in ITEMS if i.preload)
    for it, want in ((plain, False), (exempt, True)):
        rec = _record(it)
        for r in rec["rows"]:
            if r["arm"] == "pointer":
                r["touched"] = []
        assert admitted(rec, it) is want, it.id


def test_a_preload_exemption_is_only_for_descriptions_the_harness_injects() -> None:
    for it in ITEMS:
        if not it.preload:
            continue
        texts = [(REPO / t).read_text(encoding="utf-8") for t in it.targets if (REPO / t).is_file()]
        heads = [x.split("---")[1] for x in texts if x.startswith("---")]
        assert any(it.canary.lower() in h.lower() for h in heads), f"{it.id}: canary not in a frontmatter description"


def test_a_pointer_run_that_neither_answered_nor_fetched_admits_nothing() -> None:
    it = ITEMS[0]
    rec = _record(it)
    for r in rec["rows"]:
        if r["arm"] == "pointer":
            r.update(touched=[], canary=False, canary_witness="")
    assert not admitted(rec, it)


def test_a_fetch_outside_the_declared_targets_does_not_count() -> None:
    it = ITEMS[0]
    rec = _record(it)
    for r in rec["rows"]:
        if r["arm"] == "pointer":
            r["touched"] = ["Read:README.md"]
    assert not admitted(rec, it)


def test_the_child_is_launched_with_a_source_that_loads_claude_md(monkeypatch, tmp_path: Path) -> None:
    import boot_retrieval as br

    seen: list[list[str]] = []

    class _P:
        stdout, stderr, returncode = json.dumps({"type": "result", "result": "ok"}), "", 0

    monkeypatch.setattr(br.shutil, "which", lambda _n: "claude")
    monkeypatch.setattr(br.subprocess, "run", lambda argv, **_k: seen.append(argv) or _P())
    br.run_probe(tmp_path, "t", "m")
    argv = seen[0]
    assert argv[argv.index("--setting-sources") + 1] == "project"  # `local` never loaded CLAUDE.md


def test_an_arm_that_never_loaded_its_boot_text_is_refused(monkeypatch, tmp_path: Path) -> None:
    import boot_retrieval as br

    monkeypatch.setattr(br, "run_probe", lambda *_a, **_k: _stream(result="I see no sentinel"))
    assert not br.boot_text_loaded(tmp_path, "m", "QUASAR-1")[0]
    monkeypatch.setattr(br, "run_probe", lambda *_a, **_k: _stream(result="it is QUASAR-1"))
    ok, seen = br.boot_text_loaded(tmp_path, "m", "QUASAR-1")
    assert ok and "QUASAR-1" in seen


def test_a_canary_is_held_only_by_its_own_targets_among_the_scratch_inputs() -> None:
    from boot_retrieval import scratch_files

    for it in ITEMS:
        for rel in scratch_files(REPO):
            if rel.startswith(tuple(it.targets)):  # declared target FILES only, never a whole routed directory
                continue
            text = (REPO / rel).read_text(encoding="utf-8", errors="ignore")
            if it.preload:  # only INJECTED text can satisfy a preload item: the frontmatter description
                text = text.split("---")[1] if text.startswith("---") else ""
            assert it.canary.lower() not in text.lower(), f"{it.id}: canary also held by {rel}"


def test_the_probe_prompt_does_not_prime_a_fetch_and_the_selftest_has_no_read_tools(monkeypatch, tmp_path: Path) -> None:
    import boot_retrieval as br

    calls: list[tuple[list[str], str]] = []

    class _P:
        stdout, stderr, returncode = json.dumps({"type": "result", "result": "ok"}), "", 0

    monkeypatch.setattr(br.shutil, "which", lambda _n: "claude")
    monkeypatch.setattr(br.subprocess, "run", lambda argv, **k: calls.append((argv, k["input"])) or _P())
    br.run_probe(tmp_path, "the task", "m")
    br.run_probe(tmp_path, "the task", "m", tools=False)
    (argv, prompt), (argv_no_tools, _) = calls
    assert "document" not in prompt.lower() and "repo" not in prompt.lower()  # the priming flaw, guarded
    assert "--allowedTools" in argv and "Read" not in argv[argv.index("--disallowedTools") + 1].split(",")
    assert "--allowedTools" not in argv_no_tools
    assert {"Read", "Grep", "Glob"} <= set(argv_no_tools[argv_no_tools.index("--disallowedTools") + 1].split(","))
