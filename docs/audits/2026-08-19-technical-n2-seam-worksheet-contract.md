# NIGHT N2 — [#533] seam-leg worksheet (25 monkeypatch pins) — contract of record

- **Date:** 2026-08-19 (dispatch date; lane ran 2026-08-18 cloud-night)
- **Class:** technical (ADR-101 §2 audit grammar)
- **Lane:** night research lane, Anthropic cloud channel — branch `claude/seam-leg-monkeypatch-pins-91fh27`
- **Mode:** read-only analysis + ONE artifact. No code edits, no test edits, no BACKLOG/tasks writes,
  no re-points executed, no extraction, no merge.
- **Governing row:** `[#533]` — the audit.py decomposition arc; leg 1 left 27 checks in the facade,
  leg 2 landed at `f4a01f0e` (verified ancestor of this branch's HEAD)
- **Output:** `docs/audits/2026-08-19-technical-n2-seam-worksheet.md`
- **ADR-110 requirement:** this file IS the frozen dispatch prompt, landed as the FIRST COMMIT of the
  lane, before any other work

## Dispatch prompt, verbatim

```markdown
NIGHT N2 — [#533] SEAM-LEG WORKSHEET (25 monkeypatch pins) · cloud, read-only
Night research lane, claude cloud channel. FIRST COMMIT = dispatch-stamp: commit this prompt as
`docs/audits/2026-08-19-technical-n2-seam-worksheet-contract.md` on your `claude/*` branch before
other work. Gates-unavailable state (uv-pin) recorded honestly if hit. Read-only analysis + one
artifact; no code edits, no test edits, no BACKLOG/tasks writes.
CONTEXT: `[#533]` leg 1 left 27 checks in the audit.py facade, blocked by three measured classes; the
largest is 25 checks whose tests monkeypatch closure names onto the `audit` module
(`_is_hub`/`_REPO_ROOT` alone = 19) — moving one detaches the seam SILENTLY. The seam leg re-points
those seams so extraction can resume. Read the tree as merged TODAY (leg 2 landed at f4a01f0e; 16/43
checks already in scripts/audit_checks/).
ITEMS (CLEAR/BLOCKED each):

1. Pin census. For each of the 25 pinned checks: test id · exact monkeypatched name(s) · what behavior
   the pin fakes · the check's future home module under the decomposition.
2. Re-point recipe per pin class. Group pins by mechanism (module-attr patch, closure capture, path
   constant); per class: the seam-preserving re-point recipe (e.g. patch the registry-owned symbol,
   dependency-inject, fixture) — recipes must keep the test's INTENT byte-equivalent; call out any pin
   whose re-point would weaken what it guards.
3. The other two classes. `_gitenv` position-dependent load (check_handoff_probes) and the
   landing-predicate N-1 naming scripts/audit.py (check_import_edges): one paragraph each on the
   unblock shape and who must rule.
4. Risk-ranked extraction order. Which checks become extractable after which re-points — a
   dependency-ordered queue for the seam lane.
5. Draft seam-lane contract (house pattern) as a fenced block — scope strictly tests/test_audit.py +
   the re-point targets; parity-with-before proof named.

OUTPUT: `docs/audits/2026-08-19-technical-n2-seam-worksheet.md`. Commit, push, STOP packet.
NOT: no re-points executed tonight, no extraction, no merge.
```

## Lane constraints restated (binding)

1. **Read-only.** The only files this lane writes are this stamp and the named worksheet. No
   `scripts/`, no `tests/`, no `BACKLOG.md`, no `tasks/`.
2. **Tree as merged today.** All measurements are taken against this branch's checkout, which
   contains `f4a01f0e` (leg 2). Counts stated in the worksheet are measured, never inherited from
   the dispatch text — where the dispatch's own numbers disagree with the tree, the measurement wins
   and the disagreement is recorded.
3. **CLEAR/BLOCKED per item.** Each of the five items carries an explicit verdict.
4. **Gates-unavailable state recorded honestly.** If the uv-pinned toolchain makes a gate
   unrunnable in this container, the worksheet says so rather than implying a green run.
