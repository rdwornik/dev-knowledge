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

> **Maintenance:** add a row when a new repo joins `Dev/`. The `Status` column's onboarding state
> tracks `ecosystem/deployed-versions.yaml` (durable deploy record) — a repo shows `onboarded (vX.Y.Z)`
> once the deploy runbook populates its version, `unonboarded` while null. Do not hand-fabricate a
> version here; read it from `deployed-versions.yaml`.
