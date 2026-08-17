# Residual — 2026-08-17-dev-knowledge-architect-3 — the part the repo does not already encode

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
**Standing and register-dispositioned** (`ecosystem/disposition-register.yaml`), so a flag in these classes is expected rather than news: the ADR-88 FC2 `undeclared_edges` prose-edge class against the `handoff-process` and `prompt-template` specs, and the legacy `no_ff_merges` entries for the pre-floor journal/transcript wrap commits. Do not re-disposition these — they carry their reasons in the register.

**Standing and advisory BY RULING, not by register.** A different thing, and the distinction is load-bearing because these will never appear in the register no matter how long they persist: `review_artifact_coverage` (both legs) is advisory per the `[#480]` P3 ruling, its hard pre-push leg deliberately deferred pending two consecutive clean windows; and `journal_spine_anchor`'s *anchored-by-mention-not-by-record* leg is advisory per N2-L5 (`[#524]` leg c) and never changes that check's pass/fail verdict.

**New this window, and self-inflicted — recorded here rather than left to be discovered.** The two births `[#554]` and `[#555]` each exceed `doc_rot`'s declared `backlog-row-length` ceiling, so this window ADDED members to that class. They add nothing to the `backlog-accretion` ARM class, because a newly born row has a single history date, so the owned suite RED's condition — accretion findings present, not merely length findings — was not worsened by them. **But that RED's locus set has grown past what the prior supplement recorded:** it named a single accreting row, and the live corpus now carries several, `[#553]` among them. Re-derive the set; do not inherit the single-locus framing.

**The two OWNED suite REDs are unchanged in kind and still owned** — the `routine_consumers` live-corpus pin (which asserts an exact routine-row population that the batch was explicitly told to grow) and the `doc_rot` accretion pin above. Neither is a defect detector firing on a defect; both are pins tracking a corpus that keeps moving, which is exactly why they are owned rather than dispositioned.

**Everything quantitative is deliberately absent from this file** — no verdict, no counts, no `[stale]` status, no shas, no drifted ids. `PROBES.md` P4/P6/P7/P9 re-derive them at check-time; a value written here would be bluffable from a summary and would invert the anti-bluff contract this bundle exists to hold.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
- **Lane r merged** (`worktree-lane-r-412-research-intake`, new-files-only) — five EXTERNAL EVIDENCE browser-research artifacts into `docs/archive/`, intakes **#35–#39** into `docs/intake/` at `status: DRAFT`, and the lane's contract of record into `docs/audits/`. References `[#412]`; **does not close it** — that row's Done-when also wants a routing doctrine in `protocols/PLAYBOOK.md`.
- **Two births** — `[#554]` devcontainer + provisioning script (NB4-G stage 1) and `[#555]` closing campaign batch 1 + the kill-candidates instrument. Each discharges one *NO ROW — file it first* entry in the amended plan.
- **The 08-17 supplement amended** to priority order v2 and marked **INPUT, not the handoff** — additive only, per the handoff-immutability rule, so the ranking first ruled stays legible beside the one ruled after.
- **The last lane worktree and branch torn down**, so no `worktree-lane-*` branch exists. That teardown is what discharges the `[#510]` honest exception: the ADR-110 anchoring exemption keys on lane-branch SHAPE, so it is self-grantable only while such a branch exists, and it evaporates at closure.
- Detail lives in `JOURNAL.md` **2026-08-17 (e)** and this arc's commits; the rows live in `BACKLOG.md`. This is a map, not a recap — the JOURNAL already encodes the reasoning.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Carried and deliberately deferred — resume these, do not relitigate them:** the consumer-side home for `[#293]` (candidates await one ruling); the final seam re-point shape for the monkeypatch-pinned checks (smallest-diff versus a shared seams module, nb5-A on the table); the class-3 N-1 landing-predicate re-point, which is governance and separate from the seam leg; the telemetry read-path stack (D3-first is ruled — datasette versus static HTML is decided only **after** `[#529]` wiring emits real data); the routing-table amendment, gated on NB4-A seeded-defect acceptance plus the `[#492]` Grok browser check — **that peg was due 2026-08-17 and repo evidence said not-released as of 08-10, so assume it may be unmet**; and the audit-corpus `status:`-frontmatter proposal versus ADR-100's files-never-move stance, filed and unratified.

**Opened by this arc — each is a decision this seat owns, not a task:**

1. **The `doc_rot` row-length ceiling versus actual practice.** The declared ceiling sits far below what recent rows actually run, and the two births are now among the longest rows in the corpus. The standing stance is that `doc_rot` is greened by FIXES and never by dispositions — so either the ceiling is wrong and moves, or long rows get decomposed. Left undecided, every future birth adds a finding to a class that is meant to be shrinking. This was created knowingly: the row content was authorized, and trimming it to the ceiling would have cost the load-bearing reasoning, so the tension is escalated rather than silently absorbed in either direction.

2. **Which row owns the unshallow and the `uv`-pin assert.** `[#554]` and `[#453]` overlap on two of four legs — found by checking the *nothing owns this* premise instead of accepting it. `[#554]`'s clause says whichever lands second discharges by pointing at the first; that is a convention this seat can ratify or replace, not a decision already made.

3. **One denominator predicate.** Three counts of the same backlog are in circulation — the open set from `tasks/` frontmatter, the rendered `BACKLOG.md` bullet count, and the `SessionStart` load gauge, which agrees with neither. `[#555]` makes naming one predicate its first act; until that lands, any *net-negative* claim is unfalsifiable.

4. **Who performs promotion.** `assemble_paste.py` flagged ruling-bearing lines in the folded ANSWERS as promotion debt, and answer 7 names durable homes for six ratified terms (PLAYBOOK §8 / §8b / batch-protocol / batch-close, and intake #39). The homes are named; the promotion **act** is unowned — the same decided-unfiled failure mode the amended plan flags twice.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
