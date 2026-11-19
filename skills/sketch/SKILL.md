---
name: sketch
description: Draw a feature's screens as HTML sketches with the app's real styles, icons and realistic data, check them at every screen size and with /anu:screen-check, and open them in the user's browser with live reload for an OK. Saves docs/sketches/YYYY-MM-DD-<feature>/. Use for /anu:sketch, or when /anu:idea reaches the screens.
argument-hint: "<feature or brief path>"
---

# /anu:sketch — draw the screens

Input: $ARGUMENTS (a feature name or brief path; default: the brief on the current design branch).

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Work in the
feature's `design/<feature>` worktree, never on the base branch. Read the brief.

From `## anu` take the styles file, the component folder, the icon package, the themes, every
screen size and the design references. Read the styles file and two or three real screens of the
app, so the sketch looks like this app and not a template.

## 1. Plan each screen from the user's tasks

Before drawing a screen:
- List its tasks, most frequent first, with how often and which role (from the brief).
- The top one or two tasks own the screen. Every other task gets one line saying where it lives:
  a ··· menu, a setting, the editor, an import.
- Every visible control traces to a frequent task. That the system can do something is not a
  reason for a button.
- Use the design references' names for things and their flow, unless there is a reason not to.

## 2. Draw

One file per screen: `docs/sketches/YYYY-MM-DD-<feature>/screen-NN-<name>.html`.
- **Styles:** only the app's tokens, as `var(--token)`. Link the styles file by relative path
  when a browser can read it as is; otherwise copy its variable blocks into `tokens.css` in the
  sketch folder, with the source path and date at the top. No raw colours and no new spacing,
  radius or colour. If a screen needs something the styles lack, stop and say what is missing.
- **Components:** shaped like the app's real components. Name the real component in an HTML
  comment where it is not obvious (`<!-- real: Dialog from src/components/ui -->`).
- **Icons:** the real SVG path data, copied from the installed icon package in `## anu`, never
  drawn from memory. List the icon names at the top of the file.
- **Data:** realistic sample data — names, amounts, dates, a long name that wraps. Never lorem
  ipsum; never real customer data.
- **States:** loading, empty and error as labelled sections, plus each dialog or menu the screen opens.
- **Themes:** a light/dark switch that flips the app's real theme hook from `## anu`.

## 3. Check every screen size

Open the sketch in a browser tool (Playwright MCP or a built-in browser) at every size in
`## anu`, light and dark. Look for overflow, clipping, wrapped buttons, cramped tables, and tap
targets under 44 px on narrow sizes. Fix it once in the shared layout where you can. If a size
needs its own layout, draw `screen-NN-<name>-narrow.html` and describe it in `screens.md` under
`Narrow layout`.

## 4. Screen check

Run /anu:screen-check on each screen and fix every problem before the user sees it.

## 5. Show it — stop for each sketch

Start the live-reload server once, in the background, from the worktree root:

```bash
python3 "${CLAUDE_SKILL_DIR}/serve.py" <worktree-root> <worktree-root>/docs/sketches 8765
```

It binds 127.0.0.1, moves to the next free port if 8765 is busy, and prints its URL. Reuse it if
it is already running. Open each screen with `open <url>docs/sketches/<folder>/<file>.html`
(`xdg-open` on Linux). Pages reload themselves when a file changes: edit and save, never ask the
user to refresh.

Show the screen's tasks and the screen-check result in a few lines, and ask for an OK. One sketch
at a time.

## 6. Save

Write `docs/sketches/YYYY-MM-DD-<feature>/screens.md`: for each screen its route, how the user
gets there, tasks most frequent first, layout, components, states, interactions and narrow
layout. Link each sketch file from the brief's Screens section.

`git add` the sketch folder and the brief, commit "Sketches: <feature>". Stop the server after
the last OK.

## Rules

- A sketch counts only as a file under `docs/sketches/`. A link to a canvas, a design tool or a
  chat artifact is not a sketch: save the file first.
- Never call a sketch agreed in a brief or a task until its file exists on disk.
- Vague feedback twice running on the same element: ask what is wrong before a third version.
