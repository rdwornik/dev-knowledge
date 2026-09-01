# BATCH E — CLOSE PACKET

- **Class:** technical · **Date:** 2026-09-01 · **Batch:** E (HERMETIZATION) · **Arc:** `[#614]`
- **Closes:** `docs/audits/2026-08-31-technical-batch-e-manifest.md`, whose `closed_by:` names this
  exact path. Landing this file is what expires the ADR-110 declared-integration-arc exemption.
- **Author:** CC (Opus 5, fresh orchestrator seat, background) · **Consumed by:** `[#614]`

---

## 0 · The closure predicate, stated before any claim

The manifest's REFUSE-TO-FINISH clause is the contract, and it is deliberately hostile to a
narrative close: *"The batch does not close while any item is open... Removing this manifest's
`status: open` before that is closing the batch by assertion."*

So this packet is written as evidence per item, not as a report. **Where an item is NOT closed it
says so and stays open in this file** — two do.

**The manifest's `status: open` line is NOT edited.** It does not need to be: `batch_manifest`
resolves an open batch as *tracked AND `status: open` AND `closed_by:` ABSENT from the tree*. This
file's existence flips the third condition, so the exemption expires mechanically rather than by an
edit to an immutable audit. Verified after landing — see §6.

## 1 · Lane roster — final state, 15 of 15 resolved

```
lane   slug                                      state       witness
DC-1   lane-a-1-vision-to-readme                 MERGED      ea1e32a9
DC-3   lane-b-3-claude-md-genre                  SPLIT       see below -- the only non-simple case
DC-4   lane-c-3-root-contract                    MERGED      1a3c378b
DC-5   lane-d-4-ai-council-instantiation         MERGED      76f184fb
DM-1   lane-e-5-eval-sda1-harbor                 MERGED      1d814abc  (reviewed pre-merge)
DM-2   lane-f-6-observability-otel               MERGED      13fb1538  (reviewed pre-merge)
DM-3   lane-g-7-typed-multi-layer-graph          MERGED      7b0cbf14
DM-4   lane-h-8-local-memory-tier-l-evaluation   HARVESTED   docs/audits/2026-09-01-technical-dm4-local-memory-tier-l-evaluation.md
DM-5   lane-i-9-distiller-filing-amendment       MERGED      bea4c623
DM-6   lane-j-10-equilibrium-checkpoint          MERGED      b7fef9b9
HY-1   lane-k-11-derived-doc-freshness           MERGED      9b736ce2
HY-2   lane-l-12-logs-retention-rule             MERGED      1c92024f
HY-3   lane-m-13-templates-disposition           MERGED      4bc754b4
HY-4   lane-n-14-trends-burndown-and-quota-panel MERGED      720d3e09
HY-5   lane-o-15-wintooling-local-default        MERGED      32d19df   (in win-tooling)
```

**DC-3 is the one lane that did not merge as dispatched, and it is resolved rather than pending.**
Operator adjudication 2026-09-01: PARTIAL ACCEPT. Acts TWO and THREE were reconstructed act by act
on a fresh branch and merged (`ec5f5507`); Act ONE — the `protocols/ESSENTIALS.md` dissolution, the
floor-template edit, ~20 PLAYBOOK citation fixes and the "How Claude thinks" relocation — is
**deliberately not merged** and is preserved as `[#628]`'s input artifact, including its
guard-tracing research. Full hunk-by-hunk ledger:
`docs/audits/2026-09-01-technical-dc3-split.md`.

**That preservation is a DECLARED EXCEPTION to teardown, not an oversight.** The branch
`worktree-lane-b-3-claude-md-genre` is alive locally **and on origin** (pushed deliberately, so the
artifact does not depend on one disk), holding `6f226b34`. MERGE IS ATOMIC governs *merged*
branches; this one is unmerged by ruling and `git branch -d` would refuse it anyway. It dies when
`[#628]` consumes it.

**DM-4 owes no merge.** It ran on the `claude/` prefix, wrote no tree file, and is discharged by
its harvested artifact.

## 2 · Tier (A) and tier (C)

**Tier (A) — 7 of 7 executed, read-only, zero commits.** Dispatched 2026-08-31 16:44–16:50 CEST,
all `Ok=True` / `Bound=True`, all harvested (186,734 bytes). Session ids and receipts:
`docs/audits/2026-08-31-technical-batche-launch-contracts/PLAN.md` §1. They created no commits, so
no merge is owed; their teardown discharge is the manifest's own table, which names all seven —
which is what predicate 5's refusal text asks for.

**Tier (C) — executed, RED, and the RED is the finding.**
`docs/audits/2026-08-31-verification-codespace-admission-probe.md`: L1 Ok=TRUE (transport only),
**L2 RemoteExitCode=1**, **L3 HEAD comparison NOT MEASURED**, gate NOT RUN. The container's agent
returned *"Not logged in"* in 47 ms. **Z-G3's entry condition is NOT met and the router-ADR entry
condition is NOT recorded as met.** Committing lanes therefore stayed LOCAL for this batch, which
is what the manifest declares. This is the direct input to batch-F seed **F0**.

## 3 · REFUSE-TO-FINISH, item by item, with evidence

```
item                                         verdict   evidence
every lane merged or explicitly abandoned    CLOSED    section 1 -- 14 merged/harvested, DC-3 split by ruling
every worktree removed AND verified          PARTIAL   see below -- git-clean, one held directory
every branch deleted locally AND on origin   CLOSED*   *one declared exception, section 1
tier (A) harvested                           CLOSED    7/7, 186,734 B, PLAN.md section 1
DM-4 harvested                               CLOSED    2026-09-01-technical-dm4-...md
the close packet landed at closed_by:        CLOSED    this file
```

**The one PARTIAL, stated plainly rather than rounded up.** `git worktree list` shows the primary
checkout and nothing else, and `git worktree prune` is a no-op — so the worktree is gone as far as
git is concerned, and the "no leftovers" invariant is met at the level the gates can see. What
remains is an **empty directory** at `.claude/worktrees/lane-b-3-claude-md-genre` that `rmdir`
refuses with *"Device or resource busy"*. The cause was measured, not guessed: the **DC-3 lane's
Claude session is still running** (PIDs 8032 and 41560, `--worktree lane-b-3-claude-md-genre`) and
holds the directory. Its checkout has already been emptied under it, so it can do no further work.

**Ending another session is the operator's call, not this seat's**, so the directory is reported
rather than force-removed. It is empty, git-invisible, and disappears the moment that session
exits. **Remaining command, one line:**

```
rmdir "C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/lane-b-3-claude-md-genre"
```

## 4 · Asset balance

```
asset class     created   released   outstanding   note
hub worktrees   15        15         0             git-clean; one empty dir held, section 3
lane branches   15        14         1             worktree-lane-b-3-... PRESERVED by ruling
origin heads    -         -          3             main · automation/fleet-audit · the preserved lane
cloud sessions  8         8          0             7 tier-(A) + DM-4, all harvested, no commits
codespaces      1         0          2             OUT OF BALANCE -- see below
```

**The codespaces do not balance, and one of them is not this batch's.**

```
batche-c-admission-pgw54jqwv7qf65rj   Shutdown   2026-08-31T17:45  branch main
animated-dollop-rr65q4v6jgphxr4g      Shutdown   2026-08-31T22:41  branch probe/admission-roundtrip
```

The first is the tier-(C) admission probe the manifest names and tells the operator to *"delete
deliberately"*. The second appears in **no** batch-E artifact; its branch `probe/admission-roundtrip`
exists on no remote this repo tracks. Both are **Shutdown**, so neither is accruing compute
billing, and storage for a stopped codespace is the only ongoing cost.

**Neither is deleted here.** Deletion is destructive and outward-facing, the manifest reserves it
to the operator, and batch-F seed **F0** is an *attended* codespace proof-of-work that may want one
of these as its subject. **This is the batch's one genuinely open asset item.** Deferring the
decision is deliberate; leaving it unrecorded would not have been.

## 5 · Review coverage — what was reviewed, when, and by whom

**The window's own defect is carried forward rather than smoothed over.** Six lanes merged with no
independent review; the operator asked whether reviews ran unreported or were skipped, and the
answer was the process defect. `docs/audits/2026-09-01-verification-batche-post-merge-terra-round.md`
records that in its own words and runs the round post-merge — the weaker position, labelled as
such.

```
lane        when         tally                                       verdict
DM-1        PRE-merge    2 findings                                  1 corrected at integration
DM-2        PRE-merge    1 HIGH                                      fixed before merge
DC-5        POST-merge   crit=0 high=0 med=0 low=0                   CLEAN
DM-6        POST-merge   crit=0 high=0 med=1 low=0                   UPHELD -> row corrected
HY-2        POST-merge   crit=1 high=0 med=0 low=0                   UPHELD -> fixed
HY-3        POST-merge   crit=0 high=1 med=0 low=0                   REFUTED
HY-4        POST-merge   crit=0 high=0 med=1 low=0                   ACCEPTED as a limit
HY-5        POST-merge   crit=0 high=0 med=0 low=0                   CLEAN (win-tooling)
DC-3 split  PRE-merge    pass 1: 2 HIGH + 1 MED · pass 2: CLEAN      3 fixed, 1 premise refuted

post-merge round total   crit=1 high=1 med=2 low=0  |  2 fixed · 1 refuted · 1 recorded
DC-3 split loop tally    pass 2, the FINAL pass: 0 findings (not the loop total)
```

**Five lanes still have no independent review at all** — DC-1, DC-4, DM-3, DM-5, HY-1. The
post-merge round covered six; two were reviewed pre-merge; DC-3 got a full loop. That is 9 of 15
committing lanes. Said here because a coverage number nobody states reads as full coverage.

## 6 · v1.5.0 checklist — the three round-2 items, with witnesses

**v1.5.0 is NOT tagged by this packet.** The operator holds the tag. What this section does is
supply the witnesses so the GO is decided on measurement.

```
item              state         witness
README template   DISCHARGED    templates/README-md-template.md, 96 lines, TRACKED,
                                landed 2026-09-01 in eaaeafa2 -- "the one payload the
                                front-door migration was waiting on"
DC-3              RESOLVED      PARTIAL ACCEPT executed; Acts 2+3 merged (ec5f5507),
                                Act One preserved as [#628]'s input
[#276]            STILL BLOCKS  tasks/276-*.md carries `status: deferred`; it gates BOTH
                                consumer instantiations
```

**The manifest's own text on item 1 was FALSE when read today, and is corrected in this same
commit.** `deploy/manifest-v1.5.0.yaml` recorded, as its reason for not declaring the
`readme-front-door` component: *"The template does NOT EXIST; it remains the only canonical-doc
template the corpus lacks."* It exists, tracked, since `eaaeafa2` — authored hours after the
manifest's draft. The manifest is the **untagged, in-flight** one, so correcting a stale fact in it
is maintenance, not a version mint.

**What is corrected is the FACT, not the DECISION.** The component stays undeclared, because
declaring a deploy component is a release act and the remaining blocker is a different one: C7
asserts EXACT dict equality between a manifest's `doc_shapes` spines and the live
`audit._CANONICAL_SPINE`, and it lints v1.1.0 and v1.2.0 against those same live constants — so
adding `README.md` to either side alone REDs shipped specs. That coupling is unchanged and is the
operator's to sequence. `release_lint --version 1.5.0` measured today: **0 FAIL, 1 WARN** (the
pre-release tag WARN, expected until the operator tags).

**On `[#276]`, the classification is settled and only the mechanism is missing.** Neither ruff-gate
divergence is drift — both are declared, ai-council's ruled 2026-07-12
(`docs/audits/2026-09-01-technical-ruff-gate-divergence-classification.md`). The deploy tool simply
does not read the waivers. So the blocker is a feature gap with a known shape, not an unknown.

## 7 · What batch E carries out

```
[#628]  the DC-2 re-cut -- ESSENTIALS dissolution as a FLEET-COUPLED release act.
        Input artifact: branch worktree-lane-b-3-claude-md-genre @ 6f226b34.
[#629]  an amendment cannot SUBTRACT an act -- predicate 7 of the contract validator.
[#630]  manifest lane enum == contract slug at freeze.
[#621]  the hub's own VISION.md relocation, now unblocked at the gate layer and carrying
        an enumerated collateral write-scope (dc3-split section 4).
[#276]  deploy reads per-consumer waivers -- gates both consumer instantiations.
[#626]  the logs exemption that never thins.  [#627]  the agy route nothing authorizes.
[#8]    (win-tooling) five remaining canonical-doc drifts; the codemap half is discharged.
OPEN ASSET  two Shutdown codespaces awaiting a deliberate operator decision (section 4).
OPEN ITEM   one empty, git-invisible worktree directory held by a live session (section 3).
```

## 8 · Batch-E's own defects, kept where they can be read

Recorded so the next batch inherits the lesson rather than the incident:

1. **The freeze gate caught a naming defect the dispatch would have carried** (`LANE_BRANCH_RE`
   vs two-letter slugs). It worked. `[#630]` exists because the *next* comparison — manifest
   against contract — had no predicate at all.
2. **A contract amendment left a ruled-out act executable**, and the lane executed it correctly.
   `[#629]`.
3. **Six merges took no independent review**, and the round that fixed it ran post-merge.
4. **Four spine entries rode the ADR-110 exemption to the edge of the batch.** They were exempt,
   never failing — but the exemption is a deferral with a published expiry, and it dies with this
   file. They were anchored first, in JOURNAL 2026-09-01 (r), before this packet landed. Had they
   not been, this commit would have wedged every commit in the repo.

## 9 · The full suite — run once, at integration, and ATTRIBUTED

```
uv run --locked python -m pytest -q --tb=short
4772 passed · 12 failed · 3 skipped · 1 xfailed · 1043.81 s (17m23s) · exit 1
```

**A count of 12 REDs means nothing without attribution, so each was measured against a
BASELINE** — the same twelve node-ids re-run in a detached worktree at `b17fbc2c`, this session's
starting commit. Two needed help to be measurable at all: `test_desired_state_report` skipped for
a missing `pandas` until re-run with `--group analytics`, and `test_reverse_dep_oracle` skipped
for an unvendored pyright until `node_modules` was copied in. Skipping a baseline probe and
calling the result "pre-existing" would have been a guess wearing a measurement's clothes.

```
test                                                            baseline   now    verdict
consumer_at_landing::live_corpus_measures...                    FAIL       FAIL   pre-existing
desired_state_report::live_report_renders_the_real_fleet        FAIL       FAIL   pre-existing
funnel_coverage::committed_baseline_agrees_with_live            FAIL       FAIL   pre-existing
gen_north_star::the_committed_view_is_current                   FAIL       FAIL   pre-existing
export_backlog_view::no_gate_hook_or_script_reads_the_export    FAIL       FAIL   pre-existing
enforcement_coverage::anchor_gate_probe_distinguishes...        FAIL       FAIL   pre-existing ([#585])
preflight_freeze_predicates::vi_batch1_reproduces_wrong_id      FAIL       FAIL   pre-existing
cloud_provisioning::gate_never_syncs_the_environment            FAIL       FAIL   pre-existing
cloud_provisioning::provision_sh_runs_history_repair_first      FAIL       FAIL   pre-existing
validate_doc_rot::live_corpus_has_no_accretion_arm_findings     FAIL       FAIL   pre-existing (calendar-driven)
reverse_dep_oracle::finding_headline_resolves_with_provenance   PASS       FAIL   FALSE POSITIVE
gen_task_tree::live_view_is_under_the_589_done_when_byte_bar    PASS       FAIL   THIS SESSION'S
```

**Ten pre-existing. One false positive. One genuinely this session's, and it is not a bug.**

### The false positive, proven rather than asserted

`test_reverse_dep_oracle::test_finding_headline_resolves_with_provenance` failed in the full run
with `assert 3 >= 50`, passed at baseline, and **passes when re-run alone in this same working
tree**. The oracle is load-sensitive and the full suite ran alongside other work — the
measure-while-measuring artifact. Re-run evidence, not reasoning: `1 passed in 8.33s`.

### The one that is ours — and the finding underneath it

```
BACKLOG.md at session start (b17fbc2c)   69,982 B
the [#589] Done-when bar                 70,000 B      -> 18 bytes of headroom
after filing [#629] and [#630]           70,399 B
after trimming both row titles           70,276 B      -> still 276 B over
```

**The corpus had 18 bytes of headroom, so ANY new row breached the bar.** The two rows' view lines
cost 417 B; trimming their titles recovered 123 B, and even reducing both to stubs cannot recover
400. This is arithmetic, not effort.

**The bar was not raised, and the rows were not withheld.** Filing both was an explicit operator
instruction, and `[#589]` — *"One line per row ... with a size assertion that cannot be silently
undone"* — is an OPEN P1 row that owns this assertion. Raising its own bar to fit the first two
rows that hit it would be undoing it silently, which is the single thing the row exists to
prevent. So the RED stands, attributed, with its owner named. The genuine options are `[#589]`
raising the bar with a recorded justification, or a grooming pass — and grooming is **overdue
anyway**: `audit.py health` reports *"last groom 2026-07-30, 33d ago (> 21d cadence, ADR-41)"*.

### One pre-existing RED was halved, and its mechanism is now known

`consumer_at_landing` flagged two audits. One is fixed: `[#614]` cited the ruff-gate
classification as a bare path ending in `.md.` — and both citation regexes refuse a match followed
by `[A-Za-z0-9._-]`, so **the trailing sentence period made a real citation invisible**. Backticked;
it now resolves.

**The second cannot be fixed by citing it, and that is the finding.**
`LANE-w-1-wintooling-canonical-restamp.md` carries no `YYYY-MM-DD` prefix — the date lives on its
parent directory — so neither `_STEM_RE` nor `_AUDIT_NAME_RE` can ever produce its token. **No
citation anywhere can clear it.** Its batch-E siblings escape only because they are in the
arm-time baseline. That is a structural blind spot in `[#595]`'s organ for any dated-directory
contract file, and it is recorded here rather than worked around by amending an immutable artifact.

### Other gates, re-measured at this commit

```
audit.py health                           OK
deploy/release_lint.py --version 1.5.0    0 FAIL, 1 WARN (pre-release tag)
scripts/validate_backlog.py               OK (9 themes, 26 stories, 223 tasks, 2 pre-existing WARNs)
journal_anchor.unanchored_on_spine        [] -- empty BEFORE this packet expires the exemption
```

---

## AMENDMENT 1 — 2026-09-01, later the same day: the PARTIAL in §3 is now CLOSED

> **In-file amendment marker** (CLAUDE.md §5 rule 3). Everything above stands as written at the
> close; this records a state change measured afterwards, rather than editing the claim it
> supersedes.

§3 reported the worktree teardown as **PARTIAL**: git-clean, but an empty directory at
`.claude/worktrees/lane-b-3-claude-md-genre` that `rmdir` refused with *"Device or resource
busy"*, held by the DC-3 lane's still-live Claude session (PIDs 8032 / 41560). The packet said it
*"disappears the moment that session exits"* and named the one remaining command.

**It exited, and the command succeeded.** Re-measured at `0085941c`:

```
rmdir .claude/worktrees/lane-b-3-claude-md-genre   -> exit 0
test -d .claude/worktrees/lane-b-3-claude-md-genre -> GONE
ls -a .claude/worktrees/                           -> . ..   (empty)
git worktree list                                  -> primary checkout only
git branch --list "worktree-*"                     -> worktree-lane-b-3-claude-md-genre
                                                      (the DECLARED exception, §1 -- preserved)
```

**REFUSE-TO-FINISH, §3's table, revised line:**

```
every worktree removed AND verified          CLOSED   provision -> cleanup round-trip leaves
                                                      the tree identical (CLAUDE.md §5 rule 9)
```

**The batch's remaining open item is therefore ONE, not two** — the two Shutdown codespaces in §4,
which await a deliberate operator decision and are deliberately not deleted here. §7's
`OPEN ITEM` line is superseded by this amendment; its `OPEN ASSET` line stands.

**Why this is an amendment and not an edit.** The PARTIAL was true when written and the evidence
for it — a measured process holding a directory — is worth keeping. Overwriting it would erase the
record that a live lane session can outlive its own worktree and block a batch's teardown, which
is the transferable part.
