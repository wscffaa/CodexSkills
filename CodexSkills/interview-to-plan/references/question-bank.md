# Question Bank

Use only the section that matches the current mode.
Ask 1-3 questions per round and stop once the next question no longer changes the plan materially.

## Common First Pass

Use these first when the request is still fuzzy:

- What exact outcome do you want at the end?
- What is explicitly out of scope?
- What artifact must exist when this is done?
- What deadline, budget, or compute ceiling exists?
- What files, repos, papers, or links are the source of truth?
- How will we know the result is correct or complete?

## `new-project`

Prioritize these questions:

1. Who is the user and what problem is being solved?
2. What is the smallest useful version?
3. What stack, runtime, or deployment constraints already exist?
4. What data, integrations, auth, or external services are required?
5. What must be correct in v1, and what can wait?
6. What evidence would prove the project is usable?

## `project-recreation`

Prioritize these questions:

1. What is the source repo, product, paper, site, or version to recreate?
2. Do you need functional parity, UI parity, API parity, model parity, or research parity?
3. What deviations are allowed, and what must remain identical?
4. What is the validation oracle: tests, screenshots, metrics, docs, or paper claims?
5. Are there license, private-data, or closed-source blockers?
6. What deadline or quality bar makes the recreation "good enough"?

## `basicofr-paper`

Prioritize these questions:

1. What venue and deadline are you targeting?
2. What exact problem or task inside BasicOFR are you addressing?
3. What branch, baseline, or prior result is the source of truth?
4. What is the novelty claim in one sentence?
5. What code-change boundary is allowed?
6. Which datasets, splits, metrics, and minimum improvements matter?
7. Which ablations or visualizations are mandatory?
8. What compute budget and GPU constraints exist?
9. What paper artifacts are required: plan, experiments, figures, tables, draft sections?
10. What is the kill criterion if the idea does not beat the baseline?

## `hybrid`

Use the common first pass, then mix only the relevant questions from the matching sections above.
Do not ask duplicate questions under different names.

## Stop Condition

Stop interviewing and write the PRD only when all mandatory fields are in one of these states:

- answered with concrete facts
- labeled as one explicit assumption
- labeled as an unresolved risk or open question

If a missing answer would still change scope, architecture, validation, schedule, or resource cost, keep interviewing.
