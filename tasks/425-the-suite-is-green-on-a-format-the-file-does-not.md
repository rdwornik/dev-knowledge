---
id: "[#425]"
title: "The suite is green on a format the file does not use"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#425] [P2][S] **The suite is green on a format the file does not use** — every `depends-on` fixture in `tests/test_validate_backlog.py` (`:196,:214,:219,:225,:230,:236,:242`) and `tests/test_validate_backlog_twin_parity.py` (`:78,:79,:81,:124`) writes the hashed `#NNN` form, the only form the parser accepts. The bare form the live file actually carries is exercised by no test, so [#424]'s four inert clauses sat undetected while the suite reported green. Generalizable class: **a fixture corpus samples the format its author intended, not the format the file contains** — a suite can be complete against its own examples and blind to production. Distinct from [#415], which is tests coupled to live MUTABLE content; this is coverage of the input space, not coupling to it. Scope: bounded audit of parser-facing fixtures, enumerate not fix. · Done when: parser-facing test corpora are audited for input-form coverage and each gap is closed with a negative-form fixture or recorded justified · refs tests/test_validate_backlog.py, #424, #415 · kill-candidates: none — [#415] owns live-content COUPLING, not input-form COVERAGE · serialize-group: audit-py
