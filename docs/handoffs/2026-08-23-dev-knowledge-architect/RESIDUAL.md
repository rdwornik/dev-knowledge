# Residual — 2026-08-23-dev-knowledge-architect — the part the repo does not already encode

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
**Two flags are STANDING and neither is this window's**, so re-derive rather than inherit the reading. (1) The `anchor_gate_probe` suite RED, live on `main` since 2026-08-22 and rooted in a `tmp_path` fixture — queued as `f8-harness` in `docs/audits/2026-08-23-technical-window-seal.md` §3, diagnosed only as far as *"points at the fixture"*, which the seal itself says is not a diagnosis. (2) `validate_backlog`'s story-with-no-tasks WARN on `[S24]`, which is **COMPLETED 2026-08-01** and therefore expected — confirmed pre-existing against `main` at the window baseline, not introduced by any act this window.

**NEW this window, and both are dispositions rather than defects:** the `[#171]` leg-1 finding (`docs/audits/2026-08-23-technical-lane-docs-governance.md` §1 item 6) and the guard-refusal-surface question (intake 41). Neither is dispositioned in `ecosystem/disposition-register.yaml`, deliberately — a disposition would record a decision nobody has made.

**One flag was CLEARED this window rather than dispositioned:** the `doc_claims` `pytest_collected` mismatch, inherited drift from the guard merge's 111 new tests, fixed by regeneration rather than by a register entry.

Re-derive all of the above live — P4/P7/P9 hold the answers, and this paragraph deliberately states no verdict, count or `[stale]` status.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
By `#id` + ADR, one line each; detail lives in `JOURNAL.md` 2026-08-23 (a)–(g) and the cited audits.

- **`[#562]` CLOSED — REFUSED.** The guarded A/B ran (leg 3, local); both candidates failed the G1 floor. Verdict verbatim in `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §5, per ruling B3a/B5.
- **`[#578]` BORN** — carrier for the ONE earned mitigated-rerun slot + the owed incumbent refusal-promptability measurement. Register P-2: a closed row cannot carry an obligation.
- **`[#491]` ANNOTATED, not moved** — its 2026-08-22 deferral on the post-ratchet `STANDING_RULINGS` policy is untouched; only the instrument objection is retired.
- **`[#558]`'s fifth site discharged** — `VISION.md` now says `audit.py` is read-only **on siblings** (the ADR-36 invariant, and the checkable one).
- **`[#171]` NOT closed** — leg 2 (the ARCHITECTURE Ch2 pointer) landed; leg 1 has no implementation. See §4.
- **Intake 41 FILED** — the guard's refusal surface, per ADR-111 §2 (a finding may not become a row directly).
- **The R1 governance-drift top-10 discharged** across `ARCHITECTURE.md` / `CLAUDE.md` / `VISION.md`; `CLAUDE.md` v2.65 at 195 counted lines against its declared 200.
- **One instrument defect fixed** (the guard's cp1252 decode, all three sites, mutation-checked) and **three rejected with reasons** — `docs/audits/2026-08-23-technical-wave-close-funnel.md`.
- **Tree hygiene:** 17 branches retired content-verified; `origin` is `main` + `automation/fleet-audit`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Four questions, in the order they unblock each other.**

**1. Is the guard part of the instrument or part of the subject?** (intake 41 — the session's core.) 29 of 38 refusals in the A/B were `A/shell-construct`, split **22 to 7** between the two candidate lanes, and it reached a scored item: two refused attempts to DERIVE the `C1-R5` count, then an eyeball, then 86 against a true 87. The fabrication is the candidate's; the path to it was the guard's. The fork the lane recorded and did not resolve: fix it in the **item set** (items must not depend on a derivation path the guard can refuse) or in the **guard** (it must not refuse a path a scored item needs). These cost differently, and only one survives contact with the next candidate.

**2. `[#171]` leg 1 — (a) or (b), and R3 says do not leave (c).** The dashboard's own header asserts *"Generated, committed, read-only"* and `gen_dashboard.py` has **no commit path at all**. Either implement the ADR-80 writer policy, or rule that human-committed satisfies "committed" and amend ADR-86 §2 plus the two artifact strings. Worth knowing before ruling: the integrator's first pass judged this leg *met* by reading that header — the artifact's self-description, not its mechanism.

**3. What is the ONE rerun slot spent on, and when?** It is one, not many, and admission stays REFUSED until it clears the floor. Spending it before Q1 is ruled means the rerun measures the instrument. The **incumbent's** own refusal promptability is still unmeasured (billing-blocked, not judgement-blocked) and is the single most valuable measurement the control item can produce — until it exists, no ruling touching the fan-out pin should be made from this evidence.

**4. The mechanism gap this window kept paying for.** `Q2-mechanism` — *one integrator at a time enforced by a lock or branch guard, not by convention* — is still prose, and PLAYBOOK Ch8 says so about itself. This window paid for it twice: a lane's commits were refused for ~50 minutes by `journal_spine_anchor` firing on a sibling's merges (the check walks `main`'s spine but reads JOURNAL from the **working tree**, so a pinned worktree evaluates an advancing spine against a frozen JOURNAL), and the integrator merged six of a lane's seven commits because a lane's contract naming a final COMMIT does not make that commit observable as the last one. Both are cheap to survive once and expensive to keep re-deriving.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
