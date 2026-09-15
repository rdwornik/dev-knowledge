# lane-z-4-non-claude-execution — end-of-lane packet

> **Lane** `lane-z-4-non-claude-execution` · **branch** `worktree-lane-z-4-non-claude-execution`
> · **row** `[#772]` · **contract** `LANE-z-4-non-claude-execution.md` (frozen)
> · **date** 2026-09-15 · **seat** CC (Opus 5, background lane)
>
> What changed · the proposed diffs · the open items. Written at commit-and-STOP: nothing here
> is merged, and integration is the integrator's act from the primary checkout.

## 1. The question, and the answer

**Can a non-Claude CLI on this box do useful work with nobody watching, and what does it
cost?** Sixty scored calls plus re-runs — 96 ledger rows — say: **four of the five in-scope
providers run unattended and answer; three of those four match the Opus baseline on every
outcome; not one of the five can be priced in money; and the fifth has no account behind
it.**

Every number below is read from `logs/PROVIDER-BENCH-RUNS.jsonl` (append-only) or
`logs/PROVIDER-VERDICTS.json` (derived from it). Regenerate rather than quote:

```
uv run --locked python scripts/provider_bench.py report
uv run --locked python scripts/provider_bench.py verdict
```

**Scope, and it travels inside every verdict record so a later quoter cannot drop it:** ten
bounded, self-contained, closed-form text outcomes, ONE run each, from a neutral empty
non-git directory, no tool use and no repo access. **Not** a measure of agentic work, long
context, or anything run twice.

```
PASS MATRIX (Y = predicate met, . = not met)
outcome              agy  claude  codex  copilot  gemini  ollama
extract-id            Y     Y       Y       Y        .       Y
classify-enum         Y     Y       Y       Y        .       Y
regex-branch-prefix   Y     Y       Y       Y        .       Y
json-shape            Y     Y       Y       Y        .       Y
arithmetic-pricing    Y     Y       Y       Y        .       .
locate-defect         Y     Y       Y       Y        .       Y
honest-refusal        Y     Y       Y       Y        .       Y
summary-budget        Y     Y       Y       Y        .       .
write-function        Y     Y       Y       Y        .       Y
order-versions        Y     Y       Y       Y        .       Y
```

```
VERDICTS, baseline last
copilot  PARITY         10/10  241.7s  x1.89   10 PREMIUM REQUESTS      UNPRICED
codex    PARITY         10/10  109.2s  x0.86   12,194 plan-quota tokens UNPRICED
gemini   UNREACHABLE     0/10       —      —   never reached a meter    UNPRICED
ollama   BELOW-BASELINE  8/10  151.1s  x1.18   no vendor bill at all    UNPRICED
agy      PARITY         10/10  202.7s  x1.59   Antigravity quota        UNPRICED
claude   the RULER      10/10  127.6s  x1.00   per-token list price     $0.2170 PARTIAL
```

## 2. What changed

**Four commits, one row, no merges and no push to `main`.** `main..HEAD` non-merge commits:

```
1aa363db  file [#772] -- the row, and the frozen census corrected
e2480734  the harness, and three "the trap is gone" retractions the instrument manufactured
901d1abf  ten outcomes x six providers, and the four instrument defects the first sweep published
ad03c361  one verdict per provider, priced against the same ten on Opus
```

Footprint against `main` (`git diff --stat main...HEAD`), 2,698 insertions, 2 deletions:

```
scripts/provider_bench.py             1536  NEW  the harness: census / traps / run / verdict / report
tests/test_provider_bench.py           572  NEW  68 witnesses, no network call, no CLI spawn
logs/PROVIDER-VERDICTS.json            299  NEW  DERIVED -- regenerate, never hand-edit
logs/PROVIDER-BENCH-RUNS.jsonl          96  NEW  the append-only run ledger
logs/PROVIDER-CENSUS-2026-09-15.json    76  NEW  the measured census
logs/PROVIDER-TRAPS-2026-09-15.json     74  NEW  the three trap verdicts with their evidence
scripts/graph_queries.py                26  MOD  two register rows (orphan disposition, not-an-edge)
tasks/772-...-non-claude-p.md           12  NEW  the row
tasks/manifest.json + BACKLOG.md         7  MOD  the row's node, and the generated view
ecosystem/doc-counts.md                  2  MOD  pytest_collected, regenerated
```

**No JOURNAL entry** (STANDING_RULINGS P-1 — the integrator's surface). **No audits-index
regeneration** — see §5, this lane declares the single-hook bypass rather than touching a
generated index a sibling lane is also writing.

## 3. The findings

### 3.1 Three standing traps were re-verified. All three still bite — and the first pass said the opposite about all three

Every one of those three retractions was manufactured by my own instrument, not observed
from a CLI. `logs/PROVIDER-TRAPS-2026-09-15.json` carries the evidence string beside each
boolean.

- **`copilot --model` refuses every id.** `auto` was in the candidate list; it is a
  selection *mode* the CLI documents, it is accepted, and `all(refused)` went False. It is
  now the negative **control** — an accepted control is what proves the flag is parsed at
  all, so "every id refused" becomes a statement about ids rather than about a dead flag.
- **`codex exec` hangs on an open stdin.** `subprocess.run(stdin=PIPE)` does not hold stdin
  open — `communicate()` closes the write end at once, so the "open" leg was never open.
  Re-probed with `Popen` and the handle left alone: held open it does not exit; closed it
  returns in ~13 s.
- **`agy` print-mode soft-denies tools.** The only one where the CLI itself moved. On 1.1.x
  a soft-deny was `status: CANCELED` with an empty response; on 1.2.2 it is
  `status: SUCCESS`, an empty response, ~1,342 output tokens genuinely spent, and a new
  `denied_actions` array. A detector keyed on `CANCELED` scores that as a model that
  answered with nothing — `[#676]`'s founding misdiagnosis wearing a new status string.

A fourth correction was found by the verdict **flipping between two identical passes**: the
agy trap conjoined a stable permissions fact with an unstable reliability one, so the
boolean tracked agy's mood. The deny half reproduced 3/3; the flagged half answered once and
once rambled before emitting `TOOL_DENIED` with permissions it held. They are now reported
separately.

### 3.2 Four defects were found AFTER the first scored sweep, each having already published a false number

The ledger is append-only, so each repair is an **append**: `latest_per_cell` reads the
correction and the original stays. 96 rows for 60 cells, 36 supersessions.

1. **ollama's output tokens were its input tokens, on all ten rows.** `\beval count:` also
   matches inside `prompt eval count:`, which comes first. Anchored to `^`. Would have
   published a model that emits exactly as many tokens as it reads, ten times — and nobody
   reading a table notices a plausible number.
2. **The claude leg attributed 4 of 10 runs to its own bookkeeping side-call.** Ranking the
   served model by `max(outputTokens)` picks Haiku whenever the real answer is short, and
   these prompts are deliberately short. Ranked by **total** token volume instead.
3. **The same leg then priced only the model it named.** Every model in `modelUsage` is now
   priced, the figure is marked `usd_is_partial`, and the unpriced remainder is **named**.
4. **`regex-branch-prefix` was scored under two different instruments.** A fenced block was
   unwrapped as packaging and an `r"..."` string literal was not — so Opus alone lost the
   cell to packaging while ollama's identical pattern in a fence passed. **The cell was then
   re-run for every provider**, because fixing a predicate and re-running only the loser
   leaves a table scored by two instrument versions, with the difference silently favouring
   whoever was measured second.

An earlier, cheaper repair: the sweep originally buffered its ledger and wrote at the end.
It was killed at ~4 of 60 calls in; a crash at call 59 would have discarded the entire
spend. `append_ledger` is now called per row.

### 3.3 The control that makes the Opus comparison a comparison

`claude -p` run **from the worktree** loads the project hooks and the governance doctrine:
it spent **139,611 tokens and $0.40** answering a five-word probe with a report about
JOURNAL anchoring. The identical probe from a neutral empty non-git directory cost
**$0.085** and answered the question. Every provider is therefore invoked from one neutral
directory, every prompt is self-contained, and the claude leg carries
`--setting-sources local`. A benchmark that lets one contestant carry the house rules into
the ring measures the house.

Self-contained prompts are also a hard constraint, not tidiness: **ollama has no tool layer
and cannot open a file.** A task set half the field is physically unable to attempt prices
nothing.

### 3.4 An auth refusal is not ten capability losses

`gemini` exits 1 at `IneligibleTierError` before a model sees the prompt. Comparing raw pass
flags made those ten cells ten losses to Opus, and the rendering then printed ten lines
reading "CANNOT be trusted on `extract-id`" — contradicting the verdict's own sentence three
lines above, which said its capability is not measured here at all. A cell is now compared
only when **both** legs ran unattended, did not error, and put something on stdout;
unreached cells are listed by name and never scored. The negative control matters as much:
ollama's `2.8500` is a real answer that really misses and survives the same filter.

### 3.5 Unpriced is not free, and here it is the dominant case

`usd_comparable` is False for **every** row in the verdict artifact, the baseline's own
included. The reason differs per provider and naming it is the deliverable:

- **copilot** meters PREMIUM REQUESTS (10 for the ten outcomes), not tokens. Neither served
  id is in the registry.
- **codex** reports ONE undivided token total (12,194). Its id **is** declared and carries
  no `rates:` block — *unknown*, which is not the same fact as *zero*.
- **agy** discloses no model and no number.
- **ollama** has no vendor bill at all — the one provider here for which "free" is the true
  answer rather than the default one.
- **claude** is $0.2170 over ten and even that is PARTIAL: an unpriced Haiku bookkeeping
  side-call (959 tokens) is named rather than summed at zero. The vendor's own
  `total_cost_usd` for the same ten was $0.2915; the gap is that side-call plus what three
  rate rows do not cover.

A lane that divided a subscription quota by its own token count would manufacture a rate.
Two witnesses refuse it, including the subtle version: a PARTIAL figure is a lower bound
wearing a decimal point, and comparing against a lower bound flatters whoever is measured
against it.

### 3.6 copilot served two different models across ten identical command lines

`mai-code-1.1-flash` seven times, `gpt-5.6-luna` three — each billed exactly one premium
request, and both knowable only **post-hoc** from `--usage-output-file`. The `--model` flag
that would pin it is the trap verified in §3.1: it refuses every id. **A copilot result is
therefore not reproducible from its invocation alone,** and any organ that uses copilot must
record the served model after the fact rather than assume the one it asked for.

### 3.7 agy's binary self-updated in the middle of a scored sweep

8 of 10 calls died with `WinError 2` — a *missing executable*, not a refusal — because agy
replaced itself 1.2.2 → 1.2.3 mid-run, leaving `agy.EXE.<epoch>.old` behind as the evidence.
The partial leg was not patched call-by-call; all ten were re-run on 1.2.3, which is the only
way the ten rows describe one binary. It self-updated **twice** during this lane. A CLI that
can vanish from under a running batch is itself a result for the unattended question.

### 3.8 The frozen census is refuted in part

Measured with `where` on 2026-09-15. The contract declares `cursor-agent`, `aider`, `llm`
and `amp` absent: `aider`, `llm` and `amp` are indeed absent, but **`cursor-agent` is
present** (`AppData/Local/cursor-agent/cursor-agent.cmd`, 2026.09.08-6caf4ff) and **`grok`
is present** (`.grok/bin/grok.exe`, 1.0.5) while appearing in neither list. Per the
contract's own *reported absent, never substituted*, the five in-scope providers were run as
ordered and the two corrections are recorded with a liveness probe each rather than promoted
into the scored set. **A frozen scope is not widened by the lane that finds the scope wrong.**

## 4. Proposed diffs — none applied by this lane

### 4.1 `ecosystem/provider-registry.yaml` — one row this lane can justify, four it cannot

**Actionable now.** `claude-haiku-4-5-20251001` is billed by Claude Code itself on every
invocation of the baseline leg and is **not declared at all**, while three Anthropic
siblings carry `rates:`. It is the single row that would turn this lane's baseline figure
from PARTIAL into complete:

```yaml
  claude-haiku-4-5-20251001:
    provider: anthropic
    rates:
      input: <list price>
      output: <list price>
```

**Named, not proposed as priced.** `mai-code-1.1-flash`, `gpt-5.6-luna` and
`qwen2.5-coder:14b` are undeclared; `gpt-5.6-terra` is declared with no `rates:`. This lane
measured *which ids were served* and deliberately did **not** invent their prices. The
registry's owner (`[#751]`) rules the rates; the ids and the metering units are supplied
here as data.

`qwen2.5-coder:14b` needs a decision rather than a number: it is local inference with no
vendor bill, so a `rates:` block of zero would be *true* for it and would set a precedent
that "no rate row" and "free" can share a spelling. Recommend an explicit local/unmetered
marker instead.

### 4.2 `docs/audits/2026-09-15-technical-batch-z-manifest.md` — add the frontmatter

`batch_manifest.open_batches()` returns `[]` in this tree with the manifest committed and
naming this lane as #4. The manifest carries **no YAML frontmatter at all** — no `status:
open`, no `closed_by:` — and `open_batches` requires all four conditions, failing toward
no-exemption on a manifest it cannot parse. Consequence: **the ADR-110 exemption cannot fire
for any lane in batch Z**, and every lane meets the anchor gate at every commit. Unrepaired
here: the manifest is immutable and belongs to the dispatch seat.

### 4.3 `scripts/logs_retention.py` vs `scripts/validate_hermetization.py` — two organs, one directory, opposite rules

Found by being the first thing ever to try committing a bucketed log. `git ls-tree HEAD
logs/` shows **no bucketed file has ever been committed**: `logs/YYYY-MM/` exists on disk and
has never existed in git, so the two organs had never met.

- `logs_retention` relocates any `<STEM>-YYYY-MM-DD.<ext>` directly under `logs/` into
  `logs/YYYY-MM/`, byte-identically, at session start.
- `validate_hermetization` then refuses the result:
  `'logs/2026-09/' is not an admissible home for a new file`.

This lane **did neither thing**: the two dated artifacts were moved back to their committed
flat paths, nothing was bypassed, and `logs/YYYY-MM/` was not added to the allowlist —
because the gate's own refusal text says what that would be, *"a new home is an operator
decision recorded as a ruling, not a drive-by add"*. `logs/PROVIDER-VERDICTS.json` is
undated for the same reason, pinned by a witness so a later tidy-up does not re-date it and
rediscover the collision by being blocked at a commit.

Three candidate resolutions, in the order this lane would rank them; all three are the
operator's call:

1. **Admit `logs/YYYY-MM/` as a home by ruling.** Smallest diff, and it ratifies what the
   retention organ already does on every machine.
2. **Exempt TRACKED files from relocation.** Retention exists to stop an untracked
   per-event directory growing forever; a committed artifact is not that problem, and git
   already keeps its history.
3. **Retire the month bucket.** Largest blast radius — the `PROPOSALS-*.md` files already
   sitting untracked in `logs/2026-09/` are the next things to walk into the gate.

### 4.4 For `[#676]`, which owns the commit-tier invocation-shape check

The three verified shapes and their exact refusal texts are in
`logs/PROVIDER-TRAPS-2026-09-15.json`, and the working non-interactive invocation for each
of the five in-scope CLIs is in `scripts/provider_bench.py::PROVIDERS`. Supplying data to a
check is not implementing it: `[#676]` stays open and is the direct beneficiary.

## 5. Gates, and what was and was not bypassed

**Three gates refused step 2 and all three were right**; each was answered with a recorded
reason, none with a bypass:

- **`graph-orphan-census`** — `provider_bench.py` is reached by no wiring surface and should
  not be: every subcommand makes real paid calls to five vendor CLIs, so a commit- or
  session-tier trigger would bill the operator on every commit. The consumers are **named**
  (the packet, the ledger, the witnesses) rather than a trigger invented to satisfy a
  census. Owner of the disposition row: `[#676]`.
- **`graph-edge-class-census`** — every text this module extracts from is **vendor output**,
  not corpus; the relations it discovers exist nowhere in FPG-1 to be read from instead.
  Registered `not-an-edge`, which is the recall-over-precision cost the shape predicate's
  own docstring predicts.
- **`graph-task-coverage`** — answered from the *file's* direction as well as the row's:
  every artifact this module writes carries `"row": "[#772]"` inside it, so the claim
  survives a later rewrite of the row's body.

**One bypass in the whole lane, at step 2 only:** `SKIP=audit-health` on
`journal_spine_anchor`, for one entry (`0ee3d161`), with the two-sided discriminator run
first and both-False proved to be the integrator's half. **It is now spent.** The integrator
wrote the anchoring entry; the entry reads False-here/True-at-main; steps 3 and 4 committed
with **no bypass at all**. Waiting for the owner was the right remedy twice in this lane —
the same thing happened to a `decision-coverage` refusal at step 1.

**This commit declares `SKIP=audit-index-freshness`**, one named hook, because adding this
packet makes the generated `docs/audits/README.md` stale and a batch lane must not
regenerate a shared index a sibling lane is also writing. Regenerating it is the
integrator's act.

## 6. Tests

- **Targeted, per `[#528]`:** `tests/test_provider_bench.py` — **68 passed**, the selection
  `impacted_tests.py select --changed scripts/provider_bench.py` returns. `ruff` clean.
- **Not one test makes a network call or spawns a vendor CLI.** They exercise parsers,
  predicates, pricing and ledger semantics against captured fixtures — the only half of this
  lane that can be tested without spending money. Every predicate is exercised **both ways**
  against a plausible near-miss, because a predicate that only rejects gibberish is an
  always-pass wearing a green tick.
- **A RED reported at step 2 is RETRACTED here.**
  `tests/test_graph_spine.py::test_an_expired_lock_is_broken_so_a_dead_builder_never_wedges_the_store`
  failed after `tests/test_edge_class_census.py` and passed alone; it was attributed to
  neither this lane nor a real defect by a paired run (60 passed/1 failed with this lane's
  test file removed, 110/1 with it). Re-run at step 5 on the synced tree: **61 passed, 0
  failed.** It no longer reproduces. Recorded rather than quietly dropped — a retraction has
  to reach every claim that depended on it.

## 7. Open items

| # | Item | Owner |
|---|---|---|
| 1 | `logs_retention` vs `validate_hermetization` — a dated `logs/` artifact has no landable home (§4.3) | operator ruling |
| 2 | Batch Z's manifest has no frontmatter, so ADR-110 relief cannot fire for any lane in the batch (§4.2) | dispatch seat |
| 3 | `claude-haiku-4-5-20251001` is billed on every Claude Code call and is undeclared (§4.1) | `[#751]` |
| 4 | Four served ids named but unpriced; `qwen2.5-coder:14b` needs an unmetered marker, not a zero (§4.1) | `[#751]` |
| 5 | copilot's served model is knowable only post-hoc; `--model` refuses every id (§3.6) | `[#676]` |
| 6 | agy 1.2.x attests no served model anywhere — a vendor disclosure gap, not a registry gap (§3.5) | upstream / `[#691]` |
| 7 | agy self-updates mid-run and can vanish from under a batch (§3.7) | `[#676]` |
| 8 | `gemini` has no account on this box; the CLI itself runs unattended correctly (§1) | operator |
| 9 | Census corrections: `cursor-agent` and `grok` present, in neither contract list (§3.8) | next census |

**What this lane did NOT do:** no merge, no push to `main`, no JOURNAL entry, no
audits-index regeneration, no edits outside the declared footprint, and no repair of a
finding whose owner is somebody else.
