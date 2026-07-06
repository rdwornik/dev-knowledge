# 2026-07-07 — ai-council measurement #4 (#267 scope-exercising arc) — DEGRADED + half-b landed

> **Outcome: Block-5 DEGRADED per the frozen contract.** The safe, pre-specified half of #267
> LANDED (the `engages:` scope condition + the observer FIRED-semantics test); the live
> scope-exercising re-measurement is DEFERRED as a stated fork (below). Spawn feasibility is
> **PROVEN**, so the blocker is a design decision the envelope forbids me from improvising,
> **not** a capability or credit failure. Written per the Block-5 contract + the mission's
> degrade-loudly rule.

## 1. Feasibility — PROVEN (not the blocker)

The nested isolated `claude -p` spawn works in this environment:

```
DEV_SECRETS_ENV=…/.secrets/.env  PYTHONPATH=deploy python -m lived_sandbox.cli prove-isolation --haiku
-> isolation PROVEN: sentinel present-in-configA=True (positive control) /
   absent-in-configB=True (isolation); exit 0
```

- `claude` CLI on PATH: **2.1.200**. Key resolves via `DEV_SECRETS_ENV` → `.secrets/.env`
  (`load_api_key`, 108-char `sk-ant-` key). GATE-0 isolation clean. No orphan clones left
  (No-leftovers invariant held).

So the credit-billing consumer arc *could* run. It was NOT run — see §3.

## 2. What LANDED (the safe, pre-specified half — #267 Done-when conjunct b)

The **scope condition** now travels on the two components' `engages:` entries
(`deploy/manifest-v1.2.0.yaml`, INERT to `deploy/tool.py` — additive metadata, version HELD,
#220-recorded):

- **`hub-toc-hooks`** — `scope: file-scoped: FIRED iff an edit matches the consumer's
  toc-freshness files: pattern, else ARMED-BUT-SKIPPED`.
- **`floor-hash-verify-hook`** — `scope: file-scoped on ^\.claude/CLAUDE-FLOOR\.md(\.sha256)?$:
  FIRED (and FAILING) iff a floor edit is staged, else ARMED-BUT-SKIPPED`.

Observer semantics the deferred measurement relies on are **pinned by hermetic tests** (no
spawn): `test_failing_floor_hook_is_fired_not_silent_267` (a FAILING floor hook classifies
FIRED, not SILENT — the floor-fail *is* the witness) + `test_scope_matching_toc_edit_fires_not_skipped_267`
(a scope-matching toc edit → FIRED, contrast the frozen-fixture G4a ARMED-BUT-SKIPPED).

## 3. What DEGRADED — the live scope-exercising measurement (Done-when conjunct a), and WHY

**The fork (an unspecified design decision):** #267 asks for "a second commit touching a
**per-consumer** scope-matching file." The scope-matching paths are genuinely consumer-specific
— verified against the real ai-council clone:

| Hook | hub scope | ai-council scope |
|---|---|---|
| toc-freshness | `^ARCHITECTURE\.md$` | `^protocols/COUNCIL_QUESTION_GUIDE\.md$` |
| floor-hash-verify | `^\.claude/CLAUDE-FLOOR\.md(\.sha256)?$` | same |

The `ARC_PROMPT` is **shared** by the hub self-clone arc and the consumer arc, and is pinned by
the frozen GATE-0 fixtures (`arc-green.jsonl` / `arc-silent.jsonl`). Making it produce a
scope-matching edit therefore requires making the arc **scope-AWARE**, and the mechanism is
**unspecified** by #267 (the item says "e.g."):

- **(i) hardcode per-consumer paths** in the arc — brittle, and pollutes the shared prompt with
  ai-council specifics.
- **(ii) discover the scope from the consumer's `.pre-commit-config.yaml`** — the arc reads each
  hook's `files:` regex and synthesizes/edits a matching file (regex→example is non-trivial in
  general).
- **(iii) instruct the child** (in `ARC_PROMPT`) to "edit one file matching each hook's `files:`
  pattern" — offloads scope-awareness to the child's interpretation (less deterministic; a
  blocked floor-commit mid-arc may confuse the child).

Each is a **measurement-harness DESIGN decision**, and modifying the shared, frozen-fixture-
calibrated `ARC_PROMPT` then burning consumer-arc credits to test it is exactly the class the
autonomy envelope reserves ("Make design decisions: NO; a fork not covered by the contract →
DEGRADE with the fork stated"). Improvising it unattended — on a calibrated harness, single-shot,
with the credit-balance-masquerade + calibration-drift gotchas in play — is the wrong call.

## 4. Recommendation (for the architect — decision reserved)

Pick the scope-aware-arc mechanism (§3 (i)/(ii)/(iii); **(iii) instruct-the-child** is the
lowest-code, but weigh determinism), then run the single billed `observe-arc --consumer
../ai-council --haiku` **attended** (so the credit-masquerade gotcha is caught live and the
calibration re-freeze is watched). Feasibility is proven; only the design + one watched run
remain. **#267 stays OPEN** — conjunct (b) landed, conjunct (a) deferred to that attended run.

## 5. Invariants held

Wave-3 instrument-side-only: **ai-council HEAD untouched** (only the probe clone, auto-cleaned).
ARMED-as-enforcing stays REJECTED doctrine — this encodes FIRED (the real firing), never
redefines ARMED. No consumer writes. Version HELD (additive `scope:` metadata, #220-recorded).
