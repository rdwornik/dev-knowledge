---
id: "[#357]"
title: "Silent-rule census run 2"
status: open
priority: P2
size: M
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#357] [P2][M] **Silent-rule census run 2** — sweep `docs/decisions/` under the [E8] declaration test, completing the denominator. Run 1 (pinned `bf49cbf9`) scoped `protocols/` + `templates/` + `ecosystem/*.yaml` and measured N_silent 176 of 320; ADRs were deferred, so that figure is a floor. Same method: mechanical MUST-token pass, then judgment on the residue, with mechanism lookups keyed on the rule's SUBJECT and never on an ADR number (ADR-69's mechanism is `discover_repos` at `scripts/audit.py:363`, carrying no ADR ref). Excludes the pending-#242 cluster, which [#362] owns. · Done when: `docs/decisions/` is swept, every ADR-borne MUST-rule carries a state, and a combined denominator + N_silent supersedes the [E8] baseline · refs [E8] baseline, #242, #362, scripts/audit.py · kill-candidates: none — completes the measurement [E8] closure clause (a) requires; no open task covers the ADR corpus · serialize-group: audit-py
