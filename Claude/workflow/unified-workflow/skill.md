---
name: unified-workflow
description: 总控工作流路由器。用于为非平凡任务选择 `superpowers`、`CSE`、`harness`、`PRD/CSV` 的正确组合，并统一工作流产物目录到 `docs/workflow/`。
---

# unified-workflow

当问题不是“怎么改一行代码”，而是“这个任务应该走哪条工作流”时，使用本技能。

本技能是总控路由器，不替代以下子技能：

- `superpowers`
- `cybernetic-systems-engineering`
- `harness`
- `harness-engineering`
- `interview-to-plan`
- `plan-to-issues`

它只负责判断主线和产物路径。

## 触发场景

- 用户询问“应该走哪条工作流”
- 任务是 non-trivial，需要判断是否升级到 `CSE`、`harness`、`PRD`
- 用户询问工作流产物应该保存到哪里
- 任务横跨设计、规划、执行、审查、长时推进

## 输出契约

先输出这五项：

```text
Task Class:
Primary Workflow:
Escalations:
Artifacts:
Next Step:
```

保持简短、直接、可执行。

硬约束：

- 当用户要求“只输出 Task Class、Primary Workflow、Escalations、Artifacts、Next Step”时，必须只输出这五项，不要追加其他标题、解释或自由扩展。
- `Artifacts:` 只能引用本技能白名单中的固定路径或固定文件名模式。
- 不允许自造文件名，例如：
  - `task-ledger.md`
  - `execution-plan.md`
  - `plan.md`
  - 任意未在白名单中的自定义名字
- 如果不确定具体文件名，优先输出目录路径或标准模式，不要创造新名字。

## 产物路径注入契约

当本技能选择某条子工作流时，由本技能统一决定本轮的产物根目录。

要求：

- 在 `Artifacts:` 中显式写出本轮产物根和具体目标路径
- 这些路径优先于子技能文档里写的默认路径
- 不要长期依赖修改插件缓存来维持路径约定，而是由本技能在路由时注入

默认产物根：

```text
<project-root>/docs/workflow/
```

默认目标路径：

- `docs/workflow/PRD.md`
- `docs/workflow/specs/`
- `docs/workflow/plans/`
- `docs/workflow/ledgers/`
- `docs/workflow/reviews/`
- `docs/workflow/decisions/`
- `docs/workflow/harness/`

固定文件白名单：

- `docs/workflow/PRD.md`
- `docs/workflow/ledgers/issues.draft.csv`
- `docs/workflow/ledgers/issues.csv`
- `docs/workflow/harness/tasks.json`
- `docs/workflow/harness/tasks.json.bak`
- `docs/workflow/harness/progress.log`
- `docs/workflow/harness/.active`
- `docs/workflow/harness/init.sh`

允许的文件名模式：

- `docs/workflow/specs/YYYY-MM-DD-<topic>-design.md`
- `docs/workflow/plans/YYYY-MM-DD-<feature>-implementation.md`
- `docs/workflow/reviews/review-YYYY-MM-DD-<topic>.md`
- `docs/workflow/decisions/ADR-YYYY-MM-DD-<topic>.md`

## 路由规则

### `tiny`

- 单文件
- 低风险
- 不影响共享接口或共享状态

主线：

```text
direct execution -> minimum validation
```

### `normal`

- 多步但边界清楚

主线：

```text
superpowers
```

### `complex`

- 跨模块
- 共享状态或共享接口
- 代码 + 配置 / 数据 / 流程联动
- 测试全绿但系统仍失败
- 复发、振荡、长 bug hunt

主线：

```text
superpowers -> cybernetic-systems-engineering
```

### `large-vague`

- 目标未冻结
- 交付物不清楚
- 有多个阶段或 deliverables
- 需要正式冻结边界

主线：

```text
interview-to-plan -> superpowers -> (cybernetic-systems-engineering if needed) -> (harness if needed)
```

Artifacts 白名单：

- `docs/workflow/PRD.md`
- `docs/workflow/specs/`
- `docs/workflow/plans/`
- `docs/workflow/ledgers/`
- `docs/workflow/harness/`

### `frozen-prd-to-ledger`

- the PRD is already approved or frozen
- the user wants only a task ledger
- no implementation yet

主线：

```text
plan-to-issues
```

Artifacts 白名单：

- `docs/workflow/PRD.md`
- `docs/workflow/ledgers/issues.draft.csv`
- `docs/workflow/ledgers/issues.csv`

### `long-running`

- 跨会话
- 可恢复
- 需要 checkpoint
- 需要 unattended progress

主线：

```text
harness
```

如果同时也是复杂工程问题：

```text
superpowers -> cybernetic-systems-engineering -> harness
```

如果执行/验证回路弱，再叠：

```text
... -> harness-engineering
```

Artifacts 白名单：

- `docs/workflow/harness/tasks.json`
- `docs/workflow/harness/tasks.json.bak`
- `docs/workflow/harness/progress.log`
- `docs/workflow/harness/.active`
- `docs/workflow/harness/init.sh`

## 统一产物根

所有通用工作流产物默认收口到：

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

## 规则

1. `PRD` 是设计层 artifact。
2. `CSV` 是交换 / 审阅 / 导入导出格式。
3. `docs/workflow/harness/tasks.json` 是长时执行的运行时真源。
4. 不要让 `CSV` 成为默认执行真源。
5. 本技能不复制子技能全文，只负责路由、产物路径注入和交接。
6. 当任务命中 `frozen-prd-to-ledger` 时，`Artifacts:` 只能引用 `PRD.md` 与 `issues*.csv`；禁止输出任何自造 ledger 文件名。

## 最小输出模板

当用户要求“只输出 Task Class、Primary Workflow、Escalations、Artifacts、Next Step”时，按下面的模板原样作答：

```text
Task Class: <tiny|normal|complex|large-vague|frozen-prd-to-ledger|long-running>

Primary Workflow: <single primary workflow path>

Escalations:
- <only real escalation conditions>

Artifacts:
- <only allowed path 1>
- <only allowed path 2>

Next Step: <one shortest next step>
```

## 参考

- `references/workflow-map.md`
