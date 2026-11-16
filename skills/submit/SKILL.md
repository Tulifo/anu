---
name: submit
description: Finish a made task — run the checks, walk every acceptance line in the running app, commit, rebase onto origin/main, push and open the PR (one per repo, linked to each other), then ask one question about friction with anu and put the answer in the PR. Never merges. Use for /anu:submit CS-14, or as the last step of /anu:build.
argument-hint: "<task ID>"
---

# /anu:submit — check, push, open the PR

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Find the task's
worktree and state.json by exact ID and work there.

The normal start is `stage: "made"`. Stage `planned` → run /anu:make first, then carry on. Stage
`submitted` → show the PR and ask what to change.

## 1. Checks

Run every command in `## anu` `Checks:`. All must pass. If one fails, show the command and its
output, fix it, run it again.

## 2. Walk every acceptance line in the running app

Use the local stack from `## anu` (reuse a running one), the dev sign-in URL, every screen size,
light and dark. Mark each acceptance line pass or fail with what you saw, and save screenshots in
`docs/work-notes/<ID>/shots/`. Fix failures and walk again. A line that cannot be checked locally
(a real mail provider, real payments) is "not checked locally — <why>", never a pass. Inside
/anu:build, use QA's results and walk again only the lines touched after QA.

## 3. Commit

`git status --short`, then `git add` the task's files by name — code, tests,
`docs/work-notes/<ID>/` — never `git add -A`, never a path that does not exist. Messages:
`<ID>: <what changed>`. Commits carry the developer's own git identity only (if
`git config user.name` is empty, ask once and pass `-c user.name=… -c user.email=…`): no AI
co-author trailer, no "generated with" line.

## 4. Rebase and push

`git fetch origin` and `git rebase origin/main`. Resolve conflicts keeping both sides' intent;
ask the user when the intent is unclear. If the rebase brought new commits, run the checks again.
Then `git push -u origin <branch>`.

## 5. Open the PR — one per repo

Title `<ID>: <task title>`. Write the body to a temp file and run
`gh pr create --title "<title>" --body-file <file>`. Never `--body` with backticks.

```markdown
## What
<2–3 sentences>

## Task
docs/tasks/<ID>-<slug>.md

## Acceptance
- [x] <line> — <what was seen; size, theme>
- [ ] <line> — not checked locally: <why>

## Checks
- `<command>` — passed

## Decisions taken
- <decision> — <why>

## Related PRs
- <owner/repo#n> | none

## anu feedback
<filled in at step 6>
```

If the task changed more than one repo (`Other repos` in `## anu`), do steps 1–5 in each, then
update every body's `Related PRs` so each links the others (`gh pr edit <n> --body-file <file>`).

Never merge, and never turn on auto-merge.

## 6. Ask about anu

Ask one question: "Was anything about anu in this task friction, confusing, or worth changing?"
Put the answer, close to the user's words (or "none"), under `## anu feedback` in each PR body
with `gh pr edit --body-file`. Never write into the plugin's own folder.

## 7. Finish

Set `stage: "submitted"`, `pr: [<urls>]` and `updated` in state.json; commit "<ID>: work notes"
and push. Report the PR links and anything not checked. The user reviews and merges;
/anu:resume <ID> afterwards records `merged`.
