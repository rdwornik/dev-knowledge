# DM-4 — does a local vector index beat grep? Measured at 11/20 vs 2/20, and the pairing the question asked about was never reachable

> **PROVENANCE — harvested cloud artifact, body VERBATIM below this header.**
> Lane `lane-h-8-local-memory-tier-l-evaluation` (batch E, DM-4), receipt id
> `cse_01SHFSuLrRTLfraAwUtuqBqC` — G1 created / G2 bound `git_repository` / G3 first-assistant
> text at 72 s. Dispatched 2026-09-01 00:12 on `sonnet` per R-MODELS, harvested 03:07.
> Contract: `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-h-8-local-memory-tier-l-evaluation.md`.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** `[#614]` (batch E's frozen execution arc) and architect ruling **CUT-4**,
> which downgraded this from Tier-S build to Tier-L evaluation and owns its verdict. ADR-112's
> Tier-L bar applies: **the evaluation IS the deliverable**, and a negative result is a result.
>
> **THIS LANE WAS READ-ONLY BY CONTRACT** — zero tree writes, zero commits, zero rows. Confirmed
> at harvest: `git status --short` clean in its own clone.
>
> **THE HEADLINE, and its caveat is load-bearing.** `grep@5: 11/20 (55%)` against
> `hashed-vector@5: 2/20 (10%)` — grep wins clearly. **But `model2vec`, the embedder CUT-4's
> question actually names, was never reachable**: this session's egress policy answered
> `403 to CONNECT` for `huggingface.co:443`, twice, non-transient, and the lane reported the
> blocked host rather than routing around it. It substituted a network-independent hashed TF-IDF
> vector so the question got a real number, and says in its own §6 that **the original CUT-4
> question is still open**. `sqlite-vec` itself is not implicated and was proven working — 34,033
> real vectors, KNN cross-checked against independent NumPy brute-force L2 and matching exactly.
>
> **PERSIST NOTE (integrator, 2026-09-01).** The harvest tool reported its own deviation —
> *"the report does not open with its own heading — the first heading is line 5"* — which is
> precisely the shape the audits index renders as `(no # title)`. This header supplies the `# `
> line the body lacks. The two organs agree: `Harvest-Cloud` warns at persist time and
> `gen_audit_index --check` refuses at commit time, which is the mechanism landed hours earlier
> at `5069ce5f` meeting its first live harvested artifact.

---

Repo tree is untouched, as required by write-scope NONE. Here is the final measurement.

---

## lane-h-8-local-memory-tier-l-evaluation — measurement report

### 1. Scratch environment

Built entirely off-repo, in this session's scratchpad (`/tmp/.../scratchpad/venv-lane-h8`), a fresh Python 3.11 venv. Nothing installed into the repo's declared environment; `pyproject.toml`/`uv.lock` untouched (verified: `git status --short` clean).

Installed: `sqlite-vec==0.1.9`, `model2vec==0.9.0` (attempted, see §2), `wordllama` (attempted, see §2), `numpy`.

### 2. Refuted premise — record per Q10, disclosed before deviating

The brief's starting pairing is sqlite-vec + **model2vec**. `model2vec.StaticModel.from_pretrained(...)` requires fetching pretrained weights from `huggingface.co`. This session's egress policy denies that host outright: `curl .../__agentproxy/status` shows `recentRelayFailures` with `"kind": "connect_rejected"`, `"detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)"` for `huggingface.co:443`, twice, non-transient. Tried the same for `wordllama` (a non-rejected PyPI-installable static embedder) — same wall, same host.

Per the agent-proxy's own instructions ("do not retry or route around it — report the blocked host"), I did not hunt for a mirror. **This refutes "model2vec is reachable in this scratch env" as a premise.** sqlite-vec itself is not implicated — see §3.

**Decision (per-contract default, not an escalation class):** rather than PAUSE with zero measurement, I substituted a network-independent embedder — a deterministic hashed TF-IDF sparse vector (stdlib `hashlib` + `numpy`, no pretrained weights, no network) — so the actual question the lane asks ("does a local vector index beat grep") still gets a real number. This is a disclosed deviation, not an endorsement of this embedder as an adoption candidate.

### 3. sqlite-vec — actually proven this time

Loaded via `enable_load_extension`, ran real `CREATE VIRTUAL TABLE ... USING vec0(...)`, inserted 34,033 real vectors, ran real KNN queries. Cross-checked KNN output against independent pure-NumPy brute-force L2 distance — **results matched exactly**, confirming sqlite-vec's query path is correct, not a defect. (An apparent anomaly — the same handful of large files ranking near-top for almost every query — was chased down and found to be a real, structural weakness of the *hashed-BoW fallback embedder* on this size-skewed corpus, not a sqlite-vec bug: long/high-token-diversity files have far more chances to overlap a sparse few-dimension query by chance than short 2-chunk files do. Fixed one real defect along the way — IDF computed on collided hash bins instead of exact tokens — which didn't change the outcome.)

### 4. Index

2,175 `.md` files under `docs/` and `tasks/`, chunked into 34,033 pieces (~900 chars, paragraph-aware), embedded, stored in a `vec0` table (dim 4096).

### 5. The 20 questions

Real questions extracted from this repo's own recorded artifacts (`tasks/*.md` open/closed rows, `docs/decisions/ADR-*.md`, `docs/intake/*.md`) — not invented. Each has a definite source file used as ground truth for both methods.

| # | Question (abridged) | Source |
|---|---|---|
| 1 | owner=hub / owner=repo two-state-complete? | tasks/370 |
| 2 | top-level docs/archive/ still make sense? | tasks/420 |
| 3 | PASTE_THIS.md hard byte ceiling? | tasks/449 |
| 4 | codemap-generate/toc-generate in hub_hooks? | tasks/323 |
| 5 | intake flip post-#439-discharge? | tasks/466 |
| 6 | "in the cloud" = CI or cloud CC sessions? | tasks/144 |
| 7 | ecosystem enforcement own ~/.claude commit-check? | tasks/189 |
| 8 | ADR-89 Pyright oracle catches MODIFY edge? | tasks/220 |
| 9 | intake section-level status vs promotion-to-ADR? | tasks/450 |
| 10 | 3 stale dispositions — remove or re-point? | tasks/557 |
| 11 | night-batch harvest verb + API surface? | tasks/610 |
| 12 | 719 anchor WARNs — convert or re-baseline? | tasks/623 |
| 13 | may README.md be recreated? | ADR-114 |
| 14 | ruling outrank a ratified ADR? | ADR-115 |
| 15 | who writes JOURNAL.md? | ADR-39 |
| 16 | HTML dashboard writer policy? | intake 2026-07-08-dashboards |
| 17 | "project size" for role-chat scaling? | intake 2026-07-08-bootstrap |
| 18 | subagent-army pattern — where does it sit? | intake 2026-07-08-night-routines |
| 19 | which Gemini CLI is the scanning lane? | intake 2026-07-25-consolidation |
| 20 | compute placement in methodology scope? | intake 2026-08-09-compute-placement |

### 6. Result — recorded either way

**grep@5: 11/20 (55%)  ·  hashed-vector@5: 2/20 (10%). grep wins, clearly, on this corpus with this substitute embedder.**

Per-question hits: grep hit Q3,4,5,9,11,12,13,15,17,18,20 (11); vector hit only Q1,13 (2). Full raw per-question top-5 lists (both methods) were produced and are reproducible from the scratch scripts.

**Honest caveat, load-bearing:** this result answers "does grep beat a naive offline hashed-BoW vector index" — it does **not** answer "does grep beat model2vec," because model2vec was never reachable in this sandbox (§2). The hashed fallback has a known, verified structural bias toward large/high-token-diversity files regardless of topical relevance, which a real trained embedding (mean-pooled, dense) would not share. **The original CUT-4 question is still open.**

### 7. No adoption

Nothing adopted, no repo files touched, no merge, no push. This is the Tier-L measurement only; the Tier-S build (if warranted) is a future batch's call, and it should re-attempt model2vec from an environment with `huggingface.co` reachable before trusting any hit-rate number — the one produced here is a lower-bound sanity check on the substitute embedder, not a verdict on the pairing CUT-4 asked about.
