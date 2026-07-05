# EPIC RETURN — llm-first-docs · (filled by the lane at close)
<!-- scope: meta -->

Required before any merge (HANDOFF_PROCESS §14b). Fill each section; keep the headers.
Closure is claimed on the epic done-contract's **hard metric**, never on "committed".

## 1. Commits + branch state

_One line per commit (sha + subject), oldest first. Branch state: clean tree? Suite green
ON THE BRANCH (paste the suite tail)._

## 2. Contract-vs-outcome per story

_Per story: **met / partial / dropped**, with evidence against its done-when._

## 3. Self-adjudications + ARCHITECT-REVIEW-PENDING

_Every judgment call made inside the lane's discretion, and every item deferred to the root._

### ESCALATION (blocking — persisted verbatim 2026-07-05 on root order; lane STOPPED at recon, zero story commits)

**STOP — escalating to root before any commit.** The epic's core done-contract collides with an out-of-boundary enforcement organ, and per the boundary contract ("a needed file outside the boundary → STOP, escalate — don't touch") this needs a root ruling before S1–S4 can proceed coherently. No files touched; branch `epic/llm-first-docs` still at `b501f86`, tree clean.

#### Probe gate (all PASS — lane booted, then blocked on recon)

```
E1 PASS  HEAD b501f86 · branch epic/llm-first-docs · tree clean
E2 PASS  live §14 opening quoted from protocols/HANDOFF_PROCESS.md
E3 PASS  main...HEAD diff empty (nothing touched yet)
E4 PASS* ship-gate RED: 10 WARNs dispositioned, 1 undispositioned —
         deployed_methodology_version reads the WORKTREE dirname
         ("epic-llm-first-docs" not in deployed-versions.yaml).
         Pre-existing worktree artifact, zero lane commits; deploy/** is
         forbidden to me. Flagged for root; expected green from primary.
E5 PASS  bundle = EPIC_BOOT + EPIC_RETURN (unfilled 5-section skeleton) + PROBES
```

#### The escalation: S2 cannot ship through the armed gates inside the FILE-BOUNDARY

**The collision.** S2's done-when is "hub `ARCHITECTURE.md` renders zero Mermaid." But the `codemap-freshness` pre-commit hook (`.pre-commit-config.yaml:28-33`) fires on **any** `ARCHITECTURE.md` change and runs `scripts.codemap.cli check`, which regenerates the codemap **as Mermaid** and hard-fails both possible S2 shapes — I verified the code paths in `scripts/codemap/check.py:40-65`:

- text form kept inside the `CODEMAP` markers → drift diff, exit 1 → commit blocked
- markers removed entirely → "markers not found", exit 3 → commit blocked

Both `.pre-commit-config.yaml` and `scripts/codemap/` are outside my may-touch list. The only in-boundary "fix" would be `--no-verify`/`SKIP` bypasses, which I refuse — it would also merge a permanently broken gate onto main (every future ARCHITECTURE.md edit fails the hook).

**Proposed resolution for root (minimal grant, coherent with the amendment's own logic).** The S1 amendment declares visualization a separate human-facing surface (future Tier-4). That lets `scripts/codemap/` **survive unchanged** as that future surface's generator — merely decoupled from canonical-doc gating. Then the extra grant shrinks to:

1. **`.pre-commit-config.yaml`** — remove the `codemap-freshness` hook entry (hub-local gate retire; mirrors what S3 already does to audit check #7 by explicit grant).
2. **`CLAUDE.md`** — two stale lines after S2: §4 "Persistent diagrams in `ARCHITECTURE.md` are mermaid (ADR-51/ADR-59)" and the §9 `codemap-freshness` hook row. Alternatively root reconciles CLAUDE.md itself at integration (v2.29-precedent style) — either works; I just can't leave them uncorrected silently.
3. **No change needed** to `scripts/codemap/`, `tests/test_codemap.py` (tool untouched → its tests stay green), or `safe_removal` (no module removed).

**Deliberately deferred to root / follow-up ticket (not lane work):** the consumer-facing Mermaid surfaces — `.pre-commit-hooks.yaml` exported `codemap-freshness`/`codemap-generate` hooks and the `deploy/manifest-v*.yaml` precommit carriers (deploy/** is FORBIDDEN to this lane; consumer rollout is versioned-corpus territory, ADR-91); plus `ecosystem/*/state.yaml` `mermaid_theme_directive` evidence rows (regenerated artifacts) and child-repo ARCHITECTURE files that check #7 currently scans cross-repo.

**Also noting (escalation item 3 — listed, not chased):** one living doc outside the boundary carries Mermaid: `docs/handoffs/README.md` (the canonical operator runbook). Audits/old bundles are immutable per ADR-39 and correctly out of scope.

#### Why the lane is not doing S1/S3/S4 first

They're in-boundary, but the amendment's text (S1) and check #7's replacement shape (S3) must state what happens to the codemap generator and its freshness gate — that's exactly the thing under ruling. Authoring first risks an amendment the ruling contradicts, and ADRs/amendments are immutable once landed.

**Awaiting root's ruling** (via operator paste-back into this lane): approve the grant extension as proposed — items 1 and 2, or item 1 plus root-side CLAUDE.md reconciliation at integration — or reshape S2. On receipt the lane executes S1→S4 in order, commit-per-story, re-running E3 at each commit.

## 4. Proposed BACKLOG delta

_Structural changes for the ROOT to apply at integration (new stories, re-scoping,
closures) — the lane never applies these itself (BACKLOG single-writer for structure,
ADR-97)._

## 5. Merge-readiness checklist

- [ ] Diff touches ONLY the declared FILE-BOUNDARY (`git diff --name-only main...HEAD` audited)
- [ ] No merges to main performed from this lane
- [ ] JOURNAL entry on the branch names this lane's session SHAs
- [ ] Working tree clean; suite green on the branch
