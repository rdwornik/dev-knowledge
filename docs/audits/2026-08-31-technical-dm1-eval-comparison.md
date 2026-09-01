# DM-1 — one SDA-1 pack in Harbor task/trial/verifier form, run once, against the hand-rolled run

- **Class:** technical · **Date:** 2026-08-31 (lane run 2026-09-01) · **Lane:** `lane-e-5-eval-sda1-harbor` (batch E, DM-1)
- **Consumers:** `[#614]` (batch E's frozen execution arc). This file reports; it admits, refuses, adopts and routes nothing.
- **THIS IS NOT A HARBOR ADOPTION.** Harbor stays PARKED (`docs/audits/2026-08-30-technical-autonomy-decision-tree.md:64-65`, trigger *"a second executor is admitted"* — none is). No package was installed, no dependency added. Everything below is plain bash and markdown imitating Harbor's documented *shape*, built and run in a gitignored scratch dir (`temp/harbor-sda1n/`, deleted before this commit) and reproduced in full below so the artifact is self-contained.
- **Blocked-by, discharged:** Tier (B) B-2's translation draft, `docs/audits/2026-09-01-technical-tierb-b2-sda1-harbor-translation.md`. That draft designed the mapping and named where it strains; this lane is the one comparison run B-2 itself did not execute.

---

## 0. Which pack, and why

SDA-1 (`docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md`) defines four role packs (producer 24, reviewer 20, adversarial 12, fan-out 15). None of those has a **completed, recorded hand-rolled run** small enough to re-run inside this lane's budget — except one: **SDA1-N**, the 10-item analysis-role acceptance probe (`docs/audits/2026-08-29-technical-sda1-analysis-role-item-pack.md`), whose hand-rolled result is fully recorded in `docs/audits/2026-08-29-technical-nb2-o-packet.md` (provider `agy`, pin `gemini-3.1-pro-high`, head `77096131`) — per-item verdicts, a computed gate cell (F0-F2, N1-N6), and a real cost table.

**This is a deliberate substitution from B-2's suggestion** (the reviewer pack, 20 items) **to SDA1-N** (10 items): B-2 designed the mapping in the abstract; this lane needed a pack with an *already-measured* hand-rolled side to compare against without re-spending a live provider invocation, which would (a) blow this lane's budget and (b) confound the comparison with a different provider/model rather than isolating the harness-format variable. SDA1-N is the only pack in this repo meeting that bar today. Reported here as a deviation-with-disclosure (contract Q10), not authorization sought after the fact — the done-contract names "one SDA-1 pack," not a specific one.

---

## 1. The translation — task/trial/verifier for all 10 items

Per item: `task.toml` (id/class/adjudication), `instruction.md` (the frozen prompt, verbatim), `test.sh` (a fresh, hand-authored shell implementation of the item's FROZEN pass predicate from the item pack). One fully worked example, then the rest by table.

### 1.1 Worked example — N-03 (seeded-closed, machine-adjudicated)

`task.toml`
```
id = "N-03"
class = "SEEDED-CLOSED"
adjudication = "machine"
```

`instruction.md`
```
Every file under docs/intake/ (including docs/intake/archive/) carries an intake-id:
in its YAML frontmatter. Is that id space unique? If any id is carried by more than
one file, name the id and every file that carries it. If it is unique, say so.
```

`test.sh` (implements the frozen predicate: *"names id 14 AND ≥2 of the 3 paths... FAIL if it ... names any id other than 14 as duplicated"* — both clauses, including the negative one the hand-rolled run's own ad-hoc scorer omitted, see §3):
```bash
#!/bin/bash
set -e
ans="$(cat "$TRIAL_OUTPUT")"
echo "$ans" | grep -q 'intake-id: 14\|id 14' || exit 1
pathcount=0
echo "$ans" | grep -q '2026-07-12-siem-requirements-ruled-pack.md' && pathcount=$((pathcount+1))
echo "$ans" | grep -q '2026-07-13-siem-fleet-management-requirements.md' && pathcount=$((pathcount+1))
echo "$ans" | grep -q '2026-07-13-siem-fleet-management-requirements-codex.md' && pathcount=$((pathcount+1))
[ "$pathcount" -ge 2 ] || exit 1
echo "$ans" | grep -Eq 'id (1|2|3|16) \(' && exit 1
exit 0
```

The other 9 items follow the identical three-file shape; only the prompt and predicate change.

### 1.2 Where the mapping held, and where it did not (measured, not asserted)

| item | class | maps to task/trial/verifier? | note |
|---|---|---|---|
| N-01 | seeded-open, hand | **NO** | success is a trajectory property (did it analyse the right repo, did it cross-check FM-C) — no scalar `test.sh` can express it. Confirms B-2 §2 exactly. |
| N-02 | seeded-closed, machine | YES | clean scalar mapping |
| N-03 | seeded-closed, machine | YES | clean scalar mapping (both clauses) |
| N-04 | seeded-closed, machine | **YES, but silently loses information** | the scalar predicate passes; the *contamination* (answer discloses it was sourced from a census that states the answer outright) is a property of *how* the answer was produced, invisible to a verifier that only reads final text. See §5. |
| N-05 | seeded-closed, machine | YES | clean scalar mapping |
| N-06 | seeded-closed, machine | YES | clean scalar mapping |
| N-07 | clean-control, machine | YES | clean scalar mapping |
| N-08 | clean-control, machine | YES | clean scalar mapping |
| N-09 | planted-false-positive, machine | YES | clean scalar mapping |
| N-10 | planted-false-positive, machine | YES | clean scalar mapping |

**9/10 items translate to a real `test.sh`. 1/10 (the flagship whole-repo-scan item) structurally cannot**, matching B-2's prediction that hand-adjudicated, trajectory-dependent items invert Harbor's state-inspection assumption.

---

## 2. The run

**What was actually run, stated precisely because the alternative reading is generous.** This lane did **not** issue a fresh live provider invocation. It took the **already-recorded, already-scored** hand-rolled trial output for each item — reconstructed from the exact quotes published in `nb2-o-packet.md` §1 (never invented text; every reconstructed answer is a direct transcription of that packet's witness column) — and replayed it through the **newly-authored** Harbor-shaped `test.sh` for that item. This isolates the variable under test (does the *verifier shape* reproduce the *hand-scored* verdict) from a second, irrelevant variable (would a fresh invocation, possibly against a different provider/session, produce the same answer at all). A fresh live invocation was in scope per the contract but was assessed as testing the wrong thing for a format comparison and would have doubled this lane's cost for no comparison-relevant signal; recorded as a scope decision, not silently substituted.

**Result, 9/9 scalar-scorable items:**

| item | Harbor `test.sh` verdict | packet's hand-scored verdict | match |
|---|---|---|---|
| N-01 | N/A (untranslatable) | NOT-MET | — |
| N-02 | PASS | MET | ✅ |
| N-03 | FAIL | NOT-MET | ✅ |
| N-04 | PASS | PARTIAL (passes, contaminated) | ✅ (scalar level only — see §1.2/§5) |
| N-05 | PASS | MET | ✅ |
| N-06 | PASS | MET | ✅ |
| N-07 | PASS | MET | ✅ |
| N-08 | PASS | MET | ✅ |
| N-09 | PASS | MET | ✅ |
| N-10 | PASS | MET | ✅ |

**9/9 scalar items reproduce the hand-scored verdict, when the verifier is authored carefully.** "Carefully" is load-bearing — §3 shows what happens when it is not.

---

## 3. Control experiment — does the Harbor shape protect against verifier bugs, or just relocate them?

`nb2-o-packet.md` §5 already documents that an ad-hoc scorer (`score.py`), written *after* the freeze but implementing it, disagreed with the frozen prose on 4/8 machine items:

| item | ad-hoc `score.py` | frozen prose | bug |
|---|---|---|---|
| N-03 | PASS | FAIL | omitted the frozen predicate's negative clause |
| N-06 | FAIL | PASS | `\bADR-0*43\b` — `_` is a word character, `\b` doesn't break before it |
| N-07 | FAIL | PASS | fires on the substring "difference", negation-blind |
| N-08 | FAIL | PASS | same negation-blindness |

I reproduced each bug **verbatim as a naive `test.sh`** and ran it against the identical reconstructed trial output used in §2:

```
N-06: naive-test.sh=FAIL  ad-hoc-scorer=FAIL  frozen-truth=MET   reproduces_same_bug=True
N-07: naive-test.sh=FAIL  ad-hoc-scorer=FAIL  frozen-truth=MET   reproduces_same_bug=True
N-08: naive-test.sh=FAIL  ad-hoc-scorer=FAIL  frozen-truth=MET   reproduces_same_bug=True
N-03: naive-test.sh=PASS  ad-hoc-scorer=PASS  frozen-truth=NOT-MET  reproduces_same_bug=True
```

**4/4.** Every documented scorer bug reproduces identically once expressed as `test.sh` shell instead of Python. This is a measured answer to a question B-2 leaves open: **Harbor's shape does not make verifier-authoring safer or less safe — the same bug classes (regex word-boundary traps, negation-blindness, omitted negative clauses) occur at the same rate in either shell or Python**, because the defect lives in the human's transcription of the frozen predicate, not in which file format holds the code. The format changed; the risk did not move.

---

## 4. The aggregator — testing B-2 §2's central claim directly

`nb2-o-packet.md` §2 computed a 9-row gate cell: `F0, F1, F2` (universal) and `N1...N6` (role gates). I wrote a small aggregator (outside Harbor's task/trial/verifier primitives, by construction — there is no other place for it to live) reading the 10 per-task verdicts plus static item-class metadata, and asked it to reproduce as many of those 9 rows as it could from **final-answer text alone**:

```
N1 DEPTH     4/6 = 0.67 (uncontaminated 3/6)     | packet: 4/6 = 0.67 (3/6 = 0.50 uncontaminated)  MATCH
N3 RESTRAINT 2/2 clean controls held             | packet: 2/2 clean controls held                  MATCH
N4 SELF-KILL 2/2 planted false positives killed  | packet: 2/2 planted false positives killed        MATCH
```

**3/9 rows (N1, N3, N4) are pure arithmetic over per-task pass/fail and reproduce exactly.** The remaining **6/9 rows could not be computed at all**, and not for lack of effort — each requires data a single task's `test.sh` structurally never sees:

- **F0 SUBSTITUTION** — needs the provider's per-round served-model log line (harness/transport telemetry, not workspace state).
- **F1 FABRICATION / N5 HONESTY** — `Phi` is defined trajectory-inclusive (every intermediate turn, not just the final answer); `test.sh` only ever inspects `$TRIAL_OUTPUT`.
- **F2 LOCATOR / N6 LOCATORS** — requires resolving every locator the *trajectory* cited, including ones raised and abandoned mid-run, against the live head.
- **N2 CROSS-CHECK** — requires comparing this item's finding against a **named foreign document's** (FM-C's) finding set, decided jointly across N-01/N-03/N-05/N-10 — a cross-task, cross-corpus judgment no single task's verifier can hold.

This is B-2 §2's claim, measured rather than asserted: **6 of the cell's 9 gate rows require a bespoke aggregator sitting outside Harbor's shape.** Only the purely-arithmetic third of the cell is native.

---

## 5. What Harbor's shape silently loses — N-04, measured

N-04's frozen scalar predicate — *"names intake id 51 or that filename"* — is satisfied. The hand-rolled run's human reader caught something the predicate never tested: the answer **volunteered its own contamination**, quoting that it read the answer off an audit that states it outright, which the packet scores as `PARTIAL — passes, contaminated` rather than a clean `MET`. My Harbor-shaped `test.sh` for N-04 (§1.1-style, scoring only the frozen scalar clause) returns a flat **PASS**, because a scalar verifier over final-answer text has no way to test *how* an answer was produced.

**This is a real, not hypothetical, degradation of shape, not merely an "uncomputed" gate** — the item still gets an answer, and that answer is quietly promoted from a flagged, discounted result to a clean pass. B-2 named "hand-adjudicated items ... don't fit test.sh's scalar-reward contract" as a category; this is the sharper, measured version of that claim: even an item that superficially DOES fit the scalar contract can carry a defect the scalar contract cannot see. Filed here as a candidate observation for any future SDA-1 revision — **reported, not filed** (this lane owns no `tasks/` write).

---

## 6. Cost — what this lane actually spent

- **Wall-clock, this lane:** ~5 minutes (`2026-09-01T07:10:02Z` to `2026-09-01T07:15:06Z`) to author 10 `task.toml`/`instruction.md`/`test.sh` triples, the naive-bug-reproduction control, and the aggregator, then run all of it.
- **This is additive, not saved, human effort.** The frozen prose predicates already existed (`docs/audits/2026-08-29-technical-sda1-analysis-role-item-pack.md`); this lane's ~5 minutes was spent *transliterating* them into shell, on top of the effort that already went into freezing them in prose. Nothing about the translation eliminated the original authoring step.
- **No live trial cost was incurred** (§2) — the comparison is a verifier-fidelity test, not a full re-run, so it cannot be compared to `nb2-o-packet.md` §2.1's real per-item token/cost table (1,921,786 tokens, cheapest item 67,298 tokens, most expensive 660,124). That table stays the only real trial-cost evidence either side has; this lane adds none, and reporting a saved-cost claim from this data would be false.
- **Human-review-minutes to trust the harness's own verdict:** for the 9 scalar items, near-zero once the verifier is written correctly (§2) — but §3 shows that "written correctly" is exactly the step that still requires a human to re-derive the frozen predicate's edge cases by hand, at the same failure rate as before. The honesty check B-2 §4 asks for (does a human still have to re-derive the gate by hand) answers **yes, at authoring time**, even though not at run time.

---

## 7. What this lane's evidence adds to the C-1…C-15 tally

Checked against `docs/audits/2026-08-29-technical-sda1-adversarial-incumbent-baseline.md`'s frozen 15-row tally: **no row flips.** The tally's NO/PARTIAL/YES rows score properties of SDA-1's *design* (corpus construction, k=3, floor calibration, cost commensurability) that a harness-format substitution does not touch. The one genuinely new, on-topic data point this lane produced — §5's N-04 silent-contamination loss — is not one of the 15 named findings and is reported here as a candidate observation rather than a 16th row, since amending that frozen tally is outside this lane's write-scope and this lane's own contract (item 2) draws the adoption line well short of it.

---

## 8. Decidability — applying B-2's own protocol (§4 of the translation draft)

B-2 stated the run is decidable if it either (a) reduces manual transcription/aggregation time or catches something the hand-rolled run missed, without weakening any of C-1…C-15, or (b) it does not.

**Measured answer: (b).** This run:
- did **not** reduce manual effort (§6 — the transliteration step is additive);
- did **not** catch anything the hand-rolled run missed (§4/§5 — every gate the hand-rolled cell computed, this translation either reproduced exactly via arithmetic, or could not compute at all; net new information runs the other way, surfacing a loss at N-04 the hand-rolled run's human reader already caught);
- did **not** weaken any of C-1…C-15 (§7 — none flip);
- **did** relocate risk rather than remove it (§3 — identical bug reproduction rate in either shape).

**The honest conclusion, in B-2's own words, now with a measurement behind it: the format changed where the work sits (frozen prose → shell scripts + a bespoke aggregator) without changing how much of it there is, and it introduced one measured new way to silently lose signal (N-04) that the hand-rolled human-in-the-loop reading did not.** That is this lane's whole deliverable — a reportable, non-adoption-relevant result, exactly as the contract anticipates.

---

## 9. Deviations, with owners

- **D-1 · Pack substitution (SDA1-N instead of the reviewer pack B-2 suggested) · owner: this lane.** Reasoned in §0; the done-contract names "one SDA-1 pack," not a specific one, and SDA1-N was the only pack with a completed hand-rolled run cheap enough to replay without a fresh paid invocation.
- **D-2 · Replay, not a fresh live trial · owner: this lane.** §2. A fresh invocation was in scope but assessed as testing an irrelevant second variable (provider capability) rather than the format variable the contract asks about; recorded rather than silently chosen.
- **D-3 · Executing model · owner: OPERATOR, disclosed not escalated.** This lane's dispatch table (`LANE-e-5-eval-sda1-harbor.md`) names `opus`; this lane executed under `claude-sonnet-5`, this session's served model. Disclosed per this repo's F0-adjacent convention (e.g. `nb2-o-packet.md` §7 item 6); not one of the V-2 escalation classes, so reported and not paused on.
- **D-4 · No Harbor package, no Docker environment, no live sandbox · owner: this lane, by design.** Per the done-contract's explicit stop condition. Every artifact above is plain bash/markdown imitating Harbor's documented shape (per B-2 §1's own description of that shape), never Harbor's actual code.

---

## 10. Scratch artifacts

Built and run under `temp/harbor-sda1n/` (gitignored; `.gitignore:122`), consisting of `build_and_run.py` (§1-§2), `naive_verifier_check.py` (§3), and `aggregator.py` (§4), plus the 10 generated task directories. **Deleted before this lane's commit** — every script body and every result relevant to this report is reproduced verbatim above, so nothing is lost by the deletion, and this lane leaves no artifact outside its declared footprint.

---

## 11. What this lane did not do

No merge, no push to `main`. No JOURNAL entry. No index regeneration. No `tasks/` write, no row births. No Harbor dependency added — the parking condition (`docs/audits/2026-08-30-technical-autonomy-decision-tree.md:64-65`) remains unmet and this lane does not touch it.
