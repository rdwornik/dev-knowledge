# MORNING — night batch 2026-07-28→29 (branch `claude/night-2026-07-28-prep-5my46t`)

**Contract kept:** branch-only · zero merges · zero BACKLOG/`tasks/` writes · zero closures · nothing deleted.
**Verification status — UPGRADED post-batch** (still no `~/.claude` user-level gates, no Codex lane; your
local run stays authoritative). The VM was repaired mid-session: uv pinned `0.11.19` installed (the shipped
`0.8.17` shadowed it on PATH), the SHALLOW clone unshallowed (it had faked "edited 2026-07-23" freshness
FAILs — graft-boundary artifact), pre-commit armed all 3 stages. Then, for real, through `uv run --locked`:
**ruff clean · `gen_task_tree --check` ok · PLAYBOOK TOC ok · silent-rule ratchet 427 ≤ 428 (the draft's +2
drained, see commit) · audit-health hard-fail-free · the last commit passed the full armed hook stack.**
**pytest:** full run 1927 passed / 27 failed / 4 skipped (+1 deselect = the known [#430] fleet-parity red);
after `uv sync --all-groups` (pandas group was unsynced) the 18 `test_fleet_analytics` fails all PASS;
the residual 10 are environment-classified — git-version message text (`index.lock` wording), the isolated
pre-commit store push, language-server absence (reverse-dep oracle ×5, safe-remove, legibility-graph,
carrier-hooks) — re-verify locally. **ship-gate: RED on exactly 4 undispositioned WARNs, zero hard fails**
— this file's deliberate root add (fleet_parity root-sweep), 2× sibling-repo-unavailable (no `ai-council`/
`corp-monorepo` in the VM), and the pre-existing `reconciled_versions` malformed-stamp WARN on
`templates/CONTRIBUTING-md-template.md`. Dispositioning is your ADR-75 call, not the night lane's.
Line-number anchors cite the quoted text as the real anchor. This file is ephemeral operator I/O — consume
and delete it in the morning batch (its root add trips `validate-hermetization` Rule A + the root-sweep WARN
by design, both of which vanish with the file).

## Produced (3 artifacts, 3 commits)

1. **Intake #18 ratification dossier** — `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md`.
   Per-amendment A1–A11: live check + ADOPT/DEFER/REJECT + minimal cut, intake #19 §B rider register.
   Headlines: RM-7's premise was stale inside the audit (add-date selector shipped 07-23); A3's enum misses
   the `claude/` cloud-lane prefix (this branch is the witness); A11's [#422] leg is already row-owned;
   A7 + A4-item-3 should sequence AFTER the §B(b) one-round-trip-boot ruling.
2. **[#441] codification DRAFT** — in `protocols/PLAYBOOK.md` Ch8 (ADR-61 section): fat-prompt default,
   four-condition ALL-YES test, one-NO=fat-prompt; replaces the old three-check test (mapping in-block) so
   the corpus carries ONE launch test. Flags inside: the row cites "§8/Ch5" but the live home is Ch8; its
   condition-2 "pre-allocated JOURNAL letters" example conflicts with intake #18 A5 (assign-at-integration).
3. **Post-flip stale-procedure audit** — `docs/audits/2026-07-29-technical-postflip-stale-procedure-audit.md`.
   19 adjudicated rows (9 STALE, 4 AMBIGUOUS, 6 CORRECT-listed); nothing fixed. `--prune`-as-available and
   `tasks/`-as-derived: zero live instances. Plugin-cache caveat ([#442] class) on the 3 plugin-surface rows.

## Needs your word

1. **Parked `.vscode` decision** (`docs/audits/2026-07-28-technical-vscode-sizing-decision-surface.md`):
   confirm **option (b)** — then the **corp GO** for the S-sized manual visibility copy, and **pick the
   mechanism date** the [#387]→vehicle-ADR leg is scheduled behind (e1 `review_date`s re-date to it).
2. **[#441] draft adoption** — merging this branch IS the ratification; also rule the condition-2 vs A5
   conflict (or park it for the 07-30 session with the dossier's pack-finding 2).
3. **Morning fix batch** for the stale-procedure table rows 1–12 (rows 1–3 need the plugin cache-bump
   caveat; row 13 routed to the intake #18 session instead).
4. **Dossier recommendations are not authority** — they feed your per-amendment rulings on 2026-07-30 ([#435]).

## Proposed morning sequence

1. Local gates on this branch: `pytest`, `audit.py ship-gate`, pre-commit — everything above is unverified.
2. Rule [#441] adoption (item 2) → merge `--no-ff` or amend the draft in place.
3. Rule + execute the stale-procedure fix batch (item 3) as its own arc.
4. `.vscode` word (item 1) — independent of the merges.
5. Delete this file in the first fix-batch commit; the two audits + JOURNAL carry the record.

**Tip:** see the branch head — after this file's first commit (`76d161b`) the batch added the ratchet-drain
commit (`05efa7d9`, three normative tokens reworded in the [#441] draft, meaning unchanged) and this
verification-status update. All artifact content above is otherwise unchanged since its cited commit.
