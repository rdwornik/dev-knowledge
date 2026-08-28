# NB2 · CLOUD C5 — README/VISION consumer census (READ-ONLY)

**Batch:** night-batch-2 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.

**Substrate:** cloud

## BRIEF (verbatim from the frozen bundle)

> **C5 — README/VISION consumer census.** Every reference into VISION.md and README, classified,
> merge-ready. Two constraints reckoned with up front: root README.md was DELETED 2026-05-23
> (do not propose recreating it as a side effect) and ADR-114 (may a root README be recreated)
> is PARKED, not decided. A merge proposal ignoring either is unusable. ZERO edits.

## THE TWO CONSTRAINTS, FIRST — read them before you census

- **Root `README.md` was deleted 2026-05-23** (ADR-38 amendment A5; `CLAUDE.md` §5 rule 5 says
  *"do not recreate it"*). Any proposal whose side effect is a root README is refused on sight.
- **ADR-114 is PARKED, not decided** — `docs/decisions/ADR-114-*.md`, *"May a root `README.md` be
  recreated — and what does substituting a canonical living-doc filename actually cost?"* Read it.
  A parked ADR is not a licence and it is not a prohibition; treat the question as **open and
  reserved to the operator**, and do not answer it inside a census.

Open both, quote the binding line from each, and state at the top of your report how your
proposal respects them. A proposal that does not do this is unusable.

## THE CENSUS

Every reference **into** `VISION.md` and every reference to a README (root, `docs/`, plugin,
consumer, template — all of them; the root one is absent, its *references* may not be). For each:
the citing `path:line`, the exact text, what the citation is FOR (navigation, doctrine, an
example, a gate input), and whether it still resolves. Classify:

- `LIVE` — resolves and is load-bearing.
- `DANGLING` — points at something absent (the deleted root README is the obvious generator of
  this class; enumerate them all, they are the actionable set).
- `REDUNDANT` — resolves, but a nearer canonical source says the same thing.
- `GATED` — a generator, hook, test or freshness stamp reads it, so editing it has a mechanical
  consequence. Name the gate. (`VISION.md` is in the freshness-stamped set; check before you
  propose touching it.)

Then the **merge-ready proposal**: which references collapse into which single site, in what
order, and what each merge costs. Cite ADR-49/65 (info-preserving condensation) where you propose
condensing rather than deleting.

## SELF-AUDIT

If your proposal's net effect is "create one document that explains the repo", you have proposed
the root README by another name — say so and withdraw it. And if you found zero DANGLING
references to a file that has been deleted for three months, you did not search hard enough.

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
