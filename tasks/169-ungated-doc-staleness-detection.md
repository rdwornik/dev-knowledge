---
id: "[#169]"
title: "Ungated-doc staleness detection"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
depends-on: "#171"
generates: BACKLOG.md
---

- [#169] [P3][M] Ungated-doc staleness detection (ADR-85 R2) — surface ARCHITECTURE/VISION/LESSONS/CONTRIBUTING staleness (e.g. untouched >N sessions while code changed) as a deterministic signal in the daily digest / conformance dashboard, NOT a per-session gate and NOT human memory; rides with the conformance-dashboard work. · Done when: a deterministic staleness signal for the four ADR-85-ungated docs lands in the digest/dashboard · refs docs/decisions/ADR-85-session-lifecycle-enforcement.md (R2), scripts/fleet_health.py, #166 · depends-on: #171 · DEFER — peg: #171 · **RE-PEGGED 2026-08-27** (X1 step 3, night-harvest governance session) — peg `#171` REDIRECTED. `[#171]` was ruled a **K3 RE-CUT** this session (split-and-close-the-shipped-half, never a bare delete), so the row this peg names is being narrowed to its unshipped remainder. The trigger is now that **remainder** — the leg-2 scope `[#171]` retains after the re-cut — not `[#171]` in its pre-re-cut form, whose scope `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` F1 found *unresolvable from the row* across three incompatible readings.
