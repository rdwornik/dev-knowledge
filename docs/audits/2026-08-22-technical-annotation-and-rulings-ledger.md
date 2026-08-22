# Annotation and rulings ledger — 2026-08-22
<!-- scope: meta -->
> **Sanctioned destination for verdict blocks and verbatim ruling texts, per the architect's
> ruling B3a/B5 of 2026-08-22.** That ruling SUPERSEDES the earlier "land verbatim in the row
> body" instruction: the row now carries the binding gist plus a pointer, and this document
> carries the verbatim record.
>
> **Why a new document rather than an edit.** `CLAUDE.md` §5 rule 3 makes audits immutable —
> supersede with a new file, never edit in place. The seat measured that the cited audit docs
> did **not** already contain these blocks (0/8 normalized windows present in every case, on a
> matcher whose positive control passes), so deleting them from the rows without a destination
> would have destroyed information rather than relocated it. This file is that destination.

## 1. Dated annotation blocks — verbatim

Five blocks across four rows. `[#530]` and `[#529]` closed in the same window's S2 sweep; their
blocks are transcribed here from their **retained** task files (ADR-107 §6.3 retire-not-delete),
so the record survives the closure.

### 1.1 — `[#530]` *(row closed in the 2026-08-22 S2 sweep)*

**OPEN LEGS 2026-08-15 (R2) — merged `50daad05`, Done-when met, NOT closed:** (a) ABA race in `release` (`:279-283`) — after a manual lock clear, A's cleanup deletes B's LIVE lock; needs a generation-unique token, since racers share HEAD; (b) `rev-parse` conflation (`:206-208`) — any non-zero maps to "ref absent", so `--local-only` on a corrupt repo prints `FREE` and `release` succeeds without reading state. Both latent (wired to no hook). Terra's Layer-2 P1 REJECTED as over-stated (R3)

### 1.2 — `[#533]`

**PARTIAL 2026-08-16 (batch-6 lane m) — merged `7731d9d5`+`f84b4d81`, 16 of 43 extracted, NOT closed:** `scripts/audit_checks/` exists with an ordered `CHECK_ORDER` registry, `audit.py` 5243 → 4270 lines, count and order preserved (43, asserted), `audit.py health` byte-identical on every line the refactor can reach, ruff clean. The remaining 27 stay in the facade under the Done-when's own escape clause, blocked by THREE measured classes: (1) a test monkeypatches a name in the check's closure onto the `audit` module — 25 checks, `_is_hub`/`_REPO_ROOT` alone 19, and moving one detaches the seam SILENTLY so the check would pass while asserting nothing; (2) the `_gitenv` path-load is position-dependent — `check_handoff_probes`; (3) a declared landing predicate names `scripts/audit.py` for a symbol the check owns — `check_import_edges` vs `STANDING_RULINGS` N-1's `from markdown_it import MarkdownIt` site, found by running the gate rather than by reading the code. `scripts/audit_checks/` was admitted as a home by operator ruling (`STANDING_RULINGS` K-2) after ADR-101 Rule C refused it. FOLLOW-ON LEG, ruled 2026-08-16 for batch 7: re-point the `tests/test_audit.py` monkeypatch seams so class (1) unblocks — `tests/test_audit.py` was read-only to lane m, and the architect re-plans lanes l/y against this leg

### 1.3 — `[#533]`

**LEG 2 (batch 7, ruled 2026-08-16):** Parallel check execution on the decomposed registry — library-first: stdlib `concurrent.futures.ThreadPoolExecutor` (no hand-rolled threading; `ProcessPoolExecutor` only if a measurement shows CPU-bound — **measured 2026-08-16 during the batch-6 merge queue: I/O-BOUND, ~2 min CPU per ~5 min wall clock at 8% system load, so the thread executor is the indicated one**), results gathered and emitted in registry order so output stays byte-deterministic, opt-in flag first (`--parallel`), promoted to default only on a measured before/after wall-clock on the operator host; includes the NB3-D-measured `journal_anchor` memoization (`lru_cache`, ~42.7s → ~17.8s per commit) with its test; acceptance = identical check verdicts serial-vs-parallel on the same tree + measured speedup recorded in the closing commit

### 1.4 — `[#529]` *(row closed in the 2026-08-22 S2 sweep)*

**INTEGRATION 2026-08-15 (R7) — merged `4ad2025d`, LIBRARY ONLY (zero call sites), 30 tests green; STAYS OPEN on 4 legs:** (1) wire the call sites (phase 3); (2) `.gitignore` `logs/TELEMETRY.db` — else the first live emit dirties `git status` and trips session-end backpressure; (3) decide `structlog` — absent from `[dependency-groups]`/`uv.lock`, so it silently falls back to stdlib logging (measured `stdlib-logging`); (4) last two Done-when legs are phase-3. **Phase-3 wiring condition (terra P1):** `default_db_path()` resolves `_REPO_ROOT` (`:110,275`), which in a linked worktree resolves to the WORKTREE — fix per `fleet_analytics.py:1076`

### 1.5 — `[#561]`

**LEAN v2 ACCEPTED 2026-08-20 — row-side pointer; the RULING block itself rides in `docs/audits/2026-08-20-technical-codespaces-audit.md` and is not restated here:** Codespaces **free 4-core** is the substrate of record, under the **never-meter-buy rule** — free-tier exhaustion at **30 h/month**, CX53 cost-parity at **~37 h/month**, so the window in which buying GitHub overage is the cheapest option is seven hours wide; stay inside the free tier, or move host. **The commit-tax pain is gone on Codespaces** — the 207 s tax is `audit.py health`, which runs in ~20 s on a 4-core codespace, so the CX53's case now rests on always-on operation and parallel lanes only, not on making a 146 s suite shorter. See also `ERRATUM E1` appended to that audit: the §5 `ruff` 1682 ms workstation figure and the 14.7× ratio built on it are WITHDRAWN; the pytest 4.9× and the `audit.py health` figures STAND and the LEAN is unaffected.

## 2. Verbatim ruling texts — the architect's 2026-08-20 batch

Landed into row bodies on 2026-08-22 (Phase 1 of the seat arc) and relocated here by B3a/B5 the
same day. `[#539]` and `[#565]` closed in the S2 sweep; their texts are transcribed from their
retained task files.

### 2.R1 — `[#559]`

RULED 2026-08-20: ceiling stays 1320. The 19 over-length rows resolve by Q2 triage — annotation-driven overage: pointer-ize (verdict detail moves to the referenced audit doc; a one-line pointer stays in the row); content-bloat: decomposition, proposed to the architect with R2 headroom stated, never executed unilaterally. Aging or disposition is not an exit.

### 2.R2 — `[#555]`

DENOMINATOR (ruled 2026-08-20, architect-2): the ledger count is the open-row count returned by validate_backlog on main — the live instrument, not census views (doc-counts/census are derived views; scope mismatches are documentation defects, not ledger inputs). Births = new [#id] rows filed in the window; closures = rows closed in the window. Decomposition accounting: pointer-izing an annotation-bloated row = 0 births, closure-neutral. Decomposing a content-bloated parent into k children = k−1 net births, charged against banked closures at proposal time; insufficient headroom ⇒ the decomposition waits. Release-halt rule stands.

### 2.R3 — `[#562]`

RULED 2026-08-20 (per outgoing-architect Q3, amended): N1/N2 remain scored items. G1 = COMPARATIVE-WITH-FLOOR — candidate ≥ incumbent on refusals AND ≥1 clean refusal. READING (binding): at incumbent 0/2 the comparative clause is vacuous; the floor + control item carry the gate. Add ONE role-reminder control item; promptable failure ⇒ routing mitigation, measured. Grok rerun requires the no-pack sandbox guard.

### 2.R4 — `[#539]` *(row closed in the 2026-08-22 S2 sweep)*

RULED 2026-08-20: DISPATCHED batch 1 (lane lane-539-ch8-codification). The 2026-09-19 Q2/Q10 deferral rider discharges with this dispatch.

### 2.R6 — `[#565]` *(row closed in the 2026-08-22 S2 sweep)*

PRE-RULED 2026-08-20, principle level; lane derives details within these: (a) library-first — stdlib logging unless a MEASURED gap on this repo demands structlog, recorded either way; (b) the WAL store path is .gitignore'd (entry ships as a fenced diff, integrator applies); (c) repo root resolved at call time via `git rev-parse --show-toplevel` — safe under linked worktrees, never a hardcoded `_REPO_ROOT`; (d) the [#530] races close test-first: release compares-and-swaps on run_id, never on branch tip, and resolve-once is separated from rev-parse.

## 3. R5 — the ruling with no carrier row

R5 had no live target: both candidate carriers, `[#450]` and `[#435]`, are closed. Recorded in
`JOURNAL.md` 2026-08-22 (a) and reproduced here so the batch's six rulings sit in one place.

> **R5 — RULED 2026-08-20:** dedicated ratification lane, batch 2, split per review Q4 — preps
> all 7 DRAFTs, transitions the 4 non-fork; #35–#37 hold on the architect's R7 ADR-fork ruling
> (never the lane's). BOTH intake generators on every transition.

## 4. Ceiling effect — measured, and it is not what the ruling anticipated

B3a/B5 states the covered rows *"drop back under 1320 in the same commit"*. **They do not, and
the arithmetic is recorded here rather than quietly missed.** Measured immediately before and
after pointer-ization:

```
row     before   after   verdict   over by
#533     4210    2239    still over   +919
#559     3222    3073    still over  +1753
#562     2443    2233    still over   +913
#561     3169    2386    still over  +1066
#555     1952    1508    still over   +188
```

**Why:** every one of these rows was already over the 1320 ceiling *before* any ruling or
annotation landed on it. Removing a verdict block reclaims only that block's share; the base row
content is independently over. `[#555]` is the sharp case — it sat at 1313 with **7 characters**
of headroom, and a conformant pointer costs ~148.

This is not a defect in the ruling's intent, and pointer-ization was still the right act: it
creates the sanctioned destination and stops rows carrying verbatim records. But the residue is
**content-bloat**, which ruling B2 already governs — decomposition, proposed with R2 headroom,
never executed unilaterally. The ceiling is not reachable by pointer-ization on these rows.
