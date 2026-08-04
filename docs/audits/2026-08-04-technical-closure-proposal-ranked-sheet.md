---
class: technical
date: 2026-08-04
slug: closure-proposal-ranked-sheet
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-batch-review-prep-k1f2yr
anchor_sha: f6d271b1
consumer: incoming 2026-08-05 dev-knowledge architect session
consumption_path: "branch -> local re-verification -> architect adjudicates each verdict at FR-8a"
scope: "RETRIEVAL ONLY — ranked sheet of the parked closure proposals; every verdict cell is EMPTY by design"
---

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Cloud night-batch lane: no merge, no
> canon edit, no closure, no ruling. `propose_closures.py` was **not** run and no BACKLOG row was
> touched.
>
> **RETRIEVAL, NOT CLASSIFICATION.** Every column is mechanically derived from repo state at the
> anchor SHA. There is **no close/keep verdict anywhere in this document** and no classification
> against a doctrine clause — that is the architect's act, and the `verdict` column is left empty
> for it. The carried constraint is explicit: fan-out is safe for retrieval and unsafe for
> classification against a doctrine clause.

# FR-8a — closure-proposal ranked sheet

## Coverage — stated honestly, not rounded up

| Set | Target | Covered | Why |
|---|---|---|---|
| Closure proposals | 139 | **132** | the 132 enumerated in the tracked 2026-07-30 triage artifact |
| Fleet issues | 2 | **0** | source is `logs/FLEET-HEALTH.md`, gitignored (`.gitignore:30`) and absent in a fresh clone |

**The 7-proposal gap is not an omission, it is unreachable from here.** `propose_closures.py`
writes `logs/PROPOSALS-YYYY-MM-DD.md`, which `.gitignore:26` excludes; `git log --all --diff-filter=A
-- "logs/PROPOSALS-*.md"` returns empty, so no such file has ever been committed. The parked set
therefore exists only on the operator's machine. What this lane *can* reach is the tracked triage
artifact `docs/audits/2026-07-30-technical-proposals-2026-07-29-triage.md`, which enumerates 132
WEAK proposals from the 2026-07-29 run. The delta (139 − 132 = 7) accrued after 2026-07-29 and must
be appended locally.

**Same limit applies to the 2 fleet issues** — `logs/FLEET-HEALTH.md` is gitignored for the same
reason (writing it must never dirty the tree). They are named in the handoff as parked from
`/review-closures`; their content is not recoverable from the repository.

## Method (fully mechanical, reproducible at the anchor)

1. Parse the 132 `#id | #backlog_id | subject | reason` rows from the triage artifact's bucket
   tables; bucket membership read from section position (8 needs-ruling / 124 noise).
2. For each id, read **live** state: `status` / `priority` / `size` / `serialize-group` /
   `depends-on` from `tasks/<id>-*.md`, and theme/story from the id's position in
   `tasks/manifest.json` — the ADR-107 source of truth, never from `BACKLOG.md` prose.
3. Derive the staleness signal: an id absent from `BACKLOG.md`'s `^- \[#id\]` set whose retained
   record carries a terminal status = **target closed since the triage ran**.
4. Derive blocker out-degree by reversing the tree's own `depends-on` edges. Never inferred from
   prose.

**Ranking:** blockers first (A), then the mechanically-stale (B), then needs-ruling (C), then the
remainder grouped by theme (D). Sections are precedence-exclusive; 4 + 6 + 8 + 114 = 132.

## What the mechanical pass found

- **6** proposals name a target that has **closed** since the triage — the cheapest dispositions on
  the sheet, and the only staleness this pass can assert with certainty.
- **19** name a target now `deferred` (parked, not closed) — a weaker signal, reported not ranked.
- **4** name a target that gates other rows via a real `depends-on` edge.
- **0** verdicts. By design.

**A note the architect should carry into the adjudication:** the triage this sheet is built on found
**0 of 132 plausibly-closable**, reproducing `[#277]`'s own near-zero-precision diagnosis at n=132
instead of n=49. That is a property of the WEAK heuristic (it keys on churn in large canonical
files), not of the backlog. This sheet reports it as inherited context, and takes no position on
what follows from it.

---

## A · Blockers first — proposals whose target row GATES other rows (4)

Ranked by out-degree read from the task tree's own `depends-on` edges (never inferred). These come
first because a verdict here changes what is workable downstream.

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #270 | P1/M | open | [P1][M] Operator-load gauge — the gating FIRST element of any Tier-2 nightly layer (standing op… | blocks 2 row(s): #271, #348 |  |
| #171 | P3/M | deferred | [P3][M] Build the conformance dashboard at `ecosystem/conformance.md` (ADR-86 / ADR-85 R2) — a … | target now DEFERRED (parked); blocks 1 row(s): #169 |  |
| #383 | P2/L | open | [P2][L] **Execution waves per surface** — once the schema exists, converge each L0/L2 surface (… | blocks 1 row(s): #385; serialize-group `architecture` (n=23) |  |
| #390 | P2/S | open | [P2][S] **Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template**… | blocks 1 row(s): #389; serialize-group `handoff` (n=16) |  |

## B · Mechanically stale — the target row CLOSED after the triage ran (6)

The strongest derivable staleness signal, and the only one this sheet computes with certainty: the
proposal names a row that is no longer in `BACKLOG.md` and whose retained record carries a terminal
status. A stale proposal is not automatically a close — the architect still rules — but the ground
it was written on has moved.

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #367 | P2/S | closed | [P2][S] **HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule** — c… | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `handoff` (n=16) |  |
| #370 | P3/S | closed | [P3][S] **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — **RULED 202… | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `claude-md` (n=6) |  |
| #382 | P1/M | closed | [P1][M] **Desired-state data model: intake → ADR** — build the intake #16 §2 architecture (the … | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `architecture` (n=23) |  |
| #421 | P2/S | closed | [P2][S] **`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the lea… | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `handoff` (n=16) |  |
| #433 | P1/M | closed | [P1][M] **BACKLOG restructure — build-thin ENGINE + Backlog.md VIEWER** — the three-way bake-of… | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `architecture` (n=23) |  |
| #446 | P2/L | closed | [P2][L] **§B(b) one-round-trip boot build — the v6 carrier arc** — intake #19 §B(b) ADOPTED at … | **TARGET CLOSED SINCE TRIAGE — proposal is mechanically stale**; serialize-group `handoff` (n=16) |  |

## C · Needs-ruling — Done-when turns on an operator/architect decision (8)

Carried forward from the triage's own bucket 2. These are open tasks whose true state depends on
operator memory that no repo-side check can audit; the triage explicitly refused to call them noise.

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #162 | P2/M | open | [P2][M] Vocab decision (architect-session): disambiguate "architect" as the Layer-1 **actor** (… | serialize-group `handoff` (n=16) |  |
| #283 | P3/S | open | [P3][S] corp-monorepo `hybrid_classifier.json` 1.08MB duplication — byte-identical file in `mod… | — |  |
| #308 | P3/S | deferred | [P3][S] Decide the `verify` skill's canonical home (#9 self-flagged open question), pegged to P… | target now DEFERRED (parked); serialize-group `settings-json` (n=20) |  |
| #320 | P2/S | open | [P2][S] Fleet backup posture — three repos hold unpushed work on one disk: corp-ops `main` 4 ah… | — |  |
| #323 | P3/S | open | [P3][S] Design question: add `codemap-generate`/`toc-generate` to the carried `hub_hooks` insta… | serialize-group `audit-py` (n=59) |  |
| #331 | P2/S | open | [P2][S] Consumer BACKLOG schema adoption ruling — rule whether ai-council + corp-monorepo adopt… | — |  |
| #420 | P3/S | open | [P3][S] **Does a TOP-LEVEL `docs/archive/` still make sense?** — operator-raised structural que… | serialize-group `architecture` (n=23) |  |
| #443 | P3/S | open | [P3][S] **Planning artifacts outside the three enforced classes carry no rent rule** — "meta se… | serialize-group `playbook` (n=11) |  |

## D · Remainder, grouped by theme (114)

### [E1] Handoff continuity (8)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #293 | P3/S | deferred | [P3][S] Consumer runbook fan-out — seed each consumer repo's `docs/handoffs/README.md` from the… | target now DEFERRED (parked) |  |
| #298 | P3/S | deferred | [P3][S] Handoff-generator polish — three ruled enhancements (2026-07-08): (a) EPIC_BOOT auto-pu… | target now DEFERRED (parked) |  |
| #301 | P2/M | deferred | [P2][M] Session-plan artifact class — architect-mode bundles gain a bundle-resident PLAN.md, co… | target now DEFERRED (parked); serialize-group `handoff` (n=16) |  |
| #344 | P2/M | open | [P2][M] Session-close gate for handoff generation + consumer hub-write guard (NEEDS-RULING; ai-… | serialize-group `handoff` (n=16) |  |
| #350 | P3/S | open | [P3][S] Handoff-process refinements (operator priority-program item 5 — explicitly LAST, 2026-0… | serialize-group `handoff` (n=16) |  |
| #404 | P2/S | open | [P2][S] **gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)** — `_tokens… | serialize-group `handoff` (n=16) |  |
| #422 | P2/S | open | [P2][S] **`reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the sel… | serialize-group `handoff` (n=16) |  |
| #447 | P3/S | open | [P3][S] **Self-referential gate family — the committing act cannot satisfy the gate's own preco… | serialize-group `gates` (n=1) |  |

### [E2] Enforced governance (37)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #132 | P2/M | open | [P2][M] Organ-index generator — `scripts/generate_organ_index.py` (read-only, codemap/toc patte… | serialize-group `pre-commit-config` (n=6) |  |
| #139 | P2/L | deferred | [P2][L] merged-arc→record verifier (a.k.a. **#90b** — direction (b), deferred from #90 which sh… | target now DEFERRED (parked); serialize-group `audit-py` (n=59) |  |
| #169 | P3/M | deferred | [P3][M] Ungated-doc staleness detection (ADR-85 R2) — surface ARCHITECTURE/VISION/LESSONS/CONTR… | target now DEFERRED (parked) |  |
| #170 | P3/M | open | [P3][M] Design + land the traceability-spine ADR (issue-ID↔commit anchor) that #168 depends on … | — |  |
| #181 | P2/S | deferred | [P2][S] Coherence v2 nudge-response — decide escape-hatch vs deferred-hash vs promote-nudge-to-… | target now DEFERRED (parked); serialize-group `coherence` (n=3) |  |
| #210 | P3/S | open | [P3][S] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule — 3 i… | serialize-group `audit-py` (n=59) |  |
| #218 | P3/M | deferred | [P3][M] Safe-removal gate M2+M3 boundary (the deferred phases of #195) — extend the code→code (… | target now DEFERRED (parked); serialize-group `code-edge` (n=1) |  |
| #234 | P3/S | open | [P3][S] Cross-repo probe validator — give `.claude/` target paths full FAIL teeth — the #163 ha… | serialize-group `audit-py` (n=59) |  |
| #239 | P3/M | deferred | [P3][M] Follow-up — extend the Informant Organ Tier-2 beyond the 4 deploy manifest carriers to … | target now DEFERRED (parked) |  |
| #240 | P3/S | deferred | [P3][S] Follow-up — Stage-3 audit-leg regression teeth: `check_enforcement_coverage` emits WARN… | target now DEFERRED (parked); serialize-group `audit-py` (n=59) |  |
| #241 | P2/S | open | [P2][S] Undeclared-edge groom — adjudicate the 6 tier-1 candidates the newly-wired `undeclared_… | serialize-group `coherence` (n=3) |  |
| #242 | P2/M | open | [P2][M] ADR status-flip coherence check — the ratified go-forward status-flip pattern (ADR-94, … | serialize-group `audit-py` (n=59) |  |
| #267 | P2/S | open | [P2][S] Scope-exercising arc extension (REFINEMENT, root-ratified 2026-07-06 — not a closure ga… | — |  |
| #277 | P2/M | open | [P2][M] propose_closures signal repair — the 2026-07-07 /review-closures run proposed 49 items,… | serialize-group `audit-py` (n=59) |  |
| #294 | P3/M | deferred | [P3][M] `validate_backlog` deploy-carrier + `--path` de-hardcode (ai-council pilot G1+G2) — the… | target now DEFERRED (parked); serialize-group `audit-py` (n=59) |  |
| #296 | P3/S | open | [P3][S] `audit.py repo <name> --repo-path` doesn't persist its report (ai-council pilot G6) — `… | serialize-group `audit-py` (n=59) |  |
| #297 | P3/S | deferred | [P3][S] Lightweight/dry `observe-arc` coverage mode (ai-council pilot G7) — `lived_sandbox.cli … | target now DEFERRED (parked); serialize-group `audit-py` (n=59) |  |
| #303 | P2/S | open | [P2][S] Make seed_runbook.py child-class-aware (ADR-36 no-local-handoffs) — the leg-b seeder (s… | serialize-group `architecture` (n=23) |  |
| #305 | P3/S | deferred | [P3][S] Add a verify-only / already-onboarded re-run mode to the onboarding runbook — the runbo… | target now DEFERRED (parked); serialize-group `architecture` (n=23) |  |
| #310 | P3/S | deferred | [P3][S] Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as… | target now DEFERRED (parked); serialize-group `handoff` (n=16) |  |
| #324 | P3/M | open | [P3][M] Phase-6 axis-2 carrier — codify the night-batch → morning-prompt loop as a standing rou… | serialize-group `audit-py` (n=59) |  |
| #325 | P3/S | deferred | [P3][S] Carry `/save` to consumers via a manifest command-artifact carrier — the hub `/save` co… | target now DEFERRED (parked); serialize-group `settings-json` (n=20) |  |
| #335 | P3/S | open | [P3][S] Exempt `templates/` from the `reconciled_versions` check — a template file's `reconcile… | serialize-group `audit-py` (n=59) |  |
| #345 | P2/M | open | [P2][M] Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generaliz… | serialize-group `pre-commit-config` (n=6) |  |
| #349 | P2/M | open | [P2][M] Mechanize session-discipline inheritance — the test-then-close gate travels via mechani… | serialize-group `audit-py` (n=59) |  |
| #353 | P2/M | open | [P2][M] Session-boot contract hardening — refuse a mid-session externally-authored order lackin… | serialize-group `audit-py` (n=59) |  |
| #389 | P2/S | open | [P2][S] **Prompt-lint — gate the five architect fields before a lane runs** — the ADR-87 contra… | serialize-group `audit-py` (n=59) |  |
| #405 | P2/S | open | [P2][S] **Session-end leftover check — nothing verifies "no leftovers"** — cleanup failed 3x th… | serialize-group `settings-json` (n=20) |  |
| #406 | P3/S | open | [P3][S] **Commit-time doc_rot surfacing — an over-threshold BACKLOG task commits clean, reds on… | serialize-group `audit-py` (n=59) |  |
| #408 | P2/M | open | [P2][M] **Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITEC… | serialize-group `audit-py` (n=59) |  |
| #414 | P2/S | open | [P2][S] **Self-acting-on-main incident family — a session changed `main` with no operator GO an… | serialize-group `settings-json` (n=20) |  |
| #417 | P3/S | open | [P3][S] **`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non… | serialize-group `settings-json` (n=20) |  |
| #418 | P2/S | open | [P2][S] **`automation/fleet-audit` records 0–10 baselines a day, not one** — the writer branch … | serialize-group `audit-py` (n=59) |  |
| #423 | P2/M | open | [P2][M] **The integration sequence runs on prose every time, never mechanized** — landing an ar… | — |  |
| #424 | P2/S | open | [P2][S] **Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is … | serialize-group `audit-py` (n=59) |  |
| #425 | P2/S | open | [P2][S] **The suite is green on a format the file does not use** — every `depends-on` fixture i… | serialize-group `audit-py` (n=59) |  |
| #442 | P2/M | open | [P2][M] **Plugin command-cache staleness — cached command text can silently outlive a workflow … | serialize-group `settings-json` (n=20) |  |

### [E3] Lessons feedback loop (2)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #266 | P3/S | open | [P3][S] Codify the test-scoped-grant language lesson (E4-1 precedent) — Wave-2 ratified (2026-0… | — |  |
| #438 | P3/S | open | [P3][S] **Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs** —… | serialize-group `playbook` (n=11) |  |

### [E5] Canonical-file integrity (6)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #213 | P2/L | open | [P2][L] PLAYBOOK rule/history condensation — separate rule from rationale/history across protoc… | serialize-group `playbook` (n=11) |  |
| #263 | P3/S | open | [P3][S] Protocols/edge-map reconciliation residuals (ADR-51 amendment) — groom the residuals Ep… | — |  |
| #269 | P3/S | open | [P3][S] Audit-index count-tiered shape + freshness hook (ADR-100 Q2) — apply the ADR-100 count-… | — |  |
| #285 | P3/S | open | [P3][S] Extend hub freshness gating to PLAYBOOK — SESSION_SETUP + AI_COUNCIL_PROCESS joined `_F… | serialize-group `audit-py` (n=59) |  |
| #300 | P1/M | deferred | [P1][M] Hermetization residual d.ii — mode-boot home (incident-recovery arc; TRIMMED 2026-07-18… | target now DEFERRED (parked) |  |
| #388 | P3/S | open | [P3][S] **The "10–20 repo" fleet-scale target is FABRICATED — correct it to the live 5–8+ where… | serialize-group `architecture` (n=23) |  |

### [E6] Cross-repo universalization (20)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #43 | P3/L | open | [P3][L] Decide + (if yes) author a one-step new-repo scaffold (ADR + templates/new-repo-skeleto… | — |  |
| #215 | P2/M | open | [P2][M] Onboard + verify methodology in a new repo — a consolidated runbook to deploy the metho… | — |  |
| #231 | P3/M | deferred | [P3][M] Consumer → hub feedback report — when a consumer session detects a methodology gap, amb… | target now DEFERRED (parked) |  |
| #244 | P2/L | open | [P2][L] Essence-spec lifecycle epic — P1 SHIPPED (feat/essence-spec-p1: manifest-v1.1.0 grew `a… | — |  |
| #245 | P2/M | open | [P2][M] Add-path status-awareness — the deploy add-path (`deploy/tool.py` execute + each carrie… | — |  |
| #276 | P2/M | open | [P2][M] D2 per-consumer waiver-honoring — a `.methodology.yaml` divergence-allowlist the deploy… | — |  |
| #280 | P3/S | open | [P3][S] Propagate the intake area to greenfield consumers via the deploy manifest — `docs/intak… | — |  |
| #281 | P2/S | open | [P2][S] Re-peg the ai-council ADR-66 story-map convergence (ADR-99 clause A) — orphaned by #221… | — |  |
| #282 | P3/S | open | [P3][S] Fleet `.gitattributes` EOL-normalization parity — 4 consumers lack `.gitattributes` (ai… | — |  |
| #290 | P3/S | open | [P3][S] Floor-carrier verify-teeth + self-heal (residual of #275b) — the v1.3.x arm-command fix… | — |  |
| #315 | P3/S | open | [P3][S] `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried (operator ruling; fleet-boun… | — |  |
| #327 | P2/M | open | [P2][M] Protocols-as-interface genre ruling (fleet-parity register acceptance) — unify the thre… | serialize-group `architecture` (n=23) |  |
| #329 | P3/S | open | [P3][S] VS Code ownership visualization — folder icons/colors GENERATED from the #328 fleet_par… | serialize-group `settings-json` (n=20) |  |
| #334 | P3/S | open | [P3][S] Fleet-wide ruff hook id migration `ruff` → `ruff-check` (upstream `ruff-pre-commit` dep… | serialize-group `pre-commit-config` (n=6) |  |
| #342 | P3/S | open | [P3][S] fleet_parity gate-ahead max-fidelity hardening (deferred from #336/ADR-102, operator-ru… | serialize-group `audit-py` (n=59) |  |
| #343 | P3/S | open | [P3][S] fleet_parity ship-gate-only scoping (RIDER 2 perf follow-up, operator-ruled 2026-07-18)… | serialize-group `audit-py` (n=59) |  |
| #351 | P3/M | open | [P3][M] Fleet-Python-upgrade ticket ("always newest Python" — RULING-PY, 2026-07-18) — RULING-P… | serialize-group `pre-commit-config` (n=6) |  |
| #352 | P3/S | open | [P3][S] Versioned `.vscode` region decoration (RULING-S human-facing half) — editor-side backgr… | serialize-group `settings-json` (n=20) |  |
| #416 | P3/S | open | [P3][S] **ai-council `ARCHITECTURE.md` codemap drift at L23/L109** — carved out of [#262]'s Don… | serialize-group `architecture` (n=23) |  |
| #430 | P2/M | open | [P2][M] **Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on sta… | serialize-group `audit-py` (n=59) |  |

### [E7] Tooling & evaluation (18)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #271 | P3/L | open | [P3][L] Nightly proposal loop — revive the Tier-2 draft ONLY under intake brief #1 §6 constrain… | — |  |
| #273 | P3/S | open | [P3][S] Changelog-review staleness escalation (intake doc #2 R3) — the SessionStart sentinel nu… | serialize-group `settings-json` (n=20) |  |
| #274 | P3/S | open | [P3][S] Dogfood-signal prior in the /changelog-review ADOPT rubric (intake doc #2 R4) — feature… | — |  |
| #278 | P2/M | open | [P2][M] Test-suite hygiene epic (consumes intake-id 3) — theatricality review of the pytest cor… | — |  |
| #317 | P2/M | open | [P2][M] Default-parallel test invocation + slow-tier markers — close the inner-loop serial tax … | — |  |
| #322 | P2/M | deferred | [P2][M] Fleet dashboard — a human-facing fleet-observability surface, three legs: (a) DATA SOUR… | target now DEFERRED (parked); serialize-group `settings-json` (n=20) |  |
| #340 | P2/S | open | [P2][S] /ship pre-flight validator honors the consumer repo's canonical test gate — the tier1-l… | — |  |
| #387 | P2/S | open | [P2][S] **Rewrite the buy-vs-build intake BEFORE anything ingests it** — intake **#2** (the pla… | serialize-group `architecture` (n=23) |  |
| #396 | P3/S | open | [P3][S] **Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 places** — the subprocess-g… | serialize-group `audit-py` (n=59) |  |
| #397 | P3/M | open | [P3][M] **scripts/ target structure — rule on the mapped grouping, then (maybe) move** — the 20… | serialize-group `audit-py` (n=59) |  |
| #415 | P2/S | open | [P2][S] **Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)**… | serialize-group `audit-py` (n=59) |  |
| #419 | P2/M | open | [P2][M] **We run routines whose output nobody consumes** — the nightly conformance routine emit… | serialize-group `settings-json` (n=20) |  |
| #426 | P2/M | open | [P2][M] **Declare `consumer` + `consumption_path` for every LIVE routine** — ADR-105's activati… | serialize-group `settings-json` (n=20) |  |
| #428 | P2/S | open | [P2][S] **`nightly-triage` reports a dead producer to every session start** — the producer has … | serialize-group `settings-json` (n=20) |  |
| #431 | P2/S | open | [P2][S] **`codex-review` silently drops the doc lane on any mixed diff** — any code-allowlist f… | serialize-group `codex-review` (n=6) |  |
| #432 | P1/M | open | [P1][M] **Adopt `uv` as the environment/dependency toolchain — `.dev-knowledge` ONLY this windo… | serialize-group `environment` (n=7) |  |
| #440 | P2/S | open | [P2][S] **Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable… | serialize-group `architecture` (n=23) |  |
| #445 | P2/S | open | [P2][S] **`codex-review` wrapper path-guard reports SUCCESS having reviewed nothing** — third i… | serialize-group `codex-review` (n=6) |  |

### [E8] ARC-5 execution (18)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #354 | P2/M | open | [P2][M] W6 seed-1 **recurrence half** — build the staged-diff CO-CHANGE checker with explicit A… | serialize-group `playbook` (n=11) |  |
| #356 | P2/M | open | [P2][M] **RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism … | serialize-group `playbook` (n=11) |  |
| #357 | P2/M | open | [P2][M] **Silent-rule census run 2** — sweep `docs/decisions/` under the [E8] declaration test,… | serialize-group `audit-py` (n=59) |  |
| #358 | P2/S | open | [P2][S] **`ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD** —… | serialize-group `architecture` (n=23) |  |
| #359 | P1/M | open | [P1][M] **PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a mechanism that … | serialize-group `handoff` (n=16) |  |
| #360 | P3/S | open | [P3][S] **`protocols/DEFINITION_OF_DONE.md:106-109` expired in place** — the `## Scope-freeze` … | serialize-group `audit-py` (n=59) |  |
| #361 | P3/S | open | [P3][S] **ADR-immutability's real coverage is declared only in code, never in the protocol** — … | serialize-group `audit-py` (n=59) |  |
| #363 | P2/S | open | [P2][S] **`codex-review` routed a CODE-shaped diff through the `gpt-5.6-sol` lane, not terra** … | serialize-group `codex-review` (n=6) |  |
| #364 | P3/S | open | [P3][S] **`doc_rot`'s length cap blocks [#353] from doing its job** — [#353] exists to accumula… | serialize-group `audit-py` (n=59) |  |
| #365 | P3/S | open | [P3][S] **Promote `residual_completeness` from `exempt:` to `coverage_scope`** — the doc-side r… | serialize-group `audit-py` (n=59) |  |
| #366 | P2/S | open | [P2][S] **`residual_completeness` scans the WORKING TREE, not the staged blob** — codex HIGH 20… | serialize-group `audit-py` (n=59) |  |
| #369 | P3/S | open | [P3][S] **Wire `boundary_headers.py --check` into pre-commit** — the generated-not-hand-maintai… | serialize-group `pre-commit-config` (n=6) |  |
| #371 | P2/S | open | [P2][S] **Consumer editor-config write-through — declared at v1.4.0, never built, never tickete… | serialize-group `settings-json` (n=20) |  |
| #399 | P2/S | open | [P2][S] **`templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)** — `… | serialize-group `handoff` (n=16) |  |
| #400 | P3/S | open | [P3][S] **Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — sam… | serialize-group `claude-md` (n=6) |  |
| #402 | P3/S | open | [P3][S] **Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling… | serialize-group `architecture` (n=23) |  |
| #413 | P2/S | open | [P2][S] **Colors semantics — visually distinguish global/hub-managed vs per-repo content in gov… | serialize-group `claude-md` (n=6) |  |
| #427 | P3/S | open | [P3][S] **Region templates carry a repo-POSITION-DEPENDENT path** (ai-council, 2026-07-26):... | serialize-group `claude-md` (n=6) |  |

### [E9] Fleet Desired-State System (North Star) (5)

| id | P/size | live status | subject | mechanical signals | verdict |
|---|---|---|---|---|---|
| #385 | P3/M | open | [P3][M] **L4 tech-currency lane** — nightly research on new Python tech/versions → version-bump… | serialize-group `architecture` (n=23) |  |
| #391 | P3/S | open | [P3][S] **Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter** — #38… | serialize-group `audit-py` (n=59) |  |
| #392 | P3/S | open | [P3][S] **fleet_analytics rename-alias loses history on path-reuse** — `scripts/fleet_analytics… | serialize-group `audit-py` (n=59) |  |
| #393 | P3/S | open | [P3][S] **corp-sca rot review — confirm-live-or-retire 3 candidates** — the first fleet_analyti… | serialize-group `audit-py` (n=59) |  |
| #394 | P3/S | open | [P3][S] **Analytics coverage gap — corp-monorepo no-edit-record blind spot** — the run found 31… | serialize-group `audit-py` (n=59) |  |

---

## Honest limits of this sheet

1. **132 of 139, and 0 of 2 fleet issues** — stated above, not buried. The uncovered 7 + 2 live in
   gitignored local artifacts.
2. **Subjects are quoted from the 2026-07-30 triage, not re-derived from today's task files.** A
   row whose text was edited since then will read stale here; the `live status` / `P/size` columns
   ARE current, so the two can disagree. Where they do, the task file wins.
3. **`deferred` is reported, never interpreted.** A parked target may or may not make its proposal
   closable; nothing here decides that.
4. **Blocker out-degree is a floor, not a census.** It counts only declared `depends-on` edges.
   A blocking relationship expressed in prose is invisible to this pass by construction — the same
   enumerated-vs-structural distinction R-A applied to `[#481]`.
5. **No proposal was re-verified against live code.** The triage spot-checked ~12 of 132; this pass
   adds no new evidence check, only current-state retrieval.

---

**Filed by:** CC night batch, 2026-08-04 · **Governs:** input to FR-8a / `[#487]` ·
**Cites:** `f6d271b1`, `docs/audits/2026-07-30-technical-proposals-2026-07-29-triage.md`,
`tasks/manifest.json`, `BACKLOG.md`
