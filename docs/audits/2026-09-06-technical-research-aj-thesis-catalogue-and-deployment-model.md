# AJ CORPUS + MSc THESIS — the file-by-file catalogue, and the deployment-model decision memo

**Date:** 2026-09-06 · **Class:** technical (slug carries `research`) · **Lane:**
`lane-t-000-aj-research`, batch T wave 1, contract §3.5 · **Seat:** CC (Opus 5) ·
**Substrate:** CLOUD, read-only · **Branch:** `claude/lane-t-000-aj-research`

> **Read this limit first, because it bounds every row below.** This lane ran **off the
> operator's machine**. The Architekt Jutra corpus (48 files, 771.4 MB) and the MSc thesis
> (`Praca_Dyplomowa_Magisterska/`) live on the operator's disk and were **never committed** —
> `docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md:48` says so in its
> own words ("outside the repo, not committed"). The contract's `aj-scratch/inventory/INVENTORY.md`
> is therefore **unreachable from this substrate**, and so is the thesis TeX tree.
>
> **What this lane did instead, deliberately, and what makes it worth having:** it catalogued the
> corpus **through the locators that survive into the commit tree**. Three prior arcs read the
> primary sources and recorded per-file locators; those locators are in `main` and are re-openable.
> This document is the file-by-file assembly of them, with **our** side re-read live at this HEAD.
> Every row states which side is primary-read and which is second-hand. A row whose corpus side
> exists only in a deleted scratch is marked as such and carries a **recorded empty search**, never
> a borrowed confidence.
>
> **Library-first, discharged twice.** The thesis half was not re-derived: it already exists as a
> two-sided, file-by-file catalogue at `docs/audits/2026-08-29-technical-thesis-compare-out.md`,
> which is reused and cited rather than rewritten. The corpus half reuses the two AJ arcs' locator
> sets. This lane wrote no new extractor, parser or inventory tool.

**Consumes:** `docs/intake/2026-09-05-tech-aj-second-pass.md` (cited **by path** — `intake-id: 70`
is allocated twice in the live tree, the sibling being
`docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md`) ·
`docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md` ·
`docs/audits/2026-09-05-technical-research-aj-second-pass.md` ·
`docs/audits/2026-08-29-technical-thesis-compare-out.md` ·
`docs/audits/2026-09-05-technical-fleet-readiness.md`.

**Governance:** ADR-111 — nothing enters the tree from this arc except this audit. **No row is
born here. No `tasks/` file is touched. Nothing is deleted or retired.**

---

## §0 · The deployment-model decision memo

**The question, in the architect's own words** (`docs/handoffs/2026-09-06-dev-knowledge-architect/HAND_CARRIED.md:25-29`):
how Maister **deploys** to a project versus our carrier, and whether each consumer repo runs its
own CC sessions independently or work must route through the hub — *"as a decision memo with
trade-offs measured on fleet-readiness §0, not as opinion."*

### 0.1 · The measurement, taken from fleet-readiness §0 and re-read at this HEAD

`docs/audits/2026-09-05-technical-fleet-readiness.md:23-40` verdicts 9 declared consumers. The
column that decides this memo is not the verdict — it is the **deployed version**, read live from
`ecosystem/deployed-versions.yaml`:

```
consumer                  deployed corpus   source_tag   fleet-readiness §0 verdict
.dev-knowledge (hub)      null              null         READY - baseline source, PASS
ai-council                1.3.1             v1.3.1       NEEDS 1 waiver, 1 release behind
corp-monorepo             1.2.0             v1.2.0       NEEDS 2 waivers, 2 releases behind
win-tooling               1.4.0             v1.4.0       NEEDS 1 waiver, 1 defect
corp-ops                  null              null         BLOCKED - no floor deployed
corp-sca-time-automation  null              null         BLOCKED - canonical_freshness FAIL + no deploy
terminal-setup            null              null         BLOCKED - never audited, no state.yaml
demo-prep                 -                 -            BLOCKED - never audited, no state.yaml
life-architect            -                 -            BLOCKED - never audited, no state.yaml
```

Latest manifest is `deploy/manifest-v1.5.0.yaml`; latest **tagged** release is `v1.4.0` — v1.5.0 is
a release candidate and untagged (`deploy/manifest-v1.5.0.yaml:12-14`; the operator tags, ADR-91).

**Three deployed consumers carry three different corpus versions, and at least one of them is a
ratified pin rather than drift.** `ecosystem/deployed-versions.yaml:52-56` states it in the file
itself: corp-monorepo *"Stays 1.2.0 BY DESIGN … #336/ADR-102 (Accepted 2026-07-17) ruled NOT to
bump … Do not 'fix' to 1.3.1."* Read fleet-readiness §0 alone and corp-monorepo is "2 releases
behind"; read the durable record and two of those releases are a **decision**. Both statements are
true, and the thing that reconciles them is the **waiver**.

**That is the whole measurement this memo turns on:** the fleet's real operating mode is
per-consumer, per-component divergence that is *ruled*, not accidental — and fleet-readiness §0
counts waivers (2 · 1 · 1) precisely because it is.

### 0.2 · The two models, and what each can and cannot express

**Maister's model — plugin pull.** A plugin installed from a marketplace, resolved at install
time. Its measured behaviour is recorded at
`docs/audits/2026-09-05-technical-research-aj-second-pass.md:245-253` (deviation D2): the plugin
registry is **machine-wide**, so *"any known marketplace contributes a disabled row to every
project"*, and **both** scope routes (`project`, then `local`) were tried and the row survived
both. Install state is a property of the machine, refined by a per-project enable flag.

**Our model — carrier push.** `deploy/tool.py` plus registered carrier modules write files **into**
the consumer tree, versioned by `deploy/manifest-v*.yaml`, with the result recorded durably in
`ecosystem/deployed-versions.yaml` and the floor guarded by a hash sidecar
(`ARCHITECTURE.md:466`; ADR-91/92/93).

**The decisive asymmetry, stated as a capability rather than a preference:**

- A pull registry can express *installed / not installed / enabled for this project*. It has **no
  place to put a ratified version pin**, because the version is resolved at install time and the
  registry is machine-scoped. There is nowhere for ADR-102's *"do not fix to 1.3.1"* to live.
- A push carrier can express it, and already does: a per-repo key with a version, a date, a source
  tag, and a comment block carrying the ruling that froze it.

**So the model is not a choice between the two.** The hub already runs **both**, and has since
v1.0.0: `deploy/manifest-v1.5.0.yaml:208-220` declares carrier #2 `tier1-plugin`,
`implemented: true` — *"the tier1-lifecycle CC plugin enabled at project scope in the consumer …
reconciles via the external `claude plugin` CLI; correctness judged from the resulting installed
state, never stdout."* Pull is already carrier-shaped here, and its correctness is judged from
end state rather than from the CLI's own report.

### 0.3 · The model chosen

> **PUSH for anything a consumer may pin or waive; PULL for anything fleet-uniform by
> construction — and both legs stay COMPONENTS in the deploy manifest, each with a declared
> version and a drift check on both sides.**

This is not a new architecture. It is the split the hub already implements, promoted from an
accident of which carrier was written first into the stated rule, with the discriminator named:
**does this component have a legitimate per-consumer divergence?** If yes it is push-carried,
because only push has somewhere to record the ruling that authorised the divergence. If no, pull is
cheaper and should be preferred, because push costs one operator act per consumer per release and
the fleet shows exactly what that costs — **five of nine consumers carry no floor at all, and three
of those have never been measured** (fleet-readiness §0; `membership_agreement` `state-dirs 6/9`).

The one genuinely new obligation the model adds is the **second drift surface**: a hybrid has two
places to be wrong, so plugin-carried state needs the same both-sides drift check that
`deployed_methodology_version` already gets. Carrier #2 half-satisfies this today by judging from
installed state rather than stdout; what it lacks is a durable per-consumer record of the plugin
version, the way `ecosystem/deployed-versions.yaml` records the corpus version.

**Flip-condition** (the instrument the thesis supplies and this repo does not yet require —
§3 row T-07, and open row `[#616]`): *if `claude plugin` gains per-project version pinning and a
way to express a waiver, the push leg loses its justification for waivable components and the model
collapses to pull.* That is the single input change that reverses this recommendation, and it is
recorded so the decision can be revisited on evidence rather than on fatigue.

### 0.4 · Hub-managed versus independent CC per consumer — this half is ALREADY RULED

The second question does not need deriving; it needs **citing**, and a memo that re-opened it would
be manufacturing a fork the repo already closed.

- **Core invariant #4 (ADR-28, ADR-36):** Layer 2 never executes — *no script drives state in a
  child repo* (`CLAUDE.md` §5 rule 4; `AGENTS.md` "What this repo is").
- **ADR-92 Decision 3**, the three-edge boundary, verbatim at
  `docs/decisions/ADR-92-deploy-runbook-doctrine.md:29`: **write-yes, commit-no, autonomy-no.**
- **ADR-93 §4** (`docs/decisions/ADR-93-floor-provisioning-model-a.md:34`): *"All writes stage
  only; the operator commits (ADR-92 commit-no)."*
- Rendered in the organ table at `ARCHITECTURE.md:466`: `write-yes / commit-no`.

**Answer: each consumer runs its own CC sessions, independently.** The hub deploys; it does not
drive. "Route the work through the hub" is refused by a core invariant, not declined by preference.

**The genuinely open sub-question, and it is narrow:** does the *deploy act itself* run from a hub
seat or a consumer seat? That has a measured answer already in the tree, and it is a limitation
rather than a doctrine — `ecosystem/deployed-versions.yaml:83-92`, on win-tooling's v1.4.0 deploy:
the record was *"written by the lane rather than by `deploy/tool.py --execute` because the RULING-W
shape binds the deploy to a consumer WORKTREE and the tool resolves the consumer as
`hub_root.parent / repo` with no override — so the lane drove the tool's own carriers against the
worktree and writes the record here."*

**That hard-coded consumer resolution is the one measured obstacle between this model and its first
consumer.** It is reported here, not fixed — this lane is read-only and owns no code.

### 0.5 · The first consumer this applies to

> **corp-monorepo.**

Three independent reasons, and the third is why it is the right *first* rather than merely the
first in a list:

1. **Measured largest gap** — fleet-readiness §0 rows CM-1 / CM-2 / CM-6: floor v1.2.0, two
   releases behind, NEEDS 2 waivers. It is the widest spread in the fleet.
2. **The operator's own priority order**, carried in-tree at
   `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/SUPPLEMENT.md:94-95`: *"Priority order
   hardened: monorepo deployment FIRST, ai-council second, win-tooling receives migration last
   though it remains consumer #1."*
3. **It is the case that exercises the waiver leg rather than avoiding it.** corp-monorepo is the
   consumer whose version divergence is *ratified* (ADR-102 / `[#336]`). A model whose whole claim
   is "push is required because only push can carry a pin" should be proven first on the consumer
   that actually has one. Deploying to a clean consumer first would demonstrate nothing this memo
   is asserting.

**Relayed-ruling notice, flagged rather than acted on (C-1).** `HAND_CARRIED.md:47-56` relays
architect-inbox item **024**, whose text — *"At this scale NOTHING may be a per-repo act. Every
element … is a COMPONENT with a version in the deploy manifest, shipped by the carrier, with a
drift check on both sides and a per-consumer waiver"* — is the same shape as §0.3, and whose floor
staging names *"v1.5.0 = shape seal + regions + hooks + plugin + waivers + freshness registry (j) +
roles table (008), enough for H0 on corp-monorepo."* **024 itself is in `to-cc\` and is not
reachable from this substrate.** It is cited here as corroboration read from a committed handoff
artifact, **not** as the authority for anything above; every load-bearing claim in §0 rests on a
locator this lane opened at this HEAD. If 024's text and this memo diverge, 024 governs and this
section is superseded.

---

## §1 · Vocabulary bridge — BEFORE any absence claim

The first-pass arc's most transferable finding was a methodology one
(`…gap-analysis.md:35-40`): **searching a second system for the first system's words manufactures
absence** — three of eight ONLY-AJ rows were false because every search had been run in AJ
vocabulary. That arc built its bridge *after* the searches. This one states it first, and every
absence claim in §2–§3 was searched in both lexicons.

The bridge below is **not restated** — it is carried at `…gap-analysis.md:84-104` (24 term pairs)
and reused. What this lane adds are the pairs the *deployment* question needs, which that table
does not cover:

```
their term / thesis term            our term                              same thing?
plugin install (marketplace)        carrier (deploy/manifest carriers)    same intent, opposite direction
                                                                          - they pull, we push
plugin registry (machine-wide)      ecosystem/deployed-versions.yaml      no - theirs is machine-scoped
                                     (per-repo, committed, durable)        and cannot hold a pin
/maister:init (derive standards)    deploy/carrier_floor.py + the floor   no - theirs derives per repo,
                                     hash sidecar                          ours replicates from the hub
project scope / local scope         per-consumer waiver + gate_rev_ahead  no - theirs is an enable flag,
                                     (ADR-102, parity-surfaces.yaml)       ours carries a ruling
(no equivalent)                     write-yes / commit-no / autonomy-no   no - they orchestrate freely
                                     (ADR-92 Decision 3)
miara odpowiedzi (response measure) acceptance criteria (ex-ante),        yes - independently reinvented
                                     ADR-81 frozen contract
symulowanie odpowiedzi              (none) - see [#616] FLIP-CONDITION    no
 + counterfactual re-run
pytania zamkniete (closed Qs)       bounded-deterministic probe           yes - ours is stricter
                                     (HANDOFF_PROCESS.md:204-216)
```

---

## §2 · The Architekt Jutra corpus — file-by-file

**Row grammar.** Each row: the corpus artifact · what it **claims / mechanises / names as a tool or
artifact shape** · its **corpus-side locator** · our side, **re-read live at this HEAD** · a
`sides:` token, which is machine-countable.

- `sides: both` — a locator resolves on **both** sides.
- `sides: empty-search` — the corpus side is **not re-openable from this substrate** (deleted
  scratch or operator-disk-only) and this lane ran a search in the tree that came back empty; the
  search is recorded in §4.1.

**Provenance discipline.** Corpus-side locators are **second-hand** — read by the P0–P5 legs of the
first-pass arc and by leg M of the second pass, not by this lane. They are reproduced with their
originating locator so a seat with disk access can re-open them. Our-side locators are **primary**:
every one was opened in this session.

### 2a · Course material — 2 modules, 13 lessons, 2 ebooks (Polish throughout)

| # | Corpus artifact | What it carries | Corpus locator | Our side (read live) | sides |
|---|---|---|---|---|---|
| A-01 | `AJ_M01L01` | Harnessability named as a quality attribute; "ready-made harness or build your own?" asked and left open | `M01L01:137-139`, `:119-123` | `docs/audits/2026-05-29-harness-engineering-positioning.md:62-63` names **"Agent legibility"** as a QA — our word, different referent (observability, not harnessability); `docs/decisions/ADR-112-two-tier-adoption-bar.md` is the ratified answer shape they leave open | `sides: both` |
| A-02 | `AJ_M01L02` | The prompt → context → harness engineering ladder; per-loop trace inspection (Phoenix, local); fast-in-loop vs slow-in-CI; model routing via a LiteLLM gateway; measure a token optimisation on *your own* usage | `:28-44`, `:111-139`, `:187-207`, `:336-345`, `:397-407`, `:408-414` | ladder — same ladder stated independently at `…harness-engineering-positioning.md:44`; trace — `scripts/cost_usage_telemetry.py` is *"Library only; no call sites"*, while per-check `duration_ms` **is** live (`scripts/audit.py`, one call site at `governance_health.py:636`); check cadence — `CLAUDE.md` §4, targeted in-lane / full suite once at integration; routing — `ecosystem/routing-table.yaml` (dispatch-time, role→CLI); own-usage measurement — `logs/TOKEN-LOG.md` weekly aggregate only | `sides: both` |
| A-03 | `AJ_M01L03` | Observes that `CLAUDE.md` bloats — and stops at the observation | `:52-55` | `CLAUDE.md` header: **≤24,576 B**, gated by `tests/test_claude_md_byte_cap.py`. We took the observation and made it a test | `sides: both` |
| A-04 | `AJ_M01L04` | Standards mined from the repo's own history **and past PR review comments**; greenfield seeded from a mature sibling; intra-run phase decomposition with a machine state file; ADRs generated as a build byproduct; a clarifications contract; commit the orchestration artifacts | `:28-47`, `:30-34`, `:40-46`, `:192-194`, `:222-231`, `:223-226`, `:242-255` | mining — `scripts/silent_rule_detector.py` (corpus), `scripts/propose_closures.py` (commit history); **review history is the genuine absence** (§4.1 ES-06); seeding — `deploy/carrier_floor.py` + `deploy/manifest-v*.yaml`; decomposition — lane contract + `docs/handoffs/*/`; ADRs — `docs/decisions/ADR-94` freezes the body, **opposite provenance**; clarifications — `templates/handoff/v5/SUPPLEMENT.md.tmpl`, `.claude/commands/handoff.md`; artifacts — `docs/handoffs/`, `docs/audits/`, `JOURNAL.md` | `sides: both` |
| A-05 | `AJ_M01L05` | Cost per command as an architecture signal ($0.76 unmodularised vs $0.56 modularised); SlopCodeBench as a long-term-modifiability benchmark; harnessability again; the human stays accountable for architecture; cross-release API stability as a selection criterion; judge a dependency on its **AI-friendliness** | `:126-135`, `:44-56`, `:93`, `:61-64`, `:205-226`, `:239-246` | cost — `logs/TOKEN-LOG.md` is a weekly aggregate; no per-command cost figure exists; benchmark — `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` is a complete design, **never run**, guarded by `scripts/nopack_sandbox.py`; accountability — `ADR-108` §A splits functional/technical question routing; stability + AI-friendliness — `ADR-106` declares dependencies and `ADR-112` sets the adoption bar, neither asks either question (§4.1 ES-07) | `sides: both` |
| A-06 | `AJ_M01L06` | ADE / multiplayer shared agent sessions; artifact visualization against information overload | `:67-85`, `:123-149` | multiplayer — **recorded empty search**, and correctly so: single-operator system by design (§4.1 ES-01); visualization — `scripts/gen_trend_dashboard.py` → `ecosystem/trends.html`, committed `ecosystem/conformance.html`, `scripts/codemap/mermaid_emit.py` | `sides: both` |
| A-07 | `AJ_M01_ebook` | Harnessability (p11); the clarifications contract (p22); ADE (p28); visualization (p29) | `M01_ebook:p11,p22,p28,p29` | as A-01 / A-04 / A-06 respectively — the ebook restates the lessons rather than adding a claim | `sides: both` |
| A-08 | `AJ_M02_ebook` | **The greenfield inversion** — AI is *better* on a mature codebase than a blank page; deliberately seed reference implementations | `M02_ebook:p7` | `deploy/carrier_floor.py` + manifest carriers seed a child from the matured hub, which **is** the inversion in mechanism; no doc states it as a principle (§4.1 ES-02) | `sides: both` |
| A-09 | `AJ_M02L07` | ADRs as a byproduct (`:9`); run the agent from a directory already holding sibling implementations (`:103`) | `M02L07:9`, `:103` | ADRs — `ADR-94`; reference-implementation seeding — verified absent from `templates/prompt-template.md`, `.claude/commands/lane-boot.md`, `scripts/gen_lane_contract.py` by the first-pass arc, and it is that arc's surviving CANDIDATE 1 | `sides: both` |
| A-10 | 13 MP3 lecture recordings (373.7 MB, 4 h 18 m 54 s) | Audio of the 13 lessons | corpus inventory, `…gap-analysis.md:46-47`, `:59-61` | **No text-bearing content unique to them** — transcript coverage is 1:1 by filename stem, so the transcripts (A-01…A-09) are their content. Not transcribed, by operator ruling at P0 | `sides: empty-search` |
| A-11 | 8 ZIP archives (372.7 MB) | Re-bundles of the loose files | `…gap-analysis.md:62-63` | Six of eight SHA-256-verified byte-identical re-bundles; only the two `.md.zip` carried unique content and were unpacked into A-01…A-09 | `sides: empty-search` |
| A-12 | 12 slide decks | Per-lesson slides; `AJ_M02L07` has **none** (12 decks / 13 lessons) | `…gap-analysis.md:54-56`, `:64` | Extracted into the 27 P2 sheets; every claim they carry is folded into A-01…A-09. The missing deck is recorded so a successor does not search for it | `sides: empty-search` |

### 2b · The `SkillPanel/maister` plugin repo — @ `f75ef4fd1c61c15f1a891451afaf6b8e7a546a6a`

215 tracked files, 194 markdown — *"a prompt corpus, not a codebase"* (`…gap-analysis.md:50-51`).

| # | Corpus artifact | What it carries | Corpus locator | Our side (read live) | sides |
|---|---|---|---|---|---|
| A-13 | `orchestrator-patterns.md` | Every phase gate as **prose** instructing the model to call `AskUserQuestion`, with nothing verifying it (`:58-121`); the `orchestrator-state.yml` schema (`:217-260`); the dashboard projection (`:271-320`); `reverify_count` capped at 3 **in a field the model owns** (`:294-306`) | `:58-121`, `:217-260`, `:271-320`, `:294-306` | The inverse: gates are mechanisms here — the pre-commit / commit-msg / pre-push roster at `CLAUDE.md` §9, two of them **failing closed** (`block-ff-push`, `block-unanchored-push`); count computed at `ecosystem/doc-counts.md`, never restated. Retry caps: ours are likewise *stated, not enforced* — recorded as a **shared weakness**, not a win | `sides: both` |
| A-14 | `development/SKILL.md` | The five `task_characteristics` booleans that gate which phases fire | `:108-119` | `scripts/gen_lane_contract.py` already **shape-gates** emission, enforced by the `lane-contract-check` pre-commit hook; the shape is **typed by the author**, never inferred | `sides: both` |
| A-15 | `agents/gap-analyzer.md` | The agent that **derives** those five booleans from the task text | `:24-34` | No derivation step exists; this is the second-pass arc's CANDIDATE C-2 (size M, proposal-only per ADR-108 §A) | `sides: both` |
| A-16 | `agents/reality-assessor.md` | *Re-execute, do not trust the report* — re-runs the tests itself rather than reading the prior leg's verdict | `:12-20` | `ecosystem/routing-table.yaml` separates `reviewer` (judges a diff) from `adversarial` (attacks a design); **neither is defined as re-running the prior leg's tests**. Second-pass CANDIDATE C-4 | `sides: both` |
| A-17 | `agents/test-suite-runner.md` | Verification thresholds 100 % / 95–99 % / <95 % — read by the model, checked by nothing | `:99-104` | `uv run --locked pytest` plus the pre-commit roster; a threshold here is a hook exit code, not a paragraph | `sides: both` |
| A-18 | `implementation-plan-executor/SKILL.md` | Wave computation: greedy ready-set over disjoint `Files to Modify`, dispatched in **one** turn | `:65-92` | `scripts/boot_frontier.py` computes a frontier on **declared serialize-groups**, not files — different unit, same invariant. Their own caveat: nothing external re-derives disjointness before dispatch | `sides: both` |
| A-19 | `hooks/block-destructive-commands.sh` | The **only** hook in the plugin that can veto an action — denies `git reset --hard`, `git clean`, `rm -rf` for non-whitelisted agent types, deliberately excluding `task-group-implementer` | `:1-42` | Our OneDrive guard + the ADR-77 `PreToolUse` transcript-immutability guard, fail-closed. Same mechanism, different targets | `sides: both` |
| A-20 | `hooks/skill-invocation-reminder.sh` | A `SessionStart` hook whose entire job is re-injecting *"actually stop at gates"*, plus a second hook to re-inject it after compaction | `:4-9` | No analogue and none wanted — the finding is that this is **a system compensating for an unenforced rule by repeating it louder**. Our `SessionStart` arms hooks (`arm_hooks.py`); it does not re-argue them | `sides: both` |
| A-21 | `README.md` — Best Practices / Known Issues | Start each chained stage in a **fresh session** (`:157`); the **"orchestrator went quiet after a long phase"** failure mode, documented by the vendor (`:173`) | `:157`, `:173` | fresh session — `protocols/PLAYBOOK.md`, a new session boots from the handoff bundle and "continue what we were doing" is a named anti-pattern; quiet-orchestrator — **we had no such habit and paid for it**: leg M ran 2 h 06 m unbounded (second-pass §4 D6). Second-pass CANDIDATE C-5 | `sides: both` |

### 2c · The `Architekt-Jutra/architekt-jutra-code` worked example — @ `0a4a90d3f2c7cca53ddb40f84ac9de1f58d4e7e5`

1,044 files — the repo Maister itself produced.

| # | Corpus artifact | What it carries | Corpus locator | Our side (read live) | sides |
|---|---|---|---|---|---|
| A-22 | `README.md` | The residue policy, stated deliberately: *"All workflow artifacts are committed in `.maister/tasks/` so you can review the full AI-assisted development process."* | `aj-code:README.md:24-34` | Same idea, **stronger boundary**: `docs/handoffs/` + `docs/audits/` + `JOURNAL.md` are template-generated, seal-checked at commit (`check-seal-identity`) and immutable once landed, so the deliberate record cannot blur into droppings | `sides: both` |
| A-23 | `CLAUDE.md` | *"Read @.maister/docs/INDEX.md before starting any task"* — read-back **by instruction, not by mechanism**; no script anywhere parses `.maister/tasks/**` | `aj-code:CLAUDE.md:3` | Our boot contract is byte-capped and test-gated, and the handoff bundle it points at is **probe-gated** — `verify_handoff_probes` FAILs when the repo contradicts a recorded answer. Instruction vs mechanism, again | `sides: both` |
| A-24 | `verification/reality-check.md` + `orchestrator-state.yml` | **The single most decisive pair in the corpus:** verdict `Deployment Decision: NO-GO` at `reality-check.md:5`, and `status: completed` at `orchestrator-state.yml:32` in the same task. The verdict flipped no machine-readable field | `verification/reality-check.md:5`; `orchestrator-state.yml:32` | The failure class our gates exist to prevent; `audit.py health` FAIL **blocks the commit**. This is the corpus's own proof of the enforcement asymmetry | `sides: both` |
| A-25 | `tools/kg-incidents/.gitignore` + `jobs/README.md` | A curated agent-run trajectory archive: eval runs gitignored **except** one deliberately un-ignored reference set, with the strip list written down; each trial keeps `agent/trajectory.json`, an LLM-judge `assessment_eval.json` **and** a mechanical `verifier/reward.txt` | `.gitignore:8,12-16`; `jobs/README.md:61-75` | `tests/fixtures/lived-workflow/*.jsonl` — four committed CC session transcripts, frozen by `deploy/lived_sandbox/cli.py` while `logs/LIVED-WORKFLOW.md` is gitignored. **Ours is the stronger mechanism** — their strip list is prose, ours *refuses*: `_scrub_check`/`_SECRET_RE` will not freeze a transcript carrying a key. Genuine delta: they keep a **judged** score beside the mechanical one; we keep only the mechanical, deliberately | `sides: both` |
| A-26 | Undistinguished residue | 23 Playwright-MCP console logs and page snapshots landed inside a feature commit; `tools/kg-incidents/.claude/scheduled_tasks.lock` carrying a live `sessionId` and `pid`; an empty `.opik-tracing-enabled`. None gitignored, none documented | `…gap-analysis.md:220-224` | The boundary they lack. Our seal (`validate_hermetization`, ADR-101) polices the home of every added file at commit time | `sides: both` |

### 2d · Leg M's own run artifacts — shapes only; **the artifacts themselves are gone**

Produced by `/maister:init` + `/maister:development` during the second-pass arc, then **deleted at
teardown** (NC1). The second-pass audit is the only surviving description. This lane searched the
tree for all of them and found **nothing** — §4.1 ES-03. They are catalogued because the *shape* is
the transferable part, and marked `empty-search` because the artifact is not re-openable.

| # | Artifact shape | What it demonstrated | Our side (read live) | sides |
|---|---|---|---|---|
| A-27 | `.maister/docs/standards/global/*.md` (7 files) + `.maister/docs/INDEX.md` | `/maister:init` derived a 7-file standards tree + 3 project-context files from the codebase, **unprompted** | `protocols/PLAYBOOK.md` + `.claude/rules/` are authored and ratified, not derived; `silent_rule_detector.py` mines the corpus for un-mechanised normative language | `sides: empty-search` |
| A-28 | `analysis/clarifications.md`, `scope-clarifications.md`, `technical-clarifications.md` | Three clarification files, and **5 decisions recorded as *"resolved by assumption, not consent"*** | `SUPPLEMENT.md` (7-question schema, written unconditionally), folded into the next boot by `scripts/assemble_paste.py`; `/handoff-verify` **FAILs** on an answer the repo contradicts. Theirs records answers; ours fails when the repo disagrees with one | `sides: empty-search` |
| A-29 | `implementation/implementation-plan.md` | Computed `Task Groups: 1`, declared `Files to Modify:`, stated *"Single group — nothing runs in parallel"* | `scripts/boot_frontier.py` — the same invariant over a different unit (serialize-groups, not files) | `sides: empty-search` |
| A-30 | `orchestrator-state.yml` (the leg-M instance) | 14 phases, `completed_phases`, `failed_phases`, `reverify_count`; resumable **mid-phase**; `task_characteristics` demonstrably gated execution (`phase-4-skipped` because `ui_heavy: false`) | Lane contract + `git log`. **The honest asymmetry the second-pass arc recorded against itself:** leg M's state file is a far richer resumption surface, and nothing in our lane shape is equivalent | `sides: empty-search` |
| A-31 | `dashboard.html` + `dashboard-data.js` | Rewritten per phase; the run auto-opened a browser. Answers *"where is this task right now"* | `scripts/gen_trend_dashboard.py` answers *"what is the state of the fleet"* — a different question. Second-pass CANDIDATE C-3, and the one that arc most directly earned | `sides: empty-search` |
| A-32 | `verification/reality-check.md` (leg-M instance) | Re-ran the parser itself on 18 claims and 43 refusals written **independently**, and did not trust the prior report. Its `MEDIUM-1` finding was real — terra found the same class | `ecosystem/routing-table.yaml` reviewer + adversarial roles; neither re-executes. CANDIDATE C-4 | `sides: empty-search` |
| A-33 | `spec.html`, `implementation-plan.html`, `implementation-verification.html` | HTML companions emitted beside each markdown artifact | `ecosystem/trends.html`, `ecosystem/conformance.html`, `scripts/codemap/mermaid_emit.py` — committed, self-contained, direction-verdict per panel | `sides: empty-search` |

---

## §3 · The MSc thesis — file-by-file

**Robert Dwornik, *"Architektura informatyczna modelu pracy dużej instalacji fotowoltaicznej"*,
promotor dr inż. Piotr Pałka.** Source tree
`C:\Users\1028120\Downloads\Praca_Dyplomowa_Magisterska\` — **operator disk, unreachable from this
substrate**.

**This section is a reuse, not a re-derivation.** `docs/audits/2026-08-29-technical-thesis-compare-out.md`
read the TeX tree directly and recorded a per-file treatment table (`:13-24`), a derived
five-step method, ten verdict rows and four ranked gaps — all with two-sided locators. Re-deriving
it from a substrate that cannot open the source would produce a weaker copy. What follows is that
arc's file inventory, with **our side re-read live at this HEAD** and the funnel state advanced
where it has moved since 2026-08-29.

| # | Thesis file | Size / treatment there | What it carries | Our side (read live) | sides |
|---|---|---|---|---|---|
| T-01 | `main.tex` (abstracts PL + EN) | read in full | *"wzorce i metody decyzyjne"* — decision patterns and methods, the framing (`main.tex:52`) | **No ADR cites the thesis.** Verified negatives re-run by that arc: `magisterska` 0 · `dyplomowa` 0 · `Politechnik` 0 · `Pałka` 0 | `sides: both` |
| T-02 | `tex/2-cel-zakres-pracy.tex` | read in full | **Simulating questionnaire answers** to reach the recommended decision; the method is *"inspirowana pracą mgr inż. Daniela Stankiewicza"* — the third party is in the method's **genesis**, not only its validation | Absent — see T-07. The nearest live intent is `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md` §A.2, *"decide, record, and mark revertable"*, with the **shape of the mark undefined** | `sides: both` |
| T-03 | `tex/3-ogólny-wstęp-do-fotowoltaiki.tex` | **not read** — domain | Photovoltaic domain introduction | Out of scope by contract; **no claim is made about it here** | `sides: empty-search` |
| T-04 | `tex/4-wprowadzenie-do-wzorców-metod.tex` (23 KB) | read in full | *"**Architekt musi zawsze uzasadniać swoje decyzje architektoniczne**"* (`:15`) — *always*. Practised: ADD vs ATAM vs 4+1 compared with explicit Zalety/Wady, then the 4+1 choice justified in its own subsection (`:195`) | **partial, measured:** 57 of 88 ADRs (65 %) carry an alternatives-family heading; `templates/ADR-template.md`'s last line reads `<Optional. What else was evaluated…>`. *Zawsze* vs `Optional` — 65 % is what the word buys | `sides: both` |
| T-05 | `tex/5-projektowanie-architektury-krok-po-kroku.tex` (38 KB) | read in full | The **six-part scenario anatomy** (`:200`): bodziec · źródło bodźca · odpowiedź · **miara odpowiedzi** · plus the two flagged *"important though often omitted"* — środowisko and artefakt. And the response-measure's purpose (`~:204`): so the scenario can be **tested** | **partial:** `templates/intake-template.md:27` `## Scenarios (+1 view)` asks for prose; `:41` `## Acceptance criteria (ex-ante)` **is** the response-measure under another name, one section away and unlinked to the scenario it should measure. The full anatomy fired **once**, as a review lens, at `…fable-architecture-review.md:46` | `sides: both` |
| T-06 | `tex/5-5-autorska-metoda.tex` (4.4 KB) | **read in full, twice** | The author's own method as **five steps** — scenarios → tactics per QA → **closed** questionnaires → pattern tradeoff analysis → the decision, which *"must account for the impact on the system as a whole"*. Then it **critiques itself**: `Zalety` and `Wady` (czasochłonność · required expertise · **bounded by the information actually gathered**) | closed questions — `protocols/HANDOFF_PROCESS.md:204-216`, the four-part probe contract whose fourth clause is **bounded-deterministic**: *"a probe whose honest answer requires unbounded judgment over an open set is an arc, not a probe, and is rejected."* Ratified independently, for the same stated reason. Self-critique — `CLAUDE.md` §9's **"Honest limit"** convention, per organ, in the module's own words: **stricter than the thesis**, which critiques its method once | `sides: both` |
| T-07 | `tex/6-tworzenie-architektury.tex` (185 KB) | **SKIMMED** — 80 headings read, four regions read in full | The worked instrument: a nine-question closed TAK/NIE questionnaire yields *"Load Balancer jest najlepszym rozwiązaniem"* (`:1206`) — then, at `:1243`, **`Przykład dla innego zestawu odpowiedź`**, the same nine re-answered all-NIE and the recommendation **flips** to redundant-server/cloud. A **sensitivity analysis on a decision** | **absent — and this is the corpus's single most transferable move.** No ADR, template or protocol asks what would reverse a decision. It is live open row **`[#616]`** (`tasks/616-flip-condition-every-adr-records-what-evidence-w.md:12`), whose own text sources it: *"Provenance is the operator's MSc thesis principle 5, sensitivity analysis — a decision that cannot name its own flip has not been sensitivity-tested."* **This memo's §0.3 carries a flip-condition for exactly that reason** | `sides: both` |
| T-08 | `tex/7-przedstawienie-wyników.tex` | read in full (small) | Presentation of results | No comparison drawn by the source arc; **none invented here** | `sides: empty-search` |
| T-09 | `tex/8-wnioski-wynikające-z-pracy.tex` (14 KB) | read in full, incl. the commented-out draft | **Conclusion 1** — *"jaki jest nasz cel, co chcemy osiągnąć?"*, continuous re-evaluation saves time. **Conclusion 2** — change is inevitable; machine-legible documentation makes it manageable. **The Stankiewicz passage lives here**, not in `Wywiad.tex` | C1 — **DISCHARGED**: `…fable-architecture-review.md:48` verdicts it *"structurally embodied"* via Done-when, ADR-81's ex-ante frozen contract, PLAYBOOK Ch12.1 — *"better operationalized than the thesis itself managed"*, with the drift mode named (*when the gate becomes the goal*). C2 — **DISCHARGED (partial)** at `:50`: *"delivered on detection, half-delivered on removal"* | `sides: both` |
| T-10 | `tex/Wywiad.tex` (3 KB) | read in full | The **transcript**: six Q/A exchanges between "Architekt Systemu (RD)" and "Specjalista ds. Energetyki (DS)" — all domain questions (PV sizing, meteorological data, economic output). **Not one is a software question** | **DISCHARGED as heterogeneous-provider** (`…fable-architecture-review.md:52`; live at `protocols/PLAYBOOK.md:5143/:5144/:5146`, `:4058`, `:5163`). The standing delta, ranked last by its own arc and **recommended as a question, not a build**: every institutionalised second reader here is software-shaped — heterogeneous *provider*, homogeneous *frame* | `sides: both` |
| T-11 | `tex/B-Energy.tex` … `tex/F-Usability.tex` (5 appendices) | **not read as prose** — structure only | Per-attribute decision tables — and they are **commented out** in the source (`C-Modify.tex:141`, `D-Safety.tex:90`, `E-Testability.tex:105`, `F-Usability.tex:102`, `B-Energy.tex:94`) | **No claim is made about their content**, by that arc or this one. Recorded so a successor does not mistake silence for absence | `sides: empty-search` |
| T-12 | `bibliografia.bib`, `img/`, `eiti/` | **not read** — apparatus | Bibliography, figures, template apparatus | Out of scope; no claim | `sides: empty-search` |

**Two corrections that arc recorded and this lane carries forward**, because a successor grepping
for them will otherwise repeat the mistake: `Stankiewicz` is **not** a zero in this repo (one hit,
`…fable-architecture-review.md:52`), and the confrontation claim is in **ch.8**, not `Wywiad.tex`.

**One defect that arc reported and did not fix — still live at this HEAD, re-verified here:**
`protocols/AI_COUNCIL_PROCESS.md` cites `ai-council/docs/council-question-guide.md` at `:20`, `:99`
and `:399`; the file resolves at `ai-council/protocols/COUNCIL_QUESTION_GUIDE.md`. A live,
freshness-stamped protocol points three times at a moved authoritative source. **Reported, not
fixed** — this lane writes nothing outside this file.

---

## §4 · Recorded searches, lanes not run, deviations, and the before → after line

### 4.1 · Recorded empty searches

Every absence claim above rests on one of these, run in **both** lexicons per §1. Each is
reproducible.

| id | Search | Result | What it licenses |
|---|---|---|---|
| ES-01 | `multiplayer`, `shared (agent )?session`, `\bADE\b` | 0 (one `ADE` hit, a false positive on "façade") | A-06's multiplayer half — absent, and **n/a by design**: single-operator system |
| ES-02 | `greenfield` across tracked files | 42 files, **none stating the inversion** | A-08 — mechanism present, doctrine absent |
| ES-03 | `find` for `FR1-*`, `FR2-*`, `SEEDED-TASK.txt`, `DEVIATIONS.md`, `TEARDOWN.md`, `NC2-hub-plugin-list-*.txt`, `logs/TELEMETRY.db` | **0 — every one absent from the tree** | §2d's `empty-search` tokens, and §4.3's UNVERIFIED stamp on 6.4×/16.2× |
| ES-04 | `aj-scratch`, `INVENTORY.md` under any path | 0 | The contract's named input is unreachable; §2 is built from surviving locators instead |
| ES-05 | `docs/audits/2026-09-06-technical-batch-t-manifest.md` | **absent** | The batch-T manifest naming this lane is not on `main` at this HEAD — recorded, not worked around |
| ES-06 | `dos and don.?ts`, `derive.*(rule\|convention\|standard)`, `mined\|mining`, `post.?mortem\|retrospectiv` | nothing deriving a standards list from **review history** | A-04's genuine absence — we mine the corpus and the commit history, not what reviewers objected to |
| ES-07 | AI-friendliness / cross-release-stability as a dependency criterion, in `pyproject.toml`, `docs/decisions/` | 0 | A-05 — `ADR-106` declares dependencies, `ADR-112` sets the adoption bar; neither asks either question |
| ES-08 | `magisterska`, `dyplomowa`, `praca`, `diploma`, `dissertation`, `Politechnik`, `Pałka` (re-run by the source arc, `--include='*.md'`) | 0 files each | T-01 — **no ADR cites the thesis**, though three audits and one open row consume it |

### 4.2 · Lanes the contract named that could NOT be run — reported as NO REVIEW, never as clean (C-7)

Verified by `command -v` in this container:

```
uv       PRESENT  0.8.17   -- but pyproject.toml:25 requires ==0.11.19
codex    ABSENT
gemini   ABSENT
sol      ABSENT   (already a known defect: routing-table adversarial role -> uninstalled CLI)
```

- **Fan-out (Gemini, reader-only) — NOT RUN.** `gemini` is not on PATH in this substrate. The
  contract's fan-out leg therefore produced nothing. **Fabrications: not measurable — no fan-out
  ran.** This is reported as an absent lane, not as a clean one, and the count is *not* rendered as
  "0 fabrications measured", which would imply a leg that ran and behaved.
  The governing ruling (`to-cc\DECLARE-AGY-ROWS.md`) is **unreachable from this substrate**; the
  contract's own statement — Gemini is READER ONLY and never classifies against a doctrine clause —
  was applied as the operative constraint, and the trap in `ARCHITECT-INBOX-2026-09-05-021.md`
  §021-D was avoided by not running the leg at all.
- **Adversarial (codex on §0) — NOT RUN.** `codex` is not on PATH. §0 therefore carries **no
  adversarial pass**, and its derivation is single-author. That is the honest severity tally for
  this artifact: **no review of any kind was obtained.** A HIGH from a later adversarial read on §0
  should be expected rather than treated as a surprise.

### 4.3 · The 6.4× / 16.2× headline — cited as UNVERIFIED, and independently re-confirmed as such

The contract directs that lane-s's live-comparison result be read first and its headline cited **as
unverified**. It was, and this lane did not take that on trust:

- **The claim:** *"6.4× the wall-clock and 16.2× the cost, for the same verdict on the same task"*
  — `docs/audits/2026-09-05-technical-research-aj-second-pass.md:107`. Leg M $48.53 / 7809 s; leg D
  $3.00 / 1225 s.
- **Independently re-measured here (ES-03):** **not one** of that arc's evidence files is in the
  commit tree. The integrator's HIGH is corroborated, not repeated —
  `docs/handoffs/2026-09-06-dev-knowledge-architect/CENSUS.md:620` and
  `HAND_CARRIED.md:402` record the same finding, and the surviving evidence sits outside the repo
  at `Downloads\aj-scratch\second-pass-evidence\` (64 files), checkable only by a seat with disk
  access.
- **Consequence for §0:** the headline is **not load-bearing anywhere in this memo.** §0 rests on
  `ecosystem/deployed-versions.yaml`, `deploy/manifest-v1.5.0.yaml`, ADR-92/93, `ARCHITECTURE.md`
  and fleet-readiness §0 — all in-tree and all opened in this session. Whether an erratum is owed on
  that audit is the architect's call, not this lane's.

### 4.4 · Deviations — all stated, none silent

- **D1 — the dispatcher's pinned filename is refused by a live gate; the repo won.** The pin named
  `docs/audits/2026-09-06-research-aj-thesis-catalogue-and-deployment-model.md`. **`research` is not
  in `AUDIT_CLASS_ENUM`** (`scripts/validate_hermetization.py:149-158`). Verified by *running*
  `rule_b_violation()` against both candidates, not by reading the enum: the pinned name returns
  *"has no CLOSED-enum `<class>` token after the date"*; `…-technical-research-…` returns clean on
  Rules B **and** C. Resolved on the precedent both prior AJ audits already set (class `technical`,
  `research` moved into the slug) — the dispatcher's `-research-` token is preserved, one segment
  later. This is a C-3 class (b) rule-vs-ruling conflict; per `CLAUDE.md`, on conflict with a
  core-invariant gate **the repo wins**, and per C-2 it is decided and reported rather than waited on.
- **D2 — plan-mode for §0 was not entered.** §3.5 sets MODE plan-mode for §0. A background cloud
  lane has no answer channel: `ExitPlanMode` requires an approval that cannot arrive, and the
  contract forbids ending the turn waiting (C-2, and the 2026-09-01 lane that wedged 46 minutes).
  The §0 derivation was performed in-session with every premise verified against a live read, and
  the deviation is recorded rather than concealed.
- **D3 — gates were run as `python3`, by the dispatcher's own instruction, and the suite did NOT
  run.** The container carries `uv 0.8.17` against `pyproject.toml:25`'s
  `required-version = "==0.11.19"`; `uv run --locked` refuses outright — *"Required uv version
  `==0.11.19` does not match the running version `0.8.17`"* — and there is no `.venv` and no
  `pytest` importable from the bare interpreter. Declared, per the pin.

  **What DID run, and passed**, being the two gates that actually bear on a `docs/audits/` ADD:
  `validate_hermetization.rule_b_violation()` and `rule_c_violation()` against this file's path
  (both `OK`), and the `audit-title-gate` condition (a `# ` heading on line 1, present).

  **Batch-wide consequence, measured at this lane's Stop and reported for the close packet:** the
  same mismatch breaks the `Stop` hook, which invokes
  `uv run --locked python scripts/session_end_backpressure.py` and dies on the version check before
  reaching the script. **Every cloud lane in this batch will hit it**, so a lane reporting no
  session-end backpressure signal is reporting a container defect, not a clean gate. Run directly
  as `python3 scripts/session_end_backpressure.py` with a Stop payload on stdin, the check exits
  **0 with no findings** at this HEAD — so the signal itself is clean and only its carrier is
  broken. The hook is advisory in full (ADR-85 amendment §A5) and discharges no gate either way.

  **What did NOT run:** `pytest`, in any form. **This lane makes no green-suite claim.** The
  container was deliberately **not repaired** to manufacture one — a `uv self update` or a `pip
  install pytest` is a network fetch outside the decision budget, and a lane that repairs its own
  container destroys the receipt it exists to produce. The full suite runs once at integration
  (`[#528]`), in the integrator's substrate, which is the correct home for it.
- **D4 — `docs/audits/README.md` was NOT regenerated**, per the dispatcher pin and the `[#590]`
  narrowing. Three other batch-T lanes land audits; the integrator regenerates once on the merged
  result. This file is therefore **deliberately** absent from that index until integration.
- **D5 — no peer was reachable.** `ListAgents` returned no other session: `integrator`,
  `dispatcher-T`, `filings-N` and every sibling batch-T lane are missing addressees. HANDBACK is
  carried in this artifact and in the lane receipt instead of by message.
- **D6 — the browser channel is unreachable** (`to-cc\` / `to-browser\` live on the operator's
  disk). Per C-0 and the contract's substrate note, QUESTION and SESSION content is carried **in
  this artifact** and in the receipt; the dispatcher folds it into the batch close packet.

### 4.5 · The three questions this lane would have filed as QUESTION files

Recorded here because the browser channel is unreachable (D6). None blocked the work.

1. **The `intake-id: 70` double allocation** — `docs/intake/2026-09-05-tech-aj-second-pass.md` and
   `docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md` both claim it. This lane cited by
   **path** throughout, per the dispatcher pin. The namespace collision itself is unresolved and is
   already filed for the dawn list.
2. **Is an erratum owed on the second-pass audit** for a headline whose evidence left the tree at
   teardown? §4.3 states the fact; the ruling is the architect's.
3. **`deploy/tool.py` resolves the consumer as `hub_root.parent / repo` with no override**
   (`ecosystem/deployed-versions.yaml:83-92`), which is why win-tooling's v1.4.0 deploy was driven
   by a lane against a worktree rather than by `--execute`. That is the one measured obstacle
   between §0's model and corp-monorepo. **Reported, not fixed** — this lane owns no code.

### 4.6 · Before → after

The **before** half was re-measured in this session, not copied from the contract: the deliverable
path did not exist at lane start (`ls` → *No such file or directory*), and no in-tree artifact is a
file-by-file catalogue of the corpus — the first-pass audit is a **capability** gap table, the
second-pass a **decision** table, and THESIS-COMPARE covers the thesis only.

```
                         before   after
catalogue rows                0      45
two-sided locators            0      31
empty searches recorded       0      22   (14 row-level + 8 in the ES table)
fabrications                  0       0   -- no fan-out ran (4.2); not a measured zero
```

Counts are computed from this file, not typed into it. The four commands below reproduce the
`after` column exactly; the fourth must return **nothing**, which is what "no row is unmarked"
means (`F` = this file):

```
grep -cE '^\| (A|T)-[0-9]+ \|' "$F"                                  # catalogue rows
grep -E  '^\| (A|T)-[0-9]+ \|' "$F" | grep -c 'sides: both'          # two-sided locators
grep -E  '^\| (A|T)-[0-9]+ \|' "$F" | grep -c 'sides: empty-search'  # row-level empty searches
grep -cE '^\| ES-[0-9]+ \|'    "$F"                                  # ES-table empty searches
grep -E  '^\| (A|T)-[0-9]+ \|' "$F" | grep -v 'sides: '              # MUST be empty
```

A bare `grep -c 'sides: both'` over the whole file returns **33**, not 31 — it also matches this
section's own command block and the §2 legend. The row-anchored form above is the computing
surface; the bare form is the trap, recorded so a later reader does not "correct" 31 to 33.

### 4.7 · Closure, against the frozen bar

> *"every catalogue row has a locator on both sides or a recorded empty search; §0 states the model
> chosen and the first consumer it applies to."*

- **Every catalogue row** (A-01…A-33, T-01…T-12) carries either a two-sided locator or a
  `sides: empty-search` token whose search is recorded in §4.1. **No row is unmarked**, and the
  tokens are machine-countable by the commands in §4.6.
- **§0 states the model chosen** — push for pinnable/waivable components, pull for
  fleet-uniform ones, both as manifest components with both-sides drift checks (§0.3) — and it
  states the **first consumer**: **corp-monorepo** (§0.5), on three measured grounds.
- **The second question is answered by citation, not derivation:** each consumer runs its own CC
  sessions; the hub deploys and does not drive (ADR-92 Decision 3 — write-yes / commit-no /
  autonomy-no).

**Honest limits.** §0 carries **no adversarial pass** (§4.2) and its author is its only reader.
The corpus side of §2 is **second-hand throughout** — no file of the 48 was opened by this lane —
and §2d's seven rows describe artifacts that no longer exist anywhere. §3 is a **reuse** of an
arc that did open the source. What this document adds is the assembly, the live re-read of our
side, the recorded searches, and a §0 derivation that rests only on in-tree evidence.

**Funnel posture (ADR-111).** Zero rows born. Zero `tasks/` files touched. Zero deletions. Zero
retirements. Nothing here is self-ratifying: §0 is a **memo for the architect to rule**, and the
three items in §4.5 are questions, not candidates.
