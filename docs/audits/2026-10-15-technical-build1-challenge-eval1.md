# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-EVAL1-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-EVAL1-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 3b58c467cd319cd6. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: verbatim evaluator record 1 of 2 for the BUILD-1 step-0 CHALLENGE; ids re-keyed X-I<item>-<k> (decide_checks' id grammar stops at a dot), text unedited.
served-model: gpt-5.6-sol
attestation-source: codex exec session file ~/.codex/sessions/2026/10/15 ("model":"gpt-5.6-sol")
producer-model: claude-opus-5-5
run: codex exec -m gpt-5.6-sol -s read-only --json -o last.md - < challenge-prompt.md (stdin closed); 2026-10-15T09:31:09Z-09:32:49Z; exit 0

# EVAL 1 - BUILD-1 CHALLENGE (Codex sol)

### I1
- id: X-I1-1 -- `cancel-in-progress` is already implemented per ref, so BUILD-1 work would duplicate live configuration | evidence: `.github/workflows/conductor.yml:87-89` | severity: HIGH
- id: X-I1-2 -- Deferring Windows to nightly removes the current per-change Windows gate before any path classifier or required-check migration exists | evidence: `.github/workflows/conductor.yml:100-107` | severity: HIGH
- id: X-I1-3 -- The proposal ignores that the matrix-generated Windows check name is part of the required-check contract; skipping it requires ruleset changes, not merely `ci_verdict` interpretation | evidence: `.github/workflows/conductor.yml:93-107` | severity: HIGH
- id: X-I1-4 -- The claimed ≥50% savings is unsupported: only the pytest matrix has a Windows leg, while the remaining jobs already run on Ubuntu | evidence: `.github/workflows/conductor.yml:106-107,230,244,319,395,484,585,661,726` | severity: HIGH
SUGGESTED: DISAGREE retain per-change Windows pytest until a measured path classifier and ruleset migration prove equivalent coverage; do not rebuild existing concurrency.

### I2
- id: X-I2-1 -- The alleged duplicate Ruff entry does not exist; the configuration contains one intentionally managed `ruff-pre-commit` hook | evidence: `.pre-commit-config.yaml:815-828` | severity: HIGH
- id: X-I2-2 -- The plugin `validate_backlog.py` is an intentional carrier twin with a parity test, so deleting it breaks the floor-carrier contract | evidence: `tests/test_validate_backlog_twin_parity.py:1-6,31-32,102` | severity: HIGH
- id: X-I2-3 -- The hub validator itself explicitly declares the plugin twin and its drift edge | evidence: `scripts/validate_backlog.py:218-219` | severity: HIGH
- id: X-I2-4 -- `aider`, `llm`, and `amp` are negative census probes; removing them defeats the test requiring every declared-absent executable to be probed rather than trusted | evidence: `scripts/provider_bench.py:699`; `tests/test_provider_bench.py:433-438` | severity: HIGH
- id: X-I2-5 -- The `terra` job is not represented as a working reviewer; it is a deliberate, non-required observability signal explaining missing credentials and wiring | evidence: `.github/workflows/conductor.yml:626-653` | severity: HIGH
SUGGESTED: DISAGREE List A is based on false duplicate/dead classifications; preserve the carrier twin, negative probes, and explicit terra-gap signal.

### I3
- id: X-I3-1 -- The bypass is unnecessary for the measured use case: F2 itself says an in-workspace file is readable without it and an external path works with the narrower `--add-dir` grant | evidence: F2 quoted in prompt | severity: HIGH
- id: X-I3-2 -- The repository already implements the bypass in the agy read adapter, so R113 does not introduce the claimed capability | evidence: `scripts/read_gate.py:375-381` | severity: HIGH
- id: X-I3-3 -- Prior live evidence shows bypassed agy was not confined to its recorded workspace and read another checkout | evidence: `docs/audits/2026-09-01-technical-agy-admission-verdict.md:243,268-274` | severity: HIGH
- id: X-I3-4 -- “Read-only tasks” are not a mitigation when the admitted bypass approves every tool; prior runs produced files in another checkout and agy scratch storage | evidence: `docs/audits/2026-09-05-technical-627-readjudication.md:280-307` | severity: HIGH
- id: X-I3-5 -- F2 corrects the cause of one denial but does not establish confinement; earlier measurements found both `--add-dir` and bypassed invocations wandering | evidence: `docs/audits/2026-09-05-technical-627-readjudication.md:498-509` | severity: HIGH
SUGGESTED: AMEND use plain in-workspace reads and narrowly scoped absolute `--add-dir` paths; refuse the global permission bypass.

### I4
- id: X-I4-1 -- The distiller duplicates existing mapping and reuse stages instead of composing them: system map, prior-art, library-first, and purpose graph already own those decisions | evidence: `scripts/system_map.py:2,21,61`; `scripts/stage_prior_art.py:2,30`; `scripts/stage_library_first.py:2`; `scripts/file_purpose_graph.py:2,107-108` | severity: HIGH
- id: X-I4-2 -- “Completion = payload file, never process exit” contradicts the existing receipt contract, which requires status `ok`, exit code zero, duration, and matching input hash | evidence: `scripts/dodo.py:245-254` | severity: HIGH
- id: X-I4-3 -- A payload-only completion rule accepts stale, partial, or prewritten payloads from a failed process; the existing runner deliberately couples the receipt to the subprocess return code | evidence: `scripts/dodo.py:287-304` | severity: HIGH
- id: X-I4-4 -- The proposed contract recreates lifecycle behavior already supplied by doit targets and telemetry receipts | evidence: `scripts/dodo.py:1-14,318-319` | severity: HIGH
SUGGESTED: AMEND compose the existing stages and retain the existing validated receipt-plus-exit contract; a payload may trigger early harvest but cannot alone prove success.

### I5
- id: X-I5-1 -- Retrying `import-linter` against tach contradicts an accepted ADR whose replacement trigger is specifically tach failing to express the layers or becoming unmaintained; neither trigger is alleged | evidence: `docs/decisions/ADR-124-one-code-standard-enforced-by-tools-adopted-one-at-a-time.md:3,61,134-148` | severity: HIGH
- id: X-I5-2 -- The proposed BUILD-3 catalogue is not one bounded row: it combines dependency enforcement, mutation testing, model gateways, IDE intelligence, cloud agents, course extraction, and an entire M06 curriculum without per-tool owners or acceptance contracts | evidence: RATIFICATION v7 R115 quoted in prompt | severity: HIGH
- id: X-I5-3 -- Scheduling the first consumer only after every speculative trial reverses the accepted adopt-one-at-a-time ratchet and delays the only end-to-end consumer evidence | evidence: `docs/decisions/ADR-124-one-code-standard-enforced-by-tools-adopted-one-at-a-time.md:54-71`; `docs/decisions/README.md:158` | severity: HIGH
SUGGESTED: AMEND run the consumer steel thread first, then admit only individually triggered tool trials through ADR-124’s one-at-a-time ratchet.

### I6
- id: X-I6-1 -- Adding `python-statemachine` creates a second orchestration authority when doit already sequences stages, halts on failure, persists targets, and checks freshness | evidence: `scripts/dodo.py:1-14,245-254,318-340` | severity: HIGH
- id: X-I6-2 -- Pydantic is already a direct dependency for existing schemas, so counting it as an advantage unique to option e inflates the matrix rather than distinguishing runners | evidence: `pyproject.toml:36`; `uv.lock:362,388` | severity: HIGH
- id: X-I6-3 -- doit is already selected and locked at 0.37.0; the proposed choice is partly a retrospective relabeling, not an evaluated replacement | evidence: `pyproject.toml:90-100`; `uv.lock:408-413` | severity: HIGH
- id: X-I6-4 -- The matrix recommends e before its decisive resume/process-tree witnesses exist, while its own text labels them PENDING-MAP V9 | evidence: DESIGN section 3 quoted in prompt | severity: HIGH
SUGGESTED: AMEND keep conductor plus existing doit receipts; add a state-machine library only after a concrete transition invariant cannot be expressed by the existing stage table.

### I7
- id: X-I7-1 -- L1 is not a disjoint lane: it combines runner lifecycle, schema, task-source migration, constraint registry, distillation, adversarial governance, vendor dispatch, and an ADR | evidence: BATCH lane table L1 and AMEND v5 L1 quoted in prompt | severity: HIGH
- id: X-I7-2 -- L3 mixes prompts-guard recovery, known-red expiry, CI policy, destructive cleanup, and future-row filing, creating unrelated failure and review surfaces | evidence: BATCH lane table L3 and AMEND v5 L3 quoted in prompt | severity: HIGH
- id: X-I7-3 -- L2 depends on the agy permission result and shares `dispatch.py` with L4, yet is ordered after L4; that makes the sign-in lane land before its consumer route is settled | evidence: BATCH lane table L2/L4 quoted in prompt | severity: HIGH
- id: X-I7-4 -- L5 is required to teach the L6 inbox command but has no declared land-after-L6 dependency | evidence: AMEND v5 L5/L6 quoted in prompt | severity: HIGH
- id: X-I7-5 -- Moving the steel thread to BUILD-2 removes end-to-end proof from the batch introducing the loop, so BUILD-1 can close with individually green mechanisms that have never operated together | evidence: AMEND v5 “BUILD-2 slot 1” quoted in prompt | severity: HIGH
SUGGESTED: AMEND split by executable ownership, land L4 before dispatch consumers, land L6 before boot documentation, and retain a minimal BUILD-1 steel thread.

### I8
- id: X-I8-1 -- `NEW-JUSTIFIED` adds a new approval vocabulary over an existing reuse gate and prior-art stage without identifying an unmet enforcement case | evidence: `scripts/file_purpose_graph.py:1873-1882`; `scripts/stage_prior_art.py:2,30` | severity: HIGH
- id: X-I8-2 -- `ChallengeReceipt` duplicates the existing decision/finding pipeline instead of using its OWNED, DISCHARGED, CANDIDATE, and REJECTED outcomes | evidence: `docs/decisions/README.md:145` | severity: HIGH
- id: X-I8-3 -- Making another vendor’s confirmation mandatory turns duplicate detection into an external-provider availability dependency, despite the repository already having deterministic reuse surfaces | evidence: AMEND v5 L1 quoted in prompt; `scripts/system_map.py:2,21`; `scripts/file_purpose_graph.py:107-108` | severity: HIGH
- id: X-I8-4 -- The point-task payload rule weakens the existing success invariant by discarding exit status | evidence: `scripts/dodo.py:245-254,287-304` | severity: HIGH
SUGGESTED: DISAGREE reuse the existing prior-art/reuse gate and finding pipeline; do not introduce parallel receipt vocabularies or payload-only success.

### I9
- id: X-I9-1 -- Routing all reads through agy first makes an over-privileged, previously unconfined tool the default despite Copilot already being the proven fallback | evidence: `docs/audits/2026-09-01-technical-agy-admission-verdict.md:243,268-290` | severity: HIGH
- id: X-I9-2 -- The bypass route is broader than necessary under the proposer’s own F2 measurement because ordinary in-workspace reads and `--add-dir` both succeed | evidence: F2 quoted in prompt | severity: HIGH
- id: X-I9-3 -- Earlier adjudication required every agy invocation to declare its workspace and identified explicit path or `--add-dir` as the remedy; the proposed route drops that narrower contract | evidence: `docs/audits/2026-09-05-technical-627-readjudication.md:658-664,721` | severity: HIGH
SUGGESTED: DISAGREE keep Copilot first and admit agy only for explicitly scoped paths without global bypass.

### I10
- id: X-I10-1 -- The CI concurrency addition is already present | evidence: `.github/workflows/conductor.yml:87-89` | severity: HIGH
- id: X-I10-2 -- List A contains two false deletion candidates: the validator is a tested carrier twin and absent provider names are mandatory probes | evidence: `tests/test_validate_backlog_twin_parity.py:1-6,31-32,102`; `tests/test_provider_bench.py:433-438` | severity: HIGH
- id: X-I10-3 -- Filing Linux-first before resolving required Windows check contexts creates a policy row whose implementation premise is known incomplete | evidence: `.github/workflows/conductor.yml:93-107` | severity: HIGH
SUGGESTED: DISAGREE remove the already-done concurrency work and reject List A; first design the Windows required-check migration with evidence.

### I11
- id: X-I11-1 -- A fake-agy RED test can prove formatting and timeout behavior but cannot prove that agy emits a browser URL/code or supports the assumed device-auth flow | evidence: AMEND v5 L4 quoted in prompt | severity: HIGH
- id: X-I11-2 -- The provider registry records authentication/server constraints for provider CLIs, so implementation cannot be committed before the requested research establishes an actual agy sign-in protocol | evidence: `ecosystem/provider-registry.yaml:380-390,443` | severity: HIGH
- id: X-I11-3 -- A ten-minute synchronous operator wait is misplaced inside an otherwise unattended lane; existing lifecycle doctrine requires bounded file-observed loops rather than ending or blocking on waits | evidence: `ARCHITECTURE.md` quality requirement `QR-AVAIL-001`; `scripts/dispatch.py:1984-2039` | severity: HIGH
- id: X-I11-4 -- Recording only a GAP after timeout does not prove cleanup of the waiting process or authentication subprocess | evidence: AMEND v5 L4 quoted in prompt; `ARCHITECTURE.md` quality requirements `QR-AVAIL-004` and `QR-AVAIL-005` | severity: HIGH
SUGGESTED: AMEND research and probe agy’s real authentication protocol first; if device auth exists, emit a durable operator-action receipt and let a later invocation resume.

### I12
- id: X-I12-1 -- Landing “R100–R115” as a continuous range is invalid because no ratification contains an R103 heading | evidence: F3 quoted in prompt | severity: HIGH
- id: X-I12-2 -- The standing register currently asserts that R100 does not exist, while the handoff claims R100–R102 exist; blindly appending the range would preserve contradictory provenance | evidence: `protocols/STANDING_RULINGS.md:6307`; `docs/handoffs/2026-10-14-dev-knowledge-architect/SUPPLEMENT.md:160` | severity: HIGH
- id: X-I12-3 -- R104–R110 and R112 being sourced only from superseded files requires explicit provenance resolution; a boot lesson cannot treat them as live merely because v7 says “unchanged” | evidence: F3 and RATIFICATION v7 “Unchanged” quoted in prompt | severity: HIGH
- id: X-I12-4 -- Boot v2 is being made dependent on unbuilt distiller, routing, CI, transport, and authentication behavior, so its citations can pass while its operational claims remain false | evidence: AMEND v5 L5 quoted in prompt | severity: HIGH
SUGGESTED: DISAGREE reconcile each ruling ID and authoritative source individually, omit nonexistent R103, then generate boot content only from landed mechanisms.

### I13
- id: X-I13-1 -- Most of L6 is already implemented: write-triggered INDEX refresh, janitor dry-run/apply with manifest verification, query, seat IDs, and archive conservation all exist | evidence: `scripts/transport.py:917-982,1021-1030,1070-1112,1196-1230,1548-1607,1637-1681` | severity: HIGH
- id: X-I13-2 -- The proposed architect inbox duplicates the existing `query` command, which already filters generated INDEX rows by seat, status, date, and kind | evidence: `scripts/transport.py:1548-1580,1727-1737` | severity: HIGH
- id: X-I13-3 -- “One live file per subject” plus machine-written OPEN→ANSWERED→CLOSED state conflicts with the repository’s immutable dated-artifact rule; request files cannot be rewritten in place to add disposition fields | evidence: `ARCHITECTURE.md` Layer Boundaries invariant 5; AMEND v5 L6 quoted in prompt | severity: HIGH
- id: X-I13-4 -- Running `janitor --apply` against the operator’s Drive is a material synced-directory move operation, and the carried lane contract explicitly required a constrained dry run before any such apply | evidence: `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1439-transport-index.md:89`; `scripts/transport.py:1026-1028` | severity: HIGH
- id: X-I13-5 -- INDEX auto-refresh currently fails open, so the proposed done-when “index --check exits 0 after a transport write” is not guaranteed by the existing trigger and requires a policy decision about whether transport writes must fail | evidence: `scripts/transport.py:964-982` | severity: HIGH
- id: X-I13-6 -- L6 conflates an operator-approved destructive archive act, generated-index policy, request lifecycle design, lint expansion, Stop-hook repair, and a help-text defect into one lane | evidence: AMEND v5 L6 quoted in prompt | severity: HIGH
SUGGESTED: AMEND treat current transport/index/query/janitor code as the base, split defects by owner, keep requests immutable through separate answer records, and require an operator-reviewed janitor manifest before Drive moves.

DONE.
