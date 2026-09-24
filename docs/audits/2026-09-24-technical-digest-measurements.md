> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-browser/DIGEST-MEASUREMENTS-2026-09-24.md` (a Drive transport path, not retained in
> this repo — verifiable against the bytes landed below by their hash,
> `sha256:6864c968dbd66f4d472fc5d5674e02760041e7dde7cbaa97a14406485fc6cc6e`, 10,209 B, computed by
> this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-digest-measurements.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: the morning review; the model pick is the operator's routing ruling, and the plan_lint grammar defect needs a row
date: 2026-09-24
from: night-readonly (BATCH-NIGHT-READONLY-2026-09-23 Part 3, job a58f3cec, Opus 5.5), read-only on main @ 4667f731

# DIGEST — measurements: /skill-doctor, /doctor, and the Opus 4.8 vs 5.5 A/B

## 1. `/skill-doctor` and `/doctor` at the hub root

**Both RAN HEADLESS.** Neither was NOT RUNNABLE, and no flag was invented. The commands, verbatim, with the hub root as cwd:
- `claude doctor` (a CLI subcommand; `claude doctor --help` lists only `-h`);
- `claude -p "/skill-doctor" --output-format json`;
- `claude -p "/doctor" --output-format json`.

- **`claude doctor` (CLI):** exit 0, 8 s. The native install is 2.1.281, auto-updates on. It reports "No installation issues found." It says nothing on CLAUDE.md: the CLI form checks the install only.
- **`/skill-doctor`:** exit 0, 29 s, 0 turns, $0. It is a local report, not a model call.
  - **4 project skills loaded, never invoked:** `preflight`, `spine`, `why`, `conformance-hub`.
  - **8 claude.ai-synced skills never invoked:** `anthropic-skills:{docs,docx,import-memory,morning,pdf,pptx,skill-creator,xlsx}`.
  - Each one's listing costs its "context" column every turn (about 30 to 330 tokens per skill).
  - Heaviest by 7-day tokens: `codex-review` 67.6m, `gotchas` 29.9m, `changelog-review` 22.3m, `handoff-verify` 14.9m, `handoff` 9.9m.
  - Its remedy: disable in `/skills`, or turn the synced ones off on claude.ai (a deleted synced copy re-downloads).
- **`/doctor` (the CLAUDE.md trim proposal):** exit 0, 151 s, 21 turns, **$0.81**, served `claude-opus-5-5[1m]`.
  - Headless, it was **denied every read outside the repo**. Checks 0 (install), 1 (unused skills/plugins/MCP), 7 (version), 8 and 9 were BLOCKED.
  - **CLAUDE.md trim: "No cuts proposed."** CLAUDE.md is about 6k est. tokens, under its threshold and byte-capped by `tests/test_claude_md_byte_cap.py`.
  - The only candidates it named: the §9 hook roster (about 35 lines, about 1.2k tokens, largely restating `.pre-commit-config.yaml`), kept because it is the designated annotated roster. And about 1k tokens loaded twice, once from CLAUDE.md and once from AGENTS.md (branch prefixes, append-only files, the test command). The hub-region parity rule means a fix goes through a row, not an edit.
  - Warnings:
    - SessionStart timeouts: surface-triage 96%, fleet-health 41%.
    - `lane_end_guard.py` runs as bare `python`.
    - `MEMORY.md` is about 3.8k tokens, the largest always-loaded item.
    - 4 worktree folders remain (possibly live lanes; untouched).
  - It changed no files. `git status` was clean afterwards.
- **For the operator's morning** (to finish the blocked checks): run `/doctor` in an interactive session and approve its read-only prompts (`~/.claude.json`, `~/.claude/settings.json`, the session-log folder, `claude --version`).

## 2. The Opus A/B (S1 Part C design)

**Design, as run:**
- **Two fixed orchestrate-role inputs** (sha256 prefixes: input1 `2ec95d400a3de99b`, input2 `1b305a0d0b1776c0`):
  - input 1: one lane contract drafted from OPEN row `[#703]` (the impacted-test empty selection);
  - input 2: a 3-lane batch plan from OPEN rows `[#588]` (spine parent-map), `[#864]` (decision-coverage flake) and `[#893]` (lane-cost close).
  - Each input inlines the row files verbatim, `LANE-5A-2` as the template, and the plan_lint grammar (`**Files you own:**`, Serial/Starts-after).
- **The instrument, for both arms alike:**
  - `claude -p --model <id> --setting-sources project --tools "" --no-session-persistence --output-format json`, with the prompt on stdin;
  - cwd is a scratch copy of CLAUDE.md, AGENTS.md and the two `@`-imports, with no settings and no hooks;
  - no tools, so nothing could touch the repo.
  - **A sentinel line in the scratch CLAUDE.md appears in all 4 outputs,** which proves the doctrine loaded for both arms.
- **Models served** (from `modelUsage`): exactly `claude-opus-4-8` and `claude-opus-5-5`. No substitution.

**Scores:**

```
leg                 | lint (raw)  | lint (slug-adapted) | Done items w/ named verifier | owned files disjoint | wall
opus-4-8 in1        | REFUSED     | PASS (0 findings)   | 3/6                          | n/a (1 lane)         | 28 s
opus-5-5 in1        | REFUSED     | PASS (0 findings)   | 7/8                          | n/a                  | 31 s
opus-4-8 in2        | REFUSED x3  | PASS (0 findings)   | 8/15                         | yes (0 overlap)      | 53 s
opus-5-5 in2        | REFUSED x3  | PASS (0 findings)   | 16/18                        | yes (0 overlap)      | 60 s
total 4-8           |             | 4/4 contracts pass  | 11/21 = 52%                  | yes                  |
total 5-5           |             | 4/4 contracts pass  | 23/26 = 88%                  | yes                  |
```

**How to read each rubric leg honestly:**
- **Lint:** every contract from both models is REFUSED raw, because plan_lint requires a ``slug `<slug>` `` line that neither the prompt nor the template (a real frozen contract) asked for. That is a harness defect, not a model difference (§3).
  - After the same one-line scorer adaptation on both arms, all 8 contracts lint clean.
  - Input 1 was linted paired with the reference `LANE-5A-3`, because `check` needs two or more contracts.
- **Done-when testable:** the mechanical proxy counts items that name their verifier (a test/command/path in backticks, or a number with a unit).
  - **On a side-by-side read, 4.8's items are testable in substance too** (e.g. "assert the git-call count `== 1`"). The proxy under-credits terse phrasing.
  - **5.5 is consistently more specific.** It names fixture shapes (a range mixing `--no-ff`, FF and root commits), repetition counts (5 timing runs, medians), exact gate commands (`uv run --locked ruff check`, `audit.py health`), and commit ordering of the golden before the refactor.
  - Verdict: **5.5 better, not 4.8 failing.**
- **Files disjoint:** both models produced disjoint ownership on input 2, with no Serial clauses needed.
  - 4.8 claimed `scripts/block_ff_push.py` and `scripts/journal_anchor.py` for the spine lane. That is broader, but row 588 names both.
  - 5.5 claimed two not-yet-existing paths (`tests/fixtures/no_ff_spine/`, `tests/test_decision_coverage_determinism.py`), which is legitimate for new tests.
  - **Neither model honoured row 588's `serialize-group: audit-py`.** The plan lint cannot see that frontmatter either.

**Price.** Registry rates:
- `claude-opus-4-8`: $5 in / $25 out, cache write 1.25× = $6.25, cache read 0.1× = $0.50 (`ecosystem/provider-registry.yaml:699`, card `as_of` 2026-06-24).
- **`claude-opus-5-5` has no registry row**, so the batch's stated fallback applies: $4 / $20, cache read $0.20. Cache write is 1.25× = $5, the registry multiplier. That last one is an assumption, recorded.

```
leg              | in  | cache-write | cache-read | out  (thinking) | $ registry-rate | $ CLI-reported
opus-4-8 in1     | 2   | 20,653      | 0          | 1,788 (328)     | 0.1738          | 0.2512
opus-5-5 in1     | 2   | 21,111      | 17,667     | 3,413 (1,442)   | 0.1774          | 0.2407
opus-4-8 in2     | 2   | 19,543      | 2,131      | 4,459 (1,023)   | 0.2347          | 0.3080
opus-5-5 in2     | 2   | 21,157      | 531        | 6,963 (2,371)   | 0.2452          | 0.3086
total opus-4-8   |     |             |            |                 | 0.4085          | 0.5592
total opus-5-5   |     |             |            |                 | 0.4226          | 0.5493
```

- **Cost is a tie within 3.5%.** 5.5 writes about 1.6× the output tokens (more thinking, longer contracts) at a 20% lower per-token rate.
- **The two price columns disagree for one reason:** the CLI bills these 1-hour cache writes at 2× input, while the registry declares a single 1.25× multiplier. That is a registry gap, independent of the A/B.
  - The CLI figures reproduce exactly under 2× write. For opus-5-5 they also need $4 / $20 / $0.20, which independently corroborates the fallback rates.
- The whole A/B cost $1.11 as billed by the CLI.

**A/B verdict for the routing ruling:** at equal cost and equal structure (lint, disjointness), **opus-5-5 writes more checkable Done-contracts** (88% vs 52% by proxy; also better on a read-through). N = 2 inputs, 1 run each. That is a direction, not a significance claim.

## 3. The defect the A/B exposed (for a row)

**`scripts/plan_lint.py` cannot read the contract format the batches actually use.**
- It refuses any contract without a ``slug `<slug>` `` line (`plan_lint.py:176-185`, `_SLUG_RE` at `:143`).
- It reads ownership only from `**Files you own:**` (`:110-112`).
- **All 10 live WAVE5A contracts carry neither.** They carry `**Owns:**` and no slug line (MEASURED by grep tonight).
- **Corroborated independently:** the WAVE5A dispatcher's own receipt (`SESSION-dispatcher-wave5a-2026-09-23.md` lines 10-36) records the same refusal. It worked around it by translating the contracts by hand.
- Consequence: the ordered step-0 command cannot run on real contracts. Even the translated run depends on a hand-translation the lint does not own.
- **Fix, one of two:**
  1. teach `parse_lane_contract` the live grammar (the slug from the `## Dispatch` `-n <slug>`; `**Owns:**` as an ownership label), which is library-first because the Dispatch line already carries the slug;
  2. make `gen_lane_contract.py` emit plan_lint's grammar, and refuse hand-written contracts.
- It also blocks the WIRE of `plan_lint` at `pre-launch` (Digest ORGAN-TRIAGE).
- **Secondary:** plan_lint does not read a row's `serialize-group:`, so two lanes in the same group (e.g. `audit-py`) pass as parallel-safe.

## Routing record (what served)

- orchestrate + scoring: claude-opus-5-5 (this session).
- the A/B legs: `claude-opus-4-8` ×2 and `claude-opus-5-5` ×2, as named. The served ids were verified from `modelUsage`.
- `/doctor`: its child served `claude-opus-5-5[1m]` (the CLI default; no model was specified, as ordered).
- `/skill-doctor`, `claude doctor`: no model (local).
- No sub-agents were used for Part 3.

DONE 2026-09-24 00:45
