"""POST /api/segment - turn a messy brain dump into a clean list of ideas."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _core import KEY, MODEL, MODELS, ask, build_payload  # noqa: E402


class handler:
    """Vercel Python function: BaseHTTPRequestHandler style."""

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
            lang, payload = build_payload("segment", data)
            result, _model = ask("segment", lang, payload)
            self._send(200, result)
        except Exception as e:
            print("AI error:", e)
            self._send(502, {"error": "ai failed"})

    def do_GET(self):
        self._send(405, {"error": "method not allowed"})
