# Step-2 measurement — the registry row, the precedent, and the host

Consumers: `[#627]` (the admission precedent this lane follows) · intake #75 (the `offload`
role this measurement is taken for).

> **Class:** technical · **Date:** 2026-09-09 · **Lane:** `lane-v-000-offload-admission`
> **Mode:** read-only. Every line below is a command run on this host today, with its output.
> Nothing here is transcribed from an earlier artifact.

## 1 · The registry row, read rather than quoted

`ecosystem/provider-registry.yaml`, `providers:` → `copilot-enterprise`:

```
display_name:    GitHub Copilot Enterprise
council_alias:   null          # not a council panellist
cli:             copilot
version_command: [copilot, --version]
```

Read through `scripts/provider_registry.providers()`, which validates the whole file against
`ecosystem/schema/provider_registry.py` on every load — so this is the schema-checked value,
not a `grep`. `tests/test_offload_admission.py::test_the_LIVE_registry_declares_copilot_enterprise_reached_by_copilot`
pins it, so a later rename or repoint turns RED instead of silently making every
`copilot-enterprise` record `unknown-provider`.

**What the registry does NOT carry, checked and stated because the lane is pinned out of it.**
Operational doctrine for this provider — the capability profile and the BILLING VERDICT — is
at L0 in `~/.claude/ROUTING.md`, outside this repository. The registry's own comment block says
so, and the row's schema forbids extra fields. This lane reads the row and adds nothing to it.

**Billing was not probed.** Ruled closed 2026-08-29: consumption meters to the enterprise org
seat, a zero on the user premium-requests meter is correct, and the ruling is NO FURTHER
PROBING. The `--usage-output-file` capture in section 4 is a per-run token/AIU statistic the
CLI writes locally about the call this lane made; it reads no billing surface and queries no
account.

## 2 · The precedent — `[#627]`, and what it actually establishes

`tasks/627-agy-route-is-inert-no-row-authorizes-analysis-admission.md` is **open**, `[P2][M]`.
Two things in it govern this lane:

1. **The measured verdict was REFUSE, not ADMIT** (`lane-f-6-agy-admission`, 2026-09-01) — and
   the row stayed open, because the verdict discharged the *measurement* half of its done-when
   clause and not the two births A7 FINDING A names (the role row, and routing a CLI to it).
   The same separation applies here and is the reason section 6 of the lane artifact does not
   write a routing row.
2. **The bar is seeded, not happy-path.** The row's flagship failure is instructive precisely
   because it is a *mechanism* failure and not a reading one: the whole-repo-scan item failed
   three consecutive draws "always by analysing a repository that is not `.dev-knowledge`".

The second, complementary precedent is the reader bar itself:
`docs/audits/2026-09-05-technical-corpus-coherence-gemini.md` — one structured retrieval-only
question, every locator re-opened on disk by the verifier, "**six locators, all six EXACT on
disk. Zero fabrications**", with the standing caveat that "locator-exactness is not
claim-correctness". Both halves are implemented in `scripts/offload_admission.py`: the
fabrication check and the quote-at-the-line drift check are separate refusal codes.

## 3 · The host — the CLI the registry declares actually resolves

```
> (Get-Command copilot).Source
c:\Users\1028120\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\copilotCli\copilot.ps1

> copilot --version
GitHub Copilot CLI 1.0.82.
Run 'copilot update' to check for updates.
exit=0
```

The registry's declared `version_command` runs and exits 0. `copilot` resolves to a PowerShell
script shipped inside the VS Code extension's global storage, not to a standalone binary on a
managed PATH — recorded because it is a fact about *where this route lives* on this host, and a
route whose entry point is an editor extension's private directory has a different upgrade and
availability story from one installed on PATH. No claim is made here about whether that matters;
it is recorded so a later reader does not have to rediscover it.

## 4 · The route answers — liveness, separately from admission

```
> copilot -p "Reply with exactly: OK" --no-color -s
OK
exit=0
```

Liveness only. This says the credential resolves and the server answers; it says nothing about
the role. Admission is section 5 of the lane artifact and its verdict is **REFUSE**.

## 5 · What step 2 fixed as the lane's premises

- `copilot-enterprise` / `cli: copilot` — present, schema-valid, and now test-pinned.
- `[#627]` — open, and its REFUSE verdict is the shape this lane's own verdict takes.
- The Copilot CLI is installed, resolvable, and answers a prompt on this host.
- Nothing in `ecosystem/routing-table.yaml` carries an `offload` role. That absence is
  unchanged by this lane, deliberately — see the artifact's section 6.
