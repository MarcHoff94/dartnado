import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
from enum import Enum

class ServerMessageType(Enum):
    NEW_GAME = 'New_Game'
    NEW_ROUND = 'New_Round'

    def __dict__(self) -> dict:
        return {self.name: self.value}

@dataclass
class ServerMessage():
    type: ServerMessageType
    data: dict
    
    def __dict__(self) -> dict:
        return {'type': self.type.value, 'data': self.data}

class MainServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
    
   
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            match data['type']:
                case 'Throw':
                    #Tournament muss throw handeln und nächste action zurückgeben
                    msg = ServerMessage(ServerMessageType.NEW_ROUND, {'instert': 'Roundobject here'})
                    self.respond('application/json', json.dumps(msg.__dict__()).encode())
        except Exception as e:
            self.respond('test/plain', f"Error occurred while processing data: {e}".encode('utf-8') )

    
    def do_GET(self):
        self.respond()

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
    
    def respond(self, content_type, content):
        self.handle_http(200, content_type)
        self.wfile.write(content)

