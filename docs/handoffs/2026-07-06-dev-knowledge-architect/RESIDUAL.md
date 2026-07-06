# Residual — 2026-07-06-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
Authored **recall/inferred** from the JOURNAL window (Wave-2 root + Wave-3); re-derive every value live via `PROBES.md` **P7/P4/P6/P2**. **No new drift class this window.**

**Standing dispositioned set (unchanged in class — see `ecosystem/disposition-register.yaml`):**
- `git_backlog_drift` — the **#77** voided-closure false positive (a misattributed closing sha vs an operator-ruled keep-open). Standing; do not touch.
- `no_ff_merges` — the journal-wrap / transcript-archive direct-to-`main` class; **#210** proposes converting it to a path-scoped standing exemption. This handoff's own JOURNAL wrap may add one more instance of the **same** class — re-derive via P7, do not read it as a new regression.
- `undeclared_edges` — the 6 `…→handoff-process` prose edges (BACKLOG / VISION / AI_COUNCIL_PROCESS / ESSENTIALS / PLAYBOOK / SESSION_SETUP), dispositioned under **#241**.

**One structural change this window (NOT a drift):** Wave-2 **retired audit check #7** (`mermaid_theme`, ADR-51 amendment 2026-07-05), so `ALL_CHECKS` shrank by one and `ecosystem/doc-counts.md` was regenerated once. The live count + last-registered check **name** are **P2**'s answer (withheld here).

**Informational legs (by design — never FAIL/WARN):** `deployed_methodology_version` (ai-council carries a deployed version, the hub's own entry stays null; the linked-worktree-dirname keying artifact is **#265**) and `enforcement_coverage` (read-only — per-consumer truth is the sandbox `--fire` measurement, not this leg).

_No `[stale]` disposition is asserted here — **P7** re-derives the GREEN/RED verdict + the dispositioned-WARN count + any `[stale]` line over live git ∩ `main`; do not trust this prose._
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Two waves landed since the last architect bundle (`2026-07-05-dev-knowledge-architect` — an overnight scaffold cut *before* Wave-2 integration, FILL-INs never authored). **recall/inferred** — re-derive load-bearing values via `PROBES.md`; the JOURNAL top ~6 entries encode the detail. All on `main`; nothing on a feature branch except **this** handoff branch + the routine `automation/fleet-audit` data branch (**#254**).

**Wave-2 — root integration (2026-07-05; ADR-97 tree-orchestration, loop-closes-at-root):** three epic lanes merged serial `--no-ff` — **test-tiering** ([#260]/[#256]/[#257]: /ship pre-flight parallel + diff-shaped `live_repo` selection), **doc-consolidation** ([#258]: ESSENTIALS→charter trim, PLAYBOOK-absorb, CLAUDE.md generability seam), **llm-first-docs** ([#259]: zero-Mermaid ARCHITECTURE, compact-text codemap, **check #7 retired**). **ADR-51 amendment 2026-07-05** ratified (LLM-first canonical docs). 5 tasks closed; follow-ups **#262–#266** filed; doc-counts regenerated once. → `JOURNAL.md` 2026-07-05 root entry.

**Wave-3 — prove the hub on ai-council like a sandbox (2026-07-06; priority-#1 CLOSED):** the `deploy/lived_sandbox/` observer (Slice B) measured ai-council **before 1-of-6 FIRED → after FULL-COVERAGE** (4 FIRED incl. `session-end-backpressure` BLOCKING the child's stop + 2 ARMED-BUT-SKIPPED as correct file-scope behavior), **GATE-0 PROVEN**, **zero consumer-side changes** (every gap instrument-side — measure-first vindicated). Instrument hardening **G1–G7** + two **Codex** passes (0 CRIT). Shipped `templates/consumer-onboarding-runbook.md` (advances **#238** runbook half); filed **#267** (scope-exercising refinement); noted **#238**; +2 **LESSONS** trust-seam proof points; filed the ai-council relative-path fragility pointer for its dedicated chat (ADR-41). → `JOURNAL.md` 2026-07-06 ×3 · `docs/audits/2026-07-06-*`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The re-sequenced program (2026-07-04 supplement — **read it**: `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md`) was **Phase 0 safety → Phase 1 sandbox as the retroactive acceptance instrument → Phase 2 fleet re-gated**, with **P5/P6 held WAIT** while the corpus was moving. Wave-2 stabilized the corpus (three epics integrated) and Wave-3 delivered the Phase-1 payoff (priority-#1 CLOSED — the hub proven enforcing on a real consumer). **The frontier is Phase 2.** The outgoing chat's strategic *why* is **now in `SUPPLEMENT.md` (FILLED)** — its ANSWERS are folded into `PASTE_THIS.md` below; read them for the operator's own framing of Phase 2 (a consolidation wave + the undesigned functional/technical-architect intake process), which supersedes any tag-uncertainty in this CC-derived residual.

### (1) PRIMARY — the fleet-roll sequencing decision (#221 / #244 P6)

The WAIT's two preconditions have moved: the corpus stopped moving (Wave-2) and the sandbox is now the **proven** acceptance instrument (Wave-3, ai-council n=1 FULL-COVERAGE, repeatable via `templates/consumer-onboarding-runbook.md`). **Open decision: is the P5/P6 WAIT lifted, and if so what is the n=2 sequence?**
- **Inputs/gates (verify each live in `BACKLOG.md`):** #221 MUST follow **#225** (comment-preserving surgical precommit carrier — still open) and pairs with **#262** (child codemap migration to compact text); each deploy uses the **#230** conformance self-test as its acceptance gate + the new runbook; **#226** arming already satisfied (2026-07-02); ADR-41 routes each child deploy to its **dedicated chat**, not the hub.
- **The call to make:** pick the first n=2 consumer (corp-monorepo / corp-ops / corp-sca-time-automation) and the residual-close order — or record that the WAIT stays, with the reason.

### (2) Close out the enforcement-transfer epic (#238 doctrine half + Stage-3 adjudication)

Wave-3 proved hub enforcement **fires** on ai-council; two halves remain:
- **[#238] Stage 4 — doctrine half (open; runbook half shipped Wave-3, root-ratified 2026-07-06):** write into **LESSONS + PLAYBOOK** the "deployed *presence* ≠ deployed *enforcement*; done only on enforcement-in-effect (configured→armed→proven, generalized to the mesh)" doctrine + the repeatable deploy-and-re-verify runbook reference.
- **Adjudicate Stage 3 (#236/#237 mesh carrier) — VERIFY-FIRST, don't assume closed:** does the FULL-COVERAGE proof (enforcement fires consumer-local on ai-council, via the already-deployed v1.2.0 corpus) *close* Stage 3, or is the measurement orthogonal to the carrier's port? Check the live BACKLOG state and decide.
- **[#267] P2 — refinement, NOT a closure gate (root ruling: armed-as-enforcing not adopted as doctrine):** extend the ai-council arc with an in-scope edit to witness `hub-toc-hooks` + `floor-hash-verify-hook` **FIRED** (currently ARMED-BUT-SKIPPED — the single-file arc never matched their `files:` scope), and encode the scope-conditional `engages:` entries.
- **FLAG (architect's call — do NOT fold unilaterally):** whether #139 / #168 / #170 (arc-tracking / record-integrity) fold into this epic. My read matches the standing BACKLOG FLAG: **#168/#170 adjacent** (they harden the same `session_end_backpressure` organ #237 ports consumer-local), **#139 tangential** (hub record-integrity). **#243** (the #168-hard vs Fable-WARN conflict) resolves at/after this adjudication.

### (3) The carried methodology reviews' remaining halves

- **RF-1 (handoff anti-bluff) — spec half LANDED:** the structural withhold + the spec amendment both shipped (**v5.4** §5 structural anti-bluff, **v5.5** §14 epic handoffs; `9d5ebe5`). Remaining: the **first bluff-dogfood re-run** since the 2026-06-11 promotion — **this very bundle is the candidate** (it withholds every probe value by construction; try to answer P2–P9 from the compaction summary alone — every probe must fail to be bluffed).
- **RF-4 — CLAUDE.md §5 "handoffs/audits immutable" vs the §13 SUPPLEMENT fill/fold lifecycle:** a standing doctrine contradiction; reconcile to the **ADR-94** status-line-mutable precedent or carve a §13 exception. Coincides with **#157** (intra-CLAUDE.md §4/§5 file-lifecycle restatement) + **#112** (the §5 supersede-vs-never-edit fix).
- **RF-5 / #220 — MODIFY / semantic-drift axis:** VERIFY-FIRST whether any organ gates a meaning-change-without-version-bump (the two doc↔doc walkers' corpus-scope disagreement rides here); establish a demonstrated-catch bar before any design.
- **#159 (RF-3b):** the boot-transcript echo that could close #159 on evidence — **this architect handoff, if the operator runs `supplement filled`, is exactly #159's Done-when** (the incoming §13(d) beat exercised against a *filled* supplement).

### (4) Held / standing debt (do NOT advance without an explicit operator unlock)

- **ai-council relative-path pre-commit fragility (off-repo):** `repo: ../.dev-knowledge` in ai-council's `.pre-commit-config.yaml` breaks ANY out-of-layout checkout (CI, second clone, the sandbox clone — witnessed in measurement-3). Filed as a **pointer** in the BACKLOG ai-council-residuals block for the **ai-council dedicated chat** (ADR-41) — decide pin-by-URL+rev vs documented layout constraint there, NOT in the hub.
- **ai-council CLAUDE.md A2-stale (off-repo, LIVE):** `last_reviewed` < last edit; the now-deployed `canonical_freshness` gate **will block ai-council's next real commit** until a **genuine** re-review + re-stamp (never a faked stamp) — the transferred organ dogfooding itself in a consumer.
- **Deploy-arc residuals:** **#225** (surgical precommit carrier — also gates #221), **#233** (deploy-index test tempdir isolation — the xdist flake), **#247** (Rich markup swallows `[#id]` in the tombstone print), **#245/#246** (add-path `status: removed` awareness / hub-toc-hooks retirement).
- **Corpus growth (ADR-class calls):** **#212** (`docs/handoffs/**` retention/rollup — 400+ immutable bundles, the single largest growth vector), **#213** (PLAYBOOK rule/history condensation).

### Pointers (open the primary source; do not trust a paraphrase)
- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **The strategic frame (READ FIRST):** `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md` (the filled re-sequenced program) — this residual sits inside it.
- **The Wave-3 evidence:** `docs/audits/2026-07-06-ai-council-measurement-3.md`, `templates/consumer-onboarding-runbook.md`, `deploy/lived_sandbox/` (the observer), `JOURNAL.md` top-3.
- **Task-graph:** `BACKLOG.md` — Cross-repo universalization (#221/#244/#262) + the enforcement-transfer mesh epic (#235–#240, #267) + Handoff continuity (#159/#161/#164).
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
