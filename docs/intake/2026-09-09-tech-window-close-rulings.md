---
intake-id: 90
status: DRAFT
origin: browser seat (Fable), closing rulings of window 2026-09-08-dev-knowledge-architect-2, 2026-09-09 — `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` + `to-cc/AMEND-CONDUCTOR-DECISION-001.md`, `to-cc/DECLARE-DISPATCH-RETIREMENT-2026-09-09.md`, `to-cc/DECLARE-BATCH-V-CLOSE-2026-09-09.md`; filed by the operator's 2026-09-09 background act as the transports V-10 did not cover
consumed-by:
---

# Who fires the next phase, what dispatch becomes, and where the baseline lives — the three window-close rulings V-10 left on the transport

<!-- class: tech (process spine + the mechanisms that carry it) · status: DRAFT — these are
BROWSER-SEAT declarations carrying the operator's stated direction; the conductor decision (E) is
a scored recommendation, NOT an operator ratification, and this doc does not claim one.
Non-citable as doctrine until ruled. The repo wins on any conflict.
Genre note (ADR-98 §3): two of the three sources are decision-shaped and one is a close packet.
WHAT/WHY is carried in the canonical sections below; the declared matrices, sequences and
deletion lists are carried verbatim-in-substance under "The rulings as declared", which is a
RECORD of the sources, not a specification this doc invents.
Provenance limit: `DECLARE-CONDUCTOR-DECISION` §7 lists three facts to verify before build. One
came back NO (see §A2). The other two are UNVERIFIED here and are carried as open questions, not
as findings. -->

## Problem / motivation

**The gates are mechanisms and the process between them is not.** Organs fire at commit and at
push; what happens between them — a row moving from intake to task to build to review to merge to
docs to deploy to telemetry to archive — is carried by seats' diligence and by the operator
pasting. `DECLARE-HARNESS-IS-PROCESS` §5 names this exactly: the Maister plugin's only real
structural advantage was a **process spine** — a state file that triggered phases and knew where
the task stood — and *"ours have no spine"*.

Three rulings close that window and they are one argument, not three:

1. **Who fires the next phase** — scored across five options, decided as **E** (state in repo
   files, GitHub Actions as runner, `claude-code-action` as lane executor).
2. **What happens to `dispatch`** — it does **not** move to the hub. It is **retired** once
   Actions is the runner, and win-tooling returns to its charter.
3. **Where the baseline lives** — the gates ship against Windows, so **Windows is the baseline
   substrate**; the Codespaces 44-RED figure is retired as a comparison base.

The motivation for filing them together is that ruling 2 is a *consequence* of ruling 1 and is
unsafe to act on alone: retiring the dispatch layer before the runner exists leaves a day on
which nothing can fire a lane.

## Scenarios (+1 view)

- **Operator, today.** Wants a feature in `corp-monorepo`. Pastes a contract to a seat, waits,
  pastes to an integrator, waits. Phase transitions without operator action: ~0%.
- **Operator, under E.** Sets `phase:` in a task file and pushes. Actions evaluates the phase
  gate and performs the phase action; `claude-code-action` opens the PR. The operator reads
  `gh run list` at SessionStart and answers only what awaits his word.
- **Seat, under E.** Reads the task file as its contract, works in the runner, opens a PR. No
  worktree discipline, no `dispatch` verb, no "paste this to the integrator".
- **+1 (deployment view).** State never leaves the repo, so the fallback (**B** — same task
  files, same phase table, run locally by a hook) needs **no state migration**. That is what
  makes E reversible.
- **The failure scenario this must survive.** GitHub is down, or Actions minutes are exhausted
  mid-batch. Under E the runner stops; under B the same task files still drive a local hook.

## Functional requirements

- **FR-1 · State stays in the repo.** `tasks/<row>.md` gains a `phase:` field; `validate_backlog`
  knows the enum. ADR-38 untouched; "decisions are files" untouched.
- **FR-2 · Runner is GitHub Actions.** `.github/workflows/conductor.yml` on
  `push · pull_request · schedule · workflow_dispatch`, reading `tasks/`, evaluating the phase
  gate, performing the phase action. Scheduling, durability, retries, logs and UI are GitHub's;
  the only custom content is the phase table, which is custom in every option because it *is* the
  process.
- **FR-3 · The hub holds configuration, not execution.** `conductor.yml` is config, so ADR-28's
  "Layer 2 never executes" stays true. This is the requirement that makes the whole design legal
  here, and it is why moving `dispatch` into the hub was refused.
- **FR-4 · Gates are required checks** on `main` — pytest · ruff · seal · terra review. Codex
  review becomes a job, never a paste. **This leg is currently BLOCKED — see AC-2.**
- **FR-5 · Lane executor is `claude-code-action`**, reading the task file as its contract. Local
  `claude` stays available unchanged for when the operator wants to code himself.
- **FR-6 · Retirement is ORDERED, not simultaneous.** New hands hold before old hands let go:
  (1) E lands, (2) a first batch runs through Actions and the runner is proven, (3) only then a
  win-tooling lane deletes the dispatch layer.
- **FR-7 · The transport survives the retirement, narrowly.** Local sessions still need it for
  exactly one purpose: ingesting the browser's `to-cc/` files into `tasks/`, because the browser
  has Drive, not git. The resolver and the dev-terminals launcher setting `CLAUDE_PROMPTS_DIR`
  from User scope before spawning `claude.exe` (merged `6470fa8`) are kept; everything
  dispatch-specific from that arc retires with the layer.
- **FR-8 · Windows is the baseline substrate.** `28 RED @ ba0dd7a7 (Windows, unattended path,
  --timeout=900)` is the standing baseline. Codespaces keeps its role as fast read-only compute
  and is **never again a comparison base**.

## Acceptance criteria (ex-ante)

- **AC-1 · Phase transitions without operator action ÷ all transitions** — today ~0%, target
  **> 80%**, read from Actions logs.
- **AC-2 · The gate leg is honest about being blocked.** `AMEND-001` §1 verified that the **free
  plan blocks rulesets and branch protection on this private repo** (403 on both APIs). Required
  checks were E's gate mechanism; without them Actions can RUN every check and post a status but
  **nothing BLOCKS a merge** — which degrades to "a human reads the status", i.e. today's
  integrator with better logs. The runner leg is unaffected. Accepted only under one of: GitHub
  Pro (~$4/month, restores E as designed, **the amendment's recommendation**), or an explicit
  ruling to accept the degraded gate.
- **AC-3 · Operator hours per feature landed in `corp-monorepo`** — today ∞ (nothing has reached
  it), target: **a number**.
- **AC-4 · Operator pastes per week** — today dozens, target **< 5**.
- **AC-5 · Organs deleted from the §5 list** — target **≥ 10**.
- **AC-6 · Actions minutes per week** against the free 2,000/month (Pro: 3,000) — added by
  `AMEND-001` §3 as the fifth number. Current: **1,005 of 2,000 used this month**. If a batch
  burns the month's minutes the runner is not free and the decision is re-scored.
- **AC-7 · The 30-day re-evaluation is binding.** If AC-1 and AC-4 do not move, **revert to B**.
  No state migration needed — that is the point of FR-1.
- **AC-8 · The six unattributed REDs are attributed by measurement, not reasoning** — one
  same-substrate run on the pre-batch commit, overnight, unattended. One row.

## Non-goals

- **Not a ratification.** E is a scored recommendation from a browser seat. This document records
  it; it does not adopt it.
- **Not a migration of `dispatch` into the hub.** Explicitly refused: it would break ADR-28 and
  make the store an orchestrator — a second error on top of the first.
- **Not a deletion of the dispatch layer now.** FR-6 forbids it until the runner is proven.
- **Not a claim that the Windows and Codespaces RED counts are comparable.** They are not; that
  is the ruling.
- **Not a cross-substrate regression analysis.** Ruled unattributable by construction.

## Impact sketch (4+1 lite)

- **Logical.** `tasks/*.md` gains one field (`phase:`); the phase table becomes the process
  definition; BACKLOG stays a render. Nothing about "state = files" changes.
- **Process.** Dispatcher and integrator stop being **seats** and become mechanisms: runner =
  worktree, PR = branch, merge queue = integrator.
- **Development.** Deletions land in win-tooling (`Invoke-Dispatch.ps1`, `dispatch-alias.ps1`,
  `dispatch.cmd`, the dispatch half of `DispatchHelpers.psm1`, the four
  `Dispatch-Local/Cloud/Codespace` verbs) and in the hub (`SEAT-BOOT-dispatcher`,
  `SEAT-BOOT-integrator`, `[#441]`, PLAYBOOK Ch8's dispatch table and worktree launch test).
  Declared deletion count: **≥ 4 files, 4 verbs**.
- **Physical.** Compute moves off the workstation to GitHub runners — which is the operator's own
  "workstation is not fleet compute" criterion, weighted 2 and scored 3 for E.
- **+1 (scenario).** The whole point is AC-1: a phase that fires itself.
- **Kept, explicitly:** `tasks/`, BACKLOG-as-render, pre-commit hooks, audit organs, the graph —
  everything that is state or gate.

## Open questions

1. **Does the operator ratify E?** The matrix is a browser seat's scoring of the operator's own
   criteria; the decision is functional and therefore his (ADR-108 §A).
2. **AC-2's money question.** GitHub Pro, or accept the degraded gate and revisit when the paste
   count stalls? The amendment recommends Pro; nothing has been bought.
3. **`/install-github-app` on the hub repo** — `DECLARE-CONDUCTOR-DECISION` §7 fact 3. **Not yet
   reported.** Unverified here.
4. **Actions minutes headroom** — §7 fact 2 is partly answered (1,005 / 2,000 used) but no batch
   has been run through Actions, so cost-per-batch is unmeasured.
5. **`[#563]`'s owner may disagree** with the §2 ruling below; the declaration says escalate
   rather than pick a side silently, and that escalation has not happened.
6. **Does retiring `dispatch` strand any consumer** the deletion count did not enumerate? The
   count is declared (≥4 files, 4 verbs), not measured against a reader census.

## The rulings as declared

*A record of the three sources, carried verbatim-in-substance. Not a specification this document
invents.*

### §A · Conductor decision — E (`DECLARE-CONDUCTOR-DECISION-2026-09-09` + `AMEND-001`)

**A1 · Why a matrix at all.** Three turns produced three different answers because there was no
scoring — each turn answered the last conversational pressure. The matrix is the mechanism
against that, and it is the artifact the decision is re-evaluated against in 30 days.

**A2 · The options and the score.** A (Issues + Actions) 52 · B (Claude Code native) 55 ·
C (workflow engine, self-hosted) 38 · D (local state machine) 46 · **E 58**. Criteria and weights
are the operator's own: library-first (3), one entry point (3), workstation is not fleet compute
(2), state = files in the repo (3), deletes more than it adds (3), reversibility (2), Claude Code
as executor (2), cost (1), offline (1), evaluable in 30 days (2).

**A3 · The amendment's three corrections.** (i) §7 fact 1 came back **NO** — free plan blocks
rulesets and branch protection (403); E's gate leg degrades and needs a plan decision. (ii) A
fifth evaluation number: Actions minutes per week. (iii) **A row-number correction:**
`DECLARE-RECOVERY` and `DECLARE-SPINE` name the spine row `[#644]`, but V-4 assigned
`[#644]`–`[#663]` to the assembly rows and **the spine is `[#664]`**. Browser error; both
DECLAREs read `[#664]` from the amendment forward.

### §B · Dispatch retirement (`DECLARE-DISPATCH-RETIREMENT-2026-09-09`)

**B1 · The systemic error, named correctly.** Dispatch landed in win-tooling *by consequence of
ADR-28, not by accident*: the hub is "passive storage & governance, not an orchestrator", so it
refused to hold anything that executes; the process still needed a runner, and it went to the only
repo that spawns processes — the launcher repo, which carries no governance. **The error is that
the hub's process had no governed home for its runner.** Moving dispatch into the hub would break
ADR-28 and make the store an orchestrator: a second error.

**B2 · The decision.** Under E the runner is Actions and the hub holds `conductor.yml` —
configuration, not execution — so ADR-28 stays true. The PowerShell dispatch layer is **retired,
not moved**. `dispatch <contract>` becomes "set `phase:` in the task file and push";
`Dispatch-Local` becomes native `claude` with Claude Code's own subagent-in-worktree isolation.
Win-tooling returns to its charter: TypeWhisper, dev-terminals, VS Code.

**B3 · The order.** No day on which nothing can fire a lane — see FR-6.

### §C · Batch V close (`DECLARE-BATCH-V-CLOSE-2026-09-09`)

**C1 · Windows is the baseline.** *"28 == 28" is arithmetic coincidence*, correctly refused by the
integrator. The prior baseline is Codespaces (44 REDs, 17 of them the `fleet_analytics`/pandas
delta, 27 comparable); this run is Windows. **A cross-substrate diff cannot separate a regression
from a substrate effect**, so the 9 "new" are not attributable by reasoning. Ruled: the gates ship
against Windows, therefore **Windows is the baseline substrate**.

**C2 · ADR-111 CANDIDATE — the `[#563]` collision is ruled against the TEST, not the census.**
The census requires a disposition for every unwired script keyed by script path; `[#563]`'s test
greps the corpus for the substring `export_backlog_view` to prove nothing reads the export, so the
disposition cannot name the file and the census requires that it does. **The test checks a NAME to
prove a RELATIONSHIP** — same class as `asserted_by` naming a non-reading organ, the v1.5.0 drift
probe matching the literal `--report`, and P11's presence-only check: **six instances in two
days**. Ruled: `[#563]`'s test is corrected, not the census; it asserts the absence of a `reads`
edge into the export artifact, checkable now that FPG-1 is armed. *"This is the spine's first
useful act: it settles a conflict a grep could not express."*

**C3 · What batch V landed.** P11 prose → gating predicate (V-5) · FPG-1 spine armed and verified
(V-9) · seal WAIVE 336 → 204, consumer residue 67 (V-3) · `#73` clauses read 4/9 → 8/9, lying
`asserted_by` 3 → 0 (V-2) · Copilot refused on the seeded-defect bar, 0 → 21 attributed (V-8) ·
assembly debt filed as `[#644]`–`[#663]` (V-4) · five SEAT-BOOT templates + LEDGER generator
(V-6) · this window's rulings as intake + rows (V-10) · the operator's host completed its own
suite for the first time.

**C4 · Not landed: nothing reached `corp-monorepo`.** Stage 10 of the delivery loop is untouched
and **remains the only item that changes the operator's day**. It waits on his ruling on the
2026-08-29 deploy freeze.

**C5 · Practice worth keeping.** The integrator's wrong lane count in JOURNAL (g) was corrected
**by append in (i), not by editing the entry**. History stays; corrections attach.

## Landed by this act — two rulings executed, three confirmations recorded

*This section is the RECORD of repo changes made while filing this intake, so the rulings and
their execution are legible in one place.*

### Ruling (a) · `dispatch_drift` is landed and armed — two prose lines corrected

Two live governance surfaces asserted the organ was owed. **Both were false, and had been since
`[#592]` landed on 2026-08-27:**

- `protocols/PLAYBOOK.md` Ch8, the dispatch table's closing bullet — read *"This table checks
  nothing… the drift organ… is owed rather than landed."*
- `protocols/STANDING_RULINGS.md` §V "Honest limit" — read *"is owed and unbuilt; until it exists
  these rulings bind the seat and not the tree."*

**The premise was verified before either line was touched**, not taken on the instruction:
`scripts/dispatch_drift.py` exists, `scripts/audit_checks/check_dispatch_drift.py` wraps it,
`tests/test_dispatch_drift.py` covers it, and `scripts/audit_checks/registry.py` wires it at
`TIER_COMMIT`. It appears in the live check list as check **52 · `dispatch_drift`**.

Both lines are corrected **in place, with the prior claim quoted and dated**, so the record shows
what was asserted and for how long. The PLAYBOOK correction is deliberately **line-count neutral**
(3 lines → 3 lines) because live citations at `PLAYBOOK.md:3439`, `:3630` and `:3700` sit below it
— and `[#607]` requires `PLAYBOOK.md:3700` to stay byte-identical as a `provider-registry-agreement`
gate seam.

**Two observations this act does NOT act on, recorded rather than silently fixed:**

1. **`[#592]` is still `status: open` while its organ is landed and armed at commit tier.** That
   is a closure decision, not a new row — an **ADR-111 CANDIDATE** for the operator's word.
2. **`scripts/audit.py:2828`** — the `dispatch_verb_agreement` docstring describes its sibling as
   *"the drift organ `protocols/STANDING_RULINGS.md` §V records as 'owed and unbuilt'"*. That
   description was accurate about §V and is stale the moment §V is corrected. **Deliberately not
   edited:** `audit.py` carries line-shift-sensitive oracle tests, and the operator's ruling named
   two prose lines. Six further sites quote the same phrase as *provenance* (`dispatch_drift.py:12`,
   `dispatch_surface.py:10`, `tests/test_dispatch_surface.py:7`, `ecosystem/doc-code-edge.yaml:206`,
   two `tests/test_audit.py` history comments) — those are correct as history and are left alone.

### Ruling (b) · Five PLAYBOOK sections marked DEAD — marked, not cut

Each section now carries a blockquote marker directly under its heading, citing
`DIGEST-playbook-chapter-map` per section with that map's own line span, byte count and verdict.
**Nothing was deleted:** disposition awaits the operator's word, and the marker is the record that
it is owed.

| § | Section | Span (map) | Scope of the ruling |
|---|---|---|---|
| 1 | Starting a New Project | 4450–4523, 2,304 B | whole section — every concrete instruction contradicted |
| 6 | Code Review with Claude Code | 5159–5173, 452 B | whole section — superseded 590 lines later |
| 9 | Weekly Review (Friday) | 5417–5432, 833 B | whole section — zero practice trace |
| 12 | Multi-Project Rules | 5598–5622, 1,054 B | **config hierarchy only** — `Dev/CLAUDE.md` verified ABSENT |
| 13 | Where Knowledge Lives | 5623–5663, 2,771 B | **Obsidian row only** — remnant of a ruled deletion |

The map's line numbers were **resolved against the live file before use** and still match exactly,
so PLAYBOOK has not shifted since `d12beac6`. §12 and §13 are scoped deliberately: the operator
ruled the config hierarchy and the Obsidian row, not the sections containing them.

### Confirmation · `[#644]`–`[#663]` carry R-2…R-8 — and where §5 actually lives

**R-2…R-8 are fully carried, one row each, no gaps:** R-2 `[#644]` · R-3 `[#645]` · R-4 `[#646]` ·
R-5 `[#647]` · R-6 `[#648]` · R-7 `[#659]` · R-8 `[#658]`.

**`DECLARE-HARNESS-IS-PROCESS` §5 is carried, but NOT by that range — and no row was filed for it,
because filing one would have manufactured a duplicate.** §5 makes two claims and both already
have homes:

- **The spine claim** (*"ours have no spine"*) is row **`[#664]`** — which is precisely the
  `[#644]`→`[#664]` correction `AMEND-CONDUCTOR-DECISION-001` §4 exists to make, so its absence
  from the `[#644]`–`[#663]` range is the *corrected* state, not a gap.
- **The four AJ deltas** §5 names as *triggers the process lacks* are all live intake items at
  status DRAFT: reviewer re-runs tests (**#79**), resumable lane state (**#80**),
  reference-implementation seeding (**#78**), cost per command (**#83**).

**Honest limit on this confirmation:** what *is* absent is any **citation** of
`DECLARE-HARNESS-IS-PROCESS` from a task row — the string appears in three `docs/audits/` artifacts
and in zero of the 20 rows. That is a traceability thinness, not missing work, and it is recorded
here rather than converted into a row the funnel does not need.

### Append · `[#675]` gains its ninth instance

A one-file, text-only row merged out-of-batch cost **~12 minutes and two merges**. Three
mechanisms compounded, none able to see the size of what it was deciding: **(a)** the ADR-110
anchor exemption is bound to *"an open batch"*, not to work class — batch V had closed 8/8, so a
two-line edit took the posture of a twelve-lane arc; **(b)** the anchor rule is **self-referential**
— an entry cannot name a SHA that did not exist when it was written, so two commits is the
structural minimum; **(c)** the apparatus fires on the **contract**, never on what the contract
writes. Done-when gains: a text-only diff takes a **single-commit path with its anchor in the same
commit**, taking minutes-to-merge from the measured 12 to **under 2**.

## Status

**DRAFT.** Filed 2026-09-09 by the operator's background act. Carries three browser-seat
declarations plus one amendment; **none is an operator ratification**, and the conductor decision
(E) in particular is a scored recommendation awaiting his functional ruling (ADR-108 §A).

Rulings (a) and (b) above are **executed in the tree**. Everything under "The rulings as declared"
is **recorded, not adopted**. The blocking decision is Open Question 2 (AC-2): without required
checks, E ships its runner and not its gate.
