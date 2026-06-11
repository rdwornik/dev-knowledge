# Thin boot pointer — paste this to start the browser
<!-- scope: meta -->

> v5 replaces the heavy multi-file bundle with **one** boot file. The whole boot for a
> fresh browser (Claude.ai) chat is **`protocols/HANDOFF_BOOT.md`** — not copied here, by
> design (a hand-copy drifts from its source — the `/review` vs `/codex review` class).

## What the operator does

1. Open a fresh Claude.ai chat.
2. Paste the **full contents of `protocols/HANDOFF_BOOT.md`** (the ~3-line core +
   the resident browser operating role + the plan-review output contract). That file
   carries the browser's role *with it* — never assume a CC-held file reaches the
   file-less browser, so it must be the thing you paste.
3. The browser replies, verbatim:
   `Booted as architect under HANDOFF_PROCESS v5. Ready for CC's handoff.`
   — a partial or missing paste is then visible (if it can't reply, it says what's missing).
4. Hand it `RESIDUAL.md` (this bundle), drift-flags first; then run `PROBES.md`.

## Why a pointer, not a copy

The methodology and the browser role live in the repo and are referenced by **pointer**;
CC (which holds the repo) serves any part the file-less browser needs, just-in-time. This
file points; `protocols/HANDOFF_BOOT.md` is the source. If the two ever disagree, the
source wins — fix the pointer.
