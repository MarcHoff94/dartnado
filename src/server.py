import json
from http.server import BaseHTTPRequestHandler
from Game.Game import Throw

class MainServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
    
   
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Data received successfully: {data}".encode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error occurred while processing data: {e}".encode('utf-8'))

    
    def do_GET(self):
        self.respond()

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes("180!!", "UTF-8")
    
    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)

