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


def evidence_lines(events: list[dict], oracle: _oracle.Oracle,
                   *, max_lines_per_component: int = 3) -> dict[str, tuple[str, ...]]:
    """Verbatim hook-stdout lines matching each gated-active signature — the
    enforcement-in-effect proof quotes. Extraction only touches the structured hook-stdout
    surface (C1 holds: narration never enters it)."""
    surface = _observe.hook_stdout_surface(events)
    lines = surface.splitlines()
    out: dict[str, tuple[str, ...]] = {}
    for exp in oracle.gated_active:
        hits = tuple(_SECRET_RE.sub(_MASK, ln.strip())
                     for ln in lines if exp.signature in ln)[:max_lines_per_component]
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
    tombstones_ok: bool           # every gated tombstone CORRECTLY-ABSENT (no prune regression)
    evidence: dict[str, tuple[str, ...]]  # component_id -> verbatim matched stdout lines

    @property
    def full_coverage(self) -> bool:
        return self.coverage_fired == self.coverage_total and self.tombstones_ok

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
        lines.append(
            f"COVERAGE: {self.coverage_fired}-of-{self.coverage_total} enforcing on this consumer"
            f"; tombstones {'ok' if self.tombstones_ok else 'REGRESSED'}")
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
    active_ids = {e.component_id for e in oracle.gated_active}
    tombstones_ok = all(
        f.verdict == _observe.ABSENT_OK
        for f in observation.gated_findings
        if f.component_id in {e.component_id for e in oracle.gated_absent})
    return ConsumerReport(
        consumer=consumer,
        oracle_version=oracle.version,
        gate=gate,
        observation=observation,
        coverage_fired=len(fired & active_ids),
        coverage_total=len(active_ids),
        tombstones_ok=tombstones_ok,
        evidence=evidence_lines(events, oracle),
    )


def run_consumer_arc(consumer_repo: Path | str, *, hub_root: Path | None = None,
                     api_key: str | None = None, model: str = _spawn.DEFAULT_MODEL,
                     timeout: int = 600) -> ConsumerReport:
    """LIVE: clone the CONSUMER as-is, run the same six-hook arc prompt inside the clone,
    and measure firing against the HUB oracle. Never shapes the clone, never touches the
    real consumer repo. GATE-0 (isolation-only) is evaluated; the caller decides exit
    semantics — the report is produced either way (labeled untrusted on a failed gate)."""
    consumer_repo = Path(consumer_repo).resolve()
    root = Path(hub_root) if hub_root else _arc._repo_root()
    key = api_key or _spawn.load_api_key()
    oracle = _oracle.load_for_version("1.2.0", repo_root=root)
    with _spawn.sandbox_clone(consumer_repo, prefix="lived-consumer-") as (clone, env):
        cfg = _spawn.write_isolated_config(
            clone.parent / "cfg", session_start_marker=_arc.PROVENANCE_MARKER)
        result = _spawn.spawn(clone, _arc.ARC_PROMPT, config_dir=cfg, api_key=key,
                              model=model, extra_env=env, timeout=timeout)
        gate = _arc.evaluate_gate_zero(result)
        events = _observe.events_from_spawn(result)
        observation = _observe.observe(events, oracle, clone=clone)
        return build_report(str(consumer_repo), gate, observation, oracle, events)
