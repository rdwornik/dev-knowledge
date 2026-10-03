# Codex Review — foundation-10-model-currency

**Date:** 2026-10-04
**Branch:** `worktree-foundation-10-model-currency`
**Diff range:** `origin/main...HEAD` at `3157d69b` (the base this lane merged at step 0)
**Mode:** diff-review, isolated read-only session (the diff and the changed files in an empty folder — not the lane)
**Consumer:** `LANE-FOUNDATION-foundation-10-model-currency.md` (Done-contract item 3, "the review record citing this contract inside it");
`ecosystem/provider-registry.yaml` (the `last_verified` / `evidence` fields of the five model rows name this record as their evidence); `[#1016]` (the grok-4.6 currency discrepancy, whose open question the served `grok-4.7` evidence here answers)

*(The review sections below are filled in after the review ran; the ledger comes first because the registry rows cite it.)*

---

## Served-evidence ledger (2026-10-03 reads, re-read 2026-10-04)

Each id below was read as SERVED from a run's own record, not from a release note. Transcript counts
come from `~/.claude/projects/<dir>/<session>.jsonl`, counting assistant messages by `message.model`
(read by this lane with a throwaway script in its job tmp; timestamps are UTC).

| id | served evidence | where |
|---|---|---|
| `claude-sonnet-5-5` | FOUNDATION lane transcripts carry `message.model` = `claude-sonnet-5-5` and no other model: `foundation-3-handoff-boot` 470 + 24 messages (2026-10-03 15:35Z-18:13Z), `foundation-6-ci-speed` 491 (17:08Z-20:48Z; plus 4 `<synthetic>` stop-hook messages), this lane 102 at the time of the read (22:11Z-22:23Z). First read: the render record's step 0.3 probe, job `0d5e4736`, `message.model` = `claude-sonnet-5-5` at 11:56:09Z and 11:56:12Z | transcripts (job records); `to-browser/SESSION-gen-foundation-record-2026-10-03.md` step 0.3 (transport) |
| `claude-opus-5-5` | the render seat's transcript (`seat-render-foundation`, session `c468771a`): `message.model` = `claude-opus-5-5` on all 247 assistant messages (11:49Z-12:23Z); its record's header reads "model served: claude-opus-5-5" | transcript (job record); `to-browser/SESSION-gen-foundation-record-2026-10-03.md` line 10 (transport) |
| `grok-4.7` | three independent reads, each with the id from the CLI's own `usage.json` `primaryModelId`: the AMEND-3 probe (2026-10-03 15:41:42Z, nonce `8879e2891328c4d869983998` returned); the foundation-3 re-run (nonce `NONCE-1d8ae831cbf4`, `modelUsage` holds only `grok-4.7`); foundation-6 review 1 (nonce `STONE-4417`) | `docs/audits/2026-10-03-codex-foundation-3-handoff-boot.md` (re-run section, "Served model"); `docs/audits/2026-10-03-codex-foundation-6-ci-speed.md` ("Review 1"); the probe in the transport render record |
| `gpt-5.6-terra` | foundation-6's second review: the run's own header read `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`. `codex --version` on this host reads `codex-cli 0.155.0` (read 2026-10-04) | `docs/audits/2026-10-03-codex-foundation-6-ci-speed.md` ("Review 2") |
| `gemini-3.8-flash` | the B2-prep digest's served line: "agy 1.2.16, 'Gemini 3.8 Flash (High)' on every run (run-log label)". `agy --version` on this host reads `1.2.16` (read 2026-10-04) | `to-browser/DIGEST-B2-PREP-2026-10-03.md` line 9 (transport) |

**Honest limits, so the dates are not read as stronger than they are.**

- The `claude-sonnet-5-5` and `claude-opus-5-5` rows have no in-repo run record of their own: the repository's
  `logs/MERGE-RECEIPTS.jsonl` rows for the FOUNDATION lanes carry no `ran_model`, and `logs/LANE-COSTS.jsonl` has no row for
  them yet. This ledger is therefore the in-repo record, and it is a reading of job transcripts that sit outside the repository.
- The `gemini-3.8-flash` row rests on a run-log LABEL in a transport digest. This lane did not re-run agy: the digest records the
  agy quota as exhausted after 15 groups (reset in about four hours), and a served read here would spend a call for a fact
  already recorded. The label is the weakest of the five reads; the next served agy run is the right moment to strengthen it.
- No price was read for `claude-sonnet-5-5`, so its row carries no `rates:` block and the reader refuses it by name.
