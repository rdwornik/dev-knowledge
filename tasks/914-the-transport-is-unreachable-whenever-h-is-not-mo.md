---
id: "[#914]"
title: "The transport is unreachable whenever H: is not mounted -- a post-hook must deliver to-browser artifacts regardless of mount, and refuse loudly instead of reporting success after writing to Downloads"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#914] [P1][M] **The transport is unreachable whenever H: is not mounted -- a post-hook must deliver to-browser artifacts regardless of mount, and refuse loudly instead of reporting success after writing to Downloads** - The operator channel is `H:\My Drive\CLAUDE PROMPT DIR\{to-cc,to-browser}`, a Google Drive mount. On 2026-09-19 the night-wave-2 integrator seat ran with only `C:` mounted. `CLAUDE_PROMPTS_DIR` resolved to `H:\...` and the drive did not exist. The seat could read neither the 05:20 integrator report nor any lane handback, and wrote its own report and the L3 handback to `C:\Users\1028120\Downloads\to-browser\` instead. **Three sessions that day rebuilt state from git and lane transcripts** because they could not read prior reports. The fallback write is the worst part: a seat that writes to Downloads and says "delivered" reports success to a channel the operator does not read (the same shape as memory `prompts-dir-has-two-live-values`, and defect E-29) · Done when: a post-hook (or the one delivery organ every seat calls) delivers each `to-browser` artifact to the operator channel when H: is mounted, and otherwise queues it durably and delivers it on the next mount; while undelivered it REFUSES loudly (non-zero exit, a line naming the artifact and the missing mount), never a success line; a RED-first test covers the unmounted case; and the two artifacts from 2026-09-19 (`INTEGRATOR-wave2-pass2-2026-09-19.md`, `HANDBACK-wave2-dispatch-2026-09-19.md`) reach the channel · refs `C:\Users\1028120\Downloads\to-browser\`, memory `prompts-dir-has-two-live-values`, memory `gdrive-file-visible-before-bytes-land`, `[#509]` · kill-candidates: [#509] -- `Invoke-Dispatch.ps1` resolving `CLAUDE_PROMPTS_DIR` is the read side of the same channel; if one delivery organ owns resolution, #509 folds into it
