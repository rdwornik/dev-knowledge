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

## Step 3 onward

See "What changed" below for the implementation, the retired/re-pointed budgets, the PROBES fold,
the Q7 extension, and the final real-cut measurement.
