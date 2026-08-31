# CODESPACE ADMISSION PROBE — batch E §1(C). VERDICT: RED. Committing lanes stay LOCAL.

> **Consumed by:** batch E's freeze (`docs/audits/2026-08-31-technical-batche-launch-contracts/CUT.md`
> and `PLAN.md` §U-8), ruling Z-G3's conditional-default clause, and `[#593]` / `[#616]`.
>
> Run 2026-08-31 on operator instruction, in parallel with the architect's cut. Fresh codespace
> `batche-c-admission-pgw54jqwv7qf65rj`, `basicLinux32gb`, branch `main`, idle 30m / retention 24h.
> Provision 6s, run 44s. **Stopped immediately on the RED verdict** — compute billing ended
> 2026-08-31T17:45:48+02:00; storage remains until the 24h retention or an explicit
> `gh codespace delete -c batche-c-admission-pgw54jqwv7qf65rj`.

---

## THE THREE RECEIPT LEGS, REPORTED INDIVIDUALLY

```
L1  Ok                     TRUE   -- and it means TRANSPORT ONLY
L2  RemoteExitCode == 0    FALSE  -- exit 1                        <- RED
L3  receipt HEAD == pushed NOT MEASURED -- the agent never ran      <- UNMEASURED
GATE (audit.py health)     NOT RUN
```

**The conjunction fails. §1(C)'s own rule applies: "Any leg red ⇒ name the defect, committing
lanes stay LOCAL, nothing waits."**

`Ok=True` is not a pass and the module says so itself, unprompted, in its own output:
*"transport OK, but the remote command exited 1. `Ok=$true` reports the TRANSPORT only… read the
receipt (and RemoteExitCode) before treating this lane as done."* A probe that reported L1 alone
would have called this green.

---

## THE DEFECT — W4 DEFECT 4: THE AGENT IS NOT AUTHENTICATED

The remote receipt, verbatim:

```
{"type":"result","subtype":"success","is_error":true,...,"duration_ms":47,
 "num_turns":1,"result":"Not logged in · Please run /login",...,"total_cost_usd":0,
 "usage":{"input_tokens":0,...,"output_tokens":0}}
```

`claude -p` inside the container reached a decision in **47 ms**, consumed **zero tokens**, and
returned **"Not logged in · Please run /login"**. The codespace image carries no Claude
credential, so the agent cannot start. Everything downstream of it — the arrival-HEAD
measurement, the fetch, the `uv` provisioning, the hub gate — never executed.

Note the shape, because it is a trap: `subtype` reads `"success"` while `is_error` is `true`.
A consumer keying on `subtype` alone records a successful run of an agent that never ran.

### Why every previous smoke-6 probe missed this

**They never invoked the agent.** `NB2-SMOKE6-zg3-entry.md` asks for four facts —
`git rev-parse HEAD`, `git status -sb`, `git log -1 --format=%cI`, `uv --version` — all of them
plain shell over `gh codespace ssh`. They measured **the container**. This probe measured **the
agent in the container**, because `Dispatch-Codespace` runs `claude -p` headless, and that is
the first time the auth surface was on the path at all.

So the defect is not new *behaviour*; it is newly *visible*. Any Z-G3 reasoning that treated a
green smoke-6 as evidence about lane execution was reasoning about a different subject.

### Secondary finding, carried because it will bite next

```
Ignoring 1 permissions.allow entry from .claude/settings.json: this workspace has not
been trusted. Run Claude Code interactively here once and accept the trust dialog, or set
projects["/workspaces/dev-knowledge"].hasTrustDialogAccepted: true in /home/vscode/.claude.json.
```

A `permissions.allow` entry was **silently dropped**. Even with auth fixed, a headless lane would
run under a narrower permission set than its `.claude/settings.json` declares, and nothing in the
lane's own output would say so. The remedy is a container-side
`hasTrustDialogAccepted: true`, not an interactive session that by definition cannot happen on a
headless substrate.

---

## WHAT THIS PROBE DID **NOT** ESTABLISH

Stated explicitly, because a red run tempts an over-reading in both directions:

- **W4 defect 2 (`uv` version) is UNMEASURED here.** The provisioning step never ran.
- **W4 defect 3 (silently-stale clone, `[#616]`) is UNMEASURED here.** Arrival HEAD was never
  printed, so this run is evidence neither for nor against the codespace-AGE hypothesis.
- **The hub gate is UNMEASURED on this substrate.** `audit.py health` never executed.

This run therefore **closes nothing** and **refutes nothing** about defects 2 and 3. It adds a
fourth defect that is upstream of both: the agent does not start, so nothing downstream is
observable.

---

## CONSEQUENCE FOR BATCH E — decided by §1(C)'s own rule, not by preference

- **Z-G3's entry condition is NOT met.** The router-ADR entry condition is **NOT** recorded as MET.
- **All committing lanes freeze with `substrate = local`.** This is §1(C)'s named fallback, and it
  is what `PLAN.md` already assumed pending the probe (U-8).
- **Nothing waits.** The batch proceeds at full speed on LOCAL; the probe was run in parallel
  precisely so a red verdict would cost no wall-clock.
- **The three cloud read-only censuses are unaffected** — tier (A) ran on the `cloud` substrate,
  not `codespace`, and all seven returned bound with receipts.

## THE REMEDY, NAMED SO THE NEXT ATTEMPT IS CHEAPER

The blocker is one credential on a disposable machine. Candidates, in the order a next probe
should try them — **none attempted here, because a probe that repairs its subject destroys its
own measurement**:

1. A **Codespaces secret** carrying the Claude credential, set at the repo or user level, so a
   fresh container has it at create time and no interactive step is needed.
2. The same act that sets `projects["/workspaces/dev-knowledge"].hasTrustDialogAccepted: true`,
   since both defects live in `/home/vscode/.claude.json` and one write can close them together.
3. Re-run this exact probe unchanged. It is idempotent, costs ~50s of `basicLinux32gb`, and its
   receipt block is directly comparable to this one.

**Do not route a committing lane to Codespace until L2 and L3 both come back green with the gate
line attached.** A lane dispatched into an unauthenticated container does not fail loudly — it
returns `Ok=True` in under a minute with an empty result, which is the most expensive kind of
false green there is.
