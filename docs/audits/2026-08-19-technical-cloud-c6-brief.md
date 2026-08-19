# CLOUD C6 — TELEMETRY READ-PATH DESIGN MEMO ("where the operator sees the data") · read-only + drafts

Cloud lane. FIRST COMMIT = dispatch-stamp (this prompt as
`docs/audits/2026-08-19-technical-c6-telemetry-readpath-contract.md`). **No index regeneration,
no JOURNAL writes.** Drafts only.

CONTEXT: the emit side ([#529] telemetry / [#530] single_flight) is being wired TODAY by lane
L2. The read path was ruled **D3-first**, with datasette-vs-static-HTML deliberately deferred
"until #529 emits data" — that trigger fires at L2's merge. The operator's standing demand:
"gdzie w końcu będą wyniki tej telemetrii" — a place he OPENS and SEES.

ITEMS (CLEAR/BLOCKED each):
1. Read the N1 wiring spec (docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md) for
   the emit store's shape/path; state the exact data contract the read path consumes.
2. **Design the D3-first read page** (draft, fenced HTML/JS skeleton in the artifact): commit-tax
   over time, per-check timing distribution, WARN-class trend, closures-vs-births ledger line —
   four charts, self-contained file, zero external services. State how it coexists with lane
   K's dashboard (one page linking the other, no duplication — name which surface owns what).
3. **Datasette-vs-static decision memo**: both routes priced on OUR constraints (Windows
   operator console, no server appetite, corporate AppLocker precedent) — recommendation
   labelled LEAN, ruling stays with the architect.
4. **Draft the build-lane contract** (house pattern, fenced) for the read-path lane that
   dispatches after L2 merges — sized S/M, file-disjoint from K's dashboard.
OUTPUT: `docs/audits/2026-08-19-technical-c6-telemetry-readpath.md`. Commit, push, STOP packet.
NOT: no build, no dependency additions, no touching L2's files.
