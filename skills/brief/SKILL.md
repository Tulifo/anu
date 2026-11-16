---
name: brief
description: Write the feature description (the brief) — the problem and who has it, what people do on each screen, the data and server changes, who may do what, and what is out — after the user picks an approach. Saves docs/briefs/YYYY-MM-DD-<feature>.md. Use for /anu:brief, or when /anu:idea reaches the brief.
argument-hint: "<idea or feature>"
---

# /anu:brief — write the feature description

Input: $ARGUMENTS (an idea, a feature name, or nothing to continue the current design branch).

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Work in the
feature's `design/<feature>` worktree (see /anu:idea step 1), never on main.

## 1. Read before asking

- Briefs in `docs/briefs/` and tasks in `docs/tasks/` on `origin/main`: was part of this
  designed already?
- The code: search for anything close to the idea (a field, a flag, an endpoint, a screen). Tell
  the user what you found before proposing anything; extending what exists usually beats a second
  way of doing the same thing.
- `LESSONS.md` entries for the area.

If the idea spans unrelated parts of the app, say so and ask which part to brief first.

## 2. Ask, one question at a time

Only what you cannot find out: the problem and who has it, who uses the feature and how often,
what done looks like, limits (security, data, speed, existing data), what is out. Skip what is
already clear.

## 3. Choose the approach — stop

Give 2–3 approaches, your pick first, each in 3–4 sentences with what it costs and what it rules
out. Wait for the user's choice.

## 4. Write the brief

```markdown
# <Feature> — brief

Date: YYYY-MM-DD
Status: draft

## What and why
<2–3 sentences: the problem, for whom, what changes for them>

## Done means
- <something a user can see or measure>

## Who does what
- As a <role>, I can <action>, so that <outcome>.

## Screens
### <Screen name>
- Tasks, most frequent first: <task> (<many times a day | weekly | rarely>, <role>)
- Where rare tasks live: <··· menu | setting | editor>
- Reference: <how the design references in `## anu` do this>

## Data and server
- Data: <tables or collections, fields added or changed>
- Server: <endpoints, functions, jobs — inputs, outputs, errors>
- Access: <who may read and change what>

## Out
- <what this feature will not do>

## Open questions
- <question> → <answer, or who decides>

## Decisions taken
- <decision> — <why>
```

A screen lists what people do there, not what the system can do: a field or endpoint that exists
does not earn a control, and a rare task never sits on the main view. If you do not know how
often a task happens, ask.

Before showing it: no TBDs, nothing that clashes with endpoints or tables the code already has,
and every screen task traces to a "Who does what" line.

## 5. OK the brief — stop

Show the brief. Apply changes until the user says OK, then set `Status: agreed`.

## 6. Save

Save `docs/briefs/YYYY-MM-DD-<feature>.md` (today's date). `git add` that file only and commit
"Brief: <feature>". Say the path. Next: /anu:sketch (inside /anu:idea it runs on its own).
