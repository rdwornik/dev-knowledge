---
id: "[#512]"
title: "`gen_handoff.py`'s open-batch refusal doesn't scrub `GIT_DIR`"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#512] [P2][S] **`gen_handoff.py`'s open-batch refusal doesn't scrub `GIT_DIR`** — PRE-2 retroactive terra (HIGH, `gen_handoff.py:403`): `_open_batches()` delegates to `batch_manifest.open_batches()`, whose `_git()` (`batch_manifest.py:140`) runs `subprocess.run` with no `env=` scrub, so an inherited `GIT_DIR` redirects the read and the reader silently returns no open batches — an immutable handoff could be cut mid-batch, the wrong-repo failure `gen_handoff.py`'s own scrub (lines 181-272, #355/RM-8) guards against elsewhere. **Not a duplicate of [#396]** (DRY-consolidates a scrub that already exists in 3 places); this is a 4th call site with none at all. · Done when: `batch_manifest._git()` scrubs the same GIT_* vars as `gen_handoff.py`'s own reads, with a regression test asserting an inherited `GIT_DIR` doesn't suppress a real open batch · refs `scripts/batch_manifest.py:140`, `scripts/gen_handoff.py:181-272,403`, `docs/audits/2026-08-07-codex-pre-cut-retro-handoff-engine-thinning.md`, [#396], [#355] · kill-candidates: none — [#396] DRY-consolidates an EXISTING scrub, not this MISSING one · serialize-group: gates
