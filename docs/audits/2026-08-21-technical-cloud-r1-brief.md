# CLOUD-R1 — governance drift audit: ARCHITECTURE.md · CLAUDE.md · VISION.md
slug: cloud-r1-governance-drift · effort: high · read-only

**RULES (binding):** You are a READ-ONLY review lane in `.dev-knowledge` (bound at Revision main). Read your subject from the repo first — repo is the record. You mutate NOTHING except ONE file: `ARTIFACT-<slug>.md` (slug below) committed once on your own session branch; then STOP. Never merge, never push main, never touch tasks/, BACKLOG.md, STANDING_RULINGS §Q, protocols/, .pre-commit-config.yaml, .gitignore, docs/intake/, or move any file. Findings = EVIDENCE + RECOMMENDATION; the architect rules — you change nothing. Shallow-clone guard: if this environment lacks full git history, do NOT run spine-walking instruments (validate_git_backlog and kin) — skip and say so. If any instruction here conflicts with repo core-invariants, the repo wins: report the conflict, do not improvise.

**Question this answers:** the repo is worked 8h/day, yet ARCHITECTURE.md (stamp 2026-08-14,
equal to its last touch) and CLAUDE.md rarely change — stale, or stable by design? Prove
drift with evidence; do not assume it from age.

**Done-contract:**
1. Claim-by-claim pass over ARCHITECTURE.md, CLAUDE.md, VISION.md vs the live repo
   (structure, scripts/, check registry count in scripts/audit.py, workflows, dispatch/lane
   reality, worktree doctrine, protocols). Output table per file:
   claim · live evidence (path/line or command output) · verdict {CURRENT / STALE /
   MISSING-COVERAGE (repo does X, doc silent)} · proposed one-line fix.
2. CLAUDE.md extra pass: mine JOURNAL.md and docs/audits/ for REPEATED executor mistakes;
   list the top lines that, added to CLAUDE.md, would have prevented them — ranked by
   frequency of the mistake, with citations.
3. End section: top-10 fixes ranked by operator impact, each one line, marked
   {SAFE-MECHANICAL / NEEDS-ARCHITECT-RULING}.
Commit ARTIFACT-cloud-r1-governance-drift.md, STOP.
