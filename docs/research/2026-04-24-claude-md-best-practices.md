# Research Report

**Query:** What are the latest best practices for structuring CLAUDE.md files and AI coding agent instructions as of 2026?

**Generated:** 2026-04-24 11:20:24
**Total cost:** $0.0119
**Duration:** 1m 18s
**Sources found:** 9

## Provider Summary

| Provider | Status | Duration | Cost | Sources |
|----------|--------|----------|------|---------|
| perplexity | ok | 11s | $0.0119 | 7 |
| openai_mini | error | — | — | 0 |
| gemini | ok | 1m 18s | — | 2 |

## Summary

## Report from PERPLEXITY (perplexity) ### CLAUDE.md File Structuring Best Practices (2026) **Keep CLAUDE.md concise, under 60-200 lines per file to prevent Claude from ignoring rules, focusing only on non-inferable info like build commands, branch conventions, and architectural decisions.** [1][2][3] Include essentials such as common bash commands (e.g., `npm run test`), code style guidelines (e.g., "Use ES modules"), key file patterns, and testing instructions.[3] Use multiple CLAUDE.md files for monorepos or subfolders (e.g., root for general, `/frontend/CLAUDE.md` for specific context), with ancestor-descendant loading.[2][3] **Split large rules into `.claude/rules/` directories or skills folders for progressive disclosure, avoiding overload.** [1][2] Wrap critical rules in `<important if="...">` tags to ensure they're not skipped during compression or long files.[2][4] Apply a deletion framework: retain only instructions Claude can't infer elsewhere (e.g., from code/README), move context-specific ones to skills, and include `/compact` policy for consistent auto-compression.[1][4] | Element | Recommended Location | Purpose | Limits | |---------|----------------------|---------|--------| | Core rules (build cmds, styles) | CLAUDE.md (root/subdirs) | Permanent project brain | <60-200 lines [1][2] | | Overflow rules | `.claude/rules/` | On-demand loading | Multiple files [1][2] | | Hierarchical config | `.claude/settings.json` | Permissions, model, output styles | N/A [2] | | Memory persistence | CLAUDE.md + `@path` imports | Auto-memory across sessions | Avoid memory.md reliance [2] | **Hooks are mandatory for always-on enforcement (e.g., auto-lint post-save, block sensitive file writes via PreToolUse hooks with exit code 2); use CLAUDE.md for advisory, judgment-based rules like code conventions.** [4] ### AI Coding Agent Instructions and Skills Best Practices **Structure skills as complete folders: SKILL.md (core rules + index, <500 lines) + `references/`, `scripts/`, `examples/` subdirs for on-demand reading, avoiding deep nesting (keep references one level from SKILL.md).** [1][5] Use a "plan-then-execute" workflow: plan first, pause/refine, then code to reduce rework.[3] **Differentiate instruction types:** - **Commands**: `.claude/commands/` for repeated workflows (e.g., Git branching).[3] - **Agents/Sub-agents**: Delegate complex tasks with `/clear` resets; restrict `tools`, specify `model`/`skills` in configs.[3][4] - **Prompting**: Reference files/URLs/images specifically; use Git worktrees/branches for safety.[3] | Instruction Type | Use Case | Key Technique | |------------------|----------|---------------| | CLAUDE.md | Project memory | Central + sub-files [3] | | Skills | Modular knowledge | Folder structure, shallow refs [1][5] | | Custom Tools/Commands | Automation | Slash cmds, MCP integration [3] | | Hooks | Enforcement | Pre/PostToolUse JSON [4] | | Git Workflow | Safety | New branches per task [3] | **For monorepos/large projects, combine ancestor CLAUDE.md with `.claude/rules/` and project-specific `~/.claude/projects/<project>/memory/`.** [2] Test iteratively: if Claude errs post-removal, restore; prioritize hooks over advisory files for compliance.[1][4] ### Sources from this provider - [Source 1](https://discuss.huggingface.co/t/10-essential-claude-code-best-practices-you-need-to-know/174731) - [Source 2](https://github.com/shanraisshan/claude-code-best-practice) - [Source 3](https://www.eesel.ai/blog/claude-code-best-practices) - [Source 4](https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/) - [Source 5](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - [Source 6](https://uxplanet.org/claude-md-best-practices-1ef4f861ce7c) - [Source 7](https://aimaker.substack.com/p/anthropic-claude-updates-q1-2026-guide) --- ## Report from GEMINI (gemini) ## The Evolution of AI Collaboration: 2026's Best Practices for CLAUDE.md and Agent Instructions **Report Date:** April 24, 2026 **Research Analyst:** Gemini ### Executive Summary As of 2026, the interaction with AI coding agents has matured from simple prompt-and-response to a sophisticated, structured collaboration. The `CLAUDE.md` file, once a simple context-setting document, has evolved into the cornerstone of a multi-layered instruction architecture that governs AI agent behavior, project knowledge, and workflow automation. This report details the latest best practices for structuring `CLAUDE.md` files and AI coding agent instructions, emphasizing a shift towards "context engineering." This new paradigm prioritizes providing AI agents with the right information at the right time through a combination of persistent context, on-demand knowledge, and explicit, task-oriented instructions. The key takeaway for developers and teams is to treat the instruction of AI agents as a deliberate act of system design. A well-structured `CLAUDE.md` and a modular system of "skills" and "subagents" are no longer optional but essential for maximizing the efficiency, reliability, and scalability of AI-assisted software development. The most effective teams are those that invest in creating and maintaining a clear, concise, and evolving set of instructions for their AI collaborators. ### Key Findings 1. **Conciseness is Paramount:** The `CLAUDE.md` file should be a high-level guide, not an exhaustive document. The recommended length is under 200 lines, with an absolute maximum of around 300. Every line should be essential for preventing mistakes. 2. **Progressive Disclosure is the New Standard:** Instead of overloading the main `CLAUDE.md` file, best practices now dictate a "progressive disclosure" approach. This involves using a lean `CLAUDE.md` that points to more detailed information in separate files, often within a `.claude/skills/` directory. These "skills" are loaded on-demand, conserving the context window for the immediate task. 3. **The "WHAT, WHY, HOW" Framework Structures `CLAUDE.md`:** A successful `CLAUDE.md` file should onboard the AI agent by clearly defining the project's purpose, architecture, and operational procedures. This includes the tech stack (WHAT), the project's goals (WHY), and the specific commands and workflows for testing and building (HOW). 4. **Explicit Instructions Outperform Vague Directions:** Claude models respond best to direct and unambiguous instructions. Instead of saying "write good code," specify the coding conventions. For complex tasks, breaking them down into smaller, explicit steps significantly improves performance. 5. **Verification is a Force Multiplier:** Providing the AI agent with a clear way to verify its work is the single most effective way to improve performance. This can include commands to run tests, linting rules, or expected outputs. A recent best practice is to enforce a test-driven development (TDD) workflow for bug fixes directly within the `CLAUDE.md`. 6. **Skills and Subagents Enable Specialization:** The use of "skills" allows for the encapsulation of domain-specific knowledge and workflows that the AI can load as needed. For more complex tasks, "subagents" can be dispatched with specific roles and limited permissions, preventing context pollution and improving focus. 7. **Prompt Engineering is Evolving into Context Engineering:** The focus is shifting from crafting the perfect single prompt to designing a system that provides the AI with the necessary context at each step. This includes a combination of the persistent context in `CLAUDE.md`, the on-demand context from skills, and the immediate task-specific context in the user's prompt. ### Detailed Analysis The latest best practices for structuring `CLAUDE.md` files and AI coding agent instructions revolve around a multi-layered approach that balances persistent guidance with on-demand, specialized knowledge. This evolution is driven by the need to manage the AI's limited context window effectively and to provide increasingly complex instructions for a wider range of development tasks. **The Role of `CLAUDE.md` in 2026** The `CLAUDE.md` file serves as the foundational layer of instruction, providing the AI with a persistent "mental model" of the project. It is not a replacement for detailed documentation but rather a high-level briefing for a new team member. The most effective `CLAUDE.md` files are structured to answer three fundamental questions: * **WHAT is this project?** This section should concisely define the tech stack, project structure, and key architectural patterns. It's crucial to point to important configuration files like `package.json` or `tsconfig.json` rather than duplicating their contents. * **WHY does this project exist?** A brief, one-to-two-line description of the project's purpose helps the AI make better high-level decisions. * **HOW do we work on this project?** This is often the most detailed section, outlining essential commands for running the development environment, executing tests, and building the project. It should also specify coding conventions that differ from standard practices and any critical "do-not-do" rules. **Progressive Disclosure: The Power of Skills and Subagents** To keep the `CLAUDE.md` file lean and effective, the principle of "progressive disclosure" is now standard practice. This involves moving detailed, task-specific instructions out of the main `CLAUDE.md` and into a structured directory of "skills," typically located at `.claude/skills/`. A "skill" is a folder containing a `SKILL.md` file that provides detailed instructions for a specific task, such as performing a security review, writing database migrations, or generating a new component based on a template. The AI agent only loads the content of a skill when the current task matches the skill's description, thus preserving the context window. For even more complex workflows, developers are increasingly using "subagents." These are instances of the AI that are spun up with a specific, narrow focus and a restricted set of permissions. For example, during a debugging session, a `CLAUDE.md` file might instruct the main agent to first dispatch a subagent to write a failing test, and only then dispatch another subagent to fix the bug and make the test pass. **Task-Specific Instructions: From Project Setup to Maintenance** The content of your instructions should evolve with the development lifecycle. Here are some examples of how to structure your `CLAUDE.md` and prompts for different phases: * **New Project Setup:** The `CLAUDE.md` should be focused on the foundational architecture, tech stack, and initial setup commands. Prompts will be high-level, such as "Scaffold a new React component using our design system principles outlined in the `new-component` skill." * **Feature Development:** The `CLAUDE.md` will be stable, and the focus shifts to task-specific prompts that reference existing patterns and skills. For example: "Implement the user authentication flow as described in the product requirements document. Refer to the `auth-patterns` skill for our preferred implementation." * **Debugging:** A powerful pattern that has emerged is to enforce a test-driven debugging workflow in the `CLAUDE.md`. A rule like, "When a bug is reported, your first step is to write a failing test that reproduces the bug. Only after the test is written and failing should you attempt to fix the code," has proven to be highly effective. **The Rise of Context Engineering** Ultimately, the latest best practices represent a move from "prompt engineering" to "context engineering." The goal is not just to write a good prompt but to create an environment where the AI has access to all the necessary information to perform its tasks effectively. This involves a thoughtful combination of: * **Persistent Context:** The core principles and guidelines in `CLAUDE.md`. * **On-Demand Context:** The specialized knowledge encapsulated in skills. * **Dynamic Context:** The specific details of the current task provided in the user's prompt. ### Competing Perspectives While there is a strong consensus on the principles of conciseness and progressive disclosure, there are differing opinions on the best high-level frameworks for structuring the *content* of instructions, particularly within prompts. **Chain-of-Thought (CoT) vs. Direct Instruction:** * **Chain-of-Thought (CoT):** This technique encourages the AI to "think step by step" and articulate its reasoning process before providing a final answer. This can be particularly useful for complex problem-solving and debugging tasks, as it allows the developer to follow the AI's logic and identify any flawed assumptions. * **Direct Instruction:** Proponents of this approach argue that for many coding tasks, CoT can be overly verbose and consume unnecessary tokens. They advocate for providing very direct, explicit instructions on the desired output, especially when the task is well-defined. Some research in 2025 suggested that for highly advanced models, the benefits of CoT may be diminishing as they perform more implicit reasoning by default. **CRISPE Framework:** The CRISPE (Capacity, Role, Insight, Style, Persona, Experiment) framework offers a structured way to build prompts by defining: * **Capacity:** What the AI is capable of doing. * **Role:** The persona the AI should adopt (e.g., "You are a senior security engineer"). * **Insight:** The context for the task. * **Style:** The desired tone and format of the output. * **Persona:** The target audience for the response.

*(truncated — summarizer unavailable)*

---

## Full Research Report

## Report from PERPLEXITY (perplexity)

### CLAUDE.md File Structuring Best Practices (2026)

**Keep CLAUDE.md concise, under 60-200 lines per file to prevent Claude from ignoring rules, focusing only on non-inferable info like build commands, branch conventions, and architectural decisions.** [1][2][3] Include essentials such as common bash commands (e.g., `npm run test`), code style guidelines (e.g., "Use ES modules"), key file patterns, and testing instructions.[3] Use multiple CLAUDE.md files for monorepos or subfolders (e.g., root for general, `/frontend/CLAUDE.md` for specific context), with ancestor-descendant loading.[2][3]

**Split large rules into `.claude/rules/` directories or skills folders for progressive disclosure, avoiding overload.** [1][2] Wrap critical rules in `<important if="...">` tags to ensure they're not skipped during compression or long files.[2][4] Apply a deletion framework: retain only instructions Claude can't infer elsewhere (e.g., from code/README), move context-specific ones to skills, and include `/compact` policy for consistent auto-compression.[1][4]

| Element | Recommended Location | Purpose | Limits |
|---------|----------------------|---------|--------|
| Core rules (build cmds, styles) | CLAUDE.md (root/subdirs) | Permanent project brain | <60-200 lines [1][2] |
| Overflow rules | `.claude/rules/` | On-demand loading | Multiple files [1][2] |
| Hierarchical config | `.claude/settings.json` | Permissions, model, output styles | N/A [2] |
| Memory persistence | CLAUDE.md + `@path` imports | Auto-memory across sessions | Avoid memory.md reliance [2] |

**Hooks are mandatory for always-on enforcement (e.g., auto-lint post-save, block sensitive file writes via PreToolUse hooks with exit code 2); use CLAUDE.md for advisory, judgment-based rules like code conventions.** [4]

### AI Coding Agent Instructions and Skills Best Practices

**Structure skills as complete folders: SKILL.md (core rules + index, <500 lines) + `references/`, `scripts/`, `examples/` subdirs for on-demand reading, avoiding deep nesting (keep references one level from SKILL.md).** [1][5] Use a "plan-then-execute" workflow: plan first, pause/refine, then code to reduce rework.[3]

**Differentiate instruction types:**
- **Commands**: `.claude/commands/` for repeated workflows (e.g., Git branching).[3]
- **Agents/Sub-agents**: Delegate complex tasks with `/clear` resets; restrict `tools`, specify `model`/`skills` in configs.[3][4]
- **Prompting**: Reference files/URLs/images specifically; use Git worktrees/branches for safety.[3]

| Instruction Type | Use Case | Key Technique |
|------------------|----------|---------------|
| CLAUDE.md | Project memory | Central + sub-files [3] |
| Skills | Modular knowledge | Folder structure, shallow refs [1][5] |
| Custom Tools/Commands | Automation | Slash cmds, MCP integration [3] |
| Hooks | Enforcement | Pre/PostToolUse JSON [4] |
| Git Workflow | Safety | New branches per task [3] |

**For monorepos/large projects, combine ancestor CLAUDE.md with `.claude/rules/` and project-specific `~/.claude/projects/<project>/memory/`.** [2] Test iteratively: if Claude errs post-removal, restore; prioritize hooks over advisory files for compliance.[1][4]

### Sources from this provider
- [Source 1](https://discuss.huggingface.co/t/10-essential-claude-code-best-practices-you-need-to-know/174731)
- [Source 2](https://github.com/shanraisshan/claude-code-best-practice)
- [Source 3](https://www.eesel.ai/blog/claude-code-best-practices)
- [Source 4](https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/)
- [Source 5](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Source 6](https://uxplanet.org/claude-md-best-practices-1ef4f861ce7c)
- [Source 7](https://aimaker.substack.com/p/anthropic-claude-updates-q1-2026-guide)

---

## Report from GEMINI (gemini)

## The Evolution of AI Collaboration: 2026's Best Practices for CLAUDE.md and Agent Instructions

**Report Date:** April 24, 2026

**Research Analyst:** Gemini

### Executive Summary

As of 2026, the interaction with AI coding agents has matured from simple prompt-and-response to a sophisticated, structured collaboration. The `CLAUDE.md` file, once a simple context-setting document, has evolved into the cornerstone of a multi-layered instruction architecture that governs AI agent behavior, project knowledge, and workflow automation. This report details the latest best practices for structuring `CLAUDE.md` files and AI coding agent instructions, emphasizing a shift towards "context engineering." This new paradigm prioritizes providing AI agents with the right information at the right time through a combination of persistent context, on-demand knowledge, and explicit, task-oriented instructions.

The key takeaway for developers and teams is to treat the instruction of AI agents as a deliberate act of system design. A well-structured `CLAUDE.md` and a modular system of "skills" and "subagents" are no longer optional but essential for maximizing the efficiency, reliability, and scalability of AI-assisted software development. The most effective teams are those that invest in creating and maintaining a clear, concise, and evolving set of instructions for their AI collaborators.

### Key Findings

1.  **Conciseness is Paramount:** The `CLAUDE.md` file should be a high-level guide, not an exhaustive document. The recommended length is under 200 lines, with an absolute maximum of around 300. Every line should be essential for preventing mistakes.

2.  **Progressive Disclosure is the New Standard:** Instead of overloading the main `CLAUDE.md` file, best practices now dictate a "progressive disclosure" approach. This involves using a lean `CLAUDE.md` that points to more detailed information in separate files, often within a `.claude/skills/` directory. These "skills" are loaded on-demand, conserving the context window for the immediate task.

3.  **The "WHAT, WHY, HOW" Framework Structures `CLAUDE.md`:** A successful `CLAUDE.md` file should onboard the AI agent by clearly defining the project's purpose, architecture, and operational procedures. This includes the tech stack (WHAT), the project's goals (WHY), and the specific commands and workflows for testing and building (HOW).

4.  **Explicit Instructions Outperform Vague Directions:** Claude models respond best to direct and unambiguous instructions. Instead of saying "write good code," specify the coding conventions. For complex tasks, breaking them down into smaller, explicit steps significantly improves performance.

5.  **Verification is a Force Multiplier:** Providing the AI agent with a clear way to verify its work is the single most effective way to improve performance. This can include commands to run tests, linting rules, or expected outputs. A recent best practice is to enforce a test-driven development (TDD) workflow for bug fixes directly within the `CLAUDE.md`.

6.  **Skills and Subagents Enable Specialization:** The use of "skills" allows for the encapsulation of domain-specific knowledge and workflows that the AI can load as needed. For more complex tasks, "subagents" can be dispatched with specific roles and limited permissions, preventing context pollution and improving focus.

7.  **Prompt Engineering is Evolving into Context Engineering:** The focus is shifting from crafting the perfect single prompt to designing a system that provides the AI with the necessary context at each step. This includes a combination of the persistent context in `CLAUDE.md`, the on-demand context from skills, and the immediate task-specific context in the user's prompt.

### Detailed Analysis

The latest best practices for structuring `CLAUDE.md` files and AI coding agent instructions revolve around a multi-layered approach that balances persistent guidance with on-demand, specialized knowledge. This evolution is driven by the need to manage the AI's limited context window effectively and to provide increasingly complex instructions for a wider range of development tasks.

**The Role of `CLAUDE.md` in 2026**

The `CLAUDE.md` file serves as the foundational layer of instruction, providing the AI with a persistent "mental model" of the project. It is not a replacement for detailed documentation but rather a high-level briefing for a new team member. The most effective `CLAUDE.md` files are structured to answer three fundamental questions:

*   **WHAT is this project?** This section should concisely define the tech stack, project structure, and key architectural patterns. It's crucial to point to important configuration files like `package.json` or `tsconfig.json` rather than duplicating their contents.
*   **WHY does this project exist?** A brief, one-to-two-line description of the project's purpose helps the AI make better high-level decisions.
*   **HOW do we work on this project?** This is often the most detailed section, outlining essential commands for running the development environment, executing tests, and building the project. It should also specify coding conventions that differ from standard practices and any critical "do-not-do" rules.

**Progressive Disclosure: The Power of Skills and Subagents**

To keep the `CLAUDE.md` file lean and effective, the principle of "progressive disclosure" is now standard practice. This involves moving detailed, task-specific instructions out of the main `CLAUDE.md` and into a structured directory of "skills," typically located at `.claude/skills/`.

A "skill" is a folder containing a `SKILL.md` file that provides detailed instructions for a specific task, such as performing a security review, writing database migrations, or generating a new component based on a template. The AI agent only loads the content of a skill when the current task matches the skill's description, thus preserving the context window.

For even more complex workflows, developers are increasingly using "subagents." These are instances of the AI that are spun up with a specific, narrow focus and a restricted set of permissions. For example, during a debugging session, a `CLAUDE.md` file might instruct the main agent to first dispatch a subagent to write a failing test, and only then dispatch another subagent to fix the bug and make the test pass.

**Task-Specific Instructions: From Project Setup to Maintenance**

The content of your instructions should evolve with the development lifecycle. Here are some examples of how to structure your `CLAUDE.md` and prompts for different phases:

*   **New Project Setup:** The `CLAUDE.md` should be focused on the foundational architecture, tech stack, and initial setup commands. Prompts will be high-level, such as "Scaffold a new React component using our design system principles outlined in the `new-component` skill."
*   **Feature Development:** The `CLAUDE.md` will be stable, and the focus shifts to task-specific prompts that reference existing patterns and skills. For example: "Implement the user authentication flow as described in the product requirements document. Refer to the `auth-patterns` skill for our preferred implementation."
*   **Debugging:** A powerful pattern that has emerged is to enforce a test-driven debugging workflow in the `CLAUDE.md`. A rule like, "When a bug is reported, your first step is to write a failing test that reproduces the bug. Only after the test is written and failing should you attempt to fix the code," has proven to be highly effective.

**The Rise of Context Engineering**

Ultimately, the latest best practices represent a move from "prompt engineering" to "context engineering." The goal is not just to write a good prompt but to create an environment where the AI has access to all the necessary information to perform its tasks effectively. This involves a thoughtful combination of:

*   **Persistent Context:** The core principles and guidelines in `CLAUDE.md`.
*   **On-Demand Context:** The specialized knowledge encapsulated in skills.
*   **Dynamic Context:** The specific details of the current task provided in the user's prompt.

### Competing Perspectives

While there is a strong consensus on the principles of conciseness and progressive disclosure, there are differing opinions on the best high-level frameworks for structuring the *content* of instructions, particularly within prompts.

**Chain-of-Thought (CoT) vs. Direct Instruction:**

*   **Chain-of-Thought (CoT):** This technique encourages the AI to "think step by step" and articulate its reasoning process before providing a final answer. This can be particularly useful for complex problem-solving and debugging tasks, as it allows the developer to follow the AI's logic and identify any flawed assumptions.
*   **Direct Instruction:** Proponents of this approach argue that for many coding tasks, CoT can be overly verbose and consume unnecessary tokens. They advocate for providing very direct, explicit instructions on the desired output, especially when the task is well-defined. Some research in 2025 suggested that for highly advanced models, the benefits of CoT may be diminishing as they perform more implicit reasoning by default.

**CRISPE Framework:**

The CRISPE (Capacity, Role, Insight, Style, Persona, Experiment) framework offers a structured way to build prompts by defining:

*   **Capacity:** What the AI is capable of doing.
*   **Role:** The persona the AI should adopt (e.g., "You are a senior security engineer").
*   **Insight:** The context for the task.
*   **Style:** The desired tone and format of the output.
*   **Persona:** The target audience for the response.
*   **Experiment:** Encouraging the AI to try different approaches.

While comprehensive, some argue that the full CRISPE framework is too cumbersome for the fast-paced nature of coding and that a more streamlined approach focusing on role, context, and explicit instructions is more practical.

Ultimately, the most effective approach often involves a hybrid model. For complex, multi-step tasks, a CoT approach within a prompt can be beneficial. For more routine tasks, direct instructions are often more efficient. The CRISPE framework can be a useful mental model for ensuring all necessary context is provided, even if not all elements are explicitly stated in every prompt.

### Sources

1.  How to Write a CLAUDE.md File That Actually Works: Best Practices for API Projects. (2026, March 9). *TurboDocx Blog*.
2.  Best Practices for Claude Code. (n.d.). *Anthropic*.
3.  How to Set Up a Claude.md File That Actually Works. (2026, April 18). *MindStudio*.
4.  CLAUDE.md Best Practices. 10 Sections to Include in your… (2026, March 6). *UX Planet*.
5.  Writing a good CLAUDE.md. (2025, November 25). *HumanLayer Blog*.
6.  What to include in CLAUDE.md... and what not? (2026, March 9). *Reddit*.
7.  Best AI Prompt Generator for Anthropic 2026. (2026, April 16). *AI Prompt Engineering Blog*.
8.  claude-code-best-practice/CLAUDE.md at main. (2026, April 22). *GitHub*.
9.  How To Build An AI agent (2026). (2026, February 18). *Dust Blog*.
10. 150 Best Claude Prompts That Work in 2026. (2026, March 21). *Build Fast with AI*.
11. How to Build an AI Agent from Scratch in 2026: A Complete Step-by-Step Guide. (2026, March 21). *Generative AI Today*.
12. How to Build Your First AI Agent in 2026: A Practical Guide. (2026, March 20). *DEV Community*.
13. The simplest way to build AI agents in 2026. (2026, January 9). *Personal Blog*.
14. Claude Prompt Engineering Best Practices 2026: Checklist + Templates. (2025, December 13). *Prompt Engineering Pro*.
15. How to Build an AI Agent: A Practical Guide for 2026. (2026, January 20). *SolaceCode*.
16. Prompt Engineering for Developers: Production Patterns That Actually Work in 2026. (2026, April 16). *AI for Developers*.
17. How to Prompt Claude Opus 4.7 Differently Than 4.6. (2026, April 22). *MindStudio*.
18. The Setup Is the Strategy: How I Orchestrated a Product Migration with Claude Code. (2026, April 16). *Engineering Manager Blog*.
19. Claude Code Best Practices: Lessons From Real Projects. (2026, March 23). *Ran the Builder*.
20. Mastering Prompt Engineering for Claude. (2024, September 12). *Walturn*.
21. 8 Chain-of-Thought Prompts That Improved My AI Reasoning. (2025, September 18). *Medium*.
22. Prompting best practices. (n.d.). *Claude API Docs*.
23. The Decreasing Value of Chain of Thought in Prompting. (2025, June 8). *Wharton Generative AI Labs*.
24. 12 prompt engineering tips to boost Claude's output quality. (2024, February 2). *Vellum*.

### Sources from this provider
- [humanlayer.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEZi9iKXjqzU7TPKBARm8frLVaHODGoJY3Lp2H0GxN7nPUqAN1JP0Spn8AGoxCxSotQWY-yBd0AoO79oYUK_1ZtjZ4Re_PHq59pIWsIXToaPDb0cAxG34m0tlBo4kp1SziBQZXjmeJMYytYJ0QAXf1O7vDd)
- [upenn.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5i1CK5-cv695XqCtCYu8P6Ah6cW9l1_0nONPZrs305Q4T1tc-VjP5Hl_7En6xdvISQQXDZyLu0EK1fN8HOavj76XjpGWO3NSdeXyBYbAcjo5bgzHNwZy6P1irTY4WWDcP6HiUmSwDZ8EPL6YgJD7_ASyzMwXy_NIvX1w-5FrqrPvqJxCsbu2KJcOWScw=)

---
