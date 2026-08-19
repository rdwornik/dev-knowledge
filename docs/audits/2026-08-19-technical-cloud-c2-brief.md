# CLOUD C2 — [#82] PER-REPO AGENTIC-REVIEW PROFILES (draft pack) · read-only + drafts

Cloud lane. FIRST COMMIT = dispatch-stamp (this prompt as
`docs/audits/2026-08-19-technical-c2-review-profiles-contract.md`). **No index regeneration.**
Read-only + one artifact; no config/scripts writes.

CONTEXT: `[#82]` (E6, LIVE): define per-repository agentic-review profiles — which reviewer
lane(s), what severity focus, what artifact shape — per fleet repo class, instead of the hub's
one-size review. Current doctrine: reviewer=terra for every code-impact arc; adversarial=sol
when stakes warrant; review artifacts must carry a parseable `**Tally:**` and a title matching
the coverage check (`^# Codex Review` — lane A's artifact failed admission on exactly this;
read N5 pack §4.4 for both failure modes and design AGAINST them).

ITEMS (CLEAR/BLOCKED each):
1. Read the row + the fleet repo list (parity-surfaces members) + 3 recent review artifacts;
   derive the repo classes that actually differ (hub / deployed tool / pre-deploy).
2. **Draft profile schema** (YAML-shaped, in the artifact only): reviewer lane, trigger class,
   severity floor for FIX-BEFORE-MERGE, artifact title + Tally format REQUIRED BY THE CHECK
   (quote the check's regexes verbatim so profiles are admission-safe by construction).
3. **Draft the profiles** for the 2 walked repos + the hub; one paragraph on rollout order.
4. Name what needs a ruling vs what is mechanical adoption.
OUTPUT: `docs/audits/2026-08-19-technical-c2-review-profiles.md`. Commit, push, STOP packet.
NOT: no live config lands, no check edits, no profile enforcement.
