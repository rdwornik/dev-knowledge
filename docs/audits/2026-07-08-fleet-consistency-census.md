# Fleet consistency census — 2026-07-08

<!-- scope: meta -->

> **Overnight mission 2026-07-07/08, Phase 2 (READ-ONLY census).** Five-part fleet audit
> across 7 repos + the Phase-1 operator-surface fix. Every claim carries an evidence command
> + excerpt; forks are recorded, never resolved unilaterally (frozen-contract mode).
>
> **Date note:** the work ran overnight 2026-07-07 (system clock 2026-07-07 02:00–04:00+);
> the doc carries the mission-specified `2026-07-08` name. Phase-1 stamps/commits are 2026-07-07.
>
> **Envelope honoured:** zero writes outside the hub deliverables; every consumer repo READ-ONLY
> (no edits, installs, or state-mutating organ runs — mutating organs recorded SKIPPED-WOULD-MUTATE);
> no OneDrive-zone operations. The one sanctioned registration write became a **drafted-not-landed**
> NEEDS-OPERATOR item (the target file does not exist — Part 5).

---

## Mission ledger (both phases)

### Phase 1 — operator-surface fix (hub, mutating) — COMPLETE ✅
Merged to `origin/main` as **d981f19** (`2ad33f5..d981f19`, `--no-ff`, block-ff-push passed); branch deleted.

| Block | Result | Commit |
|---|---|---|
| **1-B** intake/ → docs/intake/ | history-preserving `git mv` (6 files, 100% rename); 10 live-reference surfaces repathed; 5 dated docs kept content-intact (captured content, like ADR bodies) | `693cb6c` |
| **1-A** /handoff operator surface | PLAYBOOK §8 "How to hand off" (5-mode table + exact invocations + worked #278 example); handoff.md "Modes & exact invocation"; HANDOFF_PROCESS §13 + docs/handoffs/README pointers (pointer-only → no version bump, v5.7 stands) | `7339757` |
| **1-C** intake↔ADR traceability | ADR-template `Intake:` field + MUST-cite rule; ADR-98 `Intake: #1` backfill + amendment (docs/intake universal home + traceability); BACKLOG #280 filed (deploy-manifest gap) | `47d6a11` (+case-fix `7dd00c8`) |
| pre-existing fix | audit-index regen (`docs/audits/README.md` stale from prior c30b236; unrelated to intake) | `ca9ded0` |
| close | full pytest GREEN (1394 passed/2 skipped, parallel `-n auto`); ruff clean; ship-gate GREEN; JOURNAL SHA-anchored `b7a270d`; sandbox 5/5 mode shapes | — |

**Sandbox (agent-run) verification:** fresh clone, operator path, all 5 modes — architect (5-file incl SUPPLEMENT), execution (4-file, no SUPPLEMENT), epic (EPIC_BOOT+PROBES+EPIC_RETURN), developer (byte-identical to epic; header renders `epic`), functional (FUNCTIONAL_BOOT only; index lists all 5 docs/intake docs). Clone torn down, zero leftovers. **Acceptance bar met:** the exact epic-#278 invocation is readable off the command help + PLAYBOOK §8.

**No fork in Phase 1** — all three blocks landed clean.

### Phase 2 — census (read-only) — this document
- 6 read-only recon subagents (one per non-hub repo) + hub self-census + a Part-4 audits-vs-reality verifier + cross-repo synthesis.
- Anomalies: (1) **registration target `ECOSYSTEM.md` does not exist** → drafted-not-landed + NEEDS-OPERATOR (Part 5). (2) **demo-prep brief-premise stale** — mission said `feat/v2-sources-ingest` dirty=6; the repo is clean on `main` (state changed between reads; mission never touched it). (3) full serial pytest >5min (subprocess-heavy) — used `pytest -n auto` (2:13); recorded as a finding-adjacent note, not drift.
- Coverage gaps: audits-vs-reality sampled the last ~10 hub audits (not exhaustive); consumer repos enumerated at ROOT fully, subdirectories sampled.

---

## Part 1 — FILES (root + taxonomy + hygiene)

### Cross-repo matrix (the mission's named files)

| File | hub | ai-council | corp-monorepo | corp-ops | corp-sca | demo-prep | life-architect |
|---|---|---|---|---|---|---|---|
| `.gitignore` | ✓ | ✓ | ✓ (floor negations) | ✓ | ✓ | ✓ | ✓ |
| `.gitattributes` | ✓ | **✗** | ✓ (LF/CRLF) | **✗** | **✗** | **✗** | ✓ |
| `INSTALL.md` | ✗ (source) | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| `.methodology.yaml` | ✗ (source) | ✗ (correct) | ✓ (ruff divergence) | ✗ | ✗ | ✗ | ✗ |
| `.worktreeinclude` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `.pre-commit-config.yaml` | ✓ | ✓ | ✓ | **✗ (by design)** | ✓ | ✓ | ✓ |
| `.claude/` (tracked subset) | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `docs/` decisions/audits/… | full | partial | full (no handoffs/intake) | partial | partial | **full incl docs/intake/** | decisions+intake(root) |

**`.methodology.yaml`** (mission Q: *should ai-council have one?*) — it is the hub Informant's consumer **divergence-allowlist** (`scripts/enforcement_coverage.py` reads `<root>/.methodology.yaml` `sanctioned_divergences`, fail-soft). Present **only where a divergence exists**: corp-monorepo declares one (`ruff-gate`, its own ruff v0.15.8, review 2026-10-07, ADR-96). **ai-council should NOT have one** — it carries the non-waivable floor and declares no divergence, so absence = "nothing to waive" (correct). VERDICT: INTENTIONAL absence fleet-wide except corp-monorepo.

**`.worktreeinclude`** — present **only in the hub** (1 line). No consumer carries it; it is not orphaned (hub-local worktree-seeding aid). VERDICT: INTENTIONAL, hub-only.

**`.gitattributes` gap (DRIFT — mechanical-freezable):** absent on **4 consumers** (ai-council, corp-ops, corp-sca, demo-prep) — no EOL normalization on Windows repos. hub + corp-monorepo + life-architect have it. Low-risk (mitigated by CRLF-tolerant floor-hash + normalize_headers), but a fleet-parity gap. Target shape: `* text=auto eol=lf` (+ `*.ps1` CRLF where relevant).

### docs/ taxonomy vs the NEW convention (decisions/audits/handoffs/intake under docs/)

- **hub** — full: `docs/{decisions,audits,handoffs,intake,archive}`. `docs/intake/` is the Phase-1 relocation (this mission).
- **demo-prep** — **full hub-mirror incl. `docs/intake/`** (built to ADR-98; the NEW convention path). INTENTIONAL — the most doc-conformant unonboarded repo.
- **life-architect** — `docs/decisions/` + **`intake/` at ROOT** (ADR-98 "calibrated lighter", pre-#280 path). DRIFT-adjacent: uses root `intake/`, not `docs/intake/` — the exact split #280 targets.
- **ai-council** — `docs/{decisions,audits,archive}`; **NO `docs/handoffs/`, NO `docs/intake/`** — the intake doc + ADR-98 lane designs are filed under `docs/audits/`. NEEDS-RULING (intended divergence vs drift).
- **corp-monorepo** — `docs/{decisions,audits,archive,diagrams}`; no handoffs (ADR-36 design), no intake-under-docs. INTENTIONAL.
- **corp-ops / corp-sca** — `docs/{decisions,audits,archive}` (ADR-60 child variant); no handoffs (centralized in hub). INTENTIONAL.

**Finding:** the fleet is **split on intake location** — demo-prep=`docs/intake/` (new), life-architect=`intake/` (root), ai-council=under `docs/audits/`. Corroborates the Phase-1 `docs/intake/` universal convention + BACKLOG #280 (propagate it at deploy).

### Per-repo root verdicts (highlights; full enumeration in recon)
- **hub** — every root entry INTENTIONAL. `node_modules/` + `temp/` present but gitignored (`temp/` is BACKLOG #229, operator-gated). `JOURNAL.md` 1.17MB / `LESSONS.md` 180KB — large but append-only by design (not bloat). No DRIFT/GARBAGE at root.
- **ai-council** — all INTENTIONAL; **`.claude/worktrees/fable-audit/` hollow orphan** (LEFTOVER, gitignored, not a registered worktree — flag only).
- **corp-monorepo** — all INTENTIONAL; **byte-identical 1.08MB `hybrid_classifier.json` duplicated** in `models/` + `src/corp/extractor/data/` (DRIFT/NEEDS-RULING — artifact vs shipped package-data); **`.claude/worktrees/cm-deep-vault/` hollow orphan** (LEFTOVER).
- **corp-ops** — **`tasks/` dir** (`todo.md`+`lessons.md` empty pre-canonical stubs, superseded by BACKLOG/LESSONS/JOURNAL, orphaned) → DRIFT/NEEDS-RULING; **no git remote (local-only)** — no off-machine backup.
- **corp-sca** — all INTENTIONAL; feature branch `feature/tenrox-loader` 6 commits ahead of main, **unpushed** (no origin backup).
- **demo-prep** — all INTENTIONAL; tracked BY platform knowledge PDFs (up to 3.6MB) pushable to a personal-account remote (within ADR-001 policy; operator eyes-on flag).
- **life-architect** — all INTENTIONAL; personal health/family content by design (`dimensions/D04-health`, `seed/`).

### Hygiene sweep
- **Secrets:** ZERO secret-shaped strings in tracked files on **all 7 repos** (only detector-regexes / AWS-doc-examples in corp-monorepo). `.env` files are untracked/gitignored everywhere. CLEAN fleet-wide.
- **Oversized tracked:** hub JOURNAL 1.17MB (append-only); corp-monorepo 1.4MB audit-inventory JSON + the 1.08MB×2 duplicate; demo-prep knowledge PDFs (3.6MB, by design). No stray/accidental binaries.
- **Stale branches:** none on hub/ai-council/corp-monorepo/corp-ops/life-architect (main + working branch only). corp-sca + demo-prep carry multiple feature branches (several merged) — minor cleanup candidates, not stale-in-flight.
- **Fleet LEFTOVER pattern:** `.claude/worktrees/<name>/` hollow orphans on **ai-council (fable-audit)** + **corp-monorepo (cm-deep-vault)** — the "worktree remove blocked by live session" gotcha; gitignored (cosmetic) but violates No-leftovers §5.9. Operator-gated cleanup when owning sessions close.

---

## Part 2 — CODE (review + organs-in-effect)

### Refactor candidates (flagged, never fixed)
- **hub** — n/a (governance repo; validators only).
- **ai-council** — `tests/test_research.py` 1760 lines/91 defs (dominant split candidate); `cli.py` 639, `output.py` 487 (source). TODO=0.
- **corp-monorepo** — `extract.py` 1184, `inbox.py` 951, `router.py` 893; test files >1000 lines. TODO≈0 (4 enum hits).
- **corp-ops** — `backup-onedrive.ps1` 374 (only decomposition candidate). TODO=0.
- **corp-sca** — `run.py` 562, `gap_filler.py` 450. TODO=0 (1 format-placeholder FP).
- **demo-prep / life-architect** — content/placeholder repos; no authored product code to refactor.

### Test-theatricality pre-scan (feeds #278)
**CLEAN fleet-wide** — zero `assert True`/`assert 1 ==` on any repo; all `def test_…():`-EOL regex hits are real multi-line-body tests (spot-verified). One #278-relevant *shape* (not theatre): ai-council `test_base_provider.py` = 28 one-assertion tests (parametrize candidate, each asserts real behaviour). **Data point for #278: high test counts are backed by real assertions, not counter-padding.**

### Organ verification (read-only; WORKS / BROKEN / NOT-WIRED / ABSENT / SKIPPED-WOULD-MUTATE)

| Organ | hub | ai-council | corp-monorepo | corp-ops | corp-sca |
|---|---|---|---|---|---|
| `audit.py` health / doc_rot / doc_code_edge / import_edges | **WORKS** (29 checks; import_edges OK, doc_code_edge 12 resolved, doc_rot OK) | ABSENT (hub-only) | ABSENT (hub-only) | ABSENT (hub-only) | ABSENT (hub-only) |
| `check_floor_hash.py` (floor guard) | n/a (source) | **WORKS** (exit 0) | **WORKS** (hash match `4d268f3…`) | n/a | **WORKS** (hash match) |
| `canonical_freshness_gate.py` | **WORKS** (rc 0) | **WORKS** (rc 0) | **WORKS** (rc 0, **WARN 3 docs >30d**) | ABSENT | ABSENT |
| `session_end_backpressure.py` | WORKS | **WORKS** (RO, silent on empty stdin) | WORKS | ABSENT | ABSENT |
| Tach (import boundaries) | n/a | ABSENT | **WORKS, DOUBLE-enforced** (pre-commit + CI, "[OK] All modules validated!") | ABSENT | ABSENT |
| pyright reverse-dep oracle | n/a | ABSENT | **ABSENT as oracle** (Pylance `basic` editor-only; no config/CLI/CI) | ABSENT | ABSENT |
| `enforcement_coverage.py` | present (needs `--run-date`) | ABSENT (subject, not host) | ABSENT (subject) | ABSENT | ABSENT |
| mutating organs | `current_state_audit`-class n/a | `normalize_headers.py` **SKIPPED-WOULD-MUTATE** | `current_state_audit.py` **SKIPPED-WOULD-MUTATE** | `sync-mywork.ps1` **SKIPPED** (OneDrive read-source; described from source) | — |

**Highlights:** corp-monorepo's **Tach is the healthiest fleet organ** (double-enforced, 4-layer, pinned). **pyright is NOT wired as a reverse-dep oracle anywhere** (only Pylance editor mode) — the mission's "pyright reverse-dep oracle if wired" is answered: not wired. Consumer conformance (`audit.py`) is **hub-only by construction** — consumers carry the deployed floor/freshness/backpressure organs, not the hub validators.

---

## Part 3 — CONVENTIONS (naming + legacy)

### BACKLOG-scheme census
| Repo | Scheme |
|---|---|
| hub | ADR-66 story-map (themes → stories → `[#id][P][size]` + Done-when + refs) |
| corp-monorepo | ADR-66 story-map (matches hub; `[#N]` numeric) |
| corp-ops | ADR-66 story-map (1 open item) |
| corp-sca | ADR-66 story-map (`[#1]`–`[#9]`) |
| demo-prep | ADR-66 story-map (own 3-digit ADR-001/002) |
| life-architect | ADR-66 story-map (hand-followed, no validate-backlog gate) |
| **ai-council** | **Track-X backbone + story-map hybrid** (Tracks A–F; stories carry `[#id][P][size]`+Done-when) |

### ADR-99 convergence — did the P6/#221 closure fire its trigger? **NO (FINDING).**

ADR-99 clause (A), VERBATIM:
> "**(A) at P6 — converge on one scheme.** When the methodology corpus rolls to ai-council (**P6 / #221**), carry the ADR-66 story-map + `validate_backlog` as part of that deploy, converging on **one enforced, traceable, non-colliding scheme fleet-wide**."

Interim (VERBATIM): *"until P6, two structural schemes still exist — hub ADR-66 story-map, ai-council Track-X lettered streams — but the names no longer collide. The `[#id]` monotonic traceability + validator suite reach ai-council only at P6."*

**Live check:** #221 is CLOSED (`8933007`, merged `8aab435`) — but it closed on the **corp-monorepo n=2 deploy**, NOT on carrying the story-map to ai-council. The deploy manifest (`deploy/manifest-v*.yaml`) ships **no `validate_backlog` / story-map component**, and ai-council's BACKLOG is confirmed still **Track-X** (recon). So ADR-99's convergence clause (A) **did NOT fire**; ai-council remains on Track-X; and the **#221 peg the convergence was pinned to is now closed** → the convergence is **orphaned** (its trigger ticket is gone). NEEDS-RULING: re-peg the ai-council story-map convergence to a new ticket, or accept Track-X as durable.

### Legacy-Mermaid codemap inventory (cross-ref #262)
| Repo | Mermaid | Verdict |
|---|---|---|
| hub | none in canonical docs; `.md` fences only in frozen audits + `docs/handoffs/README.md` (human-facing, INTENTIONAL per ADR-59) | CLEAN (ADR-51 amendment held) |
| **corp-monorepo** | **3 `.mermaid` files (`docs/diagrams/`) + 2 blocks in `ARCHITECTURE.md` (L72, L275)** | NEEDS-RULING (sanctioned hand-authored codemap ADR-25 vs drift behind ADR-51-out) |
| **ai-council** | **2 blocks in `ARCHITECTURE.md` (L23, L109)** | DRIFT-candidate (behind ADR-51 Mermaid-out) |
| corp-ops / corp-sca / demo-prep / life-architect | none | CLEAN (corp-ops CLAUDE §11 has stale "Mermaid codemap" phrasing but no actual Mermaid) |

**Finding:** legacy Mermaid persists in canonical `ARCHITECTURE.md` on **corp-monorepo + ai-council** — the two repos behind the hub's 2026-07-05 ADR-51 Mermaid-relocation. #262's Done-when should enumerate these exact sites.

---

## Part 4 — TRUTH (currency + audits-vs-reality)

### Hub currency table (`last_reviewed` vs last git-touch; gated?)
| Doc | last_reviewed | last-touch | gated | note |
|---|---|---|---|---|
| VISION.md | 2026-06-19 | 2026-06-19 | GATED | fresh |
| ARCHITECTURE.md | 2026-07-07 | 2026-07-07 | GATED | fresh |
| CLAUDE.md | 2026-07-07 | 2026-07-06 | GATED | fresh |
| CONTRIBUTING.md | 2026-07-07 | 2026-07-06 | GATED | fresh |
| protocols/ESSENTIALS.md | 2026-07-05 | 2026-07-05 | GATED | fresh |
| docs/handoffs/README.md | 2026-07-07 | 2026-07-07 | GATED | fresh |
| **protocols/PLAYBOOK.md** | **none** | 2026-07-07 | **NOT-GATED** | **large canonical doc, no stamp, ungated** |
| protocols/HANDOFF_PROCESS.md | none | 2026-07-07 | not-gated | version-gated instead (reconciled_versions @5.7) — OK by design |
| **protocols/SESSION_SETUP.md** | **none** | 2026-06-21 | **NOT-GATED** | ungated protocol doc |
| **protocols/AI_COUNCIL_PROCESS.md** | **none** | 2026-06-01 | **NOT-GATED** | ungated, oldest-touched (2026-06-01) |
| BACKLOG.md | none | 2026-07-07 | not-gated | living/in-place by design (validate_backlog gates schema) |

### Hub gating-coverage (generalizes the Arc-5 PLAYBOOK finding)
`_FRESHNESS_FILES` = {VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, ESSENTIALS, docs/handoffs/README}. **Ungated canonical/living docs: PLAYBOOK (biggest gap — no stamp at all), SESSION_SETUP, AI_COUNCIL_PROCESS.** HANDOFF_PROCESS is version-gated instead (fine). **Finding:** the freshness gate covers 6 of ~9 canonical/protocol docs; PLAYBOOK — one of the two largest, most-load-bearing docs — is entirely outside it.

### Fleet freshness (generalized)
Freshness enforcement exists **only where the `canonical_freshness_gate` organ is deployed** (hub, ai-council, corp-monorepo). Consequence: **corp-sca CLAUDE.md §9 is stale AND wrong** (claims "no hooks"; floor-hash-verify is active since ~Jun-8) and **nothing catches it** (no audit.py). corp-monorepo's freshness organ DOES catch its own soft-drift (3 docs >30d WARN). ai-council is fresh. **Pattern: the hub's own PLAYBOOK-ungated gap generalizes fleet-wide** — uninstrumented docs rot silently.

### Audits-vs-reality (23 claims sampled from the last ~10 hub audits, verified live)

Sampled: `2026-07-07-changelog-review`, `-overnight-mission-ledger`, `-stage3-adjudication-memo`, `-ai-council-measurement-4`, `2026-07-06-arc5-{buy-vs-build-verdicts,must-verification,routines-pilot-design}` (+ cross-refs). **Result: 22 MATCH / 1 DRIFTED.**

Representative MATCH rows (all with evidence commands in the recon transcript):
- `ALL_CHECKS` grew 28→29, `check_import_edges` added as a FAIL-tier @import gate — **MATCH** (count=29, last=`check_import_edges`).
- `claude-rosters-freshness` hook added, gate count 11→12 — **MATCH** (`.pre-commit-config.yaml` 12 ids).
- `gen_audit_index.py` + audit-corpus index — **MATCH** (README "199 audit documents"; index current at 199 — *note: current only because this mission's `ca9ded0` regenerated it*).
- 16 evidence SHAs (block leaves/merges) are real commits with matching subjects — **MATCH**.
- Sonnet-5 pins refreshed (`608eed6`/`399c843`, string `claude-sonnet-5`) — **MATCH**.
- ADR-70 XL=Fable-5 amendment (browser-architect only, anti-conflation) — **MATCH** (ADR file Accepted).
- Closed ids (#225/#233/#247/#118/#159/#249/#250/#236/#237) left BACKLOG (done-items-leave) — **MATCH** (only `refs` prose remains).
- #262 OPEN (hub-side done, child-side remains) · #267 OPEN (half-b done, half-a DEGRADED) · #264 PARKED · #239/#240 open — **MATCH**.

**The DRIFT (row 7, benign lifecycle):** the `2026-07-07-overnight-mission-ledger` audit's Block-4 review pointer — *"3 DRAFTs on `drafts/2026-07-07-proposals` (head `3da29ea`), NOT merged; review via `git show <branch>`"* — is now **dead**: those drafts were **ratified into ADR-98/99/100**, the DRAFT files removed, and the branch ref pruned, so `git show drafts/2026-07-07-proposals` fails (`fatal: Needed a single revision`). This is the intended drafts→ADR lifecycle, but it leaves a **stale non-executable pointer in an immutable audit** — the inverse of a ruled-but-not-executed retirement. Finding only (immutable audit; not fixable in place).

**RETIRE-verdict check (the special-attention target):** all four `2026-07-06-arc5-buy-vs-build` RETIRE verdicts were written **conditional**, and **no trigger condition has fired** — so correctly **nothing was retired** (verdict-consistent): (1) Routines/nightly-harness retire gated on the second routine landing (post-#270, n=2) — not in effect; (2) /batch/ADR-97 hand-provisioning retire gated on scale-adoption — not run; (3) manual RETURN-triage retire gated on Outcomes reaching CC — still Agent-Platform-only; (4) stored-viz + `mermaid_emit.py` retire gated on #264 unpark — still PARKED, file present-and-unwired. **No ruled-but-not-executed retirements** — the audit corpus's retirement discipline is clean.

**Verdict:** the last ~10 hub audits are **highly accurate against live state** (22/23), the single drift is a benign ratification artifact, and every conditional RETIRE is correctly un-fired. Audit-corpus trustworthiness: HIGH.

---

## Part 5 — FLEET (enforcement + new projects)

### Enforcement map per consumer (presence ≠ enforcement)
| Repo | git hooks (armed) | core.hooksPath | floor | plugin | commit-gate | CI |
|---|---|---|---|---|---|---|
| **corp-monorepo** | pre-commit + commit-msg + pre-push | unset (no relic) | PRESENT, hash INTACT | enabled | ruff + tach + floor + freshness + toc | tach.yml + nightly-conformance-triage |
| **ai-council** | pre-commit + commit-msg + pre-push | unset | PRESENT, INTACT | enabled | floor + canonical_freshness + toc + backlog-id | — |
| **corp-sca** | pre-commit (floor-hash only) | unset | PRESENT, INTACT | enabled | **floor-hash ONLY** (ruff asset unwired) | — |
| **demo-prep** | pre-commit + pre-push | unset | ABSENT | — | ruff + repo-invariants (self-adopted) | — |
| **life-architect** | pre-commit | unset | ABSENT | — | baseline (whitespace/yaml/ruff) | — |
| **corp-ops** | **none (only *.sample)** | unset | ABSENT | enabled (CC-only) | **NONE at git level (manual by design)** | — |

**Enforcement gradient:** corp-monorepo (fullest — floor+tach+CI+freshness, v1.2.0) ≈ ai-council (deploy #1, 3 hook stages) > demo-prep / life-architect (baseline pre-commit armed, self-adopted, no mesh) > corp-sca (floor-hash only) > corp-ops (zero git hooks, manual by documented design). **Presence ≠ enforcement confirmed twice:** (1) corp-ops's enabled plugin gates nothing at commit time; (2) the shipped `assets/ruff-pre-commit.yaml` is unwired on corp-sca AND corp-ops (asset present, gate dormant). **All 6 consumers: `core.hooksPath` unset** — the relic-hooksPath disarm gotcha (n=2 hub/ai-council history) does NOT recur anywhere now. **Floor hash `4d268f32…8111f` verified INTACT** on all three floor-carrying consumers.

### New-project recon

**demo-prep** — *Blue Yonder corporate presentation creation.* On `main`, clean (743 files, media-heavy). Origin `github.com/rdwornik/demo-prep`. **Grew its own `docs/intake/`** (ADR-98 format — the new convention path) + full hub docs taxonomy + own 3-digit ADRs + armed pre-commit/pre-push. Methodology mesh deferred (`[#8b]`, riding P6). Self-adopted more hub convention than any other unonboarded repo.

**life-architect** — *persistence + governance layer for the "architect of life" workflow.* On `research/taxonomy-v2` (main published, in sync). Origin `github.com/rdwornik/life-architect`. **Grew its own `intake/` (root)** (ADR-98 "calibrated lighter") + `docs/decisions/` (5 genesis ADRs) + armed baseline pre-commit. Methodology-unonboarded by design (ADR-04). Holds personal health/family content by design.

### Registration — DRAFTED, NOT LANDED (NEEDS-OPERATOR)

**The mission's one sanctioned write could not land: the target does not exist.** There is **no `ECOSYSTEM.md` at root and no `.ecosystem` file**. The actual fleet registry is:
- `ecosystem/<repo>/` **subdirectories** (enumerated by `fleet_health.py` via `iterdir()`; 5 repos registered) — each holds a **gitignored** `state.yaml` + tracked `history/*.md`.
- `ecosystem/deployed-versions.yaml` (tracked, **version-keyed** — not purpose).
- `ecosystem/index.yaml` (**GENERATED** — `audit.py::regenerate_index` overwrites wholesale; stale @2026-06-02; **do not hand-edit**).

**No tracked file carries a `name + path + purpose + status` schema.** Per the mission's own anti-fabrication guard + CLAUDE.md §5 ("no new markdown files without checking growth triggers") + the Layer-2 no-orchestration boundary, I did **not** fabricate a registry file/convention. The two entries are drafted here, ready to land once the operator rules on the mechanism (create a hand-maintained `ECOSYSTEM.md`? extend `deployed-versions.yaml` with a purpose axis? create `ecosystem/<repo>/` subdirs — which need an audit run to populate committably?).

**Drafted entry — demo-prep:**
```
name:    demo-prep
path:    C:\Users\1028120\Documents\Dev\demo-prep
purpose: Single home for Blue Yonder corporate presentation creation — brand kit ·
         templates · knowledge base · deck-production pipeline · generator patterns +
         reference decks; explicit precursor to a corp-monorepo presentation module.
status:  registered / methodology-unonboarded
```

**Drafted entry — life-architect:**
```
name:    life-architect
path:    C:\Users\1028120\Documents\Dev\life-architect
purpose: Persistence + governance layer for the operator's "architect of life" workflow —
         archives ephemeral per-dimension browser chats into durable work-items, knowledge
         notes, and decision records; a sibling applying the dev-methodology loop to life
         domains (horizon: a "Life OS").
status:  registered / methodology-unonboarded
```
Both purposes are stated **unambiguously from each repo's own VISION/ARCHITECTURE/CLAUDE** (not fabricated). Companion NEEDS-OPERATOR: confirm `github.com/rdwornik/life-architect` is **Private** (health/family content; its own CLAUDE mandates private; not verifiable read-only).

---

## TRIAGE QUEUE

### A — mechanical-freezable now (deterministic, low-judgment)
1. **`.gitattributes` on 4 consumers** (ai-council, corp-ops, corp-sca, demo-prep) — add `* text=auto eol=lf`. *Proposed BACKLOG: [P3][S] EOL-normalization parity.*
2. **audit-index freshness has no pre-commit gate** (hub) — the `test_gen_audit_index` red this mission cleared (`ca9ded0`) can recur; add a `gen_audit_index --check` pre-commit hook (mirrors codemap/toc). *Proposed BACKLOG: [P3][S] gate the audit index.*
3. **corp-ops `docs/audits/README.md` "Current contents: (Empty)"** stale (2 files tracked) — regen. (Consumer-side; hub cannot write it — route to corp-ops chat.)

### B — needs-ruling (a genuine fork; operator/architect decides)
4. **ADR-99 convergence orphaned** — #221 (its peg) closed on the corp-monorepo deploy without carrying the story-map to ai-council; the deploy manifest ships no `validate_backlog`. Re-peg to a new ticket, or accept Track-X as durable. *Proposed BACKLOG: [P2][S] re-peg ai-council story-map convergence.*
5. **Legacy Mermaid in canonical `ARCHITECTURE.md`** on corp-monorepo (3 files + 2 blocks) + ai-council (2 blocks) — sanctioned hand-authored codemap (ADR-25) vs drift behind ADR-51-out. Fold into #262's Done-when.
6. **ai-council docs/ taxonomy partial** — no `docs/handoffs/` or `docs/intake/`; intake under `docs/audits/`. Intended divergence or drift?
7. **corp-ops `tasks/` dir** — orphaned pre-canonical stubs. Delete (operator-gated) or ticket.
8. **corp-monorepo `hybrid_classifier.json` 1.08MB duplicate** (models/ + src/) — de-dup or accept artifact-vs-shipped.
9. **ruff-gate asset unwired** on corp-sca + corp-ops — install the documented gate, or accept manual-lint (route to each consumer chat).

### C — needs-operator-input (can't proceed without a decision/fact)
10. **ECOSYSTEM registration mechanism** — the target `ECOSYSTEM.md` doesn't exist; rule on how to register (both entries drafted above). *The mission's one sanctioned write, held pending this ruling.*
11. **life-architect GitHub Private?** — confirm before any push (health/family content).
12. **Fleet `.claude/worktrees/<name>/` hollow orphans** (ai-council, corp-monorepo) — operator-gated cleanup when the owning sessions close (do not self-delete).
13. **corp-ops has no git remote** (local-only) — intended, or is an off-machine backup expected?
14. **corp-sca CLAUDE.md §9 stale + wrong** (claims "no hooks"; floor-hash active) — route to corp-sca chat to re-stamp; symptom of no freshness organ deployed there.

### Proposed BACKLOG items (listed here, NOT filed — per envelope)
- `[P2][S]` Re-peg the ai-council ADR-66 story-map convergence (ADR-99 (A)) — #221 closed on the corp deploy without firing it. refs ADR-99, #221, deploy/manifest.
- `[P3][S]` Gate the audit index — add `gen_audit_index.py --check` as a pre-commit hook (silent-rot class; this mission cleared one instance). refs scripts/gen_audit_index.py, ca9ded0.
- `[P3][S]` Fleet `.gitattributes` EOL-normalization parity (4 consumers lack it). refs Part 1 matrix.
- `[P3][S]` Extend hub freshness gating to PLAYBOOK (+ SESSION_SETUP / AI_COUNCIL_PROCESS) — the largest ungated canonical doc. refs canonical_freshness_gate.py, _FRESHNESS_FILES.

---

**Compiled by:** CC (Opus 4.8), overnight mission Phase 2, 2026-07-07/08. Read-only across the fleet; every consumer byte-untouched.
