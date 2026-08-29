# NB2 · WAVE 2 · LANE I — FM-2: `check_funnel_lifecycle`, the reaper's teeth — HAND-BACK PACKET

**Batch:** night-batch-2, wave 2 · **Repo:** `.dev-knowledge` · **Substrate:** local
**Branch:** `worktree-lane-i-2-fm-funnel-lifecycle-check` · **Merge base:** `77096131`
**Contract of record:** `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-2, dispatched as `NB2-W2-LANE-I-FM2-funnel-check.md` (read end-to-end; the LATE ADDENDUM and the STATE-OF-THE-TREE section are both acted on below).
**Posture:** committed and STOPPED. No merge, no push, no JOURNAL entry, no `tasks/` write, no generated-surface regeneration.

---

## 0. THE EX-ANTE LINE, VERBATIM, THEN THE MEASURED RESULT

> **Ex-ante:** RED-first against live main reproducing FM-C's findings (that is the proof of
> teeth), plus a seeded-violation test that FAILs then passes.

**Measured — both halves MET.**

**RED #1, live main, direct invocation** (`uv run --locked python scripts/funnel_lifecycle.py --report`, exit 1):

```
detector           funnel-lifecycle/v1
intakes            55 live / 8 archived
live ADRs          88
rows               343 (7 on/after 2026-08-27)
READY threshold    NOT RULED

a1 terminal intake not archived        2
    docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md
    docs/intake/2026-08-06-func-parallel-execution-system.md
a2 ACCEPTED, all named rows terminal   0
b  terminal ADR not archived           0
c  post-cutoff row provenance          0
d  READY past threshold                0
```

**The overlap, stated explicitly as the contract requires.** FM-C's census
(`docs/audits/2026-08-29-census-nb2-funnel.md` §3.2) listed **N = 3** objects in the class
"requires a status ruling first": intake **#19**, **#26**, **#28**. The check FAILs on
**M = 2** of them. **N − M = 1, and the difference is #28**, which the 2026-08-29 wave-2 GO
**HELD at ACCEPTED per ADR-112** rather than ruling terminal — so it is correctly invisible to
leg a1 (not terminal) and correctly invisible to leg a2 (its `consumed-by:` names no row).
Seeing fewer than 2 would mean no teeth; seeing #28 would mean enforcing a ruling that was
deliberately not made. Two instruments, one reality.

**Re-measured, not reused.** FM-C measured *"docs at a TERMINAL status still sitting at depth 1:
**0**"* on revision `fcc94855`. On the merged tree it is **2**, because the GO flipped #19
(SEED → CONSUMED) and #26 (ACCEPTED → CONSUMED). Live statuses re-derived here:
**SEED 9 · DRAFT 7 · READY 19 · ACCEPTED 18 · CONSUMED 2 = 55** (the STATE-OF-THE-TREE section's
`SEED 10 · ACCEPTED 19` predates the two flips and reconciles exactly).

**RED #2, seeded.** Leg a1 was deliberately neutered in `scripts/funnel_lifecycle.py`
(`if doc.status in TERMINAL_INTAKE_STATUSES:` → `if False:`) and the suite was re-run:
**5 tests went RED** — the three `test_a1_flags_every_terminal_status_at_depth_1[...]`
parametrisations, `test_a1_is_right_either_way_when_the_doc_is_relocated`, and
`test_one_finding_per_violation_never_a_bundle`. The neutering was reverted and the file
restored byte-for-byte before commit 1. Final: **64 passed**.

That first RED also exposed a defect in the RED itself, recorded rather than smoothed: the live
overlap test carried a `pytest.skip` branch for the case where lane J has already relocated the
docs — and it therefore SKIPPED under the neutered detector too. A skip that is
indistinguishable from a blind detector is the green-by-skip class the 2026-08-25 sweep closed.
It was rewritten to the invariant that holds on both sides of the relocation: each ruled doc is
**either flagged by leg a1 or present in the archive, and not neither**.

---

## 1. PER-DONE-ITEM VERDICTS

### FAIL-class legs

| Leg | Contract text | Verdict | Witness |
|---|---|---|---|
| **a1** | intake at a terminal status, not archived → FAIL | **MET** | 2 live subjects; `test_a1_flags_every_terminal_status_at_depth_1` × 3 statuses + refusal twin over SEED/DRAFT/READY/ACCEPTED |
| **a2** | intake ACCEPTED, all rows terminal, not archived → FAIL | **MET (armed, near-inert — see F3)** | measures **0 of 18** ACCEPTED docs live; `test_a2_flags_accepted_whose_named_rows_are_all_terminal` + three refusal twins (one open row, vacuous empty set, unknown row) |
| **b** | ADR superseded/rejected, not archived → FAIL | **MET** | measures **0** — armed against a corpus at zero, the `check_adr_status_grammar` / `consumer_at_landing` bar. Bound to `validate_adr_status.TERMINAL_STATUSES`, the ruled constant, not a local copy |
| **c** | post-cutoff row whose source does not resolve → FAIL | **MET, via the addendum's substitute** | measures **0** of 7 post-cutoff rows; 10 tests incl. grandfathering, undated-in-scope, namespace ambiguity, repo containment |
| **d** | intake READY beyond FM-1's N days, no ruling → WARN | **NOT-MET — FM-1 did not land** | see §2 |

**Leg (b) — one honest correction to the contract's wording.** It says *"superseded/rejected"*.
The live ADR status enum (`validate_adr_status.STATUS_ENUM`) has no `Rejected`; the ruled terminal
set is `TERMINAL_STATUSES = {Superseded, Deprecated}`. The leg binds to that constant rather than
to the contract's prose, so it cannot drift from the enum, and
`test_b_binds_to_the_ruled_constant_not_a_local_copy` pins it.

**Leg (c) — the LATE ADDENDUM discharged, and re-derived on the merged tree.**

```
tasks/*.md rows carrying a `source:` frontmatter key   0 of 343     (census P1 reproduced)
OPEN rows carrying a `· refs …` provenance clause    151 of 151     (100 %)
```

FM-C measured **153 / 153**; the merged tree is **151 / 151** because `[#577]` and `[#584]` closed.
The substitute holds, so leg (c) reads `· refs …` and says so in the module docstring. **No
`source:` field was added to any row** — that is a schema change to the backlog source of truth,
lane D is the batch's `tasks/` writer, and it is filed as a candidate (F1) instead.

### Cross-cutting requirements

| Requirement | Verdict | Witness |
|---|---|---|
| **Z-G4: cannot-compute → FAIL, never skip** | **MET** | nine enumerated raise conditions, each with its own test; `test_zg4_no_leg_returns_a_skip_or_an_unavailable_status` pins that every verdict is pass/warn/fail; the adapter renders `LifecycleUnreadable` as `fail`, deliberately not `unavailable` |
| **Exit codes follow the sibling gates** | **MET** | CLI: 0 clean / 1 violation / 2 internal error. Adapter: an internal error is a `fail` Finding — it BLOCKS (`test_adapter_blocks_on_an_unexpected_internal_error`) |
| **Extend, never rival** | **MET** | §3 |
| **Registration, and state which you did** | **MET** | §4 |
| **RED-first, twice** | **MET** | §0 |
| **Terra pre-merge, tally-in-body** | **PARTIAL** | §5 — pass 1 complete and all 13 findings fixed; pass 2 unreachable, error recorded |
| **Ratchet measured before first and last commit** | **MET** | §6 |
| **A1 — name the telemetry store** | **MET** | `logs/TELEMETRY.db` (`scripts/telemetry_emit.py:167`, `DEFAULT_DB_RELPATH`, overridable via `$DEV_KNOWLEDGE_TELEMETRY_DB`). **No second store was created and nothing was written to this one** — the check emits per-run evidence strings like every sibling, which is the existing pattern; `funnel_coverage` and `consumer_at_landing` write no telemetry either |
| **The four things this lane does not do** | **MET** | no JOURNAL entry (the Stop hook is declined explicitly, with the reason: the integrator writes one anchor for the whole queue, ADR-85 amendment 2026-08-03 §A5 made that hook advisory in full and a lane does not push); no self-merge and none suggested; no row closures and no `tasks/` write; no generated-surface regeneration — see D4 |

---

## 2. FM-1's THRESHOLD — READ FROM THE TREE, AND IT IS NOT THERE

The contract: *"FM-1 (lane H) rules the READY threshold as a number and lands it in `protocols/`.
It merges before you. Find it, quote it, and cite the file:line."*

**It did not merge before me, and the number does not exist in the tree.** Evidence, at boot and
re-checked at hand-back:

```
$ git log --oneline -1 main
77096131 Merge branch 'docs/batch-2-w2-preflight' -- the wave-2 GO's carried acts …
$ git branch -a | grep lane-h
  worktree-lane-h-1-fm-lifecycle-doctrine        # tip == 77096131, i.e. no commits yet
$ grep -rniE "READY.{0,40}(day|threshold)|threshold.{0,40}READY" protocols/
  (no match)
```

The nearest live doctrine is **prose, not a number**: `docs/intake/README.md` §7 —
*"intake docs sitting unconsumed after **~1 month of operation** trigger a review of the scene for
removal (ADR-98 §6)"* — and `protocols/STANDING_RULINGS.md` I-D7 applied it once, at an ad-hoc
**31 days**. A gate cannot act on "~1 month".

**Leg (d) is therefore NOT-MET, with the reason, and the other three legs ship** — exactly the
branch the contract prescribes. What the lane did instead of inventing a constant:

* the leg is **built and armed-on-arrival**. `funnel_lifecycle.ready_threshold()` scans
  `protocols/*.md` for a declared constant and `_READY_THRESHOLD_RE` is documented with the shape
  it binds: `READY threshold: <N> days` (case-insensitive; an optional list marker, optional `**`
  emphasis, `intake READY threshold` / `READY-age threshold`, and `=` for `:` all accepted).
  `test_d_arms_the_moment_a_threshold_is_ruled` proves the same tree and the same document start
  discriminating the moment the constant appears.
* absent, it emits **one WARN naming the absence and the 19 READY intakes it did not examine** —
  a reported gap, which is what Z-G4 requires of a skip. It does **not** FAIL: Z-G4 governs a
  check that cannot compute the ground truth *of a rule that exists*, and arming a hard refusal
  against a threshold nobody ruled is the invented-constant drift this batch exists to stop.
* the shape reconciliation is filed as candidate **F5** for the integrator.

---

## 3. WHAT THE THREE EXISTING ORGANS ALREADY DO, AND WHAT THIS ADDS

All three were opened before a line was written.

| Organ | Corpus | Unit | Question it answers |
|---|---|---|---|
| `funnel_coverage` (M3) | `docs/audits/` (non-recursive) | artifact | was this audit **DISPOSITIONED** — ACTIONED / FILED / REJECTED / SUPERSEDED? |
| `consumer_at_landing` (`[#595]`) | `docs/audits/` (recursive) | artifact | is this landed artifact **CITED** by a governance surface, and has the unconsumed set grown? Its POOL includes `docs/intake/` and `tasks/` as **citers** |
| `intake_tree_coherence` (`[#383]`) | `docs/intake/` residue carrier | the derived artifact | does `manifest.json` + the generated index **REGENERATE byte-identically**? |

**What `funnel_lifecycle` adds:** none of the three reads a governed object's **STATUS** and asks
whether its **LOCATION** and its **provenance** still agree with that status. `funnel_coverage`
and `consumer_at_landing` never touch `docs/intake/`, `docs/decisions/` or `tasks/` as subjects at
all. `intake_tree_coherence` is regen-and-diff and is blind to what the frontmatter *says* — the
census D1 finding measured it reproducing a **wrong** index byte-for-byte and staying green
through six broken docs.

**Resolvers are borrowed, not rewritten** — the contract's "two answers to *is this intake
consumed?* is the failure mode" clause, honoured mechanically:

| Borrowed from | Used for |
|---|---|
| `gen_intake_index._parse_frontmatter` | intake frontmatter (and a `{}` parse is a Z-G4 FAIL, per the STATE-OF-THE-TREE instruction) |
| `gen_intake_index._STATUS_ORDER` | the ruled intake status enum |
| `validate_adr_status.scan_zone` + `TERMINAL_STATUSES` | ADR status and the ruled terminal set |
| `gen_task_tree.frontmatter_id` / `frontmatter_status` / `extract_body` / `_ORPHAN_RE` / `_TERMINAL_STATUSES` | rows, from `tasks/` — the source of truth. `BACKLOG.md` is a one-line VIEW and was not read |
| `consumer_at_landing.ARM_DATE` | leg (c)'s cutoff — one constant, `test_c_cutoff_is_the_consumer_at_landing_constant` pins the identity |

---

## 4. REGISTRATION — WHICH OF THE TWO OPTIONS, STATED

The contract offered: land unregistered, *or* register at a tier the commit gate does not run,
prove the RED by direct invocation, then register at the gate in a second commit **only if the
tree is clean by then**.

**Taken: both commits, and the second registers at SHIP tier, not at the commit gate.**

* **Commit 1 (`09aaf695`)** — detector + tests, **not registered**. The RED was proven by direct
  invocation of the module CLI.
* **Commit 2 (`9a77a6b9`)** — facade + `ALL_CHECKS` + `CHECK_ORDER` at `_tier(TIER_SHIP, …)`.

**Why not the commit gate: the tree is not clean, and this lane cannot clean it.** Leg a1 FAILs on
live main by design — that is the deliverable. Clearing it means **relocating** intake #19 and #26
into `docs/intake/archive/`, which is lane J's act in this same wave and outside this write-scope.
A `TIER_COMMIT` registration would have wedged every commit in every lane on a defect the
committing session may not legally repair.

**Measured, not assumed** — `uv run --locked python scripts/audit.py health`, exit **0**,
`health: OK`:

```
[--] funnel_lifecycle: [n/a-reason:NOT-APPLICABLE] declared ship-tier -- not run at the commit
     gate ([#597] per-check tiering; ship-gate and `audit run` run it)
```

`cmd_health` invokes `run_checks(tier=TIER_COMMIT)`; `runs_at_tier` is a nested-subset test, so
ship runs commit too. Both directions pinned by
`test_adapter_does_not_run_at_the_commit_gate_but_does_at_ship`.

**The tier is a DECLARED exception, the third one.** `ALL_CHECKS`'s assignment rule reserves
`TIER_SHIP` for checks that cannot emit `fail`. `fleet_parity` and `routing_agreement` are the two
standing exceptions; this is the third, and it borrows `routing_agreement`'s exact argument. The
**promotion condition is written into the registry comment rather than remembered**: flip to
`TIER_COMMIT` when leg a1 measures 0 on `main` (candidate F6).

**⚠ THE INTEGRATOR MUST EXPECT A SHIP-GATE RED.** `cmd_ship_gate` blocks on `fail`. After this
lane merges, the ship-gate will report **2 `funnel_lifecycle` FAILs** until intake #19 and #26 are
relocated. That is the gate working, not a defect — but it is a wedge if it arrives unannounced,
so it is announced here. If lane J merges first, the FAILs are gone before the gate ever sees them.

**The six count pins**, 53 → 54, moved together in commit 2:

| # | Site | Moved |
|---|---|---|
| 1–2 | `tests/test_audit.py` (×2) | ✅ |
| 3–4 | `tests/test_doc_code_edge.py` (×2) | ✅ |
| 5 | `tests/test_writer_integrity.py` | ✅ |
| 6 | `ecosystem/doc-counts.md:14` | ❌ **owed to the integrator** — see D4 |

`tests/test_audit_parallel.py::…` asserts `tuple(c.__name__ for c in ALL_CHECKS) == CHECK_ORDER`
and `tests/test_audit.py` asserts `len(CHECK_ORDER) == len(ALL_CHECKS)`; both pass. The
`gen_handoff` stub-shadows-`audit` trap named in the contract did not bite — the adapter tests read
`CHECK_ORDER` from `audit_checks.registry`, never `ALL_CHECKS` through a stub.

---

## 5. TERRA — TALLY IN BODY

**Pass 1** — `codex exec --skip-git-repo-check -c model_reasoning_effort=high`, scoped to this
lane's diff only (**not** `/codex-review`, per the contract).

```
TALLY: critical=0 high=13 medium=0 low=0     — all 13 ACCEPTED and FIXED
```

Seven of the thirteen were **vacuous-pass paths that looked like ordinary defensive coding**:

| # | Defect | Fix |
|---|---|---|
| 1 | leg a2's loose `\[?#(\d+)\]?` also matched the `#28` inside `intake #28` — one namespace judged as the other | bracketed-only `_BRACKETED_ROW_RE` |
| 2 | `--diff-filter=A` **drops renames**, and `gen_task_tree` renames a row whenever its title changes — one live row (`tasks/440-*.md`) read as undated | rename-aware replay |
| 3 | the stem universe skipped `docs/{intake,decisions}/archive/` — a row citing an archived object falsely FAILed | archive dirs added |
| 4 | "oldest add wins" grandfathered a delete-then-re-add | oldest-first replay; newest add wins |
| 5 | `errors="replace"` turned `CONSUM\xffED` into a passing non-terminal string | strict UTF-8 decode → raise |
| 6 | intake with no `status:`, or an off-enum one, matched no leg and vanished silently | raise |
| 7 | a row with an unparseable `id:` left leg (c)'s **denominator** as well as its numerator | raise |
| 8 | `scan_zone`'s `missing`/`extra` discarded — an absent status read as a clean one | raise |
| 9 | an absent `docs/intake/` / `docs/decisions/` / `tasks/` read as an empty set | raise (`_require_dir`) |
| 10 | a READY doc with an undated filename silently excluded from leg (d) | NAMED at WARN |
| 11 | `· refs ../outside.md` resolved against a sibling checkout on the operator's disk | repo containment |
| 12 | `_REFS_RE` with `re.S` ran past its own line and swallowed later prose — silent false coverage | single-line regex |
| 13 | the inert-leg test compared the status tuple to one arbitrary pair and would have passed on a `fail` | assert the exact list |

Each fix carries its own regression test naming its finding number. Post-fix the live post-cutoff
row count corrected **8 → 7** (finding 2's witness).

**The fixes exposed a fourteenth defect the reviewer could not see.** `Path.write_text` launders
LF → CRLF on Windows; `gen_task_tree._FM_ID_RE` is `^id: "\[#N\]"$` under `re.MULTILINE`, so **every
synthetic row in the test file had an unparseable id**. Under the pre-fix code that was a silent
`continue` — so every row-shaped test was scoring an **empty row set** and passing green. The new
Z-G4 raise made it visible; the fixtures now write bytes. A second instance of the same class was
then found by re-reading assertions rather than results: `test_zg4_unreadable_file_raises` patched
`Path.read_text`, which `_read` stopped using when it went strict, so it was catching
`scan_zone`'s raise three legs away. Both are recorded in the test file at the site.

**Pass 2 — UNREACHABLE.** One recorded line, per the contract:

```
ERROR: You've hit your usage limit. Upgrade to Pro … or try again at 4:20 PM.
```

Owed as candidate **F8**.

---

## 6. BUDGET DECISIONS

**Ratchet — measured twice, as instructed, and the gate caught one violation.**

| When | detector | files | count |
|---|---|---|---|
| before commit 1 | silent-rule-v5 | 61 | **443** |
| before commit 2, first attempt | silent-rule-v5 | 61 | **444 — REFUSED** |
| before commit 2, after repair | silent-rule-v5 | 61 | **443** |

The wave-1 dispatch figure was **443 / 61 files, zero headroom**; measured, not assumed, and it had
not moved. `ecosystem/*.yaml` is inside `silent_rule_detector`'s scope
(`_SCOPE_RULES`), the first draft of the `doc-code-edge.yaml` exempt row contained one modal verb,
`silent_rule_ratchet` reported `444 > 443` and **`audit-health` refused the commit**. Repaired by
rewriting the row **token-free** — the CLAUDE.md v2.68 precedent — rather than by requesting
headroom against a baseline that has none. Final delta **0**. `protocols/` and `templates/` are
untouched by this lane.

**Tier decision.** SHIP over COMMIT — argued at §4, with a written promotion condition rather than
a remembered one.

**Scope decisions declined.** Three things this lane could have done and did not:
adding a `source:` field to 343 rows (F1); repairing the `intake-index-freshness`
correctness gap (F2); relocating intake #19 / #26 to make its own gate green (lane J's act, and a
check that clears its own subject is not a check).

---

## 7. CANDIDATE FILINGS — reported, not filed

| # | Candidate | Why it is a decision, not work |
|---|---|---|
| **F1** | *Either the funnel doctrine names `refs` as the provenance clause, or `tasks/` grows a `source:` field — one act, ruled once.* | The contract's own words. 0 of 343 rows carry `source:`; 151/151 open rows carry `· refs …`. A schema change to the backlog source of truth is a ruling; lane D is the batch's `tasks/` writer |
| **F2** | `intake-index-freshness` is regen-and-diff, so it reproduced a wrong index byte-for-byte and stayed green through six broken docs (census D1). A freshness gate cannot detect a generator bug. | Named by the contract as "a candidate filing, not your work". `funnel_lifecycle` treats a `{}` parse as FAIL, which catches the *consequence* — it does not repair the *generator* |
| **F3** | `consumed-by:` is not in the ADR-98 companion-field schema (`docs/intake/README.md` §3), and **0 of 18** live ACCEPTED intakes carry it with a `[#id]` row token. Leg a2 is armed and near-inert. | Either the schema admits `consumed-by:` as the intake→row link, or a2 needs a different one. A check cannot rule its own join key |
| **F4** | **A1 gap:** intake docs carry **explicit state but no dated transitions**, so leg (d) measures document age from the filename, not time-at-READY. A doc that reached READY yesterday after two months at DRAFT is aged from its birth. | A1 says "every governed object carries explicit state + dated transitions". Half of that is not true of `docs/intake/` today. It is a schema act, not a check act |
| **F5** | Reconcile FM-1's landed threshold shape with `funnel_lifecycle._READY_THRESHOLD_RE`. | The binder expects `READY threshold: <N> days` under `protocols/`. If lane H lands a different shape the leg stays inert **and says so** — but one of the two has to move, and neither lane can see the other |
| **F6** | Promote `funnel_lifecycle` `TIER_SHIP → TIER_COMMIT` once leg a1 measures 0 on `main`. | One line. Written into the registry comment so it is not remembered; still needs someone to notice the condition is met |
| **F7** | **4 rows carry provenance that resolves to nothing** (whole-corpus, all pre-cutoff and therefore grandfathered): `[#518]` (`N4-F1/F6/F5/F12`), `[#123]` (`#85, #14, #113, audit C matrix R7`), `[#35]` (`coherence-audit`), `[#71]` (`G6 process-hardening sweep`). FM-C found **1** of these; the difference is that this resolver deliberately does **not** try a bare `#N` against the intake namespace. | Real provenance debt on live rows. The stricter resolver is a deliberate choice (a FAIL-armed leg may not resolve a token two ways until one works) — but that choice is worth ratifying rather than leaving as an implementation detail |
| **F8** | Terra pass 2 owed on this diff. | Provider quota, not a finding |
| **F9** | `scripts/audit.py run` is the **fleet routine** — it registers repos, writes `ecosystem/*/history/`, and commits **and pushes** to `automation/fleet-audit`. Nothing in its `--help` says so, and its name reads like the read-only per-repo runner. | See D2. A naming/doc hazard that cost this lane one unintended pushed commit |

---

## 8. DEVIATIONS, WITH OWNERS

**D1 — one write outside the literal write-scope: `ecosystem/doc-code-edge.yaml`, one appended
line.** The contract's write-scope is *"new check module + registration (audit.py) + tests"*.
This write is **structural, not a choice**: `check_doc_code_coverage_drift` is FAIL-class and names
any `ALL_CHECKS` member that is neither `# rule:`-annotated nor `exempt:`-listed, so the check
**cannot enter the registry at all** without it. Precedent: the `supplement_folded` row states this
exact reason for itself, including "appended at the end of the list to conflict cleanly", which
this row does too. *Owner: integrator, to accept or bounce.*

**D2 — an unintended fleet-audit commit, pushed.** I ran `uv run --locked python scripts/audit.py
run --repo-path .` to see the ship-tier verdict. It is the **fleet routine**, not a read-only
runner: it registered this worktree as a 7th repo, wrote `ecosystem/*/history/2026-08-29.md`, and
committed **and pushed** `35050915 chore(routine/fleet-audit): record 2026-08-29 baseline` to
`origin/automation/fleet-audit`. Four other baselines already exist for 2026-08-29 from other
sessions, so the artifact is the routine's normal daily shape rather than an anomaly, and
`check_fleet_audit_replication` reads **0 commits ahead of origin**. **Not reverted**, deliberately:
`automation/*` is an explicitly protected branch that lives outside `main` by design, and undoing
this would need a force-push to a shared protected branch — worse than the artifact. The
**leftover** it created in the working tree (`ecosystem/lane-i-2-fm-funnel-lifecycle-check/`, a
gitignored `state.yaml` plus an empty `history/`) **was removed and the removal verified**; the
tree is identical to its pre-run state. *Owner: reported to the operator; no action proposed.*

**D3 — leg (d) NOT-MET.** FM-1 (lane H) had not merged and its constant is absent from the tree.
Full evidence at §2. *Owner: lane H / the integrator, via F5.*

**D4 — the sixth count pin (`ecosystem/doc-counts.md:14`, "53 registered checks") is stale.**
Deliberate: it is a **generated** surface the contract reserves for the integrator ("no
generated-surface regeneration … the integrator does it ONCE on the merged result"), and
`check_doc_claims` — which reconciles it — is itself SHIP-tier, so a stale value blocks no commit.
**Owed:** `uv run --locked python scripts/gen_doc_counts.py --write`. *Owner: integrator.*

**D5 — terra pass 2 unreachable.** Recorded verbatim at §5. *Owner: F8.*

**D6 — the full suite was not run**, per the contract's targeted-only cadence. Targeted set, all
green: `tests/test_funnel_lifecycle.py` (**64 passed**) and the four files coupled to the pins —
`test_audit.py`, `test_doc_code_edge.py`, `test_writer_integrity.py`, `test_audit_parallel.py`
(**385 passed** in that set, 4 min 59 s). `uv run --locked ruff check scripts/ tests/` clean.
Neither of the two inherited REDs the contract names (the anchor-gate probe test; a worktree's
`test_stale_worktrees`) is in the targeted set, so neither was encountered. *Owner: integrator, at
the single full-suite run.*

---

## 9. COMMIT SHAs, IN ORDER

| # | SHA | Subject |
|---|---|---|
| 1 | `09aaf695` | `feat(scripts): FM-2 funnel-lifecycle detector — the reaper's teeth, landed UNREGISTERED` |
| 2 | `9a77a6b9` | `feat(audit): register funnel_lifecycle at SHIP tier + the six ALL_CHECKS count pins` |
| 3 | *(this packet)* | `docs(audits): NB2 lane I hand-back packet — FM-2 funnel lifecycle` |

**Branch:** `worktree-lane-i-2-fm-funnel-lifecycle-check`, off `77096131`. Not merged, not pushed.
**Gate state at hand-back:** `audit.py health` → **OK, exit 0**; pre-commit passed on both commits
(no `--no-verify`, no `SKIP=`); `ruff` clean; silent-rule ratchet **443, delta 0**.

**STOP.**
