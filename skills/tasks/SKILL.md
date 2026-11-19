---
name: tasks
description: Split a feature into numbered tasks — vertical slices of data, server and screen that a user can test, 1–3 days each — reserve their IDs on the `Next:` line of docs/todo.md first, write one file per task, and open one PR. Use for /anu:tasks, or when /anu:idea reaches the tasks.
argument-hint: "<feature or brief path>"
---

# /anu:tasks — split a feature into tasks

Input: $ARGUMENTS (a feature name or brief path; default: the brief on the current design branch).

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." `<base>` below is its `Base branch` (`main` if the key is absent).
Work in the feature's `design/<feature>` worktree, never on `<base>`. Read the brief, `screens.md` and every
sketch file.

## 1. Draft the tasks

Each task is a vertical slice: the data, the server and the screen for one behaviour a user can
test in the running app, 1–3 days of work.
- Never a backend-only, frontend-only or data-only task. A change with no screen of its own goes
  in the first task whose screen uses it.
- Too big? Cut by behaviour ("invite by email", "resend an invite"), still top to bottom, never
  by layer.
- Order: a screen that sets something up comes before the screens that use it (settings before
  the list that reads them). Each task is still testable on its own.
- Check every task before showing it: does it cover data, server and screen for its behaviour,
  or say why a layer needs no change? A task that touches one layer only merges into the task
  that needs it.

## 2. OK the list — stop

Show the tasks as a numbered list: title, size, blocked by, acceptance lines. Ask whether to
split, merge or change any. Wait for an OK.

## 3. Reserve the IDs — the `Next:` line first

`git fetch origin`, then rebase the design branch onto `origin/<base>` so `docs/todo.md` is
current. Read `Next: <PREFIX>-<n>`. The new tasks take `<n>`, `<n+1>`, … in the agreed order;
never take an ID from file names. Edit the `Next:` line to the first unused ID, add each task to
`## Coming` (`- CS-14 Invite a member — docs/tasks/CS-14-invite-member.md`), drop `## Coming`
lines whose task PR is merged, and commit this on its own: "Reserve CS-14–CS-16".

## 4. Write one file per task

`docs/tasks/<ID>-<slug>.md`: the ID always in the name, no date, the slug names the behaviour
(never `-backend` or `-frontend`).

```markdown
# CS-14 Invite a member by email

ID: CS-14
Brief: docs/briefs/YYYY-MM-DD-<feature>.md
Sketches: docs/sketches/YYYY-MM-DD-<feature>/screen-02-invite.html
Size: S | M | L
Blocked by: CS-13 | none

## What and why
<2–4 sentences>

## Acceptance
Each line is checked in the running app: dev sign-in, every screen size, light and dark.
- [ ] <a specific behaviour a user can see>
- [ ] <its error, empty and permission cases>

## Slice
- Data: <tables or fields, migration> | none (<why>)
- Server: <endpoint or function, inputs, outputs, errors, who may call it>
- Screen: <route, components, which sketch>
- Files likely touched: `<path>`
- Pattern to follow: `<path>` — <what to copy>
- Lessons that apply: <LESSONS.md title>
```

`Blocked by` lists task IDs only. A task with a screen names its exact sketch file; a screen with
no sketch file under `docs/sketches/` is not ready — say so instead of writing the task.

## 5. Commit, check the numbers, open the PR

`git add` the task files and `docs/todo.md` by name; commit "Tasks: <feature> (CS-14–CS-16)".
`git fetch origin` and rebase onto `origin/<base>` again.

If the rebase conflicts on the `Next:` line, someone else took those IDs. Keep their line, then
renumber the new tasks from their `Next:` value: rename the files, fix the IDs inside them, every
`Blocked by`, the `## Coming` lines and the brief's links; set `Next:` past the last new ID;
continue the rebase.

PR already open (you came from /anu:resume)? `git push --force-with-lease`, skip
`gh pr create`, and correct the task IDs in the PR body with `gh pr edit --body-file`.

`git push -u origin design/<feature>`. Write the PR body to a temp file — the brief, the
sketches, the task list with IDs, the decisions taken — and run
`gh pr create --title "<Feature>: brief, sketches, tasks" --body-file <file>`. Never `--body` with
backticks. Commits carry the user's own git identity, with no AI trailer. Never merge.

Report the PR link and the task IDs. Next, once this PR is merged: `/anu:build <first ID>`.
