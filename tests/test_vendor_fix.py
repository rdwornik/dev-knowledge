"""PART V of AMEND-1-BATCH-RESUME-NIGHT-2026-10-16: Copilot and Grok actually work, and a vendor
that fails is never silently replaced.

THE MATRIX (Copilot CLI 1.0.98, `-p` mode, one tiny read each, 2026-10-16, measured):
  base   --allow-all-tools --deny-tool shell, read OUTSIDE the cwd  -> "Permission denied because
         no interactive user response was available"  (path permission, not tool permission)
  (a)    --allow-all-tools --allow-all-paths, read outside          -> read
  (b)    COPILOT_ALLOW_ALL=true, read outside                       -> denied (a no-op on 1.0.98)
  (c)    file staged INSIDE the cwd, base flags                     -> read
  (d)    not run: (a) succeeded with this repo's own `.claude/settings.json` deny rules loaded,
         so they are not the cause.
ROOT CAUSE: `--allow-all-tools` grants TOOLS; a path outside the cwd needs a PATH grant, and in
`-p` mode nothing can ask. The fix that needs no wider grant is to stage the input inside the cwd.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import gen_lane_contract as glc  # noqa: E402
import read_gate as gate  # noqa: E402
import run_phase  # noqa: E402
import vendor_probe as vp  # noqa: E402


# --- Copilot: stage inside, never point at an outside path ----------------------------------


def test_stage_input_copies_the_file_inside_the_directory(tmp_path: Path) -> None:
    src = tmp_path / "drive" / "contract.md"
    src.parent.mkdir()
    src.write_text("hello", encoding="utf-8")
    inside = tmp_path / "wt"
    inside.mkdir()
    staged = run_phase.stage_input(src, inside)
    assert staged.parent == inside and staged.read_text(encoding="utf-8") == "hello"


def test_read_gate_copilot_reads_a_staged_copy_with_cwd_at_the_workdir(tmp_path: Path) -> None:
    source = tmp_path / "outside" / "src.txt"
    source.parent.mkdir()
    source.write_text("the sentence", encoding="utf-8")
    work = tmp_path / "work"
    work.mkdir()
    seen: dict = {}

    def runner(argv, **kw):
        seen["argv"], seen["kw"] = list(argv), kw
        return subprocess.CompletedProcess(argv, 0, "", "")

    gate.copilot_invoker(10, runner=runner)(gate.RouteSpec("copilot-enterprise"), source, work)
    prompt = seen["argv"][seen["argv"].index("-p") + 1]
    assert Path(seen["kw"]["cwd"]).resolve() == work.resolve()
    assert str(source.parent) not in prompt, "the prompt must not point Copilot outside its cwd"
    assert "--add-dir" not in seen["argv"] and "--allow-all-paths" not in seen["argv"]
    assert (work / "src.txt").read_text(encoding="utf-8") == "the sentence"


# --- Grok: always -m, from the registry, and the served id must equal it --------------------


def test_every_review_argv_for_grok_pins_the_registry_model() -> None:
    argv = glc.review_argv("xai", "PROMPT")
    assert argv[argv.index("-m") + 1] == "grok-4.7"
    assert "--max-turns" in argv


def test_served_model_mismatch_is_a_failure() -> None:
    assert vp.served_matches("grok-4.7", "grok-4.7")
    assert not vp.served_matches("grok-4.7", "grok-4.20-0309-non-reasoning")
    assert not vp.served_matches("grok-4.7", None)


# --- VENDOR-FAIL: loud, never a silent substitution ------------------------------------------


def test_vendor_fail_line_shape() -> None:
    assert vp.vendor_fail_line("xai", "challenge", "served grok-4.5") == \
        "VENDOR-FAIL xai challenge served grok-4.5"


def _idea() -> str:
    return "title: A wholly unique idea\nproposes: zzz-nothing\nclass: decision\n"


def test_challenge_records_vendor_fail_and_only_then_falls_back(tmp_path: Path, monkeypatch) -> None:
    """The first reviewer exits with no payload; the registry-named next one answers. The receipt
    must carry the VENDOR-FAIL of the first, so the substitution is visible."""
    monkeypatch.setattr(glc.shutil if hasattr(glc, "shutil") else __import__("shutil"), "which",
                        lambda name: name)
    good = [sys.executable, "-c",
            "import json,os,sys;"
            "p=os.environ['PHASE_PAYLOAD'];"
            "json.dump({'nonce':os.environ['PHASE_NONCE'],'input_hash':os.environ['PHASE_INPUT_HASH'],"
            "'verdict':'AGREE','reasons':['ok'],'amendments':[]},open(p,'w'))"]
    bad = [sys.executable, "-c", "import sys;sys.exit(3)"]
    receipt = glc.challenge(_idea(), producer_vendor="anthropic", organ_index_text="",
                            reviewers=[("openai", bad), ("xai", good)], work_dir=tmp_path,
                            timeout_s=30)
    assert receipt.reviewer_vendor == "xai"
    assert any(e.startswith("VENDOR-FAIL openai challenge") for e in receipt.evidence)


def test_challenge_with_every_vendor_failed_names_each_failure(tmp_path: Path) -> None:
    bad = [sys.executable, "-c", "import sys;sys.exit(3)"]
    receipt = glc.challenge(_idea(), producer_vendor="anthropic", organ_index_text="",
                            reviewers=[("openai", bad), ("xai", bad)], work_dir=tmp_path,
                            timeout_s=30)
    assert receipt.row_state == "INPUT_REQUIRED"
    assert sum(e.startswith("VENDOR-FAIL") for e in receipt.evidence) == 2


# --- the distiller routes only to vendors whose probe passed today ----------------------------


def test_probe_result_is_cached_per_day(tmp_path: Path) -> None:
    calls: list[str] = []

    def probe(vendor: str) -> vp.ProbeResult:
        calls.append(vendor)
        return vp.ProbeResult(vendor, True, "grok-4.7", "")

    first = vp.probe_today("xai", cache_dir=tmp_path, today="2026-10-16", probe=probe)
    again = vp.probe_today("xai", cache_dir=tmp_path, today="2026-10-16", probe=probe)
    next_day = vp.probe_today("xai", cache_dir=tmp_path, today="2026-10-17", probe=probe)
    assert first.ok and again.ok and next_day.ok
    assert calls == ["xai", "xai"], "second same-day call must come from the cache"


def test_challenge_skips_a_vendor_whose_probe_failed_today_and_says_so(tmp_path: Path) -> None:

    def gate_fn(vendor: str) -> vp.ProbeResult:
        return vp.ProbeResult(vendor, vendor != "openai", None, "" if vendor != "openai" else "denied")

    good = [sys.executable, "-c",
            "import json,os;p=os.environ['PHASE_PAYLOAD'];"
            "json.dump({'nonce':os.environ['PHASE_NONCE'],'input_hash':os.environ['PHASE_INPUT_HASH'],"
            "'verdict':'AGREE','reasons':[],'amendments':[]},open(p,'w'))"]
    receipt = glc.challenge(_idea(), producer_vendor="anthropic", organ_index_text="",
                            reviewers=[("openai", good), ("xai", good)], work_dir=tmp_path,
                            timeout_s=30, vendor_gate=gate_fn)
    assert receipt.reviewer_vendor == "xai"
    assert "VENDOR-FAIL openai challenge probe-failed-today: denied" in receipt.evidence


# --- live: a real `copilot -p` read of a staged file (skipped without the CLI or its sign-in) ---


@pytest.mark.skipif(__import__("shutil").which("copilot") is None, reason="copilot CLI absent")
def test_live_copilot_reads_a_staged_file(tmp_path: Path) -> None:
    if not (Path.home() / ".copilot").exists():
        pytest.skip("no copilot sign-in on this box")
    src = tmp_path / "outside" / "probe.txt"
    src.parent.mkdir()
    src.write_text("LIVE-STAGED-READ-OK\n", encoding="utf-8")
    work = tmp_path / "work"
    run_phase.stage_input(src, work)
    done = subprocess.run(
        [__import__("shutil").which("copilot"), "-p", "Read probe.txt in the current directory and "
         "reply with exactly its contents.", "--model", "claude-sonnet-5", "--allow-all-tools",
         "--no-ask-user", "--no-color"], cwd=work, capture_output=True, text=True, timeout=300,
        encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
    assert "LIVE-STAGED-READ-OK" in done.stdout, done.stdout[:300] + done.stderr[:300]
