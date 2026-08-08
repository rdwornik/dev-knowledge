# Batch 3 — consolidation report: the merge queue was NOT run, and why

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** batch-3-consolidation-report
- **Arc:** `ARC-batch3-consolidation-integrate` (v2), executed from the hub PRIMARY checkout on `main`.
- **Mechanism:** `/lane-integrate` (`.claude/commands/lane-integrate.md`), read first per the contract's AUTHORITY section.
- **Outcome:** **STOPPED at the precondition gate. Zero merges, zero teardown, zero row closes.**
  Every lane branch and worktree is exactly as its lane left it.

## 0. The STOP, stated first

`/lane-integrate`'s close-out checklist item 4 requires "the lane manifest and end-of-batch packet
are committed in the tree". **Batch 3 has no committed manifest.** The contract's own
PRECONDITION 2 pre-authorised this outcome: *"If it needs a manifest that does not exist, STOP and
report — do not back-date or fabricate one."*

That would be a reportable-but-survivable shortfall on its own. It is not survivable here, because
the same missing artifact is the key to the **ADR-110 declared-integration-arc exemption**, and
without it the merge queue is mechanically unrunnable under this contract's own prohibitions.

### The wedge, demonstrated rather than asserted

1. `audit-health` is a **pre-commit hook with `always_run: true`, `pass_filenames: false`**
   (`.pre-commit-config.yaml:121-129`). It fires on every commit that reaches the pre-commit stage,
   including a **conflicted** merge commit. (A conflict-free `git merge` runs commit-msg hooks only —
   which is why the wedge bites at the first *conflicting* merge, not the first merge.)
2. `audit.py health` exits 1 on any FAIL. `check_journal_spine_anchor` is a **FAIL-tier** check.
3. Measured, per lane, against the JOURNAL each merge would produce:

   | Lane branch | Post-merge anchoring |
   |---|---|
   | `worktree-lane-intakes-28-29` | **anchored** — its own entry names `b29b955a` |
   | the other **nine** lane branches | **UNANCHORED** — none touches `JOURNAL.md` |

4. So merge #2 onward each lands an unanchored first-parent spine entry → `journal_spine_anchor`
   FAILs → `audit-health` blocks **every subsequent conflicting merge**. **Nine of the ten lanes
   touch the generated `docs/audits/README.md` index** (each adds its own row to the same file), so
   the first of those nine merges clean and the remaining **eight conflict** — plus
   `ecosystem/doc-counts.md`, which `lane-e-gitenv-scrub` (2570) and `lane-280-315-carriers` (2582)
   both rewrite. The block is therefore hit early and then on nearly every remaining merge.
5. The exemption that exists precisely for this is `scripts/batch_manifest.py`, and it requires a
   **committed manifest declaring an open batch**. Batch 2's manifest is **closed** — its declared
   `closed_by:` packet `docs/audits/2026-08-07-technical-batch-2-packet.md` is committed — so no
   exemption is live. Confirmed in the gate's own evidence line, which carries no `EXCEPT` clause.

**`batch_manifest.py`'s own docstring states the conclusion reached independently here:** *"Anchoring
is retrospective; the commit-time backstop is not. Between merges the two cannot both be satisfied,
and batch 1 resolved it with `SKIP=audit-health`."* The only three exits are the exemption (needs
the manifest), `SKIP=audit-health`, or `--no-verify`. **The contract forbids the latter two by name
and forbids fabricating the first.** There is no fourth exit, so the queue does not start.

### Why STOPPING BEFORE merge #1 — not part-way — was the only order that delivers anything

Merging even two lanes turns `journal_spine_anchor` RED. Because `audit-health` is `always_run`,
a RED spine then blocks **every** later commit in this checkout — including the commit that lands
**this report**. A partial merge run would have left `main` half-integrated, eight lanes still open,
and no ability to write down what happened. Stopping at zero merges is what makes this artifact
possible.

## 1. Per lane / arc

### 1a. Hub batch-3 lanes — all 10 PENDING, none merged

Second-seat verification was run on all ten regardless, so the re-dispatch inherits verdicts rather
than repeating the work. Footprint read from `git diff --stat main...<branch>`.

| # | Lane branch | Tip | Rows | Footprint verdict | Second seat | Disposition |
|---|---|---|---|---|---|---|
| 1 | `worktree-lane-intakes-28-29` | `174b6ff6` | intakes #28/#29 | 5 files: JOURNAL + 2 intakes + README + manifest.json | **PASS** — both required generators present (`gen_intake_index` README **and** `gen_intake_tree` manifest.json) | PENDING — carries the `(d)` collision, see 1b |
| 2 | `worktree-lane-e-gitenv-scrub` | `9ac62422` | [#396] [#512] | 11 files, code lane, confined | **PASS** — terra artifact present, **Tally 0/5/0/0** cumulative over 5 passes; the review demonstrably ran | PENDING |
| 3 | `worktree-lane-290-floor-teeth` | `b6d81501` | [#290] | 5 files, code lane, confined | **PASS** — terra artifact, **Tally 0/0/0/0** final over 15 passes | PENDING |
| 4 | `worktree-lane-280-315-carriers` | `6423df11` | [#280] [#315] | 8 files, code lane, confined | **PASS** — terra artifact, **Tally 1/1/0/0**; the CRITICAL was closed on-lane by `295f3594` | PENDING |
| 5 | `worktree-lane-506-groom-sheet` | `98f5afd9` | [#506] evidence | **2 files** — report + index row | **PASS** (structural) | PENDING |
| 6 | `worktree-lane-c-393-rot` | `719b6b61` | [#393] | **2 files** | **PASS** (structural) | PENDING |
| 7 | `worktree-lane-archival-audit` | `2c198067` | archival lifecycle | **2 files** | **PASS** (structural) | PENDING |
| 8 | `worktree-lane-502-pythonpath-measure` | `23198aae` | [#502] | **2 files** | **PASS** (structural) | PENDING |
| 9 | `worktree-lane-seeded-defect-substrate` | `b014baf6` | [#491] [#492] | **2 files** | **PASS** (structural) | PENDING |
| 10 | `worktree-lane-wave-closures` | `139d6689` | [#506] proposals | **2 files** | **PASS** (structural) | PENDING |

**Every report lane is exactly 2 files** — its report plus the mandated `docs/audits/README.md`
index row. No `tasks/`, no `BACKLOG.md`, no `JOURNAL.md` on any of the six. The contract's
structural check passes on all six with no exceptions.

**Lane E's review ran** — the contract asked this to be confirmed specifically. It did: five passes,
cumulative tally 0/5/0/0, with an explicit in-artifact note that the script's *heuristic* tally
(`0/0/0/0` on pass 3, `0/2/0/0` on pass 4) disagreed with the counted findings and that the counted
number is authoritative.

**Merge-order and conflict rulings are unused** — no merge was attempted, so the `(d)`-collision
renumber, the generated-file rulings, the `deploy/tool.py` both-registrations ruling, and the
`f3134310` STAYS ruling are all **carried forward unexercised** to the re-dispatch.

### 1b. The JOURNAL letter collision — confirmed, unresolved

`main` carried 2026-08-08 entries **(a)–(e)** on arrival. `worktree-lane-intakes-28-29` carries its
own **(d)**.

**The renumber target is `(g)`, not `(f)` — and this arc is why.** This report's own JOURNAL entry
takes **(f)** when it lands, so by the time the intakes lane is merged the next free letter has
moved on by one. Stated explicitly because the contract, written before this arc ran, would have
said (f), and a re-dispatch reading only the contract would collide a second time.

Not applied here: applying it means committing on the lane branch, which a stopped batch has no
authority to do.

### 1b-bis. Conflict map, computed — hand this to the re-dispatch

Measured from `git diff --name-only main...<branch>`, so the integrator does not rediscover it:

| Generated file | Lanes that rewrite it | Consequence |
|---|---|---|
| `docs/audits/README.md` | **9** — every lane except `intakes-28-29` | first merges clean, the other **8 conflict**; never hand-resolve — take either side, then `python scripts/gen_audit_index.py --write` |
| `ecosystem/doc-counts.md` | **2** — `e-gitenv-scrub` (2555→2570), `280-315-carriers` (2555→2582) | second one conflicts; resolve by `python scripts/gen_doc_counts.py --write` after both land, **not** by picking a number |
| `JOURNAL.md` | **1** — `intakes-28-29` only | conflicts with `main`'s (a)–(e); keep both sides, renumber the incoming `(d)` to `(f)` |
| `BACKLOG.md`, `tasks/` | **0** | no lane touches either — the contract's "no `tasks/`/`BACKLOG.md` except intakes" check passes trivially |

The doc-counts figure to expect after **all** lanes land is neither 2570 nor 2582: both lanes
counted from a 2555 base independently, so the merged total must be regenerated, not summed.

### 1c. Consumer lanes merged into satellites earlier today — all VERIFIED LANDED

These are outside the hub merge queue and were already complete before this arc began.

| Repo | Merge SHA | Lane branch | Row | Pushed |
|---|---|---|---|---|
| `corp-monorepo` | `37b8aa1` | `worktree-lane-a-283-dedup` | [#283] | yes — `origin/main` at the merge |
| `ai-council` | `4d2a63c` | `worktree-lane-b-416-codemap` | [#416] | yes |
| `corp-ops` | `3bde930` | `worktree-lane-d-282-eol` | [#282] | yes |
| `corp-sca-time-automation` | `1a80a9e` | `worktree-lane-d-282-eol` | [#282] | yes |
| `demo-prep` | `d849c81` | `worktree-lane-d-282-eol` | [#282] | yes |

**Note the contrast, because it is diagnostic:** every satellite lane branch conforms to the
ratified enum `lane-<letter>-<id>-<slug>`. Nine of the ten *hub* lanes do not. See finding F3.

### 1d. `win-tooling` private-remote arc

- **Remote established:** `origin` points at the `rdwornik/win-tooling` GitHub remote. Verified.
- **Branches pushed:** all **15** local branches have an `origin/` counterpart, plus `origin/main`.
  Verified by `git branch -a`.
- **`main` at** `d743937` (`Merge branch 'feat/dispatch-v2'` — the contract-file-as-dispatch-source
  change this arc's own dispatch block uses).
- **gitleaks clean / clone-verified:** **asserted by the contract, NOT verifiable from repo state.**
  No gitleaks report or clone-verification artifact exists in `win-tooling`, and a
  `git log --all --grep` for either returns nothing. Recorded as operator testimony, not as a
  checked fact.

## 2. Velocity block — the 169-vs-202 disagreement RECONCILED

Both readings are correct. They count different sets, and neither is wrong.

- **169** = `tasks/*.md` files with `status: open` — the tasks/ source-of-truth tree, open only.
- **202** = task **rows rendered into `BACKLOG.md`**, which is what `validate_backlog` reports
  (`validate_backlog: OK (9 themes, 26 stories, 202 tasks, 1 warning(s))`).

**The difference is exactly the 33 `status: deferred` rows: 169 + 33 = 202.** `BACKLOG.md` renders
open **and** deferred; the boot-time reading filtered to open only.

Full tally of the 249 files in `tasks/` (248 task records + `tasks/README.md`, which carries no
`status:`):

| status | count | rendered into BACKLOG.md |
|---|---|---|
| open | 169 | yes |
| deferred | 33 | yes |
| closed | 44 | no (retire-not-delete) |
| superseded | 1 | no |
| retired | 1 | no |
| **rendered total** | **202** | — |

**Enumeration filter to name when quoting either number:** `status: open` (169) versus
`open + deferred`, i.e. the rendered BACKLOG surface (202).

**Opened / closed / net for this batch: 0 / 0 / 0.** No row was opened or closed by this arc —
the batch stopped before its close-out. Open-total is unchanged at **169 open / 202 rendered**.

## 3. Gate state

**Before and after are identical**, because nothing was committed to `main` by this arc before this
report's own branch.

- **Ship-gate: GREEN** — `audit.py ship-gate` → `verification organs green against this arc
  (18 WARN dispositioned)`. Every WARN carries a disposition; zero blocking verdicts.
- **`audit.py health`: OK.**
- **`journal_spine_anchor`: PASS** — *"every first-parent spine entry above the ADR-85 disposition
  floor `24882f8cc` is JOURNAL-anchored"*, with **no** `EXCEPT` clause, confirming no batch
  exemption is live.
- **`git stash list`: empty.** `/lane-integrate` checklist item 5 passes on entry.
- **Organs that moved: none.** No merge, no commit to a gated surface, no generator run.

### 3a. PRECONDITION 1 of the contract is FACTUALLY FALSE — reported, not worked around

The contract opens: *"`journal_spine_anchor` is hard-RED on `ae339ace` … it also RED-blocks
`audit-health` at pre-commit and causes 2 of the 4 current suite failures. Repair by extending the
2026-08-08 JOURNAL entry…"*

**No such RED exists.** Verified three independent ways:

1. `audit.py health` → `[OK] journal_spine_anchor`, `health: OK`.
2. `audit.py ship-gate` → GREEN.
3. Directly through the shared predicate: `journal_anchor.unanchored_on_spine(main, floor)` returns
   **`[]`** — zero unanchored entries above floor `24882f8cc`.

`ae339ace` **is** anchored: it introduced `{a343f6ad, 8f09c12d, be23aa1b, 78cb6fab, 489f67e6,
2bd91563, 4d7b5cbf}`, and the 2026-08-08 **(e)** JOURNAL entry names `8f09c12d`. The predicate is
"names at least one SHA the entry INTRODUCED", and it is satisfied.

**No repair was performed, because performing one would have been fabricating a fix for a defect
that does not exist** — and the prescribed repair (extending the (e) entry) would have edited a
JOURNAL entry that is already correct. The contract's premise appears to predate commits
`8f09c12d` / `a343f6ad`, which cleared the day's held RED before this arc was dispatched.

## 4. `/lane-integrate` divergences from this contract

The contract asked for this list as a deliverable. **Where they disagree, the command wins.**

| # | Contract | `/lane-integrate` | Resolution |
|---|---|---|---|
| **D1** | PRECONDITION 3: *"Live inventory: enumerate from git … This inventory, **not this contract**, is the merge queue's source of truth."* | §1: *"The queue is the lane list from the batch's **plan** — not whatever branches happen to exist. A branch present but absent from the plan … is itself a finding."* | **Direct contradiction.** Command wins → the queue must come from a committed plan. **Batch 3 has no plan in the tree**, so under the command the queue is *unbuildable*, and under the contract every branch is authoritative. This is the manifest gap wearing a second face. |
| **D2** | Checklist not mentioned. | §3 item 4 requires manifest **and** packet committed. | Command adds the requirement the contract omits. **This is the STOP.** |
| **D3** | *"Restore green: … Then full suite + ship-gate on the merged result"* — one suite at the end. | §2: `uv run --locked pytest -q` **after each merge**. | Command is stricter: **10 full suites, not 1.** At this suite's runtime that is a materially different batch cost, and the re-dispatch should budget for it. |
| **D4** | *"ONE JOURNAL entry as the **LAST commit before pushing**"* | §3: push after the checklist; JOURNAL unmentioned. | **The contract's shape is not achievable as written.** A JOURNAL-only commit made while standing on `main` is a non-merge commit on the first-parent spine — core-invariant #5 forbids it and `block_ff_push` refuses the push. A JOURNAL-only *wrap branch* is structurally unanchorable (its merge introduces only the entry, which cannot name itself). The entry must ride a branch that also carries other commits. |
| **D5** | Teardown *"whatever four-step the command specifies"*. | §2 teardown = `worktree remove` + `prune` + `branch -d`; `.claude/rules/git-discipline.md` adds **"teardown is TWO branches"** (work + provisioning). | No conflict. Note for the re-dispatch: batch-3 lanes are native CC worktrees where the work branch **is** `worktree-lane-*`, so the two collapse to one — do not hunt a second branch that never existed. |
| **D6** | Report at a named path *"in addition to whatever packet the command produces"*. | §4: emit **one** end-of-batch packet. | Contract supplements; two artifacts are intended. Only this report exists — there was no batch to packet. |
| **D7** | Merge-order preference (intakes → E → 290 → 280/315 → reports). | §1–2: order follows the plan; one merge at a time. | Compatible; the contract supplies the order the absent plan would have. |

**Also recorded, though not a command divergence:** the contract's PRECONDITION 1 is factually
false (§3a), and its acceptance item *"Spine GREEN before the first merge"* was satisfied on
arrival rather than by repair.

## 5. Findings carried, not fixed

Carried verbatim from the contract, plus four this arc surfaced. **None was fixed** — the contract
forbids it.

**Surfaced by this arc:**

- **F1 — the missing batch-3 manifest.** Batch 2 committed one at dispatch as its condition 1;
  batch 3 did not. It is not a bookkeeping gap: it is the load-bearing key to the ADR-110
  exemption, and its absence is what stops the batch. *A finding about the dispatch, not about the
  lanes.*
- **F2 — batch-3 lane contracts are not repo artifacts.** Every contract this batch ran on lives in
  `~/Downloads` (`$env:CLAUDE_PROMPTS_DIR` did not expand at dispatch — this integrator's own
  contract path arrived as a literal `\ARC-batch3-consolidation-integrate.md`). Batch 2's packet
  had already named the fix — *"lane contracts must be committed artifacts, referenced by the
  manifest… That is one change away"* — and batch 3 did not take it.
- **F3 — nine of ten hub lane branches violate the ratified lane-name enum.**
  `validate_branch_naming.py` requires `lane-<letter>-<id>-<slug>`. Only `lane-c-393-rot` passes;
  `lane-290-floor-teeth`, `lane-e-gitenv-scrub`, `lane-intakes-28-29`, `lane-280-315-carriers`,
  `lane-506-groom-sheet`, `lane-archival-audit`, `lane-502-pythonpath-measure`,
  `lane-seeded-defect-substrate` and `lane-wave-closures` all FAIL. The validator exists and is
  correct; **nothing runs it at provisioning** (`/lane-boot` §1 asks the operator to, and that is
  the whole enforcement). Every *satellite* lane the same day conformed — so this is a hub-side
  dispatch-discipline gap, not a broken validator.
- **F4 — two different definitions of "a lane branch" ship in the same repo.**
  `validate_branch_naming.LANE_BRANCH_RE` is `^worktree-lane-[a-z]-\d+-<slug>$` (strict) versus
  `batch_manifest.LANE_BRANCH_RE` at `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$` (loose). All ten
  batch-3 branches match the loose one and nine fail the strict one. `journal_anchor.py`'s own
  docstring states the standard being broken here: *"A second definition is a drift edge, not a
  convenience."* Consequence, and it cuts the safe way: had a manifest existed, the exemption would
  have applied to all ten off-enum branches.

**Carried from the contract, unmodified.** Three were spot-verified against live state in passing and
are marked **[verified]**; the rest are relayed as the contract stated them and carry no
independent check from this arc.

- The unattributed HEAD-swap pattern (n=5).
- **[verified]** The stale "(hard)" label on an advisory stop-hook leg — `session_end_backpressure.py:332`
  still emits `JOURNAL (hard): …` while CLAUDE.md §9 and the ADR-85 amendment §A5 make that hook
  **advisory in full**, unable to block a turn. Note for whoever fixes it: the stale wording is
  **test-pinned** — `tests/test_session_end_backpressure.py` asserts the literal `"JOURNAL (hard)"`
  in five places, one carrying the comment *"the leg's own wording is unchanged; its EFFECT is
  not"* — so the repair is a two-file change, not a one-word one.
- The xdist instrument defect — the parallel aggregate undercounts import breakage; isolated
  collection is the admissible evidence.
- **[verified]** `ESSENTIALS.md`'s forward-dated stamp defeating freshness structurally — confirmed,
  and the mechanism is worth stating precisely because it is invisible if you compare the stamp to
  *today*. Commit `e0528cc3` was **authored 2026-07-29** and set `last_reviewed: 2026-07-30`. The
  A2 check fails when a stamp *predates* the file's last edit; a stamp dated one day **after** its
  own edit can never be predated by that edit, so the edit is permanently immune. The stamp reads
  as ordinary past-dated text now (9 days old, inside the 30-day backstop) — the defect is in the
  stamp-vs-commit relationship, not the stamp-vs-today one.
- The applied-but-unwritten ADR archival "zero-refs bar".
- `ADR-45`'s self-contradiction.
- **[verified]** `docs/audits/README.md:5` pointing at closed `[#212]` — confirmed dead: no
  `tasks/212-*.md` exists and `[#212]` appears **zero** times in `BACKLOG.md`. Note for whoever
  fixes it: that README is **generated**, so the repair belongs in `gen_audit_index.py`'s header
  template, not in the output file.
- `ADR-100`'s unbuilt index split.
- `ADR-98 §6`'s fired survival trigger.
- **[verified]** `audit.py:3004`'s unscrubbed `_git` — confirmed: it calls
  `subprocess.run(["git", *args], cwd=str(repo_path), …)` with **no `GIT_*` scrub and no `-C`**, so
  an inherited `GIT_DIR` overrides `cwd`. This is the same defect class lane E's `scripts/gitenv.py`
  was built to remove, in a module lane E did not reach.
- `corp-sca`'s `CLAUDE.md` denying a hook that fires.
- `ai-council`'s `healthcheck → providers` layer inversion.
- **[verified, with a correction]** The intake area's two generators with only one hooked —
  `intake-index-freshness` is the **only** intake hook in `.pre-commit-config.yaml` and it gates
  `gen_intake_index.py` alone; `gen_intake_tree.py` (which writes `docs/intake/manifest.json`) has
  no regen hook. **But it is not ungated:** its output is checked by `intake_tree_coherence` under
  `audit-health`, which is FAIL-tier — so forgetting the second generator blocks the commit anyway,
  just with a coherence error rather than a regen-and-diff. The `worktree-lane-intakes-28-29` lane
  ran **both**, so this batch does not exercise the gap.
- The consumer intake README's 23 dead links (pegged before v1.4.0 is tagged).

## 6. Row closes — NONE EXECUTED, each assessed for readiness

The contract named eight rows to close plus one to assess. **No row was closed**: six of the eight
depend on hub lane merges that did not happen, and executing the three that are independently
evidenced would have mutated `BACKLOG.md` mid-stopped-batch for no gain — the re-dispatch closes
them in one pass. Readiness is recorded so that pass is mechanical.

| Row | Evidence | Ready to close? |
|---|---|---|
| [#283] | `corp-monorepo` `37b8aa1`, pushed | **YES** — independently landed, evidence outside the hub queue |
| [#416] | `ai-council` `4d2a63c`, pushed | **YES** — same |
| [#282] | `corp-ops` `3bde930`, `corp-sca` `1a80a9e`, `demo-prep` `d849c81`, all pushed | **YES** — same, three repos |
| [#396] [#512] | lane E, `9ac62422` | **NO** — awaits merge |
| [#280] [#315] | lane 280/315, `6423df11` | **NO** — awaits merge |
| [#290] | lane 290, `b6d81501` | **NO** — awaits merge |
| [#506] | — | **NO — and left open deliberately** per the contract (evidence half only) |
| [#502] | lane 502, `23198aae` | **NO — left open deliberately** per the contract (measurement delivered; adoption ruled to batch 4) |

### [#505] — assessed line by line. **VERDICT: DO NOT CLOSE. Two legs unmet.**

The row's four "Done when" legs:

1. **"a fresh seat runs a full batch from repo artifacts alone" — UNMET, and batch 3 REGRESSED it.**
   Batch 2's packet already returned *"clause 1 stays falsified"* and pinned the remaining gap
   precisely: *"lane contracts must be committed artifacts, referenced by the manifest. That is one
   change away."* Batch 3 not only failed to take that change, it removed the manifest as well — so
   a fresh seat inheriting batch 3 finds **neither** the contracts **nor** the plan in the tree.
   This report's own STOP is the demonstration.
2. **"batch-1 executes under it with exactly 2 operator touches" — UNMET / ambiguous, unchanged.**
   Batch 2 measured it and got two defensible answers: **7** per-batch (falsified) and **2**
   per-integration (met, and it is what `/lane-integrate` §0 actually says). Its verdict —
   *"clause 2 needs disambiguation before it can be closed"* — still stands; nothing in batch 3
   disambiguated it.
3. **"hygiene WARN and branch-prefix enum are validator-checked" — MET as written.**
   `audit.py::check_stale_worktrees` carries the hygiene WARN; `validate_branch_naming.py` checks
   the enum. **But see F3:** checked is not enforced — 9/10 lanes were provisioned off-enum in the
   very batch that ran under this protocol.
4. **"the refuse-to-finish checklist is mechanical" — MET as written.** `/lane-integrate` §3 is a
   five-item table where each item names the command that checks it. The command's own honest limit
   ("this is a command, not a gate") is consistent with the row, which asked for *mechanical*, not
   *gated*.

**Legs 1 and 2 are unmet. The row stays open.**

## 7. Teardown ledger

**EMPTY BY CONSTRUCTION — no teardown was performed, and none was permissible.** A branch is never
deleted before its content is verified on `main`; nothing reached `main`.

State on exit, unchanged from entry:

- **13 worktrees registered** (1 primary + 12 linked). 8 are `locked`.
- **10 lane branches** carry unmerged work; 3 further worktrees
  (`lane-batch4-prep`, `lane-integrate-consumers`, `lane-wintooling-remote`) sit at `3ed60c4c`,
  which **is** an ancestor of `main` — their work is already integrated and only the worktrees
  remain. They are the cheapest teardown available to the re-dispatch, and the only ones whose
  content is already verified on `main`.
- `git stash list` — **empty**.
- `automation/fleet-audit` is unmerged **by design** (its dailies never reach `main`) — not a
  batch-3 lane, not in the queue, not to be deleted.

**F1 verify-before-destroy was therefore never exercised. Protected worktrees were never
approached:** `demo-prep`'s `fix/audit-needs-input`, `corp-monorepo`'s foreign `vk/c35d-test`, and
`corp-sca`'s `feature/tenrox-loader` are all untouched and confirmed present.

## 8. What is owed next

**To unblock this batch — the operator's ruling is required. Two clean options:**

- **(A) Commit a batch-3 manifest now, dated today, describing the batch as it actually ran**, with
  `closed_by:` naming its end-of-batch packet — then re-dispatch the integrator. This is *not* the
  back-dating the contract forbids: it is a present-tense declaration that a batch is open, which
  is what the artifact means. It restores the ADR-110 exemption and the queue runs.
- **(B) Rule the exemption unnecessary for this batch** and authorise a named, logged bypass. This
  is the option the contract closed off, and it should stay closed unless (A) is rejected.

Either way the re-dispatch inherits from this report: the live inventory, ten second-seat PASSes,
the merge order, the `(d)`-to-`(f)` renumber, and the conflict rulings — all carried, none consumed.

**Carried forward from the contract, unchanged:**

- The consolidated post-integration write: the A7(d) row, intake #25 flip, the velocity law
  (§2 above supplies the reconciled numbers and the filter it needs), seam-name alignment, the
  zero-refs bar, two LESSONS entries, and the `[#502]` adoption ruling.
- The closure-adjudication wave.
- Batch-4 planning inputs.

**Added by this report:**

- Decide **F3/F4**: reconcile the two lane-branch regexes to one definition, and decide whether
  `/lane-boot`'s enum check becomes a gate rather than an instruction.
- Take the change batch 2 already named: **lane contracts as committed artifacts referenced by the
  manifest** — the single change that moves [#505] leg 1.
- Disambiguate **[#505] leg 2** (per-batch vs per-integration touch counting) so the row can ever
  close.

## 9. SELF-TEST against the contract's frozen acceptance list

Run against the contract's own checklist, honestly, before STOP.

| # | Acceptance item | Verdict |
|---|---|---|
| 1 | `lane-integrate.md` read; command used as mechanism; divergences listed | **PASS** — read before anything else; 7 divergences at §4 |
| 2 | Spine GREEN before first merge and before push; zero `SKIP=` / `--no-verify` | **PASS** — GREEN on arrival and at exit; **zero** bypasses used anywhere in this arc |
| 3 | Batch-manifest precondition checked and state reported (STOP if the command requires one that is absent) | **PASS** — checked, absent, reported, **STOPPED** |
| 4 | Live inventory recorded; every branch merged (SHA) or skipped (reason); second-seat verdict per branch incl. PASSes | **PARTIAL** — inventory recorded and all 10 second-seat verdicts given; **no merge SHAs**, single blocking reason recorded for all 10 |
| 5 | Named rows closed with evidence; [#505] assessed; [#502]/[#506] left open | **PARTIAL** — [#505] assessed with a stated verdict (do not close, 2 unmet legs); [#502]/[#506] left open; **the eight closes were NOT executed** (§6, with readiness per row) |
| 6 | Suite + ship-gate on merged result; residuals classified | **PARTIAL** — ship-gate GREEN and the suite run on **current `main`** (§10); there is no merged result to judge |
| 7 | Teardown ledger with F1 evidence; protected worktrees untouched | **PARTIAL** — ledger at §7 is empty by construction; protected worktrees confirmed untouched |
| 8 | Report exists at the named path covering all six sections | **PASS** — this file; all six sections plus the STOP, the divergence list, and this self-test |

**Four PASS, four PARTIAL, zero silent skips.** Every PARTIAL traces to the single STOP at item 3.

## 10. Suite on current `main`

`uv run --locked pytest -q` from the primary checkout at `ae339ace`, nothing merged:

```
1 failed, 2550 passed, 4 skipped in 1903.85s (0:31:43)
```

**2550 + 4 + 1 = 2555 — exactly the `tests: 2555 collected` claim in `ecosystem/doc-counts.md`.**
The count claim is accurate against live state.

### The one failure, classified

`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`

```
AssertionError: assert '1 declared routine row' in
  '2 declared routine row(s) name a consumer and a consumption_path ...'
```

**PRE-EXISTING.** This is the first of the two failures the contract named — *"the routine-consumers
row-count test (live BACKLOG has 2 routine rows, test pins 1)"* — reproduced exactly. Not
merge-caused (nothing was merged) and not teardown-clearable. The test's own docstring says the fix
is a coordinated one: *"If this number moves, the ADR, the docstring and [#426] must move with it."*

### The second known pre-existing failure did NOT occur

The contract predicted *"the linked-worktrees reader inversion — re-check the latter after teardown,
it may clear once the worktrees are gone."* It **passed here, with all 12 linked worktrees still
present.** That test inverts when the suite runs *from inside a lane worktree*, not from the
primary; run from the primary it is green regardless of how many worktrees exist. **Teardown is not
required to clear it, and the re-dispatch should not wait on teardown expecting it to.**

### This also refutes the rest of PRECONDITION 1

The contract asserted *"4 current suite failures"*, of which *"2"* were attributed to the spine RED.
**There is 1 failure, and zero are spine-related** — consistent with §3a, where the spine is GREEN.
Three of the four predicted failures do not exist.

### Timing — a hard input for the re-dispatch, and for divergence D3

**One full suite run costs 31m43s on this machine** (16 cores, `addopts = "-n auto"`). `/lane-integrate`
§2 mandates a full suite **after every merge**. At 10 lanes that is **roughly 5.3 hours of suite time
alone**, before conflict resolution, generator regeneration or the close-out. Whoever re-dispatches
should either budget for it explicitly or obtain a ruling to batch the suite across merges — it is
not a detail that absorbs quietly into an evening.

---

## AMENDMENT — 2026-08-08, same session, correcting §7's worktree line

`docs/audits/` is immutable (CLAUDE.md §5 rule 3), so this corrects the line by marker rather
than by edit. **§7's bullet reading "13 worktrees registered (1 primary + 12 linked). 8 are
`locked`." is wrong on both numbers, and the two are wrong for different reasons.**

| | §7 as written | Correct | Why it was wrong |
|---|---|---|---|
| Registered worktrees | 13 (1 primary + 12 linked) | **14 (1 primary + 13 linked)** | **Author arithmetic error.** `git worktree list` returned 14 lines at inventory time and still does; the report miscounted its own input. |
| Locked | 8 | **1** (`lane-290-floor-teeth` only) | **Genuine state change, not a misread.** 8 were `locked` at inventory (~20:45); 1 is locked now (~22:00). Lane sessions released their locks while this arc ran. |

**Neither correction changes any conclusion.** The STOP rests on the missing manifest and the
anchoring arithmetic, not on worktree counts. But §7 is the teardown ledger — the section a
re-dispatch acts on directly — so a wrong count there is the kind that propagates into a
destructive step.

**Two consequences the re-dispatch should carry:**

1. **Teardown scope is 13 linked worktrees and 13 `worktree-lane-*` branches, of which 10 carry
   unmerged work.** The other three (`lane-batch4-prep`, `lane-integrate-consumers`,
   `lane-wintooling-remote`) sit at `3ed60c4c`, already an ancestor of `main` — verified-on-main
   and therefore safe to tear down first.
2. **Lock state is not a stable property.** It changed by 7 worktrees inside 75 minutes with no
   teardown performed. `/lane-integrate` §2 already warns that `git worktree remove` silently
   no-ops on a locked directory and says to re-check rather than assume; this is a live instance
   of why. Read lock state at the moment of removal, never from an earlier inventory — including
   the one in §7 of this report.

---

## AMENDMENT 2 — 2026-08-08: the batch WAS integrated. §0's STOP is superseded.

`docs/audits/` is immutable, so the integration outcome is recorded by marker rather than by
rewriting the sections above. **Everything above this line remains an accurate record of the first
attempt.** What changed is the world, not the report: the operator ruled **option (A)** of §8 —
commit a manifest, present-tense — and the batch then integrated cleanly.

**Superseded by this amendment:** §0 (the STOP), §1a's ten `PENDING` dispositions, §6's "NONE
EXECUTED", §7's empty teardown ledger, and the four `PARTIAL` verdicts in §9. **Not superseded:**
the second-seat verdicts, the divergence table (§4), the conflict map (§1b-bis), the velocity
reconciliation (§2), the `[#505]` assessment (§6), and every finding in §5 — all accepted as final
by the re-dispatch and carried unchanged.

### A2.1 — The unblock

`docs/audits/2026-08-08-technical-batch-3-manifest.md` (`0476e4ce`, merged `121499da`) declares
batch `3` open with `closed_by:` naming a packet that did not yet exist. The gate immediately began
reporting the exemption in its own evidence line rather than applying it silently:

```
[OK] journal_spine_anchor: ... EXCEPT 8 lane merge(s) exempt under the ADR-110
declared-integration-arc rule while batch 2026-08-08-batch-3 is open ... the exemption
expires when docs/audits/2026-08-08-technical-batch-3-packet.md lands
```

**Zero `SKIP=`, zero `--no-verify`, zero force-pushes across both attempts.**

One defect was introduced and caught in the same session: the manifest's `batch:` field first
carried the batch's human name (`2026-08-08-batch-3`) rather than a digit string, which the
**pre-existing** `test_the_live_repos_own_manifest_is_well_formed` asserts. The exemption worked
anyway — `open_batches` reads `batch:` as free-form — so this was a defect that left the mechanism
functional, the kind that survives a batch. Corrected to `batch: 3` (`453089c2`, merged `89b8d401`)
with its own in-file amendment marker.

### A2.2 — Merge ledger: ten lanes, ten SHAs, zero skipped

| # | Lane branch | Merge SHA | Conflicts, and how resolved |
|---|---|---|---|
| 1 | `worktree-lane-intakes-28-29` | `d608b6f3` | `JOURNAL.md` — both sides kept, incoming `(d)` renumbered to **`(i)`** |
| 2 | `worktree-lane-e-gitenv-scrub` | `764f06c8` | `docs/audits/README.md` — regenerated |
| 3 | `worktree-lane-290-floor-teeth` | `2928cf1c` | `docs/audits/README.md` — regenerated |
| 4 | `worktree-lane-280-315-carriers` | `946d904a` | index **+** `ecosystem/doc-counts.md` — both regenerated |
| 5 | `worktree-lane-506-groom-sheet` | `15cc3ec9` | index — regenerated |
| 6 | `worktree-lane-c-393-rot` | `08aea7a7` | index — regenerated |
| 7 | `worktree-lane-archival-audit` | `2732f166` | index — regenerated |
| 8 | `worktree-lane-502-pythonpath-measure` | `e3821ae1` | index — regenerated |
| 9 | `worktree-lane-seeded-defect-substrate` | `1a4b11bb` | index — regenerated |
| 10 | `worktree-lane-wave-closures` | `87b993af` | index — regenerated |

**No generated file was hand-resolved.** Every conflict was unblocked with `checkout --ours` and
then overwritten by its generator, so the committed state is generator output in every case.

**The doc-counts prediction held.** Lane E carried 2555→2570 and lane 280/315 carried 2555→2582,
both counted independently from the same base. The merged truth is **neither**: regenerated to
**2721** = 2555 + 15 + 27 + lane 290's 124 new tests. A merge that picked either side would have
committed a number nobody counted.

**`deploy/tool.py` auto-merged with BOTH carrier registrations**, per the ruling — verified in
`make_carriers`, which now returns `FloorCarrier` (lane 290) and `DocsCarrier` (lane 280/315)
alongside the four pre-existing carriers. Checked, not assumed.

**Lane 290's `f3134310` stayed**, per the ruling — its terra artifact is present on the merged tree.

### A2.3 — F3 required NO renames

The nine non-conformant branch names never blocked a merge. `batch_manifest.LANE_BRANCH_RE` is the
looser `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$` and all ten matched it, so the exemption applied
without touching a name. **F3 and F4 are carried, not repaired** — and F4 is now load-bearing
rather than theoretical: the two regexes disagreeing is precisely what let this batch integrate.
A future tightening of `batch_manifest`'s pattern to match `validate_branch_naming`'s would have
made nine of these ten merges non-exempt.

### A2.4 — Row closes: eight closed, three deliberately left open

Retire-never-delete (ADR-107 §6.3): node out of `tasks/manifest.json`, task file **kept** with
`status: closed` as the id's allocation record. `BACKLOG.md` regenerated with `--emit-source`;
`gen_task_tree --check` ok. Commit `f98d1262`.

Evidence was verified **by content**, not by the existence of a `closes` tag:

- **[#396] [#512]** — `764f06c8`. `scripts/gitenv.py` is a genuine stdlib-only leaf (its only
  imports are `__future__`, `os`, `subprocess`); `audit.py`, `batch_manifest`, `fleet_parity` and
  `fleet_analytics` all resolve to it; `fleet_parity` aliases it directly, `fleet_analytics`
  delegates, and `audit.py` loads it **by path** with the lazy-import constraint and its outcome
  stated in-file.
- **[#280] [#315]** — `946d904a`. `deploy/carrier_docs.py` + `manifest-v1.4.0.yaml`; `DocsCarrier`
  registered in `make_carriers`.
- **[#290]** — `2928cf1c`. `deploy/carrier_floor.py` teeth + `tests/test_deploy_floor.py`.
- **[#283]** — `corp-monorepo` `37b8aa1`, 98-line disposition artifact.
- **[#416]** — `ai-council` `4d2a63c`, ARCHITECTURE.md codemap 151+/47−.
- **[#282]** — `corp-ops` `3bde930`, `corp-sca` `1a80a9e`, `demo-prep` `d849c81`. `.gitattributes`
  **sha256-identical** to the `ai-council` referent in all three — hashed and compared, not eyeballed.

**Left open, with reasons:** **[#505]** (legs 1 and 2 unmet; batch 3 regressed leg 1 — this
manifest is a partial repair, not a discharge), **[#502]** (measurement only; adoption ruled to
batch 4), **[#506]** (evidence half only).

### A2.5 — Final velocity

- **Opened 0 · closed 8 · net −8.**
- **Open total: 161** (`status: open`) — down from 169.
- **Rendered total: 194** = 161 open + 33 deferred, which `validate_backlog` confirms
  (`9 themes, 26 stories, 194 tasks`). The §2 filter still holds: quote `status: open` for 161,
  or the rendered surface for 194.
- Closed-file count 44 → **52**, consistent with 8 retirements.

### A2.6 — Teardown ledger, completed

F1 verify-before-destroy on every removal: each branch was confirmed an **ancestor of `main`**
before deletion, and `git branch -d` (never `-D`) was the safety net — it refuses an unmerged
branch, so the check could not be bypassed by mistake.

- **14 registered worktrees → 1** (primary only). **13 lane branches → 0.**
- All 13 removed cleanly; **zero** `worktree remove` no-ops, re-checked on disk after each.
- **One stale lock cleared, not forced.** `lane-290-floor-teeth` was locked by
  `claude session … (pid 36568)`; the pid was verified **dead** before unlocking. A live pid would
  have been a SKIP — another session's worktree is not this integrator's to kill.
- **Three empty leftover directories removed** — `.claude/worktrees/lane-a-283-dedup`,
  `lane-b-416-codemap`, `lane-d-282-eol`, residue of the satellite consumer lanes. Each was proven
  to hold **0 entries and 0 tracked files** first, and removed with `rmdir` (which refuses a
  non-empty directory) rather than `rm -rf`. `.claude/worktrees/` is now empty — §5 rule 9's
  "no leftovers" round-trip satisfied.
- `git stash list` **empty** throughout.
- **Protected and untouched, confirmed present:** `demo-prep`'s `fix/audit-needs-input`,
  `corp-monorepo`'s `vk/c35d-test`, `corp-sca`'s `feature/tenrox-loader`. No hub teardown reaches
  another repo.
- `automation/fleet-audit` deliberately retained — its dailies never reach `main`.

The audit organ confirms it independently: `stale_worktrees: no linked worktrees registered
(primary only) — nothing to close out` and `git stash list is empty`.

### A2.7 — Final gate state, and the suite classified

**Ship-gate: GREEN** — *"verification organs green against this arc (18 WARN dispositioned)"*.
Same 18 as the pre-integration baseline; **no new undispositioned WARN was introduced by any of
the twelve merges.**

Organs that moved:

- `journal_spine_anchor` — now reports **batch `3`** open (the corrected field) and names the
  packet that will expire the exemption. It has since expired: this packet is committed.
- `stale_worktrees` — 13 linked worktrees → **primary only**.
- `doc_claims` — 3 → **4** self-claims matching repo state.
- `intake_tree_coherence` — 261 → **263** nodes (intakes #28/#29).
- `doc-counts` — `tests: 2555` → **2721 collected**.
- `git_backlog_drift` — still WARNs `#505 closed-but-present`, unchanged and still dispositioned.
  That is correct and deliberate: **[#505] stays open**, so the row remains in `BACKLOG.md`.

**Full suite on the merged result: 2715 passed, 3 skipped, 1 xfailed, 2 failed in 8m23s.**
2715 + 3 + 2 + 1 = **2721**, matching `ecosystem/doc-counts.md` exactly. Both failures classified,
neither left unexplained:

1. `test_routine_consumers_live_backlog_governs_exactly_one_row` — **PRE-EXISTING.** Identical on
   bare `main` before any merge (§10 of this report). Live `BACKLOG.md` has 2 routine rows; the
   test pins 1. Its own docstring makes the repair a coordinated one: *"If this number moves, the
   ADR, the docstring and [#426] must move with it."* Out of scope here, and untouched.
2. `test_finding_headline_resolves_with_provenance` — **MERGE-CAUSED, and fixed.** Lane E's merge
   added 17 lines above `class Finding:` in `scripts/audit.py` (the by-path `gitenv` load), moving
   it from line **327 to 344**. Two live pins in `tests/test_reverse_dep_oracle.py` asserted 327.
   Repinned to 344 (`679ccbc0`); that module now passes 21/21. The pin count was **re-grepped, not
   recalled** — exactly two live sites, and no other `327` remains in the file.

**Confirmation run after the repin: `1 failed, 2716 passed, 3 skipped, 1 xfailed in 8m59s`** —
2716 + 3 + 1 + 1 = 2721 again, with only the pre-existing failure standing. The suite was re-run
in full rather than trusting the single-module pass, because the repin edited a test file and the
"full suite once on the merged result" item is about the tree as it will be pushed.

**Neither failure was teardown-clearable**, and the second known-pre-existing failure the first
attempt predicted — the linked-worktrees reader inversion — **never appeared**, before or after
teardown, confirming §10's finding that it inverts only when the suite runs from *inside* a lane
worktree.

**Suite runtime dropped from 31m43s to 8m23s** across the same repo, and the difference is the
teardown: the baseline ran with 13 linked worktrees registered, this one with none. That is a
÷3.8 change from worktree hygiene alone — worth knowing before budgeting a per-merge suite
cadence, and it materially softens divergence **D3**.
