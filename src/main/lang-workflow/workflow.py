from langgraph.graph import StateGraph, END
from typing import Dict, Any
from code_agent import CodeAgent
from task_agent import TaskAgent

class WorkflowState:
    def __init__(self):
        self.todos = []
        self.task_result = None

def run_code_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    agent = CodeAgent()
    state["todos"] = agent.fetch_todos()
    return state

def run_task_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    agent = TaskAgent()
    message = {
        "task_id": "task_001",
        "from": "CodeAgent",
        "to": "TaskAgent",
        "action": "add_tasks",
        "data": state["todos"]
    }
    state["task_result"] = agent.process_a2a_message(message)
    return state

def build_graph():
    workflow = StateGraph(WorkflowState)
    workflow.add_node("code_agent", run_code_agent)
    workflow.add_node("task_agent", run_task_agent)
    workflow.add_edge("code_agent", "task_agent")
    workflow.add_edge("task_agent", END)
    workflow.set_entry_point("code_agent")
    return workflow.compile()

def main():
    graph = build_graph()
    result = graph.invoke(WorkflowState())
    print(f"Workflow completed: {result.task_result}")

if __name__ == "__main__":
    main()