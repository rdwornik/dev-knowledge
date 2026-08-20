# FINAL INTEGRATOR — WINDOW CLOSE CONSOLIDATION (2026-08-20)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**PRIMARY checkout, serial, ONE pass, END PACKET at the end. Operator gate = ONE PAUSE before
push.** ADR-110: commit this prompt first as
`docs/audits/2026-08-20-technical-final-integrator-contract.md`.

## QUEUE (strict order)
1. **Origin verification first:** `git fetch --prune`; confirm the hygiene-docrot and
   playbook-status artifacts exist on origin/main (find them under docs/audits/ by date-slug;
   report exact paths). Enumerate ALL origin branches — this is the BEFORE census.
2. **Merge queue, serial `--no-ff`, inspect-before-merge each:**
   a. `worktree-flip-parallel` (2 commits; contract already verified — merge, lane id in msg).
   b. `worktree-night-ab-gemini-2` — read its artifact from the branch BEFORE merging; extract
      VERBATIM into your END PACKET: the substitution-probe outcome (which CLI, which model
      honoured/refused), the per-item result table if the 14 items ran, computed G2/G3, raw
      C1-N1/C1-N2 outputs, and any wall it hit. Merge if its frozen contract is satisfied;
      REFUSE with file:line evidence if not (a lane that stopped honestly at a wall MERGES —
      its artifact is the deliverable).
   c. `worktree-ab-grok46-2` — same extraction: P0 version-probe evidence (served model string
      verbatim), result table, G2/G3, N1/N2 raws, USD spend line. Same merge-or-refuse rule.
   NO admission verdicts anywhere — the architect rules from your packet.
3. **Land the Codespaces audit into the repo:** copy
   `C:\Users\1028120\Downloads\CODESPACES-AUDIT-2026-08-20.md` to
   `docs/audits/2026-08-20-technical-codespaces-audit.md`, commit (its RULING block rides in).
4. **Regenerate ONCE:** audits index, then the dashboard (`python scripts/gen_dashboard.py`,
   markdown + HTML) so Section 0 and the theme boards reflect every landing of the day.
5. **Full targeted suite once** on the merged result (`-m "not slow" -n auto`); triage any RED
   honestly (owned vs pre-existing, with evidence).
6. **TEARDOWN, complete:** remove ALL worktrees except primary (`git worktree list` must show
   primary only at the end), prune; delete local merged branches with `-d`; force-delete ONLY
   known dead remnants (`worktree-ab-grok46` first attempt, `worktree-night-ab-gemini` first
   attempt) after logging their unmerged commits for the record. Origin: delete merged
   `claude/*` and any lane branches AFTER the push succeeds (push-before-delete standing
   order); `automation/fleet-audit` NEVER touched. Report the AFTER census (branches +
   worktrees, local + origin).
7. **PAUSE before push:** print the pre-push summary (merged/refused per lane, suite verdict,
   WARN delta, dashboard path) and WAIT for the operator's GO in this session. After GO: push,
   then execute the origin deletions, then the END PACKET.

## END PACKET (the consolidation the operator asked for — human-readable)
Per lane: merged/refused + shas · the two A/B extractions verbatim (Gemini, Grok) · ledger
line (closures/births/live) · WARN delta · **"WHERE TO LOOK" section for the operator:
dashboard HTML path (task counts, per-theme status, priorities, release notes), the four key
audits by path (codespaces, playbook-status, c-lanes digest, gemini/grok results)** · teardown
census before/after · pending items with owners (Ch8 codification, provider-config lane,
step-0 ceiling test, ssh BOM).

## NOT
No rulings, no births, no closures beyond what merges mechanically carry, no JOURNAL beyond
your own merge anchors, no touching ~/.gemini or ~/.ssh, no SKIP without a declared reason in
the commit body.
