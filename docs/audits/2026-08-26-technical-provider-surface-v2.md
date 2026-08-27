# TO THE ARCHITECT — state of the world, 2026-08-26 evening
**From: operator + outgoing browser seat. Read before your next planning act.**
While your batch ran, a parallel front closed. This is what is now true, what it changes for you,
and where I think your plan is wrong.

---

## 1 · The provider surface is no longer a question mark — it is measured

Eight CLIs on the operator's machine, each proven with the SAME task
(`Reply with exactly: OK <your model name>`), each with its headless flag established from its own
`--help`, all on 2026-08-26:

| Surface | Verdict | Headless | Note that matters |
|---|---|---|---|
| Claude Code | working, **Max subscription** | `-p` | billing leak found and guarded — see §3 |
| Codex | working | `exec` | — |
| **`agy`** (Antigravity 1.1.21) | **working**, Google OAuth | `-p`/`--print` | **serves 14 models incl. `claude-sonnet-4-6` and `claude-opus-4-6-thinking`** |
| `grok` | working, **credential proven by server round-trip** | `-p`/`--single`, `--prompt-file` | **PAY-PER-CALL** — one small test cost **$0.037**. Not a subscription. |
| `copilot` | working | `-p` + `-s`, needs `--allow-all-tools` | — |
| `deepcode` (DeepSeek) | working | `-x` with `-p`, stdin | third-party package, ships ~2 minor versions/day |
| `dsk` (DeepSeek via Anthropic-compatible endpoint) | working | `-p` passthrough | wrapper around `claude`, call-scoped |
| `cursor-agent` | **answers, but CANNOT carry a lane** | `-p`/`--print`, needs `--trust` | see below |
| `glm`, `kimi` | built, wired, **accounts inactive** | `-p` passthrough | operator purchases, not defects |

**Gemini CLI is RETIRED by operator ruling** — it returns `UNSUPPORTED_CLIENT`, not a tier refusal.
`agy` is the channel to Google models and it carries the operator's own subscription.

**Cursor's limitation is sharper than "not configured":** the Free plan refuses **every named
model** (`Named models unavailable — Free plans can only use Auto`). "Auto" is a *selection mode*,
not a model, and Cursor does not disclose what served a call. **An undisclosed model is an
unreproducible result**, so `cursor-agent` is plan-gated out of lane use until the plan is
upgraded. Also measured: `--model` is a **persisted setting, not a per-invocation flag** — after a
refused pin, later calls kept using the stored id while the error pointed elsewhere.

### The finding that is YOURS: intake #42, measured live
Planted probe files (`AGENTS-4711` / `CLAUDE-8822`) settled instruction-file precedence by
execution rather than by documentation:
- **`agy` and `deepcode` pick AGENTS.md**
- **`grok` and `copilot` pick CLAUDE.md**
Combined with the landed R-L research (Codex and Cursor strict AGENTS.md-only), the #42 criterion
is no longer "met on documentation" — it is **met on measurement, with a split field**. Fold this
into the ADR's evidence section; it is stronger than anything in the file today.

---

## 2 · Dispatch is consolidated. Codespaces still waits on YOU.

One verb per substrate, all deployed and tested: **`Dispatch-Local` · `Dispatch-Cloud` ·
`Dispatch-Codespace`** (old names kept as aliases). Bypass permissions enforced on all three with
mutation-proven tests. `Ok` and `RemoteExitCode` separated so transport-success can no longer read
as work-success. Terminal billing errors now fail fast: **187s → 15s, 197s → 14s**, measured live.

**The Codespaces transport is PROVEN end-to-end** — machine created (5.4s), contract and runner
shipped in, executed **inside the container**, receipt retrieved; ~95s total, ~0.85 of 120 free
core-hours across five runs. The receipt reads
`{"error":"claude is not installed in this devcontainer"}`.

**So the only thing between this fleet and a working third substrate is two acts in YOUR repo:**
- **ACT 1** — install Claude Code in the devcontainer image (one feature or `RUN` line; quote the
  documented install route in the commit).
- **ACT 2** — reference the `CLAUDE_CODE_OAUTH_TOKEN` Codespaces secret, **already set
  server-side** by the operator, scoped to this repo. Do **not** resurrect the `containerEnv` block
  removed under `[#554]` — that removal was correct. Land the exposure/rotation note as a register
  section in the same commit.
- **DONE-WHEN: smoke run 5 returns `Ok=True` AND `RemoteExitCode=0`** with a check-count receipt
  from inside the container. Wall-times land as D1 evidence. Only then does the substrate table's
  Q4 default become real.

**New input for that work:** `agy` serves Anthropic models through the operator's Google
subscription. That does not change ACT 1/ACT 2, but it does mean the fleet has a second,
already-authenticated route to Opus-class capacity — relevant when the router ADR weighs cost.

---

## 3 · Two defects found on the operator's machine that change how you think about checks

**The billing leak.** The shell profile exported the whole secrets file, so Claude Code silently
preferred a credential over the operator's Max subscription and **billed per token for an unknown
number of hours**. It was caught **by eye, on a banner**. The guard now launches a real child shell
per PowerShell edition — reading its own environment would have reported a hand-cleaned shell as
clean.

**A foreign installer changed a registry value's TYPE.** Cursor's installer converted the user PATH
from `REG_EXPAND_SZ` to `REG_SZ`, baking `%LOCALAPPDATA%\...` into a literal. Every variable-based
entry silently stopped resolving. **A check that reads only a value's text cannot see this** — the
new guard asserts the type.

Both are the same shape as everything else this window: **a system reports health because nothing
asks the question that would reveal illness.**

---

## 4 · Telemetry — and why it is no longer optional

Research landed (artifact L5 in the manifest). Library-first shape: `ccusage` (local per-tool
tokens/cost, including subscription usage) + provider billing APIs (Anthropic Cost, OpenAI Costs,
GitHub enhanced-billing for Codespaces core-hours and Actions) + a price catalog to value
subscription usage + DuckDB + a GitHub Actions weekly cron rendering Markdown into a repo. **Only
the join-and-render script is custom.**

**Why it is urgent rather than nice:** the fleet now has **at least four distinct billing
regimes running simultaneously** — Anthropic subscription, xAI pay-per-call (**$0.037 for one
trivial test**), DeepSeek pay-per-token, GitHub core-hours — plus two providers that will start
billing the moment their accounts are topped up. **Nobody can currently answer "what did I spend
this week, on what".** The billing leak is proof: it ran for hours and was caught by accident.

**Known gap to declare rather than engineer around:** Anthropic-hosted cloud sessions expose no
usage export.

**I recommend this as the FIRST consumer arc (O4 parity)** — the beneficiary is the operator, not
the hub, and it produces the cost/latency evidence D1 needs. Parity has now slipped three windows.

---

## 5 · Artifacts you must land — they exist ONLY in the operator's Downloads

Eight files, all ADR-101 technical class, byte-identical, `research` naming for the research set:

| # | Source | Target `docs/audits/` |
|---|---|---|
| L1 | `DISPATCH-SURFACE-MEASURED.md` (2083 lines) | `2026-08-25-technical-dispatch-surface-measured.md` |
| L2 | `DISPATCH-CONSOLIDATION-PLAN.md` | `2026-08-25-technical-dispatch-consolidation-plan.md` |
| L3 | `DISPATCH-CODESPACE-REPORT.md` | `2026-08-25-technical-dispatch-codespace-build.md` |
| L4 | `compass_artifact_wf-02c9f141-….md` | `2026-08-26-technical-research-chinese-coding-models.md` |
| L5 | `compass_artifact_wf-4a3dfa9f-….md` | `2026-08-26-technical-research-cost-usage-telemetry.md` |
| L6 | operator-playbook research (Claude Code invocation, orchestration, Codespaces via `gh`) | `2026-08-25-technical-research-operator-dispatch-playbook.md` |
| **L7** | `compass_artifact_wf-a264d29b-….md` | `2026-08-26-technical-research-backlog-management.md` |
| L8 | `ALL-PROVIDERS-READY-REPORT.md` + `PROVIDER-SURFACE-REPAIR-REPORT.md` | **REDACTED or derived summary only** — they carry the operator's org id, email and a map of where credentials live |

---

## 6 · THE CHALLENGE — where I think your plan is wrong

**L7 is the one that should stop you.** It is a research artifact commissioned **months ago** that
prescribed, verbatim: *the aggregate view is NEVER the source of truth* · *prune to ~40–60 active
items* · *per-item files merge, a regenerated aggregate does not* · and that **a `generated_sha256`
on a regenerated aggregate guarantees merge collisions git cannot auto-resolve**. None of it was
implemented.

Two consequences you are living with right now:
1. **`BACKLOG.md` measures 283 KB / 464 lines / ~70,000 tokens** — average **608 characters per
   line**. Every agent burns a large share of its context before doing anything. The defect is
   **not row count** (208 rows in 464 lines is healthy) — the generator projects each row's **full
   body** into the view. Fix: emit a table (`id · theme · status · title · one-line · pointer`),
   bodies stay in the rows. **~20 KB, ~14× smaller, zero information loss.**
2. **Your three-lane integrations take hours** because every lane regenerates the same aggregate
   surfaces, so every merge conflicts on them. That is the predicted collision, manifesting.
   Parallelism is being paid for and then spent on serial conflict resolution.

**And the mechanism behind it, which is the real finding of this window:** every step of this
process **creates** an artifact; **no step destroys one**. Intakes create documents, ADRs create
documents, rulings create sections, audits create artifacts. Closure closes *rows*, not
*documents*. There is no reaper. Worse: **landing is measured, consumption is not.** An artifact
can land and never be read again and **nothing goes red**. That asymmetry is why four months of
correct analysis went unexecuted while the corpus grew — and it is the same
green-without-predicate shape as every defect above.

**The operator's proposal, which I endorse: make the next window SUBTRACTION-ONLY.** No new
intakes, no new ADRs, no new research — **including the five intakes from this window**. Its only
acts: implement L7 (rows as source, view as a ranked 40–60 slice, fix or remove
`generated_sha256`), archive (`docs/intake/` decided, `docs/decisions/` superseded, `docs/audits/`
pre-wave), and **build the reaper** — an artifact cited by no row, ADR or ruling within one window
gets flagged for archival. Net must be strongly negative.

**Before you agree or disagree, run the read-only diagnostic** in
`WINDOW-RECORD-AND-DIAGNOSTIC.md` PART X. It writes one report to Downloads and touches no repo
file. Its section 3 is the measurement this fleet has never made: **for every audit and every ADR,
is it cited by anything?** Two lists — CITED, and CITED BY NOTHING. Until that number exists,
every judgement about accumulation here is an impression.

---

## 7 · What was achieved, so the record is honest

Governance: 37 candidate rows adjudicated and landed as `STANDING_RULINGS` section U · 29 closures
(212→183) · five verification lanes merged · two researches landed.
Machinery: dispatch collapsed from **four rival commands to one verb per substrate** · the
Codespaces transport **built from nothing and proven end-to-end** · bypass permissions mechanised ·
a credential leak found, measured and guarded · terminal billing errors 187s→15s · a repo-root
hygiene guard · a registry-type guard.
Knowledge: eight provider surfaces measured, six working · instruction-file precedence settled by
execution · **`LESSONS.md` started being written to again** after months of neglect.

**Nine architect errors of one class were recorded this window** (asserted-instead-of-measured,
every one caught by an executor with a gate, never by the browser). That is the strongest argument
for the direction the operator keeps pushing: **the browser is the least reliable component, so
the fix is a smaller fact surface at the architect and more mechanisms in the repo** — a contract
names the command, never the fact.
