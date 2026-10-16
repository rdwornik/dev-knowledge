# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-M4-RUNNER-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-M4-RUNNER-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] c8e03da2b3d82b16. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: CHALLENGE matrix M4 - design section 3 runner choice, re-scored with measured citations only. Verdict AGREE for BUILD-1 scope (a = conductor + doit + pydantic); python-statemachine stays behind the Q14a spike in [#669] (BUILD-2), as design D3 already says.

# M4 - the runner (design section 3), re-scored

## Why re-score
The design's matrix (89 for e) carried 4s and 5s without citations (its own O13); `decide_checks` caps those at 3. V9 has since run.

## Evidence
- V9 (DIGEST-VERIFIED-HARNESS-MAP-2026-10-15, "V9 engine answer"): doit halts at the first failing task and exits 1 with no model call; Workflow gated only via an LLM-relayed field, ~122k tokens for a 2-row table; /loop has no per-step exit gate.
- doit 0.37.0 locked (uv.lock:408-413), chained by `task_dep` (scripts/dodo.py:330-345); receipts fresh only on exit 0 + input hash (dodo.py:243-256); no timeout on the stage run (dodo.py:302) - the adapter is needed whatever runner wins.
- python-statemachine: Q14a is conditional on a spike (STANDING_RULINGS.md:5653); no spike has run.
- X-I6-1 (Codex): psm would be a second orchestration authority beside doit. Held for BUILD-1.

Weights: unattended=20 code=15 libfirst=15 modelagnostic=15 osagnostic=10 tokens=10 testable=10 simplicity=5
| Option | unattended | code | libfirst | modelagnostic | osagnostic | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| a. conductor + doit + pydantic | 3 | 4[^1] | 4[^2] | 3 | 3 | 4[^3] | 4[^3] | 4[^1] | 3.55 |
| e. (a) + psm now | 3 | 4[^1] | 4[^2] | 3 | 3 | 4[^3] | 3 | 2 | 3.35 |
| b. dynamic workflows | 2 | 3 | 3 | 1 | 3 | 1 | 2 | 3 | 2.20 |
| d. durable engine (DBOS) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 2.90 |

[^1]: measured -- scripts/dodo.py:330-345 task_dep chain, read 2026-10-15
[^2]: measured -- uv.lock:408-413 doit 0.37.0 locked; no new dependency
[^3]: measured -- V9 toy: doit p1=True p2=True p3=False, exit 1, no model call (VERIFIED-MAP V9)

## Verdict: AGREE (BUILD-1 freezes option a; e's psm leg is BUILD-2 [#669] after its spike - unchanged from design D3)
