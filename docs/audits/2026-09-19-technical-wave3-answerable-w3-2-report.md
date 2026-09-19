# W3-2 wave3-answerable — `list` verb, `/why` + `/spine` commands, discovery measurement

Lane contract: `2026-09-19-technical-wave3-answerable-lane-contract.md` (frozen). Base `main` @ `8b474f64`.
Model: sonnet (execute, medium).

## PRE-REGISTRATION (written and committed BEFORE the first child run)

**Exact task prompt** (stdin, verbatim, all 5 runs identical; the harness prepends nothing else):

```
Do not edit anything; answer in a few sentences.

TASK: I am thinking of deleting scripts/block_ff_push.py as cleanup. Before I do, tell me what that file is for and whether anything else in this repo depends on it.
```

The prompt does not mention `why`, the graph, commands, skills or tools.

**Counting rule.** A session counts iff its stream-json transcript shows EITHER
(A) a `Skill` tool_use whose input names `why` (or a slash invocation `/why`), OR
(B) a `Bash` tool_use whose command contains `file_purpose_graph.py` followed by `why` or `list`.
Sub-counts reported separately (A, B; a session with both counts once in the total, once in each sub-count).
**Bar: >= 3/5. Raw count reported unrounded. A miss is a result: no re-wording, no re-run.**

**Harness.** Child = `claude -p --setting-sources project --model sonnet --output-format stream-json
--verbose --max-turns 15 --no-session-persistence`, prompt on stdin (stdin then closed), tools
allowed `Bash,Read,Grep,Glob,Skill`, denied `Write,Edit,NotebookEdit,WebFetch,WebSearch`.
cwd = a **scratch copy** of this worktree's committed tree (`git archive HEAD`) with
`.claude/settings*.json` and hooks removed — NOT the live worktree (memory
`child-claude-p-harness-stdin-and-setting-sources`: a child in a live worktree adopts the repo's
hooks and writes to its index). The scratch copy carries `.claude/commands/why.md` and `spine.md`.
**Deviation from the contract's "run from this worktree's root", declared here:** the copy has the
same commands at the same relative path; the live tree is unsafe to point a child at.
**Self-test (6th, control run):** same harness, prompt "List the slash commands and skills
available to you, names only." Must show `why` and `spine`, else the instrument never loaded what
it tests and the 5 results are void (reported as such, not as 0/5).

---

## What changed

- `scripts/file_purpose_graph.py`: new `list` subcommand (no new script). `list_nodes()` walks the
  built graph once; purpose via the shared `_purpose_of`; edges = out-degree and consumers =
  in-degree, i.e. exactly what `why` lists. Header row + tab-separated rows. A missing purpose
  prints the literal token `NO_STATED_PURPOSE` (`why` still prints its prose constant
  `<no stated purpose>`; the dump uses the token so it is machine-greppable).
- `tests/test_file_purpose_graph.py`: 2 tests, committed RED first (`490bc870`, output verbatim in the body).
- `.claude/commands/why.md`, `.claude/commands/spine.md`: one-line `description:`, bodies run the real commands.

## Acceptance (a): `list` timing — RAW

```
run 1 : 22.7664893 s
run 2 : 23.9064324 s
run 3 : 22.9606217 s
```
Bar < 30 s: **met** (but ~all of it is the graph build, not the dump; 23 s is not a large margin on a loaded box).

Counts:
- `list` rows: **2972** (excluding the header) — equals `stats` nodes **2972** (contract cited 2,973 at base; 1 fewer here).
- `git ls-files | wc -l`: **3623**. The operator's "3,620" is ~this figure.
- Composition of the 2972: 2555 tracked files · 410 virtual nodes with no path (task/adr/rule/carrier keys; printed by key) · 7 untracked on-disk paths (`.claude/settings.local.json`, `ecosystem/*/state.yaml` ...).
- **1068 tracked files have no node** (docs 751, tests 154, ecosystem 81, templates 36, deploy 18, protocols 6, logs 4, tasks 2). By design: the graph's population is "files some governed input names". **Not widened here — OPEN (scope change).** Any "list every file" ask needs that decision first.
- 66 rows are `NO_STATED_PURPOSE`.

## Acceptance (b): discovery, 5 fresh Sonnet sessions — RAW

Pre-registration above was committed (`c52451ce`) before any child ran. Harness exactly as registered.

- Control (self-test): child's init lists slash commands `spine` and `why`; its answer lists both. **Instrument loaded the commands** — results are valid.
- **Total: 0 / 5.** Sub-counts: (A) Skill/slash `why` = **0**; (B) Bash `file_purpose_graph.py why|list` = **0**. **Bar >= 3/5: MISSED.**
- What all five did instead: `Grep`/`Glob` for `block_ff_push`, then `Read` of the script and `.pre-commit-config.yaml` (4–7 tool calls each; no Bash at all).
- Per the contract a miss is a result: the prompt was not re-worded and not re-run.
- Confound worth recording, not excusing: the prompt names the exact file, so a direct grep is an obvious first move; a task with an unknown starting point might behave differently. That is a different experiment.

Child-session tokens (5 runs, from result usage), separate from mine:
```
run1 in 6  out 1561 cache_create 12419 cache_read 118153
run2 in 6  out 1381 cache_create 33207 cache_read  96185
run3 in 8  out 1735 cache_create 33440 cache_read 142203
run4 in 6  out 1537 cache_create 12465 cache_read 119543
run5 in 6  out 1644 cache_create 18011 cache_read 120000
fresh (in+out+cache_create) = 117,432 ; control run additional: out 428, cache_create 38,232
```

## Handback checks

- Impacted tests: `tests/test_file_purpose_graph.py`, **37 passed**. Free memory measured immediately before: **10,593 MB** of 28,330 -> n = min(4, floor((10593-2048)/1500)=5) = **4**.
- `ruff check` on both touched files: All checks passed.
- Codex: `codex exec review -m gpt-5.6-terra --base main < /dev/null` (codex-cli 0.155.0, model line confirms `gpt-5.6-terra`, reasoning effort low). Non-empty run (~97 KB). Verdict text: "No critical or high-severity regressions were identified". Findings to disposition: **none**. Not a claim of cleanliness beyond HIGH/critical.

## Hooks skipped (declared)

- `claude-rosters-freshness`, `organ-index-freshness` on commit `0c1f33cd` — both stale only because two commands were added; regenerate at integration (`gen_claude_rosters.py --write`, `generate_organ_index.py --write`). No other hook skipped. No task id allocated, no claiming row needed (none demanded).

## Open items

1. **Discovery bar missed (0/5).** Command registration did not change behaviour for a file-naming task with no hint. Options for the operator: a boot-text pointer, a hook, or a task with no named file — not tried here.
2. Population gap: 1068 tracked files absent from the graph (scope change, not done).
3. Integrator: regenerate the two generated rosters above; `doc-counts` (collected-test count) may need regen since 2 tests were added.
4. `list` speed is build-bound (~23 s); caching the graph would be a separate change.

## Tokens ACTUAL vs ORDERED

- ORDERED: 200k. ACTUAL (this session, dedup by message id, measured before writing this section): fresh input 102 + output 18,293 + cache-creation 97,473 = **~115.9k fresh**; **cache reads 5,277,962** reported separately (not counted against the order; they dominate because of the large boot context re-read each turn). Child sessions: 117,432 fresh, reported separately above. Within the 2x stop (400k).
