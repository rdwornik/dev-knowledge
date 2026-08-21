# ARTIFACT — CLOUD-R2 · universalization readiness (provider-agnostic repo)

- **Slug:** `cloud-r2-universalization` · **Lane:** READ-ONLY review · **Effort:** high
- **Bound at:** `78267fdbd12d80d1a491845fa64b006f1b00a97b` (detached from `refs/heads/main`), working tree clean at entry
- **Environment:** Anthropic cloud session, **shallow clone** (`.git/shallow` present, 314 commits reachable)
- **Mutation footprint:** this file only. Nothing else read-modified, moved, or deleted.
- **Consumer:** the future MUTATION lane **CLOUD-4**, which is cut from this artifact.

Findings are **EVIDENCE + RECOMMENDATION**. The architect rules; this lane changed nothing.

---

## 0. Guards fired, conflicts found — read before anything else

### 0.1 Shallow-clone guard: HONOURED

`.git/shallow` is present. Per the binding rules, **no spine-walking instrument was run** —
`validate_git_backlog`, `validate_no_ff`/`block_ff_push` range scans, `journal_spine_anchor`,
`check_fleet_audit_replication` and kin were all skipped. Every count in this artifact is derived
from the **working tree at the bound revision**, never from history walks. Where a claim would
have needed history (e.g. "newest bundle by git add-date", `audit.py::_select_active_bundle`), it is
marked as unverified rather than guessed.

### 0.2 CONFLICT-1 — the brief's own deliverable path collides with ADR-101's tree seal

The brief instructs: *"Commit `ARTIFACT-cloud-r2-universalization.md`"* — a **new top-level file at
the repo root**. `scripts/validate_hermetization.py` Rule A (`rule_a_violation`, line 213–219)
blocks any *added* top-level path whose first component is not in `SANCTIONED_TIER1_FILES`
(lines 82–99). `ARTIFACT-*.md` is not a member of that frozenset, and there is **no `ARTIFACT-`
precedent anywhere in the tree** (`grep -rn "ARTIFACT-"` over `*.md`/`*.yaml`/`*.py` excluding
`JOURNAL.md`/`LESSONS.md` → 0 hits; `.gitignore` has no `ARTIFACT` entry).

So on a properly-armed checkout the `validate-hermetization` pre-commit gate would **REFUSE this
commit** with *"new path outside allowlisted homes — operator approval required"*.

**What I did, and why it is not improvisation:** this container has **no armed hooks**
(`.git/hooks/` holds only `.sample` files; the `pre-commit` binary is absent), so the commit
succeeds physically **without any bypass flag** — I did not use `--no-verify` and did not edit
`.pre-commit-config.yaml`, `.gitignore`, or the allowlist. The file lands on the session branch
`docs/cloud-r2-universalization`, which is **never merged**. The repo invariant is therefore
reported, not overridden.

**Owed to the architect:** before CLOUD-4 (or any lane) lands an `ARTIFACT-*.md` at the root on a
real checkout, either (a) rule the artifact into `SANCTIONED_TIER1_FILES` / a sanctioned home, or
(b) re-home review artifacts under an already-sanctioned genre (`docs/audits/` fits the ADR-101 R3
class enum — `verification` or `technical` — and would additionally pick up `audit-index-freshness`
indexing for free). **(b) is the cheaper and more conformant answer**, and it is the architect's
call, not this lane's.

### 0.3 CONFLICT-2 — "VISION→README rename" collides with two standing prohibitions

The brief's Section 1 frames the work as a **VISION.md → README.md rename**. Two live repo rules
say the destination filename is forbidden:

1. **`CLAUDE.md` §5 rule 5** (line 90): *"Root `README.md` deleted 2026-05-23 (deprecated per
   ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only
   repo) — **do not recreate it**."* Echoed at `ARCHITECTURE.md:366`.
2. **`scripts/validate_hermetization.py` Rule A** again: `README.md` is **absent** from
   `SANCTIONED_TIER1_FILES` (lines 82–99). Adding a root `README.md` is a Rule-A BLOCK on the
   same gate as CONFLICT-1.

Two further machine surfaces would have to move in the same commit or the rename reds them:

- `scripts/audit_checks/check_canonical_md_visibility.py:19–26` — `README.md` currently sits in
  `_CANONICAL_ALL` (the *casing-checked-if-present* list) but **not** in `_CANONICAL_MANDATORY`.
  `VISION.md` sits in `_CANONICAL_MANDATORY`. A rename inverts both memberships.
- `scripts/audit_checks/check_adr38_baseline.py:21,29` — the docstring states *"README.md is
  optional (deprecated from the baseline)"* while `required_files` demands `VISION.md`. Same
  inversion.
- `scripts/audit_checks/check_dot_prefix_discipline.py:33` — `"README.md",  # deprecated from
  baseline; if present, no dot`.

**Recommendation:** the rename is a **doctrine change first** (an ADR that supersedes ADR-38 A5's
README deprecation and amends ADR-101 §1's file enum), and a reference migration second. A
mutation lane that starts with the `git mv` has already lost. Stated plainly: **this is not a
rename, it is the reversal of a 2026-05-23 deletion decision plus a fleet-wide canonical-file
substitution.**

### 0.4 CONFLICT-3 — ADR-53 forbids the file Section 2 asks me to propose

`CLAUDE.md` §10 (line 203) names *"Narrating or managing AGENTS.md"* an anti-pattern and states
*"AGENTS.md is retired (ADR-53)"*. ADR-53 Decision 2 is explicit: *"`AGENTS.md` as a separate
per-repo file is retired."*

The brief asks for a proposed **universal AGENT.md / provider-specific split**. That proposal is
therefore *authored*, but it is **blocked pending a ruling** — and the repo already knows this:
`docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md:70–74` carries
**PROPOSED ROW R1** whose whole content is *"Rule on AGENTS.md: two memos vs ADR-53's
single-instruction-file rule"*, with the hard gate at line 107: **"Must: rule on R1 before any
AGENTS.md file is created."** Section 2 below is written as *input to R1*, not as an instruction
to build.

### 0.5 What this lane did not touch

`tasks/`, `BACKLOG.md`, `protocols/` (read only), `STANDING_RULINGS.md` §Q, `.pre-commit-config.yaml`,
`.gitignore`, `docs/intake/` (read only). No file moved. No merge, no push to `main`.

---

## 1. VISION → README reference census

**Instrument:** `grep -rn "VISION\.md" --binary-files=without-match . --exclude-dir=.git`, run at
the bound revision over the **entire tree** — workflows, scripts, tests, protocols, ADRs, handoff
templates, generated indexes, config and lockfiles all included, nothing excluded but `.git/`.

### 1.1 The headline count

```
total occurrences ............ 1,924
total files .................. 672
```

Partitioned by **whether a mutation lane is permitted to edit the file at all** (the partition that
matters, because `CLAUDE.md` §5 rules 1–3 make most of the corpus unwritable):

```
class            files    refs   editable?
--------------   -----   -----   ---------------------------------------------
EXECUTABLE          23     108   yes  - scripts/, tests/, .claude/workflows/
CONFIG               9      31   yes  - ecosystem/*.yaml, deploy/manifest-*, workspace
LIVING-DOC          23      36   mostly - doctrine + generated + derived (see 1.3)
--------------   -----   -----
LIVE SUBTOTAL       55     175
APPEND-ONLY          2      56   NO   - JOURNAL.md, LESSONS.md (rule 1 + 2)
IMMUTABLE          615   1,693   NO   - ADRs, audits, handoffs, archives, history (rule 3)
--------------   -----   -----
FROZEN SUBTOTAL    617   1,749
```

**The migration input is 55 files / 175 references — 9.1% of the occurrences.** The other 90.9% are
in files the repo forbids editing. That is the single most important number in this section: a
`sed -i` over the tree is not merely risky, it is a **core-invariant violation on 617 files**.

**Zero of the 1,924 references are markdown links.** `grep -cE "\]\(\.?/?VISION\.md"` → **0**. Every
reference is bare text, backticked prose, a Python string literal, or a YAML value. **No link
checker, no CI, and no existing gate would notice a broken reference after the rename** — which is
precisely what makes the census necessary rather than nice-to-have.

### 1.2 The 32 live machine references (EXECUTABLE + CONFIG) — the complete list

```
file                                                refs   what breaks
------------------------------------------------   ----   ------------------------------
scripts/audit_checks/check_vision_md.py               9    the whole check (ADR-33 gate)
scripts/gen_handoff.py                                5    boot-bundle vision extract
scripts/session_end_backpressure.py:127               1    _CANON tuple (Stop hook)
scripts/validate_hermetization.py:84                  1    SANCTIONED_TIER1_FILES
scripts/validate_doc_rot.py:117                       1    _SECTION_HISTORY_DOCS
scripts/validate_doc_structure.py:72                  1    _STRUCTURE_DOCS
scripts/canonical_freshness_gate.py:32                1    DEFAULT_FRESHNESS_FILES
scripts/audit_checks/check_adr38_baseline.py:29       1    required_files
scripts/audit_checks/check_canonical_md_visibility.py:19  1  _CANONICAL_MANDATORY
scripts/audit_checks/check_canonical_structure.py:24  1    _CANONICAL_SPINE key
scripts/enforcement_coverage.py:558                   1    comment only (stale-note)
scripts/verify_handoff_probes.py:92                   1    comment only (regex doc)
.claude/workflows/conformance-hub.js:133              1    V2 verifier scan list
tests/test_verify_handoff_probes.py                  29    fixtures + assertions
tests/test_audit.py                                  23    fixtures + assertions
tests/test_fleet_parity.py                           16    probe fixtures (path_tracked)
tests/test_enforcement_coverage.py                    3
tests/test_fleet_parity_events.py                     3
tests/test_validate_doc_structure.py                  3
tests/test_gen_handoff.py                             2
tests/fixtures/README.md                              2
tests/test_release_lint.py                            1
tests/test_v6_frozen_contract.py                      1
ecosystem/index.yaml                                 17    recorded audit evidence strings
ecosystem/disposition-register.yaml                   5    2 disposition ids + prose
ecosystem/parity-surfaces.yaml                        3    canonical-doc-vision probe
deploy/manifest-v1.{1,2,3,3.1,4}.0.yaml               5    doc_shapes key x5
.dev-knowledge.code-workspace:162                     1    editor task arg
------------------------------------------------   ----
                                                    139   (108 EXECUTABLE + 31 CONFIG)
```

### 1.3 The 23 LIVING-DOC files, split by who owns them

- **Hub doctrine, hand-edited (8 files / 16 refs):** `protocols/PLAYBOOK.md` ×6, `CLAUDE.md` ×3
  (lines 40, 57, 65, 66, 90 — note §4 also carries the composite token
  `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS`), `protocols/HANDOFF_PROCESS.md` ×2,
  `protocols/{ESSENTIALS,HANDOFF_BOOT,DEFINITION_OF_DONE,ENVIRONMENT}.md` ×1 each, `VISION.md`
  itself ×1 (line 126, the child-repo instruction).
- **Carriers — edit these and the change propagates to consumers (4 files / 4 refs):**
  `templates/handoff/v5/PROBES.md.tmpl:81`, `templates/handoff/03_PROJECT.md.tmpl`,
  `templates/handoff/README.md.tmpl`, `templates/child-methodology-floor.md.tmpl`.
- **Command specs (2 files / 2 refs):** `.claude/commands/handoff.md:111`,
  `.claude/commands/handoff-verify.md:99`.
- **Generated / derived — do NOT hand-edit, regenerate (6 files / 9 refs):**
  `ecosystem/{conformance.md,conformance.html,registry.md}`, `tasks/558-*`, `tasks/453-*`,
  `tasks/462-*` (all three derived from `BACKLOG.md` by `scripts/gen_task_tree.py`).
- **Off-limits to this lane and to any lane without a filing decision (3 files / 5 refs):**
  `BACKLOG.md:1`, `docs/intake/2026-07-08-func-new-project-bootstrap.md` ×2,
  `docs/intake/2026-08-05-func-simplification-distribution-wave.md` ×1.

### 1.4 The riskiest references — what a bare rename silently breaks

Ranked by *silence*: how far the failure travels before anything says so.

**R1 — `ecosystem/parity-surfaces.yaml:133–139` — the rename is a FLEET migration, not a hub one.**

```yaml
- id: canonical-doc-vision
  kind: path
  tier: {hub: MUST, consumer: MUST}
  probe: {type: path_tracked, path: VISION.md}
```

`tier: {hub: MUST, consumer: MUST}` means **every consumer repo must carry `VISION.md`**.
`ADR-104`'s `adr104-fleet-members` declaration (`docs/decisions/ADR-104-fleet-repository-shape.md:149–161`)
enumerates **nine** members: `.dev-knowledge`, `ai-council`, `corp-monorepo`, `corp-ops`,
`corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`.
Renaming in the hub alone turns `fleet_parity` RED for **every onboarded consumer simultaneously**,
and the hub cannot fix them (§5 rule 4: Layer 2 never drives a child repo's state). **This is the
single hardest constraint on CLOUD-4 and it is not visible from the hub's own tree.**

**R2 — `scripts/gen_handoff.py:507–520` — a CONTENT dependency, not a path dependency.**
`_vision_extract()` opens `repo_root / "VISION.md"` and regex-matches `^## Vision\s*\n(.*?)(?=^## |\Z)`.
Its degrade contract returns the literal string
`"(VISION.md `## Vision` section not found — fix VISION.md before using this boot)"`. After a bare
rename the generator **does not crash** — it emits that placeholder into every new handoff boot
bundle, and the bundle is an **immutable artifact** the moment it is committed. Failure mode:
silent, permanent, and stamped into the record.

**R3 — the `## Vision` heading spine, replicated across five deploy manifests.**
`deploy/manifest-v{1.1.0,1.2.0,1.3.0,1.3.1,1.4.0}.yaml` each carry
`VISION.md: spine: ["## Vision","## Scope","## Values","## Lifecycle","## References"]`, mirrored by
`scripts/audit_checks/check_canonical_structure.py:24`. The *filename* and the *H2 spine* are two
separate migration surfaces. A rename that keeps `# VISION — .dev-knowledge` (`VISION.md:8`) as the
H1 inside a file called `README.md` is internally incoherent; a rename that changes the H1 without
the spine reds `check_canonical_structure` on all five manifest versions.

**R4 — handoff PROBES rows are baked into 104 immutable bundles.**
`templates/handoff/v5/PROBES.md.tmpl:81` defines probe **P1a** with the literal verification command
`grep -A4 '^## Vision' VISION.md`. 104 of the 114 committed `docs/handoffs/*/` bundles reference
`VISION.md`; **69 distinct `PROBES`-named files** carry such a row. These are immutable (§5 rule 3),
so they can never be corrected. The mitigating fact, verified in code: `check_handoff_probes`
validates **only the active bundle** (`scripts/audit.py:1450`; the scoping is stated at
`scripts/audit_checks/check_residual_completeness.py:38`). So the blast radius is *the active bundle
at rename time plus every bundle generated afterwards* — bounded, but it means **the rename commit
must also re-cut or retire the active bundle's probe**, and the template must move in the same
commit or the very next handoff bakes a dead command into a new immutable artifact.

**R5 — `scripts/session_end_backpressure.py:127`, a Stop hook.** `_CANON = ("VISION.md", ...)`.
Per the ADR-85 amendment 2026-08-03 §A5 this hook is **advisory in full** and cannot block a turn —
so a stale entry here produces *no error at all*, just a silently-narrowed advisory. Lowest severity,
highest silence.

**R6 — `scripts/enforcement_coverage.py:558` is already a documented stale claim.** The comment reads
*"(ai-council's VISION.md uses the quoted form). The deployed gate parses both (yaml); this stale…"*.
A rename that only rewrites the token leaves a comment describing a *cross-repo* file. Cosmetic, but
it is evidence the corpus already carries cross-repo `VISION.md` assumptions in prose.

**R7 — `ecosystem/index.yaml` (17 refs) and `ecosystem/disposition-register.yaml` (5 refs) are
RECORDED EVIDENCE, not configuration.** `index.yaml` lines quote past audit findings verbatim
(*"VISION.md present; frontmatter keys: […]"*); `disposition-register.yaml:113,255` carry the
disposition **match keys** `"VISION.md -> handoff-process"` and `"VISION.md -> prompt-template"`.
Rewriting `index.yaml` would **falsify history**; leaving `disposition-register.yaml` alone would
**orphan two live dispositions** so their WARNs resurface undispositioned. These two files need
*opposite* treatment, and a mechanical sweep gets at least one of them wrong.

### 1.5 GO / NO-GO for CLOUD-4 — Section 1

**NO-GO as scoped.** Do not cut a mutation lane for "rename VISION.md to README.md".

Three blockers, each independently sufficient:

1. **The destination filename is prohibited** by `CLAUDE.md` §5 rule 5 + `ARCHITECTURE.md:366`, and
   gate-blocked by `validate_hermetization` Rule A (CONFLICT-2). This needs an **ADR** that
   supersedes ADR-38 amendment A5 and amends ADR-101 §1 — not a lane.
2. **The rename is fleet-scoped, and the hub may not execute it.**
   `parity-surfaces.yaml` `canonical-doc-vision` is `{hub: MUST, consumer: MUST}` across
   ADR-104's nine members; §5 rule 4 forbids the hub driving a child's state. Sequencing across
   nine repos is a program, not a commit.
3. **90.9% of references are unwritable** (617 immutable/append-only files, 1,749 refs). Any lane
   that reaches for a tree-wide substitution violates rules 1–3 on contact.

**GO on a narrower, genuinely useful cut** — recommend CLOUD-4 be re-scoped to **produce the
migration mechanism, not the migration**:

- **(a)** Author the ADR (destination-name legality + fleet sequencing + the immutable-locator
  cost, which §1.4 R4/R7 has now priced).
- **(b)** Land **one** table: a canonical-doc-name registry that the ten machine constants in §1.2
  read from instead of each hardcoding `"VISION.md"` — `check_vision_md`, `check_adr38_baseline`,
  `check_canonical_md_visibility`, `check_canonical_structure`, `canonical_freshness_gate`,
  `validate_doc_rot`, `validate_doc_structure`, `validate_hermetization`,
  `session_end_backpressure`, `gen_handoff`. That is the **table-not-a-rewrite** shape the whole
  CLOUD-R2 brief is aiming at, and it is worth landing **whether or not the rename ever happens**.
- **(c)** Add the missing detector: since **0 references are links**, nothing today can tell you a
  canonical-doc reference has gone stale. A `doc_claims`-family check that asserts every
  `<CANONICAL>.md` token in the *live* corpus resolves to a tracked path would have made this
  census a command instead of an artifact.

---

## 2. AGENT.md / agents.md — the published standard vs what CLAUDE.md carries

### 2.1 Library-first: the standard is already in the repo, and it was researched here

`agents.md` is **egress-blocked** from this container (`WebFetch https://agents.md` →
`EGRESS_BLOCKED`), so the primary source is unreachable from this lane. That turns out not to
matter, because **the repo already holds a verified account of the standard** — and the brief's
"library-first, do not invent a format" instruction points straight at it:

**`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`** — 187 lines,
explicitly source-graded (`VERIFIED` / `REPORTED` per claim). The normative facts, quoted:

- **Governance (line 21):** *"AGENTS.md was formalized as an open spec in **August 2025**, led by
  OpenAI with participation from Google, Cursor, Factory, Sourcegraph and Amp. On **December 9,
  2025** […] it was contributed to the **Linux Foundation's Agentic AI Foundation (AAIF)**"* —
  alongside Anthropic's MCP and Block's Goose.
- **What the spec mandates (line 23):** *"Almost nothing. Per agents.md: 'AGENTS.md is just standard
  Markdown. Use any headings you like; the agent simply parses the text you provide.' No required
  fields, no YAML, no schema."*
- **Precedence (line 23):** *"The closest AGENTS.md to the edited file wins; explicit user chat
  prompts override everything."* Monorepos nest files.
- **Claude Code is the exception (lines 11, 35):** *"Claude Code reads `CLAUDE.md`, not
  `AGENTS.md`."* The idiomatic bridge is a one-line `@AGENTS.md` import, *"imports resolve up to 4
  hops deep."*
- **Adoption (line 25):** *"more than 60,000 open source projects and agent frameworks including
  Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code."*
- **Codex precedence chain (line 31):** `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md`
  (global) → repo-root → intermediate dirs → cwd; concatenated, later wins; **32 KiB cap**
  (`project_doc_max_bytes`); `project_doc_fallback_filenames` for alternates.
- **The honest counter-evidence (line 120):** ETH Zurich, **arXiv:2602.11988** (Feb 2026), 138
  tasks / 12 repos — *"providing context files does not generally improve task success rates, while
  increasing inference cost by over 20% on average."* LLM-generated files made it **worse**
  (−0.5% to −2%). **Implication as the memo itself draws it:** *"keep AGENTS.md short and
  high-signal (a ~150-line threshold is widely cited), and do NOT rely on it to carry enforcement."*
- **Reject symlinks (line 48):** on Windows without `core.symlinks=true` + Developer Mode, *"git
  silently checks out a plain text file containing the link target string"* — a broken stub. The
  fleet is Windows + git-bash. **Symlink is off the table by evidence, not preference.**

A **second independent memo reached the same recommendation**
(`docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md:24–33`), which is why
that intake's **R1** exists (§0.4). Its Q1 shape (line 54): *"one **AGENTS.md** (≤30 lines) + a
one-line **`CLAUDE.md` = `@AGENTS.md`** + a **`.gemini/settings.json`** with
`context.fileName: ["AGENTS.md"]`."*

**Note the spelling.** The standard's filename is **`AGENTS.md`** (plural). The brief says
`AGENT.md` (singular). Singular is not the standard and **no tool reads it** — a repo that ships
`AGENT.md` gets the portability of neither convention. Treated throughout as `AGENTS.md`.

### 2.2 What CLAUDE.md carries today — the real structural fact

`CLAUDE.md` is **200 lines, hard-budgeted** (ADR-53; enforced by `validate_doc_rot`'s
`_FILE_SIZE_BUDGETS = {"CLAUDE.md": 200}` at `scripts/validate_doc_rot.py:112`). It carries twelve
sections, and — critically — **it is already region-split with byte-coupled carriers**:

```
region                          axis   carrier in templates/claude-regions/
-----------------------------   ----   ------------------------------------
first-read                      HUB    first-read.md
conventions-commit-branch       HUB    conventions-commit-branch.md
conventions-output-formatting   HUB    conventions-output-formatting.md
critical-rules-records          HUB    critical-rules-records.md
critical-rules-consistency      HUB    critical-rules-consistency.md
critical-rules-no-leftovers     HUB    critical-rules-no-leftovers.md
session-start-protocol          HUB    session-start-protocol.md
antipatterns-universal          HUB    antipatterns-universal.md
repo-identity                   REPO   -
repo-architecture               REPO   -
commands-repo-roster            REPO   - (generated: .claude/generated/commands-repo.md)
skills-repo-roster              REPO   -
hooks-repo-roster               REPO   -
recent-adrs-roster              REPO   - (generated: .claude/generated/recent-adrs.md)
section-history                 REPO   -
```

8 HUB regions (byte-coupled to carriers; asserted by
`test_hub_region_bodies_still_byte_match_the_templates`) + 7 REPO regions.

**This is the single most important finding in Section 2, and it cuts against the naive split.**
The repo *already has* a carrier mechanism for splitting `CLAUDE.md` — but its axis is
**hub-vs-repo** (who owns the words), **not universal-vs-provider** (which tool reads the words).
An `AGENTS.md` split needs the second axis. The two are **orthogonal**, and they cross-cut: the
`hooks-repo-roster` region is REPO-owned *and* deeply Claude-specific; `conventions-commit-branch`
is HUB-owned *and* almost entirely provider-agnostic — except that its enum contains
`claude/<slug>` and `claude --worktree` (see §3, seam S1).

### 2.3 The proposed split — exactly what moves where

Judged per region against one test: **would a Codex/Cursor/Gemini session need this to work
correctly in this repo?**

**→ `AGENTS.md` (universal, target ≤150 lines per the ETH-Zurich-informed bar; the intake's Q1
says ≤30 for always-on — recommend ≤120 as the reconciliation):**

| From | What moves | Why universal |
|---|---|---|
| §2 `repo-identity` | name, purpose, owner, critical paths, related locations | any agent needs to know what repo it is in |
| §3 `repo-architecture` | the pointer to `ARCHITECTURE.md` + "NOT a code project" | orientation, tool-neutral |
| §4 `conventions-commit-branch` | Conventional Commits, `--no-ff`, never commit to `main` | **minus** the `claude/`+`worktree-` enum members (see below) |
| §4 (rest) | naming, testing (`pytest -x --tb=short`), linting (`ruff check --fix`), file-lifecycle, freshness cadence | build/test/lint commands are the standard's own core use case |
| §5 rules 1–5, 8, 9 | append-only / immutable / Layer-2 / no-leftovers | these are **repo** invariants; every agent must obey them |
| §6 `session-start-protocol` | `git status`, `git log -5`, read active bundle, check BACKLOG, `pytest --collect-only` | tool-neutral procedure |
| §10 (partial) | "editing old LESSONS entries", "adding orchestration scripts", "duplicating content", "running validators with no args" | provider-neutral anti-patterns |

**→ `CLAUDE.md` (thin: `@AGENTS.md` + Claude-only deltas):**

| Stays | Why Claude-specific |
|---|---|
| §1 first-read order | describes Claude Code's auto-read-on-session-start behaviour |
| §5 rule 7 | *"No executable rules in this repo — those go in `~/.claude/` with `verify:` lines"* — names a Claude path |
| §7 commands roster | `.claude/commands/*.md` is a Claude-Code-only format (8 files) |
| §8 skills roster | `.claude/skills/` + the `tier1-lifecycle` plugin (Claude marketplace format) |
| §9 **session** hooks | `.claude/settings.json` Stop / PreToolUse / SessionStart — **no cross-tool standard** |
| §10 first bullet | *"Narrating or managing AGENTS.md"* — **this bullet is the thing R1 must rule on and would be deleted or inverted** |
| §11 recent-ADRs roster | `@`-import syntax is Claude-specific |
| §12 section history | file-local bookkeeping |

**→ `codex/AGENTS.md` — already exists, and must NOT be confused with the new root file.**
`codex/AGENTS.md` (79 lines) is the **global reviewer role config**, canonical source for
`~/.codex/AGENTS.md` (ADR-54; carried by `deploy/carrier_globalconfig.py:53–54`,
`deploy/tool.py:340`). It contains *"Codex is a **read-only code reviewer** across all repos"* plus
the severity checklist. **It is a role definition, not repo doctrine.**

**This is the collision, stated precisely** — and it is exactly what
`docs/intake/2026-08-12-func-repo-self-description-consolidation.md:138–146` calls
*"THE DECISION IS THE `AGENTS.md` COLLISION"*: per the standard's precedence chain (memo line 31),
Codex would read **`~/.codex/AGENTS.md` (the reviewer role) THEN a repo-root `AGENTS.md` (the new
doctrine), concatenated, later wins**. A repo-root `AGENTS.md` carrying repo doctrine therefore
**layers on top of and can silently override the hub-owned reviewer role** that PLAYBOOK:4261 pins
as *"HUB-OWNED (R1 — fleet doctrine) … Consumers never edit it."* And the combined payload runs
against Codex's **32 KiB `project_doc_max_bytes` cap**, which the intake at line 101 already names
as an owed check (*"a check computes the combined size Codex would read"*).

**→ `.gemini/settings.json`, `.github/copilot-instructions.md`:** not proposed. Neither tool is in
the fleet's active toolset (ADR-53: *"The active toolset is Claude Code + Codex only"*), and
`.gemini/` would be a **new top-level dir** → `validate_hermetization` Rule A → needs ADR-101 §1
amendment. Cost with no present consumer.

### 2.4 Mechanism — generation + hash, not symlink, not duplication

The memo's verdict (lines 48–54, 146, 173–174) and this repo's own precedent agree:

- **Reject symlinks** — Windows fleet, silent degradation to text stubs.
- **`@AGENTS.md` import** is Windows-clean, git-clean, Anthropic-documented, and keeps `CLAUDE.md`
  a real file so Claude-only deltas can sit beneath the import.
- **Drift guard = generation + content-hash + version stamp**, enforced by `pre-commit`.

The hub **already runs this exact pattern four times over** and does not need to invent it:

- `.claude/CLAUDE-FLOOR.md` + `.sha256` sidecar + `check_floor_hash.py --require-present` (ADR-78/93)
- `templates/claude-regions/*.md` byte-coupled to `CLAUDE.md`'s HUB regions
- six regen-and-diff gates already in `.pre-commit-config.yaml`: `roster-freshness`,
  `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`,
  `intake-index-freshness`, `codemap-freshness`
- `coherence-nudge` + `reconciled_versions` for spec-version skew

So the `AGENTS.md` → `CLAUDE.md` guard is a **seventh instance of a pattern with six live
precedents** — genuinely library-first inside this repo, not a new organ family.

### 2.5 GO / NO-GO for CLOUD-4 — Section 2

**NO-GO on authoring any `AGENTS.md` file. GO on producing R1's decision packet.**

The blocker is not technical, it is procedural and already filed: the intake's own gate reads
*"**Must:** rule on R1 before any AGENTS.md file is created"*
(`docs/intake/2026-08-17-...-distillation.md:107`), and its acceptance criterion (line 117) is
*"a reader can determine, from a committed artifact, whether AGENTS.md is admitted or refused."*
A mutation lane that writes the file pre-empts the ruling it depends on.

**What CLOUD-4 should deliver instead — the four inputs R1 is missing:**

1. **The precedence collision, priced.** §2.3 establishes that `~/.codex/AGENTS.md` (role) and a
   root `AGENTS.md` (doctrine) **concatenate with later-wins**. Measure the combined byte size
   against the 32 KiB cap (the check the intake already owes at line 101) and state whether the
   role config can survive the layering. **If it cannot, R1 must refuse the root filename and pick
   a `project_doc_fallback_filenames` alternate instead** — Codex already supports that mechanism,
   and ADR-53 records it is already in use for `CLAUDE.md`.
2. **The ADR-53 reading question**, verbatim from the intake (line 187): *"Does ADR-53's 'single
   instruction file' ruling forbid **AGENTS.md specifically**, or forbid **two files that both
   carry content**?"* A one-line `CLAUDE.md = @AGENTS.md` pointer **preserves ADR-53's substance**
   (one substantive file) while inverting its letter. Recommend R1 rule on the *substance* reading
   and supersede ADR-53 Decision 2 explicitly — a silent reinterpretation is exactly the drift
   ADR-53 itself was written to end.
3. **The region-axis reconciliation.** §2.2's finding — the existing carrier split is hub-vs-repo,
   the needed split is universal-vs-provider, and they cross-cut. R1 must say whether
   `templates/claude-regions/` **becomes** the AGENTS.md carrier set (adding a second axis to
   existing files) or whether a **parallel** carrier tree is created. The first is cheaper and
   keeps one byte-coupling test; the second is clearer. **Recommend the first.**
4. **The efficacy caveat, on the record.** arXiv:2602.11988 says context files don't generally
   improve success and cost >20% more tokens. The honest framing for R1: **adopt AGENTS.md for
   portability insurance, not for quality**, and hold it to ≤120 lines. Do not let the adoption
   argument rest on a benefit the cited evidence does not support.

---

## 3. Provider-swap seam inventory

Every hardcoded model / CLI / provider name on the live surface. **Swap cost** is what a *second
provider* would cost at that site:

- **table-edit** — a value in a dict/frontmatter/YAML/constant; add a row, done.
- **code-change** — control flow, argv construction, or a file format only one vendor reads.
- **doctrine-change** — a ruled surface; changing it needs an ADR, a recorded ruling, or an
  operator decision, regardless of how few characters move.

### 3.1 The table

| # | Location | What is hardcoded | Swap cost |
|---|---|---|---|
| S1 | `scripts/validate_branch_naming.py:18,84` · `templates/claude-regions/conventions-commit-branch.md:1` · `CLAUDE.md` §4 | Branch-prefix enum contains `claude/<slug>` ("Anthropic cloud-session lanes") and `worktree-<name>` ("`claude --worktree` / EnterWorktree") | **doctrine-change** — CLAUDE.md §4 states a new prefix "enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface" (cf. B5) |
| S2 | `deploy/lived_sandbox/spawn.py:33–34` | `DEFAULT_MODEL = "sonnet"`, `CLAUDE_BIN = "claude"` | **code-change** |
| S3 | `deploy/lived_sandbox/spawn.py:3,50–67,148–151,181` | `claude -p` headless invocation, `ANTHROPIC_API_KEY` auth, `CLAUDE_CONFIG_DIR` isolation — *the isolation property itself is Claude-specific* | **code-change** |
| S4 | `deploy/lived_sandbox/cli.py:3–5,176,186` | `--haiku` as the model-selector CLI flag | **code-change** (flag name is in the public CLI surface) |
| S5 | `deploy/carrier_plugin.py:193,336,339,369` | `claude plugin list/install/update`, `claude plugin marketplace add` | **code-change** — plugin/marketplace has no cross-tool analogue |
| S6 | `deploy/carrier_globalconfig.py:53–54` · `deploy/tool.py:340` | `DEFAULT_SOURCE_REL = "codex/AGENTS.md"` → `~/.codex/AGENTS.md` | **table-edit** for retarget; **code-change** to carry a *third* provider (module assumes one source→one target) |
| S7 | `scripts/changelog_sentinel.py:32–34` | `_TOOLS = {"claude-code": ["claude","--version"], "codex": ["codex","--version"]}` | **table-edit** |
| S8 | `ecosystem/tool-versions.yaml` | `tools:` keys `claude-code` / `codex` + `source_url` to `anthropics/claude-code` and `openai/codex` | **table-edit** |
| S9 | `.claude/agents/artifact-reader.md:8,30` | `model: claude-sonnet-5` frontmatter; note pins upgrade path to `claude-opus-4-8` | **table-edit** |
| S10 | `.claude/workflows/conformance-hub.js:150–152` | three per-stage `model: 'claude-sonnet-5'` pins | **table-edit** |
| S11 | `.claude/workflows/conformance-hub.js:133` | verifier scan list naming `VISION.md, ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, protocols/ESSENTIALS.md` | **table-edit** (also a §1 census site) |
| S12 | `templates/prompt-template.md:66,77–92` | routing matrix `<opus\|sonnet>`, "`opus` is the `.dev-knowledge` default" | **doctrine-change** — v1.11 amendment 2026-08-07 is operator-ruled on measured evidence |
| S13 | `templates/prompt-template.md:113` | dispatch line `claude --bg --model opus --effort high --permission-mode bypassPermissions "…"` | **code-change** — every batch-lane dispatch is this literal string |
| S14 | `.claude/commands/lane-boot.md:62` | `claude --worktree lane-<letter>-<id>-<slug> --bg "…"` | **code-change** |
| S15 | `protocols/PLAYBOOK.md:2178–2197` | the ruled routing matrix: `opus` / `sonnet` / `haiku` rows + the CONTEXT-LOAD amendment | **doctrine-change** |
| S16 | `protocols/PLAYBOOK.md:2386` · `ARCHITECTURE.md:670–674` | t-shirt pins **S=Haiku · M=Sonnet · L/judgment=Opus**; "unpinned fan-out is a bug"; "inherits the main session model (Opus 4.8)" | **doctrine-change** (ADR-70) |
| S17 | `protocols/PLAYBOOK.md:3135` | *"The Sonnet/M tier is Sonnet 5 (`claude-sonnet-5`)"* — exact model string bound to a tier | **table-edit** inside a **doctrine** paragraph |
| S18 | `protocols/PLAYBOOK.md:4251` | *"Exact model strings only"*: `gpt-5.6-terra` / `-sol` / `-luna`, never bare `gpt-5.6` | **doctrine-change** |
| S19 | `protocols/PLAYBOOK.md:4252–4253` | terra as **doctrinal default review lane**, pinned in `~/.claude/bin/codex-review.ps1`; doc-lane pinned to `gpt-5.6-terra` | **doctrine-change** — *the wrapper is outside this repo* |
| S20 | `protocols/PLAYBOOK.md:4261–4263` | `~/.codex/AGENTS.md` + `~/.codex/config.toml` hub-owned; producer lane charter-only pending `#341` | **doctrine-change** |
| S21 | `protocols/PLAYBOOK.md:4518` (Appendix B) | *"The model-routing table is canonical in `~/.claude/ROUTING.md`"* — **the routing source of truth is not in this repo** | **doctrine-change** + out-of-repo dependency |
| S22 | `protocols/PLAYBOOK.md:4530–4544` | time-shifting schedule + token techniques keyed to Opus/Sonnet/Haiku and `/clear`, `/compact`, `@file:15-80` | **doctrine-change** (Claude-only command syntax) |
| S23 | `docs/decisions/ADR-70-amendment-2026-07-07-*.md` | tier **XL = Claude Fable 5**, browser-architect layer, "fallback is Opus", re-evaluate on pricing | **doctrine-change** — immutable ADR; supersede only |
| S24 | `.claude/settings.json` (whole file) | Stop / PreToolUse / SessionStart×5 hooks, `enabledPlugins`, `autoMode.classifyAllShell`, `permissions.allow:["Workflow"]` | **code-change** — hooks have no cross-tool standard |
| S25 | `.claude/` organ tree | 8 commands · 2 skills · 1 agent · 1 workflow · 1 rules file; plus `plugins/tier1-lifecycle/` (2 commands + `hooks/hooks.json`) + `.claude-plugin/marketplace.json` | **code-change** — re-author per provider |
| S26 | `.claude/settings.json` `extraKnownMarketplaces` | `"path": "C:\\Users\\1028120\\Documents\\Dev\\.dev-knowledge"` | **table-edit** — a *host* seam, not a provider seam; flagged because it is a hardcoded absolute path in committed config |
| S27 | `deploy/floor_conformance.py:99` | *"a live `claude -p` floor-sentinel"* as the auto-load proxy | **code-change** |
| S28 | `.claude/CLAUDE-FLOOR.md` + `.sha256` · `templates/child-methodology-floor.md.tmpl` · `check_floor_hash.py` | the floor is a Claude-Code `@import` artifact under `.claude/` | **doctrine-change** (ADR-78/93) |
| S29 | `ecosystem/satellite-onboarding-rulings.yaml:51` | `proposed_by: census 2026-07-13 (gpt-5.6-sol)` | **table-edit** (provenance only) |
| S30 | `pyproject.toml:36` | `<3 bound: … (grok L5)` — provenance attribution | **table-edit** (cosmetic) |
| S31 | `scripts/*.py` × ~12 files, several hundred comment lines | `terra P1` / `terra HIGH` reviewer attributions (`gpt-5.6-terra`) | **none** — provenance in comments; a swap adds a new attributor, it does not invalidate these |
| S32 | `scripts/setup-fleet-scheduler.ps1:7` | *"Scheduler → `python scripts/fleet_health.py` directly. No `claude -p`"* | **none — already agnostic by design** |
| S33 | `.pre-commit-config.yaml` (19 gate ids) · `.pre-commit-hooks.yaml` (6 exported) · `.github/workflows/report-only-wall.yml` | pre-commit / commit-msg / pre-push / Actions gates | **none — provider-agnostic already** |

### 3.2 The shape of the result

```
doctrine-change ....... 12 sites   (S1, S12, S15, S16, S18, S19, S20, S21, S22, S23, S28, + S17 partial)
code-change ........... 10 sites   (S2, S3, S4, S5, S13, S14, S24, S25, S27, + S6 for a 3rd provider)
table-edit ............  9 sites   (S6 retarget, S7, S8, S9, S10, S11, S17, S26, S29, S30)
already agnostic ......  3 classes (S31, S32, S33)
```

**The load-bearing observation: the enforcement mesh is already provider-agnostic.** Nineteen
pre-commit/commit-msg/pre-push gate ids plus a GitHub-Actions report-only wall run identically no
matter which agent authored the change. The Claude-specific enforcement is **seven session hooks**
(`.claude/settings.json`: 1 Stop, 1 PreToolUse, 5 SessionStart) plus the plugin's Stop hook — and by
the repo's own ADR-85 amendment 2026-08-03 §A5, the **Stop hook is advisory in full** and the teeth
moved to `pre-push` (`block-unanchored-push`, `block-ff-push`) precisely because *"an organ that can
be exhausted cannot carry teeth"* (`CLAUDE.md` §9).

That is the same conclusion the portability memo reaches independently at line 128: *"your
enforcement layer should live in provider-agnostic git hooks + pre-commit + GitHub Actions, NOT in
tool-specific agent hooks."* **The repo already did the expensive part of universalization without
calling it that.**

**Where the swap actually hurts, in order:**

1. **`~/.claude/ROUTING.md` is the canonical routing table and it is outside this repo** (S21).
   PLAYBOOK Appendix B deliberately killed the resident copy (#158 Decision B) to prevent drift.
   Correct for drift; fatal for a table-driven swap, because **the table CLOUD-4 would edit is not a
   file this repo owns**. Same for `~/.claude/bin/codex-review.ps1` (S19) and `~/.codex/config.toml`
   (S20). Three of the highest-leverage seams live at L0.
2. **The `.claude/` organ tree does not port** (S24, S25). 13 organs + a plugin. The memo (line 13)
   is blunt: hooks, slash commands, subagents, skills and permissions *"do NOT port — each tool has
   its own file format, location, event set, and blocking semantics."*
3. **Routing doctrine is ruled, not configured** (S12, S15, S16, S23). The `opus`-default was
   operator-ruled **on measured evidence** — *"a shape-S arc on sonnet ran ~3h against this repo's
   gate mesh"* (PLAYBOOK:2189–2197). A provider table cannot inherit that measurement; a new
   provider needs its own.

### 3.3 GO / NO-GO for CLOUD-4 — Section 3

**GO — narrowly, and this is the highest-value cut in the whole brief.**

**GO on the 9 table-edit sites.** Land **one** provider/model registry (`ecosystem/` YAML, beside
`tool-versions.yaml`, whose two-key shape is already the right one) and repoint S7–S11, S17, S26,
S29, S30 at it. This is genuinely *"swap via a table, not a rewrite"*, it is a **read-and-repoint**
change with no doctrine attached, and it is worth doing whether or not a swap ever happens — today
`claude-sonnet-5` is hardcoded in **three different file formats** (`.md` frontmatter, `.js` object
literal, `.md` prose) with nothing asserting they agree.

**NO-GO on the 12 doctrine sites.** Each needs an ADR or a recorded ruling. Two are especially
load-bearing and must not be swept into a lane: **S1** (the branch-prefix enum — CLAUDE.md §4 says
in terms that a prefix enters "only via a recorded ruling, never silently") and **S23**
(ADR-70's XL tier is an immutable ADR; supersede, never edit).

**NO-GO on the 10 code sites for now** — S2–S5, S13, S14, S24, S25, S27 are a real
port, not a parameterization, and per the memo's own steelman (line 154) they are the mechanisms
worth *keeping* Claude-specific: *"do NOT sacrifice Claude-specific mechanisms to the lowest common
denominator."*

**The one thing CLOUD-4 must record even if it does nothing else:** S21's finding, that
`~/.claude/ROUTING.md` is the canonical routing table and **is not in this repo**. Any
"provider-agnostic repo" claim is false while the routing source of truth sits at L0 outside version
control here. That is a **finding for the architect**, and the honest options are (a) bring a copy
in-repo with a drift gate — reversing #158 Decision B for a stated reason, or (b) state explicitly
in ARCHITECTURE Ch3 that routing is an L0 concern and out of the repo's universalization scope.
Either is fine; silence is not.

---

## 4. [#82] provider profiles — design inputs and feeds

### 4.1 The row, read from the repo

`tasks/82-define-per-repository-agentic-review-profiles.md` (`status: open`, `priority: P3`,
`size: M`, theme `[E6] Cross-repo universalization`, story `[S15]`), mirrored verbatim at
`BACKLOG.md:210`.

> **[#82] [P3][M] Define per-repository agentic-review profiles** — what agentic review each repo
> runs (dev-knowledge = methodology conformance; child repos = their domain needs, e.g.
> corp-monorepo deep-audit, ai-council's flow) and on what cadence, so agentic-ness is deliberate
> per repo. · **Done when:** every member of the `adr104-fleet-members` declaration carries a
> recorded agentic-review profile (which review runs, and on what cadence) at its stated home, and
> any member deliberately without one is named there with its reason · refs ADR-70, #9, #70.

**Naming correction, stated because it changes what the lane builds:** the brief calls [#82]
"provider profiles". The row is **agentic-*review* profiles** — *which review runs, on what
cadence, per repo*. Provider/model choice is an **input** to a profile
(`model_reasoning_effort` is one of its listed keys), not the profile's subject. A lane that builds
a provider-routing table and closes [#82] would not satisfy the Done-when.

**Design inputs the row already carries as live** (quoted):

1. **heterogeneous second reader** — *"(different model architecture) is the field-validated shape
   — same-model self-review fails to sycophantic convergence"*.
2. **evaluate natives first** — *"`/code-review --fix`, `/simplify`, `/code-review ultra` — the last
   a COMPLEMENT to Codex cross-vendor heterogeneity, not a substitute — before any plugin/custom
   simplifier"*.
3. **per-profile keys** — `model_reasoning_effort` plus output-hygiene `hide_agent_reasoning`,
   `web_search`.
4. **Un-deferral provenance** — *"UN-DEFERRED 2026-08-09 (ARC-2): peg 'per-repo at Wave-1
   onboarding' met 2026-07-07 ([#221] closed), one day BEFORE the peg was written."*

Input 1 is the reason this row belongs in a universalization brief at all: **heterogeneity is the
requirement**. [#82] does not want a provider-agnostic repo so any provider can be swapped in — it
wants **at least two providers present at once**, because a single-provider fleet cannot satisfy
"different model architecture". Portability is therefore not insurance here; it is the mechanism.

### 4.2 Design inputs the build lane still needs

**D1 — the member roster, which is fixed and machine-locatable.** `adr104-fleet-members`
(`docs/decisions/ADR-104-fleet-repository-shape.md:149–161`) declares **nine** ids:
`.dev-knowledge`, `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`,
`demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`. It is delimiter-anchored
(`<!-- declaration:start id=adr104-fleet-members v=1 -->`), read by
`scripts/audit.py::check_membership_agreement` (`_DECL_ANCHOR_ID`, `audit.py:2651`) and pinned in
both directions by `tests/test_membership_agreement.py:221`. **The lane must not re-derive the
roster** — it reads this anchor.

**D2 — "its stated home" needs defining, and four members have no home.** The Done-when says each
profile lives *"at its stated home"* but does not say where that is. `ecosystem/parity-surfaces.yaml`
records four of the nine as `role: pre-deploy` — `demo-prep`, `life-architect`, `terminal-setup`
(*"no VISION.md, no CLAUDE.md, no deploy record"*), `win-tooling`. **A repo with no `CLAUDE.md`
has nowhere to state a profile.** The Done-when's own escape clause covers this — *"any member
deliberately without one is named there with its reason"* — but the lane must decide **where
"there" is**. Candidate homes, in order of fit: (a) `ecosystem/parity-surfaces.yaml` as a new
surface class (already has an `ownership`/`reason`/`provenance` shape and already carries per-repo
`role` + `reason` rows for exactly these four); (b) a new `ecosystem/review-profiles.yaml`;
(c) each repo's own `CLAUDE.md` §8 (fails for the four homeless members, and Layer 2 may not write
them anyway).  **Recommend (a).**

**D3 — the cadence vocabulary.** "On what cadence" needs a closed enum, or profiles drift into
prose. Live cadences already in the tree: `nightly` (conformance digest), `pre-merge`
(`/codex-review`, `/ship`), `operator (push)` (`/changelog-review`), `monthly` /
`after major refactors` (`codex/AGENTS.md`'s full-audit mode), `weekly informal`
(PLAYBOOK discovery). **Recommend an enum drawn from ARCHITECTURE.md:313's existing trigger
column** rather than a new vocabulary.

**D4 — the heterogeneity constraint, made checkable.** Input 1 is currently prose. To be
enforceable a profile needs to name **which model architecture** reviews, so a check can assert
reviewer ≠ author. This is the point where [#82] **hard-depends on §3**: the reviewer identity today
is `gpt-5.6-terra`, pinned in `~/.claude/bin/codex-review.ps1` — **outside this repo** (S19). A
profile that names a reviewer the repo cannot read cannot be verified from the repo.

**D5 — the natives-first evaluation, not yet done.** Input 2 says evaluate `/code-review --fix`,
`/simplify`, `/code-review ultra` before any custom simplifier. That evaluation is **evidence the
lane must produce**, and per ADR-74's rubric it carries an **n=2 gate** (*"a routine codifies only
after two real runs"* — ARCHITECTURE.md ~line 690). Two runs per candidate, pre-registered kill
criteria.

**D6 — the `#341` block on the Codex producer lane.** PLAYBOOK:4262 is explicit: *"the producer
lane is NOT activatable as written today … Do not treat 'Codex producer' as available."* A profile
that assigns Codex an authoring role is describing future work. **Profiles may specify Codex as
reviewer only**, until `#341` lands and is ruled.

**D7 — ADR-70's tier structure, including XL.** ADR-70 anchors S/M/L; the amendment 2026-07-07 adds
**XL = Claude Fable 5** scoped to the browser-architect layer, explicitly **orthogonal** to the
fan-out sizes (Decision 2) and with a **mandatory anti-conflation note** vs ADR-80 §5's
`fallbackModel` prohibition (Decision 4). A profile schema that flattens XL into a fourth fan-out
size re-introduces exactly the conflation that amendment forbids.

**D8 — `#9` and `#70` are unreadable from this container.** The row's `refs ADR-70, #9, #70` cite
two ids with **no live `tasks/` file and no `BACKLOG.md` row** — both are closed, and the shallow
clone means their content is not recoverable here. The build lane must recover them from full
history before treating input 2's "natives-first" framing as complete.

### 4.3 Which of Sections 1–3 feed [#82]

| Feeds | How | Strength |
|---|---|---|
| **§3 → [#82]** | The seam inventory **is** the profile schema's value domain. Every field a profile needs — reviewer model string (S17, S18), routing tier (S15, S16, S23), effort key (S12/S13's `--effort high`), invocation (S13, S14, S19) — is a §3 row. And §3's S21/S19/S20 finding (**three highest-leverage seams live at L0, outside the repo**) is the constraint that decides whether a profile can be *verified* from the repo or only *recorded* in it. | **PRIMARY — direct** |
| **§2 → [#82]** | Heterogeneity (input 1) requires ≥2 providers reading the same repo doctrine. `AGENTS.md` is the layer that makes a Codex/Cursor reviewer see the same rules a Claude author saw — otherwise the "different architecture" reader is reviewing against different instructions, and the heterogeneity is confounded. **§2's precedence collision is the direct blocker**: a root `AGENTS.md` concatenates *after* `~/.codex/AGENTS.md`, the file that today *defines Codex's reviewer role* — the exact role [#82] is profiling. R1 must land before a Codex review profile can be written down. | **PRIMARY — blocking** |
| **§1 → [#82]** | Weak and indirect. VISION.md naming does not affect review profiles. **Two real touchpoints:** (i) `check_vision_md` and the ADR-38 baseline set are **part of what `.dev-knowledge`'s own "methodology conformance" review checks**, so renaming changes that profile's content; (ii) §1's method — the immutable/live partition and the "0 references are links" finding — is the **template** for [#82]'s D2 problem: enumerate every site, decide which are writable, before touching anything. | **SECONDARY — method, not content** |

**Cleanest sequencing:** §3's table-edit registry → R1 ruling (fed by §2) → [#82] schema →
per-repo profiles. §1 sits on a separate track and gates none of it.

### 4.4 GO / NO-GO for CLOUD-4 — Section 4

**NO-GO on building [#82] in CLOUD-4.** Four independent blockers, none of which a mutation lane can
clear on its own authority:

- **D2** — four of nine members have no home for a profile (no `CLAUDE.md`, no deploy record), and
  §5 rule 4 forbids the hub writing into them.
- **D4** — the reviewer identity that makes heterogeneity checkable lives at L0
  (`~/.claude/bin/codex-review.ps1`), outside this repo.
- **D5** — the natives-first evaluation is unstarted and carries ADR-74's **n=2** evidence gate;
  that is two real runs per candidate, which is a lane of its own.
- **D6** — the Codex producer role is doctrinally unavailable pending `#341`.

**GO on the two prerequisites, both of which are §3's output:**

1. **The provider/model registry** (§3.3's GO). It is [#82]'s value domain. Land it first and the
   profile schema writes itself; skip it and every profile hardcodes strings that already disagree
   across three file formats.
2. **A recorded decision on the L0 boundary** (§3.3's "one thing CLOUD-4 must record"). [#82]'s
   Done-when says *"carries a recorded agentic-review profile … at its stated home"*. If the
   reviewer pin lives at L0, then either the home is L0 — and [#82] is **partly unverifiable from
   this repo by construction**, which must be stated in the row rather than discovered at closure —
   or the pin comes in-repo. **Recommend deciding this before the schema, not after.** It is the
   difference between a row that can close and a row that cannot.

---

## 5. Summary — what CLOUD-4 should actually be cut as

Consolidated verdicts:

```
section  scope as briefed                      verdict   re-scoped GO
-------  -----------------------------------   -------   ----------------------------------------
1        VISION.md -> README.md rename          NO-GO     produce the ADR + a canonical-doc-name
                                                          registry the 10 constants read from
2        author AGENT.md / provider split       NO-GO     produce intake R1's decision packet
                                                          (4 named inputs, incl. the 32 KiB
                                                          precedence collision)
3        provider-swap seam inventory           GO        land ONE model/provider registry;
                                                          repoint the 9 table-edit sites
4        [#82] provider profiles                NO-GO     land section 3's registry + rule the
                                                          L0-boundary question first
```

**The one-sentence finding:** this repo is **much closer to provider-agnostic than the brief
assumes on the enforcement axis** — 19 pre-commit/pre-push/commit-msg gates plus a GitHub Actions
wall already run under any agent, and the repo's own ADR-85 amendment deliberately moved the teeth
off the Claude-specific Stop hook — **and much further from it on the routing axis**, where the
canonical table (`~/.claude/ROUTING.md`), the reviewer pin (`~/.claude/bin/codex-review.ps1`) and
the Codex config (`~/.codex/config.toml`) all sit at L0, outside this repository entirely.

**If CLOUD-4 lands exactly one thing, make it the model/provider registry from §3.3.** It is the
only cut in the brief with no doctrine gate, no fleet coordination, no immutable-artifact cost, and
a standalone payoff — and it is the prerequisite [#82] is actually waiting on.

**Three items are handed to the architect, not to a lane:**

- **CONFLICT-1** — where `ARTIFACT-*.md` may legally live (`docs/audits/` recommended).
- **CONFLICT-2** — whether root `README.md` may be recreated at all (ADR-38 A5 + ADR-101 §1).
- **CONFLICT-3 / R1** — whether `AGENTS.md` is admitted or refused, and under which reading of
  ADR-53.

---

*Read-only lane. Nothing in this repository was modified except this file. No merge, no push to
`main`, no file moved. Every count above is reproducible at the bound revision with the commands
quoted inline.*
