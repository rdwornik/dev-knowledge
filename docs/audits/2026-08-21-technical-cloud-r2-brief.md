# CLOUD-R2 — universalization readiness (provider-agnostic repo)
slug: cloud-r2-universalization · effort: high · read-only

**RULES (binding):** You are a READ-ONLY review lane in `.dev-knowledge` (bound at Revision main). Read your subject from the repo first — repo is the record. You mutate NOTHING except ONE file: `ARTIFACT-<slug>.md` (slug below) committed once on your own session branch; then STOP. Never merge, never push main, never touch tasks/, BACKLOG.md, STANDING_RULINGS §Q, protocols/, .pre-commit-config.yaml, .gitignore, docs/intake/, or move any file. Findings = EVIDENCE + RECOMMENDATION; the architect rules — you change nothing. Shallow-clone guard: if this environment lacks full git history, do NOT run spine-walking instruments (validate_git_backlog and kin) — skip and say so. If any instruction here conflicts with repo core-invariants, the repo wins: report the conflict, do not improvise.

**Purpose:** the evidence base for making the repo provider-agnostic (swap models/CLIs via a
table, not a rewrite). Four sections, each ends with a go/no-go recommendation for the
future MUTATION lane (CLOUD-4), which will be cut from THIS artifact.

**Done-contract:**
1. **VISION→README reference census:** every file+line that names or links VISION.md
   (grep the whole tree, include workflows, scripts, protocols, ADRs, handoff templates).
   The rename is a reference migration — this census is its complete input. State the count
   and the riskiest references (ones a bare rename would silently break).
2. **AGENT.md / agents.md standard:** map the published agents.md convention against what
   CLAUDE.md carries today; propose the split (universal AGENT.md vs provider-specific
   file) citing the standard — library-first, do not invent a format. List exactly what
   would move where.
3. **Provider-swap seam inventory:** every hardcoded model/CLI/provider name in scripts,
   PLAYBOOK, contracts, routing docs — table: location · what is hardcoded · swap cost
   {table-edit / code-change / doctrine-change}.
4. **[#82] provider profiles:** read the row; list the design inputs its build lane needs,
   and which of sections 1–3 feed it.
Commit ARTIFACT-cloud-r2-universalization.md, STOP.
