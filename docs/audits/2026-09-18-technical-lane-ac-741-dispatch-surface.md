# LANE ac-741 — where the dispatch verb lives, whether a launch verb can carry a non-Claude model, and what moving it to the hub would cost in lanes

**Measured:** 2026-09-18 · **Host:** win32 / Windows 11 Enterprise 10.0.26200 · **Method:** live
probes (`Get-Command`, executed `dispatch -DryRun`, `dispatch_surface.py`, `pytest`) and verbatim
file reads on both `.dev-knowledge` and `win-tooling`. Nothing below is inferred from
documentation alone — every claim below carries the command or file that produced it.

**Framed as evidence for:** `[#741]` `[#509]` `[#582]` `[#604]`. This is a fact-read, not a
request for a second integrator.

---

## L6 GATE LINE (read this first — the dispatcher boots or does not on this line)

**The dispatch verb does NOT resolve inside this repo.** `dispatch` resolves to
`C:\Users\1028120\.dev-terminals\bin\dispatch.ps1`, deployed FROM `win-tooling`
(`scripts/dev-terminals/bin/dispatch.ps1`), which delegates to `win-tooling`'s
`scripts/dispatch/Invoke-Dispatch.ps1`. `.dev-knowledge` is a *consumer* of the verb (it writes
contracts the verb reads and supplies `PLAYBOOK.md`'s dispatch table as the doctrine of record)
but owns none of the executing code.

---

## 1a — where `dispatch` physically resolves, with the resolving command

```
PS> Get-Command dispatch -All
```

Returns, in PATH order:

1. `C:\Users\1028120\.dev-terminals\bin\dispatch.ps1` (`ExternalScript`) — **wins**, first on
   `$env:PATH`.
2. `C:\Users\1028120\.dev-terminals\bin\dispatch.cmd` (`Application`) — the same verb reachable
   from `cmd.exe`, where a bare `.ps1` is not executable.

Both are **deployed copies**. `dispatch.ps1`'s own header states its provenance verbatim:

> "SOURCE lives here: `scripts/dev-terminals/bin/dispatch.ps1`. DEPLOYED by
> `scripts/dev-terminals/Apply-DevTerminals.ps1` to `$HOME\.dev-terminals\bin\`, which the same
> applier puts on the USER PATH."

Confirmed on disk: `C:\Users\1028120\Documents\Dev\win-tooling\scripts\dev-terminals\bin\dispatch.ps1`
exists (`Test-Path` → `True`); `win-tooling`'s `origin` remote is
`https://github.com/rdwornik/win-tooling.git` — a repo distinct from `.dev-knowledge`.

The deployed script is a **thin entry point**: it does no contract parsing itself and delegates to

```
$InvokeDispatchPath = Join-Path $HOME 'Documents\Dev\win-tooling\scripts\dispatch\Invoke-Dispatch.ps1'
& $InvokeDispatchPath -ContractFile $ContractFile -DryRun:$DryRun -Run:$Run
```

`Invoke-Dispatch.ps1` (also `win-tooling`) is where the actual contract flow lives: resolving
`$env:CLAUDE_PROMPTS_DIR` (live value probed today: `H:\My Drive\CLAUDE PROMPT DIR`, a Google
Drive mount — this repo's `[#509]` row), reading the `## Dispatch` fenced block, tokenizing it into
an argv array with no shell re-parse, asserting the head token is `claude`, and gating live
execution behind `-DryRun` / `-Run` / an interactive `[y/N]`.

**Superseded mechanism, recorded so a stale prior measurement is not relied on:** the 2026-08-25
audit (`docs/audits/2026-08-25-technical-dispatch-surface-measured.md`) found the operator verb
resolving through the auto-loading `DispatchHelpers` PowerShell **module** (`Dispatch-Lane` alias,
`PSModulePath`). That module still exists on disk and its `Dispatch-Local`/`Dispatch-Lane` alias
is still the documented **manual fallback** (PLAYBOOK Ch8 Layer 2 row 1) — but it is no longer what
`dispatch` resolves to. The **PATH-file form measured here today is newer**: `dispatch.ps1`'s own
docstring names the reason — a dot-sourced function/module route "failed four times in five hours"
because `$PROFILE` resolves inside the corp OneDrive exclusion zone and `$PROFILE.AllUsersAllHosts`
needs elevation no agent can perform, while a PATH file is per-user (HKCU, no elevation), outside
the exclusion zone, and resolved identically by every shell including this agent's own PowerShell
tool. This session's own live probe is proof of that last property: `Get-Command dispatch` resolved
correctly from inside a Claude Code PowerShell tool call with no profile loaded.

---

## 1b — RE-SCOPED (binding; `[#740]` stays CLOSED). AX25-2 conformance today, and the six batch-AA lanes

**`[#740]` is not reopened.** Per today's measurement:

```
uv run --locked pytest -x --tb=short tests/test_dispatch_conformance.py
```

→ **22 passed** (16 xdist workers, 44.9s). AX25-2 — the generator-to-verb conformance assertion
`[#675]` clause 1 carries — is **GREEN today**.

**The six lanes.** `tasks/804-a-batch-manifest-committed-before-the-first-l.md` states the
batch this refers to explicitly: *"batch AA dispatched six lanes without one [manifest] and
nothing noticed until merge."* Five of those six contracts still exist in the prompts dir
(`H:\My Drive\CLAUDE PROMPT DIR`) as of this measurement:

| Contract | `## Dispatch` fence head token | Routing table (`\| Model \| Mode \| Effort \|`) | Live `dispatch -DryRun` |
|---|---|---|---|
| `LANE-aa-1-substrate-provenance.md` | `claude` | absent | `source: contract` — resolves clean |
| `LANE-aa-2-integrator-model-split.md` | `claude` | absent | (fence matches; not re-probed live) |
| `LANE-aa-12-enforced-routing.md` | `claude` | absent | `source: contract` — resolves clean |
| `LANE-aa-13-resource-lifecycle.md` | `claude` | absent | (withdrawn/superseded by aa-14) |
| `LANE-aa-14-resource-lifecycle.md` | `claude` | absent | (fence matches; not re-probed live) |

The sixth is not resolvable by name from what survives on disk; `tasks/804` itself notes the batch
had no committed manifest to enumerate lanes from, which is the row's own finding, not a gap this
measurement introduces.

**Verdict: they came through the generator.** Every surviving contract's fence is the exact
`claude --bg --model <m> --effort <e> --permission-mode bypassPermissions --worktree <slug> "Read
and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\<file>"` shape `gen_lane_contract.py`
emits for `--shape local` — byte-for-byte the same template this very lane's own contract carries.
Live-probed twice (`dispatch "LANE-aa-1-substrate-provenance.md" -DryRun`,
`dispatch "LANE-aa-12-enforced-routing.md" -DryRun`): both printed `[dispatch] source: contract`
with **no** derivation warning, meaning `Invoke-Dispatch.ps1` found a literal fence and ran it
verbatim — the generator-conforming path, not the Model/Effort-table-plus-filename fallback.

One thing they are missing that this lane's own contract carries: the two-row
`| Model | Mode | Effort |` header table above the `## Dispatch` block. `scripts/dispatch_surface.py
check` (the hub-side half of the AX25-2/§V organ) refuses all five on exactly that ground — *"no
`| Model | Mode | Effort |` routing row"* — because that check is `[#752]`'s later concern
(resolving a *declared* routing row into launcher flags), not AX25-2's (does the verb accept the
fence). AX25-2 is silent on the table's presence; `[#752]`'s check is a stricter, later-landed gate
that these five contracts predate. **Both explanations do not compete here: the fence mechanism is
generator-conformant and green; the routing-table mechanism is a newer, additional requirement
these five contracts were frozen before.**

Corroborating the manifest finding directly: `LANE-aa-1-substrate-provenance.md` carries
`carried-by: docs/audits/2026-09-15-technical-batch-aa-manifest.md` at its head — and that file
**does not exist** anywhere in this repo (`find … -iname "*batch-aa-manifest*"` → no hits). The
contract points at a manifest that was never committed, which is `[#804]`'s finding verified fresh
rather than merely cited.

---

## 1c — can a launch verb carry a non-Claude model, at all? (unconditional)

**No.** `Invoke-Dispatch.ps1`'s `Assert-ClaudeCommand` (the function the contract mandate calls out
by name, `[#675]` clause 1 / AX25-2) refuses any head token that is not `claude` (bare, or a
path/extension form of it):

> `"Refusing: the contract's ## Dispatch block must invoke 'claude', not '$Head' -- this script
> never runs an arbitrary command from a contract file."`

This is a closed, load-bearing safety property, not an oversight — the same docstring calls it out
as preventing "arbitrary execution" from a contract file. There is **no flag, enum member, or
parameter** on either the deployed `dispatch.ps1`/`dispatch.cmd` shim or `Invoke-Dispatch.ps1`
itself that admits a different head token. The Model enum it validates (`opus, sonnet, haiku,
opusplan`, or a `claude-*` full model string) is scoped to *which Claude model*, never *which
program*.

**`to-cc/run-lane-copilot.ps1` — witness search, both negative.** `[#824]` (open, P1/M, filed
2026-09-16) names this script as the hand-written runner batch AB's Copilot-producer lane
(ab-828) actually launched through, because no registered verb could carry a non-Claude producer.
Searched today, exhaustively, for a witness that it still exists:

- Filesystem: `find "C:\Users\1028120" -iname "run-lane-copilot*"` and
  `find "C:\Users\1028120" -type d -iname "to-cc"` → **zero hits**, both.
- Git history, all branches, both repos: `git log --all --diff-filter=A --name-only | grep -i
  run-lane-copilot` in `.dev-knowledge` and in `win-tooling` → **zero hits**, both. Neither repo
  ever tracked a `to-cc/` directory or this filename.

**So the specific artifact is not re-witnessable today** — it was never committed anywhere on this
machine's two repos, and nothing on disk under the user profile carries its name now. That is
consistent with `[#824]`'s own framing (a hand-written, ad hoc runner reached for because no
launch path existed) rather than evidence the row is stale: `[#824]` stays **open**, and its
absence from disk today is itself further evidence for its Done-when (1)/(2) — there is still no
registered runner for a non-Claude producer, hand-written or otherwise, for this lane to find.

---

## 1d — the verb's contents, split: methodology vs. machine-local (itemised)

**METHODOLOGY (hub-owned today, OS-independent — this is what "the hub owns lane launching"
already means in practice):**

- The **ruling** that `dispatch <contract.md>` is THE sole operator verb for a local lane, and
  that the raw `claude --bg`/`--worktree` form is fallback-only — `protocols/PLAYBOOK.md` §"The
  dispatch table — the SOLE literal-command site" (Ch8), `docs/audits/2026-08-25-technical-
  dispatch-consolidation-plan.md` §2.
- The **contract grammar**: a `## Dispatch` heading + fenced block that wins outright over
  derivation; a `**Shape:**` declaration; a `| Model | Mode | Effort |` routing row —
  `scripts/gen_lane_contract.py` (the sole emitter), read by `scripts/dispatch_surface.py`.
- The **closed enums**: `MODEL_ENUM`, `EFFORT_ENUM`, `MODE_ENUM`, `SHAPE_ENUM` — declared once in
  `gen_lane_contract.py`, read (never restated) by `dispatch_surface.py` via `_vocabulary()`.
- The **safety property** that a contract names work, never the program — "the head token must be
  `claude`" — is a *doctrine* the hub states (this contract's own "What NOT to do" / AX25-1) even
  though the *code* that enforces it lives outside the hub (see below).
- The **routing resolution**: declared model/mode/effort/shape → the flags a launcher must honour,
  including the measured `opusplan`-is-inert-under-`--bg` fact and the mode→`--permission-mode`
  table — `scripts/dispatch_surface.py::resolve_launch` (`[#752]`).
- The **branch/worktree pairing convention**: `worktree-<slug>` ↔ ADR-110 exemption ↔ one contract
  file — stated in PLAYBOOK Ch8 and in every generated contract's own "Worktree pairing" section.
- The **agreement check**: that the two point-of-use surfaces (`.claude/commands/lane-boot.md`,
  `templates/prompt-template.md`) name the ruled verb and carry no rival literal form —
  `dispatch_surface.py::agreement_findings`, run by `audit.py::dispatch_verb_agreement`.

**MACHINE-LOCAL (win-tooling; Windows- and this-workstation-specific; NOT movable into the hub
without breaking ADR-28/36 "Layer 2 never executes"):**

- The **deployed launcher files themselves**: `dispatch.ps1` / `dispatch.cmd` on the User `PATH`
  under `$HOME\.dev-terminals\bin\` (HKCU registry `PATH`, no elevation) — a Windows-specific
  per-user PATH mechanism, deployed by `win-tooling`'s `Apply-DevTerminals.ps1`.
- **`Invoke-Dispatch.ps1`** itself: `#requires -Version 7` PowerShell, PowerShell-specific argv
  tokenization (quote/backtick handling matching PowerShell's own rules), `Read-Host` for the
  interactive confirm, `& $command @argv` invocation.
- **`$env:CLAUDE_PROMPTS_DIR` resolution and its live value** — a User-scope environment variable
  whose value today, measured live, is `H:\My Drive\CLAUDE PROMPT DIR`, a Google Drive mount
  specific to this workstation; fallback `$env:USERPROFILE\Downloads` is equally machine-local.
- The **legacy `DispatchHelpers.psm1` module** and its `PSModulePath` auto-load wiring (User-scope
  registry variable, SHA-verified deploy, the corp-OneDrive-exclusion-zone shadowing hazard) — the
  documented manual fallback (`Dispatch-Local`/`Dispatch-Lane`), still present but no longer what
  `dispatch` itself resolves to.
- The **`claude` CLI's own resolution** on this machine — `C:\Users\1028120\AppData\Roaming\npm\
  claude.cmd`, an npm global install path.
- The **cloud/codespace transports' machine-local halves**: `Dispatch-CloudV2`'s credential store
  (`Get-CloudApiCredential`), and `Dispatch-Codespace`'s dependency on `gh` being authenticated on
  this machine.

The split is already close to clean: everything a *contract* declares or a *doctrine* rules is
hub-owned prose/code today; everything that turns a declared line into a real OS process — file
placement, PATH/PSModulePath wiring, PowerShell version, credential stores, drive letters — is
necessarily machine-local, and Critical Rule #4 (ADR-28/36, "Layer 2 never executes") forbids the
hub from owning that half regardless of convenience: a script in `.dev-knowledge` that spawns
`claude --bg` on this operator's machine would be exactly the orchestration-script class that rule
exists to prevent.

---

## 1e — what moving it to the hub would cost, in lanes

**The execution half cannot move to the hub at all**, by the hub's own standing rule (ADR-28/36,
Critical Rule #4, restated in this repo's own `CLAUDE.md` §5 rule 4: "Layer 2 never executes — no
script drives state in a child repo"). Moving `Invoke-Dispatch.ps1`'s process-spawning half into
`.dev-knowledge` would violate the invariant the hub is built on, not merely add a lane's worth of
work. So "moving it to the hub" can only mean the methodology half — and that half is
**already there** (see 1d): the doctrine, the contract grammar, the enums, and the routing
resolution all already live in `protocols/PLAYBOOK.md` and `scripts/gen_lane_contract.py` /
`scripts/dispatch_surface.py`. There is no undone "move" to cost.

What is genuinely outstanding is the **remaining seam between the two halves** — where the hub's
methodology and win-tooling's execution still disagree or leave a gap — and each seam is already
a filed, sized, open row:

| Row | Size | What it costs (already estimated by its own filer) |
|---|---|---|
| `[#824]` | M | A contract grammar admitting a declared non-Claude producer + a registered (not hand-written) runner the verb dispatches through + a post-hoc ran-model read for non-Claude receipts. ≈ **1 lane**. |
| `[#823]` | S | The dispatch verb refuses to boot with no committed batch manifest — currently only `/lane-boot` refuses; `dispatch` itself does not. ≈ **1 lane**, and it lands in `win-tooling`'s footprint (`Invoke-Dispatch.ps1` calling `scripts/lane_boot.py preflight` from the target repo), so it is cross-repo work either way. |
| `[#509]` | S | Its Done-when — `Invoke-Dispatch.ps1` resolves `$env:CLAUDE_PROMPTS_DIR` in either shape, with a test — reads as **already satisfied** by the code measured in 1a (`Get-DispatchPromptsDir` / `Sync-DispatchPromptsDir`, live-probed resolving `H:\My Drive\CLAUDE PROMPT DIR`). The row is stale-open, not outstanding build work: closing it costs evidence, not a lane. |

**Total measured cost: ≈ 2 lanes** (`[#824]`, `[#823]`) for the outstanding seam work, plus a
zero-build evidence-only close for `[#509]`. `[#582]`'s substrate router (L, open) is a larger,
separately-scoped act — it replaces the *Substrate:* field's documentation-only status with a
gated enum and capability table, which this lane's evidence supports but does not itself cost,
since 1a–1d measure the LOCAL row only (BACKGROUND_SHAPES in `dispatch_surface.py` is explicitly
scoped to `("local",)`, an honest limit the module states about itself). `[#604]`'s deploy-registry
admission is already recorded DONE for win-tooling by its own row text; only `terminal-setup`
remains, and that is orthogonal to dispatch itself.

---

## Organs used, and the raw scans this lane declared rather than ran silently

Per this lane's own "Organs and rows" mandate: `file_purpose_graph.py why` and
`graph_queries.py process-list --render` were consulted for the process roster (found
`scripts/dispatch_surface.py`, `scripts/dispatch_conformance.py`, `scripts/dispatch_drift.py`, and
`scripts/lane_boot.py`'s recorded non-wiring to the dispatch verb). One raw grep
(`git log --all --diff-filter=A --name-only`, both repos) was run to search for
`to-cc/run-lane-copilot.ps1` — a witness-search over git history that no organ answers, since the
question is "did this ever exist," not "what does the live graph say." A second raw `find` over
the user profile (1c) is the same class: a filesystem existence probe outside any organ's scope.
Both are declared here rather than run silently.

## What NOT done (per this lane's Done-contract, read-only)

No edit was made to `Invoke-Dispatch.ps1`, `dispatch.ps1`, `DispatchHelpers.psm1`, or any
`win-tooling` file. No task row status was changed, including `[#509]`'s stale-open state noted
above. No merge, no push to `main`, no JOURNAL entry, no index regeneration.
