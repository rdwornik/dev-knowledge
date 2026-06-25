# Residual — 2026-06-25 CC session-close (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the corrected state, the
> disposition, and the **pending queue**. It does **not** re-narrate the A1–C2 / Audit-A/B window
> (that is in `JOURNAL.md` last-5, read in full) or re-transmit methodology (pointer + mechanical
> enforcement). This is the **finalization arc** of the 2026-06-25 window: the substantive work was
> already committed + JOURNAL-wrapped before this session; this residual carries the three things a
> fresh session cannot reconstruct from the repo alone — the **confirm-live main-state correction**,
> the **#184 disposition rationale**, and the **forward pending queue**.

---

## §1 — Corrected main-state (THE HEADLINE — the originating prompt's premises were REFUTED)

The session-close prompt was pre-authored against an **earlier** git state and asserted a
"concurrency incident / coordination crisis" requiring repair before any push. **Confirm-live
refuted every Step-0 premise** — the branch-race was **already repaired non-destructively** in the
prior arc of this window and JOURNAL-wrapped (see the 2026-06-25 Audit-A entry + merge `1e5fa80`
subject "branch-race repair"). All rows below are **witnessed** (re-derived live).

| Prompt premise | Live reality | Re-derive with |
|---|---|---|
| `5276b7e` still direct-to-main on the first-parent spine | **NO** — it is the 2nd parent behind `--no-ff` merge `56cd7c5`; not on the spine | `git rev-list --first-parent main \| grep 5276b7e` (empty) |
| JOURNAL anchor for `5276b7e` still owed | **NO** — covered by the 2026-06-25 JOURNAL entry (`a19aaf8`) | `git log --oneline \| grep a19aaf8` |
| `block-ff-push` would REFUSE a push of main now | **NO** — push range `origin/main..main` has **0** FF/direct commits on the spine (4 clean `--no-ff` merges) | `git log --first-parent --no-merges origin/main..main` (empty) |
| `validate_no_ff` flags a 2026-06-25 violation | **NO** — only the 2 **pre-existing 2026-06-19** commits (`3a894ee`, `d0f9ead`), both already on `origin/main` (not in the push range) | `python scripts/validate_no_ff.py` |

**Net:** `main` is clean, working tree clean, **ahead of `origin/main` by 12** (all `--no-ff`
merges: C2 `009c3e1` · Audit-A `56cd7c5` · Audit-B `6e92222` · journal-wrap `1e5fa80`, plus this
finalization arc). `ship-gate` is GREEN with the **same pre-existing dispositioned WARNs** (the two
2026-06-19 `no_ff_merges`, the `#77` voided-closure `git_backlog_drift`, the `doc_rot`
history-accretion family); this arc adds **zero** new WARN. **Do NOT touch `5276b7e`** — it is not
this session's commit, and journaling/repairing it here would falsely claim another arc's work.

---

## §2 — #184 CLOSED (the empirical close of the ADR-87 architect/CC equilibrium contract)

**Verbatim done-when:** *"a real next-build prompt = intent + plan/auto mode + a thin
governance-pointer AND CC self-loads code-impact + gotcha context correctly (demonstrated)."*

**Operator-confirmed CLOSE** (`closes [#184]`, commit `5c21933`). Evidence — the contract held
across the **A1–C2** arc (and this session):
- **Prompt shape:** each arc's prompt carried intent + plan/auto mode + thin governance-pointers
  (ADR refs, DO-NOT lists, ship-gate-from-git-bash).
- **CC self-load + verify-don't-assert:** CC refuted the architect's premises at the authoritative
  source rather than executing them — the `cc-prompt-skill` premise (A1: "no cc-prompt skill
  exists"), the A2 `#194`-scope premise, the dead-corpus premise (C1/C4/C6: every named removal
  target verified live/gated), the fold-hint premise (C2: "diverged from the naive fold-1+4+5
  model"), and this session's `5276b7e` direct-to-main premise.
- **Close-on-hard-metric:** `#161/#164/#144/#145` were all **advanced-not-closed** on their
  verbatim done-when ("no closes-bracket"); #184 itself closed only when its hard metric was met.
- **Gotcha + code-impact self-load:** git-bash ship-gate (avoided the PowerShell `handoff_probes`
  false-RED), `doc_rot`/`validate_backlog` markers; **code-impact** on A3/C3
  (`tests/test_handoff_modes.py` — CC self-loaded the test contract + updated assertions correctly).

**Concurrency caveat (SEPARABLE finding, not a blocker on #184):** the 2026-06-25 shared-checkout
branch-race exposed a **multi-session-coordination / worktree-orchestration** gap — a **different
axis** than the architect/CC *prompt-contract* #184 measures. It is **already covered** by existing
lessons (LESSONS 2026-06-05 + 2026-06-07 + the user-level gotchas §worktree-discipline + ADR-61);
the worktree-orchestration clause is **resident** in `HANDOFF_BOOT.md` (A1-prose). The gap was
**application, not doctrine** — the clause was simply not applied to the concurrent read-only
audits. A 2026-06-25 witness was appended to `LESSONS.md` (see §3 "Lesson").

---

## §3 — Pending queue (carry forward)

### Push (outward-facing, operator-gated — NOT blocked)
- `git push origin main` — the gate would **PASS** (§1); `main` is ahead by 12 `--no-ff` merges
  awaiting the operator's push decision. The prompt's "coordination crisis before any push" is
  **already resolved**; this is a normal operator-gated push, nothing more.

### Audit-A — dependency-architecture follow-ups (`docs/audits/2026-06-25-dependency-architecture-coverage-audit.md`)
- **GAP-1 (highest leverage):** wire the **proven Pyright reverse-dependency oracle** (122 deps
  live, consumed by no gate) into an actual gate — e.g. `#195` safe-removal. The **code↔code import
  graph** among the flat `scripts/*.py` modules is currently **unenforced** (codemap polices an
  ~empty 2-package/0-edge graph).
- **Promote the 8+ undeclared `reconciled_with` edges to declared** — these are discovery-only,
  never gated. ⚠ The v5.3 bump did **NOT** re-check them → **spot-check CLAUDE/PLAYBOOK/VISION/etc.
  for staleness vs @5.3** before promoting.
- **Ranked test-writing backlog** (GAP-2/3/4/6/7 — designs in the audit §4) as a **gated,
  test-first, review-first** build — **NOT** blind generation.

### Audit-B — process/trigger/usage follow-ups (`docs/audits/2026-06-25-...process-trigger-usage` per JOURNAL)
- **`check-against-spec` decision:** the skill is **BUILT + tested** (2026-06-17) but **NOT invoked
  at its real trigger** — C2's v5.3 reconciliation was done **manually** (a "verify-first" pass + 3
  freshness re-reads, no skill invocation). Either **exercise it on the next spec bump** (its exact
  trigger) or **retire it as speculative**.
- **`../dev-knowledge-138` orphan cleanup:** an **empty sibling** dir (outside the repo, NOT a
  registered worktree, created 2026-06-18) — the `.dev-knowledge-*`-orphan class critical-rule #9
  warns about. Needs **explicit operator OK to `rm`** (core-invariant #3); does not affect the clean
  tree or ship-gate.
- **CLAUDE.md §8 stale claim:** the **user-level** `verify`-skill entry is stale —
  `~/.claude/skills/` holds only `gotchas` (the real `verify` is repo-level). A **canonical-file
  groom** (editing CLAUDE.md trips the freshness gate → batch with the §11/§7 grooms, don't
  piecemeal).

### Drift
- **#204** — CONTRIBUTING "Nightly outcome management" describes the **superseded** squash-merge-to-
  `main` model (ADR-84 + ARCHITECTURE Ch3/Ch6 say divert-to-`automation/conformance-digest`-and-
  close). Filed; awaits a canonical-file-integrity groom.

### Lesson (captured this session)
- Appended a 2026-06-25 witness to `LESSONS.md`: a **read-only audit that writes a report still
  commits** → still races a shared checkout → landed direct-to-main + owed an ADR-85 anchor. The
  forward rule already existed (2026-06-05/06-07 + ADR-61); the fix is **applying** worktree
  isolation to *every committing session, including read-only audits*. (Optional follow-up in
  `~/.claude`: bump the gotchas worktree-entry "Last triggered" → 2026-06-25.)
