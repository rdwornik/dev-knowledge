# CLOUD-R3 — conformance review, [#171] leg 2 scope
slug: cloud-r3-conformance · effort: medium · read-only

**RULES (binding):** You are a READ-ONLY review lane in `.dev-knowledge` (bound at Revision main). Read your subject from the repo first — repo is the record. You mutate NOTHING except ONE file: `ARTIFACT-<slug>.md` (slug below) committed once on your own session branch; then STOP. Never merge, never push main, never touch tasks/, BACKLOG.md, STANDING_RULINGS §Q, protocols/, .pre-commit-config.yaml, .gitignore, docs/intake/, or move any file. Findings = EVIDENCE + RECOMMENDATION; the architect rules — you change nothing. Shallow-clone guard: if this environment lacks full git history, do NOT run spine-walking instruments (validate_git_backlog and kin) — skip and say so. If any instruction here conflicts with repo core-invariants, the repo wins: report the conflict, do not improvise.

**Done-contract:** review conformance.html AND its generator, scoped EXACTLY per [#171]
leg 2 as written in that row — read the row first. If leg 2's scope is ambiguous, review
against the row's literal text and FLAG the ambiguity; never widen scope on your own.
Output: findings table — item · evidence (path/line) · severity {P1/P2/P3} · proposed
disposition — plus one paragraph: what the operator SEES in conformance.html today vs what
[#171] leg 2 says they should see. No fixes, no dispositions, evidence only.
Commit ARTIFACT-cloud-r3-conformance.md, STOP.
