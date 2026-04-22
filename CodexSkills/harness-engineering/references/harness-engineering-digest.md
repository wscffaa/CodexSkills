# Harness Engineering Digest

## Core idea

Harness matters more than prompt polish when the task depends on real execution.
A good harness gives Codex access to the repo, tests, logs, CI signals, and failure feedback inside clear safety boundaries.

## Stable rules worth reusing

1. Solve execution and verification first.
2. Give Codex controlled autonomy, not blind freedom.
3. Start from low privilege and escalate by evidence.
4. Define when to ask a human; do not ask too early and do not retry forever.
5. Finish with traceable delivery, not vague success claims.

## Minimal checklist

- Success criteria and non-goals are explicit.
- Available commands, tests, logs, and CI signals are known.
- Missing loop pieces are listed before deep edits.
- Time and retry budgets are explicit.
- Escalation thresholds are explicit.
- Final report includes evidence and risks.

## Good escalation triggers

- The same failure mode repeats 2–3 times.
- A required secret, environment variable, or external permission is missing.
- The repo allows multiple meaningful solutions with different costs.
- A change would cross a safety boundary or impact unrelated systems.

## Anti-patterns

- Prompt thrashing without improving the validation loop.
- Claiming success from reasoning alone.
- Repeating the same command without a new hypothesis.
- Asking the user to choose before evidence exists.
- Hiding a failure behind a fallback path.
