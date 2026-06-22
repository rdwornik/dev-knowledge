# HANDOFF_PROCESS — comprehensive audit & rework agenda

<!-- scope: meta -->

- **Date:** 2026-06-23
- **Type:** audit (analysis + proposal — NO implementation; decisions route to Council/architect)
- **Author:** CC (Claude Code), Opus max-effort, fresh session
- **Scope:** the whole HANDOFF_PROCESS v5.2 surface — spec, boot, command, probe machinery, the live bundle artifact
- **Status:** findings standing as a decidable rework agenda. Opens the rework; closes no backlog task.
- **Verified against live files** (not the briefs' characterization): `protocols/HANDOFF_PROCESS.md` (575 L, v5.2), `protocols/HANDOFF_BOOT.md`, `.claude/commands/handoff.md`, `scripts/verify_handoff_probes.py`, `scripts/audit.py`, `protocols/DEFINITION_OF_DONE.md`, `protocols/ESSENTIALS.md`, PLAYBOOK §2/§"Parallel sessions", ADRs 82/85/87, BACKLOG, the live `2026-06-21-dev-knowledge-architect` bundle.

---

## 0. Provenance, method, and two brief-premise corrections

**Method.** Grades are weighted in the prompt's order: (1) this session's observed failures (empirical, highest), (2) the live spec + repo state (verify-don't-assert), (3) the three architect briefs (weighed, not adopted). Every state claim below was re-derived from the live file; citations are `file:line` / SHA / probe-id / `#id`.

**Provenance limit — the three briefs are NOT attached and do NOT exist as files.** A grep for their distinctive terms (`decision-verification asymmetry`, `prompt-corpus staleness`, `acceptance-contract`, `complexity-budget`) returns nothing in the repo, and no attachments were delivered to this session. I worked from the prompt's *characterizations* of Brief A/B/C (D1/D2/D5; source→gate→agent; acceptance-contract invariant). **The brief weighing in §7 is therefore against the prompt's summary of each brief, not the full text** — a fidelity gap the architect should note, because it is exactly the off-repo input CC cannot self-verify (see §8).

**Correction 1 — ADR-60 mis-cited.** The prompt cites "ADR-60 (retired calendar-review — the on-trigger-not-calendar precedent)." `docs/decisions/ADR-60-docs-folder-taxonomy.md` is the **docs/ folder taxonomy** — it has nothing to do with a retired calendar review. The *principle* (act on a trigger, not a calendar) is genuinely repo-established, but its real carriers are `/changelog-review` (PUSH-triggered, not nightly), #134 backlog-grooming ("POST-ARC — obsolescence is event-driven; the n=1 calendar-style pass found 0 kills"), and ADR-76. I use those as the precedent; the ADR-60 citation is dropped.

**Correction 2 — a probe the spec calls "deferred" actually shipped.** §1 of T2/T4 below: `scripts/verify_handoff_probes.py` (#163) exists and gates `/ship`, but the spec still describes it as deferred. Verified, not assumed.

---

## 1. Headline — GRADE counts + the one-line verdict

**KEEP 12 · CUT 6 · ADD 3 (all 3 route to *exercise/relocate existing*, not *build new*).**

> **The verdict in one line:** the thesis is **substantially right about the diagnosis and wrong about the prescription**. The verification topology *is* lopsided (T1 ✓) and the repo *has* matured past parts of the state-ritual (T2 ✓), but the three "things to build" (T3) are **already designed and partly shipped** — ADR-87 + #184 (role), the #194 coverage-test-as-inventory (acceptance contracts), #156's durable serialize-group/depends-on schema (backlog spine). The audit's real payload is therefore **CUT the accreted ritual + dead v4 corpus + stale spec text, and make three already-existing mechanisms *resident/exercised*, not invent them.** Routing three "ADDs" to net-new machinery would itself fail the complexity-budget gate (§6).

---

## 2. Thesis verdicts (T1–T4) — pressure-tested against evidence

### T1 — "The verification topology is inverted." **CONFIRMED, with a sharpened remedy.**

The handoff carries **nine** live-state probes (`PROBES.md` P1a/b orientation + P2–P9 state) plus a structural teeth validator that gates `/ship`. Role-behavior carries **zero teeth** — it lives as prose in `HANDOFF_BOOT.md` "Architect mode" and the §7 plan-review contract. So state gets teeth; role gets good intentions. The asymmetry is real.

**The correction the evidence forces:** the remedy is **not** "remove state teeth." State probes are nearly free — they reuse read-only validators that already exist (`audit.py`, `validate_git_backlog`), and the anti-bluff design is the genuine v5 innovation that *worked*. The remedy is **additive on the role side** (make the role contract resident at the point of action + give it a self-check), plus a **modest consolidation** of the probe *set* (T2). T1's framing of "teeth on the cheap-to-recompute, intentions on the expensive-to-recover" is rhetorically right but must not license gutting the part that works.

### T2 — "Repo maturity made state-probes partly redundant." **CONFIRMED, with a precise boundary.**

Evidence the repo now self-enforces what the handoff used to prove by hand:
- `scripts/verify_handoff_probes.py` (#163) **landed** and is wired as `audit.py check_handoff_probes` (registered in `ALL_CHECKS`, `audit.py:1660`), mapping a malformed/dangling probe to a **gating** Finding so `/ship` blocks.
- `audit.py` is 23 checks; `validate_doc_claims` / `validate_git_backlog` / `canonical_freshness` self-enforce the facts P2/P4/P5/P6/P7/P9 probe.
- The probes themselves now say *"re-derive, don't trust this line"* (`PROBES.md` P3/P7) — CC re-derives live state regardless of the handoff.

**The boundary T2 must respect:** the gates verify the **repo is internally consistent**; the probes verify the **receiver actually opened primary source** (anti-bluff). Those are **orthogonal**, not redundant. So the shrink is specific: probes P2/P4/P5/P6/P7/P9 each re-run a validator and can collapse into **one `audit.py ship-gate` invocation** the receiver must run; the **anti-bluff function and the orientation read are not redundant** and stay. Net: shrink the probe *set*, keep the teeth *function*. (This is the strong-CUT that Brief A's D2 names — see §7.)

### T3 — "Three under-served dimensions." **CONFIRMED as gaps; REFRAMED as already-filed.**

All three are real and observed. But none is *missing* — each has a backlog item and partial implementation, which changes the routing from "build" to "exercise/relocate":
- **Role operationalization** — real (the session's central failure, §2-evidence). Owned by **ADR-87** (the equilibrium contract, codified across PLAYBOOK §2 / ESSENTIALS / HANDOFF_BOOT), **#184** (demonstrate it on a real build — still open), **#200** (merge-serialization gate — the two-`/ship` near-tangle, *already filed*). The gap is **residence + a self-check**, not a new contract.
- **Testing-as-architecture** — real and **already proven this very week**: #194 Phase-A committed "an xfail-strict coverage test whose failing output IS the rollout inventory" *before* annotating anything (JOURNAL 2026-06-22). That is Brief C's acceptance-contract-authored-upstream, demonstrated. The gap is **generalization** (#144 already asks to sharpen ADR-81(d) "done" to an end-to-end contract).
- **Backlog-as-navigation** — real. #156 **shipped** the durable task-graph (`depends-on` / `serialize-group` schema, enforced read-only in `validate_backlog.py`). The gap is the **opening move**: the orientation-grep is the architect's scripted first move (§13c) but the evidence says it "didn't change behavior."

### T4 — "Prompt-staleness in the handoff itself." **CONFIRMED for accretion-staleness; PARTIALLY REFUTED for the "weaker-model patch" framing.**

Confirmed staleness (concrete, verified):
- `.claude/commands/handoff.md` carries a **complete dead v4 8-file two-phase generator** (the "## Conventions" / "## Phase 1" / "## Phase 2" / "## Hard constraints" sections, ~200 lines) under a "superseded" flag. It is the command that fires on `/handoff` today, with v5 bolted on top.
- **Stale-in-two-places:** the spec §11 ("the bespoke read-only teeth validator was deferred to a post-flip ticket; until it lands, the manual probe-gate covers v5-bundle validation") **and** `audit.py:608` (same claim) both describe `verify_handoff_probes.py` as not-yet-landed. It landed (#163).
- §13 is ~320 lines carrying **two full descriptions of the supplement** (the dead v5.1 ephemeral-interview form and the live v5.2 always-generated-file form), plus inline superseded "three-file bundle" text under a later "four-file PASTE_THIS" entry. Heavy amendment scar tissue.

**The refutation:** the prompt's *specific* T4 sub-claim — "emphatic instructions written for WEAKER models that now over-trigger on Opus" — is **not** what the evidence shows. The repetition that looks like over-scaffolding is mostly **architectural emphasis that is model-independent**: "never assume a CC-held file reaches the file-less browser" (repeated 3×) is a true structural constraint (the browser genuinely has no file access — it is not a model weakness); the four-tag claim discipline (`witnessed/recall/inferred/unknown`) is epistemic hygiene that applies to Opus too (Opus still faces the compaction-summary-vs-live-state gap the whole teeth design exists for). The staleness is **version-accretion** (v3→v5.2) and **architectural redundancy**, not generation-patching. So: CUT the accreted/dead text; **do not** CUT the emphasis as "weaker-model residue" — that test mostly fails to reproduce.

---

## 3. GRADE table

Every mechanism marked **KEEP / CUT / ADD**, with the session evidence, the hard metric that should gate it, and the routing.

### KEEP (12) — proven, cheap, or architecturally load-bearing

| # | Mechanism | Session evidence | Hard metric | Route |
|---|---|---|---|---|
| K1 | Teeth-y anti-bluff read design (§5) — answer exists only in live state | The core v5 innovation; the failure it fixed (summary-bluffable v4 questions) does not recur | A probe is admissible only if it fails when answered from the compaction summary alone (§5 dogfood) | KEEP as-is |
| K2 | `verify_handoff_probes.py` structural teeth validator (#163), gating `/ship` | Landed since the spec was written; self-enforces probe *structure* | A malformed/dangling-source probe FAILs `audit.py ship-gate` (already true) | KEEP; **fix the spec text that calls it deferred** (→ C5) |
| K3 | Drift-flags-as-headline (§2; residual §1) | The 2026-06-21 residual leads with the `[stale] disposition` + ship-gate verdict — surfaced first, not buried | Residual §1 is drift-flags and nothing above it | KEEP |
| K4 | Lean task-state = pointer to `BACKLOG.md` + branches + drift-flag (§6) | No re-narration drift observed; the pointer + #156 schema carry it | Handoff re-narrates zero `#id` bodies | KEEP |
| K5 | The residual = un-committed "why" + pointers (§2) | The irreducible thing only the prior session holds; v4-kept-right | Residual contains only non-repo-derivable content (no methodology copy) | KEEP |
| K6 | Verification split — browser=artifact, CC=state fidelity (§8) | Matches the file-access reality; no observed failure | Each actor checks only what it is positioned to check | KEEP |
| K7 | Plan-review output contract — 3 forms only (§7) | Directly targets the "operator had to re-explain how to answer plan-mode questions" failure | Browser emits exactly one of {select option / paste-ready text / approve} | KEEP but **make resident + strengthen** (→ A1); the failure recurred, so prose alone is under-delivering |
| K8 | Self-updating `/handoff` — version/pointers read live, never hardcoded (§10) | The de-hardcode pattern; no version-drift observed in v5 stamps | `/handoff` carries no hand-copied version or methodology prose | KEEP |
| K9 | Modes: architect \| execution (§13) | The architect bundle (5 files, rich residual) vs execution bundle (3 files) is a real, working distinction | Mode selects residual profile + browser posture deterministically | KEEP |
| K10 | Browser operating role **resident in the boot** (§4, HANDOFF_BOOT) | Architectural necessity — a CC-held file never reaches the file-less browser | The role is in `HANDOFF_BOOT.md`, not only in the CC-held spec | KEEP (refutes a T4 "redundant emphasis" cut) |
| K11 | Escalation ladder / degrade-loudly (§10) | No fabricated-pass observed; the contract is sound | A probe that can't be answered → FAIL/abort, never synthesized pass | KEEP |
| K12 | Empirical dogfood as the teeth **promotion** gate (§5/§11) | The right gate-shape: prove teeth bite by attempting to bluff | At promotion, every probe must fail to be bluffed from the summary | KEEP (semantic teeth; complements K2's structural teeth) |

### CUT (6) — redundant ritual or stale/dead text

| # | Mechanism to cut | Why now redundant / non-reproducing | Hard metric (admissibility of the cut) | Route |
|---|---|---|---|---|
| C1 | The dead v4 8-file two-phase generator in `.claude/commands/handoff.md` (~200 L) | Superseded by the v5 residual/probe/boot flow; flagged "superseded" in-file but still resident and still the command that fires | The v5 generator (#164) emits the four-file bundle, after which the v4 prose is provably unreachable | **#164** (already scoped to remove it; **ADR-83 LIVE constraint:** v4 templates stay live for corp-monorepo until it migrates) |
| C2 | Probe-set redundancy — 9 probes where P2/P4/P5/P6/P7/P9 each re-run a validator | The repo self-verifies these (T2); one `audit.py ship-gate` call recovers them | Every cut probe's fact is provably reproduced by a single named validator the receiver still runs | **#161** (the capture-only "stable teeth probe-core" item — this is its scoping decision) |
| C3 | Orientation-grep as the architect's scripted **first move** (§13c P1a/b) | Empirically "didn't change behavior" (session evidence); the backlog is the real navigation spine (T3). The exact-line read is a clever anti-bluff design but its *primacy* is the ritual | Demote: the first move becomes vision→backlog (A3); orientation, if kept, is a cheap secondary read, not the gate | **AI Council / architect ruling** (it is currently a normative §13c gate) |
| C4 | §13 supplement scar tissue — the dead v5.1 ephemeral-interview description coexisting with the live v5.2 always-file description | v5.2 superseded v5.1's mechanism; carrying both full descriptions inflates the most-read section | The live §13 describes the supplement once; the v5.1 mechanism lives only in Section history | **ADR-82 amendment / spec edit** (immutable-ADR-safe: append the supersession marker, condense the body) |
| C5 | Stale "verify_handoff_probes deferred / manual gate covers" text — spec §11 **and** `audit.py:608` | The validator landed (#163, K2); the text is false in two places | Both surfaces state the validator is live + gating; neither says "until it lands" | **spec edit + code-comment edit** (mechanical; pairs with C1/#164) |
| C6 | The 40 KB / 474-line `PASTE_THIS.md` single-paste as the "thin boot" | The v5 thesis is a *thin* boot; the live architect paste is 474 lines (a full concatenation of boot+residual+probes+supplement). It is a real convenience (one paste vs hand-feeding) but it is not "thin," and it duplicates the bundle files | The pasted payload carries no content recoverable by CC on demand (e.g. methodology stays pointer-only; the residual is the only irreducible bulk) | **#164** (the assembler owns `PASTE_THIS`); decide thin-paste-vs-one-paste tradeoff there |

> **Admissibility note (per the prompt's hard metric):** every CUT above is either (a) provably recoverable from the repo's own self-verification (C2 → `ship-gate`; C5 → the live `check_handoff_probes`), or (b) provably dead/superseded text (C1, C4), or (c) an empirically-observed no-behavior-change ritual (C3), or (d) a measurable thinness violation (C6). None prunes a fact the repo does not self-verify.

### ADD (3) — intent-level only; **all route to exercise/relocate, not build**

Detailed in §5; each clears the complexity-budget gate in §6.

| # | ADD (intent) | Already-exists | The actual gap | Route |
|---|---|---|---|---|
| A1 | **Architect Operating Contract** — resident role loop + role-stability self-check + serialized-merge-as-a-GATE | ADR-87 (contract), §7 plan-review contract, #200 (merge-serialization filed), #184 (demo owed) | **Residence at point-of-action** + a one-line self-check + promoting #200 from "filed" to designed | Relocate to HANDOFF_BOOT (resident); **#200** (Council) for the merge gate; **#184** exercises it |
| A2 | **Test-first acceptance contracts** — frozen "done" authored upstream, immutable to CC, gamed-check on review | #194 coverage-test-as-inventory (proven 2026-06-22); ADR-81(d); #144 (E2E DoD sharpening) | **Generalize** the proven pattern into the prompt contract + a DoD clause, **scoped to build tasks** | **#144** + a `DEFINITION_OF_DONE.md` clause; ADR-81 amendment |
| A3 | **Backlog-as-navigation-spine** — open at vision→backlog; backlog drives the architect | #156 (durable serialize-group/depends-on schema, shipped); §13b task-state pointer | **Reorder the opening move** (backlog before/over orientation-grep) — a net *cut* in complexity | **architect ruling** + spec §13 reorder (pairs with C3) |

---

## 4. The CUT set, justified (each names its self-enforcer or non-reproduction)

- **C1 (v4 dead corpus)** — self-enforced-by: the v5 generator (#164) makes the v4 path unreachable; until then it is inert text behind a "superseded" banner. *Non-admissible alternative rejected:* deleting it now would break corp-monorepo's live v4 cross-repo path (ADR-83 constraint in #164). So the cut is **gated**, not immediate.
- **C2 (probe redundancy)** — self-enforced-by: `audit.py ship-gate` returns P7's verdict + P2's check count + P4's `git_backlog_drift` + P5's `canonical_freshness` + P6's `pytest_collected` + P9's serialize-groups in one (or two) calls. The probe *fact* is recoverable; only the **anti-bluff act of running it** must remain. So C2 consolidates 6 probes → "run `ship-gate` and read it back," keeping P1 (orientation, if retained) + P3 (HEAD/sync, genuinely volatile) + P8 (bundle-shape, spec∩filesystem).
- **C3 (orientation-grep primacy)** — non-reproduction: the session evidence is explicit that the vision/arch orientation read "didn't change behavior." It is not *wrong* (the exact-line teeth are valid), it is *low-leverage as a first move*. Demote, don't delete.
- **C4 (supplement scar tissue)** — superseded-by: v5.2's always-generated file strictly replaces v5.1's ephemeral block (ADR-82 2026-06-17 amendment). The live section needs one description; the other is history.
- **C5 (deferred-validator text)** — non-reproduction: `check_handoff_probes` is in `ALL_CHECKS` and gating (verified `audit.py:1441/1660`). The "until it lands" clause is counterfactual. Mechanical fix.
- **C6 (40 KB paste)** — measurable: the live `PASTE_THIS.md` is 474 lines / ~40 KB. "Thin boot" (§4) and a 40 KB paste are in tension; the resolution (accept the one-paste tradeoff, or thin it) belongs to #164. Surfaced, not decided here.

---

## 5. The ADD set — intent + hard metric + routing (NOT implemented)

### A1 — The Architect Operating Contract (resident role-behavior)

**Intent.** The session's central, repeated failure was **role-drift**, not mechanism-failure: the architect deferred to CC's plan-mode output as authoritative (the operator had to re-assert that *CC produces, the architect reviews*); skipped its own designed review-gate (Phase A→B ran in one session; the cohort-1 scope decision was CC's); over-narrowed before establishing the frame; and two concurrent `/ship`s nearly corrupted `main`, "resolved by accident." The operating loop — **decide → plan → delegate-with-declared-mode → verify-landed → archive → educate-the-operator** — plus a **role-stability self-check** (*am I deciding/reviewing, or deferring to CC's framing?*) and a **parallel-work protocol** (disjoint file sets + **serialized-merge-as-a-GATE** + a worktree-state tracker) must be **resident where the role acts**, not buried in a CC-held spec or PLAYBOOK.

**The honest scoping (what is genuinely new vs already-owned).** The *contract* exists (ADR-87); the *merge-serialization need* is filed (#200); the *empirical demo* is owed (#184); the parallel-work discipline is in PLAYBOOK §"Parallel sessions". The **net-new** is small and exactly right: (a) **residence** — the role loop + self-check belong in `HANDOFF_BOOT.md` (the only artifact the file-less browser reads), because the observed pain is *constant reminding*, which is the definition of not-resident-enough; (b) **serialized-merge-as-a-gate** — promote #200 from prose to a mechanism (refuse a second concurrent merge-to-`main`).

**Hard metric.** A fresh architect, from the boot alone, (1) states "CC produces, I review" before acting on any CC plan-mode output; (2) cannot run two `/ship`s into `main` concurrently (the gate refuses the second); (3) the role loop is in `HANDOFF_BOOT.md`, verifiable by grep. The empirical close is #184 (a real build where the contract holds).

**Route.** Relocate the role loop + self-check into HANDOFF_BOOT (spec edit, architect). The merge gate → **#200 (AI Council candidate** — it is a design decision: merge-lock vs refuse-on-`MERGE_HEAD`, hub-vs-fleet scope). The demonstration → **#184**.

### A2 — Test-first acceptance contracts (frozen, immutable-to-CC)

**Intent.** "Done" was treated as a state-check; the **coverage-test-as-inventory worked precisely because it made "done" an executable contract authored before the build** (#194 Phase-A: the xfail-strict test whose failing output *is* the rollout inventory, committed before any annotation). Generalize: a build task gets an **acceptance contract** (Given/When/Then + I/O examples + closure criterion), **architect-authored, upstream of CC, shipped as a FROZEN first deliverable in the prompt, immutable to CC** (CC may add tests, never weaken the gate), with **review checking for gaming** (assertion removal, input-specific branching, scope-narrowing) — not just green status.

**Hard metric.** No **build** lands without its frozen acceptance contract green; review verifies the contract was not gamed (the assertions are the originals, the scope is not narrowed). For the #194 instance this already held — the xfail-strict decorator made a premature green *fail*, which is the immutability property in action.

**Route.** **#144** already asks to sharpen ADR-81(d) "done" to an end-to-end/user-flow contract — fold the frozen-acceptance-contract requirement there + add a clause to `protocols/DEFINITION_OF_DONE.md` (single-source DoD). **Scope it to build/code-impact tasks** — see the complexity gate (§6). ADR-81 amendment routes through the architect.

### A3 — Backlog-as-navigation-spine

**Intent.** The handoff should open at **vision→backlog**, and the backlog should drive the architect (or the architect builds the backlog, then delegates). The low-value vision/arch orientation-grep is demoted (C3). #156 already shipped the durable spine (`depends-on` / `serialize-group`), so the architect can *navigate* the task-graph, not re-read orientation prose.

**Hard metric.** An incoming architect reaches the correct first action **via the backlog** (the open `#id` + its serialize-group + drift-flag), not via re-reading orientation prose. Testable: the §13 opening move names BACKLOG as step 1; the orientation read, if retained, is secondary.

**Route.** Architect ruling + spec §13 reorder (pairs with C3). This is a **net reduction** in handoff complexity (it removes a scripted first move and replaces it with a pointer that already exists).

---

## 6. Complexity-budget self-check (Brief A's D5 applied to this audit)

Every ADD must clear: *"prevents a drift class OBSERVED this session > the complexity it adds,"* and must not exist solely to patch a prior amendment. **The gate's value here is that it forces the right scoping — it does not reject any ADD, but it shrinks all three to exercise/relocate.**

| ADD | Drift class OBSERVED this session? | Complexity added | Solely patching a prior amendment? | Verdict |
|---|---|---|---|---|
| A1 role contract | YES — deferred-to-CC, skipped-own-gate, over-narrowed, two-`/ship` near-tangle (all witnessed) | **Low** — relocate existing ADR-87 text to the boot + a 1-line self-check + promote #200; not new doctrine | No — it operationalizes ADR-87, but the *drift* is independently observed, so it is not patch-on-patch | **PASS** (scoped to residence + the merge gate) |
| A2 acceptance contracts | YES — "done" as state-check; counter-proven by #194's working pattern | **Low-if-scoped** — a frozen contract per *build* task (not every backlog item); reuses the proven #194 shape + #144 | No — extends ADR-81(d), which #144 already targets | **PASS** (scoped to build/code-impact tasks only; per-item-for-everything would FAIL the gate) |
| A3 backlog spine | YES — over-narrowing; orientation-grep no-behavior-change | **Negative** — it *cuts* a scripted first move (C3) and points at #156's existing schema | No | **PASS** (it is net-subtractive) |

**The audit applied to itself.** This audit must not become the refinement spiral it audits. It clears its own gate by **routing all three ADDs into existing backlog items (#144, #161, #184, #200) and spec relocations**, adding **no net-new mechanism** beyond promoting the already-filed #200 merge gate. The CUT set is larger than the ADD set, and the ADDs are subtractive or relocative — the net complexity of the rework is **down**.

---

## 7. Brief weighing (critical — demote the hypothesized, elevate the observed)

> Weighed against the prompt's *characterization* of each brief (the full briefs are not available — §0).

- **Brief A / D2 (prune ritual probes) — CONFIRM (strong CUT).** Maps to C2/T2. The repo self-verifies the state facts; the probe *set* can shrink to one `ship-gate` call + the genuinely-volatile/anti-bluff probes. Route #161.
- **Brief A / D1 (per-task decision-probe) — DEMOTE.** The prompt's test: is the observed failure *CC-violates-a-decision* or *architect-role-drift*? The evidence is unambiguous: the architect deferred to CC's framing, skipped its own gate, over-narrowed — **architect-role-drift**, not CC violating a recorded decision. A per-task probe that checks *CC honored a decision* aims at the wrong actor. The fix is **role residence (A1)**, not a decision-probe on CC. (If a future session shows CC actually overriding a frozen architect decision, D1 re-enters — but that is hypothesized, not observed.)
- **Brief A / D5 (complexity-budget self-check) — ADOPT** as the gate on this audit's own ADDs (§6). It did real work: it shrank all three ADDs to exercise/relocate.
- **Brief B (source→gate→agent reuse; weaker-model patches) — CONFIRM the reuse, PARTIALLY REFUTE the patch claim.** The `source→gate→agent` reuse is sound and already embodied: the teeth manifest reuses read-only validators (§5), and A1's merge gate should reuse the advisory-check shape rather than invent one. But the "patches for weaker models over-trigger now" finding mostly **does not reproduce** (T4): the handoff's emphatic repetition is architectural (file-less-browser) and epistemic (four-tag discipline), not generation-patching. CUT the *accreted* text (C1/C4/C5), not the *emphasis*.
- **Brief C (acceptance-contract authored upstream, immutable to executor) — ADOPT, and note it is already proven.** This IS A2. Its fit to the handoff is strong *and demonstrated*: #194 shipped exactly this (frozen-before-build, immutable-to-CC via xfail-strict). The handoff-specific move is to make it the **default prompt shape for build tasks** + a DoD clause, scoped per §6.

---

## 8. CC prompt-shape decision (the operational payoff)

**Given T2 + ADR-87, what should a CC prompt now CONTAIN?** Per ADR-87's verified finding (CC self-loads reliably **only** for code-impact tasks; GAP-1 read-only, GAP-2 gotchas, GAP-3 governance are unreliable):

**A prompt should contain:** *intent* + *the frozen acceptance contract* (A2, for builds) + *mode (with basis)* + *a THIN governance-pointer* (the ADR/LESSONS/sibling-spec it touches) + *off-repo inputs the architect uniquely holds*. **CC self-loads** the skeleton (PLAYBOOK §2, now CC's consumption-spec), code-impact context, generic gotchas, model/effort.

**Contrast with the observed prompt shape — THIS audit prompt is the live instance.** It is long, but **correctly long for its class**: an audit is a **read-only, governance-heavy task** (GAP-1 + GAP-3), which is *exactly* the class ADR-87 says needs the architect to supply intent + governance-pointers, because CC will not self-load them. So the prompt's heavy front-matter (thesis, evidence base, ADRs 82/85/87/81 + BACKLOG items, closure contract, anti-patterns, complexity gate) is the **right** shape — not over-scaffolding.

**What should move OUT** (CC self-loads it): the methodology-discipline reminders ("verify against live," "don't assert from memory," the four-tag stance) — these are CC's standing job, not per-prompt cargo. The skeleton. The generic gotchas line.

**What is RIGHT to keep IN** (and was): the thesis to test, the **evidence base** (this session's failures — off-repo, only the architect holds them), the **closure contract** (the findings doc end-state — which *is* an acceptance contract, A2 in action), and the **governance pointers** (the ADRs/BACKLOG to read — GAP-3, which CC cannot self-infer).

**The sharp, actionable lesson.** The architect's *unique* contribution is off-repo inputs + governance pointers — and **that is exactly where this prompt's two errors landed**: the mis-cited ADR-60 (§0 Correction 1) and the "three briefs attached" that were not (§0 provenance). CC could self-verify neither — they are the off-repo half of the equilibrium contract. So the prompt-shape rule sharpens to: **the thinner the prompt leans on CC self-load, the higher the fidelity bar on the architect's irreducible half** (pointers + off-repo inputs), because nothing downstream can catch an error there. A frozen acceptance contract (A2) is partial insurance — it makes the *deliverable* checkable even when the *inputs* have a gap (as here: the audit still produces a decidable agenda despite the missing briefs).

---

## 9. The rework agenda (decidable — what a fresh architect does next)

Ordered by leverage; each names its route. **No item is implemented here.**

1. **Correct the two stale-text instances (C5)** — spec §11 + `audit.py:608` say `verify_handoff_probes` is deferred; it gates `/ship`. *Mechanical spec+comment edit.* (Lowest cost, highest honesty.)
2. **Make the Architect Operating Contract resident (A1)** — relocate the role loop + add the role-stability self-check into `HANDOFF_BOOT.md`. *Architect/spec edit.*
3. **Promote the merge-serialization gate (A1/#200)** — design a mechanism that refuses a second concurrent merge-to-`main`. *AI Council candidate (#200).*
4. **Reorder the opening move to backlog-first + demote orientation-grep (A3/C3)** — *architect ruling + §13 reorder.*
5. **Generalize test-first acceptance contracts, scoped to builds (A2)** — fold into #144 + a `DEFINITION_OF_DONE.md` clause. *ADR-81 amendment.*
6. **Scope the stable teeth probe-core + consolidate the probe set (C2/#161)** — collapse the 6 validator-recoverable probes into one `ship-gate` read-back; keep orientation + volatile + anti-bluff. *Architect scoping (#161).*
7. **Remove the dead v4 corpus + decide the 40 KB-paste tradeoff (C1/C4/C6)** — gated to the v5 generator. *#164 (respect the ADR-83 corp-monorepo-live constraint).*
8. **Empirically close the contract (#184)** — the first real build that exercises A1 + A2 is the proof, per ADR-87's own closure rule (codification ≠ demonstration).

---

## 10. What this audit deliberately did NOT do

- **Did not implement** — no spec edit, no ADR, no version bump, no probe written. Analysis + proposal only.
- **Did not accept the briefs uncritically** — demoted D1 (wrong actor), partially refuted T4's weaker-model framing and Brief B's patch claim, corrected the ADR-60 citation, flagged the missing-briefs provenance gap.
- **Did not over-narrow** — graded the whole surface before any single probe; the first move was the headline grade.
- **Did not add ritual** — every ADD cleared the complexity gate and routes to existing items; the net complexity of the rework is down.
- **Did not assert state from memory** — every claim is `file:line` / SHA / probe-id / `#id` verified against live files.

> **Closure:** these findings stand as a decidable rework agenda — what the handoff does well (KEEP 12), what to stop doing (CUT 6, each with proof of redundancy or non-reproduction), and the three things to make resident/exercised (ADD 3, each with a hard metric and a route). Not "the audit ran" — a rework an architect can act on without re-deriving it.
