# Codex Review — lane-290-floor-teeth

**Date:** 2026-08-08
**Branch:** `worktree-lane-290-floor-teeth`
**HEAD:** `8969ba2f`
**Diff range:** `main..worktree-lane-290-floor-teeth`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/0/0/0 <!-- Critical/High/Medium/Low — the FINAL (pass-15) verdict on the shipped diff, counted from the Findings section below, which is empty. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Loop tally — 15 passes over the same diff

This artifact holds the **final** pass. The 0/0/0/0 above is the shipped diff's verdict, not the
loop's cost: this file was overwritten by each `-Force` re-run, so the per-pass findings live in
the commit messages that fixed them (`git log main..HEAD`), each naming its pass number.

| Pass | HEAD reviewed | C | H | Disposition |
|---|---|---|---|---|
| 1 | `5abc96a9` | 1 | 1 | HIGH fixed (`install-hooks -t …` read fully armed); CRITICAL (D9) refuted |
| 2 | `6a0b53b1` | 2 | 1 | all 3 fixed (command position · newline boundary · shell quoting); D9 re-raised, refuted again |
| 3 | `0be4df56` | 1 | 3 | all 4 fixed (runner-prefix word bag · `-t=X` · line continuation · case-sensitive `.EXE`); **D9 withdrawn by the reviewer** |
| 4 | `bd818c09` | 1 | 0 | fixed (an argparse-rejecting invocation credited with its valid flags); `_ensure_settings` + `_host_group` cleared by the reviewer |
| 5 | `d6f3fdb3` | 0 | 1 | fixed (`-t==X` via an over-greedy `lstrip`); also corrected this addendum's own stale test count |
| 6 | `3c3ac7df` | 2 | 0 | 1 fixed (`--help` / unknown option / positional); 1 refuted (`&&` reachability — not statically decidable) |
| 7 | `e09d5606` | 0 | 1 | fixed (`--color` not choices-validated) |
| 8 | `1c481df6` | 0 | 1 | fixed (long-option abbreviations rejected — first FALSE-UNARMED) |
| 9 | `836f6f42` | 0 | 3 | all 3 fixed, and the hand-rolled flag walk **replaced by argparse itself** |
| 10 | `523f0c86` | 0 | 2 | both fixed (`exec` prefix · POSIX continuation deleting rather than spacing) |
| 11 | `349433a4` | 0 | 1 | fixed (dangling redirection = shell syntax error) |
| 12 | `70f2ec53` | 0 | 1 | fixed as a family (operator in redirection-target position) |
| 13 | `9b9800b1` | 0 | 1 | fixed (`env -u` — reviewer-classified as *not* a punctuation variant) |
| 14 | `8969ba2f` | 0 | 1 | fixed (`env -0` refuses a command, so it arms nothing) |
| 15 | this file | 0 | 0 | **CLEAN** — no category (a) defect, no reportable (b) residue |

**Totals across the loop: 7 Critical · 17 High · 0 Medium · 0 Low.** 21 accepted and fixed, 3
refuted with reasons (D9 twice, then withdrawn by the reviewer; `&&` reachability once). Every
accepted finding was one shape — a command that pre-commit or the shell would reject, or never
reach, read as **fully armed** — i.e. the false `PRESENT_CORRECT` that [#290] exists to close,
reachable through the new teeth themselves. Two of the fixes corrected **my own wrong test
assumptions** (a trailing `-t` does not fall back to the default stage; `exec` is not an
incomplete runner prefix), and one corrected a **regression I introduced** mid-loop (posix
lexing mangling Windows paths), each caught before commit.

**Stopping condition**, stated rather than assumed: pass 15 returned zero findings AND the
reviewer explicitly agreed with the reasoning for stopping on a category-(b) residue — the
carrier writes the canonical arm command itself, so the only foreign input is a hand-edited
`settings.json`, and anything the parser cannot establish already fails **safe** (reads as no
arm leg, so `apply` adds a canonical leg beside it and never rewrites what it could not parse).

---

## Focus

Pass 15, and I intend this to be the last unless you surface a category (a) defect.

Fourteen passes. Pass 14's nv -0 is fixed (it left the skippable set, so it now falls through to unarmed - the safe direction). You classified that one yourself as category (b).

Settled, do NOT re-raise: D9; _ensure_settings / _host_group; && control-flow reachability; -c/--config path existence.

Answer these two things first, plainly, before any findings:
1. CLEAN or NOT CLEAN.
2. Whether anything remaining is category (a) - a form a real consumer's settings.json could plausibly contain, which I will fix - or only category (b) - malformed shell punctuation, or another wrapper CLI's option semantics needing to be modelled, which I will record as a stated limit.

My reasoning for stopping on (b): the carrier WRITES the canonical arm command itself, so the only foreign input is a hand-edited settings.json; and for anything the parser cannot establish, the safe direction already holds - it reads as no arm leg, so apply ADDS a canonical leg beside it and never rewrites what it could not parse. A (b) residue is therefore a fuzzing surface, not a consumer risk. Tell me if you disagree with that reasoning, and why.

Report ONLY demonstrable findings with a concrete input and wrong outcome.

---

## Findings
CLEAN.

No remaining category (a) defect found. I agree with your reasoning: unrecognised/opaque commands fail safe as unarmed, and `apply` adds the canonical leg without rewriting them. I found no demonstrable category (b) residue worth reporting.

## Critical

(none)

## High

(none)

## Medium

(none)

## Low

(none)