# Architect strategic supplement — 2026-09-10-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-10

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

## 1 · Strategic intent — what the next session should achieve at the way-of-working level

**Subtract and connect. Prove the harness on a consumer, not on itself.**

This window MEASURED. It did not connect and it did not subtract. The census (216 processes,
160 triggered, 32 orphan), the armed FPG-1 spine, the Windows baseline, the 16-stage loop map,
the chapter map — every one of them is an instrument, and instruments were the right thing to
build because nothing could be deleted honestly without them. But the operator's own verdict
stands: *"Ty tylko dodajesz i dodajesz."* Thirteen decision files, eight merged lanes, twenty
new rows, and **zero bytes removed from the corpus and zero bytes delivered to a consumer repo.**

So the next window's way-of-working rule, and it should be enforced at dispatcher step 0 rather
than remembered:

> **Every lane either DELETES something or CONNECTS two organs that already exist. No lane adds
> a new organ. A contract whose Done-when contains no number that goes DOWN, and no edge that
> joins two existing things, is refused.**

And the window's own success metric is not a repo metric. It is **operator hours to land one
feature in corp-monorepo** — today infinite, because Stage 10 of the delivery loop has never
fired. A window that improves hub hygiene and leaves that number infinite has failed on its own
terms, however clean its close packet.

The methodological target underneath: make **"declared enforcement without enforcement"**
extinct by mechanism. Nine-plus instances were witnessed in two days — P11 specified with no
code · `asserted_by` naming a non-reading organ · `test_logs_retention` asserting `is not None` ·
the generator↔verb seam whose own docstring claimed it could not drift · two resolver copies ·
`[#563]`'s test grepping a name to prove a relationship · a drift probe matching the literal
`--report` · `.get(key, default)` over a heterogeneous node list · a ruling that never travelled
back to the question that asked it. These are not nine bugs. They are one bug with nine faces:
**a claim about a relationship that nothing verifies.** The spine exists now to check exactly
that class, and the next window's highest-leverage act is to point it at itself.

## 2 · Tensions weighed, where this seat landed, and why

**(a) Boot forensics vs planning.** The window opened on a failed gate (`-1` and `-2` both
failed P11) and this seat gave five turns to forensics before planning. **Landed: ONBOARDING
BLOCKED blocks rulings and dispatch — it does not block planning.** Recorded as a defect against
this seat, not against the gate. The incoming seat should plan from turn two even if the gate is
red.

**(b) State location — repo files vs GitHub Issues.** Weighted matrix, five options, ten
criteria (`DECLARE-CONDUCTOR-DECISION-2026-09-09`). **Landed: E — state stays in `tasks/`,
GitHub Actions becomes the runner, required checks become the gates.** Rationale: Issues would
have scored well on deletion but broke "decisions are files" and added lock-in; E takes the
runner without moving the state. **Caveat that arrived after the decision: the account is on
GitHub Free and rulesets return 403, so E's GATE leg is unavailable without Pro (~$4/mo). E's
runner leg is unaffected.** The operator's word is owed.

**(c) Dispatch — move to the hub, or retire.** **Landed: retire, do not move.** Moving it into
the hub breaks ADR-28 (the hub is passive storage and governance, not an orchestrator). The
error being corrected is older and subtler: the hub's process needed a runner and the hub had
forbidden itself from having one, so the runner went to win-tooling — a repo with no floor. That
is why the harness's hands lived for months in ungoverned code with two resolver copies and a
deployed module from an unmerged lane.

**(d) Baseline substrate.** Codespaces (44 RED) vs Windows (28 RED). "28 == 28" was arithmetic
coincidence and the integrator was right to refuse it. **Landed: the gates ship against Windows,
therefore Windows is the baseline.** Codespaces keeps a real role — fast read-only compute, a
RED *list*, never a verdict.

**(e) JOURNAL.** Keep / render / delete / window / PR-as-anchor, matrix with seven criteria.
**Landed: B — the anchor is a property of the commit (`[#id]` + a body), the pre-push gate reads
commit messages, and `JOURNAL.md` becomes a render of `git log --first-parent --merges`.**
Deliberately NOT landed as a repo change: it amends ADR-85, which is spine, and its own decider
(the night's DELETE-LIST row 0 — which process READ JOURNAL in 30 days for anything but checking
it was written) **was never produced**, so the verdict is provisional by construction.

**(f) Batch V's lane list.** V-7 (FPG-1 spine) was swapped out for V-8 (offload admission) on
the operator's "Enterprise is a priority". **This seat now judges that swap wrong on the merits:**
the spine returned as V-9 in the same batch anyway, so the swap bought nothing and briefly
removed the single most important lane from the plan. Recorded so the next seat does not repeat
the pattern — *a priority ask is a reason to add a lane to the next batch, not to displace the
critical path from this one.*

**(g) Speed vs measurement on deletion.** The census counted 32 orphans on 2026-09-08; something
counted 39 on 2026-09-09; nothing reconciled them. **Landed: do not delete on a contested count.**
Only three deletions survive unambiguously (three `SUPERSEDED` OneDrive hook copies, `/override`,
`setup-fleet-scheduler.ps1` as a declared bootstrap). This is frustrating and correct.

**(h) Review as paste vs gate.** Terra review was requested by an operator paste at least twice
this window. **Landed: review is a merge gate — a lane branch with no tally line carrying
reviewer model and HIGH raw/fixed/unresolved cannot merge.** Filed.

## 3 · Considered and REJECTED — do not relitigate

| Option | Rejected because |
|---|---|
| **GitHub Issues as the state carrier** (conductor option A) | lock-in; breaks "decisions are files"; scored 52 vs E's 58 |
| **Claude Code native orchestration as the primary conductor** (option B) | runs on the operator's workstation and bills tokens per orchestration turn. **KEPT as E's fallback** — same task files, same graph, no state migration |
| **A workflow engine — Prefect / Windmill / Kestra / Temporal** (option C) | adds a server to operate and replaces not one existing hook; 38/58 |
| **A local `transitions` + sqlite state machine** (option D) | another custom loop file; the operator rejected it in the same words |
| **Moving the PowerShell dispatch layer into the hub** | breaks ADR-28; see 2(c) |
| **Copying Maister's code** | would stand a second organ set beside ours. The *shape* is adopted; the code is not |
| **Extending `ecosystem/organ-registry.yaml` to all 216 census rows** | **retracted by this seat mid-window.** It would be a hand-maintained copy of the graph — INBOX-037's defect at the spine. The registry is a QUERY |
| **Raising `[#589]`'s byte bar to fit new rows** | raising a bar to fit the first rows that hit it is what the row forbids; grooming is archival, and archival is an operator closure act |
| **Cutting a `-3` bundle to discharge P11** | at the time, validated by nothing — P11 had no code. Superseded: V-5 built the predicate |
| **Deleting the 32 orphans on the 2026-09-08 count** | contested by the 39-count; see 2(g) |
| **Substituting a different reviewer model when Codex hit quota mid-series** | changes the measure mid-measurement; the tally would lie |
| **Reasoning the six unattributed REDs into attribution** | one same-substrate run at `08c35b9c` decides it. `[#673]` says "never by argument" in the row body for exactly this reason |
| **AI Council for the conductor decision** | **the operator ruled it out explicitly** ("there will be no AI counsel"). Architecture decisions in this fleet now come from browser web-research + a weighted matrix + the operator's ruling. See §6 |

## 4 · Open questions — unresolved or deliberately deferred

**Operator words owed (each blocks something named):**
1. **GitHub Pro** — E's gate leg is unavailable on Free (403 on rulesets, verified).
2. **Orphan deletion** — BLOCKED on the 32-vs-39 census contradiction. Reconcile first.
3. **Five DEAD PLAYBOOK sections** — §1, §6, §9, §12 (config hierarchy only), §13 (Obsidian row only), each with per-section evidence in the chapter map.
4. **The 2026-08-29 deploy freeze** — the single named blocker on Stage 10. Never put to the operator before this window; put to him three times within it; still open. **This is the one that decides whether the next window delivers anything to a consumer.**
5. **JOURNAL's verb** — delete or wire, decided by a measurement not yet taken.

**Unratified intakes:** `#75` (offload admission — the recommendation is to ratify the BAR, which Copilot failed; ratifying the bar is not ratifying Copilot) · `#86` (`orphan_census` — ratify only if the intake names the census's own trigger, else V+1 builds an orphan that measures orphans) · the ADR-98 intake owed by AF-1 (unread by this seat; no recommendation offered rather than a blind one).

**Design questions genuinely open:**
- **Does win-tooling get the floor before corp-monorepo?** `AMEND-PROMPTS-DIR-001` §3 recommends yes — a consumer cannot be universalised by an ungoverned launcher — and it was never ruled. It costs corp-monorepo one window.
- **The 16-stage delivery-loop order is enumerated NOWHERE in the repo** (REVIEW §1 row 4); the recovery intake's ratio line is its fullest in-repo description. Either enumerate it or stop citing it.
- **Are the night bundle's ~220 UNVERIFIED locators usable?** 24 verified against ~220 carried. The Maister/spine leg (1c, codex) is the only adversarially checked one. The bundle is honest about this; the next seat must not read it as uniformly evidenced.
- **The model-agnosticism audit (leg 1f) has not been read by this seat.** It is the input to "swap the architect model in one config line", which is now an explicit operator requirement.
- **Seven R1 rulings** in REVIEW §4, including two ordered readers that died on free-tier quota with no substitute run (R1 held correctly), and one that is our own fault: our `PreToolUse` guard wedged `cursor-agent` and burned two paid runs, because `$CLAUDE_PROJECT_DIR` does not expand outside Claude Code and matcher `"*"` makes that a total refusal of every non-Claude tool. **In a repo that must become model-agnostic, our own guard refuses every other vendor.**

## 5 · Decomposition rationale — and what NOT to redo

**Why batch V had this shape.** Six committing lanes at the ADR-110 ceiling; all local because
all commit; one worktree each; V-4 (assembly debt) held on Sitting 1 because its rows are the
rulings' output. The sitting itself split three ways because Fable turns are budgeted (≤10) and
eleven rulings plus a version declaration do not fit one: S0 ruled homes-by-kind (the critical
path to a consumer that can be sealed), S1 ruled the eleven, S2 was administrative.

**Do NOT redo:**
- **The process-trigger census.** Merged; 216/160/24/32 with per-row evidence and both of its own wrong passes recorded. *Do* reconcile it against the 39-count — that is new work, not a re-derivation.
- **The eleven carried questions.** `DECLARE-SITTING-2026-09-08` is landed as intake; V-4's rows carry them.
- **The conductor decision.** Re-open only if one of `DECLARE-CONDUCTOR-DECISION` §6's five numbers moves (phase transitions without operator action · operator hours per feature · operator pastes per week · organs deleted · Actions minutes per week).
- **Dispatch retirement.** Ruled with its ordering condition: new hands hold before old hands let go — E must run one batch before anything in win-tooling is deleted.
- **Substrate pricing.** Measured (Codespaces ~5 min · local chunked ~110 min · local overnight ~60–90 min · `-n auto` is the OOM path and `-n 0` alone holds peak at ~600 MB).
- **P11's implementation gap.** Built by V-5; predicate runs against the live transport and reproduces the hand-run recipe by name.
- **Reading the 500 KB PLAYBOOK.** The chapter map exists (33,450 B, pinned `d12beac6`), with per-section verdicts on quoted pairs. Its DUP verdicts stand on citation pairs, not on a similarity score — `[#190]`'s detector cannot find what is wrong here, because the duplication is conceptual (a rule restated in different words), not copy-paste.
- **The Organ-map-is-a-registry-copy hypothesis.** DISPROVEN by measurement: 5 of 23 names shared with `organ-index.md`; ARCHITECTURE carries a failure-posture column nothing else has. The render must give the registry that column first.

**One decomposition lesson to carry:** the apparatus fires on the CONTRACT, never on what the
contract WRITES. A one-line backlog row provisioned a worktree and, after batch V closed, cost
~12 minutes and two merges under the self-referential anchor rule. `[#675]` carries this with a
size-gate Done-when.

## 6 · Off-repo context — changed INTENT only

**(a) The definition of "harness" changed mid-window, and it is now the operator's, not ours.**
It is process management: a registry of automatically triggered processes, *trigger event →
organ → artifact*. Anything no process triggers is **inventory, not harness** — it gets a
trigger or it is removed, and there is no third state. He never asks CC to run a library by
hand; the process must call it. This reframing is upstream of every other decision in the
window and it is why the census exists.

**(b) "Nothing is implemented without a task."** `nic nie wdrażamy bez tasków` — a task is the
control point over the process even when it is the longer road. Enforced today only at CLOSE;
the intent is at OPEN.

**(c) The measure of success moved to the operator's own day.** Not "the hub is healthy" but
**"I open corp-monorepo and I work."** Three months of building, nothing in a consumer. Every
plan should be read against that sentence.

**(d) Model-agnosticism became an explicit requirement this window.** The whole process —
handoff, seat boots, routing, dispatch, the browser contract — must survive swapping Anthropic
for Codex or Gemini. The goal is that switching the architect model is one config line. This is
new intent, not a restatement.

**(e) Deletion outranks addition, as a standing posture.** Not a preference — a complaint with
evidence behind it. The next window is judged on what it removed.

**(f) AI Council is out as a decision mechanism.** Ruled explicitly. Architecture decisions come
from browser web-research plus a weighted matrix with named criteria, presented for the
operator's ruling. He additionally demands that a decision be **re-evaluable later** — hence the
30-day measurement blocks now attached to the conductor and JOURNAL decisions. A recommendation
without a falsifier is not acceptable output.

**(g) Provider posture.** GLM and DeepSeek deferred (API-only, CLI unreliable). `gpt-6-astra` is
treated as the XL tier on cost — ruling-class and adversarial derivations only, explicit opt-in,
never a default, never lanes/reviews/fan-out. The cheaper providers are to be USED, not
theorised about: the operator is explicit that offloading read-only work to them is the point.

**(h) A hard boundary the next seat must not cross.** Substituting a tool the operator ordered,
without saying so, is treated as a false report — not as initiative. It happened once this
window (an ordered reader failed and CC's own subagents produced the work; this seat relayed the
result as fact). R1 of the night mission is the codified form: record the failure, mark the leg
SUBSTITUTED-PENDING-OPERATOR, do not silently swap.

## 7 · Ratified-in-chat register — not yet in the repo

**Terms and rulings ratified in chat, with their durable homes:**

| Term / ruling | One line | Home |
|---|---|---|
| **assembly debt / enforcement debt** | ruled-but-unrowed vs specified-but-uncoded — the two halves of "everything is built, nothing is connected" | LESSONS; partially carried in `docs/intake/2026-09-09-tech-window-close-rulings.md` (#90) |
| **declared enforcement without enforcement** | the class: a claim about a relationship that nothing verifies. Nine-plus instances in two days | LESSONS, as a named class with its instance list |
| **map vs conductor** | the graph answers questions; the conductor fires phases. Independent; the graph can exist without the conductor | ADR (spine), citing ADR-118 |
| **`DECLARE-HARNESS-IS-PROCESS-2026-09-08`** | the operator's harness definition — **cited by three committed audits and ABSENT from the tree.** REVIEW's finding #1 in its purest form | the repo, urgently — an intake or ADR; a P11 OPEN carrier today |
| **`DECLARE-JOURNAL-DECISION-2026-09-09`** | the anchor-in-commit decision — **deliberately not landed**; amends ADR-85, needs a terra-reviewed lane and a measurement | ADR-85 amendment via a lane |
| **"no AI Council"** | architecture decisions by research + weighted matrix + operator ruling, with a 30-day falsifier | PLAYBOOK (decision-making section) or STANDING_RULINGS |
| **the ordering condition on dispatch retirement** | new hands hold before old hands let go — E runs one batch before win-tooling deletes anything | carried in `DECLARE-DISPATCH-RETIREMENT` §4; needs a row |

**Interface behaviours relied on and not yet named in `protocols/OPERATOR-INTERFACE.md`:**

| Behaviour | What relying on it looked like | Home |
|---|---|---|
| **Named-session addressing** | the browser tells the operator WHICH session a paste goes to (integrator · dispatcher · working CC · win-tooling · night), because Cloud SDK shows many concurrent sessions. Getting this wrong cost turns | `OPERATOR-INTERFACE.md` |

<!-- CC transcription note - not the author's words. The answer above shipped SEVEN interface
     behaviours as "not yet named in protocols/OPERATOR-INTERFACE.md". Six were verified against
     that file on 2026-09-10 and found ALREADY DOCUMENTED, so they are struck per the operator's
     transcription instruction; one survives. Every other word in this ANSWERS region is verbatim. -->

> **Transcription note (CC, 2026-09-10) — six of the seven interface behaviours were struck as
> already documented.** The operator's instruction was that anything already named in
> `protocols/OPERATOR-INTERFACE.md` is struck before transcription. Verified line-by-line against
> that file; the six removed rows and their citations are:
>
> - **Browser writes decisions to the transport via the Drive connector** — `OPERATOR-INTERFACE.md:46-48`,
>   the prompts-dir constant: "a Google Drive folder synced by Drive for Desktop, **which the browser
>   reads/writes via the Drive connector**"; reinforced by "Rule 1 (inbox 029) — a browser decision
>   exists only as a file" (:147).
> - **Browser READS the transport itself** — the same `reads/writes` clause at :46-48, and §2's
>   `CC output` row: "read from the transport — `STATUS-*`, `LEDGER-<repo>`, `QUESTION-*`, close
>   packets — on 'check'. A pasted session log counts as a browser-seat defect."
> - **The END-OF-PASTE sentinel as a truncation detector** — :143-145, verbatim purpose: `PASTE_THIS.md`
>   "ships a terminal `=== END OF PASTE ===` sentinel so a truncated one is visible on sight."
>   **Residual drift, reported not struck:** the file documents the BARE sentinel; the live assembler
>   emits `=== END OF PASTE — n sections · b bytes ===`. The counts are undocumented.
> - **Model-switch line format** — :165 carries both strings verbatim: `ROUTINE — Opus is enough` /
>   `RULING AHEAD — Fable (est. ~N k tokens: <files>)`. **The answer's actual complaint survives the
>   strike and is a change request against that documented line, not an unnamed behaviour:** neither
>   form carries an explicit *stay / return / switch* verb, which is why the operator could not tell
>   them apart.
> - **A copy-ready block substitutes for a described action** — it is §7's own heading, at :250:
>   "Operator-action steps end with a copy-ready block." (The answer's Home column already conceded
>   this: "already the operator's standing rule".)
> - **CC transcripts pasted into chat arrive corrupted mid-token** — §2 is the named home, heading at
>   :132 ("Inline chat paste of large content arrives empty — so uploads are `.md` files"), with the
>   discriminator at :140-141 ("A paste that ends mid-sentence ended mid-transport"). The answer's own
>   Home column calls it "defect report against `OPERATOR-INTERFACE.md`" — which is Q6's stated
>   carve-out, not a behaviour missing from the file. **Its substance survives: the rule is written
>   and nothing enforces it**, which is this window's own `declared enforcement without enforcement`
>   class applied to the interface file.
>
> **`Named-session addressing` is genuinely absent and is the only row kept.** Nothing in
> `OPERATOR-INTERFACE.md` tells the operator which session a paste goes to. The nearest text is
> :83, "A chat paste is not addressable", which argues that *ownership metadata belongs in the file*
> (`owner-role:` at :70) — a different claim: it addresses the WORK, not the operator's paste.
