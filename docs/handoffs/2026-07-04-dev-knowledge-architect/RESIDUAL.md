# Residual — 2026-07-04 architect handoff — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This window CLOSED the [#244] essence-spec lifecycle epic P1→P4.** The prior
> `2026-07-03-dev-knowledge-architect` handoff resumed the epic at **P2 (PRUNE)**. This window ran
> **P2 → P3 → P4** to completion: the deploy engine gained a **remove leg** (ADR-96) and pruned a
> real component from ai-council (verified ABSENT, locally-modified REFUSED); the **methodology
> roster is now machine-generated** (CLAUDE.md §9 `@import`, Fable R3 closed); the **Informant
> gained a Tier-3 drift classifier + fleet drift line** (n=1 seb inject→DRIFT→rejected-non-waivable
> proven). Deployed methodology **v1.2.0 to ai-council** (tag `v1.2.0`). Only **P5 (hub self-prune,
> #130) + P6 (fleet roll n=2+, #221)** remain of the epic.
>
> **Separately, three Fable analysis-only audits + one Fable-5 architecture review LANDED** (all
> merged, nothing built) — and they are the **real architect work of the next session**: the
> handoff-adoption review, the coherence-spine review, and the rot-algorithm design each surfaced
> meaty methodology findings that need **architect adjudication + routing**, not execution.
>
> **`SUPPLEMENT.md` is generated EMPTY** — the operator fills it from the outgoing architect chat
> (`supplement filled`) or leaves it empty for a cold handoff (§13 disposition). Until filled, the
> incoming §13(d) operator-context beat fires **FULL**.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the
> load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-04-architect-handoff` off `main` `25b104e`, tree clean, in sync with `origin/main`).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and CLEAN; **10 WARN dispositioned, NO `[stale]` line**

`python scripts/audit.py ship-gate` → **GREEN** (**10 WARN dispositioned**, **NO `[stale]`**) —
verification organs green against the `main` arc. The 10 dispositioned WARNs are the **same
standing set** as the prior handoff (no new regression this window):

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) — **expected seam, not a regression.** **#210** (open) proposes converting
  this class to a standing rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap).
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241** — the standing declare-vs-defer adjudication. **The Fable coherence-spine review (RF-4)
  argues these 6 are major-granularity edges mis-served by an `@5.3` remedy — a §4 decision.**

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the
  methodology source; its own entry stays null. **ai-council** now records **`1.2.0`** (`source_tag
  v1.2.0`, `deployed_date 2026-07-04`) in `ecosystem/deployed-versions.yaml` — moved 1.1.0→1.2.0 by
  this window's **P2 prune deploy**. corp-monorepo / corp-ops / corp-sca-time-automation still `null`
  (P6 fleet not yet run).
- `enforcement_coverage` (`[--]`) — the Informant's static leg is **read-only, never FAIL/WARN**;
  per-consumer coverage is measured by `scripts/enforcement_coverage.py --fire` (the fire test is the
  truth-maker, not this leg). **New this window:** the Informant now also carries a Tier-3 drift
  classifier + `static_drift_summary` (no-clone/no-fire snapshot).

_(No `[stale]` disposition. This is a clean gate — the whole §1 is standing flags, no new regression.)_

---

## §2 — Shipped this window (prior `-architect` bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~10). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`. **All on `main` (`25b104e`)** — unlike the prior
handoff, nothing is left on an unmerged feature branch.

**The [#244] essence-spec lifecycle epic — P1→P4 SHIPPED (the sealed backdrop; do NOT redo):**
- **P1 essence-spec v1 + release-lint** (merged `b65c760`): the prior handoff's immediate review
  item. Spec-path (**in-place absorb-not-pair**) was **APPROVED** by the outgoing architect and
  merged; `manifest-v1.1.0.yaml` grew `anchors:`/`components:`/`doc_shapes:`, `deploy/release_lint.py`
  reconciles all 5 version anchors to `source_tag` (C1–C7), 27 golden-diff/teeth tests.
  Behavior-preserving (golden-diff IDENTICAL). release-lint stays **manual** (preflight wiring
  correctly deferred).
- **P2 PRUNE — the deploy remove leg** (ADR-96; merged `2c86951`; deploy record `86aec77`): the
  add-only engine gained `detect_prune`/`prune`/`verify_pruned` (`deploy/contract.py`), the
  `carrier_precommit` remove leg (hash-guarded whole-entry removal), manifest `removed_in`/`reason`/
  `prune` schema with `ruff-gate` flipped to `status: removed`, `release_lint` C6 unlocking `removed`,
  and a Terraform-style destroy-confirm in `tool.py`. **Tagged `v1.2.0`; PROVEN n=1 on ai-council** —
  `ruff-pre-commit` **pruned + verified ABSENT**, a **locally-modified target REFUSED**
  (`PRESENT_MODIFIED` → abort, no record), non-pruned surface byte-identical. **First deleting phase —
  autonomous deletion stays forbidden; consumer-invoked + staged + hash-guarded only.**
- **P3 generated methodology roster** (merged `a750456`): Fable **R3** closed (consumer CLAUDE.md
  rosters were hand-prose → rot). The deployed corpus is now machine-generated from
  `deploy/manifest-v*.yaml` `components:[].roster` into `.claude/methodology-roster.md`, `@`-imported
  via CLAUDE.md §9; `gen_methodology_roster.py` + a blocking `roster-freshness` gate. Generated file
  is deliberately OUT of `DEFAULT_FRESHNESS_FILES` (currency = regen). FU **#248** (hub-local-source
  registry), **#249** (`@import`-edge coverage gate).
- **P4 sync surfacing** (merged `25b104e`): the Informant gained a **Tier-3 drift classifier**
  (`classify_tier3` over Tier-1, allowlist-driven `.methodology.yaml` at the consumer root),
  `static_drift_summary` (no-clone/no-fire), and a **fleet_health per-consumer drift roll-up line**.
  **n=1 demonstrated-catch:** a seb divergence **INJECTED** into an ai-council clone → **DRIFT** → a
  valid but **non-waivable** allowlist entry → **STILL DRIFT (rejected-non-waivable)**. Version
  **HELD 1.2.0** (the `waivable:` field is inert to `deploy/tool.py`). FU **#250** (codemap-freshness
  has no `components:` entry → a P6-coverage gap).

**Four Fable read-only reviews LANDED (analysis-only, all merged — nothing built; §4 is where they go):**
- **Fable handoff-adoption review** (`132c5c9`, `docs/audits/2026-07-04-handoff-adoption-review.md`):
  9 red flags on the v5 handoff surface. **Headline RF-1: the anti-bluff probe contract is INVERTED**
  — every recent architect bundle prints its probes' answers as `expected:` hints, which §5 says are
  "rejected"; the bluff-dogfood ran once at promotion (2026-06-11) and never again; hint-count crept
  1→11. **This bears directly on the bundle you are reading** (see §4 + `PROBES.md` header — I
  minimized `expected:` hints here as a first corrective). RF-2 (#164 generator unbuilt → every
  bundle hand-copied), RF-3 (#159 browser-side contract structurally unwitnessable), RF-4 (CLAUDE.md
  §5 "handoffs immutable" contradicts the §13 fill/fold lifecycle).
- **Fable coherence-spine review** (`5d87838`, `docs/audits/2026-07-04-coherence-spine-review.md`):
  **inverted investment** (heaviest machinery on the least-drifting axis; ESSENTIALS↔PLAYBOOK drift
  has zero mechanized edge) + **demonstrated self-blindness** (3 canon surfaces call the
  undeclared-edge scan "not in gate" a day after it was wired) + RF-5 latent FAIL-trap (the two
  doc↔doc walkers disagree on corpus scope) + the shared **presence-not-currency** blind spot (#220).
- **Fable rot-algorithm design** (`493fccb`, `docs/audits/2026-07-04-rot-algorithm-design.md`):
  designs `scripts/rot_report.py` — a nightly zero-LLM reverse-reference multimap + 3 existence
  predicates (dangling-path / dangling-wiring / tombstone blast-radius) + `--impact` pre-deletion
  query. **Verdict: build it, but small — assembly over existing primitives.** Implements #169's
  intent; feeds #244 P4/P5; the natural home for the operator's continuous-conformance vision.
- **Fable-5 architecture review** (`d319df9`, merged `22a5a22`,
  `docs/audits/2026-07-04-comprehensive-...` per the prior handoff's demoted-goal input): the
  whole-system review — the prior three-goal priority's (a) item.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — on `main`: **7 themes, 23 stories, 107 tasks** (witnessed via
  `validate_backlog`). The `[#244]` epic now records **P1/P2/P3/P4 SHIPPED**, P5/P6 remaining. The
  spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (all epic work integrated), this handoff
  branch `docs/2026-07-04-architect-handoff`, and `automation/fleet-audit` (a routine baseline branch,
  unmerged — separate concern, **leave**). **No unmerged feature branch this time** (contrast the
  prior handoff's `feat/essence-spec-p1`). No merged stragglers left to `-d`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9):
  **code-edge = just `#218`**; **coherence = `#180/#181/#182/#220/#241`**; **audit-py group =
  `#242/#153/#7/#36/#95/#139/#166/#190/#210/#234/#243/#240`**. The **new follow-ups** from this
  window (#245/#246 P2, #248/#249 P3, #250 P4) are filed but their graph edges are light — open the
  file for placement.

---

## §4 — The next frontier (open architecture decisions)

**The build epic is essentially done; the next session is an ADJUDICATION session, not a build one.**
[#244] P1–P4 shipped and proved (n=1); what remains is (1) **routing the four Fable reviews' findings**
(the meaty methodology work), (2) sequencing the epic's tail P5/P6, (3) the continuous-conformance
build decision, and (4) a live standing debt. **recall/inferred** — the architect resumes here; the
outgoing chat's strategic *why* fills `SUPPLEMENT.md`.

### (1) IMMEDIATE — adjudicate + route the four Fable reviews (the real architect work)

Four analysis-only reviews landed this window; **none acted on any finding** (by mandate). The
architect's first job is to triage and route them. Highest-stakes, in order:

- **RF-1 (handoff-adoption) — re-ratify or retire the anti-bluff probe contract. META-URGENT: it
  indicts THIS handoff mechanism.** §5 says a probe that ships its answer is "rejected"; every recent
  architect bundle (including this one, minimally) prints `expected:` hints. Either the hints are a
  legitimate *drift-reference* (the spec's current framing) or they inﬂate the contract (Fable's
  claim). **Decide + record**, and if the contract stands, **re-run the bluff-dogfood** (it has not
  run since promotion). This is the one finding that changes how the *next* handoff is generated.
- **RF-3b (handoff-adoption) — the boot-transcript echo that could close #159 on evidence.** The
  browser-side contract (#159) is unwitnessable because the exercise happens in a chat the repo can't
  see; RF-3b proposes an on-load echo the repo *can* capture. Cheap, closes a 12-supplement-old
  unclosable ticket.
- **Coherence-spine "demonstrated self-blindness" + RF-5 FAIL-trap.** 3 canon surfaces mis-describe a
  live gate; the two doc↔doc walkers disagree on corpus scope (handoff bundles' embedded
  `reconciled_with` escape the gate only by an assembly-format accident). Correctness bug in the
  coherence mesh — worth a fix pass.
- **RF-4 (both reviews) — CLAUDE.md §5 "handoffs immutable" vs the §13 fill/fold lifecycle.** A
  standing doctrine contradiction the fill/fold practice already violates. Reconcile the rule to the
  ADR-94 status-line-mutable precedent (or carve a §13 exception).

### (2) Sequence the epic tail — P5 (hub self-prune) → P6 (fleet roll n=2+)

- **`#130` / P5 — hub self-prune:** the hub prunes its **own** tombstoned components (dogfood the
  remove leg on the hub, not just a consumer). Next epic phase; Opus, plan-first.
- **`#221` / P6 — fleet roll n=2+:** Axis-1 proven n=1 (ai-council @ v1.2.0); run `deploy/tool.py` on
  corp-monorepo / corp-ops / corp-sca-time-automation. **Carry the pilot rule** (LESSONS 2026-07-03):
  treat each consumer's `.gitignore` + config shape as an **UNKNOWN to probe, not a copy of the hub**
  (the gitignore defect that halted the ai-council deploy). **Gated on `#225`** (surgical precommit
  carrier) closing first; FU **#250** (codemap-freshness component) + the rider-2 coupling warning
  become live here. **Do NOT onboard a new consumer through a soon-to-change corpus** — if RF-1/RF-4
  or the rot-algorithm build will move the methodology, sequence P6 after.

### (3) The continuous-conformance build decision (the rot-algorithm)

The Fable rot-algorithm design (`493fccb`) is **landed as a design doc, not filed as a build.** It
maps directly to the operator's **continuous-conformance vision** (prior supplement §6: Opus
decomposes → cheap Sonnet observers do per-file binary rot-checks). **Decision:** file it as a
BACKLOG build item with an ex-ante ADR-81 contract + a ratifying ADR (the design's own "Next"), or
defer. Implements #169's intent; the layer *above* P4/P5 where manual release-lint gets wired.
Same-day the design flagged **two stale P1-era comments** (manifest-v1.2.0 header L40-43, release_lint
docstring) + P4 flagged a **stale `enforcement_coverage.py` docstring** (seb "reported absent" is now
false for a v1.2.0 consumer) — small doc-currency fixes the rot-report would itself surface.

### (4) Standing debt (off-repo, LIVE consequence) — ai-council CLAUDE.md re-stamp

ai-council's `CLAUDE.md` is genuinely A2-stale (`last_reviewed` < last edit). The now-live **deployed**
`canonical_freshness` gate **WILL block ai-council's next real commit** until it is genuinely
re-reviewed + re-stamped — **the transferred organ dogfooding itself in a consumer.** Resolution is a
**real re-review, never a faked stamp** — owed in the ai-council chat.

### The prior three-goal priority — still real, sequenced-after (kept, not deleted)

- **(a) Fable whole-system review** — the Fable-5 architecture review (`d319df9`) landed this window;
  routing its findings is part of (1)'s adjudication load.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier) —
  **designed, not built** (ADR-95 recorded the lane-split).
- **(c) Close the ADR + ai-council methodology tracks** — `#170`/`#168` verified-at-source as
  arc-tracking (NOT the ADR sticking point earlier feared); (b)+(c) remain one work-stream.
- **`#243` — the `#168`-hard vs Fable-WARN conflict** (unresolved): `#168` wants the JOURNAL leg
  fail-closed HARD; Fable consult #1 ruled arc-tracking stays WARN. Resolves alongside (1)/(2).

### Adjacent open decisions (smaller, mostly unchanged)

- **`#241` — declare-vs-defer `reconciled_with`** for the 6 `…→handoff-process` edges (now
  dispositioned; RF-4 above reframes the remedy granularity).
- **`#242` — ADR status-flip coherence check** (Pattern-A vs Pattern-B header↔README divergence).
- **`#220` — the MODIFY / semantic-drift axis** (presence ≠ currency — named by both reviews as the
  shared blind spot). VERIFY-FIRST: does any organ gate a meaning-change-without-version-bump?
- **`#210` — journal-wrap no-ff standing rule**; **`#233`/`#232` — ship-gate right-sizing / tempdir
  isolation** (hygiene).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The [#244] epic close (READ FIRST — the P0 that finished):** `JOURNAL.md` top ~8 entries
  (P2 PRUNE → P3 ROSTER → P4 SYNC-SURFACING); `deploy/contract.py`, `deploy/carrier_precommit.py`,
  `deploy/manifest-v1.2.0.yaml`, `deploy/release_lint.py`, `scripts/gen_methodology_roster.py`,
  `scripts/enforcement_coverage.py`, `scripts/fleet_health.py`; `ecosystem/deployed-versions.yaml`
  (ai-council `1.2.0`); **ADR-96** (remove leg); ADR-91/92/93.
- **The four Fable reviews (THE ADJUDICATION INPUT — §4 item 1):**
  `docs/audits/2026-07-04-handoff-adoption-review.md` (RF-1 anti-bluff),
  `docs/audits/2026-07-04-coherence-spine-review.md` (inverted investment / RF-5 FAIL-trap),
  `docs/audits/2026-07-04-rot-algorithm-design.md` (the continuous-conformance build), and the
  Fable-5 architecture review landed `d319df9`.
- **The continuous-conformance vision (off-repo, prior supplement §6):**
  `docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md` (the operator's own contribution —
  Opus-decomposes → Sonnet-observers nightly rot-check). Do NOT lose it.
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
