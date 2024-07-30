import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from email.parser import BytesParser
from email.policy import default
import base64

UPLOAD_DIR = 'uploads'
USERNAME = 'admin'
PASSWORD = 'password'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Unauthorized')

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
            return False
        
        auth_type, auth_string = auth_header.split(' ', 1)
        if auth_type.lower() != 'basic':
            self.do_AUTHHEAD()
            return False
        
        auth_bytes = base64.b64decode(auth_string)
        auth_decoded = auth_bytes.decode('utf-8')
        username, password = auth_decoded.split(':', 1)

        if username == USERNAME and password == PASSWORD:
            return True
        else:
            self.do_AUTHHEAD()
            return False

    def do_GET(self):
        if not self.authenticate():
            return

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
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
        else:
            filepath = os.path.join(UPLOAD_DIR, self.path[1:])
            if os.path.isfile(filepath):
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(filepath)}"')
                self.end_headers()
                with open(filepath, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")

    def do_POST(self):
        if not self.authenticate():
            return

        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])

        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {content_length}")

        if not content_type.startswith('multipart/form-data'):
            self.send_error(400, 'Content-Type must be multipart/form-data')
            return

        boundary = content_type.split("boundary=")[1].encode()
        data = self.rfile.read(content_length)
        print(f"Raw Data: {data}")

        # Ensure boundary starts with --
        boundary = b'--' + boundary

        # Split parts by boundary
        parts = data.split(boundary)
        parts = parts[1:-1]  # Ignore the first and last part
        print(f"Parts: {parts}")

        for part in parts:
            if part == b'--\r\n' or part == b'--':
                continue

            part = part.lstrip(b'\r\n').rstrip(b'\r\n--')
            headers, body = part.split(b'\r\n\r\n', 1)
            print(f"Headers: {headers}")
            print(f"Body: {body}")

            headers = BytesParser(policy=default).parsebytes(headers)
            disposition = headers.get('Content-Disposition')
            if disposition and 'filename' in disposition.params:
                filename = disposition.params['filename']
                print(f"Filename: {filename}")

                # Save the file
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, 'wb') as output_file:
                    output_file.write(body)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
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

