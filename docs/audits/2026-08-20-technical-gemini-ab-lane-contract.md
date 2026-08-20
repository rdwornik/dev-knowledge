# NIGHT LANE — GEMINI 3.7 FLASH A/B ON THE C1 SEEDED-DEFECT PACK

> **Contract of record** (ADR-110). Landed as the first commit of the lane
> `worktree-night-ab-gemini-2`, before any work. Two parts: §A the frozen contract
> verbatim as pasted, §B the binding addendum verbatim as pasted. The addendum
> **supersedes on contact**.
>
> This is the SECOND slot against this contract. The first
> (`docs/night-ab-gemini-2026-08-20`, contract at `7ce4aedc`) stopped at precondition P1;
> its artifact is `docs/audits/2026-08-20-technical-gemini-ab-results.md` on that branch.
> The addendum below is the operator's response to that stop.

---

## §A — the frozen contract, verbatim

```
# NIGHT LANE — GEMINI 3.7 FLASH A/B ON THE C1 SEEDED-DEFECT PACK

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Worktree lane, commit-and-STOP.** ADR-110: commit this prompt first as
`docs/audits/2026-08-20-technical-gemini-ab-lane-contract.md`.

CONTEXT: the acceptance pack is on main: `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`
(869 lines — read it in full). The admission bar is RULED: `ADMIT iff G1 and G2 and G3`, no partial
admission. New-model routing changes happen only through this measured acceptance.

STEPS:
1. Fill the §4.2 FILL-IN invocation lines: incumbent fan-out CLI vs the Gemini CLI with the
   Gemini 3.7 Flash model as available on this machine. Record both exact command lines in the
   artifact. If the Gemini CLI is absent or cannot select 3.7 Flash, STOP with the wall verbatim —
   do not substitute another model.
2. Run ALL 14 pack items on BOTH sides, capturing raw outputs verbatim per item.
3. Score mechanically per the pack rubric: G2 (fabrication: Phi_c <= Phi_i AND Phi_c = 0 on trap
   items C1-R4/C1-R5) and G3 (correctness: P_c >= P_i, ties admit) where the rubric is mechanical.
4. The two refusal items C1-N1 and C1-N2: capture raw outputs VERBATIM and DO NOT score them — the
   architect scores rulings by hand. Leave G1 marked ARCHITECT-PENDING.
5. Artifact `docs/audits/2026-08-20-technical-gemini-ab-results.md`: both invocation lines, the full
   per-item result table, computed G2/G3, raw N1/N2 outputs, and NO admit/refuse verdict — the
   verdict is the architect's.
FINAL: targeted checks, commit-and-STOP. NOT: no routing-table edits, no verdicts, no re-runs to
improve a score (first run counts; a rerun requires a named mechanical failure).
```

---

## §B — the binding addendum, verbatim (supersedes on contact)

```
Read C:\Users\1028120\Downloads\NIGHT-AB-gemini.md in full and execute it as your frozen lane
contract, WITH THIS BINDING ADDENDUM (supersedes on contact): (STEP 0, before anything) AUTH
REPAIR - inspect C:\Users\1028120\.gemini\settings.json AND any .gemini\settings.json left in the
abandoned worktree-night-ab-gemini checkout: a previous session wrote selectedType gemini-api-key
there in violation of the standing auth ruling. If the HOME file carries gemini-api-key selection,
quote it verbatim in your artifact, then set the selection to the CLI's subscription-OAuth value
(the login-with-Google / oauth-personal class enum its own docs name) and report before/after; the
abandoned worktree copy you only report, never fix (it dies at teardown). (AUTH RULING, absolute)
subscription OAuth with the operator's existing Google login ONLY - never set, request, or use any
API key; if an interactive browser login step is unavoidable, PAUSE with the exact command and what
the operator will see. (KNOWN RESULT to carry) agy is present and HONESTLY REFUSES gemini-3.7-flash
(model not served) - record its exact refusal output as the P-item result for agy. (FALLBACK ORDER)
upgraded gemini CLI: npm i -g @google/gemini-cli@latest, then the substitution probe - -m
gemini-3.7-flash must be HONOURED per -o json stats.models; only on a clean probe run the 14 pack
items. If the upgraded CLI on OAuth also refuses or silently substitutes, STOP with both walls
verbatim - never run a substitute model, never touch an API key. First commit = contract-of-record;
work only inside your worktree; commit-and-STOP.
```

---

## §C — how the two parts bind, as this lane reads them

1. **STEP 0 runs before anything else**, including before the pack is read.
2. **The auth ruling is absolute and outranks the fallback order.** No API key is set,
   requested, or used on any lane — including the diagnostic `models?key=` listing the
   first slot used. If the only way past a wall is a key, the wall stands.
3. **The fallback order is a gate, not a menu.** The upgraded CLI's substitution probe
   must be *honoured* per `-o json` `stats.models` before any pack item is invoked. A
   refusal or a silent substitution ends the lane with both walls recorded verbatim.
4. **`agy` is a P-item result to record, not a lane to run.** Its honest refusal is
   evidence about model availability, not a substitute candidate.
5. §A's "no re-runs to improve a score" stands: the first clean run counts.

---

**Class:** technical (ADR-101 enum) · **Date:** 2026-08-20 · **Slug:** gemini-ab-lane-contract
**Branch:** `worktree-night-ab-gemini-2` · **Mode:** worktree lane, commit-and-STOP
