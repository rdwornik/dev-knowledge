# LANE `ac-863-notification` — end-of-lane artifact (PARTIAL, PAUSED on a rule-vs-ruling conflict)

**Consumers:** `[#863]` PRIMARY · `[#886]` · `[#888]`

**Lane:** `lane-ac-863-notification` · branch `worktree-lane-ac-863-notification` · contract
`LANE-ac-863-notification.md` · model `sonnet` (ran `claude-sonnet-5`) · effort high · dispatch
`local` · kind `code` · decision budget V-2 · base = dispatching checkout HEAD.

---

## 0 · The verdict, first

**PARTIAL.** Done-contract item 2 (expiry field) is DONE and committed (`dc5729fe`). Done-contract
item 1 (restore Notification with a counter) is **PAUSED**, not done and not silently skipped — a
V-2 class **(b)** rule-vs-ruling conflict, disclosed here rather than decided by this lane. Item 3
(further hooks per family) has nothing to restore: every one of the nine measured-broken hooks
remains over the bar. Item 4 (remove a zero-catch gate) does not apply — no hook was newly wired
with a counter this lane, so there is no window to report against.

| Done-contract item | State |
|---|---|
| 1. Notification hook restored WITH A COUNTER | **PAUSED** — see §1. No commit. |
| 2. `expiry` field beside every individually-disabled hook | **DONE** — `dc5729fe` |
| 3. Further hooks restored only per family, only where measurement clears it | **NONE cleared** — see §2 |
| 4. A gate with no catch in its window is removed, not tuned | **N/A this lane** — see §3 |

## 1 · Why the Notification restore is PAUSED, not done

**The premise.** "The Notification hook" has exactly one instantiation anywhere in this repo's own
history and docs: the **global, L0** hook `~/.claude/claude-notify.ps1`
(`ecosystem/organ-index.md:94`, `ecosystem/organ-registry.yaml:119`, ADR-74, and five
`docs/audits/*` mentions going back to 2026-05-12). It has never existed in this repo's own
`.claude/settings.json`, in any commit, at any point (checked: `git log --all -p -- .claude/settings.json`
has no `"Notification"` hit). It was removed along with everything else by the global emergency
disable: live-read just now, `~/.claude/settings.json` carries `"disableAllHooks": true` and
`"hooks": {}`.

**The conflict.** None of the three linked rows this lane owns (`[#863]`, `[#886]`, `[#888]`) name
Notification or `claude-notify.ps1` anywhere in their body text or Done-when clauses; all three are
scoped to the *repo-local* `.claude/settings.json` and the three parity-required surfaces
(`settings-precommit-arm`, `settings-stop-backpressure`, `settings-deny-and-point`). So "restore the
Notification hook" in this contract's Done-contract item 1 can only mean editing the **global**
`~/.claude/settings.json` — infrastructure this repo does not own and that affects every repo and
every concurrent session on the machine. The standing global rule
(`~/.claude/CLAUDE.md` core-invariants §6, "Global-infra edits are exception-with-ruling — never
unilateral... if a task seems to need a global-infra edit and you lack an explicit ruling for it,
STOP and ask") requires an explicit, edit-scoped operator ruling before Claude Code touches it. This
contract's own text never says "edit `~/.claude/settings.json`", and none of its three linked rows
license that edit either.

**Why this was not escalated by asking.** A `--bg` lane has no answer channel — `AskUserQuestion`
here would return `InputValidationError` and the session would sit producing nothing,
indistinguishable from a working lane, for the whole remaining run. Per this contract's own Q10
("a lane that discovers a refuted premise PAUSEs with the fact... the disclosure discharges the
reporting duty, it does not authorise the deviation"), the correct move is to do neither — not edit
global infra unilaterally, and not invent an unruled repo-local substitute (e.g. a brand-new
project-scoped `Notification` hook that was never asked for) — and instead leave the fact here for
the integrator, who has an answer channel.

**What the integrator owes, one of two:**
1. **Rule the global edit explicitly**, scoped to this restoration (component: `claude-notify.ps1`,
   Notification + Stop events, counter requirement stated), and either perform it directly or
   re-dispatch this lane with that ruling cited in the contract text so a future bg session has the
   authorization on its face.
2. **Amend the contract** (or file a new row) to state plainly that "restore the Notification hook"
   means a *new*, repo-local Notification hook in this repo's own `.claude/settings.json` — a
   different mechanism from `claude-notify.ps1`, not a restoration of it — if that is in fact what
   is wanted. That reading is not precluded by anything read this lane, but it is not supported by
   anything either; guessing between the two was the thing declined here.

Either way, the counter shape itself is not a fork: `scripts/hooks/bounded_hook.py`'s existing
`HOOK-BYPASSES.jsonl` record (hook id, bound, elapsed, session id, event, tool, reason, posture) is
the organ already built for exactly "what it caught, what it cost, over what window" (this
contract's own item-1 wording), so whichever hook gets wired, it should ride that record rather
than invent a second one — flagged for whoever picks this back up, per the no-new-organ rule this
contract's `rows:` section states.

## 2 · Step 1 / item 3 — the measured families, and why none is restored further

Read `disabled_individually` (all nine entries) before editing, per contract step 1. Bar (operator
ruling 2026-09-17 item 2): at or under 10% bypass, full 168h window, >= 20 runs.

| hook | rate | vs. bar |
|---|---|---|
| `surface_triage.ps1` | 96% | over |
| `surface-closures.ps1` | 58% | over |
| `fleet_health.py` | 41% | over |
| `codespace_regime.py session-start` | 33% | over |
| `resource_lifecycle.py session-start` | 25% | over |
| `billing_leak_sentinel.ps1` | 22% | over |
| `conductor.py session-start` | 17% | over |
| `changelog_sentinel.py` | 10.3% | over (by 0.3 pts) |
| `propose_closures.py` | 15% | over, and KNOWN-UNGOVERNABLE regardless (no per-repo lever exists) |

**All nine remain over the bar.** No family clears measurement, so none is restored tonight. This is
stated rather than left implicit, per the contract's own instruction that a family left alone must
be named and reasoned, not just omitted.

## 3 · The `expiry` field (item 2, DONE)

Added `"expiry": "2026-09-24"` (ISO-8601, matching the `.methodology.yaml` `sanctioned_divergences`
convention) to eight of the nine `disabled_individually` entries — the field on the existing record,
not a new record type, per `[#886]`'s ownership of the record shape. The date is not a guess: it is
the 168h/7-day measurement window already named in every entry's own `reenable_when` text, dated
from the 2026-09-17 disable, so it is derived from data already in the file.

`propose_closures.py` is excluded from the numeric expiry. Its own `owner` field already states
`KNOWN-UNGOVERNABLE, operator ruling 2026-09-17 -- LEFT RUNNING deliberately`, and its `state` field
already reads `RUNNING (not disabled)` — it is not the same class of thing as its eight siblings (a
temporary, re-measurable disable). Giving it a calendar expiry would misrepresent a standing
architectural limitation as pending debt with a review date. It carries a prose `"expiry": "n/a --
..."` field instead, stating the exclusion in place rather than leaving a silent gap a future reader
could mistake for an oversight.

This does **not** close `[#886]` or `[#888]` — both still need the gate-read DATA record (a verdict
engine that renders these as a distinct DEBT/DEGRADED state) that this lane's contract does not
build. It only fields the existing register per `[#886]`'s scope: "this row owns the record shape,
so this lane adds a FIELD to it and does not invent a rival record."

## 4 · Verification

`uv run --locked pytest tests/ -k "settings or hook"` — targeted per this lane's footprint
(`.claude/settings.json` only touched).

- First pass (`-x`): 2 failed, 90 passed. Both failures (`test_archive_row_body.py::…archive_row_body_and_not_merely_names_it`,
  `test_conductor.py::test_the_session_start_hook_is_wired_in_settings_json`) reproduce byte-identically
  on the pre-edit tree (`git stash push -u` / verified / `git stash apply <sha>` / `git stash drop
  <resolved index>` — never a bare `stash pop`, since the stash stack is shared with concurrent
  lanes). Neither concerns anything this lane touched.
- Full pass (no `-x`): 27 failed, 212 passed. The larger cluster
  (`test_prompts_guard_hook_wiring.py` × 16, `test_graph_spine_commit_tier.py` × 3, plus the original
  2) all inspect the live `hooks` object or `.pre-commit-config.yaml` — neither of which this lane's
  diff touches; the diff is confined to the `//`-prefixed `disabled_individually` **comment** array,
  which Claude Code does not parse as hook wiring. A baseline re-run on the stashed tree was killed
  by the harness's OOM guard mid-run (concurrent lanes on the box) before completing, but its partial
  output already showed the same failure clustering at the same relative test positions, consistent
  with pre-existing causes rather than this edit. Per the harness's own guidance the background OOM
  kill was not re-attempted.
- `uv run --locked ruff check` (repo-wide): clean.
- `git status`: clean after `dc5729fe`.

## 5 · What the integrator owes

1. Rule on §1 (global edit vs. repo-local reinterpretation) and either perform the global edit
   directly or re-dispatch with the ruling cited.
2. `[#886]` / `[#888]` still need their gate-read record and DEGRADED verdict — untouched by this
   lane by design (record-shape ownership, not this contract's scope).
3. No JOURNAL entry, no index regeneration — both reserved to the integrator per this contract's
   "What NOT to do".
