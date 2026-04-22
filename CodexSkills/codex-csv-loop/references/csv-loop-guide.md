# CSV Loop Guide

## Goal

Use an external ledger to make long-running work resumable, inspectable, and less sensitive to context loss.

## Recommended columns

- `ID`
- `Title`
- `Content`
- `Acceptance Criteria`
- `Review Requirements`
- `State`
- `Labels`

## Stable state machine

- `未开始`
- `进行中`
- `已完成`

Keep exactly one `进行中` row per active loop.

## Good atomic task properties

- Small enough to validate in one focused pass.
- Narrow impact boundary.
- Acceptance criteria reference observable behavior, commands, outputs, or files.
- Review requirements catch common regressions.

## Review + Rewind

Before closing a row:

1. Confirm all acceptance criteria with evidence.
2. Check boundary-local leftovers.
3. Verify no partial edits remain in the intended impact area.
4. Record blockers instead of silently skipping them.

## Anti-patterns

- Rows that are really entire epics.
- Subjective acceptance criteria.
- Marking tasks complete without running validation.
- Advancing to the next row while the previous row still has cleanup work.
- Treating CSV as a todo list instead of the source of truth for loop state.
