# NB2 · CLOUD C2 — [#598] slow-marker selector evidence (READ-ONLY)

**Batch:** night-batch-2 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.

**Substrate:** cloud

## BRIEF (verbatim from the frozen bundle)

> **C2 — [#598] slow-marker selector evidence.** Marker taxonomy, selector shape, and what a
> --durations run must produce for the marker set to be REGENERABLE. Durations themselves:
> MEASUREMENT-OWED-LOCAL, never guessed. State the fast set's coverage gap explicitly.

## WHAT TO GROUND IT IN

- The row: `tasks/598-*.md` — read its done-when clause by clause; your report answers it.
- `pyproject.toml` `[tool.pytest.ini_options]` — the existing marker registrations, addopts, and
  whether `-n auto` (xdist) is already default. A marker scheme that fights xdist is not a scheme.
- `tests/` — the actual suite. Enumerate the test FILES and their apparent cost drivers by
  reading them (subprocess spawns, `git` calls, whole-corpus scans, `audit.py` invocations,
  `tmp_path` repo constructions). Cost drivers are readable; **durations are not** — the suite
  cannot run here.
- Any existing `slow`/`oracle`/tier markers already in the tree, and `[#528]`'s tiered-suite
  doctrine (`protocols/PLAYBOOK.md` Ch5, "Tiered suite").

## THE THREE DELIVERABLES, IN ORDER

1. **Marker taxonomy** — the smallest set of names that partitions the suite usefully, each with
   a one-line admission rule a contributor can apply without asking. Name the alternative you
   rejected and why.
2. **Selector shape** — the literal invocations for each tier, and where they are declared so the
   declaration is single-sourced (addopts? a `Makefile`-equivalent? the `verify` skill? name it).
3. **REGENERABILITY** — precisely what a `--durations` run must emit, and the mechanical rule that
   turns that output into the marker set, so the set is **derived and re-derivable** rather than
   hand-curated and rotting. This is the half [#598] actually turns on.

## THE COVERAGE GAP — state it, do not soften it

A fast tier that skips the slow tier is a tier that does not run some tests. Enumerate, by name,
what the fast set would NOT cover, and say which gates would therefore be unproven in a fast run.
The repo's own doctrine is that a gate that never fired is not proven.

## SELF-AUDIT

Every duration, every "this test takes ~Ns", every ranking by cost is
**MEASUREMENT-OWED-LOCAL**. If your report contains a number you did not compute from a file in
the clone, you have guessed — flag it yourself.

---

## STANDING CLAUSES FOR EVERY CLOUD LANE OF NIGHT-BATCH-2 (frozen)

> Shared: zero writes, zero deletions, zero commits; no gate runs (uv mismatch); gate-dependent
> claims = MEASUREMENT-OWED-LOCAL. Each ends with EXACTLY ONE self-contained artifact.

**You are READ-ONLY.** Do not create, edit, delete, stage, commit, branch, push or tag anything.
Your entire output is ONE report, written as your final assistant message.

**You cannot run this repo's gates.** The container's `uv` is 0.8.17 against the repo's pinned
`required-version = "==0.11.19"`, so `uv run --locked …` cannot start. Read files, use `git log`
/ `git show` / `grep` / `python3` directly. **Any claim that would need a gate, a hook, the
pytest suite or `scripts/audit.py` to establish is written as `MEASUREMENT-OWED-LOCAL`, never
estimated and never asserted.** That marker is a first-class, correct outcome here.

**Every claim carries a resolving locator** — `path`, `path:line`, a heading, or a SHA. A claim
without one is not a claim. Do not restate a count you did not compute; compute it and show the
command.

**Output shape.** ONE self-contained artifact as your final message. Begin with the report's own
`#` heading as byte 0 — no preamble line, no wrapping code fence around the whole report. (Two of
the four 2026-08-26 cloud reports wrapped themselves in a fence behind one line of prose; the
harvester kept the bytes and recorded the deviation, which is more expensive than getting it
right.) Inside the report, fence code and tables that the operator will copy.

**Self-audit clause.** Each brief below states a way its own output can fail while looking
complete. Apply it to yourself and **say so in the report** if it happens.

**Repo facts you can rely on (measured on the operator's disk, 2026-08-28 23:36 local):**
`docs/intake/*.md` = 56 · `docs/decisions/*.md` (top level) = 89 · `docs/audits/*.md` (top level)
= 769 · `tasks/**/*.md` = 344 · `BACKLOG.md` = 67,883 B (a generated one-line VIEW since [#589];
the SOURCE OF TRUTH is `tasks/`). If your own count of the clone disagrees, **report both** — the
clone is `origin/main` and the disk may be ahead.
