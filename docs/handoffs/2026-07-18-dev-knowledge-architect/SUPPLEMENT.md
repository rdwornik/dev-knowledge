# Architect strategic supplement — 2026-07-18-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-18

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

ANSWERS — authored by the outgoing browser architect (2026-07-18); CC transcribes verbatim. Supersedes the CC-drafted fill in full.

STRATEGIC INTENT — One goal above all others, operator-dictated: UNIVERSALIZATION. A single fleet-wide pattern for system architecture, file naming, folder structure, and file structure — AND a universalized DEPLOYMENT of that pattern — so every repo is manageable from the center and improvable uniformly. The operator's bar, verbatim in spirit: "I never again want to ask why files differ between repos." Equalization of corp-monorepo + ai-council (ARC 4) is the first APPLICATION of the pattern, not the goal itself: every align must, where possible, land as manifest/template/carrier material that REPLICATES onto the next repo, not as a one-off file fix. This includes dependency/test-library parity (a missing pytest library made one repo's tests slower — dep parity is part of structure), test-suite optimization, and rolling libraries out where needed. Ladder position: explain→consolidate→document→ENFORCE are done; this cycle enters AUTO-DEPLOY and MANAGE.

OPERATOR PRIORITY PROGRAM (dictated 2026-07-18, in priority order — the next sessions' agenda skeleton):
1. Universalization of structure + deployment (above).
2. Formalize the engineering loop/harness end-to-end: intake → functional requirements (a functional-architect session that seeds the backlog) → ADR → implementation → sandbox/console dynamic testing → review → backlog close + REAL deletion. Standing pain named by the operator: files get frozen/tombstoned instead of properly deleted — the junkyard effect; design a sanctioned safe-deletion pattern (extends the proof-then-delete ruling on #122).
3. Night routines + CONFIGURED multiagent workflows (self-orchestrated Sonnet/Haiku fan-out, no ultracode) + backlog grooming as routine + Q&A sessions — stop re-improvising these per session; make them configuration.
4. Mechanize session discipline: a fresh browser must inherit "a session ends only after proper testing and the close sequence" from a gate/boot mechanism, never from the operator reminding it.
5. Handoff-process improvements — other browsers able to trigger a handoff; file-dependency issues at handoff; general refinement. Explicitly LAST priority.

BINDING RULINGS (made in the outgoing chat; travel verbatim):
- RULING-W: hub MAY/SHOULD write into consumer repos for methodology/cleanup — separate worktree/branch, then report; FIRST step of any consumer leg = codify this as the ADR-36/41 amendment (mechanism before act).
- RULING-S: every governed file gets READER-VISIBLE sections separating methodology-universal vs repo-personal content (CLAUDE.md + configs; machine markers alone insufficient).
- RULING-PY: ruff baseline targets py311 now (corp floor ≥3.11); standing direction "always newest Python" → file the fleet-Python-upgrade ticket.
- RULING-CF: ai-council adopts the conformance workflow (equalize upward).
- #329 design input: editor-side background decoration (grey/navy on dark theme) of owner=hub/owner=repo regions via versioned .vscode — the human-facing half of RULING-S.
- #341 R2: producer-activation = sanctioned repo-local AGENTS.md override (per-run flag REJECTED on witnessed precedence evidence).
- Satellite wave: FROZEN until corp + ai-council lessons are extracted.

TENSIONS WEIGHED — pattern-vs-patch: operator explicitly rejects one-off aligns without a deployable pattern behind them. Mechanism-before-act: the ADR-36/41 amendment lands before any consumer edit. Freeze-vs-delete: tombstone doctrine served safety but breeds the junkyard; a real deletion path is now wanted (design question, not yet ruled). Breadth-vs-depth: unchanged — two Wave-1 consumers first, wave frozen.

CONSIDERED + REJECTED (do not relitigate): per-run codex profile/flag (#341 R2, witnessed); firing the satellite wave now; unmediated hub↔consumer writes (RULING-W path only); immediate newest-Python baseline bump (ticketed lift instead); equalization as one-off fixes without replication material (operator intent).

OPEN / DEFERRED: #344 session-close gate + consumer hub-write guard (needs ruling; its guard must ALLOW the RULING-W path); fleet-Python-upgrade ticket unfiled; safe-deletion pattern design; functional-architect role/session design (seeds backlog with functional requirements); night-workflow configuration formalization; #343 fleet_parity ship-gate-only scoping; #339 build leg; #342; #300 residual d.i/d.ii (d.iii COVERED by ADR-101, closeable); #341 build (mechanism ruled); #338; night-triage 15 findings; #162 vocab collision; handoff-trigger-from-other-browsers (last).

DECOMPOSITION RATIONALE — ARC 4 opens the cycle: (1) ADR-36/41 amendment (RULING-W codified), (2) re-witness BOTH consumers live (their HEADs moved repeatedly — never edit from a stale ledger), (3) equalize with replication in mind (manifest rows / templates / carrier material), sections per RULING-S throughout. Then the loop-formalization work (priority 2-3) as its own arcs. Do NOT redo: the seven rulings, the census classifications, the R2 mechanism, the frozen wave, the night-ledger verdicts (re-witness refreshes state, not the verdict logic).

OFF-REPO CONTEXT — The approved ARC 4 prompt file is operator-held (off-repo). Two stale background agents (5d/11d) were stood down with commit-and-STOP wind-down orders; their reports may surface residual branches — operator rules integrate-vs-discard. The 2026-07-17 night-audit artifacts are filed in docs/audits (four files). This supplement was authored by the browser architect; CC transcribed it verbatim (the authorship rule is now standing).
