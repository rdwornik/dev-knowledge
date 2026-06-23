# Structural-integrity fixture — doc side (#194 L1 scan)

An ISOLATED fixture for `scan_structural_integrity` / `build_edge_index`. It lives under
`tests/fixtures/` (never in `declaration_docs`, never under `scripts/`), so its tokens are
never a live edge — the structural tests copy it to a tmp tree and scan with roots pointed at
the copy. Each rule-ID below encodes exactly one structural state:

- `clean-ok` — declared here AND implemented in `impl.py` → resolved (the negative control).
- `dangling-doc-1` — declared here, NO `# rule:` in code → dangling_doc.
- `dup-doc-1` — declared on TWO doc sites (below) → duplicate_doc.
- `dup-code-1` — one doc site here, TWO code sites in `impl.py` → duplicate_code.

(`code-orphan-1` is declared NOWHERE here — it exists only as a `# rule:` in `impl.py`, so it
is a code→nonexistent-rule orphan.)

clean resolved edge <!-- rule: clean-ok -->
declared but unimplemented <!-- rule: dangling-doc-1 -->
duplicated on the doc side (first) <!-- rule: dup-doc-1 -->
duplicated on the doc side (second) <!-- rule: dup-doc-1 -->
single doc anchor for the duplicate-code case <!-- rule: dup-code-1 -->
