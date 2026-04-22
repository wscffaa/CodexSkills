---
name: interview-to-plan
description: Iterative requirements clarification and PRD generation. Use when the user has a vague idea and needs Codex to repeatedly question them, converge on goals, constraints, boundaries, deliverables, specification, acceptance criteria, and execution phases, then produce or refine a PRD. When routed through `unified-workflow`, use the injected `Artifacts:` path for the PRD; otherwise fall back to `docs/workflow/PRD.md`.
---

# Interview To Plan

Turn ambiguous requests into a reviewable PRD. When `unified-workflow` has already injected an artifact root, use that path. Otherwise use `docs/workflow/PRD.md`.
Drive the process with short interview rounds, explicit uncertainty tracking, and a fixed stopping rule.

## Core Rules

- Treat a vague idea as insufficient input. Do not draft the final PRD until critical unknowns are answered or explicitly recorded as assumptions or risks.
- Ask at most 3 high-leverage questions per round. Prefer the smallest question set that can change plan shape, cost, risk, or validation.
- After each round, summarize in three buckets: `Confirmed`, `Unclear`, `Assumption`.
- Keep at most one reasonable assumption per round, and label it.
- Mirror the user's language. Stay direct. Avoid style-heavy prose.
- If the user already provided enough information, skip more interview and draft the plan immediately.

## Classify The Request

Choose one mode before asking questions:

- `new-project`
- `project-recreation`
- `basicofr-paper`
- `hybrid`

Read `references/question-bank.md` and use only the section that matches the chosen mode.

## Mandatory Fields Before Final PRD

Do not finalize the PRD until each item below has either a concrete answer or an explicit placeholder:

- objective and success signal
- non-goals
- deliverables
- hard constraints
- boundaries and allowed deviations
- dependencies and required inputs
- validation and acceptance evidence
- major risks and open questions

If any item is missing, keep interviewing.

## Interview Loop

1. Identify the mode and the immediate deliverable.
2. Extract what is already known from the user's words.
3. Ask the next 1-3 questions with the highest information gain.
4. Update `Confirmed`, `Unclear`, and `Assumption`.
5. Repeat until the mandatory fields are closed enough to write the PRD.

## Produce The PRD

Default path:

- If `unified-workflow` injected a PRD path via `Artifacts:`, use that path.
- Otherwise use `docs/workflow/PRD.md`.

Use `assets/prd.template.md` as the starting structure.

When drafting:

- fill every section with concrete facts, explicit assumptions, or explicit unknowns
- order phases by dependency, not by cosmetic grouping
- write acceptance criteria as observable evidence: command, file, test, metric, report, or artifact
- keep unresolved questions visible; do not bury them in prose
- if the request is BasicOFR-related, include baseline, novelty claim, dataset and evaluation plan, compute budget, and paper deliverables

## Mode-Specific Notes

- `new-project`: clarify target user, core workflow, stack, deployment, deadline, and MVP boundary.
- `project-recreation`: clarify source of truth, required parity, allowed deviations, license or compatibility concerns, and validation oracle.
- `basicofr-paper`: clarify target venue, hypothesis, baseline, novelty, code-change scope, experiments, ablations, figures or tables, and submission deadline.

## Handoff

- If the user approves the PRD and wants atomic execution tasks, hand off to `plan-to-issues`.
- If the PRD is for BasicOFR execution, suggest the next relevant BasicOFR skill only after the PRD is accepted.

## Resources

- `references/question-bank.md`: mode-specific interview prompts and stopping rule
- `assets/prd.template.md`: reusable PRD skeleton
