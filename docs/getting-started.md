# Getting started

This page takes you from nothing to a first merged task. Each step says what you run, what anu
does, and what you get back.

## What you need

- **Claude Code**, signed in.
- **git** and the **GitHub CLI** (`gh`), signed in to an account that can push to the app repo
  and open pull requests.
- **python3**, for the sketch preview server (standard library only).
- **A browser tool** in Claude Code — the Playwright MCP, or a built-in browser — so sketches and
  built screens can be checked at every screen size. QA needs it.
- **Agent teams** turned on, for `/anu:build` (see below). The solo path works without it.

## 1. Install anu

```bash
claude plugin marketplace add Tulifo/anu
```

```bash
claude plugin install anu@anu
```

Turn on agent teams in `~/.claude/settings.json`, keeping any keys already there:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

Restart Claude Code. Check that anu loaded:

```bash
claude plugin list
```

You should see `anu` with its version. In a session, typing `/anu:` lists the 13 commands.

## 2. Set up an app (once per app)

Open Claude Code in the app repo and run:

```
/anu:setup
```

What happens:

1. anu makes a worktree on branch `anu/setup` off `origin/main`. Your main checkout is not
   touched.
2. It reads the repo to find each fact itself: the stack from `package.json` and friends, the
   check commands from scripts and CI, the local stack from dev scripts and docker-compose, a dev
   sign-in route, breakpoints, themes, the styles file.
3. It asks you, in one message, only what it could not find. Usually that is the **task prefix**
   (for example `CS` for compass-saas) and the **design references** (apps or screens sketches
   should look like).
4. It writes the `## anu` section into CLAUDE.md, creates `docs/briefs/`, `docs/sketches/`,
   `docs/tasks/`, `docs/work-notes/`, `docs/todo.md` and `LESSONS.md`, adds `.claude/worktrees/`
   to `.gitignore`, and turns anu on in `.claude/settings.json` so everyone who opens the repo
   gets it.
5. If the repo has its own agents or skills that do anu's job, it lists them and asks before
   removing any. App facts they hold move into CLAUDE.md first.
6. It commits under your git identity and opens a PR titled "Set up anu".

Review and merge that PR. Every other command reads `## anu` from it.

> **No dev sign-in route?** Setup writes `Dev sign-in: none yet` and tells you. QA and the
> screen checks need one to reach screens behind a login. See
> [Configuration → Dev sign-in](configuration.md#dev-sign-in).

## 3. Design a feature

```
/anu:idea "members can invite others by email"
```

anu runs three steps on one branch, `design/<feature>`, and stops for your OK four kinds of
times:

| Step | Stops for |
|---|---|
| Brief | choosing an approach (2–3 options, its pick first), then the brief itself |
| Sketches | each screen, shown in your browser with live reload |
| Tasks | the task list (titles, sizes, blockers, acceptance lines) |

At the end it opens one PR holding the brief, the sketches and the task files, and tells you the
task IDs, for example `CS-14`, `CS-15`, `CS-16`.

Review and merge the design PR. Tasks are built from `origin/main`: anu stops and asks before
building a task whose design PR is not merged yet.

## 4. Build a task with the team

Start a session as the tech lead, in the app repo:

```bash
claude --agent anu:tech-lead
```

Then:

```
/anu:build CS-14
```

The tech lead:

1. finds the task by its exact ID and checks every task in `Blocked by` has a **merged** PR;
2. makes a worktree on `task/CS-14-<slug>` and reads the task, the brief, the sketches and the
   code it touches (`study.md`);
3. writes the plan: two slices with no file in common and the interfaces they share
   (`plan.md`). It does not wait for an OK;
4. starts the local stack and spawns the team: two senior devs (one slice each), QA and
   security;
5. gates each slice on green checks, QA in the running app and a clean security review;
6. commits, rebases onto `origin/main`, pushes and opens the PR.

You get one status line each time a part of the work changes state, and no questions in between.
Calls it had to make are listed under "Decisions taken" in the PR.

At the end it asks one question — was anything about anu friction or confusing — and adds your
answer to the PR.

Review and merge the PR. Then record it:

```
/anu:resume CS-14
```

It sees the PR is merged, sets the stage to `merged`, and offers to remove the worktree.

## 5. Or build it alone

Without the team, run the four steps yourself, in any session:

```
/anu:study CS-14
/anu:plan CS-14
/anu:make CS-14
/anu:submit CS-14
```

Each step carries on into the one before it if needed: `/anu:make` on a task that was only
studied runs the plan first. `/anu:submit` still runs the read-only QA and security agents before
it opens the PR, so the code is never signed off by whoever wrote it.

## 6. Every day after that

| You want to | Run |
|---|---|
| Design a feature | `/anu:idea "<idea>"` |
| Build the next task | `claude --agent anu:tech-lead`, then `/anu:build <ID>` |
| Pick up a task a session left | `/anu:resume <ID>` |
| Record a bug that must not come back | `/anu:lessons` |
| See what is next | open `docs/todo.md` |

## Keeping anu up to date

```bash
claude plugin update anu@anu
```

Installs pick up a new release when its version in `.claude-plugin/plugin.json` goes up.
