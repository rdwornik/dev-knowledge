# Architect strategic supplement — 2026-08-06-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-06

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

Q1. STRATEGIC INTENT: Stop preparing parallelism — exercise it. The next
session's way-of-working goal is to run batch 1 (3 lanes + integrator) as a
MACHINERY DRILL and prove the V-1 shape end-to-end (worktree lanes, frozen
contracts, per-lane V-2 budgets, single serial integrator, exactly 2
operator touches), then go wide in batch 2 (pre-named, R-i: 5-8 lanes —
#25 W-wave · [#487] repaired-pipeline legs · [#490] North-Star entry).
"Three windows of hub introspection spent" is a commitment, not a mood.

Q2. TENSIONS WEIGHED: (a) narrow-vs-wide batch 1 — staging won (3 lanes
drill the machinery; width without a proven integrator is risk, not speed).
(b) ADR-now vs ADR-at-arming for server-side enforcement — arming-moment
won; tier=Free then removed arming's live trigger entirely. (c) [#487]
engine-vs-judgment — judgment + pipeline-repair won on evidence (0 confirms
/62 files/2 months). (d) process-production vs shipping — register+template
landed but Finding-1 proved the cost of touching doctrine surfaces without
the coupled updates; the introspection budget is declared SPENT. (e) UI
cockpit vs contract discipline — VS Code Agents window adopted as cockpit,
ruled NEVER load-bearing (lane discipline comes from contract + gates).

Q3. CONSIDERED + REJECTED: vale as ratchet host (measured refutation:
per-block counting, closed scripting hatch — 441 stays bespoke) · P2 as its
own row (folded into [#493]) · equalizing the ~10 work-lane ceiling with
the 2-3 epic-lane cap (different axes, now cross-pointed) · name-match
closes ([#170] defense) · ceiling-change as the prose-orphan fix (rejected
in R-C; diagnosis-home standard adopted instead) · origin/* reads without
fetch as remote evidence (V-1 lesson iii) · root AGENTS.md without
codex/AGENTS.md reconciliation · WSL for mutmut (operator: CI-only) ·
public repos for CI minutes (standing, employer material).

Q4. OPEN QUESTIONS: [#408] per-section granularity values (pre-chewed in
the night design draft; operator decision) · [#487] repair-leg sequencing
inside batch 2 · [E8] ARC-5 has NO completion record — silently stopped or
unrecorded? · DEFINITION_OF_DONE.md is outside the freshness-gated set ·
W-6 schema-as-code placement · STANDING_RULINGS B2 label + three V-1
doctrine lessons (uv-pin load-bearing; mid-flight lane corrections =
untrusted; fetch-before-remote-evidence) — OWED next window · assisted-
approvals posture after batch-1 experience.

Q5. DECOMPOSITION RATIONALE: batch 1 is cut by FILE-OWNERSHIP
footprint-disjointness with the one shared file (ARCHITECTURE.md) held out
of all lanes and carried by the integrator; [#502] rides as [#501]'s
dependency-chained tail (CI-only ruling). Do NOT redo or re-decide:
R-A/R-B/R-C/R-D rulings and their red-team amendments · the batch-1 cut
(operator GO + predecessor approve on record) · grooming verdicts · the
four births' scope and footprints · B3's refutation.

Q6. OFF-REPO CONTEXT: GitHub tier = Free (checked in Billing) → [#501] is
report-only recorder indefinitely; WSL excluded by operator; VS Code
1.129/1.130 cockpit research done (Agents window, agent host, New Worktree
checkbox) with a pre-batch-1 checklist — enablement is being executed in a
parallel terminal THIS session so the successor boots into a ready cockpit;
operator's Downloads carry: SESSION-PLAN (v2, §A-§J), VSCODE-PARALLEL-
COCKPIT, SUPPLEMENT-ANSWERS-C1-C8 (predecessor riders folded in header).

Q7. RATIFIED-IN-CHAT REGISTER (not yet in repo): "batch-1 cut as named +
GO" — 3 lanes + integrator holding ARCHITECTURE.md; home: this supplement +
successor bundle intent · "riders R-i/R-ii/R-iii" — batch-2 pre-named,
W-5 placed-not-deferred, supplement-commits-clean; home: this supplement ·
"cockpit adopted, never load-bearing" — VS Code Agents window is optional
sugar on unchanged mechanics; home: LESSONS one-liner or next window's
STANDING_RULINGS pass · "introspection budget spent" — hub-only windows end
here; home: successor bundle Purpose. The three V-1 lessons + B2 label are
already listed in Q4 with their durable home (STANDING_RULINGS, next
window). Everything else ratified this window is already ON the spine
(A2 rule 042ef33b · JOURNAL-rides-the-branch mechanism in seal 616f4814 ·
scope-split precedence adf85c4a).

ADDENDUM (post-enablement, binding successor intents):
· Fourth V-1 lesson: bare pytest in a worktree lane inherits VIRTUAL_ENV
  from the primary tree and tests the WRONG environment — `uv run --locked`
  is mandatory per lane (joins the three lessons for the STANDING_RULINGS
  pass).
· Parallel-management architecture RULED this window (do not relitigate):
  Track 1 (batch 1) = CC-native primitives (`claude --worktree`, agent
  view / `claude agents`) + the batch protocol REPO-ENCODED as versioned
  artifacts (PLAYBOOK §, project-scoped .claude/commands/, handoff-bundle
  pointer) so no seat depends on memory — authoring that protocol is the
  successor's task, [#429] slim scope (adopt-native + hygiene-organ WARN +
  lane/ branch-prefix enum). Track 2 (batch 2, multi-provider) = 30-min
  eval of Vibe Kanban WITH its official VS Code extension
  (bloop.vibe-kanban), PASS criteria pre-named: in-IDE tasks/logs/diffs ·
  full lifecycle incl. worktree CLEANUP verified · second provider (Codex)
  on one card · headless server as a VS Code task; version pinned in
  win-tooling config-as-code; sunset-to-community risk accepted because
  lock-in is zero. Rejected with reasons: hand-rolled /batch-* (native
  /batch exists), web-UI-outside-VS-Code as primary surface, tmux (WSL),
  Copilot-gated Agents window. herdr on the watch-list (terminal
  multiplexer candidate if the native board stops sufficing).
