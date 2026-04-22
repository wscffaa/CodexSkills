---
name: harness
description: Use for long-running, resumable Codex work that needs project-local state, checkpointing, failure recovery, and dependency-aware task execution.
metadata:
  short-description: Codex-native long-running harness
---

# Harness

Codex-native long-running task orchestrator.

Use this skill when the task needs more than a single plan/execution burst:

- multi-session autonomous progress
- resumable task queues
- project-local checkpoints and logs
- dependency-aware task ordering
- repeated validation after each atomic task

Do **not** use this for ordinary one-shot feature work. For those, keep using:

- `superpowers:writing-plans`
- `superpowers:executing-plans`
- `superpowers:subagent-driven-development`

Use this skill when the problem is "keep working reliably across sessions", not just "how do I edit code".

## Relationship to Other Skills

- `cybernetic-systems-engineering`:
  - use when the task is a complex engineering/system problem
  - if the task is also long-running or resumable, combine it with this skill
- `harness-engineering`:
  - use when the execution or verification loop itself is weak
  - combine it with this skill for flaky CI, weak repros, constrained environments
- `codex-csv-loop`:
  - use that when the source of truth is an external ledger such as `issues.csv`
  - use this skill when the source of truth should live in project-local harness state
- `do`:
  - use `do` for multi-agent wave orchestration
  - use this skill for persistent single-controller execution with recovery

## Artifact Roles

- `PRD` is the design artifact for large or ambiguous work
- `CSV` is an exchange, review, or import/export format
- `docs/workflow/harness/tasks.json` is the runtime source of truth for long-running execution

Do not treat `CSV` as the default execution truth when a project-local harness state exists.

## State Layout

All harness state lives inside the project:

```text
docs/workflow/harness/
  tasks.json
  tasks.json.bak
  progress.log
  .active
  init.sh            # optional, idempotent
```

## Commands

Run the controller script directly:

```bash
python3 ~/.codex/skills/harness/scripts/harness.py init <project-path>
python3 ~/.codex/skills/harness/scripts/harness.py status <project-path>
python3 ~/.codex/skills/harness/scripts/harness.py add <project-path> "task title" \
  --acceptance-criteria "..." \
  --validation-command "..."
python3 ~/.codex/skills/harness/scripts/harness.py run <project-path>
python3 ~/.codex/skills/harness/scripts/harness.py import-csv <project-path> <issues.csv>
```

## Trigger Rules

Trigger this skill when any of the following are true:

- the user wants long-running or resumable execution
- the task should continue across multiple Codex sessions
- a complex task needs explicit project-local checkpoints
- the user says `harness`, `resume later`, `continue tomorrow`, `keep working`, `long-running`, `任务编排`, or `自动继续`

For complex engineering tasks, prefer:

```text
$cybernetic-systems-engineering
$harness
```

For complex tasks with weak execution loops, prefer:

```text
$cybernetic-systems-engineering
$harness
Use harness-engineering for the weak verification loop.
```

## Operating Rules

1. Initialize state before adding or running tasks.
2. Keep exactly one controller writing `tasks.json` at a time.
3. One atomic harness task must have one observable validation command.
4. Do not mark a task completed without validation evidence.
5. On interrupted `in_progress` tasks, recover to the task boundary before proceeding.
6. Keep the final summary traceable: changed files, validation, residual risks.

## Task Fields

Each harness task may contain:

- `id`
- `title`
- `description`
- `acceptance_criteria`
- `status`
- `priority`
- `depends_on`
- `attempts`
- `max_attempts`
- `started_at_commit`
- `validation.command`
- `validation.timeout_seconds`
- `workflow.cse`
- `workflow.harness_engineering`
- `on_failure.cleanup`
- `on_failure.rollback`
- `error_log`
- `checkpoints`
- `completed_at`

See `assets/task-template.json`.

## Recovery Model

- interrupted tasks are recovered at the **task boundary**
- recovery is stateful and logged in `progress.log`
- rollback on task failure is available, but only when explicitly enabled in task policy or run flags

## Load on Demand

- Read `references/porting-notes.md` for the differences versus the upstream Claude harness
- Read `assets/task-template.json` before creating tasks programmatically
