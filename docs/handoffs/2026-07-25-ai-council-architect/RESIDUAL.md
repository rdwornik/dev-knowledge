# Residual — 2026-07-25-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The ANSWERS outrank this residual on intent, priority and SEQUENCING — read them before acting on
> §4's ordering.** This residual is repo-derived; the supplement carries what only the outgoing
> architect held. Five load-bearing corrections, so §4 is not silently followed as written:
>
> - **(A) Sequencing is inverted — "Unit 1.5 before Unit 2."** Two filed follow-ups change the
>   **frozen `Finding` harness surface** (one adds a field, one changes the printer). Land them while
>   the blast radius is four legs; at eleven it becomes a retrofit. §4 item 1 (the registry repair) is
>   still correct as the *standalone* first move, but the harness changes come **before** any Unit-2
>   rule building — not after, as §4 item 4 implies.
> - **(B) The dispositioned precision-over-recall High is NOT merely "waiting on the operator"** (as
>   §4 item 8 files it). Its revisit trigger has **already fired early**: the same repo-rooted guard is
>   implicated in three separate failures, making it the **single highest-leverage fix in the checker**.
>   Treat it as a live design item near the top, not queued admin.
> - **(C) A ruling landed this window that §4 does not carry at all** — the operator ruled **CLI is the
>   default transport for debate, API for research mode**. It exists **only in chat**: it belongs in an
>   ADR or at minimum a ticket. It also **reframes the blind-scoring lane** (§4 item 0) from a decision
>   into a **cost control** — measuring what the preference costs in quality, not whether it is
>   preferred — so that lane's done-when needs rewriting. Item 0's *ordering* rule still stands
>   unchanged: operator-only, never sequenced behind anything (it has now slipped **six consecutive
>   windows**).
> - **(D) An open governance question, absent from §4:** a push to `origin/main` this window came from
>   neither CC nor the cloud session. "The operator is the serial merge gate" is **not enforced against
>   a background pusher.**
> - **(E) A hard execution constraint on the next arc:** in this target, **worktrees are blocked
>   outright** — a worktree shares the primary's editable install, so pytest inside one silently tests
>   the primary's source, and the include-file that would fix it does not exist here. Plan the arc as
>   primary-checkout work.
>
> Also carried by the supplement and worth reading directly: a **do-not-relitigate list** (§3) and an
> explicit **architect-seat calibration** — several browser-seat errors this window were all one class
> (asserting conclusions rather than primitives), all caught downstream. Treat browser-seat pointers as
> claims to verify. **On any number, the probes outrank both this residual and the supplement.**

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks **the target actually has** — the four gating `ai-council`
validators (P7) + `validate_backlog` (P9) + the **new** report-only claim-vs-reality checker (P11/P12)
— plus hand intersection where the hub organ has no target equivalent (P2, P4, P14). **Re-derive each
at read-time — the teeth are in `PROBES.md`, not in trusting these lines.** This bundle states **no**
validator verdict, count, drifted `#id`, or sha — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo re-frame:** `ai-council` still carries **no** `audit.py` ship-gate, `validate_doc_claims`,
`validate_git_backlog`, or disposition register. What changed this window: the doc-vs-reality gap the
last two bundles named as *specified-but-not-built* is now **partially built** — `scripts/validate_claims.py`
(`#97` Unit 1) runs read-only and **non-blocking** as a `check.ps1` section. It is a **measurement
surface, not a gate**; a non-zero finding count is the point, not a failure.

**NEW + LOAD-BEARING (the headline): the checker's rule registry is INCOMPLETE, and its own test suite
structurally cannot say so.** `#97` specifies fourteen rules. Some rule ids have **no row in the
registry at all** — not implemented, not stubbed, not disclosed by the checker's KNOWN LIMITATIONS
header — so **no run mentions them and no drift they were commissioned to catch is monitored today**
(**P11** re-derives the exact set difference; the outstanding total is larger than the report implies).
The root cause is the part that generalizes and is the reason this leads the headline: the registry
test is parametrized **over the registry**, so it covers whatever is present and **cannot detect an
omission** — a self-referential completeness test has no denominator. A large new test module went
green while rules were missing. This is the *same shape* as the rule-14 leg-(a) vacuity the last
window fixed (validating a hand-maintained map against itself), recurring one layer up, in the organ
built to catch exactly that class. The repair (register the absent rules + an **external** expected-set
test) is `#97`'s own remaining work and is not done.

**NEW: the checker's finding set self-replicates and is GROWING.** Every JOURNAL entry that discusses
dangling-SHA findings **cites SHAs**, which the rule-8 leg then re-reports — so the count climbs on its
own with each prepend, and the line numbers in each finding shift as the newest-first file grows
(**P12** measures it live). This matters structurally, not cosmetically: a filed task's done-when is a
**zero-findings gate**, and it is blocked by two others precisely because the gate is unpassable while
this loop runs. Treat P12's number as *distance-to-passable*, and note that it moves without anyone
touching the checker.

**NEW: one rule is non-deterministic across checkouts for the identical commit.** A gitignored
directory exists as untracked debris on this primary checkout but is absent from a fresh clone, so the
same rule fires here and is suppressed there. Two honest sessions reported contradictory results and
**both were right**. This undercuts the per-rule clean-window trigger a filed follow-up depends on,
independently of the other two blockers — and that follow-up's blocker list does **not** yet name it.

**STANDING, now RECORDED rather than open (do not re-litigate):** the `ARCHITECTURE.md` Layer-edges
allowed set was ruled this window — marked **TARGET, not current state**, with a dated current-state
note recording `cli.py`'s real edge surface, **set values byte-unchanged** (the ruling deliberately did
not widen the boundary to match the defect: *rewording a boundary to match a defect launders the
defect*). The re-derivation trigger is `#92` landing. So the live question is no longer "what is the
gap" but **"has the trigger fired, and is the dated snapshot still true"** — **P14**. The `cli -> boost`
open case is still unruled and still bound to the `#69`/P2 arc.

**STANDING (fenced, not yet resolved):** the dangling `refs #96` occurrences in the carried hub-id
tasks — hazard contained by the BACKLOG **Id-reservations note**, which was **extended a third time**
this window after another hub/local id collision was caught by the standing grep-before-assign rule
(**P13** re-derives the fence). Reactive reservation per collision is the patch; the checker's
ticket-reference rule is the fix, and it is one of the unbuilt ones.

**STANDING (uncommitted, and therefore invisible to every other organ):** a **local** `gc.auto` setting
is what currently keeps four unreachable commit objects alive — they are past git's default prune
horizon, so age no longer protects them. This is a load-bearing fact that **is not in the repo** and
cannot be carried by any clone, doc, or summary (**P15**). Restoring the setting is part of the filed
task's done-when, so the repo is knowingly carrying silent disabled-maintenance debt until then.

**RESOLVED THIS WINDOW — do not re-flag:** the cloud-run contradiction over a checker finding (resolved
as the checkout-nondeterminism above, not a disagreement); the "missing token log" finding (reconciled
as **stale addressing, not a missing file** — the log is the hub's, as the install doc already states);
a reported protocol-file drift (reconciled as a **checker false positive** — an allowlist keys on a
path prefix *inside* the backticks while the attribution is in prose; folded into an existing follow-up
as a leg, not filed as drift).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-23 handoff. One line each; detail lives in `JOURNAL.md` (entries
2026-07-24/25) + the merge messages. All ids/paths are **ai-council's**. Six first-parent merges.

- `766241a` — **`#27` blind-scoring instrument prepped** (`READING-INDEX.md` + blank `SCORING-RECORD.md`
  inside the existing frozen cli4-parity workspace; rubric inline, 12 pairs in scoring order, sealed key
  verified untracked and never opened). Lane is **READY and waiting on the operator** — not on any build.
- `766241a` (same branch, Lane 1) — **STEP-0 acceptance-freeze reads**: established that the night-batch
  report carries *twelve* rules on disk while the fourteen-rule spec lives only in `BACKLOG.md` `#97`;
  confirmed both late-added rules carry real non-vacuous earned-by traces, with the honest caveat that
  they were earned in their own authoring session and two are partly self-referential.
- `b1f3319` — **FLOOR1 R1 ruling applied** (ARCHITECTURE only): allowed edge set relabelled **TARGET,
  not current state**, `cli.py`'s real surface re-derived **live via AST** (not trusted from the prior
  bundle's probe numbers — the derivation reproduced them exactly), dated current-state note added,
  codemap-completeness gap recorded with a pointer to the map-vs-source rule leg. **Set values
  byte-unchanged**; `cli -> boost` still the one open case.
- `b94e8d1` — **`#97` Unit 1 shipped**: `scripts/validate_claims.py`, a read-only claim-vs-reality
  checker wired as a **non-blocking** `check.ps1` section per the standalone-not-a-gate ruling. Four
  rules implemented RED-first; the remaining registered ones are Unit-2 stubs; the evidence-command rule
  is **structural** (an argv tuple whose shlex round-trip is executed by the harness — verified, not
  promised) rather than a leg. terra returned **5 High / 0 Critical**; four fixed, one dispositioned as
  a deliberate precision-over-recall tradeoff. A KNOWN LIMITATIONS header was added pre-merge so the
  checker does not overclaim about itself.
- `6002aba` — **filing batch**: one 18-item operator window → **12 new ids + 5 rider edits**, every
  claim grep-verified against the live tree before proposing (which changed three of the filings). Task
  count and story count both moved; one id **skipped and newly reserved** on a third hub/local
  collision. `gc.auto` set to `0` repo-locally **before** the branch was cut (mechanism, not prose).
- `1fa0054` — **`#97` reconciled to reality**: the task line now records Unit 1's landing instead of
  reading as unbuilt work, **records the two absent rules**, and amends a done-when whose first clauses
  were already true for the implemented subset. Two gates added to its scope: register all fourteen with
  the one sanctioned structural exemption, and an **external expected-set** registry test.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
Ordered: the standalone correction first, then the design question it raises, then the arc it gates,
then record debt. **One item is deliberately out of the ordering** — see item 0.

**0. `#27` blind scoring is OPERATOR-ONLY and must never be sequenced behind anything.** The instrument
is built and the lane is READY (`766241a`); what remains is the operator reading twelve pairs, then the
unseal and the parity tally. A downstream ticket is gated behind it. It shares no surface with anything
below, so it runs in parallel with every item here — do not let a build arc absorb it. (This ordering
rule was an explicit correction from the last window's supplement; it is repeated because it was
violated once.)

1. **The `#97` registry repair — immediate and standalone.** Register the absent rules, and add the
   **external expected-set** test (an explicit id set asserted against `RULES`, not derived from it).
   This is not blocked on Unit 2 scope, on the checker's gate question, or on anything else; it is a
   correction to something already shipped, and until it lands the checker silently under-reports its
   own coverage. **P11** gives the exact set to repair.
2. **The design question the defect raises — does the "external denominator" rule get a durable home?**
   Twice now the same failure has shipped: a validator checked against its own artifact (the map-vs-map
   leg) and a test parametrized over its own registry. The specific fixes are cheap; the recurring shape
   is the real finding. **Open:** is this a checker rule of its own (self-referential-validation
   detection), a `LESSONS.md` entry, a review-checklist item, or nothing durable? The architect should
   rule — this is exactly the way-of-working question architect mode exists for, and it is currently
   held nowhere but in one JOURNAL paragraph.
3. **Is the zero-findings gate the right shape for the checker follow-up at all?** Its done-when is "0
   findings," and it is already blocked by two other items. Two facts landed this window that the gate's
   design did not anticipate: the finding set **self-replicates** with each JOURNAL prepend (so the
   target moves away from you as you write about it), and one rule is **non-deterministic across
   checkouts for the identical commit**. **Open fork:** (a) keep the zero-findings gate and first fix
   the loop + the nondeterminism, (b) re-shape the gate to a per-rule clean window — which the
   nondeterminism *also* undercuts — or (c) accept a non-zero baseline and gate on *new* findings only.
   Whichever is ruled, the blocker list currently does **not** name the checkout-nondeterminism; that
   omission should be closed in the same edit.
   - **Sub-question worth ruling explicitly:** should JOURNAL entries stop citing bare SHAs for
     dangling-SHA discussions? The last two entries deliberately declined to re-cite them for exactly
     this reason — that is a convention being followed with no written rule behind it.
4. **Checker Unit 2 scope + posture.** The remaining rules (including the AST import-graph leg) build
   against a frozen interface — that part is settled. **Open:** which rules gate versus report; whether
   the checker graduates from a non-blocking `check.ps1` section into a real gate, and if so which
   subset; and whether it becomes the target-side organ that closes the "no automated doc-claim check"
   gap (§1) or stays advisory permanently. Note the standalone-not-a-pre-commit-gate ruling settled the
   *home*, not the *posture*.
5. **The `#92` arc still carries three coupled things — unchanged, and still unruled.** (a) `#92`'s
   `cli.run()` refactor is the named **re-derivation trigger** for the allowed-set snapshot (**P14**
   tells you whether it has fired and whether the dated note still holds); (b) the `cli -> boost` open
   case — reclassify `boost` to orchestration, or admit a *scoped* interface→core edge — rule it with
   the re-derivation, not before; (c) the parity fix carries a **verified constraint**: the divergent
   models-gating expression **is also** what makes the wide panel the effective default, so any fix must
   decouple the two and land a bare-invocation panel-default regression test **first**, or it silently
   flips the default. A strict xfail errors the suite the moment the wiring lands — wiring and parity
   fix are one arc by construction.
6. **The fenced ADR-02 amendment** — scope is (a) overlap policy + (b) stale stamp only. The
   panel-default question inside it is **DISSOLVED and out of scope**; the amendment must not reopen it.
   The checker's config-parity rule carries the guard: adjudicate *effective flag-resolution behaviour*,
   never raw config keys.
7. **Record debt, in dependency order.** The **renumber arc** (both carried hub-id tasks, resolving or
   dropping every `refs #96` occurrence **in the same edit** — the audit's explicit instruction; **P13**
   re-derives the fence, and note the fence grew again this window). Then **restoring `gc.auto`** once
   the dangling objects are dealt with (**P15** — until then the repo carries silent
   disabled-maintenance debt, and the protection is uncommitted). Then the still-**un-triaged** batch
   proposal set, which a BACKLOG-only reader still cannot see item-by-item.
8. **Three done-when texts are still awaiting an operator ruling**, and one of them — the
   **review-runner convention** — is the fresh-architect gap named two windows running: the review-lane
   routing posture (which reviewer lane runs what; one lane withdrawn on cost) lives only in `~/.claude`
   and the JOURNAL, and is **not a repo record**. A ruling here would also absorb it. Separately, the
   dispositioned High from the terra review and the checker's self-negating allowlist residual are both
   waiting on the operator, not on design.
9. **A newly-filed pair encodes a real fork, deliberately as two tickets:** the boost sharpening-
   annotation block and the interactive clarify-loop. The second names **both** exits — built per the
   proposed design, **or** closed as deliberately-not-doing if the ADR-11 decision-1 ruling forecloses
   interactivity — so a ruling either way resolves it rather than leaving a zombie. That ruling is
   architect work and has not been made.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council`'s**
`BACKLOG.md` (themes `[E1]`–`[E7]`; the grooming log carries this window's rulings), the live
in-progress branches (`git branch -v`, run in the **target**), and the drifted-closed intersection
**P4 computes by hand** (§1 — the target has no `validate_git_backlog`). Re-narrating item text splits
the truth and drifts — the pointer + the drift-flag is the whole task-state. The whole-open-set
grooming obligation at boot is **P10**, and its denominator grew materially this window — the filing
batch is the single largest task-count move in the recent record, and several new items are blocked on
each other rather than on work.
