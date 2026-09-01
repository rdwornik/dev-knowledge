# ATLAS-R1 — Atlas of the Governed Graph (SIDECAR to the landed HTML artifact)

- **Class:** technical · **Date:** 2026-09-01 · **Lane:** ATLAS-R1 (read-only census, zero rows filed)
- **Artifact:** `2026-09-01-technical-atlas-r1-layer-graph.html` — **same stem, landed VERBATIM**
- **Consumed by:** intake #66 (`docs/dashboard/` view) · `[#615]` (the `tests/`+`ecosystem/` layers owed)

---

## Why this file exists, and what it is NOT

**The `.html` beside it is the artifact. This `.md` is its twin, not its replacement.** Architect's
format ruling, 2026-09-01: a **generated view is not rewritten into markdown by hand** — that
would fork one fact into two surfaces with no gate holding them equal, which is the conformance
lesson this repo already paid for. So the view lands byte-identical and sha-verified, and this
sidecar carries the provenance, the integrity record and the consumer list **so the corpus stays
markdown-indexed and census/consumers cite a `.md`**.

## Provenance and integrity

```
source        C:\Users\1028120\.claude\jobs\1732b879\tmp\atlas.html   (EPHEMERAL — job-scoped)
bytes         34,295
sha256        03a67eedf3c50465900892a27068dbab7ce5ccfcd444e128dfa948c7c30af727
verified      hashed at source AND re-hashed after the copy into docs/audits/ — identical
published     https://claude.ai/code/artifact/dd03ecac-fe91-4e49-8571-d19debb9fac0
              PROVENANCE, NOT THE STORE. The tracked file here is the durable copy.
measured at   HEAD 16f91f69 · uv 0.11.19 · python 3.12.10 · rustworkx 0.18.1 · writes: none
```

## What it measured

```
nodes 1,783 · edges 11,515 · cross-layer 87.3% · build 4.69 s
aggregate cells 12 · governed files 37.7%
```

**The finding that makes a render possible at all:** 11,515 edges collapse into **12 aggregate
cells**. And the ratio is stable while the corpus is not — DM-3 measured 1,758 nodes / 11,309 edges
on 2026-08-31 with cross-layer at 87.3%; one day later the graph is 25 nodes and 206 edges larger
and **cross-layer reproduces to the decimal**.

## Reconcile-before-birth, which is the actual deliverable

Four incumbents cover parts of this ground and ATLAS is scoped to what none of them do — *"a fifth
surface re-answering a live question would be the defect."* `gen_dashboard.py` renders **status,
not structure**; `gen_trend_dashboard.py` renders **time series, no topology**; `gen_north_star.py`
renders **arcs, not files**. The gap is `file_purpose_graph.py`: it **already owns a real rustworkx
graph and has no view of the whole** — one node at a time, in text.

**It renders DM-3's design; it does not re-derive it.** Batch-E lane DM-3 landed a 279-line
amendment on intake #40 (merge `7b0cbf14`) specifying the layer function, the attribute schema and
the L0 edges. That amendment is `status: DRAFT` and binds nothing. Re-deriving it would have
produced a second copy of a fact that already has a home.

## Consumers, recorded at landing

- **intake #66 — the OBSERVABLE HARNESS**, `docs/dashboard/` view. This atlas is the worked
  example of what that view renders.
- **`[#615]`** — the `tests/` and `ecosystem/` layers the graph still owes. `[#615]` is also the
  row the *ledger* names as the enabling one for per-lane attribution; the same row, two reasons.
