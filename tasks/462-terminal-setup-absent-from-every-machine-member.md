---
id: "[#462]"
title: "terminal-setup registered + the blind spot mechanized — membership_agreement reports declaration-vs-surface presence, so an absent member is no longer invisible"
status: closed
priority: P2
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
serialize-group: architecture
generates: BACKLOG.md
---

- [#462] [P2][S] **terminal-setup registered + the blind spot mechanized — CLOSED 2026-08-01 ([#383] wave 2)** — filed because `terminal-setup` was declared fleet by ADR-104 and VISION.md:111 while present in ZERO machine surfaces; found only because three consecutive nightly digests (N4/S3/S4) re-noticed it by hand. Structural cause, and the thing actually fixed: the [#382] census censused `registry.md` ITSELF, so a member missing FROM that registry was invisible BY CONSTRUCTION. **Done-when clause 1 met** — `terminal-setup` is in the member set via an `ecosystem/registry.md` row (existing surface, no new file, zero schema change), purpose distilled from the repo itself (2 commits, HEAD `d8a7b61`) and status stating plainly that it has no `VISION.md`/`CLAUDE.md`/deploy record rather than fabricating one. **Beyond the letter of the clause**, `audit.py::check_membership_agreement` (`ALL_CHECKS` 37→38) now diffs the ADR-104 declaration against all six repo-keyed surfaces and reports per-repo per-surface presence — RED-first witnessed (a perturbed `parity-surfaces.yaml` fired `fail` naming repo AND surface, reverted clean) — so the *class* of defect is machine-detected, not just this instance. **Ruled 2026-08-01 and deliberately NOT done:** no `deployed-versions.yaml` entry (its write-contract binds it to real deploys; forcing one fabricates deployment state for a never-deployed repo), so `terminal-setup` reports **declared-but-not-deployed at PASS** per ADR-109 §2/§8 — data, not a failure; `resolve_fleet_members` NOT widened (a named ADR-109 §2 ruling). Companion: the ADR-109 Related-line gloss "5 fleet repos" corrected by appended amendment — **9 governs**; the 5 is a loader artifact of the deployed-versions anchor. **RESIDUAL → [#472]:** the declaration is a code constant, so it can drift from ADR-104:15 silently; making it loadable is [#472]'s own Done-when and is not half-solved here. · Closed when: registry row landed + the census check armed and RED-tested · evidence 53ec1738 (check, RED-first), 50a18278 (registry row), 219424a6 (ADR-109 amendment) · refs ADR-104, ADR-109 §2, VISION.md, #383, #472 · serialize-group: architecture
