# Copilot Enterprise — implement-role admission evidence

**Lane:** `lane-provider-registry` (`LANE-5A-8-provider-registry.md`, WAVE5A). **Carries:** the
in-repo evidence for `ecosystem/provider-registry.yaml`'s `roles.implement.order[].
copilot-enterprise.admission` and `providers.copilot-enterprise.licence`, both moved to
`admitted` / `permitted` by this lane under operator ruling O-3 (`RATIFICATION-2026-09-23-
copilot.md`, transport-only — cited here for date/author, never as the evidence itself).

**Consumer:** `ecosystem/provider-registry.yaml:596`, copilot-enterprise's `implement`-role
admission entry (`evidence: docs/audits/2026-09-23-technical-copilot-admission-evidence.md`),
which cites this file by path as its evidence.

## Why this file exists

The lane's done-contract requires the admission entry's evidence to cite **in-repo artifacts
only**. Two of the four artifacts — the ab-828 and ab-832 `HANDBACK.json` / `copilot-usage.json`
receipts — exist only on the transport (`H:\My Drive\CLAUDE PROMPT DIR\receipts\lane-ab-{828,832}-*\`),
never landed in this repository. This file is the commit-in copy the done-contract asks for,
with the provenance stated rather than presented as an original in-repo artifact.

**Copied 2026-09-23** from the transport paths above, byte-for-byte reproduction of the top-level
`HANDBACK.json` and `copilot-usage.json` in each lane's receipt directory (not the `attempt-1/` or
`fix-1/` intermediates).

## The four in-repo artifacts

### 1 — `JOURNAL.md:962`

> **MERGED** `[#832]`, the operator-ordered correction of lane z-11's repository selection: a
> fresh-HEAD re-verification of copilot-collections against its anchor. No anchor claim found
> gone; claims whose counts or model spelling moved are marked **changed**, not carried;
> `tsh-` namespacing, `applyTo` scoping, XML tags and the large agent/skill roster stay
> **REJECTED** for a solo Claude-Code hub. Not in the close order's named list; merged because
> it was finished, clean and idle since 2026-09-16 21:30 -- the close order's headline is "merge
> every finished branch". A non-Claude lane (Copilot co-author): `lane_cost.py` finds no
> transcript, so its cost is UNKNOWN, not zero. **No tests run here**, by operator order.

### 2 — `JOURNAL.md:1113`

> ...828 closure-census (Copilot producer + Codex reviewer), 802 conductor-reads-the-freeze, 664
> spine witnessed, 694 cost telemetry, 832 copilot-collections comparison, 833 seat registry, 834
> protocols heading gate. ...

### 3 — merge `88dc48f4`

```
commit 88dc48f4fe03571c48df86db77bcceb336d67cc8
Merge: bc8ddda5 48bfe2ca
Author: rdwornik <robert.dwornik@outlook.com>
Date:   Thu Sep 17 13:01:11 2026 +0200

    Merge branch 'worktree-lane-ab-832-copilot-collections-comparison' @ 48bfe2ca -- [#832] copilot-collections comparison re-run

    kill-candidates: none -- the lane's own commits carry its filings

 BACKLOG.md                                         |   1 +
 JOURNAL.md                                         |   8 ++
 ...l-lane-ab-832-copilot-collections-comparison.md | 114 +++++++++++++++++++++
 tasks/832-copilot-collections-comparison-rerun.md  |  12 +++
 tasks/manifest.json                                |   6 +-
 5 files changed, 140 insertions(+), 1 deletion(-)
```

`docs/audits/2026-09-16-technical-lane-ab-832-copilot-collections-comparison.md` (this merge's
own audit artifact) and its sibling `docs/audits/2026-09-16-technical-lane-ab-828-closure-
census.md` are both already in-repo and are the fifth and sixth artifacts a reader can open
directly, alongside this file.

### 4a — `receipts/lane-ab-828-closure-census/HANDBACK.json` (transport copy)

```json
{
  "slug": "lane-ab-828-closure-census",
  "contract": "LANE-ab-828-closure-census.md",
  "branch": "worktree-lane-ab-828-closure-census",
  "started": "2026-09-16T21:18:41.9528557+02:00",
  "contract_sha256": "95874ff3e927821c2b1dbe53590ef73a8f25caf089dce45c35e755a91b12cd3d",
  "base": "f8ca1d40",
  "producer_exit": 0,
  "producer_served_model": "gpt-5.6-luna",
  "commits": 1,
  "stash_list": 0,
  "reviewer_exit": 0,
  "reviewer_model": "gpt-5.6-terra",
  "review_critical_or_high": 3,
  "finished": "2026-09-16T22:02:26.1559990+02:00"
}
```

### 4b — `receipts/lane-ab-828-closure-census/copilot-usage.json` (transport copy, trimmed to the
top-level totals — `modelMetrics`/`agentMetrics`/`codeChanges.filesModified` repeat the same
figures per-model and are omitted here as restated detail)

```json
{
  "totalPremiumRequestCost": 1,
  "totalUserRequests": 1,
  "totalNanoAiu": 29655749000,
  "tokenDetails": {
    "input": { "tokenCount": 318 },
    "cache_read": { "tokenCount": 10673737 },
    "cache_write": { "tokenCount": 173163 },
    "output": { "tokenCount": 33107 }
  },
  "totalApiDurationMs": 393937,
  "sessionStartTime": "2026-09-16T19:19:13.438Z",
  "codeChanges": {
    "linesAdded": 455,
    "linesRemoved": 35,
    "filesModifiedCount": 24
  },
  "currentModel": "gpt-5.6-luna",
  "lastCallInputTokens": 37044,
  "lastCallOutputTokens": 248
}
```

### 4c — `receipts/lane-ab-832-copilot-collections-comparison/HANDBACK.json` (transport copy)

```json
{
  "slug": "lane-ab-832-copilot-collections-comparison",
  "contract": "LANE-ab-832-copilot-collections-comparison.md",
  "branch": "worktree-lane-ab-832-copilot-collections-comparison",
  "started": "2026-09-16T21:20:12.0961551+02:00",
  "contract_sha256": "baa07f2d22bd6a599c3860c0bf91896eb9276c302cb7825ff6d356f80b04261f",
  "base": "f8ca1d40",
  "producer_exit": 0,
  "producer_served_model": "gpt-5.6-luna",
  "commits": 2,
  "stash_list": 0,
  "reviewer_exit": 0,
  "reviewer_model": "gpt-5.6-terra",
  "review_critical_or_high": 1,
  "finished": "2026-09-16T21:38:00.2136476+02:00"
}
```

### 4d — `receipts/lane-ab-832-copilot-collections-comparison/copilot-usage.json` (transport copy,
trimmed the same way as 4b)

```json
{
  "totalPremiumRequestCost": 1,
  "totalUserRequests": 1,
  "totalNanoAiu": 9778853000,
  "tokenDetails": {
    "input": { "tokenCount": 120 },
    "cache_read": { "tokenCount": 2644304 },
    "cache_write": { "tokenCount": 112717 },
    "output": { "tokenCount": 13916 }
  },
  "totalApiDurationMs": 164417,
  "sessionStartTime": "2026-09-16T19:20:41.967Z",
  "codeChanges": {
    "linesAdded": 132,
    "linesRemoved": 0,
    "filesModifiedCount": 3
  },
  "currentModel": "gpt-5.6-luna",
  "lastCallInputTokens": 112720,
  "lastCallOutputTokens": 285
}
```

## What this evidence does and does not establish

**Establishes:** both lanes exited 0 on the producer step, served by `gpt-5.6-luna` (Copilot
Enterprise's served model on this host), each committed real work, and were reviewed by Codex
terra (`gpt-5.6-terra`, exit 0) before merge — one commit for ab-828 (3 critical-or-high review
findings, addressed before the merge this file's §3 shows), two commits for ab-832 (1
critical-or-high finding). Both premium-request costs are `1` — i.e. one premium request billed
per lane, metered to the BY-Product-Development enterprise org seat, consistent with the
`providers.copilot-enterprise` billing note already in `ecosystem/provider-registry.yaml`.

**Does not establish, and is not cited for:** the RATIFICATION's specific figures "3/3 correct,
0.46 AI credits, 14 s" — those numbers appear in none of the four artifacts above, and
`to-browser/DIGEST-OPUS55-HARNESS-2026-09-23.md` Part A independently confirms no 2026-09-17
admission record exists anywhere in this repository under that description. The lane's
done-contract names this explicitly ("Do not cite '3/3, 0.46 credits, 14 s': those figures have
no repo source"), and this file does not cite them.

**The invocation admitted here is the transport script, not an in-repo verb.** Both lanes were
launched by `run-lane-copilot.ps1` (on the transport, `H:\My Drive\CLAUDE PROMPT DIR\`), not by
`scripts/dispatch.py launch`. `ecosystem/provider-registry.yaml`'s admission note records this
distinction; giving Copilot an in-repo producer verb is wave 5b's job (`RATIFICATION-2026-09-23-
copilot.md`'s systemic-fix item 1).

## Disposition

Role `implement`, provider `copilot-enterprise`: **ADMITTED** 2026-09-23, `decided_by: operator`
(O-3), on the evidence above. Provider `copilot-enterprise` licence: **permitted**, 2026-09-23,
`decided_by: operator` (O-3) — the corporate Copilot budget may be used for this repository's
work, per `RATIFICATION-2026-09-23-copilot.md` §O-3, whose precondition
(`DECLARE-COPILOT-TRIAL-2026-09-23.md`) the operator records as met. Both edits land in
`ecosystem/provider-registry.yaml` in this lane's commit.
