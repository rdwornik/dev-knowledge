---
intake-id: 23
status: SEED
origin: operator, dictated 2026-07-31 in the outgoing browser-seat window and relayed with that seat's research pack; ingested verbatim at the 2026-08-01 filing batch
consumed-by:
---

**NOTE 2026-08-29 (FILE DISTILLATION — the OUTPUT half, and its evidence is MEASURED):** this
doc's P1 named repomix as the *input*-side distiller, and that half is **rejected on
measurement** (`[#467]`, closed 2026-08-01 — 0% on markdown, the live paste re-renders LARGER).
The **output** half — how many bytes the corpus makes a seat read before it can work — was never
carried by a row, and it now has a number rather than an argument. The trends dashboard
(`scripts/gen_trend_dashboard.py`, run at `77096131`, console summary recorded in
`docs/audits/2026-08-29-technical-nb2-n-packet.md` §0) reports
**`paste / boot bytes  WORSENING  +11232 bytes`** over a 12-sample window — **the only worsening
panel**, while open rows, banked ledger and backlog velocity all read IMPROVING. Its store is the
`protocols/HANDOFF_BOOT.md` blob size per revision, so the regression sits in the artifact every
session reads first. `[#467]`'s own closure names the re-entry route — *"Re-entry is a new filing
citing the pain"* — and this measurement is that pain. Carrier: **`[#617]`**, born 2026-08-29.
Two closed rows are **cited, not reopened**: `[#449]` ruled an accepted-with-reason HOLD on a hard
paste ceiling, `[#467]` rejected the tool. **`[#607]` is NOT the doc-diet row** — it is the
PLAYBOOK census's mechanical half, which ruling X7 orders BEFORE any structural diet; the diet's
structural half has no row at all today, and intake #57 is still READY.

# Operator design input — distillation and library-first

<!-- class: func (operator design input) · status: SEED — NOT ratified; ingest per the intake
convention. Non-citable until ingested; repo wins on conflict. -->
<!-- origin: operator, dictated 2026-07-31 in the outgoing browser-seat window -->

OPERATOR FUNCTIONAL INTAKE — context distillation + library adoption priorities (relayed via
the outgoing seat with its research pack).
FUNCTIONAL REQUIREMENT (operator's why, plain): "When Claude gets a big file, it does not
read everything and sometimes misunderstands. Distillation matters to me because dense,
compressed context is read better, not just cheaper. Library-first is doctrine: research
libraries BEFORE implementing anything from scratch."
EVIDENCE PACK (outgoing seat's online research, 2026-07-31): LLMLingua family (Microsoft,
EMNLP/ACL): up to 20x prompt compression with minimal loss; LongLLMLingua improves
long-context RAG performance by up to 21.4% at ~1/4 tokens — compression increases
key-information density and mitigates position-bias degradation. repomix: ~26k stars,
~255k npm downloads/month, tree-sitter compression ~70% claimed token reduction,
--token-budget CI flag, MCP server mode.
PRIORITIES: P1 repomix distiller pilot ([#449] paste budget + review-lane packing; anti-bluff
invariants are ours — distill around, never through). P2 copier re-open procedure for L3.5
propagation (read the recorded rejection first; re-open only if the reason does not survive).
P3 networkx STANDS for [#383] v1; rustworkx noted as swappable (3-100x, near-compatible API;
ADR-109 types edges as data). P4 minor: why-not-python-frontmatter hygiene line; typer/rich
when the CLI surface grows.
POST-INTAKE MEASUREMENT NOTE (night batch 2026-08-01, L2): repomix measured 0% compression on
markdown on this corpus; paste re-renders larger — P1's paste-budget half is rejected on
evidence; the code-context review-packing half (−35.5% on scripts/) remains a deferred trial.
