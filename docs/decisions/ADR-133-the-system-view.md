# ADR-133: The system view is a pure rendering of what organs compute

- **Status:** Proposed
- **Date:** 2026-10-31
- **Decision tier:** Path A -- a `/decide` proposal for operator ratification (R13, ADR-108 section A).
- **Related:** ADR-106 (declared dependencies), ADR-121 (event log, Proposed), ADR-130 (the outer loop); row row 1748 (filed by e30-bootstrap, not yet in this tree) (stays open until the build); GO-E3.0 PR-3 (no hand-written prose).
- **Decommission:** none.
- **Source:** the design evidence docs/audits/2026-10-31-technical-design-view.md (matrix, pre-mortem, response table); the proposal is the operator's view, digest section C, 2026-10-31.

## Context

The operator wants one page that shows the system as organs compute it: the graph, the process, the runs and the state. The rule is no hand-written prose (PR-3). Today the repo has two stdlib HTML generators, scripts/system_map.py (graph, on demand, called only by the /map command) and scripts/gen_dashboard.py (a committed conformance page). No page shows runs or state. Receipts exist as files, per checkout, and ADR-121 (an event log) is only Proposed.

## Decision

- **D1 -- a new stdlib-only generator, a sibling of the map.** One new script renders `view.json` and `view.html` into the gitignored output directory beside the map outputs. No templating library, no Node toolchain, no change to uv.lock. The view lane does not edit scripts/system_map.py.
- **D2 -- data only.** `view.json` is assembled from organ outputs alone: the map JSON and tracked record, the P1 Mermaid, phase receipts, launch receipts, logs/MERGE-RECEIPTS.jsonl, the ledger and the conductor metrics. Every tile carries its source and a state: OK, STALE, ABSENT, UNREADABLE, or NOT COMPUTED with a reason. A source that is missing shows its state, never an empty tile.
- **D3 -- purity is tested on the output.** The renderer is a deterministic function of `view.json`. A test parses the rendered HTML and requires every text node to be a value from the data or an entry of one label table kept as data; two renders of the same input are byte-identical.
- **D4 -- two legs, three triggers.** The fast leg (receipts, merge receipts, ledger; seconds) runs after each conductor event once the runner exists. The full leg runs the map build with `--record` first and runs at the batch-close moment. A scheduled run renders the tracked parts only.
- **D5 -- one file, two modes.** `view.html` embeds a snapshot of `view.json`; served by `python -m http.server` on localhost it re-reads `view.json` on an interval. Opened as a file or published as an artifact it shows the snapshot.
- **D6 -- Mermaid is shown as source text by default.** A rendering library is not part of the build. Whether to add one (a pinned CDN build with a Subresource Integrity hash, or a vendored file) is a separate operator ruling; neither exists in the repo today.
- **D7 -- no event log is assumed.** The view reads the files that exist now. When ADR-121 is ratified, a reader is a new source, not a redesign.

Nothing is built by this ADR. The build is a later lane that starts only after the operator ratifies.

## Quality attributes

- **Quality attribute(s):** verifiability (every figure on the page traces to an organ output), modifiability (a new organ adds a tile by data), portability (no new toolchain or dependency).
- **Scenario:** Source: the operator or a CC seat. Stimulus: a lane hands back, a merge lands, a batch closes, or a writer changes its receipt shape. Artifact: the view generator and its page. Environment: a local checkout with receipts present, a fresh clone with none, localhost or a file. Response: the page regenerates; each tile shows value, source and state; an unreadable or absent source shows its state rather than a blank or a guess.
- **Response measure:** two renders of the same `view.json` are byte-identical; 100 percent of rendered text nodes are a data value or a label-table entry (checked by test); zero dependencies added to pyproject.toml or uv.lock; a fixture for each source reader that yields UNREADABLE on a changed shape. The fast leg finishing in seconds is a target to be measured by the build lane, not a claim.
- **Decision evidence:** the matrix in the design evidence (V2 3.50 against V1 3.15, V5 2.80, V3 2.70, V0 2.45, V4 1.85); the probes of its Subagent claims, among them the stdlib-only generators (scripts/system_map.py:67, scripts/gen_dashboard.py:60), the single whole-tree entry (scripts/system_map.py:381) and the gitignored map outputs (.gitignore:201).

## Flip-condition

- Switch to extending scripts/system_map.py (option V1) if the build lane shows the map can expose a partial build, so a fast leg does not walk the whole tree, or if the operator rules for one organ per page.
- Switch to a template library only if the label table and tile set outgrow what a stdlib renderer can keep testable, and only through a separate dependency decision under ADR-106.
- Drop the live mode (D5) if localhost serving proves unused after two batch closes.
- Revisit D2 when ADR-121 is ratified.

## Alternatives considered

- **V0 keep only the on-demand map:** rejected; it shows the graph and nothing about runs or state (matrix 2.45).
- **V1 extend scripts/system_map.py:** the closest rival (3.15); rejected as first choice because its single build walks the whole tree, which the fast leg cannot afford, and because it would couple two organs.
- **V3 Jinja2 templates:** rejected; a new locked dependency for output the stdlib already produces (2.70).
- **V4 MDX or a JS build:** rejected; a second toolchain in a repo that records it is not a node app, and a format built for hand-written prose (1.85).
- **V5 extend scripts/gen_dashboard.py:** rejected; its page is a committed artifact that can go stale, which cannot serve a live view (2.80).
