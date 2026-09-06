---
batch: T
seq: 1
shape: ADR-110 — ONE plan -> N file-disjoint lanes -> ONE integrator. Cut as FOURTEEN by the architect; THIRTEEN contracts frozen, TWELVE dispatched in wave 1 and ONE (3.14) held for wave 2. Lane 3.2 was HELD AT THE DISPATCH GATE on the C-6 quote-vs-intent mismatch and an independent C-8 block, with evidence, rather than launched on a guess.
dispatched: 2026-09-06
status: open
closed_by: docs/audits/2026-09-06-technical-batch-t-close-packet.md
substrate: MIXED — LOCAL (7: gate-dependent or operator-disk-bound, Q1/Q2) · CLOUD (3: read-only reconnaissance, Q3) · CODESPACE (2: repo-mutating and disk-independent, Q4, against the 2-concurrent cap)
---

# BATCH T — THE 2026-09-06 NIGHT BATCH · THE MANIFEST

**This file is the gate-readable manifest**, committed AT DISPATCH and before any lane boots —
the ADR-110 §3 item this batch is being deliberate about. `scripts/batch_manifest.py` resolves an
open batch as the conjunction of four facts: the manifest is TRACKED, `status: open`, `closed_by:`
names a shape that CAN resolve, and that path is ABSENT from the tree. All four hold at the time of
writing.

Authorization: the operator's GO recorded in `DECLARE-GO-2026-09-06.md` §5 — *"GO for the 12–14-lane
night batch … maximum autonomous work while the operator sleeps."* The frozen contract set is
`BATCH-2026-09-06-NIGHT-CONTRACTS.md`; the dispatcher's step-0 evidence is
`to-browser\STATUS-DISPATCHER.md`.

**`<BATCH-ID>` = `T` and `<L>` = `t`, filled ONCE at step 0.** Lane letters `a`–`r` are consumed in
history and `s` is live this window (`lane-s`), so `t` is the next free letter. Batch letter == lane
letter follows the E/F/G precedent.

## THE LANES — 13 committing (12 in wave 1, 1 in wave 2)

Contracts: `docs/audits/2026-09-06-technical-batch-t-launch-contracts/`.

```
L1   lane-t-000-v2-logs               local      opus  no row  logs/ flat retention -- fix the CALLER
L3   lane-t-000-v4-archive-report     cloud      opus  no row  V4 REPORT-STAGE; executes nothing
L4   lane-t-000-v5-closures           cloud      opus  no row  closure proposals + witnesses; closes nothing
L5   lane-t-000-aj-research           cloud      opus  no row  AJ catalogue + deployment-model memo
L6   lane-t-000-nc1-clear             local      opus  no row  undispositioned 36 -> 0, reason per organ
L7   lane-t-000-shape-seal            local      opus  no row  shape-spec DRAFT + corp-monorepo seal REPORT
L8   lane-t-000-batch-p-audit-speed   codespace  opus  no row  batch P: P2/P3/P5 audit-gate speed  [HELD]
L9   lane-t-000-trace-scorecard       codespace  opus  no row  first consumer of the L4 trace store
L10  lane-t-000-reds-spine            local      opus  no row  two REDs -> GREEN; spine predicate named
L11  lane-t-000-playbook              local      opus  no row  PLAYBOOK+ENVIRONMENT re-read; Ch8 section
L12  lane-t-000-readme                local      opus  no row  README to industry standard
L13  lane-t-000-browser-floor         local      opus  no row  browser-seat floor rendered      [HELD]
L14  lane-t-628-v1-release            local      opus  [#628]  V1 release act                   [WAVE 2]
```

**Every local/codespace branch is `worktree-<slug>` and every cloud branch is `claude/<slug>`; all
match their grammar.** The frozen contract's shorthand lane names (`lane-<L>-v2-logs`,
`lane-<L>-42-v3-ecosystem`, `lane-<L>-022a-research`) are **REFUSED** by
`scripts/validate_branch_naming.py` — `LANE_WORKTREE_RE` is `^lane-[a-z]-\d+-<slug>$`, with a
ONE-letter `<letter>` and a **NUMERIC** `<id>`, so `v2`, `42-v3` and `022a` cannot stand as ids. Same
class as batch G's and R5P's deviations: the gate is the authority over the prompt's shorthand.
`000` is the no-row id — twelve of the thirteen lanes discharge no BACKLOG row and file none.

**Only L14 carries a real row id.** `[#628]` is a live `tasks/` row. `#42` and `#71`, which the
contract's §1 step 5 calls "`tasks/` rows", are **INTAKE ids** — see the next section.

## L2 WAS HELD AT THE DISPATCH GATE — the evidence, not the intention

The batch was cut as fourteen lanes. **L2 (`lane-<L>-42-v3-ecosystem`, "`conformance.html` →
MIGRATE per intake #42") was not launched.** C-6 states the branch taken: *"a mismatch between the
quote and the intent below = HOLD this lane + QUESTION file, not a guess."* Two independent blocks
fired, and both come from intake #42's own text rather than from the dispatcher's judgement.

**1 · The Done-when the contract orders pasted into the header is about a different subject.**
`docs/intake/2026-08-23-tech-generated-artifact-currency.md` (`intake-id: 42`) carries its ex-ante bar
under `## Acceptance criteria (ex-ante)`, and those four criteria govern a **currency rule for the
committed-generated artifact CLASS**: a `doc-code-edge.yaml` entry moved from `exempt:` to
`coverage_scope:`, every generated artifact covered by an armed mechanism or carrying a reasoned
exception, `gen_dashboard.py --check` armed, and a deliberately-stale tree producing a signal. The
lane's intent is **migrating one file**. A migration cannot witness any of them, and pasting them in
as a frozen criterion would have bound the lane to a bar its own work could not reach.

**2 · The intake says exactly this, in its own words.** AMENDMENT 2026-09-01(b) §3 closes:

> **No zone-class ruling**, and therefore no discharge of this intake's acceptance criteria.

**3 · And the migration's destination does not exist and may not be created.** Same amendment:

> **No folder is created.** `docs/dashboard/` does not exist, and a Tier-2 ADR-101 genre admission
> is still owed before it may.

so **C-8** ("no new repo folder or path without the operator's approval") blocks the lane
independently of the quote mismatch. The same amendment also records *"No file is moved and no
artifact is retired."*

**Nothing was touched:** `ecosystem/conformance.html` is where it was, no folder was created, and the
lane's footprint is untouched. The ruling needed at dawn is filed as `to-browser\QUESTION-dispatcher-T.md`
item 1 — admit `docs/dashboard/` as an ADR-101 Tier-2 genre (which releases the migration as
written), or re-scope the lane to the class-currency rule its Done-when actually describes. The
amendment notes the same open question is recorded on intakes #38 and #66 as well and is *"the same
question in three places, to be ruled once."*

## THE NAMESPACE CORRECTION THIS BATCH RESTS ON

§1 step 5 of the frozen contract instructs the dispatcher to take Done-when quotes from "`tasks/`
rows #42 (V3), #71 (P)". **Both are INTAKE ids, and following the instruction literally would have
frozen the wrong criterion into a lane header.**

```
#628  tasks/628-dc2-recut-essentials-dissolution-is-a-release-act.md   RESOLVES -- a real row
#42   tasks/42-*.md DOES NOT EXIST
      -> docs/intake/2026-08-23-tech-generated-artifact-currency.md    (intake-id: 42)
#71   tasks/71-reconcile-environment-md-s-claude-directory-tree.md EXISTS and is the WRONG SUBJECT
      -> docs/intake/2026-09-05-tech-batch-p-audit-gate-speed.md       (intake-id: 71)
```

The `#71` case is the dangerous one: the decoy row resolves successfully, so a grep confirms rather
than fails. Had it been followed, lane L8 would have carried an **ENVIRONMENT.md-reconciliation**
Done-when as its frozen, binding criterion for an **audit-gate-speed** build. This is the
cross-namespace collision class recorded in `LESSONS.md` — a locator that resolves into the wrong
sequence produces a confident, well-evidenced, wrong answer.

**Filed, not fixed:** `intake-id: 70` is allocated **twice** —
`docs/intake/2026-09-05-tech-aj-second-pass.md` and
`docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md` — so a bare `#70` on the dawn
ratification list is ambiguous. Renumbering is nobody's lane tonight (a frontmatter id edit REDs the
tree manifest and needs both intake generators). Recorded as `QUESTION-dispatcher-T.md` item 3.

## THE COUPLING SCAN (E-03) — decisions, never silent

**COLLISION 1 — RESOLVED, both lanes launch. L1 vs L9 on `scripts/fleet_health.py`.** Both footprints
name it. The witnessed WRITE is `scripts/propose_closures.py:19` — *"ALWAYS writes
`logs/PROPOSALS-YYYY-MM-DD.md`"* — the sole writer; `fleet_health.py`, `review_closures.py` and
`logs_retention.py` only `glob()` those files. Witnessed write-footprints are therefore **disjoint**,
and `STANDING_RULINGS` **G2** governs: label co-membership does not serialize lanes whose witnessed
footprints are disjoint. Pinned in both headers — L1 writes `propose_closures.py` and treats
`fleet_health.py` as read-only; L9 owns `fleet_health.py`.

**COLLISION 2 — SERIALIZED. L6 vs L7, both add a `docs/intake/` file.** `docs/intake/` is served by
TWO generators and a lane cannot commit an intake without running both: `gen_intake_index.py --write`
(→ `docs/intake/README.md`, hooked by `intake-index-freshness`) and `gen_intake_tree.py --write`
(→ `docs/intake/manifest.json`, whose omission FAILs `audit-health` on `intake_tree_coherence` and
**blocks the commit**). Two lanes would rewrite the same two generated files. **L6 goes first; L7's
intake commit is gated on L6's HANDBACK**, and L7 runs its corp-monorepo seal REPORT — which is
unblocked — meanwhile, so it is not idled.

**NOT a collision, by construction — L3/L4/L5/L7 all land a `docs/audits/` artifact.** `[#590]`
narrowed `audit-index-freshness` on 2026-08-26 to `README.md`/`gen_audit_index.py` precisely because
that file sat in 6 of the last 7 conflicted merges — 86 % of all manual merge resolution in this
repo. **A lane must NOT regenerate the audits index**; the integrator regenerates once on the merged
result. Pinned as an anti-pattern in all four headers.

**HAZARD — L13 would have RED-ed the very test L10 is fixing.** Root holds 8 `.md` files. A ninth,
`BROWSER-SEAT-FLOOR.md` at root, trips both the `fleet_parity` root sweep — which is exactly what
L10 is turning GREEN this batch — and the ADR-101 Tier-1 file class. Compounded by the fact that
intake #68 **names no location** for the file (verified; its cited source
`docs/audits/2026-09-05-technical-browser-seat-notes.md` names none either), which fires L13's own
anti-pattern against inventing a path. **Decision: L13 creates no repo path**; it renders the floor
and its PIN hash to `to-browser\`, where the operator rules the destination at dawn.

**MERGE-ORDER CONSTRAINT, not a serialization — L8 vs L10.** L8 reworks `audit.py`'s git-subprocess
layer; L10 fixes `test_check_fleet_parity` and the spine-anchor check's message. Different files, but
L8 can move verdict-adjacent machinery, so L10 is merged and green before L8 is considered. L8 is
`[ratification-pending]` and merges last regardless.

**HAZARD flagged to L6 — `docs/audits/` is immutable** (critical rule 3). §3.6 asks NC1 to add
citation lines to batch manifests. Only a manifest's `status:`/`closed_by:` frontmatter is a
sanctioned in-place edit; prefer citing FROM the row/intake/register inward over editing a sealed
artifact.

## THE SHIP-GATE AT DISPATCH — measured, git-bash, `PYTHONUTF8=1`

Run at `a39edb2d` before any launch (`audit.py ship-gate`, ran to completion, exit 0):

```
ship-gate: RED -- not shipped-ready (1 hard-fail organ(s); 36 new/undispositioned WARN(s))
[!!] routing_agreement  -- the L0 derived copy diverges from ecosystem/routing-table.yaml:
     adversarial (table: codex) -- the L0 copy mentions the role but not codex beside it
[stale] 4 dispositions matched no live WARN -- exactly the four the operator consented to remove
displayed per organ: consumer_at_landing 22 · funnel_coverage 1 · adr_status_grammar 1
```

The headline totals match the frozen contract's premises exactly (1 hard-fail / 36 undispositioned /
4 stale). **One premise correction:** the contract states `consumer_at_landing` 21; live is **22**,
the extra being `2026-09-05-technical-research-aj-second-pass.md`, which is simultaneously the single
`funnel_coverage` row — one artifact carrying two WARNs, and L6's existing plan covers both legs.

**Wave 2 is gated on this gate going GREEN**, and `routing_agreement` is L6's to clear under operator
consent #6. Per §3.14, if wave 1 ends RED, L14 is not launched and the dispatcher records the
blocking organ in the close packet.

## WHAT THIS MANIFEST DOES NOT DO

- **It closes nothing.** `status: open`; the batch ends when
  `docs/audits/2026-09-06-technical-batch-t-close-packet.md` lands.
- **It assigns no owner** to any unowned item (DECLARE-GO's authorization boundary).
- **It ratifies nothing.** Lanes backed by a DRAFT intake (L8 `#71`, L13 `#68`, L11's second commit
  `027`) HANDBACK `[ratification-pending]` and the integrator HOLDs them off `main` until the
  operator's dawn word.
- **It declares no tag.** The v1.5.0 tag is the operator's act on the checklist, never a seat's.
