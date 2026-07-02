# Comprehensive System Audit — `.dev-knowledge`
## For external architectural review

<!-- scope: meta -->

> **Type:** point-in-time audit output (ADR-60 `docs/audits/` zone). Immutable once landed — supersede with a new file, do not edit in place.
> **Date:** 2026-07-02 · **Audited HEAD:** `b986711` (main; `#226`/`#230` closed, `feat/226` merged) · **Auditor:** Claude Code (Opus 4.8), read-only synthesis.
> **Grounding:** every claim below is grounded in a live read of the repo at this HEAD; load-bearing sources are cited as `file` / `file:line` / `ADR-NN`. Where a doc's own claim is stale, that is flagged (§4, §7), not repeated.

---

## Preamble — how to read this, and what we want from you (the reviewer)

**What `.dev-knowledge` is, in one sentence.** It is a self-governing *methodology system*: a Layer-2 governance authority that authors the universal LLM-development method for a fleet of repos, enforces that method against itself and its children with read-only validators and deterministic gates, and disseminates it outward as versioned, hash-guarded artifacts. It writes almost no product code; its "product" is the method and the machinery that keeps the method honest.

**Why we are asking for a review.** The system has reached a maturity inflection. Its two internal "lifelines" (delivery + coherence) are stable and heavily instrumented; its *outward* arm — deploying the method into other repos — just crossed from designed to proven-on-one-consumer (ai-council, n=1) and is about to fan out to the fleet. That is exactly the moment where architectural forks harden into path-dependence. We want an external architect (a fresh model, the AI Council, or any reviewer) to **propose decisions** on the open forks — not to rubber-stamp what exists.

**How this document is organized.**
- **§1** — what the system is and why (Vision + the three-layer model).
- **§2** — the two tracks (dwutorowość), represented faithfully and *not* collapsed. This is the central ask; read it before §7.
- **§3** — the universalization/dissemination arm (deploy subsystem, the configured→armed→proven progression, the ai-council n=1 case study).
- **§4** — a per-doc audit of the canonical corpus, honest about where docs lag reality.
- **§5** — the enforcement machinery (gates, organs, the 26-check registry, the coherence spine).
- **§6** — next steps, tied to concrete backlog IDs and the dependency graph.
- **§7 — the highest-value section: open architectural tensions.** The reviewer cannot propose decisions without knowing where the forks are. §7 states each fork, the evidence on both sides, and what a ruling would settle.

**One meta-point the reviewer should hold throughout.** This repo's *named* failure class is **resident-copy drift** — one document restating another, then silently diverging (`ARCHITECTURE.md:14`). The whole system is, in a sense, an immune response to that one disease. Several of the open tensions in §7 are places where the cure is incomplete or where the immune system has a blind spot. Judge the architecture against its own stated standard.

---

## §1 — System overview / Vision

### 1.1 The function-goal

`.dev-knowledge` describes itself as *"a universal LLM-driven development guide and methodology framework … the ecosystem's knowledge guardian and methodology author: it absorbs lessons from individual projects, universalizes them into patterns, and disseminates those patterns back as enforceable conventions. It also functions as auditor"* (`VISION.md:13-19`). Its self-image is *"the LLM-development Scrum Master for the ecosystem: it doesn't write code, it ensures the framework is applied consistently and evolves with experience"* (`VISION.md:21-23`).

Four named roles recur across VISION and BACKLOG: **Knowledge Guardian · Methodology Author · Auditor · Disseminator** (`BACKLOG.md:5`).

The operating posture is not steady-state maintenance but continuous evolution: *"Continuous improvement is the baseline operating posture, not an option. Sessions advance the framework; static maintenance is exception requiring explicit justification"* (`VISION.md:25-33`). The methodology now **self-enforces** — it applies its own conventions to its own process (the Tier-1 lifecycle, ADR-70) *"to the same enforced-not-remembered bar it imposes on the artifacts it governs"* (`VISION.md:29-33`).

### 1.2 The three-layer model (ADR-28) — where the repo sits

`.dev-knowledge` is **Layer 2** of a three-actor closed loop (`ARCHITECTURE.md:48-58`, Ch1):

| Ecosystem layer | Role |
|---|---|
| Layer 1 — browser chat (**architect**) | external — analysis & design; produces prompts/handoffs; no filesystem access |
| **Layer 2 — `.dev-knowledge`** | **this repo** — passive storage, governance, prescription; *nothing here executes orchestration* |
| Layer 3 — projects (**executor**) | external — corp-monorepo, ai-council, corp-ops, corp-sca-time-automation; Claude Code does the work |

The loop: architect proposes → **operator is the consent gate** (pasting a prompt into Claude Code *is* the act of consent) → executor acts only inside ratified scope → executor commits the handoff back to Layer 2 → Layer 2 is read as context by Layer 3 → reflection returns to a new browser chat (`ARCHITECTURE.md:92-128`). ADR-28 is **descriptive** — it documents existing practice, not a new constraint (ADR-28, Accepted; load-bearing sentence: *"`.dev-knowledge` contains no executable orchestration — scripts do not reside here"* `ADR-28:15`).

*"**Ratification bandwidth is the scarce resource** the whole system economizes — every protocol that compresses context (handoff bundles, the methodology floor, valves) exists to spend less of it"* (`ARCHITECTURE.md:126-128`). This is the economic engine behind almost every design decision downstream.

### 1.3 The five binding Layer-2 invariants (`ARCHITECTURE.md:130-141`)

1. **Layer 2 never executes** — no script here orchestrates or drives state changes in another repo.
2. **Validators are read-only on siblings** — `scripts/` only reads/checks/reports; cross-repo `audit.py run` reads each sibling read-only and writes **only** into `.dev-knowledge`.
3. **Prescriptive authority** — PLAYBOOK + ADRs bind child repos; children may not locally override (ADR-31, authority model 1B, *prescriptive with conformance audit*).
4. **Append-only files are never edited** — `LESSONS.md`, `logs/TOKEN-LOG.md` accept only appends.
5. **Dated artifacts are immutable** — ADRs, transcripts, handoffs, audits are superseded by a new file, never edited in place.

These five are the constitutional floor. Note (§7) that invariant #1 is under quiet, principled pressure: the deploy subsystem writes into consumers — resolved by the *"write-yes, commit-no, autonomy-no"* boundary (ADR-92), but it is the closest the system comes to the edge of its own constitution.

---

## §2 — The two tracks (dwutorowość)

> This is the central ask. The system genuinely runs on two tracks, but **the canonical framing and the framing in this review's brief do not name them the same way** — a real and reviewable subtlety, surfaced honestly here and again in §7.7.

### 2.0 Two vocabularies for "the two things" — reconciled

The methodology's **own** canonical frame is **"The two lifelines"** (`PLAYBOOK.md:229-264`), which opens: *"The methodology maintains exactly two things; every chapter below serves one of them. Naming them is the frame"* (`PLAYBOOK.md:232`). The two lifelines are:

- **Lifeline 1 — Workflow** — the architect↔CC delegation loop (`PLAYBOOK.md:234`).
- **Lifeline 2 — Coherence** — the corpus stays internally consistent across dependency edge-types (`PLAYBOOK.md:249`).

The review brief frames the two tracks differently: **Track 1 = methodology authoring / self-maintenance**, **Track 2 = delivery / deployment loop**. These do **not** map 1:1 onto the lifelines. The cleanest reconciliation:

| Brief's track | Maps mostly to | But note the leak |
|---|---|---|
| **Track 2** — delivery loop | **Lifeline 1 (Workflow)** — near-exact match | clean |
| **Track 1** — methodology authoring / self-maintenance | **Lifeline 2 (Coherence)** + parts of Lifeline 1 | ADR lifecycle, handoff process, Council are mapped to **Lifeline 1** in PLAYBOOK's own chapter map (`PLAYBOOK.md:262`), *not* to Coherence — even though the brief calls them Track-1 authoring |

So the two tracks are real and load-bearing, but **"authoring vs delivery" and "coherence vs workflow" are two different cuts through the same corpus.** The rest of §2 presents both tracks as the brief asks, while flagging where PLAYBOOK's own lifeline assignment diverges. §7.7 treats "is the dwutorowość clean?" as an open tension.

### 2.1 Track 1 — Methodology authoring / self-maintenance

*How the method is created and kept coherent.*

**The methodology engine (the loop that authors the method).** ARCHITECTURE Ch6 states it as a closed feedback engine: `Lessons (LESSONS.md)` → `Decision/ADR (docs/decisions/ + Council)` → `Conventions (PLAYBOOK / ESSENTIALS / CLAUDE.md)` → `Enforcement (audit.py + hooks)` → `Dissemination (conformance audit to child repos)` → *(run in live sessions → new friction)* → back to `Lessons` (`ARCHITECTURE.md:529-536`). *"The two frontier stages — Enforcement and Dissemination — are where active work concentrates."*

**ADR lifecycle.** Decisions that bind future sessions live in `docs/decisions/ADR-NN-*.md` (Michael Nygard format). Two authorship paths (`PLAYBOOK.md:2528`): chat-drafted (browser architect → CC creates the ADR in-repo) and Council-convened (debate → post-debate distillation). The **amend-vs-reopen** protocol (`PLAYBOOK.md:2538-2574`): amend in place if tooling diverged but original intent holds; reopen (new ADR / Council) if the intent itself was wrong. Amendments append a dated `## Amendment YYYY-MM-DD` block and **never rewrite the original decision text** — the immutability invariant. (This produces one live wrinkle: ADR-88/89 headers still read *Proposed* while a 2026-06-21 in-place amendment marks them *Accepted* — §4.5.)

**The decision flow (how a contested need becomes doctrine).** `Council brief (ephemeral)` → `ai-council debate (5-provider, blind vote — ai-council ADR-03)` → `routed transcript (target/docs/decisions/transcripts/ — ADR-43)` → `operator distils an ADR` → `BACKLOG item + convention edit` → `enforcement organ` (`ARCHITECTURE.md:567-574`). The complexity router: 1-file mechanical → conversational; 3+ files / 2+ packages → formal CC prompt; architecture/contested → Council.

**The handoff process (v5.3, stable; ADR-82).** v5 inverts the old v4 model: instead of a browser-delivered 8-file bundle, **CC owns the handoff** — it emits a lean *residual* (un-committed reasoning + pointers + drift-flags) + a *probe manifest* under `docs/handoffs/<slug>/`, and a fresh browser chat boots from the thin `protocols/HANDOFF_BOOT.md` (`CONTRIBUTING.md:188`). The probes have **teeth**: they force CC to re-derive every load-bearing fact from live primary source at check-time, mechanized by the `handoff_probes` audit check (FAIL-class — a toothless probe blocks `/ship`). Two payload *modes* — architect (big-picture + vision) vs execution (lean task-state) — one process (LESSONS 2026-06-11; BACKLOG #150/#159/#162).

**Skills, plugins, workflows (Claude Code internals — PLAYBOOK Ch14).** Skills auto-load from `~/.claude/skills/` (user-level, e.g. `gotchas`) and `<repo>/.claude/skills/` (repo-level, e.g. `verify`, `check-against-spec`). The `tier1-lifecycle` plugin (enabled) drives the closure loop and ships `/ship` + `/review-closures`. Dynamic Workflows are the **heavy-execution** organ (JS harness driven by a runtime), explicitly bounded: *"the AI Council remains the heavy-decision organ … the workflow is the heavy-execution organ — workflows do not creep into Council's role"* (`PLAYBOOK.md:2155`).

**The dependency-coherence spine (Lifeline 2 — the reverse-dependency legibility thesis).** The corpus stays consistent across **four dependency edge-types**, each with a *discovery/compute* half and a *gate/enforce* half (`PLAYBOOK.md:249-257`):

| Edge | Mechanism | State (per PLAYBOOK) |
|---|---|---|
| **code↔code** | reverse-dependency oracle computes referrers before a module is removed | oracle built; consuming safe-removal gate partial (#195 M1 only; M2/M3 = #218) |
| **code↔doc** | rule-ID `<domain>-<slug>`: doc `<!-- rule: -->` ↔ code `# rule:`, resolved by `doc_code_edge` | gated for the curated rule set (12 rules); completeness via ADR-90 resolver-allows-N |
| **doc↔doc** | `reconciled_with: <spec>@<version>`: gate checks the version stamp | declared-half **gated (FAIL)**; undeclared-discovery advisory-only |
| **undeclared** | `scan_undeclared_edges` surfaces prose refs lacking a declared edge | surfaces; **does not gate** |

The organizing doctrine is **ADR-88** (*"repo files — markdown documents first — as the unit of dependency … coherence across declared edges is held by machinery, not by memory"* `ADR-88:33-35`) and its computed-edge sibling **ADR-89** (*"declare what you cannot compute; compute what you can"* — doc→doc declared, code→code computed via a Pyright reverse-dependency oracle, `ADR-89:46-47`). This is the reverse-dependency-legibility thesis: rather than a human remembering what depends on what, the graph is *in the repo* (declared) or *computable from source* (Pyright), and machinery holds coherence. §7.5 asks whether the thesis is sound and fully applied.

### 2.2 Track 2 — Delivery / deployment loop (= Lifeline 1, Workflow)

*How the system delivers work.*

**The delegation loop, stated canonically** (`PLAYBOOK.md:234`): *"**decide → plan → delegate → verify → archive → educate.** Judgment-phases (plan / verify / archive / educate) are the architect's and are never delegated; build-phases (implement / test / deploy) are delegated to CC but *owned* by the architect — 'merged' ≠ 'done', and the architect declares closure on the hard end-state, not on 'tests pass.'"* The transition gates that keep the loop honest: `HANDOFF_BOOT` (orientation), the ship-gate, the Stop-gate, `block_immutable_edits`, `block_ff_push`.

**The plan-review contract (ADR-87 equilibrium).** The architect↔CC division is canonical in the "two lifelines" table (`PLAYBOOK.md:238-247`):

| Resident in the browser (architect) | Outsourced to CC |
|---|---|
| decompose, prioritize | pick the model |
| choose MODE (plan vs auto) | fill the prompt skeleton |
| decide parallel / worktree | load code-impact context |
| review + verify CC's output | load generic gotchas |
| declare closure (hard metric) | execute + commit |
| off-repo inputs + governance-pointer | self-load the rest |

The architect emits **intent + closure + anti-patterns + MODE + a thin governance-pointer**; CC self-loads the rest. **Model is CC's pick** (default Opus 4.8, the floor); the architect sets Mode + Effort, never the model (`PLAYBOOK.md:247`; `ESSENTIALS.md:273`). Crucially, **intent-only is conditional** (ADR-87): reliable for code-impact tasks, but a read-only/governance/gotcha-sensitive task **requires** the thin governance-pointer or it regresses GAP-3 (*"omitting it regresses the gap CC cannot close from inside the repo"* `ADR-87:52-53`). Mode encodes the judgment/build boundary: `plan` (architect reviews each step) / `plan-then-auto` (judgment at UNDERSTAND+PLAN, then build) / `auto-accept` (approach pre-approved).

**Judgment-phases vs build-phases** is the load-bearing distinction: judgment is never delegated; build is delegated but *owned*. "Merged ≠ done."

**Test strategy — deterministic vs LLM-judge split (Ch10 two-tier automation doctrine).** Two orthogonal axes (`ARCHITECTURE.md:392-402`): Axis 1 (LLM judgment — does the organ run a model?) and Axis 2 (friction cadence — Tier 1 always-on / Tier 2 scheduled / Tier 3 episodic).

- **Deterministic (no model)** — pre-commit + commit-msg hooks, `audit.py` self-conformance, the scheduled `fleet_health.py` cross-repo baseline. Posture: **fail-closed** on executing paths, **fail-soft** on awareness paths (`PLAYBOOK.md:1444`).
- **LLM-judgment (runs a model)** — *"always read-only + adversarial-skeptic-filtered + operator-ratified — it proposes, a skeptic kills false positives, and a human funnel ratifies before anything binds"* (`PLAYBOOK.md:1446`). E.g. the nightly cloud conformance Routine.

Per-step discipline: `pytest -x --tb=short && ruff check && git status` **after each step, not at the end** (`PLAYBOOK.md:2259`; core-invariants #2).

**The delivery lifecycle — Definition of shipped (the acceptance-contract, ADR-81).** Three distinct "done" scopes are kept separate (this separation is itself doctrine — MEMORY `dod-three-scopes-distinct-homes`):

1. **Organ-done (ADR-81)** — an organ is not DONE until it has (a) a methodology home in PLAYBOOK sufficient for a fresh session to act, (b) a deployment path, (c) a maintenance/refresh cadence with staleness detection, (d) actual deployment OR an explicit named deferral. *"Stopping at build+test is the half-feature rot trap: build-and-test ≠ done"* (`ADR-81:26`).
2. **Arc-shipped (PLAYBOOK Ch12.1 "Definition of shipped")** — a feature/arc is shipped only when ALL SIX hold: git clean+merged; version surfaces coherent; an **E2E/user-flow test** passes; **checked against the original expectation in a back-and-forth** (not a one-shot self-grade); records updated; the verification organs **RUN green** (`PLAYBOOK.md:1566-1575`). Plus an **ex-ante** property for deterministic build tasks (ADR-81 amendment 2026-06-24): the executable pass/fail criterion is **authored by the architect before the build and frozen** — immutable to the executor (CC may strengthen, never weaken); closure declared on that contract, not on "tests pass." Proven exemplar: #194 Phase-A xfail-strict coverage test whose failing output *is* the rollout inventory (`PLAYBOOK.md:1577`).
3. **Session-close (`DEFINITION_OF_DONE.md`, ADR-85)** — the narrower per-session record obligation (§5.3).

### 2.3 How the two tracks connect — one skeleton, two views

PLAYBOOK does not use "one skeleton, two views" verbatim, but the connective tissue is explicit and threefold:

1. **The chapter map assigns every chapter to one lifeline or "cross-cutting"** (`PLAYBOOK.md:260-264`). Lifeline 1: Ch2, Ch4+§2, Ch5, Ch7+§6+§16+§17, Ch8, Ch9, Ch12, Ch14, §1/§4/§5/§7/§8. Lifeline 2: Ch3, Ch6, Ch11, §10, §14, §19. Cross-cutting (where they touch): Ch1, Ch10, Ch13, §3/§9/§11/§12/§13/§15, Appendices A–C. *(Gap surfaced: §20 — the deploy runbook — is unmapped to any lifeline; see §7.7.)*
2. **The sealing test applies to both** (`PLAYBOOK.md:258`): *"does this mechanism have its consumer / gate?"* — and its refinement, *"is there real signal for a consumer to act on?"* *Built-without-consumer* is the recurring failure class both 2026-06-25 audits found; this test is the standing guard. It is deliberately allowed to answer **no** (the import-cycle gate was the right shape but guarded nothing, so it was declined).
3. **The governance-pointer injects Lifeline-2 state into every Lifeline-1 delivery act** (`PLAYBOOK.md:2209`): each governance-touching prompt carries `[A] → Governance pointer: the ADR / LESSONS / sibling-spec this task touches`, so corpus-coherence state is brought into scope at execution time. And the shipped-gate (arc-shipped point 5 "records updated" = Lifeline 2; point 6 "organs run green" = deterministic gate) requires both lifelines satisfied before shipping.

---

## §3 — Universalization / dissemination

*How the methodology deploys into new repos, and how it is managed over time.* This is the "Dissemination" frontier stage of the methodology engine (§2.1) and the arm that just crossed from designed to proven.

### 3.1 The distribution model — five carriers, different scopes and freshness models

The methodology is authored in the hub and **carried** to where it is consumed (`ARCHITECTURE.md:452-464`, Ch4):

| Carrier | Scope | What it carries | Ref |
|---|---|---|---|
| user-layer `~/.claude` | fleet-wide (L0) | `block-onedrive`, gotchas, ROUTING, Codex config, `surface-closures`, the `--no-ff` rule | global; ADR-54 |
| `tier1-lifecycle` plugin | repo-class | `/ship`, `/review-closures`, `propose_closures`, `validate_backlog` | ADR-70/73 |
| pre-commit source repo | consumer-pull | codemap×2 + toc×2 freshness hooks (children consume via `repo:/rev:`) | ADR-71 |
| child floor `.claude/CLAUDE-FLOOR.md` | per child repo | ≤1,500-tok generated floor + `.sha256`; operator-invoked generator | ADR-78 |
| browser bundle | browser sessions | consolidated `BUNDLE.md`; Projects deferred | ADR-79 |

Two doctrines bound this: **children consume, never author** (agents/orchestration are versioned in the hub); and **cloud is hub-independent** (a cloud Routine clones only its own repo and consults no hub reference on the executing path — ADR-72; the private hub permanently closes ADR-71's "URL-swappable later" hatch for cloud). The canonical gap map is the 12-row × 7-context transfer matrix (`docs/audits/2026-06-07-methodology-transfer-audit.md`); headline: friction concentrates in **one cell** — child-repo CC sessions, where the floor is a *pointer the agent must choose to follow*, not resident text.

### 3.2 The deploy subsystem (ADR-91/92/93) — the versioned, verification-gated push

Built 2026-06-29→07-01. Three ADRs stack:

- **ADR-91 (corpus versioning)** — semver + a git-tag release marker for the corpus (`protocols/` + accepted ADRs + `templates/` + the `audit.py` engine + carrier contracts); *"No changelog or version file is introduced"* (`ADR-91:25`) — git-is-changelog. Baseline `v1.0.0`. The durable record lives in a purpose-built committed `ecosystem/deployed-versions.yaml` — **not** the derived `index.yaml` (which `audit.py regenerate_index` clobbers wholesale) and **not** the gitignored `state.yaml`. The record-home decision was itself a caught bug (LESSONS 2026-06-27: a live read of `index.yaml`'s generator showed it would clobber any field written there).
- **ADR-92 (deploy-runbook doctrine)** — a **deterministic, versioned, verification-gated deploy tool** (not a slash command — verification must run in a deterministic runtime; Claude Code is shelled out to *only* for the plugin carrier, result verified deterministically). Operator-run in two phases with a three-edge Layer-2 boundary: **write-yes, commit-no, autonomy-no** (`ADR-92`, Decision 3). Core principle: *"per-carrier verification gates the version-record write. The registry reflects **verified reality, not intent**"* (`ADR-92:46`).
- **ADR-93 (floor provisioning model A)** — commit + hash-guard the floor (§3.4).

**The orchestrator (`deploy/tool.py`).** Two phases in one module:
- **ASSESS (read-only)** — `preflight()` hard-aborts on tag-resolve / consumer-registered / clean-consumer-tree (`tool.py:225-277`); `assess()` calls only `carrier.detect(target)` in manifest order, capturing a raising detect as an `error` row so it stays usable against a degraded fleet (`tool.py:434-494`); `render_plan()` prints the per-carrier plan and *"No record will be written in assess mode."*
- **EXECUTE (`tool.py:761-856`)** — per carrier: apply-if-needed (or `--force`) then verify; **fail-fast** on the first carrier whose apply/verify raises or whose `verify.ok` is False. The two writes happen **only on full success** (Decision 9): (a) `stage_consumer()` — `git add` in the consumer, *write-yes/commit-no*; (b) `write_record_to_branch()` — commits the version record on a **new hub branch** `deploy/record-<repo>-<ver>` via pure git plumbing (`hash-object`/`commit-tree`/throwaway index), never touching HEAD/worktree/index and **never auto-merged**. *(Note: `tool.py`'s module docstring calls execute "scaffolded … never implemented" — this is stale; execute is fully built. §4.6.)*

**The four carriers** (each `detect/apply/verify` against the tiny `Carrier` ABC in `contract.py`; the D9 invariant: verify is independent of detect so a detect bug cannot make verify pass):

| Carrier | Order | Deploys | How |
|---|---|---|---|
| **globalconfig** | 1 | hub `codex/AGENTS.md` → user `~/.codex/AGENTS.md` | byte copy; user-machine scoped; 3 states (no version) |
| **plugin** | 2 | `tier1-lifecycle` plugin at project scope | only carrier via external CLI (`claude plugin …`); judges from resulting state, never stdout/exit |
| **precommit** | 3 | pinned hooks into consumer `.pre-commit-config.yaml` | pure-file reconcile; **single writer** of that file; owns the `floor-hash-verify` local hook |
| **floor** | 4 | the per-repo floor **+ arms it** | see §3.4 |

The git transport is binary + explicit UTF-8 + LF at every subprocess site — a deliberate, tested invariant to avoid the Windows cp1252/CRLF corruption class that cost three iterations on run #1 (`tool.py:92-137`; LESSONS 2026-07-01, §3.5).

### 3.3 The configured → armed → proven progression

The three-stage framing is doctrine (ADR-93), not a code constant, and it is the **conceptual spine of the whole dissemination arm**:

- **configured** = the files are present (what a naive presence-check sees).
- **armed** = the consumer is *self-verifying* — `carrier_floor.apply` writes all six arming artifacts, and detect/verify demand every one (`ApplyResult.detail = "floor armed at corpus state"`).
- **proven** = the `#230` conformance suite functionally exercises the armed loop end-to-end (not "files exist" — "the guard actually fires").

The pivotal risk the progression exists to kill is the **"configured-not-armed facade"**: ADR-93 rejects Model B (a gitignored floor) precisely because *"a gitignored floor → absent on clone → broken `@`-include"* is *"exactly what creates the configured-not-armed facade"* (`ADR-93:17`). This term came from the outgoing architect's SUPPLEMENT (JOURNAL 2026-07-01 `f18b0a9`: *"configured-not-armed = facade"*), and it drove the resolved priority chain `#226→#230→#222/223→#225→#221`.

### 3.4 Model A floor + the two-leg hash-guard (ADR-93)

The methodology floor (`.claude/CLAUDE-FLOOR.md` + `.sha256`) is **committed and tracked** in the consumer (not gitignored), behind a **two-leg hash-guard** running one canonical `.claude/check_floor_hash.py`:

- **Session-start VERIFY leg** — a `SessionStart` hook in the committed `settings.json` runs `check_floor_hash.py --require-present`. It **travels with the clone**, is un-suppressible by `--no-verify`, and `--require-present` catches drift **and** a deleted-but-tracked floor (the case the commit-time leg can't catch — this delete-hole was found and closed 2026-07-01 `67a7975`).
- **Commit-time leg** — the `floor-hash-verify` pre-commit hook, **owned by the precommit carrier** (single-writer-per-file). Because git hooks never travel with a clone, the SessionStart leg idempotently `pre-commit install`s this leg — **warn-loud-not-fail** if pre-commit is absent.

The hub template stays the **single authoritative source**; the committed consumer floor is a hash-guarded **replica** — so the #95 copy-drift invariant is preserved: *"drift is caught by the guard, not avoided by non-tracking"* (`PLAYBOOK.md:3252`; ADR-93). The tracking is enabled by rewriting a bare `.claude/` gitignore to `.claude/*` + `!`-negations (a bare dir exclusion defeats negations, #138), so the floor stages with a plain `git add` — no `-f`.

The reservation is stated in ADR-93 itself and is **load-bearing**: *"The hash-guard is load-bearing: if it were weak — commit-only, silent, or trivially bypassed — model A would degrade into exactly the committed-copy-that-silently-drifts #95 fears … If the guard ever proves unbuildable or is materially weakened, reopen model B"* (`ADR-93:40-42`). Two known limits are surfaced, not hidden: **greenfield `settings.json` tracking** (a fully greenfield consumer that gitignores `.claude/` with no pre-tracked settings.json would not carry the SessionStart hook on fresh clone — now a *tested* property via `#230`'s `assert_sessionstart_wired`; #221 must generalize); and `--no-verify`/out-of-CC commits bypass the commit-time leg (session-start leg is the backstop; accepted per the accidental-drift threat model).

### 3.5 The #230 conformance harness (`deploy/floor_conformance.py`)

Proves the armed loop **functions**, not just that files exist. An ordered 8-property suite (each raising a named `ConformanceError`): `@`-include present + floor hashes to sidecar; SessionStart wired (path-agnostic — a consumer whose settings.json didn't travel **fails here**, no false green on self-arm); clean floor passes; poisoned floor fails loud with the `"floor hash drift"` marker; deleted floor fails via `--require-present`; `pre-commit install` auto-arms `.git/hooks/pre-commit`; the commit-time hook blocks a poisoned-floor commit with HEAD unmoved; a real task flows branch → commit → `--no-ff` merge onto the first-parent spine.

Two layers: **Layer 1** = hermetic hub CI (synthetic consumer, real carriers arm it — synthetic GREEN). **Layer 2** = the operator CLI against the **real** cloned consumer — this is the **#226 hard-metric**. Layer 2 surfaced two real harness bugs on run against ai-council (JOURNAL 2026-07-02 `8517c91`): (A) clone set `autocrlf=false` *after* checkout so every LF file read as unstaged; (B) ai-council's config carries a relative-path hub-hooks repo + a remote ruff repo, and pre-commit inits every repo before running any hook. Both fixed; re-ran → **9/9 GREEN** against real ai-council, all four legs (clean-pass, tamper both legs, delete-backstop, assert_sessionstart_wired), from the committed harness. This retired the settings.json known-limit **for ai-council by test**.

### 3.6 The ai-council arc — the worked n=1 case study

ai-council is the first real consumer and the deliberate **generalization probe** (BACKLOG #215: *"the first onboarding pilot doubles as the first real test of whether the two lifelines transfer to a structurally-different repo-shape (CLI / provider-heavy / fewer governance-docs)"*).

**What "configured, not armed" meant here, and how it was retired.** A prior plugin deploy to ai-council had left the Tier-1 ruff lint gate **unapplied** — *"a silent partial deployment … a verification gap, not a process-form gap"* (`ADR-92:8,17`; `carrier_precommit.py:3-5`). The `PRESENT_DRIFTED` carrier state is documented as *"the observed ai-council failure shape"* (`contract.py:50`). The fix arc: arm the floor carrier (#226b), build the #230 harness, then run Layer-2 against the *real* armed ai-council. Closed 2026-07-02 (`b986711`): **#226 + #230 closed**, `feat/226` merged, the #226 hard-metric met (Layer-2 9/9 GREEN vs the real armed ai-council incl. tamper, not synthetic).

**What transferred vs what didn't (the probe's whole value)** — LESSONS 2026-07-01: the *core* transferred end-to-end (assess→execute→ratify; the per-carrier verify-gate; the detect/apply/verify contract; the record-on-a-hub-branch). Three things did **not** transfer cleanly: (i) **consumer `.gitignore` shape** — ai-council gitignores `.claude/`, so the floor reconciles on-disk-but-*unstaged* (correct per #95, but a per-consumer divergence); (ii) the **Windows-text-mode-git-I/O class** — CRLF+cp1252 corruption on two axes × two sides, three iterations to fully close; (iii) the **precommit YAML comment-strip** (cosmetic, deferred as #225). Forward rule for runs #2–4: *"treat each consumer's `.gitignore` + config shape as an UNKNOWN to probe, not a copy of the hub."* Three meta-lessons landed (LESSONS 2026-07-01): Windows I/O as a from-the-start tested invariant; **verify the bytes before merge** (the record was blocked twice at the merge boundary — CRLF then em-dash mojibake — both looked "fine" to a values-only check, caught only by a byte-level check); and **review discipline is the load-bearing safety net** (*"a prompt is a HYPOTHESIS; do not let 'the prompt said merge' override 'the bytes aren't clean'"*).

### 3.7 Managing over time — versioning, drift-catch, feedback, and the deferred active-push decision

**Versioning.** `ecosystem/deployed-versions.yaml` records per-repo `deployed_methodology_version` / `deployed_date` / `source_tag`, written by `deploy/tool.py --execute`, read by `audit.py::check_deployed_methodology_version` (n/a while null, pass once set), surfaced via `fleet_health.py`. **Current fleet state (n=1):** only `ai-council` is populated (`1.0.0` / `2026-07-01` / `v1.0.0`); the hub and the other three consumers are `null` (pre-deploy) (`deployed-versions.yaml:24-45`).

**Drift-catch, both legs.** The two-leg hash-guard catches floor drift in the consumer (session-start + commit-time). Template↔copy drift *between rollouts* for the per-repo orchestration copies is the acknowledged, still-open gap — **BACKLOG #95** (*"no organ detects a copy diverging from the hub canonical template between rollouts"*), flagged in ADR-73's own cost note.

**The consumer→hub feedback loop.** There is **no** consumer→hub feedback loop in the subsystem today — the model is deliberately **one-way, hub→consumer push, with local drift-catch**. The intended feedback loop is **filed but not built: BACKLOG #231** (*"when a consumer session detects a methodology gap, ambiguity, or broken piece — including a failing #230 self-test — it emits a STRUCTURED report destined for the hub … instead of guessing"*). The only hub-ward write in the whole flow is the version record, and even that lands on an operator-merged branch, never auto-merged.

**Active-push vs drift-catch-on-re-run — the deferred decision.** ADR-93's Model A endorses *"the hub pushes the canonical floor **once**; a fresh clone is armed at once; and the copy-drift #95 fears is **caught** by the guard rather than **avoided** by non-tracking"* (`ADR-93:18`). The alternative — re-running the deploy on every consumer to stay current (active push) — is not the chosen model, but the general question ("which model for managing currency over time, and when?") is not settled beyond the floor. This is §7.6.

### 3.8 Fleet rollout — the n≥2 generalization gate

**BACKLOG #221** is the rollout item: run the tool on the other consumers (corp-monorepo, corp-ops, corp-sca-time-automation) to reach the **n=2+ generalization gate** and populate the registry fleet-wide. Sequencing is explicit: *"#221 MUST follow #226 (the arming carrier fix) so fleet repos don't replicate ai-council's configured-not-armed gap; each repo's deploy uses the #230 conformance self-test as its acceptance gate"* (BACKLOG #221; the `depends-on: #226` was dropped 2026-07-02 now that arming landed). The cross-repo floor-generation doctrine is **ADR-73** (per-repo orchestration copies, hub-canonical template, propagation at rollout moments, bidirectional back-port) and **ADR-78** (the child floor itself, operator-invoked generator, strict no-autonomous-cross-repo-writes Layer-2 invariant, the `methodology_surface` whitelist/F5-blacklist zone).

---

## §4 — Canonical docs audit

*Per-doc: purpose, current state, faithfulness, gaps.* The corpus is unusually self-aware about its own drift; the honest headline is that **the outward-facing arm (deploy) outran the map (ARCHITECTURE) and the freshness signal is presently corrupted for one file.**

### 4.1 `VISION.md` (last_reviewed 2026-06-19)
**Purpose:** the universal brain — vision, scope, values, relationships, lifecycle. **State:** faithful and stable; the four roles and the continuous-improvement posture are current. **Gap:** minor — the self-owned cleanup #35 (adoption-signal + a formerly-stale stamp) is the only open low-severity item; scope language predates the deploy arm but is broad enough to contain it (dissemination is named in-scope). No material drift.

### 4.2 `ARCHITECTURE.md` (last_reviewed 2026-07-01 — **forced/false stamp; the corpus's largest current doc-debt**)
**Purpose:** the navigation map — six chapters (layers · organs · automation axes · distribution · zones · verification mesh) that **point** to ADRs/protocols and never restate doctrine. **State:** excellent for what it covers; the six-chapter structure is faithful to the shipped reality through ADR-84. **Two real gaps, both filed:**
- **#223 — the deploy subsystem is invisible in ARCHITECTURE.** The only "deploy" hit is the unrelated nightly Routine. The ADR-91/92/93 `deploy/` tool + four carriers + the `deployed_methodology_version` record + the ADR-93 floor arming/conformance are **entirely absent** from Ch2 (organ map), Ch4 (distribution), Ch6 (verification mesh), and the Validators list.
- **#224 — the Governing-ADRs list stops at ADR-89** (90/91/92 are Accepted and in the index but not rotated in; CLAUDE.md §11 "last 5" has the same lag).
- **The `last_reviewed: 2026-07-01` stamp is forced/false** (JOURNAL 2026-07-01 `cadf53d`, explicitly): the last several commits were pytest-count bumps that advanced the file's commit date, so `canonical_freshness` (check #10, commit-based A2) demanded a same-day re-stamp *with no genuine re-read* — proven false because the "reviewed" file omits deploy and stops its ADR list at 89. This is the concrete instance behind the tension in §7.3, and the coupling itself is filed as **#222** (decouple the volatile count from the freshness gate).

### 4.3 `CLAUDE.md` (last_reviewed 2026-06-26)
**Purpose:** the single canonical per-repo agent contract (≤200 lines, ADR-53). **State:** faithful and dense; §9 hook roster and §7 command list are current (reconciled through the deploy arc). **Gaps:** §11 "last 5" ADRs stop at 85–89 (the deploy 90/91/92 rotation is #224); an intra-file file-lifecycle restatement (§4 bullet ↔ §5 rules #1–3 both authoritatively define the append-only/immutable disposition) is a known, filed resident-copy-drift instance (**#157**) — the repo's own named disease, inside its own contract.

### 4.4 `PLAYBOOK.md` (3456 lines; last_reviewed via reconciled_with handoff-process@5.3)
**Purpose:** the full process reference — Part I (Ch1–14 doctrine) + Part II (§1–20 workflows), organized under the "two lifelines" frame. **State:** the two-track structure is genuinely present and both tracks are substantively covered (§2). **Faithfulness caveats / gaps:**
- **No single consolidated gate-map** lives in PLAYBOOK — the gate roster's canonical home is CLAUDE.md §9; PLAYBOOK's gate doctrine is distributed across Ch10 + the sealing test. (Whether a resident gate-map *should* exist is a judgment call — a resident copy would itself risk drift.)
- **§20 (deploy runbook) is unmapped in the two-lifelines chapter map** (the map lists up to §19). The deploy arm is doctrinally homeless in the lifeline frame — §7.7.
- **Known bloat / condensation debt is filed as #213** (separate rule from rationale/history across 3456 lines) and **#214** (surface cleanup: `/changelog-review` naming collision; move the raw-worktree fallback to an appendix). These are grooming items, not accuracy defects.
- Two under-described spots (per the two-track digest): the "educate" leg (closing the delivery loop back into the corpus) is implicit via JOURNAL/LESSONS rather than a named section; and the "verify" entry-criteria are scattered across Ch10+Ch12 rather than consolidated.

### 4.5 `docs/decisions/` (66 ADR files, ADR-27→93 minus 44/45)
**Purpose:** the decision ledger + Council transcripts. **State:** the index (`README.md`) is comprehensive and the ADR↔transcript traceability table is maintained. **Gaps:**
- **#228 — numeric-order quirk:** the index lists ADR-90 physically *after* ADR-91/92 (rows for 91, then 90, then 92) — a sequencing quirk, filed.
- **ADR-88 and ADR-89 carry frozen `Proposed` headers** while a 2026-06-21 in-place amendment marks them *Accepted* (the immutability convention forbids editing the frozen header). Correct per convention, but a reader scanning headers alone would misread status — a legibility wrinkle inherent to the immutability invariant. The ADR-index status convention (MEMORY `adr-index-status-prefix-convention`) drops the `**Proposed** —` prefix on ratification; this was done for 88/89 in the index but the ADR-file headers remain frozen.
- Several load-bearing ADRs are **"doctrine only, build deferred"** (ADR-89 Track A tooling; ADR-91 → its writer became ADR-92; ADR-92 → tool/manifest/carriers). ADR-93 is the exception (authored *during* its build, recording a proven mechanism). This is a deliberate pattern (do-not-build-is-doctrine, ADR-88 Principle 5), not rot — but it means "Accepted" ≠ "built" for a nontrivial slice of the corpus, which a reviewer should hold.

### 4.6 Code docstrings vs code (a minor but real drift)
`deploy/tool.py`'s module docstring calls `execute` *"scaffolded … never implemented"* while `execute()` is fully built (`tool.py:761-856`). Harmless operationally, but it is a code-level instance of the same resident-copy-drift the whole repo fights — and it is *not* caught by any doc-code gate (the gates cover declared `<!-- rule: -->` edges, not free-prose docstrings). Worth a one-line fix and a note in §7.5 on the reach of the legibility thesis.

### 4.7 Corpus growth vectors (filed, not yet decided)
- **#212 — `docs/handoffs/**`** is the single largest growth vector: 416 immutable bundles, immutable-by-design (ADR-82) but unbounded; the one sanctioned uncontrolled-growth vector, owed a deliberate retention/rollup call.
- **#229 — `temp/`** holds ~700 MB of personal/client scratch (gitignored, not a leak, but a Three-Homes violation) — operator-gated cleanup.

---

## §5 — Enforcement mechanisms

*How the system ENFORCES, not just documents.* This is the machinery that makes "held by mechanism, not memory" real.

### 5.1 The organ map — which organ fires when (`ARCHITECTURE.md:194-218`, Ch2)

Every enforcement/awareness organ, with trigger, layer, and **failure posture** (fail-closed = blocks; propose-only = writes a proposal, never mutates; fail-soft = logs/exits 0). Layer: **L0** = global `~/.claude` (fleet-wide) · **hub** = this repo's `.claude/` · **plugin** = `tier1-lifecycle` (repo-class) · **pre-commit** = local git gate. Selected load-bearing rows:

| Organ | Trigger | Layer | Posture |
|---|---|---|---|
| `block-onedrive.ps1` (PreToolUse) | every Bash/Edit/Write | L0 | **fail-closed** (P0) |
| `block_immutable_edits.py` (PreToolUse) | Edit/Write on `transcripts/**` | hub | fail-closed in-zone |
| `propose_closures.py` (Stop) | session end | plugin · Tier-1 | **propose-only** (never mutates BACKLOG) |
| `session_end_backpressure.py` (Stop) | session end | hub | **hard-block** on JOURNAL leg; advisory on BACKLOG |
| `conformance-hub.js` (Workflow) | operator/cloud Routine | Tier-3 | read-only + skeptic + evidence-required |
| pre-commit gates (10) | local commit | pre-commit · Tier-1 | **fail-closed** |
| audit checks (`git_backlog_drift`, `doc_claims`, `no_ff_merges`, `doc_rot`, `doc_structure`, `doc_code_edge`) | `audit.py health` gate | hub | fail-soft (**WARN**, awareness) |
| `handoff_probes`, `reconciled_versions`, `safe_removal`, `doc_code_coverage_drift` | `audit.py health` gate | hub | **fail-closed** (FAIL-class) |

> *Caveat the map states about itself:* it is hand-maintained today; a generated `docs/ORGAN-INDEX.md` (#132) will become its verified source once it ships — until then, this table is memory, not mechanism (a small instance of the disease the repo fights).

### 5.2 The `audit.py` check registry — 26 checks, two postures on one list

`scripts/audit.py` is the self-audit + cross-repo conformance engine (read-only, Layer-2). `ALL_CHECKS` = **26 registered checks** (`audit.py:1915-1942`; live count confirmed = ARCHITECTURE's claim of 26 — no drift). The same list runs under two very different postures:

- **`health`** = the `audit-health` **pre-commit gate**: **FAIL blocks the commit, WARN only informs** (`audit.py:2390-2391`). Sets `_GATE_MODE=True` so the expensive `doc_claims` pytest-collect claim is skipped for speed (~1.4s).
- **`ship-gate`** (#147) = the `/ship` **arc gate**: reads `Finding.status` directly (awareness organs exit 0 on drift), runs the full verification, and blocks on **any FAIL *and* any new/undispositioned WARN**; expected WARNs are dispositioned via `ecosystem/disposition-register.yaml` (a register entry matching no live WARN is surfaced as `[stale]`).
- **`run` / `repo`** = the manual cross-repo sweep; identical check list, advisory (no downstream commit-gating), writes only into `.dev-knowledge`.

**Severity is decided by each check, not a config flag** — each returns a `Finding.status` in `pass|fail|warn|unavailable|n/a`; the gate interprets it. The **awareness-organ pattern** is deliberate: the six hub-only drift checks (`git_backlog_drift`, `doc_claims`, `no_ff_merges`, `doc_rot`, `doc_structure`, `doc_code_edge`) **emit WARN, never FAIL, by design** so they never wedge the per-commit gate — they surface at `ship-gate` instead. The FAIL-class (blocking) checks are the structural/presence baseline plus `handoff_probes` (a toothless probe cannot ship), `reconciled_versions` (fail-closed on version mismatch), `safe_removal`, and `doc_code_coverage_drift` (the meta-gate: a newly-added `ALL_CHECKS` member cannot silently escape the curated doc→code coverage).

**Key checks (behavior):**
- **`canonical_freshness` (#10)** — `last_reviewed` cadence over VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS/handoffs-README. Two signals: **A2 (FAIL)** — `last_reviewed` predates the file's last git-commit date → "edited but not re-reviewed"; **A1 (WARN)** — older than the 30-day backstop. A2 is **commit-based, not working-tree** — the root of the §7.3 forced-stamp problem: a count-bump commit trips A2 even with no genuine review.
- **`doc_claims` (#89, WARN)** — living-doc count/list prose vs ground truth (ARCHITECTURE "N registered checks" vs `len(ALL_CHECKS)`; pre-commit gate count; CLAUDE §9 roster; test-count off-gate).
- **`reconciled_versions` (FAIL, coherence spine)** — a dependent's `reconciled_with: <spec>@<version>` must equal the spec's live version; mismatch → FAIL (fail-closed); own-input error → WARN (fail-open).
- **`no_ff_merges` (#153, WARN)** — a non-merge commit on main's first-parent spine (direct-to-main or FF); **detect-and-surface only**. True *prevention* is the separate `block-ff-push` pre-push gate (the PREVENT half; hub-only, fail-soft, bypassable via `--no-verify`).
- **`doc_code_coverage_drift` (#203, FAIL)** — every `ALL_CHECKS` member is `coverage_scope`-annotated or explicitly exempt (the coverage meta-gate for the doc→code edge).

### 5.3 The three deterministic gate layers

- **Pre-commit (10 gates, `.pre-commit-config.yaml` / CONTRIBUTING.md:97-110):** `normalize-dated-headers`, `codemap-freshness`, `toc-freshness` (ARCHITECTURE), `toc-freshness-playbook`, `validate-backlog`, `audit-health` (FAIL blocks), `ruff` (≥0.15.5), `coherence-nudge` (non-blocking, always exits 0), `backlog-id-on-close` (commit-msg), `block-ff-push` (pre-push).
- **Ship-gate (`/ship` arc):** the #147 verification-organ gate (arc-shipped point 6), reading `Finding.status`, dispositioning expected WARNs.
- **Session-end Stop-gate (ADR-85, `DEFINITION_OF_DONE.md`):** the single source of truth for session-close. **JOURNAL leg — hard block, un-gameable:** any session with commits must add a JOURNAL entry naming ≥1 commit SHA from *this session* (the session boundary, not the push boundary — the C1 fix, 2026-06-19). **BACKLOG leg — advisory nudge (v1),** promoted to hard only when the traceability-spine ADR lands (#170→#168). Rationale (a load-bearing design principle): *a hard gate is justified only for a check that is BOTH un-gameable AND always-warranted* — the JOURNAL SHA anchor qualifies; the BACKLOG marker qualifies for neither (LESSONS 2026-06-16). Escape only via logged, HEAD-bound `/override`; no auto-bypass-after-cap.

### 5.4 The coherence spine (`validate_reconciliation.py` + `coherence_enumerator.py`)

The spine enforces the **doc↔doc declared edge** — `reconciled_with` — split into a deterministic gate half and a semantic enumerator half (the ADR-88 "completeness is deterministic, judgment is semantic" split):

- **`validate_reconciliation.py`** — the **deterministic gate half** (`# rule: coherence-spec-reconciled`). A single-entry spec registry (`handoff-process` → `HANDOFF_PROCESS.md`); the spec version is read **live, never hardcoded**. It discovers every `.md` declaring `reconciled_with` frontmatter (v1: exactly one edge — `docs/handoffs/README.md` → `handoff-process@<version>`), classifies `match|mismatch|malformed|unknown-spec`, and the audit adapter maps **mismatch → FAIL** (fail-closed), malformed/unknown → WARN (fail-open on own error). On mismatch it emits a copy-pasteable `check-against-spec` skill invocation to drive the semantic re-reason.
- **`coherence_enumerator.py`** — the **enumerator half**. Given a flagged stale edge, it deterministically **over-extracts** every candidate reference site into 5 categories and renders a flat checklist where an LLM verdicts each site `stale|fine|not-relevant`. *"Over-extraction is fine; missing a real site is the only failure mode."*

The three-part enforcement pattern (ADR-88 Principle 2): **deterministic trigger + AI per-site verdict + human signature.** The completeness (which sites exist) is deterministic; the judgment (is this site stale) is the LLM's; the human ratifies. Note the scope boundary: the spine covers `reconciled_with` only — `serialize-group` / `depends-on` are handled elsewhere (BACKLOG cycle-check in `validate_backlog.py`; doc→code via `validate_doc_code_edge.py`).

### 5.5 The verification mesh — layered dimensions (`ARCHITECTURE.md:538-553`, Ch6)

Checks escalate from cheap/local to unattended/cross-repo; each layer checks a *different dimension*, so a green one and a red other are both correct:

| Layer | Organ | Dimension | Posture |
|---|---|---|---|
| In-session | `verify` skill (pytest+ruff+git) | does this step pass its gates | per numbered step |
| Pre-merge | `/codex-review`; `/ship` gate | code-diff correctness; branch→`--no-ff`→clean | operator-invoked |
| Nightly (cloud) | conformance Routine | claims-vs-docs coherence (own repo) | read-only + skeptic |
| Nightly (local) | `fleet_health.py` / `audit.py run` | structural + freshness-stamp health (repo + siblings) | deterministic, fail-soft |
| Funnel | `surface_triage.ps1` + morning triage | operator ratifies before findings bind | human gate |

The nightly cloud run is defined by `conformance-hub.js` but the native Workflow launcher is not enabled in cloud, so a Routine **falls back to reading the `.js` as a spec** — with the load-bearing consequence that *any guarantee written as in-script code is inert on the fallback path; the real backstop sits on the executing path (the Action/parser), not the generator* (ADR-72/80; `CONTRIBUTING.md:149-168`).

---

## §6 — Next steps, mapped to the backlog

The backlog is a story map (ADR-66): Big Picture → 7 themes → user stories → tasks `[#id] [P][size] · Done when · refs`. Done items **leave** the file (ADR-65). The near-term frontier is the **dissemination arm** + paying down the debt the deploy build created.

### 6.1 The immediate arc (post-#226/#230 closure)

| ID | P/size | What | Depends / sequences |
|---|---|---|---|
| **#222** | P2/M | Decouple ARCHITECTURE's pytest-count claim from the freshness gate (the forced-stamp root cause) | pairs with #223 |
| **#223** | P2/M | Document the deploy subsystem in ARCHITECTURE (organ map + carriers + mesh + Validators) via a *genuine* re-read + honest re-stamp | same visit as #222; enlarged by the #226 arming build |
| **#224** | P3/S | Rotate ADR-90/91/92 into ARCHITECTURE Governing-ADRs + CLAUDE §11 | — |
| **#225** | P2/M | precommit carrier — comment-preserving surgical edit (kill the YAML round-trip noise) | deploy-arc residual; refs #221 |
| **#221** | P2/M | Deploy across the fleet (corp-monorepo, corp-ops, corp-sca-time-automation) → n=2+ gate + populate the registry | **must follow #226** (done); each deploy uses #230 as its acceptance gate; closes when #223/#225/#226 close |
| **#231** | P3/M | Consumer→hub feedback report (structured gap/ambiguity/broken-piece report instead of guessing) | refs #230/#215/#221 |
| **#232** | (soft-reserved) | ship-gate right-sizing (the PowerShell false-RED env artifact — handoff_probes shells to grep/sed absent on PATH) | architect's candidate |
| **#233** | P3/S | Isolate the deploy-record-index test's tempdir (concurrency-fragile `listdir(gettempdir())`) | test-hygiene debt |

**Explicitly deferred (correct, not this arc):** the C.3 live `claude -p` floor-sentinel smoke (optional); the active-push decision (§7.6); the deploy tool's fleet-batch / version-delta / rollback / drift-poller (ADR-92 out-of-scope list).

### 6.2 The dependency graph as it stands (serialize-groups + depends-on)

**`serialize-group`s** (tasks that must land in order within a group): `handoff` (#1/#26/#159/#161/#162/#164), `playbook` (#146/#18/#27/#67/#213/#214/#217/#219 …), `audit-py` (#7/#36/#95/#139/#166/#190/#210/#211 …), `coherence` (#180/#181/#182/#220 — the ADR-88 spine extensions), `claude-md` / `claude-md-template` (#112/#157/#17/#109/#129), `architecture` (#35/#165/#223/#224), `pre-commit-config` (#15/#132), `code-edge` (#218), plus `environment` / `settings-json` / `record` groups.

**`depends-on` edges (the hard sequencing):**
- **#112** (adr_amend helper) → **#23** (ADR supersedes/related/amends graph)
- **#168** (harden ADR-85 BACKLOG leg to a hard gate) → **#170** (the traceability-spine ADR — issue-ID↔commit anchor)
- **#169** (ungated-doc staleness detection, ADR-85 R2) → **#171** (build the `ecosystem/conformance.md` dashboard, ADR-86)
- **#221** (fleet rollout) formerly `depends-on: #226` (dropped 2026-07-02 — arming landed)

Two **cross-cutting spine items** worth the reviewer's attention: **#170/#168** (the traceability-spine that would promote the session-end BACKLOG leg from advisory to hard — the one gate ADR-85 explicitly left half-built), and **#171/#169/#86** (the conformance dashboard where ungated-doc staleness — including ARCHITECTURE's — is meant to surface deterministically instead of by human memory).

---

## §7 — Open architectural tensions (the highest-value section)

*Each fork below is stated with the evidence on both sides and what a ruling would settle. These are where the reviewer can propose decisions the system cannot make for itself.*

### 7.1 Does "configured-not-armed" generalize as a failure class beyond the floor?

**The finding.** The floor arc discovered a facade: files present but the mechanism inert (a floor that loads but whose guard never fires; a plugin deployed but its ruff gate unapplied — `ADR-92:8`). ADR-93 fixed it *for the floor* via the two-leg hash-guard and the #230 "proven" stage. The `PRESENT_DRIFTED` carrier state generalizes the *shape* (`contract.py:50`), and the sealing test (*"does this mechanism have its consumer/gate?"*, `PLAYBOOK.md:258`) is the standing guard against *built-without-consumer*.

**The open question.** Is "configured-not-armed" a **class** that should be systematically hunted across *every* carrier and *every* organ (a coverage audit of "is this thing actually armed, not just present?"), or is it adequately handled case-by-case as each organ ships? BACKLOG **#188** (deny-rule + hook completeness audit) and **#132** (organ-index generator) are adjacent but not the same question. A ruling would decide whether the system needs a general "armed-not-just-configured" conformance dimension, or whether per-organ proof (the #230 pattern) replicated at each rollout is sufficient.

### 7.2 The hash-guard is load-bearing — is single-point-of-failure acceptable?

**The finding.** ADR-93 states it plainly: *"The hash-guard is load-bearing: if it were weak — commit-only, silent, or trivially bypassed — model A would degrade into exactly the committed-copy-that-silently-drifts #95 fears … If the guard ever proves unbuildable or materially weakened, reopen model B"* (`ADR-93:40-42`). Two known bypasses are accepted: `--no-verify` / out-of-CC commits (session-start leg is the backstop) and the greenfield-`settings.json` limit (#221 must generalize; ai-council retired it by test only because it pre-tracks settings.json).

**The open question.** Is a single load-bearing guard (however well-tested) the right risk posture for the mechanism that keeps the *entire disseminated corpus* honest? The tension: the whole model A rests on the guard firing; the guard's own coverage has a greenfield hole that is only closed for one consumer. A ruling would decide whether fleet rollout (#221) requires (a) a hardened greenfield-settings.json path as a *precondition*, (b) a second independent guard leg, or (c) acceptance of the documented residual with the session-start leg as sole backstop.

### 7.3 The forced-stamp debt — the freshness gate passes but genuineness is unverifiable

**The finding.** `canonical_freshness` A2 is commit-based: `last_reviewed < last-commit-date → FAIL`. Any edit that advances the commit date (even a pure pytest-count bump) forces a same-day `last_reviewed` re-stamp — with **no mechanism that the re-stamp reflects a genuine end-to-end re-read**. ARCHITECTURE's 2026-07-01 stamp is the proven-false instance (§4.2): the file was "re-stamped" while omitting the entire deploy subsystem. Filed as **#222** (decouple the volatile count) + **#169/#171** (surface ungated-doc staleness deterministically).

**The open question.** The gate enforces *"the stamp is not older than the last edit"* but cannot enforce *"a human/agent actually re-read the file."* Genuineness is, by construction, outside a deterministic gate's reach (the same limit ADR-85 hit when it demoted the four ungated docs to "update when materially affected"). A ruling would decide the right shape: (a) decouple volatile counts into a generated fragment so edits stop forcing stamps (#222), (b) split "freshness" (deterministic) from "reviewedness" (a separate, honestly-advisory signal in the #171 dashboard), or (c) accept that `last_reviewed` is a *claim* and gate only its non-regression. This is a specific instance of a general question: **what should a deterministic gate do when the property it cares about is inherently semantic?**

### 7.4 Doc↔doc semantic edges are open-world — is advisory-by-design the right stance?

**The finding.** The declared doc↔doc edge (`reconciled_with`) is gated (FAIL on version mismatch). But *discovering* undeclared edges — a doc that prose-references a spec without declaring the edge — is **advisory only**: `scan_undeclared_edges` *"surfaces; does not gate"* (`PLAYBOOK.md:256`), emits candidates for human confirm, writes nothing. ADR-88 makes this a principle (narrow-first; do-not-build-is-doctrine). The reason is logical: doc→doc semantic edges are **open-world** — you cannot deterministically enumerate every place a document *should* declare a dependency, so declaration-completeness is not machine-decidable (the partial-closed-world finding).

**The open question.** Given that completeness is logically unavailable, is the current *"declare the edges you know; surface candidates; never gate discovery"* stance correct, or does the system need a stronger nudge (e.g. promote the undeclared-edge scan to a WARN in the ship-gate, or the #205 `check-against-spec`-on-bump content re-reason as a gate)? Related open axis: **#220 — the MODIFY / semantic-drift edge** — a source whose *meaning* changes while its version pin and symbol signature stay put leaves dependents silently stale, and *no* current organ catches it (verify-first pending). A ruling would settle whether advisory-by-design is the permanent stance for the open-world half, or an interim one pending the semantic-drift work.

### 7.5 The reverse-dependency-legibility thesis — sound, and fully applied?

**The finding.** ADR-88/89's thesis is *"declare what you cannot compute; compute what you can"* — the graph is in-repo (declared) or computable-from-source (Pyright oracle), held by machinery not memory. It is elegant and largely realized. But application is **partial**:
- The code→code oracle is built, but its consuming safe-removal gate delivered **M1 only** (#195); M2 (computed path / dotted-module string refs) + M3 (declared-prose reverse-deps) are **deferred to #218**. So a symbol deletion is guarded against *import* referrers but not against string/path/prose referrers.
- The oracle binds **three normative limits** (repo-scoped — no extrapolation to corp-monorepo; static-Python-only — dynamic/getattr/string-keyed-registry/cross-language edges out of scope; call-hierarchy warm-up) — meaning whole edge classes are held *by tests and the doc→code scheme*, not by the oracle.
- Free-prose docstrings are outside the legibility graph entirely (the stale `tool.py` execute docstring, §4.6, is uncaught).

**The open question.** Is the thesis sound (yes, on the evidence) *and* is the current coverage the right stopping point, or should the reviewer push for M2/M3 (#218) and the semantic-drift axis (#220) as preconditions before the fleet grows the code surface the oracle can't reach? Deeper: the thesis assumes an **agent-override bias** — that an agent will follow the declared/computed graph rather than its own recollection. ADR-87 already found CC's self-load unreliable for governance/read-only tasks (GAP-3), and the GAP-2 execution-time gotcha backstop is *filed-not-built* (#185). A ruling would settle whether the legibility graph is trustworthy enough to *lean on* fleet-wide, or whether the unreached edge classes (M2/M3, semantic-drift, prose) are large enough to demand closure first.

### 7.6 Manage-over-time — active-push vs drift-catch-on-re-run?

**The finding.** The deploy model is deliberately **one-way, hub→consumer push once, + local drift-catch** (ADR-93 Model A: *"the hub pushes the canonical floor once … copy-drift is caught by the guard rather than avoided by non-tracking"*, `ADR-93:18`). There is **no** consumer→hub feedback loop (filed as #231, not built) and **no** organ detecting template↔copy drift *between* rollouts for the per-repo orchestration copies (#95, ADR-73's own acknowledged cost). Active-push (re-run the deploy on every consumer to stay current) is not chosen but not ruled out beyond the floor.

**The open question.** As the fleet grows to n≥2, which currency model governs, and when? Options: (a) **drift-catch** — push once, rely on the hash-guard + a periodic read-side audit to surface staleness (current default; needs #95 for the orchestration copies); (b) **active-push** — the hub re-runs deploy on a cadence (tension with the Layer-2 *autonomy-no* invariant — this would be the hub initiating cross-repo writes on a schedule, which ADR-78/92 currently forbid); (c) **consumer-pull** — consumers re-pull on their own cadence (the pre-commit source-repo carrier already works this way; the floor does not). A ruling would settle the currency model per carrier and whether #231's consumer→hub feedback is a precondition for any of them.

### 7.7 Two-track coherence — is the dwutorowość clean, or does one track leak?

**The finding.** The system genuinely runs on two tracks, but the framing is not internally uniform (§2.0):
- The canon names them **Workflow / Coherence** (`PLAYBOOK.md:229`); the brief names them **authoring / delivery**. These are *different cuts* — ADR lifecycle, handoff, and Council are Track-1 "authoring" in the brief but are mapped to **Lifeline 1 (Workflow)** in PLAYBOOK's own chapter map (`PLAYBOOK.md:262`).
- **§20 (the deploy runbook) is unmapped to any lifeline** — the chapter map lists up to §19. The entire dissemination arm — arguably a *third* track (the "Disseminator" role, `VISION.md:17`; the "Dissemination" frontier stage, `ARCHITECTURE.md:533`) — has no home in the two-lifelines frame.
- The corpus already senses this: **#219** (cross-reference the two loop framings — PLAYBOOK "two lifelines" = execution/consistency view vs ARCHITECTURE Ch6 "methodology engine" = knowledge-evolution view — *"a fresh reader has no signal they're complementary"*).

**The open question.** Is the two-lifelines model the right decomposition, or does the system actually have **three** tracks (author the method / deliver work / disseminate the method) — with dissemination currently mis-filed or homeless? The leak is real: the brief's "authoring" spreads across both lifelines, and deploy sits outside both. A ruling would settle whether to (a) keep two lifelines and explicitly fold dissemination into Coherence (corpus-consistency *across repos*), (b) name a third track and re-home §19/§20 + the deploy ADRs under it, or (c) reconcile the "authoring vs delivery" and "workflow vs coherence" vocabularies into one canonical frame (closing #219 structurally rather than with a cross-pointer).

### 7.8 (Bonus, surfaced by this audit) The system shipped its own deploy subsystem without its own tracking discipline

**The finding.** The ADR-91/92 deploy subsystem was *"built 2026-06-29→07-01 and proven on run #1, but shipped with no backlog item and no closure tag — recorded here retroactively"* (BACKLOG #221; JOURNAL 2026-07-01 `cadf53d`). The system whose entire premise is *"held by mechanism, not memory"* built its most significant recent subsystem *by memory* (in-conversation), then reconstructed the backlog trail after the fact.

**The open question.** This is not a defect in the shipped code — it's a gap in the system's *own* application of its arc-shipped discipline (Ch12.1) to a fast-moving build. Is the closure loop (propose_closures → /review-closures) + the session-end gate sufficient to catch *untracked* work, or does the "backlog carries the work, not the conversation" principle (JOURNAL's recurring phrase) need a mechanical backstop of its own — e.g. the #139 merged-arc→record verifier, which is precisely the *"every merged arc on main maps to a backlog item / closure / documented no-item class"* gate, still deferred? A ruling would decide whether the retroactive-filing pattern (which worked, but by discipline not mechanism) is acceptable, or whether #139 should be prioritized to close the gap for the fleet-rollout arc that is about to generate a lot of arcs.

---

## Appendix — what the reviewer is holding

- **Deploy fleet state:** n=1 (only ai-council at v1.0.0; three consumers + the hub null). Fleet rollout = #221, gated on the just-closed arming.
- **Doc currency:** ARCHITECTURE is the one canonical file whose freshness stamp is presently forced/false (#222/#223); everything else is current or has only filed, low-severity gaps.
- **The corpus's own self-image of its frontier:** *"The two frontier stages — Enforcement and Dissemination — are where active work concentrates"* (`ARCHITECTURE.md:535`). §7's tensions cluster on exactly those two frontiers.
- **The standard to judge against:** the repo exists to kill **resident-copy drift** — "held by mechanism, not memory." Several open tensions (7.3, 7.5, 7.7, 7.8) are places where that cure is incomplete or where the mechanism is not yet trusted enough to lean on. That is the review's highest-leverage target.

---

*End of audit. Read-only synthesis; no repo state was mutated in its production. All citations resolve against HEAD `b986711`.*
