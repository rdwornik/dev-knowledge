# LANE H — terra review of frozen branches C + E · 2026-08-18

**FROZEN CONTRACT OF RECORD.** Saved verbatim at step 0 per ADR-110, before any review work.
Source: `~/Downloads/LANE-H-codex-review.md`. Content arriving later in the session is not
load-bearing — a correction re-enters as a new contract, never as a mid-flight message
(STANDING_RULINGS D2).

- **Lane:** `h`
- **Worktree:** `lane-h-554-codex-review`
- **Branch:** `worktree-lane-h-554-codex-review`
- **Reviews:** `worktree-lane-c-554-devcontainer`, `worktree-lane-e-502-mutmut` (read-only on both)
- **Births nothing; fixes nothing; merges nothing.**

**RECORDED DEVIATION (filename only, forced by a live gate).** The contract names the output
artifact `docs/audits/2026-08-18-review-batch1-c-e.md`. That name is REFUSED by the
`validate-hermetization` pre-commit gate (ADR-101 R3, Rule B): `review` is not a member of the
CLOSED 11-class audit-class enum, so the file cannot be committed under that name. The output
lands at `docs/audits/2026-08-18-codex-review-batch1-c-e.md` — the enum class `codex` (the
reviewer-origin class every prior `/codex-review` artifact uses) prefixed to the contract's own
string, which survives verbatim as the slug. No other term of the contract is altered.

---

## Contract, verbatim

# LANE H — TERRA REVIEW OF FROZEN BRANCHES C + E (PRE-MERGE, MANDATORY)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | medium |

**Governing doctrine:** every code-impact arc gets a terra review before merge, severity tally
written INTO the persisted artifact. Branches C and E are frozen NOW — reviewing them before
lane A stops takes review off the integration critical path.
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-review-lane-contract.md`, COMMIT first.

## SCOPE
- `worktree-lane-c-554-devcontainer` (5 commits) — devcontainer.json + provisioning script
- `worktree-lane-e-502-mutmut` (4 commits, HEAD c43351de) — test module-name fix + pyproject comment
Review the DIFF vs `main` per branch (`git diff main...<branch>`), via `/codex-review` (terra);
if the skill cannot target a branch diff directly, fall back to `codex exec` with the diff as
input — record which path was used.

## OUTPUT — one artifact: `docs/audits/2026-08-18-review-batch1-c-e.md`
Per branch: findings list with severity (P1/P2/P3), **severity tally in the artifact body**, and
exactly one verdict: `MERGE-CLEAN` · `FIX-BEFORE-MERGE (itemized)` · `BLOCK (reason)`.
Review focus, per branch: C — provisioning idempotency, ADR-106 uv-pin fidelity, gate-liveness
smoke honesty, no secrets/paths leaked into devcontainer.json; E — the module-name fix's blast
radius on every other test importing `fleet_analytics` (grep them all), sys.modules registration
correctness, pyproject truly comment-only (byte-diff the TOML values).

## RULES
Read-only on both reviewed branches — **you fix nothing, you write only your own artifact**.
No verdict prose beyond the three-value enum. No review of A, F, G, D (A reviews after its STOP;
F/G/D are non-code). Commit-and-STOP; STOP packet = both verdicts + tallies + artifact sha.

## WHAT NOT TO DO
No fixes on reviewed branches · no merges · no re-running their suites beyond what review needs ·
no scope creep onto other branches · no `git add -A`.
