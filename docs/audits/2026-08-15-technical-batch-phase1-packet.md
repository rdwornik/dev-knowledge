# Phase-1 batch (batch 5) — END-OF-BATCH PACKET

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** batch-phase1-packet
- **Closes:** `docs/audits/2026-08-15-technical-batch-phase1-manifest.md` (`batch: 5`, `status: open`).
  **Committing this file is the single act that closes the batch** and expires the ADR-110
  declared-integration-arc exemption — no edit anywhere, per the ADR's own expiry design.
- **Authority:** the phase-1 architect rulings **R1–R7** of 2026-08-15, issued on
  `PHASE1-REVIEW-PACKET.md`. Every ruling's discharge is tabled in §7.
- **Base:** `main` @ `d62796ad`, clean, `audit.py health` → `health: OK`, `open_batches()` → `[]`.
- **Width:** 7 dispatched (M N O P Q R S) · 7 merged · **0 abandoned** · close-width delta **0**.

---

## 1. Per-merge SHAs — the R4 ruled order, walked serially from the primary checkout

| # | Lane | Branch | Lane tip | **Merge SHA** | Exemption | Anchored by |
|---|---|---|---|---|---|---|
| 0 | — | `docs/phase1-batch-manifest` | `8dfadb8e` | **`faad5f48`** | n/a | JOURNAL (b) names `a8208619` |
| 1 | **S** | `worktree-lane-s-w20-draft-landing` | `6516f6e2` | **`bce5838a`** | **NO — off-grammar** | JOURNAL (b) names `6516f6e2` |
| 2 | **Q** | `worktree-lane-q-293-satellite` | `82d128f8` | **`dce393ec`** | yes (ADR-110) | exemption |
| 3 | **R** | `worktree-lane-r-gateclose-drain8` | `41c040b4` | **`8c9163e0`** | **NO — off-grammar** | JOURNAL (b) names `41c040b4` |
| 4 | **N** | `worktree-lane-n-528-legs12-latency` | `03814f6c` | **`7d1f6ce0`** | yes (ADR-110) | exemption |
| 5 | **M** | `worktree-lane-m-529-telemetry-emit` | `d45fdb9e` | **`4ad2025d`** | yes (ADR-110) | exemption |
| 6 | **P** | `worktree-lane-p-530-single-flight` | `11b0cbdb` | **`50daad05`** | yes (ADR-110) | exemption |
| 7 | **O** | `worktree-lane-o-527-block-main` | `9732daea` | **`60eefbb7`** | yes (ADR-110) | exemption |

Integration arcs after the queue, on `docs/phase1-integration-wrap`: `87ba324e` (row updates),
`a84f069d` (CLAUDE.md §9 roster row), and this packet committed together with JOURNAL `(c)` —
deliberately ONE commit, because committing the packet is what expires the ADR-110 exemption and
the JOURNAL entry that re-anchors the five exempted lane merges must land in the same breath.
Their SHAs and the wrap merge SHA are recorded in JOURNAL `2026-08-15 (c)`.

**Lane P's tip moved during integration.** The review packet recorded `73da833c`; the merged tip is
`11b0cbdb`, which adds R2's fixup commit. Every other lane merged at exactly the reviewed tip.

**Every merge conflicted on `docs/audits/README.md` and only there** — the generated audit index,
which all seven lanes touch. Resolved by regeneration, never editorially: incoming audits were
staged *before* `gen_audit_index.py --write`, since the generator reads **tracked files only** and
silently omits an unstaged addition.

### 1a. THE FINDING THAT ALMOST WEDGED THE QUEUE — two lanes get no ADR-110 exemption

`batch_manifest.is_lane_merge` imports `validate_branch_naming.LANE_BRANCH_RE`
(`^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`). Measured live before merge #1:

```
worktree-lane-s-w20-draft-landing    REFUSED   id slot reads `w20`, not \d+
worktree-lane-r-gateclose-drain8     REFUSED   no id slot at all
worktree-lane-{q,n,m,p,o}-<id>-…     accepted
```

So the exemption covered **five of seven**, and **S was merge #1**. Unhandled, S's merge lands an
unanchored non-exempt first-parent spine entry, `check_journal_spine_anchor` returns FAIL, and
because `audit-health` is a **pre-commit** gate that FAIL wedges every subsequent commit in the
queue — at merge #1 of 7.

**Resolved by anchoring, not by renaming or reordering.** Reordering is foreclosed (R4 rules the
order) and would not have helped anyway: unlike batch 4, where the hazard was a *future* landing,
the strict grammar is already on `main`. Renaming would have worked but invents sentinel ids for
two lanes carrying no row id, and mutates refs the review packet and the lane commit bodies cite by
name. Instead the JOURNAL entry riding the manifest arc names both lane tips on an explicit
`Anchors:` record line, so both merges satisfy `journal_anchor.is_anchored` by the gate's **ordinary
predicate**. Verified live immediately after merge #1, which is the measurement that mattered:

```
is_lane_merge(bce5838a) -> False      (no exemption)
is_anchored(bce5838a)   -> True       (JOURNAL)
audit.py health         -> health: OK
```

**The honest limit of that route, disclosed rather than left implicit:** it works because the
anchoring predicate is a text match over `JOURNAL.md`, which lets an integrator anchor a merge
*before* making it. That is a real property of the mechanism, not a hole opened here — but it was
used deliberately, and only for the two merges the exemption cannot reach.

**This is the third occurrence of the class** (batch 4 filed it against its W4/W6 and resolved it by
dropping both lanes from the roster). The root cause is neither branch name: **the lane grammar is
enforced nowhere at provisioning.** `validate_branch_naming` is read-only and wired into no gate,
and a lane dispatched straight through `claude --worktree <name>` never passes `/lane-boot` step 1 —
`batch_manifest.py`'s own honest-limits block says exactly this. An off-enum name is still freely
creatable; what it silently loses is the exemption. **Owner: needs a row; none exists.**

---

## 2. Suite result

**`uv run --locked pytest -q` on the merged tree — ONE run, in a DEFAULT shell with
`PYTHONUTF8` unset:**

```
1 failed, 2955 passed, 3 skipped, 1 xfailed in 1431.73s (0:23:51)
PYTEST_EXIT=1
```

**The single failure is PRE-EXISTING and is not this batch's.**
`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` —
`AssertionError: assert '1 declared routine row' in '2 declared routine row(...)'`.

Lane N declared it pre-existing and proved it three ways. **That was not taken on trust.** It is
re-proved here on the integrator's own measurements, and one leg is stronger than N's because it
predates the batch entirely:

1. **The pre-merge baseline — the decisive leg.** `audit.py health`, run on clean `main` @
   `d62796ad` *before merge #1* and recorded in this run's own opening evidence, printed
   `[OK] routine_consumers: 2 declared routine row(s) name a consumer and a consumption_path`.
   The test asserts `'1 declared routine row'`. **It was already failing at the base commit, with
   no lane merged and nothing of this batch in the tree.**
2. **The declaration count is unchanged.** Rows declaring `routine:` / `consumption_path:` measure
   **6 at `d62796ad` and 6 now.**
3. **The batch changed no declaration.** `git diff d62796ad..HEAD -- BACKLOG.md` alters no
   `routine:` or `consumption_path:` line — lane R's drain only condensed prose inside `#487` and
   `#428`, both of which merely *mention* `routine_consumers`.

**Honest limits, both stated rather than implied.** (a) The run executed on the wrap branch with
all seven lanes merged and every row update applied; the only delta to final `main` is this packet
and the JOURNAL `(c)` entry — two markdown files no test reads. (b) It is **one** run, as the
tiered-suite law requires, and the exit code is read from the process rather than from a pipe
(`PYTEST_EXIT=1`, which is the pre-existing failure and nothing else).

---

## 3. Final gate line, per-WARN owners

`python scripts/audit.py health` → **`health: OK`, exit 0, ZERO FAILs, 36 WARNs.**

**No gate was forced green and no WARN was dispositioned.** Every WARN is attributed below, and the
attribution is measured, not assumed.

| WARN class | n | Attribution | Owner |
|---|---|---|---|
| `doc_rot` backlog-accretion | 7 | **2 caused by this run** — `#529` and `#530`, whose ruled row updates crossed a ceiling they sat 27 and **1** char under. 5 inherited (`#514 #523 #492 #419`, plus `#528`, which grew but was already a locus) | `[#529]` `[#530]` — §6 |
| `undeclared_edges` (ADR-88 FC2) | 20 | **Pre-existing**, unchanged in kind by this batch | inherited doc-edge debt |
| `review_artifact_coverage` | 2 | **4 of the 6 named merges ARE this batch's** (O, P, M, N). Terra review *was* run on all four, but the artifact is persisted **off-repo** at `~/Downloads/PHASE1-TERRA-RAW-2026-08-15.md` rather than as a canonical `docs/audits/<date>-codex-<slug>.md` carrying a `**Tally:**` header — so the organ cannot see it. This is exactly the unfalsifiable-review-claim class the check exists to surface, and it fires correctly | **W9** — `[#480]` / `[#499]` |
| `no_ff_merges` | 3 | **Pre-existing** — three legacy June commits. Never rewrite them | inherited |
| `git_backlog_drift` (`#505` closed-but-present) | 1 | **Pre-existing — verified, not assumed:** the closing commit `25ff8ec3` is an ancestor of the base `d62796ad` | `[#505]` |
| `journal_spine_anchor` mention-not-record | 1 | Advisory SHAPE check, a WARN by design (`STANDING_RULINGS` L-10). It never changes the hard verdict | n/a |
| `reconciled_versions` · `preflight_backlog_ids` | 2 | **Pre-existing** | inherited |

**The hard anchoring leg PASSES:** `[OK] journal_spine_anchor: every first-parent spine entry above
the ADR-85 disposition floor 24882f8cc is JOURNAL-anchored` — including `bce5838a` (S) and
`8c9163e0` (R), the two merges the ADR-110 exemption does not cover.

**Net WARN delta caused by this run: +3** — two `doc_rot` loci and one `review_artifact_coverage`
line, each named above with an owner.

---

## 4. Teardown table v2 — PROPOSALS ONLY · NOTHING WAS DELETED

Re-verdicted live against `main` after the queue, with lane S landed and R5's two reports landed.

> **R5 expected "SUPERSEDED-DELETE across the board". That expectation is FALSIFIED and the table
> below is the measurement, not the expectation.** Landing S plus the two PLAYBOOK-cited reports
> supersedes **three** branches. The other **five** carry artifacts that nothing in this batch —
> or anywhere on `main` — has landed. They are the only refs keeping those commits reachable.

| # | Branch | Tip | Ahead | Unique artifact | On `main`? | **Verdict v2** |
|---|---|---|---|---|---|---|
| 1 | `claude/night2-wave2-drafts-fmbwa4` | `104e8b12` | 1 | `…-technical-w4-wave2-conversion-drafts.md` | **YES** | **SUPERSEDED-DELETE** |
| 2 | `claude/night2-latency-audit-6s1k6p` | `8387ff2a` | 1 | `…-technical-night2-latency.md` | **YES** | **SUPERSEDED-DELETE** |
| 3 | `claude/night2-research-d30vhu` | `413bbd60` | 2 | `…-technical-night2-research.md` | **YES** | **SUPERSEDED-DELETE** |
| 4 | `claude/night2-census-audit-btqr42` | `2f39e60d` | 1 | `…-census-night2-census.md` | **no** | **UNIQUE-HOLD** |
| 5 | `claude/night2-hygiene-sweep-8zgyjx` | `73435adb` | 2 | `…-verification-night2-hygiene.md` | **no** | **UNIQUE-HOLD** |
| 6 | `claude/night2-plancheck-audit-6ldr94` | `ed5c7ff6` | 1 | `…-verification-night2-plancheck.md` | **no** | **UNIQUE-HOLD** |
| 7 | `claude/night2-quality-audit-8a3ixh` | `ba50027a` | 1 | `…-qa-night2-quality.md` | **no** | **UNIQUE-HOLD** |
| 8 | `claude/night2-consolidation` | `b97499a8` | 1 | `…-technical-night2-consolidated-briefing.md` | **no** | **UNIQUE-HOLD** |

**Tally: 0 MERGED-DELETE · 3 SUPERSEDED-DELETE · 5 UNIQUE-HOLD.** All eight remain **unmerged**
into `main` (`git merge-base --is-ancestor <branch> main` → NO, ×8), so for rows 4–8 the branch is
the sole reference keeping its commits reachable.

**Evidence for the three supersessions, blob by blob:**

- **wave2-drafts** — its condition ("delete only after S is on `main`") is now **met**. Both states
  are on `main`: the **byte-identical original** blob `8df3be88` at commit `6c4743cd`, and the
  four-ruled-edits amendment `4c3481a8` at `6516f6e2`. Nothing is lost by deleting the branch.
- **latency-audit** — blob `41aa7bae` on `main`, **byte-identical** to the branch's, and the branch
  tip *is* the SHA `PLAYBOOK.md` cites (`8387ff2a`).
- **research** — blob `c01efd44` on `main`, **byte-identical to the branch tip**. The tip was landed
  rather than the cited `757077f2` because the delta is **+24 / −0** in one hunk amending §4.6, so
  the cited §1/§2.2–§2.6 material is byte-identical *and* the correction travels with the reference.

**The teardown trap, restated because it now applies to five branches rather than seven:** deleting
an unmerged branch orphans its commits, and once gc runs their content is gone. Rows 4–8 are sole
copies. **Do not delete them without landing their artifacts first.**

### 4a. Worktree teardown — NOT PERFORMED, awaiting the operator's word

Per the standing instruction, worktrees are removed **only** for lanes whose board session the
operator confirms closed. **Nothing was removed and no branch was deleted.** `git worktree list`
still reports 8 entries (primary + 7 lanes) — checklist item 3 is therefore **open by construction,
not passed**, which is recorded rather than checked off.

**The exact tile titles to confirm closed** (worktree directory · work branch):

| Tile / worktree directory | Work branch | Newest session-jsonl mtime |
|---|---|---|
| `lane-s-w20-draft-landing` | `worktree-lane-s-w20-draft-landing` | 18:12:19 |
| `lane-q-293-satellite` | `worktree-lane-q-293-satellite` | 17:58:19 |
| `lane-r-gateclose-drain8` | `worktree-lane-r-gateclose-drain8` | 18:23:19 |
| `lane-n-528-legs12-latency` | `worktree-lane-n-528-legs12-latency` | 18:33:02 |
| `lane-m-529-telemetry-emit` | `worktree-lane-m-529-telemetry-emit` | 18:30:19 |
| `lane-p-530-single-flight` | `worktree-lane-p-530-single-flight` | 18:42:19 |
| `lane-o-527-block-main` | `worktree-lane-o-527-block-main` | 18:43:19 |

**All seven are merged, so all seven are removable the moment you confirm.** The mtimes are
evidence, **not** a verdict: a stalled session jsonl means *idle*, not *closed*, and the two cannot
be told apart from outside. That is precisely why the confirmation is yours.

---

## 5. Wrap items — carried, not done

| # | Item | Why it is not done here | Owner |
|---|---|---|---|
| **W1** | **`CLAUDE.md` §5 rule 4 is descriptively false** — *"Layer 2 never executes — `scripts/` contains read-only validators only"*, while ~23 scripts mutate state and `scripts/audit.py:4707` already pushes to `origin` | **Ruled R3:** carry as a wrap item, do **not** edit `CLAUDE.md`. It is a governance edit to a canonical file, not an integrator's drive-by. Either amend the rule or re-scope it to §10's narrower and accurate *"no scripts that drive state in child repos"* | operator / architect |
| **W2** | **Re-point N's audit citations** — `PLAYBOOK.md` L844/L866 still describe both night-2 audits as drafts *"on the unmerged branch"*. Stale as of merge #4: the content is now on `main` | Rewriting the lane's freshness-coupled doctrine surface at its own merge is a drive-by beyond R5's scope | `[#528]` leg 3 |
| **W3** | **The lane grammar is enforced nowhere at provisioning** (§1a) — third occurrence; an off-enum lane name silently forfeits the ADR-110 exemption | Needs a row; birthing one requires a `kill-candidates:` line and no ruling authorises a birth this run | needs a row |
| **W4** | **`[#527]` is NOT closed** though its Done-when is evidenced on all three legs | The review packet calls it "closeable"; **no ruling in R1–R7 closes it**, and R2's *merged ≠ closed* is this batch's standing posture. Proposed, not self-declared | operator (`/review-closures`) |
| **W5** | **Process-lane cap exceeded by one** — width 7 permits `⌊7/4⌋ = 1` hub-process lane; **N** and **O** both occupy that bucket | Reported, not adjudicated — a packet does not overturn a dispatch. The **O** bucketing is the debatable one: read as a shipped feature rather than a hub-process surface, the roster is within cap | operator |
| **W6** | **`[#505]` leg 1 stays unmet** — this is the **fourth consecutive batch** to miss commit-at-dispatch, and the latest of the four (batch 3, night-cloud and batch 4 were at least mid-flight; this manifest landed at integration) | The manifest is a partial repair, explicitly not a discharge | `[#505]` |
| **W7** | **`doc_rot` 5 → 7 loci**, both new ones forced by ruled row updates (§6) | Disclosed, owned, WARN-tier; see §6 for why it could not be avoided | `[#529]` `[#530]` |
| **W8** | **`_git` in `tests/test_single_flight.py` carries the same strict-utf8 read** the R2 fixup repaired in `_cli` | R2 scopes the change to one line, and `_git` only ever reads ASCII git plumbing in this file. Same latent class, named rather than silently widened | `[#530]` |
| **W9** | **`review_artifact_coverage` cannot see this batch's terra review** — it ran on lanes M/N/O/P and is persisted, but **off-repo** and in a non-canonical shape, so 4 merges read as unreviewed | The harvest deliberately invoked codex directly rather than through `codex-review.ps1` *because* the wrapper writes into `docs/audits/`, and R3 names the Downloads file as the artifact of record. Landing a canonical `docs/audits/2026-08-15-codex-<slug>.md` with a `**Tally:** 0/0/6/0` header would clear it — but that changes which file is the review of record, which is a decision, not integrator hygiene | operator; `[#480]` / `[#499]` |

---

## 6. The owned WARN delta — `doc_rot` 5 → 7, and why it was unavoidable

Lane R drained `validate_doc_rot` from **11 loci on `main` to 5** — re-measured independently by the
integrator on the merged tree, and the 5 survivors were exactly `#514 #528 #523 #492 #419`, matching
R's claim line for line. The ruled row updates then took it to **7**.

**It could not be avoided, and three things were tried.** Measured before editing:

```
BACKLOG#530  1319 chars   headroom to the 1320 ceiling:  1
BACKLOG#529  1293 chars   headroom:                     27
BACKLOG#528  1741 chars   already a locus
BACKLOG#293   869 chars   headroom:                    451
```

The 1320-char gross-bloat ceiling was raised from 1200 **this same morning** (D1.1, "p90"). R2
requires the two P1 legs on `[#530]`'s row and R7 requires the four legs on `[#529]`'s. **Any leg
text on either row mints a locus by construction.**

1. **The `[#480]` shape was attempted first** — detail sections *below* the generated row bullet,
   which cost no BACKLOG row chars. **`gen_task_tree` refused it outright**: *"a task is ONE
   physical line; non-task prose belongs in manifest.json"* (ADR-107 §2). The generator refused
   rather than silently emitting, which is the correct behaviour and is why it was caught.
2. **Row text was then cut to only what is actionable**, with the full argument carried in this
   packet, which each row cites. First draft would have produced **8** loci; the trimmed version
   produces 7.
3. **`[#293]`, the one row with real headroom, was kept UNDER the ceiling deliberately** — by
   dropping its dated tokens. Worth recording: **this packet's own filename contains `2026-08-15`,
   so every full-path citation costs a dated block** against the `≥3 dates AND >700 chars` predicate.
   `[#293]` tripped on *dates*, not length, until the citation was reworded.

**Net across the batch: 11 → 5 → 7, still −4.** `doc_rot` is WARN-tier and gates nothing.

---

## 7. Ruling discharge — R1 through R7

| Ruling | Status | Evidence |
|---|---|---|
| **R1** — create+commit the ADR-110 manifest; derive the shape from the ADR; quote it in the commit body; authorization line for M's and P's four new files | **DISCHARGED** | `docs/audits/2026-08-15-technical-batch-phase1-manifest.md` @ `a8208619`, merged `faad5f48`. Shape derived from `scripts/batch_manifest.py` and every field run through the parser before writing (glob → `True`, `_valid_closer` → `True`, `batch: 5` a digit because a test pins `isdigit()`). **Recorded honestly:** the authorization is belt-and-braces — `validate_hermetization.classify()` **admits all four paths with no grant**, since `scripts/` and `tests/` are established allowlisted homes. It records an operator decision that the births land; it does not paper over a refusal that never happened |
| **R2** — one-line encoding fixup on P's branch; re-run 20/20 in a DEFAULT shell; the two P1s filed as open legs; `[#530]` stays OPEN | **DISCHARGED** | Fixup `11b0cbdb` (`errors="replace"` on `_cli`, copying lane O's solved pattern). **20 passed, exit 0** with `PYTHONUTF8` explicitly unset — before the fix, 19 passed / 1 failed in the same shell. Re-run again post-merge on `main`: **20 passed**. Both P1s appended to `[#530]`; row **OPEN** |
| **R3** — reject terra's Layer-2 claim on P as over-stated; record in the persisted terra artifact; carry the `CLAUDE.md` §5 rule-4 falsity as a wrap item; do **not** edit `CLAUDE.md` for it | **DISCHARGED** | Rejection appended to `~/Downloads/PHASE1-TERRA-RAW-2026-08-15.md` as an "ADJUDICATION OF RECORD" block, so it travels with the finding. Falsity carried as **W1**. `CLAUDE.md` §5 was **not** edited — the §9 edit that *was* made is the separate, independently-owed roster row (W5-precedent debt), and its §12 entry says §5 rule 4 is knowingly left standing |
| **R4** — merge order S → Q → R → N → M → P → O | **DISCHARGED** | §1, walked serially from the primary checkout in exactly that order; O last, so the queue completed under today's rules and the new gate governs from a clean edge |
| **R5** — land the two PLAYBOOK-cited night-2 reports byte-faithful in the N-merge step; re-verdict all 8 branches | **DISCHARGED, with its expectation falsified** | Both landed **inside merge `7d1f6ce0`** so `main` never held a state where newly-landed doctrine cited unlanded objects. Blobs `41aa7bae` and `c01efd44`, byte-faithfulness verified by `git rev-parse` against the source branches. Teardown table v2 in §4 — **3 SUPERSEDED-DELETE, 5 UNIQUE-HOLD, not "across the board"**. **Nothing deleted** |
| **R6** — `[#293]` denominator ruled = ADR-104's 8; correct at `tasks/` source; seeding NOT executed | **DISCHARGED** | `tasks/293-consumer-runbook-fan-out.md` corrected at source and re-emitted; the row now reads **0 of 8** with the eight members named. Cross-repo seeding **not executed** — it stays operator-gated |
| **R7** — apply N's six owed items and the harvest to-dos; derive the JOURNAL letter at merge time | **DISCHARGED** | All six dispositioned with owners on `[#528]` (item 6 **discharged** by R5's landing). `[#529]`/`[#530]`/`[#528]` row updates at `tasks/` source (`87ba324e`). Q's JOURNAL allocation folded into the integrator's entries. Day letters derived live from `JOURNAL.md`: `(a)` existed, so this run took **`(b)`** and **`(c)`** |

---

## 8. Checklist — `/lane-integrate` §3, item by item

| # | Condition | Verdict |
|---|---|---|
| 1 | Every lane branch merged-or-explicitly-abandoned | **PASS** — 7 of 7 merged with SHAs, 0 abandoned |
| 2 | Full suite run once on the merged result | **PASS, with a pre-existing RED disclosed** — one run: `1 failed, 2955 passed, 3 skipped, 1 xfailed`. The single failure is proved pre-existing three ways in §2, one leg predating the batch entirely |
| 3 | `git worktree list` == primary only | **OPEN BY CONSTRUCTION** — 8 entries. Teardown deliberately withheld pending the operator's confirmation (§4a). Recorded, not checked off |
| 4 | Manifest/packet archived | **PASS** — manifest `faad5f48`; this packet is the closer |
| 5 | `git stash list` empty | **PASS** — empty output, verified after the last merge |

---

## 9. What this run did NOT do

- **Deleted nothing** — no branch, no worktree, no ref, local or remote. All 8 night-2 branches and
  all 7 lane worktrees are exactly as they were found.
- **Did not close `[#527]`**, `[#528]`, `[#529]`, `[#530]` or `[#293]`. Only `[#527]` is *proposed*.
- **Did not execute the `[#293]` cross-repo seeding** — operator-gated by R6.
- **Did not edit `CLAUDE.md` §5 rule 4**, or re-point PLAYBOOK's citations (W1, W2).
- **Did not rename or reorder any lane branch** — both were considered for §1a and rejected with
  reasons.
- **Did not force any gate GREEN by disposition.** The one WARN delta this run caused (§6) is
  reported with its cause and its owners.
