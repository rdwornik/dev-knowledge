# [#433] schema-spike verification — K1–K5 referents, round-trip proof, viewer pilot

**Date:** 2026-07-27 · **Arc:** [#433] spike + restructure strangler STEP 1–2 (verbatim split + byte-stable round-trip), branch `feat/433-schema-spike-split`, base `feb95e18`
**Method:** module 1 records the K-criteria referents (this section is the module-1 commit); modules 2–3 build the deterministic splitter/emitter + byte-identity round-trip and the derived `tasks/` tree; module 4 pilots the Backlog.md viewer against the real tree; module 5 completes this report with verdicts, the swap-out contract, and the [#382] schema findings.
**Not ruled here:** VIEWER ADOPT/REJECT below is labelled as **evidence** — the ruling stays with the restructure ADR ([#433] Done-when). BACKLOG.md remains the source of truth this arc; the `tasks/` tree is DERIVED (the flip is a later, separate arc).

---

## 1. K-criteria definitions (module 1 — the undefined-terms flag, cleared)

[#433] records: the K1–K5 validation spike is "operator's term, undefined in-repo — the spike records it first." The referents are defined here, **verbatim from the operator paste of 2026-07-27** (the arc's authorizing order):

> K1 viewer operates over/beside our files WITHOUT forcing its folder taxonomy
>    (its tree confinable to a path we choose, or absent)
> K2 [#N] identity survives byte-exact -- no task-N rewrite, no renumbering
> K3 foreign frontmatter keys (serialize-group, verified_by) survive its read
>    AND write byte-stable
> K4 works on Windows (the fleet's actual host)
> K5 read surface scriptable (JSON/CLI) consumable without importing its code

And the sixth criterion, **SCHEMA COMPOSABILITY** (provenance: operator-ratified S3d, 2026-07-26):

> a task record must be expressible as one typed row inside a declared desired-
> state model -- identity, status, dependencies surviving as fields among others
> -- without requiring its own parallel store.

**Placement disposition (recorded, not silent):** the paste directs these definitions into "[#433]'s spike scope (and docs/audits report later)" under the 1200-char ceiling, with overflow to this report. The [#433] BACKLOG entry sits at **1189/1200** doc_rot chars (11 chars of headroom) and the arc's frozen acceptance contract requires `git diff` on BACKLOG.md to be **empty** this arc — so per the paste's ceiling clause the definitions overflow **entirely** to this report, cross-linked: this section is the in-repo record; the [#433] entry's own text ("the spike records it first") is the standing forward pointer to it. No BACKLOG edit was made.

**Cross-references:** [#433] (carrier), [#382] (receiver of the schema findings per the pilot-precedes-contract ruling, `docs/decisions/README.md` "Restructure pilots the pattern before the fleet contract", operator ruling 2026-07-26, obligation 1), SUPPLEMENT `docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §2(c) (frozen bake-off criteria: `[#N]` preserved exactly · frontmatter extensible with serialize-group / verified_by / Fibonacci scoring · dependency graph · Windows · agent integration · maintenance risk · license).

## 2. Round-trip proof (modules 2–3) — PENDING at module 1

*(Filled by module 5: splitter/emitter design, the byte-identity round-trip test, and the committed-tree coherence result.)*

## 3. Viewer spike — K1–K5 verdicts + evidence (module 4) — PENDING at module 1

*(Filled by module 5: pinned viewer version, per-criterion PASS/FAIL with verbatim command + output evidence.)*

## 4. Swap-out contract (module 5) — PENDING at module 1

*(Filled by module 5: what the gate must pin, how the viewer is replaced.)*

## 5. Schema findings owed to [#382] (pilot-ruling obligation 1) — PENDING at module 1

*(Filled by module 5.)*

## 6. Review lanes (terra) — PENDING at module 1

*(Filled by module 5: terra CODE + DOC lane findings and dispositions.)*
