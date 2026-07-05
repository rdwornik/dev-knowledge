# EPIC RETURN — llm-first-docs · (filled by the lane at close)
<!-- scope: meta -->

Required before any merge (HANDOFF_PROCESS §14b). Fill each section; keep the headers.
Closure is claimed on the epic done-contract's **hard metric**, never on "committed".

## 1. Commits + branch state

_One line per commit (sha + subject), oldest first. Branch state: clean tree? Suite green
ON THE BRANCH (paste the suite tail)._

## 2. Contract-vs-outcome per story

_Per story: **met / partial / dropped**, with evidence against its done-when._

## 3. Self-adjudications + ARCHITECT-REVIEW-PENDING

_Every judgment call made inside the lane's discretion, and every item deferred to the root._

## 4. Proposed BACKLOG delta

_Structural changes for the ROOT to apply at integration (new stories, re-scoping,
closures) — the lane never applies these itself (BACKLOG single-writer for structure,
ADR-97)._

## 5. Merge-readiness checklist

- [ ] Diff touches ONLY the declared FILE-BOUNDARY (`git diff --name-only main...HEAD` audited)
- [ ] No merges to main performed from this lane
- [ ] JOURNAL entry on the branch names this lane's session SHAs
- [ ] Working tree clean; suite green on the branch
