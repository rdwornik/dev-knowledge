# ADR-104: Fleet repository shape — partial fold on engineering grounds; polyrepo mostly retained

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision tier:** Path A — operator ruling (the shape constraint) + architect recommendation (the shape), session 2026-07-24 (Lane A). The operator accepts, amends, or rejects the recommended shape; the ruling itself is settled.
- **Related:** ADR-28 (three-layer ecosystem model — the hub is Layer 2, a governance authority that never executes), ADR-61 (separate repos parallelize freely — a consequence of the split, not its cause), ADR-41 (per-repo session ownership)
- **Intake:** #16 (`docs/intake/2026-07-21-func-fleet-north-star.md` §4 — the polyrepo-ruling inputs; this ADR is step 2 of §6)
- **Decommission:** none. No fold executes on this ADR. Execution is the downstream chain #382 (desired-state ADR) → #383 (execution waves) → #385 (tech-currency); a fold begins only after the precondition scan below and its own ruling.
- **Source:** operator shape ruling 2026-07-24 (Lane A prompt, quoted verbatim below); architect fold-shape derivation; independent second derivation by `gpt-5.6-sol` run without sight of the architect draft (both reported below). **Amended 2026-07-24 (same session, draft — Status held Proposed):** operator follow-on ruling (corp-monorepo OUT, incremental consolidation) recorded after the **corp-monorepo content-and-history scan** (read-only `git grep` / `git log --all`, zero mutations) discharged precondition (c) — see §2.

## Context

`[#381]` is the fleet's **first repository-shape ADR**. The shape entered canon as an observation, never an argument: intake #16 §4 records that across 78+ ADRs, zero weigh monorepo vs polyrepo, and ADR-28 self-declares descriptive ("names an operating pattern already in place"). Three months of fleet machinery then grew *under* that unargued shape — roughly 15,000 lines of plural-only machinery (measured below) that exists only because there are N>1 repos.

The fleet is **9 git repos**: the hub `.dev-knowledge` (governance authority, not a code project) plus `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`.

Intake #16 §4 flagged three unpriced items that MUST be in this ADR: (a) the cost of unfolding if the fold is wrong; (b) whether the employer-data (Blue Yonder) boundary can compliantly share a tree with personal repos; (c) blast radius on live pre-sales work. Item (b) — the compliance boundary — was the **main pillar** of the prior architect recommendation (a partial fold *along the compliance line*: a work tree and a personal tree). This ADR opens with the operator's ruling that removes that pillar, then re-derives the shape on engineering grounds alone.

## Decision

### 1. The operator's ruling (recorded, not relitigated)

> **"Repos may share one tree; any employer material simply goes under `.gitignore`. Compliance is therefore NOT a constraint on the fold shape."**

The compliance/employer-data boundary is **removed as a constraint on the fold shape**. This ADR records the ruling and prices it; it does not re-argue it.

**Amendment ruling (2026-07-24, same session — supersedes the mechanism, not the verdict).** After the corp-monorepo scan (§2c below) proved the `.gitignore` disposition mechanism inoperative, the operator ruled:

> **"corp-monorepo stays OUTSIDE the fold. The remaining repos consolidate incrementally — stage by stage, verifying value after each step — not in one move."**

This **supersedes the `.gitignore` disposition mechanism** and sets the execution shape (§5). It does **not** change the PARTIAL verdict (§3); the first ruling removed compliance as a constraint, and this one records that `.gitignore` cannot dispose of corp-monorepo's employer material either.

### 2. Execution precondition — caveats (a)/(b) stand; (c) DISCHARGED NEGATIVE by the corp-monorepo scan

Two of the ruling's `.gitignore` consequences stand as a precondition on any fold that would rely on `.gitignore`; the third — the unverified premise — has now been **verified and found FALSE for corp-monorepo**, and that finding **strikes `.gitignore` as the disposition mechanism** for the repo it was meant to cover.

- **(a) `.gitignore` filters tracking, not presence.** It stops *new* commits of a path; it does **not** reach content **already committed to history**. (Confirmed decisive below.)
- **(b) Gitignored paths are ungoverned.** Ignored material is invisible to the fleet's governance tooling (`audit.py`, `fleet_parity.py`) — it cannot be parity-checked, freshness-checked, or edge-scanned. Where `.gitignore` *is* used, ignored material is a real, stated cost; but per (c) it is **not** the mechanism for corp-monorepo.
- **(c) DISCHARGED — the premise was unverified; it is now verified and FALSE.** A read-only content-and-history scan of `corp-monorepo` (deterministic `git grep` / `git log --all`, zero mutations, 2026-07-24) found:
  - **104 tracked files carry ~206 real enterprise account tokens; 104/104 are already in committed history** (verified per-path via `git log --all`). **`.gitignore` reaches ZERO of them** — the ruling's original mechanism is **inoperative for every file that matters** (caveat (a), made concrete).
  - **Volume points opposite to exposure.** What `.gitignore` *does* handle correctly is `data/_outputs/` (18 GB, 2,925 files) — **never committed, already ignored**. The bulk is in ignorable never-committed data; the *risk* is the small **tracked** surface `.gitignore` cannot touch.
  - **The tracked material is load-bearing, not stray.** Curated account config and `client_aliases.yaml` are read by the extractor; **40 test files depend on real-account fixtures** — removing them breaks the suite.
  - **No live exposure, no live secrets.** corp-monorepo's remote is **private, under a personal GitHub account** (operator-verified: `gh repo view rdwornik/corp-monorepo` → `isPrivate: true`) — no public exposure. The `AKIA`/`password` hits are a secret-**detector** pattern list, not credentials.

**Consequence — the mechanism is struck; the disposition is exclusion.** `.gitignore` cannot dispose of corp-monorepo's employer material: it is **history-entangled** (already committed, caveat a) and **load-bearing** (removal breaks the suite). Per the amendment ruling (§1), **corp-monorepo stays OUTSIDE the fold — and the reason is history-entanglement plus a load-bearing dependency, NOT compliance** (the first ruling removed that) and **NOT a `.gitignore` fix** (the scan proved it inoperative). For any *other* repo a later stage considers, the original hard gate stands: a content-and-history disposition scan before execution — classifying every path/historical object as never-committed, already-committed, excluded, or governed — with no path or historical object unclassified when a fold begins.

### 3. The shape verdict — PARTIAL (re-derived on engineering grounds only)

**Recommendation: PARTIAL fold. Not FULL, not NO.** The recommended default is a **narrow, domain-scoped consolidation**, with the fleet remaining a governed polyrepo.

**Did the answer change?** The *verdict* stayed PARTIAL, but the *reasoning changed entirely*, and this is the load-bearing point:

- The prior PARTIAL rested mainly on the **compliance boundary** (work tree vs personal tree). The first ruling removed that pillar.
- Removing it **does not strengthen the case for a FULL fold** — the remaining engineering factors still argue against aggressive folding. The corp-monorepo scan (§2c) then made the argument against folding the employer repo **concrete and stronger than the original hypothetical**: it is not a "would-be ungoverned zone if gitignored" — it is that `.gitignore` **cannot dispose of the material at all** (history-entangled + load-bearing), so folding corp-monorepo is precluded on engineering grounds outright.
- **What the verdict now rests on:** unfold-cost asymmetry, pre-sales blast radius, the product/domain-scoping of every repo, worktree-substitutability of the leading justification, and — for corp-monorepo specifically — **history-entanglement + a load-bearing dependency** (§2c). It rests on **engineering cost and history-entanglement — no longer the compliance boundary, and no longer the `.gitignore` mechanism** (the scan struck it). The verdict itself is unchanged; the scan does not move it.

**Live-verified cost basis** (re-derived this session; the intake's "~4,200" was verified, not inherited):

| Plural-only surface (dissolves only at ONE tree) | Live line count |
|---|---|
| Parity/boundary/floor script cluster (`fleet_parity` 1974, `boundary_report` 376, `boundary_headers`, `generate_floor` 406, `check_floor_hash`, `enforcement_coverage`) | 4,222 |
| Deploy subsystem (`deploy/*.py` — carriers + tool + contract) | 4,811 |
| Registries / manifests (yaml: 6 manifests + `parity-surfaces` + `ecosystem/` registries) | 6,376 |
| **Total plural-only estate** | **15,409** |

The intake's "~4,200 lines" corresponds **exactly** to the script cluster (4,222); the full plural-only estate is ~3.7× larger. **What survives any fold** (does not dissolve): worktree isolation guards, the hub/repo ownership axis, the handoff harness, the silent-rule census, and the methodology layer (ADR lifecycle, JOURNAL gates, doc-code-edge, freshness checks) — i.e. the hub's actual value is fold-invariant.

**The five priced factors (engineering only):**

1. **Savings vs survival.** The 15,409-line estate only *fully* dissolves at ONE tree; a PARTIAL fold to a few trees keeps the cross-tree core (parity/deploy machinery still coordinates the remaining trees). The saving is real but smaller than "retire 15k lines" implies, because the methodology layer — the point of the hub — survives regardless.
2. **Unfold cost (asymmetry).** Folding is a near-one-way door: unfolding later needs history extraction (git-filter-repo), remote recreation, CI/hook reconstruction, and path-ownership recovery — materially harder than folding one more coherent domain later. This argues for **incrementalism over a big-bang FULL fold.**
3. **Pre-sales / employer blast radius.** `corp-monorepo` carries live pre-sales/employer work (DECISION-28:92 rejected push-down enforcement precisely to avoid disrupting it). The ruling removes the *legal* constraint but not the *operational* one: a shared hook/CI/remote failure across a universal tree would hit active employer work, personal products, tooling, and the governance authority at once.
4. **Tooling/CI surface.** A fold collapses N remotes + N hook sets + N default-branch controls; path-scoped CI inside a consolidated tree captures the operational gain. But this gain is realizable by *domain* consolidation without converting every change into fleet-wide infrastructure work.
5. **Ungoverned-zone cost (new, from the ruling).** Under a FULL fold, the gitignored employer blind zone sits *inside the universal tree* and weakens every whole-tree governance claim. Keeping it inside a *corporate-domain* tree makes the boundary explicit and bounds the damage.

**Architect's recommended shape (narrow):** corp-domain consolidation only — `demo-prep → corp-monorepo` (already planned, per corp's own charter), and `corp-ops` / `corp-sca-time-automation` folded into the corporate tree **only if the content-scan confirms they are corp-scoped**. Keep standalone: `.dev-knowledge` (governance authority — must stay distinct per ADR-28), `ai-council` (distinct product), `life-architect` (personal), `terminal-setup` / `win-tooling` (kept standalone absent a demonstrated shared-release benefit). The plural-only cost of the retained repos is carried by worktrees + the hub deploy channel, which survive a fold anyway.

### 4. Independent second derivation (`gpt-5.6-sol`, run without sight of the architect draft)

Run as a foundational cross-vendor check on the same inputs. **sol's verdict: PARTIAL** — convergent with the architect on verdict, reasoning, and the ungoverned-zone cost. sol's boundaries and the divergence, reported **unreconciled** per the lane contract:

- **sol's trees (5 total):** `.dev-knowledge` standalone · `ai-council` standalone · `life-architect` standalone · **Corporate tree** {`corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`} · **Workstation tree** {`terminal-setup`, `win-tooling`}.
- **sol's strongest counter-argument (its own steelman):** a FULL fold uniquely deletes the entire 15,409-line estate, and worktrees already answer the isolation argument — so PARTIAL risks paying migration cost while keeping most of the fixed cross-tree machinery.

**The divergence — both land on PARTIAL, but on *aggressiveness*.** **sol goes 9 → 5 trees** (confidently folding corp-ops/corp-sca into the corporate tree and creating a workstation tree for terminal-setup+win-tooling). **The architect is narrower** — corp consolidation gated on the content-scan, terminal-setup/win-tooling kept standalone absent a demonstrated shared-release benefit, trending toward the minimal defensible fold. The gap is whether to consolidate the workstation-tooling and the corp-satellite repos *now* on the operational-surface argument (sol), or to fold only the already-planned corp domain and hold the rest as governed polyrepo (architect).

**RESOLVED (operator ruling 2026-07-24) — sol's derivation kept on record, its aggressive fold rejected.** sol's **9 → 5 aggressive fold is NOT adopted**; the operator ruled **incremental consolidation** (§1/§5). sol's derivation stays recorded — the rejection and its reason are the point. Reason, verbatim:

> *"Folding is easy, unfolding is hard — the asymmetry is the argument. Consolidate two trees, verify the value over a working week, then consolidate the next. One move forecloses the cheap correction."*

Two specifics fall out: (i) corp-monorepo — which sol placed *inside* its corporate tree — is ruled **permanently outside** (§2c: history-entangled + load-bearing); (ii) **hub governance of corp-monorepo already works WITHOUT a fold** — it is a Wave-1 methodology consumer, covered by the parity walk and the audits — so its exclusion **costs no manageability**. The architect's narrower instinct and the operator's incremental ruling converge; sol's simultaneous 5-tree move is the rejected alternative, recorded here, not deleted.

### 5. Execution shape (the ruled consolidation path)

- **corp-monorepo is permanently outside the fold** — history-entanglement + a load-bearing dependency (§2c), governed by the hub *without* a fold (Wave-1 methodology consumer, parity walk, audits). Its exclusion costs no manageability.
- **The remaining repos consolidate in stages** — each stage is its **own arc with its own witnessed value check** (consolidate, then verify the value before the next step), never one move. The asymmetry — folding easy, unfolding hard — is exactly why the path is staged and not atomic: one move forecloses the cheap correction.
- **This ADR does NOT enumerate which repos pair first, nor size the stages** — that is **[#383]**'s job (execution waves). The **E9 brake holds** (no new fleet machinery, no repo moves, no history rewrites) until this ADR is **accepted and merged**.

## Consequences

- **Governed polyrepo is the retained default.** The hub keeps governing all trees; the methodology layer is fold-invariant, so the hub's value is unaffected by the shape chosen.
- **The plural-only estate is not retired by a PARTIAL fold** — only per-repo duplication within a consolidated tree is removed. The 15,409-line saving is available only at a FULL fold, which is rejected on the five factors above. This is the priced trade-off, stated plainly.
- **The ruled shape introduces no ungoverned zone.** The `.gitignore` disposition mechanism was **struck** (§2c — inoperative for corp-monorepo: history-entangled + load-bearing), and corp-monorepo stays a **governed** repo *outside* the fold rather than an ignored zone *inside* it. Caveat (b) reapplies only if a *future* stage proposes `.gitignore` for any material — then the precondition scan must quantify the blind zone (candidate follow-up: a governed-coverage metric that reports any ignored surface).
- **Downstream chain is gated on this ADR's acceptance, not this draft.** #382 (desired-state schema; its matrix width is set by the ruled tree count) → #383 (execution waves, worktrees singly) → #385 (tech-currency). The E9 brake ("no new fleet machinery until the shape is ruled") holds until this ADR is **accepted and merged**.
- **No execution here.** No repo moves, no history rewrites, no machinery. Acceptance closes `[#381]`; the first fold action is a separate ruling after the precondition scan.

## Alternatives considered

- **FULL fold (all 9 → one tree) — rejected.** It is the only shape that retires the whole 15,409-line estate (sol's steelman), but: the unfold-cost asymmetry makes it a near-one-way door; it maximizes pre-sales blast radius; every repo is product/domain-scoped so the fold has no domain logic; worktrees already deliver the agent-lane isolation that was its leading justification; and **folding corp-monorepo is precluded outright** — its employer material is history-entangled and load-bearing (§2c), so no `.gitignore` line disposes of it. The savings are real but do not clear these costs at 5–8+ repos.
- **NO fold (status-quo polyrepo) — rejected as the stated recommendation, but it is the fallback.** The architect recommendation is *close* to it — a narrow domain consolidation over a retained polyrepo. Pure NO-fold forgoes the already-planned `demo-prep → corp` consolidation and the operational-surface reduction that a domain tree captures cheaply, so a narrow PARTIAL is preferred to strict NO.
- **PARTIAL along the compliance boundary (the prior recommendation) — superseded by the ruling.** It drew a work tree vs a personal tree along the employer-data line; the operator's ruling removes that line, so the boundary is re-drawn on domain/blast-radius grounds instead.

*Scale note: priced at the real 5–8+ repos (live fleet = 9 git repos). The "10–20 repo" figure that appeared in the 2026-07-21 audit and three handoff files is fabricated and is not used here (intake #16 §4 item 2).*

## Amendment — 2026-08-03 (the fleet declaration gains a machine-locatable anchor; [#472] / ADR-94)

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94).** The decision body above is
> preserved **verbatim** — nothing in it is edited, including the line-15 fleet enumeration this
> section makes machine-readable. It adds **no member, removes none, and changes no ruling**: it
> re-states the SAME nine repos inside a delimited block a checker can locate, so the
> enumeration stops being reachable only by prose. Landed under **[#472]**, whose Done-when is
> *"a ruling records how the ADR-104 declaration becomes loadable without violating ADR-109 §9"*.

- **Source:** [#472] (clause 2 split out of [#462], architect ruling 2026-08-01). In-file
  amendment per **ADR-94** — an own-invariant refinement of THIS ADR's own enumeration, not a
  new domain; the same channel ADR-101 uses to grow a closed set (`ADR-101` amendments
  2026-07-13 / 2026-07-27 ×2).
- **Correction of a recurring mis-citation:** the enumeration is at **line 15 of this file**, in
  the Context section. This ADR has **no §15** — its sections are §1–§5. Cite `ADR-104:15` or
  "the Context enumeration", never "§15".

### Why an anchor, and deliberately not a new file

The declaration has been machine-consumed since [#462] — as the hardcoded constant
`ADR104_FLEET_DECLARATION` in `scripts/audit.py`, whose own comment names the gap: *"the
constant can drift from ADR-104:15 silently."* That constant was the right call and stays: a new
persisted declaration file is **rejected by ADR-109 §2** (*"No new physical contract file is
created in v1"*) and again by **ADR-109 §9** (*"A new persisted desired-state file in v1 —
rejected"*). This amendment closes the drift without crossing that bar: the ADR — already the
authority — is made *locatable*, and the constant is checked against it.

### The declaration block

The block below is the ADR-104 fleet declaration in machine-locatable form. Its content is
byte-identical to the line-15 enumeration and to `scripts/audit.py::ADR104_FLEET_DECLARATION`.
One repo id per line; ordering is not significant; the delimiters, not the fence, are the
contract.

<!-- declaration:start id=adr104-fleet-members v=1 -->
```
.dev-knowledge
ai-council
corp-monorepo
corp-ops
corp-sca-time-automation
demo-prep
life-architect
terminal-setup
win-tooling
```
<!-- declaration:end id=adr104-fleet-members -->

**Lockstep in the SAME commit** (the `ADR-101` 2026-07-13 / 2026-07-27 precedent):
`scripts/audit.py::check_membership_agreement` gains the declaration-agreement leg that reads
this anchor, and `tests/test_membership_agreement.py` pins both directions of the diff. Unlike
that precedent, the lockstep here is **machine-checked, not conventional** — an edit to either
side without the other REDs the `audit-health` gate.

### What this changes — and, deliberately, what it does not

- **Changed:** the fleet declaration is now locatable by a checker. A constant that drifts from
  this ADR fails a gate instead of ageing silently.
- **NOT changed — membership resolution.** `resolve_fleet_members` is **not** widened and this
  block is **not** consulted for it. Resolving membership toward `deployed-versions.yaml` is a
  named **ADR-109 §2** ruling (restated in the ADR-109 2026-08-01 amendment); this anchor is an
  authority to *agree with*, never the census's membership input.
- **NOT changed — no registry is created.** The block confers no authority this ADR did not
  already hold. It is not a second source of truth: `ecosystem/`'s surfaces remain the machine
  surfaces, and the census still diffs THEM against the declaration, not against each other.
- **NOT changed — no new file, no new directory.** ADR-109 §2/§9 hold intact.
- **NOT changed — `VISION.md`.** VISION states the same nine (`VISION.md:107-112`) and remains a
  prose restatement. Binding it as a second machine surface would create exactly the second
  source of truth this amendment refuses; if that is later wanted, it is its own ruling.
- **NOT changed — the fold verdict, the tree count, or any §1–§5 ruling.** Nine were declared
  before this amendment and nine after.
