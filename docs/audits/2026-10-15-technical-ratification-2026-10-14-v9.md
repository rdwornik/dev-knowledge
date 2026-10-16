# Archive copy of transport file RATIFICATION-2026-10-14.md

> Provenance: verbatim copy of `to-browser/RATIFICATION-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 3b641607ea67a6b2. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: RATIFICATION
date: 2026-10-15
supersedes: RATIFICATION-2026-10-14-v8-superseded.md
summary: v9. R102, R104–R110 and R112–R118 are carried (see v3–v8 superseded); R111 and list A are withdrawn by R116.
- R116 is closed: the operator accepted R113 (a) and the [#669] waiver on the seat's recommendation.
- R119: the day/night cadence. By day, lanes build with fast Tier-1 checks on their branch; by night, integration lands with the full suite on both OS, sharded, plus mutmut and the heavy gates. Blockers may land by day on the full CI. ADR-127 is unchanged.
- R120: tests are part of the graph. Every test is linked to the code it exercises and to the row or feature it proves; removing a feature removes or rewrites its tests in the same change; tests that prove nothing are found by measurement (coverage contexts, mutation kills) and are strengthened or removed.
The T2 mini-council (BATCH-DECIDE-TEST-STRATEGY-2026-10-15) turns R119 and R120 into an ADR; the operator ratifies it.
by: Tech-Architect-45 (2026-10-14-dev-knowledge-architect, SEQ 1; claude.ai Project chat, Claude Opus 5.5)
from: the operator, his words quoted, transcribed by Tech-Architect-45. The operator corrects or strikes any item.

# RATIFICATION — 2026-10-14/15 (v9)

**Carried unchanged:**
- R102, R104–R106 (v3);
- R107, R108 (v4);
- R109, R110 (v5);
- R113–R115 (v7);
- R112 rule + lists B and C (v6);
- R116–R118 (v8).

## R116 — closed

The operator, 2026-10-15: "pójdę za twoją rekomendacją".
- **R113 (a):** agy's own `~/.gemini` scratch writes are an accepted residual risk. The workspace is declared with `--add-dir`, and every read is verified (R59).
- **The `[#669]` → `[#664]` waiver** is confirmed (= R109 D-2).

## R119 — day/night cadence (operator, 2026-10-15; option A)

**The operator's words:**
> "Powinniśmy w ciągu dnia skupić się na działaniu, a w nocy na testowanie i integrowanie. W nocy testy mogą lecieć całą noc i mi to nie przeszkadza, ale jeżeli ja w ciągu dnia nic nie mogę zrobić, dlatego że cały czas integrujemy … to jest niemożliwe." — and: "pójdę za twoją rekomendacją".

**By day:**
- Lanes build.
- Each lane branch gets **Tier 1** in the cloud: lint and types plus **impacted tests only** (`impacted_tests.py` first; other tools per the council), in parallel, on Linux.
- The lane runs only its own RED → GREEN tests locally.

**By night:**
- ONE integration batch, with lands serial or grouped.
- The **full suite on Ubuntu + Windows** (ADR-127 unchanged), **sharded** across parallel jobs.
- **mutmut** on changed modules.
- The heavy gates (`ship_gate_diff`).
- A morning digest.

**Exceptions:**
- A blocker (for example a batch freeze) may land by day on the full CI.
- A dependent lane builds on its predecessor's branch rather than waiting for the night.

**Transition:** BUILD-1 (batch BU) finishes under its frozen orders, landing as handbacks arrive. R119 applies from BUILD-2.

**Measured goals:**
- a lane's Tier-1 verdict in ≤ 5 min;
- the night batch finishes, with its repair rounds, by morning;
- 0 regressions reach main that the full suite would catch.

## R120 — tests in the graph, and tests that prove something (operator, 2026-10-15)

**The operator's words:**
> "ty tworzysz tak testy, żeby same przeszły … nie testujesz outcome'ów, funkcjonalności … ile jest martwych, a pewnie nadal odpalamy testy z tym związane … kiedy usuwamy jakąś funkcjonalność … musimy razem dependency na testy usunąć. I dependency musi być w grafie."

**The evidence:** mutmut on 2026-10-15 executed 2077 mutants, killed 863 and let **1210 survive (≈ 41 % killed)**. Many tests do not detect wrong behaviour.

1. **Tests are nodes in the graph.**
   - Edges test → code come from **coverage contexts** (coverage.py `--cov-context=test`, library-first) and the import graph.
   - Edges test → row or feature come from the Done-when it proves.
   - The system map and R118's admission read these edges.
2. **Removal carries its tests.** Removing an organ, script or feature lists every test whose only covered code is that element (graph query). Those tests are removed or rewritten in the **same change**. Pre-commit refuses a removal that leaves orphan tests.
3. **A test must prove something.** The census flags each test:
   - **ORPHAN:** it covers only dead or removed code;
   - **DUPLICATE:** its coverage is a subset of another test's, with no extra assertions;
   - **ZERO-KILL:** it killed no mutant of the code it covers;
   - **NO-OUTCOME:** it asserts only on mocks or implementation details, with no outcome.

   Each is STRENGTHENED (an outcome assertion, RED first) or REMOVED. Removal follows R112's caller-check rule and the operator's GO on the list.
4. **New tests (R45, R104):** the RED test asserts the **outcome** the row's Done-when names. It is written by an agent other than the implementer, and its mutation score on the changed code is measured at night.

**Measured goals:**
- the mutation score on changed code ≥ 70 % per lane;
- across the repo, rising every week;
- orphan tests = 0 after the first census.

## Carriage

- **The council** (BATCH-DECIDE-TEST-STRATEGY-2026-10-15) produces the ADR for R119/R120, for the operator's ratification.
- **The build** is BUILD-2a slot 1 (tiered CI) and the first night run (coverage contexts + census).
- R101–R120 land with the next rulings lane.
