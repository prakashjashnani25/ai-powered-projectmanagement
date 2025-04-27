# ai-powered-projectmanagement
Purpose: Create a system where multiple AI agents collaborate to manage a software project, handling tasks like code analysis, task prioritization, and team communication. 

Here we use:

MCP to connect agents to external tools/data (e.g., GitHub for code, Notion for tasks).
A2A to enable agent-to-agent communication (e.g., a code agent talks to a task agent).
LangGraph to orchestrate the workflow and manage stateful interactions.


## Workflow:

The Code Agent scans a GitHub repo, identifies issues (e.g., TODOs in code), and sends them to the Task Agent.
The Task Agent adds these to Notion, prioritizes them, and sends back a prioritized list.
LangGraph manages the workflow, ensuring agents coordinate and loop as needed.

## Tech Stack:

### Python: 
For agent logic and LangGraph.
### MCP: 
Python SDK for GitHub and Notion servers.
### A2A: 
Simulated A2A protocol (since it’s new, we’ll mimic its JSON-RPC structure).
### LangGraph: 
To define the workflow graph.
### LLM: 
Open-source model (e.g., Llama via Hugging Face) or Claude (if you have access).

#### Dependencies: 
requests, langgraph, anthropic-mcp-sdk (hypothetical, we’ll use examples).

### Dev Env Setup
python -m venv env && source env/bin/activate
pip install -r requirements.txt

requests for API calls (GitHub, Notion).
langgraph for workflow orchestration.
python-dotenv to manage API keys securel


### Running The Project

#### Start MCP Servers:
python github_mcp_server.py (port 8000).
python notion_mcp_server.py (port 8001).
#### Test Agents Individually:
Run code_agent.py to fetch TODOs and simulate A2A.
Run task_agent.py to process simulated A2A messages.

#### Run the Workflow:
Run workflow.py to execute the full graph.

Verify:
Check Notion for new tasks from GitHub TODOs.
Monitor console output for A2A messages and workflow status.