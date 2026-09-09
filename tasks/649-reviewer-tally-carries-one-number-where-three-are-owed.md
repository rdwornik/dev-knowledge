---
id: "[#649]"
title: "The reviewer tally carries one HIGH number where the ruling requires three"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#649] [P2][S] **The reviewer tally carries one HIGH number where the ruling requires three** — the first sitting ruled that `HIGH = 0` means UNRESOLVED, not RAW, because a raw-zero gate rewards a reviewer for not reporting: lane V-6 reported seven terra HIGHs found and fixed, and under a raw bar that lane looks worse than one that found nothing. The tally line must therefore carry `HIGH raw=N fixed=N unresolved=0`, and a tally with a single number is `review=NONE`. V-6's landed `reviewer-mismatch` refusal compares the model id only — it does not read the HIGH counts at all — so the format half of the ruling is unbuilt · Done when: the seat templates emit the three-part HIGH line, a refusal reads a one-number tally as `review=NONE` with a trip-test behind it, and the integrator's per-merge check reads the same predicate the templates write · refs DECLARE-SITTING ruling 2, `scripts/seat_refusals.py`, `templates/handoff/seats/`, `[#642]` · source: DECLARE-SITTING ruling 2, filed by batch V lane V-4
