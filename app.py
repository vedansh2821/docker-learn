from http.server import BaseHTTPRequestHandler, HTTPServer
import os

from redis_store import get_visit_count


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        visit_count = get_visit_count()
        greeting = os.environ.get("APP_GREETING", "Hello from Docker!")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"{greeting} Visit #{visit_count}\n".encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), HelloHandler)
    print("Server running at http://localhost:8000")
    server.serve_forever()