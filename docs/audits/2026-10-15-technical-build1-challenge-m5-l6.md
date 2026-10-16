# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-M5-L6-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-M5-L6-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 0076eb20db6e2bba. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: CHALLENGE matrix M5 - AMEND v5 L6 transport and communication. Verdict AMEND - most of it exists; extend query (--since), keep requests immutable (status derived from answer records in the INDEX), find why the write-trigger left INDEX stale, janitor --apply only behind an operator-reviewed manifest.

# M5 - L6 transport / communication

## Prior art (S2 research + spot checks)
- `scripts/transport.py` subcommands report, strays, derive, inventory, index (--write/--check), seat-ids, query, janitor (:1695-1745).
- INDEX refresh ALREADY fires after every `transport.write/append` (`_after_write`, :963-982) and fails open; yet `to-browser/INDEX.md` is 375,536 B and stale (mtime 2026-10-14 23:46) - so writers bypass `transport.py` (seats writing Drive files directly), which a trigger cannot see.
- `query` has `--seat --kind --status --date --json`; no `--since` (:1727-1737). `transport_lint.py sweep` already has `--since` (:453).
- `janitor --apply` moves to `<folder>/archive/YYYY-MM/`, never deletes, and refuses without `--expect-manifest <sha of the reviewed dry run>` (:1021-1031, :1120-1150, :1738-1742).
- Nothing sets `disposition:`/`answered-by:`; `gen_handoff.py:1409,1449` only reads `disposition:`.
- `transport_report.py --help` exits 4 ("unexpected SystemExit: 0", "NOT delivered").
- X-I13-3 (Codex): machine-editing another seat's request file in place conflicts with append-only artefacts. Held - status is derived, not written into the request.
- X-I13-4: `janitor --apply` on the operator's Drive needs the reviewed manifest (BW contract precedent, LANE-bw-1439:89). Held.

Weights: unattended=20 code=15 libfirst=15 modelagnostic=15 osagnostic=10 tokens=10 testable=10 simplicity=5
| Option | unattended | code | libfirst | modelagnostic | osagnostic | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A. as written (edit requests in place, new inbox) | 3 | 4[^1] | 3 | 3 | 3 | 3 | 3 | 2 | 3.10 |
| B. extend transport.py, derived status, reviewed janitor | 3 | 4[^1] | 4[^1] | 3 | 3 | 4[^2] | 3 | 3 | 3.40 |
| C. status quo | 2 | 3 | 3 | 3 | 3 | 1 | 3 | 4[^3] | 2.65 |

[^1]: measured -- scripts/transport.py:963-982, :1021-1031, :1727-1737 exist, read 2026-10-15
[^2]: measured -- INDEX.md 375,536 B today; a headers-only `query --since` reads a fraction of it
[^3]: measured -- no change; current tools run (S2 research)

## Verdict: AMEND (intent of the operator's ask kept: simple communication, machine-set status, current index)
1. `query --seat <s> --since <iso>` = the architect inbox (extend `query`, no new command); headers only.
2. Status OPEN -> ANSWERED -> CLOSED is **derived** in the INDEX by joining a request to the answer record that names it (`answers: <file>` header written by the answering writer); no seat edits another seat's file.
3. Find and fix why INDEX went stale despite `_after_write` (direct Drive writers); `index --check` in the batch-close step; INDEX current-only <= 40 KB, history to an archive index.
4. `janitor --apply` only with `--expect-manifest` of a dry run the operator has reviewed (OPERATOR-ACTION line); never on an unreviewed plan.
5. `by:` mandatory for script writers (Stop-hook LANE-END writer); `wrong-folder` from the registry; `transport_report.py --help` exits 0.
6. `[#1332]` as its own Done-when (gen_handoff/assemble_paste), unchanged.
