# NIGHT WINDOW REPORT — 2026-08-31 23:39 → 2026-09-01, batch-E drain, consumption, universalization prep

- **Class:** technical · **Author:** CC (Opus 5, background job, night orchestrator seat)
- **Mission:** `NIGHT-MISSION-2026-08-31.md`, pre-authorised; the operator's GO ratified it
  together with five rulings — R-ENUM, R-README, R-VISION, R-MODELS, R-NOSTOP
- **Consumed by:** `[#614]` (the frozen execution arc this window drained) and **ADR-114**
- **Operator questions consumed during the window: ZERO.** Everything below batches here.

> **THIS IS NOT THE BATCH CLOSE PACKET, and the distinction is load-bearing.** The batch-E
> manifest names `docs/audits/2026-09-01-technical-batch-e-close-packet.md` as its `closed_by:`,
> and the batch is open **only while that path is ABSENT from the committed tree**. Three lanes
> are unresolved and DM-4's harvest is owed, so landing that path tonight would be *closing the
> batch by assertion* — which the manifest's own REFUSE-TO-FINISH section forbids by name. This
> file is the window report the mission's WAVE 4 asks for; the close packet is a separate act,
> and it belongs to whoever resolves the three.

## 0 · The one-paragraph verdict

Batch E moved **7 → 11 of 15 merged**. Five operator rulings landed or were measured to be
blocked, with the blocker named in each case rather than asserted. Three lanes did not land and
each has a named cause: DC-23 **refused correctly** and its refusal is the deliverable, DM-1 and
DM-2 are blocked by their own frozen contracts on tier-(B) inputs that do not exist, and DM-4 is
still running off-machine. **The most consequential finding is self-inflicted:** the integrator's
own R-ENUM merge wedged three of four live hub lanes through a tree-lag mechanism that is now
documented in PLAYBOOK — a doctrine that was written hours before it collected its own witness.

## 1 · Against the ex-ante numbers, verbatim

| # | Ex-ante | Outcome |
|---|---|---|
| **N1** | batch E merges 6/15 → 15/15, or each shortfall named | **11/15 merged.** Measured start was **7/15** by the prior seat's count and **5/15** by merge-commit count; this report uses merge commits. Four shortfalls, each named in §2: DC-23 (refused), DM-1, DM-2 (tier-(B) input absent), DM-4 (cloud, still active — owes a harvest, not a merge). |
| **N2** | DC-23 resolved; HY-1 merged if stopped; zero stopped-and-unmerged lanes; worktree list == primary only | **HY-1 was already merged** before the window. **DC-23 resolved as STOPPED-BY-REFUSAL** with zero writes. **Zero stopped-and-unmerged lanes.** `git worktree list` in the hub == primary only; win-tooling carries four PRE-EXISTING worktrees that are not this batch's (§9). |
| **N3** | A5 in PLAYBOOK · A7 row + parity row born · both step-4 mechanisms live with tests · anchor doctrine landed | **PARTIAL, 2 of 4.** A5 landed (`5c7e9e37`). Anchor doctrine + kill-guard + create-not-rebuild landed with it. **A7 births NOT taken** — A7's own verdict is that nothing in `tasks/` authorises an admission act and its quota proposal is a CANDIDATE it "may draft and may not file"; filed as intake **#64** instead, which is ADR-111's only route. **Step-4 mechanisms NOT built** — they touch `scripts/`, which was a live lane's frozen write-scope for most of the window; named in §11. |
| **N4** | north-star regenerated; funnel_lifecycle 0 FAIL; the 11 structural WARNs resolved or named | **north-star regenerated — output byte-identical**, i.e. it was already current, which is itself the check. `funnel_lifecycle` is ship-tier and not run at the commit gate; the funnel baseline was re-stamped (§4 D2). The 11 structural WARNs are **UNLOCATABLE, which is stronger than unverified** — see §13. |
| **N5** | six drift REDs re-stamped with deltas; suite green minus the named pre-existing set | **4 of 6 cleared, 2 named** (§4). **Two of the four turned out to be REAL defects, not count noise**, and were fixed rather than baselined over. The full-suite result is at the foot of §5. |
| **N6** | operator questions consumed: 0 | **0.** Everything batched to §10. |
| **N7** | consumer_at_landing: zero unnamed survivors | **MET. 46 → 0 WARNs.** Nine discharged by citation; the remaining 34 are UNDISCHARGEABLE by construction, named in the baseline provenance and filed as intake **#65**. |
| **N8** | both instantiation contracts exist, every premise live-verified | **MET** — `docs/audits/2026-09-01-technical-universalization-instantiation-prep.md`, and the plans are DERIVED from `deploy/tool.py --target` read-only runs rather than authored. |
| **N9** | the v1.5.0 release-candidate draft passes release_lint | **MET.** `release_lint --version v1.5.0` → **0 FAIL, 7 pass, 1 WARN**, and the WARN is C2-tag: *"git tag v1.5.0 does not resolve yet — pre-release state; the operator tags at release"*. |

## 2 · Batch E, per lane, against its own ex-ante done-contract

| Lane | Slug | Merge | Verdict vs done-contract |
|---|---|---|---|
| DC-1 | lane-a-1-vision-to-readme | `ea1e32a9` | MET (pre-window) |
| **DC-23** | lane-b-2-essentials-and-claude-md | — | **NOT MET, and the refusal IS the deliverable.** Act One is bound to the A3 census, which named **ten breaking consumers of `ESSENTIALS.md`, none inside the frozen write-scope** — seven live instruction lines in `SESSION_SETUP.md`, the CLAUDE-md onboarding template, a HUB region deploy-carried to every ADR-104 member, two registered-spec citations, an ADR-88 register entry whose recorded justification IS the gate dissolution would make vacuous, five set memberships in `canonical_docs.py`. A second, independent blocker sits INSIDE the footprint: the floor carrier is hash-guarded three ways and `release_lint` C5 asserts the equality, while the sidecar and three manifests are out of scope. **Zero writes, tree clean.** |
| DC-4 | lane-c-3-root-contract | `1a3c378b` | MET (pre-window) |
| DC-5 | lane-d-4-ai-council-instantiation | `76f184fb` | **MET, and the honest half is what it did NOT do.** The granted `ecosystem/ai-council/` write-scope goes **unused** and is named as unused rather than filled with a fabricated file — the exact anti-pattern its own done-contract warns about. Delivered a provenance annotation on `deployed-versions.yaml` following win-tooling's precedent, and surfaced two gaps it was out of scope to fix. |
| **DM-1** | lane-e-5-eval-sda1-harbor | — | **NOT DISPATCHED, by its own contract.** *"Blocked by: Tier (B)'s SDA-1-to-Harbor translation draft. Without it this lane has no input."* Payload B-2 has not been run; `TIER-B-COPILOT-PAYLOADS.md` states in terms that *"Enterprise Copilot is not driveable from this seat."* Dispatching would have bought an immediate refusal. |
| **DM-2** | lane-f-6-observability-otel | — | **NOT DISPATCHED**, same class — blocked on tier-(B) payload B-1, the OTel GenAI event schema. |
| DM-3 | lane-g-7-typed-multi-layer-graph | `7b0cbf14` | MET (pre-window) |
| **DM-4** | lane-h-8-local-memory-tier-l-evaluation | cloud | **DISPATCHED THIS WINDOW, still ACTIVE.** `cse_01SHFSuLrRTLfraAwUtuqBqC`, three receipt gates green at dispatch (G1 created / G2 bound to `git_repository` / G3 first-assistant-text at 72 s). It is a tier-L EVALUATION — 20 real questions, local vector index vs grep — and owes a HARVEST, not a merge; it writes no tree file. |
| DM-5 | lane-i-9-distiller-filing-amendment | `bea4c623` | MET (pre-window) |
| DM-6 | lane-j-10-equilibrium-checkpoint-blind-spots | `b7fef9b9` | **MET.** Routed `already-a-row`, so an amendment rather than a birth. Re-measured AUT-R3's B3 finding and found it **STALE**: `telemetry_emit` imports in EIGHT `scripts/*.py` modules, not the one call site B3 counted. Committed by the integrator after the lane wedged (§3). |
| HY-1 | lane-k-11-derived-doc-freshness | `9b736ce2` | MET (pre-window) |
| HY-2 | lane-l-12-logs-retention-rule | `1c92024f` | **MET.** A retention RULE, not a cleanup: 393 lines with RED-first tests, month buckets to avoid minting single-file folders (Z-G5), `logs/TOKEN-LOG.md` excluded ABSOLUTELY (ADR-29/39 has no archival carve-out for it) and `PROPOSALS-*`/`DETECTOR-ERROR-*` excluded by prefix because two live callers glob them flat. A dry run against this repo is a no-op — **the organ is ahead of the next producer, not behind this one**, and it says so. |
| HY-3 | lane-m-13-templates-disposition | `4bc754b4` | **MET.** 47 verdicts: 44 universalize, 2 retire (executed), 1 class of 3 relocate (**flagged, not executed** — content authorship, outside the decision budget). The inherited-vs-measured split is declared in the artifact's own header, which is what lets a reader tell a disposition lane from one that did the work twice. |
| HY-4 | lane-n-14-trends-burndown-and-quota-panel | `720d3e09` | **MET.** 718 lines, RED-first, 94 tests green. Two disciplines pinned: the burn-down **reads** `gen_north_star.ARCS` rather than restating it, and the quota panel renders credits as a **named absence** because no store here can compute a balance. |
| HY-5 | lane-o-15-wintooling-local-default | `32d19df` (win-tooling) | **MET.** `Dispatch-After`'s `-Substrate` defaulted to `cloud` — the only place in that repo where an unqualified "new chat" left the workstation. Now `local`; cloud and codespace still reached by naming them. 48 tests green. |

**Merged this window: DC-5, DM-6, HY-2, HY-3, HY-4, HY-5 — six.** Plus the four already merged
before it, that is **11 of 15**.

## 3 · The finding that cost the most, and it was the integrator's

**Three of four live hub lanes were wedged by the integrator's own R-ENUM merge.**
`check_journal_spine_anchor` walks `main`'s first-parent spine from the SHARED refs and reads
`JOURNAL.md` from the **LOCAL working tree**. Every lane was based at `e96638da`; the R-ENUM merge
and its anchoring JOURNAL entry landed on main while they worked; from inside a lane's tree that
merge reads as **unanchored**, and `audit-health` is a PRE-COMMIT gate, so every commit in that
lane is refused.

**They were not slow and not hung. They were correct and blocked**, and each spent roughly an
hour investigating the block instead of finishing:

```
j-10  called AskUserQuestion -> InputValidationError -> 46 minutes of nothing.
      A --bg lane has NO answer channel; PLAYBOOK Ch8 states it in terms.
n-14  spent its last hour grepping scripts/audit.py for what sets the health exit code.
m-13  ran `git fetch` and grepped its own JOURNAL for the offending SHA -- i.e. it had
      diagnosed the gap exactly and was waiting for someone else to close it.
o-15  UNAFFECTED -- it runs in win-tooling, whose main did not move.
```

**Every one of the three refused to `--no-verify`.** That refusal was right. What none of them
knew is that `git merge --ff-only main` into the lane is a plain git operation the batch protocol
does not forbid — *"no self-merge"* scopes lane-to-**main** — and it fixes the block at its cause
with no merge commit, because each lane had zero commits ahead and no dirty file in the diff set.
Applied to all three; all three then committed clean.

**The doctrine that names this landed in the same window** (`5fcb5195`), written before it
collected its own witness. It also fired **in mirror**: this seat's own cleanup probe,
`Where-Object { $_.CommandLine -like "*lane-j-10-…*" }`, **matched itself** and killed the
PowerShell running it — which is precisely why the rule says match the command line, never a bare
substring, and why a sweep keyed loosely takes its own orchestrator.

## 4 · The five rulings, and what each actually cost

**R-ENUM — LANDED, `7612a751`, all three legs in one commit.** `SHAPE_ENUM += codespace`;
`Dispatch-Codespace -Contract <FILE.md> -Slug <slug>` in the verb table; `shape=codespace` pairs
`worktree-<slug>`, not `claude/`. 120/120 in the lane-contract suite with **10 new RED-first
witnesses**; all 22 frozen batch-E contracts still pass unchanged. **A fourth thing the three legs
exposed, resolved in the same commit:** the receipt gate was keyed on the literal string `cloud`,
so a codespace contract carrying a `## Receipt gate` was refused as "a cloud-lane rule" while one
WITHOUT a gate went unchecked — a rule written to one instance of its own class. It now keys on
`RECEIPT_SHAPES = (cloud, codespace)` with per-shape fields, because the traps differ.

**R-README — LANDED, `53c1f371`.** Three things left the front door: the fleet-shape paragraph,
the restated roster and count, and the parity posture — **which was also already false**, claiming
`canonical-doc-vision` is "MUST on all nine" when lane-a had retired it to SHOULD hours earlier.
Restating a parity tier in a front door is how one tier change becomes a lie in a second place.

**R-VISION — MEASURED, AND BLOCKED. Tried rather than argued.** The file was moved to
`docs/archive/` and the gates were run against the moved tree. Two hard legs:

```
audit.py health EXITS 1 -- vision_md: VISION.md absent at repo root   (a FAIL, so it refuses
                                                                       EVERY commit in the repo)
test_gen_handoff_still_extracts_the_live_vision_section REDs -- gen_handoff.py lifts VISION's
                                                                `## Vision` into every bundle
```

Reverted; recorded in `ecosystem/registry.md`. **The registry retirement (a TIER change, taken)
and the file's archival (a PATH change, not taken) are two separate acts.**

**R-MODELS — HONOURED.** Orchestrator and every integration adjudication ran **Opus**. All seven
dispatched lanes ran **Sonnet**, set at dispatch through `Dispatch-Local`'s own `-Model` parameter
— never a composed `claude --bg` line. **Haiku was not used**, because no step this window was
purely mechanical regen or harvest; that is a report, not an apology.

**R-NOSTOP — EXERCISED TWICE, and it is the reason the window did not stall.** S4 fired at
`check_silent_rule_ratchet` and again at win-tooling's `canonical_freshness`. Both froze **only
their own queue**; every other wave continued. The first was later resolved without a ruling (§5).

## 5 · The six drift families

| | Family | Outcome |
|---|---|---|
| **D1** | `test_validate_adr_status` (4 tests) | **CLEARED — and two of the four divergences were REAL DEFECTS, not count noise.** `coherence 3→4`: **ADR-114's header reads `Accepted` (ruled 2026-08-29) while the ADR index still led its row with `PARKED`** — a superseded status carried for three days after ratification. `unindexed 0→1`: **ADR-116 had no index row at all**, a state where coherence is *indeterminate*, not clean. **Both fixed rather than baselined over**, after which the distribution returns to exactly `coherence=3` on {ADR-45, ADR-46, ADR-47} and `unindexed=0`. Only then were the two genuine deltas re-stamped: count `88→89`, `G1 41→42`, single cause **ADR-116**, with G2/G3/G4 unchanged as the check that it is one ADR and not grammar drift in disguise. |
| **D2** | funnel baseline | **RE-STAMPED with `--allow-raise`, deliberately.** The raise covers ~25 audits accumulated since 2026-08-29, not just tonight's. **The disposition debt is NOT discharged**: ADR-111 routes each to OWNED/DISCHARGED/CANDIDATE/REJECTED and that triage is the architect's. |
| **D3a** | doc_rot citation regex | **CLEARED — and it was CAUSED BY THIS WINDOW.** The consumption sweep cited seven censuses by BARE filename and the citation regex false-strips a bare dated name. Re-written with `docs/audits/` paths, which doc_rot accepts and `consumer_at_landing` still resolves. |
| **D3b** | doc_rot accretion arm | **NOT CLEARED, and the reason is itself a finding.** ARM 1 fires on `BACKLOG#267` — *3 history dates spanning 53d, 2188 chars*, calendar-driven, the row crossed a 30-day span without being edited. The ratified relief is `scripts/archive_row_body.py`, and **it cannot reach this instance**: `propose` reports exactly one relocatable row, `[#610]`, because `[#267]`'s narration is not in the clause-run shape the tool relocates. **The arm fires on a row the relief mechanism does not reach.** |
| **D4** | consumer baseline | **RE-STAMPED with explicit provenance.** The 34 undated survivors are NOT consumed and NOT discharged — they are UNDISCHARGEABLE (§7). The re-stamp preserves the ratchet's ability to catch FUTURE growth, which a permanently-red gate cannot do. |
| **D5** | `test_vi_batch1_reproduces_the_wrong_id_citation` | **NAMED, NOT RE-STAMPED.** Measured `['[#587]'] → ['[#577]', '[#584]', '[#587]']` (+2); both additions trace to ADR-115's execution rows entering the corpus. Whether the predicate's verdict on those two is right is an adjudication, not a re-measure. |
| **D6** | `test_no_gate_hook_or_script_reads_the_export` | **VERIFIED as the known false positive, and ALREADY OWNED** — `tasks/586-*` exists for exactly this RED. The two references are `ecosystem/conformance.html` and `.md`, generated report artifacts appearing in no hook, gate or script. |

**The silent-rule ratchet, which is the one that nearly cost the night's doctrine.** The held
PLAYBOOK set measured `live 453 > baseline 443` and *raising a baseline is an operator ruling* —
so it was **committed and parked** with the raise attributed line by line. It landed later without
a ruling because two things moved: **HY-3 retired two zero-consumer templates into
`templates/archive/`, which the detector EXCLUDES** (453 → 440), and **seven genuine false
positives were drained** — sentences that describe a fact rather than state a rule, each quoted
before/after in `5c7e9e37` so the judgement is reviewable in thirty seconds. Net `443 <= 443`.
**No live rule was reworded.** Seven miscounted non-rules out, seven real rules in; the pool ends
the window where it started and the proxy is more accurate than it was.

### The full suite, run ONCE at integration

```
11 failed · 4,735 passed · 3 skipped · 1 xfailed · 1,057 s (17:37)   primary checkout, HEAD
```

**Against 0b's pre-batch measurement of `28 failed · 4,605 passed`** — which was taken in a
WORKTREE, so 19 of its 28 were environment artefacts (17 `pandas` misses needing
`--group analytics`, one `test_stale_worktrees` that REDs *because* a worktree is live, one known
main RED). This run has none of those. **All eleven are classified, and only two were caused by
this window:**

```
CAUSED HERE, FIXED HERE (2)
  test_gen_audit_index::test_live_index_is_fresh
  test_gen_audit_index::test_live_index_excludes_nothing_because_every_audit_is_tracked
      -> three audits landed and the generated index was stale. A LANE must NOT regenerate it;
         the INTEGRATOR at close must. Regenerated; 19/19 green.

NAMED IN THE SIX DRIFT FAMILIES (3)
  test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export     D6, owned by tasks/586
  test_preflight_freeze_predicates::test_vi_batch1_reproduces_the_wrong_id_citation   D5
  test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings...   D3b

PRE-EXISTING ON main, VERIFIED AT 7612a751 (3)
  test_cloud_provisioning::test_the_gate_never_syncs_the_environment_it_is_asserting
  test_cloud_provisioning::test_provision_sh_runs_the_history_repair_before_arming_hooks
      -> the F1-F4 provision.sh work landed without updating these two.
  test_enforcement_coverage::test_anchor_gate_probe_distinguishes_installed_from_absent
      -> the known main RED the plan's own non-drift list already names.

FULL-SUITE-ONLY FALSE REDS -- GREEN IN ISOLATION (2)
  test_reverse_dep_oracle::test_finding_headline_resolves_with_provenance   assert 3 >= 50
  test_reverse_dep_oracle::test_main_finding_json_exit_zero                 assert 3 >= 50
      -> re-run alone: 21 passed. A measurement taken while the corpus is being measured.

PRE-EXISTING AND OUTSIDE THE SIX, newly named here (1)
  test_desired_state_report::test_live_report_renders_the_real_fleet
      -> its module-level MEMBERS pin lists FIVE members and was last touched 2026-08-19; the
         live report renders SEVEN -- the five plus `terminal-setup` and `win-tooling`. It fails
         in ISOLATION too, so it is a genuine RED and not an ordering artefact. NOT fixed: the
         pin is a shared fixture constant used by seventeen other tests in the module, and
         widening 5 -> 7 without establishing WHY the two entered the desired-state model would
         hide the signal rather than read it. The test's own name says it should assert the real
         fleet; the honest repair is to derive the column set from the loader instead of pinning
         it, which is a change with a design in it, not a re-stamp.
```

**So: nothing this window introduced survives, and the residue is eight pre-existing or
structural REDs, each with an owner or a named reason.**

## 6 · Substrate table — what ran where

| Lane / act | Substrate | Model | Receipt |
|---|---|---|---|
| DC-5, DM-6, HY-2, HY-3, HY-4 | LOCAL worktree, hub | sonnet | branch `worktree-lane-*` + merge commit |
| HY-5 | LOCAL worktree, **win-tooling** | sonnet | `432e8a3`, merged `32d19df` in win-tooling |
| DM-4 | **CLOUD** (`claude/` prefix) | sonnet | `cse_01SHFSuLrRTLfraAwUtuqBqC` — G1 created / G2 bound `git_repository` / G3 first text at 72 s |
| Orchestration + every integration adjudication | LOCAL, primary checkout | **opus** | this report, and the merge commits |
| Tier (A) ×7 (censuses) | CLOUD | — | executed 2026-08-31, pre-window; consumed §7 |
| Tier (C) codespace admission probe | CODESPACE | — | executed 2026-08-31, pre-window |
| **Tier (D) codespace proof-of-work** | **not dispatched** | — | **unblocked by R-ENUM tonight; dispatches in the morning, attended** |

**Every committing lane ran LOCAL, as the operator ruled.** `codespace` became *expressible* in
the contract grammar tonight and was deliberately not *used* — the substrate was admitted for
running on 2026-08-31 and the paperwork for it did not exist until `7612a751`.

**Dispatch surface note, recorded because it is a small defect in a ruled verb:** every
`Dispatch-Local` invocation printed `'m' is not recognized as an internal or external command`
before backgrounding successfully. Cosmetic, seven for seven, no lane affected — but it is a
stray token in the fleet's canonical launch path and belongs to win-tooling.

## 7 · Audit-consumption sweep

```
before   46 artifacts cited by no governance surface
after     0 WARNs
```

- **9 DISCHARGED BY CITATION**, named from the row whose arc commissioned them: the batch-E
  manifest, all seven tier-(A) censuses, the codespace admission-probe verification, and this
  window's own universalization prep. Later joined by HY-3's disposition artifact.
- **34 UNDISCHARGEABLE BY CONSTRUCTION**, and this is the finding. `consumer_at_landing` resolves
  a cited identifier only through `_STEM_RE`, which requires it to **start with a date**. Launch
  contracts do not: `LANE-a-1-vision-to-readme.md`, `PLAN.md`, `CUT.md`, `PROBE-*.md`,
  `TIER-B-COPILOT-PAYLOADS.md`. **Measured as a controlled experiment** — one citation block, one
  commit, one file: the dated census name resolved; the undated lane name, written the same way
  with the same full path, did not.
- **The module's own v2 bump created the asymmetry.** It made the corpus RECURSIVE precisely so
  these files would be measured, and left them unresolvable by the discharge leg. They now sit
  inside the measurement leg and outside the discharge leg — strictly worse than before, because
  the debt is counted and cannot be paid.
- **A second, independent cause on the same symptom:** PLAYBOOK Ch8 names the batch close packet
  as a launch contract's consumer, and `docs/audits/` is deliberately EXCLUDED from the governance
  pool. The doctrine names a consumer the mechanism structurally cannot accept.
- Filed as intake **#65**. **Not fixed here** — widening identity changes what the ratchet
  measures and forces a `DETECTOR_ID` bump plus a reviewed re-baseline, which is the deliberate
  act the discipline exists to require.

## 8 · Universalization prep — zero consumer-repo writes

- `deploy/manifest-v1.5.0.yaml` — **release candidate, 0 FAIL / 7 pass / 1 expected WARN.** A
  MINOR whose new material is a **state change, not a new carrier**, and whose header says so.
  Two items stay RECORDED and NOT DECLARED on the manifest's own rule that *"declaring a component
  against a payload that does not exist lints green but is undeployable"*: the `readme-front-door`
  pair (its `templates/README-md-template.md` does not exist) and the `doc_shapes` spine re-point.
- **Both instantiation contracts are DERIVED, not authored.** `deploy/tool.py <repo> --target
  v1.4.0` read-only produced an **identical** plan for corp-monorepo and ai-council — 4 carriers
  need apply, 2 correct, 1 not implemented — and an **identical hard blocker**: the `ruff-gate`
  prune finds the component `present_modified` and **WOULD REFUSE**, so `--execute` aborts with no
  record and no staging. **Neither instantiation can complete until that one component is
  adjudicated**, and adjudicating it means reading the local edit with the diff in hand.
- **A finding from trying it:** the deploy preflight refuses an untagged target **even in assess
  mode**, so a release candidate cannot be dry-run against a consumer before the operator tags it.
- **Parity blast radius, counted:** flipping `root-readme-md` consumer-wide today turns **SIX**
  members MUST-absent at severity ERROR (`check_fleet_parity` BLOCKS); `root-agents-md` turns
  **EIGHT**. The rule that follows: **the tier is a two-role scalar, not a per-member map**, so
  the consumer role stays `LOCAL` until the LAST member has the file and per-member progress lives
  in `deployed-versions.yaml`. Expressing partial progress in `tier:` REDs everyone else at once.
- **One premise refined by measurement:** `AGENTS.md` is **hub-only across the entire fleet**.
  ADR-115 made it the portable instruction layer on 2026-08-25 and no consumer carries one.

## 9 · Teardown proof, across every substrate enum

```
LOCAL / hub        git worktree list  ==  primary only          VERIFIED
                   .claude/worktrees/ ==  empty                 VERIFIED (three dirs needed a
                                                                 held-handle sweep after the
                                                                 branch delete succeeded)
                   git branch --list "worktree-*"  ==  empty    VERIFIED
LOCAL / win-tooling  lane-o-15 worktree entry removed, branch deleted   VERIFIED
                     directory CONTENTS removed; the now-EMPTY dir is
                     held open by two pwsh processes that PREDATE this
                     window (started 10:14, not this seat's to kill)   ** OPEN, §13 **
                     four PRE-EXISTING worktrees remain (cloud-fail-fast, cloud-models,
                     external-text, fix+check-advisory-unowned-path) -- NOT this batch's,
                     NOT touched, reported
CLOUD              DM-4 still ACTIVE -- teardown is its harvest, and it is owed
CODESPACE          nothing dispatched; the STOPPED admission container
                   `batche-c-admission-pgw54jqwv7qf65rj` is the prior seat's and is
                   deliberately left for an operator delete (stopping is not deleting)
```

**Sessions swept:** the two b-2 sessions and one 5-hour lane-a-1 zombie at the start; the two
completed lanes when memory ran short; four orphans from already-merged lanes; then j-10, n-14 and
m-13 as each was reaped. **All by COMMAND-LINE match with the current process excluded** — the
one time that exclusion was missing, the probe killed its own shell.

## 10 · Quota, models, and the curve that does not exist

**The quota curve cannot be drawn, and that is a measured fact rather than an omission.** A7
re-ran the search at HEAD: `quota`, `quota_source` and `quota-source` appear in **four places
repo-wide, all of them audit prose about the field's own non-existence** — zero code, zero YAML,
zero schema. **There is no quota surface in this repo and there never was.** HY-4's panel, merged
tonight, renders credits as a **named absence** for exactly this reason, and filing the field is
intake **#64** — which carries its own two-day-old counter-precedent (`86bed82`, where a rich
provider entry was refused on the ground that *"the registry is a provider/CLI identity
surface"*).

**What CAN be reported, because it was observed:** every model request tonight went through the
operator's subscription. Orchestrator + integration adjudication on **opus**; seven lanes on
**sonnet**; **haiku unused**. The real constraint the window hit was not quota but **memory** —
§11.

## 11 · Asset balance — SMALLER / VISIBLE / UNBLOCKED

**SMALLER**

```
templates/ live (non-archive)   43  ->  41   (2 zero-consumer retirements, HY-3)
templates/archive/               4  ->   6   (47 tracked under templates/ either way)
silent-rule pool              443  -> 443   HELD -- 7 non-rules out, 7 real rules in
README.md                     fleet governance, roster and parity posture REMOVED
docs/decisions/README.md      one superseded status line and one missing row, both closed
```

**VISIBLE**

```
unconsumed audit WARNs         46  ->   0   (9 discharged, 34 named + filed)
trends dashboard             +2 panels: arc burn-down (reads ARCS) + quota (named absence)
PLAYBOOK                     +A5 portability boundary, +3 night rules, +codespace row
ecosystem/registry.md        now carries fleet shape + migration posture + the R-VISION
                             measurement, beside the roster they qualify
intake                       +2 SEEDs, both raw findings on ADR-111's only route
north-star                   regenerated -- byte-identical, i.e. already current
```

**UNBLOCKED**

```
codespace lanes              REFUSED by three closed enums  ->  expressible and gate-clean
tier-(D) proof-of-work lane  blocked on contract grammar    ->  dispatchable, attended, AM
corp-monorepo + ai-council   no instantiation plan          ->  derived plan + named blocker
v1.5.0                       no candidate                   ->  release_lint-clean draft
DM-1 / DM-2                  blocked on tier-(B)            ->  STILL BLOCKED (unchanged)
```

**The bound that actually bit was MEMORY, not quota or integration capacity.** With six local
lanes live the box reached **118 `claude` processes and 1.7 GB free of 27.7 GB**, and a `git
commit` failed with `fork: Resource temporarily unavailable`. The documented batch ceiling of 4–6
lanes is justified by *integration* capacity; this is a **second, independent bound at the same
number for a different reason**, and it is worth writing into the ceiling's rationale.

## 12 · Questions batched for the operator — nothing was asked during the window

1. **DC-23's own escalation, carried verbatim.** *"DC-2 and DC-3 were merged into one lane by
   ruling CUT-3(a) for **write-scope** reasons, not because DC-3 depends on DC-2. Does DC-2's
   refusal stop DC-3, or should DC-3 run alone?"* The lane adds, and it is checkable: **ACT
   THREE's condition is already satisfied** — DC-1 is merged, and the VISION lines at
   `CLAUDE.md:39` and `:68` are landable whenever DC-3 runs. If DC-3 is cleared to run alone its
   footprint needs no change. If DC-2 is to be re-cut, its write-scope must grow to cover the ten
   breaking surfaces plus the floor sidecar and `deploy/manifest-v1.4.0.yaml` — **at which point
   it is no longer a doc lane but a fleet-coupled one.**
2. **Tier (B): run B-1 and B-2, or re-route them?** DM-1 and DM-2 are blocked on Enterprise
   Copilot payloads that only the operator can run. The payloads are self-contained thinking tasks
   and the standing offload rule would permit `agy`/`grok` — **deliberately not done**, because
   the payload pack assigns the routing and substituting the provider changes the artifact's
   provenance for work that then produces committed code. One word unblocks two lanes.
3. **`ruff-gate` is `present_modified` in BOTH consumers.** Both instantiations abort on it. The
   local edit needs reading, not deleting.
4. **Does `consumer_at_landing` widen its identity, or does `docs/audits/` enter the governance
   pool?** Intake #65. Two causes, one symptom; one ruling settles both.
5. **May the provider registry hold a quota locator at all?** Intake #64, against `86bed82`.
6. **win-tooling's commit gate is wedged for every author.** `canonical_freshness` FAILs on three
   canonical docs stale since 2026-08-29 at the latest. The HY-5 merge declared a single-hook
   bypass with the pre-existence proven; **the docs were NOT stamped**, because a stamp means
   *re-read end-to-end* and a night seat stamping three unread canonical docs is the fake stamp
   the gate's own message forbids.
7. **A5's raise request is WITHDRAWN** — it landed under the existing baseline. No decision owed.

## 13 · What the batch still owes, and why this file is not its close packet

```
DC-23   REFUSED with zero writes. Needs the operator's answer to question 1 above.
DM-1    Blocked on tier-(B) payload B-2. Unblocks the moment the payload runs.
DM-2    Blocked on tier-(B) payload B-1. Same.
DM-4    ACTIVE off-machine at packet time. Owes a HARVEST, not a merge.
```

Plus, owed and named rather than quietly dropped:

- **N3's step-4 binding mechanisms are NOT built** — the consumed-artifact filename predicate, and
  H1-before-provenance + index REDs on title-less. Both target `scripts/`, which was a live lane's
  frozen write-scope for most of the window; building them alongside would have been the
  write-scope collision the freeze exists to prevent.
- **N4's eleven structural WARNs are UNLOCATABLE, and that is a stronger finding than
  "unverified".** PLAN U-12 carries the claim -- *"the 11 structural census WARNs clearing on merge
  commits"* -- from an operator-side brief, explicitly unverified. Searched at HEAD across `docs/`,
  `protocols/`, `scripts/` and `tasks/`: the phrase appears in **exactly two places, both of them
  PLAN.md restating its own unverified claim**. No census enumerates eleven structural WARNs; no
  surface names which eleven. **So the claim cannot be verified or refuted, because its subject
  does not resolve** -- and reporting them "resolved on merge" would be asserting against a set
  nobody can list. Same class as the *"five-pillar close"* term PLAYBOOK already records as
  unlocatable rather than reconstructing from guesswork. For scale: `audit.py health` reports
  **75** WARN lines at HEAD, so eleven is not a number the live gate produces either.
- **`templates/README-md-template.md`** — the one payload the whole README migration waits on.
  First morning act; it needs `templates/` free, which it now is.
- **win-tooling's `lane-o-15` worktree directory** survived its own teardown: the git entry and
  both branches are gone, its CONTENTS are gone, and the now-EMPTY directory is held open by
  **two `pwsh` processes started at 10:14** -- hours before this window began and not this
  seat's to kill. One recursive delete once they exit.
- **The ~25 audits raised into the funnel baseline** owe ADR-111 triage.

**The batch stays OPEN by design.** `docs/audits/2026-09-01-technical-batch-e-close-packet.md` is
deliberately ABSENT from this tree, which is what keeps the ADR-110 exemption armed for the lanes
that remain. Writing it tonight would end the exemption while four items are open and would be
closing the batch by assertion — the one thing its manifest names as forbidden.

---

## AMENDMENT 1 — 2026-09-01 02:45, appended after the report first landed

> **In-file amendment marker, not an edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3),
> so the body above stands exactly as written at 02:20. Everything below happened afterwards and
> changes three of the numbers it reports. **Where the two disagree, this section wins.**

### N3 moves from 2-of-4 to 4-of-4

The body records the two step-4 binding mechanisms as **NOT BUILT**, with the reason that they
target `scripts/`, which was a live lane's frozen write-scope. **That condition ended when HY-3
merged**, and both were built with RED-first witnesses in the two hours after this report landed.

**`5069ce5f` — the audits index REFUSES a title-less artifact.** `_title_of` returned the
placeholder `(no # title)` and nothing read it: **20 of 837 indexed audits render it**, nine of
them harvested cloud artifacts whose persist shape leads with a PROVENANCE blockquote and never
emits an H1. Armed as a RATCHET against `ecosystem/audit-title-baseline.json` — the 20 are
grandfathered, the 21st refuses — with a DRAIN direction as well, because a ratchet that only
grows is a debt register nobody pays down. **The rule is H1-PRESENT, not H1-FIRST**, and that has
its own test: `_title_of` searches the whole file, so an artifact whose provenance precedes its
heading already indexes correctly and pinning the order would refuse files that render perfectly.
Wired into `--check`, which the `audit-index-freshness` hook already runs, so no new `ALL_CHECKS`
member and none of the six count pins move.

**`4e6e0e2e` — a DECLARED input that does not open is a finding.** Measured: a probe contract
citing `docs/audits/2026-01-01-technical-DOES-NOT-EXIST.md` beside two real locators made
`preflight_contract` report *"2/2 locator claim(s) resolved"*. Scoped to clauses that DECLARE a
dependency, because a leg judging every in-repo path would refuse every contract this repo
freezes for naming its own `## Write-scope` output. **Swept over all 22 frozen batch-E contracts:
zero findings** — armed against real contracts and refusing none of them.

### Two corrections to the body's own numbers

- **§11 said `templates/ live 47 -> 45`.** Re-measured: **43 → 41** excluding `templates/archive/`;
  47 is the tracked total under `templates/` either way, which is unchanged by a relocation.
- **§1's N5 row and §5 were written before the audits index was regenerated.** Two of the eleven
  suite REDs (`test_gen_audit_index`) were CAUSED by this window and are now green; the residue is
  nine, all pre-existing or structural. The regeneration is itself the finding: **a lane must not
  regenerate that index and the integrator at close must**, which is now recorded rather than
  relearned next batch.

### One true finding about a leg this window did not touch

Pointing the new `/preflight` leg at this window's own
`2026-09-01-technical-universalization-instantiation-prep.md` FAILs **two SHA claims** —
`37b8aa1` and `7a3c057`. Both are correct: they are corp-monorepo's and ai-council's HEADs, cited
as premise evidence, and neither is in THIS repo's object store by construction. **The SHA leg
has no notion of a sibling repo**, so any cross-repo artifact reads as broken locators. Not fixed
— the artifact is immutable and the leg's scope is its own decision — and not left unsaid.

### Unchanged by this amendment

DM-4 was still ACTIVE at 02:45 (2h32m). The four open batch items in §13 are unchanged, the batch
is still deliberately OPEN, and `docs/audits/2026-09-01-technical-batch-e-close-packet.md` is
still absent from the tree.
