---
id: "[#593]"
title: "Codespaces chain repair, hub half — uv in the image and a prebuild that actually refreshes"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#593] [P2][M] **Codespaces chain repair, hub half — uv in the image and a prebuild that actually refreshes** — Smoke 5 failed on three independently fatal defects; two are the hub's. `uv` is absent from the container, so no hub gate can run there (every gate is `uv run --locked` by ADR-106); and the prebuilt image served a clone stale by three days while `git status -sb` reported no divergence, so the very merge declaring the Claude Code install was missing. · Done when: smoke run 6 returns `Ok=True` AND `RemoteExitCode=0` AND the receipt's HEAD equals the pushed HEAD — all three, since any one alone has previously passed while the transport was broken; `uv` resolves on PATH inside the container at the pinned version; and the copy-leg defect is either fixed or explicitly recorded as the operator-side half this row does not own · refs docs/intake/2026-08-26-tech-dispatch-consolidation-remainder.md (intake #52), docs/audits/2026-08-26-verification-batch-1-close-packet.md section 11, .devcontainer/devcontainer.json, .devcontainer/provision.sh, ADR-106, #554 · source: intake #52 (I4) + close packet section 11 — the D1 evidence · kill-candidates: none — `[#554]` BUILT the devcontainer; this row repairs the chain that proved it non-functional, and killing it would delete the substrate
