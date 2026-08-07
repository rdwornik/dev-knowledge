# Prompt Template for Claude Code
<!-- scope: meta -->
<!-- version: 1.10 — 2026-08-07 -->

> **Copy this template, fill placeholders, save as `.md` artifact, deliver to Claude Code via paste-into-prompt.** Browser chat produces this; Claude Code executes it.
>
> **Scope — this card governs WORK-LANE prompts.** A work lane is one footprint-disjoint slice
> of a batch, delivered as a pasted contract into a Claude Code session. **ADR-97 epic lanes are
> a different object** — each runs its own chat, boots from a §14a handoff and closes with a §14b
> return — and they are governed by `protocols/PLAYBOOK.md`: the "2–3 concurrent epic lanes" cap
> (`PLAYBOOK.md` "The cap: 2–3 concurrent epic lanes") and the mode vocabulary under
> `PLAYBOOK.md` §"How to choose Mode".
> **Precedence: PLAYBOOK wins on epic-lane criteria.** This card is the point-of-use authority
> for work-lane prompts only; where a prompt boots an epic lane, PLAYBOOK's defaults govern and
> this card's execution-default does not reach it. Declared 2026-08-06 to repair the undeclared
> scope collision the FR-7 v1.6 diff left behind — PLAYBOOK remains the maintenance source and
> the live authority for rationale.
>
> **Risk-tiered ceremony — ceremony scales with arc size, it is not uniform by default:**
> - **Scale S** (single file change, <50 lines work): headless / auto-accept, no plan-mode — contract → execute → terra → queue. Minimal version — Title + Steps + What NOT to do. Skip UNDERSTAND if obvious.
> - **Scale M** (multi-file or non-trivial logic): one plan round. Full template, but UNDERSTAND can be brief.
> - **Scale L** (3+ files, architectural change): full ceremony, full template. **Plan-mode is
>   usually preferred at Scale L** — restored here from v1.5, which the v1.6 diff deleted rather
>   than replaced. For an **L-sized epic story**, PLAYBOOK's stronger rule governs instead:
>   *L-sized epic stories default plan-first* (`PLAYBOOK.md` §"Per-Scale guidance" at Scale L,
>   and "Execution MODE is part of the contract", which carry the §14a item-7 linkage — routed
>   through PLAYBOOK deliberately, since it wins here).
>
> **Plan-mode by exception — the contract IS the plan.** The browser plan-of-record plus the
> frozen contract constitute the plan, and lane MODE is set by the architect *in* the contract
> (the `Mode` row below). The **default WORK-lane mode is execution**, under the decision budget:
> ask only about (a) curated-baseline touches, (b) genuine rule-vs-ruling conflicts, (c) fork
> classes with no standing ruling — everything else is decided per contract defaults and
> **reported** in the end packet rather than asked. CC re-plans what the contract already rules
> only where the contract asks for it. Plan-mode is reserved for M/L arcs needing genuine
> repo-derivation: the class where CC's derivation can overturn the architect's premises.
>
> That execution-default is scoped to work lanes and does not restate PLAYBOOK's general rule.
> `PLAYBOOK.md` §"How to choose Mode" keeps `plan-then-auto` as the default for most
> multi-step prompts, over the three defined values `auto-accept / plan-then-auto / plan`; the
> `execution` value in the `Mode` row below is a work-lane label for that pasted-contract case,
> not a fourth member of PLAYBOOK's vocabulary. Where the two populations meet, PLAYBOOK governs.
>
> Calibration evidence, recorded both ways: a repo-derivation pass overturned 3 of 4 enumerated
> consumers (plan-mode earning its keep), while an S-size one-bit fix cost ~4 operator
> interactions (ceremony without value).
>
> **Lane count:** up to ~10 parallel **work** lanes within reason, bounded by file-disjointness
> and integration capacity rather than by default caution; the number for a given batch stays the
> emitting architect's judgment (intake #25 `AMENDMENT 2026-08-05-c` c1).
>
> **This is a different axis from PLAYBOOK's cap, and the two are deliberately not reconciled to
> one number.** `PLAYBOOK.md` "The cap: 2–3 concurrent epic lanes" caps them **at 2–3**, bounded by the
> root's review and serial-merge bandwidth. The ~10 above counts footprint-disjoint work lanes
> inside a single batch. Different objects, different bottlenecks, both live: ~10 work lanes can
> sit inside far fewer epic lanes. Equalizing the figures would erase a real distinction.
>
> **Standing rulings an agent applies without asking:** `protocols/STANDING_RULINGS.md`.
> Source for this section: intake #25 `AMENDMENT 2026-08-05-b` (V-2 decision budget, V-3
> risk-tiered ceremony) + `AMENDMENT 2026-08-05-c` (c1 lane ceiling, c2 plan-mode-by-exception).

---

| Model  | `<sonnet | opus>` — see the routing matrix below |
| Mode   | `<execution (default) | plan-then-auto (M/L repo-derivation only) | auto-accept>` |
| Effort | `<low | medium | high>`       |

**This table is M/L-only (ruled 2026-08-07).** The **dispatch line is authoritative for model and
effort**, so an **S-class contract omits the whole table** — the line that launched the session
already carries two of its three rows, and a second copy is free to disagree with the first. M and
L keep it, where `Mode` carries something the dispatch line does not. Canonical:
`protocols/PLAYBOOK.md` Ch8 "Model + effort are stated at dispatch — the routing matrix".

**Routing, as ruled — the architect states model + effort on every dispatch; the operator
overrides.** `opus`: M/L arcs, gate and organ code, architecture, adversarial verification, any arc
whose failure poisons downstream work. `sonnet`: S-class bounded edits, documentation arcs,
git-ops. `haiku`: retrieval only. Effort: `high` for multi-file reasoning / design / review,
`medium` as the S default, `low` for mechanical single-file work; `max` sits outside dispatch
routing. Rationale, the CLI check, and the declared boundary against ADR-87's "Model is CC's pick"
all live at the Ch8 heading above — this row is the point-of-use copy, not a second authority.

**Dispatch (fill when this prompt ships via `claude --bg` — every batch lane, without
exception):** `[<repo> · #<id>-or-slug · <verb-object>]` opens the title line below it, so the row
reads at a glance in Agent View at ten concurrent agents rather than needing its tail re-derived
(`protocols/PLAYBOOK.md` Ch8 "Dispatch visibility", `protocols/STANDING_RULINGS.md` B7 — VISIBLE
= DISPATCHED). Foreground, interactive sessions skip this row. **Dispatch constants** ride every
such line: `--permission-mode bypassPermissions`, `--bg`, and the board label.

# `<board label, if dispatched — see Dispatch row above> <Imperative title — what this prompt accomplishes>`

**Repo:** `<absolute path to repo, e.g. C:\Users\1028120\Documents\Dev\corp-monorepo>`
**Purpose:** `<one sentence — what gets achieved by running this prompt>`

Read `CLAUDE.md`, `<other read-first files relevant to task>`, and check `~/.claude/skills/gotchas/` before starting.

**Governance pointer:** `<the specific ADR / LESSONS entry / sibling-spec this task touches, or "none">` — the architect fills this thin pointer; CC self-loads code-impact context + generic gotchas but won't self-infer governance context (ADR-87).

## Git workflow
<!-- scope: meta -->

1. `git checkout -b <branch-name>` (branch name follows repo convention from CLAUDE.md)
2. Commit after each step (or numbered group below)
3. Merge to main when green: `git checkout main && git merge --no-ff <branch>`

## UNDERSTAND
<!-- scope: meta -->

**Problem:** `<2-4 sentences describing what's wrong, why it matters, what's the desired end state>`

**What could break:**
- `<failure mode 1 — concrete, repo-specific>`
- `<failure mode 2>`
- `<add as identified>`

**Most likely failure mode:** `<the one that's most probable given the change shape — with mitigation>`

`<For Scale L: also include "What's already done that this builds on" pointing to ADRs, prior commits, related templates>`

## READINESS (explore-mode valve — ambiguous input only)
<!-- scope: meta -->

`<Include ONLY when the input is ambiguous — unclear scope, unstated acceptance
criteria, or more than one defensible interpretation. For a well-specified task,
delete this section and proceed to Step 1.>`

When the task is under-specified, do **not** start building. Emit a named
readiness verdict and stop:

- **Verdict:** `<READY | NEEDS-INPUT | BLOCKED>` — one word.
- **What's clear:** `<the parts you can act on with confidence>`
- **What's ambiguous:** `<each open question that changes what gets built — concrete, not "let me know if you have questions">`
- **Go / no-go:** on `NEEDS-INPUT` or `BLOCKED`, **create nothing** and wait for the operator. Only `READY` proceeds to Step 1.

A richer cousin of STOP-after-UNDERSTAND: UNDERSTAND records what you know;
READINESS forces an explicit go/no-go before anything is created. The valve's job
is to make "I wasn't sure, so I guessed" impossible — an unresolved ambiguity is
a stop, not a default.

## Step 1: `<imperative — what's done>`
<!-- scope: meta -->

`<concrete action with file paths, commands, or content>`

```powershell
<commands if applicable>
```

Verify: invoke the `verify` skill — any FAIL blocks this step.

**COMMIT:** `<conventional commit message — feat(scope): / fix(scope): / docs(scope): / chore(scope): / refactor(scope):>`

## Step 2: `<imperative>`
<!-- scope: meta -->

`<repeat structure — content + verification + COMMIT marker>`

`<Add Steps 3-N as needed. Each ends with COMMIT marker unless explicitly grouping into one commit.>`

## Final
<!-- scope: meta -->

```powershell
<verification commands — typically:>
python <validator if applicable>
git log --oneline -<N>
git status
```

`<Specific success criteria for this prompt — what must be true>`

**Obsolescence pass:** propose deletion of content this change supersedes, instead of writing around it — surface candidates with evidence for the operator to ratify (auto-delete stays forbidden; git history preserves). Per the PLAYBOOK §2 pruning-symmetry rule.

Final: `/ship "<summary> [#id if closing]"` — refuses if: on `main`, dirty tree, or validators red.

## What NOT to do
<!-- scope: meta -->

- Do NOT `<anti-pattern specific to this task>`
- Do NOT `<scope creep risk>`
- Do NOT `<repo-specific hazard>`
- Do NOT touch `<repos or paths explicitly out of scope>`

---

**Section history:**
- v1.10 (2026-08-07) — **the routing matrix lands, and the Model/Mode/Effort table becomes
  M/L-only.** Architect ruling of the batch-2 consolidation arc: the browser-architect states model
  **and** effort on every dispatch, the operator overrides, and the **dispatch line is
  authoritative** for both — so an S-class contract drops the table rather than carrying a second
  copy of two rows the launching line already fixed. The matrix itself (opus / sonnet / haiku by
  arc class; high / medium / low by work shape; `max` held out of dispatch routing) rides here as a
  point-of-use copy, with rationale, the live-CLI flag check, and the **declared boundary against
  ADR-87's "Model is CC's pick"** at the canonical home — `protocols/PLAYBOOK.md` Ch8 "Model +
  effort are stated at dispatch — the routing matrix", which this version adds. The `Model` row's
  enum is lower-cased to match what a `--model` flag actually takes, and the Dispatch paragraph
  gains the three dispatch constants (`--permission-mode bypassPermissions`, `--bg`, board label).
  Reciprocal pointer added at PLAYBOOK §2 "How to choose Model", per the v1.7 precedent for
  declaring a boundary rather than equalizing two texts.
- v1.9 (2026-08-07) — adds the **Dispatch row + board-label title convention**, for prompts that
  ship via `claude --bg`: the `[<repo> · #<id>-or-slug · <verb-object>]` bracket opens the title
  line, carried through into what Agent View shows for that row. Encodes AM-4 (operator-ratified
  2026-08-06, verified live) — `protocols/STANDING_RULINGS.md` B7 "VISIBLE = DISPATCHED",
  `protocols/PLAYBOOK.md` Ch8 "Dispatch visibility". Foreground/interactive prompts leave the row
  blank; nothing else in the template changes.
- v1.8 (2026-08-06) — **line anchors converted to anchor text** ([#505] coupled repair). The [#505] arc adds a section to PLAYBOOK Ch8, which shifts every line below it; this card carried four `PLAYBOOK.md:NNN` citations that the insertion would have silently rotted, and one (`:2504`) that had already drifted eleven lines onto a table row. Each now cites the heading or bolded lead it means, per the standing lesson that a line anchor rots inside its own branch while an anchor text does not. The v1.7 entry below keeps its original line numbers: it describes a past state and is a record, not a live pointer. No doctrine changed — the only edits are the form of five citations and this entry.
- v1.0 (2026-04-24) — initial template per Gap #2. Standard 8-section structure (Model/Mode/Effort → Title → Read first → Git → UNDERSTAND → Steps → Final → What NOT to do).
- v1.1 (2026-06-06) — Final merge boilerplate replaced with `/ship` delegation (closes #103).
- v1.2 (2026-06-06) — Per-step verification line replaced with `verify` skill invocation (closes #104).
- v1.3 (2026-06-09) — Final gains a standing **obsolescence pass** line (propose deletion of superseded content instead of writing around it; operator ratifies) — point-of-use of the PLAYBOOK §2 pruning-symmetry rule (closes #136).
- v1.4 (2026-06-10) — UNDERSTAND gains an optional **READINESS valve** for ambiguous input (named verdict + go/no-go, create nothing until operator approves) — #111 (c). Folds as a valve, not a new organ.
- v1.7 (2026-08-06) — **scope-split repair.** v1.6 changed mode criteria without the matching `PLAYBOOK.md` edit its own maintenance rule (`PLAYBOOK.md:2665-2675`) requires, which PLAYBOOK names "a process bug"; the result was four undeclared collisions with landed doctrine. This version declares the boundary rather than equalizing the texts: **this card governs work-lane prompts; ADR-97 epic lanes are governed by PLAYBOOK, which wins on epic-lane criteria.** Cross-pointers added both ways (PLAYBOOK gains the reciprocal note at `:1643` and `:2504`). Restores v1.5's "plan-mode usually preferred" at Scale L, which the v1.6 diff deleted rather than replaced, and defers to PLAYBOOK's stronger *L-sized epic stories default plan-first*. Scopes the execution-default to work lanes and records `execution` as a work-lane label rather than a fourth value in PLAYBOOK's three-value vocabulary. The ~10 work-lane ceiling (AMENDMENT-c c1) and PLAYBOOK's 2–3 concurrent *epic* lane cap are kept as **different axes** and deliberately not reconciled to one number. Operator-confirmed 2026-08-06.
- v1.6 (2026-08-05) — the per-Scale block becomes a **risk-tiered ceremony** clause (S: headless/auto-accept, no plan-mode; M: one plan round; L: full ceremony) and gains **plan-mode-by-exception** — the contract IS the plan, default lane mode is execution under the decision budget, plan-mode reserved for M/L arcs needing genuine repo-derivation. Adds the lane-count ceiling and the pointer to `protocols/STANDING_RULINGS.md`; the `Mode` row enum now leads with execution. Lands intake #25 AMENDMENT-b V-3 + AMENDMENT-c c1/c2 (FR-7b); AMENDMENT-b V-2's register is the sibling commit.
- v1.5 (2026-06-18) — adds the **Governance pointer** field (the thin per-task ADR/LESSONS/sibling-spec pointer the architect always fills; CC won't self-infer governance context) — point-of-use of the ADR-87 equilibrium contract; dual-maintenance with PLAYBOOK §2 "Architect output vs CC consumption-spec".
