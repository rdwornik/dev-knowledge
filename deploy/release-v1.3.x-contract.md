<!-- scope: hybrid -->
# Release contract — methodology v1.3.x

**Status:** Draft (design contract — not a release cut)
**Date:** 2026-07-08
**Tier:** Deployment-scope contract (sibling to `manifest-v*.yaml` / `release_lint.py`; not an ADR)
**Related:** ADR-91 (corpus versioning), ADR-92 (deploy-runbook doctrine), ADR-93 (floor
provisioning model A), ADR-96 (deploy remove leg) + its 2026-07-06 amendment, ADR-81 (feature
lifecycle — clause (d) documented deferral + leg (e) functional proof) · BACKLOG #275 #280 #245
#246 #276 · `deploy/release_lint.py` · `deploy/manifest-v1.2.0.yaml`

> **Version-provenance note.** This is a **design contract**, authored during the Wave-1 prep
> lane. **The methodology version is HELD at v1.2.0** — no `manifest-v1.3.0.yaml` is authored
> here and no deploy runs from this lane. The one code change that lands (#275b) is **carrier
> engine code, pinned by none of `release_lint`'s five version anchors, and undeployed** — the
> `[NB-1]`/`[NB-2]` v1.2.0 precedent (metadata/code changes that ride ahead of a tag without a
> version bump). Consumers receive #275b only when a real v1.3.0 is cut and deployed.

---

## Context
Wave-1 fleet onboarding is GO (operator-ratified 2026-07-08): ai-council first, corp-monorepo
second. Onboarding executes per-repo in each child's dedicated chat (ADR-41). This contract
names what the **next methodology release (v1.3.x)** must carry, so the per-repo arcs and the
eventual release-cut arc share one spec. Four scope items:

- **#275b** — carrier-side hook arming (the deployed arm step installs all three hook stages).
- **#280** — propagate the intake area + template to greenfield consumers via the manifest.
- **#245 (+#246 gate clause)** — deploy add-path honors `status: removed`; last-deployed-bytes oracle.
- **#276** — a D2 per-consumer divergence-allowlist the prune leg actually reads.

**Design-only decision (operator, 2026-07-08).** Only **#275b** is built in this arc (it is
small, self-contained engine code, and the frozen acceptance contract requires a test proving
3-stage arming). #280 / #245 / #246 / #276 are **specified here and deferred** (they are
deploy-engine / new-carrier work). The `release_lint` gap is an explicit ADR-81(d) deferral —
see **§Deferred**.

**Forcing function for #276.** corp-monorepo already records `deployed_methodology_version:
1.2.0` and carries its own consumer-owned ruff (`astral-sh/ruff-pre-commit` @ v0.15.8) that
URL-matches the ruff-gate tombstone. The ADR-96 2026-07-06 greenfield-skip unblocks only
*first* deploys (registry null); a v1.3.x remove-leg run re-enters the prune sweep on a
previously-deployed consumer and **REFUSEs** on corp's ruff. So a v1.3.x that ships the remove
leg without D2 **strands Wave-1 target #2** — #276 must ride in v1.3.x.

---

## Scope
Each item: what it changes · why · acceptance (verbatim BACKLOG Done-when) · BUILD-NOW vs
DESIGN-DEFER · surface.

### 3.1 #275b — carrier-side hook arming · BUILD-NOW (landed this arc)
- **What:** the floor carrier's SessionStart arm command now installs all three managed hook
  stages: `_SESSIONSTART_ARM_CMD` in `deploy/carrier_floor.py` gains `-t pre-commit -t
  commit-msg -t pre-push` (mirrors the hub's own `scripts/arm_hooks.py`).
- **Why:** a bare `pre_commit install` arms the pre-commit stage only, so a fresh consumer's
  commit-msg / pre-push stage hooks land wired-but-dormant (#275 leg-a, the consumer-local
  `default_install_hook_types` corrective, landed on ai-council; leg-b is the carrier-side fix).
- **Acceptance (BACKLOG #275 Done-when, leg-b):** "the carrier-side fix ships at the next
  release" — met here as engine code + a test proving all three stages arm.
- **Surface:** `deploy/carrier_floor.py` (one constant) + `tests/test_deploy_floor.py`
  (content proof) + `tests/test_floor_conformance.py` (trip-test). **Landed: commit `fc8e4ef`.**

### 3.2 #280 — intake propagation to greenfield consumers · DESIGN-DEFER
- **What:** ship `docs/intake/README.md` + `templates/intake-template.md` to a deployed
  consumer via the manifest, so greenfield repos inherit an intake scene.
- **Why:** `docs/intake/` + the template are hub-only today (no `intake` reference in
  `deploy/manifest-v*.yaml`); the fleet census found the intake location split across consumers.
- **Acceptance (BACKLOG #280 Done-when):** "a manifest version ships the intake area/template
  AND a deployed consumer carries `docs/intake/README.md` + `templates/intake-template.md`."
- **Defer rationale:** the five live carriers (global-config, tier1-plugin, precommit, floor,
  enforcement-mesh) ship **no arbitrary doc tree** — global-config copies one fixed file. #280
  needs a **new file-tree/docs carrier**, not a manifest declaration alone (declaring an
  `intake` component against an unbuilt carrier lints green but is undeployable).
- **Surface:** a new carrier + `deploy/tool.py` registry + a `manifest-v1.3.0.yaml` component.

### 3.3 #245 (+#246 gate clause) — add-path status-awareness + last-deployed-bytes oracle · DESIGN-DEFER
- **What:** teach the deploy add-path to honor `status: removed` (skip re-adding), and classify
  prune targets against **last-deployed bytes** (a per-consumer sidecar, the floor-carrier
  precedent) instead of the current manifest shape.
- **Why:** the add-path is blind to `status: removed` today; the re-add tug-of-war is avoided
  only by manually dropping a pruned component from its carrier's add-target, which breaks for
  anchor-coupled entries (the hub-toc-hooks case). #246 folds in as a **gate clause**:
  hub-toc-hooks retirement is gated on #245 (its `hub_hooks` entry IS version-anchor-3 and its
  toc hooks are the entry's only content, so pruning empties it → the add-path re-creates it).
- **Acceptance (BACKLOG #245 Done-when):** "the add-path skips re-adding a `status: removed`
  component (no manual add-target drop needed) AND a source-drifted prune target classifies
  against last-deployed bytes, with tests." **#246 Done-when:** "#245 has landed AND (if still
  desired) hub-toc-hooks is pruned + verified ABSENT with no re-create."
- **Defer rationale:** pure deploy-engine change (`deploy/tool.py` add-loop + `deploy/contract.py`),
  not expressible as a manifest anchor.
- **Surface:** `deploy/tool.py`, `deploy/contract.py`, a per-consumer last-deployed sidecar.

### 3.4 #276 — D2 per-consumer divergence-allowlist · DESIGN-DEFER (rides in v1.3.x)
- **What:** a per-consumer divergence-allowlist the prune leg **actually reads**, so a
  consumer-declared divergence for a tombstoned component makes `detect_prune` **SKIP** it
  instead of REFUSE-aborting the whole run.
- **Why:** the forcing function above — corp-monorepo (records 1.2.0) re-enters the sweep and
  REFUSEs on its consumer-owned ruff. The existing P4 `.methodology.yaml` allowlist is
  Informant-side only; the deploy prune leg never consults it.
- **Acceptance (BACKLOG #276 Done-when):** "a consumer-declared divergence for a tombstoned
  component causes the prune sweep to SKIP that component (no REFUSE-abort) on a
  previously-deployed consumer, with tests."
- **Defer rationale:** deploy-engine change (`detect_prune` + `deploy/tool.py`); pairs with
  #245's last-deployed-bytes oracle.
- **Invariant (must hold):** #276 only **adds scoping** — it must never weaken the REFUSE
  default for a locally-modified component absent an explicit allowlist entry; the greenfield-skip
  (ADR-96 2026-07-06) stays intact.
- **Surface:** `deploy/carrier_precommit.py` (`detect_prune`), `deploy/tool.py`, a consumer-side
  `.methodology.yaml` divergence declaration schema.

---

## Decision per item (designed mechanism — so the build arc has a spec)
- **#280:** add a **file-tree carrier** (`carrier_docs`?) that reconciles a declared set of
  source→dest doc paths (detect = bytes-match, apply = copy, verify = re-read), registered in
  `deploy/tool.py`; declare `docs/intake/README.md` + `templates/intake-template.md` as its
  targets in `manifest-v1.3.0.yaml`. (Rejected: overloading global-config, which is L0 single-file.)
- **#245:** thread the prune sweep's already-computed removed-set into the add-loop's `apply`
  so a `status: removed` component is skipped; add a per-consumer **last-deployed sidecar** (the
  floor-carrier precedent) so `detect_prune` classifies a source-drifted component against the
  bytes actually deployed, not the current manifest.
- **#246:** once #245 lands, prune `hub-toc-hooks` and verify ABSENT with no re-create.
- **#276:** `detect_prune` consults a consumer-declared `.methodology.yaml` divergence-allowlist;
  a tombstoned component the consumer has claimed returns **SKIP / ALREADY_ABSENT** rather than
  REFUSE; a deployed consumer with **no** allowlist entry still REFUSEs (regression-pinned).

---

## Verify-at-build (the test each item must pass when built)
- **#275b:** the trip-test `tests/test_floor_conformance.py::test_arm_step_installs_all_three_hook_stages`
  (runs the carrier-written arm command; all three `.git/hooks/*` appear from absent) +
  `tests/test_deploy_floor.py::test_apply_arms_all_three_hook_stages` (content proof). **Green.**
- **#280:** a deployed synthetic consumer carries `docs/intake/README.md` + `templates/intake-template.md`.
- **#245:** a re-add run skips a `status: removed` component (no manual add-target drop); a
  source-drifted prune target classifies against last-deployed bytes.
- **#246:** hub-toc-hooks pruned + verified ABSENT with no re-create.
- **#276:** a divergence-declared tombstoned component → SKIP on a previously-deployed consumer;
  a no-allowlist deployed consumer still REFUSEs (both pinned).

---

## Deferred (ADR-81(d) — the release_lint gap)
This arc lands **design-only** for the release manifest, so `release_lint.py --version 1.3.0`
does **not** pass — it FAILs C1 immediately with "no manifest for v1.3.0" (the manifest does not
exist). That is the entire lint gap. A real v1.3.0 cut reconciles it by:
1. Author `deploy/manifest-v1.3.0.yaml` (copy `manifest-v1.2.0.yaml`).
2. `methodology_version: "1.3.0"` + `source_tag: v1.3.0` (release_lint C1).
3. precommit carrier `hub_hooks.rev: v1.3.0` (C3) — a real deployed-content change, reconcile
   only at the actual release.
4. `anchors.plugin_version` == live `plugin.json` (C4) — currently `0.1.10`; carry forward
   unless the plugin ships a new version.
5. `anchors.floor_sha256` == sidecar == recomputed template bytes (C5) — **#275b does NOT touch
   the floor template** (it changes carrier code, not the floor body), so the existing sha
   carries over verbatim.
6. Add v1.3.0 `components:` / `engages:` rows for whatever v1.3.0 ships (#280 intake component,
   the #245/#276 engine behaviors); keep C6/C8 well-formed.
7. Operator tags `v1.3.0` at release (C2 is WARN until the tag exists → passes on tag).
8. Wire `release_lint` into the `deploy/tool.py` preflight if anchor-consistency should gate at
   deploy (it is manual-only today — an unclaimed follow-up).

**#275b is the sole BUILD-NOW.** #280 / #245 / #246 / #276 are specified here and built in the
release-cut arc that authors the manifest, tags, and deploys.

---

## Consequences
- **Methodology version HELD at v1.2.0.** Only #275b code lands (undeployed engine code); the
  registry and manifest are untouched. No `release_lint` / roster / freshness gate fires from this
  lane.
- **#275b residual (deferred, minimal-fix rationale).** This arc landed the arm-command constant
  + tests only. Two follow-ups remain, filed to the grooming batch (not edited into BACKLOG from
  this lane — single-writer): **(a)** give the floor carrier's `detect`/`verify` teeth that assert
  the 3-stage arm (today they assert only the verify leg, so `verify()` still passes on a 1-stage
  arm); **(b)** relax `_ensure_settings` so a re-deploy against an already-armed 1-stage consumer
  self-heals the stale arm. Deferred deliberately: adding a DRIFTED verdict without the self-heal
  would make `detect` report drift `apply` cannot repair, and no consumer is deployed from this
  lane — so the honest fix ships with the next real deploy.
- **The next real deploy arc** authors `manifest-v1.3.0.yaml`, closes the ADR-81(d) lint gap,
  builds #280 / #245 / #246 / #276, tags `v1.3.0`, and deploys — carrying #275b to consumers then.

## Links
- `deploy/carrier_floor.py` (#275b constant) · `deploy/tool.py` / `deploy/contract.py` (#245/#276) ·
  `deploy/carrier_precommit.py` (#276 `detect_prune`) · `deploy/manifest-v1.2.0.yaml` (copy-source) ·
  `deploy/release_lint.py` (C1–C8) · `protocols/REPO_ONBOARDING.md` (the onboarding half; relocated from `docs/runbooks/` per the ADR-101 amendment 2026-07-22) ·
  `docs/audits/2026-07-08-fleet-consistency-census.md` (the fleet-state evidence).

---

## Addendum 2026-07-11 — #302 / #309 commit-discipline carriers (LANE-B arc)

> **Provenance.** Two scope items added after the 2026-07-08 draft. Their **hub-side carrier
> engine landed in the LANE-B arc** (branch `feat/302-309-carriers`): the `block-ff-push`
> hub-source entry in `.pre-commit-hooks.yaml` (commit `6b15709`) + firing tests (commit
> `dfa2427`). Per the version-provenance note above, **the methodology version stays HELD at
> v1.2.0** — the hub-source entries are undeployed engine code (the `[NB]` precedent); the
> `manifest-v1.3.0.yaml` rows below are **specified ready-to-paste and DEFERRED to the
> release-cut arc**, alongside #280/#245/#246/#276. Nothing here is deployed to a consumer.

### 3.5 #302 — pre-push `block-ff-push` carrier · hub-side BUILD landed; manifest DESIGN-DEFER
- **What:** expose the pre-push gate (`scripts/block_ff_push.py`, core-invariant #5 prevent
  organ) as a hub-source hook so a consumer inherits push-time direct-to-main / FF protection.
- **Why:** the 2026-07-08 census (Part 5) witnessed every deployed consumer's pre-push stage
  **armed-but-empty** — the stage installs (#275b) but no hub gate carries into it; a direct
  commit to `main` lands push-able on ai-council (F1/N4) and corp (morning-brief §5).
- **Portability:** the mechanism is fully generic — range resolution (native-stdin + pre-commit
  `PRE_COMMIT_*` env), `PROTECTED_REF=refs/heads/main`, fail-soft (exit 0 on any git error). The
  `BASELINE_DATE=2026-06-15` grandfather is a hub-history artifact but a **non-issue for
  consumers**: a normal push scans only the incoming range (`remote..local`), so already-pushed
  legacy commits are never rescanned; only a fresh-remote first push scans full history. The
  hard `import validate_no_ff` means the carrier ships both scripts from the same hub clone.
- **Acceptance (BACKLOG #302 Done-when):** "a consumer gains the guard, verified FIRING on a
  direct-to-main push, with tests." **Met hub-side** by the `@requires_precommit` E2E
  (`tests/test_carrier_hooks_source.py::test_carried_block_ff_push_refuses_direct_to_main` — a
  throwaway consumer installs the hub-source hook and its direct-to-main push is REFUSED).
  The per-consumer install/verify is the named rollout follow-up.
- **Surface:** `.pre-commit-hooks.yaml` (landed) + the manifest rows below (deferred).

### 3.6 #309 — commit-msg gate parity · portable subset carried; filing-backpressure hub-only
- **What:** carry the *portable* commit-msg gate — `backlog-id-on-close`
  (`scripts/check_backlog_commit_msg.py`), already exposed in `.pre-commit-hooks.yaml`.
- **Portability decision (operator, 2026-07-11):**
  - **`backlog-id-on-close` — CARRIED.** Portable: a consumer with a `- [#id]` story-map
    BACKLOG.md inherits close-traceability; a consumer without one is **fail-open** (empty
    `git diff -- BACKLOG.md` → no removed ids → pass), so shipping it is safe fleet-wide.
  - **`backlog-filing-backpressure` — HUB-ONLY-BY-CONSTRUCTION (not carried).** Reason: its
    Leg-1 `kill-candidates:` filing-discipline (PLAYBOOK §10) and Leg-3 intake / `[P1-3][L]`
    size-band advisory (ADR-98 §3) are **hub methodology conventions not fleet-adopted** —
    carrying Leg-1 would impose the hub's paired-removal ritual on every consumer commit that
    adds a task, and Leg-3 depends on hub-specific size-band + intake-doc notation. Recorded
    per #309's "or each is recorded hub-only-by-construction with a reason" clause. Pinned by
    `tests/test_carrier_hooks_source.py::test_filing_backpressure_not_carried`.
- **Acceptance (BACKLOG #309 Done-when):** "the portable commit-msg gate(s) ship to a consumer
  via a manifest carrier, verified firing on a seeded violation, with tests (or each is recorded
  hub-only-by-construction with a reason)." **Met hub-side** by the carried-gate E2E
  (`::test_carried_backlog_id_blocks_unreferenced_close` — a consumer removing a `- [#id]` line
  without citing the id is BLOCKED) + the filing-backpressure hub-only record above.
- **Surface:** `.pre-commit-hooks.yaml` (`backlog-id-on-close` already present) + manifest rows below.

### Prune-scoping interaction (verified live 2026-07-11)
Per-consumer prune scoping (#276 / #245) **does not exist** — both OPEN / design-deferred (§3.3,
§3.4). There is **no** per-component `hub_only` / `scope` / `targets` field; transferability is
decided by manifest **inclusion vs omission**. These two carriers are **add-path only** — they
add `status: active` components, never a `status: removed` one — so the ADR-96 remove/prune leg
is **not engaged** and the #276 REFUSE-forcing-function is not touched. No prune dependency; the
additions are safe to paste into a v1.3.0 cut ahead of #276 landing.

### Ready-to-paste `manifest-v1.3.0.yaml` rows

At the release cut, alongside the §Deferred recipe (bump `methodology_version` / `source_tag` /
`hub_hooks.rev` to `v1.3.0`), add to the **`precommit` carrier** `target.hub_hooks`:

```yaml
        marker_hook_ids:
          - block-ff-push          # NEW (#302); backlog-id-on-close already a marker
        hooks:
          - id: block-ff-push      # NEW (#302)
          - id: backlog-id-on-close # NEW (#309) — entry already in .pre-commit-hooks.yaml
```

and two `components:` rows (model: the `hub-toc-hooks` component). Calibrate each `expect:`
substring against real hook output at the cut, per the `hub-toc-hooks` `[#253c]` precedent
(`block_ff_push` emits its refusal on stderr; pre-commit surfaces hook output regardless of stream):

```yaml
  - id: hub-block-ff-push
    kind: hook
    carrier: precommit
    status: active
    waivable: false   # core-invariant #5 main-branch protection is universal; inert (never fires)
                      # on a non-main default branch rather than needing a waiver
    verify: wired
    engages:
      trigger: pre-push
      observable: hook-stdout
      expect: "REFUSED"            # calibrate@cut: "REFUSED — N non-merge commit(s)…"
      scope: "FIRES on a push adding a non-merge commit to main's first-parent spine; a --no-ff merge or non-main push passes; fail-soft exits 0 on git error"
    artifacts:
      - wiring: ".pre-commit-config.yaml repo <hub> rev == source_tag, hook block-ff-push (ships scripts/block_ff_push.py + scripts/validate_no_ff.py)"
    roster:
      section: precommit-hook
      line: "block-ff-push — pre-push gate; refuses direct-to-main / FF push (core-invariant #5 prevent)"

  - id: hub-backlog-id-hook
    kind: hook
    carrier: precommit
    status: active
    waivable: true    # needs a consumer BACKLOG.md with the `- [#id]` story-map format; a repo
                      # without one is fail-open (empty diff -> pass), nothing to gate
    verify: wired
    engages:
      trigger: commit-msg
      observable: hook-stdout
      expect: "removed but not referenced"   # calibrate@cut
      scope: "FIRES on a commit removing a `- [#id]` line from BACKLOG.md without [#id] in the message; a consumer without BACKLOG.md is fail-open"
    artifacts:
      - wiring: ".pre-commit-config.yaml repo <hub> rev == source_tag, hook backlog-id-on-close (ships scripts/check_backlog_commit_msg.py)"
    roster:
      section: precommit-hook
      line: "backlog-id-on-close — commit-msg gate; require [#id] when a BACKLOG task line is removed"
```

`backlog-filing-backpressure` gets **no component row** (hub-only-by-construction, above). After
pasting, `python deploy/release_lint.py --version 1.3.0` (C6 wants both new components to resolve
their carrier + carry `waivable` + `engages`; C3 wants `hub_hooks.rev == source_tag`) and
`python scripts/gen_methodology_roster.py --write` (regenerates `.claude/methodology-roster.md`,
gated by `roster-freshness`) reconcile the cut.

## Addendum 2026-07-18 — ARC 4 leg 1 fleet ruff-shape + pytest-floor equalization

### 3.7 ARC 4 leg 1 — fleet ruff-shape + pytest-floor equalization · MATERIAL (satellite wave frozen)
- **What:** the equalized fleet ruff SHAPE (`required-version` `>=0.15.5` · `target-version`
  `py311` · `line-length` `120`) + the declared pytest floor (`minversion` `9.0`), each with
  RULING-S reader-visible `=== UNIVERSAL ===` / `=== REPO-PERSONAL ===` section headers in every
  governed `pyproject.toml`.
- **Rulings (2026-07-18):** RULING-PY (py311 baseline; "always newest Python" lift tracked as
  #351), RULING-S (reader-visible universal/personal split), RULING-W (consumer writes via
  worktree/branch → report; per-consumer merge GO with the operator).
- **Canonical source:** `templates/ruff-config-block.toml` — copy-paste MATERIAL. A `pyproject.toml`
  is repo-authored and carries much else, so these blocks are HAND-MERGED per RULING-W, never
  file-copied over an existing pyproject.
- **Carrier posture — MATERIAL ONLY, not a manifest cut:** the satellite wave is FROZEN until corp
  + ai-council lessons are extracted (operator standing ruling). This section is the
  ready-to-replicate spec; **no** `manifest-v*.yaml` row is cut here. When the wave thaws, the
  shape ships as a documented pyproject-fragment carrier (or a pyproject-merge helper), NOT a
  whole-file `path`/`source` carrier (which would clobber a consumer's pyproject).
- **Divergence handling:** the three ruff keys + `minversion` are `fleet_parity`-gated; each repo's
  lint posture (`select` / `ignore` / `per-file-ignores` / `format`) and pytest markers stay
  REPO-PERSONAL, declared in `.methodology.yaml` (the #328 mechanism). An undeclared divergence
  WARNs in the nightly ecosystem audit.
- **Live application (ARC 4 leg 1):** hub `pyproject.toml` equalized on
  `feat/arc4-leg1-ruff-equalization`; consumers (corp-monorepo, ai-council) via per-consumer
  RULING-W worktrees, each commit-and-STOP + report.

## Addendum 2026-08-08 — the #275b residual is CLOSED (BACKLOG [#290])

> **Supersedes the two open items in §Consequences "#275b residual (deferred, minimal-fix
> rationale)".** That paragraph stays as written — it is the accurate record of what the
> Wave-1 prep lane deferred and why; this addendum records that both halves have since
> landed, so the paragraph's "Two follow-ups remain" no longer describes live state. Built in
> the batch-4 lane `worktree-lane-290-floor-teeth`, commit-and-STOP (integration serialized
> through the primary).

Both halves shipped together, as the deferral rationale required — a DRIFTED verdict `apply`
cannot repair was the whole reason they were held as a pair:

- **(a) teeth.** `deploy/carrier_floor.py` `detect` + `verify` now assert BOTH SessionStart
  legs, and the arm leg at **full stage cardinality**. Previously only the verify-leg sentinel
  (`check_floor_hash.py`) was checked, so a consumer armed by a pre-#275b deploy — a bare
  `python -m pre_commit install`, arming the pre-commit stage only — classified
  `PRESENT_CORRECT` and verified green with its commit-msg / pre-push stage hooks
  wired-but-dormant. `verify` now names the dormant stages ("arms 1/3 managed hook stage(s) —
  commit-msg, pre-push would land wired-but-dormant"); `detect` returns `PRESENT_DRIFTED`.
  D9 preserved: subset test in `detect`, dormant-list re-derivation in `verify`; the shared
  additions are SPEC parsers only.
- **(b) self-heal.** `_ensure_settings` no longer no-ops on the mere presence of the verify
  leg. An under-armed arm leg is repaired **in place** — only that hook's `command` string is
  rewritten; its other keys (including a consumer-tuned `timeout`), the verify leg, sibling
  SessionStart hooks, matcher groups, ordering and every unrelated `settings.json` key are
  left verbatim. The two mirror gaps (arm leg absent / verify leg absent) now each add back
  just the missing leg instead of appending a duplicate guard block. Coverage is judged as a
  union across arm legs, so a complete-but-split arm is correctly a no-op.

**Stage cardinality is now single-sourced.** `carrier_floor.ARM_HOOK_TYPES` **is**
`scripts/arm_hooks.py::HOOK_TYPES`, and `_SESSIONSTART_ARM_CMD` is derived from it rather than
re-declaring the `-t` flags — so §3.1's "mirrors the hub's own `scripts/arm_hooks.py`" is
mechanically enforced, not a convention. The emitted command is byte-identical to the #275b
constant (`fc8e4ef`), so **no deployed byte changes and no version anchor moves**: this stays
undeployed carrier engine code under the same `[NB]` precedent as #275b itself.

**Verify-at-build** (join the §Verify-at-build list): `tests/test_deploy_floor.py` 23 → 96,
including the three frozen assertions — a 1-stage-armed fixture FAILs `verify`; one re-deploy
leaves it 3-stage-armed and verify-green, repaired in place; an already-3-stage fixture is
byte-identical after re-deploy. **Trip-tested against the pre-#290 carrier: 9 of the new tests
fail there** (`verify` returns ok on a 1-stage arm, `apply` reports `changed=False`, and the
old verify-leg-less path appends a duplicate arm leg), so the teeth are witnessed, not assumed.

Most of that test growth is **adversarial parser coverage**, not the frozen assertions. Five
`/codex-review` (terra) passes over this diff each found a real way to read an arm command
wrongly, and the count is the residue of closing them: a whole-token scan credited
`install-hooks -t …`; a preceding-token rule credited `echo pre-commit install -t …`; a
word-bag runner prefix credited `python pre-commit install` (no `-m`); an invocation that
argparse REJECTS (`-t bogus`, a valueless `-t`, `-t==stage`) was credited with its valid
flags. Every one of those is a false `PRESENT_CORRECT` — the dormant-stage defect #290 exists
to close, reachable through the teeth themselves — and each is now a pinned table row. The
opposite direction is pinned too, because it is the damaging one: a genuinely-armed consumer
misread as stale would have `apply` REWRITE its command, so `--hook-type=X`, `-t=X`, quoted
values, a `VAR=value` prefix, `uv run` / `uvx` / `poetry run` / `py -3.12 -m` runners, a POSIX
line continuation and an uppercase Windows `PRE-COMMIT.EXE` path are each proven a
byte-identical no-op for `apply`.

**Stated limit** (honest, and deliberate): a command that hides its invocation from static
reading — `sh -c '…'`, a shell function, a wrapper script — is NOT recognised, so it reads as
no arm leg. `apply` then ADDS a canonical arm leg beside it and never rewrites the opaque
command, so the wrapper's behaviour survives even though it cannot be understood. Erring
toward "not armed" is the safe direction: it yields a repairable verdict, never a false green.

**Known-stale sibling claims, NOT touched by this lane** (held by other lanes / other owners;
reported, not fixed): the `floor-sessionstart-guard` roster line in `deploy/manifest-v1.1.0`
through `-v1.4.0.yaml` and `.claude/methodology-roster.md` still renders the arm leg as
`python -m pre_commit install` with no stage flags, and `deploy/floor_conformance.py`'s
`assert_sessionstart_wired` still asserts only that *an* arm leg exists, not its cardinality —
a weaker check than the carrier's own, though not a contradicted one.
