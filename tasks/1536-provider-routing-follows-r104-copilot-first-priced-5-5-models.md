---
id: "[#1536]"
title: "Provider routing follows R104: implement Copilot first, red/qa/judge roles, priced 5-5 models, one source for model ids"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1536] [P1][M] **Provider routing follows R104: implement Copilot first, red/qa/judge roles, priced 5-5 models, one source for model ids** - R104 (RATIFICATION-2026-10-14 v3) sets implement = Copilot -> Sonnet 5.5 -> Grok and review = Codex terra -> Grok -> Copilot (non-Anthropic); `ecosystem/provider-registry.yaml:660-717` still orders implement Sonnet-first (claude-sonnet-5), there is no `red`, `qa` or `judge` role, the claude-*-5-5 models carry no `rates:` (so `lane_cost` cannot price them), and model ids are typed in several places. `read` is already agy -> Copilot -> Sonnet (:776-804) and `scripts/read_gate.py:375-381` already passes agy's `--dangerously-skip-permissions` (R113), so no new read route is built; every agy read declares its workspace (`docs/audits/2026-09-05-technical-627-readjudication.md:658-664`) · Done when: RED first: (1) `uv run --locked python scripts/provider_router.py route implement` prints copilot-enterprise first, then claude-sonnet-5-5, then grok; review prints codex (gpt-5.6-terra) -> grok (`--max-turns` >= 2) -> copilot with a non-Anthropic model; (2) roles `red`, `qa`, `judge` exist in `roles:`; (3) `lane_cost` prints USD above 0 for a claude-sonnet-5-5 lane; (4) `dispatch_surface` accepts the full model ids; (5) a test fails on a planted model-id literal outside the registry; (6) a test pins that the documented agy read entry point is `read_gate` with an absolute path or `--add-dir`, and refuses an ad-hoc `agy -p` without one · touches: `ecosystem/provider-registry.yaml`, `scripts/provider_router.py`, `scripts/lane_cost.py`, `scripts/dispatch_surface.py`, `scripts/read_gate.py`, tests · kill-candidates: `[#1452]` -- its role pins to claude-sonnet-5-5 are a subset of (1)-(5); related `[#988]`, `[#989]`, `[#990]`, `[#691]` · refs `docs/intake/2026-10-15-tech-build1-owed-rows.md`, `to-browser/DIGEST-BUILD1-CHALLENGE-M2-R113-2026-10-15.md` · source: `to-cc/BATCH-BUILD1-PREP-2026-10-15.md` L2 and its AMEND v5 L2
