# Troubleshooting

When anu stops, it says why. This page lists each stop, what causes it, and what to do.

## anu stops with a message

### "Run /anu:setup first."

The repo's CLAUDE.md has no `## anu` section on the branch you are on. Run `/anu:setup` and merge
its PR. If setup's PR is open but not merged, work from a branch that has it, or merge it first.

### "Start with `claude --agent anu:tech-lead`, then run `/anu:build <ID>`."

`/anu:build` runs only in a session started as the tech lead. Quit, then:

```bash
claude --agent anu:tech-lead
```

To build in a normal session instead, use the solo path: `/anu:study`, `/anu:plan`,
`/anu:make`, `/anu:submit`.

### "Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to `1` …"

Agent teams are off. Add this to `~/.claude/settings.json`, keeping your other keys, and restart
Claude Code:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

### A blocker is not merged

`Blocked by` names a task whose PR is open, closed or missing. anu names the blocker and its
state. Merge the blocker's PR and run the command again, or tell anu to go on if you accept
building on unmerged work.

anu finds a blocker's PR by its title starting with `<ID>:`. If the blocker was merged under a
different title, tell anu, or rename the PR.

### The task's design PR is not merged

The task file exists only on a `design/<feature>` branch. Merge the design PR first, or tell anu
to go on.

### A screen has no sketch file

A task or plan names a screen with no HTML file under `docs/sketches/`. Run `/anu:sketch` for it
and merge that, or remove the screen from the task. A link to a design tool does not count.

### The worktree or branch differs from `state.json`

`/anu:resume` found the task's worktree on a different branch or path than its notes say —
usually because a worktree was moved, or a branch was renamed by hand. anu shows both values.
Say which is right; anu corrects `state.json` only after you agree.

### A rebase conflict anu cannot settle

Both sides changed the same lines and the intent is unclear. anu shows the conflict and asks
which way to go. A conflict on the `Next:` line in `docs/todo.md` is never asked about: anu
renumbers its own tasks and carries on.

### anu asks for your name

`git config user.name` is empty. anu asks once and commits with
`git -c user.name="…" -c user.email="…" commit`. To stop the question, set it:

```bash
git config --global user.name "Your Name"
```

## Something does not work

### `/anu:` commands do not show up

Check the plugin is installed and on:

```bash
claude plugin list
```

If it is missing, add the marketplace and install it again (see
[Getting started](getting-started.md#1-install-anu)). In an app repo set up with anu,
`.claude/settings.json` turns it on; accept the prompt to trust the marketplace when Claude Code
offers it.

### An update does not arrive

Installs move only when the version in `.claude-plugin/plugin.json` goes up. After a release:

```bash
claude plugin update anu@anu
```

Then restart Claude Code.

### The team spawns plain subagents

The lead should spawn teammates as an agent team. If it gets plain subagents, it spawns again
saying "as an agent team". If that keeps happening, check agent teams are on (above) and that
your Claude Code version supports them.

### The sketch preview server will not start

It tries ports 8765 to 8814 on `127.0.0.1` and exits with `no free port in 8765-8814` if all are
taken. Stop old preview servers (find them with `lsof -i :8765`), or ask anu to start it from
another port: the third argument of `serve.py` is the start port.

### The sketch does not reload

The server reloads a page when any file under the watched folder changes, checking every 0.8
seconds. Make sure you opened the page through the server URL it printed, not as a `file://`
path, and that the file you edit is under `docs/sketches/`.

### QA cannot reach a screen behind a login

The app has no dev sign-in route, or `## anu` has the wrong URL. See
[Configuration → Dev sign-in](configuration.md#dev-sign-in). Agents never type passwords into a
sign-in form, so there is no other way in.

### The local stack is already running

anu reuses a running stack and never starts a second copy. It never stops a stack another session
started; the session that started it stops it.

### A task's notes cannot be found

Notes are found by the exact ID folder on the task's branch: a worktree on `task/<ID>-…` holding
`docs/work-notes/<ID>/state.json`. Run `/anu:resume` with no ID to list every task worktree. If
the branch exists only on the remote, `/anu:resume <ID>` re-creates its worktree.

## Giving feedback on anu

At the end of every `/anu:submit`, anu asks whether anything was friction, confusing, or worth
changing, and puts your answer in the PR under `## anu feedback`. To change anu itself, see
[Changing anu](contributing.md).
