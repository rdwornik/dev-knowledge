# NB2 · WAVE 2 · LANE O — A4-AGY: staff the big-context analysis role — M/L

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-o-4-agy-acceptance` -> branch `worktree-lane-o-4-agy-acceptance`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §A4-AGY).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-o-4-agy-acceptance --permission-mode bypassPermissions "[dev-knowledge . A4 . agy analysis-role acceptance] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-O-A4-agy.md"
```

## LANE CONTRACT (verbatim)

> ## A4-AGY — staff the big-context analysis role — M/L
> Write-scope: docs/audits/ artifacts + the benchmark item files per the persisted SDA-1
> discipline; NO routing-table change (that is the architect's ruling on the evidence). Measured
> acceptance for **agy** FIRST, per R3/A4: seeded-defect items for the ANALYSIS role, one of which
> IS the operator's use case — a whole-repo holistic scan (cross-file coherence, orphan spotting,
> doc-vs-code drift) — judged against the named incumbent baseline in-window, never vibes. SDA-1
> constraints bind: **TRANSPORT PRECONDITION (self-review fix): batch-1's preflight left WHICH
> transport is alive as a hub-side record, not this contract's memory — re-verify agy's transport
> end-to-end FIRST; if it is dead, STOP this lane, record the operator act owed, do not improvise
> an alternate route at night.** Q2 served-id preflight next (agy's envelope is untrusted — a cap
> at INDETERMINATE is a legitimate, recorded outcome per C-9, chosen deliberately, not discovered);
> Φ_analysis defined in writing before the run; EXHAUSTED is a third outcome; floors without an
> in-window incumbent print UNCALIBRATED.
> Ex-ante: a computed-gates cell (agy, analysis) exists with every SDA-1 discipline token present;
> the whole-repo-scan item's ground truth cross-checks at least one FM-C finding (two instruments,
> one reality — agreement or a named discrepancy).

## STEP 0 — THE TRANSPORT PRECONDITION IS A HARD STOP, AND IT IS YOUR FIRST ACT

Verify **agy** end-to-end before anything else: it answers, on this machine, right now, with a
served model id. Known and measured on 2026-08-20 — re-verify rather than trust:

- `agy` (Antigravity CLI) is the **working OAuth path**; `@google/gemini-cli` is dead under OAuth
  (`IneligibleTierError` / `UNSUPPORTED_CLIENT`), and an API key is forbidden by the standing auth
  ruling. **"Gemini" in operator speech means agy**; the retired Gemini-CLI registry entry stays
  retired.
- `agy` **refuses a bare flash id**: `--model gemini-3.7-flash requires --effort (low|medium|high)`.
  That is an effort-pin refusal, **not** refusal-to-serve — a brief calling it the latter is wrong.
- `agy` **never substitutes silently**: an unknown id exits 1 at zero tokens and prints the served
  list.
- **`agy`'s envelope `status` is unreliable** — `status=ERROR` on 8 of 14 items while carrying a
  complete, often correct answer. **Key on `response`, never on `status`.**
- The served-id attestation is the log line `Resolving model <id>` in
  `~/.gemini/antigravity-cli/log/cli-*.log` — agy's JSON envelope carries no model field. That log
  line **is** your Q2 served-id preflight.
- **`agy` trusts all of `C:\Users\1028120`** and will wander into the primary checkout and sibling
  repos. Pass `--add-dir` and **check what it actually read** before claiming a scoped run.

**If the transport is dead: STOP this lane.** Record the operator act owed, in one paragraph, and
write the packet. **Do not improvise an alternate route at night** — that is the contract's own
instruction and it is the whole point of the precondition.

## THE INCUMBENT PROBLEM — measured, and it shapes your gates

`ANTHROPIC_API_KEY` in `C:\Users\1028120\Documents\.secrets\.env` **authenticates but has zero
credit** (verified 2026-08-23: HTTP **400** `"Your credit balance is too low"` — a 400 *after*
authenticating is billing, a bad key is 401). Re-check it; if it is still 400, there is **no
in-window incumbent**, and the contract already rules that case: **floors without an in-window
incumbent print `UNCALIBRATED`.** Print it. Carry `P_i`/`Φ_i` from the prior artifact if you carry
anything, and **state the carry as a numbered limitation against each gate it weakens** —
comparative gates against a carried baseline are not like-for-like and must not be reported as
though they were.

**Do NOT substitute `claude --safe-mode` for the incumbent.** The CLI drives unrestricted `Bash`,
which does not route through the sandbox exec and therefore bypasses the git-history leg — that
re-creates the exact asymmetry the guard exists to remove. The carried baseline is the more honest
option.

## THE DISCIPLINE IS PERSISTED — read it, do not reconstruct it

`docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` is the SDA-1 seeded-defect
benchmark design, persisted byte-verbatim on 2026-08-28 (commit `1a091249`). **It is the method.**
Read it in full before designing a single item, and name the tokens it requires:
**Φ_analysis defined IN WRITING BEFORE THE RUN** · **EXHAUSTED as a third outcome** · the Q2
served-id preflight · the INDETERMINATE cap as a *deliberate, recorded* outcome (C-9) rather than
something discovered afterwards. The Ex-ante says *"every SDA-1 discipline token present"* — so
the packet lists them and shows where each is discharged.

## THE OPERATOR'S OWN ITEM — and its cross-check

One seeded-defect item **IS** the operator's use case: a **whole-repo holistic scan** — cross-file
coherence, orphan spotting, doc-vs-code drift. Its ground truth must **cross-check at least one
FM-C finding**: FM-C's funnel census landed in `docs/audits/` earlier tonight; pick a finding from
it, and report **agreement or a named discrepancy**. Two instruments, one reality. A discrepancy
is a result, not a failure — but an unexamined one is neither.

## THE FENCE

**NO routing-table change.** `ecosystem/routing-table.yaml` and `~/.claude/ROUTING.md` (which is
**L0, outside this repo**) are the architect's to rule on your evidence. You produce the computed
gates cell; you do not promote anything. **Kimi / GLM / DeepSeek follow the same gate AFTER their
transports are repaired — operator acts, not tonight.** `grok` stays pay-per-call point-use per the
registry. Write only `docs/audits/` artifacts plus the benchmark item files the SDA-1 discipline
defines; no `ecosystem/` writes, no `tasks/` writes, no gate wiring.

---

## BOOT (mechanical — before touching a file)

`dispatch` put you in your own worktree. `/lane-boot` steps 1–2 are done (name validated,
single-flight claimed, worktree provisioned). Run 3–7:

```
Get-Location                                              # confirm the worktree
uv run --locked python scripts/worktree_seed.py --plan .  # prints the seed plan; RUN it
uv sync --locked
```

Without `ecosystem/*/state.yaml` seeded from the primary, `audit-health` reports
`repos registered (none)` -> `health: DEGRADED` and **every commit is blocked**. Every test
invocation is `uv run --locked pytest …`; a bare `pytest` inherits the primary's `VIRTUAL_ENV`
and reports green about the primary's source (STANDING_RULINGS D4).

## BINDING CLAUSES ON EVERY LANE OF THIS BATCH (operator appendix, verbatim)

> **A1** state is first-class — every governed object carries explicit state + dated transitions;
> all health numbers are TIME-SERIES on the existing telemetry-store pattern (append-only
> records, derived views; NO second store). **A5** trust contract — every claim carries a
> witness; the packet reports the ex-ante numbers verbatim. Terra pre-merge on every mutating
> lane, tally-in-body. RED-first everywhere: a gate that never fired is not proven.
> Library-first named per lane. Alias standing: "Gemini" (operator speech) = **agy**; the
> retired Gemini-CLI registry entry stays retired.

**RED-first is not a style note.** Where your deliverable is a check, a gate or a query, the
failing witness comes FIRST and is shown in the packet: the test that FAILS before your change
and passes after, or the seeded violation the new check REFUSES. A green test that never went red
proves the assertion runs, not that it discriminates.

**A1 in practice.** If you emit health numbers, they go into the **existing** telemetry store as
append-only records with derived views. Do not create a second store. Find the store before you
design against it, and name its path in your packet.

## RATCHET

`protocols/` + `templates/` deltas are **0** for every wave-2 lane except where your own contract
says otherwise. Measure with `uv run --locked python scripts/silent_rule_detector.py` before your
first commit and before your last, and report both. The wave-1 dispatch measurement was
**443 / 61 files, detector silent-rule-v5, zero headroom**; wave-1 lane C held the batch's only
authorization and may have moved it — so **measure, do not assume 443**.

## THE FOUR THINGS THIS LANE DOES NOT DO

1. **No JOURNAL.md entry.** The integrator writes one anchor for the whole queue after every lane
   STOPs. The Stop hook will demand one naming your SHAs — **decline it explicitly, with the
   reason** (ADR-85 amendment 2026-08-03 §A5 made that hook advisory in full; the hard leg is
   `block-unanchored-push`, and a lane does not push).
2. **No self-merge and no suggesting one.** Commit-and-STOP; your branch enters a frozen queue.
   A hand-back packet ends at `branch + SHAs + gate state + findings`.
3. **No row closures, no `tasks/` writes** unless your own contract grants them. Findings are
   **REPORTED as candidate filings**, never filed.
4. **No generated-surface regeneration** (`BACKLOG.md`, `docs/audits/README.md`,
   `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, `.claude/generated/*`) — the integrator
   does it ONCE on the merged result. If a gate forces one to keep your own commit legal, do it in
   its own commit and **name that commit in your packet**.

## TESTS

Targeted only — the files covering your own diff. The full suite runs once, at integration
(~9–13 min). Known REDs that are **not yours**: the anchor-gate probe test has been RED on main
since 2026-08-22, and a lane worktree structurally REDs `test_stale_worktrees`. Prove a RED is
inherited (`git merge-base --is-ancestor`) rather than asserting it.

## REVIEWER

Terra pre-merge, **tally-in-body**: run `codex exec` over your own diff (NOT `/codex-review` — a
mixed doc/code diff kills that lane) and put the tally in your packet. An unreachable reviewer is
one recorded line with the error, not a lane failure.

## YOUR PACKET

`docs/audits/2026-08-29-technical-nb2-<lane-letter>-packet.md` — never the repo root. In order:
(1) per-done-item **MET / NOT-MET / PARTIAL** with a witness each; (2) commit SHAs in order;
(3) terra tally; (4) candidate filings; (5) budget decisions; (6) deviations with owners.
**Report your contract's own Ex-ante line verbatim, then the measured result against it.**

Then **STOP**.

---

## LATE ADDENDUM — two locators resolved after the freeze predicates ran on this file

Lane G's freeze-time predicates (merged tonight) were run over this contract before it was
handed to you. Two findings, both about **locators in the architect's own quoted text**, resolved
here rather than by editing the quote:

- **`R3` is NOT a `STANDING_RULINGS.md` register heading.** `preflight_contract --freeze` reports
  *"register R3 — no `### R3` heading"*, and it is right: there is no such heading. In this repo
  **`R3` means `[#483] R3`** — a ruling scoped to a backlog row, written in the form
  `PERMANENT per [#483] R3` (`protocols/STANDING_RULINGS.md:69`, and again at `:73` and `:178`).
  Read "per R3/A4" as **`[#483] R3`**, and open that row's ruling before relying on it.
- **The agy served-id attestation path DOES exist** — the predicate's FAIL on
  `~/.gemini/antigravity-cli/log/cli-*.log` is a **false positive**: predicate (i) does a literal
  existence check and **does not expand globs**. Measured on this machine:
  `~/.gemini/antigravity-cli/log/` holds `cli-20260820_133326.log` and siblings. So the path is
  good; treat the run's own fresh `cli-*.log` as the attestation, and note in your packet that the
  newest ones are dated **2026-08-20** — if no new file appears after your run, agy did not
  actually execute, whatever its envelope says.

Both are reported as candidate filings against `[#591]`: a register-id predicate that cannot see
row-scoped ruling ids, and an off-repo predicate that cannot expand a glob.
