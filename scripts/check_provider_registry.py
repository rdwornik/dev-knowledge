#!/usr/bin/env python
"""check_provider_registry.py — hold the provider/model seams in agreement with the registry.

`ecosystem/provider-registry.yaml` is the declared home for every provider, CLI and model
string on the live surface (CLOUD-4 v2, from
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §3.3). Sites that can read
YAML at runtime read it. The rest — a `.md` frontmatter key, a `.js` object literal, a JSON
config, committed prose — cannot, so this checker is their coupling.

WHY A CHECKER AND NOT A REWRITE, stated plainly because it is the honest limit of the whole
cut: you cannot make YAML frontmatter or a JavaScript string literal *read* a YAML file. What
a registry buys at those sites is not indirection, it is **detection** — R2 §3.3's actual
finding was that `claude-sonnet-5` sits in three formats "with nothing asserting they agree".
This is that assertion. A swap still edits N files; what changes is that it can no longer edit
N-1 of them and ship.

Covers the table-edit seams R2 §3.2 enumerates:

    S7  scripts/changelog_sentinel.py        _TOOLS derived from the registry (a real import)
    S8  ecosystem/tool-versions.yaml         tool keys + changelog source_urls agree
    S9  .claude/agents/artifact-reader.md    frontmatter `model:` + the prose model note
    S10 .claude/workflows/conformance-hub.js the three per-stage `model:` pins
    S17 protocols/PLAYBOOK.md                the tier-binding sentence's exact model string
    S26 .claude/settings.json                the marketplace id + absolute host source path
    S29 ecosystem/satellite-onboarding-rulings.yaml   the `gpt-5.6-sol` provenance token
    S30 pyproject.toml                       the `grok L5` provenance attribution
    S31 protocols/AI_COUNCIL_PROCESS.md      the council provider roster vs `council_alias`

S31 was added by LANE L1 (2026-08-23) and is the seam that reads the rows that lane added.
It is not a new seam class — it is the R2 §3.3 finding applied to the surface where it was
still true: a closed provider vocabulary living in committed prose with nothing asserting it
agrees with the registry. At the time it was written the roster named five providers and the
registry declared three, and neither surface could say so.

Beside the seams, one referential check with no seam number, because it is about the registry
rather than about a site: `check_role_admission_evidence` requires every recorded admission
verdict to cite an artifact that exists.

S11 is a canonical-DOC seam, not a model seam, and is checked by `tests/test_canonical_docs.py`
against `scripts/canonical_docs.CONFORMANCE_V2_SCAN`.

Exit 0 clean, 1 on a violation, 2 on an internal error — an error BLOCKS rather than passing
silently, matching the house posture of `check_seal_identity` / `validate_hermetization`.
Read-only: this module reports, it rewrites nothing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

try:
    from scripts import provider_registry as _preg
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import provider_registry as _preg

_REPO_ROOT = Path(__file__).resolve().parent.parent

# The registry role each checked site is pinned by. Roles, not literals: the site is asserted
# against "whatever the registry says the subagent default is", which is the point.
_SUBAGENT_DEFAULT_ROLE = "subagent-default"
_WORKFLOW_VERIFIER_ROLE = "workflow-verifier"

_ARTIFACT_READER = ".claude/agents/artifact-reader.md"
_CONFORMANCE_HUB = ".claude/workflows/conformance-hub.js"
_PLAYBOOK = "protocols/PLAYBOOK.md"
_SETTINGS = ".claude/settings.json"
_TOOL_VERSIONS = "ecosystem/tool-versions.yaml"
_PYPROJECT = "pyproject.toml"
_AI_COUNCIL = "protocols/AI_COUNCIL_PROCESS.md"

_FRONTMATTER_MODEL_RE = re.compile(r"^model:\s*(\S+)\s*$", re.MULTILINE)
_JS_MODEL_RE = re.compile(r"model:\s*'([^']+)'")
#: The number of per-stage `model:` pins `.claude/workflows/conformance-hub.js` must
#: carry (its three Stage-1 verifiers). Checked as a COUNT, not only as a value: a
#: findall-and-compare leg passes clean when a pin is DELETED, because the pins it
#: still finds all agree -- so a stage silently falls back to the harness default and
#: the registry coupling this gate exists to hold is gone with nothing saying so.
_CONFORMANCE_HUB_PIN_COUNT = 3
# S17's prose seam is a tier BINDING, not a loose mention: "…tier is Sonnet 5 (`claude-sonnet-5`)".
# Anchored on the binding so the check reads the sentence that matters rather than any backtick
# in a 4,500-line file. A reworded sentence fails LOUD ("binding sentence not found") instead of
# passing quietly on an unrelated occurrence — the right direction to be wrong in for a seam gate.
_PROSE_TIER_RE = re.compile(r"tier is [^`\n]*\(`([^`]+)`\)")
# S31's roster seam is the `models` row of AI_COUNCIL_PROCESS's frontmatter-key table:
#   | `models` | `claude,gemini,openai,deepseek,grok` | All 5 by default. ... |
# Anchored on the row rather than on any backticked comma-list, for the same reason
# _PROSE_TIER_RE is anchored on its sentence: a reworded table fails LOUD ("roster row not
# found") instead of passing quietly on an unrelated match elsewhere in a 3,600-line file.
_COUNCIL_ROSTER_RE = re.compile(r"^\|\s*`models`\s*\|\s*`([^`]+)`\s*\|", re.MULTILINE)


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    """The leading `---`-delimited block, or "" — so a `model:` line in the BODY cannot be
    mistaken for the frontmatter pin."""
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def _sole_role_model(role: str) -> str:
    """The single model id carrying `role`, or raise — a role with 0 or 2 holders is a
    registry defect, not a site defect, and saying so at the registry is more useful."""
    ids = _preg.models_for_role(role)
    if len(ids) != 1:
        raise _preg.RegistryError(
            f"registry role `{role}` is held by {len(ids)} models ({ids}); expected exactly 1")
    return ids[0]


# --- per-seam checks ----------------------------------------------------------------------

def check_s8_tool_versions(root: Path) -> list[str]:
    """Registry provider identity vs the durable ADR-80 record's keys and source urls."""
    out: list[str] = []
    data = yaml.safe_load(_read(root, _TOOL_VERSIONS)) or {}
    tools = data.get("tools") or {}
    expected_urls = _preg.changelog_source_urls()
    for key, url in expected_urls.items():
        if key not in tools:
            out.append(f"S8 {_TOOL_VERSIONS}: registry declares tool key `{key}`, file has no such key")
            continue
        actual = str((tools[key] or {}).get("source_url", ""))
        if actual != url:
            out.append(f"S8 {_TOOL_VERSIONS}: `{key}.source_url` is {actual!r}, registry says {url!r}")
    for key in tools:
        if key not in expected_urls:
            out.append(
                f"S8 {_TOOL_VERSIONS}: tool key `{key}` is not declared by any provider in the registry")
    return out


def check_s9_artifact_reader(root: Path) -> list[str]:
    """The `.md` frontmatter format — the subagent default, plus the prose note beneath it."""
    out: list[str] = []
    want = _sole_role_model(_SUBAGENT_DEFAULT_ROLE)
    text = _read(root, _ARTIFACT_READER)
    m = _FRONTMATTER_MODEL_RE.search(_frontmatter(text))
    if not m:
        out.append(f"S9 {_ARTIFACT_READER}: no `model:` frontmatter key found")
    elif m.group(1) != want:
        out.append(f"S9 {_ARTIFACT_READER}: frontmatter `model: {m.group(1)}`, registry says `{want}`")
    if f"Pinned to {want}" not in text:
        out.append(f"S9 {_ARTIFACT_READER}: prose model note does not say `Pinned to {want}`")
    for upgrade in _preg.models_for_role("upgrade-path"):
        if upgrade not in text:
            out.append(
                f"S9 {_ARTIFACT_READER}: registry declares `{upgrade}` as the upgrade path, "
                f"the model note does not name it")
    return out


def check_s10_conformance_hub(root: Path) -> list[str]:
    """The `.js` object-literal format — every per-stage `model:` pin."""
    want = _sole_role_model(_WORKFLOW_VERIFIER_ROLE)
    found = _JS_MODEL_RE.findall(_read(root, _CONFORMANCE_HUB))
    if not found:
        return [f"S10 {_CONFORMANCE_HUB}: no `model: '...'` pin found"]
    out = []
    if len(found) != _CONFORMANCE_HUB_PIN_COUNT:
        out.append(
            f"S10 {_CONFORMANCE_HUB}: found {len(found)} `model:` pin(s), expected "
            f"{_CONFORMANCE_HUB_PIN_COUNT} -- a deleted pin lets that stage fall back "
            f"to the harness default, which is the coupling this gate exists to hold")
    out.extend(f"S10 {_CONFORMANCE_HUB}: pin `{got}` disagrees with the registry's `{want}`"
               for got in found if got != want)
    return out


def check_s17_playbook(root: Path) -> list[str]:
    """The `.md` prose format — the sentence that binds a tier to an exact model string."""
    want = _sole_role_model(_SUBAGENT_DEFAULT_ROLE)
    m = _PROSE_TIER_RE.search(_read(root, _PLAYBOOK))
    if not m:
        return [f"S17 {_PLAYBOOK}: the tier-binding sentence (\"…tier is X (`model-id`)\") was not "
                f"found; the registry pins `{want}` here"]
    if m.group(1) != want:
        return [f"S17 {_PLAYBOOK}: the tier-binding sentence says `{m.group(1)}`, "
                f"registry says `{want}`"]
    return []


def check_s26_settings(root: Path) -> list[str]:
    """The JSON-config format — the marketplace id and the absolute host source path."""
    out: list[str] = []
    settings = json.loads(_read(root, _SETTINGS))
    markets = settings.get("extraKnownMarketplaces") or {}
    for pid, fields in _preg.providers().items():
        mid = fields.get("marketplace_id")
        if not mid:
            continue
        if mid not in markets:
            out.append(f"S26 {_SETTINGS}: registry declares marketplace `{mid}` (provider {pid}), "
                       f"settings has {sorted(markets)}")
            continue
        actual = str(((markets[mid] or {}).get("source") or {}).get("path", ""))
        want = str(fields.get("marketplace_source_path", ""))
        if actual != want:
            out.append(f"S26 {_SETTINGS}: `{mid}` source path is {actual!r}, registry says {want!r}")
    return out


def check_provenance_pins(root: Path) -> list[str]:
    """S29 + S30 — a provenance attribution resolves to a registered model id.

    Provenance is the cheapest class R2 flags (`table-edit`, "cosmetic"), and it is checked for
    exactly one reason: an attribution naming a model the registry has never heard of is how a
    provider quietly enters the corpus without entering the vocabulary.
    """
    out: list[str] = []
    tokens = _preg.attribution_tokens()
    for rel, pins in _preg.pins_by_path().items():
        if rel in (_ARTIFACT_READER, _CONFORMANCE_HUB, _PLAYBOOK):
            continue                                    # handled by their own format-aware checks
        path = root / rel
        if not path.exists():
            out.append(f"provenance pin: registry names {rel}, which does not exist")
            continue
        text = path.read_text(encoding="utf-8")
        for mid, seam, _fmt in pins:
            token = tokens[mid]
            if token not in text:
                out.append(f"{seam} {rel}: registry pins `{mid}` here via the attribution "
                           f"token {token!r}, which the file does not carry")
    return out


def check_s31_council_panel(root: Path) -> list[str]:
    """S31 — the council's provider roster and the registry's alias vocabulary agree.

    `protocols/AI_COUNCIL_PROCESS.md` declares the default panel as a closed comma-separated
    token set. Those tokens are PROVIDER ALIASES, and for two of five they differ from the
    registry key (`claude`/`anthropic`, `grok`/`xai`) — which is why the mapping is data
    (`providers.<id>.council_alias`) rather than a dict in this module.

    Checked in BOTH directions, because each catches a different rot:

    * roster -> registry: a provider the council panels that the registry has never heard of.
      This is the same failure class `check_provenance_pins` guards — a provider entering the
      corpus without entering the vocabulary — and it is how the registry came to carry three
      of five aliases while the roster carried five.
    * registry -> roster: an alias the registry claims that the roster no longer names, i.e.
      a stale registry assertion. `council_alias: null` is the correct declaration for a
      provider the council does not panel, so this direction has an unambiguous fix.
    """
    text = _read(root, _AI_COUNCIL)
    m = _COUNCIL_ROSTER_RE.search(text)
    if not m:
        return [f"S31 {_AI_COUNCIL}: the council roster row (\"| `models` | `a,b,c` |\") was not "
                f"found; the registry declares aliases {sorted(_preg.council_aliases())}"]
    roster = [tok.strip() for tok in m.group(1).split(",") if tok.strip()]
    aliases = _preg.council_aliases()
    out: list[str] = []
    out.extend(
        f"S31 {_AI_COUNCIL}: council roster names provider `{tok}`, which no registry entry "
        f"declares as its `council_alias`"
        for tok in roster if tok not in aliases
    )
    out.extend(
        f"S31 {_AI_COUNCIL}: registry provider `{pid}` claims council alias `{alias}`, which "
        f"the roster does not name (use `council_alias: null` if it is not panelled)"
        for alias, pid in sorted(aliases.items()) if alias not in roster
    )
    return out


def check_role_admission_evidence(root: Path) -> list[str]:
    """Every recorded admission verdict points at an artifact that exists.

    The schema already refuses a decided verdict with no `evidence:` string
    (`ecosystem/schema/provider_registry.py`), but a schema is a models-only module and
    cannot touch the filesystem. This is the other half: the string has to RESOLVE. A verdict
    citing a renamed or deleted artifact is how a refusal decays into an unfalsifiable claim
    — and the registry is the surface a future lane will read to find out why a role is not
    held, so a dead locator there is worse than none.
    """
    out: list[str] = []
    for (mid, role), record in sorted(_preg.role_admissions().items()):
        rel = record.get("evidence")
        if not rel:                                  # legitimate only for `unevaluated`
            continue
        if not (root / str(rel)).exists():
            out.append(
                f"role_admission {mid}/{role}: evidence `{rel}` does not exist — a verdict "
                f"citing a missing artifact is an assertion, not a record")
    return out


def check_registry_shape() -> list[str]:
    """Cheap internal consistency, kept as a seam-level report.

    The rule itself now also lives in `ecosystem/schema/provider_registry.py`, which
    `provider_registry.load_registry()` enforces on every load — so in practice a violation
    raises `RegistryError` before this function is reached. It is retained deliberately
    rather than deleted: `run()`'s contract is that every finding is a returned STRING, and a
    caller that catches `RegistryError` at the boundary would otherwise lose the per-model
    detail. Belt and braces, with the braces load-bearing for the message.
    """
    out: list[str] = []
    known = set(_preg.providers())
    for mid, fields in _preg.models().items():
        pid = fields.get("provider")
        if pid not in known:
            out.append(f"registry: model `{mid}` names provider `{pid}`, which is not declared")
    return out


def run(root: Path | None = None) -> list[str]:
    """Every violation across every seam, in seam order. Empty list == clean.

    `root` selects the TREE being checked; the registry is always read from THIS repo. That is
    deliberate and is what makes the tmp-tree teeth tests possible — a checked-out copy is
    measured against the one source of truth, not against a copy of it.
    """
    r = Path(root) if root is not None else _REPO_ROOT
    findings: list[str] = []
    findings += check_registry_shape()
    findings += check_s8_tool_versions(r)
    findings += check_s9_artifact_reader(r)
    findings += check_s10_conformance_hub(r)
    findings += check_s17_playbook(r)
    findings += check_s26_settings(r)
    findings += check_s31_council_panel(r)
    findings += check_provenance_pins(r)
    findings += check_role_admission_evidence(r)
    return findings


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(argv[0]) if argv else _REPO_ROOT
    try:
        findings = run(root)
    except Exception as exc:                    # an internal error BLOCKS, never a silent pass
        print(f"check_provider_registry: INTERNAL ERROR: {exc}", file=sys.stderr)
        return 2
    if findings:
        print("provider/model registry disagreement — the registry is the source of truth:")
        for f in findings:
            print(f"  - {f}")
        print("\nFix the SITE to match ecosystem/provider-registry.yaml, or change the registry "
              "deliberately and let this gate carry the change to every other site.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
