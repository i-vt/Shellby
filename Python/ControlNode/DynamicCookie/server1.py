import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from email.parser import BytesParser
from email.policy import default

UPLOAD_DIR = 'uploads'
AUTH_COOKIE_NAME = 'auth_token'
AUTH_COOKIE_VALUE = 'secure_token'  

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def set_auth_cookie(self):
        self.send_response(200)
        self.send_header('Set-Cookie', f'{AUTH_COOKIE_NAME}={AUTH_COOKIE_VALUE}; HttpOnly')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Cookie set. <a href="/">Go to upload page</a>')

    def is_authenticated(self):
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookies = dict(cookie.split('=') for cookie in cookie_header.split('; '))
            return cookies.get(AUTH_COOKIE_NAME) == AUTH_COOKIE_VALUE
        return False

    def do_GET(self):
        if self.path == '/login':
            self.set_auth_cookie()
            return

        if not self.is_authenticated():
            self.send_response(401)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Unauthorized. Please <a href="/login">login</a>.')
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
        if not self.is_authenticated():
            self.send_response(401)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Unauthorized. Please <a href="/login">login</a>.')
            return

        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])

        if not content_type.startswith('multipart/form-data'):
            self.send_error(400, 'Content-Type must be multipart/form-data')
            return

        boundary = content_type.split("boundary=")[1].encode()
        data = self.rfile.read(content_length)

        # Ensure boundary starts with --
        boundary = b'--' + boundary

        # Split parts by boundary
        parts = data.split(boundary)
        parts = parts[1:-1]  # Ignore the first and last part

        for part in parts:
            if part == b'--\r\n' or part == b'--':
                continue

            part = part.lstrip(b'\r\n').rstrip(b'\r\n--')
            headers, body = part.split(b'\r\n\r\n', 1)

            headers = BytesParser(policy=default).parsebytes(headers)
            disposition = headers.get('Content-Disposition')
            if disposition and 'filename' in disposition.params:
                filename = disposition.params['filename']

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

