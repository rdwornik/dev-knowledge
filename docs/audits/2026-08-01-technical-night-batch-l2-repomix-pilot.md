# Night batch 2026-08-01 — L2: repomix pilot measurement (intake #22 §D)

**Status: PROPOSAL — measured input for a morning adopt-or-reject. Nothing adopted, nothing filed.**

**Done-contract: MET.** Every number below was measured this session against OUR corpus; none is
quoted from repomix's README or docs. The morning arc can adopt-or-reject without further research.

**Environment:** repomix **1.17.0** (fresh `npm i -g repomix`), node v22.22.2. All output written to
a scratchpad outside the repo; `git status --porcelain` empty at lane close (verified).

**Prior context trusted, not re-derived:** `docs/audits/2026-07-31-technical-intake22-d-research-rows.md:53-134`
(the grep-first leg: zero rows, zero manifest entries, zero consumption path). **Anchors re-verified
live:** `scripts/assemble_paste.py:32` `_SIZE_WARN_BYTES = 65_000` and `scripts/assemble_paste.py:44`
`HANDOFF_BOOT_BYTE_BUDGET = 18_000` — both current.

---

## Headline

**The load-bearing open question from the 2026-07-31 pass is now CLOSED, empirically:
markdown is not a supported Tree-sitter compression target in repomix 1.17.0.** `--compress` passes
unsupported file types through **byte-identical** and adds a fixed ~37-token banner — so on a
markdown-majority corpus it makes output **larger**, never smaller.

That single fact decides §D's stated consumer. §D proposed repomix as a distiller for *"the §B(b)
boot bundle itself (distillate instead of raw files)"*. On measurement, there is no distillate.

---

## (a) Raw vs `--compress` on our corpus

| target | raw tokens | compressed tokens | delta | delta % |
|---|---|---|---|---|
| whole repo (1,760 files) | 6,061,878 | 5,773,137 | −288,741 | **−4.76%** |
| `docs/handoffs/2026-08-01-…/` (bundle) | 23,918 | 23,955 | +37 | **+0.155% (LARGER)** |
| `scripts/` (67 files — CODE control) | 269,661 | 173,865 | −95,796 | **−35.52%** |
| `protocols/` (13 files — markdown) | 146,323 | 146,360 | +37 | **+0.025% (LARGER)** |

Commands were of the form `repomix <target> [--compress] [--token-count-tree N] -o <scratchpad path>`,
run against the repo root, the bundle dir, `scripts/`, and `protocols/`.

### The markdown-vs-code A/B, at maximum granularity

`--token-count-tree` with threshold 1:

- **`protocols/`: 13 of 13 files identical, token-for-token.** PLAYBOOK.md 77,609 = 77,609;
  HANDOFF_PROCESS.md 19,338 = 19,338; HANDOFF_BOOT.md 4,178 = 4,178. Zero exceptions.
- **`scripts/`: every `.py` file compresses** — `audit.py` 47,449 → 31,666 (−33.3%),
  `fleet_parity.py` 23,750 → 10,103 (−57.4%). The two `.ps1` files do **not** (1,522 = 1,522;
  1,402 = 1,402) — no Tree-sitter grammar for PowerShell, **the same signature as markdown**.

### Direct proof it is a true no-op, not merely near-zero

Diffing the raw vs compressed packs of the all-markdown bundle directory: the **entire diff is two
inserted banner lines** ("The content has been processed where content has been compressed…").
Every content byte is unchanged. Grepping the compressed output for repomix's own Tree-sitter
elision delimiter `⋮` returns exactly **2** hits — both inside that banner sentence, describing the
feature rather than using it. Zero compression activity on any file.

The whole-repo −4.76% is therefore **entirely attributable to the Python content**, not to a broad
corpus effect.

---

## (b) The [#449] assembled-paste scenario, reconstructed

`scripts/assemble_paste.py` (read in full, lines 1–222) concatenates, in order: (0) the bundle
session-header; (1) `protocols/HANDOFF_BOOT.md`; (2) bundle `RESIDUAL.md`; (3) bundle `PROBES.md`;
(4) bundle `SUPPLEMENT.md` **ANSWERS region only** (lines 104–121, divider-stripped) — joined with
`=== label ===` headers and a terminal `=== END OF PASTE ===` sentinel.

Live artifact: `PASTE_THIS.md` = **52,119 bytes** = **80.18% of the 65,000-byte budget**; 13,343 tokens.

| mode | bytes | Δ vs raw | % of 65,000-B budget |
|---|---|---|---|
| raw (on disk) | 52,119 | — | **80.18%** |
| `--compress` (default xml wrap) | 54,217 | +2,098 | 83.41% (WORSE) |
| best case: `--style markdown`, no-file-summary/tree | 52,167 | +48 | 80.26% (wash) |
| same + `--compress` | 52,167 | +48 | 80.26% (**byte-identical** to no-compress — true no-op) |
| selective `--include` reassembly of 4 raw sources | 56,722 | +4,603 | 87.27% (WORSE) |

**Every tested mode is at or above the raw byte count.** `--compress` in normal invocation makes the
live paste *worse* against budget than doing nothing.

Selective reassembly is worse still for a structural reason worth recording: **repomix can only
include or exclude whole files.** It has no concept of "fold only the filled ANSWERS region," so it
carries ~1 KB of `SUPPLEMENT.md` QUESTIONS boilerplate that the real assembler already strips for
free.

This is the negative result the lane brief anticipated as full credit. There is no favourable
framing available, and none is offered.

---

## (c) The anti-bluff invariants — distil AROUND, never THROUGH

**Enumeration method:** full read of the bundle's `PROBES.md`, `RESIDUAL.md`, `HANDOFF_BOOT.md`,
`SUPPLEMENT.md`, plus `protocols/HANDOFF_PROCESS.md` (all 1,020 lines), `protocols/HANDOFF_BOOT.md`,
and `scripts/verify_handoff_probes.py` (547 lines). **24 invariants enumerated.**

### Pass 1 — structural, via the repo's own parser

`verify_handoff_probes.parse_probes()` was imported read-only and run against text extracted from two
distilled candidates: **b2** (`--compress` pack of the live `PASTE_THIS.md`) and **b6** (selective
repomix reassembly of the 4 raw source files).

```
BASELINE (raw PROBES.md):  14 rows — P0a P0b P0c P1a P1b P2 P3 P4 P5 P6 P7 P8 P9 P10
b2 (--compress pack):      14 rows — IDENTICAL ID set.  MATCH
b6 (selective assembly):   14 rows — IDENTICAL ID set.  MATCH
Sanity (real verify() on the live bundle): 14 probes — 14 pass, 0 fail, 0 warn/skip
```

Using the repo's own parser matters: a probe the validator parses has a **machine-checkable** shape,
so survival is testable rather than a judgment call.

### Pass 2 — literal-marker sweep, all 24 invariants

**21/24 directly PRESENT in both b2 and b6** — the core withholding contract, the four-tag
discipline (`witnessed`/`recall`/`inferred`/`unknown`), the FILL-IN markers, the P7 headline, the
escalation-ladder language, the `END OF PASTE` sentinel, the exact command chains. None ALTERED.

**3/24 reclassified after checking ground truth — none is a real loss:**
- 2 are enforcement mechanisms that **never travel in the paste by design** (the "toothless" rule
  lives only in `scripts/verify_handoff_probes.py`; "never the answer" lives only in the unpasted
  `HANDOFF_PROCESS.md` spec). Both verified structurally via pass 1 instead.
- 1 (the `PASTE CHAT ANSWERS BELOW THIS LINE` divider) is **correctly absent** from b2, because the
  real `PASTE_THIS.md` never carries it either — the assembler strips it. It is **present in b6**,
  because repomix packed the whole raw `SUPPLEMENT.md` and cannot slice ANSWERS-only.

### **Net: 0 LOST, 0 ALTERED.**

### The one real finding inside the clean pass

That b2/b6 divergence on the divider is not a wash — it proves **the two distillation strategies are
not equivalent**. Re-packing the *already-assembled* `PASTE_THIS.md` preserves the assembler's
semantic fold perfectly (repomix never mutates content handed to it); re-*assembling* from raw source
files via `--include` cannot reproduce that fold.

> **Design consequence:** any repomix-based pilot must distil the assembled `PASTE_THIS.md`
> **post-fold**, never the raw bundle member files pre-fold.

### Why the clean pass must not be over-read

**The 0-LOST result is a direct consequence of finding (a).** `--compress` performs zero content
mutation on markdown, so invariant survival here is *not* evidence of markdown-safe distillation — it
is evidence that repomix currently offers **no markdown distillation lever to test against**. No
conclusion is drawn about a hypothetical future markdown-aware compressor; that stays open by absence
of a testable mechanism, not by a passed test.

---

## (d) `--token-budget` CI mode and `--mcp` server mode

### `--token-budget` — determined empirically, both directions

Tested on `protocols/` (146,323 tokens):
- **Under budget (1,000):** exit **1**, stderr `✖ Packed output exceeds the token budget: 146,323 > 1,000 tokens. Reduce with --compress, narrow with --include/--ignore, or raise --token-budget.`
- **Over-allowance (500,000):** exit **0**.
- **No truncation.** `diff` of the exceeded-budget output against the unbudgeted raw pack shows
  **byte-identical files** (591,246 B both).

So it is a **pure post-hoc pass/fail gate, never a fitting mechanism** — it suggests remedies but
applies none. Useful as a deterministic CI exit code; it does zero work toward getting under budget.

**No MCP equivalent** — all 8 installed MCP tool schemas grepped for `tokenBudget`: zero hits,
confirmed against a live JSON-RPC response.

### `--mcp` — verified via a real JSON-RPC handshake

Not merely read from source: `lib/mcp/mcpServer.js` was read from the installed package, then a live
`initialize` + `tools/list` request pair was piped over stdin and real responses captured.

- **Transport: stdio only.**
- **8 tools confirmed live:** `pack_codebase` (params include `compress`, `includePatterns`,
  `outputPatterns` for per-glob compress override), `pack_remote_repository`, `generate_skill`,
  `attach_packed_output`, `read_repomix_output`, `grep_repomix_output`, `file_system_read_file`,
  `file_system_read_directory`, plus 1 prompt.
- Worth noting, `pack_codebase`'s own description says: *"Generally not needed since
  grep_repomix_output allows incremental content retrieval."*

### Dependency-surface cost — measured, and larger than it looks

- This repo's toolchain is uv-pinned Python (ADR-106). Repomix is Node/npm.
- **The repo's entire existing npm footprint is one dependency** — `package.json` declares only
  `pyright`, and its own description states *"This repo is NOT a node app."* Repomix would be the
  **second-ever** npm dependency.
- `ecosystem/dependency-baseline.yaml` — the #332/FR-7 parity manifest that `fleet_parity.py`
  enforces (read in full: 35 lines, one row) — is scoped **entirely to Python surfaces**. It has **no
  mechanism for tracking Node dependency drift at all.** Adopting repomix therefore lands outside the
  fleet parity gate, which is real follow-on work, not a footnote.
- `--mcp` additionally means a long-lived stdio child process, which has no current home under this
  repo's Layer-2-never-executes doctrine (Critical Rule #4).

---

## Drafted pilot design

**What:** repomix `--compress`, **CLI-only** (not `--mcp`), applied to **code** context for an
external-reviewer lane (`codex exec` on a diff/PR).

**Surface:** code trees only (`scripts/` / `deploy/`, or a target repo's equivalent).
**Explicitly excluded:** all markdown / handoff / paste surfaces. §D's originally-named consumer is
the one this session rejected most clearly, and it must not be quietly re-included under a broader
framing later.

**Success metric:** across N ≥ 3 real invocations, `--compress` reduces packed tokens by **≥ 25%**
(a conservative floor under this session's measured 35.5% aggregate / 57.4% peak) **and** reviewer
finding-recall on a seeded-defect sample is not measurably lower than an uncompressed control.

**Falsification bar:** average savings < 15%, **or** any single finding-recall regression in the
N ≥ 3 sample → decline for this surface too.

**Cost:** second-ever npm dependency, outside the existing Python-only parity gate;
`npm i -g repomix` ≈ 170 packages / ~11 s; CLI-only avoids the MCP process-lifecycle question;
`--token-budget` gives a deterministic CI exit code but performs no fitting.

**What must NOT be piloted:** repomix as a handoff/paste distiller. 0 of 13 `protocols/` files and
0 of 5 bundle files showed any reduction; the live paste comes out larger under every mode tested.

---

## RECOMMENDATION

**REJECT** for §D's stated target (handoff / `PASTE_THIS.md` distillation)
· **ADOPT-NARROWED** only if rescoped to CLI-only code-context packing for review lanes, per the
pilot design above.

**Driving number: 0%.** Zero of 13 `protocols/` files and zero of 5 handoff-bundle files showed any
`--compress` token reduction — against a real 35.5% on `scripts/` code — and the live
`PASTE_THIS.md`'s best achievable repomix re-render (52,167 B) is **larger** than its 52,119-B raw
original.

**Consequence for [#449]:** the assembled-paste byte budget is not addressable by this tool. The
paste sits at 80.18% of budget and repomix cannot move it down. If [#449] needs headroom, the lever
is selective assembly inside `assemble_paste.py` — which the repo already owns and which already
does the one thing repomix structurally cannot (fold a *region* of a file, not a whole file).
