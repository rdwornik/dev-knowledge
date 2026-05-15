# ADR-46 — Cross-repo dated-entries format

<!-- scope: meta -->

Status: Accepted
Date: 2026-05-15
Stream: C, governance ADR session B+C
Supersedes: aspirational "shared format" implied by ADR-29 + ADR-38
Superseded by: none
Related: ADR-27 (scope tagging — HTML comments authoritative),
         ADR-29 (LESSONS schema + grandfathering),
         ADR-33 (VISION universalization — frontmatter precedent),
         ADR-38 (universal repo architecture),
         ADR-41 (BACKLOG architecture),
         ADR-47 (cross-repo BACKLOG organization, paired decision),
         transcripts council-out-20260515_184737-research-...md,
                      council-out-20260515_193228-pick-...md

## Context

Dated-entries files (`LESSONS.md`, `JOURNAL.md`, `CHANGELOG.md`)
have drifted both **across repos** and **within same file** in the
`.dev-knowledge` ecosystem:

- LESSONS.md schema correction at `14f0467` rewrote old body trailers
  to the 6-field canonical format; ordering convention shifted from
  "append at bottom" to "prepend at top" (`99a104e`) without a formal
  ADR
- JOURNAL entries vary on header level (`##` vs `###`); date formats
  vary across repos
- CHANGELOG uses Keep-a-Changelog semantic groupings in `.dev-knowledge`
  but is inconsistent elsewhere
- Audit Tool P1 (2026-05-15) surfaced cross-repo VISION.md frontmatter
  drift: `.dev-knowledge` has 6 keys, `ai-council` has 5 (missing
  `status`)

LLM agents (Claude Code, browser Claude) are co-readers alongside the
single human developer. Format drift degrades LLM token efficiency,
parsing reliability, and cross-repo cognitive load.

Council research (transcript `council-out-20260515_184737-...`)
converged with strong cross-provider agreement (Perplexity + Gemini)
on: ISO dates, `## YYYY-MM-DD` H2 anchors, reverse-chronological
prepend ordering, shared envelope with file-specific payloads. Council
pick (transcript `council-out-20260515_193228-...`) selected
**Option B-1 (Lightweight Hybrid)** under simple-majority rule, with
the synthesizer hardening it via a sniff-test validator strategy.

## Decision

Adopt a **lightweight shared envelope with file-specific payloads** for
LESSONS.md, JOURNAL.md, and CHANGELOG.md across all ecosystem repos.

### Universal envelope (all three files)

- **Date format:** ISO 8601 `YYYY-MM-DD` only. No locale-dependent or
  human-readable variants.
- **Outer heading:** `## YYYY-MM-DD` (H2) as the primary per-day record
  anchor. ISO date MUST appear in the heading text.
- **Inner heading:** `### Topic` (H3) optional, used for per-event
  subdivision within a per-day record. Mandatory when multiple events
  are recorded in one day for the same file.
- **Ordering:** Reverse-chronological. **Prepend-latest is mandatory**
  for all active dated-entries files. New entries are inserted at the
  top of the entry list, directly under the file's intro/frontmatter,
  before existing entries.
- **Scope metadata:** ADR-27 HTML comments (`<!-- scope: X -->`)
  remain the single authoritative source for scope. YAML frontmatter
  is OPTIONAL and, when present, is **additive only** — it MUST NOT
  redeclare `scope`. If conflict, the HTML comment wins.

### File-specific payloads

#### LESSONS.md

- 6-field canonical schema preserved (ADR-29, grandfathered):
  `### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]`
- LESSONS uses single-line entry headings as the per-event record;
  the outer `## YYYY-MM-DD` grouping is OPTIONAL when entries within
  the same day share no logical grouping (matches existing LESSONS
  practice).
- File-level `<!-- scope: hybrid -->` directly under H1 (per ADR-29
  amendment 2026-04-24).

#### JOURNAL.md

- Outer `## YYYY-MM-DD` mandatory per-day record OR `### YYYY-MM-DD —
  <session topic>` (H3) when the file's convention scopes entries to
  per-session rather than per-day (matches existing `.dev-knowledge`
  JOURNAL practice).
- Body: free-prose bullets under topic. No required field schema.

#### CHANGELOG.md

- **Keep-a-Changelog semantics preserved.** `## YYYY-MM-DD` as the
  outer date anchor (or `## [Version] - YYYY-MM-DD` if the repo uses
  semantic versioning).
- Inner `### Added` / `### Changed` / `### Fixed` / `### Deprecated` /
  `### Removed` / `### Security` / `### Verified` / `### Notes` for
  semantic grouping.

### Per-repo flexibility

- Universal envelope is **not** subject to per-repo override.
- File-specific payloads are documented here as **normative** for all
  three files in all M+ tier repos.
- Per-repo deviations from the file-specific payload (e.g., a repo
  needing a 7th LESSONS field) must be ratified by an ADR; silent
  drift is prohibited.

### Archive policy (defined now, tooling deferred)

- **Trigger:** active file > **10,000 tokens** estimated (≈40 KB at the
  4-chars-per-token rule used by ADR-38).
- **Action:** oldest entries rotated to `<file>_archive/` subdirectory
  (e.g., `LESSONS_archive/2026-Q1.md`) keyed by quarter.
- **Tooling:** deferred to a separate session; this ADR mandates the
  trigger but not the implementation.

### Enforcement (Session E scope)

Deterministic, dependency-free Python validator (no AST library, no
new dependencies beyond stdlib) implementing a **sniff-test** strategy:

1. **Frontmatter / HTML comments:** verify ADR-27 scope tag present at
   file head; verify optional YAML frontmatter (if present) does not
   redeclare `scope`.
2. **Outer heading regex:** verify each `## ` heading matches
   `^## \d{4}-\d{2}-\d{2}( |$)` (LESSONS exempted from H2 grouping
   when 6-field single-line entries are used at H3).
3. **Ordering regex:** verify ISO dates in headings are
   reverse-chronological (later dates appear physically earlier).
4. **Sniff test per file:**
   - **LESSONS.md:** verify `[scope:` substring appears in 6-field
     entries (proxy for canonical schema presence).
   - **CHANGELOG.md:** verify at least one recognized semantic
     grouping heading per date section (`### Added` / `### Fixed` /
     etc.).
   - **JOURNAL.md:** no payload sniff (free-prose).

**Stdlib-regex implementation required** for the validator: regex
over line-by-line read with simple fenced-code-block skipping is the
intended implementation. Adding a markdown-AST parsing library (e.g.
`markdown-it-py`, `mistletoe`) requires a **new ADR amendment with
empirical justification** — e.g., the regex pattern has grown to
unmaintainable complexity, or a concrete class of validation cases
cannot be expressed without an AST. Future-proof framing: the
prohibition is on adopting an AST library by default, not on ever
adopting one.

## Rationale

Pick transcript synthesis:

> B-1 is the only option that satisfies the downstream constraints
> while respecting recent structural investments. It provides a stable
> cross-repo envelope for LLMs to anchor on without forcing a rewrite
> of the ecosystem.

Specific drivers:

- **Preserves ADR-29 investment.** The LESSONS 6-field schema was
  grandfathered weeks ago and rewritten across 9 entries on 2026-05-14
  (`14f0467`, `99a104e`). Re-touching grandfathered content for a
  3-field reduction (B-2) would cause "institutional whiplash"
  without justifying value.
- **Preserves CHANGELOG semantic groupings.** Keep-a-Changelog is the
  prior art; abandoning it (B-3) discards a widely-understood
  convention for no payoff.
- **Low-dependency tooling.** Session E validator uses stdlib regex;
  no `python-frontmatter` or `markdown-it-py` dependency — coherent
  with `.dev-knowledge` "minimal deps" posture (current `requirements-dev.txt`
  is `click + pyyaml + pytest + ruff`).
- **Single authoritative metadata source.** ADR-27 HTML comments
  remain the truth-set for scope. Optional YAML is additive only.
  Avoids the split-brain blind spot the synthesizer flagged.
- **Sniff test bounds drift risk.** Validator catches payload-schema
  breakage at session start without parsing markdown AST. 90% of
  drift protection at 10% of complexity.

## Alternatives considered

### Option B-2 — Hybrid AST-Verified (Gemini's research recommendation)

Universal Markdown-KV inside entries; LESSONS reduced to 3-field
(Situation/Action/Result); YAML frontmatter mandatory; AST-based
validator with new dependencies.

**Why not chosen:** Forces a rewrite of grandfathered LESSONS content
weeks after ADR-29 ratification (institutional whiplash); introduces
`python-frontmatter` + `markdown-it-py` dependencies for problems the
ecosystem does not have; the "high 2am cognitive load" of an AST
validator is unjustified for a single maintainer.

### Option B-3 — Strict Universal Schema (Monolith)

Single rigid 3-field schema (Context / Change / Impact) for all three
files; CHANGELOG abandons Keep-a-Changelog.

**Why not chosen:** Discards Keep-a-Changelog semantics for no gain;
forces arbitrary categorisation on JOURNAL entries; high migration
cost; rejected unanimously by the panel.

### Option B-4 — Minimal Envelope Only

ISO date in any heading + reverse-chronological ordering. Per-file
payloads repo-determined.

**Why not chosen:** This is essentially the current state that
produced the observed drift. Underspecification is the root cause.

## Consequences

### Positive

- Stop drift across LESSONS / JOURNAL / CHANGELOG at the envelope
  level immediately on Session D cleanup completion.
- LLM agents can reliably anchor on `## YYYY-MM-DD` H2 across all
  three files in any repo without per-file heuristics.
- Validator stays simple (single Python file, stdlib only).
- LESSONS-6-field and CHANGELOG-Keep-a-Changelog investments
  preserved.

### Negative

- Session D cleanup must touch ~all dated-entries files across the
  ecosystem to normalise outer headers and ordering (large but
  bounded).
- Sniff test is intentionally lax inside payloads — semantic drift in
  LESSONS body bullets or CHANGELOG entry text is not caught.
- Archive tooling deferred — files will grow past 10k tokens before
  rotation is implemented.

### Follow-ups

- **Session D** (cleanup pass): apply this standard to actual files
  across all repos. Normalise outer headers, ordering, scope-tag HTML
  comments. **Bounded** to envelope and headers — payload bodies
  unchanged.
- **Session E** (audit tool extension): implement
  `check_dated_entries_format` in `scripts/audit.py` per the
  enforcement section above. Discovery script over current corpus to
  build edge-case test fixtures.
- **Update CLAUDE.md authoring prompts** so LLM agents generate
  correct payloads for each file type (synthesizer Action Item #2).
- **Archive rotation tooling** — separate session when first file
  approaches 10k token threshold.

## References

- Council research transcript: `docs/decisions/transcripts/council-out-20260515_184737-research-research-brief-cross-repo-dated-entries-format-res.md`
- Council pick transcript: `docs/decisions/transcripts/council-out-20260515_193228-pick-council-pick-cross-repo-dated-entries-format-decis.md`
- ADR-27 (scope tagging architecture — HTML comments authoritative)
- ADR-29 (LESSONS schema + grandfathering)
- ADR-33 (VISION universalization — frontmatter precedent)
- ADR-38 (universal repo architecture — mandatory files per tier)
- ADR-41 (BACKLOG architecture)
- ADR-47 (cross-repo BACKLOG organization — paired decision)
- Keep a Changelog 1.1.0 — https://keepachangelog.com/en/1.1.0/

## Synthesis notes (operator-visible)

Where the pick transcript was ambiguous and this ADR made a judgment
call:

1. **JOURNAL header level** — the transcript settled on `## YYYY-MM-DD`
   universally but did not address `.dev-knowledge` JOURNAL's existing
   convention of `### YYYY-MM-DD — <session topic>` H3 per-session
   entries. This ADR permits both forms to avoid forced rewrite of
   ~30 existing entries; the validator accepts either.
2. **Archive threshold** — synthesizer suggested "e.g., 10k tokens".
   This ADR adopts 10,000 tokens as the literal trigger. May need
   tuning after first file approaches the threshold.
3. **Validator language** — synthesizer said "dependency-free Python
   check"; this ADR sharpens it to **stdlib-regex required**, with
   any future markdown-AST library adoption gated behind an ADR
   amendment carrying empirical justification (e.g., regex
   complexity becomes unmaintainable). Preserves current design
   discipline without painting the ecosystem into a corner.
