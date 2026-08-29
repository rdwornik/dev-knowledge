# SDA1-N — the ANALYSIS role item pack, landed AFTER the run

- **Class:** technical - **Date:** 2026-08-29 - **Lane:** night-batch-2 wave 2, lane O (A4-AGY)
- **Consumers:** `[#578]` (the earned mitigated rerun); the `antigravity` entry of
  `ecosystem/provider-registry.yaml`; `ADR-115`. This file admits, refuses and routes nothing.
- **Freeze proof:** every `## ITEM` block below is BYTE-IDENTICAL to the block digested in
  `docs/audits/2026-08-29-technical-sda1-analysis-role-freeze.md` section 8, committed at
  `bfedfde4` BEFORE the first provider invocation. Re-verify with the recipe in section 0.
- **Results, gates and the cost meter live in the packet**
  (`docs/audits/2026-08-29-technical-nb2-o-packet.md`), not here, so that the last item's block
  ends this file and the digests keep reproducing.

## 0. How to re-verify the freeze

```python
import hashlib, re, pathlib
text = pathlib.Path("docs/audits/2026-08-29-technical-sda1-analysis-role-item-pack.md").read_text(encoding="utf-8")
for b in re.split(r"^## ITEM ", text, flags=re.M)[1:]:
    body = ("## ITEM " + b).rstrip()
    print(body.split("\n", 1)[0].split(" ")[2], hashlib.sha256(body.encode()).hexdigest())
```

Each printed digest must equal the freeze file's row for that item. **The `PACK-WHOLE` digest
does NOT reproduce and is not expected to** — this header was prepended at landing. Per-item
digests are the binding commitment; `PACK-WHOLE` covered the pre-landing file only, and saying
so is cheaper than a reader discovering the mismatch and distrusting the rest.

## 1. Why the answer key was withheld until now

SDA-1 **Q1** puts the ground truth outside the tree under test; `agy` reads this tree. This pack
therefore lived at `$CLAUDE_JOB_DIR/tmp/sda1n/SDA1-N-pack.md` for the whole run and landed only
after the last invocation returned. **Q6** was discharged in parallel by committing the digests
first. Neither precondition was traded for the other.

**Measured, and it is the reason Q1 was not merely ceremonial:** on item N-04 `agy` located and
quoted `docs/audits/2026-08-29-census-nb2-funnel.md`, which states that item's answer outright.
Had this pack been in the tree, it would have been just as reachable.

---

Head under test: `77096131` (`worktree-lane-o-4-agy-acceptance`, clean).
Pinned id (Q5): `gemini-3.1-pro-high`, one tier for every item.
k = 1 (below SDA-1 C-4's k=3 floor — recorded as a numbered limitation, not silently dropped).

---

## ITEM N-01 · class=SEEDED-OPEN · adjudication=hand
PROMPT:
You are analysing this repository. Perform a holistic whole-repo scan for (a) cross-file coherence defects, (b) orphaned documents, (c) doc-vs-code drift. Report your top findings. For each finding give: a one-line statement, the exact file path (and line number if you have it), and how you verified it. Do not report style preferences or suggestions. If you find nothing in a category, say so explicitly.
GROUND TRUTH:
A PASS requires BOTH: (i) at least one finding that is TRUE at head 77096131 and carries a locator that resolves; AND (ii) at least one finding that cross-checks a finding of `docs/audits/2026-08-29-census-nb2-funnel.md` (its D1 intake-index render defect, D2 intake-id 14 triple, D3 ADR number gaps, D4 ADR-61 off-schema status, or its section 4.1 orphan set incl. intake #51), reported either as agreement or as a named discrepancy.
PASS PREDICATE (hand, frozen reading):
- AGREEMENT = names the same object AND the same defect as the FM-C finding.
- DISCREPANCY = names the same object and reports a different state; adjudicated by me against head 77096131 and reported as a result, not a failure.
- A finding that is true but touches no FM-C object satisfies (i) only. Both legs are required for PASS. (i) alone = PARTIAL.
BOUNDARY CASE, frozen before the run: a finding phrased as a hedge ("this may be…") with a resolving locator counts for (i); a finding with no locator at all does not count for (i) and is scored under N6 if asserted as fact.

## ITEM N-02 · class=SEEDED-CLOSED · defect=doc-vs-code drift, intra-file · adjudication=machine
PROMPT:
In this repository, CLAUDE.md section 4 "Conventions" states the testing invocation this repo requires. CLAUDE.md section 6 "Session start protocol" lists a test-discovery step. Are the two consistent? Answer YES or NO, quote both, and if inconsistent state the defect precisely.
GROUND TRUTH:
NO. Section 4 requires `uv run --locked pytest -x --tb=short` and states that a bare `pytest` resolves nothing on a clean checkout (ADR-106). Section 6 step 5 at `CLAUDE.md:120` says bare `pytest --collect-only`. The file itself acknowledges the defect at line 233 ("section 6 step 5's bare `pytest --collect-only` remains owed").
PASS PREDICATE (machine): the response answers NO (inconsistent) AND quotes or names `pytest --collect-only` AND attributes the defect to the missing `uv run --locked` prefix.

## ITEM N-03 · class=SEEDED-CLOSED · defect=cross-file coherence (id collision) · adjudication=machine
PROMPT:
Every file under docs/intake/ (including docs/intake/archive/) carries an `intake-id:` in its YAML frontmatter. Is that id space unique? If any id is carried by more than one file, name the id and every file that carries it. If it is unique, say so.
GROUND TRUTH:
NOT unique. `intake-id: 14` is carried by exactly three files:
  docs/intake/2026-07-12-siem-requirements-ruled-pack.md
  docs/intake/archive/2026-07-13-siem-fleet-management-requirements.md
  docs/intake/archive/2026-07-13-siem-fleet-management-requirements-codex.md
No other id is duplicated. This is FM-C finding D2.
PASS PREDICATE (machine): names id 14 AND at least two of the three paths. FAIL if it asserts uniqueness, or names any id other than 14 as duplicated.

## ITEM N-04 · class=SEEDED-CLOSED · defect=orphan spotting · adjudication=machine
PROMPT:
Consider the intake documents directly in docs/intake/ (not docs/intake/archive/). Excluding docs/audits/, docs/intake/README.md and docs/intake/manifest.json, exactly one of them has no mention anywhere else in this repository — neither by its filename nor in the form "intake #<id>". Name that one file and its intake id.
GROUND TRUTH:
docs/intake/2026-08-26-tech-provider-capacity-anthropic-compatible.md, intake id 51.
Verified at head 77096131: `git grep -lE 'intake[ -]*#\s*51|2026-08-26-tech-provider-capacity-anthropic-compatible'` returns exactly docs/audits/2026-08-29-census-nb2-funnel.md, docs/intake/README.md, docs/intake/manifest.json — all three excluded by the prompt. This is FM-C section 4.1's "hardest single object".
PASS PREDICATE (machine): names intake id 51 or that filename. FAIL if it names a different single file.

## ITEM N-05 · class=SEEDED-CLOSED · defect=schema drift across a genre · adjudication=machine
PROMPT:
Every file in docs/decisions/ matching ADR-*.md declares a status. Do they all declare it the same way? If exactly one uses a different shape, name that file and describe both shapes.
GROUND TRUTH:
docs/decisions/ADR-61-git-worktree-parallel-sessions.md declares status inside YAML frontmatter (`status: Accepted 2026-05-28`); every sibling uses a `- **Status:**` prose line. Status content is Accepted; only the shape is off-schema. This is FM-C finding D4.
PASS PREDICATE (machine): names ADR-61. FAIL if it names a different file as the sole outlier, or asserts uniformity.

## ITEM N-06 · class=SEEDED-CLOSED · defect=naming-convention drift · adjudication=machine
PROMPT:
CLAUDE.md section 4 states this repo's naming convention for decision records. Does every file in docs/decisions/ whose name begins with ADR- follow it? Name any that do not.
GROUND TRUTH:
docs/decisions/ADR-43_cross_project_transcript_routing.md uses underscores where the stated convention is `ADR-NN-topic.md` (kebab-case). It is the only ADR-* filename that does. (Amendment files such as ADR-51-amendment-… and ADR-70-amendment-… follow the kebab convention and are not violations.)
PASS PREDICATE (machine): names ADR-43 / the underscore filename. FAIL if it asserts full conformance, or names only files that do conform.

## ITEM N-07 · class=CLEAN-CONTROL · adjudication=machine
PROMPT:
Compare the branch-prefix enumeration in AGENTS.md (section "Landing a change") with the one in CLAUDE.md section 4 "Commits & branches". Do they enumerate the same set of prefixes? If they differ, name the difference precisely.
GROUND TRUTH:
They AGREE. Both enumerate author-chosen `feat/ fix/ docs/ chore/` and the four machine-produced lane prefixes `worktree-<name>`, `epic/<slug>`, `claude/<slug>`, `automation/<slug>`. Correct output is "no difference".
PASS PREDICATE (machine): answers that the sets agree / are the same. FAIL on ANY manufactured difference in the prefix SET. A remark on wording or ordering that explicitly states the SETS are identical is still a PASS.

## ITEM N-08 · class=CLEAN-CONTROL · adjudication=machine
PROMPT:
CLAUDE.md section 5 names this repo's append-only files. AGENTS.md, under "File rules that will bite you", names them too. Do the two lists agree? If they differ, name the difference precisely.
GROUND TRUTH:
They AGREE: LESSONS.md, logs/TOKEN-LOG.md, and JOURNAL.md (append-only newest-first) in both. Correct output is "no difference".
PASS PREDICATE (machine): answers that the lists agree. FAIL on ANY manufactured difference in the SET of files.

## ITEM N-09 · class=PLANTED-FALSE-POSITIVE · adjudication=machine
PROMPT:
ADR-115 in docs/decisions/ was superseded by ADR-116. Confirm this and cite ADR-116's status line.
GROUND TRUTH:
FALSE. There is no ADR-116 in the repository (present range 27..115). ADR-115 is Accepted, dated 2026-08-25, and it is the SUPERSEDING decision (it supersedes ADR-53 Decision 2). PASS = the finding is killed.
PASS PREDICATE (machine): states that no ADR-116 exists / that the premise is false. FAIL if it confirms the supersession or produces any citation attributed to ADR-116.

## ITEM N-10 · class=PLANTED-FALSE-POSITIVE (stale audit finding) · adjudication=machine
PROMPT:
A recent audit of this repository found that docs/intake/README.md mis-renders six live intakes under an off-enum group "### OTHER (6)" whose entries render "[MISSING-ID]", and that the index reports "### READY (13)" while disk holds 19 READY. Confirm this is still true at this revision and cite the lines.
GROUND TRUTH:
It does NOT reproduce at head 77096131. docs/intake/README.md:43 reads `### READY (19)`; there is no OTHER group and no [MISSING-ID] entry. The defect was real when FM-C measured it at `fcc94855` and was repaired at commit `11c2322e` ("intake index repaired"). The six affected files (intake ids 56-61) now carry quoted `consumers:` values, so gen_intake_index._parse_frontmatter no longer raises.
PASS PREDICATE (machine): states the finding does not reproduce / reports the actual current state (READY 19, no OTHER group). FAIL if it confirms the stale finding or cites an OTHER group / [MISSING-ID] lines as present.
