# Codex Workflow Stack

这是 `MySkills/CodexSkills` 的默认主题。

如果你只想知道“这套技能库现在最主要的部分是什么”，答案不是所有技能，而是下面这条工作流主线：

## Core Workflow Skills

- `unified-workflow`
- `cybernetic-systems-engineering`
- `harness`
- `harness-engineering`
- `interview-to-plan`
- `plan-to-issues`
- `codex-csv-loop`

## 这条主线分别做什么

| Skill | 作用 |
|---|---|
| `unified-workflow` | 总控路由：先决定应该走哪条工作流 |
| `cybernetic-systems-engineering` | 复杂工程任务的方法论与控制合同 |
| `harness` | 长时、可恢复、跨会话的项目内执行状态机 |
| `harness-engineering` | 当执行/验证回路本身不可靠时，先修回路 |
| `interview-to-plan` | 把模糊任务冻结成 PRD |
| `plan-to-issues` | 把 PRD 拆成可评审/可执行的任务台账 |
| `codex-csv-loop` | 当已有 CSV ledger 时，按 ledger 长时推进 |

## 推荐主线

### 普通任务

```text
superpowers
```

### 复杂工程任务

```text
$unified-workflow
$cybernetic-systems-engineering
```

### 长时复杂任务

```text
$unified-workflow
$cybernetic-systems-engineering
$harness
```

### 模糊大型任务

```text
$unified-workflow
$interview-to-plan
```

PRD 冻结后：

```text
$plan-to-issues
```

或者直接：

```text
$harness
```

## 统一产物目录

默认工作流产物根：

```text
<project-root>/docs/workflow/
```

标准路径：

```text
docs/workflow/PRD.md
docs/workflow/specs/
docs/workflow/plans/
docs/workflow/ledgers/
docs/workflow/reviews/
docs/workflow/decisions/
docs/workflow/harness/
```

## 不属于主线的技能

其余 Codex skills 默认都视为 optional。先把这条 workflow stack 跑通，再考虑其它专项能力。
