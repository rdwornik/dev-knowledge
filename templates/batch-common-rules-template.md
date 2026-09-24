<!-- scope: meta -->
<!--
  templates/batch-common-rules-template.md — the rules EVERY seat of a batch shares (dispatcher,
  integrator, every lane). The seat table is `protocols/HANDOFF_PROCESS.md` §1.

  DISTILLED, NOT INVENTED (LANE-5A-9, 2026-09-24). Each rule below was written into a dated order
  after a failure it closes was measured: `WAVE4B-COMMON-2026-09-22` (sync, purity, self-check,
  session-file name, no wake-ups) and the common rules inside `BATCH-WAVE5A-2026-09-23` (nobody
  waits, the pre-authorized rulings, record what served). A batch's dated rules file FILLS this
  in — it names the batch, its plan and any rule it adds — and does not restate these.

  ROUTING IS DATA. No model name is typed here: which provider and model serve which role is
  `ecosystem/provider-registry.yaml`. Commands come from `--help`, never from prose (ruling O-5).
  Replace every <angle-bracket> placeholder; delete this comment.
-->
carried-by: OPEN
lands-via: the lanes of batch <BATCH> and their receipts in to-browser/
date: <YYYY-MM-DD>
from: <architect seat slug>
plan: <to-cc/PLAN-...md §n> — the functional requirements live there, in ONE place; nothing here restates them

# BATCH <BATCH> — common rules

Read by every seat of the batch, first. Also binding: <any earlier common-rules file still in force>.

## 1. Nobody waits for the operator

- Never stop for an answer. Decide by your contract's **Value** line, record it in your session
  file as `DECIDED-BY-LANE: <question> -> <decision> (why)`, and carry on.
- If a step is impossible, do the rest and hand back **PARTIAL** with the reason.
- Write a `QUESTION-*.md` only for the morning; never block on it.
- An act that needs the operator (global config, a purchase, a ratification) is recorded as an
  `OPERATOR-ACTION: <act> (why)` line, never waited on.

## 2. Pre-authorized rulings (no one asks for these)

- (a) A new script organ may add one dated `fates:` line (`manual_until: <date>`).
- (b) A generated file in conflict is regenerated, never hand-merged.
- (c) A file at its byte budget (`CLAUDE.md`, `protocols/HANDOFF_BOOT.md`) takes new content by
  pointer, never by overflow.
- (d) A red already in the registry, or in the standing freeze, is not yours.
- (e) Fix a Codex review's P1 findings; record the rest.
- (f) Additive conflicts in list-shaped files (`harness.yaml` fates, registries) keep both entries.
- <batch-specific rulings, lettered on>

## 3. Sync, purity, self-check

- **Sync only from origin:** `git fetch origin`, then `git merge origin/main`. Never `git merge
  main` — worktrees share the local `main`, which may hold the integrator's unverified work.
- **Purity before handback:** `git log origin/main..HEAD` lists only your commits and merges of
  `origin/main`. Anything else: stop and write a QUESTION.
- **Self-check before handback:** `audit.py ship-gate` with no hard-fail your branch introduced,
  `audit.py health`, `tests/test_silent_rule_ratchet.py`, and your Codex review record citing its
  consumer (your row) inside the record.
- **Rows cite in-repo provenance** — an ADR or ruling under `docs/decisions/` or
  `protocols/STANDING_RULINGS.md`; a transport file may be cited only in addition.
- **Backward-compatible CLIs:** a script another organ calls keeps its flags and exit codes; new
  behaviour goes behind new flags.

## 4. Waiting and processes

- Wait with the Monitor tool, using an until-loop. A background poll can be reaped under memory
  pressure; if yours is, re-arm it yourself and note it.
- No cron, no scheduled wake-ups, no loops. Nothing of yours outlives your last message.
- Temporary files go under your job's tmp only.
- pytest workers: <through the memory gate | `-n <k>`>. The full suite runs once, at integration.

## 5. Record what served

Record the model that actually served each step you ran. A routed tool that did not answer is a
**SUBSTITUTION** — record it, never hide it. Routing: `ecosystem/provider-registry.yaml`.

## 6. Files

- Your session file is exactly `to-browser/SESSION-<worktree-slug>.md` — the lane-end hook finds
  your handback only there.
- Never write outside your worktree, your job tmp, or your own transport files.

## Handback (every lane)

In `to-browser/SESSION-<worktree-slug>.md`: what is now true that was not (with the command that
shows it), the value in one sentence, the self-check results, the purity output, the vacuity
check, every `DECIDED-BY-LANE` / `OPERATOR-ACTION` line, the model served per step, and last
`HANDBACK <branch> @ <sha> <code|docs>`. Confirm it on the transport.
