"""K1.7 link migration script — one-shot, safe to re-run."""
import os

SKIP_NAMES = {'JOURNAL.md', 'LESSONS.md', 'TOKEN-LOG.md'}

ADR_RENAMES = [
    ('ADR-27_scope-tagging', 'ADR-27-scope-tagging'),
    ('ADR-28_three-layer-architecture', 'ADR-28-three-layer-architecture'),
    ('ADR-29_lessons-grandfathering', 'ADR-29-lessons-grandfathering'),
    ('ADR-30_default_branch_main', 'ADR-30-default-branch-main'),
    ('ADR-31_authority_model', 'ADR-31-authority-model'),
    ('ADR-32_handoff_format', 'ADR-32-handoff-format'),
    ('ADR-33_vision_universalization', 'ADR-33-vision-universalization'),
    ('ADR-34_file_naming_convention', 'ADR-34-file-naming-convention'),
    ('ADR-35_lessons_base_activation', 'ADR-35-lessons-base-activation'),
    ('ADR-36_audit_tool_architecture', 'ADR-36-audit-tool-architecture'),
    ('ADR-37_session_boundary_protocol', 'ADR-37-session-boundary-protocol'),
    ('ADR-38_universal_repo_architecture', 'ADR-38-universal-repo-architecture'),
    ('ADR-39_file_lifecycle_governance', 'ADR-39-file-lifecycle-governance'),
    ('ADR-40_scale_tier_evaluation', 'ADR-40-scale-tier-evaluation'),
    ('ADR-41_cross_session_backlog_architecture', 'ADR-41-cross-session-backlog-architecture'),
    ('ADR-42_handoff_format_v3', 'ADR-42-handoff-format-v3'),
]

TRANSCRIPT_RENAMES = [
    ('council_out_20260428_125133_format-and-structure-of-visionmd-for-dev',
     'council-out-20260428-125133-format-and-structure-of-visionmd-for-dev'),
    ('council_out_20260428_162415_pick_council_prompt_adr33_vision_universalization',
     'council-out-20260428-162415-pick-council-prompt-adr33-vision-universalization'),
    ('council_out_20260429_190922_pick_council_adr34_file_naming_convention',
     'council-out-20260429-190922-pick-council-adr34-file-naming-convention'),
    ('council_out_20260429_210057_pick_council_adr35_lessons_base_activation',
     'council-out-20260429-210057-pick-council-adr35-lessons-base-activation'),
    ('council_out_20260430_123043_pick_council_adr36_audit_tool_architecture',
     'council-out-20260430-123043-pick-council-adr36-audit-tool-architecture'),
    ('council_out_20260430_125039_research_question-what-prior-art-exists-for-cross-repo-audi',
     'council-out-20260430-125039-research-question-what-prior-art-exists-for-cross-repo-audi'),
    ('council_out_20260430_132308_pick_council_adr37_two_phase_handoff',
     'council-out-20260430-132308-pick-council-adr37-two-phase-handoff'),
    ('council_out_20260430_134721_pick_council_adr38_scrum_framework',
     'council-out-20260430-134721-pick-council-adr38-scrum-framework'),
    ('council_out_20260430_150751_research_question-for-a-solo-developer-with-multiple-active',
     'council-out-20260430-150751-research-question-for-a-solo-developer-with-multiple-active'),
    ('council_out_20260430_154818_research_question-how-should-an-llm-driven-multi-repo-ecosy',
     'council-out-20260430-154818-research-question-how-should-an-llm-driven-multi-repo-ecosy'),
    ('council_out_20260509_143831_research_brief-for-ai-council-architect-browser-session-con',
     'council-out-20260509-143831-research-brief-for-ai-council-architect-browser-session-con'),
    ('council_out_20260509_144836_research_question-how-should-an-llm-driven-solo-developer-a',
     'council-out-20260509-144836-research-question-how-should-an-llm-driven-solo-developer-a'),
    ('council_out_20260511_205022_pick_2026-05-11-council-question-ecosystem-separator',
     'council-out-20260511-205022-pick-2026-05-11-council-question-ecosystem-separator'),
    ('council_out_20260511_210100_judge_COUNCIL_QUESTION_adr-01-synthesizer-panel-refresh',
     'council-out-20260511-210100-judge-council-question-adr-01-synthesizer-panel-refresh'),
]

# Template pattern replacement — updates naming convention descriptions
PATTERN_RENAMES = [
    # Naming convention template in README
    ('council_out_YYYYMMDD_HHMMSS_{slug}.md', 'council-out-YYYYMMDD-HHMMSS-{slug}.md'),
    ('council_out_YYYYMMDD_HHMMSS_*.md', 'council-out-YYYYMMDD-HHMMSS-*.md'),
    # _archive path references → archive
    ('docs/handoffs/_archive/', 'docs/handoffs/archive/'),
    ('_archive/{slug}/', 'archive/{slug}/'),
    ('_archive/2026-05-09-ai-council-audit-sync/', 'archive/2026-05-09-ai-council-audit-sync/'),
    ('_archive/2026-05-09-dev-knowledge-session-sync/', 'archive/2026-05-09-dev-knowledge-session-sync/'),
    # Remaining _archive/ references
    ('handoffs/_archive/', 'handoffs/archive/'),
    ('_in_progress/{slug}/*" "docs/handoffs/_archive/{slug}/', '_in_progress/{slug}/*" "docs/handoffs/archive/{slug}/'),
    ('"docs/handoffs/_archive/{slug}"', '"docs/handoffs/archive/{slug}"'),
]


def should_skip(rel_path):
    basename = os.path.basename(rel_path)
    if basename in SKIP_NAMES:
        return True
    # Skip legacy archive (frozen point-in-time artifacts)
    if 'archive/legacy/' in rel_path:
        return True
    # Skip docs/audits (point-in-time audit snapshots)
    if rel_path.startswith('docs/audits/'):
        return True
    # Skip council transcript content (only rename filenames, not body text per prompt note)
    if rel_path.startswith('docs/decisions/transcripts/'):
        fn = basename
        if (fn.startswith('council-out-') or fn.startswith('council_out_') or
                fn.startswith('DECISION_')):
            return True
    return False


def apply_all(content):
    # Apply transcript renames (longer/more specific first)
    for old, new in TRANSCRIPT_RENAMES:
        content = content.replace(old, new)
    # Apply ADR renames
    for old, new in ADR_RENAMES:
        content = content.replace(old, new)
    # Apply pattern/path renames
    for old, new in PATTERN_RENAMES:
        content = content.replace(old, new)
    return content


changed = []
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__'}]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(root, fn)
        rel = os.path.relpath(path, base).replace(os.sep, '/')
        if should_skip(rel):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()
        updated = apply_all(original)
        if updated != original:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(updated)
            changed.append(rel)

print(f"Modified {len(changed)} files:")
for f in sorted(changed):
    print(f"  {f}")
