# Residual — 2026-07-07-dev-knowledge-architect — the part the repo does not already encode

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
Every ship-gate WARN this window is **standing + dispositioned** in `ecosystem/disposition-register.yaml` — the `git_backlog_drift` voided-closure (#77), the `no_ff_merges` journal-wrap / transcript-archive commits, and the `undeclared_edges` handoff-process prose edges (#241, the tracked deferral). **No NEW drift** was introduced: the session-wrap arc is docs-only (BACKLOG dispositions + audit-index regen) and the concurrent `/changelog-review` arc is a pure ADD. Re-derive the live verdict / WARN count / any `[stale]` marker via `PROBES.md` P7/P4 — this bundle states none.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
- **Overnight mega-mission** (merged to main — see the mission ledger `docs/audits/2026-07-07-overnight-mission-ledger.md` + `JOURNAL.md`): closed #159 / #225 / #249 / #250 / #238 / #233 / #247 + #262 hub-side; #267 **DEGRADED** (half-b landed). HANDOFF_PROCESS v5.5→5.6 (§14a MODE item); enforcement-transfer doctrine (#238 → PLAYBOOK Ch12 + LESSONS); audit-index generator; ADR-96 / ADR-97.
- **This session-wrap**: archived the architect rulings (BACKLOG FLAG fold adjudicated — #168/#170 co-seq #239/#240, #139 separate, #243 co-seq; #267 mechanism LEAN) + regen audit-index. **No new doctrine** — all mission doctrine already sits in its canonical home (independently verified HERMETIC).
- **Concurrent `/changelog-review`** (#113 PUSH half, ADD-only): claude-code 2.1.178→2.1.201 + codex 0.140.0→0.142.5 reviewed; digest `docs/audits/2026-07-06-changelog-review.md`; **A1/A2/V1 flagged to the architect** (see §4).

Detail lives in `JOURNAL.md` / `BACKLOG.md` — this is the map, not a recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The session's decision queue — ratify, don't rediscover.**

**A. Ratification — 3 decision-ready proposals on the intact `drafts/2026-07-07-proposals` branch** (`git show drafts/2026-07-07-proposals`; unmerged by design — this session consumes it):
1. **Intake process** — the functional-architect → technical-architect → epic-chat pipeline (the operator's explicit strategic ask; today undesigned).
2. **Epic-naming convention** — draft rec: Track-X labels now, full story-map at P6.
3. **Audit-retention rule** — draft rec: keep-all + age-tiered index, folding #212 into an ADR.

**B. Then tee (the mission closed these gates but did NOT lift the WAIT):**
- **P6 fleet-roll WAIT-lift** — n=2+ consumer rollout (#221 / #244-P6). Blocking gates closed + verified per the mission ledger; the go/no-go is this session's call.
- **#267 attended re-measurement** — half-a (live re-measurement) is a stated design fork; mechanism LEAN recorded (instruct-the-child for the n=1 attended witness; discover-from-config as the fleet-scale position, P6-coupled). Needs an attended run.

**C. Routed elsewhere (ADR-41 — NOT hub scope; for the named dedicated chat):**
- **ai-council chat** — the measurement-side residuals: relative-paths-only ×2 surfaces, the hub-coupling `References` generability question, the A2-stamp contradiction, and `settings.local.json` cleanup.
- **Tooling-config (from the concurrent `/changelog-review`; capture-only, no organ touched):** **A1** refresh Sonnet pins → Sonnet 5 (`.claude/agents/artifact-reader.md` + `.claude/workflows/conformance-hub.js` still pin `claude-sonnet-4-6`); **A2** native auto-mode safety nets (claude-code 2.1.178/.183/.193) for the #86 cloud-night envelope; **V1** (gates A1) verify `claude-sonnet-4-6` not deprecated. Digest: `docs/audits/2026-07-06-changelog-review.md`.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
