# CLOUD-W3PREP — win-tooling universalization recon

> Provenance: verbatim session result of the read-only cloud recon (Dispatch-Cloud, 2026-08-26),
> relayed to file by the browser architect for landing.

Mode: B — this session is bound to `.dev-knowledge` (git remote: rdwornik/dev-knowledge;
toplevel /home/user/dev-knowledge). win-tooling was NOT observed. Every claim about it below
is `hub-recorded, not observed` and carries the hub locator it came from.

FRESHNESS CEILING ON ALL WIN-TOOLING CLAIMS. Newest hub baseline for the repo is
`ecosystem/win-tooling/history/2026-07-31.md`; `ecosystem/index.yaml` stamps `last_audit:
'2026-08-05'`. Today is 2026-08-26 — 21 days stale. Worse, `[#463]`'s own body records
"51 further baseline commits (through 2026-08-01) exist LOCALLY ONLY — unpushed, unread".
The hub cannot see win-tooling's current state at all. Treat this report as a plan against a
21-day-old snapshot, not a measurement.

PREMISE CORRECTION (brief says `[#463]` is known open consumer debt).
`tasks/463-...md` frontmatter reads `status: closed`. It was closed BY RULING, not by fix:
`protocols/STANDING_RULINGS.md:2283` T-16 accepts all four items as consumer-repo debt
"the hub may surface but not close", and says in terms "This section accepts a REASON, not a
measurement." So the debt is live; the row is not. Wave 3 cannot reopen `[#463]` — it needs a
new row, which is what §5 proposes.

## 1. GAP MAP — eight organs
State is as-of the 2026-07-31 baseline unless noted.

|organ|state|evidence (hub locator)|
|---|---|---|
|backlog/tasks|PARTIAL|`BACKLOG.md` present (`canonical_md_visibility` pass, win-tooling history 2026-07-31). Engine is hub-bound: `audit.py:2508` returns n/a "hub-only — tasks/ is a hub-owned tree"; `scripts/gen_task_tree.py:96-99` binds `_REPO_ROOT` to its own `__file__`, so it can only generate its OWN BACKLOG. Schema unruled: `[#331]` open.|
|intake|LACKS|Carried by the `docs` carrier (`deploy/manifest-v1.4.0.yaml:373-386`) — but win-tooling has no deploy record, so nothing was carried. `check_intake_tree_coherence` is hub-only (`audit.py:2583`).|
|ADR log|UNKNOWN → hypothesis: absent|No hub surface records it. `check_adr38_baseline` covers the six canonical docs only (`scripts/audit_checks/check_adr38_baseline.py:35-39`), NOT `docs/decisions/`. Nothing else in the 2026-07-31 baseline reads an ADR tree. This is an evidence hole, not a finding.|
|gates/audit|LACKS locally, surfaced remotely|46 checks registered (`audit.py:3537` ALL_CHECKS, counted). 13 of them return n/a "hub-only" against win-tooling. The audit runs FROM the hub at a sibling path (`audit.py:526-531`), never inside the consumer. `enforcement_coverage` evidence: "win-tooling: session_end_backpressure=absent; canonical_freshness=absent".|
|LESSONS/JOURNAL|HAS FILES, discipline unverified|All seven canonical docs present + correctly cased (`canonical_md_visibility` pass). But every discipline check — `journal_spine_anchor`, `journal_day_letters`, `doc_claims`, `git_backlog_drift` — is hub-only. Presence is all the hub knows.|
|branch grammar|LACKS|The grammar ships in the floor (`templates/child-methodology-floor.md.tmpl`, "Ship rule (branch → merge --no-ff)"). `floor_integrity` = n/a "no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor". COMPOUNDING: win-tooling has NO `origin` remote at all and 14 local-only branches (JOURNAL 2026-08-07(f)); operator ruled private-remote, execution owed and unlanded (`STANDING_RULINGS.md:635` G3).|
|pre-commit set|LACKS|`precommit` carrier (`manifest-v1.4.0.yaml:162-211`) would pin 4 hub hooks @ rev v1.4.0 from github.com/rdwornik/dev-knowledge + `floor-hash-verify` + `canonical_freshness`. Undeployed: win-tooling absent from `ecosystem/deployed-versions.yaml`.|
|uv/pyproject standards|LACKS, AND NO CARRIER EXISTS|ADR-106 toolchain is hub-local (`pyproject.toml:1-26`, `required-version = "==0.11.19"`). No manifest carrier ships pyproject / uv.lock / .python-version. `ecosystem/dependency-baseline.yaml` holds exactly ONE row (pytest-xdist) and is read only by `fleet_parity`, which is hub-only and skipped here.|

Live FAIL/WARN set (all four ruled-accepted at T-16, none fixed):
  dot_prefix_discipline FAIL — `config.yaml` not dot-prefixed (ADR-59)
  canonical_freshness   FAIL — VISION + ARCHITECTURE edited 2026-07-12, reviewed 2026-07-11
  workspace_settings    WARN — `.win-tooling.code-workspace` missing both sortOrder keys
  deployed_methodology_version WARN — absent from deployed-versions.yaml (ADR-91)

Structural status: `ecosystem/parity-surfaces.yaml:135` classes win-tooling `role: pre-deploy`,
so EVERY parity MUST row renders "skipped (pre-deploy)". It is in the fleet declaration and
outside the fleet's enforcement in one move.

## 2. INSTANTIATION ORDER
Governing constraint, not negotiable: ADR-41 / RULING-W. The hub MAY write into a consumer, and
the ONLY sanctioned shape is consumer worktree/branch → report (`protocols/ESSENTIALS.md:86`;
`protocols/PLAYBOOK.md:1389`). Plus mechanism-before-act (`PLAYBOOK.md:3913`): the authorizing
amendment lands before the write, never retroactively.

  step 0 [S, HUB, BLOCKING] Tag v1.4.0 — or re-point the target to v1.3.1.
         Without it `deploy/tool.py:271-275` hard-aborts preflight. See §3 B1.
  step 1 [S, CONSUMER] Give win-tooling a private `origin`. Already ruled (G3), unlanded.
         Unblocks: hub_hooks pull over https, cloud/CI sessions, and backup of 14 local-only
         branches. Nothing downstream is durable without it.
  step 2 [S, HUB] Add a win-tooling key (null) to `ecosystem/deployed-versions.yaml`.
         `deploy/tool.py:253-257` rejects an unregistered repo outright. Flips its
         parity role pre-deploy → consumer.
  step 3 [S, HUB] Rule its onboarding profile (full | floor-only) into
         `ecosystem/satellite-onboarding-rulings.yaml` — it has no entry (see §3 B9).
  step 4 [M, RULING-W ARC] Run `deploy <repo> --target …` assess, then `--execute`.
         ONE act delivers: the floor (branch grammar + session contract), the pre-commit set
         (4 hub hooks + floor-hash + canonical_freshness), the enforcement mesh
         (session_end_backpressure + canonical_freshness_gate + /override), the tier1 plugin
         (/ship, /review-closures, Stop hook), the intake area, INSTALL.md.
         ◀── FIRST SLICE. Steps 1–4 fit ONE session once step 0 is discharged.
  step 5 [S, RULING-W ARC] Clear the T-16 four: dot-prefix `config.yaml`, re-stamp VISION +
         ARCHITECTURE, add the two workspace sort keys. deployed_methodology_version clears
         itself at step 4. NOTE: workspace_settings cannot be closed BY DEPLOY — see §3 B6.
  step 6 [M] ADR log + intake practice. Intake arrives at step 4; the ADR log is hand-seeded
         from `templates/ADR-template.md` (no carrier).
  step 7 [L, BLOCKED — DO NOT ATTEMPT YET] Backlog engine (tasks/ + generator).
         Three independent blocks: generator is path-bound (gen_task_tree.py:96-99),
         `validate_backlog` is hardcoded (`[#294]`, deferred), consumer schema unruled
         (`[#331]`, open).
  step 8 [M] uv / pyproject / .python-version. No carrier exists; hand-work today.

FIRST-SLICE VALUE, stated concretely: win-tooling goes from "unonboarded, zero enforcing
organs" to floor + 6 pre-commit hooks + a Stop gate + /ship, and its parity role flips, which
turns on the parity rows that render "skipped (pre-deploy)" today. That is visible in one
`audit repo win-tooling` diff.

## 3. HUB-SIDE PREREQUISITES (file:line per blocker)
B1 [BLOCKER] v1.4.0 IS NOT TAGGED. `deploy/manifest-v1.4.0.yaml:62` declares
   `source_tag: v1.4.0`; `deploy/tool.py:271-275` aborts when the tag does not resolve.
   Observed on the remote (github list_tags, this session): v1.0.0, v1.2.0, v1.3.0, v1.3.1,
   archive/drafts-2026-07-07 — no v1.4.0, no v1.1.0. `git tag` in this clone returns 0 (clone
   artifact; the remote listing is the real evidence). Operator act — CC does not tag (ADR-91).
B2 [BLOCKER] win-tooling absent from the deploy registry. `deploy/tool.py:252-257` +
   `ecosystem/deployed-versions.yaml` (keys: .dev-knowledge, ai-council, corp-monorepo,
   corp-ops, corp-sca-time-automation — 5 of the 9 declared members).
B3 [BLOCKER for any non-operator-machine run] SIBLING-PATH ASSUMPTION, twice.
   `deploy/tool.py:207-214` — `return (hub_root.parent / repo).resolve()`.
   `scripts/audit.py:526-531` — `return Path(_REPO_ROOT).parent / repo_name`.
   Both assume the consumer is a filesystem sibling of the hub under `Dev/`. In THIS cloud
   session there is no sibling; neither instantiation nor measurement is reachable. If wave 3
   is meant to run anywhere but the operator's laptop, this is the first thing to fix.
B4 [BLOCKER for copy-and-configure] NO CARRIER SHIPS THE 7 CANONICAL DOCS. The `docs` carrier's
   entire payload is three source→path pairs (`deploy/manifest-v1.4.0.yaml:373-386`):
   docs/intake/README.md, templates/intake-template.md, plugins/tier1-lifecycle/INSTALL.md.
   And `templates/` has ARCHITECTURE / CLAUDE / CONTRIBUTING / JOURNAL / LESSONS / ADR /
   audit templates but NO VISION template and NO BACKLOG template (observed: `ls templates/`).
   Two of the seven mandatory docs have no skeleton anywhere. Hand-crafting, today.
B5 Carrier coverage is 6 carriers / 17 components (1 removed) — global-config, tier1-plugin,
   precommit, floor, enforcement-mesh, editor-config, docs. NOT covered by any carrier:
   the backlog engine, the ADR log, `audit.py` itself, the uv/pyproject standard. Four of the
   eight organs in §1 have no delivery vector at all.
B6 `editor-config` carrier is `implemented: false` (`deploy/manifest-v1.4.0.yaml:326-327`) —
   declaration-only. So the `workspace_settings` WARN is NOT deploy-closable; step 5 must
   hand-fix it.
B7 `scripts/seed_runbook.py` is not child-class-aware — `[#303]` open (P2/S); a literal seed
   creates a `docs/handoffs/` that ADR-60 forbids. `[#293]` (fan-out) is BLOCKED-ON-RULING
   behind it, after 7 consumer PRs were seeded and reverted in full.
B8 [DOC DEFECT — will mislead the wave-3 lane] `deploy/tool.py` lines 9 and 28 state the
   `--execute` path "is **C2b** — it is scaffolded as an explicit guard here, never
   implemented." That is FALSE at HEAD: `execute()` is implemented (tool.py:708ff) and wired
   at tool.py:1322. The module docstring is the first thing a lane reads. Cheap fix, high cost
   if left.
B9 No onboarding-profile ruling for win-tooling. `ecosystem/satellite-onboarding-rulings.yaml`
   carries four rulings (corp-ops, corp-sca-time-automation, life-architect, demo-prep);
   win-tooling AND terminal-setup are absent. Nothing says which gate set it should receive.

## 4. `instantiate-methodology <repo>` — NORTH STAR, RANKED BUILD LIST
What it must minimally do, and what exists:

  1  resolve the consumer root explicitly           MISSING   (B3 — sibling-derived today)
  2  preflight: manifest, tag, registry, clean tree EXISTS    (deploy/tool.py:233-283)
  3  self-register a new repo in deployed-versions  MISSING   (chicken-and-egg with #2)
  4  read the onboarding-profile ruling             DATA ONLY (rulings yaml + a read-only
                                                              validator; deploy never reads it)
  5  seed the 7 canonical docs from templates       PARTIAL   (5 of 7 templates; no carrier)
  6  apply the 6 carriers + verify                  EXISTS    (deploy/tool.py execute leg)
  7  seed the ADR log + intake area                 PARTIAL   (intake carried; ADR log not)
  8  seed uv / pyproject / .python-version          MISSING   (B5)
  9  seed tasks/ + the generator                    MISSING + BLOCKED ([#294], [#331])
  10 write the version record + stage the consumer  EXISTS    (execute's record leg)
  11 re-measure (audit repo + observe-arc)          EXISTS    (templates/consumer-onboarding-
                                                              runbook.md; deploy/lived_sandbox)
  12 enforce the RULING-W branch→report shape       MISSING as code (doctrine only,
                                                              ESSENTIALS.md:86)

RANKED BUILD ORDER (each unblocks the next):
  1st  B3 — de-hardcode consumer-root resolution in deploy/tool.py + audit.py
  2nd  B1 + B2 — tag, and register the repo (operator acts, cheap, gate everything)
  3rd  B4 — extend the docs carrier to a canonical-doc seed set; author VISION + BACKLOG templates
  4th  #4 — make deploy read the profile ruling instead of ignoring it
  5th  #12 — RULING-W branch mode inside the tool, so the shape is enforced not remembered
  6th  #8 — a uv/pyproject carrier
  7th  #9 — the backlog-engine carrier, LAST, and only after [#294] and [#331]
The verb is a THIN COMPOSITION over organs that mostly exist. Items 2, 6, 10, 11 are already
built and proven at n=1 (ai-council). The missing half is path-portability and the canonical-doc
seed — not orchestration.

## 5. PROPOSED ROWS FOR ARCHITECT ADJUDICATION (6)
Checked against the open backlog first. Deliberately NOT proposed because the hub already owns
them: [#294] validate_backlog de-hardcode (deferred) · [#331] consumer BACKLOG schema ruling
(open) · [#303] seed_runbook child-class-awareness (open) · [#293] runbook fan-out (blocked) ·
[#305] verify-only re-run mode (deferred) · [#332] fleet dependency parity (open) · [#215]
onboard+verify in a new repo (closed) · the private remote (ruled at G3, owed to win-tooling's
own S-list, not hub work).

W3-1 · Tag v1.4.0 or re-point the deployable target to v1.3.1
      done-when: `deploy <repo> --target v1.4.0` clears preflight, or manifest-v1.4.0 is
      recorded undeployable and v1.3.1 named the wave-3 target in the lane contract
      size: S   dependency: none (operator act — CC does not tag, ADR-91)

W3-2 · Admit win-tooling (and terminal-setup) to the deploy registry + rule their profiles
      done-when: both carry a null-valued key in ecosystem/deployed-versions.yaml AND an entry
      in ecosystem/satellite-onboarding-rulings.yaml naming full|floor-only with ruled_by/date
      size: S   dependency: none

W3-3 · De-hardcode consumer-root resolution in deploy/tool.py and audit.py
      done-when: both accept an explicit consumer root (sibling remains the default fallback),
      a test proves a non-sibling layout resolves, and `audit repo <name>` runs from a checkout
      with no sibling tree
      size: M   dependency: none. ARCHITECT DECISION OWED: this is the same defect class as
      [#294] in a different module — fold, or keep separate?

W3-4 · Extend the docs carrier to the canonical-doc seed set; author the two missing templates
      done-when: templates/ carries a VISION and a BACKLOG template, and the docs carrier's
      doc_paths seed a greenfield consumer's 7 canonical docs without hand-copying
      size: M   dependency: W3-1 (a carrier change is a release act)

W3-5 · `instantiate-methodology <repo>` as a thin composition over existing organs
      done-when: one command runs preflight → profile-read → canonical seed → carriers →
      record → re-measure, in the RULING-W branch→report shape, proven on ONE repo
      size: L   dependency: W3-3, W3-4. OVERLAP TO ADJUDICATE: [#559] (dev-knowledge-kernel as
      an installable package) is an adjacent answer to the same portability problem — the
      architect should rule whether this row rides that arc or precedes it.

W3-6 · The win-tooling instantiation arc — the first slice, executed
      done-when: `audit repo win-tooling` reports the floor present, the pre-commit set armed,
      role flipped pre-deploy → consumer, and a fresh baseline lands in
      ecosystem/win-tooling/history/ — run as a RULING-W consumer worktree → report
      size: L   dependency: W3-1, W3-2 (W3-3 only if run off the operator machine)

HYPOTHESES, labelled as required by the brief — not evidence:
 · win-tooling has no `docs/decisions/` ADR log (no hub surface records it either way — §1)
 · the four T-16 items are still live (unconfirmable: 51 baselines unpushed, per [#463])
 · win-tooling still has no `origin` (last observed 2026-08-07; G3 execution recorded as owed)
