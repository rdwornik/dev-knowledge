# LANE lane-a-1-codespace-pow-and-router-adr — prove a COMMITTING lane green on codespace, attended, then author the wave-2 substrate router ADR from that receipt

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `codespace` — an off-machine lane in the repo's own devcontainer, receipt-gated, committing on the `worktree-` prefix like a local lane.

```
Dispatch-Codespace -Contract LANE-a-1-codespace-pow-and-router-adr.md -Slug lane-a-1-codespace-pow-and-router-adr
```

The operator runs the line above verbatim. The contract is shipped IN **as a
file**, and so is the runner: nothing on the ssh command line is a quoted
payload, because a PowerShell string reaching a bash login shell through gh's
transport is parsed twice. Tier is on the record in the routing table above
(`opus` / `high`) — `Dispatch-Codespace` carries no `-Effort`.
Permission mode is `bypassPermissions`, as on every substrate.
**The container is CREATED, never rebuilt** (ruling 2026-08-31): a rebuilt
container has not applied its own `devcontainer.json` — no features, no
`postCreateCommand`, a stale clone — while a fresh create from the same HEAD
applies all of it. The clone starts at `origin`, so every input this contract
names is pushed before dispatch. Cost flags (`-Machine`, `-IdleTimeout`,
`-Retention`) are the operator's at dispatch and are deliberately not frozen
here; board label `[.dev-knowledge · lane-a-1-codespace-pow-and-router-adr · lane-a-1-codespace-pow-and-router-adr]`.

## Worktree pairing

slug `lane-a-1-codespace-pow-and-router-adr` -> branch `worktree-lane-a-1-codespace-pow-and-router-adr` -> contract `LANE-a-1-codespace-pow-and-router-adr.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A codespace lane runs on `worktree-`, the SAME prefix as a local lane and not
the cloud transport's `claude/`: it commits and pushes like a local lane,
merely elsewhere, so `claude/` would name a branch nothing creates (R-ENUM
leg 3, 2026-08-31). Off-machine and cloud are different axes.

## Write-scope (frozen)

- `docs/decisions/ADR-117-wave-2-substrate-router.md`
- `docs/audits/2026-09-01-verification-batchf-codespace-pow.md`

## Receipt gate

This lane runs off-machine in the repo's own devcontainer, so it carries a receipt
(`protocols/STANDING_RULINGS.md` Q5) — `receipt.json`, pulled back out. Both
fields, checked as a conjunction — either one alone reports a success the other
refutes:

- `transport-ok-and-remote-exit-code-read-separately:` `<Ok=…, RemoteExitCode=…, read separately>`
- `is-error-false-not-subtype-success:` `<is_error, verbatim from receipt.json>`

`Ok` is the TRANSPORT's verdict and `RemoteExitCode` is the WORK's: gh's own exit
code is 1 regardless, so a caller branching on `Ok` alone reads a failed lane as a
success. And a receipt can carry a success `subtype` while `is_error` is true, so
`is_error` is the verdict field and `subtype` is the trap — a consumer keying on
`subtype` records a successful run of an agent that never ran. A dispatch missing
either half is treated as not having started, and is re-dispatched into a FRESH
container (created, never rebuilt).

## Done-contract (immutable)

1. **A COMMITTING lane ran green on codespace and the receipt proves it** — a real branch
   pushed from inside the container, `audit.py health` exit 0 and the targeted suite green
   IN-CONTAINER, and both receipt fields recorded above. Ok alone is the transport; it is not
   the lane.
2. **ADR-117 is AUTHORED from that receipt, not from intent** — the wave-2 substrate router:
   the gated enum, what each substrate admits, and the entry condition each must meet. It cites
   the 2026-08-31 fresh-create admission (`c8bf1390`, JOURNAL 2026-08-31 (i)) and this lane's own
   receipt as its evidence, and it states the create-vs-rebuild finding as a binding rule.
   Status `Proposed` — ratification is the operator's, never this lane's.
3. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Confirm the container is CREATED, never rebuilt, and record the create command actually
   used. A rebuilt container has not applied its own `devcontainer.json`. **COMMIT**
2. Run the committing proof-of-work: branch, real edit, `audit.py health`, targeted tests, push.
   Record both receipt fields verbatim — `Ok`/`RemoteExitCode` read SEPARATELY, and `is_error`
   rather than `subtype`. **COMMIT**
3. Author `ADR-117` from the receipt. It feeds `[#582]`; it does not implement it. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
