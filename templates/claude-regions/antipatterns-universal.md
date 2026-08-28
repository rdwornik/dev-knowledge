
- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Copying `CLAUDE.md` wholesale into `AGENTS.md`** — ADR-115 admits `AGENTS.md` as the portable instruction layer, superseding ADR-53 Decision 2; a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently — carry the portable half only, and leave the Claude-runtime remainder in `CLAUDE.md`
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
