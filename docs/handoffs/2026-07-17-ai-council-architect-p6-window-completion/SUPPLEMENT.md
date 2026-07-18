# Architect strategic supplement — 2026-07-17-ai-council-architect-p6-window-completion

Repo: ai-council (bundle hosted in the hub .dev-knowledge) · Mode: architect · Date: 2026-07-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **STATUS: FILLED (2026-07-17)** — authored by the outgoing session CC (P4-wave close → unattended night E2E audit → supervised morning close), so the incoming §13(d) beat narrows to *"anything changed since?"*.

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo.

## ANSWERS

1. **Strategic intent.** Shift from build-wave *governance* to *completion + evidence*: empty CONTRACT §7 (#22/#23) so the ADR-11 surface can carry an honest `Contract-Version: 1.0`, harden the artifact surface (#39–#43), then run #27 parity to *earn* the ADR-12 §5 cost-lane default flip. A versioned CLI-as-ABI is the whole point of ADR-11; a `1.0` that ships with known deviations would be a lie (L-INT Q7). Epic-B design (#18/#19) gets its **own** planning session on the now-un-gated baseline.

2. **Tensions weighed.** (a) *Evidence vs operator authority on G3* — **resolved by authority**, de-risked by the retained sealed EPI-1 pack + the night batch's **4/4 empirical corroboration** of openai synthesis; the ruling-over-scoring path was chosen deliberately to spend the scarcest resource (operator scoring time) wisely. (b) *Terra outage vs review discipline* — **explicit recorded waivers, never silent passes**; #33 is the dated backstop (codex credits reset 2026-07-23). (c) *Unattended autonomy vs safety* — a **pre-authorized night batch with hard stop conditions** held (zero fired).

3. **Considered + rejected.** (a) *Re-running the LLM-judge over EPI-1* — rejected: moot-by-ruling and a duplicate of the existing second-opinion note. (b) *Extending the night batch into code fixes* — rejected: doctrine is **no unattended edits**. (c) *A fresh bundle instead of updating this one* — rejected: **operator ruling was to update in place** (this bundle). Do NOT relitigate these.

4. **Open / deferred.** The two hub NEEDS-RULING intakes (§3b — codex-producer #341, session-close-gate #343) await operator rulings. The §6.3 scope-boundary fork (pure-governance vs thinking-aid) is unadjudicated. #33 + any terra-gated review are date-gated ≥ 2026-07-23. The **ADR-01 amendment text** for the synthesizer swap is owed if the hub/consumer convention requires a formal amendment. Whether #22 truly "falls out of" the already-landed A2 decomposition or needs its own wiring is unverified — check the live `cli.py` `@click.group` state first. #34 (research-path parity) is the one place the verdict package is not yet lane-complete.

5. **Decomposition rationale.** Sequence is **#22/#23 (empty §7 → `1.0` stamp) → #39–#43 (harden the artifact surface) → #27 (parity → default-flip)**; #18/#19 design is a separate session. #22 and #23 are disjoint (`cli.py` `--file` path vs `run_research`), #22 expected smaller (structural basis exists post-A2); the `1.0` stamp is the *joining* step after both parity fixes — sequence it last. Do NOT re-derive the verdict-package design or the seam contracts (settled + shipped), re-score/re-rule G3 (resolved), or re-plan Codex-as-producer (interim fallback in force, §3c).

6. **Off-repo context.** Operator priorities unchanged — **delegation window first**, **CLI cost-lane second** (flip pending #27), **debate quality third** (now un-gated). Operator scoring time remains the scarcest resource — the ruling-over-scoring G3 path was chosen deliberately for that reason. No priority shift signalled beyond "complete the window"; confirm live.
