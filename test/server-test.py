import http.server
from urllib.parse import urlparse, parse_qs
import json


class requestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = url.query
        if False:
            pass
        else:
            self.serve_html()


    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        query = url.query

        if path == '/register':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            length = int(self.headers['Content-Length'])
            request_content = json.loads(self.rfile.read(length).decode('utf-8'))
            print(request_content['auth']['user-name'])
            print(request_content['auth']['password'])

    def serve_html(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        file = open('test\index.html', 'rb')
        html = file.read()
        self.wfile.write(html)

if __name__ == '__main__':
    server = http.server.HTTPServer(('', 8000), requestHandler)
    server.serve_forever()