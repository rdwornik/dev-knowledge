# AI Council Invocation Mechanism — Discovery 2026-05-25

> **Type:** Reference artifact — operational discovery for orchestrating AI Council debates from `.dev-knowledge`.
> **Status:** Complete. All discovery questions (Q1–Q7) resolved from `ai-council` source/docs. No hard-stop triggered.
> **Purpose:** Capture the verified mechanism so future Council orchestration from this repo does not re-derive it.

## Sources read

| Source | Notes |
|--------|-------|
| `ai-council/CLAUDE.md` | Repo identity; Council is a CLI tool in `src/ai_council/`; "inbox loop" anti-pattern confirms a file-based intake exists |
| `ai-council/ARCHITECTURE.md` | Authoritative: codemap, data flow, transcript routing, folder governance, **Inbox File Detection** section (:202-217) |
| `ai-council/README.md` | Usage examples; `council --inbox`; Downloads auto-scan; transcript routing frontmatter |
| `ai-council/config/settings.yaml` | `dev_root`, `target_projects` (incl. `.dev-knowledge`), default panel/synthesizer, model strings |
| `ai-council/pyproject.toml` | Console-script entry points (`council`, `ai-council` → `ai_council.cli:main`) |
| `ai-council/.gitignore` | `council_inbox/*.md` + `council_inbox/archive/` + `output/` all ignored |
| `.dev-knowledge/docs/decisions/transcripts/` | Existing `council-out-*` transcripts confirm routing has landed here before |
| `.dev-knowledge/docs/council-questions/2026-05-25-handoff-council-Q1..Q5*.md` | 5 question files; frontmatter verified |

## Q1: Invocation command

`council --inbox`

- Console scripts `council` and `ai-council` both map to `ai_council.cli:main` (`pyproject.toml:30-32`). `python -m ai_council.cli --inbox` is equivalent (README:113-114).
- In this environment the binary lives at `ai-council/.venv/Scripts/council.exe` — **verified present**, and `import ai_council` succeeds from `.venv`.
- `--inbox` processes every `council_inbox/*.md` file (README:116-128; ARCHITECTURE.md:202-217).
- Exact command to run from `ai-council/` with the venv: `.venv/Scripts/council.exe --inbox` (or activate venv then `council --inbox`).

## Q2: Sync/async behavior

**Synchronous.** The CLI call blocks through the full pipeline (parallel debate rounds → synthesis → file write) and returns when done.

- Evidence: ARCHITECTURE.md Data Flow (:103-119) is a single linear pipeline ending in a file write; there is no queue/daemon/job-id. `asyncio` is used *inside* a run, not to detach it.
- Practical implication: each file triggers live API calls across the 4-model panel + synthesizer over 2 rounds. Expect minutes per question; all 5 sequentially may take tens of minutes. The invocation will not return until the last debate is written.

## Q3: Per-file vs batch processing

**Batch, sequential.** `--inbox` picks up all `council_inbox/*.md`, processed **oldest-first by mtime**; each file is an independent debate; each is archived to `council_inbox/archive/` (prefix `YYYY-MMDDTHHMM_`, or `FAILED_<ts>_` on error) after its run (ARCHITECTURE.md:206-217). One invocation handles all 5 question files.

## Q4: council_inbox git status

**Gitignored — safe to write.**

- `.gitignore:34` → `council_inbox/*.md`; `.gitignore:33` → `council_inbox/archive/`.
- `git -C ai-council check-ignore council_inbox/2026-05-25-handoff-council-Q1-internalization-assurance.md` → exit 0 (**FILE-IGNORED**).
- Therefore dropping `.md` question files into `council_inbox/` creates **no git-tracked content** in `ai-council` → the Layer-2 read-only contract on the Council host repo is preserved. **`council_inbox/` is the correct pickup location; the Downloads fallback is not needed.**
- (The bare-dir `check-ignore council_inbox` returns exit 1 only because the ignore pattern targets the dir's `.md` contents, not the dir node itself.)

## Q5: Transcript output location

**Auto-lands in `.dev-knowledge` — no manual move required.** Two writes per debate:

1. **Canonical** (always, hard requirement): `ai-council/output/{timestamp}_{slug}.md` (gitignored).
2. **Routed mirror** (ADR-43): because each question file carries `target-project: .dev-knowledge`, `routing.py` copies the transcript to `<dev_root>/.dev-knowledge/docs/decisions/transcripts/`.
   - `settings.yaml:17` → `dev_root: C:/Users/1028120/Documents/Dev/`
   - `settings.yaml:22-23` → `target_projects: [".dev-knowledge"]`
   - Resolved path: `C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/transcripts/`
- Mirror writes are best-effort: a mirror failure logs a warning but never fails the canonical write.
- Note: `settings.yaml:8` `secondary_output_enabled: false` — the *legacy global* mirror is OFF. Routing depends solely on the per-file `target-project` key, which all 5 files have.
- Confirmed by existing `council-out-*` transcripts already present in the target dir (most recent 2026-05-18).

## Q6: Filename convention

- **`council_inbox/` (the path we use):** ANY `.md` file is picked up — no filename token, no frontmatter required (ARCHITECTURE.md:206-210). Filename is irrelevant here.
- **`~/Downloads/` (NOT used):** the "`council` in filename stem OR council frontmatter keys" rule applies only to the opt-in Downloads scan (ARCHITECTURE.md:211-216).
- Output slug derives from the question's first `##` heading via `clean_slug()` (archive prefixes stripped).
- **CRITICAL COROLLARY:** because *any* `.md` in `council_inbox/` becomes a debate, files that are **not questions** must not be placed there. The index and evidence files have no frontmatter and are not debate questions — putting them in the inbox would spawn two bogus debates. **Only the 5 Q files go in the inbox.** (This corrects the sender prompt's "5 + index + optionally evidence" assumption, which predated mechanism discovery.)

## Q7: Panel configuration

**Per-file via frontmatter — already set, valid, no change needed.** All 5 question files carry:

```yaml
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
```

- Valid against the non-participating-synthesizer invariant (ARCHITECTURE.md invariant 5; ADR-01): `openai` is the synthesizer and is **not** in the debating panel.
- Intentionally overrides system defaults (`default_panel` = 3-model; default `synthesizer` = gemini) to a 4-model panel that uses gemini as a debater and openai as synthesizer. Config-driven; no code change.

## Question files inventory (`.dev-knowledge/docs/research/`)

| File | Frontmatter | Role | Goes to inbox? |
|------|-------------|------|----------------|
| `2026-05-25-handoff-council-Q1-internalization-assurance.md` | full, `target-project` ✓ | debate question | **Yes** |
| `2026-05-25-handoff-council-Q2-bundle-content-composition.md` | full, `target-project` ✓ | debate question | **Yes** |
| `2026-05-25-handoff-council-Q3-procedural-competence-transfer.md` | full, `target-project` ✓ | debate question | **Yes** |
| `2026-05-25-handoff-council-Q4-sender-verification-symmetry.md` | full, `target-project` ✓ | debate question | **Yes** |
| `2026-05-25-handoff-council-Q5-delivery-custody-abstraction.md` | full, `target-project` ✓ | debate question | **Yes** |
| `2026-05-25-handoff-methodology-council-index.md` | none | operator index | No (not a question) |
| `2026-05-25-handoff-failures-evidence.md` | none | reference evidence | No (not a question) |

All 7 present. The 5 Q files share identical, correct frontmatter.

## Mechanism unknowns

None blocking — Q1–Q7 fully resolved. The only residual is runtime-dependent: actual debate success requires live API keys and healthy providers at run time. `healthcheck.py` gates startup and silently skips unhealthy providers; a panel needs ≥2 healthy members. This cannot be verified until invocation; failures will be captured and diagnosed, not blindly retried.

## Decisions derived from discovery

1. **Pickup location:** `ai-council/council_inbox/` (gitignored; read-only contract preserved). Downloads fallback not needed.
2. **What to copy:** only the 5 Q files. Index + evidence stay in `docs/research/` (reference; would create bogus debates if inboxed).
3. **Evidence file rename (sender Step 2):** **not needed.** The "council in name" rule applies only to the Downloads path; via the inbox, naming is irrelevant, and the file should not be inboxed at all.
4. **Invocation:** single `council --inbox` run from `ai-council/` venv; synchronous; expect a long run; capture stdout/stderr/return code.
5. **Transcripts:** expected to auto-land in `.dev-knowledge/docs/decisions/transcripts/` via `target-project` routing; verify presence post-run, then commit them here.
