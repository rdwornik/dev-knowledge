# Probe manifest — teeth-y forced primary-source read (v5 §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and
> records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor →
> WARN `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent →
> reported *skipped* (degraded coverage visible), never counted as pass.
>
> The answers are deliberately **absent from this whole bundle** — that is what gives the
> probes teeth (`RESIDUAL.md` §4). Do not infer them; run the command.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P2 | Quote **byte-identical** the three **bold lead-in labels** (items 1/2/3) of the teeth criteria in HANDOFF_PROCESS v5 §5 "The teeth-y forced primary-source read". | `protocols/HANDOFF_PROCESS_v5.md` §5 | a paraphrase from a summary is not byte-identical; only the live file gives the substrings | read the live §5; each quoted label must be a substring |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of** `origin/main`? | live git | the summary holds the generation-time sha + ahead-count; a new commit or a push moves both | `git rev-parse --short HEAD` + `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy and documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, and what does `pytest --collect-only` collect **right now**? (DRIFT-1.) | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual (the headline names the drift, not the numbers) | `python scripts/validate_doc_claims.py` |

## Gate procedure (CC)

1. For each probe, run the command against **live state now** (not generation-time).
2. Compare to the probe's intent; record **PASS** (live ground truth obtained and
   consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer
   from memory).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder
   (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6 are *expected to move* between generation and check-time — that is
   the design. The pass criterion is **"answered from the live source,"** never "matches
   the value the summary remembered."
