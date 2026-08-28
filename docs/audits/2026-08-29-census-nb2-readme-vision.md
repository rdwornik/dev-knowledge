# NB2 · CLOUD C5 — README/VISION consumer census

**Lane:** night-batch-2 · cloud · READ-ONLY · repo `dev-knowledge` · clone at `origin/main` = `fcc9485567f81814d24b84fe2db5ceff23b743ee` ("Merge branch 'docs/batch-2-dispatch' -- night-batch-2 frozen…").
**Writes performed:** zero. No file created, edited, deleted, staged, committed, branched, pushed or tagged. `git status --porcelain` was empty at open and nothing in this lane changed that.
**Gates run:** none. Container `uv 0.8.17` vs `pyproject.toml required-version = "==0.11.19"` — every gate-dependent claim below is marked `MEASUREMENT-OWED-LOCAL`.
**Contract of record:** `docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C5-readme-vision.md` — read and verified byte-for-byte identical to the brief I was given.

---

## 0. The two constraints, quoted, and how this proposal respects them

**Constraint 1 — the root `README.md` deletion.** Binding line, `CLAUDE.md:99`:

> 5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.

Its source, `docs/decisions/ADR-38-universal-repo-architecture.md:303–309` (amendment A5, Delta 4):

> **Delta 4 — README.md deprecated from mandatory baseline.** `README.md` is removed from the mandatory baseline — operator decision 2026-05-23, option A (deprecated universally; optional for repos with an external audience). Rationale: for internal-only repos, README content is redundant with `VISION.md` (purpose), `CLAUDE.md` (how to work with the repo), and `ARCHITECTURE.md` (what exists). Repos that serve an external audience MAY keep a README.

**Constraint 2 — ADR-114 is PARKED.** Binding line, `docs/decisions/ADR-114-readme-recreation-legality.md`, Decision section:

> **Decision: PARKED** — *revisit only if A2's `AGENTS.md` track fails the universal-entry purpose.* Priced: fleet parity ×9, 104/114 immutable bundles, 69 `PROBES`, and the `## Vision` H2 spine as a second migration axis (unpriced by R2, priced here).

and, from the retained operator ruling in the same section:

> **Until it is ruled, nothing in this repo may cite ADR-114 as authority**, and the `README.md` prohibition stands unchanged.

**How the proposal below respects both.** Every merge in §7 is a *pointer collapse inside already-existing mutable prose*. Not one of them creates a file, and no proposal target is a new root-level document. §7 proposes **zero** edits to `VISION.md`, so the ADR-114 substitution question is not answered, nudged, or made cheaper by side effect; the three sites it *does* propose to correct (`protocols/PLAYBOOK.md:1072`, `:1259`, `:4789`) each currently assert that a root README exists and is *"Living, never delete"* — correcting them makes the standing prohibition **more** consistent, never less. §8 explicitly names and **withdraws** the one merge that would have amounted to a root README by another name. ADR-114 is cited below only as a *measurement source and a recorded state*, never as authority for an action.

---

## 1. Method — and what counts as a "reference"

The corpus is too large for eyeball enumeration (§2), so every claim here comes from one of three mechanical passes, each reproducible:

1. **Occurrence census** — `grep -rn` over the whole tree excluding `.git`.
2. **Path-token resolution** — a Python pass over `git ls-files` extracting every path-shaped token matching `…README….(md|tmpl)` and testing `os.path.exists()` on it. This is what turns "a mention" into LIVE-or-DANGLING mechanically rather than by reading.
3. **Stratum split** — every hit tagged MUTABLE vs IMMUTABLE/APPEND-ONLY (`docs/audits/`, `docs/handoffs/`, `docs/decisions/`, `docs/archive/`, `docs/intake/`, `ecosystem/`, `JOURNAL.md`, `LESSONS.md`), because a reference in an immutable artifact is **not actionable by construction** — `CLAUDE.md` §5 rule 3 forbids editing it — and pooling the two strata is how a census produces an unusable proposal.

**The single most important structural fact, and it decides the whole proposal:**

```
grep -rnE "\]\([^)]*README[^)]*\)" --binary-files=without-match . --exclude-dir=.git | wc -l   -> 0
grep -rnE "\]\([^)]*VISION\.md[^)]*\)" --binary-files=without-match . --exclude-dir=.git | wc -l -> 0
```

**Zero markdown links, to either file, anywhere in the tree.** Every one of the ~5,900 references censused below is prose, a code literal, a YAML value, or a shell command — never a link. `ADR-114` measured the same for `VISION.md` alone nine days earlier and drew the correct conclusion, which now extends to README as well: *nothing in this repo can mechanically detect a broken canonical-doc reference.* There is no link checker to satisfy and none to break. Consequently **no merge below can be justified as "fixing a broken link"** — the only defensible justifications are contradiction, duplication and gate coupling.

---

## 2. Measured baseline

```
== tree-wide occurrences (grep -rn … --exclude-dir=.git | wc -l) ==
VISION.md    2,024 occurrences across   703 files
README       3,857 occurrences across   956 files

== VISION.md by top-level location ==
docs/          1,466      protocols/       27      CLAUDE.md         3
ecosystem/       322      scripts/         14      VISION.md         1
tests/            91      deploy/           5      .code-workspace   1
JOURNAL.md        54      tasks/            4
templates/        27      .claude/          3      LESSONS.md        6

== README by top-level location ==
docs/          2,774      protocols/       88      LESSONS.md       11
JOURNAL.md       550      tasks/           32      ARCHITECTURE.md   7
tests/           169      templates/       27      CLAUDE.md         5
scripts/         134      deploy/          19      BACKLOG.md        4
                          ecosystem/       17      .pre-commit-…     4
                          .claude/         11      CONTRIBUTING.md   2
                                                   .gitattributes    2
                                                   VISION.md         1

== docs/ interior split ==
VISION.md:  handoffs 800 · audits 571 · decisions 90 · intake 5
README:     audits 1,397 · handoffs 1,210 · decisions 97 · intake 51 · archive 19
```

**Drift against ADR-114's own measurement** (taken at `ff01fd10`, reported in its §"measurement 2"): `1,956 / 678` then, `2,024 / 703` now. **The corpus grew ~3.5 % in files and the shape did not change** — still zero links, still ~90 % immutable. ADR-114's derived figures moved the same way and are restated below with both values.

```
                                   ADR-114 @ ff01fd10   this clone @ fcc9485
handoff bundles, total                    114                  117
bundles referencing VISION.md             104                  107
PROBES-named files citing VISION.md        69                   72
bundles referencing a README                —                  115
```

**Clone-vs-disk reconciliation** (the brief's standing clause asks for both when they disagree):

```
                        brief (operator disk, 2026-08-28 23:36)   this clone (fcc9485)
docs/intake/*.md                       56                                56   ==
docs/decisions/*.md                    89                                89   ==
docs/audits/*.md                      769                               773   (772 excl. README.md)
tasks/**/*.md                         344                               344   ==
BACKLOG.md bytes                   67,883                            67,883   ==
```

`docs/audits/` is the one disagreement and the clone is **ahead**, not behind: the night-batch-2 dispatch commits `e23e001`/`8882638`/`fcc9485` landed after the operator's 23:36 measurement, adding `2026-08-28-technical-batch-2-manifest.md` and siblings. Both figures are correct as of their own timestamps; I report the clone's.

---

## 3. Census A — references INTO `VISION.md`

### A.1 The mutable, actionable surface (the whole of it)

Only **~55 of 2,024** `VISION.md` occurrences sit in files this repo permits editing. Here is that set in full, by class.

```
CLASS   SITE                                          TEXT / PURPOSE                                              RESOLVES
-----   ----                                          --------------                                              --------
GATED   scripts/canonical_docs.py:41                  VISION = "VISION.md" — the registry's root constant;         yes
                                                      ten machine constants read it. Gate: every check below.
GATED   scripts/canonical_docs.py:67                  CANONICAL_MANDATORY tuple. Gate: check_adr38_baseline,       yes
                                                      check_canonical_md_visibility, validate_hermetization
                                                      Rule A (SANCTIONED_TIER1_FILES splats it, :103).
GATED   scripts/canonical_docs.py:82                  FRESHNESS_FILES — VISION is FIRST. Gate:                     yes
                                                      canonical_freshness_gate + audit.py check #10.
GATED   scripts/canonical_docs.py:86 / :95            SECTION_HISTORY_DOCS / STRUCTURE_DOCS. Gate:                 yes
                                                      validate_doc_rot:132, validate_doc_structure:77.
GATED   scripts/canonical_docs.py:100                 BACKPRESSURE_CANON. Gate: session_end_backpressure.          yes
GATED   scripts/canonical_docs.py:105                 CONFORMANCE_V2_SCAN (R2 seam S11).                           yes
GATED   scripts/canonical_docs.py:112                 CANONICAL_SPINE[VISION] = the five ## H2s.                   yes
                                                      Gate: check_canonical_structure + 5 deploy manifests.
GATED   scripts/audit_checks/check_vision_md.py:26-27 "VISION.md presence + parseable YAML frontmatter per         yes
                                                      ADR-33." Gate input. audit.py check #1.
GATED   scripts/canonical_freshness_gate.py:49        DEFAULT_FRESHNESS_FILES literal (deploy-carried              yes
                                                      SOFT-import fallback; pinned by test_canonical_docs).
GATED   scripts/session_end_backpressure.py:145       _CANON literal (same soft-import fallback pattern).          yes
GATED   scripts/gen_handoff.py:516-528                _vision_extract — CONTENT dependency: regex-matches          yes
                                                      `## Vision` and copies the body into every handoff
                                                      bundle. Degrades to a literal string, never raises.
GATED   scripts/gen_handoff.py:612 / :1002            doc_rot probe operand; VISION_EXTRACT template slot.         yes
GATED   scripts/consumer_at_landing.py:124            landing-check canonical tuple.                               yes
GATED   scripts/nopack_sandbox.py:226                 sandbox seed file list.                                      yes
GATED   .claude/workflows/conformance-hub.js:133      JS string list — cannot import Python; held in              yes
                                                      agreement by tests/test_canonical_docs.py only.
GATED   ecosystem/parity-surfaces.yaml:140-150        id: canonical-doc-vision, probe path_tracked VISION.md,      yes
                                                      tier {hub: MUST, consumer: MUST} — the ×9 fleet coupling.
GATED   deploy/manifest-v{1.1.0,1.2.0,1.3.0,1.3.1,    doc_shapes: VISION.md: spine + freshness_gated: true.        yes
        1.4.0}.yaml (:389/:604/:669/:678/:810)        FIVE manifest versions, all live.
GATED   ecosystem/disposition-register.yaml:113,255   match keys "VISION.md -> handoff-process" and                yes
                                                      "VISION.md -> prompt-template" — RATIFIED
                                                      PERMANENT-DEFER. Gate: scan_undeclared_edges WARNs
                                                      resurface undispositioned if these keys move.
GATED   templates/handoff/v5/PROBES.md.tmpl:81        P1a: verification command `grep -A4 '^## Vision'             yes
                                                      VISION.md`. Renders into every new bundle.
GATED   docs/handoffs/2026-08-28-dev-knowledge-       P1a, live, in the ACTIVE bundle. This is the one             yes
        architect/PROBES.md:64                        bundle check_handoff_probes actually validates.
GATED   tests/ (91 occurrences; test_verify_handoff_  assertions over presence, frontmatter, freshness,            yes
        probes 33 · test_audit 23 · test_fleet_        spine, parity.
        parity 16 · test_canonical_docs 4 · …)
LIVE    protocols/ESSENTIALS.md:10                    "Mission anchor: `VISION.md` (universal brain) +             yes
                                                      `ARCHITECTURE.md`" — navigation, boot-time.
LIVE    protocols/HANDOFF_BOOT.md:116                 orientation source for the browser seat.                     yes
LIVE    protocols/HANDOFF_PROCESS.md:506, :931        the v6 orienting line + vision-extract spec.                 yes
LIVE    protocols/DEFINITION_OF_DONE.md:148           names VISION among the not-per-session-mandatory set.        yes
LIVE    protocols/ENVIRONMENT.md:181                  tree diagram row "VISION.md ← Mission, scope, …".            yes
LIVE    protocols/PLAYBOOK.md:1093                    file-presence table: "mandatory (ADR-33…)".                  yes
LIVE    protocols/PLAYBOOK.md:3050, :4633, :4830      lifecycle posture / routing / no-Mermaid rules.              yes
LIVE    protocols/PLAYBOOK.md:586, :3580              env-var doc home; scaffold `touch` line.                     yes
LIVE    CLAUDE.md:40, :60, :68                        critical-paths, naming, file-lifecycle.                      yes
LIVE    templates/child-methodology-floor.md.tmpl:40  child-repo floor pointer.                                    yes
LIVE    templates/handoff/03_PROJECT.md.tmpl:15       v4 source pointer (v4 retained per ADR-83).                  yes
LIVE    .claude/commands/handoff.md:111               orientation-probe instruction.                               yes
LIVE    .claude/commands/handoff-verify.md:99         "Orientation: vision | VISION.md ## Vision opening           yes
                                                      sentence, substring-checked".
LIVE    VISION.md:126                                 self-reference: "every project under `Dev/` should           yes
                                                      have its own `VISION.md`".
LIVE    tasks/ (4 occurrences)                        ticket descriptions.                                         yes
```

### A.2 The immutable stratum

```
docs/handoffs/   800 occurrences · 107 of 117 bundles · 72 PROBES files   IMMUTABLE (CLAUDE.md §5 r3)
docs/audits/     571 occurrences                                          IMMUTABLE
docs/decisions/   90 occurrences                                          IMMUTABLE
ecosystem/       322 occurrences (index.yaml 17 quote past audit findings) DERIVED / history
JOURNAL.md        54 · LESSONS.md 6                                        APPEND-ONLY
```

**≈ 92 % of all `VISION.md` references (1,843 of 2,024) are in files this repo forbids editing.** That is not a finding to fix; it is the boundary condition every proposal in §7 has to respect.

### A.3 Two things absent that a reader would expect

- **`ARCHITECTURE.md` cites `VISION.md` zero times.** `grep -n "VISION\.md" ARCHITECTURE.md` returns nothing; the only three `VISION` strings (`:925`, `:1010`, `:1150`) are the bare word inside a lifecycle table, a prose sentence and an ADR roster.
- **`VISION.md`'s own `## References` section (`VISION.md:184–192`) does not cite `ARCHITECTURE.md`.** It lists ESSENTIALS, PLAYBOOK, JOURNAL, BACKLOG, CONTRIBUTING, `docs/decisions/` and ADR-88.

So the two mandatory canonical living docs — the pair ADR-38 A5 named as jointly replacing the README — carry **no mutual pointer in either direction**. Classified `REDUNDANT`-adjacent below; it is a gap, not a merge, and §7 prices it honestly rather than smuggling it in.

---

## 4. Census B — references to a README

### B.1 Path-token resolution: 84 distinct README path tokens

Mechanical pass over `git ls-files`. Every token tested with `os.path.exists()`.

```
OCCUR  RESOLVES  TOKEN                                            CLASS
  818  ABSENT    README.md                (bare — split in B.2)   mixed
  491  EXISTS    docs/audits/README.md                            GATED
  455  EXISTS    docs/handoffs/README.md                          GATED
  343  EXISTS    docs/decisions/README.md                         GATED
  325  EXISTS    docs/intake/README.md                            GATED
   81  ABSENT    00_README.md             (bare, v3.x bundle-rel) resolves in ctx
   49  EXISTS    protocols/README.md                              LIVE
   36  EXISTS    tasks/README.md                                  LIVE
   35  EXISTS    templates/handoff/v5/README.md.tmpl              LIVE (stub)
   31  EXISTS    docs/archive/README.md                           LIVE
   13  ABSENT    README.md.tmpl           (bare, template-rel)    resolves in ctx
   12  EXISTS    tests/fixtures/README.md                         LIVE
   11  ABSENT    docs/research/README.md                          DANGLING
    9  EXISTS    templates/handoff/README.md.tmpl                 LIVE (ADR-83)
    9  ABSENT    docs/tech-radar/README.md                        DANGLING
    6  ABSENT    ai-council/README.md                             cross-repo
    4  ABSENT    codex-review.README.md                           L0, out of repo
    4  ABSENT    corp-ops/README.md · corp-sca/README.md          cross-repo
    3  ABSENT    docs/README.md                                   test literal
    2  ABSENT    scripts/README.md                                test literal
    1  ABSENT    docs/handoffs/2026-08-12-dev-knowledge-          test literal
                 architect/README.md                              (vh Rule C fixture)
   —  EXISTS     35 per-bundle READMEs (20 × README.md v4-era,    IMMUTABLE
                 15 × 00_README.md v3.x-era)
   —  ABSENT     16 × src/corp/*/README.md, a/…, b/…, actions/…   cross-repo / fixtures
```

Reproduce:

```bash
python3 - <<'PY'
import re, subprocess, os, collections
files = subprocess.run(["git","ls-files"],capture_output=True,text=True).stdout.split()
pat = re.compile(r'(?<![A-Za-z0-9_./-])((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]*README[A-Za-z0-9_.-]*\.(?:md|tmpl))')
tok = collections.Counter()
for f in files:
    if not os.path.isfile(f): continue
    for line in open(f, encoding='utf-8', errors='replace'):
        for m in pat.finditer(line): tok[m.group(1)] += 1
for t,c in tok.most_common():
    print(f"{c:6d}  {'EXISTS ' if os.path.exists(t) else 'ABSENT '} {t}")
PY
```

### B.2 The bare `README.md` token — 818 occurrences, split by stratum

```
IMMUTABLE / APPEND-ONLY   638   (78.0 %)   not actionable — CLAUDE.md §5 rules 1-3
MUTABLE                   180   (22.0 %)   enumerated below
```

The 180 mutable ones break down as:

```
tests/       98    fixture literals, absence assertions, round-trip proofs
scripts/     57    generator/gate literals (gen_intake_tree alone: 28)
protocols/   15    PLAYBOOK 5 · ENVIRONMENT 2 · STANDING_RULINGS 1 · archive/HP_v4.4 7
root docs/    4    ARCHITECTURE 2 · CLAUDE 2
other/        6    generated roster 1 · templates 3 · tasks 2
```

Of those 180, exactly **~20 denote the deleted root `README.md` of this repo.** The rest denote a genre index, a bundle file, a template, or a synthetic fixture. That distinction is the whole census: a naive `grep README` returns 3,857 hits and implies a crisis; the resolved, stratified count leaves twenty sites and three defects.

### B.3 The living genre-index READMEs — all resolve, all load-bearing

```
FILE                      GATE(S) THAT READ IT                                          CLASS
docs/audits/README.md     gen_audit_index.py:48 (_TARGET) + pre-commit                  GATED
                          `audit-index-freshness` (--check) + generated_artifact_
                          freshness.py:183 + .gitattributes:51 `merge=ours`
docs/intake/README.md     gen_intake_index.py:32 (_TARGET) + pre-commit                 GATED
                          `intake-index-freshness` + gen_intake_tree.py:88 (_SOURCE,
                          lossless round-trip + manifest sha256) + deploy carrier
                          (manifest-v1.4.0.yaml:372,402) + disposition-register:189
docs/handoffs/README.md   canonical_docs.py:62 HANDOFFS_README_PATH -> FRESHNESS_FILES  GATED
                          + canonical_freshness_gate.py:50 + seed_runbook.py:40
                          (_SOURCE_README, fleet seeding) + gen_handoff.py:618
                          + scan_undeclared_edges.py:82 _LIVING_ALLOWLIST
                          + validate_reconciliation `reconciled_with:
                          handoff-process@6.3.0` + check_seal_identity.py:46
docs/decisions/README.md  validate_adr_status.py:757 + check_adr_status_grammar.py:88   GATED
                          + ecosystem/doc-code-edge.yaml:31,80 declared edge
                          `governance-adr-status` + scan_undeclared_edges allowlist
docs/archive/README.md    ADR-60 retention rule; STANDING_RULINGS:2950,2975 adds        LIVE
                          the `exempt-permanent` class to it
protocols/README.md       carries `reconciled_with: handoff-process@6.3.0`;             GATED
                          named at HANDOFF_PROCESS.md:1072-1073 as the sixth
                          reconciliation dependent
tasks/README.md           the SOURCE-OF-TRUTH runbook for the generated BACKLOG.md;     LIVE
                          PLAYBOOK:4572,4631 and AI_COUNCIL_PROCESS:377 point at it
tests/fixtures/README.md  fixture catalogue                                             LIVE
```

**None of these eight is a merge candidate.** Six are gate inputs and two are runbooks; merging any of them breaks a regen-and-diff gate, a deploy carrier or a fleet seeder. Naming that up front is what stops a "collapse the READMEs" proposal from being written.

---

## 5. The DANGLING set — the actionable output

Seven items. Ranked by whether a reader acting on them would be misled.

### D-1 · `protocols/PLAYBOOK.md:4789` — asserts a root README exists and may never be deleted

```
| Project docs      | Root            | CLAUDE.md, README.md                           | Living, never delete           |
```

**FOR:** doctrine — the markdown-file taxonomy that opens *"Every markdown file in the project falls into exactly one category. If you're about to create a .md file and it doesn't fit any category below — it probably shouldn't exist."*
**RESOLVES:** no. Root `README.md` is absent and prohibited. *"Living, never delete"* is falsified by an operator decision that deleted it three months ago.
**Severity:** highest of the seven. This is the only site in the corpus that reads as **positive authority to create** a root README — in the universal file, in a table a contributor is told to check before creating any `.md`.

### D-2 · `protocols/PLAYBOOK.md:1259` — lists README first among living in-place docs

```
- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT.
```

**FOR:** doctrine — the file-lifecycle enumeration.
**RESOLVES:** no. `CLAUDE.md:68` gives the same enumeration without README (`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`). Two canonical files, same list, one carries a deleted file.

### D-3 · `protocols/PLAYBOOK.md:1072` — full taxonomy row, no deprecation marker

```
| `README.md` | User-first navigation, what is this repo | Prose + folder layout | When repo state shifts notably | Rob, future contributors | Living (rewrite) | Per-repo |
```

**FOR:** doctrine — the "what does each documentation file do" table.
**RESOLVES:** partially. As *universal per-repo* doctrine the row is defensible (A5 keeps README OPTIONAL for external-audience repos). But `CHANGELOG.md` two rows below carries an explicit `RETIRED ecosystem-wide (ADR-49) … row kept for legacy context` marker and README carries **nothing** — so the same table marks one deprecated file and silently presents the other as current, **25 lines above `:1097`, which states the opposite in the same file**:

```
| `README.md` | optional — external-audience repos only (deprecated from baseline) |
```

`:1097` is the correct statement and is the nearest canonical restatement of ADR-38 A5.

### D-4 · `docs/decisions/ADR-114-…:` — both of its own locators have drifted

ADR-114's Decommission clause names three surfaces to retire if it is ever accepted. Two do not resolve at `fcc9485`:

```
CITED                                   ACTUAL AT fcc9485
ecosystem/parity-surfaces.yaml:133-139  the canonical-doc-vision surface is at :140-150.
                                        :133-139 is now the pre-deploy fleet-role reason
                                        block (terminal-setup / win-tooling).
ARCHITECTURE.md:366                     :364-368 is gen_dashboard R3 findings F5/F3.
                                        `grep -n "recreate" ARCHITECTURE.md` -> NO MATCH.
                                        The nearest surviving statement is ARCHITECTURE.md:478
                                        ("root `README.md` deleted 2026-05-23"), which states
                                        the deletion but is NOT the "do not recreate it" echo
                                        the ADR says it is.
```

**FOR:** a gate input in the strongest sense — these are the sites a future ratification commit is instructed to edit.
**RESOLVES:** no. **Not repairable:** ADRs are immutable (`CLAUDE.md` §5 rule 3), and ADR-94's in-place exception covers the *status line only*. This is exactly the class `CLAUDE.md` §4 warns about — *"Resolve a locator before you act on it… that audit's own replacement locator was itself off by one — the rule binds the auditor too."* The disposition is to record the correction externally, not to touch the ADR.

### D-5 · `docs/research/README.md` — 11 references, genre folder gone

`ls docs/` returns `archive audits decisions handoffs intake`. No `research/`.

```
docs/audits/2026-05-25-council-pipeline-discovery.md:58   "`docs/research/README.md:4-7` — archives …"
docs/audits/2026-05-25-council-pipeline-audit.md:27       "`docs/research/README.md:4-7` and
                                                           `PLAYBOOK.md:532,1505` define `research/`…"
JOURNAL.md:24238                                          "`docs/research/README.md` (rewritten)"
+ 8 × docs/handoffs/*/08_TREE.txt inventory rows
```

**FOR:** evidence citation (the two audits cite it by `path:line` as their source of a definition).
**RESOLVES:** no. **Not repairable** — every citing file is immutable or append-only. Correctly a *record* of a folder that existed, but a reader following the locator gets nothing.

### D-6 · `docs/tech-radar/README.md` — 9 references, same shape

```
docs/audits/2026-05-25-council-pipeline-discovery.md:107   "`docs/tech-radar/README.md:1-3` —
                                                            'quarterly inventory of tools, models…'"
+ 8 × docs/handoffs/*/08_TREE.txt inventory rows
```

Same class, same disposition as D-5.

### D-7 · 82 of 117 handoff bundles carry no README, and a live gate looks for one in each

```bash
ls -d docs/handoffs/*/ | wc -l                      -> 117
ls docs/handoffs/*/README.md    2>/dev/null | wc -l ->  20   (v4 era)
ls docs/handoffs/*/00_README.md 2>/dev/null | wc -l ->  15   (v3.x era)
#                                              without ->  82
```

`scripts/audit_checks/check_handoff_bundle_structure.py:71-73` opens `d / "README.md"` for every bundle dir and `continue`s when it is missing. `_BUNDLE_REQUIRED_FILES` at `:28` still leads with `"README.md"`.

**This is DANGLING-by-design, not a defect** — the docstring at `:41-59` states it explicitly (*"v5 bundles carry no v4 stamp, so they are skipped here by design"*), and `protocols/HANDOFF_PROCESS.md:760-761` fixes the v5+ bundle at four files with **no README**. I list it because a census that reported "82 bundles missing a required file" without reading the docstring would be the exact false-positive this lane is supposed to avoid. **The honest statement: the check's README dependency can never fire on new work — its governed set is frozen at 20 bundles and cannot grow.**

### Not DANGLING, checked and cleared

- `templates/handoff/README.md.tmpl` (v4) — **retained deliberately.** `.claude/commands/handoff.md:196` : *"**Templates (retained live):** `templates/handoff/README.md.tmpl` … kept for cross-repo v4 per ADR-83"*. A proposal to remove it is refused by a ratified ADR.
- `templates/handoff/v5/README.md.tmpl` — a self-declaring `DEFERRED STUB` (`:1`) whose phantom-source claim was the subject of `[#399]`, **closed**, and discharged by `protocols/STANDING_RULINGS.md:2638` **T-35**. Already owned; ADR-111 routes this OWNED, not a new row.
- `scripts/canonical_docs.py:54,73` (`README = "README.md"` in `CANONICAL_OPTIONAL`) and `scripts/audit_checks/check_dot_prefix_discipline.py:33` — constants naming an absent file **on purpose**: presence is required only for `CANONICAL_MANDATORY`; these check *casing when present*. `tests/test_audit.py:193-194` pins it: *"README.md is optional post-amendment (A5) — its absence does not fail the check."*
- `~/.claude/bin/codex-review.README.md` (`PLAYBOOK:4886`) — L0, outside this repo; `STANDING_RULINGS:2216` already records it as superseded in practice.

---

## 6. GATED — what a gate would notice

`VISION.md` is read by **ten machine constants plus one JS seam**, all now routed through `scripts/canonical_docs.py`:

```
check_vision_md · check_adr38_baseline · check_canonical_md_visibility · check_canonical_structure
canonical_freshness_gate · validate_doc_rot · validate_doc_structure · validate_hermetization
session_end_backpressure · gen_handoff        + .claude/workflows/conformance-hub.js:133
```

Confirmed by `grep -rln "canonical_docs" scripts/ .claude/ deploy/ tests/` → 13 scripts + 2 tests.

**The specific cost of touching `VISION.md`:** its frontmatter reads `last_reviewed: 2026-08-23` (`VISION.md:4`). `CLAUDE.md` §4 Freshness-cadence: *"A `last_reviewed` stamp means re-read end-to-end and confirmed accurate (or drift filed) — not merely 'touched'. `audit.py` check #10 fails when a stamp predates the file's last edit."* So **any** edit to `VISION.md` — including a one-line pointer addition — obliges a full end-to-end re-read plus a stamp bump, or the commit is blocked. It is `FRESHNESS_FILES[0]`, and `tests/test_enforcement_coverage.py:448-462` exists precisely because that first entry was a live-fire miss once.

Beyond the gate mesh: `ecosystem/parity-surfaces.yaml:140-143` holds `VISION.md` at `tier: {hub: MUST, consumer: MUST}` across the nine ADR-104 fleet members, and five deploy manifests pin its `## H2` spine. Both make the *filename* a fleet-wide coupling — which is ADR-114's measurement 1 and is not reopened here.

`docs/handoffs/README.md` is the second freshness-stamped README (`last_reviewed: 2026-08-28`, `reconciled_with: handoff-process@6.3.0`) and carries the heaviest coupling of the eight genre indices: freshness gate + fleet seeder + undeclared-edge allowlist + reconciliation registry.

---

## 7. The merge-ready proposal

**Scope discipline, stated before the proposal.** Of ~5,881 total references censused, ~5,700 are immutable, append-only, generated, or gate-coupled. The mergeable surface is **five lines in one file**. A proposal larger than that would be describing work the repo forbids.

### Merge M1 — collapse `PLAYBOOK:4789` and `PLAYBOOK:1259` onto `PLAYBOOK:1097`

**Single site of record:** `protocols/PLAYBOOK.md:1097` — `| README.md | optional — external-audience repos only (deprecated from baseline) |`, which restates ADR-38 A5 Delta 4 correctly and sits in the file-presence table where a reader looks for it.

**Order and shape:**

```
step 1  PLAYBOOK:4789   `| Project docs | Root | CLAUDE.md, README.md | Living, never delete |`
        ->              `| Project docs | Root | CLAUDE.md (+ optional README — see
                           "File presence", ADR-38 A5) | Living; README deprecated
                           from baseline 2026-05-23 |`
        Condensation, not deletion: the row keeps its category, its location and its
        lifecycle claim, and gains the pointer that makes the claim true. ADR-49/65
        (info-preserving condensation) is the licence — nothing recorded is lost, the
        false half is replaced by a pointer to where the fact lives.

step 2  PLAYBOOK:1259   `- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK,
                           ESSENTIALS, ENVIRONMENT.`
        ->              drop the leading `README, `, append
                           ` (README where a repo carries one — see "File presence")`.
        Same ADR-49/65 basis; the enumeration then matches CLAUDE.md:68, which is the
        nearer canonical statement for this repo.

step 3  PLAYBOOK:1072   leave the row, add the marker the sibling CHANGELOG row already
        (marker only)   carries: append to the Status/Scope cell
                           ` — deprecated from baseline 2026-05-23 (ADR-38 A5)`.
        NOT a merge: the row is legitimate universal doctrine for external-audience
        repos. It needs the marker its neighbour has, nothing more.
```

**Order matters:** step 3 last. Steps 1–2 remove the two false assertions; step 3 then marks the one true-but-unqualified row without leaving a window where PLAYBOOK carries neither the assertion nor its correction.

**Cost, itemised:**
- Three lines in one file; net line delta ≈ 0.
- `protocols/PLAYBOOK.md` is **not** in `FRESHNESS_FILES` (`scripts/canonical_docs.py:82` lists VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, `docs/handoffs/README.md`, `protocols/ESSENTIALS.md`) — **no freshness re-stamp is owed.** It *is* in `SECTION_HISTORY_DOCS` and `STRUCTURE_DOCS` (`:86`, `:95`), so `validate_doc_rot` and `validate_doc_structure` run over it: a Section-history entry is the convention for a PLAYBOOK edit, and `_SECTION_HISTORY_MAX_ENTRIES = 12` (`validate_doc_rot.py:126`) caps the block.
- `toc-freshness-playbook` pre-commit gate fires (no heading changes here, so a regen should be a no-op) — `MEASUREMENT-OWED-LOCAL`.
- `protocols/PLAYBOOK.md` carries **no** `reconciled_with:` stamp, so no reconciliation edge advances.
- **ESSENTIALS ↔ PLAYBOOK check (`CLAUDE.md` §5 rule 6):** `protocols/ESSENTIALS.md` contains no root-README statement (`grep -n "README" protocols/ESSENTIALS.md` → one hit, `:67`, `docs/intake/README.md`). Nothing to keep in lockstep. No lockstep template act is owed.
- **Cross-check that this does not collide with an open row:** `[#569]` owns a 19-finding PLAYBOOK census whose two HIGHs are H14 (`/override` at `:2770`) and H13 (an 11-site HANDOFF_PROCESS v5 cluster). `[#569]` is **CLOSED 2026-08-26** by ruling W, and its closure note records that *"the 19-finding PLAYBOOK census … NOT discharged by this closure … no open row owns them."* Under ADR-111 the three sites here are **CANDIDATE**, and the honest read is that they belong in the same successor row as the un-owned census rather than as a fourth PLAYBOOK row. Route: CANDIDATE → intake (ADR-98) → ratification. I do not birth a row.

### Merge M2 — the ADR-114 locator drift (D-4): record, do not repair

**No merge is available.** ADR-114 is immutable. The correct discharge is a `protocols/STANDING_RULINGS.md` entry under the existing **Z-C1** heading (`:3218`), which already reserves this exact territory:

> **Z-C1 · README / VISION merge** (operator theme 3, the *"README zamiast VISION"* class). Measurement first: **count and classify the consumers** of each file across the fleet before any ruling. Note the adjacent live object rather than re-deciding it: **ADR-114 is PARKED** on whether a root `README.md` may be recreated … a merge ruling that ignored ADR-114 would decide the parked question by side effect.

**This census IS the measurement Z-C1 demands** — for the hub. The recorded correction should carry: (a) `parity-surfaces.yaml:133-139` → `:140-150`; (b) `ARCHITECTURE.md:366` does not exist as described, and no *"do not recreate"* echo survives in `ARCHITECTURE.md` at all (`:478` states the deletion only) — so ADR-114's decommission item (b) is **already discharged by attrition** and a future ratification must not go looking for it; (c) the measurement drift `1,956/678 → 2,024/703`, `104/114 → 107/117`, `69 → 72 PROBES`.
**Cost:** one STANDING_RULINGS entry. `protocols/STANDING_RULINGS.md` is not freshness-gated. **Zero** ADR edits, and it decides nothing ADR-114 parked.

### Merge M3 — D-5/D-6 (`docs/research/`, `docs/tech-radar/`): no merge, record the class

Twenty references across two vanished genre folders, **every citing file immutable or append-only**. There is nothing to merge and nothing to repair. What is worth recording — once, in the same Z-C1 entry as M2 — is the class: *a `path:line` citation into a deleted genre folder is unrepairable by construction and is the price the corpus already pays for immutability.* `docs/archive/README.md` gained an `exempt-permanent` retention class for the mirror-image problem (`STANDING_RULINGS.md:2950-2978`, whose *"How to review" step 5* is exactly *"resolve a file's citers"*), so the machinery for recording this already exists.
**Cost:** shares M2's entry. Zero file edits.

### Explicitly NOT proposed

```
docs/audits/README.md      gate: audit-index-freshness + .gitattributes merge=ours
docs/intake/README.md      gate: intake-index-freshness + gen_intake_tree lossless round-trip
                                 + sha256 manifest + deploy carrier hash-match
docs/handoffs/README.md    gate: canonical_freshness (FRESHNESS_FILES) + seed_runbook fleet
                                 seeding + reconciled_with: handoff-process@6.3.0
docs/decisions/README.md   gate: validate_adr_status + check_adr_status_grammar
                                 + doc-code-edge.yaml declared edge
protocols/README.md        gate: reconciled_with: handoff-process@6.3.0
tasks/README.md            the source-of-truth runbook for a generated BACKLOG.md
templates/handoff/*.tmpl   retained live per ADR-83 (.claude/commands/handoff.md:196)
VISION.md                  any edit costs a full end-to-end re-read + stamp bump
                           (check #10) and touches the ×9 parity surface
```

### The one thing I found and am NOT proposing to fix

`ARCHITECTURE.md` cites `VISION.md` zero times and `VISION.md:184-192` does not cite `ARCHITECTURE.md` (§A.3). Adding either pointer is one line. I am not proposing it, for two stated reasons: editing `VISION.md` triggers the §6 freshness obligation for a cosmetic gain, and — more to the point — **"the two canonical docs should point at each other" is the first step of an argument that ends in a single front-door document.** That argument is ADR-114's, it is parked, and it is the operator's. Recorded here as an observation so a later reader has the measurement without my having spent the decision.

---

## 8. Self-audit — applied, and one finding against myself

**The brief's stated failure mode: "If your proposal's net effect is 'create one document that explains the repo', you have proposed the root README by another name — say so and withdraw it."**

I ran the test. The proposal's net effect is: three corrected lines inside `protocols/PLAYBOOK.md`, plus one `STANDING_RULINGS.md` entry recording two locator drifts and a measurement. **Zero files created. Zero files deleted. Zero root-level documents touched. `VISION.md` untouched.** M1 makes the root-README prohibition *more* consistent by removing the corpus's only positive authority to create one. The test passes.

**But it nearly did not, and the near-miss is worth recording.** The natural shape of a "README/VISION consumer census" proposal is: *eight genre READMEs plus VISION plus ARCHITECTURE plus CLAUDE all describe parts of this repo; collapse the navigation into one front door.* I drafted that mentally and it is exactly the withdrawal case — a "unified navigation index at repo root" **is** the root README under a different filename, and it would have decided ADR-114 by side effect while claiming to respect it. **Withdrawn before it was written.** §7's "Explicitly NOT proposed" block and the §7-final paragraph are the residue of that withdrawal, kept visible rather than deleted.

**The brief's second failure mode: "if you found zero DANGLING references to a file that has been deleted for three months, you did not search hard enough."** Seven DANGLING items found (§5), three of them in `protocols/PLAYBOOK.md` — the universal file, not a dusty corner — and one of them (D-4) inside ADR-114 itself, the very document the brief told me to read for the constraint. The first pass, a plain `grep README`, returned 3,857 hits and would have produced either a fake crisis or a shrug; the path-token resolution pass in §B.1 is what turned mentions into a resolvable verdict. Had I stopped at the grep I would have reported the count and missed all seven.

**A third failure I checked for and did not find:** I looked for DANGLING references among the eight living genre READMEs and found none — all eight resolve. Reporting "zero" there is a real result, not a shortfall, because §5 shows the search that would have found them did find seven elsewhere.

**One methodological limit I am stating rather than leaving to be discovered.** My token-resolution pass tests paths **relative to the repo root**. It therefore correctly resolves `docs/audits/README.md` and correctly flags `docs/research/README.md`, but it reports bare relative fragments (`00_README.md`, `README.md.tmpl`, `handoffs/README.md`, `v5/README.md.tmpl`) as ABSENT when they in fact resolve relative to their own context. I classified those by reading each citing site rather than trusting the resolver; the 84-token table in §B.1 marks them `resolves in ctx`. **The resolver is a finding-generator, not a verdict.**

---

## 9. `MEASUREMENT-OWED-LOCAL`

Every claim below needs a gate, a hook, `scripts/audit.py` or the pytest suite. None is estimated and none is asserted.

```
MEASUREMENT-OWED-LOCAL  Whether `audit.py health` is green at fcc9485 (uv 0.8.17 vs pinned
                        ==0.11.19; `uv run --locked` cannot start).
MEASUREMENT-OWED-LOCAL  Whether check #10 (canonical_freshness) currently passes for VISION.md
                        at last_reviewed 2026-08-23 vs its last edit date.
MEASUREMENT-OWED-LOCAL  Whether `toc-freshness-playbook` regenerates to a no-op after M1's three
                        line edits (no heading changes are made, but the gate is the authority).
MEASUREMENT-OWED-LOCAL  Whether validate_doc_rot's Section-history count for PLAYBOOK.md sits
                        below _SECTION_HISTORY_MAX_ENTRIES = 12 with M1's entry added.
MEASUREMENT-OWED-LOCAL  Whether check_handoff_bundle_structure currently reports zero violations
                        over the 20 stamped v4 bundles (D-7's frozen governed set).
MEASUREMENT-OWED-LOCAL  Whether check_reconciled_versions is green for the five documents
                        declaring reconciled_with: handoff-process@6.3.0.
MEASUREMENT-OWED-LOCAL  Whether tests/test_canonical_docs.py's soft-import fallback assertions
                        pass (the two deploy-carried files' literal VISION.md lists).
MEASUREMENT-OWED-LOCAL  fleet_parity status for the canonical-doc-vision surface across the
                        nine ADR-104 members (needs the per-repo state.yaml seeds, absent here).
```

---

## 10. Reproduce everything above

```bash
git rev-parse HEAD                                     # fcc9485567f81814d24b84fe2db5ceff23b743ee

# baseline occurrence counts
grep -rn "VISION\.md" --binary-files=without-match . --exclude-dir=.git | wc -l    # 2024
grep -rl "VISION\.md" --binary-files=without-match . --exclude-dir=.git | wc -l    #  703
grep -rn "README"     --binary-files=without-match . --exclude-dir=.git | wc -l    # 3857
grep -rl "README"     --binary-files=without-match . --exclude-dir=.git | wc -l    #  956

# THE structural fact: no markdown links to either, anywhere
grep -rnE "\]\([^)]*README[^)]*\)"    --binary-files=without-match . --exclude-dir=.git | wc -l  # 0
grep -rnE "\]\([^)]*VISION\.md[^)]*\)" --binary-files=without-match . --exclude-dir=.git | wc -l # 0

# handoff strata (ADR-114 drift check)
ls -d docs/handoffs/*/ | wc -l                                          # 117 (was 114)
grep -rl "VISION\.md" docs/handoffs/ | cut -d/ -f3 | sort -u | wc -l    # 107 (was 104)
grep -rl "VISION\.md" docs/handoffs/ | grep -i probes | wc -l           #  72 (was  69)
ls docs/handoffs/*/README.md docs/handoffs/*/00_README.md | wc -l       #  35 of 117

# the DANGLING sites
sed -n '1072p;1097p;1259p;4789p' protocols/PLAYBOOK.md
sed -n '133,139p' ecosystem/parity-surfaces.yaml     # NOT canonical-doc-vision; that is :140-150
grep -n "recreate" ARCHITECTURE.md                   # no match -> ADR-114's :366 echo is gone
grep -rn "docs/research/README\.md\|docs/tech-radar/README\.md" --exclude-dir=.git . | wc -l  # 20

# the gate coupling
grep -rln "canonical_docs" scripts/ .claude/ deploy/ tests/
sed -n '41,120p' scripts/canonical_docs.py
head -4 VISION.md                                    # last_reviewed: 2026-08-23
head -4 docs/handoffs/README.md                      # last_reviewed: 2026-08-28
```