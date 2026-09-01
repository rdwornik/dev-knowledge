# ATLAS-R1 — Batch Usage Ledger D–F (SIDECAR to the landed HTML artifact)

- **Class:** census · **Date:** 2026-09-01 · **Lane:** ATLAS-R1 companion, compiled from tracked records only
- **Artifact:** `2026-09-01-census-atlas-r1-def-usage-ledger.html` — **same stem, landed VERBATIM**
- **Consumed by:** intake #66 (telemetry stream) · the standing offload rule's **visibility clause**

---

## Why this file exists

The `.html` beside it is the artifact, landed byte-identical and sha-verified per the architect's
2026-09-01 format ruling. This sidecar carries provenance, integrity and consumers so the corpus
stays markdown-indexed and the `.md` twin is what census and consumers cite.

## Provenance and integrity

```
source        C:\Users\1028120\.claude\jobs\1732b879\tmp\ledger.html   (EPHEMERAL — job-scoped)
bytes         28,748
sha256        444c7ac51b33e0024b133dee02ff361f73dd01adb0e2ada5fc03b0f6f793103d
verified      hashed at source AND re-hashed after the copy into docs/audits/ — identical
published     https://claude.ai/code/artifact/ec0fc7fa-0406-4766-bb6d-c4204be2d0f9
              PROVENANCE, NOT THE STORE.
measured at   HEAD 16f91f69 · window 2026-08-29 → 09-01 · 31 lanes · batches D, E, F
```

## The headline

```
lanes 31   local 21 · cloud 9 · codespace 1
distinct models 1        every one of 31 lanes: opus, effort high, execute mode
credits recorded 0
```

**The routing question has a one-word answer, and the interesting statistic is that nothing was
ever routed anywhere else.**

**The credits column is empty everywhere, and the ledger shows that rather than estimating it.** No
receipt carries a cost — the tier-A dispatch receipts record `Ok`, `Bound`, `SessionId`, `ReadId`,
`Failure` and the echoed text, and no tokens, duration or dollars. The one cost surface,
`logs/TOKEN-LOG.md`, is a **host-wide weekly aggregate** that cannot attribute a lane and **stops
before the window opens** (newest entry 2026-08-04; all three batches sit in a 25-day gap). The
codespace probe **burned real compute and recorded none**. Until `[#615]` lands — a model+version
commit trailer at commit-msg — per-lane attribution is **not merely unrecorded, it is
underivable**, because nothing in a commit says which model authored it.

## THE REVIEW FINDING — the answer to "which lanes ran with no review lane"

```
merged lanes D+E   17
  terra reviewed    6      pre-merge reviewed  2      NO REVIEW  9
reviewed fraction   8 of 17

NO REVIEW, by batch
  batch D   a · b · d · g      — and the WHOLE batch has no review record of any kind
  batch E   DC-1 · DC-4 · DM-3 · DM-5 · HY-1
            (DM-3 and DM-5 were drafting/filing lanes that changed no code)
```

**The cause is named as a process defect, not a reporting one:** the lanes were integrator-verified,
which is real, and is not independent review. The terra round ran **post-merge** — the weaker
position — and records itself that way rather than presenting itself as a gate.

**Merged is not dispatched.** 17 of 31 is not a failure rate: 9 were read-only cloud censuses owing
no merge, batch D's `c` was HELD on a file conflict, `h` was a re-cut carrying no merge SHA, DC-3
was split by operator adjudication, and the codespace probe went RED. The ledger keeps them apart.

## TWO CORRECTIONS THIS SIDECAR OWES, both from events after HEAD `16f91f69`

1. **The batch-F row has expired, exactly as the ledger predicted.** It records batch F as
   *"derived, not frozen — zero lanes"* and states its own expiry: *"the next freeze commit
   supersedes it."* That commit is `12720fcf`. **Batch F is FROZEN — 7 committing lanes, both gate
   layers, zero deviations** (`docs/audits/2026-09-01-technical-batch-f-manifest.md`). The ledger
   was right about its own limit, which is why the limit is honoured here rather than left to a
   reader.
2. **DC-3's review column under-reads.** The ledger shows `operator SPLIT` and no reviewer, which
   is true of the lane as dispatched. The **reconstruction** of its accepted half took a two-pass
   terra loop — 3 findings, all fixed, pass 2 CLEAN, one premise refuted — recorded at
   `docs/audits/2026-09-01-technical-dc3-split.md` §5. An adjudication is not a review, and the
   review that did happen belongs to the branch that replaced the lane.

Also superseded: the ledger's `filing capacity BLOCKED` line. The `[#589]` bar was re-baselined
70,000 → 72,000 after an overdue groom found nothing closable (`6b256fb9`).

## Consumers, recorded at landing

- **intake #66 — the OBSERVABLE HARNESS**, telemetry stream. This ledger is the measured statement
  of what that stream would have to carry, and of what is underivable without it.
- **The standing offload rule's visibility clause** — the rule presumes an operator can see what a
  lane burned. This ledger measures that they cannot, anywhere, for 31 consecutive lanes.

---

## AMENDMENT 1 — 2026-09-01: the model column is a DECLARATION, and its headline is false

> **In-file amendment marker.** The landed HTML is untouched — a generated view is not edited in
> place. This sidecar is where its correction lives, which is one of the reasons the sidecar
> exists.

**The ledger's headline — *"Every one of the 31 lanes ran on opus at effort: high"* — is FALSE.**
Batch E ran **MIXED: 8 sonnet, 5 opus** across the thirteen lanes whose session transcripts survive.

The ledger did not misread anything it claimed to read. It states its own method — *"three of the
five columns reconstruct cleanly from committed manifests and contracts"* — and every batch-E
contract declares `| opus | execute | high |`. **The model column is a DECLARATION rendered as a
measurement**, and the declaration is wrong because three surfaces default to `opus`
independently: the contract generator's `DEFAULT_MODEL`, `Dispatch-Local`'s own `-Model` default,
and this ledger reading the first rather than the run.

**The conclusion drawn from it is therefore false twice over.** *"There is no model variance to
analyse"* — there is variance, and it is invisible to every committed surface, which is a sharper
finding than the one the ledger reached.

Witness, per lane, with turn counts, plus the OS-process capture that independently confirms it:
`docs/audits/2026-09-01-verification-model-routing-witness.md`. **`[#615]` stays the enabling row:**
session transcripts live outside the repo, per-machine, and are not a governance surface.

**What survives unchanged:** every other column, the credits finding (still zero, still
underivable), the review finding (17 merged, 9 unreviewed), and the counting note. Only the model
column and its headline are affected.
