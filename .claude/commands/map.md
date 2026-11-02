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

## `/map view` -- the system view (ADR-133)

```
uv run --locked python scripts/system_map.py view [--leg fast|full|scheduled] [--out-dir DIR]
```

Renders `view.json` and `view.html` from organ outputs alone (no hand-written prose): every tile
shows value, source, checkout and state. Both outputs are gitignored (`ecosystem/view.json`,
`ecosystem/view.html`). Report the `json:`, `html:` and `leg:` lines it prints.

- `--leg fast` (default): reads the receipts, merge receipts, ledger and the other sources; never
  runs the map build. Seconds.
- `--leg full`: runs the map build first (as `build` above, writing the tracked record), then the
  view. This is the leg wired into the harness `batch-close` moment (optional, continue_on_failure).
- `--leg scheduled`: the scheduled invocation (`uv run --locked python scripts/system_map.py view --leg scheduled`). Reads ONLY `ecosystem/system-map-record.json` and
  `logs/MERGE-RECEIPTS.jsonl`; every other tile reads NOT COMPUTED.
- Served mode: `python -m http.server` in the output directory, then open `view.html`; the page
  re-reads `view.json` on an interval and loads the pinned Mermaid build (SRI) over http only.
  Opened as a file it shows the embedded snapshot and the diagram source text.
- Receipts of sibling worktrees are read read-only; each tile names its checkout.
