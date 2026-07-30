---
class: qa
date: 2026-07-30
slug: assemble-paste-test-gap-review
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-2026-07-30-boot-prep
anchor_sha: c8490c1d
consumer: incoming 2026-07-31 dev-knowledge architect boot
consumption_path: "branch -> local re-verification -> architect reads at boot"
scope: "read-only adversarial review of the assemble_paste surfaces landed in 3cd4417a + e0528cc3; NO test code committed to canon paths"
---

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Cloud night-batch lane: no merge, no
> canon edit, no closure, no ruling. Proposed test names are proposals only — no test code was
> written into `tests/`. Every `file:line` is **re-verify-at-ruling** against base `c8490c1d`.
>
> **Consumer:** incoming 2026-07-31 dev-knowledge architect boot.
> **Consumption path:** branch -> local re-verification -> architect reads at boot.


# Adversarial test-gap review — `scripts/assemble_paste.py` (3cd4417a + e0528cc3)

Repo: `C:\Users\1028120\Documents\Dev\.dev-knowledge`, branch `claude/night-2026-07-30-boot-prep`
(not switched, not committed to; only write is this file).

## What landed (from `git show`)

**3cd4417a** — `scripts/assemble_paste.py` (+29), `tests/test_assemble_paste.py` (+78/-5, net
**4 new test functions**: `test_end_sentinel_terminal_with_count_and_bytes`,
`test_end_sentinel_not_a_section`, `test_promotion_debt_block_on_ruling_bearing_answers`,
`test_no_promotion_debt_block_without_markers` — plus edits to the pre-existing
`test_all_sections_in_order` / `_labels()` helper to account for the new sentinel line).
Commit message claims "6 tests"; the diff shows 4 new test functions. Not chased further —
noted as a discrepancy, not a code defect.

**e0528cc3** — `scripts/assemble_paste.py` (+2/-1) only appends a clause to the existing
over-budget warn string. **Zero test-file changes** in this commit — confirmed via
`git show e0528cc3 --stat` (only `ESSENTIALS.md`, `HANDOFF_PROCESS.md`,
`scripts/assemble_paste.py` touched).

Full read of `scripts/assemble_paste.py` (197 lines) and `tests/test_assemble_paste.py`
(472 lines, 18 test functions total) done. `grep` across `tests/` and `scripts/` for
`END OF PASTE|promotion-debt|_SIZE_WARN_BYTES|assemble_paste` found no other test file
touching these three surfaces (only `tests/test_gen_handoff.py` references `assemble_paste`
by name, unrelated to these surfaces).

---

## CONFIRMED gaps (verified by reading code + executing read-only probes in scratchpad)

### G1 — Plural "rulings" bypasses the PROMOTION-DEBT regex entirely
- **File:line:** `scripts/assemble_paste.py:37` — `_PROMOTION_DEBT_RE = re.compile(r"(?i)\b(?:BINDING|do not relitigate|MUST NOT|ruling)\b")`
- **Why:** `\bruling\b` requires a word boundary after "ruling"; in "rulings" the following
  character is `s` (a word char), so there is no boundary there and the whole word fails to
  match. Only the *singular* "ruling" is caught.
- **Executed probe (scratchpad `probe_assemble.py`, `p_rulings_plural`):** ANSWERS =
  `"Prior rulings apply here.\nBINDING: x.\n"` → observed stderr:
  `[promotion-debt] 1 ruling-bearing line(s)` listing only `BINDING: x.` — the "Prior rulings
  apply here." line was silently **not** flagged.
- **Rank: HIGH** — a ruling-bearing ANSWERS line using the natural plural silently skips the
  advisory that exists specifically to catch stranded rulings (BW-h / intake #18 A8); nothing
  downstream signals the miss.
- **Proposed test name:** `test_promotion_debt_plural_rulings_line_is_missed` (write it as an
  xfail/regression-documenting test, or fix the regex to `ruling(?:s)?` and assert the fixed
  behavior — either way it is currently uncovered in both directions).

### G2 — Boundary arithmetic on the size WARN (`>` vs `>=`) is never exercised at the threshold
- **File:line:** `scripts/assemble_paste.py:189` — `if size > _SIZE_WARN_BYTES:`
- **Existing tests** (`test_normal_bundle_surfaces_size_without_warn`,
  `test_oversized_paste_emits_size_warn`) only probe "small" and "way over (~12000×8 bytes
  padding)" — neither exercises `size == _SIZE_WARN_BYTES` exactly, nor `±1` byte.
- **Executed probe (`p_boundary_at_budget`, binary-search to hit exact byte counts):**
  observed `size=64999` → warn **False**; `size=65000` (exactly at budget) → warn **False**;
  `size=65001` → warn **True**. This confirms the comparison is strict `>` (not a defect by
  itself — this IS the coded behavior) but the exact-at-budget behavior is **not asserted by
  any test**, so a future edit flipping `>` to `>=` (or vice versa) would pass the whole suite.
- **Rank: MEDIUM** — visible-but-unpinned; a silent flip changes WARN posture at exactly the
  documented "healthy paste" ceiling with nothing to catch it.
- **Proposed test names:** `test_size_warn_boundary_exactly_at_threshold_no_warn`,
  `test_size_warn_boundary_one_byte_over_threshold_warns`.

### G3 — The A2 over-budget clause text ("artifacts other than PASTE_THIS must not be pasted
at all") shipped with zero test coverage
- **File:line:** `scripts/assemble_paste.py:190-192`, the string appended in `e0528cc3`.
- `test_oversized_paste_emits_size_warn` (unchanged since before e0528cc3) asserts only
  `"[warn]"` and `"heavy boot"` in stderr — never the new A2 clause. Confirmed by re-reading
  the full test at `tests/test_assemble_paste.py:391-400` and confirming `git show e0528cc3
  --stat` touched no test file.
- **Rank: MEDIUM** — the message still prints (not silently dropped today), but a later edit
  that mangles/removes the A2 sentence would ship green.
- **Proposed test name:** `test_oversized_paste_warn_includes_a2_transport_clause`.

### G4 — Two-different-byte-counts confusion: "Written: N bytes" (post-sentinel, used for the
WARN) vs the sentinel's own embedded byte count (pre-sentinel, by design) are never compared
in a test, and the delta is unpinned
- **File:line:** `scripts/assemble_paste.py:182-192` — `content_bytes` is computed on `body`
  *before* the sentinel is appended (used inside the sentinel string); `size` is computed on
  `body` *after* appending the sentinel (used for `Written:` stdout and the WARN comparison).
  These are two different numbers by design (the docstring comment explains why), but nothing
  asserts their relationship.
- **Executed probe:** a clean run printed `Written: ...\PASTE_THIS.md (412 bytes)` while the
  sentinel line embedded `357 bytes` — a 55-byte gap (the separator + sentinel-text-minus-
  count-digits). Test 15 (`test_end_sentinel_terminal_with_count_and_bytes`) only checks the
  sentinel's own internal consistency (`body_before` bytes == embedded count); it never checks
  against the `Written:` stdout number, so a reader who diffs the two numbers has no test
  telling them that's expected.
- **Rank: LOW/MEDIUM** — cosmetic confusion, not wrong data, but exactly the kind of "two
  numbers on screen disagree" report Rob would flag; currently undocumented in test form.
- **Proposed test name:** `test_written_stdout_bytes_exceeds_sentinel_content_bytes_by_separator_length`.

### G5 — A BOM in a required source file leaks byte-for-byte into `PASTE_THIS.md`, untested
- **File:line:** `scripts/assemble_paste.py:152` — `path.read_text(encoding="utf-8")` (not
  `"utf-8-sig"`) on `protocols/HANDOFF_BOOT.md` / bundle sources.
- **Executed probe (`p_bom_leak`):** wrote `protocols/HANDOFF_BOOT.md` with a UTF-8 BOM
  prefix; observed the 3-byte BOM (`\xef\xbb\xbf`) present verbatim in the written
  `PASTE_THIS.md`. The sentinel's byte count stayed **internally consistent** (355/355,
  matches), so this is not a miscount — it's an invisible stray character silently riding
  into the browser paste.
- **Rank: MEDIUM** — self-consistent counts mask that the leaked BOM is undesirable content
  reaching the browser; no test would catch a Windows-tool-authored source file regressing
  this.
- **Proposed test name:** `test_bom_prefixed_source_leaks_into_paste_untested_today` (or, if a
  fix is wanted: switch to `"utf-8-sig"` and add `test_bom_prefixed_source_is_stripped`).

---

## Checked and RULED OUT (verified via probe — reported honestly rather than padded as gaps)

- **CRLF survival:** probed a RESIDUAL.md written with `\r\n` line endings — `Path.read_text()`
  applies universal-newline translation by default, and the sentinel/body are written back
  with `newline="\n"`. Observed: **no `\r\n` in the output file.** Not a live gap despite being
  a plausible Windows risk — ruled out empirically, not just by reading.
- **Fake/spoofed "END OF PASTE" text embedded in operator-pasted ANSWERS:** probed ANSWERS
  containing a fabricated `=== END OF PASTE — 99 sections · 12345 bytes ===` line mid-content.
  The real terminal line (last line of the file) is still correctly the genuine sentinel and
  still parses correctly — `splitlines()[-1]`-style consumption (as the truncation-rule text
  in `protocols/HANDOFF_BOOT.md` prescribes: "the paste's terminal ... line") is unaffected.
  The substring `"=== END OF PASTE"` does appear **twice** in the file, which is a risk only
  for a naive substring-search consumer, not for one that follows the documented "terminal
  line" rule — noted as a **SUSPECTED, low-severity** doc-adherence risk, not a code defect
  (no test exercises it either way, but severity is low since correctness holds under the
  documented reading procedure).
- **Idempotence of the PROMOTION-DEBT block across re-runs:** probed two consecutive runs on a
  bundle with ruling-bearing ANSWERS. Observed 1 `[promotion-debt]` block per run (no
  doubling/accumulation) and byte-identical `PASTE_THIS.md` across a 3rd re-run. Behavior is
  correct today; still worth a regression test since `test_regeneration_is_byte_identical`
  (the existing idempotence test) uses a marker-free supplement, so it does not exercise this
  path at all — see proposed test list below.
- **Session-header section correctly excluded when boot content has no pre-`## ` prefix:**
  probed a bundle `HANDOFF_BOOT.md` starting immediately with `## `. Sentinel correctly
  reported `n=4` (excluding the empty header) and the header label was absent from the paste.
  Correct today, but this specific input combination is not exercised by any existing test —
  see proposed test list.
- **Empty-but-present required section:** probed `RESIDUAL.md` with empty content. It is still
  appended as a section (label present, sentinel `n=5`, i.e. counted). Correct today, matches
  the code's unconditional-append-on-exists behavior; untested combination.
- **Zero-section / single-section paste:** structurally impossible under the current script —
  the 3 required sources (`protocols/HANDOFF_BOOT.md`, `RESIDUAL.md`, `PROBES.md`) are always
  appended or the process exits(1) before any file is written (covered by existing Test 3), so
  `n` is always ≥3. Not a live gap; ruled out by reading the control flow, not executed
  (execution would just re-confirm the existing exit-nonzero test).
- **Byte vs character count for non-ASCII content:** read the code — `content_bytes` and
  `size` are both computed via `.encode("utf-8")`, i.e. genuine UTF-8 byte counts, not
  `len()` on the `str` (which would be character count). This is correct as implemented; not
  a gap. (Did not additionally probe with non-ASCII content since the code path is a single
  unconditional `.encode("utf-8")` call with no branch that could diverge — reading was
  sufficient here.)

## SUSPECTED (not executed, lower confidence — listed separately per instructions)

- The `_PROMOTION_DEBT_RE` phrase `"MUST NOT"` is a literal two-token phrase; text wrapped
  across a line break or with irregular whitespace ("MUST\nNOT", "MUST  NOT") would not match.
  Plausible but not probed — flagging as SUSPECTED, LOW rank (unusual operator input).
- `"ruling"` as a bare dictionary word (e.g. a folded ANSWERS line describing an unrelated
  "court ruling") would false-positive the advisory. This is a design/precision trade-off, not
  a code bug, and is genuinely hard to "fix" without narrowing the heuristic — flagging as
  SUSPECTED noise risk, not a defect, no test proposed.

---

## Proposed test names (flat list)

```
test_promotion_debt_plural_rulings_line_is_missed
test_size_warn_boundary_exactly_at_threshold_no_warn
test_size_warn_boundary_one_byte_over_threshold_warns
test_oversized_paste_warn_includes_a2_transport_clause
test_written_stdout_bytes_exceeds_sentinel_content_bytes_by_separator_length
test_bom_prefixed_source_leaks_into_paste_untested_today
test_regeneration_with_ruling_bearing_answers_does_not_double_promotion_debt
test_session_header_excluded_when_boot_has_no_pre_heading_prefix
test_empty_but_present_required_section_still_counted_in_sentinel
```

---

## Discipline notes

- Every CONFIRMED gap above (G1-G5) was verified by an executed, read-only probe script run
  from the scratchpad temp dir (`probe_assemble.py`, copies `scripts/assemble_paste.py` +
  `scripts/gen_handoff.py` into a `tempfile.TemporaryDirectory()` exactly like the existing
  test harness's `_make_bundle` does) — no repo file was written to, no branch was switched,
  nothing was committed.
- The "Checked and RULED OUT" section exists specifically so this list isn't padded — three of
  the prompt's suggested risk areas (CRLF, sentinel-spoofing, byte-vs-char) were probed or
  read and found NOT to be live defects, and are reported as such rather than silently
  dropped or reframed as gaps.
- Commit-message/diff discrepancy ("6 tests" claimed in 3cd4417a, 4 new test functions
  observed) is noted above under "What landed" — not a code defect, just an accounting
  mismatch worth flagging.
