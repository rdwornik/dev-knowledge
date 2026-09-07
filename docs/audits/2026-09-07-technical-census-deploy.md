# Census — `deploy/` (SWEEP 2026-09-07, lane S-12, READ-ONLY)

**Consumer:** `[#371]` (the `editor-config` declared-but-unbuilt carrier this census re-measures on
the current manifest), `[#297]` and `[#267]` (the two open `deploy/lived_sandbox/` rows), and
`ADR-92` (the carrier contract whose declared-vs-implemented boundary is this lane's question).
Substantive citations are by path throughout.

**Lane:** S-12 · **Folder:** `deploy/` · **Mode:** read-only census. Every verdict below is a
**PROPOSAL** the operator rules. Nothing was moved, edited, renamed or deleted; defects are
reported, not repaired. One of 13 parallel census lanes; the integrator merges.

**Lane question beyond the plain inventory:** manifests, carriers, sidecars — which components are
declared vs implemented, and which manifests are stale.

**Headline:** the folder is healthy at the file level — **28 files, 28 KEEP, 0 RELOCATE, 0 ARCHIVE,
0 RETIRE, 0 UNDETERMINED**. Every file has a live consumer. The findings are not about files, they
are about **pointers and prose inside the files**: three surfaces that name "the current manifest"
disagree (two are pinned to a version that is no longer current), the current manifest contradicts
its own header in a carrier comment, and one shipped manifest declares a `source_tag` that was
never cut.

**The folder changed under this census.** A `git merge origin/main` between the read pass and the
commit brought in `deploy/floor_mechanisms.py` (`cf0122b`, 2026-09-07) and grew
`manifest-v1.5.0.yaml` by ~11.8 KB with a new top-level `floor_mechanisms_pending:` key. Every
count and locator below was **re-measured after that merge**, not carried over — see F6 and Honest
limit 9.

---

## Inventory

28 files, 685,958 bytes total (`find deploy -type f | wc -l`; `find deploy -type f -exec wc -c {} +`).
"Witness" is a consumer found by `grep`, a generator/registry entry, or a test module that imports
the file.

| File | Bytes | Verdict | Witness |
|---|---|---|---|
| `deploy/contract.py` | 9,479 | KEEP | Imported by all six carrier modules (`carrier_docs.py:62`, `carrier_floor.py:69`, `carrier_globalconfig.py:47`, `carrier_mesh.py:53`, `carrier_plugin.py:64`, `carrier_precommit.py:45`) + `deploy/tool.py:98` + `scripts/enforcement_coverage.py:853` |
| `deploy/tool.py` | 61,677 | KEEP | `tests/test_deploy_tool.py`, `tests/test_deploy_tool_assess.py`, `tests/test_deploy_tool_execute.py`; last content commit `a49537c` (2026-09-07, `--consumer <path>` override) |
| `deploy/carrier_globalconfig.py` | 9,783 | KEEP | `tests/test_deploy_globalconfig.py`; instantiated `deploy/tool.py:441`; implements manifest carrier `global-config` (`deploy/manifest-v1.5.0.yaml:164`, `implemented: true`) |
| `deploy/carrier_plugin.py` | 17,178 | KEEP | `tests/test_deploy_plugin.py`; `deploy/tool.py:444`; carrier `tier1-plugin` (`manifest-v1.5.0.yaml:208`) |
| `deploy/carrier_precommit.py` | 48,573 | KEEP | `tests/test_deploy_precommit.py`, `tests/test_deploy_precommit_surgical.py`, `tests/test_carrier_precommit.py`; `deploy/tool.py:445`; carrier `precommit` (`manifest-v1.5.0.yaml:222`) |
| `deploy/carrier_floor.py` | 46,021 | KEEP | `tests/test_deploy_floor.py`; `deploy/tool.py:446`; carrier `floor` (`manifest-v1.5.0.yaml:274`) |
| `deploy/carrier_mesh.py` | 13,849 | KEEP | `tests/test_deploy_mesh.py`; `deploy/tool.py:447`; carrier `enforcement-mesh` (`manifest-v1.5.0.yaml:291`) |
| `deploy/carrier_docs.py` | 13,191 | KEEP | `tests/test_deploy_docs.py`; `deploy/tool.py:448`; carrier `docs` (`manifest-v1.5.0.yaml:407`) |
| `deploy/floor_mechanisms.py` | 26,079 | KEEP | **Landed mid-census** (`cf0122b`, 2026-09-07). `tests/test_floor_mechanisms.py:18`; reads the manifest blocks it is named by — `manifest-v1.5.0.yaml:870,1064` |
| `deploy/floor_conformance.py` | 21,975 | KEEP | `tests/test_floor_conformance.py`; `scripts/enforcement_coverage.py:346`; `deploy/lived_sandbox/spawn.py:31`; `scripts/proof_layer.py:124` |
| `deploy/release_lint.py` | 25,807 | KEEP | `tests/test_release_lint.py`; cited by `scripts/canonical_docs.py:280`, `scripts/gen_methodology_roster.py:47`, `protocols/HANDOFF_PROCESS.md:1192`, `protocols/STANDING_RULINGS.md:3535` |
| `deploy/global-instructions-codex.md` | 3,891 | KEEP | The `global-config` carrier's ONE payload — `manifest-v1.5.0.yaml:575` (`source:`), `deploy/tool.py:464`, `deploy/carrier_globalconfig.py:4`; named by root `AGENTS.md` "Precedence" section; `tests/test_codex_instruction_home.py` |
| `deploy/release-v1.3.x-contract.md` | 29,746 | KEEP | `deploy/carrier_docs.py:3` (the carrier cites it as its own spec), `manifest-v1.4.0.yaml:354`, `manifest-v1.5.0.yaml:413`, `tests/test_deploy_docs.py:22,281`, `scripts/audit.py:4555`, `tasks/290-floor-carrier-verify-teeth-self-heal.md` |
| `deploy/manifest-v1.0.0.yaml` | 10,071 | KEEP | Tag `v1.0.0` exists on origin; `tests/test_deploy_precommit.py`, `tests/test_deploy_tool_assess.py`, `tests/test_deploy_tool_execute.py`, `tests/test_floor_conformance.py`, `tests/test_file_purpose_graph.py`; `tasks/239-follow-up.md` |
| `deploy/manifest-v1.1.0.yaml` | 18,733 | KEEP (defect) | `tests/test_essence_spec.py:28` binds it as `LIVE_MANIFEST`; `tests/test_release_lint.py`; `tasks/244-essence-spec-lifecycle-epic.md`. **No `v1.1.0` tag exists on origin** — see Finding F3 |
| `deploy/manifest-v1.2.0.yaml` | 35,184 | KEEP | Tag `v1.2.0` on origin; the deployed version of `corp-monorepo` (`ecosystem/deployed-versions.yaml`); `deploy/lived_sandbox/arc.py:141` reads it as the oracle; `tests/test_release_lint.py`, `tests/test_carrier_precommit.py`, `tests/test_lived_sandbox_consumer.py`; five open `tasks/` rows |
| `deploy/manifest-v1.3.0.yaml` | 39,275 | KEEP | Tag `v1.3.0` on origin; `tests/test_carrier_hooks_source.py`; `tasks/323-design-question.md` |
| `deploy/manifest-v1.3.1.yaml` | 39,891 | KEEP | Tag `v1.3.1` on origin; the deployed version of `ai-council` (`ecosystem/deployed-versions.yaml`); `tasks/315-*.md`, `tasks/325-*.md`, `tasks/351-*.md` |
| `deploy/manifest-v1.4.0.yaml` | 49,982 | KEEP | Tag `v1.4.0` on origin; hardcoded as `MANIFEST_NAME` in `scripts/desired_state_loader.py:57`; cited by `scripts/canonical_docs.py:33`, `scripts/verify_handoff_probes.py:82`; four open `tasks/` rows |
| `deploy/manifest-v1.5.0.yaml` | 69,851 | KEEP (defect) | The current manifest — max-semver, which is what `deploy/release_lint.py:189` and `scripts/gen_methodology_roster.py:66` resolve; generated `.claude/methodology-roster.md` header ("manifest v1.5.0"); `ecosystem/parity-surfaces.yaml`, `protocols/HANDOFF_PROCESS.md`, `docs/decisions/ADR-117-carrier-split-by-divergence.md`. See F1/F2 |
| `deploy/lived_sandbox/__init__.py` | 1,450 | KEEP | Package root for the seven modules below; `tests/test_lived_sandbox.py:18` |
| `deploy/lived_sandbox/isolation.py` | 3,836 | KEEP | `tests/test_lived_sandbox.py:18` |
| `deploy/lived_sandbox/spawn.py` | 12,231 | KEEP | `tests/test_lived_sandbox.py:19`, `tests/test_lived_sandbox_observer.py:22`, `tests/test_lived_sandbox_consumer.py:22` |
| `deploy/lived_sandbox/oracle.py` | 9,752 | KEEP | `tests/test_lived_sandbox_observer.py:20`, `tests/test_lived_sandbox_consumer.py:21` |
| `deploy/lived_sandbox/observe.py` | 19,412 | KEEP | `tests/test_lived_sandbox_observer.py:21`, `tests/test_lived_sandbox_consumer.py:20` |
| `deploy/lived_sandbox/arc.py` | 25,540 | KEEP (defect) | `tests/test_lived_sandbox_observer.py:19`, `tests/test_lived_sandbox_consumer.py:17`; `tasks/267-scope-exercising-arc-extension.md` cites `ARC_PROMPT`. See F1 |
| `deploy/lived_sandbox/consumer.py` | 14,251 | KEEP (defect) | `tests/test_lived_sandbox_consumer.py:19`. See F1 |
| `deploy/lived_sandbox/cli.py` | 9,250 | KEEP | `templates/consumer-onboarding-runbook.md:23` (`python -m lived_sandbox.cli observe-arc --consumer <repo-path>`); `tests/test_lived_sandbox_consumer.py:18`, `tests/test_lived_sandbox_observer.py:826`; `tasks/297-*.md` |

No subdirectory other than `deploy/lived_sandbox/` exists (`find deploy -type d`). There is no
`__pycache__`, no scratch file, no orphan: `deploy/` is on `pythonpath` (`pyproject.toml:179`,
`pythonpath = [".", "scripts", "deploy"]`), which is why the flat `from contract import ...` style
works and why no `src/` layout is present.

---

## Proposals

### KEEP — 28 of 28

Every file in `deploy/` has at least one live consumer that a `grep` produced. No file in this
folder is a candidate for RELOCATE, ARCHIVE or RETIRE, and none is UNDETERMINED. Three groupings
carry the reasoning:

**The carrier spine (10 files) — `contract.py`, `tool.py`, the six `carrier_*.py`,
`floor_conformance.py`, `floor_mechanisms.py`.**
Witness is structural, not editorial: `deploy/tool.py:441-448` builds exactly six carriers by
`carrier_id`, one per module, and each has a dedicated test module. The spine is not merely
referenced, it is exercised. `floor_mechanisms.py` is the newest member and the only one that is
**not** a carrier: it is a two-sided drift checker over the manifest (F6), with its own test module
from the same commit.

**The manifests (7 files).** A superseded manifest is **not** dead material here. Two of the seven
are the *live deployed target* of a real consumer — `ecosystem/deployed-versions.yaml` records
`corp-monorepo` at `1.2.0` and `ai-council` at `1.3.1` — so `manifest-v1.2.0.yaml` and
`manifest-v1.3.1.yaml` are what a re-deploy or a verify of those repos reads. `release_lint` takes
`--version` and lints any of them. Under the repo's own genre rules a released manifest is a frozen
record, and `deploy/release_lint.py:426-434` (C7) now states that in code: a manifest that is not
the current one "PASSes without comparison … released/historical, not compared to live constants".
**Proposing ARCHIVE for any of them would break both a live deploy target and a test binding.**

**`deploy/lived_sandbox/` (8 files) and `deploy/release-v1.3.x-contract.md`.**
The likeliest ARCHIVE candidates by look — a sandbox package and a dated release contract — and
both survive on witnesses. `lived_sandbox` is imported by three test modules and is the documented
consumer-measurement instrument in `templates/consumer-onboarding-runbook.md:23`, with two open
backlog rows (`[#297]`, `[#267]`) naming its files. `release-v1.3.x-contract.md` is cited *as a
spec* by shipping code and by the two newest manifests (`deploy/carrier_docs.py:3`;
`manifest-v1.5.0.yaml:413`), and `scripts/audit.py:4555` names it by path. Archiving either would
strand live citations.

### RELOCATE — none

No file in `deploy/` is misfiled under the `#73` home grammar. The folder holds exactly one genre:
the deployment engine (contract, tool, carriers, manifests, the one carried payload, the release
lint, the measurement sandbox). `global-instructions-codex.md` is the closest thing to an outlier —
a markdown file among Python — and it belongs here precisely because it is a **carrier payload**,
declared at `manifest-v1.5.0.yaml:575`; root `AGENTS.md` explains in its "Precedence" section that
it is deliberately *not* named `AGENTS.md` so no intermediate directory holds a file Codex
auto-reads. Moving it would re-open that resolved collision.

### ARCHIVE — none · RETIRE — none · UNDETERMINED — none

Stated positively, not as padding: each of the 27 rows above carries a named witness, so no row
fell through to UNDETERMINED.

---

## Findings — declared vs implemented, and stale manifests

These are the lane question's answer. **All are reported, none repaired.**

### F1 — Three surfaces name "the current manifest" and two are pinned to a stale version

There is no single spelling of "the current manifest" in this repo. Two surfaces resolve it
**dynamically** by max-semver; three name a version **literally**, and each literal is behind:

```
dynamic   deploy/release_lint.py:189           highest manifest-v*.yaml present  -> v1.5.0
dynamic   scripts/gen_methodology_roster.py:66 MAX-semver deploy/manifest-v*.yaml -> v1.5.0
pinned    deploy/lived_sandbox/arc.py:141      _MANIFEST_REL = "deploy/manifest-v1.2.0.yaml"
pinned    deploy/lived_sandbox/consumer.py:6   "Oracle = the HUB manifest (deploy/manifest-v1.2.0.yaml)"
pinned    scripts/desired_state_loader.py:57   MANIFEST_NAME = "manifest-v1.4.0.yaml"
```

The consequence is specific and measurable. `deploy/lived_sandbox/consumer.py:6` states that the
**oracle** for a consumer measurement *is* the hub manifest; `arc.py:226` then loads
`manifest-v1.2.0.yaml`. So the instrument that measures whether a consumer meets the methodology
grades it against a **three-release-old** target: it cannot see the `docs` carrier (added at
v1.4.0), nor `editor-config`, nor `boot-inversion`, nor any component added after v1.2.0. A
measurement taken today reports coverage against v1.2.0 while the roster, the lint and the
generated `.claude/methodology-roster.md` all speak v1.5.0.

`scripts/desired_state_loader.py:57` is the same class one version back. **It is in another lane's
folder — flagged here only because it is a pointer *at* `deploy/`, and not touched.**

Proposal (operator's call): make "the current manifest" one resolver. `release_lint._current_manifest`
already is one; the two `lived_sandbox` pins and the `desired_state_loader` constant could call it
instead of spelling a version. Not proposed as a fix in this lane — it is a code change across two
folders, and this is a census.

### F2 — `manifest-v1.5.0.yaml` contradicts its own header

The current manifest states the C7/`doc_shapes` coupling **twice, incompatibly**:

- Header (`deploy/manifest-v1.5.0.yaml:51-57`): *"RESOLVED 2026-09-02 ([#621] lane-g-621-c7,
  R-G-G3b): C7 now binds a manifest to the constants AS OF ITS OWN VERSION — only the CURRENT
  manifest (this one) is mirrored against live constants; v1.1.0/v1.2.0 are frozen history and no
  longer compared. Adding README.md to `_CANONICAL_SPINE` no longer REDs shipped specs."*
- The `docs` carrier block, ~380 lines later (`deploy/manifest-v1.5.0.yaml:474-478`), still gives
  the **old** state as a live blocker: *"`release_lint` C7 asserts EXACT dict equality between
  `doc_shapes` spines and the live `audit._CANONICAL_SPINE`, and lints v1.1.0 and v1.2.0 against
  the SAME live constants — so adding README.md to either side alone REDs shipped specs."*

The code settles it: `deploy/release_lint.py:426-434` compares only the current manifest and
returns a pass with *"released/historical, not compared to live constants"* for every other. **The
header is right; the carrier block is stale prose.** This matters beyond tidiness — the stale block
is the recorded reason `readme-front-door` stays undeclared, so a reader sequencing `[#614]` /
ADR-114 option (C) off the carrier block will believe a blocker exists that was cleared five days
ago. The header already says the *remaining* blocker is the spine re-point itself.

**No gate reads manifest prose.** C1–C8 read `methodology_version`, `source_tag`, `carriers`,
`components`, `anchors`, `doc_shapes` and `engages` — never a comment. That is why this drifted
silently, and why the same class produced the next finding.

### F3 — `manifest-v1.1.0.yaml` declares a `source_tag` that was never cut

Origin's tags (`git ls-remote --tags origin`, this session):

```
archive/drafts-2026-07-07 · v1.0.0 · v1.2.0 · v1.3.0 · v1.3.1 · v1.4.0
```

`v1.1.0` is absent — the sequence jumps `v1.0.0` -> `v1.2.0`. Yet `deploy/manifest-v1.1.0.yaml:21`
declares `source_tag: v1.1.0`, and its own header (`:10`) says *"the tool's preflight requires that
tag to resolve before `--execute`, so v1.1.0 must be tagged by the operator before the real deploy
runs."* It never was. `deploy/tool.py:395-399` refuses on exactly this:

> `f"target tag {source_tag!r} does not resolve in the hub -- the release is not tagged yet"`

So **`manifest-v1.1.0.yaml` is permanently undeployable** — a spec for a release that does not
exist. It is nonetheless load-bearing: `tests/test_essence_spec.py:28` binds it as `LIVE_MANIFEST`,
the behaviour-preserving witness for the essence-spec P1 change (`tasks/244-*.md`). Hence KEEP, not
RETIRE — but its status is not recorded anywhere in the file. `release_lint` C2 emits a **WARN**,
not a FAIL, for an unresolved tag (`deploy/release_lint.py:230-239`), so nothing escalates it.

Contrast `v1.5.0`, which is **also** untagged but **declares it**: `manifest-v1.5.0.yaml:12-14`
says *"RELEASE CANDIDATE, drafted 2026-09-01 by the night orchestrator and NOT TAGGED — the
operator tags at release (ADR-91), so `release_lint --version v1.5.0` reports exactly ONE finding,
C2-tag, until he does."* That is the correct posture, and it is why v1.5.0's untagged state is
**not** a finding. v1.1.0's silence is the finding.

Consequence worth naming: `manifest-v1.5.0.yaml:242` pins `hub_hooks.rev: v1.5.0`. C3
(`release_lint.py:242-254`) requires `rev == source_tag`, which passes — but a consumer's
`.pre-commit-config.yaml` written from this manifest would reference a hub rev that does not
resolve on origin until the operator tags. Declared and consistent; simply not yet cuttable.

### F4 — Declared-but-unimplemented carriers: 2 of 8, covering 3 of 23 components

`manifest-v1.5.0.yaml` declares 8 carriers. Six are `implemented: true` and each has a module and a
`tool.py` factory entry; two are `implemented: false` and have **no module anywhere in the repo**:

```
global-config     order 1  implemented: true   -> deploy/carrier_globalconfig.py
tier1-plugin      order 2  implemented: true   -> deploy/carrier_plugin.py
precommit         order 3  implemented: true   -> deploy/carrier_precommit.py
floor             order 4  implemented: true   -> deploy/carrier_floor.py
enforcement-mesh  order 5  implemented: true   -> deploy/carrier_mesh.py
editor-config     order 6  implemented: FALSE  -> no module         (manifest-v1.5.0.yaml:385)
docs              order 7  implemented: true   -> deploy/carrier_docs.py
boot-inversion    order 8  implemented: FALSE  -> no module         (manifest-v1.5.0.yaml:480)
```

Three of the 23 components ride the two unimplemented carriers and therefore cannot reach any
consumer: `vscode-boundary-decoration` (carrier `editor-config`), `boot-session-command` and
`funnel-health-digest` (carrier `boot-inversion`).

**This is declared behaviour, not drift, and the engine handles it honestly.** `deploy/tool.py:689-695`
emits `"skip -- not implemented (do-not-build doctrine)"` rather than erroring, and each manifest
block states its own blocker in full: `editor-config` needs a merge strategy that does not clobber
a consumer-authored `.vscode/settings.json` under the ADR-93 single-writer constraint;
`boot-inversion` says the hub half is built and tested but the carrier module "was outside this
lane's frozen write-scope". `[#371]` owns the first. **`boot-inversion` has no backlog row that a
`grep` finds** — `grep -rn "boot-inversion"` returns the manifest, two audits and no `tasks/` file.
That asymmetry is the reportable part: one declared-but-unbuilt carrier is ticketed, the other is
recorded only in a manifest comment and two audit artifacts.

This finding **agrees with** `docs/audits/2026-09-05-technical-fleet-readiness.md:230-260`, which
measured the same 8-carrier split two days ago. That audit counted **21** components; the manifest
carries **23** today, because `cf0122b` added `floor-hooks-armed` (`manifest-v1.5.0.yaml:873`) and
`floor-waiver-register` (`:915`) hours ago. Both counts were correct when taken — this one was
re-derived independently from the manifest after the merge (`awk` over the `components:` range,
lines 503-1071), not copied from the earlier audit.

### F6 — A fourth state now exists between "declared" and "implemented"

`cf0122b` (2026-09-07) landed `deploy/floor_mechanisms.py` (26,079 B) and a **new top-level
manifest key**, `floor_mechanisms_pending:` (`manifest-v1.5.0.yaml:1072`). It changes the shape of
this lane's own question, so it is reported rather than folded into F4.

Floor v1.5.0 ruled five mechanisms. Two had a hub payload and became ordinary components; three did
not, and are declared in the new block with a **measured blocker each**:

```
components:                 floor-hooks-armed (:873) · floor-waiver-register (:915)
floor_mechanisms_pending:   floor-seal-report (:1074) · floor-roles-table (:1108)
                            floor-freshness-registry (:1143)
```

The block's own header states the reasoning, and it is the right one: the manifest's component
lifecycle is two-state by ruling (`active | removed`, enforced by `release_lint` C6), and a
mechanism whose **hub** payload does not exist is neither — *"it is not active (nothing to ship) and
it is not removed (nothing was ever there)"*. Declaring it as `active` would be the exact failure
the manifest header already names: *"declaring a component against a payload that does not exist
lints green but is undeployable."*

Two things follow that matter to this census:

- **The hub-side leg was previously unmeasured.** `deploy/floor_mechanisms.py:12-20` states that
  before it existed, `verify:`/`engages:` asked only "is it present and does it fire **at the
  consumer**", and nothing asked *does the hub still hold the payload it declares?* — so the
  declared-vs-implemented question this lane was set was, until today, **answerable only by reading
  prose**. F2 and F3 above are both instances of exactly that gap.
- **Five of 23 components declare a `mechanism.version`; 18 do not.** `grep -c "^    mechanism:"`
  returns 5 (2 in `components:`, 3 in `floor_mechanisms_pending:`). The module's docstring names
  this as the starting state, not the finished one: inbox 024's packaging rule wants *every*
  component versioned with a two-sided drift check. **18 of 23 are not there yet** — reported as
  the measured gap, with no proposal attached; sequencing it is a release act.

**Not verified by this lane:** I did not run `deploy/floor_mechanisms.py --consumer <path>` (no
consumer tree exists here — Honest limit 3) and did not read its 26 KB body beyond the docstring
and the manifest blocks it reads. Whether its hub and consumer legs behave as documented is
`tests/test_floor_mechanisms.py`'s claim, not mine.

### F5 — The three anchors are green (measured, not assumed)

`anchors:` is where a manifest could silently drift from live artifacts. All three were recomputed
this session:

```
floor_sha256   manifest-v1.5.0.yaml:161  4d268f32…8111f
               sha256sum templates/child-methodology-floor.md.tmpl   4d268f32…8111f   MATCH
               templates/child-methodology-floor.sha256 (sidecar)    4d268f32…8111f   MATCH
plugin_version manifest-v1.5.0.yaml:156  "0.1.11"
               plugins/tier1-lifecycle/.claude-plugin/plugin.json:3  "0.1.11"          MATCH
hub_hooks.rev  manifest-v1.5.0.yaml:242  v1.5.0  ==  source_tag v1.5.0                 MATCH (C3)
```

The **sidecar** leg of the lane question is therefore clean: spec pin, sidecar file and actual
template bytes agree three ways, which is exactly what C5 (`release_lint.py:275`) asserts. Note
that `tasks/444-*.md` describes the `0.1.11` plugin bump as reverted-in-arc; on disk today the
anchor and `plugin.json` agree at `0.1.11` across all seven manifests. **Whether that discharges
`[#444]` is the operator's call, not this census's** — the row's own Done-when also requires the
version-keyed plugin cache to carry it in live sessions, which is not measurable from here.

---

## Counts before → proposed after

All "before" figures are measured **after** the mid-census merge of `origin/main` (`cf0122b`
included), so they describe the tree this census actually read.

```
                                  before    proposed after    delta
files in deploy/                      28                28        0
  top level                           20                20        0
  deploy/lived_sandbox/                8                 8        0
bytes                            685,958           685,958        0

verdicts
  KEEP                                --                28
  RELOCATE                            --                 0
  ARCHIVE                             --                 0
  RETIRE                              --                 0
  UNDETERMINED                        --                 0

manifests                              7                 7        0
  tagged on origin                     5                 5        0
  untagged, declared as such           1 (v1.5.0)        1        0
  untagged, NOT declared               1 (v1.1.0)        1        0   <- F3, reported not fixed

carriers declared (v1.5.0)             8                 8        0
  implemented: true                    6                 6        0
  implemented: false                   2                 2        0   <- F4, reported not fixed
components declared (v1.5.0)          23                23        0
  reachable by a built carrier        20                20        0
  stranded on an unbuilt carrier       3                 3        0   <- F4
  carrying a mechanism.version         2                 2        0   <- F6
floor_mechanisms_pending (v1.5.0)      3                 3        0   <- F6, new key at :1072

anchors re-measured                    3                 3        0   all three MATCH (F5)
"current manifest" resolvers           5                 5        0
  dynamic (max-semver)                 2                 2        0
  literal, and behind                  3                 3        0   <- F1, reported not fixed
```

**Files this lane writes: 1** (this census). No appendix was needed — the file is well under 40 KB.

---

## Honest limits

What I could **not** establish. This section is the deliverable, not filler.

**1. Gemini fan-out: NONE.** `command -v gemini` returned nothing; the CLI is not on PATH in this
container. **Gemini-read files: 0. Fabrications: 0** — and that zero proves nothing about the
method, because no locator was ever returned to check. Absence is reported as absence, not as
clean. **Copilot Enterprise offload was NOT available** (gated on `#75` ratification) and was not
used; `command -v copilot` also returned nothing. Every locator in this census was opened by me.

**2. `release_lint.py` could not be executed, so C1–C8 here are hand-replications, not lint output.**
`uv run --locked` refuses in this container — `Required uv version ==0.11.19 does not match the
running version 0.8.17` — and the system Python lacks `click` (`ModuleNotFoundError: No module
named 'click'`), which `deploy/release_lint.py:87` imports at module scope, so even a direct import
fails. My C2/C3/C4/C5/C7 verdicts in F2/F3/F5 were derived by **reading the check bodies**
(`deploy/release_lint.py:216-480`) and recomputing their inputs by hand (`sha256sum`, `grep`,
`git ls-remote`). They should be confirmed by a real `release_lint --version v1.5.0` run in a
working environment before anyone acts on them. C1, C6 (`check_components`) and C8
(`check_engages`) were **not** replicated at all — I did not audit the 21 component rows field by
field, nor any `engages:` triple.

**3. No consumer tree exists in this container, so nothing consumer-side was measured.**
`ls /home/user/` shows only `dev-knowledge`; `deploy/tool.py` resolves a consumer relative to the
hub, and today's `a49537c` added a `--consumer <path>` override, but there is no path to point it
at. Everything in F4 is **declared-vs-hub-implemented**. Whether `ai-council` (recorded at 1.3.1)
or `corp-monorepo` (recorded at 1.2.0) actually carries what its manifest declares is
**unmeasured here**, and `ecosystem/deployed-versions.yaml`'s own header flags a related known gap
(G11: nothing records *why* a declared target has not been reached).

**4. The last-content-commit witness is coarse for 26 of 28 files.** Every file except `tool.py`
and `floor_mechanisms.py` resolves to the merge commit `428656f` (2026-09-05) under a
pathspec-limited `git log`, and `--no-merges` did not change that result, so I could not cheaply
obtain per-file leaf commits. For those 26 rows I therefore leaned on **consumer greps and
generator/registry entries** as the witness, not on commit recency. Only `deploy/tool.py`
(`a49537c`) and `deploy/floor_mechanisms.py` (`cf0122b`) have clean leaves, both 2026-09-07.

**5. Tag facts come from `origin`, not from this clone.** `git tag -l` is **empty** locally — this
container's clone carries no tags. F3 rests on `git ls-remote --tags origin`, which is
authoritative for whether a release tag exists but tells me nothing about which commit each tag
points at or whether it is reachable from `main`. I deliberately did **not** run `git fetch --tags`:
`refs/` is shared machinery and 12 peer lanes are running beside me.

**6. I did not read the carrier module bodies end to end.** `carrier_precommit.py` (48 KB),
`carrier_floor.py` (46 KB), `tool.py` (62 KB) and `floor_mechanisms.py` (26 KB) were read at their
docstrings, their factory / registry blocks and the specific regions cited above. **"Implemented"
in this census means: a module exists, `deploy/tool.py:441-448` instantiates it, and a dedicated
test module imports it.** It does **not** mean the behaviour was audited. A carrier could be
registered, tested and still wrong; this census would not have caught it.

**7. `deploy/lived_sandbox/` was censused as files, not as an instrument.** I established its
consumers and the v1.2.0 oracle pin (F1). I did **not** establish whether the pin is a deliberate
freeze — an oracle held at the version a past measurement was calibrated against is a defensible
design — or an oversight. `tasks/267-*.md` and `tasks/297-*.md` both cite these files without
settling it. **Treat F1's `lived_sandbox` half as a question for the operator, not a proven defect;**
the `scripts/desired_state_loader.py:57` half is a plain literal with no such ambiguity.

**8. No test run of any kind.** Per contract: no full suite, and I ran no targeted tests either —
the diff is one new markdown file. The known RED on main
(`test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`) was
neither reproduced nor investigated; it is not this lane's.

**9. The folder moved under me once, and could move again.** `deploy/` is in the SWEEP's
READ-NEVER-WRITTEN list, but batch U wave 2 was writing it: my first read pass saw 27 files at
`5f27b20`; the pre-commit `git merge origin/main` brought `21576e3` (10 files changed, +1,545), of
which `deploy/floor_mechanisms.py` and the `manifest-v1.5.0.yaml` growth land squarely in my scope.
I re-measured every count and re-opened every cited manifest locator afterwards (F6, and the note
under Counts), and the line numbers cited in F2 survive because the new material was appended below
them. **A census is a photograph of a moving tree.** If another wave-2 commit touches `deploy/`
after this lane's HANDBACK sha, this file is stale in exactly the same way and should be re-read
against the integrator's merge, not trusted as current.

**10. The authority file was not read.** `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` is on the Drive
transport, not in this repo (`ls to-cc/` -> absent; a filesystem search for the filename found
nothing). I executed the working copy of the contract as pasted. **If the frozen authority disagrees
with anything above, the authority wins and this census should be re-read against it.**
