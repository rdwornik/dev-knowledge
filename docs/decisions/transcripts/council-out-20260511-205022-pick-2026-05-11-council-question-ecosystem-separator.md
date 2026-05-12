# AI Council Debate: ## Question: What is the canonical filename / foldername separator across the De

**Date:** 2026-05-11 20:50:22
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 420.8s
**Panel Mode:** full (4-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\2026-05-11-council-question-ecosystem-separator.md
**Cost:** ~$0.3861 (73,192 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt **hyphen-everywhere** (`ADR-NN-topic.md`, kebab-case) as the canonical separator across the Dev ecosystem, migrate `.dev-knowledge` in one shot with link rewrites, mandate universally, and align the council CLI output to match.

## Alternatives Considered
- **Underscore everywhere (Q1-B):** Rejected. Requires migrating the majority (corp-monorepo, ai-council, audit/handoff files, all `YYYY-MM-DD-slug.md` patterns) to satisfy the minority. Fights Markdown/web ecosystem norms (URL-safe, no shift key, kebab-case is the de facto standard for `.md` files on GitHub). Underscore also visually disappears under hyperlink underlines — a real readability hit at 2am.
- **Hybrid rule (Q1-C):** Rejected outright. "Underscore as structural separator after numeric prefix, hyphen elsewhere" is exactly the kind of rule a solo ADHD operator will misapply six months from now, and that a future engineer will have to reverse-engineer from examples. High cognitive load = tech debt per my operating principle.

## Decision Criteria
1. **Cognitive load minimization** — one rule, no exceptions, memorable without consulting the ADR.
2. **Migration cost vs. status quo drift** — minimize total files touched across the ecosystem, not just in one repo.
3. **Ecosystem alignment** — match prevailing Markdown/GitHub/URL conventions.
4. **Operator constraint** — universal convention (per 2026-05-11 framing); no sustained manual discipline required.
5. **Link integrity** — internal Markdown references must survive migration.

## Assumptions
- Counting across all repos, hyphen-pattern files outnumber underscore-pattern files (audit shows hyphen dominates in corp-monorepo, ai-council, audit/handoff files; underscore is concentrated in `.dev-knowledge` ADRs + CLI transcripts — roughly 30-50 underscore files vs. 100+ hyphen files, ballpark).
- A scripted rename + link-rewrite pass (ripgrep + sed, or a small Python script) is feasible and can be validated by a link checker.
- The council CLI's filename format is owned by the operator and can be changed without breaking downstream consumers (no external system parses `council_out_*` by regex).
- "No broken internal links" means within-repo Markdown links; external bookmarks to specific ADR filenames are not a hard constraint (no public hosting implied).

## Recommendation

**Now:**
- **Q1 → A (hyphen everywhere).** Single rule: `[a-z0-9-]+\.md`. Numeric prefixes use hyphen (`ADR-27-scope-tagging.md`, `2026-05-11-cross-repo-pattern-audit.md`).
- **Q2 → A (rename all ~31 files in `.dev-knowledge` now).** Clean state. Script the rename, run a link-rewrite pass over all `.md` files, run a link checker, commit as one atomic ADR-34 amendment PR.
- **Q3 → A (universal mandate).** ADR-34 amendment makes hyphen the canonical separator for `.dev-knowledge` AND child repos. Per operator's "convention is universal" framing, recommendation-tier creates exactly the inconsistency that triggered this council.
- **Q4 → A (rename CLI output to `council-out-YYYYMMDD-HHMMSS-topic.md`).** Same rule applies to machine-generated artifacts. Carve-outs for "functional identifiers" are how hybrid conventions reappear.

**Not now:**
- Don't add redirect stubs (Q2-C). They're noise; if no external links exist, the cost is unjustified.
- Don't introduce a date-format change alongside this (keep `YYYYMMDD` vs `YYYY-MM-DD` distinction as-is for now — that's a separate ADR if anyone cares).
- Don't add lint/CI enforcement in this PR. Ship the convention first.

**Defer:**
- Pre-commit hook or CI check that rejects underscores in new `.md` filenames — add in a follow-up once the convention has settled for ~30 days and the rule is proven stable.
- Legacy archive files in `corp-monorepo`/`corp-sca` (`YYYY-MM-DD_TYPE_topic.md`): rename opportunistically when touched, not in a sweep. They're archives.

## Rationale
- **Hyphen wins the file-count vote and the ecosystem vote simultaneously.** Migrating ~31 `.dev-knowledge` files + ~15 CLI transcripts is cheaper than migrating 3+ child repos plus all audit/handoff files; estimated 46 renames vs. 100+ for the reverse.
- **One rule beats a clever rule for a solo ADHD operator.** "All lowercase, hyphens between words, `.md` extension" is recallable without lookup. The hybrid (Q1-C) violates the explicit operator constraint about sustained manual discipline.
- **URL/Markdown ergonomics:** hyphens render cleanly under link underlines, are URL-safe without escaping, and match GitHub's auto-generated anchor slugs — reducing the gap between filename and rendered anchor.
- **Universal mandate prevents recurrence:** the audit exists precisely because ADR-34 left child repos as "recommendation." Recommendation-tier conventions in a solo-operator ecosystem decay to inconsistency within months.
- **CLI alignment matters more than it seems:** ~15 transcripts/month accumulating in underscore form would re-create the bifurcation within a year. The CLI is the largest filename-emitter in the system.

## Trade-offs
- **Migration cost up front:** ~46 file renames + link-rewrite pass + CLI code change. Estimated 2-4 hours of focused work including validation.
- **Lose PEP 8 / Python-identifier resonance** that originally motivated underscore in ADR-34. Acceptable — these are documents, not Python modules.
- **ADR-34 amendment churn:** invalidates the prior spec example and forces an ADR-43 amendment process. One-time cost.
- **Existing external references** (if any) to underscore-form ADR filenames break. Acceptable given no public hosting assumed.

## Risks
- **Link rewrite misses references in non-`.md` files** (e.g., scripts, configs that hardcode ADR paths). Likelihood: medium. Impact: low-medium. *Mitigation:* run `rg '_'` across the full repo, not just `.md`, before committing; include a post-rename link check in the PR checklist.
- **CLI rename breaks something downstream** (a glob pattern, a sort order, an external indexer). Likelihood: low. Impact: medium. *Mitigation:* grep the CLI codebase for the literal `council_out_` prefix before changing; the `YYYYMMDD-HHMMSS` ordering still sorts lexicographically.
- **Operator reverts to underscore by muscle memory on next ADR.** Likelihood: medium given ADHD constraint. Impact: low individually, high cumulatively. *Mitigation:* this is exactly why the deferred CI lint matters — schedule it as the immediate follow-up, not "someday."
- **Mid-migration interruption leaves repo in mixed state.** Likelihood: medium (solo operator). Impact: medium. *Mitigation:* script the rename so it's idempotent and runnable in a single command; commit as one PR, not incrementally.

## Signals to Revisit
- A tooling dependency emerges that requires underscore-separated filenames (e.g., a static site generator or indexer that treats hyphens as word boundaries in a way that harms search).
- The ecosystem grows to include repos where underscore is already mandated by external convention (e.g., a Python package's docs directory governed by its own style guide).
- Link-rewrite migration reveals >200 inbound references — at that scale, redirect stubs (Q2-C) become worth reconsidering for the migration approach, though not for the convention itself.
- Operator reports the rule still feels ambiguous after 60 days — indicates the problem wasn't separator choice but something else (e.g., numeric prefix format, topic slug rules).

*Latency: 38.16s | Tokens: 4877*

### Gemini (gemini-3.1-pro-preview)

## Position
Mandate the hyphen (`-`) as the universal canonical separator for all filenames and foldernames across the entire ecosystem, execute an atomic automated rename of all existing files/links now, and enforce the convention via CI/CD linting. 

## Alternatives Considered
- **Hybrid Separator (Underscore for structure, hyphen for words):** Rejected. From an integration perspective, complex delimiter rules require complex regex parsing in automation scripts. Complex parsing is fragile, increasing the risk of script failures or command-injection edge cases in cross-repo automated workflows.
- **Rename Forward-Only (Legacy mixed state):** Rejected. A permanent mixed state forces all future security scanning, compliance auditing, and integration scripts to maintain multiple parsing branches indefinitely. This increases the integration blast radius and cognitive load. 

## Decision Criteria
- **Integration Predictability:** Ease and safety of programmatic parsing across varied external integrations, shell scripts, and CI/CD pipelines.
- **Operator Constraint (ADHD):** Must require zero manual discipline post-decision; the convention must be universally consistent and mechanically enforceable.
- **Blast Radius of Change:** Risk of breaking internal linking structures vs. the long-term risk of ecosystem fragmentation.
- **Universal Application:** Solutions must bridge the `.dev-knowledge` and child repos without variance.

## Assumptions
- No external, unmodifiable systems (like a rigid third-party documentation portal) tightly couple to the exact current file paths of the existing ~31 underscore-named `.dev-knowledge` files.
- The CLI tool source code generating the `council_out_*` files is fully within your control and can be updated synchronously with the file migration.
- You have the ability to enforce filename compliance via CI/CD (e.g., pre-commit hooks or GitHub Actions).

## Recommendation
**What to do now:**
- Ratify Option 1A, 2A, 3A, and 4A. Standardize strictly on `kebab-case` (`ADR-NN-topic-name.md`).
- Amend ADR-34 to upgrade the filename convention from a `.dev-knowledge` mandate / child recommendation to a **universal mandate**.
- Update the CLI tool to output `council-out-YYYYMMDD-HHMMSS-topic.md`.
- Execute an atomic migration script (e.g., bash + `sed`/`rg`) in a single PR to rename the ~31 existing `.dev-knowledge` files and rewrite all internal Markdown links simultaneously. 
- Implement a CI linter or pre-commit hook that explicitly blocks the commitment of files with underscores in their names across all managed repos.

**What not to do now:**
- Do not create redirect stubs or symlinks in the old paths. Stubs leave legacy routing active, artificially expanding the integration surface area and complicating automated audits.
- Do not rely on "remembering" to use hyphens. If the linter isn't active, the decision isn't finalized.

**What to defer until later:**
- Retroactively renaming files in the `archive/` directory. Since this folder is functionally inactive, the integration blast radius of ignoring it is near zero, and it avoids unnecessary git history churn.

## Rationale
- **Deterministic Regex Parsing:** Underscores (`_`) are part of the `\w` regex character class in nearly all engines, while hyphens (`-`) are not. Standardizing on hyphens guarantees that word-boundary (`\b`) parsing in cross-repo integration scripts will reliably extract IDs, dates, and topics without catastrophic backtracking or truncation.
- **Ecosystem Tooling Compatibility:** Hyphens are the canonical web and markdown separator (RFC 3986 URL slugs). Using them prevents unpredictable URL-encoding artifacts (`%5F` vs `_`) when integrating with static site generators or external issue trackers.
- **Zero-Discipline Security:** For an ADHD solo operator, consistency is a security boundary. A single, universal rule ("hyphens only") combined with automated CI enforcement completely eliminates the human error vector from directory structuring.
- **Trivial Migration Footprint:** ~31 files is a very small blast radius. Executing an atomic rename now eliminates the technical debt before the `.dev-knowledge` repo scales to a size where a migration would carry critical operational risk.

## Trade-offs
- **External Link Breakage:** Any external bookmarks (e.g., local browser bookmarks, Notion docs, external system references) pointing to the old underscore URLs will break. 
- **Immediate Implementation Tax:** Requires an upfront investment of 1-2 hours to write the migration script, configure the CI linter, and validate internal link integrity before merging.

## Risks
- **Risk:** The migration script misses nested internal Markdown links, resulting in broken documentation navigation (violating constraints).
  - *Likelihood:* Moderate
  - *Impact:* High
  - *Mitigation:* Run an automated markdown link checker (e.g., `markdown-link-check` CLI) as a required CI step on the migration PR before merging.
- **Risk:** Open feature branches or PRs contain modifications to the currently underscore-named files, resulting in severe merge conflicts upon rename.
  - *Likelihood:* Low
  - *Impact:* Moderate
  - *Mitigation:* Institute a brief code freeze. Merge or close all active PRs touching the target files before executing the migration PR.

## Signals to Revisit
- Adoption of a mandatory upstream dependency (e.g., an enterprise code-generation framework or specific static site engine) that functionally requires underscores or camelCase for file routing.
- High frequency of CI pipeline failures specifically due to the filename linter, which would indicate that auto-generated files from an unmanaged third-party integration are clashing with the universal mandate.

*Latency: 34.58s | Tokens: 4392*

### Deepseek (deepseek-v4-pro)

## Position
Adopt **hyphens everywhere** as the single canonical word separator in filenames and foldernames. Rename all existing artifacts and internal links immediately, enforce it universally across `.dev-knowledge` and all child repos, and align the CLI output convention to hyphens.

## Alternatives Considered
- **Underscore everywhere**: Would require migrating the majority of audited repos (which already use hyphens) and goes against the Markdown/static-site ecosystem preference for kebab-case. Rejected because it creates more migration cost without a compensating operational advantage, and risks subtle URL/path ambiguities in tooling that treats underscores as formatting hints.
- **Hybrid (underscore as structural separator after numeric prefix, hyphens elsewhere)**: Would preserve ADR‑34’s original intent but introduces a context‑sensitive rule that must be remembered and manually applied (“is this after a numeric prefix or not?”). For a solo operator with ADHD, that is a guaranteed inconsistency generator and violates the no-manual-discipline constraint. Rejected as the riskiest option for universal convention at scale.

## Decision Criteria
1. **Zero manual discipline post‑decision** (solo operator, ADHD – every naming choice must be mechanically determinable).
2. **Universal consistency** across all repos and artifact types (operator’s framing: convention must be uniform; inconsistency is a failure mode at any scale).
3. **Migration safety** – broken internal links are unacceptable; the change must be automatable with verifiable correctness.
4. **Ecosystem alignment** – lowest impedance with URLs, static site generators, and common Markdown toolchains.
5. **Rule simplicity** – a single character class, no conditional logic, so automation can enforce it with a trivial regex.

## Assumptions
- An automated script can rename ~31 files and recursively rewrite all internal Markdown links with 100 % accuracy, and a link‑checker can validate the result.
- No significant external inbound links reference the current underscore filenames; if they do, they are either undiscovered or can be handled with one‑time redirects.
- The CLI output convention change is a single‑repository code change with no downstream automation dependencies that aren’t under the council’s control.
- The operator’s “universal convention” framing overrides any historical per‑repo recommendations; ADR‑34 can be amended accordingly without blocking the rename.

## Recommendation
### What to do now
- **Define canonical separator as hyphen** (`-`) for all filenames and foldernames. This means `ADR-NN-topic.md`, `YYYY-MM-DD-slug.md`, `council-out-YYYYMMDD-HHMMSS-topic.md`, and all archive paths use hyphens.
- **Rename all existing ADRs and transcripts** in `.dev-knowledge` and any child repos currently using underscores. Run an automated script that: (a) renames files, (b) finds every Markdown link `[text](old-name)` or image reference and rewrites the path component, (c) verifies with `find`/`grep` that no old underscore reference remains.
- **Amend ADR-34** (via ADR‑43 process) to mandate hyphens universally, replacing the underscore spec.
- **Update the Council CLI** to output `council-out-YYYYMMDD-HHMMSS-topic.md`; release that change immediately.
- **Add a CI lint rule** that rejects any filename or folder containing an underscore in `.dev-knowledge` and, once adopted, in child repos.

### What not to do now
- Do **not** attempt a hybrid separator scheme; it creates a persistent decision point that will produce drift.
- Do **not** do “rename forward only” or leave old paths with redirect notes; that permanently bakes inconsistency, doubling the operator’s mental matching cost.
- Do **not** leave CLI output unaligned – treating it as a “functional identifier” rebuilds the ambiguity we’re eliminating.

### What to defer until later
- If external permalink commitments surface, set up HTTP redirects from old underscore URLs to new hyphen URLs. This is a separate, low‑priority operational task and does not affect the convention itself.

## Rationale
- **Quantitative safety**: 31 files and their internal links can be atomically renamed and link‑checked in under 10 seconds of CI runtime; the risk of a lingering link is bounded by the regex `[^\]]+\([^\)]*_[^\)]*\)` failing to match any remaining underscore paths. A zero‑miss is achievable with a dry‑run diff.
- **Cognitive load elimination**: Hyphen‑everywhere removes the question “which separator here?” entirely. There is no prefix, file type, or exception – the rule fits in a single clause and can be enforced by `awk` or `grep -v` without context. For an ADHD operator, that is the difference between a convention that survives and one that decays.
- **Exosystem default**: Kebab‑case is the de facto norm for Markdown files in static‑site generators, URL slugs, and GitHub’s own rendering of links. Using underscores invites subtle breakage when a filename appears in a URL without percent‑encoding, or when certain Markdown parsers interpret underscores as italics delimiters in raw text.
- **Migration effort is one‑off**: The entire change is a scheduled, automatable operation, not an ongoing maintenance tax. That aligns with treating convention as a “presence/absence” property, not a scaling concern.

## Trade-offs
- **Readability micro‑trade**: Some developers perceive underscores as slightly more human‑readable in source‑file listings. This is negligible and is outweighed by tool‑level consistency.
- **Loss of PEP‑8 familiarity**: For Python‑centric operators, filenames with hyphens feel unfamiliar, but this repo’s filenames are not Python modules and are never `import`‑ed.

## Risks
- **Automated link rewrites miss edge cases** (links embedded in triple‑backtick code blocks, HTML attributes, or YAML front matter). Likelihood: medium. Impact: broken internal links that fail CI. Mitigation: post‑rename, run `remark‑validate‑links` or a custom link checker across the entire repo; keep a Git `pre‑rename` tag for instant rollback.
- **External tooling depends on underscore naming** (analytics scripts, issue‑bot parsers). Likelihood: low. Impact: temporary reporting gaps. Mitigation: search org‑wide for `council_out_` and `ADR-*_` patterns before the rename, notify maintainers.
- **CLI output change disrupts unattended automation** that parses transcript filenames. Likelihood: low, given the council’s controlled scope. Mitigation: pair the CLI change with a one‑week notice to all consumers; version‑stamp the new format if needed.

## Signals to Revisit
- **External link breakage volume becomes unacceptable**: if monitoring shows a high rate of 404s from external references (e.g., Slack, pinned issues), implement permanent redirects at the repo‑host level rather than reconsidering the separator.
- **Tooling ecosystem universally rejects hyphens** (e.g., a critical tool that cannot handle hyphenated filenames surfaces). Extremely unlikely; if it occurs, fall back to underscores with the same rename‑and‑link approach.
- **Operator reports friction** after a trial period – if the hyphen convention genuinely causes more cognitive load than anticipated (e.g., misreading numbers split by hyphens), reassess, but only after collecting measurable error counts, not anecdotes.

*Latency: 115.97s | Tokens: 4553*

### Grok (grok-4.3)

## Position
Adopt hyphen as the single universal separator for all filenames and foldernames across `.dev-knowledge` and every child repo; perform a one-time rename of the 31 affected files while updating all internal markdown links.

## Alternatives Considered
Underscore-everywhere was rejected because it contradicts the hyphen pattern already present in 2 of the 3 major repos and in all audit/handoff filenames, violating the operator's explicit universal-convention requirement. Hybrid (underscore after numeric prefix only) was rejected because it imposes a context-sensitive rule that a solo operator with ADHD cannot maintain without ongoing manual discipline.

## Decision Criteria
- Must produce one separator used identically in every repo and artifact.
- Must not break any existing markdown internal links.
- Must eliminate any post-decision naming decisions that require sustained attention.
- Must align with the majority observed pattern in the audited corpus (hyphen in corp-monorepo, ai-council, and all YYYY-MM-DD audit files).
- Must be enforceable by tooling or one-time script rather than memory.

## Assumptions
- A one-time bulk rename plus link-update script is feasible and will be executed correctly.
- No external systems or published URLs currently hard-link to the current underscore filenames.
- The council CLI can be updated in a follow-on change without affecting the human-readable convention decision.

## Recommendation
Execute a one-time migration that renames every ADR and transcript file to hyphen separators, updates every internal markdown link in the same commit, and changes the CLI output template to `council-out-YYYYMMDD-HHMMSS-topic.md`. Do not keep any legacy underscore files or create redirect notes. Do not defer the CLI change. Do not allow child repos to retain their own convention.

## Rationale
- Hyphen already appears in the two largest codebases and in every audit artifact, so the change normalizes the majority pattern rather than forcing the minority pattern on more files.
- A single commit that both renames and rewrites links guarantees zero broken references without ongoing maintenance.
- Universal mandate plus one-time script satisfies the ADHD constraint by removing all future naming choices.
- CLI alignment in the same decision prevents the exact internal inconsistency now visible between `.dev-knowledge` transcripts and ADR-34 examples.
- Archive folder prefix change is already complete, so this decision finishes the remaining separator surface without reopening that work.

## Trade-offs
- 31 files must be touched and links rewritten now instead of zero files under a forward-only policy.
- Existing external references or bookmarks to underscore-named files become invalid (estimated <5 occurrences given internal audit focus).

## Risks
- Script error leaves dangling links (likelihood low if tested in a branch; impact high) — mitigate by running link checker in CI before merge.
- Operator later forgets the new convention when creating files manually (likelihood medium without tooling) — mitigate by adding a pre-commit hook that rejects underscore filenames.
- Future third-party tool defaults to underscores (likelihood low) — mitigate by documenting the hyphen rule in the root README and ADR-34 amendment.

## Signals to Revisit
- Discovery of >10 external inbound links to current underscore filenames.
- Introduction of a new repo or tool whose filename generator hard-codes underscores and cannot be configured.
- Operator reports repeated manual naming mistakes after the rename and hook are in place.

*Latency: 23.89s | Tokens: 2387*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A

**Steelman:** If (1) the rename script is provably exhaustive (zero missed links verifiable by a deterministic checker), (2) CI lint is shipped *with* the rename PR rather than later, and (3) the hyphen rule is treated as a single character-class constraint enforceable by `grep -v _`, then this is exactly the right move. The one-rule, one-tool, one-PR shape is what a 2am on-call engineer wants: "did this filename get past CI? then it's correct."

**Assessment:** Agree with the Position. The proposal correctly identifies that conventions only survive when they're mechanically enforced, not remembered.

**Strongest point:** Framing the hybrid option as "a guaranteed inconsistency generator" for an ADHD operator. That's not opinion — it's a structural claim about how context-sensitive rules decay, and it's correct.

**Weakest assumption:** "An automated script can rename ~31 files and rewrite all internal Markdown links with 100% accuracy." 100% is a strong claim. Links in YAML frontmatter, HTML `<a href>`, code fences showing example paths, and `.txt`/script files referencing ADR paths are common miss vectors. If this is wrong, the link checker catches it — but only if the link checker is configured to scan beyond `.md` bodies. Proposal doesn't specify that.

**Hidden assumptions:**
1. That the link checker (`remark-validate-links`) will catch references in non-Markdown files. It won't — it parses Markdown ASTs. References in shell scripts, JSON configs, or YAML frontmatter are invisible to it.
2. That "CI lint" can be added in the same PR without bootstrapping problems. If the lint runs on the PR that does the rename, you need to ensure it's evaluating post-rename state only.

**Overlooked risks:** Doesn't address the muscle-memory risk (operator reverts to underscore on the next manual `touch`). Defers CI lint implicitly to "post-rename" — but Proposal D correctly identifies this as the highest-likelihood failure mode for a solo ADHD operator.

---

## Proposal B

**Steelman:** If the integration surface really does include external scanners, compliance auditors, and cross-repo automation that parse filenames via regex, then the `\w` vs `\b` argument is a hard correctness issue, not aesthetics. In that world, hyphen-only isn't a preference — it's a parsing precondition.

**Assessment:** Partially agree with the Position. Right answer, partially wrong rationale. The "security boundary" and "command-injection edge cases" framing reads as imported from a different threat model (enterprise CI with hostile inputs). For a solo operator's documentation repo, this is overstated. The decision is correct; the justification overreaches.

**Strongest point:** The `\w` regex observation. Underscore being in the word-character class genuinely does cause subtle parsing failures when extracting topic slugs from filenames via `\b` boundaries. This is a concrete, testable claim with operational consequences.

**Weakest assumption:** That "security scanning, compliance auditing" are real consumers of these filenames. In a solo-operator documentation ecosystem, they aren't. If this assumption is false, the proposal's framing loses force but the recommendation survives — which means the framing is doing no load-bearing work.

**Hidden assumptions:**
1. That CI/CD enforcement infrastructure already exists in `.dev-knowledge`. Proposal A assumes the same. Neither verifies it.
2. That "code freeze" is meaningful for a solo operator — there are no concurrent contributors to freeze.

**Overlooked risks:** Deferring archive rename ("functionally inactive, blast radius near zero") is reasonable but creates a permanent mixed-state precedent. Future engineer encountering archive files with underscores will reasonably conclude the convention is "hyphen for new, underscore for old" — which is exactly the hybrid rule we just rejected, smuggled in via legacy.

---

## Proposal C

**Steelman:** If the operator's stated framing — "convention is universal" — is taken as a hard constraint rather than an aspiration, then the only remaining work is mechanics: pick the separator with the smallest migration footprint, do it atomically, enforce with a hook. C does exactly this with no embellishment.

**Assessment:** Agree with the Position. This is the most disciplined proposal — it states the decision, lists the mitigations, and stops. No drift into adjacent concerns.

**Strongest point:** "Universal mandate plus one-time script satisfies the ADHD constraint by removing all future naming choices." This is the cleanest articulation of why this decision is structurally simple even though it touches many files.

**Weakest assumption:** "<5 external references" is asserted without method. If the operator has a personal knowledge-base tool (Obsidian, Logseq, Notion) that links into `.dev-knowledge` by filename, this number could be much higher. Not catastrophic — but the proposal doesn't ask.

**Hidden assumptions:**
1. That a pre-commit hook is sufficient enforcement. Pre-commit hooks are bypassable (`--no-verify`) and only fire on commit. They don't catch files created and never committed, or files committed from another machine without the hook installed. CI-level enforcement is stronger.
2. That the operator will actually install the pre-commit hook. On a fresh clone or new machine, the hook doesn't auto-install.

**Overlooked risks:** Doesn't address the CLI re-emission problem in depth — if the CLI is regenerated frequently, the *moment* between deciding and shipping the CLI fix is a window where new underscore files appear and need re-migration. Proposal D catches this; C doesn't.

---

## Proposal D

**Steelman:** If the operator's actual highest risk is "I will type the wrong separator at 2am next Tuesday," then the proposal's structure — ship the convention, ship the CLI fix immediately, defer the lint by ~30 days only after explicitly naming the muscle-memory risk as the reason — is honest about its sequencing tradeoffs.

**Assessment:** Partially agree with the Position. Right on Q1/Q3/Q4. Wrong on the deferred CI lint. "Ship the convention first, lint in 30 days" violates D's own stated principle that conventions decay without enforcement. The 30-day window is exactly when muscle memory creates new violations. This is the same mistake ADR-34 made (recommendation-tier for child repos) reappearing inside a single proposal.

**Strongest point:** Counting files across *all* repos, not just `.dev-knowledge`. The observation that hyphen wins the file-count vote (46 underscore renames vs. 100+ hyphen renames for the reverse) makes the decision quantitatively obvious rather than aesthetic. None of the other proposals do this math explicitly.

**Weakest assumption:** "Don't add lint/CI enforcement in this PR. Ship the convention first." This assumes the operator will reliably return to add the lint within 30 days. For an ADHD operator — by the proposal's own framing — this is precisely the kind of deferred follow-up that doesn't happen. Breaks: convention decays, exactly as the proposal warns elsewhere.

**Hidden assumptions:**
1. That ADR-34 amendment "churn" via the ADR-43 process is a meaningful cost. For a solo operator, this is a paperwork formality, not a coordination cost.
2. That archive files in `corp-monorepo`/`corp-sca` can be renamed "opportunistically when touched." Archives are by definition not touched. This is "never," dressed up as "later."

**Overlooked risks:** The 30-day deferred lint window. Proposal D names muscle-memory as a "medium likelihood, high cumulative impact" risk and then schedules the only mitigation 30 days out. Internally inconsistent.

---

# Revised Recommendation

**I am updating my position in one specific way:** the CI lint must ship in the same PR as the rename, not deferred.

**What changed my mind:** Proposal D's own risk analysis. D correctly identifies muscle-memory reversion as medium-likelihood, high cumulative impact, then defers the only mitigation by 30 days "once the rule is proven stable." But the rule cannot prove stability without enforcement — that's circular. Proposals A, B, and C all ship the lint with the rename. D is the outlier, and D's own framing argues against itself.

**My recommendation for the council:**

| Q | Decision | Notes |
|---|---|---|
| Q1 | **A — Hyphen everywhere** | One character class. `[a-z0-9-]+\.md`. No exceptions. |
| Q2 | **A — Rename all 31 files now** | Atomic PR. Single commit. Reversible via tag. |
| Q3 | **A — Universal mandate** | Recommendation-tier is what created this audit. Don't repeat it. |
| Q4 | **A — Rename CLI output** | The CLI is the largest filename-emitter; carve-outs reconstitute the bifurcation. |

**Operational requirements the PR must satisfy (the 2am test):**

1. **Lint ships with the rename, not after.** A CI check that rejects any new file matching `[A-Za-z0-9]*_[A-Za-z0-9]*\.md` in the tracked tree. Pre-commit hook is supplementary, not primary — CI is the enforcement point because it's not bypassable and not machine-local.

2. **Link scan must cover non-Markdown files.** Run `rg '_' --type-not md` across the repo before merging and audit hits manually. Proposal A's `remark-validate-links` is necessary but not sufficient.

3. **Archive files are renamed in the same sweep.** Proposal B's and D's "leave archives alone" creates a precedent that says "the rule has exceptions for old stuff." Future engineer reading the codebase will infer a hybrid rule from the evidence. Rename them. Git history is preserved; that's what `git log --follow` is for.

4. **The PR is the artifact a future engineer reads to understand the convention.** Include in the PR description: (a) the one-sentence rule, (b) the lint regex, (c) the rationale for universal mandate. The ADR-34 amendment links to this PR.

**What I'm not conceding:** The decision is hyphen. The migration is now. The mandate is universal. The CLI aligns. These are non-negotiable per the operator's universal-convention framing and the ADHD constraint. The only update is sequencing: enforcement is part of the decision, not a follow-up.

*Latency: 48.52s | Tokens: 14078*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, my primary lens on this filename convention is not aesthetics or readability—it is parsing safety, ecosystem predictability, and the blast radius of change. Filenames are system inputs. They are passed as arguments to shell scripts, parsed by CI/CD pipelines, and evaluated by external indexing tools. Mixed conventions require complex, branching regex logic in downstream integrations, which exponentially increases the risk of catastrophic backtracking (ReDoS), command injection, and broken automation. 

Here is my evaluation of the council's proposals.

---

### Proposal A

**Steelman first:** This proposal is exactly right if the primary risk to the ecosystem is human cognitive load, and if a purely mechanical, regex-driven migration can flawlessly execute the rewrite without introducing subtle syntax errors into the documentation supply chain. 

**Your assessment:** Partially agree with the Position. The core mechanics (hyphen everywhere, universal mandate, automated rename) are sound. However, I disagree with its reliance on simplistic bash/regex tools (`awk`/`grep`/`sed`) for rewriting Markdown links, which introduces unnecessary risk.

**Strongest point:** The explicit link between cognitive load and system decay ("For an ADHD operator, that is the difference between a convention that survives and one that decays"). This accurately recognizes the operator as a critical dependency in the system architecture.

**Weakest assumption:** "An automated script can... rewrite all internal Markdown links with 100% accuracy" using standard CLI text-processing tools. Markdown is context-sensitive (code blocks, inline HTML, frontmatter). Regex will inevitably rewrite a path it shouldn't or miss a malformed link, breaking downstream rendering.

**Hidden assumptions:** 
1. Assumes external inbound links are non-existent or statistically irrelevant without prescribing an audit log to prove it.
2. Assumes the CI lint rule can be written flawlessly on day one without falsely flagging valid artifacts.

**Overlooked risks:** Supply chain risk of the validation tooling. Relying on "a custom link checker" or unvetted npm packages (`remark-validate-links`) to validate the rename introduces third-party dependency risks into the CI pipeline.

---

### Proposal B

**Steelman first:** This proposal is exactly right if ecosystem fragmentation and programmatic parsing complexity represent literal integration vulnerabilities, and if enforcing a single deterministic parsing rule (hyphens) is the only way to secure cross-repo workflows.

**Your assessment:** Agree with the Position. This proposal correctly identifies filenames as an integration boundary and prioritizes deterministic parsing over legacy preservation.

**Strongest point:** The insight regarding "Deterministic Regex Parsing." Underscores are part of the `\w` regex class; hyphens are not. Standardizing on hyphens guarantees that word-boundary (`\b`) parsing in integration scripts will reliably extract metadata without edge-case truncation. 

**Weakest assumption:** The assumption that the `archive/` directory is "functionally inactive" and its blast radius is "near zero." Security tools, compliance audits, and historical scrapers parse archives. Ignoring them preserves the exact parser bifurcation we are trying to eliminate.

**Hidden assumptions:**
1. Assumes the solo operator's ADHD will not prevent them from maintaining the CI/CD linting infrastructure itself.
2. Assumes a "brief code freeze" across multiple repositories is easily coordinated without disrupting parallel background automation.

**Overlooked risks:** CI pipeline lockout. If the CI linter is misconfigured in the atomic PR, it will block all subsequent commits across all repos, bringing the continuous integration pipeline to a halt until bypassed or rolled back.

---

### Proposal C

**Steelman first:** This proposal is exactly right if the safest path is the one of least resistance—normalizing the ecosystem to the existing majority pattern (hyphen) to minimize the sheer number of files mutated and integrations disrupted.

**Your assessment:** Disagree with the execution strategy. While the end-state (hyphen everywhere) aligns with the council, the enforcement mechanisms are dangerously weak.

**Strongest point:** The statistical justification: Hyphen already appears in the two largest codebases and all audit artifacts. Normalizing to the majority minimizes the integration blast radius by mutating the fewest number of upstream integrations.

**Weakest assumption:** "Mitigate by adding a pre-commit hook that rejects underscore filenames." Client-side pre-commit hooks are easily bypassed (`git commit --no-verify`), fail silently if local environments drift, and provide zero defense-in-depth. 

**Hidden assumptions:**
1. Assumes a one-time script equates to a permanent fix, entirely ignoring how the CI/CD pipeline will process future PRs from automated bots (e.g., Dependabot, Snyk) that might auto-generate files.
2. Assumes external tools will honor the "documented hyphen rule in the root README" without programmatic enforcement.

**Overlooked risks:** No rollback plan. A bulk one-time rename without a phased CI deployment or dry-run validation is a high-risk operational maneuver. If the script corrupts file metadata, there is no stated recovery mechanism.

---

### Proposal D

**Steelman first:** This proposal is exactly right if immediate, momentum-driven execution (deferring CI friction) gets the migration done before the operator gets distracted, treating over-engineering as an anti-pattern.

**Your assessment:** Strongly disagree with the timeline and phasing. Deferring CI linting while demanding immediate execution is an architectural failure mode.

**Strongest point:** The explicit math on migration cost (46 renames vs 100+). By measuring the exact footprint of the change, it effectively scopes the potential blast radius of the operation.

**Weakest assumption:** "Defer... CI check... in a follow-up once the convention has settled for ~30 days." A convention without enforcement is merely a suggestion. With an ADHD operator, a deferred 30-day task has a high probability of never occurring, guaranteeing a recurrence of the mixed state.

**Hidden assumptions:**
1. Assumes leaving historical archive files in `YYYY-MM-DD_TYPE_topic.md` format (underscores) does not violate the "universal mandate" rule explicitly demanded in Q3. 
2. Assumes the CLI output format change will not break downstream event triggers or glob-based artifact uploads in GitHub Actions.

**Overlooked risks:** State drift during the 30-day "settling" period. Without the CI linter active on day one, the CLI or the operator will inevitably generate underscore files in the gap, forcing a second, undocumented migration later.

---

### Revised Recommendation

**Update Position:** I maintain the universal consensus to adopt **hyphen everywhere (`kebab-case`)**, rename all existing files natively, and mandate this universally. However, I am updating the execution strategy strictly based on Proposal B's integration insights (regex boundaries) and correcting the critical enforcement failures in Proposals C and D. 

Every time we write a script that parses a filename, we are creating an API boundary. Supporting multiple delimiters means writing parsing branches. Parsing branches breed regex vulnerabilities and logic bugs. Therefore, universality must be absolute.

**The following enforcement and execution mandates must be applied immediately:**

1. **Absolute Universal Mandate (No Archive Exemptions):**
   We will not defer or exempt the `archive/` directories (overriding Proposals B and D). Leaving mixed states in historical folders forces security scanners, data-loss prevention (DLP) tools, and compliance scripts to maintain dual-parsing logic indefinitely. The migration script must hit *every* Markdown file in the ecosystem.
   
2. **Synchronous Server-Side CI Enforcement (No Deferrals, No Pre-commits):**
   Do not defer the CI linter (overriding Proposal D), and do not rely on local pre-commit hooks (overriding Proposal C). In the *exact same atomic PR* that renames the files, a server-side GitHub Actions workflow (or equivalent CI pipeline) must be merged that strictly fails any build containing `_` in a `.md` filename. For an ADHD solo operator, the pipeline is the only trusted boundary. 

3. **AST-Based Link Rewriting (No Regex for Content):**
   Do not use bash, `sed`, or raw `ripgrep` to rewrite Markdown links (overriding Proposals A, B, and D). Regex is insufficient for structural rewriting and will corrupt code blocks or frontmatter. You must use an AST-aware tool (Abstract Syntax Tree) like `remark-cli` or a robust Python Markdown parsing library to rewrite the links. The blast radius of corrupting documentation via bad regex is higher than the blast radius of broken links.

4. **CLI Realignment:**
   The Council CLI must be updated to emit `council-out-YYYYMMDD-HHMMSS-topic.md` synchronously with the file rename. Leaving it as a "functional identifier" creates a permanent parsing exception. 

**Summary of Action:**
Adopt `kebab-case` universally. Execute an AST-aware atomic rename of *all* files (including archives). Merge the CI enforcer in the exact same commit. Do not defer structural integrity.

*Latency: 44.64s | Tokens: 10446*

### Deepseek (deepseek-v4-pro)

After reviewing the four proposals, I note that they have converged on the same core answer: **hyphen everywhere, rename all files now, universal mandate, CLI alignment**. The divergence is in enforcement timing (immediate CI lint vs. deferred) and archive handling (sweep vs. opportunistic). My evaluation therefore dissects those micro‑differences, because they determine whether the convention survives its first human mistake.

I’ll walk through each proposal, then state where my own recommendation lands after absorbing the strongest parts of all four.

---

## Proposal A

**Steelman**  
The proposal is exactly right if:
- A fully automated script can rename ~31 ADR + ~15 transcript files (46 total) and rewrite every internal Markdown link with 100 % precision, including references in YAML front‑matter, code blocks, and HTML attributes.
- No external permalink commitments exist that would break; any that do can be handled later with HTTP redirects without blocking the rename.
- A CI lint rule rejecting underscores can be activated immediately and will be accepted as “the way things are” without friction.
- The operator’s ADHD constraint is satisfied by making the rule mechanically enforceable at the moment of commit, so no manual discipline is needed from day one.

**Assessment** — **Agree**  
The reasoning is quantitative (regex‑based zero‑miss achievable, CI runtime <10 seconds), directly addresses cognitive load, and puts enforcement in place immediately. That immediate CI rule is the right call for a solo ADHD operator — it prevents the next file from being created with an underscore the moment the PR merges.

**Strongest point**  
The statement that for an ADHD operator “the question ‘which separator here?’ removed entirely” is the difference between a convention that survives and one that decays. The proposal backs that with an enforcement mechanism from hour zero, not “someday.”

**Weakest assumption**  
That the automated link‑rewrite script will catch references embedded in ` ``` ` code blocks, HTML attributes, or YAML front‑matter with equal certainty. If the regex misses structured data blocks, internal links will break, and the CI link‑checker *after* the rename will find them only after the commit is pushed. The fix could then require a revert or a second pass, injecting confusion and potential mixed‑state commits.

**Hidden assumptions**
1. That the operator will **not** create new files between the migration commit and the CI lint rule activation. If the lint rule is added in the same PR, they’re deployed atomically. If the migration is one PR and the lint is another, a window exists. The proposal says “add a CI lint rule” but doesn’t state it would be in the migration PR — it might be separate.
2. That all “internal markdown links” live in `.md` files only. The script may need to scan all text files (e.g., `.yaml`, `.json`, `.ts`, `.py`) for path strings containing underscores that reference filenames.

**Overlooked risks**
- The script’s `find` and `grep` verification step after rename will re‑read renamed files; if the rename renames files in‑place and the link‑rewrite doesn’t account for new filenames in a second pass, it could miss links that were broken by the rename itself (e.g., a link `[old](old_file.md)` after `old_file.md` is renamed but link is not updated because the rewrite used the old name and then the file is gone — though careful script avoids that).
- Non‑Markdown configuration files that contain ADR paths (e.g., CI scripts, issue templates) are not explicitly mentioned. The audit would need to target those.

---

## Proposal B

**Steelman**  
This is the right answer if:
- Downstream integrations truly parse filenames using regex word boundaries (`\b`), and underscores inside `\w` cause catastrophic backtracking or mis‑extraction.
- A one‑time freeze of all open PRs can be coordinated without delaying urgent work.
- No archive file renaming is desired now, and deferring them is safe because future scripts won’t have to parse mixed separators in archived filenames (since archives are “inactive”).
- The CI linter is deployed immediately as part of the migration, preventing post‑merge drift.

**Assessment** — **Agree**  
Its strongest addition is the concrete regex‑parsing argument: `_` is `\w`, `-` is not. That’s a real failure mode when you later write an automation script that tries to isolate a topic slug from a filename like `ADR-27-scope-tagging.md` — a pattern like `(\d+)-(.+)\.md` works; with underscores you risk splitting on `_` versus `-` inconsistently. The proposal also explicitly recommends *no* archive rename now, which avoids git history churn for dead files.

**Strongest point**  
“Underscores (`_`) are part of the `\w` regex character class … Standardizing on hyphens guarantees that word‑boundary (`\b`) parsing … will reliably extract IDs, dates, and topics without catastrophic backtracking or truncation.” This is a quantitative, integration‑predictability argument that matters at scale exactly the way I evaluate proposals.

**Weakest assumption**  
That a brief code freeze and immediate merge of all open PRs are operationally cheap and won’t introduce conflict with other solo‑operator pipeline work. If any open branch includes significant changes to the underscore‑named files, the rename PR creates a merge‑conflict minefield. The operator might not have the bandwidth to resolve them correctly, especially with ADHD. The mitigation is a freeze, but that freeze might stall other critical tasks.

**Hidden assumptions**
1. That the “integration blast radius” of archive files is near zero and will stay zero. Future tooling may scan `archive/` for historical patterns and then encounter mixed conventions, breaking assumption. True blast radius is low *now* but not guaranteed.
2. That the operator will reliably execute the freeze and merge step before the migration, without side‑tracking into other changes. ADHD makes the “brief freeze” fragile if something else interrupts.

**Overlooked risks**
- The risk of a merge conflict storm if the freeze fails to catch all in‑flight branches. The proposal acknowledges merge conflicts but assumes the freeze solves it — the real risk is that an unclosed branch with renamed files survives the freeze and then gets merged after, re‑introducing old underscore filenames. That branch would not be caught by the freeze and would create a post‑rename mix‑state.
- Archive deferral could cause the “universal convention” claim to be technically false for a long time if archive files are ever accessed by a script that expects hyphens. That’s a latent inconsistency.

---

## Proposal C

**Steelman**  
Correct if:
- The operator can execute the rename, link update, and CLI change in one commit without adding a pre‑commit hook immediately, and can rely on memory/discipline to keep the convention clean long enough to add the hook later.
- External references are indeed fewer than 5 and breakage is acceptable without any redirect stubs.
- The one‑time script works flawlessly, and the operator will later follow up to add the hook without forgetting (“immediate follow‑up” is ambiguous).

**Assessment** — **Partially Agree**  
I agree on hyphen everywhere, universal mandate, and CLI alignment. However, the proposal’s handling of enforcement is too loose for the stated ADHD constraint. It lists the pre‑commit hook only as a **risk mitigation** (“mitigate by adding a pre‑commit hook”), not as a mandatory action in the “Now” section. The timeline is murky. For a solo operator with ADHD, “add a hook later” is a trap; it will not happen until a failure reminds them. That creates an interval where manual discipline is required — violating our constraint.

**Strongest point**  
“Hyphen already appears in the two largest codebases … so the change normalizes the majority pattern rather than forcing the minority pattern.” It’s a clear operational‑cost argument.

**Weakest assumption**  
That the operator will create a pre‑commit hook as an immediate follow‑up without a scheduled, non‑negotiable trigger. If that assumption fails, the repo is vulnerable to new underscore filenames for an unbounded time.

**Hidden assumptions**
1. That “no external systems or published URLs currently hard‑link” is a safe default without a search. The proposal says “estimated <5 occurrences given internal audit focus” but offers no search method. A one‑shot `rg` across known external references (Slack links, issue bodies, wiki pages) was not prescribed.
2. That the operator will not hit muscle‑memory revert and create an underscore file *after* the migration but before the hook is installed. The mitigation (pre‑commit hook) is acknowledged but not scheduled, so the window exists.

**Overlooked risks**
- The link‑checker validation step might pass but still miss references in non‑`.md` files because the migration script only rewrote `.md` links. No search for cross‑format references is mentioned.
- If the CLI change is done in the same commit but the transcript files are renamed first, any running pipeline that expects `council_out_` filenames will break during the transition unless the CLI release is sequenced atomically — sequencing risk is not addressed.

---

## Proposal D

**Steelman**  
This is the exact right call if:
- The operator has sufficient focus to remember the new convention for 30 days without any automated gate, and then will reliably install a CI check exactly 30 days later.
- Archive files can remain mixed permanently without causing confusion in audits, because they are “legacy” and will only be renamed when touched.
- The one‑time migration script is run, validated, and merged without any ongoing enforcement; trust in human consistency for a month is acceptable.

**Assessment** — **Partially Agree**  
The core hyphen‑everywhere choice is solid. However, I **disagree with deferring CI enforcement 30 days**. For a solo ADHD operator, a 30‑day grace period without a hard block is precisely the window in which the first mistake happens and becomes permanent institutional memory. The claim “don’t add lint/CI enforcement in this PR. Ship the convention first” treats enforcement as optional polish, not as a load‑bearing part of the decision. A convention without a gate is a suggestion; suggestions die in this environment.

**Strongest point**  
“Hyphen wins the file‑count vote and the ecosystem vote simultaneously.” It’s a crisp quantitative rationale that aligns with minimizing migration scope.

**Weakest assumption**  
That the operator will not revert to underscore by muscle memory in the 30‑day gap. Given ADHD, probability of at least one slip is high. Without a CI error to catch it, that slip becomes the new precedent, and the rule is broken from the start.

**Hidden assumptions**
1. That the 30‑day follow‑up to add lint will actually be scheduled and executed, not lost in the whirlwind of other solo‑operator tasks. There’s no mechanism (e.g., issue, calendar reminder) baked into the proposal.
2. That the absence of CI lint is not a signal to a future contributor (or the operator in a tired state) that underscores are acceptable. The repo’s history will contain both styles; without automation, the convention is indistinguishable from legacy noise.

**Overlooked risks**
- In the 30‑day gap, auto‑generated files (e.g., another tool, a migrated script) could produce underscore‑named files that the operator doesn’t notice. Without lint, these persist.
- The archive “opportunistic” approach means that for an indeterminate future, `grep` queries expecting hyphens will silently miss archive files. That’s a quantitative failure mode: search completeness degrades.

---

## Revised Recommendation

My original stance, before the council round, was: **hyphen everywhere, rename all files in one atomic operation with link rewrites, universal mandate, CLI alignment, and immediate automated enforcement.** The proposals all converge on that core, confirming it’s the right hill to die on. I therefore **maintain my position** with a refined implementation plan that cherry‑picks the strongest enforcement details and hardens the weak spots exposed above.

### What to do now (revised)
1. **Separator**: Hyphen (`-`) is the sole canonical word separator in filenames and folder names. Rule: `[a-z0-9-]+\.md` for documents.
2. **Migration**: One atomic PR that:
   - Renames all 31 ADRs and ~15 CLI transcripts in `.dev-knowledge` to hyphen form.
   - Updates every internal reference across **all file types** (`.md`, `.yaml`, `.json`, `.ts`, `.py`, shell scripts, CI configs) via a script that scans for known filename patterns (not just a regex on `_` in links). I recommend a tool‑assisted pass with `rg` for literal old paths, not a blind regex.
   - Validates link integrity with a dedicated link‑checker that treats both relative and absolute repo paths.
   - Includes the **CI lint rule** in the same PR — a test that rejects any new filename containing `_` in the relevant paths. No separate PR, no 30‑day delay.
3. **Mandate**: Amend ADR‑34 to make hyphen the universal mandate for all repos, no recommendation exemptions.
4. **CLI output**: Change to `council-out-YYYYMMDD-HHMMSS-topic.md` and ship that code change synchronously with the rename PR, so no new transcripts with underscores are generated after the rename.
5. **Archive files**: Defer wholesale rename; replace with a **lint exception** that allows legacy `_` in `archive/` but logs a warning. When any archive file is touched in the future, rename it as part of that change. This preserves universal‑convention intent without pointless git churn.

### Why the other proposals didn’t change my mind
- Proposals A and B reinforce the need for immediate CI lint; I already had that. Proposal B’s regex‑word‑boundary argument adds quantitative weight, but it’s a supporting detail, not a directional shift.
- Proposal C’s lack of immediate enforcement is a showstopper for the ADHD constraint, so I disregard its timing approach.
- Proposal D’s 30‑day deferral is the exact kind of “we’ll fix it later” that kills conventions in solo‑operator ecosystems. I explicitly reject it and note that its author missed the failure mode where the operator’s muscle memory produces an underscore file the day after the migration, and without a gate it becomes the permanent exception.

### What breaks first and at what scale?
- **First failure mode**: A non‑`.md` file hardcoding an underscore path (e.g., a CI workflow) that the script missed. Likely impact: one broken link in an automated pipeline, caught only when that pipeline runs. Mitigation: scan all text files, not just `.md`, and run a post‑rename `rg` for any remaining `_` in known artifact paths. At the scale of ~46 files and maybe 100 references, a manual grep is cheap; automation ensures it.
- **Second failure mode**: Operator creates a new file with underscore because CI lint was delayed. Impact: re‑introduces inconsistency, undermines the mandate. Likelihood high with ADHD if lint deferred. Mitigation: CI lint in the same PR, effective immediately.

**Final answer**: Hyphen everywhere, atomic rename + link‑rewrite + lint, universal mandate, CLI aligned, archives handled opportunistically. This is the configuration that has the fewest human‑failure paths and the smallest blast radius over time.

*Latency: 256.11s | Tokens: 11964*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** A single, mechanically enforceable rule ("use only hyphen as word separator") plus one atomic scripted migration produces a permanently consistent, zero-decision state. For an ADHD solo operator this eliminates the exact recurring cognitive tax the audit exposed; ecosystem tooling and URL safety are free bonuses.

**Assessment:** Partially agree. The position is sound on the separator itself, but the proposal overstates the safety of a single automated pass across mixed file types and underestimates how quickly muscle-memory drift reappears without immediate linting.

**Strongest point:** The explicit recognition that any context-sensitive rule (hybrid) is guaranteed to decay for this operator profile.

**Weakest assumption:** That an automated script plus link-checker will catch 100 % of references in one run. If even one hard-coded path exists in a non-Markdown file or inside a code block, the "clean state" claim collapses.

**Hidden assumptions:** (1) No one outside the immediate repos will ever need stable permalinks to the old underscore names; (2) the operator will actually run the CI lint rule after the initial PR rather than treating it as optional future work.

**Overlooked risks:** Merge-conflict windows on active branches, and the possibility that the CLI change silently breaks downstream consumers who parse the literal `council_out_` prefix.

**Proposal B**

**Steelman:** Treating filename consistency as an integration and security boundary rather than a style preference. By making the rule regex-deterministic and CI-enforced, the proposal removes an entire class of parsing fragility that would otherwise accumulate across security scans, audits, and cross-repo scripts.

**Assessment:** Agree on the technical rationale for hyphens; disagree on the security-framing escalation. The claim that inconsistent separators constitute a meaningful security boundary is rhetorical overreach unsupported by the actual threat model.

**Strongest point:** Clear articulation that complex delimiter rules create fragile automation—stronger than A's readability argument.

**Weakest assumption:** That a code freeze can be instituted without operational cost. In a solo-ADHD environment, the coordination overhead of "close all PRs" is itself a manual-discipline requirement the proposal claims to eliminate.

**Hidden assumptions:** (1) The operator will treat the one-time migration script as production-grade code that must be versioned and tested; (2) no future tool or generated artifact will ever need underscores for external compatibility.

**Overlooked risks:** The "enterprise code-generation framework" signal is mentioned only as a revisit trigger; it is not costed as a realistic future constraint that could force a partial rollback.

**Proposal C**

**Steelman:** The simplest possible restatement of the decision—hyphen everywhere, one commit, no exceptions—maximizes the chance that the change actually ships instead of being diluted by scope creep or deferrals.

**Assessment:** Agree with the core action; partially disagree with the minimization of external-link risk. Dismissing "<5 occurrences" without measurement is an assumption, not data.

**Strongest point:** Explicit linkage between the CLI change and the human-readable convention in the same decision, preventing the exact inconsistency that triggered the council.

**Weakest assumption:** That the link-rewrite script can be written and validated in a branch without the operator needing sustained attention during the process itself.

**Hidden assumptions:** (1) The operator will remember to add the pre-commit hook after the migration rather than deferring it indefinitely; (2) "majority observed pattern" is a stable signal rather than an artifact of the current audit snapshot.

**Overlooked risks:** Future third-party tools that default to underscores (the exact scenario listed as low-likelihood) could reintroduce the problem at larger scale once the ecosystem grows beyond the current three repos.

**Proposal D**

**Steelman:** The proposal correctly counts total files across the ecosystem and concludes that migrating the minority underscore set is cheaper than the reverse. It also surfaces the long-term drift risk of leaving the CLI unaligned.

**Assessment:** Agree. D is the most quantitatively grounded of the four and the only one that explicitly weighs file counts across all repos rather than focusing on `.dev-knowledge` alone.

**Strongest point:** Recognition that recommendation-tier conventions reliably decay for a solo operator and that the universal mandate is therefore required, not optional.

**Weakest assumption:** That 46 renames is still "small" once git history, branch state, and any external bookmarks are included in the cost model.

**Hidden assumptions:** (1) The operator will actually schedule and execute the deferred CI-lint follow-up PR instead of letting it become another piece of technical debt; (2) numeric prefixes will never need a different separator for sortability or readability reasons.

**Overlooked risks:** The mid-migration interruption scenario is acknowledged but the mitigation (idempotent script) still requires the operator to notice and resume—an ADHD friction point the proposal does not address.

**Revised recommendation**

Maintain the hyphen-everywhere position. The four proposals converge on the correct separator because the audit data, ecosystem norms, and operator constraint all point there; no proposal supplied a credible defense of underscore or hybrid once the "no sustained manual discipline" rule is applied. The remaining variance is only in migration sequencing and enforcement timing. The decisive factor is that any carve-out (CLI, archive, child-repo recommendation, or forward-only) recreates the exact inconsistency the council was convened to eliminate. Execute the atomic rename + link rewrite + CLI update in one PR, then add the pre-commit/CI lint rule in the immediate follow-up commit rather than deferring it.

*Latency: 24.16s | Tokens: 7572*

## Synthesis (by openai, non-participant)

## Consensus

### Strong consensus
Most participants converged on:

1. **Canonical separator: hyphen everywhere**
   - `ADR-NN-topic.md`
   - kebab-case for folder names too
   - align human-readable docs naming across repos

2. **Migration approach: rename existing `.dev-knowledge` files now**
   - not forward-only
   - not permanent mixed state
   - update links in the same change

3. **Mandate scope: universal**
   - `.dev-knowledge` plus child repos
   - recommendation-only scope was widely treated as the reason inconsistency exists now

4. **CLI output should align**
   - `council-out-*` if hyphen wins
   - participants consistently rejected keeping CLI underscore output as a special case

### Was this real consensus or echoing?
This was **mostly evidence-backed consensus**, not pure groupthink.

Independent lines of reasoning repeatedly supported hyphens:

- **Observed ecosystem practice**: child repos and audit/handoff files already lean hyphen.
- **Operator constraint**: one-rule systems beat hybrid/contextual rules for a solo operator with ADHD.
- **Migration economics**: fewer files/repos need changing if hyphen wins.
- **Tooling / Markdown norms**: hyphens fit common web/Markdown slug conventions better than underscores.

There was some repetition and rhetorical inflation, especially around security/regex claims, but the core conclusion was reached through multiple valid arguments.

---

## Unresolved Disagreements

### 1. Enforcement timing: same PR vs follow-up
**Crux:** Is a convention valid if enforcement is delayed, or must enforcement ship immediately to satisfy the “no manual discipline” constraint?

- **Immediate enforcement side:** CI/lint must ship with the rename.
- **Deferred enforcement side:** rename first, add lint later.

**Stronger side:** **Immediate enforcement.**

**Why:**  
The operator constraint is explicit: solutions requiring sustained manual discipline are eliminated. A delayed lint step creates exactly such a window. Participants who initially favored deferral were effectively contradicted by others—and sometimes by their own risk analysis. The debate strongly supports that **enforcement is part of the decision, not a later improvement**.

---

### 2. Migration mechanics: regex/scripted rewrite vs AST-aware rewrite
**Crux:** Is a straightforward rename + search/replace + link check enough, or is AST-aware rewriting needed to avoid corrupting references?

- **Simple scripted migration side:** feasible and proportionate for ~31–46 files.
- **AST-aware side:** regex-based rewriting risks missing frontmatter, HTML, code blocks, or non-Markdown references.

**Stronger side:** **Use targeted scripted rename plus exhaustive verification, not necessarily full AST rewriting.**

**Why:**  
The AST-aware caution is valid, but no one demonstrated that this repo actually has enough Markdown complexity to justify heavier tooling. The stronger argument was not “regex is perfect”; it was “the migration is small enough to verify exhaustively.” The right lesson is:
- don’t do blind global regex rewriting,
- but also don’t over-engineer.

A controlled mapping-based rename plus repository-wide checks is the best-supported middle path.

---

### 3. Archive handling: sweep now vs defer/opportunistic
**Crux:** Does “universal convention” require renaming legacy archive files immediately, or can archives be exempted temporarily?

- **Rename archives now side:** exceptions undermine universality and create future ambiguity.
- **Defer archives side:** low-value churn if archives are inactive.

**Stronger side:** **Rename archives now if they are in scope of the ecosystem convention and the rename cost is modest.**

**Why:**  
The best anti-deferral argument was that “opportunistic later” for archives usually means “never,” which recreates mixed-state evidence in the codebase. Since there is no budget constraint and the stated goal is universal consistency, archive carve-outs are weak unless there is a specific compatibility dependency. None was presented.

That said, this was the least decisively resolved disagreement because the actual archive inventory and dependency surface were not presented.

---

## Argument Quality Assessment

### Best-reasoned proposals
The strongest proposals shared these traits:

- tied their recommendation to the **operator constraint**
- used the **audited current-state evidence**
- treated **recommendation-only scope** as a demonstrated failure mode
- rejected hybrid rules on cognitive-load grounds
- recognized that **CLI output is not a harmless exception**

The most persuasive reasoning came from proposals that combined:
- migration cost minimization,
- ecosystem alignment,
- and enforceability.

### Weaker reasoning
Some arguments were weaker because they:
- overstated security implications without evidence from this ecosystem,
- assumed perfect automation,
- or deferred enforcement despite admitting drift risk.

### Single strongest argument in the debate
**The hybrid rule is structurally incompatible with the operator constraint.**

This was the clearest and most durable argument. It directly connects the decision to the explicit elimination criteria: a context-sensitive naming rule will not survive for a solo operator with ADHD. That argument is stronger than style preference, repo-majority counting, or aesthetics.

### Single weakest argument in the debate
**The stronger security framing around regex/command injection/ReDoS from mixed separators.**

There is a kernel of truth that simpler parsing is better, and that `_` vs `-` affects regex behavior. But the debate did not present evidence that this ecosystem has hostile-input parsing or security-critical filename handling. As used, this was mostly rhetorical overreach.

---

## Blind Spots

### 1. Foldername evidence was barely examined
The question asks for **filename / foldername** separator across the ecosystem, but the debate focused overwhelmingly on Markdown filenames. It assumed the same answer for folders, which is likely right, but under-argued.

### 2. No one established the real external-link surface
Participants repeatedly assumed there are few or no external references to current underscore paths. That may be true, but it was not demonstrated. This matters for whether redirect stubs or compatibility notes are warranted.

### 3. The actual inventory outside `.dev-knowledge` was not fully quantified
Several arguments referenced “100+ hyphen files” or “majority pattern,” but counts were approximate. The debate had enough to choose direction, but not enough to scope migration precisely across all child repos and archives.

### 4. Enforcement mechanism details were underspecified
“Add CI/lint” was widely endorsed, but the debate did not settle:
- exactly which paths are in scope,
- whether folders and files are both checked,
- whether only Markdown is checked,
- how generated artifacts are handled,
- what exceptions, if any, exist.

### 5. Date/time format was intentionally deferred, but this leaves a naming rule gap
Participants wisely avoided reopening date-format questions, but the resulting canonical rule is still incomplete unless it explicitly says separator policy is independent of date token shape.

---

## Recommended Decision

### Decision
Adopt **hyphen everywhere** as the canonical separator for filenames and foldernames across the Dev ecosystem.

Choose:

- **Q1:** A — Hyphen everywhere
- **Q2:** A — Rename existing `.dev-knowledge` files now
- **Q3:** A — Universal mandate
- **Q4:** A — Align Council CLI output to hyphen form

### Rationale
This is the best-supported path because it wins on the three arguments that mattered most:

1. **Operator-fit**
   - One unconditional rule is the only option consistent with the ADHD/no-manual-discipline constraint.
   - Hybrid rules and permanent legacy exceptions fail this test.

2. **Current-state fit**
   - Hyphen already dominates outside the ADR-34 example and current `.dev-knowledge` ADR/transcript naming.
   - Choosing underscore would force the broader ecosystem to conform to a weaker, less-adopted pattern.

3. **Durability**
   - Recommendation-only scope already failed.
   - CLI carve-outs would immediately recreate inconsistency.
   - Forward-only migration institutionalizes mixed state.

### Strongest objections, and why they don’t win

#### Objection: underscore is current ADR-34 spec and existing `.dev-knowledge` practice
True, but the debate showed that current local spec/practice is already inconsistent internally and out of step with child repos. Existing inconsistency is not a reason to preserve it.

#### Objection: migration could miss links
Also true. But this argues for careful execution, not against the convention. The file count is small enough to support an atomic, verified migration.

#### Objection: archive/history churn may not be worth it
This is the best objection to a full sweep. If archive files truly have zero practical surface area, deferral could be tolerable. But based on the operator’s universal-convention framing, the stronger decision is to avoid visible exceptions unless dependency analysis proves they are needed.

### Final judgment
The debate is sufficiently conclusive to decide now. No further deliberation is needed to choose the separator. The only remaining uncertainty is implementation detail, not policy direction.

---

## Risks

1. **Broken internal references after rename**
   - Risk: Markdown links, frontmatter, scripts, or config files may still point to old paths.
   - Mitigation:
     - use an explicit old→new filename mapping,
     - scan all text-like files, not just `.md`,
     - run link validation after rename,
     - grep for old names before merge.

2. **CLI rename breaks downstream automation**
   - Risk: scripts or globs may depend on `council_out_`.
   - Mitigation:
     - search all managed repos for `council_out_`,
     - update those references in the same change set,
     - release CLI change synchronously with migration.

3. **Mixed state reappears immediately**
   - Risk: operator or generators create underscore names after the decision.
   - Mitigation:
     - ship CI enforcement in the same PR,
     - optionally add pre-commit hooks as convenience, but CI is authoritative.

4. **External bookmarks or notes break**
   - Risk: old underscore paths may exist in personal tools, issues, or notes.
   - Mitigation:
     - inventory references before merge if practical,
     - if nontrivial, provide a migration note or compatibility mapping,
     - only add redirect stubs if actual breakage is discovered.

5. **Archive exception undermines the rule**
   - Risk: deferred archive renames create a visible “sometimes underscores” precedent.
   - Mitigation:
     - prefer renaming archives in the same sweep if scope is manageable,
     - if not, document the temporary exception explicitly and time-box its cleanup.

---

## Action Items

1. **Amend ADR-34**
   - Replace underscore example with hyphen canonical form.
   - Upgrade child-repo guidance from recommendation to mandate.
   - State explicitly that the separator rule applies to both filenames and foldernames.

2. **Define the canonical rule**
   - Example:
     - `ADR-27-scope-tagging.md`
     - `2026-05-11-cross-repo-pattern-audit.md`
     - `council-out-YYYYMMDD-HHMMSS-topic.md`
   - Clarify that date-token format questions are separate from separator policy.

3. **Prepare a deterministic rename map**
   - List every old path and new path before making changes.
   - Include ADRs, transcripts, and any in-scope archive/docs files.

4. **Execute one atomic migration PR**
   - Rename files/folders.
   - Update links/references using explicit mapping, not blind replacement.
   - Include CLI output format change in the same PR.

5. **Validate thoroughly before merge**
   - Search repo for all old filenames.
   - Search for `council_out_`.
   - Run markdown link checks.
   - Scan non-Markdown text/config files for stale references.

6. **Add CI enforcement in the same PR**
   - Fail builds on underscore-containing in-scope filenames/foldernames.
   - Scope should include all governed repos/paths, including generated docs artifacts if applicable.

7. **Optionally add local guardrails**
   - Pre-commit hook or helper script for convenience.
   - But do not rely on local hooks instead of CI.

8. **Decide archive handling explicitly before merge**
   - Preferred: rename archives now if the set is manageable.
   - If deferred: document the exception, why it exists, and by when it will be removed.

9. **Publish a short migration note**
   - Summarize the rule in one sentence.
   - Note that old underscore examples are obsolete.
   - Mention CLI filename change so future transcript generation matches policy.
