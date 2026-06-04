export const meta = {
  name: 'conformance-hub',
  description: 'Read-only documentation-conformance review of the .dev-knowledge repo: 3 verifiers (JOURNAL vs git, living-doc claims vs repo state, BACKLOG closure coherence) fan out, an adversarial skeptic kills false positives, a digest synthesizes. Findings are returned as structured data with a required evidence_command; agents never write.',
  phases: [
    { title: 'Stage 1 - verifiers', detail: '3 read-only verifiers fan out (Sonnet)' },
    { title: 'Stage 2 - skeptic', detail: 'adversarial review of all findings (Opus)' },
    { title: 'Stage 3 - digest', detail: 'synthesis sorted by severity (Opus)' },
  ],
}

const REPO = '.'  // repo root = cwd; portable across local + Linux cloud clone

const READONLY = [
  'You are STRICTLY READ-ONLY. You may Read files, run read-only git (git log, git show, git diff, "git log -p -S"), and grep.',
  'You MUST NOT write or edit any file (Write/Edit are denied this session anyway). Do NOT use Bash to write either (no Set-Content, no >, no New-Item).',
  'Operate ONLY within ' + REPO + '. Do NOT read or touch any sibling repo.',
  'Return your findings as the structured object only. NEVER write findings to disk.',
  'Every finding MUST include a concrete evidence_command: the exact git/grep/shell command (or file:line read) that PROVES or DISPROVES the claim. If you cannot produce such a command, DROP the finding entirely.',
].join(' ')

const findingSchema = {
  type: 'object',
  additionalProperties: false,
  properties: {
    domain: { type: 'string', description: 'journal | living-docs | backlog-closures' },
    claim: { type: 'string', description: 'the exact claim being checked' },
    location: { type: 'string', description: 'where the claim lives, e.g. JOURNAL.md:24 or ARCHITECTURE.md:421 or commit hash' },
    evidence_command: { type: 'string', description: 'exact command that proves/disproves the claim (REQUIRED)' },
    verdict: { type: 'string', enum: ['contradicted', 'unsupported', 'omitted'], description: 'contradicted=repo disproves it; unsupported=no corroborating evidence found; omitted=real work missing from the doc' },
    severity: { type: 'string', enum: ['high', 'med', 'low'] },
    note: { type: 'string', description: 'what the evidence actually shows' },
  },
  required: ['domain', 'claim', 'location', 'evidence_command', 'verdict', 'severity', 'note'],
}

const verifierSchema = {
  type: 'object',
  additionalProperties: false,
  properties: {
    verifier_id: { type: 'string' },
    checked_clean: { type: 'array', items: { type: 'string' }, description: 'claims/areas checked that produced NO finding (so absence is informative)' },
    findings: { type: 'array', items: findingSchema },
    summary: { type: 'string' },
  },
  required: ['verifier_id', 'checked_clean', 'findings', 'summary'],
}

const skepticSchema = {
  type: 'object',
  additionalProperties: false,
  properties: {
    surviving_findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          domain: { type: 'string' },
          claim: { type: 'string' },
          location: { type: 'string' },
          evidence_command: { type: 'string' },
          severity: { type: 'string', enum: ['high', 'med', 'low'] },
          proposed_fix: { type: 'string', description: 'one-line proposal only; no action' },
          skeptic_note: { type: 'string', description: 'why it survived' },
        },
        required: ['domain', 'claim', 'location', 'evidence_command', 'severity', 'proposed_fix'],
      },
    },
    killed_findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          kill_reason: { type: 'string', enum: ['opinion', 'style', 'true-but-irrelevant', 'documented-decision', 'evidence-not-definitive'] },
          kill_detail: { type: 'string', description: 'explanation; cite ADR id if documented-decision' },
        },
        required: ['claim', 'kill_reason', 'kill_detail'],
      },
    },
    survive_count: { type: 'number' },
    kill_count: { type: 'number' },
  },
  required: ['surviving_findings', 'killed_findings', 'survive_count', 'kill_count'],
}

const digestSchema = {
  type: 'object',
  additionalProperties: false,
  properties: {
    summary: { type: 'string' },
    findings_by_severity: {
      type: 'object',
      additionalProperties: false,
      properties: {
        high: { type: 'array', items: { type: 'string' } },
        med: { type: 'array', items: { type: 'string' } },
        low: { type: 'array', items: { type: 'string' } },
      },
      required: ['high', 'med', 'low'],
    },
    counts: {
      type: 'object',
      additionalProperties: false,
      properties: {
        raw_findings: { type: 'number' },
        survived_skeptic: { type: 'number' },
        killed_false_positive: { type: 'number' },
      },
      required: ['raw_findings', 'survived_skeptic', 'killed_false_positive'],
    },
    checked_clean: { type: 'array', items: { type: 'string' } },
    next_actions: { type: 'array', items: { type: 'string' } },
  },
  required: ['summary', 'findings_by_severity', 'counts', 'checked_clean', 'next_actions'],
}

const V1 = READONLY + '\n\nDOMAIN V1 - JOURNAL vs git reality.\n'
  + 'Read the LAST 10 entries (newest-first) of ' + REPO + '/JOURNAL.md. Each entry has Did / Result / Changes / (Abandoned) / Next lines.\n'
  + 'For each concrete claim of work done (Did/Result/Changes), corroborate it against git: use "git log --oneline -40", "git show <hash>", "git log -p -S \"<string>\" -- <file>", and direct file existence checks.\n'
  + 'SHALLOW-HISTORY GUARD: before flagging a JOURNAL entry commit SHA as absent, verify that SHA date falls within the available git history (the clone may be SHALLOW -- cloud clones start at the first push). SHAs older than the history boundary are OUT-OF-SCOPE, not findings.\n'
  + 'FLAG: (a) entries asserting work that git history does NOT show (verdict contradicted/unsupported); (b) significant merged work in git (recent commits/merges) that the last-10 JOURNAL entries do NOT mention (verdict omitted).\n'
  + 'Populate checked_clean with the claims you verified as TRUE (so their absence from findings is informative). Set verifier_id="V1".'

const V2 = READONLY + '\n\nDOMAIN V2 - Living-doc claims vs repo state.\n'
  + 'Scan these files for VERIFIABLE FACTUAL claims (counts, file paths, command names, "we do X via Y"): VISION.md, ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, protocols/ESSENTIALS.md. Do NOT scan protocols/PLAYBOOK.md (out of scope, too large).\n'
  + 'Check each claim against actual repo state: e.g. a count like "12 checks" -> "python scripts/audit.py checks" or grep the ALL_CHECKS registry; a file path -> test it exists; a command/hook name -> verify it exists in .pre-commit-config.yaml / scripts/ / .claude/commands/.\n'
  + 'FLAG mismatches with the exact file:line and the disproving command (verdict contradicted). Known reference class: hardcoded counts that drift. Only flag falsifiable claims; ignore prose/opinion.\n'
  + 'Populate checked_clean with the factual claims you verified as correct. Set verifier_id="V2".'

const V3 = READONLY + '\n\nDOMAIN V3 - BACKLOG <-> commits semantic coherence.\n'
  + 'Find backlog items CLOSED in the last ~3 weeks: "git log --all --since=\"2026-05-14\" --grep=\"closes \\[#\"". For each, "git show <hash>" to read the closing diff.\n'
  + 'Closed items LEAVE BACKLOG.md, so reconstruct the original item text from the removing diff (the "-" lines) or "git log -p -S \"[#<id>]\" -- BACKLOG.md".\n'
  + 'FLAG: closures whose diff does NOT deliver what the item text describes (verdict contradicted), and done-work that landed in git with NO backlog entry/closure (verdict omitted).\n'
  + 'Do NOT flag mere presence/absence of the "closes [#id]" TAG - the commit-msg hook already gates that syntax. Focus on SEMANTIC coherence: does the diff match the stated scope/Done-when?\n'
  + 'Populate checked_clean with closures you verified as coherent. Set verifier_id="V3".'

log('conformance-hub: read-only hub conformance review. Target ~80k tokens (single pass).')
log('budget.total=' + String(budget.total) + ' spent=' + budget.spent())

phase('Stage 1 - verifiers')
const [v1, v2, v3] = await parallel([
  () => agent(V1, { label: 'V1-journal-vs-git', phase: 'Stage 1 - verifiers', schema: verifierSchema, model: 'claude-sonnet-4-6' }),
  () => agent(V2, { label: 'V2-livingdoc-claims', phase: 'Stage 1 - verifiers', schema: verifierSchema, model: 'claude-sonnet-4-6' }),
  () => agent(V3, { label: 'V3-backlog-closures', phase: 'Stage 1 - verifiers', schema: verifierSchema, model: 'claude-sonnet-4-6' }),
])

const verifiers = [v1, v2, v3].filter(Boolean)
const raw = []
for (const v of verifiers) for (const f of (v.findings || [])) raw.push(f)
const cleanAll = []
for (const v of verifiers) for (const c of (v.checked_clean || [])) cleanAll.push((v.verifier_id || '?') + ': ' + c)
log('Stage 1 raw findings: ' + raw.length + ' (V1=' + (v1 ? v1.findings.length : 'null') + ' V2=' + (v2 ? v2.findings.length : 'null') + ' V3=' + (v3 ? v3.findings.length : 'null') + '). spent=' + budget.spent())

phase('Stage 2 - skeptic')
const skepticPrompt = READONLY + '\n\nYou are an ADVERSARIAL SKEPTIC. Below are ' + raw.length + ' findings from 3 read-only verifiers. Default to KILLING a finding unless its evidence_command definitively proves a real conformance problem.\n'
  + 'KILL if the finding is: opinion; style preference; technically-true-but-irrelevant; explainable by a documented decision (CONSULT ' + REPO + '/docs/decisions before deciding - cite the ADR id); or its evidence_command is not actually definitive.\n'
  + 'You MAY re-run any evidence_command yourself (read-only) to confirm before keeping. For each SURVIVOR set: severity (high/med/low), keep the evidence_command, and a one-line proposed_fix (PROPOSAL ONLY - take no action). For each KILL: claim + kill_reason + kill_detail.\n\n'
  + 'FINDINGS JSON:\n```json\n' + JSON.stringify(raw, null, 2) + '\n```'
const skeptic = await agent(skepticPrompt, { label: 'skeptic-adversarial', phase: 'Stage 2 - skeptic', schema: skepticSchema })

// Enforce the /goal-equivalent: no survivor without a state-based evidence_command reaches the digest.
const survivors = (skeptic.surviving_findings || []).filter(f => f.evidence_command && String(f.evidence_command).trim().length > 0)
const droppedNoEvidence = (skeptic.surviving_findings || []).length - survivors.length
log('Stage 2: survived=' + survivors.length + ' killed=' + (skeptic.kill_count || (skeptic.killed_findings || []).length) + ' dropped_no_evidence=' + droppedNoEvidence + '. spent=' + budget.spent())

phase('Stage 3 - digest')
const digestPrompt = 'Synthesize a documentation-conformance digest from the data below. Do not re-investigate; just synthesize faithfully.\n'
  + 'Produce: findings_by_severity (one-line each, sorted high->med->low, survivors only); counts {raw_findings=' + raw.length + ', survived_skeptic=' + survivors.length + ', killed_false_positive=' + ((skeptic.killed_findings || []).length) + '}; an explicit checked_clean list (so absence of findings is informative); a one-paragraph summary of overall doc health and the skeptic kill-rate; and next_actions ONLY if survivors exist (proposals for the operator, no action).\n\n'
  + 'SURVIVORS:\n```json\n' + JSON.stringify(survivors, null, 2) + '\n```\n\n'
  + 'KILLED:\n```json\n' + JSON.stringify(skeptic.killed_findings || [], null, 2) + '\n```\n\n'
  + 'CHECKED-CLEAN (from verifiers):\n```json\n' + JSON.stringify(cleanAll, null, 2) + '\n```'
const digest = await agent(digestPrompt, { label: 'digest-synthesis', phase: 'Stage 3 - digest', schema: digestSchema })

log('conformance-hub complete. spent=' + budget.spent())

return {
  raw_count: raw.length,
  raw_findings: raw,
  verifier_checked_clean: cleanAll,
  skeptic: { survive_count: survivors.length, kill_count: (skeptic.killed_findings || []).length, killed_findings: skeptic.killed_findings || [], dropped_no_evidence: droppedNoEvidence },
  survivors,
  digest,
}