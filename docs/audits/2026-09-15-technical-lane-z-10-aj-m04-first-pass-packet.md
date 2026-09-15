# Lane z-10 — AJ M04 first pass: end-of-lane packet

Consumers: `[#765]` (the row this lane implements), `[#764]` (batch Z's night-plan row)

> **Row id correction, stated once and up front.** This lane filed its row as `[#763]` in
> commit `faef0e76` and **renumbered it to `[#765]`** when the sync merge revealed that a
> concurrent session had landed a different `[#763]` on `main` (commit `6572c1b1`, the batch-Z
> suite-baseline freeze) minutes earlier. `faef0e76`'s commit message therefore names `[#763]`
> and is wrong about it; the message is history and is not rewritten. **The live id is `[#765]`
> everywhere else, including in this packet and in every row this lane files.** §4 records how
> the collision happened and why it was predicted in `faef0e76`'s own body.

> **Lane** `lane-z-10-aj-m04-first-pass` · branch `worktree-lane-z-10-aj-m04-first-pass` ·
> contract `LANE-z-10-aj-m04-first-pass.md` (frozen) · batch Z lane 10, LOCAL substrate ·
> model `opus`, mode `execute`, effort `high`.
>
> **Why LOCAL.** The M04 corpus sits on the operator's disk and in no repository. The night
> plan says so in its own header — *"premise corrected during planning: the M04 material lives
> on the operator's local disk, not in the repo, so that lane cannot run in the cloud"* — and
> `[#660]` records the identical constraint for the tools-and-evals table.

This packet is written across the lane's steps, not at the end: §1 lands at step 2, §2 at
step 3, §3 at step 4, and §4–§6 at step 5.

---

## 1 · The corpus, located (contract step 2)

**Directory:** `C:\Users\1028120\Documents\Priv\Architekt Jutra\`

This is the same directory the M03 night mission names as its input A
(`docs/audits/2026-09-10-technical-night-aj-m03/MISSION-PROMPT.md`, the `INPUTS · A` block),
so the location is not a new discovery — what is new is that the M04 files are in it.

**Everything the directory holds for M04, with the size and mtime it was read at**
(`ls -la`, 2026-09-15; every file written 2026-09-14, between 23:09 and 23:10):

```
AJ_M04_ebook.pdf                   13,289,558 B   2026-09-14 23:10
AJ_M04_transkrypcje.md.zip             29,993 B   2026-09-14 23:09
AJ_M04_wszystkie_transkrypcje.zip     581,269 B   2026-09-14 23:09
AJ_M04_wszystkie_mp3.zip          165,775,907 B   2026-09-14 23:10
AJ_M04L01_transkrypcja.pdf             74,694 B   2026-09-14 23:09
AJ_M04L02_transkrypcja.pdf            125,706 B   2026-09-14 23:09
AJ_M04L03_transkrypcja.pdf             89,104 B   2026-09-14 23:10
AJ_M04L04_transkrypcja.pdf             90,872 B   2026-09-14 23:10
AJ_M04L05_transkrypcja.pdf             96,276 B   2026-09-14 23:10
AJ_M04L06_transkrypcja.pdf             81,127 B   2026-09-14 23:10
AJ_M04L07_transkrypcja.pdf             60,777 B   2026-09-14 23:10
AJ_M04L01_prezentacja.pdf             951,847 B   2026-09-14 23:09
AJ_M04L02_prezentacja.pdf             854,825 B   2026-09-14 23:09
AJ_M04L03_prezentacja.pdf             809,620 B   2026-09-14 23:10
AJ_M04L04_prezentacja.pdf             756,919 B   2026-09-14 23:10
AJ_M04L05_prezentacja.pdf             756,616 B   2026-09-14 23:10
AJ_M04L01..L07.mp3                  (7 files)     2026-09-14 23:09-23:10
```

**Two asymmetries against M01–M03, stated because a reader will otherwise assume symmetry.**
M04 has **seven** lessons where M01–M03 had six (M02 also had a seventh transcript without a
deck). And **L06 and L07 ship no `_prezentacja.pdf`** — five decks for seven lessons. Both are
properties of the corpus, not gaps in this reading.

### 1.1 · The source of record for this lane, and why

**`AJ_M04_transkrypcje.md.zip` → `AJ_M04_transkrypcje.md`** — one markdown file, 80,092 B,
1,233 lines, holding all seven lessons.

```
AJ_M04_transkrypcje.md.zip   sha256 bff7649ca7c77741c1f6d079393d09539816f5dd58f390d1f9748391289e84ba
AJ_M04_transkrypcje.md       sha256 ebd8753f03bcd80cb3277841a03dbc7def5f929feb55f3e3e96771a8a9e55f06
AJ_M04_ebook.pdf             sha256 70b4f13aa901ad0f937d8e6b5462fd3edcc99c91429cb3464b8830dbb5aee1b3
```

Extracted to `$CLAUDE_JOB_DIR/tmp/m04/` — **outside the repository and outside the corpus
directory**, so this lane writes nothing into either. It unzipped clean, which is the M03
mission's own stated preference (*"prefer the `.md` if it unzips clean"*).

**This choice is the direct repair of the `[#696]` locator defect, for this module.** `[#696]`
records that M03's leg-1a locators are UNVERIFIED because *"the chosen source carries no page
numbers and no timestamps, so locators became line numbers in a split file the mission never
asked for"*. Here the locators are line numbers in **the vendor's own single file, shipped
whole in the vendor's own archive** — nothing was split, and the archive and the extracted file
are both hashed above. Anyone who unzips the same archive gets byte-identical content and
therefore identical line numbers. The locator is reproducible without this lane's scratch
directory surviving.

This lane does **not** thereby close `[#696]`: that row owns the M03 **re-run**, and M03 is not
in this lane's scope.

### 1.2 · The seven lessons and their line spans in the source of record

Line numbers are into `AJ_M04_transkrypcje.md` at the sha256 above. Every lesson names
`Instruktor Jakub Kubryński` on its third line.

```
L01  lines    1- 118   Wprowadzenie do MPC            (introduction to MCP)
L02  lines  119- 459   Komponenty MCP                 (MCP components)
L03  lines  460- 638   Autoryzacja                    (authorization)
L04  lines  639- 830   Production readiness
L05  lines  831-1025   Specyfikacja 2026-07-28        (the 2026-07-28 specification)
L06  lines 1026-1172   Jak działa MCP Server w praktyce (kod i flow)
L07  lines 1173-1233   Nieprzekazywanie tokenów: Introspection i Exchange w praktyce
```

**The module's subject is MCP — the Model Context Protocol — and that is a finding in itself,**
because it is not what the AJ corpus taught before. M01–M03 were read for *operator practices*
and *process spine*; intake #70's own problem statement frames the corpus as *"about how a
human runs an agent"*. M04 is a **technical protocol module**: transport, components,
authorization, production-readiness, a dated specification, and two implementation lessons.
What that does to the matrix's item boundary is §2's first question, not this section's.

**The corpus is in Polish.** Lesson titles above are given as they appear, with an English
gloss; claims quoted in §2 are quoted in Polish and glossed, so a verifier can grep the source
for the quoted string.

---
