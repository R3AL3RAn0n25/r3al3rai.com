#!/usr/bin/env python3
"""
Simple demo server for R3ALER AI React frontend
"""
import http.server
import socketserver
import json
import os
import time

class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            # Serve React app
            build_dir = os.path.join(os.path.dirname(__file__), 'application', 'Backend', 'build')
            if os.path.exists(build_dir):
                os.chdir(build_dir)
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_api(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.path == '/api/thebrain':
            response = {
                'success': True,
                'response': 'Hello! I am R3ALER AI. This is a demo response. The full AI system integrates with knowledge bases, adaptive learning, and specialized tools for advanced AI capabilities.'
            }
        elif self.path == '/api/auth/login':
            response = {
                'success': True,
                'token': 'demo-token',
                'user': {'username': 'demo', 'id': 1}
            }
        elif self.path == '/api/roles':
            response = {
                'success': True,
                'roles': [
                    {'name': 'Assistant', 'description': 'General AI assistant'},
                    {'name': 'Coder', 'description': 'Programming expert'},
                    {'name': 'Researcher', 'description': 'Academic research'}
                ]
            }
        else:
            response = {'success': True, 'message': 'Demo API endpoint'}

        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    port = 3000
    print("R3ALER AI React Demo Server")
    print("Serving on http://localhost:" + str(port))

    with socketserver.TCPServer(("", port), DemoHandler) as httpd:
        httpd.serve_forever()