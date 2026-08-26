# W2B — surfaces: the boot tax and the merge-conflict tax, both measured and both closed

**Lane:** `worktree-w2b-surfaces` · **Contract:** `~/Downloads/W2B-surfaces.md` (frozen)
**Rows:** `[#589]` (one-line-per-row BACKLOG projection) · `[#590]` (audits index regenerated, never merge-resolved)
**Substrate:** LOCAL worktree, gates armed · **Mode:** commit-and-STOP, no merge
**Evidence base:** `docs/audits/2026-08-26-technical-hub-diagnostic.md` §1 / §5 / §7

---

## 1. What the two rows were worth, measured

Both taxes were quantified by the hub diagnostic before this lane existed; both are now
closed, and the numbers below are re-measured on the landed state rather than restated.

### `[#589]` — the boot tax

`BACKLOG.md` is read by every session that touches the queue. It rendered each row's whole
body while those bodies already lived in `tasks/`, the ADR-107 source of truth — so it was
carrying a second copy of 242 KB.

```
                 bytes      ~tokens (B/4)   rows   mean B/row   max B/row
before         279,814          69,953       202       1,198        3,773
after           66,649          16,662       202         141          222
delta         -213,165         -53,291         0      -88.2%       -94.1%
                 -76.2%          -76.2%
```

**Boot-read saving: ~53,300 tokens per session that reads the file.** For scale, the
diagnostic measures the whole *contracted* boot read at ~30,000 tokens — this one file was
costing more than twice the entire mandated read, and now costs about half of it.

The `[#589]` done-when bar was "under 70,000 bytes on an unchanged `tasks/`": **66,649**.
Nothing is lost — every field the old view rendered is either on the new line or reachable
from the pointer it ends with, asserted per row by
`test_every_projected_row_is_derivable_back_to_its_body`.

The remaining 66 KB is now **57% scaffolding** (38,095 B of theme/story prose) against 28,554 B
of rows. If the file is ever squeezed again, that is where the weight is — the diagnostic §7
Q1 said the same, and it is still true.

### `[#590]` — the merge-conflict tax

`docs/audits/README.md` appeared in **6 of the last 7 conflicted merges — 86% of all manual
merge resolution in this repo**, and was touched 41 times per 300 commits. Not by accident:
the `audit-index-freshness` gate matched every `docs/audits/*.md`, so regenerating the index
was *mandatory* for any lane that wrote an artifact, and under ADR-110 every lane writes one.
Parallel lanes were **required** to collide on one generated file.

The mechanism is proved, not argued, on real git repositories in
`tests/test_audit_index_merge_free.py` — **two negative controls first**, so a green result
cannot be a fixture that never collided:

| # | fixture | result |
|---|---|---|
| 1 | two lanes regenerate, no attribute, no driver | **CONFLICT** on the index (the defect, reproduced) |
| 2 | `merge=ours` attribute, driver **not** configured | **CONFLICT** — the attribute alone is inert |
| 3 | attribute **+** driver armed | **clean, zero manual hunks** — the done-when |
| 4 | after (3) | index is stale by construction; one regen recovers it |

---

## 2. What landed

**`[#589]`** — `128f5093`. `gen_task_tree` gains `render_view` / `project_row` as **siblings**
of `reassemble_from_tree`, never a flag on it: the lossless proof and the lossy projection
must not sit behind one boolean where a caller can get the wrong one by omission.
`--emit-source` writes the view; `--check` grows a size/shape leg and a **losslessness** leg
(before this, leg 3 proved recoverability for free by comparing the reassembly against disk —
dropping that proof silently is how a lossy view stops being recoverable); `--roundtrip` moved
to the tree, because round-tripping the projection still prints `roundtrip ok` while proving
nothing.

The dangerous half was never the renderer. **A gate that greps a row body and is pointed at
the projection finds nothing and reports a clean PASS** — it measures an empty set and calls
it green. Four live checks were in that position. The fix is single-sourced in the new
`scripts/backlog_source.py::canonical_text` (tasks/ reassembly where a tree exists, the file
where none does — the consumer-repo case, which is why it is a function and not a constant).
Re-pointed: `validate_backlog`, `check_routine_consumers`, `preflight_backlog_ids`'s
assertions, `validate_doc_rot`'s two BACKLOG arms, `gen_dashboard`'s intake verdict.

Two gates needed a **scope** change instead: `validate-backlog` now fires on `tasks/` too (a
body edit no longer moves the view, so on the old pathspec it would sit out exactly the
commits that can break the schema), and `check_backlog_filing` scans the `tasks/` diff with
**no regex change** — a task file's body *is* its backlog line, so a new file already emits
the shape it matches.

**`[#590]`** — `be084c91`. Four parts, none sufficient alone: the `.gitattributes` pin; the
**arming** of `merge.ours.driver` (`ours` is not a built-in driver — without the config the
pin does nothing, which is worse than no pin because the tracked file says the problem is
solved); the narrowed pre-commit `files:` pattern, which is what actually removes the lane's
obligation; and the replacement guarantee at ship time.

---

## 3. terra review — two rounds, 2 Critical + 8 High, all fixed

Two rounds, because the round-1 fixes were themselves substantial unreviewed code — and the
second round found a Critical in them. Both tallies are counted from the artifact FILE: the
wrapper's console heuristic printed `0/0/0/0` for round 2 against five real findings.

### Round 1 — tally 1 / 4 / 0 / 0, all fixed

`docs/audits/2026-08-26-codex-w2b-surfaces.md` (`gpt-5.6-terra`, `main...HEAD`). The contract's
bar is ≥ medium; there were no mediums or lows, so everything found is fixed in `HEAD`.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | **Critical** | `_looks_like_view` bypassable by a row whose **title** contains `Done when:` — `--write --force` would then import the projection and overwrite all 202 bodies, through a guard whose own message says "NOT overridable" | **FIXED**, then fixed again: the round-1 replacement (byte-equality, else an end-anchored grammar + per-row budget) was itself Critical — see round 2, findings 1–2. The landed answer carries no shape heuristic at all. |
| 2 | **High** | `audits-index` freshness compares calendar **dates** with a 0-day baseline, so a same-day stale index reads `fresh` — and audits land ~10/day, so the leg would have been blind to essentially every staleness it was registered to catch | **FIXED.** `GeneratedArtifact` gains an optional `content_check`; the audits index declares a regen-and-diff one whose answer **outranks** the date relation. Demonstrated live: the leg printed `CONTENT-STALE … (0d by commit date, which cannot see a same-day drift)`. |
| 3 | **High** | `gen_dashboard` closure history reads historical `BACKLOG.md` revisions, so every post-flip closure would render the "no `Done when:`" fallback and silently degrade release notes to a list of titles | **FIXED.** `_gain_from_task_file` resolves the gain from the row's own `tasks/` file **at the parent revision** (never HEAD, which could resolve a retired slug against a re-slugged tree). Returns `""` on any failure — the pre-existing degraded-row fallback, never a crash. |
| 4 | **High** | `backlog_source` fallback decoded with `errors="replace"` while promising "as-is" — corrupt bytes would become U+FFFD, body markers would vanish, and gates would scan damaged text and PASS | **FIXED.** Strict decode. `routine_consumers`' declared `UnicodeDecodeError` → FAIL arm is reachable again. Newlines are still normalized, or the fix would have introduced a CRLF regression on Windows consumers in the same line. |
| 5 | **High** | Size ceilings bound how *much* comes back but not *what*, so a renderer could append body to every row and stay under them | **FIXED.** An end-anchored grammar leg: a row must END at its `tasks/<file>.md` pointer, so appended material breaks the match outright. |

**Two defects in the fixes were caught by the suite, and both are recorded rather than
quietly corrected.** The first version of the shape leg was **not fence-aware** and reported
`BACKLOG.md`'s own documented row grammar (inside a ``` block) as malformed — caught by
`test_fenced_task_shaped_prose_is_still_legitimate`, a fixture that predates this arc. And a
`Done when:` **text** leg in the gate was a false FAIL on a legitimate title, which meant
`--emit-source` REFUSED to regenerate the very view the gate demanded. Both are gone; the
constants block now records why no row-text signal belongs in either predicate.

### Round 2 — tally 1 / 4 / 0 / 0, all fixed

`docs/audits/2026-08-26-codex-w2b-surfaces-r2.md`, run over `be084c91..HEAD` — the fix diff
itself, which round 1 could not have seen. It was worth running: **the round-1 fixes carried a
Critical of their own**, and the console tally printed `0/0/0/0` against five findings, so the
count is again read from the artifact.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | **Critical** | The replacement predicate folded the **per-row byte budget** into "is this a projection", so a view carrying one over-long row stopped being recognised as one — reopening the same `--write --force` import round 1 had just closed | **FIXED**, and structurally. |
| 2 | **High** | …and the mirror: any full-body row under the budget that happened to cite its task file last **matched**, so `--write` refused a legitimate bootstrap input with no override | **FIXED** by the same change. |
| 3 | **High** | A **raising** `content_check` was swallowed into the date relation — which for a same-day pair says `fresh`, so an index whose exact verification *crashed* would be reported clean | **FIXED.** A failed verifier is `unverifiable` (WARN), distinct from "no verifier declared". The green-by-skip state the field exists to prevent had been reintroduced by the field's own error handler. |
| 4 | **High** | `gen_dashboard` trusted `row.gain` **before** checking for a projection pointer, so a title containing `· Done when: …` would publish title text as the gain | **FIXED.** The pointer is checked first; where a row points at a task file, that file is the authority. |
| 5 | **High** | Normalizing only `\r\n` was **narrower** than the `read_text` it replaced — universal newlines also translates a lone `\r`, so a bare-CR consumer backlog would now be REFUSED where it used to be processed | **FIXED.** CRLF, then any remaining lone CR. |

**Findings 1 and 2 are one defect seen from both sides, and that is the round's real lesson:**
tightening a shape heuristic closes one hole while widening the other, so no amount of tuning
converges. The refusal now asks only questions with exact answers — byte-equality with
`render_view(tasks/)`, else a **generator-owned identity marker** (`_VIEW_MARKER`) emitted by
`render_view` and by nothing else. Shape stays where a false positive is a loud gate message
rather than silent data loss: in `view_problems`.

The marker has one honest failure direction, stated at its definition: strip the line and
`--write` stops refusing. That is strictly better than the shape predicate's, which failed in
*both* directions — and the exact leg still catches the current tree's view regardless, so
stripping it only reaches a view of some *other* tree.

---

## 4. Honest limits

- **The whole-file ceiling is not growth-proof, and is not pretended to be.** The per-row
  ceiling (400 B) is; the whole-file one (100,000 B) is a backstop against wholesale
  regression. Residual: a view can still pass at 100,000 B, which over today's 202 rows and
  37,972 B of scaffolding is a ~307 B/row mean — **2.2× the live 141 B**, and still a quarter
  of the 1,198 B/row a full-body render costs. Re-inflation to body length cannot pass; a 2×
  drift can, and the total ceiling is what eventually catches it. The `[#589]` done-when's
  70,000 bar is asserted separately in the suite, where a point-in-time measurement belongs,
  with its ~23-row headroom stated on the test.
- **`merge=ours` leaves the index stale by construction** — the incoming lane's artifact is
  missing until someone regenerates. That is the mechanism, not a side effect, which is why
  the ship-gate leg and the `/lane-integrate` regen step exist and why it has its own test.
- **Arming is per-checkout machine state.** `merge.ours.driver` is set by `arm_hooks` at
  SessionStart and asserted by `check_hooks_armed`; a checkout that never ran either merges
  with conflicts exactly as before. Client-side, and bypassable like every other local hook.
- **`gen_dashboard.closed_rows_between`** (the fallback path used only when `log_pairs` yields
  nothing) has no revision handle, so it cannot recover a gain from `tasks/`. Fix #3 covers
  the primary path only.
- **A registered spec named ONLY inside a row body is now invisible to the advisory
  undeclared-edge scan** — it left `BACKLOG.md` with the projection, and `tasks/` stays pruned
  because a task file structurally cannot carry a `reconciled_with` edge (its frontmatter is
  templated fresh on every emit). Recorded at the prune's own site.

## 5. Owed, and deliberately not taken here

Both are stale-doc corrections this lane could not land honestly:

1. **`protocols/PLAYBOOK.md`, "Layout (ADR-66 …)"** — still says "the story-map layout above
   is unchanged, it is simply assembled rather than hand-maintained", and the Schema block
   still shows the full-body task bullet as `BACKLOG.md`'s shape. Both now describe the
   CANONICAL text, not the committed file. The contract scopes this lane out of `protocols/`,
   and the file is freshness-gated: a one-line edit owes either a genuine end-to-end re-read
   of a ~105 k-token protocol or a stamp bump that would be a lie.
2. **`CLAUDE.md` §9, the `audit-index-freshness` row** — still says "Fires on ANY
   `docs/audits/*.md` (an add/edit/remove changes the index)", which `[#590]` makes false.
   `CLAUDE.md` is freshness-gated and line-budgeted at 195/200, so a one-bullet edit owes a
   §12 version bullet and a full re-read — a whole act — and it is the known collision file
   across the three sibling lanes live during this session.

## 6. Suite state — 4 pre-existing REDs, none inherited from this diff

Each is proven foreign, not asserted:

| Test | Cause | Proof |
|---|---|---|
| `test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | row `[#348]` crossed the 30-day accretion span organically | reproduces from `git show HEAD:BACKLOG.md` at the lane's base |
| `test_no_gate_hook_or_script_reads_the_export` | `export_backlog_view` appears in `ecosystem/conformance.{md,html}` | reproduces from `git show HEAD:ecosystem/conformance.html` |
| `test_health_ok_with_registered_repo` | invokes `cmd_health` against the LIVE repo | inherits the foreign spine gap below |
| `test_health_stays_ok_with_na_status` | same | same |

**The final push used `git push --no-verify`, and this paragraph is why that is not silent.**
`block_unanchored_push` refused it naming `08b0d192` (Merge branch
`chore/workspace-provider-roots-2026-08-26`) — a **sibling session's merge on local `main`,
made at 23:02 while this lane ran, and not yet pushed**. Proof it is not this lane's:
`git merge-base --is-ancestor 08b0d192 HEAD` answers NO, and the push updates only
`origin/worktree-w2b-surfaces`, introducing exactly one commit with zero merges among them
(`git log --merges --oneline origin/worktree-w2b-surfaces..HEAD` → 0). The hook scanned
`main`'s spine rather than the push range, so a lane branch was blocked by a gap it does not
contain. Sync-merging `main` — the usual lane-lag remedy — would have been the wrong move
here: it would pull the unanchored merge INTO this branch and make it this lane's. The escape
CLAUDE.md §9 names for exactly this is `--no-verify`, kept honest by the `journal_spine_anchor`
audit backstop, which stays FAIL until someone anchors those merges.

**Also integration-owned, and named so it is not mistaken for a regression:** this lane's two
audit artifacts each raise a `funnel_coverage` WARN ("carries no disposition and is not in the
arm-time baseline"). That WARN already stands against roughly thirty artifacts from the last
few days, so these two are not the difference between a green and a red ship-gate — but they
do need a ledger row like the rest. Not filed here: `ecosystem/disposition-register.yaml` is a
shared register that sibling lanes were editing during this session.

**The foreign spine gap.** `journal_spine_anchor` FAILs on `ac677b6e` (Merge branch
`worktree-prompts-revocation`) and, later in the session, also on `d8211b03` (Merge branch
`docs/anchor-prompts-revocation` — the anchor merge `ac677b6e` could not carry, since a merge
cannot name its own hash). Both are a **sibling session's**; `ac677b6e` was already `main`'s
tip when this lane started, and neither is an ancestor of this branch. It is a REAL gap, not
lane tree-lag: the predicate reproduces the same SHAs against `main`'s own `JOURNAL.md`, so a
sync-merge buys nothing. Both commits here therefore carry a declared `SKIP=audit-health` with
that ownership proof in the message. This lane merges nothing and introduces no unanchored
spine entry.

## 7. Environment finding, outside the contract but worth the operator's minute

**A second `uv` (0.12.6, installed 2026-08-25 at `~/.local/bin/uv`) shadows the ADR-106-pinned
0.11.19** (WinGet). Whenever it wins the PATH race, *every* gate in this repo dies with
`Required uv version ==0.11.19 does not match the running version 0.12.6` — `uv run --locked`
is the entrypoint for the whole gate set, so this is not a local nuisance. It was intermittent
within a single session, which is the worst shape for it. Not touched here: ADR-106 makes a uv
bump its own gated change, and this lane pinned the correct binary on PATH instead.
