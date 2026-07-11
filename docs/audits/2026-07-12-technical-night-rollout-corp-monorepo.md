```
# Rollout plan draft — corp-monorepo (methodology v1.3.0)

STATUS: DRAFT — read-only recon output from night-batch agent N2. NOT executed.
For operator morning review only. All findings verified against live repo
state and current hub ADR content as of 2026-07-11 (not assumed from the
task brief's framing).

Hub owner=hub baseline source: .dev-knowledge/CLAUDE.md (v2.35), 8 owner=hub
Form-A regions extracted via grep "methodology:start" + full-file read.
```

## 1. Grandfathering map

### Hub owner=hub regions (8) vs corp-monorepo/CLAUDE.md (169 lines)

- id: first-read | hub span: CLAUDE.md L18-28 (section 1) | corp equivalent: section 1, L17-27
  verdict: DIVERGES — corp item 4 uses pre-v5 handoff phrasing ("Most recent
  corp-monorepo handoff bundle in ../.dev-knowledge/docs/handoffs/ if
  continuing prior session (ADR-36 — corp carries no local handoffs dir)")
  vs hub's current v5-aware phrasing (start with HANDOFF_BOOT.md, then the
  canonical docs/handoffs/README.md runbook). Corp ADDS item 6 (`VISION.md`)
  and a trailing "Skip if not applicable — but always read 1-2" line, both
  outside the hub's 5-item template — these must move OUTSIDE the fenced
  owner=hub span if kept (byte-alignment requirement), with the ADR-36
  parenthetical preserved as repo-local color alongside them.

- id: conventions-commit-branch | hub span: L56-59 (section 4 sub-span) | corp equivalent: section 4, L47-48
  verdict: DIVERGES — commit-type tokens differ: corp uses
  `feat:/fix:/docs:/chore:/refactor:/test:` (colon-suffixed, plus an extra
  `test:` type hub's list doesn't declare) vs hub's bare
  `feat/fix/docs/chore/refactor`. Branches line adds "; never commit to
  main directly" (compatible elaboration, redundant with core-invariant #5
  / the block-ff-push gate below).

- id: conventions-output-formatting | hub span: L73-75 (section 4 sub-span) | corp equivalent: NONE
  verdict: GAP — no equivalent paragraph anywhere in corp CLAUDE.md section 4.
  The render-layer box-drawing/fenced-block doctrine is entirely absent.
  Fill verbatim from hub baseline at rollout.

- id: critical-rules-records | hub span: L80-84 (section 5 items 1-3) | corp equivalent: NONE in section 5
  verdict: GAP (major) — corp's 7 numbered section-5 rules are entirely
  local (vault-writer invariant, CKE purity, API keys, OneDrive exclusion,
  test scripts, gotchas check, forward-slashes). None of hub's
  LESSONS/TOKEN-LOG append-only, JOURNAL append-only-newest-first, or
  ADR/transcript/handoff/audit immutability rules appear. A partial,
  out-of-place echo exists only in section 6's session-end prose
  ("Append-only; never edit prior entries" for JOURNAL) — not positioned
  as a section-5 critical rule. Fill verbatim from hub baseline.

- id: critical-rules-consistency | hub span: L87-89 (section 5 item 6) | corp equivalent: NONE
  verdict: GAP — no equivalent. Content describes the hub-owned
  ESSENTIALS/PLAYBOOK relationship; corp doesn't own those files, but
  Form-A byte-alignment still calls for carrying this line verbatim as
  universal doctrine awareness.

- id: critical-rules-no-leftovers | hub span: L92-94 (section 5 item 9) | corp equivalent: NONE
  verdict: GAP — no equivalent anywhere in corp CLAUDE.md.

- id: session-start-protocol | hub span: L98-111 (section 6) | corp equivalent: section 6, L80-93
  verdict: DIVERGES — missing the /boot mention (archived at hub too — note
  as archived rather than omit), missing "Check BACKLOG.md for in-progress
  items," missing the "pytest --collect-only" test-discovery step, missing
  the "If any check fails -> stop and ask Rob" line, missing the trailing
  "Verify after updates: ESSENTIALS <-> PLAYBOOK..." line. Corp interleaves
  its own "Read last 5 entries of JOURNAL.md" as item 4 (duplicates hub's
  own section-1 item 5) plus trailing "Session end:" / "Handoffs:"
  paragraphs that extend past the hub span — must live outside the fenced
  region if kept.

- id: antipatterns-universal | hub span: L184-192 (section 10) | corp equivalent: NONE
  verdict: GAP — corp's section 10 is entirely local (Codex/AGENTS.md
  global-config note, module paths, pip install, CKE staging hierarchy,
  status.json retries, --no-verify bypass warning). None of hub's 6
  universal bullets (orchestration-scripts Layer-2 invariant, AGENTS.md
  retirement, ESSENTIALS/PLAYBOOK duplication, executable-rules-belong-in-
  ~/.claude, validators-need-args, LESSONS/TOKEN-LOG editing) appear.

### Corp-monorepo project-specific sections -> owner=repo candidates
- Section 2 Repo identity (L29-33)
- Section 3 Architecture pointer (L35-42) — note: corp's section 3 carries
  more local content ("Key facts" bullets) than hub's bare pointer-only
  span; still owner=repo, just richer
- Section 4 non-owner=hub bullets: Naming, Testing, Linting, Config,
  Methodology, Engagement, Out-of-scope (L46,49-57)
- Section 5 all 7 corp-local critical rules + the "Graduated learned rules" block
- Section 7 Slash commands roster
- Section 8 Skills active roster
- Section 9 Hooks active roster (currency note: the file's actual
  .pre-commit-config.yaml is MISSING backlog-id-on-close entirely — the
  documented roster doesn't claim it either, so prose and file agree, but
  both are stale relative to the fleet target; see section 2 below)
- Section 10 Anti-patterns (all corp-local)
- Section 11 Recent ADRs (local + ecosystem lists)
- Section 12 Section history

## 2. Carried-gates install plan

### Current state (verified live from corp-monorepo/.pre-commit-config.yaml)
- `default_install_hook_types: [pre-commit, commit-msg, pre-push]` already
  declared at file top — arming mechanism already correct via the existing
  SessionStart hook (`python -m pre_commit install`); no separate arming
  fix needed.
- `default_stages: [pre-commit]`
- Hub-sourced block: `repo: ../.dev-knowledge`, `rev: v1.2.0`, hooks:
  toc-freshness (files: `^ARCHITECTURE\.md$`), toc-generate (manual stage
  only).
- MISSING both v1.3.0 carriers: block-ff-push AND backlog-id-on-close.
  Note: backlog-id-on-close is not new in v1.3.0 (it was already a hub
  marker hook at v1.2.0) — corp simply never adopted it, unlike ai-council
  which did. This is a pre-existing gap the v1.3.0 bump is a good occasion
  to close, not a new v1.3.0-only requirement.
- DIVERGENT repo-reference FORM: corp uses a relative path (`../.dev-knowledge`)
  while manifest-v1.3.0.yaml's `hub_hooks.repo` declares the GitHub URL
  form (`https://github.com/rdwornik/dev-knowledge`) as canonical —
  ai-council's config already matches that manifest form. Corp's config
  also carries a comment block citing a stale pilot-era commit SHA
  (`69558c7`) that no longer matches the live `rev: v1.2.0` tag value —
  the comment itself is stale documentation, separate from the functional
  rev pin. Flag as an explicit decision point for the rollout session, not
  a silent fix.

### Exact edit to .pre-commit-config.yaml

Replace the final block:
```
  - repo: ../.dev-knowledge
    rev: v1.2.0
    hooks:
      - id: toc-freshness
        files: '^ARCHITECTURE\.md$'
      - id: toc-generate  # manual stage only: pre-commit run toc-generate --hook-stage manual
```
with (Option A — recommended: align to the manifest's canonical GitHub-URL
form, matching ai-council and removing the local-path divergence):
```
  - repo: https://github.com/rdwornik/dev-knowledge
    rev: v1.3.0
    hooks:
      - id: toc-freshness
        files: '^ARCHITECTURE\.md$'
      - id: toc-generate  # manual stage only: pre-commit run toc-generate --hook-stage manual
      - id: block-ff-push
      - id: backlog-id-on-close
```
(Option B — keep the existing relative-path pattern, only bump rev + add
the two new hook ids, IF the operator has a specific reason to keep
local-path pinning for corp specifically. Less consistent with both the
manifest and ai-council's own config; recommend A unless B is deliberate.)

Do NOT add codemap-freshness / codemap-generate — corp's existing comment
block explains why (hand-authored codemap; hub generator incompatible with
corp's single-package `src/corp/` layout, 0-edge orphan graph). This
rollout should not disturb that documented exclusion.

### Install/verify steps
1. Edit `.pre-commit-config.yaml` as above (single-writer-per-file).
2. `default_install_hook_types` already covers all three stages — run
   `pre-commit install` (bare, no flags) to refresh the local git-hook
   shims against the edited config; safe/idempotent even if already armed.
   Belt-and-suspenders explicit form if preferred:
   `pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push`
3. Locate and bump the recorded `deployed_methodology_version` (the
   release contract notes "corp-monorepo already records
   deployed_methodology_version: 1.2.0" — find that record, likely under
   `ecosystem/state.yaml` or a repo-local equivalent) to 1.3.0 once
   deployed, or let `deploy/tool.py` do this if the rollout runs through
   the deploy tool rather than a hand-edit.
4. Reconcile corp CLAUDE.md section 9 hooks-active prose in the same pass
   (it currently omits backlog-id-on-close entirely, matching the
   under-provisioned file) — hand-edit, not generated.

### Expected firing checks (verify in a disposable/throwaway clone — never against corp's real main)
- **block-ff-push**: attempt a direct-to-main push (or a fast-forward merge
  landing a non-merge commit on main's first-parent spine) from a
  throwaway clone -> expect `REFUSED — N non-merge commit(s)...` on stderr,
  non-zero exit. A `--no-ff` merge passes clean.
- **backlog-id-on-close**: stage a commit that removes a `- [#id]` line
  from BACKLOG.md without citing that bracketed id in the commit message
  -> expect a block citing `removed but not referenced`. A commit whose
  message includes the bracketed `[#id]` passes.

## 3. Commands gap

- **/handoff**: ABSENT from `.claude/commands/` (only override.md present).
  Verdict: **intentional absence, not a gap.** Corp-monorepo's own CLAUDE.md
  section 6 already documents the correct model: "Handoffs: Generated in
  .dev-knowledge per ADR-62/HANDOFF_PROCESS.md ... NOT in this repo
  (ADR-36 read-only contract)." Delivering a local /handoff command would
  directly contradict ADR-36's read-only-contract doctrine. Do NOT deliver
  /handoff to corp-monorepo. No action needed.
- **/save**: ABSENT. Verdict: **genuine gap**, no doctrinal blocker — /save's
  function (stage + commit with a Conventional Commits message) is generic
  and repo-agnostic, unlike /handoff. Delivery options: (a) hand-author a
  repo-local `.claude/commands/save.md` now (fastest, but reintroduces a
  hand-sync surface); (b) extend a manifest carrier to ship it as a new
  file artifact, following the exact precedent already proven for
  /override (the enforcement-mesh carrier ships `.claude/commands/override.md`
  via a `path`/`source` artifact pair — no new carrier TYPE is needed, just
  a new artifact entry). Recommend routing via a hub BACKLOG follow-up
  (sibling framing to #280's carrier-gap) rather than improvising a local
  copy during this rollout.

## Consumer-specific extra: D4 staleness inventory (corp-monorepo/ARCHITECTURE.md)

Scope per task brief: ADR-30, ADR-31, ADR-38, ADR-53, ADR-54 references
only. Every citation verified against the CURRENT hub ADR file content
(read in full, not assumed stale from the brief's framing). Mermaid/diagram
dimension explicitly out of scope per instructions.

**ADR-30** (default-branch-main): NOT REFERENCED anywhere in
ARCHITECTURE.md (confirmed via targeted grep, zero hits). No stale
citation exists to fix — this is an absence, not staleness.

**ADR-31** (Authority Model) — `corp-monorepo/ARCHITECTURE.md:568`:
"corp-monorepo is a **product/code repo** governed by `.dev-knowledge`
(Layer-2 binding authority, ADR-31)."
STALE/IMPRECISE. The "Layer-2" numbering is not ADR-31's content — it
belongs to ADR-28 (Three-Layer Architecture; ADR-28's Decision explicitly
sets "Execution is one-way (Layer 2 -> Layer 3)", and the hub's own
CLAUDE.md self-identifies as "Layer 2 of the ADR-28 three-layer ecosystem
model"). ADR-31 itself defines the AUTHORITY/conformance-audit model
("1B: Prescriptive with conformance audit"), not layer numbering.
Confirmed internally inconsistent within the SAME file:
`ARCHITECTURE.md:570`, two lines later, correctly attributes the identical
"Layer-2" concept to ADR-28 ("`.dev-knowledge` never writes here (Layer-2
invariant, ADR-28)").
Should now say: split the citation so each ADR is credited for what it
actually decided, e.g. "governed by `.dev-knowledge` (Layer-2, ADR-28;
binding authority via conformance audit, ADR-31)".

**ADR-38** (Universal Repo Architecture Baseline) —
`corp-monorepo/ARCHITECTURE.md:558,568,581,588`: VERIFIED CURRENT, not
stale. Line 558's namespace claim (`src/corp/`) still matches ADR-38's
original Decision, explicitly preserved by the A5 amendment's carve-out
("[code-structure requirements] remain ... the convention for code
projects"). Lines 568/581/588's "A6 seven-file canonical baseline"
citations correctly name the LATEST amendment (A6, 2026-06-02) and match
present reality — both ai-council and corp-monorepo currently carry all
seven canonical files (VISION/ARCHITECTURE/CLAUDE/BACKLOG/CONTRIBUTING/
JOURNAL/LESSONS, confirmed via directory listing). Not superseded by the
newer ADR-101 (Hermetization, ratified 2026-07-10) — that ADR is
explicitly scoped to hub-only top-level-directory sealing +
`docs/audits/` filename grammar ("child-repo propagation ... hub-only,
n=1 ... until a P6 rollout"), a disjoint concern from the seven-canonical-
file doctrine. No fix needed.

**ADR-53** (CLAUDE.md single instruction file) —
`corp-monorepo/ARCHITECTURE.md:588`: "ADR-53 (CLAUDE.md)". VERIFIED
CURRENT. ADR-53 is Accepted, carries no amendments, and its decision
(CLAUDE.md as the single canonical per-repo agent-instruction file) is
unchanged. No fix needed. (Side note, not a fix: the LIVE rollout this
recon is staging — Form-A boundary markers inside CLAUDE.md — is a new
structural layer on top of ADR-53's doctrine, tracked by the #312 BACKLOG
design, not yet itself a ratified ADR superseding ADR-53; nothing in
ARCHITECTURE.md needs to change for that yet.)

**ADR-54** (Codex Reviewer Global Standard): NOT REFERENCED in
ARCHITECTURE.md (it does appear in corp-monorepo's CLAUDE.md section 10 —
"ADR-54" for the global Codex reviewer config note — but that file is out
of this ARCHITECTURE.md-scoped inventory per the task brief). No stale
citation exists within ARCHITECTURE.md to fix.

**Net finding**: 1 genuinely stale/imprecise reference found (ADR-31 at
line 568), not 5. ADR-30 and ADR-54 are simply absent from the file (no
citation to correct); ADR-38 and ADR-53 check out as accurate against
current hub ADR content. Reporting this honestly rather than manufacturing
additional findings the evidence doesn't support — the task brief's framing
("these hub ADRs have moved on") holds for one of the five, not all five.
