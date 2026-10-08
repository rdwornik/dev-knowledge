# Architect strategic supplement — 2026-10-08-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-08

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

Headline: B2-W1 is closed. The control plane improved (decisions enforced by mechanism, rows closed on merge, a merge gate that flags pre-existing reds and refuses only new ones, seats that cycle themselves, a handoff boot that passes its test), but the line is still slow (merge median 98 min against 15) and not yet autonomous (spine not built, Codespace half-done, laptop memory-starved).
Open threads (with carriers): Codespace sign-in via tag archive/b2-w1-13-codespace-subscription-auth; merge latency via DIGEST-DECIDE-MERGE-LATENCY-2026-10-05 and DIGEST-PERF-LESSONS-2026-10-06; spine via the night leg-3 measure; transport index and boot teaching via W2 lanes; R80–R89 landing via the rulings_carried gate; plus the eight threads in DIGEST-HANDOFF-ADDENDUM-2026-10-06 — full list with carriers below.
Next authorized action: the incoming seat boots on the pin, reads the lessons, retro, perf and addendum digests plus RATIFICATION 10-05 and 10-06 and the B2-W1 close digest, passes the seat exam (isolated grading), teaches back, then freezes B2 W2's first wave with CC — one build batch at a time.
Contingencies: if codex still says no-credits after unsetting CODEX_API_KEY, check the plan allowance or use codex login --device-auth as manual recovery; if laptop memory pressure persists, run heavy lanes alone or in the Codespace; if the merge median does not fall, read the merge clock before adding levers; if the exam fails again, do not dispatch until W2-22 lands boot teaching.
Do-not-repeat: asserting from memory; changing a file's shape without asking CC who reads it (four times, this SUPPLEMENT's labels included); more than 2–3 pastes per turn; deciding alone (R76); bounds in prose instead of code; acceptance that depends on state outside the lane; API keys instead of mirroring the local sign-in; late scope growth without a capacity check; pushing a handoff before cleanup; unclear relay instructions.

### Sprint retrospective — pragmatic

**Delivered and in `main`:**
- **Row close on merge.**
- **Merge gate:** FLAG pre-existing, REFUSE NEW and non-pass.
- **CI poll:** 300 s → under 13 s.
- **Local dispatch** is hub-only (R75, local part).
- **Integrator liveness:** event wake, plus cycle handover — about 20 unattended cycles.
- **Transport lint.**
- **Codespace basics:** secrets via login shell, classifier, heartbeat, runnable parity checks.
- **Branch-context tests.**
- **Handoff hardening:** Plan row, boot version and sha8, one first move, no probe table.
- **Rulings R55–R79 landed,** plus the `rulings_carried` gate.
- **Transport probe** by subset.

**Not delivered:**
- **W1-13 Codespace subscription sign-in.** The auth.json mirror and version pin work. Codex still says "no-credits", likely because of `CODEX_API_KEY` (R88).
- **Three green Codespace runs** (R63, R83). Blocked by a red `main` and by auth.
- **The spine** (R74). The measure r3 is not frozen.
- **The OT-M merge-gate acceptance.** Cases 1 and 3 await rebuild, so the ruleset is not armed.

**Why it was slow (measured):**
- **Merge median 98 min,** broken down as:
  - queue behind the single integrator: 38.5 min;
  - flaky reruns: 23.7 min;
  - Windows CI: 19 min;
  - prep: 11 min;
  - unexplained: about 25 min.
- **Every landing runs full two-OS CI,** bookkeeping included.
- **73 known reds on `main`,** so verdicts become set-diffs.
- **The laptop is memory-starved;** the reaper killed long steps.
- **W1-12 looped 13 times** on an impossible acceptance.
- **The B2-W1 close took the integrator about 8 h.**

**AJ (Architekt Jutra) conclusions in force:**
- The single writer is the spine (R74).
- Observer-side proof and revision-bound verdicts go to W2.
- Per-role newest models (R61, R82).
- Allow-list by absence is rejected (R69).

### Open threads — full list with carriers

| Thread | Carrier | Next |
|---|---|---|
| Codespace sign-in, all providers (R87, R88) | tag `archive/b2-w1-13-codespace-subscription-auth` (407b17e0), W2 lane | Unset `CODEX_API_KEY` for codex; prove a served id |
| Three green Codespace runs (R63, R83) | follow-on W2 lane | Needs a green `main` and proven auth |
| Unlanded dispatcher seat row | tag `archive/b2-w1-dispatcher-seat-row-cycle-22` (4c717ecb) | W2's first landing |
| Merge latency (R85) | the two digests above | W2 first wave — see below |
| Spine (R74) | night leg-3 measure | Freeze the text with CC, then L10 writer → R59-principle lanes → engine → D1 (10-14 if Trial A passes) → Trial B |
| Transport index and boot teaching (R84, R79) | `b2-transport-index` and W2-22 | W2-22 also puts SEAT-LESSONS and the exam on the reading path |
| R80–R89 landing | `rulings_carried` gate | next landing run |
| Night-rule records (N1–N10 applications) | seat receipts, B2-W1 close digest | review |
| SEAT-LESSONS v3 | v2 plus drafts 18–23 plus this do-not-repeat list | merge |
| Ruleset arming (R64) | OT-M rebuild | then the operator arms it |
| B2 W2 draft (23 lanes) | night leg 7 | approve, reorder per R84, R85 and the perf digest, render |
| Eight more threads | `DIGEST-HANDOFF-ADDENDUM-2026-10-06` | THROUGHPUT ADR; cloud-leg ADR (R75); removal engine, retire list and ceremony removals; registry currency; demo-prep's unpushed commits; empty job dirs; seat memory file at its cap; the user-config hook flag |

**W2 merge-latency first wave, in order:**
1. W2-24 merge clock.
2. Docs and ledger fast path: `dorny/paths-filter` plus one "All Clear" aggregate required check. Never workflow-level `paths` on a required check.
3. Close bookkeeping in one landing.
4. Green `main`.
5. W2-25 pre-handback verdict.
6. No reruns of registered flaky tests.
7. W2-13a Windows shards (R86).
8. W2-13b one full run per change.
9. Parallel integration.

### Purpose, destination, intent, findings

**Purpose (proposed fill-in):** Start B2 W2 so the line becomes fast and truthful:
- merge median toward 15 min (R85);
- spine measure frozen and L10 writer built (R74);
- transport index and boot teaching (R84);
- Codespace sign-in by subscription (R87, R88).

One build batch at a time.

**Destination (proposed):** The incoming browser seat writes to the transport only. It works in architect mode for the W2 freeze, then in execution mode (R76, R80).

**Operator intent (standing):**
- Claude Code is the runtime; the harness is model-agnostic, off the laptop, with the process in code.
- One process with a spine; no self-evaluation (R68, R74).
- Autonomy through bypass and self-healing (R69).
- All dispatch in the harness (R75).
- No forgotten decisions; minimal prose (R79).
- Generated facts (R70).
- Newest model per role (R82).
- Tested, teaching handoffs (R73).
- Triage, then one topic per turn, together with CC (R76, R80).
- Emergencies, then cleanup, then test, then a fresh-session cut (R89).

**Findings not in the repo:**
- **How the operator works:** Polish in chat; plan before acting; slow and accurate; plain explanations; exact pastes.
- **The project is universal** — private and company.
- **Cost:**
  - The hub is public, so Actions are free; pay-as-you-go is approved.
  - mutmut runs in CI.
  - Larger runners and the merge queue need an organization account.
- **Laptop:**
  - It is memory-starved.
  - `bash` resolves to the WSL stub, so use Git Bash.
- **Codespace sign-in:**
  - codex: mirror `auth.json`;
  - gemini: retired;
  - agy: keyring, so BLOCKED-AUTH;
  - Copilot: token, accepted.
- **Hand off by about 40 turns, or one working day.** This seat ran more than three days.

**Decisions changed in this window — all in files:**
- R55–R67: RATIFICATION-2026-10-03 v8.
- R68–R79: RATIFICATION-2026-10-04 (v4 text).
- R80–R86: RATIFICATION-2026-10-05.
- R87–R89: RATIFICATION-2026-10-06.
- The R59 ADR loop is stopped; its four principles stand.
- R76 refines ADR-108 §A.
