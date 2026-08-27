# CLOUD-NIGHT-C4 — Backlog quality census (read-only)

**Substrate** cloud, read-only · **Tree** `.dev-knowledge` @ `d8211b0` (origin/main, 2026-08-26) · **Writes** none. This report proposes; the architect rules.

---

## 0. Method, and the one limit that shaped it

**Row corpus.** 328 `tasks/*.md` (plus `README.md`, no frontmatter). Live status counts, measured:
`grep -h '^status:' tasks/*.md | sort | uniq -c` → **open 176 · closed 121 · deferred 26 · retired 4 · superseded 1**.

**Reconciling the brief's "~191".** 191 = the diagnostic's 165 open + 26 deferred, and W3 uses the same denominator (`STANDING_RULINGS.md:2898` — *"191 rows carry 245,486 bytes of body"*). Live that set is now **202** (176 + 26): 11 rows were born after the diagnostic ran. This census treats the **176 `status: open`** rows as the subject and the 26 `deferred` as the existing icebox.

**HARD LIMIT — the age axis had to be rebuilt.** The clone is shallow: `.git/shallow` present, oldest commit 2026-08-21, `git log --oneline -- BACKLOG.md | wc -l` → **16 revisions**, and `tasks/` shows a single add-date of 2026-08-22. The diagnostic's 781-revision BACKLOG birth-age scan is **not reproducible here**, and filesystem mtimes are all clone-time (`Aug 26 15:06`). So I built an **id→birth-age interpolation** from the 75 (id, age) pairs the diagnostic itself publishes (§2.1 twenty-oldest + §4.3 ranked-60), ids being allocated in birth order.

**It validates against W3's own table on 4 of 5 buckets, exactly:**

| threshold | W3 measured | this census (interpolated) |
|---|---:|---:|
| 90 d | 0 | **0** ✓ |
| 75 d | 14 | **14** ✓ |
| 60 d | 19 | **19** ✓ |
| 45 d | **49** | 48 (+ boundary `[#332]` @ 44.4 → **49**) |
| 30 d | 94 | **94** ✓ |

Ages below are therefore **inferred**, ±1 d at the boundary, and load-bearing only as a rank. Every other claim is a quoted line or a re-runnable command.

**PROTECTED set (not proposed for closure, per the constraint).** 8 rows carry a `T-nn` section header naming them in `protocols/STANDING_RULINGS.md`: **`[#210] [#341] [#347] [#351] [#362] [#389] [#414] [#418]`**, plus **`[#585]`** (W5, `:2924`). Correction against my own first pass: `[#23]` is *not* protected — its only U/V/W appearance is as W3's age exemplar (`:2881` *"the oldest is `[#23]` at 86 d"*), which is a measurement, not a ruling.

---

## 1. Kill-candidates, ranked (top 40)

Scored on: age band · P3 · a live `DEFER`/peg clause while `status: open` · verdict-language mention in a 2026-08-18+ artifact · zero mentions in any 2026-08-20+ artifact · no `kill-candidates:` line · decision-shaped-not-build-shaped. Rows younger than 7 d are excluded (too young to judge). PROTECTED rows are scored −10 and none reached this table.

| # | row | age | p/sz | CASE for closing | COUNTER-CASE |
|---|---|---:|---|---|---|
| 1 | `[#43]` | 86 | P3/L | Row's own body: *"scaffold scope folded into `docs/intake/2026-07-08-func-new-project-bootstrap.md` (intake-id 6) — **superseded-by that intake**"*. Trial audit `2026-08-19-technical-backlogmd-trial.md:134` classes it *"L-sized, folded into an intake by supersession"*. | Body also says it *"persists as the decomposition target"* — killing it leaves intake #6 without a task carrier. **Close only if #6 is re-anchored.** |
| 2 | `[#82]` | 83 | P3/M | `2026-08-19-technical-c2-review-profiles.md:455`: *"It does not close `[#82]`: **0 of 9 members carry a profile**"* — 83 days, zero denominator movement. | Same audit `:404` says the choice *"decides whether `[#82]` can close from the hub at all"* — a **ruling is owed**, so this is CANDIDATE-for-decision, not a clean kill. |
| 3 | `[#117]` | 80 | P3/S | Gated on VF-1 auth probe never run; `2026-08-23-technical-phase0-preconditions.md:167`: *"**Superseded in scope**, deliberately alive as a carrier."* | Un-deferred 2026-08-11 on a **met peg** (`[#270]` closed at `679d8eca`) — the operator deliberately revived it 15 d ago. |
| 4 | `[#127]` | 80 | P3/S | `2026-08-18-census-p10-grooming-evidence.md:149` scores it **git silent, 0 / 0** — no commit has ever touched it in 80 d. | The `verify` skill is live and its failure contract genuinely has no test; this is un-started, not overtaken. |
| 5 | `[#146]` | 77 | P3/S | Clause (a) **landed** (`PLAYBOOK:1016-1024`, verbatim). Only "the sweep" remains, unscoped, 77 d. | Row itself flags *"Authorship unverified"* — the landed text may belong to `#11`. Closing on a half it may not own is the wrong record. |
| 6 | `[#171]` | 70 | P3/M | `2026-08-21-fresh-eyes-cloud-r3-conformance.md:88` F1: *"Leg-2 scope is **unresolvable from the row**. Three incompatible readings… **Any close of `[#171]` today is ambiguous** about what was closed."* An unclosable row is a kill candidate by construction. | It is the landing surface `[#169]`/`[#322]` are both pegged to. Kill it and two deferred rows lose their peg. **Re-cut, don't delete.** |
| 7 | `[#269]` | 51 | P3/S | `2026-08-19-technical-c3-grooming-wave2.md:1539`: *"#269 count-tiered index shape — header repoint to ADR-100 **already DONE**"*, and the row concedes the freshness hook *"LANDED EARLY 2026-07-08"*. **Both Done-when legs may be discharged.** | The count-tiered *shape* itself may not be rendered. One `git show` of `docs/audits/README.md` settles it — the cheapest verdict on this list. |
| 8 | `[#285]` | 49 | P3/S | Absorbed six rows (*"absorbs #67 #18 #27 #39 #217 #219"*) and shipped none in 49 d — a classic absorber that converts six deaths into one immortal row. | Its Done-when forbids the cheap path (*"a bare stamp to green a gate is forbidden"*). The PLAYBOOK re-read is real work, not rot. |
| 9 | `[#293]` | 48 | P3/S | Executed, then **reverted in full** — *"the architect ruled ADR-60 wins over a task row's stated path"*. The row's own named path is now forbidden doctrine. | Its own body names the fix: *"`[#303]` … must land first"*. It is **blocked**, not dead — see §4 edge 2. |
| 10 | `[#71]` | 85 | P3/S | Pure reconciliation of `ENVIRONMENT.md` against `ls ~/.claude/…`; 85 d untouched; no gate depends on it. | The Codex/"Rejected" contradiction it names is a **live false statement** in a canonical doc. |
| 11 | `[#116]` | 80 | P3/S | PowerShell `args:[]` exec-form migration from a 2026-06-07 audit; superseded in practice by the hook roster's growth. | The Windows quoting failure class is real and unfixed. |
| 12 | `[#99]` | 80 | P3/S | 3-line digest ergonomics; 80 d, no citer outside its birth audit. | Genuinely cheap; the operator still needs a second command to learn what is red. |
| 13 | `[#130]` | 79 | P3/S | "Periodic pass" with no cadence, no owner, 79 d. Done-when has grown a **second** arm (capture-time scrub) without the first ever running. | The dedupe-at-write arm is a real, testable defect. |
| 14 | `[#145]` | 77 | P3/M | Self-describing as a *"pass"*; its own A4 advance already landed; the residue is an open-ended enumeration. | ADR-81 (a) names the fresh-session test as doctrine. |
| 15 | `[#170]` | 70 | P3/M | 70 d; re-phrased 2026-08-12 because its Done-when pointed at `#168`, *"which has no `tasks/168-*.md` in any status"* — a row whose target never existed. | `[#139]` is deferred **pegged to `[#170]`**. Killing it strands the peg. |
| 16 | `[#189]` | 68 | P3/S | Body: *"The methodology-reach question … **is decided in `#153`**"* — the row defers its own premise to another open row. | `~/.claude` drift is the recurring failure the row names. |
| 17 | `[#244]` | 53 | P2/L | P1–P4 all **SHIPPED**; P5/P6 *"both UNOWNED — #221 closed at 8aab4356; **no successor**"*. An epic with no owner for its remainder. | L-sized with a real remaining scope; kill converts to two unfiled rows. **Prefer split-and-close-the-shipped-half.** |
| 18 | `[#271]` | 51 | P3/L | Its constraints are carried *"ex-ante, not renegotiable"* from intake #1 — the row is a **charter**, and the nightly loop it describes has been replaced in practice by the lane/batch protocol. | `[#288]` depends on it (§4 edge 1). |
| 19 | `[#324]` | 45 | P3/M | `2026-08-23-technical-backlog-adjudication-prep.md:1478`: *"`65c9827e` discharges **leg c only**… the routine + consumer clauses are untouched."* Row is explicitly *"Charter only — do not build this session"* — 45 d ago. | Overlaps `[#348]`/`[#419]`/`[#426]` — see §2 cluster D. Merge, don't orphan. |
| 20 | `[#227]` | 55 | P3/S | Row states its own target is *"a self-labelled v0.1 unimplemented stub with **no readers**… and no gate"*. Moving a dead file is not work; **deleting it is the honest act**. | ADR-101 Rule A/C seal `protocols/` — the move needs operator approval either way. |
| 21 | `[#234]` | 54 | P3/S | Hardening a WARN to a FAIL on a cross-repo path class with n=1 witness in 54 d. | Real teeth-gap; `_FALLBACK_EXCLUDE_DIRS` still excludes `.claude`. |
| 22 | `[#241]` | 54 | P2/S | 6 candidates all already dispositioned `pre-existing` in `ecosystem/disposition-register.yaml` — the register already holds the outcome the row would produce. | Two declarations must ride a genuine freshness re-stamp; the row is the only carrier of that coupling. |
| 23 | `[#242]` | 54 | P2/M | `2026-08-23-technical-lane-status-grammar.md:215`: *"This lane therefore **cannot close `[#242]`**, and does not claim to."* Two lanes have now built around it without closing it. | **Cannot close before `[#362]`** — `[#362]`'s Done-when binds it (§4 edge 13). PROTECTED-adjacent. |
| 24 | `[#266]` | 51 | P3/S | One sentence of guidance into two templates; 51 d; the precedent it codifies was already ratified 2026-07-05. | Genuinely 20 minutes of work — cheaper to do than to adjudicate. |
| 25 | `[#267]` | 51 | P2/S | Row's own header: *"REFINEMENT… **not a closure gate**; armed-as-enforcing NOT adopted as doctrine"*, and half-a is DEFERRED as a *"design decision, feasibility proven"*. | Its mechanism choice is explicitly *"LEAN (not decided)"* — a decision is owed. |
| 26 | `[#273]` | 50 | P3/S | Escalation teeth for a sentinel that already nudges; 50 d, zero touches. | The month-long unreviewed window it was born from is a real measured failure. |
| 27 | `[#274]` | 50 | P3/S | A rubric-wording change (name a "dogfood-signal prior"); 50 d; the smallest surviving row on this list. | Trivially closable — likely faster to land than to icebox. |
| 28 | `[#277]` | 50 | P2/M | `2026-08-19-technical-c3-grooming-wave2.md:265` reports the two STRONG false positives *"no longer"* surface — leg (a) looks discharged. | Legs (b) and (c) (WEAK-heuristic rework, hub↔plugin parity test) are untouched, and `[#487]` consumes this pipeline. |
| 29 | `[#288]` | 49 | P3/S | Depends on `[#271]` (P3/L, itself a kill candidate at #18). A dependency chain of two dormant P3s. | Model-swap detection is newly load-bearing given the provider work in W1. |
| 30 | `[#296]` | 48 | P3/S | Live repro 2026-08-06 **refuted the row's own premise** (*"the row's original guess… is refuted"*); it survives only as a cosmetic locator fix. | One-line fix with a test; cheap. |
| 31 | `[#297]` | 48 | P3/S | Un-deferred 2026-08-09 on a peg the row concedes was *"met 2026-07-07, **one day BEFORE the peg was written**"* — the deferral was never real. | The billed-child constraint it removes is a genuine blocker for `#215`. |
| 32 | `[#298]` | 48 | P3/S | Un-deferred 2026-08-09 because *"peg 'next handoff-group pass' **RAN this window and skipped this row**"* — it has now been skipped by its own trigger. | Three concrete, tested WARN legs. Also `[#301]` is deferred-pegged to it. |
| 33 | `[#335]` | 43 | P3/S | `c3-grooming-wave2.md:283`: *"ASK: `reconciled_versions` **no longer flags**…"* — the false positive it exists to remove may already be gone. | If it is gone, the standing disposition should auto-clear; verify before closing. |
| 34 | `[#348]` | 39 | P3/S | `2026-08-21-technical-seat-act0-act1-contract.md:65` already directs: *"**verify DEAD-candidate** against live evidence; if confirmed, **close it**"*, and `n4-grooming-wave1.md:751` finds **both Done-when clauses met** (routine block present with all six ADR-105 fields; gate `[#270]` closed). | Same audit flags a caveat: the row is *"the live anchor"* for the routine block it validates. |
| 35 | `[#369]` | 36 | P3/S | Re-scoped once already because its clause named an absolute gate count that *"re-breaks every time a hook lands"*. Overlaps six existing regen-and-diff hooks. | The header-generation property genuinely rests on the test suite alone. |
| 36 | `[#391]` | 35 | P3/S | Row offers a disjunction (*"either wire it… or narrow #384"*) — an undecided row, 35 d, in the E9 theme with 5 open rows total. | Completes `#384`'s own nightly-lane claim, which is currently false. |
| 37 | `[#393]` | 35 | P3/S | **Consumer-repo work** — three files in `corp-sca-time-automation`. `n4-grooming-wave1.md:716` calls it *"the sheet's cleanest example"*; hub cannot execute it (Layer-2 invariant). | Nothing else discharges `#384`'s rot-findings clause. |
| 38 | `[#419]` | 32 | P2/M | Its rule + gate **landed 07-26 (ADR-105)**; the residue is *"coverage pegged to `[#426]`"* — a peg on another open row, i.e. it is `[#426]`'s tail. | Amended by **operator ruling** 2026-08-11 (Fork 3 / I-F3) and marked **STAYS OPEN** in-row. Treat as operator-touched. |
| 39 | `[#420]` | 32 | P3/S | *"operator-raised structural question, **filing only**"* — a question, not work, 32 d old. | Carries a live freeze: *"**Do NOT touch `docs/archive/` while this is open**"*. Closing it unfreezes 9 files with no destination. |
| 40 | `[#112]` | 80 | P2/M | 80 d; absorbs `#105` + `#157`; its CLAUDE.md §5 self-contradiction leg was **independently resolved** by v2.65 rule-7 re-scoping. | The `adr_amend` sanctioned-writer mechanism does not exist. Not overtaken — un-started. |

**Three P2 elders scored into the top 42 and are deliberately NOT proposed:** `[#123]` (80 d), `[#153]` (76 d), `[#185]` (69 d). Each names a live, unbuilt mechanism with no substitute organ; age alone is not a case against them. `[#153]` is additionally the named decider for `[#189]` and a kill-candidate reference for four rows.

**`kill-candidates:` line audit.** Only **4 of 176** open rows name a real kill target; 126 say `none — <reason>`; **46 carry no line at all** — and those 46 are exactly ids ≤ 388, i.e. every row born before the `backlog-filing-backpressure` commit-msg hook existed. **One spent line found:** `[#400]` (`kill-candidates: … #370 … are spent`) — target `#370` is `status: closed`, and the row itself already records the premise as *"falsified"*. `[#303]`'s line names `#293` (open, and `#293` names `#303` as its prerequisite — a mutual-reference loop, §2 cluster F).

---

## 2. Duplicate / overlap clusters

Cosine similarity over `Done when:` text (TF-IDF, doc-artifact paths excluded so co-birth in one packet doesn't fake an edge) + shared **code** targets. 7 clusters, 16 rows.

| # | rows | evidence | proposal |
|---|---|---|---|
| A | `[#341]` `[#347]` `[#362]` | sim 0.31 / 0.28 / 0.26; shared `protocols/STANDING_RULINGS.md` (+ `PLAYBOOK.md` on the first pair) | **KEEP ALL THREE — all three are PROTECTED** (T-31 / T-37 / T-36). Similarity is an artifact of a shared *discharge surface*, not shared subject. Flagged so the morning does not re-cut them. |
| B | `[#404]` `[#422]` `[#547]` (+ `[#511]`) | 3 shared code targets each: `scripts/gen_handoff.py`, `protocols/HANDOFF_PROCESS.md`, `PROBES.md` | **MERGE into one handoff-generator arc.** Four E1 rows, 9–34 d, all editing one generator; `[#422]`'s own line already concedes `[#404]` is adjacent. Keep `[#404]` (oldest, most concrete), fold the rest. |
| C | `[#587]` `[#588]` | sim 0.28; shared `scripts/journal_anchor.py`; both born today, both P1, both from intake `2026-08-26-tech-loop-tax-and-gate-performance.md` | **MERGE.** P-1 and P-2 are two passes over the same module in the same file; two P1 rows for one edit inflates the P1 count. |
| D | `[#277]` `[#428]` | sim 0.25, shared source `2026-08-15-technical-night3-decision-queue.md` | **KEEP BOTH, declare an edge.** Different organs (closure proposer vs triage producer), same root: a routine reporting a signal nobody can act on. Candidates to sequence behind `[#487]`. |
| E | `[#387]` `[#561]` | sim 0.25; both E7/P2/S; both re-price the same buy-vs-build substrate question | **MERGE into `[#561]`** (7 d, has the corrected Hetzner basis) and kill `[#387]` (35 d, *"rewrite the intake BEFORE anything ingests it"* — a precondition that 35 d of nothing-ingesting has made moot). |
| F | `[#293]` `[#303]` | shared `scripts/seed_runbook.py` + `docs/handoffs/README.md`; mutual reference | **KEEP BOTH, order them** — `[#303]` first (§4). Do not merge: one is a code change, one is operator-gated fan-out. |
| G | `[#389]` `[#390]` / `[#401]` `[#413]` | sim 0.24 / 0.23, **no shared code targets** | **NO ACTION — false positives.** Reported so they are not re-surfaced by the next text-similarity pass. `[#389]` is PROTECTED (T-24). |

Also flagged, below the join threshold but structurally overlapping: `[#533]` `[#534]` `[#535]` (all three edit `scripts/audit.py`, ages 9.0–9.3, and `[#534]` exists *only* because `[#533]`'s decomposition broke locators — **it is `[#533]`'s cleanup step, not a peer row**).

---

## 3. Icebox-45 d list — verbatim-ready

W3 adopted 45 d and measured **49 rows**. This census reproduces **48** by interpolation; the 49th is the boundary row **`[#332]`** (interpolated 44.4, `Fleet dependency-version parity`, P2/M, E6). Exact id list, oldest first, for a mechanical `status: open → deferred` sweep:

```
[#43]  86d P3/L E6      [#227] 55d P3/S E5      [#274] 50d P3/S E7
[#23]  86d P3/S E4      [#234] 54d P3/S E2      [#285] 49d P3/S E5
[#71]  85d P3/S E5      [#242] 54d P2/M E2      [#288] 49d P3/S E7
[#82]  83d P3/M E6      [#241] 54d P2/S E2      [#289] 49d P2/M E2
[#127] 80d P3/S E7      [#244] 53d P2/L E6      [#293] 48d P3/S E1
[#123] 80d P2/S E7      [#245] 53d P2/M E6      [#296] 48d P3/S E2
[#117] 80d P3/S E2      [#266] 51d P3/S E3      [#297] 48d P3/S E2
[#116] 80d P3/S E2      [#267] 51d P2/S E2      [#298] 48d P3/S E1
[#112] 80d P2/M E2      [#269] 51d P3/S E5      [#303] 47d P2/S E2
[#99]  80d P3/S E2      [#271] 51d P3/L E7      [#317] 46d P2/M E7
[#130] 79d P3/S E3      [#273] 50d P3/S E7      [#324] 45d P3/M E2
[#146] 77d P3/S E2      [#278] 50d P2/M E7      [#331] 45d P2/S E6
[#145] 77d P3/M E3      [#277] 50d P2/M E2      [#329] 45d P3/S E6
[#153] 76d P2/M E2      [#276] 50d P2/M E6      [#327] 45d P2/M E6
[#171] 70d P3/M E2      [#220] 55d P2/M E2      [#332] 44d P2/M E6  <- W3's 49th (boundary)
[#170] 70d P3/M E2      [#185] 69d P2/M E2      [#189] 68d P3/S E2
[#210] 61d P3/S E2  <- PROTECTED (T-25): exclude from the sweep
```

**Two carve-outs the sweep must honour:** `[#210]` is PROTECTED (T-25) — leave `open`. `[#242]` cannot be moved independently of `[#362]` (PROTECTED, and `[#362]`'s Done-when binds `[#242]`'s terminal status). Net mechanical sweep: **47 rows**, leaving 129 open — close to W3's projected 116, the difference being the 11 rows born since.

**Free adjacent arithmetic:** the 26 `deferred` rows are already iceboxed, and **9 of them carry pegs that are spent or dead** — `[#325]` (*"peg #221 DEAD, unreplaced"*), `[#294]`/`[#308]` (both re-pegged to the same intake #25 W-wave decision), `[#139]`→`[#170]`, `[#169]`→`[#171]`, `[#188]`→`[#112]`, `[#218]`→`[#487]`, `[#301]`→`[#298]`, `[#492]` (*"the calendar leg is SPENT and dropped"*). Every one of those pegs points at a row in §1's kill list. **Killing a §1 row without re-pegging its dependent orphans a deferred row** — this is the single highest-risk mechanical error available at morning adjudication.

---

## 4. Inferred dependencies — 17 proposed edges

Extracted from dependency-language sentences in row bodies where both endpoints are open. Format is `_DEPID_RE`-parseable (`#` retained). **A proposal file, not an edit.**

| # | add to row | proposed line | the sentence that implies it |
|---|---|---|---|
| 1 | `[#288]` | `depends-on: [#271]` | *"the survival-metric review at **#271 depends on comparing** like-for-like"* |
| 2 | `[#293]` | `depends-on: [#303]` | *"`[#303]` — this row's own named **prerequisite** — must land first"* |
| 3 | `[#385]` | `depends-on: [#383]` | *"**Gated on the apply channel existing** — the contract + regenerate/apply path from [#383]"* |
| 4 | `[#413]` | `depends-on: [#400]` | *"either the colors semantics cite the ruled ownership model … (with **`[#400]`'s ruling** referenced)"* |
| 5 | `[#419]` | `depends-on: [#426]` | *"coverage **pegged to [#426]**"* |
| 6 | `[#548]` | `depends-on: [#329]` | *"[#329]/[#331]/[#332] **CONSUME the manifest** and none owns producing it"* |
| 7 | `[#548]` | `depends-on: [#331]` | (same sentence) |
| 8 | `[#548]` | `depends-on: [#332]` | (same sentence) |
| 9 | `[#559]` | `depends-on: [#332]` | *"the mechanism `[#332]`, `[#334]` and `[#351]` are each **separately waiting** on"* |
| 10 | `[#559]` | `depends-on: [#334]` | (same sentence) |
| 11 | `[#559]` | `depends-on: [#351]` | (same sentence) |
| 12 | `[#579]` | `depends-on: [#153]` | *"`[#146]` and `[#153]` **CONSUME such an ADR** rather than produce it"* |
| 13 | **`[#242]`** | **`depends-on: [#362]`** | `[#362]`'s Done-when: *"and **`[#242]` does not reach a terminal status before this row does**"* — the brief's named class; my prose scan missed it because the constraint is written as a negation, which is itself a finding for any future extractor |
| 14 | `[#589]` | `depends-on: [#523]` | *"`[#523]` … would **consume this projection** rather than duplicate it"* |
| 15 | `[#591]` | `depends-on: [#582]` | *"`[#582]` owns the router ARC that this validator is a **precondition of**"* |
| 16 | `[#594]` | `depends-on: [#582]` | *"`[#582]`'s ARC **consumes this schema**"* |
| 17 | `[#596]` | `depends-on: [#583]` | *"`[#583]`'s sweep rows are shown to be **instances of it**"* |

Adopting all 17 takes declared dependencies from **4 → 21 rows** and makes 13 rows genuinely blocked, so "ready now" stops meaning "everything" for the first time. `[#424]` (the row that owns the inert-`_DEPID_RE` defect) must land first or edges 1–17 parse but never gate.

---

## 5. The 40–60 active slice — proposed n = 52

Rule: **all 12 open P1s** + the **40 highest-ranked P2s** (age < 45 d, not inferred-blocked), ordered S → M → L then age descending — the diagnostic's own ranking rule, so the window is continuous with §4.3 of that report.

| theme | n | rows (id · pri/size/age) |
|---|---:|---|
| **[E2]** Enforced governance | 20 | `[#514]`P1/M/16 `[#519]`P1/M/16 `[#579]`P1/L/0 · `[#389]`S/35 `[#401]`S/34 `[#405]`S/33 `[#414]`S/32 `[#418]`S/32 `[#424]`S/31 `[#454]`S/26 `[#457]`S/26 `[#477]`S/23 `[#478]`S/23 `[#518]`S/16 `[#520]`S/16 `[#531]`S/10 `[#534]`S/9 `[#560]`S/7 `[#592]`S/0 `[#345]`M/39 |
| **[E7]** Tooling & evaluation | 18 | `[#588]`P1/S/0 `[#528]`P1/M/11 `[#555]`P1/M/8 `[#580]`P1/M/0 `[#587]`P1/M/0 `[#581]`P1/L/0 `[#582]`P1/L/0 · `[#340]`S/40 `[#341]`S/40 `[#387]`S/35 `[#428]`S/31 `[#431]`S/30 `[#440]`S/29 `[#445]`S/28 `[#493]`S/21 `[#535]`S/9 `[#561]`S/7 `[#347]`M/39 |
| **[E8]** ARC-5 execution | 6 | `[#359]`P1/M/37 · `[#371]`S/36 `[#448]`S/26 `[#354]`M/37 `[#357]`M/37 `[#362]`M/36 |
| **[E5]** Canonical-file integrity | 4 | `[#589]`P1/M/0 · `[#551]`S/9 `[#585]`S/0 `[#590]`S/0 |
| **[E1]** Handoff continuity | 3 | `[#390]`S/35 `[#404]`S/34 `[#422]`S/31 |
| **[E6]** Cross-repo universalization | 1 | `[#332]`M/44 |

**Three properties of this window the architect should weigh before adopting it.**
1. **E2 + E7 are 38 of 52 (73%)** — the same concentration the whole open set has (58 + 49 of 176). The cap does not diversify the backlog; it just makes the concentration visible.
2. **Six of the 12 P1s were born today** (`[#579]`–`[#589]`, ARC packets A–D + P-1/P-2). If the cap is adopted as written, the active window is dominated by rows with zero elapsed time, and five §1 kill candidates older than 45 d sit outside it. That is the intended effect of a cap — stated so it is a choice, not a surprise.
3. **30 unblocked P2s fall below the cut** (`[#426] [#430] [#442] [#451] [#487] [#506] [#510] [#511] [#522] [#523] [#533] [#538] [#552] [#554] [#564] [#567] [#568] [#570] [#571] [#572] [#574] [#575] [#576] [#577] [#583] [#584] [#593] [#595] [#597] [#383]`). They are **not iceboxed by this proposal** — they are simply not in the window. If the cap is meant to *shrink* rather than *rank*, those 30 need a second disposition, and several (`[#487]`, `[#523]`, `[#583]`, `[#577]`) are inputs to rows that *are* in the window.

---

### Closing arithmetic, for the birth budget
If the architect rules the §1 top-40 at even a 50% CLOSE rate, and the §3 sweep moves 47 rows to `deferred`, the open set goes **176 → ~156 open with ~73 deferred**, and the banked-births ledger refills by every ruled closure. The §4 edges are what stop it refilling straight back into a flat 156.