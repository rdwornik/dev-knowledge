# Git-Native Delivery Telemetry and AI Model Attribution for an LLM Coding Fleet

## TL;DR
- **Build both, git-first, in this order:** a weekly text digest carrying 6-8 numbers computed purely from `git log`/tags, and an `Assisted-by:`/`Model:` commit-trailer convention enforced by a `commit-msg` hook. `Assisted-by:` — not `Co-authored-by:` — is now the cross-ecosystem standard (Linux kernel, Fedora, LLVM, OpenTelemetry, Rocky Linux, OpenInfra all published it in 2025-2026), so adopt it rather than inventing a schema.
- **Most of what the operator wants is git-derivable today.** Deployment frequency (merges/tags to main), lead time (branch first-commit → merge timestamp), revert/rework rate (revert-commit detection + fix-follows-feature), and per-model share (trailer parsing) all come from history alone. Change-failure rate and time-to-restore need an external incident signal, so approximate them with revert rate and flag the gap.
- **Instrument minimally and watch quality, not just speed.** Recent primary research converges on one message: AI raises throughput but degrades stability/maintainability. Google's 2024 DORA one-pager estimated a 25% rise in AI adoption is associated with a 7.2% *decrease* in delivery stability; GitClear (Feb 2025) measured code churn roughly doubling (≈3.3% pre-AI → 7.1% in 2025) and duplicated blocks rising ~8x in 2024. A fleet digest must pair a throughput number with a rework/churn number or it will mislead.

## Key Findings

1. **Framework landscape.** DORA (now five metrics), SPACE (five human/system dimensions), DevEx, and the 2024 DX Core 4 (Speed, Effectiveness, Quality, Impact) are the credible frameworks. For a git-only, no-survey, no-dashboard instrument, DORA's throughput metrics and derived rework signals are the only fully automatable pieces; SPACE/DevEx/DX Core 4 lean heavily on surveys and external systems.
2. **DORA on AI (primary).** The 2024 report (39,000+ respondents) found AI adoption improved individual productivity, perceived code quality, and documentation but *worsened* software delivery throughput and stability. The 2025 "State of AI-assisted Software Development" report (~5,000 respondents, 90% AI adoption) reversed the throughput finding — AI now correlates with *higher* throughput — but AI *still increases delivery instability*. DORA's own framing: AI is an "amplifier"/"mirror and multiplier." DORA added a fifth metric, deployment rework rate, in 2024.
3. **Git-native tooling exists but is uneven.** Google's Four Keys is the reference implementation but heavyweight (BigQuery/Cloud Run/webhooks). Middleware (open-source DORA platform) is actively maintained. git-quick-stats is maintained and simple. Hercules/gitbase (src-d/source{d}) are effectively abandoned. For a text-digest target, raw `git log` plumbing beats any of them.
4. **AI attribution has consolidated on `Assisted-by:`.** Claude Code stamps `Co-Authored-By: Claude <noreply@anthropic.com>` (now with model name) by default; VS Code/Copilot flip-flopped a `git.addAICoAuthor` default through 2026; Aider appends `(aider)` to author/committer names by default; Codex CLI and Gemini CLI add nothing by default. But every major open-source foundation that wrote a policy chose `Assisted-by:` (keeps the human as sole author/DCO signer). The Linux kernel prescribes `Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]` and forbids AI `Signed-off-by`.
5. **Quality is measurable from git and it's deteriorating under AI.** GitClear's multi-year analysis (211M+ changed lines) found "moved"/refactored code collapsing (24.8% of changed lines in 2021 → 9.5% in 2024), copy-paste exceeding moved code for the first time in 2024, duplicate blocks up ~8x, and churn roughly doubling. These are git-derivable proxies the digest should carry.

## Details

### 1. Delivery-telemetry frameworks and git-derivability

**DORA — five metrics (dora.dev).** Per DORA's own history page, the metrics evolved as: deployment frequency and change lead time (throughput); change fail rate and failed deployment recovery time (formerly MTTR, renamed 2023); and **deployment rework rate**, added in the 2024 report as a third stability signal — "the ratio of deployments that are unplanned but happen as a result of an incident in production." DORA also moved failed-deployment-recovery-time to *throughput* framing in 2024.

**SPACE (Forsgren et al., 2021; GitHub/Microsoft/Univ. Victoria).** Five dimensions: Satisfaction & well-being, Performance, Activity, Communication & collaboration, Efficiency & flow. Only *Activity* is meaningfully git-derivable; the rest require surveys.

**DevEx (2023) and DX Core 4 (DX, Nov 2024).** DX Core 4 unifies DORA+SPACE+DevEx into Speed, Effectiveness, Quality, Impact; each dimension has one key + three secondary metrics, and it deliberately includes self-reported metrics (perceived delivery rate, perceived software quality) plus the proprietary Developer Experience Index (DXI). Because it depends on surveys and a proprietary index, it is not a git-only instrument.

**What the DORA reports say about AI (primary):**
- *2024 report (Google DORA one-pager, 39,000+ respondents):* 81% of respondents say their company has shifted resources into developing AI; 67% report AI helps improve their code; 39% reported having little or no trust in AI. The report's modeled associations for a **25% increase in AI adoption**: **+7.5% documentation quality, +3.4% code quality, +3.1% code-review speed, +1.3% approval speed, −1.8% code complexity — but −1.5% delivery throughput and −7.2% delivery stability.** That stability hit is the headline caution for an AI fleet.
- *2025 report (State of AI-assisted Software Development, Google Cloud, ~5,000 respondents):* AI adoption surged to 90% (a 14-point rise from 2024); median ~2 hours/day with AI; 30% report little/no trust in AI-generated code. DORA's "Balancing AI tensions": "higher AI adoption is associated with an increase in **both** software delivery throughput **and** software delivery instability. AI's primary role in software development is that of an amplifier." Seven team archetypes (from "Harmonious high-achievers" ~20% to "Legacy bottleneck" ~11%) and a seven-capability AI model (clear AI stance, healthy data ecosystems, AI-accessible internal data, strong version-control practices, small batches, user-centricity, quality internal platform).

**Git-derivability table:**

| Metric | Framework | Purely git-derivable? | How / why not |
|---|---|---|---|
| Deployment frequency | DORA | Partial→Yes | Count merges to main, or tags matching release pattern; exact only if "deploy" == "merge/tag to main" |
| Lead time for changes | DORA | Partial | Branch first-commit → merge-commit timestamp; ambiguous with squash/rebase and no CI/prod signal |
| Change fail rate | DORA | No (approximate) | Needs incident/CI link; approximate via revert rate |
| Failed-deployment recovery time | DORA | No | Needs incident open/close timestamps |
| Deployment rework rate | DORA (2024) | Partial (approximate) | Needs "unplanned/incident-driven" label; approximate via fix-follows-feature + reverts |
| Activity (commits, PRs) | SPACE | Yes | Direct from log |
| Satisfaction, Communication, Efficiency | SPACE/DevEx | No | Surveys |
| Speed (Core 4) | DX Core 4 | Partial | Overlaps DORA throughput |
| Quality/Effectiveness/Impact (Core 4) | DX Core 4 | No | Surveys + DXI (proprietary) |
| Per-model contribution share | (fleet-specific) | Yes | Parse `Assisted-by:`/`Model:` trailers |
| Churn / rework / duplication | GitClear-style | Yes | Diff analysis over recent history |

### 2. Git-native measurement tools and pitfalls

**Tool landscape / maintenance:**
- **Google Four Keys (`dora-team/fourkeys`)** — reference implementation for the four keys; ETL via webhooks → BigQuery → dashboard; requires a billed Google Cloud project. Powerful but far too heavy for a text-digest target, and it is deployment/incident-webhook oriented, not pure-git.
- **Middleware (`middlewarehq/middleware`)** — actively maintained open-source DORA platform (Docker-deployable). Good if you later want a UI.
- **Apache DevLake / OpenDORA (Backstage plugin)** — listed on dora.dev/resources; aggregates GitLab/GitHub/Jira/Jenkins. Heavy.
- **git-quick-stats** — maintained, simple shell tool over `git log`; good for exploration, not deployment metrics.
- **Hercules / gitbase / go-git (src-d / source{d})** — the company is defunct; Hercules' last substantive activity was ~2020. Treat as abandoned.
- **git-of-theseus, GitHammer, gitstats, git_stats** — niche/legacy line-history visualizers; mostly stale.
- **GitClear, LinearB, Swarmia, Sleuth, Faros** — commercial; some publish open components/plugins but core is SaaS.

**Recommendation:** For a small fleet targeting a committed text digest, prefer **raw `git` plumbing in a shell/Python script** run weekly (optionally in CI), not a platform. Graduate to Middleware only if you later want dashboards.

**Known pitfalls of git-only measurement:**
- **Squash merges destroy granularity:** the whole branch collapses to one commit, erasing per-commit lead-time signal, bisect precision, and (critically for this fleet) any per-commit `Assisted-by:` trailers unless they are consolidated into the squash message. If per-model attribution matters, avoid squash-merging away trailers.
- **Rebase rewrites timestamps/SHAs:** author vs. committer dates diverge; lead-time calculations must pick one deliberately (author date survives rebase; committer date reflects landing).
- **Lead-time definition ambiguity:** "first commit on branch," "PR open," and "merge" give very different numbers; pick one and document it.
- **Revert detection is heuristic:** `git revert` writes "This reverts commit <sha>" which is greppable, but manual reverts/hotfixes don't; and rebase/merge-train patch-ID dedup can silently drop reverted-then-reintroduced commits (a documented GitLab merge-train failure mode).
- **Author identity noise:** agents commit under the operator's identity or a bot identity; contribution graphs mis-attribute.

### 3. AI code-attribution conventions — state of the art (2025-2026)

**Default behavior per tool (exact formats):**

| Tool | Default attribution | Exact format | Source |
|---|---|---|---|
| **Claude Code** | ON | `Co-Authored-By: Claude <noreply@anthropic.com>` (recently includes model, e.g. `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`) + PR footer "Generated with Claude Code"; controlled via `attribution` setting in settings.json (`includeCoAuthoredBy` deprecated) | Claude Code docs; multiple 2026 writeups |
| **GitHub Copilot / VS Code** | Flipped repeatedly in 2026 | `Co-authored-by: Copilot <copilot@github.com>` / `<223556219+Copilot@users.noreply.github.com>`; setting `git.addAICoAuthor` (off / chatAndAgent / all). Default was off, briefly flipped to `all` in 1.117/1.118 causing backlash, then reverted | microsoft/vscode issues #314311, #313931, #310226 |
| **Cursor** | Attribution-on (version-dependent) | Body/trailer attribution; format varies | Secondary (explainx.ai, 2026) |
| **Aider** | ON (name-based) | Appends `(aider)` to git author + committer name by default (`attribute-author`/`attribute-committer` = True). Optional trailer (off by default, `--attribute-co-authored-by`): `Co-authored-by: aider (<model_name>) <noreply@aider.chat>` | aider.chat/docs/git.html; Aider-AI/aider issue #4226 |
| **OpenAI Codex CLI** | OFF | No default trailer; opt-in only. When enabled: `Co-authored-by: Codex <noreply@openai.com>` | openai/codex discussion #9449, PR #11617, commit_attribution.rs |
| **Gemini CLI** | OFF | No default attribution | google-gemini/gemini-cli discussions #11447, issue #12419 |

**The emerging model-level standard — `Assisted-by:`.** GitHub's `Co-authored-by:` renders extra avatars and counts in contribution graphs; it was designed for *humans* and implies legal personhood the AI cannot hold. The ecosystem has therefore converged on **`Assisted-by:`**:
- **Linux kernel** (`docs.kernel.org/process/coding-assistants.html`): prescribes `Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]`; example `Assisted-by: Claude:claude-3-opus coccinelle sparse`; "AI agents MUST NOT add Signed-off-by tags. Only humans can legally certify the Developer Certificate of Origin (DCO)." Optional `[TOOL]` slots are for specialized analysis tools (coccinelle, sparse, smatch, clang-tidy) — "Basic development tools (git, gcc, make, editors) should not be listed." Merged Dec 2025 (Sasha Levin / Jonathan Corbet), originating from Levin's July 2025 RFC after an undisclosed AI patch landed in kernel 6.15.
- **Fedora** AI-Assisted Contributions Policy (approved Oct 2025): recommends `Assisted-by:` (e.g., `Assisted-by: generic LLM chatbot`, `Assisted-by: ChatGPTv5`); disclosure required "when the significant part of the contribution is taken from a tool without changes."
- **Rocky Linux:** modeled on Fedora; recommends `Assisted-by:`.
- **OpenTelemetry** genai policy: recommends `Assisted-by:` with model; examples verbatim `Assisted-by: ChatGPT 5.2` and `Assisted-by: Claude Opus 4.5` (disclosure is "appreciated," not mandated).
- **LLVM:** recommends `Assisted-by:`, mandates human-in-the-loop, bans autonomous agent actions.
- **Apache Software Foundation:** recommends a `Generated-by:` token for a machine-parsable Tooling-Provenance file.
- **OpenInfra:** adopts both — `Assisted-by:` default, `Generated-by:` for substantial AI generation.
- **Bans:** QEMU declines AI-generated code; Gentoo Council (2024) forbids NL-AI-assisted contributions; NetBSD presumes AI code "tainted"; curl shut its bug bounty after AI-report spam.

**Tooling to emit/enforce/parse:**
- Emit: `git commit --trailer "Assisted-by: ..."` (routes through `git interpret-trailers`, added in git 2.32/2021 — the correct way vs. concatenating text).
- Enforce: `commit-msg`/`PreToolUse` hooks (the `bcmyguest/assisted-by` Claude Code plugin blocks commits with wrong attribution; the `fluxcd` `commit-assisted-by` skill adds `Assisted-by: <agent-name>/<model-id>`).
- Parse/report: `git log --format='%(trailers:key=Assisted-by,valueonly)'`; `git interpret-trailers --parse`; `git log --grep="Assisted-by:"`. GitHub and GitLab both parse trailers (GitLab uses them for changelogs). Git *notes* (`refs/notes/...`) are an alternative for post-hoc, SHA-stable metadata.

**Legal/provenance angle (brief).** Attribution matters for (a) license compliance — AI can emit verbatim licensed snippets that dependency scanners miss because inlined code has no package/version/CVE; (b) SBOM-adjacent provenance / emerging "AI-BOM" expectations and the EU AI Act's high-risk documentation/audit-trail provisions (taking effect Aug 2026); (c) audit trails — "without attribution there is no way to identify AI-generated code in a future audit," and it must be enforced at commit time, not left to guidelines. Keep signature (DCO `Signed-off-by:` = "who stands behind this," human-only) separate from provenance (`Assisted-by:` = "what went into this").

### 4. Quality signals from git — GitClear findings with dates

GitClear's reports (CEO Bill Harding) analyze structured diff operations (added/deleted/updated/moved/copy-pasted/find-replaced/churned):
- **AI Copilot Code Quality (Feb 2025), 211M changed lines, 2020-2024:** "Moved" (refactored) code fell from **24.8% of changed lines in 2021 to 9.5% in 2024**; copy/pasted code rose from **8.4% to 12.3%**, and in 2024 **copy/pasted code exceeded moved code for the first time in the five-year dataset**; "the number of code blocks with 5 or more duplicated lines increased by 8 times during 2024"; short-term churn (code revised within ~2 weeks) climbed from the pre-AI baseline toward ~5.5-7.9% depending on the cut.
- **Prior 2024 report:** 153M+ lines, 2020-2023; first flagged churn/moves/duplicates as the three red flags, projecting churn could double vs. 2021.
- **2026 "Maintainability Gap":** block duplication climbed from 40.3 to 73.0 per million changed lines (2023→2026 YTD, +81%); moved code fell to ~3.8% YTD 2026; **code churn rose from a pre-AI baseline of ~3.3% to 5.7% in 2024 and 7.1% in 2025 — a doubling over two years.** GitClear also reported (Jan 2026) heavy AI users out-produce non-users ~4-10x, but most of that gap predated AI (a ~25% self-vs-self velocity gain).

**Git-derivable quality proxies:** revert rate (grep `git revert`), fix-follows-feature (commits whose message references/`Fixes:` a recent commit), churn/rework (lines rewritten within N days of introduction), duplication (diff analysis). These are exactly the "instability" signals DORA and GitClear both say AI inflates.

### 5. Minimal-instrumentation design patterns

Practitioner consensus (Gitmore, GitDailies, Faros, DORA guides): start with one throughput metric, add lead time, then approximate stability; a spreadsheet or a shell script is enough at small scale; resist comparing to elite/high benchmarks early. Per-AI-model contribution breakdowns are still emerging prior art — GitHub added per-model token breakdowns to Copilot billing reports (Aug 2026), and third parties (Exceeds AI, custom git-hook scripts) parse trailers for per-tool analytics — but there is no turnkey per-model git report, which is why a trailer + parse script is the right build.

## Recommendations

**Stage 0 (this week) — adopt the trailer schema.** Standardize on `Assisted-by:` for AI provenance and keep the human operator as the sole `Signed-off-by:` (DCO) signer. Recommended fleet schema, following the kernel's `AGENT_NAME:MODEL_VERSION` shape but split for easy parsing:

```
Assisted-by: <agent>:<model-version>        # e.g. claude-code:claude-sonnet-4-6
Model: <model-version>                        # redundant, single-key for fast per-model rollups
Lane: <worktree/lane id>                       # your parallel-lane identifier
```

Configure each agent to emit it: Claude Code via `attribution.commit` in settings.json (set it to your `Assisted-by:` line and disable the default `Co-Authored-By`); Aider via `--attribute-co-authored-by` off + a commit template; Codex/Gemini/Cursor via `AGENTS.md`/`GEMINI.md`/rules that instruct the trailer. **Do not rely on tool defaults** — they disagree and change between releases.

**Stage 1 — enforce at commit time.** Add a `commit-msg` hook (tracked via `git config core.hooksPath .githooks`) that (a) blocks any commit lacking a human `Signed-off-by:` on the merge to main, and (b) if the committer is an agent identity, requires a well-formed `Assisted-by:`/`Model:` trailer. Reuse the `bcmyguest/assisted-by` hook or the fluxcd skill rather than writing from scratch. Skip enforcement on merge/rebase/cherry-pick (guard on `MERGE_HEAD`).

**Stage 2 — ship the weekly git-only digest.** A committed `DIGEST.md` (regenerated weekly by a script) carrying **7 numbers**:

1. **Merges to main** (deployment-frequency proxy): `git log --first-parent --merges --since="7 days ago" --oneline main | wc -l` (or count tags: `git tag --sort=-creatordate` filtered by date).
2. **Median lead time** (branch first-commit → merge): for each merge, diff `git log --format=%at` between the merge commit and the branch's earliest commit; take the median. Document the definition; prefer author date to survive rebases.
3. **Revert/rework rate** (stability approximation): `git log --since="7 days ago" --grep="^Revert" --oneline | wc -l` over total merges, plus fix-follows-feature via `--grep="Fixes:"`.
4. **Net vs. churned lines** (maintainability): compare added lines to lines rewritten within 14 days (`git log --numstat` windowed) — your local GitClear-style churn proxy.
5. **Per-model commit share:** `git log --since="7 days ago" --format='%(trailers:key=Model,valueonly)' | sort | uniq -c | sort -rn`.
6. **Per-lane throughput:** same, keyed on `Lane:`.
7. **Commits missing attribution** (hygiene/audit): count agent-identity commits with no `Assisted-by:` trailer — should trend to zero once the hook is live.

Pair every throughput number (1, 6) with a stability/quality number (3, 4) in the digest so speed is never read alone — the central lesson of the 2024-2026 DORA and GitClear data.

**Stage 3 — only if needed:** stand up Middleware (maintained OSS) for dashboards, or Four Keys if you add real deployment/incident webhooks. Add true change-fail-rate and recovery-time only once you have an incident source (even a manual `incidents.csv`).

**Thresholds that change the plan:** if squash-merging is unavoidable, move attribution to the *merge* message and accept coarser lead-time; if the fleet exceeds ~10 contributors/agents or you need line-level (not commit-level) AI attribution, graduate from trailers to a line-attribution tool (e.g., git-notes-based "Git AI") and a real platform; if revert/churn rate climbs materially week-over-week, tighten pre-commit gates and human review before adding more agent lanes.

## Caveats
- **Change-fail-rate and time-to-restore are NOT purely git-derivable** — the digest's revert/rework numbers are approximations; label them as such.
- **Squash merges and rebases** can erase per-commit trailers and distort lead time; the trailer strategy assumes you preserve commit granularity or consolidate trailers into merge messages.
- **Attribution is unauthenticated** — anyone/any tool can write any trailer; it is a transparency/telemetry signal, not a cryptographic guarantee. Line-level accuracy and 30-60-day-latent debt are beyond commit-trailer parsing.
- **Tool defaults are volatile:** Claude Code changed its trailer format/model-name behavior across releases; VS Code/Copilot flipped `git.addAICoAuthor` defaults twice in 2026 (and a bug briefly attributed non-Copilot code to Copilot). Pin your own convention and enforce it.
- **DORA and GitClear are different evidence types:** DORA is survey-based correlation (self-reported); GitClear is diff-measurement of real repos. Both point the same direction on AI instability, but neither proves causation for your specific fleet — measure your own churn/revert baseline. The DORA one-pager figures (e.g., −7.2% stability per 25% AI-adoption increase) are modeled associations, not deterministic effects.
- **The kernel `Assisted-by:` example uses `Claude:claude-3-opus`; the `Assisted-by: Claude Opus 4.5` form is OpenTelemetry's** — pick one delimiter convention (`agent:model`) and apply it fleet-wide. The kernel-policy merge date (Dec 2025) is from secondary reporting; the trailer *format* is confirmed from the primary kernel doc.