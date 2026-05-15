# Action Plan — .dev-knowledge (session-sync, 2026-05-15)

<!-- scope: meta -->

## Next session goal

Build the **Audit Tool P1 MVP** per ADR-36 [audit tool architecture — see
`05_GOVERNANCE_ESSENCES.md`]. This is the first executable implementation
phase of `.dev-knowledge`'s "Auditor" function declared in VISION.md.

P1 MVP delivers: a Click CLI at `scripts/audit.py` with subcommands `audit
run`, `audit health`, `audit list-repos`; an ecosystem state schema
(`ecosystem/{repo}/state.yaml` snapshot + `ecosystem/{repo}/history/YYYY-MM-DD.md`
append-only log); three pure-Python deterministic checks (VISION.md
presence/frontmatter, ADR-38 root-file baseline, ADR-31 CLAUDE.md presence);
and a single markdown report at `docs/audits/YYYY-MM-DD-ecosystem-audit.md`.

Success criteria: self-audit of `.dev-knowledge` produces a coherent
markdown report; cross-repo audit of `ai-council` produces a coherent markdown
report; all new tests pass via `pytest -x --tb=short`. Both runs are
mandatory — testing only on self-audit would reproduce the
`universal-without-cross-case-verification` pattern captured in LESSON #9.

## Action plan

0. **Pre-flight state verification** — read repo state before any scaffolding:
   `git log --oneline -20`; `JOURNAL.md` (last 100 lines); `BACKLOG.md` (full);
   `LESSONS.md` (last 80 lines); `protocols/PLAYBOOK.md` §18 (Ecosystem Audit
   Tool Workflow — the operational spec); `docs/decisions/ADR-36-audit-tool-architecture.md`;
   `docs/decisions/ADR-38-universal-repo-architecture.md` (verify mandatory files
   list before implementing check #2).
   Present state summary + revised implementation plan to operator. Wait for
   operator "proceed" before continuing.

1. **Scaffold Click CLI** at `scripts/audit.py` with subcommands `audit run`,
   `audit health`, `audit list-repos`. Match `scripts/validate_scope_tags.py`
   pattern (single-file, Click, runs as `python scripts/audit.py`).
   Verification: `python scripts/audit.py health` exits 0; `--help` text
   coherent and matches PLAYBOOK §18.

2. **Define ecosystem state schema** — `ecosystem/{repo}/state.yaml` (fields:
   repo name, path, last-audit timestamp, findings list with `check_name`,
   `status`, `evidence`); `ecosystem/{repo}/history/YYYY-MM-DD.md` (append-only
   per-run record). Implement with Python dataclasses (no new deps unless
   `pyyaml` or `pydantic` already in `config/requirements-dev.txt`).
   Verification: schema roundtrip test passes.

3. **Implement check #1: VISION.md presence + frontmatter** per ADR-33 —
   target repo has `VISION.md` at root; YAML frontmatter present, valid,
   contains minimum keys (verify exact list against ADR-33 before coding).
   Verification: passes on `.dev-knowledge` self; passes on `ai-council`
   (has VISION.md per repo tree); fails on fixture missing VISION or with
   malformed frontmatter.

4. **Implement check #2: ADR-38 root-file baseline** — target repo has all
   mandatory root files (verify list against `ADR-38-universal-repo-architecture.md`
   before coding; expected: `BACKLOG.md`, `LESSONS.md`, `VISION.md`,
   `README.md`, `CHANGELOG.md`, `JOURNAL.md`). Returns gap list of missing
   files.
   Verification: passes on `.dev-knowledge`; passes on `ai-council`; fails on
   fixture with missing files.

5. **Implement check #3: ADR-31 CLAUDE.md presence** — target repo has
   `CLAUDE.md` at root; file non-empty.
   Verification: passes on `.dev-knowledge`; passes on `ai-council`; fails on
   fixture without CLAUDE.md.

6. **Implement markdown report output** to
   `docs/audits/YYYY-MM-DD-ecosystem-audit.md` — per-repo findings table
   (repo, check, status, evidence), aggregate summary (n repos, n checks,
   n passes, n fails), links to per-repo history files.
   Verification: report file generated; renders cleanly as markdown; passes
   scope-tag validator with `<!-- scope: meta -->` at top.

7. **Write tests** in `tests/test_audit.py` — schema roundtrip; each check
   on known-good and known-bad fixtures; report generation with mocked check
   results; `audit health` exit code.
   Verification: `pytest -x --tb=short tests/test_audit.py` passes.

8. **Run self-audit**: `python scripts/audit.py run --repo .dev-knowledge`.
   Verification: report generated; findings match expected state OR surface
   real issues (acceptable — surfaced issues become BACKLOG items).

9. **Run cross-repo audit**: `python scripts/audit.py run --repo ai-council`.
   Verification: report generated; findings surfaced for operator routing
   (NOT written to ai-council — read-only contract absolute).

10. **Update BACKLOG**: mark Stream C "Audit tool P1 implementation" `[done]`;
    add any surfaced findings as new BACKLOG items in the correct repo.
    Verification: BACKLOG diff shows P1 item flipped to `[done]`.

11. **Commit, CHANGELOG, JOURNAL** on feature branch `feat/audit-tool-p1-mvp`
    with per-concern commits (scaffold+schema; check #1; check #2; check #3;
    report; tests; self-audit results; cross-repo results; BACKLOG/CHANGELOG/
    JOURNAL). Merge `--no-ff` to main after operator approval.
    Verification: pre-commit clean; scope-tag validator clean; tests pass;
    hybrid ratio ≤25%.

## Hard Constraints

- **Do NOT write to child repos.** ADR-36 read-only contract is absolute.
  Any write path to a repo other than `.dev-knowledge/` is an architectural
  violation.
- **Do NOT add new Python dependencies without operator confirmation.** Check
  `config/requirements-dev.txt` first; surface as a decision request if new
  deps are desired.
- **Do NOT implement P2 (handoff folder generator) in this session.** Scope
  boundary: P1 = audit run + state + report. P2 is a separate session.
- **Do NOT use LLM for deterministic checks.** All three P1 checks are pure
  Python. LLM augmentation is P4 scope.
- **Do NOT skip tests.** New audit tooling must follow `scripts/validate_scope_tags.py`
  + `tests/` pattern. No tests = incomplete P1.

## Narrow scope rules

- Do NOT expand check scope beyond the three specified (VISION/ADR-38/CLAUDE.md).
  Scope-tag drift, gotcha staleness, cross-reference integrity, LESSONS
  append-only invariant — all P2+.
- Do NOT couple P1 with sacred-files maintenance enforcement (separate P2 item).
- Do NOT regenerate or modify historical handoff bundles during this session.
- Do NOT push to remote without explicit operator approval.
- Do NOT skip the self-audit step. Self-audit is mandatory dogfooding.
- Do NOT mark BACKLOG P1 `[done]` until both self-audit and cross-repo audit
  runs produce coherent markdown reports (not just scaffold passing tests).
- LESSONS entries (if captured) must use canonical 6-field schema; prepend at
  top of dated-entries section per `99a104e` correction.

## Fallback contingencies

- If `pyyaml` or `click` is absent from `config/requirements-dev.txt`: surface
  to operator as dep-addition decision. Do not install silently.
- If `ai-council` VISION.md is malformed or absent: that is a valid finding,
  not a bug. Report it; do not auto-fix in target repo.
- If self-audit surfaces unexpected findings on `.dev-knowledge`: treat as
  open questions, not confirmed failures. Surface to operator before any
  remediation.
- If ADR-38 mandatory files list differs from the architect-inferred list in
  this document: defer to ADR-38 canonical spec; surface discrepancy in
  CHANGELOG.

## Success criteria

1. `python scripts/audit.py health` exits 0.
2. `python scripts/audit.py run` produces `docs/audits/YYYY-MM-DD-ecosystem-audit.md`
   with coherent findings.
3. Self-audit of `.dev-knowledge` completes without errors.
4. Cross-repo audit of `ai-council` completes without errors.
5. `pytest -x --tb=short` passes for all new `tests/test_audit.py` tests.
6. Pre-commit passes clean; hybrid ratio ≤25%.
7. BACKLOG Stream C P1 "Audit tool P1 implementation" marked `[done]`.
