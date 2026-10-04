# Codex Review — b2-codespace-1to1

**Date:** 2026-10-04
**Branch:** `worktree-b2-codespace-1to1`
**HEAD:** `4cd8f4ff`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 3/0/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469]) — served model id read from the run header: `gpt-5.6-terra`; proof-of-read nonce returned: `REV-87AC5C9E` (matches the Focus)
**Review profile:** code
**Consumer:** [#1335] LANE-B2-W1-b2-codespace-1to1 (batch B2-W1, lane W1-7)

---

## Focus

Contract: LANE-B2-W1-b2-codespace-1to1 (batch B2-W1, lane W1-7; R63, R61, R59, ADR-126 D2). Check, in this order:
(1) scripts/codespace_parity.py -- the C1 served-model-id probes: is the served id really read from each CLI's OWN record (claude stream message.model, codex run header, grok usage.json primaryModelId, agy run-log label) and never from the model's words? Can a CLI that answered with another model, or with no id, still print PASS? Are secrets or model output ever written to the record? Any path where an absent or unauthenticated CLI is silently passed instead of named?
(2) .devcontainer/provision.sh and provisioning.yaml -- the grok leg, the agy pin it cannot select, fetch_installer. Does any leg type a version, carry a credential, or pipe an unchecked download into a shell?
(3) scripts/dispatch.py -- only the Codespace default lines (machine standardLinux32gb, idle timeout 240m) may differ.
Flag P1 for anything that would make a parity check pass while a model CLI serves a different model than the registry routes it to, or that leaks a credential.
PROOF OF READ: end your answer with one final line exactly: REVIEW-NONCE: REV-87AC5C9E

---

## Findings
## Critical

**P1 — scripts/codespace_parity.py:473**

**What:** Codex’s served ID is parsed from combined stdout and stderr; model output on stdout can supply a forged `model: <expected-id>` line before the real run header.
**Why:** A Codex CLI actually serving a different model can pass C1.
**Fix direction:** Parse the run-header field only from stderr and restrict it to the header section.

**P1 — scripts/codespace_parity.py:523**

**What:** The probe record stores the first 80 characters of CLI stderr on a 124/127 result.
**Why:** CLI stderr is untrusted and may include credentials or model output, violating the record’s no-secret/no-output contract.
**Fix direction:** Store only a fixed error category/exit code; add an adversarial secret-bearing stderr test.

**Critical — .devcontainer/provision.sh:767**

**What:** The Claude pin leg still pipes a downloaded installer directly into `bash`.
**Why:** A malformed or compromised response executes immediately, bypassing the new installer validation path.
**Fix direction:** Fetch and validate the installer before execution, consistently with the other vendor-installer legs.

## High

(none)

## Medium

(none)

## Low

(none)

REVIEW-NONCE: REV-87AC5C9E


---

## Amendment 2026-10-04 — the three findings fixed (RED-first)

Verdict: all three confirmed real, all fixed; none disputed.

- **P1 codespace_parity.py:473 (forged id on stdout)** — RED `e6991460`, fix `6a723c54`. `read_codex(stderr, stdout, nonce)` now takes the id only from the header block between the first two rules of stderr; stdout is searched only for the nonce. Witnesses: forged-stdout test, echoed-`model:`-after-header test, headerless-stderr test.
- **P1 codespace_parity.py:523 (stderr in the record)** — same commits. A 124/127 result records a fixed category (`timed out` / `could not start`) with the exit code, never CLI text. Witnesses: secret-bearing stderr at rc 124 and 127, and a sweep that no detail carries printed text.
- **Critical provision.sh:767 (claude pin piped into bash)** — same commits. `leg_f5_claude_pin` fetches via `fetch_installer` (shebang-checked file) and runs `bash "${installer}" "${want}"`; the fetch-installer test now covers agy, grok and claude.

Evidence at `6a723c54`: `tests/test_codespace_parity.py` + `tests/test_provision_sh.py` — 191 passed; `ruff check` clean on the touched files.
