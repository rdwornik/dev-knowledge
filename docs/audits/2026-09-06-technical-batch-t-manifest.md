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
L15  lane-t-000-freshness-unstamped   local      opus  no row  seven unstamped canonical docs   [AMENDMENT 1]
```

> **The `L15` row is ADDED BY AMENDMENT 1** (see the amendment section at the foot of this file);
> the thirteen rows above it stand byte-identical to the dispatch-time freeze. The row lives inside
> this fence rather than only in the amendment because this table is a **machine surface**, not
> prose: `batch_manifest.manifest_lane_slugs` reads the FIRST `## THE LANES` block and stops at the
> next heading, and `batch-manifest-contract-slug-agreement` ([#630]) requires **set equality both
> ways** between these slugs and the launch-contracts directory. A lane recorded only in an
> amendment section would be a lane the teardown and the ADR-110 exemption cannot see — which is the
> measured batch-E defect that predicate exists to catch.

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

---

## AMENDMENT 1 - 2026-09-06 - lane 3.15 added; batch width 13 -> 14 contracts

**This is an in-file amendment marker, not an edit of the record above.** `docs/audits/` is
immutable (critical rule 3); the sanctioned forms are a superseding file or an in-file amendment
marker, plus a manifest's `status:` / `closed_by:` frontmatter. Everything above stands as frozen at
dispatch. This section ADDS.

**Authority.** `AMEND-BATCH-T-001.md` A3 (architect, within the seat that froze
`BATCH-2026-09-06-NIGHT-CONTRACTS.md`; operator consents unchanged). Applied by `dispatcher-T` on the
operator's instruction to add the lane to this manifest, to STATUS and to the close packet.

**The defect this lane closes - found by the integrator, confirmed by the architect as "the
contract's own error".** Wave-1 ship-gate GREEN was **unreachable by construction**:
`canonical_freshness` reports a `derived ungated-and-unstamped` line naming **eight** files, and no
lane at any wave owned any of them. Section 3.6 forbids NC1 from touching `canonical_freshness`;
section 3.14 re-stamps `CLAUDE.md` but launches only on GREEN - a circular condition. Wave 1 would
have ended RED whatever every lane did, and lane 3.14 would never have launched.

### L15 - the added lane

```
L15  lane-t-000-freshness-unstamped   local  opus  no row  seven unstamped canonical docs, really re-read
```

Branch `worktree-lane-t-000-freshness-unstamped`. **Its frozen contract is NOT in this
directory, and could not be put there.** Contract of record, which is the file the lane actually read
and executed: `<PROMPTS_DIR>/to-cc/LANE-t-000-freshness-unstamped.md`, 17211 bytes, sha256
`2d628f6d14a02986b860c65625193db872c9c588b526633d304da35ec8e0023a`. Recorded by hash because it is
verifiable by hash; the operator's copy is the authority, not a restatement of it here.

**Why it could not land, measured rather than assumed.** `[#630]`
`batch-manifest-contract-slug-agreement` compares this manifest's lane roster against the contracts
**in the CHANGESET**, not against the contracts on disk
(`gen_lane_contract.py::_check_manifest_contract_agreement` -- "`contracts` (the paths `check` was
given)"). Batch T's other 13 contracts landed together in the freeze commit and are unchanged since,
so `git add` cannot re-stage them: there is no diff to stage. Every ordering therefore refuses.
Contract alone -> the manifest names 13 slugs it cannot see. Contract plus this amendment -> the
manifest names 14 and the changeset holds 1. Both directions were attempted and both refused, with
the refusal naming the other thirteen. This commit lands the manifest amendment ALONE, which the
predicate skips (0 contracts given -> "0 checked"), and no gate was bypassed to do it.

**This is a predicate GAP, not a lane defect, and it is a dawn item.** `[#630]` is scoped "at
freeze" by its own docstring and does exactly what it was built for. Adding a lane AFTER freeze is
outside that scope, and the amendment path is the sanctioned way to add one, so the two are simply
not composed. The sharper form of the same gap: **lane 3.15's WORK merged at `0d2db2f7` while its
contract never landed, and `[#630]` cannot see that either** -- a lane whose work merges without its
contract is invisible to a predicate that only compares against the changeset. Tonight the
launch-contracts directory holds **13 contracts for 14 executed lanes**, and the manifest above is
the only in-tree surface that says so.

Recorded alongside it, found while diagnosing: `.pre-commit-config.yaml` `lane-contract-check`
carries a comment asserting "`always_run: true` + `pass_filenames: false` (lane-g-630, [#630])",
but the hook body sets `always_run: true` and a `files:` glob and **does not set
`pass_filenames: false`**. The comment describes an every-commit repo-wide gate; the configuration
implements a staged-files gate. The behaviour above is the configuration's, not the comment's. Which
of the two is intended is a question for dawn, and it decides whether this gap is a bug or a scope.

**Footprint (seven files):** `AGENTS.md` - `protocols/AGENT_FRAMEWORK.md` -
`protocols/FUNNEL_LIFECYCLE.md` - `protocols/HANDOFF_PROCESS.md` - `protocols/README.md` -
`protocols/REPO_ONBOARDING.md` - `protocols/STANDING_RULINGS.md`.

**Coupling scan, run before launch as A3 requires - DISJOINT.** None of the seven is touched by any
other wave-1 lane. The five files deliberately NOT in scope, and who holds them:

```
protocols/PLAYBOOK.md            L11 lane-t-000-playbook
protocols/ENVIRONMENT.md         L11 lane-t-000-playbook
protocols/OPERATOR-INTERFACE.md  L6  lane-t-000-nc1-clear   (per A2 below)
protocols/HANDOFF_BOOT.md        NOBODY - excluded by ruling
README.md                        L12 lane-t-000-readme
```

**`protocols/HANDOFF_BOOT.md` is excluded and stays unstamped tonight.** Its sha256 is the ROLE PIN
every browser seat carries in project knowledge and in the bundle, so stamping it is a
curated-baseline touch (C-3 class (a)) that breaks every booted seat until the operator re-uploads
the file. Measured at `a39edb2d` by L13:
`3b6d5691294e149844e16a2965d27ff49d2e95e3a69d138f6f77a33ecdef5858`. **Before -> after is therefore
`unstamped 8 -> 1`, and the remaining 1 is correct, named and expected** - not a shortfall.
Dawn-list item: stamp it in the next window together with a PIN re-issue.

### The other four legs of AMEND-BATCH-T-001

- **A1 - lane 3.14's launch condition, RE-ISSUED.** It now launches on `PACKET-MERGED wave-1 @ <sha>`
  **AND** hard-fail = 0 **AND** every remaining undispositioned WARN being a `canonical_freshness`
  line naming only `CLAUDE.md` (which 3.14 re-stamps in the same act) and/or
  `protocols/HANDOFF_BOOT.md`. Any other surviving WARN and 3.14 is not launched, with the blocking
  organ recorded **by name and file** so dawn does not misread RED as NC1 having failed. This
  supersedes the `ship-gate GREEN` condition recorded above.
- **A2 - lane 3.6 gains one act:** after declaring the `reconciled_with:` edge on
  `protocols/OPERATOR-INTERFACE.md`, NC1 also re-stamps it. Delivered to the lane as
  `ADDENDUM-lane-t-000-nc1-clear-A2.md` - additive, withdrawing nothing, because an amendment that
  NARROWED a frozen contract would have to be re-issued through `gen_lane_contract` rather than
  annotated (`validate_substrate::RULE_AMENDMENT_SUBTRACTS`).
- **A4 - lane 3.8 merge order.** Any text reading "3.8 merges LAST regardless" is void where it
  conflicts with DECLARE-GO's authorization boundary: 3.8 HANDBACKs `[ratification-pending]` and the
  integrator HOLDs it. The integrator's reading stands.
- **A5 - count premise:** `consumer_at_landing` live 22, not 21, exactly as recorded above.

### What this amendment does NOT change

Operator consents (the `routing_agreement` render; the four `[stale]` lines; V4 report-stage), the
HOLD boundary for DRAFT-backed lanes, the tag remaining the operator's own act, lane 3.2's HOLD, and
every other section 0-4 clause of the frozen contract.
