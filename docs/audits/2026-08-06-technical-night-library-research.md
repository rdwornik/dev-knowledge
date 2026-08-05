# Library-first research — seven adoption questions for the B1–B5 births and the P-carries

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** unattended night batch, Claude Code on the web; branch `claude/night-batch-2026-08-06-p59kml`; HEAD `8e2be6a1`
- **Status:** complete for items 3–7 · items 1–2 recorded as NOT DELIVERED (see §8)
- **Model:** claude-opus-5 orchestrating; Sonnet-class web-research lanes

Framing per PLAYBOOK §11 "Library-first adoption order (ruled 2026-08-04)"
(`protocols/PLAYBOOK.md:3442-3454`): stdlib > an existing dependency > a new distribution, and
an adoption claim carries a **measured divergence** rather than a preference. Every verdict
below names what the candidate does and does not cover.

## Verdict board

```
item                              verdict            the constraint that decides it
--------------------------------  -----------------  ------------------------------------------
3  doc-code drift ([#408])        BUILD-thin         no tool binds a GLOB to a doc SECTION;
                                                     closest (Fiberplane drift) is 1-file -> 1-doc
4  commit-convention engines      LEAVE              commitlint cannot see the diff; gitlint can
   (P6 carry)                                        but is dormant since 2023-09
5  link/pointer rot (P6 carry)    ADOPT-candidate    covers local links + heading anchors;
                                                     cannot do file.py:123 (different class)
6  scheduled runs + dead-man's    BUILD-thin         watchdog is buildable; "who watches the
   switch (P2 -> [#493])          + LEAVE            watchdog" has no GitHub-native answer
7  gh findings-as-Issues (P3)     ADOPT-candidate    secondary limit blocks at ~100-150 issue
                                                     creations -- issue-per-finding is refuted
1  mutation testing (B2)          NOT DELIVERED      see §8
2  prose linting / vale (B3)      NOT DELIVERED      see §8
```

## Item 3 — doc-code drift detection (the [#408] substrate). **BUILD-thin.**

The field is thin: two commercial players and one genuinely close open-source tool.

**Fiberplane `drift`** — the closest prior art, and worth studying rather than adopting.
MIT, ~128 stars, repo touched June 2026, ships a GitHub Action and a `drift check` CLI.
Bindings live in a `drift.lock` TOML carrying `doc`, `target` (`path` or `path#Symbol`), `sig`
(a hash), and an optional `origin` cross-repo pointer.
https://github.com/fiberplane/drift · https://fiberplane.com/blog/drift-documentation-linter/

Its one genuinely better idea, which the [#408] design should steal outright: `sig` is a
**normalized AST fingerprint** (tree-sitter node-kinds plus token text, ignoring whitespace
and position), not a raw commit SHA. A naive "any commit after SHA X" trigger false-positives
on every reformat, typo fix and comment edit — and this repo generates a lot of those. The
fingerprint approach only fires when the code's *structure* moved.

Where it falls short of what [#408] needs, in two load-bearing dimensions:
- it binds **one file (or one symbol) per edge**, not a **glob** of files;
- it anchors to a whole **doc file**, not a **doc section / heading**.

Both gaps are exactly the shape this repo needs, because an `ARCHITECTURE.md` H2 chapter
describes a subsystem spread across many files.

**Swimm** — alive, not acquired, not shut down. $33.3M raised; Series A $27.6M (2021, Insight
Partners + Dawn Capital). Pro ~$16–29/user/mo; Enterprise custom. Genuinely self-hostable
including air-gapped, with a no-AI option. Its "Smart Tokens" bind prose to code symbols and
its auto-sync is a proprietary multi-signal heuristic ("histogram" of line markers, line
numbers, token references, change magnitude, VCS history), verified per commit.
https://techcrunch.com/2021/11/08/swimm-nabs-27-6m-series-a-to-include-up-to-date-documentation-in-every-release/
· https://swimm.io/enterprise · https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work
Not adoptable here: it is a platform requiring docs authored in its own token markup, and a
paid black box in place of the deterministic, git-anchored, auditable manifest this repo's
culture is built on.

**Dosu** — the interesting counter-design. $8.5M Series A (Sequoia, Innovation Endeavors);
used by Airflow, LlamaIndex. Ships a 0–100 freshness signal in CI: three deterministic checks
plus an LLM layer for the gray zone — structurally the same three-layer shape as the operator's
[#408] spec, which is a useful independent corroboration that the shape is right.
https://dosu.dev/blog/score-documentation-freshness-in-ci
But it deliberately **rejects hand-curated doc↔code mappings** in favour of tree-sitter-derived,
graph-ranked, fully AI-inferred bindings, plus a per-doc frontmatter **TTL** (time-based shelf
life, not source-based). Proprietary SaaS; excluded by the no-external-SaaS constraint.

**Mechanism classes that are not substitutes** (checked, and each rules itself out):
- *Inclusion* — Sphinx `literalinclude`, `pymdownx.snippets`, mdBook `{{#include}}`.
  Guarantees the *quoted* code cannot go stale; says nothing about surrounding prose, and is
  inapplicable to prose that *describes* code rather than quoting it — which is nearly all of
  `ARCHITECTURE.md`.
- *Execution testing* — `doctest`, `pytest --doctest-glob`, `mdsh`, `phmdoctest`, Doc
  Detective. Verifies runnable snippets; has no concept of a descriptive claim.
- *Linters* — explicit negative finding: **no Vale or markdownlint plugin does code-reference
  staleness**. Searched directly; found only prose/style and Markdown-syntax rules.
- *PR-rule DSLs* — Danger.js has carried "if this file changes, require that file to change
  too" as an **open feature request** for years (https://github.com/danger/danger-js/issues/431).
  That a major PR-automation framework still treats this as a wishlist item is itself evidence
  of how narrow the built tooling is.

**Verdict: BUILD-thin**, and the divergence is categorical rather than a matter of taste — no
candidate implements the layer at all. Steal the fingerprint-not-raw-SHA trick from `drift`.

## Item 4 — commit-convention engines (P6 carry). **LEAVE.**

The two rules at stake both need the **staged diff**, not just the message: Rule A (a commit
removing a backlog task line carries `[#id]`) and Rule B (a commit adding a task id carries a
`kill-candidates:` trailer). Both exist today as bespoke Python `commit-msg` hooks.

| | commitlint | gitlint |
|---|---|---|
| Latest release | **21.2.1 — 2026-07-08** | **0.19.1 — 2023-03-10** |
| Last commit to main | active | **2023-09-02** |
| License | MIT | MIT |
| Adoption | ~18.6k★, ~8.1M weekly downloads | 966★ |
| Rule API sees the diff? | **No — message text only** | **Yes** |
| Custom trailer with a value grammar | `trailer-exists` is **presence-only** | `body-match-regex` (B8), config-only |

**commitlint would be lossy, and this is the decisive fact.** Every rule is
`function(parsed, when, value)` where `parsed` is the conventional-commits breakdown of the
message text — `type`, `scope`, `subject`, `body`, `footer`, `notes`, `references`, `raw`,
`header`, `mentions`, and nothing else. No changed-files list, no diff, no repo path.
https://commitlint.js.org/reference/plugins.html
A rule *could* shell out to `git diff --cached` on its own initiative, but that is
undocumented, assumes `process.cwd()` is the repo root, and no ecosystem precedent for it was
found. **Named loss: direct diff access** — precisely what both rules require.
It also introduces a Node dependency *class* into a Python-only toolchain, though
pre-commit's `language: node` self-provisions an isolated runtime via `nodeenv`, which softens
the cost. Note commitlint ships no `.pre-commit-hooks.yaml` of its own
(https://github.com/conventional-changelog/commitlint/issues/2109), so adoption depends on the
third-party `alessandrojcm/commitlint-pre-commit-hook` wrapper — one more supply-chain hop.

**gitlint would not be lossy — but it is dormant.** Its `CommitRule.validate(self, commit)`
receives a `GitCommit` carrying `changed_files_stats` (per-file add/delete counts),
`changed_files`, and a reachable `context.repository_path`; under a `commit-msg` hook it builds
these from `git diff --staged --numstat -r`. So the "did this file change" half is free, and
one subprocess call — identical to what the bespoke hook already does — covers line content.
It even has a structural precedent for the shape, `body-changed-file-mention` (B7).
https://github.com/jorisroovers/gitlint/blob/main/gitlint-core/gitlint/git.py
The disqualifier is maintenance: PyPI's latest is **0.19.1 (2023-03-10)**; the last commit to
`main` is **2023-09-02**; and `CHANGELOG.md` on `main` currently reads
`# v0.20.0 (Unreleased)` directly above the 2023 release — unshipped work that has sat for
close to three years. The maintainer has described the model as bursty by choice
(https://jorisroovers.com/posts/maintaining-gitlint/), and users are still filing issues into
2025–2026, so the project is not abandoned — but the release valve has been shut.

**Verdict: LEAVE.** Rehoming two working, zero-external-dependency Python hooks into a dormant
third-party framework for the ceremony of `.gitlint` rule discovery is a net risk increase for
no capability gain. If a future general commit-hygiene need arises, gitlint is the right
*shape*; its dormancy should be treated as disqualifying for anything gating `main`.

## Item 5 — link / pointer rot (P6 carry). **ADOPT-candidate, with the boundary named.**

**lychee** — `v0.24.2` (2026-05-01); most recent commit 2026-08-03; Apache-2.0 OR MIT; 3.8k★;
official `lycheeverse/lychee-action` whose `action.yml` already defaults to v0.24.2. Named
users include Kubernetes docs, OpenSearch, HashiCorp Consul, Fastify.
https://github.com/lycheeverse/lychee/releases · https://github.com/lycheeverse/lychee-action

**(a) Local relative file links — yes, this is default behaviour.** `lychee .` recursively
checks links in all supported files, resolving markdown targets against the filesystem.
`--offline` restricts it to local files with no network calls — a same-repo, no-network audit
mode. `--root-dir` and `--base-url` handle the absolute-style and hosted-tree cases.

**(b) Heading / fragment anchors in local markdown — yes, and this is the decisive capability.**
`--include-fragments` (`none` / `anchor-only` / `text-only` / `full`) parses the **target
file's actual headings** two ways: explicit `{#custom-id}` attributes, and GitHub-style
auto-generated kebab-case anchors from heading text — handling Unicode, inline code in
headings, and underscores. https://lychee.cli.rs/recipes/anchors/
**This is exactly the repo's real rot class** — a renamed `ARCHITECTURE.md` heading breaking an
`#ch2-organ-map`-style citation elsewhere. Two caveats from the same source:
JavaScript-generated anchors cannot be checked, and complex nested HTML may not be. And it is
**opt-in, not default** — a lychee run without the flag proves nothing about anchors. Currency
signal: a "GitHub markdown fragment matching" fix landed 2026-07-05, so this is under live
refinement.

**(c) `file.py:123` locators — no, and not a gap in lychee.** Its extractors recognize link
*syntax* (markdown links, `href`/`src`, autolinks, emails). A bare prose token like
`scripts/audit.py:825` carries no link syntax and is never proposed as a candidate. That check
is a different class — doc-to-code locator drift — and the repo already has the right tool for
it: `/preflight` (`scripts/preflight_contract.py`, claim kinds `file-line`, `heading`, `sha`,
`backlog-id`). The two compose cleanly and neither replaces the other.

**(d) Caching and rate-limit control.** `cache = true` + `max_cache_age` + `cache_exclude_status`
persist to `.lycheecache`, which the Action's README recommends carrying across runs via
`actions/cache@v4` explicitly "to reduce rate limiting stress". Independent throttles:
`max_concurrency`, `host_concurrency`, `host_request_interval`, `max_retries`,
`retry_wait_time`. `github_token` (Action input `token`, default `${{ github.token }}`)
authenticates lychee's own outbound `github.com` checks — which matters here, because a
governance repo dense with `github.com` cross-links generates many API-bound checks per run.
See item 7(c) for how tight that budget is.

**Verdict: ADOPT-candidate** for (a)+(b) — actively maintained, GitHub-native, no SaaS.
**LEAVE** for (c), which is `/preflight`'s job.

## Item 6 — scheduled runs + dead-man's switch (P2, folds into [#493]). **BUILD-thin, and one part is honestly unsolvable.**

**(a) `schedule:` reliability, verbatim from current docs** — and note it says *dropped*, not
merely delayed, which changes a watchdog's design:

> "The `schedule` event can be delayed during periods of high loads of GitHub Actions workflow
> runs. High load times include the start of every hour. **If the load is sufficiently high
> enough, some queued jobs may be dropped.** To decrease the chance of delay, schedule your
> workflow to run at a different time of the hour."

Also confirmed: the shortest interval is **once every 5 minutes**; scheduled workflows **run
only on the default branch** ("Workflow file versions that exist outside of the default branch
will not trigger on these events").
https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule

**The 60-day auto-disable — an ambiguity left unresolved rather than papered over.** Every
instance of this rule locatable in GitHub's own docs says **"public repository"**: "In a
public repository, scheduled workflows are automatically disabled when no repository activity
has occurred in 60 days." No official sentence naming *private* repositories was found. Many
third-party sources assert flatly that it applies to both; that is their paraphrase, not
GitHub's statement. **The target repo is private, so this is an open question, not a settled
one** — and it is load-bearing for [#493], because it determines whether the wall can die of
inactivity.

**(b) The dead-man's-switch pattern — option (i) is the only viable one.**
- *(i) A second scheduled workflow querying the Actions API and opening an Issue on staleness* —
  buildable and GitHub-native. `GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs`
  is current and works on private repos with `actions: read` (or classic `repo` scope).
  https://docs.github.com/en/rest/actions/workflow-runs · CLI form:
  `gh run list --workflow=<name> --json databaseId,status,conclusion,createdAt --limit 1`.
- *(ii) `workflow_run` — confirmed NO.* Verbatim: "This event occurs when a workflow run is
  **requested or completed**." Activity types are `completed`, `requested`, `in_progress` — all
  real transitions of a run that happened. Absence produces no event.
- *(iii) External cron* — excluded by the no-SaaS constraint.

**(c) The self-referential hole is real, and there is a documented case.** GitHub's Actions
notifications are run-scoped: "you'll receive a notification when any workflow runs that you've
triggered have **completed**" — a run that never fires produces no completion event, so that
channel structurally cannot surface silence.
https://docs.github.com/en/actions/concepts/workflows-and-actions/notifications-for-workflow-runs
The proof that this is not theoretical: a private repo's `*/5 * * * *` schedule produced **zero**
scheduled runs for a stretch in late January 2026 while manual `workflow_dispatch` worked
throughout, and a GitHub staff member confirmed on the record — *"We identified a related change
from last week that was rolled back today"* — advising a default-branch push to resync.
https://github.com/orgs/community/discussions/185373
A watchdog built on the same scheduler would have been broken by the same regression, at the
same time, with nothing to say so. **Stated plainly: the watchdog shares the failure mode**, and
no GitHub-native channel monitors the scheduler from outside the scheduler.

**(d) Current incident evidence.** 2026-07-22 (19:36–22:04 UTC), ~15% of hosted-runner workflow
runs delayed >5 min and ~1% failed to start; 2026-07-29 (14:51–15:28 UTC), ~2% of workflows
delayed on an under-provisioned internal Actions service. A primary-source post from GitHub's
own status account, 2026-07-19/20: "Actions self-hosted and larger runners were unable to
connect to GitHub. During this period, Actions jobs were delayed or failed when trying to
acquire a runner." https://x.com/githubstatus/status/2079681401146708254
(The two percentage figures are search-indexed summaries of githubstatus.com, which refused
direct fetches — treat them as likely-accurate but not independently re-verified; the X post
and the community discussion are primary.)

**Verdict: BUILD-thin** for the watchdog (no off-the-shelf Action does "detect silence → open
Issue"; the keepalive-Action family *prevents* disablement rather than *detects* silence).
**LEAVE** for who-watches-the-watchdog — no configuration closes it.

## Item 7 — `gh` CLI findings-as-Issues (P3). **ADOPT-candidate, but the issue-per-finding design is refuted.**

**(a) Version and commands.** `gh` **v2.97.0**, released **2026-07-31**.
https://github.com/cli/cli/releases/tag/v2.97.0
Create from a file: `gh issue create --title "<t>" --body-file <path>` (`-F`; `-` reads stdin).
Label at creation: `--label`/`-l`, repeatable. De-dupe search: `gh issue list --search "<query>"`.
Close: `gh issue close <n> [--comment "<text>"]`.

**(b) Self-diagnosis works.** `--log` and `--log-failed` are current and mutually exclusive
(`view.go`: "specify only one of --log or --log-failed"). Inside a workflow, `gh` authenticates
via `env: GH_TOKEN: ${{ github.token }}` — GitHub's own documented pattern — so
`gh run view ${{ github.run_id }} --log-failed` with `permissions: actions: read` is the
self-diagnosis loop. (That exact one-liner is an inference from two independently confirmed
building blocks, not a quoted worked example.)

**(c) The rate limit that decides this item.** Two numbers matter, and the smaller one is the
relevant one:

> "The rate limit for `GITHUB_TOKEN` is **1,000 requests per hour per repository**."

— not the 5,000/hour personal limit. And the secondary limits are what actually bite:

> "In general, no more than **80 content-generating requests per minute** and no more than
> **500 content-generating requests per hour** are allowed. Some endpoints have lower content
> creation limits."

https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api#secondary-rate-limits

**A real reported case lands almost exactly on this repo's numbers.** A user creating issues in
batches of 10, spaced 90 seconds apart, hit HTTP 403 — "You have exceeded a secondary rate limit
and have been temporarily blocked from content creation" — after roughly **100–150** successful
creations, while their *primary* limit still showed 4,820 of 5,000 remaining. No `Retry-After`
header; a reply confirmed secondary limits "cannot be increased or exempted."
https://github.com/orgs/community/discussions/50326

**Why that is decision-changing rather than a footnote:** `[#487]`'s parked set is **149
proposals**. An issue-per-finding emitter over that set sits inside the exact band where this
failure was observed, and it would fail *partway through* — leaving a half-emitted set with no
`Retry-After` to back off against. So P3 should batch findings into one Issue per run (or
comment on a standing Issue), not open one per finding.

**Verdict: ADOPT-candidate** for the mechanics; the issue-per-finding *shape* is refuted on
measured platform limits.

## 8. Coverage statement — items 1 and 2 were NOT delivered

**Items 1 (mutation testing — mutmut vs cosmic-ray, for B2) and 2 (prose linting — vale, for
B3) are missing.** The research lane assigned to them did not return within this batch's
window. This is a real gap, not a soft one, and it has two consequences the morning packet
repeats:

- **B2's brief carries no library verdict.** What is known from the repo rather than the web:
  `mutmut` appears nowhere in `pyproject.toml` today (grepped); the four candidate subject
  modules (`audit.py`, `validate_backlog.py`, `enforcement_coverage.py`,
  `canonical_freshness_gate.py`) all have dedicated test files; and the pilot's live evidence
  case is verified (§B2 of the prep packs). The open questions are exactly the ones that
  decide adoption: current maintenance state of both tools, `uv` compatibility, Windows
  behaviour, and — the critical one — whether runs can be scoped to selected modules, since a
  2228-test suite makes an unscoped mutation run impractical.
- **B3's brief carries no library verdict**, and its decisive question is untested: whether
  vale's rule types can express a **corpus-wide numeric ceiling** (the silent-rule ratchet's
  441 total across 57 files) or only per-file / per-scope counts. One relevant fact did surface
  from item 3's search and is recorded there: no Vale plugin does code-reference staleness, so
  the `doc_claims` overlap vale could plausibly cover is the *prose* half only.

Neither gap was smoothed over in the prep packs: both briefs carry `LIBRARY VERDICT: NOT
DELIVERED` with the specific unanswered questions listed, so the day lane knows exactly what
to run rather than inheriting a false green.

Other bounded coverage: the percentage figures in item 6(d) are search-indexed rather than
directly fetched (githubstatus.com refused fetches); the `gh --json` field enum in item 6(b)
was not pulled from source; and the private-repo applicability of the 60-day auto-disable in
item 6(a) is genuinely unresolved rather than resolved in either direction.
