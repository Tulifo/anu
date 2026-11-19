---
name: resume
description: Continue a task, or a feature's design, where the last session stopped — find the worktree by its branch, check the branch matches state.json, show uncommitted files and the PR, then run the next stage. Use for /anu:resume CS-14 or /anu:resume <feature>, or when the user says continue, pick up or carry on.
argument-hint: "<task ID or feature name>"
---

# /anu:resume — continue a task or a design

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." `<base>` below is
its `Base branch` (`main` if the key is absent). Do not pull `<base>` or switch branches in the
main checkout: the work lives on its own branch.

## 1. Find the work notes — by ID folder

`git worktree list --porcelain`: the worktree whose branch starts with `task/<ID>-` (exact ID:
`task/CS-4-` never matches `task/CS-41-`). Read `docs/work-notes/<ID>/state.json` there.
- No worktree, but `origin/task/<ID>-*` exists → `git worktree add .claude/worktrees/<ID> <branch>`
  and read it there.
- Not a task ID, or a `design/<name>` branch matches it → go to "A design branch" below.
- Nothing at all → no work yet: run /anu:study <ID>.
- Nothing given → list every worktree on a `task/` or `design/` branch with its ID or feature,
  stage, branch and updated date, and ask which.

## 2. Check it is the right place

- `git -C <worktree> branch --show-current` equals `branch` in state.json. If it differs, stop
  and say what differs; correct state.json only after the user agrees. state.json stores no
  path: ignore a `worktree` key written by an older anu.
- If `plan.md` changes one of `Other repos`, find that repo's worktree on the same branch name
  and show the same two lists for it.
- Show `git status --short` (uncommitted files) and `git log --oneline origin/<base>..HEAD`
  (commits not yet on `<base>`), so the user sees where the last session stopped.
- If `pr` has entries: `gh pr view <url> --json state,reviewDecision` for each. All `MERGED` →
  set `stage: "merged"`.

## 3. Report

```
CS-14 — Invite a member by email
Last finished: planned · Branch: task/CS-14-invite-member
Worktree: <path>
Uncommitted: 6 files · Commits not on <base>: 2
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

## A design branch

Work in the worktree on `design/<feature>`; if only the remote branch exists,
`git worktree add .claude/worktrees/design-<feature> design/<feature>`. Show `git status --short`
and the PR: `gh pr view --json state,mergeable,url`.
- No PR yet → run /anu:idea "<feature>": it carries on from the first missing step.
- PR open, `mergeable` is `CONFLICTING` → another design landed first, often on the same task
  IDs: run /anu:tasks step 5 (rebase, renumber, push).
- PR open with review comments → change the brief, sketch or task they name (a changed sketch
  passes /anu:screen-check again), commit, push, and reply on the PR.
- PR merged → done; offer to remove the worktree, only on the user's yes.
