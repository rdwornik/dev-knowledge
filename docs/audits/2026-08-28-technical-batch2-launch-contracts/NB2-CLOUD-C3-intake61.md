# NB2 · CLOUD C3 — intake-61 ratification sheet (READ-ONLY)

**Batch:** night-batch-2 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.

**Substrate:** cloud

## BRIEF (verbatim from the frozen bundle)

> **C3 — intake-61 ratification sheet.** Options-and-consequences for all five open questions;
> q1 ("what exactly IS the engine?" — assembler, probe gate, seal-identity, boot contract) and
> q2 (copy-with-hash on the floor pattern VS consumer-side pin to a hub release tag — a stale
> copy is detectable, a stale pin is not) get the deepest treatment; q5 tested against the
> ADR-28/36 Layer-2 invariant rather than waved through. NO row proposed — this feeds
> ratification, not filing.

## FIND THE INTAKE FIRST

`docs/intake/` — locate intake **61** by its number in the filename or frontmatter, read it in
full, and **quote each of its five open questions verbatim** before answering. If the intake's
question set is not exactly five, say so and answer what is actually there — do not manufacture
symmetry.

## HOW TO ANSWER (this is a ratification sheet, not an essay)

Per question: **the options** (2–4, each a decision the operator could actually take), **the
consequences of each** (what becomes true, what becomes impossible, what it costs), **the
evidence** (locators in this tree), and **what the answer would bind** (which files, gates or
rulings change). No recommendation is required; where you have one, mark it as yours.

- **q1 — "what exactly IS the engine?"** The four candidate constituents named are the
  **assembler**, the **probe gate**, **seal-identity**, and the **boot contract**. Locate each in
  the tree (`scripts/gen_handoff.py` and its neighbours; `scripts/check_seal_identity.py`;
  `protocols/HANDOFF_PROCESS.md`) and decide, per constituent, whether it is engine or cargo.
  An "engine" that is a synonym for "everything" answers nothing.
- **q2 — copy-with-hash VS pin-to-tag.** The asymmetry the brief hands you is the crux: **a stale
  copy is detectable, a stale pin is not.** Ground both sides in the live floor pattern:
  `.claude/CLAUDE-FLOOR.md` + its sha256 sidecar + the `floor-hash-verify` hook + the
  `check_floor_hash.py --require-present` SessionStart guard. Then say what a consumer-side pin
  to a hub release tag would detect, and what it would silently miss.
- **q5** — whatever it is, test it against the **ADR-28/36 Layer-2 invariant**: Layer 2 never
  executes; no script here drives state in a child repo; validators, generators and gates are in
  scope, orchestration is not. If q5 would breach that invariant, say so plainly.

## SELF-AUDIT

**Propose no backlog row and no intake.** If you find yourself writing a row body, you have left
the brief. Also: if you answered a question without quoting it first, you may have answered a
question the intake does not ask — check, and say so.

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
