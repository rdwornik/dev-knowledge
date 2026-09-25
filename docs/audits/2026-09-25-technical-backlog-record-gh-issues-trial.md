# Backlog record — the live GitHub Issues trial (O2), the re-weighted O1-vs-O2 matrix, the sol check and the Astra round

- **Date:** 2026-09-25 · **Lane:** `lane-trial-gh-issues` (branch `worktree-lane-trial-gh-issues`, base `2ae86d07`)
- **Order:** `to-cc/BATCH-TRIAL-GH-ISSUES-2026-09-24.md` items 1-9, as re-routed for item 4 by
  `to-cc/AMEND-BATCH-WAVE5B-N1-COPILOT-2026-09-25.md` §3; contract `LANE-5B-8-trial-gh-issues.md`
  (batch WAVE5B-N1 row 8).
- **Decision it feeds:** ADR-122 (Proposed; amended 2026-09-25 with this outcome, still Proposed).
  **Prior records:** `docs/audits/2026-09-24-technical-backlog-record-research.md` (Parts A-D; the 20-row
  sample of §3 Part C is reused here unchanged), `docs/audits/2026-09-24-technical-backlog-record-debate.md`.
- **Provenance:** ADR-122 (the decision under trial), ADR-120 (the spine files, dispatches and closes
  rows), ADR-108 §A (functional vs technical question routing).
- **Immutable** once landed (audits are immutable; supersede with a new file).

## 0. Routing — what served each step

```
step | requested | served | evidence
orchestrate, trial items 1-3 and 5-8, write | claude-opus-5-5 | Claude Opus 5.5 (this session) | session
reader harness (item 3) | Sonnet subagent | Sonnet subagent (Agent tool, model sonnet), 110 tool calls, 75 min | its report, §2.3
item 4 implementation | Copilot CLI, claude-opus-5.5 | claude-opus-5.5 (usage file `currentModel`), 41 requests | copilot-usage.json
item 4 code review | Codex terra | gpt-5.6-terra, 54,557 tokens | codex log "model: gpt-5.6-terra"
item 9 independent check | Codex sol | gpt-6-sol, --search, read-only, 115,506 tokens | codex log "model: gpt-6-sol"
item 9 debate round | Codex Astra | gpt-6-astra, read-only, 44,004 tokens | codex log "model: gpt-6-astra"
```

No SUBSTITUTION: every routed tool answered with the id requested. `/context` and `/cost` cannot run
in a headless background session; recorded as not run (the session file says so).

## 1. The scratch repository

- **Name: `rdwornik/dk-trial-gh-issues-20260925`** (public, on the hub's own account per AMEND5 §1 Q2),
  created 2026-09-25T00:35:52Z by `gh repo create`. Tree = a history-less snapshot of the hub at
  `2ae86d07` (`git archive`), its three hub workflows removed so none runs there, plus `TRIAL.md`, an
  issue form and two trial workflows. History was left out on purpose: pushing 8,361 commit messages
  would have fired the `#N` trap (item 5) uncontrolled; it was witnessed with two controlled commits
  instead.
- **Deletion is the operator's act** (the token has no `delete_repo`):
  `gh repo delete rdwornik/dk-trial-gh-issues-20260925 --yes`.
- Issue form `.github/ISSUE_TEMPLATE/task.yml` (the schema, item 1): required Legacy id, Description,
  Criteria, Verifier kind (dropdown command / review / unresolved), Verifier, Wave, Links, Provenance;
  optional Notes and a `Legacy row (verbatim)` carrier. Labels: `task`, `legacy`, `status:<s>`,
  `P<n>`, `size:<S|M|L>`, `theme:<E>`, `story:<S>`, `wave:unassigned` (no row carries a wave).
- Workflows: `ci.yml` (on PR: ruff + pytest over the test files the PR adds or changes; a PR changing
  no test fails — the runnable check), `issues-snapshot.yml` (item 6).

## 2. The trial, items 1-9

### 2.1 Item 1 — the 20 rows become issues through `gh`

- The sample of research record §3 Part C (ids 4, 190, 290, 347, 393, 428, 463, 496, 532, 568, 601,
  634, 669, 702, 743, 784, 829, 907, 940, 973; 12 open, 6 closed, 2 deferred) → issues **#1-#20** in id
  order by `gh issue create --body-file -` (a 114-line migration script over the repo's own parsers
  `export_backlog_view.parse_frontmatter`, `gen_task_tree.extract_body`).
- **2.16-2.84 s per create; 20 rows, labels and the 6 closes in 1 min 53 s.** The 6 closed rows were
  closed `--reason completed`; the 2 deferred rows stay OPEN with `status:deferred` — GitHub has two
  states plus `state_reason` (completed / not planned / duplicate), so `deferred` is a label.
- Verifier kind by a backticked-command classifier over each Done-when: **1 of 20 `command`** (#463),
  19 `review` — the same scarcity the research record measured (at most 61 of 667).
- **Schema, probed (5 writes that O1's model refuses):** a body with an unknown section and no
  verifier kind — accepted (#23); two exclusive status labels at once — accepted (#22); `gh issue
  create --label status:bogus` and `--label P9` — refused, **client-side only** (`could not add label
  … not found`); the same unknown label through the raw REST API (`labels[]=status:bogus`) — **the
  issue AND the label were created** (#24). **Server-side refusals: 0 of 5.** The issue form binds the
  web UI only; it does not bind `gh` or the API.
- **Links (dependencies):** `POST /issues/13/dependencies/blocked_by` expressed #669's `depends-on:
  #664` (#664 is outside the sample, so a stub issue #21 was filed as its target). The reverse link —
  a cycle — was **refused HTTP 422** ("would create a cycle"); a dangling issue id **refused HTTP 404**.
  Sub-issues: add, list and remove all worked. Dependencies are typed and integrity-checked on the
  server; kill-candidates, implements, provenance and serialize-group remain body text.
- **Projects v2 fields: NOT tried.** Both `gh` tokens lack the `project` / `read:project` scope
  (`gh project list` refused); adding it is an interactive browser grant — `OPERATOR-ACTION`.
- **Identity:** issue numbers are sequential and shared with PRs; legacy ids were not preservable
  (#4 → #1, #190 → #2, …). The **filename is not derivable either**: `gen_task_tree.task_filename`
  reproduced only **12 of 20** filenames (the slug froze at filing), so a `Legacy file` section was
  added to every body — a schema change on O2 is a rewrite of every issue body (20 `gh issue edit`,
  mean 2.48 s, max 3.27 s), with no migration tool.

### 2.2 Item 2 — closing by `Closes #N`

- PR #25 (item 4's) carried `Closes #2`. With a ruleset requiring a PR and the status check `check`,
  `gh pr merge` of the red PR was **refused** ("the base branch policy prohibits the merge"). The
  ruleset was then deleted and the PR merged at 01:13:08Z: **issue #2 closed COMPLETED at 01:13:09Z,
  `closedByPullRequestsReferences: [25]`**, a `closed` event on its timeline. `Closes #N` is O-6 for
  free, and CI becomes the closing gate with no code — **but** a ruleset requiring PRs on `main` also
  blocks the snapshot bot's direct push (item 6) unless it is given a bypass or writes elsewhere; the
  combined arrangement was not run end to end.

### 2.3 Item 3 — the compat renderer against the readers

- Renderer (71 lines): `gh issue list --json number,title,state,stateReason,labels,body` → per issue,
  the body's sections → `gen_task_tree.TaskRow` → **the repo's own writer**
  `gen_task_tree.emit_task_file_text` (status from state + labels) → `tasks/<Legacy file>`. One
  `gh issue list` of all issues: 1.83-1.95 s.
- **With the verbatim carrier: 20/20 byte-identical** (filename included, once carried). **From the
  typed sections only (no carrier): 16/20 byte-identical, 20/20 clause-set-identical** — the 4
  differences are clause order (463, 702, 743, 784), the same class O1 recorded without its carrier.
- The 13 readers of research record §3 (R1-R14, R8 absent), rebuilt by a Sonnet subagent and run on
  three `git clone --local` copies of the scratch repository (baseline; the 20 row files replaced by
  each variant), output per reader compared with the baseline's:

```
variant | readers equal to baseline (of 13) | what broke
O2 compat, carrier | 13 | -
O2 compat, typed sections only | 12 | R3 export_backlog_view: 4/20 exported rows differ (463, 702, 743, 784 — clause order, carried verbatim into the export)
```

  As in the research record, "equal" is not "green": R4 (`preflight_contract`) exits 1 at baseline,
  and it reads the committed BACKLOG.md, which no variant regenerates — its "equal" says nothing about
  the row files. The harness had to force `PYTHONUTF8=1` for its reader subprocesses (cp1252 console
  crashes on em-dashes would have faked a reader difference). O2's carrier compat therefore ties O1,
  O5 and beads (13/13); without the carrier it beats git-bug (10) and Backlog.md (6).
- Harness defect, found and corrected: 21 of 22 multi-line bodies came back CRLF. The one created with
  an inline `--body` (#23) kept LF: the CRLF was introduced by the harness (Python
  `subprocess(text=True)` on Windows translates `\n` on the stdin pipe to `gh --body-file -`), **not
  by GitHub**. The renderer normalises it; a real migration must write bodies in binary mode.

### 2.4 Item 4 — Copilot (re-routed to the CLI under the Enterprise seat)

- The cloud agent (issue → PR on GitHub's side) is recorded as **not applicable outside the
  enterprise**, per the contract — not probed, no issue assigned to it. (The sol check notes GitHub
  offers the cloud agent on paid individual plans; for this fleet that is a purchase, an operator
  act — §4.)
- Issue #2 (legacy [#190], the intra-file duplication detector — bounded, a test-shaped Done-when) in
  a worktree of the scratch clone on `copilot-item4-2`:
  `$null | copilot -p "<issue #2 title + body>\n\nImplement it in this repository. Do not commit."
  --model claude-opus-5.5 --allow-all-tools --deny-tool='shell(git commit)' --deny-tool='shell(git
  push)' --deny-tool='shell(gh:*)' --no-ask-user -s --no-color --usage-output-file … --log-dir …`,
  with `PYTEST_ADDOPTS=-n 0` set by the harness (memory headroom; not a prompt change).

```
measure | value
wall-clock | 640.5 s (10.7 min), exit 0
model served | claude-opus-5.5 (usage file currentModel), 41 requests, 1 premium request
AI credits (usage file) | totalNanoAiu 196,516,500,000 = 196.5
credits_used counter | 88 (00:49:13Z) -> 274 (01:02:14Z, lagging) -> 285 (01:25:27Z): +197, matching the usage file
tokens | 3,752,295 cache-read, 131,618 cache-write, 84 input, 27,814 output
change | 5 files, +297/-21: scripts/validate_doc_rot.py (sixth sub-detector), tests (11 new), scripts/audit.py (docstring, label), protocols/PLAYBOOK.md (rule text), a disposition-register entry for the one live duplicate it found
commit / push / PR | by rdwornik (gh active account verified), PR #25 `Closes #2`; Copilot made none of them
CI on the PR | RED: 1 failed / 74 passed — test_citation_regex_strips_only_real_dated_artifact_identifiers, which fails identically at the base (1 failed / 63 passed): PRE-EXISTING; the 11 new tests pass
Codex terra review | 1 P1 (the disposition locus hashes only the earliest copy, so drift in a later copy stays suppressed), 2 P2 (dup-allow survives blank lines; a "one-word edit" test edits nothing); VERDICT mergeable-after-P1-fixes; Done-when "partly"
```

- One Copilot run only, as contracted; the P1 was not fixed (a fix would be a second run).

### 2.5 Item 5 — the `#N` trap

- **Live witness (scratch repo, pushed to main):** commit `a4d92116` "… closes [#4]" did **not** close
  issue #4, but put a `referenced` event on it — #4 is legacy row 347, not 4. Commit `fbcffd04` "…
  fixes #5" **closed issue #5** (legacy 393, a different row) at 01:00:12Z; reopened with a comment.
  Issue #1's body text `[#4]` cross-referenced issue #4.
- **Census over the hub** (read-only; commit leg over `origin/main`, file leg over the worktree):

```
measure | value
commits | 8,361
[#N] refs in messages | 10,683 (in 3,367 commits)
bare #N refs in messages | 6,385 (in 2,358 commits)
closing keyword + bare #N | 79 (the research record's figure, reproduced)
closing keyword + [#N] | 590 (no close when pushed — witnessed — but each autolinks)
message refs to N <= 74 (the hub's highest issue/PR number today) | 2,212
refs in tracked files | 64,505 (JOURNAL 8,020; audits 28,928; tasks 4,763; ADRs 1,049; scripts+tests 3,962; other)
distinct cited numbers | 957; live row files 667; highest legacy id 1014
```

- GitHub autolinks `#N` in issues, PRs, comments and commit messages, not in rendered repository files:
  the file refs are a semantic ambiguity for readers, the message refs are live links.
- **The ongoing trap is in new commits:** the `backlog-id-on-close` gate *requires* `[#id]` in a
  closing commit, so every close would autolink — correctly only if issue N is row N.
- **Migration designs:**
  - *sequential* (issues #75-#741) — **726 of 957** cited numbers resolve to a different issue;
  - *aligned* (placeholder issues so issue N = legacy N for N > 74) — 940 creates incl. **280
    placeholders**, **7** live ids <= 74 remapped (a `legacy:N` label + a mapping table), **74** cited
    numbers still mislink; GitHub's documented content-creation limit (~80/min, ~500/h) puts it at
    **>= ~66 min** (sol's correction of my "~2 h"); any PR opened mid-migration shifts every later
    number, so it needs a repository freeze.
  - Rewriting references is safe only in files (64,505 sites); commit messages cannot be rewritten
    without rewriting history.

### 2.6 Item 6 — the snapshot as a projection

- `issues-snapshot.yml`: on every `issues` event (opened, edited, closed, reopened, labeled, …),
  `gh issue list --state all --json …` → `backlog/issues.json` (sorted, labels as names) → commit to
  `main` (concurrency group, pull-rebase retry).
- **Freshness:** the last issue event (01:13:09Z) reached `main` at 01:13:21Z (12 s); across 34 events,
  the next snapshot commit landed 1-12 s later (median 6 s). **230 runs** for this trial's traffic, **202
  cancelled** by the concurrency group, 28 succeeded (median run 13 s).
- **Size:** 99,795 B for 24 issues (~4.2 KB per issue incl. the carrier; the hub's 667 row files total
  1,566,320 B) — one file rewritten per change.
- **Not in it (sol):** dependencies and sub-issues have their own webhook events and are not in the
  exported fields, so the git projection currently carries no links — a restore from git would lose
  them.
- **Prior-art does not read it:** `stage_prior_art.py emit --subject "<a phrase only in the snapshot>"`
  over the scratch tree → `NONE FOUND` (it reads commit messages over `tasks scripts protocols` and the
  content of `docs/audits` and `docs/archive`). It does not read today's `tasks/*.md` content either;
  one `CONTENT_ROOTS` entry would add the snapshot.

### 2.7 Item 7 — the browser

- The scratch repository and the hub are **public** (`gh api` → `private: false`), so three channels
  are readable **with no auth**: the issues page (`github.com/<repo>/issues?q=…`), the REST list
  (`api.github.com/repos/<repo>/issues?state=open&labels=legacy`, 60 unauthenticated requests/h), and
  the raw snapshot (`raw.githubusercontent.com/<repo>/main/backlog/issues.json`).
- Through a summarising fetch tool (this session's WebFetch, a stand-in for the browser seat's):
  the HTML page and the API list each returned **12 of the 14** open legacy issues; the raw JSON listed
  **all 14** (its own count line was wrong). **Ground truth from `gh`: 14.** The reliable channel for
  a seat is the raw snapshot, read as data.

### 2.8 Concurrency (for the merge criterion)

- Two writers editing one issue body from the same read (applied one after the other, as a stale
  second writer does): **both rc 0, the first edit silently lost** — last write wins; `gh issue edit`
  has no If-Match. Two concurrent label adds: **both survived** (labels are set operations). State kept
  in labels merges safely; facts kept in the body do not.

## 3. Item 8 — the re-weighted matrix, O1 vs O2

Weights: ADR-122's twelve with **offline → 0**, plus **no custom code 10** and **Copilot pipeline 6**
(the operator's order); total weight 110, maximum 550. Totals computed by script, never typed.

```
criterion | w | O1 | O2 | O2 in ADR-122 | evidence (O2 unless stated)
agent CLI write | 10 | 3 | 5 | 4 | every write in this trial ran through gh: create 2.2-2.8 s, edit 2.5 s, close, label, dependency, sub-issue, PR, merge; O1's task CLI is unbuilt
git merge behaviour | 12 | 4 | 3 | 2 | no generated shared file in the merge path (ADR-122's 127/600 collision source is gone); labels merge as sets; a stale body edit is silently lost (2.8)
schema validation | 10 | 5 | 1 | 1 | 0 of 5 invalid writes refused server-side; the form binds the web UI only; the raw API creates unknown labels (2.1)
verifier as data | 10 | 4 | 2 | 1 | a verifier-kind field (text); a ruleset makes CI the closing gate (refusal measured) — but CI checks the PR, not the criterion
links | 8 | 5 | 4 | 3 | typed blocked-by with cycle 422 and dangling 404 on the server; the rest are body text
no byte ceiling on truth | 6 | 5 | 5 | 5 | body limit 65,536 chars; largest trial body 10,395
offline | 0 | 5 | 1 | 1 | weight 0 by ruling
migration cost (5 = cheap) | 10 | 3 | 2 | 1 | lossless compat 20/20 with a carrier, readers 13/13; ids lost or a >= 66 min aligned migration with 280 placeholders under a freeze; filename must be carried
one source of truth (snapshot counted) | 10 | 4 | 3 | 2 | the git snapshot trails by ~12 s but lacks links (2.6)
library-first | 6 | 4 | 4 | 4 | gh + GitHub; unchanged
ADR-121 fit | 6 | 4 | 2 | 1 | state outside git; the snapshot is a projection, not an event log
simplicity | 6 | 4 | 4 | 3 | no schema library or CLI; a form, labels, two workflows and a renderer
no custom code | 10 | 2 | 4 | new | O2 still needed 208 lines of Python (migration, renderer, schema change) and 155 of YAML; O1 needs the pydantic model, task CLI, converter and projection library (ADR-122 D1-D9)
Copilot pipeline | 6 | 3 | 4 | new | the CLI took the issue text and `Closes #N` closed it on merge (2.4); the CLI takes any text, so an O1 record feeds it equally
TOTAL /550 | | 418 | 352 |
```

- Under **Codex Astra's cells** (§5): O1 396, O2 346.
- **Sensitivity:** the ranking flips only if "no custom code" weighs **43** (of 143) — four times the
  ruled 10; raising O2's schema 1→5 *and* merge 3→5 together still leaves it 2 points short.

## 4. Item 9 — Codex `gpt-6-sol`, the load-bearing claims

`codex --search exec -m gpt-6-sol -c model_reasoning_effort=high --sandbox read-only`, 17 claims
against the evidence files and GitHub's documentation: **3 VERIFIED, 12 PARTLY, 2 REFUTED.** Most
PARTLY verdicts were "the output was not saved as an evidence file"; the outputs were then saved and
the figures above carry them. The substantive corrections, all applied here:

```
claim | sol | applied
C2 GitHub rewrote bodies to CRLF | PARTLY (one file shown) | RETRACTED by me on re-measurement: the harness did it (2.3)
C9 aligned migration "at least ~2 h" | REFUTED | corrected to >= ~66 min (two 500/h windows)
C11 "two concurrent body edits" | PARTLY — sequential from a stale read | reworded (2.8); the lost update stands
C13/C16 cloud agent "not applicable" | REFUTED — offered on paid individual plans | kept as the contract's fact for this fleet; enabling it is a purchase (OPERATOR-ACTION)
new | snapshot carries no dependency / sub-issue links | added (2.6)
new | a PR-required ruleset blocks the snapshot's direct push | added (2.2)
```

## 5. Item 9 — one Claude-vs-Codex `gpt-6-astra` round, O1 vs O2

Claude's position was written before reading Codex's; Codex received the claims, sol's verdicts, the
matrix and Claude's text (`codex exec -m gpt-6-astra -c model_reasoning_effort=high --sandbox
read-only`).

- **Claude (Opus 5.5): O1 stays the store (418 vs 352).** GitHub lost on paper for partly wrong
  reasons and loses live for measured ones: no server-side schema, a lost update on the body, a live
  wrong-row close by a legacy-style commit, identity that needs a carrier and a frozen, rate-limited
  migration, and a Copilot path that does not need issues.
- **Codex Astra: "FINAL: O1", provisionally.** Deciding facts: the backlog feeds machines (23 modules
  parse row prose) and moving facts into bodies keeps the parsing problem unless another schema layer
  is built; identity migration has demonstrated consequences; O2 has not shown the promised reduction
  in owned machinery — "operated through `gh`" and "no custom code" are different claims.

**Disagreements — recorded, not smoothed:**

```
# | point | Claude | Codex Astra
A1 | schema | O1 5 / O2 1 | O1 4 (unbuilt) / O2 1; "no schema" too categorical — GitHub has native fields and relationships, it lacks the task contract
A2 | lost updates | measured, decisive | a stale-read pattern, not a concurrent test; git can merge separate edits into an invalid combined meaning too
A3 | the carrier | identity needs one | a stored filename + an id map suffices; byte identity does not prove fields agree with the carrier
A4 | simplicity | O1 4 / O2 4 | O1 2 / O2 3 — O1 owns substantial infrastructure
A5 | no custom code | O2 4 | O2 3 — C15/C18 contradict near-native completeness
A6 | Copilot pipeline | O1 3 / O2 4 | 3 / 3 — CLI parity measured, the cloud advantage unmeasured; "not applicable outside the enterprise" is overbroad
A7 | one source of truth | O2 3 | O2 4 — a strictly derived snapshot is not a second authority; its completeness is a separate defect
A8 | ADR-121 fit | O2 2 | O2 3 — issue identity can key verdict events
A9 | what would flip it | a server-side typed-field surface (Projects v2, untried) + an If-Match edit path | engineering + operator minutes per correctly completed task over matched batches
```

Also Codex's strongest point against Claude, which Claude accepts: O1's "schema 5" is a model that
does not exist yet, compared with O2's weaknesses measured on a live service.

## 6. Recommendation

**Keep O1 as ADR-122 decides it; both sides converge; O2's live strengths become requirements on
O1, not a reason to switch.** Adopt from the trial, without moving the store: `Closes #N`-style
closing as the model for the closure sweep (a PR / CI-gated close, measured working); server-side
link integrity (cycle and dangling refusal) as a required check of O1's graph validator; a raw-JSON
projection as the browser seat's channel (answers ADR-122 operator question 1 in shape); and the
Copilot CLI fed from the record's text (measured: 10.7 min, 197 credits for one bounded row). The
tie-breaker ("CC operates it all through `gh`, no new tool") holds for O2 and not for O1, but it
decides ties only, and the gap is not a tie under either side's cells.

**What would reopen it:** Projects v2 typed fields tried live (needs the `project` scope), an
If-Match edit path, and the minutes-per-completed-task measurement Codex names.

## 7. Honest limits

- One row implemented by Copilot, one run; its P1 unfixed. CI red on a pre-existing test, so "CI
  green" was not observable for this change.
- Projects v2 fields untried (scope). The cloud agent unprobed (contract). The ruleset + snapshot-bot
  arrangement not run end to end.
- The lost-update probe is sequential writes from one read (the stale-writer case), not two
  simultaneous requests.
- The browser channel was measured with this session's fetch tool, a proxy for the browser seat's.
- Matrix cells are judgments on measurements; two sides differ on six cells (§5), not on the order.
- Scratch scripts lived in the job's tmp dir (removed with the job); their definitions are stated
  inline wherever a number depends on them. The scratch repository stays until the operator deletes it.
