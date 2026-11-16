---
name: plan
description: List the changes a task needs, file by file and in order, split them into two slices with separate files and the interfaces they share, and say how each acceptance line will be checked; stops for the user's OK. Writes docs/work-notes/<ID>/plan.md. Use for /anu:plan CS-14, or inside /anu:build.
argument-hint: "<task ID>"
---

# /anu:plan — list the changes and who builds which part

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Find the task's
worktree and `docs/work-notes/<ID>/state.json` by exact ID (as in /anu:study steps 1–2) and work
there.

The normal start is `stage: "studied"`. Stage `null` → run /anu:study first, then carry on here;
never send the user back a step. Stage `planned` or later → show the plan and ask: redo it, or go
on to the next step.

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

## Shared interfaces
Copied verbatim to both builders:
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

A small task may have one slice; say why. A screen with no sketch file under `docs/sketches/` is
not designed: stop and say so; never plan its look from prose alone.

## 2. OK the plan — stop

Show the plan and apply changes until the user says OK. After this, the work runs to the PR
without stopping.

## 3. Finish

Set `stage: "planned"` and `updated`. `git add docs/work-notes/<ID>/` and commit "<ID>: plan".
Next: /anu:make <ID> to build alone, or /anu:build <ID> with the team.
