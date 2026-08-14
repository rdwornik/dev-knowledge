# Residual — 2026-08-14-dev-knowledge-architect — the part the repo does not already encode

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
**STANDING / dispositioned — none of these is new this window** (dispositions live in
`ecosystem/disposition-register.yaml`; re-derive every value via P4/P6/P7/P9):

- The `undeclared_edges` prose-edge family (ADR-88 FC2) — owned by `[#241]`, cardinality-free
  Done-when so the set grows without re-breaking the row.
- `preflight_backlog_ids` — advisory per the `[#483]` R3 ruling.
- `review_artifact_coverage` — advisory per the `[#480]` P3 ruling, deferred pending 0 false
  positives over two consecutive windows.
- `journal_spine_anchor` "anchored by mention, not by record" — the advisory leg built under
  CODEX-524 leg (c) / L5; WARN-not-FAIL by design.
- `no_ff_merges` — three legacy June non-merge spine commits, grandfathered. **Never rewrite them.**
- `doc_rot` backlog-accretion on the large rows (`[#511]` `[#510]` `[#514]` `[#522]` `[#505]`
  `[#322]`) — the condense route is `[#426]`/grooming territory, not an in-window fix.

**NEW THIS WINDOW, RESOLVED BY CORRECTION:** the 2026-08-14 batch-4 TRUE close packet
(`docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §5) named **five** `claude/*`
branches as "the next window's inheritance" — `claude/nc-lessons-mechanisms-jw5dda`,
`claude/nd-governance-promotion-prune-77qc6b`, `claude/night-nb-handoff-prep`,
`claude/night-ne-northstar-value`, `claude/window-truth-audit-yr83j2`. This seat confirmed
(twice, via `git branch -a` after `fetch --prune` and `gh api repos/rdwornik/dev-knowledge/
branches`) that **none of the five exist on `origin`** — only `main` and `automation/
fleet-audit` remain. **`SUPPLEMENT.md`'s correction addendum resolves this**: all five were
verified branch-by-branch and deliberately deleted (verdict SUPERSEDED-DELETE — none was an
ancestor of `main`), with every actionable item individually dispositioned in
`STANDING_RULINGS.md` §L/§M (the 143/143 adjudication, tables M-1..M-11 — both confirmed
present in-repo). The per-branch deletion evidence itself is an **off-repo operator record**,
so it is advisory rather than re-derivable here — but the repo-verifiable half (branch
non-existence + the §L/§M disposition tables) checks out. Nothing was lost; the TRUE-close
packet's "next window's inheritance" phrasing is superseded, not this session's to edit
(`docs/audits/` is immutable).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
| id / artifact | Where |
|---|---|
| Batch-4 **TRUE close packet** — corrects FLAG-1's carried count now `[#513]` discharged; CLOSED `[#270]`/`[#132]`/`[#521]`/`[#513]`, CARRIED `[#514]`/`[#510]` | `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md`; commit `e4e1624b` |
| `doc_rot` dual-instrument claim corrected — no disposition-register suppression exists in code (one instrument, not two) | `STANDING_RULINGS.md` §O-1/O-2; commit `90daea1e` |
| Usage-telemetry design memo landed + attached as a LEG on intake #29 Fold A (v1-EMIT slice) | `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`; commit `c3c7aa90` |
| `[#526]`/`[#527]`/`[#528]` **born** (root-hygiene audit P3/S, anti-direct-to-main hook P2/S, lane-latency gate-mesh cost P1/M) + a leg on `[#523]` | `tasks/526-*.md`/`527-*.md`/`528-*.md`, `BACKLOG.md`; commits `30c1ed91`/`2588d07d`/`50e9f251`/`d63a6dc6` |
| `[#511]` three-loads split ruled **DEFERRED**, stays unsplit P2/M — "JOURNAL-purpose" load has no located scope anywhere in the tree | `STANDING_RULINGS.md` N2-E3-06 |
| ADR-112 bullet added to `ARCHITECTURE.md`'s Governing-ADRs list | commit `d63a6dc6` |
| 4 LESSONS entries appended — duplicate-execution, unlocated register loads, doc_rot dual-instrument, serialize-group derivation | `LESSONS.md`; commit `eac92922` |
| PR #67 merged `worktree-packet-close` → `main`, one commit per step | `65bdd836` |
| W4 wave-1 arithmetic: 69 live ids, 39 converted / 30 skipped, no skip silent | `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §3 |
| Two duplicate-execution artifacts (independent runs of the SAME packet-close contract, colliding on `[#526]`-`[#529]` numbering) flagged, **not merged**: `docs/packet-close`, `docs/packet-close-v2` — both now absent from `origin` post-PR-67 | JOURNAL 2026-08-14 (d) |

Detail is in `JOURNAL.md` 2026-08-14 (d)/(c); this is the map, not the recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Three items, ordered by what blocks what — this session's own residual, distinct from
`SUPPLEMENT.md` (pointer, not a duplicate; its answers are folded into `PASTE_THIS.md`).**

1. **THE 5-BRANCH NIGHT-LANE SET IS RESOLVED, NOT OPEN.** §1 above records the correction:
   `SUPPLEMENT.md`'s addendum confirms deliberate SUPERSEDED-DELETE with every actionable item
   dispositioned in `STANDING_RULINGS.md` §L/§M. The remaining open question for `[#511]`'s I-D4
   continuity legs (R43/R50/R51) is narrower than "was this lost" — it is whether those
   distillate rows' own text still accurately cites what the (now-deleted) branches carried, a
   normal staleness check, not a recovery investigation.

2. **`SUPPLEMENT.md` §2 NAMES A CONCRETE NEXT-WINDOW MECHANISM CANDIDATE** — a single-flight
   dispatch guard against contract-of-record collision, born from this window's own near-miss
   (three concurrent executions of the packet-close contract; one caught and stopped via
   `TaskStop` before it merged anything; all three colliding on `[#526]`-`[#529]` numbering for
   the same four filings). It is a candidate, not a ruled row — whether it becomes a `[#id]` is
   the next architect's call.

3. **THE E1-5/L-9 TIMING CLAUSE DISCHARGES WITH THIS CUT.** `protocols/STANDING_RULINGS.md` L-9
   ("Clause 5 (handoff cut < 10 min) discharges by timing the very next cut") is satisfied by
   this bundle's own generation — the measured wall-clock is in this session's closing packet to
   the operator, not restated here. Whether the result clears the 10-minute bar, and what that
   implies for `[#511]`'s re-scoped non-mechanized load, is the next architect's read to make,
   not this cut's to adjudicate.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
