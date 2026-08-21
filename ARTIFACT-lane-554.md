# ARTIFACT — lane-554 cloud provisioning (batch 1, lane B)

> **Status: STUB (step 1 of 6).** Legs and their acceptance are enumerated here BEFORE any
> is executed, per the frozen contract's step 1. Every row below is filled in as its leg
> lands; a leg that cannot land is reported blocked-with-reason rather than dropped.
>
> Contract: `LANE-554-cloud-provisioning.md` (frozen, operator-held) · Row: `BACKLOG.md`
> `[#554]` · Branch: `worktree-lane-554-cloud-provisioning` · Repo: `.dev-knowledge`.

## 0. What this lane inherited (read before the leg table)

`[#554]` is **not** a green-field row. Five commits already landed `.devcontainer/` on `main`
(`2330e0fd`, `876e288d`, `57313811`, `b3060764`, `1c6e07cc`), and two prior artifacts measured
the result:

- `docs/audits/2026-08-19-technical-554-proof.md` — the proof lane. Verdict: **all four legs
  plus the C1/C2 obligations assert clean on the Codespaces free tier** (§2); `audit.py health`
  **RED** with 2 FAILs; `pytest -m "not slow"` **RED** with 8 failures; `devcontainer up`
  off-Codespaces **BLOCKED** (no container runtime on the workstation).
- `docs/audits/2026-08-20-technical-codespaces-audit.md` — the substrate audit, whose §4.5
  LEAN v2 was **accepted verbatim as the ruling**. It re-measured lane J's clone-shape class
  from `main` instead of a probe branch and found `audit.py health` drops to **exactly one**
  `[!!]`: `repos registered (none)`.

So the question this lane answers is not "do the four legs work" — that is measured and
answered — but **what is still between the landed provisioning and the row's Done-when**,
plus the two contract amendments A3 and B1.

## 1. The legs and their acceptance

Row `[#554]` names four legs; the contract adds A3, B1 and the leg-4 library-first line. The
Done-when adds a fifth obligation nobody has been able to satisfy in a container, which this
lane treats as a leg rather than as an excuse.

| # | Leg (source) | Acceptance — what would make it true | Status |
|---|---|---|---|
| L1 | pinned-`uv` assert (row) | provisioned `uv --version` equals `pyproject [tool.uv] required-version`, and the pin is an exact `==` | *(pending)* |
| L2 | `git fetch --unshallow` (row) | `git rev-parse --is-shallow-repository` is `false` **and** the refs the spine-walking gates read resolve — see B1, depth alone is not sufficiency | *(pending)* |
| L3 | deterministic `pre-commit install`, all three hook types (row) | `pre-commit` / `commit-msg` / `pre-push` all present in the resolved hooks dir, pre-commit-managed, bound to a live interpreter | *(pending)* |
| L4 | env gate refusing a half-provisioned environment (row) | `provision.sh --gate` exits non-zero when a pin has moved, history is shallow, hooks are unarmed or the stamp is absent — **and writes its stamp where it says it does** | *(pending)* |
| L5 | `repos registered` — the row's Done-when D1a, not a named leg | `audit.py health` operational block reports at least one registered repo inside a single-repo container | *(pending)* |
| A3 | devcontainer prebuild — trigger *on configuration change*, region *EuropeWest*, template history *1* (contract) | the three settings are declared in a machine-readable home and a checker reports live drift; **plus** resume-vs-create wall-clock recorded from at least two timed runs | *(pending)* |
| B1 | spine-walking instruments vs a depth-limited clone (contract, **blocking**) | provisioning either (a) deepens/unshallows **before** any spine-walking instrument runs in a cloud lane, or (b) documents an explicit exclusion of those instruments from cloud lanes — and the artifact states **which and why** | *(pending)* |

## 2. Measurements

*(pending — the A3 warm-start table lands here)*

## 3. Proposed diffs (not applied)

*(pending — pre-commit hook entries are proposed as fenced diffs only; this lane edits no
`.pre-commit-config.yaml`, per the contract)*

## 4. Terra review tally

*(pending — step 5)*

## 5. Blocked / not done, with reasons

*(pending)*
