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
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted
> `#id`, the serialize-group membership, the dates — are deliberately **absent from this whole
> bundle**. That is what gives the probes teeth. Do not infer them; run the command.

## P1 — Orientation (the architect's **first move**, before any mechanism — v5 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a
copy of VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line
read**: the line enters the session **only** by CC reading the **live** primary source, and the
quote must match as a **substring** (never a paraphrase). The browser has no files → it replies
**"run `<command>`"**; CC reads live and substring-checks.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` (line 11) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` (line 47) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read
live by CC, substring-matched. **Then, before design, the operator-context beat fires (v5 §13d):**
the browser asks the operator one targeted question for **off-repo** context (intent / priorities /
findings not in the repo / changed decisions). **v5.1 narrowing:** if the operator relayed a
strategic **supplement** for this session, its Q6 already captured the off-repo context — narrow the
beat to *"anything changed since the supplement was written?"* (§13(d), "(d) refined, not
duplicated"). Exercising this beat **and** the supplement interview in a real architect session is the
only-remaining clause of **#159** — and this is the first handoff to reach the v5.1 supplement step
(see `RESIDUAL.md` §2 "The supplement-interview finding").

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `0752efa`, the tree was clean, and `main` was `ahead 9` of `origin/main` (unpushed) — plus this handoff's own commits since** — but HEAD/sync move on any commit, push, or fetch; **re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual — **and at generation this probe is EXPECTED TO MISMATCH** (the §1 headline drift: doc=511, live moved past it), so the live answer is the only ground truth | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** catch this; use the standalone |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 handoff bundle** carry, does it include a **per-bundle `README.md`**, and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + optional architect `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-16-dev-knowledge-architect/` (no `README.md`; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, and which `#id`s are in the **handoff** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, narrowed to
   "changed since the supplement?" if a supplement was relayed — before design. Then run P2–P9, each
   against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P6 is expected to MISMATCH at generation** (the headline drift) — the pass criterion is
   **"answered from the live source,"** never "matches the value the summary remembered." P8 pins the
   post-collapse four-file shape (+ optional architect `SUPPLEMENT.md`, no README); P9 pins the
   now-durable serialize-group graph (#156).
