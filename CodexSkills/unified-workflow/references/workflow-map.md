# Unified Workflow Map

## Core Layers

- `superpowers` = stage routing
- `cybernetic-systems-engineering` = complex systems framing
- `harness` = long-running execution
- `interview-to-plan` = PRD generation for large/vague work
- `plan-to-issues` = optional CSV ledger generation

## Default Main Flows

### Tiny

```text
direct execution -> minimum validation
```

### Normal

```text
superpowers
```

### Complex

```text
superpowers -> CSE
```

### Long-running Complex

```text
superpowers -> CSE -> harness
```

### Large / Vague

```text
PRD -> superpowers -> (CSE if needed) -> (harness if needed)
```

## Artifact Paths

```text
docs/workflow/PRD.md
docs/workflow/specs/
docs/workflow/plans/
docs/workflow/ledgers/
docs/workflow/reviews/
docs/workflow/decisions/
docs/workflow/harness/
```

## Injection Rule

`unified-workflow` owns the artifact root for the current task.

If a child skill documents another default path, the current task should still use the paths above when routed through `unified-workflow`.

## Non-goals

- do not replace `superpowers`
- do not replace `CSE`
- do not replace `harness`
- do not make `CSV` the runtime source of truth
