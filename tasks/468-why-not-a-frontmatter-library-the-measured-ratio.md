---
id: "[#468]"
title: "Record why the tasks/intake frontmatter parser is hand-rolled — the measured rationale is redundancy, NOT fidelity"
status: closed
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#468] [P3][S] **Record why the tasks/intake frontmatter parser is hand-rolled — the measured rationale is redundancy, NOT fidelity** — grep confirms zero hits for `python-frontmatter`/`ruamel` in ADR-107/109, the `gen_*_tree.py` pair, `docs/audits/`, LESSONS or PLAYBOOK, so a load-bearing parser sits on no checkable justification. Measured on 20 real fixtures: `python-frontmatter` is 0/20 byte-identical with no config escape (PyYAML `sort_keys=True` reorders keys, quote style re-derived, trailing newline stripped) — disqualified. But `ruamel.yaml` IS 20/20 faithful at `width>401`, so the expected "libraries break byte-exactness" answer is TRUE of one library and FALSE of the other. The honest rationale is redundancy: `gen_task_tree.py` TEMPLATES frontmatter fresh from the body instead of round-tripping, so no library is on the critical path. · Done when: the rationale is placed at one home (script docstring or LESSONS entry) naming BOTH measured results, not the false generalisation · refs docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md, scripts/gen_task_tree.py · kill-candidates: none — no open row owns parser rationale · serialize-group: architecture
