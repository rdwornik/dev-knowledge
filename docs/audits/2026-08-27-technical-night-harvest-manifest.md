# CLOUD-NIGHT MANIFEST — harvest of 2026-08-26

Harvested read-only from the Anthropic cloud API via `DispatchHelpers`
(`GET /v1/code/sessions/{cse_id}/events?sort_order=asc`, paginated by `next_cursor`).
All four sessions were COMPLETE at first wake (45 min). No second sleep was needed.
Nothing was written to any repo; these five files are the only artifacts.

---

## Reports

**1. night c1 doc-diet**
- file: `CLOUD-NIGHT-C1-RESULT.md`
- bytes: 22620
- first heading: `CLOUD-NIGHT-C1 — DOC-DIET EXECUTION PLAN (read-only)` (line 4, inside the report's own code fence; the file opens with a one-line preamble, see Verification)
- top recommendation: Run the doc diet as four sequenced lanes and do the purely mechanical PLAYBOOK correction step FIRST — it discharges 17 of the 19 census findings without moving a single heading, because a structural diet run first would silently discard those corrections.

**2. night c2 kodeks**
- file: `CLOUD-NIGHT-C2-RESULT.md`
- bytes: 16429
- first heading: `# CLOUD-NIGHT-C2 — Python-standards kodeks: the hub measured against its own North Star`
- top recommendation: Adopt Option C — split the Python standard on enforceability, putting every ruff-decidable clause into `[tool.ruff.lint]` pinned as a fifth MUST-uniform parity surface while carrying the three ruff-unrepresentable items (Click, Rich, dataclasses-over-dicts) as doc-level intent rather than building a new hub checker, starting with the free ratchet of the twelve zero-cost rule families.

**3. night c3 rotation**
- file: `CLOUD-NIGHT-C3-RESULT.md`
- bytes: 18019
- first heading: `CLOUD-NIGHT-C3 — APPEND-ONLY SURFACES ROTATION (RECON)` (line 4, inside the report's own code fence; the file opens with a one-line status banner, see Verification)
- top recommendation: Take option (a-prime) — rotate the FILE, not the PREDICATE: make `journal_anchor.journal_text()` tile `JOURNAL.md` with sorted `JOURNAL-legacy-*.md` so the gates' universe is unchanged by construction, landing that seam first as a commit that moves zero bytes and needs no governance act.

**4. night c4 backlog census**
- file: `CLOUD-NIGHT-C4-RESULT.md`
- bytes: 25156
- first heading: `# CLOUD-NIGHT-C4 — Backlog quality census (read-only)`
- top recommendation: Rule the top-40 kill list and run the 45-day icebox sweep (47 rows, honouring the `[#210]` and `[#242]` carve-outs) while adopting the 17 inferred dependency edges — but re-peg dependents BEFORE closing anything, since 9 already-deferred rows hang off pegs pointing straight into the kill list.

---

## PENDING

None. All four sessions had delivered their report before the first wake.

---

## Verification

- All four files exist, are non-empty, and are byte-for-byte the session's own report text (written verbatim, UTF-8 without BOM).
- C2 and C4 satisfy "starts with the report's own heading" literally — byte 0 is `# CLOUD-NIGHT-C…`.
- C1 and C3 DO NOT. Each session wrapped its report in a code fence preceded by one line of prose
  ("Read-only pass complete. Report follows…" / "**RECON COMPLETE — read-only…**"), per the repo's own
  §4 output-formatting convention. The heading is line 4 in both. The text was written verbatim rather
  than trimmed to force the check to pass; the deviation is recorded here instead.
- Report text was selected as the longest assistant text in each session. In all four this is assistant
  text #2, immediately after the RECEIPT. The LAST assistant text in each session is NOT the report —
  it is trailing Stop-hook backpressure noise ("Unchanged. Done.", "Nothing further.") from a container
  where `uv run --locked` could not start (uv 0.8.17 vs the pinned 0.11.19).
