"""Lived-workflow sandbox — the CONSUMER measurement seam ([#252] Phase 0.5).

``observe-arc --consumer <repo-path>`` measures a REAL consumer's enforcement-in-effect
against the HUB's expectation. Frozen rulings (2026-07-05 overnight run):

- **Oracle = the HUB manifest** (``deploy/manifest-v1.2.0.yaml``) — the deployment's
  EXPECTATION. A manifest is never looked for inside the consumer clone.
- **Reality = the consumer clone's actual firing** across the three external channels
  (C1 — inner narration is never evidence).
- **Report per gated component**: FIRED / EXPECTED-BUT-SILENT / tombstone verdicts, plus a
  COVERAGE figure (n-of-6 enforcing on this consumer). **FAIL-by-coverage on a partial-mesh
  consumer is the CORRECT verdict** — the deliverable is measurement, never forced green.
- **No consumer-shaping** (no ruff-prune, no carriers — observe as-is) and **no mutation of
  the real consumer** (``sandbox_clone`` + observe only; the arc runs inside the throwaway
  clone, torn down with the guarded blast-radius teardown).
- Reuses the Slice-A/B primitives verbatim: ``sandbox_clone``, the observer, the oracle
  loader, and GATE-0 (isolation-only, [MF-1]).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from . import arc as _arc
from . import observe as _observe
from . import oracle as _oracle
from . import spawn as _spawn

# Evidence lines are verbatim consumer-clone stdout; belt-and-braces mask if a key-shaped
# token ever appears there (the report is printed, never committed — [MC-2] posture anyway).
_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}")
_MASK = "sk-ant-****MASKED****"

_PLUGIN_KEY = "tier1-lifecycle@dev-knowledge-methodology"


def mirror_relative_precommit_sources(real_repo: Path, clone: Path) -> list[str]:
    """G7 (STEP-3 witnessed, 2026-07-06): a consumer may pin a pre-commit source by
    RELATIVE path (ai-council: ``repo: ../.dev-knowledge`` @ rev v1.2.0) — resolvable on
    the operator machine's layout, unresolvable beside a sandbox clone in the temp dir, so
    pre-commit errors before ANY hook runs and the three pre-commit components can never
    be measured. Same class as G2 (root-ratified): MIRROR the operator machine's state —
    for each relative local repo path in the CLONE's pre-commit config, git-clone what it
    resolves to on the REAL machine into the same relative position beside the clone.

    Blast-radius guards: the mirror target must land INSIDE the sandbox temp root (an
    escaping path like ../../x is skipped + noted, never written); the source must exist
    as a git repo on the real machine (else skipped + noted — that IS the honest
    consumer-environment finding). The clone itself is never touched (observe-as-is)."""
    notes: list[str] = []
    cfg = Path(clone) / ".pre-commit-config.yaml"
    if not cfg.exists():
        return notes
    import yaml as _yaml
    try:
        data = _yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
    except _yaml.YAMLError:
        return notes
    temp_root = Path(clone).resolve().parent
    for entry in data.get("repos") or []:
        repo_ref = entry.get("repo", "") if isinstance(entry, dict) else ""
        if not isinstance(repo_ref, str) or not repo_ref.startswith(("..", "./")):
            continue  # URLs, `local`, `meta`, absolute paths: nothing to mirror
        source = (Path(real_repo) / repo_ref).resolve()
        target = (Path(clone) / repo_ref).resolve()
        if temp_root != target.parent and temp_root not in target.parents:
            notes.append(f"SKIPPED mirror {repo_ref!r}: escapes the sandbox temp root")
            continue
        if not (source / ".git").exists():
            notes.append(f"SKIPPED mirror {repo_ref!r}: {source} is not a git repo on the "
                         "real machine (consumer-environment finding)")
            continue
        if target.exists():
            notes.append(f"mirror {repo_ref!r}: already present")
            continue
        import floor_conformance as _fc
        r = _fc._run(["git", "-c", "core.autocrlf=false", "clone", "--quiet",
                      str(source), str(target)], temp_root)
        if r.returncode != 0:
            notes.append(f"SKIPPED mirror {repo_ref!r}: clone failed ({r.stderr.strip()[:120]})")
            continue
        notes.append(f"mirrored {repo_ref!r} -> {target.name} (operator-machine layout)")
    return notes


def consumer_declares_plugin(clone: Path) -> bool:
    """True iff the CONSUMER's own tracked settings declare the tier1 plugin enabled
    (exact JSON check, never a substring). Codex HIGH 2026-07-06: plugin seeding must be
    GATED on this — seeding a consumer that never deployed the enablement would let the
    harness MANUFACTURE plugin firing instead of measuring consumer enforcement."""
    settings = Path(clone) / ".claude" / "settings.json"
    if not settings.exists():
        return False
    try:
        data = json.loads(settings.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return False
    enabled = data.get("enabledPlugins")
    return isinstance(enabled, dict) and enabled.get(_PLUGIN_KEY) is True


def evidence_lines(events: list[dict], oracle: _oracle.Oracle,
                   *, max_lines_per_component: int = 3) -> dict[str, tuple[str, ...]]:
    """Verbatim hook-stdout lines matching each gated-active signature — the
    enforcement-in-effect proof quotes. Extraction only touches the structured hook-stdout
    surface (C1 holds: narration never enters it). G4a: executed lines lead; a skip-echo
    line is quoted too (it IS the honest evidence for an ARMED-BUT-SKIPPED verdict) but
    never masquerades ahead of real execution output."""
    surface = _observe.hook_stdout_surface(events)
    out: dict[str, tuple[str, ...]] = {}
    for exp in oracle.gated_active:
        executed, skipped = _observe.signature_lines(surface, exp.signature)
        hits = tuple(_SECRET_RE.sub(_MASK, ln.strip())
                     for ln in (*executed, *skipped))[:max_lines_per_component]
        if hits:
            out[exp.component_id] = hits
    return out


@dataclass(frozen=True)
class ConsumerReport:
    """One consumer measurement — verdicts + coverage, computed inside the clone's lifetime."""

    consumer: str                 # the measured repo path (as given)
    oracle_version: str           # hub methodology version the expectation came from
    gate: _arc.GateZero
    observation: _observe.ObservationResult
    coverage_fired: int           # gated-active components that FIRED on this consumer
    coverage_total: int           # gated-active components the hub expects (the six)
    coverage_armed_skipped: int   # G4a: consulted-but-Skipped (enforcing for their file scope)
    tombstone_state: str          # "ok" | "REGRESSED" | "VACUOUS" (G4b)
    evidence: dict[str, tuple[str, ...]]  # component_id -> verbatim matched stdout lines

    @property
    def tombstones_ok(self) -> bool:
        return self.tombstone_state == "ok"

    @property
    def full_coverage(self) -> bool:
        # G4a: an armed-but-skipped hook counts as covered (it enforces for its file scope;
        # the arc's single-file commit simply cannot exercise every files-filter) — but it is
        # never REPORTED as FIRED, so the reading stays uninflated.
        covered = self.coverage_fired + self.coverage_armed_skipped
        return covered == self.coverage_total and self.tombstones_ok

    def report_lines(self) -> list[str]:
        """The per-component measurement report (stdout-facing, flat — no box glyphs)."""
        lines = [
            f"consumer measurement: {self.consumer}",
            f"oracle: HUB manifest v{self.oracle_version} (expectation), consumer firing (reality)",
            self.gate.summary(),
        ]
        for f in self.observation.gated_findings:
            lines.append(f"  [{f.verdict}] {f.component_id} ({f.channel})")
            for ev in self.evidence.get(f.component_id, ()):
                lines.append(f"      | {ev}")
        for f in self.observation.observed_not_gated:
            lines.append(f"  ({f.verdict}) {f.component_id} ({f.channel}) — observed, not gated")
        armed = (f" + {self.coverage_armed_skipped} armed-but-skipped"
                 if self.coverage_armed_skipped else "")
        lines.append(
            f"COVERAGE: {self.coverage_fired}-of-{self.coverage_total} enforcing on this consumer"
            f"{armed}; tombstones {self.tombstone_state}")
        lines.append(
            "VERDICT: FULL-COVERAGE" if self.full_coverage
            else "VERDICT: FAIL-by-coverage (partial mesh — correct measurement, not an error)")
        return lines

    def summary(self) -> str:
        return "\n".join(self.report_lines())


def build_report(consumer: str, gate: _arc.GateZero, observation: _observe.ObservationResult,
                 oracle: _oracle.Oracle, events: list[dict]) -> ConsumerReport:
    """Pure assembly: verdicts -> coverage figures + evidence quotes (unit-testable offline)."""
    fired = {f.component_id for f in observation.gated_findings if f.verdict == _observe.FIRED}
    armed = {f.component_id for f in observation.gated_findings
             if f.verdict == _observe.SKIPPED_ARMED}
    active_ids = {e.component_id for e in oracle.gated_active}
    tomb_ids = {e.component_id for e in oracle.gated_absent}
    tomb_verdicts = [f.verdict for f in observation.gated_findings if f.component_id in tomb_ids]
    if any(v == _observe.UNEXPECTED for v in tomb_verdicts):
        tombstone_state = "REGRESSED"
    elif any(v == _observe.VACUOUS for v in tomb_verdicts):
        tombstone_state = "VACUOUS"    # G4b: absence unproven — no commit was attempted
    else:
        tombstone_state = "ok"
    return ConsumerReport(
        consumer=consumer,
        oracle_version=oracle.version,
        gate=gate,
        observation=observation,
        coverage_fired=len(fired & active_ids),
        coverage_total=len(active_ids),
        coverage_armed_skipped=len(armed & active_ids),
        tombstone_state=tombstone_state,
        evidence=evidence_lines(events, oracle),
    )


def run_consumer_arc(consumer_repo: Path | str, *, hub_root: Path | None = None,
                     api_key: str | None = None, model: str = _spawn.DEFAULT_MODEL,
                     timeout: int = 1200) -> ConsumerReport:
    """LIVE: clone the CONSUMER as-is, run the same six-hook arc prompt inside the clone,
    and measure firing against the HUB oracle. Never shapes the clone, never touches the
    real consumer repo. GATE-0 (isolation-only) is evaluated; the caller decides exit
    semantics — the report is produced either way (labeled untrusted on a failed gate)."""
    consumer_repo = Path(consumer_repo).resolve()
    root = Path(hub_root) if hub_root else _arc._repo_root()
    key = api_key or _spawn.load_api_key()
    oracle = _oracle.load_for_version("1.2.0", repo_root=root)
    with _spawn.sandbox_clone(consumer_repo, prefix="lived-consumer-") as (clone, env):
        # G1+G3 (measurement-#2 root ruling): FULL trust-seam parity with the hub arc path
        # via the ONE shared builder — provenance sentinel + scoped #253a allowlist (rides
        # the HARNESS-OWNED user-level config, the only place a headless child honors it:
        # the untrusted sandbox workspace IGNORES the clone's own settings.local.json
        # allows, witnessed verbatim at measurement #2) + the G3 owned-config sanction.
        # Never a bypass — anything beyond the arc still hits the wall.
        cfg = _arc.arc_isolated_config(clone.parent / "cfg")
        # G2 (measurement-#2 root ruling): plugin PRESENCE is harness-seeded from the HUB
        # checkout (the marketplace the consumer's settings point at) into the isolated
        # user config — mirroring the operator machine's user-level state, which the
        # isolated CLAUDE_CONFIG_DIR deliberately cannot reach. What is MEASURED is the
        # firing (the Stop hook + the /review-closures command act), never the presence.
        # GATED on the consumer's OWN enablement declaration (Codex HIGH 2026-07-06): a
        # consumer that never deployed the plugin gets no seed — its Stop-hook silence is
        # then the honest not-deployed reading, never a harness-manufactured firing.
        if consumer_declares_plugin(clone):
            _arc.seed_tier1_plugin(cfg, clone, source_root=root)
        # G7: materialize the consumer's relative-path pre-commit sources beside the clone
        # (operator-machine layout mirror) so pre-commit can run AT ALL — else it errors
        # before any hook and the pre-commit trio is unmeasurable (STEP-3 witnessed).
        mirror_relative_precommit_sources(consumer_repo, clone)
        result = _spawn.spawn(clone, _arc.ARC_PROMPT, config_dir=cfg, api_key=key,
                              model=model, extra_env=env, timeout=timeout)
        gate = _arc.evaluate_gate_zero(result)
        events = _observe.events_from_spawn(result)
        observation = _observe.observe(events, oracle, clone=clone)
        return build_report(str(consumer_repo), gate, observation, oracle, events)
