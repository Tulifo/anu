#!/usr/bin/env python3
"""Serve sketches on 127.0.0.1 with live reload.

Usage: python3 serve.py <root> [watch-dir] [port]
  root       folder to serve (the worktree root, so a sketch can link the app's styles file)
  watch-dir  folder whose changes reload open pages (default: root)
  port       first port to try (default 8765); the next free one is used if it is busy
"""
import http.server
import sys
from functools import partial
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
WATCH = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT
START = int(sys.argv[3]) if len(sys.argv) > 3 else 8765
RELOAD = (b"<script>(()=>{let v;setInterval(async()=>{try{const n=await(await fetch('/__version'))"
          b".text();if(v&&n!==v)location.reload();v=n}catch(e){}},800)})()</script>")


def version():
    # Walks the tree on every poll: fine for a sketches folder, too slow for a whole repo.
    return str(max((p.stat().st_mtime for p in WATCH.rglob("*") if p.is_file()), default=0))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/__version":
            return self.reply(version().encode(), "text/plain")
        file = Path(self.translate_path(self.path))
        if file.suffix == ".html" and file.is_file():
            body = file.read_bytes()
            body = body.replace(b"</body>", RELOAD + b"</body>", 1) if b"</body>" in body else body + RELOAD
            return self.reply(body, "text/html; charset=utf-8")
        return super().do_GET()

    def reply(self, body, kind):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    allow_reuse_address = False  # so a port another server holds counts as busy


if __name__ == "__main__":
    for port in range(START, START + 50):
        try:
            server = Server(("127.0.0.1", port), partial(Handler, directory=str(ROOT)))
            break
        except OSError:
            continue
    else:
        sys.exit(f"no free port in {START}-{START + 49}")
    print(f"http://127.0.0.1:{port}/", flush=True)
    server.serve_forever()
