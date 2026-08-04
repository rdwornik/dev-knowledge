# Codex Review — 483-terra-round2

**Date:** 2026-08-04
**Branch:** `feat/preflight-contract`
**HEAD:** `abf7c12a`
**Diff range:** `main..feat/preflight-contract`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Round 2. Round 1 raised 3 HIGH (windows-absolute locators skipped; bare-name fallback could verify the wrong file; git operational failure conflated with a stale SHA), all fixed in abf7c12a.
- Verify the FIXES. Is the widened _FILE_LINE_RE now too permissive - can it extract things that are not locators (it now allows spaces and a drive colon)? Any catastrophic-backtracking risk?
- _resolve ambiguity guard: correct? Can a qualified path still be mis-resolved, or an unambiguous bare name wrongly rejected?
- git health probe: is exit 2 now reached on EVERY operational-failure path, and is a genuinely-missing SHA still exit 1? Any path where verify() returns a clean report while git was unusable?
- Are there remaining silent-skip paths anywhere in extraction - a locator shape a contract would plausibly use that is neither extracted nor reported as unsupported?
- Tests: any vacuous, tautological or self-constructing assertions? Is the chr(92) fixture sound?

---

## Findings
## Critical

(none)

## High

### [HIGH] scripts/preflight_contract.py:70 — widened locator regex treats prose as file locators

**What:** Backticked prose such as `` `see audit.py:1` `` matches as path `see audit.py`.  
**Why:** A valid contract can fail preflight on explanatory inline code, making the verifier noisy and easy to ignore.  
**Fix direction:** Require a separator/root before allowing spaces; require a drive colon to be followed by `\` or `/`; add a backticked-prose negative test.

### [HIGH] scripts/preflight_contract.py:127 — resolver still mis-resolves some non-bare paths and root collisions

**What:** `direct` returns immediately for a root file, so `twin.py` is accepted even if `scripts/twin.py` also exists; a missing qualified path can also fall through into source-root searching.  
**Why:** Both cases can verify a citation against a file the contract did not name—the Round 1 failure mode.  
**Fix direction:** Only source-root-search a syntactically bare filename, include the repo root in that ambiguity set, and never fall back for qualified/absolute paths. Add root-collision and missing-qualified-path fixtures.

### [HIGH] scripts/preflight_contract.py:169 — unusable Git can still yield a clean report without a SHA claim

**What:** The failed health probe is only acted on inside the SHA loop; a file-only contract against an unusable Git repo can return a clean report.  
**Why:** This violates the stated fail-closed health posture and makes a failed operational probe silent.  
**Fix direction:** Either defer the probe until a SHA is extracted, or fail closed immediately when the probe fails; add a no-SHA unusable-repository test.

### [HIGH] scripts/preflight_contract.py:206 — SHA check neither proves reachability nor reliably separates Git failure from a missing SHA

**What:** `git cat-file -e` only proves an object exists, so dangling commits pass; after a successful `rev-parse --git-dir`, every later nonzero `cat-file` result is reported as “not reachable.”  
**Why:** Object-store/corruption/permission failures can become exit 1, and an unreachable commit can incorrectly pass despite the documented “reachable in history” contract.  
**Fix direction:** Use commands with explicit missing-vs-operational-error semantics, then verify reachability from the intended ref set; add fault-injected and dangling-object coverage.

## Medium

(none)

## Low

(none)

The regex has no apparent catastrophic-backtracking risk: it has no nested/unbounded competing quantifiers. The `chr(92)` fixture is sound, though asserting the exact extracted `file-line` raw value would make it stronger.