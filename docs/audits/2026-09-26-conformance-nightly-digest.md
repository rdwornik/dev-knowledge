# Nightly Conformance Digest — 2026-09-26

- **Lane:** nightly READ-ONLY documentation-conformance review, `.dev-knowledge` / `rdwornik/dev-knowledge`
- **Posture:** proposals only. Nothing was fixed, nothing merged, nothing written to `main`.
- **Bound at:** `main` HEAD `bff9a8c1997475e28bc7163dae23cd2687d8802c` (*Merge branch 'worktree-lane-adr-drafts' @ 2be3eaa5 — ADR-123..126 Proposed*)

## Run

**Path: NATIVE Workflow launcher** — `.claude/workflows/conformance-hub.js` ran directly via the `Workflow` tool (`name: "conformance-hub"`, run id `wf_85dd2ad9-b40`). The native launcher was enabled tonight, same as the immediately preceding run (2026-09-25). No spec-orchestration fallback was needed. Per the re-probe instruction, native is attempted first every night; this is now the second consecutive night it has worked.

**Actual models per stage** (from the run's own `workflowProgress` records):

| Stage | Agent | Requested model | **Actual model** |
|---|---|---|---|
| 1 — verifiers | V1-journal-vs-git | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V2-livingdoc-claims | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V3-backlog-closures | `claude-sonnet-5` | `claude-sonnet-5` |
| 2 — skeptic | skeptic-adversarial | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |
| 3 — digest | digest-synthesis | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |

**Flag for the operator (repeat observation, carried from 2026-09-25):** Stage 2/3 are commented as Opus-intended in `conformance-hub.js:6-7` but carry no `model:` override on their `agent()` calls, so both ran on Sonnet again tonight — same as every night this has been checked. Not counted as a documentation-conformance finding (it's a script/comment mismatch, not a doc-vs-repo mismatch), but it has now persisted at least two nights running and is worth a script fix or a comment correction.

**Harness note:** the workflow's own log stream flagged that each of the 5 subagents' structured output matched an "instruction-shaped pattern" (`settings-json`) and neutralized control characters in place. Inspecting the underlying findings, this fired because several findings legitimately quote `.claude/settings.json` hook-command strings as evidence — not an actual injection attempt. No finding below was affected in substance; noted here for the record since the prompt requires flagging anything injection-shaped.

Total: 5 agents, 96 tool calls, 428,390 subagent tokens, ~393s wall time.

## Delta vs prior digest

**Baseline:** `docs/audits/2026-09-25-conformance-nightly-digest.md`, from `origin/claude/conformance-2026-09-25` (unmerged — the highest-dated true V1/V2/V3-shaped nightly digest; `2026-08-21-fresh-eyes-cloud-r3-conformance.md` is a differently-scoped, differently-shaped targeted review and is excluded from this delta for the same reason the 2026-09-25 run excluded it).

Eight `claude/conformance-<date>` branches (2026-09-18 through 2026-09-25) currently sit unmerged on origin, none absorbed into `main` yet — this run does not attempt to fix that; it is flagged for the operator as in every recent cycle.

All 4 of the 2026-09-25 baseline's survivors were independently re-checked against current `origin/main` (`bff9a8c1`) with fresh evidence commands (not merely re-asserted from the prior file). Tonight's automated V1/V2/V3 fan-out independently re-derived one of the four on its own (the `CANONICAL_MANDATORY[0]` claim); the other three were not re-flagged by tonight's V2 pass (whose raw output happened to surface different lines in the same files) but were confirmed still live by direct re-run of the baseline's own evidence commands:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING** | prior HIGH: `docs/archive/VISION.md:18` claims `canonical_docs.CANONICAL_MANDATORY[0]` | Independently re-derived by tonight's V2 verifier and confirmed by the skeptic; `scripts/canonical_docs.py` still defines `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)` with VISION absent, and `CANONICAL_RETIRED = (VISION,)` |
| **PERSISTING** | prior HIGH: `docs/archive/VISION.md:17` claims `MUST` on all nine ADR-104 fleet members | `grep -n -A5 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml` → `tier: {hub: SHOULD, consumer: SHOULD}`, unchanged from baseline; VISION.md:17 text itself unchanged (still says "MUST ... all nine") |
| **PERSISTING** | prior MED: stale "43.50 KiB" wholesale-copy figure in `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32` | `grep -n "43.50 KiB\|43\.50" CLAUDE.md AGENTS.md CONTRIBUTING.md` → all three still present verbatim; `wc -c CLAUDE.md` = 23,988 B, still under (not over) the 32 KiB cap |
| **PERSISTING** | prior LOW: `CONTRIBUTING.md:19` claims AGENTS.md is 5,714 B | `wc -c AGENTS.md` → 5,843 B, same 129 B drift as baseline, unchanged |

**NEW this cycle** (raised by tonight's independent V1/V2/V3 fan-out, not present in the 2026-09-25 baseline):

| Status | Finding |
|---|---|
| **NEW** | HIGH: `CLAUDE.md:194` §9 says exactly two Stop hooks are wired; `.claude/settings.json` now registers three (`lane_handback_gate` added 2026-09-25, one day after CLAUDE.md's own "Last updated: 2026-09-24" stamp) |
| **NEW** | HIGH: `CONTRIBUTING.md:169-170` describes `audit-health`/`ruff`/neighbors as active blocking commit-stage gates; both moved to `stages: [manual]` / Actions-conductor report-only on 2026-09-17, a week before CONTRIBUTING.md's own `last_reviewed: 2026-09-10` stamp |
| **NEW** | LOW: `docs/archive/VISION.md:18-19` says "five deploy manifests" reference it; six manifest files (`v1.1.0` through `v1.5.0`) actually match |

**Delta counts:** 0 resolved · 4 persisting (0 worse, 0 better — all unchanged) · 3 new
**This run's own raw → survived → killed:** 4 → 4 → 0
**Skeptic kill-rate:** 0% (0 of 4 raw findings killed — all 4 held up under adversarial re-verification)

## Findings (PROPOSALS ONLY)

**This run's raw:** 4 · **Survived skeptic:** 4 · **Killed false positives:** 0
**Plus 3 persisting findings carried forward from the 2026-09-25 run** (independently re-verified above with fresh evidence, not re-run through tonight's skeptic pipeline)

### High (4)

**Carried + independently re-derived tonight** — `docs/archive/VISION.md:18` claims `canonical_docs.CANONICAL_MANDATORY[0]`
- **Claim:** "it is `canonical_docs.CANONICAL_MANDATORY[0]`"
- **Evidence command:** `grep -n -A3 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py; grep -n 'CANONICAL_RETIRED: tuple' scripts/canonical_docs.py`
- **Verdict:** contradicted
- **Note:** `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)` — VISION is absent; it lives in the singleton `CANONICAL_RETIRED` tuple per ADR-114. Self-contradictory with VISION.md's own opening "superseded" framing.
- **Proposed fix:** Change `VISION.md:18` from `canonical_docs.CANONICAL_MANDATORY[0]` to `canonical_docs.CANONICAL_RETIRED[0]`.

**Carried** — `docs/archive/VISION.md:17` claims `MUST` on all nine ADR-104 fleet members
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members (`ecosystem/parity-surfaces.yaml`, `canonical-doc-vision`)"
- **Evidence command:** `grep -n -A5 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml`
- **Verdict:** contradicted
- **Note:** The row sets `tier: {hub: SHOULD, consumer: SHOULD}`, demoted from MUST on 2026-08-31 ([#614] lane-a, ADR-114); VISION.md's prose was never reconciled with that demotion. Unchanged since 2026-09-25.
- **Proposed fix:** Update VISION.md's paragraph to reflect the SHOULD/SHOULD demotion and the corrected eight-of-nine tracking count.

**NEW** — `CLAUDE.md:194` §9 undercounts Stop hooks (2 vs 3 wired)
- **Claim:** "**+ 2 Stop** (`session_end_backpressure`, advisory; `lane_end_guard`)"
- **Evidence command:** `python3 -c "import json; d=json.load(open('.claude/settings.json')); print(len(d['hooks']['Stop'])); [print(h['hooks'][0]['command']) for h in d['hooks']['Stop']]"`
- **Verdict:** contradicted
- **Note:** `.claude/settings.json` registers three Stop hooks today: `session_end_backpressure.py`, `lane_end_guard.py`, and `lane_handback_gate.py`. The third was added by a 2026-09-25 commit ("a Stop hook refuses to end a lane session without a clean HANDBACK line") — one day after CLAUDE.md's own "Last updated: 2026-09-24" stamp.
- **Proposed fix:** Add `lane_handback_gate` to the Stop-hook roster in CLAUDE.md §9 and bump the "Last updated" stamp past 2026-09-25.

**NEW** — `CONTRIBUTING.md:169-170` describes demoted hooks as still blocking
- **Claim:** Validators table lists `audit-health` and `ruff` (and neighbors) as active pre-commit "commit"-stage gates — "FAIL-level findings block the commit" (audit-health), "Blocks on violations" (ruff)
- **Evidence command:** `grep -n -A2 'id: audit-health' .pre-commit-config.yaml; grep -n -A2 '  - id: ruff' .pre-commit-config.yaml`
- **Verdict:** contradicted
- **Note:** Both hooks (and `check-seal-identity`, `validate-backlog`, `normalize-dated-headers`, `toc-freshness-playbook`, `audit-title-gate`, `doc-counts-pytest-freshness`, `prepend-order`, `coherence-nudge`, several `graph-*` hooks) carry `stages: [manual]  # MOVED to the Actions conductor, 2026-09-17` — an explicit, dated operator ruling (CLAUDE.md §9 itself already says "rest `stages: [manual]`"). CONTRIBUTING.md's `last_reviewed: 2026-09-10` predates that ruling by a week and still documents these as blocking.
- **Proposed fix:** Update CONTRIBUTING.md's Validators table to mark the demoted hooks as manual-stage/Actions-conductor report-only, and refresh its `last_reviewed` stamp past 2026-09-17.

### Med (1)

**Carried** — stale "43.50 KiB" wholesale-copy figure (3 files)
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — repeated in `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`
- **Evidence command:** `wc -c CLAUDE.md`
- **Verdict:** contradicted
- **Note:** CLAUDE.md measures 23,988 B — under, not over, the 32 KiB cap. Unchanged since 2026-09-25; the figure was reportedly never accurate at any checkable point in tracked history (per the 09-25 skeptic's deeper check).
- **Proposed fix:** Recompute/correct the figure in all three files, or replace it with a pointer to a live-computed size instead of a fixed number.

### Low (2)

**Carried** — `CONTRIBUTING.md:19` AGENTS.md byte-count drift
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"
- **Evidence command:** `wc -c AGENTS.md`
- **Verdict:** contradicted
- **Note:** AGENTS.md measures 5,843 B, the same 129 B drift recorded on 2026-09-25 — unchanged.
- **Proposed fix:** Drop the byte figure (cite `wc -c AGENTS.md` as the live surface) or refresh it.

**NEW** — `docs/archive/VISION.md:18-19` "five deploy manifests" undercounts six
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine"
- **Evidence command:** `grep -rl '^  VISION.md:' deploy/manifest-v*.yaml | wc -l`
- **Verdict:** contradicted
- **Note:** Six manifest files carry a `VISION.md:` entry (v1.1.0, v1.2.0, v1.3.0, v1.3.1, v1.4.0, v1.5.0), not five — the same stale-count class CLAUDE.md §4 itself warns against.
- **Proposed fix:** Correct "five" to "six", or replace the literal count with a cite to the computing grep, per this repo's own anti-restated-count convention.

## Killed Findings

None from tonight's own V1/V2/V3 → skeptic pipeline (0 of 4 raw findings killed, 100% survival). The three carried-forward baseline findings were not re-run through tonight's skeptic pipeline; they were confirmed still live only by direct re-execution of their own evidence commands (see Delta table above), not by adversarial re-review.

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL vs git, last 10 entries, 2026-09-25(j) through 2026-09-25(s)):**
- All 10 entries' anchored commit hashes exist in `git log` with matching subject lines and merge commits ✓
- Spot-checked technical claims all matched live tree state: `learning_distiller.py`'s 26 tests, `dispatch.py`'s `queue`/`--dry-run`/`--watch`, `substrate-heartbeat.yml`'s schedule+`workflow_dispatch` trigger, `provision.sh`'s login-path fallback order, `lane_handback_gate.py`'s Stop-hook wiring plus task 1010's closed status, `transport-registry.yaml`'s exact 21-kind count, `plan_lint.py`'s grammar handling, the `moment_only.py` test fixture mechanism, and the GH-Issues trial audit file plus ADR-122's dated amendment ✓
- No commits exist between the JOURNAL's newest anchor (`bff9a8c1`) and current HEAD — nothing merged is omitted ✓
- Working tree clean at HEAD ✓

**V2 (living-doc claims, scope: VISION.md/ARCHITECTURE.md/CLAUDE.md/CONTRIBUTING.md):**
- CLAUDE.md's ≤24,576 B budget: 23,988 B, within cap, gating test file exists ✓
- ARCHITECTURE.md's Codemap block reproduces byte-for-byte via `python3 -m scripts.codemap.cli generate` ✓
- ARCHITECTURE.md's "29 requirements, 8 measured, 21 candidate" matches an exact grep of `ecosystem/quality-requirements.yaml` ✓
- ARCHITECTURE.md's "8 classes" organ-index claim matches `ecosystem/organ-index.md`'s heading count exactly ✓
- CLAUDE.md §9's "8 SessionStart" hooks list matches `.claude/settings.json`'s SessionStart array exactly, same order ✓
- CONTRIBUTING.md's ruff pin (v0.15.5) matches `.pre-commit-config.yaml` and the `pyproject.toml` floor ✓
- ADR-115's Accepted/superseding/amending frontmatter matches the ADR file exactly ✓
- 7 cross-referenced scripts/tests spot-checked all exist on disk ✓

**V3 (BACKLOG closure coherence, ~3-week window):**
- `[#960]` wave 4b lane 4 — all 6 Done-when clauses verified landed before closure ✓
- `[#727]` PreToolUse deny-and-point fail-closed — diff matches amended Done-when; later unwiring (2026-09-18) is a separate, non-contradicting concern ✓
- `[#684]` MA-1 PreToolUse guard fail-closed — diff matches the long Done-when including fail-closed behavior, trip-tests, SessionStart check ✓
- `[#716]`/`[#717]`/`[#718]` dispatch defects — commit body verifies each of three fixes live ✓
- `[#692]` decision-coverage — named test confirmed ✓
- `[#614]` vision-to-readme arc — README.md and VISION.md's `status: superseded` both verified live ✓
- `[#530]` single-flight lock races — diff matches two RED-first race fixes ✓
- `[#490]`/`[#429]`/`[#320]` batch-2 closure sweep — each Done-when re-verified against live post-merge state; stale figures corrected in the same commit, `[#430]` correctly left open ✓

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, persisting)** Absorb the queue of unmerged `claude/conformance-*` branches — now 9 deep (2026-09-18 through 2026-09-26, this run included). No branch in this chain has been merged since at least 2026-09-18.
2. **HIGH — persisting** Fix `docs/archive/VISION.md:18` — `canonical_docs.CANONICAL_RETIRED[0]`, not `CANONICAL_MANDATORY[0]`.
3. **HIGH — persisting** Fix `docs/archive/VISION.md:17` — SHOULD/SHOULD tier, eight-of-nine tracking, per ADR-114 / [#614] lane-a.
4. **HIGH — new** Add `lane_handback_gate` to CLAUDE.md §9's Stop-hook roster; bump "Last updated" past 2026-09-25.
5. **HIGH — new** Update CONTRIBUTING.md's Validators table to mark the B2-lane4-demoted hooks (`audit-health`, `ruff`, and neighbors) as manual-stage/report-only; refresh `last_reviewed` past 2026-09-17.
6. **MED — persisting** Correct or remove the "43.50 KiB" figure in `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`.
7. **LOW — persisting** Refresh or drop the AGENTS.md byte figure in `CONTRIBUTING.md:19` (5,843 B actual vs 5,714 B recorded).
8. **LOW — new** Correct `docs/archive/VISION.md:18-19`'s "five deploy manifests" to six.
9. **(Process, persisting)** `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md`'s F1–F10 (the `[#171]` conformance-dashboard review) remain out of this pipeline's V1/V2/V3 scope and have not been re-checked by any nightly run since 2026-08-21. If still open, they need a dedicated re-check.
10. **(Process, persisting)** Stage 2/3 of `conformance-hub.js` are commented as Opus-intended but carry no `model:` override and have run on Sonnet for at least two consecutive nights — worth a script fix or a comment correction.
11. **(Infrastructure, observed this session, not a doc-conformance finding)** The cloud runtime's `uv` (`0.8.17`) still does not match the pinned `==0.11.19` — fired repeatedly on `session_end_backpressure.py` during this session, consistent with the persisting infra gap noted in digests back to 2026-08-02.

## Safety Tripwire

`git status --porcelain` output at digest write time (captured after writing this file, before commit):

```
?? docs/audits/2026-09-26-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. ✓ Safety check passes.

<!-- counts: raw=4 survived=4 killed=0 -->
