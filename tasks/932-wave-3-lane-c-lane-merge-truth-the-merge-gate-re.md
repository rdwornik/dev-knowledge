---
id: "[#932]"
title: "Wave 3 lane C (lane-merge-truth) -- the merge gate reads the right lane, and the census counts real callers"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#932] [P1][M] **Wave 3 lane C (lane-merge-truth) -- the merge gate reads the right lane, and the census counts real callers** - filed by LANE-W3-A per `to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md` hard precondition 2 (every wave row is filed before any other wave-3 lane fires); frozen contract `LANE-W3-C-merge-truth.md`, branch `worktree-lane-merge-truth`, a lane of the loop `[#929]` evaluated. Value: Three truths the merge currently gets wrong. The ordered-vs-used model check reads the integrator's own transcript instead of the lane's, so it would refuse every real merge. The organ census calls 162 organs uncalled when 126 are called by pre-commit or the conductor, so its one real signal is buried. And nothing reads the operator's GO. After this lane each of the three answers truthfully. · Done when: carried verbatim from the frozen contract — 1. **`merge_receipt.py models` defaults `--worktree`** to `.claude/worktrees/<slug>` when that directory exists (R-W3-5); an explicit flag still wins. 2. **The organ-truth check counts real callers** (R-W3-4): an organ invoked by an armed or dated manual pre-commit hook, or by a conductor job, is declared; the check fails only on organs with no caller anywhere, and names each. It reads those surfaces from their own config files. 3. **`scripts/go_reader.py`** answers one question for a batch — is there a GO file `to-cc/GO-<batch>.md` — and exits non-zero with a receipt when there is not (R-W3-7). It reads; it writes no GO. 4. **Tests (common rules 1-4):** the declared `merge_receipt.models` row, read from `harness.yaml` and run as written against a fixture lane worktree, compares the lane's transcript, not the caller's; an organ called only by a manual-with-date hook is declared; an organ with no caller fails and is named; a missing GO file is a refusal, a present one a pass. 5. **Codex terra review** recorded; **handback** per common rules. · refs `to-cc/WAVE3-COMMON-2026-09-21.md`, `to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md`, `[#929]` · kill-candidates: none -- each wave-3 lane wires an organ that already exists; no open row is absorbed
