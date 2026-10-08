---
id: "[#1376]"
title: "Codespace model credentials for codex, grok and agy are loaded from the secrets folder, and the agy sign-in gap is closed or recorded"
status: superseded
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1376] [P2][M] **Codespace model credentials for codex, grok and agy are loaded from the secrets folder, and the agy sign-in gap is closed or recorded** - SUPERSEDED 2026-10-08 by [#1423]: its Done-when requires `CODEX_API_KEY` to be present, which R87 (subscription sign-in, never the API key) and R88 (Copilot by token, gemini retired, agy BLOCKED-AUTH) contradict -- seat ruling D5 in `to-browser/RATIFICATION-2026-10-08.md`. R78 (operator, 2026-10-04): load the credentials for codex, grok and agy from the operator's secrets folder into the account's Codespaces secrets, with device-login where a CLI needs it; values are not printed, logged, or written into a repository or transport file (R13); hardening comes later. Status 2026-10-04: `CODEX_API_KEY` and `XAI_API_KEY` are set and scoped to dev-knowledge; claude, gh and rclone were already set; agy needs a Google sign-in per Codespace, which keeps agy from being autonomous and is an open gap. · Done when: a preflight lists the Codespaces secret NAMES present for codex, grok and agy (never values) and, for a missing one, prints the exact OPERATOR-ACTION; `CODEX_API_KEY` and `XAI_API_KEY` appear in that list for this repository; the agy leg either passes a non-interactive read that returns a nonce in a fresh Codespace, or the batch records `agy: interactive sign-in required per Codespace` as an OPERATOR-ACTION; a grep of the run's receipts and logs for any secret value returns nothing · owner: the operator for the secrets themselves; lane `b2-codespace-1to1` (W1-7) for the preflight and the agy measurement · touches: `scripts/codespace_parity.py` (credential leg), the provisioning script, tests · kill-candidates: `[#772]` -- every dispatched lane inherits the whole secret store; hardening is that row, loading is this one · refs `[#772]`, `[#627]`, `scripts/codespace_parity.py`, `protocols/STANDING_RULINGS.md` section AR (R78) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R78 in `to-browser/RATIFICATION-2026-10-04.md R78`
