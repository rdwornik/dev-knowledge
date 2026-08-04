---
intake-id: 22
status: SEED
origin: operator, dictated 2026-07-30/31 in the outgoing browser-seat window; ingested verbatim from the operator's drafted file at the [#446] window close
consumed-by:
---

**NOTE 2026-07-31:** §A + §B ratified by promotion → ADR-108. §C–§H remain unratified.

**NOTE 2026-07-31 (2):** §E ratified by promotion → ADR-109 (the [#382] arc's functional
requirement, transcribed verbatim there). Doc stays SEED — §C/§D/§F–§H remain open.

# Operator design input — decision routing, engineering standards, and lane timeline

<!-- class: func (operator design input) · status: SEED — NOT ratified; ingest per the intake
convention and ratify AFTER [#446] lands. Non-citable until ingested; repo wins on conflict. -->
<!-- origin: operator, dictated 2026-07-30/31 in the outgoing browser-seat window -->

## A. Decision-routing doctrine (the core ask — ratify as standing rule)

1. **The operator rules FUNCTIONAL questions only** — what the system should do, how output
   should look, priorities between outcomes. Plain-language briefs, no technical vocabulary.
2. **The architect rules TECHNICAL questions in its own lane** — makes the call, records it
   (git + changelog + record), and relies on revertability instead of escalation. Uncertainty
   is not a reason to ask the operator; it is a reason to decide, record, and mark revertable.
   Continuous improvement: decide → test → revert-if-wrong is the sanctioned loop.
3. **AI Council is the distillation organ for genuinely contested technical decisions** — not
   the operator. Endstate the operator wants: finish/deploy ai-council once the methodology
   lands, and keep it as the standing organ for "we have a technical question" moments.
4. Anti-pattern to retire: presenting the operator with option menus of technical forks
   (R1/R2-style). If a brief cannot be written functionally, it is not the operator's decision.

## B. Engineering standards (standing, every build arc)

- **Clean architecture** — layer model as specification (declared edges, mechanized check;
  the ai-council layer-edge review is the precedent), file-size equilibrium as a design value.
- **TDD** — RED-first witnesses and failing tests before build code, frozen after freeze.
- **Spec-driven development** — rule-first, spec before build, acceptance contract ex-ante.
- These are expectations the harness enforces, not per-arc negotiations. Target operating
  model: operator states requirements; the harness (methodology + agents) implements —
  Cursor-like, "the operator should not have to think about the how".

## C. Model-fleet timeline (open rulings R-G, R-S — give them dates)

- **grok (R-S, shadow review):** consumer exists today (code review beside terra). Proposal:
  A/B shadow on 2–3 arcs immediately after [#446]; decision criterion = findings quality vs
  cost vs Codex/terra. Cheaper-and-possibly-better is the operator's stated hypothesis.
- **Gemini (R-G, large-context lane):** consumer = read-heavy folder/file scanning (fleet
  census, cross-repo reads) where Gemini's context size is the differentiator. Proposal:
  activate with the #383/L4 era (graph + census work), per ADR-105 (named consumer +
  consumption_path required).

## D. Context-distiller pre-phase (research 2026-07-27 — currently unfiled, do not lose)

- **repomix `--compress`** — deterministic Tree-sitter distillation of files before an agent
  reads them (token counts per file, MCP server). Operator's intent: a "booster/pre-phase"
  so agents stop skimming large markdown/code. Candidate consumer: the §B(b) boot bundle
  itself (distillate instead of raw files) and any read-heavy lane.
- Siblings from the same research pass, also unfiled: **pyadr** (ADR lifecycle CLI),
  **copier/cruft** (fleet template propagation — directly serves the "change X for all
  repos at once" requirement in §E).
- Ask: verify none has a row (grep), then file as research-consumption rows; sequence after
  [#446] as cheap standalone items.

## E. Fleet-management requirement (functional statement of the #382 chain)

The operator's target, in his words: ask "which repos have component/role X" and get an
answer from a graph; change a library, a CLAUDE.md, a template for ALL repos in one governed
operation; see at a glance what is hub-owned vs repo-local, with versioning. Current state
(declarations in `.methodology.yaml` + fleet_parity + plugin lockstep) is the seed; the
query-and-manage layer IS #382 (pydantic) → #383 (networkx) → #385 (pandas) + copier/cruft
for propagation. Ratify this paragraph as the chain's functional requirement so every arc in
it closes against operator intent, not only technical Done-whens.

## F. Backlog equilibrium (raise the 08-26 cluster's rank)

The backlog must SHRINK — that is a functional requirement, not a review item. The 08-26
cluster (scoring/Fibonacci scale, drain, D-queue, caps-as-equilibrium incl. file-size legs)
is the mechanism; its entry gate stays the §3.2-vs-[#364]-4(a) reconciliation. tasks/ in
root: confirmed good.

### F.1 — RULED 2026-08-04: §F is a FLOW property, not a count target

> Ruled by the architect this window and recorded here, beside the §F it governs, because it
> had been chat-only. The §F text above is preserved verbatim; this is the ruling on how it is
> measured, appended.

**The rule, as ruled:**

> §F is gated per window as a flow property — **closed ≥ filed** — with the window boundary
> defined by **consecutive handoff seal SHAs**; **no gross-count target exists**; **deferred
> rows are excluded** from the flow metric and owe a **one-time batch review**.

**What each clause is doing.** The L-F ruling-prep laid out four candidates
(`docs/audits/2026-08-03-technical-night-lf-rulings-prep.md`); this is **candidate 3, the
per-window flow invariant**, and the ruling supplies the one thing that candidate was blocked
on. Candidate 3's stated cost was that it *"requires a machine-readable window BOUNDARY, and
`window_metrics.py` explicitly refuses to supply one"* — that refusal is correct and stands
(`[#461]`: a computed-looking number there would launder an estimate into a measurement). The
ruling does not overturn it; it supplies the boundary from a **committed fact that already
exists** — the handoff seal SHA — so the boundary is read, never estimated.

The **deferred-row exclusion** answers candidate 2's named loophole in the other direction:
there, `· DEFER` on a row would have been a legal way to satisfy an open-count gate, so a batch
deferral of 29 rows would have read as a 29-row shrink. Excluding deferred rows from the flow
metric removes the incentive; the **one-time batch review** is the companion constraint that
stops the exclusion from becoming a parking lot.

**No gross-count target** is explicit and load-bearing: candidate 4 (a dated number checked by a
human) is rejected, and so is any invented level. Flow is the only thing measured.

**FIRST APPLICATION — 2026-08-04, and it reported RED.**

| | |
|---|---|
| boundary (prior seal) | `80dd54d6` — `docs/handoffs/2026-08-01-dev-knowledge-architect-2` |
| boundary (this window's seal) | the seal cut at this window's close |
| closed | **3** — `[#479]` superseded · `[#472]` · `[#465]` |
| filed | **5** — `[#481]` `[#482]` `[#483]` `[#484]` `[#485]` |
| verdict | **RED** — `closed >= filed` is false at 3 ≥ 5 |

**The verdict stands.** It was reported as RED at the window's wrap rather than reconciled,
softened, or re-scoped, and the rule is recorded here *with its own first failure attached*. A
rule whose first application is quietly excused is not a rule; the honest first data point is
part of what is being ratified. Three of the five filings (`[#481]` `[#482]` `[#483]`) are
residue of work that shipped in the window; two (`[#484]` `[#485]`) are operator-directed
carries. Paying the debt is the next window's opening obligation, not a footnote here.

## G. Handoff v6 scope note (for the [#446] window, informational)

Operator expects v6 to carry: PLAN.md in-process, standardized prompt methodology (no more
hand-writing do-nots — contract + templates make every browser seat emit the same prompt
shape), and the worktree de-emphasis already ruled (fat-prompt default; parallel only behind
the four-condition test — operator confirms the practice matched this ruling).

## H. Portability probe (provider-independence, witnessed not declared)

The fleet's strategic property is model-independence: providers are swappable cards, the
methodology is the motherboard (witnessed already: sol produced the v6 spec, terra reviewed,
CC built, the cloud lane ran nights — no model owns the process). What is missing is the
TEST. Proposal: after [#446], run ONE full arc with a non-Claude builder (natural first
candidate: grok/Codex on the same fat-prompt + frozen contract, terra review, operator as
serial gate). PASS → record "portability witnessed" as a repo fact. FAIL → every silently
Claude-specific element (skills, stop-hooks, prompt formats) files as universalization debt.
This probe and §C's grok shadow are the same first step — sequence them as one.

## I. Sequencing note — how this intake fits the APPROVED 2026-07-31 plan (v2, R1–R6 folded)

**This intake changes NOTHING in the running [#446] window.** The plan of record is approved
and executes as written; the outgoing seat reviewed it and re-affirms: zero amendments. The
intake's items hook into already-existing beats, in this order:

1. **During [#446]:** nothing from here is in scope. (§G is informational only — it matches
   what the plan already builds. §D's repomix is NOT injected into the boot build.)
2. **At [#446] close (Step 10's educate beat / the next consolidation touch):** ingest this
   intake per the convention (SEED, next free intake-id), exactly as intake #21 was ingested.
3. **First ruling batch after [#446]:** ratify §A (decision routing) + §B (standing
   standards) — these are XS prose rulings; §D files its three research-consumption rows
   (grep-first to confirm none exists).
4. **Immediately after, as one step:** §C grok shadow = §H portability probe, first arc.
5. **At 08-26 planning:** §F enters as the cluster's functional requirement ("backlog must
   shrink"), alongside the already-gated §3.2-vs-[#364]-4(a) reconciliation; §C's Gemini
   activation waits for its #383/L4-era consumer per ADR-105.

Rationale for the operator in one line: the continuous plan you have held for several
sessions stays intact — this document only gives names, dates, and one cheap test to the
things that were living in chat memory instead of the repo.
