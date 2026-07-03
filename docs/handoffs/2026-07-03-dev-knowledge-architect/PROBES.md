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
> **Branch note (load-bearing for P3/P6/P9).** This bundle was generated on `docs/2026-07-03-architect-handoff`
> **off `main` (`ff3d744`)**, deliberately NOT off the unmerged `feat/essence-spec-p1`. So the
> generation-time values below are **`main`-side**. If the operator checks out `feat/essence-spec-p1`
> (the P1 arc under review), several probes shift by known deltas: **P6 pytest → 1101** (not 1074),
> **P9/BACKLOG → 23 stories / 101 tasks** (the `#244` epic). The pass criterion is still "answered
> from the live source" — note *which* branch is live before comparing to the hint.
>
> **`SUPPLEMENT.md` is FILLED.** The operator supplied this window's strategic *why* from the outgoing
> architect chat; its ANSWERS are folded into `PASTE_THIS.md` and supersede the residual on
> priority/design (P2/PRUNE resume · essence-spec merge APPROVED · mesh-model consult MOOT ·
> continuous-conformance vision). So the §13(d) operator-context beat in P1's gate **NARROWS** to
> *"anything changed since?"* — not a FULL re-ask. **P8's expected value is FILLED** (see P8).
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
are folded into `PASTE_THIS.md`), so the beat **NARROWS** to *"anything changed since the supplement was
written?"* — **not** a FULL re-ask. The load-bearing off-repo calls are **already answered** in the
folded supplement: essence-spec P1 merge **APPROVED**, resume at **P2 (PRUNE)**; the **mesh-model Fable
consult #2 is MOOT** (do not spin one up).

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — **expected at generation: 28, last name `doc_code_coverage_drift`** (the count moved 26→28 this window: `+enforcement_coverage` `+undeclared_edges`) | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; **this bundle was cut on `docs/2026-07-03-architect-handoff` off `main` `ff3d744`, tree clean, `main` in sync with `origin/main` — but this handoff's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed; and `feat/essence-spec-p1` is a DIFFERENT tip. Re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` (and `git branch --show-current` — which branch is live?) |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: only the standing `#77` voided-closure false positive (`77e5d7df9`), no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — **expected: stamp on/after the last touch (both 2026-07-02); HONEST — this window did not touch ARCHITECTURE on `main`** | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH: `1074/1074` on `main`, or `1101/1101` on `feat/essence-spec-p1`** (the P1 suite adds 27 tests + regen'd doc-counts). The pass test is "answered from the live source on the live branch," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline:** at generation `ship-gate` is **GREEN** with **`10` WARN dispositioned** (#77 voided-closure + 3 journal-wrap/transcript no-ff + **6 `…→handoff-process` undeclared edges under #241**, NEW this window) AND carries **NO `[stale]` line**. The live answer is the only ground truth (a new direct-on-`main` commit would re-RED it); the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement state; the live bundle + spec are the only ground truth — **expected: FIVE files (BOOT + RESIDUAL + PROBES + SUPPLEMENT + PASTE_THIS), NO `README.md`; `SUPPLEMENT.md` present with ANSWERS **FILLED** (the operator filled it from the outgoing chat → the ANSWERS region IS folded into `PASTE_THIS.md`); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-07-03-dev-knowledge-architect/` ∩ `HANDOFF_PROCESS.md` §13 (∩ `grep -A2 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md` — is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: code-edge = ONLY `#218`; coherence = `#180/#181/#182/#220/#241`** (`#241` added this window); the `audit-py` group includes `#234/#240/#242/#243`. On `main`: 22 stories / 100 tasks; on `feat/essence-spec-p1`: 23 / 101 (the `#244` epic) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — it **NARROWS** (this bundle's
   supplement is FILLED, ANSWERS folded into the paste) to *"anything changed since the supplement was
   written?"* — not a FULL re-ask (the essence-spec merge + mesh-model calls are already answered). Then
   run P2–P9, each against **live state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **First
   check which branch is live (P3)** — `main` vs `feat/essence-spec-p1` shifts P6 (1074↔1101) and P9
   (22/100 ↔ 23/101). **P7 is the headline: expected GREEN with `10` dispositioned WARNs AND NO
   `[stale]` line** — but the pass criterion is **"answered from the live source,"** never "matches the
   verdict the summary remembered." **P2** is expected to read **28** (last name `doc_code_coverage_drift`).
   **P5** expects an HONEST 2026-07-02 stamp. **P8** pins the five-file shape with `SUPPLEMENT.md`
   **FILLED** (ANSWERS folded into `PASTE_THIS`; no README). **P9** pins the now-durable serialize-group graph
   (#156) with **code-edge = just #218** and **#241 newly in coherence**.
