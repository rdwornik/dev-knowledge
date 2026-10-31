# ADR-133: The system view is a pure rendering of what organs compute

- **Status:** Proposed
- **Date:** 2026-10-31
- **Decision tier:** Path A -- a `/decide` proposal for operator ratification (R13, ADR-108 section A).
- **Related:** ADR-106 (declared dependencies), ADR-121 (event log, Proposed), ADR-130 (the outer loop); row 1748 (filed by e30-bootstrap, not yet in this tree; it stays open until the build); GO-E3.0 PR-3 (no hand-written prose).
- **Decommission:** none.
- **Source:** the design evidence docs/audits/2026-10-31-technical-design-view.md (matrix, pre-mortem, response table); the proposal is the operator's view, digest section C, 2026-10-31. Two independent evaluators (codex gpt-6-sol, grok-4.7) amended the first draft; their twenty findings are all answered in the evidence file.

## Context

The operator wants one page that shows the system as organs compute it: the graph, the process, the runs and the state. The rule is no hand-written prose (PR-3). Today the repo has two stdlib HTML generators, scripts/system_map.py (the graph, on demand, called by the /map command) and scripts/gen_dashboard.py (a committed conformance page). No page shows runs or state. Receipts exist as files, per checkout, and ADR-121 (an event log) is only Proposed.

## Decision

- **D1 -- extend the map organ with a view subcommand, stdlib only.** The `/map` CLI gains a `view` subcommand that renders `view.json` and `view.html` into an output directory whose files the build adds to .gitignore (D5). The view code lives in a sibling module the subcommand calls. The map build and the map JSON are unchanged, and the existing byte-identity test of that JSON must stay green untouched. No templating library, no Node toolchain, no change to uv.lock. The view lane edits no other organ.
- **D2 -- data only.** `view.json` is assembled from organ outputs alone: the map JSON and tracked record, the P1 Mermaid, phase receipts, launch receipts, logs/MERGE-RECEIPTS.jsonl, the ledger (through its collect function, local leg only) and the conductor metrics. The quota report, the health output and the verdict ledger the operator named are also sources, but no one has yet measured their shape: each gets a reader that shows ABSENT or NOT COMPUTED until the build lane measures it. Every tile carries its source and a state: OK, STALE, ABSENT, UNREADABLE, or NOT COMPUTED with a reason. A state is computed at assembly and stored in the data, so rendering stays a pure function: STALE means assembly time minus the source's own timestamp exceeds that source's maximum age, a bounded entry in the label and threshold table. Only a missing required field makes a source UNREADABLE; an optional field never does. Every receipt tile names the checkout it was read from.
- **D3 -- purity is tested on the output.** The renderer is a deterministic function of `view.json`. A test parses the rendered HTML and requires every text node and every attribute value to be a value from the data or an entry of one label table, which is part of the data embedded in `view.json`. Each label entry is bounded in length and the table in size, both asserted by the test. The page's script is a fixed routine pinned by its hash, and a test requires that it holds no string literal beyond data keys and a fixed list of selectors, so it can write only data and label values and cannot carry a sentence. Mermaid source is data, shown as pre-formatted text. Two renders of the same input are byte-identical.
- **D4 -- two legs, three triggers, none blocking.** The fast leg (receipts, merge receipts, ledger) never calls the whole-tree map build. Until the conductor runner exists it is run by hand or at batch close; once the runner exists it may run after each event. The full leg runs the map build with `--record` and then the view. A scheduled run renders the tracked parts only (the map record and the merge receipts). Wiring the full leg to the batch-close moment is the operator's routing decision, and the step is declared optional and continue_on_failure, as the ci_red_age step is, so a failure never blocks a close. Neither leg gates anything: both are advisory.
- **D5 -- one file, two modes.** `view.html` embeds a snapshot of `view.json`, with the less-than sign escaped in the embedded copy. Served by `python -m http.server` on localhost it re-reads `view.json` on an interval; a parse failure keeps the snapshot. `view.json` is written atomically. Opened as a file or published as an artifact the page shows the snapshot. The build adds an ignore line for each output name and a test that `git check-ignore` holds for both, because the existing ignore lines name the map files only.
- **D6 -- Mermaid follows the operator's recommendation.** The P1 diagram is drawn by a pinned CDN build of the Mermaid library with a Subresource Integrity hash, loaded only when the page is served over http; the source text is always present as the fallback and is the only mode on a file or an artifact. The library, its version and its hash are data in one place. Two points are left for the operator to confirm: it would be the first Subresource Integrity use in the repo (an unverified count), and it makes the live page depend on the network. A vendored file would be a new path with no cited convention and is not proposed.
- **D7 -- no event log is assumed.** The view reads the files that exist now. When ADR-121 is ratified, a reader is a new source, not a redesign.

Open for the operator: confirm D6's CDN; decide whether the view reads receipts of sibling worktrees (this ADR reads the current checkout only); decide the batch-close wiring of D4.

Nothing is built by this ADR. The build is a later lane that starts only after the operator ratifies.

## Quality attributes

- **Quality attribute(s):** verifiability (every figure on the page traces to an organ output), modifiability (a new organ adds a tile by data), portability (no new toolchain or dependency).
- **Scenario:** Source: the operator or a CC seat. Stimulus: a batch closes or the view is requested; once the conductor runner exists, a lane hands back or a merge lands; or a writer changes its receipt shape. Artifact: the view subcommand and its page. Environment: a local checkout with receipts present, a fresh clone with none, localhost or a file. Response: the page regenerates; each tile shows value, source and state; an absent or unreadable source shows its state rather than a blank or a guess.
- **Response measure:** two renders of the same `view.json` are byte-identical; 100 percent of rendered text nodes and attribute values are a data value or a bounded label-table entry (checked by test); the page script's hash is pinned; the map JSON test stays green untouched; zero dependencies added to pyproject.toml or uv.lock; a fixture for each source reader that yields UNREADABLE on a missing required field and tolerates a missing optional one; `git check-ignore` holds for both outputs; a test parses the live and the frozen mode of the page and compares them. The cold start of the view subcommand and the fast leg finishing in seconds are targets the build lane measures, not claims.
- **Decision evidence:** the matrix in the design evidence (V1 3.30 against V6 3.10, V2 3.00, V5 2.80, V3 2.70, V0 2.45, V4 1.85), whose lead for V1 over the nearest rival is 0.20 and small; the probes of its Subagent claims, among them the two generators that import stdlib html (scripts/system_map.py:67, scripts/gen_dashboard.py:60), the single whole-tree entry (scripts/system_map.py:381), the explicit ignore lines (.gitignore:201) and the optional non-blocking batch-close precedent (the batch-close moment at ecosystem/harness.yaml:86 and the continue_on_failure claim).

## Flip-condition

- Switch to a separate generator with its own command (option V2) if the build lane measures that importing the map module makes the fast leg too slow to start, or that the view code cannot stay in its sibling module without coupling to the map build.
- Switch to a template library only if the label table and tile set outgrow what a stdlib renderer can keep testable, and only through a separate dependency decision under ADR-106.
- Drop the live mode (D5) if localhost serving proves unused after two batch closes.
- Drop the CDN renderer (D6) if the operator does not confirm it, leaving text only.
- Revisit D2 when ADR-121 is ratified.

## Alternatives considered

- **V0 keep only the on-demand map:** rejected; it shows the graph and nothing about runs or state (matrix 2.45).
- **V2 a new stdlib generator with its own command:** a rival (3.00); rejected as first choice because it adds an organ to wire and loses the map organ's existing writer, tests and fates entry; it is the flip target.
- **V6 extend scripts/gen_dashboard.py into the gitignored directory:** second (3.10); rejected because that generator is a conformance report with no graph or process model, so coverage is low.
- **V3 Jinja2 templates:** rejected; a new locked dependency for output the stdlib already produces (2.70).
- **V4 MDX or a JS build:** rejected; a second toolchain in a repo that records it is not a node app, and a format built for hand-written prose (1.85).
- **V5 extend scripts/gen_dashboard.py, committed page:** rejected; its page is a committed artifact that can go stale, which cannot serve a live view (2.80).
