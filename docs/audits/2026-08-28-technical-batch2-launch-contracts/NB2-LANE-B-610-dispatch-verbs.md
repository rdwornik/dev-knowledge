# NB2 · LANE B — [#610] carrier half: Dispatch-After · Harvest-Cloud · cp-quote — M

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\win-tooling` (a CONSUMER)
**Branch:** `worktree-lane-b-610-dispatch-verbs` · **Frozen by the architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N2.**

**Substrate:** local
**Worktree pairing:** slug `lane-b-610-dispatch-verbs` -> branch `worktree-lane-b-610-dispatch-verbs`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-b-610-dispatch-verbs --permission-mode bypassPermissions "[win-tooling . #610 . dispatch verbs] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-B-610-dispatch-verbs.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N2 — [#610] carrier half: Dispatch-After · Harvest-Cloud · cp-quote — M
> Write-scope: win-tooling `config/dispatch-helpers/DispatchHelpers.psm1` + `tests/
> test_dispatch_helpers_*.py`. Consumer repo ⇒ RULING-W: consumer worktree/branch → report;
> never direct hub writes; mechanism-before-act.
> Intent: the two verbs the 2026-08-26 night performed BY HAND get names — the missing half of the
> cloud fleet the operator wants. Harvest-Cloud is an EXTRACTION (the paginated
> GET /v1/code/sessions/{id}/events loop already exists inside Start-DispatchCloudV2 ~line 1079);
> Dispatch-After is documented as a FORM OF the ruled Dispatch verb, never a rival.
> Done: (1) both verbs exist, each with a usage line and its API surface recorded; (2) **P2 first:
> locate and REPRODUCE the cp-quote defect** (the argv seam is correct by construction — suspect
> the remote-path construction at ~lines 1279/1282/1402), then fix with a test that FAILS before
> and passes after; if it cannot be reproduced without a live codespace, ship the verbs, mark the
> cp fix MEASUREMENT-OWED with the reproduction recipe, and say so; (3) targeted tests only — the
> full suite is ~18 min and carries ONE pre-existing env RED (faster_whisper) that is NOT this
> lane's; (4) commit-and-STOP on the win-tooling branch.
> Anti-patterns: renaming the existing Dispatch-* family · touching .claude/ or
> .pre-commit-config.yaml (N1 owns them) · reporting the known env RED as a lane failure.

## LOCATORS RESOLVED AT DISPATCH — two of the contract's are OFF, and that is recorded

`config/dispatch-helpers/DispatchHelpers.psm1` is **2,472 lines**. Measured tonight:

- **"paginated … events loop … ~line 1079"** — line 1078–1085 is a **RECEIPT-POLLING** loop: one
  `GET /v1/code/sessions/$readId/events?sort_order=asc` per iteration until
  `Get-CloudFirstAssistantText` returns. **`next_cursor` appears NOWHERE in the module** (grep:
  zero hits). The pagination the 2026-08-27 harvest manifest describes was performed **by hand**,
  not by this code.
- **cp defect "~lines 1279/1282/1402"** — 1279, 1282 and 1402 are all inside **comment/doc
  blocks**. The live `gh codespace cp` argv arrays are at **1591** (`$cpMd`), **1637** (`$cpRun`)
  and **1669** (`$cpBack`), plus a doc echo at 1513–1516.

Neither correction changes the deliverable; both change where you look. **Report them in your
packet as contract-premise defects** — this batch is running a lane (lane G, in the hub) whose
whole purpose is to make that class refusable at freeze time, and a fresh instance is evidence.

Consequence for done-item (1): "Harvest-Cloud is an EXTRACTION" is **only half true**. The
single-page GET and the first-assistant-text selection exist and should be reused
(`Invoke-CloudApi`, `Get-CloudJsonMember`, `Get-CloudFirstAssistantText`,
`ConvertTo-CloudSessionReadId`); the **cursor loop does not exist and you are writing it**. Say
so rather than describing new code as an extraction.

## WHAT HARVEST-CLOUD MUST DO (from the reference instance, not from imagination)

The 2026-08-27 harvest — `docs/audits/2026-08-27-technical-night-harvest-manifest.md`, committed
in the hub since 2026-08-28 — is the behaviour to name:

- `GET /v1/code/sessions/{cse_id}/events?sort_order=asc`, following `next_cursor` to the end.
- **The report is the LONGEST assistant text, not the last.** The last assistant text is trailing
  Stop-hook backpressure noise ("Unchanged. Done.", "Nothing further.") from a container where
  `uv run --locked` cannot start. In all four 2026-08-26 sessions the report was assistant text
  **#2**, immediately after the receipt. Encode the selection rule; do not hardcode "#2".
- **Write the text VERBATIM, UTF-8 without BOM.** Two of four reports opened with a line of prose
  before their own heading; the correct behaviour is to keep the bytes and **record the
  deviation**, never to trim the file so a check passes.
- **ID TRAP:** create mints `session_<suffix>`; every read endpoint wants `cse_<suffix>`.
  `ConvertTo-CloudSessionReadId` already exists — use it.

## THE cp-QUOTE DEFECT (P2 — do this FIRST, before writing either verb)

The symptom recorded on the hub side is: `gh codespace cp` **writes literal quotes** into the
remote path. Reproduce it before you fix it. The argv arrays at 1591/1637/1669 are already arrays
(no shell re-parse on the PowerShell side), so the suspect is what goes *into* `remote:$remoteMd`
— how `$remoteMd` / `$remoteRun` / `$remoteJson` are built, and what gh's own transport does with
them. A test that FAILS before and passes after is the deliverable; a fix with no failing witness
is not accepted. **If it cannot be reproduced without a live codespace, ship the verbs and mark
the cp fix MEASUREMENT-OWED with the reproduction recipe** — that is the contract's own sanctioned
outcome, not a failure. Do not spin up a codespace to chase it; that is an operator-cost act.

## BOOT (win-tooling, not the hub — different rules)

You are in `.claude/worktrees/lane-b-610-dispatch-verbs` on `worktree-lane-b-610-dispatch-verbs`.
This repo is **win-tooling**: its own conventions govern, not the hub's. Read its `CLAUDE.md`
first. Run **targeted** tests only — the `tests/test_dispatch_helpers_*.py` files covering your
diff — never the full suite: it is ~18 min and carries **one pre-existing environment RED
(`faster_whisper` absent)** that is **not yours** and must not be reported as a lane failure.
Copy this repo's own test invocation rather than composing one.

## THE FOUR THINGS THIS LANE DOES NOT DO

1. **No JOURNAL entry** in either repo, and **no hub writes at all** — the hub half of [#610] is
   lane C's, running concurrently. RULING-W: consumer worktree/branch, then **report**.
2. **No self-merge and no suggesting one.** Commit-and-STOP on `worktree-lane-b-610-dispatch-verbs`.
   Your branch enters a frozen integrator queue (you are merged *before* lane A).
3. **No `.claude/` and no `.pre-commit-config.yaml`** — lane A owns them and is committing in this
   same repo, in its own worktree, right now. Touching them is a collision, not a fix.
4. **No renaming of the existing `Dispatch-*` family**, and no touching the four pre-existing
   win-tooling worktrees or any branch but your own.

## YOUR PACKET

You cannot write to the hub, so land it in win-tooling at the path that repo's conventions give
artifacts (check its `CLAUDE.md`; if it has no artifact home, use
`docs/2026-08-28-nb2-lane-b-packet.md` and say you had to choose). It carries: per-done-item
**MET / NOT-MET / PARTIAL** with a witness each; the commit SHAs in order; the terra tally
(`codex exec` over your own diff — if codex is unreachable, one line with the error is a recorded
deviation, not a failure); candidate filings; budget decisions; deviations with owners.

Then **STOP**.
