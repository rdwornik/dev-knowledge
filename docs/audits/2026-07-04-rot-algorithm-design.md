# Rot-algorithm design — nightly reverse-dependency / referential-integrity report

<!-- scope: meta -->

> **Type:** design doc / audit (findings-and-proposal, ADR-60 `docs/audits/` zone). Immutable once landed — supersede with a new file, do not edit in place. NOT an ADR: the ratifying ADR for the chosen design is a separate, operator-approved step.
> **Date:** 2026-07-04 · **Read at HEAD** `86aec77` in worktree `fable-rot-design` · **Author:** Claude Fable 5 (`claude-fable-5`), read-only session — DESIGN ONLY per the operator mandate (no code; this artifact is the session's only repo write, operator-approved landing).
> **Grounding:** live reads of `scripts/scan_undeclared_edges.py` (#179), `scripts/reverse_dep_oracle.py` (#193), `scripts/safe_remove.py` (#195), `scripts/validate_reconciliation.py`, `scripts/validate_doc_structure.py`, `ecosystem/doc-code-edge.yaml`, `deploy/manifest-v1.2.0.yaml`, ADR-96, `scripts/enforcement_coverage.py`, the `audit.py` registry (28 checks), BACKLOG (full), the 2026-07-04 Fable architecture review §5/§6, the JOURNAL coherence / deletion (#244 P2) / conformance arcs, and the live nightly infrastructure (ADR-74/76 two-track model; the `\DevKnowledge\fleet-baseline` Task Scheduler task verified REGISTERED and Ready on the operator's machine, next run 09:00).
> **Operator approval recorded:** design + landing path approved in-session 2026-07-04; defaults D-A…D-D (§9) unremarked, so they stand as stated.

---

## 0. Verdict in one paragraph

**Build it, but small — and it is mostly an assembly job, not an invention.** The corpus already computes four edge families (declared doc→spec, undeclared prose→spec, doc→code rule-IDs, code→code Pyright) and already has a deterministic nightly host (ADR-76 Task Scheduler, verified armed). What is genuinely missing is exactly the operator's scenario ("delete `essentials` → it is referenced in N places → those references must propagate"): **no mechanism answers "who references X?" for an arbitrary corpus artifact, and nothing runs that question on a cadence** — every existing organ is commit-event-driven, registry-scoped (the spec registry holds ONE entry), or code-only. The right mechanism is one new read-only script (`scripts/rot_report.py`): a typed reverse-reference index rebuilt from scratch each night (seconds, zero LLM), three existence predicates plus a blast-radius query, a delta-aware morning report surfaced at SessionStart. The full "dependency graph database + per-node staleness scoring" version of this idea IS over-engineered; the reverse index + existence predicates + `--impact` query is not, and the #199 precision lesson (245 candidates → 12 after immutable-zone pruning) is the load-bearing reason it can be signal rather than noise.

---

## 1. Inventory — what already exists (and what each does NOT do)

The mandate's premise ("today nothing catches this except a human noticing") is **true only at the corpus-reference layer**. Three adjacent layers are already solved or filed:

- **Code→code removal — SOLVED, event-driven.** `reverse_dep_oracle.py` (#193) computes reverse-dependents via a headless Pyright `references()` query with mandatory provenance; `safe_remove.py` (#195, audit check `safe_removal`) blocks removing a `scripts/` module with surviving external referrers, at commit time, from the git diff. Does NOT: run on a cadence, see cross-language edges (its own stated ADR-89 limit: markdown→script, settings.json / pre-commit hook-wiring, plugin manifests are INVISIBLE), or cover docs. The M2/M3 extension (path-string + declared-prose referrers) is filed as **#218**, not built.
- **Deploy-layer removal — SOLVED as of 2026-07-04, hub→consumer.** ADR-96 / #244 P2: a `status: removed` manifest component is pruned from a consumer, hash-guarded (locally-modified target REFUSED), verified ABSENT independently of detect (D9). Does NOT: touch the hub's own prose — the tombstoned component's roster lines, doc mentions, and teaching references across the hub corpus stay wherever they are. P4 (sync surfacing) and P5 (hub self-prune) are the filed-but-unbuilt phases this design feeds.
- **Declared doc edges — SOLVED, but nearly empty.** `reconciled_with: <spec-id>@<ver>` frontmatter → `validate_reconciliation.py` → the `reconciled_versions` ship-gate FAIL, plus the `check-against-spec` re-stamp flow. Does NOT: see undeclared references (that is #179's discovery scan — candidates surfaced for human confirm, NO auto-declare; currently 12 tier-1 candidates awaiting the #241 groom), and `_SPEC_REGISTRY` holds exactly one spec (`handoff-process`).
- **Intra-file staleness — SOLVED per class.** `canonical_freshness` (check #10, `last_reviewed` vs last edit), `doc_claims` (a doc's own counts), `doc_rot` (accretion/file-budget/grooming-cadence), `doc_structure` (numbering / header scheme / ToC — including *intra-doc* dangling ToC entries, but nothing cross-file).
- **Nightly hosts — TWO exist** (the ADR-74 layer→job matrix):
  - *Track A, cloud:* the nightly conformance Routine (spec-orchestrated read-only verifiers + skeptic + digest) → PR diff-guarded by `.github/workflows/nightly-conformance-triage.yml` → digest diverted to the `automation/conformance-digest` branch (never `main`, ADR-84) → `nightly-triage` Issues → surfaced at SessionStart by `scripts/surface_triage.ps1`.
  - *Track B, local:* Windows Task Scheduler task `\DevKnowledge\fleet-baseline` (registered by `scripts/setup-fleet-scheduler.ps1`; daily 09:00, `StartWhenAvailable=ON`, `WakeToRun=OFF`, 15-min execution cap) running `python scripts/fleet_health.py` directly — **no `claude -p`, no LLM on the scheduled path** (ADR-76 decision) — writing the gitignored `logs/FLEET-HEALTH.md`.
  - Track B is the pattern this design rides.

**The gap, precisely:** a *file-and-organ-level reverse-reference index over the whole actionable corpus*, with existence predicates, on a cadence. Live evidence the class is real: `protocols/ESSENTIALS.md` is referenced today from **~15–20 actionable files** (ARCHITECTURE ×5, CLAUDE.md ×9, PLAYBOOK ×15, VISION ×4, BACKLOG ×7, SESSION_SETUP ×8, DEFINITION_OF_DONE, two commands, the conformance workflow, tests, both manifests, `doc-code-edge.yaml`, the disposition register) — delete or move it and every one dangles silently; no organ would say a word until a human tripped over one. (386 raw occurrences across 60+ files, but the majority sit in the immutable/append-only zone — which is exactly why the #199 actionable-corpus pruning is load-bearing for precision.)

---

## 2. Graph construction (mandate Q1)

**Shape: not a tree, not a package graph — a typed reverse-reference multimap, rebuilt from scratch every run.** `target-node → [(source, line, edge-kind)]`. The corpus is ~715 markdown files plus configs; a full scan is seconds of pure Python. A persistent/incremental graph store would be machinery without a customer — rebuild-per-run is the correctness guarantee, the same doctrine as `validate_doc_code_edge.build_edge_index` (rebuildable index, never a hand-kept cache).

**Node universe (typed, enumerated from live state — never a hand-kept list):**

- `file` — every git-tracked path (`git ls-files`)
- `command` — `.claude/commands/*` + plugin commands + user-level (`~/.claude/commands`) (the #132 organ walk, subsetted)
- `skill` — `.claude/skills/*` + `~/.claude/skills/*`
- `organ/hook` — `.claude/settings.json` hooks + `.pre-commit-config.yaml` entries
- `check` — `audit.py` ALL_CHECKS names
- `component` — manifest `components:` ids + their lifecycle `status`
- `spec` — `_SPEC_REGISTRY` ids

**Edge extractors (reuse, don't re-parse — each already has an owner):**

- **X1 path-verbatim (NEW, the core):** a repo-relative path or distinctive basename mentioned in an actionable-corpus doc → `file` node. This is #179's tier-1 matcher *generalized from the 1-entry spec registry to the full tracked-file universe*, inheriting its fenced-block exclusion (a fenced command example is not a content-dependency) and its #199 actionable-corpus pruning (immutable/append-only zones + gitignored scratch are never sources — a JOURNAL mention of a dead file is history, not rot). Basename matching only where the basename is repo-unique (the #179 note: `.md` + SCREAMING_SNAKE stems are distinctive; `README.md` is not).
- **X2 declared edges:** import `validate_reconciliation.enumerate_edges` output as-is.
- **X3 rule-ID edges:** import the `validate_doc_code_edge` rebuildable index as-is.
- **X4 wiring edges (NEW extractor, cheap):** `settings.json` hook commands → script paths; `.pre-commit-config.yaml` `entry:` lines → script paths; plugin manifest → scripts/commands. This is precisely the cross-language edge class the Pyright oracle declares INVISIBLE — closing it deterministically here is the single highest-value new cell.
- **X5 manifest edges:** component `artifacts.path/source` → file nodes; component id → its `status`.
- **X6 organ-name tokens (v1.1, deferred):** `/command-name` and check-name tokens in prose → organ nodes. Deferred because precision is unproven; path-verbatim ships first, token matching follows once the live noise floor is measured.
- **Code→code: deliberately EXCLUDED from the nightly.** Per-symbol Pyright queries are the one expensive extractor, and their consumer (`safe_removal`) already fires at the right moment — commit-time, on an actual deletion diff. A nightly re-ask answers no standing question.

---

## 3. Per-node-type rot predicates (mandate Q2)

The report is signal only if "rotted" is defined per type, and only for cells no existing organ owns:

- **`file` target — P1 DANGLING-PATH:** an actionable-corpus source references a repo-relative path that no longer resolves. Git-aware sub-classification: basename still exists elsewhere (e.g. under `archive/` or `~/.claude/archive/`) → **moved — repoint**; gone entirely → **deleted — rewrite or drop the reference**. An "(archived …)" annotation on the same line, or an inline `<!-- rot-allow: <target> — <reason> -->` marker, suppresses the finding (the `structure-allow` co-located-marker precedent from `validate_doc_structure.py` — CLAUDE.md §7's deliberate `/boot (archived …)` lines must NOT flag).
- **`organ` target — P2 DANGLING-WIRING:** a `settings.json` / pre-commit / plugin wiring edge points at a script that does not exist — a configured organ that can never fire. Fail-loud class; near-zero false-positive rate expected.
- **`component` target — P3 TOMBSTONE BLAST-RADIUS:** for every manifest `status: removed` component, enumerate live actionable-corpus references to its id, artifacts, and roster line — "removed at the deploy layer; these N hub surfaces still present it as live." This is the deletion-propagation one-to-many made mechanical, and the standing feed for #244 P4/P5.
- **`spec` / declared-edge staleness — already owned** (`reconciled_versions`, `undeclared_edges` at ship-gate) — the nightly **aggregates** their current output into the morning view (giving them a cadence independent of shipping activity), never re-implements them.
- **In-degree-zero organs (informational, not an alarm):** the reverse index yields orphans for free — commands/checks/skills nothing references (the RF-8 v4-era-check class), gotchas dormant by `Last triggered` age. Rendered as a "prune candidates" appendix feeding #244 P5 / #130 / #212. Surfaced-not-alarmed; never counted in the headline.
- **Explicitly NOT predicates (deterministic honesty):**
  - *Semantic claim-drift* — a comment or prose claim asserting superseded behavior — is invisible to existence checks. Live proof found during this audit: `deploy/manifest-v1.2.0.yaml` L40-43 still claims `components:` is "INERT to deploy/tool.py this release (the tool reads only `carriers:`)" and `deploy/release_lint.py`'s docstring still says only `status: active` is legal — both false since P2 shipped the same day, and every path in them resolves fine. That class belongs to the operator's continuous-conformance vision (LLM tail — #220 / Track A, with binary verdicts + `evidence_command` per the 2026-07-04 review §5), behind its own adoption gate — not this organ.
  - *Backlog-id references* are OUT: done-items-leave (ADR-65) makes departed `[#id]` mentions legitimate history, so flagging them manufactures noise.

---

## 4. Nightly mechanics (mandate Q3)

- **Script:** `scripts/rot_report.py` — read-only Layer-2 validator (ADR-28/36: reads tree + git, writes only gitignored logs). Exits 0 always — an awareness organ like #179, never a gate.
- **Host:** a sibling Windows Task Scheduler task `\DevKnowledge\rot-report`, registered by extending `scripts/setup-fleet-scheduler.ps1`, same posture as fleet-baseline (daily 09:00, `StartWhenAvailable=ON` catch-up, `WakeToRun=OFF`, 15-min cap). Sibling rather than folded into the fleet-baseline action so one job's failure never silences the other. **Arming caveat (RF-2 class):** task registration is per-machine manual state — the SessionStart surfacing below doubles as the armed-check by alarming on a stale report (the `surface_triage` missing-digest pattern).
- **Output:** `logs/ROT-REPORT.md` (human, gitignored — the fleet_health precedent) + `logs/rot-report.json` (machine state for tomorrow's delta). ASCII-only rendering (the cp1252 `cmd_checks` crash is the standing lesson; RF-5).
- **Surfacing:** one SessionStart line, fail-soft: `[rot] 3 new / 11 known / 2 allowed -- logs/ROT-REPORT.md`; silent when zero new; alarms if the report file is >48h old (missed-run / unarmed-task detection).
- **Failure handling:** fail-soft everywhere (git absent → empty extractor; unparseable YAML → skip with a self-report line); missed runs tolerated (catch-up posture, ADR-76).
- **Cost model:** zero LLM, zero network, single-pass text scan — sub-10-seconds on this corpus. No LLM judgment is needed anywhere in v1 because every predicate is an existence check; that is *why* it may run nightly under the ADR-76 "no LLM on the scheduled path" doctrine, and why it does not collide with the §6 sandbox refusals in the 2026-07-04 review ("no nightly" there was about the *episodic LLM harness* — a different mechanism).
- **On-demand mode — the pre-deletion question:** `py scripts/rot_report.py --impact protocols/ESSENTIALS.md` prints the reverse slice *before* a removal: today that answers "ESSENTIALS is referenced by CLAUDE.md (9 sites), PLAYBOOK (15), ARCHITECTURE (5), VISION (4), SESSION_SETUP (8), DEFINITION_OF_DONE, handoff.md, changelog-review.md, conformance-hub.js, 2 manifests, tests… — if removed, ~17 actionable files must update." Same index, zero extra machinery; arguably the single highest-value feature, and the natural doc-side sibling of `safe_remove`'s CLI (run BEFORE cutting).

---

## 5. Report shape (mandate Q4)

Delta-aware, ranked, fully enumerated (no silent caps), flat + fence-safe per the CLAUDE.md §4 render-layer rule:

```
rot-report 2026-07-05 (delta vs 2026-07-04)
NEW (3) -- act or rot-allow:
1. DANGLING-PATH  protocols/SESSION_SETUP.md:42 -> scripts/boot.ps1
   target deleted 2026-06-05 (archive copy: ~/.claude/archive/2026-06-05-machinery-c3/)
   fix: repoint to archive path, or rot-allow if the mention is historical
2. DANGLING-WIRING  .claude/settings.json -> scripts/foo_sentinel.py (organ can never fire)
3. TOMBSTONE  component ruff-gate (removed v1.2.0) still presented live by 2 hub surfaces:
   - templates/child-CLAUDE-roster: "ruff -- lint gate..."
   - PLAYBOOK.md:xxxx
KNOWN (11) -- carried, oldest first ...
ALLOWED (2) -- rot-allow markers in force (enumerated, self-policed for staleness)
AGGREGATED: reconciled_versions 0 mismatch | undeclared_edges 12 candidates (#241 groom pending)
PRUNE-CANDIDATES (informational): 2 checks in-degree 0 (handoff_tag_canonicity, ...) | 4 gotchas untriggered > 90d
```

The one-to-many relation is explicit in every tombstone/impact block: *target → the N sources that must update*. New findings first; knowns don't re-alarm; allow-markers are enumerated and self-policed (a `rot-allow` whose target now exists gets flagged — the `scan_dangling_allow` precedent).

---

## 6. Noise management — the make-or-break

Every awareness organ here lives or dies on precision (one false positive kills adoption — `validate_doc_structure`'s own words). Four inherited defenses:

1. **Actionable-corpus pruning** (#199: proven 245→12 on the undeclared-edge scan — immutable/append-only/gitignored zones are never sources).
2. **Tier-1 verbatim-path matching only in v1** (the highest-precision class; basename/token tiers follow only after live noise data).
3. **Co-located `rot-allow` markers** + archived-annotation recognition.
4. **The #123 value-review:** launch under a findings-acted-on tally; demote to weekly if two weeks surface nothing actioned.

Plus the delta discipline: the headline number is NEW-since-yesterday, never the standing total.

---

## 7. Boundary vs adjacent mechanisms (mandate Q5)

**This is the standing nightly deterministic layer above the commit-time organs — it aggregates and extends, replaces nothing:**

- **vs the coherence spine** — the spine checks *declared* edges at ship-gate; this computes *undeclared existence* edges on a cadence. Complementary; the spine's outputs are aggregated rows.
- **vs #179** — same philosophy (surface, never auto-fix), different target universe: #179 finds missing *declarations* against the spec registry; this finds dangling *references* against the file/organ universe.
- **vs the Informant (`enforcement_coverage.py`)** — the Informant proves organs FIRE on consumers; this proves references RESOLVE on the hub. No overlap; P2 dangling-wiring is upstream of the Informant (an organ whose script is gone will also fail fire_test — this catches it for free, without a clone, every night).
- **vs #244 P2 / ADR-96** — ADR-96 removes *artifacts from consumers*; this propagates removals through *hub prose*. It is the mechanical feed for P4 (sync surfacing) and the discovery instrument for P5 (hub self-prune).
- **vs `safe_remove` / #218** — same question ("who references X before I cut it"), different layer and moment: code-symbol at commit-time there; corpus-file at query-time/nightly here. The X4 wiring extractor delivers a working subset of #218's M2 discovery half; #218's *gate* posture stays commit-time and separate.
- **vs Track A (cloud Routine)** — Track A is the semantic/LLM tier; this is the deterministic tier beneath it. If the operator's continuous-conformance vision is later built, this report's JSON is its input queue (decompose→verdict per finding), per the 2026-07-04 review §5 design notes (binary verdicts + `evidence_command`, n=2 adoption gate).
- **vs the §6 essence-spec-as-oracle (2026-07-04 review)** — §6 extended the manifest into an *engagement* oracle for the episodic sandbox (trigger → expected observable). This design extends the same spec-as-oracle idea along a different axis: the manifest's *lifecycle* field (`status: removed`) becomes the deletion-propagation oracle for hub prose. Same source of truth, two consumers, no duplication.

**Backlog reconciliation:** this design **implements** #169's deterministic staleness-signal-in-daily-digest intent (the reference-existence slice of it) and is the natural **generator for #171** (`ecosystem/conformance.md`) if later promoted from gitignored log to committed dashboard (ADR-80 writer policy) — v1 deliberately starts gitignored to defer the writer-policy question. It **feeds** #244 P4/P5, #130, #212, and RF-8 grooming. It **leaves alone** #218 (gate), #220 (semantic axis), #241 (groom), #132 (full organ-index doc — though X4/X6 share its enumerator and should be built as one walker).

---

## 8. Tradeoffs and refusals

- **No LLM per node** (mandate anti-pattern, agreed): every v1 predicate is deterministic; the semantic tail is a different, separately-gated mechanism.
- **No persistent graph database / no incremental index:** rebuild-per-run; the corpus is small and the rebuild is the correctness guarantee.
- **No transitive-closure alarms:** direct edges only in the report; transitive walks happen on demand in `--impact`. A transitive nightly alarm multiplies noise quadratically.
- **No auto-fix / no auto-declare:** surface-only, human ratifies — the #179 load-bearing rule, unchanged.
- **No new declaration format:** everything here is *computed* from live state (ADR-89's computed-edge doctrine generalized); the only new author-facing token is the optional `rot-allow` suppression marker.
- **Honest limits, stated in the report footer:** prose-mention detection is lexical (a paraphrased reference without the path/name is invisible); semantic claim-drift is out of scope by design; consumer repos are out of scope until P6.
- **Residual risk:** the KNOWN list can silently grow into a tolerated wall — the #123 demotion rule and the disposition/allow discipline are the counterweights, and the weekly review should read the KNOWN count *trend*, not just NEW.

---

## 9. Recommendation + open operator decisions

**Recommendation: build v1 as scoped above — one read-only script, three predicates (P1/P2/P3) + aggregation rows + `--impact` + delta report + `rot-allow`, on a sibling Task Scheduler task, surfaced at SessionStart.** Estimated build: 1–2 sessions, mostly reusing #179's walker/matcher and the existing YAML/config parsers, with fixture-driven tests per predicate (leg-e-style seeded-rot proofs: a seeded dangling path / dead wiring / tombstone reference must each flag). File it as its own BACKLOG item with an ex-ante ADR-81 acceptance contract; the ratifying ADR is the operator's separate step.

Open decisions the operator owns (approved 2026-07-04 on defaults, unremarked):

- **D-A report home:** gitignored `logs/` (default, v1) vs committed `ecosystem/conformance.md` (#171 promotion later).
- **D-B host:** sibling scheduled task (default) vs SessionStart-computed only (cheaper, but couples cadence to session starts and adds latency to an already 5-hook SessionStart).
- **D-C v1 predicate set:** P1+P2+P3 (default) vs also enabling the organ-token tier X6 immediately.
- **D-D prune-candidates appendix** (in-degree-zero organs, dormant gotchas): ships in v1, informational-only (default) vs waits for the P5 hub-self-prune arc.

**Incidental live findings surfaced by this audit (cheap same-day fixes, independent of this design):** the stale P1-era comments in `deploy/manifest-v1.2.0.yaml` (L40-43 "components: … INERT to deploy/tool.py this release (the tool reads only `carriers:`)") and `deploy/release_lint.py`'s docstring ("only `status: active` is legal this release") — both superseded by the P2 remove leg merged 2026-07-04. Honest evidence of the *semantic claim-rot* class that needs the LLM tier rather than this deterministic one.

---

*End of design. Read-only analysis session; this artifact is the session's only repo write (operator-approved landing in `docs/audits/`). Implementation is a separate, later effort behind its own BACKLOG item + ADR.*
