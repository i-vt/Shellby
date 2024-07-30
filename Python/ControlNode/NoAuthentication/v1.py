import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from email.parser import BytesParser
from email.policy import default

UPLOAD_DIR = 'uploads'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, code=200, content_type='text/html'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _serve_upload_form(self):
        self._set_response()
        self.wfile.write(b'''
            <html>
                <body>
                    <h2>Upload File</h2>
                    <form enctype="multipart/form-data" method="post">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </body>
            </html>
        ''')

    def _serve_file(self, filepath):
        self._set_response(content_type='application/octet-stream')
        self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(filepath)}"')
        self.end_headers()
        with open(filepath, 'rb') as file:
            self.wfile.write(file.read())

    def do_GET(self):
        if self.path == '/':
            self._serve_upload_form()
        else:
            filepath = os.path.join(UPLOAD_DIR, self.path[1:])
            if os.path.isfile(filepath):
                self._serve_file(filepath)
            else:
                self.send_error(404, "File not found")

    def do_POST(self):
        content_type = self.headers['Content-Type']
        if 'multipart/form-data' not in content_type:
            self.send_error(400, 'Content-Type must be multipart/form-data')
            return

        boundary = content_type.split("boundary=")[1].encode()
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)

        parts = data.split(b'--' + boundary)
        for part in parts:
            if b'Content-Disposition: form-data;' in part:
                headers, content = part.split(b'\r\n\r\n', 1)
                headers = BytesParser(policy=default).parsebytes(headers + b'\r\n')
                disposition = headers.get('Content-Disposition')
                if disposition and 'filename' in disposition.params:
                    filename = disposition.params['filename']
                    file_data = content.rsplit(b'\r\n', 1)[0]

                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    with open(filepath, 'wb') as output_file:
                        output_file.write(file_data)

                    self._set_response()
                    self.wfile.write(b'File uploaded successfully')
                    return

        self.send_error(400, 'File not found in request')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

