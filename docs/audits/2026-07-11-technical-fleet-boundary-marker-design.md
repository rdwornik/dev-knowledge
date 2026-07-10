# Fleet methodology-boundary marker + CLAUDE.md diff-routine — design (DESIGN-ONLY)
- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-11
- **Source-session:** Lane A worktree `lane-a-312-boundary-design`, branch `design/312-boundary-marker` off `main` @ `e47a2b7`; model Opus 4.8
- **Status:** PROPOSAL-ONLY — design for operator ruling; the build is downstream (#312 child). No mechanism/gate/generator built in this session.

> **Immutable once landed** (ADR-60 `docs/audits/` zone) — supersede with a new file, do not edit in place. NOT an ADR: the ratifying ADR for the chosen marker form is a separate, operator-approved step.
> **Grounding (live reads at HEAD `e47a2b7`):** `docs/audits/2026-07-11-fleet-boundary-matrix.md` (Surface 2 + C1 + Amendment), `docs/decisions/ADR-78-child-methodology-floor.md`, `ADR-93-floor-provisioning-model-a.md`, `ADR-101-hermetization.md` (R3/R4/R5), `ADR-27`/`ADR-48` (withdrawn scope-tags), `scripts/fleet_health.py`, `scripts/audit.py` (`Finding`, `_CANONICAL_SPINE`, `discover_repos`), `.claude/CLAUDE-FLOOR.md` machinery (`templates/child-methodology-floor.md.tmpl`, `deploy/carrier_floor.py`), consumer `CLAUDE.md`/`.gitignore` in ai-council + corp-monorepo (READ-ONLY).
> **Governing principle (operator, immutable — verbatim from #312):** *the hub is the ROOT of a decision tree that traverses repo-by-repo and must classify every surface methodology vs application WITHOUT searching — the boundary must be machine-readable.* This principle **outranks the convenience** of any particular marker form.

---

## 0. Verdict in one paragraph

**Adopt Form A (in-band fenced region markers) for section-level classification, layered on the existing floor (Form B) which stays as it is** — the single-source of the universal *executor contract*. Two complementary machine-readable boundaries result: the floor `@import` line (executor contract, hash-guarded, already shipped) plus fenced `owner=hub` / `owner=repo` regions classifying the 12-section skeleton content the floor does not carry. Together the hub root can classify **every** surface of a child CLAUDE.md by a deterministic parse of that one file — no searching. Form A is chosen over Form C (sidecar manifest) — a genuinely close contender on the literal governing principle — because a classification addressed by section-number in a *separate* file reintroduces exactly the invisible drift the ticket exists to kill (the ADR-27/48 co-location lesson); it is chosen over promoting sections wholesale into the floor (Form B as the section classifier) because §7/§8/§9 interleave repo-specific rosters and §4/§11 are mixed, so wholesale promotion over-claims uniformity and cannot classify the residual skeleton. The diff-routine (§4) is a read-only `fleet_health.py`/`audit.py` sibling that aligns `owner=hub` regions by `id` across repos and reports drift. **Nothing is built here** — this is the design for operator ruling; the region set and the marker form are the operator's to ratify (§6).

---

## 1. Problem

All three fleet repos (hub, ai-council, corp-monorepo) carry the **identical 12-section CLAUDE.md skeleton** verbatim — it is **de-facto methodology**. Yet the only *explicitly-marked, machine-readable* methodology block is the floor `@import` line (ADR-78/93). Which of the 12 sections are methodology vs project is **implicit and hand-maintained per repo**, so:

- There is **no machine-checkable "methodology block"** a hub-rooted traversal can classify without reading and interpreting prose.
- The matrix (Surface 2) dispositioned this **DEFECT** and filed candidate **C1** (this design): a read-only fleet CLAUDE.md diff-routine, whose stated **precondition is an explicit hub-owned boundary marker**.

Witnessed nuance from the matrix (Surface 2 / Surface 9 evidence) that constrains any marker form:
- The audit classifies ai-council's sections as **methodology-derived §1/§6/§7/§8/§9** vs **project §2/§3/§4/§5/§10/§11/§12** — but flags **§4 as *mixed*** (project naming + a hub `.methodology.yaml` bullet) and **§11 as *namespaced*** (project-local + ecosystem ADRs).
- §7/§8/§9 already interleave **repo-specific generated rosters** (`@commands-repo.md`, `@recent-adrs.md`, `@methodology-roster.md`) — the command set itself diverges (hub 4 vs consumers 1; Surface 9). So the section→class mapping is **not clean at section granularity**; some sections are genuinely mixed.

Any marker form must therefore be judged on whether it (a) is machine-readable from the hub root without searching, and (b) can represent a boundary that does **not** fall cleanly on section headings.

## 2. Option matrix (authored independently — see §3 provenance note)

> **Method:** each of three marker forms is scored on five axes with per-cell evidence, **before** the recommendation in §3 is written or the pre-declared lean consulted. Rating scale: **Strong** (clearly satisfies) · **Adequate** (satisfies with a caveat) · **Weak** (material shortfall). The governing principle maps to **Axis 1**; per the operator's ranking, the two *convenience* axes (4 edit-friction, 5 grandfathering) are down-weighted where they conflict with Axes 1–3.

**Forms under evaluation:**
- **Form A — in-band fenced region markers.** HTML-comment delimiters wrapping methodology regions in each CLAUDE.md, e.g. `<!-- methodology:start id=session-protocol owner=hub -->` … `<!-- methodology:end -->`. Precedent: the shipped `<!-- generated by …; do not edit by hand -->` fragment sentinels. Sub-section granularity possible (wrap a paragraph, not only a heading).
- **Form B — floor-import promotion.** Extract the methodology sections (candidate §1/§6/§7/§8/§9) into an `@`-imported, hash-guarded fragment, extending the `@.claude/CLAUDE-FLOOR.md` pattern (ADR-78/93). The `@import` line is the boundary; fragment content is methodology by construction.
- **Form C — sidecar boundary manifest.** A hub-owned structured file, e.g. `.claude/claude-md-boundary.yaml`, mapping `section → {methodology | project | mixed}`. A *gated* successor to the `<!-- scope: X -->` tags whose **enforcement was withdrawn** (ADR-27, ADR-48) — informality + no gate was their failure mode.

```
AXIS                              | Form A: fenced markers        | Form B: floor-import promotion  | Form C: sidecar manifest
                                  |                               |                                 |
1. Hub-traversability WITHOUT     | Strong. Read one known file   | Weak. The @import line cleanly  | Strong. Read ONE structured
   searching (GOVERNING           | (CLAUDE.md), scan delimiter   | marks the PROMOTED subset, but  | file per repo -> class of every
   PRINCIPLE)                     | pairs -> every marked region  | leaves the RESIDUAL skeleton    | section incl. an explicit
                                  | classified; unmarked=project  | (§2/3/4/5/10/11/12) UNmarked -> | `mixed` verdict. Literal match
                                  | by default. Deterministic     | cannot classify "every         | to "classify every surface
                                  | parse, not a corpus grep.     | surface" (§5 hub critical-rules | without searching."
                                  |                               | ARE methodology yet stay out).  |
                                  |                               |                                 |
2. Deterministic parseability     | Adequate. Delimiter-pair      | Strong. The fragment file IS    | Adequate. Trivial YAML parse,
                                  | parse is robust; must handle  | the unit; `@path` + one file,   | BUT the manifest addresses
                                  | unbalanced/nested pairs.      | nothing to interpret.           | sections by number/anchor -> a
                                  | No indirection: marker sits   |                                 | renumber/heading edit silently
                                  | ON the content.               |                                 | mis-maps (indirection risk).
                                  |                               |                                 |
3. Deploy-carrier compatibility   | Adequate. Marker is an        | Strong. EXACTLY the shipped     | Adequate. Sidecar is a hub-
                                  | author-placed CONVENTION the  | floor carrier (`carrier_floor`  | owned whole file (single-writer
                                  | routine READS; the carrier    | writes fragment+sidecar+@import  | OK), but its content is repo-
                                  | need not write into a         | +hash-guard; n=2 rollout).      | specific (§11 project ADRs) ->
                                  | consumer-authored file        | Single-writer-per-file; kills   | hub ships a baseline, consumer
                                  | (avoids the ADR-93 single-    | drift structurally via hash.    | must extend -> partial hub
                                  | writer conflict).             |                                 | ownership.
                                  |                               |                                 |
4. Consumer edit-friction         | Adequate. Keep marker pairs   | Weak. §1/6/7/8/9 relocate out   | Strong (prose) / Adequate
   (convenience — down-weighted)  | intact around sections;       | of the file the consumer reads  | (overall). Prose untouched;
                                  | slight prose clutter.         | inline; §7/8/9 carry repo-      | but a SECOND artifact to keep
                                  |                               | specific rosters that CANNOT go | in sync per edit.
                                  |                               | in a shared fragment.           |
                                  |                               |                                 |
5. Grandfathering cost            | Adequate. One-time hand pass  | Weak. Restructure all 3 files:  | Strong. Add one small sidecar
   (convenience — down-weighted)  | wrapping regions in 3 files;  | extract+re-sequence 5 sections, | per repo (3 files created);
                                  | touches prose, bounded.       | wire @imports, gen hashes — AND | prose untouched.
                                  |                               | the mixed-section promotion is  |
                                  |                               | partially INFEASIBLE.           |
```

### 2.1 Per-axis tally (raw, pre-recommendation)
- **Axis 1 (governing principle):** C ≈ A (both Strong) > B (Weak — incomplete coverage).
- **Axis 2 (determinism):** B (Strong) > A ≈ C (Adequate); C's Adequate is undercut in practice by sidecar indirection.
- **Axis 3 (carrier):** B (Strong) > A ≈ C (Adequate).
- **Axis 4 (friction, down-weighted):** C > A > B.
- **Axis 5 (grandfathering, down-weighted):** C > A > B.

### 2.2 Cross-cutting observations surfaced by the scoring
- **No form dominates.** B owns the carrier/determinism axes but fails the load-bearing Axis 1 (it cannot classify the residual skeleton) and is partly infeasible for the mixed sections.
- **The ADR-27/48 lesson is decisive between A and C.** The withdrawn `<!-- scope: X -->` tags failed on informality + no enforcement; the *deeper* structural risk they expose is **drift between a classification and the content it describes**. Form C's sidecar maximises that distance (classification lives in a separate file addressed by section number) — reintroducing exactly the *invisible drift* the ticket exists to kill. Form A minimises it (classification travels **on** the content).
- **Only Form A represents a non-section-aligned boundary** (wrap a paragraph inside mixed §4). B and C are both section-granular and cannot express `mixed` without extra machinery (C via a third enum value, B not at all).
- **The floor (Form B) is not a rival to A/C for this job** — it already single-sources the *universal executor contract*. The open question is how to classify the *rest* of the de-facto-methodology skeleton, where B does not reach.

## 3. Recommendation + marker spec

> **Provenance (per the Step-1/2 ordering amendment):** the §2 matrix was authored and **committed independently** (commit `63bb7fc`) **before** this recommendation was written; the pre-declared lean was consulted only after. Outcome: the matrix **CONFIRMED** the lean (Form A layered on the floor). It did surface **Form C (sidecar manifest) as a closer contender than the lean anticipated** — C ties Form A as *Strong* on the literal governing principle (Axis 1) and beats it on both convenience axes (4, 5). C is nonetheless rejected on the **ADR-27/48 co-location lesson**: a classification addressed by section-number in a separate file maximises the distance between a claim and the content it describes, reintroducing the *invisible drift* the ticket exists to eliminate. Had the matrix instead shown Form A materially weak on Axis 1 or 3, the recommendation would have changed to C — it did not.

### 3.1 Recommendation
**Form A (in-band fenced region markers) for the section-level methodology/project classification, layered on the existing floor (Form B) — which is unchanged.** Rationale, in governing-principle-first order:
1. **Axis 1 (the principle):** a deterministic parse of one known file (each repo's `CLAUDE.md`) classifies every marked region; unmarked = project by default. No corpus search.
2. **Anti-drift by co-location (the decisive A-vs-C factor):** the classification travels **on** the content, so it cannot silently desynchronise from the prose the way a section-numbered sidecar can — directly answering the operator's "3 months and still invisible" failure.
3. **Represents a non-section-aligned boundary:** a region may wrap a sub-section span, so mixed §4 / namespaced §11 are expressible **without** a third enum value — B and C cannot do this cleanly.
4. **No invasive carrier write:** the marker is an author-placed *convention the routine reads*, so it avoids the ADR-93 single-writer-per-file conflict that region-writing into a consumer-authored file would create.
5. **The floor stays in its proven role:** the universal *executor contract* remains single-sourced + hash-guarded behind `@.claude/CLAUDE-FLOOR.md` (ADR-93); Form A classifies only the *skeleton* methodology the floor does not carry. Two boundaries, complementary, each machine-readable.

### 3.2 Marker spec (exact syntax)
```
<!-- methodology:start id=<kebab-id> owner=<hub|repo> [v=<corpus-version>] -->
… classified content …
<!-- methodology:end id=<kebab-id> -->
```
**Attributes**
- `id` (**required**, kebab-case) — stable region identifier used by the diff-routine to **align regions across repos**. The same `id` in two repos denotes the same methodology region, so it is diffable (e.g. `session-start-protocol`, `critical-rules-universal`, `antipatterns-universal`).
- `owner` (**required**) — `hub`: content is **hub-canonical** (must match the hub baseline for that `id`, modulo declared variables; a mismatch is the DEFECT the routine reports). `repo`: a **project-specific** region the consumer owns (recorded as project; never diffed against the hub).
- `v` (**optional**) — the methodology-corpus version the `owner=hub` block was last synced from (informational; the content diff is authoritative, not `v`).
- The **closing** marker repeats `id` — unambiguous pairing, so a nested/unbalanced pair fails the parse loudly rather than silently mis-scoping (Axis-2 hardening).

**Placement rules**
- Markers are **HTML comments** — invisible in rendered markdown, zero reader friction, and already the repo's sentinel idiom (`<!-- generated by …; do not edit by hand -->`).
- A region wraps **either a whole section** (`## 6. …` through its end) **or a sub-section span** (one paragraph/bullet-group inside a mixed section). This is how `mixed` is represented: mark the methodology spans `owner=hub`; leave the project spans unmarked.
- **Default is project.** Only methodology is affirmatively marked. Unclassified content therefore fails **safe** (treated as project — never a false methodology claim).
- **Hub asymmetry:** the hub `CLAUDE.md` *is* the source — it carries the canonical `owner=hub` regions (the diff baseline) but **no floor `@import`** (it cannot import its own floor). Consumers carry the floor `@import` **and** `owner=hub`/`owner=repo` regions.

**Who marks what**
- The **hub** authors the canonical `owner=hub` regions (the baseline the routine diffs against).
- **Consumers** carry the same `id` + `owner=hub` regions (grandfathered once by hand; a downstream carrier can later sync them — out of scope here) and mark their own sections `owner=repo`.
- The diff-routine aligns by `id`, diffs each `owner=hub` region consumer-vs-hub, and reports drift; `owner=repo` regions are inventoried as project and never diffed.

**Relationship to the floor (no change to the floor)**
- `@.claude/CLAUDE-FLOOR.md` remains the single-source of the universal *executor contract* (session contract, valve discipline, verify cadence, ship rule, context budget, safety) — hash-guarded (ADR-78/93). It is **not** re-marked; the `@import` line is its existing boundary.
- Form A markers classify the **de-facto-methodology skeleton authored in-file** — the content the floor does not carry (session-start protocol, universal critical rules, universal anti-patterns).

**Grandfathering (the one-time cost)**
- A single hand pass over the 3 CLAUDE.md files wrapping the agreed methodology regions in comment markers — bounded, prose-preserving. The **exact region set** is an operator-ruling input (§6), seeded by the §2 Surface-2 section evidence (candidate `owner=hub`: §1, §6, the universal subset of §5, §10; candidate `mixed` needing sub-section marks: §4, §11; candidate `owner=repo`: §2, §3, §12 and the repo-specific roster spans of §7/§8/§9).
