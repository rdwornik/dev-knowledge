> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a4-doc-freshness-derivation-audit` | receipt id `cse_01Pj8no7mTqTneUZVmRxGe2m` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a4-doc-freshness-derivation-audit.md`.
> Selection rule: the LONGEST assistant text, not the last - text #13 of 20 across 6 pages.
> Bytes written unchanged: **22,276**.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** HY-1 (`lane-k-11-derived-doc-freshness`).
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

# AUDIT — batch-e-a4-doc-freshness-derivation-audit

## Receipt

```
git-source-resolves-non-empty: https://github.com/rdwornik/dev-knowledge (origin, fetch+push)
                               HEAD ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b
first-assistant-text-echoed:   114 lines
                               final line: "- No edits outside this lane's declared footprint. Prose in English; hyphen-only names."
```

Write-scope honored: **0 tree files written, 0 commits, 0 rows.** Working tree clean, HEAD unchanged, no branch created. Ran `python3` directly (3.11.15) — **declared**, as the gate note requires. **No gate or hook was executed**; where a gate verdict is quoted below it was obtained by importing the gate's own pure `evaluate()` function read-only, and is labelled as such.

---

## PAUSE — three brief premises tested, three do not survive as stated

Reported per Q10, not repaired.

**1. "493 tracked `.md` files carry a `last_reviewed` field" — REFUTED. The true figure is 39.**

```
git grep -l last_reviewed -- '*.md'          -> 493   <- what the brief measured
.md files with a PARSEABLE last_reviewed
  key in YAML frontmatter                    ->  39   <- what the gate can actually read
.md files with any YAML frontmatter          -> 578
```
493 counts files that *mention the string* — ADRs, audits and handoff prose discussing the freshness regime. The stamped population is 12.6x smaller. The lane's sizing was therefore built on a grep, not a field.

**2. "2,761 files / 42,083,797 B" — the file count is right, the byte figure is not the corpus.**

```
tracked files                 2,761        <- correct
tracked bytes                 4,736,983 B  <- the actual corpus
working dir minus .git       42,083,797 B  <- the brief's figure
  (61,344,561 total - 19,260,764 .git = 42,083,797, exact)
```
The sizing measured the working directory less `.git`, which counts untracked/ignored build output. The tracked corpus is **8.9x smaller** than budgeted. The CLOUD routing call still stands on the git-walk leg (1,090 per-file commit diffs on the living set alone), but not on the arithmetic given.

**3. The PLAYBOOK premise — CONFIRMED in conclusion, wrong in two details.**

```
protocols/PLAYBOOK.md
  declared               2026-08-01   ("> Last updated:", line 8 — PROSE, not frontmatter)
  last CONTENT commit    2026-08-29   3a423bf1b
  delta                  +28 days     STALE
  total commits          262
```
Right that the stamp reads 2026-08-01 and right that it lies. Wrong that this followed "last night's edits" — PLAYBOOK's last content commit is **2026-08-29**, two days before today; nothing touched it on 08-30 or 08-31. The doc edited last night is `README.md` (2026-08-31), a *different* stale case. And the deeper fact the premise misses: PLAYBOOK carries **no `last_reviewed` frontmatter at all**. Its date lives in a prose line no gate parses, so this is not a stamp that drifted — it is a stamp the gate mesh cannot see. `audit.py:462-464` records this as a deliberate deferral.

---

## Substrate correction — the clone arrived shallow

`.git/shallow` was present on arrival: `is-shallow-repository = true`, 333 commits, history grafted at **2026-08-25**. Every git-derived date computed against it is a floor, not a fact — a file whose true last edit predates the graft reports the graft commit instead. A first pass under that graft wrongly dated `protocols/ESSENTIALS.md` and 14 others to 2026-08-26.

`git fetch --unshallow origin` recovered the full history: **6,122 commits, 2026-03-30 → 2026-08-31**. All figures below are against complete history. This touched `.git/` only — no working-tree file, no commit. **Any cloud lane in this repo that reads git dates without unshallowing first will produce silently wrong numbers.**

---

## 1. The CONTENT-vs-TOUCH rule (done-contract item 2)

A commit touching file F is **CONTENT** unless it matches a TOUCH predicate:

- **T1 — empty under whitespace-blindness.** `git show <sha> -w --ignore-blank-lines --ignore-space-at-eol -- F` yields no hunk. Catches reflows, blank-line churn, and merge commits carrying no unique change.
- **T2 — frontmatter-only.** Every changed line falls at or above F's closing `---`. This is the load-bearing one: it is exactly the re-stamp and version-bump commit.
- **T3 — stamp-line-only.** All changed lines are `Last updated` / `Version:` / `last_reviewed:` / `reconciled_with:` lines. Catches prose-stamp bumps outside frontmatter.
- **T4 — mechanical regeneration.** Commit subject declares regeneration *and* every changed hunk lies inside a `<!-- TOC:START/END -->` or `<!-- CODEMAP:START/END -->` span.

Line ranges come from `--unified=0` hunk headers checked against the frontmatter span of the blob **at that commit** (`git show <sha>:F`), not against today's file. Dates are author dates (`%as`), matching the gate. The walk runs newest-first and stops at the first CONTENT commit.

**Measured effect over full histories of all 39 living docs — 1,090 commits:**

```
CONTENT  1,032   (94.7%)
TOUCH       58   ( 5.3%)
  frontmatter-only      46
  empty-diff under -w    7
  stamp-line-only        5
```

Worked example — `docs/handoffs/README.md`: 28 commits, 9 TOUCH. `git log -1` alone would have dated it off a `reconciled_with` bump. The rule matters most on the high-churn gated docs (ARCHITECTURE 16 TOUCH of 167; PLAYBOOK 5 of 262) and is a no-op on quiet ones (VISION, README: 0 TOUCH).

**Honest limit:** T4 requires a declared regen subject *and* full containment in a marker span, so a regeneration commit with an undeclared subject and no markers scores CONTENT. That biases toward over-reporting staleness — the safe direction, and the residual over-report is small (58 of 1,090 caught; the naive delta and the corrected delta differ on **zero** of the 13 stamped living docs, because in every case the newest commit was itself CONTENT).

---

## 2. The table — every living doc, sorted by delta descending (item 1)

**Living-doc set = 39 files.** Mutable, session-maintained markdown: root canon + `protocols/*.md` + `.claude/` instruction surfaces + `deploy/` + `plugins/` + `docs/handoffs/README.md`. Excluded by class: immutable (ADRs, audits, transcripts, handoff bundles), append-only (JOURNAL, LESSONS, logs), generated (BACKLOG, `.claude/generated/`, `ecosystem/`), plus `templates/` and `tests/fixtures/`.

`delta = last_content_commit − declared`. Positive = content newer than its review.

```
delta_d;gate;path;declared;stamp_surface;last_content_commit;sha;version;commits
53;ungated;protocols/ENVIRONMENT.md;2026-07-06;prose;2026-08-28;aba765276;-;13
28;ungated;protocols/PLAYBOOK.md;2026-08-01;prose;2026-08-29;3a423bf1b;-;262
2;ungated;README.md;2026-08-29;frontmatter;2026-08-31;080295422;1.0;20
2;ungated;protocols/OPERATOR-INTERFACE.md;2026-08-26;prose;2026-08-28;6adac1dc7;-;3
0;GATED;ARCHITECTURE.md;2026-08-29;frontmatter;2026-08-29;e08cdf8ea;-;167
0;GATED;CLAUDE.md;2026-08-29;frontmatter;2026-08-29;6b8d517b6;-;119
0;GATED;CONTRIBUTING.md;2026-08-28;frontmatter;2026-08-28;e4eaee05f;-;50
0;GATED;VISION.md;2026-08-29;frontmatter;2026-08-29;c20d92399;1.1;19
0;GATED;docs/handoffs/README.md;2026-08-28;frontmatter;2026-08-28;e4eaee05f;-;28
0;GATED;protocols/AI_COUNCIL_PROCESS.md;2026-08-29;frontmatter;2026-08-29;99bf123ee;2.2;8
0;GATED;protocols/DEFINITION_OF_DONE.md;2026-08-23;frontmatter;2026-08-23;af570e773;-;8
0;GATED;protocols/ESSENTIALS.md;2026-08-23;frontmatter;2026-08-23;eccdf31cf;-;68
0;GATED;protocols/SESSION_SETUP.md;2026-08-23;frontmatter;2026-08-28;6adac1dc7;-;18
```

13 of 39 living docs carry a declared date. The remaining 26 are listed in §4.

**Two declared-freshness surfaces exist and are not interchangeable.** Frontmatter `last_reviewed` is machine-readable and gated; a prose `> Last updated:` line is neither. **Three of the four stale docs declare only in prose.** `CLAUDE.md` alone carries both (`last_reviewed: 2026-08-29` and `**Last updated:** 2026-08-29`) — they agree today, and nothing enforces that they ever will.

---

## 3. The gated set, named separately (item 3)

Computed by reading `scripts/canonical_docs.py::FRESHNESS_FILES` (6) + `scripts/audit.py:468-469 _HUB_ONLY_FRESHNESS_FILES` (3) — **9 files**, all present.

**(a) gated-and-stale — 0, by the gate's own predicate.** `canonical_freshness_gate.evaluate()` returns 0 FAIL, 0 WARN. The gate is green. **But see the finding below: green is not the same as correct.**

**(b) gated-and-fresh — 9.** All nine, listed above at delta 0.

**(c) ungated-and-stale — 4. This is the class no gate is watching, and it funds HY-1.**

```
protocols/ENVIRONMENT.md          53d stale   prose stamp only    13 commits
protocols/PLAYBOOK.md             28d stale   prose stamp only   262 commits
README.md                          2d stale   frontmatter         20 commits
protocols/OPERATOR-INTERFACE.md    2d stale   prose stamp only     3 commits
```

`README.md` is the sharpest of these. ADR-114 made it the hub's canonical front door on 2026-08-29, and `canonical_docs.py` documents at length why `README` stayed in `CANONICAL_OPTIONAL` rather than `FRESHNESS_FILES` — re-pointing `VISION` would break six of nine fleet members. The consequence is that **the repo's front door is the one canonical living doc with a frontmatter stamp and no gate on it**, and it went stale within two days of being created.

**(d) ungated-and-unstamped — 26.** The largest class; §4.

### The finding: the A2 gate is date-granular, and same-day drift is structurally invisible

`git_last_commit_date` returns `%as` (day precision) and `evaluate()` fails only when `reviewed < git_date`. Content committed *later the same day* as the stamp therefore passes. Walking each gated file back to the commit that set its current `last_reviewed`, then classifying everything after it:

```
gated file                        commits after stamp   of which CONTENT
ARCHITECTURE.md                            1                   1  !!
CLAUDE.md                                  1                   1  !!
protocols/ESSENTIALS.md                    1                   1  !!
protocols/SESSION_SETUP.md                 1                   1  !!
VISION.md                                  0                   0
CONTRIBUTING.md                            0                   0
docs/handoffs/README.md                    0                   0
protocols/AI_COUNCIL_PROCESS.md            0                   0
protocols/DEFINITION_OF_DONE.md            0                   0
```

**4 of 9 gated files carry unreviewed content that landed after the review they claim.** The gate cannot see any of it. The individual commits:

```
ARCHITECTURE.md         e08cdf8ea  docs: re-point the four in-scope doc surfaces at the universalised carrier source
CLAUDE.md               6b8d517b6  docs(claude-md): re-genre to a boot contract — 39,588 B → 23,931 B
protocols/ESSENTIALS.md eccdf31cf  docs(protocols): keep the silent-rule ratchet green -- indicative mood
protocols/SESSION_SETUP 6adac1dc7  docs(governance): 0a Source A — codify B1/B2/B3 ratified 2026-08-28
```

The `CLAUDE.md` case is the proof by construction: the **re-genre that deleted 15,657 bytes — 40% of the file — landed after the stamp asserting the file had been read end-to-end and confirmed accurate.** A2 scored it fresh. So class (a) is 0 by the gate's predicate and **4 by the predicate the gate intends**; the gap is entirely the date-vs-commit-order granularity, and it is worth more to HY-1 than the ungated class, because it is a gate reporting green over drift rather than a gate that is absent.

---

## 4. Living docs carrying no declared freshness at all (item 4) — 26 of 39

An absent stamp is not a fresh one.

```
path;last_content_commit;commits;generated
.claude/commands/save.md;2026-05-16;2;-
.claude/skills/check-against-spec/SKILL.md;2026-06-25;3;-
plugins/tier1-lifecycle/commands/ship.md;2026-07-05;9;-
.claude/agents/artifact-reader.md;2026-07-06;2;-
plugins/tier1-lifecycle/INSTALL.md;2026-07-29;7;-
plugins/tier1-lifecycle/commands/review-closures.md;2026-07-29;5;-
.claude/commands/preflight.md;2026-08-04;1;-
.claude/commands/override.md;2026-08-06;3;-
.claude/methodology-roster.md;2026-08-08;9;gen
deploy/release-v1.3.x-contract.md;2026-08-08;8;-
protocols/AGENT_FRAMEWORK.md;2026-08-23;4;-
protocols/REPO_ONBOARDING.md;2026-08-23;4;-
.claude/commands/handoff-verify.md;2026-08-25;4;-
.claude/commands/lane-boot.md;2026-08-25;6;-
protocols/HANDOFF_BOOT.md;2026-08-25;32;-
.claude/commands/lane-integrate.md;2026-08-26;5;-
.claude/commands/changelog-review.md;2026-08-28;5;-
.claude/commands/handoff.md;2026-08-28;27;-
.claude/rules/git-discipline.md;2026-08-28;6;-
.claude/skills/verify/SKILL.md;2026-08-28;3;-
AGENTS.md;2026-08-29;4;-
deploy/global-instructions-codex.md;2026-08-29;1;-
protocols/FUNNEL_LIFECYCLE.md;2026-08-29;7;-
protocols/HANDOFF_PROCESS.md;2026-08-29;86;-
protocols/README.md;2026-08-29;10;-
protocols/STANDING_RULINGS.md;2026-08-29;54;-
```

Three stand out by churn against absent stamp: **`protocols/HANDOFF_PROCESS.md` (86 commits)**, **`protocols/STANDING_RULINGS.md` (54)**, **`protocols/HANDOFF_BOOT.md` (32)**. HANDOFF_PROCESS carries a `Version: 6.3.0` line and is the spec four gated docs declare `reconciled_with` — the spec itself has no review stamp while its dependents are gated on agreement with it. `AGENTS.md` is the ADR-115 portable instruction layer, `@`-imported by the gated `CLAUDE.md`, and unstamped: a session reads it at boot on the strength of the importer's stamp.

---

## 5. Derivation design — `last_reviewed` from git rather than by hand (item 5)

Drafted, not built. HY-1 is the consumer.

### The core substitution

Today `last_reviewed` is a hand-typed date asserting *"re-read end-to-end and confirmed accurate"*. Its failure mode is not that the date is wrong but that **nothing binds the assertion to the artifact reviewed**. Derivation replaces the date with a **commit identity**:

```
reviewed_at: <sha of the commit whose tree the reviewer confirmed>
```

The gate then becomes an ancestry question, not a date comparison:

```
stale(F) := exists a CONTENT commit C touching F such that
            reviewed_at(F) is an ancestor of C
```

This is strictly stronger than A2 and fixes the same-day hole outright: commit order is total, calendar dates are not. All four invisible drifts in §3 become visible. It needs no new bookkeeping — the sha is already in the commit the reviewer makes.

### What it buys, beyond the same-day fix

- **A derived *floor*, always available.** `derived_last_content = date of last CONTENT commit` is computable for every tracked file with zero author cooperation, so the 26 unstamped docs get a machine-visible freshness signal immediately, without anyone hand-stamping 26 files.
- **The TOUCH rule stops re-stamp churn.** 46 of 58 TOUCH commits were frontmatter-only. Under derivation, a stamp bump is not a file edit at all — the review record is the commit — so the re-stamp commit class disappears, and with it the `coherence-nudge`/`canonical_freshness` ping-pong of editing a file to declare you read it.
- **Prose and frontmatter stop diverging.** One machine surface; `> Last updated:` becomes rendered output, not input.

### What it breaks — and these are real

1. **It cannot express "reviewed and found still accurate."** Derivation measures *edits*, and a review that changes nothing leaves no commit. This is the whole A1 calendar backstop, and it is the reason derivation must be **additive**: keep an explicit reviewed-at record, and derive only the *comparison target*. A pure `last_reviewed := last_commit_date` is not a review stamp — it is a mtime, and it would report every file permanently fresh. **This is the single most important constraint on HY-1.**
2. **It silently redefines the promise.** `last_reviewed` today means a human read the whole file. Derived, it means "no unreviewed edits since". A doc can be fully current against git and badly drifted against a new ADR that never touched its bytes — `audit.py:735-738` already states this limit for A2, and derivation does not narrow it.
3. **CONTENT-vs-TOUCH becomes load-bearing and gameable.** Today the rule is an audit convenience; under derivation a misclassification silently marks a doc fresh. T4 keys partly on commit *subject* — author-controlled text. Any shipped classifier should drop subject-matching and rely only on the structural predicates (T1, T2, T3), accepting more false-stale.
4. **Cost moves to every gate run.** A2 today is one `git log -1` per file. Ancestry + CONTENT classification is a history walk with per-commit diffs — 13.8s for 39 files here. That is fine at ship time, not at pre-commit. Given `check_generated_artifact_freshness` already precedents `_tier(TIER_SHIP, ...)`, the derived leg belongs at ship tier with the cheap date compare retained at commit tier.
5. **Shallow clones break it.** Demonstrated above: under the graft this repo's own numbers were wrong for 15 files. A derived gate must refuse rather than pass when `git rev-parse --is-shallow-repository` is true. A date compare degrades quietly on a shallow clone; an ancestry test must not.
6. **The consumer carrier constrains the design.** `canonical_freshness_gate.py` is byte-copied standalone into child repos and already soft-imports `canonical_docs`. Any derived logic must survive as a single file with no hub-local imports, or the next deploy breaks every consumer.

### Which files could not be derived, and why

Against the **true 39 stamped files** (not the refuted 493). Four classes, none derivable:

```
class                              n   why derivation corrupts them
---------------------------------  --  ----------------------------------------------
immutable handoff-bundle copies    21  docs/handoffs/*/02_VISION.md, 02b_ECOSYSTEM_VISION.md.
                                       Their last_reviewed is a SNAPSHOT of the source doc's
                                       stamp at cut time (e.g. 2026-05-09 inside a bundle
                                       committed 2026-05-19). Deriving overwrites the record
                                       of WHICH VISION was cut with the date it was filed —
                                       destroying the only fact the field carries. Also a
                                       CLAUDE.md rule-3 immutable-artifact edit.
template placeholders               3  templates/{ARCHITECTURE,CLAUDE-md,CONTRIBUTING-md}-*.md
                                       carry literal <YYYY-MM-DD> / handoff-process@<version>.
                                       Deriving substitutes a real date and the template stops
                                       being a template.
test fixtures                       4  tests/fixtures/repo-with-structural-checks/*.md, all
                                       pinned 2026-06-02. Fixture determinism: a derived date
                                       moves whenever the fixture is touched for unrelated
                                       reasons, making test_audit.py time-dependent.
immutable audit artifact            1  docs/audits/2026-05-28-universalization-durability-
                                       audit.md — immutable by rule 3.
---------------------------------  --
NOT derivable                      29
derivable (the living set)         10  the 9 gated + README.md
```

**Only 10 of the 39 stamped files are derivation candidates at all** — 26% — and all 10 are already the gated-or-should-be-gated living set. The right reading is that derivation is not a corpus-wide migration; it is a change to how ~10 canonical docs prove freshness, plus a free derived floor for the 26 unstamped living docs. Sizing HY-1 as a 493-file or even 39-file migration would be sizing the wrong thing.

### Recommended shape for HY-1

1. Keep an explicit reviewer record; change its **type** from date to commit sha. Additive — the calendar backstop survives.
2. Make the gate an **ancestry** test over CONTENT commits, not a date compare. Fixes §3's four invisible drifts.
3. Ship the CONTENT classifier with structural predicates only (T1/T2/T3), no subject matching.
4. Run it at **ship tier**; leave the cheap date compare at commit tier.
5. **Fail closed on a shallow clone.**
6. Emit a derived floor for unstamped docs as WARN — that alone lights up all 26 in §4 with no authoring work.
7. Settle the ungated four (§3c) as its own question. `README.md`'s exclusion is a documented fleet-compatibility decision, not an oversight; PLAYBOOK's is a documented deferral. Neither is fixed by derivation, and both are functional questions for the operator (ADR-108 §A) rather than technical ones this design can absorb.

---

## 6. No repair performed (item 6)

No file re-stamped. No commit proposed or made. No index regenerated. No JOURNAL entry. No branch, no push. `git status` clean, HEAD `ec8731a9`. Analysis scripts were written to the session scratchpad, outside the repo.

## End packet

- **Decided per contract defaults, not escalated:** the living-doc set boundary (39 files — immutable/append-only/generated/template/fixture classes excluded by CLAUDE.md §4 file-lifecycle classes); the CONTENT/TOUCH predicates; treating a prose `> Last updated:` line as a declared stamp where no frontmatter exists (without it, PLAYBOOK — the lane's own subject — would have had no declared value to compare).
- **Escalated: nothing.** No curated-baseline touch, no rule-vs-ruling conflict, no fork class without a standing ruling arose.
- **Disclosed deviation:** `git fetch --unshallow origin` was run. It writes only `.git/`, leaves the working tree and HEAD untouched, and was necessary — under the shipped graft the audit's central measurements were wrong. Reported, not treated as licensed; if the operator holds that a read-only lane may not mutate `.git/`, that is a ruling this lane should receive rather than assume.
- **Owed follow-up not in this lane's scope:** the lane brief's substrate sizing (493 files, 42 MB) should be corrected at its source, since the same numbers will size the next lane.