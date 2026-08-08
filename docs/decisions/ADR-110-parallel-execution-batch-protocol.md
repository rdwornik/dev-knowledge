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

---

## Amendment — 2026-08-06: the operator directives of the same day now have an in-repo carrier

**Not a new decision.** This addendum records where five operator directives issued on
2026-08-06 came to rest, so a later reader looking for them opens a file rather than a chat.
The body above is unchanged.

At the time §7 was written ("this ADR arms no gate … until the row lands, the protocol is as
memory-resident as it was before"), five directives from the same window had no in-repo home.
They now have two between them — intake #27
(`docs/intake/2026-08-06-tech-adoption-consolidation-intake.md`) as the ledger, and the
PLAYBOOK Ch8 section [#505] landed as the doctrinal home:

| Directive | Where it now lives |
|---|---|
| **Rhythm** — WINDOW = BATCH; the seal fires at true batch boundaries, not mid-batch | PLAYBOOK Ch8, "The batch protocol" |
| **Transport** — 2 touches on *both* seams: operator↔batch (GO · end-of-batch packet) and browser↔operator (batched packets; single-question round-trips reserved for ask-class (a)–(c)) | PLAYBOOK Ch8, "The batch protocol"; the (a)–(c) classes are `protocols/STANDING_RULINGS.md` "The decision budget" |
| **Ceremony** — V-3 tiering, with the S-contract floor carrying JOURNAL as a fixed final step | PLAYBOOK Ch8, "The batch protocol"; per-Scale detail stays in `templates/prompt-template.md` |
| **Process-lane cap** — from batch 2 onward, ≤1/4 of a batch's lanes target methodology/hub-process surfaces; a shortfall is reported rather than backfilled | PLAYBOOK Ch8, "The batch protocol" |
| **`pytest -n auto` authorization** — adopted on a measured 5.2× divergence (serial 1785.61s vs 358.77s / 330.15s, identical pass/fail/skip), landed as `addopts = "-n auto"` at `d11dda35` | `pyproject.toml`; the eval record is `protocols/STANDING_RULINGS.md` E1 |

**What §7's honest limits still say, and still correctly.** The first — *this ADR arms no
gate* — is unchanged by [#505]: the two organs that landed are advisory by ruling
(`audit.py::check_stale_worktrees` is WARN-tier, `scripts/validate_branch_naming.py` is wired
into no gate at all), and the refuse-to-finish refusal is carried by the `/lane-integrate`
checklist rather than by machinery. The third — *§2's 4–10 range is a design target, not a
measured ceiling* — is likewise unchanged: no batch above 3 has run, and the artifacts are
parameterized for N rather than validated at N.

The second limit is the one this addendum narrows. The AM-1/AM-2 provenance is still off-repo,
but the five directives above are no longer memory-resident: each has a file a later reader can
open.

---

## Amendment — 2026-08-07: the declared integration arc (R-1, adjudicated APPROVED as drafted)

**Status: ratified by architect adjudication 2026-08-07.** Drafted as R-1 in
`docs/audits/2026-08-06-technical-batch1-verification.md` §7, approved as drafted, built in the
PRE-2 arc. The body above and the 2026-08-06 amendment are unchanged.

### The problem, stated structurally rather than as a symptom

A batch's JOURNAL entry names the lane **merge** SHAs, so it is writable only *after* the
merges. Each merge meanwhile lands an unanchored first-parent spine entry, and `audit-health`
evaluates **per-commit**. Anchoring is retrospective; the commit-time backstop is not. The two
cannot both be satisfied between merges.

Batch 1 resolved it with `SKIP=audit-health` on two intermediate merges — surgical, disclosed,
and still a gate turned off by hand at the exact moment the protocol makes it fire. At the
width 6 this ADR's §2 envelope allows, that is five times per batch.

### What was NOT wrong, and is therefore not changed

The pre-push organ `block_unanchored_push.py` discharges **range-level** and was satisfied
normally throughout batch 1. The `journal_spine_anchor` backstop reads the whole spine and was
clean at close. **Only the per-commit evaluation is structurally unsatisfiable mid-queue** — so
only that is addressed.

### Decision

`audit.py::check_journal_spine_anchor` gains a **declared integration arc** exemption. A
first-parent spine entry is exempt when **both** hold:

1. it is a `--no-ff` merge of a `worktree-lane-*` branch, **and**
2. a committed batch manifest declares an **open** batch.

Neither alone. Condition 1 without 2 would exempt any lane merge forever; condition 2 without
1 would amnesty every merge landed during a batch, including the integrator's own `docs/…` arcs.

**Why a manifest is the right key.** It is the only artifact that makes "a batch is open" a
fact in the tree rather than a claim in a chat, and Ch8 already requires it at dispatch — so
the exemption costs no new ceremony. Keying on the branch prefix alone would exempt any lane
merge forever; keying on the manifest makes the exemption as short-lived as the batch.

**How openness expires — and why it is not a mutable `status:` flag.** Manifests live under
`docs/audits/`, which is **immutable** (CLAUDE.md §5 rule 3). An exemption whose expiry
required editing an immutable artifact would either never expire or corrupt the record. So the
manifest declares at dispatch the artifact that will close it (`closed_by:`), and the batch is
open only while that path is **absent** from the tree. The end-of-batch packet landing ends the
exemption automatically, with no edit anywhere. Extending an exemption takes a visible act —
deleting the packet, or committing a new manifest — never silence. A manifest carrying no
`closed_by:` opens nothing, because an exemption with no declared expiry is exactly the
permanent hole the honest limit below warns about.

**The exemption is reported, never applied silently.** When it fires, the check still returns
`pass` but its evidence names the count, the batch, the manifest path, and the packet whose
arrival will end it. A skipped entry a reader cannot see is the failure this gate exists to
prevent.

### Rejected alternative

**Keeping `SKIP=audit-health`.** It disables **every** check in the registry, not the one that
cannot pass, and it trains the reflex the ADR-85 amendment 2026-08-03 exists to remove.

### Scope — what this does not touch

The range-level pre-push leg and the whole-spine per-entry scan are unchanged, so **nothing
ships unanchored**; the anchor obligation simply lands where it is satisfiable. Enforced
structurally rather than by intent: `scripts/block_unanchored_push.py` and
`scripts/journal_anchor.py` do not import `scripts/batch_manifest.py`, and
`tests/test_batch_manifest.py::test_the_pre_push_organ_does_not_consult_the_manifest_at_all`
asserts that on the AST — a behavioural test would pass only for as long as no input happened
to reach a manifest read.

### Honest limits

- **This adds a second exemption surface to a gate whose value is having none.** Accepted
  deliberately, weighed against the state it replaces: a documented instruction to turn the
  whole registry off twice per batch, five times at width 6.
- **The merged-branch name is read from the merge subject** (`Merge branch '<name>'`), which is
  what `git merge --no-ff` writes and what `/lane-integrate` produces. A hand-written merge
  message omitting the branch name is not recognised as a lane merge — it fails **closed** (no
  exemption), the safe direction.
- **The exemption is not scoped to the lanes the manifest enumerates.** Any `worktree-lane-*`
  merge qualifies while a batch is open. That is the draft as approved — its stated concern is
  temporal, not per-lane. Tightening it to declared lanes is a separate decision, recorded here
  so it is a visible choice rather than an oversight.
- **Unverified at width 6.** The mechanism is tested at the unit level and against real git,
  but no batch above 3 has run. Batch 2 is its first live exercise, and is also the first test
  of [#505] clause 1 (a fresh seat running a batch from committed artifacts alone).

## Amendment — 2026-08-08: the process-lane cap is evaluated against dispatched width

The 2026-08-06 amendment's directive table above restates the process-lane cap as "≤1/4 of a
batch's lanes target methodology/hub-process surfaces" without naming the width that fraction is
taken over — which is the one thing a batch needs to know to apply it. Operator-ratified
2026-08-08: **the cap is evaluated against dispatched width; the end-of-batch packet reports the
close-width delta.**

**This is an amendment note, not an edit.** The table row above stands as written; where the two
are read together, this section governs. The doctrinal home for the cap remains
`protocols/PLAYBOOK.md` Ch8, "The batch protocol", which carries the ratified sentence verbatim;
the ledger record is intake #27's "Ratification amendment — 2026-08-08".

**Scope — denominator only.** The 1/4 fraction, the from-batch-2-onward start date, the
report-the-shortfall-and-run-narrower behaviour, and the no-backfill rule are all unchanged by
this amendment.
