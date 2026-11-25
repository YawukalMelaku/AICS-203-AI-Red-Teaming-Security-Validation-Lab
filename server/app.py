"""Loopback-only HTTP endpoint for SSH tunnel experiments."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from engine import evaluate

HOST, PORT = '127.0.0.1', 8765

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, item):
        body = json.dumps(item, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/health':
            self.send_json(200, {'ok': True, 'service': 'ICDFA AICS-203 simulated AI application',
                                 'binding': HOST, 'external_services': False})
        else:
            self.send_json(404, {'error': 'unknown route'})

    def do_POST(self):
        if self.path != '/evaluate':
            self.send_json(404, {'error': 'unknown route'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 12000:
                self.send_json(413, {'error': 'body size must be between 1 and 12000 bytes'})
                return
            payload = json.loads(self.rfile.read(length))
            self.send_json(200, evaluate(payload))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.send_json(400, {'error': str(exc)})

if __name__ == '__main__':
    print(f'ICDFA AICS-203 - listening on http://{HOST}:{PORT}', flush=True)
    print('SSH tunnel is required from another machine. Ctrl+C to stop.', flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
