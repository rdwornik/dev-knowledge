---
id: "[#1445]"
title: "Every dated item -- a known-reds expiry, a manual_until fate, a hook expiry -- warns at least 3 days before its date"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1445] [P1][S] **Every dated item -- a known-reds expiry, a manual_until fate, a hook expiry -- warns at least 3 days before its date** - The 40 `[#912]` entries of `logs/KNOWN-REDS-REGISTRY.json` expired on 2026-10-08 and made `known_reds.py compare` exit 2 ("40 problem(s)") on both OS with no warning first; the B2-W2 render (2026-10-09) counts the next cliffs: registry expiries on 2026-10-16 (the 40, re-dated by seat ruling S-1), 2026-10-17 (9 members, 9 ubuntu, 11 windows) and 2026-10-19 (`[#1350]`), `ecosystem/harness.yaml` fates `transport.py` `manual_until: 2026-10-15` and `transport_lint.py` `manual_until: 2026-10-19`, and three `.claude/settings.json` expiries already past (2026-10-08) · Done when: (1) one command lists every dated item of the registry, `harness.yaml` fates and `.claude/settings.json` with its date, owner and days left, generated from those files, never typed; (2) an item <= 3 days from its date is reported at session start and at batch close as a WARN naming its owner, and a past one as a FAIL; (3) RED-first: a fixture registry entry 2 days from expiry yields no warning on `03d21ff8` and a WARN after the change · kill-candidates: none -- `known_reds.py` refuses an expired entry only after the date (`scripts/known_reds.py:265`) and no organ looks ahead (`git grep -n -i "days left" origin/main -- scripts` = 0) · refs `scripts/known_reds.py`, `logs/KNOWN-REDS-REGISTRY.json`, `ecosystem/harness.yaml`, `.claude/settings.json` · source: `to-cc/BATCH-B2-W2-2026-10-09.md` §1 step 5; the plan's S1b (`to-browser/QUESTION-session-plan-tech-architect-44-2026-10-09.md` §1) · evidence (ADR-111 §1 (a), attached 2026-10-10 by the B2-W3 render under seat ruling S-39): `to-browser/DIGEST-SESSION-REVIEW-B2-W2-2026-10-10.md` §4 F9 (21 organs past `manual_until`; three lapsed disabled-hook expiries in `.claude/settings.json` — `to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` §0 items 4, 5)
