**RECON COMPLETE — read-only, no writes, working tree clean.**

````
CLOUD-NIGHT-C3 — APPEND-ONLY SURFACES ROTATION (RECON)
Repo .dev-knowledge @ d8211b0 (origin/main). CLOUD, READ-ONLY. Zero writes; zero gates run.
Every number below is measured on this checkout with the command named, or cited at file:line.
CAVEAT: this clone is SHALLOW (git rev-parse --is-shallow-repository = true; 310 commits,
72 first-parent spine entries). ADR-85's floor 24882f8cc is BELOW the boundary, so spine
counts above the floor could not be measured here. Byte/entry measurements are unaffected.

0 · THE ROW — FOUND, AND IT IS NOT A ROW
  The spec exists: docs/audits/2026-08-25-technical-register-ruling-packet.md:133-139,
  "H-plus (operator-priority 2026-08-25): JOURNAL rotation", under ARC-H. Verbatim done-when
  equivalent (the packet's Row spec sentence):
    "split into a small LIVE file (current period; the spine/anchoring predicate and
     block-unanchored-push keep reading THIS file only) + dated archives under docs/;
     universal across fleet repos; before/after timing measured in the closing artifact."
  NO tasks/*.md row was ever born for it. Verified three ways: `grep -rli rotat tasks/*.md`
  = 0 hits; no `title:` in tasks/ names rotation; `rotat` occurs 0 times in tasks/manifest.json.
  Meanwhile intake #49's own frontmatter names three consumers and only two exist —
  [#589] (VIEW half) and [#590] (concurrency half). The JOURNAL half is an ADR-111 CANDIDATE
  that never became an intake-carried row. Its nearest ratified done-when is intake #49
  acceptance criterion 4 (docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md:77):
    "JOURNAL.md live file is < 100,000 bytes after rotation, and journal_spine_anchor plus
     block-unanchored-push still pass against it."

1 · CONSUMER INVENTORY (every reader, by file:line)

  HARD GATES — refuse a push / FAIL an audit
  - scripts/journal_anchor.py:42 _JOURNAL="JOURNAL.md" — the ONE path constant
  - scripts/journal_anchor.py:116 journal_text() — whole-file read (tree, or `git show rev:`)
  - scripts/journal_anchor.py:203 is_anchored() — `c[:7] in journal`, substring over the WHOLE text
  - scripts/journal_anchor.py:208/220 unanchored_in_range / range_is_anchored — pre-push verdict
  - scripts/journal_anchor.py:232 unanchored_on_spine() — backstop, entries ABOVE ADR-85's floor
  - scripts/journal_anchor.py:319 mention_not_record_warnings() — advisory WARN, whole-file
  - scripts/block_unanchored_push.py:57,126,127,130 — pre-push HARD leg, fails CLOSED (exit 2)
  - scripts/audit.py:3007-3101 check_journal_spine_anchor — backstop; a gap is FAIL, not WARN
  - scripts/audit.py:3133 check_journal_day_letters — whole-file regex, floor _JOURNAL_DAY_LETTER_FLOOR
    = "2026-07-30" (audit.py:3116)
  - scripts/session_end_backpressure.py:143,297-346 — reads the COMMIT'S OWN DIFF additions via
    git show, never the file. Advisory since ADR-85 §A5. Rotation-immune.
  - scripts/audit.py:3322-3350 check_review_artifact_coverage — reuses journal_anchor's spine walk
    and introduced(), NOT the journal text. Rotation-immune.

  SHAPE / NAME / MANIFEST checks
  - scripts/canonical_docs.py:45,68 JOURNAL ∈ CANONICAL_MANDATORY; :117 CANONICAL_SPINE requires
    the literal heading "# Journal"
  - scripts/canonical_docs.py:81 FRESHNESS_FILES — JOURNAL deliberately EXCLUDED (rationale
    stated at audit.py:349-352). A new archive file inherits that exclusion only if named so.
  - scripts/audit_checks/check_canonical_md_visibility.py:22, check_adr38_baseline.py:31-32
  - deploy/manifest-v1.4.0.yaml:827-829 (and v1.1.0:406, v1.2.0:621, v1.3.0:686, v1.3.1:695) —
    spine ["# Journal"], freshness_gated: false

  COMMIT-TIME REWRITER — will touch archive files too
  - .pre-commit-config.yaml:52-57 normalize-dated-headers → scripts/normalize_headers.py:4,17.
    types:[markdown], pass_filenames:true, so ANY JOURNAL-legacy-*.md that is ever re-staged is
    rewritten by it. This is the one hook that can violate byte-identity after a split.

  PATH-KEYED CLASSIFIERS — each hardcodes the basename and each needs the archive glob added
  - scripts/preflight_contract.py:95 _CITATION_FILES ("JOURNAL.md","LESSONS.md")
  - scripts/audit.py:3170 doc_claims — JOURNAL is citation-role wholesale (not assertion-role)
  - scripts/scan_undeclared_edges.py:83 _APPEND_ONLY_FILES
  - scripts/nopack_sandbox.py:229 NEVER_REMOVE
  - scripts/generate_floor.py:258 F5_BLACKLIST — the child floor must NOT name JOURNAL.md
  - scripts/propose_closures.py:103 _CHURN_FILES
  - scripts/enforcement_coverage.py:291-292,397,510-515 — WRITES a synthetic JOURNAL.md into a
    throwaway clone to probe the anchor gate; applicability is `(root/"JOURNAL.md").exists()`

  GENERATORS / AGENTS / HUMANS
  - scripts/gen_handoff.py:691,862-884 journal_draft — emits a draft, never writes the file
  - .claude/workflows/conformance-hub.js:125-129 — V1 verifier reads "the LAST 10 entries"
  - CLAUDE.md:25 + templates/claude-regions/first-read.md:6 + PLAYBOOK.md:1352 — boot read,
    "last 5 entries" (a hub region: the template moves in lockstep or fleet parity breaks)
  - PLAYBOOK.md:1059,1082,1102,1211,1909-1920; ESSENTIALS.md:127,132; VISION.md:188;
    .claude/commands/lane-boot.md:143-144 (JOURNAL-rides-the-branch)

  THE BLINDEST CONSUMER, and it is not the anchor gate:
  check_journal_day_letters (audit.py:3133) regexes the whole file for duplicate day letters.
  Shrink the file and it silently sees FEWER headings, so it PASSES harder — it fails OPEN on
  rotation with no error. is_anchored fails the other way: a shrunken universe can only turn a
  pass into a FAIL, loudly. The open-failing one is the hazard.

  GOVERNANCE CONSTRAINTS (the real blockers)
  - ADR-29 amendment 2026-07-17, docs/decisions/ADR-29*.md:122, verbatim: "The stricter
    JOURNAL / logs/TOKEN-LOG append-only rules ... are preserved unchanged." The chronological
    archival exception was granted to LESSONS.md ONLY and explicitly withheld from JOURNAL.
    Rotation is therefore a governance act before it is a code act.
  - STANDING_RULINGS B6 (:237), restated at PLAYBOOK.md:1914-1918: an anchor discharges by
    APPEND ONLY, "the predicate matches a SHA anywhere in the file, so editing a landed entry
    discharges the anchor retroactively". Removing text is the mirror image: it UN-anchors
    retroactively, and leaves no trace it once did.
  - ADR-60 Rule 5 (PLAYBOOK.md:605) — append-only records are not rewritten on move; this is
    what SANCTIONS a byte-identical relocation once the amendment exists.

  W2A POST-CHANGE SHAPE — ASSUMPTION, STATED
  Branch worktree-w2a-perf-core is NOT visible from here: `git ls-remote origin` returns only
  refs/heads/main and refs/heads/automation/fleet-audit (measured). Design is therefore against
  the frozen spec, not the branch: docs/audits/2026-08-26-technical-perf-recon.md:249-254 (P-1)
  + tasks/587-...md — "one precomputed {short_sha -> (mentioned, recorded)} map built in ONE
  pass over JOURNAL.md; findings byte-identical to today". THIS IS THE GIFT: after W2A the whole
  consumer surface collapses to ONE function that turns ONE string into ONE map. Rotation then
  changes that function's INPUT and nothing else.

  MEASURED SIZE COST (python3, this box, 2,931,155 chars / 1,002 entries):
    read whole file                 23.1 ms
    entry split (regex)             37.1 ms
    one-pass short-sha map          80.6 ms  -> 3,063 distinct short SHAs
    100 substring scans            286.9 ms  (~2.87 ms each — today's per-commit shape)
  So AFTER W2A the gate's whole-file size cost is ~104 ms per process. Rotation buys ~0.1 s.
  THE GATE IS NOT THE REASON TO ROTATE. The reasons are: context (736,707 tokens, intake #49:21),
  grep/agent readability, and collision — 64 of 310 available-history commits (21%) touch
  JOURNAL.md, every one of them prepending at the same offset (~line 20), which is the single
  hottest merge point a parallel lane can land on.

  BYTES BY MONTH (awk over the headings): 2026-03 1,152 · 04 27,540 · 05 199,144 ·
  06 724,985 · 07 1,008,003 · 08 996,920 (+935 header). August: 246 entries / 996,920 B =
  ~4,053 B/entry. So intake #49 AC4 (<100,000 B live) implies an active window of ~24 entries —
  roughly THREE WEEKS at current velocity, not "the current month". Name that or AC4 is unmeetable.

2 · ROTATION DESIGN OPTIONS

  (a) DATED ARCHIVES + ACTIVE WINDOW, gates read active-only  [the H-plus spec as written]
      Breaks: nothing at push time — range_is_anchored only ever reads the range being pushed,
        which is always new work. The exposure is the BACKSTOP: unanchored_on_spine scans every
        spine entry above ADR-85's floor 24882f8cc / 2026-08-02 (ADR-85:256, parsed by
        journal_anchor.floor_sha:86). If a rotation boundary ever rises above that floor, the
        anchors for the archived entries leave the file the backstop reads and it FAILs — loudly,
        but on history nobody can fix by append (B6 forbids editing them back in).
      Survival rule, and it is checkable: the archive boundary must stay STRICTLY OLDER than the
        floor. Today that is trivially satisfiable (floor is 2026-08-02; 07-and-older is 1.96 MB,
        67% of the file). But floor and boundary are coupled forever after, and nothing today
        enforces the coupling — a floor advance in an ADR-85 amendment would silently outrun it.
      Consumers changed: journal_anchor (boundary logic), day_letters (floor vs boundary),
        the 6 path-keyed classifiers, normalize-dated-headers scope, the manifest + canonical_docs
        entry for the new file class, CLAUDE.md §1/§4 + its hub template.
      Migration cost: HIGH — dominated by governance, not code (see §4).

  (a′) DATED ARCHIVES + ACTIVE WINDOW, gates read the TILED WHOLE   [recommended variant]
      Same on-disk layout; ONE difference: journal_text() returns live + JOURNAL-legacy-*.md
      concatenated in date order. The predicate's universe is then unchanged BY CONSTRUCTION —
      byte-identical findings, no floor coupling, no boundary rule to get wrong, and the day-letter
      check keeps its whole-history view instead of failing open. Cost is the 23 ms read + 81 ms
      map we already pay, unchanged. Humans and agents read only the ~100 KB live window; the
      gates read everything. This does not answer intake #49's open question 1 — it DISSOLVES it:
      an anchor referencing an archived entry stays provable because the archive is still in the
      string the predicate is handed.
      Consumers changed: journal_anchor.journal_text ONLY, plus the path-keyed classifiers'
      globs. Zero predicate change, zero floor coupling, zero new failure mode.

  (b) YEAR/MONTH SHARDING
      Breaks the single narrative — and ADR-29:73 already ruled against exactly this reasoning
      ("a by-scope split shatters the single chronological narrative into parallel logs"). Worse,
      it buys NO collision relief: newest-first prepend means the current month's shard is still
      the hot file every lane writes to. 6 files today, ~12/yr, each one a normalize-dated-headers
      target and a manifest/canonical_docs entry. Migration cost HIGH, payoff strictly less than
      (a′). REJECT.

  (c) LEAVE BYTES, FIX ACCESS (generated index + viewer)
      Breaks nothing. Zero governance cost — no append-only rule is touched, so no ADR act.
      Consumers changed: none; one new generator + its freshness gate. Fixes the LARGEST measured
      cost (context/navigation) and none of the others: grep still sweeps 2.9 MB, and every lane
      still prepends to the same line. Migration cost LOW. Composes with (a′) rather than
      competing — the index is what makes a rotated archive navigable anyway.

3 · LESSONS ORGAN TIE-IN
  It shares the ARCHIVAL half of the mechanism and not the ORGAN half. The chronological
  byte-identical relocation is already fully ratified for LESSONS — ADR-29 amendment 2026-07-17
  (:70,:77,:78), its ADR-39 six-element registry entry for the LESSONS-legacy-<span>.md file class
  (ADR-39:403-407), and a byte-identity test spec that diffs the moved block against the PRE-SPLIT
  BLOB of the parent commit (ADR-29:97) — so one parameterised archival executor (file, boundary,
  proof) serves both surfaces, and JOURNAL needs only its own amendment to use it. The organ half —
  intake #49's one-lesson-one-file with front-matter — is a SHAPE change that ADR-29's append-only
  rule does not admit, which is precisely intake #49 open question 3, and it shares nothing with
  rotation. Two live findings while I was there: LESSONS.md is at 303 entries (`grep -c` on the
  dated headings) against ADR-29's ratified trigger of 300 (:87) — THE TRIGGER HAS TRIPPED AND
  NOTHING FIRED; and no split tooling exists (`grep -rl LESSONS-legacy scripts/ tests/` returns
  only preflight_contract.py), so [#339]'s build leg is still blocked with no open row carrying it.

4 · RECOMMENDATION — (a′), and the first slice moves ZERO bytes

  Take (a′): rotate the FILE, not the PREDICATE. It is the only option where the anchor question
  has no answer to get wrong, and it is strictly cheaper than (a) because it deletes the
  floor/boundary coupling that (a) would have to invent and then enforce forever.

  SMALLEST FIRST SLICE (one commit, no governance act, no ADR):
    Make journal_anchor.journal_text() tiling-aware — read JOURNAL.md plus sorted
    JOURNAL-legacy-*.md and join in date order — and land it BEHIND W2A's map inversion so the
    single-pass map is built from the tiled text. On today's tree the glob matches nothing, so the
    returned string is byte-identical and every finding is unchanged. Ship it with one test
    asserting exactly that (tiled read == single-file read on a tree with no legacy files) and one
    asserting a synthetic two-file tiling reproduces the same anchor verdicts. This buys the seam
    before it is needed, which is the whole point: when the split finally lands, no gate changes.
  ROLLBACK: revert one function in one file. No tracked content has moved, so there is nothing to
    restore. Thereafter each later slice reverts independently — and the split commit itself is
    revertible byte-exactly, because the pre-split blob IS the parent's blob (ADR-29:97's own
    argument, reused rather than restated).
  THEN, in order and separately: (2) the ADR-29 amendment extending the sanctioned chronological
  split to JOURNAL + the ADR-39 registry entry for JOURNAL-legacy-<span>.md + the cross-doc
  reconciliation set — the prerequisite list the 2026-07-17 amendment already ratified (ADR-29:114,
  :122), so this is a fill-in, not a design. (3) the first split, boundary 2026-07-31 or older.
  (4) option (c)'s generated index over the tiled whole.

5 · PROPOSED ROWS — CANDIDATE ONLY (ADR-111), NOT FILED

  C-1 · [P1][S] Tiling-aware journal read — the seam, before the split
    Done when: journal_anchor.journal_text returns JOURNAL.md tiled with sorted
    JOURNAL-legacy-*.md in date order; a test proves the tiled read is byte-identical to today's
    single-file read on a tree with no legacy files; a second test proves anchor verdicts are
    unchanged across a synthetic two-file tiling; block_unanchored_push and
    check_journal_spine_anchor still share ONE predicate with no second implementation.
    Depends on [#587] (W2A) landing first. kill-candidates: none — no open row touches journal_text.

  C-2 · [P1][M] The JOURNAL rotation governance act — carrier for intake #49's missing third half
    Done when: an appended ADR-29 amendment extends the chronological byte-identical archival
    exception to JOURNAL.md (ADR-29:122 currently withholds it explicitly); an ADR-39 six-element
    registry entry for the JOURNAL-legacy-<span>.md file class exists BEFORE any such file is
    created; the cross-doc reconciliation set lands atomically (CLAUDE.md §4/§5 + its hub template,
    ARCHITECTURE, PLAYBOOK, the deploy manifests' canonical block); and the active-window size
    target is stated in ENTRIES, reconciled against intake #49 AC4's 100,000 bytes (~24 entries at
    the measured 4,053 B/entry). kill-candidates: none — the H-plus spec never became a row.

  C-3 · [P2][M] One archival executor, two surfaces — and LESSONS' tripped trigger
    Done when: a single parameterised splitter (file, boundary, byte-identity proof against the
    pre-split blob per ADR-29:97) executes an archival for LESSONS.md — now at 303 entries against
    the ratified 300-entry trigger, with the 180-entry hysteresis target of ADR-29:87 — and is
    reusable unchanged for JOURNAL once C-2 lands; normalize-dated-headers is proven not to rewrite
    an archived file; and the tiling (no gap, no overlap, strict date order) is enumerated by the
    tool, not asserted. kill-candidates: none — [#4] is deferred and indexes lessons, it does not
    move them.

DECISION OWED BEFORE ANY BUILD (architect, per ADR-108 §A — technical): (a) vs (a′), i.e. do the
gates read active-only or the tiled whole. Everything downstream forks on that one answer.
````

Three things worth your attention beyond the deliverable:

- **The rotation row does not exist.** The H-plus spec sits in the ruling packet; intake #49 names JOURNAL rotation as a consumer, and its two siblings ([#589], [#590]) were born while this one was not.
- **`LESSONS.md` is at 303 entries against ADR-29's ratified 300-entry trigger.** The trigger has tripped, nothing fired, and no split tooling exists.
- **After W2A, rotation buys ~0.1 s of gate time, not seconds.** The measured case for rotation is context (736k tokens), grep, and merge collisions (21% of commits prepend to the same offset) — not the anchor gate. Worth saying out loud before the row is written against a performance premise it can't deliver.