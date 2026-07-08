# Residual — 2026-07-09-dev-knowledge-architect — the part the repo does not already encode

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
Every drift-flag this window is **STANDING and dispositioned** in `ecosystem/disposition-register.yaml`; **none is new**. The standing classes, by reference: `no_ff_merges` — the pre-existing journal-wrap / transcript-archive direct-to-main commits (grandfathered, `#210` is the standing-rule proposal); `doc_rot` backlog-accretion — `#262` + `#278` (dispositioned); `undeclared_edges` — the handoff-process prose edges under `#241`. Self-induced drift was **trimmed, not dispositioned**: the morning-ops `#254` progress-note tripped a doc_rot block and was made date-free to clear it (no new register row). Run **P4/P6/P7** for the live verdict/count/`[stale]` — this file names none by design.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = **2026-07-09** (night-verification → morning-ops → session-close → handoff fill). Detail is in `JOURNAL.md` (five 2026-07-09 entries) + `docs/audits/2026-07-09-*`; this is the map only:
- **Night verification** — full-day adversarial re-proof; found F1 (`#284` false close) + F2 (groom-parser latent). → `docs/audits/2026-07-09-night-verification-report.md`.
- **`#291`** — fleet backup posture filed **and closed** (F1 fix: corp-ops/corp-sca/demo-prep backed up + verified); supersedes the false `#284` close.
- **F2** — `validate_doc_rot` groom-parser fix (a past "Next quarterly:" no longer masks escalation).
- **`#254`** — fleet-audit durability progress (part (b): `origin/automation/fleet-audit` pushed; organ-map decl still open).
- **`#255`** — conformance-digest mechanism **retired** (ADR-84 organ; workflow + remote branch deleted, `surface_triage` Surfacing 2 removed) and closed.
- **39/39 WEAK** closure proposals rejected at architect triage (evidence for `#277` signal repair).
- **Deletion-candidates sweep** — 3 merged branches deleted. → `docs/audits/2026-07-09-deletion-candidates-report.md`.
- **changelog-review** — claude-code 2.1.204 + codex 0.143.0 (0 ADOPT). → `docs/audits/2026-07-09-changelog-review.md`.

State pointer: `BACKLOG.md` (73 tasks post-`#255`).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The operator's execution-first verdict governs this frontier** (verbatim in `SUPPLEMENT.md` ANSWERS — read it; this is the CC-observed framing around it). The bar: *visible outcomes over governance* — any new meta/governance work must unblock onboarding or be rejected. The un-committed "why" the next session must resume:

- **Sequence is visible-first, dependency-second** (do not reorder into another grooming session): (1) `#286` remaining leg — surface `S<n>` story numbers in BACKLOG titles + `validate_backlog` schema (mechanical, instant visibility); (2) **ai-council Wave-1 onboarding EXECUTED**, not planned — emit the runbook's onboarding prompt + run the n=1 pilot in ai-council's own chat (carries `#281` story-map convergence, `#282` gitattributes, `#262` child codemap, `#110`/`#128` re-file; this IS `#131`'s first real test); corp-monorepo second; (3) `#164` — **build** the v5 `/handoff` generator mode split (architect|functional|technical|developer — decided in ADR-98, asked for three sessions running, not yet built); (4) SEED 6→9 triage timeboxed, only as far as it feeds (2)/(3).
- **Open questions to rule at session start:** `docs/runbooks/` relocation — keep or move? (created on `#131`'s task text WITHOUT explicit operator surfacing — process miss; surface any new folder as a question BEFORE creating it). `#264`/SEED-9 (dashboards, lowest priority per operator) is blocked on the operator's one-sentence Arc-5 P6 usability verdict.
- **CC-observed residual (must reconcile, NOT drive-by):** `ARCHITECTURE.md` (~Ch440/442/600, incl. an outcome-table row) + `CONTRIBUTING.md` (~L134–147) still narrate the just-retired conformance-digest divert as **current** — reconcile inside a genuine `canonical_freshness` re-stamp arc (ADR-84 itself stays immutable/correct-as-history). Also latent: the **filing-backpressure hook** has never had a LIVE exercise (tests only); `#122` shim (`billing_leak_sentinel` reference) needs untangling before delete.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
