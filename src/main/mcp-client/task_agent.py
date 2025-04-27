import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from langchain.llms import FakeListLLM

class TaskAgent:
    def __init__(self, mcp_server_url="http://localhost:8001"):
        self.mcp_server_url = mcp_server_url
        self.llm = FakeListLLM(responses=["Prioritized tasks and added to Notion"])

    def add_task(self, task):
        payload = {
            "method": "add_task",
            "params": {"task": task},
            "id": 1
        }
        response = requests.post(self.mcp_server_url, json=payload)
        return response.status_code == 200

    def process_a2a_message(self, message):
        todos = message.get("data", [])
        prompt = f"Received TODOs: {todos}. Prioritize and add to Notion."
        result = self.llm(prompt)
        
        for todo in todos:
            if self.add_task(todo):
                print(f"Added task: {todo}")
            else:
                print(f"Failed to add task: {todo}")
        return {"status": "completed", "result": result}

class A2AServer(BaseHTTPRequestHandler):
    def __init__(self, task_agent, *args, **kwargs):
        self.task_agent = task_agent
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        message = json.loads(self.rfile.read(content_length))
        
        if message.get("action") == "add_tasks":
            result = self.task_agent.process_a2a_message(message)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unknown action"}).encode())

def run_a2a_server(task_agent, port=8002):
    server_address = ("", port)
    httpd = HTTPServer(server_address, lambda *args, **kwargs: A2AServer(task_agent, *args, **kwargs))
    print(f"Starting A2A server on port {port}...")
    httpd.serve_forever()

def main():
    agent = TaskAgent()
    # Simulate receiving A2A message from Code Agent
    test_message = {
        "task_id": "task_001",
        "from": "CodeAgent",
        "to": "TaskAgent",
        "action": "add_tasks",
        "data": ["TODO: Update README", "TODO: Fix bug"]
    }
    agent.process_a2a_message(test_message)

if __name__ == "__main__":
    main()