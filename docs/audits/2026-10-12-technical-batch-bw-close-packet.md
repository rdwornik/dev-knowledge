# Batch BW (B2-W4 finish) — close packet · 2026-10-13

> The `closed_by` artifact named in `docs/audits/2026-10-12-technical-batch-bw-manifest.md`.
> Written by the successor integrator seat (Claude Code, claude-opus-5-5, session `86360a36`)
> under `to-cc/BATCH-BW-FINISH-2026-10-13.md` v2 (R98, R100, R101) and the night order's R4/R5.
> Every figure names its instrument; a figure with no instrument is marked UNMEASURED.

## 1. Landed on main (first-parent spine, batch base `c1b65e6d`)

| Wave | Main merge | Integration tip | Lands | Run |
|---|---|---|---|---|
| F0 | `3db32c1a` | `955e5a35` | manifest + F1 contracts; row F1-MR | 38319729602 |
| F1 | `26bd4d93` | `92b8b9b2` | b2w3-carry, distill-kind-fix, known-reds-expiry, main-red, hook-launcher (1 refusal, 1 repair) | 38357704691 |
| C | `d8619ab0` | `68a82db1` | C1 lane-report-rollup, C2 required-tools, C3 reuse-gate, C4 sessionstart-one, C5 adr-lifecycle, C6 system-map (1 refusal, 1 repair) | 38381707578 |
| D | `8e00b78d` | `81f0b06a` | D3 rulings-landing `214ea12e`, D4 registry-repoint `b06c621a`, D6 harness-probes `1fdeae35`, D8 transport-index `a880ed01`, R98 re-date `dc24b371`, repair `eff36928` (1 refusal, 1 repair) | 38431018618 |

Every land verdict was LANDED PRE-EXISTING (instrument: `merge_path.py land` output, recorded in
`to-browser/SESSION-b2w4-finish.md`). Wave D's first candidate `2709d9a7` (run 38425926539) was
REFUSED REGRESSED by one new red, `test_generator_newlines.py::test_every_text_write_in_scripts_pins_newline`
(`scripts/harness_probes.py:448`, lane D6); the repair `b6d19b6c` pins `newline="\n"` (Codex r1
APPROVE, session `01a13617-851f-71c1-9352-06fbd4edd9ac`, nonce `20a86cac`).

## 2. Not landed

| Lane | State | Tip (pushed) | Why |
|---|---|---|---|
| D1 lane-bw-1374-lane-controller | INPUT_REQUIRED, held | `b1db35ff` | `land` refuses the integrator's own merges as LANE-UNATTRIBUTED (measured on `271d7f35`, `2d81452c`); Codex r1 REQUEST-CHANGES HIGH:3; architect UNSURE |
| D5 lane-bw-1450-boot-teaching | INPUT_REQUIRED, held | `f0d49169` | R95 D1 citation check reads R97's "replaces R96 D14" as superseding all of R96; Codex r1 REQUEST-CHANGES HIGH:1; architect NO. Boot v2 unlanded: 17,822 B, sha256 `91178f8b86437273074bf4c28c01f07cea5839fa47693575789c6120d4481396` |
| D7 lane-bw-1439-commit-attribution | CANCELED, held | not provisioned | `lane_boot.py preflight` refused: the manifest row is HELD and no `…-manifest-amendment-N.md` GO is on main ([#685]); distill found no BUILD-LIST row |
| D2 lane-bw-680-handoff-gen | FAILED | `10268435` | operator cost ruling 2026-10-13 16:11 after five REQUEST-CHANGES rounds |

## 3. Rows filed vs closed

Instrument: `tasks/<id>-*.md` presence and `status:` at `c1b65e6d` vs `8e00b78d`.
**Filed 0, closed 1** (`[#1103]`, by D4). Open task files at close: 580.
Owed and not filed (operator decisions in the rollup): rows for the three `test_consumer_at_landing`
reds (ROWS-OWED at every BW land), the Windows `test_pairing` flake, R94 / R95 D1-D2 / ADR-123/124
(D3's HOLDING dispositions), `AMEND-BATCH-B2-W4-CC-FINISH-R99` (the local IN_ERA red).

## 4. BACKLOG size

Instrument: `git show <ref>:BACKLOG.md` bytes and `\n- [#` count.
Base `c1b65e6d`: 127,041 B, 633 lines. Close `8e00b78d`: 126,873 B, 632 lines.

## 5. R97 (a)-(c), reported by the BW integrator as its carriage requires

- **(a) CI economy:** each wave landed in ONE integration branch, but every wave needed a second
  land after one refusal and one repair (F1, C, D) — 7 land CI runs for 4 waves, plus F0's first
  REGRESSED land. No re-run was used to clear a registered flake. R97's reopen clause ("a wave lands
  with more than one CI run outside a registered flake") **fires** for F1, C and D.
- **(b) B5** was narrowed to the WIRE-intake kind fix and landed in F1 (distill-kind-fix, `[#1447]`).
- **(c) B2-W3 seat leftovers:** cycle-2's four dirty files were proven on main (three byte-identical
  blobs, one receipt line present) and archive-committed `014effc6` under tag
  `archive/2026-10-13/worktree-seat-integrator-b2-w3-cycle-2`; cycle-4 `5eacd135` tagged
  `archive/2026-10-13/worktree-seat-integrator-b2-w3-cycle-4`. No `--force` was used.

## 6. Hygiene (R4)

Instrument: `git worktree list`, `git branch`, `git ls-remote --heads origin`, `git stash list`.

| | worktrees (incl. primary) | local branches | origin branches | stashes |
|---|---|---|---|---|
| before R4 | 19 | 23 | 20 | 0 |
| at this packet | 2 (primary + integrate-bw, removed after this land) | 17 | 14 | 0 |

Merged and deleted (local + origin): the four landed Wave D lanes, `worktree-b2w2-transport-index`,
`worktree-scope-guard-copilot`; `fix/bw-d-land-repair` (local only, never pushed). Every unmerged
branch is kept and tagged `archive/2026-10-13/<branch>` on origin (14 tags); deleting them is the
operator's act, listed in the rollup. `automation/fleet-audit` is protected (STANDING_RULINGS I-D).

## 7. Cost

Instrument: `scripts/lane_cost.py seat --session <id>` (rates as_of 2026-06-24; main thread only,
subagent transcripts are not in the figure, so each is a FLOOR).
Seat `ac626cdc` (BW orchestrator, F0-D boot): USD 31.72. Seat `86360a36` (this successor): measured
at the rollup. `claude -p` launches by this seat: 0. BW lane costs: UNMEASURED (no `lane_cost.py
close` entries for batch BW in `logs/LANE-COSTS.jsonl`).

## 8. Vendors (S0, 2026-10-13)

Codex live (gpt-5.6-terra); Copilot CLI 1.0.96 live, no printed model list; Grok and Gemini have
no `provider_router` route (MISSING). Every BW code review was Codex.
