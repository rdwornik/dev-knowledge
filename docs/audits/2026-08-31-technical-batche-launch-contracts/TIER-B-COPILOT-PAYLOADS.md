# BATCH E — TIER (B) ENTERPRISE COPILOT PAYLOADS

**Four payloads, each self-contained, each ≤75% of the measured 284.3k-token floor
(= 213,225 tokens).** Paste one per session. `sonnet-5` is the default; `opus-5` only where the
payload says tier L is pinned.

**Why these are yours to run:** Enterprise Copilot is not driveable from this seat. The lane
contracts they feed are already frozen in-tree, so a payload landing later does not re-open the
freeze — it unblocks a lane that is already written and waiting.

**What each payload FEEDS (so a result has somewhere to go):**

```
B-1  OTel GenAI event schema      -> DM-2  lane-f-6-observability-otel     (BLOCKED on this)
B-2  SDA-1 -> Harbor translation  -> DM-1  lane-e-5-eval-sda1-harbor       (BLOCKED on this)
B-3  Decision-tree updates        -> the AUTONOMY arc's next batch          (filing input)
B-4  grok PRODUCER acceptance     -> next batch's run lane; NOT this batch  (design only)
```

**Lane-contract drafts are NOT in this pack.** The brief listed them as a (B) item; they are
done and frozen at `docs/audits/2026-08-31-technical-batche-launch-contracts/` — 15 contracts
through both gates. Re-drafting them on Copilot would produce a rival to a frozen artifact.

---

## B-1 · OTel GenAI EVENT SCHEMA (sonnet-5)

```
You are designing an event schema, not adopting a vendor.

CONTEXT, and it is binding:
- OpenTelemetry GenAI semantic conventions are already DISCHARGED in this repo's decision
  tree. You are CONSUMING that verdict, not re-deciding it.
- Arize Phoenix and Langfuse are BOTH already DISCHARGED with recorded evidence. The
  collector must be PLUGGABLE between them. Do not recommend one over the other; do not
  hard-wire either.
- The VERDICT LAYER (trends -> rulings) is UNCHANGED. You are moving the emission format,
  not the judgment.
- NO NEW DEPENDENCY. If the schema would need a package, say so as a FINDING and stop —
  adding one is a separately gated act under this repo's dependency ADR.

DELIVER, as text:
1. The event schema: every span/event, its attributes, and which OTel GenAI convention
   attribute each maps to. Where our concept has NO convention attribute, say so and
   propose a namespaced custom attribute rather than bending a standard one.
2. The COLLECTOR SEAM: the smallest interface that keeps Phoenix and Langfuse
   interchangeable. Name what each would need that the other does not.
3. What this schema CANNOT express about our telemetry, stated plainly. A schema
   presented as total is the failure mode here.
4. A migration note: what our current emission would have to change, and what breaks.

Prose in English. No code beyond illustrative snippets. State every assumption you make
about our internals as an assumption, since you cannot see them.
```

---

## B-2 · SDA-1 PACK → HARBOR task/trial/verifier FORMAT (sonnet-5)

```
Translate an evaluation pack into Harbor's task/trial/verifier shape. TEXT ONLY.

HARD CONSTRAINT, and it is the point: THIS IS NOT A HARBOR ADOPTION. Harbor is PARKED in
this repo's decision tree behind the trigger "a second executor is admitted", and none is.
You are producing a TRANSLATION so a single comparison run can happen. If your output
starts to read like an adoption plan, a dependency list, or an install guide, you have
exceeded the brief — stop and say so.

DELIVER, as text:
1. The SDA-1 pack expressed as Harbor tasks, trials and verifiers, one to one where
   possible.
2. Every place the mapping is NOT one to one, named, with what is lost or invented at that
   point. This is the most valuable section — a clean-looking translation that silently
   drops a verifier is worse than a messy honest one.
3. What the Harbor shape BUYS over the hand-rolled run, and what it COSTS. Both, concretely.
   A translation reported with only upside has not been evaluated.
4. The comparison protocol: exactly what to measure so the single run is decidable against
   the hand-rolled baseline.

Prose in English. No installation steps. No recommendation to adopt.
```

---

## B-3 · DECISION-TREE UPDATES FROM THIS BATCH (sonnet-5)

```
Update a routing artifact from a batch's outcomes. FILING INPUT ONLY — you propose, the
repo's funnel disposes.

WHAT THE BATCH ESTABLISHED (treat as fact; these are measured, not claimed):
- A FOURTH codespace defect: a fresh codespace's agent is UNAUTHENTICATED — `claude -p`
  returns "Not logged in" in 47 ms, zero tokens. Every prior smoke probe missed it because
  none invoked the agent; they ran plain shell over ssh and measured the container.
- The prior W4 defects 2 (uv version) and 3 (silently-stale clone) remain UNMEASURED by
  that run — the steps never executed. It closes nothing and refutes nothing about them.
- `conflict/` does not exist anywhere in the fleet; a census premise had no subject.
- sqlite-vec was never installed or run; "proven under pinned uv" was refuted. It is
  Tier L, not Tier S, and `sentence-transformers` is on the REJECTED list (model2vec is
  the non-rejected pairing).
- A lane-branch naming enum admitted only single-letter lane ids, so a whole batch's lanes
  were invisible to its own teardown — caught at freeze by a new predicate.

DELIVER, as text:
1. For each item above: does it CHANGE an existing decision-tree leaf, ADD one, or CORRECT
   the record? Name the disposition and the reason. Every item lands in exactly one.
2. For anything you would ADD: the TRIGGER that would release it. A gap with no trigger is
   not routed, it is parked in disguise.
3. RECONCILE FIRST. Where an existing leaf already covers an item, say so and amend it
   rather than proposing a rival. Birthing ahead of a blocker is the failure mode this
   artifact exists to prevent.

Prose in English. Propose no backlog rows — that path runs through intake and ratification.
```

---

## B-4 · grok PRODUCER ACCEPTANCE DESIGN (opus-5 — TIER L IS PINNED HERE)

```
Design a MEASURED ADMISSION for a code-producing model. Design only; the run is a later
batch's lane.

THE BAR, and it is deliberately high:
- Admission is MEASURED, never default. A producer that is "probably fine" is not admitted.
- The design carries a REJECTION TAX: what it costs when the producer's output is wrong,
  who pays it, and how that cost is observed rather than assumed.
- The design carries an ADVERSARIAL SUITE: cases chosen because they are where a
  code-producing model is most likely to fail plausibly — not a happy-path sample.
- Heterogeneity is the point. This repo's recorded finding is "PLURALITY BUYS LITTLE;
  ASYMMETRY AND HETEROGENEITY BUY A LOT." A second producer that fails the same way as the
  incumbent buys nothing; say what asymmetry this one would actually add.

DELIVER, as text:
1. The acceptance pack: tasks, the pass criterion FROZEN EX ANTE, and how it is scored.
   Ex ante matters — a criterion chosen after seeing output is not a criterion.
2. The rejection tax, quantified as far as it can be, and named where it cannot.
3. The adversarial suite, with WHY each case is adversarial for a producer specifically.
4. The admission verdict shape: what result admits, what refuses, and what is inconclusive.
   An inconclusive band that is not declared up front becomes an accidental admission.
5. What this design CANNOT establish about the producer.

Prose in English. Do not run anything. Do not recommend admission — produce the instrument
that would decide it.
```

---

## RECORDING THE SPEND

The brief's token policy asks for per-lane provider + model + credits in the quota-source
telemetry, and makes the burn-down and quota panels this batch's visibility proof. **Record what
each payload cost when you run it** — HY-4 (`lane-n-14`) builds the panel that consumes it, and
that panel already declares its own limit: it can attribute **provider and credits** but **not a
MODEL**, because `[#615]` (the model+version commit trailer) is open and unfunded this batch.
