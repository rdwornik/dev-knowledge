---
name: preflight
description: Verify every repo locator a contract or prompt cites — file:line, headings, SHAs, [#id] liveness — BEFORE acting on it. Read-only, adoption-first, wired into no gate.
---

# /preflight — check a contract's locators before you act on one

```bash
uv run --locked python scripts/preflight_contract.py <contract-or-prompt-file>
```

Add `--repo-root <path>` to verify against a different checkout.

## Why

Nine architect premise errors landed in the 2026-08-03/04 window and every one was caught
downstream by accident — three arcs in, by a human re-deriving a number a machine could have
checked in a second. Four were pure locator claims:

- `len(ALL_CHECKS)` "stays 38" — live 39
- the ALL_CHECKS registration "at `scripts/audit.py:3381`" — live 3429
- an AC's `38 -> 37` arithmetic — live `39 -> 38`
- "five consumer dailies for 2026-08-02" — the tree tops out at 2026-07-31

The cost was never that a frozen contract was wrong; the ex-ante rule already says report the
discrepancy rather than edit it. The cost was **when** it surfaced.

## What it checks

| kind | form | verified |
|---|---|---|
| `file-line` | `` `path/file.py:123` `` | file resolves (repo root, then `scripts/`, `deploy/`, `tests/`, `protocols/`, `docs/`) and has ≥ 123 lines |
| `heading` | `` `FILE.md` `` heading `"..."` | the heading text occurs in that file |
| `sha` | `` `abc1234` `` | reachable in this repo's history |
| `backlog-id` | `[#123]` | currently OPEN in `BACKLOG.md` |

## What it does NOT check — read a PASS narrowly

- **Whether a citation points at the *right* line.** `:3381` and `:3429` are both real lines in
  a 3800-line file, so the very error that motivated this tool would *not* have been caught by
  it. It catches the coarser class: a line past EOF, a path that does not exist.
- **Reasoning.** Two of the nine were an internal contradiction and an unmet precondition;
  neither is a locator, and neither is reachable from here.
- A PASS means *every locator resolves*, never *the contract is correct*.

## Exit codes

- `0` every extracted claim resolved
- `1` at least one did not — each named with the live value
- `2` internal error / the contract could not be read. **Fail-closed**, the
  `check_seal_identity` posture: an error is never a silent pass, and `2` stays distinct from
  `1` so "I could not look" is distinguishable from "I looked and it is wrong".

Note when scripting it: do **not** pipe it through `| tail` inside a `&&` chain — the pipeline's
exit status is `tail`'s, which masks the verdict (the standing gotcha; it bit this tool's own
first live run).

## Posture

Read-only, Layer 2 (ADR-28/36) — reads the contract and the tree, writes nothing. **Adoption
first: wired into no gate.** Whether it should become one is a separate ruling; that question is
carried by its BACKLOG row, not decided here.

Running it against a **historical** artifact will report closed `[#id]`s as FAIL. That is
correct and not a defect — the tool is for *pre*-flight, where a closed id in a live contract is
exactly the staleness worth knowing about.
