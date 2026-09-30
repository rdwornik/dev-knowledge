# Review — lane-handoff-boot-dispatch repair-1

**Consumer:** `LANE-5B5-3-lane-handoff-boot-dispatch.md`

**Date:** 2026-09-30
**Branch:** `worktree-lane-handoff-boot-dispatch`
**HEAD:** `94efde63`
**Diff range:** repair-1 only — the two `REFUSED-lane-handoff-boot-dispatch.md` fixes (the
render-seat/fallback paragraph and the R34.1-vs-`--watch` precedence clause), both inside
`protocols/HANDOFF_BOOT.md`. The prior full-arc reviews are the session file's own "Codex
`gpt-5.6-terra` review" section (original pass, against `511073f9`/`f7f4f051`) and this
file (repair-1's two agy passes, against `94efde63`).
**Files in scope:** `protocols/HANDOFF_BOOT.md`
**Tally:** original terra pass 2/0/0/0 (P1/P2/P3/P4, both FIXED across the original
handback and this repair); repair-1 first agy pass 0/2/2/1 (P1/P2/P3 counted separately
below: 2 P1 + 2 P2, all FIXED); repair-1 agy recheck 0/0/1/0 (1 P3, non-blocking, no fix
needed)
**Reviewer:** `agy` CLI — **SUBSTITUTION**: Codex (`gpt-5.6-terra`) was at its usage limit
both before and after the repair-1 fix (`codex exec review --uncommitted -m gpt-5.6-terra
--title ...`, stated reset: Oct 3rd 2026 9:07 PM), so `agy` ran instead as the recorded
SUBSTITUTION per ruling (e) (`agy -p "..." --effort high --dangerously-skip-permissions` —
print-mode without that flag soft-denies every tool call and returns empty output, a known
`agy` gotcha; both raw outputs below are non-empty, satisfying the "accepted only if its
output file exists and is non-empty" bar). The model actually served by `agy` is not
independently identified in its own output. Codex terra's own error output for both
attempts (`codex-review-raw.txt`, `codex-recheck.txt` under the lane's job tmp) is a
usage-limit error only, carrying no findings.
**Review profile:** docs, correctness-only (prose-only diff; zero lines of Python changed)

---

## Focus

This record closes the contract's close-out item 4 gap left open by
`REFUSED-lane-handoff-boot-dispatch.md`'s note: the Codex review existed only in the
session file and in the lane's own job tmp (deleted with the job), with no consumer-citing
record under `docs/audits/`. It carries, in order: (1) the original terra pass's 2 P1s
(from the lane's first build, job `6bbc8028`) with their fix status; (2) the repair-1 `agy`
first-pass raw output verbatim; (3) the repair-1 `agy` recheck raw output verbatim.

---

## Original terra pass — 2 P1s (job `6bbc8028`, against `511073f9`/`f7f4f051`)

Recovered from `codex-review-raw.txt` under job `6bbc8028`'s tmp (the lane's own
first-build session; recoverable at the time this record was written).

> - [P1] Do not launch the integrator through pre-launch —
>   `protocols/HANDOFF_BOOT.md:160-164`
>   For a new batch, this instruction deadlocks startup: `dispatch.py launch --batch
>   <BATCH>` always runs the `no-live-integrator` pre-launch organ, so launching the first
>   integrator this way is refused precisely because it has not yet bound. The integrator
>   must first be started through its order/session path and bind itself; otherwise no
>   batch can establish the live integrator required to launch lanes.
>
> - [P1] Keep queue operation aligned with the dispatcher order —
>   `protocols/HANDOFF_BOOT.md:177-180`
>   This newly tells a fresh dispatcher never to use `--watch`, but the live
>   dispatcher-order template requires one bounded `queue --watch` invocation and its
>   handover procedure restarts that watcher. Following this boot instead leaves
>   dependency-cleared lanes dependent on manual repeat invocations rather than firing when
>   the integrator updates state, so the two canonical instructions now prescribe
>   incompatible batch behavior.

**Disposition:**

- **P1 #1 (pre-launch deadlock): FIXED** at the lane's original handback (`511073f9`) —
  the text now states the integrator and dispatcher start by the operator pasting their
  filled order template into a new session, per each template's own `authorized-by:` line.
- **P1 #2 (`--watch` conflict): FIXED at repair-1** (`94efde63`) — the original handback
  left it `ACKNOWLEDGED, not fixed` (the template is outside **Files you own**); the
  integrator's refusal (item 2) required an in-owned-file precedence clause instead of a
  template edit, and repair-1 added: "The queue is one-shot passes, not `--watch`" (R34.1)
  — supersedes `templates/dispatcher-order-template.md`'s still-live `--watch` line until
  updated.

---

## `agy` first pass (repair-1 diff) — raw output verbatim

Recovered from `agy-review-raw.txt` under this lane's job `bb3d9dfb`'s tmp.

```
### Review Summary: Changes Requested (P1 Findings Present)

The diff attempts to address the two items from the integrator refusal, but introduces semantic inaccuracies regarding the `no-live-integrator` organ, garbled syntax in the fallback clause, a fragile line locator, and an unrequested out-of-scope edit that drops protocol guidance.

---

### P1 Findings (Must-Fix)

1. **Omission of the condition "before an integrator is bound" & misleading "first render" phrasing**
   * **Diff location:** `protocols/HANDOFF_BOOT.md:158-161`
   * **Text:** `...launch is a LANE's path only; a batch's first render, integrator or dispatcher refuses on that same organ.`
   * **Issue:** 
     * The `no-live-integrator` check fails **if and only if no integrator is currently bound/live**. Once an integrator is bound, `no-live-integrator` succeeds.
     * The refusal requirement was explicitly: *naming the 'render' seat, alongside integrator and dispatcher, as a seat that 'launch' refuses via the no-live-integrator pre-launch check **before an integrator is bound***.
     * Stating *"a batch's first render, integrator or dispatcher refuses on that same organ"* misstates the mechanism:
       1. "First render" is nonsensical (a batch does not have a sequence of renders where only the first refuses).
       2. It omits the causal condition: it refuses because an integrator is not yet bound, not inherently because of the seat role itself.
   * **Fix:** State clearly that calling `launch` for render, integrator, or dispatcher **before an integrator is bound** refuses on `no-live-integrator`.

2. **Garbled syntax and ambiguous actor in fallback clause**
   * **Diff location:** `protocols/HANDOFF_BOOT.md:163-165`
   * **Text:** `A seat pre-launch refuses anyway falls back to its own order's ## Dispatch line, recorded FALLBACK <slug>: <why>...`
   * **Issue:**
     * Grammatically broken: *"A seat pre-launch refuses anyway falls back..."* is missing a relative connector (e.g., *"A seat that pre-launch refuses..."* or *"If pre-launch refuses a seat..."*).
     * The colloquial *"anyway"* is ambiguous.
     * Actor ambiguity: Who falls back, and who records `FALLBACK <slug>: <why>`? In this workflow, the dispatcher (or operator) executing the dispatch falls back to the manual order dispatch line and logs the fallback. Passive phrasing obscures who is responsible for the record.
   * **Fix:** Restructure clearly, e.g.:
     `If pre-launch refuses a seat, the dispatcher falls back to the seat's own order ## Dispatch line, recording FALLBACK <slug>: <why>...`

---

### P2 Findings (Should-Fix)

3. **Out-of-scope edit and dropped specification in Hunk 1 (Architect off-repo context)**
   * **Diff location:** `protocols/HANDOFF_BOOT.md:127-133`
   * **Issue:**
     * This hunk is completely unrelated to the two repair items named by the integrator refusal.
     * In condensing the prose, it silently deletes explicit handling for cold/cleared handoffs:
       *(“...but an empty supplement (a cold / cleared handoff) carries no answers, so ask the full question...”)*.
     * Modifying this unrelated section introduces scope creep and risks regression during a targeted repair lane.
   * **Fix:** Revert Hunk 1 to keep the repair diff minimal and strictly focused on the refusal repair items.

4. **Fragile line-number locator (`templates/dispatcher-order-template.md:65`)**
   * **Diff location:** `protocols/HANDOFF_BOOT.md:165`
   * **Text:** `(templates/dispatcher-order-template.md:65)`
   * **Issue:** Hardcoding line `:65` creates immediate drift debt, especially since Hunk 3 explicitly notes that `templates/dispatcher-order-template.md` is currently out-of-date and pending changes. Once that template is edited, line 65 will drift.
   * **Fix:** Reference the section or pattern anchor (e.g. `templates/dispatcher-order-template.md` `## Dispatch` or fallback instructions) rather than a rigid line number.

---

### P3 Findings (Minor / Polish)

5. **Style and slight redundancy in R34.1 precedence rule**
   * **Diff location:** `protocols/HANDOFF_BOOT.md:177-179`
   * **Text:** `...until that template updates; on conflict, follow R34.1.`
   * **Note:** "until that template updates" is slightly colloquial ("until that template is updated" is cleaner). "On conflict, follow R34.1" is slightly redundant with "supersedes", but acceptable for emphasis.
```

**Disposition:** all four (2 P1 + 2 P2) confirmed FIXED — see the recheck below. P3 finding
5 (style nit) was folded into the same reword as P1 #1/#2's fix and is not separately
tracked.

---

## `agy` recheck (repair-1 diff, post-fix) — raw output verbatim

Recovered from `agy-recheck.txt` under this lane's job `bb3d9dfb`'s tmp.

```
### Review Summary: All Four Findings FIXED

All four findings raised in the previous review have been successfully addressed. A minor P3 nit is noted below regarding the word "render", but it does not block landing.

---

### Finding Status

#### [P1#1] Mechanism misstatement and "first render" phrase
- **Status: FIXED**
- **Rationale:** The revised text removes the nonsensical "first render" phrase and correctly specifies the mechanism and condition:
  > *"`launch` is a LANE's path only; render, integrator or dispatcher called before an integrator is bound refuses on that same organ."*
  Stating *"before an integrator is bound"* accurately identifies the gate condition enforced by `no-live-integrator`.

#### [P1#2] Grammatically broken fallback clause and ambiguous actors
- **Status: FIXED**
- **Rationale:** The clause has been rewritten into two clean, unambiguous independent clauses:
  > *"A `pre-launch`-refused seat falls back to its own order's `## Dispatch` line; the launcher records `FALLBACK <slug>: <why>` (`templates/dispatcher-order-template.md`)."*
  The actor executing fallback (the seat) and the actor logging fallback (the launcher) are now explicitly separated and distinct.

#### [P2#3] Dropped empty-supplement/cold-handoff handling
- **Status: FIXED**
- **Rationale:** The trimmed bullet preserves the necessary fallback clause for cold/cleared handoffs without bloat:
  > *"[...] an empty supplement (cold/cleared handoff) carries no answers, so ask in full."*

#### [P2#4] Fragile hardcoded line number (`:65`)
- **Status: FIXED**
- **Rationale:** The brittle `:65` locator in `templates/dispatcher-order-template.md:65` was replaced with a robust content locator:
  > *"`templates/dispatcher-order-template.md`'s still-live `--watch` line until updated."*

---

### New Findings

- **[P3] Semantic grouping of "render" with order-templated seats**
  - **Location:** Line 154 / 161
  - **Detail:** In *"the render, integrator and dispatcher do not"* followed by *"Each instead starts by the operator pasting its own filled order template into a NEW session"*, "render" is lumped in with seats that have order templates (`integrator` and `dispatcher`). Contract render is an action/step rather than a separate seat with its own order template. This is minor context/phrasing and non-blocking.
```

**Disposition:** SKIPPED (non-blocking, per the recheck's own words). The render seat's own
order (`to-cc/SEAT-RENDER-WAVE5B-N5-2026-09-29.md`) is in fact a filled template pasted
into a new session exactly like the other two, confirmed by inspection at repair-1 — the
grouping this P3 flags is not a factual error, only a phrasing preference the recheck
itself declines to block on.

---

## Verification (repair-1, from the session file's own repair-1 self-check re-run)

- `boot_byte_budget`: PASS — `protocols/HANDOFF_BOOT.md is 17989 bytes, within its 18000-byte budget`.
- `silent_rule_detector.py .` on the staged tip: 450 — unchanged from pre-repair, still ≤ origin/main's 452 baseline.
- Targeted suite (`memory_admission_gate.py run --workers-flag -n -- pytest tests/test_handoff_modes.py tests/test_silent_rule_ratchet.py tests/test_claude_md_byte_cap.py`): 69 passed.
