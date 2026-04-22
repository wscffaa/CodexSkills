# Plan to Issues Guide

## Goal

Convert a structured plan into an executable ledger with atomic tasks, objective acceptance criteria, and review checkpoints.

## Output stages

- injected draft ledger path from `Artifacts:`: preferred output when routed through `unified-workflow`.
- `docs/workflow/ledgers/issues.draft.csv`: fallback output for review and correction.
- injected final ledger path from `Artifacts:` or `docs/workflow/ledgers/issues.csv`: only after the user explicitly wants an execution-ready ledger.

## What to extract from the plan

Before writing rows, identify:

- primary goal and non-goals
- user-visible deliverables
- technical constraints
- dependencies and required order
- validation strategy
- regression risk areas

## Decomposition algorithm

1. Break the plan into deliverables or milestones.
2. Split each deliverable into the smallest independently verifiable task.
3. Keep setup, implementation, migration, cleanup, and regression tasks separate when they do not complete in one pass.
4. Preserve dependency order with `ID` values.

## Atomic row checklist

A good row:

- changes one narrow behavior or artifact
- has a clear impact boundary
- can be validated without relying on future rows
- can name an observable success condition
- has obvious review points

A bad row usually:

- bundles multiple deliverables
- says "implement feature X" with no boundary
- lacks testable acceptance criteria
- hides cleanup or migration work inside a generic title

## Acceptance Criteria writing rules

Prefer criteria that reference:

- a command and expected output
- a test and expected pass condition
- a file and expected content or behavior
- a visible API, UI, or CLI effect

Avoid:

- works correctly
- code is clean
- logic implemented
- anything that cannot be verified by a reviewer

## Review Requirements writing rules

Each row should mention the most likely review failure points, such as:

- regression risk in adjacent modules
- boundary conditions and error cases
- leftover partial edits
- naming, contract, or schema consistency
- missing tests or unverified branches

## Required finishing rows

Always add at least one row near the end for:

- regression or end-to-end validation

Add a second finishing row when useful for:

- documentation, cleanup, or follow-up verification

## Draft-to-final gate

Before promoting the draft ledger to the final ledger, verify:

1. every row is atomic
2. every acceptance criterion is observable
3. every review requirement is meaningful
4. dependency order is safe
5. finishing rows exist

If any check fails, keep the file as draft and call out the uncertain rows.

## Example transformation

Plan fragment:

- Add authentication middleware
- Protect admin routes
- Add tests

Good rows:

1. Create middleware skeleton and config plumbing.
2. Apply middleware to admin route group.
3. Add auth failure tests for protected routes.
4. Run regression for unprotected routes and login flow.

Bad rows:

1. Implement authentication system.

## Gap handling

If the plan is missing key information, call it out explicitly, for example:

- validation path unknown
- dependency order ambiguous
- public contract not stated
- migration boundary unclear

In that case, produce the safest draft you can and clearly mark the uncertain rows for user review.
