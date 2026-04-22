---
name: harness-engineering
description: Use only when progress is blocked by a weak execution or verification loop rather than a simple code edit. Best for CI failure triage, long debugging chains, flaky environments, permission-constrained work, or tasks that need harness-first execution with explicit evidence and escalation thresholds.
metadata:
  short-description: Harness-first, evidence-driven execution
---

# Harness Engineering

Use this skill when the problem is not just code, but the execution loop around the code.

## Trigger cues

- Progress is blocked by a weak or missing test, log, CI, or repro loop.
- The task is a long bug hunt, CI fix, flaky failure, or constrained-environment repair.
- The user wants autonomous progress, but the current feedback loop is not trustworthy enough.
- Success depends on repairing the execution loop, not just editing code.

## Quick start

Ask Codex to follow this sequence:

1. Define success, boundaries, and non-goals.
2. Choose the current harness level.
3. Identify missing loop pieces before large edits.
4. Set an autonomy budget and escalation thresholds.
5. Iterate with evidence only.
6. Escalate with one decision and A/B/C options when blocked.
7. Finish with traceable delivery and risks.

## Harness levels

- `L1` Read-only inspection and documentation.
- `L2` Run tests, checks, and repro commands.
- `L3` Edit code and validate locally.
- `L4` Perform high-risk or external actions only with explicit approval or policy support.

## Operating rules

- Fix the harness before optimizing prompts or rewriting large areas.
- Require concrete evidence for every claimed result: command output, test result, log, CI signal, or artifact.
- Do not repeat the same failed tactic without a new hypothesis.
- If blocked, ask one decision only and provide a recommended option.
- Keep the final handoff traceable: changed files, validation, risks, and known gaps.

## Escalation template

```text
当前阻塞: <一句话>
已验证事实:
1) <证据1>
2) <证据2>

根因假设:
- H1: <假设 + 置信度>
- H2: <假设 + 置信度>

可选决策:
- A(推荐): <方案> | 成本 <x> | 风险 <y> | 预计耗时 <z>
- B: <方案> | 成本 <x> | 风险 <y> | 预计耗时 <z>
- C: <方案> | 成本 <x> | 风险 <y> | 预计耗时 <z>
```

## Load on demand

- Read `references/harness-engineering-digest.md` for thresholds, anti-patterns, and checklist details.
