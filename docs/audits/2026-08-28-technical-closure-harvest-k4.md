# Closure-harvest lane — MORNING PACKET §K4 verdicts executed

<!-- scope: meta -->

**Date:** 2026-08-28 · **Lane:** `docs/closure-harvest-k4`, primary checkout, serial commits
**Source:** `MORNING-PACKET-2026-08-27.md` §K4 (the 35-row HOLD table) + four operator
amendments delivered mid-lane
**Consumer:** `JOURNAL.md` 2026-08-28; the rows this lane closed, re-cut and birthed;
`protocols/HANDOFF_PROCESS.md` v6.3.0 section history

---

## 1. What was executed

| Act | Instruction | Outcome |
|---|---|---|
| 1 | DO-IT eight | **7 closed**, 1 re-cut with a structural reason |
| 2 | RE-CUT six | **6 narrowed**, each shipped half closed on verified evidence |
| 3 | DECIDE two | `[#391]` **ruled + closed**; `[#267]` **HELD** on a real contradiction |
| 4 | Ledger arithmetic + D6 births | **3 rows born**, funded, arithmetic below |
| 5 | D-R1 role residency + Amd 2/3 versioning | **HANDOFF_PROCESS v6.3.0** shipped |

### Act 1 — the DO-IT eight

- **`[#335]`** VERIFIED-THEN-CLOSED. The verdict assumed the false positive "may already be
  gone"; **one live run refuted that** (`warn: templates/CONTRIBUTING-md-template.md:
  malformed`). So the row was **landed**, not closed on a stale premise: a `templates/`
  placeholder exemption narrow on both axes, three tests, disposition removed.
- **`[#348]`** CLOSED with its ADR-105 routine block **re-anchored** to `protocols/PLAYBOOK.md`
  §10. The 2026-08-22 re-peg held it open because the row was the declaration's only carrier —
  a mortal carrier. Re-anchoring is the fix, not deferral.
- **`[#71]`** CLOSED against **live L0 state** the 2026-08-23 pass could not reach (it ran in a
  cloud container and said so). `commands/`+`skills/` matched as written; `hooks/` and `memory/`
  did not. The Rejected-list Codex entry — the half LANE-L5 left standing — is annotated.
- **`[#266]`** CLOSED at both named carriers in one act: the EPIC_BOOT FILE-BOUNDARY template and
  an **appended** ADR-97 Amendment (in-file marker per CLAUDE.md §5 rule 3, never in-place).
- **`[#99]`** CLOSED. A red digest row now names its failing checks, proven against the **real**
  `ecosystem/` states, not a fixture. 6 tests.
- **`[#296]`** CLOSED on the **second** branch of its own Done-when ("or prints where it actually
  lands") — the report is not misplaced, it is deliberately isolated onto `automation/fleet-audit`.
  6 tests, incl. an end-to-end pin asserting both halves at once.
- **`[#127]`** CLOSED. Actionable failure block + a **bitmask** exit code (pytest 2 · ruff 4 ·
  git 8) so an iterate-until-green loop can tell it made no progress. 14 tests.
- **`[#274]`** **RE-CUT, not closed.** Leg 1 landed; leg 2 requires *"one **subsequent**
  changelog-review digest"* and the command is PUSH-trigger by its own frontmatter — no act that
  writes the rubric can produce the run that consumes it. Faking it would be a false closure.

### Act 3 — the two DECIDE rows

**`[#391]` — both options measured before choosing, then the smaller executed.**

| Option | Size | Blocker found by measuring |
|---|---|---|
| A: wire it nightly | **M** | `routine_consumers` reads BACKLOG rows only, so the declaration would live in a mortal carrier (the defect `[#348]` closed the same day); and there is **no live Tier-2 nightly surface** — intake #60 is defining that protocol now, so A invents a rival |
| B: narrow to a manual reporter | **S** | none — `[#384]` is already closed and a repo-wide grep finds exactly ONE live surface, which already said "manual CLI" |

Executed **B**. The row's own premise (*"#384 claims 'runs as a nightly lane'"*) is recorded as
**stale**: that claim now survives only in gitignored proposals and immutable dated artifacts.

**`[#267]` — HELD, and the instruction's own escape clause is why.** Quoted verbatim, the LEAN is a
**two-part** mechanism: *"(iii) instruct-the-child for the n=1 attended witness; (ii)
discover-from-config at fleet-scale, **coupled to P6**."* **P6 is UNOWNED** — `[#221]` closed at
`8aab4356` with no successor, per `[#244]`'s own body. Ratifying it whole binds a fleet-scale
mechanism to a carrier nobody owns. Part (iii) is independently executable; part (ii) is blocked.
**Unblocking needs one word:** (a) adopt-deferred behind a P6 successor, (b) drop (ii), or
(c) re-couple to a carrier that exists.

---

## 2. Ledger arithmetic (PLAYBOOK D3/D5 — births <= `banked_D`)

```
opening balance                                   0   (morning packet, THE NUMBERS)
closures this lane                               +8   [#335] [#348] [#71] [#266]
                                                      [#99] [#296] [#127] [#391]
banked_D                                          8
births spent                                     -3   [#609] [#610] [#611]
remaining banked                                  5
```

Closures were made **before** filing, which is the point of the D3/D5 order: the cap has to be
known before it is spent. Row count moved **206 -> 203 -> 206** (eight closures, three births, six
narrowings that move nothing).

| Born | Funded by | kill-candidates (proposal only) |
|---|---|---|
| `[#609]` free ruff ratchet | intake #58 / I-KODEKS, X3+X4 | `#334` |
| `[#610]` night-batch protocol | intake #60 / I-NIGHT, X8 | `#271` |
| `[#611]` HANDOFF_PROCESS v7 | operator Amendment 4 | `#511` |

Amendment 4's conditional resolved **in favour of birth**: 8 banked covers 3.

---

## 3. Amendment 3 — the version surface, MEASURED not trusted

Repo-wide grep for handoff version markers: **874 hits**, every one classified. Zero unclassified.

| Class | Hits | Disposition |
|---|---:|---|
| **(a) LIVE-NORMATIVE** | 15 sites | updated to **6.3.0** (enumerated below) |
| **(b) STRUCTURAL-LEGAL** | 1 file | `templates/handoff/v5/` — a folder name, **not renamed**; CANDIDATE recorded |
| **(c) HISTORICAL-IMMUTABLE** | 701 | dated audits / handoffs / archives, JOURNAL, LESSONS, gitignored `logs/`, the generated `BACKLOG.md` view, and in-spec citations of the version that *introduced* a clause |

**The (a) set, and the proof it equals what was updated:**

| Site | Form | Updated |
|---|---|---|
| 8 x `reconciled_with` frontmatter | `handoff-process@6.2.0` | yes |
| `protocols/HANDOFF_PROCESS.md` | `Version: 6.2.0` | yes |
| `CONTRIBUTING.md` | `stamp v6.2.0` (the `handoff_version_stamp` gate reads it) | yes |
| `protocols/SESSION_SETUP.md` x2 | prose `v6.2.0` | yes |
| `protocols/PLAYBOOK.md` | "Authoritative spec ... v6.2.0" | yes |
| `docs/handoffs/README.md` x8 | prose — incl. **six** "role file is inlined" claims | yes |

The eight `reconciled_with` edges were derived **live** from
`validate_reconciliation.discover_dependents`, not from a list: the v6.2.0 section-history entry
says **"six"**, and that number went stale when `PLAYBOOK.md` and `SESSION_SETUP.md` joined. **This
is Amendment 3's own vindication** — the six "inlined" prose claims in `docs/handoffs/README.md`
appeared in **no** enumerated surface list, and a trusted list would have shipped v6.3.0 carrying
six live false statements about its own central change.

**Deliberately NOT updated, with reasons.** Files saying plain **"v6"** (`.claude/commands/handoff.md`,
`.methodology.yaml`, `ecosystem/parity-surfaces.yaml`) are live-normative but state the **major**,
which a minor bump leaves true. Test fixtures pin arbitrary versions by design.
`ecosystem/.dev-knowledge/state.yaml` is generated audit evidence and self-corrects on the next run.

---

## 4. Act 5 measurement — the residency flip

Re-assembled `docs/handoffs/2026-08-25-dev-knowledge-architect` from its own sources into a
**scratch copy** (the committed bundle is immutable and was not touched):

```
PASTE_THIS.md   before  50,852 bytes
                after   34,624 bytes
                drop    16,228 bytes
```

Not a round number, and that is the proof: the role file is **17,196** bytes, so the body gave back
17,196 and took on ~968 for the pin, its section label and the separator. Verified on the same
artifact — the PIN renders at v6.3.0, its `sha256` equals `sha256sum protocols/HANDOFF_BOOT.md`
byte for byte, and the role body is gone.

**Coherence proven on the branch:** `reconciled_versions` pass (8 edges) · `silent_rule_ratchet`
pass (443 <= 443) · `verify_handoff_probes` pass (14 probes) · `handoff_version_stamp` pass ·
`boot_byte_budget` pass · `audit.py health` OK.

The ratchet first went **+3**. All three additions were **restatements of the unchanged
requirement** — the organ firing on quotation, not on new doctrine — and were drained by rewording
rather than by a SKIP or a baseline raise.

---

## 5. CANDIDATEs recorded (ADR-111 §1(c)) — findings that are NOT rows

Each is triaged, none silently absorbed, none birthed (the funnel's only path to a row is
CANDIDATE -> intake -> ratification):

1. **The global `~/.claude/memory/` protocol gap.** The global CLAUDE.md Self-Evolution Protocol
   step 1 directs a read of `~/.claude/memory/learned-rules.md`, which **does not exist** (nor do
   `README.md`, `evolution-log.md`, `observations.jsonl`, `violations.jsonl`; live state has two
   files). **L0, outside this repo's write scope** — the hub cannot discharge it (Layer-2
   invariant). Recorded in `protocols/ENVIRONMENT.md`'s tree block. Found while closing `[#71]`.
2. **`templates/handoff/v5/` rename.** STRUCTURAL-LEGAL under Amendment 3; a rename is a real
   change with real reference cost and was explicitly not executed here.
3. **`templates/handoff/README.md.tmpl` claims "Generated by HANDOFF_PROCESS v4.4 (status:
   live)"** — a *live* version claim that is three majors stale. NOT updated: its own in-file
   comment defers it to `#164`, and rewriting a v4.4 citation to v6.3.0 would fabricate history.
4. **ADR-115 vs `CLAUDE.md` §10.** ADR-115 (Accepted 2026-08-25) supersedes ADR-53 D2 and amends
   ADR-101 §1 to admit `AGENTS.md`, but §4's enum diff is **deliberately unapplied**, so the gate
   still refuses. `CONTRIBUTING.md` is corrected here to hold both facts; `CLAUDE.md` §10's
   anti-pattern is **still false doctrine**, owned by `[#577]` — it sits in a hub-single-sourced
   Form-A region needing a lockstep template act.
5. **`CLAUDE.md` §6 step 5's bare `pytest --collect-only`** — the ADR-106 defect, same class of
   hub-single-sourced region. Unchanged from v2.66; recorded again rather than fixed half-way.

---

## 6. Deviations from the instruction, stated

1. **`[#274]` was not closed.** The DO-IT verdict was executable only for leg 1; leg 2 is
   structurally undischargeable in the same act. Re-cut and pegged instead of faked.
2. **`[#267]` was not decided.** The instruction's own escape clause ("unless quoting it reveals a
   contradiction — then HOLD and report") fired. Reported at §1.
3. **`[#112]`'s cited evidence was wrong and is corrected on the record.** The K4 case credited
   *v2.65 rule-7* with resolving the CLAUDE.md §5 leg; that edit re-scoped the `.claude/rules/`
   carve-out, a different rule on a different subject. What discharges the leg is **rule 3's own
   ADR-94 exception**. Same conclusion, correct evidence.
4. **`[#146]`'s authorship question resolved against the row.** `git log -S` returns exactly one
   commit — `4b27125e`, subject *"docs(playbook): **#11** methodology home..."*. Clause (a) is
   therefore **satisfied-by-#11**, credited to #11, and this row is not closed on it.
5. **`[#335]`'s first close was silently reverted and had to be redone.** `--emit-source`
   re-derives frontmatter from the manifest, so `status: closed` without removing the manifest
   node prints "refreshed derived frontmatter" and reverts the close — with every gate green,
   correctly, because nothing was incoherent. Closes are verified here by **row count**, never by
   the generator's own success.
6. **Two scratch files** (`Last`, `**Living`) were created by a mangled shell command mid-lane and
   **removed and verified removed** before the next commit (CLAUDE.md §5 rule 9, no leftovers).
