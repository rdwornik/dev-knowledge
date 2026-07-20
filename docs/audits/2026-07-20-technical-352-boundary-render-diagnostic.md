# [#352] clause (f) — reader-visible boundary render diagnostic

Render-lane diagnostic · ADR-101 class `technical` · read-only investigation; no repo file mutated to produce it

**render-status: PREDICTED / PENDING-ADOPTION — NOT WITNESSED.**
Clause (f) is witnessed by the operator's eye in a **consumer repo**, and cannot be witnessed
until the editor-config adoption lands there (§5). This stamp flips to `WITNESSED` only on that
eye, in a later commit — and records a failure honestly if the render is wrong.

## 1. What this document is

Evidence of a gap. It records a real defect found while diagnosing why the reader-visible
ownership boundary does not render, **and** the correction of a wrong witness target that would
have produced a meaningless green.

It is **not** a build plan. The vehicle for the fix is decided by a buy-vs-build fleet-template
ADR (intake pending, filed separately). Nothing here authorizes a bespoke implementation.

## 2. The wrong witness target — corrected

The original diagnostic prompt directed the investigation at the **hub's own** `CLAUDE.md`
(`.dev-knowledge`). That target was wrong, and the operator caught it.

**The hub is entirely methodology by definition.** There is no repo-local content there to
contrast against hub content, so grey/navy decoration in the hub is a near-single-colour wall
that demonstrates nothing about a *boundary*. A green witness in the hub would have been
worthless — it would have shown decoration working while proving nothing about the thing clause
(f) exists to make visible.

**The operator's actual, repeatedly-stated need is to see the boundary in a CONSUMER repo** —
`corp-monorepo` or `ai-council` — where hub methodology sits directly beside repo-local content
and the contrast is the whole point.

## 3. Phase A findings — factually correct, scoped to the wrong repo

All four findings below were measured against live state and stand as fact. They describe the
**hub**, which §2 establishes is the wrong witness surface. They are retained because they are
true and because finding 3.1 was a genuine blocker that had to be cleared regardless.

### 3.1 Extension not installed — TRUE, and now RESOLVED

`fabiospampinato.vscode-highlight` was absent from `C:\Users\1028120\.vscode\extensions`; the
same-publisher `fabiospampinato.vscode-open-in-application-2.3.0` was present, suggesting a wrong
pick from the extension picker. `.vscode/extensions.json` states the dependency outright: *"VS
Code core has no mechanism to paint arbitrary line ranges from settings alone."*

**Now resolved** — `fabiospampinato.vscode-highlight-2.1.0` is installed in the user-global
extensions directory, so it is available in **every** folder, consumers included.

**Necessary but not sufficient**, and not the operator-visible defect. See §4.

### 3.2 Hub markers present — TRUE

All 15 Form-A regions present in the hub `CLAUDE.md`, worktree and primary identical, with the
generated `> **[HUB - methodology]**` / `> **[REPO - local]**` headers immediately preceding each
start marker.

### 3.3 Open mode — bare folder, not the broken node

No `.dev-knowledge.code-workspace` exists in either tree (the `//repo-personal-sort` comment in
`.vscode/settings.json` still references it — a stale reference, unfiled). Folder-mode **does**
load `.vscode/settings.json`, which carries the decoration config.

### 3.4 Hub regexes match — TRUE, 15/15

Executed with Node against the real file, flags `gm`: 8 `owner=hub` (grey) matches, 7
`owner=repo` (navy) matches, `filterFileRegex` true for both patterns. Colours match the v2.44
architect ruling: hub = grey `rgba(140,140,140,0.16)`, repo = navy `rgba(38,79,140,0.30)`.

### 3.5 A sufficiency claim, corrected

An earlier draft claimed the fix was "zero repo diff, machine-local install only" while also
finding that the hub's §7/§8 runtime lines fall outside the roster regions. Both could not be
acted on. Resolved by mapping every regex match back to line numbers: the install alone does
**not** paint hub `CLAUDE.md:119,120,122-124,133,137,140-145`; only `:126-131` and `:147-154`
band navy. Operator-ruled 2026-07-20 that this §7/§8 gap is **out of clause (f)'s scope** — those
runtime lines are not marker-owned boundary material, and painting them would be a #312
marker-substrate change. Filed as the open question [#370]; **no owner nominated**.

## 4. THE REAL DEFECT — consumer write-through declared but never built

**Both consumers carry a near-empty `.vscode/settings.json` with zero highlight keys:**

```
corp-monorepo/.vscode/settings.json   77 bytes   highlight keys: 0
ai-council/.vscode/settings.json      72 bytes   highlight keys: 0
```

Each contains only a `files.watcherExclude` block. Neither carries `highlight.regexes`,
`highlight.regexFlags`, or an `extensions.json`.

**Consequence:** the extension is now installed user-global and *does* activate in a consumer
folder — and finds **nothing to read**. Zero decoration. No further installing can fix this;
the config is per-workspace and it is not there.

**This was declared, not accidental.** `deploy/manifest-v1.4.0.yaml:325` carrier `editor-config`,
`implemented: false`:

> "the hub half is built and the material is declared fleet-owned here, but no carrier module
> writes it to a consumer … the consumer write-through is the next ticket, because both
> consumers already track a `.vscode` of their own (2026-07-12) and a clobbering write would
> break ADR-93 single-writer-per-file."

W1 shipped the hub half and the declaration. The consumer half was deferred to "the next ticket"
and **was never filed**. The gap therefore sat declared-but-unbuilt and untracked — which is why
it survived roughly twenty sessions of the operator asking to see the boundary.

## 5. Consumer readiness — everything else is in place

Both consumers are ready to render the moment the config arrives. Markers are present with
**both** owner values, so the contrast that makes the boundary meaningful genuinely exists:

```
corp-monorepo   CLAUDE.md 240 lines    9 owner=hub / 14 owner=repo markers
ai-council      CLAUDE.md 251 lines    9 owner=hub / 16 owner=repo markers
```

Running the hub's real regexes against the consumers' live `CLAUDE.md` files:

```
corp-monorepo   HUB(grey)  8 matches   REPO(navy) 13 matches   filterFileRegex -> true
ai-council      HUB(grey)  8 matches   REPO(navy) 15 matches   filterFileRegex -> true
```

21 and 23 banded regions respectively, both colours interleaved through the file. **That is the
render the operator has been asking to see**, and it is blocked solely by §4.

## 6. ADR-93 constraint — MERGE, never clobber

Recorded verbatim from the manifest, because it is the reason this cannot be a blind copy:

> "both consumers already track a `.vscode` of their own (2026-07-12) and a clobbering write
> would break ADR-93 single-writer-per-file."

**Any write must MERGE the highlight keys into the consumer's existing `files.watcherExclude`
block, never overwrite the file.**

### 6.1 Open question for the ADR — investigated, answered

*Is that `files.watcherExclude` block fleet material or repo-local?*

**Answer: fleet material by operator ruling, but UNDECLARED in machine-readable form.** Evidence:

- The value is byte-identical across all three repos: `"**/.claude/worktrees/**": true`.
- The consumer commit that introduced it says so explicitly —
  `ai-council 2707d73 "chore(vscode): carry hub files.watcherExclude for .claude/worktrees (fleet ruling)"`.
- **But** `grep -rn watcherExclude deploy/ ecosystem/` returns **nothing** — it appears in no
  manifest artifact list and no parity-surfaces row.

So the consumer `.vscode/settings.json` already holds hub-originated fleet content that no
machine-readable declaration covers. **This matters to the fleet-template ADR**: the merge target
is not neutral repo-local config, it is undeclared fleet material, and the ADR should decide
whether `watcherExclude` becomes a declared artifact alongside the highlight keys rather than
remaining a ruling-only carry.

## 7. Witness protocol — consumer, ai-council first

Clause (f) will be witnessed in a **consumer**, never in the hub (§2).

**Order — operator ruling: `ai-council` FIRST** (smallest repo, the proof-of-adoption surface),
`corp-monorepo` second. Both only **after** the fleet-template adoption lands the editor-config
in the consumer.

When that has landed:

1. **Open `CLAUDE.md` via the editor tab (the file-name tab), NOT the Markdown Preview pane.**
2. **Confirm the right-gutter overview ruler shows grey/navy ticks.** If the ruler is bare,
   either the extension did not activate **or** you are in preview — **rule out preview first**,
   then check activation logs. **Do not touch config.**
3. Only then confirm the interleaved grey (`owner=hub`) / navy (`owner=repo`) bands — 23 regions
   expected in `ai-council`, 21 in `corp-monorepo` (§5).

If the render is wrong, **stop** — do not edit markers, regexes, or `.vscode` speculatively.

## 8. Follow-on

- **[#371]** — consumer editor-config write-through. **Vehicle decided by the buy-vs-build
  fleet-template ADR (intake pending); do NOT implement bespoke.** Same
  vehicle-subject-to-ADR pattern as R7.
- **[#370]** — is the `owner=hub` / `owner=repo` ownership model two-state-complete, given a
  third content class (`~/.claude/` user-level surfaces) demonstrably exists? No owner nominated.
- **[#369]** — pre-existing, unrelated: wire `boundary_headers.py --check` into pre-commit.

## 9. Status ledger

| Item | State |
| --- | --- |
| Phase A findings (hub) | MEASURED — true, but scoped to the wrong repo |
| Witness target | CORRECTED — consumer, not hub |
| Extension installed (user-global, 2.1.0) | RESOLVED — necessary, not sufficient |
| Consumer write-through | **THE REAL DEFECT — declared `implemented: false`, never built, never ticketed** |
| Consumer markers + regex match | VERIFIED READY (21 / 23 regions) |
| `watcherExclude` provenance | fleet-by-ruling, UNDECLARED in manifest/parity |
| §7/§8 runtime lines | OUT of clause (f) scope — operator-ruled 2026-07-20 |
| Post-adoption render | **PREDICTED — awaiting the operator's eye in ai-council** |
| Clause (f) | **OPEN** — not closed by this document |
