# Checkpoint Lite

Use this when execution is interrupted but the full `/do-csv` checkpoint system would be overkill.

## Minimum resume note

Record at least:

- current row ID and title
- current state (`未开始` / `进行中` / `已完成`)
- blocker or stop reason
- last verified evidence
- next suggested resume command or prompt

## Example

```md
### CSV Resume Note
- 当前任务: `Row 7 - Add auth failure tests`
- 当前状态: `进行中`
- 阻塞原因: `test fixture missing`
- 已验证证据: `unit auth middleware tests pass`
- 下一步建议: `补 fixture 后继续执行 row 7`
```

## Rules

- Never claim a row is finished if the last evidence is incomplete.
- Prefer a short, honest resume note over a fake clean stop.
- Keep the note focused on the current row, not the whole project.
