"""[#1525] RED-first: the bw-912 launch contract is consumed by a batch-manifest link.

The contract is undated, so the consumer_at_landing pool tokenizer cannot count a tasks/ or ADR
citation as consumption; the route is the batch-manifest link (`batch_manifest.manifest_links`).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import consumer_at_landing as cal  # noqa: E402

NAME = "LANE-bw-912-known-reds-expiry.md"


def test_bw912_contract_is_manifest_linked_not_unconsumed():
    m = cal.measure(ROOT)
    assert NAME in m.corpus
    assert m.manifest_linked.get(NAME) == "explicit"
    assert NAME not in m.unconsumed


def test_baseline_no_longer_carries_the_consumed_contract():
    baseline = cal.load_baseline(ROOT)
    assert baseline is not None
    assert NAME not in baseline["artifacts"]
    assert cal.ratchet_findings(cal.measure(ROOT), baseline) == []
