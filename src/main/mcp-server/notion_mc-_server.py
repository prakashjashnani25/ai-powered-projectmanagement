import json
import os
from dotenv import load_dotenv
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
NOTION_API = "https://api.notion.com/v1/pages"

class MCPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request_data = json.loads(self.rfile.read(content_length))
        
        if request_data.get("method") == "add_task":
            params = request_data.get("params", {})
            task = params.get("task", "")
            
            # Add task to Notion
            headers = {
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            payload = {
                "parent": {"database_id": NOTION_DB_ID},
                "properties": {
                    "Name": {"title": [{"text": {"content": task}}]},
                    "Priority": {"select": {"name": "Medium"}}
                }
            }
            response = requests.post(NOTION_API, headers=headers, json=payload)
            
            if response.status_code == 200:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"result": "Task added"}).encode())
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to add task"}).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unknown method"}).encode())

def run_server(port=8001):
    server_address = ("", port)
    httpd = HTTPServer(server_address, MCPServer)
    print(f"Starting MCP Notion server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()