# Close-out diff review -- b2w3-red-burn-down (Copilot route, Codex limit-refused)

**Date:** 2026-10-10
**Branch:** `worktree-b2w3-red-burn-down`
**Reviewed tip:** `4cedf945` (five fix/registration commits plus the sync merge of `origin/main` `b78c08b6`)
**Diff range:** `origin/main...HEAD` (`diff.patch` sha256 prefix `ca6ae45f2493`)
**Mode:** close-out diff review (common rules 2 (e), S-38 (b))
**Tally:** 0/0/1/0 <!-- Critical/High/Medium/Low -->

Consumer: lane contract `LANE-1341-b2w3-red-burn-down.md` (batch B2-W3, lane 2; rows [#1342] [#1345] [#1346] [#1023] [#1481]; contract sha256 prefix `3cc75e97515f`), whose Done-contract item 6 requires this record.

## Route and proof of reading

- **First route, Codex `gpt-6-astra`, refused on a usage limit.** `codex exec -m gpt-6-astra -c model_reasoning_effort=high -s read-only` (codex-cli 0.155.0, session `01a12630-3a48-7281-b021-e62b94749bd5`, header `model: gpt-6-astra`) exited 1 at 2026-10-10T14:21:02Z with `You've hit your usage limit ... try again at 4:39 PM.` Not retried inside that window (S-32). No review output exists from it.
- **Second route (S-38 order 2), the Copilot CLI**, a different vendor from the producer (Anthropic): `copilot -p ... --model gpt-6.1-sol --add-dir <isolated folder> --allow-all-tools --no-ask-user -s --no-color --usage-output-file`.
  - **Served model id, from the tool's own usage file** (sha256 prefix `1e6fed756bc5`, session start 2026-10-10T14:21:56Z): `modelMetrics` key `gpt-6.1-sol`, 1 request.
  - **Nonce returned:** `c97e5228ec9f` (the value in the folder's `nonce.txt`).
  - **Input hashes returned and matching the files read:** `diff.patch` `ca6ae45f2493`, `contract.md` `3cc75e97515f`.
- The folder held only `contract.md`, `diff.patch`, `log.txt`, the eight changed files at the tip and `nonce.txt`.

## Findings

CRITICAL: (none)

HIGH: (none)

MEDIUM -- `scripts/telemetry_emit.py:637-646` (`_apply_pragma`): the deadline is tested only after a failed attempt, not before the next one. A refusal at 4.99 s sleeps and tries again at about 5.04 s, and that attempt can itself wait up to the connection's 5 s busy window, so the stated 5 s window does not bound the retries tightly (worst case about the window plus one backoff plus one busy wait; still finite). The injected-clock test asserts only a lower bound (`now >= JOURNAL_SWITCH_WINDOW_S`), so it does not see this. Fix direction: stop retrying when `monotonic() + backoff >= deadline`, and assert an upper bound on the fake clock for a near-deadline failure.

LOW: (none)

TALLY CRITICAL:0 HIGH:0 MEDIUM:1 LOW:0

## Disposition

- No CRITICAL or HIGH finding, so nothing is a gate for the handback (common rules 2 (e)).
- The MEDIUM is **recorded, not fixed in this lane**: the retry is finite (one extra attempt past the window), the failure it guards is a rare CI start-up race, and changing the reviewed code after the review would leave the reviewed diff and the landed diff different. It is carried as `BUILD-NOTE` for the integrator and as `ROWS-OWED` in the session file; the fix direction above is the whole change.
