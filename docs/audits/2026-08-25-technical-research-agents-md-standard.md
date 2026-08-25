# AGENTS.md and Native Instruction-File Support Across AI Coding Agents: An ADR Input Report

*Compiled August 25, 2026. This landscape changes monthly; every claim is dated. Primary sources are vendor docs and the agents.md spec itself. This report maps findings onto the two decision-fork options but does not make the decision.*

## TL;DR
- **The decision criterion is met.** As of August 2026, well more than two admitted providers natively consume AGENTS.md while NOT reading CLAUDE.md — OpenAI Codex, Google Gemini CLI (one-line config), GitHub Copilot coding agent, plus Cursor, Windsurf, Zed, opencode, Aider, Devin, Jules and 20+ others. xAI Grok Build also reads AGENTS.md (and additionally auto-reads Claude files). Claude Code is the lone major holdout that reads CLAUDE.md and does NOT read AGENTS.md at runtime. Under the stated rule this points toward the thin-file (root AGENTS.md) option.
- **AGENTS.md is now a Linux Foundation standard**, donated by OpenAI to the Agentic AI Foundation on December 9, 2025, adopted by 60,000+ repositories (up ~3x from ~20,000 in August 2025), with native support in 20–30+ tools. It is plain Markdown, no schema, nearest-file-wins nesting.
- **The premise in the retired ADR — "both tools read CLAUDE.md directly" — is now false for a multi-provider fleet.** Only Claude Code (and Grok, which also auto-reads Claude files) reads CLAUDE.md; Codex, Gemini, Copilot, Cursor et al. do not. The robust cross-tool primitive today is AGENTS.md, with CLAUDE.md relegated to a thin Claude-specific importer.

## Key Findings

1. **AGENTS.md is the industry-convergent standard.** Released by OpenAI in August 2025; co-developed with Amp (Sourcegraph), Jules (Google), Cursor, and Factory; donated to the Linux Foundation's new Agentic AI Foundation on December 9, 2025 (alongside Anthropic's MCP and Block's goose). Plain Markdown, no required fields, no YAML frontmatter (v1.1 proposes optional description/tags). Nesting rule: the nearest AGENTS.md to the edited file wins; explicit user chat prompts override everything.

2. **Native AGENTS.md readers (no adapter):** OpenAI Codex (CLI + cloud), GitHub Copilot coding/cloud agent, Cursor, xAI Grok Build, Windsurf/Devin, Zed, opencode, Amp, Google Jules, Factory, VS Code, JetBrains Junie, Warp, RooCode, Cline, Kilo Code, Augment, Ona, Semgrep, UiPath, and more.

3. **AGENTS.md requiring one config line (still effectively native):** Google Gemini CLI (`context.fileName` in settings.json) and Aider (`read: AGENTS.md` in .aider.conf.yml). These do NOT auto-discover AGENTS.md by default but read it with a single documented setting.

4. **Claude Code is the exception.** Anthropic's official memory docs state Claude Code reads CLAUDE.md (and CLAUDE.local.md, ~/.claude/CLAUDE.md), NOT AGENTS.md at runtime. The documented, Anthropic-recommended bridge is a one-line `@AGENTS.md` import at the top of CLAUDE.md, or a symlink. The feature request to read AGENTS.md natively (issue #6235) is the single largest unmet request in the Claude Code tracker — 5,270+ reactions as of 2026-06-02, "by a 4x margin" the largest, with related request #31005 adding ~220 more — and remains open, with Anthropic's stated position reported as "not planned for now" as of mid-2026.

5. **Size matters.** Every tool loads the whole instruction file into context at session start on every request. Vendors and practitioners converge on "keep it short" — Claude Code docs flag files over 200 lines; Codex caps combined instruction files at 32 KiB (`project_doc_max_bytes`) and truncates silently beyond it. Research and practitioner reports document performance degradation from bloated always-on instructions ("lost in the middle," instruction budget, drift/staleness). A ≤120-line thin file is squarely aligned with best practice (one practitioner analysis puts "the practical limit for a high-signal CLAUDE.md at 80 to 120 lines").

## Details

### (a) AGENTS.md standard — adoption state with dates

- **Origin:** Introduced by OpenAI in **August 2025** for Codex; the agents.md site credits collaboration across OpenAI Codex, Amp, Jules (Google), Cursor, and Factory. (agents.md, fetched Aug 2026; OpenAI blog, Dec 9, 2025.)
- **Governance:** Donated to the **Linux Foundation's Agentic AI Foundation (AAIF)** on **December 9, 2025**, alongside Anthropic's MCP and Block's goose. Platinum AAIF members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. (Linux Foundation press release; TechCrunch; OpenAI — all Dec 9, 2025.)
- **Format/spec:** Plain Markdown. No required fields, no YAML frontmatter, no JSON schema, no MUST/SHOULD conformance language. The site's only normative guidance: "use whatever headings make sense." Popular H2 sections: project overview, setup/build commands, code style, testing instructions, security considerations, PR/commit rules. (agents.md, fetched Aug 2026.)
- **Location & nesting:** Root of repo; monorepos place nested AGENTS.md per package. "Agents automatically read the nearest file in the directory tree, so the closest one takes precedence." OpenAI's own Codex repo maintains 88 AGENTS.md files. (agents.md, fetched Aug 2026.)
- **Adoption trajectory:**
  - ~**20,000** repos — reported by InfoQ and Socket.dev, August 2025 (both citing the agents.md homepage).
  - ~**40,000** repos — SiliconANGLE, December 9, 2025 ("adopted by over 40,000 open-source projects and coding agents") — an interim figure reported the same day as the LF announcement.
  - **60,000+** repos — OpenAI blog + Linux Foundation press release, December 9, 2025 ("more than 60,000 open source projects and agent frameworks including Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code"); reaffirmed by InfoQ (March 2026), arXiv 2601.20404 (Jan 2026), and the agents.md homepage (still "over 60k" as of Aug 2026).
  - This is roughly **3x growth in ~4 months** (Aug→Dec 2025). The "60k+" homepage figure has been frozen across Dec 2025–Aug 2026, so the true mid-2026 count is likely higher but unpublished; treat 60k as a floor.
  - Academic framing: arXiv "Agentic Much? Adoption of Coding Agents on GitHub" (v2, data collected Feb 21, 2026) studied 128,018 mature projects and found overall coding-agent adoption of 22.20%–28.66%, "extremely rapid for a technology only a year old." (Note: its ~5,325 "Generic/AGENTS.md" count is a filtered-sample subset, not comparable to the whole-GitHub 60k figure.)
  - Tool-support count: agents.md listed 19 agents on Nov 14, 2025; 20–30+ by 2026.

### (b) Per-tool native-support matrix

| Tool | Instruction file(s) read natively | AGENTS.md native? | Precedence / nesting | Source (date) |
|---|---|---|---|---|
| **OpenAI Codex** (CLI + cloud) | AGENTS.md; AGENTS.override.md; ~/.codex/AGENTS.md; fallback via `project_doc_fallback_filenames` | **Yes** | Walks git-root→cwd, concatenates root-first/leaf-last; closer-to-cwd wins on conflict; AGENTS.override.md beats AGENTS.md at each level; ~/.codex global loaded first; combined cap 32 KiB (`project_doc_max_bytes`), silent truncation. config.toml is separate tooling config, discovered by walking to project root (.git). Fallback-filename support landed via issue #4376 / PR #4544 (closed 2025-10-01). | developers.openai.com/codex/guides/agents-md; config-advanced (2026) |
| **Anthropic Claude Code** | CLAUDE.md; CLAUDE.local.md (deprecated → imports); ~/.claude/CLAUDE.md; @path imports; .claude/rules/*.md | **No (runtime)** | Recurses cwd upward reading CLAUDE.md/CLAUDE.local.md; higher-in-hierarchy loaded first as foundation; @-imports resolved at launch (max depth 5), do not save context. `/init` (with CLAUDE_CODE_NEW_INIT=1) can *read* AGENTS.md/.cursorrules/.windsurfrules to *generate* CLAUDE.md, but does not load AGENTS.md at runtime. Bridge: `@AGENTS.md` import or symlink. | docs.anthropic.com/en/docs/claude-code/memory; code.claude.com/docs/en/memory (checked 2026-06) |
| **Cursor** | .cursor/rules/*.mdc (modern); .cursorrules (legacy, deprecating); AGENTS.md; User/Team rules | **Yes** | Cursor reads AGENTS.md as a "simple alternative to .cursor/rules"; reads both and merges; .mdc rules (alwaysApply/glob) carry higher contextual weight when scoped; nested AGENTS.md inherit hierarchically; rule precedence Team→Project→User. | cursor.com/docs/rules (2026) |
| **Google Gemini CLI / Code Assist** | GEMINI.md (default); configurable via settings.json `context.fileName` (accepts array incl. AGENTS.md); @file imports; Code Assist agent mode reads GEMINI.md or AGENT.md | **Config (one line)** | Default GEMINI.md; set `{"context":{"fileName":["AGENTS.md","GEMINI.md"]}}`; all discovered context files concatenated and sent every prompt; footer shows count loaded. | google-gemini.github.io/gemini-cli docs; agents.md FAQ (2026) |
| **xAI Grok (Grok Build CLI)** | AGENTS.md family (AGENTS.md, Agents.md, AGENT.md); also auto-reads CLAUDE.md, Claude.md, CLAUDE.local.md, .claude/rules/; .grok/GROK.md; .grok/settings.json | **Yes** | Walks cwd→repo-root for the AGENTS.md family; also reads Claude Code instruction files, skills, MCPs "with zero config." `grok inspect` shows what was loaded. | docs.x.ai/build (2026); community grok-cli |
| **DeepSeek** | No official first-party coding CLI/instruction convention. Community forks: DeepSeekCode (Claude Code fork → reads CLAUDE.md/.agents/skills), DeepSeek-TUI, Deep Code CLI (.agents/skills). Typically used via other agents (Cline/Continue/Aider/OpenCode) that read AGENTS.md. | **Via host tool** | DeepSeek = model+API; instruction-file behavior inherited from whichever harness wraps it. | DeepSeek API docs; community forks (2026) |
| **GitHub Copilot** (coding/cloud agent) | AGENTS.md (root + nested); .github/copilot-instructions.md; .github/instructions/**.instructions.md (applyTo globs, excludeAgent); also CLAUDE.md and GEMINI.md | **Yes** (coding agent, since Aug 28 2025) | All read and merged; Copilot-specific instructions typically win on conflict; nested AGENTS.md apply to their subtree; NOT strict enforcement (nondeterministic). Note: **Copilot CLI** uses .agent.md custom-agent files, not AGENTS.md. | github.blog changelog (Aug 28, 2025; Nov 12, 2025) |
| **opencode** | AGENTS.md | **Yes** | Reads both AGENTS.md and CLAUDE.md; AGENTS.md wins (published order). | opencode docs; alexdunlop.com (Aug 7, 2026) |
| **Aider** | CONVENTIONS.md / AGENTS.md via `--read` or `read:` in .aider.conf.yml | **Config (one line)** | Does NOT auto-discover; needs explicit `read: AGENTS.md`. | aider.chat docs; agents.md FAQ (2026) |
| **Windsurf / Devin (Cognition)** | AGENTS.md; .windsurfrules / .windsurf/rules/; Devin native .devin/rules/ | **Yes** | Root AGENTS.md always active; subdirectory AGENTS.md apply when Cascade works there; Devin reads AGENTS.md before tasks, nearest-file precedence. Windsurf became "Devin Desktop" June 2, 2026. | agents.md; vibecoding.app; blakecrosley.com (2026) |
| **Zed** | AGENTS.md | **Yes** | Reads both; AGENTS.md wins (published order). | zed.dev/docs/ai/rules; agents.md (2026) |
| **Amp (Sourcegraph)** | AGENTS.md (native); falls back to CLAUDE.md if no AGENTS.md | **Yes** | Per-directory fallback; keep one canonical root file. Created predecessor AGENT.md (May 2025), adopted AGENTS.md name Aug 20, 2025. | ampcode.com; alexdunlop.com (2026) |
| **Jules (Google)** | AGENTS.md | **Yes** | Nearest-file precedence. | agents.md; InfoQ (Aug 2025) |
| **RooCode / Cline** | AGENTS.md (+ .clinerules for Cline) | **Yes** | Cline confirmed reading AGENTS.md (Aug 7, 2026 verification). | agents.md; alexdunlop.com (2026) |

### (c) Thin-file / pointer pattern landscape

The multi-tool problem: teams historically maintained 4–6 overlapping files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, .github/copilot-instructions.md, .windsurfrules), causing duplication, version drift, and precedence surprises. Documented approaches:

- **AGENTS.md canonical + CLAUDE.md as one-line `@AGENTS.md` importer** (the pattern Anthropic itself recommends). CLAUDE.md holds only Claude-specific overrides below the import. Cleanest for mixed fleets; works cross-platform including Windows. Caveat: @-imports load at launch and do NOT reduce context/token cost.
- **Symlink** (`ln -s AGENTS.md CLAUDE.md`): zero divergence, 5-second setup. Pitfalls: Windows requires Administrator/Developer Mode or `core.symlinks=true`, else the checkout becomes a plain text file containing the literal path; some tools resolve the symlink and complain about content type. Anthropic recommends the @-import over symlink on Windows/mixed-OS teams.
- **Single-source generation tools:** `rulesync` (npm/PyPI; generates CLAUDE.md, .cursorrules, copilot-instructions.md, GEMINI.md, .windsurfrules, .clinerules from a canonical `.rulesync/`), `ruler` (intellectronica; also distributes MCP configs), `agentsync`/ai-rules-sync (converts between formats, zero-deps). These run in pre-commit hooks/CI to prevent drift.
- **Enforce mechanically in CI:** keep CLAUDE.md a symlink or one-line import and fail the build if CLAUDE.md becomes a regular file lacking `@AGENTS.md`; diff any real copies and fail on divergence. "Drift is a process problem; the fix belongs in the pipeline."
- **Reported failure modes:** (1) *drift* — the larger the file, the more surface area to diverge from code; agents then search for renamed modules or follow stale CI instructions; (2) *precedence surprises* — subdirectory files silently override root; Codex's AGENTS.override.md *replaces* rather than *extends* a level; (3) *token bloat / silent truncation* — Codex drops content past 32 KiB with no warning ("no log output, no indication in the TUI"), starving project-specific files if the global file is large.

### (d) Size and content best practices

- **Codex:** combined instruction files capped at 32 KiB by default (`project_doc_max_bytes`); silent truncation beyond; docs advise "raise the limit or split instructions across nested directories when you hit the cap."
- **Claude Code:** verbatim from docs — "Files over 200 lines consume more context and may reduce adherence. Claude Code skips a file over 4 MiB." `/doctor` (requires Claude Code v2.1.206+) proposes trims, cutting content Claude can derive from the codebase (directory layouts, dependency lists, architecture overviews) and keeping pitfalls, rationale, and conventions that differ from tool defaults. @path imports organize but do not save context.
- **Cursor:** keep always-apply rules under 200 words to avoid the "token tax."
- **Practitioner "instruction budget":** frontier thinking models reliably follow only ~150–200 distinct instructions; one analysis notes Claude Code's own system prompt already occupies ~50 of those slots, leaving "100 to 150 usable instruction slots," and puts "the practical limit for a high-signal CLAUDE.md at 80 to 120 lines." Every token loads on every request. Past the low-thousands of tokens, adherence becomes unreliable and models "start randomly ignoring rules across the board." Research on "lost in the middle" (Liu et al. 2023) shows middle-of-file instructions are under-used. Long-context agent studies show capability degradation well before the technical limit (often noticeable past ~100K tokens; some models degrade after 50K).
- **Content guidance:** put non-inferable facts (build/test commands, conventions that differ from defaults, "do not touch" boundaries, security gotchas, historical/architectural rationale). Move on-demand detail to skills (SKILL.md, progressive disclosure) or linked docs rather than always-on instruction text. Anthropic removed 80%+ of Claude Code's own system prompt for the Claude 5 generation with no measured regression, and over-verification rules ("always double-check") now cause harm on newer models. **A ≤120-line thin file of non-inferable facts is squarely best practice.**

### (e) Nesting / precedence semantics (monorepo-relevant)

- **AGENTS.md (general spec):** nearest file to the edited file wins; user prompt overrides all; nested files provide package-level overrides.
- **Codex:** deterministic chain — ~/.codex/AGENTS[.override].md → git-root → each intermediate dir → cwd, concatenated root-first, leaf-last; later (closer) files override; AGENTS.override.md *replaces* a level entirely (does not extend); 32 KiB cap halts discovery; rebuilt every run (edits mid-session require restart).
- **Claude Code:** recurses cwd upward reading CLAUDE.md/CLAUDE.local.md; higher-in-hierarchy loaded first as foundation that more-specific files build on; also reads files above cwd (foo/CLAUDE.md and foo/bar/CLAUDE.md both load).
- **Cursor:** root AGENTS.md applies repo-wide; src/AGENTS.md scopes to src/ and below; nested inherit from parent, more specific overrides on conflict; .mdc glob rules add scoped precision.
- **Windsurf/Devin:** root AGENTS.md always active; subdirectory files apply only when working in that directory.
- **opencode/Zed:** read both AGENTS.md and CLAUDE.md, AGENTS.md wins (order published). **Amp:** per-directory fallback — keep one canonical root file rather than scattering both names.

## Recommendations

1. **Treat the decision criterion as satisfied.** The stated rule — "≥2 admitted providers natively consume AGENTS.md and not CLAUDE.md → thin-file option" — is comfortably exceeded: Codex, Gemini CLI (one-line config), and Copilot coding agent all consume AGENTS.md and none read CLAUDE.md; Cursor, Windsurf, Zed, opencode, Aider, Devin, and Jules add to the count. (Grok reads both, so it is neutral to the test.) This maps to the **adopt-root-AGENTS.md-thin-layer** fork. This report does not make the decision; it maps findings onto the criterion.

2. **If adopting the thin AGENTS.md layer**, stage it:
   - Make root **AGENTS.md** canonical: ≤120 lines, non-inferable facts only (build/test commands, boundaries, security gotchas, conventions that differ from defaults).
   - Reduce **CLAUDE.md** to a one-line `@AGENTS.md` import plus any genuinely Claude-specific overrides (this is Anthropic's own recommendation and is Windows-safe). Avoid a bare symlink unless the whole team is on macOS/Linux.
   - For **Gemini CLI**, commit `.gemini/settings.json` with `{"context":{"fileName":["AGENTS.md","GEMINI.md"]}}`. For **Aider**, commit `.aider.conf.yml` with `read: AGENTS.md`.
   - **Do not symlink whole tool directories** (.claude/ holds Claude-only settings); symlink or generate only shared items.
   - Add a **CI drift-check**: fail if CLAUDE.md is a regular file lacking `@AGENTS.md`, and diff any real copies. Optionally adopt `rulesync`/`ruler` if you need to generate many tool files from one source.

3. **Monorepo/nesting:** use nested AGENTS.md per package; document that closest-file-wins and that Codex's AGENTS.override.md replaces (not extends). Keep each nested file small so the 32 KiB Codex cap never truncates deeper, more-specific files.

4. **Benchmarks that would change the recommendation:**
   - If **Anthropic ships native AGENTS.md read** (watch claude-code issue #6235 / the memory docs; current position reportedly "not planned for now"), the CLAUDE.md importer becomes optional — you could drop to a single AGENTS.md file with no per-tool pointer for Claude.
   - If the fleet standardizes on **Claude Code + Grok only** (both read CLAUDE.md), the criterion flips and CLAUDE.md-only becomes defensible.
   - If any admitted provider **drops AGENTS.md support**, re-run the count.

## Caveats

- **Fast-moving landscape.** Every claim is dated; re-verify vendor docs before finalizing the ADR. The "60k+" adoption figure has been static across Dec 2025–Aug 2026 and is a floor, not a precise current count.
- **"Native" is fuzzy.** Gemini CLI and Aider need a one-line config to read AGENTS.md — I count these as effectively native (documented, single setting, no adapter) but they are not zero-config like Codex or Cursor. If the ADR requires strict zero-config auto-discovery, exclude them; the criterion is still met by Codex, Copilot, Cursor, Grok, Windsurf, Zed, opencode, etc.
- **Claude Code "fallback" myth.** Several third-party guides claim Claude Code reads AGENTS.md "as a fallback when no CLAUDE.md exists." Anthropic's official docs contradict this; do not rely on it.
- **Enforcement ≠ loading.** All these files are advisory context, not guarantees. GitHub explicitly warns Copilot may not follow instructions exactly (nondeterministic). Hard requirements belong in CI/branch protection, not instruction files.
- **DeepSeek** has no first-party instruction-file convention; its behavior depends entirely on the host harness. If DeepSeek is an "admitted provider," specify which CLI/IDE wraps it before relying on any file convention.
- **Source quality:** vendor docs (OpenAI, Anthropic, Google, GitHub, Cursor, xAI) and the agents.md spec are primary and reliable. Adoption numbers ultimately trace to the agents.md homepage self-report (GitHub code search); the academic arXiv figures use a filtered sample and are not directly comparable. Many "complete guide" blogs corroborate but are secondary.