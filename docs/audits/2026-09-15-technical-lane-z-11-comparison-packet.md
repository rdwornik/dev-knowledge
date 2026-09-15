# lane-z-11-three-repo-comparison — end-of-lane packet

> **What changed · proposed diffs · open items.** Step 4 of
> `lane-z-11-three-repo-comparison`, and the last act of the lane. Commit-and-STOP: nothing
> was merged into `main`, nothing was pushed to `main`, no index was regenerated, no JOURNAL
> entry was written.
>
> **Which part do you want first.** The **integrator** wants PART 1 (four commits, what is
> in each) and PART 5 (what is owed at the merge). The **operator** ratifying wants PART 3
> (four intakes, graded) and PART 4 (the seven refusals). A seat asking *what did this lane
> actually find* wants PART 0.

---

## PART 0 — The finding, in one paragraph

The lane was asked to compare three public repos against this methodology, and the most
useful thing it produced is not an import. Pointing our own `preflight_contract.py` at our
own corpus surfaced **one** live broken locator in 127 files —
`protocols/STANDING_RULINGS.md:4074`, citing line 96 of a 77-line template — and that one
turned out not to be a stale number at all. The ruling it sits in, **AG-1**, describes a
defect (a literal `v5` era string hardcoded in the handoff probe template) that has since
been **fixed**: the template now reads `v7.1` and the single probe P8 was split into P8a/P8b
at lines 69–70. The citation rotted *because the thing it described was remediated and the
ruling was never updated*. A living rulings document is carrying a ruling about a defect
that no longer exists, pointing at a line that no longer exists. That is a better argument
for corpus-wide locator checking than any count, and it is the shape of finding this lane
was for.

The second finding was produced by accident, and is the one this lane rates highest:
**`preflight_contract.py` cannot tell "I could not look" from "I looked and it is wrong"**
when the object store is incomplete. In this session's shallow clone it rendered 3,774 false
refusals out of 3,894 SHA citations. The module already owns that exact distinction — it
keeps exit 2 apart from exit 1 for precisely this reason — and simply does not extend it to
a shallow clone, which is what every cloud lane runs on.

---

## PART 1 — What changed

Four commits on `claude/lane-z-11-three-repo-comparison`, branched fresh off `origin/main`
at `b5270d6`.

```
eae6e58  docs(z-11)  the three comparison repos and the axis each is admitted on
87b3670  docs(z-11)  the gap matrix -- 15 rows, each resolved to a surface here
1a57a77  docs(z-11)  both lists -- four filed candidates, seven refusals with reasons
<this>   docs(z-11)  end-of-lane packet
```

Eight files added, none modified, none deleted. **No existing file was touched** — the lane
was declared read-only over the corpus and stayed that way.

```
docs/audits/2026-09-15-technical-lane-z-11-comparison-slots.md          126 +
docs/audits/2026-09-15-technical-lane-z-11-comparison-matrix.md         139 +
docs/audits/2026-09-15-technical-lane-z-11-comparison-dispositions.md   194 +
docs/audits/2026-09-15-technical-lane-z-11-comparison-packet.md        (this)
docs/intake/2026-09-15-tech-preflight-cannot-evaluate-verdict.md         97 +
docs/intake/2026-09-15-tech-corpus-wide-locator-resolution.md           111 +
docs/intake/2026-09-15-tech-command-declares-the-module-it-runs.md      122 +
docs/intake/2026-09-15-tech-provider-agreement-over-behaviour.md        116 +
```

---

## PART 2 — Receipt

```
git-source-resolves-non-empty:  https://github.com/rdwornik/dev-knowledge
first-assistant-text-echoed:    "## RECEIPT  **Total line count of the brief: 82 lines.**
                                 **Final line, verbatim:**
                                 `- No edits outside this lane's declared footprint.`
                                 Not truncated. Proceeding to execute."
```

Branch base: `origin/main` @ `b5270d6`, fetched fresh (the session's initial checkout was a
detached HEAD; the lane branched off `origin/main`, per the receipt gate's Q4 clause).

**Substrate disclosure — this matters for one measurement.** The cloud checkout is a
**shallow clone**: `.git/shallow` present, 275 commits. This is what made the `sha` leg
unusable and what produced finding `#95`. Recorded here because a later reader re-running
the measurement in a full clone will get different numbers and should know why.

---

## PART 3 — Filed candidates (LIST A)

Four intakes, filed via ADR-111's only route — CANDIDATE → intake (ADR-98) → ratification.
**Ratification is the operator's act, so this lane filed no `tasks/` rows and closed
nothing.** Next free intake-id was 95, verified against all intake frontmatter including
the archive.

|Intake|Subject|Size|Grade|
|---|---|---|---|
|`#95`|A locator predicate that cannot look must say so|small|**strongest** — a defect, in our own organ, in our own substrate|
|`#97`|A command file does not declare the module it runs|small–medium|strong — unblocks ADR-119 and the `[#664]` census|
|`#96`|Nothing checks our living docs' own locators|small|honest-but-thin — yield is 1 in 127, filed at that strength|
|`#98`|Provider agreement is over strings, never behaviour|**large**|real, but gated on a functional question|

`#98` carries a question only the operator can answer (ADR-108 §A): **how many providers
does this fleet actually take seriously?** The item's size is entirely downstream of it.

## PART 4 — Refusals (LIST B), in one line each

Mandatory list, so a later reader cannot re-litigate a rejection as an oversight. Full
reasons in the dispositions file.

```
R-1  consumer-init CLI (spec-kit)      STRUCTURAL  Layer 2 never executes (ADR-28/36)
R-2  corpus i18n (BMAD)                ECONOMIC    one operator, English specified
R-3  tasks -> issue tracker (spec-kit) STRUCTURAL  a second authority over row state
R-4  10-rule skill validator (BMAD)    ECONOMIC    two skills; revisit trigger named
R-5  agent-persona roles (BMAD)        STRUCTURAL  would be a THIRD role vocabulary
R-6  blanket TDD mandate (superpowers) STRUCTURAL  Council rejected Mandatory TDD
R-7  second docs site (BMAD)           ECONOMIC    intake #9 already holds the direction
```

Two are worth the integrator's eye because they are the kind that get quietly re-proposed:

- **R-1 and R-6 cannot be bought with better tooling.** An installer and the Layer-2
  invariant cannot both hold; a blanket-TDD skill would reverse a Council ruling by import.
  Where either is genuinely wanted, the route is a new ADR, not an adoption.
- **R-4 is the only refusal with a named revisit trigger** — when the hub's skill corpus
  exceeds its command roster, or when a consumer begins authoring skills.

Three further rows (G-5 `analyze`, G-6 `clarify`, G-9 aggregated quality entry point) were
judged real and **deferred, explicitly not refused**, so List B stays honest about what it
contains.

---

## PART 5 — Proposed diffs, and what is owed at the merge

### Owed at the merge (the integrator's act, not this lane's)

1. **Regenerate `docs/intake/README.md`.** Its generated Contents block does not list
   intakes `#95`–`#98`, and the count in it is four low. This is the lane's **declared
   single-hook bypass** (`intake-index-freshness`), stated in the Step-3 commit body;
   the integrator is gate-of-record and regenerates once at the merge (Q1).
   ```
   uv run --locked python scripts/gen_intake_index.py --write
   ```
2. **Run the full suite once, at integration** ([#528]) — this lane ran none (PART 6).
3. **Consider `docs/audits/README.md`** (`audit-index-freshness`) — four new indexed audits.
4. **JOURNAL anchor** — no JOURNAL entry was written by this lane (P-1); the `block-unanchored-push`
   pre-push hook fails CLOSED on a push to `main` whose range carries no anchor.

### Proposed diff — the one measured defect, NOT applied

`protocols/STANDING_RULINGS.md:4074` cites `templates/handoff/v5/PROBES.md.tmpl:96`; the
file is 77 lines. **This lane deliberately did not fix it**, for two reasons: it is a
living-doc edit outside the declared footprint, and — more importantly — **the right remedy
is a judgment call this lane has no standing to make.** The two candidates are not
equivalent:

- **(a) Repoint the locator.** P8 is now P8a/P8b at lines 69–70. Cheapest, and *wrong if (b)
  is true*, because it would preserve a ruling about a fixed defect.
- **(b) Mark AG-1 discharged.** The defect AG-1 describes is gone: `grep -n "v5"` over the
  template returns nothing, and line 14 now reads `the v7.1 cut`. If AG-1's subject no
  longer exists, the ruling is spent and the honest edit records that rather than repairing
  its citation.

This lane's reading is that **(b) is correct** and the evidence above supports it — but
whether a standing ruling is discharged is an architect's call, and the lane records the
evidence instead of taking it. Either way the edit belongs to whoever holds
`STANDING_RULINGS.md`, not to this branch.

### Reproducing the G-1 measurement

The measurement script lived in the session scratchpad and was **not** committed — it is a
throwaway that imports the real organ, and committing it would add an ungoverned surface to
do what intake `#96` proposes doing properly. To re-derive: import
`preflight_contract.verify()`, point it at the living corpus, and discard the `sha` leg
unless the checkout is a full clone. Expect three false-positive classes (closed `[#id]`,
bare prose `name.ext:NN`, shallow-clone SHAs) — all three are characterised in the matrix,
and eliminating them is `#96`'s acceptance criterion 2.

---

## PART 6 — Lane hygiene

```
git stash list                    EMPTY
working tree                      clean
commits                           4, all on claude/lane-z-11-three-repo-comparison
files modified or deleted         0  (8 added, read-only over the corpus)
merged to main                    no
pushed to main                    no
other lanes' branches touched     none
JOURNAL entry                     none (P-1 -- integrator's surface)
indices regenerated               none (Q1 -- declared bypass: intake-index-freshness)
tasks/ rows created or closed     none (ADR-111: ratification is the operator's act)
scratchpad clones                 /tmp scratchpad only; nothing written into the repo tree
```

**No gate was run, and that is the contract, not an omission.** This lane declares substrate
`cloud`; no hook is armed there, and PLAYBOOK Ch8 Layer-1 Q1 routes gate-dependent work away
from cloud precisely because a suite run in a cloud session would report green about a tree
no gate inspected. The full suite runs once, at integration ([#528]).

**Escalations under the V-2 budget: none.** No curated-baseline touch, no rule-vs-ruling
conflict, and no fork class without a standing ruling arose. One premise was checked before
use rather than assumed: the lane confirmed a read path to public repos existed (clone via
the proxy) before selecting any comparison repo, since a cloud session's GitHub access is
scoped to this repository alone. Had that failed, the lane would have PAUSEd under Q10
rather than compare from memory.

---

**Lane:** `lane-z-11-three-repo-comparison` · **Branch:** `claude/lane-z-11-three-repo-comparison`
**Base:** `origin/main` @ `b5270d6` · **Substrate:** cloud · **Date:** 2026-09-15
