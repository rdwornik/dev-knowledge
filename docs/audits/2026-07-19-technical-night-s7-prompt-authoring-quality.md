# Night-audit S7 — Prompt-authoring quality: the browser↔CC equilibrium

Night-audit cycle-close · Stream S7 · ADR-101 class `technical`; read-only

## 1. Current mechanism (witnessed expectations + the emissions sampled, file:line)

**The codified contract is ADR-87 + PLAYBOOK §2; the closest existing per-item CHECKLIST is HANDOFF_PROCESS §14a — but §14a scopes only to generated EPIC-lane handoffs, not to ad hoc chat-native operator mandates (which is what actually shaped tonight's run and this cycle's real architect emissions).**

- **ADR-87** (`docs/decisions/ADR-87-equilibrium-contract.md:42-49`) — the equilibrium: *"The architect emits: intent · closure (what "done" looks like) · anti-patterns · the plan/auto mode · a thin per-task governance-context pointer... CC owns: code-impact context · generic gotchas · the prompt skeleton · model/effort."* Item 4 (line 55-58): the governance-pointer is required whenever governance applies, never optional.
- **PLAYBOOK §2 "Summary table"** (`protocols/PLAYBOOK.md:2245-2254`) — the single mandatory field-set for every formal prompt: `Model | Mode | Effort`. **No field for fan-out shape, worktree name, Codex lane, or deliverable location.**
- **PLAYBOOK §2 "Structure"** (`protocols/PLAYBOOK.md:2326-2362`) — the `[A]`/`[CC]` skeleton: TITLE/REPO/PURPOSE, governance pointer, git workflow, UNDERSTAND, STEPS, FINAL, WHAT-NOT-TO-DO. Single-session-shaped; no multi-agent/fan-out section.
- **`templates/prompt-template.md`** (v1.5, 2026-06-18, full file read) — the point-of-use build-prompt artifact. Fields: Model/Mode/Effort table, Repo, Purpose, Governance-pointer, Git-workflow (branch name only — no worktree-path field), UNDERSTAND, READINESS, numbered Steps, Final/`ship`, What-NOT-to-do. **Five section-history entries (v1.1-v1.5) tracked additive fields (obsolescence pass, READINESS valve, governance pointer) — none ever added fan-out shape, Codex lane, or a named-worktree field.** The template predates this cycle's multi-agent fan-out pattern.
- **HANDOFF_PROCESS §14a — EPIC handoff** (`protocols/HANDOFF_PROCESS.md:491-513`) — the ONE place a 7-item scope-contract checklist is actually codified: (1) epic scope, (2) epic done-contract, (3) **worktree+branch** (relative-paths-only), (4) **FILE-BOUNDARY** (explicit file/dir set), (5) escalation rules, (6) refusals, (7) **execution MODE + basis**, re-declared every prompt (no mode inheritance). This is the design precedent my §4 checklist generalizes — but it applies only to the `--mode epic`/`--mode developer` **generated artifact**, not to a raw operator chat prompt.
- **Sampled architect emissions this cycle** (`docs/handoffs/2026-07-18-dev-knowledge-architect/`, `2026-07-18-corp-monorepo-architect/`, `2026-07-17-ai-council-architect-p6-window-completion/`):
  - The dev-knowledge bundle's `SUPPLEMENT.md` ANSWERS (verbatim, `docs/handoffs/2026-07-18-dev-knowledge-architect/SUPPLEMENT.md:35-63`) and hand-authored `PLAN.md` (`docs/handoffs/2026-07-18-dev-knowledge-architect/PLAN.md`) are rich on **strategic intent** (RULING-W/S/PY/CF) but this is the **architect-mode strategic-supplement genre** (HANDOFF_PROCESS §13, six fixed questions: intent/tensions/rejected/open/decomposition/off-repo) — not a build prompt, and it carries **no** Model/Mode/Effort table, no per-task Codex-lane assignment, no per-task deliverable path.
  - **The actual build-shaping artifact — "the operator-approved ARC 4 fleet-equalization prompt file" — is explicitly named as `operator-held, off-repo`** (`PLAN.md:5-9`: *"Source: the operator-approved ARC 4 fleet-equalization prompt file (operator-held, off-repo)"*; `SUPPLEMENT.md:58`: *"The approved ARC 4 prompt file is operator-held (off-repo)."*). It never lands in the tree — structurally unauditable by any repo mechanism, ever, by construction.
  - `docs/handoffs/2026-07-18-corp-monorepo-architect/SUPPLEMENT.md:88` — the ONE Codex-lane mention across all three sampled bundles is a risk caveat, not a per-task assignment: *"Codex lanes terra/sol/luna with quota volatile this week — smoke before relying."* No bundle names which lane reviews which leg.
  - `docs/handoffs/2026-07-17-ai-council-architect-p6-window-completion/SUPPLEMENT.md` — pure strategic frame (three product themes); zero fan-out/worktree/Codex/deliverable content (architect-mode genre, correctly so per §13 — but this confirms none of the three sampled bundles is the genre PLAYBOOK §2's skeleton actually targets).
- **Tonight's mandate (the prompt this probe executes under) as the positive exemplar, contrasted:** it names an explicit worktree (`C:/Users/1028120/.../night-audit-cycle-close`, branch `audit/2026-07-19-cycle-close` — confirmed live via `git branch --show-current`), a fan-out shape (Opus orchestrator · Sonnet/Haiku probe tiers), Codex lanes (sol/terra/luna) in its CONTEXT block, an explicit HARD CONSTRAINTS read-only/write-scope line, an exact deliverable path + naming grammar, and a stream-scoped Investigate list functioning as the plan-mode basis. **It satisfies every item of the §4 checklist below — and it exists only as a live orchestrator instruction, never committed to the repo**, the same off-repo-by-construction pattern as the ARC-4 prompt file.

## 2. Designed/intended shape (per ADR-87 / PLAYBOOK §2)

- **ADR-87 Decision item 2** (line 42-49) is the canonical division of labor, restated verbatim at `protocols/PLAYBOOK.md:242-260` ("The two lifelines" table) — architect: decompose/prioritize · choose MODE · decide parallel/worktree · review+verify · declare closure · off-repo inputs+governance-pointer. CC: pick model · fill skeleton · load code-impact context · load generic gotchas · self-load the rest.
- **ADR-87 item 3** (line 50-53): intent-only is conditional — for **read-only, governance-touching, or gotcha-sensitive** tasks (exactly this audit's class) the thin governance-pointer is **required**, never optional.
- **ADR-87 item 5** (line 60-64): "the mode is the architect's judgment, **with a recorded basis**" — state the mode AND why, pointing to PLAYBOOK §2 "How to choose Mode" (`protocols/PLAYBOOK.md:2293-2298`).
- **HANDOFF_PROCESS §14a item 7** (line 509-513): "**every architect prompt into the lane re-declares MODE** — a lane inherits no mode from a prior prompt" — the strongest existing per-prompt discipline on record, but scoped to epic-lane prompts only.
- **RULING-W, the sanctioned hub→consumer write path** (`docs/decisions/ADR-36-audit-tool-architecture.md:319-361`, amendment 2026-07-18): *"The **only sanctioned write shape** is: consumer worktree/branch → report... Never a direct push into a live consumer checkout."* This is the designed content of the "read-only vs write scope" checklist item whenever a mandate crosses a repo boundary — it exists as doctrine but, per §3 below, nothing structurally confirms a given prompt actually declares it.

## 3. Gap

1. **No mechanism checks the CONTENT of an inbound prompt/brief against any spec — proven by absence, not inference.** `scripts/verify_handoff_probes.py` (header comment, lines 1-8, 36-39) is explicit about its own scope: *"Structurally prove every probe in a v5 handoff bundle's PROBES.md binds to live state... reads PROBES.md + resolves repo paths; writes nothing; never orchestrates."* It validates **CC's own outbound PROBES.md rows** (teeth of an already-generated bundle), never the architect's inbound instruction. `scripts/audit.py:check_handoff_bundle_structure` (lines 568-643) is the only other candidate and it explicitly **excludes v5 bundles by design**: *"Post-#149 flip, v5 is canonical... this check now governs only the HISTORICAL v4 bundles"* (line 571-576) — it regex-checks section-header presence in **v4-stamped** bundles only. Grep of `scripts/` for `def check_` (30 hits in `audit.py`) shows no function that inspects `HANDOFF_BOOT.md`'s purpose field, an `EPIC_BOOT.md`'s FILE-BOUNDARY/MODE section, or any raw operator-prompt text for the §4 checklist items below.
2. **The build-shaping prompt is structurally invisible by design.** Both this cycle's real task-authoring artifact (the ARC-4 prompt file, `PLAN.md:5-9`) and tonight's own mandate are `operator-held`/live-orchestrator text that never lands in the tree. A repo-resident gate — however well-built — has **zero reach** over a prompt that is never committed; the gap is not merely "no gate exists" but "the artifact class the gate would check is architecturally off-repo unless the operator chooses to commit it" (as the dev-knowledge bundle's `SUPPLEMENT.md` does for strategic answers, but never for the raw prompt).
3. **The one general-purpose skeleton (`templates/prompt-template.md`) has no fields for the checklist this audit was asked to derive.** Five tracked version bumps (v1.1-v1.5, template footer) added an obsolescence pass, a READINESS valve, and the governance pointer — never a fan-out/multi-agent section, a named-worktree field (git-workflow only says "branch name follows repo convention," no worktree path), a Codex-lane field, or a deliverable-naming/location field. The template is single-session-shaped; this cycle's actual practice (parallel worktrees, Codex sol/terra/luna review lanes, multi-file audit deliverables) has outgrown it.
4. **§14a's own 7-item checklist has no completeness gate either** — it is a documented template contract (HANDOFF_PROCESS.md prose), not a validated one; nothing in `ALL_CHECKS` confirms a given `EPIC_BOOT.md` actually populated all 7 fields (worktree+branch, FILE-BOUNDARY, MODE+basis, etc.) rather than leaving one blank. The same "prose contract, no teeth" gap S1 found for the intake→ADR citation rule recurs here.
5. **Three BACKLOG tickets already exist in this exact neighborhood, and none of them is this checklist.** `#344` (`BACKLOG.md:23`, NEEDS-RULING) Ask-2 is a consumer-side PreToolUse write-guard enforcing the RULING-W shape — mechanism for the **write-scope** item only, not yet ruled/built. `#353` (`BACKLOG.md:42`, operator-ruled 2026-07-18) is the narrowest and closest: *"refuse a mid-session externally-authored order lacking a worktree/clean-tree declaration"* — but it is scoped to exactly one checklist item (worktree+clean-tree), triggered by a specific witnessed incident (an inherited untracked corp-E5 bundle mid-session), and says nothing about fan-out shape, Codex lane, plan-mode basis, or deliverable naming. `#349` (`BACKLOG.md:41`) is session-**discipline inheritance** (test-then-close), a different axis (close-time, not prompt-content). **None of the three is a content-completeness spec for a prompt/brief as a whole** — this audit's §4 is the first attempt to name that spec as a single checklist.
6. **Codex-lane declaration, specifically, is the weakest-observed item across all three sampled bundles** — it appears exactly once, as a shared risk caveat ("quota VOLATILE, re-smoke") rather than a per-task lane assignment, in a genre (architect strategic supplement) that isn't even the right artifact class for it. No sampled emission assigns sol/terra/luna to a specific review leg ex-ante.

## 4. Proposed MECHANISM — the codified prompt-spec checklist

**Draft PLAYBOOK §2 amendment** (new subsection, positioned after "Structure," before "Quick-reference examples" — additive, does not touch the existing single-session skeleton):

```
### Multi-agent / fan-out prompt checklist (the browser-emitted mandate contract)
<!-- scope: hybrid -->

The Structure skeleton above is single-session-shaped. A prompt that fans out to more
than one agent, worktree, or repo (a night-audit run, an ARC-scale multi-leg mandate, a
parallel-epic dispatch) additionally states these seven items — generalizing HANDOFF_PROCESS
§14a's EPIC-handoff checklist to any multi-agent mandate, chat-native or generated:

1. FAN-OUT SHAPE — how many agents, at which model tier each (Opus orchestrator / Sonnet
   / Haiku, or the t-shirt pins), and whether they run parallel or serial.
2. WORKTREE + BRANCH — the absolute path and branch name for every side-effecting agent
   (or an explicit "no worktree — tree must be clean" fallback declaration; the #353
   boot-contract precedent). No agent acts on an undeclared worktree.
3. READ-ONLY vs WRITE SCOPE — per agent: read-only, or write-scoped to a named
   file/dir set (the §14a FILE-BOUNDARY shape). Any write that crosses a repo boundary
   MUST cite the RULING-W path (consumer worktree/branch → report; ADR-36 Amendments) —
   never an unmediated write into a live consumer checkout.
4. CODEX LANE — which lane (sol/terra/luna), if any, reviews each leg, named per task,
   not as a shared risk caveat; note known quota/availability volatility if applicable.
5. PLAN-MODE BASIS — the MODE (plan / plan-then-auto / auto-accept, per "How to choose
   Mode") AND its basis, declared per agent/lane — no agent inherits a mode from a prior
   prompt (§14a item 7, generalized).
6. DELIVERABLE NAMING + LOCATION — the exact output path(s) each agent must write to and
   the naming grammar it follows (e.g. the ADR-101 `<date>-<class>-<slug>.md` audit
   grammar), stated ex-ante, not left to the agent to infer.
7. CLOSE DISCIPLINE — what "done" looks like for the mandate as a whole: how per-agent
   outputs get consolidated/integrated (serial merge from primary / operator digest /
   `/ship`), and the escalation rule (§14a items 5-6: a genuine fork or boundary breach
   STOPS and returns to the architect — it is never silently absorbed by an agent).

Applies whenever §2 "Decision scope for when to write a formal prompt" already requires a
formal prompt AND the mandate spans more than one agent/worktree/repo. A single-session,
single-worktree prompt stays on the existing Structure skeleton unchanged.
```

**Candidate probe/gate at handoff-time** (not built — proposed shape, mirrors `verify_handoff_probes.py`'s resolve-only, read-only pattern and `#279`'s advisory-WARN precedent, never a fabricated FAIL on a genre that legitimately omits an item):

- A new read-only `audit.py` check (working name `check_prompt_contract`) that fires **only on a committed multi-agent artifact** — an `EPIC_BOOT.md` (already generated, §14a) or an operator-committed mandate file (e.g. a `docs/handoffs/<slug>/PROMPT_CONTRACT.md`, if the operator chooses to commit one, mirroring how `SUPPLEMENT.md` commits strategic answers today).
- For each of the 7 checklist items, scan for a load-bearing marker (a named worktree path, a MODE token, a deliverable path pattern) the way `verify_handoff_probes._LOAD_BEARING` scans PROBES.md columns; an item with a genre-appropriate reason to be absent (e.g. a pure read-only audit has no write-scope to declare) downgrades to WARN, never a blocking FAIL — advisory-first, per the `#279` precedent, until false-positive rate is proven low.
- **Honest limit, stated up front:** this gate can only ever reach a *committed* mandate artifact. The dominant real-world case — a live chat-native operator prompt, off-repo by construction (§3.2) — is out of its reach entirely; the checklist's main near-term value is as an **authoring discipline for the architect** (PLAYBOOK §2 text) and a **structural spec for any future committed prompt artifact**, not a guaranteed catch-all gate.

## 5. BACKLOG seed

**Title:** Codify + gate the multi-agent prompt-authoring checklist (fan-out shape · worktree+branch · read-only/write scope · Codex lane · plan-mode basis · deliverable naming+location · close discipline)

**Description:** Land the §4 draft as a real PLAYBOOK §2 subsection, then build the advisory `check_prompt_contract` probe against any committed multi-agent artifact (EPIC_BOOT.md first, since it already carries 4 of the 7 items per §14a). Explicitly out of scope: gating a live, uncommitted chat-native operator prompt (structurally unreachable — §3.2/§4).

**refs:** ADR-87, HANDOFF_PROCESS §14a, PLAYBOOK §2, `templates/prompt-template.md`, `scripts/verify_handoff_probes.py`, ADR-36 Amendments (RULING-W), #344 (Ask-2 write-guard — the write-scope item's mechanism), #353 (worktree/clean-tree boot-refusal — the narrowest existing sibling), #349 (session-discipline inheritance — adjacent, close-time not prompt-content axis)

**kill-candidates:** none — narrower than and complementary to #344 (Ask-2 is a write-guard mechanism, one of this ticket's seven items) and #353 (worktree/clean-tree boot-refusal, also one item); this ticket is the first attempt at the full content-completeness checklist as a single codified spec, and landing it does not obsolete either narrower ticket — if anything it gives #344 Ask-2's guard-shape design a ready-made checklist to enforce against.

**Done when:** the 7-item checklist is committed verbatim as a PLAYBOOK §2 subsection (byte-checkable against §4 above) AND either (a) `check_prompt_contract` exists as a read-only advisory check wired into `ALL_CHECKS`, scoped to committed multi-agent artifacts, with a passing test proving it flags a missing load-bearing item on a synthetic fixture, or (b) a recorded permanent-defer-with-reason (e.g. "no committed multi-agent artifact class exists yet to gate against" — falsifiable the day one does).
