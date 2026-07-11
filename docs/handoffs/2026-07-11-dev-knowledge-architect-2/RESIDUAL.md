# Residual — 2026-07-11-dev-knowledge-architect-2 — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
All drift-flags this window are **STANDING / dispositioned — none NEW**: the journal-wrap `no_ff_merges` instances + the `undeclared_edges` tier-1 candidates (both in `ecosystem/disposition-register.yaml`, ref #241/#210) and the `doc_rot` backlog-accretion on **#262/#278** (history-bloat, pre-existing — this window's BACKLOG filings #318-#322 + the #301/#320 edits were trimmed net-neutral to NOT add any new doc_rot WARN). The integration merges each cleared their own gates; the filings passed filing-backpressure. Re-derive the live verdict / WARN-count / any `[stale]` via `PROBES.md` (P4/P7) — this bundle names no value.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map (JOURNAL `2026-07-11` two entries encode the detail):
- **#306** — ADR-101 §3 hermetization refusal gate `validate_hermetization.py` (HUB-ONLY, prospective-only) + `validate-hermetization` pre-commit gate; Codex-hardened (rename/slug/.MD loopholes fixed).
- **#307** — `gen_intake_index.py` status-grouped `docs/intake/` index + `intake-index-freshness` gate; Codex-hardened (label/splice/frontmatter). Gates 14→16.
- **E2E** — consumer-lifecycle gauntlet `tests/test_e2e_consumer_lifecycle.py` (opt-in `slow`+RUN_E2E); 10/11 stages green ×3.
- **PLAYBOOK Ch9** — the fleet methodology↔project boundary doctrine (charter debt H1; cites the #312 design + matrix).
- **win-tooling** — registered in the fleet REGISTRY (operator's `c198cf1`, declarative-only).
- **Filed:** #318/#319 (Codex A3/A4 parity gaps), #320 (fleet backup posture), #321 (ARCHITECTURE organ-map debt), #322 (fleet dashboard); folded plan-continuity into **#301(iv)**.
- All 4 night branches merged `--no-ff` + pushed to `main` (spine ends `b94a232`). Deliverables: `docs/audits/2026-07-12-technical-night-*.md` (codex-review · e2e-evidence · c4-requirements · rollout-{ai-council,corp-monorepo} · delete-candidates · plan-continuity-proposal · verdict-sheet).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Priority-ordered next-frontier (operator-set at this wrap; the residual's core payload):**

- **P1 — the hermetization/universalization goal LANDS HERE: #318/#319 triage → ai-council rollout.** First triage the two Codex-surfaced enforcement-transfer gaps — **#318** (block-ff-push pre-push adapter misses empty-remote/multi-ref ranges) + **#319** (v1.3.0 carrier bumps `rev` but does not append the new hook ids to existing consumers) — because both undercut the #302/#309 parity the rollout arms. THEN the **ai-council rollout** from the staged draft `docs/audits/2026-07-12-technical-night-rollout-ai-council.md` (grandfather map aligned to the hub baseline · carrier-arm v1.3.0 · commands gap · #314/#315 deltas). This rollout IS the operator's universalization/hermetization headline — visible outcome, not meta-work.
- **P2 — corp rollout (ADR-41) + D4 staleness.** From `…-rollout-corp-monorepo.md`: carrier-arm (corp has NEITHER gate) + the D4 staleness fix (only **ADR-31 at `corp-monorepo/ARCHITECTURE.md:568`** is genuinely stale — a "Layer-2" misattribution; N2 verified ADR-30/38/53/54 current). Runs in the corp dedicated chat (ADR-41 — hub cannot write a child).
- **P3 — C4 visualization research [ARCHITECT-OWED · STANDING DEBT · ~4× overdue — FLAG].** The open-web codemap/diagram/visualization research the architect owes; the repo-side requirements are staged in `…-c4-requirements.md` (fleet Mermaid inventory=12 · the #262/#295 `ast_walker` node-granularity root-cause · per-repo tach matrix · the hub's own codemap is a 2-orphan stub). It has slipped multiple handoffs — treat as the standing debt, not a fresh item. It **GATES** the Mermaid/ToC diagram-selection ruling (#165) AND the #322 Fleet-dashboard **visualization layer** (leg b).
- **P4 — EPIC H spike (incl. the NEW Codex axis) → then #270, #317, grooming.** EPIC H = subagent/model-routing doctrine (OD3): research spike → PLAYBOOK doctrine (Opus=orchestration/judgment · Sonnet=bounded probes/mechanical · Haiku=cheap fan-out). **This night-batch + integration is itself an evidence datapoint** — an Opus orchestrator + 5 Sonnet read-only subagents ran cleanly with EVERY git mutation serial in the main thread; the doctrine held under load (and two incidents — the accidental out-of-order merge + the immutable-bundle overwrite — were caught + recovered, evidencing the verify-and-surface discipline). **CHARTER EXTENSION (this wrap): a SECOND routing axis — Codex-5.6 variant-routing.** SOL/TERA/LUNA task-class routing + a **producer-role pilot** (Codex as a code PRODUCER, not only reviewer) with **ex-ante success criteria** + a **CC-verifies-Codex contract** (CC adversarially checks every Codex-produced artifact — the inverse of tonight's Codex-verifies-CC). **GATED ON AVAILABILITY (verified live this wrap): the 5.6 variants are ABSENT** — codex-cli 0.144.0 pins `model = gpt-5.5` (effort medium, script-overridden to high); no `sol`/`tera`/`luna` in `~/.codex/config.toml` or the CLI (migration path tops out at gpt-5.5). So the variant-routing pilot is charter-only until 5.6/sol/tera/luna land; the producer-role + CC-verifies contract can be designed now against gpt-5.5. THEN **#270** (operator-load gauge, re-enters admission), **#317** (parallel-test — **post-D1**: the global core-invariant #2 change is operator-gated, never unilateral), and grooming.

**Plan-continuity (per #301 clause iv — the reason this residual exists).** The incoming session's plan-vs-implementation comparison baseline is the **operator-held plan-vs-execution review doc** — it lives in the operator's browser workspace, NOT in the hub tree (searched `docs/handoffs/**` + `docs/audits/`, not found; the operator carries it forward). Compare this arc's ACTUAL execution — the night-batch + morning integration (JOURNAL `2026-07-11` two entries) — against that plan-of-record before starting P1. The #301(iv) fold this wrap names the carrier that makes this mechanical next time (a `prior_plan:` bundle field + gen_handoff discover-step + a RETROSPECTIVE plan-vs-execution subsection), so a future handoff carries the prior plan automatically rather than relying on the operator holding it.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
