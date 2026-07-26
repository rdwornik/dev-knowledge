---
intake-id: 17
status: ACCEPTED
origin: Layer-1 architect decision session, 2026-07-25 (browser chat, self-review folded + Fable double-check applied); operator rulings recorded verbatim in the document's own header line
decided-by: operator rulings of 2026-07-25 recorded in this document's header (D1-D6 accepted; grok in; Copilot kept; Gemini re-reviewed; Fibonacci doctrine adopted with boundaries), ingested to `docs/intake/` by CC on operator instruction the same day
disposition: active
note: this document is v2 and supersedes the same-day v1 decision brief (`2026-07-25-architect-consolidation-decision.md`), which is operator-held and NOT ingested - see the provenance note below
---

<!--
  INGESTION NOTE (CC, 2026-07-25) - read this before the document body.

  This intake was INGESTED VERBATIM on operator instruction: "the intake IS the
  document". Everything from the `# CONSOLIDATION DECISION v2` heading down is the
  operator-held brief byte-for-byte; CC added ONLY this note, the frontmatter above,
  and the two ingestion-added sections below (prior art + template-section map).
  Nothing in the brief was restated, summarized, re-ordered, or edited.

  GENRE CAVEAT, recorded not resolved: ADR-98 section 3 draws the intake genre as
  WHAT/WHY only - no HOW, no solutioning. This document carries substantial HOW
  (a scoring formula, a migration sequence, a three-piece plan). It is ingested as-is
  under the operator's explicit ruling, which makes it a sanctioned exception to the
  genre line rather than a silent one. The nearest in-folder precedents are intake #13
  (plan-of-record) and #14 (ruled consolidation pack), both ACCEPTED and both carrying
  plan material.

  STATUS CALL, flagged for cheap reversal: ACCEPTED / disposition: active follows the
  #13 and #14 precedent, because the document's own header records the operator's
  rulings and it is the plan-of-record for the immediately-next arc. If the operator
  intended it to land at READY (approved, awaiting its consumer) instead, that is a
  one-line frontmatter edit - no content changes.
-->

## Prior art (MANDATORY row)

> The prior-art row is the mandatory, gate-enforced intake field ruled in the v1 brief
> ("Backlog.md and projen both came from exactly this move. Make it structural, not
> lucky"). The gate that would enforce it **is not built** - this row is satisfied by
> hand, and the enforcing organ remains unfiled work. Recorded here so the claim is not
> mistaken for an enforced one.

| Prior art | What it is | Evaluated how it landed |
|---|---|---|
| **Backlog.md** (OSS backlog CLI) | Per-ticket-file backlog tree with a directory-as-counter | **Pattern donor, not adopted as the tool.** Rejected as the primary on two named grounds: taxonomy collision with the existing `docs/intake/` + `docs/decisions/` split, and `[#N]` ids already cited across all git history. Its per-ticket-file shape and "the counter IS the directory" property are both carried into the build |
| **build-thin** (author our own minimal layer) | The alternative to adopting a tool wholesale | **PRIMARY - the chosen approach.** Reasoned against Backlog.md above, not assumed |
| **projen** | Generated-project-config tooling | Cited alongside Backlog.md as the precedent proving the prior-art check pays for itself - the reason the row becomes mandatory rather than lucky |
| **AGENTS.md** | Agent-context-file standard: released by OpenAI Aug 2025, donated to the Linux Foundation's Agentic AI Foundation, 60,000+ projects, supported by Codex / Cursor / Gemini CLI / Copilot / Devin / VS Code | **Adopted as a consolidation vehicle, not an addition** - "adopting it is not a bet" (the standard is settled); the bet would be landing it as a sixth context file |
| **ETH Zurich context-file evaluation** (arXiv 2602.11988) | Empirical evaluation of agent context files | **Evidence that reversed the recommendation.** Context files generally do not improve task success and raise inference cost 20%+ (both LLM-generated and developer-committed); repository overviews specifically are unhelpful; instructions ARE followed well, so the value is in non-standard practices; harm is measurably the duplication of what the repo already holds. This is what makes D4's anti-duplication rule + size ceiling + "no repository overview" the ADR's real content |
| **WSJF** (Weighted Shortest Job First) | Standard prioritization scoring | **Shape donor for the formula.** Its sum-of-components form is the cited reason the scoring formula is a sum, not a product - a product of three estimated terms compounds error and lets one low estimate zero an item |
| **Modified Fibonacci scale** {1,2,3,5,8,13} | Standard agile estimation practice | **Adopted as binding doctrine with explicit boundaries** (section 3): consecutive Fibonacci numbers approach the golden ratio, so each step is ~phi x the last, which matches relative-magnitude judgment and kills false precision. Explicitly NOT retrofitted onto functionally measured values |
| **Strangler pattern** | Incremental-replacement migration pattern | **Adopted as the migration shape** - dual-run, byte-stable round-trip, then flip; chosen over a big-bang 158-file cutover |

**Provenance gap, stated plainly.** The Backlog.md / build-thin / projen comparison and the
ETH-evaluation reading were authored in the **v1** brief
(`2026-07-25-architect-consolidation-decision.md`, operator-held, superseded by this
document). v1 was **not ingested** - only v2 was, per instruction - so the rows above cite a
source that is not in the repo. If the reasoning behind those rejections needs to be
defensible later, v1 should be ingested too (its own intake id, SUPERSEDED status) or its
comparison folded in. Flagged for the operator; not acted on.

## Template-section map (ingestion-added; no content restated)

Where `templates/intake-template.md`'s required sections are satisfied by the document
below, and where they genuinely are not. Pointers only.

| Template section | Satisfied by | Honest status |
|---|---|---|
| Problem / motivation | The six corrections table (section 1) carries the defects being corrected | **Partial** - the measured diagnosis behind the initiative (179 KB, 944-char average, 82 tickets in the 900-1200 band) lives in v1, not here |
| Scenarios (+1 view) | - | **Not present.** No "as the operator I ... and then ..." walkthroughs. The load-bearing template section, absent by the document's genre |
| Functional requirements | Sections 1, 3, 4 carry the binding corrections, the Fibonacci doctrine and the scoring form | Present as rulings rather than must/should/could |
| Acceptance criteria (ex-ante) | Section 5's exit test: a fresh session boots and its FIRST message quotes the top-5 ready-set with rationales plus every ruling overdue > 8 days, zero operator memory involved | **Present and falsifiable** - written before build, with a stated stop condition ("not landed in one arc -> stop and re-plan, never roll by momentum") |
| Non-goals | Section 3 item 3 (where Fibonacci does NOT apply), section 5 ("No LLM scoring in this arc"), section 2 (Copilot: no build, no eval ceremony now) | Present, distributed |
| Impact sketch (4+1 lite) | - | **Not present** as a four-view sketch |
| Open questions | Section 6 (R-G, R-N, R-S) | Present |
| Status | Frontmatter above | Present |

---

# CONSOLIDATION DECISION v2 — final form
2026-07-25 · Layer-1 architect, self-review folded, Fable double-check applied · supersedes the 07-25 v1 decision brief
Operator rulings recorded: D1–D6 accepted · grok in · Copilot kept · Gemini re-reviewed (§2) · Fibonacci doctrine adopted with boundaries (§3)

---

## §1 The six corrections, final form

| # | Defect in v1 | Correction (now binding) | Lands where |
|---|---|---|---|
| D1 | "Backlog is hub-only, deploy cost zero" — false in one row: `validate_backlog` ships in the fleet `tier1-lifecycle` plugin | Migration gets an explicit **plugin leg**: the validator handles both formats (or is version-gated) for the transition window; consumer *data* stays old-format per the `#331` deferral | backlog ADR §migration |
| D2 | §6 packed six lanes into "one arc" — violates one-wave-one-arc | **Micro-window** (ARCHITECTURE currency + two filings, ~1h) → **main arc** (intake→ADR→strangler→graph) → **AGENTS.md sitting** (ruling-only, separate) | §5 plan |
| D3 | 3-state PLAN.md erased the review beat — the arc's highest-hit-rate mechanism | **Four states: DRAFT → REVIEWED → APPROVED → CLOSED(outcomes)**. Review SLA (P2): **1 working day** at DRAFT, then cold-review fires automatically — review is a role, not a chat. Deviations (P3): **split ruling** — scope changes need a mid-session operator ruling (strict); order/mechanics changes need only an OUTCOMES entry with rationale (loose) | handoff ADR |
| D4 | "AGENTS.md consolidates five surfaces" — overclaim | Consolidates **CLAUDE.md + per-tool files** (codex/ dissolves). FLOOR stays (ADR-93 armed artifact); ARCHITECTURE/PLAYBOOK/VISION are human-review surfaces. The ADR's real content: **anti-duplication rule** — AGENTS.md repeats nothing that lives elsewhere; pointers over copies; size ceiling; no repository overview (the ETH-verified harm class) | AGENTS.md ADR |
| D5 | Strangler demanded byte-stable round-trip AND prose relocation — mutually exclusive | **Sequence fixed:** verbatim split → byte-stable round-trip proven → source-of-truth flip → **then** prose relocation (944→≤300) as ordinary edits on the new format | backlog ADR §migration |
| D6 | Lane D deferred `#403`'s child-roster derivation the same day §2 found the three-fleet-counts drift it would have caught | **Child-roster added to `#403`'s ruled scope**, with the drift as evidence. The manual ARCHITECTURE fix still happens in the micro-window (the map must be right *now*); the derivation keeps it right | `#403` + micro-window |

---

## §2 Model fleet — re-reviewed without bias, and I reverse myself on one

The operator asked for a re-review free of deference. Here it is, with the reversals and the holds both argued.

### Gemini — REVERSED, with a sharper scope than either of us had

My v1 rejection was scoped to the corp content scan, and **for that job class it stands**: exact-token retrieval (account names, paths, `git log --all` per file) is deterministic work where grep is not just cheaper but *more correct* — a count you derived is a count you can defend.

But the operator's counter names a **different job class, and he is right about it**: the fleet's dependency problem (doc2doc, doc2file, code2file edges) is **semantic**, not lexical. `grep` finds the string "ADR-92"; it cannot find the paragraph that *depends on* ADR-92 without naming it — and the three-fleet-counts drift (§1 D6) is exactly that failure: three surfaces stating one fact, no lexical link between them. ADR-88's own doctrine is "declare what you cannot compute" — and a long-context model is precisely a machine for *proposing* what we currently hand-declare. Free, with a context window that swallows the governing corpus whole.

**Disposition: ACCEPTED as a propose-only semantic lane.** Rules that make it safe, all three hard:
1. **Propose, never write.** Output = candidate edges/findings, each with `path:line` evidence quoted. A deterministic verifier confirms the cited text exists; the operator ratifies. (The moratorium doctrine, applied.)
2. **Deterministic-first routing stands.** If grep/git can answer it exactly, Gemini doesn't get the job. Gemini gets what grep structurally cannot: semantic edges, redundancy maps, long-context synthesis.
3. **AG-2/ADR-12 gate first.** The recorded Gemini lane (Antigravity CLI) is exclusion-listed until the identity-roulette question clears — **R-G below: which CLI is meant** must be answered before any work routes.

**Two pilot jobs, both real:** (a) propose missing doc2doc/doc2file edges for the governing corpus against `doc-code-edge.yaml`, verifier-checked; (b) the **redundancy map for the AGENTS.md consolidation** — find doctrine duplicated across CLAUDE.md/PLAYBOOK/ESSENTIALS/ARCHITECTURE, which is exactly the input D4's anti-duplication rule needs, and exactly a long-context strength.

### grok — clarified: it was never rejected, and it enters now

v1 said probation-before-retirement and the operator read it as gatekeeping. Precise form: **grok enters the review lane on the next code-impact arc, immediately** — shadow alongside terra, zero extra process. **Codex retires on evidence, not on schedule:** the seeded-defect test plants the classes terra actually caught this month (assertion beyond verified scope · the GIT_* scrub-set derivation · the duplicate stale header · the wrapper scoping gap); grok must catch them. Pass → swap, recorded as an ADR, $20 saved. Fail → we learned the lane's ceiling for free. The money was never the argument; the unmeasured quality of a load-bearing safety organ was.

### Copilot — held, and here is the unbiased version of why

"Free" prices the subscription, not the lane: every model lane costs configuration, prompt-shaping, and **output triage** — and the fleet's live, operator-named defect is `#419`: *we already produce output nobody consumes*. Adding a fourth producer before the morning-loop consumer exists makes the actual problem worse, for zero named job — every job on the table is taken (terra/grok: review; Gemini: semantic scans; Haiku/Sonnet: fan-out; sol: derivations). **Disposition: the row stays filed with a trigger, not a rejection** — Copilot activates the day a job appears that the current fleet doesn't cover (most plausible: a GitHub-PR-native review lane if the flow ever moves to PRs). No build, no eval ceremony now.

**One guard binds all three, derived from the operator's own `#419` reframe:** *no model lane without a named consumer* — every lane states, at activation, which morning-loop slot or gate reads its output. A lane whose output nobody reads is `#419` with a subscription attached.

---

## §3 Fibonacci — the doctrine, honestly scoped

The operator's instinct lands on a real foundation, and it deserves the honest version rather than flattery: the modified Fibonacci scale is standard estimation practice **because consecutive Fibonacci numbers approach the golden ratio** — each step is ~φ× the last, which matches how human judgment actually works (we perceive relative magnitude, not absolute; log-spaced scales force meaningfully distinct choices and kill false precision like "7 vs 8").

**Where it becomes binding doctrine (real mechanism, adopted):**
1. **Every estimated field is on the modified Fibonacci scale {1, 2, 3, 5, 8, 13}**: priority, alignment, age_boost bucket, effort. This also *repairs the sum formula* — a sum is only meaningful over one scale, so the scale is what makes `(priority + alignment + age_boost) / effort` sound. unblock_count stays a separate exact column (§4).
2. **Arbitrary constants come from the Fibonacci family.** Where a number is a judgment call anyway, pick it from {…, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, …}: the overdue-ruling WARN threshold = **8 days** · READY-SET quotes **top-5** · ticket body target ≤ **233** chars (was "~300" — arbitrary either way, now family-consistent) · doc_rot per-file cap = **1597** (was 1200 — same protective intent, one family). One recognizable family across the fleet = a constant you can tell apart from a measured value at a glance.
3. **Where it does NOT apply, stated plainly:** functionally measured values (a 1,500-token floor budget measured against context limits; a 30-day cadence tied to a calendar; a hash length) are never retrofitted to φ. The fleet's own core doctrine is mechanism-over-narrative — a golden-ratio file-size proportion has no enforcing mechanism and no failure mode it prevents, so it would be decoration, and decoration is what this fleet exists to kill. The philosophy is honored where a *scale or a free constant* is needed; it is not imposed where reality already fixed the number.

---

## §4 Scoring — final form

```
score = (priority + alignment + age_boost) / effort        # all four on Fibonacci {1,2,3,5,8,13}
```
- **unblock_count**: computed exactly from the graph, shown as its **own column**, never folded into the estimate. "Important" and "unblocks five things" are different facts; the board shows both.
- **Re-scoring is event-driven**, not weekly: score at intake · re-score when the ticket's own fields change · invalidate `alignment` fleet-wide only when VISION changes.
- **Operator override is sticky** — a human-set field survives every sweep.
- Every estimated value carries its one-line rationale beside it.
- **`verified_by`** on every ticket: a command, a path, or the literal `manual` — enforced at intake. (The `#215`/`#339` killer.)

---

## §5 The plan — three bounded pieces, in order

**MICRO-WINDOW (~1h, primary, before or at the next handoff's start):**
ARCHITECTURE currency — ADR-104 into Purpose + Governing roster · one fleet count (point at `index.yaml`, fix its 6→9 registration gap) · strike the paid ADR-92 note · `block_immutable_edits` row + the new `.methodology.yaml` declaration · **add the organ status column** (ARMED / RULED-UNBUILT / RETIRED) · file the codex-wrapper CODE-profile defect · verify the TOKEN-LOG merge anchor · extend `#403` scope (D6).

**MAIN ARC (one wave = one merged arc; the exit test is the closure metric):**
`backlog-as-system` intake (prior-art row satisfied by the brief's own table) → ADR carrying §1 D1/D5, §3, §4, and the §2 v1-rejections-with-reasons → **strangler build**: verbatim split → byte-stable round-trip → flip → prose relocation → **graph layer + READY.md + boot probe**. No LLM scoring in this arc.
**Exit test (falsifiable, unchanged):** a fresh session boots and its FIRST message quotes the top-5 ready-set with rationales + every ruling overdue > 8 days, zero operator memory involved. Not landed in one arc → stop and re-plan, never roll by momentum.

**AGENTS.md SITTING (ruling-only, separate):** the D4-scoped ADR — consolidation vehicle, anti-duplication rule, size ceiling, no repository overview. Gemini pilot job (b) feeds it the redundancy map. Per-repo deploy waits for the wave anyway.

**Riding along, not arcs of their own:** grok shadow on the next code-impact diff · Gemini pilot (a) after R-G clears · `#402` window and the corp `#327` merge stay queued as before.

---

## §6 What remains for the operator (one sentence each)

- **R-G.** Which Gemini CLI is the scanning lane (so the AG-2/ADR-12 exclusion check runs against the right tool)?
- **R-N.** Confirm 8 days as the overdue-ruling threshold (Fibonacci per §3.2) — or name another family member.
- **R-S.** Confirm the seeded-defect list for grok's acceptance test (the four classes in §2) — additions welcome, the test is only as good as its seeds.
