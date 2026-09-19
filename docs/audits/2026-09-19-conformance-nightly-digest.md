<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-19

**Date:** 2026-09-19
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded**, second consecutive clean run (2026-09-18 was the first). `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`) and ran to completion in one pass — no spec-orchestration fallback needed.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 82,997 | 15 | 118s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 123,312 | 26 | 265s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 135,270 | 48 | 370s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 76,103 | 23 | 150s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 52,519 | 1 | 36s |

Total: 470,201 subagent tokens, 113 tool calls, ~683s (11.4 min) wall time.

**Platform re-probe signal — concurrency regression.** On 2026-09-18 all 3 Stage-1 verifiers ran fully concurrently (wall time ≈ max(92,203,121)s + skeptic + digest ≈ 318s total). Tonight, V1 and V2 started together as expected, but **V3 did not start until V1 finished** (`V3 startedAt` = 1789780268464 ms, ~1.5s after `V1`'s `lastProgressAt`, despite all three being `queuedAt` within the same 40ms window and the script issuing one `parallel([v1,v2,v3])` call). This reads as a session-level concurrency cap of 2 simultaneous Stage-1 subagents tonight, not a script defect — the script's `parallel()` call is unchanged from 2026-09-18. It cost roughly the extra ~118s of serial V1→V3 handoff visible in tonight's longer total wall time. Not a doc-conformance finding; flagged for the platform re-probe record only.

**Harness safety-neutralization fired 3 times (non-incident).** The workflow's own instruction-shaped-content guard fired on the V2, skeptic, and digest agent outputs: `[harness: subagent output matched instruction-shaped pattern(s): settings-json. Control tags below are neutralized...]`. Investigated: this traces to `.claude/settings.json`'s own comment key `//hooks-EMERGENCY-DISABLED-2026-09-17`, whose value ("ALL PreToolUse hooks are DISABLED 2026-09-17 by operator emergency order...") reads as an imperative instruction when quoted verbatim inside a verifier's structured-output string field. This is the repo's own tracked configuration content being cited as evidence (correctly — see Finding D below), not an external or adversarial injection attempt; no verifier's actual behavior was redirected by it. Noting for transparency per this reviewer's standing instruction to flag suspected-injection-shaped content, and because it explains the neutralized `<` characters if the operator inspects raw agent transcripts.

**Known-advisory infra note (unrelated to doc conformance):** the session's Stop-hook backpressure fired repeatedly throughout this run with `Required uv version ==0.11.19 does not match the running version 0.8.17`. Same systemic mismatch flagged in the 2026-08-10 digest's Next Actions #7 and the 2026-09-18 digest, now **40+ days unresolved**. Advisory-only per `CLAUDE.md` §9 ("Stop backpressure (advisory)") — not a doc-conformance finding.

**Environment note:** during Stage 2, the skeptic agent ran `git fetch --unshallow` (read-only with respect to tracked files — no working-tree write) to resolve a shallow-clone false-negative (see Finding E below). This session's clone is consequently no longer shallow (7,973 commits now visible vs. the prior shallow boundary); `git status --porcelain` confirms no tracked file was touched by this.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-09-18-conformance-nightly-digest.md`, fetched read-only from the **unmerged** branch `origin/claude/conformance-2026-09-18` (`git show origin/claude/conformance-2026-09-18:docs/audits/2026-09-18-conformance-nightly-digest.md`). No `docs/audits/*-conformance-nightly-digest.md` file with a higher date exists on `main` — the most recent merged one is still 2026-08-10. `origin/claude/conformance-2026-09-18` is the only other `claude/conformance-*` branch on origin. `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` has a date between these but is a differently-scoped, differently-shaped artifact (a one-off `[#171]` dashboard review, no counts-marker contract) — not used, consistent with the 09-18 digest's own reasoning for excluding it.
**Gap:** 1 day (2026-09-18 → 2026-09-19).

All 5 of 2026-09-18's survivors were independently re-checked against current `origin/main` (`14d273f`) with fresh evidence:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING** | prior HIGH: `docs/archive/VISION.md:16-19` self-describes as `CANONICAL_MANDATORY[0]` / MUST on all nine ADR-104 fleet members; ADR-114 retired it to `CANONICAL_RETIRED` | Re-raised independently by tonight's V2 and re-verified by tonight's skeptic (see Finding 1 below) — `python3 -c "import canonical_docs as c; ..."` still prints VISION in `CANONICAL_RETIRED`, not `CANONICAL_MANDATORY`. Text at `VISION.md:16-19` unchanged. |
| **RETRACTED — baseline finding invalidated** | prior HIGH: 15 "Proving SHA" values in the 2026-09-16 closure census / `tasks/470-*.md` etc. do not exist as git objects | Tonight's V3 independently re-raised the same claim (16 SHAs, near-identical set), but tonight's skeptic ran `git fetch --unshallow` and re-tested: **all 16 SHAs resolve as real, reachable ancestor commits** once full history is fetched (e.g. `09fd7a00` — subject line literally names `[#613]`, the row it's cited for). The 2026-08-10→09-18 lineage never ran this repo unshallowed for a backlog-domain check; `conformance-hub.js`'s `SHALLOW-HISTORY GUARD` text exists only in the **V1** (JOURNAL) prompt, not V2 or V3 — see Next Actions #1. This means the 2026-09-18 digest's HIGH "fabricated closure evidence" finding was almost certainly **itself a false positive** caused by the same shallow-clone gap, not a real provenance defect. Not counted as "resolved" (nothing was fixed) or "persisting" (the underlying claim is false) — recorded as **retracted**. |
| **PERSISTING** | prior MED: `docs/archive/VISION.md:18-19` overstates its own machine-site footprint ("thirteen machine constants plus five deploy manifests" vs actual eleven sites / six manifests) | Not re-raised by tonight's V1/V2/V3 fan-out (verifier-coverage gap, same file/paragraph as the finding above — one re-read would catch both). Independently re-verified by this session: `grep -n "thirteen machine constants plus five deploy" docs/archive/VISION.md` → still present verbatim at line 18. |
| **PERSISTING** | prior MED: the synced anti-pattern text's "43.50 KiB / 32 KiB cap" figure is stale in `CLAUDE.md`, `AGENTS.md`, `templates/claude-regions/antipatterns-universal.md`, `CONTRIBUTING.md` | Not re-raised tonight. Independently re-verified: `grep -rn "43.50 KiB" CLAUDE.md AGENTS.md templates/claude-regions/antipatterns-universal.md CONTRIBUTING.md` → all 4 hits still present. Current `wc -c CLAUDE.md AGENTS.md` = 24,561 + 5,843 = 30,404 B (29.69 KiB) — still under the 32 KiB cap, but the stale absolute figure remains wrong and the margin has narrowed since 2026-09-18. |
| **PERSISTING** | prior LOW: `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count (5,714 B vs actual) | Not re-raised tonight. Independently re-verified: `CONTRIBUTING.md:19` still reads "5,714 B"; `wc -c AGENTS.md` → 5,843 B. |

**NEW this cycle** (3 findings, all survived the skeptic):

| Status | Finding | Severity |
|---|---|---|
| **NEW** | `ARCHITECTURE.md:17-24`'s BUILD MODE header note claims only `audit-index-freshness`/`organ-index-freshness` (pre-commit) and the two `block-*-push` hooks run locally since 2026-09-17; the 2026-09-18 B2-lane4 review re-armed 9+ more pre-commit-stage hooks the same day the note's own `last_reviewed` stamp claims currency | HIGH |
| **NEW** | `CLAUDE.md:65` and `AGENTS.md:66` state "`ruff check` is also a pre-commit gate ... and blocks"; the `ruff` hook is `stages: [manual]` with an explicit "NOT RE-ARMED 2026-09-18" comment — report-only via the Actions conductor, not a local blocking gate | HIGH |
| **NEW** | `CLAUDE.md:80` states "the ADR-77 guard stays armed"; `CLAUDE.md:200` (§9) says "the ADR-77 guard stays off ([#863])"; `.claude/settings.json` confirms §9 is correct — an internal self-contradiction within one file | MED |

**Delta counts:** 0 resolved · 1 retracted (false positive) · 4 persisting · 3 new
**This run's own raw → survived → killed:** 5 → 4 → 1
**Skeptic kill-rate:** 20% (1 of 5) — the kill was a genuine correction (shallow-clone artifact), not a weak-evidence call; the skeptic re-ran the disproving command itself (`git fetch --unshallow` + `git cat-file -t` + `git merge-base --is-ancestor`) before killing.

---

## Summary

Tonight's independent fan-out raised 5 findings; 4 survived adversarial review and 1 was killed as a genuine false positive traceable to a shallow-clone artifact — an artifact that, on closer look, almost certainly also produced the prior baseline's headline HIGH finding ("15 fabricated closure SHAs"), which this digest is retracting rather than carrying forward as resolved or persisting. Net doc-health picture: zero items from the 2026-09-18 baseline were actually fixed since yesterday. Four of that baseline's five survivors persist unchanged (one independently re-confirmed by tonight's own pipeline, three not re-caught by tonight's verifier coverage but still verifiably present on disk), and three new items surfaced — all in the same family as the carried findings: a living doc (`ARCHITECTURE.md`, `CLAUDE.md`/`AGENTS.md`) describing a pre-dates-itself state that a same-day or prior operator decision already superseded. The `CLAUDE.md` self-contradiction (armed at §4 line 80, off at §9 line 200) is the sharpest instance: the file disagrees with itself, and the live `.claude/settings.json` sides with §9.

The more consequential finding for the record is procedural, not a specific doc drift: this pipeline's `SHALLOW-HISTORY GUARD` is written into only the V1 (JOURNAL) prompt in `conformance-hub.js`, not V2 or V3. Both of the last two nights' backlog-domain runs (2026-09-18 and tonight) independently rediscovered the same 15–16 "missing" closure SHAs — tonight's skeptic happened to unshallow and disprove it; last night's skeptic did not and let a false HIGH ride into a merged-worthy digest. The underlying closure provenance for `#470`, `#587`, `#613`, and the rest of that batch is very likely intact; the prior digest's claim that it was "fabricated/unverifiable" should not be acted on.

<!-- counts: raw=5 survived=4 killed=1 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 5 · **Survived skeptic:** 4 · **Killed false positives:** 1
**Plus 3 persisting findings carried forward from the 2026-09-18 run (independently re-verified above with fresh evidence, not re-run through tonight's skeptic pipeline) and 1 retraction of a prior HIGH finding**

### High (3)

**PERSISTING — carried, independently re-caught tonight** — `docs/archive/VISION.md:16-19` self-describes a MUST-tier tracking status ADR-114 retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members ... it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-18`
- **Evidence:** `python3 -c "import sys; sys.path.insert(0,'scripts'); import canonical_docs as c; print(c.CANONICAL_MANDATORY[0]); print(c.VISION in c.CANONICAL_MANDATORY); print(c.VISION in c.CANONICAL_RETIRED)"` → prints `ARCHITECTURE.md`, `False`, `True`.
- **Verdict:** contradicted
- **Proposed fix:** Rewrite VISION.md's "why this file is still here" paragraph to state its actual current status (`CANONICAL_RETIRED`, not `CANONICAL_MANDATORY[0]`, per ADR-114) instead of its pre-ADR-114 status.
- **Note:** Unchanged since 2026-09-18; ADR-114 (`docs/decisions/ADR-114-readme-recreation-legality.md:10-11`) is the documented decision the file itself fails to reflect, so this is not killable as "documented-decision" — the decision is exactly what's unpropagated. Same paragraph also carries the still-unfixed machine-site-footprint MED below; one re-read closes both.

**NEW** — `ARCHITECTURE.md:17-24`'s BUILD MODE header note is stale against the 2026-09-18 B2-lane4 hook re-arm
- **Claim:** "since 2026-09-17 only `audit-index-freshness`, `organ-index-freshness` (pre-commit) and `block-ff-push`, `block-unanchored-push` (pre-push) run locally; the rest of `.pre-commit-config.yaml` is `stages: [manual]`."
- **Location:** `ARCHITECTURE.md:17-24` (the file's own `last_reviewed` stamp is 2026-09-18, the same day this claim went stale)
- **Evidence:** `grep -n -A3 'id: codemap-freshness$' .pre-commit-config.yaml; grep -n -A3 'id: validate-hermetization$' .pre-commit-config.yaml; grep -n -A3 'id: row-archive-proof$' .pre-commit-config.yaml` — none carry a `stages:` override; all three (plus 7 more) carry a `# RE-ARMED 2026-09-18 (B2 lane4 hook-role review)` comment and inherit the default pre-commit stage.
- **Verdict:** contradicted
- **Proposed fix:** Update the header note to cite the 2026-09-18 B2-lane4 re-arming (`docs/audits/2026-09-18-technical-b2-lane4-hook-role-review.md`), matching `CLAUDE.md` §9's own accurate "B2 lane4 armed 13" line.
- **Note:** Skeptic confirmed by direct inspection of `.pre-commit-config.yaml`; `CLAUDE.md` §9 already states the correct current count, so this is `ARCHITECTURE.md` specifically lagging a sibling doc and the live config, not a documented-decision non-issue.

**NEW** — `CLAUDE.md:65` / `AGENTS.md:66` claim ruff "blocks" as a pre-commit gate; it is currently report-only
- **Claim:** "`uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks."
- **Location:** `CLAUDE.md:65`; `AGENTS.md:66`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, with comment "NOT RE-ARMED 2026-09-18 (B2 lane4 hook-role review) ... Left manual; flagged as a B3+ candidate. Rule 7 stands: no counter, no arm."
- **Verdict:** contradicted
- **Proposed fix:** Reword to state ruff is currently `stages: [manual]` / report-only via the Actions conductor, pending a B3+ re-arm decision, rather than "a pre-commit gate ... that blocks."
- **Note:** The documented decision (leaving ruff manual) is exactly what these two files fail to reflect — not a documented-decision kill. (`CONTRIBUTING.md` does not exist at repo root; the 2026-09-18 finding's phantom third citation to it was itself slightly inaccurate.)

### Med (2)

**NEW** — `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status
- **Claim:** `CLAUDE.md:80` (§4): "the ADR-77 guard stays armed" vs. `CLAUDE.md:200` (§9): "the ADR-77 guard stays off ([#863])."
- **Location:** `CLAUDE.md:80` vs `CLAUDE.md:200`
- **Evidence:** `grep -n -i 'ADR-77' .claude/settings.json CLAUDE.md` → `.claude/settings.json` key `//hooks-EMERGENCY-DISABLED-2026-09-17`: "ALL PreToolUse hooks are DISABLED 2026-09-17 by operator emergency order ... the ADR-77 transcript guard (`python scripts/hooks/block_immutable_edits.py`) ... with them."
- **Verdict:** contradicted
- **Proposed fix:** Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," matching §9 and the live `settings.json` emergency-disable entry.
- **Note:** Plain internal self-contradiction within one file — §9 is already correct, only §4 needs the fix. Not explainable by a documented decision (the decision is that it's off; line 80 is the stale half).

**PERSISTING — carried, not re-caught this cycle** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine."
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `grep -n "thirteen machine constants plus five deploy" docs/archive/VISION.md` → still present, line 18.
- **Verdict:** contradicted (per the 2026-09-18 digest's own re-verified counts: eleven sites / six manifests)
- **Proposed fix:** Correct the counts, or drop the hardcoded numbers per the hub's own "never restate a count or roster in prose" convention (`CLAUDE.md` §4). Same re-read as the HIGH VISION.md finding above closes this too.
- **Note:** Tonight's V2 did not independently re-derive this count (verifier-coverage gap, not evidence the claim became true) — carried forward on the strength of the 2026-09-18 digest's own verification plus tonight's direct grep confirming the text is unchanged.

### Low (1)

**PERSISTING — carried, not re-caught this cycle** — `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count
- **Claim:** "`AGENTS.md` — now exists" (added 2026-08-29, 5,714 B).
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B (unchanged from the 2026-09-18 measurement).
- **Verdict:** contradicted
- **Proposed fix:** Update the byte figure or drop the hardcoded count.
- **Note:** Not re-raised by tonight's V2 fan-out; carried forward on direct re-verification.

---

## Retracted Finding (correction to the 2026-09-18 baseline)

**RETRACTED** — 2026-09-18's HIGH finding "15 Proving SHA values in the 2026-09-16 closure census do not exist in git" — likely a false positive
- **Original claim (2026-09-18):** Commit `0c120be` and `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md` cite "Proving SHA" values for closed `BACKLOG.md` rows that fail `git cat-file -t`.
- **Tonight's re-derivation:** V3 independently raised the same claim (16 near-identical SHAs). The skeptic ran `git fetch --unshallow` (read-only w.r.t. tracked files) and re-ran `git cat-file -t` on all 16 — **every one now resolves** as a real, reachable commit (`git merge-base --is-ancestor` confirmed at least two, e.g. `09fd7a00`, whose own subject line names `[#613]`, the row it's cited for).
- **Root cause:** the repo clone was shallow at evidence-collection time on both 2026-09-18 and tonight (until the skeptic unshallowed it); `git cat-file -t` on a shallow clone reports "Not a valid object name" for any real commit older than the shallow boundary. `conformance-hub.js`'s `SHALLOW-HISTORY GUARD` text exists only in the V1 (JOURNAL) prompt — see Next Actions #1.
- **Disposition:** Do not act on the 2026-09-18 digest's HIGH finding of this shape. The underlying closure provenance for the affected rows (`#470`, `#587`, `#591`, `#592`, `#596`, `#597`, `#600`, `#601`, `#605`, `#608`, `#613`, `#626`, `#643`, `#653`, `#740`, `#742`) appears intact once full history is consulted.

---

## Killed Findings

**Killed (1 of 5 raw this cycle):**

- **Claim:** "Commit `0c120be` and `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md` cite 16 of 25 'Proving SHA' values that are not valid git objects anywhere in the repo, so the closure trail is fabricated/unverifiable for those rows."
- **Kill reason:** evidence-not-definitive
- **Kill detail:** The `evidence_command` was run against a shallow clone. `git fetch --unshallow origin` (read-only re: tracked files) followed by the identical `git cat-file -t` command shows all 16 SHAs resolve to real commits, at least two of which (`f903a24f`, `09fd7a00`) were spot-checked as genuine ancestors of HEAD with subject lines matching the rows they're cited for. See "Retracted Finding" above for the fuller writeup, since this kill directly corrects the prior digest.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries through 2026-09-19):**
- All merge-chain anchors (6fc296d8, ee40592a, beae756e) and the full `4377e72..14d273f` merge sequence resolve and match the JOURNAL's claimed order exactly, with no unmentioned merges ✓
- `automation/fleet-audit` and `origin/claude/conformance-2026-09-18` remote branches exist as claimed (KEPT disposition) ✓
- Codex review commit `aa410ec6`'s claimed 1-HIGH/0-0-0-0 heuristic-line mismatch verified verbatim; commit `80df0753`'s test-replacement diff and `548b2cf7`'s baseline-raise diff (447→452, 62→71) both match their JOURNAL descriptions exactly ✓

**V2 (living-doc factual claims):**
- `CLAUDE.md` byte size (24,561 B) is within its own stated ≤24,576 B cap, gated by `tests/test_claude_md_byte_cap.py` ✓
- `ARCHITECTURE.md`'s "organ map ... 8 classes" matches `ecosystem/organ-index.md`'s 8 actual `## ` headings ✓
- `ARCHITECTURE.md`'s generated quality-requirements block (29 total / 8 measured / 21 candidate) matches `ecosystem/quality-requirements.yaml` exactly ✓
- `CLAUDE.md` §7's repo-command roster and §11's recent-ADR roster both match disk exactly ✓
- `CLAUDE.md` §9's own "ADR-77 guard stays off ([#863])" line is itself accurate against `.claude/settings.json` — the contradiction is with §4 line 80, not with reality ✓

**V3 (BACKLOG closure semantic coherence):**
- `#750` merge-receipt and `#785` provider-bench rows: Done-when criteria delivered verbatim by their cited commits, evidence hashes resolve ✓
- `#613` in-repo routing table row: closed transparently as CLOSE-PRE with the live-table test left explicitly RED and a tracked follow-up (`#829`) filed — not a deceptive partial closure ✓
- BUILD MODE (B2) commits with no `[#id]` tag are correctly ungoverned by `BACKLOG.md` per `protocols/BUILD-MODE.md` rule 1 (a flat build list, not an omission) ✓
- No literal `closes [#id]` commit-trailer convention exists in this repo; closures are tracked via `tasks/<id>-*.md` `status: closed` + inline `CLOSED` markers instead ✓

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent)** Extend `conformance-hub.js`'s `SHALLOW-HISTORY GUARD` text (currently only in the V1 prompt) to the V2 and V3 prompts too. Two consecutive nights independently rediscovered the same shallow-clone false-positive in the backlog-closures domain; only tonight's skeptic happened to catch it. Without this, a future HIGH "fabricated evidence" finding of this exact shape could reach a merged digest unchallenged.
2. **HIGH — carried** — Re-read `docs/archive/VISION.md:16-19` end-to-end: fix the `CANONICAL_RETIRED` status claim and the machine-site/manifest counts in one pass (closes both the HIGH and the carried MED below).
3. **HIGH — new** — Update `ARCHITECTURE.md`'s BUILD MODE header note (lines 17-24) to cite the 2026-09-18 B2-lane4 re-arm instead of the pre-lane4 2-hook framing.
4. **HIGH — new** — Correct `CLAUDE.md:65` and `AGENTS.md:66` to describe `ruff` as currently `stages: [manual]` / report-only, not "a pre-commit gate ... that blocks."
5. **MED — new** — Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," resolving the self-contradiction with `CLAUDE.md:200`.
6. **LOW — carried** — Update `CONTRIBUTING.md:19`'s `AGENTS.md` byte figure (5,714 B → 5,843 B), or drop the hardcoded count.
7. **(CORRECTION)** Do not act on the 2026-09-18 digest's HIGH "15 fabricated Proving SHA" finding — see Retracted Finding above. If that finding already prompted a reopen-pending-evidence action on any of the named rows, it should be reconsidered.
8. **(INFRASTRUCTURE, persisting since ≥2026-08-02, now 40+ nights unresolved)** Upgrade cloud runtime `uv` to `==0.11.19`. Fires on every Stop-hook check.
9. **(PROCESS, positive-but-mixed signal)** The native `Workflow` launcher has now run cleanly end-to-end two nights running, but tonight showed an apparent concurrency cap (2 simultaneous Stage-1 subagents instead of 3) that roughly doubled wall time vs. 2026-09-18. Worth watching whether this recurs.
10. **(PROCESS, operator-consumption gap, same shape as the prior [#426] finding)** This is the **second** consecutive night's digest sitting on an unmerged `claude/conformance-*` branch — `origin/claude/conformance-2026-09-18` was never absorbed into `main`, and tonight's branch will be the same until absorbed. Every finding above, including this digest's own correction of the 2026-09-18 HIGH finding, is invisible to anyone who only reads `main`.

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-19-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
