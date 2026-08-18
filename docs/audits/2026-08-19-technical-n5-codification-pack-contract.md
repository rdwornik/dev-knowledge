# NIGHT N5 — CODIFICATION + DECISION-MEMO PACK · frozen contract of record · 2026-08-19

**FROZEN CONTRACT OF RECORD.** Saved verbatim as the FIRST COMMIT of the lane, before any
research or drafting work, per ADR-110 (contract-as-first-commit). Content arriving later in
the session is not load-bearing — a correction re-enters as a new contract, never as a
mid-flight message (`protocols/STANDING_RULINGS.md` D2).

- **Lane:** night N5 — codification + decision memos
- **Channel:** claude cloud (Anthropic cloud-session lane)
- **Branch:** `claude/night-n5-codification-memos-eyef8r`
- **Mode:** read-only + drafts. No PLAYBOOK edits, no scripts, no roster rows, no
  BACKLOG/`tasks/` writes, no rulings, no merge.
- **Output artifact:** `docs/audits/2026-08-19-technical-n5-codification-pack.md`

**Dating note (recorded, not a deviation of terms):** the session's `currentDate` is
2026-08-18; the contract names both artifacts `2026-08-19-*`. The contract's names are used
verbatim — a night lane dispatched against the next working day dates its artifacts to the day
the operator reads them, and the `validate-hermetization` Rule B check is shape-only
(`^\d{4}-\d{2}-\d{2}-` + closed class enum), so `2026-08-19-technical-…` is admitted on both
legs. No term of the contract is altered.

---

## Contract, verbatim

NIGHT N5 — CODIFICATION + DECISION-MEMO PACK · cloud, read-only + drafts
Night research lane, claude cloud channel. FIRST COMMIT = dispatch-stamp: this prompt as `docs/audits/2026-08-19-technical-n5-codification-pack-contract.md` on your `claude/*` branch. Drafts and memos only — no PLAYBOOK edits, no scripts, no rows, no BACKLOG/tasks writes. Sources you must read first: the batch-1 integrator packet (docs/audits/2026-08-18-technical-batch1-integrator-packet.md incl. its amendment), lane H's review artifact, and rows [#539] [#540] [#514].
ITEMS (CLEAR/BLOCKED each):

1. Dispatch-runbook codification draft for [#539]/[#540] + a PLAYBOOK Ch8 section draft. Must encode, from today's measured lessons: `claude --bg --worktree <slug>` prepends `worktree-` (doubled-prefix defect class); one-block batch dispatch with a branch-existence wait (config.lock race); board status ≠ completion (false-DONE precedent); harvest from git never transcripts; contract-as-first-commit (ADR-110); grammar check at PROVISIONING — [#514] leg 1's KIND_UNKNOWN block (2 of 8 batch-1 lanes reached the integrator off-grammar; quote the packet's §2). Draft as paste-ready fenced blocks.
2. Parallel-default decision memo ([#533]): should the audit-health hook flip to `--parallel`? Assemble the evidence: measured 1.41× serial-memoized end-to-end vs A's 4.28× parallel claim; A's byte-identical parity tests; risks (thread-safety surface, CHECK_ORDER emission, CI vs local variance); the acceptance evidence a flip ruling would require (e.g. N quiet parallel runs + parity on live tree). RECOMMEND one option; operator rules.
3. D8 decision memo (`.devcontainer` fleet_parity WARN, packet §A2): the two lawful routes (parity-surfaces.yaml hub role vs local .methodology.yaml) — consequences of each for the other 7 fleet repos, one recommendation, three lines max each.
4. Review-artifact linkage gap: `review_artifact_coverage` still WARNs on batch-1's own merges despite H's artifact existing — read the check, state what linkage it wants (naming? frontmatter? merge-message ref?), draft the row text that would close the gap.
5. Session-lessons sweep: from the packet + this chat's recorded rules, a deduplicated LESSONS candidate list (≤10, one line each) for the seat's promotion ruling — include the bc-absent-in-git-bash and job-tmp-lifetime items from Phase 0.

OUTPUT: `docs/audits/2026-08-19-technical-n5-codification-pack.md`. Commit, push, STOP packet (5 CLEAR/BLOCKED + shas). NOT: no PLAYBOOK/scripts edits, no rulings (memos recommend, the operator/architect rule), no merge.
