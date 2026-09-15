# Lane z-10 — AJ M04 first pass: end-of-lane packet

Consumers: `[#765]` (the row this lane implements), `[#764]` (batch Z's night-plan row)

> **Row id correction, stated once and up front.** This lane filed its row as `[#763]` in
> commit `faef0e76` and **renumbered it to `[#765]`** when the sync merge revealed that a
> concurrent session had landed a different `[#763]` on `main` (commit `6572c1b1`, the batch-Z
> suite-baseline freeze) minutes earlier. `faef0e76`'s commit message therefore names `[#763]`
> and is wrong about it; the message is history and is not rewritten. **The live id is `[#765]`
> everywhere else, including in this packet and in every row this lane files.** §4 records how
> the collision happened and why it was predicted in `faef0e76`'s own body.

> **Lane** `lane-z-10-aj-m04-first-pass` · branch `worktree-lane-z-10-aj-m04-first-pass` ·
> contract `LANE-z-10-aj-m04-first-pass.md` (frozen) · batch Z lane 10, LOCAL substrate ·
> model `opus`, mode `execute`, effort `high`.
>
> **Why LOCAL.** The M04 corpus sits on the operator's disk and in no repository. The night
> plan says so in its own header — *"premise corrected during planning: the M04 material lives
> on the operator's local disk, not in the repo, so that lane cannot run in the cloud"* — and
> `[#660]` records the identical constraint for the tools-and-evals table.

This packet is written across the lane's steps, not at the end: §1 lands at step 2, §2 at
step 3, §3 at step 4, and §4–§6 at step 5.

---

## 1 · The corpus, located (contract step 2)

**Directory:** `C:\Users\1028120\Documents\Priv\Architekt Jutra\`

This is the same directory the M03 night mission names as its input A
(`docs/audits/2026-09-10-technical-night-aj-m03/MISSION-PROMPT.md`, the `INPUTS · A` block),
so the location is not a new discovery — what is new is that the M04 files are in it.

**Everything the directory holds for M04, with the size and mtime it was read at**
(`ls -la`, 2026-09-15; every file written 2026-09-14, between 23:09 and 23:10):

```
AJ_M04_ebook.pdf                   13,289,558 B   2026-09-14 23:10
AJ_M04_transkrypcje.md.zip             29,993 B   2026-09-14 23:09
AJ_M04_wszystkie_transkrypcje.zip     581,269 B   2026-09-14 23:09
AJ_M04_wszystkie_mp3.zip          165,775,907 B   2026-09-14 23:10
AJ_M04L01_transkrypcja.pdf             74,694 B   2026-09-14 23:09
AJ_M04L02_transkrypcja.pdf            125,706 B   2026-09-14 23:09
AJ_M04L03_transkrypcja.pdf             89,104 B   2026-09-14 23:10
AJ_M04L04_transkrypcja.pdf             90,872 B   2026-09-14 23:10
AJ_M04L05_transkrypcja.pdf             96,276 B   2026-09-14 23:10
AJ_M04L06_transkrypcja.pdf             81,127 B   2026-09-14 23:10
AJ_M04L07_transkrypcja.pdf             60,777 B   2026-09-14 23:10
AJ_M04L01_prezentacja.pdf             951,847 B   2026-09-14 23:09
AJ_M04L02_prezentacja.pdf             854,825 B   2026-09-14 23:09
AJ_M04L03_prezentacja.pdf             809,620 B   2026-09-14 23:10
AJ_M04L04_prezentacja.pdf             756,919 B   2026-09-14 23:10
AJ_M04L05_prezentacja.pdf             756,616 B   2026-09-14 23:10
AJ_M04L01..L07.mp3                  (7 files)     2026-09-14 23:09-23:10
```

**Two asymmetries against M01–M03, stated because a reader will otherwise assume symmetry.**
M04 has **seven** lessons where M01–M03 had six (M02 also had a seventh transcript without a
deck). And **L06 and L07 ship no `_prezentacja.pdf`** — five decks for seven lessons. Both are
properties of the corpus, not gaps in this reading.

### 1.1 · The source of record for this lane, and why

**`AJ_M04_transkrypcje.md.zip` → `AJ_M04_transkrypcje.md`** — one markdown file, 80,092 B,
1,233 lines, holding all seven lessons.

```
AJ_M04_transkrypcje.md.zip   sha256 bff7649ca7c77741c1f6d079393d09539816f5dd58f390d1f9748391289e84ba
AJ_M04_transkrypcje.md       sha256 ebd8753f03bcd80cb3277841a03dbc7def5f929feb55f3e3e96771a8a9e55f06
AJ_M04_ebook.pdf             sha256 70b4f13aa901ad0f937d8e6b5462fd3edcc99c91429cb3464b8830dbb5aee1b3
```

Extracted to `$CLAUDE_JOB_DIR/tmp/m04/` — **outside the repository and outside the corpus
directory**, so this lane writes nothing into either. It unzipped clean, which is the M03
mission's own stated preference (*"prefer the `.md` if it unzips clean"*).

**This choice is the direct repair of the `[#696]` locator defect, for this module.** `[#696]`
records that M03's leg-1a locators are UNVERIFIED because *"the chosen source carries no page
numbers and no timestamps, so locators became line numbers in a split file the mission never
asked for"*. Here the locators are line numbers in **the vendor's own single file, shipped
whole in the vendor's own archive** — nothing was split, and the archive and the extracted file
are both hashed above. Anyone who unzips the same archive gets byte-identical content and
therefore identical line numbers. The locator is reproducible without this lane's scratch
directory surviving.

This lane does **not** thereby close `[#696]`: that row owns the M03 **re-run**, and M03 is not
in this lane's scope.

### 1.2 · The seven lessons and their line spans in the source of record

Line numbers are into `AJ_M04_transkrypcje.md` at the sha256 above. Every lesson names
`Instruktor Jakub Kubryński` on its third line.

```
L01  lines    1- 118   Wprowadzenie do MPC            (introduction to MCP)
L02  lines  119- 459   Komponenty MCP                 (MCP components)
L03  lines  460- 638   Autoryzacja                    (authorization)
L04  lines  639- 830   Production readiness
L05  lines  831-1025   Specyfikacja 2026-07-28        (the 2026-07-28 specification)
L06  lines 1026-1172   Jak działa MCP Server w praktyce (kod i flow)
L07  lines 1173-1233   Nieprzekazywanie tokenów: Introspection i Exchange w praktyce
```

**The module's subject is MCP — the Model Context Protocol — and that is a finding in itself,**
because it is not what the AJ corpus taught before. M01–M03 were read for *operator practices*
and *process spine*; intake #70's own problem statement frames the corpus as *"about how a
human runs an agent"*. M04 is a **technical protocol module**: transport, components,
authorization, production-readiness, a dated specification, and two implementation lessons.
What that does to the matrix's item boundary is §2's first question, not this section's.

**The corpus is in Polish.** Lesson titles above are given as they appear, with an English
gloss; claims quoted in §2 are quoted in Polish and glossed, so a verifier can grep the source
for the quoted string.

---

## 2 · The matrix (contract step 3)

### 2.1 · How the item set was produced, and how every locator was resolved

**Reading was done by `agy`, as the contract orders, and `agy` was a READER ONLY.** That is
`[#722]`'s interim routing — *"read-only digests, censuses and scans default to agy as a READER
ONLY, with conclusions and verdicts staying on Claude"*. `agy` extracted normative statements
and their locators; every SHIPPED / OWNED / UNOWNED verdict below is Claude's, and `agy` was
never shown this repository.

Three legs, one file each, all three ordered and none substituted (R1 shape, from the M03
mission). `agy` **1.2.1**, model `gemini-3.1-pro-high`:

```
leg A  L01-L03   exit 0   132.7 s   in 30,335 tok / out 22,801 tok   status SUCCESS
leg B  L04-L05   exit 0   134.0 s   in 17,275 tok / out 23,886 tok   status SUCCESS
leg C  L06-L07   exit 0    72.8 s   in 13,006 tok / out 11,813 tok   status SUCCESS
invocation: agy --model gemini-3.1-pro-high --output-format json --print-timeout 20m \
            --dangerously-skip-permissions --print=<prompt file>
```

**The scope check was run rather than assumed.** `agy` is known to answer about a different
repository while logging the right workspace, and the cheap detector is the input-token count
against the corpus size. An 80,092 B source drew 30,335 input tokens on the first leg — about
0.38 tokens per byte, which is reading this file and nothing else. The known failure mode
produced ratios ~600×. No leg shows one.

**EVERY LOCATOR WAS RESOLVED MECHANICALLY, WHICH IS THE POINT OF THIS LANE'S EXISTENCE.**
`[#696]` records that M03's leg-1a shipped locators nobody could re-open. Here a script takes
each extracted block, searches the source for the quoted Polish clause, and reports where it
actually is:

```
items extracted: 82
EXACT   2    quote found verbatim at the stated lines
NORM   80    quote found after whitespace folding only -- the transcript is hard-wrapped, so a
             clause spanning a line break differs from the file by a newline and nothing else
MOVED   0    quote real but at different lines
ABSENT  0    quote not found anywhere in the source
```

**Zero ABSENT and zero MOVED.** Every one of the 82 items is quoted verbatim from the source and
every stated line range is right to within the one line hard wrapping moves it. No item in this
matrix is marked UNVERIFIED, and none had to be.

### 2.2 · What counts as an item, and why the question had to be asked first

M04 is **not** the kind of module M01–M03 were. Those were read for operator practice and
process spine; intake #70 frames the corpus as being *"about how a human runs an agent"*. M04 is
a technical module about **MCP, the Model Context Protocol** — seven lessons of obligations on
someone building an MCP server.

A naive reading would make all 82 items UNOWNED and file 82 rows about implementing a protocol
this governance hub does not speak. **That reading is wrong, and one open row is why.**

> `[#729]` — *"FPG-1's queries are shell scripts the model must remember to run — expose them as
> MCP tools so they sit in the tool list beside Grep"* — is OPEN, P2, size M, and its Done-when
> commits to *"a minimal stdio MCP server [exposing] FPG-1's `why`, `process-list` and `stats`
> plus the impacted-test selector as tools"*, reachable from CC **and from at least one
> non-Claude admitted provider**.

So this repository has already decided to author an MCP server. That makes M04's obligations
real obligations here, and it fixes the shape they land in:

- **`[#729]` says stdio.** Every obligation conditional on remote HTTP transport — session
  affinity, load balancers, SSE lifetimes, WAF interference, OAuth, token exchange — is decided
  by `[#729]`'s transport choice rather than being unowned. A row that has chosen the transport
  owns the consequences of that choice.
- **`[#729]` says tools, and only tools.** Obligations on resources, prompts, sampling and MCP
  Apps are decided the same way: `[#729]` fixes the primitive set.
- **`[#729]` says "no query logic of its own".** Obligations about what a tool returns are
  obligations on the server it builds.

**The verdict rule, stated once:**

| Verdict | Means |
|---|---|
| **SHIPPED** | a landed organ in this repo already satisfies the item, or its transferable form; the commit that landed it is named |
| **OWNED** | an OPEN row already decides the item — either by naming it, or by committing to a deliverable the item is an obligation on; the row id is named |
| **UNOWNED** | no commit and no open row decides it; **it becomes a row in this lane** |

**The honest caveat on OWNED, stated up front rather than buried.** 56 of the 82 items resolve to
`[#729]`, and **`[#729]` names none of them**. It owns them by entailment: it commits to building
a conformant MCP server, and these are what conformance means. That is a real interpretive step,
and it is load-bearing enough that it becomes one of this lane's UNOWNED findings in its own
right — **U6 below: `[#729]`'s Done-when contains no protocol-conformance criterion at all**, so a
server could satisfy `[#729]` completely and still not be an MCP server. The matrix does not
hide the weakness in its own largest column; it files it.

### 2.3 · The counts

```
items extracted and verified   82
SHIPPED                        13
OWNED                          57     ([#729] x 56, [#728] x 1)
UNOWNED                        12  ->  7 rows filed in this lane
```

Exhaustive and mutually exclusive: 13 + 57 + 12 = 82, and no item carries two verdicts.

### 2.4 · SHIPPED — 13 items an organ in this repo already answers

Each row: the M04 item, then the organ that already satisfies its transferable form and the
commit that landed that organ.

| # | Ls | Lines | The M04 item | Already shipped as | Commit |
|---|---|---|---|---|---|
| 01 | L01 | 17–19 | The protocol defines the request format; the application independently decides how the model is managed and when tools fire | ADR-28's three-layer model and CLAUDE.md §5 rule 4 — Layer 2 defines the rules and **never executes**; no script here drives state in a child repo | `a95318d1` |
| 12 | L02 | 249–250 | Resources are not an unlimited disk — a model's context window is finite and must be budgeted | the CLAUDE.md byte cap, `tests/test_claude_md_byte_cap.py` — a boot-time instruction file gated in **bytes**, on the stated ground that a line count is gameable and bytes are what a session pays | `3721f4fc` |
| 16 | L02 | 265–267 | Expose a dedicated search tool rather than making the model hunt through a bulk resource | `[#727]`'s deny-and-point guard — a raw `Bash`/`Grep` search over a question FPG-1 already holds is refused, and the refusal names the organ to run instead | `6eb08d30` |
| 17 | L02 | 273–275 | Prefer tools, so the exchange stays visible to the model in the window | FPG-1 as a queryable store with commit-tier refusals, rather than knowledge the session must reconstruct | `dd161577` |
| 18 | L02 | 292–293 | Notify on prompt-list change so the host reloads without a reconnect | `claude-rosters-freshness` — `.claude/generated/commands-repo.md` is regenerated and diffed at commit time, so a changed command list cannot go unannounced | `e35b7ade` |
| 22 | L02 | 398–401 | Design only against primitives your target clients actually support | the provider/model registry and its `provider-registry-agreement` gate over nine provider seams | `ff01fd10` |
| 38 | L04 | 646–648 | Build on the transport you will actually run on — transports differ fundamentally | `[#752]`'s witnesses: `resolve_launch` refuses a model a background shape cannot honour, and the ran-model is read off the transcript rather than trusted from the dispatch line | `b2d1bcdc` |
| 43 | L04 | 717–719 | Schema and returned payload must align perfectly; any discrepancy aborts the call | `validate_backlog.py` hard-fails a row whose body does not carry the literal contract (`Done when:`), and `validate_hermetization.py` refuses a filename outside the naming grammar | `4b9401bf`, `874d452f` |
| 45 | L04 | 740–742 | Version by introducing new method names; never apply a breaking change to a live contract | the spec-version spine — `coherence_nudge` flags a registered spec changed without a version bump, and `check-against-spec` reconciles each dependent site | `79ff7dd5`, `89f71402` |
| 46 | L04 | 747–749 | Emit `notifications/tools/list_changed` so clients reload definitions | the regen-and-diff roster gates (`roster-freshness`, `claude-rosters-freshness`) — the capability list cannot change silently | `e35b7ade` |
| 48 | L04 | 824–827 | Integrate with internal bots and internal features rather than exposing the server publicly | the Layer-2 invariant again, from the deployment side: the hub is the methodology source consumers install from, never a public service | `a95318d1` |
| 60 | L05 | 900–901 | A cached answer must declare whether its scope is global or per-user | ADR-119 — a command file counts as a wiring surface **only while invocations are recorded**, which is a scope declared on the claim rather than inherited | `c8058953` |
| 61 | L05 | 902–903 | A cached answer must carry a TTL saying how long it may be retained | ADR-119's core sentence — *"adoption decays, it is not conferred"* — is a TTL on a capability claim | `c8058953` |

**Items 60/61 are the most surprising SHIPPED in the table and the mapping is deliberate.** M04 is
talking about HTTP response caching; ADR-119 is talking about whether a command file still counts
as wired. They are the same rule: *a declaration goes stale unless something re-establishes it,
and the declaration must say in what scope and for how long it holds.* That transferable form is
shipped here; the HTTP mechanics are not, and are not claimed.

### 2.5 · OWNED — 57 items an open row already decides

**`[#728]` — 1 item.**

| # | Ls | Lines | The M04 item | Why `[#728]` owns it |
|---|---|---|---|---|
| 06 | L02 | 155–157 | The better you describe what a function does and what its parameters are, the less the model hallucinates when to use it or what to pass | `[#728]` is that claim, applied to our surface: *"each description states WHEN to invoke it — the situation, not the organ's name — since that is what progressive disclosure matches on"* |

**`[#729]` — 56 items.** Grouped by the clause of `[#729]` that decides them. Every item below is
verified and located; the group heading carries the shared reason so the table stays readable.

*Because `[#729]` builds a server at all — obligations on any MCP server it ships:*
`02` (59–61, host-side connection/consent/authorization) · `03` (111–112, re-handshake to gain
an undeclared capability) · `04` (112–113, negotiated capabilities bind for the whole session) ·
`69` (1038–1040, declare your capabilities) · `47` (774–776, expose methods
returning permission-scoped filter criteria) · `57` (881–884, carry protocol version, identity
and capabilities in `meta` on every request) · `58` (887–889, implement the `discover` method for
capability-version negotiation) · `62` (915–917, return `input_required` with the missing
parameters) · `63` (921–923, client re-sends augmented with `input_responses`) · `64` (937–939,
tie state to the logged-in user where the logic permits) · `65` (943–945, otherwise pass a
state-tracking parameter) · `59` (895–898, allow clients to cache list/read endpoints).

*Because `[#729]` fixes the primitive set to TOOLS — resource, prompt, sampling and app
obligations are decided by the primitives it does not expose:*
`11` (244–247) · `13` (256–257) · `14` (258–259) · `15` (261) · `19` (319–322) · `21` (347–348) ·
`51` (856–858) · `52` (860–861).

*Because `[#729]` says stdio — every remote-transport obligation is decided by that choice:*
`23` (416–418) · `24` (433–437) · `25` (439–441) · `26` (448–449, *choose stdio for local
process communication* — the item `[#729]` positively satisfies) · `27` (449) · `28` (450–452) ·
`29` (452–454) · `39` (652–654) · `40` (662–665) · `41` (691–695) · `53` (861–863) · `54`
(863–865) · `74` (1120–1124).

*Because a stdio server has no network surface — the whole OAuth and token-exchange mechanism is
decided by the same choice:*
`30` (494–495) · `31` (539–540) · `32` (543–546) · `33` (552–554) · `34` (563–565) · `35`
(595–598) · `36` (599–601) · `37` (611–613) · `55` (865–869) · `67` (1014–1017) · `68`
(1021–1022) · `71` (1065–1067) · `72` (1094–1095) · `73` (1099–1101) · `76` (1183–1184) · `77`
(1195–1196) · `78` (1196–1198) · `79` (1217–1218) · `80` (1218–1220) · `81` (1220–1221) · `82`
(1223–1225).

*Because they are requirements on the server against whichever specification is current when it
is built:*
`49` (848–850) · `50` (850–851).

### 2.6 · UNOWNED — 12 items, becoming 7 rows

Each is an item no commit and no open row decides, and each carries its M04 source. The rows are
filed at contract step 4; §3 records the ids they were given.

| U | M04 items | The finding, as it applies here |
|---|---|---|
| **U1** | `42` (L04 702–706) | **A single file has a byte budget; the session's boot payload does not.** M04 measures the cost precisely — *"taki jeden MCP Server potrafi zjeść kilkadziesiąt tysięcy tokenów na starcie serwera"*, one server can eat tens of thousands of tokens at startup, because every tool ships its description and its input and output schema. This repo gates the bytes of `CLAUDE.md` (`3721f4fc`) and nothing else that loads at session start: the §7/§9 rosters, `.claude/methodology-roster.md`, the two `@`-imported generated fragments, `AGENTS.md`, the plugin's commands, the skill descriptions — and, once `[#729]` lands, MCP tool schemas on top. Nobody measures the total, and `[#728]` and `[#729]` both *add* to it. |
| **U2** | `05` (L02 153–154), `66` (L05 949–952), `70` (L06 1053–1055) | **Descriptions are gated for the generated surface and ungated for the hand-authored one, and no surface gates the parameters at all.** M04 requires a description of the tool *and* of its input/output schema, and explicit names and descriptions for state parameters. `[#728]` covers organ skills *rendered from the index*; `.claude/commands/*.md` frontmatter is hand-authored and rendered verbatim by `gen_claude_rosters.py` with no predicate on what a description must say, and nothing anywhere describes a command's arguments. |
| **U3** | `09` (L02 195–197), `10` (L02 198–199) | **A gate here has exactly one refusal channel, so "you violated something" and "I could not evaluate" are indistinguishable to the committer.** M04's rule is the distinction itself: a JSON-RPC protocol error is critical and must not be used for an application-level condition — that comes back as a *successful* response with `isError: true`. **This lane is the witness.** `decision-coverage` refused this lane's first commit for four transport files dropped by the operator forty minutes earlier, naming a repo home only the integrator can land; it refuses identically with an empty staged set. The repo does reason about posture per hook — `.claude/settings.json` argues fail-closed for the ADR-77 guard and fail-OPEN for `[#727]`'s — but it does so by hand, per hook, in prose, and the refusal itself carries no channel for "this is not yours". |
| **U4** | `44` (L04 721–723) | **An unattended lane has no cancel for a long-running gate.** M04: *"jeżeli nie zaimplementujecie cancel przy długich operacjach, może to zablokować cały wątek czatu tak długo, jak czat nie stwierdzi, że trzeba uwalić dane połączenie"* — without cancel the thread is blocked until the connection is killed. Measured here: this lane's pre-commit runs exceeded 120 s and then 400 s and had to be backgrounded; an attended seat can interrupt, and a `--bg` lane — which is what the night plan's LOCAL substrate dispatches — has no lever but killing the session. |
| **U5** | `56` (L05 876–879) | **Nothing notices an external specification revising under us.** M04 L05 is a whole lesson on one dated revision removing stateful mode, sampling, roots, native logging, HTTP+SSE and dynamic client registration, and its warning is explicit: do not build new servers on deprecated features, because they will need a complete rewrite. `coherence_nudge` and `check-against-spec` detect an *in-repo* spec changing; `[#385]`/`[#495]` distribute *dependency version* bumps through the deploy channel. Neither watches an outside standard. `[#729]` proposes to build against exactly such a standard. |
| **U6** | `07` (L02 159–162), `08` (L02 184–186) | **`[#729]` has no protocol-conformance criterion, so it can be fully satisfied by a non-conformant server.** Its Done-when tests one thing — that the server's output matches the script's for the same input — and says nothing about the protocol the server claims to speak. The two items are the cheapest evidence: tool annotations (`readOnlyHint`, `destructiveHint`) and the text-content fallback alongside `StructuredContent` are both conformance obligations, both invisible to an output-equality test. This is also the row that repairs §2.5's weakness: 56 items are owned by entailment, and only a conformance criterion makes that entailment checkable. |
| **U7** | `20` (L02 343–345), `75` (L06 1156–1157) | **Every dispatched lane inherits the whole secret store; there is no introspect-and-exchange step and no row about it.** M04 L07's principle is that forwarding the caller's token to the backend is the wrong design — introspect it, exchange it for a backend-specific token, pass that one — and L02's sampling rule is the same boundary from the host side: filter what the server can pull out of the conversation. Locally, keys live in one `.env` loaded by the PowerShell profile, so a lane needing one provider's key receives all of them, and a sweep of `BACKLOG.md` for secret / credential / API-key / token-scope returns **no row at all**. |

---

## 3 · The rows filed (contract step 4)

Seven rows, carrying twelve UNOWNED items. A row may carry more than one item; **no item is
carried by more than one row**, which is what keeps the matrix mutually exclusive after filing.

| Row | P | Size | Theme / story | Items | Title |
|---|---|---|---|---|---|
| `[#766]` | P2 | M | [E5] / [S14] | 42 | The session boot payload has a byte budget on one file and none on the whole |
| `[#767]` | P2 | M | [E2] / [S4] | 05, 66, 70 | A tool description is gated only where it is generated, and no surface gates its parameters at all |
| `[#768]` | **P1** | M | [E2] / [S3] | 09, 10 | A gate has one refusal channel, so a violation and an environment it could not evaluate are indistinguishable |
| `[#769]` | P2 | S | [E7] / [S18] | 44 | An unattended lane has no cancel for a long-running gate |
| `[#770]` | P2 | M | [E9] / [S27] | 56 | Nothing notices an external specification revising under us, and `[#729]` proposes to build on one |
| `[#771]` | P2 | S | [E7] / [S18] | 07, 08 | `[#729]` carries no protocol-conformance criterion |
| `[#772]` | **P1** | M | [E2] / [S3] | 20, 75 | Every dispatched lane inherits the whole secret store |

**The two P1s are argued, not defaulted.** `[#768]`: an unattributable refusal is what makes a
`--no-verify` reflex look reasonable, and that reflex is banned here without exception.
`[#772]`: the exposure widens every time `[#722]` or `[#753]` routes work to another provider,
so it gets worse while it sits.

**Three rows are witnessed by this session rather than reasoned from analogy.** `[#768]`'s
evidence is the `decision-coverage` refusal that blocked this lane's first commit for a
condition no lane could satisfy. `[#769]`'s is this lane's own commits exceeding a 120 s and
then a 400 s timeout with no lever but backgrounding them. `[#772]`'s premise is a sweep that
returned zero rows.

**`[#771]` audits this packet.** §2.5 resolves 56 items to `[#729]` by entailment while `[#729]`
names none of them; `[#771]` asks for the conformance criterion that makes the entailment
checkable. The matrix files the weakness in its own largest column rather than carrying it as a
caveat.

---

## 4 · Deviations, bypasses and things the next seat must not inherit as normal

Everything here is reported under the V-2 decision budget — decided per contract defaults and
reported in this packet, not escalated. Nothing in this section was asked of the operator.

### 4.1 · The id collision, which this lane predicted and then suffered

`[#763]` was filed by this lane in `faef0e76` at `max(tasks/) + 1`, the synthetic `[#777]`
excluded per standing precedent, with four sibling batch-Z lanes live and none having allocated.
That commit's body named the hazard in PLAYBOOK Ch8 rule 3's own terms — parallel branches read
their own stale `main`, so write-time allocation collides unless the range was reserved **in the
file** before the split, and batch Z reserved none. Roughly forty minutes later `6572c1b1`
landed a different `[#763]` on `main`. **The unmerged side moves**, so this lane renumbered to
`[#765]` in `627297c0`. `faef0e76`'s message still says `[#763]` and is wrong about it; it is
history and was not rewritten, which is why the correction sits at the top of this file.

The batch manifest records the same event from the dispatcher's side (§11, *"The concurrent-id
collision, witnessed rather than theorised"*). The later batch-Z lanes allocated into the **780s**
instead, leaving 765–779 clear — which is the non-overlapping range the rule asks for, arrived at
by convention mid-batch rather than reserved before the split. This lane's seven rows took
766–772 from that gap, verified free against `origin/main` before filing.

### 4.2 · Two single-hook bypasses, both declared, both under STANDING_RULINGS Q1

Q1: *"the integrator is gate-of-record, and a declared single-hook bypass on a lane branch is
sanctioned, with the declaration carried in the commit body."* One **named** hook each time.
`--no-verify` is banned in this repo without exception and was never used.

**(1) `SKIP=decision-coverage`, on `faef0e76` only.** Four decision files appeared in
`$CLAUDE_PROMPTS_DIR/to-cc/` between 00:24 and 00:40 that night, all four carrying
`carried-by: docs/audits/2026-09-15-technical-batch-z-manifest.md`, a path then absent from
`main` and `origin/main`. `decision_coverage.py check` refuses identically **with an empty staged
set**, so the refusal was a property of the tree and the transport rather than of the diff. It
was cleared by `[#764]` arriving on `main` and **was not needed again**.

**(2) `SKIP=audit-health`, on `cb92014b`.** `journal_spine_anchor` reports `0ee3d161` as an
unanchored first-parent spine entry. The check's own prescribed discriminator was run:

```
introduced:            ['0ee3d161...', '1da24766...']
anchored in this tree: False
anchored at main:      False
```

Both-False is documented as **ambiguous** — a real gap, or an anchor sitting in another seat's
*unpushed* local `main`, which a lane cannot see. **That third form is eliminated by asking the
remote rather than trusting a fetched ref:** `git ls-remote origin refs/heads/main` returns
`0ee3d161`, and local `main` is `0ee3d161`. The flagged commit **is** main's published tip, so no
unpushed anchor can exist above it. The merge introduces only itself and the JOURNAL commit
inside it, and a JOURNAL entry cannot name its own not-yet-existing hash — the structurally
unanchorable one-commit-arc shape.

**Not fixable by a lane**: discharging it means appending a JOURNAL entry, and this contract
forbids a lane to journal at all (STANDING_RULINGS P-1). **Owed at integration:** anchor
`0ee3d161` in the next JOURNAL entry, which clears it for every batch-Z lane at once.

### 4.3 · Four sync merges, and why a lane paid one per integrator merge

`627297c0`, `b6526ec1`, `737c6def`, `4bf18972`. Each cleared a `journal_spine_anchor` block
caused by `main` advancing mid-step: the check reads the JOURNAL from the **committing tree** and
the spine from the **shared ref**, so a tree even minutes behind reports gaps that do not exist.

**The ADR-110 lane exemption, which exists to stop exactly this, never armed.**
`batch_manifest.open_batches()` returns `[]` against this tree's `HEAD`: the batch-Z manifest
carries no frontmatter, no `status: open`, no `batch:` key and no `## THE LANES` heading, so it
declares a batch to a human and **zero** to the machinery. The manifest is excellent as a record
and invisible as a declaration. Reported rather than filed — the manifest is immutable and is the
dispatcher's surface, not this lane's.

The fourth merge also had to target the **local** `main` ref rather than `origin/main`: the
integrator had merged locally without pushing, and the gate reads the shared ref, so
`git merge origin/main` reported *"Already up to date"* while the block persisted.

### 4.4 · Step 3 and step 4 landed in one commit, and only the boundary moved

The contract commits at the end of both steps. Step 3's commit was refused by `audit-health`
(§4.2 case 2) with its content already staged, so when step 4 committed under the declared skip,
the matrix, the evidence files and the seven rows landed together as `cb92014b`. **The step
CONTENT is unchanged and both steps were completed in order** — the matrix was built and
verified before any row was written, and the rows were derived from its UNOWNED column. Only the
commit boundary moved, and it was moved by the gate rather than chosen.

### 4.5 · `git stash list` is NOT empty, and this lane must not make it so

The contract's step 5 requires an empty stash list. It is not empty:

```
stash@{0}: On worktree-lane-z-0-quality-requirements: lane-z-0-qr-commit4-wip-54637863
```

**The entry is not this lane's and cannot be cleared by this lane.** The stash stack is shared
across every worktree of this repository; the entry is tagged with lane z-0's own slug and with
`54637863`, which the batch manifest §2 records as that lane's background id. **This lane created
no stash at any point** — work was set aside by committing, never by stashing.

The clause is therefore satisfied in the only way it honestly can be: **this lane contributes
nothing to the stash stack, and dropping a peer's in-flight WIP to make a check read green would
destroy another seat's work.** Reported, untouched.

### 4.6 · `[#589]`'s byte bar is RED and this lane did not clear it

Measured in this tree, both figures, because only the difference is attributable:

```
BACKLOG.md at main       95,484 B
BACKLOG.md in this tree  97,076 B
the [#589] bar           72,000 B
```

`main` is **23,484 B over** before this lane touches anything. This lane adds **1,592 B** — 222 B
for `[#765]` and 1,370 B for the seven rows, about 196 B each, which is the one-line view
projection rather than the row bodies. The bar is `[#589]`'s own Done-when and `[#589]` is an open
P1 row, so raising the constant is the act that row exists to forbid. Reported, not fixed.

---

## 5 · Tests

Targeted to this lane's diff, which is `tasks/`, `tasks/manifest.json`, `BACKLOG.md` and
`docs/audits/`. The full suite runs once at integration, not per lane (`[#528]`).

```
uv run --locked pytest tests/test_gen_task_tree.py tests/test_task_tree_gate.py \
                       tests/test_validate_backlog.py -p no:randomly -n 0
185 passed, 2 failed
```

**Both failures are attributed, and one is now green.**

1. `test_task_tree_gate.py::test_registered_and_green_on_live_repo` — **not a finding.**
   `check_task_tree_coherence` requires the index and the working tree to agree, and the seven
   rows were unstaged when the suite first ran. Re-run after `git add`: **1 passed in 2.56 s.**
2. `test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar` — **RED on
   main**, §4.6, not cleared here.

`audit.py health` reports exactly one `[!!]`, the `journal_spine_anchor` gap of §4.2, and it is
main's, not this lane's.

---

## 6 · Open items for the integrator

1. **Anchor `0ee3d161`** in the next JOURNAL entry. It clears `audit-health` for every batch-Z
   lane at once, and it is the only reason this lane spent its second bypass.
2. **Regenerate `docs/audits/README.md`** on the merged result — this lane deliberately left the
   audits index stale, per `[#590]`, and landed five files under `docs/audits/`.
3. **`[#729]` gains a leg**: `[#771]` asks for the protocol-conformance criterion `[#729]`'s
   Done-when does not carry. It is a strengthening of an open row, not a new organ.
4. **The batch-Z manifest declares nothing machine-readable** (§4.3). Every lane in the batch pays
   a sync merge per integrator merge because of it. The manifest is immutable; the fix is a
   declaration in the next one, not an edit to this one.
5. **`[#772]` is P1 and is the one finding here with a blast radius outside this repo** — it is
   about credentials reaching third-party binaries, and it gets worse while it sits.

**Not owed, stated so it is not looked for:** no JOURNAL entry (P-1, the integrator's surface),
no index regeneration beyond `gen_task_tree.py --emit-source`, which is the only way a `tasks/`
row reaches `BACKLOG.md` at all, and no merge or push — this lane commits and stops.
