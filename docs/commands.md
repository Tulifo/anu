# Commands

anu has 13 commands. Two cover most days: `/anu:idea` designs a feature, `/anu:build` builds a
task. The rest are the steps those two run, and you can run any of them on its own.

Every command first reads the `## anu` section of the repo's CLAUDE.md and stops with "Run
/anu:setup first." if it is missing.

| Command | Use it to | Stops for you |
|---|---|---|
| [`/anu:setup`](#anusetup) | prepare an app repo, once | only what it cannot find in the repo |
| [`/anu:idea "<idea>"`](#anuidea) | idea → brief → sketches → tasks, one PR | approach, brief, each sketch, task list |
| [`/anu:brief`](#anubrief) | write the feature description | approach, brief |
| [`/anu:sketch`](#anusketch) | draw the screens as HTML | each sketch |
| [`/anu:screen-check`](#anuscreen-check) | check a screen is easy and safe to use | no |
| [`/anu:tasks`](#anutasks) | split a feature into numbered tasks | task list |
| [`/anu:build <ID>`](#anubuild) | one task → PR, with the agent team | no |
| [`/anu:study <ID>`](#anustudy) | read the task and the code first | unmerged blocker or design PR |
| [`/anu:plan <ID>`](#anuplan) | list the changes and the slices | no |
| [`/anu:make <ID>`](#anumake) | write the code alone | no |
| [`/anu:submit <ID>`](#anusubmit) | independent check, push, open the PR | no |
| [`/anu:resume <ID>`](#anuresume) | continue where a session stopped | only if the place is wrong |
| [`/anu:lessons`](#anulessons) | record what broke before | the file list and each lesson |

---

## /anu:setup

Prepare an app repo to use anu. Run once per app, inside the app repo.

**Steps**

1. Make a worktree on `anu/setup` off `origin/main`. If CLAUDE.md on `origin/main` already has
   `## anu`, show it and ask what to change instead of starting over.
2. Find each fact in the repo: stack, checks, local stack and ports, dev sign-in route, screen
   sizes, themes, styles, other repos. Ask in one message only what is missing — usually the
   task prefix and the design references.
3. Write the `## anu` section (see [Configuration](configuration.md)).
4. Create `docs/briefs/`, `docs/sketches/`, `docs/tasks/`, `docs/work-notes/` (each with a
   `.gitkeep`), `docs/todo.md` with `Next: <PREFIX>-1`, and `LESSONS.md`. Add
   `.claude/worktrees/` to `.gitignore`.
5. Merge anu into `.claude/settings.json` so it is on for everyone who opens the repo.
6. List the repo's own agents and skills that do anu's job, and delete them only on your yes,
   after moving any app facts they hold into CLAUDE.md.
7. Commit, push, open the PR "Set up anu".

**Writes** CLAUDE.md, `.claude/settings.json`, `.gitignore`, `docs/`, `LESSONS.md`.

**Next** merge the PR, then `/anu:idea "<idea>"`.

---

## /anu:idea

Take an idea all the way to tasks a developer can build, on one branch and one PR.

```
/anu:idea "members can invite others by email"
```

With no idea given, it shows `## Coming` from `docs/todo.md` and asks what to design.

**Steps**

1. Pick a kebab-case feature name. Look for work already started (a `design/<feature>` branch or
   worktree, or a brief on `origin/main`) and carry on from the first missing step. Otherwise make
   or reuse a worktree on `design/<feature>`.
2. Run `/anu:brief`.
3. Run `/anu:sketch` for every screen the brief lists (skipped if the feature has no screen).
4. Run `/anu:tasks`, which opens the PR.

**Stops** exactly four kinds: the approach, the brief, each sketch, the task list. If you give
vague feedback twice on the same thing ("not right"), it asks what is wrong — broken, looks off,
or the wrong direction — before a third try.

**Next** merge the PR, then `claude --agent anu:tech-lead` and `/anu:build <first ID>`.

---

## /anu:brief

Write the feature description. Usually run by `/anu:idea`.

**Steps**

1. Read before asking: earlier briefs and tasks, the code (anything close to the idea), and
   `LESSONS.md` for the area. Tell you what already exists — extending it usually beats a
   second way of doing the same thing.
2. Ask, one question at a time, only what it cannot find: the problem and who has it, how often,
   what done looks like, limits, what is out.
3. **Stop:** give 2–3 approaches, its pick first, each with what it costs and what it rules out.
4. Write the brief: what and why, done means, who does what, screens (tasks most frequent first),
   data and server, access, out, open questions, decisions taken.
5. **Stop:** show the brief and apply changes until you OK it. `Status: agreed`.

A screen lists what people do there, not what the system can do: an existing field or endpoint
does not earn a button, and a rare task never sits on the main view.

**Writes** `docs/briefs/YYYY-MM-DD-<feature>.md`, committed as "Brief: <feature>".

---

## /anu:sketch

Draw each screen as an HTML file that uses the app's real styles, icons and realistic data, and
show it in your browser with live reload.

**Steps**

1. Read the brief, the styles file, and two or three real screens of the app.
2. Plan each screen from its tasks: the top one or two own the screen; every other task gets a
   line saying where it lives (a ··· menu, a setting, the editor).
3. Draw `screen-NN-<name>.html`:
   - only the app's tokens as `var(--token)`, no raw colours or new spacing;
   - components shaped like the real ones, named in a comment where not obvious;
   - icons copied as real SVG path data from the installed icon package, never drawn from memory;
   - realistic sample data (a long name that wraps; never lorem ipsum, never real customer data);
   - loading, empty and error states, and each dialog or menu;
   - a light/dark switch that flips the app's real theme hook.
4. Check every screen size in `## anu`, light and dark. If a size needs its own layout, draw a
   `-narrow.html` version.
5. Run `/anu:screen-check` and fix every problem before you see it.
6. **Stop, one sketch at a time:** start the preview server once and open the screen in your
   browser. Edits reload the page by themselves.

The preview server is `skills/sketch/serve.py`, standard library only. It binds `127.0.0.1`
(never your network), starts at port 8765 and moves to the next free port if that one is busy,
and injects a small script that reloads the page when a file under `docs/sketches/` changes.

**Writes** `docs/sketches/YYYY-MM-DD-<feature>/` (`screens.md`, one HTML file per screen, and
`tokens.css` when the styles file cannot be linked), committed as "Sketches: <feature>".

**Rule** a sketch counts only as a file under `docs/sketches/`. A link to a design tool, a canvas
or a chat artifact is not a sketch.

---

## /anu:screen-check

Check a screen — a sketch or a built page — is easy and safe to use. Looks are judged elsewhere.

```
/anu:screen-check docs/sketches/2026-11-16-member-invites/screen-02-invite.html
/anu:screen-check http://localhost:3000/settings/members
```

**The ten checks**

1. Looking is safe; changing is on purpose (edit mode, Save, old → new for values that matter).
2. Errors are prevented, not reported; a destructive action is never the default or one key away.
3. Confirm and undo fit the cost: Undo for cheap changes, a named confirm for costly or final ones.
4. Focus and keyboard: focus lands on the top task; Esc closes and returns focus; frequent tasks
   work from the keyboard.
5. One meaning per control, the same across screens.
6. State is visible, never by colour alone.
7. Walk the top two tasks click by click, then the likeliest mistake in each.
8. Only what the frequent tasks need is on the screen.
9. Safe for every role: hidden, not just disabled; private data masked; nothing secret in a URL.
10. Readable and reachable: contrast in both themes, names for screen readers, 44 px tap targets.

**Output** a table of pass or problem-and-fix per check, the top task's step count, what the
likeliest mistake does, and a verdict: "ready to show" or "fix first". On a sketch it fixes the
problems itself; on a built screen it names the file and the change.

---

## /anu:tasks

Split a feature into numbered tasks and open the design PR.

**Steps**

1. Draft vertical slices: data, server and screen for one behaviour a user can test, 1–3 days
   each. A screen that sets something up comes before the screens that use it.
2. **Stop:** show the numbered list — title, size, blocked by, acceptance lines.
3. Reserve the IDs: rebase onto `origin/main`, read `Next:` in `docs/todo.md`, move it on, add
   the tasks to `## Coming`, and commit that alone ("Reserve CS-14–CS-16").
4. Write one file per task, `docs/tasks/<ID>-<slug>.md`: what and why, acceptance lines, the
   slice (data, server, screen), files likely touched, the pattern to follow, lessons that apply.
5. Rebase again. On a conflict on the `Next:` line, renumber (see
   [How it works → Task IDs](how-it-works.md#task-ids)). Push and open the PR "<Feature>: brief,
   sketches, tasks".

A task with a screen names its exact sketch file. A screen with no sketch file is not ready, and
anu says so instead of writing the task.

---

## /anu:build

One task to a PR with the agent team. Run in a session started with
`claude --agent anu:tech-lead`, with agent teams turned on.

```
/anu:build CS-14
```

**Steps**

1. Study and plan, carrying on from the task's stage. No wait for an OK on the plan.
2. Start the local stack from `## anu` (reuse a running one; never start a second copy).
3. Spawn the team as an agent team, with shared tasks and dependencies:
   `stack` → `slice-a` and `slice-b` (`dev-a`, `dev-b`) → `qa` and `security` → `land`.
4. Run it: a slice is done when its dev reports green checks, QA has verified it in the running
   app, and security has cleared its diff. Defects go back to the owning dev by name.
5. Land it with `/anu:submit`, adding `## Slices` (who built what) to the PR.
6. Shut the team down, stop the local stack if it started it, and report.

**Stops** none until the PR. See [The build team](team.md) for how the team works.

---

## /anu:study

Read a task and the code it touches before changing anything.

**Steps**

1. Find the task file by exact ID on `origin/main`. Not there but on an open `design/*` branch →
   say its design PR is not merged, and go on only if you say so.
2. Already started (a `task/<ID>-` branch with a stage set)? Hand over to `/anu:resume`.
3. Check every blocker's PR is `MERGED`, in this repo and in each of `Other repos`. If not, stop
   and name it.
4. Make or reuse a worktree on `task/<ID>-<slug>` and write `state.json`.
5. Read CLAUDE.md, the `LESSONS.md` entries for the files it may touch, the task, its brief and
   sketches (screenshotting each sketch at every screen size into `shots/`), every file it will
   touch, and one example of each pattern it needs.
6. Write `study.md`: what the task builds, files to touch, patterns to follow (with file:line),
   lessons that apply, risks, decisions taken.

**Writes** `docs/work-notes/<ID>/state.json`, `study.md`, `shots/sketch-*.png`. Stage `studied`.

---

## /anu:plan

List the changes file by file and split them into two slices.

**Steps**

1. Write `plan.md`: changes in order with why; two slices with no file in common (usually the
   screen and the server and data); the shared interfaces written out (endpoints or functions
   with inputs, outputs and errors; data fields; routes and events); each screen's sketch and
   components; tests; how each acceptance line is checked; what is out; decisions taken.
2. Show the plan in a few lines and carry on.

A small task may have one slice, with a reason. A screen with no sketch file stops the plan.

**Writes** `docs/work-notes/<ID>/plan.md`. Stage `planned`. Run it again by hand to redo a plan.

---

## /anu:make

Write the code alone, in plan order, without pausing between parts.

**Steps**

1. Build every change in `plan.md`, following the patterns `study.md` names. Every new piece of
   logic gets a test; no existing test is deleted or weakened. Server code checks the caller on
   the server and validates input. Screens use only the app's tokens, components and icons, with
   loading, empty and error states.
2. Run every command in `Checks:` and fix failures.
3. Look at each changed screen in the running app through the dev sign-in URL, at every screen
   size, light and dark, against the sketch screenshots. Save `built-*.png` screenshots.

A gap the plan does not cover is decided and written under `## Decisions taken`. `/anu:make`
does not commit; `/anu:submit` does.

**Writes** code, tests, `shots/built-*.png`. Stage `made`.

---

## /anu:submit

Check, push and open the PR. The last step of both the team and the solo path.

**Steps**

1. Run every command in `Checks:`. All must pass.
2. **Independent check.** Whoever wrote the code does not sign it off. After `/anu:build`, the
   team's QA and security reports are used. Alone, it starts the local stack and runs two
   read-only agents at the same time: `anu:qa-engineer` walks every acceptance line in the
   running app, and `anu:security-engineer` reviews the diff. Every QA fail and security blocker
   is fixed and re-checked. A "should fix" finding may land, listed under `## Follow-ups`.
3. Commit the task's files by name, under your git identity.
4. `git fetch origin`, `git rebase origin/main`, checks again if new commits came in, push.
5. Open the PR with `--body-file`: What, Task, Acceptance (checked by QA), Security, Checks,
   Decisions taken, Follow-ups, Related PRs, anu feedback. One PR per repo, linked to each other.
6. Ask one question — was anything about anu friction, confusing, or worth changing — and put the
   answer in each PR.

A line that cannot be checked locally (a real mail provider, real payments) is written as "not
checked locally — <why>", never as a pass.

**Writes** commits, the PR. Stage `submitted`. Never merges.

---

## /anu:resume

Continue a task where the last session stopped.

**Steps**

1. Find the worktree whose branch starts with `task/<ID>-` (or re-create it from
   `origin/task/<ID>-*`). With no ID, list every task worktree with its stage and ask which.
2. Check the branch and worktree path match `state.json`; stop and say what differs if not.
3. Show uncommitted files and commits not yet on main. If every PR is merged, set `merged`.
4. Report, then run the next stage.

| Last finished | Runs next |
|---|---|
| `null` | `/anu:study`, then onward |
| `studied` | `/anu:plan`, then onward |
| `planned` | `/anu:make`, or `/anu:build` for the team |
| `made` | `/anu:submit` |
| `submitted` | each PR's state and review comments; fixes what reviewers asked and replies |
| `merged` | done; offers to remove the worktree, only on your yes |

Uncommitted files are the last session's work in progress: kept and carried on from, never
stashed, reset or discarded.

---

## /anu:lessons

Record "this broke before, don't repeat it" in `LESSONS.md`, each lesson tied to a file and line.

```
/anu:lessons
/anu:lessons src/billing/close.ts
/anu:lessons "the double charge fixed in #212"
```

**Steps**

1. Pick a topic and make or reuse a worktree on `lessons/<topic>`.
2. With no starting point, rank up to 15 risky files by churn, fix commits and TODO/FIXME
   markers, and **stop** to let you add or drop files.
3. Read each file and ask about one specific line at a time ("line 88 locks the row before
   reading the total — what goes wrong without the lock?").
4. Keep lessons and follow-ups apart. A lesson is why the code is so and what breaks if it
   changes; it goes in `LESSONS.md`. A follow-up is something to fix; it goes in `docs/todo.md`.
5. **Stop:** show every lesson and follow-up, apply your edits, commit, push, open the PR
   "Lessons: <topic>".

Every lesson has this shape, and none is recorded without a file and line:

```markdown
## Lock the row before reading the total

File: `src/billing/close.ts:88` (closeInvoice)
Why: two closes at once read the same total and both charge
What breaks: customers are charged twice
Added: 2026-11-16
```

The build agents read the `LESSONS.md` entries for every file they touch before changing it.
