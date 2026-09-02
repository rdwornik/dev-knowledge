# lane-g-628-essentials-debless — end-of-lane packet

Batch G, `[#628]`. Contract: `LANE-g-628-essentials-debless.md` (frozen). Branch
`worktree-lane-g-628-essentials-debless`, base `b5753f52`.

## Sequencing correction (architect, mid-lane)

The lane's original boot read "G3 merged before this lane" as a **boot precondition** and
PAUSEd when `.claude/workflows/conformance-hub.js:133` still carried the `protocols/ESSENTIALS`
token and G3's owning branch (`worktree-lane-g-621-freshness-absent`) had zero commits over
base. The architect corrected the premise: this is an **integration-order** statement (G3 lands
on `main` before G6 at `/lane-integrate`), not a start-gate for a parallel lane. Corrected
instruction: execute closures (a), (c), (d) now; for (b), run the grep-to-zero **excluding**
`conformance-hub.js:133` and record the exclusion + current token state (this document);
`conformance-hub.js` was never edited.

## Closure (a) — SESSION_SETUP.md + DEFINITION_OF_DONE.md pointers reworded

Landed in `55d67d42`. `protocols/SESSION_SETUP.md` Step 2 (functional chat, programming chat,
new-project scaffolding — 3 upload lists + 2 first-message blocks + 1 "PLAYBOOK not needed"
sentence, 7 literal occurrences total, not the 3 the contract's prose named) and Step 4's
transfer instruction no longer tell the operator to upload `ESSENTIALS.md`. Programming-chat and
new-project paths keep `CLAUDE.md` / `PLAYBOOK.md`, which already carried the content those
steps needed. `protocols/DEFINITION_OF_DONE.md`'s closing See-also dropped the `ESSENTIALS
"Ending a Session"` citation (removed, not replaced — matching the precedent of the original
de-bless commit `12f4113a`); the ADR-85 citation on the same line stands. No content deleted —
`protocols/ESSENTIALS.md`'s body is untouched.

## Closure (c) — asks-digest sequencing line corrected

Landed in `55d67d42`. `protocols/HANDOFF_PROCESS.md` §17.1's OPERATOR ASKS seed table (the live
source `fleet_health.parse_operator_asks` reads) had its "ESSENTIALS de-bless" row's sequencing
line changed from *"deferred to batch G after the v1.5.0 tag"* to *"batch G rides WITH the
v1.5.0 tag as a release act, not behind it"* — matching `CLAUDE.md` §12 v2.71 and the `tasks/`
DC-2 re-cut row's ruling that a floor edit is a release act.

**Left alone, flagged, not fixed:** the same seed-table row's RESIDUAL note still names
`SESSION_SETUP.md Step 2 (x3) + Step 4` and `DEFINITION_OF_DONE.md`'s See-also as outstanding —
now stale after closure (a) above. The frozen write-scope names only the one sequencing line;
updating the RESIDUAL prose (and the `re-asked`/`visible-fix` bookkeeping) is left for whoever
next touches that row, per the table's own "amended in place inside the fence" pattern.

## Closure (b) — grep-to-zero, EXCLUDING conformance-hub.js:133 (recorded, not discharged here)

```
grep -rn 'protocols/ESSENTIALS' protocols/ docs/ CLAUDE.md .claude/
```

339 hits total. **Current token state, excluded per the corrected instruction:**
`.claude/workflows/conformance-hub.js:133` still carries the literal token — G3
(`worktree-lane-g-621-freshness-absent`) has 0 commits over base; not landed. Never edited here.

Remainder (338 hits, minus 1 immutable audit-doc citation of the excluded line = 337 substantive)
breaks down as:

- **~192 hits are immutable historical records** (`docs/handoffs/*` bundles, `docs/decisions/
  ADR-*.md`) — per `CLAUDE.md` §5 rule 3 these are never edited in place; a route inside a sealed
  handoff or ADR is not a live boot instruction.
- **~12 hits are `docs/archive/` / `protocols/archive/`** — explicitly out of the "zero hits"
  scope per the contract's own wording.
- **~12 hits are `docs/audits/`** — dated, immutable evidence records, same genre as handoffs.
- **4 hits are `CLAUDE.md` itself** (`:16`, `:25`, `:203`ish §12 history entries) — these are the
  **correctly-worded** "SUPERSEDED / do not boot from it" banner and its own changelog, not a
  route. Landed by the original de-bless commit `12f4113a`; unchanged by this lane.
- **The remaining live-protocol-doc hits** (`protocols/STANDING_RULINGS.md` x3,
  `protocols/PLAYBOOK.md` x1, `protocols/AI_COUNCIL_PROCESS.md` x1, `protocols/HANDOFF_PROCESS.md`
  x1 — the line 1059 citation inside the seed table itself, describing what `12f4113a` did, not a
  route) belong to sibling batch-G lanes per the `tasks/628` consumer census (ten named
  consumers; this lane's frozen write-scope covers exactly two of them). **Not touched — outside
  this lane's footprint.**

**The integrator re-runs this grep after every batch-G lane (including G3) has merged.**

## Closure (b), RE-STATED so it can actually be discharged (integrator, 2026-09-02)

The instruction as written — `grep -rn 'protocols/ESSENTIALS' protocols/ docs/ CLAUDE.md .claude/`
reaching **zero** — cannot succeed, and the reviewer and the integrator found this independently:

1. `docs/` holds hundreds of IMMUTABLE audit and handoff records that legitimately cite
   ESSENTIALS as it was. An immutable record is not a route, and rewriting one to reach zero
   would corrupt the institutional record to satisfy a grep.
2. `.claude/` contains `.claude/worktrees/`, which during a batch holds a FULL COPY of the repo
   per lane. The command therefore greps itself N+1 times and returns thousands of self-matches.
   **It can only return zero on a tree with no worktrees — i.e. never while a batch is running,
   which is exactly when it is run.**
3. This lane's own packet, and the de-blessing banners in `CLAUDE.md`, ADD matching lines. A
   document that says "nobody routes to ESSENTIALS" contains the string.

**ACCEPTANCE, restated: zero actionable LIVE routes.** A live route is a line in a
currently-governing surface that sends a reader to `protocols/ESSENTIALS.md` for guidance — not
a citation, not a negation, not a history entry, not a worktree copy of one of those.

```
grep -rn 'protocols/ESSENTIALS' protocols/ CLAUDE.md   | grep -v '^\.claude/worktrees/' | grep -v '^protocols/archive/'
```

**MEASURED AT INTEGRATION, 2026-09-02, after G3 and this lane merged: TWO live routes remain.**

```
protocols/AI_COUNCIL_PROCESS.md:413  - "Repo-artifacts-in-Claude-Code rule: protocols/ESSENTIALS.md"
protocols/PLAYBOOK.md:330            - "1. .dev-knowledge/protocols/ESSENTIALS.md + PLAYBOOK.md"
```

Everything else resolves as a NON-route: `CLAUDE.md:25` reads "SUPERSEDED … skip it",
`HANDOFF_PROCESS.md:1059` reads "nobody to protocols/ESSENTIALS.md", and the STANDING_RULINGS and
CLAUDE.md §12 hits are evidence locators and section history.

**Closure (b) is therefore PARTIALLY DISCHARGED, and the reason is structural rather than an
oversight: neither surviving file is in this lane's frozen write-scope.** The lane was asked to
prove a repo-wide property while being handed three files. Recorded for the close packet, with
the ask-registry row updated to name the two survivors instead of the two this lane fixed.

## Closure (d) — tests, delta A2, conventions

**Targeted tests: 202 passed.** `uv run --locked pytest -q --no-header -k "session_setup or
definition_of_done or handoff_process or fleet_health or claude_md_byte_cap or canonical_docs"`
— covers every file this lane touched. No test pins the edited prose directly (`test_fleet_
health.py`'s `parse_operator_asks` tests run against an inline fixture, independent of the live
`HANDOFF_PROCESS.md` content).

**Ruff:** clean (no Python files under `protocols/` — doc-only lane).

**Delta A2 — NOT MEASURED this session.** Three consecutive full-suite (`pytest -q --no-header`,
default `-n auto`) attempts were killed by the harness before completing (progress at commit
time: ~72%, ~36%, ~2% after an internal `[gw13] node down` self-restart), each following
`tasklist` showing 50+ concurrent `python.exe`/`pytest.exe` processes — the seven sibling
batch-G worktrees running their own suites in parallel on the same machine. None of the three
kills produced a `passed`/`failed` summary line or a `failed_set.py`-readable report; this is
environment contention, not a suite defect, but it means the base-set subset comparison the
contract's Delta A2 clause requires (`docs/audits/2026-09-02-verification-base-failed-set-
1e064921.json`, 13 nodeids) **could not be run to completion in this session.**

**Partial evidence in lieu:** the 202-test targeted subset above is green, which covers every
node this lane's diff could plausibly affect. Nothing in this lane's diff (three docs files,
zero code) is a plausible source of a new regression outside that subset. **Recommendation:**
the integrator re-run the full-suite Delta A2 compare at `/lane-integrate`, when the seven
sibling lanes are no longer running concurrently and the machine has headroom.

**Conventions:** docs-only change; English, hyphen-only names, no code/logging/CLI surface
touched.

## Commits

- `55d67d42` — closures (a) + (c): SESSION_SETUP.md, DEFINITION_OF_DONE.md, HANDOFF_PROCESS.md
- This packet — closure (b) record + closure (d) status, per contract Step 4

## What NOT done (frozen anti-patterns honored)

- `conformance-hub.js` never touched.
- `CLAUDE.md` body never touched.
- No merge, no push to `main`, no index regeneration, no JOURNAL entry.
- No edit outside the declared write-scope.

**STOP.**
