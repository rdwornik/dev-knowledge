# Fleet registry — `Dev/` repos (human-facing)

<!-- scope: meta -->

> **Hand-maintained human registry.** Created per the 2026-07-08 fleet-consistency census
> ruling C-10 (`docs/audits/2026-07-08-fleet-consistency-census.md` Part 5) — the census's one
> sanctioned registration write, held pending the operator's ruling on the mechanism, now landed
> as this file.
>
> **The registry is two surfaces, split by audience:**
> - **`ecosystem/registry.md` (this file) = the human registry** — name · path · purpose · status,
>   hand-maintained. Add a row when a repo is created; it needs no tooling.
> - **`ecosystem/<repo>/` + `ecosystem/index.yaml` = the machine registry** — born at methodology
>   onboarding (`ecosystem/<repo>/state.yaml` is gitignored; `history/*.md` is tracked). `index.yaml`
>   is **generated** (`audit.py::regenerate_index` overwrites it wholesale) — **never hand-edit it**.
>   The durable per-repo deployed-corpus version lives in `ecosystem/deployed-versions.yaml` (written
>   by the deploy runbook, not by hand).
>
> Purposes for the five already-registered repos are distilled from each repo's own `VISION.md`;
> the demo-prep and life-architect rows are the census Part-5 drafted entries verbatim.

| Repo | Path | Purpose | Status |
|---|---|---|---|
| `.dev-knowledge` | `C:\Users\1028120\Documents\Dev\.dev-knowledge` | Universal LLM-driven development guide and methodology framework; governs all projects under `Dev/`; Layer 2 of the ADR-28 three-layer ecosystem model. | source (hub — methodology origin) |
| `ai-council` | `C:\Users\1028120\Documents\Dev\ai-council` | Multi-model AI debate and research tool for architectural decision-making across the dev ecosystem; produces binding ADRs governing all `Dev/` repos; standalone CLI consumed via the `council` entry point. | registered · onboarded (v1.3.1) |
| `corp-monorepo` | `C:\Users\1028120\Documents\Dev\corp-monorepo` | Consolidated codebase of a personal Corporate OS — AI platform automating Rob's pre-sales / solution-advisory work at Blue Yonder; extracts corporate source material into a queryable knowledge base and drives RFP responses, presentation drafts, and opportunity prep. | registered · onboarded (v1.2.0) |
| `corp-ops` | `C:\Users\1028120\Documents\Dev\corp-ops` | Standalone operational toolbox for the Corporate OS ecosystem — Python package + PowerShell scripts managing OneDrive/SharePoint files, Google-Drive backup, bidirectional sync, and ecosystem health checks; not an agent (manual / Task-Scheduler triggered). | registered · unonboarded |
| `corp-sca-time-automation` | `C:\Users\1028120\Documents\Dev\corp-sca-time-automation` | Automates weekly time-entry submission to the SharePoint SCA Time Tracker from Outlook calendar exports — maps events to categories, detects the client, fills to a 40-hour week, writes an Excel preview, and uploads via the Graph API. | registered · unonboarded (floor-carrying) |
| `demo-prep` | `C:\Users\1028120\Documents\Dev\demo-prep` | Single home for Blue Yonder corporate presentation creation — brand kit · templates · knowledge base · deck-production pipeline · generator patterns + reference decks; explicit precursor to a corp-monorepo presentation module. | registered · methodology-unonboarded |
| `life-architect` | `C:\Users\1028120\Documents\Dev\life-architect` | Persistence + governance layer for the operator's "architect of life" workflow — archives ephemeral per-dimension browser chats into durable work-items, knowledge notes, and decision records; a sibling applying the dev-methodology loop to life domains (horizon: a "Life OS"). | registered · methodology-unonboarded · GitHub origin CONFIRMED Private (operator, 2026-07-08) |
| `terminal-setup` | `C:\Users\1028120\Documents\Dev\terminal-setup` | PowerShell terminal-profile bootstrap - an Oh My Posh theme (`huvix-custom.omp.json`) plus a `setup.ps1` installer for PS5/PS7. Purpose distilled from the repo itself (2 commits, HEAD `d8a7b61`), NOT from a `VISION.md` - it has none. | registered 2026-08-01 ([#462]) · unonboarded · declared fleet by ADR-104 2026-07-24; no methodology adoption (no VISION.md, no CLAUDE.md, no deploy record) |
| `win-tooling` | `C:\Users\1028120\Documents\Dev\win-tooling` | Personal Windows desktop-productivity toolbox - local Whisper transcription (large-recording cloud fallback) + TypeWhisper dictation-quality helpers; home for future desktop tooling (Flow Launcher, tablet). Not an agent; run manually. | registered · unonboarded |

## Fleet shape, and the migration posture

> Moved here from the root `README.md` by operator ruling **R-README** (2026-09-01). The README
> is the HUMAN front door -- what this repo is, why it exists, how to start, where to go deeper.
> Fleet-internal governance states are not that, and a reader arriving at the front door does not
> need them to start. They belong on an `ecosystem/` surface, beside the roster they qualify.

**The shape is a governed POLYREPO** (ADR-104, Accepted 2026-07-24). The ruled shape is a
**partial** fold: `corp-monorepo` stays permanently outside it -- history-entangled employer
material plus a load-bearing test dependency -- and the remaining repos consolidate
**incrementally**, verifying value stage by stage rather than in one move. **No fold executes on
that ADR**, so the independent-repo relationship the table above describes is current state, not
a provisional arrangement.

**The canonical purpose document is mid-migration, and the posture is per-member.** ADR-114
(Accepted 2026-08-29, AMENDMENT 1) moved the hub's front door to `README.md` and superseded
`VISION.md`. Two rows carry the consequence and **neither count is restated here** -- both are
derived, and `ecosystem/parity-surfaces.yaml` is the surface that computes them:

- `canonical-doc-vision` -- **retired from MUST to SHOULD on both roles**, 2026-08-31, by
  `[#614]` lane-a. `VISION.md` is retired from a mandatory ROLE, not removed from any tree: it is
  still tracked, byte-identical, at the hub root and in the members that carry one.
- `root-readme-front-door` -- **MUST at the hub, LOCAL for consumers**, on measured evidence
  rather than preference. A consumer-side MUST would turn members RED in one commit, so the
  promotion travels **by the deploy carrier**, repo by repo, in CUT-1's ruled order
  `hub -> monorepo -> ai-council -> win-tooling`. Each member's row flips when the carrier has
  landed there, and not before.

**Why the file rename is a program and not a flag flip.** `VISION.md` is read by name, or by its
`## H2` spine, from hub organs and deploy manifests -- among them the `vision_md` audit check,
which **hard-FAILs** on its absence at the repo root, and `gen_handoff.py`, which extracts its
`## Vision` section into every handoff bundle. Measured 2026-09-01 by moving the file and running
the gate: `audit.py health` exits 1 on `vision_md: VISION.md absent at repo root`, and
`tests/test_canonical_docs.py::test_gen_handoff_still_extracts_the_live_vision_section` REDs. The
registry retirement (tier) and the file's archival (path) are therefore **two separate acts**, and
only the first has been taken.

> **Maintenance:** add a row when a new repo joins `Dev/`. The `Status` column's onboarding state
> tracks `ecosystem/deployed-versions.yaml` (durable deploy record) — a repo shows `onboarded (vX.Y.Z)`
> once the deploy runbook populates its version, `unonboarded` while null. Do not hand-fabricate a
> version here; read it from `deployed-versions.yaml`.
