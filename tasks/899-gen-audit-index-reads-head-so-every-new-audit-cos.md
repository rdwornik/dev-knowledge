---
id: "[#899]"
title: "gen_audit_index reads HEAD, not the working tree -- every new audit costs a second, index-only commit and --check is falsely green before it"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#899] [P3][S] **gen_audit_index reads HEAD, not the working tree -- every new audit costs a second, index-only commit and --check is falsely green before it** - `scripts/gen_audit_index.py` enumerates committed files. An uncommitted new `docs/audits/*.md` is invisible to it, which plays out in five steps. (1) `--write` prints `wrote docs/audits/README.md` and produces no diff. (2) `--check` returns rc=0, a false green comparing HEAD to HEAD. (3) The local `audits-index-freshness` pre-commit hook SKIPS ("no files to check"), because the index was not staged. (4) After the commit, `--check` goes red. (5) A second, index-only commit follows. Witnessed at batch AC's freeze (`01ecb63b`, then the forced `7f15218b`) and again in this window's own audit commit. Every lane that writes an audit pays it, and a batch lane is barred from regenerating the index at all, so the second commit lands on the integrator · Done when: the generator reads the working tree (or the index), so writing an audit and regenerating the index is ONE commit. `--check` fails, not passes, when a working-tree audit is missing from the index. RED-first witness: an uncommitted new audit makes `--check` exit non-zero and `--write` produce its row · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W8, `scripts/gen_audit_index.py`, `.pre-commit-config.yaml` (`audit-index-freshness`), `to-browser/HANDBACK-batch-AC-consolidated.md` (L-freeze item 7) · kill-candidates: none -- no open row names the HEAD read
