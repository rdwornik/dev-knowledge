# Lane ab-834 — one protocols/ heading enforced: the commit-message type prefix

**Lane:** `lane-ab-834-protocols-heading-gate` · **Branch:** `worktree-lane-ab-834-protocols-heading-gate` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md`) · **Date:** 2026-09-16

Consumers: [#834]

## 1 · Premise — the plan as given

Row `[#834]`, ORDERED by the operator 2026-09-16: "one `protocols/` heading enforced";
standing constraint: "no new commit-tier gate without a measured cost", following the
`[#786]` `validate_prepend_order.py` pattern (one ungated rule-bearing heading, measured
breaches, a refusal + trip-test).

## 2 · Enumeration and ranking (Done-when 2)

Every `##`/`###` heading in `protocols/*.md` was read and judged for a MUST/NEVER/refuse-shaped
rule (`protocols/archive/` excluded as retired; PLAYBOOK "### Order conventions" excluded per
the contract, already gated by `[#786]`).

| Heading | File:line | Rule (paraphrase) | Enforced by | Breach count (real, non-merge, non-synthetic) |
|---|---|---|---|---|
| Commit message standard — Conventional Commits type prefix | PLAYBOOK.md:671 | `type(scope): summary` shape | **none** (picked) | **15** SHAs, see §3 |
| Commit message standard — summary length `~72` chars | PLAYBOOK.md:672 | soft length guidance | none | 5680/7985 (see §4, rejected) |
| Commit message standard — never bare "wip"/"fix"/"stuff" | PLAYBOOK.md:672 | trivial-summary ban | none | 0 |
| Commit message standard — body required for non-trivial change | PLAYBOOK.md:673 | body content rule | none | not mechanically checkable (no fixture found) |
| Commit message standard — one logical change per commit | PLAYBOOK.md:674 | split on "and" | none | fuzzy predicate, no clean git-log signal |
| Two-tier new-path rule | PLAYBOOK.md:644 | block convention-violating new paths | **declared not-yet-mechanized** by its own text, pending `[#345]` | n/a — out of scope, tracked elsewhere |
| Parallel sessions — no raw sibling `git worktree add` | PLAYBOOK.md:1734 | use native `--worktree`/`EnterWorktree` | none | 0 committed (2026-06-02 incident was uncommitted disk orphans, no SHA) |
| Root hygiene — files that MUST remain at root | PLAYBOOK.md:720 | 5 named configs never move | none | 0 |
| Root hygiene — `.env.example`: do not create | PLAYBOOK.md:734 | never auto-generate | none | 0 |
| Root hygiene — no `files.exclude` | PLAYBOOK.md:745 | never hide root config in VS Code | none | 0 |
| Rule-ID naming convention | PLAYBOOK.md:771 | ID form for `doc_code_edge` | `doc_code_edge` advisory check (explicitly non-blocking) | n/a |
| Testing rules table | PLAYBOOK.md:953 | tests required at scale | `impacted-tests-guard` ([#278]) | already enforced |
| Branch prefixes — closed enum | PLAYBOOK.md:678 | 8-shape closed enum | `scripts/validate_branch_naming.py` | already enforced |
| Universal visual pattern (ADR-59) | PLAYBOOK.md:747 | dot-prefix/ALL-CAPS/sort discipline | `scripts/audit.py` (3 checks) | already enforced |
| Order conventions | PLAYBOOK.md:1399 | *(excluded — [#786])* | — | — |

Excluded as non-rule-bearing (for legibility): "Default branch — main" (pointer, not itself
normative beyond a one-liner covered elsewhere), "Folder structure", "docs/ folder taxonomy"
(pointers to ADR-60), "Secrets storage path" (`[UNRULED]`), "Capitalization conventions"
(`[TBD]`), "Checkable rules: concrete over aspirational" (meta-guidance about writing rules,
not itself a rule), the two "Architect epistemic discipline" headings (agent-behavior prose,
no committable breach signal), "Architect → operator channel-discipline" (governs browser-chat
behavior outside this repo's commit surface).

## 3 · The pick, and why the sub-clause matters

**"Commit message standard" is the top-ranked heading in the `none` set** — every sub-rule
under it is ungated, and at least one sub-rule (the type prefix) has clean, real, historical
breach evidence: **15 commits** (non-merge, excluding git's own `Merge `/`Revert "` auto-generated
subjects and the stash/worktree synthetic pseudo-commits `git status` surfaces), all from the
pre-formalization era:

```
08aff16c 7117c076 1e075a87 4e1320cd 19a88450 d97482b0 f0e5502f
fabb6eb3 3a2bf18e 7289cdde 415f2758 341548c7 274221ba 2b337bf6 49d6647c
```

Fixture SHA used in the RED-first test: `2b337bf6` (`[ADR-30] Add ADR-30 -- default branch =
main for all Rob's repos`) — no type prefix at all.

**Why the gate is the structural type-prefix shape, not the whole heading verbatim:** the
heading bundles four sub-rules, and gating them all as written would refuse sanctioned,
current practice:

- **Rejected — the closed six-type enum** (`feat fix docs refactor test chore`). Measured:
  `git log --all --no-merges --format='%H %s' | grep -cvE '^(feat|fix|docs|refactor|test|chore)(\(...\))?: '`
  → 2093/7988 raw, but most of that is legitimate: `perf`, `build`, and `lessons` are live,
  organically-extended types — `lessons:` is explicitly sanctioned by
  `~/.claude/rules/git-discipline.md` for LESSONS.md appends. Gating the literal PLAYBOOK
  enum would refuse sanctioned commits on day one.
- **Rejected — the `~72` char summary length.** Measured: **5680 of 7985** commits exceed it,
  including commits that comply with this repo's own `[#id]`-citation and `kill-candidates:`
  conventions (AGENTS.md "Landing a change"). A 71% violation rate including this lane's own
  commits reads as a stale/aspirational rule superseded by practice, not a live norm anyone
  is breaching — enforcing it now would be exactly the "refuted premise" the contract's
  decision budget (Q10) warns against mechanizing silently. Judged as a lane-decision-budget
  default (not escalated — see §6) rather than picking a different heading, because the
  **structural** type-prefix sub-rule of the same top-ranked heading is real, clean, and
  non-disruptive.
- **Rejected — "never wip/fix/stuff/various changes" and "one logical change per commit".**
  Zero exact-match breaches for the former; no clean git-log signal for the latter (fuzzy,
  "would you write 'and'" is not mechanically checkable from a subject line alone).

**What's gated:** the subject line must carry a leading `type` or `type(scope)` (optionally
`!`) token before `: `. `Merge `/`Revert "`-prefixed subjects (git's own auto-generated
shapes) and empty messages are exempt. This is a real, currently-true property of the modern
commit history (0 breaches since the `[ADR-30]`/`@ docs(...)` era), so the gate should not
false-positive on future normal commits — the RED-first test suite pins both the trip case
and the extended-type pass case.

## 4 · Stage choice and measured cost (Done-when 3)

**Stage:** `commit-msg` (existing, active stage — `backlog-id-on-close` and
`backlog-filing-backpressure` already fire there; no new pre-commit STAGE introduced, one
more hook at an already-armed stage).

**Wall time measured** (`scripts/check_commit_message_type.py` invoked standalone against a
typical one-line commit message, this box):

- cold: **4.688s** real (`user 0.015s`, `sys 0.312s`)
- warm: **2.892s** real (`user 0.015s`, `sys 0.328s`)

Both numbers are dominated by `uv run --locked` + interpreter startup — the check itself
(a single regex match) is sub-millisecond. Same order of magnitude as the two sibling
commit-msg hooks already active; no new cost class introduced.

## 5 · RED-first witnesses and implementation

- **RED-first commit** `e70fe130`: `tests/test_check_commit_message_type.py` added with
  `scripts/check_commit_message_type.py` absent. Confirmed RED by running
  `uv run --locked pytest tests/test_check_commit_message_type.py -x` before the commit —
  16 collection errors (`FileNotFoundError`), loud, not silent.
- **Implementation commit** `a63668ff`: `scripts/check_commit_message_type.py` +
  `commit-message-type-prefix` pre-commit hook (`.pre-commit-config.yaml`, `stages:
  [commit-msg]`) + the PLAYBOOK.md cross-reference line (Done-when 5) +
  `ecosystem/organ-index.md` regenerated (the new hook is now a listed organ).
- **Coverage:** the trip case (bare subject, no prefix), the passing Conventional-Commits
  shape (with and without scope/`!`), the extended-but-sanctioned types (`perf`, `lessons`),
  `Merge`/`Revert` exemption, empty message, multiline (subject-only check), and the real
  historical breach SHA `2b337bf6` replayed as a fixture.
- 9/9 tests pass post-implementation; `ruff check` clean on both new files.

## 6 · Verdict, decisions taken under the budget, and what the integrator owes

**Targeted suite:** `tests/test_check_commit_message_type.py` (9),
`tests/test_check_backlog_commit_msg.py` (8, sibling hook — unaffected),
`tests/test_generate_organ_index.py` + `tests/test_gen_doc_counts.py` +
`tests/test_doc_counts_commit_tiering.py` (68, cover the two regenerated freshness files).
**All 85 pass.** Full suite not run, per the operator's constraint for batch AB and this
lane's "No full suite on this workstation" instruction.

**Rows.** `[#834]`: Done-when (1)-(6) all met. The row stays `status: open` — closure is the
operator's Tier-1 closure loop, not this lane's act.

**Decisions taken under the budget, none escalated:**

1. Gated the **structural type-prefix shape**, not the heading's closed six-type enum or its
   length/one-change sub-rules — see §3 for the measured reasoning. This is an
   implementation-detail judgment about which normative clause within the top-ranked
   heading becomes the checkable predicate (the same kind of choice `[#786]` made picking
   one interpretation of "append-only" as its predicate), not a deviation from "pick the
   top heading by breach count."
2. `SKIP` was never used on any commit in this lane — every gate that fired was either
   passed on merit or fixed (organ-index regen, doc-counts regen) before retry.
3. Regenerated `ecosystem/organ-index.md` and confirmed `ecosystem/doc-counts.md` needed no
   change (the RED-state commit's collection count matched the committed claim; the
   GREEN-state commit added no new *collected* tests beyond what the RED commit already
   introduced).
4. **Host was under heavy memory pressure throughout this lane** — 9-10 concurrent peer
   lanes on the same box. Every commit attempt required multiple retries (killed, not
   failed, each time) at the same heavy hook (`impacted-tests-guard` / `Zero-selection
   refusal`). No `--no-verify` was used at any point; every retry ran the full hook chain
   honestly. Recorded here since it inflated this lane's wall-clock materially and is not
   a defect in this lane's own work.

**Merge order.** No dependency on sibling AB lanes' content (this lane touches
`protocols/PLAYBOOK.md` §"Commit message standard" only, plus new files); check for
conflicts with any other lane editing `.pre-commit-config.yaml` or `PLAYBOOK.md` at
integration.

## To file

- Further ungated `protocols/*.md` headings surfaced but not picked (see §2 table): the
  "Two-tier new-path rule" mechanization is already tracked as `[#345]`; the sibling-worktree
  discipline (PLAYBOOK.md:1734) and the root-hygiene rules (PLAYBOOK.md:720/734/745) have
  zero measured historical breaches and are not strong candidates for a follow-on row unless
  a real incident surfaces. No new row filed for either — insufficient breach evidence to
  justify one under the same "measured, not chosen by taste" standard this row was held to.
