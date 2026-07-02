# Probe manifest — architect mode: orientation first, then teeth (v5.3 §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted `#id` +
> closing sha, the serialize-group membership, the counts, the dates — are deliberately **absent from
> this whole bundle**. That is what gives the probes teeth. Do not infer them; run the command. The
> "expected at generation" hints below are a **drift reference** so CC can detect movement between
> generation and check-time — the pass criterion is **"answered from the live source,"** never
> "matches the remembered number."
>
> **Generated cold, then FILLED — the fill RE-SCOPED the priority.** The git window is housekeeping-only
> (a stale-disposition prune, `b255a8c`), but the operator then **FILLED `SUPPLEMENT.md`** with a
> CC-verified live finding — **the enforcement-transfer gap (5 hub organs HUB-ONLY, 5/5 ABSENT across all
> 4 consumers)** — that **supersedes** the prior three-goal priority. Its ANSWERS are folded into the
> paste; `RESIDUAL.md` §4 + `HANDOFF_BOOT` are re-scoped to lead with the **enforcement-mesh P0** (three
> goals + fleet #221 demoted to sequenced-after). So the §13(d) operator-context beat in P1's gate
> **NARROWS** to *"anything changed since the supplement was written?"* — it does **not** fire FULL.
>
> **Windows note:** `audit.py checks` (P2) crashes mid-listing on a bare cp1252 PowerShell console
> (a `→` in a check docstring) — run with `PYTHONUTF8=1` or in git-bash. `ship-gate` (P7) can
> false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P1 — Orientation (the architect's **first move**, before any mechanism — v5.3 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (v5.3 §13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` (near line 11) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` (near line 48) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (v5.3 §13d):** the
browser asks the operator for **off-repo** context. This bundle's supplement is **FILLED** (its ANSWERS
are in the paste — the enforcement-mesh P0, the Informant-Organ → mesh-carrier decomposition, the
mesh-model A/B/C fork), so the beat **NARROWS** to *"anything changed since the supplement was
written?"* — **not** a FULL re-ask. (The load-bearing off-repo call is already answered:
**enforcement-mesh gap is P0; the prior three goals + fleet are sequenced-after.**)

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — **expected at generation: 26, last name `doc_code_coverage_drift`** (unchanged this window — no new check landed) | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **this bundle was cut at HEAD `f3c3f51`, tree clean, `main` in sync with `origin/main` — but this handoff's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: only the standing `#77` voided-closure false positive (`77e5d7df9`), no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — **expected: stamp on/after the last touch (both 2026-07-02); the 2026-07-02 stamp is HONEST (#223 genuine re-read; #222 decoupled the count-claims that had been forcing it) — this housekeeping window did not touch ARCHITECTURE** | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH (1030/1030)**, but the live count is the only ground truth and the pass test is "answered from the live source," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline:** at generation `ship-gate` is **GREEN** with **`4` WARN dispositioned** (#77 voided-closure + 3 journal-wrap/transcript no-ff) AND carries **NO `[stale]` line**. The register dropped **6 → 4** this window — the prune (`b255a8c`) tombstoned the 2 stale ai-council cross-repo P5/P7 dispositions (probes now bind clean). The live answer is the only ground truth (a new direct-on-`main` commit would re-RED it); the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement state; the live bundle + spec are the only ground truth — **expected: FIVE files (BOOT + RESIDUAL + PROBES + SUPPLEMENT + PASTE_THIS), NO `README.md`; `SUPPLEMENT.md` present with ANSWERS FILLED (generated cold, then filled by the operator → the ANSWERS region carrying the enforcement-mesh finding is folded into `PASTE_THIS`); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-07-02-dev-knowledge-architect-2/` ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: code-edge = ONLY `#218`; coherence = `#180/#181/#182/#220`; the `audit-py` group includes `#234`** (unchanged this window — no BACKLOG edit) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — **NARROWED** to *"anything changed
   since the supplement was written?"* (this bundle's supplement is FILLED, ANSWERS folded into the paste),
   not a FULL re-ask, before design. Then run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **P7 is
   the headline: expected GREEN with `4` dispositioned WARNs AND NO `[stale]` line** (the prune dropped
   6→4) — but the pass criterion is **"answered from the live source,"** never "matches the verdict the
   summary remembered." **P2** is expected to read **26** (last name `doc_code_coverage_drift`). **P5**
   expects an HONEST 2026-07-02 stamp. **P6** is expected to **MATCH** (1030/1030), the claim in
   `doc-counts.md`. **P8** pins the five-file shape with `SUPPLEMENT.md` **FILLED** (generated cold, then
   filled by the operator + folded into `PASTE_THIS`; no README). **P9** pins the now-durable
   serialize-group graph (#156) with **code-edge = just #218** and **`#234` in the `audit-py` group**.
