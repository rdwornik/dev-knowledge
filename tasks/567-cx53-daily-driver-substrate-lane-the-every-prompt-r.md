---
id: "[#567]"
title: "CX53 daily-driver substrate lane — the every-prompt requirement, carried under `[#561]`"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#567] [P2][M] **CX53 daily-driver substrate lane — the every-prompt requirement, carried under `[#561]`** — Carrier lane under `[#561]`, born 2026-08-20 beside the accepted Codespaces LEAN v2 rather than against it. The two substrates are ruled **complementary, not competing**: **Codespaces free 4-core stays the parallel-burst substrate** (watched against the 30 h/month free ceiling, and never metered past it), and the CX53 is evaluated for the thing Codespaces structurally cannot be — **always-on operation with no hour metering**, which is what the operator's *every-prompt* requirement actually asks for. The LEAN's own framing is why this is a lane and not a purchase: **the commit-tax pain is already gone on Codespaces** (207 s to ~20 s), so the CX53's case rests on always-on and parallel lanes only, and the counterweight stands — **`devcontainer up` on a host we control has still never been executed** (lane J's D2 remains BLOCKED), and the ruling deliberately puts that discharge **before any Hetzner spend**. Shape: same `devcontainer.json`, VS Code Remote, `claude` on the box. · Done when: `devcontainer up` is executed on a host we control and the result recorded (discharging lane J's D2), the same devcontainer boots on a CX53 with `claude` reachable over VS Code Remote, and the every-prompt requirement is measured against it rather than asserted — with the Codespaces monthly burn recorded alongside, so the two substrates are compared on evidence · refs docs/audits/2026-08-20-technical-codespaces-audit.md, #561, #541, #554 · kill-candidates: none — `[#541]` owns the scale-out DECISION and `[#561]` the price-basis correction; this row is the daily-driver carrier and answers neither · serialize-group: architecture
