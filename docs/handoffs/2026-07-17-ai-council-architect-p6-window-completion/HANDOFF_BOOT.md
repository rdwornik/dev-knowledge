# Handoff boot — session header + paste-pointer (architect mode · P6 window completion)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-17-ai-council-architect-p6-window-completion` |
| **Chat title** | `[ai-council] Architect — P6 window completion — 2026-07-17-ai-council-architect-p6-window-completion · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working posture; the session's WORK is small **product BUILD** — the ADR-11 D2 parity pair) |
| **Target repo** | `ai-council` — this bundle lives in the hub .dev-knowledge (ADR-36/42: the hub is the sole handoff carrier; consumers hold no docs/handoffs/ surface). **Run every probe command IN the ai-council checkout.** (The cross-repo probe resolver reads the first backtick span of this row as the target root — it must be `ai-council`.) |
| **Purpose** | **P6 completion wave.** The prior session **closed clean** (P4 build wave COMPLETE — doctor #25 → CLI seats #16 → verdict package #26 — plus a night E2E audit + a morning close). This session drives, in order: (1) the **ready slack #22 + #23** — the ADR-11 **D2 parity closure** (CONTRACT §7 known-deviations: `--file` frontmatter parse #22 + research `--return-dir` #23), both **UNBLOCKED**; closing both **empties CONTRACT §7 → triggers the DRAFT-INT-2 `1.0` version stamp**; (2) the **night-finding hardening fixes #39–#43** (no-persist/scratch output guard #39 · `options_considered` extractor #40 · CLI-seat token regexes #41 · research double-prefix #42 · first-class `codex` seat name #43); then (3) **#27 CLI-4 parity** as the follow-on centerpiece — **un-gates the ADR-12 §5 default-flip**. **Date-gates to flag:** **#33** (terra pass-3) and any terra-gated review are runnable only **on/after 2026-07-23** (codex credits reset). **G3 / Epic B is RESOLVED by operator ruling** (not scoring) — do not re-score. Navigate via ai-council `BACKLOG.md` [E1]/[S10] + the night audit `docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` §4.2 gap-map; the RESIDUAL carries only what the repo does not already encode. |
| **Generated at** | Hand-authored in the hub from **READ-ONLY live git** of `../ai-council` at the **2026-07-17 session close** (P4 wave complete + night batch + morning close all merged; session closed clean). States **no** sha / count / verdict / armed-state — **re-derive HEAD / tree / branch / counts / hooks live in the ai-council checkout** (`PROBES.md` P1–P3) and read the live ready-slack from BACKLOG (P4). |

> **`SUPPLEMENT.md` is FILLED** by the outgoing session CC (which drove the P4-wave close + night batch + morning close). The incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written (2026-07-17)?"* — it does not fire full.

> **Anti-bluff in effect (read `PROBES.md` header).** This bundle **withholds every probe answer value** by construction — no SHAs, counts, region text, phase-table lines, or armed-state. The withholding IS the teeth; run the commands **in the ai-council checkout**.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives **once** in the hub canonical runbook **`docs/handoffs/README.md`**. This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry **no per-bundle README** (HANDOFF_PROCESS §13).

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste **`PASTE_THIS.md`** (in this bundle directory) — the browser role file + residual + probes, assembled in order by `scripts/assemble_paste.py`. One paste; never hand-feed individual files to the file-less browser.
3. The browser replies with its on-load acknowledgment line (naming the Layer-1 actor); a partial/missing paste is then visible.
4. **architect mode** — the browser adopts the posture from `protocols/HANDOFF_BOOT.md`: orient, ask the operator for off-repo context, then drive the decision of what to close first in the P6 window. This is a small **build** session (the D2 parity pair); the browser holds the whole-system view (the CONTRACT §7 deviations + the DRAFT-INT-2 version-stamp trigger) and stress-tests the plan.
5. **Orient before design** — hand the browser `PROBES.md` **P4** (the forced ready-slack read) first; it replies `run <command>`, CC reads the live ai-council `BACKLOG.md` **#22/#23 lines** and substring-checks the browser's quote. This anchors the window-completion work in the live story-map before design.
6. **Then the operator-context beat (§13d), NARROWED** — the supplement carries the off-repo context, so the browser asks only *"anything changed since the supplement was written?"* (a priority shift since 2026-07-17) — not the full off-repo interview.
7. Hand `RESIDUAL.md` — the window-completion "why" + the carried residuals, then run the rest of `PROBES.md` (P1–P3). Any probe FAIL blocks onboarding (the escalation ladder). **Re-derive every value live — the bundle states none.**

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo(s) and are referenced by **pointer**; CC (which holds both trees) serves any part the file-less browser needs just-in-time. `PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited); `docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins.
