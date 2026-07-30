# Codex Review — 446-v6-boot-prose (doc-lane, terra)

**Date:** 2026-07-30
**Branch:** `feat/446-boot`
**HEAD:** `7723a431`
**Diff range:** `main..feat/446-boot` (prose subset — 18 `.md`/`.tmpl` files)
**Codex version:** codex-cli 0.145.0
**Model:** `gpt-5.6-terra`
**Mode:** doc-review (invoked via direct `codex exec`, NOT the skill)

---

## Why this artifact exists (path record, [#445])

The `/codex-review` skill was run first, as instructed. Its documented path-guard filtered this
MIXED diff (11 `.py` + 16 `.md` + 3 `.yaml` + 2 `.tmpl`) down to the **code subset** and reviewed
it with the **code profile**, inheriting the config default model **`gpt-5.6-sol`** — so the
review the operator asked for (model **terra**, full diff) was not what the skill path produced:
the 18 prose files, which carry the substance of the v6 bump, were never reviewed, and terra was
never invoked. Both runs were PAID under the [#445] check (each named consumed files and surfaced
concrete findings; neither returned a bare SUCCESS).

- code lane → `docs/audits/2026-07-30-codex-446-v6-boot-build.md` (skill path, model sol, 3 HIGH)
- prose lane → this file (direct `codex exec -c model=gpt-5.6-terra`, 5 HIGH + 3 MEDIUM)

This is the known mixed-diff behaviour, not a skill defect: the rule is stated in the skill doc
("Mixed code+prose diffs are filtered down to the code subset ... prose in a mixed diff is not
separately doc-reviewed"). Recorded here so the coverage gap is visible rather than implied.

---

## Findings

No Critical findings.

## HIGH templates/handoff/v5/HANDOFF_BOOT.md.tmpl:51 — v6 bundle template still directs the retired per-probe ferry

**What:** The operator walkthrough tells the browser to reply `run <command>` for P1, then to run P2–P10 individually.  
**Why:** Newly generated v6 bundles contradict the one-evidence-block contract and reintroduce the transport v6 removes.  
**Fix direction:** Replace this walkthrough with one `/handoff-verify` invocation and one pasted evidence block; retain per-probe instructions only in the explicit pre-v6 path.

## HIGH .claude/commands/handoff.md:128 and :137 — supplement policy contradicts the inherited-claims gate

**What:** The supplement is defined as advisory, non-rederivable “why,” but every folded answer is then required to be live-verified and fails onboarding if unverifiable.  
**Why:** Strategic intent, trade-offs, rejected options, and off-repo context have no live repo source; architect bundles with valid supplements become intrinsically unverifiable/blocking.  
**Fix direction:** Keep non-repo supplement content advisory, and narrowly verify only claims that assert a repo-verifiable fact.

## HIGH protocols/HANDOFF_PROCESS.md:396 and templates/handoff/v5/PROBES.md.tmpl:102 — the §13(c) “emission vs. reading” ruling does not resolve the actual ordering conflict

**What:** The spec says readers consume `role → vision → standing topics → backlog`, while the emitted gate and operator runbook require `P0` standing topics before `P1` orientation.  
**Why:** These are both execution instructions, not merely independent table/display orders; an operator cannot follow both sequences.  
**Fix direction:** Choose one operational order and align the gate procedure, runbook, P1 heading, and seam explanation to it.

## HIGH templates/handoff/v5/PROBES.md.tmpl:59 — P0c is presented as a deterministic probe without a deterministic check

**What:** Its command only prints the hand-authored Purpose and asks CC to “name” an authority it serves; it cannot mechanically determine “unquotable” or “contradicted.”  
**Why:** This conflicts with the stated bounded-deterministic P0 contract and lets `/handoff-verify` overclaim a PASS/FAIL check.  
**Fix direction:** Define a mechanical matching predicate/source field, or reclassify P0c as an advisory judgment rather than a blocking probe.

## HIGH .claude/commands/handoff-verify.md:6 — command claims v5 support despite the documented pre-v6 exemption

**What:** `/handoff-verify` says it runs the one-block gate for “a v5/v6 handoff bundle,” while the canonical runbook says pre-v6 bundles use the per-probe ferry and are judged by their own era.  
**Why:** A v5 bundle lacks P0 and Destination rows, so invoking this command either produces an invalid v6-shaped block or blocks a deliberately exempt legacy handoff.  
**Fix direction:** Restrict the command to v6 bundles, or document a clearly non-onboarding legacy diagnostic mode consistent with the pre-v6 runbook.

## MEDIUM docs/handoffs/README.md:208 — current-version claim remains stale

**What:** “Current bundles are v5” and “v5 (canonical)” conflict with the v6 canonical spec and this document’s own v6 run-loop.  
**Why:** Operators can select the wrong era and wrongly use the per-probe flow.  
**Fix direction:** Mark v6 as current/canonical and describe v5 as the prior bundle era/lineage.

## MEDIUM ARCHITECTURE.md:225 and protocols/HANDOFF_PROCESS.md:40 — incomplete current-version sweep

**What:** The organ map still cites “HANDOFF v5,” and the current actor table is labelled “In v5.”  
**Why:** These are present-tense descriptions in files restamped `handoff-process@6.0`, not historical records.  
**Fix direction:** Update current-state labels to v6 or neutral “v5/v6 lineage”; retain v5 only where explicitly historical.

## MEDIUM .claude/commands/handoff-verify.md:3 and :10 — source citation points to the wrong spec section

**What:** The command cites HANDOFF_PROCESS §2 as the one-round-trip boot contract, but §2 defines the residual; the one-round-trip contract is §5.  
**Why:** The new command’s primary-source pointer sends users to unrelated doctrine.  
**Fix direction:** Point the description and source-of-truth line to §5 (and §13 only where mode behavior is relevant).

The new P0 rows do not appear to leak an answer value (count, SHA, verdict, date relation, or concrete group membership); the concern is P0c’s unenforceable semantic verdict, not anti-bluff value leakage.
