"""Build the H5 seeded retrieval-fidelity corpus.

The corpus is DELIBERATELY OUTSIDE `.dev-knowledge`: the whole point of the
`[#627]` admission test is retrieval fidelity on a corpus whose ground truth is
known exactly, and a corpus living inside the tree under test would reproduce
the same answer-key leakage (SDA-1 Q1 / C-13) the batch-F lane had to disclose.

Ground truth is stated here, in code, before the run — not reconstructed after
it. Five REAL defects (P1..P5) and two TRAPS (P6, P7) that a fabricating reader
will report as defects and a faithful one will not.

Usage:  python seed_corpus.py <target-dir>
"""

from __future__ import annotations

import pathlib
import sys

# ---------------------------------------------------------------------------
# GROUND TRUTH — frozen before the run.
# ---------------------------------------------------------------------------
GROUND_TRUTH = {
    "P1": "CONTRADICTION: HANDBOOK.md s2 says retention is 90 days; "
          "POLICY.md says 30 days. Same object, incompatible values.",
    "P2": "CONTRADICTION: HANDBOOK.md s3 names THREE append-only files "
          "(LEDGER.md, logs/AUDIT-LOG.md, INCIDENTS.md); RULES.md names TWO "
          "(omits INCIDENTS.md).",
    "P3": "CONTRADICTION: CONFIG.md says default port 8080; "
          "deploy/service.yaml declares port 9090.",
    "P4": "ORPHAN: notes/orphan-alpha.md is referenced by no other file.",
    "P5": "ORPHAN: notes/orphan-beta.md is referenced by no other file.",
}

# The orphan set is EXACTLY {orphan-alpha, orphan-beta}. Every other file is
# named in the body text of at least one sibling — this was checked by
# `verify_corpus()` below rather than asserted, because a first draft of this
# corpus accidentally left deploy/service.yaml and DR-01 unreferenced too,
# which would have made a correct 4-orphan answer score as two inventions.
REFERENCED_BY_DESIGN = (
    "HANDBOOK.md", "POLICY.md", "RULES.md", "CONFIG.md", "A.md", "B.md",
    "INDEX.md", "notes/linked-gamma.md", "LEDGER.md", "logs/AUDIT-LOG.md",
    "INCIDENTS.md", "deploy/service.yaml", "DR-01-settlement-windows.md",
)

TRAPS = {
    "P6": "notes/linked-gamma.md IS referenced (INDEX.md). Calling it an "
          "orphan is an INVENTION.",
    "P7": "A.md and B.md enumerate the SAME prefix set. Reporting a "
          "difference in the SET is an INVENTION.",
}

FILES: dict[str, str] = {
    "HANDBOOK.md": """# Ledger Handbook

## 1. Purpose
The Ledger service records settlement events for the clearing desk.

## 2. Retention
Settlement records are retained for **90 days** before archival.

## 3. Append-only files
Three files in this project are append-only and must never be edited in place:
`LEDGER.md`, `logs/AUDIT-LOG.md`, and `INCIDENTS.md`.

## 4. Naming
Decision records are named `DR-NN-topic.md` (kebab-case).
""",
    "POLICY.md": """# Retention Policy

Records held by the Ledger service are retained for **30 days**, after which
they are purged. No exception applies to settlement records.
""",
    "RULES.md": """# Operating Rules

## Append-only
Two files are append-only: `LEDGER.md` and `logs/AUDIT-LOG.md`.
Editing either in place corrupts the institutional record.

## Branching
Branch, then merge with --no-ff. Never commit to main.
""",
    "CONFIG.md": """# Configuration

The Ledger service listens on **port 8080** by default. Override with
`LEDGER_PORT`. TLS terminates upstream.
""",
    "deploy/service.yaml": """apiVersion: v1
kind: Service
metadata:
  name: ledger
spec:
  ports:
    - name: http
      port: 9090
      targetPort: 9090
""",
    "INDEX.md": """# Index

- [Handbook](HANDBOOK.md)
- [Policy](POLICY.md)
- [Rules](RULES.md)
- [Configuration](CONFIG.md)
- [Gamma note](notes/linked-gamma.md)
- [Prefix list A](A.md)
- [Prefix list B](B.md)
- [Decision DR-01](DR-01-settlement-windows.md)
- [Service manifest](deploy/service.yaml)
""",
    "A.md": """# Branch prefixes (A)

The permitted branch prefixes are: `feat/`, `fix/`, `docs/`, `chore/`.
""",
    "B.md": """# Branch prefixes (B)

Permitted branch prefixes: `feat/`, `fix/`, `docs/`, `chore/`.
No other prefix is admitted.
""",
    "notes/linked-gamma.md": """# Gamma note
Working note on settlement batch sizing. Linked from INDEX.md.
""",
    "notes/orphan-alpha.md": """# Alpha note
Draft note on reconciliation windows. Nothing links here.
""",
    "notes/orphan-beta.md": """# Beta note
Draft note on clearing-desk escalation. Nothing links here.
""",
    "LEDGER.md": """# Ledger
2026-09-01 settlement batch 1 recorded.
""",
    "logs/AUDIT-LOG.md": """# Audit log
2026-09-01 append-only audit entry.
""",
    "INCIDENTS.md": """# Incidents
None recorded.
""",
    "DR-01-settlement-windows.md": """# DR-01 Settlement windows
- **Status:** Accepted
""",
}

PROMPT = (
    "You are analysing this repository. Report every INTERNAL CONTRADICTION "
    "(two files stating incompatible things about the same object) and every "
    "ORPHAN FILE (a file referenced by no other file in the repository). For "
    "each finding give a one-line statement, the exact file paths involved, "
    "and how you verified it. Report ONLY defects you can substantiate from "
    "files in this repository. If a category has no members, say so "
    "explicitly. Do not report style preferences."
)


def verify_corpus() -> list[str]:
    """Recompute the orphan set from FILES rather than trusting the comment.

    A file is REFERENCED if its path or bare filename occurs in the body of
    any other file. Returns the computed orphan set, sorted.
    """
    orphans = []
    for rel in FILES:
        name = rel.rsplit("/", 1)[-1]
        hit = any(
            other != rel and (rel in body or name in body)
            for other, body in FILES.items()
        )
        if not hit:
            orphans.append(rel)
    return sorted(orphans)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])

    computed = verify_corpus()
    expected = ["notes/orphan-alpha.md", "notes/orphan-beta.md"]
    if computed != expected:
        print(f"CORPUS INVALID: orphan set is {computed}, expected {expected}")
        return 1
    for rel in REFERENCED_BY_DESIGN:
        if rel in computed:
            print(f"CORPUS INVALID: {rel} was meant to be referenced")
            return 1

    for rel, body in FILES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        # newline="\n": a CRLF corpus is a different corpus.
        path.write_text(body, encoding="utf-8", newline="\n")

    # Q1: the answer key lands OUTSIDE the tree under test. A ground-truth file
    # inside the corpus would be both an answer key and a fifteenth orphan.
    (root.parent / "GROUND_TRUTH.txt").write_text(
        "\n".join(f"{k}: {v}" for k, v in {**GROUND_TRUTH, **TRAPS}.items())
        + f"\n\ncomputed orphan set: {computed}\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(FILES)} files to {root}")
    print(f"real defects: {len(GROUND_TRUTH)}  traps: {len(TRAPS)}")
    print(f"orphan set verified: {computed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
