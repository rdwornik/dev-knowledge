# Codex Review — lane-handoff-probes-5b5r-6b-repair-1

**Date:** 2026-09-29
**Branch:** `worktree-lane-handoff-probes`
**HEAD:** `8809e7ab`
**Diff range:** `origin/main...HEAD` (`ca5d057a..8809e7ab`)
**Codex version:** n/a — SUBSTITUTION, see below
**Mode:** diff-review
**Tally:** 0/0/1/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gemini-3.1-pro-high` via `agy` (**SUBSTITUTION** for `gpt-5.6-terra` — Codex
usage limit hit, reset stated as 8:57 AM local; common rules §5 / ruling (e): "At the Codex
usage limit the review waits for the stated reset or falls back to Gemini (`agy`), recorded
as a SUBSTITUTION." Reachability checked first (`agy -p "Reply with exactly: OK"` → `OK`).
Because `agy --print` rejects a single argument over the Windows command-line length limit
(the diff is ~51 KB; `agy.exe: Argument list too long`), the diff was sent across 3
`-c`-continued turns of a single conversation, each instructed only to `ACK` until the final
turn asked for the review — session id `99ca5f41-46f0-438e-ae9a-0244d02446e1`... (turn 1
established a fresh conversation; see raw turns under this lane's job tmp,
`~/.claude/jobs/d579373e/tmp/repair1-agy-turn{1,2,3}.txt`).**
**Review profile:** code

---

## Focus

consumer: the frozen contract `H:\My Drive\CLAUDE PROMPT DIR\LANE-5B5R-6b-handoff-probes.md`,
repair 1, per `H:\My Drive\CLAUDE PROMPT DIR\to-browser\REFUSED-lane-handoff-probes.md`

This is repair 1 of lane-handoff-probes (LANE-5B5R-6b-handoff-probes), fixing the two HIGH
findings the integrator's REFUSED file said were declined instead of fixed in the prior
follow-up review (`2026-09-29-codex-lane-handoff-probes-5b5r-6b-followup.md`, kept under this
lane's job tmp, never committed — that file predates this lane owning `docs/audits/`):

1. `verify_handoff_probes.py:450` (Git fallback marks non-runnable probe commands as
   available) — fixed via option (a): a new `_exe_fallback_path()` helper, read only at the
   probe call site, makes a `pass` that rests on the Git-for-Windows `usr/bin` fallback say so
   in its detail (`"binds to live state (resolved via Git-for-Windows usr/bin: <path>)"`)
   instead of reading identically to an ordinary PATH hit. A tool absent from both PATH and
   the fallback still reads `skipped`
   (`test_a_grep_led_probe_absent_from_both_path_and_fallback_still_skips` exercises the real
   `_exe_available`/`_git_bundled_tool` chain, nothing mocked at the `_exe_available` level).
2. `verify_handoff_probes.py:1436` (eight-character session prefixes are not identities) —
   fixed inside `_rule_bd_seats`'s own comparator (`verify_handoff_probes.py`, never
   `seat_registry._label`): live sessions are now counted per 8-char prefix, and a cut-named
   wedged/starved prefix that matches more than one live session FAILs as ambiguous instead
   of being treated as resolvable. New regression test:
   `test_bd_seats_fails_when_a_named_prefix_is_ambiguous_among_live_sessions`.

Asked to verify both fixes are correct and complete on their own terms, that neither
introduces a new false-pass or false-fail path, and to re-check the rest of the diff (BD-seats
identity/liveness, capability status-column header mapping, Windows tool-absent fallback) for
anything two prior review rounds could have missed.

---

## Findings

## Critical

(none)

## High

(none)

## Medium

- `verify_handoff_probes.py:1494` (approx, pre-fix line) — `_rule_bd_seats` passed the raw
  rendered `value` parameter (carrying the ` — evidence: ... [FRESHNESS]` tail) to
  `_sr.named_bad_seats(value)`, while correctly passing the unrendered `fresh.value` for the
  live side. **Why:** `named_bad_seats` is designed to parse the underlying
  `seat_health_line`, not a rendered `StateRow` string; passing the rendered string worked
  only by coincidence (the last named segment's lazy regex match absorbs the tail, and
  splitting on the first `" ("` happens to discard it), which is fragile string-splitting
  behavior the parser was never designed to rely on. **Fix direction:** pass `underlying`
  (already extracted by the tail-stripping regex a few lines earlier) instead of `value`.

## Low

(none)

The rendered-tail stripping, the fallback-detail wording, and the ambiguous-prefix rejection
are each correct and complete on their own terms; no new false-pass or false-fail path found
in the re-check of BD-seats identity/liveness, the capability status-column mapping, or the
Windows tool-absent fallback.

---

## Disposition

`DECIDED-BY-LANE: the Medium above is not a P1 (this batch counts P1 as Critical+High only,
per the integrator's own REFUSED-lane-handoff-probes.md item citing sibling lane L4) -> fixed
anyway rather than merely recorded, since it was a one-line, low-risk, RED-first-verified
change (commit fe6b859d) -> ruling (e) only REQUIRES fixing P1 and recording the rest, and
fixing a trivial, already-diagnosed correctness gap while the diff is open costs less than
carrying it forward as a ROWS-OWED line.` Fixed in commit `fe6b859d`, RED-first
(`test_bd_seats_uses_the_tail_stripped_value_not_the_rendered_string_for_named_seats`, shown
failing against the pre-fix code via the stash protocol before the fix landed, then passing).
