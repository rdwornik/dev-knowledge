Read-only pass complete. Report follows — flat and fenced per the output-formatting convention (§4), so it copies out without TUI border glyphs.

```
CLOUD-NIGHT-C1 — DOC-DIET EXECUTION PLAN (read-only)
Substrate: cloud, no writes. Tree: HEAD d8211b0 (= origin/main, detached). Date 2026-08-26.
All sizes measured live with a fence-aware `## ` scanner; all locators re-resolved on this tree.

MEASUREMENT BASIS
  protocols/PLAYBOOK.md      5208 lines   (Part I 300-3518 = 3219 | Part II 3519-5014 = 1496 | apps/addenda 5015-5208 = 194 | front+TOC 1-259)
  protocols/ESSENTIALS.md     185 lines
  ARCHITECTURE.md            1160 lines   (prose ~1148 | generated CODEMAP region 227-238 = 12)
  CLAUDE.md                   239 lines   -- OUT OF SCOPE per R-F2 (Form-A fleet-parity surface)

CENSUS INPUT CONSUMED: docs/audits/2026-08-20-technical-playbook-status.md item 3 (19 findings, 484-line audit),
reached via [#569]'s closure note (tasks/569-*.md, "CLOSED 2026-08-26 ... NOT discharged: the 19-finding census")
and register W5 (protocols/STANDING_RULINGS.md:2924-2934). The census was taken at 1def12f; every line number
below is RE-MEASURED at d8211b0, and two census values have themselves rotted (noted inline).

=========================================================================================
1. PLAYBOOK DIET PLAN
=========================================================================================
1a. PER-CHAPTER DISPOSITION (start line, size in lines, verdict)

  front matter + TOC     1-259    259  KEEP-GENERATED. TOC:START at :18 is regen-gated by the
                                       `toc-freshness-playbook` pre-commit hook. Never hand-edit; every
                                       heading act below forces a regen in the same commit.
  The two lifelines      260      37   KEEP. The frame the chapter map hangs on. Zero findings.
  Ch1 System Arch        300      16   KEEP (already pointerised to ARCHITECTURE Ch1). Carries H6.
  Ch2 CLAUDE.md contract 316     155   SHRINK -> pointer. It restates CLAUDE.md's own section model
                                       (:339 "v2.1 template, 12 sections"). Cut to the contract rule +
                                       a pointer to CLAUDE.md; ~90 lines recoverable.
  Ch3 Repo conventions   471     165   SHRINK. :475 already declares the subsections are ADR pointers;
                                       finish the job. Holds H19a/H19b (:610/:617). ~60 lines.
  Ch4 Prompt-writing     636     154   KEEP. Human-facing functional doc, the R-F2 core audience.
  Ch5 Complexity bands   790     254   UNTOUCHABLE (brief: tier cadence).
  Ch6 Doc types + cont.  1044    178   SHRINK-partial. Carries 6 of the 14 <!-- rule: --> tokens
                                       (:1093 :1108 :1118 :1126 :1132 :1140) -- those paragraphs are
                                       doc_code_edge FIXTURES and must not be deleted. Only the
                                       taxonomy table (:1056 H4, :1066 H13) is dietable. ~25 lines.
  Ch7 Review postures    1222     16   KEEP. It is the citation ruling H6-H12 are judged against.
  Ch8 Session boundaries 1238   1541   UNTOUCHABLE (brief: sole literal-command site). 29.6% of the
                                       file. Its heading "The dispatch table -- the SOLE literal-command
                                       site" (live :2236) is a /handoff-verify PASS/FAIL probe.
                                       Correction-only inside it: H2 (:1869).
  Ch9 Tier-1 closure     2779     25   KEEP.
  Ch10 Two-tier autom.   2804     38   KEEP.
  Ch11 Routine/night     2842     98   MOVE-candidate -> ARCHITECTURE Ch3 "Automation axes" (:730),
                                       which already owns the axis. Leave a one-line pointer. ~90 lines.
  Ch12 Definition of done 2940    45   KEEP (ADR-81/108 operational surface).
  Ch13 Continuous Impr.  2985    221   SHRINK. Largest non-Ch8 reference block with no gate reading it.
                                       ~80 lines.
  Ch14 CC internals      3206    313   SHRINK-heaviest. Holds H10 H11 H12 H14 H15 H16 H17. Its command
                                       table (:3237-3245) restates a generated roster; its hooks half
                                       already pointerises to CLAUDE.md §9 -- apply the same to the
                                       commands half. CAUTION: :3700 is the S17 seam read by the
                                       `provider-registry-agreement` pre-commit gate via
                                       _PROSE_TIER_RE (scripts/check_provider_registry.py:105);
                                       rewording that sentence fails the gate LOUD. ~110 lines.
  Part II  §1-§21        3519   1496   Recipes. Net verdict SHRINK, per-recipe:
      §2 Prompt recipe   3596    256   KEEP (functional, human-facing).
      §5 AI Council      3932    299   MOVE -> protocols/AI_COUNCIL_PROCESS.md (exists; canonical there).
                                       Largest single recoverable block outside Ch8. ~270 lines.
      §8 Handoffs        4293    194   SHRINK -> pointer to HANDOFF_PROCESS.md, which :4296 already
                                       calls "the single live source of truth ... must not duplicate".
                                       This is the H13 epicentre (:4296 :4302 :4461 :4468). ~150 lines.
      §10 BACKLOG groom  4503     90   KEEP-FIXTURE. Carries rule tokens :4510 :4521 :4540.
      §16/§17 review     4786     89   KEEP. §16 holds H18 (:4799).
      §1 §3 §4 §6 §7 §9 §11-§15 §19-§21 + 10 Commandments  ~570  KEEP (each <90 lines, all functional).
  Appendix A shortcuts   5015     65   DELETE-candidate. Platform-volatile, ungated, restates CLI help.
  Appendix B routing     5080     18   MOVE -> ~/.claude/ROUTING.md is L0-canonical (ruled 2026-08-22,
                                       ARCHITECTURE Ch3). Leave the pointer only.
  Appendix C tokens      5098     29   KEEP.
  Codemap workflow       5127     71   SHRINK -> pointer (runbook duplicated in the tool's --help).
  Auto-TOC addendum      5198     10   KEEP.

  Recoverable without touching Ch5/Ch8 or any gate fixture: ~955 lines (~18% of the file).

1b. THE 19 CENSUS FINDINGS -> DISPOSITION (live line, act)
  H1  :2684  "41-member ALL_CHECKS".  Live = 46 (scripts/audit.py:3537-3595, last check_funnel_coverage).
             CENSUS ITSELF STALE: it says 43. Act: DELETE the integer, cite ecosystem/doc-counts.md
             (which already reads "46 registered checks"). M2, not a re-count.
  H2  :1869  "all five hold" vs .claude/commands/lane-integrate.md:53 "Run all six". Act: CORRECT
             in place + replace the enumeration with a pointer to the command. Inside Ch8 -> correction
             only, no structural edit.
  H3  :3520  "recipes (§1-§19)". Header :12 already says §1-§21. HALF-FIXED since the census; one site
             left. Act: CORRECT.
  H4  :1056  "10-section template" vs :339 "12 sections". Act: DELETE the count (M2).
  H5  :8     "Last updated: 2026-08-01"; file edited 2026-08-26 (d7ce675). Now 25 days stale. Nothing
             gates it: PLAYBOOK is deliberately absent from _FRESHNESS_FILES (tests/test_audit.py:1025).
             Act: DELETE the hand-stamp, point at git. (Adding PLAYBOOK to the gate is [#285], not this.)
  H6  :303   cites ARCHITECTURE.md:106 -- live :106 is a last_reviewed blockquote. The census's own
             replacement (:193) HAS ALSO ROTTED -- live arrow is ARCHITECTURE.md:258.
             Act: convert to a heading-anchor citation, no line number. (This is the M1 failure class
             repeating at the auditor's level; worth one sentence in the commit body.)
  H7  :890   pyproject.toml L83-91 -> live L93-103.   } All five: same act -- Ch7's citation ruling
  H8  :942   gen_intake_index.py:44 -> DEFECT FIXED.  } (:1229) says a line number is a dated
  H9  :1216  gen_audit_index.py:57  -> DEFECT FIXED.  } measurement, not an anchor. Re-anchor on
  H10 :3168  test_enforcement_coverage.py:389 -> :386.} symbol/heading names. H8 and H9 additionally
  H11 :3682  HANDOFF_PROCESS.md:704 -> :786.          } TEACH A REPAIRED DEFECT AS LIVE -> rewrite the
  H12 :3682  self-locator ":3148" -> the §8 table.    } claim, do not just move the number.
  H13 11 live sites: TOC :185, :1066(v5.4), :1199, :3242, :3334, :4296, :4302, :4461, :4700, plus the
             process stamps :1758(v5.6) and :4468(v5.5). Frontmatter declares handoff-process@6.2.0.
             Act: NOT find-and-replace. Run the `check-against-spec` skill (dependent=PLAYBOOK.md,
             spec=HANDOFF_PROCESS.md, 5 -> 6.2.0) and verdict each site stale|historical individually.
             Historical and NOT to be touched: :1193-class "v4 superseded by v5", "pre-v5 frozen
             copies", "ADR-82 (v5 ratification)". Interacts with the §8 SHRINK -- do the re-stamp
             FIRST, then shrink, or the shrink silently discards the verdicts.
  H14 :3335  "/override ... the gate's only escape" -- RETIRED (ADR-85 amend. 2026-08-03 §A2;
             .claude/commands/override.md reads RETIRED). Act: CORRECT, one line. Highest value/cost
             ratio in the census -- it points a reader at a dead organ.
  H15 :3242 :3334  subset of H13; falls out of the same re-stamp.
  H16 :3237-3245  command table lists 7; .claude/generated/commands-repo.md carries 8.
             Act: SHRINK-to-pointer, mirroring what the hooks half of the same section already did.
  H17 :3695  "<!-- last-verified: 2026-07-06 -->" / CC 2.1.202, contradicted twice in-file at :2159
             and :2708 (2.1.224). Act: DELETE the pins, keep the re-ground instruction.
             DO NOT reword :3700 -- provider-registry-agreement gate seam.
  H18 :4799  "/code-review ultra (/ultrareview deprecated alias)". Live skill takes low|medium|high|
             xhigh|max. Act: CORRECT.
  H19a :610  "[TBD -- Stream C session 3, ADR-33]" mis-pointed (ADR-33 is VISION universalization) and
             hard-codes a live absolute secrets path into a governance doc. Act: DELETE the path,
             re-point or retire the TBD.
  H19b :617  "[TBD -- ADR-34]" -- ADR-34 (Accepted 2026-04-29) already answers it; sibling at :475
             pointerises correctly. Act: DELETE the TBD, replace with the pointer.
  Coverage: 19 of 19 dispositioned. 2 findings (H3, H8/H9 partially) have moved since the census;
  1 census replacement locator (H6) is itself now wrong.

=========================================================================================
2. ESSENTIALS DIET PLAN (185 lines; last_reviewed 2026-08-23; IN the freshness gate)
=========================================================================================
  How Claude thinks        :14   19  KEEP -- the only section with no canonical home elsewhere.
  Roles                    :33   13  KEEP.
  Architect disciplines    :46   14  KEEP.
  Governance frame         :60   11  SHRINK -> pointer to ARCHITECTURE Ch1/ADR-28.
  Starting a Session       :71    9  SHRINK -> pointer to CLAUDE.md §6 (which is itself Form-A).
  Parallel sessions        :80   12  SHRINK -> pointer to PLAYBOOK Ch8. Highest drift risk in the file:
                                     it summarises the surface that lane-h just rewrote tonight.
  Writing a Prompt         :92   11  KEEP.
  Conventions (homes)     :103   14  KEEP -- this is the routing table the file exists for.
  Managing Tokens         :117    7  KEEP.
  Ending a Session        :124   16  KEEP.
  Feedback Loop           :140   11  KEEP.
  Backlog (ADR-64/65/66)  :151    7  SHRINK -> pointer (tasks/ is source of truth since ADR-107 §7.2).
  Three Homes             :158   13  KEEP.
  Repo complexity         :171    7  KEEP.
  The 5 Rules             :178    7  KEEP.
  Net: ~30 lines recoverable (~16%). ESSENTIALS is ALREADY at diet weight -- the honest finding is
  that it is not the problem, and effort spent here buys ~3% of what Ch14+§5+§8 buy in PLAYBOOK.
  HARD CONSTRAINT: any edit here trips canonical_freshness A2 unless last_reviewed is bumped after a
  GENUINE end-to-end re-read (CLAUDE.md §4; 185 lines, so this is cheap -- but it is not optional).

=========================================================================================
3. ARCHITECTURE PROSE PLAN (per W2/D5, STANDING_RULINGS.md:2865-2876)
=========================================================================================
Generated half that STAYS untouched: CODEMAP region :227-238 (codemap-freshness gate).
Prose half, section by section -- "functional doc + pointer", never deletion:

  Purpose [CORE]                    :187   31  KEEP whole. Functional.
  Codemap [CORE]                    :218   24  KEEP (12 lines are the generated region).
  Layer Boundaries & Invariants     :242   52  KEEP whole. It is the canonical home three other files
                                               point INTO (PLAYBOOK :303, ESSENTIALS :60). Diet here
                                               would push restatement back outward.
  Authority and governance [CORE]   :294   26  KEEP.
  Organ map                         :320  143  SHRINK-to-pointer -- the flagship D5 case. Its own
                                               blockquote (:326-333) already licenses it: "may be
                                               replaced by a pointer to it ... when they disagree,
                                               trust the index". ecosystem/organ-index.md is generated
                                               and gated by organ-index-freshness. KEEP ONLY the
                                               failure-posture column, which :356+ states the index
                                               cannot carry. ~95 lines.
  Validators and enforcement [CORE] :463  267  SHRINK -- largest prose block in the file and the
                                               densest restatement layer. Keep the seam explanations
                                               (ship-gate vs health, :477-485) which nothing computes;
                                               pointerise the per-organ inventory to
                                               ecosystem/organ-index.md + ecosystem/doc-counts.md.
                                               Preserve the one <!-- rule: --> reference at :559.
                                               ~120 lines.
  Automation axes                   :730   87  KEEP + RECEIVE PLAYBOOK Ch11 (net grows ~10 lines).
  Distribution and transfer         :817   63  KEEP.
  Key conventions & zones           :880   86  SHRINK ~20 -> ADR pointers.
  Verification mesh & decision flow :966  138  SHRINK ~35 -- restates the nightly loop PLAYBOOK Ch11
                                               also carries; after the Ch11 move, one of the two must
                                               become the pointer. This one is the functional home.
  Governing ADRs                   :1104   56  KEEP -- but DELETE any restated status; cite
                                               .claude/generated/recent-adrs.md (M2).
  Net: ~270 prose lines to pointers (~23%), zero generated bytes touched.
  HARD CONSTRAINT: last_reviewed 2026-08-23 -> A2 gate. A 1160-line genuine re-read is a real cost and
  must be priced INTO the lane, not bolted on. Counts already live in ecosystem/doc-counts.md, so a
  count fix does not force the stamp (that decoupling is #222 and it holds).

=========================================================================================
4. EXECUTION SHAPE -- smallest lane sequence, no generated half touched
=========================================================================================
STEP 1 (S, mechanical, no heading changes -> no TOC regen)
  Edits: protocols/PLAYBOOK.md ONLY.
  Lands H1 H2 H3 H4 H5 H14 H17 H18 H19a H19b + the seven locator repairs H6-H12 as heading-anchor
  citations. Pure correction; no diet. Ships the whole census except H13/H15/H16.
  Why first: it is the half that mis-directs readers TODAY, and it is the half a later structural
  diet would otherwise silently discard.
  Gate exposure: none. PLAYBOOK is not freshness-gated; no headings move.
  DO NOT TOUCH :3700 (provider-registry-agreement S17 seam).

STEP 2 (M, spec arc)  -- must precede any §8/Ch6 shrink
  Edits: protocols/PLAYBOOK.md; possibly protocols/HANDOFF_PROCESS.md (verdict-dependent).
  Runs the check-against-spec skill for the H13 11-site v5 cluster + H15. Each site verdicted
  stale|historical|not-relevant in the re-stamp commit message, per the skill's contract.
  *** COLLISION FLAG -- lane-h landed 2026-08-25 21:56 (c5bf642) ***
    It touched protocols/HANDOFF_BOOT.md, templates/handoff/v5/HANDOFF_BOOT.md.tmpl,
    templates/prompt-template.md AND PLAYBOOK Ch8. Three consequences:
    (a) The template directory is literally named templates/handoff/v5/ while the spec is v6.2.0.
        A v5->v6 prose sweep that "helpfully" renames or repoints that path breaks the generator.
        The directory name is OUT OF SCOPE for this arc -- state it in the contract.
    (b) c5bf642 added a /handoff-verify DISPATCH probe (.claude/commands/handoff-verify.md:104) that
        greps PLAYBOOK Ch8 for the heading "The dispatch table -- the SOLE literal-command site"
        (live :2236). A missing heading is a FAIL ON ANY HOST. Ch8 is untouchable anyway; this makes
        it enforceable rather than merely instructed.
    (c) HANDOFF_PROCESS.md was edited three times in the last 48h (86d9903, 0d5d961, and c5bf642's
        sibling). Re-read the spec at lane HEAD, not from the census.

STEP 3 (M) -- ARCHITECTURE prose, per W2/D5
  Edits: ARCHITECTURE.md ONLY (Organ map, Validators, Key conventions, Verification mesh, Governing
  ADRs). CODEMAP region untouched. Ends with a genuine end-to-end re-read and a last_reviewed bump.
  Gate exposure: canonical_freshness A2 (blocking), codemap-freshness (passes if the region is
  untouched), validate_doc_claims anchors.

STEP 4 (S) -- the two human-facing diets
  Edits: protocols/PLAYBOOK.md (Ch2, Ch3, Ch6 table, Ch11 move-out, Ch13, Ch14, §5 move-out, §8,
  Appendix A/B, Codemap addendum) + protocols/ESSENTIALS.md + protocols/AI_COUNCIL_PROCESS.md
  (receives §5) + ARCHITECTURE.md (receives Ch11).
  This is the ONLY step that moves headings -> regen the TOC in the same commit
  (`toc-freshness-playbook`), and leave a `structure-allow` marker for any deleted §N rather than
  renumbering (validate_doc_structure heading-scheme scan; precedent marker at PLAYBOOK.md:14).
  Preserve all 14 <!-- rule: --> tokens (PLAYBOOK :285 :391 :626 :630 :1093 :1108 :1118 :1126 :1132
  :1140 :1675 :4510 :4521 :4540) -- a deleted paragraph carrying one breaks a doc_code_edge edge.
  ESSENTIALS half needs its own last_reviewed bump (A2).

  Steps 1 and 3 are independent and may run as parallel lanes (disjoint file sets).
  Steps 2 -> 4 are strictly serial on PLAYBOOK.md. Do not put Step 1 and Step 4 in one lane: one is
  line-local, the other moves headings, and a conflicted merge on a 5208-line file is the expensive
  failure this sequencing exists to avoid.
  Nothing in any step touches CLAUDE.md, templates/claude-regions/*, .claude/generated/*,
  ecosystem/organ-index.md, ecosystem/doc-counts.md, or the CODEMAP region.

=========================================================================================
5. PROPOSED ROWS -- CANDIDATE only, not filed (ADR-111: CANDIDATE -> intake -> ratification)
=========================================================================================
R1 · PLAYBOOK census discharge, mechanical half  [S]
     Done when: H1 H2 H3 H4 H5 H14 H17 H18 H19a H19b are corrected and H6-H12 are re-anchored as
     heading/symbol citations carrying no bare line numbers; the hard-coded secrets path at :610 is
     gone; `uv run --locked pytest -x --tb=short` green; :3700 byte-identical.

R2 · H13/H15 v5->v6 re-stamp via check-against-spec  [M]
     Done when: all 11 sites individually verdicted stale|historical in the re-stamp commit message,
     PLAYBOOK's reconciled_with stamp re-earned rather than merely current, and the
     templates/handoff/v5/ path explicitly recorded as out of scope.

R3 · ARCHITECTURE prose -> functional doc + pointer (D5)  [M]
     Done when: Organ map keeps only the failure-posture column and points at ecosystem/organ-index.md;
     the Validators inventory points at the index + doc-counts; no count or roster is restated in prose;
     CODEMAP region byte-identical; last_reviewed bumped after a genuine end-to-end re-read.

R4 · The human-facing diet: PLAYBOOK Ch11/§5 relocation + ESSENTIALS pointerisation (R-F2)  [M]
     Done when: Ch11 lives in ARCHITECTURE Ch3 and §5 in AI_COUNCIL_PROCESS.md, each leaving a one-line
     pointer; ESSENTIALS' four pointerisable sections point; TOC regenerated in the same commit; all 14
     rule tokens still resolve under doc_code_edge; a structure-allow marker replaces every removed §N.

HONEST LIMITS OF THIS PLAN
  - Sizes are line counts, not tokens. A pointerised line is cheaper than a prose line by more than 1:1,
    so the ~955 / ~30 / ~270 figures understate the real saving and are not a token budget.
  - KEEP/SHRINK verdicts are this session's judgment against R-F2 and W2/D5. They are not a ruling.
  - No lane was run and nothing was verified by execution: every gate interaction above is read off the
    hook config, the script source, and the command files -- not observed firing.
```

**Three things worth pulling out of the report:**

1. **The census has itself rotted in six days.** H1's "live value 43" is now 46 (`scripts/audit.py:3537-3595`), H3 is half-fixed, and the census's *replacement* locator for H6 (`ARCHITECTURE.md:193`) is wrong — the live arrow is `ARCHITECTURE.md:258`. That is the M1 failure class recurring at the auditor's level, exactly as `CLAUDE.md` §4 records.

2. **Ch8 is now enforceably untouchable, not just instructed.** Tonight's lane-h commit `c5bf642` added a `/handoff-verify` DISPATCH probe that greps Ch8 for its dispatch-table heading (live `:2236`) and FAILs on any host if it's missing. The brief's constraint and the repo's gate now agree.

3. **The cheapest real win is not in ESSENTIALS.** ESSENTIALS is already at diet weight (~30 recoverable lines of 185). Ch8 alone is 1541 lines — 29.6% of PLAYBOOK — and is off-limits, so the recoverable mass concentrates in Ch14 (313), §5 (299), Ch13 (221), §8 (194) and ARCHITECTURE's Organ map + Validators (410 together).