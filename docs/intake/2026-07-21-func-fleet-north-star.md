---
intake-id: 16
status: DRAFT
origin: Layer-1 browser architect consolidation, 2026-07-21 — consolidates the operator's dictated vision (2026-07-20/21), the Fable vision audit, the polyrepo recon brief (2026-07-21), the assets/ delivery session, and three months of session lessons
consumers: (a) the polyrepo shape-ruling session — consumes §4; (b) the desired-state ADR session — consumes §1–§3 and §5
consumed-by:
---

# FLEET NORTH STAR — Consolidated Vision & Plan
**Date:** 2026-07-21 · **Author:** Layer-1 browser architect · **Status:** SEED for (a) the polyrepo ruling session and (b) the desired-state intake→ADR
**Supersedes nothing; consolidates:** the operator's dictated vision (2026-07-20/21), the Fable vision audit, the polyrepo recon brief (2026-07-21), the assets/ delivery session, and three months of session lessons.

---

## 0. What shipped today (educate: change · why · what-next)

**Change.** `assets/` is gone from ai-council (merge `88b0876`, --no-ff): the vestigial `ruff-pre-commit.yaml` deleted, its two live references repaired (`INSTALL.md §2` now points at the live hook `astral-sh/ruff-pre-commit @ v0.15.5`; the obsolete sentence removed from `.claude/settings.json`), the supersession of the 2026-07-11 "kept" disposition recorded live in ai-council's JOURNAL. Gates green (pre-commit 9/9, ship-gate EXIT 0). Witness fact (a) confirmed by the operator's own terminal. **Push pending — operator's call.**

**Why it matters.** Not the 1 KB file. This was the first end-to-end pass of the delivery loop after 3–5 sessions of plan-without-ship, and every safety mechanism fired for real: the unfiltered live-session check **blocked** a merge under a live session (the exact class that corrupted hub main the night before), the frozen contract held, terra reviewed before merge, and closure was defined as *operator-witnessed*, not *merged*. **The loop is proven repeatable. That is the deliverable.**

**What next.** The loop now gets pointed at the system the operator actually wants (below). One hygiene item rides along: the fabricated "10–20 repo" figure must be corrected to the real 5–8+ in the three handoff files it propagated into.

---

## 1. The vision, consolidated (operator-dictated, layered)

A **system, not hole-patching** — built on real data structures and existing libraries, never hand-rolled from zero.

| Layer | Scope | Today |
|---|---|---|
| **L0** | Names + folder/file structure as managed state (caches, `.claude` surface incl. skills, archives-inside-each-folder, docs layout) | ~25% — fragments, 4 registries, no single contract |
| **L1** | Dependency architecture: doc2doc + doc2file edges, hooks, skills; rot detection from day one | ~45% — ADR-88/89, doc-code-edge.yaml, freshness checks live |
| **L2** | Methodology versioning + deployment: PLAYBOOK, CLAUDE.md, managed files, review system | ~40% — manifest/carriers half-built (editor-config `implemented:false`) |
| **L3** | Full lifecycle: intake → ADR → build → archive → real deletion; Q&A, looping, harness | harness ~80% (proven today); archive/safe_remove decided, unbuilt |
| **L4** | Tech-currency: research new Python tech/versions online → rule → **distribute** through the deploy channel | ~5% — one-offs only |
| **L5** *(new, 2026-07-21)* | **Predictive layer:** a local model that learns from how we work — logs, decisions, file traffic — so the fleet predicts dependencies, finds rot, flags risk ("the repo learns us") | 0% — designed below |

The honest shape of the gap: **the hardest layer (harness) is the furthest along; the simplest (L0 as a system) is nearest zero.** Cause, not accident — the fleet built *checks* instead of *one data model*, and grew fleet machinery under a repo-shape nobody ever argued.

---

## 2. The architecture: **the Terraform model, not the Terraform tool**

The operator's instinct is exactly the industry pattern — GitOps / Infrastructure-as-Code: *desired state declared as versioned data in git → a reconciliation loop observes actual state, diffs it, and converges → drift is detected, rollback is a git revert.* The 2026 refinement ("configuration-as-data") says: intent as **structured, versioned data**, not templated text — which is precisely the pydantic-schema direction.

Terraform itself manages cloud resources through providers; for local-disk repos the tool doesn't apply but the model does — the same ruling shape as Copier ("adopt the deletion-propagation model, not the tool", 2026-07-03, do-not-relitigate).

**The mapping, concrete and library-based:**

| Terraform concept | Fleet implementation | Library |
|---|---|---|
| Declarative config (.tf) | ONE schema-versioned desired-state contract in `ecosystem/` — dissolves the 4-registry sprawl | **pydantic** |
| Dependency graph | doc2doc / doc2file / hooks / skills edges; rot = a graph query (nodes with no fresh edges) | **networkx** |
| `terraform plan` | Divergence report: surface × repo × {conform / diverge / declared} — read in 2 minutes | **pandas** |
| `terraform apply` | The existing **regenerate-and-diff** machinery + carriers (the hub is already projen-shaped) | existing hub code |
| State file | `deployed-versions.yaml` + per-consumer version-pin scalar (the one idea kept from Copier) | existing |
| Drift detection | Nightly reconcile run producing the plan-report; "done" for any wave = **zero undeclared divergence** | derived from schema |

**What stays custom (and only this):** the methodology layer — ADR lifecycle, handoff harness, census, JOURNAL gates. No library does it; it sits *on top of* the schema, never beside it.

**The trust consequence (the point of all of it):** the operator stops verifying anything by hand. "Done" stops being anyone's word and becomes a mechanical report. The current distrust is the *correct* response to the mechanism not existing yet.

---

## 3. The predictive layer (L5) — how predictive AI is actually used in software development, 2026

State of practice, from research: predictive quality analytics is mainstream — ML models trained on **change history, complexity, and defect data** forecast high-risk modules (industry reports cite ~87% accuracy and 30–35% fewer critical defects reaching production); the mature product pattern is **behavioral code analysis** (CodeScene): **hotspots** (where activity concentrates — a power law in every codebase) and **change coupling** (files that change *together* over time = learned, temporal dependencies that static analysis can't see). That last one **is** the operator's "repo learns how we walk the graph."

**Our build, honest sequencing:**

- **L5a — descriptive/diagnostic (cheap, now-capable, no ML):** mine our own history — git commits, JOURNAL, session transcripts, gate results — with **PyDriller** (the standard Python MSR framework, feeds straight into pandas) → compute hotspots, change coupling, knowledge/rot maps per repo and fleet-wide. Runs as a nightly lane. This already answers "where is it rotting, what silently depends on what, where do we keep going."
- **L5b — predictive (gated on data volume):** simple models (risk scoring per change, defect-prone-file prediction) on top of L5a's frames — scikit-learn class, not a platform. At n≈3 repos and one operator, heavy ML now would be ceremony; the gate is "L5a frames show enough signal."
- **Frame discipline:** the Splunk analogy is honored at the *data* level, but the SIEM ruling stands — the fleet is nightly cooperative **state-diff**, not real-time adversarial event-stream. L5 *reads* the same event data; it does not resurrect ingestion machinery.

---

## 4. The polyrepo ruling — inputs distilled (decision is the operator's, in its own session)

The recon (2026-07-21, read-only) re-prices the bet. Facts, none of which is a decision:

1. **Never argued.** 78 ADRs; zero weigh monorepo vs polyrepo. ADR-28 self-declares descriptive ("names an operating pattern already in place"). The shape entered canon as an observation.
2. **The 10–20 target is fabricated.** It exists only in the 2026-07-21 audit + its downstream files. Live requirements say **5–8+**. Correction owed in 3 handoff files. (Architect's own miss, owned: I repeated the number unverified in earlier turns — propose-then-verify failed there.) Directional consequence: the dissolution case *weakens* at the real 5–8.
3. **The fold's savings are real but smaller than the audit implies:** ~4,200 lines of plural-only machinery + 4 registries dissolve (fleet_parity 1974 ln, 7 carriers + 6 manifests, floor generator, boundary_report…); but "the collector" was never built (can't be counted as savings), and worktree guards + the ownership axis + handoff harness + census **survive** any fold.
4. **The leading justification is substitutable.** Agent-lane isolation via separate repos is equally delivered by worktrees, which the fleet already operates with a documented decision gate and witnessed 5-concurrent-lane history. ADR-61's "different repos parallelize freely" is a *consequence* of the split, not its cause.
5. **Counter-evidence is one-sided:** every registry-recorded repo purpose is product/domain-scoped; corp-monorepo is *itself* a deliberate monorepo (tach.toml boundaries); demo-prep is already scheduled to fold into corp.
6. **Three material items are unpriced and MUST be in the ADR:** (a) the cost of *unfolding* if the fold is wrong; (b) whether the **Blue Yonder employer-data boundary** can legally/compliantly share a tree with personal repos — a hard constraint, not a preference; (c) blast radius on live pre-sales work (DECISION_28:92 rejected push-down enforcement precisely to avoid disrupting it).
7. Both falsification hooks are month-scale — instruments for *after* the ruling, not inside it. H8 rewritten at 5–8.

**Architect's recommendation (to be graded as strictly as anyone's):** the evidence points at a **partial fold along the compliance boundary**, not a binary. Target shape: a *work tree* (corp-monorepo absorbing demo-prep per its own charter, likely corp-ops/corp-sca) and a *personal tree* (life-architect), with the hub governing both — "fewer repos," not "one repo." At 2–3 trees most plural-only machinery still dissolves, the BY boundary is respected by construction, and the desired-state matrix narrows before it is built. The ruling session accepts, amends, or rejects this — with item 6 priced first.

---

## 5. Lessons codified (three months of mistakes, as design rules)

1. **One data model, not N registries.** Every check derives from the schema; a check without a schema row is the registry-sprawl anti-pattern. (Kills the witnessed "green that means nothing" class: phantom enforcement, filtered review, non-distinguishing assertions, one-directional verification.)
2. **Decide the bet before building its machinery.** The standing brake (JOURNAL.md:76) generalizes: shape rulings precede structure investment.
3. **Prove, then codify.** Working discipline enters PLAYBOOK after it has shipped once — never as a substitute for shipping.
4. **Witnessed, not merged.** Closure is the operator's eye or a mechanical report — never a proxy.
5. **Adopt the model, not the tool** when the tool's substrate doesn't match (Copier → regenerate; Terraform → reconcile loop; Splunk → the data frame, not the platform).
6. **Verify numbers before they propagate.** The 10–20 figure crossed from one audit into three handoff files in a day. Load-bearing figures get a live re-derivation before reuse.
7. **Meta serves object.** Every session's success metric is a visible, witnessed change; planning artifacts are enablers or they are distractions.

---

## 6. The plan — sequenced, each link unblocks the next

| # | Step | Gate to advance | Owner |
|---|---|---|---|
| 1 | **Close assets/**: `git push` from ai-council main; educate = §0 of this doc | Operator pushes + confirms §0 landed | Operator / architect |
| 2 | **Polyrepo ruling session** — inputs: recon brief + §4; price the three unpriced items first; correct 10–20→5–8 in the 3 handoff files | Operator ruling recorded as the fleet's **first shape ADR** | Operator (architect recommends) |
| 3 | **Desired-state intake → ADR** — the §2 architecture (pydantic + networkx + pandas + regenerate/apply + state file), matrix width set by the ruling; L0 surfaces from the operator's checklist (caches, `.claude`+skills, archives, docs layout, Python parity, colours-via-carrier) | ADR accepted; schema v1 committed | Architect → CC |
| 4 | **Execution waves per surface** — worktrees launched singly, one in focus at a time; wave-done = **the pandas report shows zero undeclared divergence** for that surface | Report-green per wave, operator reads the report | CC (architect reviews) |
| 5 | **L5a analytics lane** — nightly PyDriller mining → hotspot/change-coupling/rot frames per repo + fleet | First frames reviewed; rot findings become tickets | CC nightly |
| 6 | **L4 tech-currency lane** — nightly research → version-bump proposals written *into the contract* → ruled → distributed via the apply channel | First proposal flows contract→deploy end-to-end | CC nightly / operator rules |
| 7 | **L5b predictive** — risk scoring on L5a frames | Gated: L5a shows signal volume | later |

**Standing constraints across all steps:** no new fleet machinery before step 2 rules (the brake) · PLAYBOOK codification of the delivery loop rides after step 1 (prove→codify) · the buy-vs-build intake is rewritten before ingest (it argued for the rejected engine) · plan-governs: new scope files as backlog, never derails the active lane.

---

*This document is the seed artifact. Step 2 consumes §4; step 3 consumes §1–§3 and §5. It is deliberately not an ADR — it evolves; ADRs it spawns do not.*
