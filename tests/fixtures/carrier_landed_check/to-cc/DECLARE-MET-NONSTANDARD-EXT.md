carried-by: OPEN
lands-via: logs/result.jsonl, once the run lands it

## Fixture

A decision file whose stated landing home resolves on `main` (per the test's monkeypatched
`_is_blob_on_main`) but uses an extension (`.jsonl`) the organ's FIRST version's file-extension
allowlist did not name -- Codex terra review round 2, LANE-5B3-4-decision-debt: that version
silently missed exactly this class. The fixed version discriminates file-vs-directory by asking
git whether the resolved object is a blob, not by an extension list, so this is flagged.
