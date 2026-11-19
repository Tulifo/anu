#!/usr/bin/env python3
"""PreToolUse hook: stop anu's read-only agents from writing through the shell.

Claude Code passes the tool call as JSON on stdin. Exit 2 refuses the call and shows stderr to
the agent. Every other agent, and the main session, passes straight through.
"""
import json
import re
import sys

# Matched on the name after the plugin prefix, so "anu:qa-engineer" and "qa-engineer" both count.
READ_ONLY = {"qa-engineer", "security-engineer"}

# shortcut: pattern match, not a shell parser. A write hidden in `python -c`, `node -e` or
# `bash -c "..."` passes. Upgrade to an OS sandbox if a reviewer must be held, not just stopped.
START = r"(?:^|[;&|({`]|\$\(|\bxargs\b|-exec\b)\s*(?:sudo\s+)?"
GIT = START + r"git\b(?:\s+(?:-[cC]\s+\S+|--?[\w-]+(?:=\S+)?))*\s+"
RULES = [
    (START + r"(?:rm|rmdir|mv|cp|tee|touch|mkdir|chmod|chown|ln|truncate|dd|patch)\b", "changes files"),
    (r"\b(?:sed|perl)\b[^|;&]*\s-\w*i", "edits a file in place"),
    (GIT + r"(?:add|am|apply|checkout|cherry-pick|clean|commit|merge|mv|pull|push|rebase|reset"
           r"|restore|revert|rm|stash|switch|tag)\b", "changes git state"),
    (GIT + r"(?:branch\s+(?:-[dDmMcCf]|[^-\s])|worktree\s+(?:add|move|prune|remove))", "changes git state"),
]
QUOTED = r"'[^']*'|\"(?:\\.|[^\"\\])*\""
REDIRECT = r"(?<![-=])>>?\s*(?!&|>|/dev/(?:null|stderr|stdout)\b)\S"


def refusal(command):
    """Why the command is refused, or None."""
    for pattern, why in RULES:
        if re.search(pattern, command, re.M):
            return why
    if re.search(REDIRECT, re.sub(QUOTED, '""', command)):
        return "writes to a file"
    return None


if __name__ == "__main__":
    call = json.load(sys.stdin)
    agent = call.get("agent_type") or ""
    why = refusal(call.get("tool_input", {}).get("command", "")) if agent.rsplit(":", 1)[-1] in READ_ONLY else None
    if why:
        print(f"anu: {agent} is read-only and this command {why}. "
              "Report the change you need to its owner instead.", file=sys.stderr)
        sys.exit(2)
