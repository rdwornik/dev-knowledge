# ADR-85: Session-lifecycle enforcement — deterministic JOURNAL/BACKLOG stop-gate

**Status:** Accepted
**Date:** 2026-06-16
**Decision tier:** Architecture (AI Council, 4-model panel — see verdict: council-out-20260616_131123)

## Context
The human is the manual trigger at every session end, reciting which canonical docs to update. The reminder is unreliable: docs rot (CONTRIBUTING untouched for days) and a recent agent-authored close-plan silently omitted most of the doc set. The workflow's value is its discipline — every change traceable, no fabricated state — so any enforcement must not be gameable into box-ticking. A 4-model Council debated mechanism (deterministic vs LLM-judge), teeth (hard/soft), and scope (strict/adaptive), plus a contrarian (enforce vs simplify).

## Decision
1. **Scope reduction is the primary intervention.** Gate **only JOURNAL + BACKLOG** per session — the two docs that both rot worst and legitimately change every working session. Demote ARCHITECTURE, VISION, LESSONS, CONTRIBUTING to **"update when materially affected"** — not per-session-gated.
2. **Mechanism: deterministic, executor-side.** Extend the existing session-end-hygiene Stop-hook; no LLM in the gate. Rationale: once scope is two docs, currency is no longer a fuzzy semantic question — it is a deterministic check that is debuggable, zero-latency-per-turn, and cannot hallucinate compliance.
3. **Teeth: hard block on the JOURNAL leg only in v1.** JOURNAL leg verified by an **un-gameable commit-SHA anchor** (the journal diff must reference ≥1 commit SHA produced this session) — this **supersedes** the prior advisory journal-presence check, which the SHA anchor strictly subsumes. The **BACKLOG leg is advisory (a nudge, not a block) in v1** — verified by a structural-marker delta — and is **promoted to a hard block when the traceability-spine gives it an airtight, always-warranted anchor (see R1)**. Rationale: a hard gate is justified only for a check that is both un-gameable *and* always-warranted; the backlog-marker check is neither (it is gameable, and per the "done tasks leave the file" convention a session that advances but does not finish a task warrants no backlog change), so hard-gating it in v1 would manufacture the false-positives the criteria below warn against.
4. **Override: explicit + logged, HEAD-bound.** A blocked turn exits only via `/override [reason]`, which is logged. The override is a gitignored token recording the current HEAD; the Stop-hook **pure-reads** it and allows while HEAD is unchanged, **re-arming automatically when a new commit lands** — keeping the hook a read-only validator (per the repo's scripts-are-read-only invariant). **No auto-bypass-after-cap** — auto-bypass trains the agent that persistence beats policy.
5. **Single source of truth.** One `definition-of-done` doc, injected into the executor at session-start and into the orchestrator handoff.
6. **Scope-freeze.** No docs added to the gate for 4 weeks; gather reliability/override-rate data first.

### Architect refinements (on top of the panel verdict)
- **R1 — Backlog anchor couples to the traceability-spine.** The journal leg is airtight (SHA); the backlog "structural-marker" leg is the weak, gameable leg. Its real anchor (issue-ID↔commit) IS the separate traceability-spine decision. Therefore: ship the JOURNAL gate hard now; the BACKLOG leg runs as an **advisory nudge** on the interim marker-check and is **promoted to a hard block when the traceability-spine ADR lands**. Co-design. *(Hard-gating the weak leg in v1 would manufacture the false-positives the criteria warn against — this refines an earlier version of R1 that had backlog as a hard interim gate.)*
- **R2 — Ungated-doc rot is handled by detection, not human review.** The panel's "human bi-weekly review" of the ungated docs reintroduces the human-as-trigger. Instead, ungated-doc staleness (e.g. ARCHITECTURE untouched >N sessions while code changed) is **surfaced as a signal in the daily digest / conformance dashboard** — deterministic, not per-session-gated, not human-memory. This is a later item that rides with the conformance-dashboard work; v1 accepts the other docs are ungated.
- **R3 — Explicit override only on the new gate (no auto-bypass).** *Implementation verified the existing hook is purely advisory — it emits a soft nudge, always exits 0, and has no hard block and no auto-allow-after-cap. There is nothing to remove; the original framing of this refinement ("remove the existing auto-override antipattern") was based on a wrong premise and was corrected after CC read the live hook.* This is therefore a **forward constraint on the new hard gate**: a blocked turn exits only via explicit `/override`, never via a retry-counter that auto-allows (which would train "persistence beats policy").

## Consequences
**Positive:** human is no longer the trigger; deterministic (debuggable at 2am, no per-turn LLM latency/cost); journal leg un-gameable; narrow scope → low false-positive surface; v1 removable in one revert sequence.
**Negative / accepted trade-offs:** the four ungated docs will rot more until R2 lands (accepted for v1); the backlog leg is advisory-only until the traceability-spine hardens it to a gate (R1); override-normalisation risk — mitigated by logging (if overrides exceed ~10% of sessions, the rules need tuning, not the human).

## Alternatives rejected
- **LLM-judged primary gate** (the going-in lean): nondeterministic, per-turn latency, can hallucinate compliance — and scope-reduction dissolves the semantic-fuzziness that justified it.
- **Hard block on the full doc set:** guarantees false-positives → the gate gets disabled; incentivises box-ticking.
- **`/wrap` operator routine as primary:** still a human trigger — fails the core goal.
- **Auto-allow after N retries:** trains the agent to loop until the gate yields.

## Amendment — 2026-06-16 (CC implementation correction; defect fix, not a new decision)
The v1 hook exposed a **contract error** in this ADR's framing. A Stop hook's
`hookSpecificOutput.additionalContext` is **not** a clean allow: per CC changelog v2.1.163 it
"continues the conversation" — it **keeps the turn going** — and consecutive keep-goings count
toward CC's block-cap (v2.1.143), which auto-overrides the turn. So the "advisory = exit-0,
non-blocking" premise (Decision 3 / R3) was **wrong**: an advisory built on additionalContext
**loops to the cap** when its condition persists across stop attempts (a no-task session's
BACKLOG-no-marker — the *correct* state per the DoD — or freshness same-day, where re-stamping
is a no-op diff) → the exact "persistence beats policy" auto-bypass §4 / "Alternatives
rejected" forbid. Witnessed live: "a hook blocked the turn from ending 9 consecutive times —
overriding and ending turn."

Realized fix: advisory legs are made guaranteed-terminating by a **structural floor** —
advisory-only output never keeps the turn going; advisory rides **only** folded inside a hard
block. This is the *load-bearing* guarantee, because `stop_hook_active` is **NOT** in the
CC-2.1.178 Stop-hook stdin schema (verified) so a fire-once-on-retry scheme cannot carry it; a
fire-once path is wired but **dormant** (activates only if a runtime ever supplies the field).
The **hard JOURNAL leg is unchanged** and explicitly does **NOT** honor `stop_hook_active`
(honoring it = fire-once = the forbidden antipattern); it terminates by *compliance*, never the
cap. Fix commit `8840b33`; tests reproduce the keep-going loop red→green. See JOURNAL &
LESSONS 2026-06-16.

**Correction (2026-06-16, same-session, witnessed at wrap):** the claim above that
`stop_hook_active` is "NOT in the CC-2.1.178 stdin schema … fire-once is dormant" is
**wrong** — the live Stop event at this session's wrap surfaced the advisory, which the code
emits *only* on `stop_hook_active is False`, proving the runtime **does** send the field. The
docs page (and a fast-model summary of it) omitted it; the runtime overruled the doc-read.
So **fire-once is ACTIVE** (the standalone-nudge mechanism), and the **structural floor is the
backstop** for any context that omits the field — both ship, the no-loop guarantee holds
either way. This re-validates the witnessed-behavior-outranks-the-read rule: a doc/summary is
a lead, not verification.

## Amendment — 2026-06-19: per-session SHA-anchor (push-boundary → session-boundary fix; C1)

**What this corrects.** Decision 3 states the JOURNAL anchor must name "≥1 commit SHA produced
**this session**". The v1 implementation computed the wrong boundary: it took the arc as
`base..HEAD` with `base = @{upstream}` (= `origin/main`) — the **push** boundary, not the
session boundary. Under deferred-serial-push the unpushed arc spans **multiple sessions**, and
the leg passed on `any(sha cited)` over that whole arc, so **one** citation from a *prior*
session vaccinated the entire arc and a later session that shipped commits without journaling
**passed silently** (witnessed live on the 2026-06-18 arc; surfaced by the #188 hook-
completeness audit as finding C1).

**The fix.** The arc is narrowed to the **session**: the commits since the last JOURNAL-citing
("journal-wrap") commit. Walk `base..HEAD` newest-first and stop at the first commit that
*wrote* a SHA-citation into `JOURNAL.md`; the trailing run of commits after it is the current
session's work, which fires when non-empty. `any()` is **kept** — over the narrowed arc (one
citation in the session suffices; requiring *every* commit cited would deadlock the
multi-session arc). The boundary is detected by a commit that **wrote** a citation (a wrap),
never one that **is** cited — a wrap cites its session's *work* commits, never its own
unknowable hash, so keying on "is cited" would leave the wrap forever in the trailing run and
over-fire every happy path. Two robustness points: per-commit detection uses `git show
--first-parent` so a `--no-ff` merge that carries the branch's journal still anchors (git's
combined `--cc` merge diff would otherwise hide it and hard-block every merged-then-journaled
`/ship`, HEAD = merge commit); and `_base_ref()` now prefers a **verified** `origin/main`, with
a `git rev-list` error anchoring on HEAD instead of an empty-range **vacuous PASS** (the
secondary C1 false-pass: a degenerate worktree base made the range error → empty → silent
pass).

**Relationship to original text.** Decision intent is **unchanged** — the anchor was always
meant to be per-session and un-gameable. This amendment records that the v1 *computation* of
the session boundary was wrong (push, not session) and fixes it, plus the merge-diff and
degenerate-base edge cases. The hard/advisory split, the override (§4), and the structural
floor (2026-06-16 amendment) are untouched. Fix + regression tests this session
(`test_e2e_cross_session_miss_blocks`, `test_session_shas_bad_base_anchors_head`,
`test_e2e_merge_delivered_journal_passes`); see the 2026-06-19 JOURNAL entry and
`docs/audits/2026-06-19-hook-completeness-audit.md` (C1 finding).

## Amendment — 2026-08-03: the obligation moves to integration, the teeth move to pre-push

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94).** The decision body above is
> preserved **verbatim** — nothing in it is edited, including Decision 4's `/override` text and
> the two prior amendments. This section records a **change of mechanism**, ruled by the operator
> on 2026-08-03 against two independent derivations (CC, sealed before `sol`; `sol` via
> `codex exec -s read-only`, brief only). Decisions 1, 2, 5 and 6 of the body stand unchanged;
> Decision 3's *intent* stands and its *implementation* is replaced; Decision 4's local-token
> path is **retired** by this amendment and is superseded by §A2 below.

### A0. Motivation — the sharpest available statement of the defect

`_base_ref()`'s first branch prefers the branch's own upstream. So on a feature branch,
`git push -u origin feat/x` **moves the base to `origin/feat/x` and empties `base..HEAD`**, and
the hard leg returns None. **Re-measured at `4f3f8531`** in an isolated clone with its own bare
origin, immediately before this amendment was written:

```
BEFORE push -u:  base=origin/main       set=['cd86ab8']  HARD=BLOCK
AFTER  push -u:  base=origin/feat/x     set=[]           HARD=none
```

The commit is still unmerged, unreviewed and unjournaled. **The cheapest discharge available
today is not "push to main" — it is "publish to a branch nobody reads."** Any fix that addresses
only the merge-to-main path leaves this open, which is why the boundary itself is replaced rather
than adjusted.

### A1. D1 — the obligation is created by **integration onto `main`**, not by an authored commit

An obligation arises when a first-parent spine entry lands on `main`. Authored commits on a
feature branch create none.

**Reason, and the second is decisive.** Authorship is not reliably derivable from git metadata in
a shared checkout or a parallel lane — the 2026-07-25 override token records this gate demanding
SHAs belonging to a *concurrent session*, where the only literal repair was to claim another
session's commits as one's own. And an obligation over *authored commits* policed by a detector
over *publication* is the exact shape that produced this incident. Under Decision 3's own
un-gameability bar, **an integration event is a recorded fact; authorship is an inference.**

**Cost:** ADR-85 no longer guarantees one JOURNAL record per executor session. It guarantees one
per integrated unit. Session-level fidelity is traded for a boundary the serial merge gate can
actually enforce.

### A2. D2 — the local token path retires; `--no-verify` is the sole escape; the backstop makes it non-silent

- The **Decision 4 local-token path is retired.** Local state cannot make an integration event
  compliant. `_override_active()` and `logs/.session-override-token` cease to be a discharge.
- The **sole escape is `git push --no-verify`** — transport-level, explicit, human-typed, and
  pretending to be nothing else.
- The escape is made **non-silent by an audit backstop** (§A8): an `ALL_CHECKS` leg asserting
  every first-parent spine entry on `main` is anchored. A bypass therefore survives in the record
  as a standing FAIL until a JOURNAL anchor lands.

**Cost:** a session whose scope forbids JOURNAL edits cannot integrate debt-free; it parks, or it
integrates and carries a visible debt until a later entry pays it. There is no longer a local
artifact that makes non-compliance look like compliance — which is the point.

### A3. D3 — the push boundary is removed **in the code as well as in the text**

The 2026-06-19 amendment above is titled *"push-boundary → session-boundary fix"* and states the
v1 implementation "took the arc as `base..HEAD` with `base = @{upstream}` … the **push** boundary,
not the session boundary." **It narrowed only the inner walk.** `_session_shas()` still computes
`base..HEAD` at `:167-168`, and `check_journal_sha_anchor()` returns at `:300` on an empty range
**before** the session walk at `:302-307` ever runs. In the case the incident hit, the 2026-06-19
fix is unreachable code.

**This amendment records that as the precedent it exists not to repeat: an amendment declared a
removal it did not deliver, and the declaration was believed for six weeks because nobody
re-measured it.** Under this amendment the push boundary is gone from the obligation semantics
entirely — no `@{upstream}`, no `origin/main`, no invented base.

**Cost:** none to correctness. The replacement bound is supplied by git itself (§A5), so the
disagreement between the two derivations about *what* should replace the base — a journal-wrap
walk with a floor, versus a fixed epoch scan — dissolved rather than being adjudicated.

### A4. D4 — parked-and-awaiting-operator-GO is legitimate, as a **consequence** of A1

Commits sitting on a feature branch awaiting operator GO create **no obligation**, because no
integration has occurred. This is not a new rule and needs no new machinery: it falls out of A1.

**No agent-asserted marker is required anywhere** — no "parked", no "awaiting approval", no flag
the agent sets about its own state. That satisfies the non-negotiable that Decision 3 already
implied: nothing the agent asserts is an input to a hard check.

**Cost:** ADR-85 supplies no reminder for a forgotten parked branch. Branch inventory and handoff
discipline carry that risk, as they did before.

### A5. D5 — the HARD leg lives at **pre-push, scoped to `main`**; Stop is advisory in full

Both derivations reached this independently, which is the strongest signal in the adjudication.

The Stop hook cannot host a hard gate: its unit is a model-turn boundary, and the host force-ends
a turn after N consecutive blocks. **Nine identical firings on 2026-08-03 added zero enforcement
pressure and terminated in exactly the silent auto-bypass Decision 4 forbids by name.** An organ
that can be exhausted cannot carry teeth.

At pre-push the obligation range is **the one git hands the hook** — `remote_sha..local_sha` for
the ref being pushed. Exact, bounded by construction, no invented base, no floor, no cap. A
refused push is simply refused; there is no retry surface to exhaust.

**Cost:** compliance is collected at integration rather than immediately after authoring. A
locally created unanchored merge needs a follow-up JOURNAL entry before it can be pushed.

### A6. D6 — hard organs fail **closed**; D7 — the dirty tree never guards a hard check

**D6.** A hard organ returns non-zero on internal error. `check_seal_identity.py:73-77` is the
in-repo model — *"refusing the commit; an error is never a silent pass."* The same fix applies at
`block_ff_push.py:205-207`, which today prints *"degraded — allowing push"* and returns 0, silently
auto-allowing the very push it exists to refuse. The now-advisory Stop leg may fail soft, but
**loudly** — never the silent `return 0` at `:497-498`.

**Cost:** a transient git or environment failure can block an ordinary push and require explicit
operator recovery. That is intentional friction traded for the elimination of false green.

**D7.** `:297` — `if not _is_clean(): return None` — suppresses the hard leg entirely whenever any
file is uncommitted. It was written as anti-nag ergonomics (`:56-57`: "gated to a clean tree = a
plausible wrap, so mid-work turns are not nagged") and is **named here for the first time as a
discharge path**: a single uncommitted file silences the gate, indistinguishably from compliance.
No prior ADR text documents it. It survives on the advisory path only, where anti-nag is correct,
and guards no hard check.

**Cost:** none material — ADR-85 does not enforce documentation of uncommitted work, and never did.

### A7. The anchored object

The anchored object is the **first-parent spine entry** on `main` — the merge commit, or a direct
commit where one exists. **Not every reachable commit.** This is consistent with the repo's
existing spine scan (`git log --first-parent main`), with the per-shipped-unit journaling rule
(operator ruling 2026-08-03), and with how JOURNAL entries are already written.

**Definitional detail, measured — a spine entry is anchored when JOURNAL names ≥1 SHA the entry
INTRODUCED, not the entry's own SHA.** A merge commit cannot name its own hash: the JOURNAL entry
it carries is authored before the merge exists. Measured at `4f3f8531`, the naive "spine SHA is
named" predicate reports **686 of 1292** spine entries unanchored *including HEAD itself*; the
correct "introduced SHA is named" predicate (which is what Decision 3's SHA anchor and §A8's
discharge both mean) reports a contiguous anchored run of **11** from HEAD. Any implementation
using the naive predicate is measuring the wrong thing and will fail on its own merge.

**Named residual, stated rather than hidden.** A single push carrying **multiple** shipped units
is anchored by an entry naming ≥1 SHA in the range — so the second and later units in one push
ride on the first unit's anchor. Under the operator's serial merge gate this is rare (one merge,
one push). It is a known limit, filed as such in the manner of `[#475]`'s stated limit, not an
oversight.

### A8. Migration note and the dated disposition floor

**The backstop.** An `ALL_CHECKS` leg walks `git log --first-parent main` and asserts every spine
entry is anchored. **A gap is a FAIL, not a WARN** — a WARN would be dispositionable, and a
dispositionable backstop cannot be the thing that makes `--no-verify` non-silent.

**The floor, with its measurement.** Applying the §A7 predicate at `4f3f8531`: the contiguous
anchored run from HEAD is **11 spine entries**, reaching back to `24882f8cc` (2026-08-02, *"Merge
branch 'claude/conformance-2026-08-02'"*). The next older entry, `5d1c71f03` (2026-08-02, *"Merge
branch 'chore/doc-counts-2182'"*), is the newest gap.

> **Dated disposition floor: `24882f8cc` (2026-08-02).** Spine entries **strictly older** than
> `24882f8cc` are dispositioned once, here, by this amendment. **Reason:** they were authored
> under the pre-amendment contract, in which push, a dirty tree, or hook exhaustion were live and
> undocumented discharge paths — the record they would be judged against did not exist when they
> landed. Retro-anchoring 1,281 historical spine entries would mean writing JOURNAL entries for
> sessions nobody attended, which manufactures record rather than keeping it.

**A floor is a recorded fact, not a bypass.** It is dated, it names its SHA, it states its reason,
and it is written into the ADR rather than into a disposition register where it could be quietly
extended. Nothing after `24882f8cc` is covered by it, and the floor does not move without a
further amendment.

**What changes meaning.** "The gate is silent" no longer implies "nothing is owed" — today that
sentence conflates compliance, push, and a dirty tree. After this amendment, pre-push silence
means *nothing unanchored is being integrated*, and backstop silence means *the spine is whole
above the floor*. Any prior reasoning of the form "it stopped complaining, so we are clean" is
retroactively invalid — including the 2026-08-03 afternoon arc, whose debt (`808ef911`,
`42ff1323`) was discharged by push and later paid honestly at `476116c6`.

**What is untouched.** The `--first-parent` requirement at `:268` remains load-bearing (git's
combined merge diff would otherwise hide a branch's JOURNAL entry). The advisory BACKLOG-marker
leg (R1) is unchanged and stays advisory. The existing `warn-no-ff-*`, `warn-doc-rot-*`,
`warn-undeclared-*` dispositions reference other organs and are unaffected.

## Links
- Council verdict: `council-out-20260616_131123-pick-council-brief-session-lifecycle-enforcement.md`
- Coupled decisions: traceability-spine (R1), handoff-supplement (the DoD-via-handoff is process-context-in-handoff), conformance-dashboard (R2).
