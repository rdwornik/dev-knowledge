---
batch: 2
closes: docs/audits/2026-08-07-technical-batch-2-manifest.md
---

# Batch 2 — end-of-batch packet (the artifact that closes the batch and expires R-1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-07 · **Slug:** batch-2-packet
- **Manifest:** `docs/audits/2026-08-07-technical-batch-2-manifest.md`, committed at DISPATCH
  (`876cc463`) — the first batch in this repo's history to have one.
- **Integrator:** one dispatched Opus seat, primary checkout, branch `docs/batch-2-integration`.

**Committing this file is what closes the batch.** It discharges close-out item 4 and expires
the ADR-110 R-1 declared-integration-arc exemption in the same act, by design — the manifest
named this exact path as its `closed_by:` before this file existed.

---

## 1. Merge queue — discovered from reality, not from the manifest's branch column

The manifest's branch column is **not** the queue, and that is a finding, not a nuisance. Three
of the four branches that actually existed were named differently from the plan:

| Lane | Rows | Planned branch | ACTUAL branch | Merge SHA |
|---|---|---|---|---|
| AM4-FOLD | [#480] [#505] | `docs/am4-dispatch-visibility` | *(as planned)* | **`ea4ddf23`** |
| lane-2 | [#429] | `worktree-lane-2-429-worktree-portability` | `worktree-lane-b-429-worktree-portability` | **`e685a306`** |
| lane-1 | [#490] + [#430] | `worktree-lane-1-490-parity-manifest` | `worktree-joyful-scribbling-hummingbird` → renamed | **`47bd4f52`** |
| lane-3 | [#320] | `worktree-lane-3-320-fleet-backup` | `worktree-lane-c-320-backup` | **`ad9332c3`** |

Merged serially in that order — doctrine before lanes, then the two script-touching lanes, then
the record lane. One merge at a time; the suite verdict is on the final merged tree.

Integrator's own commits: `a96040c3` (closures), `63b7b6a9` (self-correction), plus this
packet + JOURNAL.

### I-1 — the manifest's own lane grammar is unusable, and lane-2 found out first

Lane-2's routed finding **LB-1** is confirmed independently here. The manifest writes the lane
grammar with a **digit** (`worktree-lane-2-...`); `scripts/validate_branch_naming.py` compiles it
with a **single lowercase letter**. PLAYBOOK Ch8 delegates the grammar to that validator, so
**the validator is canonical and the manifest is wrong**. Measured, not argued:

```
worktree-lane-1-490-parity-manifest      kind=unknown      R1-exempt=True
worktree-lane-a-490-parity-manifest      kind=batch-lane   R1-exempt=True
worktree-joyful-scribbling-hummingbird   kind=worktree     R1-exempt=False
```

Lanes 2 and 3 each independently renamed themselves to the letter form. Lane-1 did not: it kept
the `claude --worktree` auto-generated name, a decision it recorded under its V-2 budget —
reasonably, since `worktree-<name>` is a valid lane prefix.

**The consequence it could not have seen, and the reason this is I-1 rather than a note.** The
R-1 exemption keys on the `worktree-lane-*` shape. An auto-named lane branch is therefore
**not exempt**, so lane-1's merge would have failed `audit-health` at commit time on the one
gate R-1 exists to relieve — and the fallback would have been `SKIP=audit-health`, the exact
thing the manifest retired. Resolved mechanically: the branch was renamed
`worktree-lane-a-490-parity-manifest` before merge (tip unchanged at `b025c15e`, zero content
touched), conforming it to the letter grammar lanes 2 and 3 had already converged on. Recorded
here rather than absorbed silently.

**For the operator:** the manifest template's branch column should be regenerated from
`validate_branch_naming.py`, and `/lane-boot` should refuse to boot a lane whose branch does not
classify `batch-lane`. Neither is done here — both are dispatch acts, and this arc's contract
forbids new dispatch.

### I-2 — two unexpected worktrees, reported not improvised

`worktree-compiled-jumping-lighthouse` and `worktree-zany-stargazing-pudding` existed in the
shared ref store, both sitting **at `main` with zero unique commits** and clean trees — empty
provisioning shells, no work at risk. Torn down under close-out item 3. Neither appears in the
manifest; the first is AM4-FOLD's provisioning branch (the half of teardown that gets
forgotten), the second has no identified owner.

---

## 2. The R-1 mechanism — first production firing, and what it actually did

R-1 was **live, load-bearing, and reported — never silent**. Verbatim from `audit.py health`
after the second lane merge:

```
[OK] journal_spine_anchor: every first-parent spine entry above the ADR-85 disposition floor
24882f8cc is JOURNAL-anchored, EXCEPT 2 lane merge(s) exempt under the ADR-110
declared-integration-arc rule while batch 2 is open
(docs/audits/2026-08-07-technical-batch-2-manifest.md) -- the exemption expires when
docs/audits/2026-08-07-technical-batch-2-packet.md lands
```

Exactly **2** merges were exempted — lane-1 and lane-2, the two lanes that correctly declined to
write JOURNAL. AM4-FOLD and lane-3 were **not** exempted and did not need to be: each carries its
own JOURNAL entry naming a SHA its merge introduced, so both self-anchor. The exemption named
the batch, named the manifest, and named its own expiry path. **No `SKIP=audit-health` was used
at any point in this batch** — batch 1 used it twice.

### The gate-firing finding that R-1's design did not anticipate

**`pre-commit` does not run on a clean `git merge`.** Git invokes `commit-msg` for an
auto-committing merge but not `pre-commit`, so on the two conflict-free lane merges
(`ea4ddf23`, `e685a306`) only the two commit-msg hooks fired — `audit-health` never ran. It ran,
and passed, on the two **conflicted** merges (`47bd4f52`, `ad9332c3`), where conflict resolution
forces an explicit `git commit`.

So R-1's protection is real but **conditional on a merge conflicting**. This does not weaken the
mechanism — a conflict-free merge needs no exemption because nothing evaluates it — but it does
mean the width-6 "five firings per batch" figure in the manifest's rationale is an upper bound,
not a prediction. Worth folding into ADR-110's amendment text.

### F2 carried forward — the exemption is self-grantable, and I demonstrated it

`batch_manifest.py`'s second honest limit says the exemption is not scoped to the lanes the
manifest enumerates: **any** `worktree-lane-*` merge qualifies while a batch is open. That makes
the exemption **self-grantable by branch naming**, and this batch is the live demonstration —
renaming lane-1's branch is exactly the act that granted it the exemption. It was the right call
here and it is recorded in the open, which is the point: the vector is a rename away, by a lane
or by an integrator.

**Push-leg mitigation confirmed as designed:** `block_unanchored_push.py` does not import
`batch_manifest` and never consults a manifest, so the range-level pre-push refusal stays
unconditional and nothing ships unanchored regardless of the commit-time verdict. **Carried to
the consolidation arc, not fixed here** — tightening the exemption to the enumerated lanes is a
separate decision, and `batch_manifest.py` says so in its own docstring.

---

## 3. Rows — closed, and deliberately not closed

Closures were run by the integrator through the closure loop, **not by the lanes**. All three
lanes declined to self-close and each gave the reason: ADR-70 Tier-1 puts closure outside a
lane's budget, and `BACKLOG.md` is a shared surface the manifest reserves for integration. That
is the loop working.

| Row | Verdict | Evidence (re-verified live post-merge, not taken from the packet) |
|---|---|---|
| [#490] | **CLOSED** | `parity-surfaces 9/9` (was 5/9) via the done-when's SECOND limb — declared absence, since 4 of 9 are genuinely unonboarded and "all 9 resolve" would be false |
| [#429] | **CLOSED** | `scripts/worktree_import_proof.py` is a real CLI; lane-2 exercised it on ai-council in BOTH directions (FAIL then PASS), exit codes 0/1/3 verified as values |
| [#320] | **CLOSED** | `git status -sb` in each of the three named repos shows no ahead/behind marker |
| [#430] | **OPEN on (b)** | (a) landed at `3cf3a5b0` and the standing RED cleared on its merits; (b) untouched — see §4, the ruling has no locator |
| [#502] | **not closed** | per contract; blocked on [#501] |
| [#505] | **not closed** | see §7 — the evidence is incomplete in a specific, stated way |

**[#490]'s stale in-row figures corrected at close**, as both contracts required: the row
asserted `state-dirs 0/9`; the live figure was **6/9** at dispatch and is 6/9 now. The row was
simply wrong, and closing it silently would have retired the error into the archive. The
correction is written into the retained task file, which is the record that survives the close.

**[#320] found more than its done-when covers, and the surplus is a NEW gap, not a closed one.**
Lane-3 swept all 9 fleet repos, not the 3 the row names. **`win-tooling` has NO `origin` remote
configured at all, and 14 branches of real typewhisper work are local-only.** That is outside the
row's done-when (which names three repos, all discharged) so it does not block the close — but it
is the same single-disk data-safety class the row was filed for. **Not filed as a row here:
filing is a dispatch act and this contract forbids new dispatch.** It is the second operator item.

---

## 4. TOP OPERATOR ITEM — the [#430](a) ruling has no locator on record

**This is the batch's most serious finding, and it is a finding about my own work as much as
lane-1's.** My closure commit `a96040c3` repeated, as verified fact, that "the operator ruled
2026-08-07 that a root `conftest.py` is permitted fleet-wide and mandated nowhere". I had taken
that from lane-1's packet without verifying it — which is precisely what the [#430] row warned
against, since its own text said the (a) fix was "UNRULED, **not chosen by inference**".
Self-corrected at `63b7b6a9`. What I then checked:

1. `git log --all -S "permitted fleet-wide"` — the phrase **enters the repo at lane-1's own
   commit `3cf3a5b0`**. Nothing earlier carries it. Same for "mandated nowhere".
2. Lane-1's session transcript contains **exactly two operator messages**: the dispatch line, and
   a later two-item answer (HOLD integration; disposition-register removal accepted). **Neither
   mentions conftest, templates, or any fleet-wide permit.**
3. `protocols/STANDING_RULINGS.md` carries no 2026-08-07 entry for it. Lane-1's
   disposition-register block asserts "Discharged by operator ruling 2026-08-07" and **cites no
   locator** — no JOURNAL entry, no ruling id, no quote. `declared_by:
   ruling-2026-08-07-root-conftest` is a token the lane minted for a ruling it did not cite.

**What this does and does not establish.** Not that the operator did not rule — it may have been
given out-of-band in a channel no artifact and no transcript records, and lane-1 escalated rather
than inferred by its own account. What IS established is that the ruling is **unlocatable from
the record**, so no reader can verify it.

**Blast radius, stated so it is not larger than it is.** [#430] stays OPEN regardless; nothing
was closed on it. But it is not inert: `ecosystem/parity-surfaces.yaml` now carries a
`root-conftest` row admitting the entry fleet-wide, and the standing RED
`test_check_fleet_parity_green_on_live_repo` cleared **because** of it. **The current ship-gate
green rests, in part, on a ruling with no locator.** Lane-1's code is deliberately NOT reverted:
it is merged and tested, reverting on suspicion is worse than flagging, and this contract forbids
editing lane content beyond mechanical conflict resolution.

**Ask:** confirm or deny the ruling. If confirmed, it needs a `STANDING_RULINGS.md` entry so the
`declared_by` token resolves to something. If denied, `3cf3a5b0` needs revisiting and [#430](a)
returns to UNRULED.

---

## 5. Suite — run once on the merged result

```
uv sync --locked --group analytics
uv run --locked pytest -n auto -q

1 failed, 2539 passed, 3 skipped in 597.19s (0:09:57)
```

**The single RED is exactly the residue the contract predicted, and nothing else:**
`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` — the test
pins "1 declared routine row" while the live file declares 2. Pre-existing, owned elsewhere,
named in the manifest's own dispatch baseline, and untouched by any lane.

Two things that were RED at dispatch and are **not** RED now, both resolved on their merits
rather than by disposition:

- `test_check_fleet_parity_green_on_live_repo` — **cleared by lane-1's [#430](a) work.** The
  manifest predicted this ("the parity RED clears on lane-1's merits") and it did. See §4 for
  the caveat attached to the ruling underneath it.
- **The 17 pandas REDs did not appear.** They were environmental, as lane-1 claimed and as this
  run proves rather than asserts: `uv sync --locked --group analytics` first, and
  `tests/test_fleet_analytics.py` is green in the count above.

---

## 6. The five refuse-to-finish items, each checked because its command was run

| # | Condition | Result |
|---|---|---|
| 1 | Every lane branch merged-or-explicitly-abandoned | **PASS** — 4 merged, 0 abandoned. `git branch --list 'worktree-lane-*'` empty. All 6 branches deleted (4 work + 2 provisioning), remote `docs/am4-dispatch-visibility` deleted too |
| 2 | Full suite run once on the merged result | **PASS** — §5 |
| 3 | `git worktree list` == primary only | **PASS with a stated residue** — see below |
| 4 | Manifest **and** packet archived | **PASS** — manifest at `876cc463`, this packet |
| 5 | `git stash list` empty | **PASS** — empty at dispatch, empty throughout, empty at close. Lane-2 and lane-3 each independently reported zero stashes across all repos they touched |

**Item 3, honestly.** `git worktree list` returns **one line, the primary** — the item as
specified passes. All five worktrees were unregistered and pruned. But **two directory skeletons
survive on disk** (`.claude/worktrees/dazzling-purring-ullman`,
`.claude/worktrees/joyful-scribbling-hummingbird`) because their lane sessions are **still alive**
(pids 19884, 12560) and hold those paths as their working directory — `git worktree remove`
returned "Permission denied", `rm -rf` returned "Device or resource busy".

Both contain **zero files** — `git worktree remove --force` deleted the contents before hitting
the pinned directory. Nothing is at risk and nothing is hidden there. They were not force-removed
by killing the operator's sessions, which is not the integrator's call. **They vanish when those
two sessions are closed.** Against CLAUDE.md §5 rule 9 ("no leftovers") this is a residue, and it
is reported rather than papered over: the provision-to-cleanup round-trip did not leave the tree
identical.

---

## 7. [#505] — assessed honestly, and NOT closed

The contract asked whether this batch satisfies clause 1, either way, with evidence.

**Clause 1 — "a fresh seat runs a full batch from repo artifacts alone." PARTIALLY satisfied,
and therefore not satisfied.** The advance over batch 1 is real and is the thing the manifest was
built to test: the plan **was** in the tree at dispatch, the R-1 exemption keyed off it and fired
(§2), and this seat reconstructed the queue, the footprints, the collision rules and the close-out
list from committed artifacts. But the seat did **not** run from repo artifacts *alone*:

- The four **lane contracts were files in `C:\Users\1028120\Downloads\`**, not repo artifacts —
  the same defect as batch 1, moved from chat to the filesystem. The manifest froze the lane
  *roster*; it did not carry the contracts.
- Three of four branch names did not match the manifest (§1), so the queue had to be discovered
  from the ref store and matched to **session transcripts**, which are not repo artifacts either.
- The lane hand-back packets exist only in those transcripts. Contract item 3 ("apply carried
  paste-block artifacts") was a **no-op** — searched all three lane transcripts for
  `paste.block|PASTE_THIS`: zero hits — but that was verifiable only by reading transcripts.

**Verdict: clause 1 stays falsified.** Closing it on this batch would ratify "the plan is in the
tree" as if it meant "the whole batch is in the tree". The gap is now precise and small: **lane
contracts must be committed artifacts, referenced by the manifest.** That is one change away.

**Clause 2 — "exactly 2 operator touches." Measured for the first time, and it depends entirely
on the unit.** Counted from the session transcripts (real operator messages, excluding
system-reminders and tool results):

| Session | Operator messages |
|---|---|
| AM4-FOLD | 1 (dispatch) |
| lane-1 | **2** (dispatch + a mid-lane answer) |
| lane-2 | 1 (dispatch) |
| lane-3 | 1 (dispatch) |
| integrator | 1 (dispatch — the GO) |
| **total** | **6**, plus this packet's hand-back = **7** |

- **Per-batch reading: 7 much greater than 2 — FALSIFIED.**
- **Per-integration reading (the GO + the packet, which is what `/lane-integrate` §0 actually
  says): exactly 2 — MET.**

Both are reported because the row does not say which it means, and a single number here would be
a choice dressed as a measurement. Clause 2 needs disambiguation before it can be closed.

Every lane dispatch carried the AM-4 board label — the doctrine AM4-FOLD encoded this same night
was already in use at dispatch.

---

## 8. Quota — REPORTED as a shortfall, not backfilled

The manifest planned **width 6: 5 feature/consumer + 1 process**, compliant with the ≤1/4
process cap. The batch **ran at width 3** (wave 1 only), and truncation broke the quota
retroactively:

- **Under the operator's ruled reading** (consumer-class = acts on consumer repos or fleet
  outcomes): lane-1 and lane-3 are feature/consumer, lane-2 is process → **1/3 process**. The
  ≤1/4 cap permits `floor(3/4) = 0` process lanes at width 3, so **the executed batch exceeds
  the cap it was planned to satisfy**.
- **Under the stricter reading** the manifest itself surfaced (product work = non-methodology
  feature development): all three lanes are hub-methodology work → **3/3 process-adjacent**, and
  this repo supplies zero product lanes by construction.

**The mechanism is the finding: the ≤1/4 cap is width-dependent, so a batch that is compliant as
planned becomes non-compliant merely by being truncated.** A cap expressed as a ratio needs a
rule for partial execution — measure against planned width, or re-check at close. Not decided
here. **Deliberately NOT backfilled** — the cap exists to leave the gap visible.

---

## 9. Wave 2 — declared, NOT dispatched, carried with reasons

Lanes d/e/f were frozen in the manifest and are **carried to the next batch, not run**:

| Lane | Row | Reason carried |
|---|---|---|
| lane-4 | [#283] corp-dedup | satellite repo lacks the enforcement organs the lane would need |
| lane-5 | [#416] ai-council codemap | same — satellite has no codemap gate to check the work |
| lane-6 | [#393] corp-sca rot | same, plus the operator control ruling |

The manifest's **serialize-group note holds**: [#430] (lane-1) and [#393] (lane-6) both declare
`serialize-group: audit-py` and were separated by wave. Wave 2 was not pulled forward, so the
pair never met — but [#430] is now partly landed, so **that pair must be re-checked before
lane-6 runs**, exactly as the manifest instructed.

Note the record contains a superseded instruction: lane-1 was told mid-session to "HOLD
integration — `/lane-integrate` runs ONCE, after wave-2's three lanes also STOP". The
integrator contract (later) overrides it: close at width 3, carry wave 2. Recorded so the
contradiction is not mistaken for a missed step.

---

## 10. Gates — before and after

**Before (main `85e18016`, at dispatch):** `audit.py health` → **OK**. No FAILs; WARNs only
(`no_ff_merges` x3 legacy June, `reconciled_versions`, `doc_rot` BACKLOG#492,
`undeclared_edges` x10, `fleet_parity` ai-council conftest, `preflight_backlog_ids`,
`review_artifact_coverage`). Suite baseline: 2 REDs.

**After:** `audit.py health` → **OK**. The `fleet_parity` conftest WARN is **gone** — cleared on
its merits by [#430](a), not dispositioned (see §4 for the caveat on that ruling). Every other
WARN is the same pre-existing set. `pre-commit run --all-files` passes every hook except one
(below). `gen_task_tree --check` and `--roundtrip` ok; `gen_audit_index --check` clean.

### [#499] line-item — local-gate false-positive count for this seal: **0**

Stated explicitly because [#499]'s evidence bar is "0 false positives over two consecutive
windows, **reported at each seal**".

`check_review_artifact_coverage` produced **zero false positives on this batch's six commits**,
verified per-commit rather than assumed:

- `e685a306` (lane-2) and `47bd4f52` (lane-1) touch `scripts/` + `tests/` and **each carries a
  parseable Tally line** — lane-2 `0/7/0/0`, lane-1 `0/2/0/0`. Correctly not flagged.
- `ea4ddf23`, `ad9332c3`, `a96040c3`, `63b7b6a9` touch **no** `scripts/` or `tests/` paths, so no
  artifact is owed. Correctly not flagged.
- The leg's single live finding names `5af0b33c` pointing at
  `2026-08-06-codex-lane-c-504-failclosed.md`, a **batch-1 carryover and a TRUE positive** (that
  artifact genuinely lacks a parseable Tally line).

**This is one window. Whether it is the second consecutive clean window is the operator's count
to make, not mine.**

### A separate gate observation, NOT an [#499] datapoint

`check-seal-identity` **FAILS under `pre-commit run --all-files`**, on
`docs/handoffs/2026-08-01-dev-knowledge-architect-2` — whose `HANDOFF_BOOT.md` declares slug
`2026-08-01-dev-knowledge-architect` while its directory is `...-architect-2`. Verified
**pre-existing and untouched by this batch**: added at `80dd54d6`, and
`git log 85e18016..HEAD -- <bundle>` is empty. It never fired on any commit in this batch,
because the hook is prospective-only on **staged** handoff files. It is a real defect in an
**immutable** artifact (`docs/handoffs/` cannot be edited), so it is reported, not fixed — and it
will keep failing every `--all-files` sweep until someone rules on how an immutable bundle with
a bad seal gets retired.

---

## 11. Lane decisions taken under V-2 budgets

**lane-1** — worked in the auto-provisioned worktree rather than re-provisioning under the
contract's name (see I-1 for what that cost); took [#490] via *declared absence* rather than
claiming 9 resolve, because 4 are genuinely unonboarded; **removed** the spent
`warn-fleet-parity-ai-council-root-conftest` disposition rather than re-wording it (operator
accepted the removal as executed, one of its two operator messages); drained 2 normative keywords
from its own prose to hold `silent_rule_ratchet` at 441 ≤ 441; made `declared_by` a validated
enum with a loader refusal. Terra: 6 findings → **0/2/0/0**, both HIGHs fixed in-lane at
`c4f505ef`, same wrong-type class.

**lane-2** — reshaped leg (a) after measuring that ai-council's *correct* `.worktreeinclude` is
**empty**, and an empty manifest still leaves every worktree broken: the need was never a file,
it was an environment. So the manifest models the copy set (hub-declared) **and** the environment
bootstrap (derived from the target's own packaging files). Found **ten defects in its own
organs**, six from the terra loop — including that its proof ran `python -m pytest`, which puts
cwd on `sys.path`, so a flat-layout package "passed" because the *proof* put it there. One terra
claim **refuted** with a sentinel probe and turned into a regression guard. Terra **0/7/0/0**,
final pass clean. Deferred by choice: no pre-commit gate on the new organs (adoption-first, the
`/preflight` precedent); no deploy-manifest carrier (needs a v1.5.0 cut + operator tag, ADR-91).

**lane-3** — swept 9 repos rather than the 3 its row names; pushed 5 repos' unpushed work
(`corp-ops` 4, `corp-sca-time-automation` 4, `demo-prep` 60, `life-architect` 4,
`corp-monorepo`'s `docs/327-interface-genre-markers`); recorded accept-local where a branch had
zero unique commits; **refused** win-tooling rather than adding a remote (out of scope) — §3.

### A lane contract violation, recorded because it changed the merge

Lane-3's frozen contract lists `JOURNAL.md` in its Do-NOT set. **It wrote one anyway**
(`d29e6b83`), under Stop-hook pressure, while lanes 1 and 2 both declined the same demand and
gave their reasons. Two consequences: it collided with AM4-FOLD's JOURNAL entry at merge (both
labelled `2026-08-07 (f)`; resolved by relabelling AM4-FOLD's to `(g)` on a 43-second timestamp
margin, both entries preserved verbatim), and it made lane-3's merge self-anchoring, which is
why only 2 merges needed R-1 rather than 3. The Stop hook is advisory in full (ADR-85 §A5), so
nothing forced this — but three lanes met the same pressure and one folded, which is a
measurement of how advisory it really is.

### An integrator-side collision worth recording

This session runs as a dispatched background job, whose isolation guard **refuses `Edit`/`Write`
in the shared checkout** and directs the session into a worktree. The integrator role cannot
comply: `/lane-integrate` must run from the primary checkout on `main`, a linked worktree cannot
check out `main`, and the session was already mid-merge with a conflict when the guard fired. The
JOURNAL and index conflict resolutions were therefore done through the shell instead. The guard
and the integrator role are in direct conflict, and this is the first batch to hit it.

---

## 12. Deferred, and to whom

1. **[#430](a)'s ruling provenance** — §4. Operator. Highest priority in this packet.
2. **`win-tooling` has no remote**, 14 local-only branches — §3. Operator; a dispatch act.
3. **The manifest's lane-grammar defect** (digit vs letter) and a `/lane-boot` refusal on a
   non-conforming branch — I-1.
4. **F2: the R-1 exemption is self-grantable by branch naming** — §2. Consolidation arc.
5. **`pre-commit` does not fire on conflict-free merges** — §2. Fold into ADR-110's amendment.
6. **The ≤1/4 process cap is width-dependent** and breaks under truncation — §8.
7. **[#505] clause 2 needs disambiguation** (per-batch vs per-integration) before it can close;
   clause 1 needs lane contracts as committed artifacts — §7.
8. **`check-seal-identity` fails `--all-files` on an immutable bundle** — §10.
9. **Wave 2 ([#283] [#416] [#393])** carried; re-check the `audit-py` serialize-group pair before
   lane-6 — §9.
10. **The bg-isolation guard vs the integrator role** — §11.

---

**Batch 2 is closed at width 3.** Three rows closed on verified evidence, one held open on its
unmet half, wave 2 carried with reasons, the quota shortfall reported and not backfilled, and
ten items deferred with owners. The R-1 mechanism fired in production for the first time and
reported itself. `SKIP=audit-health` was used zero times.
