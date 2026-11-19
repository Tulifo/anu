# Changing anu

## Repo layout

```
.claude-plugin/
  plugin.json          name, version, description — the only place the version lives
  marketplace.json     lets `claude plugin marketplace add Tulifo/anu` find the plugin
  icon.png             1024×1024 icon, rendered from assets/logo.svg
agents/                tech-lead, senior-dev, qa-engineer, security-engineer
hooks/                 hooks.json and read_only.py: the shell is read-only for QA and security
skills/<name>/SKILL.md one folder per command; /anu:<name> runs it
skills/sketch/serve.py the sketch preview server (standard library only)
assets/logo.svg        the logo, source of the icon
docs/                  this documentation
scripts/check.py       the checks every pull request must pass
tests/                 tests for the hook and the preview server
.github/               the check workflow and the feedback issue template
CHANGELOG.md           one entry per version
LICENSE                MIT
README.md
```

## Rules for skills

- **Frontmatter:** `name` (the same as the folder), `description` (what it does and when to use
  it — Claude Code picks skills by this line), and `argument-hint` when it takes input.
- **Input** arrives as `$ARGUMENTS`. A file shipped next to the skill is reached with
  `${CLAUDE_SKILL_DIR}`, as the sketch skill does with `serve.py`.
- **First step, every skill:** read `## anu` in the repo's CLAUDE.md and stop with "Run
  /anu:setup first." if it is missing.
- **No app facts.** No product names, ports, stacks or incident stories. Anything app-specific
  belongs in the app's `## anu` section.
- **Plain words:** brief, sketch, task, lessons, submit, work notes.
- **Short:** each SKILL.md stays under about 150 lines. Move detail to the agent that needs it,
  or cut it.
- **Stops** are only the design stops in `/anu:idea` and the PR merge. A new stop needs a reason
  that is a problem, not a decision (see [How it works → Where it stops](how-it-works.md#where-it-stops)).
- **Base branch:** never write `main`. Write `origin/<base>` and define `<base>` in "Before you
  start" as `Base branch` in `## anu`, `main` if the key is absent.
- **No machine paths in committed files.** Find a worktree by its branch.
- **Docs in the same PR:** a change to a skill changes its section in
  [Commands](commands.md) too.
- **Git:** work in a worktree off `origin/<base>`, never on the base branch; add files by name; `--body-file`
  for PR bodies; never merge; no AI trailer in commits or PRs.

## Rules for agents

- **Frontmatter:** `name`, `description`, `model`, and `disallowedTools` for read-only agents.
- **Models are pinned in the agent file:** tech-lead `fable`, senior-dev `opus`, security-engineer
  `opus`, qa-engineer `sonnet`. Skills spawn by agent type and never name a model.
- **Read-only agents** (QA, security) list `Edit, Write, NotebookEdit` in `disallowedTools`, say
  in their instructions that the shell is read-only too, and are named in `READ_ONLY` in
  `hooks/read_only.py`, which refuses their shell commands that write.
- **No** `hooks`, `mcpServers` or `permissionMode` in agent files: Claude Code ignores them in a
  plugin's agents. That is why the read-only rule is a plugin hook.

## Try a change locally

From your branch's checkout, load the plugin from the folder instead of the installed copy:

```bash
claude --plugin-dir . plugin list
```

```bash
claude --plugin-dir . plugin details anu
```

Both should show anu with 13 skills and 4 agents. To try a command in an app repo, start Claude
Code there with `--plugin-dir <path to your anu checkout>`.

## Check before a PR

```bash
claude plugin validate .
```

It must pass. Then the checks the pull request runs (`.github/workflows/check.yml`):

```bash
python3 scripts/check.py
```

```bash
python3 -m unittest discover -s tests
```

`check.py` checks the manifests agree and the version has a changelog entry, every skill and
agent is named after its file, is short and has a section in the docs, and every relative link
and anchor resolves. The tests cover the read-only hook and the preview server.

One check stays by hand: no app or product facts crept in. Grep the diff for ports, product
names and stack names.

## Release

1. Branch off `main` (better, a worktree), make the change, run the checks.
2. Bump `version` in `.claude-plugin/plugin.json` — patch for wording and fixes, minor for a
   behaviour change — and add its entry at the top of `CHANGELOG.md`. Installs do not move
   without a bump.
3. Commit under your own name, push, open a PR. `main` is protected: every change goes through a
   PR whose `check` run passes, history stays linear (rebase or squash merge, no merge
   commits), and force pushes are blocked.
4. After the merge, tag the release on `main`: `git tag v<version> origin/main` and
   `git push origin v<version>`.
5. Everyone updates with:

```bash
claude plugin update anu@anu
```

## The logo

`assets/logo.svg` is the source: a single-storey "a" with one orbit and a particle — *anu* means
a tiny particle. The README shows the SVG.

`.claude-plugin/icon.png` is the plugin icon, rendered from the SVG at 1024×1024 (the plugin
directory accepts a square PNG or JPEG of 512–2048 px, no SVG). After changing the SVG, render it
again with headless Chrome, from a page that shows the SVG at 1024 px:

```bash
printf '<body style="margin:0"><img src="file://%s/assets/logo.svg" width="1024" height="1024" style="display:block">' "$PWD" > /tmp/anu-icon.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
  --default-background-color=00000000 --window-size=1024,1024 \
  --screenshot="$PWD/.claude-plugin/icon.png" file:///tmp/anu-icon.html
```

Run it from the repo root, then open the PNG and check it before committing.
