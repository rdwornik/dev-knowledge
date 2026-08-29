# THESIS-COMPARE — the operator's MSc thesis vs the live organs

**Lane:** THESIS-COMPARE, read-only side-session · **Date:** 2026-08-29
**Repo read (as reader, zero writes):** `C:\Users\1028120\Documents\Dev\.dev-knowledge` @ `96399b20`
**Input:** `C:\Users\1028120\Downloads\Praca_Dyplomowa_Magisterska\` — Robert Dwornik,
*"Architektura informatyczna modelu pracy dużej instalacji fotowoltaicznej"*, promotor dr inż. Piotr Pałka
**Rows born:** ZERO. **Files written to the repo:** ZERO. **Worktree provisioned:** NONE.

---

## 0. HONESTY — what I read, skimmed, and did not read

| File | Treatment |
|---|---|
| `tex/5-5-autorska-metoda.tex` (4.4 KB) | **read in full**, twice |
| `tex/8-wnioski-wynikające-z-pracy.tex` (14 KB) | **read in full**, incl. the commented-out earlier draft |
| `tex/Wywiad.tex` (3 KB) | **read in full** |
| `tex/2-cel-zakres-pracy.tex`, `tex/7-przedstawienie-wyników.tex` | **read in full** (small) |
| `main.tex` abstracts (PL + EN) | **read in full** |
| `tex/4-wprowadzenie-do-wzorców-metod.tex` (23 KB) | **read in full** |
| `tex/5-projektowanie-architektury-krok-po-kroku.tex` (38 KB) | **read in full** |
| `tex/6-tworzenie-architektury.tex` (185 KB) | **SKIMMED, as instructed.** I read its section skeleton (all 80 headings), and read four regions in full: the availability QA-scenario tables (`:892`–`:1020`), tactics (`:1020`–`:1049`), the questionnaire → optimal-pattern determination (`:1200`–`:1243`), and the counterfactual re-run (`:1243`–`:1265`). I did **not** read the other six quality attributes' equivalent blocks, the seven 4+1 functional walkthroughs (`:117`–`:881`), or any photovoltaic content. My claim that the per-attribute procedure is uniform rests on the **heading skeleton**, which repeats the same five-subsection shape per attribute — not on reading each instance. |
| `tex/B-Energy.tex` … `tex/F-Usability.tex` (5 appendices) | **not read as prose.** I checked their structure only, and found their decision tables are **commented out** (`% Uzasadnienie i założenia` at `C-Modify.tex:141`, `D-Safety.tex:90`, `E-Testability.tex:105`, `F-Usability.tex:102`, `B-Energy.tex:94`). I therefore make no claim about their content. |
| `tex/3-ogólny-wstęp-do-fotowoltaiki.tex`, `bibliografia.bib`, `img/`, `eiti/` | **not read** — domain / apparatus, out of scope per contract. |

**Encoding:** clean UTF-8 throughout; no macro or encoding region was unresolvable. Nothing in the TeX defeated me — where I say "absent" it is from a resolved read or an exhaustive grep, not from a failure to parse.

**Method note on the negatives.** Where I claim a concept is absent from the thesis, the evidence is a case-insensitive grep across `tex/` + `main.tex` for the Polish stem set, with every hit's context resolved by hand. Counts are reproducible.

---

## 1. RECONCILE — the thesis is NOT unread by this repo

The contract's reconnaissance is **accurate on every point I could test**, with two corrections and one refutation, all below. Prior consumption, resolved and confirmed:

**1. `docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md`** — intake #1, frontmatter `status: CONSUMED`, `consumed-by: "ADR-98, #268"`. Confirmed at the cited lines: `:20` ("Corporate mapping the operator wants preserved (BY delivery + **his thesis**)"), `:31` (the intake format "Framed on the operator's own thesis method — 4+1, where the +1 scenarios view drives the rest"), `:37` ("**Impact sketch (4+1 lite)** … Keeps the thesis framing honest without ceremony"). This intake consumed the thesis's **4+1 documentation-views** axis and is **terminal — it cannot absorb more.** Its derivative surface is live: `templates/intake-template.md` carries `## Scenarios (+1 view)` at `:27` and `## Impact sketch (4+1 lite)` at `:51` (contract locator `51-59` — exact).

**2. `docs/audits/2026-07-04-fable-architecture-review.md` §2** — *"The thesis lens — the operator's own method, applied backward"*. **All four contract locators resolve exactly:** `:44` (the §2 heading), `:46` (method mapping), `:48` (conclusion 1), `:50` (conclusion 2), `:52` (the confrontation ruling). This is an immutable audit and the only end-to-end read of the thesis. I treat `:48` and `:52` as binding and **concur with both** — see §2 rows 5 and 6, where I argue deltas rather than re-asserting gaps.

**3. Derivative surfaces** — cited, not re-derived: `docs/intake/README.md`, `templates/intake-template.md:51-59`, `templates/handoff/functional/FUNCTIONAL_BOOT.md.tmpl`, `JOURNAL.md` 2026-07-04.

### Verified negatives — independently re-run, and they hold

`magisterska` 0 files · `dyplomowa` 0 · `praca` 0 · `diploma` 0 · `dissertation` 0 · `Politechnik` 0 · `Pałka` 0 (case-insensitive, `--include='*.md'`, repo-wide). **No ADR cites the thesis.** ADR-98, the consumer of intake #1, carries no attribution.

### Correction 1 — `Stankiewicz` is NOT a zero

The contract lists the negatives as a block. `Stankiewicz` returns **one file**: `docs/audits/2026-07-04-fable-architecture-review.md` (at `:52`). This does not change any conclusion — it is the Fable audit the contract itself cites — but the name is *not* absent from the repo, and a future reconnaissance grepping for it will get a hit. Recording it so the next lane is not surprised.

### Correction 2 — the "confrontation" sentence is in ch.8, not `Wywiad.tex`

The contract sources the *"confrontation with a differently-thinking third party"* claim to `tex/Wywiad.tex`. It is not there. `Wywiad.tex` is the **transcript** — six question/answer exchanges between "Architekt Systemu (RD)" and "Specjalista ds. Energetyki (DS)", all of them domain questions about PV sizing, meteorological data and economic output. The **claim** lives in `tex/8-wnioski-wynikające-z-pracy.tex`:

> *"Rozmowa z magistrem energetyki, panem Danielem Stankiewiczem, była punktem zwrotnym w pisaniu tej pracy dyplomowej. Możliwość skonfrontowania swoich pomysłów i sposobu myślenia z osobą, która ma inne podejście do problemu, pomaga określić właściwy kierunek."*
> — *"The conversation with the energy-engineering graduate, Mr Daniel Stankiewicz, was the turning point in writing this thesis. The ability to confront one's own ideas and way of thinking with a person who has a different approach to the problem helps determine the right direction."*

Minor, but the contract asked to be corrected with the locator, and a lane that opens `Wywiad.tex` looking for the claim will not find it.

---

## 2. THE COMPARISON

### 2a. FIRST — the thesis's own schema, derived from the text

The contract said: *"Derive the principles from the thesis text, do not take my four labels as the schema."* Doing so changes the answer materially, so it goes first.

`5-5-autorska-metoda.tex` states the author's own method as **five steps**, and it is not the dispatch's four principles:

1. **Zdefiniowanie ogólnych scenariuszy dla określonych wymagań niefunkcjonalnych** — *define general scenarios for specified non-functional requirements.*
2. **Opracowanie zestawu taktyki dla każdego atrybutu jakości** — *develop a set of tactics per quality attribute.* "Każda taktyka powinna być oceniona pod względem korzyści i kompromisów" — *each tactic evaluated for benefits and tradeoffs.*
3. **Przeprowadzenie ankiet w celu zebrania informacji** — *conduct questionnaires to gather information* from developers and stakeholders. Load-bearing constraint: **"Pytania powinny być zamknięte tak aby sprawnie przeprowadzić proces ewaluacji odpowiedzi"** — *questions should be CLOSED so the evaluation of answers can be carried out efficiently.*
4. **Przeanalizowanie korzyści i kompromisów różnych wzorców projektowych** — *analyze benefits and tradeoffs of the candidate patterns*, informed by step 3.
5. **Podjęcie decyzji architektonicznej** — *make the architectural decision*, which "powinna uwzględniać wpływ na system jako całość" — *must account for the impact on the system as a whole.*

The same file then does something the dispatch did not anticipate: **it critiques its own method**, under `Zalety` (advantages: structured, systematic, stakeholder-involving, tradeoff-analytic) and `Wady` (disadvantages: **czasochłonność** / time cost; **wymagana wiedza specjalistyczna** / requires specialist expertise; **ograniczenie do zebranych informacji** / limited to the information the respondents actually supplied).

### 2b. The dispatch's four labels, tested against that text

| # | Dispatch label | In the thesis? | Evidence |
|---|---|---|---|
| 1 | Architecture **decision trees** | **NO** | `drzewo` 0 hits · `drzewa` 0 hits across `tex/` + `main.tex`. The single `decyzyjn` hit is `main.tex:52`, *"wzorce i metody decyzyjne"* (decision patterns and methods) — the abstract's framing, not a tree. |
| 2 | **Mandatory self-questioning** | **YES** | Present and load-bearing — see row 5. |
| 3 | **Cognitive-bias mitigations** | **NO — zero trace** | `błąd poznawczy` 0 · `uprzedzeni` 0 · `stronnicz` 0 · `heurystyk` 0. `poznawcz` returns **1** hit — `8-wnioski:38`, inside a **commented-out** paragraph, meaning *"sprawny proces poznawczy całego systemu"* (efficient **cognitive process** of comprehending the system) — comprehension, not bias. `obciążeni*` returns 48 hits and every one is **system load** (`obciążenia` ×31, `obciążenie` ×13 — "równoważenie obciążenia" = load balancing). No named bias, no countermeasure, anywhere. |
| 4 | **Adversarial multi-agent debate as the decision mechanism** | **NO, in that form** | `debat` 0 · `adwersar` 0 · `krytyk` 0 · `oponent` 0 · `agent` 0 · `konfrontac` 0 (the confrontation is expressed as *"skonfrontowania"*, a verb form, once). What exists is **consultative, not adversarial, and it feeds requirements rather than deciding**: one interview with one expert, plus stakeholder questionnaires. See row 6. |

**Finding about the brief, stated plainly because it is worth more than a padded row:** of the four labels, **one is in the thesis (2)**, **one is in it in a substantially weaker form than the label claims (4)**, and **two are not in it at all (1, 3)**. Principle (3) in particular is not a thesis principle — it is an *ai-council* objective that the dispatch attributed to the thesis. The repo has far more cognitive-bias machinery than the thesis does (row 7).

### 2c. A fifth load-bearing principle, not in the dispatch

**Simulated stakeholder responses, and the counterfactual re-run.** This is the thesis's most distinctive and most transferable move, and no dispatch label names it.

`2-cel-zakres-pracy.tex` and `5-5-autorska-metoda.tex` both state it: *"**symulując odpowiedzi na kwestionariuszach**, można podjąć rekomendowaną decyzję architektoniczną"* — *"by **simulating the answers to the questionnaires**, one can arrive at the recommended architectural decision."* The author does not only gather real answers; he **simulates an answer set** and derives the decision from it.

`6-tworzenie-architektury.tex` then demonstrates the consequence. At `:1206` (`Określanie optymalnego wzorca dostępności na podstawie wyników kwestionariuszy taktyki`) a nine-question closed TAK/NIE questionnaire yields the verdict *"wzorzec architektoniczny 'Load Balancer' jest najlepszym rozwiązaniem"*. Then at `:1243`, under the heading **`Przykład dla innego zestawu odpowiedź`** (*"Example for a different set of answers"*), the same questions are re-answered all-NIE and the recommendation **flips**: *"inny wzorzec architektoniczny, taki jak redundantny serwer lub chmura, byłby lepszym dopasowaniem."*

That is a **sensitivity analysis on a decision** — the method does not merely record what was decided, it exhibits *which input change reverses it*. It is the closest thing in the thesis to a robustness or bias check, and it is arrived at structurally rather than psychologically. Its absence from the repo is the strongest gap in §3.

### 2d. The comparison table — verdicts

Verdict enum: **implemented** · **partial** · **absent**. Every verdict carries a locator.

---

**ROW 1 — Scenario-first NFR specification, with the six-part scenario anatomy**
*Thesis:* step 1. `5-projektowanie-architektury-krok-po-kroku.tex:200` — *"Scenariusze atrybutów jakości składają się z sześciu części"*: **bodziec** (stimulus), **źródło bodźca** (stimulus source), **odpowiedź** (response), **miara odpowiedzi** (response measure), plus the two the thesis flags as *"ważne, choć często pomijane"* (important though often omitted) — **środowisko** (environment) and **artefakt** (artifact).

**VERDICT: partial.**
*Locator (what exists):* `templates/intake-template.md:27` — `## Scenarios (+1 view)`, the intake format's load-bearing section, and `:51` `## Impact sketch (4+1 lite)`. The full six-part anatomy fired **once**, as a review lens, at `docs/audits/2026-07-04-fable-architecture-review.md:46` (*"§3 states scenarios (stimulus → response → response-measure, per the thesis's 6-part scenario anatomy)"*).
*Gap:* the intake template asks for a scenario as prose ("as the operator I … and then …"). It does **not** ask for stimulus / source / environment / artifact / response / **response-measure**. The response-measure is the half that makes a scenario testable — and it is the half the repo's own ADR-81 ex-ante acceptance contract independently reinvented for build tasks. The anatomy was applied *to* the repo once and never installed *in* it.

---

**ROW 2 — Quality attribute → tactic → tradeoff evaluation**
*Thesis:* steps 2 and 4, and the whole spine of ch.6. `5-projektowanie…:~270` — *"Taktyki to konkretne decyzje projektowe … Ocena kompromisów między różnymi taktykami i wybór taktyk, które najlepiej spełniają wymagania systemu."*

**VERDICT: absent.**
*Locator:* `grep -ril "quality attribute" protocols/ templates/ docs/decisions/` returns **zero files**. There is no quality-attribute vocabulary, no tactic register, and no obligation for a decision to name the attribute it serves.
*Honest qualifier, because this is the row most likely to be over-read:* the repo governs a methodology corpus, not a runtime system with latency and availability budgets, so the thesis's *specific* attribute set (dostępność, wydajność, bezpieczeństwo…) does not transfer. But the **Fable audit proved the frame does transfer** — it ran exactly this machinery over this repo in the evaluation direction (`:44`–`:52`) and produced the two conclusions now binding this lane. The gap is not "no QA vocabulary"; it is that the audit was a **one-off lens, never a standing obligation**. See §3 gap 4, where I rank it accordingly rather than inflating it.

---

**ROW 3 — Closed-question questionnaires as the decision instrument**
*Thesis:* step 3, with the closedness constraint quoted in §2a, and the worked instrument at `6-tworzenie-architektury.tex:1206` (nine closed TAK/NIE rows).

**VERDICT: implemented — and this is the single strongest structural match in the whole comparison.**
*Locator:* `protocols/HANDOFF_PROCESS.md:204-216`, the four-part teeth-bearing probe contract: **(1) live-only answer** — "the answer exists only in the live primary file/state at answer-time"; **(2) generator-excluded** — "the handoff ships the **question + source-locator + the exact verification command**, and **never the answer**"; **(3) CC-checkable**; **(4) bounded-deterministic** — "A probe whose honest answer requires unbounded judgment over an open set is an **arc, not a probe**, and is rejected."

That fourth clause *is* the thesis's *"pytania powinny być zamknięte"* — closedness, ratified independently, for the same stated reason (efficient, mechanical evaluation of the answer). The Fable audit already anticipated this at `:46`: *"The thesis's questionnaire instrument (its human-consultation core) maps onto what this system built instead: council debates, Fable consults, and the handoff probe manifest — machine-era questionnaires."* I concur, and sharpen it: of those three, the **probe manifest** is the exact analogue — closed, gradeable, answer-excluded — while council debates are the analogue of the *stakeholder consultation*, not of the questionnaire.

---

**ROW 4 — "The architect must always justify architectural decisions" / considered alternatives**
*Thesis:* `4-wprowadzenie-do-wzorców-metod.tex:15` — *"**Architekt musi zawsze uzasadniać swoje decyzje architektoniczne** a zwłaszcza wtedy, gdy chodzi o dobór wzorca architektonicznego."* — *"The architect must ALWAYS justify their architectural decisions, especially when it comes to the choice of architectural pattern."* The thesis practises it: ch.4 compares ADD vs ATAM vs 4+1 with explicit Zalety/Wady for each, then justifies the 4+1 choice in its own subsection (`:195`, labelled *"Dlaczego wybrałem model 4+1 widoków?"* — *"Why I chose the 4+1 view model"*).

**VERDICT: partial. Measured, not impressioned.**
*Locator + measurement:* **57 of 88** ADRs (`docs/decisions/ADR-*.md`) carry an alternatives-family heading — **65%**. Heading shapes, counted: `## Alternatives considered` ×43, `## Rejected alternatives` ×6, `## Alternatives rejected` ×3, plus 5 one-off variants (`## 10. Alternatives considered`, `## §9 Alternatives considered`, `## §4 — Alternatives considered and rejected, with their recorded reasons`, `## Rejected alternative — canonical-organ-only`, `## Alternatives considered (the #86.2 operator fork)`).
*Gap — and it answers the contract's question directly:* **it is a habit, not a template obligation.** `templates/ADR-template.md` ends with:

> `## Alternatives considered`
> `<Optional. What else was evaluated and why it was not chosen?>`

The word is **`Optional`**, in the template, in the last line of the file. The thesis says *zawsze* (always). 65% is what "optional" buys. What the template *does* mandate is adjacent and arguably stronger: `**Decision tier:**` (*"names how it was decided, not the topic"*), `**Source:**` (provenance), and a mandatory `## Consequences` section — the repo enforces *how* a decision was routed and *what it costs* more strictly than *what else was on the table*.

---

**ROW 5 — Continuous re-evaluation: *"jaki jest nasz cel, co chcemy osiągnąć?"***
*Thesis:* `8-wnioski-wynikające-z-pracy.tex` — *"można odpowiedzieć na najważniejsze pytanie w procesie twórczym 'jaki jest nasz cel, co chcemy osiągnąć?'. Ciągła ocena z wykorzystaniem tego pytania pozwala zaoszczędzić znaczną ilość czasu i energii"* — *"one can answer the most important question in the creative process: 'what is our goal, what do we want to achieve?'. Continuous evaluation using this question saves a significant amount of time and energy."*

**VERDICT: implemented — DISCHARGED, and I concur with the standing ruling.**
*Locator:* `docs/audits/2026-07-04-fable-architecture-review.md:48` verdicts this **"structurally embodied"** via Done-when on every BACKLOG task, ADR-81's ex-ante frozen acceptance contract, and PLAYBOOK Ch12.1 closure-on-hard-metric — *"the thesis's question turned into gates — better operationalized than the thesis itself managed."* I re-read the thesis passage and the ruling stands; the audit is not over-claiming.
*Delta I can add without re-asserting the gap:* the audit names the drift mode ("when the gate becomes the goal") and prescribes "a standing genuineness audit per proxy". The thesis supplies something the audit did not draw on — its own `Wady` list, whose third entry is *"ograniczenie do zebranych informacji … Jeżeli brakuje ważnych informacji, podejście może nie zapewnić najdokładniejszej rekomendacji"* (**limited to the information gathered**; if important information is missing, the method may not yield the most accurate recommendation). That is the thesis pre-registering its own failure mode. The repo's nearest equivalent is the honest-limit convention (`CLAUDE.md` §9 hook rows: *"Honest limit, the module's own…"*), which is live and well-observed. Not a gap — a concurrence with a note that the two conventions are the same instinct.

---

**ROW 6 — Confrontation with a differently-thinking third party**
*Thesis:* the ch.8 passage quoted in Correction 2. Note also `2-cel-zakres-pracy.tex`: the method itself is *"inspirowana pracą mgr inż. Daniela Stankiewicza"* — the third party is in the method's genesis, not merely its validation.

**VERDICT: implemented — DISCHARGED, and I concur.**
*Locator:* `docs/audits/2026-07-04-fable-architecture-review.md:52` — *"institutionalized here as multi-provider council debate, cross-vendor Codex review, and Mythos-tier consults — heterogeneous-second-reader as standing doctrine, not a lucky interview."* Live organs confirm it: `protocols/PLAYBOOK.md:5143` (exact model strings, the three Codex lanes), `:5144` (terra pinned as doctrinal default on **both** wrapper paths — the pin exists because an unpinned run asked for as terra silently executed as sol, drift closed by `[#469]`), `:5146` (*"Every plan names its Codex lane"* — an addressable planned decision, not an ad-hoc pick), `:4058` (which lane reviews each leg, named per task), and `:5163` (*"independent reviewer — no authorship bias"* — the rationale stated outright).
*Delta, offered as a real difference and not as a gap to fund:* the thesis's turning point came from a **domain expert outside software** — an energy engineer, whose questions in `Wywiad.tex` are about solar altitude at winter solstice, meteorological data and module efficiency. Not one of them is a software question. Every institutionalized second reader in this repo is **software-shaped**: other LLMs, reading the same corpus, in the same vocabulary, about the same artifacts. The repo has institutionalized *heterogeneous provider*; the thesis's instance was *heterogeneous domain*. Whether that difference matters for a governance repo is a genuine open question, not a defect — I flag it in §3 gap 4 and recommend it be settled by a question rather than a build.

---

**ROW 7 — Cognitive-bias mitigation**
*Thesis:* **absent — zero trace** (evidence in §2b row 3).

**VERDICT (repo side): implemented — and this REFUTES the contract's stated thin spot.**

The contract states: *"principle (3), cognitive-bias mitigation, appears to have **no object in this repo at all** — its only trace is an ai-council objective relayed through two handoff bundles."* I asked to confirm or refute from my own read. **Refuted**, with locators:

`protocols/AI_COUNCIL_PROCESS.md:99-110` — a live protocol section, `status: active`, `last_reviewed: 2026-07-29` — carries **five named biases with named countermeasures**: Leading headline · Asker-leakage · False dichotomy · Choice-set bias · Loaded terminology. It carries a **bias self-check** at `:109-110`: *"if a fast unanimous agreement would not surprise you, the question is leading."* It carries the mitigation **wired into the artifact** at `:149` — `D: a different approach (name it)  # explicit escape — choice-set bias mitigation`. And it carries a **failure-mode remediation row** at `:399`: synthesis biased toward the asker's pre-stated preference → *"Discard the verdict; rewrite the brief … rerun. **Blind voting cannot fix this.**"*

The canonical roster is cross-repo, in the sibling `ai-council`, at `protocols/COUNCIL_QUESTION_GUIDE.md:242-289` — **seven** named biases, each with a `*Fix:*`: Leading/framing · **Anchoring** · Confirmation/asker-leakage · False dichotomy · Loaded terminology · Choice-set bias · **Availability**. Its framing statement at `:231-241` is unambiguous:

> *"A biased question is the one failure mode the Council cannot recover from. Blind voting (ADR-03), the multi-model panel (ADR-02), and adversarial personas are all downstream defenses … Question framing is the only bias-control point with no safety net."*
> *"**The Council's success metric is the elimination of cognitive bias.**"*

That last line is the ai-council objective the handoff bundles were relaying (`docs/handoffs/2026-07-23-ai-council-architect/SUPPLEMENT.md:62`, *"T1 minimize cognitive bias / raise debate value"*) — it is not an aspiration floating in a bundle; it is the stated success metric of a documented, versioned organ. A third countermeasure of the same family lives in this repo at `protocols/STANDING_RULINGS.md:405` — *"a NO carries full credit … the clause that keeps the measured-divergence bar from decaying into a **bias toward adoption**."*

*Why the contract's recon missed it:* the surfaces say "Neutralizing bias" and name biases individually; they never use the string "cognitive bias" except in the ai-council guide's metric line. A grep for the compound term returns only the two handoff bundles — exactly what the contract reported. The recon was honest and its method was the limitation.

*Net:* the thesis is silent on bias; the repo has a seven-item roster with countermeasures, an escape option wired into the ballot, a pre-flight self-check and a remediation row. **The comparison runs backwards on this principle.** The correct disposition is DISCHARGED, not CANDIDATE — see §3.

**One real defect found in passing (locator resolution, per the contract's `/preflight` rule):** `protocols/AI_COUNCIL_PROCESS.md:99` and `:399` both cite the guide as **`council-question-guide.md`** under `ai-council/docs/`. The `> Authoritative sources.` block at the top of the file (`:20`) cites the same path. That file **does not exist**. `git ls-files` in `ai-council` resolves it to **`protocols/COUNCIL_QUESTION_GUIDE.md`**. A live, freshness-stamped protocol points three times at a moved file — the bias roster is real, but the repo's pointer to it is broken. Reported, not fixed: this lane writes nothing.

---

**ROW 8 — Architecture decision trees**
*Thesis:* **absent** (`drzewo`/`drzewa` = 0). What the thesis actually builds is a **decision table**: a closed answer-vector maps to a recommended pattern (`6-tworzenie-architektury.tex:1206`), with the mapping's sensitivity demonstrated at `:1243`. A table, not a tree — and never named as either.

**VERDICT (repo side): implemented, and the attribution question is moot.**
*Locator:* two genuine decision trees exist and both are live — `protocols/PLAYBOOK.md:4375` (`#### Decision tree`, amend-in-place vs reopen, with explicit branch conditions) and `docs/intake/2026-07-11-tech-ownership-manifest.md:58` (`## The nightly decision tree (per repo R, per root entry E)`, pseudo-code branching, `status: ACCEPTED`). The contract flagged both as *"candidates but none thesis-attributed"* and asked me to confirm or refute. **Confirmed as candidates, and their non-attribution is correct** — they cannot be attributed to a thesis that contains no decision tree. There is nothing to fix here.

---

**ROW 9 — Simulated responses + counterfactual re-run** (the fifth principle, §2c)
*Thesis:* `2-cel-zakres-pracy.tex` / `5-5-autorska-metoda.tex` (*"symulując odpowiedzi"*) + `6-tworzenie-architektury.tex:1243` (the flip).

**VERDICT: absent.**
*Locator:* no ADR, template, or protocol asks what would reverse a decision. `templates/ADR-template.md` has Context / Decision / Consequences / Alternatives-considered(Optional) — four sections, none of which is "what input change flips this". `protocols/STANDING_RULINGS.md:26` (`## The decision budget`) and `protocols/PLAYBOOK.md:1880` (the V-2 budget: escalate only on curated-baseline touches, genuine rule-vs-ruling conflicts, and fork classes with no standing ruling) govern **who decides and when to escalate** — not **when to revisit**. The nearest live intent is `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md` §A.2 (`status: SEED`): *"relies on revertability instead of escalation … decide, record, and **mark revertable**."* The repo says *mark revertable*; nothing says **what shape that mark takes**. The thesis supplies exactly that shape. Ranked #1 in §3.

---

**ROW 10 — The method critiques itself (`Wady`)**
*Thesis:* `5-5-autorska-metoda.tex` — the author lists his own method's three disadvantages immediately after its four advantages.

**VERDICT: implemented.**
*Locator:* `CLAUDE.md` §9's hook roster states an **"Honest limit"** for organ after organ in the module's own words — `block-commit-on-main` (*"a genuine git failure silently ALLOWS the commit — a stated hole … internally inconsistent with sibling `merge_in_progress()`"*), `provider-registry-agreement` (*"it asserts AGREEMENT, not correctness"*), `lane-contract-check` (*"it checks SHAPE, never whether a contract's footprint claims are true"*), `check-seal-identity`, `validate-hermetization` (*"Rule C polices the HOME of an added file, and the two open homes … admit arbitrary depth by design"*). `templates/ADR-template.md` makes `## Consequences` — *"What becomes easier or **harder**"* — a standing section, not an optional one. The instinct is the same as the thesis's `Wady`, and here it is the stricter of the two: the thesis critiques its method once; the repo requires every organ to state its own limit. No gap.

---

## 3. THE GAP LIST — ranked, decision-ready, ZERO ROWS BORN

Four gaps. I could have written twelve; the other eight would have been row 2 restated at different altitudes, or DISCHARGED items dressed as work. Each entry carries **(a)** the thesis principle in Polish + gloss, **(b)** the live verdict + locator, **(c)** the delta in one sentence, **(d)** the ADR-111 funnel home, **(e)** a size band, **(f)** the cheapest thing that settles it.

### GAP 1 — A decision records what it *is*, never what would *flip* it — RANK 1

**(a)** *"Analizując korzyści i kompromisy różnych wzorców projektowych dla danego atrybutu i **symulując odpowiedzi na kwestionariuszach**, można podjąć rekomendowaną decyzję architektoniczną."* (`5-5-autorska-metoda.tex`) — *"By analyzing the benefits and tradeoffs of the different design patterns for a given attribute and **simulating the answers to the questionnaires**, one can arrive at the recommended architectural decision."* Demonstrated at `6-tworzenie-architektury.tex:1243`, `Przykład dla innego zestawu odpowiedź` — the same nine questions re-answered, the recommendation flips from Load Balancer to redundant-server/cloud.

**(b)** **absent** — `templates/ADR-template.md` (Context / Decision / Consequences / Alternatives-considered`<Optional.>`); `protocols/PLAYBOOK.md:1880` and `protocols/STANDING_RULINGS.md:26` govern escalation, not revisitation.

**(c) Delta:** the thesis makes a decision's **sensitivity** part of the decision record — the answer-set that reverses it is written down — whereas every ADR here records the decision and its rejected alternatives but never the condition under which the choice stops being right.

**(d) Funnel home:** **CANDIDATE.** It **amends an existing object** — `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md` §A.2 (`status: SEED`, `intake-id: 22`), which already ratified *"decide, record, and mark revertable"* as doctrine but never specified the shape of the mark. This gap **is** that shape, so it belongs as an amendment to intake #22 rather than a new intake — and #22 is SEED, so it can still absorb it. (Not intake #1: `status: CONSUMED`, terminal.) A secondary, cheaper landing exists if the operator prefers the smallest possible act: one line in `templates/ADR-template.md`.

**(e) Size: S.** One template line plus a doctrine sentence. It creates no new organ, no gate, no script.

**(f) Cheapest settle if unsure:** take the three most consequential ADRs of the last month and try to write the flip condition retrospectively. If it is writable in one line each, the practice is cheap and real; if it is not writable, the gap is theoretical and should be REJECTED on the spot. That is one sitting, no code, and it produces evidence either way — the `measured-divergence` bar at `protocols/STANDING_RULINGS.md:405`, applied to this proposal.

---

### GAP 2 — The scenario has no response-measure — RANK 2

**(a)** *"Miara Odpowiedzi — Po wystąpieniu reakcji powinna być ona w jakiś sposób mierzalna, aby można było przetestować scenariusz — czyli **ustalić, czy architektowi udało się go zrealizować**."* (`5-projektowanie-architektury-krok-po-kroku.tex:~204`) — *"Response measure — once the response occurs it should be measurable in some way, so the scenario can be tested — that is, to **establish whether the architect actually achieved it**."*

**(b)** **partial** — `templates/intake-template.md:27` (`## Scenarios (+1 view)`) asks for a narrative scenario; the six-part anatomy fired once as a review lens at `docs/audits/2026-07-04-fable-architecture-review.md:46` and was never installed. Note `:41` of the same template **does** carry `## Acceptance criteria (ex-ante)`, which is the response-measure under a different name — so the ingredient exists in the file, one section away, unlinked to the scenario it should measure.

**(c) Delta:** the thesis binds each scenario to its own measure so the scenario is individually testable, whereas the intake template collects scenarios in one section and acceptance criteria in another, leaving no per-scenario measure and no way to tell which scenario a given criterion discharges.

**(d) Funnel home:** **CANDIDATE**, **amending an existing object** — `templates/intake-template.md` (`## Scenarios (+1 view)`, `:27`). This is the same surface intake #1 authored, but intake #1 is `status: CONSUMED` and terminal, so the amendment attaches to the template directly, with the ADR-98 traceability edge pointing back at it.

**(e) Size: S.**

**(f) Cheapest settle:** open the two SEED intakes (#7, #22) and check whether their scenarios already imply a measure. If they do, this is documentation of existing practice (do it); if their scenarios are unmeasurable as written, that is the evidence the section needs the prompt.

---

### GAP 3 — *"Zawsze"* vs `<Optional.>` — RANK 3

**(a)** *"**Architekt musi zawsze uzasadniać swoje decyzje architektoniczne** a zwłaszcza wtedy, gdy chodzi o dobór wzorca architektonicznego."* (`4-wprowadzenie-do-wzorców-metod.tex:15`) — *"The architect must **always** justify their architectural decisions, especially where the choice of an architectural pattern is concerned."*

**(b)** **partial** — measured: **57/88 ADRs (65%)** carry an alternatives-family heading; `templates/ADR-template.md`'s final line reads `<Optional. What else was evaluated and why it was not chosen?>`.

**(c) Delta:** the thesis makes justification unconditional; the template makes it optional, and 65% is the observed price of that word.

**(d) Funnel home:** **CANDIDATE**, **amending an existing object** — `templates/ADR-template.md`. I flag one honest complication for the operator's decision rather than hiding it: promoting a section from optional to mandatory in a template is the kind of change that acquires a gate, and a gate on "did you write an Alternatives section" measures presence, not thought — precisely the drift mode the Fable audit names at `:48` (*"every deterministic proxy for a semantic goal will eventually be satisfied without the goal"*). Recommend the word change **without** a gate.

**(e) Size: S.**

**(f) Cheapest settle:** read the 31 ADRs that lack the section. If most are mechanical (a status flip, a naming rule) the 65% is correct behaviour and this closes as **REJECTED — working as intended**. If several are consequential forks with no alternatives recorded, the word changes. One sitting.

---

### GAP 4 — Every second reader is software-shaped — RANK 4

**(a)** *"Możliwość skonfrontowania swoich pomysłów i sposobu myślenia z osobą, która ma **inne podejście do problemu**, pomaga określić właściwy kierunek."* (`8-wnioski-wynikające-z-pracy.tex`) — *"The ability to confront one's own ideas and way of thinking with a person who has **a different approach to the problem** helps determine the right direction."*

**(b)** **implemented as heterogeneous-provider, DISCHARGED at `docs/audits/2026-07-04-fable-architecture-review.md:52`.** Live: `protocols/PLAYBOOK.md:5143/:5144/:5146`, `:4058`, `:5163`.

**(c) Delta:** the thesis's turning point came from a **different domain** (an energy engineer who asked about winter-solstice solar altitude, `Wywiad.tex`), while every institutionalized reader here is a language model reading the same corpus in the same vocabulary — heterogeneous *provider*, homogeneous *frame*.

**(d) Funnel home:** **CANDIDATE, but the honest recommendation is to route it as a question, not work.** It plausibly belongs to intake #7 (`docs/intake/2026-07-08-func-ai-council-interface.md`, `intake-id: 7`, `status: SEED`) if it goes anywhere. I rank it last and would not fund it ahead of gaps 1–3: the audit's DISCHARGED ruling covers the principle as the operator institutionalized it, and this delta questions whether the institutionalization is *complete*, which is a different and much larger claim than I can support from a thesis reading alone.

**(e) Size: L** — and that size is itself an argument for settling it cheaply first.

**(f) Cheapest settle:** one Council `judge` question — *"does a governance repo get anything from a non-software second reader that a cross-provider software reader cannot supply?"* — run through the very bias-neutralization checklist at `ai-council/protocols/COUNCIL_QUESTION_GUIDE.md:242`. If the answer is no, this closes REJECTED with a citation and never returns.

---

### DISCHARGED — recorded as successes of this lane, not as absent work

| Item | Disposition | Locator |
|---|---|---|
| Continuous *"jaki jest nasz cel"* re-evaluation | **DISCHARGED** — ruled "structurally embodied"; I concur on re-read | `docs/audits/2026-07-04-fable-architecture-review.md:48` |
| Confrontation with a differently-thinking third party (as institutionalized) | **DISCHARGED** — ruled "institutionalized here"; I concur | `…fable-architecture-review.md:52` |
| Questionnaire instrument → machine-era equivalents | **DISCHARGED** — ruled at `:46`; I concur and sharpen (the probe manifest is the exact analogue) | `…:46` + `protocols/HANDOFF_PROCESS.md:204-216` |
| Machine-legible docs make change manageable | **DISCHARGED (partial, already ruled)** — *"delivered on detection, half-delivered on removal"*; the PRUNE half is tracked work, not a thesis finding | `…:50` |
| 4+1 documentation views | **DISCHARGED** — consumed by intake #1 → ADR-98, #268; terminal | `docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md:31,:37` |
| **Cognitive-bias mitigation** | **DISCHARGED — and the brief had it backwards.** Absent from the thesis (zero trace); present in the repo as a 7-item roster with countermeasures | `protocols/AI_COUNCIL_PROCESS.md:99-110,:149,:399` · `ai-council/protocols/COUNCIL_QUESTION_GUIDE.md:242-289` · `protocols/STANDING_RULINGS.md:405` |
| **Architecture decision trees** | **REJECTED — not a thesis principle.** `drzewo`/`drzewa` = 0 hits; the two live trees are correctly unattributed | `protocols/PLAYBOOK.md:4375` · `docs/intake/2026-07-11-tech-ownership-manifest.md:58` |

### One defect, reported not fixed (this lane writes nothing)

`protocols/AI_COUNCIL_PROCESS.md` cites `ai-council/docs/council-question-guide.md` at `:20`, `:99` and `:399`. That path does not exist; the file is at `ai-council/protocols/COUNCIL_QUESTION_GUIDE.md`. A live protocol (`status: active`, `last_reviewed: 2026-07-29`) points three times at a moved authoritative source. Funnel home if the operator wants it: **CANDIDATE**, trivially **S**, or **OWNED** if an existing cross-repo-locator row already covers it — I did not search the funnel for one, and say so rather than guessing.

---

## 4. NORTH STAR NOTE — what should bind the AUTONOMY arc

The operator has ruled this thesis the north-star input for the AUTONOMY arc (library-first, TDD, measured spectrum). Two cloud lanes (AUT-R1 industry survey, AUT-R2 decision-quality frameworks) are running beside this one; I have not seen their output and this section is deliberately narrow to what the thesis text actually supports.

**The thesis is a poor source for three things the arc will be tempted to take from it, and I would rather say so than pad.** It is pre-LLM-agent (the Fable audit already says this at `:52`); it contains no multi-agent content, no bias content, and no decision-tree content; and its human-consultation core (steps 3 and 5) assumes a stakeholder who can be interviewed. An implementer told "the thesis is the north star" will otherwise go looking for an agent architecture in it and find none.

**What it genuinely supplies, in priority order:**

**1. The decision function must be explicit, closed, and re-runnable.** This is the thesis's real contribution and it survives translation to autonomy intact. The method's shape is: closed questions → answer vector → recommended pattern, with the mapping stated well enough that *a different answer vector visibly produces a different recommendation* (`6-tworzenie-architektury.tex:1206` vs `:1243`). An autonomous decision-maker that cannot exhibit its own flip condition cannot be audited, and cannot know when to revisit. **Bind this to the arc's contract.** It is also gap 1, which is why gap 1 is ranked first.

**2. Closed questions, because the answers get evaluated mechanically.** *"Pytania powinny być zamknięte tak aby sprawnie przeprowadzić proces ewaluacji odpowiedzi."* The repo has already ratified this independently and more rigorously — `protocols/HANDOFF_PROCESS.md:204-216`, where **bounded-deterministic** is a teeth-bearing criterion and *"a probe whose honest answer requires unbounded judgment over an open set is an arc, not a probe, and is rejected."* **The arc should reuse the probe contract rather than re-derive an instrument.** An implementer should be pointed at that section by line, not told to invent a questionnaire.

**3. Simulation is a legitimate substitute for consultation — with its limit stated in the same breath.** The thesis simulates stakeholder answers (*"symulując odpowiedzi"*) and then, in `Wady`, states the resulting exposure: *"ograniczenie do zebranych informacji … jeżeli brakuje ważnych informacji, podejście może nie zapewnić najdokładniejszej rekomendacji."* For an autonomy arc this is the licence **and** the caveat for an agent standing in for a human stakeholder: it is permitted, and it inherits a known failure mode that must be declared, not discovered. **An implementer must be told both halves.** The repo's honest-limit convention (`CLAUDE.md` §9) is the existing shape for declaring it.

**4. The fuzzy band is where this lands, and it already has a home.** `docs/decisions/ADR-81-feature-lifecycle-definition-of-done.md:45` — *"Scope — deterministic only; fuzzy deferred … The **fuzzy band** — decks, prose, judgment artifacts where closure cannot be an exact pass/fail — is **explicitly deferred to its own arc** (it needs a different, non-binary acceptance shape)."* The thesis's tradeoff analysis (*korzyści i kompromisy*) is exactly a non-binary weighing: a tactic is not pass/fail, it is better-on-this-attribute and worse-on-that. **If the AUTONOMY arc is to be the arc ADR-81 deferred to, say so in its contract explicitly** — the deferral has been open since 2026-06-24 and naming its heir is free.

**What an implementer would have to be told, concretely:**

- The north star is a **decision procedure**, not an architecture. Take steps 1–5 of `5-5-autorska-metoda.tex`; ignore chapters 3 and 6's photovoltaic content entirely.
- The **response-measure** (`miara odpowiedzi`) is the load-bearing half of a scenario. A scenario without one is not testable — the thesis says so in as many words, and ADR-81's ex-ante frozen criterion is the repo's independent rediscovery of it.
- **Do not reinvent the questionnaire.** `protocols/HANDOFF_PROCESS.md:204-216` is a stricter version of the thesis's instrument, already ratified, already gated.
- **Do not source bias mitigation to the thesis.** It has none. The live roster is `ai-council/protocols/COUNCIL_QUESTION_GUIDE.md:242-289` (seven biases, each with a fix) — and the pointer to it from `protocols/AI_COUNCIL_PROCESS.md` is currently broken (see §3).
- **Do not source adversarial debate to the thesis.** Its third-party confrontation is a single consultative interview that produced *requirements*, and it is a source of input, not a decision mechanism. The adversarial-debate lineage in this repo is `docs/archive/2026-04-24-multi-agent-debate-patterns.md` (proposer/critic/synthesizer; retention `exempt-permanent`, KEEP verdict 2026-08-26), which **predates** the thesis reads and owes it nothing.
- The thesis's own stated cost is **czasochłonność** — time. It says its method is slow, needs expertise, and is bounded by what the respondents told you. An arc that adopts the procedure inherits all three.

---

**Lane close.** Zero repo writes. Zero rows born. Zero worktrees provisioned; `git worktree list` shows only the primary throughout.

**Concurrency note — the primary checkout moved under this lane, and it was not me.** This lane opened at `96399b20` with two staged modifications (`docs/audits/README.md`, `ecosystem/doc-counts.md`) already present. It closed at `3345d303` (*"Merge branch 'docs/batch-2-w2-anchor' — the wave-2 anchor discharge (B6, append-only) + the single regeneration pass"*), with those two files now committed and a new unstaged ` M protocols/FUNNEL_LIFECYCLE.md`. That is the night mission's integrator working the primary concurrently, exactly as the contract anticipated when it denied this lane a worktree. **This lane wrote nothing** — its sole write was `~/Downloads/THESIS-COMPARE-OUT-2026-08-29.md`.

**Consequence for this artifact, checked rather than assumed:** `git diff --stat 96399b20 HEAD` touched three files — `JOURNAL.md`, `docs/audits/README.md`, `ecosystem/doc-counts.md`. **None is cited anywhere above.** Every load-bearing locator was re-resolved against the new HEAD after the move and still holds: `…fable-architecture-review.md:48` and `:52`, `protocols/AI_COUNCIL_PROCESS.md:99`, `protocols/PLAYBOOK.md:5144`, `docs/decisions/ADR-81…:45`, `protocols/HANDOFF_BOOT.md:49`, and the 57/88 ADR measurement (re-counted at `3345d303`: 57 of 88). Reads taken before the move are therefore still accurate; where a reader wants a single pin, use **`3345d303`**.
