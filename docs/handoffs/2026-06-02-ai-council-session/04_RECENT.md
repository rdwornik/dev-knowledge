# 04 · What just happened

A narrative of recent work on `ai-council`, written so a chat with zero prior context can
pick up the thread. Prose, not a log dump.

## The arc

The last stretch of ai-council work was **ecosystem alignment, not feature work**. Over
2026-05-17 → 2026-05-19 the repo did its ADR-51/53 conformance pass: `ARCHITECTURE.md` was
created from the canonical template and `AGENTS.md` was retired into a single canonical
`CLAUDE.md` v2.1, with displaced technical depth moved into ARCHITECTURE. No Python was
touched in that pass and the 407-unit-test suite stayed green. (Parallel earlier work over
the same window — research-provider migrations, the degradation alarm/ADR-08, the
billing-diagnosis health-gate — is in JOURNAL if a specific fact is load-bearing.)

On **2026-06-02** two things landed in sequence. First, the **universalization coherence
audit (G1)**: a read-only conformance check against `.dev-knowledge` committed `main`, which
fixed doc-truth drift the machine checks don't cover (ARCHITECTURE namespace path
`src/research/`→`src/ai_council/research/`, ADR-60 folder taxonomy; CLAUDE.md `last_reviewed`
frontmatter + §7/§8/§10/§11 reconciliation). That pass took ai-council's machine floor from
9/10 to **10/10 pass, 0 fail, 0 warn**. Two operator decisions came out of it: **D1 = Defer**
the BACKLOG schema migration (don't pre-empt the open upstream decision) and **D2 = Track,
don't build** the ADR-67 implementation obligation.

Then the **7-file canonical unify (ADR-38 A6)** landed: `CONTRIBUTING.md` was added, VISION
and ARCHITECTURE were normalized to the canonical spine, the `LESSONS.md` H1 was retitled,
and **D1 was effectively reversed** — `BACKLOG.md` was migrated to the ADR-66 story-map
(all 11 items preserved) because the upstream canonical-baseline decision settled
(`.dev-knowledge` BACKLOG #20 closed). This is where ai-council is **now**: unified to the
seven-file standard, the unify merged to `main` at `b4135e3` (Stage 1 done), working tree
clean.

The state-currency wrinkle worth knowing: the unify merge (`e91ba24` → `b4135e3`) landed in
git **after** the JOURNAL's newest entry (the G1 audit), so **the unify itself is not yet
journaled**. The G1 entry still reads "D1 = Defer / keep the stream schema," which the unify
superseded. Next session should prepend a JOURNAL entry recording the unify and the D1
reversal so the business record matches git.

## Four-tag discipline (canonical)

The sender tagged every claim using this discipline (canonical per HANDOFF_PROCESS v4.3
Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no reason to
  think it changed since
- **recall** — sage remembers from earlier in the session; **state may have changed** —
  verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file, verify via CC
before acting on it. This is the "handoff is back-and-forth" rule from PLAYBOOK methodology.

## What the sender said (state snapshot)

This was a **forward-looking state-snapshot handoff**, not a browser-chat interview — the
operator supplied the lived context directly: *ai-council is now unified (Stage 1 merged); its
pending work is the tracked ADR-67 implementation obligation and the 17 pre-existing ruff
errors as known code debt.* Phase 2 cross-checked each of those load-bearing claims against
ai-council repo state (table below) before generating this bundle. Where a claim could only
be carried from JOURNAL rather than re-verified this session, it is tagged `recall`.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| ai-council unified to the 7-file canonical standard (ADR-38 A6) | `CONTRIBUTING.md` present; BACKLOG migrated to ADR-66 story-map; unify merge on main | ✅ witnessed — verified | `git log --oneline -3` (`b4135e3` merge `chore/ecosystem-unify`) |
| Stage 1 merged | unify merge `b4135e3` is `main`'s HEAD, tree clean | ✅ witnessed — verified | `git rev-parse --short HEAD` → `b4135e3` |
| ADR-67 implementation obligation tracked, not built | BACKLOG `#9 [P3][L]` DEFERRED (`/council-question` template + gate + `council.return_dir`) | ✅ witnessed — verified | `BACKLOG.md` §"Council process & methodology" #9 |
| 17 pre-existing ruff errors (known code debt) | `ruff check src/ tests/` reports exactly 17 | ✅ witnessed — verified | `ruff check src/ tests/` → "Found 17 errors" |
| 407 unit tests pass | last green run recorded in JOURNAL (2026-06-02 + 2026-05-19); not re-run this session | ⚠ recall — re-run before relying on it | `pytest tests/ -m "not integration and not envcheck"` |
| Unify is journaled | JOURNAL newest entry (2026-06-02 G1 audit) **predates** `e91ba24`; unify not yet journaled | ✅ witnessed — state-currency gap, see arc | `git log -1 --format=%h -- JOURNAL.md` vs unify SHA |

## Decisions & reasoning to carry forward

- **D1 was reversed by the unify, deliberately.** The G1 audit deferred the BACKLOG
  story-map migration to avoid pre-empting an open upstream decision; once `.dev-knowledge`
  #20 closed, the unify migrated BACKLOG to the story-map with all 11 items preserved. If
  the JOURNAL still reads "Defer," that is stale, not contradictory — fix it by journaling
  the unify.
- **ADR-67 is "track, don't build" on purpose.** D2 kept the implementation obligation as
  BACKLOG #9 and explicitly **deferred building** it until the canonical-baseline settles
  (it now has). Even so, do not start it without an operator go-ahead — it is `[L]` and
  mirrors `.dev-knowledge` #70. (Recommendation, mark as such.)
- **The 17 ruff errors are known debt, not a fresh regression.** They predate this work and
  are carried as code debt; "tests green" does not make them "done." Closing them is a
  candidate Sonnet/medium housekeeping task, not silent scope creep.
