---
id: "[#530]"
title: "Single-flight dispatch guard — one contract execution at a time"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#530] [P2][S] **Single-flight dispatch guard — one contract execution at a time** — born 2026-08-15 (D4.6, ruled IN). Closes the witnessed triple-execution class: three executions of one contract live at once, two independently allocating the same four ids, sharing neither tree nor machine. **Design: a git ref as a distributed compare-and-swap**, claimed with `--force-with-lease=<ref>:` (empty expect = the ref does not exist) pushed to `origin`, plus a local `git update-ref --stdin create` fast leg for same-clone contention. Zero new dependencies. **The trap it avoids:** a plain `git push` of a lock ref exits 0 with `Everything up-to-date` when both racers sit at the same commit — the normal batch-dispatch state — so the lease IS the mechanism. Fail CLOSED on internal error · **Ruled precondition: step 0 now needs network** · Done when: the guard claims and releases a lock ref, a second clone that never fetched the ref is refused, a same-commit racer is refused rather than passing, and those T2/T4 properties are demonstrated against the real `origin`, not a local bare remote · refs the night-2 research audit §1 (design + T1–T10 evidence), `protocols/STANDING_RULINGS.md` I-D3 · kill-candidates: none — [#527] refuses a direct commit on main and owns no dispatch concurrency · serialize-group: gates
