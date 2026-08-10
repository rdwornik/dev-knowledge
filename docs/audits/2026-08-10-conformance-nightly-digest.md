<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-10

**Date:** 2026-08-10
**Author:** Claude Code (claude-sonnet-5), spec-orchestration fallback (native launcher attempted and failed — see Run below)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** Native `Workflow` launcher was **attempted first** (`.claude/workflows/conformance-hub.js` via the Workflow tool, name `"conformance-hub"`) per the re-probe instruction. This is the first night the launcher tool itself was available and accepted the job — a change from all six prior nightly runs (2026-08-03 through 2026-08-09), which recorded it as "not enabled in this cloud runtime."

**But it failed, not merely absent.** All 3 Stage-1 verifier subagents hit `StructuredOutput retry cap (5) exceeded`. Reading the subagent transcripts (`agent-ab4df74f1efa1ba11.jsonl` etc.) shows the actual cause: every tool call the workflow-subagents made — Read, Bash, Grep, and even the terminal `StructuredOutput` call itself — was rejected by the permission-handler layer with `"The permission handler returned updatedInput that failed schema validation: required parameter missing"`, despite valid parameters being supplied each time, across multiple retries and multiple distinct tools. One subagent's own diagnostic summary called it verbatim: `"Tooling environment fault... not an issue with the request."` This reads as a genuine harness bug specific to the `Workflow` tool's subagent-permission plumbing in this session, not a content or schema-design problem in `conformance-hub.js`.

Because the failure mode was a hard tool-plumbing fault (not "tool unavailable or auto-denied"), and because it affected all 3 parallel verifiers identically, this run treated it as non-functional for tonight and fell back to **SPEC-ORCHESTRATION**: reading `conformance-hub.js` as the canonical specification and reproducing its exact stage prompts/schemas via the `Agent` tool (`Explore` subagent type — read-only by tool grant, no Edit/Write available).

| Stage | Label | Model actually used |
|---|---|---|
| Native attempt (failed) | `conformance-hub` Workflow, Stage 1 (V1/V2/V3) | claude-sonnet-5 (per script's `model: 'claude-sonnet-5'` pin) — all 3 failed on StructuredOutput/permission-handler fault before producing output |
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent, fallback) | claude-sonnet-5 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent, fallback) | claude-sonnet-5 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent, fallback) | claude-sonnet-5 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent, fallback) | claude-sonnet-5 |
| Stage 3 — digest | synthesized by orchestrator (this file) | claude-sonnet-5 |

**Platform re-probe signal for the operator:** `CONTRIBUTING.md:155-156` currently states *"the native `Workflow` launcher is not enabled in the cloud runtime (re-probed; still unavailable)."* That framing is now imprecise: the launcher **is** invocable (it accepted the job, spawned 4 agents, ran 138s, consumed real tokens) — it just cannot currently produce valid subagent output due to the permission-handler bug described above. "Not enabled" and "enabled but faulting" are different operator-actionable states; worth a wording pass next time CONTRIBUTING.md is touched. Not filed as a formal doc-conformance finding below (it wasn't run through the verifier→skeptic pipeline), just flagged here since detecting exactly this kind of platform-state change is this section's stated purpose.

---

## Delta vs Prior Baseline

**Important baseline correction:** the most recent digest *merged into main* is `docs/audits/2026-08-02-conformance-nightly-digest.md` (8 days old), but that is **not** the most recent conformance *run* — six more digests were produced on schedule (2026-08-03, 04, 05, 07, 08, 09; no branch exists for 08-06) and pushed to their own `claude/conformance-<date>` branches, but never merged. This is a known, already-diagnosed operator-consumption gap: commit `189fcb376` (2026-08-10, this same morning) independently measured and named it, ruled it "BROKEN, not deliberate," and filed the retrofit as **[#426]**. Comparing against the stale merged baseline (08-02) would silently re-report findings the 08-09 run already caught and would miss real regressions since; this digest instead diffs against **`origin/claude/conformance-2026-08-09`** (the actual most recent run, fetched read-only for this comparison, not merged or altered), and separately reports the merge-gap status.

**Prior digest used for delta:** `origin/claude/conformance-2026-08-09:docs/audits/2026-08-09-conformance-nightly-digest.md` (unmerged)
**Gap:** 1 day (2026-08-09 → 2026-08-10)

All 5 of 2026-08-09's survivors were independently re-checked against current `origin/main` (f91a433) with fresh evidence commands (not merely re-asserted from the prior file):

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING** | prior S1 (HIGH): `protocols/ESSENTIALS.md:123` instructs agents `/override [reason]` is the only session-end escape — ADR-85 §A2 retired this 2026-08-03 | `grep -n "override.*only escape" protocols/ESSENTIALS.md` → line 123, text unchanged, verbatim identical to 08-09's citation |
| **PERSISTING** | prior S2 (MED): ARCHITECTURE.md says "five carriers" at 4 locations; six `carrier_*.py` files exist | `ls deploy/carrier_*.py` → still 6 files (`carrier_docs.py` + 5 others); `grep -n "five carrier" ARCHITECTURE.md` → still 4 hits (282, 456, 615, 888) |
| **PERSISTING (worse)** | prior S3 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit — was 10 days (vs 08-04) | `git log --date=short --format='%cd' -1 -- VISION.md` → **2026-08-05**; gap now 11 days |
| **PERSISTING (worse)** | prior S4 (MED): ESSENTIALS.md `last_reviewed: 2026-07-30` predates last commit — was 5 days (vs 08-04) | `git log --date=short --format='%cd' -1 -- protocols/ESSENTIALS.md` → **2026-08-05**; gap now 6 days |
| **PERSISTING** | prior S5 (LOW): ARCHITECTURE.md pre-commit gates paragraph omits `block-unanchored-push` | `grep -n "block-unanchored" ARCHITECTURE.md` → no output, still absent |

**NEW this cycle** (found by tonight's independent V1/V2/V3 fan-out, not carried from 08-09):

| Status | Finding | Notes |
|---|---|---|
| **NEW** | T1 (HIGH, historical): commit `cd38fb8` claimed to close `[#213] [#215] [#441]` but its diff never touched `BACKLOG.md` rows or `tasks/manifest.json` nodes for those ids | Self-corrected 18 minutes later by commit `a62d988`, which documents the identical defect in its own message. **HEAD is not currently broken by this** — flagged for the historical record / process-integrity awareness, not as a live defect needing a fix. |
| **NEW** | T2 (MED): `ARCHITECTURE.md:405` says `validate_doc_code_edge.py` is "live on 13 rules" with an explicit 13-item enumeration; the registered declaration docs actually carry 15 live `<!-- rule: ID -->` tokens | Enumeration omits `seal-journal-anchor` / `seal-journal-spine-anchor`, added by the ADR-85 amendment (2026-08-03); both resolve to live code sites and the latter backs an active `ALL_CHECKS` member. |
| **NEW** | T3 (LOW): `ARCHITECTURE.md:95` Purpose line says the file is "ratified through ADR-109," but the file's own changelog 3 lines above (line 26-ish) already names ADR-110 by name, and ADR-110 is Accepted 2026-08-06 | Internal inconsistency within the same file, not cross-file drift; the Governing-ADRs roster below is separately self-declared "curated, not exhaustive" so its own non-listing of ADR-110/111 is not itself a defect. |

**Delta counts:** 0 resolved · 5 persisting (3 of them worse) · 3 new
**This run's own raw → survived → killed:** 3 → 3 → 0
**Skeptic kill-rate:** 0% (0 of 3 raw findings killed — all 3 held up under adversarial re-verification, including one the skeptic strengthened by checking the authoritative source directly rather than trusting the raw evidence_command alone)

---

## Summary

Doc health did not improve this cycle and the *review pipeline itself* is now the more urgent finding. All 5 survivors from the last actual run (2026-08-09, unmerged) are still live on `origin/main` — the HIGH-severity `ESSENTIALS.md` `/override` misinstruction has now sat uncorrected and unread for at least a week (unclear exact age since 08-06 has no branch and is UNDETERMINED per commit `189fcb376`'s own measurement), and both backward-dated freshness stamps (VISION.md, ESSENTIALS.md) widened by another day each, now 11 and 6 days respectively. Three new findings surfaced from tonight's independent fan-out (a historical, self-corrected backlog-closure false-claim; an undercounted rule-edge enumeration; an internal ADR-number inconsistency), none HIGH-and-live. The zero-kill skeptic rate is not evidence of a lax pass — the skeptic actively re-derived the rule-edge count from the authoritative YAML source rather than trusting the raw grep, and explicitly narrowed one of the two ADR-related claims (killing the weaker "Governing ADRs roster is incomplete" framing implicitly by not carrying it forward, since that roster is self-declared non-exhaustive) while keeping the stronger "Purpose line contradicts the file's own changelog" claim.

The structural issue this run surfaces most clearly is upstream of documentation content: **seven** `claude/conformance-<date>` branches (08-03, 04, 05, 07, 08, 09, and now this one) sit unmerged, meaning every night's findings — including the HIGH one — have been invisible to anyone who only reads `main`. This was independently discovered and filed by the operator this same morning as [#426]; this run's findings corroborate it needed no further diagnosis, only confirms the HIGH finding's exact persistence.

The systemic `uv` infrastructure mismatch (cloud runtime `0.8.17` vs pinned `0.11.19`) also continues: it fired on every Stop-hook check during this session, exactly as in the 2026-08-02 digest's Next Actions #1, still unresolved 8+ nights later, still blocking `session_end_backpressure.py`'s advisory JOURNAL check locally (though not this PR — see Safety Tripwire).

<!-- counts: raw=3 survived=3 killed=0 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 3 · **Survived skeptic:** 3 · **Killed false positives:** 0
**Plus 5 persisting findings carried forward from the 2026-08-09 run (independently re-verified above with fresh evidence, not re-run through tonight's skeptic pipeline)**

### High (2)

**Carried — prior S1** — `protocols/ESSENTIALS.md:123` instructs agents that `/override [reason]` is the only session-end escape
- **Claim:** "`/override [reason]` is the only escape" from the JOURNAL hard-gate.
- **Location:** `protocols/ESSENTIALS.md:123`
- **Evidence:** `grep -n "override.*only escape" protocols/ESSENTIALS.md` → line 123, unchanged since 2026-08-09.
- **Verdict:** contradicted (ADR-85 amendment 2026-08-03 §A2 retired `/override`; CLAUDE.md corrected this in v2.51 the same day)
- **Proposed fix:** Replace the clause with: "the sole escape for the pre-push hard leg is `git push --no-verify` (ADR-85 amendment 2026-08-03 §A2 retired `/override`; the Stop hook is advisory in full)."
- **Note:** Persisting at least since 2026-08-09's digest; unread because the branch that found it was never merged. This is the most operationally risky finding in this digest — it is always-on-boot guidance telling agents to use an escape hatch that no longer exists.

**T1 (historical, not live)** — commit `cd38fb8` claimed to close `[#213] [#215] [#441]` without discharging them
- **Claim:** Commit `cd38fb8` ("ARC-2 Phase A — the adjudication wave: closes [#213] [#215] [#441]") closes those three backlog items per the repo's own retire mechanics.
- **Location:** `cd38fb8a8e88afea2231eeb30f43294709bda18d` (`BACKLOG.md`, `tasks/manifest.json`)
- **Evidence:** `git show cd38fb8^:BACKLOG.md | grep -n '\[#213\]\|\[#215\]\|\[#441\]'` vs `git show cd38fb8:BACKLOG.md | grep -n same` — rows byte-identical before and after; `git show cd38fb8 --stat` touches no `tasks/213-*.md`/`215-*.md`/`441-*.md`.
- **Verdict:** contradicted
- **Proposed fix:** No repo action needed — self-corrected 18 minutes later by commit `a62d988`, which states the defect explicitly in its own message. If an audit trail of commit-message reliability is ever built, annotate `cd38fb8` as superseded-same-session by `a62d988`.
- **Note:** Skeptic confirmed this is not a live defect (HEAD reflects the corrected state) but kept it at HIGH severity since a commit message asserting an untrue closure, even if self-caught, is a genuine process-integrity event worth a permanent record — anyone reading commit history without diffing would be misled.

### Med (4)

**Carried — prior S2** — ARCHITECTURE.md says "five carriers" at 4 locations; six carrier files exist
- **Location:** `ARCHITECTURE.md:282,456,615,888`
- **Evidence:** `ls deploy/carrier_*.py` → 6 files (`carrier_docs.py carrier_floor.py carrier_globalconfig.py carrier_mesh.py carrier_plugin.py carrier_precommit.py`).
- **Verdict:** contradicted
- **Proposed fix:** Update all four "five carriers" occurrences to "six"; add `carrier_docs` to the enumerated list; line 888's "five in reality today" needs updating since `carrier_docs` (previously `implemented: false` per its own note) is now real.
- **Note:** `carrier_docs.py` landed via batch-3 after ARCHITECTURE.md's review stamp; persisting since at least 2026-08-09.

**Carried — prior S3** — VISION.md `last_reviewed: 2026-07-25` predates last commit (now 11 days, was 10)
- **Location:** `VISION.md:4`
- **Evidence:** `git log --date=short --format='%cd' -1 -- VISION.md` → `2026-08-05`.
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end; bump `last_reviewed` to on/after 2026-08-05.
- **Note:** Widened by 1 day since the 08-09 measurement (then vs 08-04); the A2 `canonical_freshness` gate fires on every audit run this stays backward-dated.

**Carried — prior S4** — ESSENTIALS.md `last_reviewed: 2026-07-30` predates last commit (now 6 days, was 5)
- **Location:** `protocols/ESSENTIALS.md:2`
- **Evidence:** `git log --date=short --format='%cd' -1 -- protocols/ESSENTIALS.md` → `2026-08-05`.
- **Verdict:** contradicted
- **Proposed fix:** Re-read ESSENTIALS.md end-to-end (this pass would also catch the T1/prior-S1 `/override` defect at line 123, since ESSENTIALS carries the same instruction); bump `last_reviewed` to on/after 2026-08-05.
- **Note:** Widened by 1 day since 08-09.

**T2** — `ARCHITECTURE.md:405` claims `validate_doc_code_edge.py` is "live on 13 rules" (explicit enumeration); actual live count is 15
- **Location:** `ARCHITECTURE.md:405-407`
- **Evidence:** `grep -c '# DONE' ecosystem/doc-code-edge.yaml` → 15; `grep -on "<!-- rule: [a-zA-Z0-9_.-]\+ -->" protocols/PLAYBOOK.md protocols/DEFINITION_OF_DONE.md protocols/HANDOFF_PROCESS.md | sort -u | wc -l` → 15.
- **Verdict:** contradicted
- **Proposed fix:** Update the count to "15 rules" and extend the enumeration to include `seal-journal-anchor` (`DEFINITION_OF_DONE.md:26`) and `seal-journal-spine-anchor` (`DEFINITION_OF_DONE.md:64`), both merged 2026-08-05 (commit `1cc7c44`) and marked DONE.
- **Note:** Skeptic re-verified against the authoritative `ecosystem/doc-code-edge.yaml` source (not just the doc-side grep) before keeping this — confirms the gap is real, not a counting artifact.

### Low (1)

**Carried — prior S5** — ARCHITECTURE.md pre-commit gates paragraph omits `block-unanchored-push` (17th hook, live since 2026-08-03)
- **Location:** `ARCHITECTURE.md:512`
- **Evidence:** `grep -n "block-unanchored" ARCHITECTURE.md` → no output.
- **Verdict:** omitted
- **Proposed fix:** Add `block-unanchored-push` to the pre-push hooks enumeration.
- **Note:** Persisting since at least 2026-08-09; low severity since the hook itself is documented in CLAUDE.md §9, just missing from ARCHITECTURE.md's Ch2 enumeration.

**T3** — `ARCHITECTURE.md:95` Purpose line says "ratified through ADR-109"; file's own changelog already names ADR-110 (Accepted 2026-08-06)
- **Location:** `ARCHITECTURE.md:95` vs its own changelog entry naming ADR-110
- **Evidence:** `grep -n 'ADR-110' ARCHITECTURE.md`; `grep -n '^\*\*Status' docs/decisions/ADR-110-parallel-execution-batch-protocol.md` → Accepted.
- **Verdict:** omitted
- **Proposed fix:** Bump the Purpose line to "ratified through ADR-110" (ADR-111 is still Proposed, not yet applicable).
- **Note:** Internal inconsistency within the same file (changelog vs Purpose line), not cross-file drift. The separate "Governing ADRs roster ends at ADR-109" observation was NOT kept as its own finding — that roster is explicitly self-labeled "curated, not exhaustive" (ARCHITECTURE.md:862), so its non-exhaustiveness is a documented property, not drift.

---

## Killed Findings

None. All 3 findings raised by tonight's V1/V2/V3 fan-out survived adversarial skeptic review (0% kill rate this cycle).

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries, 2026-08-09(b) through 2026-08-10(a)):**
- All 29 distinct commit SHAs cited across the window exist in git log with matching subject lines ✓
- `ecosystem/disposition-register.yaml` has exactly 20 entries with `ref: "#241"`, matching the claimed "20th disposition, exactly 20" ✓
- `docs/handoffs/2026-08-10-dev-knowledge-architect/` exists with exactly the 5 claimed files ✓
- Task-status totals in commit `01410f94`'s own message (open 170, deferred 26, closed 55, superseded 1, retired 1 = 253) match live `grep -h '^status:' tasks/*.md` counts exactly ✓
- `STANDING_RULINGS.md` §H (ARC-3 hygiene close-out) with subsections H1-H4 confirmed present ✓
- `ADR-111-finding-triage-pipeline.md` exists, Status: Proposed, matching the JOURNAL's citation ✓
- Full commit-range walk from the oldest-cited commit to HEAD shows no significant work outside what the 10 entries narrate — no omitted-work findings ✓

**V2 (living-doc factual claims):**
- CLAUDE.md's "≤200 lines" budget: 198 prose lines under the enforced definition (`validate_doc_rot.py` excludes comment-boundary lines) ✓
- Fleet "nine git repos" (ADR-104) matches `ecosystem/registry.md` (8 child rows + hub) ✓
- Pre-commit hook roster (17 hooks) matches `.pre-commit-config.yaml` exactly ✓
- `audit.py`'s "41 registered checks" matches the literal `ALL_CHECKS` list length ✓
- `reconciled_with: handoff-process@6.2.0` frontmatter stamps match `HANDOFF_PROCESS.md`'s current version ✓
- ~30 cross-referenced file paths spot-checked across VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING all exist on disk ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-20 → HEAD):**
- `a96040c` (#490/#429/#320): rows removed, manifest nodes dropped, cited evidence commits all exist and match Done-when ✓
- `93b2fa3` (#501): `.github/workflows/report-only-wall.yml` exists, ARCHITECTURE.md Ch2 row matches all 4 Done-when clauses ✓
- `1447d06` (#503/#504): `block_ff_push.py:39` fail-closed docstring, `.claude/commands/override.md` retired banner, `DEFINITION_OF_DONE.md` Override section marked RETIRED — all present as claimed ✓

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent)** Absorb the queue of unmerged `claude/conformance-*` branches — currently 7 deep (08-03, 04, 05, 07, 08, 09, and this run's 08-10). This is [#426]'s subject; the operator's own commit `189fcb376` (this morning) already ruled the gap "BROKEN, not deliberate." The HIGH-severity `/override` misinstruction (carried-S1/T1 above) has been sitting unread in at least one of these branches since 08-09 or earlier.

2. **HIGH — carried S1** — Fix `protocols/ESSENTIALS.md:123`'s stale `/override` instruction (see Findings above). Lowest-effort, highest-impact item in this digest.

3. **MED — carried S2** — Update ARCHITECTURE.md's 4 "five carriers" occurrences to six, including `carrier_docs`.

4. **MED — carried S3 / S4** — Re-read VISION.md and ESSENTIALS.md end-to-end and bump both `last_reviewed` stamps (currently 11 and 6 days backward-dated respectively). A single ESSENTIALS.md re-read would also naturally catch item 2 above.

5. **MED — T2** — Update ARCHITECTURE.md:405's rule-edge count from 13 to 15 and extend the enumeration.

6. **LOW — carried S5 / T3** — Add `block-unanchored-push` to ARCHITECTURE.md's pre-push hook enumeration; bump the Purpose line's "ratified through ADR-109" to ADR-110.

7. **(INFRASTRUCTURE, persisting since ≥2026-08-02)** Upgrade cloud runtime `uv` to `==0.11.19`. Fired on every Stop-hook check this session; blocks `session_end_backpressure.py` locally.

8. **(PLATFORM, new observation)** `CONTRIBUTING.md:155-156`'s "native launcher not enabled... still unavailable" framing is now imprecise — tonight the launcher ran but failed on a permission-handler/StructuredOutput bug. Worth a wording pass to distinguish "unavailable" from "available but faulting" next time this section is touched; not urgent on its own.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-10-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
