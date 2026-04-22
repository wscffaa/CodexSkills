# Harness Porting Notes

This Codex-native harness is adapted from `stellarlinkco/myclaude`'s `skills/harness`, but it is not a byte-for-byte port.

## Preserved

- project-local state files
- append-only progress log
- structured task state
- dependency-aware scheduling
- checkpoint records
- interruption recovery
- lock-based single-controller safety

## Changed for Codex

- No Claude command hooks (`SessionStart`, `Stop`, `TeammateIdle`, `SubagentStop`)
- No slash commands (`/harness init`, `/harness run`, etc.)
- Explicit script entrypoints instead:
  - `python3 ~/.codex/skills/harness/scripts/harness.py init ...`
  - `status`
  - `add`
  - `run`
  - `import-csv`
- State lives under `docs/workflow/harness/` instead of project root
- First version defaults to exclusive single-controller mode
- Recovery is conservative: recover to the task boundary, not arbitrary mid-edit continuation

## Integration Rules

- Use `cybernetic-systems-engineering` for systems framing
- Use `harness-engineering` when the verification loop is weak
- Use this `harness` skill when the task itself is long-running or resumable
- Keep `do` and `codex-csv-loop` as separate orchestrators
- Keep `PRD` as a design-layer artifact and `CSV` as an exchange/import format
- Treat `docs/workflow/harness/tasks.json` as the runtime source of truth once execution begins

## First-Version Safety Bias

- No automatic hook-driven loop
- No hidden background workers
- No multi-worker shared-state execution by default
- Rollback on task failure requires explicit enablement
