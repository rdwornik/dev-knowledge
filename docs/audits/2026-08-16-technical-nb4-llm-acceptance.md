# LLM-lane acceptance benchmark — seeded-defect design, per-CLI integration facts, and the promotion gate

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, admits no lane, and births no
> BACKLOG row. No config file, dependency, hook, protocol or routing surface was edited by the lane
> that produced it. The §4 routing amendment is a **draft for an operator act**, not an applied edit.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** nb4-llm-acceptance
- **Lane:** `claude/nb4-llm-acceptance-benchmark-pnoo2q` (Anthropic cloud session, Linux container),
  night-batch-4 lane A. Not a batch-6 lane — batch 6's roster (`docs/audits/2026-08-16-technical-batch-6-manifest.md`)
  is twelve local worktrees and does not include this one.
- **Mode:** read-only repo research + web research. Zero repo mutations outside this file and the
  mandated `docs/audits/README.md` index regeneration.
- **Tally:** 2/3/3/2 <!-- Critical/High/Medium/Low -->
- **Standing law this serves:** a new model lane enters ONLY through measured acceptance on seeded
  defects vs the incumbent baseline; artifact-or-RED with the severity tally in the artifact body
  from day one (`BACKLOG.md:267` `[#492]`, the `[#480]` durability property).
- **Consumer:** the seat that runs the `[#492]` re-check dated **2026-08-17** (register
  `protocols/STANDING_RULINGS.md` I-D item 1) — i.e. tomorrow.

---

## 0. Headline — the `[#492]` peg is MET, four days before its own re-check

**This is the one finding that changes what the next seat does, so it leads.**

`[#492]` is `DEFER`red behind a single external fact: *"peg: the Grok 4.6 release ALONE"*
(`BACKLOG.md:267`). The fleet's last recorded observation is **`EVIDENCE 2026-08-10` — "Grok 4.6 not
released as of 2026-08-10 (browser-verified) — no model card and no API id"**, and the row parks
behind a dated re-check of **2026-08-17**.

**Grok 4.6 was released 2026-08-12.** Both legs the 2026-08-10 evidence line names as missing now
exist:

| Leg the row requires | 2026-08-10 state (recorded) | 2026-08-16 state (this lane) |
|---|---|---|
| a model card | absent | present — a first-party card is published at `media.x.ai/v1/website/card-4p6-*.pdf`, revision 2026-08-12 |
| an API id | absent | present — `grok-4.6`, 500K context, served via the xAI API, Grok Build and Cursor |

**Honest limit on how this was established, stated before the claim is used.** The first-party model
card and `docs.x.ai` are both **blocked by this container's network egress proxy**
(`EGRESS_BLOCKED`, verified on three separate fetches). What this lane could verify is (i) the
first-party card **URL exists and is indexed** on an x.ai-owned domain with a 2026-08-12 revision
stamp, and (ii) the release, the model id and the price sheet are **corroborated consistently across
multiple independent secondary sources**. That is one grade weaker than the browser verification the
row itself used on 2026-08-10, and it is not a substitute for it. **The 2026-08-17 re-check should
still be run by the operator in a browser** — but it should be run expecting to *lift* the peg, and
the acceptance harness below should be commissioned now rather than after.

Recorded price sheet for `grok-4.6`, used in the §5 cost estimate and flagged as secondary-sourced:
**$2.00/M input · $0.50/M cached input · $6.00/M output** below 200K prompt tokens; the rate
**doubles above 200K** and xAI applies the higher rate to *all* tokens in such a request.

---

## 1. The seeded-defect benchmark — 13 defects across the four lane roles

### 1.0 What this design is not, and why that matters

The prior art is explicit that the fleet's only precedent — the 2026-07-31 Grok/terra shadow A/B —
**seeded nothing**: *"the A/B used a NATURAL diff. It seeded nothing"*
(`docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md:26`). Its `6.5/8` and
`~17/21` figures are **precision after triage, not recall** (`:80-83`). Seeding supplies a
denominator for the first time, so **catch rate is a new instrument, not a continuation** (R10).
This design therefore measures recall *and* keeps precision, per R11.

A second, sharper constraint: **`SEEDED-DEFECT-CORPUS-v0.1.md` already exists** (operator's
`Downloads`, browser-authored 2026-08-10; 12 seeds across classes V/F/L/C, verdicts re-derived
2026-08-13 with **0 flips** — `docs/audits/2026-08-13-verification-492-corpus-reconciliation.md`).
**Its four classes are not the five this brief names.** v0.1 covers vacuous test / fail-open except /
stale locator / fence corruption; this brief names encoding-strict-utf8, manifest-first ordering,
substring test pins, dead-SHA citations and grammar forfeits. **The design below is corpus v0.2 and
is additive to v0.1, not a replacement** — v0.1's 12 seeds stay valid and reconciled, and a full
acceptance run should draw from both (25 seeds total). Rebuilding v0.1's classes here would discard
a reconciliation that cost a lane.

### 1.1 The five classes, each pinned to a witnessed instance in this repo

Every class below is cited to a live locator, verified by reading the file in this session. No class
is asserted from memory.

| Class | Witnessed instance (verified this session) | Locator |
|---|---|---|
| **E — encoding / strict-utf8** | `_default_git` decoded round-tripped registry DATA with `errors="replace"`; a malformed byte baked U+FFFD into the record. Fixed by splitting the decode: **stdout STRICT, stderr lenient**, with `UnicodeDecodeError` → `RecordError` | `JOURNAL.md:14268` |
| | `scripts/fleet_parity.py:192` — invalid UTF-8 raised `UnicodeDecodeError`, never converted to `ManifestUnreadable`; an unreadable manifest exited **1** where the contract requires **2** | `JOURNAL.md:12364` |
| | The class as doctrine: *"any git/CLI subprocess I/O on Windows = binary + explicit UTF-8 + LF … with a test asserting 0 CR AND non-ASCII byte-fidelity AND loud-fail-on-malformed"* | `LESSONS.md:109`, `:111` |
| **M — manifest-first ordering** | *"Closing a row is **manifest-first**: flipping `status:` while the task node is still in `tasks/manifest.json` lets `--emit-source` rewrite the frontmatter back to `open` **while reporting success**"* | `JOURNAL.md:358` |
| | Four consecutive batches missed commit-the-manifest-at-dispatch; `[#505]` leg 1 was unmet that whole time and is met for the first time by batch 6 | `docs/audits/2026-08-16-technical-batch-6-manifest.md:45-53` |
| **S — substring test pins** | *"These are TOKENS, matched against the token preceding `install`, never substrings of the whole command: **a substring test credits `install-hooks` and `echo "pre_commit install"` as arming**"* | `deploy/carrier_floor.py:180` |
| | *"Both are checked so neither a `..` escape nor a symlink alias slips past the **lexical substring test**"* | `scripts/hooks/block_immutable_edits.py:96` |
| **D — dead-SHA citations** | A retrieval leg returned `799789025`; it does not resolve (`fatal: ambiguous argument`) — transposed digits from the real `79788902`. **One fabricated-looking locator in 26**, caught only because every SHA was re-resolved | `docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md:198-201` |
| | S9 — a citation pointing at a §8 that contains nothing on its stated subject; *"a stale locator inside the very document that catalogued the stale-locator class"* | same file, `:170-180` |
| | *"the one that does not resolve (`80dd54d6`) is named as unresolvable rather than quietly repeated"* | `docs/audits/2026-08-08-technical-library-research.md:692` |
| **G — grammar forfeits** | Batch 5 shipped two lanes `validate_branch_naming.LANE_BRANCH_RE` REFUSED — *"silently forfeiting the ADR-110 exemption and forcing a hand-anchoring workaround"*. **THIRD OCCURRENCE** of the class | `docs/audits/2026-08-16-technical-batch-6-manifest.md:74-77`; `BACKLOG.md:66` `[#531]` |

**Why these five are good discriminators, stated as a property rather than a hope.** Class **S** and
class **G** are machine-checkable in principle but checked by nothing at the point of failure — they
are the classes where a reviewer must reason about *what a predicate admits*, not about what the
code says. Class **E** and class **D** require reading live state (a byte stream, a git object)
rather than reasoning from the diff — which is precisely the axis on which the 2026-07-31 A/B found
the challenger stronger: *"grok actually READ `parity-surfaces.yaml`; terra reasoned from the diff +
ADR"* (`:186-187`). Class **M** is an ordering defect that leaves the tree in a state where the tool
**reports success** — the same shape as the fail-open class, which the substrate inventory calls the
best discriminator because *"the defect was written deliberately, with a stated rationale"* (`:152`).

### 1.2 The four lane roles

The roles are not invented for this document; each is a live fleet concept.

| Role | Live definition in this repo | What a seed measures |
|---|---|---|
| **producer** | Codex-as-producer, charter-only pending `[#341]`; interim R5 is *specify → CC implements → terra reviews* (`protocols/PLAYBOOK.md:4247-4248`) | Does the lane **emit** the defect when writing code/docs under a bounded prompt? |
| **reviewer** | `/codex-review` → `gpt-5.6-terra`, findings-only, artifact-or-RED with `Tally:` in the header (`docs/audits/2026-08-15-codex-o-review.md:1-9`) | Does the lane **catch** a seeded defect in a diff it did not author? |
| **adversarial** | *"CC adversarially verifies every Codex-produced artifact"*; the `conformance-hub` skill's *"adversarial skeptic kills false positives"* | Does the lane **refute** a seeded false claim instead of ratifying it? |
| **fan-out** | Haiku retrieval subagents, pinned by t-shirt size; *"unpinned fan-out is a bug"* (`protocols/PLAYBOOK.md:2371`) | Does the lane **retrieve without fabricating** at volume? |

### 1.3 The 13 seeds

Notation: `NB4-<role letter>-<n>`. **P**roducer · **R**eviewer · **A**dversarial · **F**an-out.
Every seed names its class, its witnessed ancestor, the exact injected mutation, and — per **R12,
fixed ex ante** — the **catch predicate**: the minimum a lane must say for the finding to score.

#### Reviewer role — 5 seeds (catch a defect in a diff you did not author)

| id | Class | Injected mutation | Catch predicate (ex ante) |
|---|---|---|---|
| **NB4-R-1** | E | In a new `subprocess` call site, `capture_output=True, text=True` on a path that round-trips **data** (not error text). Ancestor: `JOURNAL.md:14268` | Names that **data** decoding is locale-dependent (cp1252 on the Windows host) **and** that the correct split is stdout-strict / stderr-lenient. Naming only "add `encoding='utf-8'`" scores **half** — it fixes the instance, not the class. |
| **NB4-R-2** | E | A `try/except UnicodeDecodeError` that returns a sentinel, in a function whose documented contract is a distinct exit code. Ancestor: `JOURNAL.md:12364` (`fleet_parity.py:192`) | States that the handler makes an **unreadable** input indistinguishable from a readable one, **and** that the documented exit code is not reachable. |
| **NB4-R-3** | S | A new gate that decides arming with `if "pre-commit install" in cmd:`. Ancestor: `deploy/carrier_floor.py:180` | Produces at least one **concrete false-positive string** that the substring admits (`install-hooks`, `echo "…"`, a commented-out line). A finding that merely says "prefer token matching" without an admitting input scores **half**. |
| **NB4-R-4** | S | A path guard using `if target.startswith(PROTECTED_DIR)` with no `normpath`/`realpath`. Ancestor: `scripts/hooks/block_immutable_edits.py:96` | Names a **`..` escape or symlink alias** that defeats the lexical test. |
| **NB4-R-5** | M | A closer that flips `status:` in the task file **before** removing the node from `tasks/manifest.json`. Ancestor: `JOURNAL.md:358` | States that the generator will **rewrite the frontmatter back to `open` while reporting success** — i.e. identifies the silent-revert, not merely the ordering. |

#### Producer role — 3 seeds (does the lane emit the class under a bounded prompt?)

Scored on the **artifact the lane produces**, not on findings. A producer seed is a prompt whose
naive completion carries the defect; the lane passes by not emitting it, or by emitting it and
flagging it.

| id | Class | Bounded prompt | Pass predicate (ex ante) |
|---|---|---|---|
| **NB4-P-1** | E | *"Write a helper that shells out to `git show <ref>:<path>` and returns the file's text."* | The emitted code does **binary I/O + explicit UTF-8**, or states the encoding hazard in-line. Emitting `text=True` unflagged = **FAIL**. |
| **NB4-P-2** | S | *"Write a check that answers whether a settings blob arms the pre-commit hooks."* | The emitted check is **token-based** or states the substring hazard. A bare `in` test unflagged = **FAIL**. |
| **NB4-P-3** | G | *"Provision a batch lane for row #533, slug `docrot-arms`, and give me the branch name."* | Emits a name matching `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`, **or** says it cannot without the lane letter. Inventing an off-grammar name unflagged = **FAIL** — this is the `[#531]` class reproduced at the point it actually occurs. |

#### Adversarial role — 3 seeds (refute a plausible false claim)

These are the **precision guard** (R11). A lane that ratifies a false claim is worse than one that
misses a defect, because the fleet's whole finding pipeline (ADR-111) assumes findings are triable.

| id | Class | Seeded false claim, presented as established | Refute predicate (ex ante) |
|---|---|---|---|
| **NB4-A-1** | D | A prose paragraph citing a **transposed-digit SHA** as the fixing commit, in the style of the real `799789025` incident | Reports the SHA **does not resolve**. Silence or paraphrase = **FAIL**. |
| **NB4-A-2** | D | A citation of the form *"see `<real file>` §N for X"* where §N exists but is about something else. Ancestor: S9 | Reports the section **does not support the claim**, having read it. |
| **NB4-A-3** | G | The claim *"`block-ff-push` fails closed, so a direct-to-main push cannot land"* — true of the gate, **false as stated** because `--no-verify` is the documented escape and the hook is client-side | Names the bypass. Ratifying the absolute = **FAIL**. |

#### Fan-out role — 2 seeds (retrieve at volume without fabricating)

The binding constraint here is already ruled, not a preference: **"retrieval-not-classification is
baked into every Gemini contract"** — recorded as *"a measured incident, not a style preference"*
after a fan-out leg **fabricated an ADR count** (`BACKLOG.md` `[#491]`;
`docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md:386-391`).

| id | Class | Task | Pass predicate (ex ante) |
|---|---|---|---|
| **NB4-F-1** | D | *"Return the introducing and fixing SHA for each of these 8 named defects."* Two of the eight are **unresolvable by construction** | Returns `UNRESOLVABLE` for both planted items. **Any fabricated SHA is a HARD FAIL of the whole run**, not a scored miss (§3.4). |
| **NB4-F-2** | D | *"Count occurrences of `<token>` across `docs/audits/` and list the files."* Ground truth is fixed by `rg -c` at seed time | Count matches ground truth exactly, or the lane states it sampled. An **asserted** wrong count = FAIL — this is the ADR-count incident reproduced. |

### 1.4 Two properties the design deliberately keeps

- **A decoy is included and is not counted in recall.** One diff hunk in the reviewer bundle is
  ugly-but-correct. A lane that reports it is charged a false positive. Without this, a lane that
  flags every line scores 100% recall (R11).
- **Unseeded findings are dispositioned, not discarded (R13).** The 2026-07-31 verdict —
  *"COMPLEMENTARY, not redundant"* — rests entirely on **unique** catches. A run that scores only
  seeded defects structurally cannot reproduce the finding that justified keeping two lanes. So
  unseeded findings are triaged into ADR-111's four outcomes and reported as a **separate column**,
  never folded into recall.

### 1.5 The contamination hazard, and the concrete mechanism for it

**R8 is the live threat to this instrument's validity and it is unruled.** Every class above is
*described in this repo's own audits, JOURNAL and commit messages — including this document*. A lane
with repo read access can find the answer key by `grep` instead of by review.

Three mechanisms, in increasing cost. **This design proposes (b) as the default and (c) as the
measurement.** The choice is the operator's; it is named here because leaving it implicit is how the
result becomes unfalsifiable.

- **(a) Tool denylist.** Grok Build supports `--disallowed-tools "web_search,run_terminal_cmd"` and
  an allowlist `--tools "read_file,grep,list_dir"`; Gemini CLI has `--include-directories` to bound
  the workspace. **Insufficient alone** — `grep` is exactly the tool that finds the answer key.
- **(b) Scrubbed worktree (default).** The acceptance worktree is cut from the seeded base with
  `docs/audits/`, `JOURNAL.md`, `LESSONS.md` and `tasks/` **removed from the working tree**. Both
  lanes get byte-identical scrubbed trees. Cheap, deterministic, and verifiable by diffing the two
  worktrees before dispatch.
- **(c) Contamination canary (measurement).** One extra seed is planted whose answer text **is**
  present in a scrubbed-out file, and the run is executed twice on one lane — scrubbed and
  unscrubbed. The delta is the contamination coefficient. Costs one extra run (~$0.13) and converts
  R8 from an unruled hazard into a number.

### 1.6 The declared blind spot (R9)

**A seeded corpus measures only the classes it contains.** The 2026-07-31 A/B's single most valuable
catch — grok's C1, *reading live disk state* to find `RefKind` missing the `audit` provenance kind —
belongs to **none** of these five classes, and a seeded run would have scored it **zero**. This is
stated in the artifact body per R9 so that a REFUSE verdict cannot be read as "the lane is weak"
when it may mean "the corpus does not contain what the lane is good at".

---

## 2. Per-CLI integration facts, read from real docs

**Sourcing rule observed throughout: no flag appears below that was not read in a primary document
or a first-party repository.** Where a primary source was unreachable from this container, the fact
is marked `EGRESS_BLOCKED` and either corroborated or left open. No flag is inferred from another
CLI's conventions.

### 2.1 CRITICAL — two different CLIs are both invoked as `grok`, with incompatible flags

This is the finding most likely to burn an acceptance run, so it precedes the flag tables.

| | **xAI first-party** | **community** |
|---|---|---|
| Repo | `github.com/xai-org/grok-build` | `github.com/superagent-ai/grok-cli` |
| Product | "Grok Build" — xAI's coding agent harness + TUI | open-source coding agent for the Grok API |
| Binary | `xai-grok-pager`; **official installs ship it as `grok`** | **`grok`** |
| Install | `curl -fsSL https://x.ai/cli/install.sh \| bash` · `irm https://x.ai/cli/install.ps1 \| iex` | `curl -fsSL …/superagent-ai/grok-cli/main/install.sh \| bash` · `bun add -g grok-dev` |
| Headless prompt | `-p, --single <PROMPT>` | `-p, --prompt` |
| JSON | `--output-format <plain\|json\|streaming-json\|streaming-messages-json>` | `--format json` (NDJSON event stream) |
| Turn limit | `--max-turns <N>` | `--max-tool-rounds` |
| Auto-approve | `--yolo` / `--always-approve` | *(the fleet's 2026-07-31 run used `--always-approve`)* |
| API key env | `XAI_API_KEY` | `GROK_API_KEY` (also `GROK_BASE_URL`, `GROK_MODEL`) |

**What the fleet actually ran on 2026-07-31 was `grok 0.2.102` with
`--always-approve --max-turns 20 -p`** (`docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md:8`,
quoted in the substrate inventory `:41-44`; re-probed unchanged 2026-08-08 at
`:320-330`). That version string and flag set match **neither current CLI cleanly** — the community
CLI has since renamed `--max-turns` → `--max-tool-rounds`, and the first-party CLI is a different
program that happens to answer to the same name. **Consequence: the acceptance contract must pin the
binary by install path and `--version`, not by the word `grok`.** Running the wrong one is a burned
test in exactly the sense `[#492]` uses the phrase.

**Recommendation (stated, not ruled): use the xAI first-party Grok Build CLI.** It is the surface
`grok-4.6` is shipped through, it has the richer headless contract (below), and it is the one whose
docs are versioned in a first-party repository.

### 2.2 Grok Build (xAI first-party) — headless integration facts

Source: `xai-org/grok-build`, `crates/codegen/xai-grok-pager/docs/user-guide/14-headless-mode.md`
and `02-authentication.md`, read this session. `docs.x.ai` is **EGRESS_BLOCKED** from this container;
the repository docs are the primary source used instead.

- **Headless trigger:** `-p, --single <PROMPT>`; also `--prompt-json <JSON>` (content blocks) and
  `--prompt-file <PATH>`.
- **Output:** `--output-format <FMT>` ∈ `plain` | `json` | `streaming-json` |
  `streaming-messages-json`. The `json` object carries `text`, `stopReason`, `sessionId`, and
  **`usage: {input_tokens, output_tokens}`**.
- **Bounding:** `--max-turns <N>` (headless only) · `--tools <CSV>` allowlist · `--disallowed-tools
  <CSV>` denylist (both headless-only) · `--permission-mode <bypassPermissions|defaultMode>` ·
  repeatable `--allow <RULE>` / `--deny <RULE>` with `ToolPrefix(glob)` syntax, **deny taking
  precedence**.
- **Model:** `-m, --model <MODEL>`. **Pin it explicitly** — `[#469]` exists because the codex lane
  ran an unpinned model, and ADR-80 §5 forbids a silent swap on a pinned stage because it breaks
  evidence comparability across runs.
- **Auth, headless:** `export XAI_API_KEY="xai-…"`, or `grok login --device-auth` where no browser
  is available. Browser login is the interactive default; OIDC/SSO and an external auth provider
  also exist.
- **Exit codes:** `0` success · `1` error (auth/network/runtime) · `130` SIGINT · `143` SIGTERM.
- **Cost surface:** token counts are exposed per run in the JSON `usage` object. Price is **not** —
  the monitoring guide states plainly: *"There is no `cost.usage` metric: join `grok_code.token.usage`
  with your own price sheet."*
- **No stdin piping.** The docs use command substitution (`$(git diff --staged)` inside the prompt)
  or `--prompt-file`. A harness that pipes a diff on stdin will not work.
- **Windows fit — the honest statement, quoted:** *"macOS and Linux are supported build hosts;
  Windows builds are best-effort and not currently tested from this tree."* The installer does ship a
  PowerShell path (`irm https://x.ai/cli/install.ps1 | iex`), and Windows Terminal is a detected
  emulator. **Sandbox features are macOS-only** in the community CLI (`macOS 14+ Apple Silicon`);
  the first-party sandbox doc was not read for a Windows statement. Given this fleet's history with
  the Windows-text-mode class (`LESSONS.md:109`) and the ConPTY notes already in
  `ecosystem/tool-versions.yaml`, **treat Windows as a probe, not an assumption.**

### 2.3 Gemini CLI — headless integration facts

Source: `google-gemini/gemini-cli` `docs/cli/headless.md`, `docs/cli/cli-reference.md`,
`docs/get-started/authentication.mdx`, `docs/get-started/installation.mdx`, read this session.
`geminicli.com` and `google-gemini.github.io` are both **EGRESS_BLOCKED**; the repository docs are
the primary source used instead.

- **Headless trigger:** non-TTY environment, **or** `-p` / `--prompt`. Documented as *"Prompt text.
  Appended to stdin input if provided. Forces non-interactive mode."* — **so stdin piping works**,
  unlike Grok Build. `-i` / `--prompt-interactive` runs the prompt then stays interactive.
- **Output:** `-o` / `--output-format` ∈ `text` (default) | `json` | `stream-json`. The `json`
  object carries **`response`** (string), **`stats`** (token usage + API latency), and optional
  **`error`**. `stream-json` emits `init` · `message` · `tool_use` · `tool_result` · `error` ·
  `result`.
- **Model:** `-m` / `--model`, **default `auto`** — which is precisely the ADR-80 §5 hazard. **A
  pinned stage must pass `-m` explicitly**; leaving `auto` means the evidence is not comparable
  across runs.
- **Approval:** `--approval-mode` ∈ `default` | `auto_edit` | `yolo` | `plan`. `-y` / `--yolo` is
  **documented as deprecated** in favour of `--approval-mode=yolo` — do not write the deprecated
  form into a wrapper.
- **Workspace bounding:** `--include-directories <array>`. `-s`/`--sandbox`. `--allowed-tools` is
  **deprecated** in favour of the Policy Engine.
- **Sessions:** `-r` / `--resume` taking `"latest"` or an index.
- **Exit codes:** `0` success · `1` general error or API failure · `42` input error ·
  `53` turn limit exceeded. **`53` is load-bearing for a benchmark harness** — a turn-limit
  termination must be scored as an incomplete run, not as a zero-recall run.
- **Auth:** Google sign-in (browser) · `GEMINI_API_KEY` · Vertex AI via ADC, a service-account JSON
  at `GOOGLE_APPLICATION_CREDENTIALS`, or `GOOGLE_API_KEY`; `GOOGLE_CLOUD_PROJECT` /
  `GOOGLE_CLOUD_LOCATION` for organizational and Vertex paths. The docs state *"Headless mode will
  use your existing authentication method, if an existing authentication credential is cached"*, and
  recommend service-account keys for CI.
- **Cost model.** The free tier is the material fact and it is **tier-dependent**: browser Google
  sign-in with a personal account is reported at **~1,000 requests/day, 60/min**, while an unpaid
  **API key** path is reported at **~250/day, 10/min, Flash-only**. These numbers are
  **secondary-sourced** — the primary auth doc points at a separate quotas page and states no
  numbers itself, and that page was not reachable. **The auth path materially changes the quota, so
  it must be pinned in the contract and re-verified at run time**, not assumed.
- **Windows fit:** documented platforms are **macOS 15+, Windows 11 24H2+, Ubuntu 20.04+**;
  runtime **Node.js 20.0.0+**; **PowerShell listed as a supported shell** alongside Bash and Zsh.
  Install via `npm install -g @google/gemini-cli`, `brew`, or `npx`. **This is the better Windows
  story of the two by a clear margin.**
- **Unverified:** a `--session-summary` flag (writing execution metrics to a JSON file) is described
  in secondary sources but **does not appear in the primary `cli-reference.md` or `headless.md`**
  read this session. It is **not** relied on anywhere in this design.

### 2.4 What changed since the A/B's recorded cost limit

The 2026-07-31 A/B recorded: *"**Neither CLI exposes token pricing** — the cost leg of the §C
criterion is INCONCLUSIVE on hard numbers"* (`:32-34`), and the substrate inventory carried that
forward unchanged as **R14** on 2026-08-08.

**R14 is now partially stale, and this is a genuine advance rather than a re-reading.** Both
candidate CLIs expose **machine-readable per-run token counts** in headless JSON — Grok Build's
`usage.{input_tokens,output_tokens}`, Gemini's `stats`. Price is still not exposed by either, and
Grok Build's own docs say to join tokens against your own price sheet. So:

> **R14, restated for this design:** token counts are measurable per run and belong in the artifact
> body; **price** is computed externally from a pinned, dated price sheet and is reported as a
> derived figure with its sheet cited. A cost claim is no longer "wall-clock-comparable" — it is
> tokens-exact and price-derived.

---

## 3. The acceptance protocol

### 3.1 Prerequisite that is not optional — the wrapper (R6)

The A/B's own debt list records that the challenger lane *"ran ad-hoc (hand-built prompt, no
wrapper)"* and that a wrapper symmetric to `codex-review.ps1` *"would make the shadow repeatable +
comparable"* (`:93-95`). **A measured comparison requires both lanes invoked identically. Today only
the incumbent has a wrapper.** Building it is step 0, not a nicety — and note `[#338]` leg (c) is
already open on bringing `codex-review.ps1` itself under version control, which is a core-invariant
#6 surface. The candidate wrapper should be born **in-repo** rather than repeating that debt.

### 3.2 Identical worktrees, identical contract

1. **Seed once, off `main`.** Cut a seeding branch, inject the 13 mutations (plus v0.1's 12 if the
   full corpus is run), commit. **Seeds are never landed on `main`** — the v0.1 protocol paragraph
   already binds this, and the 2026-08-13 reconciliation honoured it by re-running seeds in a job
   scratch dir off-tree.
2. **Two worktrees, one tree state.** Provision `worktree-lane-<x>-<id>-accept-incumbent` and
   `…-accept-candidate` from the **same commit**, both scrubbed per §1.5(b). **Assert byte-identity
   with `git diff --no-index` between the two working trees before dispatch** and record the result
   in the artifact — the A/B's *"Both reviewers saw the SAME diff"* property made deliberate rather
   than incidental (R7).
   Both names must satisfy `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$` — running an
   acceptance benchmark on an off-grammar lane name would forfeit the ADR-110 exemption while
   testing for exactly that class (§1.3 NB4-P-3). Stated because the class has three occurrences.
3. **One contract, byte-identical prompts.** The same review contract text goes to both lanes.
   Neither lane sees the fix, the seed list, or this document.
4. **Pin everything ADR-80 §5 requires.** Explicit `-m` on both lanes; no `fallbackModel`; CLI
   `--version` recorded; `--max-turns` set; the price sheet dated.

### 3.3 Blind scoring

**The seeder does not score.** Findings from both lanes are stripped of lane identity, merged,
shuffled, and adjudicated against the pre-registered answer key by a seat that did not perform the
seeding. Each finding is scored against its §1.3 **catch predicate**, which was fixed before the run
— this is R12 discharged, and it is what stops the result being adjudicable after the fact.

**Severity mismatch (R12's specific open question), ruled ex ante for this design:** a
severity-mismatched catch **counts as a catch at full weight**, and the mismatch is reported in a
separate column. Rationale from the record: terra ranked the W2 root under-build **Critical** where
grok ranked it **High** — *"same defect, different severity"* (`:64-67`) — and both were real. A
scoring rule that zeroes one of them would have destroyed the A/B's actual finding.

**Partial credit is explicit**, not improvised: seeds NB4-R-1 and NB4-R-3 name a half-score
condition in their own predicate. Half-points follow the A/B's own precedent (`6.5/8`).

### 3.4 Promotion threshold

Let **recall** = seeded defects caught ÷ seeded defects present; **precision** = accepted findings ÷
total findings after triage (the A/B's `6.5/8` measure); **FP** = decoy and non-defect findings.

| Verdict | Condition |
|---|---|
| **HARD REFUSE** (overrides everything) | **any fabricated locator** — a SHA, `file:line` or section reference that does not resolve. Not scored as a miss: it fails the run. The fleet has a measured incident of exactly this (`[#491]`'s fabricated ADR count) and one near-miss in its own retrieval leg (1 in 26). A lane that invents citations cannot be admitted at any recall. |
| **HARD REFUSE** | the run cannot produce an artifact (artifact-or-RED), or the artifact carries no severity tally in its body. |
| **ADMIT — full lane** | recall **≥ incumbent's recall on the same corpus** · precision **≥ 0.70** · FP ≤ 2 · zero fabricated locators. |
| **ADMIT — shadow only** | recall **< incumbent** but **≥ 3 unique catches the incumbent missed** · precision ≥ 0.70 · zero fabricated locators. Runs **in parallel with**, never instead of, the incumbent. This verdict exists because it is the one the 2026-07-31 evidence actually supports: *"the two lanes are COMPLEMENTARY, not redundant"*. |
| **REFUSE** | anything else. |

**n=1 is not admission.** ADR-74 Footnote B's **n=2 evidence gate** binds: a routine codifies only
after **two** real runs. So a first ADMIT is provisional and the lane is confirmed on the second
independent corpus run. `[#492]`'s Done-when says *"≥1 real diff set"*, which is the floor for
**running the comparison**, not for **codifying a routine** — both are stated so the next seat does
not read one as the other.

**Every run writes an artifact regardless of verdict** — `docs/audits/<date>-verification-<slug>.md`,
class `verification` per the ADR-101 enum, with `Tally: C/H/M/L` in the header block per the codex
artifact grammar, plus the recall/precision/FP/tokens figures. **A REFUSE is as much a result as an
ADMIT**, and recording it is what stops the same candidate being re-tried by a seat that does not
know it was already refused (ADR-112's Tier S ledger reasoning, applied to a Tier L question).

---

## 4. Routing-table amendment — DRAFT, roles-not-vendors, one table edit

### 4.1 The blocking fact, stated first

**The canonical routing table is not in this repo and is not reachable from this container.**
`protocols/PLAYBOOK.md:4502` states it plainly: *"The model-routing table is canonical in
**`~/.claude/ROUTING.md`** … Not duplicated here (#158, Decision B: killed the resident copy — a
cached table silently drifts from ROUTING.md)."* Verified this session: `~/.claude/ROUTING.md` does
not exist in this container (the cloud runtime's `~/.claude` is not the operator's machine).

Two consequences, both material:

1. **This lane cannot draft a byte-accurate edit against the live table's actual columns.** The draft
   below states its **content and shape**; the operator maps it onto the real columns.
2. **`~/.claude/` is a core-invariant #6 surface** — per-machine global infra, hub-owned, edited only
   by exception with a ruling. `[#338]` leg (c) is already open on exactly this class for
   `codex-review.ps1`. **Applying this amendment is an operator act, not a session act.**

### 4.2 The draft — one added row

**Roles-not-vendors** means the row keys on the *role*, and admitted vendors live in a cell. Adding a
lane then becomes a **cell edit**, not a schema change — which is the property that keeps the table
from being rewritten every time a candidate appears.

```
| Role | Task class | Admitted lanes (pinned model) | Admission gate |
|---|---|---|---|
| reviewer — second opinion (shadow) | pre-merge review of a lane diff, run in parallel with the incumbent reviewer, never as the sole reviewer | gpt-5.6-terra (incumbent, admitted) | seeded-defect acceptance run vs the incumbent on identical scrubbed worktrees; ADMIT/shadow-ADMIT/REFUSE per the promotion threshold; artifact-or-RED with the severity tally in the artifact body; n=2 before the lane codifies as a routine |
```

**Notes for whoever applies it.**

- The `Admitted lanes` cell is deliberately **not empty and not speculative** — it lists the
  incumbent only. A candidate's model id is written into that cell **by the ADMIT verdict**, never
  in advance. This is the whole point of roles-not-vendors: the table records what passed, not what
  is being considered.
- The existing t-shirt pins (**S = Haiku · M = Sonnet · L/judgment = Opus**) are **untouched**. They
  route *size*; this row routes *role*. They are orthogonal axes and conflating them would be the
  drift the row is meant to prevent.
- If the operator prefers the amendment in-repo rather than in `~/.claude/ROUTING.md`, the single
  in-repo site that already carries routing claims is `ARCHITECTURE.md` Ch3 **"Model routing
  (t-shirt)"**. Note that placing it there **re-creates the resident copy #158 Decision B killed** —
  so it is named as an option with its known cost, not recommended.

---

## 5. Cost estimate and recommended first candidate role

### 5.1 Harness cost

**Build (one-time), the dominant cost and it is not tokens:**

| Item | Estimate | Basis |
|---|---|---|
| Candidate wrapper, symmetric to `codex-review.ps1` (R6) | **~1 lane-session** | named as a prerequisite by the A/B's own debt list; today only the incumbent has one |
| Corpus v0.2 — the 13 seeds above, injected + answer key + decoy | **~1 lane-session** | v0.1's 12 seeds already exist and are reconciled; this is additive |
| Scrub + byte-identity harness (§3.2) | folded into the above | `git worktree` + `git diff --no-index`, no new machinery |

**Per acceptance run (recurring), computed rather than guessed.** Assume 4 diff bundles carrying the
13 seeds, ~40K input / ~8K output per bundle per lane:

| Lane | Marginal cost per full run | Basis |
|---|---|---|
| incumbent `gpt-5.6-terra` | **$0** marginal | ChatGPT-auth subscription path |
| candidate **Grok 4.6** | **≈ $1.02** | 4 bundles × (40K × $2/M + 8K × $6/M) = 4 × $0.128; secondary-sourced price sheet, dated 2026-08-12; **stays under the 200K long-context band, so the doubling does not apply** — a bundle that crosses 200K costs 2× on *all* its tokens |
| candidate **Gemini CLI** | **$0** marginal on the browser-login free tier | ~1,000 req/day; 8 requests uses 0.8% of a day's quota. On the unpaid-API-key path (~250/day, Flash-only) it is still free but the model is not comparable |
| contamination canary (§1.5c) | **+ ≈ $0.13** | one extra Grok bundle |

> **Harness cost estimate: ≈ $1.15 in candidate API spend per full acceptance run, plus ~2
> lane-sessions of one-time build. Recurring marginal cost after build is under $1.20 per run, and
> under $0.20 for a single-bundle re-run.** The token cost is negligible; **the wrapper and the
> corpus are the real price**, and both are already named as owed work in the record.

### 5.2 Recommended first candidate role

**Reviewer (shadow), with Grok 4.6 via the xAI first-party Grok Build CLI.** Four reasons, each
resting on something verified above rather than on preference:

1. **The peg is met.** Grok 4.6 released 2026-08-12 with a model card and the API id `grok-4.6`
   (§0). `[#492]` is the only lane row whose blocker was external, and it has just cleared — four
   days before its own dated re-check.
2. **The role already has a method and a live baseline.** The 2026-07-31 A/B ran precisely this
   role, and terra runs the same diffs today with a wrapper and an artifact grammar. Nothing has to
   be invented except the candidate wrapper.
3. **The cost leg finally closes.** Grok Build's headless JSON exposes `usage.{input_tokens,
   output_tokens}` per run, so the A/B's *"cost INCONCLUSIVE"* limit becomes tokens-exact and
   price-derived (§2.4) — the acceptance run can answer the operator's original
   *cheaper-and-possibly-better* hypothesis on both halves for the first time.
4. **Gemini is the wrong first candidate for this role, by the fleet's own ruling, not by
   preference.** *"Retrieval-not-classification is baked into every Gemini contract"* — recorded as
   a measured incident after a fan-out leg fabricated an ADR count. Reviewing a diff against a
   doctrine clause is classification-shaped, so it sits **outside the lane's competence by ruling**.

**Gemini enters second, in the fan-out (retrieval) role only** — where seeds NB4-F-1 and NB4-F-2
test exactly the property its ruling is about, its free tier makes the run cost nothing, and its
Windows story (Windows 11 24H2+, PowerShell, Node 20+) is the better of the two on the operator's
actual machine. `[#491]` also has the cheaper unblocked first move: **the R-G one-line ruling needs
no corpus, no harness and no external release** — a grep of `protocols/STANDING_RULINGS.md` for
`R-G`/`Gemini` still returns no match, as the substrate inventory found on 2026-08-08.

---

## 6. Honest limits of this document

- **Nothing here was run.** No CLI was invoked, no model was called, no defect was seeded, no
  worktree was cut. This is a design plus a facts inventory; every number in §5.1 is an estimate
  derived from a stated price sheet and a stated bundle size, not a measurement.
- **Three primary sources were unreachable** from this container's egress proxy and are marked as
  such: `docs.x.ai`, `media.x.ai` (the Grok 4.6 model card itself), `geminicli.com` and
  `google-gemini.github.io`. Where they were needed, first-party **repository** docs were read
  instead; where only secondary sources existed (Grok 4.6 pricing, Gemini free-tier quotas), the
  fact is labelled secondary-sourced in place. **The §0 release finding should still be
  browser-confirmed by the operator at the 2026-08-17 re-check** — this lane raises the prior, it
  does not discharge the check.
- **The corpus is designed, not built.** The 13 seeds are specified to the level of an injected
  mutation and an ex-ante catch predicate; none is written as a patch. Whether one patch format
  covers all five classes is **R3, still open**.
- **The corpus form question (R2) is still unruled** — pointers-only vs extracted patches vs a
  manifest — and this document does not prefer an answer. Note only that extracted patches are the
  form that creates a new content class, which is what engages ADR-101's tree-seal gate.
- **The contamination mechanism (R8) is proposed, not ruled.** §1.5 recommends (b)+(c) and says so
  explicitly; the choice is the operator's, and the result's validity depends on it.
- **`--session-summary` is not relied on** anywhere, because it could not be found in the primary
  Gemini CLI docs read this session despite appearing in secondary sources.
- **This document is itself contamination.** It names five defect classes, their witnessed
  ancestors, and thirteen catch predicates — in `docs/audits/`, which is one of the trees §1.5(b)
  scrubs. That is deliberate and it is why the scrub list includes `docs/audits/`. A lane run
  against an unscrubbed tree after this file lands is measuring `grep`, not review.
