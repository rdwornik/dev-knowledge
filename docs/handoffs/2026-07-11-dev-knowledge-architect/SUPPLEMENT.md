# Architect strategic supplement — 2026-07-11-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-11

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
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

1. STRATEGIC INTENT — Universalization + hermetization of the methodology across the three
repos (dev-knowledge / ai-council / corp-monorepo) is priority ONE. Dev-knowledge is the
source of truth over what is methodology-specific vs project-specific. Next session's
way-of-working goal: produce the evidence-based BOUNDARY per surface (root files, CLAUDE.md
sections, hooks inventory, folders, protocols/, .code-workspace, caches, tests layout),
document it in the PLAYBOOK, and route it into mechanisms (carriers/gates/routines), not
prose. Framing correction on record: Wave-1 n=2 proved the ENFORCEMENT layer is in effect;
it never proved structural uniformity — that gap is this charter. "All onboarded = all OK"
is hereby rejected as a claim shape.

2. TENSIONS WEIGHED — (a) universal-vs-project boundary: land = every CLAUDE.md carries an
explicit methodology block (~identical fleet-wide, hub-owned) + a free project block.
(b) visible-outcomes bar vs meta-work: this audit is meta but operator-ruled P1; it
qualifies because trustworthy fleet rollout (P6 carriers) is blocked without the boundary.
(c) epic numbering: KEEP numbered IDs fleet-wide (EPIC n / S-n / #n) — referenceability
wins; settled, do not relitigate. (d) ARCHITECTURE ToC: operator leans REMOVE — but
toc-freshness is a deployed hub@v1.2.0 carrier component, so removal = a methodology
component deprecation decision, not a doc edit. (e) Mermaid: operator now leans REMOVE-ALL
(visualization method changing) — NOTE this reverses the 2026-07-11 menu-12 ruling
(M1/M2 KEEP-HAND-AUTHORED) and, with #262 BLOCKED, deletion without a successor leaves corp
mapless. Successor first, deletion second.

3. CONSIDERED + REJECTED (do not relitigate) — (a) deleting .methodology.yaml: REJECTED
WITH EVIDENCE — permanently answered 2026-07-11 (corp brief §3.2-A): hub Informant contract
file at the fixed root path (enforcement_coverage ALLOWLIST_REL + fleet_health); operator
ratified KEEP-ROOT + the CLAUDE.md §4 note. (b) "only hub has pre-commit hooks": CORRECTED
— all three repos have armed hooks (corp: 6 firing, QA-proven scorecard; ai-council: B-S1);
the real divergence is hook-SET inventories (empty commit-msg/pre-push stages = #302 +
parity item). Audit compares inventories, never presence. (c) retroactive renames: rejected
by ADR-101 (prospective-only + grandfather, Accepted). (d) redoing dependency mapping
(code-to-code/file-to-file): works, not a bottleneck, out of scope. (e) re-numbering
debate: settled per (2c).

4. OPEN QUESTIONS (the audit's charter) — (a) where exactly the methodology/project
boundary runs, per surface. (b) protocols/ as a methodology-mandated genre? (ai-council
has it, corp lacks it; operator wants per-package protocol docs in corp — "interface in
markdown", coupled to ARCHITECTURE). (c) ToC deprecation (carrier impact) + Mermaid
successor (vs the #262 codemap north star; corp G11 requirement input stands). (d) the
missing consolidation MECHANISM: a routine/generator that concatenates + diffs all
CLAUDE.md (methodology blocks) fleet-wide and surfaces drift continuously — the "3 months
and still invisible" gap; candidate new organ. (e) .claude/ full review across repos
(worktrees, workflows, skills — gotchas already universalized); commands documentation
coverage in each CLAUDE.md (/codex-review present; /code-review and other session commands
missing). (f) INSTALL.md in ai-council root vs absent in corp — why, and which is
methodology. (g) .code-workspace diffs; cache-folder policy (ai-council has ruff/pytest/
mypy caches, corp doesn't — programming-style drift evidence). (h) CI/CD report currency.
(i) tests/ layout chaos in corp (separate dedicated session — flag only). (j) web-research
leg: are there better current libraries/approaches for architecture + dependency
visualization (file-to-file, file-to-code, code-to-code) than our home-grown set —
sky-is-the-limit budget.

5. DECOMPOSITION RATIONALE — shape: ONE big multi-dimensional comparative audit session
(read-heavy → read-only parallel fan-out per repo is sanctioned; synthesis serial),
deliverable = a DIVERGENCE MATRIX with per-item disposition (methodology-generic vs
project-specific vs defect) + PLAYBOOK update; mechanism-building sessions follow, never
inside the audit. The audit must BUILD ON (not repeat): the 2026-07-11 corp root-hygiene
audit + the naming census (they are INPUTS — corp root is already inventoried to the file),
ADR-101 + audit-template (ratified), the QA n=2 scorecard (gates fire — do not re-prove),
gotchas universalization (done). The audit must NOT end with a verdict ("all OK" is a
banned claim shape) — it ends with the matrix + dispositions for operator ruling.

6. OFF-REPO CONTEXT — Operator trust statement on record: trust in the system is GATED on
visible universalization; treat as P1 posture until the boundary is documented and
mechanism-held. Queue after the audit: #270 (clock-triggered staleness — demoted from
headline to position 2 by operator priority), builds #306/#307, corp D4 refresh (GO
stands), CLAUDE.md trim RANK 1+2+3 (architect GO stands), #302 + commit-msg parity,
57 WEAK closure candidates grooming pass. Standing: codex-review now pinned gpt-5.6-sol
(A/B-proven, caught #311); P7 one-liner STILL OWED (closes EPIC C). Session plan file +
verdict sheet from 2026-07-10/11 are the audit's provenance trail.
