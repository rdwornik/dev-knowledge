<!-- scope: meta -->

# Protocols/ Structural Doc-Rot Audit (read-only)

**Date:** 2026-06-03
**Scope:** every `*.md` under `protocols/` except the frozen archive
**Mode:** READ-ONLY. Nothing in any protocol file was edited. This report records the true state and a recommended cleanup order; consolidation is a separate, decision-gated pass.
**Why now:** a strict read of `PLAYBOOK.md` surfaced real structural rot. The freshness gate (`audit.py` check #10) verifies only re-read recency (`last_reviewed` vs last commit) for VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING — it does not look at `protocols/` files at all, and it checks nothing structural. So this rot was invisible to tooling.

---

## Inventory (verified via `wc -l`)

```
protocols/AGENT_FRAMEWORK.md                 48
protocols/AI_COUNCIL_PROCESS.md             416
protocols/ENVIRONMENT.md                    270
protocols/ESSENTIALS.md                     426
protocols/HANDOFF_PROCESS.md                504
protocols/PLAYBOOK.md                      3024
protocols/SESSION_SETUP.md                  233
protocols/archive/HANDOFF_PROCESS_v3.4.md   898   (frozen archive — do-not-edit; excluded)
```

Live protocol corpus (excl. archive): **5,021 lines across 7 files**, of which PLAYBOOK is 60%.

---

## Per-file findings (severity-ranked)

### PLAYBOOK.md — 3024 lines

**HIGH — intra-file duplication with drift: "When a lesson becomes a rule" stated twice.**
- L1687–1690: heuristic trigger — *"If you find yourself writing a lesson that sounds like 'always do X' or 'never do Y' — it might be a rule… add it to `~/.claude/`… with a verify: line."*
- L2318–2321: ontological framing + 3-step process — *"A lesson in LESSONS.md is human context… A rule is machine-executable… When a lesson matures into a rule: (1)… (2)… (3)…"*
- The two give materially different decision models (rhetorical heuristic vs human-vs-machine ontology + procedure). A reader landing on one section forms a different mental model than one landing on the other. (This is also half of the cross-file drift below — ESSENTIALS L393 is a third variant.)

**HIGH — hub-only tooling presented as universal protocol.**
- §18 "Ecosystem Audit Tool Workflow" (L2486 → ~L2780) documents the `.dev-knowledge`-only `scripts/audit.py` CLI: `health`/`run`/`repo`/`registry update` subcommands (L2512–2562), the `ecosystem/` folder + `ecosystem/index.yaml` rollup mechanics (L2578–2656), and child-repo registration bootstrap (L2668–2692). A child repo reading PLAYBOOK as universal protocol has no `audit.py` and no `ecosystem/` — the whole section is non-actionable for them and reads as binding governance.
- L283 "Three pillars, all audit-enforced via `scripts/audit.py`" and L291–292 (ADR-59 exception list "mirrored in the audit tool") similarly bake hub tooling into a section titled as universal repo conventions.

**MED — per-section "Section history" blocks (ADR-49 retired doc-embedded changelogs; git is the record).** Ten blocks: L342, L497, L575, L718, L931, L1085, L1391, L1409, L2008, L2819. L432 even reads *"This section's history is in the Section history blocks + git log… CHANGELOG.md was retired ecosystem-wide per ADR-49"* — i.e. it cites ADR-49 while preserving exactly the doc-embedded mini-changelogs ADR-49's spirit removed. Pattern is also inconsistent: most major sections carry no such block.

**MED — mixed numbering / structure.** Unnumbered foundational sections (System Architecture, Repo conventions, etc.) run to ~L1415, then the doc abruptly switches to numbered §1–§19 (L1416 → L2745), then unnumbered Appendices A/B/C, then loose trailing sections (Codemap workflow, Auto-TOC). A reader cannot rely on the numbered spine.

**LOW — `CHANGELOG.md` cited as a live convention in two spots.** L2125 *"TOKEN-LOG.md and CHANGELOG.md: newest-first (prepend)"* and the L2351 doc-types table row list CHANGELOG as if current, although ~13 other lines in the same file correctly annotate it retired per ADR-49. Internally inconsistent.

Note (positive): PLAYBOOK already self-disambiguates its two internal "Continuous Improvement" uses (L959 tool/model adoption vs L1311 "Distinct from PLAYBOOK Section 6… this covers Claude Code's own extension mechanisms"). The unmanaged collision is with ESSENTIALS (see cross-file).

---

### ESSENTIALS.md — 426 lines

**HIGH — the file violates its own contract.** L3 header: *"Daily cheat sheet. Keep under 1 page."* The file is 426 lines (~4–5 pages). The size discipline it prescribes has been abandoned under additive editing — the clearest single symptom of unmanaged accretion.

**HIGH — summary-fidelity drift vs PLAYBOOK (CLAUDE.md critical rule #6).** L393 condenses lesson→rule to *"When a lesson becomes a rule → write rationale in LESSONS.md, write executable rule in `~/.claude/` with verify: line"* — it drops the *decision trigger* entirely (neither PLAYBOOK's "sounds like always/never" heuristic nor the human-vs-machine test). A reader following ESSENTIALS has no criterion for *when* something is a rule. (Third variant of the cross-file drift.)

**MED — duplicated concept without a canonical pointer.** L99 "Three-layer flow (per ADR-28)" restates PLAYBOOK's System Architecture model in parallel; neither cites the other as canonical, so they can drift independently.

**MED — name collision.** L27 "## Continuous Improvement" (project-evolution posture) reuses the heading PLAYBOOK uses for external tool/model adoption (§6, L959) — a third, unlinked sense of the same heading across the corpus.

**LOW — no frontmatter / `last_reviewed`.** Like all `protocols/` files, ESSENTIALS sits outside the `audit.py` freshness gate (which covers only VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING). Worth noting because it explains why none of this was flagged. (Positive: ESSENTIALS L351 *does* carry the canonical LESSONS format with the `[scope: X]` field — see SESSION_SETUP for the divergent copy.)

---

### HANDOFF_PROCESS.md — 504 lines

**MED — buried claim-reframe.** §5 "File generation principle (critical)" (L195) presents the strong "generated from source" framing, but Amendment v4.3 §A "Architectural claim sharpening" (L409–411) — 200+ lines later — reframes it as *partly aspirational* (deterministic for sacred-file tables; LLM-synthesized for narrative/wisdom/warnings). A reader of §5 never learns of the correction unless they read to the amendments. The body needs a one-line forward pointer.

**MED — amendment bloat / embedded changelog.** L336 "## Section history" + three stacked amendment blocks — v4.2 (L360, items A–G), v4.3 (L405, items A–G), v4.3.1 (L445, items A–E) — occupy ~L336–504, roughly one-third of the file. Justified as decision-amendment practice for a near-immutable process doc, but it is doc-embedded version history (ADR-49 tension) and reuses A–G letters across versions.

Positive: Amendment v4.3.1 §D (L478–480) honestly narrows the `audit.py` check #9 claim from "enforces" to "syntactic — does not detect mis-labeled tags." Good honest-limits practice; not a finding.

---

### AI_COUNCIL_PROCESS.md — 416 lines

**MED — one "Section history" block** (L413), ADR-49-borderline (reads as a version manifest rather than a line-by-line changelog).

Otherwise healthy: clean numbered spine (Purpose → When to convene → Gated loop → Stage 0–6 → Troubleshooting → Cross-references), a single live cross-reference block (L398), no hub-tooling-as-universal content, no stale references found. Heavy `ai-council/` repo detail is appropriate (its audience is Council operators).

---

### ENVIRONMENT.md — 270 lines

**MED — staleness in a living snapshot doc.** Version Tracking table "Last checked" dates are 6–10 weeks stale (Claude Code 2.1.87 / 2026-04-17 at L267; Python 2026-03-28; VS Code 2026-03-29) against a "Last updated: 2026-06-01" header; binding-decisions section carries past-dated items ("GLM-5.1 re-evaluate April 12", L249). Expected drift for an env snapshot, but it is drift.

**MED (by-design caveat) — operator-specific absolute paths.** L143–148 Key Paths and L214 API-keys path embed `C:\Users\1028120\…`. This is *appropriate* for a doc whose explicit purpose is "Dev Environment — Current State" (hub-only, personal snapshot) — it is **not** a universal-doc-carrying-hub-detail hazard the way PLAYBOOK §18 is. Flagged only because it would mislead if ever reused as a template. No frontmatter/`last_reviewed` (outside freshness gate).

---

### SESSION_SETUP.md — 233 lines

**MED — two handoff mechanisms, under-delineated.** Step 4 "Handoff — When the Chat Gets Heavy" (L114–159) describes a browser-chat auto-handoff triggered by typing `wygeneruj handoff` (Claude generates a <100-line block). A separate later section "Handoff workflow trigger" (L178–219) describes the HANDOFF_PROCESS v4 two-phase Claude-Code protocol (`please create handoff for {repo}` / `complete handoff for {repo}`). These serve different layers (browser-to-browser vs Claude Code), but the file never signposts that distinction, so the two can read as competing instructions for the same act.

**MED — divergent LESSONS format.** L169 gives the lesson append format as `### YYYY-MM-DD | [source] | [one-line lesson] | [category] | [action taken]` — **omitting the `[scope: X]` field** that both the canonical `LESSONS.md` header and `ESSENTIALS.md` L351 carry. Stale copy.

**LOW — duplicated decision-routing table** (L105–110) restates the size→venue routing that also lives in PLAYBOOK/ESSENTIALS. Polish-language example phrasings (L37/53/71) are operator-specific but fine as adaptable templates.

---

### AGENT_FRAMEWORK.md — 48 lines

**LOW — healthy stub.** Well-scoped v0.1 stub; honestly surfaces that the enforcement layer is half-built. Minor staleness: L34 says "checks #1–#10 already ship / new check #11+", but `audit.py` now ships 12 checks (#11 `no_sibling_orphans`, #12 `canonical_structure`). No hazards.

---

### archive/HANDOFF_PROCESS_v3.4.md — 898 lines

**N/A — frozen archive.** Marked do-not-edit; excluded from the audit per its archival status.

---

## Cross-file drift (Step 2b — all HIGH)

CLAUDE.md critical rule #6 requires ESSENTIALS to *summarize* PLAYBOOK, not diverge. These are the concepts stated divergently across files — a reader following one file ends up with a different model than one following another:

1. **"Lesson → rule" — three variants, three decision triggers.** ESSENTIALS L393 (no trigger), PLAYBOOK L1687–1690 (rhetorical heuristic "sounds like always/never"), PLAYBOOK L2318–2321 (human-vs-machine ontology + 3-step). Pick one canonical statement; the others point to it.

2. **"Continuous Improvement" — one heading, three scopes.** ESSENTIALS L27 (project-evolution posture) vs PLAYBOOK §6 L959 (external tool/model adoption) vs PLAYBOOK L1311 subsection (Claude Code extension mechanisms). PLAYBOOK self-disambiguates its two; ESSENTIALS adds an unlinked third.

3. **LESSONS entry format — field drift.** Canonical `LESSONS.md` and ESSENTIALS L351 include `| [scope: X] |`; SESSION_SETUP L169 omits it. One format, authored two ways.

4. **Three-layer flow — parallel copies.** ESSENTIALS L99 and PLAYBOOK System Architecture both diagram the model with no canonical-source pointer.

5. **Handoff mechanism — browser vs protocol.** SESSION_SETUP Step 4 (browser `wygeneruj handoff`) vs HANDOFF_PROCESS v4 + SESSION_SETUP's own trigger section, with no explicit "these are different layers" signpost.

---

## Recommended cleanup order (recommendation only — no execution here)

Decision-gated; each item needs the operator's per-finding call before any protocol file is touched.

1. **PLAYBOOK §18 extraction (HIGH, highest leverage).** Move the Ecosystem Audit Tool Workflow + the L283/L291–292 audit-tool specifics out of universal PLAYBOOK into a `.dev-knowledge`-local home (or clearly fence the section "applies to `.dev-knowledge` only"). This is the change most likely to mislead child repos.
2. **Resolve the "lesson → rule" canon (HIGH).** Choose one statement (recommend PLAYBOOK L1687–1690 as the decision trigger), collapse L2318–2321 to a pointer, make ESSENTIALS L393 a one-line cheat-sheet pointer. Same pattern for "Continuous Improvement" naming and the three-layer-flow duplication.
3. **ESSENTIALS re-trim to its contract (HIGH).** Bring it back toward "one page" by replacing inlined PLAYBOOK content with pointers — directly fixes both the size-contract breach and most summary-fidelity drift.
4. **Strip the 10 PLAYBOOK "Section history" blocks + AI_COUNCIL/HANDOFF embedded changelogs (MED).** Replace with a single "history is in git" note; reconcile L2125/L2351 CHANGELOG-as-live mentions.
5. **PLAYBOOK numbering pass (MED).** Decide one scheme (numbered spine + labelled appendices) and apply.
6. **SESSION_SETUP handoff delineation + LESSONS-format fix; HANDOFF body forward-pointer to the v4.3 claim reframe (MED).**
7. **ENVIRONMENT freshness refresh (MED)** and **AGENT_FRAMEWORK check-count fix (LOW)** — small, low-risk.

---

## Tooling gap this audit exposes

`audit.py` checks #1–#12 cover presence, casing, frontmatter schema, mermaid theme, handoff structure, freshness (re-read recency), sibling orphans, and canonical spine headings — **none** look at intra-file duplication, file size/bloat, per-section-changelog accumulation, or cross-file summary fidelity. None of them even target `protocols/` files. That is precisely why this rot accumulated undetected. Captured as a LESSON and a BACKLOG task (doc-rot review machinery, building on ADR-68 + `audit.py`).
