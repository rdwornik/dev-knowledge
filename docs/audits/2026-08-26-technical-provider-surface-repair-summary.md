# Provider-surface repair — DERIVED SUMMARY (redacted)

**Class:** technical · **Measured:** 2026-08-26 · **Landed:** 2026-08-26 (endgame governance session)

> **REDACTION NOTICE — read before citing this file.**
> This is a **derived summary**, not the source report. The source
> (`PROVIDER-SURFACE-REPAIR-REPORT.md`, operator-side, 2026-08-26) is **deliberately not landed
> byte-identical**, under WINDOW-RECORD Part V.b row L8 and the endgame brief's absolute L8
> privacy rule. **Removed here and nowhere recoverable from this file:** the operator's
> organisation identity, any email address, and the **credential-location map** — the loader
> profile paths, the secrets-file path, and the per-provider config-root column of the source's
> truth table. **No credential VALUE appears in the source or here**; the source's own risk was
> identity and credential-*location* disclosure, which is what this redaction removes.
> What is preserved is exactly what the registry and the wave-2 provider rows need: presence,
> auth state, the blocked-with-cause/absent distinction, and the mechanism findings.
> The source remains available to the operator outside the repo.

---

## 1 · Headline — two findings that contradicted the commissioning brief

**(a) The permanent credential fix is an OPERATOR act, not an agent act.** The environment loader
that exports the two billing-relevant variables is not a repo file: it is a pair of PowerShell
profiles inside the **absolute exclusion zone**. Writing there is barred four independent ways —
the P0 rule, the consumer repo's `core-invariants` T2 (which states that *no grant mechanism
exists in code* for such writes), a `PreToolUse` block hook, and the session sandbox. The lane
therefore **measured every entry point, produced the exact two-line patch, and landed a failing
check** — but could not apply the fix. That is the correct outcome, not a shortfall.

**(b) The current override is `CLAUDE_CODE_OAUTH_TOKEN`, not `ANTHROPIC_API_KEY`.** A hand-written
`claude.cmd` shim on PATH already strips `ANTHROPIC_API_KEY` from the child process, so
`claude` currently reports `authMethod: "oauth_token"` rather than `"Claude API"`. **The billing
hole the brief described is real but presently plugged by a fragile band-aid**, which is also the
source of the separate stderr-noise item. **Sequencing is load-bearing: removing the shim before
fixing the profile makes billing worse, not better.**

### The measurement, as presence booleans only (no value was ever read or printed)

| Shell | `ANTHROPIC_API_KEY` | `CLAUDE_CODE_OAUTH_TOKEN` |
|---|---|---|
| pwsh 7, profile loaded | **present** | **present** |
| Windows PowerShell 5.1, profile loaded | **present** | **present** |

With **both names removed from the process environment only**, the same shell reports
`authMethod: "claude.ai"`, `subscriptionType: "max"`. **The subscription was never lost — the
environment was overriding it.** A prior one-shell `Remove-Item` was a diagnostic, not a fix:
every new terminal still exports both.

This is the direct evidence base for **register ruling 7** (`ANTHROPIC_BASE_URL` /
`ANTHROPIC_AUTH_TOKEN` — and this same class of billing-relevant name — are never set globally).

---

## 2 · What the lane DID land: a check that fails honestly

A new **credential-scope** section was added to the consumer repo's existing drift checker, with a
forbidden-variable list defaulting to the two names, a skip switch, and a shell test seam.
Design points worth carrying into the hub's own equivalent:

- It **launches a real child shell** rather than reading its own environment. Reading the current
  process environment is the precise mistake that made a one-shell `Remove-Item` look like a fix,
  because the check is usually run from an already-scrubbed terminal.
- It probes **both PowerShell editions**, which load different profiles.
- The child's **baseline is scrubbed** before launch, so a hit proves the *profile chain* set the
  variable rather than the caller.
- `-NoProfile` is deliberately **not** passed — the profile is the thing under test — and
  execution policy is deliberately not overridden, since a policy that stops the profile also
  stops the leak.
- **It never reads or prints a value.** The child emits presence lines only, and a dedicated test
  asserts a planted secret never reaches stdout or stderr.
- **A probe that cannot run reports `info`, never a silent pass** — the green-without-predicate
  lesson (WINDOW-RECORD Part VII), applied.

Live result against the workstation: **exit 1, four credential-scope findings, no value printed.**
Eight new tests. **Two real bugs were caught by those tests**, both generalisable:
`pwsh -File` binds every argument as a **string**, so a hashtable seam arrived as text; and a
comma-separated list arrived as **one** string, so the check probed for a variable literally named
`"A,B"` and reported **all-clear** — a **false PASS**, the worst possible failure mode for a check
of this kind.

---

## 3 · Registry-ready truth table (config roots REDACTED)

Presence and auth state only. **Roles are R3's** — no role opinion is offered here.
`blocked-with-cause` vs `simply-absent` is the operative distinction.

| `cli` | Present | Auth state | blocked-with-cause vs absent | Measured |
|---|---|---|---|---|
| `claude` | **yes** — two installs, npm shim resolves first | `claude.ai` / **max** once both env names are unset; `oauth_token` otherwise | **blocked-with-cause** — env overrides subscription; cause named, fix specified, failing check landed | 2026-08-26 |
| `deepcode` (`@vegamo/deepcode-cli`) | **yes** — v0.3.1 | **unauthenticated** — no settings file written | **blocked-with-cause** — headless lane viable once configured | 2026-08-26 |
| DeepSeek vendor CLI | **no** | n/a | **simply-absent** — no vendor CLI exists | 2026-08-26 |
| `dsh` (`@deepseek-ai/dsh`) | **no** | n/a | **REJECTED-BY-FIT** (operator ruling) — a localhost web UI is the wrong model for a CLI lane; needs pnpm (absent); the npm route livelocked 46 min. **Not** "failed to install" | 2026-08-26 |
| `gemini` | **yes** — v0.56.0 | **server-refused** | **blocked-with-cause** — `IneligibleTierError`, `reasonCode: UNSUPPORTED_CLIENT` | 2026-08-26 |
| `agy` | **yes** — v1.1.20 | **working** — `agy models` returns a full list | **present, healthy** | 2026-08-26 |
| `grok` / `agent` | **yes** | not re-measured this pass | **present** — owns the bare name `agent` on this PATH | 2026-08-26 |
| `cursor-agent` | **no** | n/a | **blocked-with-cause** — the only documented Windows route force-copies `cursor-agent.*` to `agent.*`, claiming xAI's name; **not installed by rule** | 2026-08-26 |

This table is the evidence base for the WINDOW-RECORD Part VIII **I3** registry consequences:
`deepcode` as a third strict `AGENTS.md` provider, **Cursor recorded blocked-with-cause rather
than absent**, and **a measured-on date required for fast-moving third-party CLIs**.

---

## 4 · Per-item findings

- **`deepcode` is HEADLESS-CAPABLE — the make-or-break, and it passes.** `-x/--exec` with
  `-p/--prompt` runs one prompt non-interactively, and **stdin piping works**. **Machine-readable
  output: NO** — no JSON mode. **It moves fast:** two minor versions in a single day (0.1.33 to
  0.3.1), which is precisely why registry rows need a measured-on date. **Supply chain:** single
  unattributed maintainer, MIT, four months old, daily updates — R3 should rule before it is given
  a key and shell permissions.
- **`gemini` has changed failure class.** No longer a plain free-tier quota refusal but a
  **client-deprecation** refusal (`UNSUPPORTED_CLIENT`) demanding migration to another suite.
  **A tier upgrade alone would not necessarily revive this CLI** — so "wait for a tier change" is
  no longer a valid holding position.
- **The bare name `agent` belongs to xAI on this host** and was neither pinned, aliased, nor
  documented — Part IV ruling 6, honoured.
- **`DEEPSEEK_API_KEY` is not read by `deepcode`** — zero occurrences in the shipped package; it
  reads a generic key name from its own settings file.
- **Two brief items dissolved on measurement:** the orphaned npx lock was **not present** (nothing
  to delete), and the DeepSeek VS Code extension is **absent** (confirmed two independent ways).
- **The "duplicate Claude Code install" is not what it looks like** — both entries are the same
  version; the one that resolves first is a **hand-written batch shim**, not an npm shim, and it
  is the band-aid described in section 1(b).

---

## 5 · Open operator decisions carried forward (one line each)

1. Apply the two-line guard to both loader profiles — **only the operator can write there**; until
   then the drift check stays red and the subscription stays overridden.
2. Preferred additionally: **denylist the two names inside the key loader**, so a mid-session
   reload cannot re-export them.
3. **After (1) verifies**, remove the hand-written shim — **order matters**.
4. Cursor: choose among the three routes; the only viable install needs a drift guard.
5. `deepcode`: decide whether to configure it — one prompt settles whether it is genuinely
   unauthenticated; a lane also needs an explicit permissions block.
6. `deepcode` supply chain: R3 should rule before it gets a key and shell permissions.
7. `gemini`: decide whether to **retire the CLI** rather than wait on a tier change.

## 6 · Restraint record (what the lane deliberately did NOT do)

Did not modify or **read** either profile; did not delete the shim; did not install Cursor; did not
pin or document the bare name `agent`; did not run any DSH install route after the ruling; sent
**no paid request**; **printed, read or pasted no credential value**; left the secrets file
**byte-identical, hash-verified before and after**; and made **no hub writes** — no rows, no
registry edits. The hub-side consequences are the intakes and rows filed by this session instead.

---

**Provenance.** Derived 2026-08-26 by the endgame governance session from the operator-side report
`PROVIDER-SURFACE-REPAIR-REPORT.md` (measured 2026-08-26), under WINDOW-RECORD Part V.b row L8.
**Related landed evidence:** `docs/audits/2026-08-25-technical-probe-providers-report.md`,
`docs/audits/2026-08-25-technical-probe-dsh-report.md`,
`docs/audits/2026-08-26-technical-research-chinese-coding-models.md`.
**Consumed by:** the I3 provider-capacity intake filed by this session, and register ruling 7.
