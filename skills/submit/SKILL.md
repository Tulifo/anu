---
name: submit
description: Finish a made task — run the checks, have the read-only QA and security agents check it independently, commit, rebase onto the base branch, push and open the PR (one per repo, linked to each other), then ask one question about friction with anu and put the answer in the PR. Never merges. Use for /anu:submit CS-14, or as the last step of /anu:build.
argument-hint: "<task ID>"
---

# /anu:submit — check, push, open the PR

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." `<base>` below is its `Base branch` (`main` if the key is absent). Find the task's
worktree and state.json by exact ID and work there.

The normal start is `stage: "made"`. Stage `planned` → run /anu:make first, then carry on. Stage
`submitted` → show the PR and ask what to change.

## 1. Checks

Run every command in `## anu` `Checks:`. All must pass. If one fails, show the command and its
output, fix it, run it again.

## 2. Independent check — QA and security

Whoever wrote the code does not sign it off. Inside /anu:build the team's `qa` and `security`
have done this already: use their reports, and send only what changed after them back for a
re-check.

Otherwise start the local stack from `## anu` (reuse a running one) and run two read-only
subagents at the same time:
- `anu:qa-engineer`: walk every acceptance line in the running app — dev sign-in, every screen
  size, light and dark — compare with the sketch screenshots in `docs/work-notes/<ID>/shots/`,
  and report pass or fail per line.
- `anu:security-engineer`: review the task's diff in the worktree.

Each prompt carries the task ID, the worktree path, the paths of the task file, `study.md` and
`plan.md`, and the `## anu` facts it needs: local stack URL, dev sign-in URL and users, screen
sizes, themes, checks.

Fix every QA fail and every security blocker, run the checks again, and send the same agent back
to re-check what you fixed. A "should fix" finding may land; list it under `## Follow-ups` in the
PR. A line that cannot be checked locally (a real mail provider, real payments) is "not checked
locally — <why>", never a pass.

## 3. Commit

`git status --short`, then `git add` the task's files by name — code, tests,
`docs/work-notes/<ID>/` — never `git add -A`, never a path that does not exist. Messages:
`<ID>: <what changed>`. Commits carry the developer's own git identity only (if
`git config user.name` is empty, ask once and pass `-c user.name=… -c user.email=…`): no AI
co-author trailer, no "generated with" line.

## 4. Rebase and push

`git fetch origin` and `git rebase origin/<base>`. Resolve conflicts keeping both sides' intent;
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

## Acceptance (checked by QA)
- [x] <line> — <what QA saw; size, theme>
- [ ] <line> — not checked locally: <why>

## Security
<findings and their status, or "No findings" and what was checked>

## Checks
- `<command>` — passed

## Decisions taken
- <decision> — <why>

## Follow-ups
- <should-fix finding or known gap> | none

## Related PRs
- <owner/repo#n> | none

## anu feedback
<filled in at step 6>
```

If the task changed more than one repo (`Other repos` in `## anu`), do steps 1–5 in each — in
that repo's `task/<ID>-<slug>` worktree, with its own checks and base branch — then update
every body's `Related PRs` so each links the others (`gh pr edit <n> --body-file <file>`).

Never merge, and never turn on auto-merge.

## 6. Ask about anu

Ask one question: "Was anything about anu in this task friction, confusing, or worth changing?"
Put the answer, close to the user's words (or "none"), under `## anu feedback` in each PR body
with `gh pr edit --body-file`. Never write into the plugin's own folder.

If the answer asks for a change to anu, say where to send it: an issue on anu's repository
(`repository` in `${CLAUDE_SKILL_DIR}/../../.claude-plugin/plugin.json`). Never file it
yourself: the words may carry details of this app.

## 7. Finish

Set `stage: "submitted"`, `pr: [<urls>]` and `updated` in state.json; commit "<ID>: work notes"
and push. Report the PR links and anything not checked. The user reviews and merges;
/anu:resume <ID> afterwards records `merged`.
