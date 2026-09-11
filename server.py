import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from ai_engine import PlumineAIEngine

engine = PlumineAIEngine()

class PlumineHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ["/api/chat", "/api/status", "/api/telemetry"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            payload = {
                "status": "online",
                "core": "Plumine AI Neural Kernel",
                "data": engine.device.system_info()
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return
        if parsed.path in ["/", ""]:
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                data = json.loads(body) if body.strip() else {}
                query = data.get("prompt", "")
                result = engine.process_query(query)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "response": f"Plumine AI Execution Note: {str(e)}",
                    "action": "error_recovery",
                    "data": {}
                }).encode("utf-8"))
            return

        super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_server(port=7860):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(("127.0.0.1", port), PlumineHandler)
    print("=====================================================")
    print(f"  PLUMINE AI NEURAL INTERFACE ONLINE")
    print(f"  URL: http://127.0.0.1:{port}")
    print("  Autonomous On-Device Execution Engine Active")
    print("=====================================================")
    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
    except Exception:
        pass
    server.serve_forever()

if __name__ == "__main__":
    run_server()
