---
intake-id: 55
status: READY
origin: read-only cloud census (Dispatch-Cloud, 2026-08-26, `.dev-knowledge` @ 852e145c), relayed to file by the browser architect and landed by lane `g2-consume-recon` at `docs/audits/2026-08-26-technical-handoff-census.md`
consumers: HANDOFF_PROCESS v6.2.0 (deltas D1–D6); `gen_handoff.py` + `assemble_paste.py`; `templates/handoff/v5/PROBES.md.tmpl`; `verify_handoff_probes`; ALL_CHECKS; the browser project instruction
---

# The handoff bundle carries three parts constant to one part judgment — mechanize the constants

## Problem / motivation

A bundle is supposed to **shrink as the mechanisms grow** — `HANDOFF_PROCESS` §2's own design
note says so. Measured across the whole corpus, it has done the opposite for three months while
the mechanisms grew. The note is correct as doctrine and **falsified as description**, and until
this intake nothing had acted on it.

The census measured the gap rather than asserting it (every figure below resolves in the landed
report, which prints the command that produced it):

- **~77% of what the operator pastes is not window-specific**, and one repo file inlined 70 times
  accounts for 1.04 MB of a 3.25 MB paste corpus.
- **`PROBES.md` is 96% invariant window to window** — a fifteen-day diff changed four lines of
  101, and all four were the bundle slug substituted into a path.
- **Nineteen recorded architect-seat errors; nineteen of one class; zero errors of judgment.**
  `LESSONS.md` states the class outright — a fact stated from memory where a command existed that
  would have produced it.

The conclusion the evidence forces is *not* "less browser". The seat's judgment output — rulings,
lane contracts, ADRs — is what everything downstream cites. **The golden mean is the same browser
holding fewer facts.** This intake owns moving the constants out of the paste and the derivations
out of the seat's head, without moving a single value into the bundle.

One case is already a **silent, irreplaceable loss** rather than a projected cost: 62 supplements
were filled, 61 folded into the paste, and the one that was not is the most recent — 87 answer
lines of rulings, rejections and off-repo context that never reached the next seat because no
organ re-folds a supplement filled after assembly.

## Scenarios (+1 view)

- **As an incoming seat**, my role contract is resident in the project instruction at a pinned
  version and sha; the paste carries a 3-line pin, and I refuse to answer if my instructions do
  not carry that version — so residency is *checked*, not assumed.
- **As an incoming seat**, the standing-vs-NEW WARN split arrives **generated** — three lists, no
  verdict, no count, no sha — and the hand region asks me only the one thing a list cannot answer:
  which NEW flag is a decision rather than a defect.
- **As an incoming seat**, the forms card carries the **ruled** dispatch verb, so I do not invent
  a launch procedure from four disagreeing sources.
- **As an outgoing seat**, if I fill the supplement after the paste was assembled, a check FAILs
  rather than letting my window's judgment evaporate.
- **As the operator**, one seat's paste is ~20 KB of mostly window-specific text instead of ~51 KB
  of mostly constant.

## Functional requirements

- **Must:** the standing-WARN attribution arrives as a **generated** block, never a hand-authored
  paragraph — the discriminator is already written down (*attribute a WARN by asking whether the
  arc's diff touched the file it fires against, not by counting*).
- **Must:** `P10` leaves the shipped probe manifest. It asks the seat to classify every open item
  at boot; `HANDOFF_PROCESS` §5 condition 4 rejects exactly this and **names P10 as its origin** —
  and P10 survived the v6 cut that ratified the condition rejecting it.
- **Must:** an audit check FAILs when a supplement carries answers and the assembled paste carries
  no supplement section.
- **Must:** the bundle ships the ruled dispatch verb, and an agreement gate asserts the other
  literal-command sites name that verb and no rival — the register's §V calls this organ *"owed and
  unbuilt"* in its own closing line.
- **Should:** the resident role file and the invariant probe text leave the per-seat paste in
  favour of a version+sha pin plus the variable rows.
- **Should:** the recurring operator-interface facts live in a capability file the forms card
  points at, so the supplement's Q6 means only *changed intent*.
- **Could:** correct `HANDOFF_PROCESS` §13's stale "a v5 bundle carries FOUR files" claim — a probe
  asks the seat this exact question, so the drift is load-bearing rather than cosmetic.

**Attachment by reference — the draft browser role contract.** The census's **Appendix A** is a
one-page role contract (identity · what the seat decides · what it authors · what it must never
carry · what it must never re-explain · how it receives state · how it emits a plan review · its
one standing refusal · its closing duty). It is **not** restated here and it is **not** ratified
here: it is the candidate text a future ADR or register ruling would adopt, and it lives at
`docs/audits/2026-08-26-technical-handoff-census.md` Appendix A. Its "must never carry" list — a
count, a sha, a path, a roster, a status, a line number, a verdict, a branch name, a date relation
— is the same nineteen-error class this intake's mechanisms are designed to remove.

## Acceptance criteria (ex-ante)

1. The next bundle cut measures **≤ 20 KB pasted** at **≥ 70% window-specific** — the minimal-bundle
   shape the census specifies part-by-part at its §3.2 — measured the way the census measured it
   (split the assembled paste on its section labels and account the bytes).
2. `verify_handoff_probes` FAILs a probe row that is unbounded, with the RED-first test landing
   before the row is removed.
3. `supplement_folded` is FAIL-class in `ALL_CHECKS` and is RED against the one live instance,
   green only after regeneration or a **recorded** immutable-and-lost disposition.
4. The generated standing-vs-NEW block carries three lists and **no verdict, count or sha**, and
   the residual-completeness and probe gates stay green with the hand region narrowed.
5. The agreement gate REDs when any of the four literal-command sites names a rival verb.
6. A seat that boots without the pinned role version says so **before** answering anything else.

## Non-goals

- Weakening the answer-free probe contract or its structural enforcement. It is the reason the
  corpus contains no bluffable bundle, and every delta here moves constants out of the paste and
  derivations out of the seat's head — **none moves a value into the bundle**.
- Redesigning the v6 bundle format, the probe gate's teeth (they live at check-time), or the
  browser's judgment remit.
- Deciding the operator-interface contract's **home** — that is intake **#53**'s open question 1,
  and answering it twice is the defect that intake exists to prevent.
- Any routing change. The census's container-uv finding is filed below as a candidate amendment
  and applied nowhere.

## Impact sketch (4+1 lite)

- **Logical:** the bundle splits cleanly into GENERATED / AUTHORED / RESIDENT, and the seat's role
  contract becomes a pinned, refusable artifact.
- **Process:** the outgoing seat's supplement duty gains a mechanism; the incoming seat stops
  re-deriving state it was handed.
- **Development:** `gen_handoff.py`, `assemble_paste.py`, one probe-template deletion, one
  boundedness rung, one new audit check, one agreement gate.
- **Physical:** one browser project instruction becomes load-bearing — the only change that alters
  how the operator sets up a chat, which is why it is the one proposal held for an operator ruling.

## Open questions

1. **Held for the operator, not the architect:** retiring the resident role file from the paste
   changes chat setup. It is the census's own R1 and the only proposal of the nine this lane did
   not birth.
2. Where does the operator-interface capability file live — `protocols/`, a `PLAYBOOK` Ch8
   subsection, or `HANDOFF_PROCESS`? **Two homes is the defect**; this is intake #53's Q1 and is
   answered there, once, for both intakes.
3. The one unfolded supplement is inside an **immutable** committed bundle. Is the discharge a
   regeneration, or a recorded immutable-and-lost disposition? The check must accept both.
4. **Carried from the census's Appendix B, not applied:** `PLAYBOOK` Ch8 Q1 records cloud `uv` as
   *unpinned*. Measured, it is **pinned-but-wrong** (container 0.8.17 against the repo's
   `==0.11.19`) **and provisionable in one step**, which is a different routing fact with a
   different consequence. That is a **candidate amendment to the routing row** — it is recorded
   here and deliberately not applied, since routing is doctrine and Ch8 is a sibling lane's
   surface.

## Status

READY — evidence-complete and landed. Five of the six proposed rows are birthed by lane
`g2-consume-recon` citing this intake; R1 alone is held at open question 1 for an operator ruling.
