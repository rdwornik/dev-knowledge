---
id: "[#513]"
title: "Propagation completeness — a ruled adoption that landed at some sites and not others."
status: open
priority: P2
size: M
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
generates: BACKLOG.md
---

- [#513] [P2][M] **Propagation completeness — a ruled adoption that landed at some sites and not others.** ONE defect class at n=3, not three rows: the `markdown_it` fence ADOPT reached 2 of 4 fence sites (`audit.py` `_strip_code_regions` anchors at column 0, so legal indented fences leak into the `@import` scan `check_import_edges` gates on; `validate_doc_structure.py` is blind to `~~~`); the `yaml.safe_load` ADOPT reached 1 of 2 frontmatter readers (`gen_claude_rosters.py` still regex-parses with a key class that cannot match an underscore-bearing key in a generator feeding two `@`-imported CLAUDE.md fragments read at every boot); and the terra git-tracked-corpus ruling never reached `tests/test_toc.py` or `tests/test_normalize_headers.py`. Three rulings, one shape: nothing owns propagating an adoption to all sites. **The landing predicate is the DETECTOR, not the fixes** — fixing sites alone leaves the class live. Done when: a detector reports any ruled adoption present at some sites and absent at others, AND the three instances are conformant or exempted with a reason · refs N5-03/N5-05/N3-04, C-5, ADR-111 · kill-candidates: none — [#357] is the census, not the propagation
