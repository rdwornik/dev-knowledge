# NB2 · wave 2 · lane J — FM-3, the visible shrinkage — hand-back packet

**Lane:** J (FM-3) · **Branch:** `worktree-lane-j-3-fm-visible-shrinkage` · **Substrate:** local
**Contract:** `docs/audits/2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-J-FM3-shrinkage.md`
(frozen bundle `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-3)
**Branch point:** `77096131` — the wave-2 GO merge. **Date:** 2026-08-29.

---

## 0. THE EX-ANTE, VERBATIM, THEN MEASURED

The contract's own Ex-ante line, quoted from the OPERATOR RULING CARRIED section:

> **Your Ex-ante, restated against what is now true:** `docs/intake/*.md` **56 → 54** and
> `docs/intake/archive/` **8 → 10**, both md5-proven. `docs/decisions/*.md` stays **89** — no ADR is
> superseded-and-unarchived, and ADR immutability plus ADR-100 mean there is nothing lawful to move
> there. Say that plainly rather than leaving the decisions count looking like a miss.

Measured on the live merged tree, before and after, by re-count rather than by inheritance:

```
surface                     before   after   ex-ante   verdict
docs/intake/*.md              56       54      56->54   MET
docs/intake/archive/*.md       8       10       8->10   MET
docs/decisions/*.md (top)     89       89          89   MET (stays, by authority — see D-1)
docs/decisions/archive/        2        2           -   untouched
```

The original contract-body Ex-ante — *"docs/intake and docs/decisions counts DROP"* — is **MET on
intake and NOT MECHANICALLY ACHIEVABLE on decisions**, exactly as the late addendum predicted.
Stated plainly rather than left looking like a miss: **no ADR is lawfully movable tonight.**
ADR immutability (`CLAUDE.md` §5 rule 3) and ADR-100 §1 protect all 88 ADRs plus the README;
`docs/decisions/archive/` already holds the two that were lawfully moved before tonight. Nothing
was manufactured to make the number move.

---

## 1. PER-DONE-ITEM — MET / NOT-MET / PARTIAL, each with a witness

### D-1 · Staleness guard built FIRST, as a function, run over the whole predicate — **MET**

The contract's first requirement was that the guard be a function gating the relocation, not a
disclaimer. It was written before any file was touched and run over `docs/intake/README.md`'s
archival predicate as a whole, not over FM-C's worklist. FM-C censused `fcc9485`; this lane
recomputed on `77096131`, after seven wave-1 lanes landed.

**FM-C's numbers beside this lane's own, as the contract asked:**

```
                                FM-C @ fcc9485        lane J @ 77096131 (live)
docs/intake/ depth 1            57 objects            56 *.md
  status split                  SEED 10 · DRAFT 7     SEED 9 · DRAFT 7
                                READY 19 · ACC 19     READY 19 · ACCEPTED 18 · CONSUMED 2
docs/intake/archive/            8 (all terminal)      8: CONSUMED 6 · SUPERSEDED 1 · REJECTED 1
docs/decisions/ top level       89                    89
CONSUMED-AND-ARCHIVABLE         0                     2   <-- the GO's flips created the worklist
```

**Discrepancy found and reported rather than smoothed over.** The wave-2 GO states the repaired
index reads *"SEED 10 · DRAFT 7 · READY 19 · ACCEPTED 19"*. On the live tree it read
**SEED 9 · ACCEPTED 18 · CONSUMED 2** — the GO quoted the index as it stood **before its own two
status flips**, which moved #19 out of SEED and #26 out of ACCEPTED. Both readings are internally
consistent and neither is a defect; the GO's figure is simply pre-flip. Named here so the
integrator does not chase a phantom regression.

The four predicate legs, run per candidate:

```
LEG 1  terminal-at-depth-1 (== the worklist)  -> exactly {#19, #26}
LEG 2  reverse mis-filing (non-terminal in archive/) -> none
LEG 3  per-candidate, against the LIVE tree:
         #19  object present at census path       PASS
              status CONSUMED (terminal)          PASS
              consumer ADR-82 exists, Accepted    PASS
              row [#446] CLOSED 2026-07-31        PASS   -> RELOCATE
         #26  object present at census path       PASS
              status CONSUMED (terminal)          PASS
              consumer ADR-110 exists, Accepted   PASS
              row [#505] status: closed           PASS   -> RELOCATE
LEG 4  born-tonight: git diff fcc9485..HEAD -- docs/intake
         -> ten M's, ZERO A's. No new intake and no new consumer was born tonight.
```

**RED → GREEN witness for the predicate itself** (the guard is the deliverable, so the failing
witness comes first, per the batch's RED-first clause):

```
before the move   LEG 1 -> 2026-07-27-func-...-handoff-reform.md, 2026-08-06-func-parallel-...
                          (the predicate's own violation: terminal docs sitting at depth 1)
after the move    LEG 1 -> (none)
                  archive/ CONSUMED 6 -> 8
```

### D-2 · #28 not touched; #42 not revisited — **MET**

The guard reached neither by construction, which is the strongest form of compliance available:
**#28 is `status: ACCEPTED`, `disposition: active`, so it is not in the terminal set and LEG 1
never nominated it.** No special case was written for the operator's HELD ruling — the predicate
already agrees with it. `ADR-112:87` was opened and confirms the hold's premise: *"The fourteen
candidates in intake #28 §C become actionable"*. **#42** stays `DRAFT`, untouched, not revisited.

Both files are byte-unchanged: `git diff main...HEAD` names neither.

### D-3 · Two relocations, byte-identical, md5-proven, `git mv`, zero deletion, zero content edit — **MET**

```
md5 before                          md5 after                           bytes  object
20f954913b0afa61043843866e19be97 -> 20f954913b0afa61043843866e19be97     6342  intake #19
752cce5fe6a02f4c419cc81197a8c707 -> 752cce5fe6a02f4c419cc81197a8c707     4474  intake #26
```

Proven a second, independent way at the git layer — the proof that cannot be faked by re-hashing
the same clipboard:

```
$ git diff --cached -M --stat
 docs/intake/{ => archive}/2026-07-27-func-operator-design-input-...md  | 0
 docs/intake/{ => archive}/2026-08-06-func-parallel-execution-system.md | 0
 2 files changed, 0 insertions(+), 0 deletions(-)

commit a5f71b1f: rename ... (100%)   x2
```

Moved with `git mv`, so history follows. **ZERO deletions. ZERO content edits** — not a heading,
not a status line, not a frontmatter key. The `SEED → CONSUMED` and `ACCEPTED → CONSUMED` flips
were the operator's act on `main` before this lane booted and were **not redone here**; both files'
`status:` read `CONSUMED` when opened, so the stop-and-report condition did not fire.
**ADR-94's in-place status-line exception is not exercised by this lane** — archiving is a move.

### D-4 · Generated surfaces: only what two gates forced, named — **MET**

The contract permits regenerating what a lane's own commit needs to be legal, in exchange for
naming it. Two were forced; both ride commit `a5f71b1f` because the gates refuse the commit
otherwise, and both are named here:

| surface | gate that forced it | diff |
|---|---|---|
| `docs/intake/README.md` Contents block | `intake-index-freshness` pre-commit hook | 1 insertion / 6 deletions inside the generated block; **55 → 53 documents**; the `CONSUMED (2)` group drops out of the depth-1 scan, as the README says archived docs do |
| `docs/intake/manifest.json` | `audit.py::check_intake_tree_coherence` — FAILed with *"item node(s) with no intake doc on disk"* → `health: DEGRADED` → commit blocked | regenerated by `gen_intake_tree.py --write`, 53 item nodes |

The manifest is the trap `MEMORY` records as *"intake add needs TWO generators"*, and it fired
here on a **removal**: the index generator is hooked, the tree generator is not, so the first
commit attempt was refused by `audit-health` rather than by the index hook. Witnessed, not
theorised — the blocked attempt is in this session's transcript.

**Nothing else was regenerated.** `BACKLOG.md`, `docs/audits/README.md`, `ecosystem/doc-counts.md`,
`ecosystem/organ-index.md` and `.claude/generated/*` are left for the integrator's single pass. In
particular this lane deliberately left `docs/audits/README.md` stale for its own packet — per
[#590], a batch lane must not regenerate the audits index.

### D-5 · Shrinkage axis 2 — `tasks/` row bodies through lane D's landed mechanism — **MET, with the measurement reported honestly**

Executed through `scripts/archive_row_body.py` ([#612], merged at `43c94846`). **No second
mechanism was built**; the script is byte-unchanged by this lane.

```
$ uv run --locked python scripts/archive_row_body.py relocate --id "169,188,298,535"
  [#169]  1123 -> 625 chars, 1 clause(s) relocated
  [#188]   856 -> 559 chars, 1 clause(s) relocated
  [#298]   886 -> 819 chars, 1 clause(s) relocated
  [#535]  1309 -> 1259 chars, 1 clause(s) relocated
                    4174 -> 3262 chars of live row body, -912
```

Byte-identity proven by the mechanism's own verifier rather than asserted by this lane — LEG C
re-splices the stored clauses into the live row and asserts the recorded pre-relocation digest:

```
before  archive_row_body: OK - 20 record(s), 20 byte-identity PROVEN (legs A/B/C/D/E)
after   archive_row_body: OK - 24 record(s), 24 byte-identity PROVEN (legs A/B/C/D/E)
```

No row closed, no row deleted, no byte rewritten. LF verified on every touched file
(`file` reports UTF-8 with no CRLF terminators; terra's independent probe: `CRLF: False`, `CR: 0`).

**The measurement the contract asked for, and it does not flatter the lane:**

```
validate_doc_rot   before 59 loci   after 59 loci   -- NO CHANGE
```

It was never going to move: **none of these four rows is a doc-rot locus.** Each is already under
the 1320-char ceiling and carries no accretion finding, which is precisely why lane D left them and
filed them as its C-1. What did move is the mechanism's reachable set:

```
$ uv run --locked python scripts/archive_row_body.py propose
  archive_row_body: no row carries a relocatable dated-amendment run
```

**Zero.** Lane D's drain is now exhausted against the live corpus. See C-2 for what that implies
about the residual 59.

**Why this lane executed C-1 at all, since lane D called it "an integrator call, not an
executor's":** the wave-2 addendum answered that call explicitly — *"Lane D's exclusive `tasks/`
ownership ended when it STOPped; your contract's write-scope names row-body pointers explicitly"* —
and the addendum was authored after lane D merged. No generated surface was needed:
`gen_task_tree.py --emit-source` reports *"BACKLOG.md already current (206 task(s))"*, because the
[#589] view renders one line per row and row bodies do not appear in it.

### D-6 · Re-run `check_funnel_lifecycle` and show it GREEN on main afterwards — **NOT MET, by dispatch condition, not by execution**

**The gate does not exist on any tree.** The contract's header says *"Runs AFTER FM-2 merges — you
execute under the new gate, not beside it"* and its addendum §4 says *"lane I's, merged before
you"*. Neither is true. Witnesses:

```
$ grep -rn "funnel_lifecycle" scripts/                 -> no match
$ git log --oneline -3 worktree-lane-i-2-fm-funnel-lifecycle-check
  77096131 Merge branch 'docs/batch-2-w2-preflight' ...   <-- identical to this lane's branch point
```

Lane I has committed nothing; its branch sits at the shared wave-2 GO merge. **This lane ran
beside FM-2, not after it.** No attempt was made to build the check — the contract's *"No new
check code"* clause binds, and a lane inventing the gate it is supposed to be measured by is the
worst available outcome.

**What is delivered instead is the thing the gate would consume**, per the addendum's own fallback:
*"If it is GREEN because there is genuinely nothing to reap, say that — a gate that is green on an
empty set is only worth something when the emptiness has been proven, and §1 is that proof."*
§1 (D-1 above) is that proof, and it is now stronger than when the addendum was written: the
terminal-at-depth-1 set is empty **because two members were reaped tonight**, not because it was
never populated. The reverse leg is also proven empty — no non-terminal doc sits in `archive/`.

The nearest live surface was run for a real verdict rather than left blank:

```
$ audit.check_funnel_coverage(.)
  pass | 78 of 787 artifact(s) in docs/audits/ carry a ruled disposition with a locator,
         2 are PENDING, and no undispositioned artifact is outside the arm-time baseline of 707
```

**Owner: the integrator.** Re-run `check_funnel_lifecycle` on the merged result once lane I lands.
Its expected verdict against this lane's contribution is GREEN-on-a-proven-empty-set.

### D-7 · The RULING REQUEST as a deliverable — **MET, and materially changed by the GO**

The addendum asked for a decision-ready ruling request on intakes #19 / #26 / #28. **The operator
ruled all three in the wave-2 GO before this lane booted**, so that specific request is discharged
by execution, not by asking. Restating it would waste an operator touch. What follows is the
**residual** request — what tonight's execution left genuinely undecided, in the operator's terms.

**RR-1 — intake #28 has no recorded un-park condition.**
`docs/intake/README.md` §5 requires a `deferred` disposition to carry a `trigger:` or
`review-date:` so *"the un-park condition is part of the record, not tribal memory."* #28 is
`disposition: active`, so that requirement does not bind it — and the result is that #28 is HELD
by a ruling whose release condition exists only in `ADR-112:87` ("the fourteen §C candidates
become actionable") and in the GO text, not in the document's own frontmatter. **Cost of leaving
it:** the next archival pass re-derives the hold from prose every time, which is exactly the
tribal-memory failure the README's rule was written against. **Cost of fixing it:** one frontmatter
line on a live document — an operator/architect act, not a lane's.
**The one line the operator would have to say:** *"#28 stays ACCEPTED; record its release condition
as the discharge of ADR-112 §C's fourteen candidates."*

**RR-2 — the next archival cohort is measurable, and it is one document.**
This lane sized what the predicate will produce next, so the operator is ruling on a number rather
than on a feeling. Of the 18 live ACCEPTED intakes at depth 1, exactly **one** cites only closed
rows: **intake #18** (`disposition: active`, cites `[#435]`, CLOSED). Every other ACCEPTED intake
either cites at least one open row (#20, #28, #30, #38, #39) or cites no row at all (12 documents,
which the predicate cannot reason about — see C-3). **The honest reading:** the archival predicate
has a backlog of roughly one document per wave, so the shrinkage it produces is real but slow, and
tonight's 56 → 54 is close to its natural rate, not a one-off.
**The one line the operator would have to say, if they want the next unit of shrinkage:**
*"intake #18: ACCEPTED → CONSUMED, consumed-by ADR-82 / [#435] closed."*
This lane does **not** propose that flip and did not touch #18. It is named because the addendum
asked for what "decision-ready" means here, and a cohort of one, measured, is decision-ready.

---

## 2. COMMIT SHAs, IN ORDER

```
a5f71b1f  docs(intake): archive intakes #19 and #26 byte-identically — the wave-2 GO's
          ruled relocation
          4 files changed, 6 insertions(+), 44 deletions(-); 2 renames at 100%

ee01a2c1  docs(tasks): drain the last four relocatable row bodies — lane D's mechanism
          reaches zero
          8 files changed, 172 insertions(+), 4 deletions(-)

<this packet>  docs(audits): lane J hand-back packet — FM-3, the visible shrinkage
```

Branch: `worktree-lane-j-3-fm-visible-shrinkage`. **Not merged, not pushed, no JOURNAL entry.**

---

## 3. TERRA TALLY — reviewer pre-merge, tally in body

`codex exec --model gpt-5.6-terra` over this lane's own diff (`git diff main...HEAD`, 349 lines),
**not** `/codex-review` — a mixed doc/code diff kills that lane. Prompt named the four hard
prohibitions and asked for adversarial review of rename purity, row-body content loss, generated-
surface mechanicality and CRLF.

```
TALLY: Critical=0 High=0 Medium=0 Low=0
```

> *"No findings. The two intake documents are 100% similarity renames; row annotations are preserved
> in their corresponding archives with retained pointers; generated changes are mechanical; no
> prohibited paths or CRLF appear."*

The tally is trusted here because the reviewer showed its own work rather than only a verdict: it
enumerated the diff by line number and ran an independent line-ending probe
(`CRLF: False · LF: True · CR: 0 · LFCount: 349`). That probe is a second, independent witness for
the LF claim in D-5.

---

## 4. CANDIDATE FILINGS — REPORTED, NEVER FILED

**C-1 — `[#591]` predicate (iii) cannot distinguish a dispatch target from terminal-state evidence.**
Carried verbatim from this lane's own contract, which raised it about itself: the freeze predicates
flagged `[#446]` as *"resolves to a CLOSED row … a contract cannot dispatch work against it"*, when
`[#446]` was cited as **evidence that intake #19's only born row reached a terminal state** — the
very fact that made #19 archivable. **An archival contract is made almost entirely of the second
kind of citation.** This lane confirms the diagnosis empirically: both its candidates were qualified
by closed rows (`[#446]`, `[#505]`), and under predicate (iii) as written, a correct archival
contract cannot be frozen without tripping it. Suggested shape: distinguish an id in an imperative
clause from an id in an evidential clause. **Filed against `[#591]`. Nothing was opened, reopened or
closed** — `[#446]` and `[#505]` were read for state only.

**C-2 — lane D's drain is exhausted, and the residual 59 loci are structurally beyond its predicate.**
`propose` now returns zero rows while `validate_doc_rot` still reports 59. The gap is not backlog,
it is reach: 55 length findings sit on rows whose bulk is **structural** clauses (`Done when:` /
`refs` / `kill-candidates:` / `depends-on:` / `serialize-group:`), which `_STRUCTURAL_MARKERS`
refuses to move **by design and correctly** — relocating a `· DEFER` clause would silently flip a
deferred row to open. The 4 accretion findings (BACKLOG #82 #267 #276 #297) are the same story:
their dates live inside structural clauses. **So doc-rot cannot be driven below ~59 by relocation
at all**, and any further movement needs either a different mechanism or a re-pinned ceiling. This
is the decision lane D's C-3 anticipated; it is now measured rather than predicted.

**C-3 — 12 of 18 live ACCEPTED intakes cite no `[#id]` at all, so the archival predicate cannot
reason about them.** Ids 12, 13, 14, 16, 17, 24, 25, 27, 29, 31, 32, 33. Whatever consumed them is
recorded in prose (`note:` / `origin:`) or nowhere. **Consequence:** the cohort measurement in RR-2
can see only 6 of 18 documents, so "the next cohort is one document" is a floor, not a total. A
`consumed-by`/`decided-by` discipline on ACCEPTED docs would make the predicate complete; today it
is sound but partial, and this packet says which half it can see.

**C-4 — the wave-2 GO's quoted index counts are pre-flip.** See D-1. Not a defect in any artifact;
worth one line in the integrator's record so the next reader does not chase it.

---

## 5. BUDGET DECISIONS

**Ratchet — `protocols/` + `templates/` delta must be 0.**

```
$ uv run --locked python scripts/silent_rule_detector.py
before first commit   detector: silent-rule-v5   files: 61   count: 443
before last commit    detector: silent-rule-v5   files: 61   count: 443
                                                  DELTA: 0 files, 0 count
```

Measured, not assumed — the dispatch warned that wave-1 lane C held the batch's only authorization
and may have moved the 443. It did not; 443 is still the live figure at this branch point. This
lane **wrote nothing under `protocols/` or `templates/`** (`git diff main...HEAD --stat` names no
path under either), so the zero is structural, not lucky. The in-commit gate agrees:
`[OK] silent_rule_ratchet: live 443 <= baseline 443 under detector silent-rule-v5`.

**Decision budget.** Two judgment calls were made and both are named rather than buried:

1. **Executing lane D's C-1** (draining four sub-ceiling rows lane D deliberately left). Resolved
   in favour of executing, because the wave-2 addendum explicitly reassigned the axis to this lane
   after lane D stopped. Reported with the honest consequence that `validate_doc_rot` does not
   move (D-5).
2. **Not building `check_funnel_lifecycle`** when it turned out not to exist. Resolved in favour of
   reporting the dispatch-condition failure, because *"No new check code"* is in the contract's own
   WHAT THIS LANE DOES NOT DO section, and a lane that authors its own gate proves nothing (D-6).

**Not spent:** no `--no-verify`, no `SKIP=`, no bypass of any kind. Every commit passed the full
pre-commit set on its own merits, including the one that was correctly refused first.

---

## 6. DEVIATIONS, WITH OWNERS

**V-1 — dispatched beside FM-2, not after it. Owner: integrator.**
The contract is titled *"runs AFTER FM-2 merges"*; lane I had zero commits when this lane booted
(witness in D-6). Consequence: Ex-ante item *"check_funnel_lifecycle GREEN on main afterwards"* is
**NOT MET** and cannot be met from inside this lane. **Action for the integrator:** after lane I
merges, re-run `check_funnel_lifecycle` on the merged result. The proof of emptiness it needs is
D-1; nothing else is owed by this lane.

**V-2 — the original contract-body Ex-ante is half-unmeetable, by retention authority. Owner: none
— this is a correct outcome, recorded so it is not re-litigated.**
*"docs/intake and docs/decisions counts DROP"*: intake dropped 56 → 54; **decisions did not and
must not.** ADR immutability plus ADR-100 §1 (*"audit files are never physically moved, rolled up,
or compacted"*) leave nothing lawful to move. **No relocation was manufactured to satisfy the
number** — which the contract named as the one unacceptable outcome.

**V-3 — inherited suite RED, proven inherited rather than asserted. Owner: integrator (lane D's C-2).**

```
$ uv run --locked pytest <6 targeted modules> -q
  1 failed, 258 passed in 28.25s
FAILED tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings
```

The assertion demands **zero** `backlog-accretion` findings; the live corpus has four
(BACKLOG #82 #267 #276 #297). Proof it is not this lane's:

```
$ git merge-base --is-ancestor 128f5093 HEAD~1        -> true
    (the test's last edit predates this lane's branch point)
$ git log --oneline -1 -- <the four accretion rows>   -> 45ff9a74, lane D's own commit on main
```

None of the four is a row this lane touched; this lane's four rows are #169 #188 #298 #535. Lane D
declared this RED as its C-2 and named the fix as out of its write-scope; it is out of this lane's
too. **Not fixed here, and not silently absorbed.**

**V-4 — a first commit attempt was refused, and the refusal is reported as evidence.**
`audit.py::check_intake_tree_coherence` FAILed → `health: DEGRADED` → commit blocked, because
`docs/intake/manifest.json` had gone stale under the two moves and its generator is **not** hooked.
Resolved by regenerating the manifest into the same commit and naming it (D-4). Recorded because a
lane that only reports its successful commands has not reported its gates: this is a live gate
firing correctly on a real staleness, and it is the second generator that a removal — not just an
addition — makes stale.

**No JOURNAL entry written** (the integrator writes one anchor for the whole queue). **No
self-merge, no push, no row closed, no row filed.** The Stop hook's demand for a JOURNAL entry
naming these SHAs is **declined explicitly**: per ADR-85 amendment 2026-08-03 §A5 that hook is
advisory in full, the hard leg is `block-unanchored-push`, and a lane does not push.

---

**Branch `worktree-lane-j-3-fm-visible-shrinkage` · commits `a5f71b1f`, `ee01a2c1`, + this packet ·
gates green on its own diff · 1 inherited RED, proven inherited · terra 0/0/0/0 · STOP.**
