# Handoff Interview — 2026-06-05-dev-knowledge-session

| Field | Value |
|---|---|
| Repo | `.dev-knowledge` (self-handoff) |
| Slug | 2026-06-05-dev-knowledge-session |
| Date | 2026-06-05 (Barcelona local; harness clock reads 2026-06-04 — same divergence the C3/C4 JOURNAL thread carries) |
| Type | session |
| Purpose | **Phase D — codification of the deployment arc into the methodology** |
| HEAD captured | 6e8c84fef3d2cfabee3e0cda89c5866c5082f9f1 (state being handed off: `main`, clean) |
| Branch (at capture) | `main` (interview committed on `docs/handoff-2026-06-05`) |
| Working tree (at capture) | clean |
| Process | HANDOFF_PROCESS v4.3.2 — Phase 1 (interview) |

## Role frame

Imagine an elder sage handing wisdom to a young apprentice. You — the sage —
are tired, your context is fading, but you hold the lived experience the
apprentice needs to continue this specific project's work. The apprentice
will read the books independently — PLAYBOOK, ESSENTIALS, CLAUDE.md, ADRs
— that's the theory. What only you can transmit is how the theory was
implemented in THIS project's specific circumstances during this session.

Answer narratively. Tag each claim with the **four-tag** discipline (v4.2
Amendment A — canonical; supersedes the three-tag body in §3.1):

- **witnessed** = I just verified this OR saw it happen recently AND have no reason to think it changed since
- **recall** = I remember this from earlier in the session — state may have changed; prefer verifying via CC inline if the claim is load-bearing
- **inferred** = reasoning from evidence (not direct knowledge)
- **unknown** = I don't know — say so explicitly

Skip any question that doesn't apply. Say so explicitly.

## Question block — copy from here

### 1. Past — what shipped

What did this session actually accomplish? Concretely: what merged, what
shipped, what changed in the codebase, what audits or decisions landed.

### 2. Present — where things stand

What's currently in-flight? Anything half-done, on an unmerged branch,
waiting on a merge, paused mid-decision, blocked on something external?

### 3. Future — natural next step

Of the open paths, which is the natural next step? What were you about to
do when this chat wound down? What's the obvious follow-up to what was
just done?

### 4. Wisdom — key decisions

Of the key decisions made this session, what was the reasoning? Anything
considered and rejected, and why? What turned out harder or easier than
expected?

### 5. Warnings — landmines

What should the next session NOT do? Anti-patterns you saw recur, landmines
specific to the current state, things that look wrong but are intentional,
witnessed-only context that won't be obvious from JOURNAL / BACKLOG / git
history.

## Question block — copy to here

---

## Phase-D receiver context (for Phase 2 — NOT part of the copy block)

> This is the standing brief the apprentice (the Phase-D chat) inherits. Phase 2
> folds it into `04_RECENT.md` / `05_NOW.md`. The deployment arc (phases A–C) is
> shipped and reconciled to git as of `main @ 6e8c84f`; **Phase D is codification
> only — bring the stale prose docs current with what already shipped.** Do NOT
> re-litigate the arc; do NOT rewrite prose in the sending session.

### Workstream 1 — living-doc staleness map (the rewrite targets)

| File | Verdict | Phase-D codification targets |
|---|---|---|
| `ARCHITECTURE.md` | **STALE** | add spec-orchestration doctrine; t-shirt model routing; machinery-retirement lifecycle (C3); adoption process; GitHub-Actions standard (cloud-night + nightly Action ARE already present) |
| `CLAUDE.md` | **STALE-by-deferral** | silent on cloud/nightly/spec-orch/routing; ≤200-line per-repo instruction defers to ARCHITECTURE — fix = add pointers once ARCHITECTURE gains the sections |
| `VISION.md` | **CURRENT** | strategic layer; operational detail appropriately deferred (optional: name model-routing efficiency as an emphasis) |
| `CONTRIBUTING.md` | **PARTIAL** | nightly Action + cloud-night documented; MISSING the spec-orchestration fallback rationale (why the `.js` workflow exists / when it runs) |
| `protocols/PLAYBOOK.md` | **STALE** | verify+complete Appendix B Model-Routing Table (suspected stub); add GitHub-Actions/cloud standards; add machinery-retirement patterns; expand §6 adoption with kill-criteria + tool-vs-platform rubric |
| `protocols/ESSENTIALS.md` | **CURRENT** | daily cheat sheet; correctly defers detail to PLAYBOOK/ARCHITECTURE |

### Phase-D agenda (the codification topics)

- **Adoption process** — rubric = tool-vs-platform / pain-owned-vs-imagined / subscription-economy fit + pilot discipline with **pre-registered kill criteria** + 3 case studies (Dynamic Workflows **ADOPT**, graphify **REJECT**, GitHub Action **ADOPT**).
- **T-shirt model-routing doctrine** — S=Haiku, M=Sonnet, L/judgment=Opus; unpinned fan-out = bug; unpinned default inherits the **main session model** (Opus 4.8). Verified functional on **both** the Agent-tool and workflow-engine paths after removing the `CLAUDE_CODE_SUBAGENT_MODEL=haiku` override (the C3 root-cause).
- **Deterministic prose-vs-state checker** — BACKLOG **[#89]** (counts / version stamps / enumerated lists = three evidence loci).
- **V4 verifier candidate** — BACKLOG **[#90]** (git↔backlog two-direction reconciliation — the inverse of V3; this sweep ran it manually as the reference spec).
- **Cloud-readiness** — shallow clones; environment guards in hooks; spec-orchestration as the canonical cloud execution path with a nightly native re-probe; cloud-session closeout = check stranded `claude/*` branches.
- **Maintenance cadences** — quarterly machinery review; plans prune.
- **Lessons codification** — config-archaeology (enumerate your OWN overrides before attributing behavior to the platform); operator-ruling-requires-the-operator's-explicit-word (never a paste-relay).
- **Superpowers reading pass** — skill-tests / format / hook-enforcement patterns (idea-mine only).
- **Python/Node floor pins** (ENVIRONMENT); **diagrams refresh** via the SVG pipeline.

### Pending-elsewhere markers (do NOT pull into Phase D)

- BACKLOG **#86** ADRs (selective-push / relative-path→URL hook migration / R2 saved-workflow distribution) + **AI-Council** work happen **after** Phase D, per the operator sequence: universalization → handoff → ADR/Council chat.
- **Watch item:** the first **production** nightly run — read the raw count without the shallow-clone false-positive class; confirm a clean tripwire and the Run-line path.

### Reconciliation baseline (record state at handoff)

git↔BACKLOG reconciled both directions this sweep — all arcs since 2026-06-04
**consistent**. Three record-gaps fixed: withdrew **[#87]** (routing bug-report
premise refuted by the C3 re-probe — self-inflicted env override, not a platform
bug), corrected **#83**'s stale "Haiku-only de-facto" note, added **[#89]/[#90]**.
JOURNAL + LESSONS complete (config-archaeology lesson present). `validate_backlog`
OK (52 tasks); pytest 235 green; ruff clean.

=== PASTE ANSWERS BELOW THIS LINE ===

