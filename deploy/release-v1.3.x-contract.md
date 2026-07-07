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
  `deploy/release_lint.py` (C1–C8) · `docs/runbooks/repo-onboarding.md` (the onboarding half) ·
  `docs/audits/2026-07-08-fleet-consistency-census.md` (the fleet-state evidence).
