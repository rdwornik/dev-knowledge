---
intake-id: 27
status: DRAFT
origin: "2026-08-06 operator-directed retrospective + tech-adoption audit, browser seat of the sealed 2026-08-05/06 window; consolidates and SUPERSEDES-as-ledger the adoption-status view of intake #24 (tech-currency wave 1) and intake #25 (simplification & distribution wave); landed verbatim by operator instruction"
note: "Parents: intake #24 · intake #25 · ADR (parallel-execution way-of-working, successor Phase 2). Landed VERBATIM by operator instruction (ARC-2 S-batch contract 1) — body unedited. The source frontmatter carried an off-schema `parents:` key (README §3 schema); its value is preserved here as prose rather than dropped."
---

# INTAKE DRAFT — tech-adoption consolidation ledger (36 items, successor-facing)

## WHY — what this intake is and is not

The fleet decides fast and executes through one serial channel; ~21 of the 36 tracked adoption items are IN-FLIGHT behind that channel. This intake is the **single durable ledger** of all 36 so the vision cannot be lost between windows — every item has a status, an owner-or-gap, and a recommended priority class. It is **not** a new proposal wave: it births at most the four §D eval rows; everything else already has a home and this document only makes the queue visible and sequenceable. Rulings referenced here are settled — this intake carries them, it does not reopen them.

## §A — Ledger (status vocabulary: ADOPTED-live / EVAL-RUN(result) / SCHEDULED(where) / UNPLACED / REFUTED / DEFERRED(trigger) / DORMANT)

| # | Item | Status | Evidence / locator | Priority class (§C) |
|---|---|---|---|---|
| 1 | Gemini CLI lane [#491] | SCHEDULED(batch-2 grooming) | supplement C3(a) | P-A |
| 2 | Grok lane [#492] | SCHEDULED(peg ≥2026-08-07; seeded-defect list unwritten) | supplement C3(b) | P-A |
| 3 | Copilot Free as Grok channel | DEFERRED(opens with #2) | intake #24 P6 | P-A |
| 4 | sol/terra/luna routing table | ADOPTED-live | R-6 ruling; terra owed on [#504] | — |
| 5 | Actions report-only recorder [#501] | SCHEDULED(batch 1) | row e7c0b70e; YAML in night packs c55c7e51 | P-A |
| 6 | Scheduled runs + dead-man ([#493], P2 folded) | DEFERRED(no date) — B-2 still silent | FR-3 fold ruling | P-C |
| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | night finding 5 (rate limits, ~150→403) | P-C |
| 8 | mutmut [#502] | EVAL-RUN(pass) + SCHEDULED(behind [#501], CI-only) | night research; B2→B1 dependency edge | P-A |
| 9 | CONTRIBUTING currency [#503] | SCHEDULED(batch 1, ×6 claims + DoD + override.md) | Lane D + night finding 7 | P-A |
| 10 | vale (P6) | REFUTED | commit 5125dd6 + JOURNAL (b) 616f4814 | — |
| 11 | commitlint / gitlint (P6) | EVAL-RUN(LEAVE) | night packs 81cf13b | — |
| 12 | lychee (P6) | EVAL-RUN(ADOPT-candidate, --include-fragments) | night packs 81cf13b | P-B |
| 13 | copier living-template (W-1) | DEFERRED(batch 2 W-wave) | R-i pre-naming | P-A |
| 14 | kernel/lab check tiering (W-2) | DEFERRED(batch 2; pyproject collision recorded) | Lane C ledger | P-A |
| 15 | pre-commit native distribution (W-3) | DEFERRED(batch 2; reconcile [#497] @ carrier_mesh.py:75 FIRST) | mega-packet collision | P-A |
| 16 | reusable kernel.yml (W-4) | DEFERRED(batch 2; .github/workflows/ single-owner = [#501]) | Lane C ledger | P-A |
| 17 | pytest-testmon (W-5) | SCHEDULED(batch-2 ledger per rider R-ii; targets 410s/run) | supplement rider R-ii | P-A |
| 18 | schema-as-code (W-6) | DEFERRED(floats behind W-5) — reshaped by §D item 35 | rider R-ii | P-B |
| 19 | sphinx-needs study (W-7) | UNPLACED | intake #25 heading only | P-D |
| 20 | local-vs-reference matrix (W-8) | UNPLACED(intake prose) — candidate for a one-line register ruling | intake #25 W-8 | P-B |
| 21 | AGENTS.md + thin shim (W-9a) | DEFERRED(batch 2) + HAZARD: collides with existing codex/AGENTS.md | mega-packet hazard | P-A |
| 22 | VISION→README (W-9b) | UNPLACED (S, gap-week) | — | P-B |
| 23 | .claude/skills ↔ .agents/skills symlink (W-9d) | UNPLACED (S, gap-week) | — | P-B |
| 24 | routing-table-as-config (W-10) | DEFERRED(batch 2) | intake #25 | P-A |
| 25 | standing-rulings register (V-2) | ADOPTED-live (applied silently; 4 lessons + B2 label land in successor Phase 2) | protocols/STANDING_RULINGS.md, 90351bd0 | — |
| 26 | risk-tiered ceremony + plan-mode-by-exception (V-3) | ADOPTED-live | templates/prompt-template.md v1.6, 12dbb65a; precedence repair adf85c4a | — |
| 27 | first V-1 worktree batch | GO-GIVEN, runs as successor Phase 4 | predecessor approve + plan §2 | P-A |
| 28 | worktree hygiene prune (V-5) | SCHEDULED(mechanized in [#429] slim, successor Phase 3) | plan §2 P3 | P-A |
| 29 | seal velocity metrics (V-6) | PARTIAL(qualitative only; hard numbers = batch-1 packet) | retro RS-3 | P-A |
| 30 | [#408] three-layer sync spec | DESIGN-LANDED(c55c7e51, fingerprint trigger); build = OWN ARC, unplaced | row pointer per rider R-iii | P-C |
| 31 | Fibonacci estimate binding | UNPLACED ([#488] scope; backlog still has no ranking function) | audit row 31 | P-D |
| 32 | R1–R4 retirement ranking | DORMANT since [#487] engine refutation | 2026-08-06 grooming used live-peg evidence instead | P-D |
| 33 | **pytest-xdist** (`-n auto`) | NEW EVAL candidate — immediate 410s relief, orthogonal to W-5 | operator pain (410s); suite 2362 tests | P-B |
| 34 | **jsonc-parser (Microsoft)** as merge engine | NEW EVAL candidate — replaces hand-rolled JsoncMerge.ps1 (196 lines) | 2 latent bugs bit in one week (win-tooling lane) | P-B |
| 35 | **check-jsonschema** (pre-commit hook) | NEW EVAL candidate — reshapes W-6 from build to adopt | W-6 stalled as a build | P-B |
| 36 | **mise** (per-repo toolchain pinning) | NEW EVAL candidate — durable fix for the uv-pin class | 3 organs silent from one cause; night fix ephemeral by design | P-B |

## §B — Do-not-relitigate carried (from #24, #25, and the sealed window)

vale-as-ratchet (refuted with citation) · commitlint/gitlint (LEAVE) · hand-rolled batch orchestration (native /batch exists) · web-UI-outside-VS-Code as primary surface · tmux/WSL · Copilot-gated Agents window · Backlog.md-as-engine (pattern donor only) · public repos for CI minutes · P2 as its own row (folded into [#493]) · name-match closes · equalizing work-lane vs epic-lane ceilings · agent-orchestration frameworks (LangGraph/CrewAI class — wrong layer) · standalone worktree managers (native + hygiene organ cover) · external SaaS dead-man services.

## §C — Priority classes (recommendation to the receiving architect; operator ratifies)

- **P-A — the batch-2 unlock class (~14 items):** everything queued behind the wide batch. No per-item decisions needed; the decision is *run batch 2 with [#490] inside* (retro RS-7). Items 13–16/21/24 additionally need the recorded collision reconciliations BEFORE births.
- **P-B — gap-week S-evals (~9 items):** cheap, independent, one sitting each (12, 18, 20, 22, 23, 33–36). Recommended standing rule: every gap-week consumes ≥1 P-B item; measured-divergence bar applies — an eval that says NO (like vale) is a full success.
- **P-C — own arcs (3):** [#493] dead-man (B-2 is still silent — the oldest unwatched failure mode in the fleet), [#408] build (design landed, do not let it rot), P3-reshaped Issues loop. Sequence after batch 2 proves the channel.
- **P-D — dormant, deliberate (4):** W-7, Fibonacci/[#488], R1–R4. Re-enter only via a named trigger, not ambition.

## §F — capacity honesty

This intake births **at most 4 rows** (items 33–36, and only if the receiving architect prefers rows over a standing gap-week rule; a register one-liner "gap-weeks consume P-B evals" would birth ZERO). Everything else is already owned. The close engine question does not arise — this is a ledger, not a wave.

## Sequencing note (not binding)

Batch 1 (P4) → batch 2 wide with [#490] (P-A unlock) → P-B evals fill gap-weeks throughout → P-C arcs after the channel is proven. The single risk this intake exists to prevent: the 36-item vision fragmenting back into chat memory. Its counter-mechanism is this file itself — versioned, statused, and small enough to re-read at every window boot.
