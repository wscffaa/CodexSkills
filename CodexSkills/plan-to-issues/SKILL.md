---
name: plan-to-issues
description: Use only when the user explicitly wants to convert a PRD or another structured product or implementation spec into a CSV task ledger. When routed through `unified-workflow`, use the injected ledger paths in `Artifacts:`; otherwise fall back to `docs/workflow/ledgers/issues.draft.csv` and `docs/workflow/ledgers/issues.csv`. Do not use this skill to execute the tasks.
metadata:
  short-description: Convert a PRD into a CSV task ledger
---

# Plan to Issues

Use this skill to generate or refine an executable task ledger from a plan. It is a bridge between planning and execution, not an execution workflow.

## Trigger cues

- The user explicitly asks to turn a PRD into a CSV task ledger.
- The user wants issue rows or atomic executable task rows for a CSV ledger or another explicit task ledger from a structured plan.
- The user wants acceptance criteria and review checks generated from an existing plan.

## Do not use when

- The user explicitly invokes `/do` or `/do-csv`; prefer the `do` skill.
- A valid CSV ledger already exists and the user wants execution; prefer `codex-csv-loop`.
- The task is ordinary coding, planning-only, or review-only work.

## Required input

- A PRD or an equivalent structured product or implementation spec.
- Enough detail to identify scope, deliverables, dependencies, and validation paths.

## Output modes

Default output:
- injected ledger draft path from `Artifacts:`, if present
- otherwise `docs/workflow/ledgers/issues.draft.csv`

Execution-ready output:
- injected final ledger path from `Artifacts:`, if present
- otherwise `docs/workflow/ledgers/issues.csv`

Generate these columns exactly:

- `ID`
- `Title`
- `Content`
- `Acceptance Criteria`
- `Review Requirements`
- `State`
- `Labels`

Default row values:

- `State=未开始`
- `Labels=等待确认`

Starter asset:

- `assets/issues.template.csv`

## Workflow

1. Read the plan and extract goals, constraints, deliverables, dependencies, and validation expectations.
2. Convert deliverables into atomic tasks that can be implemented and verified in one focused pass.
3. For each row, write objective `Acceptance Criteria` tied to commands, tests, outputs, or files.
4. For each row, write `Review Requirements` covering regression, boundary checks, and leftover cleanup.
5. Order rows by dependency and execution safety.
6. Add at least one later regression or end-to-end verification row.
7. Self-audit the draft ledger for granularity, observability, and missing coverage before returning it.
8. If the user wants an execution-ready ledger, recommend `issues-auditor` before promoting the draft to the final ledger path.

## Hard rules

- One row must represent one atomic task.
- If a row cannot be validated objectively, split or rewrite it.
- If a row spans unrelated modules or risks, split it.
- Do not mark rows complete during generation; only prepare the ledger.
- Do not invent hidden requirements that are absent from the plan.
- If the plan has critical gaps, surface them explicitly and produce a conservative draft instead of pretending certainty.

## Interop

- Default to the injected draft ledger path unless the user explicitly asks for an execution-ready ledger; otherwise fall back to `docs/workflow/ledgers/issues.draft.csv`.
- If the user wants a reviewable ledger, stop after generating the draft ledger.
- If the user wants a production-ready ledger, suggest `issues-auditor` before finalizing the final ledger.
- If the user wants to continue into generic long-running execution after ledger approval, suggest `codex-csv-loop`.
- If the user wants formal orchestration or wave execution after ledger approval, suggest `/do-csv`.
- If the plan is a migration or parity project, borrow decomposition heuristics from `cross-language-refactor`, but keep the final output as plain CSV rows.

## Load on demand

- Read `references/plan-to-issues-guide.md` for decomposition heuristics, examples, and quality checks.
