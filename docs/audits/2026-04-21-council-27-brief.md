# Council #27 Brief — LLM Practice Ecosystem Architecture

> Prepared: 2026-04-21
> Inputs: [Phase 1 inventory](./2026-04-21-dev-knowledge-inventory.md), [Phase 2 scope tagging](./2026-04-21-dev-knowledge-scope-tagging.md)
> Scope: architecture options only. Neutral framing. Council decides.

---

## Problem Statement

`.dev-knowledge/` began as a single-domain knowledge base for Rob's dev methodology: 22 markdown files, 2311 lines, anchored by PLAYBOOK.md (757 lines, 20 sections). Phase 2 tagging reveals scope has drifted: only 14% of sections are cleanly `[dev]`, while 22% are cleanly `[llm]` (universal prompting, Council debates, model routing, token techniques, handoff taxonomy). Another 21% are `[hybrid]` — inseparably coupled dev and LLM content within single sections.

**Cost of no decision:** scope drift continues invisibly; new LLM-practice material (e.g. presales prompt library) has no home and will either pollute `.dev-knowledge/` further or get written in the wrong place; PLAYBOOK becomes harder to navigate as hybrid sections compound; onboarding confusion ("what is this repo for?") grows with each addition.

**Cost of too-early decision:** premature split duplicates 35% meta overhead (README, CLAUDE.md, governance) across two repos with uncertain non-dev demand; may rebuild structure for a single hypothetical consumer.

---

## Audit Findings (summary)

- **Scale:** 22 tracked files, 2311 lines, ~111 KB. PLAYBOOK dominates at 33 KB (30% of bytes, 33% of lines). — *[Phase 1 §Size](./2026-04-21-dev-knowledge-inventory.md)*
- **Section census:** 63 sections analyzed across 8 primary files. — *[Phase 2 §Summary](./2026-04-21-dev-knowledge-scope-tagging.md)*
- **Cleanly `[llm]`:** 14 sections (22%). 13 listed as directly portable to a non-code repo. — *[Phase 2 §Candidates for extraction](./2026-04-21-dev-knowledge-scope-tagging.md)*
- **Cleanly `[dev]`:** 9 sections (14%) — fewer than `[llm]`. The repo is no longer majority-dev by section count.
- **`[hybrid]` (13 sections, 21%):** require Council decision. 7 of 13 (54%) live in PLAYBOOK; the remaining 6 span ESSENTIALS (4), SESSION_SETUP (1), LESSONS (1).
- **Dominant hybrid pattern:** 7/13 hybrid sections follow "universal structure + dev-specific examples" (e.g. S2 universal Model/Mode/Effort routing wrapped around dev git/pytest workflow; S7 universal /compact mixed with git-commit-after-each-change; S9 universal /evolve interleaved with pytest & ruff). — *[Phase 2 §Hybrid sections](./2026-04-21-dev-knowledge-scope-tagging.md)*
- **`[meta]`:** 22 sections (35%). Largest bucket. Governance, triage rules, file indexes, Council decision log. Any split duplicates this overhead.
- **`[runtime]`:** 5 sections (8%). Claude Code shortcuts, skills, hooks — already conceptually separate and arguably belongs in `~/.claude/` rather than either architecture option.
- **LESSONS.md constraint:** single append-only log (123 lines). Entries span `prompt-craft`, `token-optimization` (`[llm]`), `gotcha`, `architecture` (`[dev]`), `process`, `tooling` (both). **Cannot be retroactively split without violating no-edit rule.**
- **Activity signal:** top-4 most-modified in 30 days = ESSENTIALS (10), PLAYBOOK (8), LESSONS (5), HANDOFF_PROCESS (3) — precisely the files with the highest hybrid density. Decision affects the hot path.

---

## Design Options

### Option A: Single Repo with Section Tagging

**Description:** keep `.dev-knowledge/` as one repo. Add YAML frontmatter `scope:` tag per section (or per file where sections are uniform) using the Phase 2 taxonomy (`dev | llm | hybrid | runtime | meta`). Consumers (Claude Code, browser chats, future non-dev readers) filter by tag at read time.

**Architecture:**
```
.dev-knowledge/                     [one repo, unchanged location]
├── PLAYBOOK.md                     [sections annotated: scope: dev|llm|hybrid]
├── ESSENTIALS.md                   [sections annotated]
├── LESSONS.md                      [entries tagged inline per line]
├── HANDOFF_PROCESS.md              [sections annotated]
├── ... (all 22 files retain location)
└── .filter-manifest.yaml           [optional: view presets — "llm-only", "dev-only"]

Consumer flow:
  browser chat wants llm-only → reads sections where scope includes {llm, hybrid}
  Claude Code session on code → reads everything (dev is implicit)
```

**Migration cost:**
- **Time:** 4–6 hours. One pass to add frontmatter to 8 primary files (~63 sections). Optional `.filter-manifest.yaml` adds 1 hour.
- **Risk:** low. Non-destructive. Reversible by stripping frontmatter.
- **Steps:**
  1. Add `scope:` YAML to each section header (use Phase 2 tags as source of truth).
  2. Write `.filter-manifest.yaml` mapping tag combos to "views" (optional).
  3. Update CLAUDE.md to document tag vocabulary and consumer filter protocol.
  4. Update upload protocol in ESSENTIALS/SESSION_SETUP: "for functional chat, filter by `scope: llm|hybrid|meta`."

**Pros:**
- Zero new infrastructure, zero new repos.
- Zero duplicated meta — the 35% stays in one place.
- Incremental: can tag one file at a time without breaking anything.
- LESSONS.md stays single and append-only (tag per entry line — compatible with no-edit rule going forward).
- Reversible: if split later proves right, tags pre-classify the content for free.

**Cons:**
- Scope confusion remains in one folder — the `.dev-knowledge/` name still reads as "dev-only" to non-dev consumers.
- Tag hygiene requires discipline; a stale or missing tag poisons the filter.
- Consumers carry filter overhead (browser uploads need per-file preprocessing, or manual selection).
- Does not resolve the 7/13 "universal + dev examples" pattern — hybrid sections stay intermingled.

**Best for:** if dev and LLM work are expected to keep cross-pollinating and the boundary is genuinely fluid; if non-dev consumer demand is hypothetical rather than concrete.

---

### Option B: Two Repos with Shared Core

**Description:** split into `llm-practice/` (new repo, dev-agnostic) and `.dev-knowledge/` (refactored, dev-only). Extract `[llm]` sections. Hybrid sections stay in `.dev-knowledge/` (dev examples are load-bearing). `[runtime]` moves to `~/.claude/` (already its conceptual home). A thin `shared-core/` (submodule or symlink) holds primitives referenced by both — e.g. Model/Mode/Effort spec, handoff section schema, lesson-extraction protocol.

**Architecture:**
```
llm-practice/                       [new repo]
├── README.md                       [new]
├── CLAUDE.md                       [new — LLM-practice context]
├── PROMPT_BASICS.md                [from PLAYBOOK S2 universal portion]
├── COUNCIL_DEBATE.md               [from PLAYBOOK S5]
├── MODEL_ROUTING.md                [from PLAYBOOK AppB]
├── TOKEN_TECHNIQUES.md             [from PLAYBOOK AppC]
├── SESSION_MANAGEMENT.md           [from SESSION_SETUP + ESSENTIALS Managing Tokens]
├── HANDOFF_B.md                    [from HANDOFF_PROCESS Typ B + Required Sections]
├── LESSON_EXTRACTION.md            [from PLAYBOOK S4]
└── LLM_LESSONS.md                  [new, forward-only; LESSONS.md grandfathered]

.dev-knowledge/                     [refactored]
├── PLAYBOOK.md                     [dev sections + hybrid sections retained]
├── ESSENTIALS.md                   [dev-view cheat sheet]
├── LESSONS.md                      [original, unchanged — append-only grandfathered]
├── HANDOFF_PROCESS.md              [Typ A retained; Typ B → llm-practice]
├── ENVIRONMENT.md                  [dev-tooling portions; LLM portions → shared or llm-practice]
└── ... (meta/runtime governance as before)

shared-core/                        [symlink or git submodule, referenced by both]
├── model-mode-effort-spec.md
├── handoff-section-schema.md
└── lesson-categories.md
```

**Migration cost:**
- **Time:** 1 working week (incremental, can be sprint-shaped). Split PLAYBOOK (~1 day), create llm-practice repo and seed (~1 day), set up shared-core (~0.5 day), rewire links across files (~1 day), update upload protocols and ESSENTIALS ×2 (~1 day), verification (~0.5 day).
- **Risk:** medium. Link breakage across repos if shared-core primitive moves. Consumer protocols (browser chat uploads, Claude Code context) need updates in multiple places.
- **Steps:**
  1. Create `llm-practice/` repo with README + CLAUDE.md.
  2. Extract 13 cleanly-`[llm]` sections (Phase 2 list) to separate files under `llm-practice/`.
  3. Set up `shared-core/` as submodule or symlink; move extracted primitives.
  4. Rewrite hybrid sections in `.dev-knowledge/` to reference `shared-core/` for universal parts.
  5. Grandfather LESSONS.md as-is; start `llm-practice/LLM_LESSONS.md` for future LLM-only lessons.
  6. Update ESSENTIALS / SESSION_SETUP / CLAUDE.md with new upload protocols per consumer type.
  7. Verify: 22 file-count baseline → expected ~15 in `.dev-knowledge/` + ~9 in `llm-practice/` + ~3 in `shared-core/`.

**Pros:**
- Clean scope separation — each repo has one purpose and an obvious name.
- Independent evolution cadence: LLM practice can iterate without touching dev repo (or vice versa).
- LLM-practice repo is shareable / consumable by non-dev contexts (presales prompt work, research workflows) without dragging dev governance along.
- Reduces cognitive load per file (ESSENTIALS for dev ≠ ESSENTIALS for LLM).

**Cons:**
- **Duplicated meta overhead** — two READMEs, two CLAUDE.md files, two governance sections. 35% of current content partially duplicates.
- Cross-repo linking fragility (especially if shared-core is a submodule; symlinks have Windows quirks).
- `shared-core/` adds a third thing to understand — three-repo mental model.
- Hybrid sections remain un-refactored (they stay in `.dev-knowledge/` as-is) — does not address 7/13 pattern.
- Speculative: non-dev consumer currently hypothetical.

**Best for:** if LLM practice has (or is imminently expected to have) clearly distinct non-dev consumers — presales prompt library, research chat templates — and dev-knowledge can credibly narrow to dev-only.

---

### Option C: Base + Extension Pattern (Hub and Spoke)

**Description:** `llm-practice/` becomes the **base layer** (universal LLM work — domain-agnostic). `.dev-knowledge/` becomes an **extension overlay** (dev-specific additions layered on top of base). Consumers load base, then optionally load an extension. Pattern analog: Tailwind `extends`, Obsidian plugins, VS Code settings cascade. The 7/13 "universal structure + dev examples" hybrid pattern becomes the architectural home case: base defines structure, extension adds domain examples.

**Architecture:**
```
llm-practice/                       [base layer — universal]
├── PROMPT_FORMAT.md                [Model/Mode/Effort + universal prompt structure]
├── SESSION_PROTOCOL.md             [/clear, /compact, Plan Mode, token hygiene]
├── COUNCIL_DEBATE.md               [multi-model orchestration, ADR format]
├── HANDOFF_TYPES.md                [A/B/C taxonomy — types only, not domain-specific steps]
├── LESSON_EXTRACTION.md            [universal end-of-session protocol]
├── WEEKLY_REVIEW.md                [universal hygiene pass]
└── ANTI_PATTERNS.md                [universal commandments — date things, scope is sacred, verify]

.dev-knowledge/                     [extension overlay — dev-specific additions]
├── extends: llm-practice           [declared in CLAUDE.md]
├── extensions/prompt-format-dev.md         [adds git workflow, pytest, ruff, CLAUDE.md to PROMPT_FORMAT]
├── extensions/session-protocol-dev.md      [adds git-commit-per-step, pytest-per-step to SESSION_PROTOCOL]
├── extensions/handoff-typ-a-dev.md         [Typ A programming handoff steps on top of HANDOFF_TYPES]
├── extensions/weekly-review-dev.md         [adds test suite, lint, stale branches to WEEKLY_REVIEW]
├── extensions/anti-patterns-dev.md         [adds commandments #3 #5 #9 to universal list]
├── PROJECT_TIERS.md                        [pure dev — PLAYBOOK S0, S1, S11, S13, S15, S16]
├── CODE_REVIEW.md                          [pure dev — PLAYBOOK S6]
└── LESSONS_DEV.md                          [new, dev-only forward-looking; LESSONS.md grandfathered]

Consumer flow:
  dev session: load llm-practice + .dev-knowledge extension
  presales/research: load llm-practice only
  (an overlay loader concatenates base section + extension addendum at read time)
```

**Migration cost:**
- **Time:** 2–3 weeks. Requires rewriting 7 PLAYBOOK hybrid sections as base + overlay, plus extracting 13 `[llm]` sections, plus designing the overlay convention, plus consumer tooling (loader or read protocol).
- **Risk:** high. Unusual pattern for markdown — likely no off-the-shelf loader; overlay hygiene depends on convention enforcement; "is this base or extension?" becomes a decision per new content.
- **Steps:**
  1. Design overlay convention: how does an extension file declare "I extend base section X"? (e.g. YAML header `extends: llm-practice/PROMPT_FORMAT.md#section-3`).
  2. Create `llm-practice/` base from 13 cleanly-`[llm]` sections + the **universal-structure portions** extracted from 7 hybrid PLAYBOOK sections.
  3. For each of 7 hybrid sections: write dev-specific extension file that layers examples onto base.
  4. Create `.dev-knowledge/` pure-dev files (S0, S1, S6, S11, S13, S15, S16) as non-extension content.
  5. Build or adopt a consumer loader (for browser chats: a copy-paste helper that concatenates base + extension; for Claude Code: documented read order).
  6. Grandfather LESSONS.md; new lessons go to `LESSONS_LLM.md` (base) or `LESSONS_DEV.md` (extension).
  7. Rewrite ESSENTIALS as two cheat sheets (base + dev extension) or one that demonstrates the overlay.
  8. Verify: overlay loader produces output equivalent to current PLAYBOOK sections for 7 hybrid cases.

**Pros:**
- Maximally DRY — universal structure defined once, domain examples live alongside.
- Architectural home for the 7/13 hybrid pattern (the largest single class of ambiguous content).
- Natural future extensibility: `presales/` or `research/` extensions reuse the same base with zero duplication.
- Forces a clean separation that makes future content decisions mechanical ("is this structure or example?").

**Cons:**
- **Highest upfront cost** by 3–4x over Option B.
- Requires custom overlay convention — no standard tooling for markdown-with-overlays.
- Two-layer mental model raises onboarding difficulty.
- Over-engineering risk if non-dev demand never materializes — pays the cost for hypothetical overlays.
- Rewrites 7 hybrid sections: content change, not just reorganization. Higher regression risk on battle-tested text.

**Best for:** long-term play. Justified only if (a) LLM practice as a base will genuinely have multiple overlays (dev, presales, research, +) and (b) the 7/13 universal-structure-with-examples pattern is believed to generalize — same skeleton, new domain meat.

---

## Decision Matrix

Scores 1–10 (higher = better). Weights are a proposal; Council may renegotiate.

| Criterion | Weight | A | B | C |
|-----------|--------|---|---|---|
| Migration cost (lower is better, so scored inversely) | 30% | 9 | 6 | 3 |
| Scope clarity (names match contents) | 25% | 4 | 8 | 9 |
| Future flexibility (accommodates new consumers) | 20% | 5 | 7 | 10 |
| Maintenance overhead (lower is better, scored inversely) | 15% | 7 | 5 | 6 |
| Onboarding simplicity | 10% | 8 | 6 | 4 |
| **Weighted score** | 100% | **6.55** | **6.55** | **6.10** |

**Observation:** A and B tie at current weights. The tie collapses the moment Council re-weights "Scope clarity" up (B wins) or "Migration cost" up (A wins). C only wins if **Future flexibility is weighted ≥35%** — i.e. Council is betting that multiple non-dev overlays will exist within 12 months.

---

## Open Questions for Council

1. **Is there a concrete non-dev consumer today, or is LLM practice still dev-adjacent in reality?** The only mentioned candidate is a presales prompt library — is that work planned, or hypothetical?
2. **Is the 7/13 "universal structure + dev-specific examples" pattern generative?** If yes → C becomes defensible. If it's just how current content happened to be written → C is premature.
3. **LESSONS.md disposition:** grandfather as dev-only (simpler, some lessons misclassified), or tag retroactively per entry (respects append-only by adding only a tag column, not editing content)?
4. **Meta overhead (35%, 22 sections):** accept duplication across repos (B, C), or keep single governance (A)? What's the marginal cost of maintaining two CLAUDE.md + README sets?
5. **Acceptable migration timeline:** one sprint (forces A), one month (A or B), one quarter (any)? How much disruption is acceptable to `.dev-knowledge/` given it's the hottest file set (ESSENTIALS/PLAYBOOK/LESSONS = 23 commits in last 30 days)?
6. **Decision scope for #27 itself:** does Council decide architecture now, or first ratify the problem statement and defer architecture to #28 after a 2-week evidence-gathering period?
7. **Runtime (`~/.claude/`) boundary:** confirmed separate from this decision regardless of A/B/C? The 5 `[runtime]` sections in `.dev-knowledge/` (8%) — do they migrate to `~/.claude/` independently as a Phase 4 regardless of architectural choice?

---

## Recommendation (non-binding)

**Option A (tag-first), on grounds that the hypothesis "LLM practice has non-dev consumers" is currently weak — the only candidate non-dev use case is a prompt library for presales, which is itself hypothetical.** Option A pre-classifies the content at low cost, so the moment the non-dev hypothesis becomes real, a migration to B is mechanical (extract by tag). Option C is premature until the 7/13 pattern proves to generalize across more than one domain.

If Council disputes the weakness of the non-dev hypothesis — if a presales prompt library, research workflow, or third consumer is actually imminent within 8 weeks — recommendation shifts to B.

---

## Appendix: Migration Details per Option

### If Council chooses A

**Goal:** add `scope:` tag frontmatter to all 63 sections in 4–6 hours.

1. **File pass order** (by section density, hot-path first):
   - PLAYBOOK.md (20 sections, ~2h) — source of truth for taxonomy, do first
   - ESSENTIALS.md (9 sections, ~30min)
   - ENVIRONMENT.md (10 sections, ~30min)
   - SESSION_SETUP.md (5 sections, ~15min)
   - HANDOFF_PROCESS.md (6 sections, ~15min)
   - CLAUDE.md (7 sections, ~15min) — all `[meta]`, fast
   - README.md (5 sections, ~10min) — all `[meta]`, fast
   - LESSONS.md: add `scope:` column/inline tag to new entries going forward only (do not edit existing entries — append-only constraint)

2. **Tag source:** use Phase 2 tags verbatim as starting point. Any disagreement is a tag-vocabulary issue to resolve once, not per-file.

3. **Consumer protocol updates** (~1h):
   - ESSENTIALS §"Starting a New Browser Chat": add filter-by-tag rule per chat type.
   - SESSION_SETUP §"Step 2: Start the Chat": specify which tags to include per chat type.
   - CLAUDE.md: add tag vocabulary section.

4. **Optional `.filter-manifest.yaml`** (~1h): define named views (e.g. `llm-only: [llm, hybrid, meta]`, `dev-only: [dev, hybrid, meta, runtime]`, `universal-only: [llm, meta]`).

5. **Verification:** all 63 sections tagged; no section untagged or with unrecognized tag value; ESSENTIALS upload protocol updated.

### If Council chooses B

**Goal:** produce two repos with a shared-core, ~1 working week.

1. **Create `llm-practice/` skeleton** (day 1): new git repo, README.md, CLAUDE.md. Initial structure based on Phase 2 "Candidates for extraction" list (13 files).
2. **Extract 13 cleanly-`[llm]` sections** (day 1–2): move each section to a dedicated file in `llm-practice/`, preserving content verbatim.
3. **Set up `shared-core/`** (day 2–3): decide submodule vs symlink (recommend symlink for simplicity on Windows, or plain file copy with a sync script). Move 3 primitives: `model-mode-effort-spec.md`, `handoff-section-schema.md`, `lesson-categories.md`.
4. **Refactor hybrid sections in `.dev-knowledge/`** (day 3–4): for each of 7 hybrid PLAYBOOK sections + 4 hybrid ESSENTIALS sections + 1 SESSION_SETUP, add a link to the corresponding `shared-core/` primitive for the universal portion; keep the dev-specific content in place.
5. **Grandfather LESSONS.md** (day 4): leave untouched. Create `llm-practice/LLM_LESSONS.md` for forward-looking LLM-only lessons. Document the split convention in both repos' CLAUDE.md.
6. **Update upload protocols** (day 4–5): ESSENTIALS (dev) + new ESSENTIALS (LLM) + SESSION_SETUP updates — what to upload for each chat/session type.
7. **Rewire cross-references** (day 5): all inbound links in Phase 1 cross-reference table need verification; broken links blocked by scripted check.
8. **Verification** (day 5): file count matches expectation; no broken links; both CLAUDE.md files load cleanly; at least one consumer test (browser chat upload with new protocol) succeeds.

### If Council chooses C

**Goal:** base + extension architecture, ~2–3 weeks.

1. **Week 1 — design overlay convention:**
   - Decide extension declaration syntax (YAML header `extends: llm-practice/file.md#section` vs. filename convention `foo-dev.md` extends `foo.md`).
   - Decide loader implementation: at-read-time concatenation via a helper script, or static pre-generation into a build output.
   - Document convention in a new `OVERLAY_SPEC.md` at the workspace root.
2. **Week 1–2 — build base:** extract 13 cleanly-`[llm]` sections + the universal-structure portions of the 7 hybrid PLAYBOOK sections. This is a content rewrite, not just a move: must split each hybrid into "structure-only" (base) and "dev-specific" (extension). Sections: S2, S3, S7, S8, S9, S10, S14 of PLAYBOOK plus ESSENTIALS Writing a Prompt, Ending a Session, Feedback Loop, The 5 Rules.
3. **Week 2 — build dev extensions:** for each of the 7 hybrid sections above, write the corresponding `extensions/*-dev.md` file with only the dev examples/additions, declaring extension via the chosen convention.
4. **Week 2 — keep pure-dev files unchanged:** S0, S1, S6, S11, S13, S15, S16 of PLAYBOOK become standalone `.dev-knowledge/` files with no overlay relationship.
5. **Week 3 — LESSONS.md disposition:** grandfather original; create `llm-practice/LESSONS_LLM.md` (base) and `.dev-knowledge/LESSONS_DEV.md` (extension-domain). Document categorization rule.
6. **Week 3 — rewrite ESSENTIALS:** either as two cheat sheets (base + dev) or as a single overlay-demonstrating example — decide per Council preference.
7. **Week 3 — build consumer loader:** a helper (Python script or `cat` composition) that, given a consumer type, produces the concatenated read set. Minimal viable version: one shell command that cats base + extension files in the right order.
8. **Verification:** for each of 7 hybrid sections, loader output matches current PLAYBOOK semantics (manual diff-review, not automated — content is rewritten). Base repo alone is usable by a hypothetical non-dev consumer. Dev repo alone is not usable (extension-only is incomplete by design — documented as such).

---

*End of brief. Architectural decision deferred to Council #27.*
