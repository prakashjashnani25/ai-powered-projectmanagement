import json
import os
from dotenv import load_dotenv
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

class MCPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request_data = json.loads(self.rfile.read(content_length))
        
        # Handle MCP request (simplified)
        if request_data.get("method") == "get_todos":
            params = request_data.get("params", {})
            owner = params.get("owner", "octocat")
            repo = params.get("repo", "hello-world")
            path = params.get("path", "README.md")
            
            # Fetch file content from GitHub
            headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
            response = requests.get(REPO_URL.format(owner=owner, repo=repo, path=path), headers=headers)
            if response.status_code == 200:
                content = response.json().get("content", "")
                # Decode base64 content (simplified)
                import base64
                decoded = base64.b64decode(content).decode("utf-8")
                todos = [line for line in decoded.split("\n") if "TODO" in line]
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"result": todos}).encode())
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to fetch repo"}).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unknown method"}).encode())

def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, MCPServer)
    print(f"Starting MCP GitHub server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()