# ADR-104: Fleet repository shape — partial fold on engineering grounds; polyrepo mostly retained

- **Status:** Proposed
- **Date:** 2026-07-24
- **Decision tier:** Path A — operator ruling (the shape constraint) + architect recommendation (the shape), session 2026-07-24 (Lane A). The operator accepts, amends, or rejects the recommended shape; the ruling itself is settled.
- **Related:** ADR-28 (three-layer ecosystem model — the hub is Layer 2, a governance authority that never executes), ADR-61 (separate repos parallelize freely — a consequence of the split, not its cause), ADR-41 (per-repo session ownership)
- **Intake:** #16 (`docs/intake/2026-07-21-func-fleet-north-star.md` §4 — the polyrepo-ruling inputs; this ADR is step 2 of §6)
- **Decommission:** none. No fold executes on this ADR. Execution is the downstream chain #382 (desired-state ADR) → #383 (execution waves) → #385 (tech-currency); a fold begins only after the precondition scan below and its own ruling.
- **Source:** operator shape ruling 2026-07-24 (Lane A prompt, quoted verbatim below); architect fold-shape derivation; independent second derivation by `gpt-5.6-sol` run without sight of the architect draft (both reported below).

## Context

`[#381]` is the fleet's **first repository-shape ADR**. The shape entered canon as an observation, never an argument: intake #16 §4 records that across 78+ ADRs, zero weigh monorepo vs polyrepo, and ADR-28 self-declares descriptive ("names an operating pattern already in place"). Three months of fleet machinery then grew *under* that unargued shape — roughly 15,000 lines of plural-only machinery (measured below) that exists only because there are N>1 repos.

The fleet is **9 git repos**: the hub `.dev-knowledge` (governance authority, not a code project) plus `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`.

Intake #16 §4 flagged three unpriced items that MUST be in this ADR: (a) the cost of unfolding if the fold is wrong; (b) whether the employer-data (Blue Yonder) boundary can compliantly share a tree with personal repos; (c) blast radius on live pre-sales work. Item (b) — the compliance boundary — was the **main pillar** of the prior architect recommendation (a partial fold *along the compliance line*: a work tree and a personal tree). This ADR opens with the operator's ruling that removes that pillar, then re-derives the shape on engineering grounds alone.

## Decision

### 1. The operator's ruling (recorded, not relitigated)

> **"Repos may share one tree; any employer material simply goes under `.gitignore`. Compliance is therefore NOT a constraint on the fold shape."**

The compliance/employer-data boundary is **removed as a constraint on the fold shape**. This ADR records the ruling and prices it; it does not re-argue it.

### 2. Execution precondition (three caveats — not objections, a gate)

The ruling's `.gitignore` mechanism carries three consequences that are **not objections to the ruling** but a **precondition on any fold that relies on it**. No fold may execute until the precondition is discharged.

- **(a) `.gitignore` filters tracking, not presence.** It stops *new* commits of a path; it does **not** reach content **already committed to history**. Employer material already in any repo's history stays in history regardless of a later `.gitignore` line.
- **(b) Gitignored paths are ungoverned.** Ignored material is invisible to the fleet's governance tooling (`audit.py`, `fleet_parity.py`) — it cannot be parity-checked, freshness-checked, or edge-scanned. The ruling therefore **converts "employer material in a separate repo" into "employer material in an ungoverned zone inside a governed tree."** This is a real, stated **cost of the ruling**, not a reason to reject it.
- **(c) The premise is unverified.** No content scan of `corp-monorepo` (or any repo) has been run, so "*if* there is any employer material" is an unverified premise. The fold shape must not be executed on an assumption about what is or isn't in a tree.

**Precondition (hard gate):** before any fold executes, a **content-and-history disposition scan** produces a per-class disposition for every path and every historical object in the trees being folded — classifying each as *never-committed* (→ `.gitignore` suffices), *already-committed* (→ history rewrite, or the path stays out of the fold), *excluded*, or *governed*. The scan must also quantify the resulting ungoverned blind zone and map every remote, hook, and CI workflow to its post-fold owner. **No path or historical object may be unclassified when a fold begins.**

### 3. The shape verdict — PARTIAL (re-derived on engineering grounds only)

**Recommendation: PARTIAL fold. Not FULL, not NO.** The recommended default is a **narrow, domain-scoped consolidation**, with the fleet remaining a governed polyrepo.

**Did the answer change?** The *verdict* stayed PARTIAL, but the *reasoning changed entirely*, and this is the load-bearing point:

- The prior PARTIAL rested mainly on the **compliance boundary** (work tree vs personal tree). The ruling removes that pillar.
- Removing it **does not strengthen the case for a FULL fold** — the remaining engineering factors still argue against aggressive folding, and the ruling's own `.gitignore` mechanism *adds* a cost (the ungoverned zone, caveat b) that argues **specifically against folding the employer repo** into the universal tree.
- So the shape is re-grounded on: unfold-cost asymmetry, pre-sales blast radius, the product/domain-scoping of every repo, worktree-substitutability of the leading justification, and the new ungoverned-zone cost — **not** compliance.

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

**The divergence, NOT reconciled — for the architect to settle:** both land on PARTIAL, but on *aggressiveness*. **sol goes 9 → 5 trees** (confidently folding corp-ops/corp-sca into the corporate tree and creating a workstation tree for terminal-setup+win-tooling). **The architect is narrower** — corp consolidation gated on the content-scan, terminal-setup/win-tooling kept standalone absent a demonstrated shared-release benefit, trending toward the minimal defensible fold. The gap is whether to consolidate the workstation-tooling and the corp-satellite repos *now* on the operational-surface argument (sol), or to fold only the already-planned corp domain and hold the rest as governed polyrepo (architect). Both agree this is a recommendation the operator accepts, amends, or rejects.

## Consequences

- **Governed polyrepo is the retained default.** The hub keeps governing all trees; the methodology layer is fold-invariant, so the hub's value is unaffected by the shape chosen.
- **The plural-only estate is not retired by a PARTIAL fold** — only per-repo duplication within a consolidated tree is removed. The 15,409-line saving is available only at a FULL fold, which is rejected on the five factors above. This is the priced trade-off, stated plainly.
- **The ruling introduces an ungoverned zone.** Whatever fold executes, gitignored employer material becomes invisible to `audit.py`/`fleet_parity`; the precondition scan must quantify that blind zone so the governance claims stay honest (candidate follow-up: a governed-coverage metric that reports the ignored surface).
- **Downstream chain is gated on this ADR's acceptance, not this draft.** #382 (desired-state schema; its matrix width is set by the ruled tree count) → #383 (execution waves, worktrees singly) → #385 (tech-currency). The E9 brake ("no new fleet machinery until the shape is ruled") holds until this ADR is **accepted and merged**.
- **No execution here.** No repo moves, no history rewrites, no machinery. Acceptance closes `[#381]`; the first fold action is a separate ruling after the precondition scan.

## Alternatives considered

- **FULL fold (all 9 → one tree) — rejected.** It is the only shape that retires the whole 15,409-line estate (sol's steelman), but: the unfold-cost asymmetry makes it a near-one-way door; it maximizes pre-sales blast radius; every repo is product/domain-scoped so the fold has no domain logic; worktrees already deliver the agent-lane isolation that was its leading justification; and the ruling's own `.gitignore` mechanism places the largest ungoverned zone inside the universal tree. The savings are real but do not clear these costs at 5–8+ repos.
- **NO fold (status-quo polyrepo) — rejected as the stated recommendation, but it is the fallback.** The architect recommendation is *close* to it — a narrow domain consolidation over a retained polyrepo. Pure NO-fold forgoes the already-planned `demo-prep → corp` consolidation and the operational-surface reduction that a domain tree captures cheaply, so a narrow PARTIAL is preferred to strict NO.
- **PARTIAL along the compliance boundary (the prior recommendation) — superseded by the ruling.** It drew a work tree vs a personal tree along the employer-data line; the operator's ruling removes that line, so the boundary is re-drawn on domain/blast-radius grounds instead.

*Scale note: priced at the real 5–8+ repos (live fleet = 9 git repos). The "10–20 repo" figure that appeared in the 2026-07-21 audit and three handoff files is fabricated and is not used here (intake #16 §4 item 2).*
