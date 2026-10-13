---
name: map
description: Regenerate the system map (one JSON and one static HTML page, no LLM) from the file-purpose graph, grimp, the organ index and the harness, and print the paths and the map sha.
---

# /map — regenerate the system map

No arguments. Run from the repo root:

```
uv run --locked python scripts/system_map.py build
```

Report the lines it prints, verbatim: `json:` and `html:` (the two outputs), `map_sha:`
(sha256 of the JSON), `previous_sha:`, `diff:` (added / removed nodes) and `record:`.

- The JSON and HTML land in `ecosystem/system-map.json` and `ecosystem/system-map.html`.
  Both are gitignored: they regenerate on demand and are never committed.
- `ecosystem/system-map-record.json` IS committed: the map sha, the previous sha and the
  added / removed node diff. When `record:` says `updated`, commit that file; when it says
  `unchanged`, the map did not move and there is nothing to commit.
- DEAD organs (nothing fires them) and UNEXPLAINED files (the file-purpose graph cannot
  explain them) are listed in their own sections of the page. Say how many of each there are;
  do not explain them away.
- The build reads the whole repo and takes about half a minute.
