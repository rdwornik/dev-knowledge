> **PROVENANCE — harvested cloud artifact, body VERBATIM below this header.**
> Lane `AUT-R4-A harness-evals-observability` | receipt id `cse_01KqSQp2TnL5LYU1KVbea6S6` | dispatched 2026-08-29, harvested 2026-08-29 by `Save-CloudSessionReport` (the `Harvest-Cloud` alias).
> Selection rule: the LONGEST assistant text, not the last — text #2 of 10 across 6 pages.
> Bytes written unchanged: **77,839**. Harvester DEVIATION: the report does not open with its own heading — the first heading is line 5; bytes written UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.

---

Research complete. Below is the artifact in full.

---

# AUT-R4-A — Foundations: independent harness · eval substrate · agent observability

**Lane:** AUT-R4-A · read-only cloud reconnaissance · dispatched 2026-08-29
**Repo:** `.dev-knowledge` @ `66662c7` (`main`), clean tree
**Rows born:** ZERO. No `tasks/` edit, no intake, no ADR, no commit, no push. This lane is read-only by contract.

**Gate declaration, per brief.** I ran no gate. `python3 scripts/audit.py checks` was attempted and **failed**: `ModuleNotFoundError: No module named 'click'` — the cloud image carries no synced env. I did not attempt `uv run --locked`. Every repo fact below comes from reading files with `python3`-era tools (`grep`, `sed`, `ls`), never from a gate verdict. **Consequence stated rather than smoothed:** I could not obtain the authoritative registered-check roster from `ALL_CHECKS`, so I cite the surface instead of a number (per CLAUDE.md §4 "never restate a count").

---

## PART 1 — THE HARNESS-PORTABILITY MAP (lead deliverable)

### Why this matters, stated as the brief requires

Today **Claude Code is both the producer and the harness**. It writes the diffs *and* it is the runtime that boots the lane, reads the contract, holds the worktree, and ends the session. That is a single point of dependency sitting under a doctrine that calls itself provider-agnostic. `ecosystem/provider-registry.yaml` admits six providers and `ecosystem/routing-table.yaml` routes by role — but `ecosystem/substrate-registry.yaml:32-79` lists the **executor verbs** for all four live substrates, and every one of them launches `claude`:

```
local-worktree   verbs: [dispatch, Dispatch-Local]   aliases: [Dispatch-Lane]
local-primary    verbs: [claude]                      aliases: []
cloud            verbs: [Dispatch-Cloud]              aliases: [Dispatch-CloudV2, Dispatch-CloudBrief]
codespace        verbs: [Dispatch-Codespace]          aliases: []
```

Provider-agnosticism is real at the **model** layer and absent at the **harness** layer. This map is the resilience test of that gap. **It is not a recommendation to switch** — see the verdicts.

### The map — per organ, portable vs CC-coupled

**Verdict key:** *portable* = survives a harness swap unchanged · *seam* = survives with a named, bounded adapter · *CC-coupled* = the organ's contract names Claude Code and would have to be re-authored.

```
ORGAN 1 — the gate stack (pre-commit / commit-msg / pre-push / audit.py)
  locator     .pre-commit-config.yaml (20 local hook ids) + scripts/audit.py + scripts/audit_checks/
  verdict     PORTABLE — fully, and this is the strongest result in the map
  evidence    every local hook is `language: system` with entry `uv run --locked python scripts/<x>.py`.
              Read at .pre-commit-config.yaml:47,54,60,68,81,93,120,136,149,160,172,184,203,251,259,269,
              275,284,297,313. Zero hook entries invoke `claude`, read a transcript, or depend on a
              session. Stages are pre-commit / commit-msg / pre-push — GIT lifecycle events, not agent
              lifecycle events.
  consequence a harness swap costs this organ NOTHING. The gates bind whoever holds the checkout.
              This is the load-bearing fact of the whole shelf: the repo's teeth are git-coupled,
              not harness-coupled, and were built that way (CLAUDE.md §5 rule 7, "LLMs advise;
              hooks/tests enforce" — PLAYBOOK.md:376).
  caveat      the ONE exception is the ruff hook (.pre-commit-config.yaml:319-328), a pinned remote
              rev — also harness-neutral.

ORGAN 2 — frozen lane contracts
  locator     scripts/gen_lane_contract.py; MANDATORY_SECTIONS at :133; hook `lane-contract-check`
              at .pre-commit-config.yaml:235-252
  verdict     SEAM — the document is portable; ONE baked-in region is CC-coupled
  portable    the frozen-contract CONCEPT and most mandatory sections (decision budget, worktree<->file
              pairing, receipt-gate fields, the What-NOT-to-do close). None of these name a vendor.
  CC-coupled  the `## Dispatch` block. The generator BAKES IN the literal command line and selects it
              from the declared shape (gen_lane_contract.py:344,347): `Dispatch-CloudV2 <file>
              -Title '<slug>'` or `Dispatch-Lane <slug> <file> -Effort <tier>`, with dispatch
              constants `--permission-mode bypassPermissions`, `--bg`, and `opus` as the model
              default. The check leg REFUSES a contract without one of exactly three forms
              (gen_lane_contract.py:615-616). A contract naming `opencode run` is a REFUSAL today.
  swap cost   ONE enum widening in one module + its tests. Bounded and small. The generator is
              already shape-selecting, so a fourth shape is the same edit the cloud shape was.

ORGAN 3 — the PLAYBOOK Ch8 dispatch table
  locator     protocols/PLAYBOOK.md:2470 "### Dispatching a session"; the table's own claim is that
              it is "the only place in the repository that carries a literal launch command"
  verdict     CC-COUPLED, deliberately and by design — and this is the organ a swap actually costs
  evidence    Layer-1 routing (Q1-Q4) is substrate logic and PORTABLE: Q1 gate-dependency, Q2
              operator-disk, Q3 read-only recon, Q4 everything else — none of that names a vendor.
              Layer-2 is the coupling: three verbs, all launching `claude`, implemented in a
              PowerShell module the hub does not carry (win-tooling
              `config/dispatch-helpers/DispatchHelpers.psm1`, per PLAYBOOK.md:2481-2494).
  swap cost   the module is OUTSIDE this repo, on the operator's disk, at L0. So the swap cost is
              real but it is NOT this repo's to pay — and that is a finding, not a relief: the
              single most harness-coupled organ in the fleet is the one the hub cannot gate.
  honest      the table's own history is the argument for keeping ONE literal site: four rival
              commands, ~thirty consecutive failed browser launches, measured at
              docs/audits/2026-08-25-technical-dispatch-surface-measured.md (2083 lines). A swap
              that reintroduces rival commands re-buys that failure.

ORGAN 4 — worktree lanes
  locator     protocols/PLAYBOOK.md:1404 "### Parallel sessions & worktree discipline (per ADR-61)";
              branch enum in CLAUDE.md §4 and AGENTS.md "Landing a change"
  verdict     PORTABLE in mechanism, SEAM in naming
  portable    the rule is "one checkout = one COMMITTING session" (PLAYBOOK.md:1411) — a git-concurrency
              invariant. It is true of any agent, any human, any harness. So is the
              suite-and-commit-in-the-same-tree rule (PLAYBOOK.md:1413, the [#382] W3 phantom RED).
  seam        the branch-prefix enum is a closed set with machine-produced lane prefixes
              `worktree-` / `epic/` / `claude/` / `automation/`. `claude/<slug>` is a VENDOR NAME
              baked into a gated enum (checkable at scripts/validate_branch_naming.py). A second
              harness needs either a fifth prefix admitted by recorded ruling, or it reuses
              `worktree-`.
  honest      the live-session check (PLAYBOOK.md:1450+) IS CC-coupled at the mechanism level:
              "transcript-cwd is authoritative … ~/.claude/projects/<mangled-cwd>/*.jsonl plus a
              `cwd` grep", and the section states process inspection CANNOT answer it. A second
              harness with a different (or absent) transcript layout leaves this check with no
              implementation. This is the sharpest hidden coupling in the map and it is a SAFETY
              check, not a convenience one.

ORGAN 5 — lane packets (the hand-back artifact)
  locator     docs/audits/2026-08-29-technical-nb2-n-packet.md (shape: §0 ex-ante verbatim,
              §1 per-done-item verdicts, §2 SHAs, §3 external-review tally, §4 candidates REPORTED
              not filed, §5 budget, §6 deviations, §7 test state, §8 STOP)
  verdict     PORTABLE — entirely. It is markdown with SHAs. Nothing in it names a harness.

ORGAN 6 — skills / commands / plugin (.claude/**)
  locator     .claude/skills/ = {verify, check-against-spec}; .claude/commands/ (8 files);
              plugin tier1-lifecycle@dev-knowledge-methodology
  verdict     CC-COUPLED by file format, PORTABLE by content
  honest      `.claude/` is a Claude Code directory contract. The KNOWLEDGE inside is markdown and
              moves; the invocation surface does not. Note the fleet already proved the portable
              half is achievable: ADR-115 landed root AGENTS.md as the portable instruction layer
              (103 lines, 5,270 B) precisely so a second provider could read the doctrine.
```

### One-paragraph reading of the map

**The repo is far more harness-portable than its doctrine assumes, and the coupling is concentrated in exactly three places:** the `## Dispatch` block the contract generator bakes in, the Ch8 Layer-2 verb table (which lives at L0, off this repo), and the transcript-cwd live-session check. Everything with teeth — the 20 gates, `audit.py`, the branch discipline, the packets — binds git, not Claude. **A harness swap is a dispatch-layer project, not a governance-layer project.** That is a good result and it was not guaranteed.

---

## SHELF 1 — INDEPENDENT HARNESS

### Candidate 1.1 — OpenCode

```
what it is       terminal-native open-source coding agent: tool loop, session management,
                 plan/build agents, TUI + desktop + IDE extension
repo             github.com/anomalyco/opencode  (MOVED — see negative signal below)
license          MIT
signal           202.3k stars; 15,602 commits on dev; TypeScript
cadence          v1.18.16 (Aug 10 2026) -> v1.18.25 (Aug 28 2026) = 10 releases in ~18 days
evidence tier    practiced (adoption is real and observable); the star/commit figures are MEASURED
                 off the repo page, 2026-08-29
Windows/uv       N/A to uv — it is a Node/TS binary, not a Python dependency. It never touches
                 pyproject.toml or uv.lock, so ADR-106's pinned-uv constraint is NOT engaged.
                 That is a point IN ITS FAVOUR under the carried constraint.
self-hosted      yes, fully local, MIT. Scores ABOVE SaaS-only per the brief's rule.
```

**Negative signal, and it is first-class.** The canonical repo is now `anomalyco/opencode`; `sst/opencode` is a redirect. The move is real (issue #16440 on the new org references the stale `sst/opencode` path). *Search result, 2026-08-29; I did not find a maintainer post announcing it.* SST rebranded to Anomaly and took the project with it. For a swap decision this matters: **the governance of your fallback harness changed hands within the last year, and a 1–2-day release cadence means you would be pinning a fast-moving target** — the same hazard ADR-106 already names for `uv` ("pre-1.0 and ships ~every three days with behavioural drift in point releases").

**How it transfers to THIS repo — plainly.** OpenCode reads `AGENTS.md` natively (already recorded in-repo at `docs/audits/2026-08-25-technical-research-agents-md-standard.md:49`: *"Reads both AGENTS.md and CLAUDE.md; AGENTS.md wins"*). So the portable instruction layer ADR-115 landed **already points at it**. It would boot into a checkout, read `AGENTS.md`, and be bound by all 20 gates without any change. What it would NOT do is satisfy the `## Dispatch` block enum, or leave a `~/.claude/projects/**` transcript for the live-session check.

**Verdict: `absent`.** Searched `ecosystem/substrate-registry.yaml` (all four substrates' `verbs`/`aliases`), `ecosystem/provider-registry.yaml` (`cli:` field per provider — `claude`, `codex`, `grok`, …), `scripts/gen_lane_contract.py` (`LOCAL_RE`/`CLOUD_RE`), and `.pre-commit-config.yaml`. **No non-Claude executor is admitted anywhere.** Not found.

**Prior verdict — reconciled.** `docs/audits/2026-08-25-technical-research-agents-md-standard.md` evaluated opencode as an **AGENTS.md READER** (an instruction-compatibility question) and `JOURNAL.md:1948` records the provider roster deliberately NOT inflated to include it. It has **never** been evaluated as an *executor*. That is a genuinely new question at today's scale, not a relitigation.

**Cheapest experiment that would settle adoption (Tier S — try and keep or delete).** Not "pilot it". Concretely: **install OpenCode, point it at a throwaway worktree of this repo, and give it one already-completed lane contract with the `## Dispatch` block deleted. Measure exactly two things: (1) does the commit it produces pass all 20 pre-commit hooks unaided; (2) does `block-unanchored-push` refuse its push.** One afternoon. If both hold, the gate stack's portability claim above is proven rather than inferred, and the swap cost is confirmed as dispatch-layer only. If either fails, you have found a coupling this map missed. **Delete the worktree either way** (CLAUDE.md §5 rule 9).

### Candidate 1.2 — `pi` (pi.dev / `earendil-works/pi`)

```
what it is       minimal coding-agent harness: unified multi-provider LLM API, agent loop, TUI,
                 coding-agent CLI. Explicitly a rebuttal to large harnesses.
repo             github.com/earendil-works/pi
license          MIT
signal           ~99k stars; 5,826 commits; 72 open issues; TypeScript/Node
evidence tier    practiced. The "~200-token system prompt / 37+ models / 20+ providers" figures come
                 from SECONDARY blog coverage (silenceper, luismori, Koenig AI Academy — all
                 May-Jun 2026) and I did NOT verify them against the repo. Treat as unverified.
Windows/uv       N/A to uv (Node). Same neutral posture as OpenCode.
self-hosted      yes, MIT, local.
```

**Why it is here and why it is second.** `pi` is the *architecturally* interesting peer for this repo specifically, because its thesis — the harness should be small and the model should carry the weight — is the mirror image of what `.dev-knowledge` does. This repo puts enormous weight in the *instruction and gate layer* and treats the harness as interchangeable. A minimal harness is the natural partner for that. But it is younger, has a smaller commit base than OpenCode, and its supporting evidence is blog-tier.

**Verdict: `absent`** (same search as 1.1). **Cheapest experiment:** identical to 1.1's, run as the *second* arm only if OpenCode's arm passes — running both first is spending twice for one bit of information.

### The `"PPI"` question — answered honestly

**Unknown as a literal referent.** I searched `"PPI" AI agent harness coding agent acronym 2026` and `"PPI" agent framework open source 2026 harness OR runtime OR protocol acronym meaning`. **No product, framework, protocol or repo named "PPI" exists in the agent-harness space** in anything I could reach.

Two real referents sit adjacent, and I name them as *candidates, not as the answer*:

- **`pi`** (pi.dev, candidate 1.2 above) — the only agent-harness object whose name is a substring of "PPI", and it sits exactly where the brief placed the question (next to OpenCode, Shelf 1). This is my best guess and it is a **guess**, offered so the operator can confirm or reject it.
- **Prediction-Powered Inference (PPI)** — a real, well-established statistical method (Angelopoulos et al.; StratPPI at NeurIPS 2024; and a 2026 line of work applying it to LLM-judge evaluation, e.g. arXiv 2606.05308 "Statistically Reliable LLM-Based Ranking Evaluation via Prediction-Powered Inference"). It combines a small human-labelled gold set with a large LLM-judged set to produce provably unbiased estimates with tighter confidence intervals. **This is genuinely relevant — but to Shelf 2, not Shelf 1.** It is the published answer to SDA-1's C-2 problem (uncalibrated floors against absent baselines) and to the hand-scoring cost the adversarial review flags at line 322.

**I did not pick one.** The brief says do not invent a referent, and both of these are inferences from phonetics and adjacency, not verifications.

---

## SHELF 2 — EVAL SUBSTRATE

### First: a correction to the brief's premise, with a source

The brief groups **"Harbor … plus SkillsBench and kin"** as one family. **They are two rival substrates, not one.**

- **Harbor** = `laude-institute/harbor`, the Terminal-Bench team's framework. Terminal-Bench 2.0 is distributed via the **Harbor registry** (`harbor run -d terminal-bench@2.0`).
- **SkillsBench** = `benchflow-ai/skillsbench`, which runs on the **BenchFlow SDK** (`uv tool install benchflow`), a separate project at `benchflow-ai/benchflow`. Its task packages are "native BenchFlow `task.md` packages". Fetched from the repo page 2026-08-29: it **does not depend on Harbor**.

This matters for adoption: choosing Harbor does not get you SkillsBench, and choosing BenchFlow does not get you Terminal-Bench. Evidence tier: **measured** (both repo pages read directly).

### Candidate 2.1 — Harbor

```
what it provides task/trial/verifier abstraction; sandbox provisioning per trial; the agent
                 interaction loop; verifier checks producing reward files + logs; a task registry;
                 scale-out to many parallel containers
repo             github.com/laude-institute/harbor   license Apache-2.0
signal           4.8k stars; 1,553 commits; 237 open issues; 539 open PRs
release          PyPI `harbor` 0.22.0 (Aug 22 2026); prior 0.21.0 (Aug 10), 0.20.0 (Jul 18),
                 0.19.0 (Jul 17), 0.18.0 (Jul 7) — roughly monthly-to-fortnightly minors
python           requires-python >=3.12
wheel            py3-none-any (PURE PYTHON, platform-agnostic)
agents supported Claude Code, Codex, Gemini CLI, OpenHands, others
sandboxes        Daytona, Modal, E2B, Blaxel, Novita, Tensorlake, self-managed Kubernetes; Docker
                 for local
evidence tier    measured (GitHub + PyPI pages, read 2026-08-29)
```

**Windows / `uv 0.11.19` — first-class assessment, as the brief requires.** The wheel is `py3-none-any` and `requires-python >=3.12`; this repo is `.python-version 3.12.10`, `requires-python = ">=3.12"`. **There is no wheel risk at all — the `rustworkx` bar is not even approached, because there is nothing to compile.** But installability is the *easy* half and I will not let it carry the verdict:

- **The real constraint is Docker, not wheels.** Local Harbor runs need Docker ("This will launch the benchmark locally using Docker"). On the operator's Windows host that means Docker Desktop — a heavyweight, always-on dependency this repo has never taken. **Per the brief's rule: this scores AGAINST it.**
- **The alternative to Docker is worse under the same rule.** The cloud sandbox providers (Daytona, Modal, E2B) are all **SaaS**. Choosing Harbor without Docker means choosing SaaS, which scores against it a second time.
- **Do NOT put Harbor in `pyproject.toml`.** If adopted it belongs as `uv tool install harbor` — a tool-level install, isolated from the project environment, touching neither `uv.lock` nor the `==0.11.19` pin. This is the shape that costs no ADR-106 dependency act. Stating it because getting this wrong is how a cheap experiment becomes a gated change.
- **539 open PRs against 1,553 commits** is a maintenance shape worth naming. It is not abandonment — the release cadence is healthy — but it signals a project absorbing contributions faster than it merges them.

**Reconciliation against `sol`'s C-6/C-15 — LOCATED, not unlocatable.**

- **C-6** is at `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md:305`: *"Green-by-skip is the highest-scoring cheat and the design gates it with a diff filter."* The named build cost is its fix (ii): *"add a **second, adversarial suite** whose tests were written to break exactly the four cheats … Note honestly: (ii) is a real build cost and it is the difference between a benchmark that ranks providers and one that ranks their willingness to game."*
- **C-15** is at `:372`: the criterion has no named owner, and *"the repeat factor (C-4), the second adversarial suite (C-6) and the incumbent re-measurement (C-2) are the three things that will be cut"* under time pressure.

**Now the answer the brief actually wants, and it cuts against the framing.** Harbor would **not** relieve the C-6 cost. C-6's cost is **authoring adversarial test content** — tests that catch a broad `try/except` swallowing the asserted exception, a defaulted return making an assertion vacuous, a feature-flag reroute, a hardcoded fixture value. Harbor supplies the *plumbing* around a verifier (container, trial, reward file, parallelism, registry); it does not supply the verifier's *content*. **So: Harbor removes the harness build cost that `sol` did not flag, and leaves untouched the one it did.**

What Harbor **would** relieve, concretely, is the plumbing this repo hand-rolled in `scripts/nopack_sandbox.py` — provisioning a disposable clone, a command allowlist, teardown-with-provenance-check, and the Layer A/B answer-key guards. And the module's own stated limits are exactly the limits a container removes: *"`teardown`'s provenance is checked immediately before deletion, but a check and an `rmtree` are two syscalls. Closing that gap needs no-follow traversal from a directory descriptor, **which Windows does not offer portably**"*, and *"The marker and the root registry are both files. Someone who can write to the sandbox root can forge both."* A per-trial container has neither problem. **That is the honest case for Harbor and it is a real one.**

**Verdict: `partial`.** The organ exists — `scripts/nopack_sandbox.py`, the SDA-1 design at `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` (preconditions Q0–Q7 at §2), and the item packs at `docs/audits/2026-08-29-technical-sda1-analysis-role-item-pack.md`. **Precisely what is missing:** (a) a trial abstraction — SDA-1 runs one provider once per role, with no repeat factor, which is C-4's finding; (b) any parallel runner; (c) container isolation, so the sandbox's two stated Windows-specific holes stay open; (d) a machine-readable reward/result artifact — today the output is a hand-authored packet; (e) a registry, so a pack is a path in `docs/audits/` rather than an addressable version.

**Cheapest experiment that would settle adoption (Tier S).** `uv tool install harbor`, then **port ONE existing SDA-1 fan-out item — the role the adversarial review declares safe to run ("It is safe to run for fan-out", §10) — into a Harbor task with its verifier, and run it locally under Docker.** Success criterion, frozen before the run per ADR-108 §B: *the Harbor trial reproduces the same verdict the hand-run produced on the same item, and the container-provisioning path replaces `nopack_sandbox`'s two documented Windows holes.* If Docker Desktop is not acceptable on the host, **that alone kills it** and the experiment is a one-hour negative result rather than a project. Do NOT port the producer role — §10 says SDA-1 is not safe to run for producer, and porting an unsound benchmark to a better harness produces a faster wrong answer.

### Candidate 2.2 — SkillsBench / BenchFlow

```
what it provides a skills-evaluation benchmark (87 public tasks in v1.1) + the BenchFlow SDK task
                 format: tasks/<id>/{task.md, environment/Dockerfile, skills/, oracle/solve.sh,
                 verifier/test.sh + test_outputs.py}
repo             github.com/benchflow-ai/skillsbench   license Apache-2.0
signal           1.7k stars; 456 commits; 49 open issues
install          `uv tool install benchflow` + `uv sync --locked`  (the repo itself uses uv.lock)
prereq           Modal cloud sandbox (DEFAULT) or Docker for local; API keys for target models
evidence tier    measured (repo page, read 2026-08-29)
```

**The published finding — verified, and one number in the brief needs a footnote.** From the SkillsBench abstract (arXiv **2602.12670**, Feb 2026, Xiangyi Li et al.), quoted verbatim via `AkihikoWatanabe/paper_notes#4591` because **arxiv.org is blocked by this session's egress proxy** — flagged as a verification limit, not smoothed:

> *"a benchmark of 86 tasks across 11 domains paired with curated Skills and deterministic verifiers … We test 7 agent-model configurations over 7,308 trajectories. Curated Skills raise average pass rate by **16.2 percentage points (pp)**, but effects vary widely by domain (**+4.5pp for Software Engineering to +51.9pp for Healthcare**) and **16 of 84 tasks show negative deltas**. **Self-generated Skills provide no benefit on average**, showing that models cannot reliably author the procedural knowledge they benefit from consuming. Focused Skills with 2–3 modules outperform comprehensive documentation."*

**The brief's numbers are correct. Three corrections/refinements the brief did not carry, and each changes what it means for us:**

1. **The 16.2 pp is an average over 11 domains that range from +4.5 to +51.9.** For **Software Engineering — our domain — the effect is +4.5 pp**, the *lowest* in the study. Carrying "+16.2 pp" into a decision about *this* repo's skills overstates the expected gain by roughly 3.6×.
2. **16 of 84 tasks showed NEGATIVE deltas.** Roughly one task in five got *worse* with a curated skill. A skill library is not monotonically good.
3. The abstract says "86 tasks" and then "16 of 84". **That inconsistency is in the published abstract**, not introduced here. The repo page says 87 tasks in v1.1. Worth re-verifying against the paper body.

**SkillAxe — the published fix.** arXiv **2606.10546**, "SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement". Unsupervised iterative diagnose-and-refine over four dimensions (quality impact, trigger precision, instruction compliance with fault attribution, solution-path coverage). Reported: **+28% relative over unimproved LLM skills, closing 47–67% of the gap to human-authored skills.** **Evidence tier: measured, but at one remove** — arxiv.org is blocked here, so these figures come from a search result quoting the abstract, not from the abstract itself. **Flag for re-verification.**

**Does the brief's consequence hold? — "a prompt/skill distiller without an eval loop ships a useless library."**

**It holds, but not for the reason stated, and the correct reason is stronger.** The brief's reasoning is "LLM-authored skills give no measurable gain, therefore you need an eval loop." That is true and it is the weaker half. The stronger reason is **finding (2) above: one task in five got worse.** A distiller with no eval loop does not ship a *useless* library — a useless library is neutral. It ships a library with **an unmeasured negative tail**, and this repo's whole doctrine is built against exactly that failure class (`ecosystem/trends.html`'s ABSENT panels; the "green that means nothing" rule at PLAYBOOK.md:1450+; ADR-108 §B's frozen ex-ante criterion). **Restate the consequence as: without an eval loop, a distilled skill library is an unmeasured change to the always-on instruction surface — the surface intake #35 already says degrades under density (IFScale: 68% adherence at 500 instructions).**

**Second-order consequence, which is the one that actually binds here.** This repo has **two** skills (`.claude/skills/verify`, `.claude/skills/check-against-spec`). At n=2, the SkillsBench result does not justify building an eval loop — it justifies **not building a distiller yet**. The finding kills the *distiller* more cheaply than it justifies the *eval loop*.

**Verdict: `absent` for a skills-eval corpus.** Searched `tasks/` (`ls tasks | grep -i "eval|bench|skill"` → returns rows about *evaluating hooks*, *mutmut*, *the verify skill's output contract* — none is a skill-effectiveness eval), and `.claude/skills/` (two skills, no eval fixtures). Not found.

**Reconciliation — and this is the important one.** The general capability is **NOT unevaluated**. **Prior verdict located** at `docs/audits/2026-08-19-technical-n3-ratification-pack.md:311`, §3.4 "Not born, and why":

> *"**R3** (promptfoo rule-adherence harness) — accepted in principle, **not born**, on the intake's own kill-candidates line: *'propose FOLDING into that corpus rather than birthing a second one'*. The corpus is the one gating `[#491]` (open) and `[#492]` (deferred). Filing a second eval corpus alongside it is the duplication ADR-111 outcome (a) exists to prevent."*

The source intake is `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md` (**intake-id 35, `status: DRAFT`**), whose R3 done-when reads: *"`npx promptfoo eval` runs ≥10 cases encoding non-negotiables from `~/.claude/rules/core-invariants.md` and exits non-zero below a declared threshold; a deliberately-weakened instruction set FAILS the run."*

**Re-assessed at today's scale:** the ruling stands and SkillsBench *strengthens* it. The fold-into-the-existing-corpus decision was made to avoid a second eval corpus; SkillsBench/BenchFlow would be a **third**. **Per ADR-111 this shelf's finding is OWNED, not CANDIDATE** — R3 covers it, and the correct act is to attach the SkillsBench evidence to R3, not to birth a row.

**Windows/uv:** BenchFlow installs as a uv tool (pure-python path; no wheel risk observed). **But its default sandbox is Modal — SaaS — with Docker as the local fallback. Scores against it on both limbs of the brief's rule, same as Harbor.**

**Cheapest experiment (Tier S).** **Do not install BenchFlow.** The cheapest experiment that settles this is *not* a tool install: **take the ≥10 non-negotiables R3 already enumerates from `~/.claude/rules/core-invariants.md`, and hand-run them once against the two live skills.** If fewer than 10 produce a decidable pass/fail by hand, the harness question is premature. If 10 do, R3's promptfoo shape is already specified and already ruled — build that, not a third substrate. Cost: one session, zero dependencies, zero SaaS.

### Candidate 2.3 — `nasde` / `nasde-toolkit` — **RESOLVED, and it is the most on-target find on this shelf**

The brief flagged `noesisvision.com` "nasde" as unknown to both operator and architect. **It resolves.**

```
what it is       "CLI for benchmarks & evals of AI coding agents — on tasks you already understand,
                 using your Claude / Codex / Gemini individual subscriptions or API keys."
                 Positioning: "Measure how your whole AI coding setup performs — and what it costs
                 in tokens and dollars across models and providers — so you can choose where to
                 invest and when to switch."
repo             github.com/noesisvision/nasde-toolkit   (org also ships P3-model, 64 stars)
site             noesis.vision/nasde/  — BLOCKED by this session's egress proxy; all facts below
                 come from the GitHub org + repo pages, read 2026-08-29
license          MIT
signal           12 stars; 141 commits; 1 open issue; Python; last updated Aug 24 2026
install          `uv tool install nasde-toolkit --python 3.13`
python           3.13 recommended, 3.12 supported. "Python 3.14 is not yet supported — a transitive
                 dependency hasn't released cp314 wheels."
depends on       HARBOR (sandbox orchestration via Docker or cloud) + Opik (optional dashboard)
                 + an already-authenticated Claude/Codex/Gemini CLI
workflow         describe task w/ criteria -> agent solves in sandbox -> REVIEWER AGENT scores
                 against your criteria -> optional dashboard
measures         quality across custom rubric dimensions (e.g. domain modeling, test quality),
                 token consumption per model/provider, dollar cost per run, pass/fail
evidence tier    measured for the repo metadata; ASSERTED for the capability claims (they are the
                 project's own README; nobody has independently evaluated this)
```

**Why this is the most on-target object in the whole survey.** It is, almost line for line, **SDA-1 as a shipped tool** — including SDA-1's Q7 cost meter (*"tokens in/out, wall-clock, rounds, and $ per item per lane"*), which the adversarial review's **C-1 (CRITICAL)** identifies as the axis the operator's actual goal lives on: *"The operator's goal is cutting coding cost … Sections 4.2 P1–P4 measure correctness … A provider can clear P1–P4 and P6 and still be a net cost increase."* nasde measures **cost and quality together, per model, per provider, on your own tasks, using subscription auth**.

**And it is not a rival to Harbor — it is a Harbor consumer.** So the Harbor experiment above and this one share a substrate.

**Sober counterweights, stated because 12 stars is 12 stars.**
- **12 stars / 141 commits / one maintainer-scale org.** This is a personal project, not an ecosystem. **Abandonment risk is high** and MIT means you would be forking it, not depending on it.
- **It inherits Harbor's Docker requirement** — same score-against.
- **It uses a REVIEWER AGENT to score.** That is exactly the design SDA-1's C-6 attacks and exactly where PPI-style calibration would be needed. An LLM scorer with no gold-set calibration is the "confidently wrong verdict" failure the adversarial review exists to find.
- Every capability claim is the project's own README. **Nobody has verified it. Neither have I.**

**Verdict: `partial`.** The organ exists as a **design with no runnable instrument**: `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` (design + 15-finding critique), `scripts/nopack_sandbox.py` (the guard), `ecosystem/provider-registry.yaml` (the providers), `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md` (the cost model). **Precisely what is missing:** a runner that executes the four-step loop and emits a cost-and-quality record. Every ingredient is designed; none is wired.

**Cheapest experiment (Tier S).** **`uv tool install nasde-toolkit --python 3.12` and run it once on ONE task the operator already knows the answer to, against ONE provider pair.** Frozen success criterion: *it produces a per-model token+dollar figure and a rubric score without the operator hand-scoring anything.* If it does, it discharges SDA-1's Q7 leg for the cost of an install and turns C-1 from a build into a configuration. If it needs a Docker daemon the host won't run, or the reviewer-agent score is unreproducible across two runs of the same input, **delete it and record the negative result** — that is Tier S working correctly.

---

## SHELF 3 — AGENT OBSERVABILITY

### The live incumbents — read, not assumed

```
INCUMBENT A — the telemetry store
  locator   scripts/telemetry_emit.py  ->  logs/TELEMETRY.db  (SQLite, WAL, gitignored)
  schema    events(id, ts, event_type, name, outcome, duration_ms, context_json, run_id)  [:194-205]
  events    check_run / hook_run / blocker_fired    (emit_check_run, emit_hook_run,
            emit_blocker_fired)
  state     LIBRARY ONLY. The module says so itself at :12-18: "it wires nothing. No check, no hook,
            no dispatcher calls into this module yet … A grep for `telemetry_emit` outside this file
            and its test is expected to return nothing today."
  on disk   logs/ contains ONLY TOKEN-LOG.md on this clone. The store does not exist here.
  open rows [#575] store perf + SILENT DROPS (16.4 ms/event = 98.5% of an emit; 8 concurrent writers
            produced `database is locked` and safe_emit swallows it); [#576] read path — "no consumer,
            no query, no dashboard". BOTH OPEN.

INCUMBENT B — trends.html
  locator   scripts/gen_trend_dashboard.py -> ecosystem/trends.html (GITIGNORED, never committed)
  shape     9 panels, inline SVG on stdlib, pure ASCII by construction, direction verdict per panel
  series    open rows / banked ledger / velocity / boot bytes / doc-rot / funnel orphans
  ABSENT    "commit-gate ms" (source: logs/TELEMETRY.db events.duration_ms — ABSENT),
            "suite wall-time" (-- no store exists --), "per-model quality" (-- no store exists --)
  doctrine  "a chart of invented history is worse than no chart, and the two 'no store exists' rows
            are findings this surface exists to make visible rather than gaps it should quietly
            paper over."  [gen_trend_dashboard.py:38-40]

INCUMBENT C — lane packets
  locator   docs/audits/*-packet.md (e.g. 2026-08-29-technical-nb2-n-packet.md)
  captures  ex-ante criterion verbatim vs measured result w/ named witness; per-done-item verdicts;
            commit SHAs in order; external-review tally; deviations WITH OWNERS; test state; budget
  nature    the VERDICT LAYER. Hand-authored, immutable, git-stored.

INCUMBENT D — "the quota-source field"  ->  UNLOCATABLE AS A FIELD
  searched  `quota`, `quota_source`, `quota-source` across *.py *.md *.yaml *.json (repo-wide,
            excluding .git). Hits are PROSE ONLY: batch quota buckets (feature/process/satellite
            split, JOURNAL.md:11885,12034,12098), provider quota volatility notes
            (ecosystem/provider-registry.yaml:141, PLAYBOOK.md:4059), and handoff notes.
  also      inspected ecosystem/provider-registry.yaml keys (display_name, council_alias, cli,
            version_command, changelog_tool_key, changelog_source_url, marketplace_id,
            marketplace_source_path) and ecosystem/substrate-registry.yaml keys — NO quota field.
  verdict   NOT a field. Nearest live structured surfaces: the batch manifest's bucket labels
            (scripts/batch_manifest.py) and telemetry's freeform context_json column.
            Flagged for the operator to name what he meant.
```

### Testing the verdict frame — *"buy the collector and the tracing, keep our verdict layer"*

**The frame is right about the verdict layer and wrong about what the collector would buy.** Here is the attack, and I think the evidence goes against the framing:

**Phoenix, Langfuse and LangSmith are stores for LLM SPANS. `telemetry_emit` is a store for GATE EVENTS.** The incumbent's three event types are `check_run`, `hook_run`, `blocker_fired` — a pre-commit hook firing, an audit check passing, a push being refused. **None of these is a model call.** There is no prompt, no completion, no token count, no model id, no latency-of-inference. Mapping `hook_run("block-unanchored-push", "block", 44)` onto `gen_ai.*` semantic conventions is a category error: the GenAI conventions describe *inference operations*, and this store describes *governance operations*.

**Therefore:** buying Phoenix or Langfuse **would not discharge `[#575]` or `[#576]`.** `[#575]` is "our SQLite store drops events under 8 concurrent writers"; `[#576]` is "no consumer, no query, no dashboard over gate events grouped by `run_id`". A GenAI span store answers neither, because it is not holding that data. **The frame's "buy the collector" half is buying a solution to a problem this repo does not currently have** — and `[#576]`'s own done-when enforces the ADR-105 named-consumer rule: *"the question and its consumer named before the query is built"*. There is no named consumer for LLM spans in this repo today.

**Where the frame IS right, and it is worth saying clearly:** the verdict layer (packets → rulings) is genuinely not for sale. Nothing on this shelf produces an "Ex-ante clause / Measured result / Witness" table with named deviation owners. Keep it. That half needs no defending — it was never at risk.

**The one thing on this shelf that IS worth buying, and it is not a product:** **the OTel GenAI semantic conventions as an emission target *if and when* Claude Code's own OTel export gets wired.** That is a different question from "adopt an observability platform", and the repo already holds the research (`docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md` §1: the 8 metrics and 25+ events Claude Code emits under `CLAUDE_CODE_ENABLE_TELEMETRY=1`).

### Candidate 3.1 — OpenTelemetry GenAI semantic conventions

```
what it is       vendor-neutral conventions: spans, metrics, events for GenAI clients, MCP, and
                 provider-specific conventions
repo             github.com/open-telemetry/semantic-conventions-genai  (625 commits)
status           DEVELOPMENT — NOT stable. Split out of the main semconv repo at v1.42.0
                 (June 12 2026). As of mid-2026 no gen_ai.* attribute/span/metric/event is Stable.
                 The repo's own Schema URL section reads "TODO".
core metrics     gen_ai.client.token.usage (histogram), gen_ai.client.operation.duration
Windows/uv       N/A — it is a SPECIFICATION, not a package. Zero installability cost. This is the
                 highest-scoring candidate on the carried constraint by a wide margin.
self-hosted      N/A — a convention is neither.
evidence tier    measured for the repo/split facts; the "core chat + embeddings attributes are
                 stable enough to build on" claim is ASSERTED (secondary blog, May 2026)
```

**Error-handling and usage-stats coverage — explicit, as the brief requires.**
- **Captures:** token usage split by type; operation duration; model/provider identity; operation errors via standard OTel `error.type` on the span; MCP tool calls; agent/tool-orchestration spans (still settling).
- **Drops:** nothing about a *gate*. No hook outcome, no blocker, no check result. Also drops **cost in dollars** — the convention has token counts, not currency; dollar figures require a price catalog join (LiteLLM's, per the repo's own prior research).

**Verdict: `absent`.** Searched `gen_ai`, `opentelemetry`, `otel`, `otlp` (case-insensitive) across `scripts/`, `ecosystem/`, `tasks/`, `.claude/`. **Exactly one hit and it is a false positive** — `scripts/single_flight.py:61` matches "otel" inside "remotely". **Zero OTel awareness anywhere in the codebase.** Not found.

**Reconciliation.** Prior verdict located at `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md:13` and its anti-pattern list: *"❌ Hard-coding OTel `gen_ai.*` attribute names — they're pre-stable (Development status, June 2026 repo split); isolate behind a mapping layer."* **Re-assessed at today's scale: unchanged.** Nine months on, still Development. The prior verdict was "adopt the convention, don't hard-code it" and nothing has moved to make it stable.

**Cheapest experiment (Tier S — and it is nearly free).** **Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` with a file exporter for ONE session, and look at what lands.** No collector, no server, no dependency, no Docker. Frozen criterion: *does the emitted stream contain a field that answers a question `[#576]` names, that `logs/TELEMETRY.db` cannot answer?* If yes, there is a real second store and the Shelf-3 conversation becomes concrete. If no — and my reading of the schemas says no — **the whole shelf is discharged for the cost of one environment variable**, and that is the highest-value hour on this entire artifact.

### Candidate 3.2 — Arize Phoenix

```
what it provides tracing, evaluation, datasets, experiments, playground, prompt management
repo             github.com/Arize-ai/phoenix  — 11.2k stars, 9,789 commits, 824 open issues
license          ELASTIC LICENSE 2.0 (ELv2) — NOT an OSI-approved open-source licence. Free to
                 self-host and use; forbids offering it as a managed service. Called out because
                 "open-source" in the marketing does not mean OSI here, and this repo's fleet
                 records licences (ecosystem/dependency-baseline.yaml).
release          PyPI arize-phoenix 20.4.0 (Aug 26 2026); 20.3.0 (Aug 17), 20.2.1 (Aug 14),
                 20.2.0 (Aug 13), 20.1.0 (Aug 12) — ~weekly minors. Very active.
python           >=3.10, <3.15   wheel: py3-none-any (PURE PYTHON)
self-host        `pip install arize-phoenix && phoenix serve`. Runs locally, in a notebook, in
                 Docker, or K8s via Helm. "no usage limits, no required API keys, no phone-home
                 telemetry" (vendor claim — ASSERTED).
standards        built on OpenTelemetry; maintains the OpenInference spec; instrumentation for
                 Python, TypeScript, Java, Go
evidence tier    measured (GitHub + PyPI, read 2026-08-29); self-host claims are vendor-asserted
```

**Windows/uv:** `py3-none-any`, Python 3.12 in range. **Installs cleanly under the pinned uv with no wheel risk** — genuinely the best-installing platform on this shelf, and the *only* one that self-hosts as a single process with no external database. **Scores well on the carried constraint.** But `phoenix serve` is a **long-running server process**, and this repo has never taken a server dependency of any kind. That is a posture change, not a package addition.

**Error-handling / usage-stats coverage — explicit.**
- **Captures:** full OTel spans for LLM calls, tool calls, agent steps, retriever calls; token counts and latency per span; span status and exception events (so a failed model call, its type and its message are captured); prompt/response payloads; evaluation results attached to spans; datasets and experiment runs.
- **Drops:** dollar cost is not native — it is derived, and requires a price catalog. Drops anything not instrumented: a `pre-commit` hook run leaves no trace unless you hand-write a span for it. **Drops the entire incumbent event class.**

**Verdict: `absent` as an installed organ** (searched `Phoenix`/`arize` repo-wide: the only hits are two prior *research* artifacts naming it in a landscape list — `docs/audits/2026-08-26-...-cost-usage-telemetry.md:63` and `docs/archive/2026-08-17-research-...-distillation-wf-50111a08.md:98`). Not found on disk.
**But the CAPABILITY verdict is `partial`,** because the incumbent set covers the governance half: `telemetry_emit` is the store, `trends.html` is the trend view, packets are the verdict layer. **Precisely what is missing relative to Phoenix: any span-level view of a model call at all.** Which the repo does not currently need.

**Reconciliation.** Prior verdict: `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md:63` lists Phoenix in a one-row landscape table and the recommendation set **does not include it** — the chosen stack is ccusage + LiteLLM Proxy + LiteLLM price catalog + DuckDB + Actions + Markdown, with Langfuse/SigNoz as "later/optional". **Re-assessed at today's scale: the prior verdict stands and strengthens.** In the nine months since, `[#575]` and `[#576]` opened — and both are about *gate* telemetry, which Phoenix does not hold.

**Cheapest experiment (Tier S).** **Gate it behind 3.1's environment-variable experiment.** Only if Claude Code's OTel stream turns out to contain something the repo wants: `uv tool install arize-phoenix`, `phoenix serve`, point `OTEL_EXPORTER_OTLP_ENDPOINT` at it for one session, and see whether the resulting trace answers an operator question. Frozen criterion: *one named question, answered from a span, that no incumbent surface answers.* If you cannot name the question first, ADR-105's named-consumer rule says do not build it.

### Candidate 3.3 — Langfuse

```
what it provides LLM evals, observability, metrics, prompt management, playground, datasets
repo             github.com/langfuse/langfuse — 33.9k stars, 8,923 commits, 294 open issues
license          MIT (enterprise features in ee/ under separate terms) — the best licence on shelf 3
release          PyPI langfuse 4.15.1 (Aug 28 2026); 4.15.0 (Aug 27), 4.14.6 (Aug 27), 4.14.5
                 (Aug 24), 4.14.4 (Aug 11). Python <4.0,>=3.10. Wheel: py3-none-any.
self-host        Docker + PostgreSQL + ClickHouse + Redis + S3-compatible object storage
corporate        acquired by ClickHouse, Jan 2026 (per this repo's own prior audit, line 62)
standards        OpenTelemetry-based ingest
evidence tier    measured (GitHub + PyPI, read 2026-08-29)
```

**Windows/uv — and this is where it loses.** The *SDK* is a pure-python wheel and installs fine. **The SERVER needs Postgres + ClickHouse + Redis + S3.** Per the brief's explicit rule — *"Heavyweight server-dependent stacks score against it"* — **this scores against it harder than anything else in the survey.** Four stateful services to observe a single-operator markdown repo is not a proportionate act, and the repo's own prior audit already said so in its anti-pattern list.

**Error-handling / usage-stats coverage.** Captures OTel-based traces with token and cost capture (its cost model is more built-out than Phoenix's), plus errors/exceptions on spans, prompt-management versions, dataset runs and eval scores. **Drops the same thing everything on this shelf drops: gate events.**

**Verdict: `absent`.** Searched repo-wide: four hits, all in prior *research prose* (`docs/audits/2026-08-26-...-cost-usage-telemetry.md:62,71,105,118`). Never installed. Not found.

**Reconciliation — and this is a DISCHARGED finding under ADR-111, not a candidate.** The prior verdict is not merely "not selected", it is an explicit **anti-pattern**, at `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md:118`:

> *"❌ Building a telemetry system that costs more than the spend it tracks — for a solo dev, avoid self-hosted Langfuse/Datadog ($200–800+/mo infra + eng time); the Markdown-in-repo + DuckDB + Actions approach is near-free."*

**Re-assessed at today's scale: the verdict is unchanged and I would not reopen it.** The ClickHouse acquisition (Jan 2026) makes the project *more* durable, not lighter. Nothing about this repo grew in a direction that changes the cost/benefit. **Recommending Langfuse here would be relitigating a ruling silently, which the brief forbids and ADR-111 names.**

**Cheapest experiment: none. Do not run one.** The prior finding is DISCHARGED with a locator. The cheapest act is to record that this survey re-checked it and it still holds.

### Candidate 3.4 — LangSmith

```
what it provides tracing, evals, datasets, prompt management — the commercial LangChain platform
pricing          free/Developer: 5,000 traces/mo, 14-day retention, 1 seat, 1 workspace
                 Plus: $39/seat/mo, 10k base traces, then $2.50/1k (14-day) or $5/1k (400-day)
                 Enterprise: unpublished; self-hosting is an ENTERPRISE-tier option
scale example    ~$2,514/mo at 1M base traces on Plus, single seat
self-hosted      NO at any reachable tier. SaaS-only in practice.
evidence tier    ASSERTED — every figure above is from SECONDARY comparison sites (morphllm,
                 inference.net, pecollective, coverge — all dated 2026). langchain.com and
                 docs.langchain.com are BOTH BLOCKED by this session's egress proxy, so I could
                 not reach the primary pricing page. FLAGGED FOR RE-VERIFICATION.
```

**Windows/uv:** irrelevant — it is a hosted service. **Per the brief's rule, SaaS-only scores below every self-hosted candidate here, and this is the only pure-SaaS candidate in the survey.**

**Error-handling / usage-stats coverage.** Comparable span-level capture to the others (traces, evals, datasets), with the additional property that **your traces leave your machine**. For a repo whose governance files contain absolute host paths (`ecosystem/provider-registry.yaml:74`, a `C:\Users\...` marketplace path) and whose audits carry request-ids and SHAs, that is a data-egress consideration, not just a cost one.

**Verdict: `absent`.** Searched repo-wide: two hits, both prior research prose (`docs/audits/2026-05-29-harness-engineering-positioning.md:272` — *"LangSmith — capability vs external dependency + the 'no new deps without confirmation'"* — and the 2026-08-26 landscape table). Not found.

**Reconciliation.** The 2026-05-29 harness-positioning audit already framed LangSmith as the worked example of *capability vs external dependency* under the standing "no new deps without confirmation" rule. **Re-assessed: unchanged, and now weaker** — it is the only candidate that is simultaneously SaaS-only, per-trace-metered, and not self-hostable below Enterprise. **Recommend against. No experiment.**

*(Noted, not surveyed: Harbor ships a `langsmith` extra as one of its sandbox/integration options. That is a Harbor detail, not a reason to adopt LangSmith.)*

### Negative results on this shelf — first-class, per the brief

```
Helicone         Apache 2.0, acquired by Mintlify early/March 2026, MAINTENANCE MODE since.
                 This repo's own prior audit already recorded it ("Maintenance mode since Mintlify
                 acquisition (Mar 2026)", cost-usage-telemetry.md:63) — a correct call, aged well.
                 Evidence tier: practiced/reported (secondary, 2026).
Traceloop        acquired by ServiceNow, March 2026, reported $60-80M. OpenLLMetry (the OSS half)
                 IS still maintained with releases through mid-2026 — so this is an acquisition to
                 WATCH, not an abandonment to report. Naming it because "acquired" and "abandoned"
                 get conflated and the difference matters.  Evidence tier: reported (secondary).
Phoenix's ELv2   the licence is not OSI open source. Worth recording because the word "open-source"
                 appears in its own README description.
OpenCode's move  sst/opencode -> anomalyco/opencode. Not abandonment; a rebrand. But a
                 fallback-harness candidate that changed organisational hands is a governance fact.
The pattern      THREE of the observability tools in this repo's own 2026-08-26 landscape table
                 changed corporate hands within ~12 months (Langfuse->ClickHouse Jan 2026,
                 Helicone->Mintlify Mar 2026, Traceloop->ServiceNow Mar 2026). That consolidation
                 rate is itself the strongest argument for the brief's "keep our verdict layer"
                 instinct AND against buying deep into any one collector.
```

---

## CONSOLIDATED VERDICT TABLE

*Rendered as flat `key: value` records inside a fence rather than a pipe table, per CLAUDE.md §4 "Output formatting (render-layer)" — a pipe table copies out of the TUI carrying box-drawing glyphs at ~3× the tokens.*

**Ranked by fit × value. Six candidates carry weight; the rest are recorded to close the question, not to be adopted.**

```
=========================================================================
RANK 1  ·  Shelf 3  ·  OpenTelemetry GenAI semantic conventions
  provides      a vendor-neutral emission target for GenAI telemetry (spans/metrics/events)
  maturity      Development status, NOT stable; split to its own repo at semconv v1.42.0
                (Jun 12 2026); 625 commits; still not Stable ~14 months on
  windows/uv    NO COST — it is a spec, not a package. Best score in the survey.
  hosting       n/a
  verdict       ABSENT — searched gen_ai|opentelemetry|otel|otlp across scripts/ ecosystem/
                tasks/ .claude/ : ONE hit, a false positive ("remotely",
                single_flight.py:61). Not found.
  reconciled    prior verdict at cost-usage-telemetry.md:13 + its anti-pattern line — "adopt
                the convention, isolate the attribute strings". STANDS.
  experiment    CLAUDE_CODE_ENABLE_TELEMETRY=1 + a file exporter, ONE session, zero deps.
                Criterion: does the stream answer a question [#576] names that
                logs/TELEMETRY.db cannot? Highest value per hour in this artifact.
  why rank 1    it is the only candidate whose experiment can DISCHARGE its whole shelf.

=========================================================================
RANK 2  ·  Shelf 1  ·  The portability map itself (no product)
  provides      the answer to "what does a harness swap cost us"
  finding       gate stack PORTABLE (20/20 hooks are `language: system` + uv run);
                packets PORTABLE; worktree rule PORTABLE in mechanism;
                lane contracts SEAM (one enum in gen_lane_contract.py);
                Ch8 Layer-2 CC-COUPLED but lives at L0, off this repo;
                live-session check CC-COUPLED and it is a SAFETY check
  windows/uv    n/a
  verdict       n/a — this is the deliverable, not a candidate
  why rank 2    it retires the anxiety at zero cost. The repo is already ~80% portable and
                nobody had checked.

=========================================================================
RANK 3  ·  Shelf 2  ·  nasde-toolkit  (the resolved unknown)
  provides      a runnable cost+quality benchmark of an AI coding setup, on your own tasks,
                using existing subscription auth; reviewer-agent scoring; token + dollar
                figures per model/provider
  maturity      MIT; Python; 12 stars; 141 commits; 1 open issue; updated Aug 24 2026.
                PERSONAL-PROJECT SCALE — abandonment risk high, fork-not-depend.
  windows/uv    `uv tool install nasde-toolkit --python 3.13` (3.12 supported, 3.14 NOT —
                missing cp314 wheels). Tool-level install: touches neither uv.lock nor the
                ==0.11.19 pin. Pure-python path, no wheel risk.
  hosting       self-hosted CLI — GOOD — but depends on Harbor, hence Docker or a cloud
                sandbox. SCORES AGAINST on that limb.
  verdict       PARTIAL — organ is SDA-1's DESIGN (2026-08-28-technical-sda1-benchmark-
                design-adversarial.md §2 Q0-Q7) + scripts/nopack_sandbox.py + provider-
                registry.yaml. MISSING: any runner that executes the loop and emits a
                cost-and-quality record. Q7's cost meter is designed, unbuilt.
  reconciled    UNLOCATABLE as a prior verdict — nasde appears nowhere in this repo
                (grep: zero hits). Genuinely new. Not "unevaluated": unlocatable.
  experiment    install; run ONE task the operator already knows the answer to, ONE provider
                pair. Criterion frozen ex-ante: emits per-model token+dollar + rubric score
                with ZERO hand-scoring. Fails on Docker refusal or on non-reproducible
                reviewer scores across two identical runs -> delete, record negative.

=========================================================================
RANK 4  ·  Shelf 2  ·  Harbor
  provides      task/trial/verifier abstraction, per-trial sandbox, agent loop, reward files,
                registry, scale-out to thousands of parallel containers
  maturity      Apache-2.0; 4.8k stars; 1,553 commits; 237 open issues; 539 OPEN PRs.
                PyPI 0.22.0 Aug 22 2026, fortnightly-to-monthly minors. Healthy but
                absorbing contributions faster than merging them.
  windows/uv    py3-none-any, requires-python >=3.12 vs our 3.12.10 — NO WHEEL RISK AT ALL,
                the rustworkx bar is not approached. Install as `uv tool install harbor`,
                NEVER as a pyproject dependency.
  hosting       self-hosted via Docker (GOOD-ish) or SaaS sandboxes Daytona/Modal/E2B (BAD).
                Docker Desktop on Windows is a posture change this repo has never taken.
                SCORES AGAINST on both limbs.
  verdict       PARTIAL — organ is scripts/nopack_sandbox.py. MISSING: trial abstraction
                (no repeat factor — C-4's finding), parallel runner, container isolation
                (the module's own two Windows-specific holes: teardown TOCTOU, forgeable
                marker), machine-readable reward artifact, addressable registry.
  reconciled    UNLOCATABLE — "Harbor" returns zero hits repo-wide. Terminal-Bench appears
                only as SCORES in provider research, never as a substrate.
  C-6/C-15      LOCATED: sda1-benchmark-design-adversarial.md:305 (C-6, "(ii) is a real
                build cost") and :372 (C-15, the three things that get cut). HONEST ANSWER:
                Harbor does NOT relieve the C-6 cost — that cost is authoring adversarial
                TEST CONTENT. Harbor removes the PLUMBING sol did not flag.
  experiment    port ONE fan-out item (the role §10 declares safe) to a Harbor task; run
                locally under Docker. Criterion: same verdict as the hand-run, and the two
                nopack_sandbox Windows holes are closed by the container. Do NOT port the
                producer role — §10 says SDA-1 is unsafe there.

=========================================================================
RANK 5  ·  Shelf 1  ·  OpenCode
  provides      a second, provider-agnostic harness: tool loop, sessions, plan/build agents
  maturity      MIT; 202.3k stars; 15,602 commits; 10 releases Aug 10-28 2026 (~1 per 1-2
                days). NEGATIVE SIGNAL: repo moved sst/opencode -> anomalyco/opencode.
  windows/uv    NO uv engagement (Node/TS). Never touches uv.lock or the ==0.11.19 pin.
                A point IN ITS FAVOUR under the carried constraint.
  hosting       fully local, MIT. SCORES ABOVE all SaaS candidates.
  verdict       ABSENT — searched substrate-registry.yaml (all four substrates' verbs +
                aliases), provider-registry.yaml (cli: per provider), gen_lane_contract.py
                (LOCAL_RE/CLOUD_RE), .pre-commit-config.yaml. No non-Claude executor is
                admitted anywhere. Not found.
  reconciled    prior evaluation exists but for a DIFFERENT question — opencode was scored
                as an AGENTS.md READER (2026-08-25-technical-research-agents-md-standard
                .md:49, "AGENTS.md wins") and deliberately excluded from the provider
                roster (JOURNAL.md:1948). Never evaluated as an EXECUTOR. New question.
  experiment    one throwaway worktree, one completed lane contract with the ## Dispatch
                block removed. Measure exactly two bits: (1) does its commit pass all 20
                pre-commit hooks unaided; (2) does block-unanchored-push refuse its push.
                Delete the worktree either way (CLAUDE.md §5 rule 9).

=========================================================================
RANK 6  ·  Shelf 2  ·  SkillsBench / BenchFlow
  provides      87-task skills benchmark + a task package format (task.md + environment/
                Dockerfile + skills/ + oracle/solve.sh + verifier/)
  maturity      Apache-2.0; 1.7k stars; 456 commits; 49 open issues
  windows/uv    `uv tool install benchflow`; the repo itself ships uv.lock. Pure-python path.
  hosting       DEFAULT sandbox is Modal (SaaS) with Docker local fallback. SCORES AGAINST
                on both limbs, same as Harbor.
  correction    IT DOES NOT RUN ON HARBOR. It runs on the BenchFlow SDK
                (benchflow-ai/benchflow). The brief's "Harbor ... plus SkillsBench and kin"
                groups two RIVAL substrates. Adopting one does not get you the other.
  verdict       ABSENT as a corpus (searched tasks/ for eval|bench|skill — hits are about
                evaluating HOOKS, mutmut, and the verify skill's output contract; and
                .claude/skills/ holds exactly two skills with no fixtures). Not found.
  reconciled    PRIOR VERDICT LOCATED and it is decisive:
                docs/audits/2026-08-19-technical-n3-ratification-pack.md:311 §3.4 —
                R3 (promptfoo rule-adherence harness) "accepted in principle, NOT BORN",
                folded into the existing seeded-defect corpus, because "filing a second
                eval corpus alongside it is the duplication ADR-111 outcome (a) exists to
                prevent." Source intake #35, status: DRAFT.
                RE-ASSESSED: the ruling STANDS and SkillsBench strengthens it — BenchFlow
                would be a THIRD corpus. Per ADR-111 this is OWNED by R3, not a CANDIDATE.
  experiment    DO NOT INSTALL. Hand-run the >=10 non-negotiables R3 already enumerates from
                ~/.claude/rules/core-invariants.md against the two live skills. If fewer
                than 10 are decidable by hand, the harness question is premature.

=========================================================================
RANK 7  ·  Shelf 3  ·  Arize Phoenix
  provides      OTel-native tracing + evals + datasets + experiments, self-hosted single proc
  maturity      ELASTIC LICENSE 2.0 (NOT OSI); 11.2k stars; 9,789 commits; 824 open issues;
                PyPI 20.4.0 Aug 26 2026, ~weekly minors. Very active.
  windows/uv    py3-none-any, Python >=3.10,<3.15 — INSTALLS CLEANLY under the pinned uv.
                Best-installing platform on shelf 3.
  hosting       SELF-HOSTED, one process, no external DB required. Best hosting posture on
                shelf 3 by a distance. But `phoenix serve` is a long-running SERVER and this
                repo has never taken a server dependency — a posture change, not a package.
  captures      LLM/tool/agent spans, tokens, latency, span status + exception events,
                payloads, eval results, datasets
  drops         dollar cost (derived, needs a price catalog); EVERYTHING not instrumented —
                including the entire incumbent event class (check_run/hook_run/blocker_fired)
  verdict       ABSENT on disk (two hits repo-wide, both prior research prose).
                CAPABILITY verdict PARTIAL: telemetry_emit + trends.html + packets cover the
                governance half; MISSING is any span-level view of a model call — which the
                repo does not currently need.
  reconciled    cost-usage-telemetry.md:63 lists it; the recommendation set EXCLUDES it.
                STANDS.
  experiment    GATED behind Rank 1's env-var experiment. Only if the Claude Code OTel stream
                contains something wanted. Criterion: ONE named question answered from a
                span that no incumbent surface answers (ADR-105 named-consumer rule).

=========================================================================
RANK 8  ·  Shelf 1  ·  pi (pi.dev / earendil-works/pi)
  provides      minimal harness: unified LLM API, agent loop, TUI, coding CLI
  maturity      MIT; ~99k stars; 5,826 commits; 72 open issues; TypeScript/Node. The
                "~200-token prompt / 37+ models / 20+ providers" figures are BLOG-TIER and
                UNVERIFIED against the repo.
  windows/uv    no uv engagement (Node).
  hosting       local, MIT. Scores above SaaS.
  verdict       ABSENT (same search as OpenCode). Not found.
  reconciled    unlocatable — pi appears nowhere in this repo.
  experiment    identical to OpenCode's, run as the SECOND arm only if the first passes.

=========================================================================
RANK 9  ·  Shelf 3  ·  Langfuse   — RECOMMEND AGAINST
  provides      OTel-based tracing, evals, prompt mgmt, cost capture
  maturity      MIT (ee/ separate); 33.9k stars; 8,923 commits; 294 open issues; PyPI 4.15.1
                Aug 28 2026, near-daily patches. Acquired by ClickHouse Jan 2026.
  windows/uv    SDK is py3-none-any and installs fine. THE SERVER NEEDS Postgres +
                ClickHouse + Redis + S3.
  hosting       self-hostable but HEAVYWEIGHT SERVER-DEPENDENT — the brief's explicit
                score-against, and the hardest one in this survey. Four stateful services
                to observe a single-operator markdown repo is disproportionate.
  verdict       ABSENT (four hits, all prior research prose).
  reconciled    PRIOR FINDING IS DISCHARGED, not merely unselected —
                cost-usage-telemetry.md:118 names it an ANTI-PATTERN by name: "for a solo
                dev, avoid self-hosted Langfuse/Datadog ($200-800+/mo infra + eng time)".
                RE-ASSESSED: unchanged. The ClickHouse acquisition makes it more durable,
                not lighter. Recommending it here would relitigate a ruling silently.
  experiment    NONE. Record that this survey re-checked the finding and it holds.

=========================================================================
RANK 10 ·  Shelf 3  ·  LangSmith   — RECOMMEND AGAINST
  provides      hosted tracing/evals/datasets/prompt mgmt
  maturity      commercial. free 5k traces/mo 14-day 1 seat; Plus $39/seat + $2.50/1k over
                10k; ~$2,514/mo at 1M traces; self-host is ENTERPRISE-only.
                ALL FIGURES SECONDARY — langchain.com AND docs.langchain.com are BOTH
                blocked by this session's proxy. FLAGGED FOR RE-VERIFICATION.
  windows/uv    n/a (hosted)
  hosting       SaaS-ONLY at any reachable tier — the survey's lowest score under the
                brief's rule. Also: traces leave the machine, and this repo's artifacts
                carry absolute host paths and request-ids.
  verdict       ABSENT (two hits, both prior research prose).
  reconciled    2026-05-29-harness-engineering-positioning.md:272 already framed it as the
                worked example of "capability vs external dependency" under the standing
                no-new-deps rule. RE-ASSESSED: unchanged, and weaker than in May.
  experiment    NONE.
=========================================================================
```

---

## MY OWN LIMITS

### The three named unknowns — resolved-to-what, or unknown

**1. `"PPI"` (Shelf 1) — UNKNOWN.**
Searched `"PPI" AI agent harness coding agent acronym 2026` and `"PPI" agent framework open source 2026 harness OR runtime OR protocol acronym meaning`. **No product, framework, protocol or repository named "PPI" exists in the agent-harness space** in anything reachable. Two real adjacent objects, offered as candidates and explicitly **not** as the answer: (a) **`pi`** — pi.dev / `earendil-works/pi`, a real minimal coding-agent harness, MIT, ~99k stars, which sits exactly where the brief placed the question; (b) **Prediction-Powered Inference** — a real statistical method with a live 2026 LLM-evaluation literature (StratPPI, NeurIPS 2024; arXiv 2606.05308, 2026), which is genuinely relevant but to **Shelf 2**, as the published answer to SDA-1's C-2 calibration problem. **To settle it I need one sentence from the operator: where he saw the name, or what it sat next to.**

**2. `"nasde"` / `noesisvision.com` (Shelf 2) — RESOLVED.**
It is **`nasde-toolkit`**, `github.com/noesisvision/nasde-toolkit`: *"CLI for benchmarks & evals of AI coding agents — on tasks you already understand, using your Claude / Codex / Gemini individual subscriptions or API keys."* MIT, Python, 12 stars, 141 commits, 1 open issue, last updated 2026-08-24. Installs `uv tool install nasde-toolkit --python 3.13`. Depends on **Harbor** for sandboxing and optionally **Opik** for the dashboard. The correct domain is **`noesis.vision`** (the product page is `noesis.vision/nasde/`), not `noesisvision.com`. **Limit: `noesis.vision` is blocked by this session's egress proxy**, so every fact above comes from the GitHub org and repo pages, not the product site. **To fully settle it I would need the product page read from an unblocked network.** This is the most on-target find in the survey and it deserves that second look.

**3. `"tracys.com"` (Shelf 3) — UNKNOWN.**
Searched `"tracys.com" website` and `"tracys.com" OR "Tracys" LLM tracing observability tool`. **No LLM-observability product exists at that domain.** The literal domain returned nothing relevant (the near-matches are `playtracys.com`, an Illinois gaming café, and `tracystravelllc.com`). **`tracys.com` itself is blocked by this session's egress proxy**, so I could not check whether it resolves at all — "blocked" is not "nonexistent", and I will not report it as either. Two phonetic candidates, named as candidates only: **Tracy**, a JetBrains OTel-based AI-observability library for **Kotlin**, introduced March 2026 (exports to Jaeger/Zipkin/Grafana, integrates Langfuse and W&B Weave) — real, but Kotlin-only and therefore irrelevant to this repo; and **Traceloop** (`traceloop.com`, OpenLLMetry), acquired by ServiceNow in March 2026. **To settle it I need the operator's source for the name.**

### What else I could not verify

- **No gate ran.** `python3 scripts/audit.py checks` failed on `ModuleNotFoundError: No module named 'click'`. So the authoritative registered-check roster from `ALL_CHECKS` is **unread**, and every "the gate stack is portable" claim rests on reading `.pre-commit-config.yaml` entries directly, not on a green run. I read 20 local hook ids and their entries; I did not execute one.
- **arxiv.org, huggingface.co, emergentmind.com and alphaxiv.org are ALL blocked by this session's egress proxy.** So the SkillsBench abstract reached me via a third-party paper-note that quotes it verbatim, and the SkillAxe figures (+28% relative, 47–67% gap closure) reached me only via a search snippet quoting the abstract. **Both should be re-verified against the arXiv pages** (2602.12670 and 2606.10546) before either number is cited in a ruling. I would not freeze an ex-ante criterion on them as they stand.
- **langchain.com and docs.langchain.com are blocked**, so every LangSmith price is secondary. It does not change the verdict (SaaS-only is a licence fact, not a price fact), but the numbers should not be quoted.
- **`noesis.vision` and `harborframework.com` are blocked**, so nasde's capability claims and Harbor's quickstart/prerequisites come from GitHub and PyPI rather than the projects' own docs. Harbor's Windows story specifically — whether Docker Desktop is the only local path — is **inferred from a docs quote in a search result, not read from the docs**.
- **SkillsBench's own abstract is internally inconsistent** ("86 tasks" then "16 of 84"), and the repo page says 87 in v1.1. I report the inconsistency rather than picking a number.
- **`ecosystem/trends.html` does not exist on this clone** (gitignored by design) and `logs/TELEMETRY.db` does not exist either (`logs/` holds only `TOKEN-LOG.md`). So Incumbent A and Incumbent B were assessed **from their generators and their tests' descriptions**, not from live artifacts. The nine panel names and three ABSENT series come from `gen_trend_dashboard.py`'s own header and the lane packet's recorded console output, both of which are records rather than a run I performed.
- **The "quota-source field" is unlocatable as a field**, and I may simply be searching for the wrong name. I searched `quota`, `quota_source` and `quota-source` repo-wide and inspected the key sets of `provider-registry.yaml` and `substrate-registry.yaml`. **To settle it I need the operator to name the surface he means** — a batch-manifest bucket label, a routing-table row, and the telemetry `context_json` column are all live candidates and none of them is called that.
- **`pi`'s headline properties are unverified.** The ~200-token system prompt, four core tools and 37+ models are blog-tier claims I did not check against the repo, and I have marked them so rather than laundering them into the table.
- **I did not evaluate Opik** (Comet's OSS eval/observability tool, which nasde uses for optional logging), **SigNoz**, **promptfoo's current state**, or **DeepEval**. Each is a defensible shelf-3/shelf-2 candidate; I stopped at the six that carry weight per the brief's ranking rule rather than padding to twenty thin ones. promptfoo in particular already has a live in-repo position (R3, accepted-in-principle-not-born) and would be the *first* thing to re-price if the eval-loop question reopens — I flag that as the most likely omission to matter.

---

**Lane close.** Read-only, as contracted. Zero rows born, zero files written, zero commits, zero pushes. No hook fired and no closure proposal was accepted. Every finding above is either OWNED by a named open row (`[#575]`, `[#576]`, R3), DISCHARGED against a located prior verdict (Langfuse, LangSmith, OTel-conventions posture), or a CANDIDATE the operator may route through ADR-98 intake — **none of which this lane may do.**

**Sources:**
[anomalyco/opencode](https://github.com/anomalyco/opencode) · [opencode releases](https://github.com/sst/opencode/releases) · [earendil-works/pi](https://github.com/earendil-works/pi) · [laude-institute/harbor](https://github.com/laude-institute/harbor) · [harbor on PyPI](https://pypi.org/project/harbor/) · [benchflow-ai/skillsbench](https://github.com/benchflow-ai/skillsbench) · [SkillsBench abstract (paper note)](https://github.com/AkihikoWatanabe/paper_notes/issues/4591) · [SkillsBench arXiv 2602.12670](https://arxiv.org/abs/2602.12670) · [SkillAxe arXiv 2606.10546](https://arxiv.org/abs/2606.10546) · [noesisvision org](https://github.com/noesisvision) · [nasde-toolkit](https://github.com/noesisvision/nasde-toolkit) · [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) · [arize-phoenix on PyPI](https://pypi.org/project/arize-phoenix/) · [langfuse/langfuse](https://github.com/langfuse/langfuse) · [langfuse on PyPI](https://pypi.org/project/langfuse/) · [open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai) · [OTel: moved GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) · [PPI for LLM ranking eval, arXiv 2606.05308](https://arxiv.org/html/2606.05308v1) · [StratPPI, NeurIPS 2024](https://neurips.cc/virtual/2024/poster/96386) · [JetBrains Tracy](https://blog.jetbrains.com/kotlin/2026/03/introducing-tracy-the-ai-observability-library-for-kotlin/) · [traceloop/openllmetry](https://github.com/traceloop/openllmetry) · [LangSmith pricing (secondary)](https://inference.net/content/langsmith-pricing/) · [Langfuse vs LangSmith (secondary)](https://www.morphllm.com/comparisons/langfuse-vs-langsmith) · [Terminal-Bench 2.0 / Harbor registry](https://snorkel.ai/blog/terminal-bench-2-0-raising-the-bar-for-ai-agent-evaluation/)