# 2026-07-05 — Overnight autonomy run (CC MEGA-MISSION) — run log + Block-F audit

> **Living run log during the night; finalized as the Block-F audit at run end.**
> Appended at block boundaries (sanctioned append flow — audits accept dated addenda;
> the ADR-77 guard scopes transcripts/ADRs, not audits). Mission: pre-flight + Slice-B
> closure + consumer-run + consolidation, AUTONOMOUS NO-STOP, operator pre-authorized
> 2026-07-05. Safety envelope absolute. Model window 1: Fable 5.

## Night objective function (ex-ante)
- Minimum success: Block A closed (C4 green on real fixtures, #252 shipped) + Block C artifact.
- Full success: + Block B both runs recorded + Block D shipped.
- Hard zero: no safety-envelope violation; every self-adjudication logged.

---

## PHASE 0 — baseline + readiness — **COMPLETE (all four legs PASS)**

- **0.1 push**: `main` pushed to origin @ `71c25d2` (recovery anchor). Tree clean, health OK, `hooks_armed` green.
- **0.2 Slice-B freeze-readiness**: branch clean at held tip `c1647f1`; CLI flags parse
  (`test_cli_leg_e_target_parsing` + subcommand tests green); exactly 4 acceptance tests SKIP
  with "arc fixtures not captured — run … (Step 7)"; all 5 `test_gate_zero_*` unit tests green
  (module: 30 passed / 5 skipped; +16/1 in test_lived_sandbox.py).
- **0.3 resume dry-run**: from committed truth alone (BACKLOG #252 open "C4 gated on Step-7",
  Slice-B branch unmerged, no 2026-07-05 audit artifacts) the first incomplete block resolves
  coherently to Phase 0.4 → Block A. BOOT protocol validated.
- **0.4 spawn-auth**: **GO.** Key absent in tool-shell env / User / Machine scopes; the
  Slice-A auth path ("a shell whose profile loaded the key" — spawn.py's own documented
  contract) verified live: fresh profile-loaded pwsh carries the key (boolean-checked only,
  value never echoed). ONE minimal haiku smoke spawn through the harness:
  `exit=0 events=7 result_event=True response_ok=True secret_in_transcript=False`.
  Blocks A+B gated GO. No credential improvised, nothing read from `.secrets`, nothing
  written to disk.

## SELF-ADJUDICATION LOG (ARCHITECT-REVIEW-PENDING)

1. **SEQ-1 — Block A run before Phase 0.5** (sequencing fork). The brief orders Phase 0.5
   before Block A, but the `--consumer` seam must reuse observer/oracle/GATE-0 primitives
   that exist only on the unmerged `feat/lived-sandbox-slice-b`, and Phase 0.5 ends in its
   own `--no-ff` merge — building it off the Slice-B tip and merging would drag unclosed
   Slice-B commits onto `main` ahead of the Step-7 closure, violating Block A's
   "Slice B lands in one `--no-ff` at Step 7 [#252]" contract. Chose A-first (mechanical,
   auth-GO). Pure sequencing; no gate/semantic change; fully reversible.
2. **SEQ-2 — Phase 0.5 built on a branch off the Slice-B tip; its `--no-ff` merge to main
   DEFERRED to the architect.** After Block A degraded (below), Slice-B stays unmerged, so
   `feat/consumer-arc` must base on `c1647f1` to reach the primitives; merging it tonight
   would land Slice-B code outside its Step-7 contract. Conservative option: build + test +
   Codex-gate + push the branch; hold the merge. Block B's measurement runs from the branch
   checkout (the CLI runs from the working tree; the deliverable is measurement, not merged
   code).

## BLOCK A — Slice-B closure [#252] — **DEGRADED (per the frozen contract)**

**Step 1 (green freeze) ran live** (`observe-arc --freeze --haiku`, profile-loaded shell,
first-ever live six-hook arc). **GATE-0 FAILED → contract-mandated STOP + DEGRADE** ("the §A
seam is architect-owned; do not debug isolation autonomously"). Verbatim CLI verdict:

```
GATE-0 FAILED - STOP: isolation unproven under real work; the observer is not trusted (do not freeze a facade).
GATE-0 isolation FAILED: provenance=True outer-absent=False exit-ok=True
observer FLAGGED: 7 gated (2 ok), flags: hub-toc-hooks:EXPECTED-BUT-SILENT, floor-hash-verify-hook:EXPECTED-BUT-SILENT, floor-sessionstart-guard:EXPECTED-BUT-SILENT, session-end-backpressure:EXPECTED-BUT-SILENT, canonical-freshness:EXPECTED-BUT-SILENT; commands observed: 0
CLI-EXIT: 1
```

**Evidence-grade diagnosis recorded for the architect (NOT debugged, NOT fixed tonight):**

- `provenance=True` + `exit-ok=True` — harness, auth, and isolated-config seam all worked.
- `outer-absent=False` is a **negative-control confound, deterministic, not flaky**: GATE-0's
  `OUTER_MARKERS = ("[fleet]", "[changelog]", "[closures]")` assume those strings only come
  from the outer `~/.claude` L0 surfacing — but the arc clones **the hub itself**, and the
  hub's own project-level `.claude/settings.json` SessionStart hooks (`fleet_health.py` →
  `[fleet]`, `changelog_sentinel.py` → `[changelog]`) ride into the clone and legitimately
  emit those markers inside the child transcript. (In the clone the digest's once/day state
  file is gitignored-absent, so it fires fresh.) A retry cannot pass; API cost not re-burned.
- Secondary observation (C3 territory, architect's queue): 5/6 gated hooks SILENT and
  **0 command acts observed** — the haiku child appears not to have executed the arc steps
  at all. Distinct question from the marker confound.
- Post-failure state verified clean: no fixture frozen (CLI refused the facade), working
  tree untouched, **zero temp leftovers** (`lived-sandbox-*` teardown held on the failure
  path). Slice-A fixtures untouched.

**Consequence:** C4 closure + #252 ship do NOT happen tonight. Steps 2–7 not attempted
(contract: degrade the whole block). `feat/lived-sandbox-slice-b` stays held at `c1647f1`.
Block B remains GO (gated on auth + Phase 0.5, not on Block A); the marker confound is
hub-clone-specific — an ai-council consumer clone carries no hub fleet-surfacing hooks.

---

## PHASE 0.5 — `--consumer` seam — **COMPLETE** (built under SEQ-2; merge deferred)

Built `observe-arc --consumer <repo-path>` on `feat/consumer-arc` (base: the architect-held
Slice-B tip `c1647f1`, per SEQ-2 — merging tonight would land Slice-B outside its Step-7
contract, so the branch is **pushed, not merged**). Frozen rulings applied verbatim: hub
manifest = oracle; consumer firing = reality; per-component FIRED / EXPECTED-BUT-SILENT /
tombstone verdicts + n-of-6 coverage; FAIL-by-coverage = correct verdict (exit 2); observe
as-is (no shaping, `--freeze`/`--leg-e` refused); clone-only, real repo never mutated;
verbatim secret-masked evidence quotes. 15 hermetic tests incl. the mandated
partial-coverage-consumer case; **full suite 1266 passed / 6 skipped**; ruff clean.
**CODEX GATE:** `docs/audits/2026-07-05-codex-consumer-arc.md` — 0 CRIT / **1 HIGH**
(SandboxError/OracleError escaping the CLI as tracebacks) / 0 MED / 0 LOW; the HIGH fixed
pre-push with 2 tests. Commits `49d46d6` (seam) + `1655789` (Codex fix + audit), branch
pushed to origin.

## BLOCK B — first ai-council consumer measurement — **DELIVERED (measurement), with four architect findings**

**Run 1** (as-is clone, sonnet child) + **verbatim RETRY** (n=2) + **Run 2** (fresh clone
after the CLAUDE.md fix). All three: **GATE-0 isolation PROVEN** (provenance=True,
outer-absent=True, exit-ok=True — the Block-A marker confound is confirmed
hub-clone-specific) and **COVERAGE 1-of-6, FAIL-by-coverage, exit 2** (the contract-correct
verdict). Honest bottom line: **no in-the-wild deployed-gate fire was witnessed** — the
child never reached the arc's commit step, so the pre-commit gates (incl. the predicted
`canonical_freshness` FAIL on the A2-stale CLAUDE.md) were never exercised.

Findings for the architect (recorded, deliberately NOT fixed tonight — observer/arc are
Slice-B territory):

1. **ARC_PROMPT permission/refusal wall (blocks the whole measurement class):** run-1 ×2 the
   child refused the arc as suspected prompt-injection ("suspicious pre-message hook text and
   a nonexistent `/review-closures` command … I won't reply 'ARC DONE' as if everything
   completed"); run-2 it accepted the task but **stalled asking approval for `git checkout`**
   (headless `-p` default permissions; nobody can approve). Same wall likely explains
   Block A's "5/6 SILENT + 0 commands". Needs a permission-mode/allowlist design ruling —
   a safety-posture change not self-adjudicated at night.
2. **Observer C1 leak:** the `result`-type event's `result` field (the child's final
   narration) enters `hook_stdout_surface` — the lone FIRED (`propose-closures-stop-hook`)
   matched **narration**, not a hook. Firing-verified coverage is therefore ~0-of-6.
3. **`closure` expect-signature too broad:** run-1-retry it also matched a listed *filename*
   (`2026-05-09-…-governance-closure.md`). Calibration (Step-7 class) must use longer stable
   substrings.
4. **Run-2 behavioral delta from the CLAUDE.md fix:** after §7 gained the plugin commands,
   the child no longer flagged `/review-closures` as nonexistent/suspicious — doc currency
   measurably changed child behavior (n=1, noted, not claimed proven).

**Step 2 (genuine re-review, real ai-council):** CLAUDE.md read end-to-end + verified against
live state; real staleness fixed (§9 still claimed the ruff pre-commit gate that `31e785d`
pruned in the v1.2.0 deploy; §7 lacked the plugin's `/review-closures`/`/ship`); honest
`last_reviewed` 2026-06-02 → 2026-07-05; v2.4 history entry. Merged `--no-ff` in ai-council:
**`75006db`** (leaf `5643895`). Its A2 FAIL is cleared (freshness gate now exit 0; the two
33-day VISION/CONTRIBUTING WARNs remain, out of tonight's scope).

**Incident found + repaired in ai-council (configured-not-armed, live):** the re-review
commit ran through **zero hooks** — `core.hooksPath` pointed at the repo's pre-move relic
path (`C:\Users\1028120\Documents\Scripts\ai-council\.git\hooks`, empty), so every git hook
was silently bypassed AND the SessionStart `pre_commit install` had been refusing (exact hub
RF-2 precedent, operator-fixed there 07-04). Repaired: `core.hooksPath` unset (old value
recorded here — reversible one-liner), `pre-commit install` now armed, `canonical_freshness`
re-run **Passed through the armed hook path**; floor gate exit 0 on HEAD.
**ARCHITECT-REVIEW-PENDING: AC-1** (the hooksPath unset — sanctioned-shaped but a consumer
config change) and **AC-2** (ai-council left UNPUSHED: main there is now ahead 5, incl. the
operator's own 3 pre-existing commits — publishing them wasn't clearly sanctioned).

Follow-ups filed as **[#253]** (BACKLOG, mesh epic). Delta Run 1 → Run 2: coverage unchanged;
failure mode changed (refusal → permission stall); freshness-gate delta invisible in-arc
(commit never reached) but proven directly on HEAD.

---

*(Appended at subsequent block boundaries.)*
