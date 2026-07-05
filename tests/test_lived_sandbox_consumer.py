"""Layer-1 (hermetic, offline) tests for the CONSUMER measurement seam ([#252] Phase 0.5).

Frozen-ruling coverage: oracle = HUB manifest (never the consumer's); partial-mesh consumer
-> FAIL-by-coverage, not a crash; observe-as-is (no shaping flags); C1 (narration never
evidence); verbatim evidence quotes; CLI exit semantics 0/1/2.
"""
from __future__ import annotations

import contextlib
import itertools
import json
import sys
import types
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "deploy"))

from lived_sandbox import arc as arcmod  # noqa: E402
from lived_sandbox import cli  # noqa: E402
from lived_sandbox import consumer as con  # noqa: E402
from lived_sandbox import observe as obs  # noqa: E402
from lived_sandbox import oracle as orc  # noqa: E402
from lived_sandbox import spawn as sp  # noqa: E402

_MANIFEST_V120 = _REPO / "deploy" / "manifest-v1.2.0.yaml"

_SIX_SIGNATURES = [
    "pre-commit installed at", "sha256 sidecar", "canonical_freshness",
    "TOC freshness", "Session-end", "propose_closures:",
]

_UID = itertools.count(1)


def _tool_result(text: str) -> list[dict]:
    """A Bash-correlated tool_use/tool_result pair — the ONLY tool_result shape the
    tightened hook-stdout channel admits ([#253c] content-echo fix: results must be
    tool_use_id-correlated to a Bash invocation)."""
    uid = f"toolu_{next(_UID):04d}"
    return [
        {"type": "assistant", "message": {"role": "assistant",
         "content": [{"type": "tool_use", "id": uid, "name": "Bash",
                      "input": {"command": "git commit -m x"}}]}},
        {"type": "user", "message": {"role": "user",
         "content": [{"type": "tool_result", "tool_use_id": uid, "content": text}]}},
    ]


def _assistant_text(text: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "text", "text": text}]}}


def _tool_use(name: str, command: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "tool_use", "name": name, "input": {"command": command}}]}}


def _events(signatures: list[str], *, with_command: bool = True) -> list[dict]:
    evs = [ev for s in signatures for ev in _tool_result(f"hook fired: {s}....Passed")]
    if with_command:
        evs.append(_tool_use("SlashCommand", "/review-closures"))
    return evs


def _oracle() -> orc.Oracle:
    return orc.load_oracle(_MANIFEST_V120)


def _report(events: list[dict], *, gate_ok: bool = True) -> con.ConsumerReport:
    o = _oracle()
    gate = arcmod.GateZero(gate_ok, gate_ok, gate_ok)
    return con.build_report("X:/consumer", gate, obs.observe(events, o), o, events)


# --- coverage verdicts -------------------------------------------------------------------


def test_full_coverage_consumer_is_full():
    r = _report(_events(_SIX_SIGNATURES))
    assert (r.coverage_fired, r.coverage_total) == (6, 6)
    assert r.tombstones_ok and r.full_coverage
    assert "VERDICT: FULL-COVERAGE" in r.summary()


def test_partial_mesh_consumer_fails_by_coverage_not_crash():
    """THE frozen-ruling case: a partial-mesh consumer measures as FAIL-by-coverage."""
    r = _report(_events(["canonical_freshness", "pre-commit installed at"]))
    assert (r.coverage_fired, r.coverage_total) == (2, 6)
    assert not r.full_coverage
    assert "FAIL-by-coverage" in r.summary()
    assert "2-of-6 enforcing" in r.summary()
    silent = {f.component_id for f in r.observation.silences}
    assert len(silent) == 4  # the four un-fired gated-active hooks are named SILENT


def test_tombstone_regression_blocks_full_coverage():
    evs = _events(_SIX_SIGNATURES) + _tool_result("Ruff linter....Passed")
    r = _report(evs)
    assert r.coverage_fired == 6 and not r.tombstones_ok and not r.full_coverage
    assert "tombstones REGRESSED" in r.summary()


def test_gate_fail_report_still_builds():
    r = _report(_events(_SIX_SIGNATURES), gate_ok=False)
    assert not r.gate.passed and r.coverage_fired == 6  # measurement survives; caller labels it


def test_armed_skipped_counted_distinctly_never_as_fired_g4a():
    """G4a (measurement-#2 root ruling): a file-scoped hook pre-commit consulted but Skipped
    counts as covered (it enforces for its scope) yet is REPORTED separately — the FIRED
    figure stays uninflated."""
    evs = _events(["canonical_freshness", "pre-commit installed at",
                   "Session-end", "propose_closures:"])
    evs += _tool_result(
        "protocols TOC freshness check....................(no files to check)Skipped")
    evs += _tool_result(
        "Verify CLAUDE-FLOOR.md matches its sha256 sidecar....(no files to check)Skipped")
    r = _report(evs)
    assert (r.coverage_fired, r.coverage_armed_skipped) == (4, 2)
    assert r.full_coverage
    assert "4-of-6 enforcing on this consumer + 2 armed-but-skipped" in r.summary()


def test_vacuous_tombstone_never_reads_as_ok_g4b():
    """G4b: when no commit was attempted (the measurement-#2 shape), the tombstone is
    VACUOUS — not silently 'ok' — and full coverage is off the table."""
    evs = _tool_result("pre-commit installed at .git/hooks/pre-commit")
    r = _report(evs)
    assert r.tombstone_state == "VACUOUS" and not r.tombstones_ok and not r.full_coverage
    assert "tombstones VACUOUS" in r.summary()


# --- evidence quotes (C1 + masking) ------------------------------------------------------


def test_evidence_lines_are_verbatim_hook_stdout():
    r = _report(_events(["canonical_freshness"]))
    (lines,) = (v for k, v in r.evidence.items() if k == "canonical-freshness")
    assert lines == ("hook fired: canonical_freshness....Passed",)
    assert "| hook fired: canonical_freshness....Passed" in r.summary()


def test_narration_never_produces_evidence_C1():
    evs = [_assistant_text("canonical_freshness fired, floor-hash-verify OK, all good!")]
    r = _report(evs)
    assert r.coverage_fired == 0 and not r.evidence


def test_evidence_masks_a_key_shaped_token():
    evs = _tool_result("canonical_freshness saw sk-ant-abcdefgh12345678 in env")
    lines = con.evidence_lines(evs, _oracle())
    assert all("sk-ant-abcdefgh" not in ln for ls in lines.values() for ln in ls)
    assert any("MASKED" in ln for ls in lines.values() for ln in ls)


# --- run_consumer_arc: hub oracle, consumer without a manifest ---------------------------


def test_run_consumer_arc_uses_hub_oracle_never_consumer_manifest(tmp_path, monkeypatch):
    """The consumer clone carries NO manifest — the oracle must come from the hub root."""
    consumer_repo = tmp_path / "consumer"
    consumer_repo.mkdir()
    clone_dir = tmp_path / "clone"
    clone_dir.mkdir()

    @contextlib.contextmanager
    def fake_clone(source, prefix="x"):
        assert Path(source) == consumer_repo.resolve()
        yield clone_dir, {}

    def fake_spawn(work_dir, prompt, *, config_dir, api_key, model="sonnet",
                   extra_env=None, timeout=0):
        assert Path(work_dir) == clone_dir  # the arc runs INSIDE the clone, never the source
        stdout = arcmod.PROVENANCE_MARKER + "\nhook fired: canonical_freshness....Passed"
        return sp.SpawnResult(exit_code=0, stdout=stdout,
                              events=_events(["canonical_freshness"], with_command=False),
                              transcript_path=None, config_dir=tmp_path / "cfg",
                              work_dir=clone_dir)

    monkeypatch.setattr(sp, "sandbox_clone", fake_clone)
    monkeypatch.setattr(sp, "spawn", fake_spawn)
    report = con.run_consumer_arc(consumer_repo, hub_root=_REPO, api_key="k")
    assert report.oracle_version == "1.2.0"          # hub manifest, not a consumer file
    assert report.gate.passed
    assert (report.coverage_fired, report.coverage_total) == (1, 6)
    assert not report.full_coverage


def test_consumer_declares_plugin_exact_json_check(tmp_path):
    """Codex HIGH 2026-07-06: plugin seeding is GATED on the consumer's OWN enablement
    declaration — exact JSON key, never a substring, absent/malformed settings -> False."""
    clone = tmp_path / "clone"
    assert con.consumer_declares_plugin(clone) is False           # no settings at all
    (clone / ".claude").mkdir(parents=True)
    settings = clone / ".claude" / "settings.json"
    settings.write_text("{not json", encoding="utf-8")
    assert con.consumer_declares_plugin(clone) is False           # malformed -> never seed
    settings.write_text(json.dumps(
        {"enabledPlugins": {"some-other-plugin@elsewhere": True}}), encoding="utf-8")
    assert con.consumer_declares_plugin(clone) is False           # different plugin
    settings.write_text(json.dumps(
        {"enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True}}),
        encoding="utf-8")
    assert con.consumer_declares_plugin(clone) is True


def test_plugin_seeding_gated_on_consumer_declaration_codex_high(tmp_path, monkeypatch):
    """A consumer that never deployed the enablement gets NO seed (its silence is the honest
    not-deployed reading); a declaring consumer is seeded from the hub checkout."""
    consumer_repo = tmp_path / "consumer"
    consumer_repo.mkdir()
    clone_dir = tmp_path / "clone"
    clone_dir.mkdir()
    seeded = []

    @contextlib.contextmanager
    def fake_clone(source, prefix="x"):
        yield clone_dir, {}

    def fake_spawn(work_dir, prompt, *, config_dir, api_key, model="sonnet",
                   extra_env=None, timeout=0):
        return sp.SpawnResult(exit_code=0, stdout=arcmod.PROVENANCE_MARKER, events=[],
                              transcript_path=None, config_dir=Path(config_dir),
                              work_dir=clone_dir)

    monkeypatch.setattr(sp, "sandbox_clone", fake_clone)
    monkeypatch.setattr(sp, "spawn", fake_spawn)
    monkeypatch.setattr(arcmod, "seed_tier1_plugin",
                        lambda cfg, clone, source_root=None: seeded.append(source_root))
    con.run_consumer_arc(consumer_repo, hub_root=_REPO, api_key="k")
    assert seeded == []                                           # no declaration -> no seed
    (clone_dir / ".claude").mkdir()
    (clone_dir / ".claude" / "settings.json").write_text(json.dumps(
        {"enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True}}),
        encoding="utf-8")
    con.run_consumer_arc(consumer_repo, hub_root=_REPO, api_key="k")
    assert seeded == [_REPO]                                      # declared -> hub-sourced seed


def _git_repo_with_commit(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for args in (["init", "-q"], ["config", "user.email", "t@e.st"],
                 ["config", "user.name", "T"], ["config", "commit.gpgsign", "false"]):
        obs._git(root, *args)
    (root / "x.txt").write_text("x\n", encoding="utf-8")
    obs._git(root, "add", "-A")
    obs._git(root, "commit", "-q", "-m", "seed")
    return root


def test_mirror_relative_precommit_source_g7(tmp_path):
    """G7 (STEP-3 witnessed): a consumer pinning a pre-commit source by RELATIVE path
    (ai-council's `repo: ../.dev-knowledge`) breaks beside a temp-dir clone — the mirror
    materializes the real machine's target at the same relative position, inside the
    sandbox temp root, without touching the clone."""
    real_hub = _git_repo_with_commit(tmp_path / "real" / "hubX")
    real_consumer = tmp_path / "real" / "consumer"
    real_consumer.mkdir(parents=True)
    sandbox = tmp_path / "sandbox"
    clone = sandbox / "clone"
    clone.mkdir(parents=True)
    (clone / ".pre-commit-config.yaml").write_text(
        "repos:\n- repo: ../hubX\n  rev: v1\n  hooks: []\n"
        "- repo: local\n  hooks: []\n", encoding="utf-8")
    before = (clone / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    notes = con.mirror_relative_precommit_sources(real_consumer, clone)
    assert any("mirrored '../hubX'" in n for n in notes)
    assert (sandbox / "hubX" / ".git").exists()          # operator-layout position
    assert (sandbox / "hubX" / "x.txt").exists()
    assert (clone / ".pre-commit-config.yaml").read_text(encoding="utf-8") == before
    assert real_hub.exists()                             # source untouched
    notes2 = con.mirror_relative_precommit_sources(real_consumer, clone)
    assert any("already present" in n for n in notes2)   # idempotent


def test_mirror_refuses_temp_root_escape_g7(tmp_path):
    """Blast-radius: a relative source resolving OUTSIDE the sandbox temp root is skipped
    and noted — the mirror never writes beyond the teardown boundary."""
    real_consumer = tmp_path / "real" / "consumer"
    real_consumer.mkdir(parents=True)
    clone = tmp_path / "sandbox" / "clone"
    clone.mkdir(parents=True)
    (clone / ".pre-commit-config.yaml").write_text(
        "repos:\n- repo: ../../evil\n  hooks: []\n", encoding="utf-8")
    notes = con.mirror_relative_precommit_sources(real_consumer, clone)
    assert any("escapes the sandbox temp root" in n for n in notes)
    assert not (tmp_path / "evil").exists()


def test_mirror_skips_nongit_source_and_urls_g7(tmp_path):
    """A missing/non-git real-machine target is a NOTED consumer-environment finding, not a
    crash; URL / local / meta entries are never touched."""
    real_consumer = tmp_path / "real" / "consumer"
    real_consumer.mkdir(parents=True)
    clone = tmp_path / "sandbox" / "clone"
    clone.mkdir(parents=True)
    (clone / ".pre-commit-config.yaml").write_text(
        "repos:\n- repo: ../ghost\n  hooks: []\n"
        "- repo: https://github.com/x/y\n  rev: v1\n  hooks: []\n", encoding="utf-8")
    notes = con.mirror_relative_precommit_sources(real_consumer, clone)
    assert any("not a git repo on the real machine" in n for n in notes)
    assert len(notes) == 1                               # the URL entry produced no note
    assert not (tmp_path / "sandbox" / "ghost").exists()


def test_run_consumer_arc_seeds_arc_allowlist_g1(tmp_path, monkeypatch):
    """G1 (measurement-#2 root ruling): the consumer child's HARNESS-OWNED user-level config
    carries the scoped #253a allowlist — the untrusted sandbox workspace IGNORES the clone's
    own settings.local.json allows (witnessed verbatim at measurement #2), so user-level is
    the only place a headless child honors them. Never a bypass. Timeout matches the hub arc
    path (600s Stop-block thrash witnessed at Step 7)."""
    consumer_repo = tmp_path / "consumer"
    consumer_repo.mkdir()
    clone_dir = tmp_path / "clone"
    clone_dir.mkdir()
    seen = {}

    @contextlib.contextmanager
    def fake_clone(source, prefix="x"):
        yield clone_dir, {}

    def fake_spawn(work_dir, prompt, *, config_dir, api_key, model="sonnet",
                   extra_env=None, timeout=0):
        seen["config_dir"] = Path(config_dir)
        seen["timeout"] = timeout
        return sp.SpawnResult(exit_code=0, stdout=arcmod.PROVENANCE_MARKER, events=[],
                              transcript_path=None, config_dir=Path(config_dir),
                              work_dir=clone_dir)

    monkeypatch.setattr(sp, "sandbox_clone", fake_clone)
    monkeypatch.setattr(sp, "spawn", fake_spawn)
    con.run_consumer_arc(consumer_repo, hub_root=_REPO, api_key="k")
    raw = (seen["config_dir"] / "settings.json").read_text(encoding="utf-8")
    assert json.loads(raw)["permissions"]["allow"] == list(arcmod.ARC_ALLOW_RULES)
    assert "bypassPermissions" not in raw and "defaultMode" not in raw
    assert seen["timeout"] == 1200


# --- CLI seam ----------------------------------------------------------------------------


class _FakeReport:
    def __init__(self, *, gate_ok: bool, full: bool):
        self.gate = types.SimpleNamespace(passed=gate_ok)
        self.full_coverage = full

    def summary(self) -> str:
        return "fake consumer report"


def _run_cli(monkeypatch, argv, *, gate_ok=True, full=False):
    monkeypatch.setattr(con, "run_consumer_arc",
                        lambda c, model: _FakeReport(gate_ok=gate_ok, full=full))
    return cli.main(argv)


def test_cli_consumer_full_coverage_exit_0(monkeypatch, capsys):
    assert _run_cli(monkeypatch, ["observe-arc", "--consumer", "X:/c"], full=True) == 0
    assert "fake consumer report" in capsys.readouterr().out


def test_cli_consumer_partial_coverage_exit_2(monkeypatch):
    assert _run_cli(monkeypatch, ["observe-arc", "--consumer", "X:/c"], full=False) == 2


def test_cli_consumer_gate_fail_exit_1_report_printed(monkeypatch, capsys):
    assert _run_cli(monkeypatch, ["observe-arc", "--consumer", "X:/c"], gate_ok=False) == 1
    captured = capsys.readouterr()
    assert "fake consumer report" in captured.out       # measurement still printed
    assert "NOT trusted" in captured.err


def test_cli_consumer_sandbox_error_is_concise_exit_1(monkeypatch, capsys):
    """Codex HIGH 2026-07-05: expected live failures never escape as tracebacks."""
    def boom(c, model):
        raise sp.SandboxError("clone failed: not a git repo")
    monkeypatch.setattr(con, "run_consumer_arc", boom)
    assert cli.main(["observe-arc", "--consumer", "X:/c"]) == 1
    err = capsys.readouterr().err
    assert "consumer measurement could not run" in err and "not a git repo" in err


def test_cli_consumer_oracle_error_is_concise_exit_1(monkeypatch, capsys):
    def boom(c, model):
        raise orc.OracleError("manifest not found")
    monkeypatch.setattr(con, "run_consumer_arc", boom)
    assert cli.main(["observe-arc", "--consumer", "X:/c"]) == 1
    assert "manifest not found" in capsys.readouterr().err


def test_cli_consumer_requires_a_value(capsys):
    assert cli.main(["observe-arc", "--consumer"]) == 2
    assert "requires a <repo-path>" in capsys.readouterr().err


def test_cli_consumer_refuses_freeze_and_leg_e(capsys):
    assert cli.main(["observe-arc", "--consumer", "X:/c", "--freeze"]) == 2
    assert cli.main(["observe-arc", "--consumer", "X:/c", "--leg-e"]) == 2
    assert "observe-as-is" in capsys.readouterr().err
