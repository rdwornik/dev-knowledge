# ADR-93: Floor provisioning model A — commit + hash-guard the methodology floor

<!-- scope: meta -->

**Status:** Accepted (ratified by merge; authored DURING the #226(b) build so it records the *implemented* mechanism, not a pre-image)
**Date:** 2026-07-01
**Decision tier:** Doctrine (how the ADR-78 methodology floor is *provisioned + armed* in a consumer — the missing half of "the floor is deployed"). Model A itself was decided at #226(a); this ADR formalizes the mechanism the build implemented.
**Related:** ADR-78 (child methodology floor — D2 "children commit their own floor", D5 "child pre-commit hook verifies the sidecar hash"); ADR-92 (deploy-runbook doctrine — the write-yes/commit-no/autonomy-no boundary + the accidental-drift threat model); ADR-73 (per-repo orchestration distribution — hub-canonical); ADR-91 (corpus versioning); ADR-88 (do-not-build-is-doctrine). Supersedes the "local-only" framing in `protocols/PLAYBOOK.md` §20.
**Decommission:** none.
**Source:** the approved plan `cc-prompt-polished-lighthouse` (architect review 2026-07-01) + operator rulings on the three build forks (bootstrap warn-loud; precommit-owns-the-hook; fresh-clone isolation).

## Context

The ADR-91/92 deploy subsystem was built and proven on n=1 (ai-council → v1.0.0), but the floor it deployed was **configured, not armed**: `deploy/carrier_floor.py` dropped `.claude/CLAUDE-FLOOR.md` + its `.sha256` sidecar and stopped there. Nothing loaded the floor at session start and nothing blocked a drifting-floor commit — the six arming steps lived only as a printed manual runbook (`scripts/generate_floor.py` `INSTALL_NOTE`). ai-council's floor was even git-ignored (a bare `.claude/` line), so it would be absent on a fresh clone and the `@`-include would resolve to nothing.

Two provisioning models were on the table:
- **Model B — floor local-only** (generated per-deploy on disk, gitignored, never committed): rejected — it is exactly what *creates* the configured-not-armed facade (gitignored floor → absent on clone → broken `@`-include), and it leans on re-running the deploy on every consumer to stay current.
- **Model A — commit the floor + a hash-guard** (tracked, not gitignored): the hub pushes the canonical floor once; a fresh clone is armed at once; and the copy-drift #95 fears is **caught** by the guard rather than **avoided** by non-tracking.

ADR-92's threat model applies unchanged: the solo operator owns every repo and the agents in them are the operator's own sessions. The guard defends against **accidental drift**, not a malicious agent — "hard-to-bypass" means "won't silently miss drift," not adversary-proof.

## Decision

**Adopt model A: the consumer commits its methodology floor, and a two-leg hash-guard makes any drift loud.** ADR-78 D2 ("children commit their own floor") and D5 ("child pre-commit hook verifies the sidecar hash") already bless this; model A adds the session-start leg and the tracked-via-`.gitignore`-negation mechanism, and supersedes PLAYBOOK §20's contradictory "local-only".

1. **Committed + tracked floor.** The floor, sidecar, and the guard script live at `.claude/CLAUDE-FLOOR.md` / `.sha256` / `.claude/check_floor_hash.py`, made trackable by rewriting the consumer `.gitignore` from a bare `.claude/` to the contents-form `.claude/*` + `!`-negations (a bare directory exclusion defeats negations — git will not re-include a file under an excluded dir, #138). The hub template `templates/child-methodology-floor.md.tmpl` stays the **only authoritative source**; the committed consumer floor is a hash-guarded *replica*, not a rival source.

2. **Two-leg hash-guard, one canonical script.** Both legs run the single `.claude/check_floor_hash.py` (single-sourced from `generate_floor.CHECK_FLOOR_HASH_SCRIPT` — the paste-ready `INSTALL_NOTE` body — so the automated arm and the manual runbook can never disagree on the guard bytes). The legs:
   - **Session-start** — a `SessionStart` command hook in the committed `.claude/settings.json`. It travels with the clone (settings.json is tracked), fires every session, and is un-suppressible by `git commit --no-verify`. A plugin `hooks.json` SessionStart hook was rejected — it registers too late for the one-shot init event and never fires (verified 2026-06-02).
   - **Commit-time** — a `floor-hash-verify` local hook in `.pre-commit-config.yaml` that blocks a commit staging a drifted floor.

3. **The "zero manual steps on fresh clone" linchpin.** Git never lets `.git/hooks` travel with a clone, so the commit-time leg is irreducibly per-clone-armed. Resolution: the session-start hook does double duty — leg (a) runs the verify, leg (b) idempotently runs `python -m pre_commit install` to bootstrap the git hook. The first CC session auto-arms it. If `pre-commit` is absent in the environment the bootstrap **warns loud but does not fail the session** (operator ruling) — the independent session-start verify still runs every session, so integrity is never silently lost; only the commit-time convenience defers. No pip-install-at-session-start (non-deterministic, network-dependent, unneeded at n=1).

4. **Arming spans two carriers (single-writer-per-file).** `carrier_floor.apply` writes/stages the floor, sidecar, guard script, the `CLAUDE.md` `@`-include, the `.gitignore` negation block, and the `settings.json` SessionStart block. The **precommit carrier** owns the `.pre-commit-config.yaml` `floor-hash-verify` entry — it is the single writer of that file (the floor carrier writes the *script* the hook runs; the precommit carrier writes the *hook*). All writes stage only; the operator commits (ADR-92 commit-no).

5. **#230 is the acceptance metric, not files-present.** A conformance harness (`deploy/floor_conformance.py`) proves the loop *functions* end-to-end in an isolated fresh clone (own `.git`, plain-delete teardown — the operator-approved amendment of the acceptance-contract's "worktree file-disjointness"): clean floor passes both legs, a poisoned floor fails loud at both legs, the git hook auto-arms, and a real task flows branch → commit → gate → merge. #226 is DONE only when Layer-2 passes against the **real** ai-council (incl. the tamper leg) — a green Layer-1 synthetic fixture is CI regression, not closure.

## The hash-guard reservation (load-bearing)

The hash-guard is **load-bearing**: if it were weak — commit-only, silent, or trivially bypassed — model A would degrade into exactly the committed-copy-that-silently-drifts #95 fears. The whole safety of "commit the floor" rests on the guard firing at both legs, fail-loud, on accidental drift. This is the decision's central risk and the reason both legs (not just commit-time) exist, and the reason #230 proves the tamper is *caught* rather than asserting files are present. If the guard ever proves unbuildable or is materially weakened, reopen model B.

## Known limits (surfaced, not silently accepted)

- **Greenfield `settings.json` tracking.** The SessionStart hook lives in `.claude/settings.json`, but the model-A `.gitignore` negation block tracks only the floor, sidecar, and guard script — **not** `settings.json`. ai-council (the n=1 proving ground) already force-tracks its `settings.json`, so its self-arm holds. A *fully greenfield* consumer that gitignores `.claude/` with no pre-tracked `settings.json` would not carry the SessionStart hook on the next fresh clone → its session-start leg would not self-arm. Fleet rollout (#221) must either extend the negation block to `!.claude/settings.json` or force-track it per consumer. Recorded so the fleet does not inherit ai-council's accident as an assumption.
- **`--no-verify` and out-of-CC commits.** A `git commit --no-verify`, or a raw `git commit` in a clone never opened in CC, bypasses the commit-time leg. The session-start leg is the backstop (it catches the drift on the next session). Accepted per the accidental-drift threat model.

## Rejected alternatives

- **Model B — floor local-only / gitignored** (per-deploy on disk, never committed). Rejected — it manufactures the configured-not-armed facade; reopen only if the hash-guard proves unbuildable.
- **`@`-include alone as the guard.** The `@`-include *loads* the floor but never hashes it — a poisoned floor loads silently. Kept for its real job (loading); rejected as a guard.
- **Commit-time-only guard** (no session-start leg). Rejected — a floor can drift between commits, and a `--no-verify` commit would leave it unguarded until someone happens to touch the floor path; the session-start leg is the always-on backstop.
- **Plugin `hooks.json` SessionStart hook.** Rejected — dead on arrival (registers too late, never fires).
- **`carrier_floor` writing the pre-commit hook** (two carriers editing `.pre-commit-config.yaml`). Rejected in favor of single-writer-per-file: the precommit carrier owns that file.

## Consequences

- A fresh clone of an armed consumer self-arms with zero manual steps (the `@`-include auto-loads the floor; the SessionStart hook verifies it and bootstraps the commit-time gate).
- The deployed floor is a hash-guarded tracked replica — drift is caught, not avoided — so committing the floor is compatible with the #95 copy-drift invariant.
- Arming logic is split across two carriers by the single-writer-per-file rule; the #226(b) BACKLOG wording is reconciled to state the precommit carrier owns the `floor-hash-verify` write, so a later pass does not "fix" the code back to a literal reading.
- PLAYBOOK §20's "Floor semantics — local-only" is superseded by "tracked + hash-guarded (model A)"; the #95 invariant survives, reframed as *caught, not avoided*.
