---
intake-id: 31
status: DRAFT
origin: "Layer-1 architect (predecessor seat), 2026-08-09 — operator directive of 2026-08-09 plus the commissioned research report 'Enforcing a universal code-style doctrine across an LLM-written Python fleet'; authored off-repo and filed verbatim by the ARC-3 hygiene close-out"
note: "BODY FILED VERBATIM — zero edits, zero births. The body's own header bullet still reads `intake-id: 31 (PROPOSED — verify next-free before filing)`; that check is now DISCHARGED and the id is 31, held in reserve for this document since intake #32 recorded 30/31 as RESERVED rather than free. The bullet is left unedited because the archival value of a verbatim filing outranks tidying a resolved parenthetical."
---

# Universal code-style doctrine for an LLM-written Python fleet

- **intake-id:** 31 (PROPOSED — verify next-free before filing)
- **Class:** functional · **Date:** 2026-08-09 · **Status:** DRAFT — triage at the batch-4 planning GO with #28/#29/#30, ONE ratification batch
- **Author:** Layer-1 architect (predecessor seat), from the operator's directive of 2026-08-09 and a commissioned research report
- **Provenance:** research report "Enforcing a universal code-style doctrine across an LLM-written Python fleet" (2026-08-09, this window); operator's stated goal — one development style across all repos so work and code can be AGGREGATED and ANALYZED, and so agents stop drifting between OO and functional Python, inventing utilities, and producing over-long modules

## §A — Proposed ruling 1: the doctrine is ONE page, and it separates TASTE from MECHANISM

Written doctrine (taste — stated once, never gated): **"functional core, imperative shell"** as the fleet's paradigm sentence (Cosmic Python); **deep modules over thin layers** (Ousterhout, *A Philosophy of Software Design*) — explicitly NOT Clean Code's very-short-function rule, which is contested and conflicts with deep modules; Google Python Style Guide's falsifiable mechanics (comprehension/lambda limits, no globals) copied as the concrete style paragraph; *Effective Python* / *Fluent Python* named as the idiom references. **Recorded as a do-not-relitigate item:** "Functional Programming in Scala" is a MISMATCH as a fleet source of truth — its type-driven FP has no idiomatic Python equivalent and fights the style Python tooling enforces; no book text is copied into the repo (copyright).

Everything else in this intake is mechanism. **The paradigm question is not gateable — the enforceable proxy is structural: size caps, complexity ceilings, naming rules, import boundaries.**

## §B — Proposed ruling 2: the mechanism stack, in adoption order (each retires something)

1. **ruff rule-family expansion**, shipped from one canonical config: `C901` · `PLR0912/0913/0915/1702` (size/branch/nesting) · `N` (pep8-naming — kills naming drift) · `SIM/RET/ARG/TRY/ERA/FURB/B` · `I/TID/TC`. Per-file ignores for tests. Retires: ad-hoc per-repo lint opinions.
2. **One type checker fleet-wide** (mypy, or basedpyright for speed/strictness) with a **baseline** — the machine-checkable contract that most constrains agent output.
3. **Count ratchets** on the complexity rules and type debt — a direct extension of the existing `silent_rule_ratchet` shape (never worse than baseline; auto-lower on improvement; raising requires a reviewed, git-tracked baseline update). Retires: "we'll clean it up later".
4. **import-linter contracts** (actively maintained, v2.13 Jul 2026) — the one architecture gate; enforces the functional-core/imperative-shell split and forbidden import directions. NOTE: prefer it over `tach`, whose original upstream lapsed in 2025.
5. **Agent gates:** a PostToolUse hook running the quality gate on every agent edit and feeding failures back into context, and a PreToolUse guard that blocks writes to paths outside governance (the mechanized form of "zero invented paths").
6. **Fleet propagation:** a versioned config package published from the hub + `copier` for the files that cannot be packaged (pre-commit, CI, AGENTS.md). Retires: copy-paste drift. Pairs with the existing doc-carrier for verification.

## §C — Proposed ruling 3: LIBRARY-FIRST becomes mechanical

`deptry` (v0.25.1, Mar 2026; uv/PEP-621 native) catches unused, missing, transitive and misplaced dependencies. **`semgrep` custom rules are the mechanical form of the library-first rule**: "don't hand-roll X — use Y" written as a pattern that fails CI. This is the highest-leverage answer to the operator's observation that agents invent their own utilities instead of using existing libraries. Optional add-ons once the core holds: `jscpd` (duplication threshold), `complexipy` (cognitive complexity — catches deep nesting that ruff's branch counting misses), `wily` (trend).

## §D — Proposed ruling 4: NO fleet-wide refactor without a hotspot measurement

Do not refactor code merely because it predates these patterns. Procedure, in order: churn-vs-complexity hotspot analysis (change frequency is the better-supported signal; a small fraction of files typically carries most of the work) · complexity and file-length distributions · coverage on the hotspots · duplication rate · dependency cycles. **Refactor only where high churn ∩ high complexity, tests first where coverage is thin; everywhere else, ratchets + opportunistic improvement as agents touch the code.** Big-bang rewrites are the recorded failure mode; strangler-fig is reserved for a genuinely load-bearing, high-churn, high-complexity module.

## §E — Recorded caveats (so they are not relitigated)

Cyclomatic complexity is a contested defect predictor (Shepperd 1988; correlates strongly with LOC) and the Maintainability Index is flagged unreliable by its own tooling — both are **triage smells combined with churn, never proof**. Goodhart's law is the master risk of every gate here: an agent optimizing to a metric will split files to dodge length caps; keep the human on the baseline-raise escape hatch. Astral (ruff/uv) acquisition by OpenAI reported Feb 2026 — no change today, a governance signal to watch since the fleet pins both.

## §F — The hand-rolled pieces, declared

Two items have no established OSS equivalent and therefore need a measured-divergence justification per the library-first rule: the **prompt pre-dispatch checker** (intake #29's Rule-C shape — a gate that refuses a task contract lacking module target, size/complexity budget, and a governance-path reference) and the **checksum carrier verification**. Propagation itself must NOT be hand-rolled — `copier` covers it.

## Births

ZERO at filing. Candidate rows at batch-4 planning, against demonstrated close capacity: doctrine page + ruff expansion (S) · type-checker baseline (M) · complexity ratchet (S, extends the existing organ) · import-linter contracts (M) · agent hooks (S–M) · config package + copier propagation (M) · hotspot baseline measurement (S, read-only).

## Acceptance criterion

§A ratified as the written doctrine; §B ordered into batch-4/5 waves with each item's owning row; §C's deptry+semgrep pair scheduled; §D's hotspot measurement run BEFORE any refactor row is born; §E recorded in the do-not-relitigate register.
