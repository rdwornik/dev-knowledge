# NB2 · CLOUD FM-C — the FULL FUNNEL CENSUS (READ-ONLY)

**Batch:** night-batch-2, wave 1 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.
**This lane's output is the BEFORE half of tomorrow's asset balance.** Wave 2's FM-3 executes
against it under a staleness guard, so a wrong classification here is caught but expensive.

**Substrate:** cloud

## BRIEF (verbatim from FM-WAVE2-CONTRACTS-2026-08-28.md §FM-C — this section IS the brief)

> FULL FUNNEL CENSUS. Zero writes/deletes/commits; no gate runs (uv 0.8.17 vs pin — gate-dependent
> claims marked MEASUREMENT-OWED-LOCAL). ONE self-contained artifact.
> Scope: every file under docs/intake/, docs/decisions/, docs/audits/ (the conformance HTML
> dashboard enters like any artifact) + BOTH directions: every OPEN tasks/ row's source: resolves.
> Classify EVERY object with a resolving evidence locator: CONSUMED-BY <ids> /
> CONSUMED-AND-ARCHIVABLE (all consumers terminal) / ORPHAN (no consumer AND no rejection record) /
> PROTECTED (cite the retention or ruling). Carry each object's status + dated transitions where
> derivable (frontmatter, git dates). Output: (1) headline counts per directory per class —
> the BEFORE numbers; (2) the ARCHIVAL WORKLIST, decision-ready; (3) the ORPHAN LIST, both
> directions; (4) UNCLASSIFIED — must be 0, each exception explained. Do not propose deleting the
> codex/ precedence-layer file. Ex-ante: 100% classified, every claim locatored; a census routing
> most objects to ORPHAN without evidence has not censused — say so of your own output.

## THE BINDING CLAUSES THAT REACH THIS LANE

**A1 — state is first-class.** Every governed object carries an explicit state plus **dated
transitions**. Derive them where the tree allows: intake frontmatter `status:`, ADR status lines,
`tasks/` frontmatter `status:`, and git dates (`git log --diff-filter=A --format=%ad -- <path>`
for birth, last-touch for the latest transition). Where a transition is not derivable, say
`UNDATED` — never invent one.
**A5 — trust contract.** Every claim carries a witness. Print the command for every count.

## THE STATE MACHINE YOU ARE CENSUSING AGAINST

`audit -> intake | ADR` · `intake -> reject/archive | ADR` · `ADR -> backlog rows` ·
`rows -> executed` · **consumed sources -> ARCHIVED at terminal state.** An object is
CONSUMED-AND-ARCHIVABLE when every consumer it produced has reached a terminal state and nothing
else cites it. That is the judgement the whole census turns on — make the terminal-state test
explicit and apply it uniformly.

## BOTH DIRECTIONS — this is the half a census usually skips

- **Forward:** for every object in `docs/intake/`, `docs/decisions/`, `docs/audits/`, what
  consumed it? (an ADR, a `tasks/` row, a packet, a gate, another artifact).
- **Backward:** for every **OPEN** `tasks/` row, does its `source:` resolve to a real object?
  A row whose source does not resolve is an orphan **in the other direction**, and it is the
  direction that produces work nobody can justify.

Row ids and statuses come from **`tasks/`**, the source of truth since [#589] — `BACKLOG.md` is a
generated one-line VIEW and a body-reading pass over it silently returns an empty set.

## SCALE, AND HOW TO SURVIVE IT

Measured on the operator's disk 2026-08-28 23:36 local: `docs/intake/*.md` = **56**,
`docs/decisions/*.md` = **89**, `docs/audits/*.md` (top level) = **769**, `tasks/**/*.md` = **344**.
That is ~1,258 objects. Do not read all of them end to end. Build the citation graph
mechanically first — one pass extracting every `docs/(intake|decisions|audits)/…` path, every
`ADR-\d+`, every `[#\d+]` and every intake number from the whole tree — then classify from the
graph and only open a file when the graph is ambiguous. Show the extraction commands. If you
cannot complete all four directories, complete `docs/intake/` and `docs/decisions/` **fully**
(they are what FM-3 archives) and report `docs/audits/` as a partial with the exact coverage
fraction — a truthful partial beats a complete-looking guess.

## HARD CONSTRAINTS

- **Do not propose deleting `codex/AGENTS.md`** — root `AGENTS.md`'s precedence section documents
  it BY NAME as the third precedence layer. Classify it PROTECTED and cite that section.
- The conformance HTML dashboard is censused **like any other artifact** — no special pleading in
  either direction.
- **UNCLASSIFIED must be 0.** Every exception is named and explained individually.

## SELF-AUDIT

The brief's own words: *a census routing most objects to ORPHAN without evidence has not
censused.* Print your class tally. If ORPHAN is the plurality, say so under an unmissable heading
and re-test a sample of ten by a second search method before standing behind it.

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
