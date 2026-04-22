# Unified Workflow Map

## Core Layers

- `superpowers` = 阶段路由
- `cybernetic-systems-engineering` = 复杂系统建模
- `harness` = 长时执行
- `interview-to-plan` = 大型/模糊任务的 PRD 生成
- `plan-to-issues` = 可选 CSV 台账生成

## Main Flows

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

### Frozen PRD -> Ledger

```text
plan-to-issues
```

## Artifact Root

```text
docs/workflow/PRD.md
docs/workflow/specs/
docs/workflow/plans/
docs/workflow/ledgers/
docs/workflow/reviews/
docs/workflow/decisions/
docs/workflow/harness/
```

## Fixed File Whitelist

- `docs/workflow/PRD.md`
- `docs/workflow/ledgers/issues.draft.csv`
- `docs/workflow/ledgers/issues.csv`
- `docs/workflow/harness/tasks.json`
- `docs/workflow/harness/tasks.json.bak`
- `docs/workflow/harness/progress.log`
- `docs/workflow/harness/.active`
- `docs/workflow/harness/init.sh`

Allowed filename patterns:

- `docs/workflow/specs/YYYY-MM-DD-<topic>-design.md`
- `docs/workflow/plans/YYYY-MM-DD-<feature>-implementation.md`
- `docs/workflow/reviews/review-YYYY-MM-DD-<topic>.md`
- `docs/workflow/decisions/ADR-YYYY-MM-DD-<topic>.md`

Do not invent new artifact names outside this set.

## Injection Rule

`unified-workflow` 负责在本轮任务中注入统一产物路径。

即使子技能文档写着其他默认目录，只要本技能已生效，本轮就应优先使用上面的 `docs/workflow/...` 路径。
