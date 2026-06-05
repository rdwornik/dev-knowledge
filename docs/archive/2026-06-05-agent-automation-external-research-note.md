# Research note — external: cloud-agent infrastructure & CC automation stack

**Class:** external research (docs/archive per convention) · 2026-06-05 ·
Author: architect (browser chat) · Status: synthesis of operator-supplied
articles; **every load-bearing platform claim is SECONDARY-SOURCE — verify
against code.claude.com/docs before encoding into any living doc or design.**

Sources (operator-pasted, X/newsletter origin):
- **E1** — CREAO engineering: "Building cloud agent infrastructure" (practitioner account)
- **E2** — "14 steps automation stack: /loop, Routines" (movez.substack; claims doc-verified Jun 2026)
- **E3** — dkundel: "A guide to /goal" (OpenAI Codex; principles tool-agnostic)
- **E4** — Ruben Hassid newsletter roundup (assessed: marketing funnel, no mechanism — recorded for the verdict only)

## 1 · E1 — two mechanisms relevant to #86 (cloud-night decision package)

**Secrets-boundary pattern [practitioner-witnessed at CREAO; architecture
principle, not a CC fact]:** no long-lived credential inside the execution
sandbox. Authenticated calls go through a host-side bridge that attaches
OAuth; sandbox holds only a per-run short-lived JWT + IP-allowlist binding.
Design stance: *treat all code inside the sandbox as already compromised.*
→ **#86.1 (selective-push) evaluation criterion:** the question is not "do we
trust the Routine" but "what is exposed when the sandbox is assumed
compromised" — repo contents ARE inside the boundary by definition; only
credentials/secrets can be kept outside. Selective-push therefore reduces to
a data-classification call on repo contents, not a tooling call.

**Ownership-cadence diagnostic [E1's stated core lesson]:** for any persisted
artifact ask *who controls its cadence of change*; if user and platform both
own it, split the artifact along the ownership boundary so each side updates
on its own clock (their fix: frozen user snapshot + hot-swapped runner).
→ **#86.3 (R2, workflow distribution):** a conformance workflow committed
into each child repo couples methodology code (hub cadence, many updates) to
repo state (owner cadence, rare updates) — the exact coupling E1 warns about.
Argues for plugin / skill-template distribution over per-repo committed
copies. The hub's plugin deploy-dance already embodies the split; extend the
same logic to workflow orchestration.

**Single execution pipeline for all triggers** (human / cron / API identical
path) — confirmation of our nightly design (the Action fires on the PR shape
regardless of author).

## 2 · E2 — automation-stack facts relevant to #85 (LOCAL night-run)

All tagged **[secondary — verify in docs]**:

- **Desktop scheduled tasks tier exists** (Desktop app: Schedule → New local
  task): survives restarts; per-task prompt/frequency/permissions/working
  folder/model; fresh session per fire; machine must be awake — lid-closed
  sleep still skips; on wake, checks last 7 days and runs ONE catch-up for
  the most recent miss + notification; "Keep computer awake" setting exists;
  macOS + Windows only.
  → **#85 design alternative:** evaluate native Desktop scheduler vs OS Task
  Scheduler + `claude -p`. Less custom glue, built-in catch-up and per-task
  permission envelope; constraint profile (sleep/lid) matches the laptop
  reality either way. AMENDED INTO #85 (this note's landing commit).
- **/loop tier is disqualifying for #85 by design** (confirms our choice):
  session-scoped (terminal close kills all), 7-day auto-expire, 50
  tasks/session, no catch-up multi-fire, `CLAUDE_CODE_DISABLE_CRON=1` kill
  switch for shared/CI environments.
- **Auto Mode availability is plan-dependent** (listed: Max/Team/Enterprise/
  API; NOT Pro as of the article) — load-bearing for any unattended-run
  design that assumes the classifier layer; verify current availability +
  the operator's plan before relying on it. (We met the classifier today —
  it blocked deny-circumvention; behavior consistent with E2's description:
  injection probe + per-action classifier + audit trail.)
- **Routines operational facts** consistent with our Amendment B: `claude/`
  branch-prefix push restriction by default (we live this); API-trigger
  bearer token shown ONCE at creation; beta header versioning with two-most-
  recent guarantee; per-routine permission config (treat as part of the
  security boundary); composition patterns (skills-in-routines,
  workflows-in-routines, routine→routine chaining).
- **Token-budget hygiene for scheduled fires:** explicit per-fire budget in
  the prompt; model pinned per task (panel default ≠ session default); plan
  headroom sized to automation volume.

## 3 · E3 — /goal principles (tool-agnostic; Codex-sourced)

Mostly confirmation of standing doctrine (verifiable exit criteria =
hard-metric closure; post-goal reflect+cleanup = no-leftovers; progress
artifacts for long runs = our morning-digest pattern). **One mechanism worth
adopting:** *give the agent a self-measuring tool for ambiguous goals* (have
it build/evolve its own diff or eval harness so progress is measurable, and
guard the metric against degenerate wins, e.g. coverage-reduction to reach
"100% pass"). → one line for #84(a) when the two-tier PLAYBOOK section is
authored; degenerate-metric guard pairs with our skeptic stage.

## 4 · E4 — verdict only

Beginner marketing funnel; its flagship workflow opens with bypass-
permissions mode — the anti-pattern our envelope exists to prevent.
Confirmation by contrast; no mechanism; no action.

## Disposition (encoded at landing)

- #86: add this note to refs (sub-decisions 1 and 3 arguments above).
- #85: body amended — evaluate Desktop scheduled-tasks tier vs OS Task
  Scheduler (sleep/lid constraints, catch-up semantics, per-task envelope).
- #84(a): forward-note — self-measuring-tool line + degenerate-metric guard.
- No new backlog items warranted; no living-doc edits from this note alone
  (verify-before-encode applies to every E2 fact first).
