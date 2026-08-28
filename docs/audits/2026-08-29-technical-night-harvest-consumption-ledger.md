# NIGHT-BATCH-2 CONSUMPTION LEDGER — 2026-08-28/29

**Purpose.** Every finding from the six night cloud reports, with its proposed destination. This
file is the durability mechanism: if this session is lost, the next seat executes THIS file and
nothing from the night is dropped. A rejected item stays listed with its reason — rejected is a
recorded verdict, not a deletion.

**WHO RULED WHAT — stated first, because the 2026-08-27 instance of this file opened with a
section of architect rulings and this one may not.** Tonight ran with **zero operator contact** by
design. CC is the executor, not the architect (ADR-108 §A: the operator rules functional
questions, the architect rules technical ones). So **every disposition below is a CC DERIVATION
awaiting a ruling**, never a ruling. Where a finding is discharged by an already-landed ruling the
locator is given and that IS the authority; where it needs a decision it is marked **RULING OWED**
with the owner named. L-S4 governs: *a derivation is not a plan.*

**Sources — six reports, landed byte-identical in `docs/audits/` by this batch's integrator:**
C1 candidate triage · C2 slow-marker evidence · C3 intake-61 ratification · C4 codex census ·
C5 README/VISION census · FM-C full funnel census, plus the harvest manifest.

---

## A · DISCHARGED — an already-landed ruling answers it; the locator IS the authority

- **A1** cloud-container `uv` 0.8.17 vs the pinned `==0.11.19`
  -> `protocols/STANDING_RULINGS.md` T-15 item (2)
- **A2** served-id as an admission precondition -> `protocols/STANDING_RULINGS.md` Q9
- **A3** locate / re-commission SDA-1
  -> `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` (`1a09124`)
- **A4** 664+ anchored-by-mention WARNs -> `ecosystem/disposition-register.yaml:609`
- **A5** codex surfaces: **zero REMOVAL-READY, zero bytes freed** -> C4 §4. Every class is
  BLOCKED-BY a live consumer or PROTECTED; 166 of the 168 audit artifacts are enumerated **by
  filename** inside two machine baselines that four live scripts read. The adversarial re-search
  the self-audit clause demanded **strengthened** the blocks.
- **A6** the intake archival mechanism itself -> FM-C §3.1. **Zero backlog, zero mis-filings**,
  both directions; `docs/intake/README.md:228-231` is being honoured exactly.

**A5 and A6 are the night's two most valuable results and both are NEGATIVE.** They say the two
cleanups this window kept proposing do not exist as work. That is worth more than a worklist, and
it is why they are recorded as discharges rather than quietly dropped.

## B · OWNED — an open row or a lane in flight already covers it

- **B1** `[#577]` byte-cap test -> `[#577]`, executed tonight as **lane F**.
- **B2** `**Shape:**` parse ambiguity (finding C-F) -> `[#591]` **as extended by lane G's frozen
  contract**. C1 declined to let the row id carry a clause its own Done-when never names — the
  same over-claim that cost batch-1 a repair arc.
- **B3** `[#598]` slow-marker selector -> `[#598]`, **narrowed-by-measurement but NOT
  discharged**. The 2026-08-27 durations arm returned LONG-POLE at **21.42 %** of worker-seconds
  and correctly stopped the sweep; the row is nevertheless still `status: open` and its done-when
  still asks for a regenerable set. C2 ships the design of record and shows that a *purely*
  durations-derived set cannot be regenerable.
- **B4** the conformance HTML dashboard's future -> `[#586]` (open). FM-C classifies it
  **CONSUMED-BY `[#586]` + ARCHITECTURE.md** and explicitly **not** PROTECTED: *"a regenerable
  artifact earns no retention ruling, and I decline to invent one for it."* Wave-2 lane N (DB-1)
  is its successor arc.

## C · CANDIDATE — needs a decision. RULING OWED; owner named.

- **C1 · ratchet zero-headroom policy** — three incompatible forms (authorized per-arc raise /
  scope narrowing / accepted freeze with a declared destination). `[#447]` owns the raise
  mechanism, not the freeze, and the candidate's own text forecloses the cheap form. *Owner:
  architect.*
- **C2 · the SDA-1 admission instrument** — carries producer-pack prerequisites, corpus rotation
  and transport-health preflight. Corpus rotation **amends standing ruling Q9**; the preflight has
  a real siting fork (SessionStart provider probe vs admission-instrument precondition). All three
  are preconditions on ONE instrument, so this is **one** intake, not three. *Owner: architect.*
- **C3 · tile manifest for rotation** — a design fork inside READY intake **#59**, whose one born
  row explicitly excludes it. It **joins** #59; it does not open an intake. *Owner: architect.*
- **C4 · three intake docs archivable only behind a STATUS RULING** — **#19** (SEED, consumed by
  ADR-82, only row `[#446]` CLOSED — the strongest), **#26** and **#28** (both ACCEPTED, consumed
  by ADR-110 / ADR-112). `docs/intake/README.md:228-231` makes ACCEPTED *deliberately* non-terminal
  because *"a standing decision stays live"*, so a status flip is an operator act.
  **CAUTION on #28:** ADR-112:87 says fourteen candidates in its §C are still actionable — §C must
  be ruled before the doc is flipped. *Owner: operator.*
- **C5 · `docs/intake/README.md` is FRESH AND WRONG** (FM-C D1) — six live intakes (ids **56–61**)
  render `[MISSING-ID]` inside an off-enum `### OTHER (6)` group, and the index says `READY (13)`
  while disk has **19**. Root cause reproduced: an **unquoted backtick opening a YAML scalar** on
  the `consumers:` line, line 5 column 12, identical in all six; `_parse_frontmatter` returns `{}`
  by design. **The `intake-index-freshness` gate cannot see it** — regen-and-diff reproduces the
  wrong output byte-for-byte. Separately, `consumers:` is not in the ADR-98 companion-field schema
  at all. The fix is six quoted strings, which is exactly why it must be **triaged** rather than
  done in passing. *Owner: architect.*
- **C6 · `intake-id: 14` is assigned to THREE files** (FM-C D2) — `intake #14` is the join key
  both `consumer_at_landing` and this census rely on, so every citation of it is ambiguous. The id
  space is otherwise clean: 1..61, no gaps, no other duplicate. *Owner: architect.*
- **C7 · `tasks/` rows carry NO `source:` field — 0 of 344** (FM-C P1) — the funnel doctrine and
  FM-2's FAIL-leg (c) are both written against a field that does not exist. `· refs …` is the
  de-facto one and **153 of 153 open rows carry it**. One act, ruled once: either the doctrine
  names `refs`, or `tasks/` grows a `source:` field. *Owner: architect.*
- **C8 · README/VISION merge M1 — five lines in one file** — of ~5,881 censused references,
  ~5,700 are immutable, append-only, generated or gate-coupled. Three `protocols/PLAYBOOK.md`
  sites currently assert a root README exists and is *"Living, never delete"*; correcting them
  makes the standing prohibition **more** consistent, not less. ADR-49/65 is the condensation
  licence. **Zero `VISION.md` edits are proposed**, so the ADR-114 question is neither answered nor
  made cheaper by side effect. *Owner: architect.*
- **C9 · ADR numbering** — **27 numbers absent** (1–26 and 44), unexplained by
  `docs/decisions/README.md` (FM-C D3); and **ADR-61 uses a different status schema** — YAML
  frontmatter rather than the `- **Status:**` prose line its 87 siblings use (D4). Not asserted as
  loss (ADR-49/65 condense-to-git is live doctrine), recorded so it is not rediscovered a third
  time. *Owner: architect.*
- **C10 · `[#598]`'s own `refs` list cites `conftest.py`, which exists nowhere in the repo** —
  `pyproject.toml:144-145` records the absence deliberately (`[#430](a)`, STANDING_RULINGS F5:
  permitted-not-mandated, none exists). A design assuming a conftest hook point assumes a file
  that would have to be **created**, which is an ADR-101 Rule C question, not a free move.
  *Owner: architect.*
- **C11 · `funnel_coverage` is non-recursive** — the 20 files under
  `docs/audits/*/launch-contracts/` are real governed objects and are invisible to it; that gap is
  the 97.5 % coverage fraction FM-C reports. Fixing it changes what the detector measures.
  *Owner: architect.*
- **C12 · the launch-contracts home has an implicit schema nothing documents** — every `*.md` in
  it must parse as a lane contract. Found by this session at freeze (defect D-M1):
  `check_substrate_declaration._corpus` treats every file there as a contract, while Ch8's
  *"copied there byte-identical"* reads as permission to copy a bundle in. It is not.
  *Owner: architect.*

## D · REJECTED — recorded with the reason, not relitigated

- **D1 · intake #42 as archivable.** FM-C's own graph flagged it; **opening ADR-115 refuted it** —
  §6 and §7 name #42's second and third open questions as still open. `docs/intake/README.md:242-257`
  governs exactly this: a partially-ruled intake keeps its pre-ratification status and gains a
  pointer note. Correctly DRAFT.
- **D2 · a merge whose net effect is "one document explaining the repo".** C5 raised it against
  itself in its own self-audit and **withdrew it**: it is the root `README.md` by another name,
  which `CLAUDE.md` §5 rule 5 forbids and ADR-114 has PARKED.

## E · MEASUREMENT-OWED-LOCAL

Each report carries its own section; they are not restated here. The class is anything needing
`scripts/audit.py`, a git hook, or the pytest suite — none of which can run on the cloud rung.
**None of it was estimated.** All six lanes honoured the discipline.

## F · METHOD FINDINGS — about the instruments, not the corpus

- **F1 · The cloud clone is SHALLOW.** `.git/shallow` exists, history starts 2026-08-23, 340
  commits over 7 distinct dates. `git log --diff-filter=A` — the command an A1-style
  dated-transition clause names — returns the **graft boundary** for **835 of 951 objects
  (87.8 %)**. Only 116 objects have a trustworthy git birth date there. Any cloud brief asking for
  git-derived dates is asking for fiction; frontmatter and filename dates are intact and were used
  instead. **This is a standing property of the cloud substrate, not a one-night accident.**
- **F2 · A filename-keyed consumption graph has a measured ~42 % false-orphan rate.** FM-C's first
  pass produced 19 orphan intakes; identifier keying cut it to 11. `consumer_at_landing.py:22-27`
  had already recorded the trap. The same graph mis-flagged 1 of 4 archivable candidates — a 25 %
  error rate on the highest-consequence list in that report. Both were caught by the report's own
  self-audit clause, which is the argument for keeping that clause in every brief.
- **F3 · A regen-and-diff freshness gate cannot detect a generator bug.** C5 is the live instance.
  The gate is a **currency** check, not a **correctness** check, and the two are conflated wherever
  "the index is gated" is offered as evidence that the index is right.
- **F4 · An explicit output-shape clause fixed the byte-identity deviation for free.** 2026-08-27:
  2 of 4 reports opened with prose before their own heading, and the deviation had to be recorded.
  2026-08-29, with one clause in the shared cloud brief: **6 of 6 start at byte 0 with their own
  heading.** No harvester change was involved.
- **F5 · One attribution error against a lane, recorded rather than repeated.** C2 states that its
  brief's "WHAT TO GROUND IT IN" names `conftest.py`. It does not — `grep -i conftest` over the
  brief returns nothing. The **substantive** half of the finding is true and is carried as C10; the
  attribution is not.

## G · WHAT THIS LEDGER OWES THE NEXT SEAT

1. Nothing in section C may become a `tasks/` row without triage — ADR-111 and Z-G1 both say the
   only path is CANDIDATE -> intake (ADR-98) -> ratification. C1's own proposal is that the five
   candidates it triaged collapse into **at most three intake acts**, not five rows.
2. Sections A and B need no act at all. They are recorded so the next census does not re-derive
   them, which is the cost F2 measures.
3. The one item with a live clock is **C5**: the intake index is wrong *now*, in a generated
   surface a boot sequence reads, and its gate is structurally unable to notice.
