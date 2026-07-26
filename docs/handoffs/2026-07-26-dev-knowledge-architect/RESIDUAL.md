# Residual — 2026-07-26-dev-knowledge-architect — the part the repo does not already encode

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

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Read this section as a map of WHICH flags exist and WHY. Every value — verdict, WARN count,
`[stale]` status, drifted id, sha — is withheld by construction; P4/P6/P7/P9 are the answer.**

**Standing (dispositioned before this window, unchanged by it).** Four classes in
`ecosystem/disposition-register.yaml`, none of them new information for the next session:
`no_ff_merges` (legacy pre-invariant commits on main's first-parent spine — history, never to be
rewritten); `undeclared_edges` (the handoff-process references from `BACKLOG.md` / `VISION.md` /
`AI_COUNCIL_PROCESS.md` / `ESSENTIALS.md` / `PLAYBOOK.md` / `SESSION_SETUP.md` — declared-and-parked,
not drift); `doc_rot` on `BACKLOG#278` / `#332` / `#344` (the **accretion** class); and
`reconciled_versions` on `templates/CONTRIBUTING-md-template.md` (a check-precision bug against a
placeholder, not real drift).

**New this window — three entries, and TWO of them are architecturally interesting, not routine.**

1. **`doc_rot` on `BACKLOG#421` + `#422` — filed under a DISTINCT reason class: *oversized single
   filing, explicitly NOT accretion.*** One session, one day, one filing each; the length is precise
   mechanism description, not accumulated dated history. Trim was refused by operator ruling
   (2026-07-26) and other sessions' task text is not rewritten (the A0-seal precedent). **The register
   entries themselves say the fix is the format, not the wording** — they point at intake #17. Treat
   these two rows as evidence in the restructure argument (§4), not as a cleanup chore.
2. **`fleet_parity` on ai-council's root `conftest.py` — an EXTERNAL, IN-FLIGHT condition with no
   action available inside this repo.** A sibling repo's merge turned this repo's gate red mid-close.
   Both candidate fixes (a per-repo manifest declaration in ai-council vs an amendment to the hub's
   consumer-role root template) are real and **neither was chosen by inference** — filed as `[#430]`,
   which carries both halves. This row should clear itself once `[#430]` rules, at which point it
   decorates stale; that is the intended lifecycle, not rot.

**A predicate defect recorded in the register as a comment rather than a seventh ticket.**
`validate_doc_rot`'s backlog accretion predicate counts date **occurrences**, not **distinct days**,
and counts dates appearing inside **path-like tokens** — so a single-day filing that cites a dated
`docs/handoffs/…` path registers as multiple "dated blocks" and trips the ACCRETION leg although
nothing accreted. Both rows above would still WARN on the gross-chars leg, which is the honest
signal. Deliberately left unticketed (six were filed that session and none closed); it is a candidate
fix for whoever re-reviews at the shelf-life date.

**One condition that is NOT a disposition and NOT a gate — do not conflate them.** A single named
test (`tests/test_audit.py::test_check_fleet_parity_green_on_live_repo`) is red on **proven external
provenance** — it calls the check directly and asserts on the raw finding, so the disposition that
legitimately clears the same WARN at the ship-gate is invisible to it. `main` was pushed red by
explicit operator ruling, on evidence, and the record of that exception is deliberate: JOURNAL
2026-07-26 (d) exists so the exception is never mistaken for an oversight. **The gate-vs-test
divergence is itself the finding** — see §4. Re-run to learn whether the sibling has since declared
it; the bundle asserts nothing about its current state.

**Two surfacers are shouting and neither is a drift-check.** The session-start hooks report a
standing pool of unreviewed **closure proposals** (`/review-closures`) and a set of unreviewed
**nightly triage findings** in the Issues tab; the changelog sentinel reports the tool has moved
several patch versions past the last review (`/changelog-review`). None of these gate anything.
That is precisely why they have accumulated — and §4 treats the pattern, not the queue.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the previous architect bundle merged (`docs/handoffs/2026-07-25-dev-knowledge-architect/`).
Detail lives in `JOURNAL.md` 2026-07-26 entries (a)–(e) and `BACKLOG.md`; this is the map only.

- **ADR-105 accepted** — Routine consumer declaration: a six-field row shape, **gated at ACTIVATION,
  not at filing**. Landed with the `[E9]` brake discharged and `[#419]` given teeth.
- **Hygiene + currency (the last merge)** — `ARCHITECTURE.md` brought current through ADR-105; the
  organ map gained a **Status** column (ARMED / RULED-UNBUILT / RETIRED); Ch6's nightly loop marked
  **broken at the triage edge**; the `[#373]`–`[#380]` reserved-id banner released; three merged
  branches deleted.
- **A stranded branch recovered** — intake **#17**
  (`docs/intake/2026-07-25-tech-consolidation-decision.md`, ACCEPTED, three open questions) plus
  `[#421]` and `[#422]`, which had been misfiled onto another session's branch and never reached
  `main`. See JOURNAL (c).
- **Filed, not closed:** `[#423]`, `[#427]`, `[#428]`, `[#429]`, `[#430]`, `[#431]` — plus the two
  recovered above. **Closures this window: none.** That direction is a standing input to §4.
- **`[E8]` decision table dispositioned against live state** — outcome: one DEAD-OBE, three
  already-ruled, four ruled by operator-delegated adoption, **two still open (`R8`, `R12`)**. A ruling
  there is *recorded, never executed* — each adopted row still needs its build.
- **Two review lanes both bit** — the doc lane and the adversarial lane each returned High findings on
  work that had already passed the other, including a **relitigated BINDING ruling**. See §4.
- **The `[E8]` preamble now carries an explicit reconciliation-debt list** (stale `CONTRIBUTING.md`
  prose describing a deleted Action in the present tense; `[#389]`/W3/W4/W6/W7 R-status text now
  stale) — enumerated rather than silently left.

> **Reconciliation against the folded `SUPPLEMENT.md` — the repo wins, per §13's advisory contract.**
> The supplement is carried **verbatim** and is **never trusted over the repo**; one of its claims has
> since been overtaken by live state, and it is flagged here rather than edited there.
>
> - **Its wave-1 `MICRO-WINDOW` is described as *"prompt already delivered, awaiting paste"* — that
>   wave has SHIPPED.** It merged this window (`ARCHITECTURE.md` currency through ADR-105, the organ
>   Status column, the reserved-id release, the `R1`–`R12` liveness sweep, the codex-wrapper filing);
>   see the §2 map above and JOURNAL (e). **Do not re-run it.** The supplement's wave order is
>   otherwise unaffected — the next arc is its wave 2 (uv adoption), then the restructure.
> - **Checked and still accurate:** *"one merged branch awaiting the operator's word to delete"*
>   (`git branch --merged main` shows exactly one straggler). Its §7 instruction to **verify the live
>   conformance-branch set before acting rather than assume the count** is correct and still binding —
>   re-derive it; this bundle deliberately states no count.
>
> Everything else in the supplement is *why*, not state, and stands as written.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### A. The two rulings the operator owns — nothing downstream moves without them

**`R8` — the corp-side `#38` channel pick** (1 primary-direct / 2 worktree / 3 epic-dev). Four
exhaustive searches across BACKLOG / JOURNAL / `docs/` found **no ruling**. It was **explicitly
excluded** from the 2026-07-26 delegation order — the operator's own pick. Do not re-search for it and
do not infer it; ask.

**`R12` — the ARC-5 closure contract is not satisfiable as written, and this is the largest open
architecture question in the repo.** Clause (b) requires that *"everything still unenforced has moved
to declared-unenforced with an owner and a review date."* At **N_silent = 176** that means
dispositioning 176 rules — not achievable in one arc. Two options are on the table: **(i) NARROW** the
target to a bounded load-bearing slice (the four census escalations `[#358]`–`[#361]`, the two
still-silent seed-1 rules `[#356]`, the 49 dropped `#242` guards `[#362]`), or **(ii) GATE THE GROWTH**
of silent rules instead of draining the pool. **No recommendation is attached, deliberately** — there
is nothing to rule by delegation, and narrow-vs-gate is a genuine choice with different downstream
shapes.

> **A third framing the record does not yet contain, offered as an option and not as a
> recommendation:** amend the closure contract itself. It is currently marked *frozen — reproduced
> verbatim*, so amending it is a real decision with its own cost (it is the artifact that stops "waves
> merged, ship-gate green" from counting as closure). Narrowing the target and amending the contract
> are **not** the same move, and the record currently conflates them.

### B. Structural questions this window surfaced — each is a design call, not a bug fix

**B1 — The 1200-char `doc_rot` ceiling stopped being a constraint and became a censor.** The evidence
crossed a threshold this window: three findings **could not be recorded in their own tickets at all**
and were relocated to `LESSONS.md`, and **all three references are one-directional** — the lessons cite
the tickets; the tickets cannot cite back. A ticket that cannot hold the evidence for its own defect is
not a formatting inconvenience. Two register entries now say in their own text that **the fix is the
format, not the wording**. The decision is *what a backlog task record is* — not *what the limit
should be*; intake #17 (`docs/intake/2026-07-25-tech-consolidation-decision.md`, ACCEPTED) is the
vehicle. Its three open questions — **R-G** (which Gemini CLI is the scanning lane), **R-N** (confirm
8 days as the overdue-ruling threshold), **R-S** (confirm the seeded-defect list for the acceptance
test) — are unanswered and cheap to close.

**B2 — A gate and a test can disagree about the same condition, and the divergence is structural.**
The disposition register is a **ship-gate** concept; a test that calls a check directly and asserts on
raw findings cannot see it. So a legitimately-dispositioned WARN stays green at the gate and red in
pytest, forever, by construction. Three shapes are available and none has been chosen: make
direct-check tests disposition-aware; rule that such tests must assert only on *undispositioned*
findings; or accept and document the divergence as a declared property. Until one is picked, every
future disposition can mint a permanently-red test.

**B3 — Should a gate's verdict be allowed to depend on state outside its subject?** `fleet_parity`
reads **live sibling-repo working trees**, so another repo's merge can turn this repo's gate red with
**no action available here** — which is exactly what happened. `[#430]` carries the two local fixes
(declare it in the sibling's manifest vs amend the hub's consumer-role root template) and neither was
chosen by inference. The larger question sits above both: a cross-repo gate that reads *live* trees is
non-deterministic by design; reading **declared/committed** state instead would make it reproducible.
That is an architecture ruling, not a ticket.

**B4 — The ruling corpus has no single searchable home, and that already cost us.** A probe searched
`JOURNAL` / `LESSONS` / `docs/decisions/` and concluded *"no prior ruling exists"* — then the
adversarial lane found the ruling in a **handoff supplement**, marked *"BINDING — do not relitigate."*
A settled decision was relitigated because the surface it lived on was not in the search set. Either
binding rulings get a canonical home (and handoff bundles stop being load-bearing for them), or the
"where do I look" contract has to enumerate `docs/handoffs/` explicitly. **This is a live defect in how
decisions are found, not a process nicety.**

**B5 — An attached recommendation is a poor predictor of the operator's call.** Of the `[E8]` rows that
turned out to already have a ruling, **the attached recommendation lost 3 times out of 3** (R1b
rejected, R2 chose (b) over (a), R4 rejected outright). The methodological consequence is direct:
verify each row against live state, never ratify a table wholesale — and treat a recommendation as a
hypothesis, not a default. Worth codifying rather than leaving as a one-session observation.

**B6 — Detection is healthy; consumption is not.** Filings this window: eight. Closures: **zero**. A
standing pool of closure proposals sits unreviewed, the nightly triage findings sit unconsumed (Ch6 is
now explicitly marked **broken at the triage edge**), and the changelog sentinel has been nagging
across several tool versions. Every one of these surfacers is **non-gating** — which is why they
accumulate. Closure-contract clause (d) requires accretion **net ≤ 0**; the current direction is the
opposite. The question is not "run the queues" but **whether a surfacer with no consumer should exist
at all**, and what makes consumption obligatory without turning every nag into a blocker.

**B7 — A repo cannot fix the defects that live in its own tooling.** `[#431]` (the codex-review wrapper
silently drops the doc lane on mixed diffs) sits behind a **core-invariant #6 global-infra ruling** —
so the repo that suffers the defect is not permitted to repair it unilaterally. That guard is correct
and it is also a bottleneck. Worth deciding whether a narrow standing grant exists for
defect-repair-in-place, or whether every such fix waits on a per-instance ruling.

### C. Small open calls — cheap, and each is genuinely the operator's

- **`ecosystem/registry.md` is missing a `terminal-setup` row** (human-registered 8, should be 9). It
  needs a purpose line and a verified status — not derivable. **Note the correction the last session
  had to make:** `index.yaml` is **derived and regenerated wholesale** (`audit.py` says do not hand-edit
  it), so the originally-asserted "`index.yaml` registration gap" was the wrong target; the
  hand-maintained `registry.md` is the real one.
- **Reconciliation debt, enumerated in the `[E8]` preamble rather than silently left:**
  `CONTRIBUTING.md` still describes a deleted Action in the **present tense**; the R-status text on
  `[#389]` / W3 / W4 / W6 / W7 is now stale.

### D. Dated pressure — the only genuinely time-boxed things here

- **W1's `.vscode` ruling shelf-life: 2026-08-13.** W1 is SEEDLESS — justified by operator priority and
  this deadline, *not* by audit evidence. It is the most visible wave, deliberately.
- **Disposition `review_date`s cluster at 2026-08-26** (the `#421`/`#422`/`fleet_parity` rows). Those
  are shelf-lives, not deadlines — they exist so suppressions cannot rot into paper.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
