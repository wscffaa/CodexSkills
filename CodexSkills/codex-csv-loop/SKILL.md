---
name: codex-csv-loop
description: Use only for long-running or batched development driven by an external CSV ledger. When routed through `unified-workflow`, use the injected ledger paths in `Artifacts:`; otherwise fall back to `docs/workflow/ledgers/issues.csv`. Best for unattended progress, resumable multi-issue work, or any request that needs atomic task loops with explicit acceptance criteria and persistent state.
metadata:
  short-description: CSV-driven long-running Codex workflow
---

# Codex CSV Loop

Use this skill for autonomous multi-task execution, not for normal one-off feature work.

## Trigger cues

- The user wants long-running or batch execution.
- The task list is large enough to need external state and resume safety.
- The user mentions `issues.csv`, task ledgers, unattended loops, or resumable automation.

## Required artifacts

- a PRD or equivalent design note
- a CSV ledger with objective acceptance criteria; prefer the `Artifacts:` path injected by `unified-workflow`
- A known validation path for each atomic task.

Starter files:

- `assets/issues.template.csv`
- `assets/execution-prompt.md`
- `assets/regression-tail-template.md`
- `references/csv-loop-guide.md`
- `references/checkpoint-lite.md`

## Hard rules

- Only one atomic task may be `进行中` at a time.
- Do not start coding before locking task state.
- Acceptance criteria must be observable and objective.
- After each task, run Review + Rewind inside the task boundary before moving on.
- Reserve at least one later task for regression or end-to-end verification.
- Do not enable this workflow unless the user wants batch or long-running execution.
- If the user explicitly invokes `/do` or `/do-csv`, prefer the `do` skill over this generic loop.

## Loop

1. Read the ledger and select the first eligible atomic task.
2. Lock it to `进行中`.
3. Implement only that task.
4. Validate against acceptance criteria and review requirements.
5. Rewind: scan for leftovers inside the intended impact boundary.
6. Persist the result and mark the task `已完成` only when evidence exists.
7. Continue to the next eligible task or stop with a clear checkpoint.

## When to stop and ask

- Acceptance criteria are ambiguous or not testable.
- The environment or permissions needed for validation are missing.
- A single row has grown too broad and should be split.
- The loop would require risky global changes not covered by the current row.

## Manual driving support

- If the user wants a reusable execution prompt instead of direct skill execution, load `assets/execution-prompt.md`.
- If the ledger lacks a proper final regression phase, use `assets/regression-tail-template.md` to append one.
- If execution is interrupted and the user wants a lightweight resume note, use `references/checkpoint-lite.md`.

## Load on demand

- Read `references/csv-loop-guide.md` for ledger design, state rules, and anti-patterns.
