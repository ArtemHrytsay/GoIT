from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

import mimetypes, datetime
import pathlib, json
import urllib, urllib.parse, socket


MAIN_PATH = pathlib.Path()
STORAGE = MAIN_PATH / "storage" / "data.json"

class HTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == '/':
            self.send_static("index.html")
        elif url.path == "/message":
            self.send_static("message.html")
        else:
            self.send_static(url.path[1:])


    def do_POST(self):
        self.send_response(302)
        self.send_header('Location', self.path)
        self.end_headers()

        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        data = json.dumps(data_dict)

        message = data.encode()
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # client_socket.connect(("localhost", 5000))
        client_socket.sendto(message, ("localhost", 5000))


    def send_static(self, name):
        filename = MAIN_PATH / name
        if filename.exists():
            self.send_response(200)
            mimetype = mimetypes.guess_type(filename)
            if mimetype:
                self.send_header("Content-type", mimetype[0])
            else:
                self.send_header("Content-type", "text/plain")
            self.end_headers()
            with open(filename, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_static(MAIN_PATH / "error.html")



class StorageServer(Thread):

    def __init__(self, address):
        super().__init__()
        self.address = address


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.address)

        while True:
            data, address = sock.recvfrom(1024)
            timestamp = datetime.datetime.now()
            decoded_data = data.decode()

            data_dict = json.loads(decoded_data)
            data = dict()
            data[str(timestamp)] = data_dict
            jsdata = json.dumps(data)

            with open(STORAGE, "w") as file:
                file.writelines(jsdata)
                file.write('\n')

def main():
    http = HTTPServer(("localhost", 3000), HTTP)
    http_cl = Thread(target=http.serve_forever)
    http_cl.start()

    soc_server = StorageServer(("localhost", 5000))
    soc_server.start()

    http_cl.join()
    soc_server.join()


if __name__ == "__main__":
    main()
