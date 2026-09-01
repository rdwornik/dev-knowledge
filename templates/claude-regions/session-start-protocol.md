
1. `git status` — clean working tree?
2. `git log --oneline -5` — recent context
3. Read the **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves; same predicate as §1 item 3, so the two boot instructions select the same bundle — if continuing prior session
4. Check `BACKLOG.md` for in-progress items
5. `pytest --collect-only` — test discovery sanity check
6. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.
