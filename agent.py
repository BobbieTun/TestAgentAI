# agent.py
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
# .\venv\Scripts\Activate.ps1  - to activate the venv
# -------------------- TOOLS --------------------

def search_semantic_libraries(query: str) -> str:
    """Danh sách thư viện Python cho semantic search"""
    data = [
        "FAISS – efficient vector similarity search",
        "Chroma – open-source embedding database",
        "Pinecone – managed vector database",
        "Weaviate – vector search engine with schema",
        "Haystack – full-text + semantic search framework",
        "Sentence Transformers – embeddings for semantic search",
        "Gensim – topic modeling and similarity analysis",
        "OpenAI API – embeddings for semantic search"
    ]
    return "\n".join(data)

def calculator_tool_func(expression: str) -> str:
    """Tính toán biểu thức Python"""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"

# Tạo tools theo LangChain mới
search_tool = StructuredTool.from_function(
    search_semantic_libraries,
    name="search_tool",
    description="Tìm thư viện Python cho semantic search"
)

calculator_tool = StructuredTool.from_function(
    calculator_tool_func,
    name="calculator_tool",
    description="Tính toán biểu thức Python"
)

TOOLS: Dict[str, StructuredTool] = {
    "search_tool": search_tool,
    "calculator_tool": calculator_tool
}

# -------------------- STATE --------------------
class AgentState(TypedDict):
    messages: List

# -------------------- LLM --------------------
import os
api_key = "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"


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=api_key
).bind_tools(list(TOOLS.values()))

# -------------------- AGENT NODE --------------------
def agent_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# -------------------- TOOL NODE --------------------
def tool_node(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]
        tool_name = tool_call["name"]
        args = tool_call["args"]
        result = TOOLS[tool_name].invoke(args)
        return {"messages": state["messages"] + [HumanMessage(content=result)]}
    return state

# -------------------- ROUTER --------------------
def route(state: AgentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    return END

# -------------------- GRAPH --------------------
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tool", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", route, {"tool": "tool", END: END})
graph.add_edge("tool", "agent")
app = graph.compile()

# -------------------- CLI --------------------
print("=== AgentAI CLI ===")
print("Nhập 'exit' để thoát.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break

    result = app.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    for msg in result["messages"]:
        print("AI:", msg.content)
    print("-" * 40)
