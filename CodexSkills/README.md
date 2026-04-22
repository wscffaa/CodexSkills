# CodexSkills

可复用的 Codex skills 工作区，重点包含 `do` 编排技能与一整套分层工作流 skills。

## 包含内容

- `do/`：`$do` 显式激活技能、`/do` 与 `/do-csv` 协议、agents 配置、CSV 收尾守护脚本。
- `unified-workflow/`：总控工作流路由器。统一选择 `superpowers`、`CSE`、`harness`、`PRD/CSV` 的组合，并统一工作流产物路径。
- `cybernetic-systems-engineering/`：完整 CSE 方法论 skill，用于复杂工程问题的系统建模、控制合同和分层验证。
- `harness/`：Codex-native 长时任务编排器。提供项目内 `tasks.json` / `progress.log` / checkpoint / recovery。
- `harness-engineering/`：harness-first 的执行/验证回路方法论，适合 flaky、CI、弱复现和受限环境。
- `interview-to-plan/`：把模糊需求收敛为 `PRD`。
- `plan-to-issues/`：把 `PRD` 或结构化计划转换成 CSV 任务台账。
- `codex-csv-loop/`：外部 CSV ledger 驱动的长时、可恢复任务循环。
- `remotion-best-practices/`：Remotion 领域规则技能。
- `skill-creator/`、`skill-installer/`：技能创建与安装工具。

## 快速安装（推荐）

```bash
git clone https://github.com/wscffaa/CodexSkills.git

# 方式 1：安装单个 skill（示例：do）
cd CodexSkills/do
bash scripts/install_to_codex.sh

# 方式 2：按目录复制工作流 skill 到 ~/.codex/skills
cd ..
rsync -a \
  CodexSkills/unified-workflow \
  CodexSkills/cybernetic-systems-engineering \
  CodexSkills/harness \
  CodexSkills/harness-engineering \
  CodexSkills/interview-to-plan \
  CodexSkills/plan-to-issues \
  CodexSkills/codex-csv-loop \
  ~/.codex/skills/
```

安装完成后重启 Codex 会话。

## 在 Codex 中调用 `do`

```text
$do
/do <任务描述>
/do-csv <csv路径>
/do-csv
```

- `$do`：显式激活技能。
- `/do`：单任务 5 阶段编排。
- `/do-csv <csv路径>`：按依赖 wave 执行。
- `/do-csv`：从 `.codex/tasks/csv-checkpoint.json` 续跑。

## 推荐工作流

### 普通任务

```text
superpowers
```

### 复杂工程任务

```text
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

PRD 冻结后可继续：

```text
$plan-to-issues
```

或直接进入：

```text
$harness
```

## 新增工作流技能说明

### unified-workflow
总控路由器。先判断任务属于 tiny / normal / complex / large-vague / long-running，再决定调用哪条主线。

### cybernetic-systems-engineering
完整 CSE。适合跨模块、共享状态、测试全绿但系统失败、振荡复发等复杂工程问题。

### harness
长时执行器。提供项目内状态真源、checkpoint、恢复和依赖调度。

### harness-engineering
当执行/验证回路本身差时使用。比如 flaky、CI 弱信号、复现不稳定、权限受限。

### interview-to-plan
把模糊需求问清楚，产出项目内 PRD。

### plan-to-issues
把 PRD 拆成原子 CSV 台账。

### codex-csv-loop
当已有外部 CSV ledger 时，用它驱动长时循环执行。

## 稳定性设计（do）

- `/do-csv` 的 checkpoint/report 统一要求 `apply_patch` 落盘。
- 每个 wave 完成后立即落盘 `csv-wave<N>-report.md` 与 checkpoint。
- 返回前执行守护脚本，自动补齐缺失产物：
  `python ~/.codex/skills/do/scripts/csv_artifact_guard.py --task-dir .codex/tasks`
- `status=done` 时要求至少存在：
  `csv-checkpoint.json`、所有已完成 wave 报告、`csv-resume-report.md`、`csv-done.flag`。
