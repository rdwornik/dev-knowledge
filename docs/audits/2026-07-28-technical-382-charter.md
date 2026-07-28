# [#382] charter — desired-state data model, intake → ADR (skeleton; C5 middle path)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** 382-charter
- **What this is:** the contract SKELETON for the [#382] desired-state ADR arc — scope, inputs, Done-when
  draft, kill-criteria draft, dependency map. **NO build.** No ADR is drafted here, no schema line is written,
  no library is added.
- **Arc:** PROMPT P6 prep arc, branch `docs/p6-dated-pressure-prep`.

> **PREP, NOT EXECUTION — and explicitly: this charter does NOT trip intake #16's un-parking trigger.**
> Intake #16 is ACCEPTED / `disposition: deferred` with `trigger: "[#382] build starts"`
> (`docs/intake/2026-07-21-func-fleet-north-star.md:6-7`, ruled 2026-07-28, JOURNAL (j)). A charter is a
> contract for a future build; **build has not started.** #16 stays deferred and its `consumed-by:` stays
> empty until the build arc opens.

---

## 1. Scope

**IN (what the [#382] arc delivers):**
- The intake #16 §2 architecture — the Terraform **model**, not the tool: ONE schema-versioned desired-state
  contract in `ecosystem/` dissolving the 4-registry sprawl (**pydantic**); the dependency graph as
  doc2doc / doc2file / hooks / skills edges with rot as a graph query (**networkx**); the divergence report as
  surface × repo × {conform / diverge / declared} (**pandas**). `apply` = the EXISTING regenerate-and-diff
  machinery + carriers; state = `deployed-versions.yaml` + the per-consumer version pin. (`tasks/382-*.md`;
  intake #16 §2 mapping table.)
- One ADR (the row's Done-when: "an ADR is accepted AND schema v1 is committed") that consumes the inputs in
  §2 below and defines the id-allocation rule the spike left open (obligation 3).
- The methodology layer (ADR lifecycle, handoff harness, census, JOURNAL gates) stays custom and sits ON TOP
  of the schema, never beside it (intake #16 §2 "what stays custom").

**OUT (owned elsewhere; the charter names the owner so scope cannot creep silently):**
- Wave execution over surfaces → **[#383]** (`depends-on: 382`). The ADR defines the report; running waves to
  zero-undeclared-divergence is [#383]'s Done-when, not this arc's.
- The L4 tech-currency lane → **[#385]** (`depends-on: 383`).
- L5 analytics/predictive builds → [E9] S26 rows. Intake #16 §3 is consumed as *input* (the schema's frames
  must not preclude the L5a data model) but nothing of L5 is built.
- The viewer — settled: ADR-107 (engine build-thin, viewer slot **declared empty**, swap-out contract in the
  spike §4). Not re-openable here without ADR-107 §3's re-entry criteria.
- The fleet repo shape — settled: ADR-104 (partial fold, polyrepo mostly retained). Sets the matrix width;
  not relitigated.
- New fleet machinery beyond the schema — the intake #16 §6 standing brake.

## 2. Inputs, with pointers (the accumulation [#382] was held open for)

1. **Intake #16 §1–§3 + §5** — this arc is its **declared consumer (b)** ("the desired-state ADR session —
   consumes §1–§3 and §5", frontmatter `:8`). §1 layer table (L0–L5 + honest %s) · §2 the model mapping ·
   §3 L5 sequencing constraints (input only) · §5 lessons 1/5 as design rules ("one data model, not N
   registries"; "adopt the model, not the tool").
2. **The 7 schema findings** — `docs/audits/2026-07-27-verification-433-schema-spike.md` §5, fed forward
   under the pilot-precedes-contract ruling (obligation 1, `docs/decisions/README.md`, 2026-07-26):
   identity opaque + byte-exact · unknown-key survival as a WRITE-path contract clause · typed row =
   frontmatter + verbatim body + manifest residue · preserve-raw beats normalize-at-ingest · provenance
   field pair for every derived surface · a split needs a residue carrier · directory-as-id-counter substrate
   built, **allocation rule NOT built**.
3. **The allocation surface** (spike §5.7 / obligation 3): the ADR must *define and witness* the id-allocation
   rule over the `tasks/` substrate — `max` over filenames is not an allocation rule; no next-free calculation
   exists in the generator. (Live constraint feeding it: closed ids stay consumed — next-free scans all
   history, not the open set.)
4. **The lived flip evidence** — ADR-107 ratified + strangler flip executed 2026-07-28 (JOURNAL (f)); the
   ADR-107 §6.2 generalization obligation is deliberately NOT discharged (owner [#383], JOURNAL (m)) — the
   schema this ADR declares is what §6.2's second surface will be expressed in.
5. **ADR-104** — matrix width premise (5–8 repos, partial fold; the fabricated 10–20 corrected).
6. **ADR-105/106** — routine-consumer declaration shape and the uv toolchain rows already live in
   `ecosystem/parity-surfaces.yaml` — existing registry rows the schema must be able to absorb or reference,
   not duplicate ([#358]'s posture defect is a cautionary input: self-description must derive from the schema).

## 3. Done-when (draft — for the arc's frozen contract, to be ratified at arc open)

1. An ADR (Proposed → operator-Accepted) records: the schema's scope over the 4 registries it dissolves or
   absorbs (named individually), the identity / unknown-key / provenance clauses (findings 1, 2, 5), the
   preserve-raw validation split (finding 4), the residue-carrier requirement for derived surfaces
   (finding 6), and the id-allocation rule (obligation 3) — each finding addressed-or-recorded-with-reason.
2. Schema v1 committed under `ecosystem/` (pydantic), with validators read-only per Layer-2 (ADR-28/36) and
   at least the piloted `tasks/` surface expressible as typed rows without a parallel store (S3d
   composability, spike §1).
3. The allocation rule witnessed (one allocation performed under it, or its refusal path tested) — the
   clause-(e) "witnessed, not installed" standard.
4. Intake #16 flips `deferred` → CONSUMED with `consumed-by:` filled — **at build start, per its trigger**,
   not at charter time.
5. Adversarial review pre-merge (terra; sol optional per lane profile), findings fixed or dispositioned.

## 4. Kill-criteria (draft)

- **Kill (schema shape):** if the piloted surface cannot be expressed as one typed row + verbatim body +
  manifest residue without a parallel store, the S3d premise fails — stop, record, return to the operator
  (do not bend the ADR to rescue the library choice; lesson 5 "adopt the model, not the tool").
- **Park (shape premise moves):** if a further repo-fold ruling supersedes ADR-104's matrix width, park the
  arc and re-scope the matrix first (intake #16 §6 brake: shape rulings precede structure investment).
- **Kill (scope creep):** the ADR draft acquiring execution scope (waves, deploy runs, L4/L5 builds) is a
  contract violation, not an expansion — cut it back to [#383]/[#385] or abort the arc.
- **Kill (input rot):** if at arc open the 7 findings' evidence no longer reproduces (the spike's probes are
  re-runnable, §4.4), re-verify before consuming — a contract built on rotted findings inherits their rot.

## 5. Dependency map

```
[#387] buy-vs-build intake rewrite ──(ordering: rewritten BEFORE any ADR cites it;
       │                              intake #16 §6 standing constraint)
       v
[#382] desired-state ADR + schema v1     <- consumes: intake #16 §1-§3+§5 (consumer b),
       │                                    spike §5 findings 1-7, allocation obligation 3
       │  (un-parks intake #16 at BUILD start: trigger "[#382] build starts")
       v
[#383] execution waves per surface       (depends-on: 382, tasks/383:8;
       │                                  also owner of ADR-107 §6.2 second surface)
       v
[#385] L4 tech-currency lane             (depends-on: 383, tasks/385:9;
                                          gated on the apply channel existing)
```

Ordering note on [#387]: the constraint is conditional — it binds **if** the [#382] ADR cites the buy-vs-build
intake (intake #2). If the ADR draws only on the inputs in §2 above, [#387] does not block; the arc-open
session states which branch holds. Related, not identical: [#371]'s "buy-vs-build fleet-template ADR" (the
`.vscode` write-through vehicle) is a sibling consumer of the same rewritten intake, not a dependency of this
arc.

## 6. Boundary restated

Charter only. Zero schema code, zero ADR text, zero intake mutations in this arc. The next action this
charter authorizes is *scheduling the [#382] arc* — and the first act of that arc is freezing §3 into its
acceptance contract.
