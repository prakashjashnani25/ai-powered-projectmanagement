import json
import requests
from langchain.llms import FakeListLLM  # For testing; replace with real LLM

class CodeAgent:
    def __init__(self, mcp_server_url="http://localhost:8000"):
        self.mcp_server_url = mcp_server_url
        self.llm = FakeListLLM(responses=["Analyzed TODOs and sent to Task Agent"])

    def fetch_todos(self, owner="octocat", repo="hello-world", path="README.md"):
        payload = {
            "method": "get_todos",
            "params": {"owner": owner, "repo": repo, "path": path},
            "id": 1
        }
        response = requests.post(self.mcp_server_url, json=payload)
        if response.status_code == 200:
            return response.json().get("result", [])
        return []

    def analyze_and_send(self, todos):
        # Simulate LLM reasoning
        prompt = f"Found TODOs: {todos}. Summarize and send to Task Agent."
        summary = self.llm(prompt)
        
        # Prepare A2A message (simulated)
        a2a_message = {
            "task_id": "task_001",
            "from": "CodeAgent",
            "to": "TaskAgent",
            "action": "add_tasks",
            "data": todos
        }
        # In real A2A, this would be sent to Task Agent's endpoint
        print(f"Simulated A2A message: {json.dumps(a2a_message, indent=2)}")
        return a2a_message

def main():
    agent = CodeAgent()
    todos = agent.fetch_todos()
    if todos:
        agent.analyze_and_send(todos)
    else:
        print("No TODOs found")

if __name__ == "__main__":
    main()