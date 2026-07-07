# ADR-98: Intake pipeline — functional/technical/developer modes turn operator intent into a decomposed epic set

- **Status:** Accepted
- **Date:** 2026-07-07
- **Decision tier:** Architecture (Path A — direct operator ruling, 2026-07-07 architect ratification session)
- **Related:** ADR-28 (three-layer authority model — "the operator pasting a prompt IS consent", moved one step earlier here), ADR-97 (tree orchestration — the epic-lane / §14a handoff this feeds), ADR-87 (architect↔CC equilibrium contract), ADR-95 (AI-council query lane-split — the functional/technical split is the same frames-vs-expands shape), ADR-66 (BACKLOG story-map — the decomposition target), #162 (the architect actor-vs-mode vocab-collision class this rename touches), PLAYBOOK §2 (Creating a Claude Code prompt — the consumption-spec this sits before)
- **Intake:** #1 (born substantially from operator intake brief #1 — the `functional-architect-nightly-loop` doc, intake-id 1; backfilled per the 2026-07-07 traceability amendment below)
- **Decommission:** none
- **Source:** 2026-07-07 architect ratification session (operator ruling R1); consumes the draft `docs/audits/2026-07-07-DRAFT-intake-process-design.md` on branch `drafts/2026-07-07-proposals` @ `3da29ea` **by ratification, not by merge** (tag `archive/drafts-2026-07-07`); superseded-in-part by operator intake brief #1 (uploaded, lands in-repo in Arc 2). This ADR satisfies the draft's "does this need an ADR?" requirement (draft §5 Q5).

## Context

A raw operator ask ("I want X") reaches an architect (HANDOFF_PROCESS §13) or an epic lane (§14a) with no defined step that turns *intent* into a *decomposed, contracted work-set*. The architect improvises the decomposition inline. Two gaps (draft §1):

- **No requirements-capture step.** The "why / for whom / done-looks-like" of a new initiative is captured ad-hoc in a prompt, not a durable, re-readable, reconcilable intake artifact — the same class the strategic supplement closed for *handoffs*, left unclosed for *initiatives*.
- **No named hand-off from requirements to structure.** The jump from "here's what I want" to "here are the backlog items + ADRs + §14a epic handoffs" is one undifferentiated act with no seam to inspect when it goes wrong (mis-scoped epic, missing ADR).

The 2026-07-07 architect session ratified a shape for this pipeline. Where the draft recommended a role-*progression within one chat*, the ruling went to **modes** (a `--mode` profile mechanism), and the operator's uploaded **intake brief #1** (Arc 2) supersedes the draft in part. This ADR records the ruling; Arc 2 (the intake-scene build, BACKLOG #268) documents the full chain and creates the artifacts.

## Decision

### 1. Three roles, expressed as MODES (not persons, not separate chats)

The single "architect" act splits into three roles, each a boot **mode / profile**, not a distinct human:

- **Functional architect — `--mode functional` (NEW).** Minimal boot, **no probes**. Its sole product is an **intake doc** (requirements, users, done-looks-like, constraints, non-goals). It **never solutionizes** — it captures WHAT/WHY, not HOW.
- **Technical architect — `--mode architect` (EXISTS).** Consumes the confirmed intake doc and produces the decomposition: BACKLOG items (ADR-66 story-map), any ADRs the initiative forces, and one §14a EPIC handoff per parallelizable epic (ADR-97 file-boundary discipline). Decomposition doctrine (§13d, ADR-97) is unchanged — intake only adds the requirements-capture step *before* it.
- **`--mode developer` (renames the existing epic mode, ADDITIVELY).** The epic-lane executor mode (HANDOFF_PROCESS §14 / ADR-97) is renamed `developer` **alias-first**: `developer` is added as an alias now; any deprecation of the old name is **later**. **§14 must not break.**

### 2. Terminology — defined once (rule stated here; PLAYBOOK documents the chain in Arc 2)

- **developer = the mode / profile.** **epic lane = the unit of work** (ADR-97). A developer *works on* an epic lane. The two terms are **cross-referenced, never synonyms.** (Same collision class as #162; the canonical definition lands in PLAYBOOK in Arc 2, not here — this ADR states the rule.)

### 3. Demarcation — the three artifact genres (the operator's ratified boundary)

- **Intake doc = WHAT / WHY** — problem, scenarios, requirements, **ex-ante acceptance criteria**. (0..1 per initiative; the requirements spine.)
- **ADR = the DECISION at a genuine fork** — authored **only** when a reasonable person could choose otherwise **and** reversal is costly. **0..n per intake** (an intake may force no ADR, or several).
- **Backlog epic = the WORK** — **1..n per accepted intake**; each epic entry **cites its intake-id + ADR-id(s)**.
- **Acceptance criteria copy VERBATIM** from the intake doc into the epic UAT (no re-derivation between the two — the intake's ex-ante criteria *are* the epic's acceptance test).

### 4. The intake doc is a confirm-gated artifact (folded from the draft)

The intake doc is a **real, confirm-gated artifact**, not an advisory note: the **operator approves the draft intake doc before it lands** (draft §5 Q3 resolved toward gated). This is ADR-28's "operator consent" moved one step earlier — consent attaches to the confirmed intake doc, before decomposition.

### 5. The intake↔epic edge is advisory until n=2 (folded from the draft)

A §14a epic handoff **citing a confirmed intake doc** is a coherence edge that stays **advisory until two intake docs have been consumed end-to-end**; only then is hardening (a required-linked-intake gate) decided. This is the n=2 evidence discipline — the gate must earn its keep before it becomes a gate.

### 6. Rent rule — the functional scene pays rent

The functional scene is subject to the same **rent discipline every routine carries**: it names its **consumer + survival metric ex-ante**. If intake docs go **unconsumed after ~1 month of operation**, the scene is **reviewed for removal** (the justify-or-retire / fleet-audit lesson — a scene with no consumer is dead weight, not permanent infrastructure).

### 7. Feed — `/changelog-review` seeds intake

`/changelog-review` **ADOPT** and **OBSOLETES-WORKAROUND** outputs land in `intake/` as **`status: SEED`** (a pre-intake candidate the functional architect can pick up). This is the standing feeder into the functional scene (operator intake brief #2, R1).

### 8. Scope boundary for THIS arc

`intake/` is **NOT created here.** Folder creation (and any new top-level area) rides the **Arc 2 intake-scene build (#268)** with its own folder-approval; this ADR records the decision only.

## Consequences

- **Easier:** initiative requirements become a durable, confirmable, re-readable artifact with a named seam to decomposition; a mis-scoped epic or missing ADR now has an inspectable failure point (the intake doc ↔ decomposition boundary).
- **Cost / mechanism (deferred to #268):** a `--mode functional` boot profile, `--mode developer` as an additive alias of the epic mode, an `intake/` area + `templates/intake-template.md`, and the PLAYBOOK chain documentation. Capture precedes construction (ADR-70 pattern) — this ADR is the record; #268 is the build.
- **What this does NOT decide:** whether the intake↔epic edge hardens to a gate (advisory until n=2); the deprecation timing of the old "epic mode" name (alias-first, later); the intake-doc / strategic-supplement template-sharing question (draft §5 Q4, left open). None of these are ruled here.
- **Authority model preserved:** consent still attaches at an operator-confirmed artifact (ADR-28), only earlier; the technical architect's decomposition (ADR-97 §13d) and Layer-2's no-orchestration boundary are untouched.

## Alternatives considered

- **Three roles as a role-progression within ONE architect chat** (the draft's §6 recommendation). Not adopted: the ruling chose explicit **modes** (a `--mode` profile mechanism) so each role has a clean, named boot contract — the functional role's "no probes, intake-doc-only, never solutionize" profile is a real boundary, not a hat worn mid-conversation.
- **Three distinct browser chats** (draft §5 Q1, the maximal-ceremony option). Not adopted: modes give clean seams without a chat-per-role's handoff overhead; the tree-orchestration split (ADR-97) already handles the epic-lane fan-out.
- **Leave requirements capture ad-hoc (advisory note).** Rejected: an un-confirmed, non-durable note can't be reviewed or reconciled later — the exact gap this closes; the intake doc is confirm-gated precisely so consent and re-readability attach to it.
- **A new epic-mode name that breaks §14.** Rejected: the rename is additive (alias-first) so no existing §14 handoff or ADR-97 lane breaks on day one.

## Amendment — 2026-07-07 (advisory edge → WARN; block-level revisit deferred to n≥4)

§5 set the intake↔epic edge **advisory until n=2** consumed intake docs, then a hardening decision. **n=2 is now met** — intake-id 1 (`functional-architect-nightly-loop` → consumed by #268) and intake-id 2 (`platform-feature-scan` → consumed by #272) both ran end-to-end. Ruling (operator, 2026-07-07 post-triage): harden the edge **one notch — to an advisory WARN, not a block**. A new **L-sized new-feature epic** that lacks an intake-id citation earns a `validate_backlog` WARN; **residual filings (chore/fix follow-ups) and bugfixes are EXEMPT** (they have no intake doc by construction). The WARN is filed as BACKLOG **#279**; this amendment is its doctrine record. **Block-level enforcement stays deferred** — revisited only at **n≥4** consumed intake docs (a second evidence bar before a hard gate, extending §5's n=2 discipline). Additive: §5's advisory-until-n=2 clause stands as the historical basis; the WARN is the next rung, not a replacement.

## Amendment — 2026-07-07 (intake home = `docs/intake/` universal; intake↔ADR traceability)

Two additive rulings from the operator-surface arc; neither disturbs the decision above.

1. **Intake home is `docs/intake/`, a universal fleet convention.** §8 recorded that the folder is created by the Arc-2 build (#268) and left the physical location to that build, which placed it at repository root. Ruling (operator, 2026-07-07): the standing home is **`docs/intake/`** — under the docs/ taxonomy (decisions / audits / handoffs / intake), fleet-wide. The hub folder was relocated `intake/` → `docs/intake/` (history-preserving `git mv`) with every live reference repathed; the 5 dated intake docs stay content-intact — their narrative `intake/` references are captured content, exactly like this ADR's own body above (immutable), and are not rewritten. **Greenfield consumers** inherit `docs/intake/` at methodology deploy. The deploy manifest does **not** yet propagate the intake area or `templates/intake-template.md` (verified: no `intake` reference in `deploy/manifest-v*.yaml`), so that propagation gap is filed as **BACKLOG #280** rather than silently assumed — deploy-manifest work is out of this arc's scope.

2. **Intake ↔ ADR traceability convention.** `templates/adr-template.md` gains an optional **`Intake:`** field and the rule: **an ADR born from an intake doc MUST cite its intake-id.** This makes the docs/intake ↔ ADR edge inspectable from the ADR side, complementing §3's intake-id citation on the epic side. **Backfill:** this ADR — born substantially from operator **intake brief #1** (the `functional-architect-nightly-loop` doc, intake-id 1; see Source) — is stamped **`Intake: #1`** in its header as the convention's canonical first example. **ADR-99 and ADR-100 keep their `drafts/2026-07-07-proposals`-branch provenance** (they were not born from a numbered intake doc — no id is fabricated). The header-field backfill is recorded here for immutability transparency (§5 rule 3): it is a metadata backfill establishing the new convention, not a decision-content edit. The intake↔ADR edge is **advisory** (a convention, not a gate) — consistent with the §5 / n=2 edge-hardening discipline; no new enforcement organ is created here.
