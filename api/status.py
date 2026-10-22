"""GET /api/status - tells the page whether the server has an OpenRouter key.

Vercel file-based Python function: api/status.py -> /api/status
"""
import json
import os
import sys

# make the shared module importable no matter where the runtime puts us
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT, os.path.dirname(os.path.abspath(__file__))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from _core import KEY, MODEL, MODELS  # noqa: E402
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

    def do_GET(self):
        self._send(200, {
            "ai": bool(KEY),
            "server_has_key": bool(KEY),
            "model": MODEL,
            "models": MODELS,
            "service": "openrouter",
            "status": "ok",
        })

    def do_POST(self):
        self._send(405, {"error": "method not allowed"})
