---
name: resume
description: Continue a task where the last session stopped — find its work notes by ID folder, check the worktree and branch match state.json, show uncommitted files, then run the next stage. Use for /anu:resume CS-14, or when the user says continue, pick up or carry on with a task.
argument-hint: "<task ID>"
---

# /anu:resume — continue a task

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Do not pull main
or switch branches in the main checkout: the work lives on the task's branch.

## 1. Find the work notes — by ID folder

`git worktree list --porcelain`: the worktree whose branch starts with `task/<ID>-` (exact ID:
`task/CS-4-` never matches `task/CS-41-`). Read `docs/work-notes/<ID>/state.json` there.
- No worktree, but `origin/task/<ID>-*` exists → `git worktree add .claude/worktrees/<ID> <branch>`
  and read it there.
- Nothing at all → no work yet: run /anu:study <ID>.
- No ID given → list every worktree on a `task/` branch with its ID, stage, branch and updated
  date, and ask which.

## 2. Check it is the right place

- `git -C <worktree> branch --show-current` equals `branch` in state.json, and the worktree path
  equals `worktree`. If either differs, stop and say what differs; correct state.json only after
  the user agrees.
- Show `git status --short` (uncommitted files) and `git log --oneline origin/main..HEAD`
  (commits not yet on main), so the user sees where the last session stopped.
- If `pr` has entries: `gh pr view <url> --json state,reviewDecision` for each. All `MERGED` →
  set `stage: "merged"`.

## 3. Report

```
CS-14 — Invite a member by email
Last finished: planned · Branch: task/CS-14-invite-member
Worktree: <path>
Uncommitted: 6 files · Commits not on main: 2
Next: make
```

## 4. Continue from the next stage

| Last finished (`stage`) | Run next |
|---|---|
| `null` | /anu:study, then onward |
| `studied` | /anu:plan, then onward |
| `planned` | /anu:make — or /anu:build for the team, which needs `claude --agent anu:tech-lead` |
| `made` | /anu:submit |
| `submitted` | show each PR's state and review comments; fix what reviewers asked, run the checks, commit, push, and reply on the PR |
| `merged` | done; offer to remove the worktree (`git worktree remove <path>`), only on the user's yes |

Uncommitted files are the last session's work in progress: keep them, read them, and carry on
from them. Never stash, reset or discard them.

Read the task, `study.md` and `plan.md` before the code. Keep the stops of the stage's own skill.
