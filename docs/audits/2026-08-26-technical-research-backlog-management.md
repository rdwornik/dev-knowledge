# Managing a Large Backlog for Human-Plus-AI-Agent Software Teams

## TL;DR
- **Keep the structured source (per-task files + manifest) but stop treating the giant `BACKLOG.md` as the artifact people read.** The decisive problem is not the storage medium — it is that a flat 212-row file collides on merge and defeats both human and LLM attention. Adopt a git-native, dependency-aware model (either your own view layer done properly, or the Beads/`backlog.md` pattern) whose default surface is a *ranked, short "ready/next" view*, not the full inventory.
- **Prune aggressively to a defensible ~40–60 active items.** Practitioner consensus and the empirical stale-bot literature converge: large backlogs are an anti-pattern, silence rarely means value, and "if it matters it will be re-filed." Move everything not slated for the next ~2–3 windows to an archived "icebox," keeping the git history as the safety net.
- **A net-negative ledger is a sound *diagnostic* but a dangerous *target*.** It is the backlog analogue of an SRE error budget / Kanban WIP limit. Keep it as a visible signal with graduated responses; never let "banked=0" force closing real work or suppress filing. Instrument it with flow metrics (aging WIP, throughput) so it cannot become a pure proxy metric.

## Key Findings

1. **The medium is less important than the shape.** Markdown-in-repo, git-native trackers, and GitHub Issues all work; the failure the user reports (a file that "looks the same, huge, huge, huge") is a *flat-list-plus-merge-collision* failure, not a Markdown failure. Every credible 2025–2026 tool in this space (Beads, `backlog.md`, git-bug, Spec Kit) has independently converged on the same three design commitments: one file/object per item, dependency edges, and a generated "what's ready now" query.

2. **The merge-collision problem is solved by per-item files + append-only logs + non-sequential IDs — exactly the opposite of a single regenerated file with a `generated_sha256`.** The user's design guarantees collisions; the fix is architectural, not procedural.

3. **LLM context degradation is real and quantified.** Feeding a 212-row file into an agent wastes tokens and triggers "lost in the middle" degradation; the winning pattern is a small, ranked, queryable slice.

4. **Aggressive pruning is well supported; auto-close bots are not a clean win.** Independent empirical evidence shows stale bots clear backlog in the short term but reduce contributor engagement and can bury valid work. The lesson for a solo/agent operator differs from open-source, but the caution transfers: prune by human judgment on a ranked view, exempt real bugs, and archive rather than delete.

5. **A net-negative/closure-budget discipline mirrors SRE error budgets and Kanban WIP limits — proven ideas with well-documented gaming failure modes.**

## Details

### Area 1 — File-based versus tracker-based backlogs

The 2025–2026 "docs/issues-as-code" movement is real and growing, and Markdown remains the lingua franca that both humans and LLMs read natively. The strongest articulation of *why* keep work in the repo comes from tools built for exactly the user's situation. `backlog.md` (MrLesk) frames it precisely: "AI agents can now produce more plausible code in an hour than you can carefully read in a day. The bottleneck is no longer writing code. It's your attention." Its answer is one plain `.md` file per task under `backlog/tasks/` with YAML frontmatter, a zero-config CLI, and an optional Kanban web UI — "human-readable, git-diffable, and offline-capable." `agilemarkdown` makes the git-merge argument explicitly: "Concurrent edits across different items merge cleanly, attribution comes from the git author of each commit."

The critical, load-bearing distinction: **per-item files merge; one regenerated aggregate file does not.** The user's `BACKLOG.md` is generated with a `generated_sha256` that "changes on every edit, so two agents filing one row each collide in a way git cannot auto-merge." This is the single most important architectural fact in the whole engagement. Both `backlog.md` and the file-based approaches survive concurrent writes precisely because each item is its own file and the aggregate view is *never* the source of truth — it is disposable and regenerated on read.

Markdown-task standards worth knowing: **todo.txt** and **TaskPaper** (lightweight line formats); **GitHub Flavored Markdown task lists**; and the **`tasks.md` convention** now standardized across spec-driven tools. GitHub **Spec Kit**'s `/speckit.tasks` command "produces a tasks.md file with task breakdowns organized by user story, dependency ordering ..., parallel execution markers tagged [P], exact file path specifications, and checkpoint validation between phases." Amazon **Kiro** generates `requirements.md` (EARS notation), `design.md`, and `tasks.md`, and "builds a dependency graph of the tasks in your tasks.md and groups independent tasks into waves." Note the scale mismatch: these `tasks.md` files are *per-feature* (dozens of lines), never a 212-row program-wide backlog. That is a signal: **the industry does not put hundreds of items in one Markdown file.**

**How large can a Markdown backlog get before it breaks?** For humans: practitioner guidance treats "hundreds of items" as already an anti-pattern (Scrum Alliance lists "the backlog has grown to hundreds of items" and "you don't want to show anyone the list" as the diagnostic signs). For LLMs: the "lost in the middle" study (Liu et al., *Transactions of the ACL* vol. 12, 2024, DOI 10.1162/tacl_a_00638) found "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models" — a U-shaped curve with >30% degradation, replicated across GPT-3.5-Turbo, GPT-4, Claude 1.3, LongChat-13B, MPT-30B, and Cohere Command. Chroma's "Context Rot" technical report (Hong, Troynikov & Huber, July 14, 2025) evaluated 18 LLMs "including the state-of-the-art GPT-4.1, Claude 4, Gemini 2.5, and Qwen3 models" and found "models do not use their context uniformly; instead, their performance grows increasingly unreliable as input length grows." A Beads commentator makes the direct application: "A 500-item backlog of 'someday/maybe' features would clutter that query and waste context tokens every time an agent checks what to do next."

### Area 2 — Git-native issue trackers

The landscape, by data model and conflict behavior:

- **Beads (`bd`)** — the flagship "AI-native" entrant (Steve Yegge, 2025). Data model: a version-controlled database (SQLite, or Dolt in newer builds) synced to git via JSONL export/import. Key features directly relevant to the user: **hash-based IDs** (`bd-a1b2`) that "prevent collisions when multiple agents work concurrently"; **`bd ready`** which "queries the database for all open issues with no uncompleted dependencies"; four dependency types (blocks, related, parent-child, **discovered-from**); `--json` on every command; an MCP server. Maturity: **alpha, heavy churn** — one doc notes "Optimized for project-scoped databases (< 500 issues)" and reviewers report schema-migration pain and Dolt build complexity (CGO required). Independent reviewer caution (Tekai): the token-efficiency claim is real but "the comparison is against a deliberately weak baseline (flat markdown files)"; and Ian Bull's line, "The tool provides the memory. You provide the discipline." Beads's own guidance says to keep the distant backlog elsewhere (GitHub Issues, Notion, "a simple markdown file") and only promote items into `bd` when they move to "now."

- **`backlog.md`** — Markdown-native (one `.md` per task, YAML frontmatter), Go/TypeScript, zero-config CLI + MCP + Kanban web UI. ~5,600 stars, active (38 contributors). Honest limitation from a third-party analysis: "No built-in isolation: multiple agents editing different tasks in the same working tree can create merge conflicts if not disciplined about feature branches" — but because each task is a separate file, conflicts are per-item and human-readable, not whole-file.

- **git-bug** — stores issues as git objects in `refs/bugs/` (not files in the tree), so it "doesn't pollute your project." Uses Lamport timestamps and an operation-based (CRDT-like) data model so "even when multiple users modify the same issue concurrently across different remotes, the changes can be merged without conflicts." Mature-ish (v0.8+), CLI/TUI/web, bridges to GitHub/GitLab. Trade-off: issues live in refs, so they are less directly greppable than files, and it is less "agent-native" than Beads.

- **git-native-issue / the `refs/issues/` pattern** — issues as commit chains under `refs/issues/`, metadata as git trailers, "merge commits resolve conflicts ... No CRDTs, no operational transforms, just merge commits," and "scales to 10,000+ issues because `git for-each-ref` is a single batch operation." Elegant, early-stage, single-author.

- **Fossil** (built-in ticketing) — tickets are append-only "ticket change artifacts"; current state is computed by replaying changes in timestamp order, and "independently entered changes are automatically merged together when artifacts are shared." Ticket IDs are random 40-char hex (no collisions). This is a battle-tested, decades-old realization of exactly the append-only, merge-friendly model the user needs — but adopting Fossil means adopting a whole SCM.

- **Older/quieter:** `git-issue`, `ticgit`, `sit`, GitIssius, BugsEverywhere — mostly proof-of-concept or dormant; useful as design references (per-item files, JSON payloads) rather than production choices.

The pattern to steal regardless of tool: **per-item object + append-only change log + content/hash IDs + a `ready` query.** Fossil's replay model and git-bug's operation-based CRDT are the two proven answers to "two agents each file one row without a merge conflict."

### Area 3 — GitHub Issues + Projects at scale, for agents

State outside the repo, but now genuinely agent-integrated:
- **2025 issue features:** sub-issues (up to eight levels of hierarchy), issue types, converting checklist items directly to sub-issues, required fields on issue forms. Tasklist blocks retired April 30, 2025 in favor of sub-issues.
- **Projects v2 limits:** the historical 1,200-item cap was raised to a **50,000-item soft limit** (public preview Feb 2025); project **insights** are now free on all plans. Note the archiving-via-API pain reported by users at the old cap.
- **API/rate limits:** REST is **5,000 req/hr** authenticated (15,000 for GitHub Enterprise Cloud org apps; **60/hr unauthenticated**); GraphQL is point-based (2,000 points/min); secondary limits cap concurrency (~100 concurrent, 900 pts/min REST). For an agent fleet polling issues, these matter — the guidance is webhooks-not-polling, conditional requests, serial writes.
- **Agent integration is now first-class:** GitHub's **Agent HQ** lets you assign an issue to **Copilot, Claude, or Codex (or all three)** via the Assignees dropdown; each "will automatically begin work and submit a draft pull request." Copilot cloud agent (GA Sept 2025, renamed "cloud agent" April 2026) takes an issue → sandboxed Actions runner → draft PR. Practical gotcha for automation: assigning Copilot via REST requires the exact handle `copilot-swe-agent[bot]` and a **fine-grained PAT** (GitHub App tokens are rejected).

Does issue-driven agent work reduce or increase overhead? Vendor docs claim reduction ("assign straightforward issues ... spend less time"); independent sources are mixed and note the feedback loop is "measured in hours." No independent controlled evidence yet shows net overhead reduction — treat the ROI claims as vendor/practitioner opinion.

The decisive trade-off for this user: **GitHub Issues moves state out of the repo** — breaking offline work, portability, single-artifact review, and the "the LLM sees what the human sees in the repo" property that a Corporate-OS methodology hub depends on. `git-native-issue`'s framing is apt: "Your code travels with git clone. Your issues don't."

### Area 4 — Generated views over a structured source (the user's existing pattern)

The user has already built the right architecture (per-task files + `manifest.json` + generator + an unused `export_backlog_view.py` and `gen_task_tree --rank`). The literature on this pattern:

- **Obsidian Dataview** turns Markdown+frontmatter into a queryable database (DQL: `TABLE/LIST/TASK ... FROM ... WHERE ... SORT`). Crucial limitation for a task backlog: **Dataview's `TASK` and inline-field queries read per-item metadata, but the newer no-code Obsidian Bases reads only frontmatter**, so per-task metadata must live in frontmatter to be queryable by Bases. And a hard warning from a heavy user (15,000+ queries): "a result that only exists at render time is not knowledge you own" — i.e., **serialize the ranked output to a committed file**, don't leave it as an ephemeral render.
- **Dendron / Foam** (VS Code, Markdown+frontmatter) and **SQL-over-Markdown** approaches are viable but heavier.
- **CI-generated dashboards:** committing a generated Markdown/HTML report on a schedule (Graham Wheeler's `ghreport` pattern) is the proven way to make a view *durable and diffable*.

**What makes a generated view actually get used rather than ignored?** From the evidence: (a) it must be *short and ranked* (a "next 5," not the full list) — flat inventory is what the user already ignores; (b) it must show **what changed since last time** (a diff/digest) so a returning operator sees progress; (c) it must be **committed** (diffable, reviewable), not render-only; (d) it must surface **staleness and next-actionable**, not just status. A "useful" view contains: the ready/unblocked set, ranked; aging outliers; a since-last-window changelog (births vs. closures); and the ledger denominator. The plain 212-row emit fails all four tests — which is exactly why the user reports it "looks the same, huge, huge, huge."

### Area 5 — Prioritisation and ranking frameworks that scale to hundreds

The named frameworks and the honest evidence:
- **WSJF** (SAFe): Cost of Delay ÷ Job Size. Good for economic sequencing at portfolio scale; critiqued because "its inputs are human judgment" and it lacks an explicit confidence term.
- **RICE** (Reach × Impact × Confidence ÷ Effort, from Intercom): best when you have usage analytics; includes confidence explicitly.
- **ICE** (Impact × Confidence × Ease): fastest, most subjective.
- **MoSCoW**, **Kano**, **Cost of Delay/CD3**, **Eisenhower**, **value/effort**: each a different lens.

The critical meta-finding: **there is no empirical winner, and all scoring frameworks share a fatal arithmetic weakness** — Itamar Gilad and Saeed Khan both note that multiplying/dividing 3–4 subjective estimates compounds the margin of error (±20% per factor → ~80% total error in RICE), so the scores carry false precision. Khan's sharper point applies directly to the user: "If you have so many 'features' to implement that you need a framework and spreadsheet to prioritize them, then you have another problem ... Why are you not able to reduce them by other means?"

**The most valuable ranking mechanism for an agent workflow is not a value-scoring framework at all — it is dependency-aware topological ordering** ("what is actually ready now"). Beads's `bd ready`, Kiro's dependency-graphed "waves," and Spec Kit's `[P]` markers all encode this. This is exactly what the user's `gen_task_tree --rank` should produce. Automated/assisted scoring from structured fields is reasonable; **LLM-assisted grooming should be treated as a proposer, not a decider** — the reliability evidence is thin and vendor-sourced.

### Area 6 — Backlog hygiene, aging, and deletion

The strongest guidance here is unusually consistent:
- **Large backlogs are an anti-pattern in themselves** (Scrum Alliance): "the larger the backlog, the harder it is to manage."
- **Aggressive deletion is endorsed by senior practitioners.** Mike Cohn: "be fairly ruthless in purging items ... If you don't think you'll realistically ever do it, just get rid of it," and "I can come up with new ideas faster than they can develop them." His four rules: delete what you'll never do; don't refine items >3 sprints out; when adding one, remove one; learn to say "not now."
- **"Backlog bankruptcy"** is a recognized, repeatedly-reported move: archive everything, rebuild top-down. ProductPlan's firsthand account: after deleting everything not in a near-term sprint, "There were no repercussions from that decision. And I got a sense of relief." Multiple sources recommend a fixed cap afterward (Mountain Goat's template: limit to ~50 items, "one in, one out").
- **The "item older than N months is effectively dead" argument:** widely asserted (stories written "six months, a year, two years ago are more likely to cause harm than good"), presented as practitioner opinion, not measured.
- **Flow metrics are the instrument the user is missing:** Little's Law (Avg WIP = Throughput × Avg Cycle Time); **average age of WIP** ("if something's getting old and nobody's talking about it, that's your system waving a red flag"); cumulative flow diagrams; flow efficiency. These measure whether pruning *improved* anything (falling aging, stable/rising throughput).

**Stale bots — the independent empirical evidence (this is the strongest data in the whole report):**
- **Wessel et al. (BotSE 2019, DOI 10.1109/BotSE.2019.00018)** studied **765 OSS projects**. The bot's default `daysUntilStale` = **60**, `daysUntilClose` = **7** (across projects, median days-until-close = 7, Q1=Q3=7). Only **77 of 765** projects disabled auto-close. **~59.2%** of projects only added the config and never modified it; **~83%** made ≤3 modifications. Key qualitative finding: "issues tagged as bug reports are exempt from being considered stale." (The exact percentage of projects exempting bugs sits in a table not recoverable from the accessible text — treat the exemption as a strong qualitative pattern, not a precise figure.)
- **Khatoonabadi et al. (TOSEM 2023, DOI 10.1145/3624739)** studied **20 large projects** (median 18,975 PRs each) with interrupted time-series over 12 months before/after adoption. Findings: **+15% PRs closed in month 1, but −10% closed and −24% merged by end of year 1**; first-review latency on merged PRs **−21%**; resolution time on closed PRs **−22%**; **but −14% active contributors**. Counter-intuitive and directly relevant: **projects with larger backlogs did NOT rely more on the bot** (Spearman ρ = −0.31 with backlog size, non-significant; ρ = −0.38 with monthly open PRs); higher bot activity correlated with more aggressive *configuration* (ρ = −0.79 with days-to-stale), not backlog size. Conclusion: "relying solely on Stale bot to deal with inactive PRs may lead to decreased community engagement and an increased probability of contributor abandonment."
- **The open-source critique of auto-close** is fierce and well-argued (nostalebots.xyz; Jacob Tomlinson: "once an issue becomes a clear actionable task it should never be closed due to inactivity ... a human needs to make that call, not a bot"). The synthesized best practice: use bots to **label/triage and nudge**, exempt bugs, and only auto-close items still awaiting *reporter* input — never triaged, actionable work.

For a **solo operator with LLM agents** (not an OSS community), the contributor-abandonment downside largely evaporates — there is no community to alienate. That materially *strengthens* the case for aggressive, judgment-driven pruning here, provided git history is the safety net.

### Area 7 — Net-negative / closure-budget disciplines

The user's "births must not exceed banked closures" rule has strong, well-studied analogues:
- **Kanban WIP limits** — the canonical version. Backed by Little's Law: reducing WIP reduces cycle time at constant throughput. But the literature is emphatic that **a WIP limit is "a signal, not a failure"** and must have agreed policies for when it can be broken (classes of service), or teams "hide the problem under a policy change."
- **SRE error budgets** — the closest philosophical match. An error budget "converts 'we should focus on reliability' from an engineering opinion into an organizational fact." Google's own guidance uses graduated tiers and warns that **partial freezes don't hold** and exceptions "normalize the behavior they are meant to prevent" — except a small number of pre-approved "silver bullet" escalations.
- **"Zero bug bounce" / bug caps / defect-debt budgets / "one in, one out"** — all variants of the same idea.

**Documented failure modes (all apply to a naive net-negative ledger):**
- **Gaming / refusing to file real issues** — the arXiv "degenerate admissibility" result formalizes it: a control becomes vacuous when "every signal that could elevate risk has been suppressed prior to evaluation." A ledger that punishes births incentivizes *not filing* real work — the worst outcome for an agent system that *should* surface discovered work (Beads's `discovered-from` edge exists precisely to capture it).
- **Hiding work / bundling** — closing many trivial rows to "bank" closures while real work stalls.
- **Proxy-metric capture (Goodhart)** — "banked = 0" becoming the goal instead of a healthy, actionable backlog.

Mitigation from the evidence: keep the ledger as a **visible diagnostic with graduated responses**, pair it with **aging-WIP and throughput** (so gaming shows up as rising age/falling throughput), exempt a "discovered-from/bug" class from the birth penalty, and review breaches for *cause* rather than auto-enforcing.

### Area 8 — Agents writing to the backlog safely

The user's manifest + `generated_sha256` design is the textbook cause of un-mergeable collisions. The evidence-based fixes:

- **Per-item files, not one aggregate.** This is the single highest-leverage change. Every tool that survives concurrent agent writes (backlog.md, Beads via JSONL-per-line, Fossil artifacts, git-bug refs) does this. A whole-file regenerate with a changing hash *cannot* three-way-merge.
- **ID allocation:** avoid `max+1` scans (the classic race — two agents both pick `#556`). Options, with trade-offs:
  - **ULIDs** — 128-bit, timestamp-prefixed, **lexicographically sortable**, monotonic option, decentralized, "collisions are only possible inside the same millisecond." A TU Ilmenau comparative study (Karimian Kakolaki, arXiv:2509.08969) found "ULIDs significantly outperform UUIDv4 and UUIDv7, reducing network overhead by 83.7% and increasing generation speed by 97.32% ... ULIDs offer a 98.42% lower collision risk compared to UUIDv7." Best fit for "sortable + collision-free + no coordinator."
  - **Hash-based short IDs** (Beads `bd-a1b2`) — collision-resistant, human-readable, no coordinator.
  - **UUIDv7** — standardized (RFC 9562), time-sortable.
  - **Reserved ranges per agent** — simple, works, but brittle and wastes space.
  - Human-friendly `[#555]` sequential IDs can be kept as a *display alias* derived at emit time, decoupled from the collision-safe canonical ID.
- **Append-only event log with derived state** (Fossil's model): agents *append* a change record; current state is a replay/fold. Appends from different agents merge trivially.
- **"Propose, don't write"** — the strongest pattern for the user's integrator discipline: an agent emits a *proposed* task spec (its own file, or a PR), and an integrator (human or a single privileged process) lands it. This maps directly onto GitHub's "draft PR from an issue" flow and onto the user's existing "ledger discipline on main."
- **CRDT/operation-based merges** (git-bug) — the most automatic, but heavier to build.

**Real-world reports of agents corrupting/duplicating state are abundant and specific:** parallel agents in a shared working tree "overwrite each other's files, operate on stale views ... and compete for `.git/index.lock`," with "agents proceed silently on corrupted data rather than surfacing exceptions." The consensus mitigation is **git worktrees** (one isolated checkout per agent) — but note worktrees solve *file* isolation, not *shared-artifact* logic: "the conflict problem moves to the PR merge stage," and "duplicated implementations emerge when parallel branches cannot share intermediate decisions." Harvey AI's production "isolate-then-reconcile" pattern (sub-agents edit isolated copies; a reconciliation step auto-merges non-conflicting edits, surfacing conflicts to an orchestrator) is the mature reference design. And a sober counterweight: "Stop parallelizing your AI agents — the merge tax will eat your 10x speedup"; the merge cost is superlinear past ~5 concurrent agents.

### Area 9 — Making a backlog legible (the operator experience)

What makes a large backlog comprehensible at a glance, from the evidence:
- **"Next 5 things," not the full list.** The ready/unblocked, ranked slice is the primary surface. This is `bd ready` and the three-zone model (Active / Archive / Someday-Maybe) from Humanizing Work.
- **Roadmap ≠ backlog.** A backlog is "most effective as a shorter, detailed visualization of the product roadmap" (Kutter's "Graveyard" board pattern for parked ideas).
- **Show flow, not inventory.** Dashboards that show throughput, aging WIP, and WIP counts "turn vague observations into actionable insights" ("average WIP age jumped from 3 → 7 days ... most issues stuck in Review"). This is precisely the "instrument" the user says grooming lacks.
- **Show what changed since last time.** A since-last-window digest/changelog (births, closures, net, newly-unblocked, newly-stale) is what lets a returning operator see progress — directly answering "some tasks closed, some not, I don't know what the difference is." This is a diff of the backlog itself, which the per-item-file + git model makes trivial (`git log`, `git diff` over `tasks/`).
- **Tree/hierarchy + dependency visualization** (theme → story → task, with blocks edges) beats a flat list for comprehension; Beads `dep tree` and Kiro's wave view are the references.

## Recommendations

**Stage 0 — Stop the bleeding (this week).**
1. **Freeze the `generated_sha256`-on-a-single-file design as the write target.** Keep `BACKLOG.md` as a *read-only, generated* artifact; make the per-task `.md` files + `manifest.json` the sole write surface. This alone removes the two-agents-one-row collision because agents now touch different files.
2. **Give the manifest a collision-safe canonical ID per task (ULID or content hash), and keep `[#555]` as a derived display alias.** Kill any `max+1` allocation.

**Stage 1 — Make the view earn its keep (next 1–2 weeks).**
3. **Ship the dormant `export_backlog_view.py` and `gen_task_tree --rank`, but redefine "the view" as a committed, short, ranked digest**, not the 212-row dump. Minimal viable view (see below). Commit it in CI so it is diffable.
4. **Compute and display flow metrics:** open count, throughput per window, average age of open items, and the aging outliers (oldest 10). This is the missing "instrument."

**Stage 2 — Prune to a defensible size (next 2–4 weeks).**
5. **Declare a controlled backlog bankruptcy.** Move every item not slated for the next ~2–3 windows into an `icebox/` (archived, still in git history). Target a live backlog of **~40–60 items** (Mountain Goat's ~50 template is a reasonable anchor). The evidence that this is safe: senior-practitioner consensus + "if it matters it will be re-filed" + your git history as the undo button.
6. **Adopt "one in, one out" for the live set** and a quarterly ruthless purge. Exempt a "bug/discovered-from" class from the cap so agents are never disincentivized from surfacing real defects.

**Stage 3 — Choose the durable tool (evaluate over a month).**
7. **Default recommendation: keep your git-native, in-repo, per-item-file model** (it uniquely preserves "the LLM sees what the human sees," offline, and portability for a Corporate-OS methodology hub). **Pilot Beads (`bd`) on one theme** to get `bd ready`, dependency edges, and hash IDs "for free" — but treat it as the *active* layer only, keeping the icebox in Markdown, exactly as Beads's own authors advise. **Do not move to GitHub Issues/Projects** unless you specifically need Agent HQ's assign-issue-to-Claude/Codex/Copilot flow or Projects v2 dashboards more than you need repo-native state.
8. If you prefer a finished tool over your own generator, **`backlog.md`** is the closest match to your current design (per-task `.md` + frontmatter + CLI + web board + MCP).

**Benchmarks that would change these recommendations:**
- If concurrent agents routinely exceed ~5, revisit the "propose-don't-write" integrator model and worktree isolation before scaling further (the merge tax is superlinear).
- If average age of WIP keeps rising after pruning, the problem is throughput/WIP, not backlog size — stop pruning and lower WIP limits instead.
- If Beads stabilizes past 1.0 and drops the Dolt/CGO build friction, promote it from "pilot" to "active layer of record."
- If you ever need multi-human collaboration or external contributors, re-evaluate GitHub Issues (the offline/portability costs become worth paying).

## Direct answers to the five decision questions

**(a) Should the 212-row backlog stay Markdown-in-repo, move to a git-native tracker, or move to GitHub Issues/Projects?**
**Stay git-native and in-repo, but restructure to per-item files with a disposable generated view; pilot Beads as the "active" layer.** Decisive criteria: (1) you need offline + portability + "LLM sees what humans see" → rules *out* GitHub Issues as the source of truth; (2) you need concurrent agent writes without merge hell → rules *out* the single-regenerated-file design and *in* per-item files/append-only logs; (3) you need dependency-aware "what's ready" → favors Beads/`backlog.md`/your own `gen_task_tree --rank`. Move to GitHub Issues only if assign-to-agent (Agent HQ) or Projects dashboards outweigh losing repo-native state.

**(b) Minimal viable "view" for progress + next actions at a glance.** A single committed `BACKLOG_VIEW.md` (regenerated in CI) containing, in order: **(1) the ledger line** — this window's births, banked closures, net, and the ruled denominator; **(2) "Next 5" ready/unblocked items**, ranked by your `--rank` score, with theme/story tags; **(3) flow vitals** — open count, throughput (last 3 windows), average age of open items; **(4) aging outliers** — the 10 oldest open items (candidates for pruning); **(5) "Since last window"** — a diff/changelog of births, closures, newly-unblocked, newly-stale. This replaces the 212-row dump entirely; the full inventory lives in `tasks/` and is queried, never read linearly.

**(c) How to get from 212 to a defensible target.** Mechanism: **controlled backlog bankruptcy → cap → one-in-one-out.** Archive (not delete) everything outside the next ~2–3 windows into `icebox/`; set a live cap of ~40–60; enforce one-in-one-out with a bug/discovered-from exemption; quarterly ruthless purge. Evidence supporting aggressive pruning: Mike Cohn's "be ruthless"; ProductPlan's "no repercussions ... a sense of relief"; Scrum Alliance's "large backlog is an anti-pattern"; and the stale-bot data showing silence rarely tracks value — combined with the fact that, as a solo+agents operator, you have *no community to alienate*, so the main documented downside of aggressive closing (−14% contributors in the TOSEM study) does not apply to you. Git history is the safety net; "if it matters, it gets re-filed."

**(d) How to let parallel agents file and close items without merge collisions.** Four combined moves: **(1) per-item files** (kill the single regenerated aggregate as a write target); **(2) collision-safe IDs** (ULID or hash; abolish `max+1`); **(3) append-only change records** with derived state (Fossil's replay model) so two appends always merge; **(4) "propose-don't-write"** — agents emit proposed task files/PRs, a single integrator lands them on `main` (this is your existing ledger-on-main discipline, formalized). Run each agent in its own **git worktree** for file isolation, and accept that genuine logical conflicts surface at PR-merge time (which is where you want them). Keep concurrency ≤ ~5 to avoid the superlinear merge tax.

**(e) Is a net-negative ledger a good idea, and how to instrument it so it isn't a proxy metric?**
**Yes as a diagnostic, no as a hard target.** It is the correct analogue of an SRE error budget / WIP limit and gives you "objective authority to say 'not now.'" But guard against its documented failure modes (gaming, refusing to file real work, hiding work, Goodhart capture — the "degenerate admissibility" trap). Instrument it so it can't degenerate: (1) make it a **graduated signal**, not an auto-enforcing gate (green/caution/freeze tiers, à la error-budget policy); (2) **pair it with aging-WIP and throughput** so gaming shows up as rising age / falling throughput even when the ledger looks green; (3) **exempt a bug/discovered-from class** from the birth penalty so agents keep surfacing real work; (4) **review breaches for cause**, not with automatic closes; (5) never let "banked = 0" force closing legitimate work — that is the mechanical floor you have already hit, and it is the signal to *prune the icebox and lower WIP*, not to sweep-close.

## Caveats
- **Vendor/practitioner vs. independent evidence:** Beads, `backlog.md`, Kiro, Spec Kit, and the GitHub Agent HQ claims are **vendor/author documentation or single-practitioner blogs**, not independent studies; the AI-native tracker category is <18 months old and alpha-quality (Beads explicitly). The prioritization-framework and backlog-pruning guidance is overwhelmingly **practitioner opinion** (Cohn, ProductPlan, Scrum Alliance), not controlled research. Treat "issue-driven agent workflows reduce overhead" as unproven.
- **The genuinely independent, peer-reviewed evidence** is narrow: the two stale-bot studies (765 projects; 20 projects), the "lost in the middle" (Liu et al., TACL 2024) and Chroma "context rot" work, Little's Law, and the ULID/UUID comparison (arXiv:2509.08969). The stale-bot studies are on *open-source communities*, so their contributor-abandonment finding may not transfer to a solo+agents setting — I have flagged where that changes the recommendation. One Wessel-2019 detail (the exact percentage of projects exempting bug labels) sits in a table not recoverable from accessible text; the bug-exemption pattern is reported qualitatively.
- **Beads is in flux** (SQLite vs Dolt, CGO build complexity, schema migrations, "<500 issues" sweet spot). Piloting is warranted; betting the methodology hub on it today is not.
- **Flow metrics assume a roughly stable system** (Little's Law's constraints); with bursty agent output, treat throughput/aging as directional signals, not precise forecasts.
- I did not independently verify the user's internal tooling behavior (the `generated_sha256` collision, `export_backlog_view.py`, `gen_task_tree --rank`); recommendations take the user's description as given.