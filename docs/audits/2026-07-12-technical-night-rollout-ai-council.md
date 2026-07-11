```
# Rollout plan draft — ai-council (methodology v1.3.0)

STATUS: DRAFT — read-only recon output from night-batch agent N2. NOT executed.
For operator morning review only. All findings verified against live repo
state as of 2026-07-11 (not assumed from the task brief's framing).

Hub owner=hub baseline source: .dev-knowledge/CLAUDE.md (v2.35), 8 owner=hub
Form-A regions extracted via grep "methodology:start" + full-file read.
```

## 1. Grandfathering map

### Hub owner=hub regions (8) vs ai-council/CLAUDE.md (169 lines)

- id: first-read | hub span: CLAUDE.md L18-28 (section 1) | ai-council equivalent: section 1, L14-23
  verdict: DIVERGES — item 4 uses pre-v5 handoff phrasing ("Most recent
  handoff under .dev-knowledge/docs/handoffs/ if continuing prior session")
  vs hub's current v5-aware phrasing (start with HANDOFF_BOOT.md, then the
  canonical docs/handoffs/README.md runbook). Otherwise items 1/2/3/5 plus
  the trailing "flag it" line track the hub template closely, with paths
  correctly relativized to `../.dev-knowledge/protocols/...`.

- id: conventions-commit-branch | hub span: L56-59 (section 4 sub-span) | ai-council equivalent: section 4, L40-41
  verdict: DIVERGES — commits line uses
  `type(scope): summary (imperative; body for non-trivial changes)`
  instead of hub's bare `feat/fix/docs/chore/refactor` type list; branches
  line omits the "off main" trailing qualifier hub's line carries.

- id: conventions-output-formatting | hub span: L73-75 (section 4 sub-span) | ai-council equivalent: NONE
  verdict: GAP — no equivalent paragraph anywhere in ai-council CLAUDE.md
  section 4. Fill verbatim from hub baseline at rollout.

- id: critical-rules-records | hub span: L80-84 (section 5 items 1-3) | ai-council equivalent: section 5 items 4-5, L55-56 (PARTIAL)
  verdict: DIVERGES (materially incomplete) — item 4 "LESSONS.md is
  append-only — never edit old entries (ADR-29)" echoes hub rule 1 but
  drops the logs/TOKEN-LOG.md half and the ADR-39 co-citation; item 5
  "ADRs are immutable — supersede with a new ADR; never edit in place"
  echoes hub rule 3 but drops transcripts/handoffs/audits from the
  immutability scope and omits the ADR-94 ratification-exception carve-out
  entirely. Hub rule 2 (JOURNAL.md append-only newest-first) has NO
  equivalent anywhere in ai-council section 5.

- id: critical-rules-consistency | hub span: L87-89 (section 5 item 6) | ai-council equivalent: NONE
  verdict: GAP — no equivalent.

- id: critical-rules-no-leftovers | hub span: L92-94 (section 5 item 9) | ai-council equivalent: NONE
  verdict: GAP — no equivalent anywhere in ai-council CLAUDE.md.

- id: session-start-protocol | hub span: L98-111 (section 6) | ai-council equivalent: section 6, L60-67
  verdict: DIVERGES — missing /boot mention, missing "Check BACKLOG.md for
  in-progress items," missing the "If any check fails -> stop and ask Rob"
  line, missing the trailing "Verify after updates: ESSENTIALS <-> PLAYBOOK..."
  line. ai-council interleaves its own "Run .\scripts\check.ps1 when ready
  to merge" inside the numbered sequence (position 5) — would need to move
  outside a byte-aligned fenced span if the marker wraps the whole list.

- id: antipatterns-universal | hub span: L184-192 (section 10) | ai-council equivalent: section 10 "Do NOT:" sub-list, L127-132 (PARTIAL)
  verdict: DIVERGES — one narrow overlap: "Edit existing LESSONS.md
  entries — append-only per ADR-29" echoes hub's "Editing old LESSONS.md
  or logs/TOKEN-LOG.md entries" bullet but drops the TOKEN-LOG mention.
  Hub's other five bullets (orchestration-scripts Layer-2 invariant,
  AGENTS.md retirement, ESSENTIALS/PLAYBOOK duplication, executable-rules-
  belong-in-~/.claude, validators-need-args) have no ai-council
  equivalent.

### ai-council project-specific sections -> owner=repo candidates
- Section 2 Repo identity
- Section 3 Architecture pointer
- Section 4 non-owner=hub bullets: Naming, Testing, Linting, Out-of-scope
- Section 5 items 1-3,6-7 (repo-local: `.claude/rules/` pointer, API keys,
  `check.ps1`, `config/settings.yaml`, xai/deepseek separation)
- Section 7 Slash commands roster
- Section 8 Skills active roster
- Section 9 Hooks active roster — needs a currency pass alongside the
  pre-commit edit below (prose already names backlog-id-on-close but omits
  block-ff-push and the rev number)
- Section 10 Anti-patterns (repo-local content + the "Do NOT:" list minus
  the one hub-overlap bullet noted above)
- Section 11 Recent ADRs (local ADR-01..08 + ecosystem list)
- Section 12 Section history

## 2. Carried-gates install plan

### Current state (verified live from ai-council/.pre-commit-config.yaml)
- `default_install_hook_types: [pre-commit, commit-msg, pre-push]` already
  declared — arming already correct; this is the #275 leg-a consumer-local
  corrective the hub's own v1.3.x release contract names as "landed on
  ai-council."
- `default_stages: [pre-commit]`
- Local hooks: normalize-headers, floor-hash-verify, canonical_freshness.
- Hub-sourced block: `repo: https://github.com/rdwornik/dev-knowledge`,
  `rev: v1.2.0`, hooks: toc-freshness (files:
  `^protocols/COUNCIL_QUESTION_GUIDE\.md$`), toc-generate,
  backlog-id-on-close.
- Already matches the manifest's canonical `hub_hooks.repo` form (GitHub
  URL) — no repo-field change needed, only a rev bump.
- MISSING only **block-ff-push** — the one genuinely new v1.3.0 hook for
  this consumer; backlog-id-on-close is already wired (adopted at v2.5 of
  ai-council's own CLAUDE.md, per its section-history log).

### Exact edit to .pre-commit-config.yaml — bump rev, add one hook id
```
- repo: https://github.com/rdwornik/dev-knowledge
  rev: v1.3.0
  hooks:
  - id: toc-freshness
    files: ^protocols/COUNCIL_QUESTION_GUIDE\.md$
  - id: toc-generate
    files: ^protocols/COUNCIL_QUESTION_GUIDE\.md$
  - id: backlog-id-on-close
  - id: block-ff-push
```

### Install/verify steps
1. Edit `.pre-commit-config.yaml` as above.
2. `default_install_hook_types` already covers all three stages; run
   `pre-commit install` (bare) to refresh the shims, or explicitly
   `pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push`
   for a belt-and-suspenders re-arm.
3. Update ai-council's own CLAUDE.md section 9 hooks-active prose in the
   same pass — it already documents `backlog-id-on-close (hub-sourced)`
   but doesn't mention `block-ff-push` and doesn't state the rev; this
   section is hand-authored/repo-owned, not generated, so it's a manual
   edit.
4. Locate and bump the recorded `deployed_methodology_version` (ai-council's
   own CLAUDE.md v2.4 history entry records adopting "methodology corpus
   v1.2.0" — find that record, e.g. `ecosystem/state.yaml`) to 1.3.0 once
   deployed.

### Expected firing checks (verify in a disposable/throwaway clone — never against ai-council's real main)
- **block-ff-push**: a direct-to-main push (or FF merge landing a
  non-merge commit on main's first-parent spine) -> expect
  `REFUSED — N non-merge commit(s)...` on stderr, non-zero exit; a
  `--no-ff` merge passes.
- **backlog-id-on-close**: already wired at v1.2.0 — re-verify it still
  fires post-bump (the rev change shouldn't affect behavior, but confirm
  no regression): a commit removing a `- [#id]` line from BACKLOG.md
  without citing it -> blocked with `removed but not referenced`.

## 3. Commands gap

- **/handoff**: ABSENT from `.claude/commands/` (only override.md present).
  Verdict: **intentional absence, not a gap** — same reasoning as
  corp-monorepo. ai-council's own CLAUDE.md section 11 cites "ADR-42:
  handoffs centralized in .dev-knowledge" as ecosystem doctrine binding
  here, and sections 1/6 both already point at `.dev-knowledge/docs/handoffs/`
  as the read location. A local /handoff command would fight that
  centralization. Do NOT deliver.
- **/save**: ABSENT. Verdict: **genuine gap**, same as corp-monorepo —
  generic, repo-agnostic function, no doctrinal blocker. Same delivery
  recommendation: prefer extending a manifest carrier via the
  /override-artifact precedent (`path`/`source` pair, no new carrier type
  needed) over a one-off hand-authored copy, routed through a hub BACKLOG
  follow-up rather than improvised during this rollout.

## Consumer-specific extra: #314 / #315 delta inventory (ai-council)

### #314 — protocols/ as a methodology-mandated genre (hub-pointer vs local-marked split)

Current state, verified:
- `ai-council/protocols/` contains exactly 3 files:
  `COUNCIL_INVOCATION_CONTRACT.md`, `COUNCIL_QUESTION_GUIDE.md`,
  `SYNTHESIS_QUALITY_RUBRIC.md` — confirmed by content (Council-domain:
  invocation lanes/flags, question-writing guide, synthesis scoring
  rubric). These are genuinely "project protocol docs (ai-council Council
  domain)" per #314's own framing — correctly local, and correctly hold NO
  copies of hub methodology protocols (ESSENTIALS.md/PLAYBOOK.md confirmed
  absent from this folder).
- The hub-pointer half is already structurally satisfied: ai-council's
  CLAUDE.md section 1 already points at
  `../.dev-knowledge/protocols/ESSENTIALS.md` and `PLAYBOOK.md` directly,
  never copying them.
- **GAP**: the "marked" half of #314's split is missing — nothing inside
  `ai-council/protocols/` itself documents that the folder is
  intentionally domain-scoped-only, with methodology protocols living at
  the hub by design (today that split exists only in the hub's BACKLOG
  #314 text and in CLAUDE.md section-1 prose, not visibly inside the
  folder a reader lands in first).
- **Delivery plan**: add a short marker — e.g. a `protocols/README.md`
  header note, or a one-line comment at the top of each of the 3 files —
  stating: "Project-local Council-domain protocol docs. Methodology
  protocols (ESSENTIALS.md, PLAYBOOK.md) are hub-pointer only — see
  ../.dev-knowledge/protocols/, never copied here (BACKLOG #314)." Small,
  additive, no restructuring required.
- **Side observation** (not a defect): the hub's own `protocols/` folder is
  broader than just ESSENTIALS/PLAYBOOK — it also holds
  `AGENT_FRAMEWORK.md`, `AI_COUNCIL_PROCESS.md`, `DEFINITION_OF_DONE.md`,
  `ENVIRONMENT.md`, `HANDOFF_BOOT.md`, `HANDOFF_PROCESS.md`,
  `SESSION_SETUP.md`, plus an `archive/` subfolder. Only ESSENTIALS.md and
  PLAYBOOK.md are named in ai-council's CLAUDE.md section 1 as required
  reading. Note the hub's `AI_COUNCIL_PROCESS.md` is a DIFFERENT thing from
  ai-council's local `COUNCIL_*.md` docs — the hub file is ecosystem
  governance (the six-step gated Council process binding ADRs, ADR-67),
  while ai-council's local docs are tool-operational (CLI invocation
  contract, question format, synthesis scoring). Not a conflict, but worth
  the rollout session confirming no content overlap/drift at delivery time
  (line-by-line diff was out of this recon's depth budget).

### #315 — INSTALL.md uniform, hub-owned, deploy-carried

Current state, verified:
- The hub ALREADY has a canonical source:
  `.dev-knowledge/plugins/tier1-lifecycle/INSTALL.md` (referenced by hub
  CLAUDE.md section 8: "full distribution model in ARCHITECTURE.md ... +
  plugins/tier1-lifecycle/INSTALL.md").
- `ai-council/INSTALL.md` (root-level) is a **stale fork** of that
  canonical file, not a synced copy. Diffed directly — ai-council's root
  copy is MISSING, relative to the hub's current version:
  - The "Surfacing is NOT a plugin hook" callout (explains proposal-
    surfacing is a global `~/.claude` SessionStart hook, not a plugin
    hook — a gotcha the hub version documents that ai-council's copy
    predates).
  - The fuller "REQUIRED — gitignore the loop's ephemeral output" section
    (hub version distinguishes repos tracking nothing under `logs/` from
    repos like `.dev-knowledge` that track `logs/TOKEN-LOG.md`;
    ai-council's copy has only a one-line stub: "A logs/ directory will be
    created on first run (gitignore logs/PROPOSALS-*.md).").
  - The ENTIRE "Keeping the plugin up to date" section (a cache-refresh
    workflow table covering plugin-source-changed / new-machine /
    new-repo scenarios) — completely absent from ai-council's copy.
- This confirms ai-council's root INSTALL.md was forked at an earlier hub
  revision and never resynced — exactly the drift #315's "uniform
  fleet-wide, hub-owned" ruling exists to close.
- #315 is **not yet a manifest component** (confirmed: no INSTALL.md entry
  exists anywhere in `deploy/manifest-v1.3.0.yaml`'s carriers or
  components lists) — same "needs a new artifact declaration" shape as
  #280's deferred intake-propagation item.
- **Delivery plan (two-step)**:
  1. Immediate/interim — resync ai-council's root `INSTALL.md` content to
     match the hub's `plugins/tier1-lifecycle/INSTALL.md` verbatim (a
     straight content copy), closing the drift now without waiting on
     manifest work.
  2. Structural — file (or confirm already filed) a hub BACKLOG follow-up
     to add INSTALL.md as a manifest-carried artifact, using the same
     artifact-pair shape already proven for override-command
     (`path: INSTALL.md`, `source: plugins/tier1-lifecycle/INSTALL.md`),
     so future hub-side edits propagate automatically instead of drifting
     again. #315's own BACKLOG text already frames this correctly
     ("becomes a hub-canonical, deploy-manifest-carried file present in
     every onboarded repo, sibling of #280") — nothing new to decide, just
     execute.
- corp-monorepo has NO INSTALL.md at all (confirmed absent from its root
  listing) — consistent with #315's framing ("only the co-authoring repo
  [ai-council] carried a root copy"). Once #315 is manifest-carried,
  corp-monorepo would receive it for the first time too — out of scope for
  this ai-council-only extra, but the same manifest change would serve
  both consumers.

**Delta count**: 2 rulings inventoried (#314, #315); #314 yields 1 concrete
gap (missing "marked" split, small fix) + 1 side observation (no action);
#315 yields 1 concrete drift finding (stale INSTALL.md fork, 3 missing
sections) + a 2-step delivery plan.
