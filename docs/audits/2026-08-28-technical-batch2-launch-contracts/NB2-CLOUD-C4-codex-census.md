# NB2 · CLOUD C4 — codex-surface census (READ-ONLY)

**Batch:** night-batch-2 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.

**Substrate:** cloud

## BRIEF (verbatim from the frozen bundle)

> **C4 — codex-surface census.** Corrected figures: **168** codex-* audit artifacts (not 155),
> 587 files tree-wide with codex- references. MUST classify the precedence-trap edge explicitly:
> the codex/ tree is the third precedence layer root AGENTS.md documents BY NAME — a removal
> proposal that deletes the file the precedence section describes is unusable. Every consumer
> counted and classified, removal-ready. ZERO deletion.

## THE PRECEDENCE TRAP, STATED SO YOU CANNOT WALK INTO IT

Root `AGENTS.md` carries a section titled **"Precedence — resolved BY SCOPE, not by position"**.
It names three layers, and the third is `codex/AGENTS.md` — *"a cwd at or below `codex/` yields
`role → doctrine → role`, and the role wins by position rather than by intent"*. **That file is
therefore load-bearing documentation, not residue.** Any removal proposal that deletes it, or
that deletes the `codex/` tree containing it, invalidates a section of a Tier-1 canonical doc.
Classify that edge **explicitly and by name**; a census that silently lumps it in with the rest
is unusable and will be rejected.

## WHAT TO COUNT AND CLASSIFY

1. **Verify the two figures first** — 168 `codex-*` audit artifacts and 587 files tree-wide
   carrying a `codex-` reference. Show the command you counted with and report **your** number
   beside the brief's. A restated count that nobody re-derived is exactly the defect class this
   repo names in `CLAUDE.md` §4 ("never restate a count or roster in prose").
2. **Per class, every consumer.** For each codex surface (audit artifacts, the `codex/` tree, the
   `/codex-review` command + skill, provider-registry rows, hooks, tests, doc references),
   enumerate **what reads it**. A surface with zero readers is removal-ready; a surface with a
   reader is not, whatever it looks like.
3. **Removal-readiness verdict per surface**: `REMOVAL-READY` (zero live consumers — list the
   search that proved zero) / `BLOCKED-BY <consumer>` / `PROTECTED <ruling or retention>` /
   `PRECEDENCE-TRAP` (the class above). Ordered by size freed.

## SELF-AUDIT

**ZERO deletion, zero edits** — you are producing a decision-ready worklist, not executing one.
And: if your `REMOVAL-READY` count is large, re-run one of them against the whole tree with a
different search (a grep for the bare stem, not the full path) before you claim zero consumers.
The cheap way to look productive here is to under-search.

---

## STANDING CLAUSES FOR EVERY CLOUD LANE OF NIGHT-BATCH-2 (frozen)

> Shared: zero writes, zero deletions, zero commits; no gate runs (uv mismatch); gate-dependent
> claims = MEASUREMENT-OWED-LOCAL. Each ends with EXACTLY ONE self-contained artifact.

**You are READ-ONLY.** Do not create, edit, delete, stage, commit, branch, push or tag anything.
Your entire output is ONE report, written as your final assistant message.

**You cannot run this repo's gates.** The container's `uv` is 0.8.17 against the repo's pinned
`required-version = "==0.11.19"`, so `uv run --locked …` cannot start. Read files, use `git log`
/ `git show` / `grep` / `python3` directly. **Any claim that would need a gate, a hook, the
pytest suite or `scripts/audit.py` to establish is written as `MEASUREMENT-OWED-LOCAL`, never
estimated and never asserted.** That marker is a first-class, correct outcome here.

**Every claim carries a resolving locator** — `path`, `path:line`, a heading, or a SHA. A claim
without one is not a claim. Do not restate a count you did not compute; compute it and show the
command.

**Output shape.** ONE self-contained artifact as your final message. Begin with the report's own
`#` heading as byte 0 — no preamble line, no wrapping code fence around the whole report. (Two of
the four 2026-08-26 cloud reports wrapped themselves in a fence behind one line of prose; the
harvester kept the bytes and recorded the deviation, which is more expensive than getting it
right.) Inside the report, fence code and tables that the operator will copy.

**Self-audit clause.** Each brief below states a way its own output can fail while looking
complete. Apply it to yourself and **say so in the report** if it happens.

**Repo facts you can rely on (measured on the operator's disk, 2026-08-28 23:36 local):**
`docs/intake/*.md` = 56 · `docs/decisions/*.md` (top level) = 89 · `docs/audits/*.md` (top level)
= 769 · `tasks/**/*.md` = 344 · `BACKLOG.md` = 67,883 B (a generated one-line VIEW since [#589];
the SOURCE OF TRUTH is `tasks/`). If your own count of the clone disagrees, **report both** — the
clone is `origin/main` and the disk may be ahead.
