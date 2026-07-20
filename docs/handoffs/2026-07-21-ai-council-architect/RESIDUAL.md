# Residual — 2026-07-21-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> ## ⚠ CROSS-REPO BUNDLE (ADR-36/41)
>
> **The subject of this handoff is `ai-council`. The bundle lives in the `.dev-knowledge` hub.**
> Every `#id`, file path, ADR number, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The two repos have same-named files with different contents — `BACKLOG.md`,
> `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and even `scripts/validate_backlog.py`
> exist in both. Reading the wrong one is the primary failure mode of a cross-repo bundle; `PROBES.md`
> names a **run-in root** per probe for exactly this reason.
>
> **The hub is read-only w.r.t. the target** — this session plans `ai-council` work; it does not edit
> the hub's governance corpus, and CC made **no** change to `ai-council` while generating this bundle
> (including the recoverable-but-unreachable spike evidence in §1 — surfaced, deliberately not
> recovered). The stock generator probes were hub-bound and have been **re-authored against
> verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which and why).

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the target's **own** read-only checks (`scripts/canonical_freshness_gate.py`,
`validate_docs_registry`, `validate_sealed_keys`, `validate_audit_casing`, `validate_backlog`) plus
judgment over `BACKLOG.md` ∩ git — **not** by the hub's `audit.py`, which `ai-council` does not have.
**Re-derive each at read-time — the teeth are in `PROBES.md` (P4/P6/P7/P9/P11/P12), not in trusting
these lines.** This bundle states **no** verdict, exit code, WARN count, drifted `#id`, or count —
those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS part of the headline).** `ai-council` has **no
counterpart to the hub's drift-flag machinery** — no `audit.py ship-gate`, no
`ecosystem/disposition-register.yaml`, no `validate_doc_claims`, no `validate_git_backlog`. There is
therefore **no dispositioned-WARN set to inherit and no standing-vs-new distinction** in the hub's
sense. The target's drift surface is four independent read-only validators plus judgment over
`BACKLOG.md` ∩ git — which is why `PROBES.md` P2/P4/P6/P7 are re-bound rather than run as generated.
**Treat the absence of a consolidated verdict as the flag**, not as a green light: several of those
gates pass *silently*, so "no output" is not "no drift" (P7 reads exit codes explicitly).

**⚠ NEW — and the loudest flag in this bundle: the markdown-it-py spike's EVIDENCE is unreachable.**
The spike branch `chore/spike-md-parser` was deleted with `-D` after teardown. Its JOURNAL prose was
preserved by two cherry-picks — but **those cherry-picks carried `JOURNAL.md` only.** The spike's
actual artifacts (`spike/FINDINGS.md`, `spike/evidence.py` — including the `#81c INVERSION` cases —
plus four implementation files) exist **on no branch**. They survive solely inside a commit object
that is reachable from **no ref**, i.e. dangling and eligible for `git gc`. The teardown JOURNAL entry
**predicted this exact risk in writing** ("cherry-pick … to main if it should survive worktree
teardown") and the mitigation was applied only to the prose half. Recovery handle while it lasts:
**`26192dd`** (`git show 26192dd:spike/FINDINGS.md`). **P11 re-derives live whether it is still
there** — if `gc` has run, this is already unrecoverable.

Why this is the headline and not housekeeping: **§4 items (1) and (2) ask the architect to rule on
`[#80]`/`[#81]` and on buy-vs-build — and the entire empirical basis for both rulings is in that
dangling object.** The perf measurement and the inversion proof are currently prose claims whose
witness is unreachable, in a repo whose own freshly-minted doctrine is *"a report without a
re-runnable checker is a claim, not a witness."* **Recovering or deliberately discarding this is a
decision, and it is time-boxed by `gc`, not by the architect's convenience.** (Read-only bundle: CC
did **not** recover it — that is the target's call, ADR-36/41.)

**CLEARED this window (the prior bundle's single biggest standing flag):** `options_considered`
corrupted on `main` is **fixed and struck** — `[#77]` closed as one contract-scoped ticket, not a
third round of partial patches. The prior handoff's §4 item (1) is **answered**; do not re-open it as
though it were still live.

**Standing, by reference — carried deliberately, not oversights:**

- **Delegation-surface defects still open:** `[#75]` (`secondary_dir` raises where `target_paths`
  swallows), `[#76]` (verdict package names a return copy that never landed), `[#78]`
  (`target_paths` accepts destructive iterable shapes), `[#79]` (failed metrics sidecar can still
  enter the manifest). All four were classified **PRE-EXISTING by differential run**, not by diff
  reading — none were introduced by a merge.
- **`[#66]` stays OPEN, gated on `[#27]`** (CLI-backend scoring); no billed witness authorized. A
  cost decision awaiting the operator — not a stalled task.

**NEW this window, by reference:**

- **A pre-push gate was deliberately bypassed.** `block-ff-push` refused the `#18` push; the operator
  authorized `--no-verify`. **Live re-derivation corrects the JOURNAL's framing on scale:** the entry
  reads as a 3-commit anomaly, but the non-merge population on `main`'s first-parent spine is **very
  much larger and long-standing** (P12 re-derives the live number — it is deliberately not stated
  here). The dominant shape is the *post-merge journal-anchor commit*, which lands direct on `main`
  because a `--no-ff` merge leaves you standing on `main`. So this is a **systemic tension between an
  established anchoring practice and core-invariant #5**, not a one-off — and the gate will keep
  refusing. The decision to not rewrite history was right; the *recurring* condition is unruled.
- **`[#83]` is date-gated:** the `#18` crux-check terra **pass-2 repairs carry no adversarial
  re-review** (pass 3 blocked by a codex usage limit until 2026-07-25). Merged code, unreviewed
  repairs, on a documented deferral.
- **`[#18]` merged but NOT closed** — no live end-to-end witness (every crux path is mock-tested).
  Correct per the doctrine; it means merged ≠ witnessed here, deliberately.
- **A large WEAK closure-proposal backlog is unreviewed** and re-proposes at each session end; only
  `[#77]` was reviewed by operator instruction. P10 grooms the whole open set at boot.

**Do not trust the above as current state** — P4/P7/P9/P10/P11/P12 re-derive all of it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (the **2026-07-20** block, nine entries) already encodes the detail; do
not re-read it as narrative here. **Window boundary:** this covers work landed *after* the
`2026-07-20` bundle was cut — that bundle predates all of it.

- **`[#77]` `options_considered` settled AS ONE CONTRACT and struck.** Six consecutive adversarial
  (terra) passes, each returning real defects; rebuilt on a lane branch, merged, then closed via
  `/review-closures` scoped to `#77` alone. → JOURNAL 2026-07-20 (the six-passes entry + the strike
  entry).
- **The pass-4 finding is the window's real lesson:** the rebuild **introduced a HANG** on an
  ordinary Windows path string, and it **survived three prior review passes**. Answered with fuzz
  guards (termination + non-fabrication, deterministically seeded) rather than another point fix.
- **`[#80]` / `[#81]` filed as DESIGN FORKS — deliberately not fixed.** Both pre-existing; both need
  a ruling, not a patch. Filing-instead-of-widening was explicit: *"quietly widening scope is
  precisely how the previous two fix windows on this function failed."*
- **markdown-it-py buy-vs-build spike — THROWAWAY, recommendation KEEP-SCANNER.** Time-boxed,
  committed-and-stopped, never merged, branch `-D`'d; `src/` never touched. Grounds: a large perf
  regression **and** the `#81` inversion (below). → §1 for the evidence-reachability flag.
- **A published spike verdict was RETRACTED on `main`.** The spike first concluded `#81` was
  *dissolved* by the library; re-testing the half it had not tested showed the opposite. The
  retraction was committed rather than the original entry edited (append-only respected).
- **`[#18]` bounded crux-check Phase A built and merged** — new `crux_check` service + headless
  research executor, wired through orchestrator/synthesis/metrics, with mutation-tested verdict-package
  guards and mechanically-verified boundedness (untouched modules proven byte-identical).
  **Merged, NOT closed.** → JOURNAL 2026-07-20 (the crux entries).
- **Two tickets filed *before* they could become silent debt:** `[#82]` (an accepted Phase-A hole,
  filed **before any implementation**) and `[#83]` (the blocked adversarial re-review, date-gated).
- **`main` pushed** through a deliberate, operator-authorized pre-push bypass (§1).
- **Housekeeping:** two worktree teardowns, both hitting the **same stale-lock / dead-PID** pattern —
  now a repeat, and both resolved by verifying the PID before escalating (no forced removal).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The design questions this window **surfaced but deliberately did not settle**. Resume these; do not
rediscover them. Ordered by how much each constrains the others.

> **Two corrections to the PRIOR bundle, re-derived live — apply before ranking anything.**
> 1. Its §4 item (1) (`options_considered` as a contract) is **DONE**, not open — `[#77]` is closed.
> 2. Its §4 item (3) asserted `LESSONS.md` records the inbox/CLI parity pattern *"three separate
>    times."* **Live re-read: it carries TWO write-ups** — and *each independently claims to be the
>    "3rd instance,"* while naming **different** third incidents. See item (4): this makes the case
>    for the structural fix **stronger** than the prior bundle argued, not weaker.
>
> The supplement (if filled) outranks this section on *intent and priority*; this section stays
> authoritative on *what the defects are*. Everything factual in both is re-derived live (P2–P12).

**(1) `[#80]`/`[#81]` — rule on the preferred failure. The doctrine and the done-when CONTRADICT
each other, and nobody has said so yet.**
This is the item the spike was run to inform, and it is now **evidence-backed and blocking**. The
spike proved **neither implementation satisfies both halves of `[#81]`'s own done-when**: the
line-level scanner *fabricates* options out of a fenced diff, while the library *totally loses* a
fenced options list (returns empty). Here is the contradiction the record does not yet name:

- The `[#77]`/F8 doctrine, operator-ruled and now in `LESSONS.md`, is **under-match toward the loud
  failure** — *"`[]` is honestly empty; `['Risk one']` is plausibly wrong and consumed silently."*
  That doctrine **prefers total loss over fabrication.**
- `[#81]`'s done-when requires *"a fenced options list is shown **not to be silently emptied**"* —
  which **forbids exactly what the doctrine prefers.**

So the ticket cannot be closed as written, by any implementation, while the doctrine stands. **The
ruling is therefore not "which parser" — it is "amend `[#81]`'s done-when to match the doctrine, or
carve out an exception to the doctrine for this case."** Resolve that first; the implementation
question collapses once it is answered. (`[#80]` — continuation-line vs nested-annotation — is a
smaller, genuinely independent rule choice and can ride along.)

**(2) Buy-vs-build is NOT closed — it is deferred on one cheap, unanswered empirical question.**
`output.py` now carries roughly a hundred-plus lines of hand-rolled CommonMark inline parsing, and
that hand-rolling **is the acknowledged root cause of adversarial passes 2–6, including the hang.**
The spike's KEEP-SCANNER recommendation rests on a perf regression measured at a large input size —
and the spike itself posed the gating question and **left it unanswered: is an option payload of that
size realistic at all?** These are synthesizer-emitted option bullets; if the realistic ceiling is far
below the measured point, **the perf objection evaporates and the recommendation flips to ADOPT.**
That is a one-afternoon question with a large architectural consequence, and it should be answered
before any more hand-rolled parser maintenance is authorized.
**Also still unexamined — the prior bundle's actual boundary question, which the spike did NOT
address:** *should the synthesizer be asked to emit structured options directly, so there is nothing
to parse?* The spike compared **two parsers**; it never tested **not parsing**. That third option
remains the only one that removes the defect class rather than relocating it, and it has never been
costed. Do not let "we ran a spike" read as "the boundary question was settled."

**(3) Contract-Version 1.1 — `[#34]` + `[#76]`, now untouched for TWO consecutive windows.**
Carried forward unchanged and slipping. Both change the delegation surface, so they version
**together**. `[#34]` = research-path verdict-package parity; `[#76]` = two-pass write so the
manifest is serialized only after the writes it describes have landed. **Settled and not to be
relitigated** (prior supplement ruling): a *compliance* fix forces no version bump, so do **not**
fold `[#77]`-class work into the 1.1 bundle.

**(4) `[#69]` inbox/CLI parity — the recurrence argument is stronger than previously stated.**
The two `LESSONS.md` write-ups name overlapping-but-different incident lists (they agree on two, and
diverge on the third), so the underlying duplication bug has **more distinct occurrences than either
entry alone claims**, and `[#69]` is the next one after those. **Neither entry records a structural
fix ever landing** — both end with the same unexecuted rule: *share a common processor, or add a
parity-check test.* `[#69]` is itself two defects: frontmatter `models:` is dead in the default path,
**and** the two entry points guard it on **different conditions**, so the same brief yields a
different panel via `--file` than via `--inbox`. **Decide the permanent answer — shared processor or
enforced parity test.** Patching `[#69]` alone guarantees a next instance.

**(5) Two stacked cost decisions on the crux-check, both unpriced.**
(a) `crux_check.providers` is currently a single-provider list and the step is **unconditional** —
widening it toward the general research provider set would put a very long deep-research call between
**every pair of rounds**. The JOURNAL flags this correctly as deserving **an ADR note, not a tuning
knob**: it is a per-run cost multiplier disguised as config. (b) `[#18]` cannot close without a
**billed live end-to-end witness**. Both need an operator call, and (a) should be recorded as a
decision before it is silently widened by someone tuning config.

**(6) Enforcement asymmetry with the hub — carried, with NEW evidence in BOTH directions.**
Still the genuinely cross-repo question the architect is uniquely positioned to rule on: `ai-council`
has independent read-only validators and **no consolidated gate**; the hub has a registry, a ship-gate
verdict, and a disposition register.
*New evidence for "gap":* a pre-push gate was bypassed; the spine condition behind it is systemic and
unruled (§1); and **six evidence files left the repo with no organ noticing** — no gate, anywhere,
observed the spike-evidence loss.
*New evidence for "correct-by-design":* the four validators pass cleanly and silently, and this repo
took `[#77]` through six adversarial passes to a defensible contract **without** a consolidated gate —
the adversarial-review loop, not a gate, is what actually caught the defects here.
**Rule on it; do not close it by defaulting to hub parity.**

**(7) Verification-as-code — the doctrine's first stress test, and it bent on the flank nobody
guarded.**
The doctrine held where it was pointed: `[#18]` merged with mock-only coverage and **stays open** for
want of a live witness — exactly right. But the spike is the counterexample: a **throwaway** branch
produced the empirical basis for two pending rulings, and that basis is now unreachable (§1) while its
conclusions circulate as prose. **The doctrine covers deliverables and does not cover spikes** — yet a
spike is precisely where evidence is most load-bearing and least durable. Decide whether
"verification-as-code" extends to throwaway work, and if so what the minimum durable residue of a
spike is (the measurement script, at least, promoted to `scripts/` before teardown). This is the
generalizable lesson of the window and it is currently unfiled.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per ADR-66. Every `#id` in this residual is an **ai-council** id. `[E1]` (invocation surface
  & delegation-readiness) carries the delegation-surface work §4 items (1)–(4) are about.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** — this is a cross-repo handoff and the
  hub is read-only-adjacent: it hosts the bundle, it is not the subject. Note that at least one
  merge subject on the target's spine carries a **hub-range `#id`**, so an `#id` seen in git is not
  automatically an ai-council ticket — P4/P10 must resolve each against `ai-council/BACKLOG.md`.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist there. P4 substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection,
  and **P10 is the judgment layer over it** (groom every open `#id` as live / dead / awaiting-ruling).
  This grooming is the operator-ruled boot obligation, not optional. **Caution for P4:** a bracketed
  `[#id]` in a merge subject does **not** imply closure here — this window deliberately merged
  `[#18]` *without* closing it, so a naive bracket-scan will report false closures.
