# NIGHT N5 — CODIFICATION + DECISION-MEMO PACK

<!-- scope: meta -->

**Lane:** night N5 (claude cloud channel) · **Branch:** `claude/night-n5-codification-memos-eyef8r`
**Contract of record:** `docs/audits/2026-08-19-technical-n5-codification-pack-contract.md` (commit `17b0a85`)
**Mode:** read-only + drafts. **Nothing in this file is a ruling.** Every memo RECOMMENDS; the
operator/architect rules. No PLAYBOOK edit, no script edit, no roster row, no BACKLOG/`tasks/`
write, no merge.

**Verdict line — 5 items:**

```
1  dispatch-runbook codification + PLAYBOOK Ch8 section draft      CLEAR
2  parallel-default decision memo ([#533])                          CLEAR
3  D8 decision memo (.devcontainer fleet_parity WARN)               CLEAR
4  review-artifact linkage gap + draft row text                     CLEAR
5  session-lessons sweep (<=10 candidates)                          CLEAR (one provenance caveat, S5.0)
```

---

## 0 · Method, and the two environment limits this lane had to work around

**Sources read end-to-end**, not skimmed:

| source | what was taken from it |
|---|---|
| `docs/audits/2026-08-18-technical-batch1-integrator-packet.md` (348 lines, incl. the amendment) | S2 grammar evidence, S5 closure acts, S7 deviations, A2 the D8 decision, A3 the 1.41x measurement + WARN delta table |
| `docs/audits/2026-08-18-codex-review-batch1-c-e.md` (lane H's artifact) | S0.3 — H *predicted* the linkage gap of item 4 before it fired |
| `docs/audits/2026-08-18-codex-review-batch1-a.md` | the second, different linkage failure mode (item 4) |
| `docs/audits/2026-08-18-technical-533-leg2-measurements.md` (306 lines) | STEP-1 attribution, STEP-3 fork re-evaluation, STEP-6 medians + parity digests |
| `docs/audits/2026-08-18-technical-phase0-baselines.md` (268 lines) | T0.1 the 290.9 s quiet-tree baseline, T0.2 the mutation pilot |
| BACKLOG rows `[#539]` `[#540]` `[#514]` `[#533]` `[#531]` `[#530]` | scope of each row, and what is already owned elsewhere |
| `scripts/audit.py` `check_review_artifact_coverage` + its regexes; `scripts/audit.py` `run_checks`; `ecosystem/disposition-register.yaml` header; `ecosystem/parity-surfaces.yaml`; `.methodology.yaml`; `protocols/PLAYBOOK.md` Ch8 | read directly rather than quoted from a summary |

**Limit 1 — the container's clone was SHALLOW and its `main` was four days stale.** `.git/shallow`
was present, `git rev-list --count main` returned **48**, and local `main` pointed at `7bbb0674`
(2026-08-14) while the branch this lane sits on descends from `87dd41af` (2026-08-18). Measuring
item 4 against that ref would have reported **1 code-impact merge scanned, 0 unlinked** — a
green answer produced by a truncated history. Repaired with `git fetch --unshallow origin main`
(read-only; 5291 commits) and every measurement below walks `origin/main` @ `87dd41af`. **This is
recorded because the un-repaired reading would have been wrong in the direction of "no problem",
which is the dangerous direction.**

**Limit 2 — `audit.py` cannot be imported in this container** (`ModuleNotFoundError: click`; the
pinned `uv` is 0.11.19 and the container ships 0.8.17, so `uv run --locked` refuses). Item 4's
measurement therefore comes from a **faithful stdlib re-implementation** of
`check_review_artifact_coverage` written from the live source — same four regexes verbatim, same
`_REVIEW_CUTOFF_EPOCH`, same `_REVIEW_CODE_SUFFIXES`/`_REVIEW_CODE_EXACT`, same first-parent walk,
same `introduced()` set, same first-match-wins linkage loop. It lives in the session scratchpad and
is **not committed** (no script may be born by this lane). Reproduction command for a seat that has
the real environment:

```
uv run --locked python -c "import sys;sys.path.insert(0,'scripts');from pathlib import Path;import audit;[print(f.status.upper(),'|',f.message) for f in audit.check_review_artifact_coverage(Path('.'))]"
```

**Limit 3, stated for the STOP packet — the pre-commit gates did not run on this branch.**
`.git/hooks/pre-commit` is absent in this container (fresh clone, `pre-commit install` never run,
and `arm_hooks.py` is a `SessionStart` hook of the local harness, not of a cloud session). The
dispatch-stamp commit `17b0a85` therefore passed **without** `audit-health`, `validate-hermetization`,
`ruff`, `audit-index-freshness` or either commit-msg gate firing. No gate was bypassed — none was
armed. Both filenames were nonetheless checked by hand against `validate_hermetization`'s live
`AUDIT_CLASS_ENUM` / `_SLUG_RE` / `_DATE_SHAPE` (class `technical`, all-lowercase kebab, `YYYY-MM-DD-`
prefix: admitted on all three legs), and the generated audits index was regenerated with
`gen_audit_index.py --write` rather than left stale. **An integrator merging this branch should
expect the gates to run for the first time at that merge.**

---

# ITEM 1 — DISPATCH-RUNBOOK CODIFICATION + PLAYBOOK Ch8 SECTION DRAFT · **CLEAR**

## 1.1 · Three of the six lessons are ALREADY doctrine — codifying them again is the failure mode

The dispatch names six things to encode. Checked against the live tree **before** drafting, because
CLAUDE.md §5 rule 6 and §10 both name duplication as the drift mechanism here:

| lesson the dispatch names | already in the tree? | where |
|---|---|---|
| `--worktree <slug>` prefixes `worktree-` exactly once (doubled-prefix) | **YES, in full** | `protocols/PLAYBOOK.md:2095-2106`, Ch8 "The dispatch surface is `dispatch <file>`" — batch-6 witness, all twelve lanes, `batch_manifest.is_lane_merge` matched 0 of 12 |
| contract-as-first-commit (ADR-110) | **YES, as a documented path** | `protocols/PLAYBOOK.md:2045-2086`, Ch8 "Dispatch prompts and the contract of record" — and it states its own honest limit: *"This is a documented path, not a mechanism: nothing checks that a manifest's lane rows resolve to committed contracts"* |
| grammar check at PROVISIONING | **PARTIALLY** — `/lane-boot` step 1 calls `validate_branch_naming.py` (`.claude/commands/lane-boot.md:25`), and `KIND_UNKNOWN` exists (`scripts/validate_branch_naming.py:96`), but nothing enforces it. `[#514]` leg 1 + `[#531]` both own the unbuilt gate | rows `[#514]`, `[#531]` |
| one-block batch dispatch + branch-existence wait (config.lock race) | **NO — zero occurrences** | searched `protocols/PLAYBOOK.md`, `.claude/commands/lane-boot.md`, `.claude/commands/lane-integrate.md`: the only lock precedent in-tree is `.git/index.lock` (JOURNAL 4515, 11519), a **different** lock |
| board status != completion (false-DONE) | **NO** | `/lane-integrate` §1 builds the queue and never says how a lane is known finished |
| harvest from git, never transcripts | **PARTIALLY** — Ch8 already says transcripts *"are repo artifacts in no sense at all"* (`:2058`); the positive `git show <branch>:<path>` shape exists only inside row `[#540]` | `protocols/PLAYBOOK.md:2058`, row `[#540]` |

**So the draft's real payload is three items, not six**, and the other three enter it as one-line
cross-references. A Ch8 section that restates the doubled-prefix witness would put the same
measured fact in two places in one chapter, which is the divergence mechanism §5 rule 6 names.

## 1.2 · Provenance ledger — what each drafted claim rests on

This matters because every load-bearing paragraph in Ch8 today carries its evidence, and a
codification commit that quietly drops that convention weakens the chapter it joins.

```
claim                                    provenance                                    status
---------------------------------------------------------------------------------------------
doubled-prefix defect class              batch-6, twelve lanes, PLAYBOOK:2095-2106      IN-TREE
contract-as-first-commit                 ADR-110 + PLAYBOOK:2045-2086                   IN-TREE
grammar at provisioning / KIND_UNKNOWN   packet S2: 2 of 8 lanes off-grammar            IN-TREE
harvest by `git show`, never `claude logs`  row [#540], recommended twice               IN-TREE
one-block dispatch + branch-existence wait  DISPATCH STATEMENT ONLY                     UNCITED
board status != completion (false-DONE)     DISPATCH STATEMENT ONLY                     UNCITED
```

**The two UNCITED rows are drafted exactly as the dispatch states them** — that is what
codification of a measured lesson means, and the operator witnessed them today. But they are the
only two claims in the draft with no artifact behind them, and the seat that lands this section
should either (a) name the session artifact that records them, or (b) accept them on the operator's
own witness and say so in the commit body. **Flagged, not smoothed over** — a Ch8 paragraph that
cites nothing reads, six weeks later, exactly like one whose citation was lost.

## 1.3 · DRAFT A — PLAYBOOK Ch8 section, paste-ready

Insertion point: `protocols/PLAYBOOK.md`, Ch8, **between** "The dispatch surface is `dispatch <file>`
— the contract file is the source ([#509] v2)" and "Model + effort are stated at dispatch — the
routing matrix". That places it after the surface that produces a dispatch line and before the
routing that parameterises one, which is the order a batch actually runs in.

Paste-ready (outer fence is 4 backticks so the inner blocks survive the copy):

````
### Dispatching a BATCH — one block, then wait for the refs ([#539]/[#540])
<!-- scope: meta -->

The sections above cover ONE dispatch line. A batch dispatches N of them within seconds of each
other, and three failure classes belong to that plural case alone. None is a flag error; each is a
property of dispatching concurrently, so none of the single-dispatch discipline above catches them.

**1 — Dispatch the whole batch in ONE block, then WAIT for every branch to exist before doing
anything else.** Concurrent `claude --bg --worktree` provisionings contend on the CLI's own
config lock, and a lane that loses the race can return an apparently-successful dispatch while its
branch is never created. The wait is not politeness, it is the acceptance test for the dispatch
step: the batch is dispatched when N branches exist, not when N commands have returned.

```
# after the dispatch block, before ANY other act:
for slug in <lane-slugs>; do
  git show-ref --verify --quiet "refs/heads/worktree-$slug" \
    && echo "OK   worktree-$slug" \
    || echo "MISSING worktree-$slug   <- re-dispatch this lane, do not proceed"
done
```

A MISSING row is re-dispatched individually. It is never assumed to be a slow start, because the
two states — still provisioning, and silently lost — are indistinguishable from the board.

**2 — A board state of `done` is a statement about the SESSION, not about the WORK.** Agent View
reports that a session stopped. It cannot report whether the lane committed, whether its packet
exists, or whether its contract was satisfied — a session that stops early, stops on an error, or
stops after writing nothing at all reports `done` exactly like one that finished its contract.
Treating the board as a completion signal produces a false-DONE: the integrator opens a merge queue
against a lane that has nothing to merge.

The board tells you when to LOOK. The tree tells you what HAPPENED. Concretely, a lane is finished
when its own artifacts say so:

```
git show <branch>:<packet-path>          # the packet exists and is readable
git log --oneline main..<branch>         # commits exist, and the FIRST is the contract stamp
```

**3 — Harvest from git, never from transcripts.** Fetch every lane's packet with
`git show <branch>:<path>`. Do not parse `claude logs`: it is ANSI screen replay, not data, and a
harvest built on it expires with the transcript and is unavailable to any later seat. This is the
same property the contract-of-record section above establishes for lane contracts, applied to the
return leg — a batch is reconstructable from repo artifacts in both directions or in neither.

**4 — Grammar is checked at PROVISIONING, not at the merge queue.** `/lane-boot` step 1 runs
`validate_branch_naming.py`, but a lane dispatched straight through `claude --worktree` never
reaches `/lane-boot`, so the check is skipped by exactly the path a batch uses. Batch 1 measured
the cost: **2 of 8 lanes reached the integrator off-grammar** (`worktree-lane-f-p10-evidence` and
`worktree-lane-g-a9-trim` — `p10` and `a9` are not `\d+`), and the grammar held only because a
human ran it by hand at integration. Until `[#514]` leg 1 / `[#531]` land the `KIND_UNKNOWN` block
at the one point every provisioning path crosses, **the pre-dispatch grammar check runs against the
names git will actually create** — never against the intended ones, which is the reading that let
the batch-6 doubled prefix through:

```
uv run --locked python scripts/validate_branch_naming.py --lane lane-<letter>-<id>-<slug>
```

**Note the argument shape, because it is the batch-6 defect in miniature:** `--worktree` and this
validator both take the **bare** lane name; the provisioner adds `worktree-` exactly once. Passing
the branch name to either produces the doubled prefix the dispatch-surface section above records.
````

## 1.4 · DRAFT B — the operator dispatch runbook, paste-ready

This is the point-of-use card — the sequence an operator runs. Ch8 carries the doctrine and the
evidence; this carries the order of acts. It is written so `[#539]`/`[#540]` can absorb steps 1, 3
and 5 mechanically without the card changing shape.

````
# BATCH DISPATCH RUNBOOK

## 0 — before any dispatch
- [ ] The batch manifest is COMMITTED, and each lane row points at a COMMITTED contract file
      (ADR-110; PLAYBOOK Ch8 "Dispatch prompts and the contract of record").
- [ ] Every contract's first instruction is: save this prompt as its own audit artifact and
      COMMIT IT FIRST, before any work. That commit is the lane's proof-of-boot.
- [ ] Every contract filename is legal under the ADR-101 Rule B grammar
      (`YYYY-MM-DD-<class>-<slug>.md`, class from the closed 11-class enum, all-lowercase kebab)
      — a refusal discovered after boot costs the lane a deviation note.

## 1 — grammar check, on the names git will CREATE
uv run --locked python scripts/validate_branch_naming.py --lane lane-<letter>-<id>-<slug>
# bare lane name. `worktree-` is added by the provisioner, exactly once.
# a `\d+` id segment is required: `lane-f-p10-evidence` FAILS, `lane-f-348-p10-evidence` passes.
# ANY off-grammar name is fixed HERE. At the merge queue it costs a rename mid-batch, and
# `batch_manifest.is_lane_merge` silently forfeits the ADR-110 exemption until it is fixed.

## 2 — dispatch the WHOLE batch in ONE block
# operator-run, from a terminal. never spawned from inside another session: a nested session
# carries no Agent View row (PLAYBOOK Ch8, AM-5).
dispatch <lane-a-contract>.md
dispatch <lane-b-contract>.md
...

## 3 — WAIT for the refs. this is the acceptance test for step 2.
for slug in <lane-slugs>; do
  git show-ref --verify --quiet "refs/heads/worktree-$slug" \
    && echo "OK   worktree-$slug" || echo "MISSING worktree-$slug"
done
# any MISSING row -> re-dispatch that lane alone. do not start integration with a hole in the batch.

## 4 — monitor: the board says WHEN to look, not WHAT happened
claude agents --json --all        # state == "done" is a SESSION signal
# it is not a completion signal. proceed to step 5 for every done lane.

## 5 — harvest from git, per lane. never from `claude logs`.
git log --oneline main..<branch>          # >=1 commit, and commit #1 is the contract stamp
git show <branch>:<packet-path>           # the packet, read from the tree
# a lane whose branch is missing, whose log is empty, or whose packet does not resolve is
# REPORTED as such. it is never recorded as done because the board said done.

## 6 — integrate
/lane-integrate    # serial merge queue from the primary checkout, one writer throughout
````

## 1.5 · What `[#539]` / `[#540]` would mechanize from this runbook — mapping, not a design

Recorded so the two rows inherit a concrete surface rather than a paraphrase. **No row text is
proposed here; neither row is edited by this lane.**

- **Step 1 is `[#539]`'s `--check` leg, already.** The row's Done-when says the leg *"refuses a
  contract whose branch name is off-enum or whose cited locators do not resolve"* — i.e. the
  grammar check moves from an operator's step-1 discipline into contract emission, which is
  strictly earlier than provisioning and therefore earlier than the point `[#514]` leg 1 /
  `[#531]` guard. The two are complements, not duplicates: `[#539]` refuses a bad name in the
  *contract*, `[#531]` refuses one at *ref creation*.
- **Steps 3 + 5 are `[#540]`'s whole subject.** The row already specifies board-read then
  `git show <branch>:<path>`, and *"a test proving it never invokes `claude logs` and that an
  unreachable lane is reported rather than skipped silently"*. Step 3's ref-existence wait is
  **not** in the row today; it is the same class of check (ask git, not the board) and is the
  natural companion to "an unreachable lane is reported rather than skipped".
- **Step 4 stays human.** Nothing here proposes mechanizing the board read — `[#540]` explicitly
  leaves dispatch operator-run, and a script that polls the board and decides a lane is done is
  the false-DONE defect with a cron on it.

---

# ITEM 2 — PARALLEL-DEFAULT DECISION MEMO ([#533]) · **CLEAR**

**Question as asked:** should the `audit-health` hook flip to `--parallel`?
**Recommendation:** **YES — but as a one-line change to the HOOK ENTRY, not to `run_checks`'s
default, and only after a five-run quiet-tree window.** Full statement at §2.5. The operator rules.

## 2.1 · The two numbers are not in conflict, and reconciling them changes the answer

| figure | what was actually measured | conditions |
|---|---|---|
| **1.41x** (integrator packet §A3) | the whole `audit.py health` invocation, **`--parallel` off** — 206.871 s vs the 290.9 s Phase-0 baseline | quiet tree, **single run** vs a median-of-3 baseline (4.9% spread) |
| **1.87x** (lane A, STEP 6) | one `run_checks()` call, serial, memo on vs memo off — 195.50 s vs 366.14 s median-of-3 | **loaded** — four sibling lane worktrees live; one uncached pair spread **84%** |
| **4.28x** (lane A, STEP 6) | one `run_checks()` call, `--parallel` + memo vs serial uncached — 85.60 s | same loaded conditions |

They measure different things and neither refutes the other. **But the gap between 1.41x and 1.87x
for the same memoized-serial mode is the decision-relevant fact, and it points one way:** the
end-to-end gain is smaller than the in-process gain, because `run_checks` is not the whole
invocation. Phase-0 T0.1 rules out the interpreter as the cause — `uv run --locked` measured 3.7 s
*faster* than direct venv Python — so the residue is import + `cmd_health`'s work outside the loop,
plus quiet-vs-loaded conditions.

**Derived estimate, labelled as derived — not a measurement.** Taking the quiet-tree memoized
end-to-end figure of **206.9 s** as the real starting point, and lane A's own parallel-over-cached
ratio of **0.438** (85.60 / 195.50) applied to the loop portion with a small fixed overhead F:

```
end-to-end parallel  ~=  F + 0.438 x (206.9 - F)
    F =  5 s  ->  ~93 s          F = 15 s  ->  ~99 s
```

So the honest expectation is **~90-100 s of commit tax, not the ~68 s** lane A's own extrapolation
gives — because that extrapolation multiplies the loaded-loop ratio against the quiet-tree
*baseline*, mixing two conditions. **Either way the saving is real and large: roughly 110 s off
every commit in this repo**, on top of the 84 s the memo already took. That is the case for acting.

## 2.2 · The parity evidence is unusually strong, and one named risk is already retired

- **Live-tree byte-identical digests.** All three modes wrote a `check_name:status` digest in
  emission order; three files, 2005 bytes each, **md5 `f2577dbc83f70248ff878bf03f2de69f` in every
  case**, 102 findings per run. That is parity on the real registry at full width, not on fixtures.
- **Load-independent counters back it.** 812 -> 408 git subprocesses (exactly the 404 duplicate
  spawns STEP-1 predicted), `_entries` split time 75.22 s -> 0.10 s at an unchanged 934 calls.
  These are properties of the code and do not move when the machine is busy.
- **`tests/test_audit_parallel.py` carries 20 tests**, including
  `test_serial_and_parallel_are_byte_identical_on_real_checks_against_the_live_tree`,
  `test_parallel_emits_in_registry_order_even_when_completion_order_is_reversed`,
  `test_an_exception_in_a_worker_propagates_and_is_never_swallowed`, and
  `test_health_restores_gate_mode_when_a_parallel_check_raises`.

**"CHECK_ORDER emission" is not a live risk — it is structurally impossible to violate.**
`run_checks` (`scripts/audit.py:3587-3594`) allocates one slot per check *indexed by submission
order*, assigns `slots[futures[future]]` as each future completes, and flattens in submission
order. Completion order never reaches the output. The docstring states this as the contract
(*"ORDER IS THE CONTRACT, not a side effect ... NEVER appended as work completes"*) and the
reversed-completion test pins it. Listing it as an open risk would overstate the exposure.

## 2.3 · Risks, each rated against what actually retires it

| risk | verified status | residual |
|---|---|---|
| **Thread-safety of check bodies** | **Verified this lane:** zero write operations (`write_text`, `open(...,'w'/'a')`, `mkdir`, `shutil.*`, `unlink`, `remove`) inside ANY `check_*` body — 0 hits across all 43, in the facade and in `scripts/audit_checks/` alike. **No `os.chdir` anywhere** in `audit.py`, `audit_checks/` or `journal_anchor.py` — the classic killer for concurrent git work is simply absent. | Checks are readers over git and the filesystem. LOW. |
| **Shared process globals** | `_GATE_MODE` is set once before the loop and restored after (two tests cover it, including the raise path). `journal_anchor`'s two `lru_cache`s are thread-safe containers; the worst concurrent case is two threads computing the same value once each — wasted work, never a wrong answer, and the values are immutable-by-hash by the memo's own design note. Other module globals (`ECOSYSTEM_DIR`, `_REPO_ROOT`) are read-only in the loop. | LOW. |
| **CI vs local variance** | **Retired by the recommended scope.** CI reaches the checker at `.github/workflows/report-only-wall.yml:149` as a bare `audit.py health` — recorded, never blocking. Flipping the *hook entry* does not touch that line, so CI keeps running serial and no CI variance is introduced at all. `_PARALLEL_MAX_WORKERS = 8` is a fixed constant, **not** `os.cpu_count()`-derived, so a 2-core runner would run 8 threads — a reason not to flip `run_checks`'s default, and a non-issue if only the hook flips. | NONE for the recommended option; MEDIUM for a runner-default flip. |
| **No quiet-tree parallel measurement exists** | **This is the real gap.** Every parallel figure was taken with four sibling worktrees live, on a run whose uncached sibling pair spread 84%. The 1.41x integration number is the only quiet-tree measurement, and it is serial. | The evidence bar at §2.6 exists to close exactly this. |
| **A FAIL verdict has never been produced under `--parallel`** | The parity digest was taken on a tree whose `health` was OK-with-WARNs. `test_health_restores_gate_mode_when_a_parallel_check_raises` covers a *raise*, not a FAIL finding + exit 1 — which is the gate's whole job. | Bar item 4 at §2.6. |

## 2.4 · The options, stated so the operator can pick a different one

- **A — flip `run_checks`'s `parallel` default to `True`.** Every caller changes at once: the hook,
  `audit_repo`, ship-gate, the nightly digest, CI. Largest blast radius, and the one option where
  the fixed 8-worker cap on a small CI runner matters. **Not recommended.**
- **B — change nothing.** Costs ~110 s per commit indefinitely. Defensible only if the parity
  evidence is doubted, and §2.2 is the reason to doubt it less than usual.
- **C — flip the HOOK ENTRY only**, `.pre-commit-config.yaml:172`:
  `entry: uv run --locked python scripts/audit.py health` -> `... health --parallel`. One line of
  data. Every other caller stays serial. Reverting is the same one line.
- **D — C, gated on a bounded quiet-tree evidence window.** C plus §2.6's bar run first.

## 2.5 · RECOMMENDATION — **option D**

Flip the **hook entry**, after the five-run quiet-tree window. Three reasons, in order of weight:

1. **The question is about the hook, and the hook is where the whole 291 s tax is paid.** Changing
   `run_checks`'s default to move one gate is a wider change than the problem needs, and it is the
   only version of this change that drags CI, ship-gate and the nightly digest along with it.
2. **The rollback is a one-line data revert**, with no code change to unwind and no test to
   re-baseline. That asymmetry — large measured gain, trivially reversible mechanism — is what
   makes acting on a single-condition measurement reasonable here rather than reckless.
3. **`run_checks`'s docstring already rules this the right shape**: *"Flipping the `audit-health`
   hook's default is a separate ruling ([#533] leg 2 contract), not a consequence of this code
   landing."* Option D is that separate ruling, taken at the surface the docstring names.

**What would change the recommendation to B:** any of the bar items at §2.6 failing — in
particular a single digest mismatch. Parity is the load-bearing claim; the speed is only worth
having if the verdicts are identical.

## 2.6 · Acceptance evidence a flip ruling should require

```
1  FIVE consecutive `--parallel` runs of `audit.py health` on a QUIET tree, operator host,
   nothing else running. Record all five, the median, and the spread. Bar: spread <= 10%
   (Phase-0's own quiet-tree discipline measured 4.9%).
2  For each of those five runs, the `check_name:status` digest is BYTE-IDENTICAL to a serial
   run on the SAME tree state. Repeat A's md5 comparison five times, not once -- a race that
   fires one run in five is exactly what a single comparison cannot see.
3  `pytest tests/test_audit_parallel.py tests/test_journal_anchor.py` green on that tree.
4  ONE run against a tree carrying a real FAIL finding, confirming `--parallel` produces the
   same finding, the same position in the emission order, and the same non-zero exit as serial.
   No measurement so far has exercised the gate's blocking path under threads.
5  The flip commit body records the measured median, the digest hash, and the literal revert
   line, so the rollback needs no reconstruction.
```

**Not required, and deliberately so:** a second opinion on thread-safety. §2.3's first two rows are
verified facts about the code (zero writes, zero `chdir`), not judgements, and re-litigating them
would be the kind of ceremony that makes an evidence bar unusable.

---

# ITEM 3 — D8 DECISION MEMO: THE `.devcontainer` `fleet_parity` WARN · **CLEAR**

**The WARN, verbatim** (packet §A2): `fleet_parity: .dev-knowledge root-sweep WARN-undeclared:
top-level entry '.devcontainer' is not in the template for role 'hub'`. Lane C landed a new
top-level tree and closed the ADR-101 hermetization surface for it but not the fleet desired-state
surface. Both routes are lawful by `fleet_parity`'s own logic (*"not in template? -> declared in
that repo's `.methodology.yaml` -> OK"*). Neither is chosen here.

**One correction to the framing, because it changes the blast radius.** The dispatch says "the
other 7 fleet repos". `ecosystem/parity-surfaces.yaml` declares **9** members: 1 hub
(`.dev-knowledge`), **2 consumers** (`ai-council`, `corp-monorepo`), and **6 pre-deploy**
(`corp-ops`, `corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`,
`win-tooling`). Pre-deploy members are rendered *"skipped (pre-deploy)"* and are not walked. So the
population either route can actually affect today is **2 repos, not 7 or 8** — and the six
pre-deploy repos inherit whichever choice is made only if and when they onboard.

### Route 1 — add a `.devcontainer` surface to `ecosystem/parity-surfaces.yaml`, hub role

- Declares `.devcontainer/` **fleet doctrine**; at `tier: {hub: LOCAL}` it binds only the hub, at
  `{hub: MUST, consumer: SHOULD}` it becomes an obligation the 2 walked consumers must satisfy.
- Consequence for the other 8: at `LOCAL` none is touched; at anything stronger, both consumers go
  `MUST-absent`/`WARN-undeclared` on the next walk until they carry a devcontainer they never asked for.
- Costs a manifest `version:` bump (`1.4.0`, nudge-parseable) and an `ownership.provenance` block —
  and `[#554]`'s D1/D2 proof legs are still OPEN, so it would enshrine an unproven substrate.

### Route 2 — declare `.devcontainer` in this repo's `.methodology.yaml`

- Declares it a **local opt-in**: `WARN-undeclared` -> `PASS-declared`, no other repo's walk changes.
- Consequence for the other 8: **exactly none** — this is the same shape the hub already uses for
  `.vscode`, `.claude-plugin`, `.worktreeinclude`, `codex`, `package.json`, and it needs only a
  `component` + `reason` + `review_date`.
- The `review_date` is the mechanism that forces the revisit rather than letting the question rot —
  precisely how the `.vscode` entry is already carrying an open fleet ruling (e1) on a short shelf-life.

### RECOMMENDATION — **Route 2**, with a short `review_date`

`.devcontainer/` is one repo's unproven experiment: `[#554]` stayed OPEN because D1 and D2 — the
*proof* legs, one lane running green on the Codespaces free tier and the identical script running
via `devcontainer up` — were never obtained. Promoting an unproven substrate to fleet doctrine
inverts the ordinary order (try, then generalise), whereas a declaration with a `review_date` set
near `[#554]`'s expected close costs nothing, clears the WARN honestly, and puts the fleet-doctrine
question back on the calendar with evidence in hand. **Route 1 stays available and loses nothing by
waiting** — the reverse is not true.

---

# ITEM 4 — REVIEW-ARTIFACT LINKAGE GAP · **CLEAR**

## 4.1 · Live measurement, on the real `main`

Re-implementation of `check_review_artifact_coverage` (see §0, Limit 2), walking `origin/main`
@ `87dd41af`:

```
review artifacts recognised : 21
code-impact merges scanned  : 41   (since the 2026-08-05 ruling date)
UNLINKED                    : 9
UNTALLIED                   : 1

f4a01f0e  worktree-lane-a-533-leg2          <- batch 1
7a316976  worktree-lane-e-502-mutmut        <- batch 1
e32093fd  fix/533-oracle-pin-repoint
b5054945  docs/batch6-wrap
d714cfea  worktree-lane-m-533-audit-decompose
e2403a44  worktree-lane-x-532-docrot-arms
d137cc6a  chore/phase2-position0
d62796ad  merge boot-acts 2026-08-15: gate 41->11,
387b794a  integrator/513-repin-close
5af0b33c  -> 2026-08-06-codex-lane-c-504-failclosed.md   (linked, no parseable **Tally:**)
```

**"2 WARNs" in the packet's §A3 table means two Finding objects, not two merges** — the leg emits at
most one `unlinked` Finding and one `untallied` Finding regardless of how many merges are in each.
The two counts are 9 and 1.

## 4.2 · Batch-1's two merges fail for two DIFFERENT reasons, and only one is the one H predicted

**Mode 1 — `f4a01f0e` (lane A): the artifact is never admitted to the candidate set at all.**
`docs/audits/2026-08-18-codex-review-batch1-a.md` carries a well-formed
`**Branch:** worktree-lane-a-533-leg2` and `**HEAD:** cb452ff1`. But its H1 is:

```
# TERRA REVIEW — BATCH 1 BRANCH A (`worktree-lane-a-533-leg2`)
```

and `_REVIEW_TITLE_RE` is `(?m)^# Codex Review\b`. The loop's guard is
`if not _REVIEW_TITLE_RE.search(txt) or not (branch_m or head_m): continue` — so the file is
skipped before its fields are ever read. It also carries **no `**Tally:**` line at all**, so even
with the title admitted it would move from `unlinked` to `untallied` rather than to green. Two
independent defects in one file. **Note this is the title predicate working as designed**: the
docstring records that 13 tracked non-review audit docs carry a `**Branch:**` field and 0 carry
this title, which is exactly why field-presence alone was rejected. The gap is that the enum of
admitted titles has one member while the tree has more than one review-artifact shape.

**Mode 2 — `7a316976` (lane E): the review exists, is well-formed, and is in the second half of a
file whose first half wins.** Lane H's one-artifact rule put both reviews in
`2026-08-18-codex-review-batch1-c-e.md`, which carries **two** complete triples:

```
line   4  **Branch:** `worktree-lane-c-554-devcontainer`
line   5  **HEAD:**   `5506f59aeb534d4dc0eab4a1edb856df87d9b349`
line  11  **Tally:**  0/1/4/0
line 274  **Branch:** `worktree-lane-e-502-mutmut`
line 275  **HEAD:**   `c43351de8134e9a5c040e3c4e5af099688b9a33d`
```

The reader uses `.search`, which returns the **first** match, so the artifact dict holds branch C
only and branch E is invisible. **Lane H predicted this in its own §0.3 before the merge happened**
— *"Branch E's merge will WARN (`review_artifact_coverage`) despite having been reviewed here"* —
and correctly left the choice to the integrator. The prediction was accurate.

## 4.3 · A third finding the measurement surfaced, on the disposition side

The packet's §5 act 2 removed `warn-review-artifact-387b794a-repin-close` and
`warn-review-artifact-d62796ad-boot-acts`, reasoning that *"the live `review_artifact_coverage` WARN
names a **different** merge set entirely, so the two review-artifact entries have left the scan
window rather than moved"*. **Both SHAs are still in the unlinked set today** — they are items 8 and
9 of 9. What changed is the *rendering*, not the scan window:

```
9 code-impact merge(s) since 2026-08-05 carry no linked review artifact: f4a01f0e
worktree-lane-a-533-leg2, 7a316976 worktree-lane-e-502-mutmut, e32093fd
fix/533-oracle-pin-repoint, b5054945 docs/batch6-wrap, d714cfea
worktree-lane-m-533-audit-decompose (+4 more)
```

The evidence string truncates at **5 names + `(+N more)`**, and `ecosystem/disposition-register.yaml`
keys each entry by `match` — *"a substring that must appear in the WARN's evidence"*. So a
disposition keyed on a SHA stops matching the moment newer unlinked merges push that SHA past
position 5, **even though nothing about the dispositioned merge changed**. The removal was
therefore correct about the mechanism (the entries genuinely no longer matched) and wrong about the
cause (they had not left the scan window). **This is a structural incompatibility, not a mistake by
the closing seat** — and the register's own header names the reason it bites:

> *"A dispositioned organ must emit one Finding PER concern, else one matched token would wave
> through unrelated drift bundled in the same finding (Codex CRITICAL 2026-06-10).
> `git_backlog_drift` emits one Finding per drifted id for exactly this reason."*

`review_artifact_coverage` bundles N merges into one Finding, so it does not satisfy the
precondition its own disposition entries assume. That is why the row below carries "one Finding per
unlinked merge" as a Done-when item rather than leaving it to a later discovery.

## 4.4 · What linkage the check actually wants — the direct answer

The dispatch asks: naming? frontmatter? merge-message ref? **Answer: a naming rule AND a field
rule, both first-occurrence-only; the merge message is read but never authored by the reviewer.**

```
1  H1 TITLE (naming)   `^# Codex Review\b` at line start, `(?m)`. NOT optional: without it the
                       file is skipped before any field is read. Sole admission criterion.
2  FIELDS (frontmatter-shaped, but plain markdown bold lines, not YAML):
     **Branch:** `<name>`        must equal the merge subject's `Merge branch '<x>'` capture
     **HEAD:**   `<7-40 hex>`    must prefix-match a commit in the merge's introduced() set
     **Tally:**  `n/n/n/n`       at line start; absent -> `untallied` WARN even when linked
   EITHER Branch or HEAD satisfies linkage; the Tally is required on top of whichever linked.
3  ONE TRIPLE PER FILE  every field is read with `.search` -> first match only.
4  MERGE-MESSAGE REF    NOT a thing the reviewer writes. The merge subject is the JOIN KEY,
                        parsed by `^Merge branch '([^']+)'`. A reviewer cannot add linkage
                        from the merge side; naming the artifact in the merge subject does
                        nothing, because the leg never reads the merge body.
```

**And the constraint that decides the fix's shape: audits are IMMUTABLE (CLAUDE.md §5 rule 3).**
Lane A's artifact cannot be given a title or a tally after the fact. So the gap cannot be closed on
the artifact side for anything already committed — **every part of the repair has to be reader-side**,
which is also consistent with the leg's own FORWARD-ONLY design note about never demanding a
retro-edit.

## 4.5 · DRAFT ROW TEXT

Filed here as a draft only — **this lane writes no BACKLOG row** (contract exclusion). The `[#NNN]`
placeholder is for the filing seat. Measured against both `validate_doc_rot` arms before drafting
was finished: **1311 chars against the 1320 ceiling (headroom 9)**, and **0 raw dates** outside
artifact identifiers, so arm 1 (`>=3 dates AND >700ch`) is clear too. A filing seat that adds a
word will red `backlog-row-length`; trim §"Two structural riders" first, since the source carries it.

```
- [#NNN] [P2][S] **`review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it** — measured on `origin/main` @ `87dd41af`: 9 unlinked merges, two of them batch-1's own, failing two DIFFERENT ways. Lane A's artifact is never admitted (H1 `# TERRA REVIEW …` vs `_REVIEW_TITLE_RE` `^# Codex Review`; no `**Tally:**`); lane E was reviewed but sits in the SECOND triple of a two-branch artifact and `.search` takes the first. Lane H predicted both (§0.3). Artifacts are IMMUTABLE (§5 rule 3), so the repair is reader-side. Two structural riders (bundled Finding; evidence truncation) are in the source · Done when: the reader parses EVERY triple in a file, a multi-branch artifact links every branch it reviews, the title predicate admits the forms actually in `docs/audits/` while still admitting 0 of the 13 non-review docs carrying `**Branch:**`, the leg emits one Finding per unlinked merge, and any residual WARN on an immutable artifact is dispositioned · refs scripts/audit.py:3117-3320, ecosystem/disposition-register.yaml, #480, #499 · kill-candidates: none — `[#499]`'s hard flip is GATED on this leg's false-positive count, which these false WARNs corrupt · source: docs/audits/2026-08-19-technical-n5-codification-pack.md §4
```

**Why this is worth a row rather than a disposition.** `[#499]`'s hard pre-push leg is gated on
*"zero false positives over two consecutive windows"*. Lane A and lane E are **two false positives
in one batch** — both merges were genuinely reviewed. Dispositioning them would suppress the WARN
while leaving the evidence bar corrupted, so `[#499]` would be measuring the leg's parser rather
than the repo's review discipline. Fixing the reader is what makes that bar mean what it says.

---

# ITEM 5 — SESSION-LESSONS SWEEP · **CLEAR** (with the §5.0 caveat)

## 5.0 · The provenance caveat, stated first because it bears on two of the ten

The dispatch asks for *"the bc-absent-in-git-bash and job-tmp-lifetime items **from Phase 0**"*.
**`docs/audits/2026-08-18-technical-phase0-baselines.md` records neither by that name** — it was
read end-to-end and searched (`bc`, `git-bash`, `TMPDIR`, `tmp`, `retention`): T0.1 is the commit
tax, T0.2 the mutation pilot, T0.5 the hotspot ranking, T0.6 the grammar verify. The session-chat
wording is not recoverable from this container.

Rather than paraphrase from nothing, **each is grounded on the nearest in-tree evidence that does
exist**, cited in the table. The promoting seat should reconcile candidates 1 and 2 against its own
transcript before promotion — if the session recorded something sharper, the session wins.
Candidates 4 and 6 are the two §1.2 flagged as resting on the dispatch's own statement.

## 5.1 · Ten candidates, deduplicated against all 278 existing `LESSONS.md` entries

Checked live: no existing entry mentions `bc`, `TMPDIR`, a shallow clone, the doubled `worktree-`
prefix, board-vs-tree completion, or transcript-vs-git harvest. **All ten are non-duplicates.**
Format below is candidate-shorthand; a promoted entry gets the full
`### YYYY-MM-DD | source | lesson | category | [scope: X] | action taken` shape.

```
#   lesson (one line)                                                          category    provenance
--------------------------------------------------------------------------------------------------------
1   Assert a CLI tool is present before depending on it -- `bc` is ABSENT in   tooling     IN-TREE:
    Git Bash on Windows, and the first count attempt must fail loudly (exit                2026-07-19-census-
    127) rather than return zeros.                                                         silent-rule-ledger:51
2   A CI job's working files do not outlive the job -- the mutmut diagnostic    tooling     IN-TREE: phase0 T0.2
    was readable ONLY because `upload-artifact` captured `mutmut.out`                       + report-only-wall.yml
    (retention 90d). Upload what you will need to diagnose, before it ends.                 :295-302
3   An unset env var in a compound shell line collapses the path and `set -e`   tooling     IN-TREE: JOURNAL:679
    does NOT abort the line -- an empty `$TMPDIR` sent `mkdir`/`cd` to bare                (ran against the LIVE
    root and the rest of the line ran against the live hub checkout.                        hub checkout)
4   A board state of `done` is a statement about the SESSION, not the WORK --   process     DISPATCH-STATED
    it cannot distinguish a finished contract from a session that stopped                   (see S1.2)
    early. Verify completion from the tree, never from the board.
5   Harvest lane output from git (`git show <branch>:<path>`), never from       process     IN-TREE: row [#540];
    `claude logs` -- transcripts are ANSI screen replay, expire, and are                    PLAYBOOK:2058
    unavailable to any later seat.
6   Dispatch a batch in ONE block, then WAIT until every branch EXISTS --       process     DISPATCH-STATED
    concurrent provisionings contend on the CLI config lock, and a lost lane                (see S1.2)
    returns an apparently-successful dispatch with no branch.
7   Check lane grammar against the names git will CREATE, not the ones you      verification IN-TREE: packet S2
    intended -- batch 1 lost 2 of 8 lanes to `p10`/`a9` not matching `\d+`,                 (2 of 8) + PLAYBOOK
    batch 6 lost 12 of 12 to a doubled `worktree-` prefix. One defect, twice.               :2095-2106 (12 of 12)
8   In a fresh cloud container, verify clone DEPTH and ref CURRENCY before      verification MEASURED THIS LANE
    measuring anything against `main` -- this lane's clone was shallow (48                  (S0, Limit 1)
    commits) with `main` four days stale, and the un-repaired reading of
    item 4 returned "0 unlinked", i.e. wrong in the reassuring direction.
9   A cloud lane's commits pass WITHOUT the pre-commit gates -- they are not    process     MEASURED THIS LANE
    armed there, so nothing is bypassed and nothing is checked. Say so in the               (S0, Limit 3)
    packet; the integrator meets those gates for the first time at the merge.
10  A suppression keyed on a SUBSTRING of a RENDERED message inherits that      methodology MEASURED THIS LANE
    renderer's truncation -- two dispositions silently stopped matching when                (S4.3)
    newer merges pushed their SHAs past the evidence string's 5-name cutoff.
```

**Two notes for the promotion ruling, offered rather than assumed.** Candidate 7 merges two
separately-witnessed incidents into one lesson because they share a root (validating intent instead
of the created ref); a seat that wants them separable should split it before promotion, since
`LESSONS.md` is append-only and a merged entry cannot be split later. Candidates 8 and 9 are
properties of the **cloud lane channel** rather than of this repo's methodology — if the seat holds
that `LESSONS.md` is repo-scoped, they belong in the channel's own runbook instead, and this lane
has no view on which is right.

---

# STOP PACKET

```
LANE      night N5 — codification + decision-memo pack
BRANCH    claude/night-n5-codification-memos-eyef8r
CONTRACT  docs/audits/2026-08-19-technical-n5-codification-pack-contract.md
OUTPUT    docs/audits/2026-08-19-technical-n5-codification-pack.md

ITEM                                                     VERDICT
1  dispatch-runbook + PLAYBOOK Ch8 section draft          CLEAR   2 paste-ready drafts; 3 of the 6
                                                                  named lessons were already doctrine
                                                                  and are cross-referenced, not restated
2  parallel-default memo ([#533])                         CLEAR   recommends option D (flip the HOOK
                                                                  ENTRY, after a 5-run quiet window)
3  D8 memo (.devcontainer fleet_parity)                   CLEAR   recommends route 2 (.methodology.yaml)
                                                                  with a short review_date
4  review-artifact linkage gap                            CLEAR   9 unlinked measured; 2 distinct failure
                                                                  modes named; row drafted at 1311/1320
5  session-lessons sweep                                  CLEAR   10 candidates, all non-duplicates;
                                                                  one provenance caveat at S5.0

NOT DONE, by contract: no PLAYBOOK edit · no script edit · no roster row · no BACKLOG/tasks write
                       · no ruling · no merge · no PR
```

**Open decisions handed back — three, none of them this lane's to make:**

1. **`[#533]` parallel default** — options at §2.4, recommendation §2.5, evidence bar §2.6.
2. **D8 `.devcontainer`** — two lawful routes at §3, recommendation route 2.
3. **The two DISPATCH-STATED lessons (§1.2)** — cite the session artifact, or accept them on the
   operator's own witness and record that in the codification commit body.

**Honest limits of this artifact, in one place:** the `audit.py` measurement of §4.1 comes from a
re-implementation, not the real module (§0 Limit 2) — the reproduction command is given and a seat
with the environment should re-run it before filing the row; the §2.1 end-to-end parallel estimate
is arithmetic on two measurements taken under different conditions and is labelled derived, not
measured; and no gate ran on this branch (§0 Limit 3).

---

# AMENDMENT — 2026-08-19, post-STOP · item 4 measured against the REAL module

> **In-file amendment marker** (audits are immutable; superseded content is not rewritten —
> CLAUDE.md §5 rule 3, same form the batch-1 integrator packet uses). This section resolves §0
> Limit 2 **for item 4 only**. Nothing above is edited, and no conclusion above changes.

**What changed in the environment.** `uv self update 0.11.19` was attempted first and **failed**
(*"version 0.11.19 was not found for the app uv in workspace uv"*), so the pinned-`uv` path stayed
shut. The three missing imports were installed directly instead — `click`, `markdown-it-py`,
`pyyaml` — after which `import audit` succeeds under the container's Python 3. The local `main`
ref was also fast-forwarded to `origin/main` @ `87dd41af` (a **local ref move only, never pushed**;
`main` is not checked out here), because the check walks `main` by name and this container's copy
was the stale 2026-08-14 one recorded in §0 Limit 1. **No tracked file was changed by any of this.**

**The real `check_review_artifact_coverage`, run in-process:**

```
WARN | 9 code-impact merge(s) since 2026-08-05 carry no linked review artifact: f4a01f0e
       worktree-lane-a-533-leg2, 7a316976 worktree-lane-e-502-mutmut, e32093fd
       fix/533-oracle-pin-repoint, b5054945 docs/batch6-wrap, d714cfea
       worktree-lane-m-533-audit-decompose (+4 more) -- advisory per the [#480] P3 ruling ...

WARN | 1 linked artifact(s) carry no parseable **Tally:** line: 5af0b33c ->
       2026-08-06-codex-lane-c-504-failclosed.md -- persistence is not machine-auditability ...
```

**Agreement with §4.1 is exact** — 9 unlinked, the same five names in the same order, the same
`(+4 more)`, the same single untallied artifact, and **two Finding objects**, which independently
confirms §4.1's reading that the packet's "2 WARNs" counts Findings and not merges. The
re-implementation was faithful; §4.1's numbers stand as measured against the real module.

**What this retires, and what it does not.** It retires §0 Limit 2's instruction to *"re-run before
filing the row"* — the row at §4.5 may be filed on these numbers. It does **not** retire §0 Limit 1
(recorded because the stale-ref reading really did return a false clean) or §0 Limit 3: the
pre-commit gates remain unarmed here, `audit.py health` as a whole was never run, and the
`session_end_backpressure.py` Stop hook still cannot start, because it is invoked through
`uv run --locked` and that path is the one the failed `uv` update left shut.
