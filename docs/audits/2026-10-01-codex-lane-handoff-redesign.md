# Codex Review — lane-handoff-redesign

**Date:** 2026-10-01
**Branch:** `worktree-lane-handoff-redesign`
**HEAD at review time:** `15fcf29a`
**Diff range:** `origin/main...15fcf29a` (135,715 B)
**Codex version:** n/a — SUBSTITUTED under operator ruling (2) (see below)
**Mode:** diff-review, fresh isolated session (contract + diff only — not the lane, not agy)
**Tally:** P1=3 P2=1 P3=3
**Consumer:** `LANE-HANDOFF-REDESIGN-BUILD-lane-handoff-redesign.md` (item 17, "the Codex review");
`docs/decisions/ADR-129-handoff-cut-gated-by-handoff-relevant-checks.md`

**Model used:** `claude-sonnet-5` (SUBSTITUTE for the pinned `gpt-5.6-terra` — see Substitution note)
**Review profile:** code

---

## Substitution note

Codex terra was at its usage limit (reset "Oct 3rd, 2026 9:07 PM"), and the lane's own
recorded substitute, `agy` (Gemini), had 3 failures in-session
(`SESSION-lane-handoff-redesign.md` :523-538). The registry's remaining fallbacks do not
serve this lane either: `grok-4.6` is `requires_admission: true` and unevaluated, and
`claude-sonnet-5` is this lane's own producer, `excludes_producer: true`
(`ecosystem/provider-registry.yaml:724`).

Operator ruling (2), given to the integrator 2026-10-01 (quoted in full in
`to-browser/REFUSED-lane-handoff-redesign.md` §0): *"Independent review is mandatory (R45,
R47.5): run the registered fallback reviewer, claude-sonnet-5, in a fresh isolated session
that sees only the diff and the contract — not the lane, not agy; record it; refuse on any
open P1."* The ruling explicitly overrides the registry's `excludes_producer: true` for
this one review; isolation is by SESSION, not by model — the review session saw only
`diff.patch` (`git diff origin/main...15fcf29a`), `contract.md` and `contract-amend.md`, no
conversation history and no tool access beyond `Read`.

**Command:** `claude -p --model claude-sonnet-5 --tools Read --strict-mcp-config
--disable-slash-commands --no-session-persistence`, cwd holding only the three files above;
23:29:29 -> 23:35:35, exit 0. Full command/evidence block:
`to-browser/REVIEW-sonnet-lane-handoff-redesign-2026-10-01.md` (carrier of this record's
review body, landed here per repair 1's Done-contract, U5).

---

## Review: `lane-handoff-redesign` / ADR-129 diff

### P1 findings

**1. Two new tests perform live, unmocked `gh`/GitHub network calls — side effect outside the sanctioned surfaces (R15 "Do not")**
`tests/test_gen_handoff.py`, hunk `@@ -2172,3 +2181,104 @@`, functions `test_a_successful_real_cut_resets_the_refusal_count` and `test_receipt_carries_whole_repo_verdict_and_refusal_count` (≈ file lines 2239 and 2260).

Both call `gh.generate(..., transport=<tmp path>)` on a successful path, which makes `_write_receipt` take the `if transport is not None:` branch and call `_whole_repo_verdict(repo_root)` — unmocked:
```
+    monkeypatch.setattr(gh, "_handoff_organ_findings", lambda _root: [])
+    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [])
...
+               date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False,
+               transport=transport)
```
`_whole_repo_verdict` is not stubbed, so it runs `ci_verdict.find_run` / `fetch_jobs` / `fetch_job_log`, each shelling out to the real `gh` CLI against GitHub's live API (`scripts/gen_handoff.py`, `_whole_repo_verdict`, hunk `@@ -803,47 +1115,... @@`). This is a tool call outside the repository/worktree/job tmp/transport, exactly what the contract's "Do not" list forbids, and it makes the unit suite depend on network availability/`gh` auth, risking hangs up to the `GH_TIMEOUT_S` bound per call and flakiness on machines without `gh` configured.
**Fix:** monkeypatch `gh._whole_repo_verdict` (or `ci_verdict.find_run`) in both tests the same way `_handoff_organ_findings` is stubbed elsewhere.

**DISPOSITION (repair 1, U5): FIXED.** Both tests now `monkeypatch.setattr(_civ, "find_run", lambda *a, **k: None)` (import `ci_verdict as _civ`) before the real `generate()` call — the exact fix named above, via `find_run` (the `(or ci_verdict.find_run)` alternative) so `test_receipt_carries_whole_repo_verdict_and_refusal_count`'s own assertions on `verdict["source"]`/`verdict["verdict"]` keep exercising `_whole_repo_verdict`'s real "not run" shape rather than a fully stubbed return. No live `gh` call remains in either test.

**2. `check_review_artifact_coverage`'s batched rewrite silently drops entries missing from the new map, inverting the function's own stated principle**
`scripts/audit.py`, hunk `@@ -5116,18 +5135,14 @@` (≈ new line 5145):
```
+            # Looked up from the batched walk above, not a fresh `git diff` spawn (item 13/L8).
+            changed = merge_changed.get(sha, [])
             if not _review_is_code_impact(changed):
                 continue
```
`merge_changed` is built from one `git log --first-parent --diff-merges=first-parent --name-only ... main` call. If any `sha` from `_ja.spine_entries(root, "main")` is not a key in that map (traversal mismatch, truncation, or a future divergence between `spine_entries`'s notion of "main" and this literal `git log ... main` call), `changed` silently becomes `[]`, `_review_is_code_impact([])` returns `False`, and the entry is quietly skipped (not counted as `scanned`, never reported). This directly contradicts the adjacent, unchanged comment in the very same function a few lines above (`"Absent from the map is NOT treated as in-scope: ... an unknown must not silently become a WARN against a merge that may not deserve one"`) — the new code does exactly what that principle warns against, just for a different map. The old per-sha `git diff` call could never silently under-count this way. The live-repo "finding-identical" check the ADR cites is a one-time empirical check (contract-sanctioned per N4), not a standing guarantee, so this is a latent regression risk in an organ whose entire job is to catch missing review coverage.
**Fix:** raise/flag instead of defaulting to `[]` when `sha not in merge_changed` (or assert completeness once, e.g. `assert set(spine shas) <= merge_changed.keys()`), so an unmapped entry becomes a loud "unknown", not a silent pass.

**DISPOSITION (repair 1, U5): FIXED.** `sha not in merge_changed` is now checked explicitly before the `_review_is_code_impact` call; a miss is accumulated into a new `unmapped` list rather than silently defaulting to `[]`, and a non-empty `unmapped` list emits its own `warn` `Finding` (naming up to 5 shas, same truncation idiom as `unlinked`/`untallied`) rather than vanishing. `tests/test_review_artifact_coverage.py` (59 tests, including the finding-identical parity test) still passes unchanged.

**3. Contract item 16 (R38 input set) / render-note N11 additions are not touched or dispositioned in the diff**
Item 16 verbatim lists `protocols/HANDOFF_PROCESS.md`, `scripts/seat_refusals.py`, `docs/handoffs/README.md` among the files requiring an update or a recorded "reviewed-unchanged, reason" (contract.md:125; N11 at contract.md:64 specifically flags `protocols/HANDOFF_PROCESS.md:286` — "the ship-gate read-back probe" — and `scripts/seat_refusals.py:33` — "names the `preflight_rows` leg"). Both describe exactly the mechanism this ADR rewrites (row 1 going from a subprocess ship-gate read to an in-process organ-set run). The diff contains zero hunks for any of these three files — no edit, no comment, no disposition line. Meanwhile `scripts/decision_coverage.py`'s new `adr:129` entry (hunk `@@ -326,6 +326,26 @@`) asserts:
```
+        reason="Accepted and self-executing: ... No open implementing work "
+               "remains to file a row for.",
```
which is contradicted by the absence of any visible R38 disposition for files the contract's own render notes call out as likely stale. Since this review only has the diff (not the session file), this is flagged as the diff failing to demonstrate compliance with Done-contract item 0 and item 16 for these three named paths — at minimum `docs/handoffs/README.md`, which almost certainly documents the same preflight cost/behavior that `.claude/commands/handoff.md` (which *was* updated) describes.
**Fix:** update `docs/handoffs/README.md` to match the new row-1 behavior, and record the `protocols/HANDOFF_PROCESS.md:286` / `scripts/seat_refusals.py:33` disposition (edit or reviewed-unchanged-with-reason) per N11.

**DISPOSITION: DISCHARGED by the integrator pre-repair** (see this record's header "integrator dispositions" lineage — `to-browser/REVIEW-sonnet-lane-handoff-redesign-2026-10-01.md` line 7, P1-3): the lane's own R38 table (`SESSION-lane-handoff-redesign.md:178-180`) records all three paths reviewed-unchanged with reasons, and `grep -n 'preflight|ship.gate|minute|row 1' docs/handoffs/README.md` returned 0 hits at `9dda621c` — the integrator verified the claim rather than taking it on trust. Not reopened by this repair; operator ruling (3)'s repair scope is U1-U5 only.

### P2 findings

**1. `_whole_repo_verdict`'s up-to-three sequential `gh` round trips can add real wall-time to every CLI cut, undermining the "never blocks / cheap" intent**
`scripts/gen_handoff.py`, `_whole_repo_verdict` (hunk `@@ -803,47 +1115,... @@`): `find_run`, `fetch_jobs`, `fetch_job_log` are each capped independently at `ci_verdict.GH_TIMEOUT_S` (120s per the function's own docstring). In a degraded-network scenario a real cut via `main()` (which always passes the live `transport_root()`, hunk `@@ -3174,12 +3424,14 @@`) could add several minutes to receipt-writing after the fast preflight already passed. It never fails the row (per contract), but it works against the ADR's own "Performance" and "Usability" quality attributes (one quick attempt) and isn't bounded by the 120s figure the ADR advertises everywhere else.
**Fix:** apply a single overall timeout (e.g., `concurrent.futures` with one deadline) around the whole `_whole_repo_verdict` read, not per-sub-call only.

**DISPOSITION: NOT in operator ruling (3)'s repair scope (U1-U5) — carried, not fixed in this repair.**

### P3 findings

**1. Crude heuristic in the new membership test**
`tests/test_audit.py`, hunk `@@ -731,6 +779,35 @@`, `test_handoff_organ_set_is_finding_identical_serial_vs_parallel`'s sibling `test_handoff_organs_every_member_can_fail_except_doc_claims` (earlier hunk) determines "can fail" via `'"fail"' in src or "'fail'" in src` on `inspect.getsource(fn)` — a literal substring match that could false-pass (string appears in a comment/docstring) or false-fail (status built via a constant, not a literal). Low risk since it's a new safety net, not a weakened existing check, but worth tightening (e.g., check for `Finding(..., "fail", ...)` call shape, or a declared capability flag).

**2. `--preflight-only` and `--trial-cut` combined is unvalidated**
`scripts/gen_handoff.py`, hunk `@@ -3163,6 +3408,11 @@` / `@@ -3174,12 +3424,14 @@`: `if preflight_only or trial_cut:` silently prefers `trial_cut`'s row set/label if both flags are passed together, with no guard against the combination. Harmless in practice (nothing dispatches both), but untested and unvalidated.

**3. Item 14/L9's "hard-fails outside the set" receipt field is implicit, not explicit**
`scripts/gen_handoff.py`, `_write_receipt` (hunk `@@ -2915,7 +3109,... @@` / `@@ -2346,11 +2517,23 @@`): the receipt only stores `whole_repo_verdict` (raw CI tail text) and `refusal_count_since_previous_cut`. "Hard-fails outside the set" is never computed as its own field — it is only true by the invariant that `_write_receipt` is reached solely when row 1 (the 11-organ set) already passed, so any RED in the CI tail is *necessarily* outside the set. That's logically sound today but undocumented and untested as an explicit invariant, so a future refactor could silently break it.

**DISPOSITION: NOT in operator ruling (3)'s repair scope (U1-U5) — carried, not fixed in this repair.**

Tally: P1=3 P2=1 P3=3 — P1-1 FIXED, P1-2 FIXED, P1-3 DISCHARGED (pre-repair); P2-1, P3-1, P3-2, P3-3 carried (out of scope).
