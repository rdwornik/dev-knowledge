---
id: "[#363]"
title: "`codex-review` routed a CODE-shaped diff through the `gpt-5.6-sol` lane, not terra"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#363] [P2][S] **`codex-review` routed a CODE-shaped diff through the `gpt-5.6-sol` lane, not terra** — live observation, this lane is the evidence. The standing instruction was "terra reviews the diff pre-merge"; the wrapper's terra pin applies to the **doc lane** only ([#333]), so a code-shaped diff inherits the code lane's config default. **Impact:** a Codex review demonstrably ran and its 2 HIGH findings were real, yet the standing "terra before merge" rule was **not actually satisfied** — a rule can be observed as followed while being unmet, the same recorded-vs-enforced gap ARC-5 tracks. Binds to [#333] and [#341]. · Done when: lane selection is explicit at invocation (or the doctrine is reconciled to the wrapper), and the invoked model is reported by name in the review artifact · refs #333, #341, docs/audits/2026-07-19-codex-residual-completeness-gate.md, PLAYBOOK §16 · kill-candidates: none — a routing defect neither #333 nor #341 covers; both are its parents · serialize-group: codex-review
