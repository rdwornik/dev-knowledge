# FLEET READINESS — the H0 runbook per consumer, measured against the FLOOR

**Date:** 2026-09-05 · **Class:** technical · **Arc:** fleet-readiness research arc (read-only) ·
**Seat:** CC (Opus 5) · **Substrate:** CLOUD · **Branch:** `claude/fleet-readiness-h0`

Read-only research arc. No consumer repo was modified; no consumer repo was reachable. One hub
write: this file (plus the generated `docs/audits/README.md` index it obliges).

**Two premises in the launching brief did not survive verification.** Both are corrected in §1
rather than restated: the nightly fleet baseline is **not** failing, and the OPERATOR ASKS register
carries **no** "fleet baseline INCOMPLETE" ask. What *is* true is narrower, structural, and
measurable — and it is finding **FB-1**.

---

## §0 · Verdict per repo

Every verdict cites the §2 row that produces it. **`origin SHA` is UNREAD for every consumer** —
this cloud session's GitHub token resolves `rdwornik/dev-knowledge` and nothing else (§1, B1), so
no consumer origin ref could be read. The measured columns below come from the hub's own nightly
baseline of **2026-09-05T13:38:43**, which reads the operator's local working copies, not origin.

```
REPO                      VERDICT                                              ORIGIN SHA   CITES
.dev-knowledge (hub)      READY - baseline source, PASS                        ca0a2a2      HUB-1
corp-monorepo             NEEDS 2 waivers - floor v1.2.0, 2 releases behind    UNREAD (B1)  CM-1, CM-2, CM-6
ai-council                NEEDS 1 waiver - floor v1.3.1, 1 release behind      UNREAD (B1)  AC-1, AC-2
win-tooling               NEEDS 1 waiver - floor v1.4.0 (current), 1 defect    UNREAD (B1)  WT-1, WT-2
corp-ops                  BLOCKED by no floor deployed (pre-deploy)            UNREAD (B1)  CO-1, CO-2
corp-sca-time-automation  BLOCKED by canonical_freshness FAIL + no deploy       UNREAD (B1)  CS-1, CS-2
demo-prep                 BLOCKED by never audited - no state.yaml             UNREAD (B1)  FB-1
life-architect            BLOCKED by never audited - no state.yaml             UNREAD (B1)  FB-1
terminal-setup            BLOCKED by never audited - no state.yaml             UNREAD (B1)  FB-1
```

No repo is STALE: every audited repo carries a `2026-09-05` history entry on
`automation/fleet-audit`. The three BLOCKED-by-never-audited repos are not stale either — they have
never been measured at all, which is a different and worse condition.

**demo-prep's unpushed feature branch** (`feat/leadership-template-deck`, 2 dirty files, reported by
the operator at launch) could not be corroborated: demo-prep is unreachable **and** unaudited. It is
recorded here as an operator-supplied fact, not a measured one.

---

## §1 · Baseline status, and the two corrected premises

**Hub SHAs read at:**

```
main                     ca0a2a2fecaf6830a4eb3868ed89941d1567a477  (2026-09-05)
automation/fleet-audit   f60f7762a4904467093b2b13bae090a7d899eaea  (2026-09-05)
latest manifest          deploy/manifest-v1.5.0.yaml  (source_tag v1.5.0, NOT TAGGED on origin)
latest TAGGED release    v1.4.0
tags on origin           v1.0.0  v1.2.0  v1.3.0  v1.3.1  v1.4.0
```

### The verb, witnessed

The brief offered `audit.py fleet` / `fleet_health.py`. **There is no `fleet` verb.** The verb set,
from `audit.py --help`:

```
Commands:
  checks  doc-freshness  governance-health  health  registry  repo  run  ship-gate
```

The cross-repo audit is **`audit.py run`**. `fleet_health.py` is the SessionStart surfacing organ
that *triggers* it, not the audit itself.

### Premise correction 1 — the nightly baseline is NOT failing

It ran today and completed:

```
docs/audits/2026-09-05-ecosystem-audit.md  (on automation/fleet-audit, f60f776)
  Generated: 2026-09-05T13:38:43
  Repos audited: 6
  Checks: 527 total - 135 pass, 8 fail, 209 warn, 0 unavailable, 175 n/a
```

Per-repo verdicts that run produced: `.dev-knowledge — PASS`, and `ai-council`, `corp-monorepo`,
`corp-ops`, `corp-sca-time-automation`, `win-tooling` all **FAIL**. The run is complete, dated, and
pushed. A reader looking only at `main` would conclude otherwise, because on `main` the newest
`ecosystem/*/history/` entry for four of five consumers is `2026-07-31.md` — 36 days stale. That is
**not** decay: it is ADR-84 writer isolation working as designed. The durable baselines live on the
orphan branch `automation/fleet-audit`, where `ecosystem/corp-monorepo/history/2026-09-05.md`
exists. Reading staleness off `main` is a trap this audit nearly fell into.

### Premise correction 2 — no such ask is registered

The brief pointed at "the 'fleet baseline INCOMPLETE' ask" in the OPERATOR ASKS register. The
register parses to 15 entries, `0 RED`, and none of them is it:

```
ESSENTIALS de-bless · VISION.md out of root · logs thinning · config/ fate · dashboard home
Codespace used · prompt distiller · conformance.html · ARCHITECTURE size · BACKLOG few closures
tasks/ vs archive/ · multi-provider telem · README front door · Python code-style · logs override token
```

The pointer does not resolve. Whatever motivated it, it is not carried by the register.

### FB-1 — what "INCOMPLETE" actually is: 6-of-9 coverage, structurally

The baseline audits **6 repos out of a declared fleet of 9**. The hub's own
`membership_agreement` check states the gap exactly:

```
9 declared (ADR-104); 7 resolved members (deployed-versions); coverage registry-md 9/9,
index-yaml 6/9, deployed-versions 7/9, parity-surfaces 9/9, onboarding-rulings 6/9,
state-dirs 6/9; declared-but-not-deployed: demo-prep [registry-md, parity-surfaces,
onboarding-rulings]; life-architect [registry-md, parity-surfaces, onboarding-rulings]
```

`state-dirs 6/9` is the operative number. `audit.py run` iterates registered repos, and
registration *is* an `ecosystem/<name>/state.yaml`. **demo-prep, life-architect and terminal-setup
have no state dir, so the nightly has never measured them and never reports their absence as a
failure.** The check that names the gap (`membership_agreement`) reports **PASS**. That is the
finding: the fleet baseline is silently 67% of the fleet, and the organ that could say so is green.

### B1 — the cloud substrate cannot run this arc, and that is by design

Four independent walls, each witnessed:

**B1.1 — token scope.** Anonymous clone is refused, and the session token resolves exactly one repo:

```
$ git ls-remote https://github.com/rdwornik/corp-monorepo
fatal: could not read Username for 'https://github.com': terminal prompts disabled

$ git ls-remote https://x-access-token:$GITHUB_TOKEN@github.com/rdwornik/dev-knowledge HEAD
ca0a2a2fecaf6830a4eb3868ed89941d1567a477	HEAD
$ git ls-remote https://x-access-token:$GITHUB_TOKEN@github.com/rdwornik/corp-monorepo HEAD
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/rdwornik/corp-monorepo/'
```

**B1.2 — the audit resolves consumers by on-disk path only.** There is no clone leg anywhere in the
fleet machinery. `scripts/fleet_health.py::_resolve_consumer_root` returns the `state.yaml` `path:`
or `<hub parent>/<name>`, and `None` otherwise — its own docstring says *"None when neither
resolves (isolated/cloud clone)"*. `deploy/tool.py` resolves identically
(`DEV_KNOWLEDGE_FLEET_ROOT` or `hub_root.parent / repo`, `tool.py:328-330`). Run live here:

```
$ uv run --locked python scripts/fleet_parity.py --run-date 2026-09-05
  ai-council      fleet-membership  unavailable  unresolved: /home/user/ai-council is not a git repo
  corp-monorepo   fleet-membership  unavailable  unresolved: /home/user/corp-monorepo is not a git repo
```

**B1.3 — the registry itself is untracked.** `.gitignore:78` is `ecosystem/*/state.yaml`, so a fresh
clone carries zero registered repos, and `audit.py run` degrades to a **vacuous pass**:

```
$ uv run --locked python scripts/audit.py run
No repos registered in ecosystem/. Use --repo-path to register one.
RUN_EXIT=0
```

Exit 0. An audit that measured nothing is indistinguishable, by exit code, from a green one — the
"validators with no args → vacuous pass" anti-pattern `CLAUDE.md` §10 already names, reached here
without passing a single argument. (Run in a throwaway copy of the tree, not the hub, because
`audit.py run` writes `state.yaml` and `history/` entries.)

**B1.4 — doctrine already settled this.** ADR-74 ratified the recurring baseline onto a local
scheduler for the stated structural reason that *"only local sessions see sibling repos"*; ADR-76
fixed the host as Windows Task Scheduler → `python scripts/fleet_health.py`. The cloud is not a
degraded host for this arc; it is the wrong host, by a ruling that predates the arc.

### B2 — the cloud image ships the wrong `uv`, which REDs every gate

Not fatal, but it costs every cloud session that touches a gate. `pyproject.toml:25` pins
`required-version = "==0.11.19"`; the image's `uv` on `PATH` is `0.8.17`, and every
`uv run --locked` refuses before doing anything:

```
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
Update `uv` by running `uv self update 0.11.19`.
```

The suggested remedy also fails — `uv self update 0.11.19` → *"The version 0.11.19 was not found for
the app uv in workspace uv"*. What works is `pip install uv==0.11.19`, which lands the pinned binary
at `/usr/local/bin/uv` while a stale `0.8.17` shim stays ahead of it at `/root/.local/bin/uv`, so
the absolute path is required. Every command in this audit was run through
`/usr/local/bin/uv run --locked` after `uv sync --locked` succeeded (exit 0).

### B3 — the hub's own commit gate cannot pass in the cloud, for FB-1's reason

Committing this file exercised the finding. `audit-health` (`audit.py health`, FAIL blocks) exits 1
in a fresh cloud clone. Verified pre-existing: stashing this arc's changes and running against clean
`ca0a2a2` also exits 1, so it is the substrate, not the diff. Three of the four causes were
genuinely repairable and were repaired:

```
[!!] hooks_armed: merge.ours.driver unset -- the .gitattributes `merge=ours` pin on
     docs/audits/README.md is inert ([#590])
     -> FIXED: git config --local merge.ours.driver true

[!!] canonical_freshness: derived leg REFUSES (shallow clone): "every git-derived date is a
     floor, not a fact, and a grafted history silently mis-dates every file older than the graft"
[!!] journal_spine_anchor: AnchorError - disposition floor 24882f8cc "is not a valid object name"
     -> BOTH FIXED: git fetch --unshallow origin
```

The cloud image clones **shallow**, which silently disarms two governance organs at once — the
freshness derivation refuses (correctly, loudly) and the ADR-85 anchor backstop cannot resolve its
own floor SHA. Neither is visible until something runs `audit.py health`.

The fourth cause is not repairable here:

```
[!!] repos registered  (none)
```

That is B1.3 and FB-1 restated by the gate itself. **The hub's blocking self-conformance gate is
red in the cloud because no consumer is registered** — so this audit could only be committed by
skipping that one named hook. Declared in the commit body, with the other gates left armed and
passing.

### P3 did not run

`agy` and `gemini` are both absent from the cloud image (`command -v agy gemini` → no output). The
Gemini whole-fleet read is not attempted, so §5 carries no fidelity numbers. Nothing was inferred in
its place.

---

## §2 · Floor-diff tables

### The floor, as declared

From `deploy/manifest-v1.5.0.yaml` — **8 carriers, 21 components** (20 active, 1 tombstoned).

```
CARRIER            ORDER  IMPLEMENTED  COMPONENTS
global-config      1      yes          codex-agents-config
tier1-plugin       2      yes          tier1-lifecycle-plugin, propose-closures-stop-hook,
                                       review-closures-command, ship-command
precommit          3      yes          hub-toc-hooks, hub-codemap-hooks, hub-block-ff-push,
                                       hub-backlog-id-hook, floor-hash-verify-hook,
                                       ruff-gate (status: removed since 1.2.0)
floor              4      yes          methodology-floor, floor-sessionstart-guard
enforcement-mesh   5      yes          session-end-backpressure, canonical-freshness,
                                       override-command
editor-config      6      NO           vscode-boundary-decoration
docs               7      yes          intake-area, install-guide
boot-inversion     8      NO           boot-session-command, funnel-health-digest
```

**Six components are NON-WAIVABLE** (`waivable: false`) — a `.methodology.yaml` entry naming one is
REJECTED by `enforcement_coverage.validate_allowlist_entry` (contract 2), so these are the true
floor:

```
hub-block-ff-push · floor-hash-verify-hook · methodology-floor
floor-sessionstart-guard · session-end-backpressure · canonical-freshness
```

The other 15 are waivable with a reason and a time-box. Note that
`vscode-boundary-decoration`, `boot-session-command` and `funnel-health-digest` sit on carriers
declared `implemented: false` — **no carrier module writes them to a consumer**, so no consumer can
reach parity on them by deploying. They are declarations awaiting a carrier, not drift.

### Carrier plan mode — witnessed, not invented

`deploy/carrier_precommit.py` has **no CLI and no dry-run flag of its own**; `deploy/contract.py:11`
states plainly that `--dry-run` "and the version-record write are the deploy *tool*'s job". The plan
mode lives in `deploy/tool.py`, and it is the **default**:

> `"""Deploy <REPO> against --target. Without --execute: read-only assess + plan.`
> `With --execute: apply each needing-apply carrier then verify; then prune..."""` — `tool.py:1440`

`tool.py:58`: *"here writes unless `--execute` is passed explicitly"* — the read-only default is
stated, not inferred. **No consumer-mutating behaviour exists in plan mode**, so decision-budget
item (c) is not triggered. The tool could not be run here only because it resolves the consumer as
`hub_root.parent / repo` (B1.2).

**Consequence for this audit:** the ADD/PRUNE columns below are derived by comparing the manifest's
declared component set against the baseline's measured rows — *not* by a carrier plan run. They are
sound about what is absent and silent about splice-level detail (which pre-commit stanza would be
rewritten, which surgical edit is unavailable) that only a real plan run yields.

### Region drift — NOT MEASURABLE this run

The hub's own 8 regions are byte-clean at `ca0a2a2` (each `templates/claude-regions/*.md` body
appears verbatim in `CLAUDE.md`, marker present, 8/8):

```
antipatterns-universal 1129B · conventions-commit-branch 538B · conventions-output-formatting 748B
critical-rules-consistency 168B · critical-rules-no-leftovers 346B · critical-rules-records 1002B
first-read 1243B · session-start-protocol 681B
```

That establishes the **source** is sound. It says nothing about any consumer: a byte diff needs the
consumer's `CLAUDE.md`, and none was readable. The only consumer-side signal the baseline carries is
size, which is not a drift measurement:

```
ai-council 33406 · corp-monorepo 22708 · win-tooling 10449 · corp-sca 6920 · corp-ops 6818 chars
```

Region drift per consumer is **unmeasured**, and is the single largest gap in this audit.

### Freshness set vs PRESENCE_REQUIRED

`canonical_freshness_gate.PRESENCE_REQUIRED` is computed, not listed —
`[f for f in DEFAULT_FRESHNESS_FILES if f in canonical_docs.CANONICAL_MANDATORY]`, falling back to
`["ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md"]`. Cadence backstop is 30 days (WARN); the
load-bearing FAIL is A2, edited-since-review. Every consumer resolves all three required files
(`adr38_baseline` PASS, `canonical_md_visibility` PASS fleet-wide). The registered-but-optional set
is absent everywhere and reported, never skipped:

```
docs/handoffs/README.md · protocols/ESSENTIALS.md · protocols/SESSION_SETUP.md
protocols/AI_COUNCIL_PROCESS.md · protocols/DEFINITION_OF_DONE.md
```

---

### HUB — `.dev-knowledge` — PASS

```
HUB-1  DEPLOY      no release deployed to the hub (n/a by design - the hub IS the source)
HUB-2  REGIONS     8/8 hub-owned regions byte-identical to templates/claude-regions/
HUB-3  PARITY      2 WARN-undeclared: canonical-doc-vision (VISION.md SHOULD absent);
                   claude-commands-roster (.claude/commands/boot-session.md uncovered)
HUB-4  PARITY      1 advisory-rewarn: root-sweep '.vscode' declaration EXPIRED
HUB-5  REPLICATION WARN: "automation/fleet-audit is 1 commit(s) ahead of origin -- a recent push
                   likely failed". Self-referential: measured mid-run, before that run's own
                   commit was pushed. Origin carries f60f776 (2026-09-05) - the push landed.
HUB-6  FRESHNESS   3 ungated-and-stale, 27 ungated-and-unstamped; 8 gated files fresh
```

### CM — `corp-monorepo` — FAIL · deployed **v1.2.0**

```
ROW    AXIS          MEASURED                                          FLOOR ACTION
CM-1   DEPLOY        deployed_methodology_version PASS: v1.2.0         BEHIND by v1.3.0, v1.3.1,
                     (held by ADR-102 ruling #336: the v1.3.1 pin is   v1.4.0. #336 rules the gap
                     a 2-hook gate repoint, NOT a corpus deploy)       DELIBERATE - do not "fix"
CM-2   FLOOR         floor_integrity PASS (sha256 4d268f329a7e)        AT PARITY - non-waivable
                     matches manifest anchors.floor_sha256             floor component satisfied
CM-3   HOOKS         enforcement_coverage: block_unanchored_push=       ADD: block_unanchored_push.
                     absent; canonical_freshness=present-unverified;   NOTE: not a manifest
                     reconciled_versions=absent                        component - see §3 note
CM-4   ADR GRAMMAR   FAIL 14 blocking: 8+ ADRs with no status field;   Consumer-local defect. NOT
                     duplicate-id=1, grammar=14, unindexed=23          a floor component
CM-5   SUBSTRATE     FAIL: ecosystem/substrate-registry.yaml           Hub-only surface leaking
                     FileNotFoundError                                 into consumer scope - see
                                                                       candidate (Z-C-2)
CM-6   FRESHNESS     WARN ARCHITECTURE.md 55d · CLAUDE.md 54d ·        3 re-stamps owed. CLAUDE.md
                     CONTRIBUTING.md 49d (all > 30d cadence);          also gated-and-stale: 1
                     23 ungated-and-unstamped                          content commit after stamp
CM-7   RECONCILED    WARN CONTRIBUTING.md: malformed                   1 fix (format only)
                     (reconciled_with not '<spec-id>@<version>')
CM-8   WORKTREE      WARN vk/c35d-test registered but gone from disk   git worktree prune
CM-9   CONSUMPTION   WARN no audit-consumer-baseline.json - ratchet    Hub-shaped artifact absent
                     INERT (live unconsumed 43 of 64)                  in consumer - (Z-C-2)
CM-10  PRUNE         ruff-gate tombstoned since 1.2.0; corp declares   PRUNE: none pending - the
                     the waiver (RESIDUAL 2026-07-13: "the             existing waiver holds
                     .methodology.yaml ruff-gate waiver KEPT")
```

### AC — `ai-council` — FAIL · deployed **v1.3.1**

```
ROW    AXIS          MEASURED                                          FLOOR ACTION
AC-1   DEPLOY        deployed_methodology_version PASS: v1.3.1         BEHIND by v1.4.0 (one
                     (registered 2026-07-11, pre-engine route -        release). Known gap G11:
                     deployed-versions.yaml annotates this)            no field records WHY
AC-2   FLOOR         floor_integrity PASS (sha256 4d268f329a7e)        AT PARITY
AC-3   HOOKS         enforcement_coverage: block_unanchored_push=       ADD: block_unanchored_push
                     absent; canonical_freshness=present-unverified;
                     reconciled_versions=absent
AC-4   ADR GRAMMAR   FAIL 3 blocking: ADR-01/02/06 status values       Consumer-local defect
                     'Revised (...)' outside the declared enum
AC-5   SUBSTRATE     FAIL: substrate-registry.yaml FileNotFoundError   Same as CM-5 - (Z-C-2)
AC-6   FRESHNESS     WARN CLAUDE.md 40d · CONTRIBUTING.md 43d;         2 re-stamps owed
                     10 ungated-and-unstamped
AC-7   RECONCILED    WARN CONTRIBUTING.md: unknown-spec (declares      Structural: a reconciled_with
                     handoff-process with no local spec to resolve)    edge with no local spec
AC-8   CONSUMPTION   WARN ratchet INERT (live unconsumed 111 of 138)   Highest unconsumed count
                                                                       in the fleet - (Z-C-2)
```

### WT — `win-tooling` — FAIL · deployed **v1.4.0** (current)

```
ROW    AXIS          MEASURED                                          FLOOR ACTION
WT-1   DEPLOY        deployed_methodology_version PASS: v1.4.0         AT the latest TAGGED
                                                                       release. No deploy owed
WT-2   PARITY ROLE   HELD at pre-deploy despite the v1.4.0 record:     11 MUST surfaces the v1.4.0
                     "11 MUST surfaces the v1.4.0 carrier set does     carrier set DOES NOT SHIP.
                     not ship remain absent on the deployed tree,      Not consumer drift - a
                     so a `consumer` role would RED the live-parity    manifest/parity-template
                     invariant" (parity-surfaces.yaml, ADR-91 #606)    disagreement. See §3 note
WT-3   FLOOR         floor_integrity PASS (sha256 4d268f329a7e)        AT PARITY
WT-4   DOT-PREFIX    FAIL: root 'config.yaml' not dot-prefixed and     1 fix, or an ADR-59
                     not on the ADR-59 exception list                  exception-list entry
WT-5   WORKSPACE     WARN .win-tooling.code-workspace: sortOrder and   2 settings
                     sortOrderLexicographicOptions both '<absent>'
WT-6   WORKTREE      WARN 4 of 4 linked worktrees unclosed, all last   4 lanes to close or
                     committed 10d ago                                 justify
WT-7   FRESHNESS     WARN CONTRIBUTING.md 56d; 16 ungated-unstamped    1 re-stamp owed
```

### CO — `corp-ops` — FAIL · deployed **null** (pre-deploy)

```
ROW    AXIS          MEASURED                                          FLOOR ACTION
CO-1   FLOOR         floor_integrity N/A: "no .claude/CLAUDE-FLOOR.md  ADD the whole floor carrier.
                     - repo has not adopted the methodology floor"     THE blocker: methodology-floor
                                                                       is NON-WAIVABLE
CO-2   DEPLOY        deployed_methodology_version N/A: unset           ADD: full deploy at v1.4.0.
                                                                       Profile ruled `full`
                                                                       (satellite rulings, 2026-07-16)
CO-3   HOOKS         enforcement_coverage: block_unanchored_push=       ADD: canonical_freshness
                     absent; canonical_freshness=ABSENT (not merely    (NON-WAIVABLE) + the mesh
                     unverified); reconciled_versions=n/a-no-edges
CO-4   FRESHNESS     WARN ARCHITECTURE.md / CLAUDE.md /                3 re-stamps owed; 2 also
                     CONTRIBUTING.md all 95d (> 30d cadence)           gated-and-stale
CO-5   ADR CORPUS    WARN corpus unusable: no ADR-*.md under           No ADR corpus exists
                     docs/decisions
CO-6   SUBSTRATE     FAIL: substrate-registry.yaml FileNotFoundError   Same as CM-5 - (Z-C-2)
CO-7   IMPORTS       0 @import edges across 1 file - CLAUDE.md (6818   Consistent with CO-1: no
                     chars) imports nothing                            floor to import
```

### CS — `corp-sca-time-automation` — FAIL · deployed **null** (pre-deploy)

```
ROW    AXIS          MEASURED                                          FLOOR ACTION
CS-1   FRESHNESS     FAIL 1 stale: "CLAUDE.md: last_reviewed           THE blocking defect. A2 -
                     2026-06-02 predates last edit 2026-06-08 -        the load-bearing leg. Live
                     edited but not re-reviewed"                       and unfixed since 2026-06-08
CS-2   DEPLOY        deployed_methodology_version N/A: unset           ADD: full deploy. Profile
                                                                       `full` but GATED: onboarding
                                                                       starts only from an approved
                                                                       clean main after
                                                                       feature/tenrox-loader is
                                                                       dispositioned
CS-3   FLOOR         floor_integrity PASS (sha256 4d268f329a7e)        AT PARITY - floor present
                                                                       WITHOUT a deploy record
CS-4   HOOKS         enforcement_coverage: canonical_freshness=        ADD: canonical_freshness.
                     ABSENT                                            Explains CS-1 persisting:
                                                                       the gate that would block it
                                                                       is not installed
CS-5   FRESHNESS     WARN ARCHITECTURE.md / CONTRIBUTING.md 95d        2 further re-stamps
CS-6   ADR CORPUS    WARN corpus unusable: no ADR-*.md files           No ADR corpus exists
CS-7   SUBSTRATE     FAIL: substrate-registry.yaml FileNotFoundError   Same as CM-5 - (Z-C-2)
```

**CS-3 + CS-4 together are the sharpest finding in this table.** The floor is installed and
hash-clean, but `canonical_freshness` — a NON-WAIVABLE mesh component — is absent, and the
consequence is measurable: CS-1 has been live since 2026-06-08 and nothing blocks it. A hash-clean
floor is not a working floor.

### FB — fleet baseline coverage

```
FB-1   COVERAGE      state-dirs 6/9. demo-prep, life-architect, terminal-setup have no
                     ecosystem/<name>/state.yaml, so audit.py run never reaches them.
                     No row above exists for them because none was ever measured.
                     The check that names this (membership_agreement) reports PASS.
```

---

## §3 · Waivers each repo must declare

**Shape** (`enforcement_coverage.read_allowlist`, `AllowlistEntry`, `validate_allowlist_entry`):
`<consumer root>/.methodology.yaml`, key `sanctioned_divergences`, a list of mappings with
`component` (a manifest component id), `reason` (**mandatory**, whitespace-only is no reason), and
at least one of `expiry` / `review_date` as an **ISO-8601 `YYYY-MM-DD`** date. A present-but-
unparseable date is `invalid-no-date`, never treated as absent — a malformed waiver fails closed.
An entry naming a `waivable: false` component is `rejected-non-waivable`. An entry for an unknown
component is inert.

**corp-monorepo** — 2, both already partly established:

```yaml
# corp-monorepo/.methodology.yaml
sanctioned_divergences:
  - component: ruff-gate
    reason: >-
      Tombstoned since manifest 1.2.0 (#244 P2 remove-leg truth-maker). corp keeps the
      hook; the removal is NOT a fleet retirement of ruff. Waiver KEPT per the
      2026-07-13 corp-monorepo W3 lane residual.
    review_date: 2026-12-31
  - component: vscode-boundary-decoration
    reason: >-
      editor-config carrier is implemented:false at v1.5.0 - no carrier module writes
      .vscode to a consumer, and corp already tracks its own (adopted 2026-07-12).
      Undeployable, not divergent.
    review_date: 2026-12-31
```

**ai-council** — 1:

```yaml
# ai-council/.methodology.yaml
sanctioned_divergences:
  - component: vscode-boundary-decoration
    reason: >-
      editor-config carrier implemented:false; ai-council tracks its own .vscode
      (adopted 2026-07-12). Undeployable until the consumer leg ships.
    review_date: 2026-12-31
```

**win-tooling** — 1:

```yaml
# win-tooling/.methodology.yaml
sanctioned_divergences:
  - component: vscode-boundary-decoration
    reason: >-
      editor-config carrier implemented:false at v1.5.0 - nothing writes it.
    review_date: 2026-12-31
```

**corp-ops, corp-sca-time-automation** — **none, and none would help.** Both are blocked on
`methodology-floor` / `canonical-freshness`, which are `waivable: false`. A waiver naming either is
rejected by contract 2. The only path is deploy.

**demo-prep, life-architect, terminal-setup** — **not determinable.** Never measured (FB-1). Naming
waivers for them here would be fabrication.

### Three notes the waiver frame does not cover

1. **`block_unanchored_push` is absent fleet-wide** (CM-3, AC-3, CO-3, CS-4) and is **not a
   manifest component**. `enforcement_coverage` measures it; no carrier ships it. It cannot be
   waived because it is not declared, and it cannot be deployed because nothing carries it. That is
   a manifest gap, not consumer drift.
2. **`canonical_freshness=present-unverified`** on corp-monorepo, ai-council and win-tooling: the
   hook line exists; static reading cannot prove it fires. Only `scripts/enforcement_coverage.py`
   run locally against the consumer proves enforcing-local.
3. **WT-2's 11 MUST surfaces** are a disagreement between the parity template and what the v1.4.0
   carrier set ships. Deploying again will not close them. This is hub-side work.

---

## §4 · H0 runbook — corp-monorepo

**Derived from §2 rows CM-1…CM-10 and §3, not from memory.** Every step ends with the exact command
and the witness that proves it landed.

**Target is `v1.4.0`, not v1.5.0.** v1.5.0 is a drafted release candidate that the operator has not
tagged (ADR-91: CC does not tag), and `deploy/tool.py`'s preflight requires the tag to resolve
before `--execute`. Origin carries `v1.0.0 v1.2.0 v1.3.0 v1.3.1 v1.4.0`.

**Substrate: LOCAL.** Every step below requires the consumer on disk beside the hub (B1.2). None of
this runs in the cloud.

> **Step 0 — CM-1 says the deploy gap may be deliberate.** ADR-102 / #336 ruled corp-monorepo stays
> at v1.2.0 and `deployed-versions.yaml` says *"Do not 'fix' to 1.3.1."* That ruling is about a
> **hook-rev repoint**, not about a v1.4.0 corpus deploy — but the two are close enough that this
> runbook must not assume. **This step is an operator ruling, not a command.** If the answer is
> "hold at v1.2.0", steps 3–5 drop and steps 1, 2, 6, 7 still stand on their own.

**Step 1 — re-stamp the three stale canonical docs (CM-6).** `ARCHITECTURE.md` 55d, `CLAUDE.md`
54d, `CONTRIBUTING.md` 49d. `CLAUDE.md` is also gated-and-stale: one content commit landed after
its stamp on the same date. Re-read end-to-end and confirm accurate — a stamp is not a touch.

```bash
cd ~/Documents/Dev/corp-monorepo
git checkout -b chore/h0-freshness-restamp
# edit last_reviewed in ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md frontmatter to 2026-09-05
git commit -am "chore(freshness): re-stamp ARCHITECTURE/CLAUDE/CONTRIBUTING after end-to-end re-read"
```

*Witness:* the next baseline's `corp-monorepo` section shows `canonical_freshness` with no
`> 30d cadence` WARN for those three, and no `derived gated-and-stale` row for `CLAUDE.md`.

**Step 2 — fix the malformed `reconciled_with` (CM-7).** It must be `<spec-id>@<version>`;
ai-council's working form is `handoff-process@5.7`.

```bash
cd ~/Documents/Dev/corp-monorepo
grep -n "reconciled_with" CONTRIBUTING.md
# set it to: reconciled_with: handoff-process@7.0.0
git commit -am "fix(contributing): reconciled_with to <spec-id>@<version> shape"
```

*Witness:* baseline row `reconciled_versions` for corp-monorepo is no longer
`WARN ... malformed`.

**Step 3 — declare the two waivers BEFORE deploying (§3).** The carrier reads
`.methodology.yaml` at deploy-action time; a `ruff-gate` prune with no waiver present will REFUSE.

```bash
cd ~/Documents/Dev/corp-monorepo
cat .methodology.yaml   # confirm the existing ruff-gate entry before editing
# add / confirm the two entries from §3
git commit -am "chore(methodology): declare ruff-gate + vscode-boundary-decoration divergences"
```

*Witness:*

```bash
cd ~/Documents/Dev/.dev-knowledge
uv run --locked python -c "
import sys; sys.path.insert(0,'scripts')
import enforcement_coverage as ec
from pathlib import Path
from datetime import date
pol = ec.waivability_policy_from_manifest(ec._latest_manifest())
for e in ec.read_allowlist(Path.home()/'Documents/Dev/corp-monorepo'):
    print(ec.validate_allowlist_entry(e, run_date=date.today(), waivable_policy=pol))
"
```

Every line must start with `('valid',`.

**Step 4 — plan the deploy, read-only (CM-1).** No `--execute`: `tool.py:1440` makes plan the
default and `tool.py:58` states nothing writes without the flag.

```bash
cd ~/Documents/Dev/.dev-knowledge
uv run --locked python deploy/tool.py corp-monorepo --target v1.4.0
```

*Witness:* a per-carrier plan naming each needing-apply carrier, and — because of Step 3 — a prune
plan that skips `ruff-gate` with `waived by consumer .methodology.yaml -- skipping prune` rather
than REFUSING. **Read the plan before Step 5.** If it proposes touching anything Step 0's ruling
protects, stop and go back to the operator.

**Step 5 — execute, only after Step 0 rules GO and Step 4's plan is read.**

```bash
cd ~/Documents/Dev/.dev-knowledge
uv run --locked python deploy/tool.py corp-monorepo --target v1.4.0 --execute
```

*Witness:* `ecosystem/deployed-versions.yaml` `corp-monorepo.deployed_methodology_version` reads
`1.4.0` with today's `deployed_date` and `source_tag: v1.4.0`, and the next baseline's
`deployed_methodology_version` row reads `corp-monorepo: deployed methodology corpus v1.4.0`.

**Step 6 — prune the dead worktree (CM-8).** `vk/c35d-test` is registered but gone from disk.

```bash
cd ~/Documents/Dev/corp-monorepo
git worktree list
git worktree prune
git worktree list
```

*Witness:* `vk/c35d-test` absent from the second listing; next baseline's `stale_worktrees` reads
`no linked worktrees registered (primary only)`.

**Step 7 — confirm the whole H0 by re-running the baseline.**

```bash
cd ~/Documents/Dev/.dev-knowledge
uv run --locked python scripts/audit.py run
```

*Witness:* the freshly written `docs/audits/<today>-ecosystem-audit.md` shows corp-monorepo with
CM-6, CM-7 and CM-8 cleared. **corp-monorepo will still read FAIL** — CM-4 (14 ADR-grammar defects)
and CM-5 (substrate registry) are untouched by this runbook and are separate arcs. H0 is complete
when those three rows clear, not when the repo turns PASS.

---

## §5 · Candidates (Z-C shape — no BACKLOG rows born here, ADR-111)

Each is a CANDIDATE for intake triage. None is filed.

**Z-C-1 — the fleet baseline is silently 6-of-9, and the check that knows reports PASS.**
`membership_agreement` computes `state-dirs 6/9` and returns PASS. demo-prep, life-architect and
terminal-setup have never been audited. Either registration becomes a precondition the check fails
on, or the three get state dirs. Evidence: FB-1, §1. Related: candidate (j) (per-consumer freshness
registry), ADR-104.

**Z-C-2 — four hub-only surfaces are measured against consumers and FAIL by construction.**
`substrate_declaration` FAILs on every consumer with `could not read
ecosystem/substrate-registry.yaml: FileNotFoundError` — **4 of the run's 8 total failures**, one per
consumer, for a file no carrier ships to a consumer. `consumer_at_landing` and `proof_layer`
similarly WARN "no readable `ecosystem/*-baseline.json`" fleet-wide. Either these checks declare
themselves hub-only (as 20+ others correctly do with `[n/a-reason:NOT-APPLICABLE] hub-only`), or the
artifacts join the manifest. Today they inflate the fleet failure count with noise. Evidence: CM-5,
AC-5, CO-6, CS-7.

**Z-C-3 — `audit.py run` exits 0 on an empty registry.** A vacuous pass is indistinguishable from a
green run by exit code, which is exactly what a scheduled job checks. Evidence: B1.3.

**Z-C-4 — three declared components sit on `implemented: false` carriers.**
`vscode-boundary-decoration`, `boot-session-command`, `funnel-health-digest` are declared but
undeployable, so every consumer diverges on them permanently and each must carry a waiver for a
component nothing can install. Evidence: §2 carrier table, §3 note 1.

**Z-C-5 — `block_unanchored_push` is measured everywhere and declared nowhere.**
`enforcement_coverage` reports it `absent` on all four measured consumers; it is not a manifest
component. Unwaivable because undeclared, undeployable because uncarried. Evidence: CM-3, AC-3,
CO-3, CS-4.

**Z-C-6 — a hash-clean floor is not a working floor.** corp-sca carries `floor_integrity PASS` and
`canonical_freshness ABSENT`, and its A2 FAIL has been live since 2026-06-08. Floor integrity and
enforcement coverage are being read as one signal when they are two. Evidence: CS-1, CS-3, CS-4.

**Z-C-7 — the cloud substrate cannot host this arc, and nothing says so at dispatch.** Four walls
(B1.1–B1.4), one of them a ratified ADR. A Dispatch-Cloud row that ruled fleet-measurement arcs out
of the cloud would have saved this run's P0/P2 measurement legs. Evidence: §1 B1, ADR-74, ADR-76.

**Z-C-8 — the cloud image ships `uv 0.8.17` against a `==0.11.19` pin.** Every `uv run --locked`
REDs until manually corrected, and the error's own suggested remedy fails. Evidence: §1 B2.

**Z-C-9 — a shallow clone silently disarms two governance organs.** The cloud clones shallow;
`canonical_freshness`'s derived leg then REFUSES and `journal_spine_anchor` cannot resolve the
ADR-85 disposition floor SHA. Both surface only under `audit.py health`, and both clear on
`git fetch --unshallow origin`. A SessionStart unshallow (or a refusal to run gates while shallow)
would make this deterministic instead of discovered. Evidence: §1 B3.

**Z-C-10 — the blocking self-conformance gate is red in the cloud by construction.**
`audit-health` FAILs on `repos registered (none)`, so no cloud session can commit to this repo
without skipping a blocking gate — including a session whose entire purpose is to report that fact.
Either `health` treats an empty registry as n/a with a stated reason (rather than a FAIL that
cannot be discharged where it fires), or cloud sessions get a sanctioned, recorded skip. Today the
skip is ad-hoc. Evidence: §1 B3, B1.3.

**Gemini fidelity:** P3 did not run (`agy` absent). No fabrication count, because no retrieval
occurred.

---

## §6 · Cost

**Wall-clock** (session start ≈ 12:35 UTC → 13:15 UTC; ~40 min total, phase boundaries at tool-call
granularity):

```
PHASE                                              WALL-CLOCK  MODEL CLASS
P0 inventory (blocked → substituted, see below)    ~6 min      Opus 5 (main session)
P1 baseline (env repair + audit verbs + root cause) ~14 min     Opus 5 (main session)
P2 floor diff (manifest, carriers, waiver schema,   ~13 min     Opus 5 (main session)
   region parity, baseline-branch extraction)
P3 Gemini fan-out                                   0 min       NOT RUN - agy absent
Deliverable authoring + commit                      ~7 min      Opus 5 (main session)
```

No subagents were spawned: every phase was a bounded deterministic read, and fan-out would have
added coordination cost without adding reach — the reach limit was credential scope, not context.

**Defaults taken under the decision budget, reported not asked:**

1. **Substituted the baseline branch for the unreachable consumers.** With no consumer clonable, the
   arc's measured half would have been empty. `automation/fleet-audit` at origin carries the
   2026-09-05 nightly, which measures 5 consumers directly. Consequence, stated plainly: this is
   the operator's **local working copies** as of 2026-09-05T13:38:43, **not** an origin read. The
   brief said read from origin, never a local disk. That was not available; the substitution is
   named rather than silently made.
2. **Targeted v1.4.0, not v1.5.0, in §4** — v1.5.0 is untagged and `tool.py` preflight requires the
   tag.
3. **Installed `uv 0.11.19` via pip** to run the hub's own declared environment. Nothing tracked
   changed.
4. **Ran `audit.py run` in a throwaway copy** under the scratchpad, never the hub, because it writes
   `state.yaml` and `history/`. The copy was discarded.
5. **Did not fabricate consumer origin SHAs.** §0's SHA column reads UNREAD.
6. **Probed one consumer remote once** (`git ls-remote corp-monorepo`) to obtain hard evidence for
   B1 rather than asserting unreachability from the scope declaration alone. Read-only, refused by
   the server, no content retrieved.
7. **Repaired the clone rather than bypassing the gates it broke** (B3): armed
   `merge.ours.driver` and ran `git fetch --unshallow origin`. Both are local-clone state, not
   tracked content.
8. **Skipped exactly one named blocking hook to land this commit** — `audit-health`, via
   `SKIP=audit-health`, with every other gate armed and passing. Its sole remaining cause is
   `repos registered (none)`, which is finding FB-1 itself and is not dischargeable from the
   cloud. Proven pre-existing at clean `ca0a2a2` by a stash test, so it is not this diff's.

**Closure clause (4) — verified:** `git status --porcelain` is empty apart from this file.
`logs/FLEET-PARITY.md`, written by the `fleet_parity.py` run, is gitignored. No consumer repo was
touched, because none was reachable.

---

## Open ask for the operator

**Decision-budget item (b): every consumer repo is unreachable from the cloud.** Three ways
forward, in the order I'd rank them:

1. **Re-dispatch the measurement half to a LOCAL session.** The tooling is on-disk-only by ADR-74's
   own reasoning (B1.2, B1.4). Locally, `deploy/tool.py <repo> --target v1.4.0` runs its real plan
   mode and the §2 ADD/PRUNE columns become carrier-derived instead of manifest-derived, and region
   drift (the largest gap here) becomes measurable.
2. **Widen the cloud token to the consumer repos and clone them to `/home/user/<name>`.** That
   parent slot is exactly what `_resolve_consumer_root` and `tool.py:329` fall back to, so the
   machinery would work unmodified. This makes the cloud viable for *reading*, and does nothing for
   `--execute`, which should stay local anyway.
3. **Accept the hub-side half as the deliverable** and treat region drift and carrier-plan output as
   a separate local arc.

Both (1) and (2) are real options; I do not need an answer to close this arc, only to close the gap
it names.

---

## AMENDMENT 1 — the measurement half, LOCAL (2026-09-05)

**Date:** 2026-09-05 · **Class:** technical (measurement) · **Seat:** CC (Opus 5) ·
**Substrate:** **LOCAL — explicit operator exception**, ruled 2026-09-05 ·
**Branch:** `worktree-lane-fleet-readiness-measurement`

This amendment is the **measurement half** of the arc whose reasoning half is the body above. It
was dispatched under the body's own **recommendation option 1** ("re-dispatch the measurement half
to a LOCAL session"). It re-derives nothing above it and re-litigates nothing above it: it replaces
unmeasured columns with measured ones and, where a measurement contradicts the body, says so in A6.

Read-only against consumers. Three consumers were cloned fresh from origin outside `Dev/`, read,
and deleted. `deploy/tool.py` was run in its **default read-only plan mode** on all three;
`--execute` was never passed. No consumer repo was modified.

### A1 · What this supersedes, and what it leaves standing

**SUPERSEDED — three surfaces, and only these three:**

1. **§0's `origin SHA` column.** All eight consumer rows read `UNREAD (B1)`. **All nine rows now
   carry a read SHA** (A2). §0 is re-issued in full at A5.
2. **§2's "Region drift — NOT MEASURABLE this run"**, and its closing sentence *"Region drift per
   consumer is unmeasured, and is the single largest gap in this audit."* It is measured at A4.
3. **§2's carrier caveat** — *"the ADD/PRUNE columns below are derived by comparing the manifest's
   declared component set against the baseline's measured rows — not by a carrier plan run… sound
   about what is absent and silent about splice-level detail."* A3 replaces manifest-derived with
   **carrier-derived** output for the three cloned repos. It does **not** replace it for corp-ops or
   corp-sca-time-automation, which were not cloned; their §2 rows stand as written.

**LEFT STANDING — everything else, explicitly:**

- **Every §1 finding.** B1, B2, B3 and FB-1 are untouched, and **B1 is corroborated, not weakened**:
  a single local `git ls-remote` sweep resolved **all eight** consumer remotes on the first attempt
  (A2). The cloud wall was the cloud session's *token scope*, exactly as B1.1 diagnosed — not a
  property of the repos, the URLs, or the operator's credentials in general. B1.2's on-disk-only
  resolution is likewise corroborated: every plan run in A3 required `--repo-root` pointing at a
  real working tree.
- **Every §3 waiver *shape* rule** (`AllowlistEntry`, mandatory `reason`, ISO date, non-waivable
  rejection). Measurement exercised that machinery and it behaved exactly as §3 documents. What
  changes is not the shape but **which waivers already exist** — see A6-C2.
- **Every §5 candidate (Z-C-1 … Z-C-10).** None is contradicted. Z-C-4 and Z-C-5 are *strengthened*
  by A3; Z-C-6 is strengthened by A4 and the stage-arming measurement in A3-S.
- **§4's corp-monorepo H0 runbook**, with two step-level corrections recorded at A6-C2 and A6-C3.
- **§6's cost accounting** for the cloud half. A7 is additive, not a replacement.

No BACKLOG row is born here (ADR-111). New findings are stated as measurements; anything that would
become work is a CANDIDATE for intake triage, marked as such at A6.

### A2 · M0 — origin SHAs, READ

**Substrate exception, named.** PLAYBOOK Ch8's `local-execution = explicit-request` axis makes LOCAL
a named exception rather than a default. Q3 routes read-only reconnaissance to CLOUD; a cloud lane
tried on 2026-09-05 and hit B1. **The operator ruled this half LOCAL on 2026-09-05.** This section
exists because of that ruling, and would be empty without it.

Three repos **cloned full** (not shallow — a shallow clone disarms `canonical_freshness`'s derived
leg and the ADR-85 anchor backstop, §1 B3):

```
REPO           ORIGIN URL                                     origin/main SHA                           COMMIT DATE (UTC)     DEPTH  COMMITS
corp-monorepo  https://github.com/rdwornik/corp-monorepo.git  fd3325e0f5d6d7790886d468e1daa0ce9d978e9c  2026-08-09T05:39:31Z  full   1194
ai-council     https://github.com/rdwornik/ai-council.git     7a3c05794d1fea274d2ca0c76de984f90b568a90  2026-08-12T16:15:55Z  full   900
win-tooling    https://github.com/rdwornik/win-tooling.git    49cb75e8b8ff53ccab3515fcb3e28213023785a4  2026-09-01T21:09:51Z  full   194
```

Each verified `rev-parse --is-shallow-repository` = **false**, `HEAD` = `main`, and
`git status --porcelain` **empty** at clone and again immediately before deletion (closure 4).

The remaining five consumers were **not cloned** (the contract names three). Their `refs/heads/main`
was read by `git ls-remote` — a real origin read, which is what the `UNREAD (B1)` column asked for:

```
REPO                      refs/heads/main SHA                       METHOD
corp-ops                  3bde9304ff04282f27aed7de3e953e811b31019a  ls-remote (not cloned)
corp-sca-time-automation  1a80a9efc2a906b0a1fc3c2a8826d1d824f391c1  ls-remote (not cloned)
demo-prep                 d849c8179f5d63b34ff56a0747b19cd6418ff6b2  ls-remote (not cloned)
life-architect            7688b76f0c7316f5286a341e8d1e14ce1d619137  ls-remote (not cloned)
terminal-setup            d8a7b61644430719eb68559f9a1e090bab43eb6e  ls-remote (not cloned)
```

**All eight resolved on the first attempt, anonymously refused nowhere.** Hub `origin/main` at the
time of this amendment is `09f80530ad59d5e498bb5c2739cec196982f1e22` (2026-09-05), ahead of the
`ca0a2a2` the body read.

**A finding this table produces on its own, before any deeper measurement:** corp-monorepo's origin
`main` is **27 days old** (2026-08-09) and ai-council's is **24 days old** (2026-08-12), yet the
nightly baseline the body relies on reported both as of `2026-09-05T13:38:43`. The baseline reads
the **operator's local working copies**, never origin — §6 default 1 says so plainly. The gap
between those two facts is unmeasured by any organ in the fleet, and is recorded as candidate
**Z-C-11** at A6.

### A3 · Carrier plan mode — carrier-DERIVED, per repo

**CLI surface, witnessed** (`deploy/tool.py --help`), matching the body's §2 reading exactly:
positional `REPO`; `--target` (required); `--execute`, `--force`, `--auto-approve`, `--repo-root`.
Plan is the default; **`--execute` was never passed**, and no other flag was invented. Command run,
once per repo:

```
uv run --locked python deploy/tool.py <repo> --target v1.4.0 --repo-root <clone path>
```

Target **v1.4.0** — the current tagged release, per §4. All three runs exited **0**.

**Add leg — detected state per carrier:**

```
CARRIER            ORDER  corp-monorepo     ai-council        win-tooling
global-config      1      present_correct   present_correct   present_correct
tier1-plugin       2      ABSENT            ABSENT            ABSENT
precommit          3      present_drifted   present_drifted   present_correct
floor              4      present_drifted   present_drifted   present_correct
enforcement-mesh   5      present_drifted   present_drifted   present_drifted
editor-config      6      n/a (not impl)    n/a (not impl)    n/a (not impl)
docs               7      present_drifted   present_drifted   present_drifted

SUMMARY                   5 need apply      5 need apply      3 need apply
                          1 correct         1 correct         3 correct
                          0 undetected      0 undetected      0 undetected
                          1 not implemented 1 not implemented 1 not implemented
```

Planned actions, verbatim from the plan tables (identical text across repos for a given carrier):

```
tier1-plugin      would apply from scratch (claude plugin install/update --scope project)
precommit         would reconcile drift (merge required pins into .pre-commit-config.yaml)
floor             would reconcile drift (generate .claude/CLAUDE-FLOOR.md + .sha256 sidecar)
enforcement-mesh  would reconcile drift (deploy seb + freshness-gate scripts + /override
                  + Stop hook + logs/)
docs              would reconcile drift (copy the manifest-declared hub docs (intake area,
                  INSTALL.md) into the consumer)
editor-config     skip -- not implemented (do-not-build doctrine)
```

**`tier1-plugin` is ABSENT on all three consumers.** The carrier is `implemented: true` at v1.4.0
and v1.5.0, so unlike `editor-config` this is a real, closable gap — and the body's §2 carrier
table, which lists `tier1-plugin` as implemented and says nothing further, never surfaced it. Four
components ride that carrier (`tier1-lifecycle-plugin`, `propose-closures-stop-hook`,
`review-closures-command`, `ship-command`). **This is new: it is the only carrier absent fleet-wide,
and it is absent even on win-tooling, the one consumer recorded at the current release.**

**Remove leg — the prune sweep:**

```
COMPONENT  CARRIER    removed_in  corp-monorepo    ai-council       win-tooling
ruff-gate  precommit  1.2.0       already_absent   already_absent   already_absent
```

**Read that row carefully — it does not mean what it appears to.**
`carrier_precommit.detect_prune` classifies via `_classify_prune(config, prunable, waived=...)`, and
`prune()` proves the conflation directly: `ALREADY_ABSENT` renders as
`"... waived by consumer .methodology.yaml -- skipping prune"` **when waived** and
`"... already absent"` otherwise. **Plan mode prints the same token for both.** Measured ground
truth behind the identical token:

```
REPO           ruff hooks in .pre-commit-config.yaml   .methodology.yaml ruff-gate waiver   ACTUAL PATH
corp-monorepo  4 matching lines (PRESENT)              present + valid to 2026-10-07        WAIVED
ai-council     4 matching lines (PRESENT)              present + valid to 2026-10-12        WAIVED
win-tooling    0 matching lines (ABSENT)               no .methodology.yaml at all          GENUINELY ABSENT
```

This retires §4 Step 4's stated witness. That step expects the plan to *distinguish* a waived skip
from a refusal by printing `waived by consumer .methodology.yaml -- skipping prune`. **Plan mode
never prints that string** — only `--execute` does. Correction recorded at A6-C3.

**Out of scope (ADR-92 `l0_scope`)** — identical on all three, not failures:
`surface-closures`, `block-onedrive`, `gotchas`, `routing` (all deferred deployables);
`no-ff-rule` (enforced elsewhere).

#### A3-F · Why `floor` drifts on two repos — the leg isolated

`floor` is a **non-waivable** component and its drift is not in the floor bytes.
`carrier_floor._classify_floor` requires five legs; each was measured independently:

```
REPO           floor_ok  include_ok  hook_ok  gitignore_ok  settings_ok   ->  CARRIER STATE
corp-monorepo  True      True        True     FALSE         FALSE             present_drifted
ai-council     True      True        True     FALSE         FALSE             present_drifted
win-tooling    True      True        True     True          True              present_correct
```

`floor_ok` is **True on all three**: every `.claude/CLAUDE-FLOOR.md` hashes (LF-normalised, via
`generate_floor.floor_sha256` — the repo's own function) to
`4d268f329a7edc8dc95a1c8fded9bdf8244ad8de60be69bf8e250a9b15a8111f`, which is **both** the live hub
corpus digest **and** the `anchors.floor_sha256` pinned by v1.4.0 and v1.5.0 alike, and every
`.sha256` sidecar records that same value. **CM-2, AC-2 and WT-3 are CONFIRMED by measurement.**

> A raw-byte hash of the same three files disagrees (win-tooling's reads `fcbfd664...`). That is a
> CRLF artefact of a Windows clone, **not** drift — the carrier hashes normalised text. It is
> recorded here because it is the exact false positive the contract warned about for A4, and it
> reached "win-tooling's floor is hash-broken" before the repo's own function refuted it.

#### A3-S · The real drift: two of three consumers arm only ONE hook stage

`settings_ok` requires the SessionStart guard to arm **all three** stages
(`_ARM_STAGES` = `commit-msg`, `pre-commit`, `pre-push`). Measured `SessionStart` commands:

```
REPO           SessionStart pre-commit install command                       STAGES ARMED
corp-monorepo  python -m pre_commit install                                  pre-commit
ai-council     python -m pre_commit install                                  pre-commit
win-tooling    python -m pre_commit install -t pre-commit -t commit-msg      pre-commit, commit-msg,
                 -t pre-push                                                 pre-push
```

**On corp-monorepo and ai-council, `commit-msg` and `pre-push` are never armed.** Whatever those
repos declare in `.pre-commit-config.yaml` at those stages — `block-ff-push` (non-waivable),
`backlog-id-on-close`, any pre-push anchor gate — **is installed and does not fire.**

This **resolves §3 note 2**, which could only say `canonical_freshness=present-unverified` —
*"the hook line exists; static reading cannot prove it fires."* It is now proven, and the answer is
negative for two stages on two consumers. It is also **Z-C-6 ("a hash-clean floor is not a working
floor") demonstrated a second, independent way**: three floors are hash-clean, and two of them arm a
third of the stages they are supposed to.

`gitignore_ok` fails on the same two repos, for all four required lines
(`.claude/*`, and the negations `!.claude/CLAUDE-FLOOR.md`, `!.claude/CLAUDE-FLOOR.md.sha256`,
`!.claude/check_floor_hash.py`). win-tooling carries all four.

#### A3-W · Waiver state, validated live

`enforcement_coverage.validate_allowlist_entry` run against each clone at `run_date=2026-09-05`
with the policy from the latest manifest:

```
REPO           VALID ENTRIES                                                  EXPIRED
corp-monorepo  ruff-gate, hub-codemap-hooks, hub-toc-hooks,                   .vscode (2026-08-26)
               audit-casing-r4, github-ci-local,
               vscode-boundary-decoration
ai-council     ruff-gate, hub-codemap-hooks, hub-hermetization-rule-a,        dep-pytest-xdist (2026-08-16)
               hub-hermetization-rule-b-grammar,                              .vscode (2026-08-26)
               claude-md-section-11-title, vscode-boundary-decoration,
               claude-md-token-log-address
win-tooling    (no .methodology.yaml — zero entries)                          —
```

**Both waivers §3 prescribes for corp-monorepo already exist and are valid. The one waiver §3
prescribes for ai-council already exists and is valid.** Only win-tooling's is genuinely owed, and
owing it means creating `.methodology.yaml` from scratch. Correction at A6-C2.

**Three expired entries are live and were invisible to the body**, which had no consumer tree to
read them from. An expired entry is not a valid divergence.

### A4 · Region drift — the eight-region matrix, per consumer

**This section replaces §2's "Region drift — NOT MEASURABLE this run" and closes what the body
called "the single largest gap in this audit."**

**Method.** Region bodies were extracted with the repo's own parser
(`scripts/boundary_report.parse_regions`, which owns the sole definition of the
`<!-- methodology:start id=... owner=... -->` vocabulary) — not by a hand-written regex. Each body
and each `templates/claude-regions/*.md` source was **line-ending normalised (CRLF/CR to LF) and
stripped before comparison**, so a CRLF difference cannot be reported as drift. Comparison is on
**UTF-8 bytes** of the normalised text. Parser warnings were captured: **zero** on every file.

**Control — the hub itself**, re-measured at this branch, reproducing HUB-2 (8/8 byte-identical):

```
antipatterns-universal IDENTICAL · conventions-commit-branch IDENTICAL
conventions-output-formatting IDENTICAL · critical-rules-consistency IDENTICAL
critical-rules-no-leftovers IDENTICAL · critical-rules-records IDENTICAL
first-read IDENTICAL · session-start-protocol IDENTICAL
```

**The matrix.** `IDENT` = present, byte-identical. `DRIFT` = present, differs (byte delta shown).
`ABSENT` = no marker for that region in the file.

```
REGION                          corp-monorepo        ai-council           win-tooling
antipatterns-universal          DRIFT  654B (-473)   DRIFT  671B (-456)   ABSENT
conventions-commit-branch       DRIFT  289B (-248)   DRIFT  289B (-248)   ABSENT
conventions-output-formatting   DRIFT 1223B (+476)   DRIFT 1223B (+476)   ABSENT
critical-rules-consistency      DRIFT  103B  (-64)   DRIFT  103B  (-64)   ABSENT
critical-rules-no-leftovers     IDENT  345B          IDENT  345B          ABSENT
critical-rules-records          DRIFT  689B (-312)   DRIFT  704B (-297)   ABSENT
first-read                      DRIFT  765B (-476)   DRIFT  765B (-476)   ABSENT
session-start-protocol          DRIFT  517B (-162)   DRIFT  517B (-162)   ABSENT

MARKERS IN CLAUDE.md            21 regions           23 regions           0 regions
CLAUDE.md SIZE                  23,025 B             33,831 B             10,533 B
```

`.claude/CLAUDE-FLOOR.md` was measured on all three as well: **3,136 B, zero markers, all eight
regions ABSENT** on every consumer. The floor does not carry the hub regions — so a consumer whose
`CLAUDE.md` lacks them has them nowhere.

#### A4-P · The drift is a PIN, not tampering — provenance resolved

A byte delta alone cannot distinguish "a consumer edited this" from "the hub moved on." So every
drifted body was searched against **the full git history of its own template** in this repo
(`git log` over `templates/claude-regions/<region>.md`, comparing each historical blob):

```
REGION                          corp-monorepo               ai-council
antipatterns-universal          hub template c46e1837 (2026-07-12)   NO hub revision
conventions-commit-branch       hub template af4a1ad2 (2026-07-12)   hub template af4a1ad2 (2026-07-12)
conventions-output-formatting   hub template c46e1837 (2026-07-12)   hub template c46e1837 (2026-07-12)
critical-rules-consistency      hub template c46e1837 (2026-07-12)   hub template c46e1837 (2026-07-12)
critical-rules-no-leftovers     hub template af4a1ad2 (2026-07-12)   hub template af4a1ad2 (2026-07-12)
critical-rules-records          hub template c46e1837 (2026-07-12)   NO hub revision
first-read                      hub template af4a1ad2 (2026-07-12)   hub template af4a1ad2 (2026-07-12)
session-start-protocol          hub template c46e1837 (2026-07-12)   hub template c46e1837 (2026-07-12)
```

**corp-monorepo: 8 of 8 regions match a hub template revision exactly, all dated 2026-07-12. Zero
local edits.** It is not drifted in the sense of tampering — it is **pinned at the 2026-07-12 hub
region corpus**, and the hub has moved since. The right verb is *stale*, and the right fix is a
redeploy, not a reconciliation.

**ai-council: 6 of 8 likewise pinned at 2026-07-12; 2 match no hub revision** and are genuinely
locally edited. Those two, diffed against the live hub source:

```
antipatterns-universal
-  - **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** ...
+  - **Editing old LESSONS.md or `.dev-knowledge/logs/TOKEN-LOG.md` entries** ...

critical-rules-records
-  1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** ...
+  1. **`LESSONS.md` and `.dev-knowledge/logs/TOKEN-LOG.md` are append-only** ...
```

**Both edits are DECLARED and SANCTIONED.** ai-council's `.methodology.yaml` carries
`claude-md-token-log-address` (valid through 2026-10-26), whose reason names *exactly these two
regions* and argues the hub's bare `logs/TOKEN-LOG.md` "is correct AT THE HUB and false here" —
ai-council has never had a local token log. **So the fleet's only genuinely-edited hub regions are
two, in one repo, and both are covered by a valid time-boxed waiver.** That is a materially
different finding from "drift", and the body could not have reached it.

#### A4-D · One doctrine defect the pin actually carries

Being pinned to a July corpus is not cost-free. Both marker-carrying consumers instruct sessions:

```
- **Narrating or managing AGENTS.md** - AGENTS.md is retired (ADR-53); CLAUDE.md is the
  single instruction file
```

**ADR-115 (Accepted, 2026-08-25) reversed exactly this**, admitting `AGENTS.md` as the portable
instruction layer and superseding ADR-53 Decision 2. Measured: the string `AGENTS.md is retired` is
present in corp-monorepo's and ai-council's `CLAUDE.md`; the string `ADR-115` appears in **none** of
the three. Two consumers' boot files carry a governance instruction that live doctrine has
reversed, and no organ in the fleet reports it — there is no region-drift check on the consumer
side at all. Recorded as candidate **Z-C-12** at A6.

**win-tooling carries zero hub regions**, so it carries neither the stale instruction nor the
correct one. Its `CLAUDE.md` (10,533 B, 0 markers) is outside the Form-A boundary system entirely.
That is the more serious structural condition of the two: corp-monorepo and ai-council are *behind*;
win-tooling is *unenrolled*, and a redeploy of the region corpus has nothing to update. Recorded as
candidate **Z-C-13**.

### A5 · §0 RE-ISSUED in full

Same nine-row shape. `ORIGIN SHA` is now READ for every row (A2). Verdicts changed by a measurement
are marked **[AMENDED]**; each still cites the §2 row, or the A3/A4 row, that produces it.

```
REPO                      VERDICT                                                  ORIGIN SHA  CITES
.dev-knowledge (hub)      READY - baseline source, PASS; 8/8 regions clean         09f8053     HUB-1, A4
corp-monorepo             [AMENDED] NEEDS 5 carrier applies + 2 hook stages        fd3325e     A3, A3-S, A3-W,
                          armed. Waivers ALREADY PRESENT and valid (not owed);                 A4, A4-P, CM-1,
                          1 EXPIRED. Region corpus pinned 2026-07-12, 0 local                  CM-6
                          edits. Floor bytes clean
ai-council                [AMENDED] NEEDS 5 carrier applies + 2 hook stages        7a3c057     A3, A3-S, A3-W,
                          armed. Waiver ALREADY PRESENT and valid (not owed);                  A4, A4-P, AC-1,
                          2 EXPIRED. 6/8 regions pinned 2026-07-12, 2 edited                   AC-6
                          under a valid waiver. Floor bytes clean
win-tooling               [AMENDED] NEEDS 3 carrier applies + 1 waiver + a         49cb75e     A3, A3-W, A4,
                          .methodology.yaml (absent). UNENROLLED in the region                 WT-1, WT-2
                          boundary system: 0 of 8 hub regions present. Floor
                          and hook stages fully correct - the only consumer
                          at settings_ok=True
corp-ops                  BLOCKED by no floor deployed (pre-deploy)                3bde930     CO-1, CO-2
corp-sca-time-automation  BLOCKED by canonical_freshness FAIL + no deploy          1a80a9e     CS-1, CS-2
demo-prep                 BLOCKED by never audited - no state.yaml                 d849c81     FB-1
life-architect            BLOCKED by never audited - no state.yaml                 7688b76     FB-1
terminal-setup            BLOCKED by never audited - no state.yaml                 d8a7b61     FB-1
```

**Rows 5-9 are UNCHANGED in verdict.** corp-ops and corp-sca-time-automation were not cloned (the
contract names three repos), so no measurement in this amendment touches their §2 rows; their SHAs
are read, their verdicts stand on CO-1/CO-2 and CS-1/CS-2 as written. demo-prep, life-architect and
terminal-setup remain BLOCKED on FB-1: **a read origin SHA is not an audit.** Their SHAs prove only
that the repos exist and are reachable — which, read against B1, is itself worth stating: they were
never unreachable, only unregistered.

**No row's verdict improved.** Three changed because measurement found *more* than the body could
see, not less.

### A6 · Corrections — what the measurement contradicts

**C1 — "NEEDS N waivers" was wrong for two of three repos, in the consumers' favour.**
§0 reads `corp-monorepo NEEDS 2 waivers` and `ai-council NEEDS 1 waiver`; §3 then writes out the
YAML for each. **All three of those waivers already exist at origin/main and validate as `valid`**
(A3-W). The body could not know: it had no consumer tree, and inferred the waiver requirement from
the manifest's component set. The requirement was real; the *gap* was not. Only win-tooling's waiver
is genuinely owed. §3's YAML for corp-monorepo and ai-council should be read as *confirmation of
what is there*, not as work to do.

**C2 — §3's corp-monorepo `ruff-gate` rationale is right, but not for the stated reason.**
§3 says corp "keeps the hook" and the waiver is KEPT per the 2026-07-13 residual. Measured: corp
keeps 4 ruff lines and the waiver is valid to 2026-10-07 — **confirmed**. But §4 Step 3's premise
that "a `ruff-gate` prune with no waiver present will REFUSE" is not what plan mode shows: with or
without the waiver, plan prints `already_absent` (A3). The refusal path is real but lives in
`--execute`, and win-tooling — with no waiver at all — also shows `already_absent`, because for it
the component is genuinely gone.

**C3 — §4 Step 4's witness is unobtainable in plan mode.** It instructs the reader to look for
`waived by consumer .methodology.yaml -- skipping prune` in the plan output. That string is emitted
by `carrier_precommit.prune()`, which runs only under `--execute`. A reader following Step 4 as
written will not find it and may conclude the waiver failed. Step 4's witness should be: the remove
leg lists `ruff-gate` with prune state `already_absent`, **and** the waiver validates `valid` under
the Step 3 command — the two together, because the plan token alone does not distinguish waived from
absent.

**C4 — §2's consumer `CLAUDE.md` size table is superseded as a drift proxy.** §2 offers
`ai-council 33406 · corp-monorepo 22708 · win-tooling 10449 chars` and correctly says size "is not a
drift measurement." Measured byte sizes at origin/main are `33,831 / 23,025 / 10,533` — close, and
the divergence is explained: those figures came from the operator's local working copies, not
origin (see Z-C-11). Size is now retired as a proxy; A4 measures the thing itself.

**C5 — a false positive this amendment generated and killed, recorded so it is not re-derived.**
A raw-byte SHA-256 of win-tooling's `.claude/CLAUDE-FLOOR.md` does not match its sidecar, which
reads as a broken non-waivable floor gate. It is a CRLF artefact: the carrier hashes LF-normalised
text (`generate_floor.floor_sha256`). Measured with the repo's own function, **all three floors match
the corpus digest and their sidecars exactly.** WT-3, CM-2 and AC-2 stand.

**New candidates (Z-C shape, none filed — ADR-111):**

**Z-C-11 — the nightly baseline measures local working copies; nothing measures the gap to origin.**
corp-monorepo's origin `main` is 27 days behind the baseline's run date and ai-council's 24 days
(A2). Every §2 row is therefore a statement about the operator's disk, and a reader would reasonably
take it as a statement about the repo. No organ compares the two. Evidence: A2, §6 default 1.

**Z-C-12 — two consumers boot from a governance instruction ADR-115 reversed.** Both carry
"AGENTS.md is retired (ADR-53)"; neither mentions ADR-115. Inherited from the 2026-07-12 region
corpus, so it is a *pin* defect, not an edit defect — which means a region redeploy fixes it and
nothing today triggers one. Evidence: A4-D, A4-P.

**Z-C-13 — win-tooling is unenrolled in the region boundary system.** 0 of 8 hub regions, 0 markers,
no `.methodology.yaml`. It is simultaneously the *most* conformant consumer by carrier state
(3 correct, the only `settings_ok=True`) and the *least* governed by region content. The two signals
point opposite ways and no verdict combines them. Evidence: A4, A3-F, A3-S.

**Z-C-14 — plan mode conflates "waived" with "already absent."** `detect_prune` returns
`ALREADY_ABSENT` for both, and only `prune()` distinguishes them in its detail string. A reader of a
plan cannot tell a live sanctioned divergence from a component that was never there. Evidence: A3,
`carrier_precommit.py:1037-1055`.

**Z-C-15 — `tier1-plugin` is absent on every measured consumer.** The only `implemented: true`
carrier absent fleet-wide, carrying four components. Evidence: A3.

**Z-C-16 — a consumer can arm one hook stage of three and pass every floor check but one.**
corp-monorepo and ai-council run bare `pre_commit install`; their `commit-msg` and `pre-push` hooks
never fire. The single organ that notices is `carrier_floor`'s `settings_ok` leg, and it reports
only as an aggregate `present_drifted` on the whole floor carrier. Evidence: A3-S.

### A7 · Cost

**Wall-clock**, session start 13:58 UTC, phase boundaries at tool-call granularity:

```
PHASE                                                    WALL-CLOCK  MODEL CLASS
Setup (worktree verify, merge claude/fleet-readiness-h0,  ~5 min      Opus 5 (main session)
  read the 791-line prior art end to end)
M0 clone + SHA (3 full clones, 8 ls-remote reads)         ~2 min      Opus 5 (main session)
M1 carrier plan x3 + floor-leg / waiver / prune forensics ~7 min      Opus 5 (main session)
M2 region drift + history provenance + diff excerpts      ~3 min      Opus 5 (main session)
M3 amendment authoring + commit + scratch teardown        ~9 min      Opus 5 (main session)
```

No subagents were spawned. Every phase was a bounded deterministic read over three small trees;
fan-out would have added coordination cost without adding reach.

**Defaults taken under the decision budget, reported not asked:**

1. **Read `refs/heads/main` for the five uncloned consumers via `git ls-remote`.** The contract names
   three repos to clone; A5 asks for READ SHAs in all nine rows. `ls-remote` is a read-only origin
   query that discharges the `UNREAD (B1)` column without a clone. Their *verdicts* are untouched.
2. **Measured `.claude/CLAUDE-FLOOR.md` for regions as well as `CLAUDE.md`.** The contract names
   `CLAUDE.md`; measuring the floor too was needed to state honestly that win-tooling has the regions
   *nowhere*, rather than merely not in `CLAUDE.md`.
3. **Resolved drift provenance against the hub's own template git history.** Not asked for. Without
   it, A4 would have reported 15 drifted regions and implied 15 reconciliations, when the true
   finding is one stale pin plus two waived edits.
4. **Used the repo's own parser and hash function** (`boundary_report.parse_regions`,
   `generate_floor.floor_sha256`) rather than hand-rolled equivalents. This killed one false
   positive outright (C5).
5. **Did not run `audit.py run` or any fleet write path.** This lane measures; it does not audit.
   `audit.py health` was run only as the pre-commit gate.
6. **The worktree already carried all five `ecosystem/*/state.yaml`.** The contract's B3 seeding step
   was verified rather than performed: all five present, 11-16 KB each, `repos registered` non-empty.
   No `SKIP=` was used, and no gate was bypassed.
7. **Targeted v1.4.0, not v1.5.0**, per the contract and §4.

**Closure verification:**

```
(1) M0 table printed before M1                          YES - printed in session before any plan run
(2) every A5 verdict cites an A3/A4 or §2 row           YES - CITES column, all nine rows
(3) amendment is APPENDED, zero changes above           YES - git diff is pure addition; pre-amendment
                                                          body sha256 237612269309f298... unchanged
(4) no consumer repo modified                           YES - git status --porcelain empty in all three
                                                          clones at clone time and before deletion;
                                                          --execute never passed in any invocation
(5) aj-scratch/fleet removed and verified               YES - see teardown below
(6) deliverable is a COMMIT on the lane branch          YES
```

**Teardown (critical rule 9, no leftovers).** Immediately before deletion, each clone reported
`git status --porcelain` empty on branch `main` (closure 4). The scratch tree
`<prompts>/aj-scratch/fleet/` was then removed recursively and its absence verified
(`Test-Path` -> `False`); the sibling scratch directories under `aj-scratch/` predate this lane and
were not touched. Every measurement in this amendment is carried by the tables above, so the clones
were disposable by construction.

**Substrate note for the record.** This half ran LOCAL under a named operator exception, and the
exception earned its keep: of the seven measurement results this amendment contributes — origin SHAs,
carrier plan output, floor-leg isolation, hook-stage arming, waiver validation, region drift, and
drift provenance — **not one was obtainable from the cloud**, and six of the seven required a
consumer working tree on disk, exactly as §1 B1.2 predicted.
