---
id: "[#1585]"
title: "Provider census probes only providers that exist, and each probe answers or says why"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1585] [P3][S] **Provider census probes only providers that exist, and each probe answers or says why** - `grok -p --max-turns 1` cannot answer (2 turns works) and `-p` conflicts with `--prompt-file`; the ollama census row cannot connect; aider, llm and amp are ABSENT yet listed; agy 1.3.5 vs the contract's 1.2.2; a stray `'m' is not recognized` line on every claude launch via the cmd shim (`docs/audits/2026-10-15-technical-verified-harness-map.md:70-71,112,121,189`). `[#1327]` covers agy empty output · Done when: RED first: a test asserts the census omits ABSENT providers, reports ollama as `unreachable` with the reason, uses `--max-turns 2` for grok, and a claude launch via the shim prints no stray line; fails on 97bcd374 · touches: `scripts/provider_bench.py`, shim, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1327]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
