# CONTRACT-W2B — Lane b conversions · worktree `worktree-lane-b-210-conversions`

**Committed verbatim from the operator's frozen `~/Downloads/CONTRACT-W2B.md` (I-D3, step 0).**
Batch-6 (phase-2) manifest: `docs/audits/2026-08-16-technical-batch-6-manifest.md` roster row
**b** — rows `#210 #285 #361`, bucket finish-line, contract of record `CONTRACT-W2B.md`.

## §C · CONTRACTS (12 + 1 optional) — ex-ante buckets: finish-line/feature = a–i(+k), hub-introspection = x,y,l (3 of 3 at width 12)

COMMON (applies to every lane, verbatim law): auto mode; own worktree/branch only; `uv sync
--locked --group analytics` first; PYTHONUTF8=1 on console errors; T_start = packet line 1; step 0
commits contract-of-record + prints OWNED-FILES manifest; edit nothing outside it (regen surfaces
excluded); tasks/ edits at SOURCE then `gen_task_tree.py --emit-source`; targeted tests only (full
suite = integration, once); no merges, no pushes to main, no births, no register edits unless the
contract names them; decision budget: STOP only for curated-baseline touch, rule-vs-ruling
conflict, or unruled fork — else decide-and-report in ONE packet; commit-and-STOP.

## LANE b — CONTRACT-W2B.md · worktree `worktree-lane-b-210-conversions`

Ids #210 #285 #361. Same procedure. OWNED-FILES: 3 tasks files.

---

## Step 0 verification (live, this session)

Worktree letter `b` matches the batch-6 manifest roster row exactly (`worktree-lane-b-210-
conversions`, ids `#210 #285 #361`) — `git worktree list` confirms this checkout plus 11 sibling
lanes (a c d e f g h i k m x), none colliding on letter `b`. Branch
`worktree-worktree-lane-b-210-conversions`, tree clean at boot on top of main tip `43cd1cee`,
which is also the tip every sibling worktree carries — no lane has yet advanced past Position-0.

"Same procedure" resolves against the sibling `worktree-lane-*-conversions` lanes (a/c/d/e/f/g):
this is a Done-when-conversion lane per the `[#425]`/`[#387]`/`[#338]`/`[#112]` W4a–d precedent —
apply the reviewed drafts in `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` to
this lane's 3 owned `tasks/*.md` source files (§3 `[#210]`, §4 `[#285]` group-A / `[#361]` group-B
of that artifact), none of which carries an AMBIGUITY flag (§5 lists only `[#391]`, not owned
here). OWNED-FILES resolved to: `tasks/210-convert-journal-wrap-no-ff-warns-from-per-instan.md`,
`tasks/285-extend-hub-freshness-gating-to-playbook.md`,
`tasks/361-adr-immutability-s-real-coverage-is-declared-onl.md` (BACKLOG.md regen via
`gen_task_tree.py --emit-source` + audit-index regen are the named-excluded regen surfaces).

Env: `.claude/settings.local.json` and 5 `ecosystem/*/state.yaml` already present in this
worktree (pre-seeded); `uv sync --locked --group analytics` run clean this session (5 packages:
numpy/pandas/python-dateutil/six/tzdata installed, 34 resolved).

Draft premises re-verified live before applying (per the draft's own "verified live at drafting"
claims, re-checked rather than trusted): `_HUB_ONLY_FRESHNESS_FILES` in `scripts/audit.py:294-295`
holds exactly `[SESSION_SETUP, AI_COUNCIL_PROCESS, DEFINITION_OF_DONE]` — PLAYBOOK absent, and
`_FRESHNESS_FILES` (`:296`) is the composed list, confirming `[#285]`'s draft correction that the
row's own constant name was wrong. `scripts/hooks/block_immutable_edits.py:9,83` still scopes the
guard to `docs/decisions/transcripts/**` only, confirming `[#361]`'s draft. `ecosystem/disposition-
register.yaml` carries exactly 3 journal-wrap-class entries (`warn-no-ff-3a894eeb5-journal-wrap`,
`warn-no-ff-d0f9ead67-transcript-archive`, `warn-no-ff-533109f-journal-wrap`, the last one's
reason text stating "RECURRENCE: 3 instances... tracked for a standing path-scoped rule by
[#210]"), confirming `[#210]`'s draft count.
