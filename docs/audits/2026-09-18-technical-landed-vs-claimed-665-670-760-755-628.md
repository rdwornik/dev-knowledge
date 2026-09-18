# LANDED-vs-CLAIMED — nine rows: [#665] [#666] [#667] [#668] [#669] [#670] [#760] [#755] [#628]

**Measured:** 2026-09-18, on this worktree's HEAD (branch `worktree-lane-ac-741-dispatch-surface`).
**Method:** read each row's own `tasks/<id>-*.md` frontmatter/body for its claimed state, then
independently checked the files/scripts/commits it cites — `wc -c`, `git log`/`git show --stat`,
direct file reads, and `scripts/file_purpose_graph.py why` for wiring questions the repo's own
graph gate requires queried rather than grepped.

## [#665]

**Claimed:** `status: open`. Done when: "one map file covers every chapter of `protocols/
PLAYBOOK.md` and `ARCHITECTURE.md` with the four fields per chapter [purpose · live/dead/
duplicated · implementing modules · keep/merge/cut recommendation]; every locator resolved
against the live tree."

**Actually landed:** no chapter-map file exists anywhere in the tree. A search for any file
matching the deliverable this row describes (by content or by an obvious name) found nothing
outside the task row itself and its own archived annotations (`tasks/archive/665.md`). No
`agy`/Gemini-substrate output artifact is present.

**Verdict:** AGREE — row correctly remains open; nothing claims otherwise.

## [#666]

**Claimed:** `status: open`, `depends-on: #665`. Done when: "every chapter of both files carries
a recorded keep/merge/cut ruling in ONE file... and [#667]'s write-scope is DERIVED from that
file."

**Actually landed:** since [#665]'s map (its sole input) does not exist, the operator sitting
this row describes cannot have happened, and no such ruling file was found in the tree.

**Verdict:** AGREE — correctly blocked/open; dependency [#665] is itself unmet.

## [#667]

**Claimed:** `status: open`, `depends-on: #664`. Five acts: (1) `ARCHITECTURE.md` ≤15 KB
rendered from the spine graph, (2) `PLAYBOOK.md` cut chapter-by-chapter, (3) `protocols/
DISPATCH.md` split out of PLAYBOOK Ch8, (4) `CLAUDE.md` §7–§9 become generated fragments,
(5) `ESSENTIALS.md` deleted (owned by `[#628]`, explicitly not duplicated here).

**Actually landed:** `[#664]` (`tasks/664-wire-fpg-1-as-the-delivery-spine-three-commit-tier.md`)
is itself `status: open`, so the row's own stated precondition is unmet. Independently: (1)
`ARCHITECTURE.md` is **110,357 B** today (`wc -c`), nowhere near ≤15 KB, and `scripts/
file_purpose_graph.py` (checked directly — `sub.add_parser` calls) exposes only `why` and
`stats` subcommands, no render/emit, so act (1) cannot have been built. (3) `protocols/
DISPATCH.md` does not exist in `protocols/`. (4) is **partially true independent of this row**:
`CLAUDE.md` §7 and §9 already import generated fragments (`@.claude/generated/commands-repo.md`,
`@.claude/methodology-roster.md`, `@.claude/generated/recent-adrs.md`), but this predates/
is-orthogonal to this row and §8 (skills) is still hand-rostered prose, not generated. (5) did
land, via `[#628]`'s effort (see the ESSENTIALS section below), consistent with this row's own
text that `[#628]` owns and is not duplicated here.

**Verdict:** GAP, in the not-yet-landed direction for acts (1)–(3) — status open is honest;
act (4) is partially true but not attributable to this row landing; act (5) landed but via
`[#628]`, exactly as the row itself says it should.

## [#668]

**Claimed:** `status: open`, `depends-on: #667`. Done when: two ten-question scored evals (one
per file) run against a seat given only the file under test, scored per cut, a stated passing
bar, kept fresh by a hook.

**Actually landed:** `[#667]` (this row's sole dependency) is open and its acts unmet (see
above), so the precondition for this row cannot have been satisfied. No eval script, scored
artifact, or passing-bar declaration was found referencing this row.

**Verdict:** AGREE — correctly blocked/open.

## [#669]

**Claimed:** `status: open`, `depends-on: #664`. Done when: four delivery-loop transitions
(intake→row, row+contract→dispatch, merged→render/telemetry/closure-propose, ratified→archive)
each fire from a declared trigger with trip-tests; `archive_row_body` runs from its trigger
rather than by hand; telemetry has a named consumer on the merge leg.

**Actually landed:** `[#664]` is open (same blocker as above), which the row cites as a hard
precondition ("cannot start before [#664]"). Independently: `scripts/file_purpose_graph.py why
scripts/archive_row_body.py` shows it "is triggered by file:.pre-commit-config.yaml [wiring]" —
but `CLAUDE.md` §9 documents that hook (`row-archive-proof`) as running **`archive_row_body.py
verify` only, "never the writing subcommands ([#664] TRIGGER row)"** — i.e. the archiving
*write* action is explicitly still gated behind `[#664]`, matching this row's own dependency.
`propose_closures` does have a live `Stop` hook (per `.claude/methodology-roster.md`), so that
one sub-piece is wired, but the row's Done-when is the whole four-transition machine, which is
not built.

**Verdict:** AGREE — correctly blocked/open; the one piece that IS wired (`propose_closures`
Stop hook) doesn't discharge the row's full done-when.

## [#670]

**Claimed:** `status: open`, `depends-on: #644`. "The only step of the plan that reaches the
operator's working day" — floor v1.5.0 deploy to `corp-monorepo`, blocked until `[#644]`'s
deploy-freeze is ruled either way.

**Actually landed:** `tasks/644-the-2026-08-29-deploy-freeze-has-never-been-ruled.md` is
`status: open` — the freeze has still not been ruled. No deploy artifact/log for a v1.5.0
floor push to `corp-monorepo` was found.

**Verdict:** AGREE — correctly blocked/open on its named, still-open blocker.

## [#760]

**Claimed:** `status: open`. X3 row carrying the ≤15 KB `ARCHITECTURE.md` target out of batch Y
(filed by operator ruling 2026-09-14). Documents the render-premise as REFUTED three ways
(no emit/render subcommand in `file_purpose_graph.py`; no script writes `ARCHITECTURE.md`;
`[#664]` itself sequences the render as X3), and records the 100,845 B / eleven-chapter
measurement as the starting point.

**Actually landed:** the refutation still holds today — confirmed independently:
`file_purpose_graph.py` has only `why`/`stats` subparsers, and `ARCHITECTURE.md` is currently
**110,357 B**, still far over ≤15 KB (see the untracked `docs/audits/2026-09-18-technical-
architecture-md-live-byte-count.md` already sitting in this tree, which independently confirms
the live count and shows the file has actually **grown back** past every prior cut milestone:
129,213 B baseline → 100,800 B "at freeze" per the batch-Y contract → 95,288 B per commit
`530dbecf` on 2026-09-15 → 110,357 B live today).

**Verdict:** AGREE — row correctly stays open; its premise (render not yet built) is still
true, and the target is further from met today than at either prior measurement point.

## [#755]

**Claimed:** `status: open`. Residual of batch-Y lane `lane-y-755-docs-cut-finish`. Claims that
lane "DELETED `protocols/ESSENTIALS.md` (16,461 B) and closed `[#628]` on the file's absence."
Clauses A–F document what the lane did NOT reach: ARCHITECTURE ≤15 KB (blocked, handed to X3/
`[#760]`), the floor template's ESSENTIALS mention (owned by `[#628]`'s release-act sequencing),
manifest `doc_shapes` rows, `AI_COUNCIL_PROCESS.md`'s history entry, `STANDING_RULINGS.md` T-29,
and a `PLAYBOOK.md` freshness stamp (deliberately left RED as a tripwire).

**Actually landed:** the deletion is real — commit `e791cffc` (2026-09-14, "docs(protocols):
delete protocols/ESSENTIALS.md and follow every surface it breaks") is a commit on branch
`worktree-lane-y-755-docs-cut-finish`, merged via `b779616e`, matching this row's claim that
its lane did the deleting. **However the "closed `[#628]` on the file's absence" clause is
false as stated** — the merge commit `b779616e` explicitly records an operator ruling: "`[#628]`
does NOT close -- deletion discharged, floor sidecar and pinned manifests are a release act;
the row stays open with what is discharged recorded," and `[#628]`'s task file is still `status:
open` today. So this row's own summary sentence overstates its lane's effect on `[#628]`; the
detailed clauses A–F later in the same row correctly describe `[#628]` as still carrying
unfinished work (floor template, manifests), which is internally consistent with `[#628]`
staying open — only the opening summary line is wrong. `ARCHITECTURE.md`'s live size (110,357 B)
also confirms clause A's "not reached" is still true, and confirms it has drifted further from
target since this row's own 95,288 B milestone.

**Verdict:** GAP — the opening summary claims `[#628]` was closed; it was explicitly ruled to
stay open in the very same merge. The row's detailed clauses (which cite `[#628]` as still
owning open work) contradict its own summary sentence.

## [#628]

**Claimed:** `status: open`. "DC-2 re-cut — dissolving `ESSENTIALS.md` is a FLEET-COUPLED release
act, not a doc lane." Done when: frozen contract covering all ten consumers plus the floor
sidecar/pinned manifests; ADR-88 register entry re-based; `canonical_docs.py` memberships moved;
tolerant readers confirmed; two anchor-text sites (`AI_COUNCIL_PROCESS.md`, `PLAYBOOK.md` Ch2)
re-worded — all in the SAME act as the deletion.

**Actually landed:** matches. `ESSENTIALS.md` is gone (confirmed: `git log --diff-filter=D` finds
only `e791cffc`, and the file is absent from `protocols/` today). The deleting commit's own body
explicitly frames itself as discharging `[#628]`'s release-coupling requirement ("[#628] closes
on the file's ABSENCE rather than its de-registration," refs `[#628]`, `[#667]`, `[#755]`) — but
the merge that actually landed it (`b779616e`) carries an explicit operator ruling overriding
that framing: `[#628]` does **not** close, because the floor template/sidecar/pinned-manifest
work (part of this row's own Done-when) is a separate release act sequenced with v1.5.0 and was
deliberately NOT touched by the deleting commit ("templates/child-methodology-floor.md.tmpl --
... its line is stale prose, not a broken route, so the deletion does not force it"). `[#628]`'s
task file correctly reflects this: `status: open`.

**Verdict:** AGREE — row correctly stays open; the deletion (the headline act it owns) landed,
but the row's own broader Done-when (floor/manifest work) has not, and the row has not been
closed, consistent with the explicit operator ruling.

## The ESSENTIALS.md contradiction, resolved

**Deleting commit:** `e791cffc` — 2026-09-14 (17:21:44 +0200) — "docs(protocols): delete
`protocols/ESSENTIALS.md` and follow every surface it breaks." It is a lane commit on branch
`worktree-lane-y-755-docs-cut-finish`, merged into `main` via merge commit `b779616e` ("Merge
branch 'worktree-lane-y-755-docs-cut-finish' @ 09a5cebd -- ESSENTIALS.md is deleted, [#628]
stays OPEN by ruling"), same day. The deleting commit's own trailer cites `Refs: [#628], [#667],
[#755]`, and its body states "[#628] closes on the file's ABSENCE rather than its de-registration."
The merge commit that actually lands it on `main` **overrides that framing with an explicit
operator ruling**: "`[#628]` does NOT close -- deletion discharged, floor sidecar and pinned
manifests are a release act; the row stays open with what is discharged recorded."

**Which row is authoritative:** `[#628]` is authoritative for the deletion's *governance* — it
is the row that was filed (operator ruling 2026-09-01) to own "dissolving ESSENTIALS.md [as] a
FLEET-COUPLED release act," it is the row the deleting commit itself cites as the thing being
discharged, and `CLAUDE.md`'s own top-of-file claim ("`protocols/ESSENTIALS.md` was deleted
2026-09-14 (`[#628]`)") matches this — `[#628]` is correctly the citation for the fact of
deletion. `[#755]` is authoritative for *execution* — its lane (`lane-y-755-docs-cut-finish`)
is the branch the deleting commit actually lives on, and `[#755]`'s row correctly carries the
detailed residue (floor template, manifests, AI_COUNCIL history, T-29, PLAYBOOK stamp) that
`[#628]` still owns.

**What is wrong:** `[#755]`'s own summary sentence — "closed `[#628]` on the file's absence" —
is factually wrong/stale. The same merge that landed the deletion (`b779616e`, same lane,
same day) explicitly rules `[#628]` stays open, and `[#628]`'s task file is `status: open`
today, confirming the ruling held. `[#628]`'s text is not wrong on this point; it does not
claim closure anywhere in its own body.

**Resolution:** the deletion of `protocols/ESSENTIALS.md` landed 2026-09-14 in commit
`e791cffc` on lane `lane-y-755-docs-cut-finish` (merged as `b779616e`), discharging part of
`[#628]`'s release-coupling requirement but — per an explicit operator ruling recorded in that
same merge commit and confirmed by `[#628]`'s still-`open` status today — **`[#628]` did not
close**, making `CLAUDE.md`'s citation of `[#628]` for the deletion correct while `[#755]`'s
own "closed `[#628]`" summary line is the stale/incorrect claim that should be corrected.
