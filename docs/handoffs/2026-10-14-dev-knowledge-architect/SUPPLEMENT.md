# Architect strategic supplement — 2026-10-14-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-14

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

## 1. Strategic intent

Make the harness pay for itself in outcomes the operator uses. The way of working is now fixed by R99 and R101:

- **The orchestrator.** The Claude Code main thread is the one orchestrator. It runs on Sonnet; Opus does short architect reviews only.
- **Producers and reviewers.** Codex and the other vendors produce bounded code. The reviewer is never the producer's vendor.
- **Cost.** Cost is measured per lane.
- **The browser** reads only generated surfaces, at most about 20 KB per review.

**The next session's goal** is ONE batch of user-visible deliverables, not more harness-about-harness:
- Codespace off the laptop;
- the transport index applied, so the browser stops reading big files;
- commit attribution;
- D1, so Claude Code launches every vendor.

## 2. Tensions weighed

**(a) Cost against quality.**
- My R97 moved all production onto Claude Opus/high. With 18 of 19 lanes Opus/high and a 15-hour Opus main thread, it cost about 25% of the weekly limit in one night.
- Landed: R101 — tier by class, Codex produces, a Sonnet orchestrator, two review rounds at most, no wait over 30 minutes.

**(b) Unattended autonomy against safety.**
- The night run was pre-authorized with stop rules.
- Landed: the stop rules held. Two refused lands each got one repair lane and re-landed; D1, D5 and D7 were held rather than forced. The 30-minute rule cut the run short, and that was accepted as the price.

**(c) Gate strictness against flow.**
- Landed: never bypass a gate.
- D1's new gate refuses the integrator's own merges, so D1 was held, not landed.
- Wedged seats were cleared by stopping the job (`claude stop`), not by forging registry events.

**(d) Hygiene against preservation.**
- The protocol never deletes an unmerged branch.
- Landed: every unmerged branch was given an `archive/2026-10-13/*` tag, and then deleted on the operator's GO. Origin went from 20 to 6 branches, local from 23 to 6.

## 3. Considered and rejected (do not relitigate)

| Rejected | Why |
|---|---|
| Copilot as the primary producer (R96 D14) | quality: inline `python -c` hooks, a duplicated launcher, CI run per lane. Replaced by R97 and then R99 |
| Forging a SessionEnd to clear seats | `seat_registry.py:66` calls it forgery |
| Back-dating the cut with `--date` | R102.3 |
| Re-pointing an archive tag by force-push | it drops commits |
| Landing D2 after five REQUEST-CHANGES rounds | it is FAILED |
| Re-dating `[#912]` a third time without a new ruling | R98 |
| Deleting unmerged branches without a tag | — |
| Retrying the session that died in the power loss | two orchestrators would collide |
| Running the cut while a batch is open or a worktree is linked | the gates in `gen_handoff` |

## 4. Open questions (unresolved or deferred)

1. **D1.** How does `land` tell an integrator-made merge from a hand-started lane branch without refusing the integrator? (Codex: 3 HIGH.)
2. **D5.** The citation check reads "replaces R96 D14" as superseding all of R96. Partial supersession needs a grammar.
3. **R101a, tier enforcement.** Does it live in `lane_boot` against the distiller, and what is the override path?
4. **SessionStart.** It now has one injection, but p90 is 14.2 s against 2 s ([#962]).
5. **The midnight defect.** A cut straddling midnight is refused, because the window date is read at cut time.
6. **D1's usage fixture** writes real rows into the live seat registry under the parent's pid.
7. **No routes.** `provider_router` has no Grok or Gemini route (MISSING). Add them, or drop them from R101h?
8. **The GitHub ruleset for main** exists, but enforcement is disabled. That is the operator's setting.
9. **Hygiene's "superseded branch" check:** content that landed by another route, detected with `git cherry` and a diff against main.

## 5. Decomposition rationale; what NOT to redo

**The shape, which worked:**
- the manifest lands on main first (`lane_boot` refuses without it);
- waves, with one land and one CI run each;
- one repair lane per refusal;
- hygiene to zero;
- the close packet;
- then the cut.

**Do NOT redo or reopen:**
- BW is CLOSED at `2512b210`.
- Already landed: A1, B1–B4, B6, the F1 wave (hook-launcher, B5, known-reds-expiry, b2w3-carry, main-red), C1–C6, D3, D4, D6 and D8.
- Reuse what exists rather than rebuilding it: the hook launcher, the lane-report schema, `/map`, the reuse gate and the transport index code.
- The R98 re-date is done, and branch cleanup is done. The 6 remaining branches are kept on purpose.

**Next:**
- D1, D5 and D7 start from their kept branches.
- D7 needs a manifest-amendment row on main citing R100 before `/lane-boot` will start it.

## 6. Off-repo context — changed intent

- **Value.** The operator judged the spend too high for the visible value, so the priority moved to user-visible outcomes.
- **Orchestration.** Claude Code must launch Copilot, Codex, Grok and Gemini itself; the operator never starts a vendor by hand (R99).
- **The browser** must read little.
- **The operator does not want sessions left hanging, or long waits.**
- **Codespace.** The operator's laptop `codex login` (2026-10-13) cleared the "laptop codex cache age" blocker. The agy sign-in inside the Codespace is still owed.

## 7. Ratified-in-chat register (not yet in the repo)

**Rulings and terms:**

| Item | Where it is now | Durable home |
|---|---|---|
| R100, R101 (a)–(i), R102 (cut GO; seat stop; no back-dating) | `RATIFICATION-2026-10-13` v2 and `-10-14` (transport) | the next rulings-landing lane |
| R98 | same | same; R93–R99 are already in `STANDING_RULINGS` §AT |
| "superseded branch": an unmerged branch whose content reached main by another route | — | the BACKLOG, as a hygiene check |
| "wedged seat": a registry row with only a SessionStart under a live pid | — | the LESSONS entry for the D1 fixture defect |

**Interface behaviours relied on, not yet in `protocols/OPERATOR-INTERFACE.md`:**
1. **The agent-view list as a status source.** The operator pastes the session list ("Claude SDK") as the status source.
2. **Needs-input pickers.** A session's needs-input picker is answered by a copy-ready one-line block, addressed to that same session.
3. **Destructive and process acts.** The operator runs no shell commands himself. Such acts (branch deletion, `claude stop`) are delegated to CC; the operator's paste is the GO, with safety checks written into it.
4. **The architect on the transport.** The architect renames and writes transport files on Drive itself, without a relay.

## 8. Fixed slots

Headline: BW closed at 2512b210 (21 lanes landed across B2-W4 and BW; hygiene to 1 worktree / 6 branches); the cost of 25% of the weekly limit in one night led to R101; the next batch must be user-visible.
Open threads (with carriers): D1 lane-controller, D5 boot v2 and D7 attribution — their kept branches, in the next batch; Codespace — branch worktree-b2w2-codespace-finish plus the operator's agy sign-in; transport index apply — janitor --apply in the next batch; R100–R102 landing — the next rulings-landing lane.
Next authorized action: the operator merges this handoff bundle; the next seat boots from PASTE_THIS.md (the ROLE PIN is the only boot check; no /handoff-verify, R30); then one user-visible batch under R101.
Contingencies: if D1's gate still refuses integrator merges after its fix, land D1 without the refusal leg and file it; if no Grok or Gemini route exists, the reviewer chain is Codex then Copilot with a non-Anthropic model; a new weekly-quota squeeze means Codex produces and Sonnet orchestrates only.
Do-not-repeat: an order that leaves the model tier "to the distiller" without a check (18 of 19 lanes went Opus/high); resume blocks written only when context runs high (the crash found one 3 h stale); claiming a branch is merged without git ancestry proof.
