---
name: idea
description: Take an idea all the way to tasks a developer can build — a brief, then sketches of the screens, then numbered tasks — stopping for the user's OK at each step, all on one branch and one PR. Use for /anu:idea "<idea>", or when the user says "I have an idea" or "design this feature".
argument-hint: "<idea>"
---

# /anu:idea — idea to tasks

The idea: $ARGUMENTS

## Before you start

Read the `## anu` section of the repo's CLAUDE.md. If it is missing, stop and say: "This repo has
no `## anu` section. Run /anu:setup first." `<base>` below is its `Base branch` (`main` if the key is absent).

No idea given? Show the `## Coming` list from `docs/todo.md` on `origin/<base>` and ask what to design.

## 1. One branch for the whole feature

Pick a short kebab-case feature name (e.g. `member-invites`). `git fetch origin`, then look for
work already started: a worktree or branch `design/<feature>`, or a brief
`docs/briefs/*-<feature>.md` on `origin/<base>`. If found, say what exists and carry on from the
first missing step.

Otherwise, reuse this session's worktree only if it is a linked worktree — `.git` at its root is a file, not a
folder (`test -f "$(git rev-parse --show-toplevel)/.git"`) — with no commits
beyond `origin/<base>` and nothing uncommitted; then rename its branch: `git branch -m design/<feature>`. If it does
not pass, make one: `git worktree add -b design/<feature> .claude/worktrees/design-<feature> origin/<base>`.
Never rename or switch the main checkout's branch; never commit to `<base>`.

Everything this command writes is committed on `design/<feature>` and goes up as one PR.

## 2. Brief

Run /anu:brief. It stops twice: to choose the approach, and to OK the brief.

## 3. Sketches

Run /anu:sketch for every screen the brief lists. Each sketch passes /anu:screen-check, opens in
the user's browser, and stops for an OK. Skip only if the brief says the feature has no screen.

## 4. Tasks

Run /anu:tasks. It stops once to OK the task list, then numbers the tasks, writes the files and
opens the PR with the brief, the sketches and the tasks.

## Rules

- The stops are exactly: the approach, the brief, each sketch, the task list. Between stops,
  decide, and note each call in the brief under `## Decisions taken`.
- Vague feedback twice in a row on the same thing ("not right", "make it better"): ask what is
  wrong — broken, looks off (which part), or the wrong direction — before a third try.
- Never merge.

## Finish

Report the PR link, each task ID with one line, and what comes next: once the PR is merged,
start `claude --agent anu:tech-lead` and run `/anu:build <first task ID>`.
