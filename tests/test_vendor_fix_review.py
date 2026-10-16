"""Codex terra review, round 1 (gpt-5.6-terra, 2026-10-16) of the PART V diff: four HIGH findings,
each pinned RED-first here. Companion to tests/test_vendor_fix.py."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import gen_lane_contract as glc  # noqa: E402
import provider_router  # noqa: E402
import read_gate as gate  # noqa: E402
import vendor_probe as vp  # noqa: E402

_IDEA = "title: A wholly unique idea\nproposes: zzz-nothing\nclass: decision\n"
_GOOD = [sys.executable, "-c",
         "import json,os;p=os.environ['PHASE_PAYLOAD'];"
         "json.dump({'nonce':os.environ['PHASE_NONCE'],'input_hash':os.environ['PHASE_INPUT_HASH'],"
         "'verdict':'AGREE','reasons':[],'amendments':[]},open(p,'w'))"]


def test_a_declared_vendor_with_no_argv_builder_is_a_vendor_fail_not_a_silent_skip(tmp_path: Path) -> None:
    receipt = glc.challenge(_IDEA, producer_vendor="anthropic", organ_index_text="",
                            reviewers=[("antigravity", None), ("xai", _GOOD)], work_dir=tmp_path,
                            timeout_s=30)
    assert "VENDOR-FAIL antigravity challenge no argv builder" in receipt.evidence


def test_default_reviewers_keep_a_declared_vendor_that_has_no_builder() -> None:
    names = [v for v, _ in glc._default_reviewers(lambda v: Path(v), "N", "H")]
    assert names == [e["provider"] for e in provider_router.declared_order("review")]


def test_a_cache_entry_for_another_vendor_or_model_is_a_miss(tmp_path: Path) -> None:
    (tmp_path / "xai.json").write_text(json.dumps(
        {"day": "2026-10-16", "model": "grok-4.5",
         "result": {"vendor": "other", "ok": True, "served": "grok-4.5", "error": ""}}), encoding="utf-8")
    calls: list[str] = []

    def probe(vendor: str) -> vp.ProbeResult:
        calls.append(vendor)
        return vp.ProbeResult(vendor, False, None, "fresh")

    got = vp.probe_today("xai", cache_dir=tmp_path, today="2026-10-16", probe=probe, model="grok-4.7")
    assert calls == ["xai"] and got.error == "fresh"


def test_an_unwritable_cache_dir_never_raises(tmp_path: Path) -> None:
    blocker = tmp_path / "file-not-dir"
    blocker.write_text("x", encoding="utf-8")
    got = vp.probe_today("xai", cache_dir=blocker, today="2026-10-16",
                         probe=lambda v: vp.ProbeResult(v, True, "grok-4.7", ""), model="grok-4.7")
    assert isinstance(got, vp.ProbeResult)


def test_a_raising_vendor_gate_is_recorded_as_a_vendor_fail(tmp_path: Path) -> None:
    def boom(vendor: str):
        raise OSError("disk gone")

    receipt = glc.challenge(_IDEA, producer_vendor="anthropic", organ_index_text="",
                            reviewers=[("openai", [sys.executable, "-c", "pass"])], work_dir=tmp_path,
                            timeout_s=30, vendor_gate=boom)
    assert any(e.startswith("VENDOR-FAIL openai challenge") and "disk gone" in e for e in receipt.evidence)


def test_a_source_named_like_the_output_file_cannot_collide_with_it(tmp_path: Path) -> None:
    source = tmp_path / "outside" / "copilot-enterprise.output.txt"
    source.parent.mkdir()
    source.write_text("the real source", encoding="utf-8")
    work = tmp_path / "work"
    work.mkdir()

    def runner(argv, **kw):
        return subprocess.CompletedProcess(argv, 0, "", "")

    gate.copilot_invoker(10, runner=runner)(gate.RouteSpec("copilot-enterprise"), source, work)
    assert source.read_text(encoding="utf-8") == "the real source"
    assert not (work / "copilot-enterprise.output.txt").exists(), "the output path must stay free"
    assert any(p.read_text(encoding="utf-8") == "the real source" for p in work.rglob("*") if p.is_file())
