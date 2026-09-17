---
id: "[#811]"
title: "A frozen contract can be re-issued after its pin, and a lane still boots on it -- the freeze is nominal"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#811] [P1][S] **A frozen contract can be re-issued after its pin, and a lane still boots on it -- the freeze is nominal** - Measured by lane ab-808. The batch AB manifest (`d0fe3865`, 16:03) pinned `LANE-ab-808-guard-timeout.md` at `25ece422...`. The prompts-dir file was re-issued at 19:41 (`2e7d91a6...`). The lane was dispatched and booted on the re-issued bytes, and ran for about an hour before the manifest followed: amendment 1 (`6ab764fc`, 20:41) re-pinned the new hash. It did not say the contract had changed or what changed. `LANE-ab-810` was re-issued in the same minute. The diff was recoverable only because the manifest seat's job scratch dir (`.claude/jobs/62117afb/tmp/contracts/`) still held the pinned bytes. It is a pure 13-line insertion of a "Model -- why opus" section (operator ruling 2026-09-16, "every model justified"); Done-contract, Steps and What-NOT-to-do are byte-identical. The content was benign this time; the mechanism would have let a Done-contract change through the same way. Nothing compares the contract a lane boots on against the committed pin. · Done when: RED-first, (1) `/lane-boot` and the `dispatch` verb REFUSE to boot a lane whose contract sha256 differs from the pin in the committed open-batch manifest (original or amendment), naming both hashes; (2) a re-issue after pinning lands only with a manifest amendment that carries the new hash AND the diff, or a byte-level statement of what changed; (3) the pinned bytes are kept in a durable home, not a job scratch dir, so a mismatch can always be diffed · refs `docs/audits/2026-09-16-technical-batch-ab-manifest.md` section 1, `docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md` section 2, `scripts/lane_boot.py`, `scripts/preflight_contract.py`, `docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md` section 0 · kill-candidates: none -- `[#823]` is the dispatch verb skipping the manifest's EXISTENCE check; this row is the contract's IDENTITY against the pin · source: operator ruling 2026-09-17 on lane ab-808's report, id 811 reserved by push from the lane's block
