# Close-out diff review — lane b2w3-verdict-base (Copilot route, gpt-6.1-sol)

- **Class:** verification (ADR-101 enum) · **Date:** 2026-10-10 · **Slug:** b2w3-verdict-base-review
- **Contract:** `LANE-1480-b2w3-verdict-base` (`$CLAUDE_PROMPTS_DIR/LANE-1480-b2w3-verdict-base.md`, Done-contract item 7) · batch B2-W3 · lane 1 · seat Tech-Architect-44
- **Consumers:** [#1480]
- **Branch:** `worktree-b2w3-verdict-base`
- **Diff range:** `b78c08b6..e9c40eaa` over `scripts/` and `tests/` (six files; the generated `ecosystem/doc-counts.md` is not code and was not sent)
- **HEAD at first review:** `1c38d08e363f7c03b8e4ab62dc4d59487c8b787f` · **fix tip at second review:** `e9c40eaae8c9d13620a81f67b9386458fbb9d754`
- **Tally:** 0/1/2/1 (first review, against `1c38d08e`) → 0/0/2/2 (second review, against `e9c40eaa`) <!-- Critical/High/Medium/Low -->
- **Verdict:** FAIL at `1c38d08e` (one HIGH) → **PASS at `e9c40eaa`** (no CRITICAL, no HIGH). The HIGH was fixed in `e9c40eaa`; the four remaining items are recorded below with their dispositions.
- **Posture:** the reviewer was given a folder of files (diff, contract, ruling, source and tests at the tip), not the repository. It could hash and read them; it could not run the suite. Statements of the form "demonstrated in memory" are the reviewer's own and were not re-run by the lane.

This record is owed an index line: `docs/audits/README.md` is generated and the lane leaves it alone; the integrator regenerates it on the merged result (`gen_audit_index.py --write`, after `git add`).

---

## 1. Route (S-38 (b), common rules §2 (e))

Codex `gpt-6-astra` through `deploy/codex-review.ps1` first; the Copilot CLI `gpt-6.1-sol` second; never the producer's vendor (every lane is Anthropic) and never the implementing session.

**Codex was attempted and refused.** Started 18:50:56 local (UTC+2) on 2026-10-10 as `deploy/codex-review.ps1 -Topic b2w3-verdict-base -DiffRange b78c08b6..HEAD -Consumer '[#1480]' -Force`. The tool's own log:

```
OpenAI Codex v0.155.0
model: gpt-6-astra
provider: openai
session id: 01a126b9-e326-7771-ae30-4d945cfdf5d5
ERROR: You've hit your usage limit. ... or try again at 9:40 PM.
```

The line appears twice (one retry); no review was produced, `codex exec` exited non-zero and the script wrote no `docs/audits/*-codex-b2w3-verdict-base.md`. Nothing was substituted for it other than the Copilot route below. Grok was not used.

## 2. Review 1 — `gpt-6.1-sol` against `1c38d08e` (verdict FAIL)

- **Run:** 18:59:15 → 19:02:28 local. `copilot -p <prompt> --model gpt-6.1-sol --add-dir <folder> --allow-all-tools --no-ask-user -s --no-color --usage-output-file <json>`, working directory the input folder (not the repository), exit 0, stderr empty.
- **Served model, from the tool's own usage file:** `currentModel: "gpt-6.1-sol"`, `modelMetrics` key `gpt-6.1-sol`, 10 requests / 1 premium request. Usage file sha256 prefix `d0da3f674dd9`; reply sha256 prefix `7f618124e9a4`. The reply itself states `gpt-6.1-sol`.
- **Nonce returned:** `NONCE-1480-closeout-4e82a9` — equals `nonce.txt` in the folder.
- **Proof of reading:** the reviewer printed the sha256 first-12 of all sixteen input files (the whole diff `c69c4b5aab8b`, the contract `8527c7658805`, the resume ruling `e6f90b435a28`, `src-actions_verdict.py` `bd9a69d5bf86`, `src-ci_verdict.py` `63b513d3bb5a`, `src-known_reds.py` `bbde964fdbcb`, `tests-test_actions_verdict.py` `940b7bc4e3d9`, `tests-test_ci_verdict.py` `4a7b4edbe7ec`, `tests-test_known_reds.py` `edea0e57ee31`, and the rest); every one equals the lane's own `Get-FileHash` of the same file.
- **Prompt:** attack, not confirm — the base relaxation as a launder path (the base registry also vouches registered-flaky swaps), every route to a verdict that skips the head read, any date typed or any caller-passable relaxation, the base read's fail-closed set, the quality of each new test, and edits outside the lane's files.
- **Findings, as returned:**
  - **CRITICAL** none.
  - **HIGH H1** — new tests type date-shaped literals (`tests/test_actions_verdict.py` fixture `baseline_id="2026-10-01-reg"` ×3 uses, a run `createdAt`/`updatedAt` pair; `tests/test_ci_verdict.py` a job-log timestamp). The contract bars any date typed into code or a test.
  - **MEDIUM M1** — the tripwire "only the base-side read calls the structural validator" checks the caller's file name only: moving the call into `head_registry_problems`, or importing the name under an alias, still passes it.
  - **MEDIUM M2** — the tripwire "no production caller injects a fetch function" scans call shapes and misses an aliased call and a `**` unpack.
  - **LOW L1** — the injection-policy tests pin the private helper `_resolve_head_check`.
  - **VERDICT** FAIL.
- **Targets 1–3 of the prompt** (the base relaxation as a launder path, a route that skips the head read, a relaxed expiry) produced no finding of their own: H1 is target 3's date question and M1/M2 are target 4's tripwires. The reply states no positive conclusion on targets 1–2; the lane does not read the silence as one — the `land`-level tests are its evidence there.

## 3. Fix — commit `e9c40eaa` (the HIGH, and both MEDIUM tripwires)

- **H1 fixed.** The fixture `baseline_id` is an opaque label (`fixture-registry-baseline`, deliberately not date-shaped); the run timestamps and the log timestamp are computed from the clock (`_stamp`, `_log_ts`); the three docstring/comment mentions of a calendar date no longer name one (they say "the S-15 incident" and "the first ordinary merge after the base's entries lapse"). A scan of every added line of the whole diff for `20dd-dd-dd` finds none.
- **M1 hardened.** `_mentions()` collects every mention of the name — the def, a bare name, an attribute, an import (aliased or not), the exact string a `getattr` would carry — with the enclosing function, and the test asserts the whole map: `{known_reds.py: [<definition>], actions_verdict.py: [_load_registry_at]}`. Mutation witness, run and reverted (source restored byte-identical, sha256 `BF3B22E9…AF2C` before and after):
  - the head reader's `registry_problems` call replaced by `registry_structural_problems` → FAILED, `{'actions_verdict.py': ['_load_registry_at', 'head_registry_problems']} != {'actions_verdict.py': ['_load_registry_at']}`;
  - an aliased `from known_reds import registry_structural_problems as _rsp` appended → FAILED, `{'actions_verdict.py': ['', '_load_registry_at']} != …`.
- **M2 replaced.** The AST scan became a behavioural test, `test_the_production_reader_hands_the_ci_verdict_no_injection_seam` (×2: with and without a pinned `run_id`): it runs `merge_path.read_verdict`, the one function `land` reads a verdict through, with `ci_verdict.verdict_for` replaced by a recorder, and asserts that none of the seven injection seams reaches it and that `baseline` does. An alias, a `**` unpack or a renamed variable cannot hide from a recorder.
- **Re-run after the fix:** `ruff check` clean; 497 passed (the three test files, `test_merge_receipt.py`, `test_gen_doc_counts.py`, `test_doc_counts_commit_tiering.py`, `test_validate_doc_claims.py` and the five no-push `tests/test_merge_path.py` tests) through `memory_admission_gate.py run -- … pytest -n 4`, run on the working tree at `1c38d08e` plus the uncommitted fix, which was then committed unchanged as `e9c40eaa`; the Done-3 differential against that run's junit file: 129 of 129 base verdicts present and unchanged, 368 tests only at the tip, all passed.

## 4. Review 2 — `gpt-6.1-sol` against the fix `e9c40eaa` (verdict PASS)

- **Run:** 19:17:54 → 19:20:39 local, same command shape, exit 0, stderr empty. Served model from the usage file: `currentModel: "gpt-6.1-sol"`, key `gpt-6.1-sol`, 10 requests / 1 premium request; usage file sha256 prefix `cf181c8da0fa`; reply sha256 prefix `e302de856ee5`.
- **Nonce returned:** `NONCE-1480-delta-9b61d3` — equals `nonce.txt`. The sha256 first-12 of all thirteen inputs were printed and every one equals the lane's own (the full diff `5188fc8f1d6c`, the delta `22e8a246319c`, the first review `7f618124e9a4`, `tests-test_known_reds.py` `cbf33a01d6ec`, `tests-test_actions_verdict.py` `e3e82a6504ce`, `tests-test_ci_verdict.py` `d4e5fa877668`, and the rest).
- **Prompt:** attack the fix — scan every added line for a typed date; find a way to reach the structural validator that the new tripwire would not report; check the recorder really intercepts what `read_verdict` calls; look for anything the fix broke.
- **Fix status, as returned:** H1 **FIXED** (all 936 added lines inspected, none carries a typed date or timestamp); M1 **PARTLY**; M2 **PARTLY**; L1 **NOT FIXED**.
- **Findings, as returned:** CRITICAL none; HIGH none; MEDIUM M1, M2 (residual); LOW L1, N1 (new). **VERDICT PASS.**

## 5. What remains, and why it is recorded rather than changed (R68: fix CRITICAL and HIGH, record the rest)

- **M1 residual — a bounded tripwire, not a reachability proof.** It does not see a computed-name lookup (`getattr(kr, "registry_" + "structural_problems")`, `importlib`), a call hidden in a nested function of the same name, or a second `scripts/**/actions_verdict.py` (the map is keyed by basename). The reviewer itself calls the string-splitting bypass "deliberate, not a likely accidental refactor". What actually keeps head expiry enforced is behaviour, not this scan: `head_registry_problems` is exercised on an expired, a last-valid-day and an unreadable registry (`tests/test_actions_verdict.py`, T2bf), and `land` on the production wiring refuses an expired head (T2b-a, T2b-green, T2b-ruff, T2b-cli). The tripwire's job is to make a new caller a conscious act, and it does.
- **M2 residual — a coverage hole, not an existing caller.** The recorder always omits `verdict_fn`, so a future caller passing `functools.partial(ci_verdict.verdict_for, log_fn=…)` through `read_verdict` or `land` would switch the head read off and this test would still pass. The reviewer states this "is not evidence that an existing production caller does so"; `merge_path`'s CLI paths use the default reader, and the `land`-level tests pin that the head read is ON on the production wiring.
- **L1 — recorded.** The resolver tests pin `_resolve_head_check` directly. They document the wiring rule (ON only when nothing is injected and a baseline is given; OFF when any of six seams is injected unless `head_check` is too); the observable consequence on the production path is pinned at the `land` level.
- **N1 (new, LOW) — a local-midnight window.** The boundary-day tests (`_iso(0)`, "the last valid day") create the fixture, run several git operations and then validate, each reading today's date separately; a run that crosses local midnight inside that window would see the entry as expired. Lane-added, not introduced by the fix; the window is the seconds around midnight. Not changed: the production path has no clock to pass — `head_registry_problems` takes none and calls `registry_problems(registry)`, whose `today` parameter is the pre-existing one and is not forwarded — and freezing it would need a patch of `known_reds`'s clock in every such test; a clock argument on the head reader is the kind of seam the contract forbids adding.

## 6. What this review does not cover

`ecosystem/doc-counts.md` (generated), `scripts/merge_path.py` and `tests/test_merge_path.py` (not in the diff; context only), `logs/KNOWN-REDS-REGISTRY.json` (no diff — Done 4). The reviewer did not run the suite; the suite runs are the lane's own and are pasted in the session file. The reviewer's claim that the structural-validator tripwire is a "bounded tripwire" is accepted as the honest description of §5's M1.
