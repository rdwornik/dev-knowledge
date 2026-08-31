# LANE batch-e-l-12-logs-retention-rule (HY-2) - dated logs into dated subfolders by a RETENTION RULE - a mechanism, not a one-off cleanup.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-l-12-logs-retention-rule LANE-l-12-logs-retention-rule.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-l-12-logs-retention-rule` -> branch `worktree-lane-l-12-logs-retention-rule` -> contract `LANE-l-12-logs-retention-rule.md`

## Write-scope (frozen)

- `logs/`
- `scripts/`  (the retention organ)
- `tests/`    (its fire-test)

## THE ONE THING THAT WILL BITE YOU

**`logs/TOKEN-LOG.md` IS STRICT APPEND-ONLY (ADR-29 / ADR-39) AND HAS NO ARCHIVAL EXCEPTION.**
The 2026-07-17 amendment that permits a byte-identical chronological relocation applies to
`LESSONS.md` ONLY - the register says so in as many words: *"`logs/TOKEN-LOG.md` stays strict"*.
**The one token log stays FLAT.** Moving it, splitting it or rotating it is a violation, not an
improvement.

## Done-contract (immutable)

1. **A RETENTION RULE, expressed as a MECHANISM** - dated logs land in dated subfolders because
   an organ puts them there, not because someone tidied once. A cleanup that leaves no rule
   behind will be re-needed next month and is not this lane's deliverable.
2. **The rule names what it EXCLUDES**, `logs/TOKEN-LOG.md` first among them, and a test proves
   the exclusion actually fires.
3. **Artifact naming stays honest** - `logs/` artifacts are UPPERCASE-KEBAB with an extension
   true to the format ([#395]).
4. **No log content is edited or deleted.** Relocation only, and only where the rule permits.

## Steps

1. Read ADR-29, ADR-39 and the ADR-29 2026-07-17 amendment before touching anything in `logs/`.
2. Write the fire-test FIRST (ADR-108 section B), including the TOKEN-LOG exclusion case.
3. Implement the organ. Run the TARGETED tests. Commit and STOP.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
