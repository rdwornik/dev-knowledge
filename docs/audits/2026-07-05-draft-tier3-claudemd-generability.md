# 2026-07-05 — DRAFT (plan-only): Tier-3 CLAUDE.md generability

> **PLAN-ONLY. Nothing here is built.** Produced by the 2026-07-05 overnight run (Block E)
> for architect review. Question: how much of a repo's `CLAUDE.md` is derivable from machine
> sources (and could be generated like `.claude/methodology-roster.md`, [#244] P3), vs
> irreducibly hand-authored — and what would the generation seam + migration risk be?

## Section-by-section derivability (hub CLAUDE.md as the case study)

| Section | Class | Machine source (if derivable) |
|---|---|---|
| frontmatter (`last_reviewed`, `reconciled_with`) | **irreducible** (stamps ARE human attestations; generating them would fake the very review they attest) | — |
| §1 First read | mostly irreducible (reading ORDER is doctrine) | paths verifiable against disk |
| §2 Repo identity | irreducible (purpose/owner are declarations) | name/status could echo config |
| §3 Architecture pointers | irreducible (chapter map is editorial) | chapter list derivable from ARCHITECTURE.md headers |
| §4 Conventions | mixed — naming/commit/branch prose is doctrine; the **lint/test command lines** are derivable (pyproject, pre-commit config) | `.pre-commit-config.yaml`, `pyproject.toml` |
| §5 Critical rules | **irreducible** (the rules are the doctrine itself) | — |
| §6 Session start protocol | irreducible (ordered operator doctrine) | — |
| §7 Slash commands | **derivable** — the exact class the roster already generates for the deployed subset | `~/.claude/commands/`, `./.claude/commands/`, plugin manifest |
| §8 Skills | **derivable** (same class) | `~/.claude/skills/`, `./.claude/skills/` |
| §9 Hooks | **derivable** — pre-commit list from `.pre-commit-config.yaml`; session hooks from `.claude/settings.json`; the deployed subset ALREADY generated (`@.claude/methodology-roster.md`) | configs named |
| §10 Anti-patterns | irreducible (empirical lessons) | — |
| §11 Recent ADRs | **semi-derivable** — the "last 5" LIST is mechanical (docs/decisions/README.md tail); the one-liners are editorial | ADR index |
| §12 Section history | **irreducible** (append-only human record) | — |

Rough mass: ~35–40% of the file (by lines) sits in the derivable classes (§7/§8/§9 + §4
command lines + §11 list) — exactly the classes whose staleness this repo keeps paying for
(tonight's live proof: ai-council §9 claimed a ruff gate its config had pruned; its §7 missed
two plugin commands — both would be impossible under generation).

## Generation seam (the roster pattern, extended — no new invention)

- **Mechanism:** per-section generated fragments under `.claude/generated/` (e.g.
  `commands-roster.md`, `hooks-roster.md`), `@`-imported from CLAUDE.md exactly like
  `@.claude/methodology-roster.md` today. One generator script per repo-local surface
  (`gen_local_roster.py`), the manifest-driven one staying separate (different source of
  truth: disk state vs manifest declaration — do NOT merge them).
- **Freshness model:** generated fragments stay OUT of `DEFAULT_FRESHNESS_FILES` (currency =
  regeneration, the [#244] P3 precedent); a `roster-freshness`-style regen-and-diff
  pre-commit hook per fragment gates drift. Hand-prose CLAUDE.md remains IN the freshness
  gate — the split is the point: stamps attest judgment, hooks attest mechanical currency.
- **Consumer reach:** the generator ships as a deploy-tool carrier component only AFTER the
  hub n=1 proves it (the [#244] P6 WAIT rule applies unchanged).

## Migration risk (why NOT to do this in one pass)

1. **The @import budget** — each import adds boot-context mass; CLAUDE.md's ≤200-line budget
   discipline must extend to the composed total, or generation becomes licensed bloat.
2. **ADR-45 scope** — the `@path` ban is browser-handoff-scoped, not local session-boot
   (re-verified at the v2.27 review); a consumer rollout must re-verify each child's
   tooling honors imports (ai-council's floor import is the live precedent).
3. **Doc_claims interplay** — `validate_doc_claims` currently reconciles CLAUDE §9's
   hand-roster against the config; generating §9 RETIRES that check leg (currency moves to
   the regen hook). Retiring a check leg is a gate-semantics change → needs its own arc +
   ADR note, not a silent side-effect.
4. **Fleet heterogeneity** — child CLAUDE.mds are smaller and their §7/§8/§9 differ per
   repo; the generator must read each repo's OWN configs (the ai-council staleness tonight
   is the target class, but a hub-shaped template would overwrite child-specific truth —
   generation must be enumeration-from-local-state, never template-stamping).
5. **History sections** — §12 and any append-only content must never pass through a
   generator (regeneration is rewriting; append-only is the older invariant and wins).

## Recommendation (for the architect, not executed)

Phase 1 (hub n=1): generate §7+§8+§9's repo-local rosters via the seam above, keep every
other section hand-prose; measure two release cycles for stale-claim incidents (target: the
class tonight's ai-council fix exemplifies → zero). Phase 2 (decision-gated): §11 list +
§4 command lines. Never: frontmatter, §5, §6, §10, §12. File as a BACKLOG item only after
the architect ratifies the seam — this draft is analysis, not a queued build.
