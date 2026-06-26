# PLAYBOOK condensation — rule-inventory diff (SEAL-1a, [#213])

**Date:** 2026-06-26
**Branch:** `docs/playbook-condensation` (commits Group 0 + A–F; **not merged** — operator integrates after review)
**Arc:** SEAL-1a — separate rule from rationale/history in `protocols/PLAYBOOK.md`, lose zero rules, organize around the two-lifelines spine.
**Closure metric (HARD):** every rule that was in PLAYBOOK is still reachable afterward — in place, or via a pointer to its LESSONS/ADR home. This file is the proof.

---

## 1. Headline

- **HARD metric — MET.** Zero rules removed. Every relocation moved an *incident / dated-provenance / redundant-restatement*, not a rule; each has a pointer to its (pre-existing) LESSONS/ADR home. Verified below per group.
- **Inbound-pointer integrity — MET.** No chapter/section renumbered; every `##`/`###` heading title preserved verbatim. All 14 `## ChN.` + 18 Part-II `## N.` headings present (§18 intentionally gapped). The one *live* line-number referrer (`scripts/audit.py` docstring `§924`) was de-referenced to a stable section name. The many `L<n>` referrers in `docs/audits/*.md` are immutable dated records (ADR-60 Rule 5) — correctly left frozen.
- **Frame-as-spine — MET.** `## The two lifelines` extended with a chapter→lifeline map (Lifeline 1 / Lifeline 2 / cross-cutting) — a mapping layer above Part I, not a renumber.
- **Drift reconciled (surfaced, not silent) — see §4.** Ch8 carried a refuted claim ("native `claude --worktree` auto-seeds `ecosystem/*/state.yaml` for you", verified 2026-06-18); reconciled to the canonical n=3 finding (LESSONS 2026-06-19).
- **Size byproduct — reported honestly: 3410 → 3386 = −24 lines (~0.7%).** Far below the prompt's ~1500 target and below the plan's ~2600–2950 honest band. **Why, and the held-back lever: §5.** No rule was cut to chase a number (the size-yields-to-substance guard).

---

## 2. Per-group rule-preservation map (the proof)

Legend: **RULE KEPT** = the actionable rule stayed in place · **moved→** = incident/provenance relocated to an existing home + pointer · **reconciled→** = stale claim aligned to canonical home.

### Group A — spine + Ch1–Ch4 (commit e3b8752)
| Item | Disposition |
|---|---|
| Chapter→lifeline map | ADDED to the spine (net-positive organizing layer; no rule). |
| Ch2 "LLM-LLM context transfer" rule | **RULE KEPT** (sender verifies inline; receiver asks back; applies broadly). |
| Ch2 v4.1 "aborted folder" war-story | moved→ LESSONS 2026-05-30 (pointer left in place). |

### Group B — Ch5–Ch7 (commit f755584)
| Item | Disposition |
|---|---|
| Ch5 circular-testing guard + "Teeth check" + "The rule" | **RULE KEPT** verbatim. |
| Ch5 #141 vacuous-claim-3 worked-example (~16 ln) | compressed-in-place to ~8 ln (kept the vacuous pattern `!= "skipped" or actual`, the fix, the test ref). Not in LESSONS → kept inline as teaching, trimmed. |
| Ch6 freshness/amendment/reconciled "honest limits" prose | **RULE KEPT** (the honest-limit statement *is* the rule). |
| Ch7 review postures | **RULE KEPT** (verbatim-from-audit). |

### Group C — Ch8 keystone (commit 47f655a)
| Item | Disposition |
|---|---|
| Decide-first checklist (0), native command, shared-canonical handling, integration-from-primary, #200 six-bullet merge-serialization mechanism, teardown 3-command round-trip, no-leftovers invariant | **RULE KEPT** (every rule). |
| 49c7db7 shared-checkout sweep narrative | moved→ LESSONS 2026-06-07 / 2026-06-05. |
| `.dev-knowledge-*` sibling-orphan war-story | moved→ LESSONS 2026-06-02. |
| 2026-06-15 smoke-test / 2026-06-18 verification dates; #200 "closed accepted-prose-only" provenance | trimmed (provenance; test reference kept as the verify anchor). |
| "native auto-seeds for you" claim (×5 occurrences) | **reconciled→** the n=3 rule "seed from the primary; don't rely on auto-seed" (LESSONS 2026-06-19). See §4. |
| Raw-`git worktree add` fallback recipe (PowerShell block) | **KEPT in body** — its appendix move is 1e/#214's scope; only the dated narration around it was trimmed. |

### Group D — Ch9–Ch14 (commit a1d9971)
| Item | Disposition |
|---|---|
| Ch10 two-tier doctrine; Ch11 cloud-routine rules + 7-point operational standard; Ch12 ADR-81(a)–(d) + 6-point shipped-gate + ex-ante contract | **RULE KEPT** (dense doctrine, pointer-form provenance already). |
| Ch14 7d "Amendment 2026-04-25 (subagents factually active)" note | moved→ git (section-history per ADR-49; the current subagent rule is untouched). |
| Ch10 + Ch11 duplicated `221c63e` SHA / "PR #17 squash-merged to main as" provenance | trimmed to "witnessed 2026-06-07 PR#17"; the by-design rule kept verbatim. |

### Group E — Part II §1–§19 + Appendices (commit 929f8af)
| Item | Disposition |
|---|---|
| §1–§4, §6–§17, Appendices A–C, Codemap, Auto-TOC | **RULE/REFERENCE KEPT** (recipes/templates/schema; #158-pointerized). |
| §5 "Pattern emerged organically 2026-04-24 — used 3 times" list | collapsed to a one-line pointer (the same 3 amendments are covered fully in the "Examples (2026-04-24)" table below it — intra-section redundancy). |
| §5 "Retroactive archive recovered 5 debates" incident | dropped (rule + accumulation anti-pattern stand alone). |
| §5 decision-pattern Example tables (Council-vs-single, Amendment) | **KEPT** as teaching (per plan). |
| §19 scrum-master empirical reference (I7/I8 specifics) | trimmed to a pointer at the audit file; addendum-mechanism rule kept. |

### Group F — finalize (this commit)
| Item | Disposition |
|---|---|
| `scripts/audit.py` `check_no_sibling_orphans` docstring `PLAYBOOK G5 §924` | de-referenced to `PLAYBOOK "No leftovers ... invariant"` (stable name, no line-number drift). |
| This rule-inventory artifact | added (dated/immutable). |

---

## 3. Inbound-pointer integrity — detail

- **NAME-style pointers** (e.g. `PLAYBOOK "Routine/night deployment standard"`, `"Two-tier automation doctrine"`, `"Subagents"`, `"Project complexity bands"`, `"Canonical-file freshness cadence"`, `"Universal visual pattern"`, `"No leftovers"`) — all target titles preserved verbatim. RESOLVE.
- **NUMBER-style pointers** (`PLAYBOOK §2/§4/§5/§7/§8/§9/§10/§13`, `Ch4`, etc.) — no chapter/section renumbered; §18 gap + its `structure-allow` marker preserved. RESOLVE (any that were stale before this arc remain exactly as they were — not this arc's scope; ESSENTIALS reconciliation is the NEXT arc).
- **LINE-style pointers** — the only *live* one (`audit.py` docstring `§924`) de-referenced to a name. All others are in immutable `docs/audits/*.md` (frozen at their dates per ADR-60 Rule 5; not rewritten).
- Machine confirmation each group: `validate_doc_structure: OK` (numbering / headers / ToC / heading-scheme), TOC regeneration a no-op every group (no heading added/removed/renamed).

---

## 4. The seed-claim reconciliation (surfaced for explicit review)

Ch8 repeatedly asserted the **native** `claude --worktree` path "auto-seeds `ecosystem/*/state.yaml` for you" — including a "**Verified 2026-06-18**" block claiming all 5 state files seeded with no manual step. That claim is **refuted** by **LESSONS 2026-06-19** (n=3: *neither* native nor raw `git worktree add` reliably auto-seeds; the one 2026-06-18 pass over-generalized) and by the `seed-state-yaml` memory ("the 'native seeds' distinction is refuted").

Faithfully condensing would have carried a **known-false rule** forward. So every occurrence (5 sites) was reconciled to the canonical rule: **treat a fresh worktree as unseeded by default; seed `ecosystem/*/state.yaml` from the primary before the first commit; do not rely on the auto-copy.** This is a content change beyond pure condensation — flagged here and in the Group-C commit body so it is a *deliberate, easily-revertable* coherence fix, not a silent edit. If the operator prefers the literal-preservation reading, revert commit 47f655a's seed bullets.

---

## 5. Honest size accounting + the held-back lever

**−24 lines is small. The honest reasons:**
1. **PLAYBOOK was already lean.** The #158 pass pointerized the compressible doctrine into ADRs ("Not restated here"). The residual genuinely-relocatable incident/history was **~30 lines**, not the 450–650 the plan estimated (which was itself below the original ~1900-line implied ask).
2. **Most "long sections" are irreducible rule**, not war-story — the worktree keystone (Ch8) is mostly the decide-first / integration / teardown *rules*; Ch10–Ch12 are dense doctrine; Ch6's "honest limits" prose *is* the rule.
3. **Incidents already live in LESSONS.** Relocation was overwhelmingly "trim the duplicated war-story to its existing LESSONS pointer," which removes few lines because PLAYBOOK only carried brief mentions, not the full narrative.

**The lever I deliberately did NOT pull** (per the approved "keep reference doctrine" posture): compressing verbose **reference** — Ch14's 4× `When to use / When NOT / Real examples / Anti-patterns` parallel structure (~150 ln of the ~300-ln chapter), the Ch5 VS Code workspace templates (~70 ln; cf. #16), the §2/§5 protocol prose. That is a *different, riskier* kind of cut (thinning reference, not relocating history) with a real "thinner-reference" downside. **Operator's call** whether to authorize a reference-compression pass for a larger reduction; it is not part of this approved arc and was not done unilaterally.

---

## 6. Gate evidence

Per-group cadence GREEN throughout: `validate_doc_structure: OK` · TOC regeneration no-op · `audit.py ship-gate: GREEN` (4 pre-existing WARNs dispositioned) · targeted doc/toc/merge-serialization tests pass · full `pytest` 854 passed (Group 0 baseline; re-run at Group F). `validate_backlog: OK` (84→87 tasks). No new WARN introduced.
