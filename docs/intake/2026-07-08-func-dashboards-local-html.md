---
intake-id: 9
status: SEED
origin: "operator direction, 2026-07-08 (this session)"
consumed-by:
---

# Dashboards as local HTML — the Tier-4 human surface opens in VS Code, not the cloud

## Problem / motivation

The Tier-4 human-facing visualization surface has drifted between two candidate forms. Intake doc #4
§S4 (Arc-5 pilot follow-ups) recommended **Artifacts pages** (claude.ai-hosted) as the surface, and
#264 parks `mermaid_emit.py` pending a build-vs-park decision. This session the operator gave a
**direction**: the Tier-4 surface should be **local HTML** — a file openable **inside VS Code
in-session** — **not** cloud artifact pages. The itch: a cloud-hosted surface sends repo-derived
content to claude.ai hosting (a per-surface data-classification call) and lives outside the operator's
in-editor loop; a local HTML file stays in the working tree, opens in-session, and carries no
publishing boundary. Without capturing this direction, #264's re-scope and the Arc-5 P6 pilot would
proceed on the Artifacts assumption the operator has now countered.

## Scenarios (+1 view)

- As the operator I open a generated dashboard as a **local `.html` file inside VS Code**, in the same
  session, without publishing anything.
- As the operator the dashboard renders from repo-derived data (fleet health, operator-load, conformance)
  with **zero external hosting** and zero data leaving the machine.
- As the operator, when I *want* to share, that is a **separate explicit act** — the default surface is
  local and private-by-construction.
- As the operator I want #264's visualization decision and the Arc-5 P6 pilot to **target local HTML**,
  so the evidence they gather is for the surface I actually chose.

## Functional requirements

- **Must:** the Tier-4 human visualization surface is **local HTML** — a file openable inside VS Code
  in-session, **self-contained** (renders with no external host and no CDN dependency for the data).
- **Must:** generation writes into the **repo/working tree** (a committed-generated or gitignored local
  artifact), **not** to claude.ai hosting.
- **Should:** the surface **re-scopes #264** (`mermaid_emit` wiring) and provides the **Arc-5 P6 pilot's
  evidence target**.
- **Should:** no repo-derived content is **published by default** — sharing is a separate explicit
  operator act.
- **Could:** reuse the existing emitters (`text_emit` / `mermaid_emit`) where content is genuinely
  graph-shaped, embedded in the local HTML.

## Acceptance criteria (ex-ante)

1. A generated dashboard **opens as a local `.html` file inside VS Code** and renders correctly with **no
   network fetch** required — verified by opening it offline.
2. Generation produces the file **in the working tree** (path recorded) and **publishes nothing** to any
   external host — verified by the absence of any hosting/upload step.
3. **#264 is re-scoped in writing** to target local HTML (build-vs-park decision recorded against this
   surface) **and** the Arc-5 P6 pilot's evidence target is restated as local HTML — verified against
   #264 + the Arc-5 plan.
4. The surface renders in **both VS Code light and dark themes** (theme-aware), matching the operator's
   in-editor context.

## Non-goals

- Does **not** adopt claude.ai Artifacts as the default Tier-4 surface — this doc **counters** intake doc
  #4 §S4's Artifacts recommendation.
- Does **not** forbid sharing — it makes local-and-private the **default**, sharing an explicit separate act.
- Does **not** decide the graph-vs-flat content split for `mermaid_emit` (that is #264's technical call) —
  only the surface **medium**.
- Does **not** build the dashboards' data pipelines (fleet_health / operator-load / conformance already
  have their own items).

## Impact sketch (4+1 lite)

- **Logical:** fixes the Tier-4 surface **medium** as local HTML; supersedes the Artifacts-page candidate.
- **Process:** dashboards enter the **in-editor session loop** rather than a publish-then-view loop.
- **Development:** re-scopes #264; sets the Arc-5 P6 pilot target; may rewire `mermaid_emit` for embedded
  graph content.
- **Physical:** a local `.html` artifact in the working tree; **no claude.ai hosting**; theme-aware for
  VS Code.

## Open questions

- **Committed-generated vs gitignored** for the local HTML artifact (the ADR-80 writer-policy question)?
  (technical-architect.)
- Which dashboards are in scope first — fleet health, operator-load (#270), conformance (#171)?
- Does any genuinely graph-shaped content still justify `mermaid_emit`, or does local HTML render it
  natively (the #264 narrow-vs-retire call)?
- How is "opens inside VS Code" delivered (a Simple Browser preview, an external-file open) — a
  technical-factual item, recorded not answered.

## Status

SEED — captured 2026-07-08 from operator direction (this session). Feeds the #264 re-scope, counters
intake doc #4 §S4, and sets the Arc-5 P6 pilot's evidence target. Awaiting technical triage.
