---
name: screen-check
description: Check a screen — a sketch or a built page — is easy and safe to use: looking never changes data, mistakes are prevented, confirm and undo fit the cost, focus and keyboard work, state is visible, roles see only their controls, and the likeliest mistake does no harm. Run by /anu:sketch before every sketch is shown; also on its own for any screen.
argument-hint: "<sketch file or page URL>"
---

# /anu:screen-check — is this screen easy and safe to use

Input: $ARGUMENTS — a sketch file under `docs/sketches/`, or a URL in the running app.

Looks are judged elsewhere. This asks whether people can do their work here without mistakes.

## Before you start

Read `## anu` in the repo's CLAUDE.md; missing → stop: "Run /anu:setup first." Get the screen's
tasks, most frequent first, from `screens.md` or the brief. Open the screen in a browser tool; for
the running app, sign in with the dev sign-in URL from `## anu`.

## The checks

For each one, write pass, or the problem and the fix.

1. **Looking is safe; changing is on purpose.** A screen people mostly read shows values
   read-only. A change starts from a clear action, the user can see they are editing, and it ends
   with Save. Values that matter (money, quantities, permissions) show old → new before saving.
2. **Prevent errors instead of reporting them.** Impossible input is blocked where it is typed.
   The default is the safe choice. A destructive action is never the default, never one key
   away, and sits in a ··· menu.
3. **Confirm and undo fit the cost.** Cheap and reversible: no confirm, offer Undo. Costly or
   final (money, deleting, sending to other people): a confirm that names the object and says what
   will happen. Every save says it happened, in the button's own words.
4. **Focus and keyboard.** Focus lands on the top task's field when the screen opens. Enter
   submits only inside a form the user opened; Esc closes without saving and returns focus. Every
   frequent task works from the keyboard — list the keys. Focus is always visible.
5. **One meaning per control.** The same action has the same name, place and look as on the
   app's other screens. A row click always does the same thing.
6. **State is visible.** The user can tell what is selected, being edited, saved or unsaved,
   loading, and which filter is on. Status never relies on colour alone: add a word or an icon.
7. **Walk the real flow.** Do the top two tasks click by click and count the steps. Then do the
   likeliest mistake in each (wrong row, double click, closing mid-edit, going back, a slow
   network) and say what happens. "Data changes without the user meaning it" fails.
8. **Only what the frequent tasks need.** Rare options sit behind ···, a setting or the editor.
   Labels and units sit next to values. Error messages say what is wrong and how to fix it, in
   plain words.
9. **Safe for every role.** Controls a role cannot use are hidden for that role, not just
   disabled. Private data (emails, phone numbers, amounts) shows only to whoever needs it, masked
   where the full value is not needed. Nothing secret appears in a URL.
10. **Readable and reachable.** Text and icons have enough contrast in light and dark; every
    control has a name a screen reader can read; tap targets are at least 44 px on narrow sizes;
    nothing needs hover to work.

Fewer steps never justify dropping a safeguard from checks 1–3.

## Output

```markdown
### Screen check: <screen>

| # | Check | Result | Fix |
|---|---|---|---|
| 1 | Looking safe, changing on purpose | Pass / Problem: … | … |

Top task: <steps, counted>
Likeliest mistake: <what happens>
Verdict: ready to show | fix first
```

In a sketch, fix every problem yourself and re-run the failed checks before saying "ready to
show". In a built screen, name the file and the change for each problem.
