# Codex Review — g7-mirror

**Date:** 2026-07-06
**Branch:** `main`
**HEAD:** `ff184e4`
**Diff range:** `80fbaa9^1..80fbaa9`
**Codex version:** codex-cli 0.141.0
**Mode:** diff-review

---

## Focus

- G7 mirror (deploy/lived_sandbox/consumer.py mirror_relative_precommit_sources): materializes a consumer's relative-path pre-commit sources beside the sandbox clone. Attack: path traversal / temp-root escape (the guard uses resolve() + parents check -- bypassable on Windows? junctions, drive-relative paths, UNC?), yaml parse edge cases, clone of an attacker-shaped repo path, notes/quoting.
- Teardown coverage: the mirrored clone lands in temp_root and must be removed by the existing guarded teardown -- any leak path?
- Faithfulness: mirror runs unconditionally pre-spawn for ANY relative repo entry -- facade risk vs measuring reality?

---

## Findings
## [CRITICAL]

(none)

## [HIGH] deploy/lived_sandbox/consumer.py:62 — non-mapping YAML can crash the harness

**What:** `yaml.safe_load()` can return a list/string/scalar, but the code unconditionally calls `data.get(...)`.
**Why:** A syntactically valid but malformed `.pre-commit-config.yaml` can raise `AttributeError` before the sandbox spawn, replacing an honest measurement failure with a harness crash.
**Fix direction:** Validate `data` is a mapping, and validate `repos` shape before iterating; otherwise return a note or no-op safely.

## [HIGH] deploy/lived_sandbox/consumer.py:235 — mirror diagnostics are discarded

**What:** `mirror_relative_precommit_sources(...)` returns skip/clone-failure notes, but `run_consumer_arc()` ignores them.
**Why:** Missing sibling repos, temp-root escape skips, or clone failures become indistinguishable from ordinary hook silence, degrading the measurement report and hiding the consumer-environment cause.
**Fix direction:** Carry mirror notes into `ConsumerReport.report_lines()` or an equivalent surfaced diagnostic, with a test through `run_consumer_arc()`.

## [MEDIUM]

(none)

## [LOW]

(none)
