# NB2 · CLOUD C3 — intake-61 ratification sheet

**Repo** `dev-knowledge` · clone at `origin/main`, HEAD `fcc9485567f81814d24b84fe2db5ceff23b743ee` ("Merge branch 'docs/batch-2-dispatch' — night-batch-2 frozen") · **read-only, zero writes** · no gate, hook, pytest or `audit.py` run (container `uv` 0.8.17 vs pinned `==0.11.19`).

**No backlog row and no intake is proposed anywhere in this document.**

---

## 0. Counts — computed on this clone, both reported where they disagree

```
ls docs/intake/*.md    | wc -l   ->  56    (brief: 56)   AGREE
ls docs/decisions/*.md | wc -l   ->  89    (brief: 89)   AGREE
ls docs/audits/*.md    | wc -l   -> 773    (brief: 769)  DISAGREE +4
find tasks -name '*.md'| wc -l   -> 344    (brief: 344)  AGREE
wc -c < BACKLOG.md               -> 67883  (brief: 67,883 B) AGREE
ls scripts/*.py        | wc -l   ->  84
wc -c protocols/HANDOFF_BOOT.md  -> 17196
```

The `docs/audits/` delta is **+4 in the clone's favour**, the opposite direction the standing clause anticipates. Most likely cause, not asserted: HEAD is the `docs/batch-2-dispatch` merge, whose own subject line says it landed "13 lane contracts", and the batch-1 lane contracts live at `docs/audits/2026-08-21-*-lane-contract.md` (CLAUDE.md §9, `lane-contract-check` row). Reconciling 769 vs 773 needs the operator's disk — **MEASUREMENT-OWED-LOCAL**.

---

## 1. The intake, located

`docs/intake/2026-08-28-tech-handoff-engine-deployable-carrier.md` — frontmatter `intake-id: 61` (line 2), `status: READY` (line 3), title *"The handoff engine becomes a deployable, versioned carrier"* (line 8). 67 lines. Read in full.

**Its question set is exactly five** (`## Open questions for ratification`, lines 43–61). No manufactured symmetry required.

**Preflight finding on the intake's own `origin:` line (line 4).** It cites two artifacts. Neither exists as a file in this clone:

```
find . -iname "*TO-NEXT-ARCHITECT*" -not -path "./.git/*"   -> (no output)
grep -rl "PHASE0-CONTRACT-2026-08-28" --exclude-dir=.git .
   -> ./JOURNAL.md                                (prose reference, JOURNAL.md:269)
   -> ./protocols/STANDING_RULINGS.md             (prose reference, :3101)
   -> ./docs/intake/2026-08-28-tech-handoff-engine-deployable-carrier.md
grep -rl "TO-NEXT-ARCHITECT" --exclude-dir=.git .
   -> ./docs/intake/2026-08-28-...-carrier.md     (the intake itself, and nowhere else)
```

`PHASE0-CONTRACT-2026-08-28.md` is named as an executed artifact by `JOURNAL.md:269` and as the authority for `STANDING_RULINGS.md` section Z (`:3101`), so it existed; it is not committed here. `TO-NEXT-ARCHITECT-2026-08-28` theme 10 resolves **nowhere in the tree**. Both are operator-side. This does not weaken the intake — it means **the operator is the only reader who can check the provenance clause against its source**, and the ratification should not treat either locator as verifiable from the repo.

---

## 2. Question 1 — what, exactly, is "the engine"?

### Quoted verbatim (intake lines 45–48)

> 1. **What, exactly, is "the engine"?** The assembler (`gen_handoff.py`), the probe gate, the
>    seal-identity check and the boot contract are candidates. A carrier that ships all of the hub's
>    handoff scripts would ship hub-only assumptions with them; one that ships too little leaves a
>    consumer unable to cut a bundle. The boundary is the decision.

### The test I applied, stated before the verdicts

A constituent is **ENGINE** if (a) a consumer cannot cut or verify a bundle without it, and (b) its behaviour does not depend on a surface only the hub has. It is **CARGO** if it encodes the hub's own governance surfaces. A constituent can be **SPLIT** — and three of the four are.

### Per-constituent verdict

**(a) The assembler — SPLIT, and the split line is already drawn in the code.**

`scripts/gen_handoff.py` is 1,086 lines; `scripts/assemble_paste.py` is 300. The generic core (`collect_state`, `_resolve_bundle_dir`, `_render`/`_substitute`, `_splice_fill_regions`, `detect_fill_state`, `reflow_framing`, `verify_seal_identity`) reads only git and the bundle dir. The hub-coupled collectors are enumerable, and I enumerated them by the paths the module opens:

```
grep -n "repo_root /\|_REPO_ROOT /" scripts/gen_handoff.py
 :59-61  templates/handoff/{v5,epic,functional}     -> CARGO (hub-authored templates)
 :273    .git                                       -> engine
 :503    scripts/  (imports audit.ALL_CHECKS)       -> CARGO, hub-only
 :521    VISION.md (via canonical_docs.VISION)      -> engine (canonical living-doc name)
 :539    docs/intake/                               -> boundary: the folder IS carried already
 :633    ecosystem/disposition-register.yaml        -> CARGO, hub-only
 :953    docs/handoffs/                             -> engine
```

Plus `assert_batch_boundary` / `_open_batches` (`:400`, `:415`), which refuse a cut while a committed **batch manifest** declares an open batch — a hub-only concept.

**The decisive fact for the carrier decision is that every one of those already has a written degrade contract**, not an assumption:

- `collect_hints` (`:486`): *"Every leg degrades to a 'run <command>' pointer on failure — a generator that cannot compute a hint must never guess it into the bundle."*
- `_intake_index` (`:532`): *"an absent or empty docs/intake/ directory returns a literal 'no intake docs yet' marker, never a guess."*
- `_register_organs` (`:627`): *"Returns [] when the register is absent or unreadable, and the caller degrades loudly rather than guessing."*
- `_window` (`:641`): *"Returns None when git is unavailable or there is no prior bundle — a generator that cannot compute the window says so; it never guesses a range."*

So the assembler **already runs in a repo that has none of the hub's surfaces**, by design, degrading rather than crashing. That is the single strongest piece of evidence that the assembler is shippable — and it was engineered for the answer-free invariant, not for portability, so the portability is a by-product the ratification gets for free. Whether it *actually* degrades cleanly on a consumer tree is **MEASUREMENT-OWED-LOCAL** (needs execution).

**(b) The probe gate — SPLIT, along a line the spec draws itself.**

`protocols/HANDOFF_PROCESS.md` §5, under *"Who runs it"*, is explicit:

> **The checker is a COMMAND, not a `scripts/` validator, by necessity.** Running the probe commands is *execution*, which Layer 2 does not do (Critical Rule #4; ADR-28/36) — the reason `scripts/verify_handoff_probes.py` is resolve-only. The gate therefore has two organs and they are not interchangeable[.]

- `scripts/verify_handoff_probes.py` (781 lines) — **ENGINE**. Already parameterized on `repo_root` and already carries a `cross_repo` flag (`:675`, `:575`). Its audit adapter `audit.py::check_handoff_probes` (`:1653`) is already **presence-based**: *"a repo with no such bundle is a no-op pass, so this no-ops on the fleet's child repos."* The organ is pre-shaped for consumers.
- `/handoff-verify` — **ENGINE, as an instruction file**. A command file is carried, not executed by the hub. Precedent: `carrier_mesh.py` already ships `.claude/commands/override.md` "verbatim (repo-agnostic)" into consumers.
- **The probe manifest** (the five-row table in §5) — **CARGO**. Four of five rows bind to hub-only surfaces: `ALL_CHECKS` in `scripts/audit.py`; a named `PLAYBOOK`/`ESSENTIALS` section; `audit.py ship-gate` ∩ `ecosystem/disposition-register.yaml`; the "pointer round-trip" into a live PLAYBOOK section. **Only "Live HEAD / tree" is repo-agnostic.** A consumer receiving this manifest unchanged receives four probes it cannot answer.

**(c) Seal-identity — ENGINE, the cleanest candidate in the set, with one coupling that must be named.**

`scripts/check_seal_identity.py` is 87 lines and reads nothing but the bundle directory name and the bundle's own Slug row. Exit-code contract is already stated ("0 clean / 1 identity violation / 2 internal error — an error is a BLOCK, never a silent pass"). Zero hub surfaces.

**The coupling:** it imports its verifier *from the assembler* —

```
scripts/check_seal_identity.py:36-39
    from gen_handoff import BundleIdentityError, verify_seal_identity
```

deliberately, to avoid "the #153 two-copies identity/monkeypatch trap". So **the seal hook cannot be shipped without `gen_handoff.py`**. Any carrier that ships the hook alone ships a broken import. This is a hard boundary fact, not a preference.

**(d) The boot contract — CARGO in content, ENGINE in shape, and FLEET-SINGULAR in one part.**

Three distinct objects hide under one name:

- `protocols/HANDOFF_PROCESS.md` — 1,191 lines, `Version: 6.3.0`, and it **is** in the spec registry (verified: `scripts/validate_reconciliation.py:113` lists `"protocols/HANDOFF_PROCESS.md"`). **This is the version anchor a consumer would pin.** The intake's claim on this point resolves.
- `protocols/HANDOFF_BOOT.md` — 17,196 B (budget 18,000, so 804 B headroom; the budget is at `assemble_paste.HANDOFF_BOOT_BYTE_BUDGET`, `:52`, gated by `audit.py::check_boot_byte_budget`, registered at `audit.py:4018`). Since v6.3.0 this file is **resident in the operator's browser project, installed once** (§4, *"Residency"*), not shipped per repo. It is **fleet-singular**: one browser project serves N repos. Shipping it per-repo would create N copies of the file whose entire v6.3.0 mechanism is that there is exactly one, pinned by sha.
- `templates/handoff/v5/*.tmpl` — **CARGO**, measured:

```
grep -o -E "PLAYBOOK|BACKLOG|JOURNAL|audit\.py|docs/intake|ecosystem/|ADR-[0-9]+|\[#[0-9]+\]" \
     templates/handoff/v5/*.tmpl | sort | uniq -c | sort -rn
  8 PROBES.md.tmpl:BACKLOG     7 HANDOFF_BOOT.md.tmpl:PLAYBOOK
  6 RESIDUAL.md.tmpl:JOURNAL   6 PROBES.md.tmpl:audit.py
  5 RESIDUAL.md.tmpl:BACKLOG   5 PROBES.md.tmpl:docs/intake
  3 PROBES.md.tmpl:ecosystem/  3 PROBES.md.tmpl:JOURNAL
  1 PROBES.md.tmpl:[#436]      1 PROBES.md.tmpl:ADR-83
  1 HANDOFF_BOOT.md.tmpl:ADR-87
```

A backlog id and two hub ADR numbers are baked into the templates. That is the "hub-only assumptions" the intake warns about, made countable.

### The options

```
OPTION A — Engine = the four Python organs; templates, spec and probe manifest are
           SEPARATE carried components with their own versioning.
  Becomes true:  a consumer can cut, seal and structurally verify a bundle.
  Impossible:    treating "the engine" as one indivisible artifact; the templates and
                 the probe manifest must each be given a home and a version.
  Cost:          ~2,254 lines of Python (gen_handoff 1086 + verify_handoff_probes 781
                 + assemble_paste 300 + check_seal_identity 87) enter the carrier set;
                 the hub-only collectors ship and degrade rather than being stripped.

OPTION B — Engine = everything that cuts or verifies a bundle, shipped whole.
  Becomes true:  one component, one version, nothing to argue about.
  Impossible:    a consumer receiving a probe manifest it can answer — four of its five
                 rows bind to hub surfaces the consumer does not have.
  Cost:          exactly the failure the intake names ("would ship hub-only assumptions").

OPTION C — Engine = the two never-execute VALIDATORS only (verify_handoff_probes +
           check_seal_identity); the assembler stays hub-local and the hub cuts a
           consumer's bundle under RULING-W (worktree/branch -> report).
  Becomes true:  the smallest carrier; nothing hub-coupled leaves the hub.
  Impossible:    "every project can run its own handoff" — the intake's opening premise.
                 A consumer could verify a bundle it cannot cut.
  Cost:          check_seal_identity imports gen_handoff, so this option is not
                 implementable as stated without first breaking that import.

OPTION D — Engine ships as the already-ACCEPTED `dev-knowledge-kernel` package
           ([#559] / intake #25 W-2), tagged, resolved by reference.
  Becomes true:  version legibility is native — the pin IS the version.
  Impossible:    treating this intake as independent of [#559]; it becomes a consumer
                 of that row's vehicle.
  Cost:          blocked behind [#559] (open, P2, size L, depends-on #332/#334/#351).
```

**My recommendation, marked as mine:** Option A for the *boundary*, with D as the *vehicle*. The line that survives contact with the tree is **"reads a hub-only surface"** — it is checkable by the grep above, it lands `check_seal_identity` and `verify_handoff_probes` cleanly on the engine side, it splits the assembler at seven named call sites rather than in principle, and it forces the probe manifest to be re-authored for a consumer rather than shipped broken. What it explicitly does **not** do is answer "everything" — three of four constituents come back SPLIT.

### What answering q1 binds

`deploy/manifest-v1.4.0.yaml` (a new `components:` entry, and possibly a new `carrier:`); `protocols/HANDOFF_PROCESS.md` §5's probe manifest (a consumer profile of it); `templates/handoff/v5/*.tmpl` (de-hub-referencing, which is a spec-version-bearing act); `scripts/check_seal_identity.py` ↔ `scripts/gen_handoff.py` (the import coupling); `[#559]`; `[#611]` (v7 owns the bundle *contents*, this owns the carrier — the intake's own out-of-scope line, line 65).

---

## 3. Question 2 — copy-with-hash vs pin-to-tag

### Quoted verbatim (intake lines 49–52)

> 2. **Does the engine ship as code, or as a declared dependency?** Copy-with-hash (the
>    `CLAUDE-FLOOR.md` pattern, already proven and already gated by `floor-hash-verify`) versus a
>    consumer-side pin to a hub release tag. These have different failure modes: a stale copy is
>    detectable, a stale pin is not.

### First finding: the tree already runs **three** modes, not two

**Mode 1 — copy-with-hash (the floor).** `deploy/carrier_floor.py` writes into the consumer: `.claude/CLAUDE-FLOOR.md`, `.claude/CLAUDE-FLOOR.md.sha256`, `.claude/check_floor_hash.py`, an `@`-include in `CLAUDE.md`, a `.gitignore` negation block, and a `SessionStart` hook. The hook line itself is owned by a *different* carrier (`deploy/manifest-v1.4.0.yaml:196-201`, `required_local_hooks: - id: floor-hash-verify`), because "arming spans two carriers (ADR-93)".

**Mode 2 — pin to a hub tag (the pre-commit hooks).** `deploy/manifest-v1.4.0.yaml:180-186`:

```yaml
      hub_hooks:
        rev: v1.4.0
        repo: https://github.com/rdwornik/dev-knowledge
        hooks: [codemap-freshness, toc-freshness, block-ff-push, backlog-id-on-close]
```

**Mode 3 — copy *without* a version anchor (the mesh).** `deploy/carrier_mesh.py` byte-copies `scripts/session_end_backpressure.py` and `scripts/canonical_freshness_gate.py` into consumers. Its own docstring: *"script content-mismatch is drift, not a version anchor — the manifest rev-pin on the precommit carrier is the version surface, so no PRESENT_WRONG_VERSION."*

Note what mode 3 means: **hub Python code already ships into consumers today, by copy, with no hash and no version.** Whatever this intake decides, it is not deciding whether hub code may travel — that is settled practice.

### Second finding: the brief's asymmetry needs qualification, and the qualification changes the design

The brief hands me *"a stale copy is detectable, a stale pin is not"* as the crux. Tested against the tree, **neither half is quite right, and the real axis is different.**

**A copy's hash does not detect staleness. It detects tampering.** `deploy/carrier_floor.py`, verbatim:

> Three contract states (the `.sha256` is content-integrity, **not a version anchor** — so no `PRESENT_WRONG_VERSION`): `ABSENT` … `PRESENT_CORRECT` … `PRESENT_DRIFTED`.

The consumer-side sidecar answers "has this file been edited since it was written?" It cannot answer "has the hub's copy moved?" — the consumer has nothing to compare against. Staleness of a copy is detected **hub-side**, when `_classify_floor` compares the consumer's floor to the corpus floor at deploy/detect time. Which is the same place a pin is checked.

**A stale pin *is* detectable — hub-side, and the mechanism is already built.** `ecosystem/parity-surfaces.yaml:472`:

```yaml
    probe: {type: precommit_remote, repo_token: dev-knowledge,
            expected_rev_from: deployed-versions, ancestry: true,
            required_hook_ids: [backlog-id-on-close, block-ff-push]}
```

That reads the consumer's pinned `rev`, compares it to `ecosystem/deployed-versions.yaml`, and proves ancestry. It has already had to be *legislated around*: ADR-102's `gate_rev_ahead` block (`parity-surfaces.yaml:481-493`) blesses corp-monorepo's pin at `v1.3.1` while its corpus record stays `1.2.0`, with the reason stated in the file.

**So the honest restatement of the asymmetry:**

```
                       detects TAMPER        detects DRIFT-FROM-HUB   where the detector lives
copy + sha sidecar     YES, consumer-side    NO                       travels with the clone
pin to a tag           n/a (nothing local)   NO, by itself            hub-side only
hub-side comparison    -                     YES, both modes          hub, on repos it audits
```

The real difference is **not detectability. It is residency of the detector.** The floor's guard runs in the consumer at every session start and, per `carrier_floor.py`, is *"un-suppressible by `git commit --no-verify`"* — it fires on a repo the hub is not looking at. The pin's checker fires only when the hub runs an audit against a repo listed in `parity-surfaces.yaml`. **That** is the asymmetry the design has to answer, and it is q4's subject, not q2's.

### Third finding: the copy-vs-reference question is already ruled — and the ruling never landed in the register

`docs/intake/2026-08-05-func-simplification-distribution-wave.md` carries `status: ACCEPTED` (line 3, ratified 2026-08-09 by the recorded erratum). Its **W-8**, lines 43–53, is titled *"local-copy vs hub-reference ruling matrix (the operator's explicit ask — proposed as the standing rule)"*:

```
| Fleet asset                              | Mode                        | Vehicle                     |
| Enforcement code (kernel checks, hooks)  | REFERENCE, version-pinned   | W-2 package + W-3 rev       |
| Structure, naming, config skeletons      | REFERENCE with merge        | W-1 copier + answers file   |
| CI definition                            | REFERENCE                   | W-4 reusable workflow @tag  |
| Toolchain pins (python, uv, ruff base)   | REFERENCE                   | W-2 package metadata        |
| Repo's own tasks/, JOURNAL, ADRs, state  | LOCAL, always               | never templated             |
| Methodology docs (PLAYBOOK etc.)         | LOCAL pointer to hub version| template stamps the version |
Principle: code and structure by reference (versioned, updatable), state and identity local.
```

And `[#559]` (open, P2, L) carries the same decision as a live row: *"the kernel ships as an installable package from the hub, a git-tag-pinned dependency (`uv add dev-knowledge-kernel @ git+<hub>@vX.Y`), so consumers pull versioned CODE **by reference** rather than by copy."*

With the constraint from intake #38 that saves the wasted refactor, quoted from the same row: *"Python tooling **cannot** inherit config from an installed package (Ruff `extend`, mypy, pytest and coverage resolve a file path, never a package name), so the *config* is distributed as files while the *code* is imported."*

**But W-8 has never landed in the standing-rulings register:**

```
grep -n "W-8\|copy-vs-reference\|hub-reference\|by reference" protocols/STANDING_RULINGS.md
   -> (no matching line)
```

It is accepted doctrine sitting only in an intake body. **This is the most consequential thing on this sheet for q2:** the ratification is at risk of re-deciding, from scratch, a question an ACCEPTED intake already answered — and re-deciding it *differently*, because the intake-61 framing ("copy-with-hash is proven") leans toward the mode W-8 rules against for code.

### The options

```
OPTION A — COPY-WITH-HASH (the floor pattern), for the engine's Python.
  Becomes true:  a consumer-side, fail-closed, clone-travelling guard fires on tamper at
                 every SessionStart and at commit time, on repos the hub never audits.
  Impossible:    a single source of truth for the code — N byte-identical copies exist,
                 and every hub engine edit becomes a fleet redeploy event.
  Cost:          ~2,254 lines x N consumers to keep hash-identical. And the recorded
                 failure mode of exactly this path: intake #25's WHY names carrier_mesh's
                 hand-copy as where "[#498] exec-bit defect lived".
  Contradicts:   W-8 row 1 ("Enforcement code -> REFERENCE, version-pinned").

OPTION B — PIN TO A HUB RELEASE TAG (the hub_hooks.rev / [#559] package shape).
  Becomes true:  the operator's clause is satisfied LITERALLY — the pin IS the version,
                 so "consumers know which engine version they run" is answerable by
                 reading one line in the consumer's own pyproject/config.
  Impossible:    a consumer-side refusal, unless one is added (see D). Nothing in a
                 consumer fails when its pin goes stale.
  Cost:          blocked behind [#559]'s package existing at a tag; adds a network/VCS
                 dependency to a consumer's `uv sync`.
  Aligns with:   W-8 row 1, and [#559]'s already-accepted vehicle.

OPTION C — BOTH, SPLIT BY ARTIFACT KIND (what W-8 already says).
  Engine CODE by reference at a tag; the SPEC version stamped locally; the TEMPLATES
  and probe-manifest profile carried as files (intake #38's file-not-package constraint).
  Becomes true:  each artifact rides the vehicle its own nature admits; consistent with
                 the accepted matrix and with the intake-area/install-guide precedents
                 (manifest-v1.4.0.yaml:387, :410 — kind: config, verify: hash).
  Impossible:    a single "the engine" version number covering code + spec + templates,
                 unless one is deliberately defined over the set.
  Cost:          three versioning surfaces to keep coherent, which is q3's subject.

OPTION D — PIN, PLUS A CARRIED VERSION STAMP AND A CONSUMER-SIDE CHECK.
  The code is referenced at a tag; a one-line engine-version stamp is written INTO the
  consumer; a small consumer-side gate asserts installed-version == stamp.
  Becomes true:  the only option under which a stale pin is detectable FROM INSIDE the
                 consumer -- the actual hole, once the asymmetry is restated correctly.
  Impossible:    claiming the check is free; it is a new gate in every consumer.
  Cost:          one more artifact per consumer, and it must obey Z-G4 (below).
```

**My recommendation, marked as mine:** **C as the shape, D's stamp as the mechanism.** C because it is not a new decision — it is the accepted W-8 matrix applied to a new asset, and re-deciding it here would fork doctrine. D because the corrected asymmetry locates the real gap precisely: a pin's detector lives hub-side and therefore misses "a repo the hub is not currently looking at" — the intake's own words in q4. A stamp is the cheapest thing that moves one detector into the consumer.

I would also recommend the ratification **land W-8 in `protocols/STANDING_RULINGS.md`** as part of this act, since it is being relied on. That is a doctrine-siting observation, not a row.

### What answering q2 binds

`deploy/manifest-v1.4.0.yaml` (`hub_hooks` vs a new component with `verify: hash`); `deploy/carrier_*.py` (a new carrier, or none if by reference); `ecosystem/parity-surfaces.yaml` (a probe row); `protocols/STANDING_RULINGS.md` (W-8's landing); `[#559]` (its package becomes this intake's vehicle, or is explicitly not); `pyproject.toml` in each consumer, if by reference.

---

## 4. Question 3 — where does a consumer record its engine version?

### Quoted verbatim (intake lines 53–55)

> 3. **Where does a consumer record its engine version?** Reusing `deployed-versions.yaml` avoids a
>    second registry; a separate field or file avoids conflating corpus version with engine version,
>    which can legitimately diverge.

### Evidence

`ecosystem/deployed-versions.yaml` header states its own write-contract: *"the fields are written by the DEPLOY-RUNBOOK (`deploy/tool.py --execute`) at deploy time… Do NOT hand-fabricate a value: a value cannot precede its release."* Read by `audit.py::check_deployed_methodology_version` (`scripts/audit.py:2322`, registered `:4001`).

**The file has already anticipated a fold and refused one**, in its own words: *"Modeled 1:1 on the `ecosystem/tool-versions.yaml` pattern: committed · written-by-command · read-by-a-check — same pattern, a new axis (repo-keyed deployed-corpus-version, not tool-keyed reviewed-changelog-version), so a dedicated file, not a fold."*

**And the divergence the question hypothesizes is already realised and already legislated.** From the same file, the corp-monorepo entry:

> Stays 1.2.0 BY DESIGN — corp's hub-block pin v1.3.1 is an enforcement-gate carrier repoint (2 hooks), not a corpus deploy; modeled as ADR-102 `gate_rev_ahead` in `parity-surfaces.yaml`. #336/ADR-102 (Accepted 2026-07-17) ruled NOT to bump… Do not "fix" to 1.3.1.

So "corpus version and gate version legitimately diverge" is not a hypothetical — it cost an ADR, a `gate_rev_ahead` block, and a do-not-fix comment.

### The options

```
OPTION A — reuse `deployed_methodology_version` (one number covers corpus and engine).
  Becomes true:  no new registry, no new check.
  Impossible:    engine and corpus moving independently -- which corp-monorepo already
                 does. The gate_rev_ahead escape hatch would have to be built a second
                 time, for a second axis.
  Cost:          re-creates the exact defect ADR-102 was written to contain.

OPTION B — sibling fields in the same file (`deployed_engine_version`, `engine_source_tag`).
  Becomes true:  one file, one read; check_deployed_methodology_version grows a sibling.
  Impossible:    honouring the file's own stated reasoning -- it justified NOT folding
                 tool-versions in on the grounds that a different AXIS earns its own file.
                 A per-repo engine version is a different axis by that same test.
  Cost:          a documented principle bent at its first re-application.

OPTION C — a dedicated `ecosystem/deployed-engine-versions.yaml`, on the precedent
           deployed-versions.yaml itself cites.
  Becomes true:  consistent with the stated pattern; one concern per file; a new
                 audit check on the check_deployed_methodology_version shape.
  Impossible:    a single-file answer to "what is deployed here".
  Cost:          a third file in the same family, and a third check.

OPTION D — record it IN THE CONSUMER, not in the hub.
  Becomes true:  the operator's clause is satisfied as WRITTEN -- "consumers know which
                 engine version they run" becomes answerable without the hub.
  Impossible:    the hub answering the fleet-wide question from one read; it would have
                 to walk N repos (or keep a hub mirror, i.e. D plus one of A/B/C).
  Cost:          a new consumer-side artifact; a hub-side aggregate becomes a walk.
```

**Observation I would put in front of the operator, marked as mine:** A, B and C are all **hub-side records**. They answer *the hub's* question ("what did I deploy where"). The operator's quoted requirement — reproduced at intake line 20 — is that **consumers know which engine version they run**. Only D answers that from inside a consumer. A/B/C are worth having, but choosing among them without also choosing D leaves the stated requirement discharged by a file the consumer cannot see.

### What answering q3 binds

`ecosystem/deployed-versions.yaml` (schema + header write-contract); `scripts/audit.py` (`check_deployed_methodology_version` at `:2322`, and `ALL_CHECKS` registration at `:4001` if a sibling check is added); `deploy/tool.py` (the writer); `ecosystem/doc-code-edge.yaml` (the audit's own docstring at `:2379` names it as the sibling-posture surface); `ecosystem/parity-surfaces.yaml` if the new axis gets a probe.

---

## 5. Question 4 — what is the refusal?

### Quoted verbatim (intake lines 56–58)

> 4. **What is the refusal?** A consumer whose engine version does not match what the hub deployed
>    should fail somewhere. Deciding *where* that check lives — hub-side fleet check, consumer-side
>    gate, or both — determines whether it has teeth on a repo the hub is not currently looking at.

### Evidence: both sites exist, and the floor already chose "both"

- **Hub-side precedent:** `audit.py::check_deployed_methodology_version` (`:2322`) plus the `precommit_remote` probe (`parity-surfaces.yaml:472`). Reach: repos registered in `parity-surfaces.yaml` **and** audited. `deploy/tool.py:253` refuses an unregistered repo before it even reads a manifest (per the win-tooling admission comment in `deployed-versions.yaml`), so registration is a hard precondition.
- **Consumer-side precedent:** the floor's two legs — the `floor-hash-verify` pre-commit hook (`manifest-v1.4.0.yaml:196-201`) and the `SessionStart` guard `check_floor_hash.py --require-present` (`manifest-v1.4.0.yaml:715` component `floor-sessionstart-guard`). `carrier_floor.py` names the property that matters: the SessionStart leg *"fires every session, travels with the clone, un-suppressible by `git commit --no-verify`"*.
- **The floor is already BOTH**, and ADR-93 records why: *"arming spans two carriers"*.

### A live ruling this question must obey

`protocols/STANDING_RULINGS.md:3096`, section Z, **Z-G4** — ruled 2026-08-28, the same day intake 61 was filed:

> **A check that cannot compute its ground truth must FAIL, never skip.** A `skipped` status is a **reported gap**, never a pass, and no aggregate surface may count it as one.

with the reason: *"the skip condition and the failure condition are frequently correlated: a hygiene test wrapped in `skipif(tool missing)` skips on precisely the machine whose missing tool is breaking hygiene."*

Applied here: a consumer-side engine-version check that cannot reach the hub, or cannot resolve the expected version, **must FAIL**. A design that has it skip when offline is pre-refused by a ruling already on the books.

### The options

```
OPTION A — hub-side fleet check only.
  Becomes true:  one implementation; reuses check_deployed_methodology_version's shape.
  Impossible:    teeth on an unregistered or unaudited repo -- the intake's own concern,
                 stated in its own words.
  Cost:          registration in parity-surfaces.yaml becomes load-bearing for safety,
                 not just for reporting.

OPTION B — consumer-side gate only.
  Becomes true:  teeth travel with the clone; fires without the hub present.
  Impossible:    a fleet-wide answer from one read; the hub learns nothing.
  Cost:          the pre-commit leg is `--no-verify`-bypassable (as every client hook is);
                 the SessionStart leg is not, which is why the floor uses both.

OPTION C — both legs, the floor's shipped shape.
  Becomes true:  the property the floor already demonstrates -- local teeth plus fleet
                 visibility, with each leg covering the other's blind spot.
  Impossible:    a one-carrier implementation (ADR-93: arming spans two carriers).
  Cost:          two carriers, two hook lines, two failure modes to keep honest --
                 which is the cost the floor already pays and the fleet already runs.
```

**My recommendation, marked as mine:** C, because the question's own framing ("a repo the hub is not currently looking at") is answerable only by a consumer-resident leg, and the fleet-visibility half is answerable only hub-side. C is not a compromise here; it is the only option that answers the question as posed. Whatever is chosen, Z-G4 binds the failure semantics.

### What answering q4 binds

`deploy/manifest-v1.4.0.yaml` (`required_local_hooks` and/or a `SessionStart` component); `deploy/carrier_precommit.py` and a second carrier (ADR-93 split); `scripts/audit.py` `ALL_CHECKS`; `ecosystem/parity-surfaces.yaml`; `protocols/STANDING_RULINGS.md` Z-G4 (as the governing failure semantics).

---

## 6. Question 5 — the Layer-2 boundary check

### Quoted verbatim (intake lines 59–61)

> 5. **Layer-2 boundary check.** ADR-28/36 hold that no hub script drives state in a child repo.
>    A DEPLOYED engine is carried, then run BY the consumer — this intake reads that as consistent,
>    and the ratification should confirm it rather than let it pass unexamined.

### Tested against the invariant, as the brief requires

**(1) ADR-28's literal words are already false of this tree, and the intake paraphrases the wrong sentence.** `docs/decisions/ADR-28-three-layer-architecture.md:17`:

> - `.dev-knowledge` contains no executable orchestration — **scripts do not reside here**

But `ls scripts/*.py | wc -l` = **84**. ADR-28 itself anticipated this, at `:21`: *"If a future session produces evidence contradicting the model (e.g., a script genuinely must reside in `.dev-knowledge`…), reopen with Council #N."* The operative form of the invariant is the re-scoped one in `CLAUDE.md` §5 rule 4: *"Layer 2 never executes — no orchestration scripts: no script drives state in a child repo (ADR-28, ADR-36). Hub-local validators, generators and gates are in scope."* **The intake's paraphrase happens to be the correct, operative version** — it says "no hub script drives state in a child repo", not "no scripts reside here". A ratification that cites ADR-28's literal text will be citing a sentence the tree already contradicts.

**(2) ADR-36 Q5's hard constraint is real, and it is already qualified.** `ADR-36:109-121`: *"NEVER touches child repos. Read-only contract is hard constraint in ADR-36, enforced via tool architecture (no write paths to child repo paths)."* Amended at `ADR-36:319` by **RULING-W** (2026-07-18), quoted verbatim there:

> RULING-W: hub MAY/SHOULD write into consumer repos for methodology/cleanup — separate worktree/branch, then report; FIRST step of any consumer leg = codify this as the ADR-36/41 amendment (mechanism before act).

with hard bounds: never a direct push into a live consumer checkout; re-witness the consumer live before any edit; the consumer's own merge discipline governs integration.

**(3) The precedent is not one deep, it is three.** `carrier_floor` writes a floor + guard + settings.json into a consumer. `carrier_mesh` writes two Python scripts and a command file in. `carrier_docs` writes `docs/intake/README.md` + `templates/intake-template.md` in (manifest component `intake-area`, `:387`). All under ADR-92's **write-yes / commit-no** posture — the hub writes and stages, the operator ratifies the commit. The manifest even names the model: *"Model D: deploy-into-consumer"* (`manifest-v1.4.0.yaml:227`).

**(4) The one place a genuine breach could hide, and where it does not.** `/handoff-verify` **runs commands** — HANDOFF_PROCESS §5 says so explicitly and calls it out as the reason `verify_handoff_probes.py` is resolve-only. But the runner is the **consumer's own CC session in the consumer's own repo**; the hub ships a command *file*. Shipping instructions is not executing. The breach would occur only if the hub ran a consumer's probe commands from the hub — which nothing in this intake proposes.

**(5) The sharpest live statement of the boundary, and the constraint a carrier inherits.** `scripts/generate_floor.py` docstring:

> **OPERATOR-INVOKED ONLY** (ADR-73 rollout-moment). This generator must **NEVER** be wired to a hook or a schedule, and never makes autonomous cross-repo writes… Strict Layer-2 invariant — **no runtime/scheduled cross-repo writes from the hub.**

### Verdict, stated plainly as the brief requires

**q5 does not breach the Layer-2 invariant, and the intake's reading is correct — but it understates its own case and cites the wrong sentence.**

- A deployed engine, carried at deploy time and run by the consumer, is **already precedented three times** in the shipped carrier set. It is not "consistent with" the invariant; it is the invariant's existing practice.
- The invariant it must be tested against is **not ADR-28's literal "scripts do not reside here"** (false since at least the audit tool), but the composite: `CLAUDE.md` §5 rule 4 + ADR-36 Q5 **as qualified by RULING-W** + `generate_floor.py`'s never-scheduled clause.
- **The one live constraint the design must inherit, and it is a real bound, not a formality:** deploy is **operator-invoked at a rollout moment**, never wired to a hook or a schedule. An engine carrier that acquired a scheduled refresh — "keep consumers current automatically" — would breach the invariant at the exact clause `generate_floor.py` states. That is the failure mode worth naming at ratification, because it is the one a convenience feature would walk into.

### What answering q5 binds

Nothing new, if the answer is "consistent" — which is the finding. If the ratification wants the confirmation to be *citable*, the sites are `docs/decisions/ADR-36-audit-tool-architecture.md` (a further amendment marker under RULING-W's precedent, since ADRs are immutable per CLAUDE.md §5 rule 3) or `protocols/STANDING_RULINGS.md` (a register entry, which is the cheaper and more conventional home for a technical confirmation under ADR-108 §A). ADR-28's stale literal sentence is a separate defect this sheet surfaces and does not propose an action for.

---

## 7. Cross-cutting findings the ratification should have in hand

1. **Three of the four q1 constituents come back SPLIT.** Only seal-identity is unambiguously engine, and it is import-coupled to the assembler (`check_seal_identity.py:36-39`), so the smallest shippable unit is larger than the smallest engine-classified unit.
2. **q2 is not open ground.** `docs/intake/2026-08-05-func-simplification-distribution-wave.md` is `status: ACCEPTED` and its **W-8** matrix rules enforcement code to REFERENCE, version-pinned. `[#559]` carries the same as an open row with a named vehicle. Re-deciding q2 without addressing W-8 forks doctrine.
3. **W-8 never landed in the register** (`grep` over `protocols/STANDING_RULINGS.md` returns no hit for W-8, "copy-vs-reference", "hub-reference" or "by reference"). It is being relied on from an intake body.
4. **The brief's asymmetry, as handed to me, does not survive the tree.** A copy's sidecar detects *tamper*, not staleness (`carrier_floor.py`: "content-integrity, not a version anchor"); a stale pin *is* detected, hub-side (`parity-surfaces.yaml:472`). The surviving asymmetry is **where the detector lives** — which relocates the crux from q2 into q4.
5. **The divergence q3 hypothesizes is already realised** (corp-monorepo: pin v1.3.1, corpus 1.2.0) and already cost ADR-102 plus a `gate_rev_ahead` block.
6. **Z-G4 (2026-08-28) pre-binds q4's failure semantics** — a check that cannot compute its ground truth FAILS, never skips.
7. **The operator's own clause is consumer-facing** ("consumers know which engine version they run"), and three of q3's four options are hub-side records that do not satisfy it from inside a consumer.
8. **Both of intake 61's `origin:` locators are unresolvable in this clone** (§1). Provenance is operator-verifiable only.

---

## 8. MEASUREMENT-OWED-LOCAL

Every item below needs a gate, hook, the pytest suite or `scripts/audit.py` — none of which can start here (`uv` 0.8.17 vs `==0.11.19`).

```
M1  Whether gen_handoff.py actually degrades cleanly (not crashes) on a tree with no
    ecosystem/disposition-register.yaml, no scripts/audit.py and no batch manifest.
    The docstrings at :486/:532/:627/:641 CLAIM it; only execution proves it.
M2  Whether verify_handoff_probes.py runs clean against a consumer-shaped bundle
    (cross_repo=True path, :675).
M3  Current audit.py::check_boot_byte_budget verdict. HANDOFF_BOOT.md measures
    17,196 B against the 18,000 B budget by `wc -c` (computed here) -- but the gate's
    own read is what ships.
M4  Whether the `precommit_remote` probe currently passes for corp-monorepo under the
    gate_rev_ahead blessing.
M5  Whether floor-hash-verify and the SessionStart guard actually fire as described in
    a live consumer (deploy/floor_conformance.py's fire test).
M6  The 769 vs 773 `docs/audits/*.md` reconciliation (section 0).
M7  Line/byte cost of any carrier addition against CLAUDE.md's line budget --
    validate_doc_rot.scan_file_budget, per Z-G2's constraint note.
```

---

## 9. Self-audit

**Against the brief's stated failure mode** ("if you answered a question without quoting it first, you may have answered a question the intake does not ask"): all five questions are quoted verbatim from `docs/intake/2026-08-28-tech-handoff-engine-deployable-carrier.md:45-61` immediately before each answer. The set is exactly five; no symmetry was manufactured, and none needed to be.

**Against the standing self-audit clause** ("propose no backlog row and no intake"): no row body, no `done-when`, no `kill-candidates`, no id is proposed anywhere above. Two doctrine-siting observations appear (landing W-8 in the register; ADR-28's stale literal sentence) — both are stated as findings for the operator, neither carries a proposed row.

**One deviation to declare.** The brief handed me its q2 asymmetry as "the crux": *a stale copy is detectable, a stale pin is not.* Grounded in the tree, it does not hold in that form — `carrier_floor.py` states in its own words that the sidecar is "content-integrity, **not** a version anchor", and `ecosystem/parity-surfaces.yaml:472` is a working hub-side stale-pin detector. I answered the corrected question rather than the one as handed, and said so rather than producing an answer that would have read as complete and been wrong. If the operator intended the framing to be taken as given, §3 is the section to re-read.

**Output shape.** This report is my final message, `#` at byte 0, no wrapping fence; tables and command blocks are fenced for copying, per CLAUDE.md §4 render-layer rule. Zero writes, zero commits, zero branches — `git status` on this clone is untouched by me.