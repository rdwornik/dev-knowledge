<!-- scope: llm -->
# Repo-onboarding runbook — bring a repo onto the universal methodology baseline

> Operator-run from a **trusted hub checkout** (ADR-92: write-yes / commit-no — the
> operator ratifies every consumer commit). Deploys the methodology into a consumer repo
> **and** verifies it conformed. Onboarding executes in each child's **dedicated chat**
> (ADR-41), never from a hub worktree; this doc is the sequence those arcs follow.
>
> **This runbook hosts BOTH halves of a split pair as DISTINCT sections that close on
> SEPARATE Done-whens — do not merge the ids:**
> - **#131** — the 6-layer *install sequence* (`## Install sequence`). Done when: the runbook
>   exists, lists all 6 layers in order, and has been piloted n=1 with the n=2 gate recorded.
> - **#215** — the *conformance-verify* half (`## Conformance verify`). Done when: one onboard
>   runbook + a conformance verification exist.
>
> Governing decisions: ADR-78 (child methodology floor), ADR-93 (floor provisioning model A
> — committed floor + two-leg hash-guard), ADR-92 (deploy-runbook doctrine), ADR-91
> (methodology corpus versioning).

## Prerequisites
- A clean hub checkout at the target methodology version (currently **v1.2.0**;
  `deploy/manifest-v1.2.0.yaml` is the authoritative carrier set).
- On PATH: `claude` CLI, `pre-commit`, and a `python` that imports `pre_commit`.
- The consumer working tree is **clean** (the deploy preflight aborts on a dirty tree).
- The consumer will be registered in the ecosystem at Layer 5 (below).
- Notation: `<consumer>` = the consumer repo's filesystem path; `<name>` = its short repo name.

---

## Install sequence (#131)
Six layers, in order. Each layer names its **deploy command** and its **verify command** —
no "then check it works" prose. Layers 1, 2, 4, and 5's writes are all driven by the single
deploy converge (`deploy/tool.py … --execute`); the per-layer verify commands prove each
landed.

Run an assess (read-only plan) first, then execute the converge:

```bash
# read-only: preflight + detect + print the plan (no writes)
python deploy/tool.py <consumer> --target 1.2.0
# apply every needing-apply carrier, verify each, stage the consumer + write the version
# record (destroy-confirm required before pruning any status:removed component)
python deploy/tool.py <consumer> --target 1.2.0 --execute
```

### 1. Floor (ADR-78 / ADR-93)
The `.claude/CLAUDE-FLOOR.md` baseline + its `.sha256` sidecar + the `check_floor_hash.py`
guard + a `CLAUDE.md` `@`-include, dropped by the **floor carrier** during the converge.

```bash
# verify: floor bytes hash to the corpus + F5 self-containment (hub-runnable, per consumer)
python scripts/audit.py repo <name> --repo-path <consumer>   # -> floor_integrity OK
# verify: the consumer-side guard (run INSIDE the consumer; travels with the clone)
python .claude/check_floor_hash.py --require-present          # -> PASS
```

### 2. Carriers
The remaining reconcilers the converge applies: **precommit** (`.pre-commit-config.yaml`),
**enforcement-mesh** (session-end backpressure + `canonical_freshness` gate + `/override`),
and **global-config** (Layer 4). "Carrier" = one deployment vector's detect/apply/verify
reconciler; the ordered set lives in the manifest `carriers:` block.

```bash
python scripts/audit.py health                               # -> hooks/organs healthy
python scripts/enforcement_coverage.py --consumer <consumer> --fire   # -> organs FIRE
```

### 3. Lifecycle command (tier1-lifecycle plugin, ADR-70)
The `/review-closures` + `/ship` commands + the session-end propose-closures Stop hook,
installed as a Claude Code plugin. `marketplace add` **must** precede `install` on a new
machine, or install fails "Plugin not found in marketplace".

```bash
claude plugin marketplace add <hub-path> --scope project
claude plugin install tier1-lifecycle@dev-knowledge-methodology --scope project
# verify: enabledPlugins carries the plugin, and the command resolves
#   .claude/settings.json -> "enabledPlugins": { "tier1-lifecycle@dev-knowledge-methodology": true }
#   /review-closures       -> resolves in a CC session
```
> Prerequisite before installing the plugin: gitignore `logs/PROPOSALS-*.md` (do NOT blanket-
> ignore `logs/` in a repo that tracks files there). Cache gotchas — `plugin update … --scope
> project` is the upgrade path; `marketplace update` alone does not refresh an unchanged version.

### 4. Review profile
The **global-config carrier** copies `codex/AGENTS.md` → `~/.codex/AGENTS.md` (the L0
reviewer surface). The per-repo agentic-review profile (which reviewer, what cadence — a
heterogeneous second reader; natives `/code-review` / `/simplify` first) is a recorded
per-repo decision, not a deployed artifact (ref #82).

```bash
# verify: the L0 reviewer config landed
test -f ~/.codex/AGENTS.md && echo "codex reviewer config present"
```

### 5. Ecosystem registration
The consumer joins the machine + human registries. Auditing the repo seeds its machine-
registry `state.yaml`; the deploy converge writes the durable version record; the human row
is hand-added.

```bash
python scripts/audit.py repo <name> --repo-path <consumer>   # seeds ecosystem/<name>/state.yaml (gitignored)
# add a row to ecosystem/REGISTRY.md: | <name> | <path> | <purpose> | registered · onboarded v1.2.0 |
# ecosystem/deployed-versions.yaml gets the deployed-corpus version (written by the converge)
python scripts/fleet_health.py                               # -> the repo appears in the roll-up
```

### 6. Re-anchor mechanic (SessionStart self-arm)
The floor's behavioral rule (re-read the floor before structural work) rides in the deployed
floor; the arming that makes it live is the SessionStart self-arm. `.git/hooks/` never travel
with a clone, so every fresh checkout must arm them once.

```bash
# open a Claude Code session in the consumer (SessionStart auto-arms) OR arm manually:
python -m pre_commit install -t pre-commit -t commit-msg -t pre-push
# verify: all three managed stages are installed + pre-commit-managed
ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push
python scripts/audit.py health                               # -> hooks_armed OK
# verify (amendment): the hook shim's INSTALL_PYTHON resolves to a python that imports
# pre_commit — a stale/foreign interpreter = armed-but-erroring hooks:
python -c "import pre_commit"                                # with the shim's interpreter -> no error
```

---

## Conformance verify (#215)
The prove-it-conformed half — DISTINCT from the install sequence (do not merge the ids).
Each row is **run X → expect Y**, naming a command. "Configured ≠ armed ≠ proven": presence
is not enforcement, so the last three rows exercise the organs actually firing.

```bash
python scripts/audit.py repo <name> --repo-path <consumer>
#   -> floor_integrity OK (floor bytes hash to corpus; F5 self-contained; no orphaned root floor)
python scripts/audit.py health
#   -> hooks_armed OK + reconciled_versions OK; exit 0
python .claude/check_floor_hash.py --require-present          # run inside the consumer
#   -> PASS (fails LOUD on a deleted-but-tracked floor)
python scripts/enforcement_coverage.py --consumer <consumer> --fire
#   -> the deployed mesh organs FIRE on a real branch->edit->commit arc (Informant fire_test)
PYTHONPATH=deploy python -m lived_sandbox.cli observe-arc --consumer <consumer>
#   -> per-component FIRED / ARMED-BUT-SKIPPED / EXPECTED-BUT-SILENT + coverage n-of-6 (exit 0/1/2)
python deploy/floor_conformance.py --consumer <consumer>
#   -> the armed loop FUNCTIONS end-to-end (guard fails loud both legs; git hook auto-arms;
#      a real task flows through the gate) — not merely files-present
python scripts/fleet_health.py
#   -> the consumer is registered and reachable in the fleet roll-up
```

**The two Done-whens** this doc satisfies separately:
- **#131** — runbook exists, 6 layers in order, piloted n=1 with the n=2 gate recorded. Pilots
  on record (per the 2026-07-08 fleet-consistency census): **ai-council = n=1**, **corp-monorepo
  = n=2**, both deployed v1.2.0 with all three hook stages armed and the floor hash intact.
- **#215** — one onboard runbook (this doc) + a conformance verification (the section above,
  dry-run runnable — see below) exist.

---

## Per-clone gotchas
Three failure modes the pilots surfaced. Each is mandatory, with its command/edit.

1. **`pre-commit install` is mandatory, arming ALL THREE stages.** `.git/hooks/` are untracked
   and never travel with a clone, so the floor hash-verify + `block-ff-push` are inert until
   armed. A bare `pre_commit install` arms the **pre-commit stage only** (the #275 defect);
   arm all three:
   ```bash
   python -m pre_commit install -t pre-commit -t commit-msg -t pre-push
   ```
   (A fresh consumer's `.pre-commit-config.yaml` carrying top-level
   `default_install_hook_types: [pre-commit, commit-msg, pre-push]` makes even a plain install
   arm all three — but an already-cloned checkout still needs the `-t` form once.)

2. **`.gitignore` floor negations must use the contents form.** The bare `.claude/` directory
   form defeats negations (git won't re-include files under an excluded directory, #138):
   ```
   .claude/*
   !.claude/CLAUDE-FLOOR.md
   !.claude/CLAUDE-FLOOR.md.sha256
   !.claude/check_floor_hash.py
   ```
   Verify: `git check-ignore .claude/CLAUDE-FLOOR.md` prints **nothing**.

3. **Delete any orphaned ROOT floor copy** on migration to `.claude/`. `floor_integrity` reads
   `.claude/` only, so a stray floor at repo-root is an invisible **vacuous PASS**:
   ```bash
   git rm CLAUDE-FLOOR.md CLAUDE-FLOOR.md.sha256 2>/dev/null   # if present at root
   python scripts/audit.py repo <name> --repo-path <consumer>  # re-verify floor_integrity
   ```

---

## Per-repo checklist (queue-only here; executes per-repo in Wave 1, ADR-41)
- **#281 — ai-council ADR-66 story-map convergence.** ai-council is the sole Track-X BACKLOG
  outlier (6/7 repos already on the story-map); #221's corp-monorepo deploy did not carry the
  story-map. Decide at onboarding: carry the ADR-66 story-map + `validate_backlog` convergence
  (Track-X → story-map, ADR-99 clause A), or accept Track-X as durable — record either.
  ```bash
  python scripts/validate_backlog.py    # after converging, the story-map schema passes
  ```
- **#282 — `.gitattributes` EOL-normalization parity.** Four consumers lack `.gitattributes`
  (ai-council, corp-ops, corp-sca-time-automation, demo-prep). Add the target shape and
  renormalize:
  ```
  * text=auto eol=lf
  *.ps1 text eol=crlf     # where PowerShell scripts are tracked
  ```
  ```bash
  git add --renormalize .
  ```

---

## Dry-run attestation (#215 acceptance)
The conformance-verify commands above are **runnable today, not aspirational** — dry-run
against the hub itself / the lived-sandbox at authoring time (see the arc's session record for
captured output): `scripts/audit.py health` runs GREEN (it is the live `audit-health` pre-commit
gate); `scripts/fleet_health.py` enumerates the registered fleet; the floor-conformance machinery
(`deploy/floor_conformance.py`) is exercised end-to-end by the hermetic conformance suite
(`tests/test_floor_conformance.py`, green — it arms a synthetic consumer with the real carriers
and drives both guard legs + the auto-arm + a real gated commit); `enforcement_coverage.py --fire`
and `lived_sandbox.cli observe-arc` are the Informant commands that measure a real consumer AS-IS.
The consumer-scoped `check_floor_hash.py` guard runs inside a deployed consumer (attested via the
conformance suite, which exercises it on a synthetic consumer).
