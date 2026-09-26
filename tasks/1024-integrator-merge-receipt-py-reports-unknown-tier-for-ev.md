---
id: "[#1024]"
title: "integrator: merge_receipt.py reports unknown-tier for every explicit model id"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1024] [P3][S] **integrator: merge_receipt.py reports unknown-tier for every explicit model id** - WAVE5B-N1 integrator FINDING: `scripts/merge_receipt.py` knows only family aliases, not explicit versioned ids (`claude-opus-5-5`, `claude-sonnet-5`, ...), so every lane this batch reads as unknown-tier; the integrator worked around it by reading `ran == ordered` from the transcript by hand. · Done when: `scripts/merge_receipt.py` resolves an explicit model id to its tier via `ecosystem/provider-registry.yaml`, RED-first witnessed on a fixture receipt naming an explicit id · refs `scripts/merge_receipt.py`, `ecosystem/provider-registry.yaml` · kill-candidates: none -- no open row tracks this gap
