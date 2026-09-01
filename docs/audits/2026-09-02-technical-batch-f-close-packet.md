# BATCH F — CLOSE PACKET

- **Class:** technical · **Date:** 2026-09-01 (filed at the 09-02 identifier the exemption keys on)
- **Arc:** `[#614]` · **closed_by:** this file · **Author:** CC (Opus 5, integrator seat)
- **Manifest:** `docs/audits/2026-09-01-technical-batch-f-manifest.md` (frozen + 4 amendments + the phase-boundary note)

> **Flat by design** (`CLAUDE.md` §4 output-formatting) — no pipe tables, so this copies into
> browser chat without the TUI painting border glyphs.
>
> **This packet CLOSES the batch, and closing it KILLS the ADR-110 exemption.** Every lane merge
> was therefore anchored BEFORE this file landed, in JOURNAL `(aj)` and `(ak)` — not after.

## 0 · THE ONE-LINE RESULT

**Eight lanes merged. Zero rows closed. That is not a failure — it is the batch working.**

Terra pre-merge (amendment 2) ran on every lane including the ones that changed no code, and
returned **14 real defects (HIGH) and 5 recorded tensions against 1 clean pass.** In five cases
the defect defeats the row's own stated purpose, so the row is **MERGED BUT NOT CLOSED**. Closing
them on "tests pass, merged" is precisely the substitution ADR-81 forbids.

## 1 · WHAT LANDED

```
L2  lane-b-2-handoff-v7          [#611]  31640426  v7 BOOT-INVERSION: /boot-session,
                                                   boot_frontier.py, FUNNEL HEALTH, sec17
L3  lane-c-3-logs-retention      [#626]  6241e5a8  three hub callers re-pointed, order honored
L4  lane-d-4-deploy-waiver       [#276]  c092bc4c  _classify_prune consults a consumer waiver
L5  lane-e-5-vision-relocation   [#621]  441b08d8  VISION.md -> docs/archive/, byte-identical
L6  lane-f-6-agy-admission       [#627]  d8bc4a2b  SDA-1 against agy live; VERDICT REFUSE
L7  lane-g-7-contract-validator  [#629]  ad41ced2  lane-slug agreement predicate
                                [#630]
--  worktree-lane-632-proof      [#632]  5f42d86e  codespace long-run proof, six layers
--  dashboard-home-ruling        [#614]  3a4066eb  DASHBOARD HOME -> docs/dashboard/
--  boot-r1-survey               [#611]  3fe5db59  prioritization/scheduling survey
--  feat/v7-version-bump         [#611]  d2fd7537  v6.3.0 -> v7.0.0, ONE coupled release act
```

**L1 was never dispatched** as a codespace proof-of-work lane; the operator's later ruling
replaced it with the `[#632]` proof lane above, which DID run and DID report.

## 2 · TERRA TALLY — refutations as prominent as acceptances (amendment 2)

```
lane                     real defects (a)   tensions (b)   verdict
dashboard-home-ruling            0               0         CLEAN PASS
boot-r1-survey                   2               1         NOT CLEAN
lane-b-2  [#611]                 1               1         NOT CLEAN  (+2 explicit no-findings)
lane-c-3  [#626]                 3               0         NOT CLEAN
lane-d-4  [#276]                 1               0         NOT CLEAN
lane-e-5  [#621]                 2               1         NOT CLEAN
lane-f-6  [#627]                 3               0         NOT CLEAN
lane-g-7  [#629][#630]           2               0         NOT CLEAN
632 proof [#632]                 2               1         NOT CLEAN  (1 discharged, below)
TOTAL                           16               4         1 clean of 9
```

**ONE PATTERN ACCOUNTS FOR MOST OF IT: the lane fixed the ROOT copy and missed the copy that
actually EXECUTES.** `[#626]` re-pointed the three hub call sites and left the DEPLOYED plugin
copies (`propose_closures.py:323`, `review_closures.py:232`) and `fleet_health.py:576` globbing
flat — and the Stop hook runs the plugin copy. `[#621]` moved VISION losslessly and left
`canonical_docs.py:160` and `conformance-hub.js:133` pointing at the vanished root file, where
the freshness gate SILENTLY SKIPS an absent file and reports green while checking nothing.

**WHAT TERRA CONFIRMED, recorded as prominently as what it refused:**
- `[#611]` did NOT bump the registered spec (still 6.3.0 at merge) and `boot_frontier.py:175`
  DELEGATES to `gen_task_tree.rank_key` rather than inventing a scoring model — exactly the seam
  BOOT-R1 pinned. Both were the disciplines most at risk in that lane.
- `[#626]` honored its own caller-first sequencing (`07e3adcb` before `e358d613`).
- `[#621]`'s relocation is byte-identical — both blobs hash `61bd603e8b2b5b022cebb19eac393fe947792419`.
- `[#276]`'s missing-file and YAML-parse-error paths BOTH fail closed.
- `[#630]`'s set-difference compares BOTH directions, so an extra contract is not missed.

**ONE FINDING DISCHARGED BY THE INTEGRATOR, on evidence terra could not see.** Terra called
`[#632]`'s L6 GREEN unevidenced because the artifact promises push output it does not contain.
Correct about the artifact, wrong about the world: the branch was fetched FROM origin into the
primary checkout at `dd471c31`, which is direct proof the push landed. The artifact's failure to
carry its own evidence stands as the defect.

## 3 · ROWS MERGED BUT NOT CLOSED — with the reason each stays open

```
[#626]  the hub callers are right; the DEPLOYED plugin copies and fleet_health's gauge are not.
        The Stop hook and /review-closures both run the plugin copy, so the closure loop still
        breaks the moment retention relocates a PROPOSALS-* file.
[#630]  the predicate is NEVER INVOKED (the lane-contract-check hook entry is unchanged) and
        passes VACUOUSLY on empty sets. The batch-E slug defect it exists to catch would still
        reach integration. A gate that is never called is not a guarantee.
[#629]  rides with [#630] -- same lane, same unwired surface.
[#276]  the waiver FAILS OPEN on missing/invalid/expired dates, so a stale declaration can
        suppress a refusal the hash-guard should have made.
[#621]  the move is clean and provably lossless; two machine-read surfaces still name the
        vanished root file, one of them a gate that silently skips rather than failing.
[#627]  MERGED, VERDICT NOT RATIFIED. The REFUSE may be directionally right, but its evidence
        is not reproducible (placeholder paths, no raw artifacts), it names no re-open
        condition, and its gate arithmetic contradicts its own rubric (nine gates, reported as
        "five of eight"). A REFUSE on thin evidence is as much a defect as an ADMIT on thin one.
[#632]  the proof REPORTED, which is what the precondition asked. The substrate verdict is RED
        at L5, so the row stays open on its own sequence (the 13, then the probe, then the
        hardening).
[#611]  v7.0.0 IS cut and every dependent reconciled -- but the Done-when also requires an
        assembled paste from a REAL cut measuring <=20 KB at >=70% window-specific content.
        That measurement belongs to the v7 bundle this session generates, so the row closes on
        the operator's verdict of that bundle, not on the version bump.
```

## 4 · EFFICIENCY PANEL — nine concurrent worktrees against the 6/12 ruling

```
PER-LANE WALL-CLOCK, dispatch -> STOP (measured from transcript timestamps)
  lane-b-2  handoff-v7                 115.6 min   635 assistant turns
  lane-c-3  logs-retention              16.5 min   113
  lane-d-4  deploy-waiver               41.7 min   189
  lane-e-5  vision-relocation           88.4 min   401
  lane-f-6  agy-admission              127.7 min   241
  lane-g-7  contract-validator         110.3 min   265
  SUM of lane work                     500.1 min  (8.34 h)
  WALL-CLOCK ELAPSED  15:51 -> 17:59   ~128 min
  EFFECTIVE SPEEDUP                    ~3.9x at 6 concurrent lanes (9 worktrees live)
```

**The 6/12 ruling held, and the ceiling is REAL — it was hit, at the integrator, not at the
lanes.** Concurrency did not degrade the lanes; it degraded the SEAT. Three concurrent `codex
exec` terra reviews on top of nine worktrees produced two hard failures the seat had to work
around: `memory allocation of 1071307 bytes failed` (terra OOM, twice, on lane-c and lane-b) and
`cygheap read copy failed / fork: Resource temporarily unavailable` killing a `git push`
mid-flight. Both cleared when reviews were serialized. **The measured lesson: the optimum-6
ruling governs LANES; the integrator's own fan-out is a separate budget nobody had costed, and
at 3 concurrent terra passes this workstation is over it.**

```
COST OBSERVED
  codespace attempt 3 (prior seat)   ~75 min billed, 3 s CPU, ZERO productive work
  codespace proof (this seat)        1156 s run, remote exit 0, 2 commits, pushed -- PRODUCTIVE
  codespaces leaked                  0 -- every one created was deleted; `gh codespace list` empty
  credits per lane per model         NOT DERIVABLE. All lanes ran sonnet/high; nothing records
                                     per-lane spend, and [#615] is the row that would make it
                                     derivable. Reported ABSENT rather than proxied, per DB-1's
                                     own standard.
```

## 5 · v1.5.0 CHECKLIST — with witnesses

```
README template            DISCHARGED   templates/README-md-template.md, 4,007 B, tracked,
                                        landed eaaeafa2 (2026-09-01). Pre-existing to batch F.
DC-3                       RESOLVED     docs/audits/2026-09-01-technical-dc3-split.md;
                                        CLAUDE.md v2.71 + v2.72 record the landed acts.
[#276]                     OPEN         un-deferred and BUILT this batch (c092bc4c) -- but see
                                        section 3: the waiver fails open, so the row that
                                        blocked two consumer instantiations is not closed.
[#628] ESSENTIALS          OWED         deliberately deferred to G, after the v1.5.0 tag: a
                                        floor edit is a release act (release_lint C5's
                                        three-way hash equality). TWO live drift sites were
                                        FILED this batch rather than absorbed --
                                        SESSION_SETUP.md Step 2 (x3) and Step 4, and
                                        DEFINITION_OF_DONE.md's closing "See also".
deploy manifest v1.5.0     AMENDED      two v7 organs declared by L2; the integrator fixed a
                                        --propose flag the CLI never had (verified at
                                        boot_frontier.py:302-303, not taken on report).
carried codespace assets   CLEAN        the two Shutdown codespaces the manifest ordered
                                        deleted are gone; `gh codespace list` returns empty.
```

**NOT A WITNESS, AND SAID SO: the v1.5.0 TAG itself is the operator's act and has not happened.**
This packet does not tag, and nothing here should be read as tagging.

## 6 · WHAT THE INTEGRATOR FOUND THAT NO LANE REPORTED

```
1. THE SPINE WAS WEDGED, AND IT WAS BLOCKING THE LANES, NOT THE PACKET.
   Two unanchored --no-ff merges (3a4066eb, 3fe5db59) FAILed journal_spine_anchor, which is
   pre-commit and repo-wide. L5 sat with 13 files ready and 0 commits, polling. It was not
   stalled -- it was correctly refusing a broken gate. L6 sat at zero output for the same
   reason and was nearly torn down as an empty lane.
   The ADR-110 exemption did NOT cover either merge: it requires a `worktree-lane-*` branch,
   and neither `worktree-dashboard-home-ruling-filing` nor `worktree-boot-r1-survey` matches.
2. THE STOP SENTINEL'S HEURISTIC IS WRONG FOR A GATE-BLOCKED LANE.
   Transcript-bytes-plus-clean-worktree reported L6 as "ahead=0 dirty=0" -- apparently no
   output. L6 then committed TWICE after the gate cleared. An idle lane waiting on a gate is
   byte-quiet and clean, i.e. indistinguishable from a finished one. The ancestor proof before
   teardown is the only reason its work survived.
3. THE ENUMERATED LIST OF SIX v7 DEPENDENTS WAS INCOMPLETE.
   The gates named three more: CONTRIBUTING.md's BODY stamp (a second site in a file whose
   frontmatter was already done), /handoff's description anchor, and docs/handoffs/README.md's
   own reconciled_with. [#611]'s Done-when already mandates grep-and-classify and says "never a
   trusted enumerated list" -- this is the measurement that proves the mandate right.
4. CONTRIBUTING.md WAS DESCRIBING A TREE THAT NO LONGER EXISTS.
   Found by the A2 re-read the v7 bump forced: it claimed AGENTS.md "does not exist here yet"
   and that validate_hermetization.py "still refuses the add". AGENTS.md has been at the root
   since 2026-08-29 and the script now sanctions it. Corrected in place.
5. A FALSE "gh not authenticated" REFUSAL WAS KILLING CODESPACE DISPATCH.
   Start-DispatchCodespace's guard runs `& gh` with StandardOutputEncoding set; under a
   REDIRECTED stdout that throws, $LASTEXITCODE is never set, and the guard reports "not
   authenticated" while gh is fully authenticated. Fix: dispatch under `pwsh -NoProfile`.
   Then two cp/scp failures were mapped: -IdentityFile with a Windows path (scp reads `C:` as
   host:path) and `-- -O` with no identity (scp treats -O as a filename). Fix:
   -LegacyScpProtocol $false. THREE transport layers named and fixed.
6. win-tooling CARRIES ~256 LINES OF UNCOMMITTED [#632] RUNNER HARDENING.
   IdleTimeoutSeconds (an inference fuse measuring EVENT ARRIVAL, not elapsed time), --detach,
   stream-json logging -- written by a prior seat, never committed. The proof lane above ran
   WITH it, so that result's reproducibility currently depends on uncommitted local state in
   another repo. NOT TOUCHED by this seat. It needs an operator decision.
```

## 7 · FIVE-PILLAR CLOSE

```
P1 RECORD        JOURNAL (ai) (aj) (ak); this packet; the terra tally artifact
                 (2026-09-01-verification-batchf-terra-tallies.md). Spine clean and ANCHORED
                 AHEAD of this file, so closing it cannot manufacture a gap.
P2 GATES         audit.py health: ZERO [!!] at the v7 bump. Both pre-push gates Passed on
                 every push. FOUR disclosed SKIP=audit-health bypasses inside lane-b, all the
                 same lane-lag false positive, whose root cause is now fixed on main.
P3 REVIEW        terra on all NINE merged branches (amendment 2 satisfied, including the lane
                 that changed no code). 16 real defects, 4 tensions, 1 clean pass, 1 finding
                 discharged with counter-evidence. Every tally is in the merge commit body of
                 the lane it belongs to -- not summarised away.
P4 CLEANUP       worktree list == primary + land-article-substrate-brief (another seat's live
                 tree, LEAVE per the manifest). All eight batch worktrees removed, all eight
                 branches deleted locally, the two merged non-lane branches deleted on ORIGIN
                 (B1: both places). Zero codespaces leaked.
                 HONEST EXCEPTION: two directories (lane-f-6, lane-g-7) survive on disk under
                 .claude/worktrees/ -- "Device or resource busy", a process still holds them.
                 git no longer tracks either; they are inert directories, not worktrees. This
                 is a real "no leftovers" miss and is stated rather than hidden.
P5 NEXT          the v7 bundle this session generates, and the batch-G seed below.
```

## 8 · BATCH G — SEEDED BY THE OPERATOR THIS WINDOW

```
G-SEED-1  /boot-session gains TWO GENERATED sections (operator, this window; reconcile with
          intake #66 and [#611]):
          (1) HISTORY DELTA -- this bundle's numbers against the PREVIOUS bundle's, with a
              direction per metric. docs/handoffs/ is an immutable time series; read it.
          (2) EQUILIBRIUM MAP -- per dimension (execution, funnel, contracts, routing, review,
              eval, observability, graph, memory/distiller, planning, doctrine), WHO DRIVES:
              REPO mechanism / BROWSER judgment / OPERATOR decision. Derived from the organ
              inventory plus the decision tree.
          Metric set: operator process questions (target 0), budget-decided vs escalated,
          architect rulings per batch, OPERATOR ASKS re-asked, validator-caught vs human-caught
          premise errors, review coverage, orphans/rot, off-laptop lane share, credits per lane
          per model. The seat reads the map to know where it is still needed; the DIRECTION is
          the equilibrium's own health check.
CARRIED   F5 ARCHITECTURE slice 2 · [#628] ESSENTIALS dissolution (after the v1.5.0 tag) ·
          F2 the distiller build, RE-DECIDED AS TIER L (ADR-112's guard: "Tier S never touches
          gates"), so G owns the design lane that writes its build contract.
NEW       the five merged-but-not-closed rows in section 3 are G's most concrete inventory:
          every one has a named defect and a named fix direction, which is a better batch input
          than a fresh survey.
```

## 9 · HONEST LIMITS OF THIS PACKET

- **Terra is one reviewer at `medium` reasoning effort.** Nine passes at ~1 pass each; the
  manifest priced 1–2. A second pass was not run, so "16 real defects" is a floor, not a census.
- **No full-suite run at integration.** `[#528]` says the full suite runs once, at integration.
  It was NOT run here: the `[#632]` proof lane ran it IN THE CODESPACE (17 failed / 4759 passed
  / 298 s) and terra then removed the argument that those failures are container-independent.
  So the suite's state is MEASURED but its attribution is OPEN. Targeted tests were run per lane.
- **Credits per lane per model are ABSENT, not estimated.** `[#615]` is the row that fixes it.
- **The L2 auth mechanism in `[#632]` is inference**, not proof — the nested-CLI failure it
  warns about IS proven; the channel behind it is not.

---

## AMENDMENT 3 — the codespace section, closed by `[#632]`'s win-tooling lane (2026-09-01)

> Appended as an in-file amendment marker, not an in-place edit (CLAUDE.md §5 rule 3). §4's
> efficiency panel already recorded ONE productive codespace proof from the prior seat
> (1156 s, exit 0, 2 commits). This amendment supersedes that as the codespace section's
> verdict, because the arc that followed it found the transport had been broken all along and
> then proved the substrate at **n=2** under a hardened runner.

### The n=2 verdict — VERBATIM

Two lanes, two independently provisioned codespaces, both end-to-end, both committing and
pushing from inside the container, both returning a receipt to the workstation.

| | Lane A (M, sonnet, attached) | Lane B (S, `-Detach`) |
|---|---|---|
| Codespace | `lane-632-longrun-a-w95qprj5wq4cg67g` | `lane-632-admission-b-7r5j6v45qrr3wwqp` |
| Provision | 6 s | 7 s |
| Run | **863 s, remote exit 0** | dispatch **returned in 62 s**; work done by +3 m 53 s |
| Receipt | in hand, `is_error:false`, `status:DONE` | harvested after the fact, same |
| Turns / events | 76 / 338 | 28 / 99 |
| Commits pushed from container | **2** (`4133cd19`, `7b3ba003`) | **1** (`7fbd54e7`) |

**The hang is measured out, not hoped away.** The full hub suite ran in-container to completion
in `294.07 s` real against `8 m 23 s` user and `42 s` sys — CPU proportional to wall-clock at
every scale tried, the exact inverse of the recorded **75-min-elapsed / 3-second-CPU** hang
signature. Nothing hung at any point in either lane.

**L5 is RED on CONTENT, not on the substrate:** the suite exits non-zero because sixteen hub
tests fail on their own merits. That is a hub repo-state row and it is named here rather than
absorbed into the substrate verdict.

**Teardown:** every codespace this arc created is deleted; `gh codespace list` empty. Free pool:
0.1166 h of 2-core compute, **net $0.00**.

### The four live-only defects — VERBATIM

The brief named two defects in one cluster. **Running the thing found four more**, and the first
had been silently breaking every real codespace dispatch since the transport was written. None
was reachable by reading the code or by any offline test: the seam that records argv is not gh,
and the container's own PATH is not visible from the workstation.

**1 · The `--` block was appended AFTER the operands.** gh's usage is
`cp [-e] [-r] [-- [<scp flags>...]] <sources>... <dest>` — every flag comes BEFORE the operands.
After `--`, Cobra stops parsing flags, so a trailing `-- -O -i KEY` was never a passthrough at
all: `-O`, `-i` and the key PATH became three extra FILE OPERANDS, and scp read the key path as
its destination. Measured live, one 14-byte file per arm, each verified with `ls` **and** `cat`:

```
cp --expand SRC remote:DST -c NAME -- -O -i KEY   FAILED   "...codespaces.auto: Not a directory"
cp -c NAME --expand -- -O -i KEY SRC remote:DST   LANDED   14 bytes, content correct
cp -c NAME --expand SRC remote:DST                LANDED   14 bytes, content correct
```

Every prior live run died at the SSH key before cp moved a byte, which is why this survived.

**2 · The dry run understated the live command.** It printed `bash <runner>` where the live path
sends `bash -l <runner>` — the login shell being the exact token that had already cost a
dispatch. A dry run that understates the live command is worse than none: it is consulted
precisely when someone is confirming the live command is right.

**3 · The admission gate refused on `gh`.** The first successful end-to-end run returned a
receipt in 6 s saying `"gh is not authenticated in this container"`. The gate worked; the gate
was wrong. That devcontainer has **no `gh` at all** (`bash: gh: command not found`) and does not
need one — `GITHUB_TOKEN` is set and `git ls-remote origin HEAD` answers, which is every remote
thing a committing lane does. Gating on gh refuses a container that is fit to run the work.
`gh` became a reported field; `timeout 30 git ls-remote origin HEAD` became the gated one.

**4 · The gate accepted `GITHUB_TOKEN` as an ANTHROPIC credential** — found by the proof lane
auditing the runner it was running under. In its own words: the gate would have declared
`adm_ok=yes` on a token that cannot authenticate `claude` at all, so **"the gate's green and the
real green are correlated by luck in this run, not by what the gate verifies."**

It then proved the obvious repairs are ALSO wrong: in that container `CLAUDE_CODE_OAUTH_TOKEN`
is UNSET, `claude auth status` returns `{"loggedIn": false, "authMethod": "none"}`, and a fresh
nested `claude -p` reproduces the documented trap verbatim — `"subtype":"success"` **with**
`"is_error":true` and `"Not logged in"` — while the dispatched session ran 338 events fine,
authenticated over `CLAUDE_CODE_MESSAGING_SOCKET`. **Both available probes false-negative.** So
the two credential families are now probed and reported SEPARATELY, by name and never by value,
and **neither gates**. A gate that cannot verify a thing must not claim to.

**That is twice in one arc a gate was found asserting something it had not checked, and both
were found by running rather than reading.**

### Residual risk carried forward, not hidden

- **The fuse is proven on a SYNTHETIC stall only.** The mechanism — event silence → kill →
  diagnose → receipt — is exercised end-to-end by a test that fires it, but a genuine
  provider-side hang cannot be induced on demand.
- **`-Detach` versus the codespace idle timeout is UNMEASURED for a long lane.** A detached run
  holds no ssh connection, and whether GitHub counts a background process as activity was never
  tested. Lane B was too short to tell. **Attached long lanes are proven; detached long ones are
  not.**

Full evidence, timelines and receipts: `win-tooling` `docs/2026-09-01-lane-632-codespace-arc-packet.md`
(merge `49cb75e`); substrate verdict recorded in `win-tooling` `config/dispatch/dispatch-cockpit.md` §7.
