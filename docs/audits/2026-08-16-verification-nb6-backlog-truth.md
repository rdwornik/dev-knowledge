# NB6-B — batch-6 backlog truth verification, and the batch-7 morning queue

- **Class:** verification (ADR-101 R3 enum) · **Date:** 2026-08-16 · **Slug:** `nb6-backlog-truth`
- **Status: DRAFT — this report verifies and proposes. It rules nothing, closes nothing, births no
  row, and edits no BACKLOG line.** Read-only lane; the only files it adds to the tree are this
  report and the regenerated `docs/audits/README.md` index. Landed on
  `claude/batch-6-backlog-verify-s767wm` — the session's harness-designated branch — rather than the
  `claude/nb6-backlog-truth` name the brief used; stated here so the lane is locatable by the ref
  that exists.
- **Tree under test:** `main` @ `88422f5c` (*"Merge branch 'docs/batch6-close' — batch 6 closes"*),
  the tip that carries the batch-6 closing packet.
- **Subjects:** `docs/audits/2026-08-16-technical-batch-6-packet.md`,
  `docs/audits/2026-08-16-technical-batch-6-manifest.md` (+ AMENDMENTS 1 and 2),
  `JOURNAL.md` entries `2026-08-16 (b)`–`(f)`, and `tasks/` + `tasks/manifest.json` as the
  source of truth `BACKLOG.md` is generated from.

**Method.** Every claim below was re-derived from the live tree with a script or a gate, not read
off the artifact that asserts it. Where a claim could not be checked from this container, it is
marked UNVERIFIABLE-HERE with the reason rather than passed. Where this report quotes an **unmerged**
night-lane report (§1.7), the substantive claim was re-verified against the live tree before use —
**nothing quoted from an unmerged branch binds anything.**

---

## §1 · Verdict table — 31 claims checked, 26 verified, 4 mismatches, 1 not reproduced

| # | Claim (source) | Verdict | How it was checked |
|---|---|---|---|
| 1 | 29 Done-when conversions landed across lanes a–g (packet "Rows") | **VERIFIED** | Roster arithmetic a4 b3 c4 d5 e4 f4 g5 = 29, 29 distinct ids, 29 task files present |
| 2 | Each of the 29 carries a Done-when clause | **VERIFIED** | Regex extraction of `· Done when:` from each `tasks/<id>-*.md` body — 29/29 present |
| 3 | Each of the 29 clauses actually changed in this batch | **VERIFIED** | Clause diffed against `43cd1cee` (the dispatch base): 29/29 differ, 0 unchanged |
| 4 | The conversions are structurally well-formed (no unhomed Form-E escape) | **VERIFIED** | Swept all 29 for *"recorded …-with-reason"* with no named home: **0 hits** |
| 5 | Conversion closes zero rows by design | **VERIFIED** | All 29 ids still live in `tasks/manifest.json` |
| 6 | Conversion preserves each row's intent | **MISMATCH** | `[#417]`'s conversion replaced a **satisfied** clause with an unsatisfied one. See §1.8 |
| 7 | Form-E predicate repair applied to `[#409] [#410] [#411]` | **VERIFIED** | All three carry the repaired two-branch predicate; none is heading-named in `STANDING_RULINGS.md` |
| 8 | `[#415]`/`[#425]` AFFECTED, verify-only, owed | **VERIFIED** | Live measurement: exactly **2** rows whose Form-E escape is already satisfied by an existing `###` section — and they are precisely `[#415]` and `[#425]` (both via `### L-8` and `### M-7`) |
| 9 | `[#502]` NOT affected | **VERIFIED** | `[#502]` carries no `STANDING_RULINGS` escape branch at all |
| 10 | `[#524]` closed | **VERIFIED** | `tasks/524-*.md` → `status: closed`; absent from manifest |
| 11 | `[#352]` closed | **VERIFIED** | `status: closed`; absent from manifest |
| 12 | `[#527]` closed | **VERIFIED** | `status: closed`; absent from manifest; closed at `e123947` (Position 0, after baseline `ce1dade1`) |
| 13 | `[#532]` closed | **VERIFIED** | `status: closed`; absent from manifest; restored at `3def2821` after the resolver revert |
| 14 | `[#364]` retired | **VERIFIED** | `status: retired`; absent from manifest; retired `e9482bf` 2026-08-15, an ancestor of the batch-6 baseline |
| 15 | Manifest **coherence** — no closed row left as a live node | **VERIFIED** | Set difference both ways over 196 manifest nodes vs 267 task files: **0 mismatches in either direction** |
| 16 | Manifest **correctness** — the resolver-revert class is extinct | **VERIFIED** | Full-history sweep of every close-claiming commit against live status. **0 surviving instances.** See §1.5 |
| 17 | `BACKLOG.md` is in sync with its source | **VERIFIED** | `gen_task_tree.py --check` → `check ok`; `generated_sha256` matches the live file byte-for-byte |
| 18 | `[#533]` carries a dated PARTIAL marker, NOT closed | **VERIFIED** | `status: open` + **PARTIAL 2026-08-16 (batch-6 lane m)** in the row body |
| 19 | `[#533]` "16 of 43 extracted" | **VERIFIED** | 16 `check_*.py` modules under `scripts/audit_checks/`; `CHECK_ORDER` has 43 entries; 27 held |
| 20 | `[#533]` "`audit.py` 5243 → 4270 lines" | **VERIFIED** | `43cd1ce`=5243, `f84b4d8`/`d714cfe`=4270. (Live is 4271 — wrap act (i) at `86e1693` added one line *after* the measurement; the row's claim is correctly SHA-scoped) |
| 21 | `[#533]` follow-on leg 1 (seam re-point) recorded | **VERIFIED** | "FOLLOW-ON LEG, ruled 2026-08-16 for batch 7" present in the row |
| 22 | `[#533]` leg 2 (parallel + `lru_cache`) recorded | **VERIFIED** | "**LEG 2 (batch 7, ruled 2026-08-16)**" present, carrying the I/O-bound measurement |
| 23 | `[#293]` is BLOCKED-ON-RULING | **VERIFIED** | Row is `status: open` and carries "**Row now BLOCKED-ON-RULING:**" with the two `[#303]` candidate homes named and no path invented |
| 24 | `[#529]` row state matches reality | **VERIFIED** | All four recorded open legs still open: `logs/TELEMETRY.db` is **not** git-ignored; `structlog` is absent from `pyproject.toml` and `uv.lock` |
| 25 | `[#530]` row state matches reality | **VERIFIED** | Both recorded defects latent — `single_flight` appears in no hook config |
| 26 | `[#531]` row state matches reality | **MISMATCH** | Row still reads "THIRD OCCURRENCE". Batch 6 was the **fourth**, and the worst. See §1.1 |
| 27 | Live open-total = 196 | **VERIFIED** | 172 `open` + 24 `deferred` = 196; `validate_backlog` independently reports `196 tasks`. But see §2.1 on how the wrap describes it |
| 28 | Untestable denominator = 29 | **MISMATCH** | The arithmetic omits `[#364]`. Corrected chain gives **28**; the *measured* figure is different again. See §2.2 |
| 29 | 2 owned REDs; ARM 1 fires on `BACKLOG#428` | **MISMATCH** | The ARM-1 characterisation is wrong — there are **two** loci. See §1.3 |
| 30 | The `routine_consumers` RED is inherited; nothing in this roster could clear it | **VERIFIED** | Detector run against the pre-batch and post-batch `BACKLOG.md`: **2 declared rows both times**. The alternative hypothesis was tested and rejected. See §1.9 |
| 31 | D-A's three `[#533]` oracle pins were re-pointed correctly | **VERIFIED** | Test run live: the `scripts/audit_checks/_common.py` + line-30 assertions **pass** on both a parallel and a serial run |
| 32 | The third RED "fails at 16 xdist workers and **passes serially**" | **NOT REPRODUCED** | Run serially (`-n 0`), alone, on this host it still fails — `assert 0 >= 50` at the 40s timeout. See §1.9 |

**Also verified, outside the numbered claims:** the 15 nightly-triage GitHub Issues
(`#19 #21 … #47`) are **all CLOSED** and `rdwornik/dev-knowledge` currently has **0 open Issues**;
all 18 SHAs the packet cites resolve, and every one it calls a merge has 2 parents;
`batch_manifest.open_batches('.')` → `[]`, so the ADR-110 exemption is genuinely expired;
`gen_audit_index.py --check`, `generate_organ_index.py --check` and the ADR-53 `file-budget`
check on `CLAUDE.md` all pass.

**UNVERIFIABLE-HERE (stated, not passed):** the packet's teardown state ("twelve worktrees and
twelve lane branches intact"), the "no `--no-verify` / no `SKIP=`" claim, and the full-suite verdict.
This container is a fresh clone with one worktree. **The uv trap was hit and then discharged — see
§1.10 — so the tests named in §1.9 WERE run**; the full suite still was not, and teardown and the
`--no-verify` claim remain operator-host facts.

---

### §1.1 · MISMATCH — `[#531]` records three occurrences; batch 6 was the fourth, at 12 of 12

`tasks/531-*.md` has been edited exactly once, at its birth (`e6ee9a1`), and still reads:

> THIRD OCCURRENCE: batch-4 W4/W6 …, batch-4 `lane-a-514-lane-regex`, and batch-5 lanes S … + R …

Batch 6 is a fourth occurrence and a categorically worse one. AMENDMENT 2 of the batch-6 manifest
records it in full — `claude --worktree <name>` doubled the prefix, so **0 of 12** branches matched
`LANE_BRANCH_RE` at creation — and closes with the sentence that belongs in the row:

> `[#531]`'s gate would have refused all twelve of these names at creation had it been armed.

**Corroborated independently.** NB4-C's coverage matrix reaches the same tally from the PLAYBOOK
side, naming lane grammar as one of its two WORST rows: *"3 consecutive batches damaged (b4 dropped
2 lanes, b5 forfeited the exemption on 2 of 7, b6 had to verify 12 names by hand against the
regex)"*. AMENDMENT 2 shows batch 6 was worse than NB4-C knew — the hand verification ran against
the names the roster *intended*, not the names git produced.

The strongest live evidence the row could carry is therefore in the manifest and not in the row.
The row is the artifact a batch-7 lane boots from; the manifest amendment is not. **Repair is one
appended sentence**, and the row is already 2067 chars against the ARM-2 ceiling of 1320 (§1.4), so
the append should be a locator, not a retelling.

### §1.3 · The doc_rot ARM-1 RED has **two** loci; every artifact names only one

The packet, and JOURNAL `(d)`, `(e)` and `(f)`, all characterise the second owned RED as ARM 1
firing on `BACKLOG#428` alone:

> `test_live_corpus_has_no_accretion_arm_findings_only_length_findings` — ARM 1 correctly fires on
> `BACKLOG#428` (3 dates spanning 52d).

Run live on this tree, `validate_doc_rot.scan(.)` returns **two** `backlog-accretion` findings:

```
BACKLOG#428   3 history dates spanning 52d, 2030 chars
BACKLOG#293   4 history dates spanning 40d, 2864 chars
```

`BACKLOG#293` is lane k's row — the one this batch set to BLOCKED-ON-RULING. Its own append pushed
it over the same ARM-1 threshold, at a *wider* date span and a *larger* body than `#428`.

This does not change the RED/GREEN verdict (the test asserts `== []`, so it fails on either count),
and it does not weaken the packet's conclusion that ARM 1 is behaving correctly — it strengthens it,
by a second independent hit. What is wrong is the **characterisation**: the disposition owed for this
RED is scoped to one row in every artifact, and it covers two. A `[#428]`-only remedy leaves the
test RED.

### §1.4 · Unrecorded consequence — 8 of the 29 conversions crossed the ceiling this batch declared

`[#532]` shipped ARM 2 with a **declared ceiling of 1320 characters**. The wrap commit for the
Form-E repair explicitly guarded against reddening it: *"the repair script REFUSES if a row would
cross 1320 — a repair that reddened the detector lane x just armed would be self-defeating."*

The seven conversion lanes carried no such guard. Measured, pre-batch vs post-batch, same rows:

```
rows pushed OVER 1320 by their own conversion:  8 of 29
  #361 1061->1331   #146 1135->1323   #443 1163->1370   #484 1113->1374
  #502 1187->1390   #271  983->1364   #412 1178->1389   #417 1066->2360
one row shrank below it:                        #419 1908->1264
```

Corpus-wide, applying the new ceiling retroactively to the pre-batch `BACKLOG.md`:

```
rows over 1320   pre-batch  10
rows over 1320   post-batch 19        net +9
newly over: 146 271 277 293 361 412 417 428 443 484 502   (11)
no longer over: 419, 532                                   (2)
```

The batch **nearly doubled the ARM-2 finding count on the ceiling it itself declared**, and no
artifact records the number. The manifest carefully lists "Known carried WARNs at baseline … `doc_rot`
9 loci" so later readings are attributable; there is no post-batch counterpart, so the next reader
has nothing to attribute 21 findings against. This is a cost of a real trade — conversion buys
verdictability with length — but the trade is currently unpriced.

Two of the batch's own births are also over: `[#531]` at 2067 and `[#533]` at **4210**, the largest
in the corpus. The wrap entry states `[#533]`'s size honestly and gives its reason; the conversion
crossings are not stated anywhere.

### §1.5 · The detector gap the packet names would currently find nothing — which is the good news

The packet proposes a detector-gap candidate:

> `gen_task_tree --check` needs a closed-in-history-vs-open-in-manifest leg — nothing compares the
> tree against its own history.

That sweep was built and run here across the **entire** history: every commit subject asserting a
close/retire/kill of a `[#id]`, cross-checked against that row's live status.

```
close-claiming (sha, row) pairs in history : 29
rows so claimed                            : 16
  #532 #527 #352 #524 #513 #525 #508 #360 #452 #132 #521 #270  -> all non-live  OK
  #277 #428 #310 #511                                          -> false positives, see below
surviving resolver-revert instances        : 0
```

The four apparent hits are regex false positives on the verb, not the row: `#277`'s commit closes
*15 GitHub Issues*; `#310`/`#428` matched on the literal `kill-candidates:`; `#511`'s subject closes
*an ADR-112 gap* and separately records that a **split** was deferred. Each was read and dismissed
on its text.

**So the class is extinct in the current tree.** The proposed detector would land green — which makes
it a regression guard rather than a cleanup, and means it can be built at leisure with no backlog of
violations to dispose of first. Worth saying explicitly, because a detector proposed after an
incident is usually assumed to have work waiting behind it.

### §1.6 · The repaired Form-E predicate introduces a term nothing defines — including its own source

The repair replaced *"ruled out in `STANDING_RULINGS.md` in a section naming `[#NNN]`"* with:

> … by a `###` section whose heading names `[#409]`, **or by a line where `[#409]` carries a
> disposition token**

Branch 1 is sound and measurably so: only ids `294 308 360 396 511 512 513` are named in any `###`
heading, and `[#409]`/`[#410]`/`[#411]` are not among them.

Branch 2 is not yet checkable. **`disposition token` occurs nowhere in the repo except inside the
three rows that introduce it** — no definition, no enumeration, no validator. It is not defined in
its source either: NB4-E uses the phrase exactly once, in its recommended repair
(*"a body line of the form `[#NNN]` **followed by a disposition token**"*), with no glossary line
anywhere in that report. And the nearest live candidate sits on the exact line the ruling cited as
the defect:

```
STANDING_RULINGS.md:1353
  - **Fold set A (`[#409]`/`[#410]`/`[#411]`) and fold set B (`[#415]`/`[#425]`) — NIE, both.**
STANDING_RULINGS.md:1440
  draft's own instruction · `TAK` / `NIE` accept / decline as drafted.
```

`NIE` is the register's own declared decline token, and line 1353 is a line on which `[#409]`
appears. A careful reader resolves this correctly — the `NIE` disposes of the *fold*, not the *row* —
but that is precisely the judgement the mechanical form exists to remove. Note also that the shipped
wording (*"carries"*) is looser than NB4-E's recommendation (*"followed by"*), which was positional.
**Honest limit on this finding:** it is an interpretation gap, not a demonstrated false satisfaction;
nothing has yet claimed the branch is met. The cheap fix is to enumerate the accepted tokens where
the predicate names them.

### §1.7 · The authority the wrap cites does not resolve in-tree

Wrap act (vi) is attributed to **NB4-E**, and the commit's trailer reads `refs NB4-E, …`. `NB4-E`
has **zero occurrences** anywhere in `docs/`, `protocols/` or `JOURNAL.md`.

It is not missing — it is unmerged. Every night-4 and night-5 lane report is sitting on `origin`
with no path into `main`:

```
claude/nb4-llm-acceptance-benchmark-pnoo2q   docs/audits/2026-08-16-technical-nb4-llm-acceptance.md
claude/nb4-telemetry-read-path-ivoka2        docs/audits/2026-08-16-technical-nb4-telemetry-read.md
claude/nb4-playbook-gap-coverage-1ktsuc      docs/audits/2026-08-16-verification-nb4-playbook-gap.md
claude/nb4-equilibrium-audit-el1o0w          docs/audits/2026-08-16-verification-nb4-equilibrium.md
claude/nb4-closing-campaign-prep-gb68l0      docs/audits/2026-08-16-census-nb4-closing-campaign.md
claude/nb4-scaleout-substrate-f8fhi1         docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate{,-v2}.md
claude/nb4-consolidated-ychsah               docs/audits/2026-08-16-technical-nb4-consolidated-briefing.md
claude/adr-104-fleet-parity-audit-f1lr7a     docs/audits/2026-08-16-technical-nb4-fleet-parity.md
claude/nb5-seam-repoint-analysis-lmaspu      docs/audits/2026-08-16-technical-nb5-seam-repoint.md
claude/consumer-home-adr60-audit-xd341y      docs/audits/2026-08-16-technical-nb5-consumer-home.md
```

**Ten reports, eleven files, none in `main`.** The precedent exists and is one day old — JOURNAL
`2026-08-16 (a)` landed *"the five night-3 lane reports … byte-faithful"* as its own arc. The
batch-6 packet's "Owed" list does not carry this one, which is how it became invisible.

The consequence is not bookkeeping. A batch-7 lane booting from `main` cannot read NB4-E, cannot
read NB4-C's paste-ready PLAYBOOK drafts, cannot read NB4-E's campaign plan — and cannot read nb5-A,
which contains the finding that most changes what batch 7 should do (§3 Q2).

### §1.8 · MISMATCH — `[#417]`'s conversion replaced a met clause with an unmet one, and its new locator is already dead

This is the sharpest finding in the report, and the only one where the batch's work moved a row
*backwards*.

**Before** (at the dispatch base `43cd1ce`):

> · Done when: the dirty-tree leg ignores tool-owned writer-isolated paths **with a test**, or the
> exclusion is recorded rejected with a reason

**That clause is met on `main` today** — verified live here, independently of the report that
claims it:

```
scripts/session_end_backpressure.py:375   _LANE_DAILY_RE = ^ecosystem/[^/]+/history/[^/]+$
scripts/session_end_backpressure.py:402   _is_lane_owned_daily()
scripts/session_end_backpressure.py:412   check_dirty_tree()
scripts/session_end_backpressure.py:418   changes = [ln for ln in changes if not _is_lane_owned_daily(ln)]
tests/test_session_end_backpressure.py    exclusion tested in BOTH directions
mechanism landed at 3b711e8 (batch-4 GO, 2026-08-11)
```

**After** (lane f's conversion, merged `8e8d55a2`):

> · Done when: the `history_specs`/`pathspecs` scope list at `_commit_routine_outputs`
> (`scripts/audit.py:4751-4760`) is extracted into a location shared with `check_dirty_tree`'s
> exclusion scope, narrowed to …

That is a **code refactor that has not happened**. A row that was closeable on live evidence is now
open on a new, unmet condition — and the row grew 1066 → 2360 chars doing it, the largest ARM-2
crossing of the batch (§1.4).

**And the new locator is already dead.** A sweep of every live row for a `path:line` citation past
end-of-file returns exactly one row: `[#417]`. `scripts/audit.py` is 4271 lines and
`_commit_routine_outputs` is now at `:3759` — the same batch's own decomposition invalidated the
locator its own conversion had just written. The D-A ruling swept the three `[#533]` **test** pins
after the decomposition; nothing swept the **row** locators.

**The decision that should have caught this expired by default.** The NB4 consolidated briefing put
this exact fork at the head of its queue as precondition **D0.1** — *"`[#417]` vs lane f — close it
or let lane f convert it"* — and noted both D0 preconditions *"expire when a lane integrates."* Lane
f integrated. Nothing records which branch was taken or why, so the fork was resolved by scheduling
rather than by ruling.

There is an irony worth preserving, because it is the general lesson: NB4-E's own footnote explains
that the census missed `[#417]` because the row's `refs` pin had rotted
(*"`:340-349` is now `check_backlog_marker`, a different function entirely"*) — and the conversion
then wrote a fresh locator that rotted inside the same batch. **Line-number locators in row bodies
rot faster than the rows do.**

*(Note for the record: NB4-E cites `4bef950` as where the `[#417]` mechanism landed. That SHA is the
2026-08-09 intake-#25 ratification merge and touches nothing relevant. The cited SHA is wrong; the
substantive claim is right, and is re-verified above from the live tree rather than accepted.)*

### §1.9 · The three REDs, run live — one claim confirmed against its alternative, one not reproduced

Once the uv trap was discharged (§1.10) the three tests the packet names became runnable. All three
were run.

**`routine_consumers` — the packet is right, and this is the stronger form of right.** The packet
calls it *"batch-7 lane l's named subject; deferred by D-1v2, so nothing in this roster could clear
it."* There was a live reason to doubt that: lanes a and g converted six rows (`#409 #410 #411`,
`#271 #324 #391`) whose new clauses all mention the ADR-105 `· routine:` marker, taking rows
carrying that string from 2 to 8. If any had registered as a *declared* routine, the batch would
have moved the number the test pins, and the RED would be partly the batch's.

Measured by running the detector against the pre-batch and the post-batch `BACKLOG.md`:

```
PRE-batch 43cd1ce   pass   2 declared routine row(s) name a consumer and a consumption_path
NOW       88422f5   pass   2 declared routine row(s) name a consumer and a consumption_path
```

**Unmoved.** The detector strips inline-code spans by design — *"a row quoting the marker stays a
proposal"* — so six conversions that name the marker in backticks correctly register as nothing. The
inherited-RED claim survives a test that could have falsified it, which is worth more than an
unchallenged pass.

**D-A's oracle re-point is correct.** Both runs pass
`res["definition"]["file"] == "scripts/audit_checks/_common.py"` and `["line"] == 30`. The ruled
layout re-point did what it claimed.

**The third RED's triage does not reproduce.** The packet states it *"fails at 16 xdist workers
(`assert 3 >= 50`) and **passes serially** — the pyright oracle returns partial results under
contention within its 40s timeout."* Run here with `-n 0`, as the only test, with no contention of
any kind:

```
assert 0 >= 50        1 failed in 40.69s
```

Zero reverse dependents, not a partial 3, and the run consumed the full 40s budget. **Stated
carefully, because this is a different machine:** the failure is still plausibly environmental — a
40s oracle timeout on a slower host is an environment fact, not a defect. What does not hold is the
*mechanism* and the *evidence*. The trigger is not xdist contention specifically, and "passes
serially" is a single-host observation that fails on the second host anyone tried it on. A
disposition resting on it is weaker than it reads, and the durable fix is a timeout the oracle
reports rather than absorbs.

### §1.10 · The uv trap is discharged by a route the reports name but never tested

Both Stop-hook firings in this session failed with NB4-E's trap 3 — `uv` pinned to `0.11.19`, image
ships `0.8.17`. That is a **third variant** beyond what the reports document: NB4-E catalogues the
trap breaking *commands*, and the consolidated briefing's AMENDMENT 1 measured that on its image no
`0.11.19` binary exists *"anywhere on the filesystem, shadowed or otherwise"*. Here it disarmed a
**hook** — the gate returned an error instead of a verdict, so a session trusting the wrapper's exit
would have ended with session-end backpressure never evaluated. Run directly under plain python the
same script exits **0, clean**; only the wrapper was broken.

The briefing's surviving remedy — *"obtain uv from a source other than its own updater"* — was never
tested. It works, and the measurements are worth recording because they narrow the trap:

```
uv self update 0.11.19   ->  error: The version 0.11.19 was not found for the app uv
                             in workspace uv          (the updater's own channel cannot serve it)
PyPI /pypi/uv/json       ->  0.11.19 present: True    (latest 0.12.5; the PIN IS SATISFIABLE)
pip install uv==0.11.19  ->  /usr/local/bin/uv, 0.11.19, works
uv run --locked ...      ->  session_end_backpressure.py  EXIT 0
```

So the pin is not wrong and the version is not missing upstream — **`uv self update` is the wrong
source, and it is the source the error message itself recommends.** A preflight that shells `uv self
update` will fail forever on this image while a `pip install uv==<pin>` succeeds. `/root/.local/bin`
still precedes `/usr/local/bin` on `PATH`, so the shadowing `0.8.17` continues to win for bare `uv`;
un-shadowing it was not attempted here (it is an environment mutation outside a read-only lane's
remit, and it is unnecessary once the pinned binary can be named explicitly).

That is the concrete content the un-owned preflight fix needs, and no row owns it.

---

## §2 · Re-derived denominators

### §2.1 · Live open-total: **196 = 172 `open` + 24 `deferred`**

Three independent routes agree on 196: task nodes in `tasks/manifest.json`; `tasks/*.md` whose
frontmatter `status` is `open` or `deferred`; and `validate_backlog.py`'s own `196 tasks`.

The arithmetic across the batch also closes exactly:

```
195   night-3 sessionplan baseline (171 open + 24 deferred, 2026-08-15)
+3    births   [#531] [#532] [#533]
-2    closes   [#527] (Position 0) · [#532] (lane x)
=196
```

**One wording defect worth fixing at the next re-derivation.** JOURNAL `2026-08-16 (e)` writes
*"against a live denominator of **196** open rows"*. 196 is not the open count; it is open **plus**
deferred. The night-3 sessionplan states the same quantity correctly — *"195 rows (171 open + 24
deferred)"* — so the two phrasings now disagree in the record about what the number counts. Given
that this batch was bitten twice by stale numbers, and that two denominators in circulation is the
defect I-D6 exists to end, the decomposition is worth carrying every time the total is quoted.

### §2.2 · Untestable denominator — the reported 29 is one correction short, and the measured figure is different again

**The reported chain.** JOURNAL `(e)`: `58 − 29 = 29 remaining`.

**The chain the plan asked for.** The night-3 sessionplan named **three** staleness counts, not one:

> The `58` baseline is now stale on at least three counts: `#364`'s retirement, the `#529`/`#530`
> births, and the 29 conversions themselves.

Only the third was applied. `[#364]` is graded **PROSE-CONVERTIBLE** in the census
(`| [#364] | P3/S | PROSE-CONVERTIBLE | N | audit-py | …`), it was **not** converted by wave 1 — its
only edit in the whole 08-12→08-15 window is its retirement at `e9482bf` — and its Done-when still
reads *"…or the constraint is recorded as accepted-with-reason"*, the unhomed escape that put it in
the 95 in the first place. It was in the 58, and it left the live set. So:

```
58  −1  (#364 retired)  −29 (conversions)  =  28
```

`[#529]` and `[#530]` both read MECHANICAL as written (each names its tests and its store/ref
predicate), as do the batch's surviving births `[#531]` and `[#533]`, so the births add **+0**.
**The corrected arithmetic figure is 28, not 29.**

**The measurement the plan actually asked for** (*"Re-measure the untestable count properly … this is
the one close-out item where the measurement matters more than the work"*) was not attempted — the
wrap carries O-3's honest limit forward instead. It can be done, and here it is: every one of the
census's 95 untestable rows resolved against the live tree, by status and by whether its Done-when
clause has been rewritten since the census landed (`3b711e87`).

```
census untestable                                     95   (72 PC + 15 PJ + 8 DEFECTIVE)
  no longer live                                       6   #132 #360 #364 #452 #508 #513
  still live, Done-when REWRITTEN since census        72   (68 PC + 4 DEFECTIVE)
  still live, Done-when UNTOUCHED since census        17   (15 PJ + 2 DEFECTIVE: #241 #359)
```

Two things fall out, and both matter more than the ±1:

**(a) The PROSE-CONVERTIBLE stock is exhausted — 0 rows remain.** All 72 census PC rows have either
left the live set (4) or had their clause rewritten (68). And **68 = wave-1's 39 + wave-2's 29
exactly**, which independently confirms both wave counts from the clause text rather than from the
lane reports. **There is no wave-3 conversion lane to cut.** This is the single most consequential
number in this report for batch-7 planning, and §4 is built on it.

**(b) A 38-row ungraded overhang now sits under the number.** 34 live rows were **born after the
census and have never been graded at all** — 17% of the live set:

```
4 19 102 117 139 144 166 169 181 188 190 218 231 240 294 300 301 305 308 310
322 325 492 494 495 499 522 523 526 528 529 530 531 533
```

plus the 4 DEFECTIVE rows whose clause changed (`#170 #369 #383 #505`), where "changed" does not
establish "now mechanical" — the census's verdict on DEFECTIVE was that intent is unrecoverable.

**Name the three numbers separately rather than quoting one.**

```
measured floor, from the graded set     17   (15 PROSE-JUDGMENT + 2 DEFECTIVE, clauses untouched)
+ O-3's two post-census filings          2   ([#526] [#528])
= measured, defensible                  19
arithmetic estimate, corrected          28   (58 − 1 − 29)
ungraded overhang                       38   (34 never graded + 4 DEFECTIVE-changed)
live denominator                       196   (172 open + 24 deferred)
```

The reported **29** sits inside that band but is neither endpoint. The 15 PROSE-JUDGMENT rows are
the honest hard core — the census's own rule is that they need a **decision**, not a rewrite, so no
conversion lane can touch them:

```
#43 #122 #126 #153 #281 #323 #397 #400 #406 #407 #420 #449 #450 #488 #507
```

---

## §3 · Morning priority queue — batch-7 candidates ordered by unblock-value

Ordering rule: what unblocks the most downstream work per unit of effort, with hard preconditions
respected. Sizes are the row's own `[S]`/`[M]` where one exists, else this report's estimate marked
*(est.)*.

### Q1 · Land the ten night-4/night-5 lane reports — **S, ~30 min, blocks 4 of the 9 items below**

**Why first, and why it is not bookkeeping.** Q2, Q5, Q7 and Q8 each boot from a report that is not
in `main` (§1.7). A lane cannot cite what it cannot read, and the wrap already shipped one act
citing `NB4-E` as authority with nothing in-tree behind it. This is the cheapest item on the list
and it is upstream of the four most valuable ones.

**Depends on:** nothing. **Unblocks:** Q2, Q5, Q7, Q8. **Shape:** the JOURNAL `2026-08-16 (a)`
precedent — merge byte-faithful, regenerate `docs/audits/README.md`, one JOURNAL anchor. **Do not**
rule on any content while landing it; all ten are DRAFTs that bind nothing, and one
(the consolidated briefing) already carries an AMENDMENT withdrawing its own §0 X1 remedy.

### Q2 · `[#533]` seam leg — **M, and it must ship the test split (nb5-A "6b"), not just the source move**

**This is the highest-value technical item, and its recorded shape is wrong.** `[#533]`'s FOLLOW-ON
LEG says *"re-point the `tests/test_audit.py` monkeypatch seams so class (1) unblocks"*. nb5-A
(unmerged, `f8a8357`) independently reproduced lane m's 25-of-43 count from the live tree **and
rejected its conclusion**, with a working prototype:

> The 25 checks are not unmovable, and the two that matter are the cheapest of them. … it reaches
> **byte-identical `audit.py health` output**, preserves `ALL_CHECKS` order and count (43), and lands
> on **exactly the baseline test result — 5 failed / 249 passed, the same 5 named failures — with
> ZERO test-file edits**.

So no seam *re-pointing* is required for the source move. The fix is *"one ~12-line accessor per
extracted module, plus mechanical `X` → `_f().X` rewriting of seam references inside the moved
body."* Measured diff for the two checks that matter: `scripts/audit.py −132/+15`, two new modules
(84 and 119 lines), **one existing file touched**, k=4 files.

**But the source-only diff does not unblock lanes l and y**, which is the whole point of the leg:

> The test half is not gone, and 6a alone does not clear it. `check_hooks_armed`'s five tests live at
> `tests/test_audit.py:1976–2052` … the residual collision is **precisely and only** the `hooks_armed`
> block. … **6b clears it.** … If lane m ships 6a only, the batch-7 matrix will re-refuse the same
> pair. That is the single most consequential recommendation in this report.

Verified live on this tree: `check_hooks_armed` (`scripts/audit.py:984`) and `check_stale_worktrees`
(`scripts/audit.py:891`) are **both still inline in the facade**; the decomposition touched neither.
**The D-1v2 collision is live and unchanged; batch 7 reproduces batch 6's refusal unless this leg
runs first.**

**What it unblocks, exactly:**

```
27 checks held today
 25  class 1 (monkeypatch closure seam)  -> UNBLOCKED by this leg
  1  class 2  check_handoff_probes  (_gitenv position-dependent)      -> separate ruling item
  1  class 3  check_import_edges    (N-1 landing predicate names audit.py) -> separate ruling item
after the leg: 41 of 43 extractable, 2 held, each with a named owner
```

**Depends on:** Q1. **Unblocks:** lanes l and y, the `[#533]` continuation, and Q3. **Cost of
skipping:** batch 7 loses two lanes to the same collision that cost batch 6 two lanes.

**One thing this leg should file and nb5-A deliberately did not.** nb5-A found a **silent** defect —
the dual-import idiom creates two live `audit` module objects, and *"eleven tests silently stop
testing anything."* It is pre-existing and already triggered today by
`scripts/enforcement_coverage.py:565` (`from scripts import audit as _audit`, verified live). nb5-A
states it does not fix it and files no row. **No row owns it.** A silent eleven-test hole outranks
most of this queue on severity and belongs in front of the architect as a birth candidate, not
folded into `[#533]`'s scope.

### Q3 · `[#533]` continuation — the 25 newly-unblocked checks — **M *(est.)*, strictly after Q2**

Mechanical once Q2 lands, with byte-comparison as the proof. nb5-A's sequencing proposal: Wave 0
(18 free) → Wave 1 (hooks_armed + stale_worktrees, **must** include the test split) → Wave 2 (9
low-site) → Wave 3 (`journal_spine_anchor` last). nb5-A's stated limits apply: it prototyped **3**
checks, not 43; `check_doc_claims` was not prototyped; its baseline was a cloud clone where 114 of
2886 tests fail for environment reasons, so the lane must re-establish its own baseline first.

### Q4 · `[#533]` leg 2 — parallel execution + `journal_anchor` `lru_cache` — **M, after Q3**

The measurement condition is already discharged in the row: `audit.py health` is **I/O-bound**
(~2 min CPU per ~5 min wall at 8% load), so `ThreadPoolExecutor` is indicated and the ruling's
`ProcessPoolExecutor` condition is not met. The `lru_cache` half is separable and carries its own
measured payoff (~42.7s → ~17.8s per commit).

**Why it ranks here and not lower.** Lane m's throughput note, carried verbatim into JOURNAL `(e)`:
*"Eleven lanes running whole-repo `audit.py health` concurrently was the real cost driver:
**25-40 min wall-clock per gated commit**."* At batch-6 widths this is the binding constraint on how
wide a batch can go. It sits behind Q3 only because it wants the decomposed registry underneath it.

### Q5 · `[#293]` home ruling — **architect act, S, unblocks the only BLOCKED-ON-RULING row**

nb5-B (unmerged, `85e41b3`) derives three candidate homes from live governance and recommends one:

> **Recommend H1: the consumer-side home for hub-runbook guidance is `CONTRIBUTING.md` →
> `## Handoff process`, and no runbook file is seeded into any consumer.** … `[#293]`'s fan-out is
> **not-applicable-by-construction**, not deferred.

H1 rests on `CONTRIBUTING.md` existing in all three verified consumers, being required by
`scripts/audit.py:1326` and freshness-gated at `canonical_freshness_gate.py:32-33`. Runner-up is
**H3** (`.claude/`, the only mechanically proven hub→consumer carrier), explicitly *not* H2
(consumer `protocols/`), because `corp-sca-time-automation` has no `protocols/` directory and H2
would force the one-member surface ADR-101 ruled against.

**One of nb5-B's stated gaps has closed since it was written** (it was cut from `43cd1ce`, before the
batch landed): it flags *"It does not recover the lane-k packet, which is absent from the hub
remote"* — the packet **is** in `main` now, at
`docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md`. Still genuinely owed:
per-repo verification for the 5 fleet members nb5-B could not reach, before the ruling generalises.
NB4-F reaches the same place from the other side: *"`[#303]` is the prerequisite, not a sibling"*,
with seeding-readiness **0 of 8** on two independent grounds.

**This is an architect decision, not a lane** — cheap, decision-ready with a recommendation and a
runner-up, and it unblocks the only row in the corpus currently BLOCKED-ON-RULING.

### Q6 · `[#492]` browser re-check — **XS, dated 2026-08-17 — do not do it today**

The row's peg is explicit: **RE-CHECK 2026-08-17**, a dated re-check of an external fact (the Grok
4.6 release). Today is Sunday 2026-08-16. The night-3 sessionplan already ruled on the temptation:
*"do not move the date and do not treat a Sunday check as discharging a Monday commitment."* The NB4
consolidated briefing independently flags it as falling due tomorrow under its **D1**. Listed here so
it is not lost, with the note that **no organ watches it** — it needs a human tomorrow.

### Q7 · Closing campaign — **ratification first; and it is much smaller than the name suggests**

STANDING_RULINGS **L-3** establishes the campaign is owed and constrains it:

> A dedicated closing campaign is owed, named in the windows-3–8 sequence. … Re-scoping the number is
> available only on evidence … **two or more windows of net closure data**.

NB4-E supplies the instrument and says plainly that it *"prepares the campaign, does not open it,
zero closes executed."* Its actual shape, which is worth knowing before the item is sized:

```
NOW-CLOSABLE            2 rows (1.0%)  ->  [#417] and [#506]
plan                    C1..C6 execution batches + C7 measurement
C1  architect seat over 25 NEEDS-RULING rows   net closes 0, unblocks 25
C2  ratification act, one seat, no lanes       net -2, plus 4 rows re-pegged
```

So "campaign batch 1" is **an architect seat, not a lane, and it closes nothing** — its value is
unblocking 25 rows. That makes it a Position-0 candidate rather than a batch-7 lane.

**Two things to carry into the ruling.**

1. **`[#417]` is no longer NOW-CLOSABLE**, and NB4-E does not know it — §1.8 shows lane f converted
   the very clause NB4-E graded met. The NOW-CLOSABLE set is **1 row (`[#506]`)** unless `[#417]`'s
   conversion is revisited. NB4-E's stated prerequisite (*"the Form-E predicate repair lands
   FIRST"*) is likewise only partly met: it landed for `[#409]`/`[#410]`/`[#411]`, not for
   `[#415]`/`[#425]`.
2. **NB4-E's own arithmetic says the plan does not reach the target**, and says so without
   smoothing: *"Cumulative expected net at the optimistic end of every range: −29. Against a required
   −97. Stated plainly rather than smoothed: this plan does not reach under 100 in windows 3–8."*
   That is a finish-line question for the architect, not something a lane can execute around.

### Q8 · NB4-C PLAYBOOK gap arc — **M, ruling-shaped rather than authoring-shaped**

`docs/audits/2026-08-16-verification-nb4-playbook-gap.md` — a PLAYBOOK coverage matrix over the 13
rows the brief enumerates: **covered 1 / partial 6 / absent 6**. Its structural finding is the useful
part: *"Every ABSENT row is a mechanism born in the last EIGHT DAYS … and every PARTIAL row is an
older section whose machine contract moved underneath it."*

The proposed work is **one arc, 12 acts** across Ch8 ×7, Ch11 ×3, §5 ×1, Ch10 ×1, sized at
**≈ +250 lines on 4628 (~5%)**. Crucially the drafts are **paste-ready**: *"They are written to be
paste-ready so the architect's cost is a ruling rather than an authoring pass."*

**Constraints to respect:** Act 8's organ-list edit points at Acts 9 and 10, so dropping either
leaves Act 8 dangling; and `silent_rule_ratchet` headroom is **1**, so the arc's arithmetic changes
if any other lane adds a normative token first. PLAYBOOK is TOC-gated but sits **outside**
`canonical_freshness`, so it does not need a review stamp to land.

Because it is a hub-process surface competing for §4's scarcest bucket, and because its cost is a
ruling rather than a build, **it belongs at Position 0, not on the roster.**

### Q9 · `harvest_batch.py` — **S–M, no collisions, direct leverage on the batch's own cost**

Proposed at `docs/audits/2026-08-15-technical-night3-research.md:329` and recommended at `:644`:

> build `harvest_batch.py` first (board watch via `claude agents --json --all` on `state == "done"`,
> then packet fetch by `git show` — never by parsing `claude logs`, which is ANSI screen replay), and
> keep dispatch operator-run with the `[#530]` `claim` gating the spawn.

New file, touches nothing else, no OWNED-FILES collision with any other candidate. Batch 6 was
integrated by hand across twelve lanes and produced two integrator errors, **both in the
harvest/merge path** (§1.5 and AMENDMENT 2). This is the tool that addresses that class directly,
which is why it earns the second hub slot in §4 over the alternatives.

### Q10 · Intake #34 ratification — **architect act, S**

`docs/intake/2026-08-16-code-architecture-enforcement.md`, `intake-id: 34`, `status: DRAFT`, landed
by wrap act (iv). Its header is unambiguous — *"DRAFT BINDS NOTHING … authorises no adoption, no
dependency, no config change and no gate"* — and its source artifact is still operator-held and
**lands with the ratification**. Nothing downstream is blocked on it, which is why it is last.

*(The NB4 consolidated briefing's arc A2 still reads "`#34` does not exist — this arc is a birth, not
an edit." It was written before wrap act (iv). When Q1 lands that report, this line is already
stale; do not act on it.)*

Intake currently carries **4 DRAFT** (#24, #27, #33, #34) and **8 SEED** alongside 16 ACCEPTED/READY.

### The owed list, unranked — small, and it should ride along rather than take a lane

From the packet's own "Owed": the **D3.1–D3.5** promotions (night-2 briefing §D3, all still marked
PROPOSED), **`ARCHITECTURE.md:427`** ("four sub-detectors" → five, deferred because the file is
freshness-gated at 1020 lines and one word does not earn a review stamp), and the
**`[#415]`/`[#425]`** Form-E repairs (§1.7 confirms exactly these two are affected; one appended
clause each). Add from this report: the `[#531]` occurrence-count append (§1.1), the
`disposition token` enumeration (§1.6), and the `[#417]` locator repair (§1.8). Seven small edits
across six files — one finish-line lane, or a Position-0 sweep.

---

## §4 · The W5 arithmetic for a plausible batch-7 roster

**The rule.** PLAYBOOK Ch8: *"at most 1/4 of a batch's lanes target methodology or hub-process
surfaces"*, evaluated against **dispatched width**, floor arithmetic, under the I-D10 §G-8 three-way
split (`feature/satellite` · `finish-line` · `hub-introspection`), declared **ex-ante**. And the
clause that governs this batch in particular:

> A batch that cannot fill its non-process lanes **reports the shortfall** in its end-of-batch packet
> and runs narrower; backfilling the gap with additional process lanes defeats the cap.

**The premise that changed.** Batch 6 reached width 12 because seven of its lanes were Wave-2
conversion lanes — a large, cleanly-partitionable, collision-free `finish-line` stock. §2.2(a)
establishes that stock is now **zero**. Batch 7 cannot fill its non-process bucket the way batch 6
did, and the cap is a *ratio*, so an empty non-process bucket shrinks the hub allowance with it.

**This is also where the existing proposal fails.** The NB4 consolidated briefing's own arc A4
sketches a batch-7 roster and scores it honestly: *"width 4 → cap = floor(4/4) = 1 hub-process lane
… verdict → 2 hub-process lanes declared against a cap of 1 == OVER CAP by one."* The arithmetic
below is the corrective, at a width the non-process stock can actually support.

**Candidate lanes, bucketed:**

```
hub-introspection (the scarce bucket)
  H1  [#533] seam leg (6b)         audit.py + audit_checks/ + tests/test_audit.py + new test file
  H2  lane l   #348 #426 #505      tests/test_audit.py + audit detectors
  H3  lane y   #531                check_hooks_armed
  H4  [#533] leg 2                 registry + journal_anchor
  H5  harvest_batch.py             NEW file only
  H6  NB4-C PLAYBOOK arc           protocols/PLAYBOOK.md

finish-line
  F1  closing campaign C2          (needs Q1 + ratification; C1 is a seat, not a lane)
  F2  the owed-list sweep          D3.1-D3.5, ARCHITECTURE:427, #415/#425, #531, #417, token enum
  F3  [#293] execution             (needs the Q5 ruling first)
  F4  ARM-2 row-length remediation 19 loci, incl. the 8 this batch created
  F5  grade the 38-row overhang    the census re-grade §2.2(b) shows is missing

feature/satellite
  S1  [#529] phase-3 wiring        telemetry call sites + the _REPO_ROOT worktree fix
  S2  [#530] leg repairs           ABA race + rev-parse conflation
```

**The collision structure caps the hub bucket below the cap.** H1, H2, H3 and H4 all touch
`scripts/audit.py` / `audit_checks/` / `tests/test_audit.py`. H1 is the precondition for H2 and H3
(§3 Q2), and H4 wants H1's registry underneath it. **At most one of {H1, H2, H3, H4} is dispatchable
in batch 7**, and it has to be H1. H5 and H6 are collision-free.

So dispatchable hub demand is 3: **H1, H5, H6.**

**The arithmetic.** Non-process stock is 5 finish-line + 2 feature = **7**, and two of those (F1, F3)
are gated on rulings that may not land in time.

```
h = hub lanes, n = non-process lanes, width w = n + h, cap = floor(w/4), require h <= cap

n = 7 :  h = 2  ->  w =  9,  floor(9/4)  = 2   WITHIN CAP
         h = 3  ->  w = 10,  floor(10/4) = 2   OVER by 1
n = 9 :  h = 3  ->  w = 12,  floor(12/4) = 3   WITHIN CAP  (needs 2 more non-process lanes)
n = 5 :  h = 2  ->  w =  7,  floor(7/4)  = 1   OVER by 1   (if F1 and F3 stay ruling-blocked)
```

**Verdict: 2 hub lanes at width 9, not 3.** One slot is spoken for — H1, the seam leg, without which
lanes l and y are refused again. The second is a genuine choice between H5 (`harvest_batch.py`) and
H6 (the PLAYBOOK arc).

**Recommendation: take H5, and run H6 at Position 0 rather than as a lane.** Batch 6 set that
precedent — seven Position-0 acts including two births and the manifest itself — and the fit is
better than a tie-break: NB4-C's drafts are paste-ready, so its cost is a *ruling*, which is what
Position 0 is for; PLAYBOOK is TOC-gated and is a poor parallel subject; and Position-0 acts do not
count against dispatched width, so this is a real saving rather than relabelling. The same reasoning
moves the closing campaign's **C1** (an architect seat over 25 rows, closing nothing) to Position 0.

**Two honest notes on this arithmetic.**

1. **If F1 and F3 stay ruling-blocked, batch 7 is a width-7 batch with a cap of 1** — and the cap
   would then refuse the seam leg's companion outright. The rulings in Q5 and Q7 are therefore not
   just queue items; they are *width* items. Deciding them before dispatch is what buys batch 7 its
   second hub lane.
2. **Backfilling is not available.** The cap clause names this exact temptation, and the obvious
   backfill here — more conversion lanes — is the one thing §2.2(a) proves does not exist. If the
   non-process bucket cannot be filled, the correct move under the clause is to **run narrower and
   report the shortfall in the packet**, not to widen with hub lanes.

**A plausible batch 7, stated as a roster:**

```
width 9, one wave, cap floor(9/4) = 2, declared ex-ante

hub-introspection  2/2  AT CAP
  H1  [#533] seam leg, shipping nb5-A's 6b (source move + hooks_armed test split)
  H5  harvest_batch.py

finish-line        5
  F1  closing campaign C2             gated on Q1 + ratification
  F2  the owed-list sweep
  F3  [#293] execution                gated on the Q5 ruling
  F4  ARM-2 row-length remediation
  F5  census re-grade of the 38-row overhang

feature/satellite  2   (empty in batch 6; non-empty here)
  S1  [#529] phase-3 wiring
  S2  [#530] leg repairs

Position 0 (not lanes, not counted against width)
  land the ten night-4/night-5 reports  ·  the NB4-C PLAYBOOK arc  ·  closing-campaign C1
  the [#293] home ruling  ·  intake #34 ratification  ·  the [#417] disposition (§1.8)
```

Lanes **l** and **y** defer a second batch, to batch 8, onto the decomposed tree the seam leg
produces. That is the same reasoning D-1v2 used — the work is deferred by one batch and arrives on a
tree where it no longer collides — and it is only true if the seam leg ships the test split.

---

## §5 · What this report did not do

- It did not run the **full** suite. It did run the three tests the packet names, after discharging
  the uv trap (§1.10), plus the `doc_rot` and `routine_consumers` detectors directly — which is how
  §1.3 and §1.9 were found. A full-suite verdict, and therefore the packet's `2 failed, 2968 passed`
  line, remains unchecked.
- It did not verify teardown, the `--no-verify`/`SKIP=` claim, or worktree state — all are
  operator-host facts and this is a fresh clone.
- It did not re-grade the 38-row overhang. §2.2(b) sizes and enumerates it; grading it is F5.
- It read four of the ten unmerged night reports (nb5-A, nb5-B, NB4-C, NB4-E + the consolidated
  briefing) and did not read the other six, so §3 may under-represent them. Every substantive claim
  taken from an unmerged report was re-verified against the live tree before use — which is how
  §1.8 was found, and how NB4-E's `4bef950` citation was caught.
- It ruled nothing, closed nothing, and changed no BACKLOG row.

---

**Claims verified 26/31 · mismatches: `[#417]`'s conversion replaced a met clause with an unmet one
and its new locator is already dead (§1.8) · `[#531]` still records three occurrences, not four
(§1.1) · untestable denominator 29 → 28 arithmetic, 19–57 measured band (§2.2) · the ARM-1 RED has
two loci, not one (§1.3) · 1 not reproduced: the third RED's "passes serially" triage fails on a
second host (§1.9) · plus 5 unrecorded findings (§1.4 eight ceiling crossings, §1.6 the undefined
`disposition token`, §1.7 ten unmerged reports, §1.10 the uv trap disarming a HOOK and its untested
discharge route, §3-Q2 the unfiled silent dual-import defect) · queue of 10 items.**
