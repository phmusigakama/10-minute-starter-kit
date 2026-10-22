"""POST /api/draft - write 2-3 starter idea drafts from the ideas the user kept.

Vercel file-based Python function: api/draft.py -> /api/draft
"""
import json
import os
import sys

# make the shared module importable no matter where the runtime puts us
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT, os.path.dirname(os.path.abspath(__file__))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from _core import KEY, ask, build_payload  # noqa: E402
from http.server import BaseHTTPRequestHandler  # noqa: E402


class handler(BaseHTTPRequestHandler):
    """Vercel Python function."""

    server_version = "StarterKit"

    def _send(self, code, data):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if not KEY:
            return self._send(503, {"error": "no api key"})
        try:
            n = min(int(self.headers.get("Content-Length", 0) or 0), 60000)
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "bad request"})
        try:
            lang, payload = build_payload("draft", data)
            result, _model = ask("draft", lang, payload)
            self._send(200, result)
        except Exception as e:
            print("AI error:", e)
            self._send(502, {"error": "ai failed"})

    def do_GET(self):
        self._send(405, {"error": "method not allowed"})
