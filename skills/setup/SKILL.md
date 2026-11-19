---
name: setup
description: Prepare an app repo to use anu, once per app. Fills the `## anu` section of CLAUDE.md, creates the docs folders, todo.md and LESSONS.md, turns anu on in .claude/settings.json, offers to remove the repo's own copies of what anu replaces, and opens a PR. Use for /anu:setup, or when another anu command says "Run /anu:setup first".
---

# /anu:setup — prepare an app repo

anu holds the process; each app keeps its own facts in the `## anu` section of its CLAUDE.md.
This writes that section and the files the other commands use.

## 1. Work in a worktree

Run inside the app repo. `git fetch origin`. `<base>` is the repo's default branch:
`git symbolic-ref --short refs/remotes/origin/HEAD` without the `origin/` (if that fails, run
`git remote set-head origin --auto` and try again). Reuse this session's worktree only if it is a linked worktree — `.git` at its root is a file, not a
folder (`test -f "$(git rev-parse --show-toplevel)/.git"`) — with no commits
beyond `origin/<base>` and nothing uncommitted; then rename its branch: `git branch -m anu/setup`.
Otherwise `git worktree add -b anu/setup .claude/worktrees/anu-setup origin/<base>` and work there.
Never rename or switch the main checkout's branch; never commit to `<base>`.

If CLAUDE.md on `origin/<base>` already has `## anu`, show it and ask what to change instead of
starting over; add any key below that it lacks.

## 2. Read the repo, then ask only what is missing

Find each fact yourself first:

| Fact | Where to look |
|---|---|
| Stack | package.json, pyproject.toml, go.mod, Cargo.toml, Dockerfile, README |
| Checks | package.json scripts, Makefile, `.github/workflows/`: type check, lint, tests |
| Local stack | dev scripts, docker-compose, emulator config, `.env.example`: start command, app URL, every port |
| Dev sign-in | grep the routes for `dev/login`, `dev-login`, `devLogin`, `?as=` |
| Screen sizes | Playwright config, breakpoints in the styles (default `390x844, 1280x800`) |
| Themes | `.dark`, `data-theme`, `prefers-color-scheme` in the styles |
| Styles | the file that defines the tokens (`:root { --…`), the component folder, the icon package |
| Other repos | README, CLAUDE.md, workspace files: repos a task here may also change |

Then ask, in one message, only what you could not find. The task prefix (suggest one from the
repo name, e.g. `CS` for a repo named `customer-site`) and the design references (apps, screens or files sketches
should match) usually need asking.

No dev sign-in route? An app with no sign-in at all gets `none (no sign-in)`. Otherwise QA
cannot reach the screens, so ask: build the route now (recommended), or leave it. On yes, write
it on this branch in the app's own style: a GET route that signs in a seeded test user and
redirects to `next`. The handler itself refuses in production, no env flag or setting can open
it on a deployed host, and `next` accepts a local path only. Add a test that production
refuses it. On no, write `none yet`: /anu:build and /anu:make stop on it.

## 3. Write the `## anu` section

Add it to CLAUDE.md (create the file if missing; replace an old `## anu` section). Keep the keys
and their order — every anu skill reads them by name:

```markdown
## anu

- Stack: <languages, frameworks, database, hosting>
- Checks: `<command>`, `<command>`
- Local stack: `<start command>`; app http://localhost:<port>; <service> :<port>
- Dev sign-in: http://localhost:<port>/<route>?as=<user>&next=<path> (users: <seeded users>)
- Screen sizes: 390x844, 1280x800
- Themes: light, dark (switch: <class or attribute on html>)
- Styles: `<tokens file>`; components: `<folder>`; icons: <package> (`<path to its SVG data>`)
- Task prefix: CS
- Base branch: <base>
- Design references: <apps, screens or files>
- Other repos: <name (path from this repo's main checkout, e.g. `../api`)> | none
```

## 4. Folders and files

Create what is missing:
- `docs/briefs/`, `docs/sketches/`, `docs/tasks/`, `docs/work-notes/`, each with an empty `.gitkeep`.
- `docs/todo.md`:
  ```markdown
  # To do

  Next: CS-1

  ## Coming

  ## Follow-ups
  ```
- `LESSONS.md` at the repo root: a `# Lessons` heading and the line "What broke before and must
  not break again. Add with /anu:lessons."
- `.gitignore`: add `.claude/worktrees/`.

## 5. Turn anu on for everyone who opens the repo

Merge into `.claude/settings.json`, keeping every existing key:

```json
{
  "extraKnownMarketplaces": { "anu": { "source": { "source": "github", "repo": "Tulifo/anu" } } },
  "enabledPlugins": { "anu@anu": true }
}
```

## 6. Offer to remove what anu replaces

List the repo's own `.claude/agents/` and `.claude/skills/` that do anu's job (a tech lead,
senior dev, QA or security agent; a build, brief, sketch, task, plan or submit skill). Show the
list and ask before deleting anything. Before a file goes, move any app fact it holds that
`## anu` lacks (ports, roles, test users, what is out of scope) into CLAUDE.md. Delete with
`git rm` on this branch only.

## 7. Commit and open the PR

`git add` only the files you created or changed. Commit under the user's own git identity (if
`git config user.name` is empty, ask for the name once and pass `-c user.name=… -c user.email=…`);
no AI co-author trailer or footer. `git push -u origin anu/setup`. Write the PR body to a temp
file and run `gh pr create --title "Set up anu" --body-file <file>` — never `--body` with
backticks. Never merge.

Report the PR link and the two daily commands: `/anu:idea "<idea>"` and `/anu:build <PREFIX>-1`.
