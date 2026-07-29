---
intake-id: 21
status: SEED
origin: outgoing 2026-07-28/29 browser-architect seat, compiled after that window sealed at 376ee882; relayed by the operator and ingested 2026-07-30
note: >-
  Orientation snapshot, not a request for a build. Ingested under the intake convention so the
  repo can cite it at all; the taxonomy has no ORIENTATION class, so it lands SEED (the status a
  feed writes — README §8). READ THE DELTA TABLE FIRST: five of its claims were overtaken by the
  2026-07-30 window before this doc landed. The repo (tasks/, ADRs, audits) is the authority; on
  any conflict the repo wins — the artifact's own header says so.
consumers: >-
  the next browser-architect seat's orientation read; the [#446] §B(b) build arc (§1 critical path)
---

# Fleet tech status — browser-architect orientation (2026-07-30), ingested

> **Provenance.** Operator-held artifact compiled by the outgoing browser seat. It was
> **non-citable inside the repo** until this ingestion; it is now citable **only together with
> the delta table below**. Nothing here overrides repo state.

## Delta table — what this window moved before the snapshot landed

Verified live at `main` `c8c01c5f` (clean tree) on 2026-07-30. **Repo wins every row.**

| # | § | Artifact claim | Live repo state | Verdict |
|---|---|---|---|---|
| 1 | §1 | critical path still needs "the v6 sol spec" | the sol-produced v6 spec **DRAFT is on main** — `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md` (merged `4d492064`). NOT canon: `HANDOFF_PROCESS.md` stays `Version: 5.7`, the bump rides [#446] | **STALE** |
| 2 | §7 | "Pending operator words: W-D checkpoint verdicts A1/A2/A3/A6/A8/A9" | **all 11** amendment rows A1–A11 ruled and landed; verdict ledger in `docs/audits/2026-07-30-technical-intake18-ratification-record.md` | **STALE** |
| 3 | §7 | "U6(b) standing closure delegation = ADR-70 amendment, trigger: next `/review-closures` batch" | **NOT ADOPTED** (operator ruling 2026-07-30). Closures stay per-batch operator words; the trigger is **reset**, not pending. Recorded in the ratification record's dated amendment marker | **STALE — reversed** |
| 4 | §7 | dated ledger: "2026-08-13 `.vscode` … corp copy + e1 re-dates **queued** as cross-repo RULING-W arc" | **EXECUTED and merged.** corp-monorepo carries both `.vscode/settings.json` + `.vscode/extensions.json`; all three repos' `.vscode` declarations now read `review_date: 2026-08-26`. Record: `docs/audits/2026-07-30-technical-vscode-w1-execution-record.md` | **STALE** |
| 5 | §8 | debt ledger ends at #445 | **[#446]** (§B(b) v6 carrier build) and **[#447]** (self-referential gate family, 2 instances) filed since | **INCOMPLETE** |
| 6 | §2 | L3 "closure loop ×4" | **×5** — [#435] retired 2026-07-30 by operator-approved closure (this arc) | **STALE** |
| 7 | §7 | "[#433] stays open on §6.2 grounds (two concordant NOT-MET)" | **CONFIRMED unchanged.** ADR-107 §6.3 still self-declares Obligation 3 "RULED, NOT YET STRUCTURALLY DISCHARGED" | **ACCURATE** (recorded so the table is honest, not only corrective) |

**Verified accurate as written, no delta:** §3's `[#382]` charter on main and the
`#382 → #383 → #385` chain · §6's §3.2-vs-[#364]-4(a) tension (still live and unreconciled;
live code is `_BACKLOG_GROSS_CHARS = 1200`, `1597` appears nowhere in `scripts/`or `tests/`) ·
§6's arc-exit test still NOT MET · §4 intake #17 D1–D6 · §5 model fleet.

---

## The artifact, as received (verbatim below this line)

# Fleet tech status — browser-architect orientation (2026-07-30)

> **Provenance:** operator-held orientation artifact, compiled by the outgoing 2026-07-28/29 browser seat
> after the window sealed at `376ee882`. **Non-citable inside the repo** until ingested per the intake
> convention — the repo (tasks/, ADRs, audits) is the authority; on any conflict, repo wins.
> Purpose: what a browser-architect seat should hold in its head before any planning.

## 1. Critical path (the only sentence that matters)

**Flip ✓ (live-witnessed 07-28) → finish W-D (§B(b) build + v6 sol spec) → [#382] desired-state
contract → waves 4–7 unlock one after another.** Everything below [#382] — analytics, tech-currency,
prediction, repo deployment — waits on that single build. Standing recommendation (operator-endorsed):
after the ratification debt, no new audits — start [#382].

## 2. North Star layers L0–L5

| | Layer | State (2026-07-30) |
|---|---|---|
| 🟡↑ | L0 structure as managed state | flip live: `tasks/` = source of truth, BACKLOG generated, root hermetization gated; single desired-state contract still missing ([#382]) |
| ✅ | L1 dependency architecture | catching live: coherence gate, doc_rot, undeclared_edges all fired in-window |
| 🟡↑ | L2 versioning + deployment | first full anchored release exercised: plugin 0.1.11 lockstep ×3 repos, release-lint, cache-lag notice |
| 🟡↑ | L3 intake→ADR→build→archive | harness PROVEN end-to-end repeatedly (#20 ratified+consumed, #16 ruled, ADR-107 accepted→built→rows closed, closure loop ×4, `--prune` refuses); archive/safe_remove unbuilt |
| ❌ | L4 tech-currency lane | one manual instance (uv); no lane |
| ❌ | L5 predictive layer | 0% |

## 3. Terraform model & libraries

| | Element | State |
|---|---|---|
| ❌ | pydantic desired-state contract | **[#382] charter ON MAIN**; sizing 08-26; pull-forward option flagged; chain head, unbuilt |
| ❌ | networkx graph · pandas divergence report | not started (chain: #382 → #383 → #385) |
| ✅ | regenerate-and-diff + carriers · deployed-versions pin | exist |
| 🟡 | drift detection | producer alive; consumer [#428] unbuilt |
| ❌ | PyDriller (L5a) · scikit-learn (L5b) | not started; #384 closed w/ live carve-out #391–#394 |

## 4. Intake #17 D1–D6

D5 strangler **✅ flip executed + witnessed** (step 4 prose relocation deliberately deferred) ·
D1 🟡 plugin surfaces now branch on host shape; dedicated two-format validate leg unverified ·
D2 🟡 main arc ✅, AGENTS.md sitting ❌ · D3 ❌ PLAN.md states + SLA · D4 ❌ AGENTS.md ADR ·
D6 ❓ child-roster unconfirmed.

## 5. Model fleet

Gemini lane ❌ (R-G open) · grok shadow ❌ (R-S open; terra carried all reviews) · Copilot ✅ held ·
ADR-105 no-lane-without-consumer guard ✅ — used in anger twice this window (lesson-7 enforcement
map; night-routine activation refused).

## 6. Scoring / Fibonacci (§3–§4) + named tensions

All mechanism ❌ (scale, score formula, re-scoring, sticky override, verified_by, READY.md, graph,
boot probe). **Open tension filed for the 08-26 build:** §3.2 ruled ceiling 1200→1597 (never landed)
vs this window's adopted [#364] option 4(a) (no cap change; linked-file + pre-write measurement) —
two rulings in conflict; reconcile before building either.

**Arc exit test (§5) — still NOT MET:** "fresh session boots; FIRST message cites top-5 ready-set
with reasons + every ruling overdue >8 days; zero operator memory." Boot half is materializing now
(§B(b) one-round-trip, U1 GO, v6 cut ruled); ready-set half needs the scoring mechanism + [#382] era.

## 7. Browser-seat obligations (what the seat owes, not what CC owes)

- **Pending operator words:** W-D checkpoint verdicts A1/A2/A3/A6/A8/A9 (with plain briefs) ·
  U6(b) standing closure delegation = ADR-70 amendment, trigger: next /review-closures batch.
- **Dated ledger:** 2026-08-13 `.vscode` (ruled (b); corp copy + e1 re-dates queued as cross-repo
  RULING-W arc) · **2026-08-26 cluster**: drain slice [#356]+[#358]–[#361] (prep artifact on main),
  D-QUEUE 26 rows, [#364] 4(a) build + §3.2 reconciliation, mechanism date for the .vscode carrier,
  disposition reviews.
- **Do-not-redo / do-not-relitigate:** flip mechanics · shared closure-token core · #20/#16 rulings ·
  .vscode option (b) · Ch8 four-condition launch test (ADOPTED) · stale-procedure rows 1–12 ·
  [#433] stays open on §6.2 grounds (two concordant NOT-MET) · night-work-as-routine (routes via
  #19 §B rider, trigger: next night-batch request).
- **Method now doctrinal (PLAYBOOK Ch8):** fat-prompt default; parallelism inside the session;
  every git mutation serial; worktrees behind the four-condition ALL-YES test; Codex lane named in
  every plan (terra default review · sol adversarial derivations · luna read-only fan-out; wrapper
  caveat [#445] — verify the review consumed the diff); JOURNAL letters assign-at-integration,
  pre-allocate only inside a sanctioned pair's dispatch; per-arc frozen A–H contracts; closure =
  operator act (batch delegation only by explicit word, batch-scoped); cap measured pre-write
  (1200 gross + ≥3-ISO-dates&>700 leg).
- **Environment classes:** cloud night lane = no `~/.claude`, no Codex → branch-only,
  UNVERIFIED-until-local · plugin cache = two-layer staleness ([#442]) · `owner=user` third
  ownership state ruled (governs-vs-contains sub-question open inside #370 disposition).

## 8. Debt ledger delta (this window)

**Closed (full loop):** #386 · #434 · #436 · #437 · #439 · #444.
**New mechanism debt (filed with evidence):** #440 id-ledger tombstone · #442 plugin-cache
staleness · #443 planning-artifact rent · #445 codex-review path-guard.
**Future intake (operator's, must not be lost):** one consolidated browser-seat operating-knowledge
update (prompting, repo management, methodology, planning) — AFTER the [#382] chain lands; half
overlaps intake #18/v6 + [#443]. Prove, then codify.
