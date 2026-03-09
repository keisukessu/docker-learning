from http.server import HTTPServer, BaseHTTPRequestHandler


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
        <body>
            <h1>Hello from Docker!</h1>
            <p>Python Web サーバーがコンテナ内で動いています。</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[アクセス] {args[0]} {args[1]}")


if __name__ == '__main__':
    print("サーバーを起動します: http://localhost:8080")
    server = HTTPServer(('0.0.0.0', 8080), HelloHandler)
    server.serve_forever()
