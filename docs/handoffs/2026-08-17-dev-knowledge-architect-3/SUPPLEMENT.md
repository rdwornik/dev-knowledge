# Architect strategic supplement — 2026-08-17-dev-knowledge-architect-3

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

ARCHITECT ANSWERS — handoff Q1-7, seat 2026-08-14-dev-knowledge-architect, 2026-08-17

1. STRATEGIC INTENT: Shift the window class from audit-PRODUCING to audit-CONSUMING and net-CLOSING. The next session's way-of-working goal: every ratified piece of knowledge becomes either a wired mechanism or a closed row — no third state. Concretely: throughput first (#533 leg 2), wire the two BUILT-UNWIRED libraries, ratify intakes #35-#39 into ADRs+rows, run the first net-negative backlog batch (closing campaign batch 1 with the kill-candidates instrument).

2. TENSIONS WEIGHED: (a) max parallel width vs serial integration queue -> settled at width 11-12 with admission control MAX 6 active locally (measured: 99.6% CPU, hook starvation at 12); the queue is the binding constraint, not lane count. (b) Workaround vs structural fix at the l<->y collision -> chose mid-batch decomposition (#533); cost accepted: 27 checks held on three measured blocker classes; gain: the collision class is dead, not patched. (c) Behavior-freeze vs performance in lane m -> kept byte-identical golden proof, deferred parallelism to leg 2 (never mix refactor and behavior change). (d) Operator visibility vs process purity -> the §D direct-supplement was a process violation (owned); handoff runs by the book now. (e) Telemetry rank: lane c said #1, architect ruled #2 with #533-leg-2 first — measured commit-tax beats measurement infrastructure by one slot, no lower.

3. CONSIDERED + REJECTED (do not relitigate): section-scoped shared ownership for l<->y (superseded by #533 decomposition); hand-anchoring the ADR-110 exemption (batch-5 emergency shape only — uniform rename + the #531 creation-time gate is the standard); a 16-wide local batch (W5 cap + queue arithmetic + measured saturation); GPU substrate (I/O-bound workload, wf-fe444def verdict: open-weight still -8.6 SWE-bench pts and 5-20x latency); Oracle free tier (gutted, enforcement 2026-08-18); greening doc_rot by dispositions (fixes only); monorepo migration (stay polyrepo, hub-as-platform per wf-460fee76); file-sync tools for remote lanes (git is the sync layer).

4. OPEN QUESTIONS (deliberately deferred): consumer-side home for [#293] (nb5-B candidates await one ruling); final seam re-point shape for the 25 monkeypatch-pinned checks (smallest-diff vs shared seams module — nb5-A on the table); class-3 N-1 landing-predicate re-point (governance, separate from the seam leg); telemetry read-path stack (D3-first ruled; datasette vs static HTML decided after #529 wiring emits real data); routing-table amendment gated on NB4-A seeded-defect acceptance + the #492 Grok browser check (DUE TODAY 2026-08-17, assume peg possibly unmet — repo evidence says not-released as of 08-10); audit-corpus status: frontmatter row vs ADR-100 files-never-move tension (row filed, unratified).

5. DECOMPOSITION RATIONALE (do not redo): batch shape = ONE plan -> N file-disjoint frozen lanes -> ONE serial integrator with the operator as the only merge gate; RESERVED ID BLOCKS for concurrent births are now proven (17 births, zero collisions) and are the standard; every lane contract carries a PINNED-BY-TESTS section (five-witness finding: OWNED-FILES bounds writes, not test-pin dependencies); #533's module home is recorded (STANDING_RULINGS K-2) — never re-derive; ADR-110 exemption evaporates at closure (batch-6 discovery, recorded); in-lane tests run -n 0, parallelism belongs to the one integration suite.

6. OFF-REPO CONTEXT: five browser-research artifacts landed with EXTERNAL EVIDENCE headers, intakes #35-#39 DRAFT await ratification — they carry the model-portability (AGENTS.md-as-canonical + pointers), autonomy-ladder, done_when schema, fleet-conformance (fleet_check.py sketch), and substrate plans; substrate direction confirmed by the operator: Codespaces free tier stage 1 -> Hetzner CX53 SHARED (post-2026-repricing; NOT CCX), VS Code Remote Tunnel + tmux as the control plane, teleport is one-way web->local and the VS Code extension cannot attach to live remote bg sessions; the operator's standing demand: visible ROI — dispositions, archival routine, and net closure are the acceptance test of the next window, not new audits.

7. RATIFIED-IN-CHAT REGISTER (verbatim term · definition · durable home): "audit-to-row conversion authority" · every audit carries exactly one disposition ACTIONED/FILED/REJECTED/SUPERSEDED, an undisposed audit is a defect · PLAYBOOK batch-close section + already embodied in the 2026-08-17 disposition ledger; "admission control" · local batch width bounded by measured schedulable concurrency, default 6 on this machine class · PLAYBOOK §8 (candidate landed in LESSONS at batch-6 wrap — promote); "reserved id blocks" · concurrent-birth safety via per-lane disjoint id ranges printed at dispatch · PLAYBOOK batch protocol; "PINNED-BY-TESTS section" · mandatory lane-contract section listing live-tree properties the lane legitimately changes · PLAYBOOK §8b; "priority order v2" · #533-leg2 -> telemetry+single_flight wiring -> devcontainer -> seam-leg+l/y -> campaign batch 1 · supplement amendment (this handoff); "teleport one-way / no VS-Code-attach to remote bg" · substrate constraint from wf-fe444def · intake #39 ratification target, not PLAYBOOK yet.

