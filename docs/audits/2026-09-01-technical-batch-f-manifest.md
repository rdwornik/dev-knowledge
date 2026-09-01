---
batch: F
seq: 1
shape: ADR-110 — DERIVE -> architect's cut -> FREEZE -> DISPATCH; 7 committing lanes (1 codespace ATTENDED + 6 local). No read-only tier; the derivation did that work.
dispatched: PENDING — FROZEN 2026-09-01, awaiting the operator's dispatch
status: open
closed_by: docs/audits/2026-09-02-technical-batch-f-close-packet.md
substrate: CODESPACE (1, L1 attended proof-of-work) + LOCAL (6)
---

# BATCH F — SUBSTRATE, DEBT AND THE TWO RULED PREDICATES · THE MANIFEST

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves an open batch as
the conjunction of four facts: the manifest is TRACKED, `status: open`, `closed_by:` names a shape
that CAN resolve, and that path is ABSENT from the tree. All four hold.

**FROZEN IS NOT DISPATCHED.** `dispatched:` says `PENDING` on purpose. Batch E wrote a date there
at freeze and the two acts collapsed in the record; here they do not. The ADR-110 exemption arms
the moment this file is committed, which is intended — it covers lane merges — but no lane has run.

**ON `closed_by:` AND ITS DATE.** The path is declared at FREEZE, before the close date is
knowable, because a manifest carrying no `closed_by:` opens nothing at all: an exemption that
cannot expire is not an exemption. **The packet lands at THIS path.** If the batch closes on
another day, the real close date is recorded INSIDE the packet — the filename is the identifier
the exemption keys on, not a claim about when the work stopped.

## THE LANES — 7 committing, frozen 2026-09-01

Contracts: `docs/audits/2026-09-01-technical-batchf-launch-contracts/`.

```
L1  lane-a-1-codespace-pow-and-router-adr    codespace  ATTENDED  opus    F0
L2  lane-b-2-handoff-v7                      local                opus    F1 · [#611]
L3  lane-c-3-logs-retention-callers          local                sonnet  F3 · [#626]
L4  lane-d-4-deploy-waiver-honoring          local                opus    F4 · [#276]
L5  lane-e-5-vision-relocation               local                opus    [#621]
L6  lane-f-6-agy-admission                   local                opus    [#627]
L7  lane-g-7-contract-validator-predicates   local                opus    [#629] + [#630]
```

**Every branch is `worktree-<slug>`, L1 included.** A codespace lane commits and pushes like a
local lane, merely elsewhere, so `claude/` would name a branch nothing creates (R-ENUM leg 3,
2026-08-31). Off-machine and cloud are different axes. All seven match `LANE_BRANCH_RE`
(`^worktree-lane-[a-z]-\d+-<slug>$`), so the teardown and the ADR-110 exemption both see all seven
— which is the defect batch E's first cut had and this one does not.

**THE MANIFEST'S LANE ENUM AND THE CONTRACT SLUGS ARE IDENTICAL, AND THAT WAS CHECKED.** Batch E's
integrator defect (b) was a slug renumbered between draft and dispatch — `lane-b-2` in the manifest
against `lane-b-3` dispatched — with nothing comparing the two. `[#630]` exists to make that a
predicate; until L7 builds it, the check was run BY HAND at this freeze, both directions, and the
sets are equal.

## THE FREEZE GATE — run 2026-09-01, over all seven contracts

```
scripts/gen_lane_contract.py check   (Layer 1, shape)
  7 of 7 OK — sections, shape/command agreement, slug->branch derived exactly once

scripts/validate_substrate.py        (Layer 2, declaration-vs-content, ALL SEVEN rule ids)
  7 contract(s): OK — substrate declaration agrees with content
  REFUSE findings: 0     WARN findings: 0     recorded deviations: 0
```

**ZERO DEVIATIONS, AND THAT IS A RESULT RATHER THAN AN ABSENCE.** Batch E froze with two overridden
WARNs. This batch has none because the one intersection the cut would have produced was designed
out: **L5's write-scope and L2's would both have claimed `protocols/HANDOFF_PROCESS.md`,
`HANDOFF_BOOT.md` and the two `.claude/commands/handoff*.md`** — the VISION pointers those files
carry are in `[#621]`'s measured collateral set AND in the files L2 rewrites for v7. Rather than
record a deviation on `substrate-lane-write-scope-disjoint`, the four files were moved into L2,
whose done-contract now owns re-pointing them. They are stale TODAY, independently of the
relocation, so L2 is their honest home and no ordering constraint is created.

**ON "ALL SEVEN PREDICATES", PRECISELY.** `validate_substrate.RULE_IDS` is a closed set of SEVEN
live rule ids — `substrate-no-live-verb`, `substrate-cloud-gate-dependent`,
`substrate-offmachine-operator-path`, `substrate-second-local-writer`,
`substrate-teardown-enum-coverage`, `substrate-lane-write-scope-disjoint`,
`substrate-unknown-override` — and the freeze ran every one. **`[#629]`'s
amendment-cannot-subtract predicate would be an EIGHTH**, and it does not exist yet; L7 builds it.
Until it does, its RULE was applied by hand here: **no contract in this batch contains an act any
ruling has subtracted**, because every contract was generated fresh rather than amended. That is
the discipline the predicate will mechanise, stated so the gap is visible rather than assumed.

**The commit-time sweep grandfathers by arm date; the FREEZE does not.** `validate_substrate` run
directly, as above, applies every leg with no date grandfather at all.

## MERGE ORDER

```
1.  L1   codespace PoW + ADR-117.  FIRST and ATTENDED -- a green PoW flips the
         substrate default for the committing lanes of THIS batch, so running it
         late means re-cutting the batch.
2.  L2 · L3 · L4 · L6 · L7   disjoint write-scopes; any order, any parallelism.
3.  L5   after L2, by preference not by constraint: L2 re-points the four handoff
         VISION pointers, and landing that first means L5 never sees a stale one.
         Nothing breaks in the other order.
```

**L4 is on the critical path to the monorepo GO**, not beside it: `[#276]` gates BOTH consumer
instantiations, and it was UN-DEFERRED 2026-09-01 on its own peg (an arc claimed it; the operator's
standing mandate re-prioritised it).

## THE JOURNAL ANCHOR

Every lane branch here matches `LANE_BRANCH_RE`, so the ADR-110 exemption covers every lane merge
while this manifest is open — batch E's forced pre-anchor, which existed because DM-4 ran on
`claude/`, is **not needed**. What IS needed is the thing batch E nearly got wrong: **the exemption
is a deferral with a published expiry, and it dies the moment the close packet lands.** Anchor the
lane merges BEFORE the packet, not after. Batch E's spine was clean at close only because entry (r)
anchored four exempt merges hours ahead of the packet; had it not, the closing commit would have
wedged every commit in the repo.

## EX-ANTE COST, from measured batch-E numbers

```
integration full suite      17m23s   MEASURED 2026-09-01 (4772 passed / 12 failed)
per-commit pre-commit gate  ~4 min   measured repeatedly this window
audit.py health alone       ~200 s   the dominant term inside that gate

7 lane merges      x ~4 min  =  ~28 min
2 anchor/JOURNAL commits     =   ~8 min
1 integration suite          =  ~17 min
                                -------
integration overhead alone      ~53 min, EXCLUDING every lane's own execution
```

**`[#528]` is open and uncomputed** — *"the full suite multiplied by per-lane + per-merge runs is
the real batch cost"* — so the per-lane half of this model does not exist yet. The figure above is
the integrator's cost, not the batch's, and it is stated that way rather than presented as a total.

## REFUSE-TO-FINISH

The batch does not close while any item is open: every lane merged or explicitly abandoned with a
reason, every worktree removed AND its removal VERIFIED, every branch deleted **locally and on
origin**, L1's receipt harvested, and the close packet landed at the `closed_by:` path above.
Removing `status: open` before that is closing the batch by assertion.

**Two teardown lessons batch E paid for, carried forward here rather than re-learned:**

1. **A live lane session can outlive its own worktree.** Batch E's DC-3 session held an empty
   directory after `git worktree remove` had already succeeded — `git worktree list` was clean
   while `rmdir` returned *"Device or resource busy"*. Verify the DIRECTORY is gone, not just the
   registration.
2. **A branch is a teardown target, not storage.** Batch E kept `worktree-lane-b-3` alive to hold
   an artifact. The artifact now lives at
   `docs/audits/2026-09-01-technical-act-one-preserved.md` and the branch is deleted. If a lane
   here produces something worth keeping, it becomes an artifact, not a branch.

## CARRIED, AND DELIBERATELY NOT IN THIS BATCH

```
F5      ARCHITECTURE slice 2 -- DEFERRED TO G. Slice and re-read are ONE act, and L5 is
        already spending this batch's ARCHITECTURE.md re-read budget.
[#628]  ESSENTIALS dissolution -- DEFERRED TO G, after the v1.5.0 tag. A floor edit is a
        release act by construction (release_lint C5's three-way hash equality).
F2      the distiller BUILD -- DEFERRED TO G. F2 is RE-DECIDED as TIER L (ADR-112's guard:
        "Tier S never touches gates"), so this batch produces no distiller work at all;
        the design lane that writes G's build contract is G's, not F's.
ASSET   two Shutdown codespaces (batche-c-admission-*, animated-dollop-*) -- DELETE BOTH
        after L1 creates its own. Neither accrues compute billing while stopped.
```

**Then, in the operator's order:** v1.5.0 tag (operator) -> monorepo instantiation (attended GO).
Ex-ante numbers ride the GO; terra tallies ride the close packet.

---

## AMENDMENT 1 — 2026-09-01, BEFORE DISPATCH: L2 REISSUED on the operator's F1 contract

> **In-file amendment marker** (CLAUDE.md §5 rule 3). The batch is FROZEN and **not dispatched**
> (`dispatched: PENDING`), so this is a **re-freeze**, not a change under a running lane.

The operator issued the F1 contract after the first freeze. **L2 was REISSUED — regenerated from
`gen_lane_contract emit` and re-filled — not amended.** That is `[#629]`'s own rule applied to the
batch that files it: *an amendment cannot subtract or replace an act; a split or re-scoped ruling
REISSUES the contract through the validator.* Annotating a frozen contract with "actually, do this
instead" is exactly the shape that made batch E's DC-3 execute a ruled-out act.

**F1 is now the BOOT-INVERSION carrier, `/boot-session`**, not merely a version bump:

```
bundle    sections GENERATED from live state -- funnel health · north-star arcs + priorities ·
          rot/orphans from funnel_lifecycle · open asks · PROPOSED NEXT BATCH (decision-tree
          ranked, ledger-bounded) + ONE hand-written RESIDUAL for judgment. ROLE PIN 7.0.0;
          a v6 bundle is REFUSED.
organ 1   .claude/commands/boot-session.md -- repo-level, deploy-carried. It NARRATES.
organ 2   a one-line FUNNEL HEALTH digest on SessionStart -- EXTENDING an existing tripwire,
          never a fifth rival.
library   scripts/boot_frontier.py -- the frontier (rustworkx topological order), the scoring
          seam and batch selection under disjointness/width/ledger. The hard part is importable
          and testable; a prompt that computes a frontier is a frontier nobody can test.
```

**Three things were VERIFIED before they became contract text, and two of them changed it:**

- **`rustworkx` is ALREADY a declared dependency** — `pyproject.toml` carries it for FPG-1 on the
  operator's A3 mandate, from a prebuilt wheel, hash-pinned in `uv.lock`, numpy cost stated. **F1
  adds no dependency**; the contract says REUSE, and would have said "add" if nobody had looked.
- **`SessionStart` runs five hooks, not four** — four surfacing organs plus `arm_hooks`. The
  ruling's *"extend the existing four tripwires, never a fifth rival"* resolves to
  `scripts/fleet_health.py`, which already prints a one-line digest and already carries the
  overdue-groom escalation. Named as the measured natural host, with the lane told to confirm
  against live docs rather than trust this line.
- **BOOT-R1's survey is still RUNNING**, so the scoring rule is a **declared seam pinned later**,
  not a model invented to fill the gap. AUT-R1 landed and is cited by path for the bounding rules.

**ONE WRITE-SCOPE MOVED, AND L5 WAS REISSUED FOR IT TOO.** L2 needs
`deploy/manifest-v1.5.0.yaml` to declare two new deploy-carried organs; L5 had claimed it for a
one-line archival-note correction. **One file, one owner** — leg 6 would have REFUSED the pair.
The correction moved into L2's done-contract. Removing a file from L5's frozen scope is a
SUBTRACTION, so L5's contract was rewritten rather than annotated, on the same rule as L2.

**Re-run at re-freeze, over all seven:**

```
gen_lane_contract.py check   7 of 7 OK
validate_substrate.py        7 contract(s) OK — 0 REFUSE, 0 WARN, 0 deviations
[#630] hand-check            manifest slug set == contract slug set, both directions
```

The lane table above is unchanged: L2's slug, branch and substrate are identical, so the manifest
and the contracts still agree. Only the contract's content moved.

---

## AMENDMENT 2 — 2026-09-01, AT THE GO: every lane gets a review lane, and the report that forced it

> **In-file amendment marker.** **ADDITIVE** — it adds a requirement to all seven lanes and
> subtracts nothing, so no contract is reissued (`[#629]`'s rule binds subtraction, not addition).
> The batch is still `dispatched: PENDING` at the time of writing.

**THE REPORT, ASKED AT THE GO: which lanes would run without a review lane? ALL SEVEN.**

As frozen, no contract in this batch names a reviewer, and this manifest declares no review lane.
Every contract's Steps end at *"pytest green, one end-of-lane artifact, COMMIT, then STOP"*. **The
freeze predates the rule**, and reporting that is cheaper than discovering it at the seventh merge.

**The rule exists because the measurement is now in the tree.** ATLAS-R1's usage ledger
(`docs/audits/2026-09-01-census-atlas-r1-def-usage-ledger.md`) counts, across batches D and E:

```
merged lanes        17
  terra reviewed     6
  pre-merge reviewed 2
  NO REVIEW          9      batch D: a · b · d · g   (the whole batch has no review record)
                            batch E: DC-1 · DC-4 · DM-3 · DM-5 · HY-1
```

and names the cause as a **process defect, not a reporting one** — the lanes were
integrator-verified, which is real, and is not independent review.

**THE REQUIREMENT, binding all seven:**

1. **No lane merges without a review lane.** Each lane's diff takes a terra pass **BEFORE** its
   merge — `codex exec -m gpt-5.6-terra --sandbox read-only`, scoped inside the focus prompt
   (`--base` and a prompt are mutually exclusive), classifying each finding as *(a) a real defect
   with an exact fix* or *(b) a design tension to record*.
2. **PRE-merge, deliberately.** Batch E's round ran post-merge and its own artifact calls that the
   weaker position. The whole content of this rule is moving the review to where it can still
   refuse something.
3. **The tally goes IN the close packet**, per lane, including CLEAN and including **refutations
   recorded as prominently as acceptances** — one of batch E's findings had a false premise and
   saying so is the point.
4. **A CLEAN pass is a review.** The requirement is that a review HAPPENED, not that it found
   something; a reviewer that must find a defect will invent one.
5. **A lane that changed no code still gets one.** DM-3 and DM-5 were excused by that reasoning in
   batch E and appear in the unreviewed nine regardless — a drafting lane's artifact is exactly
   where an unchallenged claim survives.

**EX-ANTE COST OF THE ADDITION, stated rather than absorbed.** A terra pass measures **~11 min**,
and terra is a **loop, not a check** — findings narrow across passes and one pass is not a review.
At 1–2 passes per lane:

```
7 lanes x 1 pass  x ~11 min  =  ~77 min
7 lanes x 2 passes x ~11 min =  ~154 min
```

against the ~53 min of integration overhead this manifest already prices. **The review round is
therefore the largest single line in the batch's integration cost, and it roughly triples it.**
That is the honest number, and it is the trade the rule is making.

---

## AMENDMENT 3 — 2026-09-01: L1's first dispatch, its receipt, and all seven lanes REISSUED as sonnet

> **In-file amendment marker.** Records a dispatch that happened and its outcome; the reissue is
> recorded here, and the contracts themselves were regenerated rather than hand-edited.

### L1's first dispatch — RED at the receipt, and the receipt's message was FALSE

```
codespace          lane-a-1-codespace-pow-and-router-vgrj967wg653j   (created, not rebuilt)
RemoteExitCode     91   -- the module's OWN guard: "claude is not installed in this devcontainer"
Ok / is_error      NOT CAPTURED BY THIS SEAT. The dispatch ran from the operator's trigger and
                   its result object did not reach this session. Recorded as not-captured rather
                   than inferred -- and note the guard's receipt carries `{"error": ...}` with NO
                   `is_error` field at all, so the contract's own receipt-gate leg
                   `is-error-false-not-subtype-success` reads a MISSING field on a 91, not a
                   `true` one. That is a second, smaller defect in the same area.
verdict            RED, and the message was the WRONG DIAGNOSIS
```

**Diagnosed IN the live container while it billed, then stopped.** Two commands, one connection:

```
gh codespace ssh -- 'command -v claude'             -> rc=1, NOT FOUND
gh codespace ssh -- 'bash -lc "command -v claude"'  -> /home/vscode/.local/bin/claude
non-login PATH: /usr/local/python/current/bin:...:/usr/local/bin:/usr/bin:/bin  -- no ~/.local/bin
```

**claude WAS installed** (symlink dated 01:09 → `versions/2.1.252`) and **provision DID run.** Step
4 invoked `bash <path>` — a non-login shell — so the runner's own guard fired and reported an
absence that does not exist. `uv` was never affected: it is at `/usr/bin/uv` and resolves in both
shells, which is why the gate leg was not the one that broke.

**FIX LANDED IN `win-tooling` at `ab6f087`**, RULING-W shape, RED-first: the runner now executes
under `bash -l <path>`. The alternative — symlinking claude into `/usr/local/bin` from
`provision.sh` — was **measured and refused**: that directory is root-owned and *not writable by
`vscode`*, so it would put a `sudo` into provisioning. Suite attribution against a detached
worktree at HEAD: that test file carries **13 pre-existing failures** (13F/53P before, 13F/54P
after), all clustered on cp/scp passthrough ordering and none this change's.

**Codespace STOPPED immediately after the check. Both Shutdown probe codespaces DELETED**
(`batche-c-admission-*`, `animated-dollop-*`), so the batch's one open asset item is closed.

### All seven lanes REISSUED as sonnet

**Operator ruling (ADR-108 §A): R-MODELS binds as recorded — dispatched lanes = sonnet, opus only
where a contract pins tier L, orchestrator and adjudication = opus.** No batch-F contract pins
tier L, so all seven are sonnet.

**The reissue was proved, not asserted.** Each affected skeleton was regenerated twice — once at
`opus`, once at `sonnet` — and diffed: the generator-owned delta is **exactly the routing-table row
and its two prose echoes**, nothing else. Only those lines were changed in the real contracts, so
the result is byte-equivalent to a full regeneration with the authored sections intact.

```
gen_lane_contract.py check   7 of 7 OK
validate_substrate.py        7 OK — 0 REFUSE, 0 WARN
model roll-call              7 x `| sonnet | execute | high |`
```

**One contradiction the reissue exposed and fixed.** L5's item 3 read *"sonnet workers read …
**opus adjudicates** whether each stamp is earned"* — an opus act described as happening **inside**
a lane that now runs sonnet. Corrected to the split the ruling actually implies: **the lane reads
and writes the review record; adjudication is an orchestrator act at the merge.** That makes the
record a deliverable rather than a formality, because the adjudicator was not in the room for the
read.

**Still open here:** the generator's boilerplate line *"Model defaults to `opus` — the
`.dev-knowledge` default per the Ch8 routing matrix"* is now stale doctrine against R-MODELS. It is
generator-owned text, so it is `[#631]`'s to fix at the source, not a contract's to edit.
