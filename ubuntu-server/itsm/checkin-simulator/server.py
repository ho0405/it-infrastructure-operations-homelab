from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"service":"checkin-simulator","status":"healthy"}\n'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            body = b"Not Found\n"
            self.send_response(404)

        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("127.0.0.1", 8100), Handler).serve_forever()
