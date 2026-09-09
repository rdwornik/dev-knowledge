# 1b - repo B: Architekt-Jutra/architekt-jutra-code

**Reader:** agy - **ORDERED**, invocation CORRECTED once. Not a substitution.
**Model:** gemini-3.8-flash-low.
**Source:** git clone --depth 1 https://github.com/Architekt-Jutra/architekt-jutra-code into a temp dir, READ-ONLY, 1044 files. No code from it was copied anywhere.
**First attempt FAILED SILENTLY:** printed DONE at exit 0 and wrote no file (same failure as 1a-L04).
**Exact invocation (the one that answered):** agy --model gemini-3.8-flash-low --print-timeout=15m --dangerously-skip-permissions --add-dir . --print=<repo-B audit prompt>, run from the clone root, printing to stdout.
**Wall time:** ~7 min.
**Delivery:** stdout; two duplicate renders removed on capture.
**R2 status:** locators in this table are UNVERIFIED unless a row is marked otherwise, or unless this file is named in `R2-VERIFICATION.md`. Per R1/R2 nothing here is dropped; unverified content is carried and labelled.

---

| FINDING | LOCATOR | CATEGORY | EVIDENCE-QUOTE |
|---|---|---|---|
| Showcase application implementing microkernel plugin-based architecture with Spring Boot and Vite/TS plugins | README.md:1-5 | implements | "A showcase application demonstrating the **microkernel (plugin-based) architecture** pattern built with Java 25 and Spring Boot 4." |
| Exposes host product/category operations as Model Context Protocol (MCP) tools via Spring MVC | mcp-server/pom.xml:19-24 | implements | "<groupId>io.modelcontextprotocol.sdk</groupId>\n            <artifactId>mcp-spring-webmvc</artifactId>" |
| Autonomous agent incident diagnosis benchmark using Neo4j knowledge graph | tools/kg-incidents/README.md:1-4 | implements | "Benchmark ewaluacyjny badający wpływ narzędzia MCP z grafem wiedzy (Neo4j) na skuteczność i efektywność agenta AI (Claude Code)" |
| Orchestrator state file tracking workflow phases, auto-fix attempts, and options | .maister/tasks/development/2026-03-28-microkernel-skeleton-app/orchestrator-state.yml:1-14 | shape-statefile | "orchestrator:\n  started_phase: phase-1\n  completed_phases: [phase-1, phase-2, phase-5, phase-6, phase-7, phase-8, phase-10, phase-11, phase-12, phase-14]\n  failed_phases: []\n  auto_fix_attempts: {}\n  options:" |
| No repository-level Claude hooks present in `.claude/hooks` | CLAUDE.md:19-21 | shape-hooks | "When any `/maister:*` command is invoked, execute it via the Skill tool immediately — do not skip workflows for \"straightforward\" tasks." |
| Slash command definition delegating research data collection | week7/3-research-gatherer-demo/research-gatherer-standalone/commands/research/gather.md:1-6 | shape-commands | "name: research-gather\ndescription: Gather and verify research data from multiple sources without synthesis\n---\n\n**ACTION REQUIRED**: This command delegates to a different skill. The `<command-name>` tag refers to THIS command, not the target. Call the Skill tool with skill=\"research-gatherer\" NOW." |
| Standalone subagent definition with mandated file outputs and isolated context | week7/3-research-gatherer-demo/research-gatherer-standalone/agents/information-gatherer-lite.md:1-6 | shape-agents | "name: information-gatherer-lite\ndescription: Information gathering specialist for research-gatherer workflow. Uses simplified internal/external/mixed classification. Systematic data collection with source citations and evidence.\nmodel: inherit\ncolor: green" |
| Knowledge base query skill definition for Claude Code querying Neo4j MCP server | .claude/skills/aj-kg-query/SKILL.md:1-4 | shape-agents | "name: aj-kg-query\ndescription: Answer questions about the AJ platform... by querying the AJ knowledge graph in Neo4j via the `neo4j-aj-kb` MCP server." |
| No CI workflows present in repository (no `.github/workflows` or CI configs) | pom.xml:1-15 | shape-ci | "<groupId>pl.devstyle</groupId>\n    <artifactId>aj</artifactId>\n    <version>0.0.1-SNAPSHOT</version>\n    <name>aj</name>\n    <description>Showcase application for microkernel architecture</description>" |
| LiteLLM proxy configuration with Presidio PII guardrails and Langfuse callbacks | litellm/config.yaml:12-24 | shape-gateway | "guardrails:\n  - guardrail_name: \"presidio-pii\"\n    litellm_params:\n      guardrail: presidio\n      mode: \"pre_call\"\n      default_on: true\n      presidio_ad_hoc_recognizers: \"presidio_recognizers.json\"\n      pii_entities_config:\n        CREDIT_CARD: BLOCK\n        PHONE_NUMBER: MASK\n        EMAIL_ADDRESS: MASK\n        PL_PESEL: MASK" |
| Task lifecycle phases from codebase analysis through spec audit, plan, and verification | .maister/tasks/development/2026-05-20-footprint-calc-engine/SUMMARY.md:24-33 | lifecycle | "| Phase | Output | Outcome |\n|---|---|---|\n| 1 Codebase analysis | `analysis/codebase-analysis.md` + `analysis/clarifications.md` | risk medium-high; 4 critical decisions resolved |\n| 2 Gap analysis | `analysis/gap-analysis.md` + `analysis/scope-clarifications.md` | additive build, ~52 components in 10 groups; 5 important decisions resolved |\n| 5 Specification | `implementation/spec.md` (17 sections) + `analysis/requirements.md` | implementation-ready |\n| 6 Spec audit | `verification/spec-audit.md` | pass-with-concerns; 2 critical + 6 warning + 1 info — all resolved inline before planning |\n| 7 Implementation plan | `implementation/implementation-plan.md` (10 task groups, 6 waves) + `implementation/visual-coverage.md` | plan green-lit |\n| 8 Implementation | code + `implementation/work-log.md` | 10/10 task groups complete (parallel wave dispatch); 160 active tests, 0 regressions |\n| 11 Verification (5 reviewers) | `verification/implementation-verification.md` + 4 inline sub-reports | pass-with-issues → all 16 findings (2 critical + 14 warning) fixed inline |\n| 14 Finalisation | this `SUMMARY.md` | task closed |" |
| Append-only work log tracking task step execution and standards consultation | .maister/tasks/development/2026-03-28-microkernel-skeleton-app/implementation/work-log.md:3-6 | lifecycle | "## 2026-03-28 - Implementation Started\n\n**Total Steps**: 24\n**Task Groups**: Group 1 (Database Foundation), Group 2 (Microkernel Core Interfaces), Group 3 (Backend API Layer), Group 4 (React Frontend & Maven Build Integration), Group 5 (Test Review & Gap Analysis)" |
| Human review and approval required when coding standards conflict with task requirements | CLAUDE.md:7 | human-in-loop | "Follow standards in `.maister/docs/standards/` when writing code — they represent team decisions. If standards conflict with the task, ask the user." |
| Human approval required before evolving and updating development standards | CLAUDE.md:17 | human-in-loop | "When this happens, briefly suggest the standard to the user. If approved, invoke `/maister:standards-update` with the identified pattern." |
| Human review gate evaluating deployment readiness with GO/NO-GO verdict | .maister/tasks/development/2026-03-28-microkernel-skeleton-app/verification/reality-check.md:5-9 | human-in-loop | "**Status**: NOT READY -- Critical gap in Success Criterion #1\n\n---\n\n## Deployment Decision: NO-GO" |
| Human context input point where domain materials and designs are dropped for AI ingestion | .maister/tasks/product-design/2026-03-28-ecommerce-product-management/context/README.md:1-3 | human-in-loop | "Drop files here for the design process — meeting transcripts, existing designs, spreadsheets, docs, PDFs, images, or any other relevant materials." |


---

## Rows this file is evidence for

- **[#627]** - *the agy route is INERT; no row authorizes its analysis-role admission.* This file IS agy output produced in an analysis role, with its invocation, model and wall time recorded. It is a measurement against that row, not an authorization of it.
- **[#676]** - *no check verifies a provider CLI's non-interactive invocation shape.* The R3 header above records the shape that worked, and where a first attempt failed, the shape that did not.

