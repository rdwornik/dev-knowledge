<!-- scope: meta -->

# ADR-66 — BACKLOG story-map hierarchy (Big Picture → Theme → User Story → Task)

**Status:** Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — a layout refinement of an already-ratified architecture).
**Supersedes:** **ADR-64 Decision 2 (the flat status-and-priority layout) ONLY.** ADR-64 Decisions 1/3/4 (done-items-leave, child-repo routing, the read-only validator) and **ADR-65** (done-item disposition) stand unchanged.
**Related:** ADR-41 (file mandate), ADR-47 (organization), ADR-64/65. Grounds the 2026-06-01 readability arc.

## Context

The flat `## Now / ## Open / ## Blocked / ## Coordination` layout (ADR-64) plus terse entries (the readability pass) made the file shorter but it still reads as **context-free mulch**: a flat list of tasks with no visible *why* or *goal* structure. The operator's verdict was that wording alone won't fix it — the fix is **structure**. Two established models apply:

- **Scrum backlog hierarchy** — theme → epic/story → task (strategic goals at the top, executable detail at the bottom).
- **Jeff Patton story mapping** — a big-picture "backbone" across the top, with detail hanging below it.

## Decision

`BACKLOG.md` is a four-layer story map:

1. **Big Picture** — a 2–3 sentence statement of what `.dev-knowledge` is working toward (from VISION) + the **theme backbone** (the theme list). Not prioritized; it is the map.
2. **Theme** — a `## ` backbone header (a durable area of work, e.g. *Handoff continuity*, *Enforced governance*).
3. **User Story** — a `### ` header in **human language** (the goal) + one `So that …` line (the why). **Personas = the operator and the AI agents (Claude Code / Codex) who inherit the repo.** This layer is what the operator scans.
4. **Task** — a bullet: `- [#id] [P][size] <terse technical action> · Done when: <criterion> · <ADR/refs>`. **Technical density is expected here — this layer is for the machine.**

Rules carried/changed:
- **No `repo:` field** — entries are implicitly `.dev-knowledge`. Cross-repo governance lives under the **Cross-repo universalization** theme, naming affected repos in the task text. **`repo:ecosystem` is killed** (no such repo); child-repo *execution* items remain in the relocation queue, not in `BACKLOG.md`.
- **Done tasks leave** (ADR-65, unchanged). **Git is the implementation record**, forward-indexed by `[#id]`; a `commit-msg` hook enforces that a backlog-touching commit carries `[#id]`/`closes [#id]`. The "what's been implemented" query is `git log --grep 'closes \[#'`.
- A read-only validator enforces the hierarchy (every task: unique `[#id]`, valid status, `Done when`, under a Story under a Theme; every Story has a `So that`; no done tasks remain).

## Consequences

- The operator scans **Big Picture → Themes → Stories** (goals + why); the LLM reads **Tasks** (precise execution detail). The two audiences are served by different layers of one file.
- Restructure reorganizes; **no id or task substance is lost** — prior `Why`/history stays in git history.
- Supersedes only the *shape* of ADR-64; its disposition/routing/validation decisions and ADR-65 are untouched.

## Alternatives considered

- **Keep the flat status-priority layout (ADR-64)** — rejected: empirically still unscannable for the operator (the readability pass shortened it but the operator's verdict stood).
- **A heavy/visual story map** — rejected: this is a markdown file for a solo operator; the hierarchy stays light and textual.
- **Council convene** — not taken: a layout refinement of a ratified architecture, operator-confirmed; Path A per ADR-65 precedent.

## References

- `docs/decisions/ADR-64-backlog-architecture.md` (Decision 2 superseded), `ADR-65-backlog-done-item-disposition.md`
- VISION.md (Big Picture wording); `protocols/PLAYBOOK.md` §10 (schema); `scripts/validate_backlog.py`

## Amendments

### 2026-06-13 — Accepted — 2026-06-14, **Path A** (operator ruling): durable dependency + parallelization fields (#156)

> **STATUS: Accepted — 2026-06-14, Path A (operator ruling).** This amendment was drafted as part of the #156 worktree pilot and its "ratify at integration" condition came due. #156 shipped, is enforced in `validate_backlog.py`, and was dogfooded into BACKLOG edges. The operator ratified by authority (the same path as ADR-82), making the doctrine coherent with the live enforcement. It is recorded here so the now-accepted decision travels with the schema it amends.

- **Source:** #156 ("Durable architect-mode task-graph"), built in worktree `worktree-156-taskgraph`. The architect's task-DAG (what-blocks-what / what-parallelizes) is **ephemeral residual prose** today — the Decision-item-4 task schema encodes no dependency or parallelism fields, so every session re-derives the graph by hand and its edges are never verified. The architect's own residual disclaims itself: *"Dependencies/parallelization above are the architect's read, not a schema fact — #156 is what would make them durable"* (`docs/handoffs/2026-06-12-dev-knowledge-session-3/RESIDUAL.md`).
- **Decision tier (proposed):** Path A — a layout/schema refinement of an already-ratified architecture (ADR-66 itself was Path A). The operator (or Council, at the operator's discretion) rules at integration.

**The schema extension.** Decision item **4 (Task)** gains **two OPTIONAL inline `·`-separated clauses**. Absence of either imposes no constraint (full backward compatibility — every existing task line stays valid).

| Field | Form | Meaning |
|---|---|---|
| `depends-on` | `· depends-on: #id, #id` | **Hard precedence (blocked-by) ONLY.** This task cannot start until every listed task completes. NOT provenance/supersedes, NOT a soft/"ideal" preference — those stay in prose/`refs`. |
| `serialize-group` | `· serialize-group: <label>` | A **shared-mutable-resource mutual-exclusion** label (e.g. two tasks that both edit `scripts/audit.py` → `serialize-group: audit-py`). Tasks sharing a label must not run concurrently. |

Before / after (task line, Decision item 4):

```
before: - [#id] [P][size] <action> · Done when: <criterion> · <ADR/refs>
after:  - [#id] [P][size] <action> · Done when: <criterion> · <ADR/refs> [· depends-on: #a, #b] [· serialize-group: <label>]
```

**Parallel-safety is DERIVED, not declared.** Two tasks are co-runnable iff there is no `depends-on` path between them **and** they share no `serialize-group`. There is deliberately **no `parallel-safe: true|false` field** — it would be redundant (derivable) and underspecified (it cannot express *which* tasks conflict). Absence of any annotation = parallel-safe by default, matching the architect's "independent cleanups parallelize" framing.

**Enforcement (`scripts/validate_backlog.py`, read-only Layer-2, added by #156):**

1. **Reference-existence (strict).** Every id in a `depends-on` clause MUST be a live task id in `BACKLOG.md`. A reference to a non-existent / typo'd / renumbered id is a **hard-fail**. The `depends-on` clause is parsed in isolation — `#id`s appearing in `refs` or prose are NOT dependencies.
2. **No-cycle.** The `depends-on` graph must be acyclic. The validator topologically inspects it (DFS) and **hard-fails on any cycle — direct (A↔B), indirect (A→B→C→A), or self-loop (A→A)** — reporting the cycle path.

**Consequence the operator must weigh (strict reference-existence).** Because done tasks **leave the file** (ADR-65), closing a depended-on item makes every dependent's `· depends-on: #closed` a dangling reference — a hard-fail until the now-satisfied edge is pruned. So **closing a blocker becomes a documented two-step**: remove the item *and* prune inbound `depends-on` edges to it (grep `depends-on: .*#<id>`). This is the intended trade — a consistent, dangling-free graph in exchange for a small prune-on-close tax — and the reason the alternative (lenient: allow absent ids) was rejected: a lenient check lets a typo'd id pass silently, defeating the check's purpose.

**Scope of the #156 pilot (dogfood).** A small *representative* batch of real edges is encoded — **not** all ~75 (full encoding is incremental). The pilot encodes one honest hard edge (`#112 depends-on #23` — "Option B held until #23") plus a `serialize-group: audit-py` across the audit.py-mutating items (#7, #36, #140). Soft/provenance relations (e.g. #156↔#150, #164↔#163) are deliberately **excluded** from `depends-on` per the hard-blocked-by-only rule.

- **Ratification:** ratified 2026-06-14 by operator authority (Path A), at integration of `worktree-156-taskgraph` — the "ratify at integration" condition, met. #156 was shipped, enforced, and dogfooded before this ruling; the ratification reconciles the doctrine with the already-live enforcement.
