# NB2 · CLOUD C4 — codex-surface census

**Substrate:** cloud · **Repo:** `dev-knowledge` @ `origin/main` `fcc9485` (`Merge branch 'docs/batch-2-dispatch' -- night-batch-2 frozen`)
**Mode:** READ-ONLY. Zero writes, zero deletions, zero commits, zero branches. `git status --porcelain` empty at start and unchanged at end.
**Gates:** not run — container `uv` is 0.8.17 vs pinned `==0.11.19`. Every gate/pytest/`audit.py`-dependent claim below is marked `MEASUREMENT-OWED-LOCAL`.

---

## 0. HEADLINE

**Zero surfaces are REMOVAL-READY.** Every one of the seven codex classes has at least one live consumer, a protecting ruling, or is the precedence trap itself. This is not an under-search result — §5 records the adversarial re-search the self-audit clause demands, and it *strengthened* the blocks rather than weakening them.

The single largest surface — 168 audit artifacts, 630,460 B — turns out to be the **most** blocked, not the least: 166 of the 168 are enumerated **by filename** inside two machine baselines that four live scripts read.

---

## 1. FIGURE VERIFICATION (brief's numbers vs mine)

### 1a. "168 codex-* audit artifacts" — **CONFIRMED, exactly**

```
$ ls docs/audits/*codex*.md | wc -l
168
```

Cross-checks:
- `find docs/audits -iname '*codex*' | wc -l` → **169**. The 169th is the brief's own contract file, `docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C4-codex-census.md` (4,836 B) — one level down, not a top-level artifact. The brief's 168 is the top-level figure and it is right.
- Name-pattern: 165 of the 168 are `YYYY-MM-DD-codex-*`; 3 are `*-codex-*` (`2026-07-12-technical-night-codex-review.md`, `2026-06-07-…-codex-max-audit.md` class).
- Date span: 2026-04 ×1 · 05 ×6 · 06 ×22 · 07 ×59 · 08 ×80. Growth is accelerating, not plateauing.
- Total bytes: **630,460 B** (`ls docs/audits/*codex*.md | xargs stat -c%s | paste -sd+ | bc`).

### 1b. "587 files tree-wide with codex- references" — **NOT REPRODUCIBLE**

My number for the literal predicate the brief states (`codex-`, tree-wide):

```
$ git grep -lI -- 'codex-' | wc -l
525
$ grep -rlI --exclude-dir=.git -- 'codex-' . | wc -l      # worktree, incl. untracked
525
```

**525, not 587.** I tried ten derivations to find one that lands on 587; none does. Reported in full rather than silently picking the closest:

```
predicate                                              count
-----------------------------------------------------  -----
content 'codex-'  (the brief's literal predicate)        525   <- my answer
name-or-content 'codex-'                                 529
content cs 'codex', excl docs/handoffs                   537
content 'codex-', *.md only                              475
name-or-content 'codex-', *.md only                      479
content ci 'codex', excl docs/handoffs                   634
content 'Codex' (capitalised)                            605
content cs 'codex'                                       690
content cs whole-word 'codex'                            689
content cs 'codex', excl JOURNAL.md + LESSONS.md         688
content ci 'codex'                                       863
content ci 'codex', *.md only                            765
```

587 sits inside the 525–863 bracket but matches **no** predicate I could construct. Two candidate explanations, neither verifiable from here:

1. The operator's disk is ahead of `origin/main` and carries ~62 more `codex-`-bearing files. **Weak** — my clone-vs-disk anchor check (§1c) shows the clone is *ahead*, not behind.
2. The figure was derived under a predicate not stated in the brief (a different case sensitivity, a different exclusion set, or an untracked-file-inclusive sweep on a dirty tree).

**Verdict: 587 is UNVERIFIED. Use 525.** This is exactly the class `CLAUDE.md` §4 names ("never restate a count or roster in prose — cite the surface that computes it"); the brief's own corrected figure is itself a restated count that did not survive re-derivation. The 168 did.

Breakdown of the 525 by home:

```
329  docs/audits          12  tests               5  (root)
113  docs/handoffs         8  scripts             4  protocols
 23  tasks                 7  ecosystem           2  tests/fixtures
  7  docs/intake           7  deploy              1  templates/archive
  5  docs/decisions        1  .claude/commands    1  docs/archive
```

### 1c. Clone-vs-disk anchors (brief §"Repo facts")

```
anchor                          brief (disk)   clone @fcc9485   delta
docs/intake/*.md                        56              56        =
docs/decisions/*.md (top)               89              89        =
docs/audits/*.md (top)                 769             773       +4
tasks/**/*.md                          344             344        =
BACKLOG.md bytes                    67,883          67,883        =
```

Four of five identical; the clone carries **4 more** top-level audits than the operator's 23:36 measurement — consistent with the batch-2 dispatch commit `e23e001` landing after it. The clone is ahead, so a "disk is ahead" explanation for the 587 gap does not hold.

---

## 2. THE PRECEDENCE TRAP — classified explicitly, and it is worse than the brief states

**Surface:** `codex/AGENTS.md` (3,891 B, 79 lines) · **Verdict: `PRECEDENCE-TRAP` + `BLOCKED-BY` ×6**

The brief is right that root `AGENTS.md` names this file. The locators:

```
AGENTS.md:8      ## Precedence — resolved BY SCOPE, not by position
AGENTS.md:10     > required by ADR-115 §3.2
AGENTS.md:19     | `~/.codex/AGENTS.md` (L0, operator disk) | the reviewer role … |
AGENTS.md:21     | `codex/AGENTS.md` (intermediate dir)     | its own subtree only |
AGENTS.md:23-24  The third layer is a **known trap**: a cwd at or below `codex/` yields
                 `role → doctrine → role`, and the role wins by position rather than by intent.
```

Deleting `codex/AGENTS.md` — or the `codex/` tree containing it — would leave `AGENTS.md:21` describing a file that does not exist, inside a section **ADR-115 §3.2 requires the file to carry**. That alone makes it unusable as a removal target, exactly as the brief says.

**But the trap is deeper than "it is documented."** Reading the file itself:

```
codex/AGENTS.md:1  # AGENTS.md — Global Codex Reviewer Configuration
codex/AGENTS.md:3  > **Canonical source** for `~/.codex/AGENTS.md`. Owned by `.dev-knowledge`.
                   > Deploy by copying to `~/.codex/AGENTS.md`.
```

`codex/AGENTS.md` is **not** an intermediate-directory doctrine file that "governs its own subtree." It is the **canonical deploy source for layer 1** — the file that *becomes* `~/.codex/AGENTS.md`. Its presence at `codex/` is an authoring-home accident, and the precedence collision root `AGENTS.md:21` documents is a **side effect of where the deploy source is parked**, not a designed layer.

Consequence, stated so it is not discovered later: **root `AGENTS.md:21`'s "governs its own subtree only" is a mischaracterisation.** Layer 1 and layer 3 in that table are the same content — one is the deploy source of the other. A cwd at or below `codex/` does not yield `role → doctrine → role` with three distinct authorities; it yields `role → doctrine → the same role again`. The trap is real and the guidance ("run from the repo root") is correct, but the *reason* given is wrong. Filed here as a finding, not fixed — this lane writes nothing.

**Live code consumers of `codex/AGENTS.md`, any of which independently blocks removal:**

```
deploy/carrier_globalconfig.py:53   DEFAULT_SOURCE_REL = "codex/AGENTS.md"  # hub canonical source (ADR-54)
deploy/carrier_globalconfig.py:18   source_path: codex/AGENTS.md
deploy/manifest-v1.0.0.yaml:45      source_path: codex/AGENTS.md
deploy/manifest-v1.1.0.yaml:77      source_path: codex/AGENTS.md
ARCHITECTURE.md:335                 canonical source `codex/AGENTS.md`; ADR-54
.methodology.yaml:135               (codex/AGENTS.md -> ~/.codex, ADR-54)
AGENTS.md:21                        the precedence table row itself
```

Plus a **second, independent structural block**: `scripts/validate_hermetization.py:191` carries `"codex"` in the Rule-C `_HOME_PATTERNS` home allowlist, and `:161-165` states that allowlist is *derived from the live taxonomy* with `test_rule_c_admits_every_tracked_path` asserting it against `git ls-files`. Deleting the `codex/` tree would leave an allowlist pattern describing a home no tracked file occupies. Whether that reds the test is `MEASUREMENT-OWED-LOCAL` (the assertion direction is allowlist⊇tree, so a stale-but-superset pattern may pass) — but the enum entry becomes a lie either way, and `validate_hermetization.py:67` also carries `codex` in the Tier-1 sanctioned-dirs literal (corroborated at `protocols/STANDING_RULINGS.md:1559`: *"`SANCTIONED_TIER1_DIRS` already contains `codex`"*).

---

## 3. PER-CLASS CONSUMER ENUMERATION

### C1 · Audit artifacts — 168 files, 630,460 B

**Consumers, in order of strength:**

**(a) `scripts/audit.py::check_review_artifact_coverage` — a live audit check that globs the whole directory.**

```
scripts/audit.py:3659   _REVIEW_TITLE_RE = re.compile(r"(?m)^# Codex Review\b")
scripts/audit.py:3745   for p in sorted(audits.glob("*.md")):
scripts/audit.py:3722   HUB-ONLY … the codex-review convention is a hub practice (108 artifacts here, none in a consumer)
```

Measured against the live predicate:

```
$ grep -lE '^# Codex Review\b' docs/audits/*.md | wc -l
153                       # files the check actually treats as review artifacts
$ grep -lE '^# Codex Review\b' docs/audits/*.md | grep -c codex
150                       # of those, codex-NAMED
18                        # codex-NAMED that do NOT carry the title
3                         # NON-codex-named that DO carry it
```

The three non-codex-named artifacts the check *does* read:
`docs/audits/2026-08-09-technical-night-n2-mechanism-map.md`, `2026-08-15-verification-night3-landed-review.md`, `2026-08-16-verification-nb4-playbook-gap.md`.

**Defect surfaced in passing:** `audit.py:3631` and `audit.py:3722` (and `tests/test_review_artifact_coverage.py:16`) each hardcode **"108 codex artifacts"** against a live 168, and "153" against the live title-predicate. Three restated counts, all stale — the `CLAUDE.md` §4 anti-pattern, inside the enforcement code. Not fixed here (read-only); named for the worklist.

**(b) Two machine baselines that enumerate audits BY FILENAME.** This is the hard block.

```
$ python3 -c '<extract "*.md" literals from both baselines; intersect with docs/audits/*codex*.md>'
codex audits total: 168   in a baseline: 166   NOT in either: 2
```

- `ecosystem/audit-consumer-baseline.json` names **149** of them (e.g. `:537 "2026-08-28-codex-batch1-lane-a-review.md"`)
- `ecosystem/audit-funnel-baseline.json` names **143**
- Union: 166/168.

Readers of those baselines:

```
scripts/audit.py
scripts/audit_checks/check_consumer_at_landing.py
scripts/consumer_at_landing.py
scripts/funnel_coverage.py
tests/test_consumer_at_landing.py
```

Deleting any of those 166 files desynchronises a baseline that five live surfaces read. Whether the resulting audit check FAILs or WARNs is `MEASUREMENT-OWED-LOCAL`.

**(c) The generated index.** `docs/audits/README.md` carries **170** codex references and is gated by the `audit-index-freshness` pre-commit hook (`gen_audit_index.py --check`, `scripts/gen_audit_index.py:143` globs `*.md`). Any deletion requires an index regeneration in the same commit or the hook blocks. `MEASUREMENT-OWED-LOCAL`.

**(d) Named citation coverage is 168/168.** Per-file `git grep -F <basename>` excluding `docs/audits/` and `docs/handoffs/`:

```
149  ecosystem/audit-consumer-baseline.json
143  ecosystem/audit-funnel-baseline.json
 66  JOURNAL.md
  2  protocols/STANDING_RULINGS.md          2  docs/decisions/README.md
  1 each: scripts/audit.py · scripts/check_provider_registry.py · scripts/desired_state_report.py
          ecosystem/disposition-register.yaml · deploy/release-v1.3.x-contract.md
          docs/decisions/ADR-107-…md · 5 tests/ · 1 fixture jsonl · 16 tasks/*.md
```

**Not one of the 168 is uncited.** The 2 outside both baselines are cited anyway — `2026-08-14-codex-524-check-extensions.md` (JOURNAL + 3 audits) and `2026-08-26-codex-adr115-acceptance-review.md` (JOURNAL + `docs/audits/README.md` + `protocols/STANDING_RULINGS.md`).

**(e) Immutability.** `CLAUDE.md` §5 rule 3 and `AGENTS.md` "File rules that will bite you": *"Immutable: ADRs, transcripts, handoffs, audits — supersede with a new file."* Corroborated `protocols/STANDING_RULINGS.md:1016` (*"Audits are immutable, so the correction lives here"*). There is **no retention/expiry convention for `docs/audits/`** — `STANDING_RULINGS.md:945-946` explicitly rules retention "resolves itself" by branch-deletion, i.e. deliberately declines a deletion rule.

**Verdict: `BLOCKED-BY` ×5 + `PROTECTED` (immutability doctrine, no retention rule).** 630,460 B, and none of it is free.

---

### C2 · The `codex/` tree — 1 file, 3,891 B

**Verdict: `PRECEDENCE-TRAP`.** Full treatment in §2. Also `BLOCKED-BY deploy/carrier_globalconfig.py` and five more.

---

### C3 · `/codex-review` command + skill — **0 B in this repo**

The command **does not exist in this repository.** Search that establishes it:

```
$ git ls-files | grep -i 'codex.review'
docs/audits/…  docs/decisions/ADR-54-…  tasks/…  templates/codex-review-config-template.md
# no .claude/commands/codex-review.md ; no .claude/skills/codex-review/

$ ls .claude/commands/
changelog-review.md  handoff-verify.md  handoff.md  lane-boot.md
lane-integrate.md    override.md        preflight.md  save.md

$ ls .claude/skills/
check-against-spec  verify
```

It is an **L0 surface on the operator's disk**, registered as such:

```
ecosystem/organ-registry.yaml:55-60
  - name: "/codex-review"
    class: command
    source: "~/.claude/commands/codex-review.md"
    distribution: L0
    status: ARMED
```

Corroborated by `CLAUDE.md` §7 (`/codex-review` listed under *User-level (`~/.claude/commands/`)*), `ecosystem/provider-registry.yaml:33` and `:292` (`~/.claude/bin/codex-review.ps1`, S19, *"NOT asserted from this repo"*), and by an open backlog row that says so in as many words:

```
docs/audits/2026-08-01-technical-night-batch-l1-filing-pre-pack.md:126
  [#470] … the command is user-level (`~/.claude/commands/codex-review.md`), OUTSIDE this
  repo, so the 2026-08-01 night batch could NOT verify what model it selects
```

**Verdict: `OUT-OF-SCOPE` — nothing to remove here.** It is registered ARMED at L0 and three open tasks (#431, #445, plus #341) describe defects in it, so it is live software, merely not this repo's bytes. Removing the registry row would blind `ecosystem/organ-index.md` (gated by `organ-index-freshness`).

The in-repo half — `templates/codex-review-config-template.md` (5,556 B) — is **`BLOCKED-BY protocols/PLAYBOOK.md:3555`**:

```
protocols/PLAYBOOK.md:3555
  - **Code review:** Codex configuration → see `templates/codex-review-config-template.md`
```

A canonical living doc under the freshness cadence points at it by path. Bare-stem re-search (`git grep -ln 'codex-review-config'`) returns 40+ files; the PLAYBOOK line is the one live pointer, the rest are JOURNAL/LESSONS/audits/handoff snapshots (immutable) and `templates/archive/AGENTS-md-template.md:69`.

---

### C4 · Provider / routing / registry rows

```
surface                                    codex rows   gate
ecosystem/provider-registry.yaml           :33 :78-81 :113 :185 :292   provider-registry-agreement (pre-commit)
ecosystem/routing-table.yaml               :25 :27 :31 :34             scripts/routing_agreement.py + tests
ecosystem/organ-registry.yaml              :55-60                      organ-index-freshness (pre-commit)
ecosystem/tool-versions.yaml               :15-17 :28-36               changelog_sentinel.py + provider-registry-agreement (S8)
ecosystem/dependency-baseline.yaml         :4                          comment only
ecosystem/parity-surfaces.yaml             :273                        scripts/fleet_parity.py
ecosystem/disposition-register.yaml        :21 :561 :566 :636          scripts/audit.py disposition checks
```

`provider-registry.yaml:78-81` is a **live tool row** (`cli: codex`, `version_command: ["codex","--version"]`, `changelog_tool_key: codex`, `changelog_source_url`), read by `scripts/changelog_sentinel.py:4,52` (the SessionStart sentinel) and asserted by the `provider-registry-agreement` pre-commit hook across nine seams. `routing-table.yaml:31-34` pins `reviewer: cli: codex, model: gpt-5.6-terra`.

**Verdict: `BLOCKED-BY` — all seven files. Every row is under an armed gate.** Gate-pass confirmation is `MEASUREMENT-OWED-LOCAL`.

---

### C5 · Hooks and validators

```
scripts/validate_hermetization.py:67    "codex" in SANCTIONED_TIER1_DIRS literal
scripts/validate_hermetization.py:141   "codex" in SANCTIONED_GENRES (audit filename genre)
scripts/validate_hermetization.py:191   "codex" in _HOME_PATTERNS (Rule C home allowlist)
scripts/audit.py:3659, 3722, 3631       check_review_artifact_coverage (§C1a)
scripts/changelog_sentinel.py:4, 52     parses `codex-cli 0.136.0`
scripts/check_provider_registry.py:71   cites docs/audits/2026-08-13-codex-w3-landing-predicate.md
```

`SANCTIONED_GENRES` containing `"codex"` (`:133`: *"adopts what three repos already write: `codex` not `codex-review`"*) is what **permits** a `docs/audits/YYYY-MM-DD-codex-*.md` filename to pass Rule B. Removing it would block every future codex artifact from being committed.

**Verdict: `BLOCKED-BY` — enum removal changes gate behaviour, not just bytes.**

---

### C6 · Tests — 37 files, 5,556 codex references

Top consumers by hit count:

```
tests/test_lived_sandbox_observer.py   16    tests/test_audit.py                 9
tests/test_deploy_globalconfig.py      16    tests/test_lived_sandbox_consumer.py 7
tests/test_changelog_sentinel.py       11    tests/test_routing_agreement.py      6
tests/test_verify_handoff_probes.py    10    tests/fixtures/manifest-v1.1.0-…yaml 6
tests/test_fleet_parity.py              9    tests/fixtures/lived-workflow/*.jsonl 6+2
… 27 more, each 1–5
```

`tests/test_deploy_globalconfig.py` (7,465 B) exists solely to test the `codex/AGENTS.md` → `~/.codex/AGENTS.md` carrier. `tests/test_review_artifact_coverage.py:120,131` synthesises `# Codex Review — <slug>` fixtures and `<date>-codex-<slug>.md` filenames.

**Verdict: `BLOCKED-BY` — 37 test files.** Suite status `MEASUREMENT-OWED-LOCAL`.

---

### C7 · Doc references — records, mostly immutable

```
docs/decisions/ADR-54-codex-reviewer-global-standard.md   4,971 B   Status: Accepted (2026-05-19)
docs/handoffs/archive/legacy/2026-04-15-codex-tach-…md    5,070 B   immutable handoff
docs/intake/archive/2026-07-13-siem-…-codex.md           35,808 B   cited by 6 live+immutable surfaces
tasks/{341,431,445}-*.md                                            status: open
tasks/{338,363,469}-*.md                                            status: closed
protocols/{PLAYBOOK,ESSENTIALS,ENVIRONMENT,STANDING_RULINGS,HANDOFF_PROCESS,REPO_ONBOARDING}.md
CLAUDE.md · AGENTS.md · ARCHITECTURE.md · CONTRIBUTING.md · JOURNAL.md · LESSONS.md · BACKLOG.md
```

ADR-54 is **Accepted, not superseded**, and is the governing decision for the whole global-config carrier — cited at `ARCHITECTURE.md:335`, `.methodology.yaml:135`, `deploy/carrier_globalconfig.py:53`, and four manifests.

`tasks/*.md` is the **source of truth** for the generated `BACKLOG.md` ([#439], ADR-107 §7.2, gated by `check_task_tree_coherence`). Three rows are `status: open` — #341 (Codex producer-lane activation), #431 (doc-lane silently dropped), #445 (path-guard reports SUCCESS having reviewed nothing). Removing an open row deletes live work.

The archived intake (35,808 B — the second-largest single codex-named file) is cited by `ecosystem/conformance.md`, `ecosystem/conformance.html`, `docs/intake/2026-07-11-tech-ownership-manifest.md`, and three audits. `docs/intake/README.md`'s Contents block is gated by `intake-index-freshness`.

**Verdict: `PROTECTED` (immutable class / Accepted ADR) or `BLOCKED-BY` (generated-index gates, open task rows).**

---

## 4. REMOVAL-READINESS VERDICTS — ordered by size freed

```
#   surface                                            bytes     verdict
--  -------------------------------------------------  --------  ----------------------------
 1  docs/audits/*codex*.md  (168 files)                 630,460  BLOCKED-BY x5 + PROTECTED
                                                                 audit.py::check_review_artifact_coverage;
                                                                 audit-consumer-baseline.json (149);
                                                                 audit-funnel-baseline.json (143);
                                                                 docs/audits/README.md (gated);
                                                                 JOURNAL.md (66); immutability doctrine
 2  docs/intake/archive/…-codex.md                       35,808  BLOCKED-BY conformance.md/.html,
                                                                 intake-index-freshness, 3 audits
 3  deploy/carrier_globalconfig.py                        9,511  BLOCKED-BY manifests v1.0.0-v1.4.0,
                                                                 test_deploy_globalconfig.py, ADR-54
 4  tasks/*codex*.md  (6 files, 3 OPEN)                   8,874  BLOCKED-BY gen_task_tree.py source-of-truth
 5  tests/test_deploy_globalconfig.py                     7,465  BLOCKED-BY the carrier it tests
 6  templates/codex-review-config-template.md             5,556  BLOCKED-BY protocols/PLAYBOOK.md:3555
 7  docs/handoffs/archive/legacy/…-codex-tach-…md         5,070  PROTECTED  immutable handoff class
 8  docs/decisions/ADR-54-…md                             4,971  PROTECTED  Accepted, never superseded
 9  codex/AGENTS.md                                       3,891  PRECEDENCE-TRAP  (+ BLOCKED-BY x6)
10  ecosystem/*.yaml codex rows  (7 files)                 rows  BLOCKED-BY  4 armed gates
11  scripts/ codex enums + logic  (6 files)                rows  BLOCKED-BY  removing an enum entry
                                                                 changes gate behaviour, not bytes
12  tests/  codex references  (37 files)                   refs  BLOCKED-BY
13  /codex-review command + wrapper                            0  OUT-OF-SCOPE  lives at L0
                                                                 (~/.claude/), registered ARMED

REMOVAL-READY: 0 surfaces, 0 bytes.
```

---

## 5. SELF-AUDIT

**The clause:** *"if your `REMOVAL-READY` count is large, re-run one of them against the whole tree with a different search (a grep for the bare stem, not the full path) before you claim zero consumers. The cheap way to look productive here is to under-search."*

**My REMOVAL-READY count is 0** — the failure mode the clause guards (a large removal-ready list produced by under-searching) did not occur. But the inverse failure — *over*-claiming blocks to look thorough — is equally available, so I ran the bare-stem re-search **against my three weakest blocks** rather than skipping it:

1. **`templates/codex-review-config-template.md`** — full-path search found 40 hits, but almost all in JOURNAL / LESSONS / handoff snapshots (immutable, not live readers). Bare-stem `git grep -ln 'codex-review-config'` confirmed the same set. The block therefore rests on **exactly one** live line: `protocols/PLAYBOOK.md:3555`. Narrow, but a canonical living doc under the freshness cadence — real. Reported as one line, not inflated to forty.

2. **The 168 audits** — I did not stop at "they're immutable." I ran a **per-file** `git grep -F <basename>` over all 168, excluding `docs/audits/` and `docs/handoffs/` (the two homes that would trivially self-cite), and got **168/168 cited**. That result was surprising enough that I re-derived it structurally: the two `ecosystem/*-baseline.json` files enumerate 166 by filename, and the 2 stragglers are cited in JOURNAL / STANDING_RULINGS. The block is machine-verifiable, not asserted.

3. **`codex/AGENTS.md`** — bare-stem `git grep -n 'codex/AGENTS'` surfaced `deploy/carrier_globalconfig.py:53` and `.methodology.yaml:135`, **neither of which the precedence-trap framing would have found.** The trap is real, and it was not the only block. Had I stopped at the trap I would have under-searched a live carrier.

**Where this report could still be wrong, named rather than left to be found:**

- **The 587 figure is unresolved.** I could not reproduce it under ten predicates and I do not know what produced it. My 525 is reproducible and shown; if the operator's derivation differs, mine is the one to check, not to trust by default.
- **Every gate/suite consequence is `MEASUREMENT-OWED-LOCAL`.** I established that consumers *exist* and *read* these surfaces by locator. I did **not** establish that any specific deletion turns a gate red — `uv` mismatch prevents it. "Consumer exists" ≠ "gate fails"; treat the verdicts as removal-**blocking evidence**, not as gate predictions.
- **`docs/audits/` at 773 files with no retention convention** is the real finding underneath this census, and it is out of this lane's scope to rule on. The 168 codex artifacts are 21.7% of that directory; the growth curve (1 → 6 → 22 → 59 → 80 across five months) says the class doubles roughly quarterly, and `STANDING_RULINGS.md:945-946` deliberately declined a retention rule on the grounds that branch-deletion resolves it — which it does not, for the artifacts themselves.

**Three stale restated counts found in passing, not fixed (read-only):** `scripts/audit.py:3631` and `:3722` and `tests/test_review_artifact_coverage.py:16` each say *"108 codex artifacts"* against a live **168**. The `CLAUDE.md` §4 defect class, sitting inside the enforcement code that polices it.

**One doctrine defect found in passing, not fixed:** root `AGENTS.md:21` characterises `codex/AGENTS.md` as an intermediate-directory file governing "its own subtree only." Per `codex/AGENTS.md:3` it is the canonical deploy source for layer 1 — layers 1 and 3 in that precedence table are the same content, not two authorities. The guidance is right; the reason given is not. Candidate for the worklist.

---

**Compliance:** zero files created, edited, deleted, staged, committed, branched, pushed or tagged. `git status --porcelain` empty. This report is the lane's entire output.