# Architect strategic supplement — 2026-09-28-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-28

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.
8. **Fixed slots (Part A minimum — REFUSED if the pasted answer omits one).** Restate the
   above as five short LABELED LINES, each non-empty (`"none"` is a valid non-empty value; a
   blank line after the label is not). This is the outgoing seat's judgement in a shape the
   next session can scan in five lines without reading the freeform answer above it; Part B
   (WAVE5B-N5 B1, the `seat-release` moment) is what eventually moves them into the boot card
   itself and makes the refusal a harness transaction rather than a re-render check
   (`gen_handoff.assert_supplement_fixed_slots`). The five labels, exactly:

   ```
   Headline: <one line>
   Open threads (with carriers): <thread — who/what carries it, or "none">
   Next authorized action: <the next act this window authorized, or "none">
   Contingencies: <what changes the plan if it happens, or "none">
   Do-not-repeat: <a mistake or dead end this window found, or "none">
   ```
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
<!-- the five Fixed-slot labeled lines (Q8) go anywhere in this region, each on its own line -->

date: 2026-09-28
version: v2 — supersedes -v1-superseded: the kept lane branches are removed from origin before the cut (R24); their tips are preserved as named in the cut receipt
from: 2026-09-24-dev-knowledge-architect (Layer-1 browser seat, SEQ 1, outgoing) — author of these answers
to: CC handoff-cut session f8dcc82f — transcribe verbatim below the SUPPLEMENT divider; author nothing
kind: ANSWER — the reply to to-browser/QUESTION-handoff-cut-supplement-2026-09-28.md (bundle 2026-09-28-dev-knowledge-architect)

# ANSWERS — handoff SUPPLEMENT, 2026-09-24 → 28 window

**1. Strategic intent.** Make the harness's own path the only path, and prove by measurement that it helps.

The next session changes the way of working in four ways:
- **Nothing lives in a seat's memory.** Every open item is carried by a named order file or a filed row id. The starting list is the master register `to-browser/DIGEST-OPEN-WORK-MASTER-2026-09-28.md`, refreshed from the record at every batch close.
- **Measure before building more.** An A/B pilot (harness on vs off, k runs, pass^k) and the cheap tool trials come before new mechanisms. The window produced 43 merges but cannot say whether agents work better with the harness.
- **Wire before build, enforced.** The anti-orphan gate (R18 Q1): nothing reaches main without a declared trigger and a recorded firing.
- **The decision path is the system:**
  - the browser proposes;
  - CC decides through `/decide` (research, several models, pre-mortem);
  - the operator ratifies;
  - every session starts through `scripts/dispatch.py launch`, with model and effort taken from data and checked ordered-vs-served.

**2. Tensions weighed.**
- **Build new mechanisms vs wire and measure the existing ones** → landed on stop-and-wire. The seat's rule: no new mechanism until the anti-orphan gate is live. Why: 11 mechanisms were merged and never triggered; library-first/spine/`why` were called by 0 of 25 lanes; the handback organ was bypassed by 35 of 45 sessions.
- **Local full suite vs CI** → CI on Windows and Linux is the merge verdict (R11). The laptop runs only targeted tests, the ship-gate diff and the ratchet. Why: 82-minute local suites were reaped for memory. All 12 N4 merges were judged on CI, at 15–24 local minutes each.
- **Throughput vs a clean main** → the integrator's independent re-run stays the gate. Accept a high refusal rate (16 refusals over 17 lanes in N4) for zero defects reaching main.
- **Opus vs Sonnet for orchestrators** → the integrator stays on Opus (judgment); the dispatcher runs on Sonnet (R22), because its logic is code. The N3 Opus dispatcher cost about 7× its Sonnet estimate.
- **One-file batches vs amendments** → one file per batch. Amendments only for ratified re-dispatches (17b, 6b).
- **Write-time refusal vs git-boundary enforcement** → git boundaries (BUILD-MODE rule 8, to 2026-11-18). Write-time refusal is not portable to Codex. R18 v2 carries the flip condition.
- **Offload vs the laptop** → offload is the direction (R5, R6). Codespace dispatch is in the hub's Python. What may run where is still undecided (open question).
- **Secret hardening vs working now** → make it work, harden after (R13). The rclone token has full-Drive scope; the root is the transport folder. A dedicated account is the later hardening.
- **Keeping FAILED lanes' branches vs a clean origin** → a clean origin (R24). Unmerged tips are preserved off-branch, as the cut receipt names.

**3. Considered and rejected — do not relitigate.**
- **R10** "CI red-set difference" as a workaround: withdrawn. Replaced by the ratified CI/OS ADR.
- **A Maister-style multi-subagent pipeline for ordinary lanes**: measured 6.4× wall-clock and 16.2× cost for the same verdict (report 31). Step graphs only where a process has ≥3 deterministic gates (formal decision D07 still to ratify).
- **A PreToolUse hook that refuses writes**: rejected for now — not portable to Codex, and BUILD-MODE rule 8 applies. Advisory reuse hints only.
- **Git as the transport (option B4)**: breaks the transport-registry contract.
- **Arming required checks (arm-ci) in N4 on a red main baseline**: moved to N5 with a baseline review.
- **Seats opened by hand, or the operator choosing models**: rejected. Every session goes through the launcher.
- **The browser's ledger prose as the tracker of open work**: rejected. Nine loops were lost in ledger rewrites. The master register and the open-loops audit replace it.
- **Treating secret scope as a blocker**: rejected by R13.
- **Kept `worktree-lane-*` branches as the carrier of FAILED work**: rejected by R24. The carrier is the master register plus the preserved tips.

**4. Open questions (unresolved or deliberately deferred).**
- Own-tools v2 (decisions 1–9; anti-orphan gate, organs as the only path).
- The memory-resilience + substrates proposal (includes decision B: what may run locally, in Codespace, in the Anthropic cloud).
- The second CI proposal as a convergence check of the decision process (D04).
- D07 agent architecture · D08 test executor · D09 ADR-123 (harness as a package), ADR-124 (code standard, thesis D5 shape), ADR-125 (prose → data), ADR-126 (substrate routing) · D11 ADR-121 step 2.
- ADR-120's unbuilt spine stages 7, 11, 13–16.
- D12 tool trials — the operator has not answered the four recommendations: trial block yes; LiteLLM in a Codespace with a hash pin; Tach before import-linter; no JetBrains.
- D13 KEEP vs orphans (#1033) · D20 view ceiling (10-15) · D21 O-8 clock · D22 built-ins.
- Handoff part B · R17 full build and its retention/plugin-load questions · arm-ci · the Gemini tier (0/10 reachable) · AJ M06.

**5. Decomposition rationale — the shape of N5, and what not to redo.**

Order:
1. **Truth and safety:** the scope-guard redo (R15 was breached — a lane ran `find /` over the employer folder); the anti-orphan gate once own-tools v2 is ratified; the master register refreshed at batch close.
2. **Measurement:** the A/B pilot (M07) and the cheap tool-trial block, so later work is judged by numbers.
3. **The FAILED redos from their preserved tips** (named in the cut receipt):
   - runtime-data-home with R20;
   - transport-rclone with a conditional-write design;
   - moments-fire;
   - python-standard;
   - teardown-visible.
4. **Handoff part B:** B1 lands before 2026-10-05, when the `/handoff` fates expire.
5. **R17 observability.**
6. **arm-ci** after the baseline review.

Do not redo or re-decide:
- R1–R24;
- the CI/OS ADR and its merged lanes;
- dispatch in the hub (R11(3));
- the handoff ADR (R21);
- R22;
- any lane merged in N1–N4.

The preserved FAILED tips are redo inputs, not designs to restart from zero.

Dated pressures:
- ~45 `harness.yaml` fates `manual_until` 10-04 / 10-05 / 10-15;
- broken-hook expiry 10-08 (#863);
- rclone OAuth token ~10-03;
- the #589 view ceiling 10-15;
- BUILD-MODE rule 8 until 11-18.

**6. Off-repo context — changed intent only.**
- **Trust:** the operator no longer accepts anything that depends on the seat's memory. The seat verifies from the record and reads every finished report before acting on it.
- **Priority:** prove value before building. The operator sees infrastructure, not better agent work, and wants that measured.
- **Tokens and cost are now a stated concern** after about 10 % of a weekly budget went in one night. The seat's working rules: Sonnet producers for decision runs unless the question needs Opus; one run per question.
- **Reader routing:** the harness must route large reading to the right model by itself — the design says Gemini. The operator should not have to name the model.
- **Architekt Jutra:** every new module goes through `/decide` against the harness, with browser consultation before any build. M06 arrived on 2026-09-28.
- **The laptop is the bottleneck:** memory reaps stalled batches for hours. Resilience and offload are priorities.
- **A clean repository at every cut:** no stale remote branches, worktrees or claim markers left behind.

**7. Ratified-in-chat register.**
- **R18–R24** — the operator's rulings of 2026-09-26/28. One line each in `to-browser/RATIFICATION-2026-09-28.md`; full text of R1–R23 in `RATIFICATION-2026-09-25.md` v15. They are transport-only, not yet in the repo. Home: `protocols/STANDING_RULINGS.md` via the next batch's rulings lane. Check which of R1–R17 lane 11 (portability-requirement, §AN) actually wrote, before writing the rest.
- **Seat working rules:**
  - no new mechanism until the anti-orphan gate is live;
  - read every finished report before acting;
  - every session starts through `dispatch.py launch`, never opened by hand;
  - each paste is given once.

  Home: the browser role contract (HANDOFF_BOOT / HANDOFF_PROCESS §7), via a row.
- **Interface behavior — the supplement exchanged as transport files** (QUESTION to the browser, ANSWER to CC) instead of a chat paste. Home: `protocols/OPERATOR-INTERFACE.md`.
- **Interface behavior — a standing "operator's word" to restart reaped jobs for a whole batch**, given once in a paste. Home: the memory-resilience ADR, whose goal is zero such words.
- **Interface behavior — the launcher's ordered-vs-served model check**, which refused a mismatched seat and surfaced the registry conflict. Home: the dispatch launch documentation and ADR-127's neighbours, via a row.

**8. Fixed slots.**

Headline: 43 merges landed (CI on Windows+Linux as the verdict, Codespace dispatch in the hub, /decide, handoff part A), but the harness is still optional inside lanes and its value unmeasured — N5 starts from the master register and measures before it builds.
Open threads (with carriers): every item said to be done — to-browser/DIGEST-OPEN-WORK-MASTER-2026-09-28.md; N4 outcome and 14 ROWS-OWED — to-browser/DIGEST-WAVE5B-N4-2026-09-28.md; pending ratifications (own-tools v2, memory-resilience, CI #2, D07–D13) — the next seat; AJ M06 — to-cc/BATCH-DECISION-AJ-M06-2026-09-28.md; retrospective — to-cc/BATCH-RETRO-WINDOW-2026-09-28.md (launch it if its digest has not landed); FAILED redos — the preserved tips named in to-browser/SESSION-handoff-cut-2026-09-28.md (R24).
Next authorized action: after boot, read the master register, the N4 digest and the retrospective, then launch the AJ M06 decision run through the launcher and plan WAVE5B-N5 from the register (scope-guard redo, anti-orphan gate after own-tools v2, the A/B pilot and tool-trial block first).
Contingencies: Gemini still unreachable → the registry's fallback reader, and the operator migrates the Gemini tier; the rclone token expires ~10-03 → publish the OAuth app and re-mint; the manual_until fates lapse 10-04/05 → wire or retire them before anything new; laptop memory reaps → CI stays the verdict and the memory-resilience proposal is ratified first; a usage-limit pause → seats resume on the operator's word and re-read their receipts.
Do-not-repeat: asking the operator to open sessions by hand or pick models; merging a mechanism without a trigger and a recorded firing; tracking open work in ledger prose; coupling lanes with a Starts-after they do not need (it kept the dispatch port from running for a day); leaving stale remote branches, worktrees or markers at a cut; acting on, or reporting about, a report the seat has not read.
