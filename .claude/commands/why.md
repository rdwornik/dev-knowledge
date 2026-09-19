---
name: why
description: Explain what a repo file is for and what reads it -- purpose, consumers and edges from the file-purpose graph; use before editing or deleting an unfamiliar file.
---

# /why — what is this file for, and what depends on it

Argument: `<path>` (repo-relative). Run:

```
uv run --locked python scripts/file_purpose_graph.py why <path>
```

- Add `--depth 2` for transitive consumers, `--limit 0` for every row.
- A refusal (exit 1, `nothing explains this file`) is the answer: no governed input names
  the file. Say so; do not invent a purpose.
- Every file at once: `uv run --locked python scripts/file_purpose_graph.py list` (tab-separated
  path, purpose, edges, consumers).
