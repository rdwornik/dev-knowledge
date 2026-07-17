# Architect strategic supplement — 2026-07-17-corp-monorepo-executor-product-execution

Repo: corp-monorepo (bundle hosted in the hub .dev-knowledge) · Mode: execution · Date: 2026-07-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next session captures off-repo context live via the §13(d) operator-context beat. The empty file is still committed — a record that this session had no transmissible live "why" (the defined cold-handoff disposition, not a defect). **This bundle was generated COLD, then FILLED (2026-07-17):** the outgoing senior-architect chat answered all six questions; its ANSWERS (below) fold into `PASTE_THIS.md` and carry the strategic *why* alongside the in-repo charter + signed manifest + A3 ruling. The incoming §13(d) operator-context beat therefore **NARROWS** to *"anything changed since the supplement was written?"* — the operator queue itself is Answer 4 / charter §5.

## QUESTIONS — paste these to the outgoing chat

1. **Strategic intent** — what should the next session achieve? (The product outcome, not a single task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo (the operator queue, charter §5).

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

ANSWERS — supplement (outgoing senior-architect session, 2026-07-17)

1. STRATEGIC INTENT. Take the pre-operational system to a witnessed, structured,
   testable process state — in this order: (a) execute the signed engine cleanup +
   interface unification so the substrate is trustworthy; (b) stand up
   URL/source management (FR-10 registry + source-value scoring) as THE foundation
   layer — it underpins file/directory management, the magistrala, and every
   downstream flow; (c) prove the full process by SIMULATION before improving it:
   the one-client end-to-end thread (Project_Codes → ingest/magistrala → vault →
   one cited RFP answer + one cited deck slide, per the T6 brief) run in sandbox.
   Product outcome: the operator can run one real process end-to-end and trust
   the tests around it. RFP-algorithm consolidation (one compose mechanism →
   Word/Excel/PPT) is a first-class goal, sequenced after the knowledge substrate
   (R10).

2. TENSIONS WEIGHED. (a) RFP-first (intake §8) vs knowledge-first → knowledge-first
   (R10): answer quality is bounded by the substrate, and the operator ruled it.
   (b) Usage-based vs design-intent kill criteria → design intent governs while the
   system is pre-operational (usage signals are void; the signed manifest is the
   deletion authority). (c) Protocol weight → contracts-at-seams (R2 subprocess
   boundary, R6 accessor, T6 Content Manifest, N2-class seam tests); no
   microservices at solo scale. (d) Docs now vs once-after → R9, rewrite once
   after Arc B+C. (e) Literal PageRank vs deterministic source-value scoring →
   deterministic day-1 (type/recency/curation/operator priors + neighbor
   propagation), learning later behind adopt-map triggers.

3. CONSIDERED + REJECTED (do not relitigate). Microservices/message bus (NOT-list,
   solo sizing) · literal PageRank link-graph (folders have no link graph; bandit
   queue + hierarchical priors instead) · blanket DR-4 deletions (re-greps
   disproved three of them; manifest supersedes) · deep-copy consolidation of
   sources (reference-not-copy per DR-12: physical layer in place, logical layer
   = registry + shortcut hubs) · immediate section-library↔RFP-store unification
   (deferred to an ADR, T6-D1) · prompts as untracked ephemera (routing rule v3:
   cross-chat artifacts live in the hub handoff carrier).

4. OPEN QUESTIONS. BLOCKING: the 2648/5 → 2624/6 test-collection delta must be
   explained before Arc-B execution starts. Operator-only: ADR-35 amendment
   (backup leg-2 → personal OneDrive), Graph consent (unblocks scout + X1), vault
   git remote, 4 credential rotations, final zone names, T6-D4 SharePoint push.
   Deferred by design: KB provenance (unparks at E4/R1), FR-20 Content Manifest
   ratification, section↔RFP-store ADR.

5. DECOMPOSITION RATIONALE. The methodology spine docs → intake → ADR → backlog →
   execution is COMPLETE and must not be redone: witnessed audits (ground-truth,
   double-derived by Codex) → intake +§9 (FR-1–19) → ADR-33..36 + A3 R1–R10 →
   BACKLOG 7 themes / 9 stories / 51 tasks with 3 hard depends-on edges
   (#29←#19–#23 cut-before-unify · #36←#35 registry-before-scout · #53←#29
   docs-once-after). Theme order E1→E2→E3→E5→E6→E4→E7 carries priority (R10).
   Do NOT re-decide: A3 R1–R10, the signed manifest rulings, the FR-13
   reconciliation, theme order, the depends-on edges. The executor's freedom is
   task-level within themes; theme-level changes go through the senior architect.

6. OFF-REPO CONTEXT. The system is pre-operational — the operator uses nothing as
   an agent yet; wire-it-up is the mission, and usage arguments are void until it
   runs. Operator process-vision emphases to hold: URL management is the
   foundation stone; SIMULATE the whole flow end-to-end (Project_Codes → magistrala
   → Excel/Word/PPT/demo/KT) before optimizing — treat the simulation as the
   acceptance bar for E3/E5, not a new epic; a 403-slide MASTER DECK + brand spec
   v2 + section library already exist in demo-prep (input for the deck lane and
   the T6 succession path — verify at migration, do not rebuild); continuous
   improvement runs on the night-batch cadence with code review, unit tests, and
   sandbox dynamics as standing discipline. Supervision loop: the executor submits
   each arc's plan to the senior architect (via the operator) BEFORE execution.
   The operator queue is charter §5 — it is the single list of things only he can
   do.
