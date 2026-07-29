# Post-flip stale-procedure audit — text still describing the pre-[#439] workflow

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-29 · **Slug:** postflip-stale-procedure-audit
- **Serves:** the ruled morning fix batch — the pass-11 class ([#442]'s witnessed shape: served text
  describing the pre-flip procedure), swept corpus-wide after the [#439] source-of-truth flip
  (`tasks/` = source, `BACKLOG.md` = generated, 2026-07-28).
- **Arc:** NIGHT BATCH 2026-07-28→29, cloud session, branch `claude/night-2026-07-28-prep-5my46t`.

> **TABLE ONLY — NOTHING FIXED.** Every row is adjudicated input for the operator's morning batch;
> no file listed below was edited by this arc. Line numbers are pinned at branch tip `eb68f3b`
> (the quoted text is the anchor per the anchor-rot rule; PLAYBOOK numbers include the +39-line
> shift from this batch's own [#441] DRAFT block). Cloud caveat: swept without local gates —
> UNVERIFIED-UNTIL-LOCAL.

**Sweep scope:** `protocols/` (all 6) · `docs/` READMEs + intake + decisions README · `.claude/`
(commands, rules, roster, generated) · `plugins/tier1-lifecycle/` (commands, INSTALL, README, script
docstrings) · `templates/` · root living docs (CLAUDE/ARCHITECTURE/VISION/CONTRIBUTING/BACKLOG
header) · `tasks/README.md` · `ecosystem/`. Patterns: direct-BACKLOG-edit instructions ·
line-removal closure wording · `--prune`-as-available · tasks/-as-derived role text ·
source-of-truth claims. Immutable artifacts (ADRs, past audits/handoffs, JOURNAL/LESSONS bodies)
swept for load-bearing procedure only; historical description of the pre-flip world in an immutable
record is CORRECT by construction and listed only where still cited as live authority.

## Adjudicated table

**Verdict key:** STALE = describes the pre-flip procedure as current, would mislead if followed ·
AMBIGUOUS = true-but-shape-blind or self-contradicting within its own file · CORRECT = accurate
post-flip (listed only where a reader might suspect it).

| # | file:line (tip `eb68f3b`) | quoted text (anchor) | verdict | proposed one-line fix |
|---|---|---|---|---|
| 1 | `plugins/tier1-lifecycle/commands/review-closures.md:23-24` | "You perform the BACKLOG edit (the script is read-only); use the **exact** `line` the gate returns as the Edit `old_string` so the removal is exact-match." | STALE-IN-PART — the safety-contract preamble states the unflipped path unconditionally, contradicting the file's own step 4(b); on a flipped host the exact-line Edit is exactly the edit the regen undoes | Reword: "You perform the closure edit (the script is read-only) — on an unflipped host the exact-line `BACKLOG.md` Edit; on a flipped host the step-4(b) `tasks/` retirement." |
| 2 | `plugins/tier1-lifecycle/commands/review-closures.md:90-91` | "**Never** close an unapproved id, never bulk-approve WEAK, never edit BACKLOG without the gate's `close` verdict + exact line." | AMBIGUOUS — on a flipped host you never edit BACKLOG at all; the guard reads as if the edit were the universal mechanism | "…never execute a closure without the gate's `close` verdict (on an unflipped host, its exact line)." |
| 3 | `plugins/tier1-lifecycle/scripts/review_closures.py:23` (docstring) | "Emits the exact verbatim task line so the agent's removal Edit is exact-match" | AMBIGUOUS — docstring describes the unflipped consumption only; on a flipped host the line is identification, not an Edit target | Docstring: "…so the agent's removal Edit (unflipped host) is exact-match; flipped hosts use it to identify the task to retire." |
| 4 | `protocols/PLAYBOOK.md:1354-1357` (Ch8, shared-canonical-files) | "Don't have each branch delete its own task line; leave the removal to the Tier-1 closure loop … The edits §3 serializes are BACKLOG **adds / grooming** (and id allocation at write-time) — not removals." | STALE wording, sound principle — post-flip a branch *cannot* usefully delete a task line (regen restores it), and adds/grooming/id-allocation happen in `tasks/`, not `BACKLOG.md` | "Don't have each branch retire its own row; removal travels the closure loop (manifest node out + regen). The edits §3 serializes are `tasks/` adds/grooming + id allocation." |
| 5 | `protocols/PLAYBOOK.md:3205` (§10 opening) | "`BACKLOG.md` is the single canonical source for ALL pending items across sessions." | STALE — contradicts §10's own flip-aware Layout paragraph (`:3216`) and the generated-file banner; the hub source is `tasks/` | "The task queue (`tasks/` source on the hub; `BACKLOG.md` its generated rendering — consumers unflipped) is the single canonical home for ALL pending items." |
| 6 | `protocols/PLAYBOOK.md:3256` (§10 per-handoff grooming step 3) | "Prune obvious dead items (completed, no longer relevant)" | STALE — "prune" as a direct grooming act on the file; post-flip pruning-by-edit is undone by regen, and `--prune` is refused; the departing *browser* can't edit files anyway (the step describes what it directs CC to do) | "Flag obvious dead items for the closure loop / a `tasks/` retirement — never a direct `BACKLOG.md` edit." |
| 7 | `protocols/PLAYBOOK.md:3258` (§10 per-handoff grooming step 5) | "**Remove** completed items — they leave the file (the closing commit + the per-session JOURNAL entry are the record, ADR-65)" | AMBIGUOUS — ADR-65 principle intact; the imperative "remove" now resolves to retire-in-`tasks/`+regen on the hub, unstated | Append: "(on the hub: retire in `tasks/` — manifest node out, terminal `status:`, `--emit-source`; the row leaves as a result)." |
| 8 | `protocols/PLAYBOOK.md:3268,3270` (§10 quarterly steps 1,3) | "Confirm **no `done` items remain** …" / "Remove items that no longer align with VISION" | AMBIGUOUS — same class as row 7: outcome language correct, mechanism unstated post-flip | One shared clause pointing at `tasks/README.md` as the removal mechanism on the hub. |
| 9 | `protocols/PLAYBOOK.md:3278` (§10 split-brain prevention) | "BACKLOG.md is the single source of truth." | STALE — the flip's exact inversion; on the hub `BACKLOG.md` is the generated surface and `tasks/` is the source | "The task queue is single-source (`tasks/` on the hub; `BACKLOG.md` on unflipped consumers) — handoffs must NOT duplicate it." |
| 10 | `.claude/commands/changelog-review.md:96` | "add `closes [#113]` and remove #113 from BACKLOG in the same commit." | STALE — instructs a direct BACKLOG removal; on the hub that edit REDs the coherence gate and regen restores the row | "…add `closes [#113]` and retire #113 in `tasks/` (node out + terminal status + `--emit-source`) in the same commit." |
| 11 | `protocols/AI_COUNCIL_PROCESS.md:374-375` | "**BACKLOG follow-up** — if the ADR closes a BACKLOG item, mark it closed in the same commit (or a follow-on commit)." | STALE twice — "mark it closed" predates even ADR-65 (done items LEAVE, no status marker), and post-flip the leave is a `tasks/` retirement; the neighbouring "add the new BACKLOG entry" (`:376-377`) is also a `tasks/` add now | "…if the ADR closes an item, route it through the closure loop (`closes [#id]` + retirement per `tasks/README.md`); new follow-up work is a `tasks/` add with `Refs: ADR-NN`." |
| 12 | `protocols/SESSION_SETUP.md:213` | "After session, append new items or update status via per-handoff grooming" | STALE — "update status" was never the ADR-65 shape (no status field in the queue; done items leave) and "append" post-flip means a `tasks/` add + regen | "After session, file new items (a `tasks/` add on the hub) or close via the closure loop — per-handoff grooming (PLAYBOOK §10)." |
| 13 | `protocols/HANDOFF_PROCESS.md:546-547,552` (§14a epic return) | "**Proposed BACKLOG delta** (structural changes for the architect to apply — the BACKLOG-single-writer-for-structure ruling, ADR-97)" / "applies the backlog delta" | CORRECT-AMBIGUOUS — single-writer + propose-only survive the flip untouched; "applies" now means a `tasks/` edit + regen on the hub, which the spec leaves implicit (spec edit = a v5.8/v6 ride-along, not a hotfix — route to the intake #18 session, A10's batch) | Optional clarifier at the next version bump: "applied per the queue's shape (`tasks/` + regen on a flipped host)". |
| 14 | `templates/CONTRIBUTING-md-template.md:67,74` | "pairs with the item leaving `BACKLOG.md` in the same or a following commit." | CORRECT — consumer-facing template; both consumers are UNFLIPPED (the flip is hub-only, ADR-107 step 3 executed for the hub tree), so the direct-edit shape is their live truth. Revisit at consumer flip time, not now | none (note: template inherits a flip-conditional clause when a consumer flips) |
| 15 | `CONTRIBUTING.md:58,65` (hub copy) | "pairs with the item leaving `BACKLOG.md`…" / "fails any commit that removes a `- [#id]` task from `BACKLOG.md` without referencing that id" | CORRECT — outcome/diff-keyed wording holds post-flip: the regenerated `BACKLOG.md` loses the line in the closing commit, so both the pairing and the commit-msg hook still key correctly | none |
| 16 | `.claude/methodology-roster.md:33` (generated) | "backlog-id-on-close — commit-msg gate; require [#id] when a BACKLOG task line is removed" | CORRECT — diff-keyed, still fires on the regen's line removal; file is generated (any wording change goes to `deploy/manifest-v*.yaml`, never hand-edited) | none |
| 17 | `plugins/tier1-lifecycle/scripts/propose_closures.py:13-14,28-29` (docstring) | "is still present (open) in BACKLOG.md. The closing commit fired but the item was never removed" / "NEVER mutates BACKLOG" | CORRECT — reads the generated surface, which faithfully mirrors the source; read-only contract unchanged | none |
| 18 | `templates/handoff/02_METHODOLOGY.md.tmpl:92` | "BACKLOG removal via the closure loop" | CORRECT — mechanism-agnostic, matches both shapes | none |
| 19 | `protocols/PLAYBOOK.md:1638` (Ch9) + `tasks/README.md` + `ARCHITECTURE.md:616-627` + `BACKLOG.md:2-3` banner | (flip-aware post-conformance text) | CORRECT — listed as the conformed reference set the fixes above should point at, not duplicate | none |

## Not-findings (checked, clean)

- **`--prune`-as-available:** zero live surfaces describe `--prune` as usable. Every live mention is
  the refusal (`tasks/README.md:38`, `ARCHITECTURE.md:627`, `review-closures.md:64`, ADR-107 §6.3
  discussion). The prompt's `--prune-as-available` pattern has no live instance.
- **`tasks/`-as-derived role text:** zero live instances — `ARCHITECTURE.md:18` and `tasks/README.md`
  both carry the "arrow used to point the other way" retirement note.
- **CLAUDE.md §9 hook lines** (`backlog-id-on-close`, `backlog-filing-backpressure`) — diff-keyed
  wording, correct under regen (same reasoning as rows 15/16).
- **Immutable trees** (`docs/decisions/ADR-*.md` incl. ADR-65/66/70, past audits, handoff bundles,
  JOURNAL/LESSONS bodies): pre-flip descriptions are historical record; ADR-65's amendment is
  carried by ADR-107 (recorded in ADR-107 §6.3 + `docs/decisions/README.md:96`) — no in-place ADR
  edits owed, no amendment-marker gaps found.

## Morning-batch notes (for the ruled fixes — not executed here)

1. Rows 1–3 (plugin surfaces) re-open the [#442] neighbourhood: fixing the repo copy does not refresh
   a stale plugin **cache** — a fix batch should bump the plugin patch version or note the cache risk
   (the [#444] release procedure), or the served text stays pre-fix in live sessions.
2. Rows 6–9 + 12 sit in freshness-carrying files (`SESSION_SETUP.md` is in the hub-only freshness
   set; PLAYBOOK carries "Last updated") — batch the edits with their genuine re-read stamps.
3. Rows 5/9 and the flip-aware `:3216` should converge on ONE source-of-truth sentence to avoid the
   §10-internal contradiction surviving in softened form.
4. Row 13 is deliberately routed to the intake #18/[#435] session (spec version discipline) rather
   than the fix batch.
