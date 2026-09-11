import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from ai_engine import PlumineAIEngine

engine = PlumineAIEngine()

class PlumineHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(body)
                query = data.get("prompt", "")
                result = engine.process_query(query)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
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
    print(f"=====================================================")
    print(f"  PLUMINE AI NEURAL INTERFACE ONLINE")
    print(f"  URL: http://127.0.0.1:{port}")
    print(f"  Autonomous On-Device Execution Engine Active")
    print(f"=====================================================")
    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
    except Exception:
        pass
    server.serve_forever()

if __name__ == "__main__":
    run_server()
