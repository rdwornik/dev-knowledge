# Residual — 2026-07-03 architect handoff — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This window EXECUTED the prior handoff's P0.** The `2026-07-02-dev-knowledge-architect-2`
> bundle re-scoped the priority to *close the enforcement-transfer gap*. This window **did it**:
> Informant Organ → mesh carrier → deployed v1.1.0 to ai-council → **enforcing-local ×2 PROVEN**
> (the first empirical proof the deployed methodology BITES in a consumer). Plus all 4 Fable
> consult #1 rulings landed. The one **un-integrated** arc is the P1 essence-spec on
> `feat/essence-spec-p1` (commit-and-stop, `[#244]`) — **the immediate architect review item** (§4).
>
> **This is a CC-authored (repo-derived) handoff — `SUPPLEMENT.md` is EMPTY (cold shape).** There
> is no outgoing browser chat feeding a strategic *why*; the residual below is reconstructed from
> the committed JOURNAL/git window. If an outgoing chat holds the essence-spec / mesh-model *why*,
> the operator fills the supplement (`supplement filled`); otherwise the incoming §13(d) beat fires
> FULL (§4).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the
> load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-03-architect-handoff` off `main` `ff3d744`).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and CLEAN; **10 WARN dispositioned, NO `[stale]` line**

`python scripts/audit.py ship-gate` → **GREEN** (**10 WARN dispositioned**, **NO `[stale]`**) —
verification organs green against the `main` arc. The 10 dispositioned WARNs are all standing /
benign (none is a regression):

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) — **expected seam, not a regression.** **#210** (open) proposes converting
  this class from per-instance disposition to a standing rule (path-scoped EXEMPT or branch-then-merge
  the JOURNAL wrap) — a §4-adjacent decision.
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241**. **NEW this window** — the `#179` undeclared-edge scan (Fable consult #1 ruling #2) was
  wired as a ship-gate WARN leg and **fires as designed**; the 6 hub candidates were dispositioned
  per-doc (precise, not blanket-declared) with the declare-vs-defer adjudication tracked by **#241**.

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the
  methodology source; its own entry stays null. **ai-council** now records **`1.1.0`** (`source_tag
  v1.1.0`, `deployed_date 2026-07-03`) in `ecosystem/deployed-versions.yaml` — deploy run #1.
- `enforcement_coverage` (`[--]`) — the Informant Organ's static leg is **read-only, never
  FAIL/WARN**; per-consumer coverage is measured by `scripts/enforcement_coverage.py` (the fire test
  is the truth-maker, not this leg).

_(No `[stale]` disposition. This is a clean gate — the whole §1 is standing flags, no new regression.)_

---

## §2 — Shipped this window (prior `-2` bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~8). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`. **On `main` (`ff3d744`)** except where noted.

**The enforcement-mesh P0 — BUILT + ARMED + PROVEN (n=1) — the sealed backdrop (do NOT redo):**
- **Informant Organ** (`#235` Stage-2, `99401d7`/`03a3280`; epic filed `c310058`): `enforcement_coverage.py`
  (`CoverageProbe{applicability → locate → fire_test}`; fire_test = clone+inject+assert-block, the
  **sole** truth-maker for `enforcing-local`). First run reproduced the **honest fleet-map** —
  `canonical_freshness` + `session_end_backpressure` **absent ×4** (the real closable gap);
  `doc_claims` + `git_backlog_drift` **hub-scoped ×8** (hub-only-guarded — no consumer wiring can fire
  them); `reconciled_versions` **n/a-no-edges ×4**. Static leg added to `ALL_CHECKS` (non-blocking `n/a`).
- **Mesh carrier hub-side** (`#236`/`#237`, `5028d03`/`62c26b2`/`edc1f5f`/`dd53c99`, merged `e5e88cf`):
  `deploy/carrier_mesh.py` (5th carrier) + `session_end_backpressure` **git-toplevel-first** root
  resolution + extracted `scripts/canonical_freshness_gate.py` (single-sourced hub module). A staging
  **defect** (gitignore swallowed 2 of 7 artifacts) was **caught in Phase-1 + fixed** (`5f8be71`:
  `.gitignore` re-include negation + `git check-ignore` committability verify — *presence ≠ committable*).
- **Deployed v1.1.0 to ai-council** (`52e87ac`, tag `v1.1.0`, merged `4592ed4`; ADR-91/92) →
  **fired `enforcement_coverage.py --fire` → `enforcing-local ×2`** (`5f95d06`, anchored `e2161f9`):
  seb `decision:block` on unanchored work + `canonical_freshness` blocked-in-isolation. **ADR-81
  leg-(e) acceptance MET — the first empirical proof a deployed organ BITES.** `#236`/`#237` **closed**
  (done-items-leave, operator-approved).
- **Fable consult #1 — all 4 rulings landed** (`a0f5aac` merge): **ADR-94** status-line-mutable-on-
  ratification (operator-signed, `e682bdd`); **ADR-95** ai-council query lane-split (record-only);
  the **#179** undeclared-edge scan wired as a ship-gate WARN leg (`62a8248`, demonstrated to fire);
  **ADR-81 leg-(e)** functional-proof amendment (`76d71aa`, mirrored to PLAYBOOK Ch12). Filed
  `#241`/`#242`/`#243` from the disposition pass.

**The immediate open arc (NOT on `main` — `feat/essence-spec-p1`, 7 commits, commit-and-stop `[#244]`):**
- **P1 essence-spec v1 + release-lint** (`16c31ee`→`0fc3807`): `deploy/manifest-v1.1.0.yaml` grew
  `anchors:` / `components:` (13, status `active`, INERT to tool.py) / `doc_shapes:`; `deploy/release_lint.py`
  (C1–C7 reconciling all 5 version anchors to `source_tag`); 27 acceptance tests (golden-diff proves
  `assess` is byte-identical old-vs-new + 17 injected-mismatch teeth). **Behavior-preserving by design.**
  Acceptance MET (golden-diff IDENTICAL, release-lint GREEN + fails 17 mismatch classes, 1101 passed,
  ship-gate GREEN). **This is the architect's review + integration item (§4).**

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — on `main`: **7 themes, 22 stories, 100 tasks** (witnessed via
  `validate_backlog`); on `feat/essence-spec-p1`: **23 stories, 101 tasks** (the `#244` epic). The
  spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated), `feat/essence-spec-p1`
  (**the live unmerged P1 arc — do NOT delete**), this handoff branch `docs/2026-07-03-architect-handoff`,
  plus two **merged stragglers safe to `-d`** (`feat/mesh-carrier-hubside`, `deploy/record-ai-council-1.1.0`)
  and `automation/fleet-audit` (a routine baseline branch, unmerged — separate concern, leave).
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the serialize-groups
  + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9): **code-edge = just `#218`**;
  **coherence = `#180/#181/#182/#220/#241`** (`#241` added this window — the declare-vs-defer edge item);
  **audit-py group includes `#234/#240/#242/#243`**. Note `#238`/`#240`'s `depends-on: #236` was
  **removed** when `#236` closed (satisfied) — they are unblocked.

---

## §4 — The next frontier (open architecture decisions)

**The prior P0 is substantially closed.** "Held by mechanism, not memory" is now **TRUE for one
consumer** (ai-council, n=1) — not just the hub. The frontier shifts from *build the mesh* to *review
the immediate arc, generalize the mesh, and resume the demoted goals*. **recall/inferred** — the
architect resumes here; if an outgoing chat holds more, the operator fills `SUPPLEMENT.md`.

### (1) IMMEDIATE — review + integrate the essence-spec P1 branch (`feat/essence-spec-p1`, `[#244]`)

The one un-merged arc; committed commit-and-stop precisely so the architect owns the integration call.
- **Merge decision:** review the 7-commit branch; integrate from the **primary** checkout via `--no-ff`
  (never a worktree — the seed-state lesson). P1 is behavior-preserving (golden-diff IDENTICAL) — low risk.
- **Surfaced decision — spec-path (absorb-not-pair):** P1 evolved `manifest-v1.1.0.yaml` **IN PLACE**,
  rejecting a paired `manifest-v1.2.0` (a second spec file recreates the drift-twin; a bumped version
  implies an untagged release preflight would refuse). **Architect confirm or override.**
- **Surfaced decision — release-lint wiring:** `deploy/release_lint.py` is **manually invoked**, wired
  into neither `ALL_CHECKS` nor deploy preflight. Preflight wiring is behavior-changing → **deferred for
  architect placement.**
- **`[#244]` lifecycle epic — P2–P6 gated:** P2 (PRUNE / remove-leg + tombstone) is gated on **operator
  D3**; P3 (roster generation), D2 (divergence allowlist), P5 (hub self-prune), P6 (fleet) all downstream.
  Sequence the epic.

### (2) The mesh generalization — is the Fable consult #2 (mesh-model A/B/C) still needed?

The prior handoff located a Fable consult on the **mesh-transfer model**: **(A)** 5th carrier, organs
run locally; **(B)** hub-sweep-on-cadence; **(C)** hybrid. **VERIFY-FIRST:** the Informant Organ's
fleet-map **may have already answered it empirically** — the organ-portability split is not a matter of
taste, it's structural: `canonical_freshness` + `session_end_backpressure` are **locally enforceable**
(now shipped local via the model-A mesh carrier, proven on ai-council), while `doc_claims` +
`git_backlog_drift` are **hub-scoped-by-construction** (they cannot fire inside a consumer without
changing the organ). **That reads like model C (hybrid) decided by measurement, not by consult.** So the
architect's first call: **does a Fable consult #2 still add value, or does the fleet-map + the proven
model-A carrier settle the design** — leaving only `#243` (below) as the open governance sub-question?
(See the memory note *"Enforcement organs not homogeneous"* — the 5 organs split by portability.)
- **`#243` — the `#168`-hard vs Fable-WARN conflict** (unresolved): `#168`'s Done-when says promote the
  JOURNAL leg to fail-closed HARD; Fable consult #1 ruled arc-tracking stays WARN with no-item
  disposition. Resolves at/after the mesh-model call.

### (3) Generalize + formalize the enforcement-mesh (dependency-ordered)

- **`#238` — Stage-4 record+formalize:** write the **"deployed presence ≠ deployed enforcement"**
  doctrine into LESSONS + PLAYBOOK (the configured→armed→proven distinction, generalized to the mesh:
  *done only when enforcement-in-effect is demonstrated, not merely deployed*). **Open** — the doctrine
  is proven but not yet recorded.
- **`#221` — fleet rollout n=2+:** Axis-1 is proven n=1; run `deploy/tool.py` on
  corp-monorepo / corp-ops / corp-sca-time-automation, each using **#230** as its acceptance gate and
  requiring **#225** (surgical precommit carrier) closed first. **Carry the pilot rule:** treat each
  consumer's `.gitignore` + config shape as an **UNKNOWN to probe, not a copy of the hub** (the
  `override.md`/`logs/.gitkeep` gitignore defect that halted the ai-council deploy — LESSONS 2026-07-03).
  **Do NOT onboard corp-monorepo through a soon-to-change methodology** — sequence after the Fable
  whole-system review if that will move the corpus.
- **`#239` — Tier-2 breadth**, **`#240` — audit-leg regression teeth** (WARN on an `enforcing-local →
  absent` regression once a baseline exists), **`#234` — cross-repo probe FAIL-teeth** (harden the
  `.claude/` cross-repo targets; honest-partial WARN today).
- **ai-council standing debt (off-repo, live consequence):** ai-council's `CLAUDE.md` is genuinely
  A2-stale (`last_reviewed: 2026-06-02` < edited 2026-07-02). The now-live **deployed** freshness gate
  **WILL block ai-council's next real commit** until it is genuinely re-reviewed + re-stamped (the organ
  dogfooding itself). Resolution is a **real re-review, never a faked stamp** — owed in the ai-council chat.

### The prior three-goal priority — still real, sequenced-after (kept, not deleted)

- **(a) Fable whole-system review + merge rulings** — input:
  `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`. Note the perishable Fable
  window is now best spent on the mesh-model call (2) if it is still open; the system-audit review is
  real but lower-urgency.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier; browser →
  CC → ai-council; CC owns the mechanical lifecycle, architect owns question-framing) — **designed, not
  built** (ADR-95 recorded the lane-split).
- **(c) Close the ADR + ai-council methodology tracks** — `#170`/`#168` were verified-at-source as
  **arc-tracking** (issue-ID↔commit anchor), **NOT the ADR sticking point** the earlier handoff feared;
  (b)+(c) remain one work-stream, sequenced after (2)/(3).

### Adjacent open decisions (smaller, mostly unchanged)

- **`#241` — declare-vs-defer `reconciled_with`** for the 6 `…→handoff-process` prose edges (now
  dispositioned, not declared — the standing WARN this window introduced).
- **`#242` — ADR status-flip coherence check** (the ADR-88/89 Pattern-A vs ADR-92/94 Pattern-B header↔README
  divergence — filed, not built).
- **`#220` — the MODIFY / semantic-drift axis.** VERIFY-FIRST: does any organ gate a
  *meaning-change-without-version-bump*, or only add/remove/exist? Demonstrated-catch bar first.
- **`#210` — journal-wrap no-ff standing rule** (path-scoped EXEMPT vs branch-then-merge the wrap; must
  NOT weaken core-invariant #5). **`#233`/`#232` — ship-gate right-sizing / tempdir isolation** (hygiene).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The enforcement-mesh proof (READ FIRST — the P0 that closed):** `JOURNAL.md` top ~6 entries (Informant
  Organ → mesh carrier → deploy defect+fix → **enforcing-local ×2** → close #236/#237); `deploy/carrier_mesh.py`,
  `scripts/enforcement_coverage.py`, `scripts/canonical_freshness_gate.py`; `ecosystem/deployed-versions.yaml`
  (ai-council `1.1.0`); ADR-91/92/93; the memory note *"Enforcement organs not homogeneous"* (the organ split).
- **The immediate review item:** `feat/essence-spec-p1` — `deploy/manifest-v1.1.0.yaml`,
  `deploy/release_lint.py`, `tests/test_essence_spec.py` + `tests/test_release_lint.py`, and the
  `feat/essence-spec-p1` JOURNAL top entry (the P1 arc + the 3 surfaced decisions).
- **Fable consult #1 landings:** ADR-94, ADR-95, ADR-81 (leg-(e) amendment), `scripts/audit.py`
  (`check_undeclared_edges`), `docs/decisions/README.md`.
- **The demoted-goals input:** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`.
- **Prior context (superseded on priority, kept for the "why"):** the `-2` bundle's `SUPPLEMENT.md`
  (the enforcement-mesh finding) + `docs/handoffs/2026-07-02-dev-knowledge-architect/` (the three-goal
  context, now demoted).
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
