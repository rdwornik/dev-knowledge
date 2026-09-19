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
