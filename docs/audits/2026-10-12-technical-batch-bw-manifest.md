---
batch: BW
seq: 1
status: open
closed_by: docs/audits/2026-10-12-technical-batch-bw-close-packet.md
---

# Batch BW (B2-W4, finish) — manifest · 2026-10-12

**Seat:** primary CC session `2d59e52d-ca14-4b21-88ab-26581e4b65f3` (Opus 5.5), orchestrator and
integrator · **Order:** `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md` (transport; `transport_lint`
exit 0) · **Base at freeze:** `main` `c1b65e6d` · **Open batches at freeze:** 0
(`batch_manifest.open_batches` = `[]`).

**Why `BW` and not `B2-W4`.** `validate_branch_naming.LANE_WORKTREE_RE` admits a batch token of
1-3 lowercase letters only, so `lane_boot.py preflight --lane lane-b2w4-…` refuses at the name
(exit 1, recorded at F0.2). `bw` = B2-W4. The B2-W4 Copilot run (lanes A1, B1-B6) booted with
**no** manifest at all: `open_batches` was `[]` and no B2-W3 or B2-W4 manifest exists in
`docs/audits/` (`git log -S "B2-W3" -- docs` finds lane commits only). That is the gap lane
`lane-bw-1374-lane-controller` closes at `land`.

## 0 · The GO

**GIVEN, by file.** The operator GO for every lane in §2 is:

- `to-browser/RATIFICATION-2026-10-11.md` — R96 (the B2-W3 aftermath package and the B2-W4 lane
  list, D1-D15);
- `to-browser/RATIFICATION-2026-10-12.md` — R97 ("wszystko może być przez CC zarządzane"):
  Claude Code orchestrates and produces through subagent lanes in worktrees; (a) one land and one
  CI run per wave; (b) B5 narrowed to the WIRE-intake kind fix; (c) B2-W3 seat leftovers land or
  are proven on main before their worktrees go.

No R98 exists in `RATIFICATION-2026-10-12.md` at freeze, so no known-reds entry is re-dated by
this batch (order F0.4).

## 1 · Ids

No new task id is filed by this freeze. **The `<id>` in each lane name is the nearest OPEN row,
not necessarily its owner** — only six lanes have an owning row (marked `owner`); the others are
`nearest` and their findings are filed through intake at batch close (ADR-98/ADR-111), never by a
lane computing `max + 1`.

## 2 · The lanes

Substrate LOCAL for all: a subagent of the orchestrator session, in the named worktree
`/lane-boot` provisions from the primary. Review: Codex (`codex exec -s read-only`) until APPROVE,
two failed reviews = FAILED. Usage test: Copilot (R8) for a tool, skill or command lane.

| # | Lane slug | Rows | Wave | Model / effort | Review | State |
|---|---|---|---|---|---|---|
| F1-A2 | `lane-bw-1001-hook-launcher` | `[#1001]` nearest (carries `worktree-scope-guard-copilot` @ `55922ff4`) | F1 | opus / high | Codex | GO |
| F1-B5 | `lane-bw-1447-distill-kind-fix` | `[#1447]` nearest (carries `worktree-distill-kind-fix` @ `8d4dee0e`, narrowed by R97(b)) | F1 | opus / high | Codex | GO |
| F1-KR | `lane-bw-912-known-reds-expiry` | `[#912]` `[#664]` `[#1340]` `[#1341]` `[#1343]` `[#1344]` owner | F1 | opus / high | Codex | GO |
| F1-W3 | `lane-bw-893-b2w3-carry` | `[#893]` nearest (cycle-4 `5eacd135`, tag `archive/b2-w3-close-carry`) | F1 | sonnet / medium | n/a — ledger lines | GO |
| F1-MR | `lane-bw-926-main-red` | `[#926]` owner (journal leg), nearest (Windows `test_gen_handoff` leg) — added before F0's land by `to-cc/BATCH-BW-NIGHT-2026-10-13.md` R2 | F1 | opus / high | Codex | GO |
| C1 | `lane-bw-1368-lane-report-rollup` | `[#1368]` nearest | C | opus / high | Codex | GO |
| C2 | `lane-bw-958-required-tools` | `[#958]` nearest | C | opus / high | Codex | GO |
| C3 | `lane-bw-735-reuse-gate` | `[#735]` nearest | C | opus / high | Codex | GO |
| C4 | `lane-bw-1001-sessionstart-one` | `[#1001]` owner | C | opus / high | Codex | GO |
| C5 | `lane-bw-242-adr-lifecycle` | `[#242]` nearest | C | opus / high | Codex | GO |
| C6 | `lane-bw-781-system-map` | `[#781]` nearest (D15: `uv add grimp`) | C | opus / high | Codex | GO |
| D1 | `lane-bw-1374-lane-controller` | `[#1374]` nearest | D | opus / high | Codex | GO |
| D2 | `lane-bw-680-handoff-gen` | `[#680]` nearest | D | opus / high | Codex | GO |
| D3 | `lane-bw-1378-rulings-landing` | `[#1378]` nearest | D | opus / high | Codex | GO |
| D4 | `lane-bw-1103-registry-repoint` | `[#1103]` owner | D | opus / high | Codex | GO |
| D5 | `lane-bw-1450-boot-teaching` | `[#1450]` owner (carries `worktree-b2w2-boot-teaching` @ `a9503f76`) | D | opus / high | Codex | GO |
| D6 | `lane-bw-670-harness-probes` | `[#670]` nearest; read-only in `corp-monorepo` | D | opus / high | Codex | GO |
| D7 | `lane-bw-1439-commit-attribution` | needs operator ruling R100 | D | opus / high | Codex | HELD — runs only if `RATIFICATION-2026-10-12` carries R100; none at freeze |
| D8 | `lane-bw-1439-transport-index` | `[#1439]` owner (carries `worktree-b2w2-transport-index` @ `14f91ba0`, contract `LANE-1439-b2w2-transport-index`) | D | opus / high | Codex | GO |

**Amended before landing by `to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99-2026-10-12.md`** (sha256
`8d117467…d1b1`, `transport_lint` exit 0), under R98 and R99 (`RATIFICATION-2026-10-12.md` v2):
X1 — `known-reds-expiry` re-dates nothing and its remaining list goes into the rollup's F0
section by the end of 2026-10-15; X2 — D1's Done-when is the amendment's five clauses (dispatch
launches every producer kind, the producer is written to section 3, `land` refuses a branch
dispatch did not launch, the main thread reviews every lane as architect, a Copilot and a Codex
lane end to end); X3 — D7 and D8 above, at most 6 lanes at a time; X4 — each wave's rollup
section at most 3 KB. D3 lands R93-R99.

Contracts: `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-<id>-<slug>.md`.
F1's four are frozen with this manifest; Wave C's and Wave D's are frozen on the integration
branch of the wave before them, so each rides a landed, CI-judged commit before its lane boots.

## 3 · Integration (R97a)

One integration worktree `integrate-bw`, branch `worktree-integrate-bw`. Per wave: every APPROVE
lane merged `--no-ff` into one integration commit chain, targeted tests and
`gen_doc_counts.py --write` there, then ONE `merge_path.py land --slug b2-w4-<wave>`. A re-run
only when the sole red is a registered flake (`[#1344]` class). A refused `land` stops that
wave's merging and is recorded.

## 4 · Lane rules (every contract points here; the contract's own Done-when is the lane's scope)

1. **Where.** Work ONLY in the absolute worktree path the orchestrator hands you, on branch
   `worktree-<lane>`. Every command runs there; `uv run --locked …` always, never bare
   `python`/`pytest`. Seed check: `uv run --locked python scripts/worktree_import_proof.py --repo .`.
2. **Before creating any file**, run `uv run --locked python scripts/file_purpose_graph.py why
   <neighbour>` on the files beside it. A new file is allowed only where the contract's Done-when
   names it (or names its directory and purpose); anything else is reuse or a finding.
3. **RED first.** Commit a failing test (`test(<slug>): RED -- …`), then the fix. Then
   `uv run --locked ruff check <changed .py>` and the TARGETED tests for the diff (never the full
   suite — that runs once per wave, at integration). Record exact pass/fail counts.
4. **Git.** Commit and push ONLY your own `worktree-<lane>` branch (`git push -u origin
   worktree-<lane>`). Never touch `main`, another branch, another worktree, global config, or
   `--force`/`-D`. Never `--no-verify`. If a gate fires, fix the cause; if you cannot, stop and
   report it.
5. **No JOURNAL entry, no `gen_doc_counts --write`, no BACKLOG regeneration in the lane.** The
   integrator writes one JOURNAL entry per wave with a unique day letter, and runs the
   generators on the integration commit (the five-`(d)` collision of 2026-10-11 is the reason).
6. **Review.** Run Codex on your branch diff: `codex exec -s read-only "<review prompt naming
   the Done-when verbatim and git diff origin/main...HEAD>" </dev/null`. Fix and re-review until
   APPROVE. Two REQUEST-CHANGES rounds that you cannot close = state FAILED. Record the served
   model and session id from Codex's own output.
7. **Usage test (R8)** when the lane ships a tool, skill, command or hook: run Copilot non-
   interactively against the real artefact (`copilot -p "<task that must use it>" --allow-all-tools`
   from the worktree) and record what it did. If Copilot cannot run, record `NOT_RUN` with why.
8. **Handback.** Return to the orchestrator: branch, tip sha, commits, targeted-test counts, the
   HANDBACK line `HANDBACK worktree-<lane> @ <sha> code review=codex HIGH:n MED:n LOW:n` (checked
   with `uv run --locked python scripts/audit.py handback "<line>"`), and every decision taken.
9. **LANE REPORT.** Write `to-browser/LANE-END-<lane>.md` on the transport
   (`$CLAUDE_PROMPTS_DIR`, user scope) with the transport header (`carried-by: OPEN`,
   `kind: LANE_END`, `date`, `supersedes: none`, `summary`, `by`), the one-line §3 rendering, and
   ONE fenced `json` block in the section-3 shape of
   `to-browser/DIGEST-PROPOSAL-ADR-LANE-REPORT-CONTRACT-2026-10-11.md`. `merged_sha` stays null
   (the integrator fills it). Lint it: `uv run --locked python scripts/transport_lint.py check
   <file>` exit 0. Touch no other transport file.
10. **Architect review (R99.2).** After the handback the orchestrator reviews the result against
    this contract's Done-when and records the verdict in the report's `intent_met`
    (`evaluator.vendor: anthropic`, the orchestrator's session id); the Codex review stays.
11. **Never ask the operator.** A blocker is recorded (`INPUT_REQUIRED` with `operator_action`),
    and the lane hands back.

## 5 · Closed by

`docs/audits/2026-10-12-technical-batch-bw-close-packet.md`, written when Wave D has landed or
been recorded as stopped. Until then this batch is OPEN.

## Amendment 1 (2026-10-24, lane ci-one-verdict-2, [#1525]) — contract links

Amendment marker only; nothing above is edited. The launch contract of lane F1-KR is an undated
file, so a `tasks/` or ADR citation cannot make it consumed (the consumer_at_landing pool
tokenizer reads dated names only); the batch-manifest link is the route. Linked here by path:

- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-912-known-reds-expiry.md` — F1-KR, owner rows `[#912]` `[#664]` `[#1340]` `[#1341]` `[#1343]` `[#1344]`; finding dispositioned by `[#1583]` (owner rows exist) and `[#1525]`.
