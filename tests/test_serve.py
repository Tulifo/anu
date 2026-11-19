import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path

SERVE = Path(__file__).resolve().parent.parent / "skills" / "sketch" / "serve.py"


def start(root, port):
    proc = subprocess.Popen([sys.executable, str(SERVE), str(root), str(root), str(port)],
                            stdout=subprocess.PIPE, text=True)
    return proc, proc.stdout.readline().strip()


def get(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read().decode()


class SketchServer(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.page = self.root / "screen.html"
        self.page.write_text("<html><body><p>hi</p></body></html>")
        self.procs = []

    def tearDown(self):
        for proc in self.procs:
            proc.kill()
            proc.wait()
            proc.stdout.close()

    def serve(self, port=8765):
        proc, url = start(self.root, port)
        self.procs.append(proc)
        return url

    def test_serves_html_with_the_reload_script_and_only_on_localhost(self):
        url = self.serve()
        self.assertTrue(url.startswith("http://127.0.0.1:"))
        body = get(url + "screen.html")
        self.assertIn("<p>hi</p>", body)
        self.assertIn("/__version", body)
        self.assertLess(body.index("/__version"), body.index("</body>"))

    def test_version_changes_when_a_watched_file_changes(self):
        url = self.serve()
        before = get(url + "__version")
        time.sleep(0.05)
        future = time.time() + 10
        self.page.write_text("<html><body><p>changed</p></body></html>")
        import os
        os.utime(self.page, (future, future))
        self.assertNotEqual(before, get(url + "__version"))

    def test_a_busy_port_moves_to_the_next_one(self):
        first = self.serve()
        port = int(first.rsplit(":", 1)[1].strip("/"))
        second = self.serve(port)
        self.assertNotEqual(first, second)
        self.assertIn("<p>hi</p>", get(second + "screen.html"))


if __name__ == "__main__":
    unittest.main()
