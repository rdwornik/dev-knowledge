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

Each claim is one a subagent or the producer reported and the matrix or the pre-mortem relies on. A probe was run by scripts/decide_checks.py; an absence cannot be probed by a count, so it is recorded as unverified with the producer's own count in the text.

- Q1: scripts/system_map.py imports stdlib html and no templating library {probe: grep -c 'import html' scripts/system_map.py}
- Q1: the import sits at line 67 of scripts/system_map.py {probe: scripts/system_map.py:67}
- Q1: scripts/gen_dashboard.py imports stdlib html and no templating library {probe: grep -c 'import html' scripts/gen_dashboard.py}
- Q1: the import sits at line 60 of scripts/gen_dashboard.py {probe: scripts/gen_dashboard.py:60}
- Q1: uv.lock locks no templating library; the producer's own count of name = "jinja2" in uv.lock is 0 {unverified}
- Q1: package.json says this repo is not a node app and pins only a langserver {probe: grep -c 'NOT a node app' package.json}
- Q1: no workflow under .github/workflows sets up Node; the subagent's count of setup-node over the three workflows is 0 {unverified}
- Q4: scripts/system_map.py builds the whole tree through one entry function, build_map, with no partial leg {probe: scripts/system_map.py:381}
- Q4: render_html turns the in-memory dict into server-side markup and the page's only script is the inline _JS block {probe: scripts/system_map.py:558}
- Q4: write_outputs writes the JSON, the HTML and the tracked record {probe: scripts/system_map.py:718}
- Q4: scripts/system_map.py imports click and yaml at module level, so a view subcommand pays that import cost; its size is unmeasured {probe: grep -c 'import click' scripts/system_map.py}
- Q3: the system-map JSON and HTML are gitignored by two explicit lines naming those two files {probe: git check-ignore ecosystem/system-map.json}
- Q3: the ignore lines are explicit file names, at .gitignore:201 and .gitignore:202 {probe: .gitignore:201}
- Q3: a new output name is not ignored until it has its own line; the producer's git check-ignore of a view file name exited 1 {unverified}
- Q3: the record file ecosystem/system-map-record.json is tracked and survives a fresh clone {probe: ecosystem/system-map-record.json:1}
- Q4: tests/test_system_map.py pins byte-identical JSON for the same tree and has no byte-identity test for the HTML {probe: tests/test_system_map.py:81}
- Q4: scripts/gen_dashboard.py has a byte-determinism test for its generator {probe: grep -c 'test_build_is_deterministic_and_regeneration_is_idempotent' tests/test_gen_dashboard.py}
- Q4: the /map command names scripts/system_map.py; the producer's repo-wide git grep finds the name only in that command, the harness fates entry, two test files and a ruling document {probe: grep -c 'system_map' .claude/commands/map.md}
- Q4: ecosystem/harness.yaml records scripts/system_map.py in a fates entry called by the /map command, not by a moment {probe: grep -c 'scripts/system_map.py, called_by' ecosystem/harness.yaml}
- Q4: ecosystem/harness.yaml declares a batch-close moment a generator could be wired to {probe: ecosystem/harness.yaml:86}
- Q4: a batch-close step can be declared optional and non-blocking: the ci_red_age step carries continue_on_failure true {probe: grep -c 'continue_on_failure: true' ecosystem/harness.yaml}
- Q4: the fates entry for the map says wiring it to a moment is a routing decision the operator owns {probe: grep -c 'routing decision the operator owns' ecosystem/harness.yaml}
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
- Q2: scripts/gen_ledger.py writes its markdown to the transport directory, outside the repo {probe: scripts/gen_ledger.py:76}
- Q2: scripts/gen_ledger.py also exposes collect(), which returns the open rows and worktrees as a dict without writing a file {probe: scripts/gen_ledger.py:197}
- Q2: ADR-121 is Proposed, so no event log exists to read {probe: grep -c 'Status:\*\* Proposed' docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md}
- Q2: the quota_watch report, the audit.py health output and the verdict ledger the digest names were not researched by any subagent; their shapes are unknown to this audit {unverified}

## Evidence and matrix

Options. V0 keep only the on-demand map. V1 extend the map organ, scripts/system_map.py, with a view subcommand whose code may live in a sibling module. V2 a new stdlib generator with its own command, reading organ outputs including the map JSON. V3 a Jinja2 template generator. V4 an MDX or other JS-build page. V5 extend scripts/gen_dashboard.py and its committed conformance page. V6 extend scripts/gen_dashboard.py but write the view into the gitignored output directory.

Criteria. coverage: shows graph, process, runs and state. purity: the page is a pure function of machine data, no hand text. footprint: new dependencies, toolchain and gate burden (ADR-106). reuse: library-first, an existing organ over a new one, and orphan clearance. liveness: live on localhost and as a frozen file. testability: a determinism test can pin it.

Scores are 1 to 5. A 4 or 5 carries a footnote whose body says measured and measures that very option; every other score is a judgment on an unbuilt design and caps at 3. A precedent measured on a different generator does not lift an unbuilt option above 3.

Weights: coverage=20 purity=20 footprint=15 reuse=15 liveness=15 testability=15

| Option | coverage | purity | footprint | reuse | liveness | testability | Σ |
|---|---|---|---|---|---|---|---|
| V0 on-demand map only | 1 | 3 | 4[^1] | 3 | 1 | 3 | 2.45 |
| V1 extend the map organ with a view subcommand | 3 | 3 | 4[^1] | 4[^2] | 3 | 3 | 3.30 |
| V2 new stdlib generator, own command | 3 | 3 | 4[^1] | 3 | 3 | 3 | 3.15 |
| V3 Jinja2 templates | 3 | 3 | 2 | 2 | 3 | 3 | 2.70 |
| V4 MDX or JS build | 3 | 1 | 1 | 1 | 3 | 2 | 1.85 |
| V5 extend gen_dashboard.py, committed page | 2 | 3 | 4[^1] | 3 | 1 | 4[^3] | 2.80 |
| V6 extend gen_dashboard.py, gitignored output | 2 | 3 | 4[^1] | 3 | 3 | 4[^3] | 3.10 |

[^1]: measured -- the stdlib html module already builds both repo pages (scripts/system_map.py:67 and scripts/gen_dashboard.py:60), and the producer's own count of a locked templating library in uv.lock (name = "jinja2") is 0
[^2]: measured -- scripts/system_map.py:718 is a working writer with its own tests, and ecosystem/harness.yaml:170 already records it as a fated organ
[^3]: measured -- tests/test_gen_dashboard.py:558 is a byte-determinism test of the generator V5 and V6 would extend; it measures that generator only, so it lifts no other option

Reading the matrix:
- The first draft of this matrix put V2 first at 3.50. The two evaluators showed why that was wrong (findings S1, G1, S2, S3, G2): two of V2's 4s were measured on another generator, and V2's liveness edge assumed a V1 fast leg must call the whole-tree build_map, which is not so, because a view subcommand can read the map JSON when present exactly as a sibling would. With both corrections V1 leads.
- V1 leads V2 by 0.15 and V6 by 0.20. That margin is inside judgment noise. What separates V1 is its reuse score, the one differing 4 that is measured: a working writer, its tests and a fates entry, and no new organ to wire. The operator-side digest reached the same direction (extend the map organ, section A2).
- V6 is the strongest rival to V1 that the first draft did not score (finding G9). It loses on coverage: the gen_dashboard generator is a conformance report and holds no graph or process model.
- V0 is the baseline, not a candidate: it shows the graph and nothing about runs or state.
- V3 and V4 lose on footprint and reuse, the two criteria ADR-106 and the library-first rule make binding.
- V5 loses on liveness: its page is a committed artifact the repo records can go stale (.gitignore:88).
- Unscored: modifiability and coupling are not matrix criteria. They are the reason the ADR carries a flip-condition to V2.

## Pre-mortem

Assume the view was built as V1 and failed six months later. The likely causes, and what the design must carry against each:
1. The page looks empty in CI. Receipts are per-checkout and gitignored, so a scheduled run on a fresh clone sees none. A blank tile reads as zero activity. Against: every tile carries a state (OK, STALE, ABSENT, UNREADABLE, NOT COMPUTED with a reason), the conductor metrics shape.
2. The no-prose rule decays. A string-length rule on the generator is gamed by splitting strings, and a label table is a second input a sentence can enter. Against: test the rendered output (text nodes and attributes), bound each label-table entry in length and the table in size, and pin the page's script by hash so a change to it is deliberate.
3. A writer changes shape and the tile silently breaks. System-map JSON and launch receipts have no JSON schema (claims above); only the phase receipt does. Against: typed readers per source that fail to UNREADABLE only on a required field, with optional fields tolerated, plus a fixture test per reader.
4. The view couples into the map organ. The map file is large and its JSON is pinned by a byte-identity test. Against: view code lives in a sibling module the map CLI calls, the existing byte-identity test must stay green untouched, and the flip-condition names V2.
5. The fast leg is slow to start. The map module imports click, yaml and two repo modules at load (claims above); that cost is unmeasured. Against: the build lane measures cold start of the view subcommand before the fast leg is wired to anything.
6. The two delivery modes drift or the embedded data breaks the page. Live (fetch) and frozen (embedded snapshot) are two code paths, and unescaped data in a script tag or a read during a write can corrupt the page. Against: one serialised data object consumed by both, a less-than sign escaped in the embedded copy, an atomic write of the data file, and a test that parses both and compares.
7. The ledger or an operator-named source is missing on a clean clone. The ledger markdown is written outside the repo; the quota report, the health output and the verdict ledger were never researched. Against: each such source is read by its own typed reader and shows ABSENT or NOT COMPUTED with a reason; the build lane researches a source's shape before its tile exists.
8. The batch-close wiring blocks a close. Against: the moment step is declared optional and continue_on_failure, as the ci_red_age step is, and the wiring is the operator's routing decision, not part of the build.
9. The design leans on a runner or an event log that does not exist. The conductor runner is a later lane and ADR-121 is Proposed. Against: until the runner exists the fast leg is run by hand or at batch close; the design reads only files that exist today.
10. The renderer dependency creeps in. A CDN script is the first Subresource Integrity use in the repo. Against: the library, its version and its hash are data in one place, and the text fallback is always present.
11. Receipts from other checkouts never reach the page. Against: the page names the checkout it was built from on every receipt tile; reading sibling worktrees is a build-lane measurement and an operator choice.

## Evaluator findings and responses

Evaluators: codex gpt-6-sol (to-browser/EVAL-VIEW-E30-sol-2026-10-31.md, ids S1 to S8) and grok-4.7 (to-browser/EVAL-VIEW-E30-grok-2026-10-31.md, ids G1 to G12), both from families other than the producer's, each given only copies of the input section, this evidence file and the first ADR draft. The first draft is commit 743284c35.

| id | objection (short) | response |
|---|---|---|
| S1 | V2 purity and testability 4s measure a different generator | **Accepted** -- both capped at 3 and footnote 3 now says it lifts no other option; this moved V2 from 3.50 to 3.15 |
| S2 | V1 liveness 2 against V2 3 has no evidence | **Accepted** -- V1 liveness is now 3; a view subcommand reads the map JSON as a sibling would |
| S3 | ADR says V1 fast leg cannot afford the whole-tree build, audit shows only no partial leg | **Accepted** -- the claim is withdrawn; the fast leg never calls the whole-tree build in either option |
| S4 | ledger source for the scheduled tracked-only run is not established | **Accepted** -- the scheduled run reads the map record and the merge receipts only; the ledger is a local-leg source read through collect() and is ABSENT where it cannot be computed |
| S5 | the fast-leg trigger depends on a runner that does not exist | **Accepted** -- the ADR now says the fast leg is run by hand or at batch close until the runner exists |
| S6 | receipts are per checkout, the page claims to be current | **Accepted** -- every receipt tile names its checkout; reading sibling worktrees is left to the build lane and the operator |
| S7 | the text-node test misses script-written text, attributes and Mermaid source | **Accepted** -- the test covers text nodes and attributes, the page script is pinned by hash, Mermaid source is data shown as pre-formatted text |
| S8 | no safe embedding or write protocol for the snapshot | **Accepted** -- less-than sign escaped in the embedded copy, atomic write of the data file, parse failure keeps the snapshot |
| G1 | the cap is broken to crown V2, margin disappears when capped | **Accepted** -- same correction as S1; V2 3.15 ties the old V1 score and the leader changes to V1 at 3.30 |
| G2 | the stated reason for the margin is incomplete | **Accepted** -- the first draft's reading is replaced; the margin and its sources are stated per criterion |
| G3 | V1 is rejected for coupling while V2 couples via the map build; the only-caller claim is one file | **Accepted** -- the coupling argument is dropped from the ADR as a reason against V1; the claim is reworded to what the producer's repo-wide git grep found and one probe cannot prove |
| G4 | full leg at batch close can block the lane beside the line | **Accepted** -- the step is optional and continue_on_failure like ci_red_age, and wiring it is the operator's routing decision |
| G5 | the ledger has three incompatible stories | **Accepted** -- resolved as in S4: collect() in the local leg, absent from the tracked-only scheduled run |
| G6 | operator-named state sources dropped | **Accepted** -- quota report, health output and verdict ledger are named sources in the ADR; none was researched, so each gets a reader that shows ABSENT or NOT COMPUTED until its shape is measured, and this audit says so |
| G7 | label table is an unbounded second input and script text escapes the test | **Accepted** -- label entries bounded in length, table bounded in size, script pinned by hash, attributes covered |
| G8 | the new output names may not be ignored | **Accepted** -- the ignore lines are explicit file names (.gitignore:201), so the ADR requires a new ignore line for each output and a test that git check-ignore holds for both |
| G9 | V5 mis-stated and double-penalised, gitignored rival missing | **Accepted** -- V6 added and scored (3.10); the double-penalty reading is not accepted for V5, since staleness and no live mode are different defects, but V5's text now says which is which |
| G10 | D6 overrides the operator's Mermaid recommendation | **Accepted** -- D6 now adopts the operator's recommendation (pinned CDN build with an integrity hash, text fallback always present) and leaves its confirmation as an operator item |
| G11 | STALE undefined and a clock would break byte-identity; a missing optional field could mark a receipt UNREADABLE | **Accepted** -- states are computed at assembly from each source's own timestamp and stored in the data, so rendering stays a pure function; only a missing required field is UNREADABLE |
| G12 | footprint measurement is weaker than the ADR states and two cited lines are unprobed | **Accepted** -- footnote 1 now says exactly what was measured, the two import lines carry their own path-line probes, and the absence counts stay marked unverified |
