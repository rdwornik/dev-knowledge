# Residual — 2026-07-19-corp-monorepo-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **architect** (§13) — planning / decomposition posture; the session's WORK is **product**. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/41), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS (the outgoing architect's strategic *why*) fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*. **Read the supplement's TRUST POSTURE line and its five off-file findings — they carry corrections this residual could not derive from the repo.**

---

## §1 — The headline: the E5 build crossed from design into merged code; the frontier is the `#40 → #36 → #55` continuation

**The largest single-window delivery since the A3 ruling landed, and it closed clean.** `witnessed` (READ-ONLY, at derivation): corp `main` is **clean**, **`main` is the only branch** — no open product lanes, no straggler, and **no worktrees registered** (`git worktree list` returns the primary alone). Every lane opened this window was integrated and torn down.

What a fresh architect chat lacks — and the ONLY thing this residual carries — is the **entry point + the decomposition frontier + the design "why,"** none of which the repo re-narrates:

- **Entry point.** Two documents, in this order. (1) The corp **execution charter** `docs/audits/2026-07-17-execution-charter.md` — still the single consolidated reading map (its §2 points at every canonical doc). (2) **New this window and load-bearing:** `docs/audits/2026-07-19-night-consolidation-decision-plan.md` — the N1 night-batch record **plus a large in-file amendment** (the module connection map). Its **§3-EXT start-here plan** is an ordered 8-step lane queue and its **§6 improvement options** table (O1–O9, each sized, NOT-list-bounded) is the decomposition menu. Read it second; everything in §4 below is a pointer INTO it, not a copy.
- **Role split (does not live in the repo).** This browser chat is the **TECHNICAL ARCHITECT** (Layer-1, no file access) — it decomposes the frontier into a task-graph, holds the whole-system view (A3 + `ARCHITECTURE.md`), and reviews each arc's plan before execution (one plan-review output-contract form: the exact CC option / paste-ready feedback / `approve`). The incoming Claude Code session is the **executor** (Layer-3, holds the tree). The architect does **not** execute. Methodology questions route to the **hub** `.dev-knowledge` (corp is A0-closed), **not** this chat.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P6), not in trusting these lines.** This bundle states **no** sha, count, armed-state, verdict, or region text — those are the probes' live answers.

**One standing caveat worth carrying (`witnessed`, from the module-map §7.2):** corp's `ARCHITECTURE.md` **codemap is substantially stale** — phantom import edges, one edge drawn as an import that is actually a subprocess, every runtime data-flow seam missing, and the new `#38` `ops/` modules unreflected. The audit proposes a rewrite scope (§7.3) but **deliberately did not execute it** — it belongs to the A3 R9 rewrite arc, **currently unscheduled**. Treat `ARCHITECTURE.md`'s codemap as an untrusted source until that arc runs; the module-map §5.2 is the witnessed replacement.

---

## §2 — Shipped this window (pointer, not re-narration)

Detail lives in the corp `JOURNAL.md` (newest-first) — not recapped here. The map, by lane:

- **E5 `#38` FR-10 source registry — BUILT and MERGED.** The epic's first build story: `source_registry.py` + `source_value.py` + `source_observation_repo.py` + a `source_observations` table, all pure-Python and **zero Graph calls**. 11 commits on `epic/e5-registry`; **+~80 tests** (`test_ops` roughly doubled). Cleared a **5-pass terra pre-merge review** — 6 P1s, every one a genuine fail-closed/design-invariant gap (silently-empty registry on a misspelled root key; unnormalized stored paths; `operator_prior=exclude` outvoted by arithmetic; silently-dropped unknown `dims` keys; a persistence-layer drop of the gate flag). **`#38` stays OPEN** — its "scout consumes the score" done-when completes at `#40`.
- **S13 documentation archival — SIGNED then EXECUTED** (two sessions, per the ADR-38 contract). `docs/audits/` shrank hard (relocations + signed deletions); `#66`/`#67`/`#68` all closed, story removed per ADR-65.
- **BACKLOG distribution — Parts 1 & 2.** Part 1 decomposed the census into **14 new tasks / 4 new stories** (`#55`–`#68`, `[S10]`–`[S13]`) under existing themes — operator picked "no new themes, no Big Picture edit." Part 2 ratified intake-16 §8.1 (the D1/D3/D4/D5 picks + the *"manual first, automate later; deploy first, iterate"* philosophy) → status **READY-FOR-TECHNICAL**.
- **Ratifications:** SIM acceptance-spec RATIFIED then relocated to `docs/intake/2026-07-18-func-sim-acceptance-tests.md` (taxonomy correction); **ADR-37 Accepted** (frontmatter-canonical + the facts_count projection leg); **ADR-38 Accepted** (deletion/relocation doctrine).
- **Night batch + module map.** N2 fixed `test_cke_paths_resolve` worktree-compat (the basename assertion → a stable pyproject-identity check); N3 filed `#69` (ADR archival). The N1 decision-plan was then completed into the **module connection map** — 8 modules, each verdict witnessed by command or `file:line`, adjudicated against an independent blind `sol` derivation, plus a freshness verdict and a 4/4 cold-reader comprehension probe.
- **One methodology lesson worth knowing (it shaped this window's process):** the **execution-channel discipline** entry in corp `LESSONS.md` (2026-07-19) — a prior session compounded BOTH build channels for the same epic (an in-terminal worktree lane AND a hub developer bundle) without the operator's one-channel pick. That pick is a **contract-authoring-time decision** and belongs to *this* chat when it spawns a lane.

**PENDING — nothing.** `witnessed`: no unmerged product branches, no open worktrees at derivation.

---

## §4 — Next-frontier (the design "why" that travels)

**The architect's job this session is to decompose the next arc within the operator's standing ruling** — *knowledge modules first, decks the NEXT phase*, with **SIM-2** (not SIM-1) as the phase acceptance bar and per-module witnessed sandbox runs (`#34` shape, `docs/intake/2026-07-18-func-sim-acceptance-tests.md` C1–C4/C6) as the acceptance evidence. Three ready frontiers, in the module map's own order:

1. **Finish the E5 epic — `#40 → #36 → #55`.** `#38` shipped the *primitives*; nothing is wired to the system yet. `#40` seeds the three operator golden sources, resolves them to Graph IDs, and scores them; `#36` runs the scout pilot (**day-1 = deterministic `rank_by_value_score`; the bandit is cycle-3+**); `#55` emits the draft Content-Manifest. Only then does the epic finalize. **The `epic/e5-registry` branch and its worktree are gone** — a `#40` lane starts fresh from current `main`, which supersedes the module map's §3-EXT step 1 ("sync the lane forward"). **Graph consent is GRANTED and auth D2 = delegated SSO user token + refresh** (operator charter for this lane) — but see the open question below.
2. **The SIM-1 acceptance gaps — `[S10]` `#56`–`#60`.** The spine runs end-to-end, but the module map's **§5.3 unwired-seams** list names what it costs: body-FTS absent (**the biggest live gap inside the otherwise-wired spine** — body-phrased queries return nothing, which degrades exactly the RFP grounding R10 elevated the knowledge loop to protect), no project↔vault link, index-hygiene duplicates, split path/config resolution.
3. **The `[S11]` RFP intake** — **but its input may not exist.** The module map records that the terrain-recon return branch is **absent from this repo** and must be located elsewhere or treated as not-yet-produced. Do not schedule `[S11]` on the assumption that recon landed.

**The decomposition menu is already written and sized:** module map **§6** options **O1–O9** (body-FTS · ingest cold-start · project↔vault link · `com` revival · `#38` registry wiring · the vault-writer invariant hole · synthesize→vault · Content-Manifest→deck · the ADR-27 doc drift). They are **options, not decisions** — the architect picks and sequences; each is NOT-list-bounded.

> **One menu row is already dead — do not spend a lane on it.** `witnessed` (CC re-derived live at derivation): **O2 / F1 (ingest cold-start) is FIXED**, not open. The module map's §5.3.9 and its O2 row still describe it as a live crash, but `#35` landed the bootstrap + fallback floor (`bootstrap_content_registry` and the empty-fallback path are present in `src/corp/ops/registry.py` on `main`). The audit is stale on this row; the code is the truth. **Generalize the habit, not just the correction:** re-witness any F-number, count, or audit finding at the moment it drives work — this arc alone overturned two census counts, a bundle premise, and this F-row. Two are worth flagging as cheap-and-load-bearing: **O4 `com` revival is ~4 env vars and one filename, zero code**, and **O6 closes a real safety hole** — `copy_to_vault` writes into the protected zone bypassing `write_note`, so the ADR-27 enforcement test **false-greens** and unvalidated notes can enter undetected. One option is explicitly **PARKED per ADR-37(iii)**: the key_facts retrieval surface — do **not** build it until a witnessed post-F6 real-RFP grounding failure.

**The R10 "why" (unchanged, still governing):** after the F0/E1–E2 substrate, the **knowledge loop (E5/E6) takes precedence over the RFP rewrite (E4)** — a conscious, recorded deviation from the intake's "build before gap-fill" order; the BACKLOG sequences themes E1→E2→E3→**E5→E6**→E4→E7 accordingly (theme *ids* keep identity, theme *sequence* carries priority).

**CLOSED — do NOT re-open (charter §3, PROBES P5):** CKE is a subprocess with an explicit contract (R2, one invoker); accessors resolve through config incrementally (R6); the corp↔consumer seam is the T6 Content Manifest; seam contracts are guarded by N2-class seam tests. If an arc's plan reaches for an infrastructure tier (a service, mesh, or bus), the architect rejects it — a violation at 3-RFPs/month scale.

**Operator queue (off-repo — the §13(d) beat captures it live; charter §5 is the verbatim list).** Carried forward and still open: the absent vault git remote, 4 credential rotations, final backup-zone names, the ADR-35 amendment decision (backup leg-2 → personal OneDrive, `#18`), the T6-D4 SharePoint confidentiality push. **New this window** (module map §4-EXT): final **zone names (DR-6/7)** gate `#35`'s renames · run `#69` (the ADR-archival forwarding-marker arc) now or hold · **the ADR-27 §Decision-2 doc drift + the `copy_to_vault` invariant hole — enforce-fix now or schedule to the A3 R9 arc?** · and one the module map left genuinely unresolved: **is Graph auth D2 fully closed by the charter grant, or still jointly dependent on X1's ADR (DR-11 family)?** That last one gates `#40`'s live-resolve leg, so settle it before scoping the lane.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (E1–E7 product story-map in R10 priority sequence, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P3), the live in-progress branches (`git branch -v` — none open at derivation; P2 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **A closed id never returns:** the next-free task id is `max` bracketed `[#NNN]` across **all git history** + 1, not the live-file max (P3's second command). **The anti-bluff PROBES manifest (`PROBES.md`, P1–P6) is the load-bearing carrier: every claim above that could drift has a probe.**
