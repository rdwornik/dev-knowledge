# CORPUS-492 reconciliation — the 12 seed verdicts re-derived against the landed spec

> Supersedes nothing (audits are immutable, ADR-53/CLAUDE.md §5 item 3) — this is a NEW file that
> re-runs the `docs/audits/2026-08-10-verification-arc9-rulings-recording.md` §3 seed-corpus pass
> against the spec as landed today, per the frozen contract
> `docs/audits/2026-08-13-technical-492-corpus-reconciliation-lane-contract.md` (commit `900006f6`).
> Gates the `[#492]` re-check dated 2026-08-17 (register `protocols/STANDING_RULINGS.md` I-D item 1).

## Source artifact

`SEEDED-DEFECT-CORPUS-v0.1.md` (operator's `Downloads`, browser-authored 2026-08-10) names 12
seeds across four classes (V/F/L/C). The 2026-08-10 verification pass pinned all 12 verdicts to
one config line: `[tool.ruff.lint] extend-select = []` (`pyproject.toml:160`, ruff v0.15.5).

## Method

Re-derive each verdict against the spec as it exists on this branch today (base `900006f6`, off
`main` at `09bce194`), rather than trusting the 2026-08-10 text unchanged. Two checks:

1. **Config-identity check** — did anything the 12 verdicts depend on change since 2026-08-10?
   - `pyproject.toml` `[tool.ruff.lint] extend-select` — `git log --follow -p -- pyproject.toml`
     shows exactly ONE occurrence of `extend-select` ever committed; it has never changed. Still
     `[]` at `pyproject.toml:160` today.
   - ruff version — `uv run ruff --version` → `0.15.5`, matching the pinned rev in
     `.pre-commit-config.yaml` and the `pyproject.toml` `[tool.ruff]` `required-version` floor.
     Unchanged.
   - `scripts/audit.py::check_task_tree_coherence` (the gate SD-C3's verdict depends on) —
     `git log --since=2026-08-10 --oneline -- scripts/audit.py` returns zero commits touching
     this function; still defined at `scripts/audit.py:3264`.
   - `scripts/normalize_dated_headers.py` (the rewriter SD-C1's verdict depends on) —
     `git log --since=2026-08-10 --oneline` returns zero commits. Unchanged; still wired as the
     `normalize-dated-headers` pre-commit hook (`.pre-commit-config.yaml:22`).
   - **Conclusion: the landed spec is byte-identical, on every axis the 12 verdicts cite, to the
     spec the 2026-08-10 pass measured against.**

2. **Live re-run, the two code seeds with a non-trivial gate interaction** — rather than stop at
   (1), the two verdicts that are NOT simple "ruff clean" (SD-F3 REWORK, SD-C3 BLOCKED-BY-GATE)
   were re-executed live against this branch's actual tools, off-tree (job scratch dir, never
   committed — corpus seeds are never landed on `main`, per the source artifact's own protocol
   paragraph):
   - **SD-F3 naive form** (`result = subprocess.run(..., check=False)`, unbound-returncode,
     bound-unused) → `uv run ruff check --config pyproject.toml` on the naive rendering:
     `F841 Local variable 'result' is assigned to but never used`, exit 1. **Reproduces exactly.**
   - **SD-F3 reworked form** (no binding, or binding-then-consuming `.stdout`) → same ruff
     invocation: `All checks passed!`, exit 0, oracle preserved (returncode still never read).
     **Reproduces exactly.**
   - SD-C3 was not re-run live (it would require staging a `tasks/` copy on a throwaway branch,
     out of this docs-only lane's footprint per the contract's overlap-avoidance clause) — its
     verdict rests on the config-identity check: `check_task_tree_coherence` is unchanged, so the
     gate interaction it measured (`audit.py health` exits 1 on a duplicated-frontmatter-key copy
     under `tasks/`) is unchanged.

## Re-pinned verdicts (old → new, locators)

| Seed | 2026-08-10 verdict | 2026-08-13 verdict | Flip? | Locator (landed spec) |
|---|---|---|---|---|
| SD-V1 | SEEDABLE | SEEDABLE | no | `pyproject.toml:160` `extend-select = []` — `PLR0124` not selected |
| SD-V2 | SEEDABLE | SEEDABLE | no | `pyproject.toml:160` — no vacuous-assertion rule selected |
| SD-V3 | SEEDABLE | SEEDABLE | no | `pyproject.toml:160` — no mock-self-exercise rule selected |
| SD-F1 | SEEDABLE | SEEDABLE | no | `pyproject.toml:160` — `BLE001` (flake8-blind-except) not selected |
| SD-F2 | SEEDABLE | SEEDABLE | no | `pyproject.toml:160` — `S110` (flake8-bandit) not selected |
| SD-F3 | REWORK | REWORK | no | `pyproject.toml:160` default `F841`; live-reproduced this pass (see Method §2) |
| SD-L1 | SEEDABLE | SEEDABLE | no | no gate resolves prose `file:line` citations (unchanged surface) |
| SD-L2 | SEEDABLE | SEEDABLE | no | no gate resolves SHAs in prose (unchanged surface) |
| SD-L3 | SEEDABLE | SEEDABLE | no | `undeclared_edges` reasons about declared edges only (unchanged) |
| SD-C1 | SEEDABLE, conditional | SEEDABLE, conditional | no | `.pre-commit-config.yaml:22` `normalize-dated-headers`; condition unchanged (no `## <ISO-date>` heading in the injected file) |
| SD-C2 | SEEDABLE | SEEDABLE | no | no gate parses markdown tables (unchanged surface) |
| SD-C3 | BLOCKED-BY-GATE | BLOCKED-BY-GATE | no | `scripts/audit.py:3264` `check_task_tree_coherence`, unchanged since 2026-08-10 |

**Flip count: 0 of 12.** Tally unchanged: **9 SEEDABLE · 1 SEEDABLE-with-condition (SD-C1) ·
1 REWORK (SD-F3) · 1 BLOCKED-BY-GATE (SD-C3)** — 11 of 12 reach a reviewer's eyes (the roadmap's
"11/12" phrasing), all 11 pinned to `extend-select = []` plus the two gate-dependent verdicts
(SD-F3, SD-C3) pinned to the two named organs above.

## What this reconciliation establishes, and what it does not

- Establishes that the `[#492]` re-check due 2026-08-17 will run against a corpus whose verdicts
  are current as of this commit — the corpus measures the repo the fleet actually has, not a
  2026-08-10 snapshot.
- Does not re-derive detection *rates* — same limit the 2026-08-10 pass stated. This reconciliation
  is a spec-currency check on the 12 verdicts, not a new bake-off.
- Does not touch `SEEDED-DEFECT-CORPUS-v0.1.md` itself (still in the operator's `Downloads`, per
  I-D3 the contract is committed but the corpus source is not this lane's footprint) or the
  `wf-02c940ef` corpus SPEC reconciliation named in that file's header — both are named in the
  frozen contract as out of scope; the row this reconciles is `[#492]`'s Grok-lane gate only.
