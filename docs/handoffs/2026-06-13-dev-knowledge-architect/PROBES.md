# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and records
> PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN
> `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count, the HEAD sha, the drifted `#id`, the
> ahead/behind counts, the dates — are deliberately **absent from this whole bundle**. That is
> what gives the probes teeth. Do not infer them; run the command.

## P1 — Orientation (the architect's **first move**, before any mechanism — v5 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a
copy of VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line
read**: the line enters the session **only** by CC reading the **live** primary source, and the
quote must match as a **substring** (never a paraphrase). The browser has no files → it replies
**"run `<command>`"**; CC reads live and substring-checks.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read
live by CC, substring-matched. **Then, before design, the operator-context beat fires (v5 §13d):**
the browser asks the operator one targeted question for **off-repo** context (intent / priorities
/ findings not in the repo / changed decisions) — the channel the repo-derived residual cannot
carry. Net: *readable-first is a verified property of the handoff, with zero content copied*,
**then** the off-repo steering is injected.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `8d9d35d` and `main` was AHEAD 3 / BEHIND 1 of `origin/main` — DIVERGED, not in sync** (`RESIDUAL.md` §1). HEAD/sync move on any commit, push, or fetch; **re-derive, don't trust this line** | `git rev-parse --short HEAD` + `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, and what does `pytest --collect-only` collect **right now**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual | `python scripts/validate_doc_claims.py` |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now, and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | this WARN names a nightly automation-writer direct commit (`RESIDUAL.md` §1 / Q9); the named sha + date are high-entropy and absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose sha |
| P8 | Does a v5 handoff bundle carry a **per-bundle `README.md`** — and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | the 2026-06-12 collapse dropped the per-bundle README; a summary may still "remember" the four-file shape — the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-13-dev-knowledge-architect/` (three files, no README) + `sed -n '/no per-bundle README/,+8p' protocols/HANDOFF_PROCESS.md` |
| P9 | What does the `behind 1` commit on `origin/main` actually contain (its `#id`, its high/med/low counts), and is it **integrated into local `main` yet**? | live git ∩ `origin/main` | the divergence is computed at answer-time; the digest's contents + integration state are high-entropy and **deliberately absent** from this bundle (`RESIDUAL.md` §1) — a summary can't know whether it's been merged since generation | `git log --oneline main..origin/main` + `git show --stat <sha>` (re-derive; the bundle names no sha) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask — before
   design. Then run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design (P9 especially: the operator may have reconciled the divergence per §1). The pass
   criterion is **"answered from the live source,"** never "matches the value the summary
   remembered." P8 pins the post-collapse three-file shape; P9 pins the live `origin/main`
   divergence the §1 headline names.
