# LANE lane-b-614-vision-to-readme — Execute the ruled VISION to README supersession, re-pointing every gate-coupled consumer enumerated from the C5 census.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-b-614-vision-to-readme LANE-b-614-vision-to-readme.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #614 · lane-b-614-vision-to-readme]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-b-614-vision-to-readme` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-b-614-vision-to-readme` -> branch `worktree-lane-b-614-vision-to-readme` -> contract `LANE-b-614-vision-to-readme.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

`README.md` (new) · `VISION.md` · `CLAUDE.md` (§5 rule 5 ONLY) · `ARCHITECTURE.md` ·
`scripts/canonical_docs.py` · `scripts/validate_hermetization.py` ·
`scripts/audit_checks/check_adr38_baseline.py` · `ecosystem/parity-surfaces.yaml`

**CLAUDE.md is shared with lane-c and this lane goes FIRST** — it edits §5 rule 5, which lane-c's
re-genre then inherits. The two are serialised, never parallel.

## Done-contract (immutable)

1. **The enumeration is the lane's FIRST ARTIFACT, not an implementation detail.** Every
   gate-coupled consumer is enumerated from the C5 census
   (`docs/audits/2026-08-29-census-nb2-readme-vision.md`) **before any edit** — ADR-114
   AMENDMENT 1 says this verbatim.
2. **The P1a boot probe is re-pointed, then EXECUTED against the new `README.md`, with its output
   pasted into the lane packet** — architect CUT-5. The probe is located and named in
   `docs/audits/2026-08-29-census-nb2-readme-vision.md`; it greps `VISION.md`'s opening line. A
   re-point that reads correctly in a diff and fails at boot is exactly what running it refuses.
3. **`ARCHITECTURE.md` Ch1's Layer-2 line (P1b) survives VERBATIM** — architect CUT-5 standing
   guard. Byte-identity, not paraphrase.
4. All **nine** ADR-104 fleet members' `canonical-doc-vision` parity MUST row resolved in ONE act
   (`tier: {hub: MUST, consumer: MUST}` — a partial resolution breaks parity fleet-wide).
5. **ZERO immutable or append-only files edited.** Per
   `docs/audits/2026-08-29-census-nb2-readme-vision.md`: ~5,881 references, ~5,700 in files the
   repo forbids editing, and a mergeable surface of five lines in one file.
6. ADR-114's three named decommission surfaces each become a backlog row.
4. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. **Enumerate** every gate-coupled consumer from the C5 census. This artifact lands before any
   edit. **COMMIT**
2. Create `README.md`, migrate live-normative content, re-point the consumers, resolve the
   nine-member parity row in one act. **COMMIT**
3. **Run the P1a boot probe against the new README** and paste its output verbatim. Confirm P1b
   is byte-identical. **COMMIT**
4. Final: targeted tests green, one end-of-lane artifact, **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
