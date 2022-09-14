import http.server
from urllib import response
from urllib.parse import urlparse, parse_qs
import json


class requestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)
        if path == '/search-album-id':
            album_id = query['target']
            print(album_id[0])
            self.send_response(200)
            self.send_header('Content-Type', 'application/json;charset=UTF-8')
            album_info = {
                "name": "cxk_album",
                "artist": "cxk",
                "tracks": [
                    {"trackID": "001", "trackName": "jntm"},
                    {"trackID": "002", "trackName": "rap"},
                ]
            }
            response_content = json.dumps(album_info).encode('utf-8')
            self.send_header('Content-Length', len(response_content))
            self.end_headers()
            self.wfile.write(response_content)

        else:
            self.serve_html()

    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        query = url.query

        if path == '/register':
            self.send_response(200)
            length = int(self.headers['Content-Length'])
            request_content = json.loads(
                self.rfile.read(length).decode('utf-8'))
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
