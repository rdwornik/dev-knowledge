# Two rows, reconciled before birth — ready to file, NOT filed

**Batch:** night-batch-2 post-night arc · **Lane:** `pn-audits` (contract addition) · **Date:** 2026-08-29
**Repo:** `.dev-knowledge` @ `worktree-pn-audits`, cut from `66662c70`
**Rows written:** **ZERO.** See §0 — this lane cannot write `tasks/`, and the reason is mechanical, not procedural.

---

## 0. WHY THESE ROWS ARE DRAFTED HERE AND NOT FILED — read this first

This lane's frozen contract assigns it **`docs/audits/**` and `LESSONS.md`, exclusively**, and states in as
many words: *"You may NOT create backlog rows (`tasks/` belongs to a sibling lane)."* The sibling lane
`pn-filings` owns `tasks/`, and it is **live right now and already committing into it** — measured, not
assumed:

```
git -C .claude/worktrees/pn-filings log --oneline -2
  bf1f2cac  docs(tasks): A3 + C8 amended on their existing rows -- [#610] leg 3
            discharged, [#130] gets a measured trigger
  66662c70  Merge branch 'docs/batch-2-w2-packet' ...

git -C .claude/worktrees/pn-filings diff --name-status 66662c70..HEAD -- tasks/
  M  tasks/130-memory-hygiene-review.md
  M  tasks/610-the-night-batch-protocol-named-with-its-two-verb.md
```

Two lanes writing `tasks/` in parallel is the exact collision the batch protocol exists to prevent: the
directory is also the source for `gen_task_tree.py --emit-source` and the `BACKLOG.md` view, so a
concurrent write does not merely conflict — it makes the generated surface a coin-flip on merge order.
**So the substance is done here in full and the two-file write is handed to `pn-filings` or the
integrator.** Everything below is paste-ready: frontmatter, body, `kill-candidates`, and the commit-message
line the `backlog-filing-backpressure` hook requires.

**Ids are PROVISIONAL.** Next-free is **616** and **617**, computed as max-on-disk (`615`) + 1. The
`[#777]` that a history scan returns is a **documented synthetic false positive** — trip-test prose,
excluded by precedent in `c2f10440`. If `pn-filings` births a row before these land, re-number; nothing
below depends on the specific integers.

**Theme/story are PROPOSED, not ruled** — placement derives theme in this repo, and placement is the
filer's act.

---

## 1. RECONCILE — does an existing row already cover W4 defect 3?

**Searched, not assumed:** `grep -rln "W4" tasks/` returns two files (`tasks/550-*.md`,
`tasks/manifest.json`), neither about the codespace. `grep -rln "codespace" tasks/` returns five rows.
The only real candidate is **`[#593]`**, and it is a close call that deserves the paragraph it gets.

**`[#593]` describes defect 3 in its narrative:**

> *"…and the prebuilt image served a clone stale by three days while `git status -sb` reported no
> divergence, so the very merge declaring the Claude Code install was missing."*

**But its Done-when does not own the fix.** `[#593]`'s three clauses are (a) a one-shot smoke-6 receipt
(`Ok=True` ∧ `RemoteExitCode=0` ∧ receipt HEAD == pushed HEAD), (b) `uv` on PATH at the pinned version, and
(c) the copy-leg defect fixed or recorded as operator-side.

Clause (a) **would detect** a stale clone at receipt time — that is real overlap and it is recorded here
rather than glossed. But it is an **acceptance test run once**, not a **standing detection mechanism**, and
the operator's ruling is specifically that *"a rebuild is a workaround, not the fix."* A row whose
done-when is satisfied by one green receipt cannot carry a mechanism that must fire on every session entry.

**There is also a shape difference between the two reproductions, and it matters:**

| | `[#593]`'s original (three days stale) | today's (50 commits stale) |
|---|---|---|
| `git status -sb` | *"reported no divergence"* | **`## main...origin/main [behind 50]`** — it DID report |
| what failed | git itself was wrong | git was right; **nothing in the session surfaced it** |

**Verdict: BIRTH, on a proven gap** — the gap is the standing detection/refresh mechanism, not the
one-shot receipt. `[#593]` is cited as the sibling and is **not** killed.

---

## 2. ROW 1 — ready to file as `tasks/616-...md`

```yaml
---
id: "[#616]"
title: "The silently-stale codespace clone — detection and refresh-on-entry, not a rebuild"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---
```

Body (one line in the file, wrapped here for reading):

> - [#616] [P2][M] **The silently-stale codespace clone — detection and refresh-on-entry, not a rebuild**
> — W4 defect 3, reproduced live 2026-08-29. Codespace `nb2-smoke6c-j47pvjw957ghq76v`
> (`rdwornik/dev-knowledge`, branch `main`) presented a clone **50 commits behind** with nothing in the
> session surfacing it: in-container `HEAD` = `770961316fdb176cd0cafd2d9d9b1fe3c8cc4c01`, pushed
> `origin/main` = `66662c7043c18022e6558ad8a8b738fde4dce83d`, `git status -sb` = `## main...origin/main
> [behind 50]`, in-container HEAD commit date `2026-08-29T11:02:26+02:00` (measured 2026-08-29T12:37Z).
> **CONTRAST, same probe, 8 minutes later on a FRESH codespace** `orange-happiness-pgw54jq9rqwhq6g`
> (created 2026-08-29T12:48Z, `basicLinux32gb`): `PWD=/workspaces/dev-knowledge`, `HEAD` =
> `66627c70…` == pushed HEAD (**match**), `git status -sb` = `## main...origin/main` (**no "behind"**),
> `CDATE=2026-08-29T13:44:58+02:00`, `UV=uv 0.11.19` (**exactly the ADR-106 pinned
> `required-version = "==0.11.19"`**), `TOKEN_LOGIN` PRESENT len=108, `RemoteExitCode=0`. **HYPOTHESIS, not
> a finding:** the two paired readings are consistent with W4 defects 2 and 3 sharing ONE root cause —
> **codespace AGE / drift of a long-lived container**, rather than two independent image defects — since a
> fresh instance reproduces neither. **Two paired readings are suggestive; one pair is not a controlled
> experiment**, and this row does not assert the hypothesis as fact. **Neither W4 defect is closed by this
> row:** non-reproduction on a fresh instance is not a fix, and closure is the operator's call. **A rebuild
> is a workaround, not the fix** — the missing mechanism is (i) DETECTION that surfaces clone divergence at
> session entry, and (ii) a refresh-on-entry discipline. · **Done when:** a session entering a codespace
> surfaces clone-vs-`origin` divergence without the operator running `git status` by hand, AND a
> refresh-on-entry step is either armed or explicitly recorded as operator-side; the stale reading above is
> the regression case · **refs** `[#593]` (sibling — hub-half chain repair; its Done-when clause (a) tests
> receipt-time HEAD equality but owns no standing mechanism), `docs/audits/2026-08-29-verification-night-mission-close-packet.md`
> (W4 defects 1–3), `docs/audits/2026-08-28-technical-batch-2-manifest.md`, ADR-106, `[#554]`, `[#567]` ·
> **source:** operator ruling 2026-08-29 (*"file the 50-commits-stale clone as the live reproduction of W4
> defect 3 — its own row"*) + the paired probe readings above · **kill-candidates:** none — `[#593]`
> repairs the hub-half chain and its Done-when is a one-shot receipt; this row is the standing detection
> mechanism, and killing either leaves the other's gap open · **serialize-group:** none

**Commit-message line the `backlog-filing-backpressure` hook requires** (flush-left, its own line):

```
kill-candidates: none — [#593] is the hub-half chain repair with a one-shot receipt Done-when; this row carries the standing detection mechanism it does not own
```

---

## 3. ROW 2 — the FM-2 ↔ FM-4 coupling, VERIFIED DEAD (and the brief's framing corrected)

### 3.1 · I re-measured it rather than relaying it, and one half of the premise does not hold

**Confirmed, exactly as briefed** — the coupling is dead. `funnel_lifecycle.measure` resolves cleanly, and
the six attributes `gen_handoff` reads have **zero overlap** with what `Measurement` exposes:

```
$ uv run --locked python -c "...gen_handoff._load_funnel_measure() / funnel_lifecycle.measure(...)"

resolve fn:            <function measure at 0x...>          -> resolves
resolve note:          ''                                    -> inner note IS empty
Measurement attrs:     archived_intakes, by_leg, detector, live_adrs, live_intakes,
                       post_cutoff_rows, ready_intakes, rows, threshold_days,
                       threshold_locator, violations                        (11)
gen_handoff _FUNNEL_FIELDS: intakes_consumed_unarchived, adrs_unexecuted, orphans_forward,
                       orphans_backward, rows_closed_this_window, value_evidence_attached  (6)
                       -> INTERSECTION: ZERO
```

**But the briefed consequence — *"every existing degrade-path message says nothing is wrong"* and *"the
well-built honest-degrade path is exactly what hid it"* — is FALSE, and I only know because I rendered the
block instead of reading the code.** `_load_funnel_measure`'s note is empty (that is the *inner* note, and
it is empty precisely because the module imported fine), but the note that actually reaches the bundle
comes from `funnel_health_numbers`, and it is fully populated:

```
source: scripts/funnel_lifecycle.py::measure (FM-2) — fields absent from the measurement:
intakes_consumed_unarchived, adrs_unexecuted, orphans_forward, orphans_backward,
rows_closed_this_window, value_evidence_attached

intakes consumed-unarchived: unavailable
ADRs unexecuted: unavailable
orphans forward (object -> consumer): unavailable
orphans backward (open row -> resolving source): unavailable
rows closed this window: unavailable
value evidence attached: unavailable
```

**So the degrade path did not hide the failure — it announced it, by name, in every bundle it rendered.**
The failure is not silent; it is **announced and unread**. That is a materially different defect, and it
changes what the repair lane must fix: **not** a missing detector, but a block nobody reads. Adding a
detector for a condition already printed in full would be building the organ that already exists.

This correction is recorded here rather than smoothed over, per the repo's own rule that a transferred
fact carries a locator or is derived on site.

### 3.2 · Ready to file as `tasks/617-...md`

```yaml
---
id: "[#617]"
title: "The FM-2 ↔ FM-4 funnel-health coupling is dead — six fields, zero overlap"
status: open
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---
```

> - [#617] [P2][M] **The FM-2 ↔ FM-4 funnel-health coupling is dead — six fields, zero overlap** —
> `gen_handoff.funnel_health_numbers` reads six attributes (`intakes_consumed_unarchived`,
> `adrs_unexecuted`, `orphans_forward`, `orphans_backward`, `rows_closed_this_window`,
> `value_evidence_attached`); `funnel_lifecycle.Measurement` exposes eleven (`detector`, `live_intakes`,
> `archived_intakes`, `live_adrs`, `rows`, `post_cutoff_rows`, `ready_intakes`, `threshold_days`,
> `threshold_locator`, `violations`, `by_leg`). **The intersection is EMPTY**, so every handoff bundle's
> FUNNEL HEALTH block has rendered six `unavailable`s. `_load_funnel_measure` resolves cleanly and its note
> is `''` — the module imports fine; the break is downstream of resolution.
> `docs/audits/2026-08-29-technical-nb2-k-packet.md` recorded FM-4 done-when #4 as *"MET as written,
> coupling UNPROVEN"*; it is now **PROVEN, and broken** (measured 2026-08-29 on `66662c70`). **CORRECTION
> to the first report of this defect, measured rather than reasoned:** the degrade path does **not** hide
> it — `funnel_health_numbers` emits `fields absent from the measurement: <all six, by name>` into the
> rendered block, so the failure has been **announced in every bundle and simply not read**. The repair is
> therefore a reader/consumer problem plus a mapping, not a missing detector. **Scope:** the repair is a
> **DERIVATION-DESIGN decision** — which `violations`/`by_leg` entries or corpus counts map onto each of the
> six fields — **not a rename**; this row deliberately proposes no mapping, because choosing it is the
> repair lane's first ruled act (operator ruled 2026-08-29 that this gets its own frozen lane in the next
> batch). · **Done when:** each of the six fields either renders a derived number or is removed from
> `_FUNNEL_FIELDS` by a recorded ruling, with a test that fails if the two surfaces drift apart again —
> the zero-intersection state must not be re-reachable silently · **refs**
> `docs/audits/2026-08-29-technical-nb2-k-packet.md` (FM-4 done-when #4; candidate CF-1),
> `docs/audits/2026-08-29-technical-nb2-l-packet.md` (candidates 1–2 — the emitter-resolution and
> duplicate-metric-owner questions this row's lane must settle with it),
> `docs/audits/2026-08-29-verification-wave-2-close-packet.md` §8 item 1, `scripts/gen_handoff.py`,
> `scripts/funnel_lifecycle.py` · **source:** operator ruling 2026-08-29 (own frozen lane, next batch) +
> the live measurement above · **kill-candidates:** none — `[#602]` is the v5 forms machinery and
> `[#591]` is the freeze-predicate organ; neither reads or writes `_FUNNEL_FIELDS`, so killing either
> leaves this coupling exactly as dead · **serialize-group:** none

**Commit-message line** (flush-left, its own line):

```
kill-candidates: none — [#602] and [#591] are the adjacent handoff/freeze organs and neither touches _FUNNEL_FIELDS; killing either leaves the dead coupling untouched
```

**Placement note for the filer:** theme is proposed as `[E1] Handoff continuity` because the defective code
is `gen_handoff`'s bundle block. `[E2] Enforced governance` is the defensible alternative, since the
*subject* is funnel measurement and `[#591]`/`[#615]` sit there. Placement derives theme — the filer's call,
and either is honest.

---

## 4. Refused, deferred, and owed — named plainly

- **The two `tasks/` writes are REFUSED by this lane**, on the frozen contract plus the measured live
  collision in §0. Not a judgment about the rows — both are ready, and I would file them if the scope were
  mine. **Handed to `pn-filings` or the integrator.**
- **Ids 616/617 are provisional** and may be taken by `pn-filings` before these land.
- **Neither W4 defect is recorded as closed**, per the operator's instruction: non-reproduction on a fresh
  instance is not a fix, and Z-G3's entry condition U(b) requires all three W4 defects CLOSED.
- **The root-cause hypothesis in §2 is labelled a hypothesis** and is not asserted as a finding. One pair
  of readings is not a controlled experiment; the cheap next probe is a third reading on a *different*
  long-lived codespace, which would move it from suggestive to supported.
- **`docs/audits/README.md` left STALE by design** ([#590]); the integrator owns it.
