# Batch W2 — close packet

> Serial integration of five lanes into `main`, 2026-08-27. Integrator: CC (Opus 5, background
> job, primary checkout). Contract: `INTEGRATE-W2.md` plus the operator's superseding amendment
> of 2026-08-27. Batch JOURNAL entries: `2026-08-27 (a)`, `(b)`, `(c)`.

## The two headline numbers

```
audit.py health   BEFORE   210,135 ms   46 checks   (pre-W2A, W2A report §5, run f0caf15a)
                  AFTER    200,000 ms   48 checks   (merged main ee4885de, quiet host)
                  verdict  exit 0 · health: OK · ZERO FAILs · 114 WARNs

full suite        AFTER  2,484 s (41:20)  4102 passed · 9 failed · 4 skipped · 1 xfailed
                  (-n auto, the repo default; 4116 collected)
```

**Read the health pair honestly — it is better than 210 → 200 looks, and worse than "<60 s".**
`ALL_CHECKS` went **46 → 48** across this batch (lane-H added checks), so main does *more* work in
slightly less time. Inside that, W2A's own target check went **197,808 ms → ~7,000 ms (27.9x)** and
the bound moved to `check_review_artifact_coverage` (128.4 s), which W2A's contract explicitly
forbade chasing and which **[#597]** owns. W2A's stated `< 60 s` target was **NOT met**, and the
lane said so itself.

**A premise correction, stated rather than smoothed over.** The amendment named the before-number
as "the pre-W2A number on record, 625 s-class". **No 625 s figure exists on record.** The measured
pre-W2A baseline is **210,135 ms** (W2A report §5, telemetry run `f0caf15a`, 46 checks). That is
the number used above. Nothing in `docs/audits/` or `logs/` carries a 625 s health measurement.

## Per-lane landings

| # | Lane | Merge | Conflicts | Resolution | Gate result |
|---|---|---|---|---|---|
| 0 | anchor debt (`08b0d192`) | `dbd33400` | — | — | both pre-push organs **Passed** |
| 1 | `w2a-perf-core` | `066f6ecd` | none | — | 163 passed / 1 skipped / 1 xfailed |
| 2 | `w2b-surfaces` | `bf562619` | `docs/audits/README.md` | regenerated | 648 passed / 1 failed (foreign) · health **OK** |
| 3 | `w2c-codespace-repair` | `d5a2e7d9` | none | — | audit-health **Passed** |
| — | `every_push` revert | `b8ebbd6a` | — | — | attributed integration-time fix |
| — | integration-fix anchor | `df1ec97c` | — | — | audit-health **Passed** |
| 4 | `lane-g2-consume-recon` | `c287f11c` | `BACKLOG.md`, `tasks/manifest.json` | regenerated | 188 passed |
| 5 | `lane-h-handoff-mech` | `ee4885de` | `ecosystem/doc-counts.md` | regenerated | audit-health **Passed** |

Every conflict was a **generated** file and every one was resolved by **regeneration**. No
hunk-picking anywhere. Verified after each: `gen_audit_index --check` exit 0, `gen_task_tree
--check` "check ok", `gen_doc_counts --check` exit 0 (`precommit_hook_count` 21/21,
`pytest_collected` 4116/4116), and all eight G2 births `#599`..`#606` present in both `tasks/` and
the regenerated `BACKLOG.md`.

**No `SKIP=audit-health` was used at any point in this batch** — see §"The exemption that did not fit".

## [#590] first live proof — it holds, on two lanes, and the nominated lane could not supply it

The claim is that the audits index stops being merge-resolvable. Measured across this queue:

| Merge | `docs/audits/README.md` | Reading |
|---|---|---|
| W2B `bf562619` | **CONFLICTED** | expected — W2B *is* the fix, the last merge predating it |
| W2C `d5a2e7d9` | **no signal** | touches only `.devcontainer/`; structurally cannot prove anything |
| G2 `c287f11c` | **auto-merged clean** | while the same merge conflicted on 2 other files |
| lane-H `ee4885de` | **auto-merged clean** | while the same merge conflicted on `doc-counts.md` |

**Verdict: [#590] HOLDS**, confirmed independently on G2 and lane-H — the same merges that collided
elsewhere no longer collided on the index. Two caveats, both stated because they qualify the proof:

1. **The batch contract nominated W2C as the proof, and W2C cannot be one.** It never touches the
   file. Counting "did not conflict" as a pass there would have been a measurement error.
2. **Merge-free is not regeneration-free, and this bit.** After both clean auto-merges the index was
   still **STALE** (`gen_audit_index --check` exit 1) — a clean textual merge is not a correct
   regeneration. `[#590]` removed the *collision*, not the *obligation to regenerate*. Two suite
   failures (`test_live_index_is_fresh`, `test_live_index_excludes_nothing_because_every_audit_is_tracked`)
   were exactly this, and are fixed in the same commit as this packet.

## Full-suite failure attribution — 9 of 9, none requiring lane content to be sent back

| Test | Verdict | Evidence |
|---|---|---|
| `test_gen_audit_index` ×2 | **INTEGRATOR'S** | index stale post-merge; regenerated in this commit |
| `test_validate_doc_rot::...accretion...` | foreign | `[#457]` body names it: "the two OWNED suite REDs are `routine_consumers` + the doc_rot accretion arm"; row `#348` accretion present pre-W2B |
| `test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export` | foreign | reproduces in isolation; W2B pre-declared it (`ecosystem/conformance.{md,html}` reference `export_backlog_view`) |
| `test_enforcement_coverage::test_anchor_gate_probe_...` | foreign | neither `block_unanchored_push.py` nor the test touched by this batch (last touched 2026-08-19 / 2026-08-11); **and its claim is refuted live** — the organ returned exit 0 on an anchored range and Passed a real dry-run push |
| `test_desired_state_report::test_live_report_renders_the_real_fleet` | batch consequence | G2's registry admission adds `win-tooling`; the known "registry admission REDs live-repo pins" class |
| `test_funnel_coverage::test_committed_baseline_agrees_with_a_live_measurement` | batch consequence | the batch added audit artifacts; dispositions are an architect act |
| `test_reverse_dep_oracle::test_finding_headline_...` | **environmental** | `assert 3 >= 50` under `-n auto`; **PASSES in isolation** (exit 0, 6.74 s) — Pyright truncated under parallel contention |
| `test_toc::test_corpus_fence_fix_...` | **environmental** | `FileNotFoundError` on a path inside the LIVE `lane-na-gates` worktree; **PASSES in isolation** |

**Two structural findings from that table**, both worth more than the individual REDs:
- **The full suite is not isolated from live sibling worktrees.** `test_toc`'s corpus walk descends
  into `.claude/worktrees/*`, so a concurrent lane mutating its own tree produces a false RED in the
  integrator's suite. Any batch that runs a full suite while sibling lanes are live inherits this.
- **`-n auto` can fabricate a RED that isolation clears** (the Pyright oracle). Both were settled by
  re-running in isolation rather than by argument.

## The exemption that did not fit — why the anchor entry was written at queue-open

`check_journal_spine_anchor` FAILs per-commit on an unanchored lane merge, and a conflicted merge
runs the pre-commit `audit-health` gate. ADR-110's declared-integration-arc exemption exists
precisely for this, and `batch_manifest.py` says it replaces `SKIP=audit-health`, "which disables
EVERY check in the registry, not the one that cannot pass".

**It grants nothing here.** The `[#514]`/`[#510]` W1 narrowing scoped it to the ratified lane grammar
`LANE_BRANCH_RE = ^worktree-lane-[a-z]-\d+-<slug>$`. All five branches were tested against the
imported regex and **none matches** — the first three carry no `lane-` segment, and `g2`/`h` are not
`<letter>-<digits>`. A manifest committed for W2 would have granted **ZERO** exemptions.

So the contract's sanctioned alternative was taken: the batch anchor entry was written at
queue-open naming lane **TIPS** (what §A7 actually requires), which kept `audit-health` armed on
every conflicted merge. **Cost: zero SKIPs across a five-lane batch.** This is
`validate_branch_naming`'s own honest limit landing in practice — the grammar is enforced nowhere
at provisioning, so off-enum lane names are creatable and simply get no exemption later.

## Smoke 6 — FAILED, and it failed twice over

Contract: `SMOKE6-audit-check-count.md` (read-only, two commands, one line out). Dispatch:
`Start-DispatchCodespace -Contract ... -Slug smoke6-w2-checkcount`, `basicLinux32gb`, idle 30m,
retention 24h, branch `main`. Codespace `smoke6-w2-checkcount-x9pg75qxrwvfp5w5`.

```
REQUIRED   Ok=True             ACTUAL  Ok=False        FAIL
REQUIRED   RemoteExitCode=0    ACTUAL  (never ran)     FAIL
REQUIRED   receipt HEAD == pushed HEAD                 FAIL (independently — see below)
wall       90 s to failure (create 8 s)
```

**Failure 1 — the cp literal-quote transport bug, as the amendment anticipated.** Step 3 died:

```
scp.exe: dest open "'/workspaces/dev-knowledge/SMOKE6-audit-check-count.md'": No such file or directory
```

The destination reached scp wrapped in **literal single quotes**. Ruled out by direct probe rather
than inferred: `/workspaces/dev-knowledge` **exists and is writable** (`touch` succeeded,
`-rw-rw-rw-`), so this is neither a missing directory nor permissions. **Per the amendment this is
the win-tooling half and the hub was NOT patched around it.** Owner: win-tooling.

**Failure 2, independent and more interesting — the container was serving a STALE image.** Measured
inside it before shutdown:

```
git rev-parse HEAD          6882ef74…      (pushed HEAD was ee4885de)
grep -c refresh_source_tree .devcontainer/provision.sh   ->  0     (W2C's fix ABSENT)
command -v uv                                            ->  absent (W2C's other fix ABSENT)
/workspaces contents dated 2026-08-26
```

So even had the copy succeeded, `receipt HEAD == pushed HEAD` would have failed. The codespace came
from an image predating W2C's merge, so **neither W2C repair was present to be tested**. This is
exactly the honest limit W2C declared about itself: the trigger line "only DECLARES", prebuild
configuration is server-side operator UI state with no public API, and landing it "needs an operator
edit at Settings -> Codespaces -> Set up prebuild".

**The `every_push` revert is not implicated in this staleness**, and the packet says so plainly so
nobody infers otherwise: the image was already stale from 2026-08-26, and the trigger — whatever its
declared value — is not configurable from the repo and was never set in the UI. `[#593]`'s
*enforceable* half (`refresh_source_tree`) is untouched by the revert and simply was not in this
image. **W2C's repairs remain UNPROVEN on live substrate**, and that is a real gap, not a formality.

**Codespace state: STOPPED** (compute billing ended), **not deleted** — the module treats deletion as
a deliberate operator act; retention auto-deletes at 24h. Delete sooner with
`gh codespace delete -c smoke6-w2-checkcount-x9pg75qxrwvfp5w5`.

## Named debt, with owners

| # | Debt | Owner | Evidence |
|---|---|---|---|
| D1 | **Smoke 6 cp literal-quote transport bug** — `gh codespace cp` destination reaches scp single-quoted | **win-tooling** | §Smoke 6 failure 1; dir proven writable |
| D2 | **W2C's repairs unproven on live substrate** — prebuild served a 2026-08-26 image without `refresh_source_tree` or `uv`; prebuild trigger is server-side UI state | **operator** (UI edit) + `[#593]` | §Smoke 6 failure 2 |
| D3 | **Lane grammar vs dispatched lane names** — all 5 branches off-enum, so ADR-110's exemption is dead for real batches. Widen the grammar, or make dispatch conform | **architect** | §The exemption that did not fit; `[#510]` open on this leg |
| D4 | **Full suite is not isolated from live sibling worktrees** — `test_toc` false RED from `lane-na-gates` | **architect / [#597] tiering** | §attribution table |
| D5 | **`-n auto` fabricates a Pyright RED** — `reverse_dep_oracle` passes in isolation | unowned — needs an intake | §attribution table |
| D6 | **doc_rot accretion arm + `routine_consumers`** — the two long-standing OWNED suite REDs | `[#457]` | `[#457]` body, 2026-08-18 |
| D7 | **`export_backlog_view` read by governance** (`ecosystem/conformance.{md,html}`) | pre-existing, W2B-declared | reproduces in isolation |
| D8 | **`funnel_coverage` baseline vs live** — this batch added artifacts (incl. this packet) needing dispositions | **architect** | 114 health WARNs |
| D9 | **`test_desired_state_report` fleet pin** — G2's registry admission adds `win-tooling` | G2 / `[#457]`-adjacent | known "registry admission REDs live-repo pins" class |
| D10 | **W2C's lane report is unlocatable** — only `CONTRACT-W2C.md` exists; the branch carried no report, so its "two-command unblock" could not be reconciled against intent | **operator** | §Deviations |
| D11 | **W2A's `< 60 s` health target missed** — bound is now `check_review_artifact_coverage` (128.4 s) | `[#597]` | W2A report §5 |

## Deviations from the contract, each stated rather than absorbed

1. **Two pushes, not one.** Smoke 6 requires `receipt HEAD == pushed HEAD`, so `main` had to be
   pushed before the smoke; this packet lands after. Push 1: `d8211b03..ee4885de`.
2. **W2C's two-command unblock could not be executed as written.** Command 1,
   `git merge --ff-only main` inside its worktree, returned `fatal: Not possible to fast-forward,
   aborting.` — W2C carried 2 commits on base `852e145c` and is structurally not fast-forwardable.
   Its report is unlocatable (D10), so intent could not be recovered. Command 2 (push its branch)
   succeeded and was the substantive half: W2C was the only unpushed lane. Run literally, failure
   reported, nothing substituted.
3. **The batch anchor entry was written at queue-open**, per the contract's own "write early if the
   anchor gate demands it" clause — forced by D3.
4. **Three JOURNAL entries, not one.** `(a)` discharges the foreign anchor debt (a precondition, not
   batch content); `(b)` is the single batch entry naming all merged tips; `(c)` anchors the
   integration-time fix, whose branch did not exist when `(b)` was written.

## Teardown

Five merged worktrees removed, `git worktree prune` run, nine merged branches deleted with `-d`
(safe), three merged remote lane branches deleted per MERGE IS ATOMIC. **Ancestor-proved before any
deletion**; every merged worktree verified clean (0 uncommitted) first.

**Left standing, deliberately:** `lane-na-gates` and `lane-nb-tiering` — LIVE mid-work, never merged,
never read, worktrees untouched. Both advanced during this batch (`08b0d192 -> cbceffdd`,
`6a4740ab -> fb387710`), which is the evidence they were live. Their remote branches are untouched.
`worktree-prompts-revocation` plus the merged `chore/workspace-provider-roots-2026-08-26` and
`docs/anchor-prompts-revocation` are **prior-session leftovers, not this batch's** — left alone
rather than swept, since deleting another session's branches was not this batch's call.

## Still open at close

- **`na`/`nb` follow-up mini-merge** after those lanes STOP — the only remaining merge work.
- **Smoke 6 re-run** once D1 (win-tooling) and D2 (prebuild refresh) are addressed; W2C stays
  unproven until then.
- Dispositions for this batch's audit artifacts, this packet included (D8).
