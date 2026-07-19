# EPIC HANDOFF — e5-registry · 2026-07-18
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | 2026-07-18-corp-monorepo-e5-registry-developer |
| **Chat title** | `[corp-monorepo] Developer e5-registry · SEQ 1` — name the fresh epic chat this (bump `SEQ` per parallel chat) |
| **Mode** | **epic** — one epic end-to-end, inside a root-provisioned worktree (ADR-97; HANDOFF_PROCESS §14a) |
| **Repo** | corp-monorepo |
| **Date** | 2026-07-18 |
| **Epic branch** | `epic/e5-registry` (root-provisioned; bundle generated on `docs/adr-101-two-tier-new-path-rule`) |
| **Execution mode** | root-declared in §Execution MODE below (mandatory — §14a item 7) |

## Boot (epic lane)

You are an **EPIC-CHAT lane** (HANDOFF_PROCESS §14a; ADR-97). The root architect owns ADR
acceptance, backlog structure, parallelism rulings, and ALL merges to main. On load reply:
"Epic lane e5-registry booted — worktree + boundary acknowledged."

## Worktree + branch

Worktree `epic-e5-registry` (root-provisioned — never self-provisioned) · branch
`epic/e5-registry`. **RELATIVE PATHS ONLY** (the absolute-path-bypasses-worktree lesson is a
hard rule). Commit-per-story; **commit-and-STOP** — no merges to main.

## Epic scope (the BACKLOG slice)
<!-- FILL-IN:scope START — ROOT authors: epic id · stories in order · done-when per story -->
**Epic:** E5 registry — the FR-10 source-value registry foundation (theme `[E5]` Knowledge loop; design `docs/intake/2026-07-17-tech-e5-registry-foundation-design.md`, ratified READY-FOR-TECHNICAL 2026-07-18, §8.1). Build order per design §6, the **FR-10 slice only** (`#35` `ContentRegistry` routing gate is a SEPARATE registry — OUT of this lane, see FILE-BOUNDARY):

1. **#38** [P2][M] — FR-10 source registry: schema + observation model + deterministic scorer (design §2; single-pass neighbour prior; golden vectors). **Done-when:** every registry record carries a `value_score` (struct: score + components + `weights_version` + `score_as_of`) and the scout's queue consumes it.
2. **#40** [P1][S] — Registry day-1 seed: the three operator golden sources (Cognitive Fridays · BY Product Documentation · BY Platform). **Done-when:** the three seeds resolve via **Graph METADATA listing only**; the scout NEVER filesystem-traverses the synced "OneDrive - Blue Yonder" tree (hydration invariant, core-invariant #1). *Record drafting is consent-free; LIVE resolution is BLOCKED-on-operator (Graph consent, decision G).*
3. **#36** [P1][L] — Scout foraging pilot (FR-11) with a bandit-governed queue. **Done-when:** the scout runs a pilot cycle and the bandit queue orders candidates by predicted yield. *Day-1 queue = deterministic `value_score` rank (bandit is the cycle-3+ upgrade, design §2.4). depends-on `#35` (routing gate, OUT of this lane) + BLOCKED-on-operator (Graph consent).*
4. **#55** [P2][S] — Content-Manifest producer (the epic's deck-facing tail). **Done-when:** the producer emits a DRAFT-schema manifest entry (FR-20 unratified → mark draft) for one sandbox note, witnessed.

Ratified inputs (§8.1): D3=A paste-back ratification · D4=A explicit-pick archive trigger · D5=A equal weights day-1 (`weights_version` recorded). `#36` is L-sized → plan-first per §Execution MODE.
<!-- FILL-IN:scope END -->

## Epic done-contract (ex-ante, immutable to this lane)
<!-- FILL-IN:done-contract START — the hard closure metric for the WHOLE epic -->
#38 + #40 + #36 + Content-Manifest tail each meet their BACKLOG done-when; registry + scoring operate deterministically (v1 weights per D5 pick, `weights_version` recorded); scout ratification flows per the D3 pick; end-state witnessed by a sandbox end-to-end run: registry resolves the three golden seed sources, scoring ranks them, one draft manifest entry emitted. **Merged ≠ done; the witnessed run is done.**
<!-- FILL-IN:done-contract END -->

## FILE-BOUNDARY (hard)
<!-- FILL-IN:boundary START — may-touch / may-NOT-touch; disjoint from every concurrent epic -->
**May touch:** the registry/scout/scoring module homes named in intake-16 + their tests + the config file recorded in §8 (D1) + BACKLOG/JOURNAL checkbox-status edits for its own stories. **NOTHING else** — explicitly out: `index_builder`/`query_engine` internals (KE epic's surface), `rfp` module, `docs/decisions`, any new folder. A needed file outside the boundary → STOP, escalate — don't touch.

- **Config file (D1, ratified §8.1):** `config/source_registry.yaml` — existing `config/` folder, **no new path**.

**Anti-pattern (architect rider — VERBATIM):** the registry manages URLs/REFERENCES only — pointers to folders, shortcuts, even shortcuts-to-shortcuts where needed (C++-reference model per DR-12 reference-not-copy). NO deep copy: the lane never copies, mirrors, or relocates source content; any content-copying temptation = STOP to the architect.
<!-- FILL-IN:boundary END -->

## Escalation
<!-- FILL-IN:escalation START — epic-specific triggers beyond the standing set -->
**STOP → architect on (VERBATIM):** any need outside the boundary · any premise contradicting intake-16 or ADR-37 · Graph API behavior diverging from the D2 ruling (SSO user token + refresh, corp-ops precedent) · any deletion temptation · **any content-copying / deep-copy / relocation temptation** (reference-only model — the §FILE-BOUNDARY rider).

Standing set (always): ADR-worthy fork · boundary-breach need · cross-epic dependency discovered → STOP, return to the root. Everything intra-epic is the lane's own judgment.
<!-- FILL-IN:escalation END -->

## Execution MODE (mandatory, root-declared — §14a item 7)
<!-- FILL-IN:exec-mode START — plan / plan-then-auto / auto-accept + its basis; L-sized stories default plan-first -->
**MODE = plan-then-auto (VERBATIM):** plan the first story, return it for the architect's one-form review, then auto within the boundary for subsequent stories. Basis: first developer lane on a young pipeline; one plan-review calibrates, then autonomy.

**Standing refusals (architect, VERBATIM):** no merge to main (commit-and-STOP; EPIC RETURN before merge) · no ADRs · no BACKLOG structure changes · no new folders.

**Codex lanes (architect, VERBATIM):** terra review before the epic's merge (per-story reviews at the lane's discretion, mandatory at RETURN); sol not needed (design already sol-derived); luna free for read-only probes. Part 1 itself: doc-only, no Codex — reason: BACKLOG/JOURNAL edits, no code impact.
<!-- FILL-IN:exec-mode END -->

## Refusals (standing — not editable by the lane)

No merge to main · no ADRs · no backlog structure (checkboxes inside this epic's own block
only) · no worktree lifecycle ops · no new top-level folders · no content deletion without
operator ask.

## EPIC RETURN (required before any merge)

Close the lane by filling `EPIC_RETURN.md` in this bundle (§14b): commits + branch state ·
contract-vs-outcome per story · self-adjudications · proposed BACKLOG delta ·
merge-readiness. The root reviews the return against this contract → serial `--no-ff` merge →
applies the backlog delta → declares closure → tears down the worktree.

## Probes

Boot on `PROBES.md` (this bundle) — live-state probes scoped to this epic's boundary
(HANDOFF_PROCESS §5 contract: question + source-locator + command, **never the answer**).

> **Operator note.** Paste THIS file + `PROBES.md` into the fresh epic chat. Epic mode
> assembles no `PASTE_THIS.md` — the v5 paste manifest is architect/execution-shaped
> (requires `RESIDUAL.md`); the EPIC_BOOT scope-contract IS the paste.
