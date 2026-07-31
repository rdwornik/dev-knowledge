---
id: "[#459]"
title: "ARCHITECTURE.md prose for the ADR-109 desired-state organ class"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S24] Declare desired state once, as data, instead of as N registries"
serialize-group: architecture
generates: BACKLOG.md
---

- [#459] [P3][S] **ARCHITECTURE.md prose for the ADR-109 desired-state organ class** — grep-verified 2026-07-31 at the [#382] arc close: ARCHITECTURE.md carries ZERO mention of the arc's new component class (`ecosystem/schema/` pydantic contract, `scripts/desired_state_loader.py`, `scripts/desired_state_report.py`). The codemap covers the two scripts/ modules (regen-and-diff green in-wave) but `ecosystem/schema/` sits structurally OUTSIDE its `--source-root scripts` scope — the prose leg should also rule whether the codemap's source-root widens or the schema package is declared out-of-codemap with a reason. Deferred out of the arc per freshness discipline (an ARCHITECTURE edit owes a genuine end-to-end re-read + `last_reviewed` re-stamp). · Done when: ARCHITECTURE names the organ class at the right chapter (likely Ch6 verification mesh or Ch2 organ map) with ADR-109 cited, the codemap-scope question is ruled in the same edit, and `last_reviewed` rides a genuine re-read · refs ARCHITECTURE.md, ADR-109, ecosystem/schema/, scripts/desired_state_loader.py, scripts/desired_state_report.py · kill-candidates: none — no open row owns ARCHITECTURE currency for the E9 organs; [#458] owns a PLAYBOOK note, different doc · serialize-group: architecture
