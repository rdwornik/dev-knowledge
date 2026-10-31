# Design: the system view (E3.0 /decide, lane e30-view-decide)

- **Run date:** 2026-10-31
- **Producer:** claude-sonnet-5-5 (lane head); research subagents claude-sonnet-5-5 (read-only); files written through the Copilot CLI claude-sonnet-5.5
- **Row:** refs row 1748 (filed by e30-bootstrap, not yet in this tree) (stays open: the build follows the operator's ratification)
- **Input:** to-browser digest DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31, section C (the operator's view), read from the transport
- **Output:** docs/decisions/ADR-133-the-system-view.md at status Proposed. Nothing is built.

## Brief

Question: which generator, data path and delivery should produce the operator's system view, so that the page shows only what organs compute, carries no hand-written prose, and stays current as lanes run?

Known constraints (no answer is pre-committed):
- The operator's rule is no prose, only generated or gate-checked text (PR-3, RATIFICATION-2026-10-27).
- Dependencies are declared, locked and gated (ADR-106); a new dependency or toolchain is its own decision.
- ADR-121 (the event log) is Proposed, so no event log may be assumed.
- Nothing is built before the operator ratifies; the build is a later lane (GO-E3.0 R13).
- The view is a lane beside the line, not on the path to the 2026-11-06 stop condition (GO-E3.0 R7).

Sub-questions fanned out: Q1 format and templating; Q2 data sources; Q3 delivery and refresh; Q4 where the code would live.

## Subagent briefs

Each brief is copied verbatim from the file the subagent was sent.

### Brief 1

```text
CONTEXT: the operator wants a read-only 'system view' page for this repo: a Python-generated static HTML file (plus a JSON file) showing what organs compute, with no hand-written prose. No design is chosen. Nothing is being built in this task. Digest section C is at H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md lines 150-178 (read only those lines).

SUB-QUESTION 1 (format and templating): what HTML-generating code does this repo already have, and what does it import? Answer: (a) which scripts write .html (scripts/system_map.py, scripts/gen_dashboard.py, any other: grep for '.html'), (b) for each: stdlib-only or a third-party templating import, (c) whether uv.lock / pyproject.toml declare jinja2, mako, chevron, markdown or any JS-build tool (count 'name = ' matches for each), (d) whether package.json is an app stack or a pin for a langserver, (e) whether any workflow under .github/workflows sets up Node.

EXCLUSION (R15, ecosystem/excluded-roots.yaml): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository.

OUTPUT: at most 400 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. A finding you cannot give a probe for must end in {unverified}. Facts only, no recommendation, no design. Repo root = your cwd (a git worktree of .dev-knowledge); cite repo-relative paths with forward slashes.
```

### Brief 2

```text
CONTEXT: the operator wants a read-only 'system view' page for this repo: a Python-generated static HTML file (plus a JSON file) showing what organs compute, with no hand-written prose. No design is chosen. Nothing is being built in this task. Digest section C is at H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md lines 150-178 (read only those lines).

SUB-QUESTION 2 (data sources): which machine-produced data could a view read without any hand-written text? For each of: ecosystem/system-map.json and ecosystem/system-map-record.json, the P1 Mermaid diagram (scripts/gen_process_diagrams.py --print; ecosystem/process-binding.yaml), PhaseReceipts under logs/receipts/LANE-*/r*/P*.json (schema in ecosystem/schema/phase_receipt.py), launch receipts logs/receipts/LAUNCH-*.json (writer in scripts/dispatch.py), logs/MERGE-RECEIPTS.jsonl, scripts/gen_ledger.py output, scripts/conductor.py metrics: give (a) writer script and line, (b) whether the file is tracked or gitignored (git check-ignore), (c) the top-level keys or fields of one real example if one exists on disk, (d) whether a schema or test pins its shape.

EXCLUSION (R15, ecosystem/excluded-roots.yaml): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository.

OUTPUT: at most 400 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. A finding you cannot give a probe for must end in {unverified}. Facts only, no recommendation, no design. Repo root = your cwd (a git worktree of .dev-knowledge); cite repo-relative paths with forward slashes.
```

### Brief 3

```text
CONTEXT: the operator wants a read-only 'system view' page for this repo: a Python-generated static HTML file (plus a JSON file) showing what organs compute, with no hand-written prose. No design is chosen. Nothing is being built in this task. Digest section C is at H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md lines 150-178 (read only those lines).

SUB-QUESTION 3 (delivery and refresh): what constraints bound serving a generated page live on localhost and as a frozen file? Answer from the repo, not from memory: (a) does the repo already serve any directory over HTTP (grep 'http.server' and 'serve' in scripts/ and .claude/), (b) how does scripts/system_map.py emit its output: output directory, --out-dir, --record flags, and what it does with the JSON (is the JSON embedded in the HTML or fetched), (c) which outputs are gitignored (.gitignore lines for system-map and conformance), (d) how scripts/gen_dashboard.py and scripts/system_map.py load any JavaScript library (CDN script tag, vendored file or none: grep '<script' ), (e) whether any existing page carries a Subresource Integrity attribute (grep -c 'integrity=').

EXCLUSION (R15, ecosystem/excluded-roots.yaml): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository.

OUTPUT: at most 400 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. A finding you cannot give a probe for must end in {unverified}. Facts only, no recommendation, no design. Repo root = your cwd (a git worktree of .dev-knowledge); cite repo-relative paths with forward slashes.
```

### Brief 4

```text
CONTEXT: the operator wants a read-only 'system view' page for this repo: a Python-generated static HTML file (plus a JSON file) showing what organs compute, with no hand-written prose. No design is chosen. Nothing is being built in this task. Digest section C is at H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md lines 150-178 (read only those lines).

SUB-QUESTION 4 (where the code would live): scripts/system_map.py is a candidate to extend. Answer: (a) its size in lines, its public CLI (click or argparse; subcommands and flags), and the functions that write the JSON and the HTML, (b) which tests cover it (tests/ files that import system_map) and how many test functions, (c) what wires it today: any workflow, hook, harness.yaml moment, organ-index entry or skill that calls it (grep 'system_map' over .github, .claude, ecosystem, scripts, tests), and whether ecosystem/organ-index.md lists it as an orphan, (d) the same facts for scripts/gen_dashboard.py in two lines, (e) whether a determinism test exists for either generator (same input gives byte-identical output).

EXCLUSION (R15, ecosystem/excluded-roots.yaml): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository.

OUTPUT: at most 400 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. A finding you cannot give a probe for must end in {unverified}. Facts only, no recommendation, no design. Repo root = your cwd (a git worktree of .dev-knowledge); cite repo-relative paths with forward slashes.
```

## Subagent claims

Each claim is one a subagent reported and the matrix or the pre-mortem relies on. A probe was run by scripts/decide_checks.py; an absence cannot be probed by a count, so it is recorded as unverified with the producer's own count in the text.

- Q1: scripts/system_map.py imports stdlib html and no templating library {probe: grep -c 'import html' scripts/system_map.py}
- Q1: scripts/gen_dashboard.py imports stdlib html and no templating library {probe: grep -c 'import html' scripts/gen_dashboard.py}
- Q1: uv.lock locks no templating library; the producer's own count of name = "jinja2" in uv.lock is 0 {unverified}
- Q1: package.json says this repo is not a node app and pins only a langserver {probe: grep -c 'NOT a node app' package.json}
- Q1: no workflow under .github/workflows sets up Node; the subagent's count of setup-node over the three workflows is 0 {unverified}
- Q4: scripts/system_map.py builds the whole tree through one entry function, build_map, with no partial leg {probe: scripts/system_map.py:381}
- Q4: render_html turns the in-memory dict into server-side markup and the page's only script is the inline _JS block {probe: scripts/system_map.py:558}
- Q4: write_outputs writes the JSON, the HTML and the tracked record {probe: scripts/system_map.py:718}
- Q3: the system-map JSON and HTML are gitignored {probe: git check-ignore ecosystem/system-map.json}
- Q3: the record file ecosystem/system-map-record.json is tracked and survives a fresh clone {probe: ecosystem/system-map-record.json:1}
- Q4: tests/test_system_map.py pins byte-identical JSON for the same tree and has no byte-identity test for the HTML {probe: tests/test_system_map.py:81}
- Q4: scripts/gen_dashboard.py has a byte-determinism test for its generator {probe: grep -c 'test_build_is_deterministic_and_regeneration_is_idempotent' tests/test_gen_dashboard.py}
- Q4: the /map command is the only caller of scripts/system_map.py {probe: grep -c 'system_map' .claude/commands/map.md}
- Q4: ecosystem/harness.yaml records scripts/system_map.py in a fates entry called by the /map command, not by a moment {probe: grep -c 'scripts/system_map.py, called_by' ecosystem/harness.yaml}
- Q4: ecosystem/harness.yaml declares a batch-close moment a generator could be wired to {probe: ecosystem/harness.yaml:86}
- Q3: no existing page carries a Subresource Integrity attribute; the subagent's count of integrity= in system_map.py, gen_dashboard.py and conformance.html is 0 {unverified}
- Q3: the repo serves no directory over HTTP; the subagent's search for http.server found nothing {unverified}
- Q3: ecosystem/conformance.html is a committed generated artifact that the repo itself records can go stale {probe: .gitignore:88}
- Q2: PhaseReceipt is a pydantic model with a generated JSON schema, written per checkout under a gitignored receipts directory {probe: ecosystem/schema/phase_receipt.py:162}
- Q2: receipts under logs/receipts are gitignored {probe: git check-ignore logs/receipts/LANE-x/r1/P1.json}
- Q2: the launch receipt path is built by _receipt_path in scripts/dispatch.py {probe: scripts/dispatch.py:812}
- Q2: launch receipts have no JSON schema and the caller field does not exist in this checkout; the producer's count of "caller" in scripts/dispatch.py is 0 {unverified}
- Q2: logs/MERGE-RECEIPTS.jsonl is tracked and appended by scripts/merge_receipt.py {probe: scripts/merge_receipt.py:1216}
- Q2: logs/MERGE-RECEIPTS.jsonl rows carry merge_sha {probe: grep -c 'merge_sha' logs/MERGE-RECEIPTS.jsonl}
- Q2: scripts/conductor.py metrics() reports a value or NOT COMPUTED with a reason, the shape a tile can copy {probe: scripts/conductor.py:414}
- Q2: the P1 Mermaid is produced by render_mermaid and stored in ecosystem/process-binding.yaml {probe: scripts/gen_process_diagrams.py:366}
- Q2: the stored P1 diagram sits in ecosystem/process-binding.yaml {probe: ecosystem/process-binding.yaml:872}
- Q2: scripts/gen_ledger.py writes to the transport directory, outside the repo {probe: scripts/gen_ledger.py:76}
- Q2: ADR-121 is Proposed, so no event log exists to read {probe: grep -c 'Status:\*\* Proposed' docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md}

## Evidence and matrix

Options. V0 keep only the on-demand map. V1 extend scripts/system_map.py with the view. V2 a new stdlib generator, a sibling of the map, that reads organ outputs including the map JSON. V3 a Jinja2 template generator. V4 an MDX or other JS-build page. V5 extend scripts/gen_dashboard.py and its committed conformance page.

Criteria. coverage: shows graph, process, runs and state. purity: the page is a pure function of machine data, no hand text. footprint: new dependencies, toolchain and gate burden (ADR-106). reuse: library-first, an existing organ over a new one, and orphan clearance. liveness: live on localhost and as a frozen file. testability: a determinism test can pin it.

Scores are 1 to 5. A 4 or 5 carries a footnote whose body says measured; every other score is a judgment on an unbuilt design and caps at 3.

Weights: coverage=20 purity=20 footprint=15 reuse=15 liveness=15 testability=15

| Option | coverage | purity | footprint | reuse | liveness | testability | Σ |
|---|---|---|---|---|---|---|---|
| V0 on-demand map only | 1 | 3 | 4[^1] | 3 | 1 | 3 | 2.45 |
| V1 extend system_map.py | 3 | 3 | 4[^1] | 4[^2] | 2 | 3 | 3.15 |
| V2 new stdlib sibling generator | 3 | 4[^3] | 4[^1] | 3 | 3 | 4[^3] | 3.50 |
| V3 Jinja2 templates | 3 | 3 | 2 | 2 | 3 | 3 | 2.70 |
| V4 MDX or JS build | 3 | 1 | 1 | 1 | 3 | 2 | 1.85 |
| V5 extend gen_dashboard.py | 2 | 3 | 4[^1] | 3 | 1 | 4[^3] | 2.80 |

[^1]: measured -- no templating library is locked and the stdlib html module already builds both repo pages: scripts/system_map.py:67 and scripts/gen_dashboard.py:60
[^2]: measured -- scripts/system_map.py:718 is a working writer with its own tests, and ecosystem/harness.yaml:170 already records it as a fated organ
[^3]: measured -- a stdlib html generator with a byte-determinism test exists: tests/test_gen_dashboard.py:558

Reading the matrix:
- V2 leads V1 by 0.35 on judgment scores. The difference rests on one fact: build_map is a single whole-tree entry (scripts/system_map.py:381), so a view leg that must finish in seconds cannot call it per event. A sibling generator reads the map JSON when present and runs the full map build only at batch close.
- V2 still clears the map organ's wiring gap: its full leg runs the map build, so the map gets a caller other than the on-demand command.
- V0 is the baseline, not a candidate: it shows the graph and nothing about runs or state.
- V3 and V4 lose on footprint and reuse, the two criteria ADR-106 and the library-first rule make binding.
- V5 loses on liveness: its page is a committed artifact the repo records can go stale (.gitignore:88).

## Pre-mortem

Assume the view was built as V2 and failed six months later. The likely causes, and what the design must carry against each:
1. The page looks empty in CI. Receipts are per-checkout and gitignored, so a scheduled run on a fresh clone sees none. A blank tile reads as zero activity. Against: every tile carries a state (OK, STALE, ABSENT, UNREADABLE, NOT COMPUTED with a reason), the conductor metrics shape.
2. The no-prose rule decays. A string-length rule on the generator is gamed by splitting strings. Against: test the rendered output, not the source: every text node must be a value from the data or an entry of one fixed label table.
3. A writer changes shape and the tile silently breaks. System-map JSON and launch receipts have no JSON schema (claims above); only the phase receipt does. Against: typed readers per source that fail to UNREADABLE, plus a test per reader on a fixture.
4. The full leg is slow and gets skipped. The map build is whole-tree. Against: the fast leg never calls it; the full leg runs at batch close only; the stale tile says which leg last ran.
5. The two delivery modes drift. Live (fetch) and frozen (embedded snapshot) are two code paths. Against: one data object, serialised once, consumed by both; a test parses both and compares.
6. The renderer dependency creeps in. A CDN script is the first Subresource Integrity use in the repo, and vendored JS is a new path with no convention. Against: Mermaid source is shown as text by default; a renderer is an operator ruling, not a build default.
7. The design leans on an event log. ADR-121 is Proposed and the launch receipt caller field does not exist yet. Against: the design reads files that exist today and names each one; it adds no event reader.
8. The builder extends the map organ in passing and couples the two. Against: the ADR names the new file and forbids edits to scripts/system_map.py from the view lane.
