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
