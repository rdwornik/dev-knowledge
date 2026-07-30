# [#446] §B(b) — Rulings on the 7 OPEN questions
date: 2026-07-31 · status: RULED (R4: CONFIRMED <number> by operator, 2026-07-31) · inputs: sol draft OPEN blocks (canon source) + W1 dossier cards (INPUT-NOT-AUTHORITY)

R1 — command name: /handoff-verify, a separate command. Not a /handoff flag: the generator stays answer-free, the checker answer-producing; coupling them reopens the ferry/proof boundary the anti-bluff contract protects. /boot stays archived. Build note: re-verify the .claude/commands inventory live before wiring.

R2 — P0a/P0b/P0c: adopt the intake definitions pinned at 2026-07-27-tech-handoff-process-v6-proposal.md:110-112 with terra-H3 narrowing. P0a carries a SECOND assertion: gen_task_tree --check passes (currency), alongside the ratified content assertion — BACKLOG.md is generated post-[#436], and a probe that can PASS on stale generated content is bluffable. Locator drift at build = re-pin here, never adjust in code.

R3 — P3 comparison: Option A. P3 compares `git branch --show-current` against the Destination row's branch field; mismatch = FAIL. Write-scope and MODE stay prose, outside P3 — no probe leg without a mechanical counterpart; a leg that cannot fail honestly discredits the block.

R4 — byte budget: <number> bytes on protocols/HANDOFF_BOOT.md, mechanically enforced; A10 closes against this number only. The per-bundle session header is NOT governed by A10.

R5 — RM-8: Option D. Target: any bundle directory containing git-tracked files, guarded at the creation site (gen_handoff.py:436; exist_ok=True removed). Default REFUSE with a diagnostic naming the colliding directory and the escape hatch; --allow-suffix is explicit opt-in. Silent suffixing converts today's collision into tomorrow's _select_active_bundle ambiguous-FAIL.

R6 — repo_root/cross_repo: codify the existing semantics — verify(bundle_path, repo_root=None, cross_repo=False), :444 default call intact. CLI: --repo-root PATH, --cross-repo; --cross-repo without --repo-root is a HARD ERROR. No silent root inference — that reproduces the original false-FAIL class.

R7 — [#421] absorption: Option B, both variants fixed inside the [#446] leg: (v1) _FILE_RE :54 dot-in-final-segment so repo-root dotfiles bind; (v2) header_tokens :131-133 bare-# so backticked #421 does not tokenize. Each variant gets a RED-first pytest in the frozen set; absorption acceptance = both tests green + [#421] closed pointing at them. Fallback C is permitted ONLY if terra review rules v1 outside [#446]'s file scope — and then the new owning row must exist BEFORE [#421] closes (the [#447] closure-polarity lesson, applied forward).

## Amendments

A1 (2026-07-31): R4 resolved — 18,000 bytes on protocols/HANDOFF_BOOT.md, mechanically enforced; A10 closes against this number only. RULED architect technical lane. The per-bundle session header is NOT governed by A10.
