# MORNING CONSOLIDATION — NIGHT BATCH N1–N5 (2026-08-19): HARVEST + LAND + VERIFY + REPORT

> **Contract of record** (ADR-110). Saved verbatim from the operator prompt and committed
> BEFORE any harvest, merge, or report work, per the contract's own instruction.
> Executing seat: primary checkout on `main`, sole writer. Baseline tip `87dd41af`.

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**You run on the PRIMARY checkout on `main` and are the sole writer** (verify: tree clean, no
other active session, `main == origin/main`, expected tip 87dd41af or newer — if newer, report
the delta shas and proceed from live). **You land and verify the night; you rule NOTHING** — no
ratification, no births, no closures, no PLAYBOOK edits, no execution of any spec the night
drafted. The architect adjudicates from your report.
**ADR-110:** save this prompt as
`docs/audits/2026-08-19-technical-morning-consolidation-contract.md`, COMMIT first.

## STEP 1 — NIGHT CENSUS (no invention for absent lanes — the NB7 lesson)
Expected lanes and their dispatch-stamp files (each was contracted to commit its stamp FIRST):
N1 `…n1-wiring-spec-contract.md` · N2 `…n2-seam-worksheet-contract.md` · N3
`…n3-ratification-pack-contract.md` · N4 `…n4-grooming-wave1-contract.md` · N5
`…n5-codification-pack-contract.md`.
Against a LIVE `git ls-remote --heads origin` (never a stale remote-tracking read) plus local
refs, classify each lane: **LANDED** (stamp + output artifact on a `claude/*` branch) ·
**STAMPED-BUT-DIED** (stamp only) · **NEVER-DISPATCHED** (no ref anywhere). Record the
classification with ref evidence. Absent lanes get stated absence — never a CC-derived
substitute unless this contract's report step explicitly labels one as such.

## STEP 2 — MERGE QUEUE (LANDED lanes only, serial, --no-ff, order N1→N5)
Pre-merge check per branch: **docs-only diff** (`git diff main...<branch> --name-only` must
touch only `docs/audits/**`). A night branch mutating anything else (scripts/, tasks/,
BACKLOG.md, .devcontainer/, configs) → **STOP for that branch, do not merge it, report** —
night lanes were contracted read-only+drafts. The only lawful conflict is the audits index:
resolve by regeneration (`gen_audit_index.py --write`), never by picking a side.
Per merged artifact: verify **section-completeness** against its contract's named items (every
item has its CLEAR/BLOCKED line; N4 additionally: whole-themes rule honored, top-15 table
present; N3: kernel-row draft present, ledger arithmetic present). Incomplete → merge it as-is
but flag the gap explicitly in the report; never fill it in yourself.

## STEP 3 — LAND + SANITY
Audits index regen · JOURNAL one entry for the night, every anchor SHA on ONE line · targeted
sanity (docs-only batch): `gen_task_tree --check`, `validate_backlog`, one `audit.py health`
(cloud commits may have been made with gates unavailable — the local re-run is the proof that
counts) · push `main`; both pre-push gates must pass.

## STEP 4 — TWO OPERATOR FILES (write to `C:\Users\1028120\Downloads\`)
**`MORNING-REPORT-2026-08-19.md`** — the architect's adjudication queue, digest not restatement:
1. Night census table (5 lanes × classification × shas).
2. N4 digest: per-theme class counts + the TOP-15 DEAD-CANDIDATE table **verbatim** + MALFORMED
   count — the day's closure shortlist.
3. N3 digest: per-intake one-liner (ADR? rows? deferral?) + the pack's ledger arithmetic +
   kernel-row draft location.
4. N5 digest: the three decision memos (parallel-flip, D8, review-linkage) each compressed to
   recommendation + one-line basis, with pointers into the artifact; LESSONS candidate count.
5. N1/N2 readiness verdict each: is the spec/worksheet complete enough to author tomorrow's
   lane contract from it — YES / gaps listed.
6. Numbered adjudication queue: every decision the architect must make, in recommended order.
**`POST-NIGHT-DELTA-2026-08-19.md`** — what moved on `main` since 87dd41af (grouped commits,
in/after classification), current ship-gate composition, anything degraded, open operator
decisions carried (D8; parallel-flip; #554 D1/D2 proof).

## STOP CONDITIONS
Non-docs diff on a night branch · artifact-vs-repo factual contradiction you can verify · merge
conflict beyond the index class · any pre-push gate failure on this arc's own work.

## END PACKET (chat)
Census table · merge shas · sanity results · both file paths · every deviation and flagged gap.

## WHAT NOT TO DO
No rulings, ratifications, births, closures, or status flips · no execution of N1/N2 specs ·
no PLAYBOOK/scripts edits · no filling incomplete artifacts · no `git add -A` · no `--no-verify`.
