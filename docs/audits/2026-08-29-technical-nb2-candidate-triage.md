# NB2 · CLOUD C1 — the 11-CANDIDATE triage sheet

**Batch:** night-batch-2 · **Lane:** C1 (cloud, read-only) · **Repo:** `dev-knowledge` @ `fcc9485` (`origin/main`) · **Date:** 2026-08-28
**Input:** `docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md` §6 (lines 195–229), the batch-1 close packet's filing wave.
**Writes performed:** zero. No branch, no commit, no stage, no gate run.

---

## 0. Method, and what this lane could not establish

Every candidate below is quoted from the packet's own §6 before it is dispositioned. Row ids resolve against `tasks/*.md` (the source of truth since `[#589]`), never against `BACKLOG.md`. Every disposition carries a locator that I opened.

**Gates were not run** — the container's `uv` is 0.8.17 against the repo's `required-version = "==0.11.19"`, so `uv run --locked …` cannot start:

```
$ uv --version   -> uv 0.8.17
$ python3 --version -> Python 3.11.15
```

Anything that would need `scripts/audit.py`, a hook, or the pytest suite is marked **MEASUREMENT-OWED-LOCAL** and is collected in §4. It is not estimated anywhere.

**Corpus counts, computed on this clone (`ls <glob> | wc -l`, `wc -c`):**

```
docs/intake/*.md        56   == brief's 56
docs/decisions/*.md     89   == brief's 89
tasks/**/*.md          344   == brief's 344
BACKLOG.md          67,883 B == brief's 67,883 B
docs/audits/*.md       773   != brief's 769   (+4)
```

The audits delta is explained, not asserted: commit `e23e001` (2026-08-28 23:58:43 +0200, *"night-batch-2 dispatch record"*) added exactly four top-level audit files — `2026-08-28-technical-batch-2-manifest.md`, `-fm-wave2-frozen-bundle.md`, `-night-batch2-frozen-bundle.md`, `-night-mission-authorization.md` — plus 13 lane contracts in a subdirectory (which the top-level glob does not count). The operator measured at 23:36, the dispatch landed at 23:58. **769 + 4 = 773. The clone is ahead of the disk measurement by exactly tonight's dispatch.**

---

## 1. The sheet

Flat, fenced, copy-safe:

```
#   candidate                          disposition   resolving locator / row
--  ---------------------------------  ------------  -----------------------------------------------
S1  ratchet zero-headroom (protocols/) CANDIDATE     intake: ratchet headroom policy
S2  cloud-container uv 0.8.17          DISCHARGED    STANDING_RULINGS.md T-15 item (2) :2261+
CB  producer-pack prerequisites        CANDIDATE     intake: SDA-1 instrument (shared with CC, CE)
CC  corpus rotation (C-13)             CANDIDATE     intake: SDA-1 instrument -- amends ruling Q9
CD  served-id as admission precond.    DISCHARGED    STANDING_RULINGS.md Q9 :1882
CE  transport-health preflight         CANDIDATE     intake: SDA-1 instrument (shared with CB, CC)
CG  locate / re-commission SDA-1       DISCHARGED    docs/audits/2026-08-28-technical-sda1-
                                                     benchmark-design-adversarial.md (1a09124)
CA  [#577] byte-cap test               OWNED         [#577] -- IN FLIGHT TONIGHT AS LANE F (N7)
CF  **Shape:** ambiguity               OWNED         [#591] + frozen N8 -- IN FLIGHT AS LANE G (N8)
CH  tile manifest for rotation         CANDIDATE     intake #59 (joins; AC5 is the nearest clause)
CI  664+ anchored-by-mention WARNs     DISCHARGED    ecosystem/disposition-register.yaml:609

TALLY   OWNED 2  |  DISCHARGED 4  |  CANDIDATE 5  |  REJECTED 0        (n = 11)
```

---

## 2. Row by row, with the candidate's own words

### S1 · ratchet zero-headroom on `protocols/` — **CANDIDATE**

> *"**CANDIDATE — ratchet zero-headroom freeze on `protocols/`** (the 7a FLAG; raw finding). This batch is fresh evidence rather than a restatement: **two** lanes (L1, L5) had to author around a baseline with zero headroom, and L5's own contract asserted the constraint did not apply to it."* — packet:197–200

**Not OWNED, and I checked before saying so.** The nearest open row is `[#447]` (`tasks/447-ratchet-raise-local-hook-bootstrap-deadlock.md`), whose leg (1) is *"`pre-commit install` arms from the config at install time, so a commit **raising** a threshold is judged by the value it replaces"*. That owns the **mechanics of raising a threshold**, not the **freeze that zero headroom imposes on normative authoring**. `[#357]` (silent-rule census run 2) completes the ADR-corpus denominator and would move the number, but its Done-when is a measurement, not a policy. `[#609]` is the **ruff** ratchet, a different organ.

**Not DISCHARGED, and the register says so in its own words.** `protocols/STANDING_RULINGS.md:1974` (S-1 · R12) excludes `STANDING_RULINGS.md` itself from the silent-rule corpus, and states its own limit: *"the exclusion removes only 2 token occurrences at the 2026-08-24 measurement. It is a correctness fix to what the metric MEANS, **not a headroom fix** — the headroom came from the R8 raise."*

**The constraint is real and mechanical.** `scripts/silent_rule_detector.py:130-134`:

```
_SCOPE_RULES = (
    ("protocols", False, (".md",)),
    ("templates", True, (".md", ".tmpl")),
    ("ecosystem", False, (".yaml",)),
)
```

and `ecosystem/silent-rule-baseline.yaml:20-21` — `detector_id: silent-rule-v5`, `baseline: 443`, with `:27` recording *"RAISE 441 -> 443 … set by the integrator 2026-08-24"*. Batch-1 measured live 443 against baseline 443 twice (packet:24 and packet:151-157) — headroom **0**.

**Draft intake one-liner:** *"A silent-rule baseline at zero headroom converts any normative sentence added to `protocols/*.md` or `ecosystem/*.yaml` into a blocked commit; rule which of three forms applies — per-arc authorized raise, scope narrowing, or an accepted freeze with a declared destination for new normative prose — given that S-1 forecloses the correctness-fix route."*

### S2 · cloud-container `uv` 0.8.17 — **DISCHARGED**

> *"**CANDIDATE — cloud-container `uv` 0.8.17 against the pin `==0.11.19`**, under which hub gates are silently unrunnable on the Dispatch-Cloud rung (sol session, measured). This is what made every lane in this batch route LOCAL."* — packet:201–203

**Locator 1 — ruled.** `protocols/STANDING_RULINGS.md` **T-15** (heading at `:2261`, *"`[#453]` Cloud night-run runbook — the three container gaps"*), item (2), verbatim: *"**The `uv` pin** is manual, because the container ships what it ships and `uv self update` demonstrably cannot reach the pinned version. A preflight could only report a mismatch the ADR-106 declaration already predicts."* The section's own footer reads **"Row status: CLOSED by this section. Expiry: open-ended."**

**Locator 2 — the consequence is already the routing rule.** `protocols/PLAYBOOK.md:2308`, Ch8 Layer-1 **Q1**: *"Does the result depend on a gate…? **NOT cloud** — measured: no hook armed there, unpinned `uv`, no `click`."* Every lane routing LOCAL is this rule working, not a new finding.

`[#453]` itself (`tasks/453-…`) is `status: closed` and quotes the same measurement — *"the container shipped uv 0.8.17 against the ADR-106 `==0.11.19` pin"* — so it cannot be an OWNED row, and T-15 is what closed it.

**Evidence attached rather than re-filed, and it is a conflict:** T-15 says the gap is unfixable (`uv self update` cannot reach the pin); PLAYBOOK:2308 says, measured 2026-08-26, the container is *"pinned-but-WRONG … **and provisionable in one step**, after which `uv run --locked` gates ran clean — an amendment candidate, routing unchanged pending a ruling (`docs/audits/2026-08-26-technical-handoff-census.md`, Appendix B)"* (artifact present, 23,156 B). The two live locators disagree on remediability while agreeing on the routing. That pending amendment is already registered with its own evidence pointer, so it births nothing here — see §3.

### C-B · producer-pack prerequisites — **CANDIDATE**

> *"**C-B** producer-pack prerequisites (C-1 rejection-tax cost model, C-6 adversarial suite, C-15 load-bearing list)."* — packet:207–208

The three cited items now exist in-repo, and I read them: `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md:256` (C-1, CRITICAL, *"The producer verdict measures the wrong quantity"*), `:305` (C-6), `:372` (C-15, *"The design does not state who may weaken it"*). §10 of that artifact sequences them: *"Build the producer pack only after C-1's cost model and C-6's adversarial suite exist."*

**Why this is not DISCHARGED by that artifact.** ADR-100 §4, quoted inside ADR-111:13 lines 28–30 — *"**Audit = evidence about state. Intake = a request to change state.** They are **separate genres with separate lifecycles.**"* The SDA-1 file's own status line reads *"DESIGN + CRITIQUE. Nothing here admits or refuses a provider."* A recommendation in a landed audit is evidence, not a ruling. **No open row owns SDA-1's execution** — `grep -l 'SDA-1' tasks/*.md` returns nothing; `[#578]` owns the one earned rerun of the **C1** pack, not this instrument.

**Draft intake one-liner:** *"Ratify (or refuse) SDA-1's §10 sequencing — no producer pack before C-1's rejection-tax cost model and C-6's adversarial suite — and make C-15's three load-bearing items droppable only by recorded ruling with its cost stated."*

### C-C · corpus rotation — **CANDIDATE**

> *"**C-C** corpus rotation (C-13) — ground truth never committed alongside the items."* — packet:209

**Half of it is built, and the artifact says so.** `…sda1-benchmark-design-adversarial.md:358` (C-13) ends: *"keep answer keys outside the tree — **the no-pack sandbox already enforces the last part and is the right precedent**."* `scripts/nopack_sandbox.py` exists; `[#562]` closed 2026-08-23 on *"11/11 probe vectors … a deliberate read of the pack path FAILS."*

**The rotation half is a standing-ruling amendment, which is why it needs a decision and not a row.** `protocols/STANDING_RULINGS.md:1882` (Q9) pins admission to a **named file**: *"ADMIT holds exactly when G1 ∧ G2 ∧ G3 hold on the seeded-defect pack (`docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`)"*. C-13's fix — *"split the fan-out pack into a **carried half** … and a **fresh half** … Rotate one third of every pack per round"* — changes what Q9 names. `[#578]`'s Done-when re-runs *"all 14 pack items plus `C1-N3`"*: the same pack, no fresh half. Nothing open covers rotation.

**Draft intake one-liner:** *"Amend Q9 to require a fresh, never-committed half for admission while reporting the carried half separately for commensurability — or record that commensurability outranks leakage and Q9 stands."*

### C-D · served-id as an admission precondition — **DISCHARGED**

> *"**C-D** **served-id reporting as an admission precondition.** A transport that cannot report which model served a round hits C-9's ceiling, so it decides whether a provider is evaluable at all. Measure it at admission, not at pack time."* — packet:210–212

**Locator: `protocols/STANDING_RULINGS.md:1882`, ruling Q9**, verbatim: *"…and **a version/substitution probe is a hard precondition, carried as a P-item, so a client that silently substitutes a sibling model stops the run before any gate is computed**."* "Before any gate is computed" **is** "at admission, not at pack time" — the rule the candidate asks for is already ruled, and it is already being applied: `ecosystem/provider-registry.yaml:245-246` refuses to register a DeepSeek model id because *"standing ruling Q9 makes the substitution probe a hard precondition"*, and `:221` refuses `cursor-agent` because *"an undisclosed model is an UNREPRODUCIBLE RESULT"*.

**Evidence attached, nothing born.** Batch-1's L3 measurement — *"the `agy` JSON envelope carries conversation_id, status, response, duration_seconds, num_turns and usage — and **no model identifier of any kind**"* (packet:70-73) — is a Q9 **failure witness on the one live transport**. Its carrier rows are named at `STANDING_RULINGS.md:1900` (*"Q9 → `[#562]`, `[#568]`"*); `[#562]` is closed, so the evidence attaches to **`[#568]`**, open, whose forcing evidence is already *"a silently substituted model id … turning out to be the thing that decided a run."*

### C-E · a transport-health preflight that does not trust exit codes — **CANDIDATE**

> *"**C-E** **a transport-health preflight that does not trust exit codes.** The GLM witness: an HTML file on PATH exiting 0."* — packet:213–214

The witness is packet:66 — *"**BROKEN — the file on PATH is HTML** (`<!DOCTYPE html>`), a failed download that **exits rc=0** while erroring. Worse than absent: a harness testing callability by exit code reads it as healthy."*

**Nothing owns it.** `ecosystem/provider-registry.yaml` records transport health as **hand-written measured prose** per provider (e.g. `:127`, the gemini binary that *"prints `0.56.0` at exit 0"* while its served route is dead) — a register, not a probe. `grep -l 'exit 0\|exit code\|on PATH\|fail-open' tasks/*.md` returns six rows, none of which owns provider transports: `[#504]` is one gate's docstring, `[#593]` is the Codespaces image, `[#438]` names the general asymmetry (*"a **fail-open passes every test and enforces nothing**"*) but its Done-when is a PLAYBOOK rule about **review placement**, not a probe.

**Draft intake one-liner:** *"A provider transport is healthy only when a probe asserts the artifact's identity (it is an executable that answers), never when it exits 0 — decide whether that preflight lands as an extension of the SessionStart provider probe or as a precondition inside the admission instrument."*

### C-G · locate or re-commission SDA-1 — **DISCHARGED**

> *"**C-G** **locate or re-commission SDA-1.** The contract treats it as existing and as L3's frame. Either it is unreachable from this host and needs a locator recorded, or it was never produced and the contract's basis clause is unfounded."* — packet:215–217

**Resolving locator: `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md`**, added by `1a09124`, merged at `3e52a2f` — *"Merge branch worktree-sda1-persist — SDA-1 persisted verbatim"*. I read it: 16 (provider, role) pairs, seven Q0–Q7 preconditions at §2, a 15-item severity tally at §9, a verdict at §10.

**The timing matters and is measured, not inferred.** The packet landed at `da16da7`, **2026-08-28 20:13:09 +0200**; SDA-1 landed at `3e52a2f`, **21:40:33 +0200**. C-G was **true when written and was discharged 87 minutes later** by the persistence lane. The artifact's own provenance block answers the disjunction the candidate posed: it was produced (cloud session `session_01QQyPrCbEcqJaDLLLjNhnKT`) and was *"unreachable from the hub"* — the first branch, now closed by transcription.

### C-A · `[#577]`'s byte-cap test — **OWNED, IN FLIGHT TONIGHT AS LANE F**

> *"**C-A** `[#577]`'s byte-cap test (L1, corroborated by terra) — `[#577]` does not fully discharge without it."* — packet:221–222

**Row: `[#577]`** (`tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md`, `status: open`). Covering clause, quoted from its Done-when: *"**the combined global+root payload is asserted in bytes against the 32 KiB cap by a test**"*. The packet reached the same verdict at :30 — *"**`[#577]` is not fully discharged**"*.

**In flight as lane F (architect's N7)**, contract at `docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-LANE-F-577-byte-cap.md`: *"### N7 — CANDIDATE C-A: the [#577] byte-cap test — S"*, write-scope `tests/`, Done item (3) *"`[#577]`'s done-when fully discharged"*.

**A lane in flight has discharged nothing.** Recorded because the contract itself found the packet's figure false: *"The 9,161 B figure the contract's Intent restates is **FALSE** against the landed tree"* — measured 9,430 B / 28.78 %, with `git cat-file -s 43c18e9f:AGENTS.md == 5539`. Whether lane F lands is **MEASUREMENT-OWED-LOCAL**.

### C-F · `**Shape:**` ambiguity — **OWNED, IN FLIGHT TONIGHT AS LANE G**

> *"**C-F** `**Shape:**` is ambiguous between substrate-shape and batch-shape (D3). A hand-authored contract has no way to know the token is reserved by a gate."* — packet:223–224

**Row: `[#591]`** (`tasks/591-substrate-validator-layer-2-refuse-a-contract-wh.md`, `status: open`). Covering clause: *"A contract declares a substrate and nothing checks the declaration against what the contract then asks for. This is the REFUSE layer."*

**Stated precisely, because the row alone would be an over-claim:** `[#591]`'s four ex-ante Done-when legs do not name `**Shape:**`. The clause that names C-F by its label is in tonight's **frozen N8 contract**, which extends that row — `NB2-LANE-G-591-preflight-predicates.md`: *"the live `**Shape:**`→'one' mis-parse (**finding C-F**) is fixed in the same organ … (v) the C-F defect fixed — `**Shape:**` prose no longer parses as a substrate declaration, regression test included."* The organ is `scripts/validate_substrate.py`. So: OWNED by `[#591]` **as extended by the frozen N8 contract**, in flight tonight as lane G. **Discharged: nothing yet.**

### C-H · a declared tile manifest for journal rotation — **CANDIDATE**

> *"**C-H** a declared **tile manifest** for journal rotation (L2 HIGH-1) — a deleted legacy tile is undetectable without one, shrinking the anchoring universe into a false gap."* — packet:225–226

**Not OWNED, and `[#608]` excludes it in its own words.** `tasks/608-…` (`status: open`) is *"the seam ONLY — it moves **zero bytes**, creates no legacy file, and needs no governance act"*; its Done-when is byte-identity plus a shared predicate, with no manifest. `[#608]` is the **only** row citing intake #59 (`grep -l 'intake #59' tasks/*.md`); `[#589]`/`[#590]` are intake #49's other halves and neither reads the journal.

**Nearest live clause, quoted so the delta is visible.** `docs/intake/2026-08-27-tech-append-only-rotation-execution.md` (`status: READY`), acceptance criterion 5: *"The splitter produces an archival whose concatenation is byte-identical to the pre-split blob, and **enumerates the tiling (no gap, no overlap, strict date order) rather than asserting it**."* That enumerates **at split time**; C-H asks for a **durable** record so a tile deleted *afterwards* is detectable. The fork — construction-time check versus committed manifest — is unruled.

**Draft intake one-liner (joins intake #59 rather than starting a new one):** *"Extend intake #59 AC5 from a split-time enumeration to a committed tile manifest that `journal_anchor.journal_text()` validates on read, so a later-deleted `JOURNAL-legacy-*.md` FAILs instead of silently shrinking the anchoring universe."*

### C-I · the 664+ "anchored by mention" WARNs — **DISCHARGED**

> *"**C-I** `journal_spine_anchor`'s **664+ "anchored by mention, not by record"** WARNs — the advisory backlog this batch's own entries were deliberately written against, each carrying an explicit `Anchors:` line."* — packet:227–229

**Resolving locator: `ecosystem/disposition-register.yaml:609`**, id `warn-journal-spine-anchored-by-mention`, `organ: journal_spine_anchor`, `match: "anchored by mention, not by record"`, `review_date: 2026-11-14`. Its `reason`, verbatim: *"**ADVISORY BY DESIGN, and structurally unfixable in bulk** … JOURNAL.md is append-only (CLAUDE.md section 5 rule 2), so that backlog … is not retro-fixable without the edit the append-only rule forbids. The HARD leg (block_unanchored_push) is unaffected and passes on every push."* The `ref:` field records that `[#524]` (leg c, the WARN's builder) closed 2026-08-15 at `62f42dad` and is retained as **provenance, not a live owner** — so there is no open row to claim, and the ruling is the discharge.

**Evidence attached to that register entry, and it is the one thing worth an operator's eye:** the entry's own reason says the WARN *"currently names **401** commits"*; the packet reports **664+**. That is **+263 against an entry whose premise is that the mass is historical and "the convention holds going forward."** The entry carries a `review_date` of 2026-11-14, which is the right place for it — the delta is attached as evidence for that review, not re-filed as a candidate. The live count is **MEASUREMENT-OWED-LOCAL** (it needs `audit.py`); both numbers here are quoted from their sources, neither is mine.

---

## 3. Surfaced while triaging — NOT one of the eleven, and not counted in the tally

**(i) The packet's own candidate set is internally inconsistent: C-J is orphaned.** `grep -o 'C-[A-J]'` over the packet returns C-A…C-J, but **C-J occurs exactly once, at line 311, inside §10** — *"Filed as candidate C-J"* (the skip-impersonating-a-pass finding: `test_live_report_renders_the_real_fleet` SKIPPED at baseline on a missing pandas and FAILED on the merged tree). **§6, the filing wave, does not list it.** So the packet declares a candidate in one section and omits it from the section that enumerates candidates. The brief's "exactly 11" matches §6 and is correct as scoped; C-J is a twelfth filed candidate with no row on any sheet. Its nearest ruling is already named in the packet's own sentence — Z-G4, *"a skip is indistinguishable from a pass in every summary line anyone reads"* — which makes it a strong DISCHARGE candidate, but **dispositioning it is outside this lane's frozen input** and I am reporting it rather than deciding it.

**(ii) T-15 and PLAYBOOK Q1 disagree about whether the cloud `uv` gap is fixable** (see S2). Not a new candidate — PLAYBOOK:2308 already carries it as *"an amendment candidate, routing unchanged pending a ruling"* with its evidence artifact named. Filing it again would be the `[#453]` re-derivation class ADR-111 exists to stop.

---

## 4. MEASUREMENT-OWED-LOCAL

Every one of these needs a gate, a hook, `scripts/audit.py`, or the pytest suite, and none can start in this container:

```
1. live silent_rule_ratchet count vs baseline 443 (S1's "zero headroom", today)
2. live journal_spine_anchor WARN count (the 664+ vs the register's recorded 401)
3. whether lane F lands green, and with it [#577]'s full discharge (C-A)
4. whether lane G lands green, and with it the **Shape:** regression test (C-F)
5. audit.py health on the current head fcc9485
```

---

## 5. SELF-AUDIT — read this heading

**CANDIDATE is the largest single bucket of this pass: 5 of 11.** ADR-111 §2 (`docs/decisions/ADR-111-finding-triage-pipeline.md:68`) states the standard: *"a triage pass that routes **most** items to (c) has not triaged."*

**Stated precisely rather than favourably:** 5 of 11 is a **plurality, not a majority** — 6 of 11 land on OWNED or DISCHARGED, so this pass does not route *most* items to (c). But (c) is the biggest bucket, the brief asked me to flag exactly that, and here is why each of the five genuinely needed a decision rather than a row or a locator:

1. **S1 (ratchet headroom)** — the fix has at least three incompatible forms (authorized per-arc raise / scope narrowing / accepted freeze with a declared destination), and S-1 **forecloses** the cheap one in its own text (*"not a headroom fix"*). `[#447]` owns the raise mechanism, not the freeze. A row cannot pick between three policies.
2. **C-B (producer-pack prerequisites)** — the content is fully drafted inside a landed audit, and ADR-100 §4 says an audit decides nothing. Ratifying §10's sequencing is a decision no open row holds.
3. **C-C (corpus rotation)** — the fix **amends standing ruling Q9**, which names a specific pack file as the admission corpus. Amending a standing ruling is not a row's act.
4. **C-E (transport-health preflight)** — a new organ with a real siting fork (SessionStart provider probe vs. admission-instrument precondition), against a register that currently records transport health as hand-written prose.
5. **C-H (tile manifest)** — a design fork (durable manifest vs. split-time enumeration) inside a READY intake whose one born row explicitly excludes it.

**The five do not become five intakes.** C-B, C-C and C-E are all preconditions on the same instrument and route to **one** intake (the SDA-1 admission instrument); C-H **joins** the existing intake #59 rather than opening one. So the pass proposes at most **three** intake acts — one new (S1's ratchet policy), one new (the SDA-1 instrument, carrying three candidates), one amendment to an existing READY intake.

**REJECTED is zero, and I am not going to manufacture one.** None of the eleven is a finding I can decline on a recorded reason: two are in flight tonight, four resolve against live rulings or a landed artifact, and five need a decision I do not have the authority to make.

**One more way this output could have looked complete while failing, checked against myself:** claiming OWNED for `[#591]` on the strength of the row alone. `[#591]`'s four ex-ante Done-when legs never name `**Shape:**` — only tonight's frozen N8 contract does. I recorded the row **as extended by the contract** rather than letting the row id carry a clause it does not contain, because that over-claim is exactly the class the packet's own D2 (a contract citing `[#587]` for `[#608]`'s work) cost batch-1 a repair arc to catch.