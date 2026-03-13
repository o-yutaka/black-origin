from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from BLACK_ORIGIN.kernel.system import BlackOriginSystem

MENU = [
    "Chat", "Agents", "Knowledge Graph", "World Model", "Simulation", "Research Lab", "AI Lab",
    "Civilization Map", "Universe", "Memory Timeline", "Computer Control", "System Monitor", "Settings"
]


def render_ui() -> str:
    items = "".join(f"<li>{item}</li>" for item in MENU)
    return f"""
<html><head><meta charset='utf-8'><style>
body{{margin:0;background:#0a0a0f;color:#fff;font-family:Inter,Arial,sans-serif;overflow:hidden;}}
.menu-btn{{position:fixed;top:16px;left:16px;background:#151522;border:none;color:#fff;padding:10px 14px;border-radius:8px;cursor:pointer;}}
.drawer{{position:fixed;left:-280px;top:0;bottom:0;width:260px;background:#12121b;transition:left .35s ease;padding:72px 20px;overflow:auto;}}
.drawer.open{{left:0;}}
li{{list-style:none;padding:10px;border-bottom:1px solid #27273a;}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:80px 24px 24px 24px;}}
.card{{background:linear-gradient(145deg,#171726,#0e0e18);padding:18px;border-radius:14px;min-height:140px;animation:float 4s ease-in-out infinite;}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
</style></head>
<body>
<button class='menu-btn' onclick="document.getElementById('drawer').classList.toggle('open')">☰ Menu</button>
<aside id='drawer' class='drawer'><ul>{items}</ul></aside>
<main class='grid'>
<div class='card'>Knowledge Graph (live)</div><div class='card'>Agent Network (live)</div><div class='card'>Civilization Map (live)</div>
<div class='card'>Synthetic Universe (live)</div><div class='card'>AI Reasoning Stream (live)</div><div class='card'>System Telemetry</div>
</main>
</body></html>
"""


class Handler(BaseHTTPRequestHandler):
    system = BlackOriginSystem()

    def do_GET(self) -> None:
        if self.path == "/":
            content = render_ui().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        if self.path == "/api/cycle":
            payload = json.dumps(self.system.run_cycle({"planet": "earth", "mode": "api"})).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_error(404, "Not Found")


def run_server(host: str = "0.0.0.0", port: int = 8080) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.serve_forever()
