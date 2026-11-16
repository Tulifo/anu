# anu

A Claude Code plugin that takes an idea to merged code in any Tulifo app.

anu holds the process only. Each app keeps its own facts — stack, check commands, local stack and
ports, dev sign-in URL, screen sizes, styles, task prefix, design references — in a `## anu`
section of its CLAUDE.md. Every anu command reads that section first.

## Install

```bash
claude plugin marketplace add Tulifo/anu
```

```bash
claude plugin install anu@anu
```

The build team needs agent teams turned on. In `~/.claude/settings.json`:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

## Set up an app (once per app)

In the app repo, run `/anu:setup`. It reads the repo, asks only what it cannot find, writes the
`## anu` section, creates `docs/` and `LESSONS.md`, turns anu on in `.claude/settings.json` for
everyone who opens the repo, and opens a PR.

## Every day

```
/anu:idea "members can invite others by email"
```

Idea → brief → sketches → tasks. It stops for your OK on the approach, the brief, each sketch
and the task list, then opens one PR.

```bash
claude --agent anu:tech-lead
```

```
/anu:build CS-14
```

One task → finished code, ready for your review, with no stop until the PR. The tech lead plans
it; two senior devs build it; QA checks it in the running app; security reviews the diff; the
lead opens the PR. You merge.

## Commands

| Command | What it does |
|---|---|
| `/anu:idea "<idea>"` | idea → brief → sketches → tasks, stopping for your OK at each step |
| `/anu:build CS-14` | one task → finished code, ready for your review (the agent team) |
| `/anu:brief` | write the feature description |
| `/anu:sketch` | draw the screens as HTML and open them in your browser |
| `/anu:screen-check` | check a screen is easy and safe to use |
| `/anu:tasks` | split a feature into numbered tasks |
| `/anu:study CS-14` | read the task and the code before changing anything |
| `/anu:plan CS-14` | list the changes and who builds which part |
| `/anu:make CS-14` | write the code |
| `/anu:submit CS-14` | run checks, push, open the PR |
| `/anu:resume CS-14` | continue a task where the last session stopped |
| `/anu:lessons` | record "this broke before, don't repeat it" with file:line |
| `/anu:setup` | prepare an app repo to use anu (once per app) |

To build a task alone instead of with the team: `/anu:study` → `/anu:plan` → `/anu:make` →
`/anu:submit`. Alone, `/anu:submit` still has the read-only QA and security agents check the
work before it opens the PR.

## What anu writes in an app repo

```
docs/todo.md                              Next: CS-1 line, what's coming, follow-ups
docs/briefs/YYYY-MM-DD-<feature>.md
docs/sketches/YYYY-MM-DD-<feature>/       screens.md, screen-NN-<name>.html, narrow versions
docs/tasks/CS-14-<slug>.md                the ID always in the name, no date
docs/work-notes/CS-14/                    state.json, study.md, plan.md, shots/
LESSONS.md
```

`state.json` records the last finished stage — `studied`, `planned`, `made`, `submitted`,
`merged` — plus the branch, the worktree and the PRs.

All work happens in a git worktree on a branch off `origin/main`. anu never commits to main and
never merges.

## The team

| Agent | Model | Does |
|---|---|---|
| `anu:tech-lead` | fable | studies, plans, splits the work, gates it, opens the PR |
| `anu:senior-dev` | opus | builds one slice (two per task) |
| `anu:qa-engineer` | sonnet | checks it in the running app; read-only |
| `anu:security-engineer` | opus | reviews the diff; read-only |

## Changing anu

Branch off `main`, edit, then check:

```bash
claude plugin validate .
```

```bash
claude --plugin-dir . plugin list
```

Open a PR. The version lives only in `.claude-plugin/plugin.json`; bump it when you release, and
installs pick it up with `claude plugin update anu@anu`.
