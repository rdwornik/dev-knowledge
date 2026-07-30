---
class: technical
date: 2026-07-30
slug: v6-open-questions-ruling-dossier
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-2026-07-30-boot-prep
anchor_sha: c8490c1d
consumer: incoming 2026-07-31 dev-knowledge architect boot
consumption_path: "branch -> local re-verification -> architect reads at boot"
inputs:
  - "docs/audits/2026-07-30-technical-v6-spec-sol-draft.md (OPEN questions 1-7)"
  - "docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md (A4/A7/A8/A10/A11)"
  - "docs/audits/2026-07-30-technical-intake18-ratification-record.md"
  - "docs/audits/2026-07-29-technical-intake18-ratification-dossier.md"
  - "docs/audits/2026-07-27-verification-handoff-process-audit.md (RM-7/RM-8, H2/H3)"
  - "scripts/verify_handoff_probes.py, scripts/assemble_paste.py, scripts/gen_handoff.py (live)"
---

# [#446] ruling dossier — the 7 sol-draft OPEN questions

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Produced on a cloud night-batch
> lane with no merge, no canon edit, no closure, and no ruling authority. Every card below is
> a *recommendation with evidence*, never a decision. Nothing here changes canon or the
> `[#446]` row.
>
> **Consumer:** the incoming 2026-07-31 dev-knowledge architect boot.
> **Consumption path:** branch → local re-verification → architect reads at boot.

## How to read this

One card per OPEN question from `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md`
§"OPEN questions" (all 7 covered). Each card carries: **options space** · **constraints quoted
from live code/spec with `file:line`** · **recommendation + evidence** · **what a wrong call
costs**.

**Anchor discipline.** Every `file:line` below was live-checked at branch base **`c8490c1d`**
and is marked **re-verify-at-ruling** — line numbers rot inside their own branch, so re-derive
by anchor TEXT before relying on any of them.

**Base-SHA note (read first).** The night-batch brief named base `main 470b24fa`. At lane-open,
`main` was **`c8490c1d`** — `470b24fa` is an ancestor, three commits behind, the intervening
commits being the 2026-07-31 architect bundle (`430450a8`, `69d49b93`, `9bb0f05e`, `919351c3`,
`e0220815`). This lane branched from **`c8490c1d`** so anchors reflect the bundle the architect
will actually boot into. Flagging the divergence rather than silently honoring a stale SHA.

---

## Headline finding — four of the seven are not actually open

The single most useful thing in this dossier: **Q2, Q3, Q5, and Q6 are substantially already
settled** in surfaces that were **outside sol's pin set**, not genuinely undetermined.

The sol-draft's `pinned_inputs` (its frontmatter) list the intake-18 ratification record,
HANDOFF_PROCESS v5.7, **intake #19 §B item (b) lines 95-106 only**, the deferred-leg register,
and an `audit.py` span. They **do not include** `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md`
— the pack that *defines* A4's P3 comparison, A7's P0a/P0b/P0c contracts, and A11's RM-8
target. Sol correctly reported those as OPEN *relative to its pins*; that is a pin-scope
artifact, not a real gap in the record.

**Consequence for the architect:** treat Q2/Q3/Q5/Q6 as *confirm-and-narrow* (minutes each),
and spend the ruling budget on **Q1, Q4, and Q7**, which are genuinely undetermined.

| Q | Subject | Real status | Ruling effort |
|---|---|---|---|
| Q1 | Command name | GENUINELY OPEN | needs a naming ruling |
| Q2 | P0a/P0b/P0c contracts | DEFINED at intake; ONE stale locator | confirm + re-point P0a |
| Q3 | P3 comparison | DEFINED at intake A4 item 3 | confirm + settle 1-vs-4 fields |
| Q4 | Boot byte budget | GENUINELY OPEN + a which-file ambiguity | needs a number AND a target |
| Q5 | RM-8 targets/diagnostic | DEFINED at intake; refuse-vs-suffix conflict | resolve the conflict |
| Q6 | `repo_root`/`cross_repo` | ~90% determined by live code | confirm + CLI spelling |
| Q7 | `[#421]` tokenizer | GENUINELY OPEN (2 variants, 1 unnamed) | needs a scope ruling |

---

## Q1 — What command name exposes the one-round-trip boot?

**GENUINELY OPEN.** No pinned input rules one; the sol-draft says so explicitly at
`docs/audits/2026-07-30-technical-v6-spec-sol-draft.md:52` ("The command's public name is
`OPEN`; no pinned input rules one.").

### Constraints from live state (re-verify-at-ruling)

Live command surface at `c8490c1d`:

- Repo-level `.claude/commands/`: `changelog-review.md`, `handoff.md`, `override.md`, `save.md`
- User-level `~/.claude/commands/`: `codex-review.md`, `session-summary.md`
- Plugin `tier1-lifecycle@dev-knowledge-methodology`: `/review-closures`, `/ship`

**Hard constraint — `/boot` is archived and must not be resurrected.** `/boot` was archived
2026-06-05 to `~/.claude/archive/2026-06-05-machinery-c3/commands/`. `CLAUDE.md` §12 v2.37
records the [#330] root-archive-prohibition sweep that *removed* `/boot` from §6's
session-start protocol and from §7's "commands available" list on the explicit ground that
**"an archived command isn't available"**. Naming the new command `/boot` would reverse a
codified sweep and re-point a name whose archived content still exists — the exact defect
class §12 v2.37 was written to close.

**Soft constraint — a runnable core already exists.** `scripts/verify_handoff_probes.py:436`
already exposes `def main(argv=None) -> int` as a standalone CLI. The one-round-trip command is
naturally a *thin wrapper* over an extended version of that entrypoint plus the orientation and
inherited-claim legs — not a greenfield surface.

**Soft constraint — the existing `/handoff` is the sibling beat.** `.claude/commands/handoff.md`
is described in the generated roster as "Generate or complete a handoff per HANDOFF_PROCESS.md
v5 — CC-owned residual + thin browser boot". The new command is the *consume* half of the same
pipeline whose *produce* half is `/handoff`.

### Options space

| Option | Shape | For | Against |
|---|---|---|---|
| **A. `/boot`** | reuse the archived name | shortest; matches `HANDOFF_BOOT` vocabulary | **reverses the §12 v2.37 sweep**; collides with archived content; recommend against |
| **B. `/handoff-verify`** | new top-level command | names the actual action; pairs visibly with `/handoff` | slightly long; "verify" undersells the orientation + inherited-claim legs |
| **C. `/handoff --verify` (flag)** | subcommand of the existing `/handoff` | zero new command-surface entries; keeps produce/consume in one file | overloads a generator command with a checker mode; the roster line becomes two-purpose |
| **D. `/onboard`** | new top-level command | reads as the session-entry beat; short | new vocabulary not present anywhere in the corpus today |
| **E. `/boot-check`** | new top-level command | reuses the settled `BOOT` vocabulary WITHOUT reusing the archived name | mildly awkward; but no collision |

### Recommendation

**Option B, `/handoff-verify`** — with **Option E, `/boot-check`** as the close runner-up.

Evidence for B: it is the only option that (i) avoids the archived-`/boot` collision entirely,
(ii) sits in the same naming family as the command it consumes from (`/handoff`), and
(iii) describes the action the spec actually mandates — `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md:40-42`
defines the command as running "the entire live probe gate at check-time", performing
orientation reads, verifying inherited claims, and emitting one block. That is *verification*,
not booting.

Evidence against C (the tempting one): the spec's acceptance item 1
(`…sol-draft.md:233`) is "one CC-side command produces one complete evidence block". A flag on
a generator is still one command, so C satisfies the letter — but `gen_handoff.py:509`'s `main`
already carries seven-plus parameters, and folding a checker mode into it puts the answer-free
generator and the answer-producing checker in one surface. Given that the whole v6 reshape
turns on keeping generation-time answers OUT of bundles
(`…sol-draft.md:239`, acceptance item 7), a hard file-level separation between the thing that
*must never* hold answers and the thing whose *job* is to produce them is worth one extra
roster line.

### What a wrong call costs

- **Choosing `/boot` (A):** reopens a closed defect class; a future reader finds a live `/boot`
  and an archived `/boot` with different contracts. Cost is confusion plus a likely re-sweep.
- **Choosing C:** couples the answer-free invariant and the answer-producing checker in one
  file. The cost is not immediate breakage — it is that the machine-held "never the answer"
  contract (`…sol-draft.md:125-138`) loses its structural separation and reverts toward
  hand-discipline, which the record at `9d5ebe5` already showed regresses.
- **Choosing any name (B/D/E):** cheap and reversible. A command rename is a file move plus a
  roster regen (`python scripts/gen_claude_rosters.py --write`). **This is a low-stakes ruling
  — do not over-deliberate it.**

---

## Q2 — P0a/P0b/P0c's exact locators, commands, and honest-narrowed assertions

**NOT GENUINELY OPEN — defined at intake, one locator now stale.**

### The definitions already exist

`docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md:110-112` defines all three legs in a
four-column table (leg · question · binds to · CC verifies via), quoted verbatim:

- **P0a** — "Quote live the reconciliation-debt / preamble list of the active epic theme(s)";
  binds to "`BACKLOG.md` `[E#]` preambles (machine-locatable headers)"; verified by "read the
  live preamble; quote must substring-match".
- **P0b** — "Enumerate live every intake with `status: ACCEPTED, disposition: active` and quote
  each doc's TITLE line (its first `# ` heading)"; binds to "`docs/intake/*.md` frontmatter +
  first heading (both machine-locatable; frontmatter already parsed by `gen_intake_index.py`)";
  verified by "enumerate frontmatter → quote each live title".
- **P0c** — "State which enumerated standing authority (P0a epic theme / P0b intake) this
  bundle's Purpose serves — unquotable or contradicted = FAIL"; binds to "the bundle's own
  FILL-IN purpose vs P0a/P0b output"; verified by "compare; mismatch = FAIL, route to the
  escalation ladder".

The **honest-narrowing** the question asks about is also already ruled, at
`…v6-proposal.md:113`: "**Honest narrowing (terra H3):** P0b quotes titles, not wave detail —
wave/sequence content is unstructured prose today and quoting it would overclaim determinism".
This was a *verification finding*, adopted: `docs/audits/2026-07-27-verification-handoff-process-audit.md:131`
records "H3 A7's P0b overclaimed determinism on unstructured plan prose — the pack's own RM-4
law applied to itself (narrowed to machine-locatable titles + schema-change offered as option)".

A7 was then ADOPTED at `docs/audits/2026-07-30-technical-intake18-ratification-record.md:24`:
"§13(c) line ADOPT now; P0 legs DEFER … P0a/P0b/P0c probe legs land inside the §B(b)
one-evidence-block emission, not as ferry turns."

### The one genuine open — P0a's locator is stale post-[#439]

`docs/audits/2026-07-29-technical-intake18-ratification-dossier.md:123` already flagged it:
"P0a binds to `BACKLOG.md` `[E#]` preambles — post-flip ([#439]) BACKLOG.md is GENERATED".

Live-confirmed at `c8490c1d`, `BACKLOG.md:2-3`:

```
<!-- GENERATED FILE — do not edit directly. Source of truth: tasks/ (per-task .md bodies + manifest.json).
     Regenerate: python scripts/gen_task_tree.py --emit-source   ·   ADR-107 strangler step 3, [#439]. -->
```

The `[E#]` preambles **are still present** in the generated output (`BACKLOG.md:11` carries the
"Themes (backbone) — epic ids: [E1] … [E9]" line), so P0a is not *broken* — but it would bind a
teeth-bearing probe to a **derived artifact**. If `tasks/` has advanced and
`gen_task_tree.py --emit-source` has not been re-run, the probe reads a stale surface and
reports PASS against a value that is no longer true. That directly contradicts teeth condition 1
(`…sol-draft.md:93-95`, "Live-only answer").

### Options for the P0a re-point

| Option | Locator | Comment |
|---|---|---|
| **A. Keep `BACKLOG.md`** | generated file | simplest; accepts a generated-staleness window |
| **B. Re-point to `tasks/manifest.json`** | source of truth | honest per ADR-107; but the `[E#]` *preamble prose* lives in the emitted file, so the quote target changes shape |
| **C. Keep `BACKLOG.md` + add a generator-currency assertion** | both | probe reads BACKLOG.md AND asserts `gen_task_tree.py --check` is clean |

**Recommendation: Option C.** It preserves the ratified quote-substring assertion exactly as
written (no re-drafting of an adopted contract) while closing the staleness hole that makes the
probe bluffable. The repo already uses regen-and-diff `--check` gates as its standard currency
idiom — `CLAUDE.md` §9 lists at least six (`roster-freshness`, `claude-rosters-freshness`,
`audit-index-freshness`, `intake-index-freshness`, `codemap-freshness`, `toc-freshness-playbook`).
C is that idiom applied once more, not a new mechanism.

### What a wrong call costs

- **Leaving P0a on a generated file with no currency check (A):** the probe can PASS on stale
  content. A probe that can pass without the live answer being right is precisely the
  "bluffable" class the empirical promotion gate exists to reject (`…sol-draft.md:117-121`).
  This is the highest-consequence item in Q2.
- **Re-drafting P0b/P0c (unnecessary):** they were adopted with an explicit terra-H3 narrowing
  already applied. Re-opening them re-litigates a settled finding and risks silently widening
  P0b back onto unstructured wave prose — the exact overclaim H3 caught.

---

## Q3 — What two values does P3 compare, and what is PASS?

**NOT GENUINELY OPEN — defined at intake A4 item 3.**

### The definition already exists

`docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md`, §5 "A4 — Destination contract",
item 3, verbatim:

> the bundle `HANDOFF_BOOT.md` session-header table (slug · purpose · mode today) gains a
> **`Destination`** row (`worktree · branch · write-scope · MODE`), written by `gen_handoff.py`
> from its own invocation args … **P3 then extends: "state the live branch AND compare it to the
> boot-header `Destination` row; mismatch = FAIL."**

So: **operand 1** = the live branch, re-derived at check-time (`git rev-parse --abbrev-ref HEAD`);
**operand 2** = the `branch` field of the boot-header `Destination` row. **PASS = equal;
mismatch = FAIL.**

This was itself a verification fix, not a draft: `docs/audits/2026-07-27-verification-handoff-process-audit.md:131`
records "H2 A4's P3 comparison had no named destination field (boot-header `Destination` row
specified)" — i.e. the missing-operand problem Q3 asks about **was found and closed** at the
2026-07-27 audit.

The intake also pre-empts the obvious objection, same item: "the declared destination is a
contract to check against, not an answer hint (the existing PROBES branch-note precedent:
're-derive… do not trust this line')."

### The one genuine residual — one field or all four?

The `Destination` row carries **four** fields (`worktree · branch · write-scope · MODE`), but
the P3 sentence names only the **branch**. Two readings:

| Reading | Compares | For | Against |
|---|---|---|---|
| **A. Branch only** (literal) | live branch vs declared branch | exactly what the ratified sentence says; trivially deterministic | leaves worktree/write-scope/MODE declared-but-unchecked |
| **B. All four** | each field vs a live re-derivation | closes the whole destination contract | `write-scope` and `MODE` have **no mechanical live counterpart** — checking them would need unbounded judgment, which teeth condition 4 rejects |

**Recommendation: Option A (branch only) for v6, with `worktree` as an optional second
mechanical leg.**

Evidence: teeth condition 4, ratified at intake #18 and quoted at
`docs/audits/2026-07-30-technical-v6-spec-sol-draft.md:100-103` — "**Bounded-deterministic** —
the verification terminates in bounded mechanical steps at check-time. A probe whose honest
answer requires unbounded judgment over an open set is an arc, not a probe, and is rejected."
`write-scope` ("which paths may this lane write?") and `MODE`-with-basis are exactly
unbounded-judgment operands. Extending P3 to cover them would violate the same law that H3
already applied against P0b — and the record shows this pack has a habit of catching itself on
that law, so it is worth not re-introducing.

`worktree` is the borderline one: `git rev-parse --show-toplevel` / `git worktree list` gives it
a mechanical counterpart, so it *could* join A cheaply. Offered as an option, not assumed —
mirroring how the intake offered the P0b schema change as an option rather than assuming it.

### What a wrong call costs

- **Choosing B:** re-introduces an unbounded-judgment probe leg. The cost is not a failed check
  — it is a leg that cannot honestly FAIL, which degrades every other row's credibility in the
  same block (a block where one row is theatre invites treating all rows as theatre).
- **Choosing A and forgetting the other three fields exist:** low cost, but worth a one-line
  spec note that `write-scope` and `MODE` are **declared-for-audit, not machine-checked** — an
  honest-limits statement rather than a silent gap.

---

## Q4 — What numeric byte budget applies to `protocols/HANDOFF_BOOT.md`?

**GENUINELY OPEN — and it carries a which-file ambiguity the architect should settle first.**

### The ambiguity (settle this before the number)

A10 item 2 (`docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md`, §11) says:

> AND a stated byte budget for `protocols/HANDOFF_BOOT.md` checked by the assembler's existing
> size machinery (**it already measures the file as paste section 1**) — growth past budget
> warns, mirroring the paste budget.

The sol-draft carries this forward at `…sol-draft.md:172-175` as
"`protocols/HANDOFF_BOOT.md` MUST have a stated numeric byte budget."

But these are **two different files** at very different scales (live-measured at `c8490c1d`):

- `protocols/HANDOFF_BOOT.md` — **16,156 bytes** (the resident doctrine/spec file)
- per-bundle `docs/handoffs/<slug>/HANDOFF_BOOT.md` — **4,179–8,801 bytes** across all 64 bundles;
  the 2026-07-31 bundle is **4,675 bytes**

The parenthetical "it already measures the file as paste section 1" points at the **per-bundle**
artifact (that is what the assembler assembles), while the named path is the **protocol** file.
One of the two is wrong, and a number chosen for the wrong one is off by ~3x.

**Recommendation on the ambiguity: the budget governs `protocols/HANDOFF_BOOT.md`, the resident
file, and the named path should win over the parenthetical.** Evidence: A10 item 2's *stated
rationale* is RM-3, the "honest boot" item — the same item that rewrites §4's "~3-line core"
claim into "a compact boot core … plus the resident browser-role doctrine — **resident** because
a CC-held file never transmits to the file-less browser". The thing at risk of unbounded growth,
and the thing whose size the operator pays for on every single boot, is the **resident** file.
That is the growth A10 is arresting. Offered as a reading, not a certainty — the parenthetical
genuinely points the other way, and only the architect can settle which the ruling meant.

### Precedent for the number

The paste budget is the stated model ("mirroring the paste budget"). Live at
`scripts/assemble_paste.py:29-32`:

```
# 06-15..07-03 with no budget). The healthy filled paste is ~59 KB; warn just past that so
_SIZE_WARN_BYTES = 65_000
```

So the established heuristic is: **take the healthy observed ceiling, warn just past it** —
65,000 against a ~59,000 healthy value, a margin of **~10%**.

### Applying the heuristic

**If the budget governs `protocols/HANDOFF_BOOT.md` (recommended reading):**
current size 16,156 bytes. Healthy-ceiling-plus-10% → **18,000 bytes**. A round
`18_000` matches the `_SIZE_WARN_BYTES = 65_000` styling and leaves ~11% headroom for
in-place doctrine edits before a warn fires.

**If instead it governs the per-bundle boot:** observed distribution across 64 bundles is
4,179–8,801 bytes, with the last 30 days clustering **4,388–5,740** and the all-time max
(8,801, `2026-06-19`) a clear outlier from a pre-diet era. Healthy recent ceiling ~5,740 +10% →
**6,500 bytes**.

| Target | Current | Healthy ceiling | Recommended budget |
|---|---|---|---|
| `protocols/HANDOFF_BOOT.md` | 16,156 | 16,156 | **18,000** |
| per-bundle `HANDOFF_BOOT.md` | 4,675 | ~5,740 (recent) | **6,500** |

### Failure posture is already settled — do not upgrade it

`…sol-draft.md:178-179`: "The assembler action is a **warning**; this draft does not turn it
into a blocking gate." The intake agrees ("growth past budget **warns**"). Recommend holding
that: a blocking budget gate on a doctrine file would block canon edits that legitimately grow
it.

### What a wrong call costs

- **Ruling a number without settling the which-file question:** the budget lands on the wrong
  artifact and is either permanently silent (18,000 applied to a 4.7 KB bundle boot — never
  fires, pure dead code) or permanently screaming (6,500 applied to a 16 KB protocol file —
  warns on every run, and a warn that always fires is trained-away within a week). **Both
  failure modes are worse than no budget**, because both look like coverage.
- **Choosing a too-tight number:** nuisance warns; cheap to re-tune, one constant.
- **Choosing a too-loose number:** the item closes with no real teeth. Note A10 "cannot close
  on a placeholder" (`…sol-draft.md:275`) — but it can equally close on a number that never
  binds, which is the same nothing wearing a number.

---

## Q5 — What exact targets and diagnostic does RM-8 govern?

**NOT GENUINELY OPEN as to target — but the sources carry a real refuse-vs-suffix conflict.**

### The definition already exists

`docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md:157`, verbatim:

> **Committed-bundle overwrite refusal:** `gen_handoff.py` refuses to write into a bundle dir
> that contains git-TRACKED files, and auto-suffixes (`-2`) instead — the default slug
> overwrote 4 committed files of a same-day bundle, caught only via `git status` (audit RM-8).
> Lives: `scripts/gen_handoff.py`. Cost: S.

The originating incident is recorded at `docs/audits/2026-07-27-verification-handoff-process-audit.md:41`:
"`gen_handoff.py`'s default slug overwrote 4 committed files of the same-day bundle; caught only
via `git status`, reverted verbatim; recurrence risk is **structural** (same date twice in one
day)" — with the miner cite naming `2026-07-11-dev-knowledge-architect` and the `-2` regeneration.

**Target set, therefore:** the **bundle directory** `gen_handoff.py` is about to write into —
specifically, one that **contains git-TRACKED files**. Not "any existing directory": a freshly
created or untracked-only dir is a legitimate re-run target (the fill→re-assemble workflow
depends on re-writing an uncommitted bundle).

### The unguarded code site (re-verify-at-ruling)

`scripts/gen_handoff.py:434-436`:

```
    slug = slug or f"{date}-{repo.lstrip('.')}-{mode}"
    bundle_root = bundle_root or (repo_root / "docs" / "handoffs")
    bundle_dir = bundle_root / slug
    bundle_dir.mkdir(parents=True, exist_ok=True)
```

`exist_ok=True` at `:436` is the exact structural hole: the default slug at `:434` is
date-derived, so a second same-day bundle recomputes an **identical** path and the generator
proceeds into a committed directory without objection. This corroborates the audit's
"recurrence risk is structural". The 2026-07-29 dossier independently confirms it is unshipped:
`docs/audits/2026-07-29-technical-intake18-ratification-dossier.md:168` — "*Committed-bundle
overwrite refusal (RM-8 guard):* **NOT shipped** — `scripts/gen_handoff.py:436`".

### The genuine conflict — "refuse" and "auto-suffix" are different behaviors

| Source | Prescribed behavior |
|---|---|
| Intake `:157` | "**refuses** … **and auto-suffixes (`-2`) instead**" |
| sol-draft `…sol-draft.md:198` | "Generation MUST **refuse an overwrite rather than replace** an existing target." |

Auto-suffixing is **not** a refusal — it is a silent redirect that *succeeds*. The operator who
typed a slug gets a bundle at a *different* path than the one they named, and (per the RM-8
incident pattern) may not notice. A refusal stops and reports. These produce materially
different operator experiences and cannot both be implemented as written.

### Options space

| Option | Behavior on a tracked-file collision | For | Against |
|---|---|---|---|
| **A. Hard refuse** | non-zero exit + diagnostic naming the collision and suggesting `-2` | honest; operator stays in control; matches sol-draft | one extra round-trip on a legitimate same-day second bundle |
| **B. Auto-suffix silently** | writes to `<slug>-2`, exit 0 | zero friction; matches intake's letter | a *silent* path change; reintroduces a surprise of the same family as the original defect |
| **C. Auto-suffix loudly** | writes to `<slug>-2`, exit 0, prints a prominent `[warn]` naming both paths | no friction AND no silence | still exits 0, so nothing gates on it |
| **D. Refuse by default, `--allow-suffix` opt-in** | A, with B available explicitly | safest default, escape hatch exists | one more flag |

### Recommendation

**Option D — refuse by default, with an explicit opt-in suffix flag.**

Evidence: the sol-draft is the later and more specific source and says *refuse*; and the whole
RM-8 class exists because a write happened that the operator did not intend and did not see.
Option B fixes the data loss but preserves the invisibility, which is the half that made the
original incident "luck-shaped" (the audit's own word — the catch was `git status`, not the
tool). Option D gives the ergonomic path the intake wanted without making silence the default.

**Suggested diagnostic content** (the question asks for it explicitly): the refusal message
should name (i) the bundle dir, (ii) the count and names of git-TRACKED files found there,
(iii) the next free `-N` slug, and (iv) the flag to proceed. That is enough for the operator to
act without running `git status` themselves.

### What a wrong call costs

- **Implementing B (silent auto-suffix):** a generated bundle silently lands at an unexpected
  path. Downstream, `_select_active_bundle` picks by git add date and **FAILs on ambiguous
  multiple-fresh candidates** (`…sol-draft.md:186-188`) — so a silent extra bundle can convert
  into a confusing gate failure at a later, unrelated beat.
- **Implementing nothing:** the structural recurrence stands. Note the guard's own trigger is
  "same date twice in one day", which describes a *normal* busy day in this repo — the 07-11
  and 07-20 records both show same-day multi-bundle days.

---

## Q6 — Types, defaults, CLI mapping, and interaction of `repo_root` and `cross_repo`

**NOT GENUINELY OPEN as to types/defaults/interaction — the live code already fixes them.** Only
the CLI spelling is undetermined.

### Live signatures (re-verify-at-ruling)

`scripts/verify_handoff_probes.py:409`:

```
def verify(bundle_path, repo_root=None, cross_repo=False) -> list[ProbeResult]:
```

with the docstring immediately following (`:412-415`) specifying both the default-resolution
rule and the interaction:

> `repo_root` defaults to the repo containing the bundle (`<repo>/docs/handoffs/<slug>`
> -> `parents[2]`); pass it explicitly to resolve against a different root. `cross_repo` …
> target root as `repo_root` and set `cross_repo=True`

and the fallback implemented at `:419-421`:

```
    if repo_root is None:
        …
        repo_root = parents[2] if len(parents) >= 3 else bundle_path
```

`main` at `:436` is `def main(argv=None) -> int`, and at `:444` it calls **`verify(bundle)`** —
passing neither parameter. That single line is the whole gap: `verify()` has the capability,
`main()` does not expose it. This matches the intake's framing at
`…v6-proposal.md:153`: "`verify_handoff_probes.main()` exposes the `repo_root`/`cross_repo`
params `verify()` **already has** (the 4 false-FAILs on hand-runs of cross-repo bundles)."

### So the answers, derived from live code rather than ruled

- **`repo_root`** — type `Path | None`, default `None`, meaning "infer from bundle path via
  `parents[2]`". (Typed as `Path` in every internal consumer: `_within_repo_file(repo_root: Path, …)`
  at `:215`, `_basename_matches(repo_root: Path, …)` at `:231`, `_resolve_status(repo_root: Path, …)`
  at `:243`.)
- **`cross_repo`** — type `bool`, default `False`. Its effect is visible at `:385-386`: when
  true, a file token is classified via `_resolve_status(repo_root, rel)` rather than the strict
  `_resolve_path` miss at `:394`.
- **Interaction** — documented in the `verify` docstring: for a cross-repo bundle you set
  **both** (target root as `repo_root` **and** `cross_repo=True`). `cross_repo=True` with a
  defaulted `repo_root` is the incoherent combination.

### The genuinely open part — CLI surface

Recommendation, matching the repo's existing `click`-based idiom (`gen_handoff.py:506` uses
`@click.option("--assemble/--no-assemble", default=True, …)`):

- `--repo-root PATH` — `click.Path(exists=True, file_okay=False, path_type=Path)`, default `None`
- `--cross-repo/--no-cross-repo` — default `False`

**Recommended guard on the incoherent combination:** `--cross-repo` passed *without*
`--repo-root` should error rather than silently infer, since the inferred root is by definition
the *wrong* repo in the cross-repo case — that is precisely the shape of the "4 false-FAILs on
hand-runs of cross-repo bundles" the item exists to fix.

Note `main` currently uses hand-rolled `sys.argv` parsing (`:439-443`), not `click`. Whether to
convert it to `click` or extend the manual parser is a small implementation choice; the manual
parser is only ~5 lines and adding two flags to it is not obviously worse than a `click`
conversion. Flagging as an implementation detail, not a ruling.

### What a wrong call costs

- **Very little.** This is the lowest-risk of the seven: the semantics are already fixed by
  working code with tests around `verify()`, and the change is exposure, not design. The one
  real trap is allowing `--cross-repo` alone to silently infer a root — that would reproduce the
  original false-FAIL class through the new surface.

---

## Q7 — What tokenizer behavior and acceptance test constitute the `[#421]` absorption?

**GENUINELY OPEN — and there are TWO distinct tokenizer defects, only one of which the sources name.**

### What the sources name — variant 2

`docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md:153`: "[#421] absorbs the **second
tokenizer variant** (backticked `#id` in a source column parses as an anchor — witnessed 07-26,
unfiled at window close)".

Confirmed in live code. `scripts/verify_handoff_probes.py:131-133`:

```
def header_tokens(text: str) -> list[str]:
    """Backtick spans that are markdown headers (`## …`) — the anchors to resolve."""
    return [s for s in backtick_spans(text) if s.startswith("#")]
```

The predicate is `startswith("#")` with **no further discrimination**. A backticked backlog id
such as `` `#421` `` in a source column therefore satisfies it and is treated as a markdown
header anchor to resolve — which then fails to bind and surfaces as a spurious `anchor-missing`.
The docstring says "markdown headers (`## …`)" but the code accepts a **single** `#`, so the
implementation is wider than its own stated contract.

### What the sources do NOT name — variant 1 (the leading-dot defect)

`scripts/verify_handoff_probes.py:54`:

```
_FILE_RE = re.compile(r"(?:[\w.-]+/)*[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1)")
```

Directory segments are `[\w.-]+` (dots allowed), but the **final** segment is `[\w-]+` — dots
**not** allowed. So for a repo-root dotfile like `.pre-commit-config.yaml`, the regex matches
only the substring `pre-commit-config.yaml`, silently dropping the leading dot; the resulting
token then fails to resolve. A dotfile in a *subdirectory* (`.claude/settings.json`) is
unaffected, because there the dot lives in a directory segment. This asymmetry — **only the
final path segment loses its dot** — makes the failure look arbitrary from the outside.

**This dossier's most actionable Q7 finding:** the `[#421]` row's scope is described in the
sources only as "the second tokenizer variant", which presupposes a first. If the architect
rules only on the backticked-`#id` case, variant 1 stays live and unfiled, and `[#421]` closes
while a witnessed tokenizer defect remains. **Recommend the ruling explicitly states whether
`[#421]`'s absorption covers one variant or both.**

### Options space

| Option | Scope | Comment |
|---|---|---|
| **A. Variant 2 only** | narrow `header_tokens` | matches the intake's literal words; leaves variant 1 unfiled |
| **B. Both variants** | narrow `header_tokens` + widen `_FILE_RE`'s final segment | closes the class; slightly larger diff |
| **C. Variant 2 now, variant 1 filed separately** | narrow now, new row | honest bookkeeping; costs a backlog id |

### Recommendation

**Option B**, or **C** if the architect wants the ledger clean.

Suggested contracts:

- **Variant 2 fix** — `header_tokens` should require an actual heading shape rather than a bare
  `#`. Narrowest sufficient predicate: require `#` followed by whitespace (`# `, `## `, …), which
  admits every real markdown heading and rejects `#421`, `#446`, and every other bare id. Note
  this also brings the function into line with its own docstring.
- **Variant 1 fix** — allow a leading dot on the final segment, e.g. final segment `[\w.-]+`
  with the extension alternation unchanged. Worth a precision check: `_FILE_RE` is documented as
  "precision-over-recall" (`:126-128`), so the widening should be verified not to start matching
  prose like `see audit.py health` in new places.

**Suggested acceptance tests** (the question asks for the acceptance assertion):

- `test_header_tokens_ignores_backticked_backlog_id` — a source cell containing `` `#421` ``
  yields **no** anchor token and produces no `anchor-missing`.
- `test_header_tokens_still_binds_real_heading` — `` `## Vision` `` still resolves (guards
  against over-narrowing).
- `test_file_tokens_binds_repo_root_dotfile` — `` `.pre-commit-config.yaml` `` resolves to the
  real file rather than the dot-stripped miss.
- `test_file_tokens_precision_unchanged` — a prose cell that previously yielded no path tokens
  still yields none after the widening.

The "lands with a test or is re-deferred by ruling" requirement is explicit at
`…sol-draft.md:212` ("Each A11 leg lands with a test or is re-deferred by ruling. No silent
omission completes it.") — so a test name list is part of what closing this needs, not a nicety.

### What a wrong call costs

- **Ruling variant 2 only, without saying so (A, implicitly):** `[#421]` closes with a live
  defect still in the tokenizer and no row owning it. Because the defect surfaces as
  `anchor-missing` — a **warn**, not a fail (`verify_handoff_probes.py:453` counts
  `anchor-missing` among warns) — it degrades quietly. Warns that are known-spurious train
  operators to ignore warns generally, which costs more than the bug.
- **Over-narrowing variant 2:** if the predicate is tightened past real headings, genuine anchor
  probes stop binding and silently pass. That is worse than the spurious warn, because it
  removes teeth instead of noise. Hence the paired "still binds a real heading" test.

---

## Cross-cutting notes for the architect

1. **Pin-scope, not knowledge gaps.** Four of seven questions resolve against
   `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md`, which was absent from the
   sol-draft's `pinned_inputs`. If future producer drafts are pinned this way, consider whether
   the ratified intake pack belongs in the default pin set — an ADR-level observation, not a
   ruling this dossier can make.

2. **Two conflicts to resolve, distinct from the seven questions.** Both were surfaced above and
   neither is listed as an OPEN question anywhere:
   - **Q4's which-file ambiguity** — A10 names `protocols/HANDOFF_BOOT.md` while its own
     parenthetical describes the per-bundle artifact.
   - **Q5's refuse-vs-auto-suffix conflict** — intake `:157` and sol-draft `:198` prescribe
     different behaviors.

3. **Suggested ruling order** (cheapest-unblocking first): **Q6** (confirm code-derived, ~5 min)
   → **Q3** (confirm + one narrow choice) → **Q2** (confirm + the P0a re-point) → **Q5**
   (resolve the conflict) → **Q7** (scope ruling: one variant or two) → **Q4** (settle
   which-file, then the number) → **Q1** (naming, lowest stakes, genuinely free choice).

4. **Nothing here is a decision.** Every recommendation is UNVERIFIED-UNTIL-LOCAL and every
   `file:line` is **re-verify-at-ruling** against branch base `c8490c1d`. Several anchors sit in
   files this arc will itself edit, so they will move.
