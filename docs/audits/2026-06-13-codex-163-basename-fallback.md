# Codex Review — 163-basename-fallback

**Date:** 2026-06-13
**Branch:** `integ/156-163`
**HEAD:** `9c257c5`
**Diff range:** `92a5e37^..92a5e37`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- This HARDENS just-shipped #163 teeth-validator code (verify_handoff_probes.py). Teeth-semantics change: a probe source-locator naming a real repo file by BARE basename (e.g. HANDOFF_PROCESS.md for protocols/HANDOFF_PROCESS.md) previously FAILed; now resolves via a unique non-excluded basename fallback.
- Confirm the fallback PRESERVES teeth: a genuinely missing file (0 matches) still FAILs; an ambiguous basename (>1 non-excluded match) still FAILs (must NOT silently pick one).
- Check the exclusion scoping (.git/.claude/node_modules/aborted/in-progress + archive* prefix) is correct and cannot let an archived/worktree duplicate either (a) create false-ambiguity or (b) mask a real miss.
- Any path-traversal / rglob performance / symlink concerns. Read-only contract (Layer-2) must hold: no writes, no subprocess.

---

## Findings
## CRITICAL
(none)

## HIGH
## HIGH scripts/verify_handoff_probes.py:203 — direct path resolution bypasses repo/exclusion scope

**What:** `_resolve_path` accepts `repo_root / rel` whenever it exists, without normalizing inside `repo_root`, requiring a file, or applying the excluded-dir/archive rules; `file_tokens()` can also match `../outside.md`.
**Why:** A probe can pass by naming an outside-repo file, symlink target, archived duplicate, or `.claude/worktrees` duplicate directly, which can mask a real live-source miss and weaken the validator’s teeth.
**Fix direction:** Resolve direct candidates before accepting them, require containment under `repo_root`, reject excluded/archive path parts, and require `is_file()`.

## MEDIUM
## MEDIUM scripts/verify_handoff_probes.py:208 — fallback scan does not prune excluded trees

**What:** `repo_root.rglob(name)` walks the whole repo before filtering out `.git`, `.claude`, `node_modules`, archived, aborted, and in-progress paths.
**Why:** The excluded worktree/vendor directories can still dominate runtime during pre-commit or ship-gate validation, especially when fallback runs for bare or missing basenames.
**Fix direction:** Use a pruned traversal or build a basename index once per `verify()` that skips excluded directories before descent.

## LOW
(none)

I did not run tests, since this was a read-only review and pytest can create cache state.
