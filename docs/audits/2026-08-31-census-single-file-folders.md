> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a1-single-file-folder-census` | receipt id `cse_01U9wkpZncq9GMf6S54CwUUm` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a1-single-file-folder-census.md`.
> Selection rule: the LONGEST assistant text, not the last - text #2 of 11 across 5 pages.
> Bytes written unchanged: **31,068**.
> Harvester DEVIATION, recorded not repaired: the report contains no markdown heading at all; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** HY-3 (`lane-m-13-templates-disposition`) and ruling Z-G5.
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

Census complete. No tree file was written, no commit proposed, no gate run. Everything below is the artifact.

```
LANE batch-e-a1-single-file-folder-census -- END PACKET
=======================================================

RECEIPT
-------
git-source-resolves-non-empty: origin = https://github.com/rdwornik/dev-knowledge
                               HEAD   = ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b
                               ("Merge branch 'docs/window-close' -- WINDOW CLOSE: two
                                rulings, ADR-116 recovered, the five pillars")
first-assistant-text-echoed:   brief is 117 lines; final line verbatim =
  "- No edits outside this lane's declared footprint. Prose in English; hyphen-only names."

TOOLING DECLARATION (contract "Gate note")
  Every measurement below was produced with `python3` invoked DIRECTLY and with plain
  `git`. `uv` was NOT used. NO gate was run and NO gate result is asserted -- the lane is
  read-only by contract and carries no test leg.
  One environment act was necessary and is disclosed: the cloud clone arrived SHALLOW
  (grafted at d74a980, 2026-08-26, 333 commits, every file's add-date collapsed onto the
  graft commit). Done-contract item 1 requires "the date it became single-file (from git
  history)", which a shallow clone cannot answer. `git fetch --unshallow` was run --
  read-only, writes nothing into the tree, changes no tracked file. Post-fetch: 6,122
  commits back to b635615f (2026-03-30). `git status --porcelain` is empty; HEAD unmoved.


PAUSE -- TWO REFUTED PREMISES (Q10). Reported, not repaired.
-----------------------------------------------------------

P1. `conflict/` -- CONFIRMED NEVER TO HAVE EXISTED, and the contract's own correction is
    itself incomplete.
    The contract already states there is no `conflict/` directory today. Measured deeper
    on the now-full history:
      - `git log --all -- 'conflict' 'conflict/*' '*/conflict/*'`  -> 0 commits
      - every path ever ADDED in 6,122 commits, filtered case-insensitively for "conflict"
        -> 0 paths
    So `conflict/` was never created and never removed. There is nothing to reinstate and
    nothing to report as removed.

    WHAT IT ALMOST CERTAINLY WAS. Z-G5's own text names its "first live subject" as
    `codex/` (protocols/STANDING_RULINGS.md:3222). `codex/` DID exist:
      created  fcd4eb64  2026-05-19  "feat: add codex/AGENTS.md -- canonical global Codex
                                      reviewer config"
      removed  8626db28  2026-08-29  "refactor(deploy): universalise codex/AGENTS.md into
                                      deploy/global-instructions-codex.md -- mechanism half"
    That removal is exactly the lawful discharge Z-G5 prescribed ("universalisation into
    the per-CLI instruction architecture, not deletion"), and root AGENTS.md now reads
    "There is deliberately no third layer." The batch brief's `conflict/` is best read as a
    garbling of `codex/` -- a subject that had ALREADY been discharged two days before this
    lane's freeze. Stated as an inference, not a fact: nothing in the tree records the
    garbling itself.

P2. The freeze figure "44 tracked directories holding exactly one file" -- REFUTED.
    Re-measured at HEAD (contract step 1 explicitly instructs not to trust 44):

      predicate                                              HEAD count   delta vs 44
      A  exactly one DIRECT tracked file (subdirs allowed)        23          -21
      B  A and no child directories (true leaf)                   18          -26
      D  exactly one ENTRY total (file or subdir)                 28          -16
      C  whole subtree holds exactly one tracked file             21          -23

    Tracked-file total is 2,761 -- which DOES match the freeze figure exactly. So the
    substrate sizing was measured correctly and the folder count was not.

    44 is not a stale reading either. Sampling every 60th first-parent commit across the
    full history, predicate A peaks at 33 (bf47ab78, 2026-06-05) and has never reached 44:
      2026-08-31 A=23 | 2026-08-28 A=25 | 2026-08-18 A=25 | 2026-08-05 A=23
      2026-07-07 A=25 | 2026-06-21 A=28 | 2026-06-05 A=33 | 2026-05-23 A=15
    The one predicate NOT testable from a clean cloud clone is a disk walk including
    gitignored trees (.venv, node_modules, .claude/worktrees), which exist only on the
    operator host. That is the sole remaining candidate explanation and this lane cannot
    measure it.

    This census proceeds on predicate A (23) as the superset, and reports B and D as
    columns rather than picking one silently.


THE CENSUS -- 23 directories, predicate A, measured at ec8731a9
--------------------------------------------------------------
Columns: LEAF = no child directories (predicate B). BITES = does Z-G5 actually bite.
Disposition per done-contract item 3: fold / keep-with-reason / retire.

--- 1 ---------------------------------------------------------------------------
path:        .claude-plugin/
file:        marketplace.json (427 B)
genre:       runtime manifest (Claude Code plugin marketplace root)
single since: 9f31f321, 2026-06-02 ("feat(plugin): package Tier-1 lifecycle as a portable
             CC plugin (ADR-70 #73)") -- born single, never held a second file
LEAF: yes    BITES: NO
consumers:
  REAL  deploy/carrier_plugin.py:292,369 -- `claude plugin marketplace add <source>` with
        source = _HUB_ROOT; the CLI resolves `<source>/.claude-plugin/marketplace.json` by
        hard convention. Fold the dir and the carrier's install step stops resolving.
  REAL  .methodology.yaml:118-124 -- a declared component (`.claude-plugin`) with a
        review_date; the declaration is keyed on the directory name.
  REAL  scripts/validate_hermetization.py:196 -- `.claude-plugin` is a LITERAL home-allowlist
        row (Rule C).
  MENT  plugins/tier1-lifecycle/INSTALL.md:38, docs/audits/* (7 files), JOURNAL.md (4)
disposition: keep-with-reason -- the path is an external runtime contract, not a taxonomy
             choice. Z-G5 cannot reach it.

--- 2 ---------------------------------------------------------------------------
path:        .claude/agents/
file:        artifact-reader.md (1,722 B)
genre:       agent definition (Claude Code convention dir)
single since: f8bbf1c7, 2026-06-06 ("feat(agents): add artifact-reader subagent [#97]")
LEAF: yes    BITES: NO
consumers:
  REAL  scripts/generate_organ_index.py:286 -- `_absent("agent", ".claude/agents/")`: the
        generator's OUTPUT changes when the directory vanishes (it renders
        ".claude/agents/ -- source absent" instead of the row). Directory existence is
        behaviour, tested at tests/test_generate_organ_index.py:407-441.
  REAL  ecosystem/provider-registry.yaml:292 + scripts/check_provider_registry.py:86 --
        seam S9 pins the file by full path; a pre-commit gate (provider-registry-agreement)
        enforces agreement.
  REAL  .pre-commit-config.yaml:233 -- the seam file-regex includes this path.
  MENT  ARCHITECTURE.md:422, ecosystem/organ-index.md:38 (generated row), JOURNAL/audits
disposition: keep-with-reason -- Claude Code loads agents from this exact directory name.

--- 3 ---------------------------------------------------------------------------
path:        .claude/rules/
file:        git-discipline.md (5,569 B)
genre:       repo-local rule file
single since: 583f3352, 2026-03-30 (the repo's SECOND commit; never held a second file here)
LEAF: yes    BITES: NO
consumers:
  REAL  scripts/generate_organ_index.py:334 -- `_absent("rule", ".claude/rules/")`, same
        directory-existence-is-behaviour shape as #2.
  REAL  CLAUDE.md:99 -- critical rule 7 names `.claude/rules/` as an explicit CARVE-OUT from
        the "rules live in ~/.claude/" invariant. Removing the dir invalidates a boot-contract line.
  REAL  templates/handoff/v5/HANDOFF_BOOT.md.tmpl:141 -- the generated boot carrier cites the
        path to every future session.
  REAL  tests/test_validate_doc_claims.py:52 -- fixture asserts the CLAUDE.md rendering shape.
  MENT  .claude/commands/{handoff,lane-integrate}.md, PLAYBOOK (3), STANDING_RULINGS:869
disposition: keep-with-reason.

--- 4 ---------------------------------------------------------------------------
path:        .claude/skills/check-against-spec/
file:        SKILL.md (4,681 B)
genre:       skill definition
single since: 89f71402, 2026-06-17 ("feat(coherence): per-site verdict checklist +
             check-against-spec skill")
LEAF: yes    BITES: NO
consumers:
  REAL  Claude Code skill runtime -- the DIRECTORY NAME is the skill's identity; a skill is
        `<dir>/SKILL.md` by convention. Folding renames the skill.
  REAL  scripts/generate_organ_index.py:314 -- `_files(root, ".claude/skills", "*/SKILL.md")`;
        the glob requires the per-skill directory level.
  REAL  scripts/validate_hermetization.py:196 -- `.claude/skills/*` allowlist row.
  REAL  scripts/validate_reconciliation.py (11 hits) + scripts/audit_checks/
        check_reconciled_versions.py:41 -- the skill NAME is the remediation the gate emits.
  MENT  CLAUDE.md:73, PLAYBOOK:290, HANDOFF_PROCESS (5), ecosystem/organ-index.md:67
disposition: keep-with-reason -- the sibling `.claude/skills/verify/` holds 2 files, so this
             is a per-skill directory, not a lone folder.

--- 5 ---------------------------------------------------------------------------
path:        .claude/workflows/
file:        conformance-hub.js (14,921 B)
genre:       Workflow orchestration spec (JavaScript)
single since: 8c0cf0d3, 2026-06-04 ("feat(cloud): commit validated conformance-hub workflow
             in-repo")
LEAF: yes    BITES: NO
consumers:
  REAL  scripts/generate_organ_index.py:325 -- `_absent("workflow", ".claude/workflows/")`.
  REAL  ecosystem/provider-registry.yaml:295 + scripts/check_provider_registry.py:87,96 --
        seam S10, gate-enforced; :96 pins the EXPECTED COUNT of per-stage `model:` pins.
  REAL  scripts/canonical_docs.py:38 + tests/test_canonical_docs.py:41 -- seam S11, the
        cross-language canonical-doc site.
  REAL  .claude/settings.json:77 -- the permissions envelope names the workflow.
  MENT  CONTRIBUTING.md:209, PLAYBOOK:3226, ARCHITECTURE.md:426
disposition: keep-with-reason -- project-shared workflows resolve from this exact path.

--- 6 ---------------------------------------------------------------------------
path:        .github/workflows/
file:        report-only-wall.yml (16,640 B)
genre:       CI workflow
single since: 82227f08, 2026-07-08 ("chore(automation): retire conformance-digest mechanism
             [#255]") -- it held TWO files; nightly-conformance-triage.yml was deleted then.
             This is one of only two directories in the census that SHRANK to one.
LEAF: yes    BITES: NO
consumers:
  REAL  GitHub Actions -- the path is the platform's hard contract; nothing else runs a
        workflow file.
  REAL  tests/test_report_only_wall.py:26 -- reads the file by constructed path
        (`.github / "workflows" / "report-only-wall.yml"`).
  REAL  tests/test_validate_hermetization.py:79 -- asserts Rule A admits this exact path.
  REAL  scripts/validate_hermetization.py:196 -- `.github/workflows` LITERAL allowlist row.
  REAL  ecosystem/parity-surfaces.yaml:649 -- id `github-ci`, probe `dir_tracked: .github`,
        tier hub=MUST.
  MENT  ARCHITECTURE.md:142,1097 (both cite the now-DELETED nightly-conformance-triage.yml
        as a live organ -- a stale citation this census surfaces but does not fix),
        CONTRIBUTING.md:195 (same stale name), PLAYBOOK:3227 (same)
disposition: keep-with-reason.

--- 7 ---------------------------------------------------------------------------
path:        config/
file:        requirements-dev.txt (41 B; three lines: pre-commit>=3.5.0, click>=8.0, pyyaml>=6.0)
genre:       dependency declaration -- SUPERSEDED
single since: a17ff959, 2026-04-27 ("chore(repo): file moves to new structure")
LEAF: yes    BITES: YES -- the sharpest case in the census. See below.
consumers of the DIRECTORY:
  REAL  ecosystem/parity-surfaces.yaml:408 -- id `shape-dir-config`, probe
        `dir_exists: config`, tier {hub: MUST, consumer: MUST}. The directory is MANDATED
        PRESENT FLEET-WIDE. Deleting it reds fleet parity in every repo.
  REAL  scripts/validate_hermetization.py:196 -- `config` LITERAL allowlist row.
consumers of the FILE:
  NONE  found. protocols/ENVIRONMENT.md:16 states the declaration is "superseded by
        ADR-106's pyproject.toml + uv.lock + .python-version". pyproject.toml:34 carries the
        epitaph in a comment ("was only in config/requirements-dev.txt").
  MENT  scripts/audit_checks/check_dot_prefix_discipline.py:28 lists "requirements-dev.txt"
        in _DOT_PREFIX_EXCEPTIONS -- classified MENTION, not consumer: that check iterates
        `repo_path.iterdir()` and is ROOT-LEVEL ONLY (its docstring says so), so it never
        sees `config/requirements-dev.txt`. A name match, not a path read.
  MENT  templates/CONTRIBUTING-md-template.md:97 -- ships `pip install -r
        config/requirements-dev.txt` to consumers; ADR-106 made that line wrong.
disposition: DIRECTORY keep-with-reason (a fleet-parity MUST) / FILE retire-candidate.
             This is the census's one real finding of substance: the folder survives Z-G5
             only because a superseded file is keeping a mandated shape directory occupied.
             Retiring the file empties a MUST-present directory, so the two cannot be
             decided separately. NOT decided here -- disposition column, not act.

--- 8 ---------------------------------------------------------------------------
path:        docs/handoffs/
file:        README.md (17,440 B) -- but 118 CHILD DIRECTORIES
genre:       canonical operator runbook (living doc)
single since: 1579fd97, 2026-06-12 -- it held up to 7 flat files; the last flat sibling was
             relocated then. The second directory that SHRANK to one.
LEAF: no     BITES: NO -- 118 subdirectories; not a file wearing a directory's clothes.
consumers:
  REAL  deploy/manifest-v{1.1.0,1.2.0,1.3.0,1.3.1,1.4.0}.yaml -- `docs/handoffs/README.md`
        is a carried, freshness_gated: true corpus entry (v1.4.0:834).
  REAL  CLAUDE.md:26 -- boot-contract first-read item 3.
  REAL  scripts/audit.py:1744,1880,1960 + scripts/verify_handoff_probes.py:228 -- iterate
        this directory to resolve the active bundle.
  REAL  .pre-commit-config.yaml:167 -- check-seal-identity over staged `docs/handoffs/**`.
disposition: keep-with-reason. Predicate A flags it; predicates B/C/D do not. Reported for
             completeness, not as a Z-G5 subject.

--- 9 ---------------------------------------------------------------------------
path:        docs/handoffs/2026-07-07-dev-knowledge-functional/
file:        FUNCTIONAL_BOOT.md (5,428 B)
genre:       immutable handoff bundle (mode=functional)
single since: 4ed36574, 2026-07-07 -- born single BY DESIGN
LEAF: yes    BITES: NO
consumers:
  REAL  scripts/gen_handoff.py:1143,1207 -- `mode="functional"` "emits ONE file,
        FUNCTIONAL_BOOT.md" (ADR-98; HANDOFF_PROCESS section 16). The one-file bundle is the
        mode's contract, not an accident.
  REAL  scripts/validate_residual_completeness.py:56-62 -- FUNCTIONAL_BOOT.md is in
        BUNDLE_FILES, so the carrier is fill-state gated.
  NOT-A-CONSUMER, measured: audit.py:1749 filters bundle candidates on
        `(d / "PROBES.md").exists()`, and this bundle has none -- so it never enters the
        handoff_probes candidate set. gen_handoff.py:690 globs
        `docs/handoffs/*/HANDOFF_BOOT.md` -- also invisible.
  MENT  zero. No tracked file cites this bundle by name or path (0 hits, both searches).
disposition: keep-with-reason -- CLAUDE.md rule 3: handoffs are IMMUTABLE. Z-G5 cannot bite
             an immutable record, and the mode is specified to produce exactly one file.

--- 10 --------------------------------------------------------------------------
path:        docs/handoffs/2026-08-17-dev-knowledge-architect/
file:        SUPPLEMENT.md (21,052 B)
genre:       immutable handoff bundle (supplement only -- an INCOMPLETE bundle)
single since: 8b3efc18, 2026-08-17 ("docs(journal): 2026-08-17 (d) -- repair the aee1b030
             anchor, and record why it broke")
LEAF: yes    BITES: NO (immutable), but it is an ANOMALY -- see below.
consumers:
  REAL  scripts/audit.py:1893,1910 -- `supplement_folded` iterates EVERY bundle directory and
        opens `bundle / "SUPPLEMENT.md"`. This bundle is a live input to that check.
  NOT-A-CONSUMER, measured: validate_residual_completeness.BUNDLE_FILES does NOT contain
        SUPPLEMENT.md, so the one file here is carrier-checked by nothing.
  MENT  zero by name or path.
anomaly: this is the only bundle in the tree holding a SUPPLEMENT and no PASTE_THIS.md,
         no HANDOFF_BOOT.md and no RESIDUAL.md. It passes `supplement_folded` silently --
         via that check's deliberate "a bundle with no PASTE_THIS.md at all (nothing was
         assembled, so no fold was missed)" carve-out (audit.py:1870-1873). A 21 KB
         supplement therefore sits gate-invisible in the tree.
disposition: keep-with-reason (immutable). The anomaly is reported, not repaired.

--- 11 --------------------------------------------------------------------------
path:        logs/
file:        TOKEN-LOG.md (6,709 B) -- TRACKED. Twelve MORE files live here untracked.
genre:       append-only record home + runtime artifact home
single since: a17ff959, 2026-04-27
LEAF: yes (in the tracked view only)    BITES: NO -- and this is a measurement caveat, not a
             judgment call
consumers:
  REAL  ecosystem/parity-surfaces.yaml:400 -- id `shape-dir-logs`, `dir_exists: logs`,
        tier {hub: MUST, consumer: MUST}: mandated present fleet-wide.
  REAL  ecosystem/parity-surfaces.yaml:853 -- id `token-log`, `path_tracked:
        logs/TOKEN-LOG.md`.
  REAL  .gitignore:26,30,35,39,43,49,55,56,57,65,89,90,96,110 -- FOURTEEN ignore rules for
        logs/* runtime artifacts (PROPOSALS-*, FLEET-HEALTH, ENFORCEMENT-COVERAGE,
        LIVED-WORKFLOW, BOUNDARY-DRIFT, FLEET-ANALYTICS, FLEET-PARITY, PARITY-EVENTS.jsonl(.1),
        OPERATOR-LOAD.csv, .session-override-token, OVERRIDES.md, COHERENCE-NUDGE.log,
        TELEMETRY.db*).
  REAL  deploy/carrier_mesh.py:17 -- "self-creates logs/ if absent"; deploy/lived_sandbox/
        cli.py:18; .claude/commands/override.md (10 hits, writes logs/OVERRIDES.md).
  REAL  scripts/validate_hermetization.py:196 -- `logs` LITERAL allowlist row.
  MENT  CLAUDE.md:60,68 / AGENTS.md:87 / ARCHITECTURE.md:297 (append-only rule)
disposition: keep-with-reason. THE MEASUREMENT CAVEAT: `logs/` is single-file ONLY under a
             `git ls-files` predicate. On any live checkout it holds up to 13 files. Any
             Z-G5 sweep run on tracked files alone will mis-flag this directory forever.

--- 12 --------------------------------------------------------------------------
path:        plugins/tier1-lifecycle/
file:        INSTALL.md (7,038 B) -- but 6 child directories, 11 files in the subtree
genre:       plugin root
single since: 9f31f321, 2026-06-02
LEAF: no     BITES: NO
consumers:
  REAL  deploy/carrier_docs.py:17 + deploy/manifest-v1.4.0.yaml:384 -- INSTALL.md is a
        deploy-carried source.
  REAL  tests/test_deploy_docs.py (8 hits) -- asserts the hub-canonical source path.
  REAL  scripts/validate_hermetization.py:196 -- `plugins/*`, `plugins/*/*` allowlist rows.
disposition: keep-with-reason. Predicate-A artefact only.

--- 13 --------------------------------------------------------------------------
path:        plugins/tier1-lifecycle/.claude-plugin/
file:        plugin.json (571 B)
genre:       plugin manifest
single since: 9f31f321, 2026-06-02
LEAF: yes    BITES: NO
consumers:
  REAL  Claude Code plugin runtime -- `<plugin>/.claude-plugin/plugin.json` is the manifest
        convention.
  REAL  deploy/release_lint.py:84 -- `PLUGIN_JSON_REL = "plugins/tier1-lifecycle/
        .claude-plugin/plugin.json"`, a hard-coded module constant.
  REAL  deploy/carrier_plugin.py:23 -- reads `version` from it (a SPEC read).
  REAL  scripts/generate_organ_index.py:492 -- globs `plugins/*/.claude-plugin/plugin.json`;
        the glob REQUIRES this directory level.
  MENT  PLAYBOOK:3161 (release procedure), ecosystem/organ-index.md:141 (generated row)
disposition: keep-with-reason -- four independent path reads, one of them a literal constant.

--- 14 --------------------------------------------------------------------------
path:        plugins/tier1-lifecycle/assets/
file:        ruff-pre-commit.yaml (1,054 B)
genre:       deployable pre-commit fragment
single since: 9f31f321, 2026-06-02
LEAF: yes    BITES: NO
consumers:
  REAL  scripts/fleet_parity.py:769 -- `if (root / "assets" / "ruff-pre-commit.yaml").
        exists():` -- a live path existence test that drives parity output.
  REAL  deploy/manifest-v1.0.0.yaml:106 -- "from assets/ruff-pre-commit.yaml -- repo/rev/hook
        verbatim"; deploy/carrier_precommit.py:6.
  REAL  ecosystem/parity-surfaces.yaml:702 -- the parity register cites the path.
  MENT  plugins/tier1-lifecycle/INSTALL.md:70
disposition: keep-with-reason -- folding it breaks a literal path read in fleet_parity.py.

--- 15 --------------------------------------------------------------------------
path:        plugins/tier1-lifecycle/hooks/
file:        hooks.json (797 B)
genre:       plugin hook manifest
single since: 9f31f321, 2026-06-02
LEAF: yes    BITES: NO
consumers:
  REAL  Claude Code plugin runtime -- `<plugin>/hooks/hooks.json` is the convention that
        arms the Stop: propose_closures hook.
  REAL  tests/test_generate_organ_index.py:512 -- fixture pins the path.
  MENT  ecosystem/organ-index.md:104 (generated row)
disposition: keep-with-reason.

--- 16 --------------------------------------------------------------------------
path:        scripts/hooks/
file:        block_immutable_edits.py (8,037 B)
genre:       PreToolUse guard (ADR-77)
single since: ec50c6c6, 2026-06-06 ("feat(hooks): block in-place edits of transcripts
             (PreToolUse guard) [#105]")
LEAF: yes    BITES: NO
consumers:
  REAL  .claude/settings.json:21 -- `python "$CLAUDE_PROJECT_DIR/scripts/hooks/
        block_immutable_edits.py"`. The path is the wiring; folding the dir disarms the hook.
  REAL  scripts/validate_hermetization.py:196 -- `scripts/hooks` LITERAL allowlist row.
  REAL  tests/test_block_immutable_edits.py -- the firing test.
  REAL  .methodology.yaml:29-40 -- component `adr77-transcript-guard`, a RULED declaration
        (2026-07-25, Lane D) that the guard STAYS ARMED even though its zone
        (docs/decisions/transcripts/**) was deleted 2026-07-22.
  MENT  ARCHITECTURE.md:411, ecosystem/organ-index.md:96, parity-surfaces.yaml:504
disposition: keep-with-reason -- and note the recursion: this directory holds a guard that is
             itself deliberately kept armed over a zone that no longer exists. Its
             single-file state is downstream of a recorded ruling, not of neglect.

--- 17 --------------------------------------------------------------------------
path:        templates/handoff/functional/
file:        FUNCTIONAL_BOOT.md.tmpl (3,667 B)
genre:       handoff mode template
single since: 5617fe17, 2026-07-06 ("feat(handoff): --mode functional (one-file intake boot)
             + --mode developer alias [#268]")
LEAF: yes    BITES: MARGINALLY -- the census's clearest "file wearing a directory's clothes"
             that is not protected by an external convention
consumers:
  REAL  scripts/gen_handoff.py:99 -- `_TMPL_DIR_FUNCTIONAL = _REPO_ROOT / "templates" /
        "handoff" / "functional"`, a hard-coded module constant, used at :1214 via
        `_render("FUNCTIONAL_BOOT.md.tmpl", ..., tmpl_dir=...)`.
  REAL  scripts/validate_hermetization.py:196 -- `templates/handoff/*` allowlist row.
  MENT  protocols/HANDOFF_PROCESS.md:950, PLAYBOOK:4704, .claude/commands/handoff.md:50
sibling shape: templates/handoff/ holds 8 flat .tmpl files plus three mode dirs --
             epic/ (3 files), v5/ (5 files), functional/ (1 file).
disposition: keep-with-reason -- taxonomy symmetry with epic/ and v5/, plus a literal path
             constant. But this is the one entry where the reason is CONVENTION rather than
             a hard external contract, so it is the honest candidate if the operator ever
             wants Z-G5 to actually cost something.

--- 18..23 ----------------------------------------------------------------------
SIX test-fixture directories. Grouped because the analysis is identical.

  18  tests/fixtures/codemap-arch-nomarkers/src/pkg_a/      __init__.py    (leaf)
  19  tests/fixtures/codemap-simple-repo/                   pyproject.toml (1 subdir)
  20  tests/fixtures/codemap-with-cycle/                    pyproject.toml (1 subdir)
  21  tests/fixtures/codemap-with-orphan/                   pyproject.toml (1 subdir)
  22  tests/fixtures/codemap-with-orphan/src/pkg_orphan/    __init__.py    (leaf)
  23  tests/fixtures/repo-with-structural-checks/src/my_pkg/ __init__.py   (leaf)

genre:       synthetic repository fixtures
single since: 541b7c8f / fb02241d / 9d93ad0a (all 2026-05-22, the codemap build arc) and
             c0b75124 (2026-05-17, "refactor(tests): rename fixture to
             repo-with-structural-checks")
BITES: NO for all six.
consumers:
  REAL  tests/test_codemap.py:20,183,184,228 -- module-level constants SIMPLE_REPO,
        WITH_ORPHAN, WITH_CYCLE, ARCH_NOMARKERS bind these fixture roots by name.
  REAL  tests/test_codemap.py:206 -- asserts the rendered row
        `| pkg_orphan | - | src/pkg_orphan/ | orphan |`: the DIRECTORY NAME is the assertion.
  REAL  tests/test_probe_child_backlogs.py:148 + tests/test_audit.py:65 --
        repo-with-structural-checks bound by path.
  REAL  scripts/validate_hermetization.py:196 -- `tests/fixtures/**` allowlist row.
disposition: keep-with-reason, all six. A Python package directory containing only
             __init__.py, and a fixture repo root containing only pyproject.toml, are
             SHAPES THE FIXTURE IS TESTING. Folding any of them changes what the test
             asserts. Z-G5's own wording -- "a file wearing a directory's clothes" -- does
             not describe a package marker.


DISPOSITION SUMMARY
-------------------
fold                : 0
retire              : 0
retire-candidate    : 1  (config/requirements-dev.txt -- the FILE only; its DIRECTORY is a
                          fleet-parity MUST, so the two are coupled)
keep-with-reason    : 22
Z-G5 bites          : 1 clearly (config/), 1 marginally (templates/handoff/functional/),
                      21 not at all.

That ratio IS the finding. Applied to the whole tracked tree, Z-G5 -- "no single-file
folders, ever" -- produces essentially no work: every folder it flags is either an external
runtime contract, an immutable record, a mandated shape directory, a test fixture asserting
its own shape, or a predicate artefact.


DONE-CONTRACT ITEM 4 -- THE Z-G5 EXCEPTIONS THE REPO ALREADY GRANTED IMPLICITLY
-------------------------------------------------------------------------------
The exceptions are not scattered and undiscoverable. They are enumerated in ONE place that
predates Z-G5 by eighteen days and was written for a different purpose:
`scripts/validate_hermetization.py::_HOME_PATTERNS` (:194-247), the Rule C home allowlist,
operator ruling A of 2026-08-11, register K-1.

EVERY ONE of the 23 directories is admitted by an explicit row there. Six are admitted as
BARE LITERALS -- an allowlist row that exists for exactly one directory holding exactly one
file:

  literal row        directory it admits          one file it holds
  .claude-plugin     .claude-plugin/              marketplace.json
  .github/workflows  .github/workflows/           report-only-wall.yml
  config             config/                      requirements-dev.txt
  logs               logs/                        TOKEN-LOG.md (tracked)
  scripts/hooks      scripts/hooks/               block_immutable_edits.py
  codex              -- NOTHING. SEE BELOW.

The remaining seventeen are admitted by wildcard rows: `.claude/*`, `.claude/skills/*`,
`plugins/*`, `plugins/*/*`, `templates/handoff/*`, `tests/fixtures/**`, `docs/handoffs/**`.

So the answer to done-contract item 4, stated precisely: the repo granted its Z-G5
exceptions on 2026-08-11, eighteen days before Z-G5 was ruled, by writing a home allowlist
derived from the live taxonomy. Z-G5 (2026-08-29) and Rule C (2026-08-11) are in tension by
construction -- Rule C's job is to ADMIT every home the tree already occupies, Z-G5's job is
to REFUSE the single-file ones -- and no organ reconciles them. That is not a rule-vs-ruling
conflict requiring escalation (Rule C admits; it does not mandate), so it is reported here
rather than raised under decision-budget class (b). But it is why Z-G5 currently has no
enforcement surface: the only gate that looks at directory homes is the one designed to say
yes to all of these.

THE DANGLING ROW -- the census's one actionable defect
  `scripts/validate_hermetization.py:206` still carries the literal home `codex`.
  Measured: `git ls-files codex` returns 0 paths. `codex/AGENTS.md` was removed in 8626db28
  on 2026-08-29 -- the SAME DAY Z-G5 was ruled naming `codex/` as its first live subject.
  The fold happened; the allowlist row did not follow.

  WHY NOTHING CAUGHT IT. The anti-drift test is one-directional. The module comment at
  :177-181 claims "every pattern below is a home that tracked files already occupy at the
  time of writing, and `test_rule_c_admits_every_tracked_path` asserts exactly that". The
  test (tests/test_validate_hermetization.py:399-411) asserts the CONVERSE: every tracked
  path is admitted by some pattern. Nothing asserts that every pattern still corresponds to
  a live home. So a fold can retire a directory and leave its allowlist row standing green
  forever -- and re-creating `codex/` today would be admitted silently, which is the exact
  outcome Z-G5's discharge was meant to prevent.

  Reported, not repaired: this lane writes no tree file.

  Also stale, same class, surfaced but not fixed: ARCHITECTURE.md:1097, CONTRIBUTING.md:195
  and PLAYBOOK:3227 all cite `.github/workflows/nightly-conformance-triage.yml` as a live
  organ. It was deleted 2026-07-08 (82227f08) -- which is what made `.github/workflows/` a
  single-file folder in the first place.


WHAT THIS LANE DID NOT DO
-------------------------
  - wrote no tree file, staged nothing, committed nothing, pushed nothing
  - ran no gate and asserts no gate result
  - added no JOURNAL entry, regenerated no index, ruled on nothing, deleted nothing
  - escalated nothing: no decision-budget class (a), (b) or (c) was triggered
  - `git status --porcelain` is empty and HEAD is unmoved at ec8731a9

END PACKET
```