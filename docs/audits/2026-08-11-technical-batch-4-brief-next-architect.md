# BRIEF FOR THE INCOMING ARCHITECT — operator strategy consolidation · 2026-08-11 (seat 27, end of window)

The operator dictated a strategy dump at the close of the 2026-08-10/11 window. This brief consolidates it, maps every theme to what ALREADY exists (half of these have owners — the map is the point; double-birthing is the named failure), names the three genuine gaps, and proposes an order. Rulings quoted are from STANDING_RULINGS §I unless noted.

## 1 · The map — operator theme → current owner → route

- **"Architecture isn't updated enough; needs a hook like JOURNAL's"** → partially owned: the 16-claim fix landed (`cf039756`), soft-observations scope ruled (G-7 = STEP-3 list + I-D2), re-stamp semantics established (stamp = what was actually re-read). The HOOK itself (freshness enforcement on architecture claims at commit time) is **GAP-1** below.
- **"Backlog is huge; split it; docs taxonomy (intakes→ADRs→backlog→audits) plus the archive folder's unclear role"** → the census corrected the numbers (72 convertible, 8 DEFECTIVE, kill-flags list exists); the FOLDER restructure is **GAP-2** — intake territory, not a chat decision (zero-invented-paths + ADR-98).
- **"What is JOURNAL for, given git log + CC chat? Handoffs forget it"** → session-continuity is OWNED: it attaches to `[#511]` (ruled this window, register line I-D…); the re-scoped `[#511]` covers exactly the non-mechanized handoff load. Feed this observation there as evidence — do not re-derive.
- **"Night routines — use them more"** → proven pattern (two night batches ran); constraints documented: shallow-clone false positives, uv-pin gate silence (5th witness recorded), read-only + PARTIAL protocol. Scale it, but the toolchain-attestation question is owned by intake #32/#30 §B territory.
- **"Gemini for repo-wide scanning (I have the subscription)"** → OWNED with a gate: `[#491]` is the Gemini leg; the routing doctrine says fan-out = RETRIEVAL ONLY (a fan-out lane once fabricated a count); admission runs through the seeded-defect corpus (v0.1 verified: 9 SEEDABLE / 1 cond / 1 REWORK / 1 gate-blocked) — never vibes.
- **"Grok replaces Codex ($20 saved, cheaper API)"** → the ROUTING TABLE is the operator's to edit — legitimate. But the doctrine he ratified is admit-then-retire: `[#492]` (Grok, re-check 2026-08-17) measures against the incumbent baseline on the corpus FIRST; Codex sunsets after Grok passes, not before. Retire-then-hope re-creates the unmeasured-lane problem the corpus exists to end.
- **"Copilot free tier unused"** → owned as the third corpus-gated probe channel (50 premium req/mo, named this window).
- **"We're building a Cursor-like harness; consolidate methodology BEFORE deploying it elsewhere"** → this is the operator's own priority sentence. It ratifies the order in §3: consolidation intake before any expansion.
- **"Universal agents file / per-LLM config folder (CLAUDE.md, codex/ with one file, AGENTS.md…)"** → **GAP-3**; adjacent to the multi-provider portability scope note already landed at W-9(a) — extend that, don't fork it.
- **"Orchestration workflows: sonnet/haiku armies feeding opus"** → OWNED: `[#412]` (fan-out/workflow/subagent axis — the distiller search verdict was PARTIALLY, every axis has an owner). Claude Code native custom agents (model+effort frontmatter) + auto-triggering skills are the library-first primitive to measure before building anything.
- **"Token efficiency"** → measure first (#29 is the measurement intake); optimizing unmeasured spend violates the operator's own no-budget-ceiling + measure-first stances.
- **"Monorepo tendency"** → parked BY the operator's own consolidation-first sentence; portability note W-9(a) is where it lives until then.
- **"GitHub/library search — use the world's existing code"** → this IS the library-first standing stance (stdlib > dependency > stabilized project > pattern); the enforcement moment is in every contract's library-first line. If it needs teeth, that is a one-line lane-contract template addition, not a new system.

## 2 · The three genuine gaps (nothing below has an owner)

- **GAP-1 — Architecture-freshness mechanism:** a check (not prose) that flags commits touching architecture-described surfaces without an ARCHITECTURE delta or an explicit no-impact note. Candidate: extend `validate_doc_claims`/doc-counts machinery rather than a new organ. Needs an intake or attaches to the re-read arc's successor.
- **GAP-2 — Docs taxonomy restructure:** backlog-as-folder placement, archive-folder role, the intake→ADR→backlog→audit chain made navigable. One intake, one ADR-sized decision, executed as doc-moves with redirects. Ceiling has room (3/6 DRAFT).
- **GAP-3 — Per-provider config unification:** one folder convention for CLAUDE.md-class files across providers (Claude/Codex/Grok/Gemini), byte-identical carriers where content is shared. Extends W-9(a).

Recommended packaging: **ONE consolidation intake** covering GAP-1+2+3 as sections (they are one theme: the repo's self-description), respecting the five/six ceiling.

## 3 · Proposed order (the operator decides; this is the recommendation)

1. **Finish batch-4's remnant** — W3 (`[#513]` organ), W4-after-id (conversion campaign row), `[#522]`; they attack the finish line (§B) directly.
2. **The consolidation intake (GAP-1/2/3)** — drafted, ratified at the next GO; executed as its own batch. This is the operator's stated priority ("consolidate before deploying elsewhere").
3. **Provider bake-offs as night routines** — Gemini `[#491]` and Grok `[#492]` against the corpus (spec landed in the distillate §4; reconcile v0.1 to it); Codex sunset decision AFTER the Grok measurement, as a routing-table edit with the measurement cited.
4. **Orchestration under `[#412]`** — measured against CC-native agents/skills first.
5. **Token-efficiency measurement** under #29 before any optimization.

## 4 · Anti-goals (as binding as the goals)

No monorepo migration mid-consolidation · no provider retirement before its replacement passes the corpus · no new orchestration machinery where CC-native agents/skills cover the case · no folder created outside the GAP-2 intake's ruling · no re-derivation of anything §1 maps to an owner — attach evidence to the owner instead.
