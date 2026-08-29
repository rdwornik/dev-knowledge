---
id: "[#623]"
title: "Mechanize the JOURNAL anchor record-line — 719 anchored-by-mention WARNs is a signal-to-noise defect"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: none
generates: BACKLOG.md
---

- [#623] [P2][S] **Mechanize the JOURNAL anchor record-line — 719 anchored-by-mention WARNs is a signal-to-noise defect** — `journal_anchor` counts a SHA as PRESENT anywhere but as RECORDED only on a line matching `^\*{0,2}Anchors?` (`scripts/journal_anchor.py:554`, `_RECORD_LINE_RE`). Entries that name their SHAs in prose therefore satisfy the reader and not the checker, and the live corpus carries **719 `anchored by mention, not by record` WARNs**. **Operator ruling 2026-08-29: a WARN read past three times is a signal-to-noise defect, not an operator habit** — an advisory that fires 719 times trains the reader to skip the line where the real FAIL also prints. Measured live 2026-08-29: an integrator hit the anchor rule three distinct ways in one session (no entry; a single-commit branch that cannot name its own hash; and an entry that existed, sat in the right place, read correctly and named no SHA) — the third looks discharged while being empty, which is why it cost three round-trips. · Done when: the generator or a repair pass emits the `Anchors:` record line so a new entry cannot be authored without one, AND the 719 historical WARNs are either mechanically converted or the check's baseline is re-set with the residue named — a WARN count that never falls is a WARN nobody reads · refs scripts/journal_anchor.py, docs/audits/2026-08-29-verification-wave-2-close-packet.md, #153 · kill-candidates: none — no open row owns the anchor record-line format; `[#153]` owns the FF-push prevent leg, a different organ · serialize-group: none
