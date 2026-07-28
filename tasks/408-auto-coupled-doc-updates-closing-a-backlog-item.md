---
id: "[#408]"
title: "Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOURNAL updates"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#408] [P2][M] **Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOURNAL updates** — closing a task should trigger (wired, not remembered) the coupled ARCHITECTURE update and JOURNAL entry. Evidence it is needed: ARCHITECTURE drift was found TWICE this arc, once the day AFTER a genuine re-read — memory alone does not hold it. [#403] is the mechanism seed (doc_claims extended to machine-derivable claims). Filing only, zero build. · Done when: closing a backlog item mechanically surfaces or blocks on the coupled ARCHITECTURE + JOURNAL updates (built on the [#403] seed), with a test, or recorded deferred-with-reason · refs #403, scripts/audit.py, ARCHITECTURE.md, JOURNAL.md · kill-candidates: #403 (if its doc_claims extension already discharges the coupling, fold in) · serialize-group: audit-py
