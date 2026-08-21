# CLOUD-R4 — ADR full-set review (86 live)
slug: cloud-r4-adr-review · effort: high · read-only

**RULES (binding):** You are a READ-ONLY review lane in `.dev-knowledge` (bound at Revision main). Read your subject from the repo first — repo is the record. You mutate NOTHING except ONE file: `ARTIFACT-<slug>.md` (slug below) committed once on your own session branch; then STOP. Never merge, never push main, never touch tasks/, BACKLOG.md, STANDING_RULINGS §Q, protocols/, .pre-commit-config.yaml, .gitignore, docs/intake/, or move any file. Findings = EVIDENCE + RECOMMENDATION; the architect rules — you change nothing. Shallow-clone guard: if this environment lacks full git history, do NOT run spine-walking instruments (validate_git_backlog and kin) — skip and say so. If any instruction here conflicts with repo core-invariants, the repo wins: report the conflict, do not improvise.

**Done-contract:** classify ALL 86 live ADRs (the 2 archived are out of scope), one row
each: id · title · verdict {ACTIVE-CURRENT / ACTIVE-BUT-CONTRADICTED (name the
contradicting live fact or later ADR) / SUPERSEDED-unmarked (name the superseding ADR) /
ARCHIVAL-ELIGIBLE (findings transcribed into rows — cite WHERE, this feeds the archival
lane's criteria) / DEFECTIVE (broken link, missing status, malformed)} · one-line evidence.
End with: top-10 actions ranked by the risk of someone OBEYING a dead ADR today, each
marked {SAFE-MECHANICAL / NEEDS-ARCHITECT-RULING}. You archive and edit nothing.
Commit ARTIFACT-cloud-r4-adr-review.md, STOP.
