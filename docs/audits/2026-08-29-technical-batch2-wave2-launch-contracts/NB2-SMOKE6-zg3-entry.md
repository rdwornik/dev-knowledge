# NB2 · SMOKE-6 — the Z-G3 entry-condition probe (read-only)

**Substrate:** codespace
**Consumer:** `docs/audits/2026-08-29-verification-night-mission-close-packet.md` §3 — the
night-mission close packet reads this probe's result and reports it against standing ruling
**Z-G3**'s entry condition, and against `[#591]`'s freeze-time predicate work that produced
the module change this probe is the control for.

**Purpose.** Produce, or fail to produce, the receipt Z-G3 defines as the entry condition for the
wave-2 router ADR: `Ok=True` **AND** `RemoteExitCode=0` **AND** `receipt HEAD == pushed HEAD`.
That receipt has never been produced. This is the one authorized attempt.

## Task

Zero writes. Zero commits. Report four facts and exit 0:

1. `git rev-parse HEAD` — the in-container HEAD.
2. `git status -sb` — whether the clone believes it is current.
3. `git log -1 --format=%cI` — the HEAD commit's date, which is what makes a silently-stale
   clone visible.
4. `uv --version || echo "uv ABSENT"` — W4 defect 2.

The pushed HEAD to compare against is `b4ab25abaa23719d0ba88584779e416d925d9229` on
`origin/main`.
