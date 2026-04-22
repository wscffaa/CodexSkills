# MySkills

个人技能库，包含 Claude Skills 和 Codex Skills。

当前仓库的默认主题已经收敛为：

- `Codex Workflow Stack`：复杂工程、长时执行、任务规划的主线技能栈
- `Optional Skills`：浏览器、视频、文档与其它专项能力

## 目录结构

```
MySkills/
├── WORKFLOW.md            # 仓库主线主题
├── OPTIONAL.md            # 可选技能说明
├── Codex/                 # Codex 主题导航层
│   ├── workflow/
│   └── optional/
├── Claude/                # Claude 主题导航层
│   ├── workflow/
│   └── optional/
├── shared/                # 跨平台共享文档/示例/安装入口
│   ├── docs/
│   ├── examples/
│   └── install/
├── ClaudeSkills/          # Claude AI 技能集合
│   ├── docker-nvml-monitor/
│   ├── docx-template-reformatter/
│   ├── midscene/
│   └── omo-skills/
└── CodexSkills/           # Codex 技能集合
    ├── WORKFLOW.md        # 工作流主线（推荐先读）
    ├── OPTIONAL.md        # 非主线 skill 清单
    ├── unified-workflow/
    ├── cybernetic-systems-engineering/
    ├── harness/
    ├── harness-engineering/
    ├── interview-to-plan/
    ├── plan-to-issues/
    ├── codex-csv-loop/
    ├── do/
    ├── remotion-best-practices/
    ├── skill-creator/
    └── skill-installer/
```

## 克隆

```bash
git clone https://github.com/wscffaa/MySkills.git
```

## 推荐阅读顺序

如果你第一次看这个仓库，先读：

1. `WORKFLOW.md`
2. `Codex/workflow/README.md`
3. `Claude/workflow/README.md`
4. 只有当主 workflow stack 不适合当前任务时，再看 `OPTIONAL.md`

## Claude Skills

### docker-nvml-monitor
Docker 容器 GPU 监控和自动重启工具。

**功能:**
- 使用 `docker exec nvidia-smi` 实时检测容器内 GPU 状态
- 检测到 NVML 错误时,等待 GPU 进程完成后再重启容器
- 支持多容器监控,自动记录日志

**使用场景:** GPU 容器 NVML 错误、自动化监控恢复、避免实验中断

### docx-template-reformatter
Word 文档模板重排版工具。

**功能:**
- 将论文/报告按目标期刊/会议模板重新排版
- 保留图片、公式、分节、双栏、页眉页脚
- 输出可验收的校验报告

**使用场景:** 论文投稿、期刊模板排版、文档格式转换

### midscene
AI 驱动的浏览器自动化测试工具。

**功能:**
- 使用 Midscene + Puppeteer 生成自动化测试
- 支持自然语言命令交互网页
- 自定义 AI 模型配置(OpenAI 兼容端点)

**使用场景:** UI 自动化测试、Web 爬取、测试脚本生成

### omo-skills
多代理编排框架技能集合。

**功能:**
- 提供多个预定义的专业代理(oracle, librarian, develop 等)
- 支持复杂任务的多代理协作
- 集成 codeagent-wrapper 多后端支持

**使用场景:** 复杂开发任务、多步骤工作流、代理编排

## Codex Skills

### 主线：Codex Workflow Stack

以下 skill 组成当前仓库的默认主线：

- `unified-workflow`
- `cybernetic-systems-engineering`
- `harness`
- `harness-engineering`
- `interview-to-plan`
- `plan-to-issues`
- `codex-csv-loop`

如果你的任务属于：
- 非平凡开发
- 复杂工程问题
- 长时/可恢复执行
- PRD / CSV 驱动任务

优先看这条主线，不要先跳到 optional skills。

更适合从以下入口理解：

- `Codex/workflow/README.md`
- `Codex/optional/README.md`

### unified-workflow
总控工作流路由器。

**功能:**
- 统一选择 `superpowers`、`CSE`、`harness`、`PRD/CSV`
- 统一工作流产物目录到 `docs/workflow/`
- 为子技能注入本轮产物路径

**使用场景:** 非平凡任务的工作流分流、复杂任务主线选择、统一产物落盘

### cybernetic-systems-engineering
完整 CSE 方法论技能。

**功能:**
- 复杂工程任务的系统建模
- `Control Contract v2`
- 分层验证与护栏定义

**使用场景:** 跨模块、共享状态、测试全绿但真实环境失败、振荡复发

### harness
Codex-native 长时任务编排器。

**功能:**
- 项目内 `tasks.json` / `progress.log`
- checkpoint / recovery / dependency-aware run loop
- 支持 `import-csv`

**使用场景:** 长时、可恢复、跨会话推进的任务

### harness-engineering
harness-first 的执行/验证回路方法论。

**功能:**
- 先修复测试/CI/复现链路
- 设定 harness level 和升级阈值
- 证据驱动调试

**使用场景:** flaky、CI 弱信号、环境受限、复现链路不可信

### interview-to-plan
把模糊需求收敛为 PRD。

**功能:**
- 迭代式需求澄清
- 冻结边界、约束、交付物、验收标准
- 生成项目内 PRD

**使用场景:** 大型模糊任务、研究任务、跨阶段任务

### plan-to-issues
把 PRD 或结构化计划转换成 CSV 台账。

**功能:**
- 生成 `issues.draft.csv` / `issues.csv`
- 写原子任务、客观验收标准、review 要求
- 为后续 ledger 执行做准备

**使用场景:** 任务台账生成、PRD 任务化、批量执行前拆解

### codex-csv-loop
外部 CSV ledger 驱动的长时执行循环。

**功能:**
- 读取 `issues.csv`
- 单任务锁定、实现、验证、回卷、续跑
- 适合无人值守或批量执行

**使用场景:** 已有 CSV 台账的长时执行

### do
多代理任务编排技能。

**功能:**
- 按 /do 或 /do-csv 协议执行多代理任务编排
- 支持 5 阶段结构化执行
- 任务状态管理和依赖解析

**使用场景:** 复杂任务分解、多代理协作、批量任务处理

### remotion-best-practices
Remotion 视频创建最佳实践。

**功能:**
- React 视频创建的领域知识
- 字幕、音频可视化、FFmpeg 操作指南
- 动画、转场、3D 效果最佳实践

**使用场景:** Remotion 视频开发、React 动画、视频编辑

### skill-creator
Codex 技能创建指南。

**功能:**
- 创建和更新 Codex skills 的完整指南
- 提供技能结构、最佳实践、测试方法
- 支持技能打包和分发

**使用场景:** 创建新技能、优化现有技能、技能开发

### skill-installer
Codex 技能安装器。

**功能:**
- 从 GitHub 仓库安装 Codex skills
- 支持精选技能列表和私有仓库
- 列出可用技能和安装管理

**使用场景:** 安装技能、管理技能库、技能分发

### Optional Skills

当前不属于 workflow 主线、默认视为 optional 的 Codex skills：

- `do`
- `remotion-best-practices`
- `skill-creator`
- `skill-installer`

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
