# BATCH F — THE DERIVED STATE, for the architect's cut

- **Class:** technical · **Date:** 2026-09-01 · **Arc:** `[#614]` successor · **Consumed by:** `[#614]`
- **Author:** CC (Opus 5, orchestrator seat) · **Status: DERIVED, NOT FROZEN.**

> **Nothing below is a cut.** No contract is written, no worktree provisioned, no manifest
> committed. This file supplies the measured state and the ex-ante numbers so the architect's cut
> is a decision over evidence rather than over memory.
>
> **Derived from LIVE state at `7cb9be42`** (main, clean, zero worktrees), immediately after the
> batch-E close packet landed and the ADR-110 exemption expired with zero anchor gaps.
>
> **Formatting is flat by design** — no pipe tables — so the whole file copies into browser chat
> without the TUI painting border glyphs (`CLAUDE.md` §4, output-formatting).

---

## 0 · THREE THINGS THE CUT MUST DECIDE BEFORE IT SEQUENCES ANYTHING

**These are not seeds. They are constraints the seeds run into, found by measuring.**

**(a) FILING IS BLOCKED. `[#589]`'s byte bar has NEGATIVE headroom.**

```
BACKLOG.md now                      70,276 B
the [#589] Done-when bar            70,000 B      -> 276 B OVER, already
headroom before batch E's last two rows      18 B
```

Batch F files rows. **Every row it files widens an existing breach**, and the suite RED is
already live. There is no version of batch F that does not touch this. The cut has three lawful
moves and must pick one **before** dispatch, not during: `[#589]` raises its own bar with a
recorded justification; a grooming pass shrinks the corpus (**overdue anyway** — `audit.py health`
reports *"last groom 2026-07-30, 33d ago (> 21d cadence, ADR-41)"*); or batch F files nothing and
carries its findings in artifacts only. Silently widening the bar is the one move `[#589]` exists
to forbid.

**(b) TWO SEED PREMISES DID NOT SURVIVE MEASUREMENT.** F2's and F0's briefs each name something
that does not exist as named. Both are stated at their seed below. Neither is fatal; both change
what the contract can say.

**(c) F7 IS ALREADY DONE.** `templates/README-md-template.md` exists, is tracked, is 4,007 B, and
landed 2026-09-01 in `eaaeafa2`. **F7 drops out of batch F.** What remains under that heading is
not a template but a release decision — see §F7.

## 1 · THE SEEDS, MEASURED

### F0 — codespace proof-of-work, FIRST and ATTENDED

**State: RED, and the entry condition is a three-clause conjunction, not a vibe.**

```
L1  Ok                       TRUE   -- and it means TRANSPORT ONLY
L2  RemoteExitCode == 0      FALSE  -- exit 1                          <- RED
L3  receipt HEAD == pushed   NOT MEASURED -- the agent never ran       <- UNMEASURED
GATE (audit.py health)       NOT RUN
remote receipt: "result":"Not logged in - Please run /login", duration_ms 47,
                subtype "success" WHILE is_error true   <- the trap
```

**Z-G3 (`protocols/STANDING_RULINGS.md`) makes "GitHub compute is the DEFAULT substrate"
CONDITIONAL on all three W4 defects closing:** `gh codespace cp` receiving literal single quotes
on the destination path; `uv` absent from the container (so no hub gate can execute under
ADR-106); and the silently stale clone (HEAD frozen while `git status -sb` reports no divergence).
**Until all three close, the default substrate is LOCAL.**

**PREMISE CORRECTION — there is no "router ADR" to cite.** The brief's *"router-ADR entry
condition"* is not a numbered ADR. Z-G3 names it only as *"the wave-2 router ADR"* and states it
is **not authored**, deliberately: *"The router ADR is not authored before its central evidence
exists."* A contract must not cite an ADR number here, because there isn't one.

**PREMISE CORRECTION — the helper is not called `Dispatch-Codespace`.** In `win-tooling`'s
`config/dispatch-helpers/DispatchHelpers.psm1` (178,072 B) the live functions are
**`Start-DispatchCodespace`** (line 2034) and **`Stop-DispatchCodespace`** (line 2547). A contract
naming `Dispatch-Codespace` names nothing.

**Ex-ante:** the blocker is credentials, not architecture — a Codespaces secret carrying the Claude
credential plus `hasTrustDialogAccepted: true` in `/home/vscode/.claude.json`, then a re-run of
this exact probe. **Estimate S for the auth fix + probe re-run; the CONSEQUENCE is L** (if green,
every committing lane's default substrate flips, which is a router-ADR-shaped act). **Attended is
right and the reason is measurable:** the failure returned in 47 ms with a misleading
`subtype:"success"`, which an unattended lane would have read as a pass.

**Unexplained assets, reported not resolved:** a second codespace
`animated-dollop-rr65q4v6jgphxr4g` on branch `probe/admission-roundtrip` appears in NO batch-E
artifact; and `win-tooling` carries stale worktrees at `.claude/worktrees/{cloud-fail-fast,
cloud-models,external-text}/` with older copies of the dispatch module.

### F1 — handoff v7, BEFORE the next handoff

```
row        [#611] "HANDOFF_PROCESS v7: the minimal-bundle package"
           status open · P2 · size M · [E1] Handoff continuity / [S1]
current    protocols/HANDOFF_PROCESS.md  Version: 6.3.0  (status: stable)
ROLE PIN   declared HANDOFF_PROCESS.md:127 and :1188-1200 -- three lines:
           version + sha256 + standing-refusal, emitted by scripts/assemble_paste.py
BOOT       protocols/HANDOFF_BOOT.md  17,196 B  against an 18,000 B budget
           (assemble_paste.py:52 HANDOFF_BOOT_BYTE_BUDGET) -> 804 B headroom
sync       HANDOFF_BOOT frontmatter reconciled_with: handoff-process@6.3.0 -- IN SYNC
```

`[#611]` is **fully unstarted** against this measurement. Its Done-when asks for the b4 probes-pin
delta, an assembled paste measuring **<=20 KB at >=70% window-specific content** from a real cut,
and **v7.0.0 with every version-bearing surface reconciled**, proven by re-running
`reconciled_versions`, `silent_rule_ratchet` and `verify_handoff_probes`.

**Ex-ante M, and the ordering claim is the real content.** "BEFORE the next handoff" is not
preference: a v6.3.0 bundle generated after v7 is drafted but before it lands would have to be
regenerated, and handoff bundles are immutable. **The 804 B of boot headroom is the number to
watch** — the ROLE PIN change and any HANDOFF_BOOT regeneration both spend from it, and
`boot_byte_budget` is a live `audit.py health` check that currently passes at 17,196/18,000.

### F2 — the distiller · TWO MEASURED CONTRADICTIONS, both load-bearing

```
row        [#617] "FILE DISTILLATION -- the output half, and the only worsening series"
           status open · P2 · size M · [E5] / [S14]
```

**CONTRADICTION 1 — the precondition does not trace to DM-1.** Both audits the brief names were
read in full. `2026-08-31-technical-dm1-eval-comparison.md` is a Harbor-format evaluation-harness
COMPARISON whose own §8 verdict is *(b)*: it did not reduce manual effort, did not catch anything
the hand-rolled run missed, did not weaken C-1..C-15 — it **relocated risk**.
`2026-09-01-technical-tierb-b2-sda1-harbor-translation.md` is the translation DM-1 was blocked by.
**Neither establishes any precondition for distiller work.** The *"an eval loop is a PRECONDITION,
not a companion"* claim traces to the SkillsBench finding in
`docs/audits/2026-08-29-technical-autonomy-synthesis.md:89,119` and intake #62's 2026-08-31
amendment, landed into `[#617]` by lane **DM-5**, not DM-1. A contract citing "the DM-1 eval
precondition" would cite the wrong source.

**CONTRADICTION 2 — "Tier-S" is refused by ADR-112's own guard sentence.** Verbatim: *"Tier S never
touches gates, hooks that block, or scripts/ — anything that would, is Tier L by definition."*
`[#617]`'s body frames its work as building an **eval loop / admission gate**. **That is Tier L by
definition.** `[#617]` carries no Tier-S tag of its own. Running it as Tier S — *"30-minute sandbox
try, KEEP or DELETE, no evaluation ceremony, no births"* — would put a gate-building act inside the
tier explicitly barred from gates.

**Ex-ante: as briefed, S (a 30-minute try). As measured, L.** This is the seed the cut should
re-decide rather than sequence.

### F3 — `[#626]`, the logs callers

```
row        [#626] "logs/ does not thin -- the retention rule exempts the two prefixes
           that actually accumulate"   status open · P2 · size M · [E7] / [S18]
```

HY-2 (merged `1c92024f`) built the retention MECHANISM correctly; **its dry run against this repo
is a NO-OP**, which is the row. `TOKEN-LOG.md` is excluded absolutely (ADR-29/39, correct).
`PROPOSALS-*` and `DETECTOR-ERROR-*` are excluded **by prefix** — precisely the files that
accumulate — because three live callers glob them FLAT:

```
scripts/propose_closures.py:302   find_last_proposals_head()  logs_dir.glob("PROPOSALS-*.md")
scripts/propose_closures.py:341   resolve_window()            logs_dir.glob("PROPOSALS-*.md")
scripts/review_closures.py:199    latest_proposals()          logs_dir.glob("PROPOSALS-*.md")
exemption site: scripts/logs_retention.py:71 EXCLUDED_NAME_PREFIXES
```

**Ex-ante S-to-M: three call sites, one constant, one live relocation run.** The row states its own
sequencing risk and it is correct — **re-point the callers FIRST, prove green, THEN retire the
exemption**. Reversing that order breaks the closure loop the moment the files move.

### F4 — `[#276]`, deploy reads consumer waivers

```
row        [#276] "D2 per-consumer waiver-honoring"  status DEFERRED · P2 · M · [E6]
site       deploy/carrier_precommit.py:777  _classify_prune(config, prunable) -> PruneState
           absent -> ALREADY_ABSENT · byte-match -> PRESENT_CLEAN · diverged -> PRESENT_MODIFIED (REFUSE)
grep       zero occurrences of "waiver" or "methodology.yaml" anywhere in deploy/*.py
```

**A LIVE DISCREPANCY THE CUT MUST RESOLVE FIRST: the row's frontmatter says `deferred`, and ruling
3 treats it as an active hard blocker on two consumer instantiations.** A row cannot be both the
thing nothing is waiting on and the thing everything is waiting on. `[#624]` — *"nothing watches a
BLOCKER's status"* — is the organ that would have caught this; here it is, live.

Both divergences are declared and neither is drift: ai-council's consumer-owned `ruff` id
(re-activated by a fleet ruling 2026-07-12, declared in its own `.methodology.yaml`) and
corp-monorepo's omitted `ruff-format` (CRLF/LF conflict under `core.autocrlf=true` in pre-commit's
stash cycle). **The instantiations are blocked on a DEFERRED HUB ROW, not on a consumer question.**

**Ex-ante M, one function.** `_classify_prune` gains a waiver input consulted before it returns
`PRESENT_MODIFIED`. Un-deferring the row is a prerequisite act, not part of the build.

### F5 — ARCHITECTURE slice 2, by BYTES and CONSUMERS

```
ARCHITECTURE.md   114,681 B · 1,203 lines

front matter (pre-Purpose)                     1- 205   22,759 B   <- 2nd largest
Purpose [CORE]                               206- 236    2,099 B
Codemap [CORE]                               237- 260      906 B
Layer Boundaries & Invariants [CORE]         261- 312    2,970 B
Authority and governance [CORE]              313- 338    1,518 B
Organ map (Ch2)                              339- 489   18,704 B
Validators and enforcement [CORE]            490- 770   24,927 B   <- LARGEST
Automation axes (Ch3)                        771- 857    5,918 B
Distribution and transfer (Ch4)              858- 920    6,870 B
Key conventions & zones                      921-1006    6,068 B
Verification mesh and decision flow (Ch6)   1007-1144   10,574 B
Governing ADRs                              1145-1203   11,368 B
```

**Two chapters are 41% of the file** — "Validators and enforcement" (24,927 B) and the Organ map
(18,704 B) — and the **front matter alone is 22,759 B**, larger than every chapter but one. The
front matter is where the stacked review-record blockquotes live; it is a growth series, not a
chapter.

**Consumers that cite chapters BY NAME or NUMBER — the thing a slice must keep working** (live
surfaces only; dated audits, handoffs, JOURNAL and `ecosystem/*/history` excluded):

```
protocols/STANDING_RULINGS.md 5 · protocols/PLAYBOOK.md 5 · ADR-70-amendment 3
tasks/525 2 · ecosystem/organ-index.md 2 · ADR-86 2
tasks/507 · tasks/171 · tasks/162 · protocols/HANDOFF_PROCESS.md · CLAUDE.md (Ch2)
BACKLOG.md (Ch5) · .claude/commands/handoff.md (Ch1) · .claude/commands/handoff-verify.md (Ch1)
ADR-29 · ADR-107 · ADR-105 · ADR-101 · two docs/intake entries        = ~20 live citations
```

**NO OPEN ROW PROPOSES A SLICE.** `[#41]` (split §Processes) is CLOSED and its target section does
not exist under that name any more; `[#525]` is CLOSED and was about ADDING organ rows. **So F5
would be born, not resumed** — and under constraint (a) above, being born costs a row.

**Ex-ante L, and the freshness coupling is the reason.** `ARCHITECTURE.md` is a `FRESHNESS_FILES`
member: the `canonical_freshness` A2 gate FAILs a canonical doc edited since its last review, so
ANY slice forces a `last_reviewed` bump, which in this repo means a genuine end-to-end re-read of
1,203 lines. That is the same coupling that deferred the VISION relocation today
(`2026-09-01-technical-dc3-split.md` §4). **Slice and re-read are one act, not two.**

### F6 — `[#627]` agy admission, and `[#628]` ESSENTIALS

```
[#627]  "The agy route is INERT -- no row authorizes its analysis-role admission,
         so the token policy promises what nothing gates"     open · P2 · M · [E7]/[S19]
[#628]  "DC-2 re-cut -- dissolving ESSENTIALS.md is a FLEET-COUPLED release act,
         not a doc lane"                                      open · P1 · L  · [E5]/[S14]
```

**`[#628]`'s input artifact is measured and preserved.** Branch
`worktree-lane-b-3-claude-md-genre` @ `6f226b34`, unmerged, alive **locally and on origin**:

```
git diff main...worktree-lane-b-3-claude-md-genre --stat
  CLAUDE.md 29 ++-- · protocols/ESSENTIALS.md 185 --------- · protocols/PLAYBOOK.md 69 ++++--
  templates/child-methodology-floor.md.tmpl 2 +- · 5 x templates/claude-regions/* 
  9 files, +77 -223   (ESSENTIALS.md: -185, +0 -- the whole dissolution)
```

**The gap between that diff and `[#628]`'s scope is the point.** The branch touches 9 files;
`[#628]` enumerates **ten breaking consumers plus the floor-hash release-lint chain**, none inside
the frozen write-scope. The lane refused correctly, and **its refusal is the specification.**

**`[#628]` is fleet-coupled and sequences WITH v1.5.0, not ahead of it** — its relocation target is
hash-guarded three ways (template bytes, `.sha256` sidecar, `anchors.floor_sha256` across three
live pinned manifests) with `release_lint` C5 asserting the equality. A floor edit is a release act
by construction. **Ex-ante L, and it is the one seed that cannot start before the tag.**

### F7 — README template · CLOSED BEFORE THE BATCH

```
templates/README-md-template.md   EXISTS · TRACKED · 4,007 B · added by eaaeafa2
  "feat(templates): the README-md template -- the one payload the front-door
   migration was waiting on [#614]"
```

**F7 as briefed is done.** What is left under that heading is a RELEASE decision, not a build:
declaring the `readme-front-door` component in `deploy/manifest-v1.5.0.yaml`. Its remaining blocker
is `release_lint` C7, which asserts EXACT dict equality between a manifest's `doc_shapes` spines
and the live `audit._CANONICAL_SPINE` **and lints v1.1.0 and v1.2.0 against those same live
constants** — so adding `README.md` to either side alone REDs shipped specs. **Ex-ante S in code,
L in sequencing.** The manifest's own stale claim that the template did not exist was corrected in
the batch-E close commit.

## 2 · THE SEQUENCE THE MEASUREMENTS IMPLY

Not a cut — the ordering constraints that are **forced**, separated from the ones that are choices.

```
FORCED, and why
  0.  resolve constraint (a) -- the [#589] byte bar -- BEFORE any row is filed.
      Every batch-F row widens a live breach. This is the only item that gates all others.
  1.  F0 FIRST and ATTENDED. If green, every committing lane's default substrate flips,
      which changes what every later contract declares. Running F0 late means re-cutting
      the batch. Attended because the failure returns in 47 ms wearing "success".
  2.  F1 BEFORE the next handoff. A v6.3.0 bundle cut after v7 is drafted must be
      regenerated, and handoff bundles are immutable.
  3.  F4 needs [#276] UN-DEFERRED first. A build cannot proceed on a row whose own
      frontmatter says nothing is waiting on it.
  4.  [#628] (F6b) AFTER the v1.5.0 tag. A floor edit is a release act by construction.

CHOICES, in decreasing measured readiness
  F3   [#626]  3 call sites + 1 constant, sequencing risk already written down     S-M
  F4   [#276]  1 function, deploy/carrier_precommit.py:777, once un-deferred        M
  F6a  [#627]  agy admission -- a decision row, not a build                          M
  F1   [#611]  v7 -- 804 B of boot headroom is the number to watch                   M
  F5   ARCHITECTURE slice -- born, not resumed; slice AND re-read are ONE act        L
  F2   distiller -- RE-DECIDE before sequencing; ADR-112 says Tier L, not Tier S     L

DROPS OUT
  F7   README template -- landed 2026-09-01 in eaaeafa2. What remains is a release act.

CARRIED FROM BATCH E, unsequenced
  [#629] predicate 7 · [#630] manifest/contract slug equality -- both ruled today,
         both gate predicates, both cheap, and both FILE rows (see constraint (a))
  [#621] the hub's VISION.md relocation -- gate-unblocked today, collateral enumerated
  two Shutdown codespaces awaiting a deliberate decision
  one empty worktree directory held by a live session
```

**Then, in the operator's order:** v1.5.0 tag (operator) -> monorepo instantiation (attended GO).
**`[#276]` gates BOTH consumer instantiations**, so F4 is on the critical path to the GO, not
beside it.

## 3 · WHAT BATCH F WOULD LEAVE ON THE TABLE

Open **P1** rows not covered by any seed — so the cut sees its own opportunity cost:

```
[#359] M  PHANTOM ENFORCEMENT -- HANDOFF_PROCESS §14a FILE-BOUNDARY claims a mechanism that does not exist
[#514] M  Two rival LANE_BRANCH_RE constants ship in one repo
[#519] M  The close path is two edits, and nothing makes a half-done close visible
[#528] M  Lane-latency -- the full suite x per-lane + per-merge runs is the real batch cost
[#555] M  Closing campaign batch 1 + kill-candidates instrument
[#579] L  Code doctrine & FDD -- one ADR merging intakes #31 and #34 (ARC-A)
[#580] M  State-as-data: atomic id allocation, tasks/ as the SOLE source (ARC-B)
[#581] L  Backlog vitals -- three flow instruments + what-is-unblocked-now (ARC-C)
[#582] L  Substrate router -- one gated enum, a capability-keyed table, its generator (ARC-D)
[#587] M  P-1 -- invert the journal-anchor check to a single pass
[#588] S  P-2 -- build the spine parent-map in ONE git process
[#589] M  One line per row -- the BACKLOG view projection + its size assertion
[#608] S  Tiling-aware journal read -- the rotation seam, before any split
[#614] L  VISION.md superseded by a recreated root README.md -- the frozen execution arc
[#625] M  The rule-adherence eval corpus -- a FRESH corpus
[#629] M  An amendment cannot SUBTRACT an act (predicate 7)
```

**Three of these are load-bearing on the seeds and the cut should notice:** `[#589]` IS constraint
(a); `[#582]` (substrate router) is what F0 going green would feed; and `[#514]` (two rival
`LANE_BRANCH_RE` constants) is the same class as `[#630]` — a value living in two places with a
human keeping them equal.

## 4 · HONEST LIMITS OF THIS DERIVATION

1. **Ex-ante sizes are S/M/L judgements anchored to a stated measurement** (files touched, call
   sites, bytes, consumer counts) — they are not effort estimates and no history was mined for
   comparables.
2. **F2's re-decision is surfaced, not resolved.** Whether `[#617]` runs as Tier S against
   ADR-112's guard sentence is a technical-architect question (ADR-108 §A), not this seat's.
3. **The `[#276]` deferred/blocking contradiction is reported, not repaired.** Un-deferring a row
   is a prioritisation act, which is the operator's.
4. **Consumer-side `.methodology.yaml` files were not read** — they live in ai-council and
   corp-monorepo, outside this repo, and this derivation stayed hub-local.
5. **No history was mined for the per-lane cost model.** `[#528]` — *"the full suite multiplied by
   per-lane + per-merge runs is the real batch cost"* — is open and uncomputed, and batch E's own
   integration run took **17m23s**. A width-N cut should price that.

---

## AMENDMENT 1 — 2026-09-01: §F0's premise was STALE, and the correction is the architect's

> **In-file amendment marker** (CLAUDE.md §5 rule 3). §F0 above stands as the record of what this
> seat measured; this records what it measured WRONG and why, rather than editing the claim away.

**§F0 is wrong. Codespace is ADMITTED, and has been since 2026-08-31 22:56.**

This derivation reported the tier-(C) probe RED and built the whole seed on it. It cited
`docs/audits/2026-08-31-verification-codespace-admission-probe.md` — which is a **REBUILD** probe,
and the batch-E manifest's tier-(C) section that quotes it was **frozen at dispatch**. Neither
carries what happened five hours later.

**The evidence, resolved at `c8bf1390`** (*"Merge branch 'fix/codespace-f4-workspace-trust' — F4
workspace trust, and codespace ADMITTED [#614]"*, 2026-08-31 22:56), JOURNAL 2026-08-31 (i),
anchor `5c54487d`:

```
L2    is_error False · subtype success · result "ADMISSION-PROBE-OK"
      model claude-opus-5 · provider firstParty · permission_denials []
GIT   FETCH_EXIT=0 · PUSH_EXIT=0   (a real branch pushed to origin, deleted after)
GATE  gen_task_tree --check exit 0 · audit.py health exit 0, "health: OK" IN-CONTAINER
```

**THE CREATE-vs-REBUILD FINDING IS WHY EVERY EARLIER RED WAS MEASURING NOTHING.** A
`gh codespace rebuild --full` on the old container left it with no `uv`, no `gh`, no provisioning
stamp and a clone two merges stale, while `devcontainer.json` **at that container's own HEAD**
declared both `postCreateCommand` and the feature. A fresh **CREATE** produced `claude`, `uv`, both
tokens on the login shell, and `HEAD` at current main. **Rebuild does not re-apply the devcontainer
configuration; create does.** So all three W4 defects — the `cp` quoting, absent `uv`, the silently
stale clone — are closed **under fresh-create discipline**, and Z-G3's entry evidence EXISTS.

**Consequences for the seed, per the architect's cut:**

```
F0 = (i) the proof-of-work COMMITTING lane on codespace, ATTENDED, driven by
         Start-DispatchCodespace / Stop-DispatchCodespace  (never "Dispatch-Codespace")
     (ii) AUTHOR the wave-2 router ADR NOW, from this evidence, feeding [#582]
GREEN PoW => the committing lanes of THIS batch default to substrate=codespace
```

**The premise correction that STANDS from §F0 is the naming one:** the helper really is
`Start-`/`Stop-DispatchCodespace`. The router-ADR correction is now *half* right — there is still
no ADR number to cite, because it is not authored; but the reason has changed from *"its central
evidence does not exist"* to **"its central evidence exists and authoring it is F0(ii)."**

**And the 'unexplained' second codespace is explained.** `animated-dollop-rr65q4v6jgphxr4g` on
`probe/admission-roundtrip`, created 22:41, **is** the fresh-create admission probe. It appeared in
no batch-E artifact because the artifacts that would have named it were written before it existed.
Its branch was already cleaned from origin. The 2026-08-31 (i) entry is explicit that the OLD
container `batche-c-admission-*` *"is NOT the evidence for this and should not be reused."*

**The transferable lesson, which is why this is an amendment and not a quiet edit.** A manifest's
tier section is **frozen at dispatch** and a derivation that reads it is reading a point-in-time
claim, not live state. This seat searched the audits corpus and the manifest, and did not search
`JOURNAL.md` for later evidence about the same subject — so it inherited a RED that a five-hour-old
entry had already overturned. **Derive from the JOURNAL as well as the artifacts, or derive stale.**
