# MySkills

个人技能库,包含 Claude Skills 和 Codex Skills。

## 目录结构

```
MySkills/
├── ClaudeSkills/          # Claude AI 技能集合
│   ├── antigravity-proxy/
│   ├── docker-nvml-monitor/
│   ├── docx-template-reformatter/
│   ├── midscene/
│   ├── omo-skills/
│   └── skill-creator/
└── CodexSkills/           # Codex 技能集合
    ├── do/
    ├── remotion-best-practices/
    ├── skill-creator/
    └── skill-installer/
```

## Claude Skills

### antigravity-proxy
Antigravity 代理自动配置工具。

**功能:**
- 自动安装和配置 graftcp + mihomo 代理
- TCP 劫持 Antigravity language server
- 自动检测版本更新（cron 每 5 分钟）
- 无需 sudo 权限，完全自动化

**使用场景:** Mac 本地 Antigravity 远程连接 Docker 容器开发，解决 AI 聊天连接失败

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

## Codex Skills

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

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
