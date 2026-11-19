---
name: lessons
description: Record "this broke before, don't repeat it" in LESSONS.md — each lesson tied to a file:line, with why the code is so and what breaks if it changes — keeping follow-ups apart in docs/todo.md. Commits on a branch and opens a PR. Use for /anu:lessons, after a painful bug, or when getting to know a repo.
argument-hint: "[a bug, file or area to start from]"
---

# /anu:lessons — record what broke before

Start from: $ARGUMENTS (a bug just fixed, a file, an area — or nothing, to find the risky files).

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." `<base>` below is its `Base branch` (`main` if the key is absent). Read `LESSONS.md`
so no lesson is recorded twice. `git fetch origin`, and pick a short kebab-case topic (the bug,
file or area). Reuse this session's worktree only if it is a linked worktree — `.git` at its root is a file, not a
folder (`test -f "$(git rev-parse --show-toplevel)/.git"`) — with no commits
beyond `origin/<base>` and nothing uncommitted; then rename
its branch: `git branch -m lessons/<topic>`. Otherwise
`git worktree add -b lessons/<topic> .claude/worktrees/lessons-<topic> origin/<base>`; if that
branch exists, add `-2`. Never rename or switch the main checkout's branch; never commit to `<base>`.

## 1. Find where the lessons are

With a starting point, use it. Otherwise rank up to 15 files by:
- churn: `git log --since="6 months ago" --format= --name-only | sort | uniq -c | sort -rn | head -30`
- fixes: `git log --since="6 months ago" --oneline -i --grep=fix --grep=bug --grep=revert`
- markers: `grep -rlE 'TODO|FIXME|HACK|XXX|WORKAROUND'` over the source folders

Show the list and ask what to add or drop.

## 2. Ask, one question at a time

Read each file. Look for workarounds, defensive code, odd ordering, magic numbers, and comments
that explain a "why". Ask about one specific line:
- good: "`src/billing/close.ts:88` locks the row before reading the total. What goes wrong
  without the lock?"
- bad: "What is fragile here?"

After each file: "Anything else in this file before we move on?"

## 3. Lesson or follow-up — keep them apart

- **Lesson:** why the code is the way it is, and what breaks if someone changes it. Goes in
  `LESSONS.md`.
- **Follow-up:** something that should be fixed or improved. Goes in `docs/todo.md` under
  `## Follow-ups`, one line with its file:line.

"It is fragile and we should fix it" gives one of each. Never one entry that is both.

Every lesson, no exceptions:

```markdown
## <short title: the rule>

File: `<path>:<line>` (<function>)
Why: <why the code is like this>
What breaks: <what goes wrong if someone changes it>
Added: YYYY-MM-DD
```

No lesson without a file:line. Anchor it to the line that holds the reason (the lock, the check)
and name the function, so it can be found after the lines move.

## 4. Save and submit

Show every lesson and follow-up and apply the user's edits. Append lessons to `LESSONS.md` — never
edit or delete an existing one without asking — and follow-ups to `docs/todo.md`.

`git status --short`, then `git add` only files that exist and changed. Commit "Lessons: <n>
added" under the user's own git identity, with no AI trailer. `git push -u origin lessons/<topic>`.
Write the PR body to a temp file and run `gh pr create --title "Lessons: <topic>" --body-file <file>`.
Never merge.

Report the PR link, the lessons added and the follow-ups recorded.
