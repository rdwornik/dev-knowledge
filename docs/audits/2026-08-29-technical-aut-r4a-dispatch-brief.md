# AUT-R4-A — foundations: independent harness · eval substrate · agent observability (CLOUD, READ-ONLY)

**Repo:** `.dev-knowledge` (bound to `main`) · **Substrate:** cloud (read-only reconnaissance, no
gate dependency)
**Arc:** AUTONOMY. Sibling lanes already dispatched: **AUT-R1** (autonomous SDLC orchestration),
**AUT-R2** (decision-quality frameworks), **AUT-R3** (repo-as-reinforcement-environment), and your
own sibling **AUT-R4-B** (orchestration · local memory · loop optimization). You will not see their
output; do not speculate about it.
**Dispatched:** 2026-08-29, side-session.
**Deliverable:** ONE artifact. Print it in full as your final message; it returns by harvest.

## WHAT YOU ARE AND ARE NOT DOING

**ZERO ROWS.** You birth no backlog row, no `tasks/` edit, no intake file, no ADR — not even a
draft. You commit nothing and push nothing. If a hook or a closure proposal invites you to commit,
decline and say the lane is read-only by contract. Your entire output is the artifact text.

**Gates:** you need none. A cloud image may carry the wrong `uv`, so invoke `python3` directly and
**declare that you did**. Do not attempt `uv run --locked`; never report a gate result you did not
observe.

**ONLINE RESEARCH IS EXPECTED AND REQUIRED.** These are surveys of a fast-moving field. Use the web.
Cite real, resolvable sources.

## HONESTY RULES — acceptance criteria, not preamble

- **Sources or it didn't happen.** Never invent a citation, URL, product, paper, version number or
  figure. If no real source exists, write **"no source found"** and label the item a **hypothesis**.
  Operator-named products in this brief are **hypotheses until you verify them** — three are flagged
  below by name and each is a live test of this rule.
- **Evidence tier on every claim**, exactly one of: **measured** (a study or reported result) ·
  **practiced** (organisations do it, no measurement) · **asserted** (someone recommends it).
- **Negative results are first-class.** What the industry tried and abandoned outranks a list of
  things that sound good. Abandonware, benchmarks that do not measure what their title says, and
  loudly-launched projects that went quiet are among the most valuable things you can return.
- **Recency:** note roughly when each source is from, and flag what you would want re-verified.
- Prefer primary sources — papers, framework repos, maintainer write-ups, release histories — over
  listicles and over LLM-generated summaries.
- Where you cannot verify, say so in the artifact rather than smoothing it.

## THIS REPO IS UNUSUAL — say plainly how a pattern transfers, or that it doesn't

`.dev-knowledge` is a **governance and methodology hub that never executes** (Layer 2 of a
three-layer ecosystem model): markdown governance files plus hub-local validators, generators and
gates. No script here drives state in a child repo. It is **markdown-first**, **single-operator**
with AI agents as the other participants, and **heavily gated** (pre-commit, commit-msg, pre-push
hooks plus a self-conformance audit). Read `CLAUDE.md`, `AGENTS.md` and `ARCHITECTURE.md` before
scoring anything.

A pattern built for a multi-engineer product codebase with CI runners may transfer here badly or
not at all. **Say which.** An artifact that scores candidates as if this were a normal application
repo is useless.

## VERDICT ENUM — exactly three, per candidate

- **`already-have-it`** — name the organ **and its locator** (`path:line` or a heading).
- **`partial`** — name the organ, its locator, and **precisely what is missing**.
- **`absent`** — and you must **search before declaring absence**. If you looked and could not
  find it, say "searched `<what you searched>`, not found" rather than a bare "absent".

**Reconcile before recommending.** If a candidate was evaluated in this repo before, find the prior
verdict or intake and **re-assess at today's scale** — never relitigate silently. If you cannot
locate a prior verdict, say **"unlocatable"** — do not say "unevaluated".

## ADOPTION FRAMING + THE HARD CONSTRAINT

**ADR-112 two-tier adoption bar:** Tier **L** evaluates; Tier **S** tries and keeps or deletes. For
every candidate, name **the cheapest experiment that would settle adoption here** — concretely, not
"pilot it".

**CARRIED CONSTRAINT, first-class for every candidate:** Windows wheels + installability under the
pinned `uv` (`required-version = "==0.11.19"`). The `rustworkx` precedent is the bar.
**Self-hosted-friendly scores above SaaS-only. Heavyweight server-dependent stacks score against
it** — say so explicitly, per candidate, rather than in a general caveat at the end.

## THE SURVEY — three shelves

### Shelf 1 — INDEPENDENT HARNESS

OpenCode and current open-source agent-harness peers, versus **our CC-as-harness**.

**Also verify the operator's *"PPI"*** — an unresolved name. Find what it refers to in this space,
or mark it **unknown**. Do not invent a referent to satisfy the question.

**Core question:** which of our organs are **harness-portable** versus **CC-coupled**? Score at
least: frozen lane contracts, the PLAYBOOK Ch8 dispatch table, the gate stack (pre-commit /
commit-msg / pre-push / `audit.py`), and worktree lanes. Read them before scoring.

**Why this matters, and state it in the artifact:** today Claude Code is **both the producer and
the harness** — a single point of dependency. This shelf is the **harness-swap resilience test** of
our provider-agnostic doctrine. The deliverable is an honest portability map, not a recommendation
to switch.

### Shelf 2 — EVAL SUBSTRATE

**Harbor** — the Terminal-Bench team's framework: task / trial / verifier abstraction, containers,
registry — plus **SkillsBench** and kin.

Assess **Harbor as the substrate for our SDA-1 admission packs and skill evaluations, instead of
hand-rolling the harness**. `sol`'s **C-6/C-15** named that build cost explicitly; find and read
that if it is locatable in-repo, and say "unlocatable" if it is not.

**Carry this measured finding into the verdicts** (verify it against the primary source and correct
me if the numbers differ): on SkillsBench, **human-authored skills raise pass rates ~16.2 pp while
LLM-authored skills give no measurable gain**, and **SkillAxe-style evaluation-guided refinement**
is the published fix. **The consequence for us is the point of this shelf: a prompt/skill distiller
without an eval loop ships a useless library.** Say whether that consequence holds, and on what
evidence.

**Also verify `noesisvision.com` "nasde"** — unknown to both operator and architect. Resolve it or
mark it **unknown**. A plausible-sounding invented answer here is a failure of this brief.

### Shelf 3 — AGENT OBSERVABILITY

**Arize Phoenix** (OTel-based OSS), **LangSmith**, **plus Langfuse**, and the **OpenTelemetry GenAI
semantic conventions**. Resolve the operator's *"tracys.com"* or mark it **unknown**.

Fit against our **live incumbents** — read them, do not assume: the telemetry store, `trends.html`,
the quota-source field, and lane packets.

**Verdict frame to test, not to rubber-stamp:** *buy the collector and the tracing, keep our verdict
layer* — telemetry → trends → rulings stays ours. Attack that framing if the evidence goes the
other way.

**Assess error-handling and usage-stats coverage explicitly** — per candidate, what it captures and
what it drops. The OTel GenAI conventions matter here because a convention we can emit to is worth
more than a vendor SDK we would have to rip out.

## SHAPE OF THE ARTIFACT

1. **Lead with the harness-portability map** (Shelf 1) — portable vs CC-coupled, per organ, with
   locators. It is what the arc will act on first.
2. Then the three shelves in order, each with its candidates.
3. Then **one consolidated verdict table**: shelf · candidate · what it actually provides ·
   maturity/maintenance signal (last release, commit cadence, open-issue shape) · Windows/`uv`
   installability · self-hosted vs SaaS · verdict (`already-have-it` / `partial` / `absent`) ·
   cheapest experiment.
4. Keep sources inline with their evidence tier and rough date.
5. **Rank by fit × value. Six well-sourced candidates beat twenty thin ones.**
6. **State your own limits at the end:** what you could not verify, what you marked unknown, and
   what you would need in order to settle each.

The three named unknowns — **"PPI"**, **"nasde" / `noesisvision.com`**, **"tracys.com"** — each get
an explicit line in that limits section stating resolved-to-what, or unknown.
