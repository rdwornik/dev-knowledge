# G4 (`[#626]`) — terra pre-merge tally and the blocked release act

> consumer: batch G's close packet; `[#626]`; G3b's C7 re-shape, which this finding extends to C4.

Reviewer `codex exec review --base main`, concurrency 1. **Wall-clock 111 s.**

**Severity tally: HIGH/P1 = 1 · MED = 0 · LOW = 0. CONFIRMED. BLOCKED, not fixed — by a ruling.**

| # | Sev | Finding | Disposition |
|---|---|---|---|
| 1 | P1 | The plugin scripts are fixed but `plugin.json` stays at `0.1.11`; the plugin cache is version-keyed, so every already-installed consumer keeps running the STALE copies | **CONFIRMED · BLOCKED** — the bump collides with a standing ruling; routed, see below |

## The defect recursed one level, in the lane written to stop it

`[#626]` exists because the hub copy was fixed while the **executing** copies were not. This lane
fixed the executing copies — and left the **installed** copies stale, because a consumer's plugin
cache is keyed by the version in `plugin.json`, which the lane did not touch.

**The repo already recorded this exact trap**, in July:
`docs/audits/2026-07-28-codex-437-closure-design.md:37` — *"omits the required plugin version bump
and per-consumer cache-update workflow"* — and
`docs/audits/2026-07-28-technical-437-closure-token-design.md:216` — *"a plugin version bump is
therefore a RELEASE ACT."* The class was named, filed, and walked into again.

## Why the bump is not being made here

`deploy/release_lint.py` **C4** asserts `anchors.plugin_version` == the LIVE `plugin.json`
version, and `0.1.11` is pinned in **six** manifests — `v1.1.0`, `v1.2.0`, `v1.3.0`, `v1.3.1`,
`v1.4.0` (all released) and `v1.5.0`. Bumping to `0.1.12` therefore forces one of two moves:

- edit all six, including five RELEASED manifests — **refused by ruling R-G-G3b**: *"a released
  manifest is history"*; or
- edit only `v1.5.0` — and C4 then FAILS for the five released ones.

The July precedent (`2026-07-28-codex-444-release-0-1-11.md`) took the first option, editing "all
5 deploy manifests in lockstep". That is precisely the move now ruled against.

## The finding that generalises: C4 is C7

**C4 and C7 are the same defect.** Both bind a RELEASED manifest to a LIVE constant, so any
change to that constant must either rewrite history or break the lint. G3's item 2 hit it via
C7 and `VISION.md`; G4 hits it via C4 and `plugin_version`. G3b is already chartered to re-shape
C7 so a manifest binds only the constant **as of its own version**; the identical re-shape makes
C4 correct and unblocks this release act.

**Until that lands, this lane's source fixes are correct but INERT for already-installed
consumers.** Stated plainly rather than reported as done: a fresh install gets them; an existing
`0.1.11` install does not.
