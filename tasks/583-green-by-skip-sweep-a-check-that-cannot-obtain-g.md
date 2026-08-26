---
id: "[#583]"
title: "Green-by-skip sweep — a check that cannot obtain ground truth must not report OK (packet ARC-E, C18)"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#583] [P2][M] **Green-by-skip sweep — a check that cannot obtain ground truth must not report OK (packet ARC-E, C18)** — A check that cannot obtain ground truth currently reports OK, which is green-looking evidence for an organ that never evaluated anything — the skip half of the C18 ADOPT. · Full body as born (nothing deleted, relocated for D-2): `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: the frozen sweep artifact is consumed row by row, `validate_doc_claims` no longer prints OK while a leg reports `<ground truth unavailable>`, the `cmd_checks` cp1252 crash is fixed fail-loud rather than worked around in prose, and every remaining silent-skip site either fails loud or carries a declared reason · refs docs/audits/2026-08-25-technical-register-ruling-packet.md §3 ARC-E, protocols/STANDING_RULINGS.md section U, docs/audits/2026-08-25-technical-green-by-skip-sweep.md, scripts/validate_doc_claims.py, scripts/audit.py · source: packet row C18 (ARC-E), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — `[#153]` asks which RULES lack an organ; this row asks whether a LIVE organ silently declines to evaluate · serialize-group: gates
