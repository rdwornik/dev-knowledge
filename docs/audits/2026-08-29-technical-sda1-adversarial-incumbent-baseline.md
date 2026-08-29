# SDA-1 adversarial incumbent baseline — copilot-enterprise run

Run 2026-08-29T18:37:57Z · provider copilot-enterprise · model claude-sonnet-5 · identity Robert-Dwornik_ghub

- **Consumed by:** `[#492]` (grok review-lane acceptance — this run supplies the measured
  incumbent baseline its comparison needs), the A2 fallback-chain clause in
  `protocols/PLAYBOOK.md` (every fallback model owes the SDA-1 reviewer-role gate as its
  measured admission row), and `ecosystem/provider-registry.yaml`'s `copilot-enterprise`
  entry, whose `producer: refused-pending-sda1` field is the thing this baseline is
  measured against.
- **What it is:** the incumbent baseline itself, not a verdict. C-2's floors were recorded
  UNCALIBRATED because nobody had run this pack as a baseline; the calibration rule it
  states at the foot is what future runs are scored against.


## SDA-1 Adversarial Baseline Run — Incumbent Score

Treating Pack 1 §9 (C‑1…C‑15) as the adversarial item set, "the design" = SDA‑1 as specified in §§1–8, with Packs 2/3 (the analysis‑role freeze + landed item pack) used as the only actual execution evidence available for judging whether proposed fixes were *implemented* or merely *proposed*.

| Sev | Item | Attack | Survives? | Evidence |
|---|---|---|---|---|
| 🔴 CRIT | C-1 | Producer gate measures correctness; P5 ratio hides rejected-patch cost | **NO** | §4.2 P5 still divides by *accepted* patches; §10 self-admits "not safe to run for producer role" |
| 🔴 CRIT | C-2 | Absolute floors invented, no calibration | **PARTIAL** | Pack2 §4/§7 does print `UNCALIBRATED` beside N1 and shows the live 400 billing re-check (`req_011CeWnLW9y4qixTcbaZuUdG`) — fix(b) applied for analysis role only; producer/adversarial roles unfixed |
| 🔴 CRIT | C-3 | Corpus structurally excludes omission/architecture/doctrine defects | **NO** | Pack3 has 0 items targeting D16-class omission; no mutation-survivor tier built (Pack2 §9 lim.3: "sizes a probe, not an acceptance") |
| 🟠 HIGH | C-4 | Pass-by-luck; k=3 needed | **NO** | Pack3 ran k=1, flagged as the predicted first cut (§ header, §9 lim.1) |
| 🟠 HIGH | C-5 | Fan-out bar leaks via shared preamble/scorer/adjudicator | **PARTIAL** | Pack2 §2 authors Φ_analysis with hedge carve-outs (fix ii applied); no preamble sha256 or blinding evidence (fixes i, iii unmet) |
| 🟠 HIGH | C-6 | Green-by-skip cheats evade diff-scope filter | **NO** | §10 explicitly states the second adversarial suite "does not yet exist" |
| 🟠 HIGH | C-7 | Hand-adjudication/cap-exhaustion silently resolved | **YES** | Pack2 §3 adds EXHAUSTED as a third, never-PASS/FAIL outcome + cell-level INDETERMINATE, verbatim per fix |
| 🟠 HIGH | C-8 | Incommensurable cost regimes erased by one ratio | **YES** | Pack2 §5 Q7 tags agy `subscription`, refuses to compute $ |
| 🟡 MED | C-9 | Q2 served-id probe fails on CLI providers (agy named) | **YES, w/ residue** | Pack2 §6 runs a measured per-item log-line pre-flight, decision recorded deliberately, residue stated |
| 🟡 MED | C-10 | Instruction-file precedence unmeasured for most providers | **NO** | No precedence pre-flight recorded anywhere in Pack2 preconditions |
| 🟡 MED | C-11 | No long-context/long-loop tier | **NO** | All 10 Pack3 items are single-shot; no round-distribution reported |
| 🟡 MED | C-12 | Passing score doesn't predict real-use behavior | **NO** | No shadow-trial gating mentioned for this lane |
| 🟡 MED | C-13 | Corpus leakage from reused/committed material | **NO, admitted** | Pack3 §9 lim.4 states leakage "total and unavoidable"; §1 shows agy actually located and quoted the census file answering N-04 |
| ⚪ LOW | C-14 | Binary verdicts discard per-defect-class signal | **NO** | N1–N6 remain aggregate floors; no breakdown table produced |
| ⚪ LOW | C-15 | No named owner for weakening load-bearing elements | **NO** | k=3→k=1 weakening occurred with only a self-logged limitation, no named sign-off |

TALLY Critical=3 High=5 Medium=5 Low=2

Survival scorecard: **2 full survives** (C-7, C-8), **3 partial** (C-2, C-5, C-9), **10 fail** (C-1, C-3, C-4, C-6, C-10–C-15). All 3 Criticals remain unresolved at the design level (§10's own verdict stands); only the analysis-role lane (Packs 2/3) shows genuine, evidenced mitigation, and only for a subset of the High/Medium items.

BASELINE-CALIBRATION: future SDA-1 revisions (or new role packs) should be re-run against this same 15-item C-1…C-15 set and scored NO/PARTIAL/YES per row exactly as above; a revision only earns "improved" if it flips any of the 10 current NOs to YES/PARTIAL without regressing C-7/C-8/C-9 (the only rows currently surviving), and no producer-role `ADMIT` may be trusted until C-1, C-2, and C-3 each show a YES with cited implementation evidence (not a proposed fix in prose).



Changes    +0 -0
AI Credits 21.15 (1m 38s)
Tokens     ↑ 51.3k (51.3k written) • ↓ 8.3k (6.5k reasoning)
Resume     copilot --resume=9a7259c1-f3b5-417e-a101-c8c994c61930
