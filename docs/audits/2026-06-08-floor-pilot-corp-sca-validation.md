# Floor Pilot Validation — corp-sca-time-automation (#121 Step 5)

<!-- scope: meta -->

**Date:** 2026-06-08
**Pilot repo:** `corp-sca-time-automation` (child)
**Hub:** `.dev-knowledge`
**Decision:** ADR-78 (Child methodology floor — O2 Bounded Hybrid)
**Backlog:** closes [#121]; rollout owned by [#131]
**Status:** PASS — three witnesses recorded, two install-note findings filed

---

## Purpose

#121's hub components (generator + template, `audit.py floor_integrity`, `/ship`
staleness advisory, docs) shipped 2026-06-07 (JOURNAL, commit `bd9d510`). Close was
**gated** on a single-child pilot producing three witnesses in a separate session. This
record captures those witnesses (the gate) plus the findings the pilot surfaced.

---

## Witnesses (the close gate)

### (a) Floor loaded + re-anchor rule quoted verbatim — PASS

The generated `CLAUDE-FLOOR.md` auto-loaded in the child CC session (the ADR-78 O2
`@`-include path, verified empirically on CC 2.1.168 — JOURNAL 2026-06-07). The session
quoted the floor's re-anchor rule verbatim:

> Before any **structural** change (architecture, governance, a multi-file refactor, a new
> abstraction), **re-read this floor first**. For ordinary within-session work, trust the
> context already loaded — no per-action re-read needed.

Confirms the floor is present and its load-bearing rule is legible to the consuming session.

### (b) Tamper caught on BOTH sides — PASS

A deliberate edit to the child floor (tamper) was caught by both enforcement surfaces:

- **Child side (pre-commit):** the child's floor hash-verify hook exited **1**, blocking
  the commit of the tampered floor.
- **Hub side (`audit.py floor_integrity`):** the check went **FAIL → restore → PASS**,
  corroborated on disk by the two audit snapshots taken this session against
  `docs/audits/2026-06-08-corp-sca-time-automation-audit.md`:
  - **FAIL** (tampered): `14 total — 12 pass, 2 fail`; `floor_integrity FAIL` —
    `hash drift: floor sha256 2fdaba0be076… != sidecar 4d268f329a7e… — floor edited
    without regenerating OR tampered`.
  - **PASS** (post-restore): `floor_integrity PASS` — `hash matches sidecar; F5 clean;
    pointers resolve (sha256 4d268f329a7e…)`.

Both detectors fire on the tamper; restoring the floor to the sidecar hash returns PASS.

### (c) Re-anchor quoted before structural work — PASS

Before structural work in the pilot session, the floor's re-anchor rule was re-read and
quoted (per §"Re-anchor rule"), exercising the "re-read before structural change" mechanic
rather than relying only on the session-start pointer.

---

## Findings (install-note gaps — fix before fleet rollout)

These do not block the pilot witnesses but **must** be fixed before the n-repo rollout.
Both are install-note / runbook gaps; routed to [#131] (repo-onboarding runbook).

### (i) Install note missing `pre-commit install` → hook installed-but-INERT

The install note configured the child floor hash-verify hook in `.pre-commit-config.yaml`
but omitted the `pre-commit install` step. Result: the hook was **installed-as-config but
INERT** (the *wired-but-inert* class) — present in the config, but not armed in
`.git/hooks/`, so it would not fire on commit until `pre-commit install` ran. Configuration
presence is not enforcement; the gate is dead until armed.

### (ii) `pre-commit install` is a per-clone, local, untracked step

`pre-commit install` writes into `.git/hooks/` — a **local, untracked** change that does
**not** travel with the repo. Therefore **every fleet clone must run it** independently. It
is a **rollout step, not a one-time hub action**: the floor hook is inert in any fresh clone
until that clone runs `pre-commit install`.

---

## Gotcha (recorded)

**`git checkout -- <file>` restores from the INDEX, not from HEAD.** It will **not** undo a
staged edit — and during this pilot the shared index rode the tamper to `main` on a branch
switch. Use `git checkout HEAD -- <file>` (or `git restore --staged --worktree <file>`) to
restore from the committed version, not the index.

- **Symptom:** `git checkout -- <file>` appears to "restore" but the staged tamper survives;
  a subsequent branch switch carries the staged content along.
- **Fix:** `git checkout HEAD -- <file>` / `git restore --staged --worktree <file>`.

---

## Out of scope (observed, not part of this gate)

- `corp-sca-time-automation` `canonical_freshness` **FAIL** — `CLAUDE.md last_reviewed
  2026-06-02 predates last edit 2026-06-08`. A child-repo restamp (genuine end-to-end
  re-read + `last_reviewed` bump), executed in that repo's own session per ADR-41 routing.
  Not a floor finding.

---

## Disposition

- **[#121] closes** — the three witnesses (a/b/c) are recorded above; the close gate is met.
- **[#131]** gains the `pre-commit install` mandatory per-clone rollout step (findings i/ii).
- A `[P3][S]` item is filed for hub `templates/*.sha256` LF-pinning via `.gitattributes`
  (the recurring CRLF phantom diff observed this pilot).
