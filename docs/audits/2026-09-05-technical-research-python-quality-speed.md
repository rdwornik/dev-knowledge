# Python quality & speed — a measured research arc

- **Lane:** RESEARCH, read-only · **Branch:** `worktree-research-python-quality`
- **Measured at:** `main` @ `3200757d` · **Landed on:** `main` @ `09f80530` (the lane was fast-forwarded onto
  current main before committing — zero lane commits, so no merge commit; every number below was taken at
  `3200757d` and none was re-derived after the advance)
- **Date:** 2026-09-05 · **Substrate:** local Windows workstation (win_amd64), CPython 3.12.10, uv 0.11.19
- **Thesis under test (not assumed):** *the cost is architecture (monolith, tree walks), not the interpreter.*
- **Verdict on the thesis:** **CONFIRMED, with the monolith half rejected.** The cost is architecture — but
  it is **N-spawn loops and re-reads**, not module length. `audit.py`'s size is nearly irrelevant to its
  runtime; its `subprocess` fan-out is nearly all of it. 75–79 % of both gates is spent blocked on git, and
  the single biggest defect is one `for` loop that spawns a `git log` per directory — measured at **133.7×**
  when batched, behaviour-identical.
- **Second finding, not in the brief:** on the quality side the gap is **not an undecided question but a
  decided one with no carrier.** The paradigm and naming doctrine is ruled (ADR-108 §B-4) and says of itself
  *"Arms no gate"*; mutation testing is ruled ADOPT with a no-growth ratchet. Arming the ruled naming half
  costs **13 fixes**. See §1.6–§1.7.

## Two defects in this arc's own brief, resolved and recorded

**1. The "Dispatch-Cloud row" is UNLOCATABLE in-repo.** The brief instructed this lane to quote it. It
cannot be quoted, because it is not in the repository. An exhaustive sweep found `Dispatch-Cloud` only in
`protocols/PLAYBOOK.md` Ch8's dispatch table, `protocols/STANDING_RULINGS.md` V1/V3, and
`ecosystem/substrate-registry.yaml` (`verbs: [Dispatch-Cloud]`), plus older intake provenance lines and
`docs/audits/2026-08-26-technical-perf-recon.md`. No batch row anywhere describes a Python quality/speed
research arc; the newest manifest, `docs/audits/2026-09-02-technical-batch-g-manifest.md`, carries a 9-lane
roster (G0–G8, G3b) with no such lane and no batch H exists. `PROPOSED NEXT BATCH` is **computed, not
stored** — `scripts/boot_frontier.py` derives it from `tasks/*.md` `depends-on:` in-degree-0 — so there is
no static row to quote even in principle. The row is browser/operator state, the same shape as the
2026-08-26 perf recon whose provenance note records a report "reconstructed from the operator's chat
transcript". **Stated as unlocatable rather than paraphrased.**

**2. The brief's filename would have been REFUSED by a live gate.** It specified
`docs/audits/<date>-research-python-quality-speed.md`. `validate_hermetization.AUDIT_CLASS_ENUM`
(`scripts/validate_hermetization.py:149`) admits `technical, functional, qa, census, verification,
ecosystem-audit, conformance-nightly-digest, changelog-review, codex, fresh-eyes, incident-evidence` —
there is no `research` class, and the audit-name grammar is enforced on staged ADDs at pre-commit. This
file therefore lands as `2026-09-05-technical-research-python-quality-speed.md`: class `technical`, the
brief's intended name preserved verbatim as the slug.

**3. There is no L5 profiling lane to reuse.** The brief said to use L5's numbers if landed. L5 timed the
**suite** only (`docs/audits/2026-09-01-verification-codespace-longrun-proof.md`). `audit.py health` was
profiled by *other* lanes, and those numbers are cited in §0.4 rather than re-derived.

## Model routing, per section

| Section | Model used | Why |
|---|---|---|
| §0, §1 (measurement, census) | Opus 5 (`claude-opus-5[1m]`), default worker | Instrumentation + arithmetic |
| §2 (survey) | **Fable 5.1** (`claude-fable-5-1`) | Strongest model this CLI exposes |
| §3, §4 (candidates, counter-list) | **Fable 5.1**, re-based and corrected on Opus 5 | Synthesis + judgment |

`claude-fable-5-1` **is** selectable from this CLI: the `Agent` tool's `model` parameter accepts `fable`
alongside `sonnet`/`opus`/`haiku`, and §2–§4 were drafted by subagents pinned to it. Three corrections were
applied to the Fable drafts on Opus 5 before landing, each named at its site: the CPU/IO split was re-based
from the cProfile-inflated run onto the clean run (§3d, §4); an invented `127 of them` count was struck
(§4); and **both drafts described `[#407]` and `[#502]` as open rows when both are closed with landed
rulings** — §1.6 records what they actually decided, and §3(a) and §3(c) were rewritten against those
rulings rather than against the open questions the brief assumed. That third correction changed the
substance of two candidates, not their wording.

---

## §0 — The measured split (I/O vs CPU, seconds)

**Model used, per section** (the brief asks this be stated here): **§0 and §1 on Opus 5**
(`claude-opus-5[1m]`), the default worker — instrumentation, census and arithmetic. **§2, §3 and §4 drafted
on Fable 5.1** (`claude-fable-5-1`), the strongest model this CLI exposes, **then re-based and corrected on
Opus 5**. The full routing table, including the three corrections applied to the Fable drafts, is in *Model
routing, per section* above.

**Answering §0 of the brief directly.** The ACCEPTED intake is `docs/intake/2026-08-09-func-code-style-
doctrine.md` (intake-id 31, `status: ACCEPTED`, decided at the batch-4 planning GO 2026-08-11). **Its status
is: text only. No skill and no check enforces any part of it.** Its §A doctrine is written and ratified but
gated nowhere; its §B mechanism stack is unadopted — ruff runs its default rule set, and every other tool §B
names (`mypy`, `basedpyright`, `import-linter`, `deptry`, `semgrep`, `complexipy`) is absent from every real
config file. The one exception is §B's own precondition: §D's hotspot measurement, which the ruling made
binding and which this report supplies. Details, and the full sweep for Python style-guide artifacts, are in
§1.5–§1.7.

### §0.1 Method

Both commands were run **twice**: once under `cProfile` with `subprocess.Popen`, `builtins.open`,
`Path.read_text` and `Path.read_bytes` wrapped to count and time, and once with the same wrappers but the
profiler **off**. The clean run is the authority for the split; the profiled run is the authority for
attribution. This matters: `cProfile` recorded 27.9 M function calls for `health` and 100.5 M for
`ship-gate`, and it inflated the measured Python CPU of `health` from 19.31 s to 33.41 s — a 73% overstatement.
Any split quoted off a profiled run overstates CPU.

Definitions: **wall** = `time.perf_counter()` around the click invocation. **CPU** = `time.process_time()`
(user+sys of *this* interpreter). **subprocess** = wall time inside the first blocking call per `Popen`
object, plus `Popen.__init__` (which on Windows is where `CreateProcess` is paid). Interpreter startup and
module import are outside the window. The residual line is the small overlap between the kernel time
`process_time` attributes to this process and the child-wait bucket.

### §0.2 `audit.py health` — the commit-tier gate

```
wall                     75.778 s
  blocked on children    56.888 s   75.1 %
  own Python CPU         19.312 s   25.5 %
  overlap/residual       -0.422 s   -0.6 %
checks run                    42     (commit tier; 41/155 pass, the rest n/a or ship-tier)
subprocesses                 160     159 git + 1 pwsh.EXE
distinct paths read        2,538
read-opens                 5,985
paths opened >1x           1,744  -> 5,191 of 5,985 opens (86.7 %) are re-reads
```

git subcommand census for one `health` run:

```
log 99 · show 16 · cat-file 14 · rev-parse 12 · ls-files 5 · diff 4
ls-tree 3 · rev-list 2 · worktree 1 · config 1 · status 1 · merge-base 1
```

**Three quarters of the commit gate is spent waiting on git.** Under the profiler,
`{built-in method _winapi.CreateProcess}` cost **15.851 s of tottime across 160 calls — 0.099 s per spawn,
20.4 % of that run's wall — before git executes a single instruction.**

### §0.3 `audit.py ship-gate` — the full registry

```
wall                    652.135 s   (cProfile-instrumented; clean run in §0.3a)
  blocked on children   474.426 s   72.7 %
  own Python CPU        157.766 s   24.2 %
  residual               19.943 s    3.1 %
checks run                     54     (no tier passed; everything runs)
subprocesses                1,305     1,303 git + 1 python.exe + 1 pwsh.EXE
distinct paths read         2,683
read-opens                 15,578
paths opened >1x            2,461  -> 15,356 of 15,578 opens (98.6 %) are re-reads
```

git subcommand census for one `ship-gate` run:

```
diff 468 · rev-list 467 · log 251 · check-ignore 28 · rev-parse 24 · show 23
cat-file 14 · ls-files 9 · merge-base 5 · config 4 · status 4 · ls-tree 3
worktree 2 · stash 1
```

`{built-in method _winapi.CreateProcess}` = **191.450 s tottime over 1,305 calls (0.147 s/spawn), 29.4 % of
wall.** The `diff` 468 / `rev-list` 467 / `log` 251 shape is the per-spine-entry trio that
`docs/audits/2026-08-26-technical-w2a-perf-core.md` named and deliberately did not chase.

**98.6 % of `ship-gate`'s file reads are re-reads.** Every module under `scripts/` is opened **33–34 times
in a single run** — `scripts/audit.py` 34×, `scripts/audit_checks/_common.py` 33×, and so on across the
whole tree — alongside `protocols/HANDOFF_PROCESS.md` 50×, `protocols/PLAYBOOK.md` 43×,
`protocols/DEFINITION_OF_DONE.md` 40×, `docs/decisions/README.md` 38×.

### §0.3a Clean `ship-gate` — the authoritative split

```
wall                    664.506 s
  blocked on children   521.696 s   78.5 %
  own Python CPU        121.359 s   18.3 %
  overlap/residual       21.451 s    3.2 %
subprocesses                1,309     1,307 git + 1 python.exe + 1 pwsh.EXE
```

**Nearly four fifths of the full gate is spent waiting on git.** cProfile inflated this run's Python CPU
from 121.359 s to 157.766 s (a 30 % overstatement, against 73 % on the smaller `health` run — the
overhead scales with recorded call count, which was 100.5 M here against 27.9 M there).

Two honesty notes on the pair. First, the clean run's **wall is 12.4 s *higher*** than the profiled run's
(664.5 vs 652.1) even though it did 36 s less CPU work: wall on this host is host-load-noisy at the ±2 %
level, and the two runs were taken under different background load. The CPU figure is the one the profiler
distorts and the one worth correcting; the wall figures should be read as "about eleven minutes" and not
compared to each other at the second. Second, the git subcommand counts differ by exactly +1 in three
places (`diff` 469 vs 468, `rev-list` 468 vs 467, `log` 252 vs 251) because the working tree gained this
document between the two runs — a one-file change moving three per-file spawn counts is itself a small
illustration of the shape §0.5 is about.

### §0.4 Top cumulative functions (profiled runs)

`health`, top by cumulative time:

```
77.611  cmd_health                                   audit.py:5886
77.594  run_checks                                   audit.py:5183
77.593  _run_one (42 calls)                          audit.py:5267
45.235  subprocess.run (160 calls)                   subprocess.py:506
25.539  check_handoff_probes                         audit.py:2447
25.211  _select_active_bundle                        audit.py:2345
25.206  _run (89 calls, git)                         audit.py:2379
17.231  check_journal_spine_anchor                   audit.py:4181
16.026  Popen.__init__ (160 calls)                   subprocess.py:807
15.851  _winapi.CreateProcess (160)   [tottime]
 9.950  journal_anchor.unanchored_on_spine           journal_anchor.py:521
 9.230  journal_anchor.is_anchored (494 calls)       journal_anchor.py:480
 8.804  journal_anchor.introduced (988 calls)        journal_anchor.py:444
 8.700  proof_layer.scan_guards                      proof_layer.py:363
```

`health`, top by internal (tottime) time — the genuinely CPU-bound lines:

```
 4.414  journal_anchor._introduced_from_map   494 calls
 2.916  _io.open                            6,329 calls
 1.871  ast.iter_child_nodes            1,379,432 calls
 1.157  builtins.compile                      166 calls
 1.115  ast.iter_fields                 1,885,274 calls
 1.076  ast.walk                          690,178 calls   (5.938 s cumulative)
 0.791  re.Pattern.search                  35,546 calls
```

`ship-gate`, top by cumulative time:

```
652.132  cmd_ship_gate                               audit.py:6002
651.715  run_checks / _run_one (54 calls)            audit.py:5183
474.587  subprocess.run (1,305 calls)                subprocess.py:506
367.115  check_review_artifact_coverage              audit.py:4488   <- 56.3 % of wall
359.744  journal_anchor._git (1,064 calls)           journal_anchor.py:82
193.372  Popen.__init__ (1,305 calls)                subprocess.py:807
191.450  _winapi.CreateProcess (1,305)  [tottime]
 65.349  check_doc_code_edge                         audit.py:2889
 62.053  validate_doc_code_edge.find_code_sites (32) validate_doc_code_edge.py:152
```

`ship-gate`, top by internal (tottime) time:

```
191.450  _winapi.CreateProcess                   1,305 calls
 21.775  tokenize._generate_tokens_from_c_tokenizer   10,378,383 calls
 17.479  collections.namedtuple._make                 10,373,985 calls
 13.679  _io.open                                         18,213 calls
  8.949  validate_doc_code_edge.find_code_sites               32 calls
  5.421  funnel_coverage.split_cells                     209,494 calls
  4.140  ast.iter_child_nodes                          1,379,432 calls
  3.098  builtins.compile                                    186 calls
```

**The one real CPU hotspot, named:** `validate_doc_code_edge.find_code_sites` is called 32 times — once per
rule — and each call re-tokenizes the source tree. That is **10.38 M `tokenize` calls costing 21.8 s of
tottime and 62.1 s cumulative**. This repo has already recorded the identical shape once
(`build_edge_index` re-tokenizing per rule, 14.53 s → 0.75 s). It is the same bug in a sibling function.

### §0.5 The one-spawn defect, measured end to end

`audit.py:2345 _select_active_bundle` selects the active handoff bundle by git add-date. Its body:

```python
for d in candidates:
    out = _run(["log", "--diff-filter=A", "--reverse", "--format=%at",
                "--", f"docs/handoffs/{d.name}"])
```

One `git log` **per bundle directory**, to compute a single maximum. In the profiled `health` run that was
**89 spawns costing 25.211 s of a 77.6 s wall**, i.e. the whole of `check_handoff_probes` bar 0.3 s.

Measured A/B, both halves run back to back in one process under identical load, over all 118 non-archive
bundle directories:

```
loop as shipped     118 spawns   46.374 s   (0.393 s/spawn)
one batched call      1 spawn     0.347 s
                                 ---------
speedup                          133.7x     46.027 s saved
```

The batched form is `git log --diff-filter=A --reverse --format=%at --name-only -- docs/handoffs`, reduced
in Python. **It is behaviour-identical, verified, not assumed:** all 118 add-dates agreed exactly, zero
paths missing, zero disagreements, and the selected bundle was the same
(`2026-09-01-dev-knowledge-architect-v7`). This is the single largest, cheapest, lowest-risk win in the
measurement.

### §0.6 Prior landed profiling — cited, not duplicated

- `docs/audits/2026-08-18-technical-533-leg2-measurements.md` — per-check loop total **334.49 s**; git
  subprocesses **812 calls / 116.81 s / 56.3 %** of the check, of which `git rev-list` 808 calls / 116.25 s.
  Verbatim: *"each call spawns two `git rev-list` processes at ~144 ms apiece on this platform. ~404 of the
  808 spawns compute an answer the process already had."* Its Amdahl note: with one check at 63.2 % of
  wall, parallelising the other 42 caps whole-registry speedup at **~1.58×**.
- `docs/audits/2026-08-18-technical-phase0-baselines.md` — whole-invocation median **290.9 s** (min 287.9,
  max 302.1).
- `docs/audits/2026-08-26-technical-w2a-perf-core.md` — `check_journal_spine_anchor` 197,808 ms → 7,086 ms
  (**27.9×**); wall 210.1 s → 140.1 s; **target `< 60 s` MISSED**; residual top check
  `check_review_artifact_coverage` at 128,428 ms / 42.4 %, *named and not chased*. This session measures
  that same check at 367.1 s / 56.3 % of `ship-gate` — it is still the largest single organ, and it has
  grown.
- Suite timings, already landed and reused rather than re-run: `pyproject.toml` records serial **1785.61 s**
  vs `-n auto` **330.15–358.77 s** (~5.2×) at the 2,362-test scale;
  `docs/audits/2026-09-01-verification-codespace-longrun-proof.md` records the full 4,861-item suite at
  **294.07 s** and **298.50 s** on a codespace; `docs/audits/2026-09-02-technical-batch-g-manifest.md`
  records **local 897.22 s** and **codespace 311.24 s**.

### §0.7 A live doc defect found in passing

`.pre-commit-config.yaml:284` documents the `audit-health` hook as costing **`~1.4s`**. Every landed
measurement contradicts it — phase-0 median 290.9 s, post-fix 140.1 s, and this session's commit-tier run
75.78 s clean. The claim is wrong by roughly **54× to 208×**. It is a one-line doc fix, DISCHARGED-class,
not a backlog row. (Note the hook invokes `health --parallel`; this session measured the serial arm, so the
comparison is to the 140.1 s landed `--parallel` figure as much as to 75.78 s. Either way the order of
magnitude is wrong.)

---

## §1 — Module census

Computed by AST over `scripts/*.py` (94 modules), **cross-checked against radon**, which agreed exactly on
every hotspot value (88, 65, 56, 41, 38, 35, 35, 32, 30, 28, 27). Where the two differ marginally, radon is
the authority quoted here: this census sums a nested function's complexity into its enclosing function,
radon reports nested defs separately. Never restate these counts in prose elsewhere — regenerate them.

```
modules                    94
lines                  53,748
code lines             40,077        (non-blank, non-comment)
functions               1,620
classes                   158
modules > 800 lines        17
functions > 60 lines       89
functions CC > 10         185
functions CC > 20          32
radon: 1,808 blocks analyzed, AVERAGE COMPLEXITY B (5.20), four F-rank functions in the tree
```

### §1.1 Every module over 800 lines

```
module                        lines   code    fn   cls   maxCC   sumCC
audit.py                       6193   4537   142     6      35    1007
nopack_sandbox.py              2510   1846    70     7      27     459
fleet_parity.py                2054   1717    50     5      88     502
gen_task_tree.py               1729   1291    50     3      38     290
gen_dashboard.py               1420   1098    66     8      16     316
gen_trend_dashboard.py         1369   1104    37     3      14     179
gen_handoff.py                 1334    982    40     6      15     191
fleet_analytics.py             1264   1047    40     5      23     236
fleet_health.py                1205    869    43     0      16     216
enforcement_coverage.py        1196    863    54     6      14     256
preflight_contract.py          1193    722    31     3      23     186
gen_lane_contract.py           1137    859    22     3      65     152
cloud_provisioning.py          1011    756    29     6      35     175
file_purpose_graph.py           998    761    40     5      22     203
archive_row_body.py             969    760    28     2      32     163
generate_organ_index.py         846    679    35     1      19     186
single_flight.py                837    603    24     1      25     106
```

### §1.2 Every function over 60 lines — all 89

```
module                        function                          line   lines   CC
gen_lane_contract.py          parse_contract                    698     232    65
fleet_parity.py               _eval_row                        1134     210    35
fleet_analytics.py            build_digest                      748     206    23
fleet_parity.py               collect_facts                     597     201    88
gen_task_tree.py              _scan_source                     1105     172    38
gen_lane_contract.py          render_contract                   504     170    12
single_flight.py              release                           594     164    25
generated_artifact_freshness.py measure                         362     162    27
fleet_parity.py               load_manifest                     269     159    56
audit.py                      check_review_artifact_coverage   4488     153    35
audit.py                      _commit_routine_outputs          5530     146    19
gen_handoff.py                generate                         1143     146    15
cost_usage_telemetry.py       emit_genai_span                   289     145    30
cloud_provisioning.py         repair_history                    497     143    35
funnel_lifecycle.py           measure                           532     143    41
gen_trend_dashboard.py        build_series                      719     137    12
gen_task_tree.py              _cmd_emit_source                  865     125    25
nopack_sandbox.py             _strip_and_seal                  1093     124    27
assemble_paste.py             main                              247     120    17
audit.py                      run_checks                       5183     118    24
nopack_sandbox.py             run_guarded                      2120     117    26
archive_row_body.py           verify                            768     112    21
audit.py                      check_journal_spine_anchor       4181     112    21
archive_row_body.py           parse_record                      387     108    32
preflight_contract.py         verify                            316     108    23
telemetry_emit.py             emit_event                        552     106    22
gen_task_tree.py              find_incoherences                1001     102     8
audit.py                      _select_active_bundle            2345      99    22
audit.py                      cmd_run                          5717      98    20
nopack_sandbox.py             main                             2343      98    20
verify_handoff_probes.py      _classify                         575      97    24
archive_row_body.py           relocate                          629      94    20
audit.py                      cmd_ship_gate                    6003      93    15
validate_substrate.py         validate_contract                 555      93    18
audit.py                      check_handoff_probes             2447      90    18
audit.py                      check_stale_worktrees            1861      88    10
audit.py                      check_preflight_backlog_ids      4349      87    15
funnel_coverage.py            _main                             686      87    16
nopack_sandbox.py             parse_pipeline                   1428      87    17
audit.py                      _ratchet_findings                3489      86    14
fleet_analytics.py            parse_numstat_stream              223      86    19
validate_adr_status.py        parse_status_fields               300      86    21
preflight_contract.py         check_cited_ids                   811      84    18
funnel_coverage.py            ratchet_findings                  580      83    10
single_flight.py              claim_token                       509      83    16
gen_trend_dashboard.py        collect_commit_gate               621      81     9
audit.py                      supplement_fold_violations       2584      80    14
audit.py                      check_hooks_armed                1954      78    15
archive_row_body.py           main                              888      77    17
fleet_parity.py               resolve_fleet                     479      77    17
validate_adr_status.py        index_effective_status            528      76    24
verify_handoff_probes.py      main                              702      76    27
audit.py                      _git_linked_worktrees            1705      75    16
audit.py                      derive_doc_freshness             1284      72    19
audit.py                      check_doc_code_edge              2889      72    11
audit.py                      check_task_tree_coherence        3654      71     8
audit.py                      check_canonical_freshness        1423      70     4
desired_state_loader.py       _assemble_repos                   223      70    16
gen_task_tree.py              write_tree                        491      70    15
propose_closures.py           render                            177      70    11
propose_closures.py           main                              510      70    14
gen_intake_tree.py            evaluate                          369      69    13
gen_trend_dashboard.py        main                             1296      69    14
file_purpose_graph.py         _load_tasks                       643      68    18
file_purpose_graph.py         _load_consumer_at_landing         557      67    17
gen_lane_contract.py          _check_manifest_contract_agree.  1042      67    11
nopack_sandbox.py             _screen_git                      1827      66    26
audit.py                      check_fleet_audit_replication    3816      65    10
audit.py                      cmd_health                       5900      65    15
fleet_parity.py               main                             1985      65    12
nopack_sandbox.py             provision                         983      65     9
audit.py                      _diff_index                      1106      64    10
audit.py                      check_doc_claims                 2074      64    16
cloud_provisioning.py         seed_self_registration            692      64    10
fleet_parity.py               render_digest                    1749      64    17
validate_doc_claims.py        reconcile                         185      64    13
audit.py                      check_membership_agreement       4115      63    12
funnel_coverage.py            measure                           438      63    15
gen_task_tree.py              main                             1662      63    15
nopack_sandbox.py             _load                            2443      63    10
safe_remove.py                evaluate_removal                  180      63    16
audit.py                      check_supplement_folded          2666      62    17
audit.py                      check_funnel_lifecycle           4745      62     5
check_provider_registry.py    check_s31_council_panel           255      62    15
fleet_parity.py               verdicts                         1007      62    12
fleet_parity.py               emit_events                      1829      62    12
proof_layer.py                scan_guards                       363      62    22
enforcement_coverage.py       _freshness_fire                   609      61    12
file_purpose_graph.py         _load_deploy_manifest             771      61    22
```

That is the complete set of 89. By module: `audit.py` **25**, `fleet_parity.py` 8, `nopack_sandbox.py` 7,
`gen_task_tree.py` 5, `archive_row_body.py` 4, `gen_lane_contract.py` 3, the rest one or two each.
`audit.py` contributing the most long functions while holding a mean CC of ~7 is §1.3 restated: it is long
and broad, not deep. (`gen_lane_contract._check_manifest_contract_agree.` is truncated for column width;
the full name is `_check_manifest_contract_agreement`.)

### §1.3 The finding that matters: length and complexity are different populations

**`audit.py` is the longest module in the tree and is not among its complexity hotspots.** 6,193 lines
across 142 functions is a mean CC of about 7; its worst function is CC 35. The four F-rank functions in the
whole of `scripts/` live elsewhere:

```
fleet_parity.collect_facts          CC 88    201 lines
gen_lane_contract.parse_contract    CC 65    232 lines
fleet_parity.load_manifest          CC 56    159 lines
funnel_lifecycle.measure            CC 41    143 lines
```

A size cap and a complexity gate would select almost disjoint sets here. Any doctrine that conflates them
will aim at the wrong files — which is precisely the ordering error intake #31 §D exists to prevent.

### §1.4 `audit.py` internal coupling — measured, and it is low

AST call-graph closure over `audit.py`'s own top-level names: **130 top-level functions, 6 classes, 32
`check_*` still in the facade.** Helpers reached by **three or more** checks:

```
helper                          reached by   lines
_is_hub                         23 checks        6
_git                             4 checks        7
_index_worktree_divergence       3 checks       29
                                            -------
shared core total                               42 lines
```

**Forty-two lines.** The 6,193-line module is not a tangled ball; it is a facade over ~32 near-independent
organs. Movable lines per check (the check plus helpers only it reaches):

```
check_canonical_freshness       504     check_review_artifact_coverage   156
check_stale_worktrees           251     check_supplement_folded          142
check_silent_rule_ratchet       239     check_doc_code_edge              118
check_membership_agreement      220     check_doc_code_coverage_drift    116
check_handoff_probes            210     check_journal_spine_anchor       112
```

### §1.5 The style surface, as it actually is

`ruff` and `mutmut` are the only real Python-quality config in this repo. `[tool.ruff.lint]` carries
`extend-select = []` and **there is no `select` key anywhere** — no `.ruff.toml`, no `setup.cfg`, no
`tox.ini` — so the live rule selection is ruff's default `E4, E7, E9, F` and nothing else. Confirmed absent
from every real config file: `mypy`, `basedpyright`, `import-linter`, `deptry`, `semgrep`, `radon`,
`complexipy`, `cosmic-ray`, `pep8-naming`, `C901`, `PLR0912`. `.claude/skills/` holds exactly two skills
(`check-against-spec`, `verify`); there is no `python-style` skill.

**The accepted doctrine's own precondition is discharged by this report.** Intake #31
(`docs/intake/2026-08-09-func-code-style-doctrine.md`, status ACCEPTED) ratified §A as the fleet's written
code-style doctrine and §E into the do-not-relitigate register, but the ruling **left the ruff rule-family
list open**, verbatim: *"it is not ruled here, because SecD binds and a family list settled before the
hotspot measurement would be the exact ordering error SecD exists to prevent. SecD BINDS: no refactor row is
born before a hotspot measurement."* §1 above is that hotspot measurement. Its verdict on §B item 1 is in
§3(a) and §4.

### §1.6 What is already RULED — checked row by row, not assumed

Every candidate in §3 is positioned against the live state of these rows. **Two of them are closed with
landed rulings**, which changes what may honestly be proposed:

**OPEN.** `[#609]` (the zero-cost ruff families; explicitly **excludes** C901/PLR0912/0915) · `[#579]`
(code-doctrine ADR merging intakes 31 and 34) · `[#533]` (the `audit.py` decomposition) · `[#528]` (suite
cadence) · `[#597]` (per-check tiering) · intake #58 (status READY) · intake #31 (status ACCEPTED).

**CLOSED — `[#407]`, RULED 2026-08-19.** Verbatim from the row: *"fleet Python doctrine is
**functional-first with dataclasses; classes only for stateful lifecycles; naming = PEP 8**"*, landed as an
in-file amendment at `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md` **§B-4**. That
section says of itself, verbatim: *"**Arms no gate.** `ruff` is configured for lint, not for paradigm;
nothing mechanically refuses a class that should have been a function"*, and *"Prospective, not a refactor
mandate."* **The paradigm and naming questions are settled. They are simply unenforced and have no
point-of-use surface** — which is the gap §3(a) addresses, and it is a different gap from the one the brief
imagined.

**CLOSED — `[#502]`, ADOPTED 2026-08-18.** The verdict is transcribed verbatim in intake #27's Tier-L
ledger row 8 (`docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:29`):

> **ADOPTED (Tier-L, ruled 2026-08-18)** — decision 6 = ADOPT; CI-only (Windows walls: POSIX `resource`,
> `fork`); report-only ratchet; baseline **1210 survivors** on the `fleet_analytics` slice, direction
> **no-growth**; survivor triage **deferred**, trigger post-[#533] / next audit-py batch

Mutation testing is therefore **not an open question, and its gate direction is already ruled**: a
report-only no-growth ratchet on a 1,210-survivor baseline. §3(c) is re-scoped accordingly. Note the last
clause: **the deferred survivor triage is triggered by "post-`[#533]`"** — i.e. by §3(b) landing. The two
candidates are coupled by a landed ruling, not by this report's preference.

### §1.7 What arming the ruled doctrine would actually cost — measured

Measured with the repo's own pinned ruff (0.15.5) this session, `--statistics`:

```
                              scripts/      scripts/ + deploy/
N   (pep8-naming)                   13                      24
      N818 error-suffix-on-exception-name    12              13
      N806 non-lowercase-variable-in-func     1               5
      N815 mixed-case-variable-in-class       0               6
C901 + PLR0912 + PLR0915           134                     166
      C901  complex-structure              78                94
      PLR0912 too-many-branches            37                49
      PLR0915 too-many-statements          19                23
```

Two things follow. **`N` is near-free and arms a ruled doctrine.** ADR-108 §B-4 rules "Naming is PEP 8" and
records that nothing enforces it; ruff's `N` family *is* a PEP 8 naming gate, it costs **13 fixes on
`scripts/`, twelve of them the single mechanical `N818` exception-suffix rename** — and it is **not** in
`[#609]`'s twelve zero-cost families (T203, LOG, G, ICN, INT, SLOT, TID, NPY, W, YTT, ASYNC, FA), so no open
row claims it. **The complexity families are not free**: 134 on `scripts/`, which corroborates the 131
`[#609]` recorded (small drift since that census) and confirms that row's decision to exclude them.

---

## §2 — Survey, sources cited

*Drafted on Fable 5.1. Every tool claim carries a URL and the version/date seen; items the drafting model
could not verify are marked `unverified` and are left marked rather than silently dropped.*

### §2.1 Functional core / imperative shell in Python

**Origin.** Gary Bernhardt, *Boundaries*, SCNA 2012
(https://www.destroyallsoftware.com/talks/boundaries): use plain values as the boundary between components;
push decisions into a mutation-free core and confine I/O and mutation to a thin shell. The named pattern is
his screencast *Functional Core, Imperative Shell*
(https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell; season/date not
shown on the page — unverified). Mark Seemann's *Impureim Sandwich* (blog.ploeh.dk, 2020-03-02) is the
sharpest short statement — gather impurely, decide purely, act impurely — with Seemann's own caveat that he
"never claimed that you can *always* do this."

**Python treatment.** Percival & Gregory, *Architecture Patterns with Python* (O'Reilly, 2020; free at
cosmicpython.com — the site returned 403 during this survey, so chapter numbers are unverified):
Repository (ch. 2), Service Layer (ch. 4), Unit of Work (ch. 6). The move is to make the domain pure and
give every I/O concern a *port* with a real and a fake *adapter*.

**What it buys a codebase whose cost is git subprocesses and tree walks** (judgment, applying the sources):

- **Becomes pure and I/O-free:** parsing `git log` / `git diff --name-status` output into records;
  commit-range and spine logic; task/BACKLOG schema validation; frontmatter parsing; the FAIL/WARN decision
  *given a snapshot of facts*. These get fast deterministic tests against string fixtures, with no repo setup.
- **Stays in the shell:** the `subprocess.run(["git", …])` calls, `os.walk` / `Path.rglob`, file reads,
  exit-code mapping — behind a small `GitPort` protocol with a `FakeGit`.
- **The concrete win here** is that the shape this repo actually has — checks that shell out *and* decide
  inline — becomes **snapshot-then-decide**: one collection pass builds a facts object and checks become
  pure functions of it. That is the same lever as "call git once instead of N times", which §0.5 measured at
  133.7×.

**Costs and critiques.** *Data-shovelling*: everything the core needs must be gathered up front, and
Seemann's commenters note the sandwich fails when a later decision determines which data to fetch — you
over-fetch or accept an impure core. *Over-abstraction*: Percival & Gregory themselves warn that
repositories and UoW add indirection a small script does not repay; for a 40-line shell-out plus a regex,
the shell *is* the program. It does not pay when the logic is trivial relative to the I/O, or when git's
actual output edge cases are the thing most likely to be wrong — fakes then encode your misunderstanding.

**Enforcement.** import-linter 2.15, released 2026-09-04 (https://pypi.org/project/import-linter/).
Contract types per https://import-linter.readthedocs.io/en/stable/: **forbidden**, **protected**,
**layers**, **independence**, **acyclic siblings**, plus custom types. For FC/IS: a `layers` contract with
`shell` above `core`, and a `forbidden` contract keeping `subprocess` and I/O wrappers out of `core`.
**What it cannot check:** it analyses the static import graph via grimp, so it cannot see a
`subprocess.run` inside a function that imports nothing new, cannot see `importlib` or string-based dynamic
imports, and cannot see effects reached through an allowed dependency. It enforces *module topology, not
purity*. Purity has no Python gate; the practical proxy is "core tests need no `tmp_path`, no `subprocess`,
no monkeypatched I/O".

### §2.2 LLM-readable code practices — evidenced vs folklore

**Measured (real studies).**

- **Position and length degrade retrieval.** Liu et al., *Lost in the Middle*, TACL 2024
  (https://aclanthology.org/2024.tacl-1.9/): accuracy is highest when relevant content sits at the start or
  end of context and drops in the middle. Modarressi et al., *NoLiMa*, ICML 2025
  (https://arxiv.org/abs/2502.05167): where the needle lacks lexical overlap with the query, 11 models fall
  below 50 % of their short-context score at 32K tokens. Chroma, *Context Rot* (Hong, Troynikov, Huber,
  2025-07-14, https://www.trychroma.com/research/context-rot): 18 models, reliability falls with input
  length even on trivial tasks.
- **Code specifically.** Rando et al., *LongCodeBench* (arXiv 2505.07897, 2025): Claude 3.5 Sonnet drops
  from 29 % to 3 % as context scales to 1M tokens; Qwen2.5 70.2 % → 40 %. This is repository-level context,
  **not** a study isolating file size. **No study isolating "file size" as the independent variable was
  found.** The evidence is that *total tokens loaded* hurts; small files follow only indirectly.
- **Vendor guidance — experience-based, not controlled study.** Anthropic, *Best practices for Claude Code*
  (https://code.claude.com/docs/en/best-practices, current 2026-09-05): "LLM performance degrades as context
  fills"; CLAUDE.md should carry only what Claude "can't guess" and exclude "file-by-file descriptions of
  the codebase"; "Bloated CLAUDE.md files cause Claude to ignore your actual instructions." Anthropic,
  *Effective context engineering for AI agents* (2025-09-29): "find the smallest set of high-signal tokens."
  Neither publishes effect sizes.
- **AGENTS.md** (https://agents.md/; OpenAI, Aug 2025; stewarded by the Linux Foundation's Agentic AI
  Foundation, announced Dec 2025) is a convention with adoption numbers, not a study.

**Practitioner consensus only.** Module header/docstring blocks are plausible via the retrieval results
(a summary at the top of a file lands at the "start" position) but no study was found. On **small pure
functions vs deep modules**: the retrieval evidence favours *reading less*, which pushes toward small units,
while Ousterhout (*A Philosophy of Software Design*, 2018) argues a deep module with a small interface
reduces what a reader must load. These reconcile if the unit of reading is the **interface** — a deep module
usable from its signature and docstring is cheaper than ten shallow ones. The tension bites only when the
agent must *edit* the deep module's body, where a 6,193-line file is loaded partially and "lost in the
middle" applies. **Judgment: file size matters for edit safety more than function size does.** Typed errors
over silent returns, and explicit naming, have no LLM-specific study; the argument is that an agent verifies
by running checks, and a loud failure is a check while a `None` is not.

**Net: the evidence is thin beyond "less context, front-loaded, high-signal."** Everything else here is
reasoned convention and is labelled as such.

### §2.3 Mutation testing usable as a Linux-codespace nightly

- **mutmut 3.7.0**, 2026-07-31 (https://pypi.org/project/mutmut/, https://mutmut.readthedocs.io/). Requires
  `fork()`: "if you want to run on windows, you must run inside WSL." Runs a stats pass to learn which tests
  exercise which function, stores mutants and results in `mutants/`, resumes where it stopped, and on re-run
  only re-tests mutants in functions whose source changed. Per-mutant timeout =
  `(duration_of_original_tests + timeout_constant) × timeout_multiplier`. Parallelism config was not visible
  in the fetched docs — unverified.
- **cosmic-ray 8.7.0**, 2026-08-09 (https://github.com/sixty-north/cosmic-ray/releases; Python 3.9+,
  Windows-capable per README badges). Workflow `init → baseline → exec → report`; the session is a SQLite
  file; work is farmed out via a distributor (`local` or `http`; Celery was the older model). Docs pages
  404'd during the survey, so distributor details are **unverified at this date**.
- **mutatest 3.1.0**, 2025-02-20 (https://github.com/EvanKepner/mutatest/releases): AST-level mutation with
  coverage-file filtering, no `fork()` requirement; lighter, less maintained.

**Cost model.** `runtime ≈ mutants × test-subset-time ÷ parallelism`, plus timeout drag. Controls: scope
`source_paths`/`only_mutate` to one module; coverage-guided test selection (mutmut does this automatically);
incremental re-runs against the cached baseline; workers; a tight timeout multiplier.

**Worked example** — generic; **this repo's own measured constants are in §3(c)** and are far cheaper per
mutant than this illustration (~2,000 mutants, scoped subset 10 s): serial 2,000 × 10 s = 20,000 s ≈ 5.6 h. Four cores
≈ 1.4 h. If selection cuts the average subset to ~2 s: ≈ 4,000 s serial, ≈ 17 min on four cores. An
incremental nightly where ~5 % of functions changed: ~100 mutants × 10 s ≈ 17 min serial. If 5 % of mutants
hang against a ~3× cap (30 s), add ~50 min serial. The full-suite figure is irrelevant as the per-mutant cost
**if scoping is honoured** — unscoped, 2,000 × 330 s is 7.6 days.

**What the score is.** Killed ÷ generated (minus equivalents) measures whether the *selected* tests detect
*these operators'* small syntactic changes in *this* module. It is evidence of assertion strength and a good
finder of tests that execute without asserting. It is **not** evidence of correctness, not evidence of
coverage of real fault classes, and not comparable across modules with different operator mixes. Equivalent
mutants inflate the denominator, and a score target invites the recorded Goodhart failure — tests written to
kill mutants rather than to specify behaviour.

### §2.4 When a Rust / compiled extension is justified

**Decision rule** (judgment, consistent with every cited tool's own framing): compile only when a *profiled*
CPU-bound hot path in pure Python dominates wall time, survives an algorithmic fix, and has no existing
native library. Three counter-cases come first:

- **Subprocess-bound** — this repo's profile. The cost is process spawn plus git's own work; Rust around it
  changes nothing. The fix is batching.
- **I/O-bound** — tree walks are syscall-bound; `os.scandir`, `git ls-files`, or ripgrep 15.2.0 (2026-07-15,
  https://github.com/BurntSushi/ripgrep/releases) already exist.
- **Cacheable** — a nightly that recomputes a stable answer is a caching bug, not a language bug.

**Options and cost.** *Swap in a native library* — zero build cost: orjson 3.12.0 (2026-08-14,
https://pypi.org/project/orjson/; claims ~10× dumps, ~2× loads vs stdlib), polars 1.44.1 (2026-08-26),
rustworkx (0.18.1 confirmed newest; date unverified — and already a declared dependency here, at graph sizes
far too small to matter). *Cython 3.3.0* (2026-08-22, https://pypi.org/project/Cython/): its own tutorial
reports 2× from compiling unchanged Python and 13× after adding static types; needs a C compiler on every
contributor machine or prebuilt wheels. *PyO3 0.29.2 + maturin 1.15.0* (PyO3 release date inconsistent in
search results — unverified; maturin 2026-08-24, https://pypi.org/project/maturin/): a Rust toolchain per
contributor, or a wheel per platform × CPython version via cibuildwheel. pydantic-core's "5–50× faster than
v1" (https://pydantic.dev/docs/validation/latest/blog/pydantic-v2-alpha/, 2023-04-03) is the widely quoted
number and applies to a tight validation loop over millions of objects, not to a script that waits on git.

**Realistic speedups.** Vendor and project self-reports cluster at **2–15×** for compiled hot loops and up
to ~50× for validation cores. No number from those sources transfers to code whose wall time is subprocess
or filesystem latency; the only honest figure for this repo is the one a profiler produces first — and §0
produced it.

---

## §3 — Candidates (Z-C; no rows filed, no ids minted)

Each item is a CANDIDATE in the ADR-111 sense: a proposal for the browser architect to triage, with its
pass/fail criterion stated ex-ante per ADR-108 §B. Where an open row already owns the ground, the candidate
says so. Every number is MEASURED (this session or a cited landed audit) or PREDICTED with arithmetic shown.

### (a) A `python-style` skill plus one size-cap ratchet with a grandfather list

**Statement.** A `.claude/skills/python-style/SKILL.md` (≤ 60 lines) carrying the module header-block
template, size caps, naming and error posture — paired with **one bespoke AST detector** that ratchets
module and function size against a baseline file on the `ecosystem/audit-title-baseline.json` shape.

**Evidence.** §1: 94 modules / 53,748 lines / 1,620 functions; 17 modules over 800 lines; 89 functions over
60 lines; radon average **B (5.20)** over 1,808 blocks with four F-rank functions. §1.3: length and
complexity are near-disjoint populations here.

**What the cap is for, said plainly.** It is a proxy for **LLM edit-safety and review surface**: a 6,193-line
module cannot be held in one edit's context (§2.2), and a 232-line function cannot be diffed on one screen.
It is **not** a claim that shorter is better — the accepted doctrine is Ousterhout's deep-modules-over-
thin-layers and it explicitly rejects Clean Code's very-short-function rule. The cap bites only new code.

**Cap numbers, from the measured distribution.** The grandfather count at each candidate cap is the design
input, and all of these are MEASURED, not estimated:

```
module cap   grandfathered        function cap   grandfathered (of 1,620)
> 600 lines       25              >  60 lines          89
> 800 lines       17              >  80 lines          46
> 1000 lines      13              > 100 lines          27
> 1200 lines       9              > 120 lines          18
> 1500 lines       4              > 150 lines          10
> 2000 lines       3              > 200 lines           4
```

Proposed starting point **800 / 100**: a baseline of 17 + 27 = **44 entries**. (The Fable draft proposed
800/60 = 106 entries; on the measured distribution 100 lines is the better knee — it captures every function
the doctrine would actually call oversized while cutting the register by 62, and it does not put 43 routine
60–100-line functions on a debt list that no one will ever clear. The architect may prefer the tighter pair;
both counts are given so the choice is made on numbers.)

**Ruff or bespoke? Bespoke.** Three reasons. (1) Ruff carries **no module-length rule at all**, and its
function-size rules are `C901`/`PLR0912`/`PLR0915` — complexity and statement counts, which `[#609]`
explicitly excludes (131 hits) and which the doctrine records as a contested predictor; adopting them here
would overturn a deliberate exclusion. (2) Ruff's only grandfather mechanism is `per-file-ignores` or
in-source `# noqa`, which means source edits and a debt register living in the code. (3) The repo already
runs five baseline-file ratchets (`audit-title`, `silent-rule`, `proof-layer`, `audit-funnel`,
`audit-consumer`); a sixth on the same shape is the existing pattern, not a new abstraction.

**Baseline shape.** `ecosystem/python-size-baseline.json` with `measurement` (prose describing exactly what
was counted), `detector` (the function name), and entries keyed `path` or `path::qualname` — the
`audit-title-baseline.json` triple, unchanged.

**SKILL.md headings (≤ 60 lines).** frontmatter · When this fires · Module header block (template) · Size
caps (numbers plus "see the baseline file; never add an entry") · **Paradigm and naming — transcribed from
ADR-108 §B-4, deciding nothing new**: functional-first with dataclasses, classes only for stateful
lifecycles, naming is PEP 8 · Error posture (exit codes vs raise; the FAIL/WARN vocabulary) · What this
skill does NOT enforce (complexity, typing — owned elsewhere).

**The skill's real justification, which is stronger than the brief assumed.** ADR-108 §B-4 rules the
paradigm and naming doctrine and then says of itself, verbatim, *"Arms no gate."* Intake #31 §A ratified the
written style doctrine and gated nothing. So there are **two landed rulings with no point-of-use surface
anywhere an agent will encounter them** — and `.claude/skills/` currently holds two skills, neither about
Python. That is the gap: not an undecided question, but a decided one with no carrier.

**A separate, near-free companion (stated as its own sub-candidate).** §1.7 measured ruff's `N` family at
**13 violations on `scripts/`, twelve of them one mechanical `N818` rename**. `N` *is* a PEP 8 naming gate,
it arms exactly the half of §B-4 that the ADR says nothing enforces, and it is absent from `[#609]`'s twelve
zero-cost families, so adopting it claims no other row's ground. **Ex-ante criterion:** `ruff check --select
N scripts/` is clean at HEAD after 13 fixes, and `N` is added to `extend-select` in the same commit. This is
the cheapest mechanization named anywhere in this report.

**Ex-ante pass/fail.** (i) The detector over `scripts/` at HEAD emits exactly the baseline entries and
nothing else — RED before the baseline file exists, GREEN after. (ii) A fixture with a 101-line function
trips it; the same fixture at 100 does not. (iii) Deleting a baseline entry for a still-oversize target
trips it. (iv) An entry that drops below cap is pruned in the same commit or the gate WARNs — the ratchet
only shrinks. (v) SKILL.md ≤ 60 lines, byte-gated the way `tests/test_claude_md_byte_cap.py` gates
`CLAUDE.md`.

**Cost.** One AST pass over 94 modules — the same pass that produced §1, one parse per module, not per rule.
Gate-context cost UNMEASURED.

**Positioning.** Complement to `[#609]`, which keeps its zero-cost families and its C901/PLR exclusion.
**Evidence for intake #31 §B**, whose ruling left the family list open pending a hotspot measurement: this
report is that measurement, and its verdict is that the size/complexity families should **not** be adopted
as blocking rules (§4). Naming and paradigm are **not deferred and not decided here** — they are ruled, at
ADR-108 §B-4 via the closed `[#407]`; the skill transcribes that ruling to a point of use and adds nothing.
`[#579]` (open) is the broader code-doctrine ADR that would eventually absorb both.

**Risks.** Goodhart is the master risk and it is on the record: an agent will split a 900-line module into
two 450-line files to dodge the cap, and the ratchet cannot see that. The honest mitigation is that (b)'s
map is authored by **measured coupling, never by the cap**, and a split whose halves share more than the
42-line core is a review finding. Second: a tight function cap invites thin wrappers — the exact
anti-pattern the doctrine rejects — which is why 100 is proposed over 60, and why the caps section must say
so in the skill itself.

### (b) An `audit.py` decomposition MAP by measured coupling — no rewrite

**Statement.** Extend `[#533]`'s existing `scripts/audit_checks/` package (PEP-420 namespace package, 22
checks already extracted, `_common.py`, `registry.py`) with an ordered unblocking plan whose content is:
**the blocker is the test monkeypatch surface, not source coupling.**

**Evidence.** §1.4 — 130 top-level functions, 32 `check_*` in the facade, and only **three helpers totalling
42 lines** reached by three or more checks. `registry.py`'s own criterion is the authority and is quoted,
not reinvented: *"A check can be moved only if nothing in its transitive dependency closure is monkeypatched
onto the `audit` module by a test."* It records that **25 of 43 fail that test, `_is_hub`/`_REPO_ROOT` alone
accounting for 19**, and it records the honest limit: *"nothing currently asserts that `CHECK_ORDER` still
agrees with `audit.ALL_CHECKS`."* The sixteen names `tests/` patches onto `audit` are enumerated in that
docstring.

**Ordered unblocking.**

0. **Precondition — close the honest limit.** Add the test asserting `CHECK_ORDER == audit.ALL_CHECKS` as an
   ordered list. `CHECK_ORDER` is the emission order and therefore part of the byte-identical output contract
   the git hooks depend on; every later step is unverifiable without it. Pass criterion: the test REDs on a
   permutation or a missing entry.
1. **One seam change frees 19.** Make `_is_hub()` and `_REPO_ROOT` **late-bound** — resolved at call time
   through the `audit` module attribute rather than imported by value — so the patched names keep landing
   where the tests put them. Minimal diff, zero test edits. The alternative (repointing every patch site at
   `_common`) is a larger diff and a review obligation on `tests/`, which `[#533]` recorded as out of scope.
2. **`check_handoff_probes` needs a second, independent fix.** It reaches `_gitenv`, which `audit.py` loads
   **by path** via `Path(__file__).resolve().with_name("gitenv.py")` — position-dependent, so a module under
   `audit_checks/` would resolve to a file that does not exist. Expose `_gitenv` from `_common`, anchored
   once at the `scripts/` root. Do this in the same arc as §0.5's one-spawn fix: `_select_active_bundle` is
   25.2 s of that check's 25.5 s, and the batched form agreed on all 118 add-dates and picked the identical
   bundle (MEASURED). `CLAUDE.md` §1 names three consumers of that selector (`verify_handoff_probes`,
   `check_handoff_probes`, `validate_residual_completeness`) — one fix, three beneficiaries.
3. **Batches by movable lines** (§1.4), each admitted only when the closure test says movable.
   **Batch 1:** `check_canonical_freshness` 504, `check_stale_worktrees` 251, `check_silent_rule_ratchet`
   239, `check_membership_agreement` 220. **Batch 2:** `check_handoff_probes` 210 (after step 2),
   `check_review_artifact_coverage` 156, `check_supplement_folded` 142, `check_doc_code_edge` 118. The
   42-line shared core goes to `_common.py`, with `_git` staying patch-compatible.

**Ex-ante pass/fail.** Per batch: `audit.py health` stdout at HEAD before and after the move diffs to **zero
bytes** (golden run, same tree); the step-0 test stays GREEN; the registry's movable count rises by exactly
the batch size; targeted tests for the moved checks GREEN in the lane, full suite once at integration
([#528]).

**Predicted numbers.** The eight named checks total 504+251+239+220+210+156+142+118 = **1,840 lines**;
`audit.py` 6,193 → ~4,353 (**−29.7 %**), PREDICTED. That does not reach (a)'s 800-line cap and stays
grandfathered — **the map is by coupling, not by cap**, which is the point. Wall-clock effect of step 2:
25.2 s − 0.35 s ≈ **24.9 s saved of 75.8 s (→ ~50.9 s, −33 %)**, PREDICTED from the MEASURED A/B. Note the
two runs disagree on per-spawn cost (0.099 s in the profile vs 0.393 s in the loaded A/B) — they agree on
shape, not on absolute spawn price, and the prediction uses the profiled figure.

**Positioning.** Evidence and a sequence for `[#533]`, which owns the decomposition; nothing here supersedes
its criterion. The perf leg is evidence for whichever row owned the 2026-08-26 w2a arc, whose `< 60 s` target
is still MISSED.

**Risks.** A move that relocates lines to satisfy (a) rather than the closure test is the Goodhart split; the
ordering above exists to prevent it. The late-binding seam is a behaviour change at import time — step 0 and
the golden diff are its witnesses.

### (c) Mutation testing as a codespace nightly — the gate is ALREADY RULED, and not on suite time

**Statement.** Schedule `[#502]`'s **already-adopted** mutmut ratchet as a codespace nightly. Do **not**
re-decide its direction, and do **not** gate it on suite time.

**The brief's gate is superseded, not merely marginal.** §1.6 records the landed verdict: *report-only
ratchet; baseline 1210 survivors on the `fleet_analytics` slice, direction **no-growth**.* **A gate
direction is already ruled** — survivor count must not grow — so proposing "gated on suite < 300 s" would
overwrite a ruling with a worse quantity. It is also the wrong quantity twice over: (i) measured suite walls
are codespace **294.07 s / 298.50 s / 311.24 s**, straddling 300 s on run-to-run noise, and local **897.22 s**
— a gate that flips on noise is not a gate; and (ii) mutmut runs the *selected test file* per mutant, not
the suite, so the cost driver is `mutants × seconds-per-mutant` and the full-suite wall does not appear in
that product at all.

**The real cost model, from the pilot's own landed run.** `docs/audits/2026-08-18-technical-502-mutmut-
attribution.md` records the successful run: **2,291 mutants, 2,291 of 2,291 checked, 1,210 survived,
`mutmut run` exit 0, 9m28s against the workflow's declared 30-minute budget.** Those 2,291 mutants come from
the `only_mutate = ["*fleet_analytics.py"]` slice — one module of 1,264 lines. That gives two measured
constants:

```
mutants per line     2,291 / 1,264   = 1.81
seconds per mutant   568 s / 2,291   = 0.248
```

Applied to §1's census (all figures PREDICTED from those two MEASURED constants):

```
scope                        lines    ~mutants   ~wall        verdict vs 30-min budget
fleet_analytics.py (today)   1,264       2,291   9m28s        MEASURED — fits
gen_lane_contract.py         1,137       2,058   8m30s        fits
fleet_parity.py              2,054       3,718   15m22s       fits
audit.py                     6,193      11,209   46m20s       EXCEEDS
all of scripts/             53,748      97,284   6h42m        far exceeds
```

**So the tree is not mutable in one nightly, and the two modules §1.3 identified as the genuine complexity
hotspots both are.** `fleet_parity.py` (CC 88 and CC 56) and `gen_lane_contract.py` (CC 65) each fit inside
the existing declared budget — and they are precisely where a surviving mutant would mean something, because
complexity without assertion strength is the combination that hides defects.

**The widening trigger has already fired — or is about to.** The ruling defers survivor triage with the
trigger *"post-`[#533]` / next audit-py batch"*. `[#533]` is §3(b). **These two candidates are coupled by a
landed ruling, not by this report's preference**, and (b) is the one that unblocks (c).

**Gate criteria that respect the ruling (ex-ante).** (i) Keep **report-only, never blocking** — the ruling
says so explicitly and nothing in this measurement argues otherwise. (ii) **`not checked == 0`**, else FAIL
the *report*, because a green report with unchecked mutants is the recorded failure mode, twice. (iii)
**Survivor count ≤ the committed baseline** (1,210 for the current slice; a new baseline per module on first
run), direction no-growth — this is the ruled criterion, restated, not a new one. (iv) The **selected test
file** for each mutated module passes at HEAD on the codespace substrate — this matters because the suite
currently carries **13–17 failing tests** on both substrates, and mutmut requires a green baseline; keying on
the selected file rather than the suite makes the nightly independent of that red tail. (v) `mutants ×
seconds-per-mutant ≤ the declared 30-minute budget`, computed per module from the table above.

**The two-defects warning, kept.** A `-p no:xdist` attempt once made every mutant's pytest exit 4 on
`unrecognized arguments: -n` and reported all 84 mutants `not checked` while looking green; separately a
module-name mismatch produced 0 of 2,291 checked. *Two different defects presented as one indistinguishable
output.* That is why criterion (ii) is not optional.

**Positioning.** Schedules an **adopted** mechanism; decides nothing `[#502]` left open. One stale artifact
found in passing: `.github/workflows/report-only-wall.yml:223-224` still reads *"UNGATE WHEN [#502] LANDS ITS
VERDICT"* — the verdict landed 2026-08-18 and the file has not been touched since 2026-08-07, so **the
comment's premise is stale**. Its prescribed action, however, is deliberately deferred behind `[#533]`, not
forgotten — so this is a comment fix, not an ungate.

### (d) Rust / compiled extension — **none, measured**

**Statement.** No compiled candidate is justified by the profile. The arithmetic rules it out.

**Arithmetic, from the clean run** (§0.2, un-profiled, so CPU is not inflated):

```
wall                        75.778 s
blocked on children         56.888 s   75.1 %
own Python CPU              19.312 s   25.5 %
_winapi.CreateProcess       15.851 s   20.4 %           (profiled run: 160 spawns / 77.6 s wall)
largest single Python line   4.414 s    5.8 % of wall   journal_anchor._introduced_from_map
```

**Zeroing 100 % of Python CPU leaves a 56.9 s floor: the ceiling for compiling absolutely everything is
75.778 / 56.888 = 1.33×.** Against that, one batched git call in one function measured **133.7×**. On
`ship-gate` the case is stronger still — **78.5 %** blocked on children (clean run), with 29.4 % of wall in
`CreateProcess` alone. The largest single Python tottime line in `health` is 5.8 % of wall, over 494 calls at 8.9 ms each —
a per-call rebuild shape, which is a memo's job, not a compiler's.

**What would have to be true.** A single CPU-bound Python line at ≥ ~40 % of wall **after** the spawn and
re-parse fixes land, with no algorithmic fix remaining — and then a compiled dependency would have to clear
"no new deps without confirmation" plus a Windows build chain under an exactly-pinned `uv`. Nothing in this
profile approaches that bar.

**The one thing that IS CPU-bound, and why caching beats compiling.** Source is re-parsed and re-tokenized
**per rule**. In `ship-gate`: `validate_doc_code_edge.find_code_sites` runs 32 times and drives
**10,378,383 `tokenize` calls (21.8 s tottime, 62.1 s cumulative)**; `builtins.compile` 186 calls;
`ast.iter_child_nodes` 1.38 M calls. In `health`: `ast.walk` 690,178 calls (5.94 s cumulative),
`builtins.compile` 166 calls over 94 modules. **Parse once per blob, walk once.** This repo has already
recorded the identical case and its fix — `build_edge_index` re-tokenizing per rule, **14.53 s → 0.75 s**.
The same shape applies to reads: 5,191 of 5,985 opens in `health` (86.7 %) and 15,356 of 15,578 in
`ship-gate` (98.6 %) are re-opens; a read cache is worth roughly 1.7 s in `health` and materially more in
`ship-gate` (PREDICTED, from `_io.open` at 2.92 s / 6,329 calls and 13.68 s / 18,213 calls respectively).
Compiling would make the redundant work faster; caching removes it.

---

## §4 — What NOT to do, and why (measured)

**Don't parallelise the check registry.** `docs/audits/2026-08-18-technical-533-leg2-measurements.md`
measured one check at 63.2 % of wall and capped whole-registry speedup at **~1.58×** (Amdahl). Today's
profile has the same shape — two checks own 55 % of `health`, and one owns 56.3 % of `ship-gate`.
*Consequence:* parallelism buys less than the single one-spawn fix and adds contention on spawn cost, which
already varied 4× between runs (0.099 vs 0.393 s/spawn).

**Don't rewrite `audit.py`.** Only **42 lines** are shared by three or more checks; the movability blocker
is sixteen test-patched names, not source coupling. *Consequence:* a rewrite would re-derive the 22
extractions `[#533]` has already landed, at the cost of the byte-identical output contract the hooks depend
on.

**Don't chase cyclomatic complexity fleet-wide.** radon: average **B (5.20)** over 1,808 blocks, **four**
F-rank functions in the entire tree, and CC is recorded doctrine as a contested predictor (Shepperd 1988) —
a triage smell combined with churn, never proof. *Consequence:* complexity work here is four named
functions, not a sweep.

**Don't adopt `C901` / `PLR0912` / `PLR0915` as a blocking gate now.** Measured this session with the
pinned ruff: **134 on `scripts/`** (C901 78, PLR0912 37, PLR0915 19), **166 including `deploy/`** —
corroborating the 131 `[#609]` recorded and confirming that row's deliberate exclusion. §1.3 shows they
select a nearly disjoint set from the modules that actually cost anything. *Consequence:* the gate would
fire on non-hotspots and teach agents to split functions to silence it — the Goodhart failure already on the
record. Contrast `N` at 13.

**Don't add a type checker as the first move.** mypy and basedpyright are absent from every real config
file; the landed census counts ANN at 302 non-test / 6,910 tree-wide and 141 dict-returning functions; and
the profile attributes **zero** measured cost to type errors. *Consequence:* the first year of a type checker
is annotation labour on a codebase whose measured pain is spawn count.

**Don't compile anything.** 75.1 % of `health`'s wall and 78.5 % of `ship-gate`'s is blocked on child
processes; `CreateProcess` alone is 20.4 % and 29.4 %; the largest Python line is 5.8 %. The compiled ceiling
is **1.33×** against a **measured 133.7×** from one batched git call. *Consequence:* see §3(d).

**Don't set a length cap without its ratchet and its coupling companion.** A bare 800-line cap has 17
modules over it today, and the recorded Goodhart risk is that agents split files to dodge a cap the detector
cannot see through. *Consequence:* (a) without (b)'s coupling-authored map is a thin-layer generator, which
is the one thing the accepted doctrine explicitly rejects.

**Don't trust `~1.4s` at `.pre-commit-config.yaml:284`.** Every landed measurement contradicts it: 290.9 s
phase-0 median, 140.1 s post-fix, 75.78 s this session's clean commit tier. *Consequence:* a one-line doc
fix, DISCHARGED-class, not a row.

**Don't widen `only_mutate` to `scripts/`.** From the pilot's own measured constants — 1.81 mutants/line
and 0.248 s/mutant — the whole tree is **≈97,300 mutants ≈ 6 h 42 m**, and `audit.py` alone is ≈46 minutes,
both past the declared 30-minute budget. *Consequence:* widen to `fleet_parity.py` (≈15m22s) and
`gen_lane_contract.py` (≈8m30s) — the two genuine complexity hotspots, both inside budget — and nowhere else
until a number says so.

**Don't re-decide what is already ruled.** `[#407]` closed 2026-08-19 with the paradigm and naming doctrine
(ADR-108 §B-4) and `[#502]` closed 2026-08-18 with an ADOPT and a no-growth survivor ratchet. Both were
described as open questions in this arc's brief and in the first drafts of §3. *Consequence:* the honest
work here is **arming ruled doctrine that arms no gate**, not re-opening it — which is why §3(a)'s cheapest
item is a 13-fix `N` adoption and §3(c) schedules rather than decides.

**Don't propose a gate direction where one is ruled.** The brief asked for mutation testing "gated on
suite < 300 s". The landed ruling already sets the direction — report-only, no-growth on 1,210 survivors —
and suite wall does not appear in mutmut's cost product at all. *Consequence:* a proposal keyed on suite time
would have overwritten a ruling with a noisier and less relevant quantity.

**Don't read a green mutation report as evidence.** Two independent defects — the exit-4 `-n` mismatch and
the module-name mismatch — each produced 0 checked behind a green surface. *Consequence:* `not checked == 0`
is the assertion; the kill rate is not.

**Don't micro-optimise any check before the one-spawn fix lands.** 46.03 s saved, behaviour-preserving on
all 118 add-dates, versus a parse cache bounded at ~7.1 s in `health` and a read cache at ~1.7 s.
*Consequence:* order of operations is most of the optimisation.

**Don't grandfather size violations with in-source `# noqa`.** At an 800/100 cap that is 44 source edits,
and the debt register would live in the code rather than in `ecosystem/`. *Consequence:* the baseline-file
shape already wired for five ratchets is the precedent; use it.

**Don't answer `check_review_artifact_coverage`'s 367 s by retiering it out of `ship-gate`.** It is 56.3 %
of the full gate and the obvious temptation, but `[#597]` (open) carries a binding constraint: *"MEASURE-FIRST
is binding: no check is retiered without a number… a check demoted without a number is a defect, not a
shortcut — and NO check is made faster by being made weaker."* Its cost is 1,064 `journal_anchor._git` calls
— the same per-item-spawn shape as §0.5, and therefore the same fix. *Consequence:* batch its git calls;
do not move it to a tier where it stops running.

**Don't treat `audit.py`'s length as the performance problem.** It is the longest module in the tree and its
size is close to irrelevant to its runtime — its cost is 159 git spawns in `health` and 1,303 in
`ship-gate`. *Consequence:* the decomposition in (b) is a **readability and edit-safety** change with a
performance leg attached, and must be argued and measured as such, not sold as a speed-up.

---

## Provenance

Measured on `main` @ `3200757d` in worktree `worktree-research-python-quality`, 2026-09-05, on the local
Windows workstation, and landed on `main` @ `09f80530`. The two differ because concurrent sessions merged
while this lane was measuring; the lane was fast-forwarded (no merge commit, zero lane commits) after
`journal_spine_anchor` was diagnosed as lane-lag rather than a real gap — main's own JOURNAL already
anchored both merges, and the predicate came back clear in both trees afterwards, so **no gate was
bypassed**. Instrumentation harnesses, the raw cProfile dumps, the full subprocess argv logs, the
94-module census JSON and the coupling JSON were produced in this session's job scratch directory and are
**not** committed — every number above is reproducible from the method in §0.1 and the commands named
throughout. No file outside `docs/audits/` was modified by this lane; it is read-only by contract.
