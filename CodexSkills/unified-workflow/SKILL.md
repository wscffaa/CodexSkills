---
name: unified-workflow
description: Use as the total-control workflow router for non-trivial work. Chooses between superpowers, CSE, harness, and PRD/CSV, and standardizes workflow artifact paths under `docs/workflow/`.
metadata:
  short-description: Total workflow router
---

# Unified Workflow

Use this skill when the question is not "how do I edit this line", but "which workflow should this task use?"

This skill is the **total-control router**. It does not replace:

- `superpowers`
- `cybernetic-systems-engineering`
- `harness`
- `harness-engineering`
- `interview-to-plan`
- `plan-to-issues`

It decides which of those should lead.

## Use When

Use this skill when any of these are true:

- the task is non-trivial and you need to choose the right workflow
- the user asks about the overall workflow
- the task may need `superpowers`, `CSE`, `harness`, or `PRD`
- the task spans design, planning, execution, review, or long-running orchestration
- the user asks where workflow artifacts should be stored

## Output Contract

When this skill is active, first answer with these five fields:

```text
Task Class:
Primary Workflow:
Escalations:
Artifacts:
Next Step:
```

Keep the answer short and decisive.

## Artifact Injection Contract

When this router selects a child workflow, it also owns the artifact root for that task.

The router must explicitly set artifact paths in `Artifacts:` and those paths override any child skill defaults for the current task.

Required artifact root:

```text
<project-root>/docs/workflow/
```

Required default targets:

- `docs/workflow/PRD.md`
- `docs/workflow/specs/`
- `docs/workflow/plans/`
- `docs/workflow/ledgers/`
- `docs/workflow/reviews/`
- `docs/workflow/decisions/`
- `docs/workflow/harness/`

Do not rely on plugin-cache edits to enforce these paths. Inject them at routing time.

## Routing Rules

### `tiny`

- single-file
- low-risk
- no shared interface or shared state impact

Workflow:

```text
direct execution -> minimum validation
```

### `normal`

- multi-step but bounded
- ordinary implementation, bugfix, or refactor

Workflow:

```text
superpowers
```

### `complex`

- crosses modules
- touches shared state or shared interfaces
- code plus config/data/process changes
- tests pass but the system still fails
- recurrence or oscillation

Workflow:

```text
superpowers -> cybernetic-systems-engineering
```

### `large-vague`

- target not frozen
- deliverables unclear
- multiple phases or deliverables
- needs formal design freeze

Workflow:

```text
interview-to-plan -> superpowers -> (cybernetic-systems-engineering if needed) -> (harness if needed)
```

### `long-running`

- resumable
- checkpointed
- unattended or multi-session
- project-local execution state needed

Workflow:

```text
harness
```

If the task is both complex and long-running:

```text
superpowers -> cybernetic-systems-engineering -> harness
```

If the execution or verification loop is weak:

```text
... -> harness-engineering
```

## Artifact Root

All workflow artifacts should default to:

```text
<project-root>/docs/workflow/
```

Standard paths:

```text
docs/workflow/PRD.md
docs/workflow/specs/
docs/workflow/plans/
docs/workflow/ledgers/
docs/workflow/reviews/
docs/workflow/decisions/
docs/workflow/harness/
```

## Rules

1. `PRD` is the design-layer artifact for large or vague work.
2. `CSV` is an exchange/review/import-export format.
3. `docs/workflow/harness/tasks.json` is the runtime source of truth for long-running execution.
4. Do not treat `CSV` as the default execution truth when a project-local harness state exists.
5. Do not let this router duplicate the full content of child skills. Route, inject artifact paths, then hand off.

## Load on Demand

- Read `references/workflow-map.md` for the full layer model and examples.
