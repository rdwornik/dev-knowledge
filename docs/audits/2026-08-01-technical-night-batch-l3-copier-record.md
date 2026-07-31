# Night batch 2026-08-01 — L3: copier/cruft record check (intake #22 §D)

**Status: PROPOSAL — verdict recommendation for morning architect ruling. Nothing filed, nothing ruled.**

**Done-contract: MET.** Every quote the ruling depends on is reproduced here with its citation; the
architect should not need to open the repo. Full dossier with the complete quote set:
`<scratchpad>/L3/copier-cruft-dossier.md` (kept out of the repo). `git status --porcelain` empty at
lane close.

**The question:** intake #22 §D (status SEED, explicitly NOT ratified by ADR-108) lists copier/cruft
as an unfiled research sibling serving §E's "change X for all repos at once" requirement. A standing,
evidence-based **rejection** of template engines already exists. **RE-OPEN via a §D row, or
REJECTION STANDS?**

---

## Leg 1 — the record, verbatim

### The rejection

`docs/audits/2026-07-21-technical-night-vision-audit.md`, H4 — evidence at **:154–189**, verdict
restated at **:300–303**. The verdict sentence (`:178–183`):

> *"adopting Copier/cruft as the engine would be trading a working system for a templating model
> that does not fit organs with firing acceptance."*

The audit's own **falsification bar** (`:185–189`, corrected — the input dossier's citation to
185–188 dropped the sentence's final clause): a pilot `copier update` on one consumer across **3
hub template revisions** with real `.methodology.yaml` divergences, counting conflicts and silent
mis-merges, recording either outcome as an ADR.

### "Do not relitigate" — three independent restatements, not two

Chronological (the input dossier named two; a third, *earlier* one was found):

1. **2026-07-03** — `docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md:75–76`. An
   earlier and **separate** rejection, of "copier-LITERAL": *"rejected (templating doesn't fit organs
   with firing acceptance; the carriers are proven). Adopt the copier MODEL
   (deletion-propagation), not the tool."*
2. **2026-07-21** — `docs/handoffs/2026-07-21-dev-knowledge-architect/SUPPLEMENT.md:82–84`, under an
   explicit `CONSIDERED + REJECTED (do not relitigate)` heading.
3. **2026-07-23** — `docs/handoffs/2026-07-23-dev-knowledge-architect/SUPPLEMENT.md:97–98` (heading
   at :95; the input dossier's line range was off by 2).

A fourth reaffirmation, three days before now: `docs/intake/2026-07-28-north-star-delta-review.md:97`
— *"the doc's own Copier precedent is **settled**."*

### The MODEL is already adopted — categorically distinct from the tool

`docs/decisions/ADR-96-deploy-remove-leg.md:22,45` ratifies the copier **deletion-propagation model**;
it is live in shipped code at `deploy/contract.py:128` and `deploy/carrier_precommit.py:924–925`.
Adopting the model is not a step toward adopting the tool — the record deliberately separates them.

### [#387] is open precisely to prevent re-import

`BACKLOG.md:253` (drifted from the input dossier's `:249`). [#387] is open and unblocked, filed to
stop the stale pro-template-engine intake #2 re-entering live work via [#371].

**Citation-drift root cause, traced not merely flagged:**
`docs/intake/2026-07-21-func-fleet-north-star.md` gained a 6-line NOTE block, shifting three cited
lines (59→65, 69→75, 119→125). Worth knowing: several §D-adjacent citations in circulation are
consistently 6 lines stale for this reason.

---

## Leg 2 — the 2026-07-31 evidence, diffed against that reasoning

Each external claim below was verified against the primary source (issue tracker, PR, or CHANGELOG),
not a summary.

### The audit's copier-specific criticism is **factually wrong — and was already wrong when written**

**copier#1833** (inline conflict markers vanish in GUI merge tools) is **CLOSED**, fixed by PR
**#1907**, merged **2025-01-07**, shipped in **copier v9.5.0 (2025-02-17)** — confirmed via the
issue, the PR, and copier's own `CHANGELOG.md`.

The audit was written 2026-07-21. **The fix shipped 17 months earlier.** So this is not a case of
the tool moving since the ruling; it is a sub-claim that was stale at authorship.

### The audit's cruft-specific criticism is **still accurate**

- **cruft#49** (hash bump on unresolved conflict) — **open since 2020**, unchanged.
- **cruft#181** (CI-clone 3-way merge break) — still open, unfixed.
- **renovatebot/renovate#31600** — still open.

### New, decision-relevant, and absent from the original audit

- **cruft has had zero commits since 2024-12-25** — 19+ months — with an open, unanswered
  *"Future of cruft"* issue (**cruft#343**, opened 2026-05-25) asking the maintainers whether they
  will hand it off.
- **copier**, by contrast, shipped **v9.17.0 on 2026-07-13** and has released roughly monthly through
  the present.

So the two tools' trajectories have diverged sharply, and the audit's framing treats them as one class.

### Copier's own docs confirm the operational burden is real and by design

Fetched raw from GitHub: copier recommends a dedicated pre-commit hook specifically to stop unresolved
inline conflict markers being committed. The discipline cost the audit intuited is genuine — it is
just not a *bug*, and it is not the cruft hash-bump failure.

### The four-way diagnostic (kept separate, as the ruling needs them separate)

| | finding |
|---|---|
| **(i) audit evidence wrong** | Yes — on one sub-claim (copier#1833), and **wrong at authorship**, not since. |
| **(ii) right but cruft-specific** | Yes — hash-bump (cruft#49) and CI-merge-break (cruft#181) both still true, both cruft-only, neither transfers to copier. |
| **(iii) tools moved since** | Marginally in the narrow date window — but cruft's **abandonment risk** is newly visible and material. |
| **(iv) verdict right and unchanged** | **Yes.** The load-bearing verdict is architectural fit — "templating doesn't fit organs with firing acceptance" — which is not bug-contingent and is untouched by any of (i)–(iii). |

---

## Leg 3 — verdict recommendation

### Critical context the framing missed

**Intake #22 §E was ratified 2026-07-31 by ADR-109** (`docs/decisions/ADR-109-fleet-desired-state-contract-v1.md`,
Accepted) — *after* the input research dossier was written, so the dossier does not account for it.

ADR-109 transcribes §E's paragraph **verbatim as the functional requirement**, but its own next line
explicitly declines to commit to a mechanism: *"propagation tooling is the chain's tail"* — and it
keeps `deployed-versions.yaml` as the state file, unchanged.

**Ratifying operator language that contains the word "copier" is not ratifying copier as the
technical solution.** ADR-108 §A2, ratified the same day, draws exactly this operator/architect line:
the operator rules functional questions, the architect rules technical ones.

### RECOMMENDATION: **REJECTION STANDS**

Stated as a checkable condition:

> **REJECTION STANDS** — unless the architect wants to spend the audit's own named falsification
> pilot (`copier update` on one real consumer across 3 hub template revisions with real
> `.methodology.yaml` divergences). **That pilot, not a §D backlog row, is the correct re-open gate.**

### The case for RE-OPEN, stated at its strongest (so the architect can rule against me without leaving this page)

The rejection's most concrete piece of evidence — copier's conflict markers vanishing in GUI merge
tools — is **demonstrably false and was false when the audit relied on it**. An evidence-based
rejection that leans on a stale bug report deserves at least one honest re-examination. Copier ships
monthly, has a first-class `update` path with migrations and answer-file semantics, and §E's
fleet-propagation requirement is now *ratified doctrine* rather than an aspiration. If the fleet is
going to need "change X for all repos at once" as a standing capability, buying a maintained tool
beats growing a bespoke one.

### The case for REJECTION STANDS (why I land here)

The verdict never rested on that bug. It rested on **architectural fit** — templating does not model
organs with firing acceptance, and the carriers are proven in production. Correcting the stale
sub-claim strengthens copier-vs-cruft but does not touch the fit argument. Meanwhile the evidence
that *has* moved cuts the other way for the pair as a class: cruft is effectively abandoned. And
[#387] exists specifically to stop a stale pro-template-engine argument re-entering as live — filing
a §D row on the strength of an unratified SEED mention is close to the exact motion [#387] was
written to catch.

### Two explicit answers the architect asked for

**Does §E's fleet-management requirement need copier at all?**
**No.** §E needs the already-kept **per-consumer version-pin scalar**. ADR-109 keeps
`deployed-versions.yaml` as the state file and defers propagation tooling as "the chain's tail." The
requirement is satisfied by the existing carrier + pin mechanism; copier would be a replacement for a
working system, not an addition to a missing one.

**New row, or a note on [#387]?**
**A note on [#387]** — not a new row. [#387] is open, unblocked, and already owns exactly this
concern. A new §D row would duplicate it and would itself be the re-import [#387] exists to prevent.
The note should record two things this lane established: (a) the copier#1833 sub-claim is stale and
should not be cited again, and (b) cruft is effectively unmaintained since 2024-12-25, which is new
information bearing on any future reconsideration.

---

## Method note

Read-only bounded probe. In-repo quotes verified against disk (two citation drifts found and
corrected: the falsify-block range, and the 2026-07-23 restatement offset). External claims verified
against the primary issue/PR/CHANGELOG, each with a URL and date in the full dossier. No repo file
was modified.
