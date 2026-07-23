# ADR-43: Cross-project transcript routing

<!-- scope: meta -->

Status: Accepted — 2026-05-11

## Amendments

- **2026-05-11** — Schema refactor: `target_projects` simplified from `dict[str, str]` to opt-in `list[str]` + single `dev_root` config field. DRY refactor; all ADR-43 invariants preserved. Proposal: `docs/handoffs/_archive/2026-05-11_adr-43-amendment-proposal-schema-refactor.md`. Approval: `docs/handoffs/_archive/2026-05-11_adr-43-amendment-approval-schema-refactor.md`. First live invocation of ADR-43 "Amendment process" rule.

- **2026-07-23 — RE-SCOPE (operator ruling 2026-07-22): routed-mirror clause RETIRED;
  canonical-write production stands.** The hub landing zone
  `.dev-knowledge/docs/decisions/transcripts/` was DELETED 2026-07-22 (`b4435fad`;
  night-batch audit P3a) — council-in-ADR output will never recur; the binding record
  of a decision is its ADR, and git history retains the routed transcripts.
  Consequently the **routed-mirror mechanism of this ADR is retired as fleet
  doctrine**: council transcripts no longer route into any repo's
  `docs/decisions/transcripts/`; `target-project:` / `--target-project` are not to be
  set. A transcript's sole home is the canonical `ai-council/output/`.
  **This is a RE-SCOPE, not a retirement of ADR-43** — the repo-local production in
  ai-council STANDS (canonical-first write to `output/`, fail-loud `RoutingError`
  validation, `TargetResolver`), and this ADR still governs that behaviour plus its
  Amendment process; retiring it wholesale would orphan live ai-council behaviour.
  Unaffected: ai-council's repo-local `transcripts/` (`ai-local-transcripts`,
  parity-surfaces.yaml — a different, product-owned surface). The ADR-77 immutability
  guard on the deleted zone stays ARMED (re-creation refusal); its retirement is a
  separate operator call. **Follow-up (tracked [#401], hub BACKLOG):** ai-council
  removes `.dev-knowledge` from `settings.yaml` `target_projects` (+ its docs); the
  residual mechanism gap — nothing PREVENTS CLI-side re-creation of the deleted zone —
  is declared there as an unenforced clause.

## Context

ai-council generates debate transcripts for architectural decisions
originating from multiple projects across the ecosystem
(.dev-knowledge, corp-monorepo, future repos). Prior state:

- CLI emitted only to canonical `ai-council/output/`
- Cross-project distribution required manual archival
- An always-on `secondary_output_dir` mirror existed in ai-council
  code, statically pointed to `.dev-knowledge` transcript dir —
  partial, legacy implementation of dual-write
- `protocols/ESSENTIALS.md` "Council output convention" claimed
  dual-write was implemented; reality was the always-on `secondary_dir`
  mechanism, not the per-question routing ESSENTIALS implied

Drift signals: ESSENTIALS aspirational text didn't match code
semantics; two projects could disagree on canonical scope; naming
convention drift (legacy `DECISION_27/28/29` artifacts alongside
canonical `council_out_*.md`).

12 existing transcripts in `.dev-knowledge/docs/decisions/transcripts/`
are manual archives from pre-feature era.

Full background in archived delivery report and press-back artifact
(see References).

## Decision

Implement per-invocation, opt-in, config-driven transcript routing
in ai-council CLI:

- **Two-layer model.** Target *names* (e.g., `.dev-knowledge`) are
  dynamic per invocation — supplied via YAML frontmatter `target-project:`
  field (inbox mode) or `--target-project` Click flag (direct CLI mode).
  Target *paths* are computed from `ai-council/config/settings.yaml`: a
  single `dev_root` field declares the ecosystem root; `target_projects`
  is a list of opt-in project names. Resolved path:
  `<dev_root>/<name>/docs/decisions/transcripts/`. No hardcoded paths in
  code; all paths derived from the declared `dev_root`.

- **Single resolver.** Both invocation paths feed the same
  `TargetResolver` instance. No forked resolution logic.

- **Canonical-first, best-effort mirrors.** Canonical write
  (`ai-council/output/`) is always first and required (hard failure
  on error). Target mirrors are best-effort — failure logs warning,
  source of truth never compromised.

- **Fail-loud unknown targets.** Unknown target name raises
  `RoutingError` at parse time (before debate runs), listing all known
  names sorted. No silent fallback.

- **Uniform across all 4 modes** (pick / ideas / judge / research).
  Single plumbing, no per-mode branching.

- **`secondary_output_dir` deprecation.** `secondary_output_enabled`
  default flipped to `false`. Code path retained for explicit-enable
  backwards compatibility; `target_paths` is the canonical routing
  mechanism going forward.

- **No retroactive migration.** 12 existing manual archives in
  `.dev-knowledge/docs/decisions/transcripts/` remain in place.
  Feature applies to new transcripts only.

## Consequences

### Positive

- Deterministic routing — no auto-detection magic
- Audit trail parity between tool-layer and meta-layer (this ADR)
- Multi-project scalable — new repos join via single config entry
- ESSENTIALS convention now matches code reality (drift eliminated)
- Fail-loud at parse time catches config bugs before debate runs
- DRY: ecosystem root declared once, project names listed; no repetition of full paths
- Adding a new repo to routing requires only adding its name to the opt-in list

### Negative

- Per-invocation overhead resolving target paths (trivial)
- Two-mechanism coexistence (`target_paths` + disabled-default
  `secondary_dir`) creates minor cognitive load until `secondary_dir`
  fully removed
- Operator must remember to add new repos to `target_projects` list;
  failure mode is fail-loud (acceptable)
- Assumes all routable projects share a single filesystem root;
  heterogeneous-layout projects would require schema extension if introduced

## Alternatives considered

Five mechanisms surfaced in the original feature request:

1. Hardcoded paths broadcast to all known projects — rejected (noise)
2. CLI flag only — partial (only direct mode)
3. Pull-based: projects pull from canonical — rejected (inverts ownership)
4. YAML frontmatter `target-project:` key — spec preference
5. Auto-detection from cwd/branch — rejected (implicit, error-prone)

Chosen: hybrid of 4 + 2 — frontmatter for inbox mode, CLI flag for
direct mode. Both invocation paths unified via single `TargetResolver`.
Council debate was not formally run; operator accepted the hybrid
directly per "Defer requires justification" (running debate for a
clearly-favored mechanism would have been deferral without information
value). The archived delivery report and press-back artifact serve as
the debate artifact.

## Amendment process

Future ai-council changes affecting routing semantics —
auto-detection introduction, fail-loud behavior changes, `target_paths`
deprecation, `secondary_dir` full removal, new modes affecting routing
— MUST flag back to `.dev-knowledge` browser chat at *design stage*,
before merging in ai-council. ADR-43 amendments live in `.dev-knowledge`;
design conversation must occur in `.dev-knowledge` browser chat before
ai-council implementation.

This extends the three-layer flow (browser chat → .dev-knowledge →
projects) with an explicit feedback edge: projects → .dev-knowledge
for routing-affecting changes. Cross-repo invariant: architectural
decisions affecting `.dev-knowledge`-documented conventions trigger
ADR amendment in `.dev-knowledge`, not silent change in the
implementing project.

## References

- Delivery report: `docs/handoffs/_archive/2026-05-11_ai-council-transcript-routing-delivery.md`
- Press-back: `docs/handoffs/_archive/2026-05-11_dev-knowledge-pressback-adr43.md`
- Feedback response: `docs/handoffs/_archive/2026-05-11_ai-council-feedback-response-adr43.md`
- ai-council implementation: `src/ai_council/routing.py` (`TargetResolver`), `config/settings.yaml` (`target_projects`)
- Related ADRs: ADR-33 (VISION universalization), ADR-34 (file naming), ADR-41 (BACKLOG)
