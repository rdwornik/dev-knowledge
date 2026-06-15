# Probe manifest — execution mode: teeth (v5 §5)

<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and records
> PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN
> `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> **Execution mode** (§13 default): there is **no** architect-orientation probe and **no**
> operator-context beat — `PROBES.md` is handed once and worked straight through. The answers —
> the check count, the HEAD sha, the drifted `#id`, the ahead/behind counts, the dates — are
> deliberately **absent from this whole bundle**. That is what gives the probes teeth. Do not
> infer them; run the command.

## Teeth probes (state fidelity)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P2 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at generation HEAD was `6de8bc2` and `main` was AHEAD 8 / behind 0 of `origin/main`** (`RESIDUAL.md` §1). HEAD/sync move on any commit, push, or fetch; **re-derive, don't trust this line** | `git rev-parse --short HEAD` + `git status -sb` |
| P3 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P4 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P5 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, and what does `pytest --collect-only` collect **right now**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual | `python scripts/validate_doc_claims.py` |
| P6 | Does a v5 handoff bundle carry a **per-bundle `README.md`** — and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | the 2026-06-12 collapse dropped the per-bundle README; a summary may still "remember" the four-file shape — the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-15-dev-knowledge-session` (three files, no README) + `sed -n '/no per-bundle README/,+8p' protocols/HANDOFF_PROCESS.md` |
| P7 | Do **all** probes in this bundle's `docs/handoffs/2026-06-15-dev-knowledge-session/PROBES.md` structurally **bind** to live state (zero FAIL), per the #163 teeth validator? | this bundle's probe set ∩ `scripts/verify_handoff_probes.py` | the binding set is computed at answer-time by the validator; a summary cannot know whether a later edit reworded an anchor or moved a source out from under a probe | `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-15-dev-knowledge-session` |

## Gate procedure (CC)

1. Run P1–P7, each against **live state now** (not generation-time). For each, record **PASS**
   (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored /
   receiver tried to answer from memory or this bundle).
2. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
3. Probes P2/P3/P4/P5 are *expected to move* between generation and check-time — that is the design
   (P2 especially: the operator may have **pushed**, clearing the ahead-8 origin gap). The pass
   criterion is **"answered from the live source,"** never "matches the value the summary
   remembered." P6 pins the post-collapse three-file shape; P7 pins that this bundle's own probes
   bind (the #163 validator the hub's `audit.py health` `handoff_probes` check also runs on the
   latest bundle).
