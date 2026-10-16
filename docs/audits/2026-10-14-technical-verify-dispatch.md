# Archive copy of transport file DIGEST-VERIFY-dispatch-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-dispatch-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] c09296ff4e1046e2. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-a-dispatch-land (Sonnet 5.5), base b46836c8, area V1 dispatch and lane start

| element | class | witness | caller |
|---|---|---|---|
| dispatch.py (group --help) | WORKS | `uv run --locked python scripts/dispatch.py --help` exit 0; lists 10 verbs (5 codespace-*, govern, launch, plan, queue, repair) | PLAYBOOK Ch8 dispatch table |
| dispatch.py plan | WORKS | `plan LANE-1444-b2w2-merge-clock.md --token-cap 1000000` exit 0, JSON `"slug": "b2w2-merge-clock", "model": "claude-sonnet-5-5", "substrate": "local"`; without --token-cap: `Error: Missing option '--token-cap'` | dispatch table |
| dispatch.py plan, collision guard | WORKS | `plan LANE-nv-929-b-ci-gates.md --token-cap 1000000` exit 1: `SKIP -- branch 'worktree-lane-nv-929-b-ci-gates' already exists; not dispatching a second lane.` (correct: lane is live) | launch path |
| dispatch.py queue --dry-run | WORKS | 6 NV contracts: `[queue] 6 lane(s), static order: 1. lane-nv-929-a-dispatch-land (local) ... 6. lane-nv-1450-f-handoff-gaps (local)` exit 0 | dispatch table |
| dispatch.py launch | UNRUN | forbidden by contract (a probe that launches is a lane); `--help` exit 0 | operator `dispatch` shim |
| dispatch.py govern | UNRUN | appends logs/receipts/LAUNCH-SPEND-*.jsonl (a repo write); `--help` exit 0 | launch |
| dispatch.py repair, codespace-exec / -delete / -stop | UNRUN | forbidden by contract; `--help` exit 0 each | dispatch table |
| dispatch.py codespace-harvest / -observe | UNRUN | `--help` exit 0; need a live codespace, none open (`[codespace] no open container`); observe writes a fate row | codespace-delete gate |
| MAP-DISPATCH.md vs dispatch.py --help | WORKS | to-browser/MAP-DISPATCH.md `dispatch.py verbs:` line lists the same 10 verbs as --help (diff by eye: identical) | gen_handoff.py --dispatch-map |
| substrate cloud (Dispatch-Cloud) | DEAD | MAP-DISPATCH: `substrate: cloud ... start: none ... state: DECLARED`; no cloud verb in --help; Grep `Dispatch-Cloud\|cloud_dispatch` in scripts, ecosystem, .claude/commands: name hits only, no launcher | none starts it |
| substrate interactive | DEAD | MAP-DISPATCH `substrate: interactive ... start: none ... DECLARED` (human-typed) | none |
| substrate codespace, last run | BROKEN | ~/.claude/remote-runs/CODESPACE-FINISH/codespace-parity-2026-10-14/steps.jsonl: `"failure": "the lane returned no handback"`, `"fate": FAILED`, receipt.json `"handback": {"present": false}`; admission ok | codespace-exec |
| scripts/lane_boot.py preflight | WORKS | `lane_boot.py preflight --lane lane-nv-929-a-dispatch-land --repo .` exit 1: `LANE-BOOT REFUSAL: open_batches() -> []: NO committed manifest declares an open batch` (correct: no NV manifest) | /lane-boot |
| /lane-boot | WORKS | present as .claude/commands/lane-boot.md (not .claude/skills/lane-boot/: PREMISE-FAILED); dispatch_drift: `14 literal command(s) resolve; .claude/commands/lane-boot.md names the ruled verb 'dispatch'` | operator |
| scripts/dispatch_drift.py | WORKS | exit 0, line above | audit |
| scripts/dispatch_surface.py check / resolve | BROKEN | `check LANE-nv-929-a-dispatch-land.md` exit 1: `model 'claude-sonnet-5-5' is outside the enum {opus \| opusplan \| sonnet \| haiku}`; same for `resolve`. The same contract's `dispatch.py plan` accepts the id (plan on LANE-1444 shows claude-sonnet-5-5), and gen_lane_contract emits it | gen_lane_contract.py, audit.py, gen_handoff.py |
| scripts/offload_admission.py | WORKS | `--seeded-defects` exit 0: the `[refused]` cases (7 shown) each for its own code, `[control] admissible record -> ADMITTED` | harness.yaml, audit.py |
| scripts/codespace_admission.py | WORKS | `--repo-root .` exit 1: `REFUSED -- claude_on_path, uv_on_path, python3_on_path, pre_commit_on_path, git_hooks_armed` (correct on a non-container host) | codespace dispatch |

## CHECKER
vendor: OpenAI Codex CLI 0.155.0, `codex exec -m gpt-5.6-terra -s read-only`. Served model: tool header `model: gpt-5.6-terra` (the body self-reported `gpt-5`; the header is the tool's own output). Attempt 1 ran through uv and failed: uv cache access denied in its sandbox, so every command row read DISAGREE for that reason only. SUBSTITUTION: retried once through the venv interpreter. Retry verdicts, verbatim (table sha256 7f8a9b990c1a...d3062c):

dispatch.py (group --help) | AGREE | exit 0; lists 10 verbs, including all five codespace verbs.
dispatch.py plan | AGREE | exit 0; `slug=b2w2-merge-clock`, `model=claude-sonnet-5-5`, `substrate=local`.
dispatch.py plan, collision guard | AGREE | exit 1; `SKIP -- branch 'worktree-lane-nv-929-b-ci-gates' already exists`.
dispatch.py queue --dry-run | DISAGREE | exit 0, but order is `lane-nv-1450-f...`, `689-e...`, `929-a...` through `929-d...`; `929-a` is third, not first.
substrate cloud (Dispatch-Cloud) | AGREE | `dispatch.py --help` exposes no cloud verb.
scripts/lane_boot.py preflight | AGREE | exit 1; `open_batches() -> []` refusal.
/lane-boot | AGREE | `dispatch_drift.py` exit 0; 14 commands resolve and lane-boot names `dispatch`.
scripts/dispatch_drift.py | AGREE | exit 0; host-tier resolution succeeds.
scripts/dispatch_surface.py check / resolve | AGREE | both refuse `claude-sonnet-5-5` outside `{opus | opusplan | sonnet | haiku}`.
scripts/offload_admission.py | UNRUN | sandbox has no usable temporary directory; `TemporaryDirectory()` raises `FileNotFoundError`.
scripts/codespace_admission.py | DISAGREE | exit 1 as claimed, but additionally refuses `git_remote_reachable`.
MAP-DISPATCH diff, interactive, codespace last run | UNRUN | files not read.

Both readings stand. Queue DISAGREE = argument order (priority is the order given): I passed 929-a first, the checker 1450-f first; both are correct output for their arguments. The extra codespace_admission refusal is the checker sandbox's blocked network. Cloud and dispatch_surface were AGREED; the codespace last run is single-vendor.

## USAGE
Claude tokens: not measured. agy calls: 0. Copilot substitutions: 0. Other vendor: 2 codex calls (one failed on uv, one retry), about 52k and 34k tokens.
