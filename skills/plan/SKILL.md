---
name: plan
description: List the changes a task needs, file by file and in order, split them into two slices (one for a small task) with separate files and the interfaces they share, and say how each acceptance line will be checked — then carry on without waiting for an OK. Writes docs/work-notes/<ID>/plan.md. Use for /anu:plan CS-14, or inside /anu:build.
argument-hint: "<task ID>"
---

# /anu:plan — list the changes and who builds which part

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Find the task's
worktree and `docs/work-notes/<ID>/state.json` by exact ID (as in /anu:study steps 1–2) and work
there.

The normal start is `stage: "studied"`. Stage `null` → run /anu:study first, then carry on here;
never send the user back a step. Stage `planned` or later → redo the plan only when the user ran
/anu:plan to redo it; inside /anu:build or /anu:resume, go on to the next step.

## 1. Write the plan

```markdown
# CS-14 plan

Task: docs/tasks/CS-14-<slug>.md
Branch: task/CS-14-<slug>

## Changes, in order
1. `<path>` — add or change <what>, because <why>

## Slices
Two slices with no file in common; usually the screen (A) and the server and data (B).
| Slice | Owner | Files |
|---|---|---|
| A — <screen> | dev-a | `<path>` |
| B — <server, data> | dev-b | `<path>` |
A shared file (a router, an index, package.json) belongs to one slice; the other asks its owner.
A task too small to split has one slice, owned by dev-a: say why in one line.

## Shared interfaces
Copied verbatim to every builder ("none" for a one-slice plan):
- `<METHOD /path or function>`: input <shape>, output <shape>, errors <codes>
- Data: `<table or collection>` fields <name: type>
- Routes and events: <names>

## Screens
For each: its sketch file, the components and tokens it uses, and where it differs from a
component's defaults (width, padding, size).

## Tests
- <logic> → `<test file>`

## How each acceptance line is checked
| Acceptance line | How (screen size, theme, user) |
|---|---|

## Out of this task
- <what the brief or a sketch shows that this task does not build>

## Decisions taken
- <decision> — <why>
```

A screen with no sketch file under `docs/sketches/` is not designed: stop and say so; never plan
its look from prose alone.

A change in one of `Other repos` from `## anu`: write its paths as `<repo>:<path>`, and make that
repo's worktree before you finish. From its local path: `git fetch origin`, then
`git worktree add -b task/<ID>-<slug> .claude/worktrees/<ID> origin/<its base>` — its base is its
own `Base branch`, else `git symbolic-ref --short refs/remotes/origin/HEAD`. The branch name is
the same in every repo. Never touch that repo's main checkout.

## 2. Show it and carry on

Show the plan in a few lines — the slices, the shared interfaces, what is out — and do not wait
for an OK. The design was agreed before the task was written; the user reviews the result in the
PR. Anything the plan had to decide goes under `## Decisions taken`, which the PR lists.

## 3. Finish

Set `stage: "planned"` and `updated`. `git add docs/work-notes/<ID>/` and commit "<ID>: plan".
Next: /anu:make <ID> to build alone, or /anu:build <ID> with the team (inside /anu:build it runs
on its own).
