# .dev-knowledge BACKLOG

## Big picture

`.dev-knowledge` is the ecosystem's methodology brain: it absorbs lessons from every repo, universalizes them into enforced conventions, and audits the ecosystem against them — the LLM-development "scrum master" for all `Dev/` projects (VISION: Knowledge Guardian · Methodology Author · Auditor · Disseminator). The backlog advances that mission across seven themes.

**Themes (backbone):** Handoff continuity · Enforced governance · Lessons feedback loop · Decision management · Canonical-file integrity · Cross-repo universalization · Tooling & evaluation

> **SKELETON — story/theme taxonomy pending operator GO.** Tasks are filed under these stories in step 3 (after confirmation). The 47 existing items are preserved in git at `90d407b`; the `(will hold: …)` hints below show where each id will land. Layout: ADR-66 (Big Picture → Theme → User Story → Task).

---

## Handoff continuity
> As a session inheriting this repo, I want to pick up with full state and lose nothing.

### Make every handoff self-correcting, not just the big ones
So that routine handoffs stop inheriting the ~25% insider blind spot, and framing stops leaking into receiver behavior.
_(will hold: #1, #6)_

### Let an inheritor act on the operator's defaults instead of re-asking
So that a fresh chat states-and-acts rather than over-asking on things it should assume.
_(will hold: #26)_

### Close the deferred handoff-template refinements
So that the v4 templates stop carrying known minor gaps.
_(will hold: #25)_

---

## Enforced governance
> As the operator, I want load-bearing conventions enforced by tools, not memory, so they can't silently drift.

### Turn advisory guards into enforced gates
So that a convention can't be skipped under load (the failure mode behind real aborts).
_(will hold: #11, #13, #15)_

### Extend structural validation to more governance artifacts
So that drift in transcripts, ADRs, and folders is caught cheaply, not by reviewer luck.
_(will hold: #7, #36, #42)_

### Wire up the lifecycle hooks the workflow relies on
So that session-start/close automation actually runs instead of being wired-but-vacuous.
_(will hold: #8, #12)_

---

## Lessons feedback loop
> As the methodology author, I want lessons to flow back into enforced rules, not sit in an archive.

### Make lessons an active feedback loop, not a passive archive
So that captured lessons reach runtime rules and stay enforceable.
_(will hold: #4, #22)_

### Codify recurring patterns into the methodology
So that observed failure-modes become written guidance instead of recurring.
_(will hold: #34, #28)_

---

## Decision management
> As a reader of 65+ ADRs, I want decisions navigable and free of silent contradiction.

### Keep the decision corpus navigable and contradiction-aware
So that growth past 65 ADRs doesn't bury or quietly contradict prior decisions.
_(will hold: #2, #23)_

### Codify the meta-decision rules
So that future sessions route decisions consistently (convene vs Path A; relax vs gate).
_(will hold: #18, #27)_

### Close the small ADR cross-reference + registry amendments
So that the ADR web is internally consistent.
_(will hold: #19, #20, #21)_

---

## Canonical-file integrity
> As any agent reading this repo, I want the canonical files accurate and current.

### Keep canonical files accurate
So that stale ground truth stops silently misleading sessions (the repo's own VISION is "drift detected proactively").
_(will hold: #3, #10, #24, #35)_

### Keep the day-to-day docs right-sized and current
So that the cheat-sheet and architecture stay scannable as conventions accrue.
_(will hold: #5, #41)_

---

## Cross-repo universalization
> As the disseminator, I want every child repo to converge on the universal baseline.

### Converge every child repo on the universal baseline
So that "open any repo, same layout/governance" actually holds.
_(will hold: #45, #46, #47 — child-repo execution lives in the relocation queue)_

### Give the auditor cross-repo reach
So that drift across repos is caught without a manual sweep.
_(will hold: #29, #44, #9)_

### Make new-repo scaffolding correct-by-default
So that a new repo inherits the full baseline in one step, not by re-derivation.
_(will hold: #16, #17, #43)_

---

## Tooling & evaluation
> As the operator, I want low-friction tooling and timely tech adoption.

### Cut session friction with better tooling
So that cognitive overhead per session drops.
_(will hold: #32, #33, #37, #38, #39, #40)_

### Decide the undecided artifact/tool models
So that cadence-less artifacts and unevaluated tools don't rot or get adopted blind.
_(will hold: #14, #30, #31)_

---

**About this file** — open/in-progress `.dev-knowledge` work as a story map (ADR-66): Big Picture → Theme → User Story → Task. Done tasks leave (ADR-65); git is the implementation record (`git log --grep 'closes \[#'`). Child-repo execution items live in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`. Schema: PLAYBOOK §10 (updated in step 4); machine-checked by `scripts/validate_backlog.py` (hierarchy parser lands in step 4).

**Grooming log:** 2026-05-09 · 2026-05-23 · 2026-05-24 · 2026-05-31 (marathon-arc) · 2026-06-01 (ADR-64/65 migration + readability + ADR-66 story-map). Next quarterly: 2026-07-01.
