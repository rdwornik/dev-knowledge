# Residual — 2026-07-27-dev-knowledge-architect — the part the repo does not already encode

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
**STANDING** — every disposition carried into this window is a pre-existing family in `ecosystem/disposition-register.yaml`, unchanged in kind: the `no_ff_merges` journal-wrap/transcript-archive instances ([#210] owns converting them from per-instance to a standing rule), the `reconciled_versions` template-malformed row (#335 class), the BACKLOG history-accretion rows ([#344]/[#421]/[#422]/#332/#278 — each condensed by its own build, not here), the `#241` undeclared-prose-edge family, and the `fleet_parity` ai-council root entry ([#430], whose (b) half is that a verdict depends on state outside its subject).

**NEW this window** — two rows only, both added deliberately under an operator ruling rather than to silence a signal: the `#241`-family pair covering the intake→handoff-process edges raised by intake #18 and by the generated intake index. The ruling is that an intake **proposal** is a not-yet-coupled ref by design; both rows carry a `review_date` and clear by themselves when [#435] rules the pack. Read them at their `id`s in the register, not from this line.

**ENVIRONMENTAL, not drift** — `handoff_probes` cannot resolve a cross-repo sibling from inside a git worktree; it reads clean from the primary checkout. If it surfaces, verify the checkout before dispositioning anything.

P7/P4 re-derive the live verdict, counts and `[stale]` set; nothing above states one.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
- **[#432]** uv adoption → **ADR-106** (pinned toolchain, locked gate environment, per-repo gated rollout) + **ADR-101** amendment. JOURNAL 2026-07-27 (c).
- **[#433]** strangler STEP 1–2 → `docs/audits/2026-07-27-verification-433-schema-spike.md`; engine/viewer ruling recorded, viewer **REJECT** on labelled evidence. Row stays OPEN. JOURNAL (d).
- **[#434]** conformance-branch extraction → `docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md`; **fork RULED**, verbatim in `docs/decisions/README.md` "Decision notes (non-ADR)". JOURNAL (b), (g).
- **[#428]** narrowed by that ruling to building the CONSUMER; **[#435]** filed to steward intake #18 to ratification. JOURNAL (g).
- Handoff-process v5.7 audit + **intake #18** (v6 proposal, A1–A11, PROPOSED) → `docs/audits/2026-07-27-verification-handoff-process-audit.md`. JOURNAL (e), (f).
- **intake #19** (operator design input — night shift + handoff reform, verbatim, SEED) and **[#436]** (`silent_rule_ratchet`) filed this window; **R12 ruled F1** in the `[E8]` closure-contract context.

Detail lives in `JOURNAL.md` 2026-07-27 (a)–(g) and the rows themselves — this is the map, not the record.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The expectation for this session is EXECUTION-FIRST.** Four inputs are already in the repo and none of them needs re-deriving — read them, rule them, build. Pointers only below; do not restate their content.

**1. Intake #18 ratification — [#435].** `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` (A1–A11, PROPOSED) against `docs/audits/2026-07-27-verification-handoff-process-audit.md`. The open question is per-amendment ADOPT / DEFER / REJECT with a reason, then whether the spec cuts to v6. The pack is produced and unconsumed — that is the [#419] class, and [#435] exists so it does not repeat. The intake deliberately carries **no** `reconciled_with`; its two register rows clear when this rules.

**2. Design input for that same session — intake #19 §B.** `docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md`, section B (clean-handoff contract; one-round-trip boot; inherited-claims verification as NON-NEGOTIABLE). **Not citable by a prompt or contract until ratified here** — its header says so. Section A of the same doc is the morning-loop wave's input, not this session's.

**3. The ratchet — [#436].** Row-independent by construction: build proceeds whichever drain row the operator later selects. The still-open operator decision is the **drain scope** (which slice), recorded as pending in the `[E8]` closure-contract note; the ruling itself (F1 — ratchet + bounded drain, discharging R12) is already recorded there.

**4. Restructure-ADR inputs.** `docs/audits/2026-07-27-verification-433-schema-spike.md` §1 (K1–K5 definitions — the operator's term, defined in-repo for the first time there), §5 (the seven schema findings owed to **[#382]**), §3–§4 (viewer REJECT + the swap-out contract the gate must pin). The ADR that rules engine + viewer + swap-out is not written; [#433] stays open until it is, and [#382] receives §5 either way.

**Open and NOT ruled here:** the drain-row selection ([E8] clause (b)); the [#434] branch deletion (a separate operator word now that option (1) stands); whether ai-council's ADR-11 #117 marker lands this window (a different repo, raised and not executed).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
