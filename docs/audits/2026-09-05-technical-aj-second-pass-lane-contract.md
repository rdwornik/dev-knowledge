# AJ SECOND PASS — shipped-vs-specified + live comparison — LOCAL lane contract (2026-09-05)

**Consumers:** `intake #70` (`docs/intake/2026-09-05-tech-aj-second-pass.md`) — this contract is
the dispatched form of that intake's frozen requirements, and the arc's deliverable is the evidence
its ex-ante acceptance criteria are judged against. Governance: ADR-111 (nothing from this arc
enters the tree except one audit and CANDIDATEs through the funnel).

**Frozen by:** the Layer-1 browser architect, ARCHITECT-INBOX-2026-09-05 item 003-C, under the
operator ruling of 2026-09-05 — *the test is approved; the goal is to improve OUR hub, not to
adopt a plugin that duplicates it*. **Dispatched by:** the FILINGS-2 CC session, 2026-09-05.
**Dispatched from:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Hub branch:** `worktree-aj-second-pass` · **Worktree pairing:** slug `aj-second-pass` ->
branch `worktree-aj-second-pass` (the `worktree-` prefix is applied exactly once, by the
provisioner — the flag takes the bare name).

| Model | Mode | Effort |
|---|---|---|
| opus | execution | high |

`opus` is the standing default for any arc touching `.dev-knowledge` (context load, not diff size
— PLAYBOOK Ch8 "Model + effort are stated at dispatch", AMENDMENT 2026-08-07). Judgment sections
override upward per the frozen text's Roles section.

## Substrate — LOCAL, by explicit exception

**Substrate:** `local`. The four axes route *read-only* to CLOUD and *execution* to
CODESPACE-on-green; this arc is neither. It needs the operator's **disk**: the vendor CLIs and
their authenticated credentials, a third-party plugin install, and a scratch directory outside
every repo. That is the Q2 cut — *operator-disk state -> LOCAL, stop* — and the cloud token is in
any case scoped to `dev-knowledge` alone, so a clone of `ai-council` is not reachable from there
(witnessed in the 2026-09-05 fleet-readiness dispatch). `local-execution = explicit-request` is
satisfied: item 003-B is the explicit request.

**The Ch8 LOCAL row, quoted — copied, never composed** (PLAYBOOK Ch8, "The dispatch table — the
SOLE literal-command site", row 1):

```
dispatch <FILE.md>                  prompts [y/N], then fires
dispatch <FILE.md> -DryRun          prints the resolved line, sends nothing
```

For this contract that is `dispatch AJ-SECOND-PASS-2026-09-05.md`, run **from the target repo
root** — the verb is cwd-bound.

## Dispatch

```
claude --bg --model opus --effort high --worktree aj-second-pass --permission-mode bypassPermissions "[dev-knowledge . intake-70 . AJ second pass] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\AJ-SECOND-PASS-2026-09-05.md"
```

The block above is what `dispatch` executes **verbatim**, substituting only the literal
`$env:CLAUDE_PROMPTS_DIR` token. It carries the `claude` head token because
`Invoke-Dispatch.ps1` refuses any other — *"this script never runs an arbitrary command from a
contract file"* — which is why this contract does not carry the `Dispatch-Lane` form
`gen_lane_contract.py` emits. Witnessed 2026-09-05 against
`docs/audits/2026-09-01-technical-batchf-launch-contracts/LANE-e-5-vision-relocation.md`, which
`dispatch ... -DryRun` refuses for exactly that reason. Reported to the browser architect as a
CANDIDATE; **not** repaired here.

## Dispatcher's resolutions — locators the frozen text leaves ambiguous

These resolve paths; they change no requirement. They exist because a locator a lane has not
resolved is a claim, not evidence.

1. **`$env:CLAUDE_PROMPTS_DIR` has two live values on this machine.** The USER environment
   variable is `H:\My Drive\CLAUDE PROMPT DIR` (the operator's browser channel, a Google Drive
   mount); the value in the dispatching process — and therefore the one this lane inherits — is
   `C:\Users\1028120\Downloads`. **The scratch root for FR2 is therefore
   `C:\Users\1028120\Downloads\aj-scratch\live\`**, which is what the frozen text's
   `$env:CLAUDE_PROMPTS_DIR\aj-scratch\live\` resolves to for this lane. Cloning into the Drive
   mount is refused: it would sync two full checkouts to Google Drive. If your `$env:` reads the
   H: value, use the absolute path above instead and say so in the deviations section.
2. **This contract is delivered to both prompts directories** (`H:\My Drive\CLAUDE PROMPT DIR\`
   and `C:\Users\1028120\Downloads\`) so the token resolves whichever value the reader's shell
   carries. The **authoritative copy of record is this in-tree file** (STANDING_RULINGS Q6,
   contract-as-file); the prompts-dir copies are a delivery channel.
3. **`ai-council`'s origin** is read from the hub's own registry —
   `ecosystem/ai-council/state.yaml` — not guessed. Resolve it before cloning; if it does not
   resolve, that is a PAUSE with the fact, not a substitution.
4. **Done-clause 0 applies:** the deliverable is a COMMIT on `worktree-aj-second-pass`. A receipt
   reporting success with zero commits is a FAILED run. Commit-and-STOP; the integrator merges.
   Copy the deliverable to the `to-browser\` subdirectory of the operator's prompts dir at STOP —
   a local lane can do this; do not skip it.

## Governance pointers

ADR-111 (the decision funnel — CANDIDATE is the only path, and no row is born here) · ADR-98
(intake genre) · ADR-112 (the two-tier adoption bar — Tier L evaluates, Tier S tries and keeps or
deletes; this arc is the evaluating half) · `protocols/STANDING_RULINGS.md` Q10 (a lane that
discovers a refuted premise PAUSEs with the fact — deviation-with-disclosure is not a licence) ·
PLAYBOOK Ch8 (substrate, dispatch, decision budget).

## Decision budget (V-2)

Execution mode. Ask only about: (a) any hub write outside `docs/audits/` and the candidate
filings, (b) an install or network fetch beyond the one named plugin in clone M, (c) a necessary
condition (NC1-NC6) you cannot satisfy — which is a PAUSE, not a question. Everything else is
decided against the contract's defaults and **reported** in the deviations section, never asked.

---

## FROZEN CONTRACT — verbatim, item 003-C

> Everything below this line is the architect's frozen text, carried byte-identically. Where it
> and the sections above appear to differ, the frozen text states the requirement and the
> sections above resolve a locator — they do not amend it.

## 003-C · FROZEN CONTRACT — "AJ second pass"

### Objective function
For each shared capability, a decision the operator can declare on evidence: ADOPT-INTO-HUB (as a
candidate) / ALREADY-RUNNING / REJECT — where "evidence" means an execution artifact from THIS arc,
never a document that says it exists.

### Functional requirements
FR1 SHIPPED-vs-SPECIFIED. For each of the 14 BOTH-partial / BOTH-different-name rows of the gap
    analysis §3 (rows 1,2,3,5,6,7,9,10,11,12,13,15,18,19,21 minus any BOTH-same): classify EACH side as
    RUNNING (a command was executed in this arc and produced the artifact — path recorded) /
    SPECIFIED (intake, ADR, or doc only — locator) / ABSENT. Output: a 14-row table with one execution
    witness per RUNNING cell. A cell marked RUNNING without an artifact path is RED.
FR2 LIVE COMPARISON on a scratch clone of ai-council (origin/main, cloned to
    $env:CLAUDE_PROMPTS_DIR\aj-scratch\live\ai-council-maister and a second identical clone
    ...\ai-council-dk). Task: ONE seeded, bounded S change chosen by CC from ai-council's shape
    (default: add one CLI flag with a unit test; if ai-council has an open S row, use it instead and
    say so). Leg M (Maister): install the plugin in that clone only, run /maister:init, then
    /maister:development <task>. Leg D (ours): the same task via our lane contract + local dispatch
    row on the second clone. Both legs record the SAME metrics (below). Plugin uninstalled and both
    clones deleted at the end; nothing pushed anywhere.
FR3 OPERATOR PRACTICES. From the course (M01L02, M01L04, M01L05, M02 ebook, M02L07, and the Maister
    README "Best Practices"/"Known Issues"): a list of ≤ 10 practices for the human operator, each with
    its locator and a yes/no "we do this today" with our locator or "no". No mechanisms — behaviours.

### Measurable tests (FR2 metrics, both legs, same table)
 m1 wall-clock start→stop · m2 tokens by model class (from the CLI's own usage output; "unknown"
 if not exposed, never estimated) · m3 files created/modified (count + list) · m4 tests written /
 tests passing after the run (run the suite yourself, do not read the report) · m5 number of
 human prompts required (every AskUserQuestion / needs-input counts) · m6 stalls: times the run
 stopped without finishing and needed "continue" · m7 gate honesty: does any machine-readable state
 field contradict a verdict artifact (the NO-GO/completed shape)? yes/no with paths · m8 artifacts
 a later session can resume from (list) · m9 what the run got WRONG in the code (reviewer: terra
 on both diffs, same rubric, tally in body) · m10 cost of the run if the CLI reports it.

### Necessary conditions (any failure = the arc reports FAILED, not a partial result)
 NC1 scratch clones outside every repo; `git remote -v` in each clone points at origin but NO push
     is ever run (witness: `git log origin/main..HEAD` shows local-only commits; teardown deletes
     both clones). NC2 plugin installed only in clone M; `claude plugin list` in the hub shows it
     absent before and after. NC3 the seeded task is identical text for both legs. NC4 licensed
     course content: paraphrase + locator only. NC5 no hub file changed except the deliverable and
     the candidates. NC6 every RUNNING cell has an artifact path.

### Success criterion (what makes the arc "worked")
 The FR1 table has execution witnesses for ≥ 80 % of cells; FR2 completed one full workflow on
 each leg OR recorded the exact stall point with m6 > 0; FR3 has ≥ 8 items with locators. Below
 that, the arc is INCONCLUSIVE and says which FR failed.

### Roles / models
 Reading, cloning, running: Opus orchestrator, Sonnet/Haiku fan-out (retrieval-only). Judgment
 sections (FR1 classification, the per-row ADOPT/RUNNING/REJECT proposal) on the strongest model
 the CLI exposes — try `claude-fable-5-1`; state the model used. Reviewer: terra on both FR2 diffs.
 The proposal is a PROPOSAL: the browser architect rules, the operator declares.

### Deliverable
 docs/audits/<date>-technical-research-aj-second-pass.md — §0 the decision table (14 rows ×
 ADOPT/RUNNING/REJECT proposal + witness) · §1 FR2 metrics table (two columns, m1–m10) · §2 FR3
 practices · §3 candidates (Z-C shape) · §4 cost, deviations, INCONCLUSIVE flags. Copy to
 to-browser/ at STOP. Commit-and-STOP; integrator merges.

### Anti-patterns
 No adoption of the plugin into any repo. No "they have it" without running it. No estimate where a
 number is not exposed. No editing of ai-council. No second resolver/tooling for metrics — use the
 CLIs' own outputs and `git`.
