---
id: "[#460]"
title: "`ecosystem/*/history/` dailies are WRITE-ONLY TELEMETRY, NO CONSUMER — operator question: keep / aggregate / stop"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#460] [P2][S] **`ecosystem/*/history/` dailies are WRITE-ONLY TELEMETRY, NO CONSUMER — operator question: keep / aggregate / stop** — census at the [#382] close; full evidence in `docs/audits/2026-07-31-verification-382-ladder-evidence.md` §L0.5. Writer: `audit.py cmd_run` (`audit.py:361`) via the SessionStart `fleet_health.py` hook and a daily `fleet-baseline` scheduled task. **Readers: none** — nothing in `scripts/`/`deploy/`/`plugins/` reads a daily's content (the three near-hits are an exclusion, writer-side path enumeration, and an unrelated doc §12 scan). ADR-80 sanctioned committing them as "the durable record" but named no consumer — the shape ADR-105 later ruled must be declared at ACTIVATION. Two oddities to absorb: the scheduled task runs the SYSTEM python not `uv run --locked` (ADR-106), and its trail on `automation/fleet-audit` stops 2026-07-16. · Done when: the operator rules keep (named consumer + consumption_path, ADR-105) / aggregate / stop, with both divergences dispositioned · refs scripts/audit.py, ADR-80, ADR-105, ADR-106, #419, #426 · kill-candidates: none — [#419] owns the general class, [#426] its coverage · serialize-group: settings-json
