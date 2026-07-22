# ADR-40 — Scale Tier Evaluation Algorithm

<!-- scope: meta -->

> **Status: DEPRECATED 2026-05-23.** The tier system this ADR computes is
> deprecated ecosystem-wide. No replacement. Retained for historical
> decision-trace only — defines no active machinery. See the Deprecation note
> below and [[ADR-38]] amendment A5 + [[ADR-33]] amendment, same date.

Status: Deprecated (was: Accepted)
Date: 2026-04-30 (deprecated 2026-05-23)

## Deprecation note 2026-05-23

Operator decision 2026-05-23 — full tier-system deprecation. ADR-40's
`compute_tier_score` / `classify_tier` algorithm produced calibration values
that were never operationally consumed: the audit tool did not gate on
computed tier, and the calibration baseline clamped all repos to a single tier
under the documented miscalibration (VISION F-08). Tier-conditional governance
baselines did not differentiate behavior in practice (tier-as-theater
analysis). The `tier:`/`scale:` frontmatter fields this ADR fed are removed
(ADR-33 amendment 2026-05-23); the universal baseline replaces all
tier-conditional file mandates (ADR-38 amendment A5 2026-05-23). This ADR is
retained as historical record; the algorithm below is no longer authoritative
and no tool implements it.
Related: ADR-33 (VISION universalization, tier Lite/Standard),
         ADR-36 (audit tool — consumer of this algorithm),
         ADR-38 (universal repo architecture — defines module/test/TCR),
         ADR-39 (file lifecycle governance),
         transcript council-out-20260430-154818-research_*

## Context

Repos in ecosystem are classified S (Small) / M (Medium) / L (Large)
to inform governance obligations:
- VISION.md tier: Lite (M) vs Standard (L) per ADR-33
- BACKLOG.md mandate: M+ per ADR-41 (pending)
- ARCHITECTURE.md mandate: L per ADR-38
- ADR directory mandate: L per ADR-38

Historically tier classification was subjective ("feels like M"). This
fails for solo dev because:
- Complexity creep is invisible until painful
- Retrofit cost grows exponentially (research finding)
- Multi-stream context switching makes vibe assessment unreliable

Council research debate (council-out-20260430-154818-*) validated:
- Composite metric required (no single signal sufficient)
- Logarithmic structure matches exponential complexity growth
- Maintainability Index pattern (industry standard since 1992)
- Token Context Ratio (TCR) is strongest LLM-specific signal
- Auto-detected via Python, deterministic, no LLM-dependent eval

## Decision

### Algorithm: Composite Tier Score

Adapted Maintainability Index pattern. Single composite score (0-100,
higher = simpler).

```python
import math

def compute_tier_score(tcr_tokens: int, tests_count: int, modules_count: int) -> float:
    """
    Composite Tier Score — adapted Maintainability Index.

    Logarithmic signals reflect exponential complexity growth.
    Returns score 0-100. Higher = simpler (S), lower = more complex (L).

    Args:
        tcr_tokens: total estimated tokens (per ADR-38 TCR rules)
        tests_count: total test functions (per ADR-38 test definition)
        modules_count: top-level src/ subdirectories (per ADR-38 module def)

    Returns:
        Composite score clamped to [0, 100]
    """
    # Avoid log(0) edge cases
    tcr_k = max(tcr_tokens / 1000, 0.1)  # tokens in thousands
    tests = max(tests_count, 1)
    modules = max(modules_count, 1)

    # Coefficients (calibrated against ecosystem; tunable post-validation)
    a = 100        # baseline (perfect simplicity)
    b = 12         # TCR weight (LLM context risk — most relevant for LLM workflow)
    c = 8          # tests weight (linear maintenance burden)
    d = 15         # modules weight (cognitive load — highest per-unit impact)

    score = a - b * math.log(tcr_k) - c * math.log(tests) - d * math.log(modules)
    return max(0, min(100, score))
```

**Python version requirement:** Audit tool implementation targets Python 3.10+
to use `str | None` union syntax (PEP 604). All ecosystem repos already
target 3.10+; this is not new constraint.

### Three signals (per ADR-38 definitions)

1. **TCR (Token Context Ratio)** — total estimated tokens across
   source-controlled files matching ADR-38 inclusion rules. Computed
   via chars/4 estimate (deterministic, no external dependencies).

2. **Tests count** — total test functions across `tests/` directory
   per ADR-38 test definition (functions matching `test_*` pattern,
   pytest discovery).

3. **Modules count** — top-level subdirectories under `src/{package_name}/`
   containing `__init__.py` plus 1+ Python files per ADR-38 module
   definition.

### Tier classification with hysteresis

Map composite score to tier with asymmetric promotion/demotion thresholds
(prevents flapping):

```python
def classify_tier(score: float, current_tier: str | None = None) -> str:
    """
    Map composite score to S/M/L with hysteresis.

    Promotion (toward L) at lower threshold;
    demotion (toward S) at higher threshold.
    Hysteresis band = 10 points.
    """
    # Promotion thresholds (current=S → check M, current=M → check L)
    PROMOTE_M = 65   # score < 65 → M
    PROMOTE_L = 35   # score < 35 → L

    # Demotion thresholds (current=L → check M, current=M → check S)
    DEMOTE_S = 75    # score >= 75 → S
    DEMOTE_M = 45    # score >= 45 → M

    if current_tier is None:
        # First classification, no hysteresis
        if score >= 65:
            return "S"
        elif score >= 35:
            return "M"
        else:
            return "L"

    # Apply hysteresis based on current tier
    if current_tier == "S":
        if score < PROMOTE_M:
            return "M"
        return "S"
    elif current_tier == "M":
        if score < PROMOTE_L:
            return "L"
        elif score >= DEMOTE_S:
            return "S"
        return "M"
    else:  # current_tier == "L"
        if score >= DEMOTE_M:
            return "M"
        return "L"
```

Insight: repos rarely shrink in practice. Demotion paths exist for
correctness but are rarely exercised. Logarithmic model is primary
anti-flap defense; hysteresis is secondary safety.

### Tier transition procedures (S → M, M → L)

When audit tool detects tier transition (per ADR-36), the following
procedures apply. Procedures live primarily in PLAYBOOK.md (separate
session for PLAYBOOK update) but are codified in ADR-40 below.

#### S → M transition

| Aspect | Required action |
|---|---|
| **Trigger** | Audit detects score < 65 (PROMOTE_M threshold) |
| **VISION.md** | Upgrade frontmatter to `tier: M` (Lite per ADR-33). Create VISION.md if missing. |
| **BACKLOG.md** | Initialize per ADR-41 (when ratified). Seed with current pending items. |
| **README.md** | Add "Current State" section if not present |
| **CHANGELOG.md** | Mandatory from this point per ADR-38 |
| **Process changes** | Per-handoff backlog grooming (~2 min); per-session JOURNAL entry |
| **Audit checks** | VISION tier=M; BACKLOG present; CHANGELOG entries per session |
| **Timeline** | Within 2 sessions post-detection |

#### M → L transition

| Aspect | Required action |
|---|---|
| **Trigger** | Audit detects score < 35 (PROMOTE_L threshold) |
| **VISION.md** | Upgrade to `tier: L` (Standard per ADR-33) |
| **ARCHITECTURE.md** | Create per ADR-38 mandate |
| **docs/decisions/** | Create directory; ADRs mandatory for architectural changes |
| **HANDOFF_PROCESS** | Full compliance with ADR-32 v2.0 + ADR-37 two-phase |
| **Process changes** | Quarterly grooming (~30 min); ADR for architectural decisions; lessons promotion enforced per session |
| **Audit checks** | VISION tier=L; ARCHITECTURE present; ADR directory present; quarterly groom artifact |
| **Timeline** | Within 5 sessions post-detection |

#### Demotion procedures (M → S, L → M)

Rare in practice (repos seldom shrink). Procedure: audit flags demotion
candidate, Rob reviews and decides whether to formally demote
(removing tier-specific obligations) or keep tier (e.g., repo
strategically simplified but governance still valuable).

Demotion is **not automatic** — requires Rob acknowledgment in VISION.md
frontmatter update. Prevents drift from temporary metric fluctuations
becoming permanent obligation removal.

### Enforcement (per Rob's pushback: warn only)

Audit tool (per ADR-36) reports tier mismatches in gap reports. NOT
pre-commit blocking. Solo dev autonomy preserved.

When tier transition detected:
- Audit tool logs in `.dev-knowledge/ecosystem/{repo}/history/YYYY-MM-DD.md`
- Audit tool generates handoff folder for the repo's browser chat
  (per ADR-36 + ADR-37 two-phase format) listing required actions
- Browser chat decides timing of remediation (per Rob's "Defer requires
  justification" principle — concrete reason can defer; no reason = act now)

### Calibration baseline (ecosystem snapshot 2026-04-30)

Estimated tier classification for current ecosystem (audit tool
implementation will produce authoritative measurements):

| Repo | TCR (est) | Tests | Modules | Score (est) | Tier |
|---|---|---|---|---|---|
| corp-ops | ~5k | 74 | 3 | ~74 | S |
| .dev-knowledge | ~10k | ~50 | 2 | ~75 | S |
| ai-council | ~30k | 310 | 8 | ~52 | M |
| corp-sca-time-automation | ~20k | ~150 | ~5 | ~62 | M (boundary) |
| corp-monorepo | ~150k | 2495 | 18 | ~21 | L |

Coefficients (b=12, c=8, d=15) and thresholds (PROMOTE_M=65, PROMOTE_L=35,
demotion +10 hysteresis) calibrated to produce these classifications.

Recalibration: if real ecosystem measurements diverge significantly
from estimates above, ADR-40 amendment may adjust coefficients. Solo
dev expectation: low frequency of recalibration (annual review).

### Universalization (per ADR-33 pattern)

- **Mandate**: All repos in ecosystem (.dev-knowledge + child repos
  under Dev/) classified per this algorithm
- **Audit-detected**: tier computed by audit tool (per ADR-36); declared
  in VISION.md frontmatter; mismatch = audit finding
- **Recommendation**: Future repos onboarded to ecosystem follow this
  classification from day 1 (proactive per Rob's insight: profilaktyka
  beats archeologia)
- **Cross-repo audit (Phase 3)**: ecosystem-wide tier report, drift
  detection over time

### Lifecycle entry (per ADR-39)

Tier classification itself does not create new files; lives in:
- VISION.md frontmatter (declared, manual)
- `.dev-knowledge/ecosystem/{repo}/state.yaml` (workspace inventory per ADR-36)
- `.dev-knowledge/ecosystem/{repo}/history/YYYY-MM-DD.md` (audit findings)

These are governed by ADR-39 lifecycle pattern (audit tool ownership,
append-only history, etc.). No new file lifecycle entries needed for
ADR-40.

## Consequences

### Positive
- Subjective tier classification eliminated
- Auditable, deterministic, reproducible from any commit
- Logarithmic model captures exponential complexity growth
- Three-signal approach captures distinct dimensions (LLM, maintenance,
  cognitive)
- Hysteresis prevents flapping
- Transition procedures explicit (proactive governance per Rob's insight)
- Calibration tunable post-validation

### Negative
- Coefficients (b=12, c=8, d=15) require empirical validation against
  real ecosystem measurements
- Solo dev may not always update VISION.md tier when audit flags
  transition (warn-only enforcement = honor system)
- TCR estimate (chars/4) may diverge from precise tokenizer; refinement
  to tiktoken possible if precision matters
- Edge case: tier-boundary repos (corp-sca-time-automation ~62) may
  flap absent hysteresis (mitigated by 10-point band)

### Follow-ups
- Audit tool P1 implementation (separate session per ADR-36): implement
  `compute_tier_score`, `classify_tier`, integrate with audit run
- PLAYBOOK.md update (separate session): incorporate transition
  procedures from this ADR
- VISION.md frontmatter update across ecosystem repos: declare tier
  per current measurement (Phase 2 universalization)
- Empirical validation: after audit P1 ships, compare computed tiers
  with calibration baseline; adjust coefficients if divergent
- ADR-41 (BACKLOG.md): mandate at M+ tier; references this ADR
- Future ADR for security/CI tier-specific requirements (deferred per
  Council research; ADR-40 covers governance artifacts only)

## References

- transcript council-out-20260430-154818-research-question-how-should-an-llm-driven-multi-repo-ecosy.md
- ADR-33 (VISION.md universalization, tier Lite/Standard)
- ADR-36 (audit tool architecture)
- ADR-38 (universal repo architecture, module/test/TCR definitions)
- ADR-39 (file lifecycle governance)
- Maintainability Index (Oman & Hagemeister, 1992)
