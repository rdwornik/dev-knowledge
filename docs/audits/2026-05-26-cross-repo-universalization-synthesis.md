---
type: cross-repo-synthesis
scope: universalization status + recommended execution sequence across 4 child repos
date: 2026-05-26
basis: 4 per-repo refreshes (corp-monorepo, corp-ops, corp-sca-time-automation full + ai-council reference)
status: research artifact (input to operator sequencing decision)
contract: read-only on all child repos; writes confined to .dev-knowledge/docs/audits/
---

# Cross-Repo Universalization Synthesis — 2026-05-26

Aggregates the four per-repo audit artifacts produced/referenced this session:
- `2026-05-26-corp-monorepo-audit-refresh.md` + `-execution-plan.md`
- `2026-05-26-corp-ops-audit-refresh.md` + `-execution-plan.md`
- `2026-05-26-corp-sca-time-automation-audit-refresh.md` + `-execution-plan.md`
- `2026-05-26-ai-council-audit-status-reference.md` (points at the authoritative
  2026-05-25 ai-council refresh + plan in `docs/research/`)

## Aggregate state across 4 child repos

| Repo | Baseline | Refresh | Conformance | Findings (C/H/M/L) | Plan | Audit tool | Blockers |
|---|---|---|---|---|---|---|---|
| ai-council | 2026-05-23 | 2026-05-25 | ~70% | 14 (0/0/5/9) | Ready (decisions captured) | 1 WARN | None — awaits session |
| corp-monorepo | 2026-05-23 | 2026-05-26 | ~72% | 17 (0/4/5/8) | Ready | 3 PASS | Action 6 (VISION routing) needs Council |
| corp-ops | none (initial) | 2026-05-26 | ~45% | 9 (0/3/3/3) | Ready | 2 FAIL | None |
| corp-sca-time-automation | none (initial) | 2026-05-26 | ~45% | 8 (0/3/3/2) | Ready | 2 FAIL | None |

**Total: 48 findings across 4 repos** (ai-council count referenced, not
re-derived). 0 CRITICAL; the only HIGH findings are corp-monorepo's
ARCHITECTURE.md cluster (4) and the missing-governance-file gaps in corp-ops (3)
and corp-sca (3).

## The two patterns (the central finding)

The four repos split cleanly into **two universalization shapes**, and conflating
them is the main sequencing risk:

### Pattern A — residue cleanup (ai-council, corp-monorepo)
- All four mandatory governance files **present**; the work is **stripping
  tier/scale residue** + upgrading codemap form + doc polish.
- Audit tool is **near-green** (3 PASS / 1 WARN) but **overstates** conformance —
  the standard-level sits at ~70-72% because the tool can't see tier-residue,
  codemap form, README disposition, root-hygiene, or naming.
- These have **prepared plans** and are closest to executable. ai-council's
  operator decisions are already captured (2026-05-26 amendment).

### Pattern B — creation (corp-ops, corp-sca-time-automation)
- **Missing three of four** mandatory files (VISION, ARCHITECTURE, BACKLOG);
  carry **no** tier residue (they predate the tier system entirely).
- Audit tool is **red** (2 hard FAILs) and **agrees** with the ~45% standard-level
  estimate — because the gap is *missing files* (which the tool checks), not
  *residue in present files* (which it doesn't).
- The work is **building** the governance scaffold from seeds that already live in
  each repo's CLAUDE.md, then retiring CHANGELOG/README.

**Implication:** validate each pattern on its simplest instance before scaling it.
The residue pattern (ai-council) does not transfer to the creation repos, and vice
versa.

## Common findings across repos

| Finding | ai-council | corp-monorepo | corp-ops | corp-sca |
|---|---|---|---|---|
| README present (delete per default) | ✓ (external-ish) | ✓ (product) | ✓ (internal) | ✓ (internal) |
| CHANGELOG present (retire ADR-49) | — (absent ✓) | — (absent ✓) | ✓ | ✓ |
| Missing VISION/ARCHITECTURE/BACKLOG | — (all present) | — (all present) | ✓ (all 3) | ✓ (all 3) |
| Tier/scale residue (ADR-33/40) | ✓ | ✓ | — | — |
| CLAUDE.md pre-ADR-53 free-form | — (v2.1 template) | — (template) | ✓ | ✓ |
| `.env.example` present (root hygiene) | ✓ | ✓ | ✓ (clean rm) | ✓ (**referenced** — care) |
| Codemap upgrade needed | ASCII→Mermaid | tree→Mermaid | →Mermaid (new) | →text-only (new) |
| Workspace not dot-prefixed / absent | not-dotted | not-dotted | absent | absent (.vscode/) |

**Universal across all four:** README present (delete default) + `.env.example`
present (remove). **Split by pattern:** CHANGELOG + missing-files + old-CLAUDE in
the creation repos; tier-residue + present-CLAUDE-template in the cleanup repos.

## Recommended execution sequence

1. **ai-council** — *validate Pattern A.* Plan is most ready (operator decisions
   captured 2026-05-26), smallest residue cleanup, clears the only VISION `status`
   WARN. No blockers.
2. **corp-ops** — *validate Pattern B.* Cleanest creation case: clean package
   graph (graphical Mermaid codemap), `.env.example` not referenced (clean rm), no
   in-repo backlog complexity. No blockers.
3. **corp-sca-time-automation** — *Pattern B + 2 adaptations.* Same creation
   sequence as corp-ops, plus the **text-only codemap** (flat modules) and the
   **`.env.example` migration** (it's referenced). Benefits directly from corp-ops
   lessons. No blockers.
4. **corp-monorepo** — *Pattern A, hardest, last.* Largest repo; the dominant
   work is the ARCHITECTURE.md template re-home + Mermaid codemap (4 HIGH/near-HIGH
   items in one artifact), plus a **Council-gated** VISION routing-claim resolution
   (Action 6) and a ruff-strictness decision that may surface real lint. Benefits
   from all prior lessons and is the only one with an external blocker.

**Rationale:** group by pattern, validate each pattern on its simplest instance,
and defer the largest + only-blocked repo to last. This matches the prompt's
default ordering (ai-council → corp-ops → corp-sca → corp-monorepo) with an
explicit pattern-validation justification rather than pure size ordering.

## Transferable patterns (lessons forward)

- **README disposition is per-repo and gates the doc-quality findings** — decide
  it first in every session. Default delete; corp-monorepo is the one to confirm
  as possibly external.
- **The audit tool under-reports for Pattern A, agrees for Pattern B.** A
  tool-green repo (ai-council, corp-monorepo) can be ~70% on full standard; a
  tool-red repo (corp-ops, corp-sca) is genuinely ~45%. Budget a read-only deep
  pass per repo regardless of the tool result.
- **Seed content lives in CLAUDE.md.** Every repo's CLAUDE.md already describes
  purpose (→ VISION) and structure (→ ARCHITECTURE); corp-sca's even carries a
  data-flow + Known-issues list (→ ARCHITECTURE + BACKLOG). Creation is mostly
  re-home, not authoring from scratch.
- **Match codemap form to source shape.** Real package graph → graphical Mermaid
  (corp-monorepo, corp-ops). Flat modules → text-only override (corp-sca). Never
  author empty CODEMAP markers implying a graph that doesn't exist.
- **Tier-residue is a multi-file pattern** (VISION frontmatter + CLAUDE prose +,
  for ai-council, `[L-opt]` section tags) — but **only** in repos that adopted the
  tier system. Don't hunt for residue in corp-ops/corp-sca; there is none.
- **`.env.example` removal is usually clean but check references first** — corp-sca
  is the exception (it's in the documented setup flow).
- **CHANGELOG retirement pairs with a JOURNAL question** in the creation repos
  (neither has a JOURNAL) — confirm git-history-as-record vs add JOURNAL.

## Open questions for operator

1. **corp-monorepo README** — delete (default) or keep as the one external/product
   repo? (The only README where keep-as-external is defensible.)
2. **corp-sca `.env.example`** — migrate env docs into CLAUDE.md and remove, or
   keep with a noted exception? (It is referenced by the setup flow.)
3. **CHANGELOG → JOURNAL** (corp-ops + corp-sca) — add JOURNAL.md or accept git
   history as the record?
4. **corp-monorepo ruff strictness** — adopt the stricter pyproject set (and fix
   resulting lint) or keep lenient?
5. **corp-monorepo VISION routing claim** — schedule the ai-council debate for
   Action 6 (consolidate routing vs amend §Values)?
6. **ai-council artifact migration** — move the two 2026-05-25 ai-council
   artifacts `docs/research/` → `docs/audits/` for convention consistency? (Separate
   cleanup; BACKLOG entry recommended.)

## What this synthesis does NOT include

- **Execution of any plan** — all four await dedicated per-repo sessions (run from
  each repo's own workdir, NOT from `.dev-knowledge`).
- **Methodology changes** (scrum-master review ADR, workspace-template framework
  fix) — `.dev-knowledge` standards work, out of scope.
- **Re-audit of ai-council** — the 2026-05-25 refresh is authoritative (HEAD
  unchanged at `2a980ab`).
- **Cross-repo migrations** (e.g., ai-council artifacts `docs/research/` →
  `docs/audits/`) — separate cleanup.
- **New BACKLOG entries** — this session reports; codification is separate.

## Next operator actions

1. Review all four plans (+ the ai-council 2026-05-25 plan in `docs/research/`).
2. Resolve the six open questions above (at minimum the README + `.env.example`
   decisions, which gate actions).
3. Per the recommended sequence: open a **dedicated repo session** (from that
   repo's own workdir, NOT `.dev-knowledge`), pass its execution plan as the brief,
   execute, and capture lessons forward to the next repo session.
4. Optionally land the scrum-master-review-authority codification ADR in
   `.dev-knowledge` in parallel (BACKLOG P1) so each reviewed repo cites a formal
   authority — a dependency to be aware of, not a hard gate.

---

**Contract preserved:** zero child-repo files modified (read-only per
ADR-28/ADR-36). All writes confined to `.dev-knowledge/docs/audits/`.
