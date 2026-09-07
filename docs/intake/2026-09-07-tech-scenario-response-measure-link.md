---
intake-id: 85
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row T-B; thesis row T-05 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:328`, marked **partial** there
consumed-by:
---

# A scenario and the measure that would test it sit one section apart and unlinked

## Problem / motivation

T-05 reads `tex/5-projektowanie-architektury-krok-po-kroku.tex` in full and extracts the
**six-part scenario anatomy**: bodziec (stimulus) · źródło bodźca (source) · odpowiedź (response) ·
**miara odpowiedzi** (response measure) · plus the two the thesis flags as *important though often
omitted*, środowisko (environment) and artefakt. The reason it gives for the response measure is
the whole point: so that the scenario can be **tested**.

The catalogue marks our side **partial**, and it is precise about where the seam is.
`templates/intake-template.md:27` is `## Scenarios (+1 view)` and asks for prose.
`templates/intake-template.md:41` is `## Acceptance criteria (ex-ante)` and **is** the response
measure under another name — *one section away and unlinked to the scenario it should measure*.
Both line numbers verified in the tree at filing time (2026-09-07). The full anatomy has fired
exactly once here, as a review lens, in a single audit.

The consequence is quiet and is visible in this folder. A scenario can be written with no measure
behind it, and an acceptance criterion can be written with no scenario in front of it, and nothing
notices either. The README already states the intent — *"a requirement with no scenario behind it
is suspect"* — but the mechanism only exists for requirements, not for the pairing. The intake
doc's own genre depends on this pairing holding: acceptance criteria copy **verbatim** into the
epic's UAT, so a criterion that measures nothing in particular becomes a UAT that tests nothing in
particular, three artifacts downstream.

## Scenarios (+1 view)

- As the author of an intake doc, I write a scenario and the template requires me to name, by id,
  the acceptance criterion that measures it. The question *"how would I know this happened?"* is
  asked at the moment I write the scenario, not a section later.
- As the author, I write a scenario I cannot measure. That is now visible to me immediately, and
  the honest outcomes are to sharpen the scenario or to drop it — which is exactly the pushback
  the README already asks for on unsupported requirements.
- As the check at commit time, I refuse an intake doc containing a `## Scenarios` entry that names
  no measure, the same way the index freshness gate refuses a stale Contents block.
- As the technical architect at triage, I read a doc where every scenario points at a criterion,
  so scope is legible without reconstructing the mapping in my head.
- As the epic that inherits these criteria verbatim, each of my UAT lines traces back to a
  concrete walkthrough rather than to a section heading.

## Functional requirements

- **Must:** `templates/intake-template.md` gives acceptance criteria **stable ids** and requires
  each `## Scenarios` entry to name the criterion id(s) that measure it. The id shape follows the
  structured-marker convention already used elsewhere in this repo (`AC-1`, `SEQ-2`).
- **Must:** a check refuses an intake doc with a scenario that names no measure. Refusal, not WARN
  — a WARN on a template field is the "stated, not enforced" shape this batch keeps finding.
- **Must:** the check is a ratchet, not a retroactive gate. Every intake doc already in the folder
  was written before the rule; none is refused, and the migration posture is stated
  where the check lives rather than left to be discovered.
- **Must:** the template comment says *why* — the measure exists so the scenario can be tested —
  because a required field whose purpose is unstated becomes ceremony within a month.
- **Should:** the reverse direction is at least visible: a criterion measuring no scenario is
  reported, even if not refused, so the pairing can be read in both directions.
- **Could:** the remaining flagged parts of the six-part anatomy (environment, artifact) become
  optional named sub-fields on a scenario. The thesis calls them *often omitted*; making them
  nameable is cheaper than making them required.

## Acceptance criteria (ex-ante)

- **AC-1:** A new intake doc with a scenario and no measure reference is REFUSED at pre-commit;
  the same doc with a valid `AC-n` reference passes. The pair is the trip test.
- **AC-2:** A scenario referencing an id that does not exist in that doc's `## Acceptance criteria`
  section is REFUSED, with the unresolved id quoted — an unresolvable pointer is worse than none.
- **AC-3:** All intake docs present in `docs/intake/` before this lands still pass, proven by
  running the check over the folder at the pre-change SHA.
- **AC-4:** `templates/intake-template.md` carries the id convention and the one-line reason, and
  a doc generated from the template with the fields left as placeholders is refused rather than
  passing on empty scaffolding.
- **AC-5:** The check's honest limit is recorded where it lives: it verifies that a scenario names
  a measure that exists, never that the measure actually measures the scenario. That judgment
  stays with the reader.

## Non-goals

- **Not** adopting the full six-part anatomy as required structure. Stimulus, source, environment
  and artifact stay prose; only the response measure gains a link, because only the response
  measure already exists here under another name.
- **Not** a rewrite of the 66 existing intake docs. Ratchet forward.
- **Not** a change to the acceptance-criteria → UAT verbatim rule, which is ADR-98's seam and is
  working.
- **Not** a new status, a new frontmatter key, or a change to the lifecycle enum.
- **Not** an extension to ADRs, audits or handoffs. The scenario/measure pairing is an intake-genre
  property; other genres are a separate question.

## Impact sketch (4+1 lite)

- **Logical:** the scenario and its measure become one linked unit rather than two adjacent
  sections; the thesis's testability requirement gets a carrier.
- **Process:** intake authoring gains one reference per scenario — the cheapest point at which the
  "how would I know?" question can be asked.
- **Development:** `templates/intake-template.md`, a new check, and a `.pre-commit-config.yaml`
  entry beside the existing `intake-index-freshness` hook, which already fires on
  `^docs/intake/.*\.md$`.
- **Physical:** untouched.

## Open questions

- Does the check live as its own hook, or as a rule inside an existing intake validator? A second
  hook firing on the same file glob has a cost the roster already feels.
- Is the id convention `AC-n` per document, or does it need to be globally unique so an epic's UAT
  can cite it after the verbatim copy? The copy is verbatim today, which argues for document-local
  ids and a document reference alongside.
- What is the ratchet's boundary — file mtime, git add-date, or an explicit grandfathered list?
  Every prior ratchet here answered this differently, and the answer determines whether an edit to
  an old doc drags it into scope.
- Should this template change also reach `docs/intake/README.md` §2's section list, and if so, is
  that a doc edit that trips the freshness stamp on a canonical file?

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
