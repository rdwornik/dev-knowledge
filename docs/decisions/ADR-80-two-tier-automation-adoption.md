<!-- scope: meta -->

# ADR-80 — Two-tier automation adoption: writer policy + Routine/night operational standard

- **Status:** Accepted — 2026-06-07
- **Amends:** ADR-74 (consumes its **OPEN** "LOCAL scheduled night (Tier-2 cross-repo host)" matrix row — the mechanism was resolved by ADR-76; this ADR resolves that row's **writer policy**).
- **Related:** ADR-70 (three-tier process layer), ADR-72/73 (cloud-routine self-containment + per-repo orchestration), ADR-76 (local fleet-baseline host); BACKLOG #84 (this codification), #85 (night-run architecture / local scheduler), #123 (routine observability), #14 (ecosystem/ folder operating model), #100 (corp freshness restamp).
- **Decommission:** the interim **stash→ship→pop** working pattern for automation-dirtied trees (superseded — see Consequences; the Claude Code memory note `ship-around-fleet-health-dirty-tree` is now **OBSOLETE**).
- **Source:** Operator ruling, this session 2026-06-07 (chat-drafted path — writer policy Option (b) + 3 riders); evidence-gated codification of BACKLOG #84.

## Context

ADR-70 placed `.dev-knowledge`'s process layer across three friction-cadence tiers; ADR-74 consolidated every automation organ into one canonical layer→job matrix and named its **n=2 evidence-gate meta-rule** (Footnote B): a pattern is codified only after two real runs. BACKLOG #84 was the live instance held at that gate. Two facts were unresolved before this ADR:

1. **The matrix had an OPEN row** — the LOCAL scheduled night (cross-repo Tier-2 host). ADR-76 resolved its *mechanism* (Windows Task Scheduler → `python scripts/fleet_health.py`, no LLM on the scheduled path) but explicitly **not** its writer policy: every scheduled `audit.py`/`fleet_health.py` run leaves tracked files dirty (`ecosystem/<repo>/state.yaml`, `history/*.md`, the `docs/audits/*-ecosystem-audit.md` rollup), and the interim workaround was a manual stash→ship→pop dance (#85 validation record, 2026-06-06).
2. **The doctrine was prose-less.** ADR-74's matrix was citable but had no PLAYBOOK operating-doctrine section, no Routine/night *operational standard*, and the Model/Effort doctrine predated Opus 4.8 / `xhigh` / `ultracode` / `fallbackModel`.

The n=2 gate is now satisfied: the nightly conformance routine produced a **red** run (2026-06-06: N1 high #74 Done-when drift, N2 med ARCHITECTURE timestamp) that was triaged and resolved, then a **clean** run (2026-06-07, digest `0/0/0`, merged via PR #17 → `221c63e`). The corp scoped Tier-3 audit (2026-06-06, 29 targets) is a second independent Tier-3 datapoint. Evidence floor cleared; codification proceeds.

## Decision

### 1. Two-tier automation doctrine adopted fleet-wide
The PLAYBOOK "Two-tier automation doctrine" section is the operating-doctrine prose for ADR-74's matrix. The organising axis is **LLM judgment**: *deterministic* automation (no model — fail-closed on executing paths, fail-soft on awareness) vs *LLM-judgment* automation (**always read-only + adversarial-skeptic-filtered + operator-ratified**, delivered as a cloud Routine or a dynamic Workflow). This axis is **orthogonal** to ADR-70/74's friction-cadence Tiers 1/2/3 and **does not renumber them**.

### 2. Channel verdict — the cloud Routine output channel is compliant-by-design
The conformance Routine commits nothing itself (its agents are read-only and never write to disk). Its output reaches `main` via `claude/<task>-YYYY-MM-DD` branch → PR → the `nightly-conformance-triage` GitHub Action (diff-guard → `gh pr merge --squash --delete-branch`). **Witnessed:** PR #17 (`claude/conformance-2026-06-07` → `main`, MERGED, mergeCommit `221c63e`). The single non-merge commit on `main` is the **designed** cloud channel — a squash, deliberately distinct from the local branch+merge `--no-ff` discipline that governs human-authored arcs. This is **compliant-by-design, not a misconfiguration.**

### 3. Writer policy — automation that writes the tree commits its own output (Option b + 3 riders)
A job that writes tracked files **owns the commit of those files**; the tree is never left dirty for the operator. Resolves ADR-74's OPEN local-tier row:

- **(b) Mutable/durable split** — the high-churn mutable pointer (`ecosystem/<repo>/state.yaml`) is **gitignored**; the durable record (`history/*.md`, digests, the `docs/audits/*-ecosystem-audit.md` rollup) is **committed by the writer**.
- **Rider 1 — pathspec-bounded.** The job stages **exactly its own declared output paths** — never `git add -A`, never anything outside its outputs. An operator's unrelated dirty files are untouchable by automation.
- **Rider 2 — fail-soft.** On any commit failure (locked index, mid-merge, diverged `main`) the job leaves its files uncommitted, logs one WARN line, and **exits 0** — it never forces, never pulls/rebases, never resolves.
- **Rider 3 — `state.yaml` → `.gitignore`** lands via a **captured follow-up item** (not implemented in this ratifying session).

Local writer commits carry the `Routine: <name>` observability trailer (#123); the cloud channel keeps its PR per §2.

### 4. Routine/night operational standard adopted
The PLAYBOOK "Routine/night deployment standard › What every routine must meet" 7-point spec is the contract every recurring unattended review must satisfy before it graduates: self-containment, declared output channel, `Routine:` trailer, per-stage model pins (no `fallbackModel`), fail-soft + catch-up, funnel-review as consuming contract, and the n=2 graduation gate.

### 5. fallbackModel doctrine
Interactive sessions **MAY** set `fallbackModel` (resilience). Pinned routine/workflow stages **MUST NOT** — a silent fallback to a different model breaks evidence comparability across runs (the n=2 gate compares like-for-like). VF-2 (2026-06-07) confirmed `fallbackModel` is schema-accepted on Claude Code 2.1.168; the native `--fallback-model` flag is its CLI twin.

## Consequences

- **ADR-74's OPEN local-tier row is consumed** — mechanism (ADR-76) + writer policy (here) together close it.
- **The interim stash→ship→pop pattern is superseded.** Once the wiring lands (captured follow-up), the local writer commits its own pathspec-bounded output and the tree stays clean. The Claude Code memory note `ship-around-fleet-health-dirty-tree` is **OBSOLETE** — future sessions should stop applying stash→ship→pop. **Honest interim state:** until the wiring ships, the scheduled-run dirty tree persists; this ADR ratifies the doctrine *ahead of* the wiring (capture-only, per #84's no-implement-wiring rule).
- **Touches #14.** The writer policy presumes `ecosystem/` remains a committed substrate (it commits history/digests/rollup); the broader retire/snapshot question stays open under #14.
- **Evidence retained:** n=1 `docs/audits/2026-06-06-conformance-nightly-digest.md` (red) + n=2 `docs/audits/2026-06-07-conformance-nightly-digest.md` (`221c63e`, clean); `docs/audits/2026-06-06-85-validation-record.md` (local scheduler n=1 pre-case).

## Alternatives considered

- **Option (a) — writer commits everything, including `state.yaml`.** Rejected: the high-churn pointer adds commit noise and a larger blast radius for a bad auto-commit, with no record value over the durable artifacts.
- **Option (c) — automation state moves outside the repo (`~/.claude/ecosystem/`).** Rejected: loses in-repo auditability of automation outputs, pre-empts the open #14 decision, and cannot be global — the cloud Routine commits its digest in-repo via PR, so (c) would contradict the §2 channel verdict unless scoped to local-state-only.
