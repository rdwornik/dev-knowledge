# DECLARE — the one register of this window's defects (every item becomes a mechanism, not prose)

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN`. Source: `to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`. Amended by
> `2026-09-23-technical-window-defects-amend.md` (D30-D34; corrects D16/D17).
> Carrier rows: one row per D1-D29 item, filed by `lane-landing-window` under this contract's
> Done-contract item 1 (citing an existing OPEN row where one already covers the item).

carried-by: OPEN
lands-via: LANE-5A-5 files one backlog row per item (in-repo provenance: ADR-120 + the cited audit), so this list becomes data in the repo
date: 2026-09-23
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)
basis: receipts and digests of waves 3, 4a, 4B; DIGEST-VERIFY-TIME; the operator's corrections 2026-09-20..23

**Principle** (operator, 2026-09-23): the backbone is code — scripts, hooks, gates, data. Prose only
states intent and double-checks against the code; it never triggers the process.

| # | Area | Defect (evidence) | Root cause | Mechanism that removes it | Wave |
|---|---|---|---|---|---|
| D1 | integration | merge median 93-98 min; tests run 2-3x per merge (VERIFY-TIME) | no owner of total verification time | one verification stage: each check runs once, results reused | 5a |
| D2 | integration | two known-reds registries (CI's 87-test baseline, 6 days stale, vs the batch registry): CI always red, ignored | two paths for one act | one registry, read by CI and local, refreshed by the merge moment | 5a |
| D3 | integration | CI's 8-min full suite is not the gate; a local subset takes 30-59 min | CI stayed report-only | CI verdict is the gate; local runs only Windows-only tests | 5a |
| D4 | tests | 93 % of the selection is prose-triggered; a JOURNAL change pulls in 58 files | the selector keys on the merge commit | doc-test tier once per batch; lane-diff selection (merged) as default | 5a |
| D5 | tests | `MERGE-RECEIPTS.jsonl` is unmapped in the selector (latent full-suite fallback) | missing mapping | map it, with a test | 5a |
| D6 | tests | connection test takes 18m59s; walk still stops at merge/gates | heavy integration test, reads prose tails | JSON verdicts (merged); slow tier split; gate fix | 5b |
| D7 | memory | 8+ reaps, 2 lanes lost to OOM, `-n` set by hand | no admission control | memory gate (psutil + filelock) inside the organs; `-n` from free memory | 5a |
| D8 | autonomy | 3 human waits of 8-10 h at night (a ruling, a permission prompt, dead lanes) | no defaults, no liveness, prompts hang | pre-authorized ruling table in batch orders; liveness watchdog; deny-and-point guard for root-path writes | 5b |
| D9 | autonomy | sessions left polls and wake-ups running (3x) | prose rule | session janitor at batch close | 5b |
| D10 | handback | the handback organ writes `REFUSED-<lane>.md`, the integrator's repair-order path (overwrote it once) | no transport schema | organ writes `HANDBACK-REFUSED-<lane>.md`; the adapter enforces writers | 5a |
| D11 | handback | the organ's self-check disagreed with the integrator's twice (false negatives) | two implementations of one check | organ and integrator call one comparator | 5a |
| D12 | integration | a lane merged a local unverified `main` (contamination, 2x) | shared refs across worktrees | origin-only sync; integration worktree (done by hand); purity check in the organ | 5b (merge path) |
| D13 | integration | ledger rows lack the merge sha; digest names 0 of 6 shas (B1/B4) | the moment records no steps | complete ledger row, `require` passes; the ledger line inside the merge commit | 5b (merge path) |
| D14 | contracts | a new organ needs a `harness.yaml` fate line that the contract forbade (refusal plus 8 h wait) | plan checked by eye | plan lint learns "new script -> fate line" | 5a |
| D15 | contracts | hidden cross-lane dependencies (A/C, W4-2/W4-4) | by-eye planning | plan lint (merged) runs before every freeze | now |
| D16 | contracts | the architect wrote every contract by hand, with a hard-coded model | routing lives in prose | contracts name role, size, kind; the router picks the model | 5b |
| D17 | routing | Copilot unused all window despite the operator's standing request and the 17.09 admission | routing not enforced | router from the table; per-account telemetry | 5b |
| D18 | routing | a 55-min Sonnet outage stalled lanes | no fallback | provider fallback list | 5b |
| D19 | transport | invented names, rename-to-superseded, collisions | no schema | registry of file kinds, enforced by the adapter; a command that runs an order by name | 5b |
| D20 | transport | Drive path hard-coded in every paste | env var not global | `HARNESS_DRIVE_ROOT` + `HARNESS_PROMPTS_SUBDIR` set (done); the path layer reads them | 5b |
| D21 | portability | Codespace blocked by Windows paths and shell tokens (a false "no Linux Drive client" premise repeated) | environment assumptions hard-coded | path layer + Drive API adapter + container CI job | 5b |
| D22 | compute | the laptop cannot carry the harness | a single substrate | compute ADR record (running); off-box execution host | 5b/5c |
| D23 | launch | the seat reads "absent" until the first hook event; occupancy exit 2 on a starting record | bind semantics; external format coupling | bind marks live; accept `state` or `status` | 5a |
| D24 | knowledge | decisions and audits lived only on Drive and were invisible to prior art | no landing | audits committed to `docs/audits`; decisions landed each wave | 5a (landing) |
| D25 | knowledge | ideas from earlier windows were lost (Codespace blocker, Copilot admission) | prose does not survive a handoff | the state store and ADR (running) | 5b |
| D26 | hooks | fleet health produced state in a start hook; its routine deletes untracked drafts | producer in a reader slot | split merged; hook architecture from postwave S2 | 5b |
| D27 | review | audits ran without independent verification | routing by memory | plan lint rejects an audit order without a Codex verification step | 5b |
| D28 | browser | the architect accepted big decisions too fast (state store) and relayed premises unchecked | no decision gate | ADR + matrix + debate + operator ratification for architecture-level changes | now |
| D29 | browser | the ledger went unupdated for 3 days | prose duty | batch close regenerates the ledger from the state store | 5b |
