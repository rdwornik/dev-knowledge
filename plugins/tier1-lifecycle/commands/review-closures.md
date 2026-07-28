---
name: review-closures
description: Review the session-end closure proposals and execute ONLY operator-approved closures (ADR-70 Tier-1)
---

The review half of the ADR-70 Tier-1 closure loop. The plugin's Stop hook
(`propose_closures.py`) writes `<host-repo>/logs/PROPOSALS-<date>.md`; this command
surfaces it, takes the operator's explicit approval, and executes **only**
approved closures via done-items-leave (ADR-65).

This is a **plugin** command — the gate scripts live under `${CLAUDE_PLUGIN_ROOT}`
and operate on the **host repo** (`$CLAUDE_PROJECT_DIR`, where this command runs).
Run them exactly as written below (with the `${CLAUDE_PLUGIN_ROOT}` prefix).

**Safety contract — read before acting:**
- Close ONLY what the operator explicitly approves in THIS run. No approval →
  close nothing.
- STRONG candidates may be approved together with a single `y`. WEAK candidates
  require the operator to type each `#N` individually — **never bulk-approve WEAK**.
- The gate (`review_closures.py plan`) re-verifies every approved id
  (currently open; STRONG evidence commit still exists) — trust its verdict over
  the proposals file, which may be stale.
- You perform the BACKLOG edit (the script is read-only); use the **exact** `line`
  the gate returns as the Edit `old_string` so the removal is exact-match.

## Steps

1. **Find the proposals.** Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/review_closures.py" surface`.
   If it prints nothing, tell the operator "no closures proposed" and stop. Otherwise
   read the latest `logs/PROPOSALS-<date>.md` in the host repo.

2. **Present for approval.** Show the operator, grouped:
   - **STRONG** — each `#N`, its task summary, and the `closes [#N]` evidence SHA.
     Offer: reply `y` to approve all strong, or list the specific `#N` to approve.
   - **WEAK** — each `#N`, its summary, and the changed-file evidence. Ask the
     operator to type each `#N` they want to close (no bulk approve).
   Then **wait for the operator's response.** If they skip / decline / say nothing
   actionable → close nothing, report, stop.

3. **Plan (re-verify).** Collect the approved ids into a comma list and run:
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/review_closures.py" plan --ids <approved>`
   It prints JSON `{"close": [{id,tier,evidence,line}], "skip": [{id,reason}]}`.
   Report every `skip` (with reason) to the operator — these are NOT closed.

4. **Execute done-items-leave** for each item in `close`. **Which edit is correct
   depends on the host's backlog shape — check it first**, because in a
   source-of-truth host the direct edit is silently undone:

   **First, decide the shape.** If `tasks/manifest.json` exists, the host has flipped
   (hub, ADR-107 step 3 / [#439]): `tasks/` is the SOURCE and `BACKLOG.md` is
   GENERATED. Otherwise the host is unflipped and `BACKLOG.md` is the source.

   - **(a) UNFLIPPED host — `BACKLOG.md` is the source.** Edit `BACKLOG.md`:
     `old_string` = the gate's exact `line` (plus its trailing newline),
     `new_string` = empty — removes that one task line. If the Edit fails to match,
     STOP and report (do not retry loosely).

   - **(b) FLIPPED host — `tasks/` is the source.** Do **NOT** edit `BACKLOG.md`: it
     is generated, so the coherence gate REDs the edit and the next regen restores
     the line. Instead **retire the task**:
     1. Remove the task's node (`{"task": N, "file": ...}`) from `tasks/manifest.json`.
     2. **LEAVE the task file in place** — it stays as the allocation record that
        keeps its id from being re-issued (ADR-107 §6.3, retire-not-delete). Do not
        delete it, and do not use `--prune` (it is refused).
     3. Regenerate: `python scripts/gen_task_tree.py --emit-source`. The row leaves
        `BACKLOG.md` as a result, not as a separate edit.

   Never renumber in either shape; the id gap stays.
   - After all approved removals, validate the host backlog if the host ships a
     validator (e.g. `python scripts/validate_backlog.py`); on a flipped host also
     run `python scripts/gen_task_tree.py --check`. Otherwise re-run the plugin gate
     `surface` to confirm the closed ids no longer appear.

5. **Record + commit (ADR-65).**
   - Prepend a JOURNAL entry: which `#N` closed, by what evidence SHA, that the
     operator approved it (business record; the session ritual carries it).
   - Commit (PowerShell here-string or `git commit -F`, per the channel-discipline
     LESSON) with `closes [#N]` for every removed id + the evidence SHA(s) in the
     body. The `backlog-id-on-close` commit-msg hook enforces the id reference.

6. **Report:** closed (with evidence), skipped (with reason), untouched/unapproved.

**Never** close an unapproved id, never bulk-approve WEAK, never edit BACKLOG
without the gate's `close` verdict + exact line.
