---
name: make
description: Write the code for a planned task in its worktree — every change in the plan, tests for new logic, the checks from `## anu`, and a look at each changed screen in the running app — without pausing between parts. Use for /anu:make CS-14 to build alone; /anu:build uses the agent team instead.
argument-hint: "<task ID>"
---

# /anu:make — write the code

Task: $ARGUMENTS

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Find the task's
worktree and state.json by exact ID and work there.

Step 3 needs a browser tool and, for a screen behind sign-in, a dev sign-in URL in `## anu`. If
one is missing, stop now and say which and how to get it (the Playwright MCP; /anu:setup for the
route). Go on only if the user says so, and report those screens as not checked.

The normal start is `stage: "planned"`. Stage `studied` → run /anu:plan first, then carry on.
Stage `made` or later → say so and ask: rework, or go on to /anu:submit.

Read the task, `study.md`, `plan.md`, the `LESSONS.md` entries `study.md` lists, and the sketch
screenshots in `docs/work-notes/<ID>/shots/`.

## 1. Build, in plan order, without stopping

- Follow the patterns `study.md` names. No option, wrapper or abstraction the task does not need.
- Every new piece of logic (a branch, a parser, a permission check, anything with money) gets a
  test. Keep every existing test passing; delete none.
- Server: check who is calling and what they may do on the server, never trusting the client.
  Validate input at the edge. No secrets in client code or commits.
- Screen: only the app's tokens and components and the icons from `## anu`, with real loading,
  empty and error states.
- A gap the plan does not cover: decide without stopping — the brief's default, else the smallest
  choice that exposes no more data than the brief allows — and add it to `plan.md` under
  `## Decisions taken`.
- A path the plan writes as `<repo>:<path>` is changed in that repo's `task/<ID>-<slug>`
  worktree, never in its main checkout.
- Do not pause after each part. Do not commit; /anu:submit commits.

## 2. Check

Run every command in `## anu` `Checks:`. Fix failures; never skip or weaken a test to get a pass.

## 3. Look at it running

Start the local stack from `## anu` unless it is already running; never start a second copy and
never stop one another session started. Sign in with the dev sign-in URL — never type a
password. For each screen the task changes, at every size in `## anu`, light and dark:
- compare with the sketch screenshots: layout, sizes, spacing, icons, copy;
- check loading, empty and error states, Esc and focus return on dialogs, keyboard reach;
- save screenshots as `docs/work-notes/<ID>/shots/built-<screen>-<size>-<theme>.png`.

Fix what differs. A difference you keep on purpose goes under `## Decisions taken`.

## 4. Finish

Set `stage: "made"` and `updated` in state.json. Report: files changed, check results, what you
looked at in the app (sizes, themes), decisions taken, anything left out and why.
Next: /anu:submit <ID>.
