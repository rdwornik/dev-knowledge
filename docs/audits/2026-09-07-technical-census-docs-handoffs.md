<!-- scope: meta -->

# Census — `docs/handoffs/` (SWEEP 2026-09-07, lane S-05)

**Class:** technical · **Mode:** READ-ONLY census · **Lane:** S-05 of 13, batch SWEEP 2026-09-07
**Consumer:** `[#520]` (no sanctioned way to retire a committed bundle) · `[#310]` (COLD-bundle
annotation surface) · `ADR-101` (tree seal / home grammar) · `intake #73` (shape-spec home grammar).
The substantive citations are by path, in each row's Witness column and in §Proposals.

**Nothing in this tree was moved, deleted, edited or renamed by this lane.** Every verdict below is a
PROPOSAL the operator rules. Two defects found are REPORTED, not repaired (§Proposals · REPORTED).

---

## Scope and method

**Subject:** `docs/handoffs/` — 119 date-named bundle directories, one `archive/` subtree
(15 sub-directories + `legacy/`), and one living file, `README.md`.

Measured on `claude/census-docs-handoffs` at merge-base with `origin/main` `5f27b20`:

```
find docs/handoffs -type f | wc -l          -> 762
du -sb docs/handoffs                        -> 10,976,132 B (10.5 MiB)
ls -d docs/handoffs/2026-*/ | wc -l         -> 119
ls -d docs/handoffs/archive/*/ | wc -l      -> 15  (+ legacy/, 43 files, 649,960 B)
```

**Predecessors, read before measuring, and NOT re-litigated:**
`docs/audits/2026-08-26-technical-handoff-census.md` (the browser-seat census; its §0 corpus block
is the baseline this one extends — 115 bundles / 737 files / 10,580,882 B then) and
`docs/audits/2026-08-31-census-single-file-folders.md` (which already dispositioned two of the
anomalies below as `keep-with-reason`). Where they ruled, this census cites rather than re-verdicts.

**Era classification** is by file roster on disk, not by a claim in a file:
`03_PLAYBOOK.md` present -> **v3.2** (twelve-file flat folder, `README.md:237`);
`README.md` present and no `HANDOFF_BOOT.md` -> **v4.x**; both present -> **v4/v5-trans**;
`HANDOFF_BOOT.md` and no per-bundle `README.md` -> **v5/v6/v7** (`README.md:30-35` — "There is no
per-bundle README; this is it"); neither -> **other**.

```
v5/v6/v7  78   v3.2  15   v4.x  13   v4/v5-trans  7   other  6
```

---

## Question 1 — bundle size trend against the ≤20 KB target

**The target, resolved to its locator before use:** `protocols/HANDOFF_PROCESS.md:1325` — *"An
assembled `/boot-session` paste from a real cut is measured for size (**<=20 KB**)"* — restated at
`:1524` as v7's Done-when: *"an assembled paste **<=20 KB at >=70% window-specific measured on a real
cut**"*. The budget binds **the assembled paste**, i.e. `PASTE_THIS.md`, which `README.md:38-40`
names as the one file the operator pastes. It does **not** bind the bundle directory total. Both are
reported below; only the first is a target.

**`PASTE_THIS.md`, all 74 bundles that carry one:**

```
n=74   min 27,096 B   mean 49,731 B   max 86,734 B
over the 20,480 B target: 74 of 74  (100%)
by month, mean / max:
  2026-06  n=10   50,441 / 64,400
  2026-07  n=44   49,130 / 86,734
  2026-08  n=18   52,994 / 80,676
  2026-09  n= 2   30,046 / 32,264
```

**Finding.** The target has never once been met. The trend is flat-to-rising through August
(50.4 -> 49.1 -> 53.0 KB mean) and then breaks downward at the v7 cut: the two September bundles
average 30.0 KB, a **43% drop** against the August mean. That drop is the v6.3.0 role-PIN change
landing — `docs/audits/2026-08-26-technical-handoff-census.md:130` predicted it and sized it
("Saving ~16 KB/seat"), and the measured delta (23.0 KB) exceeds the prediction. **It is still 1.5×
the target.** `2026-09-06-dev-knowledge-architect` is 27,829 B and `2026-09-01-dev-knowledge-architect-v7`
is 32,264 B; neither passes.

**The bundle directory total moves the other way** and is worth separating, because it is the number
that looks like growth and is not the governed one:

```
mean bundle bytes by month:  2026-05 143,563 | 2026-06 52,099 | 2026-07 79,723
                             2026-08  94,644 | 2026-09 110,786
```

The May figure is the v3.2 twelve-file folder (each carrying a ~110-140 KB `03_PLAYBOOK.md` snapshot
— the 14 largest files in the whole tree are these). The rise from June to September is real but is
**not** a paste-budget regression: it is `SUPPLEMENT.md` and `PROBES.md` growth in files that are
never pasted. Conflating the two would report the v7 win as a loss.

**A third budget, and it is 13 bytes from its ceiling.** `HANDOFF_PROCESS.md:1327` — *"`protocols/
HANDOFF_BOOT.md` stays inside its own 18,000-byte budget"*. That binds the **repo-resident role file**,
not the bundle-local file of the same name (`README.md:54-58` warns about exactly this same-name
collision). Measured: `protocols/HANDOFF_BOOT.md` = **17,987 B against an 18,000 B ceiling — 13 bytes
of headroom**. The next edit to that file plausibly breaches it. Reported here because this lane
measured it; the file is not in this lane's write scope and was not touched.

Bundle-local `HANDOFF_BOOT.md` (n=85) is governed by no byte budget this census could find; for the
record its max is 12,395 B (`2026-09-06-dev-knowledge-architect`) and its per-month range trends
upward without being monotone (June 1,329-8,717 B, July 4,131-7,275 B, August 5,943-12,191 B,
September 11,252-12,395 B — June's max exceeds July's, so this is a trend, not a ratchet).

---

## Question 2 — bundles older than the last two windows

**"Window", resolved:** `scripts/gen_handoff.py:786` defines it as *"the diff since
`docs/handoffs/<prev>/` was added"*. A window is therefore one bundle-to-bundle interval, and the
literal reading of "older than the last two windows" is **every bundle except the newest two** —
117 of 119. This census does **not** propose that, and says why rather than quietly narrowing it.

**The blocker is named, not inferred.** `[#520]` (`tasks/520-…md`, status `open`, P2) records the
direction already ruled: *"`docs/handoffs/` is immutable, so this is a rule gap in an artifact that
cannot be edited; direction ruled — retire via an external dated marker, bundle left byte-unchanged"*,
Done-when *"the marker surface is defined"*. **The marker surface does not exist yet.** So a blanket
relocation of 117 directories is not a proposal this census can make; what it can do is separate the
population the operator can rule on today from the one that waits on `[#520]`.

**Relocation is admissible by the tree seal** — `ecosystem/fleet-shape-spec.yaml:258-259` opens
`docs/handoffs` and `docs/handoffs/**` as homes, so `docs/handoffs/archive/<slug>/` is an already-open
home and an ARCHIVE move would not trip `validate_hermetization` Rule C. That is a statement about the
seal only; it is not a retirement mechanism.

**The retention home already exists and already has a stated rule:** `README.md:222-223` — *"older
eras are archived, not deleted"* — and `README.md:237-238` declares v3.2 *"Historical"* and pre-v3.2
*"under `archive/legacy/`"*. That sentence is the witness for the 31-bundle ARCHIVE group below: the
runbook says the pre-v5 eras belong in `archive/`, and 31 of them are still at the genre root.

---
## Inventory

One row per top-level entry of `docs/handoffs/`. **Live** = files under `scripts/ tests/ tasks/
ecosystem/ protocols/ .claude/ templates/ deploy/` citing the slug — the witness class that survives
`scripts/consumer_at_landing.py:31-34`, which rules that `JOURNAL.md` and `docs/handoffs/**` are
*"a record that the file existed, not evidence that anything consumes it"*. **Rec** = citing files in
the whole tree outside `docs/handoffs/` (dominated by `JOURNAL.md`, which alone cites 114 of 119
slugs); it is provenance, not consumption, and it is shown so nobody reads a `0` in **Live** as
"nothing ever referenced this". `Paste` is `PASTE_THIS.md` in KiB; `—` means the bundle carries none.

`ARCHIVE†` = ARCHIVE **candidate blocked on `[#520]`** — the marker/retirement surface it needs does
not exist yet. See §Proposals.

| Bundle | Era | Files | KiB | Paste | Live | Rec | Verdict |
|---|---|---|---|---|---|---|---|
| `2026-05-09-ai-council-audit-sync` | v3.2 | 12 | 162 | — | 2 | 9 | KEEP |
| `2026-05-09-dev-knowledge-session-sync` | v3.2 | 12 | 173 | — | 0 | 4 | ARCHIVE |
| `2026-05-12-ai-council-session-sync` | v3.2 | 12 | 157 | — | 0 | 3 | ARCHIVE |
| `2026-05-12-dev-knowledge-session-sync` | v3.2 | 12 | 164 | — | 0 | 1 | ARCHIVE |
| `2026-05-14-ai-council-session-sync` | v3.2 | 13 | 174 | — | 0 | 2 | ARCHIVE |
| `2026-05-14-dev-knowledge-session-sync` | v3.2 | 12 | 195 | — | 1 | 2 | KEEP |
| `2026-05-15-ai-council-cleanup` | v3.2 | 13 | 62 | — | 0 | 1 | ARCHIVE |
| `2026-05-15-dev-knowledge-session-sync` | v3.2 | 12 | 186 | — | 0 | 0 | ARCHIVE |
| `2026-05-17-ai-council-session-sync` | v3.2 | 13 | 186 | — | 0 | 2 | ARCHIVE |
| `2026-05-17-dev-knowledge-session-sync` | v3.2 | 12 | 195 | — | 0 | 1 | ARCHIVE |
| `2026-05-18-ai-council-session-sync` | v3.2 | 12 | 179 | — | 0 | 1 | ARCHIVE |
| `2026-05-18-dev-knowledge-session-sync` | v3.2 | 12 | 197 | — | 0 | 1 | ARCHIVE |
| `2026-05-19-dev-knowledge-session-sync` | v3.2 | 12 | 201 | — | 0 | 2 | ARCHIVE |
| `2026-05-25-corp-monorepo-session-sync` | v3.2 | 13 | 228 | — | 0 | 3 | ARCHIVE |
| `2026-05-25-dev-knowledge-session-sync` | v3.2 | 12 | 221 | — | 0 | 3 | ARCHIVE |
| `2026-05-29-dev-knowledge-session` | v4.x | 8 | 27 | — | 1 | 4 | KEEP |
| `2026-05-29-dev-knowledge-session-v4.2-rerun` | v4.x | 8 | 24 | — | 0 | 2 | ARCHIVE |
| `2026-05-30-dev-knowledge-session` | v4.x | 8 | 30 | — | 0 | 2 | ARCHIVE |
| `2026-05-31-dev-knowledge-session` | v4.x | 8 | 14 | — | 0 | 1 | ARCHIVE |
| `2026-05-31-dev-knowledge-session-2` | v4.x | 8 | 30 | — | 0 | 1 | ARCHIVE |
| `2026-06-03-dev-knowledge-session` | v4.x | 8 | 36 | — | 1 | 2 | KEEP |
| `2026-06-05-dev-knowledge-session` | v4.x | 8 | 35 | — | 0 | 3 | ARCHIVE |
| `2026-06-05-dev-knowledge-session-2` | v4.x | 8 | 32 | — | 0 | 1 | ARCHIVE |
| `2026-06-05-dev-knowledge-v44-wrap` | v4.x | 8 | 31 | — | 0 | 2 | ARCHIVE |
| `2026-06-06-dev-knowledge-session` | v4.x | 8 | 37 | — | 0 | 1 | ARCHIVE |
| `2026-06-09-dev-knowledge-session` | v4.x | 8 | 36 | — | 0 | 2 | ARCHIVE |
| `2026-06-10-dev-knowledge-session` | v4.x | 8 | 35 | — | 0 | 2 | ARCHIVE |
| `2026-06-10-dev-knowledge-session-2` | v4.x | 8 | 31 | — | 0 | 1 | ARCHIVE |
| `2026-06-11-dev-knowledge-session` | v4/v5-trans | 4 | 15 | — | 0 | 1 | ARCHIVE |
| `2026-06-11-dev-knowledge-session-2` | v4/v5-trans | 4 | 24 | — | 0 | 1 | ARCHIVE |
| `2026-06-11-dev-knowledge-session-3` | v4/v5-trans | 4 | 27 | — | 0 | 1 | ARCHIVE |
| `2026-06-11-dev-knowledge-session-4` | v4/v5-trans | 4 | 17 | — | 0 | 1 | ARCHIVE |
| `2026-06-12-dev-knowledge-architect` | v5/v6/v7 | 3 | 22 | — | 0 | 1 | ARCHIVE† |
| `2026-06-12-dev-knowledge-session` | v4/v5-trans | 4 | 29 | — | 0 | 3 | ARCHIVE |
| `2026-06-12-dev-knowledge-session-2` | v4/v5-trans | 4 | 34 | — | 0 | 1 | ARCHIVE |
| `2026-06-12-dev-knowledge-session-3` | v4/v5-trans | 4 | 26 | — | 0 | 3 | ARCHIVE |
| `2026-06-13-dev-knowledge-architect` | v5/v6/v7 | 3 | 26 | — | 1 | 3 | KEEP |
| `2026-06-15-dev-knowledge-architect` | v5/v6/v7 | 5 | 68 | 36 | 0 | 1 | ARCHIVE† |
| `2026-06-15-dev-knowledge-session` | v5/v6/v7 | 3 | 21 | — | 0 | 1 | ARCHIVE† |
| `2026-06-16-dev-knowledge-architect` | v5/v6/v7 | 5 | 74 | 38 | 0 | 1 | ARCHIVE† |
| `2026-06-17-dev-knowledge-architect` | v5/v6/v7 | 5 | 102 | 51 | 1 | 4 | KEEP |
| `2026-06-17-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 104 | 52 | 1 | 4 | KEEP |
| `2026-06-18-dev-knowledge-architect` | v5/v6/v7 | 5 | 106 | 54 | 0 | 2 | ARCHIVE† |
| `2026-06-19-dev-knowledge-architect` | v5/v6/v7 | 5 | 101 | 51 | 0 | 1 | ARCHIVE† |
| `2026-06-20-dev-knowledge-architect` | v5/v6/v7 | 5 | 91 | 47 | 1 | 2 | KEEP |
| `2026-06-21-dev-knowledge-architect` | v5/v6/v7 | 5 | 77 | 40 | 0 | 3 | ARCHIVE† |
| `2026-06-25-dev-knowledge-architect` | v5/v6/v7 | 5 | 115 | 63 | 0 | 2 | ARCHIVE† |
| `2026-06-25-dev-knowledge-session-close` | v5/v6/v7 | 2 | 11 | — | 0 | 2 | ARCHIVE† |
| `2026-06-27-dev-knowledge-architect` | v5/v6/v7 | 5 | 112 | 61 | 0 | 1 | ARCHIVE† |
| `2026-07-01-dev-knowledge-architect` | v5/v6/v7 | 5 | 94 | 52 | 0 | 1 | ARCHIVE† |
| `2026-07-02-ai-council-architect` | v5/v6/v7 | 5 | 94 | 52 | 4 | 12 | KEEP |
| `2026-07-02-dev-knowledge-architect` | v5/v6/v7 | 5 | 99 | 54 | 3 | 4 | KEEP |
| `2026-07-02-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 102 | 56 | 2 | 3 | KEEP |
| `2026-07-03-dev-knowledge-architect` | v5/v6/v7 | 5 | 104 | 58 | 0 | 4 | ARCHIVE† |
| `2026-07-04-dev-knowledge-architect` | v5/v6/v7 | 5 | 106 | 58 | 2 | 3 | KEEP |
| `2026-07-04-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 115 | 62 | 2 | 3 | KEEP |
| `2026-07-05-dev-knowledge-architect` | v5/v6/v7 | 5 | 48 | 30 | 1 | 3 | KEEP |
| `2026-07-05-dev-knowledge-epic-doc-consolidation` | other | 3 | 21 | — | 0 | 1 | ARCHIVE† |
| `2026-07-05-dev-knowledge-epic-llm-first-docs` | other | 3 | 24 | — | 0 | 1 | ARCHIVE† |
| `2026-07-05-dev-knowledge-epic-test-tiering` | other | 3 | 15 | — | 0 | 1 | ARCHIVE† |
| `2026-07-06-dev-knowledge-architect` | v5/v6/v7 | 5 | 81 | 47 | 0 | 1 | ARCHIVE† |
| `2026-07-07-dev-knowledge-architect` | v5/v6/v7 | 5 | 66 | 39 | 0 | 2 | ARCHIVE† |
| `2026-07-07-dev-knowledge-functional` | other | 1 | 5 | — | 1 | 8 | KEEP |
| `2026-07-08-dev-knowledge-architect` | v5/v6/v7 | 5 | 74 | 43 | 0 | 1 | ARCHIVE† |
| `2026-07-09-dev-knowledge-architect` | v5/v6/v7 | 5 | 62 | 37 | 0 | 3 | ARCHIVE† |
| `2026-07-10-dev-knowledge-architect` | v5/v6/v7 | 6 | 82 | 47 | 0 | 1 | ARCHIVE† |
| `2026-07-11-dev-knowledge-architect` | v5/v6/v7 | 5 | 74 | 43 | 0 | 4 | ARCHIVE† |
| `2026-07-11-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 69 | 40 | 0 | 1 | ARCHIVE† |
| `2026-07-11-dev-knowledge-architect-phase-a0` | v5/v6/v7 | 5 | 67 | 39 | 0 | 2 | ARCHIVE† |
| `2026-07-13-ai-council-architect-product-resume` | v5/v6/v7 | 5 | 43 | 27 | 0 | 1 | ARCHIVE† |
| `2026-07-13-corp-monorepo-architect-product-resume` | v5/v6/v7 | 5 | 43 | 27 | 0 | 1 | ARCHIVE† |
| `2026-07-13-dev-knowledge-architect-a0-closed` | v5/v6/v7 | 5 | 64 | 38 | 0 | 1 | ARCHIVE† |
| `2026-07-17-ai-council-architect-p4-build` | v5/v6/v7 | 5 | 64 | 37 | 0 | 1 | ARCHIVE† |
| `2026-07-17-ai-council-architect-p6-window-completion` | v5/v6/v7 | 5 | 67 | 39 | 0 | 2 | ARCHIVE† |
| `2026-07-17-corp-monorepo-executor-product-execution` | v5/v6/v7 | 6 | 63 | 34 | 0 | 2 | ARCHIVE† |
| `2026-07-17-dev-knowledge-architect` | v5/v6/v7 | 5 | 79 | 45 | 0 | 1 | ARCHIVE† |
| `2026-07-18-corp-monorepo-architect` | v5/v6/v7 | 5 | 62 | 37 | 0 | 2 | ARCHIVE† |
| `2026-07-18-corp-monorepo-e5-registry-developer` | other | 3 | 12 | — | 0 | 2 | ARCHIVE† |
| `2026-07-18-dev-knowledge-architect` | v5/v6/v7 | 6 | 86 | 45 | 1 | 5 | KEEP |
| `2026-07-19-ai-council-architect` | v5/v6/v7 | 5 | 91 | 51 | 0 | 2 | ARCHIVE† |
| `2026-07-19-corp-monorepo-architect` | v5/v6/v7 | 5 | 103 | 57 | 0 | 1 | ARCHIVE† |
| `2026-07-20-ai-council-architect` | v5/v6/v7 | 5 | 97 | 54 | 0 | 2 | ARCHIVE† |
| `2026-07-20-dev-knowledge-architect` | v5/v6/v7 | 5 | 76 | 44 | 3 | 10 | KEEP |
| `2026-07-20-dev-knowledge-architect-arc5` | v5/v6/v7 | 5 | 72 | 42 | 2 | 5 | KEEP |
| `2026-07-21-ai-council-architect` | v5/v6/v7 | 5 | 142 | 77 | 0 | 1 | ARCHIVE† |
| `2026-07-21-dev-knowledge-architect` | v5/v6/v7 | 5 | 95 | 53 | 0 | 3 | ARCHIVE† |
| `2026-07-23-ai-council-architect` | v5/v6/v7 | 5 | 137 | 74 | 0 | 3 | ARCHIVE† |
| `2026-07-23-dev-knowledge-architect` | v5/v6/v7 | 5 | 78 | 45 | 0 | 5 | ARCHIVE† |
| `2026-07-23-dev-knowledge-execution` | v5/v6/v7 | 4 | 55 | 34 | 1 | 2 | KEEP |
| `2026-07-25-ai-council-architect` | v5/v6/v7 | 5 | 140 | 76 | 1 | 2 | KEEP |
| `2026-07-25-dev-knowledge-architect` | v5/v6/v7 | 5 | 82 | 47 | 0 | 1 | ARCHIVE† |
| `2026-07-26-ai-council-architect` | v5/v6/v7 | 5 | 158 | 85 | 0 | 1 | ARCHIVE† |
| `2026-07-26-dev-knowledge-architect` | v5/v6/v7 | 5 | 110 | 61 | 0 | 5 | ARCHIVE† |
| `2026-07-27-dev-knowledge-architect` | v5/v6/v7 | 5 | 74 | 43 | 0 | 2 | ARCHIVE† |
| `2026-07-28-dev-knowledge-architect` | v5/v6/v7 | 5 | 79 | 45 | 0 | 1 | ARCHIVE† |
| `2026-07-29-dev-knowledge-architect` | v5/v6/v7 | 5 | 78 | 45 | 0 | 2 | ARCHIVE† |
| `2026-07-31-dev-knowledge-architect` | v5/v6/v7 | 5 | 73 | 42 | 1 | 8 | KEEP |
| `2026-07-31-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 85 | 49 | 1 | 6 | KEEP |
| `2026-08-01-dev-knowledge-architect` | v5/v6/v7 | 5 | 89 | 51 | 3 | 13 | KEEP |
| `2026-08-01-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 78 | 45 | 3 | 11 | KEEP |
| `2026-08-04-dev-knowledge-architect` | v5/v6/v7 | 5 | 83 | 48 | 1 | 4 | KEEP |
| `2026-08-05-dev-knowledge-architect` | v5/v6/v7 | 5 | 90 | 51 | 1 | 4 | KEEP |
| `2026-08-06-dev-knowledge-architect` | v5/v6/v7 | 5 | 88 | 50 | 1 | 7 | KEEP |
| `2026-08-08-dev-knowledge-architect` | v5/v6/v7 | 5 | 89 | 50 | 0 | 2 | ARCHIVE† |
| `2026-08-10-dev-knowledge-architect` | v5/v6/v7 | 5 | 126 | 67 | 0 | 4 | ARCHIVE† |
| `2026-08-10-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 149 | 79 | 0 | 3 | ARCHIVE† |
| `2026-08-12-dev-knowledge-architect` | v5/v6/v7 | 5 | 102 | 54 | 1 | 4 | KEEP |
| `2026-08-14-dev-knowledge-architect` | v5/v6/v7 | 5 | 95 | 52 | 0 | 5 | ARCHIVE† |
| `2026-08-17-dev-knowledge-architect` | other | 1 | 21 | — | 0 | 2 | ARCHIVE† |
| `2026-08-17-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 90 | 49 | 0 | 1 | ARCHIVE† |
| `2026-08-17-dev-knowledge-architect-3` | v5/v6/v7 | 5 | 91 | 50 | 0 | 1 | ARCHIVE† |
| `2026-08-20-dev-knowledge-architect` | v5/v6/v7 | 5 | 103 | 56 | 1 | 5 | KEEP |
| `2026-08-20-dev-knowledge-architect-2` | v5/v6/v7 | 5 | 119 | 64 | 0 | 3 | ARCHIVE† |
| `2026-08-23-dev-knowledge-architect` | v5/v6/v7 | 5 | 86 | 43 | 1 | 9 | KEEP |
| `2026-08-25-dev-knowledge-architect` | v5/v6/v7 | 5 | 91 | 50 | 1 | 8 | KEEP |
| `2026-08-28-dev-knowledge-architect` | v5/v6/v7 | 5 | 103 | 47 | 0 | 7 | ARCHIVE† |
| `2026-08-31-dev-knowledge-architect` | v5/v6/v7 | 6 | 66 | 26 | 0 | 4 | ARCHIVE† |
| `2026-09-01-dev-knowledge-architect-v7` | v5/v6/v7 | 6 | 74 | 32 | 2 | 8 | KEEP |
| `2026-09-06-dev-knowledge-architect` | v5/v6/v7 | 8 | 143 | 27 | 1 | 3 | KEEP |
| `README.md` *(file, not a bundle)* | living | 1 | 17 | — | 32 | 99 | KEEP |
| `archive/` *(15 dirs + `legacy/`)* | pre-v3.2 | 43 | 635 | — | 5 | 21 | KEEP |

---

## Proposals

Grouped by verdict. Every row carries a witness; a group with no witness would be `UNDETERMINED`
and is marked as such.

### KEEP — 35 entries (33 bundles + `README.md` + `archive/`)

**Witness class:** a file outside `docs/handoffs/` and outside the record surfaces cites the slug.
Enumerate with

```
for d in docs/handoffs/*/; do n=$(basename "$d"); grep -rIl --exclude-dir=.git \
  --exclude-dir=handoffs -F "$n" scripts/ tests/ tasks/ ecosystem/ protocols/ \
  .claude/ templates/ deploy/ 2>/dev/null | head -1 | sed "s|^|$n :: |"; done
```

The load-bearing ones, named rather than counted:

| Bundle | Witness (re-opened by this lane) |
|---|---|
| `2026-09-06-dev-knowledge-architect` | the **ACTIVE** bundle — the only one with its own add-commit in this clone (`0bfe074`, 2026-09-06); also `tests/test_verify_handoff_probes.py` |
| `2026-09-01-dev-knowledge-architect-v7` | previous window; `tests/test_verify_handoff_probes.py`, `protocols/STANDING_RULINGS.md` |
| `2026-08-25-dev-knowledge-architect` | `protocols/HANDOFF_PROCESS.md` cites it in the spec body |
| `2026-08-23-dev-knowledge-architect` | `tests/test_supplement_folded.py` |
| `2026-08-20-dev-knowledge-architect` *(+ `-2`)* | `scripts/nopack_sandbox.py:205` — glob `docs/handoffs/2026-08-20-dev-knowledge-architect*/*`, which covers the `-2` sibling too |
| `2026-08-12-dev-knowledge-architect` | `tests/test_validate_hermetization.py` |
| `2026-07-20-dev-knowledge-architect` | `scripts/gen_intake_index.py:43`, `scripts/audit.py`, `tasks/manifest.json` |
| `2026-07-20-dev-knowledge-architect-arc5` | `scripts/audit.py`, `tasks/manifest.json` |
| `2026-07-02-ai-council-architect` | `scripts/validate_doc_rot.py` + its test + `ecosystem/disposition-register.yaml` |
| `2026-07-02-dev-knowledge-architect` *(+ `-2`)* | `scripts/gen_handoff.py` + `tests/test_gen_handoff.py` |
| `2026-07-04-dev-knowledge-architect` *(+ `-2`)* | `tests/fixtures/lived-workflow/arc-green.jsonl`, `arc-silent.jsonl` |
| `2026-07-07-dev-knowledge-functional` | `scripts/gen_handoff.py:1172,1243-1248` — *"emits ONE file, FUNCTIONAL_BOOT.md … the single FUNCTIONAL_BOOT.md file IS the bundle"*; `scripts/validate_residual_completeness.py:63` puts it in `BUNDLE_FILES`. Already `keep-with-reason` at `docs/audits/2026-08-31-census-single-file-folders.md:257-273`; **not re-verdicted here** |
| `2026-08-17-dev-knowledge-architect` | `scripts/audit.py:2724` — `supplement_folded` opens `bundle / "SUPPLEMENT.md"` for every bundle, so this one is a live input. Already `keep-with-reason` at the same predecessor, `:277-296`; **not re-verdicted here** |
| `2026-08-01-dev-knowledge-architect` *(+ `-2`)* | `tasks/520-…md`, `tasks/473-…md`, `protocols/STANDING_RULINGS.md` — see REPORTED #1 |
| `README.md` | generated/refreshed by `scripts/seed_runbook.py:73,104-106`; gated by `scripts/canonical_freshness_gate.py:52`; 32 live citers |
| `archive/` | `docs/audits/2026-08-26-technical-handoff-census.md:42` established by `diff -rq` that these hold the Council `stage1-question.md` / `stage2-response.md` pairs and are **not** duplicates of the same-named top-level bundles. Re-confirmed here by roster: 2 files each vs 12-13 at the root. Live citers: `tests/test_validate_hermetization.py`, `tests/test_toc.py`, `tasks/420-…md`, `protocols/archive/HANDOFF_PROCESS_v3.4.md`, `templates/archive/HANDOFF_FOLDER_TEMPLATE.md` |

### ARCHIVE — 31 bundles, pre-v5 eras, no live citer

**-> retention home `docs/handoffs/archive/<slug>/`.**

**Witness:** `docs/handoffs/README.md:221-223` — *"Current bundles are **v7**; **v6** is the
immediately prior era … older eras are archived, not deleted"* — with `:237` declaring v3.2
*"Historical"* and `:238` placing pre-v3.2 *"under `archive/legacy/`"*. The runbook states the rule;
these 31 directories are the population that has not been moved under it. Second witness: each has
**0** live citers by the command above.

```
v3.2         13   of 15 (2 have live citers -> KEEP)
v4.x         11   of 13 (2 have live citers -> KEEP)
v4/v5-trans   7   of  7
             --
             31   2,898,358 B (26.4% of the genre's 10,976,132 B)
```

The v3.2 rows are where the size lives: 14 of the 15 carry a 110,877-141,973 B `03_PLAYBOOK.md`
snapshot, and **those 14 files are the 14 largest files in `docs/handoffs/`** — verify with
`find docs/handoffs -type f -printf '%s %p\n' | sort -rn | head -15`, whose 15th entry is the first
non-v3.2 file. (The 15th v3.2 bundle, `2026-05-15-ai-council-cleanup`, carries a 3,610 B stub
instead; 12 of the 14 heavy ones are in this ARCHIVE group, 2 are KEEP.) Archiving this group is the
single largest byte move available and it is the one the runbook already authorises.

**Note on `archive/` name shadowing, before anyone executes this.** 12 of the 13 proposed v3.2
slugs **already exist as directory names under `docs/handoffs/archive/`** holding different content
(the Council Q/A pairs — `ls docs/handoffs/archive/`). A move to `docs/handoffs/archive/<same-slug>/` would merge two unrelated artifact
sets into one directory. Whatever `[#520]`'s marker surface turns out to be, this group needs a
distinct destination — `archive/v3.2/<slug>/` or equivalent. **This lane proposes the verdict, not
the path.**

### ARCHIVE† — 55 bundles, v5/v6 era, BLOCKED on `[#520]`

**-> would go to a retention home; cannot today.**

**Witness for the candidacy:** `scripts/gen_handoff.py:786` defines a window as *"the diff since
`docs/handoffs/<prev>/` was added"*, so every one of these is older than the last two windows; and
each has **0** live citers.

**Witness for the block:** `tasks/520-no-sanctioned-way-to-retire-a-committed-bundle-w.md`, status
`open` — *"`docs/handoffs/` is immutable … direction ruled — retire via an external dated marker,
bundle left byte-unchanged"*, Done-when *"the marker surface is defined"*. It is not defined. A
census cannot invent it, and relocating an immutable bundle without it would be exactly the
unsanctioned act that row exists to prevent.

```
v5/v6/v7     50   of 78 (28 have live citers -> KEEP)
other         5   of  6 (1 has a live citer -> KEEP)
             --
             55   4,414,417 B (40.2% of the genre's 10,976,132 B)
```

**Recommendation to the operator:** rule `[#520]`'s marker surface first; this group is its largest
justification and is currently 40% of the genre by bytes. Ruling it also unblocks REPORTED #1 below,
which is the row's own worked example.

### RELOCATE — none proposed

No file in `docs/handoffs/` is in the wrong genre home. `ecosystem/fleet-shape-spec.yaml:258-259`
admits `docs/handoffs` and `docs/handoffs/**`; every entry is a bundle directory, the `archive/`
subtree, or `README.md`, and each is where its genre puts it.

### RETIRE — none proposed

Nothing here is safe to delete. `CLAUDE.md` §5 rule 3 makes handoffs immutable, and 114 of 119 slugs
are cited by `JOURNAL.md` (append-only): deletion would strand live locators in the record. `[#520]`
already rules the direction as *retire-by-marker, byte-unchanged* rather than delete.

### UNDETERMINED — 0 verdicts, 2 facts this lane could not establish

Both are dating questions, and both have the same cause (§Honest limits #1): **the clone is
shallow**, so `git log --diff-filter=A` returns the graft-boundary commit `428656f` (2026-09-05) for
118 of 119 bundles. No bundle but `2026-09-06-dev-knowledge-architect` can be dated from git here.

1. **Whether `scripts/audit.py::_select_active_bundle` resolves the same bundle on a full clone.** In
   this clone the answer is forced (one bundle has a real add-commit), so the selector's
   `"add-date"` branch is untested against the real add history. The answer it gives *here* —
   `2026-09-06-dev-knowledge-architect` — agrees with the slug ordering, so nothing is wrong; it is
   simply not evidence about the selector.
2. **When the 4 boot-era bundles carrying no `PASTE_THIS.md` were cut relative to
   `scripts/assemble_paste.py`.** `2026-06-12-dev-knowledge-architect`,
   `2026-06-13-dev-knowledge-architect`, `2026-06-15-dev-knowledge-session` and
   `2026-06-25-dev-knowledge-session-close` carry `HANDOFF_BOOT.md` + `RESIDUAL.md` but no assembled
   paste (the last also has no `PROBES.md`). Pre-assembler or incomplete are indistinguishable from
   git here. Verdicts for all four come from their live-citer status, not from this.

### REPORTED, not repaired — 2 defects

**#1 · `[#520]`'s subject is still live, verified.**
`docs/handoffs/2026-08-01-dev-knowledge-architect-2/HANDOFF_BOOT.md:6` reads
`| **Slug** | `2026-08-01-dev-knowledge-architect` |` — the **sibling's** slug. Because that sibling
directory exists, the bundle's own self-references verify green about the wrong bundle, and
`scripts/check_seal_identity.py` FAILs it on any `pre-commit run --all-files` sweep. Unchanged since
`[#520]` was filed. **Reported only** — `docs/handoffs/` is immutable and this lane is read-only.

**#1b · The predecessor census's script locators have drifted, and this lane re-resolved them.**
`docs/audits/2026-08-31-census-single-file-folders.md` cites `scripts/gen_handoff.py:1143,1207` and
`scripts/audit.py:1893,1910` as the consumers of the two single-file bundles. On the current tree
those lines carry unrelated code; the live lines are `gen_handoff.py:1172,1243-1248` and
`audit.py:2724`. **The predecessor's dispositions are correct — only its line numbers moved**, which
is the failure mode of citing a `file:line` in an immutable audit against a living script. Recorded
so the next reader of that audit does not conclude its consumers vanished. No file was edited.

**#2 · `check_seal_identity.bundle_dir_for` parses `archive/` as a bundle.**
`scripts/check_seal_identity.py:50-56` locates the `docs/handoffs` segment pair and returns
`Path(*parts[: i + 3])`. For `docs/handoffs/archive/legacy/2026-04-27-stream-c-session-1-final/contents/PLAYBOOK.md`
that yields bundle root `docs/handoffs/archive` — a directory that is not a bundle and carries no
seal. **Latent, not firing:** the hook is `files: '^docs/handoffs/'` over *staged* paths
(`.pre-commit-config.yaml`, per `check_seal_identity.py:13`), and the archive tree is immutable, so
nothing under it is ever staged. It becomes a real failure the first time anything is written there
— **including the ARCHIVE proposals above**. Anyone executing an archive move should read this
first. **Reported only.**

### Cross-lane note, so nobody later claims it

`docs/audits/README.md` was **not** regenerated by this lane (`[#590]` narrowed
`audit-index-freshness`; the integrator regenerates once after the last merge). `JOURNAL.md` was not
touched, no merge was performed, and no test suite was run beyond what is stated in §Honest limits.

---

## Counts before → proposed after

Nothing changed. These are the counts a ruled-and-executed proposal would produce.

```
                                        before      after (full)   after (un-blocked only)
top-level bundle directories               119                33                        88
  pre-v5, no live citer  -> ARCHIVE         31                 0                         0
  v5/v6,  no live citer  -> ARCHIVE†        55                 0                        55
  live-cited             -> KEEP            33                33                        33
archive/ sub-directories                    15               101                        46
bytes in top-level bundle dirs      10,308,411         2,995,636                 7,410,053
                                                          -70.9%                    -28.1%
bytes under archive/                   649,960         7,962,735                 3,548,318
README.md                                    1                 1                         1
files under docs/handoffs/                 762               762                       762
total bytes under docs/handoffs/    10,976,132        10,976,132                10,976,132
```

The two byte columns move between rows; the total does not. `ARCHIVE†` is contingent on `[#520]`,
which is why the third column exists — it is the only one rulable today.

**Zero files are deleted under any proposal on this page.**

---

## Honest limits

What this census could **not** establish, stated so nothing above is over-read.

1. **The clone is shallow — no bundle but one can be dated from git.** `git rev-parse
   --is-shallow-repository -> true`; `.git/shallow` is present; `git log --oneline | wc -l -> 278`
   with the oldest reachable commit dated 2026-09-01. `git log --full-history -- docs/handoffs`
   returns **2 commits**. Consequently `git log --diff-filter=A` reports the graft-boundary merge
   `428656f` (2026-09-05) as the "add date" of 118 of 119 bundles, which is an artifact of the
   clone, not a fact about the tree. **Every "older than" judgment on this page is dated from
   directory names and from in-file era markers, never from git.** The same limit was recorded by
   the predecessor census (`docs/audits/2026-08-26-technical-handoff-census.md:38-39`) — it is a
   property of this execution environment, not a new discovery, and it has not improved.
2. **"Last content commit" is therefore unmeasurable per bundle.** One of the three witness classes
   the contract offers is unavailable here. Every verdict on this page rests on the other two —
   consumers found by `grep`, and the generator/gate that emits or reads the file. No verdict
   claims a commit witness it does not have.
3. **The consumer grep is a substring match over paths, and it inherits
   `consumer_at_landing.py`'s own recorded weakness** (`:63-64`): *"A row that names an artifact
   only to say it is obsolete counts as a citer."* A **Live** count of 1 means one file contains
   the slug; it does not prove that file depends on the bundle. The KEEP table names each witness
   individually so any row can be disputed by opening it — that is the mitigation, not a claim the
   count is clean.
4. **`Live` excludes `JOURNAL.md`, `docs/audits/`, `docs/decisions/` and `docs/intake/` by
   construction.** That exclusion is copied from `consumer_at_landing.py:31-34`, not invented here.
   It is the right call for *consumption*, and it means the **Rec** column — which does count them
   — is the only place a bundle's governance provenance shows up. Reading only **Live** would
   under-count what an ARCHIVE move disturbs: 114 of 119 slugs appear in `JOURNAL.md`, and a
   relocation changes the path every one of those citations resolves to. **This census does not
   measure how many JOURNAL citations are path-shaped vs. slug-shaped, and that number should be
   established before any move is executed.**
5. **Two `docs/handoffs/…` paths cited in `JOURNAL.md` do not exist on disk** — `docs/handoffs/
   in-progress/` (4 occurrences) and `docs/handoffs/_references/` (4 occurrences). `JOURNAL.md` is
   append-only history, so these may be truthful records of directories that later went away; this
   lane could not distinguish that from a never-existing path, **because of limit #1**. Recorded as
   an observation, not a defect.
6. **Era classification is inferred from the file roster, not read from a version field.** No bundle
   carries a machine-readable `handoff-process` version stamp that this lane could find. The
   `v5/v6/v7` class is therefore one bucket of 78 and is **not** decomposed into v5 / v6 / v7 —
   which matters, because the ARCHIVE† group's real boundary is probably an era boundary rather
   than the window boundary the contract's question names.
7. **No test suite was run, and the declared environment could not be built.** The contract
   forbids the full suite (known RED on `main`, `test_manifest_link_route.py`); this lane changes
   no code, so no targeted suite applies either. Separately, **`uv run --locked` does not work in
   this container**: `pyproject.toml` pins `required-version = "==0.11.19"` and the container ships
   `0.8.17`, so every `uv run --locked …` invocation refuses before running anything. The three
   gates that bind a new `docs/audits/*.md` were therefore run under **system `python3`**, which
   is not the declared interpreter:

   ```
   python3 scripts/consumer_at_landing.py            rc=0   landing leg: 0 failures
                                                            consumption leg: this file WARNs as
                                                            uncited, alongside ~25 peer artifacts
                                                            from batch U wave 2 — expected for an
                                                            artifact on the commit that adds it
   python3 scripts/gen_audit_index.py --check-titles  rc=0
   python3 scripts/validate_hermetization.py <this>   rc=0
   python3 scripts/check_seal_identity.py             COULD NOT RUN — ModuleNotFoundError: click.
                                                      Out of scope anyway (files: '^docs/handoffs/')
   ```

   **The commit hooks were never armed in this container** — `.git/hooks/` holds only samples and
   `pre_commit` is not importable, so `pre-commit install` (which `SessionStart`'s `arm_hooks.py`
   normally does) had nothing to run and the commit carrying this file passed through no gate. The
   four green lines above are this lane running the gates by hand, out of band. **The integrator
   should treat this file as ungated at commit time** and let the pre-merge sweep be the first real
   gate it meets.

   `docs/audits/README.md` was deliberately **not** regenerated (`[#590]`). Nothing on this page is
   backed by a green suite; three gates are green under an undeclared interpreter, and that
   distinction is stated rather than left to inference.
8. **Byte figures are `du -sb` / `stat -c%s` on the working tree, not blob sizes.** `du` on a
   directory includes the directory inode itself, which is why the 119 bundle sums plus `archive/`
   plus `README.md` reconcile exactly to `du -sb docs/handoffs` here but would not on a filesystem
   with a different block accounting.
9. **`archive/` was inventoried as one row, not 16.** Its 15 sub-directories + `legacy/` were
   sampled (roster and byte comparison against the same-named top-level bundles, which is what
   falsifies the duplication hypothesis) but not verdicted individually. The predecessor census
   ruled that subtree; re-verdicting it was out of scope and would have been re-litigation.

### Fan-out — reported, including its absence

```
gemini fan-out:        NONE
  reason:              `which gemini` -> exit 1; the CLI is not on PATH in this container
  files read by Gemini: 0
  fabricated locators:  0 of 0 returned  (no locators were returned; 0 is not a clean score)
copilot enterprise:    NOT AVAILABLE — offload is gated on #75, which is not ratified.
                       It was not used, and nobody should later record that it was.
```

**Absence is not cleanliness.** Every locator on this page was opened by this lane directly —
`sed -n '<line>p' <file>` or `grep -n` against the named file — because there was no reader to
cross-check. That is a smaller sample than a fan-out would have produced, not a safer one.

---

**Lane:** S-05 · **Branch:** `claude/census-docs-handoffs`
**Measured at:** `origin/main` `5f27b20`. **Re-verified after syncing to `21576e3`:**
`git diff --stat 5f27b20 21576e3 -- docs/handoffs` is empty, and the three corpus figures re-measure
identically (119 / 762 / 10,976,132 B). Every count on this page holds at the pushed head.
**Written:** 2026-09-07 · **Read-only:** no file under `docs/handoffs/` was moved, deleted, edited or
renamed; the only file this lane wrote is this one.
