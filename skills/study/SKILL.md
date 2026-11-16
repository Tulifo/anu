---
name: study
description: Read a task and the code it touches before changing anything — find the task by exact ID, check its blockers are merged, make its worktree and branch off origin/main, and write docs/work-notes/<ID>/study.md and state.json. Use for /anu:study CS-14, or as the first step of /anu:build.
argument-hint: "<task ID, e.g. CS-14>"
---

# /anu:study — read the task and the code first

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first."

## 1. Find the task — by exact ID

`git fetch origin`. The task file is `docs/tasks/<ID>-*.md` on `origin/main`
(`git ls-tree --name-only origin/main docs/tasks/`). Match the ID exactly: `CS-4` matches
`CS-4-…`, never `CS-41-…`. No ID given → list `## Coming` from `docs/todo.md` and ask which.
Not on `origin/main` → look on open `origin/design/*` branches; if it is there, say its design PR
is not merged yet and go on only if the user says so.

## 2. Already started?

Find the task's notes by its ID folder, never by date: a worktree on a branch starting
`task/<ID>-`, or a remote branch `origin/task/<ID>-*`, holding `docs/work-notes/<ID>/state.json`.
Found with a stage set → hand over to /anu:resume.

## 3. Blockers must be merged

For each ID in `Blocked by`, in this repo and in each of `Other repos` from `## anu`:
`gh pr list --state all --search "<ID> in:title" --json number,title,state,url`. Keep the PRs
whose title starts with `<ID>:` exactly, and confirm each with `gh pr view <n> --json state`.
The blocker is clear only when every one is `MERGED`. Anything else — open, closed, no PR —
stop, name the blocker and its PR state, and go on only if the user says so.

## 4. Make the worktree

Branch `task/<ID>-<slug>` (the slug from the task file name). If this session already runs in a
worktree whose branch has no commits beyond `origin/main`, rename it: `git branch -m task/<ID>-<slug>`.
Otherwise `git worktree add -b task/<ID>-<slug> .claude/worktrees/<ID> origin/main` and work
there. Never switch branches in the main checkout; never commit to main.

Write `docs/work-notes/<ID>/state.json`:

```json
{
  "task": "CS-14",
  "file": "docs/tasks/CS-14-invite-member.md",
  "stage": null,
  "branch": "task/CS-14-invite-member",
  "worktree": "<absolute path>",
  "pr": [],
  "updated": "YYYY-MM-DD"
}
```

`stage` is the last finished stage: `null` → `studied` → `planned` → `made` → `submitted` →
`merged`. Each step starts normally from the one before it.

## 5. Read

- CLAUDE.md, and AGENTS.md or CONTRIBUTING.md if present.
- `LESSONS.md`: every entry for a file the task may touch.
- The task, its brief, `screens.md` and its sketch files. Open each sketch at every screen size in
  `## anu` and save screenshots as `docs/work-notes/<ID>/shots/sketch-<screen>-<size>.png`; the
  build is compared against them.
- Every file the task will touch, and one existing example of each pattern it needs (an endpoint,
  a screen, a test).
- If the task says a layer needs no change, check that against the sketch: does the server
  already return everything the screen shows?

Ask the user only what changes the approach. Decide the rest and note it.

## 6. Write study.md

```markdown
# CS-14 study

## What this task builds
<2–3 sentences>

## Files to touch
| File | Does now | Changes |
|---|---|---|

## Patterns to follow
- <pattern>: `<path:line>` — <what to copy>

## Lessons that apply
- <LESSONS.md title> — `<file:line>`

## Risks
- <specific: a shared endpoint, a migration on a big table, a role check>

## Decisions taken
- <decision> — <why>
```

## 7. Finish

Set `stage: "studied"` and `updated` in state.json. `git add docs/work-notes/<ID>/` and commit
"<ID>: study" on the task branch. Next: /anu:plan <ID> (inside /anu:build it runs on its own).
