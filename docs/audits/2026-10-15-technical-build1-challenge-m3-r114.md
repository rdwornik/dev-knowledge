# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-M3-R114-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-M3-R114-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 352b0260068986f5. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: CHALLENGE matrix M3 - R114 / AMEND L1: the distiller, its CHALLENGE sub-stage and the point-task contract. Verdict AMEND - extend gen_lane_contract distill and the existing kill/verify organs; completion = a FRESH valid payload, exit recorded, never payload alone.

# M3 - R114 / AMEND L1: distiller + CHALLENGE + point tasks

## Prior art (S2 research, spot-checked)
- `scripts/gen_lane_contract.py:2227-2294` `distill`: renders a contract from a `protocols/BUILD-LIST.md` row (not `tasks/` - R106 conflict), fixed model/effort rules (:1698, :1870), no reuse search, no model call, scope left as `<SLOT>`.
- Reuse/duplicate organs exist but none refuses NEW-where-a-candidate-exists: `scripts/hooks/reuse_gate.py` (PreToolUse, `.claude/settings.json:100`) refuses a new file only when no `why` search ran, and fails open; `file_purpose_graph.py why` (:1897-1931); `stage_prior_art.py` (never blocks); `system_map.py` (on demand only, `ecosystem/harness.yaml:172`).
- Verdict machinery: `decide_checks.py` gates matrix/evaluator/response artefacts but calls no model and emits no AGREE/AMEND/DISAGREE.
- Kill + verify organs: `scripts/hooks/bounded_hook.py:309-347` (psutil tree kill, POSIX killpg); `scripts/resource_lifecycle.py` (QR-AVAIL-005, test `test_qr_avail_005_a_surviving_grandchild_is_refused`); `scripts/read_gate.py:171-195` (quote verification).
- Receipts: `scripts/dodo.py:243-256` - fresh = status ok AND exit_code 0 AND input hash; `ecosystem/schema/lane_report.py` (pydantic pattern); pydantic `pyproject.toml:36`, psutil `pyproject.toml:135`.

## Objections that held (evaluator ids)
- X-I4-2/X-I4-3/X-I8-4: payload-only completion accepts stale or prewritten payloads. Held - but exit cannot be required either (`copilot.exe` may never exit, LANE-END codespace G2). Synthesis below.
- X-I8-3: mandatory other-vendor confirmation makes the gate depend on a vendor being up. Held - fail closed to INPUT_REQUIRED, with the registry's review chain as fallback.
- X-I4-1/X-I8-1: build no parallel mapper - compose the existing organs. Held (the AMEND already says reuse first).

Weights: unattended=20 code=15 libfirst=15 modelagnostic=15 osagnostic=10 tokens=10 testable=10 simplicity=5
| Option | unattended | code | libfirst | modelagnostic | osagnostic | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A. new distiller tool + new receipts + payload-only completion | 3 | 4[^1] | 2 | 3 | 3 | 2 | 3 | 1 | 2.80 |
| B. extend distill + compose organs + fresh-payload completion | 3 | 4[^1] | 4[^2] | 3 | 3 | 3 | 4[^3] | 3 | 3.40 |
| C. status quo (spine stages 2/6 only) | 2 | 3 | 4[^2] | 3 | 3 | 3 | 3 | 4[^4] | 3.00 |

[^1]: measured -- pydantic is a direct dependency, pyproject.toml:36; LaneReport pattern ecosystem/schema/lane_report.py
[^2]: measured -- gen_lane_contract.py:2227-2294, bounded_hook.py:309-347, read_gate.py:171-195, decide_checks.py read 2026-10-15
[^3]: measured -- tests/ carry test_qr_avail_005_a_surviving_grandchild_is_refused (ARCHITECTURE.md:226) for the reused kill
[^4]: measured -- no change; harness.yaml stages 2 and 6 run today (S2 research)

## Pre-mortem
- B's CHALLENGE stage is an LLM judgement wrapped in code: it can be gamed by a vague input. The code part is the gate (receipt schema, evidence count, matrix rule via `decide_checks.check_matrix`, vendor != producer via the launched argv), not the prose.
- Fresh-payload completion can still accept a payload the vendor wrote from a wrong input; the nonce + input hash bind it to this spawn.

## Verdict: AMEND (intent of R114 kept: front-stage distiller, anti-duplication, CC-owned processes)
1. **Distiller = `gen_lane_contract.py distill` extended**, reading `tasks/<id>` (R106) instead of BUILD-LIST, and adding `reuse_candidates[]` from `file_purpose_graph.py why` + `ecosystem/organ-index.md` + the skills/commands index. DistillReceipt = pydantic beside `ecosystem/schema/lane_report.py`.
2. **NEW-JUSTIFIED** is checked in code: a plan naming a new path while a candidate scores above threshold exits 1 unless the receipt carries a NEW-JUSTIFIED reason AND a ChallengeReceipt from a non-producer vendor.
3. **CHALLENGE** reuses `decide_checks.check_matrix` (no 4-5 without a measured citation) and `check_evaluator_attestation` (vendor != producer). Reviewer chain = registry `review` order; none available = INPUT_REQUIRED (fail closed). AGREE/AMEND/DISAGREE are written as ChallengeReceipt.verdict; DISAGREE halts at `INPUT_REQUIRED`.
4. **Point-task completion = a payload that is schema-valid, carries the spawn's nonce and input hash, and has mtime after spawn**; then the tree is killed with the existing psutil kill (`bounded_hook`/`resource_lifecycle`, not a new one). Exit code is recorded, not required. No valid payload by timeout = FAILED + tree kill.
