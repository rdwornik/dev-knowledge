# Batch-1 close packet — the four wave-1 lanes are integrated

**Date:** 2026-08-26 · **Class:** verification · **Integrator:** CC (Opus 5, background job,
primary checkout) · **Contract:** `INTEGRATE-batch-1.md` + operator amendments of 2026-08-25/26

**Read this first.** Ship-gate is **RED at 35 undispositioned WARNs** and the suite carries
standing REDs. Both are split with evidence below. Neither is a wholesale regression from this
batch, and saying "green" would be false.

---

## 1. What landed, per lane

| # | merge | lane | what it lands |
|---|---|---|---|
| 1 | `2626ff5b` | G — governance spine | 8 wave-1 row births `[#579]`-`[#586]`; ADR-115 (Proposed); ADR-111 amendment |
| — | `3387cdb2` | (integrator) | the single batch JOURNAL entry, written entry-first |
| 2 | `d74a9809` | X — green-by-skip sweep | 46 checks classified; `audit_check_count` fail-closed; cp1252 landmine defused; `propose_closures` no longer destroys the day's proposals |
| 3 | `158230c9` | CS — codespace transport | devcontainer declares the Claude Code install + `CLAUDE_CODE_OAUTH_TOKEN` path |
| 4 | `1858849a` | RL — registry filings + dispatch | `prompts/<date>/` as committed evidence; disposition register; PLAYBOOK Ch8; STANDING_RULINGS §V |
| — | `6882ef74` | (integrator) | doc-counts regenerated; the batch's own 2 funnel WARNs dispositioned |

Merge order was the operator-ruled dependency order G → X → CS → RL. No merge was reordered and
no two merges were batched between gates.

### Integration-time acts (attributed; none is lane work)

1. **Citation repair at G's merge** (amendment 1a). `[#583]`'s `refs` cited the contract-frozen
   `docs/audits/2026-08-25-green-by-skip-sweep.md`, which does not exist — `validate-hermetization`
   Rule B refuses that name for carrying no enum class token, so lane X landed it as
   `...-technical-green-by-skip-sweep.md`. Repaired in `tasks/583-*.md` (the ADR-107 source of
   truth) with `BACKLOG.md` regenerated, never hand-edited. The row's PROSE mention of the frozen
   name is deliberately retained: it records the freeze and names both paths itself.
2. **ADR-115 id-collision note** (amendment 7). Added at
   `docs/audits/2026-08-19-technical-n3-ratification-pack.md` §5.2 — disk allocation wins, the
   held draft renumbers at landing. **The path in the amendment (`docs/auditification-pack.md`)
   does not exist**; that pack is the only file holding an actual ADR-115 *reservation*, so it was
   the target. No ADR content authored, amended or ratified.
3. **Family-3 addendum** (amendment 5) — §2 below.
4. **A4/A5 registry corrections** (operator-dictated 2026-08-25) — §3 below.
5. **Two funnel dispositions** for lane G's and lane X's own artifacts, which RL's D3 register
   could not have covered because it was authored before those lanes landed.

---

## 2. The family-3 addendum (amendment item 5)

**Verified absent before appending**, not assumed: `skipif`, `tool-presence`, `shutil.which`,
`pytest.skip`, `find_spec`, `pwsh` — **all zero hits** across the artifact's 482 lines; sections
ran 0–8 with nothing on environment-conditional guards. Appended as §9 (482 → 616 lines) as an
in-file amendment marker, the sanctioned form for an immutable audit. Sections 0–8 untouched.

Contents: the **win-tooling exemplar sourced live at `5659ecb`** — `test_worktree_hygiene.py:60-63`
puts 23 tests behind one pwsh mark, and `test_repo_root_hygiene.py` exists as its own file
precisely to escape it (*"a hygiene test that can be skipped on the machine that breaks hygiene is
not a mechanism"*); **n=2 exemplars measured live here** — `test_enforcement_coverage.py`
(lines 33/381/412/446: the Informant Organ's own commit-time proof gated on `pre_commit` being
importable) and `test_floor_conformance.py:36` (a module-level mark hiding 21 tests of the ADR-93
armed-loop proof); the **measured host status** (pre_commit present → LATENT, not active: the
finding is that *nothing distinguishes the two worlds*); and the **conforming counter-pattern
already in-house** at `test_legibility_graph_conformance.py:50-71`, which is the fix shape.

Also recorded: the operator's "family 3" is **disjoint** from the three R-F4 families the dispatch
brief names, so the numbering cannot drift later. Disposition: **CANDIDATE, OWNED by `[#583]`** —
no row born, per ADR-111 and filing backpressure.

---

## 3. Operator-dictated registry corrections (A4/A5)

Applied at the RL merge as attributed integration-time fixes; content is the operator's, dictated
2026-08-25, and the integrator exercised no authorial judgment.

- **A4 · DeepSeek** now records **three independent absences**, dated 2026-08-25, deliberately not
  collapsed: (1) no official vendor CLI exists; (2) DSH cannot install on this machine — npm
  resolver livelock, measured; (3) not visible in VS Code, no IDE extension. Each rules out a
  different surface, so a merged sentence would let one surface's recovery read as restoring the
  provider. Conclusion recorded verbatim: *"DeepSeek is not a provider of this fleet on any
  surface today."*
- **A5 · Cursor** moves ABSENT → **BLOCKED-WITH-CAUSE**. The prior reading was wrong in kind:
  cursor is not missing, it is **shadowed** by the poisoned-name collision — Grok owns `agent` on
  this PATH (`agent.exe` byte-identical to `grok.exe` by SHA256), PATH index 19 shadowing a correct
  install at 28. Remedy named: PATH reordering, or pinning `cursor-agent` only. **Owner: operator**
  — PATH is host-level state, the hub only tracks the entry.

Both are **comments only**: no provider row, key or model id added or changed. Verified —
`check_provider_registry` exits 0, YAML parses.

---

## 4. Objective functions

### O1 — every born row cites a packet row id + `kill-candidates:` — **PASS, 8/8**

| row | packet source | kill-candidates |
|---|---|---|
| `[#579]` | C22+C23 (ARC-A) | none — reason stated |
| `[#580]` | C08+C09 (ARC-B) | none — reason stated |
| `[#581]` | C10+C11+C13 (ARC-C) | none — reason stated |
| `[#582]` | C30+C31+C32 + D-vis addendum (ARC-D) | none — reason stated |
| `[#583]` | C18 (ARC-E) | none — reason stated |
| `[#584]` | C02 (ARC-G) | none — reason stated |
| `[#585]` | C18 (ARC-E) | **`[#569]`** — verified OPEN |
| `[#586]` | C04 (ARC-G) | none — reason stated |

All eight cite a real packet row and carry a `kill-candidates:` line. `[#585]`'s only non-`none`
value names an open row, which the `preflight_backlog_ids` check independently confirms.

### O3 — open count and the banked ledger — **PASS, at cap**

Open rows **183 → 191**, exactly `183 + births_spent(8)`. The cap is met, not exceeded.

**Banked ledger, explicitly decremented: 29 → 21** (29 banked − 8 spent). **Stated honestly:**
the figure 29 is carried from the contract's own O3 line. I could find **no in-repo surface that
computes the banked figure** — `grep` for a births ledger returns only the unrelated "banked
ruling" sense. Per the repo's own M2 rule (*never restate a count, cite the surface that computes
it*), a ledger with no computing surface is itself a small finding, recorded here rather than
dressed up as verified.

### O2 — ship-gate RED, split explicitly with diff-scope proof — **RED at 35, split below**

`audit.py ship-gate` exits 1. The arithmetic reconciles exactly: **97 WARNs − 60 dispositioned = 35**.

| check | WARN | dispositioned | **undisp** | this window? |
|---|---|---|---|---|
| `doc_rot` | 32 | 3 | **29** | **8 yes** / 21 pre-existing |
| `undeclared_edges` | 23 | 20 | **3** | yes — the new `prompts/` tree |
| `funnel_coverage` | 33 | 33 | **0** | cleared by the 2 integration-time dispositions |
| `adr_status_grammar` | 1 | 0 | **1** | **yes** — ADR-115 |
| `fleet_audit_replication` | 1 | 0 | **1** | **no** — environmental |
| `review_artifact_coverage` | 2 | 1 | **1** | partly |
| `no_ff_merges` / `reconciled_versions` / `journal_spine_anchor` | 5 | 5 | 0 | — |
| **total** | **97** | **60** | **35** | |

**Diff-scope proof** (which files each undispositioned WARN fires against, vs the batch's 51-file diff):

- **`doc_rot` 29** — all are `backlog-row-length` over the declared 1320-char ceiling. The rows named
  are `348, 420, 426, 491, 533, 534, 541, 546, 547, 549, 552, 555, 559, 561, 564, 567, 568, 569,
  570, 571, 577, 578` (pre-existing, and the reason bare `main` already RED
  `test_validate_doc_rot`) **plus all eight new births `579`–`586`**. So **8 of 29 are this
  window's**: every one of lane G's births exceeds the row-length ceiling. That is a real,
  attributable finding and is named as debt in §6.
- **`undeclared_edges` 3** — the surviving ones sit on files this batch ADDED, chiefly
  `prompts/2026-08-25/LANE-RL-*.md → handoff-process`. Lane RL's own last commit
  (*"close the two coupled surfaces the new prompts/ tree opened"*) already dispositioned 20 of 23.
- **`adr_status_grammar` 1** — reports **88** ADR status fields where the measured baseline was 87.
  Caused by ADR-115. Same root cause as the two suite REDs in §5.
- **`fleet_audit_replication` 1** — `automation/fleet-audit` is 1 commit ahead of origin. That is a
  protected automation branch outside this batch's diff entirely. **Not this window.**
- **`review_artifact_coverage` 2 (1 undisp)** — 33 code-impact merges since 2026-08-05 lack a linked
  review artifact; two of the 33 are this batch's (`1858849a`, `d74a9809`). Advisory by the `[#480]`
  P3 ruling; the hard pre-push leg is deferred pending two clean windows.

**On the contract's "expect the 14 D3 dispositions reflected":** that number was already stale.
Lane RL measured **28** and recorded the correction in the open with its derivation
(*"the D3 instruction predicted 14; the live measurement is 28 … no subset totals 14 under any
derivation attempted"*). With the integrator's two additions, **30** dispositions are of D3 lineage.

Three **stale** dispositions matched no live WARN (`warn-row-length-533-audit-decomposition`,
`-529-telemetry-emit`, `-530-single-flight`) and are flagged by the ADR-75 decoration rule for
review/removal. Left in place: removing another lane's dispositions is not the integrator's call.

### O2 — DEGRADED probe row — **DISCHARGED**

Required: *"the `audit_check_count` leg must now FAIL loudly or pass computed, never skip-as-OK."*

- **Before** (bare `main`): `validate_doc_claims: OK — 4 claim(s) checked, no prose drift`, while
  its first leg silently read `skipped audit_check_count (… <ground truth unavailable>)`. Exit 0.
- **After** (post-X): `validate_doc_claims: FAIL — 1 claim(s) could NOT be checked (ground truth
  not computed); this run proves nothing about them` → `NOT-RUN not-computed`. **Exit 1.**

The residual `NOT-RUN` is the by-design GAP-1 cycle-break (the standalone CLI injects no ground
truth; `audit health`/`audit run` do). It is now loud instead of green. Discharged.

---

## 5. The suite RED split

**Baseline, measured on bare `main` BEFORE any merge** (25 m 26 s): **6 failed, 3938 passed,
4 skipped, 1 xfailed, 3949 collected.** Measuring this first is what makes every number below
attributable instead of guessed.

The 6 standing baseline REDs:
`test_funnel_coverage::test_committed_baseline_agrees_with_a_live_measurement` ·
`test_enforcement_coverage::test_anchor_gate_probe_distinguishes_installed_from_absent` ·
`test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export` ·
`test_reverse_dep_oracle::test_finding_headline_resolves_with_provenance` ·
`test_reverse_dep_oracle::test_main_finding_json_exit_zero` ·
`test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`

**After merge 1 the suite went 6 → 11.** Rather than charge all five to the lane, each was
re-run **serially and in isolation with nothing else running**. That resolved them three ways:

| new RED | verdict | owner |
|---|---|---|
| `test_normalize_headers::test_corpus_heading_map_indices_land_on_heading_syntax` | **PASSES in isolation** — contention with the integrator's own concurrent `audit.py health` runs | **nobody** — not a defect |
| `test_validate_adr_status::test_shipped_corpus_parses_one_status_field_per_live_adr` | **real** — ADR corpus 87 → 88 | **lane G** |
| `test_validate_adr_status::test_shipped_corpus_grammar_distribution_matches_the_measured_baseline` | **real** — grammar `G1` 40 → 41 | **lane G** |
| `test_audit::test_health_ok_with_registered_repo` | **real but the integrator's** — `journal_spine_anchor` FAILed on the unanchored merge | **cleared** by `3387cdb2` |
| `test_audit::test_health_stays_ok_with_na_status` | same | **cleared** by `3387cdb2` |

Both `test_audit` health tests **passed** on re-run after the JOURNAL entry landed, confirming the
attribution. So **only 2 of the 5 are genuine lane debt.** Recording the interference case matters:
charging a phantom RED to a lane is how a clean lane acquires a reputation for breaking things.

**Two of the 6 baseline REDs are exactly what lanes G born rows to own** — `[#585]` owns the
anchor-gate probe RED, `[#586]` owns the export-backlog-view RED.

---

## 6. Named debt — each with an owner

| # | debt | owner | note |
|---|---|---|---|
| D-1 | `test_validate_adr_status` ×2 — the measured ADR-corpus baselines (87→88, G1 40→41) must be re-measured alongside ADR-115 | **lane G** | Contract forbids fix-forward; the repo's own rule is that a baseline enum and its test move together. **Not patched by the integrator.** |
| D-2 | All 8 new births `[#579]`–`[#586]` exceed the 1320-char `backlog-row-length` ceiling | **lane G** | 8 of the 29 undispositioned `doc_rot` WARNs |
| D-3 | `undeclared_edges` on the new `prompts/` tree (3 undispositioned) | **lane RL** | RL closed 20 of 23; the remainder sit on the files it added |
| D-4 | 3 stale dispositions flagged by ADR-75 for review/removal | **operator / wave 1** | Left in place — removing another lane's dispositions is not the integrator's call |
| D-5 | `test_worktree_hygiene::test_installer_whatif_registers_nothing` asserts the ABSENCE of machine-global state, so it REDs the moment its feature is genuinely adopted | **carried, not fixed** (amendment 4) | **Correction:** the amendment says this is "named in Lane X's artifact". It is not — it is named in **RL's** dispatch brief `docs/audits/2026-08-25-technical-dispatch-brief-to-architect.md:155`, §5. Lane X's artifact does not mention it. |
| D-6 | Ambiguous `Dispatch-Codespace` display names | **fixed upstream** (amendment 4) | Now refuses with candidates rather than taking `[0]`. Same brief, §5 item 1. |
| D-7 | The banked-births ledger has no in-repo computing surface | **operator** | See O3 above |
| D-8 | `[#583]` owns the family-3 finding class at the proof layer | **`[#583]`** | CANDIDATE, no row born |

---

## 7. O5 / D1 — the substrate evidence, and the honest state of it

**The batch's biggest gap, stated plainly: lane X did NOT run on the mandated devcontainer.**
Its contract said *"MANDATORY … this lane doubles as the substrate measurement"*; the lane ran on
the local Windows 11 workstation (`$CODESPACES` empty, `OS=Windows_NT`) and **says so in its own
artifact** rather than passing local numbers off as devcontainer numbers. Its §4 is titled
*"why the substrate leg of this lane is NOT discharged"*. That is the right call — recording them
as devcontainer measurements would have falsified the record — but it means **the D1 substrate
question is not answered by the lane that was supposed to answer it.**

Its numbers are also **contended, not clean**: mid-lane inspection found two sibling lane sessions
and the primary checkout all running `audit.py health` concurrently.

**Lane X wall-times, relayed as router-ADR input with those two caveats attached:**

| measurement | value | caveat |
|---|---|---|
| codespace provision-to-ready | **not measured** | no codespace — leg not discharged |
| full `pytest`, lane branch | 1722.9 s (28 m 43 s) | local; 3976 tests |
| full `pytest`, pristine `main` baseline | 1923.6 s (32 m 04 s) | local; detached worktree at `436e7375` |
| `audit.py health` standalone | 625.6 s (~10 m 26 s) | **this IS the pre-commit commit tax** |
| commit 2 (hook-inclusive) | 296.0 s (~4 m 56 s) | stopwatch |
| commit 3 (hook-inclusive) | 241.6 s (~4 m 02 s) | stopwatch |
| targeted lane tests (4 files, 88) | 28.8 s | serial |

**One genuine substrate observation the lane could make:** running on Windows was an *advantage*
for its step 1 — the cp1252 `UnicodeEncodeError` reproduced **natively** rather than via the
ASCII-forced simulation the contract prescribed for the devcontainer, so the fix was verified
against the real failure mode.

**Consequence: smoke 5 is the only true devcontainer datapoint in this batch** — §8.

---

## 8. Integrator wall-times, and the xdist question (amendment item 5)

`pytest-xdist` **3.8.0 is installed and already active**: `pyproject.toml:162` sets
`addopts = "-n auto"`, across 16 logical CPUs. So `-n auto` is **not an available speedup — it is
the current baseline**, and every wall-time here is already a parallel number. `pyproject.toml:93-103`
documents why it cannot simply be unloaded: `-p no:xdist` also strips the `-n` that `addopts`
supplies. **Reported only; nothing switched mid-batch, per instruction.**

| run | wall-time | result |
|---|---|---|
| baseline, bare `main` | 1526.5 s (25 m 26 s) | 6 failed / 3938 passed / 3949 collected |
| after merge 1 (lane G) | 1625.9 s (27 m 05 s) | 11 failed / 3933 passed |
| isolated 5-test attribution probe (`-n 0`) | 870.7 s (14 m 30 s) | 4 failed / 1 passed |
| lane X targeted (`test_audit` + `test_enforcement_coverage`) | 910.0 s (15 m 09 s) | 1 failed / 256 passed — the failure is a baseline RED |
| lane X targeted (5 sweep/closure files) | 30.3 s | 96 passed |
| lane CS targeted (2 files) | 61.1 s | 156 passed |

---

## 9. MEMORY.md verdict — handed to the operator as L0, not repo-compacted

**Verdict: L0, handed over. Not compacted by this integrator.**

The memory index lives at
`~/.claude/projects/C--Users-1028120-Documents-Dev--dev-knowledge/memory/MEMORY.md` — **outside
this repository**, in the `~/.claude/` runtime tree. Core-invariant #6 makes global-infra edits
**exception-with-ruling, never unilateral**, and `CLAUDE.md` §5 rule 7 puts that tree outside what
this repo authors. An integrator compacting it mid-batch would be exactly the silent global drift
that rule exists to prevent — and it is the same class of boundary the A5 correction respects by
assigning PATH remediation to the operator rather than the hub.

It is genuinely large and worth a compaction pass; that pass is the operator's to authorize.

---

## 10. What next

1. **Wave-2 gate — the router ADR consuming the wall-times.** It should consume §7 with the caveat
   attached: the lane that was contracted to produce devcontainer numbers produced **local,
   contended** ones, so the only genuine devcontainer datapoint is smoke 5 in §8/§11. A router enum
   priced against local Windows numbers would be priced against the wrong substrate.
2. **F3 acceptance act** — one commit (ADR flip + enum edit), queued for the post-sol-review ruling.
   Not performed here: closure rulings are the architect's, not the integrator's.
3. **Lane G's D-1/D-2 debt** returns to lane G (ADR-corpus baselines; 8 over-ceiling rows).
4. **ADR-115 acceptance and the ADR-101 `prompts/` amendment** belong to the separate
   post-integration governance session, per the operator's item-7 instruction. No ADR content was
   authored here.
5. `[#242]`-class items were **not** closed opportunistically — closure rulings are the architect's.

---

## 11. Final suite, and smoke 5 (amendment item 2)

### Final full suite on the merged result — **attribution exact, no bisect needed**

**8 failed, 3964 passed, 4 skipped, 1 xfailed — 1870.1 s (31 m 10 s), 1873 s wall.**
Collected 3977, matching the regenerated `doc-counts`.

The 8 decompose with nothing left over: **the 6 baseline REDs, all still present and unchanged**,
**plus the 2 lane G ADR-corpus REDs** (D-1). **Zero unattributed failures**, so the amendment's
touched-path fallback resolved it and no bisect was required.

### Smoke 5 — **FAILED the REQUIRE. `Ok=False`, `RemoteExitCode` never set.**

The amendment required `Ok=True` **AND** `RemoteExitCode=0`. Neither was reached. Reported as a
failure rather than dressed up, because the failure *is* the D1 evidence.

```
Ok             : False
RemoteExitCode :            (never reached — the run leg never executed)
Name           : smoke-5-audit-check-count-w95qprjxvpjf947
Failure        : cp contract exited 1
SMOKE5_WALL_SECONDS = 73.4      (create 6 s; failed at the copy leg)
```

**Three independent defects, each measured, each fatal on its own.** They are listed separately
for the same reason A4's absences are: any one being fixed still leaves the transport unable to
run a lane.

1. **`gh codespace cp` is broken on this host.** scp receives a destination containing **literal
   single quotes** — `dest open "'/workspaces/dev-knowledge/SMOKE-5-audit-check-count.md'"` →
   *No such file or directory*. **Not a readiness race:** the copy was retried by hand after the
   codespace reached `state=Available` and failed identically, and `/workspaces/dev-knowledge`
   was confirmed present and `drwxrwxrwx`. This is the recorded `gh codespace cp` literal-quote
   defect, and it blocks the transport at its first file-moving step.
2. **`uv` is not installed in the container** — absent from `~/.local/bin`, `/usr/local/bin` and
   PATH. So even with the contract delivered, its `uv run --locked …` command exits 127
   (`uv: command not found`). Every hub gate is `uv run --locked` by ADR-106, so **no hub gate can
   execute on this substrate as provisioned.**
3. **The clone is stale, and silently so.** In-container `HEAD` is **`0360d6d0`** (a 2026-08-22
   commit), not the pushed `6882ef74` — while `git status -sb` reports `## main...origin/main`
   with no divergence, i.e. it never fetched. `/workspaces` is dated 2026-08-22: the machine came
   from a prebuilt image and did not update. **Consequence: lane CS's merge — the very change that
   declares the Claude Code install — is not present, and `claude` is NOT on PATH in the container
   that was supposed to prove it.**

**This is the "flag lost across substrates" family** the RL dispatch brief names: *"a discipline
proven on one transport silently absent on the next, because the assertion looked at the old
artifact."* Here the artifact examined was an image three days stale.

**What smoke 5 therefore establishes for D1 — the opposite of a green tick, and more useful:**
combined with §7 (lane X never ran on the devcontainer either), **this batch contains NO successful
devcontainer execution at all.** The wave-2 router ADR must not price a Codespaces rung as
available until items 1–3 are closed and a dispatch is demonstrated end-to-end.

**Cleanup:** the codespace this smoke created was deleted (`gh codespace delete`, exit 0) — the
no-leftovers rule. **Flagged, not touched:** four codespaces from 2026-08-25 remain in `Shutdown`
(`cs-smoke-audit-check-count`, `cs-smoke-2`, `cs-smoke-3`, `cs-smoke-4`), still consuming storage.
They predate this batch and are the operator's to remove.

---

## 12. Final state

- `main` = **`6882ef74`**, pushed; `origin/main` level. Both pre-push gates passed —
  `block-ff-push` and `block-unanchored-push`.
- **Teardown complete.** All 3 lane worktrees removed, `git worktree prune` run, and 7 branches
  deleted **each after an explicit `git merge-base --is-ancestor <branch> main` proof**:
  the 3 `worktree-*` lanes, `docs/rl-registry-filings-dispatch`,
  **`docs/handoff-2026-08-25-architect`** (discharging the flagged MERGE-IS-ATOMIC deviation), plus
  the integrator's own `docs/batch-1-journal-anchor` and `chore/batch-1-integration-owed`.
  Remotes deleted for the 3 that had them. `automation/fleet-audit` deliberately preserved —
  explicitly protected, and deleting it breaks the replication organ.
- `git worktree list` shows only the primary checkout. No leftovers.
