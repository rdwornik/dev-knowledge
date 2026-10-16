---
id: "[#1552]"
title: "Every Codespace credential has a recorded class, issuer, expiry policy and renewal act, checked at creation"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1552] [P2][M] **Every Codespace credential has a recorded class, issuer, expiry policy and renewal act, checked at creation** - UC5 spec item 2. Claude, codex, copilot and gh seed with no operator step (LANE-END-codespace-finish-2026-10-14 step 2 PASS), but no lifetime is recorded, the codex refresh path was never witnessed, and a `CODEX_API_KEY` user secret exists against R87. Lifetime sources, to be re-read against official docs in the RED step: OpenAI documents copying `~/.codex/auth.json` and refresh during use (developers.openai.com/codex/auth); the claude setup token is reported as about one year by third-party guides only · Done when: RED first: (1) each provider in `ecosystem/provider-registry.yaml` gains a credential block (class, issuer, expiry policy, renewal act, operator step yes/no) holding no secret value and no secret location; (2) `codespace-exec` reads it at creation and refuses a credential past its expiry, warning 30 days ahead with the renewal act printed; (3) the per-CLI probe is read-only: a nonce call for each model CLI, `gh auth status`, `rclone lsd` on the transport root; (4) a check lists Codespaces secret NAMES only and prints OPERATOR-ACTION for any `*_API_KEY` (R87), the deletion staying the operator's act; (5) a leak check proves no token material in any receipt · touches: `ecosystem/provider-registry.yaml`, `scripts/dispatch.py`, `scripts/codespace_parity.py`, tests · kill-candidates: none -- `[#1376]` is already superseded and `[#1537]` owns agy's sign-in · refs `[#1537]`, `[#1423]`, `[#1376]`, `docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md` · source: `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md` §2 item 2; `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md`
