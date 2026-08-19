# LANE J — [#554] D1/D2 PROOF · frozen contract of record · 2026-08-19

**FROZEN CONTRACT OF RECORD.** Saved verbatim as the FIRST COMMIT of the lane, before any
work, per ADR-110 (contract-as-first-commit). Content arriving later in the session is not
load-bearing — a correction re-enters as a new contract, never as a mid-flight message
(`protocols/STANDING_RULINGS.md` D2).

- **Lane:** J — `[#554]` D1/D2 proof (Codespaces stage-1 green run)
- **Channel:** local worktree lane (`--worktree`)
- **Branch:** `worktree-lane-j-554-proof`
- **Base:** `52542a5d` (main tip at boot)
- **Mode:** execute, commit-and-STOP. No merge, no push to main, no JOURNAL, no row closure.
- **Output artifact:** `docs/audits/2026-08-19-technical-554-proof.md`

**Operator dispatch terms carried alongside the contract body (recorded verbatim, not a
deviation):** use `gh` account **rdwornik** for all codespace calls (codespace scope confirmed
there); switch back to the previously active account at the end; delete the codespace when
done; the `--worktree` flag already created the worktree; first commit = contract-of-record;
work ONLY inside the worktree; commit-and-STOP, never merge, never push main.

---

## Contract body (verbatim)

# LANE J — [#554] D1/D2 PROOF: CODESPACES STAGE-1 GREEN RUN

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | medium |

**Worktree lane, commit-and-STOP.** Governing row: `[#554]` — read it; ONLY its D1/D2 proof
legs remain (L1–L4 landed in batch 1; C-1 waitFor fix applied at merge). Account for gh ops:
**rdwornik** (personal — `codespace` scope confirmed present); use `gh auth switch` to it and
verify with `gh auth status` before any codespace call; switch back at the end.
**ADR-110:** commit this prompt first as
`docs/audits/2026-08-19-technical-554-proof-lane-contract.md`.

## D1 — Codespaces free-tier green run
1. `gh codespace create -R rdwornik/dev-knowledge -b main` (smallest machine type offered);
   record machine type + create time.
2. In the codespace (`gh codespace ssh`): confirm the devcontainer provisioned (pinned uv
   version per ADR-106 — print it), then run `python scripts/audit.py health` AND
   `pytest -m "not slow"`; capture both outputs end-to-end.
3. D1 = both green. Capture the full log into the lane artifact (verbatim tail + exit codes).
4. `gh codespace delete` when done — no idle codespace left running; verify with
   `gh codespace list`.

## D2 — identical script via `devcontainer up` off-Codespaces
Attempt locally: `devcontainer up` (needs the devcontainer CLI + a container runtime). If the
corporate machine lacks Docker/runtime (AppLocker precedent) → **authorized fork:** record
BLOCKED with the exact wall, and note D2's remaining path (VPS or Enterprise codespace — fed by
today's Enterprise probe). Do NOT install container runtimes system-wide to force it.

## FINAL
Artifact `docs/audits/2026-08-19-technical-554-proof.md`: D1 log + verdict, D2 result-or-wall,
machine/timing numbers (they feed the Hetzner-vs-Enterprise substrate decision).
Commit-and-STOP. **Row closure is the seat's act** — you report D1/D2 states, you close
nothing. No index regen, no JOURNAL, no merge.
