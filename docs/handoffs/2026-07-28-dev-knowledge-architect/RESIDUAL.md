# Residual — 2026-07-28-dev-knowledge-architect — the part the repo does not already encode

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
**Every flag standing at generation is a CARRIED one — this window introduced no new drift class.** Read that as a claim about *provenance*, not about state: P7/P4 own the live verdict, and the sentence stops here deliberately.

**Standing, each with a register row** — `ecosystem/disposition-register.yaml` is the authority for which is which; do not infer from this list. Four families: the `no_ff_merges` legacy non-merge commits on the first-parent spine (June-era, forward-only — never rewrite them); the `reconciled_versions` malformed marker on the CONTRIBUTING template (`[#335]`); the `doc_rot` backlog-accretion cluster (`[#344]`, `[#421]`, `[#422]`, `[#332]`, `[#278]`); and the `undeclared_edges` handoff-process prose family plus the `fleet_parity` ai-council root entry (`[#241]`, `[#430]`). If a row is missing for a flag you see, that is the finding — not the flag itself.

**Two things to know about the flags that are NOT in the register, because both were self-inflicted and both were caught by a gate rather than by review.** (1) A new BACKLOG row breached the `doc_rot` gross-character ceiling on the way in; it was **trimmed at the source, deliberately not dispositioned** — a register row is for a WARN we accept, and one manufactured by its own sibling commit would launder bloat past the gate built to catch it. Precedent worth keeping. (2) `task_tree_coherence` fired **twice** this window in two distinct modes: an orphaned derived file after a closure (`--write` adds but never deletes; `--write --prune` is the closure form) and a whole-file reassembly mismatch after a **prose-only** BACKLOG edit. Treat any BACKLOG touch, prose included, as requiring a regen.

**Anti-bluff note for the incoming session:** this section names no verdict, no count, no `[stale]` status and no sha. If you want those, run the probes — and if a probe disagrees with anything above, the probe is right.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail is in `JOURNAL.md` 2026-07-28 (a)/(b)/(c) — this is the map only.

- **`[E8]` closure clause (b) AMENDED** (operator ruling D1) — the drain slice the F1 note left pending is now selected; frozen contract text unchanged, amendment recorded beside F1. Full-pool intent + the drain-owed list live in `[E8]`. **Recorded, not executed** — no drain ran. → `BACKLOG.md` `[E8]`
- **`[#434]` CLOSED** — conformance-branch extraction; both Done-when clauses re-verified live, not trusted from the WEAK gate verdict. Ruling record updated in the same arc at `docs/decisions/README.md`. → JOURNAL (c)
- **Seven `claude/conformance-*` branches deleted** (operator word D2) — the separate word RULING 2 reserved. Aggregates verified present on `main` *before* the delete.
- **`[#436]` CLOSED** — silent-rule ratchet, closed at the window's open. → JOURNAL (a)
- **Intake #20 filed** — `docs/intake/2026-07-28-north-star-delta-review.md`, **DRAFT / non-citable until ratified**. Intake #16 annotated with status markers only.
- **`[#437]` + `[#438]` filed** — see §4 carried debt; both are new this window.
- **`[#409]`/`[#410]`** differentiated (dedup heuristic cleared); teardown rule added to `.claude/rules/git-discipline.md`; `[E8]` sweep outcome line reconciled (R12).
- **ADR-107 — NOT ratified.** Authored `Proposed` in the prior window and **still `Proposed`**; two conditional ratification instructions arrived this window and neither carried the operator's word, so nothing was recorded. This is §4's first open decision.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### FIRST ACTION — the FLIP (ADR-107 strangler step 3), under its frozen contract

Do this before anything else, and only if **both** preconditions hold. Check them; do not assume them.

- **Precondition 1 — ADR-107 `Accepted`. NOT MET at bundle time: the ADR is `Proposed`.** Two conditional ratification instructions reached this window and neither carried the operator's word, so the flip is **blocked on ratification, not on build readiness**. Ratify first (below) or the flip cannot start.
- **Precondition 2 — the `tasks/` coherence gate ARMED. MET.** Active since `fa3f10a3` (`[#433]` C1), and it is not merely installed — it **fired twice for real this window**, in two different modes (orphaned derived file after a closure; whole-file reassembly mismatch after a prose-only BACKLOG edit). Enforcement witnessed, not installed — the `[E8]` clause (e) standard.

**Step 4 (prose relocation) stays EXPLICITLY DEFERRED — owner: a later arc, not this one.** ADR-107 defers it by design. Do not let flip momentum pull it forward; the flip is step 3 and stops there.

### OPEN OPERATOR DECISIONS

1. **ADR-107 ratification** — the gating decision for the FIRST ACTION above. `Proposed` since authoring; the sol adversarial review (E1–E5) is already folded in verbatim, so the ADR the operator reads is the reviewed one. Nothing further is owed *to* it — it needs a word.
2. **`[#370]` — is the `owner=hub` / `owner=repo` ownership model two-state-complete?** **Recommended path: a short READ-ONLY evidence probe enumerating the user-level `~/.claude` surfaces BEFORE ruling**, not a ruling from memory — the row's claim is that a third content class demonstrably exists, and the probe either shows it or kills it. One ruling clears **three** rows: `[#370]` + `[#400]` (the rosters cell) + `[#413]` (the colours semantics). Note the standing hazard: `~/.claude` is global infra — the probe reads, it does not edit.
3. **Intake #18 ratification session (W-D)** — steward `[#435]`; **intake #19 §B rides it** (the clean-handoff contract; not citable until ratified there). Carried unchanged from the prior bundle: per-amendment ADOPT / DEFER / REJECT with a reason, then whether the spec cuts to v6.
4. **Intake #20 ratification session** — the North Star delta review. **This session MUST rule the §5 lesson-7 vehicle question.** *"Meta serves object"* is the **only** North Star item with neither a codified rule nor a BACKLOG row — every other lesson has at least a vehicle. Three ways out: file a row, codify it into PLAYBOOK, or record it as deliberately-not-a-rule. Any of the three is fine; leaving it is the one option the operator's own driver excludes — **nothing agreed gets lost**. Secondary question in the same doc: intake #16's lifecycle (still `DRAFT` with an empty `consumed-by:` though two consumers have shipped ADRs).

### DATED PRESSURE

- **2026-08-26 — drain prep + review.** Slice `[#356]` + `[#358]`–`[#361]`. **Architect prepares / operator ratifies** — the preparation is owed before the date, not on it. Full-pool intent (drain / mechanize / deliberately retire; staged, wholesale classes post-flip) is recorded in `[E8]`; the drain-owed-now list sits there too. Nothing has been drained.
- **2026-08-13 — W1 `.vscode` ruling shelf-life.** The nearer date. Carrier is declaration-only; the consumer write-through is the unbuilt half.
- **2026-08-26 — disposition review cluster.** Same date as the drain review; expect them to land in one session.

### CLOSURE-ELIGIBLE

- **`[#386]`** — still unclosed at bundle time (verified). PLAYBOOK §21 appears to state all three of its Done-when rules. Flagged across two JOURNAL entries and not yet reviewed. **Closure is the operator's `/review-closures` act (ADR-70)** — this is a pointer, not a verdict.

### CARRIED DEBT — delta vs the 2026-07-27 bundle

**Resolved since that bundle** (do not re-raise): the `[#436]` ratchet (built + closed); the drain-row selection (ruled D1); the `[#434]` branch deletion (word D2 given, executed, row closed).

**New this window:**
- **`[#437]` — the `CLOSES_RE` quoting defect.** `propose_closures` scans raw commit text, so backtick-quoted `closes [#N]` *prose about the convention* reads as a real closure. The sharp fact: **its own filing commit is now evidence against it** — the message quotes the offending sentence to document the bug, and the detector matched the quotation. The false-positive set therefore **grows every time anyone writes about the pattern**. The fix-lever already exists one file over in `validate_git_backlog`; this is shared-core divergence, not missing capability.
- **`[#438]` — gate-class posture, owed codification.** The posture is in force as a working rule; PLAYBOOK does not yet carry it. `[#437]` is itself gate-code, so it is the first candidate to run under it.

**Carried UNCHANGED — enumerated so none is silently dropped:** intake #18 ratification (`[#435]`) · intake #19 §B (rides #18) · `[#433]` restructure ADR stays open until engine + viewer + swap-out are ruled · `[#382]` receives the spike's seven schema findings **either way** · the ai-council **ADR-11 `#117` marker** (a different repo; raised in the prior bundle, still not executed — ADR-36/41 read-only discipline applies).

### STANDING RULES — unchanged

- **MERGE IS ATOMIC** — merge `--no-ff` + push + delete the source branch are one operation, no separate authorization. **New this window:** teardown covers **both** branches — the work branch *and* the `worktree-<name>` provisioning branch.
- **R8 is PARKED** — the operator's own pick, deliberately not delegated. Do not rule it for him.
- **Closure is an operator act (ADR-70)** — a row that meets its Done-when is *closure-eligible*, never closed by the session that noticed.
- **Gate-class: design review BEFORE build for refusal-gate arcs.** A fail-open passes every test and enforces nothing, so the suite cannot be what catches it. In force as posture; codification is `[#438]`.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
