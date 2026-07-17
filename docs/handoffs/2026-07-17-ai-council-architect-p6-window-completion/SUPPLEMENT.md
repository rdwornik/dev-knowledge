# Architect strategic supplement — 2026-07-17-ai-council-architect-p6-window-completion

Repo: ai-council (bundle hosted in the hub .dev-knowledge) · Mode: architect · Date: 2026-07-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **STATUS: FILLED (2026-07-17)** — authored by the outgoing #26-session CC (which drove the P4-wave close), so the incoming §13(d) beat narrows to *"anything changed since?"*.

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo.

## ANSWERS

1. **Strategic intent.** Complete the delegation window. The P4 wave built the *council-side* machinery (doctor, CLI seats, verdict package); the way-of-working goal now is to make the ADR-11 contract **honest and versionable** — empty CONTRACT §7's known-deviations so the surface can carry `Contract-Version: 1.0`. A versioned CLI-as-ABI is the whole point of ADR-11; a `1.0` that ships with known deviations would be a lie (L-INT Q7). Small build, high closure value.

2. **Tensions weighed.** (a) *Scope of #26's "witnessed run"* — a synthetic emission vs a real LLM debate. Landed on a **real debate** (twice: once pre-terra-fix, once on shipping code) because binding closure evidence to code that never ships is the easy-proxy failure the contract exists to block. (b) *Terra gate vs codex rate-limit* — landed on an **explicit recorded waiver + filed follow-up (#33)**, offset by fresh empirical re-witness, never a silent skip. (c) *"zero added lines to save_to_file"* vs the mandated mirror block — the architect **amended the contract** to "all content-building in helpers/sibling; save_to_file stays pure orchestration + at most the package/mirror calls," and the mirror folded into `_build_header`.

3. **Considered + rejected.** (a) Verdict package as a *sidecar extension* — rejected; it is a separate caller-facing deliverable, consuming `seats[]`/`synthesis` by reference (a terra-Critical forced the shared `_seat_payload` serializer so no parallel seat schema drifts). (b) *Inventing a `contract_version` value* for #26 — rejected; emit `null` until the D2 deviations empty (that emptying is exactly this next session's job). (c) *Council-side batch / multi-question* — rejected (L-INT Q5, settled); caller-side decomposition (RIDER 2 / #37) is the sanctioned form.

4. **Open questions (deferred).** The DRAFT-INT-2 `1.0` *stamping moment* is defined (at §7-empty) but not executed — it is this session's to perform once #22/#23 land. Whether #22 truly "falls out of" the already-landed A2 decomposition or needs its own wiring is unverified — check the live `cli.py` `@click.group` state first. #34 (research-path parity) is the one place the verdict package is not yet lane-complete.

5. **Decomposition rationale.** #22 before #23 is not mandatory — they are disjoint (`cli.py` `--file` path vs `run_research`). #22 is expected smaller (structural basis exists post-A2). Do NOT re-derive the verdict-package design or the seam contracts — they are settled and shipped. Do NOT re-plan Codex-as-producer (interim fallback in force). The `1.0` stamp is the *joining* step after both parity fixes — sequence it last.

6. **Off-repo context.** P4 wave closed cleanly on 2026-07-17 (three merges, all terra-reviewed; #26's pass-3 the only waived residual, date-gated 2026-07-23). G3 (#24 operator blind-scoring) remains the operator's open mission and gates Epic B — pause-independent. P5 (#27 CLI-4 parity) is now *runnable* since #16 landed. RIDER 2 filed the caller-side advisor story [S13]/#36–#38 (filing only). No priority shift signalled beyond "complete the window"; confirm live.
