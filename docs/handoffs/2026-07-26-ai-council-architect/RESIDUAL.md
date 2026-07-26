# Residual — 2026-07-26-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **CROSS-REPO (ADR-36/41).** The subject is **`ai-council`**; the bundle is hosted in the
> `.dev-knowledge` hub. Every `#id`, path, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The hub is read-only-adjacent here: it hosts, it does not own these tickets.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **The ANSWERS outrank this residual on intent, priority and SEQUENCING — read them before acting on
> §4's ordering.** This residual is repo-derived; the supplement carries what only the outgoing
> architect held. Six load-bearing corrections and additions, so §4 is not silently followed as written:
>
> - **(A) §4's ordering is right but too weak.** The supplement upgrades "hygiene does not preempt
>   items 1–3" into a **testable sequencing rule**: *a window discharges at least one non-delegable
>   item — operator-gated or architect-owed — **before** any CC lane opens.* Testable at close: did it?
>   The diagnosis behind it is sharper than §4's: **all three axis-unblockers are non-delegable**, while
>   **every** backlog defect is CC-executable — so defect-driven ordering fills the window by
>   construction, and once a CC lane is open the architect's attention goes to directing it (which is
>   exactly how `#103` was displaced after being explicitly promised). **Naming this is not a
>   mechanism** — it was named last window and happened again, twice.
> - **(B) A whole item is missing from §4: the unanchored JOURNAL tail is the next session's FIRST
>   act** — a JOURNAL anchor for the window's last three merges. It is **structural, not drift**: an
>   entry cannot name the SHA of the commit containing it, so every session's final commit is
>   unanchorable by construction. Do not file it as a defect.
> - **(C) The mechanism half is capped, deliberately.** `#102`'s ranked queue (with axis items held in
>   its top slots) is the durable version of "axes first" — but **if it threatens to eat the window it
>   drops**. The risk is explicit: it would become the *third consecutive* methodology arc. Open
>   question attached: does the queue **reserve** top slots, or rank purely by priority? A purely
>   priority-ranked queue re-creates the failure, because **every axis item is P3 and the defects are
>   P2**.
> - **(D) Two inherited premises are REFUTED — do not carry them forward.** The previous bundle's
>   "the operator ruled CLI is the default transport" **does not survive the repo** (ADR-12 §5 is
>   unamended; the code requires per-seat opt-in and no seat declares it) — it was **intent, not
>   implemented state**, so `#27` keeps its original meaning as the authorizing gate. And "worktrees are
>   blocked outright" was **wrong as stated**: the real constraint was the system-interpreter editable
>   install, and this target needs no `.worktreeinclude` today. Also corrected: **`#88` has no `#92`
>   binding** in its live ticket text — it is independently schedulable.
> - **(E) §1's "green without its predicate" list gains a third, subtler member.**
>   `canonical_freshness` checks **stamp-vs-commit-date, not content accuracy** — the doc was factually
>   wrong for the whole period and the gate stayed green, *correctly*, because freshness is not
>   accuracy. Reading "freshness gate green" as "the doc is current in substance" is reading a
>   predicate the gate does not compute.
> - **(F) Two hub-side items land on THIS repo, not the target.** The commissioned fleet-methodology
>   intake **exists only as a file and must be placed in the hub's `docs/intake/` or it is lost**; and
>   commission I asks whether two hub handoff-tooling defects were ever filed. **Partially discharged
>   this session:** the probe-tokenizer dotfile blindness **is** filed as hub `[#421]`, and this
>   session found a **second variant** of the same tokenizer defect (a backticked `#id` in a probe's
>   source column is parsed as a markdown anchor) plus **confirmed** the `assemble_paste` partial
>   cold→FILLED reflow — it flipped its own framing sites in this very bundle and left seven
>   hand-authored ones contradicting them, swept by hand. Neither is filed yet.
>
> Also carried by the supplement and worth reading directly: a **do-not-relitigate list** (§3, nine
> items with reasons) and an explicit **architect-seat calibration** — six named browser-seat errors,
> two of which *reproduced the window's own defect class inside the auditing artifacts*. Treat
> browser-seat pointers as claims to verify. **On any number, the probes outrank both this residual and
> the supplement.**

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

**Cross-repo re-frame.** `ai-council` carries **no** `audit.py` ship-gate, **no**
`validate_doc_claims`, **no** `validate_git_backlog`, and **no** disposition register — so there is no
single GREEN/RED headline verdict to report and no dispositioned-WARN concept at all. The drift
surface here is: the **four gating read-only validators** (P7) + `validate_backlog` (P9) + the
report-only **claim-vs-reality checker** (P11/P12), plus **hand intersection** where no organ exists
(P2, P4, P8, P14). **Re-derive each at read-time — the teeth are in `PROBES.md`, not in trusting these
lines.** This bundle states **no** exit code, count, verdict, drifted `#id`, or sha.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**THE HEADLINE IS NOT A DRIFT-FLAG — IT IS THE OPPOSITE, AND THAT IS THE PROBLEM.**

Read this before the backlog, because the backlog cannot show it. A reader arriving at this repo will
find a large batch of closed tickets, a claim-checker reporting cleanly, gates exiting zero, and a
clean tree — and could reasonably conclude the window went to plan. **It did not.** Everything that
landed is **record and quality-control scaffolding**. **All three standing mission axes moved zero.**
That gap is the single most important fact about this window, and a backlog structurally cannot
express it: a backlog shows what closed, never what should have.

**The drift that matters this window is drift the instruments could not see** — five separate
instances of one class:

- **`#125` (NEW, and the sharpest).** The claim-checker's rule 4 is specified as set-equality across
  **four** doc surfaces; its implementation reads **fewer** (P11 re-derives exactly how many and
  which). A genuinely stale canonical surface sat under a clean report for the entire window. **The
  report did not move before or after the repair** — the surface was fixed by hand, and nothing
  automated ever noticed. A defective gate under a green light is *worse* than no gate, because it
  converts "unchecked" into "checked and fine." **The ticket states explicitly that the SPEC must not
  be narrowed to match the code** — the four-surface claim is the requirement; the code is what is
  wrong.
- **`#126` (NEW, sibling).** Several armed validators emit **no output at all**, so their exit zero is
  **silence, not a verdict** (P7 deliberately asks for the stdout-vs-exit-code split for this reason).
- **`#124` (NEW, and it BLOCKS `#123` — recorded in both tickets).** A clean-room install of the
  declared dependency ranges does **not** reproduce a green gate; the primary's gate passes only
  because its interpreter happens to hold versions nothing in the repo pins. `#123` repoints the gate
  at a fresh environment, so **`#123` executed first breaks the green gate on the day it lands, and
  the breakage presents as its own regression.** The order is a correctness constraint, not a
  preference.
- **`#121` (evidence upgraded, not resolved).** A config sweep narrowed three candidate explanations
  for an unattributed checkout to **one with demonstrated write access** — which narrows the
  hypothesis but **does not prove the event**. Recorded as narrowing, deliberately not as a finding.

All four are the same shape, named in `LESSONS.md` 2026-07-26: **a green published without the
predicate that produced it.** Twice it occurred *inside the checker built to catch exactly that*.

**STANDING (not new, and none of them are drift — they are un-started work):** the three mission axes
in §4 items 1–3. They carry no flag because nothing is inconsistent; they simply have not moved.

**Mechanically clean, and that is a real result, not a caveat:** the checker reached its clean state
**with no suppression** — no path allowlisted, no rule silenced; every clean result earned by
repairing the thing or adjudicating it in prose. **P12 re-derives what that clean line actually
covers** — the skipped/total split is the real denominator, and the summary line alone does not
disclose it.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail lives in `JOURNAL.md` entries **2026-07-26 (1)–(7)** — entry **(7)** is the window-close and the
best single read. This is the map only.

- **`#97` claim-checker** — driven to a clean report **without suppression**; the **rule-2 resolution
  model** and **ADR-15** (commit tree, declared bases, self-validating declarations) landed with it.
  Held set corrected in both directions (it had omitted one rule and wrongly held another; **arithmetic
  caught it, no gate did**) — the set-partition now sums.
- **`RepoContext` harness fix** — determinism moved from one rule to **every** leg, including the stubs.
- **`#112` closed** — four dangling commits made reachable via pushed `archive/cited-*` tags,
  replacing an **uncommitted local config value** with real refs (**P15** verifies the replacement
  actually holds).
- **Renumber arc closed** — the two carried hub-id tasks landed in the local id space; every live
  dangling `refs` hub-qualified; one previously-fenced id **freed**. A **third** hub/local collision
  was caught and a different id is now fenced (**P13** — re-derive; the remembered set is wrong).
- **`#106`, `#108`, `#111` closed**; **`#83` discharged** — via its *"or its findings are filed"*
  clause, **not** because the surface came back clean.
- **F2 ruling batch** — nine rulings and four forks converted from chat into repo records; the
  **Unit-2 stubs HELD by architect ruling** (registered, not deleted, so every run keeps printing them
  as not-checked — that is the whole reason registration was insisted on over deletion).
- **`conftest` wrong-tree guard** — RED-proven in a worktree before being trusted.
- **Eleven tickets filed** (`#114`–`#126`); **ARCHITECTURE** reconciled to ADR-15 and re-stamped.
- **Fleet-methodology intake commissioned to the hub `.dev-knowledge`** — this window's fleet-level
  defects assembled into ten commissions (A–J). **The hub owns those rulings; `ai-council` supplies
  evidence.** Do not re-decide them here.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
> **Ordering is stated so it is not re-derived — and it is the outgoing session's explicit ruling, not
> CC's invention.** **Hygiene does not preempt items 1–3.** Record repair, checker work and teardown
> are the **background lane**. They are how this window filled, and that is the mistake not to repeat.
> **The FILLED supplement upgrades this into a testable rule — see correction (A) above: discharge a
> non-delegable item BEFORE opening any CC lane. Read it before following the ordering below.**

**1. Owner-gated — neither is CC's to decide, both have been waiting.**
   - **`#27` CLI parity — not run for the SEVENTH window.** The instrument is ready and was verified
     untouched this window. **Nothing blocks it but the decision to sit down with it.** It shares no
     surface with anything else here, so it is never legitimately "behind" other work — if it slips
     again it should be because it was ruled out, not because it was sequenced out.
   - **The `#117` ADR-11 decision-1 interactivity ruling.** `#117` gave the ruling an *owner*, which is
     not the same as making it. ADR-11's amendment still defers interactivity as *"a separable rider
     requiring its own ADR"*, so **`#113` is unresolvable until someone rules** — and **either
     direction resolves it**. This is a cheap unblock being treated as an expensive one.

**2. Architect-owed — `#103`.** Browser-architect design work, **not CC's to build**; dated
   not-started. Non-cognitive debate (`#55`) is untouched; this is the **sixth window on paper** for
   that axis.

**3. Build lane — the Contract-Version 1.1 arc: `#34` + `#76` + `#100`, versioned TOGETHER, never
   alone.** Untouched this window. The togetherness is the design constraint — the version is the unit,
   and splitting it is what the grouping exists to prevent.

**4. Behind them, in this order** (the order within this item is load-bearing at one point):
   **`#124` → `#123`** — **serial, and a correctness constraint**: `#123` first breaks the green gate
   on the day it lands and the breakage presents as its own regression. Then **`#105`**, then
   **`#119`/`#120`**, then **unit (b) + `#125` + `#118`**.

### The open design questions — resume these, do not rediscover them

- **What is the durable answer to the "green without its predicate" class?** It has now appeared
  **five times in one window**, twice inside the checker built to find it. `#125` and `#126` repair two
  *instances*. **Whether the class gets a durable home — a rule, a report-format contract, a review
  step — is unruled.** This is the highest-leverage open question in the repo, and it is a design
  question, not a build ticket.
- **What is a validator's reporting contract?** `#126` says exit-zero-with-no-output is silence, not a
  verdict. That is a **fleet-shaped** question (it is in the hub commission set) but `ai-council` is
  where it bites. Is the answer a local convention, or does the repo wait on the hub ruling? **Waiting
  is a legitimate answer — but it should be a decision, not a default.**
- **The held Unit-2 stubs: what actually un-holds one?** The ruling is *"revisit when a drift a held
  rule would have caught actually bites, then build that one rule, earned by the incident."* The
  trigger is deliberately incident-driven — **so nothing schedules them, and nothing is supposed to.**
  Confirm that is still intended rather than quietly re-planning them.
- **Rule 4's spec-vs-code direction is already ruled** — the spec stands, the code is wrong. **Do not
  relitigate this into "narrow the spec to match."** It is recorded in the ticket precisely because it
  is the tempting wrong fix.
- **`#121` — an unattributed checkout with one demonstrated-write-access candidate.** Narrowed, not
  proven. Open question: is further pursuit worth it, or is the honest disposition to record the
  narrowing and stop? **Do not conflate it with the separate rejected-tool-call-that-had-already-
  executed finding** — that one is fully attributable from the reflog and is a *different* failure
  shape. Conflating them sends the next session hunting a phantom concurrent writer; the outgoing
  session flagged this explicitly.

### The meta-finding, stated plainly because it is the thing most likely to repeat

**The tooling got better at telling the truth about itself, and the mission did not advance.** Those
are not in tension — the first was necessary. But a window of pure scaffolding is still a window, and
this is the **seventh** for `#27`. The failure mode to guard against is not laziness; it is that
hygiene work is legible, satisfying, and always available, while the mission axes are gated on
decisions that are easy to defer. **If this window's pattern repeats, the ordering above was
decorative.**
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council/BACKLOG.md`**
(themes `[E1]`–`[E7]`, stories `[S…]`), the live in-progress branches (`git branch -v` in the target),
and the drift set re-derived by **P4** / groomed by **P10**. Re-narrating item text splits the truth
and drifts — the pointer + the drift-flag is the whole task-state.

**Read the `BACKLOG.md` grooming log's 2026-07-26 entries before re-deciding anything** — this
window's rulings landed there, including the held-stubs ruling, the `#124`→`#123` blocking direction,
and the next-session queue recorded as a **note** rather than a section.
