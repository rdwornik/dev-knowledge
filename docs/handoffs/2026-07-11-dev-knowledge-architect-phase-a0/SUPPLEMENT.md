# Architect strategic supplement — 2026-07-11-dev-knowledge-architect-phase-a0

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-11

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

ANSWERS — outgoing architect, 2026-07-11 (session: hermetization rollout + fleet consolidation)

1. STRATEGIC INTENT — Shift from rollout-posture to WORKABLE-CONSUMERS posture. The operator's goal function, verbatim intent: he must be able to do daily PRODUCT work in corp-monorepo and ai-council — a large product backlog waits in both — without risk that the methodology layer breaks under him. Phase A0 (template consolidation) is the unblocker, not an end in itself. Its exit therefore has TWO legs: (a) the three repos conform to one settled template (every divergence at parity or declared in .methodology.yaml), and (b) the OPERATIONAL MINIMUM is verified working per consumer — hooks, skills, commands, and handoffs each WITNESSED functioning (the session's doctrine: presence ≠ enforcement ≠ usable). Only after (b) may the session declare "the operator can work here today." SIEM/maintenance (Phases A1→E) then builds in parallel with product work, never blocking it.

2. TENSIONS WEIGHED — (a) checker-first vs template-first: landed template-first (A0 before #328) — a checker built against unsettled rulings chases a moving target; the operator re-sequenced and the architect concurred. (b) byte-parity vs declared-divergence: landed declared — universalization means every difference explicit and machine-readable, not identical bytes (assets/, ruff, /handoff prove the pattern). (c) rollout speed vs carrier quality: held all session — fixes before arming (#318/#319 before v1.3.1), tag-ancestry verified before every consumer arm. (d) manual-now vs mechanism-later: manual A0 sanctioned as a ONE-TIME pass; recurrence prevention is A1's checker — manual hygiene as a routine was rejected. (e) ceremony vs lane: AI Council deferred until Phase-E requirements reveal a genuine fork (pull-vs-push telemetry is the likely one); debating without requirements = manufactured ceremony.

3. CONSIDERED + REJECTED (do not relitigate) — full SIEM stacks (Grafana/Loki/ELK): oversized for a single-operator fleet, kills hermetization; posture = libraries-not-platforms (JSONL + SQLite/DuckDB-class + one viewer). Mermaid C4-syntax: experimental, style-fixed, GitHub won't render — rejected permanently. Structurizr/model-layer adoption now: no multi-view need; pre-selected candidate IF that need materializes. Filling CLAUDE.md prose gaps during marker grandfathering: rejected — marker-only, byte-identical; reconciliation is its own pass. Adding generate-hooks to the carried install list silently: rejected — consumer-behavior change needs its own ruling (#323). Deleting audits/files without operator verb-ruling: never. A second owner-map copy in .methodology.yaml: rejected — markers ARE the map; yaml holds waivers only. Relative-path hub pin (../.dev-knowledge): rejected — GitHub URL + tag is the one fleet convention. Propagating corp's _AUDIT_ uppercase to a third repo before the naming ruling: rejected — hub lowercase is the interim default.

4. OPEN QUESTIONS — The seven A0 rulings (operator, in-session): audit-filename convention winner (+ rename plan gated by ADR-100 referential-currency scan); ONE ruff-config form of the three; .vscode carried-vs-local; consumer BACKLOG story-map schema (#331); command-roster target (codex-review leftover, evolve, /save #325); CLAUDE.md archived-reference cleanup (#330; archived → templates/archive); remaining register rows. Deferred by design: Phase-E observability requirements (pull-vs-push, retention, what consumers expose — Council IF forked); Codex-producer first pilot task assignment (candidate: a bounded A1 build); .github CI fleet-generic or local; #327 protocols-as-interface genre wording; the v1.4.0 toc-hooks re-scope shape (re-key to PLAYBOOK-class surfaces vs remove from generic set). System-architecture visualization stays deferred wholesale (intake #10 is the reopen input).

5. DECOMPOSITION RATIONALE — A0 (settle template, verify operational minimum) → A1/#328 (encode it as the fleet_parity checker + JSONL event emission, least-commitment) → B (#324 nightly routine + morning prompt) → C (manifest v1.4.0: #315 INSTALL carrier, toc re-scope + waiver RETIREMENT, /save #325 — the system's first self-cleaning) → D (manifest consumers: #329 VS Code colors generated-not-hand-set, #331, #330, #327) → E (requirements-first observability, Council gate) → F (EPIC-H doctrine + Codex variant-routing, evidenced by this session). Do NOT redo or re-decide: the fleet-parity register and its accepted verdicts; the ownership-manifest tiers (intake #12, promoted by A0); today's fork rulings (marker-only grandfathering, GitHub-URL+tag pin, assets LOCAL, A5 drop-claim, §9a hub-included, §9b advisory-v1); the v1.3.1 rollouts and their evidence; the tag-ancestry rule; the #326 legs (hub ToC done, ai-council verified no-op, corp converted).

6. OFF-REPO CONTEXT — Operator priority is unambiguous: A0 is P1 because it unblocks product work he has been unable to start; the consolidation frustration ran ~20 sessions and is now fully registered (fleet-parity register + browser-side architect memory) — treat any regression as P1. The plan-of-record lives IN-TREE as intake #13 (v3) — the incoming session's comparison baseline; no operator-held documents remain (the morning's plan-of-record lesson is closed). Codex 5.6 sol/terra/luna availability stands confirmed (CLI selector = availability; config pin = default). CC-side gotcha captured in its private memory: PowerShell tool scanner can false-block commits whose MESSAGE mentions rm-like tokens — use git commit -F <file>. Two pre-existing branches intentionally untouched and carried as open items: hub automation/fleet-audit (data-branch organ) + docs/file-arch-cc-facing-ruling (verify status), corp docs/backlog-transcript-mime-fix.
