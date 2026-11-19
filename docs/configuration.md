# Configuration

anu has no settings of its own. Everything it needs to know about an app lives in that app's
repo, in three places:

| Where | What | Written by |
|---|---|---|
| `CLAUDE.md`, section `## anu` | the app's facts | `/anu:setup` |
| `.claude/settings.json` | anu turned on for everyone who opens the repo | `/anu:setup` |
| `~/.claude/settings.json` (yours) | agent teams turned on | you, once per machine |

## The `## anu` section

Every command reads these keys by name, so keep the keys and their order. Edit the values by
hand whenever they change; run `/anu:setup` again to have it re-read the repo.

```markdown
## anu

- Stack: TypeScript, Next.js, Postgres (Prisma), Fly.io
- Checks: `pnpm typecheck`, `pnpm lint`, `pnpm test`
- Local stack: `pnpm dev`; app http://localhost:3000; postgres :5432
- Dev sign-in: http://localhost:3000/dev/login?as=<user>&next=<path> (users: admin, member)
- Screen sizes: 390x844, 1280x800
- Themes: light, dark (switch: class `dark` on html)
- Styles: `src/styles/tokens.css`; components: `src/components/ui`; icons: lucide (`node_modules/lucide-static/icons`)
- Task prefix: CS
- Base branch: main
- Design references: Linear settings pages, Stripe dashboard tables
- Other repos: none
```

An `## anu` section written before 0.3.0 has no `Base branch` line; anu then uses `main`.

| Key | What it holds | Who uses it |
|---|---|---|
| `Stack` | languages, frameworks, database, hosting | everyone, to read the code the right way |
| `Checks` | every command that must pass before a PR: type check, lint, tests | make, submit, the devs, QA |
| `Local stack` | the start command, the app URL, every port | make, submit, the lead, QA |
| `Dev sign-in` | the URL that opens a session without a password, and the seeded users; `none yet`, or `none (no sign-in)` | sketch checks, make, build, QA, screen-check |
| `Screen sizes` | every size screens are drawn and checked at (default `390x844, 1280x800`) | sketch, study, make, QA |
| `Themes` | the themes and the class or attribute that switches them | sketch, make, QA |
| `Styles` | the tokens file, the component folder, the icon package and where its SVG data lives | sketch, make, the devs |
| `Task prefix` | the letters in front of every task ID (`CS` → `CS-14`) | tasks, study, resume |
| `Base branch` | the branch worktrees start from and PRs go to: the repo's default branch | every command that branches, rebases or compares |
| `Design references` | apps, screens or files sketches should match | brief, sketch |
| `Other repos` | other repos a task here may also change, each with its path from this repo's main checkout (`api (../api)`) | study (blockers), plan (a worktree there), submit (one PR per repo) |

## Dev sign-in

QA, the screen checks and `/anu:make` reach screens behind a login through a dev-only sign-in
route, because no agent ever types a password into a sign-in form. A typical route:

```
GET /dev/login?as=admin&next=/settings/members
```

The server looks up the seeded user `admin`, sets the session cookie, and redirects to `next`.
The credentials stay on the server; the agent only opens a URL.

The route must be safe to ship in the codebase:

- It answers only when the app is **not** running in production, and that check is **in the
  handler itself** (`NODE_ENV !== "production"` or the stack's equivalent).
- **No env flag, query string or setting** can open it on a deployed host. A switch that opens a
  password-free session in production is a security hole, so there is none.
- It signs in only seeded test users, and checks `next` is a path on the same site.
- It has tests: it works locally, it returns 404 in production mode, and it rejects an outside
  `next`.

If the app has no such route, `/anu:setup` asks whether to build one now, on the setup branch,
following the rules above. If you say no it writes `Dev sign-in: none yet`, and `/anu:build` and
`/anu:make` then stop at the start: QA cannot reach a screen behind a login. An app with no
sign-in at all gets `none (no sign-in)`, which stops nothing.

## `.claude/settings.json` in the app repo

Setup merges this in, keeping every existing key, so anyone who opens the repo in Claude Code is
offered anu:

```json
{
  "extraKnownMarketplaces": {
    "anu": { "source": { "source": "github", "repo": "Tulifo/anu" } }
  },
  "enabledPlugins": { "anu@anu": true }
}
```

## Agent teams

`/anu:build` needs agent teams, an experimental Claude Code feature, turned on in your own
`~/.claude/settings.json`:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

Restart Claude Code after changing it. The solo path (`/anu:study` → `/anu:plan` → `/anu:make` →
`/anu:submit`) works without it.

## `.gitignore`

Setup adds `.claude/worktrees/`, where anu makes its worktrees, so they are never committed.

## `docs/todo.md`

```markdown
# To do

Next: CS-17

## Coming
- CS-14 Invite a member — docs/tasks/CS-14-invite-member.md

## Follow-ups
- `src/billing/close.ts:88` — the lock is held across a network call
```

- `Next:` is the only source of new task IDs. Edit it by hand only to skip numbers.
- `## Coming` lists designed tasks not yet merged. `/anu:tasks` drops lines whose PR is merged.
- `## Follow-ups` holds things to fix, one line each with a file:line, from `/anu:lessons` and
  from reviews.

## `LESSONS.md`

What broke before and must not break again, one entry per lesson, appended by `/anu:lessons`:

```markdown
## Lock the row before reading the total

File: `src/billing/close.ts:88` (closeInvoice)
Why: two closes at once read the same total and both charge
What breaks: customers are charged twice
Added: 2026-11-16
```

Study lists the entries for every file a task touches, and the devs read them before editing.
