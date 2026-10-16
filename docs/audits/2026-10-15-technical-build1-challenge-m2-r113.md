# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-M2-R113-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-M2-R113-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 8732e5e52e54b943. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: CHALLENGE matrix M2 - R113 / AMEND L2: how agy reads headless. Verdict AMEND (reuse read_gate, which already passes the bypass; declare the workspace) plus one INPUT_REQUIRED (the "worktree or job tmp only" mitigation is not enforceable).

# M2 - R113: agy as the headless bulk reader

## Question
R113 sanctions `agy` headless with its permission bypass so it reads again (VERIFIED-MAP V10/V11 failed). Is that the best existing way, and do its mitigations hold?

## Measured today (local, agy 1.3.5)
- `agy --help`: the bypass flag is `--dangerously-skip-permissions`; there is no `--yolo` / `--approval-mode`; `--add-dir`, `--mode plan`, `--sandbox` exist.
- In-cwd nonce file: plain 17 s, `--mode plan` 41 s, bypass 13 s - all quoted the nonce.
- Out-of-workspace file (`H:/My Drive/.../LEDGER-dev-knowledge.md` line 3): plain = "a tool required the read_file permission that headless mode cannot prompt for, so it was auto-denied"; `--add-dir <dir>` 14 s quoted; bypass 14 s quoted. So V10/V11 was an out-of-workspace read with no bypass and no `--add-dir`.

## Prior art (repo)
- `scripts/read_gate.py:375-381` - the agy read adapter ALREADY passes `--dangerously-skip-permissions`; `verify_read` (:171-195) rejects any quote that is not a literal substring of the source (R59 in code).
- `ecosystem/provider-registry.yaml:776-804` - `read` is ALREADY ordered agy -> copilot-enterprise -> claude-sonnet-5 (agy and Copilot `unevaluated`).
- `docs/audits/2026-09-01-technical-agy-admission-verdict.md:266-274` - agy read outside its workspace on 3 of 10 items; `docs/audits/2026-09-05-technical-627-readjudication.md:280-300` - with the bypass agy WROTE files into `~/.gemini/antigravity-cli/scratch/repo`; :498-509 - `--add-dir .` did not confine it either; :658-664 - rule: every invocation declares its workspace (absolute path or `--add-dir`).

Weights: unattended=20 code=15 libfirst=15 modelagnostic=15 osagnostic=10 tokens=10 testable=10 simplicity=5
| Option | unattended | code | libfirst | modelagnostic | osagnostic | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A. new bypass route as ruled | 4[^1] | 3 | 3 | 3 | 3 | 3 | 4[^2] | 2 | 3.25 |
| B. reuse read_gate (bypass already) + declared workspace | 4[^1] | 4[^3] | 4[^3] | 3 | 3 | 3 | 4[^2] | 4[^3] | 3.65 |
| C. new --add-dir route, no bypass | 4[^4] | 3 | 3 | 3 | 3 | 3 | 4[^2] | 3 | 3.30 |
| D. Copilot only | 4[^5] | 3 | 3 | 3 | 3 | 2 | 4[^2] | 4[^6] | 3.25 |

[^1]: measured -- local probe 2026-10-15, bypass read of an H:/ file quoted line 3 in 14 s
[^2]: measured -- scripts/read_gate.py:171-195 verify_read, read 2026-10-15
[^3]: measured -- scripts/read_gate.py:375-381 already builds the bypass argv; no new code
[^4]: measured -- local probe 2026-10-15, --add-dir read of an H:/ file quoted line 3 in 14 s
[^5]: measured -- DIGEST-VERIFIED-HARNESS-MAP-2026-10-15.md:9, Copilot substituted for agy with line-quoted proof
[^6]: measured -- provider-registry.yaml:776-804, Copilot is already the second read entry

## Pre-mortem
- B fails if `read_gate`'s argv is not the path lanes actually use for reads (an ad-hoc `agy -p` in a seat bypasses it - that is exactly how V10/V11 failed). The fix is a rule plus a probe, not a new route.
- Confinement: no flag tested confines agy (bypass writes scratch outside the tree; `--add-dir` wanders). `--sandbox` ("terminal restrictions") is unprobed.

## Verdict
- **AMEND (R113, AMEND L2):** no new route. Lanes read through `read_gate.run_read_gate` (bypass already in argv), every prompt names an absolute path and passes `--add-dir <bundle dir>` (627 rule 2). L2's Done-when adds: an ad-hoc `agy -p` without `--add-dir`/absolute path is refused by a test of the documented read entry point.
- **INPUT_REQUIRED (R113 mitigation "lane worktree or job tmp only"):** not enforceable by any agy flag measured (readjudication :280-300, :498-509). Operator: accept agy's own scratch writes outside the tree under the R113 consent, or require `--sandbox` (to be probed) before agy is the default reader. Until answered, read stays agy -> Copilot with R59 verification, as the registry already says.
