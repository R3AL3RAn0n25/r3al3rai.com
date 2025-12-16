#!/usr/bin/env python3
"""
Simple HTTP server to serve R3ÆLƎR AI demo
"""
import http.server
import socketserver
import os

class DemoHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/r3aler_ai_live_demo.html'
        return super().do_GET()

if __name__ == '__main__':
    # Change to demo-deploy directory
    demo_dir = os.path.join(os.path.dirname(__file__), 'demo-deploy')
    os.chdir(demo_dir)

    port = 8080
    with socketserver.TCPServer(("", port), DemoHTTPRequestHandler) as httpd:
        print("🚀 R3ÆLƎR AI Demo Server running on http://localhost:{}".format(port))
        print("📁 Serving files from: {}".format(demo_dir))
        httpd.serve_forever()</content>
<parameter name="filePath">c:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai\serve_demo.py