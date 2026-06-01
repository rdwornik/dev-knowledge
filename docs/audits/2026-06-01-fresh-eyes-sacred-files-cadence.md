<!-- scope: meta -->

# Fresh-eyes review — sacred-files freshness cadence (check #10)

**Date:** 2026-06-01
**Branch:** `feat/sacred-files-cadence-2026-06-01`
**Reviewed at:** `e6f9bd7` (pre-fix HEAD)
**Reviewer:** independent zero-context subagent (no access to the author's reasoning)
**Pairs with:** `2026-06-01-codex-sacred-files-cadence-check10.md` (Codex, code-only)

> Immutable review record (ADR-39). The fix commit that follows supersedes the
> findings below; this file is the point-in-time evidence, not updated in place.

---

## Scope

Full branch diff `main...HEAD` — both the code surface (`scripts/audit.py`,
`tests/test_audit.py`) and the markdown/frontmatter changes (which Codex's
code-only path-guard skips). Independent re-run of the green-state claims.

## Verdict

**0 critical in the code.** Git A2 logic, frontmatter parsing, severity
aggregation, portability, the read-only/Layer-2 invariant, doc-vs-code
consistency, test coverage, and the green state were each independently verified
sound. One substantive finding (below).

## Findings + dispositions

| # | Sev | Finding | Disposition |
|---|---|---|---|
| FE-1 | Important | CLAUDE.md §4 stamped `last_reviewed: 2026-06-01` while line 49 still carried the stale "known pre-existing failure: `test_audit_run_passes_structural_checks_on_synthetic_repo`" clause — that test now passes (verified). Stamping a file "confirmed accurate" while it contains a known falsehood undercuts the `last_reviewed` semantics. Already tracked as BACKLOG [#24]. | **FIXED** — clause removed; **[#24] closed**. |

## Independently confirmed correct

- **A2 git logic** — `%cs` returns committer date; `reviewed < git_date` fails only when strictly before (equal passes); graceful `None` on absent/no-repo/no-history → A1 fallback. *(Codex separately recommended `%cs`→`%as`; applied in the fix — see below.)*
- **`_parse_last_reviewed`** — handles YAML date / datetime-coerced / quoted-string / missing-key / unclosed-frontmatter / non-date; returns `None`, never raises.
- **Severity** — FAIL dominates WARN dominates PASS; missing→WARN (child-repo-safe); absent→skip. Verified by `test_freshness_a2_dominates_a1`.
- **Portability** — no `.dev-knowledge`-specific assumptions; parameterised `_FRESHNESS_FILES`.
- **Read-only / Layer-2** — only `subprocess.run(["git","log",...])`; no mutation.
- **Doc-vs-code** — PLAYBOOK / CLAUDE §4 / CONTRIBUTING / ARCHITECTURE match the code (30-day backstop, file set, FAIL/WARN split, manual-only caveat) — except FE-1.
- **Green state** — 135 tests, audit health 10/10, ruff clean, validate_backlog OK; real-repo dogfood caught the genuine ARCHITECTURE staleness.

## Cross-reference to Codex (dual-review consensus)

Codex (code-only) raised 3 High; the fresh-eyes pass independently corroborated
the test-coverage concern. Combined dispositions recorded in the fix commit:
- **Codex H2** (`%cs` rebase false-fail) → **ACCEPTED**: switched to `%as` (author date, stable across rebase/cherry-pick).
- **Codex H3** (tests over-mock git) → **ACCEPTED**: added real-git integration tests (committed-stale FAIL, equal-date PASS, no-history `None`, not-a-repo `None`).
- **Codex H1** (A2 misses uncommitted/working-tree edits) → **REJECTED + DOCUMENTED**: folding working-tree state would FAIL during normal mid-edit work and contradicts the operator's explicit commit-based A2 definition; the post-commit / eventually-consistent boundary is now documented in the check docstring + PLAYBOOK.
