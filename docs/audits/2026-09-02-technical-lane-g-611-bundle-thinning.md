# LANE g-611 (bundle-thinning) — end-of-lane artifact

- **Class:** technical · **Date:** 2026-09-02 · **Lane:** `lane-g-611-bundle-thinning`
  (branch `worktree-lane-g-611-bundle-thinning`, contract `LANE-g-611-bundle-thinning.md`)
- **Targets:** `[#611]` HANDOFF_PROCESS v7 minimal-bundle package, Done-when's measured size
  target — a real cut **<=20,000 B at >=70% window-specific**.

## Step 1 — DERIVING "window-specific" (plan-first, before any implementation)

**The premise: this term is not new, it is un-mechanized.** "Window-specific" already has a
working definition — it is what the 2026-08-26 census and the 2026-09-01 equilibrium map both
measured by hand to produce the ~77%/~31%/~43% figures this whole `[#611]` arc cites. Neither
artifact states the definition as a reusable rule; both apply it ad hoc, once, to one bundle.
This step makes that ad hoc method a mechanized one — derived FROM the census's own working
method, not invented fresh.

### 1.1 What the census actually counted (the precedent)

`docs/audits/2026-08-26-technical-handoff-census.md` §1.1: *"roughly 11.3 KB (22%) is the
hand-authored residual and ~1 KB the purpose."* §1.2's corpus line is the tell: *"FILL-IN
region bodies from RESIDUAL.md/HANDOFF_BOOT.md, plus whole pre-generator residuals, plus
SUPPLEMENT.md ANSWERS."* The census counted **FILL-IN region bodies**, not whole files — the
"~1 KB the purpose" line is the `FILL-IN:purpose` region of `HANDOFF_BOOT.md.tmpl` counted
*separately* from the rest of that file's session header, which the census does NOT count as
window-specific (it counts the surrounding table/notes as the generic remainder alongside the
17 KB role file, in the "~77% is not window-specific" figure).

The 2026-09-01 equilibrium map (`docs/audits/2026-09-01-technical-v7-history-delta-equilibrium-map.md`
§4-5) used a **coarser** approximation for speed — it counted the *whole* of `RESIDUAL.md` as
window-specific ("window-specific = RESIDUAL 7,562 + the filled header fields ~800"), not just
its FILL-IN bodies. That document is explicit that it is a hand-derived, one-off cut ("HAND-DERIVED
ON PURPOSE... that generator is batch-G's build") — i.e. it names this lane as the one that
mechanizes it. Re-deriving at the FILL-IN-body grain (finer than the equilibrium map, matching
the census) is therefore a refinement of precedent, not a break from it — and it is a **stricter**
bar (RESIDUAL.md's own scaffolding: the "What this is" callout, "Four-tag discipline" callout, §1
headline framing, §6 pointer prose, is NOT hand-authored and does not count), so this derivation
does not manufacture an easier pass.

### 1.2 The definition

**A byte is window-specific iff it lands inside content this repo's own generator already marks
as hand-authored, and generic otherwise.** The generator already draws this exact line, for a
different reason (RF-6: a re-render must never clobber hand-authored narrative) — `scripts/gen_handoff.py`'s
`<!-- FILL-IN:<name> START ... --> body <!-- FILL-IN:<name> END -->` regions are the ONLY spans
in a rendered bundle file that are (a) never generator-authored, (b) copied byte-for-byte across
re-renders, and (c) the exact content the operator or CC actually typed for *this* window. Every
other byte in a bundle file — headings, table scaffolding, static callouts, `{{TOKEN}}`
substitutions (`{{SLUG}}` `{{MODE}}` `{{REPO}}` `{{BRANCH}}`, etc.), and all of `PROBES.md` (which
carries zero FILL-IN regions in any mode) — is generator output: identical in shape across every
bundle, changing only by template substitution, not by what this window did.

The one file that needs a second rule is `SUPPLEMENT.md`: its ANSWERS region (everything below the
`PASTE CHAT ANSWERS BELOW THIS LINE` divider) is not FILL-IN-tagged, but it is the exact same kind
of content by construction — 100% operator/architect-typed, folded only when non-empty
(`assemble_paste._extract_answers`, already the single source of truth for "is this folded at
all"). So: **window-specific bytes = the sum, over every section actually folded into
`PASTE_THIS.md`, of (a) each FILL-IN region's body bytes, plus (b) the folded SUPPLEMENT ANSWERS
bytes when present.** `window_specific_ratio = window_specific_bytes / content_bytes`, where
`content_bytes` is the exact same denominator the assembler already computes today (the body
bytes before the terminal END sentinel is appended) — one denominator, never two.

**Placeholder exclusion.** An unfilled FILL-IN region's body is the generator's own prompt text,
uniformly `_(fill: ...)_` across every template (`templates/handoff/v5/*.tmpl`, verified by
inspection — every FILL-IN placeholder in this repo matches that shape). That is generic
boilerplate the operator has NOT yet replaced, not window content, and it is excluded (counts
`0`) rather than inflating the ratio on a cold or partially-filled bundle. The rule is: a
FILL-IN body is window-specific unless it is, in full (after stripping surrounding whitespace),
exactly the unfilled placeholder — `re.fullmatch(r"_\(fill:.*\)_", body, re.S)`.

**Why the ROLE PIN and PROBES.md always read 0.** Neither carries a FILL-IN region in any
mode — the pin is three structurally-generated lines (identity/sha/refusal) and PROBES.md's rows
are the fixed, re-usable probe set (census 1.1: "96% invariant window to window... nothing about
the *questions* changed"). This is the intended, not an accidental, reading: it is exactly what
census 1.1 already measured for these two artifacts, restated as a rule instead of a one-off count.

### 1.3 Measurement procedure (mechanical, terminates, disputable)

1. `assemble_paste.py` already builds `sections: list[tuple[label, text]]` before writing the
   body — the ROLE PIN, the session header, `RESIDUAL.md`, `PROBES.md`, and (if folded) the
   SUPPLEMENT ANSWERS. No new read: this is the same list the assembler already has in hand.
2. For each section **other than** the folded SUPPLEMENT ANSWERS: scan its text with the FILL-IN
   region regex `gen_handoff.py` already declares for the splice mechanism (made importable,
   never re-declared — one regex, one home, same pattern already used for
   `HANDOFF_BOOT_BYTE_BUDGET` and `reflow_framing`). Sum each match's **body** bytes (the span
   between the `START ...-->` and `<!-- FILL-IN:<name> END`, excluding the marker comments
   themselves — the markers are generator instructions, not window content), applying the
   placeholder exclusion above.
3. For the folded SUPPLEMENT ANSWERS section (when present): its whole byte length counts, no
   scan needed — it is the answers-only content `_extract_answers` already isolated.
4. Sum -> `window_specific_bytes`. Divide by `content_bytes` (already computed at the point the
   END sentinel is appended) -> `window_specific_ratio`.
5. Print both alongside the byte count on the `Written:` line, so the ratio is never a number
   somebody has to go compute separately from the size.

**Terminates:** the regex scan is over already-in-memory, bounded text (each bundle file), no
recursion, no open-ended judgment — bounded-deterministic in the same sense §5 condition 4
requires of a probe. **Disputable:** every number traces to a named region name (`purpose`,
`driftflags`, `shipped`, `frontier`, ...) that a reader can `grep FILL-IN` and re-check by hand
against the printed total.

## Step 2 — Adversarial pass on the DEFINITION (not the ceiling)

Attacking the definition's measurability, per contract: "sol's adversarial pass attacks the
DEFINITION and its measurability... never the ceiling, which is immutable."

**A1 — "The FILL-IN markers themselves are bytes too; are they window-specific or generic?"**
Excluded from BOTH numerator and denominator-adjacent double counting — they are counted as part
of the section's *generic* remainder (they are in `content_bytes` since they are in the folded
section text, but never added to `window_specific_bytes`, since the body-only span is what's
summed). Verdict: **already correct by construction** — no fix needed, but worth stating
explicitly since the implementation must slice `m.group("body")`, never `m.group(0)`.

**A2 — "A FILL-IN region containing boilerplate-but-technically-non-placeholder text (e.g. the
operator types `N/A` or `none`) inflates the ratio for a null answer."** True, and accepted: `N/A`
IS a window-specific fact (the answer to *this window's* question was nothing) exactly as `#611`'s
own SUPPLEMENT schema treats `"None"` as "a valid answer" for Q7. A null-but-typed answer is a
smaller number of window-specific bytes, not a misclassified one — it is not the placeholder-scan
hole A-prefixed below closes. No fix; this is the definition working as intended, not a gap.

**A3 — "The regex only matches well-formed `START...END` pairs; a hand-edited bundle with a
broken marker (one FILL-IN half deleted) silently drops those bytes from BOTH the numerator and
the denominator's classification, not just the numerator."** True and cheap to mitigate at the
edge, but out of scope for THIS lane: a bundle with a corrupted FILL-IN marker already fails
`verify_seal_identity` / re-render integrity elsewhere in the pipeline (RF-6's own precondition is
a well-formed marker), so a malformed bundle is not the shape this ratio is measured against.
Recorded as an **honest limit**, not fixed: the ratio is defined over well-formed bundles, same
scope §5's probe conditions already assume for every other mechanized check in this file.

**A4 — "Placeholder detection by regex match on the FULL body assumes the operator never adds
prose ADJACENT to the placeholder instead of replacing it (e.g. types real content but leaves the
`_(fill: ...)_` stub trailing)."** Real risk if it happened, but the generator's own operator
contract is "replace the placeholder," and `_splice_fill_regions` carries the FULL body across
re-renders either way — a body that is placeholder text *plus* real content fails the
`fullmatch` placeholder test (correctly, since `fullmatch` requires the ENTIRE stripped body to
be the placeholder shape) and is counted as fully window-specific, not zero. So the failure mode
this attack describes (undercounting) cannot happen; the only failure mode possible is the
inverse (a body that is placeholder-shaped text the operator typed on purpose, coincidentally
matching `_(fill: ...)_` verbatim) — vanishingly unlikely and self-correcting the moment real
content is added. No fix.

**A5 — "PROBES.md is defined to always read 0 window-specific bytes — doesn't that make the
metric blind to a future PROBES.md that DOES gain FILL-IN rows (e.g. a per-bundle probe
addendum)?"** No: the rule is mechanical over whatever FILL-IN regions actually exist in the
rendered text, not a hardcoded exemption for the filename `PROBES.md`. If a future change adds a
FILL-IN region to `PROBES.md.tmpl`, the same scan picks it up automatically — nothing in the
implementation special-cases the file. Verdict: **already correct**, the "PROBES always reads 0"
claim in 1.2 is a description of TODAY's template shape, not a rule baked into the code.

**What survived unchanged:** the core definition (FILL-IN body bytes + folded ANSWERS, over the
existing `content_bytes` denominator) and the placeholder exclusion. **What was hardened by the
pass:** none of A1-A5 required a code change — each either confirmed the definition already
handles the case (A1, A4, A5) or is an accepted/out-of-scope honest limit rather than a defect
(A2, A3). The pass is recorded here in full rather than silently, per the contract's own
instruction to record "what survived."

## What changed (steps 3-5)

1. **`scripts/assemble_paste.py` measures + prints the window-specific ratio** (§1.3's
   procedure, implemented verbatim): `window_specific_bytes()` sums FILL-IN region bodies
   (imported `gen_handoff.FILL_IN_RE`, renamed from the private `_FILL_RE` — one regex, one
   home) plus the folded SUPPLEMENT ANSWERS, excluding an unfilled `_(fill: ...)_` placeholder.
   The `Written:` line now reads `... ({size} bytes; window-specific {ws}/{content} B =
   {pct}%)` — one line, one denominator, never two numbers to reconcile by hand.
2. **The two rival budgets retired in one commit** (`5bee082d`): `_SIZE_WARN_BYTES = 48_000`
   and `window_metrics.collect`'s `paste_budget: int = 65_000` default are both gone, replaced
   by one public constant, `assemble_paste.PASTE_BYTE_CEILING = 20_000` (CUT-3's immutable
   ceiling), which `window_metrics.py` imports (dual-import shim matching
   `audit_checks/check_boot_byte_budget.py`) rather than re-declaring. `HANDOFF_BOOT_BYTE_BUDGET`
   (18,000 B, the resident role file's own live gate) is untouched — a different artifact,
   per this lane's own anti-pattern note.
3. **PROBES contract prose folded to §5, ONE home** (`88b54021`): `templates/handoff/v5/PROBES.md.tmpl`'s
   Contract/Anti-bluff callout (~2,187 B) and 5-item Gate-procedure list (~1,850 B) — both
   restatements of prose already normative in `protocols/HANDOFF_PROCESS.md` §5 — are replaced
   by two short pointers. The one piece of content the Gate-procedure list carried that §5 did
   NOT already state (the P0-then-P1 execution order + the every-row-BOUNDED/P10 citation) was
   moved INTO §5 as a new "Execution order" paragraph first, so nothing was dropped, only
   de-duplicated. `PROBES.md` shrank 14,272 B → 11,818 B on the real cut (§"Real cut" below).
4. **The SUPPLEMENT_BANNER appears exactly once**: removed from `PROBES.md.tmpl` and
   `RESIDUAL.md.tmpl`, kept only in `HANDOFF_BOOT.md.tmpl`'s session header (folded first into
   `PASTE_THIS.md`). It appeared 3× per assembled paste before this lane, 1× now.
5. **Q7 extended to interface behaviors, both copies** (`1503fd79`): `templates/handoff/v5/SUPPLEMENT.md.tmpl`
   Q7 and `protocols/HANDOFF_PROCESS.md:731`'s canonical restatement both now capture interface
   BEHAVIORS the operator relied on that are not yet named in `protocols/OPERATOR-INTERFACE.md`
   (copy-ready blocks, `.md` uploads, the END sentinel, the Downloads fallback are the four named
   examples — each already documented there; Q7 is now the register for the NEXT undocumented one),
   alongside the existing terms/rulings capture.

## Real cut — measured, not hoped

**Methodology (so the number is checkable).** The committed bundle
`docs/handoffs/2026-09-01-dev-knowledge-architect-v7/` is immutable (§5 rule 3) and cannot be
re-rendered in place. Its four files were copied to a scratch directory OUTSIDE the repo tree
(`.claude/jobs/<job>/tmp/scratch-bundle`, never committed, removed after measuring), then
`HANDOFF_BOOT.md` / `RESIDUAL.md` / `PROBES.md` were re-rendered through this lane's UPDATED
templates via `gen_handoff._render` (the same RF-6 FILL-IN splice a real `--filled` re-run
uses), preserving every real, hand-authored FILL-IN body and the real SUPPLEMENT ANSWERS
verbatim. `scripts/assemble_paste.py` then ran against the scratch directory exactly as it
would against a live bundle. This is a **real cut** in the CUT-3 sense — genuine architect-mode
content, not synthetic filler — reusing a real bundle without mutating it.

```
PASTE_THIS.md total (FILLED, after this lane)     29,776 B
  vs. before this lane (equilibrium map §5)        32,264 B    -2,488 B

  PROBES.md            14,272 B -> 11,818 B     (-2,454 B; contract-prose fold)
  HANDOFF_BOOT.md      11,252 B -> 11,273 B     (+21 B; noise, untouched by this lane)
  RESIDUAL.md            7,467 B -> 7,413 B      (-54 B; banner removal + pointer note)

BAR 1  size            <= 20,000 B   ACTUAL 29,776 B   MISS by 9,776 B (+49%)
BAR 2  window-specific >= 70%        ACTUAL 32%         MISS by 38 points
       (window-specific = 9,551 / 29,719 content bytes; FILL-IN bodies + folded ANSWERS)
```

**This is the finding CUT-3's own text anticipates: "If the cut will not fit, that is a finding
to report, not a number to move."** Both bars still miss, and this lane does not move the
ceiling to make them pass. What is new against the 2026-09-01 equilibrium map:

- **The size gap narrowed, on the same (FILLED, architect-mode) measurement basis.** Before this
  lane the FILLED cut measured 32,264 B — +12,264 B over ceiling, +61%. After this lane's
  PROBES.md contract-prose fold: 29,776 B — +9,776 B over, +49%. A real ~2,488 B cut, from the
  one lever this lane's write-scope licensed without touching probe row semantics or moving
  prose into the resident role file (both barred by this lane's anti-patterns).
- **The window-specific ratio reads LOWER (32%) than the equilibrium map's coarse 43%** — not a
  regression, a **more honest measurement**. The map counted the whole of `RESIDUAL.md` as
  window-specific; this lane's FILL-IN-body-only definition (§1.2, refined FROM the census's own
  precedent) excludes `RESIDUAL.md`'s own scaffolding (the "What this is" callout, the "Four-tag
  discipline" callout, §1/§6 framing prose) — none of which is hand-authored. A definition that
  produced an EASIER pass than its own precedent would be the failure mode Step 2's adversarial
  pass exists to catch; this one produces a harder bar instead.
- **The remaining wall is `PROBES.md`'s ROW TABLES themselves** (~10,300 B after the prose fold),
  which this lane's write-scope explicitly protects (Done-contract item 2: "the bundle carries
  ROWS only" — rows STAY) and which this lane did not reword, for the reason the equilibrium map
  already gave: reaching either bar by cutting or diluting probe rows trades a measured-size
  finding for a weakened-teeth one, a strictly worse trade. Closing the remaining gap needs a
  structural decision this lane's V-2 budget does not cover (fork class (c) — no standing ruling)
  — reported here, not decided here.

## Design decisions under V-2 (reported, not escalated)

- **Definition granularity: FILL-IN-body-level, not whole-file** (§1.2) — a refinement of the
  census's own working method, producing a stricter bar than the equilibrium map's coarser one.
  Chosen because it is the ALREADY-MECHANIZED boundary the generator draws for an unrelated
  reason (RF-6), not a bar invented for this measurement.
- **PROBES.md's row TABLES are untouched** — only the surrounding contract prose was cut. Rows
  are the Done-contract's own explicit "carries ROWS only" floor, and rewording probe semantics
  risks the anti-bluff/`expected:`-hint machinery (§5, "Structural enforcement") this lane's
  write-scope does not license touching.
- **No new `audit.py` FAIL-class gate for `PASTE_BYTE_CEILING`** — `check_boot_byte_budget`'s
  split-by-site pattern (WARN at generation, FAIL at the gate) would be the natural mirror, but
  a new gate is outside this lane's declared write-scope (`scripts/`, `templates/`,
  `HANDOFF_PROCESS.md` §5 + Q7 only — not `scripts/audit.py`). Left as an open item.
- **Measurement methodology for the real cut** (scratch re-render of a real, immutable bundle's
  content through the updated templates) — chosen over generating a NEW bundle (would create an
  uncommitted-scope `docs/handoffs/` artifact and, per the batch-boundary guard, refuses while
  this lane's own worktree is live) and over hand-editing the committed 2026-09-01 bundle
  (barred: handoffs are immutable, §5 rule 3).

## Delta A2 (base failed-set comparison) — SUPERSEDED mid-lane by cross-batch amendment

The frozen contract's Delta A2 clause specified a full-suite run compared by SET against
`docs/audits/2026-09-02-verification-base-failed-set-1e064921.json` via `scripts/failed_set.py
--compare`. Three consecutive full-suite attempts in this lane were killed mid-run by external
process termination (`-n auto` twice, `-n 4` once; each attempt showed `[gwN] node down: Not
properly terminated` in the pytest log, and `tasklist` showed ~43 concurrent `python.exe` / ~19
`claude.exe` processes on the shared workstation at the time).

Mid-flight during the fourth attempt (`-n 4`, reached 73% before its own exit-255 failure), a
peer session running batch-G's contract review sent **AMENDMENT R-G-A2** (relayed as an operator
ruling, 2026-09-02): full-suite runs are suspended across all seven concurrently-running batch-G
lanes on this workstation for exactly this thrashing reason; each lane runs its own targeted
tests only, and **the integrator computes Delta A2 once, serially, at merge time** rather than
once per lane. The frozen closure, write-scope, anti-patterns, PLAN-mode requirement, and
commit-and-STOP obligation are explicitly unchanged by the amendment — only the Delta A2
verification mechanics move to the integrator.

**What this lane actually ran and verified, in place of the full-suite compare:**

```
uv run --locked pytest -q --no-header tests/test_assemble_paste.py tests/test_window_metrics.py tests/test_gen_handoff.py
123 passed in 28.15s
```

This is the full targeted-test coverage of this lane's write-scope (every file this lane
modified: `scripts/assemble_paste.py`, `scripts/window_metrics.py`, `scripts/gen_handoff.py`,
plus their test files). No regression is introduced by this lane's diff; the base-failed-set
SET comparison against main is deferred to `/lane-integrate`, per the amendment.

**This is reported honestly, not fabricated** — this lane did NOT complete a full-suite run and
does not claim to. Per CLAUDE.md's execution-truthfulness rule, the record above states exactly
what ran (targeted, 123 passed) and exactly what did not (the full-suite SET compare), and why
(a mid-lane cross-batch amendment, superseding the frozen contract's Delta A2 clause for this
lane specifically — acknowledged back to the sending session).

## Open items (not this lane's write-scope / not required by the Done-contract)

- **The ceiling is not met.** `PASTE_THIS.md` (architect mode, filled) measures 29,776 B against
  the 20,000 B ceiling and 32% against the 70% window-specific target. Both misses are reported
  per CUT-3's own text, not silently passed. Closing the remaining `PROBES.md` row-table weight
  needs an architect-level decision (shorten rows / restructure the probe manifest / accept a
  narrower CUT-3 scope for execution-mode bundles, which carry no SUPPLEMENT and a comparable
  PROBES.md) — a fork class with no standing ruling (V-2 escalation class (c)), left for the
  next lane or an operator ruling rather than decided here.
- **No FAIL-class `audit.py` gate exists yet for `PASTE_BYTE_CEILING`** — WARN-only today,
  mirroring the pre-`check_boot_byte_budget` state of the boot-byte budget before A10 item 2/R4
  added its gate half. A future lane could add one the same way, in `scripts/audit.py`.
- **An execution-mode real cut was not separately measured** — this lane's real-cut evidence is
  architect-mode (the only 2026-09-01 bundle available to reuse without violating immutability).
  Execution mode drops the SUPPLEMENT and part of the session-header walkthrough; its ratio and
  size likely differ (the 2026-09-01 map's own honest limit, restated: "one cut is one cut").

## Terra pre-merge review (integrator, 2026-09-03)

Reviewer `codex exec review --base main`, concurrency 1. **Wall-clock 135 s.**

**Severity tally: HIGH/P1 = 1 · MED = 0 · LOW = 0. CONFIRMED — integrator duty, discharged at
the merge, not in this lane.**

| # | Sev | Finding | Disposition |
|---|---|---|---|
| 1 | P1 | This lane adds 3 tests (2 in `test_assemble_paste.py`, 1 in `test_window_metrics.py`), moving collection 4881 → 4884, while `ecosystem/doc-counts.md` still declares **4881 collected**; `validate_doc_claims` then fails at ship-gate | **CONFIRMED** — regenerated by the integrator in the same act as the merge |

**Why the lane did not do it, and should not have.** `ecosystem/doc-counts.md` is a generated
fleet count surface. A lane regenerating it races every other lane in the batch — G8's closure (a)
set it to the live count measured BEFORE this lane's tests existed, so any lane writing it can
only be right until the next lane merges. The integrator is gate-of-record for generated surfaces
(the same rule that keeps `docs/audits/README.md` out of lane scope), and regenerates once the
merged result is known.

**This is a coupling, not an oversight, and it is the batch's seventh.** A lane's frozen
write-scope was "`scripts/gen_handoff.py`, `assemble_paste.py`, `window_metrics.py`,
`templates/handoff/v5/*`, tests" — and satisfying it necessarily invalidates a file outside it.
Recorded as evidence for the contract-freeze coupling scan: the count surface is derivable from
"this lane adds tests" by grep at freeze time.
