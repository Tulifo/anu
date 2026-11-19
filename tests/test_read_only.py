import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "read_only.py"

REFUSED = [
    "echo x > notes.txt",
    "cat <<EOF >> src/app.ts\nx\nEOF",
    "npm test 2> errors.log",
    "rm -rf build",
    "cd app && mv a b",
    "find . -name '*.tmp' -exec rm {} +",
    "git ls-files | xargs rm",
    "sed -i '' 's/a/b/' src/app.ts",
    "perl -pi -e 's/a/b/' src/app.ts",
    "git commit -m wip",
    "git -C ../api push",
    "git --no-pager stash",
    "git checkout main",
    "git branch -D task/CS-1-x",
    "git branch scratch",
    "git worktree add ../x",
    "npm test\ngit add .",
]
ALLOWED = [
    "git status --porcelain",
    "git diff origin/main...HEAD",
    "git log --oneline -5",
    "git branch --show-current",
    "git worktree list",
    "git fetch origin",
    "npm test 2>&1 | tail -20",
    "npm run lint > /dev/null 2>&1",
    "grep -rn 'x => y' src",
    "grep -n \"a -> b\" src/app.ts",
    "grep -rn 'rm -rf' scripts",
    "sed -n 1,20p src/app.ts",
    "ls -la && cat package.json",
]


def run(command, agent):
    call = {"tool_name": "Bash", "tool_input": {"command": command}}
    if agent:
        call["agent_type"] = agent
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(call),
                          capture_output=True, text=True)


class ReadOnlyHook(unittest.TestCase):
    def test_refuses_writes_from_read_only_agents(self):
        for agent in ("anu:qa-engineer", "anu:security-engineer", "qa-engineer"):
            for command in REFUSED:
                with self.subTest(agent=agent, command=command):
                    result = run(command, agent)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("read-only", result.stderr)

    def test_allows_reads_from_read_only_agents(self):
        for command in ALLOWED:
            with self.subTest(command=command):
                self.assertEqual(run(command, "anu:qa-engineer").returncode, 0)

    def test_leaves_every_other_caller_alone(self):
        for agent in ("anu:senior-dev", "anu:tech-lead", "Explore", None):
            with self.subTest(agent=agent):
                self.assertEqual(run("rm -rf build && git push", agent).returncode, 0)


if __name__ == "__main__":
    unittest.main()
