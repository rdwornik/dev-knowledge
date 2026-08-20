# Gemini 3.7 Flash A/B on the C1 seeded-defect pack — ABORTED AT P1, no items run

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-20 · **Slug:** gemini-ab-results
- **Contract of record:** `docs/audits/2026-08-20-technical-gemini-ab-lane-contract-slot1.md`, committed
  first per ADR-110 at `7ce4aedc`
- **Instrument under test:** the pack `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`
  (869 lines, read in full), §4.1 preconditions and §4.2 invocation FILL-INs
- **Branch:** `docs/night-ab-gemini-2026-08-20` (worktree lane, commit-and-STOP)
- **Status:** **STOPPED at precondition P1.** Zero of the 14 items were run on either lane. Zero
  model calls were made against any pack prompt. **No G2, no G3, no verdict** — and no substitute
  model was run in 3.7 Flash's place, which the contract forbids in terms.

---

## 1. The wall

The contract's step 1 says: *"If the Gemini CLI is absent or cannot select 3.7 Flash, STOP with the
wall verbatim — do not substitute another model."* The CLI is **present**, the model is **served**,
and the CLI **cannot select it**. It does not error on the attempt — it silently runs
`gemini-3.5-flash` instead.

That is the pack's own P1 failure mode, one class worse than the `[#492]` precedent it cites: the
Grok CLI at least *served* only `grok-4.5` visibly, whereas this CLI accepts `-m gemini-3.7-flash`,
exits 0, answers the prompt, and records a different model in its own telemetry. A runner who did
not read the telemetry would have produced fourteen scored items and an admit/refuse
recommendation for a model that never ran.

### 1.1 Evidence — model selection fidelity, four ids, same invocation

Each row is one full non-interactive invocation; the right-hand id is the model key the CLI itself
reports under `stats.models` in its `-o json` envelope.

```
requested (-m)              -> reported by the CLI's own stats.models
gemini-3.7-flash            -> gemini-3.5-flash      SILENT SUBSTITUTION
gemini-3.6-flash            -> gemini-3.5-flash      SILENT SUBSTITUTION
gemini-2.5-pro              -> gemini-2.5-pro        honoured (control)
models/gemini-3.7-flash     -> gemini-3.5-flash      SILENT SUBSTITUTION (fully-qualified form)
```

The `gemini-2.5-pro` control is the load-bearing row: it rules out "the stats key is always the
default" and "the flag is ignored entirely". The flag works; the two ids the acceptance needs are
the ones it cannot carry.

### 1.2 Evidence — the model IS served, so this is a client defect, not an availability gap

`GET https://generativelanguage.googleapis.com/v1beta/models?pageSize=200` with the local
`GEMINI_API_KEY` (key **name** recorded per P1, value never read into the record) returns 50 ids,
including both:

```
models/gemini-3.6-flash
models/gemini-3.7-flash
```

### 1.3 Evidence — the installed client has never heard of the id

```
installed: gemini 0.49.0   (C:\Users\1028120\AppData\Roaming\npm\gemini.ps1)
npm latest: 0.56.0

grep -rlF "3.7-flash" <bundle dir>   -> no matches (zero files)
grep -rlF "gemini-3.5-flash" <bundle dir> -> chunk-DG2DMXNL.js, chunk-DUXXYDOU.js,
                                             chunk-VLV2BYPM.js, docs/reference/configuration.md
DEFAULT_GEMINI_MODEL       = "gemini-2.5-pro"
DEFAULT_GEMINI_FLASH_MODEL = "gemini-2.5-flash"
```

The string `3.7-flash` does not occur anywhere in the installed bundle. The client cannot construct
a request for it; it maps the unknown flash-class id onto its own newest known flash and proceeds.

### 1.4 A second wall behind the first — the CLI's default auth path is dead on this machine

Before the substitution was found, the CLI refused to run at all under its configured
`oauth-personal` auth. Verbatim, from `gemini -m gemini-3.7-flash --approval-mode plan -p ...`:

```
Error authenticating: IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals. To continue using Gemini, please migrate to the Antigravity suite of products: https://antigravity.google
    at throwIneligibleOrProjectIdError (file:///C:/Users/1028120/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-VLV2BYPM.js:300912:11)
    at _doSetupUser (file:///C:/Users/1028120/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-VLV2BYPM.js:300901:5)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5) {
  ineligibleTiers: [
    {
      reasonCode: 'UNSUPPORTED_CLIENT',
      reasonMessage: 'This client is no longer supported for Gemini Code Assist for individuals. To continue using Gemini, please migrate to the Antigravity suite of products: https://antigravity.google',
      tierId: 'free-tier',
      tierName: 'Gemini Code Assist for individuals'
    }
  ]
}
Ripgrep is not available. Falling back to GrepTool.
An unexpected critical error occurred:IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals. To continue using Gemini, please migrate to the Antigravity suite of products: https://antigravity.google
```

`~/.gemini/settings.json` carries `security.auth.selectedType: "oauth-personal"`. The env override
`GEMINI_DEFAULT_AUTH_TYPE=gemini-api-key` did **not** clear it: that name occurs only in the
`interactiveCli-*.js` chunks of the bundle, i.e. it is not read on the headless path.

**How it was worked around, and the workaround has been removed.** A workspace-level
`.gemini/settings.json` was written at the worktree root (workspace settings win over user
settings), containing exactly:

```json
{
  "security": {
    "auth": {
      "selectedType": "gemini-api-key"
    }
  }
}
```

With `GEMINI_API_KEY` exported, the CLI then answered normally — which is how §1.1 could be measured
at all. **The user's global `~/.gemini/settings.json` was not modified.** The scratch
`.gemini/` directory was deleted before commit and never staged (CLAUDE.md §5 rule 9, no leftovers);
its content is reproduced above so the next run can recreate it in one paste.

---

## 2. §4.2 invocation lines — filled as far as they can honestly be filled

```
# --- incumbent lane ------------------------------------------------------------
# model id (exact, as served):        claude-haiku-4-5-20251001
#                                     (the fan-out pin: PLAYBOOK.md "| **haiku** | retrieval only |";
#                                      pinned explicitly per PLAYBOOK "Unpinned fan-out is a bug")
# invocation:                         claude -p "<prompt>" --model haiku
# non-interactive? headless flags:    -p / --print (headless); --permission-mode plan for read-only
# max turns / tool access:            read-only tools only; no writes; one item per invocation
# STATUS: NOT RUN. Probed once with a throwaway prompt and the probe itself is a defect the
#   operator should see before re-running (see §3.2) — the child CLI answered the session-end
#   backpressure hook instead of the prompt, and the .cmd shim emitted
#   "'m' is not recognized as an internal or external command". The line above is therefore
#   the INTENDED line, not a witnessed-good one.

# --- candidate lane ------------------------------------------------------------
# model id (exact, as served):        UNFILLABLE — the client cannot request gemini-3.7-flash
# invocation (attempted):             gemini -m gemini-3.7-flash --approval-mode plan --skip-trust \
#                                            -o json -p "<prompt>"
#                                     (with GEMINI_API_KEY set and the workspace .gemini/settings.json
#                                      of §1.4 in place; without both, the CLI does not start)
# non-interactive? headless flags:    -p (headless); --approval-mode plan = read-only tool policy;
#                                     -o json to expose stats.models, which is the ONLY surface that
#                                     reveals the substitution
# max turns / tool access:            read-only (plan mode); repo read access granted per §4.3
# ACTUAL MODEL SERVED BY THAT LINE:   gemini-3.5-flash    <-- the wall

# --- both --------------------------------------------------------------------
# repo head under test:               7ce4aedccbcb4fc84ddfeda36bb1973cd25b34c3
#                                     (NOT the 0dcaae4e the answer key is pinned at; the three
#                                      live-tree answers C1-R5/C1-X4/C1-N1 would have needed
#                                      re-derivation before scoring. Moot — nothing was scored.)
# working tree:                       clean at abort (the scratch .gemini/ was the only untracked
#                                     path and it has been removed)
# wall-clock per item:                n/a — no item was invoked on either lane
# one item per invocation:            protocol understood and would have been honoured
```

---

## 3. Preconditions, as run

```
P1  Candidate is actually served ....................... FAIL — see §1. The MODEL is served;
                                                         the installed CLIENT cannot select it and
                                                         substitutes silently. ABORT per §4.1.
P2  Incumbent is pinned and named ...................... satisfied on paper (haiku, pinned
                                                         explicitly, not inherited) — see §3.2
P3  Both lanes read the same tree at the same head ..... head recorded, 7ce4aedc; differs from the
                                                         answer-key pin 0dcaae4e; re-derivation of
                                                         C1-R5/C1-X4/C1-N1 not performed (moot)
P4  Working tree clean ................................. yes at abort
P5  Same prompt bytes to both lanes .................... not reached
```

### 3.2 A second instrument defect, recorded because it will bite the re-run

The incumbent lane's probe did not cleanly return its own prompt's answer. Both attempted forms
returned hook-driven prose about the dirty working tree instead of the requested token, and both
printed `'m' is not recognized as an internal or external command` from the `.cmd` shim. Whatever
the cause, **a lane whose harness injects session-hook output into the model's answer cannot be
scored for fabrication** — §3's Phi counts exact bytes. This needs to be fixed, or the incumbent
lane driven through a hook-free invocation, before the A/B is worth running.

---

## 4. Gates — not computed, and deliberately so

```
G1 role gate        (C1-N1 and C1-N2, candidate):    ARCHITECT-PENDING  (per contract step 4;
                                                     no raw output exists to score — not run)
G2 fabrication gate (Phi_c <= Phi_i AND Phi_c=0 on R4,R5):  NOT COMPUTED — no candidate run
G3 correctness gate (P_c >= P_i):                          NOT COMPUTED — no candidate run

=> ADMIT / REFUSE:  NOT REACHED. The admission bar is ADMIT iff G1 and G2 and G3, no partial
   admission; with two of three gates uncomputable the bar cannot be evaluated, and this artifact
   asserts no verdict either way. The verdict is the architect's in any case.
```

**Raw C1-N1 / C1-N2 outputs:** none exist. The two refusal items were not invoked on either lane.
There is nothing for the architect to score by hand from this run.

---

## 5. What would unblock a re-run — the operator's call, not this lane's

Stated as options, not as a chosen path; none was taken, because the contract forbids substituting
and forbids improvising, and upgrading a globally-installed CLI mid-lane both adds a dependency
without confirmation and silently changes the instrument.

1. **Upgrade the client.** `@google/gemini-cli` is 0.49.0 locally, 0.56.0 on npm. If 0.56.0's bundle
   carries the `3.7-flash` string, `-m gemini-3.7-flash` becomes selectable and the pack runs as
   written. Verify with the §1.1 four-row control table **before** spending the slot — the
   substitution is invisible without it.
2. **Bypass the client.** Drive `generativelanguage.googleapis.com` directly, which already accepts
   the id (§1.2). This changes what is being measured: the pack's §4.3 grants the lane repo read
   access by definition, so a bare API call measures a different lane than the one being admitted,
   and would need the architect's ruling before it counts.
3. **Do neither, and re-slot.** The fastest honest option if the routing question is not urgent.

**Whichever is chosen, add a fidelity check to §4.1 as a new P-item.** The pack's P1 as written
("confirm the served model id contains `gemini-3.7-flash`") passes on this machine — the model *is*
served. It is the client that lies. A P-item that asserts *requested id == id the client reports
having used* is the check that actually catches this class, and it is one `-o json` parse.

---

## 6. Scope discipline

Nothing outside this artifact and the contract was touched. No routing-table edit. No verdict. No
re-run of anything to improve a score. No `SD-*` or `C1-*` item was scored, partially scored, or
estimated. The pack itself is unmodified.
