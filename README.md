# MySkills

个人技能库，包含 Claude Skills 和 Codex Skills。

当前仓库的默认主题已经收敛为：

- `Codex Workflow Stack`：复杂工程、长时执行、任务规划的主线技能栈
- `Optional Skills`：浏览器、视频、文档与其它专项能力

## 目录结构

```text
MySkills/
├── ClaudeSkills/              # Claude AI 技能集合
│   ├── auto_vibe_environments/
│   ├── antigravity-proxy/
│   ├── claude-gh-skills/
│   ├── docker-nvml-monitor/
│   ├── docx-template-reformatter/
│   ├── midscene/
│   ├── omo-skills/
│   ├── skill-creator/
│   └── zotero_control/
├── CodexSkills/               # Codex 技能集合
│   ├── WORKFLOW.md            # 工作流主线（推荐先读）
│   ├── OPTIONAL.md            # 非主线 skill 清单
│   ├── unified-workflow/
│   ├── cybernetic-systems-engineering/
│   ├── harness/
│   ├── harness-engineering/
│   ├── interview-to-plan/
│   ├── plan-to-issues/
│   ├── codex-csv-loop/
│   ├── do/
│   ├── remotion-best-practices/
│   ├── skill-creator/
│   └── skill-installer/
└── auto_vibe_environments/    # 开发环境自动部署工具
```

## 克隆

```bash
git clone https://github.com/wscffaa/MySkills.git
```

## 推荐阅读顺序

如果你第一次看这个仓库，先读：

1. `CodexSkills/WORKFLOW.md`
2. `CodexSkills/README.md`
3. 只有当主 workflow stack 不适合当前任务时，再看 `CodexSkills/OPTIONAL.md`

## Claude Skills

### auto_vibe_environments
开发环境自动部署和配置工具。

**功能:**
- 一键部署完整开发环境
- 自动安装 Agent Reach（多平台内容访问）
- 自动安装和认证 GitHub CLI
- NPM 包自动更新系统（支持 cron 定时任务）
- 自定义更新时间表
- 更新日志记录和监控

**使用场景:**
- 新环境快速部署
- 开发工具自动化安装
- 包管理自动化
- 多平台内容访问配置

**支持的工具:**
- Agent Reach: Twitter/X, YouTube, GitHub, Reddit, Bilibili, 微信公众号等
- GitHub CLI: 仓库管理、PR、Issue 操作
- NPM 自动更新: @anthropic-ai/claude-code, @openai/codex

### antigravity-proxy
Antigravity 代理自动配置工具。

**功能:**
- 自动安装和配置 graftcp + mihomo 代理
- TCP 劫持 Antigravity language server
- 自动检测版本更新（cron 每 5 分钟）
- 无需 sudo 权限，完全自动化

**使用场景:** Mac 本地 Antigravity 远程连接 Docker 容器开发，解决 AI 聊天连接失败

### claude-gh-skills
GitHub 工作流全生命周期自动化技能集，从需求到合并 PR。

**包含技能:**
- **gh-autopilot** — 端到端自动化：PRD→Issue→Project→实现→PR→合并
- **product-requirements** — 交互式需求收集与 PRD 生成
- **gh-create-issue** — 从 PRD/需求创建结构化 Issue
- **gh-issue-implement** — 单个 Issue 分析→开发→创建 PR
- **gh-pr-review** — 代码审查、修复问题、合并 PR
- **gh-project-implement** — Project 级别批量实现所有 Issue
- **gh-project-pr** — Project 级别批量创建 PR
- **gh-project-sync** — 根据 PRD 同步 Project 状态

**使用场景:** GitHub 项目管理自动化、批量 Issue 处理、PR 工作流

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

### skill-creator
Anthropic 官方 Skill 创建工具。

**功能:**
- 创建和优化 Claude Code skills
- 提供评估、打包、验证脚本
- 包含分析、比较、评分代理
- 支持技能基准测试和报告生成

**使用场景:** 创建新 skill、优化现有 skill、skill 开发和测试

### zotero_control
Zotero 文献库直接控制工具，通过 Python 脚本直接调用 Zotero Web API v3，无需安装 MCP Server，零依赖。

**功能:**
- 搜索文献（关键词、标签、集合、类型过滤）
- 获取单条文献详情（按 key 或 DOI）
- 生成格式化引用（APA、Chicago、MLA、IEEE 等 10000+ 样式）
- 提取 PDF 全文（需 Zotero Desktop 已索引）
- 文献 CRUD（创建、更新、批量删除）
- 集合管理（创建、列出、删除、嵌套）
- 标签管理（添加、删除、列出）
- API 密钥信息查询

**安装:**
```bash
# 复制到 Claude Code skills 目录
cp -r ClaudeSkills/zotero_control ~/.claude/skills/
# 编辑 config.json 填入你的 API Key 和 User ID
# API Key 从 https://www.zotero.org/settings/keys 获取
```

**使用场景:** 文献综述、批量引用生成、文献库整理、学术写作辅助

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
