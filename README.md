<p align="center">
  <img src="assets/logo.svg" width="128" height="128" alt="anu logo">
</p>

<h1 align="center">anu</h1>

<p align="center">
  A Claude Code plugin that takes an idea to merged code in any app.
</p>

<p align="center">
  <a href="docs/getting-started.md">Getting started</a> ·
  <a href="docs/how-it-works.md">How it works</a> ·
  <a href="docs/commands.md">Commands</a> ·
  <a href="docs/team.md">The build team</a> ·
  <a href="docs/configuration.md">Configuration</a> ·
  <a href="docs/troubleshooting.md">Troubleshooting</a>
</p>

---

anu holds the process only. Each app keeps its own facts — stack, check commands, local stack and
ports, dev sign-in URL, screen sizes, styles, task prefix, design references — in a `## anu`
section of its CLAUDE.md. Every anu command reads that section first.

You approve the design and you merge the PRs. In between, anu writes the brief, draws the
screens, splits the work into tasks, and an agent team builds, checks and submits each task.

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

## Use it

**Once per app** — in the app repo:

```
/anu:setup
```

It reads the repo, asks only what it cannot find, writes the `## anu` section, and opens a PR.

**Design a feature** — idea → brief → sketches → tasks, stopping for your OK on the approach, the
brief, each sketch and the task list, then one PR:

```
/anu:idea "members can invite others by email"
```

**Build a task** — no stop until the PR. The tech lead plans it, senior devs build it (two, or one for a small task), QA
checks it in the running app, security reviews the diff, and the lead opens the PR. You merge.

```bash
claude --agent anu:tech-lead
```

```
/anu:build CS-14
```

To build alone instead: `/anu:study` → `/anu:plan` → `/anu:make` → `/anu:submit`. The read-only
QA and security agents still check the work before the PR opens.

The full walk-through is in [Getting started](docs/getting-started.md).

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
| `/anu:submit CS-14` | independent QA and security check, push, open the PR |
| `/anu:resume CS-14` | continue a task, or a feature's design, where the last session stopped |
| `/anu:lessons` | record "this broke before, don't repeat it" with file:line |
| `/anu:setup` | prepare an app repo to use anu (once per app) |

Each one in detail: [Commands](docs/commands.md).

## The team

| Agent | Model | Does |
|---|---|---|
| `anu:tech-lead` | fable | studies, plans, splits the work, gates it, opens the PR |
| `anu:senior-dev` | opus | builds one slice (one dev per slice) |
| `anu:qa-engineer` | sonnet | checks it in the running app; read-only |
| `anu:security-engineer` | opus | reviews the diff; read-only |

How they work together: [The build team](docs/team.md).

## Ground rules

- All work happens in a git worktree on a branch off the app's base branch (`main` unless
  `## anu` says otherwise). anu never commits to the base branch.
- anu never merges and never turns on auto-merge.
- Commits and PRs carry your git identity only.
- A task is not built until every task it is blocked by has a merged PR, unless you say so.

## Documentation

| Page | |
|---|---|
| [Getting started](docs/getting-started.md) | install, set up an app, first feature, first task |
| [How it works](docs/how-it-works.md) | the flow, stops, stages, worktrees, task IDs, files written |
| [Commands](docs/commands.md) | all 13 commands in detail |
| [The build team](docs/team.md) | the agents, how a build runs, what "verified" means |
| [Configuration](docs/configuration.md) | the `## anu` section, settings, dev sign-in |
| [Troubleshooting](docs/troubleshooting.md) | every stop message and what to do |
| [Changing anu](docs/contributing.md) | layout, rules, testing, releasing, the logo |

What changed in each version: [Changelog](CHANGELOG.md).

## Licence

[MIT](LICENSE).
