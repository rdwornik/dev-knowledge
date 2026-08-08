---
id: "[#280]"
title: "Propagate the intake area to greenfield consumers via the deploy manifest"
status: closed
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S17] Make new-repo scaffolding correct-by-default"
generates: BACKLOG.md
---

- [#280] [P3][S] Propagate the intake area to greenfield consumers via the deploy manifest — `docs/intake/` + `templates/intake-template.md` are hub-only today (no `intake` reference in `deploy/manifest-v*.yaml`), so a fully-deployed consumer inherits no intake scene. Add the area + template to a future manifest version so greenfield repos get `docs/intake/` at deploy (filed by the ADR-98 2026-07-07 amendment) · Done when: a manifest version ships the intake area/template and a deployed consumer carries `docs/intake/README.md` + `templates/intake-template.md` · refs deploy/manifest-v1.2.0.yaml, templates/intake-template.md, docs/decisions/ADR-98-intake-pipeline.md
