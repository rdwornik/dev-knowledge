# Archival lifecycle audit — do ADRs and intakes actually get archived, or do they accumulate?

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** archival-lifecycle-audit
- **Source-session:** batch lane `lane-archival-audit`, branch `worktree-lane-archival-audit`, base `3ed60c4c` (`main` at provisioning)
- **Status:** EVIDENCE ONLY — **zero moves, zero deletions, zero status edits, zero BACKLOG touches.** This arc archives nothing; the cleanup, if any, is a later arc against written exit conditions.
- **Model:** one Opus-class seat, no fan-out. Retrieval was deterministic (frontmatter/status-line parse, `git log`, directory listings), not model-summarized.
- **Consumer:** the architect seat that rules on whether an archival mechanism is owed.
- **Consumption path:** §1 for what the repo already says · §2 for whether anything enforces it · §3–§4 for the live counts · §5 for the concrete gap · §6 for the adjacent currency check.

---

## Headline

**Both corpora ARE archived, by hand, and the live sets are currently conformant.** The gap is
not accumulation of un-archived material — it is that **no organ exists to keep it that way.**
Every archival move in the repo's history was performed manually under a single operator ruling
of 2026-07-22, and each of the three corpora resolves the question differently:

- **ADRs** — rule exists (terminal → `docs/decisions/archive/`); **2 of 85 files archived**; live gap set is **EMPTY** under the stated rule.
- **Intakes** — rule exists (terminal → `docs/intake/archive/`); **6 archived**, 23 live; live gap set is **EMPTY** — no live intake carries a terminal status.
- **Audits** — **there is deliberately NO archival rule.** ADR-100 rules that audit files *never* move; navigability is the index, not the filesystem. That is a ruled position, not an omission.

The one genuine finding is §5: the criterion actually applied in 2026-07-22 was **narrower than the
written rule**, and the extra criterion lives only in a commit body.

---

## 1. The doctrine, quoted

### 1a. ADRs — a written rule exists

`docs/decisions/README.md:8`:

> `archive/` holds terminal (Superseded/Deprecated) ADRs, relocated byte-identical.

The enum and the lifecycle are stated at `CONTRIBUTING.md:185-190`:

> - Status values: `Proposed | Accepted | Superseded | Deprecated` (reconciled against
>   on-disk reality 2026-07-23, [#398] — operator-ruled; the never-used `Withdrawn`
>   dropped, the lived-but-undeclared `Proposed` and `Deprecated` admitted)
> - Status lifecycle: `Proposed → Accepted` by editing the Status line **in place at
>   ratification** (ADR-94 Pattern B — the status line is metadata, not decision
>   content); `Superseded`/`Deprecated` are terminal — a terminal ADR relocates
>   byte-identical to `docs/decisions/archive/` (operator ruling 2026-07-22)

The same file, `CONTRIBUTING.md:192-198`, pre-declares the three live exceptions as carve-outs
rather than as violations:

> - Legacy off-enum statuses on disk (named carve-outs, **not** precedent — retro-
>   normalization is deferred to [#242] with reasons): ADR-88/89 frozen `Proposed`
>   ratified by in-file markers (ADR-94's explicit operator-gated deferral); ADR-82
>   frozen `Proposed` canonical-by-waiver since 2026-06-11 (same class, [#242]'s
>   retro-normalize domain per the 2026-07-22 night-batch audit P2b); ADR-45
>   `Explored, not adopted` + ADR-46/47 `Partially superseded` (any ADR-45 flip is
>   additionally gated by [#362]'s dropped-rules disposition)

**Authority note.** No *ADR* rules ADR archival. The rule's authority is the operator ruling of
2026-07-22, recorded in `docs/decisions/README.md` + `CONTRIBUTING.md` and in the commit that
executed it (`216ce3a8`). ADR-94 governs the adjacent question (status-line mutability) and is
silent on relocation.

### 1b. Intakes — a written rule exists, and it names its own missing mechanism

`docs/intake/README.md:156-160` (the lifecycle, with terminal states routed to archive):

> ```
> SEED → DRAFT → READY → ACCEPTED (decided-by + disposition)   [live]
>                      → CONSUMED (consumed-by)                [terminal → archive/]
>                      → SUPERSEDED (superseded-by)            [terminal → archive/]
>                      → REJECTED (reason, kept)               [terminal → archive/]
> ```

`docs/intake/README.md:193-199`:

> Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
> `docs/intake/archive/` (operator ruling 2026-07-22, archive-inside-each-folder;
> terminal set per the [#398] deploy — ACCEPTED is deliberately NOT in it, a standing
> authority must stay visible live); live docs stay here. **The move is MANUAL for now —
> the status-coupled validator that would gate/automate it is wave work, not built.**
> Archived docs drop out of the generated Contents index (depth-1 scan); their
> `intake-id` join keys stay valid at the archive path.

ACCEPTED being explicitly *non*-terminal is load-bearing and stated twice — `README.md:179-183`:

> - **ACCEPTED (decided-by + disposition)** — ruled standing authority: … **Not archival** —
>   an ACCEPTED doc stays live and visible.

### 1c. Audits — **no archival rule exists, by ruling**

This absence is deliberate and is itself the doctrine. ADR-100 (`Accepted 2026-07-07`),
`docs/decisions/ADR-100-audit-retention-index-rule.md:34`:

> - **Everything older moves to an archive *section of the index*** — **a section of the index,
>   not the filesystem.** **Files never move; only their index grouping does.**

…and `:63`, recording the rejected alternative:

> - **Physically move older audits to an `archive/` dir.** Rejected here and gated for the
>   future (§3): no `archive/` dir exists, the move is under-scanned (the known gap), and
>   ADR-36/ADR-60 cite the directory structurally — a move needs a full referential-currency
>   scan **plus** an explicit architect ruling.

**Stale pointer found.** `docs/audits/README.md:5` still says:

> Retention/roll-up policy is proposed separately ([#212]).

[#212] was **folded and closed by ADR-100** (`ADR-100:8` — *"Folds and closes BACKLOG #212"*), and
no `212-*.md` exists under `tasks/`. The index header points at a closed ticket for a policy that
has since been ruled. Reported, not fixed (this arc edits no doctrine).

### 1d. `docs/archive/` — a different thing entirely

`docs/archive/` is **not** the ADR/intake archive. It is the ADR-60 pending-classification
triage queue. `docs/archive/README.md:1-10`:

> # archive/ — Pending-Classification Zone
> Per ADR-60 amendment 2026-05-27.
> Holding zone for artifacts whose destination isn't yet decided. Reviewed periodically; each
> item is either: deleted (git history retains it), or promoted to `decisions/`, `audits/`,
> `handoffs/`, `diagrams/`, or authored into an ADR.
> Not a dumping ground — a triage queue. **If something sits here across two reviews with no
> decision, default to deletion.**

`ADR-60:127` states the same semantics canonically. It holds **9 files + README**, all dated
2026-04-23 → 2026-06-05.

### 1e. `protocols/archive/` — the adjacent third corpus, and the honest limit on all of them

ADR-83 (`Accepted 2026-06-11`) governs superseded protocols. `ADR-83:20`:

> **Superseded or dead protocols move to `protocols/archive/<name>.md` carrying a blockquote
> tombstone at the top of the file. `protocols/` (top level) holds only live specs.**

And `ADR-83:52` — the clearest statement in the repo of the enforcement posture that turns out to
hold for *every* archival rule here:

> - **Cost:** the convention is enforced by discipline + review, not a hook (Layer-2 stays
>   validators-only; no orchestration added). A future check could assert "every
>   `protocols/archive/*.md` opens with an ARCHIVED blockquote" if drift appears.

---

## 2. The mechanism — **none found**

**No script, hook, command, gate, or test moves, marks, or flags an ADR or intake for archival.**

The searches performed (all read-only, from the lane worktree at `3ed60c4c`):

| # | Search | Result |
|---|---|---|
| 1 | `grep -rn "archive" scripts/*.py` | 18 hits across 7 files — **every one is an EXCLUSION** (skip `archive/` when walking) or a docstring. Zero movers. |
| 2 | `grep -rln "decisions/archive\|intake/archive" scripts/ .claude/ .pre-commit-config.yaml plugins/` | one file: `scripts/gen_intake_index.py` (+ its `.pyc`) |
| 3 | `grep -rn "git mv" scripts/ .claude/commands/ plugins/` | **zero hits** |
| 4 | `grep -rn "CONSUMED\|SUPERSEDED\|REJECTED" scripts/*.py` | intake enum appears once, at `gen_intake_index.py:42` `_STATUS_ORDER` — for **index ordering only** |
| 5 | `grep -rlin "superseded\|deprecated" scripts/*.py` | 5 files; none relates an ADR's status to its location |
| 6 | `grep -rn "adr" scripts/audit.py \| grep -i "status\|archive\|supersede"` | one hit, `audit.py:604` — `adr38_baseline`, unrelated |
| 7 | `grep -rln "archive" tests/ --include=*.py` | 8 test files; the only `docs/` archive assertion is `test_audit.py:1749`, a handoff-version comment |
| 8 | `grep -rln "archive" .pre-commit-config.yaml .claude/commands/ protocols/` | no hook or command implements archival; matches are prose |

The single organ that is archive-aware states its own non-participation in its module docstring,
`scripts/gen_intake_index.py:6-11`:

> Archival model (operator ruling 2026-07-22, superseding the earlier M4 never-move ruling):
> TERMINAL docs relocate byte-identical to docs/intake/archive/ -- the depth-1 glob below drops
> them from the index while their intake-id join keys stay valid at the archive path (README
> section 5). **This generator itself MOVES NO FILE -- the relocation is manual;** it only
> splices a marker-bounded Contents block into the hand-authored docs/intake/README.md

Its effect is *consequential*, not causal: because the glob is depth-1, a file moved by hand
disappears from the index automatically. Nothing detects a file that *should* have moved.

**The mechanism gap is already filed, under a different framing.** [#242] "ADR status-flip
coherence check" (`tasks/242-adr-status-flip-coherence-check.md`, `status: open`, P2/M, in
`tasks/manifest.json:150`) would build the closest thing: *"a read-only audit leg that flags an ADR
whose header status diverges from its README-index effective status."* That is a **status-legibility**
check, not a **status↔location** check — it would catch §5's ADR-45 divergence but would not
notice a `Superseded` ADR sitting outside `archive/`. Also live: [#362] (`tasks/manifest.json:1471`)
which additionally gates any ADR-45 flip, and [#402] (`:1455`) for the intake naming clause.

**Every archival move in this repo's history was manual.** `git log --diff-filter=A` over the two
archive dirs returns exactly three commits, all within 24 hours of one ruling:

| Commit | Date | What moved |
|---|---|---|
| `af63a0f3` | 2026-07-22 | first `docs/intake/archive/` — 3 CONSUMED intake docs |
| `216ce3a8` | 2026-07-22 | first `docs/decisions/archive/` — ADR-40 (Deprecated) + ADR-52 (Superseded) |
| `6551d363` | 2026-07-23 | 3 newly-terminal intake docs, under [#398] |

---

## 3. ADR live census

**85 ADR files total** — 83 in `docs/decisions/`, **2** in `docs/decisions/archive/`.

Reconciliation with the directory listing: `ls docs/decisions/` = 85 entries = 83 `ADR-*.md` +
`README.md` + `archive/`; `ls docs/decisions/archive/` = 2. Numbering runs ADR-27 → ADR-110 (84
slots); **ADR-44 is Reserved with no file on disk** (`docs/decisions/README.md:33` — *"Reserved —
scrum-master review propagation authority codification; held pending N=2 empirical instance"*),
leaving 83 numbered files, **plus 2 separate amendment files** (`ADR-51-amendment-2026-07-05-…`,
`ADR-70-amendment-2026-07-07-…`) = 85. ✅ reconciles.

### By status (live frontmatter / status-line values, as written)

| Status as written | Count | Location |
|---|---|---|
| `Accepted` (incl. parenthesised ratification notes) | 80 | live |
| `Explored, not adopted` — ADR-45 | 1 | live |
| `Partially superseded — retained as convention, NOT audit-enforced` — ADR-46, ADR-47 | 2 | live |
| `Deprecated (was: Accepted)` — ADR-40 | 1 | **archive/** |
| `~~Accepted~~ Superseded by ADR-53 (2026-05-19)` — ADR-52 | 1 | **archive/** |
| **Live total** | **83** | |
| **Archived total** | **2** | |

**Zero live ADRs carry `Superseded` or `Deprecated`** — the two values the stated rule makes
terminal.

**Schema note (three status-line formats coexist).** `**Status:** X` (most), `- **Status:** X`
(bulleted header block, ADR-48 onward), and YAML frontmatter `status: Accepted 2026-05-28`
(ADR-61 only). Any future machine check must parse all three; a single-format parser reports a
false `None` on ADR-61, which is exactly what the first pass of this audit's own extractor did.

### The two archived ADRs — where they live and what marks them

Both are in `docs/decisions/archive/`, moved byte-identical (`216ce3a8` shows `| 0` diff on both
paths — pure renames), and both are marked in **three** places beyond the frontmatter:

- **ADR-40** — status line `Deprecated (was: Accepted)`, date line `2026-04-30 (deprecated 2026-05-23)`, and README index row `docs/decisions/README.md:29`: *"Deprecated 2026-05-23; relocated byte-identical to `archive/` 2026-07-22"*.
- **ADR-52** — status line `~~Accepted~~ Superseded by ADR-53 (2026-05-19)`, and README index row `:41`: *"~~AGENTS.md convention…~~ Superseded by ADR-53 — relocated byte-identical to `archive/` 2026-07-22"*.

**Oldest un-archived terminal ADR by date: none exists** — the terminal set is empty. The oldest
*archived* one is ADR-40 (dated 2026-04-30, deprecated 2026-05-23, archived 2026-07-22 — a
**60-day lag** between the deprecation and the relocation, which is the interval a mechanism would
have closed).

---

## 4. Intake live census

**29 intake documents total** — **23 live** in `docs/intake/`, **6** in `docs/intake/archive/`.

Reconciliation: the generated index at `docs/intake/README.md:19` states **"23 intake documents."**
and lists 23; `ls docs/intake/*.md` = 24 (23 + `README.md`); `ls docs/intake/archive/` = 6. ✅
reconciles, and the per-status counts below match the generated index group headings exactly
(SEED (10) / DRAFT (4) / READY (1) / ACCEPTED (8)).

### Live (23) — by live-schema status

| Status | Count | intake-ids |
|---|---|---|
| `SEED` | 10 | #4, #5, #6, #7, #8, #9, #19, #21, #22, #23 |
| `DRAFT` | 4 | #10, #24, #25, #27 |
| `READY` | 1 | #15 |
| `ACCEPTED` | 8 | #12, #13, #14, #16, #17, #18, #20, #26 |
| `CONSUMED` / `SUPERSEDED` / `REJECTED` | **0** | — |

**No live intake carries a terminal status.** The `OTHER` bucket that `gen_intake_index.py:44`
would emit for an off-canon value is absent from the generated index — independent confirmation
that all 23 sit on the ruled enum.

### Archived (6) — all terminal, all with their required companion field

| intake-id | Status | Companion field present | File |
|---|---|---|---|
| #1 | CONSUMED | `consumed-by: "ADR-98, #268"` | `2026-07-06-functional-architect-nightly-loop.md` |
| #2 | CONSUMED | `consumed-by: "#272 …, #273 …"` | `2026-07-06-platform-feature-scan.md` |
| #3 | CONSUMED | `consumed-by: "#278 …"` | `2026-07-07-test-suite-hygiene.md` |
| #11 | SUPERSEDED | `superseded-by: "the fleet-parity sweep register…"` | `2026-07-11-tech-fleet-divergence-register.md` |
| #14 | CONSUMED | `consumed-by: "2026-07-12-siem-requirements-ruled-pack.md…"` | `2026-07-13-siem-fleet-management-requirements.md` |
| #14 | CONSUMED | `consumed-by: "2026-07-12-siem-requirements-ruled-pack.md…"` | `2026-07-13-siem-fleet-management-requirements-codex.md` |

The two `#14` provenance drafts share their id with the live ACCEPTED ruled pack — deliberate, per
`6551d363`: *"The live folder now holds exactly ONE intake-id 14 (the ACCEPTED ruled pack)."*

### ACCEPTED intakes — consumable candidates for archival?

Per `docs/intake/README.md:179-183`, **ACCEPTED is explicitly NOT terminal and NOT archival**, so
the question "which ACCEPTED docs have landed and could be archived" has a doctrinal answer of
*none — ACCEPTED never routes to archive*. What the schema does track is `disposition`:

| disposition | Count | intake-ids | Un-park condition on record |
|---|---|---|---|
| `active` | 5 | #16, #17, #18, #20, #26 | n/a — being consumed now |
| `deferred` | 3 | #12, #13, #14 | all three carry `trigger: "#328 build"` |

All 8 carry the `decided-by` the schema requires at ACCEPTED, and all 3 deferred docs carry the
`trigger:` the schema requires of a deferral. **Schema conformance on the ACCEPTED set: 8/8.**

**One off-schema key found (reported, not fixed).** `docs/intake/2026-07-21-func-fleet-north-star.md:8`
carries an **empty** `consumed-by:` on a doc whose status is `ACCEPTED`. `README.md:119` scopes that
field *"only when status: CONSUMED"*. The doc's own in-file NOTE (`:11-16`) explains the intent —
§1–§3+§5 were consumed by ADR-109 and §4 by ADR-104, but a doc-level CONSUMED would over-claim
because §6's plan spine is still live. The empty key is a residue of that reasoning, not a status
error. **This is a schema observation, not an archival gap** — the doc is correctly live.

---

## 5. The gap list

Derived from the quoted rules in §1 only. No opinion is expressed about what *should* be archived.

### 5a. ADRs — **gap list is EMPTY**, but the applied rule ≠ the written rule

Under `docs/decisions/README.md:8` (terminal = `Superseded`/`Deprecated`), **zero live ADRs
violate it.** The three live off-enum ADRs (45, 46, 47) are pre-declared carve-outs at
`CONTRIBUTING.md:192-198`, so they are not violations of the stated rule either.

**The finding is upstream of that.** The commit that executed the 2026-07-22 ruling applied a
criterion the written rule does not contain. `216ce3a8` commit body:

> ADR-45 deliberately STAYS (**PLAYBOOK prose refs fail the zero-refs bar**); ADR-46/47
> stay (partially-superseded, retained as convention). Byte-identical moves.

**There is a "zero-refs bar" governing ADR archival, and it exists only in a commit message.**
Neither `docs/decisions/README.md` nor `CONTRIBUTING.md` mentions it. Its premise is live and
verifiable: ADR-45 is referenced from three live PLAYBOOK sites — `protocols/PLAYBOOK.md:3646`,
`:3659`, `:3686` — plus `CONTRIBUTING.md:196-198` and `JOURNAL.md:9049`. So a future session
reading only the written rule would conclude a `Superseded` ADR must move, and would be wrong
whenever live prose still points at it.

**A second, independent divergence on the same ADR.** ADR-45's own status line reads
`Explored, not adopted; ADR-42 v3.2 remains canonical authority for handoff architecture`, while
its README index row `docs/decisions/README.md:34` renders it as
*"~~Handoff Architecture v4 …~~ **Superseded by** 2026-05-13 night minimum-viable refinement
(HANDOFF_PROCESS v3.3)"*. **The index says superseded; the ADR says explored-not-adopted.** This
is precisely the divergence class [#242] is filed to detect, and it is unresolved today.

### 5b. Intakes — **gap list is EMPTY**

Every terminal-status document is in `docs/intake/archive/` (6/6); every live document carries a
non-terminal status (23/23). The rule at `docs/intake/README.md:193-199` is currently satisfied
with zero exceptions. The corpus's own README already names why this cannot be relied on
going forward — *"The move is MANUAL for now — the status-coupled validator that would
gate/automate it is wave work, not built."*

### 5c. Audits — **the gap IS the absence of a rule, and that absence is ruled**

Per the contract's instruction ("if a corpus has no rule, list nothing there and instead name that
as the gap"): **`docs/audits/` has no archival rule, and nothing is listed.** But this is a
*decided* absence, not an oversight — ADR-100 §3 rejected filesystem archival explicitly and gated
any future move behind "a full referential-currency scan **plus** an explicit architect ruling."

The count-tiered index that ADR-100 ruled in its place is **also not built**. `ADR-100:34` requires
*"~20 most recent in the fresh section; older → an archive section of the index"*; the live
`docs/audits/README.md` is grouped **by month**, flat, with all **427** entries (this report
included) in one continuous reverse-chronological list and no fresh/archive split. Whether that satisfies the ruling is an
architect call, not this arc's — recorded as an observation.

### 5d. `docs/archive/` — one rule with a met condition and no recorded action

`docs/archive/README.md:10`: *"If something sits here across two reviews with no decision, default
to deletion."* The file records **one** review (2026-05-28) at `:15`; the 7 files kept "pending
second review" are still present today, 72 days later, alongside 2 that landed after. The second
review has not been recorded. **Naming the condition only** — the disposition is the operator's,
and this arc deletes nothing.

### 5e. Adjacent: the intake scene's own survival metric

`docs/intake/README.md:226-229` (ADR-98 §6):

> - **Survival metric:** intake docs sitting unconsumed after **~1 month of operation**
>   trigger a review of the scene for removal … A folder that only accumulates SEED/DRAFT
>   docs nobody triages has failed the same test a routine fails.

The scene opened 2026-07-07 (intake #4/#5). Today is 2026-08-08 — **~1 month of operation**, and
6 of the 10 SEED docs (#4, #5, #6, #7, #8, #9) date from 2026-07-07/08 and are still SEED.
**The condition for the review is met.** This is *not* an archival rule and is deliberately kept
out of §5a–§5c; it is the intake corpus's only accumulation-control rule, so its trigger firing
belongs in this report.

---

## 6. Doc-currency cross-check (adjacent)

Two dates each, no verdict. `last_reviewed` read from frontmatter; last-commit date from
`git log -1 --format=%ad --date=short -- <file>` on this lane at `3ed60c4c`.

| File | `last_reviewed` | Last commit | Relation |
|---|---|---|---|
| `ARCHITECTURE.md` | 2026-08-07 | 2026-08-07 | equal |
| `VISION.md` | 2026-07-25 | 2026-07-25 | equal |
| `CONTRIBUTING.md` | 2026-08-07 | 2026-08-07 | equal |
| `CLAUDE.md` | 2026-08-07 | 2026-08-07 | equal |
| `protocols/ESSENTIALS.md` | 2026-07-30 | 2026-07-29 | **stamp is 1 day AHEAD of the commit that set it** |
| `LESSONS.md` | *(no stamp)* | 2026-08-03 | n/a — carries no `last_reviewed` |
| `README.md` | *(file absent)* | n/a | n/a |

**Zero files carry a `last_reviewed` older than their last commit.** The P5 relation (stamp
predates last edit) holds nowhere in this set.

Two observations, stated as facts:

- **`protocols/ESSENTIALS.md` carries a forward-dated stamp.** Its last commit is `e0528cc3`
  (2026-07-29), and `git show e0528cc3:protocols/ESSENTIALS.md` confirms the file already read
  `last_reviewed: 2026-07-30` **in that commit** — the stamp names a date one day after the commit
  that introduced it. The A2 check (stamp-predates-edit) cannot fire on a forward-dated stamp; only
  the 30-day A1 backstop applies, and at 9 days it is inside tolerance.
- **`LESSONS.md` and root `README.md` are out of the gated set by construction, not by drift.**
  `CLAUDE.md:66` scopes the stamp to `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS`, matching
  `scripts/canonical_freshness_gate.py:32` + `audit.py:269-271`; LESSONS is append-only and
  deliberately excluded. Root `README.md` **does not exist** — deleted 2026-05-23 per the ADR-38 A5
  amendment, with `CLAUDE.md` §5 item 5 recording *"do not recreate it."* Its absence is the rule
  working.

---

## 7. What this arc did NOT do

- Archived nothing, moved nothing, deleted nothing, edited no status line.
- Filed no BACKLOG row, proposed no convention, wrote no new rule.
- Did not fix the stale [#212] pointer at `docs/audits/README.md:5`, the empty `consumed-by:` at
  `docs/intake/2026-07-21-func-fleet-north-star.md:8`, or the ADR-45 index-vs-status divergence —
  all three are reported for an architect ruling.

## 8. Acceptance-contract self-test

| # | Contract item | Verdict | Evidence |
|---|---|---|---|
| 1 | Every doctrine claim is a QUOTE with a file locator, never a paraphrase | **PASS** | §1 carries 11 block quotes, each with a `file:line` locator; §2 quotes `gen_intake_index.py:6-11` and `216ce3a8`; §5 quotes the commit body verbatim |
| 2 | Mechanism section names a concrete organ or states "none found" with the searches run | **PASS** | §2 states **none found** and enumerates 8 searches with their results |
| 3 | Both censuses use the LIVE frontmatter schema values, and totals reconcile with directory listings | **PASS** | ADR: 83 live + 2 archive = 85, reconciled against `ls` and the 27–110 numbering incl. the ADR-44 gap and 2 amendment files (§3). Intake: 23 live + 6 archive = 29, reconciled against the generated index's own "23 intake documents." and its four group counts (§4) |
| 4 | Gap list is derived from quoted rules only — zero opinions about what *should* be archived | **PASS** | §5a/§5b report EMPTY gap sets against the quoted rules; §5c names the ruled absence; §5d/§5e state met conditions without recommending action. No "should" is asserted anywhere in §5 |
| 5 | Zero moves, zero deletions, zero status edits, zero BACKLOG/row touches | **PASS** | §7; `git status` shows exactly two changed paths — this file (new) and the mandated `docs/audits/README.md` regen |
| 6 | One commit: the report + the mandated index regen; gates passed without `--no-verify`; tree clean at STOP | **PASS** | recorded in the lane packet below |
