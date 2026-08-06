# ADR-110: Parallel multi-agent execution — batch protocol as versioned artifacts

**Status:** Accepted (operator GO 2026-08-06, on SESSION PLAN v2 §3 — acceptance granted in-session)
**Date:** 2026-08-06
**Decision tier:** Methodology (way-of-working — how parallel multi-agent work is provisioned, contracted, and closed)
**Decided-by:** operator (GO 2026-08-06); architecture ruled in the 2026-08-06 consolidation window, red-teamed by the predecessor riders
**Intake:** #26 (`docs/intake/2026-08-06-func-parallel-execution-system.md`) — ACCEPTED, `disposition: active`
**Related:** [#429] (FLEET worktree portability — a **complementary, non-overlapping** concern; cross-referenced both ways, scopes deliberately NOT merged) · intake #25 / W-10 (provider-agnostic execution layer — a separate pipeline, explicitly out of scope here) · [#501] (report-only recorder; no gate promotion follows from this ADR) · ADR-98 (the intake pipeline this promotes from) · ADR-105 (named-consumer discipline, binding on the hygiene organ) · ADR-106 (`uv` environment isolation — the mechanism lesson (iv) below rests on)
**Amends:** none.
**Decommission:** none. Nothing is removed by this decision.
**Source:** 2026-08-06 consolidation window — the supplement ADDENDUM *"Parallel-management architecture RULED this window (do not relitigate)"* at `docs/handoffs/2026-08-06-dev-knowledge-architect/PASTE_THIS.md` (folded from that bundle's `SUPPLEMENT.md`), plus the predecessor ratification AM-1/AM-2. The AM-1/AM-2 ratification itself is **off-repo** (operator's Downloads, SESSION PLAN v2); intake #26 is its in-repo carrier, and this ADR cites the intake rather than claiming an in-repo locator that does not exist.

## Context

Parallel multi-agent execution is **already how work gets done here** — the 2026-08-06 window
cut a three-lane batch with an integrator and named a wider batch 2. What it is not is
**repo-encoded**. The batch shape (lanes, contracts, budgets, integrator, teardown) lives in
seat memory, so it does not survive a fresh seat and it does not survive a compaction.

Intake #26 records the three witnessed consequences: unclosed parallel work (stale worktrees,
unmerged lane branches — the operator's stated #1 pain), per-lane environment errors, and zero
portability of the way-of-working. The environment error is the sharpest, because it is silent:
a bare `pytest` inside a worktree lane inherits `VIRTUAL_ENV` from the primary tree and reports
green about **the wrong source**.

This ADR is a **transcription** of decisions already taken. It re-opens nothing. The
alternatives in §4 are recorded with the reasons they were rejected with, not re-argued.

## §1 — Decision: adopt-native, and encode the protocol as versioned artifacts

Two rulings, taken together because either alone is insufficient.

**Adopt-native.** The execution substrate is Claude Code's own primitives — `claude --worktree`,
the agents view (`claude agents`), and the native `/batch`. The fleet builds no execution
engine of its own.

**Protocol-as-versioned-artifact.** The batch *protocol* — which native primitives alone do not
supply — lives in the repo as versioned artifacts, so no seat depends on memory. Per intake #26
Track 1, the artifact set is:

1. **PLAYBOOK §** — the batch protocol: ONE plan → N file-disjoint lanes → ONE integrator;
   frozen per-lane contracts + V-2 decision budgets; `uv run --locked` mandatory per lane;
   commit-and-STOP, never self-merge; serial integration from the primary; exactly 2 operator
   touches per batch (GO · end-of-batch packet).
2. **Project-scoped `.claude/commands/`** — lane-boot and integrator commands, so no seat
   re-derives the shape.
3. **Handoff-bundle pointer** — successor bundles point at the protocol rather than restating it.
4. **Hygiene organ** — WARN on stale worktrees (the mechanized weekly prune stays).
5. **Lane/branch-prefix enum** — validator-checked naming.

The two rulings are coupled by design: adopt-native without an encoded protocol reproduces the
memory dependency on someone else's primitives, and an encoded protocol on a bespoke engine
buys the maintenance cost the adopt-native ruling exists to avoid.

## §2 — Lane-count parameterization: drilled at 3, designed for 4–10 (AM-2i)

The batch-1 drill runs **3 lanes**. Every artifact in §1 is written for **N**, with a designed
range of **4–10** — provisioning, the board view, and the integrator queue assume N, never
three.

The distinction is deliberate and is the whole content of this clause: **3 is the drill size,
not the design size.** An artifact that hard-codes three passes batch 1 and then has to be
rewritten for batch 2, which is the failure this parameterization forecloses. The Q2 tension
was weighed and staging won — *"3 lanes drill the machinery; width without a proven integrator
is risk, not speed"* — so the narrow first batch is a sequencing decision about **execution**,
not a constraint on the **design**.

## §3 — Refuse-to-finish integrator checklist as a mechanical close-out (AM-2ii)

The integrator close-out is **encoded in the artifacts themselves**, structurally unable to
close while any item is open. The four conditions, from intake #26 Track 1 item 7:

- every lane branch merged-or-explicitly-abandoned
- full suite run once on the merged result
- `git worktree list` == primary only
- manifest/packet archived

This is the direct mechanization of the operator's #1 pain. The load-bearing word is
**mechanical**: a checklist an integrator can read past and still declare done is the state that
already exists. "Explicitly abandoned" is a recorded disposition, not silence — a lane branch
with no verdict leaves the checklist open.

This clause arms no gate on its own. Which organ carries the refusal — a command, a validator,
or a hook — is build-time design, owned by the row this ADR authorizes.

## §4 — Alternatives considered and rejected, with their recorded reasons

Transcribed from the ADDENDUM's *"Rejected with reasons"* list. Recorded so they are not
re-derived; not re-argued here.

| Rejected | Recorded reason |
|---|---|
| Hand-rolled `/batch-*` commands | native `/batch` exists |
| Web-UI-outside-VS-Code as the primary surface | rejected as primary surface |
| tmux | WSL — and WSL is excluded by operator constraint |
| Copilot-gated Agents window | Copilot gating |
| Bespoke board (intake #26 non-goal) | folded into the same rejection as hand-rolled `/batch-*` |

**`herdr` is watch-listed, not rejected** — recorded as a *"terminal multiplexer candidate if
the native board stops sufficing"*. It carries no work and no row; it is a named re-entry
condition.

Two adjacent rulings from the same window bound this ADR's reach and are recorded so they are
not read as open:

- **The VS Code Agents window is adopted as cockpit and ruled NEVER load-bearing** (Q2 tension
  (e)) — *"optional sugar on unchanged mechanics"*; lane discipline comes from the contract and
  the gates, not from a UI.
- **No provider-agnostic execution layer here.** That is intake #25 / W-10, a separate pipeline.

## §5 — Track 2: the Vibe Kanban eval is a gate, not a build

Track 2 authorizes an **evaluation**, and births nothing. A 30-minute eval of Vibe Kanban with
its official VS Code extension (`bloop.vibe-kanban`), run operator-parallel during the batch-1
drill.

**PASS criteria, pre-named** (the point of pre-naming them is that the verdict cannot be
retrofitted to the experience):

- in-IDE tasks / logs / diffs
- full lifecycle including worktree **CLEANUP** verified
- a second provider (Codex) on one card
- headless server as a VS Code task

Version pinned in win-tooling config-as-code. **Sunset-to-community risk is accepted because
lock-in is zero.** The verdict is wanted BEFORE the wide batch. If the eval PASSes, its ADOPT
verdict files its own follow-up row — this ADR pre-authorizes no build against it.

## §6 — Scope boundary: what this ADR does NOT decide

- **No re-scope of [#429].** Its live body owns FLEET worktree portability (a portable
  seed-manifest stated once in the hub, plus a per-worktree venv so imports follow the
  checkout). This ADR is **hub-scoped protocol encoding**. The two are complementary and are
  cross-referenced in both directions; the scopes are not merged. The window's own ADDENDUM
  used the shorthand *"[#429] slim scope"* for what became Track 1 items 4–5; intake #26 —
  the later and ACCEPTED artifact — names that point and rules it explicitly, so the intake
  governs and [#429] receives a cross-reference only.
- **No gate promotion of [#501].** GitHub tier is Free and the repo is private by standing
  ruling, so report-only stands.
- **No provider-agnostic execution layer** (intake #25 / W-10).
- **No choice of enforcement organ** for §3's refusal — build-time design.

## §7 — Honest limits

- **This ADR arms no gate.** It is doctrine plus an authorization to build. Until the row lands,
  the protocol is as memory-resident as it was before — the ADR records the decision, it does
  not implement it.
- **The AM-1/AM-2 provenance is off-repo.** SESSION PLAN v2 lives in the operator's Downloads.
  Intake #26 is the in-repo carrier and is what a later reader can actually open.
- **§2's 4–10 range is a design target, not a measured ceiling.** No batch above 3 has run. The
  Q2 record already notes a separate ~10 work-lane ceiling and a 2–3 epic-lane cap as
  *different axes*; nothing here reconciles them.
- **§3's "mechanical" is a requirement, not a delivered property.** The mechanization is the
  row's work and its acceptance test.

## Consequences

**Easier.** A fresh seat boots a batch from repo artifacts instead of inheriting a shape by
conversation. Lane environment correctness stops depending on whoever remembers `uv run
--locked`. The close-out that has been the #1 pain becomes a checkable condition rather than an
intention.

**Harder.** The protocol becomes a maintained surface with the coupling cost every doctrine
surface carries — the Finding-1 lesson of the same window (touching doctrine surfaces without
their coupled updates has a price) applies to it directly.

**Unchanged.** The execution substrate: native primitives, no bespoke engine. The gate mesh:
this decision adds no gate and removes none.
