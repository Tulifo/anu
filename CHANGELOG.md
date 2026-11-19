# Changelog

The version lives in `.claude-plugin/plugin.json`. Each release is tagged `v<version>`.

## 0.3.0 — 2026-11-19

- **Notes work on any machine.** `state.json` no longer stores the worktree path; the worktree
  is found by its branch. An old `worktree` key is ignored.
- **Any default branch.** `## anu` has a `Base branch` key, filled in by `/anu:setup` from the
  repo's default branch. Without the key, anu uses `main` as before.
- **One-slice tasks.** A task too small to split is built by one developer, not two.
- **Checks before a build.** `/anu:build` and `/anu:make` stop at the start if there is no
  browser tool or no dev sign-in route. `/anu:setup` offers to build the route.
- **Resume a design.** `/anu:resume <feature>` continues a design branch: review comments, or a
  clash on task IDs after the PR is open.
- **Other repos.** `/anu:plan` makes a worktree in each other repo a task changes.
- **Read-only reviewers.** A hook refuses shell commands from the QA and security agents that
  write files or change git state.
- **For the repo itself.** MIT licence, checks on every pull request, tests for the hook and the
  sketch preview server, an issue template for feedback.

## 0.2.2 — 2026-11-16

- Generic wording: no company or product names.

## 0.2.1 — 2026-11-16

- Documentation in `docs/`, a logo and the plugin icon.

## 0.2.0 — 2026-11-16

- No stop between `/anu:build` and the PR; decisions are listed in the PR.
- Independent QA and security review on the solo path too.
- Safe reuse of a session's worktree.

## 0.1.0 — 2026-11-16

- First version: 13 commands and 4 agents.
