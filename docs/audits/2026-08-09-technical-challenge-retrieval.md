# Challenge retrieval — the five inventories the browser seat could not witness

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** challenge-retrieval
- **Mode:** READ-ONLY retrieval. **This report rules nothing and proposes nothing.** Every
  classification, retirement, filling and disposition below is the architect's to make.
- **Serves:** `CHALLENGE-ANSWER-2026-08-09.md` (browser seat), whose 🟠 cells at X-2.1 / X-2.2e /
  X-2.4, X-1.1, X-3's §A print, X-4.1 / X-4.3, X-5 and X-6's win-tooling row were deferred here
  rather than filled from recall.
- **Tree:** hub worktree `lane-challenge-retrieval`, pinned at `9e4b294c` for the whole run, so
  every fact below reads one consistent tree while the night-batch consolidation moves `main`.
- **Out of batch, deliberately.** This arc is absent from the night-batch manifest's lane table by
  architect instruction. It merges nothing; its JOURNAL anchor rides the architect's later merge.
- **Method:** six parallel read-only retrieval lanes, each returning facts with locators; every
  headline number and every claim reproduced below was re-verified by the orchestrator against the
  pinned tree before publication. Corrections to lane output are marked **[orchestrator-corrected]**.

## Declared bypass at commit time — `SKIP=audit-health`

This commit was made with **`SKIP=audit-health`**, declared here because an undeclared bypass is the
thing this repo's own doctrine refuses. **`--no-verify` was NOT used** — every other gate
(`validate-hermetization`, `audit-index-freshness`, `claude-rosters-freshness`, `ruff`, the backlog
commit-msg gates, `check-seal-identity`) ran and passed.

The health gate was RED on **exactly one** check, and it is **not this arc's**:

```
[!!] journal_spine_anchor: 6 first-parent spine entry(ies) above the disposition floor
     24882f8cc carry no JOURNAL anchor: 7ce25a88, e8e83ede, 2bcf3dac, a45afbd1, 78f25d8b (+1 more)
     — all "Merge branch 'claude/new-session-*'" night-lane merges
```

Ownership proven, not assumed: `git merge-base --is-ancestor <sha> HEAD` returns false for **every**
flagged commit — none is in this branch's history. They sit on `main`, which the parallel night-batch
consolidation arc advanced past this arc's `9e4b294c` pin while this report was being written. The
count was **4 when the commit was first attempted and 6 minutes later**, which is itself the
evidence that the other arc is mid-flight: its JOURNAL entry — the anchor those merges need — was
staged-but-uncommitted in the primary checkout at the time of writing.

This arc cannot discharge that gap. Writing a JOURNAL entry for another arc's merges is forbidden
both by this contract (no writes beyond this report) and by lane discipline (a lane never journals;
the integrator does). The gap is the consolidation arc's to close, and closing it clears the gate
retroactively for this commit's SHA.

Honest limit: `journal_spine_anchor` scans `main`'s first-parent spine regardless of which branch is
committing, so while that arc is mid-flight it blocks **every** commit anywhere in the repo, not just
this one. That is a property of the gate, reported as observed — not a defect claim and not a
proposal.

## Contract-premise correction (stated first, because it conditions the rest)

`$env:CLAUDE_PROMPTS_DIR\ARC-challenge-retrieval.md` **does not exist**. `CLAUDE_PROMPTS_DIR`
resolves to `C:\Users\1028120\Downloads`; nothing there matches `*challenge-retrieval*`, and the
newest `ARC-*.md` is `ARC-batch3-consolidation-integrate.md` (2026-08-08 20:43). The contract file
was never written to disk. This report executes the contract **as reproduced inline in the dispatch
message**, which is complete (purpose, six numbered outputs, writes, prohibitions, scope note).

This is itself an instance of the class the challenge answer named at X-8.2: the contract existed in
prose and never became a repo artefact — `[#505]` leg 1.

---

# 1 · The command surface, complete

## 1.1 `.claude/commands/` — 8 files

Purpose text is each command's own frontmatter `description:`. Last-touch from
`git log -1 --date=short`.

| File | Command | Purpose (own frontmatter) | Last touch |
|---|---|---|---|
| `changelog-review.md` | `/changelog-review` | "Operator-invoked review of tool changelogs since last review (claude-code + codex) — fetch, classify per the audit-trio rubric, write a digest, bump the state file. PUSH trigger only; never implements adoptions." | 2026-07-29 |
| `handoff.md` | `/handoff` | "Generate or complete a handoff per HANDOFF_PROCESS.md v6 — CC-owned residual + thin browser boot" | 2026-07-30 |
| `handoff-verify.md` | `/handoff-verify` | "Run the whole live probe gate for a handoff bundle in ONE pass and emit exactly ONE evidence block — the v6 one-round-trip boot (HANDOFF_PROCESS §5)" | 2026-08-02 |
| `lane-boot.md` | `/lane-boot` | "Boot ONE batch lane — provision its worktree per the naming enum, seed it, load the frozen contract, and state the V-2 decision budget before any work starts." | 2026-08-07 |
| `lane-integrate.md` | `/lane-integrate` | "Walk a batch's merge queue serially from the primary checkout, then run the five-item refuse-to-finish checklist mechanically — the batch does not close while an item is open." | 2026-08-07 |
| `override.md` | `/override` | "RETIRED (ADR-85 amendment 2026-08-03 §A2) — discharges no gate; arms a local telemetry token only" | 2026-08-06 |
| `preflight.md` | `/preflight` | "Verify every repo locator a contract or prompt cites — file:line, headings, SHAs, [#id] liveness — BEFORE acting on it. Read-only, adoption-first, wired into no gate." | 2026-08-04 |
| `save.md` | `/save` | "Stage all changes and commit with a descriptive Conventional Commits message" | 2026-05-16 |

Creation dates that matter for §1.3 below:

```
.claude/commands/lane-integrate.md   ADDED 2026-08-06  b6c986a1  feat(commands): /lane-boot + /lane-integrate — the two batch-lane commands [#505]
.claude/commands/lane-boot.md        ADDED 2026-08-06  b6c986a1  (same commit)
.claude/commands/preflight.md        ADDED 2026-08-04  4f11a792  feat(preflight): pre-flight becomes a mechanism — locator verification, adoption-first
```

## 1.2 Skills, plugin commands, agents, workflows, hooks

**Repo skills — `.claude/skills/`, 2:**

- `check-against-spec` — "Reconcile a dependent doc against its spec when the spec version
  advances. Runs the deterministic site enumerator, then verdicts EACH extracted site
  (stale|fine|not-relevant; +transclusion-candidate), and writes the by-category checklist into the
  re-stamp commit message. Consumes a {dependent_path, spec_path, old_version, new_version} flag."
- `verify` — "Run the standard check cadence (pytest + ruff + git-status) and report compact
  pass/fail. Invoke after each numbered step. Any FAIL blocks the current step."

**Plugin `tier1-lifecycle` ships 2 commands:**

- `/review-closures` — "Review the session-end closure proposals and execute ONLY operator-approved
  closures (ADR-70 Tier-1)" (last touch 2026-07-29)
- `/ship` — "Merge the current feature branch to main, push, and auto-delete the merged branch
  (git-finish)" (last touch 2026-07-05)

**`.claude/agents/` — EXISTS, 1 definition, and it is tracked:**

- `.claude/agents/artifact-reader.md` (1,722 B) — "Read-only subagent that ingests a named large
  artifact in its own context window and returns a structured summary with pinpoint quotes and line
  numbers. Use when a document exceeds ~20k tokens to avoid loading it in the main session.
  Read-only — never modifies files."
- Tracked (`git ls-files` returns it); last touched by `c6088922`
  *"feat(a1): refresh Sonnet pins claude-sonnet-4-6 -> claude-sonnet-5 (artifact-reader +
  conformance-hub V1/V2/V3)"*. Its Aug-9 filesystem mtime is the worktree checkout time, not an
  authoring time — checked because a today-dated untracked agent would have meant something quite
  different.

**`.claude/workflows/` — 1 file, not previously enumerated anywhere:**

- `.claude/workflows/conformance-hub.js` — tracked. Surfaced as the `conformance-hub` skill:
  "Read-only documentation-conformance review of the .dev-knowledge repo: 3 verifiers … fan out, an
  adversarial skeptic kills false positives, a digest synthesizes."
- **Bearing on X-2.4** ("does a subagent-spawning workflow command exist?"): a subagent-spawning
  *workflow* exists and is committed. Whether it satisfies what X-2.4 meant by "command" is the
  architect's call — reported as a located fact, not an answer.

**`.claude/settings.json` hooks — 7 entries:**

| Trigger | Command | Matcher |
|---|---|---|
| SessionStart | `uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py"` | — |
| SessionStart | `powershell -ExecutionPolicy Bypass -File "$CLAUDE_PROJECT_DIR/scripts/surface_triage.ps1"` | — |
| SessionStart | `powershell -NoProfile -ExecutionPolicy Bypass -File "$CLAUDE_PROJECT_DIR/scripts/billing_leak_sentinel.ps1"` | — |
| SessionStart | `uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/changelog_sentinel.py"` | — |
| SessionStart | `uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/arm_hooks.py"` | — |
| PreToolUse | `python "$CLAUDE_PROJECT_DIR/scripts/hooks/block_immutable_edits.py"` | `Edit\|MultiEdit\|Write\|NotebookEdit` |
| Stop | `uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"` | — |

## 1.3 Batch 1 and batch 2 — command occurrences

Artifacts identified, with the line that proves batch membership:

- **Batch 1:** `docs/audits/2026-08-06-technical-batch-1-integration-packet.md` (:1 "Batch-1 —
  end-of-batch integration packet"); `docs/audits/2026-08-06-technical-batch1-verification.md`
  (:3 "Under review: the batch-1 range").
- **Batch 2:** `docs/audits/2026-08-07-technical-batch-2-packet.md` (:1 "Batch 2 — end-of-batch
  packet"); `docs/audits/2026-08-07-technical-batch-2-manifest.md` (:2 "batch: 2");
  `docs/audits/2026-08-07-technical-batch-2-lessons.md`; and in `~/Downloads`,
  `INTEGRATOR-batch-2.md` (:8 "CLOSE batch 2") plus `ARC-CONSOLIDATE-v2-batch2-lessons.md`
  (and its `(1)` duplicate).

**Batch 1:**

| Command | Count | Sites |
|---|---|---|
| `/lane-integrate` | 2 | batch-1-integration-packet.md:166 · batch1-verification.md:184 |
| `/preflight` | 1 | batch1-verification.md:426 |
| all others | 0 | — |

The single `/preflight` occurrence is not a use — batch1-verification.md:426 reads
"`/preflight` — the organ built for exactly that — sat unused".

**Batch 2:**

| Command | Count | Sites |
|---|---|---|
| `/lane-integrate` | 4 | batch-2-lessons.md:126 · batch-2-packet.md:284, :332, :424 |
| `/lane-boot` | 2 | batch-2-packet.md:64, :435 |
| `/review-closures` | 1 | `~/Downloads/INTEGRATOR-batch-2.md`:10 |
| `/handoff` | 1 | batch-2-packet.md:372 |
| `/preflight` | 1 | batch-2-packet.md:402 |
| all others | 0 | — |

**Caveat, stated rather than hidden:** these counts are of *mentions in retrospective artifacts*,
which is not the same as *invocations*. Batch 1 and batch 2 packets are written after the fact and
several occurrences are the packet naming a command to say it was **not** used. Distinguishing
mention from invocation for batches 1–2 would require the session transcripts, which were not in
scope for this arc — `unknown` by scope, not by search failure.

## 1.4 A hand-written instruction that replaced a command that existed — one, named

**`~/Downloads/INTEGRATOR-batch-2.md:10`** spells the integration procedure out as prose:

> (1) **Discover the queue from reality, not from contract literals:** enumerate unmerged
> `worktree-*` and `docs/*` branches in the shared ref store, match each to its lane STOP packet …
> (2) Merge serially `--no-ff` in dependency order under the R-1 mechanism … (3) Apply any carried
> paste-block artifacts the packets name. (4) **Closure loop, not lane self-closes:** run
> `/review-closures` (ADR-70) … (5) Full suite ONCE on the merged result … (6)
> **Refuse-to-finish, all five:** every branch merged-or-explicitly-abandoned · suite once ·
> `git worktree list` == primary only (tear down ALL live lane worktrees) · `git stash list` empty ·
> **batch packet archived**

That is `/lane-integrate`'s job, restated. The command's own description is "Walk a batch's merge
queue serially from the primary checkout, then run the five-item refuse-to-finish checklist
mechanically" — including the same five-item checklist reached in step (6).

**The dates hold, and were re-verified because the whole finding rests on them
[orchestrator-corrected]:** `/lane-integrate` was **ADDED 2026-08-06** in `b6c986a1`; the prompt
file is dated **2026-08-07 15:43**. The command preceded the prompt by one day. (A lane report gave
the command's *last-touch* as 2026-08-07, which would have made the ordering ambiguous; the
`--diff-filter=A` add-date resolves it.)

The sharpest detail: step (4) invokes `/review-closures` **by name**, so the author was composing
in a register where slash commands were available — and hand-wrote the other five steps anyway.
This is the batch-2 instance of the batch-3 pattern already established (v1 of the batch-3
integration contract re-derived `/lane-integrate` from chat).

For batch 1 no such instance was found. Scanned: `2026-08-06-technical-batch-1-integration-packet.md`,
`2026-08-06-technical-batch1-verification.md`, and every `~/Downloads/LANE-*.md`. Note that
`/lane-boot` and `/lane-integrate` did not exist until 2026-08-06, so for most of batch 1 there was
no command to bypass.

---

# 2 · `[#408]` and the distiller family

## 2.1 `[#408]` — full row, verbatim (`BACKLOG.md:85`)

> - [#408] [P2][M] **Auto-coupled doc updates — closing a backlog item must mechanically PULL its
> ARCHITECTURE + JOURNAL updates** — closing a task should trigger (wired, not remembered) the
> coupled ARCHITECTURE update and JOURNAL entry. Evidence it is needed: ARCHITECTURE drift was
> found TWICE this arc, once the day AFTER a genuine re-read — memory alone does not hold it.
> [#403] is the mechanism seed (doc_claims extended to machine-derivable claims). Filing only, zero
> build. **Design draft:
> `docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md`** — the coupling-manifest
> shape, worked through ahead of build. It **pre-chews the per-section granularity values, which are
> an OPERATOR DECISION deliberately not settled there**; that choice is the first gate on any build,
> not something to infer from the draft. · Done when: closing a backlog item mechanically surfaces
> or blocks on the coupled ARCHITECTURE + JOURNAL updates (built on the [#403] seed), with a test,
> or recorded deferred-with-reason · refs #403, scripts/audit.py, ARCHITECTURE.md, JOURNAL.md ·
> kill-candidates: #403 (if its doc_claims extension already discharges the coupling, fold in) ·
> serialize-group: audit-py

- **Status:** `status: open` — `tasks/408-auto-coupled-doc-updates-closing-a-backlog-item.md:4`
- **Other sites:** `JOURNAL.md:1791` (2026-08-06, "`[#408]` row-pointer")
- **Bearing on X-1.2b, reported not ruled:** `[#408]`'s subject is *doc-coupling on closure* —
  ARCHITECTURE + JOURNAL pulled mechanically when a task closes. Whether that overlaps intake #29's
  distillation engine is the architect's determination; the standing ruling already recorded in the
  challenge answer governs the outcome if it does.

## 2.2 The distiller family, by surface

**`docs/intake/` — 2**

| id | status | quoted line |
|---|---|---|
| #23 `2026-08-01-func-distillation-and-library-first.md` | `status: SEED` (:3) | "# Operator design input — distillation and library-first" (:8) |
| #29 `2026-08-08-func-multi-model-execution-and-distillation.md` | `status: DRAFT` (:3) | "# Multi-model execution flow, session-cost instrumentation, and the distillation engine (measure-first)" (:8) |

**`docs/decisions/` — 6 ADRs. All six are Accepted [orchestrator-corrected]** — a lane returned
four as `unknown`; they carry `Status:` / `- **Status:**` at line 5, not the `**Status:**` form it
grepped.

| ADR | status | quoted line |
|---|---|---|
| ADR-108 | Accepted (ratified 2026-07-31) | ":36 — 3. **AI Council is the distillation organ for genuinely contested technical decisions**"; also ":60 — **§D** context-distiller pre-phase (repomix `--compress`, pyadr, copier/cruft)" |
| ADR-39 | Accepted | ":194 — \| Boundaries \| Reference role — distillation of PLAYBOOK + LESSONS." |
| ADR-62 | Accepted (post-implementation ratification) | ":191 — + ADR distillation) is high — so relax was correct here." |
| ADR-78 | Accepted — 2026-06-07 | ":9 — operator ratification = distillation prompt 2026-06-07." |
| ADR-79 | Accepted — 2026-06-07 | ":9 — operator ratification = distillation prompt 2026-06-07." |
| ADR-92 | Accepted (ratified by merge 2026-06-29) | ":7 — Records the architect's distilled design across two AI-Council debates" |

Note for the architect's triage: ADR-39/62/78/79/92 use "distillation" to describe *how a decision
was reached* (a council/ratification idiom), not a prompt-distillation mechanism. ADR-108 is the one
that names a distiller as a thing to build (§D). Reported as an observation about word sense; the
relevance call is not mine.

**`BACKLOG.md` — 2**

| id | status | quoted line |
|---|---|---|
| `[#449]` | open | ":32 — **Assembled-paste byte budget — should `PASTE_THIS.md` gain a hard ceiling?** … P1 repomix distiller pilot ([#449] paste budget + review-lane packing;" |
| `[#467]` | `status: closed` (`tasks/467-*.md:4`) | "**[#449] paste budget — repomix REJECTED on measurement; the ceiling question stays open**" |

**`tasks/`** — the two task files above (`408-…`, `467-…`); no additional distiller-family task
files beyond those backing the rows already listed.

**`LESSONS.md` — 0.** Searched `distill|distiller|distillation|prompt.improv|prompt.optimi|prompt.router|prompt-router`;
no matches.

## 2.3 PLAYBOOK "dynamic-workflow shape" as §16 — **the pointer is stale; the content exists elsewhere**

**§16 of `protocols/PLAYBOOK.md` today is `## 16. Cross-Tool Review` (`protocols/PLAYBOOK.md:4085`):**

> ## 16. Cross-Tool Review
> `<!-- scope: dev -->`
>
> **When:** Feature branch touches 3+ files OR 2+ packages OR safety-critical paths (vault writes,
> OneDrive ops, cleanup/delete)
> **Skip when:** Single-file fix, test-only changes. (Documentation/prose diffs are *not* skipped
> wholesale — they route to the `/codex-review` doc-lane; see "Code-vs-doc routing" below and [#333].)

Neighbouring sections, so the numbering is unambiguous: `## 14. Markdown Governance` (:3996),
`## 15. Anti-Patterns — What NOT to Do` (:4050), `## 16. Cross-Tool Review` (:4085),
`## 17. Code Quality Audit Process` (:4131).

**The dynamic-workflow content does exist — as a `###` subsection of §2, at
`protocols/PLAYBOOK.md:2949`:**

> ### When to escalate to a Dynamic Workflow
> `<!-- scope: llm -->`
>
> The Sonnet/Opus model ladder has a third rung — *the orchestration tier*. Escalate execution to a
> **scoped Dynamic Workflow** (the Claude Code `Workflow` tool: Claude writes a JS harness —
> `agent()` / `parallel()` / `pipeline()` — that a runtime drives in the background, coordinating
> many subagents while the session stays responsive) when **any** of these hold:

Related live sites: `:137` (TOC entry), `:2189` (the organ-glossary row naming the `ultracode`
trigger), `:2211` (routing table row), `:3004` ("`ultracode` is the Dynamic-Workflow trigger
keyword, NOT an effort tier").

**Answer to the question as asked:** a section by that name **is absent at §16** — no heading in
PLAYBOOK is titled "dynamic-workflow shape" (`grep "workflow shape"` → no matches; `git log -S
"workflow shape" -- protocols/PLAYBOOK.md` → no commits, so the exact phrase was never a heading).
The substance the 2026-07-16 prompt was pointing at is present, at §2's subsection, and the section
number in that prompt does not resolve. Added by `11ef2d8e` *"docs(playbook): add
workflow-escalation rule (closes [#74])"*.

---

# 3 · Intake #27 §A, every row

**File:** `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` · **status:** `DRAFT` (:3)

**Row count: 38.** Ids present, verified mechanically against the pinned tree:
`1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
36 37 40` — i.e. 1–37 contiguous, then **40**; 38 and 39 are a documented deliberate gap (item 38
was folded into row 35, item 39 into the Sequencing note).

**This corrects the challenge answer's "36 rows"** — that was the width before 2026-08-08; §A is now
38.

## 3.1 All 38 rows, current state

| # | Item | Status | Evidence / locator | Class |
|---|---|---|---|---|
| 1 | Gemini CLI lane [#491] | SCHEDULED(batch-2 grooming) | supplement C3(a) | P-A |
| 2 | Grok lane [#492] | SCHEDULED(peg ≥2026-08-07; seeded-defect list unwritten) | supplement C3(b) | P-A |
| 3 | Copilot Free as Grok channel | DEFERRED(opens with #2) | intake #24 P6 | P-A |
| 4 | sol/terra/luna routing table | ADOPTED-live | R-6 ruling; terra owed on [#504] | — |
| 5 | Actions report-only recorder [#501] | SCHEDULED(batch 1) | row e7c0b70e; YAML in night packs c55c7e51 | P-A |
| 6 | Scheduled runs + dead-man ([#493], P2 folded) | DEFERRED(no date) — B-2 still silent | FR-3 fold ruling | P-C |
| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | night finding 5 (rate limits, ~150→403) | P-C |
| 8 | mutmut [#502] | EVAL-RUN(pass) + SCHEDULED(behind [#501], CI-only) | night research; B2→B1 dependency edge | P-A |
| 9 | CONTRIBUTING currency [#503] | SCHEDULED(batch 1, ×6 claims + DoD + override.md) | Lane D + night finding 7 | P-A |
| 10 | vale (P6) | REFUTED | commit 5125dd6 + JOURNAL (b) 616f4814 | — |
| 11 | commitlint / gitlint (P6) | EVAL-RUN(LEAVE) | night packs 81cf13b | — |
| 12 | lychee (P6) | EVAL-RUN(ADOPT-candidate, --include-fragments) | night packs 81cf13b | P-B |
| 13 | copier living-template (W-1) | DEFERRED(W-wave batch — after intake #25 acceptance + births) | R-i pre-naming | P-A |
| 14 | kernel/lab check tiering (W-2) | DEFERRED(W-wave batch — …; pyproject collision recorded) | Lane C ledger | P-A |
| 15 | pre-commit native distribution (W-3) | DEFERRED(W-wave batch — …; reconcile [#497] @ carrier_mesh.py:75 FIRST) | mega-packet collision | P-A |
| 16 | reusable kernel.yml (W-4) | DEFERRED(W-wave batch — …; .github/workflows/ single-owner = [#501]) | Lane C ledger | P-A |
| 17 | pytest-testmon (W-5) | SCHEDULED(batch-2 ledger per rider R-ii; targets 410s/run) | supplement rider R-ii | P-A |
| 18 | schema-as-code (W-6) | DEFERRED(floats behind W-5) — reshaped by §A item 35 | rider R-ii | P-B |
| 19 | sphinx-needs study (W-7) | UNPLACED | intake #25 heading only | P-D |
| 20 | local-vs-reference matrix (W-8) | UNPLACED(intake prose) — candidate for a one-line register ruling | intake #25 W-8 | P-B |
| 21 | AGENTS.md + thin shim (W-9a) | DEFERRED(W-wave batch — …) **+ HAZARD: collides with existing codex/AGENTS.md** | mega-packet hazard | P-A |
| 22 | VISION→README (W-9b) | UNPLACED (S, gap-week) | — | P-B |
| 23 | .claude/skills ↔ .agents/skills symlink (W-9d) | UNPLACED (S, gap-week) | — | P-B |
| 24 | routing-table-as-config (W-10) | DEFERRED(W-wave batch — after intake #25 acceptance + births) | intake #25 | P-A |
| 25 | standing-rulings register (V-2) | ADOPTED-live (4 lessons + B2 label land in successor Phase 2) | protocols/STANDING_RULINGS.md, 90351bd0 | — |
| 26 | risk-tiered ceremony + plan-mode-by-exception (V-3) | ADOPTED-live | templates/prompt-template.md v1.6, 12dbb65a; precedence repair adf85c4a | — |
| 27 | first V-1 worktree batch | GO-GIVEN, runs as successor Phase 4 | predecessor approve + plan §2 | P-A |
| 28 | worktree hygiene prune (V-5) | SCHEDULED(mechanized in [#429] slim, successor Phase 3) | plan §2 P3 | P-A |
| 29 | seal velocity metrics (V-6) | PARTIAL(qualitative only; hard numbers = batch-1 packet) | retro RS-3 | P-A |
| 30 | [#408] three-layer sync spec | DESIGN-LANDED(c55c7e51, fingerprint trigger); build = OWN ARC, unplaced | row pointer per rider R-iii | P-C |
| 31 | Fibonacci estimate binding | UNPLACED ([#488] scope; backlog still has no ranking function) | audit row 31 | P-D |
| 32 | R1–R4 retirement ranking | DORMANT since [#487] engine refutation | 2026-08-06 grooming used live-peg evidence | P-D |
| 33 | **pytest-xdist** (`-n auto`) | NEW EVAL candidate — immediate 410s relief, orthogonal to W-5 | operator pain (410s); suite 2362 tests | P-B |
| 34 | **jsonc-parser (Microsoft)** as merge engine | NEW EVAL candidate + **MAINTENANCE FLAG 2026-08-08** (see 3.3) | audit 2026-08-08-technical-library-research §8a | P-B |
| 35 | **check-jsonschema** (pre-commit hook) | NEW EVAL candidate + **AMENDED 2026-08-08** (see 3.3) | …§8b | P-B |
| 36 | **mise** (per-repo toolchain pinning) | NEW EVAL candidate + **EVIDENCE ADDED 2026-08-08** (see 3.3) | …§8c; JOURNAL 2026-08-07 (o); STANDING_RULINGS D1 | P-B |
| 37 | **`Closes:` git trailer as the closure convention** | NEW EVAL candidate — git-native, zero deps; **the migration is the whole cost**: over `origin/main`'s 52 first-parent commits `CLOSES_RE` fires on 8 (7 ids) while `Closes:`/`Fixes:` appear on ZERO, so a pure trailer matcher would lose 100% of live signal | `git interpret-trailers --parse` over `25ff8ec37` returns zero `Closes:`; precision 7/8 — …§1 | P-B |
| 40 | **`sys.path` substrate — adopt pytest `pythonpath` (shape B)** | NEW EVAL candidate, **or fold into `[#502]`** — 100 `sys.path.insert` across 92 files, no `conftest.py`, class grew ~6× since last measurement, no ruling. Shape B is one config block; shape A permitted-not-mandated (STANDING_RULINGS F5); shape C reverses `package = false` and needs an ADR. Three shapes costed, **no pick made** | …§5 | P-B, escalating to ADR only if shape C |

## 3.2 Δ against 2026-08-07

**There is no commit dated 2026-08-07 [orchestrator-corrected].** The file's full history:

```
5f51dc0a 2026-08-08 docs: three batch-3 GO rulings land in STANDING_RULINGS (G1-G3)
7d7253c1 2026-08-08 docs: process-lane cap denominator is dispatched width — ratified 2026-08-08
08c3e0b6 2026-08-08 docs(intake): ledger truth — six spent pegs re-pegged, memo §9 applied, items 34/36 annotated
82698be5 2026-08-06 docs(intake): repair intake #27's two dangling §D references (erratum recorded)
bca18dba 2026-08-06 docs(intake): file the tech-adoption consolidation ledger as intake #27
```

Baseline used: **`82698be5` (2026-08-06)** — the last commit on or before 2026-08-07. So the
requested "Δ vs 2026-08-07" is in fact **08-06 → 08-09 (HEAD)**.

**All §A row changes landed in `08c3e0b6` alone.** Verified: `git diff 08c3e0b6 HEAD -- <file>`
returns **no** line matching `^[+-]\| [0-9]+ \|` — the two later 08-08 commits add 13 and 6 lines
respectively, elsewhere in the file, touching no numbered §A row.

**Six rows re-pegged** — the spent-peg repair. All six read `DEFERRED(batch 2 …)`, but batch 2 had
run and closed with zero W-items, so the status was a locator pointing at a finished event. Each
row's own collision/hazard qualifier was preserved verbatim:

| Row | Old | New |
|---|---|---|
| 13 | `DEFERRED(batch 2 W-wave)` | `DEFERRED(W-wave batch — after intake #25 acceptance + births)` |
| 14 | `DEFERRED(batch 2; pyproject collision recorded)` | `DEFERRED(W-wave batch — …; pyproject collision recorded)` |
| 15 | `DEFERRED(batch 2; reconcile [#497] @ carrier_mesh.py:75 FIRST)` | `DEFERRED(W-wave batch — …; reconcile [#497] @ carrier_mesh.py:75 FIRST)` |
| 16 | `DEFERRED(batch 2; .github/workflows/ single-owner = [#501])` | `DEFERRED(W-wave batch — …; .github/workflows/ single-owner = [#501])` |
| 21 | `DEFERRED(batch 2) + HAZARD:…` | `DEFERRED(W-wave batch — …) + HAZARD:…` |
| 24 | `DEFERRED(batch 2)` | `DEFERRED(W-wave batch — after intake #25 acceptance + births)` |

**Three rows amended:** 34 (maintenance flag + npm-runtime cost), 35 (concrete first target; scope
3→2 surfaces), 36 (third silenced organ + the divergence question).

**Two rows added:** 37 (`Closes:` trailer) and 40 (`sys.path` substrate).

**Zero rows removed.** §A width **36 → 38**.

## 3.3 The eight named ledger lines, verbatim, with scheduling called out

All eight are in §A. None lives in another section.

**1 · `gh` — item 7, line 26**

> `| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | night finding 5 (rate limits, ~150→403) | P-C |`

Scheduling: **UNPLACED**, class P-C (own arcs). **No gap-week assignment recorded.** (Bears on
X-3's "`gh` formalized in the ledger?" — the ledger line exists but is UNPLACED, not a formalization.)

**2 · `check-jsonschema` — item 35, line 54**

> `| 35 | **check-jsonschema** (pre-commit hook) | NEW EVAL candidate — reshapes W-6 from build to adopt — **AMENDED 2026-08-08 (memo §9 item 38):** the eval now has a **concrete first target that needs no build** — `.github/workflows/report-only-wall.yml`, born this window with `[#501]` — which `check-github-workflows` covers out of the box with no schema to author. Scope is **2 uncovered surfaces, not 3**: the six `deploy/manifest-v*.yaml` files and that workflow; `ecosystem/schema/` is pydantic (ADR-109) and validates itself, so the hook adds nothing there | W-6 stalled as a build; 0.37.4 released 2026-06-29, healthy by every signal checked — `docs/audits/2026-08-08-technical-library-research.md` §8b | P-B |`

Scheduling: class **P-B — gap-week S-evals**.

**3 · `mise` — item 36, line 55**

> `| 36 | **mise** (per-repo toolchain pinning) | NEW EVAL candidate — durable fix for the uv-pin class — **EVIDENCE ADDED 2026-08-08: the class recurred, and the count is THREE organs, not two.** In the night-cloud container `pyproject.toml` pins `required-version = "==0.11.19"` while the container shipped uv `0.8.17`, and `uv self update 0.11.19` returns *"version 0.11.19 was not found for the app uv"* — so every hook whose entry is `uv run --locked …` was unrunnable. Two were pre-commit hooks routed around by invoking their scripts directly; the third was the **`Stop` session-end backpressure hook, which fired unbidden at the boundary and failed open** — an unrunnable Stop hook is indistinguishable from a passing one to anyone reading the session. Divergence question, verbatim from the memo: *"would a `mise.toml` pinning uv `0.11.19` have produced a runnable gate mesh in a fresh cloud container tonight — i.e. can mise fetch a uv release that `uv self update` cannot?"* The honest counter the row should carry: **`mise` would not have fixed tonight** — the missing thing was a *specific uv version*, and a tool that manages uv still has to be able to fetch it | 3 organs silent from one cause; night fix ephemeral by design. Recurrence: `docs/audits/2026-08-08-technical-library-research.md` §8c; JOURNAL 2026-08-07 (o); STANDING_RULINGS D1 | P-B |`

Scheduling: class **P-B — gap-week S-evals**. (Note for the architect: the challenge answer calls
mise a *precondition*, not a gap-week candidate; the ledger still carries it as P-B gap-week. The
divergence is reported, not resolved.)

**4 · `jsonc-parser` — item 34, line 53**

> `| 34 | **jsonc-parser (Microsoft)** as merge engine | NEW EVAL candidate — replaces hand-rolled JsoncMerge.ps1 (196 lines) — **MAINTENANCE FLAG 2026-08-08: cold, not abandoned.** Latest release v3.3.1, 24 June 2024; no 2025 or 2026 releases. A stable parser for a frozen format can legitimately sit still, but the row's premise is *replacing a bug source*, and swapping a maintained-by-us one for a two-years-quiet dependency is a trade, not a win. Second friction, fleet-shaped rather than package-shaped: it is an **npm** package, so adopting it means a Node runtime in the win-tooling lane | 2 latent bugs bit in one week (win-tooling lane); maintenance flag + npm-runtime cost measured in `docs/audits/2026-08-08-technical-library-research.md` §8a | P-B |`

Scheduling: class **P-B — gap-week S-evals**.

**5 · `pytest-xdist` — item 33, line 52**

> `| 33 | **pytest-xdist** (`-n auto`) | NEW EVAL candidate — immediate 410s relief, orthogonal to W-5 | operator pain (410s); suite 2362 tests | P-B |`

Scheduling: class **P-B — gap-week S-evals**. The row is **stale relative to reality**: it still
reads "NEW EVAL candidate" targeting "410s", while xdist is adopted and holding (challenge answer
X-3 records 1785.6s → 539s on merged main). Reported as an observed divergence; the ledger update is
the architect's.

**6 · `mutmut` — item 8, line 27**

> `| 8 | mutmut [#502] | EVAL-RUN(pass) + SCHEDULED(behind [#501], CI-only) | night research; B2→B1 dependency edge | P-A |`

Scheduling: **SCHEDULED behind `[#501]`, CI-only**, class P-A (batch-2 unlock). **No gap-week
assignment.**

**7 · Gemini — item 1, line 20**

> `| 1 | Gemini CLI lane [#491] | SCHEDULED(batch-2 grooming) | supplement C3(a) | P-A |`

Scheduling: **SCHEDULED(batch-2 grooming)**, class P-A. **No gap-week assignment.**

**8 · Grok — item 2, line 21**

> `| 2 | Grok lane [#492] | SCHEDULED(peg ≥2026-08-07; seeded-defect list unwritten) | supplement C3(b) | P-A |`

Scheduling: **SCHEDULED, peg ≥2026-08-07 — a peg now in the past** — and the row itself records the
blocker ("seeded-defect list unwritten"), class P-A. **No gap-week assignment.**

---

# 4 · Provider-instruction files, fleet-wide

## 4.1 The inventory

Every file found that instructs an agent. Searched each repo for `CLAUDE.md` (root + nested),
`AGENTS.md`, `codex/AGENTS.md`, `.claude/rules/*`, `.claude/CLAUDE-FLOOR.md`, `.cursorrules`,
`.github/copilot-instructions.md`, `GEMINI.md`.

| Repo | Path | Bytes | Claims authority over (its own words) |
|---|---|---|---|
| hub | `CLAUDE.md` | 32,479 | "Session contract for Claude Code in this repo. Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53." (:12) |
| hub | `codex/AGENTS.md` | 3,891 | "Canonical source for `~/.codex/AGENTS.md`. Owned by `.dev-knowledge`. Deploy by copying to `~/.codex/AGENTS.md`. This file is read automatically by Codex CLI (OpenAI). Codex is a read-only code reviewer across all repos." (:1–7) |
| hub | `.claude/rules/git-discipline.md` | 2,214 | "This is a git-tracked knowledge base. Every edit must be committed." (:6) |
| ai-council | `CLAUDE.md` | 33,831 | same session-contract formula (:10) |
| ai-council | `.claude/CLAUDE-FLOOR.md` | 3,136 | "Auto-loaded methodology baseline for any Claude Code / Codex session in this repo. Generated from the methodology hub; do not hand-edit (a `.sha256` sidecar guards it)." (:1–3) |
| ai-council | `.claude/rules/code-standards.md` | 523 | no self-authority statement |
| ai-council | `.claude/rules/python-env.md` | 373 | no self-authority statement |
| ai-council | `.claude/rules/testing.md` | 199 | no self-authority statement |
| corp-monorepo | `CLAUDE.md` | 23,025 | same session-contract formula (:13) |
| corp-monorepo | `.claude/CLAUDE-FLOOR.md` | 3,136 | same floor formula |
| corp-ops | `CLAUDE.md` | 6,983 | same session-contract formula (:8) |
| corp-ops | `.claude/rules/code-standards.md` | 657 | no self-authority statement |
| corp-ops | `.claude/rules/python-env.md` | 396 | no self-authority statement |
| corp-ops | `.claude/rules/testing.md` | 185 | no self-authority statement |
| corp-sca-time-automation | `CLAUDE.md` | 7,125 | same session-contract formula (:8) |
| corp-sca-time-automation | `.claude/CLAUDE-FLOOR.md` | 3,177 | same floor formula |
| life-architect | `CLAUDE.md` | 6,269 | same session-contract formula (:11) |
| win-tooling | `CLAUDE.md` | 7,018 | same session-contract formula (:8) |
| demo-prep | `CLAUDE.md` | 6,990 | same session-contract formula (:9) |
| demo-prep | `.claude/worktrees/section-library/CLAUDE.md` | 6,988 | a live worktree's copy |
| terminal-setup | — | — | **no instruction file of any kind found** |

**Facts worth the architect's eye, stated as facts:**

- **`AGENTS.md` exists at exactly one place in the fleet: the hub's `codex/AGENTS.md`.** No repo
  carries a root `AGENTS.md`. This is the collision W-9a records.
- **The hub's own `CLAUDE.md` is 242 lines** against its self-description "(≤200 lines)" at
  `CLAUDE.md:12` — the file's claim about itself does not match the file.
- **`CLAUDE-FLOOR.md` is present in 3 of 8 satellites** (ai-council, corp-monorepo,
  corp-sca-time-automation) and absent from corp-ops, life-architect, win-tooling, demo-prep,
  terminal-setup. ai-council and corp-sca differ in size (3,136 vs 3,177 B), so they are not the
  same revision.
- `demo-prep` carries a live worktree at `.claude/worktrees/section-library/` with its own
  `CLAUDE.md`.

## 4.2 The same rule, stated in different words

**Branch/merge discipline** — hub `CLAUDE.md:59-61`:

> "**Commits & branches:** Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches —
> these four only)… **Never commit directly to `main`: branch → `--no-ff` merge.**"

vs hub `.claude/rules/git-discipline.md:14`:

> "**MERGE IS ATOMIC:** merge `--no-ff` + push + delete the source branch are ONE operation."

Same rule, two files, different words — and the second adds the deletion leg the first omits.
`ai-council/CLAUDE.md:54` and `corp-monorepo/CLAUDE.md:62` restate the first in a *third* wording
("Branch prefixes are `feat/ fix/ docs/ chore/` (these four only)") that drops the "author-chosen"
qualifier the hub added when the four machine lane prefixes were admitted.

**OneDrive exclusion** — `ai-council/.claude/rules/code-standards.md:14`:

> "NEVER touch "OneDrive - Blue Yonder" paths"

vs `corp-ops/.claude/rules/code-standards.md:13`:

> "No DELETE or WRITE into "OneDrive - Blue Yonder" paths; non-destructive reads-from allowed only
> when enumerated"

These two **are not the same rule**: "never touch" forbids reads; the corp-ops wording permits
enumerated reads. The global `~/.claude/rules/core-invariants.md` §1 carries the three-tier
T0/T1/T2 version, which matches corp-ops's sense and not ai-council's.

**Append-only records** — hub `CLAUDE.md:85` vs `ai-council/CLAUDE.md:73` vs
`corp-monorepo/CLAUDE.md:78`. All three say LESSONS + TOKEN-LOG are append-only; ai-council points
at `.dev-knowledge/logs/TOKEN-LOG.md` (cross-repo path) where corp-monorepo points at
`logs/TOKEN-LOG.md` (repo-local). Only the hub's carries the ADR-29 2026-07-17 archival exception.

**Test-after-each-step** — global `core-invariants.md` §2 ("Run `pytest -x --tb=short && ruff check
&& git status` between every numbered step in a plan. Not at the end.") vs
`ai-council/.claude/CLAUDE-FLOOR.md:15` and `corp-monorepo/.claude/CLAUDE-FLOOR.md:15` ("Run the
repo's checks **after each numbered step, not at the end** — default trio: `pytest -x --tb=short &&
ruff check && git status`"). Same rule, two homes.

**Destructive-action confirmation** — `core-invariants.md` §3 ("Always ask before removing files,
functions, significant code blocks, or git branches") vs `CLAUDE-FLOOR.md:32` ("Never delete files,
functions, code blocks, or branches without asking"). Same rule, two wordings.

**Minimal diffs / shell choice:** stated in the global `~/.claude/CLAUDE.md` P0 block only; no
satellite restatement found. No pair to report.

## 4.3 `validate_reconciliation._SPEC_REGISTRY`, verbatim

`scripts/validate_reconciliation.py:79`:

```python
# The live spec registry. Add a row when a new spec becomes a reconciliation authority.
_SPEC_REGISTRY: dict[str, SpecSource] = {
    "handoff-process": SpecSource(
        "handoff-process",
        "protocols/HANDOFF_PROCESS.md",
    ),
}
```

**Entry count: 1.** `handoff-process` → `protocols/HANDOFF_PROCESS.md`.

Neither `AGENTS.md` nor `templates/prompt-template.md` is registered. (X-4.2's ruling depends on
this registry; it currently has one row.)

## 4.4 Intake #25, W-9a, and the HAZARD text

**Intake #25:** `docs/intake/2026-08-05-func-simplification-distribution-wave.md` ·
**live status: `DRAFT`** (:3).

**W-9a entry in #25, in full** (`:35–36`):

> **W-9 — industry-standard naming: re-universalize the HUB itself (operator-directed; rides W-1 —
> rename ONCE in the template, copier propagates).**
> Verdict table, honest not compliant: **(a) CLAUDE.md → AGENTS.md** with a thin CLAUDE.md shim
> containing `@AGENTS.md` + Claude-only overrides — AGENTS.md is Linux-Foundation-stewarded, 60k+
> repos, read natively by Codex/Cursor/Copilot/Gemini CLI; the import pattern keeps Claude Code
> fully functional (it does not read AGENTS.md natively — the shim is the documented interop).

**The HAZARD text is NOT in intake #25 — this refutes a premise of the challenge answer.**

The challenge answer (X-4.3) states "The hazard text is recorded in intake #25". It is not.
Searches run against the pinned tree:

```
grep -n -i "W-9\|hazard" docs/intake/2026-08-05-func-simplification-distribution-wave.md
  -> lines 35, 39, 63 — all W-9 prose; ZERO occurrences of "HAZARD"
grep -rn "HAZARD" docs/intake/
  -> exactly ONE hit, in a different file
```

The sole recorded HAZARD for W-9a lives in **intake #27, §A row 21**
(`docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:40`), and its full verbatim text is
short:

> **HAZARD: collides with existing codex/AGENTS.md**

That is the entire recorded hazard — one clause. Any richer hazard statement the architect
remembers is **not on disk**; `grep -rn "HAZARD"` over `docs/intake/` returns this one line and
nothing else.

---

# 5 · Folder governance, quoted

**Propose nothing** — this section is listing and quotation only.

## 5.1 The live root listing

**Directories (17 tracked + `.venv`):** `.claude`, `.claude-plugin`, `.github`, `.vscode`, `codex`,
`config`, `deploy`, `docs`, `ecosystem`, `logs`, `plugins`, `protocols`, `scripts`, `tasks`,
`templates`, `tests` — plus `.venv` (gitignored).

**Files (all tracked; no untracked files at root):**

| File | Bytes |
|---|---|
| `.dev-knowledge.code-workspace` | 8,225 |
| `.gitattributes` | 1,790 |
| `.gitignore` | 3,706 |
| `.methodology.yaml` | 8,900 |
| `.pre-commit-config.yaml` | 11,813 |
| `.pre-commit-hooks.yaml` | 3,297 |
| `.python-version` | 8 |
| `.worktreeinclude` | 496 |
| `ARCHITECTURE.md` | 76,653 |
| `BACKLOG.md` | 232,973 |
| `CLAUDE.md` | 32,479 |
| `CONTRIBUTING.md` | 19,436 |
| `JOURNAL.md` | 2,289,101 |
| `LESSONS.md` | 225,500 |
| `package.json` | 439 |
| `package-lock.json` | 1,253 |
| `pyproject.toml` | 9,607 |
| `uv.lock` | 87,230 |
| `VISION.md` | 9,689 |

(`.git` here is a 94-B worktree gitlink, not a directory, because this is a linked worktree.)

## 5.2 Does a tool mandate each root file's location?

**[orchestrator-corrected]** — a lane marked `.gitattributes` and `.gitignore` as `YES` while its
own evidence column said "no tool mandate found, but standard practice". A mandate you cannot quote
is UNVERIFIED by this arc's own rule, so those rows are corrected below.

| File | Mandate? | The quoted requirement, or the search run |
|---|---|---|
| `.pre-commit-config.yaml` | **YES** | pre-commit resolves its config at the repo root; the repo's own hooks are declared here and `arm_hooks.py` runs `pre-commit install` against it |
| `.pre-commit-hooks.yaml` | **YES** | This file makes the repo a hook *source*; its own header: "This file makes .dev-knowledge a pre-commit *hook source repo*: child repos consume the codemap + TOC tooling." Consumers reference it by repo root |
| `pyproject.toml` | **YES** | PEP 517/518 build-system discovery at project root; `pyproject.toml` §0 — "this repo resolves, installs and runs its gate set through uv" |
| `uv.lock` | **YES** | `pyproject.toml` §0 — "the committed uv.lock + .python-version declare the environment; `uv sync --locked` rebuilds it reproducibly from a clean checkout" |
| `.python-version` | **YES** | same §0 sentence; uv reads it at project root |
| `package.json` | **YES** | npm project identity at root; `.methodology.yaml` — "Node scaffold pin for the vendored Pyright reverse-dependency oracle (#193/ADR-89) and the toc/codemap tooling" |
| `package-lock.json` | **YES** | npm lockfile beside `package.json`; `.methodology.yaml` — "Lockfile of the hub-only Node scaffold above" |
| `.methodology.yaml` | **YES** (repo-internal mandate, not a third-party tool) | `.methodology.yaml` — "Hub conformance metadata — read by the hub Informant (`scripts/enforcement_coverage.py`, [#244] P4/D2)"; ADR-101 §1 sanctions it as a root file class |
| `.worktreeinclude` | **YES** (repo-internal) | `.methodology.yaml` — "configures the native parallel-session worktree lanes (ADR-61/#107 — it is why gitignored ecosystem state is visible inside a lane)"; consumed by `scripts/worktree_seed.py` |
| `CLAUDE.md` | **UNVERIFIED as a quotable tool requirement** | The file asserts its own role — "Session contract for Claude Code in this repo. Read on every session start (auto)" (:12) — but that is the repo describing the runtime, not the runtime's own documentation, which this arc cannot quote from inside the repo. Root placement is real in practice; the *quotable mandate* is not established here |
| `.gitattributes` | **UNVERIFIED** | git honours it at any directory level, so root is convention rather than mandate. Searched `.pre-commit-config.yaml`, `pyproject.toml`, `.methodology.yaml`, `CLAUDE.md`, `CONTRIBUTING.md` for a requirement — none found |
| `.gitignore` | **UNVERIFIED** | Same: git reads `.gitignore` at every level; root is convention. Same search, none found |
| `.dev-knowledge.code-workspace` | **UNVERIFIED** | Searched `CLAUDE.md`, `ARCHITECTURE.md`, `.pre-commit-config.yaml`, `pyproject.toml`, `.methodology.yaml` — no requirement located |
| `ARCHITECTURE.md` | **UNVERIFIED** | `CLAUDE.md` §3 says "read it before structural changes" and §2 lists it under "Critical paths" — editorial, not a tool mandate. The `codemap-freshness` hook validates its *contents*, not its location |
| `BACKLOG.md` | **UNVERIFIED** | `validate-backlog` hook validates contents; no location mandate found |
| `CLAUDE.md`-adjacent docs `VISION.md`, `CONTRIBUTING.md`, `JOURNAL.md`, `LESSONS.md` | **UNVERIFIED** | All four are governed for *content* (append-only rules, freshness stamps) but no tool requiring root placement was located. Searched the hook config, `pyproject.toml`, `.methodology.yaml` and the generators |

## 5.3 The Folder Governance clause, verbatim — and what it does not cover

`protocols/PLAYBOOK.md:2867–2870`, in full:

> ## Folder governance
> - docs/: project-level governance, handoffs, decision records, architecture
> - output/: gitignored, disposable
> - Every generated .md file needs a date (filename or frontmatter)

That is the entire clause. It is not restated in `ARCHITECTURE.md`, `CONTRIBUTING.md` or
`CLAUDE.md`; the other 23 grep hits are reproductions inside `docs/handoffs/*/03_PLAYBOOK.md`
bundle copies.

**No clause governing single-file folders exists.** Searched
`single-file folder | single file folder | one-file folder` (case-insensitive) across `protocols/`,
`docs/decisions/`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CLAUDE.md` — **zero matches**.

This matters for X-5's standing constraint ("a retirement or a filling proposal must quote its
governance source"): as of `9e4b294c` **there is no clause to quote** on single-file folders. The
nearest governing text is the four lines above, which speak to `docs/` and `output/` only.

## 5.4 `config/`, `codex/`, and every other single-file folder

**`config/` — 1 file:**

```
config/requirements-dev.txt   (41 B)
    pre-commit>=3.5.0
    click>=8.0
    pyyaml>=6.0
```

**`codex/` — 1 file:**

```
codex/AGENTS.md   (3,891 B)
```

**Every single-file folder in the tracked tree** (excluding `.git/`, `.venv/`, `node_modules/`,
`.claude/worktrees/`) — enumerated mechanically from `git ls-files`
**[orchestrator-corrected: the lane returned most of these as `unknown`]**:

| Directory | Its one tracked file |
|---|---|
| `.claude/agents/` | `artifact-reader.md` |
| `.claude/rules/` | `git-discipline.md` |
| `.claude/skills/check-against-spec/` | `SKILL.md` |
| `.claude/workflows/` | `conformance-hub.js` |
| `.claude-plugin/` | `marketplace.json` |
| `.github/workflows/` | `report-only-wall.yml` |
| `codex/` | `AGENTS.md` |
| `config/` | `requirements-dev.txt` |
| `docs/handoffs/` | `README.md` (direct children only; its bundle subdirs hold many files) |
| `docs/handoffs/2026-07-07-dev-knowledge-functional/` | `FUNCTIONAL_BOOT.md` |
| `ecosystem/win-tooling/history/` | `2026-07-31.md` |
| `logs/` | `TOKEN-LOG.md` |
| `plugins/tier1-lifecycle/` | `INSTALL.md` (direct children only) |
| `plugins/tier1-lifecycle/.claude-plugin/` | `plugin.json` |
| `plugins/tier1-lifecycle/assets/` | `ruff-pre-commit.yaml` |
| `plugins/tier1-lifecycle/hooks/` | `hooks.json` |
| `scripts/hooks/` | `block_immutable_edits.py` |
| `templates/handoff/functional/` | `FUNCTIONAL_BOOT.md.tmpl` |
| `tests/fixtures/codemap-arch-nomarkers/src/pkg_a/` | `__init__.py` |
| `tests/fixtures/codemap-simple-repo/` | `pyproject.toml` |
| `tests/fixtures/codemap-with-cycle/` | `pyproject.toml` |
| `tests/fixtures/codemap-with-orphan/` | `pyproject.toml` |
| `tests/fixtures/codemap-with-orphan/src/pkg_orphan/` | `__init__.py` |
| `tests/fixtures/repo-with-structural-checks/src/my_pkg/` | `__init__.py` |

**Read this list with two cautions.** (1) It is *tracked-tree* single-file: `logs/` holds exactly
one tracked file (`TOKEN-LOG.md`) but 76 entries on disk, the rest gitignored runtime artifacts
(`PROPOSALS-*.md`, `FLEET-*.md`, `COHERENCE-NUDGE.log`, `PARITY-EVENTS.jsonl`, …). (2) Rows marked
"direct children only" are single-file at their own level but parent to populated subdirectories.
Only `codex/` and `config/` are single-file in the plain sense the challenge asked about.

---

# 6 · win-tooling organ state

The sixth satellite, surveyed on the axes the other five got on 2026-08-08.

## 6.1 Pre-commit config — **ABSENT**

```
$ ls -la C:/Users/1028120/Documents/Dev/win-tooling/.pre-commit-config.yaml
ls: cannot access '.pre-commit-config.yaml': No such file or directory
$ git ls-files | grep pre-commit
(no output)
```

No hook ids, no pinned revs, nothing to enumerate.

## 6.2 Installed hooks — **NONE ARMED**

`.git/hooks/` holds 14 files, **all `.sample`**: `applypatch-msg`, `commit-msg`,
`fsmonitor-watchman`, `post-update`, `pre-applypatch`, `pre-commit`, `pre-merge-commit`,
`prepare-commit-msg`, `pre-push`, `pre-rebase`, `pre-receive`, `push-to-checkout`,
`sendemail-validate`, `update` — untouched git defaults.

```
$ ls .git/hooks/ | grep -v ".sample$"
(no output)
$ git config --get core.hooksPath
(unset)
```

**`core.hooksPath` is UNSET** — so this is a genuine absence, not the relic-hooksPath failure mode
that silently disarms an otherwise-configured repo. Both facts independently re-verified by the
orchestrator.

## 6.3 Hook stages — none

| Stage | State |
|---|---|
| pre-commit | ABSENT |
| commit-msg | ABSENT |
| pre-push | ABSENT |

No `default_install_hook_types` declaration exists, there being no config to declare it in.

**Net:** win-tooling is **effectively UNGATED** — the same 🔴 class as corp-ops, and by the same
mechanism (no config + no armed hooks). Every commit in §6.7's history passed through no gate.

## 6.4 Branch naming — fully conforming

Current branch `main`. 14 local branches; every one carries an enum prefix:

- `chore/` ×4 — `typewhisper-hold-draft-and-detector`, `typewhisper-plugin-ab`,
  `typewhisper-plugins-as-code`, `typewhisper-retention-and-recycle`
- `docs/` ×2 — `typewhisper-issue-filenames`, `typewhisper-postfix-evidence`
- `feat/` ×2 — `dispatch-v2`, `typewhisper-pin-106`
- `fix/` ×5 — `typewhisper-cpu-instrument`, `typewhisper-jam-real-probes`,
  `typewhisper-junctions-and-upstream-check`, `typewhisper-nospeech-toggle-only`,
  `typewhisper-responding-vacuous`, `typewhisper-stability-audit`
- plus `main`

**CONFORMING: all.** No off-enum branch (contrast corp-sca-time-automation's
`feature/tenrox-loader`).

`git log --first-parent --oneline -20 main` shows **20 of 20 merge commits, zero direct-to-main
non-merge commits** — core-invariant #5 is being honoured by hand, with no hook enforcing it.

## 6.5 Tests — present

4 files under `tests/`: `test_compat.py`, `test_config.py`, `test_engine.py`, `test_io_utils.py`
(plus `__init__.py` and `_wmi_guard_plugin.py`). **41 test functions** (`grep -rn "^def test_"`).

pytest configured in `pyproject.toml:42–47`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
# Load the WMI-hang guard plugin first (before pytest's capture plugin imports
# pyreadline3, which hangs on a wedged WMI service). See tests/_wmi_guard_plugin.py.
addopts = "-p tests._wmi_guard_plugin"
```

Bearing on §A row 40: this repo already uses **shape B** (`pythonpath = ["src"]`) — the shape the
hub's `[#502]` measurement direction points at. It also carries a root `conftest.py` (635 B).

## 6.6 pyproject / locks

`pyproject.toml` present (1.3 KB). Verbatim:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "win-tooling"
version = "0.2.0"
description = "Personal Windows desktop-productivity toolbox - local transcription + TypeWhisper dictation-quality helpers."
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "click>=8.1",
    "rich>=13.0",
    "pyyaml>=6.0",
    # Preferred transcription backend. whisperx / openai-whisper are optional fallbacks
    # (see [project.optional-dependencies]); the engine auto-selects whichever is present.
    "faster-whisper>=1.0",
]

[project.optional-dependencies]
fallback = [
    "openai-whisper",
    "whisperx",
]
dev = [
    "pytest>=8.0",
]

[project.scripts]
# transcription domain
win-transcribe = "win_tooling.transcription.cli:main"
# dictation domain (TypeWhisper correction harvester; proposal-only)
win-harvest-corrections = "win_tooling.dictation.harvest:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
# Load the WMI-hang guard plugin first (before pytest's capture plugin imports
# pyreadline3, which hangs on a wedged WMI service). See tests/_wmi_guard_plugin.py.
addopts = "-p tests._wmi_guard_plugin"
```

**[orchestrator-corrected]** — the lane's transcription HTML-escaped every `>=` to `&gt;=`; the file
uses plain `>=`, re-read from disk and reproduced above.

**No lockfile of any kind:** `uv.lock` absent, `requirements.txt` absent, `poetry.lock` absent,
`package-lock.json` absent. **`.python-version` absent.** So the ADR-106 uv environment-isolation
posture the hub declares is **not** present here — the repo declares a floor (`>=3.10`) and pins
nothing.

## 6.7 Repo shape

Root: `.claude/`, `.vscode/`, `config/`, `logs/`, `output/`, `scripts/`, `sources/`, `src/`,
`tests/`, `tools/`, plus `ARCHITECTURE.md` (19 K), `BACKLOG.md` (2.8 K), `CLAUDE.md` (6.9 K),
`CONTRIBUTING.md` (2.3 K), `JOURNAL.md` (94 K), `LESSONS.md` (56 K), `README.md` (6.9 K),
`config.yaml` (2.2 K), `conftest.py` (635 B), `pyproject.toml`, `.gitignore`,
`.win-tooling.code-workspace`.

Most recent commit **2026-08-08 16:44:24 +0200**, `d743937` *"Merge branch 'feat/dispatch-v2':
contract file becomes the dispatch source"*.

`CLAUDE.md` present (7,018 B, 103 lines). **`AGENTS.md` absent.**

---

# Honest gaps — what this arc could not establish

Recorded as findings, per the contract's rule that an honest gap beats a plausible fill.

1. **Batch 1–2 mention-vs-invocation (§1.3).** The counts are occurrences in retrospective
   artifacts. Proving a command was actually *invoked* needs the session transcripts, which were
   outside this arc's read scope. `unknown` by scope.
2. **A quotable third-party mandate for `CLAUDE.md` at root (§5.2).** The repo asserts the runtime
   reads it; the runtime's own documentation is not quotable from inside the repo. Marked
   UNVERIFIED rather than assumed.
3. **The `ARC-challenge-retrieval.md` contract file.** Absent from disk; searched
   `C:\Users\1028120\Downloads` for `*challenge*` and `ARC-*`. Executed from the inline contract.
4. **`terminal-setup` and `overnight`/`illustrated-book-gen`.** `terminal-setup` carries no
   instruction file at all. `overnight` and `illustrated-book-gen` are directories under `Dev/` that
   are **not git repos**, so they were not surveyed as satellites.
5. **W-9a's richer hazard.** Only the one clause at intake #27 §A row 21 exists on disk (§4.4).
   If the architect recalls a fuller hazard statement, it was never written down.

# Where this report contradicts the challenge answer

Three places, each with the evidence above:

- **X-4.3** says the W-9a hazard "is recorded in intake #25". It is not — intake #25 contains zero
  occurrences of "HAZARD"; the sole record is intake #27 §A row 21, and it is one clause (§4.4).
- **X-3** says intake #27 §A has **36 rows**. It has **38** — rows 37 and 40 were added
  2026-08-08 in `08c3e0b6` (§3.1, §3.2).
- **X-2.4** treats a subagent-spawning workflow as an open inventory question. One exists and is
  committed: `.claude/workflows/conformance-hub.js`, surfaced as the `conformance-hub` skill
  (§1.2). Whether that answers what X-2.4 asked is the architect's call.
