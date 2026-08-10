<!-- scope: meta -->
# Conformance-digest content census — what is actually inside the seven stranded branches, and a DRAFT triage

- **Class:** census (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** conformance-digest-content
- **Seat:** CC (Opus 5), lane D `digest-absorb-prep`, worktree branch `worktree-digest-absorb-prep`
- **Posture:** **READ-ONLY except this report.** No branch merged, checked out, touched, deleted or
  proposed for deletion. No finding fixed. No row, intake or ADR edited. No JOURNAL entry (lane rule).
  The only other file this commit carries is the regenerated `docs/audits/README.md`, which the
  `audit-index-freshness` pre-commit gate requires whenever a `docs/audits/*.md` is added.
- **Filename pre-verified** against `validate_hermetization.classify()` → `None` (no block);
  `census` is in `AUDIT_CLASS_ENUM`.

## What this lane deepens, and what it does not repeat

`docs/audits/2026-08-10-technical-origin-branch-census.md` established the set at **branch** level.
`docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md` §2 established the
**verdict** (BROKEN, not deliberate), named the missing step, and proved it a recurrence of `[#419]`.
Neither is re-derived here. This lane reads the branch **contents** — the thing no one has read — and
drafts the triage the consumption act will need.

**Two corrections to the prior census, recorded here rather than by editing an immutable artifact:**

1. It reports *"`main` carries **19** `*-conformance-nightly-digest.md` files"*. The live count is
   **15**. Evidence: `git ls-tree --name-only origin/main docs/audits/ | grep -c "conformance-nightly-digest"` → `15`.
   Nothing turns on the delta — the newest is still `2026-08-02` and every claim built on that stands.
2. Its table lists **six** conformance branches; there are now **seven**. `claude/conformance-2026-08-10`
   was pushed at 09:55:44 UTC **the same morning that census was written** — the set grew during its
   own measurement.

---

## 1. The set, recounted at read time

`git ls-remote --heads origin` — run at read time, after `git fetch origin --prune`:

| Branch | Tip | Pushed (UTC) | Commits ahead of `main` | Payload |
|---|---|---|---|---|
| `claude/conformance-2026-08-03` | `5693919b` | 2026-08-03 03:12 | 1 | 1 digest |
| `claude/conformance-2026-08-04` | `3d083660` | 2026-08-04 02:43 | 1 | 1 digest |
| `claude/conformance-2026-08-05` | `19fc2371` | 2026-08-05 02:14 | 1 | 1 digest |
| `claude/conformance-2026-08-07` | `cee4472b` | 2026-08-07 01:57 | 1 | 1 digest |
| `claude/conformance-2026-08-08` | `f18419fc` | 2026-08-08 03:22 | 2 | digest + `docs/audits/README.md` + an **amendment commit** |
| `claude/conformance-2026-08-09` | `ad1822c9` | 2026-08-09 03:31 | 1 | digest + `docs/audits/README.md` |
| `claude/conformance-2026-08-10` | `40ae0e78` | 2026-08-10 09:55 | 1 | 1 digest |

**Seven, up from six.** **`2026-08-06` still has no branch** — undetermined from inside the repo, as
§2.5 of the prior audit already recorded; nothing found here changes that. **No 2026-08-11 arrival**
(tonight's run has not fired at write time), so the "an 08-11 arrival is itself a finding" tripwire
did not trip.

**Two adjacent refs, recorded and untouched.** `automation/fleet-audit` has advanced `d2036202` →
`8f6e20f8` since the prior census (it appends nightly, as designed). `claude/night-batch-cloud-lanes-a4mpkp`
now exists on `origin` at `fe81e896`, resolving the prior census's recorded ref anomaly. Neither is
in this lane's scope and neither was touched.

---

## 2. Per-digest content sheet

Read with `git show <branch>:docs/audits/<date>-conformance-nightly-digest.md` — no checkout, no merge.

| Digest | Raw | Survived | Killed | Kill-rate | H / M / L filed | Baseline it diffed against | Producer model |
|---|---|---|---|---|---|---|---|
| 2026-08-03 | 7 | 4 | 3 | 43% | 2 / 2 / 0 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-04 | 8 | 6 | 2 | 25% | 3 / 3 / 0 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-05 | 6 | 4 | 2 | 33% | 0 / 3 / 1 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-07 | 3 | 1 | 2 | 67% | 0 / 1 / 0 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-08 | 5 | 0 | 5 | 100% | 0 / 0 / 0 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-09 | 6 | 5 | 1 | 17% | 1 / 3 / 1 | `main`'s 08-02 (**stale**) | sonnet-4-6 |
| 2026-08-10 | 3 | 3 | 0 | 0% | 2 / 4 / 1 (incl. 5 carried) | **`origin/claude/conformance-2026-08-09`** | sonnet-5 |
| **Totals** | **38** | **23** | **15** | 39% | — | — | — |

**28 finding-slots were filed** across the seven digests (23 first-raised + 5 that 08-10 carried
forward with fresh evidence). Every digest is `Reports only` — no digest applied a fix, edited a
living doc, or touched a sibling repo; each carries a clean `git status --porcelain` safety tripwire.

**Two structural notes from the sheet itself:**

- **Six of seven diffed against a stale baseline.** Only the 08-10 run reached past `main` — it
  fetched `origin/claude/conformance-2026-08-09` read-only and diffed against the *actual* previous
  run, stating the correction in its own "Delta vs Prior Baseline" header. The other six each
  compared against `main`'s 2026-08-02 digest because that is the newest one `main` carries.
- **The 08-08 branch carries adjudication, not just a finding.** Its second commit is
  `f18419fc docs(audit): amend 2026-08-08 conformance digest — all 5 findings killed by skeptic`.
  That is decision work, and it is stranded with the branch. §5 M2 below shows it was then lost.

---

## 3. From 28 filed slots to 17 unique items

Deduplicated across nights. `U#` ids are this report's, not the digests'. "Nights" counts nights the
item was **filed as a survivor**; "killed on" counts nights the same item was raised and killed.

| # | Unique finding | Nights filed | Killed on | Severities assigned across nights |
|---|---|---|---|---|
| **U1** | `CONTRIBUTING.md` §"Nightly outcome management" describes the deleted GitHub Action as live | 3 (03, 04, 05) | — | HIGH, HIGH, MED |
| **U2** | `VISION.md` `last_reviewed: 2026-07-25` backward-dated (A2) | 6 (03, 04, 05, 07, 09, 10) | 08 | HIGH, HIGH, LOW, MED, MED, MED |
| **U3** | `protocols/ESSENTIALS.md` `last_reviewed: 2026-07-30` backward-dated (A2) | 3 (04, 09, 10) | 05, 07, 08 | HIGH, MED, MED |
| **U4** | `[#476]` closed before its blob-identity Done-when clause was met | 1 (03) | — | MED |
| **U5** | `[#471]` closed on a non-recursive glob that missed `scripts/toc/cli.py` | 1 (03) | — | MED |
| **U6** | `CONTRIBUTING.md` hook table lists 15 hooks; `.pre-commit-config.yaml` has 17 | 2 (04, 05) | — | MED, MED |
| **U7** | `ARCHITECTURE.md:327` calls `block_ff_push.py` "fail-soft" after §A6 flipped it | 1 (04) | — | MED |
| **U8** | `CONTRIBUTING.md:118` calls `block-ff-push` "fail-soft" | 1 (04) | — | MED |
| **U9** | `ARCHITECTURE.md` omits `block-unanchored-push` entirely (gates ¶ + Ch2 organ map) | 3 (05, 09, 10) | — | MED, LOW, LOW |
| **U10** | `protocols/ESSENTIALS.md:123` instructs agents `/override [reason]` is the only session-end escape | 2 (09, 10) | — | **HIGH, HIGH** |
| **U11** | `ARCHITECTURE.md` says "five carriers" at 4 sites; six `carrier_*.py` exist | 2 (09, 10) | — | MED, MED |
| **U12** | `cd38fb8` claimed to close `[#213] [#215] [#441]` without discharging them | 1 (10) | — | HIGH (historical) |
| **U13** | `ARCHITECTURE.md:405` says `validate_doc_code_edge.py` is "live on 13 rules"; 15 are live | 1 (10) | — | MED |
| **U14** | `ARCHITECTURE.md:95` says "ratified through ADR-109"; the file's own changelog names ADR-110 | 1 (10) | — | LOW |
| **U15** | Cloud runtime `uv 0.8.17` vs the ADR-106 `==0.11.19` pin — every governance gate non-functional | 7 (all) | — | *ungraded — filed as INFRASTRUCTURE in Next Actions* |
| **U16** | `CONTRIBUTING.md:155-156` "native launcher not enabled" is now imprecise (it runs, then faults) | 1 (10) | — | *ungraded — 08-10 explicitly declined to file it as a finding* |
| **U17** | JOURNAL entry (t) broken SHA anchor `ee76c412`, beyond the 10-entry window | 2 (03, 09) | — | *ungraded — carried OUT-OF-SCOPE, never verified on either night* |

**28 filed slots → 14 severity-graded unique findings + 3 ungraded carried items = 17 unique.**
The compression ratio is 2:1, and it is not evenly spread: **U2 alone accounts for 6 of the 28.**

---

## 4. Overlap map — what an open row already records

Every unique item checked against the live open set (`tasks/*.md`, `status: open`, 170 rows). This is
the headline that prices Fork 3.

| # | Owning open row | Evidence |
|---|---|---|
| U1 | **NONE at raise time** → now discharged | `[#503]` was born **2026-08-06** (`e7c0b70e`), *after* the 03/04/05 raises; fixed `59b191c5` (2026-08-06), row `status: closed` |
| **U2** | **`[#453]` gap (1)** — *"the container arrived a **SHALLOW CLONE**… which made `canonical_freshness` hard-FAIL on **`VISION.md`** because the graft point looked like its last edit"* | `tasks/453-cloud-night-run-runbook-container-gaps.md:13`; `status: open`; filed **2026-07-31** (`584ab835`) |
| **U3** | **`[#453]` gap (1)** — same clause, same mechanism, different file | same |
| U4 | NONE | no open row records premature-closure / Done-when-unmet-at-merge; `#277`/`#437`/`#454` own the *proposal detector's* precision, a different thing |
| U5 | NONE | same |
| U6 | NONE at raise time → now discharged | `grep -n "check-seal-identity\|block-unanchored-push" CONTRIBUTING.md` → `:112`, `:120` — both rows present |
| U7 | **`[#504]`**, closed | `tasks/504-…:4 status: closed`; closed `1447d063` (2026-08-06) |
| U8 | **`[#504]`**, closed | same |
| U9 | NONE | `[#497]` (open) covers the retired-posture class at `carrier_mesh.py:75` + `.pre-commit-hooks.yaml`, **not** `ARCHITECTURE.md`; `[#504]` covered `ARCHITECTURE.md:327` posture, not the omission |
| **U10** | **NONE — and this is the defect worth the architect's eye.** `[#503]` swept **eight** `/override`-class sites and closed; `protocols/ESSENTIALS.md:123` is the **ninth**, and the only one on the always-on boot path | `tasks/503-…:12` enumerates `CONTRIBUTING.md` ×6, `DEFINITION_OF_DONE.md:141-149`, `.claude/commands/override.md` — ESSENTIALS absent; row `status: closed` |
| **U11** | **`[#403]`** — *"count/list ⇐ `make_carriers()` keys"*, Done-when *"carrier-set AND child-roster gated"* | `tasks/403-…:13`; `status: open`; predates all seven nights |
| U12 | NONE for the class → discharged on the instance | `a62d988e` (2026-08-09) *"the Phase-A closes were never real — complete them"* |
| U13 | NONE | same *class* as `[#403]` (a machine-derivable ARCHITECTURE count) but outside its Done-when, which names carrier-set + child-roster only |
| **U14** | **`[#403]`, explicitly DEFERRED inside it** — *"Governing-ADR completeness stays DEFERRED (a citation is not a governing relation)"* | `tasks/403-…:13` |
| **U15** | **`[#453]` gap (2)** — *"the container shipped uv 0.8.17 against the ADR-106 `==0.11.19` pin"* | `tasks/453-…:13` |
| U16 | NONE | — |
| U17 | NONE | — |

### The number

**5 of the 17 unique items (U2, U3, U11, U14, U15) were already recorded by a row that was open
before the first of these seven nights ran.** `[#453]` was filed 2026-07-31; `[#403]` predates it.

Weighted by filed slots rather than unique items the picture is worse: those five account for
**16 of the 28 filed findings — 57% of the entire filed output of the stranded stream re-derives
what an open row already owned.** That is the `[#453]` class the operator named, arriving from
inside the organ that is supposed to detect it.

**5 of 17 are genuinely new and unowned** (U4, U5, U9, U10, U13). **5 are discharged**
(U1, U6, U7, U8, U12). **2 are ungraded and unowned** (U16, U17).

**Exactly one unowned item is both HIGH and live: U10.**

---

## 5. What the content census surfaces that the branch census could not

These are this lane's findings, not any digest's. Each carries its evidence line.

### M1 — Six of seven digests state, as fact, that the runs before them did not happen

Because a run can only see `main`, and `main`'s newest digest is 2026-08-02, each night reported its
predecessors as absent:

- 08-04: *"Gap: 2 days… **no conformance digest was run on 2026-08-03**"* — the 08-03 run exists at `5693919b`.
- 08-05: *"Gap: 3 days… **no digests exist for 2026-08-03 or 2026-08-04**"* — both exist.
- 08-08: *"Gap: 6 days… **no conformance digest ran 2026-08-03 through 2026-08-07**"* — four exist.

The stranding does not merely delay the findings. **It makes each digest's Delta section false in a
way a reader cannot detect from the digest alone.** Any future consumption act that trusts a digest's
own delta narrative inherits the error.

### M2 — Adjudication does not survive the stranding, so killed findings resurrect

U3 (`ESSENTIALS.md` A2) was **killed three nights running** — 08-05 K1, 08-07 K1, 08-08 K2 — each time
with a correct and increasingly precise diagnosis. 08-08's kill names the mechanism exactly:

> *"`bcfe3cf6` is listed in `.git/shallow` as a shallow boundary commit. `git log -1 -- VISION.md`
> returns this commit not because VISION.md changed there, but because git cannot traverse further back."*

The 08-09 run then re-filed it as a live MED with a hard date and **no shallow-clone caveat at all**,
and 08-10 carried that forward. The 08-09 run could not have known: the branch carrying the kill was
never merged. **The finding survives the stranding; the skeptic's kill does not.** That is the
asymmetry, and it is why the 08-08 branch's amendment commit matters more than its zero survivors.

### M3 — Every A2 freshness finding in all seven digests is a container artifact, and it is refuted

The reported "last commit date" for both files marches with the **run date**, not with either file:

| Run | `VISION.md` last-commit as reported | `ESSENTIALS.md` last-commit as reported |
|---|---|---|
| 08-03 | 2026-07-27 | — |
| 08-04 | 2026-07-31 | 2026-07-31 |
| 08-05 | 2026-07-31 | 2026-07-31 |
| 08-07 | 2026-08-02 (named a shallow boundary) | 2026-08-02 (killed as such) |
| 08-08 | 2026-08-03 (named a shallow boundary) | 2026-08-03 (killed as such) |
| 08-09 | **2026-08-04** | **2026-08-04** |
| 08-10 | **2026-08-05** | **2026-08-05** |

Two different files cannot share a last-edit date on six consecutive nights. Ground truth on full
history, from this worktree at `12ef9c91`:

```
git log -1 --format=%as -- VISION.md              -> 2026-07-25   (stamp: 2026-07-25)
git log -1 --format=%as -- protocols/ESSENTIALS.md -> 2026-07-29   (stamp: 2026-07-30)
```

and the gate itself, called directly rather than reasoned about:

```
canonical_freshness_gate.evaluate(Path('.'))  ->  FAILS: []   WARNS: []
```

**Zero A2 failures, zero A1 warnings.** `VISION.md`'s stamp is same-day; `ESSENTIALS.md`'s is
forward-dated by one day. **U2 and U3 do not reproduce.** They are 9 of the 28 filed slots — **32%
of the stream's filed output is a single false-positive class that `[#453]` named on 2026-07-31**,
ten days before the last of them was filed.

Two nights (08-07, 08-08) diagnosed this correctly and were overruled by the two nights that
followed, for the reason in M2.

### M4 — Severity is not a property of the finding in this stream

U2, with identical (and false) evidence every night, was assigned **HIGH, HIGH, LOW, MED, killed,
MED, MED**. U1 went **HIGH, HIGH, MED** while nothing about it changed. Two nights explicitly
*escalated* U2 to HIGH on the grounds that it had persisted — a rule that ratchets severity by age
will drive a false positive to HIGH given enough nights, and here it did, twice.

**Implication for the absorb:** severity labels in these seven digests cannot be used to order the
consumption work. The triage in §6 re-derives severity from live state instead.

### M5 — The one live HIGH is unowned, and it is on the boot path

`protocols/ESSENTIALS.md:123`, verified live at `12ef9c91`:

> *"…a session with commits must name ≥1 commit SHA from *this session* or the Stop-hook blocks
> turn-end; `/override [reason]` is the only escape."*

ADR-85 amendment 2026-08-03 §A2 retired that path — `CLAUDE.md` v2.51 corrected the identical claim
in §7 the same day, and `[#503]` swept eight more sites on 08-06. **ESSENTIALS was in neither.** It is
first-read item 2 for every session in this repo and every consumer that inherits it, and it names an
escape hatch that discharges nothing.

The digests found it on 08-09 and again on 08-10, correctly, at HIGH. **Nobody has read either.**

### M6 — A lane finding: the absorb's own index regen re-emits a stale pointer

`docs/audits/README.md` is generated, and its header reads *"Retention/roll-up policy is **proposed
separately** ([#212])."* `[#212]` was **closed 2026-07-06** (`b4c4b6e4`), folded into **ADR-100**
(`a40bac40`), which *ruled* retention — keep-all + a count-tiered index. The string is hard-coded at
`scripts/gen_audit_index.py:72` (and its docstring, `:9`), so **every regeneration re-emits it**,
including the one this absorb requires. This is the `[#503]` class — *the thing it describes was
retired underneath it* — at a generated site, which is why no edit-keyed signal will ever catch it.

Reported, not fixed. It is not a digest finding; it surfaced from reading the absorb path.

---

## 6. DRAFT triage — **applies only under the operator's Fork 3 + ADR-111 rulings**

> ### ⚠ DRAFT. NOT A TRIAGE.
> **ADR-111 is `Status: Proposed` and binds nothing.** Fork 3 is unruled. Every cell below is a
> **DRAFT** proposal for the operator, produced by a lane that merged nothing and filed nothing. No
> row was opened, closed, annotated or amended on the strength of any line here. If Fork 3 rules the
> digests stay on their branches, this whole table is void.

Outcome vocabulary is ADR-111 §1: **(a) OWNED** — an open row covers it, attach evidence, birth
nothing · **(b) DISCHARGED** — done or ruled, locator mandatory and must resolve · **(c) CANDIDATE** —
needs a decision, becomes or joins an intake · **(d) REJECTED** — recorded with reason, not relitigated.

| # | DRAFT outcome | Locator / row / reason | Live-state evidence line |
|---|---|---|---|
| U1 | **DRAFT — DISCHARGED** | `59b191c5` (2026-08-06) fixed it under `[#503]`, closed `1447d063` | `grep -n "RETIRED 2026-07-08" CONTRIBUTING.md` |
| **U2** | **DRAFT — REJECTED** *(reason: container artifact; does not reproduce)* | Not a defect in the repo. The recurrence is nth-instance evidence for **`[#453]` gap (1)** | `python -c "…canonical_freshness_gate.evaluate(Path('.'))"` → `([], [])`; `git log -1 --format=%as -- VISION.md` → `2026-07-25` = stamp |
| **U3** | **DRAFT — REJECTED** *(same reason)* | same; also already killed on merit by the 08-05 / 08-07 / 08-08 skeptics | `git log -1 --format=%as -- protocols/ESSENTIALS.md` → `2026-07-29` < stamp `2026-07-30` (forward-dated, passes) |
| U4 | **DRAFT — CANDIDATE** | The *instance* is repaired (`0e27f308`, 16 min post-close); the *class* — a row closed before its Done-when was met — has no owner. Joins an intake with U5 + U12, not three rows | `git log -1 --format='%h %as %s' 0e27f308` → `2026-08-02 fix(backpressure): compare the lane copy by BLOB, not by name` |
| U5 | **DRAFT — CANDIDATE** | same class, same intake | `git log -1 --format='%h %as %s' 13d9cc16` → `2026-08-01 fix(toc): … make the newline sweep RECURSIVE — codex HIGH` |
| U6 | **DRAFT — DISCHARGED** | Both hooks now carry table rows | `grep -n "check-seal-identity\|block-unanchored-push" CONTRIBUTING.md` → `:112`, `:120` |
| U7 | **DRAFT — DISCHARGED** | `[#504]`, closed `1447d063` | `ARCHITECTURE.md:30-31` records the flip to *"fails CLOSED (exit 2)"* |
| U8 | **DRAFT — DISCHARGED** | `[#504]`, closed `1447d063` | `CONTRIBUTING.md:119` → *"**Fails CLOSED (exit 2) on internal error**"* |
| U9 | **DRAFT — CANDIDATE** | Live and unowned. `[#497]` covers *different* sites; `[#504]` closed on the posture claim, not the omission | `grep -c "block-unanchored" ARCHITECTURE.md` → `0` |
| **U10** | **DRAFT — CANDIDATE (the priority one)** | Live, HIGH, unowned, on the boot path. **`[#503]`'s ninth site.** Recommend it be raised as its own intake rather than folded — a closed row's missed site is the evidence, and burying it in a bundle loses that | `grep -n "override" protocols/ESSENTIALS.md` → `:123 … "/override [reason]" is the only escape` |
| **U11** | **DRAFT — OWNED (`[#403]`)** | Attach evidence to `[#403]`; **birth nothing.** Its Done-when — *carrier-set gated* — is exactly this | `ls deploy/carrier_*.py` → 6 files; `grep -n "five carrier" ARCHITECTURE.md` → 4 hits (`:282`, `:456`, `:615`, `:888`) |
| U12 | **DRAFT — DISCHARGED** | Self-corrected 18 min later; HEAD is correct | `git log -1 --format=%s a62d988` → *"the Phase-A closes were never real — complete them"* |
| U13 | **DRAFT — CANDIDATE**, recommended **folded into `[#403]`** as a third derived claim | Same class (machine-derivable ARCHITECTURE count), outside `[#403]`'s current Done-when. A scope extension beats a new row — `[#403]` already took one (intake #17 §1 D6) | `grep -c '# DONE' ecosystem/doc-code-edge.yaml` → `15`; `ARCHITECTURE.md:405` → *"live on 13 rules"* |
| **U14** | **DRAFT — OWNED (`[#403]`, deferred leg)** | `[#403]` explicitly defers Governing-ADR completeness. **Attach, do not birth, and do not re-litigate the deferral** | `ARCHITECTURE.md:95` → *"ratified through ADR-109"*; ADR-110 `Status: Accepted` 2026-08-06 |
| **U15** | **DRAFT — OWNED (`[#453]` gap 2)** | Attach seven nights of recurrence as evidence of severity; birth nothing | `tasks/453-…:13` — *"the container shipped uv 0.8.17 against the ADR-106 `==0.11.19` pin"* |
| U16 | **DRAFT — CANDIDATE (low)** | The 08-10 run declined to file it and said so; it is a real state distinction (*unavailable* vs *available-but-faulting*) | `CONTRIBUTING.md:155-156` |
| U17 | **DRAFT — CANDIDATE (low)** | Carried unverified on two nights. Either verify `ee76c412` once and discharge, or reject the carry | `git cat-file -t ee76c412` — **not run by this lane** (out of its read scope) |
| M6 | **DRAFT — CANDIDATE** | This lane's own finding; `[#503]`-class at a generated site | `grep -n "212" scripts/gen_audit_index.py` → `:9`, `:72`; `[#212]` closed `b4c4b6e4` 2026-07-06 |

**DRAFT roll-up:** OWNED 3 · DISCHARGED 5 · CANDIDATE 7 · REJECTED 2 (18 rows = 17 unique + M6).

**One ADR-111 edge this triage hit, and could not resolve from the doctrine.** U2/U3 are simultaneously
*a false finding* (→ REJECTED) and *nth-instance evidence for an open row* (→ OWNED, "attach the
evidence to that row"). ADR-111 §1 requires **exactly one** outcome. This draft rules REJECTED for the
finding-as-stated and records the recurrence under `[#453]` as a note — but that is a judgement call
the ADR does not authorise. Batched as Q4 below.

---

## 7. Absorb-mechanics appendix

Everything here is verified against live state. Nothing was executed.

### 7.1 Serial merge order

Chronological, oldest first — **08-03 → 08-04 → 08-05 → 08-07 → 08-08 → 08-09 → 08-10**. The digests
reference each other by date; the index is date-sorted, so a single trailing regen is deterministic
regardless of order, but chronological keeps `main`'s spine legible as a stream.

### 7.2 What each merge actually costs

1. **Five of seven are clean adds.** One new `docs/audits/*.md` each, sharing no path with `main`.
2. **Two will conflict.** `claude/conformance-2026-08-08` and `-2026-08-09` each carry a
   `docs/audits/README.md` edit generated against an index of **423 / 424** documents. `main` is at
   **459**. Resolve by discarding the branch side and regenerating — never hand-merge a generated
   file: `git checkout --ours docs/audits/README.md && python scripts/gen_audit_index.py --write`.
3. **A conflict-free merge skips `pre-commit` entirely** (only `commit-msg` hooks run), so the five
   clean merges leave the index stale **silently**, and `audit-index-freshness` then fires on the next
   unrelated commit. **Precedent:** `24882f8c` (2026-08-02) added the digest alone; the index was not
   regenerated until 2026-08-04. The prior audit §2.3 already records the landed absorb as **two**
   commits for exactly this reason. **The trailing index-regen commit is mandatory, conflicts or not.**
4. **Filename grammar passes** — verified by calling the parser, not by inspection:
   `validate_hermetization.classify('docs/audits/2026-08-03-conformance-nightly-digest.md')` → `None`;
   `conformance-nightly-digest` is a member of `AUDIT_CLASS_ENUM`. **ADR-101 Rule B will not block.**
5. **`block-unanchored-push` (pre-push, fail-CLOSED) will refuse the push.** Seven merges put seven
   entries on `main`'s first-parent spine. Discharge is **range-level**: one JOURNAL entry naming ≥1
   SHA the range *introduces* (e.g. `40ae0e78`) covers all seven. **The ADR-110 batch exemption does
   not extend to `claude/*` lanes** — anchor before pushing, not after.
6. **`block-ff-push`** — pass `--no-ff` explicitly on every merge. Each branch is 1–2 commits ahead of
   a long-superseded `main`, so git would not fast-forward anyway; the flag is belt-and-braces.
7. **No `doc_claims` exposure.** `ecosystem/doc-counts.md` pins the audit-check count (41) and gate
   count (17), **not** the audit-document count. Adding seven files moves nothing pinned.
8. **No `silent_rule_ratchet` exposure.** Its scope is `protocols/*.md` (non-recursive) + `templates/**`
   + `ecosystem/*.yaml`. `docs/audits/` is outside it.

### 7.3 The one genuine rule conflict — MERGE IS ATOMIC vs EXPLICIT PROTECTION

The contract frames the absorb as *"each absorbed branch deletes at its merge"*. **The standing rule
currently says the opposite for this exact glob.** `.claude/rules/git-discipline.md:17-20`:

> *"**MERGE IS ATOMIC:** merge `--no-ff` + push + delete the source branch are ONE operation… Exceptions
> exist only by EXPLICIT PROTECTION (currently `claude/conformance-*`); silence is not protection."*

`claude/conformance-*` is the **named** exception. So same-step deletion is precisely what the rule
withholds here, and an absorb-×N that deletes on merge is **not authorised by the rule as written**.

Past practice already worked around it rather than resolving it: all five 07-29…08-02 absorb merges
carry **`operator-authorized <date>`** in their own subject lines — a per-instance authorisation
stacked on top of the protection. **That is the surface a Fork-3 ruling should move**, and three shapes
are available:

- **(a) Retire the clause** — protection existed because nothing absorbed; if absorb becomes an organ,
  the reason expires. Cleanest; requires editing a `~/.claude`-adjacent rule (core-invariant #6 territory).
- **(b) Narrow it** — *"protected until absorbed"*, making deletion automatic post-merge and keeping the
  pre-absorb guarantee. Smallest edit; keeps the safety property that matters.
- **(c) Keep it as-is** — branches survive their own absorb, which **reinstates the accumulation the
  ruling is trying to kill** (they'd merely be merged-and-kept instead of unmerged-and-kept).

### 7.4 The repo has drained this queue twice, two different ways

Both are on `main`'s spine and both are live precedent for Fork 3:

| Route | Instances | Commits | What landed | What it cost |
|---|---|---|---|---|
| **(A) Per-branch `--no-ff` absorb** | 5 (07-29 → 08-02) | `bb217819`, `61757e82`, `bd08f343`, `c7af2c03`, `24882f8c` (+ `25e9dc7d` index regen) | Every digest, verbatim, on `main` | One operator round-trip per night; the habit that lapsed |
| **(B) Extraction aggregate + bulk delete** | 1 (`[#434]`, 07-27/28) | `16c5386f` (2 aggregate audit files, 179 insertions) then `c0b40d37` (**7 branches deleted**) | Two synthesis documents | **`main` carries no digest for 2026-06-15 → 2026-07-28.** The analysis landed; the source digests did not |

That 44-day hole in `main`'s digest stream is route (B)'s receipt. Route (A) is why 06-04…06-14 and
07-29…08-02 are there.

### 7.5 DRAFT amendment text — `[#419]` / `[#426]` Done-when

> **DRAFT — paste-ready, NOT applied.** Nothing was edited. Both rows are `status: open` and untouched
> by this lane. Wording is proposed for the operator, and neither row's `kill-candidates:` line is
> affected (both currently read `none`, with reasons that remain accurate).

**`[#419]` — current Done-when:**

```
· Done when: every standing routine has a named consumer and a consumption path, and
  unconsumed output is surfaced rather than silently accumulating
```

**`[#419]` — DRAFT replacement:**

```
· Done when: every standing routine has a named consumer and a consumption path; unconsumed
  output is SURFACED, not silently accumulating; and for the nightly conformance routine
  specifically, the absorb is an ORGAN and not a habit — it has a trigger that fires without
  an operator remembering, and a detector that reports the queue depth (count of unmerged
  `claude/conformance-*`) at a surface the operator already reads, so a lapse is visible on
  the day it starts rather than eight days later
```

**`[#426]` — current Done-when:**

```
· Done when: every live routine declares a consumer and consumption path or is retired, and
  the dead-producer nags are resolved
```

**`[#426]` — DRAFT replacement:**

```
· Done when: every live routine declares a consumer and consumption path or is retired; the
  dead-producer nags are resolved; and `routine_consumers`' own stated boundary is closed or
  recorded permanent-defer-with-reason — today it gates only BACKLOG rows carrying a
  `· routine:` marker, so it reports [OK] while a routine that is not a row (the nightly
  conformance organ) accumulates unread output, which is the exact case that produced the
  2026-08-03..10 queue
```

**Rationale for both, stated rather than implied.** `[#419]`'s current Done-when is satisfiable by a
*declaration* — naming a consumer discharges it. The 07-29…08-02 window had a named consumer (the
operator) and a real consumption path (the absorb merge), and the queue still formed, because the
path had no trigger. The draft moves the bar from *declared* to *fires without being remembered*.
`[#426]`'s addition targets the specific measured gap: the check is green while the organ it should
cover is invisible to it, which the prior audit §2.3 established from the check's own docstring.

**A filing-backpressure note the operator will need:** if either edit lands as a *new row* rather than
an amendment to these two, the `backlog-filing-backpressure` commit-msg hook requires a flush-left
`kill-candidates:` line naming ≥1 existing id or `none — <reason>`. Amending in place avoids it.

### 7.6 Retention arithmetic — what a Fork-3 ruling kills, and what it does not

**Production rate, measured:** 7 branches over the 8 nights 2026-08-03…08-10 = **0.875/night**
(2026-08-06 absent). Annualised: **~319 branches/yr** at the observed rate, **~365/yr** at a clean
one-per-night. Each holds exactly one file of roughly 10–20 KB.

**What the ruling kills — the accumulation term.** Steady state moves from *+1 branch/night, forever*
to *≤1 outstanding branch at any time*. On the current 7-deep queue that is 7 branches reclaimed
immediately and ~319–365 not created over the next year. **It does not change the production term** —
the routine still runs nightly and still writes one file per night.

**What it does NOT create as a new problem.** ~365 files/yr into `docs/audits/` (index currently at
**459 documents**) is **already ruled acceptable**: `[#212]` was closed 2026-07-06 into **ADR-100 —
audit retention keep-all + count-tiered index**. There is no second-order retention question to
answer here, and the count-tiered index is designed for exactly this growth. The only residue is M6:
the generated index header still calls that ruled policy *"proposed separately"*.

**The cost of NOT ruling, priced from this census.** Per night of continued stranding the repo
accrues: one unmerged branch; a Delta section that misstates its own predecessors (M1); one round of
skeptic adjudication that will be lost and whose kills will resurrect (M2); and ~2 filed findings, of
which — on the measured 57% rate — roughly one re-derives a row that is already open.

---

## 8. Packet

- **Set at read time:** **7** branches (`08-03, 04, 05, 07, 08, 09, 10`). **08-06 still absent.**
  **No 08-11 arrival.** Grew by **+1** since the 2026-08-10 morning census — during that census's own day.
- **Findings total vs unique:** **38 raw → 28 filed slots → 17 unique** (14 severity-graded + 3 ungraded).
  **15 killed by the digests' own skeptics.**
- **Owned / new split (unique):** **5 OWNED** by rows open before night one · **5 DISCHARGED** ·
  **5 genuinely new and unowned** · **2 ungraded and unowned**.
- **Owned / new split (by filed slot — the number that prices Fork 3):** **16 of 28 filed findings
  (57%) re-derive an already-open row.** **9 of 28 (32%) are one refuted false-positive class.**
- **Live and unowned HIGH: exactly one — U10**, `protocols/ESSENTIALS.md:123`, found twice, read never.
- **Refuted:** U2 and U3. The A2 gate is **green** on full history — `evaluate()` → `([], [])`.
- **DRAFT triage:** OWNED 3 · DISCHARGED 5 · CANDIDATE 7 · REJECTED 2. **Void unless Fork 3 and
  ADR-111 are ruled.**
- **Absorb blockers, verified:** 2 index conflicts (08-08, 08-09) · 1 mandatory trailing index-regen
  commit · 1 pre-push JOURNAL anchor covering the whole range · **1 rule conflict** (MERGE IS ATOMIC
  vs the `claude/conformance-*` protection clause) that a ruling must resolve before any deletion.
- **Nothing merged, nothing deleted, nothing fixed, nothing filed.**

### Batched questions for the operator

1. **Fork 3 route — (A) per-branch absorb ×7, or (B) extraction aggregate + bulk delete?** Both have
   in-repo precedent (§7.4). (A) preserves all seven digests verbatim and costs 8 commits;
   (B) costs 2–3 and drops the sources, as the 44-day 06-15…07-28 hole shows.
2. **The protection clause (§7.3) — retire, narrow to "protected until absorbed", or keep?** An
   absorb that deletes on merge is not authorised by the rule as written, and "keep" reinstates the
   accumulation the ruling targets.
3. **U10 — does it get its own intake, or fold into a bundle?** It is the only live unowned HIGH and
   it is `[#503]`'s ninth site. My draft recommends its own, so the missed-site evidence survives.
4. **ADR-111 edge (§6) — when a finding is both false *and* nth-instance evidence for an open row,
   which single outcome applies?** This draft chose REJECTED-with-a-note; the ADR does not say.
5. **U13 — extend `[#403]`'s Done-when to a third derived claim, or a new row?** Extension precedent
   exists inside `[#403]` itself (intake #17 §1 D6).
6. **M6 — fix `gen_audit_index.py:72` in the absorb commit, or file it?** The absorb regenerates that
   file anyway, so the stale pointer will be re-emitted by the very act of consuming the queue.
