# REVIEW — 2026-09-09 night mission, AJ M03 + Maister vs our harness

**Phase 3.** This is the first file to read in the bundle. It is built from three inputs only —
`MATRIX.md` (Phase 2), `R2-VERIFICATION.md`, `NIGHT-LOG.md` — and cites no locator those three do
not already carry, with **two named exceptions** declared inline in §1 (rows 1 and 2), where one
locator that `MATRIX.md` cites was followed one hop to the file it names. Both hops are stated
where they occur.

**Carried forward without laundering:** `†` = the supporting locator is UNVERIFIED (reader-reported,
never independently re-checked). `‡` = witnessed first-hand by the session. A `†` in `MATRIX.md`
is still a `†` here. §3 is the reason that matters.

**Constraint honoured throughout: NO NEW ORGANS.** No row below proposes a script, hook, command or
skill that does not exist. Where the honest shape of a gap is "something new", the row names the
**existing** organ that should absorb it.

---

## 1. The ten things that are missing, ranked by what unblocks STAGE 10 soonest

> **These are ROW CANDIDATES ONLY — a list for the operator to rule on.** This mission is
> **forbidden from editing `BACKLOG.md` or `tasks/`** and has edited neither. Nothing below has
> been filed. Two of the ten (rows 3 and 10) are scope notes on rows that already exist.

**Stage 10** is named at `tasks/670-step-g-floor-v1-5-0-reaches-corp-monorepo-and-th.md:13` —
*"Stage 10 of the universalization order ships the v1.5.0 floor to `corp-monorepo`"* (`MATRIX.md` §0).
The ranking rule is what most directly unblocks **that ship**, soonest. Rows 8–10 are important and
do **not** touch the ship; each says so in one clause.

---

### 1 — The `[#644]` deploy-freeze ruling has never been put to the operator, and the document measuring that is not in this tree

**Missing:** the lift-or-keep ruling on the 2026-08-29 deploy freeze — the single named blocker on
Stage 10 — and any in-repo carrier for it.

**Mechanism it comes from:** `MATRIX.md` §0 — *"our decisions do not have a state carrier… a
conclusion that governs work lives in a Google-Drive transport directory, is cited by committed
audits as authority, and cannot be read by anyone working in the repository."* Maister's answer to
exactly this is `orchestrator-state.yml`; ours is a filename in a citation.

**Locator hop declared:** `MATRIX.md` §0 cites `tasks/670-…:13`. That line names its blocker
`[#644]` and attributes the measurement to `DECLARE-REVIEWS § B R-2` — *"never put to the operator,
measured as unasked for ten days"*. **`DECLARE-REVIEWS` does not exist under `docs/`, `protocols/`,
`tasks/` or `deploy/`** — the same absence `MATRIX.md` §0 recorded for `DECLARE-HARNESS-IS-PROCESS`.
The blocker file itself is real: `tasks/644-the-2026-08-29-deploy-freeze-has-never-been-ruled.md`.

**Row candidate (ADR-87 shape)**
- **intent** — put the 2026-08-29 deploy freeze to the operator and land the ruling where the repo can read it
- **closure number** — *ship-blocking decisions with no in-repo carrier: 1 → 0*; second counter, *days the question has gone unasked: 10 → 0*
- **anti-pattern** — the only step of the recovery plan that reaches the operator's working day is blocked by a question nobody has asked, and the surface that counts the days is unreadable from the tree
- **pointer** — `tasks/644-the-2026-08-29-deploy-freeze-has-never-been-ruled.md`, ruling landed as an ADR in `docs/decisions/`

---

### 2 — The v1.5.0 floor ships `/override`, a command whose own frontmatter says it discharges no gate

**Missing:** reconciliation between what the manifest says `/override` does and what the file it
ships says about itself — before that file reaches `corp-monorepo`.

**Mechanism it comes from:** `MATRIX.md` §5.1 DELETE LIST, verb **delete**:
`.claude/commands/override.md:1` — *"RETIRED (ADR-85 amendment 2026-08-03 §A2) — discharges no
gate"*. `MATRIX.md`'s words: *"A command that announces it does nothing."*

**Locator hop declared:** `MATRIX.md` marks it for deletion but does not connect it to the ship. It
is connected: `deploy/manifest-v1.5.0.yaml` carries an `override-command` component
(`:995-1004`, `waivable: true`) and at `:296-297` describes it as *"seb's only escape"* —
re-included past the floor's `.claude/*` exclusion on purpose (`:299`, `:307-308`).

**This is the one row where the mission's DELETE LIST and the mission's ship collide.** Stage 10
would deliver, to the operator's own working repo, a documented escape hatch that is inert. It is
either a delete (manifest node and payload both) or an un-retirement — it cannot stay as it is.
Deciding is cheap; discovering it in `corp-monorepo` is not.

**Row candidate**
- **intent** — make the v1.5.0 payload agree with the v1.5.0 manifest on whether `/override` does anything
- **closure number** — *shipped components whose payload contradicts their manifest description: 1 → 0*
- **anti-pattern** — a consumer reads the manifest, believes it has a session-end escape, invokes it, and gets nothing; the manifest's own note already flags the coupling hazard (`:999`)
- **pointer** — the `override-command` node in `deploy/manifest-v1.5.0.yaml`, checked by `deploy/release_lint.py`, which `[#670]`'s Done-when already requires to pass on the consumer

---

### 3 — MA-1: the deployed `PreToolUse` guard turns a missing environment variable into total refusal for any reader that is not Claude Code

**Missing:** a guard that resolves its own path, and that fails **open** when its interpreter cannot
start.

**Mechanism it comes from:** `MATRIX.md` §4 finding **MA-1** ‡ and §5.1 (verb **wire**), measured
rather than read. `.claude/settings.json:21` declares a `PreToolUse` hook, matcher `"*"`, command
`python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`. `cursor-agent` honours the
hook file and does not define the variable; it expands empty, the path becomes
`C:\scripts\fleet_health.py`, the interpreter exits non-zero, and matcher `"*"` converts that into
refusal of **every** tool call with no in-session escape (`NIGHT-LOG.md`, *"Leg 1e, in full"*).
Two full `cursor-agent` runs were spent proving it ‡.

**Why it ranks here against the ship:** `corp-monorepo` is where the operator's real day happens.
`MATRIX.md` §4 is blunt about the shape of this failure — *"our own guard converts into a total
refusal for the new reader, and presents as the reader being broken"*. `codex` escaped only because
it does not read `.claude/settings.json`. That is luck, and luck does not survive a deploy.

**Row candidate**
- **intent** — the prompts-guard resolves its own path and fails open on interpreter failure
- **closure number** — *tool calls refused because the guard's own command could not start: every call in the session → 0*
- **anti-pattern** — a safety hook that cannot run refuses everything instead of nothing, and the refusal is attributed to the tool it blocked
- **pointer** — `.claude/settings.json:21` and `scripts/fleet_health.py --prompts-guard`; both exist. This is also a scope note on `[#676]`, which was filed about exactly this class of collapse

---

### 4 — The 16-stage universalization order has no in-repo enumeration

**Missing:** the order itself. Stage 10 is named in exactly one line of one task file.

**Mechanism it comes from:** `MATRIX.md` §0, R4 target 4 — *"source absent as an enumeration…
`docs/audits/2026-09-09-technical-lane-v-664-delivery-spine.md` is **not** the loop map — it
contains no numbered 16-stage list and never says 'stage 10/12/15'."* The fullest in-repo
description is a single ratio: `docs/intake/2026-09-09-tech-recovery-plan.md:24` — *"8 of 16 loop
stages mechanical"*.

**Consequence this bundle already paid for:** `MATRIX.md` §3.2 had to caveat its entire
stage-12/stage-15 analysis, because *"'Stage 12 = eval' and 'stage 15 = nightly' are taken from the
mission prompt's own gloss"* and must be re-matched when the real map lands. A ship named by its
stage number, in an order that exists nowhere, cannot be sequenced against anything.

**Row candidate**
- **intent** — land the 16-stage order as an enumeration in the intake document that already carries its ratio
- **closure number** — *stages of the 16 with no in-repo definition: 15 → 0*
- **anti-pattern** — three separate analyses in this bundle reason about stages 10, 12 and 15 from a gloss in a prompt, because the map they name is not a document
- **pointer** — `docs/intake/2026-09-09-tech-recovery-plan.md` (existing; §4 already carries steps A–G, which is the same content at a different granularity)

---

### 5 — `tasks/` frontmatter records no execution position

**Missing:** `phase`, `attempts`, `skipped_gates`, `risk` — the four keys `MATRIX.md` §2 calls
*"the single highest-value change this mission found in the spine"*.

**Mechanism it comes from:** Maister's per-task state carrier. `MATRIX.md` §1c and §2 items 1–4:
theirs records `completed_phases`, `failed_phases`, `auto_fix_attempts`,
`options.skip_test_suite`, `task_context.{risk_level, architecture_decision}` — with **10 committed
instances verified first-hand in repo B ‡**. Ours, verified independently by R2
(`R2-VERIFICATION.md` §2, union of keys across three real task files), is
`id, title, status, priority, size, theme, story, serialize-group, depends-on, generates` —
**none of those four.**

**Stage-10 tie:** `[#670]`'s Done-when is a two-part deploy — *dry run first, then live*. In our
carrier that whole arc is `status: open` until it is `status: closed`. A dry run that went green and
then stopped is indistinguishable from a row that never started — which is the recorded gotcha
`MATRIX.md` §2 names, *"a gate-blocked lane looks identical to a finished one."*

**Row candidate**
- **intent** — task frontmatter expresses execution position, attempts, deliberately-skipped gates and risk
- **closure number** — *open rows whose partial execution cannot be recovered from the repository: all of them → 0*
- **anti-pattern** — we record a closure and never that it took three tries; every retry this mission made — three `agy` re-runs, two `codex`, three `cursor-agent` — would be invisible in our carrier (`MATRIX.md` §2.3)
- **pointer** — `tasks/*.md` frontmatter, schema-enforced by the existing `validate_backlog` pre-commit gate. **No new organ:** the schema gate already exists and already refuses malformed frontmatter; it gains four keys, not a new home

---

### 6 — The operator GO leaves no artifact

**Missing:** a written, committed GO/NO-GO at the loop's terminal gate.

**Mechanism it comes from:** `MATRIX.md` §1c, the GO/NO-GO row. Theirs:
`.maister/tasks/…/verification/reality-check.md:5-9` † — *"**Status**: NOT READY -- Critical gap in
Success Criterion #1 / **Deployment Decision: NO-GO**"*. Ours: *"our operator GO is spoken and
leaves no artifact — `PLAYBOOK.md:6068` is a spine row with no carrier."* The `:6068` locator is one
of the 8 of 8 CONFIRMED by R2 (`R2-VERIFICATION.md` §1).

**Stage-10 tie:** row 1 above is the same defect at the front of the loop — an unlanded decision
blocking a ship. This is it at the back — a GO on the ship that will leave nothing behind. If
`[#644]` is ruled KEPT, `[#670]` DEFERs on a named review date; that ruling has to be readable six
months later, and today's mechanism for making it readable is that someone remembers to write it
down.

**Row candidate**
- **intent** — the terminal GO/NO-GO becomes a committed line in the artifact the session already produces
- **closure number** — *spine rows with no carrier: 1 → 0*
- **anti-pattern** — the one gate that ends every arc produces nothing a later reader can check, in a repo whose entire enforcement thesis is that claims must be checkable
- **pointer** — the `docs/handoffs/*/` bundle, whose shape `HANDOFF_PROCESS.md` already owns. **No new organ:** the carrier exists and is produced every session; it gains a field

---

### 7 — Three more decisions that govern work and cannot be read from the tree

**Missing:** in-repo sources for `DECLARE-HARNESS-IS-PROCESS §5`, the conductor decision **E +
AMEND-001**, and the **five DEAD PLAYBOOK sections** — and a rule that stops the next one happening.

**Mechanism it comes from:** `MATRIX.md` §0, R4 targets 1–3. `Glob **/DECLARE-HARNESS-IS-PROCESS*` →
zero matches; three committed files cite it by its transport path
`to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`
(`docs/audits/2026-09-08-technical-process-trigger-census.md:4`,
`…lane-v-642-assembly-debt-rows.md:151`, `…lane-v-643-enforcement-debt.md:95`). No file names
conductor options A–D, states why E was chosen, or reproduces AMEND-001 — *"the only description of
E anywhere in the tree is the mission prompt's own clause"*, `MISSION-PROMPT.md:79`. The five dead
PLAYBOOK sections are **unnamed everywhere**; `protocols/PLAYBOOK.md` marks no section dead, and the
one "dead" hit at `:1835` is the unrelated phrase *"a fresh committing worktree is dead on arrival"*.

**Why it ranks below row 1 rather than beside it:** none of these three names Stage 10. Row 1 is the
same defect with the ship attached — which is precisely why one rule closes both.

**Row candidate**
- **intent** — a decision cited by a committed artifact as authority must exist in the repository before the citation is valid
- **closure number** — *R4 targets with no in-repo source: 4 → 0*
- **anti-pattern** — the process-trigger census cites `to-cc/…§4` as its own commission at line 4, and a reader of that census cannot check what commissioned it
- **pointer** — `docs/decisions/`, enforced by the rule that already exists and is simply not applied to architect decisions: `CLAUDE.md` §4, *"Resolve a locator before you act on it — a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a claim, not evidence."* **No new organ:** `/preflight` already performs exactly this check and is, by its own frontmatter, wired into no gate

---

### 8 — No telemetry has a consumer, and four modules that would be the consumer sit unwired

**Missing:** call sites. Not code — call sites.

**Mechanism it comes from:** `MATRIX.md` §3.1 and the four **wire** rows in §5.1:
`scripts/cost_usage_telemetry.py` — *"Library only; no call sites"*
(`…gap-analysis.md:28`), its only reference a lane contract (`…census.md:86-105`);
`scripts/gen_trend_dashboard.py`, same shape; `scripts/window_metrics.py` +
`scripts/failed_set.py`, where `failed_set` is called only by the untriggered `window_metrics`
(`scripts/window_metrics.py:359`). Meanwhile governance telemetry **does** run —
`DEV_KNOWLEDGE_TELEMETRY=1 audit.py health` wrote 42 `check_run` events with per-check
`duration_ms` — and *"**Nothing reads them**"* (`…aj-second-pass.md:26`). Our own trend surface says
so in its own words: *"gate time per runner invocation ABSENT", "suite wall-time ABSENT",
"**per-model change quality ABSENT**"* (`…aj-second-pass.md:27`).

**Ranks here because it does not touch the ship at all** — no part of deploying the v1.5.0 floor to
`corp-monorepo` waits on a telemetry consumer.

**Row candidate**
- **intent** — the four existing orphan modules get a caller; nothing is written
- **closure number** — *telemetry streams emitted and consumed by nothing: 2 → 0* (governance `check_run`, cost)
- **anti-pattern** — we pay to emit and never read; `MATRIX.md` §3.1's verdict is *"the loop is open at both ends"*
- **pointer** — `scripts/cost_usage_telemetry.py`, `scripts/gen_trend_dashboard.py`, `scripts/window_metrics.py`, `scripts/failed_set.py`. **Verb is wire, never delete:** `MATRIX.md` §5.1 is explicit that deleting `cost_usage_telemetry.py` *"would delete the one thing that already exists for stage 12"*

---

### 9 — Nothing measures the human gate, and no gate has ever been proven to refuse

**Missing:** approval-rate and review-duration measurement on the terminal GO, and a trip-test that
proves a gate can bite.

**Mechanism it comes from:** M03 L05.md:31 †, twice — *"Avoid the 'rubber-stamping' anti-pattern…
by monitoring approval rates and review durations"* and *"**Inject synthetic, flawed blind tests**
into human reviewer queues"*. `MATRIX.md` §3.2 calls the first *"the sharpest row in this table"* and
states our position without softening: *"We have **no measurement of that gate at all** — not how
long a review took, not how often GO is given, not whether any GO was ever withheld."* Both
locators are **UNVERIFIED †** (see §3).

**The second half is the direct answer to the leg this mission could not run.** `MATRIX.md` §3.2:
*"a gate that has never refused anything is indistinguishable from a gate that cannot refuse."*
That applies to the reviewer and to the pre-commit hook set — several of which, on tonight's
evidence, have never been observed to fire. Leg 1e was ordered to find cannot-fail tests and
returned nothing (§4); this is the mechanism that finds them without a reader.

**Does not touch the ship** — but it is what makes row 6's recorded GO worth recording.

**Row candidate**
- **intent** — measure the terminal gate, and trip-test the hooks that claim to refuse
- **closure number** — *gates with zero observed refusals: the pre-commit set (`MATRIX.md` §1c counts 22 ‡) → 0*
- **anti-pattern** — our whole advantage over Maister is that our gates refuse (`MATRIX.md` §2), and for most of them that is an untested assertion about ourselves
- **pointer** — `tests/`, using the hook-stage trip-test pattern the suite already uses, plus `scripts/window_metrics.py`, which already computes cadence numbers and is unwired (row 8). **No new organ:** both exist

---

### 10 — No alias layer: the physical model name is enforced at three call sites, and only one role has a fallback chain

**Missing:** logical model aliases — *"apps name `prod-model`, a config maps it to a physical model,
so provider swaps need no code change"* (L02.md:37 †).

**Mechanism it comes from:** `MATRIX.md` §4. We have the opposite:
`MODEL_ENUM = ("opus","sonnet","haiku")` enforced at `scripts/gen_lane_contract.py:129`,
`:332-335`, `:833-835` †, and the literal binary `claude` emitted at `:525` †. Our own registry is
honest about what it is: *"A swap still edits N files; what changes is that it can no longer edit
N-1 of them and ship"* — `scripts/check_provider_registry.py:13-16` †. `MATRIX.md`'s framing is the
useful part: **we already have a working alias layer for exactly one role.**
`~/.claude/ROUTING.md:48-79` † binds the REVIEWER to a cost-ascending fallback chain; nothing else
has one, *"and tonight two readers hit quota and no chain existed for them."* That makes this a
generalisation problem, not a design problem.

**Ranks last against the ship, and the clause is short:** nothing about deploying the v1.5.0 floor
to `corp-monorepo` depends on which model answers. It is on the list because two of tonight's five
ordered readers died with no chain, and because the alias layer is the one mechanism M03 names for
the nine-item change set 1f enumerates.

**Row candidate — this is a scope note on `[#582]`, not a new row**
- **intent** — generalise the working REVIEWER fallback chain to the architect role; `[#582]` is already the router row
- **closure number** — *files edited to swap the architect model: 9 (1f items 0–9 †) → 1*
- **anti-pattern** — every one of those nine items is a place a physical model name or a vendor binary leaked into a surface that should have named a role
- **pointer** — `ecosystem/routing-table.yaml:31-38` † (already declares `fan_out` as a **list** of CLIs), `~/.claude/ROUTING.md`, and `[#582]`

---

**On the bubble, and named so it is not lost:** the census population is contested by our own
measurement — **32 orphans vs lane v-664's 39, one day apart, unreconciled** (`MATRIX.md` §0.1). It
is not in the ten because it blocks no ship; it blocks the **delete list**, and `MATRIX.md` §5.2
refuses to act on it in exactly those terms: *"Deleting on a contested census is how a real caller
gets removed."* If the operator wants deletions, this reconciliation is the prerequisite, and
`file_purpose_graph.py` — wired by v-664 behind three commit-tier hooks ‡ — is the existing organ
that should own the count.

---

## 2. Which of our prior conclusions Phase 1 overturned

Four dispositions, and they are not interchangeable. **OVERTURNED** = the claim is false and the
evidence says so. **SUPERSEDED** = a later measurement of the same thing disagrees, and nothing has
adjudicated between them. **SPLIT** = the claim is true of one axis and false of another, and
stating it as a single verdict is what made it wrong. **UNCHECKABLE** = the source cannot be read
from this repository, so the claim is neither confirmed nor refuted. *We cannot check this* is not a
polite way of saying *this was wrong*, and it is not recorded as one below.

### SPLIT

| PRIOR CONCLUSION | WHAT PHASE 1 DID TO IT | LOCATOR |
|---|---|---|
| *"Maister offers nothing beyond a spine"* | **FALSE about content, TRUE about enforcement.** It carries conditional phase routing, verification-option selection, UI-mockup machinery with a reviewable gallery, and per-phase risk decisions — and enforces none of them. We carry far less shape and mechanically enforce what we carry. Stating it as one verdict is what made it wrong. | `R2-VERIFICATION.md` §2; `MATRIX.md` §2 verdict block. Phase locators **14 of 14 CONFIRMED** at `plugins/maister/skills/development/SKILL.md`, our 8-phase spine **8 of 8 CONFIRMED** at `protocols/PLAYBOOK.md:6064-6071` |
| Maister's `orchestrator-state.yml` is a state carrier we lack | **The shape exists; the writer does not.** R2's independent structural check: 33 mentions, **all `.md`**, plus one 21-line shell hook (`plugins/maister/hooks/post-compact-reminder.sh:12,15`) that emits a static reminder string and *"never opens, parses or writes the YAML"*. `find` for `*.py`/`*.js`/`*.ts` across both plugin trees returns **zero**. Yet repo B carries **10 committed `orchestrator-state.yml` instances, verified first-hand ‡**. So: written by a model that was asked to, never by code. | `R2-VERIFICATION.md` §2; `MATRIX.md` §1c rows 2–3 |

**Note the SPLIT above sits on an UNCHECKABLE base.** The original wording of *"nothing beyond a
spine"* lives in `DECLARE-HARNESS-IS-PROCESS §5`, which has no in-repo source (`MATRIX.md` §0). The
verdict is against the claim as the mission prompt restated it. That is the best available and it is
not the same as reading the original.

### OVERTURNED

| PRIOR CONCLUSION | WHAT OVERTURNS IT | LOCATOR |
|---|---|---|
| `scripts/file_purpose_graph.py` is census **orphan #10** | **It is not an orphan any more.** Lane v-664 wired FPG-1 behind three commit-tier hooks — **two of which refused this bundle's own commit tonight ‡**. Live proof, not a re-read. | `MATRIX.md` §5.2; census tag at `…census.md:109` (ADR-118 *Proposed, NOT ratified*) |
| *"REJECT (as framed)"* on per-loop model-call trace inspection — rejected partly because *"Maister does not have it either"* | **The premise is false: repo B ships it** — `litellm/config.yaml:12-24` **†**, Presidio PII guardrails (`CREDIT_CARD: BLOCK`) and Langfuse callbacks, described by `MATRIX.md` as *"the M03 lessons, running"*. The rejection's reasoning does not survive; whether the rejection itself should stand is a separate question, and the locator is **UNVERIFIED †** | `MATRIX.md` §1a (M01L02 row, `…aj-second-pass.md:26`) and §1c last row |
| `FR2-legM-01-init.json` is absent, *"its wrapper was OOM-killed, so no JSON was written… No dollar figure is estimated"* | **The file exists** and carries `total_cost_usd: 21.8585621`. The init figure was low by **3.76×**. The headline ratio is *"correct as scoped… incomplete"*. Its own honest status: *"verified by a seat with disk access — and **unreproducible from the repository**"* — so the correction is itself partly UNCHECKABLE | `docs/audits/2026-09-06-technical-erratum-aj-second-pass.md:45-48`, `:55-57`, `:160-162`, carried at `MATRIX.md` §1a |
| `ecosystem/provider-registry.yaml` records `grok` as **PAY-PER-CALL** — *"one small test cost **$0.037**, credential proven by a server round-trip"*, measured 2026-08-26 | Tonight's refusal names a **free tier with a usage limit** — *"free Grok Build usage limit"*, upsell to SuperGrok. **Those two cannot both describe the account in use tonight.** Either the credential changed, or the cost note describes the raw-HTTPS route rather than the CLI. **Not repaired** — this bundle writes no registry change | `NIGHT-LOG.md`, *"A registry correction falls out of this"* |
| Three of leg 1c's own citations | Not conclusions but **citations**, overturned by R2: `SKILL.md:559` is **WRONG** (the line is an intro sentence; the routing/option flags are at 561–608 and `completed_phases`/`failed_phases`/`auto_fix_attempts` are in a **different file**, `orchestrator-framework/references/orchestrator-patterns.md` ~218–236); `tasks/README.md:81` is **OFF-BY-2** (fields at 83–89), content accurate; the two `PLAYBOOK.md:6070`/`:6071` glosses are **NOT AT LINE** — *"Neither gloss is wrong about the repo. Both are wrong about where the repo says it"* | `R2-VERIFICATION.md` §1 |

### SUPERSEDED

| PRIOR CONCLUSION | WHAT SUPERSEDES IT | LOCATOR |
|---|---|---|
| The census's **32 ORPHAN** rows, of a 216-row population | **Lane v-664 re-measured the same class one day later and got 39** — a prediction of 26 against a measured 39. Nothing reconciled the two. This is **not** OVERTURNED: no third measurement exists, and leg 1d — ordered precisely to arbitrate — could not run. The honest state is *"two of our own measurements of the same population disagree (32 vs 39), the disagreement is one day old, and no third measurement exists"* | `MATRIX.md` §0.1; `…process-trigger-census.md:11-16` vs `…lane-v-664-delivery-spine.md:230-243` |
| The census's own two earlier passes | Superseded **by the census itself, before this mission**: a docstring-regex pass produced **133/139 false "triggered"**, and a bare-filename AST pass **collided 7 module names**. It also states *"Reachability is static… proves wiring, not execution"* and puts function granularity **out of scope** — a module can be TRIGGERED while a function inside it is orphaned | `…census.md:55-62`, `:438-445`, carried at `MATRIX.md` §0.1 |

### UNCHECKABLE

**Four of the five conclusions R4 named as attack targets have no source document in this git
repository.** They are cited, never landed. Phase 1 did **not** overturn them; Phase 1 established
that they cannot be reached.

| TARGET | STATUS | LOCATOR |
|---|---|---|
| `DECLARE-HARNESS-IS-PROCESS §5` | source absent; glob → zero matches; three committed files cite it by transport path | `MATRIX.md` §0 row 1 |
| conductor decision **E + AMEND-001** | source absent; no file names options A–D, states why E was chosen, or reproduces AMEND-001 | `MATRIX.md` §0 row 2, `MISSION-PROMPT.md:79` |
| the **five DEAD PLAYBOOK sections** | source absent **and the five are unnamed**; the one "dead" hit at `PLAYBOOK.md:1835` is an unrelated phrase | `MATRIX.md` §0 row 3 |
| the **16-stage delivery-loop map** | source absent as an enumeration; the fullest in-repo description is one ratio | `MATRIX.md` §0 row 4, `docs/intake/2026-09-09-tech-recovery-plan.md:24` |

Two further questions are UNCHECKABLE for a different reason — **the reader never ran** (§4): the
independent census diff (leg 1d) and the cannot-fail-test scan (leg 1e). `MATRIX.md` §5.2 refuses to
manufacture either: *"this mission has no evidence and will not manufacture it."*

**`MATRIX.md` §0 treats this as the mission's most important output, and this review agrees.** The
mission asked what our spine lacks. The answer arrived before any reader opened Maister: our
decisions have no state carrier. It is **upstream** of "we lack a runner" — *"A conductor that
executes phases still needs to know what was decided."* And it is upstream of the ship: §1 row 1 is
this same defect with Stage 10 attached.

---

## 3. What this mission could not verify — the R2 UNVERIFIED register

Numbers as recorded at `R2-VERIFICATION.md` §3. Nothing was dropped; everything below is carried in
its own file and marked UNVERIFIED there.

| READER | LEG | ROWS PRODUCED | R2-VERIFIED | UNVERIFIED | WHY NOT |
|---|---|---|---|---|---|
| `agy` | 1a L01 | 18 | 0 | **18** | budget went to 1c; locators are line numbers in a split transcript in a temp dir |
| `agy` | 1a L02 | ~30 | 0 | **~30** | as above |
| `agy` | 1a L03 | 32 | 0 | **32** | as above |
| `agy` | 1a L04 | 30 | 0 | **30** | as above |
| `agy` | 1a L05 | ~28 | 0 | **~28** | as above |
| `agy` | 1a L06 | ~35 | 0 | **~35** | as above |
| `agy` | 1b | 16 | 0 | **16** | source is a temp clone; locators are `path:line` into it |
| `codex` | 1c | 24 locators | **24** | **0** (3 defective, carried) | **fully verified** |
| `grok` | 1d | **0** | — | — | **LEG UNFULFILLED (R1)** — free-tier quota; no substitute run |
| `cursor-agent` | 1e | 0 at first two attempts | — | — | blocked by our own `PreToolUse` guard, then quota |
| Claude Sonnet | 1f | 31 | 0 | **31** | self-reported as opened-and-quoted; *"A Claude subagent verifying a Claude subagent is weak evidence"* |

**The ratio: 24 independently verified against ~220 UNVERIFIED carried into Phase 2.** That is
**roughly one locator in ten**, and the denominator is itself soft — four of the six 1a row counts
are approximations (`~30`, `~28`, `~35`) in the source table, so `~220` is an estimate of an
estimate.

**What that ratio means for how the rest of this bundle should be cited.** Three rules, and they are
not stylistic:

1. **Leg 1c is the only leg citable as evidence.** Its 24 locators were checked adversarially by a
   read-only verifier instructed *"do not be generous"*, and **three of twenty-four were defective**
   (§2). That failure rate on a leg that was checked is the argument for R2, and it is the rate you
   should assume applies to the ~220 that were not.
2. **No row from 1a, 1b or 1f may support a deletion, a ratification, or a spend.** `MATRIX.md`
   already honours this — every 1a and 1f row carries `†`, and §5.1's two `†`-only DELETE-LIST rows
   both carry the verb **wire**, not **delete**. Every unambiguous **delete** in that list rests on
   the census or on a file's own frontmatter, not on a reader.
3. **The `†` travels or the claim does not.** `MATRIX.md` §1b — the entire M03 practice table, which
   is where the mission's headline findings about aliases, evals, observability and rubber-stamping
   come from — is **UNVERIFIED end to end**. Those findings are worth acting on because they are
   *arguments*, not because they are *cited*. Anyone who strips the daggers converts an argument
   into a false citation.

The allocation was deliberate and this review does not fault it: *"The one leg whose conclusions the
mission most depends on — the spine comparison — is the one that was verified."* But
`R2-VERIFICATION.md` states the consequence itself, and it is the correct one: **"no reader's table
should be cited downstream as though it had been checked."**

---

## 4. Substitutions that occurred (R1) — for the operator's morning ruling

**The distinction the log draws, stated first because everything below depends on it.**
`NIGHT-LOG.md`'s legend defines three states:

- **ORDERED** — the reader the mission named.
- **CORRECTED** — *the same ordered reader*, invocation fixed after a recorded failure. This is the
  `[#676]` discipline: **a mis-invocation is not a dead tool.** A CORRECTED leg is **not a
  substitution** and needs no ruling; it needs recording, which it got.
- **SUBSTITUTED-PENDING-OPERATOR** — R1 applies.

**And the sharpest point in the whole register: both R1 legs are marked
`SUBSTITUTED-PENDING-OPERATOR`, and in neither case was anything substituted.** The label names the
disposition, not an act. `NIGHT-LOG.md` says so twice, identically: *"No other reader was run in its
place."* Read the label as **UNFULFILLED**.

### The two UNFULFILLED legs

**LEG 1d — `grok`, the independent census**

- **Ordered:** an independent re-census of the process-trigger population, to arbitrate the
  contested orphan count.
- **What happened:** two failures for two different reasons. First, `grok -p "<census prompt>"` — exit 0 after
  **two** assistant turns, 304 B of stdout, no table, no file. Cause, from `grok --help`:
  `-p, --single` is **single-turn by construction**; a census needs many tool turns, so the run was
  *structurally incapable* of finishing. From the outside it is indistinguishable from a dead
  provider — *"the exact collapse `[#676]` was filed about."* That was **CORRECTED**, on the ordered
  reader: `grok --always-approve --max-turns 80 --output-format plain -p "<census prompt>"`. The
  corrected invocation then ran 3 turns and hit: *"You've reached your free Grok Build usage limit
  for now."* **The corrected invocation was right; the account cannot pay for the work.**
- **What was done instead:** **no substitute reader was run.** The census-diff rows in `MATRIX.md`
  are built from lane v-664's **in-repo** re-measurement — *"our own dated artifact, not a substitute
  reader"* — and are labelled as such everywhere they appear.
- **THE RULING REQUIRED:** *Is an in-repo re-measurement an acceptable arbitrator of a disagreement
  it is one half of?* It is not independent: v-664's 39 is one of the two numbers in dispute
  (`MATRIX.md` §0.1). The operator must rule whether leg 1d is **re-run on a paid account** before
  any deletion is acted on, or whether the DELETE LIST stands permanently at its current length with
  the 26 remaining census orphans untouched.

**LEG 1e — `cursor-agent`, the cannot-fail-test scan**

- **Ordered:** a scan for tests that cannot fail.
- **What happened:** **three failures, three different causes** — and only the third is a provider
  problem. (1) Write blocked by our own `PreToolUse` guard (`python C:\scripts\fleet_health.py` →
  ENOENT). (2) Printing to stdout instead — still blocked: *"Every repo tool call (Read, Shell,
  Glob, Grep, Task) is blocked by a broken PreToolUse hook."* The reader then **refused to
  fabricate**: *"Without real locators I will not invent table rows."* `NIGHT-LOG.md` records that as
  correct behaviour and so does this review. (3) With `CLAUDE_PROJECT_DIR` exported — quota refusal,
  `ActionRequiredError: You've hit your usage limit`, exit 1.
- **What was done instead:** **nothing.** *"The 'cannot-fail test' scan the mission wanted from this
  leg is therefore ABSENT from the DELETE LIST, and the DELETE LIST says so in place of guessing."*
- **THE RULING REQUIRED — two questions, and the first is the expensive one:** *Do we fix
  `.claude/settings.json:21` before any non-Claude reader is ordered again?* Attempts 1 and 2 were
  **our fault, not the vendor's** — §1 row 3. Two paid runs were burned discovering a defect in our
  own configuration. Second: *is the cannot-fail-test question re-run on a paid reader, or reassigned
  to the synthetic-flawed-item mechanism in §1 row 9, which answers it without a reader at all?*

### CORRECTED, not substituted — recorded, and three still need a ruling

None of these is an R1 substitution. Three of them are findings anyway.

| LEG | ORDERED READER | WHAT WENT WRONG | THE CORRECTION | RULING NEEDED? |
|---|---|---|---|---|
| 1c | `codex` | Ran to completion, **85,017 tokens, exit 0**, then: *"BLOCKED: Repository policy restricts Codex to read-only review, so I cannot create the requested output file."* **Not a provider failure and not an auth failure — our own L0 doctrine** (`~/.codex/AGENTS.md`, the read-only reviewer role `AGENTS.md` "Precedence" names) forbids the write. 85k tokens of real derivation done and discarded | deliverable changed to *"PRINT your entire answer to stdout"* — stays inside the ordered reader **and** inside its L0 role. **DELIVERED**, 92,866 tokens | **YES.** Does the read-only reviewer role apply when `codex` is ordered as a **deriver** rather than a reviewer? *"The caller was never warned; the money was spent first."* |
| 1d (1st) | `grok` | `-p` single-turn by construction | `--max-turns 80` | no — but see the registry contradiction below |
| 1a L03/L04, 1b | `agy` | printed `DONE` at exit 0 and **wrote no file** (2 of 6 legs). `NIGHT-LOG.md`: *"silent write failure reported as success — the worst shape, because nothing downstream can tell"* | re-run stdout-only | **YES.** Is `agy`'s file-write mode banned for ordered legs from now on? |
| 1a L03 (1st) | `agy` | *"subscriber fell behind updates, stalled for 5s"* — a **client-side streaming stall under six concurrent `agy` processes**, not a model failure. A **concurrency ceiling**, recoverable by serialising | re-run | recommend a serialisation cap; not a ruling |
| probe | `cursor-agent` | the mission's own absolute path `…\Programs\cursor-agent\cursor-agent.exe` **does not exist on this host** | real path is `…\AppData\Local\cursor-agent\cursor-agent.ps1` — **a `.ps1`, not an `.exe`** | no |

### Three further rulings the log surfaces and does not act on

1. **The registry contradiction.** `ecosystem/provider-registry.yaml` records `grok` as
   PAY-PER-CALL (`$0.037`, measured 2026-08-26); tonight's refusal names a free tier. **Not repaired
   here.** The operator rules which is true. And the consequence for `[#676]`: tonight produced a
   **fifth** outcome — *reachable, correctly invoked, and refused for quota* — which the current
   four-way split (absent · corrupt · mis-invoked · answered) *"would file as 'answered' or
   'unreachable', both wrong."*
2. **The branch-name deviation, flagged and not silently taken.** The mission specified branch
   `night-aj-m03-review`; the closed branch-prefix enum (`AGENTS.md`, "Landing a change") admits only
   `worktree-<name>` for a machine-provisioned lane. **The branch carries the prefix and the worktree
   carries the mission's name.** Recorded at the first line of the log. Ratify or correct.
3. **Contamination, on the record rather than assumed away.** `MISSION-PROMPT.md` was committed into
   the tree the readers were auditing **before legs 1d/1e ran**. Attempt 1's reply quotes the
   mission's own phrase `SUBSTITUTED-PENDING-OPERATOR` — proof it read the prompt. Later invocations
   told the reader to ignore that directory. *"No leg's findings are known to be affected, but the
   possibility is on the record."* The operator rules whether that is acceptable or whether the
   affected legs are void.

**One more deviation, recorded at input time and not a substitution of reader but of locator
granularity:** the mission asked for page/timestamp locators for leg 1a. The transcript `.md`
*"carries NO page numbers and NO timestamps"*, so leg 1a's locators are **line numbers in a split
file in a temp dir**. Combined with §3 — leg 1a is 100% UNVERIFIED — this means the M03 practice
table's locators are both unchecked **and** pointing into a location that will not survive the
night. If any of it is to be citable later, the split file has to be preserved. `R2-VERIFICATION.md`
says it is (*"cheap to re-verify, and the source is preserved"*); confirming that is a five-second
job worth doing before the temp dir is cleaned.

---

## Rows this file is evidence for

- **[#582]** — *substrate router: one gated enum, a capability-keyed table, and the generator that reads it.* §1 row 10 sizes that router against a measured closure number (9 files → 1) and identifies the working prototype it should generalise — the REVIEWER fallback chain — making this a generalisation problem rather than a design one.
- **[#661]** — *SDA-1 is a complete benchmark design that has never been run.* §1 rows 8 and 9 argue the return path and the consumer matter more than the suite, and §2 records that the rejection of per-loop trace inspection rested on a premise repo B falsifies † — both of which bear directly on how that row should be closed.
- **[#676]** — *no check verifies a provider CLI's non-interactive invocation shape.* §4 is the register: two ordered readers lost to a fifth outcome the row's four-way split cannot express, two invocation-shape failures corrected on the ordered reader, and one — MA-1, §1 row 3 — where our own configuration was the thing that refused.
