import time
from http.server import HTTPServer
from server.server import MainServer

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MainServer)

    print(time.asctime(), f"Server running on : {HOST_NAME}, Port: {PORT_NUMBER}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print(time.asctime(), f"Server going down: {HOST_NAME}, Port: {PORT_NUMBER}")