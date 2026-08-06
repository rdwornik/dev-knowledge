# Batch-1 independent verification — a second seat checks the integrator's homework

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06 · **Slug:** batch1-verification
- **Seat:** cloud CC (Opus 5), unattended night run, branch `claude/night-audit-batch-1-verify-27hai3`
- **Under review:** the batch-1 range `df815c7..319f885d` and its self-graded record,
  `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`
- **Posture:** the packet is a set of CLAIMS. Every verdict below is re-derived from the tree, git,
  and the live gates. Where the packet is right, this says so and names the evidence; where it is
  incomplete, it says that too.
- **Authority used:** read/derive everything; execute only the pre-ruled fixes in §7 and the two
  fully-evidenced row closes in §3. No merge, no push to `main`, no edit to an immutable artifact.

---

## 1. Method, and what this audit could NOT verify

Everything was re-derived on a fresh clone with the pinned toolchain (`uv 0.11.19`,
`uv sync --locked --group analytics`), hooks armed (`pre-commit install -t pre-commit -t
commit-msg -t pre-push`), and the full suite plus `audit.py health` run from this seat.

**Two environment corrections were needed before any verdict was trustworthy, and both are worth
stating because each one silently produced a WRONG answer first:**

1. **The clone's `main` ref was stale.** `git clone` gave a shallow tree whose `origin/main`
   pointed at `65a549bf` (2026-07-30). Against that ref the anchor backstop returned
   `[!!] journal_spine_anchor: backstop could not complete (AnchorError('disposition floor
   24882f8cc is not an ancestor of main'))` and `review_artifact_coverage` reported **0**
   code-impact merges. Both were artifacts of the ref, not facts about the batch. After
   `git fetch --unshallow origin main` (origin/main == `319f885d`) and `git update-ref
   refs/heads/main 319f885d`, both checks report their real verdicts. **A verifier that had not
   noticed would have cleared the batch on a vacuous pass** — the exact class this repo builds
   gates against.
2. **`audit-health` cannot pass in this container at all.** No sibling repos are cloned, so the
   OPERATIONAL pre-check `[!!] repos registered (none)` fails on every commit regardless of diff.
   Every commit on this branch therefore carries `SKIP=audit-health` with that reason in its
   message, and `audit.py health` was run and read manually before each one. This is an
   environment gap, disclosed — not the F1 anchor-timing skip.

**Honest limits of this audit:**

- The suite cannot be reproduced faithfully here. This container is the **PATH-only pyright shape**
  that lane A's own `Record the Pyright shape` step models as the "UNMODELLED third shape"
  (`pyright-langserver` on PATH, no `node_modules/pyright`), the repo dir is `dev-knowledge` not
  `.dev-knowledge`, sibling repos are absent, and git is a different minor version. 14 of 2419
  tests fail here for those four reasons. Every one was individually attributed to the environment;
  none to the batch diff. The operator's-host verdict is not re-derivable from this seat.
- The **"exactly 2 operator touches"** clause of [#505] is unverifiable from the tree — nothing
  records interaction counts. Treated as unevidenced rather than as failed.
- The `wall-record-*` artifact from the CI run in §6 (artifact ID `8974801537`, 90-day retention)
  was not downloaded, so the runner's per-test failure list is unread. Its exit codes were read
  from the job summary.
- One section-number mismatch in the brief: the "zero-false-positive claim" is asked for as the
  packet's §3, but §3 is *Carried edits applied*. The claim is distributed across §2 and §6 F1.
  §5 below re-derives it on the substance.

---

## 2. Per-lane verdicts against done-when and the batch rules

### Lane A — `6714f7cd`, [#501] + [#502]

Done-when ([#501]): *runs on push, records the gate outcome retrievably, judges nothing, and the
owed ARCHITECTURE Ch2+Ch6 rows land with it.*

| Clause | Verdict | Evidence |
|---|---|---|
| runs on push | **NOT MET** | `on.push.branches: [main]` is declared and parses, but the workflow has never produced a push-triggered run. §6 is the diagnosis. |
| records retrievably | **MET, now proven** | Job summary table + `actions/upload-artifact@v4`, 90-day retention. Proven live for the first time by run `31127625224` (§6), which uploaded `wall-record-319f885d…` (8122 bytes, artifact `8974801537`). |
| judges nothing | **MET, with a stated exception** | The three measured legs carry `continue-on-error: true`. The job still reds on a *setup* failure (uv pin assertion, `uv sync`) — deliberate, and the Ch2 row says so in its own text. |
| ARCHITECTURE Ch2+Ch6 rows land with it | **MET** | Filed as an artifact (`…-technical-lane-a-architecture-rows.md`) and applied by the integrator; Ch2 gains the **server** Layer and **report-only** posture plus the organ row, Ch6 gains the **Post-merge (server)** mesh row. |

Footprint (`.github/workflows/`, `ARCHITECTURE.md`): **respected, and correctly**. The lane did not
touch `ARCHITECTURE.md` — it filed the rows forward, which is the lane-disjointness rule working.
The four conformances it did take are each verified:

- **hermetization** — `.github` added to `SANCTIONED_TIER1_DIRS` **in the same commit** as the
  ADR-101 amendment and the pinning test, matching the stated `tasks/` / `uv.lock` precedent.
- **parity root row** — `github-ci` EXTENDED to `{hub: MUST, corp-monorepo: LOCAL}` rather than a
  second `dir_tracked .github` row. The reasoning given (a second row double-matches the sweep and
  turns corp's SETTLED declaration into a WARN-undeclared) is sound and the audit's `fleet_parity`
  raises nothing about `github-ci`.
- **doc-counts** — `2417 → 2418`. Independently confirmed: `doc_claims` passes.
- **codemap** — `codemap-freshness` passes on a fresh regen-and-diff.

Prose-edge exclusion: no new undeclared prose edge appears in the audit's `undeclared_edges` list
attributable to lane A; the ten WARNs there all predate the batch.

**Lane A shipped without a terra review.** §5 is the compensating adversarial pass, and it found a
real defect (LA-1) that the review would have caught.

### Lane C — `5af0b33c`, [#504]

Done-when: *`:39` and `ARCHITECTURE.md:327` state the fail-closed posture, `:153`/`:169` are
untouched, and a terra review artifact records the diff.* **FULLY MET.**

- `scripts/block_ff_push.py:39` now reads *"Fail **CLOSED** (ADR-85 amendment 2026-08-03 §A6): an
  internal error RAISES and `main()` turns it into exit 2, refusing the push."* The retired string
  is gone — `grep "Fail-soft: any git error"` returns nothing.
- The ARCHITECTURE claim (cited as `:327`; now `:341` after the lane's +15 docstring lines and the
  integrator's Ch2/Ch6 inserts) reads **"fails CLOSED (exit 2) on internal error"**.
- **The forbidden lines are intact, verified structurally rather than by eye:** `git diff 6714f7c
  5af0b33c -- scripts/block_ff_push.py` is **ONE hunk, `@@ -36,7 +36,22 @@`**. Nothing below line
  58 was touched. The two fail-soft helper descriptions are byte-identical, relocated to `:168` and
  `:184` by exactly the +15 lines above them.
- Terra artifact: `docs/audits/2026-08-06-codex-lane-c-504-failclosed.md` (gpt-5.6-terra, 2 Critical
  / 0 High / 0 Medium / 0 Low). C1 accepted and fixed in-lane at `c49a03c2`; C2 rejected in-lane
  with reasons. Two defects in that artifact are recorded as **LC-1** in §5.

### Lane B — `a4f4f1e9`, [#503]

Done-when: *each site is corrected or recorded as intentional, and the DoD gating gap is closed or
filed.* **FULLY MET — all eight sites CORRECTED, none deferred.**

The one clause worth re-deriving rather than trusting was *"the validators table now matches all 17
live `.pre-commit-config.yaml` ids"*. Checked by set comparison, not by reading: the table's 17 ids
and the config's 17 ids are **set-identical** (`diff` of the two sorted lists is empty). The DoD
gating gap is CLOSED, not filed — `canonical_freshness` reports **9** canonical living files fresh
where it reported 8, measured from this seat's own run.

**Footprint finding (LB-1, §5):** lane B's diff includes `scripts/audit.py` and
`tests/test_reverse_dep_oracle.py`, neither of which is in the row's declared `footprint:`. The lane
is not at fault — the *row* is: its own done-when clause ("the DoD gating gap is closed") cannot be
satisfied inside the declared footprint. Lane B disclosed the excursion in its commit message,
which is the correct behaviour.

### The two ARCHITECTURE carries

Applied **verbatim**, both confirmed by reading the applied text against the source artifacts.
Lane C's two verification greps hold live today: `fail-soft to exit 0` returns nothing;
`fails CLOSED (exit 2)` returns the pasted line. Lane A's four anchors each bind uniquely.
The `last_reviewed` re-stamp claim is checkable and checks out: `git show a4f4f1e9:ARCHITECTURE.md
| wc -l` is **861**, exactly the figure the packet cites for the end-to-end re-read.

---

## 3. Row lifecycle — what was closed, and what was deliberately not

| Row | State before | Action | Why |
|---|---|---|---|
| [#501] | open | **left open** | The `runs on push` clause is unmet. §6. |
| [#502] | open | **left open** | Verdict explicitly OPEN, and the pilot measured nothing at all until LA-1 was fixed. |
| [#503] | open | **CLOSED** at `1447d063` | All eight sites corrected; gating gap closed; evidence quoted in the commit body. |
| [#504] | open | **CLOSED** at `1447d063` | All four done-when clauses met; evidence quoted in the commit body. |
| [#505] | open | **left open — this diverges from the brief** | See below. |

**[#505] is NOT closable, and the brief's "plausibly [#505]" does not survive contact with the
tree.** Two of its four done-when clauses are unevidenced:

- Clause 1, *"a fresh seat runs a full batch from repo artifacts alone"*, is **falsified by the
  batch's own packet, §8**: *"No batch manifest pre-existed in the tree — lane contracts were
  delivered as prompts, not committed artifacts."* A fresh seat could not have run batch 1 from
  the repo, because the plan was never in the repo.
- Clause 2, *"batch-1 executes under it with exactly 2 operator touches"*, has no recorded
  measurement anywhere in the tree.
- Clauses 3 and 4 hold: the hygiene WARN (`check_stale_worktrees`) and the branch-prefix enum
  (`validate_branch_naming.py`) are both validator-checked, and `/lane-integrate` walks a
  mechanical checklist.

Closing it would ratify the manifest gap as satisfied in the same window Ch8 was hardened to
require the opposite. Mechanics used for the two closes: ADR-107 §6.3 — task-file `status: open →
closed` (retire, never delete; both bodies preserved), manifest node removed, `BACKLOG.md`
regenerated by `gen_task_tree.py --emit-source`. 202 → 200 tasks. `--check` ok, `validate_backlog`
ok, `validate_git_backlog` ok.

---

## 4. Mechanism check — did the system catch its own errors?

### Gate firings in the batch range, classified independently

| # | Gate | What it did | Verdict |
|---|---|---|---|
| 1 | `validate-hermetization` Rule B | Refused `docs/audits/2026-08-06-lane-a-architecture-rows.md` | **TRUE** — re-derived: `rule_b_violation()` refuses that exact name today and allows the `-technical-` rename. |
| 2 | `validate-hermetization` Rule B | Refused `docs/audits/2026-08-06-lane-c-arch-327.md` | **TRUE** — same probe; the `-verification-` rename is allowed. |
| 3 | `audit-index-freshness` | Real merge conflict on the generated index at the lane-C merge | **TRUE** — a hand-merge would have read correctly and failed its own gate. Resolved by `gen_audit_index.py --write`; the gate then passed. Counts trace exactly: 402 → 403 (A) → 405 (C, +2) → 405 (B) → 406 (integrator's own packet). The packet's "405" is correct *at the lane-C merge*, which is where it is stated. |
| 4 | `audit-health` / `journal_spine_anchor` | Blocked the lane-C merge commit | **TRUE** — `6714f7cd` genuinely had no anchor at that instant. Discharged with `SKIP=audit-health` on two intermediate merges (surgical, not `--no-verify`). This is F1. |
| 5 | `journal_spine_anchor` | FAILed on `9cf4e33e` after the integration merge | **TRUE** — F1b. Surfaced as 2 extra suite REDs. |
| 6 | `claude-rosters-freshness` | Forced regeneration of `.claude/generated/commands-repo.md` after lane B changed `override.md` frontmatter | **TRUE** — regen present in `59b191c5`. |
| 7 | `doc_claims` / doc-counts | Forced the `2417 → 2418` bump in lane A | **TRUE** — the count is right; `doc_claims` passes. |
| 8–9 | `review_artifact_coverage` ×2 | `6714f7cd` and `a4f4f1e9` are code-impact merges with no linked review artifact | **TRUE** — both genuinely touched `scripts/` and/or `tests/`, and neither carries a terra artifact. |
| 10 | `review_artifact_coverage` ×1 | `5af0b33c`'s linked artifact carries no parseable `**Tally:**` line | **TRUE** — and **the packet does not mention this one at all.** |
| 11 | `block-ff-push` + `block-unanchored-push` | Passed at push | Correct — the range was anchored by then. |

**Zero false positives — the packet's claim is CONFIRMED.** Eleven firings, eleven true. **But the
count of `review_artifact_coverage` WARNs is 3, not the +2 the brief carries.** The third is a
different class (persistence ≠ machine-auditability) and it is the one nobody wrote down.

### Teardown — verified live, both sides

`git worktree list` → primary only. `git branch -a | grep worktree` → nothing. `.claude/worktrees/`
→ absent. `git ls-remote --heads origin` → `main`, three explicitly-protected
`claude/conformance-*`, and `automation/fleet-audit`. **No `worktree-*` branch survives locally or
on the remote**, so both halves of the two-branch teardown rule discharged. The audit's
`stale_worktrees` and `no_sibling_orphans` checks both pass.

### The spine

Five merges on the first-parent spine in the range, all `--no-ff`, in the planned order
A → C → B → integration → anchor-repair. `journal_spine_anchor` from this seat, against a corrected
`main` ref: **`[OK] every first-parent spine entry above the ADR-85 disposition floor 24882f8cc is
JOURNAL-anchored`**. The three `no_ff_merges` WARNs that remain are all from June and untouched by
this batch.

### The F1b repair shape — mechanically sound, with one process finding

The repair works, and the arithmetic is checkable. `introduced(319f885d)` is
`[319f885d, 48a0cb67, 0518e3a6]`; the JOURNAL names `48a0cb67`, so the repair merge anchors itself.
`introduced(9cf4e33e)` is `[9cf4e33e, ed9de2b5]`; the added *"Integration arc: `ed9de2b5` … merged
at `9cf4e33e`"* line names `ed9de2b5`, so the integration merge is anchored. Both discharge cleanly.

**Finding IA-1 (§5): the repair was made by editing an already-committed JOURNAL entry in place.**
`0518e3a6` does not prepend a new entry — it inserts two blocks into the existing `2026-08-06 (h)`
entry, which had already landed at `ed9de2b5` and merged at `9cf4e33e`. `JOURNAL.md` is append-only
newest-first (CLAUDE.md §4 lifecycle, §5 rule 2). The append-only-conformant alternative existed
and was equally effective: `is_anchored()` matches a short SHA **anywhere in the file**, not
per-entry, so a new `2026-08-06 (i)` entry naming `ed9de2b5` would have discharged the same anchor.
This matters beyond tidiness — because the predicate reads the whole JOURNAL at the working
tree/tip, an in-place edit is a **retroactive anchor discharge**, which is precisely the
tamper-evidence the ADR-85 amendment moved the teeth to protect. Not auto-fixed: the file is
append-only and this audit will not edit it further. Wants an architect ruling (§7 R-3).

---

## 5. Reviewer coverage and the adversarial pass

Two surfaces shipped without terra: **lane A** (code-impact — a workflow plus four gate
conformances) and **the integration arc**. Both are reviewed below. Nothing here is auto-fixed
except LA-1, which is S-mechanical by the brief's own bar.

| ID | Sev | Finding | Disposition |
|---|---|---|---|
| **LA-1** | **S-high** | **The [#502] mutation pilot measures nothing.** `[tool.mutmut] pytest_add_cli_args = ["-p", "no:xdist"]` unloads the xdist *plugin*, which also unloads the `-n` *option* that `[tool.pytest.ini_options] addopts = "-n auto"` already supplies. Every mutant's pytest exits 4 on `unrecognized arguments: -n` before collecting a test. | **FIXED** at `27c37ae3` → `["-n", "0"]` (xdist's own in-process mode; addopts is prepended, so the later `-n 0` wins). S-mechanical: the intent was already written in the file's own comment; only its expression was wrong. |
| **LA-2** | S-medium | `astral-sh/setup-uv@v5` is passed `python-version-file: ".python-version"`, which is **not a valid input**. CI emits `##[warning]Unexpected input(s) 'python-version-file'` on both jobs. The input is silently ignored, so the line claims a runner-Python pin it does not deliver (uv reads `.python-version` itself during `uv sync`, so the effect is benign today — the *claim* is not). | **PROPOSE.** One-line fix: drop the input, or switch to `python-version:`. Not auto-fixed — which of the two is right is a decision about whether the action should install Python at all. Belongs in the same push that discharges [#501]'s verification. |
| **LA-3** | S-low | The wall re-runs **3 of the 17** client-side pre-commit gates (`pytest` — not a hook at all —, `audit.py health`, the anchor backstop). `ruff` and 13 others are not re-run server-side, so a `--no-verify` push carrying a ruff violation still leaves no server record. ARCHITECTURE Ch6 describes the organ as *"the client-side gate set re-run off-host"*, which over-claims. | **PROPOSE.** Either narrow the Ch6 wording to "three legs of", or add `pre-commit run --all-files` as a fourth recorded leg. The second is the better fix and is cheap; it is an architect call because it changes what the record means. |
| **LA-4** | S-low | The `mutation-pilot` job runs on **every** push to `main` — no `paths` filter, no dispatch gate — so a "pilot" with no verdict quietly becomes standing infrastructure. Measured cost today: 68s/push. | **PROPOSE**, file against [#502]: gate it behind `workflow_dispatch`, or a `paths:` filter on `scripts/fleet_analytics.py`, until the ADOPT/REJECT verdict lands. |
| **LA-5** | S-low | The summary table interpolates `$(tail -1 pytest.out)` into a markdown table cell; a last line containing `\|` breaks the table. | **PROPOSE** (cosmetic). |
| **IA-1** | S-medium | The anchor repair edited a committed JOURNAL entry in place rather than prepending. §4. | **PROPOSE — architect ruling.** Either sanction "same-session amendment of the current entry" explicitly in CLAUDE.md §5.2, or rule it out and require a new entry. Silence here is what let it happen. |
| **LB-1** | S-low | Lane B's declared `footprint:` omits `scripts/audit.py` and `tests/test_reverse_dep_oracle.py`, which its own done-when clause forces it to touch. Row defect, not lane defect. | **PROPOSE**: when a done-when implies a code change, the footprint names the code file. Same family as F3 (a contract is checkable at authoring time) — folded into the Ch8 wording landed at `297af6e1`, but not made mechanical. |
| **LC-1** | S-low | Lane C's terra artifact (a) carries no `**Tally:**` line — WARN #10 in §4 — and (b) records HEAD `47331e26`, one commit *before* the merged lane HEAD `c49a03c2`, so the post-C1-fix diff has no recorded review. | **PROPOSE**: the `Tally:` line is a template fix for future codex artifacts; the re-review question belongs to the [#480] advisory class, which already tracks it. |
| **IA-2** | — | `last_reviewed` re-stamp claim ("all 861 lines") | **CONFIRMED, no defect.** `git show a4f4f1e9:ARCHITECTURE.md \| wc -l` = 861. |
| **IA-3** | — | Packet §2's "405 documents" vs the tree's 406 | **CONFIRMED accurate in context** — 405 is the truth at the lane-C merge, where the sentence sits. The 406th is the packet itself. |

---

## 6. The recorder diagnosis — why push `319f885d` produced no run

**This is the packet's one unclosed claim, and it is now closed.**

### The claim is true

`GET /actions/workflows` → one workflow, `report-only wall`, id `328846990`, **`state: active`**,
`created_at: 2026-08-06T21:29:36+02:00`. `GET /actions/workflows/report-only-wall.yml/runs` →
**`total_count: 0`**. The repository's entire run history is 24 runs, all `Nightly Conformance
Triage`, the newest 2026-06-25 — the organ [#255] retired.

### Ruling out the candidates, one at a time

- **Delay — RULED OUT.** The workflow was registered at 19:29:36 UTC (the push moment; later than
  every commit in the batch, the last being `319f885d` at 19:20:14 UTC). First check was 60 minutes
  later, and the dispatched run below started **in 2 seconds**.
- **Trigger syntax — RULED OUT.** `yaml.safe_load` parses `on:` to
  `{'push': {'branches': ['main']}, 'workflow_dispatch': None}`.
- **Default-branch / branch filter — RULED OUT.** The push was to `main`; `origin/main` is
  `319f885d`.
- **Workflow disabled — RULED OUT.** `state: active`, not `disabled_manually` /
  `disabled_inactivity` / `disabled_fork`.
- **Repo-level Actions state, permissions, or billing — RULED OUT, by experiment.** The
  `/actions/permissions` endpoint is blocked by this session's proxy and the MCP surface does not
  expose it, so it was settled the only remaining way: a `workflow_dispatch` on `main`, which is a
  trigger the workflow itself declares. **Accepted 204, run `31127625224` created, `run_number: 1`,
  both jobs completed `success`.** Actions is enabled, the runner works, minutes are available, and
  the workflow is executable.

### Verdict

**Not a delay, not repo-level state, and not a trigger defect in the YAML. The residual is the
workflow-landed-in-the-same-push edge: GitHub indexed the new workflow file on that push (that is
what `created_at` records) but dispatched no run for the push that introduced it.** Nothing needs
fixing in the YAML or in repo settings, and **it is self-correcting** — the next push to `main`
finds the workflow already registered.

**Falsifiable, with a named check.** If the next push to `main` also yields no run, this diagnosis
is wrong and the space reopens. The check is one command after that push:
`gh api repos/rdwornik/dev-knowledge/actions/workflows/report-only-wall.yml/runs --jq .total_count`
— expected ≥ 1, and it should name that push's SHA.

### What the dispatched run bought, and what it did not

**It bought the first real evidence that the recorder works end to end.** Every step of the
`record` job succeeded: checkout at `fetch-depth: 0`, the pinned `uv 0.11.19`, the pin assertion,
`uv sync --locked --group analytics` in **2 seconds**, pytest (2 minutes, exit 1), `audit.py health`
(exit 1), the anchor leg, the summary table, and an 8122-byte artifact. The pyright step classified
the runner as **`unprovisioned (modelled: 7/8 proven, 1 skip)`** — the shape ARCHITECTURE models,
not the unmodelled third one. The `workflow_dispatch` guard behaved exactly as designed:
`journal anchor | n/a | skipped -- no push range`.

**It did not discharge [#501]'s verification, and must not be read as doing so.** Two conditions
remain: the run was `workflow_dispatch`, not `push`, so the **anchor leg has still never executed**;
and no deliberate RED was injected, so "the run shows green with the red recorded" is unproven.
The `ARMED (never fired)` parenthetical in ARCHITECTURE Ch2 stays until a push-triggered
red-making run exists.

**Cost and disclosure:** one unscheduled run on `main`, ~3.5 minutes of Actions time across two
jobs, initiated by this audit and not by the architect. It appears in the Actions history as
`run_number 1`, event `workflow_dispatch`. It wrote nothing to the repository (`permissions:
contents: read`).

---

## 7. Drafts for architect adjudication — NOT landed

### R-1 · ADR-110 amendment draft: the integrator's intermediate merges (F1)

> ## Amendment — DRAFT, not ratified: intermediate integration merges as a declared arc
>
> - **Source:** batch-1's first live run. `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`
>   §6 F1 and this verification's §4.
> - **The problem, stated structurally.** The batch JOURNAL entry names the lane merge SHAs, so it
>   is writable only *after* the merges. Each merge meanwhile lands an unanchored first-parent
>   spine entry, and `audit-health` evaluates **per-commit**. Anchoring is retrospective; the
>   commit-time backstop is not. The two cannot both be satisfied between merges, and batch 1
>   resolved it with `SKIP=audit-health` on two intermediate merges — surgical, disclosed, and
>   still a gate turned off by hand at the exact moment the protocol makes it fire.
> - **What is NOT wrong.** The pre-push organ `block_unanchored_push` discharges **range-level**
>   and was satisfied normally. The `journal_spine_anchor` audit backstop reads the whole spine and
>   was clean at close. Only the per-commit evaluation is structurally unsatisfiable mid-queue.
> - **Proposed decision.** `check_journal_spine_anchor` gains a **declared integration arc**
>   exemption, evaluated at the push/batch boundary rather than per-commit: a spine entry is exempt
>   from the commit-time evaluation when it is a `--no-ff` merge of a `worktree-lane-*` branch AND
>   an open batch is declared by a committed batch manifest (per the Ch8 "manifest committed at
>   dispatch" rule landed 2026-08-06). The exemption expires with the manifest: the range-level
>   pre-push leg and the whole-spine backstop are unchanged, so nothing ships unanchored — the
>   anchor obligation simply lands where it is satisfiable.
> - **Why a manifest is the right key.** It is the only artifact that makes "a batch is open" a
>   fact in the tree rather than a claim in a chat. Keying on the branch prefix alone would exempt
>   any lane merge forever; keying on the manifest makes the exemption as short-lived as the batch.
> - **Rejected alternative:** keeping `SKIP=audit-health`. It disables **every** check in the
>   registry, not the one that cannot pass, and it trains the reflex the ADR-85 amendment exists to
>   remove.
> - **Honest limit:** this adds a second exemption surface to a gate whose value is having none.
>   The reviewer should weigh that against the current state, which is a documented instruction to
>   turn the whole gate off twice per batch.

### R-2 · ADR-85 amendment draft: the stale `:322-324` prose

ADR-85 is immutable; nothing was edited. Text for the architect to land as an in-file amendment
(same shape as the existing `## Amendment — 2026-08-03` block, per ADR-94):

> ## Amendment — DRAFT, not ratified: §A6's fix has landed; the pre-fix diagnosis is now history
>
> - **What is stale.** The "Consequences"/foreclosure passage (≈`:321-323`) reads:
>   *"`block_ff_push.py:205-207` **currently fails soft** — returning 0 and 'allowing push' on any
>   internal error — which is exactly the defect §A6 orders fixed. Until that fix lands, the
>   prevent organ can be silently absent."* Both halves are now false: §A6's fix **landed** in the
>   same 2026-08-03 arc, and the organ fails CLOSED (exit 2). The line reference has also drifted.
> - **Why it is not simply wrong.** It is the amendment's own pre-fix diagnosis, so it is correct
>   *as history*. The defect is that it is written in the present tense with no marker, and a
>   reader arriving cold takes it for current state — which is exactly the [#503] failure class
>   ("the thing it describes was retired underneath it"), arriving inside a governance document
>   rather than a living one.
> - **Proposed decision.** Record here that the passage describes the **pre-2026-08-03 state**;
>   the live posture is fail-CLOSED at `scripts/block_ff_push.py:39` and `:129`/`:194-195`, doc'd at
>   `ARCHITECTURE.md:341` and in the CONTRIBUTING validators table. The passage itself stays
>   unedited, per immutability.
> - **Scope:** documentation only. No decision content changes; §A6 is unaffected.

### R-3 · One-line ruling wanted (no draft — it is a yes/no)

**Is amending the current session's already-committed JOURNAL entry in place permitted?** IA-1.
Either sanction it narrowly in CLAUDE.md §5.2 (same session, same day, additive only) or rule it
out. As it stands the rule says append-only, the practice was an in-place edit, and the predicate
that reads the file cannot tell the difference — which makes the anchor retroactively editable.

---

## 8. LESSONS from the drill

**What the drill proved.**

- **Lane disjointness works, and it works predictively.** Lane A foresaw the `CONTRIBUTING.md`
  collision it would cause and handed it to the integrator instead of editing lane B's footprint.
  That is the rule doing its job before a conflict exists, not after.
- **Regeneration is the right conflict resolver for generated files.** The `docs/audits/README.md`
  collision was resolved by `--write`, and the gate then *confirmed* the resolution. A hand-merge
  would have produced a file that reads correctly and fails its own hook.
- **The gate mesh has zero false positives across eleven firings.** Everything that fired was
  right. On the [#480] advisory-before-hard bar, this is one clean window of the two required.
- **The recorder works.** Proven end to end for the first time (§6), including the load-bearing
  `fetch-depth: 0` and the exact uv pin.

**What the drill broke.**

- **The per-commit anchor backstop is unsatisfiable inside a serial merge queue** (F1), and the
  standing workaround is "turn the whole gate off, twice". R-1 addresses it.
- **The integrator is the one seat that can produce a one-commit branch** (F1b), and a one-commit
  branch is structurally unanchorable. Invisible until after the merge lands.
- **The contract-authoring surface produced two gate-refused paths in one batch** (F3) while
  `/preflight` — the organ built for exactly that — sat unused.
- **No batch manifest existed**, so checklist item 4 passed on half its evidence and clause 1 of
  [#505] cannot be evidenced at all.
- **The self-graded packet missed one of its own gate firings** (the third `review_artifact_coverage`
  WARN) and shipped a pilot that measures nothing (LA-1). Both were found by a second seat, not by
  the integrator — which is the argument for keeping this verification step.

**The generalizable lesson.** Every finding in F1/F1b/F3 has the same shape: **a rule that is
correct per-object and unsatisfiable per-process.** Anchoring is right per commit and impossible
per queue; path grammar is right per file and unchecked per contract. The fix in each case is to
move the evaluation to the boundary where the obligation is actually dischargeable — which is what
R-1 proposes and what the "manifest committed at dispatch" rule does for F3.

---

## 9. GO / NO-GO for a 6-lane batch 2

**Verdict: GO — conditional on three items landing before dispatch, none of which is large.**

The protocol survived its first run, the gate mesh was honest throughout, and every structural
defect it exposed is now either fixed, doctrine, or a drafted amendment. Widening 3 → 6 is within
ADR-110 §2's own "drilled at 3, designed for 4–10" envelope.

**Conditions:**

1. **Commit the batch manifest at dispatch.** Non-negotiable at width 6: at 3 lanes the integrator
   can hold the plan in context, at 6 they cannot, and footprint disputes have nothing to arbitrate
   against. Now Ch8 doctrine (`297af6e1`); batch 2 is its first exercise.
2. **Adjudicate R-1, or pre-authorize the skip in writing.** At 3 lanes this was two `SKIP=` merges;
   at 6 it is five. An undecided rule applied five times is how a workaround becomes practice.
3. **Give each lane its review artifact up front.** Two of three lanes shipped code-impact without
   terra. At width 6 that scales to four unreviewed code surfaces, and LA-1 is the demonstration
   that the gap costs something real.

**≥3-feature-lane quota:** the ≤1/4 process-lane cap binds from batch 2 by its own terms, and batch
1 ran **3/3 process lanes**. At width 6 the cap allows **at most 1** process lane — so **≥5 of 6
must be product/consumer work**, which is a stricter bar than the brief's "≥3 of 4" phrasing (that
figure is the cap read at width 4). **This is the binding risk: the fleet's open set is
methodology-heavy, and the cap has teeth only if the non-process lanes can actually be filled.**
Ch8's own escape is to report the shortfall and run narrower — running 6 lanes with 3 process lanes
would be a breach, not a compromise.

**Named risks at width 6:**

| Risk | Why width makes it worse | Mitigation |
|---|---|---|
| Integrator serialization | 6 merges × (conflict + suite) on one seat; F1's skip fires 5× | R-1; keep the run-suite-once contract |
| Cross-lane falsification | Batch 1 hit 2 at width 3 — pairwise surface grows ~quadratically | The manifest makes footprints comparable before dispatch |
| Shared generated indexes | `docs/audits/README.md` collided at width 3; at 6 it collides most merges | Pre-assign audit filenames in the manifest, resolve by regen always |
| Process-lane cap | See above — the quota, not the machinery, is the likely failure | Fill non-process lanes at planning time or run narrower |
| Review coverage | 2 unreviewed code surfaces at 3 → up to 4 at 6 | Condition 3 |

---

## 10. Morning packet — paste-ready

```
BATCH-1 NIGHT AUDIT — independent verification (2nd seat). Branch:
claude/night-audit-batch-1-verify-27hai3 (7 commits, pushed, NOT merged).

HEADLINE
- Batch 1 holds up. 11 gate firings, 11 TRUE, zero false positives — packet claim CONFIRMED.
- Spine clean: journal_spine_anchor OK across all 5 merges. Teardown clean, local AND remote.
- 3 things the packet missed: a 3rd review_artifact_coverage WARN, a pilot that measures
  nothing, and an in-place JOURNAL edit.

COMMITS ON THE AUDIT BRANCH
  27c37ae3  fix(mutmut)   the [#502] pilot measured nothing — `-p no:xdist` kills `-n auto`
  3879d28b  feat(enum)    admit `automation/` as the 4th machine lane prefix (+ STANDING_RULINGS B5)
  82698be5  docs(intake)  repair intake #27's two dangling §D refs (erratum in note:)
  ef251cba  docs(template) 02_METHODOLOGY.md.tmpl carries [#441]'s four-condition test
  297af6e1  docs(playbook) Ch8 hardening x4 — F3 paths, F1b >=2 commits, F2 docs/-branch, manifest
  1447d063  docs(backlog) closes [#503], closes [#504] — evidence quoted in the commit body
  <dossier>  docs/audits/2026-08-06-technical-batch1-verification.md + JOURNAL

ROWS
  CLOSED  [#503] [#504] — all done-when clauses met, evidence quoted.
  OPEN    [#501] verification owed · [#502] verdict OPEN.
  OPEN    [#505] — I DISAGREE with the brief. Clause 1 ("a fresh seat runs a batch from repo
          artifacts alone") is falsified by the packet's own §8: contracts were prompts, not
          committed artifacts. Clause 2 (2 operator touches) has no recorded measurement.

RECORDER DIAGNOSIS — [#502]/[#501]'s open claim, now CLOSED
  Not delay, not repo state, not a YAML defect. Proven by dispatching the workflow:
  run 31127625224, run_number 1, BOTH JOBS GREEN. Actions is enabled and the recorder works
  end to end (uv pin, fetch-depth 0, 3 legs, artifact uploaded).
  Residual cause: the workflow landed in the same push that would have triggered it.
  SELF-CORRECTING — the next push to main will fire it. Falsifier if I'm wrong:
    gh api repos/rdwornik/dev-knowledge/actions/workflows/report-only-wall.yml/runs --jq .total_count
  DOES NOT discharge [#501]: dispatch has no push range, so the anchor leg is still unexercised
  and no RED was injected. "ARMED (never fired)" stays.
  Disclosure: I initiated one unscheduled run on main, ~3.5 min of Actions time. Wrote nothing.

NEEDS YOUR ADJUDICATION (all drafted in dossier §7, nothing landed)
  R-1  ADR-110 amendment — replace `SKIP=audit-health` for the integrator's intermediate merges
       with a manifest-keyed integration-arc exemption evaluated at the push boundary.
       At 6 lanes the current workaround fires 5x.
  R-2  ADR-85 amendment — ADR-85 :322-324 still says block_ff_push "currently fails soft".
       Immutable, so drafted not edited.
  R-3  YES/NO — may a session amend its own already-committed JOURNAL entry in place?
       The anchor repair did (0518e3a6 edited the (h) entry rather than prepending). It works,
       but it makes anchor discharge RETROACTIVE, and the rule says append-only.
  LA-2 setup-uv@v5 `python-version-file:` is not a valid input — CI warns, input ignored.
       Drop it or use `python-version:`? Ride it with the [#501] verification push.
  LA-3 Ch6 says the wall re-runs "the client-side gate set". It re-runs 3 of 17.
       Narrow the wording, or add `pre-commit run --all-files` as a 4th leg?
  LA-4 mutation-pilot runs on EVERY push with no verdict pending. Gate it behind dispatch/paths?
  LC-1 lane C's terra artifact has no **Tally:** line and reviews 47331e26, one commit before
       the merged lane HEAD. Template fix + the [#480] class.
  ARCHITECTURE Governing-ADRs roster still ends at ADR-109 — left alone, your editorial call.

BATCH 2: GO, 3 conditions
  1. commit the manifest at dispatch (now Ch8 doctrine)
  2. adjudicate R-1, or pre-authorize the skip in writing
  3. every lane gets its review artifact up front
  QUOTA WARNING: at width 6 the <=1/4 process cap allows AT MOST 1 process lane, so >=5 of 6
  must be product/consumer work — stricter than the ">=3 of 4" phrasing in the brief.
  Batch 1 ran 3/3 process. This is the binding risk, not the machinery.

NOT DONE / HONEST LIMITS
  - The suite is not reproducible in this container (PATH-only pyright shape, no siblings,
    repo dir named dev-knowledge not .dev-knowledge). 14/2419 fail here, all attributed to
    the environment, none to the batch. Your host's verdict is not derivable from here.
  - audit-health cannot pass in this container (`repos registered (none)`), so every commit
    carries SKIP=audit-health with the reason in its message. Run manually before each.
  - The CI run's per-test failure list is in artifact 8974801537; I did not download it.
```
