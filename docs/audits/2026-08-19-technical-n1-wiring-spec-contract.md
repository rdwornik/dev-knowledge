# N1 dispatch stamp — [#529]/[#530] wiring spec (batch-2 L2 prep)

- **Lane:** NIGHT N1 — cloud channel (`claude/*`), read-only + drafts
- **Branch:** `claude/wiring-spec-telemetry-flight-o7oja9`
- **Dispatched:** 2026-08-19 (night lane; artifact dated 2026-08-19 per the brief)
- **Deliverable:** `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md`
- **Purpose of this file:** first-commit dispatch stamp. A night lane that dies must be
  distinguishable from one that was never dispatched. This file is committed BEFORE any
  other work; its presence with no sibling deliverable means the lane was dispatched and
  died mid-flight.

## Environment honesty header

Recorded per the brief's instruction ("if the environment cannot run repo gates … record
that state in the artifact header honestly; never bypass a gate that does run"). The
measured state of this channel is recorded in the **deliverable's** header block, taken
live rather than assumed, and the same statement is reproduced here on completion.

## Verbatim dispatch prompt

```
NIGHT N1 — [#529]/[#530] WIRING SPEC (batch-2 L2 prep) · cloud, read-only + drafts
You are a night research lane on the claude cloud channel. FIRST COMMIT = a dispatch-stamp: commit this prompt as `docs/audits/2026-08-19-technical-n1-wiring-spec-contract.md` on your `claude/*` branch before any other work — a night lane that dies must be distinguishable from one never dispatched. If the environment cannot run repo gates (known uv-pin issue on this channel), record that state in the artifact header honestly; never bypass a gate that does run. You draft; you change no behavior: no edits to scripts/ code, no BACKLOG/tasks writes.
CONTEXT: `[#529]` (telemetry_emit) and `[#530]` (single_flight) are BUILT-UNWIRED — zero non-test import sites. Tomorrow's Lane L2 wires them; tonight you produce the spec that makes that lane a bounded, well-specified build. `audit-py` serialize-group: the wiring will land AFTER today's `[#533]` leg 2 merge (f4a01f0e) — read the merged runner as it now exists.
ITEMS (CLEAR/BLOCKED line each):

1. Call-site derivation. For each library: read its docstring/API and the rows' Done-when; enumerate the exact insertion points (file:line, function) where wiring belongs, with a one-line why per site. Respect the decomposed registry + CHECK_ORDER emission.
2. Config surface. What must be configurable (emit destination, flight scope) — YAML/CLI, never hardcoded; name the existing config surface it joins.
3. PINNED-BY-TESTS list. Every test that pins the surfaces you'd touch (grep monkeypatch + direct asserts); per pin: touched-or-avoided.
4. Test plan. Test-first cases for the wiring (emission happens, single-flight dedupes, parity with unwired behavior where required), named target test files (NEW files only — tests/test_audit.py is the seam leg's, untouchable).
5. Draft lane contract for L2 in the house pattern (frozen contract, steps with COMMIT markers, decision budget, WHAT NOT TO DO) — as a fenced block inside the artifact.

OUTPUT: `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md` — items 1–5 + commands verbatim. Commit, push your claude/* branch, STOP packet (5 CLEAR/BLOCKED lines + shas). NOT: no wiring itself, no dependency changes, no verdicts on adoption, no merge.
```

## Scope fence (restated from the prompt, as the lane's own refusal list)

- NO wiring itself — this lane emits a spec, not an import site.
- NO dependency changes.
- NO verdicts on adoption.
- NO merge.
- NO edits to `scripts/` code.
- NO `BACKLOG.md` / `tasks/` writes.
