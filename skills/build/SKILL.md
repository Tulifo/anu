---
name: build
description: Take one task to finished code ready for review with the agent team — the tech lead studies and plans it (stops for the user's OK), two senior devs build two slices, QA checks it in the running app, security reviews the diff, and the lead opens the PR. Use for /anu:build CS-14, in a session started with `claude --agent anu:tech-lead`.
argument-hint: "<task ID>"
---

# /anu:build — one task, built by the team

Task: $ARGUMENTS

## Before you start

- You are the tech lead. If this session is not running as the anu tech lead, stop and say:
  "Start with `claude --agent anu:tech-lead`, then run `/anu:build <ID>`."
- Agent teams must be on: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` prints `1`. If not, stop
  and say: "Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to `1` in the `env` of
  ~/.claude/settings.json, then restart."
- Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first."

## 1. Study and plan — you, before anyone is spawned

Find the task and its state.json by exact ID, and carry on from `stage`:
- `null` → /anu:study (checks the blockers are merged, makes the worktree), then plan.
- `studied` → /anu:plan. The plan needs two slices with no file in common and the shared
  interfaces written out. It stops for the user's OK.
- `planned` → step 2. `made` → step 5. `submitted` → hand over to /anu:resume.

## 2. Start the local stack

From the task's worktree, start the local stack from `## anu` in the background unless one is
already running, and seed it if the app has a seed step. Never start a second copy; never stop
one another session started (check `lsof -a -p <pid> -d cwd`).

## 3. Spawn the team — as an agent team

Create the shared tasks with their dependencies:
- `stack` → you (step 2)
- `slice-a`, `slice-b` → `anu:senior-dev` named `dev-a` and `dev-b`, blocked by `stack`
- `qa` → `anu:qa-engineer` named `qa`, blocked by both slices
- `security` → `anu:security-engineer` named `security`, blocked by both slices
- `land` → you, blocked by `qa` and `security`

Spawn by agent type and never name a model: each definition sets its own. Spawn them as an agent
team, as teammates. If a spawn gives plain subagents instead, spawn again and say "as an agent
team".

Teammates do not see this conversation. Every spawn prompt carries:
- the task ID, the worktree path, and the paths of the task file, `study.md` and `plan.md`;
- its slice, the exact files it owns, and the shared interfaces verbatim;
- the `## anu` facts it needs: checks, local stack URL and ports, dev sign-in URL and users,
  screen sizes, themes;
- what is out of this task;
- who it reports to, and the rule: never edit a file another teammate owns — message its owner
  with the exact change.

## 4. Run it

- Do not build a slice yourself while teammates work.
- A slice is done when its dev reports the checks green, `qa` has verified it in the running app
  (dev sign-in, light and dark, every size in `## anu`), and `security` has cleared its diff.
- Send each defect or finding to the owning dev by name; ask `qa` or `security` to re-check
  after the fix.
- Answer teammate permission prompts in your session.
- A teammate silent for 10 minutes gets a ping; still silent → do its remaining check yourself
  and say so in the PR.
- Post one short status line to the user when a shared task changes state.
- No stop between the plan OK and the PR: decide, and add each call to `plan.md` under
  `## Decisions taken`.

## 5. Land it

When `qa` and `security` pass, set `stage: "made"` and run /anu:submit. In the PR body, next to
`## Decisions taken`, add `## Slices` (who built what), `## QA` (what was verified, sizes,
themes) and `## Security` (findings and their status).

## 6. Close

Ask each teammate to shut down, and stop the local stack if you started it. Report to the user:
PR links, what QA verified, security findings and their status, decisions taken, and what was
left out and why.
