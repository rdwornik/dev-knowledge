# Archives & Lifecycle Records — Status Legibility Without Moving Files

Night-audit cycle-close · Stream S3 · ADR-101 class `technical`; read-only

## 1. Current mechanism (witnessed, file:line)

**Intake index.** `scripts/gen_intake_index.py` parses each doc's frontmatter `status:`
(`_parse_frontmatter` L44-62, read at L86-89), buckets it into the canon
`_STATUS_ORDER = ("SEED", "DRAFT", "READY-FOR-TECHNICAL", "CONSUMED", "REJECTED")` (L37) or
else `_OTHER` (L38, applied at L96), and renders a grouped Contents block (`render_contents`
L104-119) spliced into `docs/intake/README.md` between `<!-- INTAKE-INDEX:START/END -->`
markers (README L16-49). Cross-checking the generated block against the actual frontmatter
of all 17 `docs/intake/*.md` files: 6 carry off-enum status strings — `input-for-deferred-work`
(#10), `superseded-pending` (#11), `settled` (#12, lowercase), `plan-of-record-active` (#13),
`RULED` (#14 pack), `READY-TO-FIRE` (#15) — and every one of them correctly lands in the
generated `### OTHER (6)` group (README L41-48), none silently dropped. The generator is
mechanically faithful. Separately, three physical files share `intake-id: 14`
(`2026-07-12-siem-requirements-ruled-pack.md` status RULED, `2026-07-13-siem-fleet-management-
requirements.md` status DRAFT, `-codex.md` status DRAFT) — README §3 (L98-109) calls
`intake-id` "the join key" and "permanent once assigned", §1 (L55-56) says "0..1 intake doc per
initiative", yet `_group()` (L93-101) sorts same-id rows without flagging the collision.

**ADR-88/89 header vs README index.** `docs/decisions/ADR-88-file-oriented-dependency-
management.md` L5 and `docs/decisions/ADR-89-computed-code-dependency-edges.md` L5 both read
`**Status:** Proposed` — frozen, per each file's own appended amendment marker (ADR-88
L167-177, ADR-89 L306-316: "Status (in-place marker; the frozen header above is unchanged per
the immutability convention): Proposed → Accepted."). `docs/decisions/README.md`'s ADR Index
table (`| ADR | Date | Title |`, L12-13) carries **no Status column**. ADR-88's row (L75)
happens to embed "Accepted 2026-06-21 (`911b561`, in-place marker)" in prose; ADR-89's row
(L76) contains **no status word anywhere**. A grep for `**Proposed**` over the whole README
returns zero matches — the "absent prefix ⇒ implicitly Accepted" reading is an unwritten
convention, not a machine-checkable one. `BACKLOG.md` L35 (`[#242]`) is unmarked-open: "Build a
read-only audit leg that flags an ADR whose header status diverges from its README-index
effective status ... Done when: a seeded ADR with a header↔README status divergence is flagged
by an audit check, with tests" — matching ADR-94 L36's own admission: "Enforcement is filed,
not built... tracked as #242."

**Audit index.** `scripts/gen_audit_index.py`'s `collect_audits()` (L45-62) parses only
date/slug/filename/title — no status field exists in the schema. The live
`docs/audits/README.md` (L1-10) shows "246 audit documents" grouped by `## YYYY-MM` month
headers only (L13+), zero lifecycle-state grouping. `ADR-100` (Accepted 2026-07-07) §2
"Count-tiered index" (L29-36) *designed* a fresh-section (~20 most recent) / archive-section
split — "everything older moves to an archive **section of the index** ... files never move" —
but it is unbuilt: grepping the live index for "count-tier"/"archive section"/"fresh section"
returns zero true hits, and `BACKLOG.md` L150 (`[#269]`) is open, explicitly deferring exactly
this shape. 15+ individual audit files use the word "supersede(d)" in their own prose (grep,
files list omitted for brevity) but none of that is surfaced by the index — it is read-the-file
knowledge only.

**Handoffs.** `docs/handoffs/README.md` is hand-authored, not generated. Its only
status-adjacent section is "Format eras & navigation" (L189-201), which operates at the
FORMAT-ERA granularity (v5 / v4 / v3.2 / pre-v3.2), never per-bundle. To find "the current
session" the doc instructs the operator to run `Get-ChildItem docs/handoffs/ | Sort-Object Name
| Select-Object -Last 5` (L205-207) — there is no generated index and no status field for
individual bundles. `docs/handoffs/archive/` (the non-`legacy/` top level) holds 14 dated dirs
(`2026-05-09` → `2026-05-25`), each containing exactly `stage1-question.md` +
`stage2-response.md` — a file-pair format the README's "Format eras" section never names (it
lists only v5/v4/v3.2/legacy). These `archive/<date-slug>/` dirs share **identical names** with
top-level `docs/handoffs/<date-slug>/` dirs holding **different content** — witnessed:
`docs/handoffs/2026-05-09-ai-council-audit-sync/` contains the v3.2 twelve-file bundle
(`00_first-message.md` … `09_EXECUTION_EVIDENCE.md`); `diff` against the archive path's
`stage1-question.md` fails with "No such file" at the top-level path, confirming the two are
genuinely different artifacts, not a copy. Nothing at either path says "this archived
stage1/stage2 pair predates / was superseded by the full bundle at the same-looking path."

## 2. Designed/intended shape (cite)

- `docs/intake/README.md` §5 Lifecycle (L135-153): canonical enum
  `SEED → DRAFT → READY-FOR-TECHNICAL → CONSUMED/REJECTED`, sourced from ADR-98 §5. No section
  of the doctrine documents or sanctions the growing OTHER-bucket vocabulary
  (RULED/settled/plan-of-record-active/superseded-pending/input-for-deferred-work/READY-TO-FIRE)
  as first-class — that sanctioning currently lives only inside individual docs' own `note:`
  fields (e.g. intake #15's note explicitly self-justifies against "existing custom-status
  intake docs").
- `gen_intake_index.py` L35-36 (comment): "A status outside this canon is NOT dropped -- it
  lands in a loud trailing 'OTHER' group so a typo/new-state surfaces instead of vanishing." —
  this is the designed backstop, and §1 confirms it works. The gap is one level up: nothing
  reviews or reconciles the OTHER bucket back into the README §5 enum.
- `ADR-94` (Accepted 2026-07-03) Decision (L19-29) + Consequences (L36): standardizes
  go-forward ratification on Pattern B (in-place Status-line edit), explicitly defers ADR-88/89
  retro-normalization ("out of scope here ... This ADR governs go-forward"), and explicitly
  names the missing enforcement as `#242`, "a named deferral, not a silent gap" (per ADR-81(d)).
- `ADR-100` §2 (L29-36) + §6 (L49-51): designs the count-tiered audit index and a currency
  freshness hook, explicitly sequencing both as "not built here — filed as #269."
- `docs/handoffs/README.md` §"Format eras" (L189-201) is the closest designed per-artifact
  surface, but it is explicitly ERA-level, not per-bundle status/supersession. No ADR proposes a
  per-bundle "superseded-by" field for handoffs.

## 3. Gap

1. **ADR-88/89 header↔index divergence — ruled, filed, unbuilt (#242).** ADR-94 names the
   exact defect and the exact fix, and files it; BACKLOG confirms #242 is still open. A reader
   who trusts only the ADR-88/89 headers reads "Proposed"; a reader who trusts the README index's
   absent-prefix convention reads "Accepted"; for ADR-89 specifically the README row asserts
   *neither* word, so both readings require chasing the in-file Amendment marker to resolve at
   all. No machine reconciles this.

2. **Intake enum drift — mechanically safe, doctrinally silent.** The OTHER-bucket design
   prevents silent loss (confirmed: all 6 off-enum docs surface, none vanish) — this is the one
   part of the S3 question that is *not* a legibility failure. But 6 of 17 live intake docs
   (35%) use a status vocabulary the README §5 doctrine never enumerates, and nothing flags the
   drift-rate or triggers a reconciliation — OTHER is a permanent junk drawer, not a review
   trigger. Separately, the `intake-id` join-key has a live counterexample (three files sharing
   id 14) that the generator does not flag despite the README asserting the id is a unique
   permanent join key.

3. **No supersession/status surface for audits or handoffs.** `docs/audits/README.md`
   structurally cannot say "superseded" — its generator only ever parses date/slug/title — even
   though ADR-100 itself designed a fresh/archive index-section split that would partially
   address recency-legibility; that shape is unbuilt (#269 open). `docs/handoffs/README.md` has
   no per-bundle status field at all (only format-era grouping) and offloads "find current" to a
   manual `Get-ChildItem`. Worse: `docs/handoffs/archive/` contains an undocumented stage1/stage2
   artifact class that name-collides with unrelated top-level v3.2 bundles, and the README's own
   "Format eras" section doesn't mention this class exists — a reader has no way to know these
   are two different things at the same-looking path.

**Net answer to the stream question:** the "stay-in-place" convention (ADR-29 / ADR-101 /
immutability) is followed correctly at the file level everywhere witnessed here — no evidence of
an actual illegal move. But legibility is not free from stay-in-place; it requires a surfacing
mechanism, and of the three that exist, two are index-only (position/grouping — intake, audits),
not status-aware in the supersession sense, and the third (handoffs) barely exists as a
mechanism at all for individual bundles.

## 4. Proposed MECHANISM (name the enforcement site)

1. **`adr_status_coherence` audit check** (closes #242 exactly as specified) — new check in
   `scripts/audit.py`: for every `docs/decisions/ADR-*.md`, extract the header `**Status:**`
   value and the matching `docs/decisions/README.md` index row (`| ADR-NN |`); FAIL if the row's
   title text asserts a status word contradicting the header; WARN if the header says "Proposed"
   with an in-file "## Amendment ... Accepted" marker present but the README row asserts neither
   word (the ADR-89 ambiguous-by-omission case). Enforcement site: `scripts/audit.py` (new check
   function, registered in the check roster, `ecosystem/doc-counts.md` count bump). Read-only,
   Layer-2-safe.

2. **Intake off-enum drift WARN + duplicate-id WARN** — extend `gen_intake_index.py --check`
   (or a sibling `audit.py` check) to report "N docs off-canonical-enum (OTHER group)" as a WARN
   past a threshold (mirroring the `doc_rot` threshold pattern), so a reconciliation ("promote
   RULED/settled into README §5, or explicitly sanction them as terminal states") is
   number-triggered rather than accidental. Separately, add a same-`intake-id`-duplicate WARN to
   `collect_intakes()`/`_group()` — catches the #14 case mechanically instead of relying on a
   human reading three `note:` fields.

3. **Audit-index count-tiered shape** — build `#269` as ADR-100 §2 already designed:
   `gen_audit_index.py` gains a fresh-section (~20 most recent, flat as now) + an `## Archive`
   index-section for everything older (files never move — only the rendered grouping changes).
   Not a "superseded-by" field (ADR-100 didn't design one — audits are keep-all evidence, not
   supersedable), but it closes the one legibility gap ADR-100 already ruled on and left open.

4. **Handoff-archive self-description** — smallest fix, doctrine-only, no new script: add one
   clause to `docs/handoffs/README.md` §"Format eras & navigation" documenting the
   `archive/<date-slug>/stage1-question.md` + `stage2-response.md` pair as its own micro-era
   (name it, date-range it, one line reconciling the name collision with unrelated top-level
   v3.2 bundles).

## 5. BACKLOG seed (no id; kill-candidates: + Done when:)

- **ADR status-flip coherence check** — build `adr_status_coherence` per §4.1. This is
  `#242` verbatim, already filed — no new task needed, just build it. kill-candidates: none —
  #242 already covers this ask and remains the tracked item. Done when: a seeded ADR with a
  header↔README status divergence (or an ADR-89-shaped status-omitted row) is flagged by the
  audit check, with tests, per #242's existing acceptance line.

- **Intake enum-drift + duplicate-id WARN** — extend `gen_intake_index.py`/`audit.py` to (a)
  WARN when the OTHER-bucket share crosses a threshold and (b) WARN on any `intake-id` shared by
  more than one file. kill-candidates: none — no existing task covers the OTHER-bucket
  drift-rate or the same-id duplicate check; #307 (shipped) built the index itself, not this
  drift signal. Done when: a seeded off-enum-heavy intake set trips the drift WARN, and a
  seeded duplicate `intake-id` trips the duplicate WARN, each with a test.

- **Handoffs archive micro-era documentation** — one-clause doctrine edit to
  `docs/handoffs/README.md` §"Format eras & navigation" naming the undocumented
  `archive/<date-slug>/stage1-question.md` + `stage2-response.md` class. kill-candidates: none —
  no existing task names this specific undocumented class (distinct from #212/ADR-100, which
  settled retention *policy*, not per-era documentation completeness). Done when: the README's
  Format-eras section names the stage1/stage2 archive class, its date range, and one line
  reconciling the top-level name collision.

(`#269` — audit-index count-tiered shape — is not re-seeded here; it is already filed, ruled by
ADR-100, and open. This stream's evidence corroborates prioritizing it, not duplicating it.)
